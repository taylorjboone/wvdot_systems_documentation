# PMS — Data Pipeline

How raw pavement surveys and the WVDOT LRS become the tables PMS runs on, how to refresh them, and how to recover. This is the single source for the data refresh. It replaces the refresh steps in [WVDOT PMS Data Pipeline](/docs/WVDOT_PMS_Data_Pipeline), [Import Analysis Segments](/docs/Import_Analysis_Segments) and [Segment Breakdown](/docs/Segment_Breakdown_Intersections).

Related: [LRS API (geometryToMeasure)](/docs/PMS_LRS_API) · [Business Logic](/docs/PMS_Business_Logic) · [Changelog](/changelog)

## Contents

1. [Overview](#1-overview)
2. [Quick start](#2-quick-start)
3. [Back up first](#3-back-up-first)
4. [The stages](#4-the-stages)
5. [How LRS conflation works](#5-how-lrs-conflation-works)
6. [Joints](#6-joints)
7. [Checks before data is replaced](#7-checks-before-data-is-replaced)
8. [Bookkeeping tables](#8-bookkeeping-tables)
9. [Schema migrations](#9-schema-migrations)
10. [Adding a survey year](#10-adding-a-survey-year)
11. [Where every input comes from](#11-where-every-input-comes-from)
12. [Refreshing mmsdev](#12-refreshing-mmsdev)
13. [Troubleshooting](#13-troubleshooting)
14. [What changed from the old import](#14-what-changed-from-the-old-import)
15. [Refresh history](#15-refresh-history)
16. [Bridges: the AssetWise pipeline](#16-bridges-the-assetwise-pipeline)

---

## 1. Overview

```text
                           ╔══════════════════════════════════════════════════════╗
                           ║    PMS DATA PIPELINE   ·   python -m pipeline all    ║
                           ║   one command · stages in order · logged · checked   ║
                           ╚═══════════════════════════╤══════════════════════════╝
                                                       ▼
                           ┌──────────────────────────────────────────────────────┐
                           │ 0  BACKUP                scripts/backup_pms.py       │──► ~/pms_backups/<stamp>/
                           │   pg_dump pms (+ mmsdev pms_test) · sha256           │
                           │   restore rehearsal: row count of every table        │
                           │   archive_<date> schema · input files · manifest     │
                           └───────────────────────────┬──────────────────────────┘
                                                       ▼
                           ┌──────────────────────────────────────────────────────┐
WVDOT R&H service       ──►│ A  LRS SNAPSHOT          stage lrs                   │──► refresh/<run>/
                           │   lrsops rhoverlay  layers 2 12 15 18 22 35 49 77    │    lrs_table.csv  2.csv …
                           │   lrsops rhoverlay  layer 70 (surface events)        │    70.csv
                           │   intersections.sqlite · roads2 fingerprint          │    intersections.sqlite
                           └───────────────────────────┬──────────────────────────┘
                                                       ▼
                           ┌──────────────────────────────────────────────────────┐
vendor <YYYY>.csv       ──►│ B  SURVEY INGEST         stage survey                │──► condition_history
                           │   one survey year at a time (others kept)            │
                           │   −1 → NULL · year from the file name                │
                           └───────────────────────────┬──────────────────────────┘
                                                       ▼
                           ┌──────────────────────────────────────────────────────┐
roads2 LRS geometry     ──►│ C  CONFLATE              stage conflate              │──► reconflate_normalized
lrs.geometry_to_measure    │   GPS start/end → route + milepoint on roads2        │    conflation_issues
(no HTTP, no dashcam)      │     own route › same route ± dir › nearest           │
                           │   clean: swap · drop unlocated · > 1 mi spans        │
                           │   re-weight onto each vendor window                  │
                           │   check: ≥ 97 % on own route, every year             │
                           └───────────────────────────┬──────────────────────────┘
                                                       ▼
                           ┌──────────────────────────────────────────────────────┐
70.csv · 2.csv          ──►│ D  JOINTS                stage joints                │──► pavement_joints
intersections.sqlite       │   layer 70 → merge touching → split > 3 mi           │    joint_builds
                           │     at highest-AADT intersections (≥ 1 mi)           │    joint_crosswalk
                           │   ids 70_<route>_<n> · new build only if changed     │
                           │   crosswalk: old joints → new joints                 │
                           └───────────────────────────┬──────────────────────────┘
                                                       ▼
                           ┌──────────────────────────────────────────────────────┐
lrs_table.csv           ──►│ E  SEGMENTS              stage segments              │──► analysis_segments
                           │   0.1-mi grid: newest survey per cell                │      (the engine's input)
                           │   lrsops overlay: split at joints + LRS events       │
                           │   length = end − begin · survey_year · build         │
                           │   check: length · joints · districts · roads2        │
                           │          · network % Good                            │
                           └───────────────────────────┬──────────────────────────┘
                                                       ▼
                           ┌──────────────────────────────────────────────────────┐
projects                ──►│ F  COMMITMENTS           stage commitments           │──► analysis_segments
                           │   planned / designed / awarded / in progress         │      .is_committed
                           │   projects flag the segments they overlap            │
                           └───────────────────────────┬──────────────────────────┘
                                                       ▼
                           ┌──────────────────────────────────────────────────────┐
                           │ G  DERIVED               stage derived               │──► multi_year_* views
                           │   refresh multi-year views (concurrently)            │    potential_projects
                           │   rebuild potential projects in place                │
                           │   check: every survey year covered by the views      │
                           └──────────────────────────────────────────────────────┘

   every stage ──► data_refresh_log   inputs + sha256 · roads2 fingerprint · counts · checks · status

   how a stage replaces live data

       build   ┌─────────────────┐  checks  ┌─────────────┐  pass  ┌────────────────────────────────┐
     ─────────►│ <table>_stage   │─────────►│ pass / fail │───────►│ BEGIN;                         │
               └─────────────────┘          └──────┬──────┘        │   TRUNCATE <table>;            │
                                                   │ fail          │   INSERT … FROM <table>_stage  │
                                                   ▼               │ COMMIT;   (views survive)      │
                                  stop · live table untouched      └────────────────────────────────┘
                                  (soft checks: --accept after review)
```

**The pipeline is one command, `python -m pipeline`, with stages in a fixed order.**
- Every stage can be re-run.
- Every stage writes a row to `data_refresh_log` recording its inputs with sha256 hashes, the roads2 fingerprint, counts, checks and outcome.
- Stages that replace live data build into a `*_stage` table first, run [checks](#7-checks-before-data-is-replaced), and only then swap. The swap is `TRUNCATE` + `INSERT` in one transaction, so nothing that depends on the table (views) is dropped.
- If a stage fails, the live tables are exactly as they were.

**Code map:**

| Piece | Where |
|---|---|
| Stage runner | `pipeline/__main__.py`, `pipeline/stages.py` |
| Refresh log, checks | `pipeline/refresh.py`, `pipeline/checks.py` |
| Geocoding on roads2 | `lrs/geometry_to_measure.py` (also served as `POST /api/lrs/geometryToMeasure`) |
| Conflation (geocode + clean) | `pipeline/conflate.py` |
| Survey load, re-weighting, segment build | `scripts/import_pavement_data.py` (stages B, C, E) |
| Joints | `pipeline/joints.py` (the algorithm of `scripts/joint_breakdown_intersections.py`) |
| Committed flags | `scripts/populate_committed_flags.py` |
| Potential projects | `scripts/find_potential_projects.py` |
| Backups | `scripts/backup_pms.py` |
| Migrations | `scripts/migrate.py`, `db/migrations/` |

> Bridges have their own pipeline, `python -m pipeline bridges …`, which keeps the
> AssetWise bridge inventory (`bridges_all.duckdb`) current. It writes the DuckDB,
> not the PMS tables, and is not part of `all`. See
> [§16](#16-bridges-the-assetwise-pipeline).

## 2. Quick start

All commands run from the repo root on a machine with the PMS database tunnel (`./start-dev.sh` opens it), `lrsops` on the `PATH`, and the survey CSVs.

```sh
# 0. Back up (databases, the tables a refresh replaces, the input files)
PYTHONPATH=. ./venv/bin/python scripts/backup_pms.py            # add --mmsdev to include pms_test

# 1. Make sure the schema is current
PYTHONPATH=. ./venv/bin/python scripts/migrate.py --apply

# 2. Refresh everything: new LRS download + all survey years
PYTHONPATH=. ./venv/bin/python -m pipeline all \
    --survey-dir ~/Downloads/csvs --refresh-dir refresh/$(date +%F)

# Same, but on LRS files already on disk (reproduce a build, or no network to R&H)
PYTHONPATH=. ./venv/bin/python -m pipeline all --survey-dir ~/Downloads/csvs \
    --refresh-dir refresh/$(date +%F) --reuse-lrs .

# Dry run: read and log every input, change nothing
PYTHONPATH=. ./venv/bin/python -m pipeline all --survey-dir ~/Downloads/csvs --dry-run

# Build the raw network (survey as delivered, no GPS conflation) next to the conflated one;
# then set a config's survey_network to raw. Here only the newest file.
PYTHONPATH=. ./venv/bin/python -m pipeline conflate segments commitments --survey-dir ~/Downloads/csvs \
    --survey-mode raw --raw-latest-only --refresh-dir refresh/<run>
```

**Running stages separately:** `python -m pipeline lrs joints segments --refresh-dir refresh/<run>`. Stages always run in pipeline order, whatever order they're named in. A refresh folder holds everything one refresh downloaded and produced, so keep it until the refresh has been reviewed. `refresh/` is git-ignored.

A full refresh of the 2020–2025 surveys takes roughly an hour. Most of that is stage C, which geocodes about 0.9 million GPS points and re-weights them.

## 3. Back up first

`scripts/backup_pms.py` writes to `~/pms_backups/<YYYY-MM-DD_HHMM>/`:

| Step | What it does |
|---|---|
| `dump` | `pg_dump -Fc` of the local `pms` database. With `--mmsdev`, also mmsdev's `pms_test`, streamed over ssh from a `postgres:16` container, so nothing is written to mmsdev's nearly full disk. Each dump gets a sha256 and a table of contents (`*.toc.txt`). Needs the PostgreSQL 16 client (`/opt/homebrew/opt/postgresql@16/bin`, or set `PG16_BIN`), because the server is PG 16 and older `pg_dump` refuses. |
| `verify` | Restores each dump into a scratch database `pms_restore_check`, compares the exact row count of every table with the source, then drops it. **A backup that hasn't restored doesn't count.** |
| `archive` | Copies the tables a refresh replaces into the schema `archive_<YYYYMMDD>` of the same database: `analysis_segments`, `pavement_joints`, `reconflate_normalized`, `condition_history`, `potential_projects`, `projects`, `routes` and both multi-year views, plus the view definitions. Used for before/after comparisons and fast rollback. |
| `files` | Copies every file input (LRS layers, `70.csv`, `intersections.sqlite`, joints CSVs, the TheHub export, the survey CSVs) with a manifest giving path, size, sha256 and mtime. |
| `lrs` | Records the roads2 fingerprint. |

Everything is described in `backup_manifest.json`.

**Restoring:**

```sh
# Whole database, from a dump (overwrites!)
PGPASSWORD=<redacted> /opt/homebrew/opt/postgresql@16/bin/pg_restore --clean --if-exists --no-owner \
    -h localhost -p 5434 -U wvdot_admin -d pms ~/pms_backups/<stamp>/pms_local.dump
```

To put one table back from the archive schema, run this in one transaction:

```sql
BEGIN;
TRUNCATE analysis_segments;
INSERT INTO analysis_segments SELECT * FROM archive_20260924.analysis_segments;
COMMIT;
REFRESH MATERIALIZED VIEW CONCURRENTLY multi_year_segment_analysis;
```

Restoring `pavement_joints` also means setting `joint_builds.status` back: mark the restored build `current` and the newer one `archived`.

## 4. The stages

### A. `lrs`: LRS snapshot

Gets all LRS inputs into the refresh folder from **one** source, so every later stage uses the same LRS.

- **Default: download now** from the WVDOT R&H service (`lrsops`, service URL in `lrsops --help`):
  - `lrsops rhoverlay -l 15,35,22,12,18,49,77,2 --codes-add --carry-json '{"77":["AADT_COMBINATION","AADT_SINGLE"]}' --lrs-database=false --redownload -o lrs_table.csv` writes `lrs_table.csv` plus one `<layer>.csv` per layer.
  - lrsops only downloads when attached to a terminal (its download progress screen needs one; without it `--redownload` fetches nothing and it stops on the missing CSVs), so the pipeline runs the download commands under a pseudo-terminal (`_run(..., tty=True)` in `scripts/import_pavement_data.py`).
  - `lrsops rhoverlay -l 70 --lrs-database=false --redownload` writes `70.csv`, the surface-type events. The joints use only their extents (where pavement is), not the surface type.
- **`--reuse-lrs DIR`:** copy those files from an earlier download instead. For example, the repo root holds the 2026-04-15 download.
- **`intersections.sqlite`:** copied from `--intersections`, by default the repo's copy. With `--rebuild-intersections` it is rebuilt with `lrsops intersections`, from the roads mbtiles (`$LRSPATH/wv_roads12.mbtiles`).
- **roads2 fingerprint:** row count plus an md5 over (routeid, bmp, emp, shape length), recorded in the log. roads2 has no version column, so the fingerprint is how two refreshes can be compared.

### B. `survey`: raw survey → `condition_history`

Each vendor file `<YYYY>.csv` is one survey year; the year is taken from the **file name**, because `COND_YEAR` inside can be stale.

- Each year replaces only its own rows (`DELETE … WHERE survey_year = YYYY`, then insert). Other years are kept.
- `segment_id = ROUTEID-BEG_MP` with the vendor milepoint, and `emp = bmp + 0.1`.
- A value of −1 means "not measured" and is stored as NULL.

### C. `conflate`: locate every record on the LRS → `reconflate_normalized`

See [§5](#5-how-lrs-conflation-works).
- Builds `reconflate_normalized_stage`.
- **NHS gaps of the latest survey file are loaded as delivered.** After the latest year is conflated, every record of that file that lies on the NHS and where conflation left nothing on that stretch of the route is loaded with the vendor's own `ROUTEID` and `BEG_MP` / `END_MP`, without GPS, the way dTIMS reads the file (`pipeline/conflate.nhs_gap_records`).
  - "On the NHS" means at least half the record lies in a layer-22 Federal Aid 1 / 2 / 4 stretch (`22.csv`), matched on the vendor's route and milepoints; the route must exist on roads2.
  - This covers roads the vendor labels under an old route ID. For example, it labels Corridor H (US 48) east of Davis as WV 93, so its GPS falls on US 48 and geocoding used to drop the whole route every year; dTIMS carries it as WV 93 MP 0–11.7.
  - On the 2025 file it fills 376 records, 37.3 NHS miles on 14 routes, mostly Logan US 119 SB (18.4 mi) and WV 93 (11.7 mi).
  - Each is written to `conflation_issues` as `nhs_gap_as_is`, and the stage counts `nhs_gap_as_is_records` / `_miles` per year. Without `22.csv` the step is skipped.
- Writes per-year issues to `conflation_issues`.
- Checks the match rate: at least 97% of GPS points must be located on their record's own route.
- Then swaps into `reconflate_normalized`.

#### Two modes: `--survey-mode conflated` (default) and `--survey-mode raw`

Stage C has two ways to place the vendor files on the LRS, and **both results are kept side by side** (migration 057): conflated mode writes `reconflate_normalized`, raw mode writes `reconflate_raw` (the same columns and conventions). Stage E then builds that mode's **survey network** in `analysis_segments` (`network` = `conflated` / `raw`) and replaces only that network's rows; E1 and E2 run on both. Each config reads one network (`configs.survey_network`, the Config page's Policy tab or the workbook's Model Constants sheet), so **switching a config to raw is a config edit, not a rebuild**. Rebuild a network only when its survey files change.

| | `conflated` (default) | `raw` |
|---|---|---|
| Writes | `reconflate_normalized` | `reconflate_raw` |
| Stage E network | `analysis_segments.network = 'conflated'` | `analysis_segments.network = 'raw'` |
| Code | `phase2_reconflate` + `pipeline/conflate.py` (§5) | `pipeline/raw_survey.py` |
| Where a record goes | its GPS geocoded on roads2, values re-weighted over the overlapping geocoded records | the vendor's own `ROUTEID` and `BEG_MP` / `END_MP`, values as delivered (the way dTIMS reads the file) |
| Files | every `<YYYY>.csv` in `--survey-dir` | every file, or only the newest with `--raw-latest-only` |
| Drops | unlocated records, whole routes with a > 1 mi span | only records that can't be placed (below) |
| NHS gap fill | yes (latest file) | not needed: every placeable record is loaded as delivered |
| Check | GPS match rate ≥ 97% (soft) | records placed ≥ 97% (soft), > 0 rows per year (hard) |
| Run time (2020–2025) | about an hour | about 4 minutes |

**Raw mode** (`python -m pipeline conflate --survey-mode raw [--raw-latest-only]`):
- Use it when the survey should be read exactly as the vendor delivered it: to match dTIMS, to load a new file quickly, or when only the latest file is wanted ("the last raw pavement file").
- It skips the geocoding, the fallback/prefix route matching, the > 1 mi span route drops and the re-weighting. The GPS columns are ignored.
- Every record is kept on its `ROUTEID` + `BEG_MP` / `END_MP` with its values as delivered. The rows are shaped exactly like the conflated output: `segment_id` = the vendor's `Unique`, `coverage_pct` 1.0, the same numeric and categorical fields, −1 → NULL, `Percent_Cracking` (2020–2022) read as `PERCENT_CRACKING`, and the same Good/Fair/Poor grades and surface mapping (`add_gfp`). They go through the same `_insert_reconflate_batch`, then `reconflate_raw_stage` and `swap_in` into `reconflate_raw`; the conflated table is not touched.
- A record is dropped, and counted in `conflation_issues` by route, when it:
  - has no route id (`raw_no_route`);
  - is on a route that isn't on roads2 (`raw_not_on_roads2`);
  - has a missing milepoint (`raw_no_milepoints`);
  - has `END_MP ≤ BEG_MP` (`raw_zero_length`);
  - lies outside the roads2 route (`BEG_MP` below the route's start − 0.01 mi or `END_MP` beyond its end + 0.05 mi, the NHS-gap tolerances; `raw_outside_roads2_extent`);
  - repeats a `Unique` already placed that year (`raw_duplicate_record`; the first is kept).
- Each year also gets a `raw_mode_placed` row with the number placed. `data_refresh_log` records the mode in `inputs.survey_mode` / `counts.mode`, the files, and per year the records, placed, placed miles, placed rate and drops.
- Each record keeps its survey date (`survey_date`, migration 060) from the file's `DATE` (`Date` in 2020–2022): Excel serial days (2023), `YYYY-MM-DD hh:mm:ss`, or `dd/mm/yyyy` (2024–2025, read day-first). Stage E carries the date of the record each cell took into `analysis_segments.survey_date`, which a config's `survey_excluded_*` window reads. Conflated mode leaves it NULL.
- `--raw-latest-only` loads just the newest file, so after the swap `reconflate_raw` (and the raw network's grid) holds only that year. Older years stay in `condition_history`.
- `--dry-run` places every record and runs the checks without writing anything but the log row.
- On the 2020–2025 files (2026-09-30) raw mode places 99.8–100% of each year's records: 454,807 rows against 431,684 conflated; the difference is the records the conflated path drops (unlocated GPS, whole routes with a > 1 mi span), about 5,000 a year in 2020–2022 and 6,700 in 2024. On 2025 it places all 48,516 records (4,782.0 mi, 987 routes); where both modes have a record the milepoints are the same and IRI differs by 0.18 in/mi on average (the re-weighting).

### D. `joints`: pavement joints → `pavement_joints` (a new build)

See [§6](#6-joints).
- Builds the joints from `70.csv` + `intersections.sqlite` + `2.csv` of this refresh.
- If they're identical to the current build (same IDs and spans), nothing changes.
- Otherwise it records a new build in `joint_builds`, writes `joint_crosswalk` from the previous build, and replaces `pavement_joints`.

### E. `segments`: the engine's network → `analysis_segments`

1. **Grid.** A 0.1-mi grid on the LRS: for every (route, `ROUND(actual_bmp, 1)`) cell, the **most recent survey year** in `reconflate_normalized` wins. That year is stored in `analysis_segments.survey_year`.
   - **Unsurveyed road** (migration 056): the grid is then filled with the 0.1-mi cells of every roads2 route on sign systems 1, 2, 3, 4, 7 and 8 (`UNSURVEYED_SIGNS`: Interstate, US, WV, County, federal-aid non-state, HARP — dTIMS's analysis inventory is roads2 limited to these) that have no surveyed cell, clipped to the route's ends, with `has_survey` FALSE and no condition values. dTIMS carries that road (its no-data sections, CCI 99); configs decide whether runs do (`unsurveyed_policy`, Business Logic).
   - The overlay also emits pieces of joints and LRS events outside the grid; those carry neither a survey year nor the fill's flag and are dropped.
   - Stage E's checks judge the surveyed rows (joint and district coverage, % Good) and report the fill on its own (`unsurveyed_length_matches_milepoints`: rows, miles, rows without a joint).
2. **Overlay.** `lrsops overlay` splits the grid:
   - first at joint boundaries (op 1, carrying `joint_id`)
   - then at every LRS attribute change (op 2, carrying AADT, district, county, Federal Aid type (layer 22), functional class, route status and the single/combination AADT)

   A row can therefore be much shorter than 0.1 mi.
3. **Transform** (polars):
   - missing indices treated as 5.0
   - truck share = (single + combination) / AADT
   - `current_age`: the oldest starting age, using the **system default config's** family rules and curves (`pipeline/families.py`)
   - **`length_miles = end_mp − begin_mp`**
   - `joint_build_id`
4. **Check and swap.** Written to `analysis_segments_stage`, [checked](#7-checks-before-data-is-replaced) (% Good / % Poor are the MAP-21 rating of the surveyed IRI, cracking and rutting / faulting, by lane-miles, on both the stage and the live table), then swapped in.
5. **dTIMS inputs** ([E1](#e1-inputs-the-dtims-model-inputs)) are filled on the new rows.
6. **Families, every config.** The swap renumbers `analysis_segment_id`, so each config's classifier reruns (as in [E2](#e2-families-rerun-the-family-rules--segment_families)) and rewrites its `segment_families` partition: family, pavement/rehab/truck type and the dTIMS starting state (indices, CCI, ages, raw distress and its MAP-21 rating). A config whose rules leave a segment unmatched stops the stage.

### E1. `inputs`: the dTIMS model inputs

Not part of `all` (stage E runs it after its swap); `python -m pipeline inputs` runs it on its own (`pipeline/dtims_inputs.py`), e.g. after loading CLOSED projects — follow it with `families`. It fills the inventory **facts** on the live `analysis_segments`, in one transaction; choosing among them (growth-source order, how much project coverage counts, which cracking measure, route groups such as the HPMS stand-in) is each config's policy (Business Logic § 1 *Policy tables*):

| Column | Source |
|---|---|
| `sign_code`, `route_number`, `supp_code` | route_id (sign = 3rd character; route number; supplemental code = characters 10–11, used by the Turnpike route group) |
| `inventory_cci`, `raw_psi` … `raw_csi` | the vendor's CCI and indices as delivered (−1 → NULL), from the `reconflate_normalized` row of the segment's grid cell and survey year |
| `crack_pct_dtims` | that row's PERCENT_CRACKING (what dTIMS read as PCRK); imported from the 2026-09-25 import code on, so older survey rows have none |
| `adt_growth_layer2`, `adt_growth_future`, `adt_growth_district`, `adt_growth_event` | LRS layer 2 (`2.csv` of the refresh, else the repo's), the event overlapping the segment the **longest**: `AADT_ESCALATION_PCT` (`layer2`; empty in the 2026 download), the compound annual rate of `FUTURE_AADT` over `AADT` (93% of segments, median 0.48%/yr), and the district median of those; `adt_growth_pct` / `adt_growth_source` keep the default order (then 0) for the browse pages |
| `rehab_year`, `rehab_project_id`, `rehab_treatment_id`, `rehab_coverage`, `rehab_source` | the latest CLOSED project overlapping the segment (route + milepoints), its own treatment code and the share of the segment it covers, **rebuilt from the current spatial matches** every time (25% of segments on the 2026-09-24 network) |
| `iri_source`, `rut_source`, `flt_source` | `survey`, or `dtims_default` where the engine derives the value (IRI from PSI, rut from RDI, faulting 0) |
| `fed_aid_code`, `fed_aid_desc` | LRS layer 22 **Federal Aid** (`22.csv` of the refresh, else the repo's), `FAS_TYPE` of the event overlapping the segment the longest: 1 Interstate, 2 NHS, 3 STP eligible, 4 Intermodal Connectors, 5 Non-Federal-Aid. Without `22.csv` the value stage E's overlay loaded is kept. |
| `nhs_code`, `nhs_desc` | the **NHS designation, from Federal Aid as in dTIMS** (not LRS layer 36, used before v1.7.2): the FAS type when it is 1, 2 or 4, else 0 (`NHS_FAS_TYPES` in `pipeline/dtims_inputs.py`). `nhs_code > 0` = on the NHS; dTIMS's non-Interstate NHS set (its `DEL_NHS` filter: `Fed_Aid` 2 or 4, not Interstate) is `nhs_code IN (2, 4)`. |

Patch area (county treatments) is not imported. Each config's family step then builds the starting state from these facts with its policy (see Business Logic § 2): the rehab year counts where the project covers at least `min_rehab_coverage` (0.5) of the segment, and its rehab type is the one the config's treatment of that code sets.

### E2. `families`: rerun the family rules → `segment_families`

Not part of `all` (stage E already regenerates every config). `python -m pipeline families` reruns each config's saved rules (or only `--config N`) against the live `analysis_segments` and writes that config's `segment_families` partition: family, pavement type, rehab type (from the segment's latest CLOSED project where it counts), truck load and the dTIMS starting state at the config's start year (else the current year; the seven indices with CCI from the vendor, ages from the rehab year capped at `max_start_age` — `missing_rehab_age` when there is none — raw distress and its rating), all with the config's compiled policy; only rows that change are upserted and rows of segments that no longer exist are removed, in one transaction per config. `--dry-run` shows the segments per family and how many would change without writing. Each config's run is logged in `data_refresh_log` as stage `E2_families`, with `config_id` and the rule set in `inputs`.

The same rerun happens when an admin saves a config's rules (Config → `<config>` → Family Rules) and when an Excel import changes a config's rules, curves, reset operations, route groups, cracking rules, initializers, counters, Hub treatment map or model constants (in the same transaction, classifying with the config as that transaction will commit it). Run it by hand after changing `pavement_family_rules` or `pavement_families` outside the app. Migration 030 itself needs no rerun: it copies the existing classification into config 1. About 5 s per config.

### F. `commitments`: committed projects → `analysis_segments.is_committed`

Runs `scripts/populate_committed_flags.py --apply --base-year 2026`.
- Every project with status `planned` / `designed` / `awarded` / `in_progress` (including run-validation commits) flags the segments it overlaps **by milepoint**, so flags never depend on joint IDs.
- The calendar year becomes a program year (2026 = year 1).

### F2. `patching`: patching quantities → `analysis_segments.patch_l/m/h`

`python -m pipeline patching [--patch-network KEY]` (also part of `all`, after `commitments`).

- **Source.** The patching (Patch_L / Patch_M / Patch_H, sq ft) of a dTIMS network stored in the database:
  - `dtims_reference_network_elements`, loaded by `scripts/dtims_audit/store_reference_runs.py`;
  - by default `dtims-pms-analysis-network-2026-09`, the 29,427-section pavement analysis network.
- **Mapping.** Each segment, on both survey networks, takes the dTIMS section it overlaps most on its route, and a share of that section's patching equal to its share of the section's length. Each segment therefore carries the section's patching percentage, which is what the `patch_pct_min` trigger gate reads (patching ÷ (length × 5280 × 8) × 100).
- **No match.** Segments on no section get NULL.
- **In place.** Nothing is rebuilt and no other column changes. The three columns are rebuilt from scratch on each run, and `--dry-run` rolls the change back.
- **After a rebuild.** Stage E empties the columns, so run this after it; `all` does.
- **Check.** At least one segment gets a patching source (hard).
- **2026-09-30 result.** 356,526 conflated and 356,528 raw segments, about 197,000 of each with patching; 2,708 mi at 15 % or more (County Thick Overlay's patching branch).

### G. `derived`: views and potential projects

- Refreshes `multi_year_segment_analysis` and `multi_year_condition_analysis` concurrently (both have unique indexes).
- Rebuilds `potential_projects` in place (`TRUNCATE` + insert).
- Fails if the data has a survey year the views don't cover; see [§10](#10-adding-a-survey-year).

## 5. How LRS conflation works

The vendor measures a road in ~0.1-mile records, each with start and end GPS points and the vendor's own milepoints (`BEG_MP`/`END_MP`). The vendor's milepoints don't line up with the LRS, so every record is re-located on it.

**1. Geocode on roads2.** The start and end GPS points of every record go through `lrs.geometry_to_measure` in batches of 2,000, directly against the database with a 15 m tolerance.

For each point it:
- finds every route within 15 m, using the GiST index on `operations.roads2`
- picks each route's nearest part (roads2 routes can have up to 6 parts)
- takes the M value at the closest point, `ST_InterpolatePoint`, in miles

It then chooses:

| Method | Meaning |
|---|---|
| `exact` | the record's own `ROUTEID` |
| `prefix` | the same route with its direction letter (N/B/E/S/W) stripped |
| `fallback` | the nearest route of any ID: kept, but counted as not located on its own route |
| `none` | nothing within 15 m |

This is the same computation, with the same request and response, as the dashcam `geometryToMeasure` service that was used before. On 500 random 2025 survey points both gave identical results. On 19,264 records the new milepoints were within 0.005 mi of the stored ones for 99.7% of records (median 0.0002 mi).

**2. Clean.** Each drop is written to `conflation_issues`, not just printed:
- BMP > EMP is swapped.
- Records whose start or end couldn't be located are dropped (`not_located`).
- A whole route is dropped if any record on it spans more than 1 mi after geocoding (`route_dropped_span_gt_1mi`). That's the signature of a fallback onto the wrong part of a route.
- Records that fell back to another route are listed (`fallback_route`).

**3. Re-weight** (`auto_conflate`).
- For each vendor record, every geocoded record overlapping its vendor window contributes in proportion to the overlap length, with the weights normalised to 1.
- Numeric fields (indices, IRI, rut, faulting, cracking) take the weighted mean. A −1 (missing) anywhere makes that field missing.
- Surface and shoulder type take the value with the largest share.
- Good/Fair/Poor grades are added.

**4. Grid and overlay:** stage E.

Two rules follow from this:
- **Geocoded milepoints (`actual_bmp`/`actual_emp`) are the only milepoints joined on.** Vendor milepoints stay in `condition_history` for reference.
- **Nothing calls an external geocoding service.** The API endpoint and the pipeline use the same library.

## 6. Joints

A joint is the unit the optimizer selects: a stretch of one route, about 0.2–4 miles. It's built by `pipeline/joints.py`, the algorithm of `scripts/joint_breakdown_intersections.py`, which is kept as a CLI wrapper.

**Inputs, all from the same refresh:**
- LRS layer 70 surface events: `OBJECTID, ROUTE_ID, FROM_MEASURE, TO_MEASURE`. Each event becomes a vendor joint `70_<OBJECTID>`. Only events with TO > FROM on a route in the `routes` table are used.
- `intersections.sqlite`
- layer-2 AADT

**Algorithm:**

1. Merge touching vendor joints on a route (gap ≤ 0.001 mi) into continuous sections, **whatever their surface type**. A section keeps its first vendor ID. So a surface-type change never starts a new joint; a section ends only where the pavement events have a gap or the route ends.
2. Sections of 3 mi or less stay whole.
3. Longer sections are split at intersections.
   - A candidate lies strictly inside the section.
   - The crossing route has sign system 1/2/3/4/7 and a 13-character ID, so no ramps.
   - The crossing route isn't the same US route in the other direction.
   - Each node keeps its highest-AADT crossing, and nodes within 0.1 mi are clustered.
4. Breaks are placed highest-AADT first, keeping every piece at least 1 mi long. Lower-AADT candidates are then used only inside pieces still over 4 mi.
5. So **route termini** are what cut the long roads: in the 2026-04-15 build, 6,788 of the 22,480 joints (13,438 of 29,579 miles, 45%) come from splits at crossing routes; the other joints are whole sections of 3 mi or less, ending where the pavement events have a gap or the route ends.
6. `joint_id = 70_<routeid>_<n>`, where n numbers the pieces along the route by milepoint. Each piece also records:
   - `parent_joint_id`: the vendor joint it came from
   - `termini_routeid` / `termini_aadt` / `termini_label`: the crossing route at each break

**Stable IDs.** Within one build, IDs are deterministic; the per-node AADT sort is stable. Across builds they are **positional**, so a change on a route (a new AADT count, a new intersection, a changed surface event) can renumber the later joints on that route. So:

- **Every build is recorded** in `joint_builds`:
  - its inputs with hashes
  - the roads2 fingerprint
  - the parameters
  - the joint count

  Every build's joints are kept in `joint_builds_archive`. `pavement_joints` holds only the current build.
- **`joint_crosswalk`** maps every joint of the previous build onto each joint of the new build it overlaps on the same route, with the overlap in miles and as a share of the old joint.
- **Runs record** `configuration.joint_build_id`; runs made before versioning are build 0. The Validate page maps a run's joints onto the current build through the crosswalk, composed across builds and keeping overlaps of at least 5%. A run made on build 0 therefore still simulates and commits correctly after a rebuild.
- **Committed-project flags are applied by milepoint** (stage F), not by joint ID.

**The loop is gone.** The joint input is always layer 70. Before, it was re-exported from `pavement_joints`, so each rebuild fed the previous output back in and lost the vendor boundaries. Build 0 (the joints before versioning) is reproduced exactly by the new code from the 2026-04-15 layer 70: 22,480 joints, identical IDs and spans.

**Running it alone:** `python -m pipeline.joints --layer70 70.csv --intersections intersections.sqlite --aadt 2.csv --out joints.csv` writes the CSV only. `python -m pipeline joints` also loads it as a build.

## 7. Checks before data is replaced

| Stage | Check | Limit | Hard / soft |
|---|---|---|---|
| C | Share of GPS points located on their own route, per survey year | ≥ 97% | soft |
| C (raw mode) | Records placed on their own route and milepoints, per survey year | > 0 | hard |
| C (raw mode) | Share of the file's records placed, per survey year | ≥ 97% | soft |
| E | New table has rows | > 0 | hard |
| E | Σ `length_miles` = Σ(`end_mp − begin_mp`) | within 0.1% | hard |
| E | Share of segments with no joint | ≤ previous + 0.5 pp | hard |
| E | Share of segments with no district | ≤ previous + 0.5 pp | hard |
| E | Routes that aren't on roads2 | no new ones | hard |
| E | Network % Good (length-weighted CCI ≥ 3) vs the live table | change ≤ 2 pp | soft |
| G | Every survey year is in the multi-year views | all covered | hard |

A failed check stops the stage and leaves the live table unchanged. Soft checks can be accepted with `--accept` once someone has looked at the numbers in the log. Every check's value, baseline and limit is stored in `data_refresh_log.checks`.

## 8. Bookkeeping tables

| Table | Contents |
|---|---|
| `data_refresh_log` | One row per stage run: `run_label` (the refresh folder name), `stage`, times, `status` (`ok` / `failed` / `dry_run`), `inputs` (sha256 per file), `lrs_fingerprint`, `counts`, `checks`, `message` |
| `conflation_issues` | Per survey year: `not_located`, `fallback_route` and `route_dropped_span_gt_1mi` counts by route, plus a `summary` row with the number of points. Raw mode writes its `raw_*` drop reasons by route, a `raw_mode_placed` row and a `raw_summary` row with the number of records. Each mode replaces only its own rows of a year, so both sets coexist |
| `joint_builds` / `joint_builds_archive` / `joint_crosswalk` | Joint versioning ([§6](#6-joints)) |
| `schema_migrations` | Applied migrations ([§9](#9-schema-migrations)) |
| `analysis_segments.survey_year`, `.joint_build_id` | Where each segment's condition and joint come from |

Useful queries:

```sql
-- The last refresh, stage by stage
SELECT stage, status, finished_at - started_at AS took, counts, checks
  FROM data_refresh_log WHERE run_label = (SELECT run_label FROM data_refresh_log ORDER BY refresh_id DESC LIMIT 1)
 ORDER BY refresh_id;

-- Routes that lost records in conflation
SELECT survey_year, reason, count(*) AS routes, sum(records) AS records
  FROM conflation_issues WHERE reason <> 'summary' GROUP BY 1, 2 ORDER BY 1, 2;

-- How old is "current" condition?
SELECT survey_year, count(*), round(sum(length_miles), 1) AS miles FROM analysis_segments GROUP BY 1 ORDER BY 1;
```

## 9. Schema migrations

Files in `db/migrations/` are applied **only** through `scripts/migrate.py`, which records each one in `schema_migrations`.

- 001–024 predate the runner and were recorded once with `--baseline 024`.
- Run `python scripts/migrate.py` to list pending migrations, and `--apply` to apply them in order, one transaction each.
- A file edited after it was applied is reported, never re-run.
- Apply to every environment (local, mmsdev) before running the pipeline there.

## 10. Adding a survey year

1. Put `<YYYY>.csv` in the survey folder.
2. Extend the per-year columns before refreshing, because stage G refuses otherwise:
   - `multi_year_segment_analysis` and `multi_year_condition_analysis` (migrations 009 / 010): add the year's columns in a new migration that recreates both views, with their unique indexes.
   - `scripts/find_potential_projects.py` `YEARS`.
3. Run `python -m pipeline all --survey-dir …`. Stages B and C load the new year; E picks the newest year per cell automatically.

## 11. Where every input comes from

| Input | Produced by | Used by |
|---|---|---|
| `<YYYY>.csv` survey files | Pavement survey vendor (one file per year; `~/Downloads/csvs` holds 2020–2025) | B, C |
| roads2 (`dot12_test.operations.roads2`) | The DOT12/MMS database, maintained outside PMS; read-only | C, the maps, the LRS API |
| `lrs_table.csv`, `2.csv`, `12.csv`, `15.csv`, `18.csv`, `22.csv`, `35.csv`, `49.csv`, `77.csv` | Stage A, `lrsops rhoverlay` (WVDOT R&H service) | D (`2.csv`), E, E1 (`2.csv`, `22.csv`) |
| `70.csv` (surface-type events) | Stage A, `lrsops rhoverlay -l 70` | D |
| `intersections.sqlite` | `lrsops intersections` over the roads mbtiles (`$LRSPATH/wv_roads12.mbtiles`) | D |
| `routes` table | `db/load_routes.py` (`wv_2025.csv`) | D (route filter) |
| `projects` (history) | `scripts/import_past_projects.py` (`raw_pavements.xlsx`, a TheHub export) | F, the Projects page |
| `projects` (committed) | Run Validation commits | F |

## 12. Refreshing mmsdev

mmsdev's database (`pms_test`) is on a different server from the local one.

1. Back up: `scripts/backup_pms.py --mmsdev`.
2. Deploy the code, then apply migrations inside the container: `docker exec pms python scripts/migrate.py --apply`. The first time, run `--baseline 024` before that.
3. Run the pipeline from a machine that can reach both `pms_test` (set `DB_*` to point at it) and the R&H service. `lrsops` isn't in the container.

   Alternatively, refresh locally, review it, and copy the refreshed tables across with `pg_dump -t … | pg_restore`, in the same `TRUNCATE` + `INSERT` spirit.

## 13. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `pg_dump: server version mismatch` | Use the PG 16 client (`PG16_BIN`) |
| Stage C match rate below 97% | Look at `conflation_issues` for the year: a new route missing from roads2, or GPS problems in the vendor file. Accept with `--accept` only after review |
| `routes_not_on_roads2` failed | A new route ID isn't in roads2 yet. Update roads2 (DOT12 LRS import) or accept that the route can't be mapped |
| `network_pct_good` needs accept | Compare `counts.new` and `counts.live` in the log. Expected after a length fix or a new survey year |
| Stage G: "survey years … aren't in the multi-year views" | See [§10](#10-adding-a-survey-year) |
| `lrsops overlay failed` | Check `lrs_table.csv` and the joints CSV in the refresh folder; re-run `python -m pipeline segments --refresh-dir …` |
| Validate page shows odd joints after a rebuild | Check `joint_crosswalk` covers the run's build (`configuration.joint_build_id`, default 0) |

## 14. What changed from the old import

| Before | Now |
|---|---|
| Geocoding by HTTP to the dashcam service | `lrs.geometry_to_measure` on roads2, same request and response |
| Rows without GPS shifted every later record's milepoints | Results stay aligned to their rows |
| Unlocated records and dropped routes only printed | Recorded in `conflation_issues` |
| `DROP TABLE … CASCADE` (silently dropped `multi_year_segment_analysis`) | Stage tables + checks + `TRUNCATE`/`INSERT` swap |
| Joints re-exported from `pavement_joints` into the breakdown (a loop) | Always from LRS layer 70; versioned builds + crosswalk |
| `length_miles` fixed at 0.1 (network ~10% too long) | `end_mp − begin_mp` |
| No record of which survey year a segment's condition came from | `analysis_segments.survey_year` |
| Database password as a default in scripts | From `.env` only |
| Hand-applied migrations | `scripts/migrate.py` + `schema_migrations` |
| Several competing scripts (`create_analysis_segments.py`, `joint_breakdown.py`, `reimport_pavement_joints.py`) | Removed or retired to pointers |

## 15. Refresh history

| Date | Where | What | Result |
|---|---|---|---|
| 2026-09-24 | local `pms` | First pipeline refresh: 2020–2025 surveys, LRS files from 2026-04-15 (`--reuse-lrs`), roads2 fingerprint `3bf51742…` | See below |

What the 2026-09-24 refresh showed:
- **Conflation is unchanged:** the same records and routes per year as the dashcam-era import (431,309 records). The match rate on the record's own route was 97.3–99.7% by year.
- **Joints** are identical to build 0, so no new build was made.
- **`analysis_segments`:**
  - 265,590 rows
  - Σ `length_miles` 23,935.1 mi, previously 26,303.9
  - length-weighted % Good 24.24, previously 23.26
  - joint and district coverage unchanged
- **Condition by survey year:** 2024 for 19,151 mi, 2025 for 4,710 mi, and older years for 74 mi.
- **Runs made before the refresh** show a small "data changed" difference on the Validate page: up to 1.9 pp for run 270, because segment lengths are now real.
- The first attempt at stage E was **stopped by its checks**: the overlay's pieces outside the surveyed grid had been kept. The live data wasn't touched; the fix is in stage E.

The full report is in `refresh/2026-09-24_local/comparison.md` (`scripts/compare_refresh.py --archive archive_20260924`). The backup is `~/pms_backups/2026-09-24_1605/`.

## 16. Bridges: the AssetWise pipeline

The Bridges and BMS pages read the bridge inventory from **`bridges_all.duckdb`**
(`INSPECT_DB`, ~8 GB). It is a copy of WVDOT's Bentley AssetWise Inspections
(InspectTech) tenant, opened read-only by the app and never written by it.
`python -m pipeline bridges` keeps that file current and ships it to the
servers. The code is in `pipeline/bridges/`, ported from inspect_tech `analysis/`.

It is separate from the pavement stages:

- It writes the DuckDB, not PMS tables, so `all` does not run it and it needs no
  `backup_pms.py`.
- The DuckDB keeps its own previous generation instead: `bridges_all.prev.duckdb`
  sits beside it.

```sh
python -m pipeline bridges auth login          # once: sign in to Bentley in a browser window
python -m pipeline bridges sync --dry-run      # how many bridges changed since the last sync
python -m pipeline bridges sync                # update bridges_all.duckdb
python -m pipeline bridges push mmsdev --dry-run
python -m pipeline bridges push mmsdev         # ship the differences, swap, restart the containers
python -m pipeline bridges <command> --help
```

### 16.1 Commands

| Command | What it does | Logged |
|---|---|---|
| `auth login` | Opens a visible Chromium window (a Playwright profile, `BENTLEY_PROFILE`). You sign in to Bentley once; the password and MFA are yours to type. | no |
| `auth refresh` | Headless. Renews the session silently, then writes the bearer token (`BENTLEY_TOKEN_FILE`) and the cookie files (`BENTLEY_SECRETS_DIR`), all mode 600. It checks the token against OData. Exits 0 when OK, 2 when a person must run `auth login` again. | no |
| `auth watch [--every 30]` | `refresh` in a loop; it never lets the token get within 10 minutes of expiry. | no |
| `auth status` | Token minutes left and cookie-file ages. No network. | no |
| `refresh-token [--once]` | Cookie-only fallback: scrapes a new bearer from `ASSETWISE_TOKEN_PAGE` using `bentley_cookie.txt`. | no |
| `sync` | Incremental update of the DuckDB (below). Options: `--dry-run`, `--since <ISO UTC>`, `--reuse-delta`, `--no-swap`, `--compact-only`. | `bridges_sync` |
| `push <host>` | Brings a server's copy in line with the local one, shipping only the differences (below). Options: `--dry-run`, `--no-restart`. | `bridges_push` |
| `dump <BARS>` / `dump --all` | `dump_bridge`: every inspection of one bridge, or of every bridge, into a SQLite file (`--db`). `--lean -j 8` is the profile the snapshot and the sync use. Add `--pdf` for report PDFs. | `bridges_dump` |
| `extract-reads` | Rebuilds `reads.json` / `.csv` / `.md` in `bridges/analysis_reference/` from the saved endpoint list, Swagger and EDMX. No network. | `bridges_extract_reads` |
| `infobridge` | Loads an FHWA InfoBridge export (one row per structure per NBI year, with climate) into `ib_bridge_year` and `qv_bridge_climate` in `INSPECT_DB`, replacing them. Checks first (InfoBridge columns, years, structure numbers, ≥ 1,000 rows) and writes nothing on a failure. Keeps the source beside the extract (`sources/infobridge_<date>.txt`). Options: `--file` (required), `--db`, `--dry-run`. Ship with `push`. | `bridges_infobridge` |
| `spend` | Refreshes `bms.bridge_spend`: every bridge's MMS work cost and TheHub spend (its deck-area share of each project, `bms.hub.deck_area_shares`), for the bridge list. Each source is swapped in on its own, and a read with under half the previous bridges is refused. Options: `--source mms\|hub\|all`, `--dry-run`, `--force`. The API runs it nightly at `BRIDGE_SPEND_REFRESH_AT` (default 02:30 Eastern; see BMS_Business_Logic). | `bridges_spend` |

`pipeline/bridges/godump/` is a separate Go tool (`go build`) that dumps every
OData entity set verbatim into SQLite. It reads the same `BENTLEY_TOKEN_FILE` /
`ASSETWISE_API`. `pipeline/bridges/debris_overlap_queries.sql` keeps the
heaviest queries of the debris-narrative analysis.

**Needs:** `duckdb` (in requirements.txt). `auth` also needs Playwright, which is
*not* in requirements.txt. Install it once on the machine that runs the sync:
`pip install playwright && playwright install chromium`.

### 16.2 How `sync` works

1. **Credentials:** `auth refresh`, then again every 40 minutes while the run
   lasts. The bearer lives about 65 minutes.
2. **What changed:** OData since the last sync, minus a 2-hour overlap:
   - `AssetTasks` with `LastEditDate` or `CreateDate` later than that;
   - `Assets` with `AssetTypeId 1` and `LastUpdatedDate` later than that;
   - `AssetValues` with `LastUpdatedDate` later than that.

   The last sync is recorded in `.sync_state.json` (`BRIDGES_SYNC_STATE`).
3. **Dump:** `dump --only-ids <changed> --lean -j 8` into a fresh SQLite delta in
   `BRIDGES_SYNC_WORK`.
4. **Splice:** into an APFS clone of the DuckDB. For each table, the changed
   bridges' rows are deleted and the delta's rows inserted. Rows are matched
   by `as_id`, by `ast_id` for inspection junctions, or by primary key for
   lookups. Only bridges whose dump finished cleanly are touched, so a failed
   dump never deletes data.
5. **Derived tables:**
   - The per-bridge `v_*` tables are rebuilt from `views_analysis.sql`.
   - `v_field_usage` and `v_inspector_year` are recomputed statewide.
   - `qv_bootstrap.sql` rebuilds the `qv_*` / `dt_*` analysis layer, and loads
     [Bridge Query Context](/docs/Bridges_Query_Context) into `qv_doc`.
   - It then rebuilds `qv_inspection_card` (`bridges.queries.inspection_card_table_sql`,
     about 1 s). This table is one row per inspection with the bridge page's card ratings and
     counts, so the Inspections list doesn't scan `report_value`.
   - Then `qv_traffic_load_history` (`bridges.queries.traffic_load_table_sql`, under 1 s):
     one row per inspection with its NBI / SNBI traffic and load-rating items and the derived
     truck ADT, for the bridge page's truck traffic and load rating cards.
   - Then `qv_bridge_list` (`bridges.queries.bridge_list_table_sql`, under 1 s): one row per
     bridge with the list's columns (design type and family, material, spans, longest span,
     length, lowest current rating, route and feature crossed), so the bridge list pages,
     filters and sorts in the database.
6. **Check and swap:** the table counts are checked (`asset`, `inspection`,
   `report_value`, `asset_value`, `v_bridge_card`, `v_canonical_rating`,
   `dt_history`, `qv_bridge_decoded`); none may shrink by more than 3%. Then
   the live file becomes `bridges_all.prev.duckdb` and the new file takes its
   place.
7. **Compact:** `COPY FROM DATABASE` into a fresh file. Every table's row count
   and the view count must match before the compacted file is swapped in.

The app opens the file read-only per request, so it never sees a half-built
database.

Exit codes: 0 = OK or nothing changed; 1 = error (the live file is untouched);
2 = a person must run `auth login`. On macOS the sync also posts a
notification.

### 16.3 Schedule (launchd, on the machine that holds the DuckDB)

| Job | Plist (`pipeline/bridges/launchd/`) | When |
|---|---|---|
| Token refresh | `com.inspecttech.bentley-auth.plist` → `python -m pipeline bridges auth refresh` | every 30 min, and at load |
| Nightly sync | `com.inspecttech.sync-duckdb.plist` → `python -m pipeline bridges sync` | 02:15 local |

Both run `venv/bin/python -m pipeline …` from the PMS repo, so the settings come
from its `.env`. The logs are `~/Library/Logs/inspecttech-bentley-auth.log` and
`~/Library/Logs/inspecttech-sync.log`.

The plists keep the labels of the inspect_tech jobs they replace, so only one of
each can be loaded:

```sh
launchctl unload ~/Library/LaunchAgents/com.inspecttech.sync-duckdb.plist 2>/dev/null
cp pipeline/bridges/launchd/*.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.inspecttech.bentley-auth.plist
launchctl load ~/Library/LaunchAgents/com.inspecttech.sync-duckdb.plist
```

The sync does not push. Pushing to a server is a deliberate step.

### 16.4 Pushing to mmsdev (`push`)

mmsdev (and mms) keep the file at `/bms_fixtures/bridges_all.duckdb`
(`BRIDGES_PUSH_DIR`). It is mounted read-only into the `amps` container and the
Bridge Wizard's `bms-sandbox` sidecar. (The standalone `pms` and `bms` apps on
mmsdev were decommissioned on 2026-09-27; AMPS replaces both.) Copying 8 GB
after every sync is wasteful, so `push` diffs first:

1. **Fingerprint:** every table, on both sides, grouped by `as_id`, else by
   `ast_id`, else the whole table: the row count plus the sum of an md5 of each
   row. The server side runs in a throwaway container from the image the running
   `amps` container was started from (`BRIDGES_PUSH_IMAGE` = `@amps`), which has
   DuckDB.
2. **Diff:** each table is copied (identical), spliced (some keys differ) or
   replaced (a new table, a changed schema, or no key).
3. **Delta:** a small DuckDB file with just the differing rows, the keys to
   replace, and the DDL for every table and view. It is built in
   `BRIDGES_SYNC_WORK`, then rsynced (resumable) to `/bms_fixtures/push_work/`.
   The server's free space is checked first; the old `prev` copy is removed
   only when the space is needed.
4. **Build:** on the server, a new file is written table by table: the live
   rows minus the replaced keys, plus the delta. The live file is only read.
5. **Verify:** the new file is fingerprinted again and must match the local
   fingerprints exactly, table for table. Otherwise nothing is swapped.
6. **Swap and restart:** the live file becomes `bridges_all.prev.duckdb` and the
   new file takes its place. Then the containers in `BRIDGES_PUSH_RESTART` are
   restarted (default `amps`, then `bms-sandbox`); the bind mount pins the old
   inode until a container restarts. Only the first container is required; the
   push then reads the asset and inspection counts through it, at
   `BRIDGES_PUSH_APP_DB`.

`--dry-run` stops after the diff. `--no-restart` swaps the file but leaves the
apps serving the old one until they restart. Exit 0 = OK or already identical;
1 = error, with the live file untouched.

### 16.5 Settings (`.env`; `pipeline/bridges/settings.py`)

Credentials and cookies are always written **outside the repo**. Never commit
`bentley_cookie*.txt`, `bentley_pf.txt` or a token.

| Key | Default | Used for |
|---|---|---|
| `INSPECT_DB` | `~/Downloads/inspect_tech/analysis/bridges_all.duckdb` | the DuckDB that sync updates and push ships (also what the app reads) |
| `BRIDGES_SYNC_WORK` | `sync_work/` beside `INSPECT_DB` | SQLite delta, changed ids, push delta (up to ~13 GB for a big re-dump), fallback log |
| `BRIDGES_SYNC_STATE` | `.sync_state.json` beside `INSPECT_DB` | last successful sync |
| `ASSETWISE_SITE` | `https://wvdot-it.bentley.com` | AssetWise web app (sign-in, token page) |
| `ASSETWISE_API` | `https://wvdot-it-api.bentley.com` | OData / REST API |
| `ASSETWISE_TOKEN_PAGE` | an `inspection_info.aspx` page on the site | page `refresh-token` scrapes |
| `BENTLEY_TOKEN_FILE` | `/tmp/bentley_token.txt` | bearer JWT (written by `auth`, read by `dump`, `sync`, `godump`) |
| `BENTLEY_PROFILE` | `~/.inspect_tech/bentley-profile` | Playwright browser profile holding the Bentley session |
| `BENTLEY_SECRETS_DIR` | `~/.inspect_tech` | `bentley_cookie.txt`, `bentley_cookie2.txt`, `bentley_pf.txt` |
| `BRIDGES_PUSH_HOSTS` | `mmsdev,mms` | ssh aliases `push` accepts |
| `BRIDGES_PUSH_DIR` | `/bms_fixtures` | server folder holding the file |
| `BRIDGES_PUSH_IMAGE` | `@amps` | image used for server-side DuckDB work; `@name` = the image the running container `name` was started from |
| `BRIDGES_PUSH_RESTART` | `amps,bms-sandbox` | containers restarted after the swap (first one required and checked) |
| `BRIDGES_PUSH_APP_DB` | `/app/data/bridges_all.duckdb` | the file's path inside that first container |
| `BRIDGES_REQUIRE_DB_LOG` | unset | `1` = fail a stage when `data_refresh_log` can't be written |

### 16.6 Bookkeeping

`sync`, `push`, `dump`, `extract-reads` and `spend` each write one `data_refresh_log` row:

- stage `bridges_<command>`, run label `bridges_<timestamp>`;
- `inputs`: the paths, the target and the `since` time;
- `counts`: changed and spliced bridges, per-table deletes and inserts, before
  and after row counts, delta size, server counts;
- `checks`: the shrink check, the push verify, the error on failure;
- `status`: `ok`, `dry_run` or `failed`, with the message.

These stages write the DuckDB, not PMS, and the nightly sync runs from launchd
on a laptop whose PMS tunnel may be closed. So logging is best effort: when the
PMS database can't be reached, the stage still runs and appends the same record
to `<BRIDGES_SYNC_WORK>/refresh_log.jsonl`.

`auth` and `refresh-token` only renew credentials; logging them would add 48
rows a day, so they are not logged.

### 16.7 Troubleshooting

- **Exit 2 / "Bentley sign-in needed":** run `python -m pipeline bridges auth
  login`. The session in the browser profile expired.
- **`HTTP 401` in a dump:** the token expired mid-run. `sync` refreshes it every
  40 minutes; for a long manual `dump --all`, run `auth watch` alongside it.
- **"sanity check failed, not swapping":** a table shrank by more than 3%. The
  new file is left as `bridges_all.new.duckdb` for inspection; the live file is
  unchanged.
- **The DuckDB doubled in size:** DuckDB doesn't reclaim the space deleted rows
  held. `sync` compacts after every swap; `sync --compact-only` does just that.
- **`push`: "not enough space":** the server needs about the file's size plus
  the delta plus 2 GB, counting the old `prev` copy.

Related: the saved API references are in `bridges/analysis_reference/` (see its
README). The analysis scope rule — WVDOT-owned bridges only, field 2300201 =
`S01` — is in `bridges/analysis_reference/ANALYSIS_RULES.md`.
