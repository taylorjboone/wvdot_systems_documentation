# BMS — Business Logic

Internal reference for the Bridges and BMS pages: where the data comes from,
how the plan engine works, and the rules behind runs, validation, committed
projects and the outlooks. User-facing help is the
[Bridges & BMS Usage Guide](/docs/BMS_Usage); the Bridge Wizard has its own
[logic reference](/docs/Bridge_Wizard_Logic).

## Contents

1. [Data and storage](#1-data-and-storage)
2. [Bridge inventory, inspections, 3D floods](#2-bridge-inventory-inspections-3d-floods)
3. [The plan engine](#3-the-plan-engine) (with [Configurations](#configurations) and [the dTIMS model](#the-dtims-model))
4. [Plan runs](#4-plan-runs)
5. [Run validation](#5-run-validation)
6. [Projects, TheHub and the outlooks](#6-projects-thehub-and-the-outlooks)
7. [Bridge Wizard](#7-bridge-wizard)
8. [Known gaps](#8-known-gaps)

## 1. Data and storage

- **Inventory**: the AssetWise extract `bridges_all.duckdb` (`INSPECT_DB`),
  opened read-only per request through `bridges/inventory_db.py`. It is
  EAV: current values in `asset_value`, per-inspection values in
  `report_value`, both keyed by `field_id`; NBI and SNBI carry the same
  concept under different field ids (`CANONICAL_RATINGS`,
  `v_canonical_rating`). A missing extract answers 503 on the bridge
  endpoints only.
- **Scope**: planning, LISA and the flood scenes cover WVDOT-owned bridges
  (B.CL.01 owner, `field_id = 2300201`, `'S01'`) that are in service — about
  7,100 of the 8,700 structures. The inventory pages list every structure.
- **Everything else** lives in the PMS database, schema `bms` (migrations
  043–046): `lisa_configs`, `deterioration_models`, `treatments`,
  `budget_scenarios`, `committed_projects`, `runs`, `run_logs`,
  `run_bridge_years`, `run_plan_edits`, `run_plan_state`, `bridge_lrs`,
  `flood3d_*`, `wizard_conversations`, `wizard_responses`,
  `wizard_artifacts`. `bms/store.py` connects with `search_path = bms,
  public`, so bridge SQL never touches the pavement tables of the same name.
  `scripts/bms_import.py` copied the standalone inspect_tech `bms` database
  in once (v1.8.0).
- **Users and roles** are PMS's (`app_users`, `app_user_districts`). Bridge
  districts are stored as text (`'01'`, `'1'` … `'10'`) and compared as
  integers. Every write needs `require_admin`, or `current_user` and
  `can_see(district)` for district-scoped validation edits.
- **Costs** go through one function, `bms/cost.treatment_cost`: $/sf under
  the treatment's cost basis × cost area (deck area B.G.16; length × width
  for culverts and zero-area records) × (1 + inflation)^(years after the
  start year).
- **Domain separation**: bridge condition is NBI 0–9 plus LISA 0–100; nothing
  here uses the pavement indices, GFP or `engine/`.

## 2. Bridge inventory, inspections, 3D floods

#### Data source

- The pages read the AssetWise extract `bridges_all.duckdb`. It is opened
  read-only, per request, through `bridges.inventory_db.db_conn()`. Its
  location is the `INSPECT_DB` setting:
  - locally it defaults to `~/Downloads/inspect_tech/analysis/bridges_all.duckdb`;
  - on mmsdev it is the mounted `/bms_fixtures/bridges_all.duckdb`.
- If the file is missing, the API answers `503`.
- The app never writes the extract.
- Coordinates outside West Virginia (`bridges.queries.WV_BBOX`: latitude
  37.0–40.8, longitude −82.8 to −77.0) read as missing (`wv_point`) in the
  bridge list and the BMS inventory.
  - A few AssetWise records carry a longitude without its minus sign
    (45A101, 32A103 at +80.48) or 0 / 0. Mapped as-is, those put a bridge in
    Asia and zoom every fitted map out to the world.
  - The coordinate isn't guessed; such bridges simply don't appear on maps.
- **`qv_inspection_card`** is a precomputed table with one row per inspection:
  - the six card ratings (SNBI first, NBI fallback);
  - the report-value, narrative, attachment, type and inspector counts;
  - the inspection types and inspectors, sorted alphabetically;
  - the PDF flag.

  `/api/bridges/{bars}/inspections` reads it by `ast_id`. The same list computed
  live from `report_value` (34M rows, no index) took about 70 s on mmsdev,
  where the 8 GB extract doesn't fit in the page cache. The table serves it in
  milliseconds. `python -m pipeline bridges sync` rebuilds it after
  `qv_bootstrap.sql` (`bridges.queries.inspection_card_table_sql`). An extract
  without it falls back to the live query.
- **`qv_bridge_list`** is a precomputed table with one row per bridge for the
  bridge list (`bridges.queries.bridge_list_table_sql`):
  - the identity and latest-inspection columns the list always had;
  - the NBI design type (43B) from `qv_bridge_decoded`, its family
    (`TYPE_GROUPS`: girder, box, slab, truss, arch, cable, frame, culvert,
    other), the material and the number of spans;
  - the facility carried and the feature intersected;
  - the longest span and total length in feet (SNBI field first, then the
    legacy NBI item; `SPAN_FIELDS`);
  - the current deck, superstructure, substructure, culvert, channel, scour
    and railing ratings (SNBI where recorded, else the legacy NBI item, as
    `bms/inventory.py`), NBI 67 structural evaluation, `lowest_rating` (the
    lowest of deck / super / sub / culvert) and `condition` (good 7–9, fair
    5–6, poor 0–4, unrated);
  - context for the advanced filters: deck area (B.G.16), NHS (B.H.03 Y / N,
    else NBI 104 = 1), ADT (B.H.09, else `qv_bridge_decoded.adt`), owner and
    `is_wvdot_owned`, `insp_freq_months`, and `next_inspection_due` (the last
    inspection date plus the interval).

  `python -m pipeline bridges sync` rebuilds it after `qv_inspection_card`
  (about 0.5 s). An extract without it falls back to the same query run live
  (`_list_source`), which is slower but gives the same rows.
- **`qv_traffic_load_history`** (`bridges.queries.traffic_load_table_sql`,
  rebuilt by `pipeline bridges sync`, under 1 s): one row per inspection that
  recorded traffic or load rating — NBI 29 ADT and 30 its year, 109 truck %,
  41 posting, 63–66 rating methods and operating / inventory ratings (metric
  tons); SNBI B.H.09–11 AADT, AADTT and year, B.LR.03–07 rating date, method
  and inventory / operating / legal rating factors — with `truck_adt` (SNBI
  AADTT, else ADT × truck % / 100), `traffic_year` and `source` (SNBI when an
  SNBI item is present). About 67,000 inspections on 8,600 bridges, 2001→.
- **InfoBridge climate** (`pipeline bridges infobridge --file …`): the FHWA
  InfoBridge "Selected Bridges" export — one row per structure per NBI year
  (1992→2025) with ADT, condition, deck area and gridded climate — loaded as
  `ib_bridge_year` (`bars` and `as_id` where the structure number's last six
  characters are an inventory BARS: about 8,100 of 9,650 structures; the rest
  are bridges retired before AssetWise or non-BARS structures) and summarised
  per bridge as `qv_bridge_climate` (averages and latest values). The app
  only reads them; the Bridge Wizard and `run_python` can query them.
- The queries are in `bridges/queries.py`. The routes are in
  `api/routes/bridges.py`: they are synchronous and run in the thread pool.
  Response shapes are kept identical to inspect_tech's original API.

#### Endpoints

All endpoints are GET, sit behind the `require_sign_in` middleware (401
without a session) and are read-only.

| Endpoint | Returns |
|---|---|
| `/api/bridges` | One page of the bridge list from `qv_bridge_list` (below), filtered, sorted and paged in DuckDB. Query: `search` (ILIKE over BARS, code, local / bridge name, county, facility, feature intersected, design type), and repeated-key lists `district` (compared as integers, so `01` = `1`), `county` (case-insensitive), `type` (family: girder, box, slab, truss, arch, cable, frame, culvert, other), `material`, `status`, `condition` (good, fair, poor, unrated); values of one key are OR'd, keys AND'd. Advanced: repeated `range=col:lo:hi` (either end optional; `LIST_RANGES`: deck, super, sub, culvert, channel, scour, year_built, adt, max_span_ft, total_length_ft, deck_area_sf, num_spans, insp_freq_months, last_inspection_year) and `flag` (`LIST_FLAGS`: nhs, wvdot, overdue = `next_inspection_due < current_date`, scour_critical = scour ≤ 3, in_service; plus mms / hub, resolved to a BARS list from `bms.bridge_spend` rows with amount > 0), each AND'd. Repeated `bars` (exact BARS, upper-cased) keeps only those bridges, AND'd with the rest; the search box uses it to preview one bridge. Per-component bands: repeated `rating=component:band` (deck, super, sub, culvert, channel, scour × good 7–9 / fair 5–6 / poor 0–4; bands of one component OR'd, components AND'd). `sort` = bars, local_name, district, county_name, type, max_span_ft, total_length_ft, year_built, lowest_rating, last_inspection_date, inspection_count, mms_spend, hub_spend; `dir` asc / desc (nulls last); `limit` (default 50, ≤ 20000) / `offset`. Returns `{total, limit, offset, rows}`. Each row carries `mms_spend` / `hub_spend` from `bms.bridge_spend` (read for the page's bridges; a spend sort reads the whole filtered set and pages in Python). |
| `/api/bridges/facets` | The filter values with counts over the whole inventory: `district`, `county` (upper-cased), `type` (with its `label`), `material`, `status`, `condition`, and `total`; `ranges` (min / max of each `LIST_RANGES` column, for the sliders), `flags` (bridges with each flag, mms / hub from `bms.bridge_spend`) and `ratings` (bridges in each band of each component). |
| `/api/bridges/points` | The bridges matching the same `search` / filter keys (including `condition`, `range`, `flag`, `rating`, `bars`) as a GeoJSON FeatureCollection of points (type family, design type, material, status, district, county, year built, spans, longest span, length, lowest rating, last inspection), with `matched` and `located`. Coordinates outside WV are left off (`wv_point`). |
| `/api/bridges/health` | `{ok, db, bridges, inspections}` |
| `/api/bridges/{bars}` | The asset row, the curated identification, every `asset_value`, the inspection count and the last inspection |
| `/api/bridges/{bars}/inspections` | The history, with the six card ratings (deck, super, sub, culvert, channel, scour), counts, `status_bucket` and `has_pdf` Served from `qv_inspection_card` (below). |
| `/api/bridges/{bars}/traffic-load` | Truck traffic and load rating at every inspection, oldest first, from `qv_traffic_load_history` (below; computed live on an extract without it), plus `nbi_years`: the NBI ADT, condition and deck area of every FHWA year InfoBridge has for the bridge (`ib_bridge_year`, when loaded). 404 for an unknown BARS. |
| `/api/bridges/{bars}/nbi-history` | Every inspection's component ratings, oldest first, from `qv_nbi_timeseries` (SNBI where recorded, else the legacy NBI item; all owners). Per row: `ast_id`, `insp_date`, `report_type`, `source` (NBI / SNBI / MIXED), and deck / super / sub / culvert / channel / scour / railing as integers plus their `*_raw` strings. 404 for an unknown BARS. |
| `/api/bridges/spend` | Every bridge's MMS work cost (`mms: {BARS: {cost, tasks, last_date}}`) and TheHub spend, split in `hub` (projects that are BMS treatments), `hub_inspection` (bridge inspections, code 49) and `hub_other` (every other linked project), each `{BARS: {spent, projects}}`, for the bridges table, read from `bms.bridge_spend` (refreshed nightly, see below), with `mms_refreshed_at` / `hub_refreshed_at` / `hub_inspection_refreshed_at` / `hub_other_refreshed_at`. `*_error` is set only when a source has never been refreshed. List rows carry `hub_inspection_spend` and `hub_other_spend` next to `hub_spend`. |
| `/api/bridges/{bars}/mms` | MMS (dTIMS OM) work recorded on the bridge, per task (see *MMS work on a bridge* below). Live on every call; 422 for a malformed BARS, 503 when TheHub / OM can't be reached. |
| `/api/bridges/{bars}/cover` | The newest `af_cover` photo, otherwise any photo of the newest inspection; 404 when there is none |
| `/api/bridge-inspections/{ast_id}` | The inspection, its bridge, inspectors, types and identification (as-inspected `report_value` overrides `asset_value`) |
| `…/sections` | The 15 narrative sections, the canonical ratings plus `ratings_generation`, the SNBI (`B.C.%`, `B.AP.%`) and NBI rating rows, and the identification grid |
| `…/values` | `report_value` rows, filtered by `search` / `prepopulated` and paged (≤ 5000) |
| `…/elements` | `asset_element` rows. These are stored per bridge, so every inspection of a bridge returns the same list. |
| `…/attachments` | Mapped files, cover first, with a MIME type guessed from the file extension |
| `…/layout` | The report layout (see below) |
| `…/pdf` | `pdf_blob`, otherwise the fallback file (see below); 404 when neither exists |
| `/api/bridge-files/{af_id}/data` | The file bytes. The MIME type is sniffed from the magic bytes (JPEG, PNG, GIF, PDF, BMP, ZIP → docx/xlsx), falling back to the extension. Sent inline. |
| `/api/bridge-fields/{field_id}` | The `field` row |
| `/api/bridge-assets/{as_id}` | The asset row, plus `/sub-assets`, `/schedules`, `/critical-findings`, `/files` (with `is_mapped`), `/segments` and `/everything` (the one-shot Asset page payload with totals) |

#### MMS work on a bridge (dTIMS OM)

The bridge page's **MMS work** tab is the smartcar-mms DDL (daily detail
listing, `mms-backend/mms/api/resources/ddl.py`), ported to read dTIMS OM
directly and cut down to one bridge. Code: `bridges/mms.py`.

**Connection.**
- OM is read through TheHub's SQL Server connection, using the linked server
  `[TAMSDW]` (database `OM_WVDOT`, schema `operations`).
- The only entry point is `api/hub_client.openquery(inner_sql)`, which wraps
  `SELECT * FROM OPENQUERY([TAMSDW], '…')`.
- It is read-only and uncached: every request queries OM again.
- The BARS is checked against `^\d{2}[A-Z]\d{3}$` before it goes into the
  SQL.
- The OM tables are versioned, so every join filters `ValidTo IS NULL`.

**Queries (two round trips).**
1. **Tasks.** The tasks whose `TaskAssetReference` points at an
   `AssetReference` whose `DisplayName` is the BARS.
   - For each task: `TaskId`, `TaskOrderId`, name, organization, the activity
     (`PerformanceStandard` code and description) and the task's unit.
   - Also the bridge's `AssetReferenceId`s.
   - If no task references the bridge, the second query is skipped.
2. **Work.** For those tasks:
   - **accomplishments**: every `DailyWorkReportLineItem`, grouped by task,
     day, `AssetReferenceId` and unit (sum of `Accomplishment`, line count,
     first line);
   - **transactions**: `BaseTransaction` joined to `LaborTransaction`,
     `EquipmentTransaction`, `StockpileTransaction` and `OtherCost`, giving
     quantity (hours or stockpile quantity) and `TransactionTotalCost` per
     task, day and kind. This is the DDL's `mv_task_day_costs`.
   - Estimated and posted transactions are both counted, as in the DDL (no
     `Confirmed` filter).

**Allocation (`ddl_rows`, line for line from the DDL).**
- For each task-day, each line's share is its accomplishment ÷ the day's
  total. When the day's total is 0, the share is 1 ÷ the number of lines.
- Each kind's hours / quantity and cost for the day are multiplied by the
  line's share.
- A day with transactions but no lines becomes one row with no asset.
- Rows are dropped when both the accomplishment and the cost round to 0
  (and so are days where both totals do).

**Scoping to the bridge (`summarize`).**
- Only rows whose `AssetReferenceId` is one of the bridge's are kept.
- Asset-less cost-only days can't be placed on a bridge, so they are left out.
  For 01A001, OM's task total of $1,869.82 includes a $34.21 cost-only day,
  so the page shows $1,835.61.
- Per task, the page gets:
  - the accomplishment by unit (the main unit first), hours and costs by
    kind, and the total;
  - the first and last day, and the number of days;
  - `om_url`: the task in dTIMS OM. The link is set by `DTIMS_OM_TASK_URL`
    (default `https://wvdotom.wvoasis.gov/om/entity/task/{task_id}`) and
    shown as the `TaskOrderId`.
- The summary gives task counts (with lines on the bridge / linked), cost by
  kind, accomplishments by unit, first and last day, and cost by activity.

**Every bridge at once (`spend_by_bridge`, the bridges table).** Read
nightly into `bms.bridge_spend`, not per page view (see *Nightly bridge
spend refresh* below).
- `SPEND_SQL` runs the same allocation inside OM, in one aggregate over
  every task that references an asset named like a BARS
  (`AssetReference.DisplayName LIKE '[0-9][0-9][A-Z][0-9][0-9][0-9]'`).
- A line's share of its task-day's transaction cost is its accomplishment
  ÷ the day's total, or 1 ÷ the number of lines when that total is 0.
- The shares of the lines on each BARS's assets are summed.
- Cost-only days are left out, as on the bridge page. The DDL's
  drop-if-both-round-to-zero filter only removes amounts under half a cent,
  so it isn't repeated.
- It agrees with `bridge_mms` to the cent (01A001 $1,835.61, 03A030
  $4,538.74). It covers about 6,800 bridges, about $25.8M statewide, in
  about 4 s.

**TheHub money on a bridge: split by deck area (`bms/hub.deck_area_shares`).**
- A TheHub project's money belongs to the bridges it names in proportion to
  their deck area (B.G.16, `deck_area_sf`): share = the bridge's deck area ÷
  the project's total. A bridge with no deck area recorded is weighted as the
  average of the project's bridges that have one; with none recorded the
  money splits evenly. Shares sum to 1, so every dollar is counted once.
- This is the one rule, used everywhere TheHub money is put on a bridge:
  - the nightly per-bridge spend (below) and the bridge list's TheHub spend
    column;
  - every project the TheHub routes return (`bridges[].share`,
    `allocated_estimate`, `allocated_spent`), and `this_bridge` on
    `GET /api/bms/hub/bridges/{bars}/projects` (the bridge page's TheHub tab
    and NBI history cards);
  - the project panel's bridge table;
  - the BMS project page's cost comparison, which scales TheHub's figures to
    the share of the project's bridges it holds;
  - the committed-project seed (`cost_share`, below);
  - the Bridge Wizard's `hub_projects` and `bridge_spend` tools.
- Shares are over every bridge the project names, including other owners and
  bridges outside the inventory.

**TheHub spend per bridge (`bms/hub.spend_by_bridge`).**
- It is each bridge's share (above) of the `actual_spent` (OASIS, all phases)
  of every TheHub project linked to it (`ASSOCIATED_*_SQL`: any link, any work,
  any status), with deck areas from `qv_bridge_list`.
- It is split by `category_of`: `spent` / `projects` for the projects that
  are BMS treatments, `inspection_spent` / `inspection_projects` for bridge
  inspections (construction code 49, `INSPECTION_CODES`; not 72, construction
  inspection), `other_spent` / `other_projects` for the rest. A project that
  is both a treatment and an inspection counts as a treatment.
- A project that names the bridge twice counts once.
- The columns add up across bridges. On 2026-09-30: treatments $2.25B on
  2,149 bridges, inspections $46.0M on 68, other work $1.71B on 1,476 (the
  bridge-code projects over the two old links came to $2.26B).

**How TheHub links a project to a bridge (`bms/hub.LINKS_CTE`).**
- Four columns, all pointing at `dbo.PrimaryNBIBridge` (the BARS is the last
  six characters of its NBI code):
  - `Project.PrimaryNbiBridgeID` (`link = primary`);
  - `RouteSegment.RoutePrimaryNbiBridgeID` (`segment`);
  - `FederalFundingDetailSegment.PrimaryNBIBridgeId` and
    `FederalFundingDetail.NoGISPrimaryNBIBridgeId` (`funding`): the FMIS
    location of each funding line.
- Multi-bridge jobs often name most of their bridges only on funding lines
  (TheHub 2016001061 "I-70 BRIDGES": 1 primary bridge, 1 on a route segment,
  23 on funding lines). Before 2026-09-30 only the first two were read, so
  such a project's money sat on one or two bridges.
- `BRIDGES_SQL` returns one row per project and bridge, with `is_primary` and
  the strongest `link` (primary > segment > funding).

**BMS treatment projects (`bms/hub.treatment_map`, `treatments_of`).**
- A TheHub project is a BMS treatment when one of its construction codes
  (primary or additional) is in the `hub_codes` of an active treatment of the
  system default BMS configuration; the first treatment listing a code wins,
  as in `bms.committed.map_treatments`. Cached 5 minutes.
- Every project the TheHub routes return carries `treatments`
  (`[{code, name, category, hub_code}]`), `is_treatment` and `category`
  (`treatment` | `inspection` | `other`); the UI shows them as treatment or
  Inspection chips (`ui/src/components/bms/planning/TreatmentChip.tsx`,
  coloured by kind of work, never by condition).

**Nightly bridge spend refresh.**
- `bms.bridge_spend` (migrations 049, 058) holds one row per source (`mms`, `hub`, `hub_inspection`, `hub_other`)
  and BARS: `amount`, `items` (tasks / projects), `last_date` and
  `refreshed_at`.
- `python -m pipeline bridges spend [--source mms|hub|hub_inspection|hub_other|all] [--dry-run]
  [--force]` (`pipeline/bridges/spend.py`) refreshes it.
  - Each source is read, checked and swapped in on its own: one transaction
    deletes that source's rows and inserts the new ones.
  - A source that can't be read keeps its previous rows, and the other
    source still refreshes.
  - The check refuses an empty read, and a read with under half the bridges
    the source had before (a partial read), unless `--force`.
  - It writes one `data_refresh_log` row (stage `bridges_spend`) with each
    source's rows and totals, before and after.
- The API runs it nightly (`bridges/spend_nightly.py`).
  - Each worker starts a thread at startup. Every 30 minutes it checks
    whether either source was last refreshed before the latest scheduled
    time, `BRIDGE_SPEND_REFRESH_AT` (default `02:30`, America/New_York).
  - If so, it takes a Postgres advisory lock, re-checks and refreshes the
    stale sources, so exactly one worker does the work.
  - A deploy after the scheduled time catches up at the first check, about
    90 s after start.
  - After a failed attempt it waits 2 hours before trying again.
  - `BRIDGE_SPEND_NIGHTLY=0` turns the thread off (the tests set it).

#### Curated fields and ratings

**Identification fields.** `IDENTIFICATION_FIELDS` maps 15 fields to their
field ids:

- bridge name 2300002, BARS 1049, control number 1, local name 903;
- county 1050, county code 2300102, district 2300104;
- latitude 2300105, longitude 2300106;
- location 2300110, located 1053, on route 1051;
- owner 2300201, year built 2300901, design number 805.

**Narratives.** `NARRATIVE_SECTIONS` lists 15 memo fields (5724 … 6001407).
They are shared by the NBI 90 and SNBI report types on the WVDOH Report
(rt 3); the legacy WVDOT Standard report (rt 1) has none. The narrative HTML
is returned raw and sanitised in the browser with DOMPurify:

- style, script and iframe tags are removed, as are style, class, id and
  inline event attributes;
- runs of four or more `&nbsp;` collapse to one space.

**Canonical ratings.** `CANONICAL_RATINGS` defines 19 logical ratings, each
with an SNBI field id and a legacy NBI field id. For example:

| Rating | SNBI field | NBI field |
|---|---|---|
| Deck | 2300701 | 2005800 |
| Superstructure | 2300702 | 2005900 |
| Substructure | 2300703 | 2006000 |
| Culvert | 2300704 | 2006200 |
| Channel | 2300709 | 2006100 |
| Scour | 2300711 | 2011300 |
| Approach alignment | 2300801 | 2007200 |

Some ratings exist in only one generation: bearings, joints and the condition
classification are SNBI only; structural evaluation, deck geometry,
underclearances and waterway adequacy are NBI only.

- The value is the SNBI item when it is populated, otherwise the NBI item.
- `ratings_generation` is `SNBI`, `NBI`, `MIXED` or `NONE`.
- The five history-card ratings (deck, super, sub, channel, scour) follow the
  same SNBI-first rule, in SQL.

**Rating colours.** Ratings are NBI 0–9 values, not the pavement 0–5
indices. They are coloured from `ui/src/bridges/ratingColors.ts`:

| Band | Ratings |
|---|---|
| Good | 7–9 |
| Fair | 5–6 |
| Poor | 0–4 |

N (not applicable) and the letter appraisal codes G / F / P / SD are aliased
onto these colours. The overview map colours the bridge from the lowest of
its latest deck, superstructure and substructure ratings.

**Workflow status buckets** come from the workflow stage id:

| Stage id | Bucket |
|---|---|
| −1 | In progress |
| −3 | Awaiting approval |
| −5 | Approved |
| −10 | Completed |
| −23 | Error |
| anything else | Other |

#### Report layout

1. **Sections** come from `report_section` for the inspection's report type,
   ordered by `ds_order`. When the report type has none, they come from
   `report_type_form_map` in form order (`section_source = form_map_fallback`).
2. **Elements.** Each section's `form_element` rows carry the value this
   inspection recorded on the bound field (`fe_id` → `report_value`) and the
   field name.
3. **Fill counts.** Each section reports how many fields are bound and how
   many are filled.
4. **Unplaced values.** Values on fields that no section places are returned
   in natural sort order as `unplaced_values`.
5. **Pairing in the browser.** Each Label (element type 2) is paired with the
   bound element beside or below it:
   - beside it: on the same row (within 28 px vertically) and within 260 px
     to its right;
   - below it: within 60 px down and 80 px across.

   Memos (types 7 and 15) render as narrative, signatures as type 16 and
   pictures as types 3 and 17.
6. **Photo references.** "Photo #N" references resolve first to an image
   whose file name starts with N, then to `af_order`. A reference followed by
   "in the YYYY report" for another year is marked stale and not linked.

#### PDF fallback

When `pdf_blob` is empty, the PDF is read from
`INSPECT_PDF_FALLBACK_DIR`. That setting defaults to the folder that holds
the extract. The file is `inspection_<ast_id>/<ast_id>_report.pdf` or
`<ast_id>_report.pdf`; for example, inspection 272398 (bridge 01A001).

The old hard-coded `/Users/…` path has been removed. `has_pdf` on the history
list includes these fallback files.

The current local extract has no `asset_file` rows, so photos, the cover and
file downloads are empty until the pipeline syncs them with `--file-blobs`.

#### 3D terrain & floods

The routes are mounted from `flood3d/routes.py` in `api/routes/flood3d_routes.py`:

| Endpoint | Returns |
|---|---|
| `GET /api/bridges/{bars}/flood3d` | The scene manifest: state, alignment, terrain tile template, scenarios with mesh descriptors, provenance and review |
| `GET /api/bridges/{bars}/flood3d/runs/{run_id}/assets/{tiles\|meshes\|vectors}/…` | The allow-listed assets of the bridge's selected run. Responses are sent with private immutable caching, and hybrid MBTiles terrain is rendered lazily. |
| `GET /api/bridges/{bars}/flood3d/sample?lon&lat&year&run_id` | Ground, water-surface elevation and depth in metres, read from the source rasters. It returns `409` when the run changed. Coverage is `wet`, `dry` or `unmodeled`; an unmodeled point is never reported as dry. |

**Which bridges have scenes.** Only in-service bridges owned by WVDOT
(field 2300201 = `S01`) get a scene. Archived bridges never inherit current
terrain.

**Which model is shown.** Run pointers are in `bms.flood3d_bridges`,
`bms.flood3d_runs`, `bms.flood3d_publications` and `bms.flood3d_jobs`
(migration 043).

- A published, reviewed hydraulic run takes precedence.
- Otherwise a preliminary calculation on the prepared terrain run is used.
- If Postgres is down, the prepared terrain still loads, but reviewed results
  are withheld.

**Where the files live.** Run files are under `FLOOD3D_DATA_DIR`. Without
that setting, `instance/flood3d` is used, or locally the sister repo's
`inspect_tech/webapp/backend/instance/flood3d` when the first doesn't exist.

**No write endpoints.** Preparing, calculating, importing and publishing are
offline CLI work (`python -m flood3d.cli …`, `flood3d.batch`,
`flood3d.repair`, `flood3d.audit`); see `flood3d/README.md`. The hydraulics
use `packages/rattlesnake-hydraulics`: a subcritical standard-step solver on
USGS SIR 2025-5110 regression discharges, with Manning's n = 0.045.

**How the browser draws the scene.**

- MapLibre shows the raster-dem terrain, hillshade, the alignment and the
  mapped waterways.
- A three.js custom layer (`SceneLayer`) draws the water and deck meshes at
  absolute elevations. It loads only the chunks visible at the current level
  of detail: LOD 1 at zoom ≥ 17, LOD 2 at zoom ≥ 15, otherwise LOD 4, with at
  most four requests in flight.
- Scene URLs are made absolute on `API_BASE_URL` and requested with the
  sign-in cookie.

## 3. The plan engine

`bms/` (engine, deterioration, lisa, treatments, inventory, committed). It is
based on Rob Ware's BMS notes (bms.pdf, the crosswalk, the Quick SR workbook
and `final_bridge_program.xlsx`).

### LISA

`bms/lisa.py` ports `sr_calc.py` (`compute_new`): S1 structural 55, S2
functional 30, S3 essentiality 15, clipped to 0–100. It matches `sr_calc.py`
on all 7,208 workbook bridges; against the Quick SR sheet 88.8% are within
0.5 points (the misses are whole-number offsets on bridges with an
overtopping value). `quirk_parity` (default on) reproduces the sheet's Excel
behaviour (a missing load rating costs 55 points, a blank B.C.11 costs 10, a
text scour code costs 1); off, those fall back to NBI 66 / 113 / 43B and the
fallback is flagged. **Bands**: ≥ 75 preserve, ≥ 45 rehab, below replace
(bms.pdf). The active parameters are the one `is_active` row of
`lisa_configs` (Config → LISA scoring).

### Deterioration

`bms/deterioration.py`. Each year a component at rating r stays with
probability p_r, or drops by one. Fitted by maximum likelihood over every
consecutive pair of inspections of WVDOT-owned bridges, using each pair's
real gap (0.5–6 years); pairs that went up are excluded as work. A family
(NBI 43A/43B) with ≥ 200 pairs gets its own fit, else its material group,
else statewide; ratings with < 30 observations borrow from the level above.
At 6 and below p is capped by the rating above (poor components get repaired
before they are seen to drop). Ratings 0–1 never change. Admins can refit or
override a model (Config → Deterioration); overrides survive refits.

### Treatments, costs, effects

13 seeded treatments (`bms/treatments.py` `SEED`, editable in Config →
Treatments & costs): codes from the crosswalk (SNBI, HUB/TAMP, both
activity-code lists, the dTIMS name); $/sf contract averages (bms.pdf) and
state-force figures (MMS actuals) — JT1 and SP7 are placeholders.
**Applicability** by B.SP.04/06/09 prefixes and a culvert flag;
**triggers** are a window on the rounded expected component rating, the
LISA bands allowed, and a minimum interval since the last matching work
(B.W.02/03 history, or earlier in the run); **effects** are `freeze` N
years, `improve` Δ up to a ceiling, or `reset` to a rating. `improve` may be
fractional: the rating is a probability distribution, so +1.5 moves half of
each rating's probability up one point and half up two (expected gain 1.5,
below the ceiling).

**Effects calibrated to observed outcomes (2026-09-27).** The effects were
set from what completed TheHub projects did to NBI ratings
([Treatment Effects](/docs/Bridges_Treatment_Effects)), applied through the
configuration workbook (`scripts/bms_calibrate_effects.py`, logged in
`bms.config_imports`):

| Treatment | Was | Now | Evidence (net change on the component) |
|---|---|---|---|
| SP1 Superstructure replacement | deck, super reset 8 | deck, super reset 8; sub +1 up to 7 | super 5.0 → 7.4, deck 5.6 → 7.9, sub +0.8 |
| DK1 Deck replacement | deck reset 8 | deck reset 7 | deck 4.7 → 6.1, 48% reach 7+ |
| SP2 Superstructure rehabilitation | super +2 up to 7 | super +1, deck +1.5, sub +1, up to 7 | super +0.9, deck +1.4, sub +1.1 |
| SB2 Substructure rehabilitation | sub +2 up to 7 | sub +1.5 up to 7 | sub 4.5 → 5.7 (+1.3) |
| SP6 Clean and paint | super +1 up to 7, hold 5 | super and sub +0.5 up to 7, hold 4 | super +0.4, sub +0.4, faded by ~year 5 |
| JT1 Joint replacement | sub, super hold 3 | super +0.5 up to 7, hold 3; sub hold 3 | super +0.5, deck +0.2 |
| DK4 Modified PCC overlay | deck +2 up to 8 | deck +0.5 up to 7 | deck +0.45 (11 bridges, not significant) |
| DK8 Membrane with HMA overlay | deck +1 up to 7, hold 3 | deck +0.5 up to 7, hold 3 | deck +0.4 (8 bridges, not significant) |

BR1 keeps reset 8 on every component (its measured +1.2 mixes true
replacements with mislinked old structures). DK2, DK5, SP7 and CU2 have no
measurable completed projects and keep their assumed effects. DK4 and DK8
rest on small samples; revisit them as more projects complete. Effects apply
in the treatment's year: the lag before an inspection shows the change (up
to 2 years for rehabilitations, 1 for painting) is the inspection cycle, not
the work. Runs keep the treatments they were made with.

### The planner

`bms/engine.py`, pure computation run on a background thread. Each bridge
carries a probability distribution per component (deck, super, sub,
culvert). Each program year:

1. **LISA** is recomputed from the projected ratings, setting the band.
2. **Committed projects** in a forced status (approved, committed, under
   construction, completed by default) are applied in their year. Their cost
   comes off capital if any treatment is capital, else preservation;
   completed and under-construction work costs $0 (already spent or
   encumbered). Past-due ones move to the start year; the bridge is locked
   out of optimisation until its last committed year. Overspend is logged,
   not blocked.
3. **Candidates**: every treatment that applies, is allowed in the band, is
   triggered and is past its interval. Benefit = Σ over the benefit horizon
   (20 years by default) of treated minus do-nothing Composite Condition
   Rating × cost area × traffic weight / 1000. CCR weights: deck .30 / super
   .35 / sub .35 (re-split when a component is N; a culvert alone). Traffic
   weight = 0.145·ln(ADT) − k, floored at 0.05.
4. **Selection**: incremental benefit/cost on each bridge's efficiency
   frontier, capital first, then preservation on bridges capital didn't
   touch. Unspent money doesn't carry over.
5. **Recording**: post-work expected ratings, CCR, P(Poor), P(Good), then one
   Markov step; frozen components hold. A do-nothing baseline runs alongside.

**Poor / Good** follow B.C.12: the lowest of deck/super/sub/culvert ≤ 4 is
Poor, ≥ 7 Good, as probabilities with components independent; "% poor" is
weighted by deck area. The `max_pct_poor` target is reported per year, not
enforced.

### Configurations

Named BMS configurations (migration 050), at parity with the PMS configs (migrations 030 / 037).

- **`bms.configs`:** name, comments, **model** (`amps` = this Markov planner; `dtims` = the Deighton
  dTIMS-faithful model, [below](#the-dtims-model)), `settings` (engine settings, JSON), `is_system_default` (exactly one),
  `copied_from`, `current_version`. Config 1, "AMPS Markov (current)", holds everything that existed before.
- **Per-config tables:** `treatments` (PK `(config_id, code)`), `deterioration_models` (unique
  `(config_id, family_code, component)`), `lisa_configs` (one active row per config) and `budget_scenarios`
  all carry `config_id` (ON DELETE CASCADE). **Every query of them filters `config_id`.** Budget scenarios name
  their budget categories (`categories`, default preservation / capital); a budget row is `{year, <category>: $}`.
  Committed projects are shared by every configuration (TheHub codes map to the configuration's treatments).
- **The one reader** is `bms/compiled.py`: `read_tables(config_id)` gives the config's content (name, model,
  settings and every policy table of its model, without ids and timestamps), `content_hash`, `validate`
  (the AMPS model: rules, $/sf, stay probabilities, exactly one LISA set with valid parameters and ordered
  bands), `ensure_version` / `load_version` (`bms.config_versions`, deduplicated by content hash), a small
  cache (15 s, and re-read when `updated_at` moves) and `use_compiled`. Tables are registered per model
  (`TABLES_BY_MODEL`, `VALIDATORS`), so the dTIMS model adds its own.
- **Lifecycle** is `bms/configs.py` (the twin of `api/configs.py`):
  - `user_config_id` / `resolve`: the requested config, else the user's (`app_users.bms_default_config_id`),
    else the system default. Without sign-in the default lives in memory.
  - `lock_for_edit`: a transaction advisory lock, and ConfigLocked (409, `code: config_locked`) while a run is
    pending or running on the config. Every config write (treatments, models, refit, LISA, workbook import)
    goes through it and `touch`. Budget scenario edits don't need it (runs copy their scenario).
  - `copy_config` copies every table of the model (`SUB_TABLES_BY_MODEL`); `delete_config` cascades;
    `delete_runs_for_config_delete` deletes the config's runs only when the caller confirms their number, and
    logs them in `bms.config_run_deletions`.
- **Runs pin versions:** creating a run reads the config's content, stores it as a version (if new) and records
  `runs.config_id` / `config_version`; the content the AMPS engine reads (treatments, models, LISA parameters) is
  also copied into `runs.config`, the shape every reader already used. Editing a config never changes a finished
  run. Runs from before configurations have `config_version` NULL: their `runs.config` is their full snapshot.
- **Endpoints:** `/api/bms/configs` (list with counts, get with runs, create = copy, patch, delete
  `?delete_runs=N`, `PUT /default`, `PUT /{id}/system-default`, `/{id}/check`, `/{id}/versions`;
  `bms/config_routes.py`). Every config-reading BMS endpoint takes `?config_id=` (default: the caller's BMS
  default): `/lisa*`, `/models*`, `/treatments`, `/scenarios`, `/config/workbook*`, the project and bridge
  outlooks, TheHub seed and the committed-projects import (for mapping codes), and run creation
  (`config_id` in the body; a saved scenario must belong to it). `/api/auth/me` and `/api/users/me` add
  `bms_config_id`, `bms_config_name`, `bms_config_model`.

### The configuration workbook

`bms/config_workbook.py` (`GET /api/bms/config/workbook.xlsx`, `POST …/validate`, admin
`POST …/apply?diff_hash=`, `GET …/imports`, all with `?config_id=`) is the bridge twin of the PMS config
workbook and shares its machinery (`api/config_workbook.py`: sheet / column specs,
cell coercion, the row-by-row diff, the report, `render_workbook`). The sheet set depends on the
configuration's model (`SHEETS_BY_MODEL`; the sheets below are the AMPS model's). `_meta` records the
configuration's id, name and model: a file from another configuration is flagged, one of another model refused.

- **Sheets:** LISA Parameters (the active `lisa_configs` row merged with
  `lisa.DEFAULT_PARAMS`, flattened to paths; maps of codes to points such as
  `s1.scour_vulnerability_penalty` stay one value), Deterioration Models,
  Treatments, Budget Scenarios, Scenario Budgets.
- **Checks** before anything is written:
  - LISA: each value must have its default's shape, and `0 ≤ rehab_min < preserve_min ≤ 100`.
  - Deterioration: p0…p9 are in 0–1. An edited model is saved with `is_override = TRUE`; it can't be
    switched back in the file, because that needs a refit.
  - Treatments: applicability, trigger and effects use only the keys the engine reads
    (`bms/treatments.applies` / `triggered`, `engine._apply_effect`), and ratings are 0–9. An active
    treatment must be priceable (`bms/cost.unit_cost`). Treatments can't be removed.
  - Budgets: every year falls inside its scenario's years; missing years are a warning (they become $0).
  - Scenarios can't be added or removed in the file.
  - The whole configuration must still pass `bms/compiled.validate` with the file's changes overlaid on the
    stored tables ("Config check: …" file errors).
- **Applying** re-validates and requires the reviewed report's `diff_hash`. In one transaction it takes an
  advisory lock (one import per configuration at a time), re-checks that the configuration hasn't changed since
  the check (409 otherwise), calls `lock_for_edit` unless only budget sheets change, writes, touches the
  configuration and logs the change set in `bms.config_imports` (with `config_id`, `changes`, `file_sha256`).
  It then clears the LISA score and compiled caches. Runs are unaffected: each recorded its config version.
- **The dTIMS model's sheets** (`bms/dtims/workbook.py`): Settings, Fields, Variables, Yearly Formulas,
  Expressions, Treatments (with trigger and budget-category expressions), Treatment Costs, Reset Operations,
  Treatment Links, one sheet per lookup table (Component Curves, Element Curves, Unit Costs, CCR Weights,
  Deterioration Modifiers; column names lower-case), Committed Map, Budget Scenarios and Scenario Budgets
  (one column per category). Every expression cell is parsed on validation and an error points at its cell;
  cross checks cover names (a cost, reset or link on a treatment that doesn't exist, a reset of an unknown
  variable, duplicate orders), then the whole configuration is compiled with the file overlaid. Applying
  rewrites the configuration's `dt_*` tables in the same transaction; scenario budgets are updated without
  touching their categories.

### The dTIMS model

A configuration with `model = 'dtims'` runs Deighton's dTIMS bridge model as WVDOT configured it, instead
of the Markov planner above. The model is `bms/dtims/`. Its rules are data in the configuration (tables
`dt_*`, migration 051), translated from the dTIMS test service; how dTIMS itself works, and the evidence for
each rule below, is in `dtims_docs/dTIMS_BMS_End_to_End_2026-09-27.md`.

**Two seeded configurations** (`python -m bms.dtims.seed_db`, idempotent by name; `--replace` rewrites their
rules from the seed files):

| Configuration | Seed | What it is |
|---|---|---|
| WVDOT dTIMS BMS | `bms/dtims/seed/fixed.json` | dTIMS's configuration with the defects found in the review corrected |
| dTIMS exact (2026-09) | `bms/dtims/seed/dtims_exact.json` | dTIMS's configuration as read, defects included, for comparing with dTIMS output |

They differ **only in data**: `fixed.json` is `dtims_exact.json` with `bms/dtims/seed/fixes.yaml` applied
(`scripts/dtims_seed/apply_fixes.py`), and nothing in `bms/dtims/` branches on a configuration's name. The
exact seed comes from `scripts/dtims_seed/translate.py` (dTIMS formulas → our expression language; the
original text and UUID are kept on each expression as `source_text` / `source_uuid`).

| Fix (`fixes.yaml` id) | dTIMS as configured | Fixed |
|---|---|---|
| `nhs-codes` | NHS tests compare with NBI `'1'` / `'0'`, but the inventory holds `Y-NHS` / `N-Non-NHS`: every bridge is treated as non-NHS (painting, replacement cost, budget category) | Tests use `LEFT(NHS, 1) = 'Y'` |
| `ccr-missing-components` | A missing component (`N`) counts as −1 in the CCR | Weights re-split over the components present |
| `structure-condition-gaps` | Structure condition is a minimum that can include −1, making a bridge Poor | Minimum of the components that exist |
| `overlay-renews-deck-elements` | A deck overlay sets every state of elements 1080 / 1130 to 0, so patching and sealing never trigger again | The overlay renews them (CS1 = 100) |
| `rehab-counts` | Superstructure rehab writes 0 to its count; deck rehab never increments; paint replacement assigns its count to itself | Each increments |
| `deck-rehab-hold` | Deck rehab writes a rating formula into the deck hold | A hold in years |
| `percentage-costs` | Deck patch and spot paint multiply a condition-state percentage by $/unit, with no quantity | `(CS3 + CS4) / 100 × quantity × unit cost` |
| `bkampp-committed` | Committed BKAMPP costs $0 and doesn't record itself as the last major | Its cost, and it is recorded |
| `committed-culverts` | Committed culvert work isn't forced (no committed branch in the culvert triggers) | Applied in its committed year |
| `full-length-holds` | A hold of h years freezes a rating counter for h − 1 years (holds decrement before counters read them) | Counters are evaluated before holds |

#### Execution contract

Verified by replaying all 12 saved dTIMS strategies (`tests/bms/test_dtims_golden.py`: 21,660 yearly values,
PV cost and benefit, every cost to the cent).

- **Years are slots.** Slot 0 is `start_year` (2027) and holds the initial state (initializers run with
  `YR = 0`); slot 1 repeats it; yearly formulas run from slot 2 (`first_annual_yr`). Slots run to
  `end_year` (2050, 24 slots). Treatments may be applied through slot `end_treatment_year − start_year`
  (2045 → 18). Calendar year = `start_year + slot`; budget year k of a dTIMS scenario is slot k.
- **A run's start year is its first year of work**, as for PMS and the AMPS model: a scenario starting in 2026
  runs with `start_year` 2025 (the starting state), work from 2026, and `end_year` / `end_treatment_year`
  moved by the same number of years so the horizon lengths stay dTIMS's (`bms/dtims/store.run_settings`).
  **The first year of work is an evaluation year** (setting `evaluation_first_year`, default TRUE): only
  committed work is placed in it; a bridge with no committed work that year gets no generated strategy with
  work in it, so with no committed projects the year just evaluates condition. It is also left out of the MILP's
  target rows (nothing the optimizer does can change it) but is still reported.
  The run stores them in `runs.config.dtims_settings`, and Validate, the Strategies tab and replays read the
  pinned version through `with_run_settings`. The seeded dTIMS scenarios start in 2028 (their first funded
  year), which is dTIMS's own 2027 start. Runs made before this have no `dtims_settings` and keep their years.
- **Variables are evaluated in their authored order** (`dt_variables.ord`). A name reads this year's value if
  that variable has already been evaluated this year, otherwise last year's; `PREV(v)` is always last year's.
  Order is therefore part of the model (it is what gives dTIMS's holds their h − 1 years).
- **Types:** `A` annual (a yearly formula, the first curve whose filter is true), `D` static (initializer
  only), `C` cumulative (evaluated once at the end: `PV`, `PVDIFF`).
- **Treatments in a year:** the major's `TRT_YEAR` is set, its cost is evaluated (before its resets), then its
  resets run in order; a container major (Structure Maintenance) then applies every ancillary in link order
  whose trigger holds on the state left by the work before it (`ancillary_trigger_basis = sequential`).
- **PV** = Σ over slots 1 … N − 1 of value / (1 + discount_rate)^slot. `PVDIFF(v, cutoff, weight, power)`
  compares a variable's history with the same bridge's Do Nothing history.

#### Expression language (`bms/dtims/expr`)

Triggers, costs, resets, initializers, yearly formulas, derived fields and budget categories are all
expressions. They are parsed once when a configuration compiles (`bms/dtims/config.compile_config`) and
evaluated by a tree-walking interpreter; text never reaches Python's own parser or `eval`.

- **Syntax:** numbers, `'text'`, `TRUE` / `FALSE`, `+ - * / **`, `= <> < <= > >=` (not chained),
  `AND OR NOT`, calls, `//` comments.
- **Names** resolve, in order, to a variable, an inventory field, a named expression (`dt_expressions`,
  inlined) or a global (`YR`, the settings). An unknown name, function or wrong argument count is a
  configuration error with its position.
- **Functions:** `IF` (lazy), `MIN`, `MAX`, `ABS`, `ROUND` (half away from zero), `INT`, `FLOOR`, `CEILING`,
  `MOD`, `LN` (dTIMS `LOG`), `EXP`, `SQRT`; text `LEFT`, `RIGHT`, `SUBSTR` (1-based), `LEN`, `TRIM`,
  `LTRIM`, `RTRIM`, `UPPER`, `LOWER`, `STR` / `VAL` (Visual FoxPro semantics, as dTIMS uses them),
  `ISEMPTY`; `LOOKUP(table, column, key[, default])` on the configuration's lookup tables; state
  `IS_COMMITTED()`, `IS_DN()`, `IS_MO()`, `TREATED_THIS_YEAR('t')`, `TRT_YEAR('t')`, `LAST_MAJOR()`,
  `COST_THIS_YEAR()`; history `PREV(v)`, `VAR_AT(v, yr)`, `PV(v)`, `PVDIFF(v, cutoff, w, power)`,
  `IS_DEFAULT(field)`.

#### What the WVDOT configuration does

- **Components** (deck, super, sub, culvert) move on a "time in rating" curve: each rating has a life in
  years (lookup `CR_Life` by family key); a counter counts years at the rating and the rating drops by one
  when it passes the life. Holds (from treatments) stop the counter. Deterioration modifiers adjust lives.
- **Elements** (1080, 1130, 300–306, 515) move condition-state percentages CS1–CS4 by the element curves.
- **Treatments:** 6 majors (Do Nothing, Structure Maintenance, deck/superstructure rehab and replacement,
  bridge replacement, culvert work) and 10 ancillaries under Structure Maintenance (overlay, patch, seal,
  joints, painting, …), each with an interval, a trigger, ordered costs and ordered resets.
- **Benefit** is the scenario's benefit variable, `str_nPV_BENEFIT`: PV of the deck-area-weighted CCR gain over
  Do Nothing. **Cost** for ranking is `str_nPV_COST`, PV cost per square foot. Dollars against the budget are
  nominal (inflated) per slot and budget category (`budget_category_expr`: NHS, NON_NHS, BKAMPP).
- **LISA** is computed for the report only (it doesn't choose work in this model).

#### Inputs (`bms/dtims/inventory.py`)

AssetWise fields are renamed to the dTIMS `Bridge` columns, so the saved dTIMS rows and the AssetWise extract
go through one path. Ratings are text (first character of SNBI B.C.01–04, keeping `N`, falling back to NBI
58–62); `NHS` from B.H.03; material B.SP.04; wearing surface B.SP.10; deck protection B.SP.11 (NBI 108C);
deck area B.G.16; ADT B.H.09 (NBI 29); owner B.CL.01; district B.L.04. Elements are summed from
`asset_element`; a defect's CS1 is the parent deck quantity minus the defect's. **Counter seeds** (years
already spent at the current rating) come from the NBI history (`qv_nbi_timeseries`, up to
`history_end_year`), capped by the derived field's expression (⌊`counter_seed_fraction` × life⌋, 0.7).
Derived fields (`dt_fields.derive_expr`) are evaluated after loading.

Known differences from dTIMS's inputs: AssetWise has element data dTIMS lacks (somewhat more preservation
work); dTIMS's population filter isn't known; ages and history counts default to 0 as in dTIMS.

**Committed projects** (`bms/dtims/run_db.committed_slots`): forced-status projects become up to 4 committed
slots per bridge (A–D). Their TheHub construction codes, else their AMPS treatment codes, map to a dTIMS
major and ancillaries through the configuration's **committed map** (`dt_committed_map`). Same-year projects
merge; past-due work goes to slot 1 unless completed or under construction; completed and under-construction
work costs $0, other work its stored cost. Codes with no mapping are summarised in one log line and the
project is planned without it.

#### Strategies and selection

- **Generation** (`bms/dtims/generate.py`): per bridge, a depth-first tree with shared prefixes. Do Nothing is
  the spine; at each slot the majors allowed are the initial ones, or the last major's subsequent links, gated
  by its interval and trigger; Structure Maintenance is skipped when no ancillary fires. Depth is
  `level_of_generation` (3) treatment years, at most `max_strategies_per_bridge` (2,000). A committed bridge's
  tree starts from its committed work (`IS_COMMITTED()`).
- **Pruning** (`bms/dtims/runner._prune`): Do Nothing, the committed base, the convex (cost, benefit)
  frontier from it and the best benefit/cost strategy per first treatment year, up to `keep_per_bridge` (40).
  These are stored in `bms.run_strategies`.
- **Selection** (`bms/dtims/select.py`; dTIMS's optimizer is proprietary, so the procedure is ours): every
  bridge starts at Do Nothing, or its committed base (forced; may overdraw). A max-heap on incremental
  benefit/cost along each bridge's frontier takes a step only if its dollars fit every (slot, category); when
  it doesn't, the bridge's best remaining option that fits is offered instead. `budget_years`
  (`selection.unconstrained` on a scenario): `zero_is_zero` (the default, as dTIMS with UnlimitedBudget 0)
  gives slots and categories without a budget $0, so the dTIMS 2026 scenarios fund 2028–2038 and plan no
  work after; `scenario_only` leaves slots after the last funded year and categories the scenario doesn't list
  unconstrained (a statewide run then puts about $2B of backlog in the first unfunded year). A scenario with only a
  `Total` category pools every category.
- **MILP: targets enforced** (`bms/dtims/milp.py`, run option `optimizer = milp`, or `optimizer` on the
  scenario): one binary per (bridge, kept strategy), exactly one per bridge; a budget row per
  (slot, category) the scenario limits (raised to what committed bridges' base strategies spend, so committed
  work may still overdraw); and per target year a row for deck area Poor ≤ `max_pct_poor` % and Good ≥
  `min_pct_good` % of the scope's deck area, using each strategy's class per year (the configuration's
  Good / Fair / Poor variable, recorded during generation as `Strategy.classes`). The objective is the most
  Σ PV benefit × deck area. Committed bridges choose only among strategies that carry their committed work.
  Solved with HiGHS through `engine/optimization/milp/solver.solve_milp`, warm-started from the benefit/cost
  selection, in phases like pavement MILP-assist: every target row hard; if infeasible, an indicator per row
  and the objective puts the number of rows met first, then benefit. `summary.milp` records the phase,
  status, gap, solve time and the rows missed. With MILP, generation also keeps the strategies on the
  (dollars, years Good) and (dollars, years not Poor) frontiers over the target years (up to half as many
  again as `keep_per_bridge`). Target years are `targets.years` or every funded year; `target_met` in the
  summary is judged only in those years (both targets that are set must hold).
- **Runs** use a process pool (`BMS_DTIMS_WORKERS`, default the CPU count up to 8), about 250 ms per bridge
  per worker (statewide, 7,106 bridges and 870,000 strategies: 5 minutes on 8 local workers). The selected strategies are replayed into `bms.run_bridge_years` with the AMPS model's columns
  (so the runs pages and Validate need no second shape): ratings from the output variables (−1 → blank), CCR,
  Poor / Good as 0 / 1, LISA, `treatment_code` = the year's dTIMS names without `str_` joined by `+`
  (the container dropped when it carries ancillaries), `bucket` = the budget category, nominal cost, and the
  year's marginal PV benefit and B/C. Each bridge's inputs are kept in `bms.run_bridge_inputs`, so any strategy
  can be replayed later with the pinned configuration version.

#### One simulator for runs, Validate and the outlooks (`bms/sim`)

`bms/sim/amps.py` (the Markov projection, moved unchanged; `tests/bms/test_bms_sim_parity.py` pins it to values
captured from the old code) and `bms/sim/dtims.py` (`BridgeSimulator.replay`) are what Validate
(`api/bms_validation`) and the bridge / project outlooks (`bms/detail_routes.py`) call, chosen by the run's or
configuration's model. For a dTIMS run, Validate loads the pinned config version, the frozen
`run_bridge_inputs` and the forced committed bridges, and replays each bridge's edited plan:

- program year k is slot k − 1; nothing can be scheduled in the start year (`first_work_year` 2);
- an ancillary on its own goes under Structure Maintenance; a year's price is the replayed cost of that year's work
  with the bridge's other planned work included, and its bucket the category its formula gives;
- buckets, lane budgets and totals are the scenario's categories (`plan.run.buckets`); lanes cover the treatment
  window (slots 1 … `end_treatment_year − start_year`);
- the treatment list is the treatment-set majors plus Structure Maintenance's ancillaries, with a `triggered` flag;
- commits write dTIMS names (`['DECK_OVERLAY', 'JOINT_REPLACE']`), which `run_db.committed_slots` places directly.

Replaying run 97 (District 1, 972 bridges) gives 0 differing bridges and every stored cost. Building a Validate
session replays every planned bridge (about 10 s for a district, then cached). The outlooks compare Do Nothing
with the chosen treatment in the first treatment year; a committed project's codes go through the committed map.

**Endpoints** (`bms/dtims/routes.py`, read-only; run reads hide bridges outside the user's districts):
`GET /api/bms/configs/{id}/dtims` (the whole configuration and its check), `…/dtims/expression/{name}` (one named
expression, what it references and what uses it), `GET /api/bms/runs/{id}/strategy-bridges?q=`,
`GET /api/bms/runs/{id}/strategies?bars=|as_id=` (kept strategies, frontier, IBC against the base, event years) and
`GET /api/bms/runs/{id}/strategies/{as_id}/{no}/detail` (one strategy replayed: variables before and after work,
and Do Nothing).

**Known limits.** Per-strategy numbers reproduce dTIMS; the selected program is "dTIMS model, AMPS
optimizer" (benefit/cost, or the MILP). The MILP picks among the strategies kept per bridge, so a target it
reports as unmet might be met by a strategy that was pruned. Generation matches dTIMS's strategy counts on 5 of the 6 sample bridges (20A629: 185 vs dTIMS's
206; dTIMS appears to allow Structure Maintenance inside a BKAMPP interval). Counter seeds capped at the same
fraction make many bridges at a rating drop in the same year, which shows as steps in Do Nothing % Poor.

## 4. Plan runs

#### Tables

- **`bms.runs`:** `config_id` and `config_version` (the configuration and the version of it the run used;
  NULL version for runs from before configurations). `config` holds everything frozen at creation:
  - `scenario` (id, name, start_year, years, inflation, categories, budgets[{year, <category>: $}], scope{nhs: all | nhs | non_nhs | nhs_non_interstate (NHS and B.H.01 functional class ≠ 1), districts, bars? (the bridge list, below)}, targets{max_pct_poor, min_pct_good (dTIMS model), years});
  - `config` {config_id, name, model, version};
  - `lisa_config`, `lisa_params`, `treatments`, `models`, `options` (benefit_horizon, weighting, forced_statuses);
  - **`committed_input`**: the committed projects as they were when the run was created (the run uses these,
    even if it waited for another run);
  - after completion, **`committed_snapshot`**.
  - `summary` holds `years[]` (budget / spent / committed_spend / projects by bucket, pct_poor, pct_good, base_pct_poor, base_pct_good, avg_lisa, target_met) and `totals`.
- **`bms.run_bridge_years`:** one row per bridge per year.
- **`bms.run_logs`**

**`committed_snapshot`** lists the committed projects that shaped the run: forced-status rows with a program year on bridges in scope. Each entry records id, bars, as_id, treatment_codes, program_year, status, cost, district, hub_project_number and `placed_year`, which is `null` when the project falls after the horizon and only locks the bridge. Validation replays from it.

#### Bridge lists (`scope.bars`, `bms/bridge_list.py`)

- A run or a saved budget scenario can be limited to a list of bridges by BARS. A bridge is planned when it is
  on the list **and** in the network class **and** in the districts; no list (or an empty one) means every bridge
  in scope, as before. Both models filter the same way: the AMPS planner in `engine.Planner._in_scope`, the dTIMS
  model in `dtims/run_db.execute_run` (on the derived `BARS`). Each run logs "Bridge list: N bridges listed, M of
  them in the network class and districts".
- `bridge_list.parse` reads a list or a text (BARS separated by commas, semicolons, spaces or new lines),
  upper-cases, drops duplicates and keeps the order; a token that isn't BARS-shaped is refused, as is a list of
  more than 10,000.
- Every listed BARS must be a WVDOT-owned, in-service bridge (the inventory runs plan, `inventory.load`).
  `POST /api/bms/runs` checks the list (`bridge_list.check` against `inventory.load` and `inventory.all_points`)
  and refuses a list with others, naming them and why (not in the inventory, not WVDOT-owned, not in service), so
  a run never quietly plans fewer bridges than it was given.
- The list is stored in `runs.config.scenario.scope.bars`. The runs list sends only its size
  (`scope.bars_count`); the run detail and `/configuration` send the whole list (for "New run from config").
- Saved scenarios keep it in `budget_scenarios.scope.bars` and round-trip it through the config workbook's
  `scope_bars` column (comma-separated).
- The Run Assistant saves list runs with `scope.bars` and studies them with `amps.bms.load_bridges(bars=...)`
  (same check).

#### Runner (`bms/runner.py`)

- A daemon thread per run, with one run at a time via the Postgres advisory lock `store.run_lock()` (key `0x424D5301`, separate from the PMS run lock). A second run waits.
- Progress and log lines go to the run row and `run_logs`.
- The forced-status default is `committed.DEFAULT_FORCED_STATUSES` = approved, committed, under_construction, completed. Before this port the fallback left out under_construction.
- **Cancelling.**
  - The planner is pure Python in the worker process. Unlike PMS, terminating the lock-holding Postgres backend would not stop it.
  - A cancel marks the row `cancelled`, or deletes it.
  - The planner checks between program years through `runner.is_cancelled`. That check is the in-process flag plus a database check at most every 2 s, so it works across uvicorn workers.
  - It then stops, releases the lock and never writes results over a cancelled run.

#### Engine (`bms/engine.py`)

- Candidates are priced only through `bms.cost.treatment_cost`. Results are unchanged by this refactor: a 4-year district-1 run gave identical totals, yearly % poor, spend and per-row treatment/cost digest before and after.
- Scope districts are compared as numbers. The inventory says `'01'` and the old scenario form sent `'1'`, so district scopes 1–9 used to match nothing.
- `Planner.committed_used` records each commitment and the year it was placed.

#### Condition measures

- % poor and % good are by deck area. Each bridge's P(Poor) under B.C.12 (lowest of deck / super / sub / culvert ≤ 4; Good when all ≥ 7) is weighted by its cost area.
- "Today" is the first year's do-nothing value, which is the starting state.
- The map class is Poor when P(poor) ≥ 0.5, else Good when the composite rating (CCR) ≥ 7, else Fair.

#### Endpoints (`bms/run_routes.py`, mounted by `api/routes/bms_runs.py`)

- `GET /api/bms/runs?sort=&dir=&page=&page_size=&q=&status=`
  - Sort keys: id, name, status, progress, created_at, start_year, years, scope, total_budget, final_pct_poor, total_cost, duration. NULLs sort last.
  - Returns `{total, page, page_size, items}`. Each item carries the scenario fields, the budget range and total, options, timestamps, `duration_s` and an `outcome`: initial and final % poor and % good, final do-nothing % poor, `pct_poor_by_year`, total cost and budget, projects, committed projects, bridges, and target-met years.
- `POST /api/bms/runs` (admin)
  - Takes `{name?, scenario_id?, scenario?, options{benefit_horizon, weighting, forced_statuses}}`. Options may also be sent at the top level.
  - An inline `scenario` wins; `scenario_id` is then kept as provenance.
  - Validation: years 1–30, budgets ≥ 0, nhs ∈ all/nhs/non_nhs/nhs_non_interstate, a bridge list of plannable bridges (above), forced statuses from proposed / approved / committed / under_construction / completed, horizon clamped to 5–40.
- `GET /api/bms/runs/{id}`: header, scenario, options, treatments, summary, snapshot size.
- `POST /api/bms/bridge-list/check` `{bars: [..] | "text"}` → `{count, bars (plannable), unknown, not_planned[{bars,
  reason}]}`: the new-run dialog's live check. `GET /api/bridges/bars?<list filters>` → `{bars, count}`: every
  BARS the Bridges list's filters match (its **Plan in BMS** adds `flag=wvdot&flag=in_service`).
- `GET /api/bms/runs/{id}/progress`
- `GET /api/bms/runs/{id}/configuration`: what "New Run from Config" needs.
- `POST /api/bms/runs/{id}/cancel` (admin)
- `DELETE /api/bms/runs/{id}` (admin): cancels a running run, then deletes. Edits, results and logs cascade. Both cancel and delete drop the cached Validate context.
- `GET /api/bms/runs/{id}/trajectory`: per year, condition vs do-nothing, avg LISA, budget/spent/committed by bucket, projects, deck area treated, target_met.
- `GET /api/bms/runs/{id}/treatments`: treatment × year count / area / cost matrices with totals, plus `by_district`, filtered to the caller's districts.
- `GET /api/bms/runs/{id}/projects?year=&district=&county=`: work rows with bridge name, family, facility and county (county name from the inventory's county code via `api/districts.COUNTIES`), district-filtered.
- `GET /api/bms/runs/{id}/committed`: the snapshot, or for older runs the committed work rows joined to today's table (`from_snapshot: false`). Adds the charged cost (0 for completed / under construction / lock-only) and the run's treatment and bucket.
- `GET /api/bms/runs/{id}/map?year=`: GeoJSON points with band, work and cost; district-filtered.
- `GET /api/bms/runs/{id}/bridges/{bars}`: the drill-in. Returns 403 outside the caller's districts.
- `GET /api/bms/runs/{id}/logs?offset=&limit=`: levels upper-cased.
- `GET /api/bms/runs/{id}/export.xlsx`: completed runs only. Built with `bridges/xlsx_style.write_workbook`. Sheets: Summary, Program, By year, Treatments, Committed. Rows are limited to the caller's districts.
- **Removed:** `POST /api/bms/runs/{id}/promote`. Committing run work to `bms.committed_projects` (with `source_run_id` / `source_key`) is done on the Validate page.

#### Frontend files

- `ui/src/api/bmsRuns.ts`
- `ui/src/hooks/useBmsRuns.ts`: the list polls every 5 s; progress polls only while pending or running.
- `ui/src/pages/bms/BmsRunsPage.tsx`, `ui/src/pages/bms/BmsRunDetailPage.tsx`
- `ui/src/components/bms/runs/*`:
  - `CreateBmsRunDialog`;
  - `BmsBudgetScheduleEditor`;
  - `BmsScenarioDialogs` (load/save, using `useBmsScenarios` / `useCreateBmsScenario`);
  - `BmsRunVisuals`, `BmsRunMap` (BridgePointsMap), `BmsRunBridgeDrawer`, `BmsRunBits`, `bmsRunViz`.
- Treatment colours follow the treatment code; condition colours come from `bridges/ratingColors.ts`.

## 5. Run validation

**Data**

- **The plan** is the run's `bms.run_bridge_years` rows that have a `treatment_code`: the optimizer's picks and the committed projects the run forced in. There is one item per bridge per program year.
- **Item keys**:
  - `"<as_id>"` when the bridge has a single project in the run's plan.
  - `"<as_id>:<calendar year>"` when the engine planned it more than once. In a statewide run about four in five treated bridges have repeat work, such as deck sealing every 5 years.
  - `"add-<uuid>"` for bridges added by hand.

  Keys survive moves.
- **The edit log** is `bms.run_plan_edits` (migration 046), the same shape and rules as pavement `run_plan_edits`.
  - Every edit stores full before / after snapshots.
  - Rows are never deleted or rewritten. Status moves proposed → applied / denied / withdrawn, and applied → reverted through a new `revert` edit. Only deleting the run removes them (cascade).
  - `bms.run_plan_state.head_seq` gives optimistic concurrency. Writers lock it; an edit whose `base_seq` is older than a later applied edit to the same item gets a 409.
  - Multi-item commits share a `batch_id`.
  - The current plan = the base plan + applied edits replayed by `seq`.
- **Frozen inputs** come from `bms.runs.config`: the scenario (start year, years, inflation, per-year preservation / capital budgets), the treatment catalogue (unit costs, categories, effects) and the deterioration models.
  - Names and applicability come from the bridge inventory (DuckDB). Bridges that left the planning scope fall back to the all-bridges list.
  - Committed-project names come from `config.committed_snapshot` when present, else from `bms.committed_projects`.
- **Districts**: the bridge district text (`'01'`, `'10'`) is converted to an int for `app_user_districts`. `user.can_see(district)` filters every read and guards every write, server-side.

**Costs**

- Costs come only from `bms/cost.treatment_cost`: the treatment's $/sf × the bridge's cost area (the run row's `deck_area_sf`) × (1 + run inflation)^(year − start year). Bundles such as `SP2+DK1` are the sum of their parts.
- A committed project forced into the run keeps its programmed cost while its treatment is unchanged, as the engine charged it.
- Budget bucket follows the engine rule: capital if any code is capital or none is in the catalogue, else preservation.

**Condition in the footers**

- The network shares are the run's stored results plus the change the edits make. They are by deck area, using P(Poor) / P(Good) under B.C.12 (lowest component ≤ 4 Poor, ≥ 7 Good).
- Each bridge whose plan differs from the run's is re-projected twice with the run's Markov models and treatment effects (`api/bms_validation/plan.simulate_bridge`, the same steps as `bms/engine.py`): once under its new plan and once under the run's plan. The deck-area-weighted difference is added to the stored totals.
- With no edits the footers equal the run's own numbers exactly.
- Start ratings come from the run's first-year rows when the bridge had no first-year work, else from today's inventory.
- `sanity` reports how many bridges no longer replay exactly (the inventory changed since the run) and the largest network difference. Only edited bridges are affected; the page shows an info note.
- **Card colour**: the do-nothing expected lowest rating per program year (`lowest_path`) and its class (`band_path`, rounded: < 4.5 Poor, < 6.5 Fair).
- **LISA** on a card is the run's stored LISA for that bridge in that year.

**Commit / uncommit**

Both go through one side-effects function:

- **Commit** upserts `bms.committed_projects` with:
  - status `committed`, source `run:<id>`, `source_run_id` and `source_key` (unique together);
  - `program_year` (calendar), the catalogue `treatment_codes`, cost, the bridge's district text, `as_id`, `bars` and name.
- **Uncommit** (or reverting a commit) sets that row to `cancelled`. It is never deleted, and committing the same item again re-activates the same row.

**Endpoints** (`api/routes/bms_validation.py`, prefix `/api/bms/runs/{run_id}/validation`)

| Method | Path | What it does |
|---|---|---|
| GET | (the prefix itself) | The plan: items, proposals, treatments, totals, sanity, scope and viewers |
| GET | `/totals` | Totals only |
| GET | `/edits` | The diff log, filterable by `status` and `key` |
| GET | `/geojson` | Plan items and pending adds as bridge points |
| GET | `/candidates?q=` | Bridges in the run's analysis set that can be added |
| GET | `/projects/{key}` | Item, bridge, outlook, eligible treatments, cost by year, history, the run's trajectory for the bridge |
| POST | `/edits` | `move` \| `delete` \| `retreat` \| `add` (`as_id`) \| `commit` (scope `item`/`year`/`all`) \| `uncommit`. District users must comment and create proposals |
| POST | `/edits/{id}/approve`, `/deny`, `/revert` | Admin only |
| POST | `/edits/{id}/withdraw` | The author, or an admin |
| POST | `/reset` | Admin only |
| GET | `/stream` | Server-Sent Events: `hello`, `edit`, `proposal`, `decision`, `totals`, `batch`, `presence`, plus a keep-alive every 15 s |

**Live updates**

- `api/validation/events.py` now has one `Hub` per NOTIFY channel. Each hub has its own subscribers, presence and LISTEN thread per worker.
- Pavement keeps `pms_run_validation` with unchanged behaviour. BMS uses `bms_run_validation`, because run ids overlap between the two apps.
- Payloads stay under 8 KB. Larger ones are sent as `refetch`, and batches carry only ids.

**Shared frontend**

- `components/validation/ValidationWorkspace.tsx` is the one Validate page. Pavement passes `pavementDomain` and bridges pass `bridgeDomain`; each adapter supplies the item fields, measure (miles vs deck area), condition colours, treatment names / icons / colours, table columns, dialog tabs, add-dialog candidates, map and API.
- The pop-out maps use separate BroadcastChannels: `pms-validate-map-<id>` and `bms-validate-map-<id>`.

## 6. Projects, TheHub and the outlooks

#### Data and code

**Tables** (Postgres, schema `bms`, migration 043): `lisa_configs` (one active), `deterioration_models`, `treatments`, `budget_scenarios` (soft-archived with `archived_at`), and `committed_projects`.
- `committed_projects` has these columns: `hub_id`, `hub_project_number`, `hub_stage`, `cost_share`, `source`, `source_ref`, `source_run_id` and `source_key`.
- It is unique on `(hub_id, bars)` for TheHub rows.

**Inventory:** WVDOT-owned in-service bridges (field 2300201 = `S01`) from the read-only DuckDB (`bms/inventory.py`).
- LISA inputs, ratings, family and deck area come from it.
- Inspection history is `qv_nbi_timeseries`: the last inspection per year.

**Code**
- `bms/routes.py`: LISA, models, treatments, scenarios, committed.
- `bms/hub_routes.py` and `bms/hub.py`: TheHub bridge projects and seed.
- `bms/detail_routes.py`: project and bridge detail / outlook.
- All three are mounted by `api/routes/bms_planning.py` through `bms/wiring.py`.

#### Access

- Every `/api/bms/*` route needs a signed-in session (the `require_sign_in` middleware).
- Reads are open to every signed-in user. District users see all projects read-only, as with PMS projects.
- **Every write takes `require_admin`, so a district user gets a 403:**
  - `PUT /lisa/config`;
  - `POST /models/refit`, `PUT /models/{id}`;
  - `PUT /treatments/{code}`, `POST /treatments`;
  - `POST /scenarios`, `PUT` and `DELETE /scenarios/{id}`;
  - `POST /committed`, `PUT` and `DELETE /committed/{id}`, `POST /committed/import`;
  - `POST /hub/refresh`, `POST /hub/seed`.

#### Endpoints (`/api/bms`)

**LISA**
- `GET /lisa`: every bridge's score and band, the band counts, a 10-bin histogram, and the scored / unscored counts.
- `GET /lisa/{bars}`: the breakdown, inputs, ratings and config name.
- `GET` and `PUT /lisa/config`: `params` are stored as given and deep-merged over `lisa.DEFAULT_PARAMS`; the response returns `effective` and `defaults`.

**Deterioration models**
- `GET /models` also returns years in each state, the forecast from rating 9 over 40 years, years 7→5, and the inventory count per family.
- `POST /models/refit` deletes the non-override models and refits them from inspection pairs.
- `PUT /models/{id}` takes either `{stay_probs: 10 values in 0..1}` (sets an override) or `{reset: true}` (clears it and refits).

**Treatments**
- `GET /treatments` adds `unit_cost` (from `bms/cost.unit_cost`) and `applicable_bridges`.
- `PUT /treatments/{code}` and `POST /treatments`: the category must be `preservation` or `capital`.

**Budget scenarios**
- `GET`, `POST`, `PUT /scenarios[/{id}]`: years must be 1–30. Budgets are re-keyed to `start_year..start_year+years-1`, and a missing year counts as 0.
- `DELETE` archives the scenario.

**Committed projects**
- `GET /committed`: the rows plus `in_inventory`, bridge name and NHS; the unmatched count; the statuses; and `forced_by_default`.
- `POST /committed` requires `bars` and `program_year`. The status defaults to `proposed` and the source to `manual`. `as_id` and `district` are filled from the inventory.
- `POST /committed/import?replace=true`: the body is the raw `.xlsx`. It replaces the rows whose source is `final_bridge_program.xlsx`.

**TheHub**
- `GET /hub/status`: the connection probe, cached 60 s.
- `POST /hub/refresh`: clears the caches.
- `GET /hub/projects`: the items, summary and filter options, with `stage`, `district`, `county`, `year` and `q`.
- `GET /hub/projects/geojson`: the bridge points.
- `GET /hub/projects/{number}` and `/hub/projects/by-hub-id/{id}`: the detail, with timeline, phases (with OASIS budget / spent) and scope. A project outside the bridge program (e.g. roadway work a bridge page lists) is read by number / id.
- `GET /hub/bridges/{bars}/projects`: **every** project TheHub links to one bridge (the bridge page's TheHub projects tab), whatever its construction code or status, newest first; inactive ones last. Each has `link: primary | segment | funding` (how it names this bridge), `treatments` / `is_treatment` / `category`, and the summary counts `treatments`, `inspections` and `inactive`.
  - It is queried live on every call (`PROJECTS_FOR_BRIDGE_SQL` / `BRIDGES_…` / `CODES_…`, `ONE_BRIDGE_CTE`: one parameter, the BARS, over every link in `LINKS_CTE`).
  - 422 for a malformed BARS; 503 when TheHub is down.
- Each bridge project also carries `contract`: its AASHTOWare contract (see *AASHTOWare construction contracts* below), or null.
- `GET /hub/projects/{project_number}/contract`: one project's AASHTOWare contract (`{project_number, contract}`, null when AWP has none). It is live, with no cache; 422 for a malformed number, 503 when TheHub is down.
- Statewide project data (`/hub/projects`, the map, the project pages) is cached for 300 s. The per-bridge and contract endpoints are not.
- The bridge program (`/hub/projects`, the map, the seed) is the projects that have a bridge construction code (30–47, 70–74, 100–103) and are not in an excluded status. The bridge page's list and the per-bridge spend take every linked project.
- Its bridges come from every link in `LINKS_CTE` (above); the BARS number is the last six characters of the NBI number.
- **Stage:**
  - Completed: status 10 or 11, or an actual "Complete" milestone.
  - Active: status 07/AF/AI/HF/HI with the construction phase open.
  - Inactive: an excluded status (terminated, withdrawn, non-construction, reserve); only on the bridge page's full list.
  - Otherwise: programmed.
- The roads2 map context layer is PMS's `/api/hub/tiles/roads2`. The duplicate `/api/bms/hub/tiles/roads2` was removed.

**Seeding from TheHub (`POST /hub/seed`)**
- Writes one row per project × WVDOT-owned in-service bridge. It is an upsert on `(hub_id, bars)` where the source is `thehub`.
- **Status:** completed → `completed`; active → `committed` (`under_construction` once it has been let); programmed → `approved`.
- **Cost:** the programmed cost (or the estimate) × the bridge's deck-area share (`cost_share`, `bms/hub.deck_area_shares` over every bridge the project names — so a project that also names a bridge WVDOT doesn't own charges WVDOT's bridges only their share). Re-seed to apply a changed share to existing rows.
- **Treatments:** mapped from the TheHub codes through `treatments.hub_codes`.
- **Duplicates:** a `final_bridge_program.xlsx` row on the same bridge, with a shared construction code and a year within 2, is set to `cancelled` with a note (reversible).

#### AASHTOWare construction contracts (`bms/awp.py`)

Ported from the consultant invoice portal's AWP tab (`backend/app/services/awp.py`), without its cache.

**Which projects have one**
- A TheHub project is an AWP construction contract when one of the warehouse's AWP tables carries its `Project.ProjectId`:
  - the contract feed `dbo.AWP_HUBDates.ContractNumber`;
  - the date feed `dbo.AWP_Dates.ProjectID`;
  - the imported change orders `dbo.AWP_ChangeOrders.ContractID`.
- 541 of the 2,280 TheHub bridge projects have one. District force-account and emergency work usually has none.

**What `contracts(numbers)` reads.** One pass of five parameterised queries:
- the two date feeds;
- the change orders;
- the project's CN phase (`ProjectPhase.PhaseCode LIKE 'CN%'`: dates, participating / non-participating amount, contractor);
- the average `EandCPercent` of the contracts let in the same years.

**The view it builds**

*Dates.* The nine milestones:

| Milestone | Contract-feed column | Date-feed column |
|---|---|---|
| Advertised | `PublicationDate` | `Publication_dt` |
| Let | `LET_DT` | — |
| Awarded | `AWARD_DT` | — |
| Executed | `EXEC_DT` | `EXEC_Dt` |
| Fully executed agreement | `FEA_DT` | `FEA_Dt` |
| Notice to proceed | `NTP_DT` | — |
| Work began | `WKBG_DT` | — |
| Substantially complete | `SWKC_DT` | — |
| Final estimate approved | `FEPA_DT` | — |

- The contract feed wins.
- `source` is `rich`, `simple` or `both`.
- `conflict` marks feeds that disagree, and keeps the date feed's value.

*Stage.* The latest milestone that is on or before today.

*Durations.* In days: advertised → let → award → execution → NTP → work begin, construction (work begin → substantially complete), closeout (→ final estimate) and total.

*Change orders.*
- Sorted by number, each with its net (participating + non-participating) and running net.
- The summary gives the count, the net, the days added and the latest adjusted completion.
- An order counts once it is imported into TheHub, before approval.

*E&C.* The contract's percent and its letting year's average.

*CN phase.* TheHub's construction phase, with two checks:
- the construction start equals AWP's work-begin date;
- the phase end equals the latest change-order completion.

#### Detail and outlook

**Endpoints**
- `GET /projects/{id}/detail[?scenario_id=]`
- `GET /projects/{id}/outlook[?treatment=]`
- `GET /bridges/{bars}/detail[?treatment=&project_id=&scenario_id=]`

**Grouping:** a project is its `committed_projects` row plus every row with the same `hub_id`.

**Projection**
- Each component starts as a point distribution at today's rating. It is projected 20 years on its family's Markov model (`det.ModelSet.resolve`, the same models the runs use).
- A treatment applied now uses its `effects`: reset / improve / freeze.
- The "lowest" rating is the minimum expected component rating (B.C.12).
- `p_poor` and `p_good` come from `engine.Planner._classify`, which is probabilistic.
- **Poor threshold (`POOR_BELOW` = 4.5):** an expected rating counts as Poor below 4.5, i.e. once it rounds to 4. This is not configurable; it follows the NBI Poor ≤ 4 rule, the same as `inventory.condition_band`.
- **Project averages and band shares** are weighted by cost area: deck area, or length × width for culverts and zero-area records.

**Costs**
- All pricing goes through `bms/cost.py` (`cost_area`, `unit_cost`, `treatment_cost`): $/sf (its basis, falling back to the other) × cost area × (1 + inflation)^(year − this year).
- **Inflation:** the chosen budget scenario's (`scenario_id`), otherwise `DEFAULT_INFLATION` = 3%. That is the program workbook rate, and the default for a new scenario. An unknown scenario returns 404. The response echoes `inflation` and `scenario_id`.
- **Project model cost:** each row is priced at `max(program_year, this year)`, so past work is priced today, not deflated. Structure replacement (BR1) stands alone; any other combination of treatments adds up.
- **Bridge cost:** today's cost, plus the cost if done in each of the next six years.

**Treatment options and defaults**
- Only active treatments that pass `treatments.applies` for the bridge (or for any of the project's bridges) are offered.
- **Default treatment on the bridge page:** `?treatment=`, else the context project's first code, else the first code on any non-cancelled project for the bridge.

## 7. Bridge Wizard

Full reference: [Bridge Wizard — Logic Reference](/docs/Bridge_Wizard_Logic). Summary:

- **Data:** the AssetWise DuckDB extract (`INSPECT_DB`), read-only. Model-written
  SQL runs only through `bridges.db.connect_locked` (SELECT/WITH/PRAGMA
  table_info/EXPLAIN, one statement; local filesystem disabled). 500 rows back to
  the model per query, 100,000 per export sheet, truncation always reported.
- **Model:** `claude-sonnet-5`, adaptive thinking (summarized), `effort: medium`
  (no `budget_tokens`), 16,384 output tokens per turn, up to 50 tool calls per
  question. System prompt (persona + domain primer + schema dump with row
  counts) cached with `cache_control` and memoized per database path — must stay
  byte-identical. Thinking blocks are replayed with their signatures.
- **Scope rule** in the prompt: WVDOT-owned (`qv_bridge_decoded.is_wvdot_owned`)
  by default, scope stated in every aggregate answer and on export Summary
  sheets.
- **Python** (`run_python`) only in the sandbox: `BRIGZARD_SANDBOX=socket:/run/bms-sandbox/sandbox.sock`
  on mmsdev (the existing `bms-sandbox` sidecar, `/bms_sandbox` mounted into
  `pms`), `local` for macOS development (`BRIGZARD_SANDBOX_PYTHON`), off by default.
- **Endpoints** (`/api/bridge-wizard`): `GET /status`, `POST /ask` (SSE: meta,
  status, thinking, thinking_end, tool_call_begin, tool_call, tool_result, text,
  image, file, done, error — always ends with done), `GET /conversations`
  (`?all=true` admins), `GET/PATCH/DELETE /conversations/{id}`,
  `GET /conversations/{id}/shared` (tools and owner stripped server-side),
  `GET /files/{file_id}`, `POST /feedback`, `GET /log/{short_id}`.
- **Tables** (migration 045, `bms` schema): `wizard_conversations` (owner
  `user_id`, message history JSONB, `turn_meta` with each answer's short id,
  charts and files), `wizard_responses` (answer log, timings, token counts incl.
  `cache_read_tokens`, feedback, owner), `wizard_artifacts` (file bytes in
  `data`).
- **Ownership:** conversations belong to `app_users.user_id`; list/open/continue
  your own + ownerless (imported) ones, rename/delete your own; admins all.
  Asking with someone else's conversation id starts a new chat. Share links and
  files: any signed-in user (ids are `secrets.token_urlsafe`).
- **Env:** `ANTHROPIC_API_KEY` (required to answer), `INSPECT_DB`,
  `BRIGZARD_SANDBOX`, `BRIGZARD_SANDBOX_PYTHON`. `BRIGZARD_LOG_DB` and
  `BRIGZARD_GENERATED_DIR` from the standalone app are gone (everything is in
  Postgres).

## 8. Known gaps

- Element-level (CS1–CS5) data isn't used by the planner (about 2,200
  bridges have it, only as a current snapshot).
- The % poor target is reported but not enforced; there is no multi-year
  lookahead or MILP assist as in PMS.
- No BA/BO flood-risk ranking, and no coordination between bridge and
  pavement work on the same route (both read TheHub separately).
- The local inventory extract carries no photos, PDFs or asset segments;
  those pages show empty states until the AssetWise sync includes the blobs.
- The standalone inspect_tech `/bms` app (and the older `/pms` app) on mmsdev
  were decommissioned on 2026-09-27; AMPS at `/amps` replaces both. Their
  `bms` database was left in place, but nothing made there after the v1.8.0
  import was copied.
