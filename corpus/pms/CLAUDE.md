# AMPS — WVDOT Asset Management & Performance System (PMS + Bridges + BMS)

FastAPI backend (`api/`) + Python/polars engine (`engine/`, dTIMS-derived) +
React 19 / Vite / MUI frontend (`ui/`). Postgres via `.env` (`DB_*`); SQL in
`db/schema.sql` and `db/migrations/`. The frontend builds into `api/static`
and is served under `/pms` in production.

## Running locally

`./start-dev.sh` runs everything in one terminal (Ctrl-C stops it all):
the PMS DB SSH tunnel (local port = `DB_PORT` in `.env`), the TheHub tunnel
(`ssh -N -L 1434:10.69.0.44:1433 cputest`), uvicorn with `--reload` on :8000
and Vite on :5173.

Env keys beyond `DB_*` (see `.env.example`, `ui/.env.example`):
`HUB_DB_SERVER/NAME/USER/PASS` (TheHub SQL Server, needs ODBC Driver 17),
`ROADS_DB_NAME` (database holding `operations.roads2` on the same Postgres
server, default `dot12_test`), `VITE_MAPTILER_KEY` in `ui/.env`, and the
WVDOT sign-in keys below.

## MMS (dTIMS OM) and TheHub on the bridge page

- MMS is read **only** through `api/hub_client.openquery` (TheHub connection,
  linked server `[TAMSDW]`, `OM_WVDOT.operations`) from `bridges/mms.py`.
  Read-only; always filter `ValidTo IS NULL` (OM tables are versioned);
  validate the BARS before it goes into the SQL.
- MMS cost follows the smartcar-mms DDL (`ddl_rows`: each task-day's
  transactions shared across its lines by accomplishment). Don't price MMS
  work from `PerformanceStandard` unit costs.
- The bridge page's MMS and TheHub endpoints (`/api/bridges/{bars}/mms`,
  `/api/bms/hub/bridges/{bars}/projects`, `/api/bms/hub/projects/{n}/contract`)
  are live on every call — no cache.
- The bridges table's totals are **not** live: `/api/bridges/spend` reads
  `bms.bridge_spend`, refreshed nightly by `python -m pipeline bridges spend`
  (run in-app by `bridges/spend_nightly.py`, advisory-locked across workers;
  `BRIDGE_SPEND_NIGHTLY=0` off, `BRIDGE_SPEND_REFRESH_AT` the time). The
  statewide MMS cost is `bridges/mms.SPEND_SQL`, the same allocation as
  `ddl_rows` done in OM; keep the two in step.
- **TheHub money on a bridge is split by deck area** (`bms/hub.deck_area_shares`:
  deck area ÷ the project's total; no area → the project's average; none →
  even). Every per-bridge TheHub figure (list, bridge page, project panel,
  BMS costs, committed seed, the Wizard) uses it; never show a multi-bridge
  project's total as one bridge's cost.
- AASHTOWare contracts (dates, change orders, E&C, CN phase) come only from
  `bms/awp.py` (a TheHub project is an AWP contract when `AWP_HUBDates` /
  `AWP_Dates` / `AWP_ChangeOrders` carry its `ProjectId`).

## Sign-in (WVDOT identity broker)

PMS is OIDC client `pms` of `https://ocidev.transportation.wv.gov/auth`
(fronts Entra/SAML). Code: `api/sso.py`, `api/routes/auth.py`, the
`require_sign_in` middleware in `api/main.py`, `ui/src/components/auth/AuthGate.tsx`.
Env: `SSO_ENABLED`, `SSO_DISCOVERY_URL`, `SSO_CLIENT_ID`, `SSO_CLIENT_SECRET`,
`SSO_REDIRECT_URI`, `SSO_APP_URL`, `SESSION_SECRET`, `SESSION_COOKIE_SECURE`.
Sign-in is off (API open) unless all are set.

- Registered callbacks: `https://mmsdev.transportation.wv.gov/pms/api/auth/sso/callback`
  and `http://localhost:8000/api/auth/sso/callback` (client `pms`; `/pms` on
  mmsdev is decommissioned, AMPS signs in as client `amps` at `/amps/`). The broker matches
  byte for byte; change them with `PATCH /auth/admin/clients/{client_id}`.
- Every new user is provisioned with `SSO_DEFAULT_ROLE` (currently `admin`).
  Login must never overwrite `app_users.role`.
- New `/api/*` routes are protected automatically; anything that must be
  public goes under `/api/auth/`. Browser requests to the API must send
  credentials (axios `withCredentials`; MapLibre `transformRequest`).
- Never commit the client secret or `SESSION_SECRET`; they live in `.env`
  and on mmsdev in `~/amps/env.txt`.

## Roles and run validation

- Roles live in `app_users.role` (`admin` | `district`) and
  `app_user_districts`. **Enforce them server-side**: new endpoints that read
  or change role-scoped data take `user: CurrentUser = Depends(current_user)`
  (or `Depends(require_admin)`) from `api/authz.py`, and filter with
  `user.can_see(district_code)`. The UI only mirrors these rules.
- Run validation (`api/routes/validation.py`, `api/validation/`): the plan is
  the optimizer's `project_summary` + applied `run_plan_edits` replayed by
  `seq`. **Never delete or update the content of `run_plan_edits` rows** —
  undo is a new `revert` edit. The only exception is deleting the whole run
  (they cascade), e.g. through the config run lock below. Commits write `projects` rows with
  `source_run_id`/`source_key` and must go through `_side_effects`.
- Live updates use Postgres `NOTIFY pms_run_validation` → one `LISTEN`
  thread per worker → SSE. Payloads must stay under 8 KB (send ids and let
  clients refetch for batches). Don't call blocking code while holding the
  `events._lock`, and don't touch the event loop from worker threads except via
  `loop.call_soon_threadsafe`.
- The validation page must stay fast with ~1,000 cards. Drag is a small
  custom pointer handler that writes the overlay's transform and lane
  highlight (`data-over`) directly, so React doesn't render during a drag;
  hover lives in `components/validation/hoverStore.ts`; card moves animate
  with `flip.ts` (one card), not layout animations; `Lane` is memoised, so
  pass it only stable/per-lane props. Don't add per-card drag hooks, motion
  `layout`/`layoutId`, or page-wide inline style changes (one on `body`
  restyles ~7,000 elements).

## Data pipeline (refreshing survey / LRS / joint data)

Everything that rebuilds data tables goes through `python -m pipeline`
(`pipeline/`, doc `dtims_docs/PMS_Data_Pipeline.md`). Rules:

- **Back up first**: `PYTHONPATH=. python scripts/backup_pms.py` (add `--mmsdev`
  for pms_test). It dumps, restore-rehearses, archives the replaced tables into
  `archive_<date>` and copies the file inputs to `~/pms_backups/`.
- **Schema changes only as numbered files in `db/migrations/`**, applied with
  `scripts/migrate.py --apply` (recorded in `schema_migrations`), never by hand.
- **No `DROP … CASCADE` (or DROP at all) of live tables in import code.** Build
  into `<table>_stage`, run `pipeline/checks.py`, swap with TRUNCATE + INSERT in
  one transaction (`import_pavement_data.swap_in`), so dependent views survive.
- **Geocoding (GPS → route milepoint) only through `lrs/geometry_to_measure.py`**
  on roads2 — never an external service. The HTTP face is
  `POST /api/lrs/geometryToMeasure` (dashcam-compatible; session or service
  token `LRS_SERVICE_TOKENS`, `api/service_tokens.py`).
- **Joints only from LRS layer 70** via `pipeline/joints.py` (the algorithm of
  `scripts/joint_breakdown_intersections.py`); never re-export `pavement_joints`
  as input. Loading joints must go through `load_build` (new `joint_builds` row +
  `joint_crosswalk`); runs store `configuration.joint_build_id` and validation
  translates older builds.
- **Pavement families only from a config's `pavement_family_rules`** via
  `pipeline/families.py`, written to that config's `segment_families`
  partition. Don't hard-code surface → pavement type → family mappings;
  `python -m pipeline families [--config N]` reruns the classifier (family,
  CCI, ages) in one transaction per config.
- **The BMS configuration's Excel round trip** is `bms/config_workbook.py`. It reuses the PMS
  workbook machinery (`Col` / `Sheet`, `coerce`, `_diff_sheet`, `Report`, `render_workbook`), so
  improve that machinery in one place. A new BMS config column needs a `Col` there too.
- **Config sub-tables change through the family-rules API or the Excel import**
  (`api/config_workbook.py`): validate every row first, apply only with the
  reviewed `diff_hash`, one transaction, logged in `config_imports`. A new
  config column or table needs a `Col`/`Sheet` there, or it silently isn't
  round-tripped.

## Configurations (migration 030)

- Treatments, triggers, reset operations, unit costs, sequencing, family
  curves, family rules, budget scenarios and model constants are **per config** (`config_id`, keys include it), and
  family / pavement type / CCI / ages live in `segment_families` (partition
  per config, with each segment's dTIMS starting state), read through the view
  `analysis_segments_cfg`.
  `analysis_segments` has no family columns. **Every query of these tables
  must filter `config_id`.**
- **The compiled config is the only reader of policy** (`engine/compiled.py`):
  a config compiles into one validated, hashed object (frames, route groups,
  condition policy, curve book) and every engine consumer uses it — the
  `engine/db.py` loaders return its frames. Engine code reads config tables
  only through those loaders with `config_id=` or inside
  `engine.config.use_config(config_id)` / `engine.compiled.use_compiled(cfg)`;
  they raise when no config is set (scripts: `PMS_CONFIG_ID` / `--config`).
  Threads start without one, so set it inside the thread.
- **WVDOT policy lives in config tables, not code** (migrations 035–036): route
  groups, cost adjustments, cracking rules, counters, condition initializers,
  the Hub treatment map, model constants / input policy, the rating profile.
  Don't hard-code sign codes, route numbers, factors, years or thresholds in
  engine code; add a table / column, a workbook `Sheet`/`Col`, the config check
  (`engine.compiled.validate`), the Config page Policy tab and docs.
- Runs store `analysis_runs.config_id`, `config_version` (config_versions),
  `run_spec` (engine/run_spec.py: start year, economics, overrides) and their
  starting inventory (`run_snapshots`); run-scoped reads (Validate, exports,
  run detail) replay with them (NULL config → system default). Browse pages
  use the viewer's default (`api/configs.user_config_id`). A request field
  that overrides a config value must default to None.
- **Config edits pin, never delete:** any write to a config's sub-tables goes
  through `api.configs.check_lock` / `lock_for_edit`, which refuses only while
  a run is running on the config and pins earlier runs to a stored version.
  Only deleting a config deletes its runs (`delete_runs_for_config_delete`,
  confirmed with `delete_runs`). Copy with `api.configs.copy_config` (also
  copies the partition and every policy table); delete with `delete_config`.
- Every stage writes `data_refresh_log`; conflation drops go to
  `conflation_issues`. `analysis_segments.length_miles` is `end_mp − begin_mp`.
- No credentials in code: DB settings come from `.env` via `api.database`.

## Condition model (dTIMS, v1.6)

- Condition moves through time **only** via `engine/condition/dtims_state.py`
  (anchored family curves, CCI on its own curve, holds, raw IRI / rut /
  cracking / faulting, ordered resets, MAP-21 GFP). Runs, benefits, MILP,
  Validate and the outlooks all use it; don't add another projector, and
  don't compute CCI as a minimum or classify Good / Fair / Poor from CCI.
- **GFP = the rating of the raw distress on the config's profile**
  (`gfp_profiles`, MAP21_2017), network shares by lane-miles (`classify_gfp` /
  `network_gfp`; SQL `pipeline/checks.gfp_sql`; UI `ui/src/utils/gfpProfile.ts`
  loaded from the API — no copies of the thresholds).
- Treatment effects are `treatment_reset_ops` rows (ordered; seeds in
  `engine/condition/dtims_ops.py`), gates on `treatments` /
  `treatment_triggers` (route groups, one minimum length with an optional
  branch override, `interval_years`). A new op or gate needs the engine, the
  workbook `Col`/`Sheet`, the config check, the Config page and docs.
- **Costs only through `engine/optimization/cost.price_segments` /
  `price_joint_candidates`** (per-segment pavement rate, route-group
  adjustments, default lanes, run inflation). Greedy, MILP, commitments,
  Validate and the project / segment pages use it; don't price elsewhere.
- Errors fail runs: no catch-all that returns an empty year, no running
  without triggers / ops / costs.
- MILP-assist targets are per-year rows with signed effects
  (`engine/optimization/milp/prevention.py`), solved in phases: feasibility
  (hard rows, no benefit) → hard rows + benefit, else the most years with
  % Poor met, then the most with % Good met (keeping the Poor count), then
  benefit keeping both counts. Solver
  progress (best, bound, gap, yearly shortfalls) comes from HiGHS callbacks;
  results are verified by replay.
- `tests/engine/test_dtims_state_replay.py` (saved dTIMS strategies) must
  stay within 1e-6.


## Bridges and BMS (v1.8, moved in from inspect_tech)

The bridge side of the sister app lives here too. It has three app-bar entries:
**Bridges** (`/bridges` inventory and inspections), **Brgzrd** (the Bridge
Wizard, `/bridges/wizard`) and **BMS**
(`/bms/*` planning: runs, validation, projects, committed, LISA, config).
The standalone inspect_tech `/bms` app on mmsdev was decommissioned on
2026-09-27; all bridge work lands here.

**Data**
- **The bridge inventory is the AssetWise extract** `bridges_all.duckdb`
  (`INSPECT_DB`; locally the inspect_tech copy, on mmsdev
  `/bms_fixtures/bridges_all.duckdb` mounted `:ro`).
  - Open it only through `bridges/inventory_db.db_conn()`, read-only. Never
    write it.
  - It is EAV (`asset_value` / `report_value` keyed by `field_id`), and NBI
    and SNBI use different field ids for the same concept
    (`CANONICAL_RATINGS`, `v_canonical_rating`).
  - Run `DESCRIBE` before joining or casting.
- **Planning, validation, flood3d and Wizard state live in the `bms` schema**
  of the PMS database (migrations 043–052).
  - `bms/store.py` connects with `search_path = bms, public`, so BMS SQL uses
    unqualified names that must never hit the pavement tables of the same
    name (`treatments`, `budget_scenarios`, `run_logs`, …).
  - Schema changes go through numbered migrations like everything else;
    `bms/store.py` does not self-migrate.
- **Scope is WVDOT-owned bridges** (B.CL.01 owner, `field_id = 2300201`,
  value `'S01'`) unless a page or report says otherwise.
- **Bridge districts are text** (`'01'`, `'1'`, …, `'10'`). Compare them to
  `app_user_districts` with `int(d)`.

**Domain logic stays separate from pavement**
- Bridges use NBI 0–9 ratings, LISA 0–100 (bands 75/45) and deck area in
  square feet.
- Bridge colours come only from `ui/src/bridges/ratingColors.ts` (colour means
  a condition rating).
- Bridge costs go only through `bms/cost.treatment_cost`.
- Nothing in `engine/` knows about bridges, and nothing in `bms/` uses pavement
  indices, GFP or `price_segments`.

**BMS configurations** (migration 050) follow the PMS configuration rules:
- `bms.configs` rows each pick a **model** (`amps` | `dtims`). Treatments,
  deterioration models, LISA parameters and budget scenarios (and the dTIMS
  model's tables) carry `config_id`; **every query of them filters `config_id`**.
- **`bms/compiled.py` is the only reader of BMS config content**
  (`read_tables`, `validate`, `ensure_version`, `current`); register a model's
  tables in `TABLES_BY_MODEL` / `VALIDATORS` and `bms/configs.SUB_TABLES_BY_MODEL`.
- Config writes go through `bms/configs.lock_for_edit` + `touch` (409 while a
  run is running on the config). Runs record `config_id` + `config_version`
  at creation, so edits never change a finished run.
- Endpoints take `?config_id=` (default: the user's `bms_default_config_id`,
  else the system default). The workbook is per config and per model
  (`bms/config_workbook.SHEETS_BY_MODEL`); a new config column needs a `Col`.

**The dTIMS model** (`bms/dtims/`, configs with `model = 'dtims'`, tables
`dt_*` from migration 051) reproduces Deighton's dTIMS bridge model:
- Its rules are **expressions in the config**, parsed and evaluated only by
  `bms/dtims/expr` (a registry of functions; never Python `eval`). A new
  function goes in `expr/functions.py` with docs in BMS_Business_Logic.md.
- **One simulator** (`bms/dtims/sim.BridgeSimulator`) for runs, generation,
  Validate and the outlooks (through `bms/sim`). Don't add another.
- The execution contract (slots, authored variable order, cost before resets,
  PV over slots 1..N−1) is pinned by `tests/bms/test_dtims_golden.py`, the
  12 saved dTIMS strategies; it must reproduce exactly.
- "WVDOT dTIMS BMS" (defects fixed) and "dTIMS exact (2026-09)" differ **only
  in data** (`bms/dtims/seed/fixes.yaml` → `fixed.json`). Never branch on a
  config's name; a behaviour difference is a setting or a rule row.
- Seeds are generated (`scripts/dtims_seed/translate.py`, `apply_fixes.py`)
  and loaded with `python -m bms.dtims.seed_db`.
- A run's scenario `start_year` is its first year of work; the dTIMS start
  year (slot 0) is the year before (`store.run_settings`, stored as
  `runs.config.dtims_settings`). Anything that replays a run loads its config
  with `store.with_run_settings`.
- Selection is `select.py` (benefit/cost) or `milp.py` (targets enforced,
  through `engine/optimization/milp/solver.solve_milp`).

**BMS runs and validation** follow the PMS rules above:
- Same edit log (`bms.run_plan_edits`, never deleted; undo is a `revert`
  edit).
- Commits write `bms.committed_projects` with `source_run_id`/`source_key`
  through the side-effects function.
- NOTIFY channel is `bms_run_validation`; `api/validation/events.py` takes the
  channel as a parameter.
- Runs freeze the committed projects at creation (`runs.config.committed_input`)
  and record the ones they forced (`committed_snapshot`).
- **Bridge lists** (`scenario.scope.bars`, `bms/bridge_list.py`): a run or scenario
  can plan only listed BARS (AND the class and districts). Anything that filters by
  scope (both models, `amps.bms.load_bridges`, new consumers) must honour `bars`,
  and a list is checked to be WVDOT-owned in-service bridges before a run starts.
- Writes need `require_admin`, or `current_user` + `can_see`.

**Bridge Wizard** (`bridges/wizard/`, `/api/bridge-wizard`,
`ui/src/pages/bridges/Wizard*`). Things that will bite you:
- **The SSE stream must always terminate.** Any new early return still emits
  `error` and `done`; `stream_answer` is the guard.
- **Thinking blocks are replayed unchanged, signature included.**
  `budget_tokens` is a 400 on `claude-sonnet-5`; use `output_config.effort`.
- **The model is a setting** (System → Brgzrd, `bridges/wizard/settings.py`,
  `bms.wizard_settings`; the Run Assistant has its own, System → Run Assistant):
  DeepSeek (Fireworks, the default, `low` effort), Grok (xAI on OCI Generative
  AI, `xai.grok-4.7`, `_oci_turn` via the OCI SDK: `OCI_GENAI_COMPARTMENT_ID` +
  env credentials `OCI_USER/TENANCY/FINGERPRINT/REGION/KEY_CONTENT`, a config
  file or instance principal) or Claude (Anthropic, the fallback when the
  chosen provider isn't configured or fails before starting a question).
  History is always stored in Anthropic's format; DeepSeek and Grok reasoning
  are `thinking` blocks marked `_provider: fireworks` / `oci` that must never
  reach Anthropic (`_for_anthropic` drops any marked block), and only
  Fireworks' own reasoning is replayed to Fireworks (`_to_openai`). The badge
  is DS / GK / SN-{effort} (`ModelBadge`). A new provider needs a `*_turn`
  generator with the same SSE events, a key check (`key_present`,
  `missing_key_reason`), `PRICE_KEYS`, and tests in `tests/bridges/test_wizard_admin.py`.
- **System → Brgzrd is limited to the emails in `BRGZRD_ADMINS`**
  (`api.authz.require_brgzrd_admin`), not all admins: it shows every user's
  questions. New Brgzrd admin endpoints use that dependency.
- **The system prompt is the cached prefix and must stay byte-identical.**
  Watch `cache_read_tokens` in `bms.wizard_responses`.
- **Model- or user-written SQL runs only on `bridges.db.connect_locked`** (DuckDB),
  or, for TheHub / MMS, only through `bridges/wizard/hub_mms_sql.validate`
  (read-only SELECT over the allow-lists) and `api.hub_client.hub_select`
  (always rolled back). A new table for `hub_sql` / `mms_sql` goes on the
  allow-list and into `hub_mms_schema.json` (`scripts/wizard_hub_schema.py`).
- **Model-written Python runs only in the sandbox** (`sandbox/`; the
  `bms-sandbox` container on mmsdev, no network). Never add an in-process
  fallback.
- **Charts and files are persisted in `turn_meta`**, and their bytes in
  `bms.wizard_artifacts`. A new artifact kind must be persisted too.
- **Truncation must be visible** (`run_sql` 500 rows, exports 100k).

**Refreshing bridge data** is `python -m pipeline bridges …` (AssetWise sync,
push to mmsdev). It follows the Data pipeline rules above; AssetWise
credentials come from `.env` only.

## Run Assistant (assistant/, analysis_worker/, migration 054)

An admin-only chat (the **Run Assistant** button at the top right of the app bar opens a resizable right-hand
panel) where DeepSeek or Claude plans and runs PMS / BMS studies, judges the results and saves the runs worth
keeping. Settings: System → Run Assistant (`assistant/settings.py`, `public.assistant_settings`). Docs:
`dtims_docs/Run_Assistant_Usage.md`, `dtims_docs/Run_Assistant_Logic.md`.

- **Turns run in a server thread, not the request** (`assistant/agent.start`). Everything a turn produces is an
  event row (`public.assistant_events`, seq per conversation); the panel replays and follows them over SSE
  (`GET /api/assistant/conversations/{id}/events?after=`), from any uvicorn worker. Don't stream a turn's output
  any other way, and keep new event kinds in the contract list in `Run_Assistant_Logic.md`.
- **Every turn ends with a `done` event**, on every path (error, Stop, step limit). Stop is a flag on the turn
  (`cancel_requested`) read by the heartbeat thread; a turn without a heartbeat for `STALE_S` is closed as
  `interrupted` by `store.reap_stale` (claimed by an UPDATE, so only one worker writes its events).
- **The saved history never ends in a `tool_use` without its `tool_result`** (`agent.repair_history`), and it
  follows Brgzrd's provider rules: the model calls are `bridges/wizard/brigzard._anthropic_turn` /
  `_fireworks_turn`, Fireworks reasoning never reaches Anthropic.
- **Model-written Python runs only in the analysis worker** (`assistant/worker.py` → `analysis_worker/`): the
  engine and BMS code, the `amps` helper library, the database **read-only**, no other network. Never add an
  in-process fallback. `analysis_worker/API.md` is included verbatim in the system prompt
  (`assistant/prompt.py`) — change them together.
- **Runs are saved only through the app's own create-run code** (`assistant/tools.save_pms_run` →
  `api.routes.runs.create_run`, `save_bms_run` → the POST /api/bms/runs handler) and tagged
  `configuration.assistant = {conv_id, turn_id}` (PMS) / `config.assistant` (BMS) by a JSON merge.
- The system prompt is the cached prefix: keep it byte-identical between turns. Per-question facts (today, the
  page the user is on) go in the user turn (`agent.user_turn_text`).
- One running turn per conversation and per user (`store.start_turn` → 409). Years are plain calendar years
  ("2026"), never "FY".

## Docs — MANDATORY when behavior changes

The help pages are markdown files in `dtims_docs/`, served by
`api/routes/docs.py` (whitelist `ALLOWED_DOCS`) and rendered by
`ui/src/pages/DocPage.tsx`:

- `dtims_docs/PMS_Usage.md` → `/docs/PMS_Usage`: user-facing usage guide,
  one section per screen.
- `dtims_docs/PMS_Business_Logic.md` → `/docs/PMS_Business_Logic`: internal
  business-logic reference (data model, condition, treatments, optimizer,
  projects, integrations, assumptions).
- `dtims_docs/AMPS_Overview.md` → `/docs/AMPS_Overview`: the one-page "what AMPS is and what
  it's for", opened by the app-bar logo: the folders, Bridges and Brgzrd explained, the planning
  cycle (ASCII diagram) and why validation replaced the spreadsheet-and-meetings round. Keep it an
  overview, not a manual, and true to the app (figures, folders, workflow) when those change.
- `dtims_docs/BMS_Usage.md`, `dtims_docs/BMS_Business_Logic.md` and
  `dtims_docs/Bridge_Wizard_Logic.md` are the same pair (plus the Wizard
  reference) for the Bridges and BMS pages. Bridge changes update these, not
  the PMS ones.
- The Changelog page (`/changelog`) renders `ui/src/data/changelog.ts`
  directly; it has no markdown source.

These are at the top of the **Documents** menu in the app bar
(`HELP_ITEMS` in `ui/src/layouts/AppLayout.tsx`). The bridge analysis
reports (`dtims_docs/Bridges_*.md`) sit in its "Bridges" sub-group.

Whenever a change touches:

- **User-visible workflow or UI** (pages, dialogs, filters, columns, exports,
  navigation, shortcuts) → update `PMS_Usage.md` in the same change so the
  help text matches the app.
- **Business logic, data model, calculations, thresholds, optimizer
  behaviour or integrations** (TheHub, roads2, nexuslrs, lrsops) → update
  `PMS_Business_Logic.md` in the same change. If a deeper technical doc
  in `dtims_docs/` covers the topic (e.g. `WVDOT_PMS_Optimization_Logic.md`),
  update that too.

If a change touches both, update both. This is not optional: if a doc
section is no longer accurate after your change, fix it (or note that it was
removed). Don't leave stale information.

Links between docs use in-app paths (`/docs/<slug>`, `/changelog`); DocPage
routes them through react-router so the `/pms` prefix is applied in
production. A new doc needs its slug in `ALLOWED_DOCS` **and** a nav entry in
`AppLayout.tsx`.

## Changelog — MANDATORY on every commit

When committing, update `ui/src/data/changelog.ts`:

1. Add an entry to the FRONT of `releaseChangelog` (`version`, `date`,
   `title`, `changes: [{ type, description }]`, where type is `added`,
   `changed`, `fixed` or `removed`). Operator-facing: name endpoints,
   tables/migrations, env vars and deploy changes.
2. Bump the version (default: patch `x.y.Z`, unless the user says otherwise)
   in **all four** places, kept identical:
   - `FRONTEND_VERSION` and `BACKEND_VERSION` in `changelog.ts`
   - `BACKEND_VERSION` in `api/main.py` (also returned by `GET /health`)
   - `"version"` in `ui/package.json`
3. Update `summaryChangelog`: one entry **per calendar day**, plain
   pavement-engineer language (what it means for them, not how it was
   built), **max 6 bullets**. If today already has an entry, fold your change
   into it; otherwise add a new one at the FRONT.

Both logs are visible to every signed-in user. Don't put
credentials, hostnames of internal services beyond what's already there, or
personal data in either log.

**Commit grouping:** if several uncommitted changelog entries or other
accumulated work are in the working tree when asked to commit, bundle them
into one commit. Stage only the files that belong to the work: the repo root
has many unrelated scratch files (xlsx/csv exports, notes) that must not be
committed.

## UI style

- **The app is called AMPS** (Asset Management & Performance System, for WVDOT's Asset
  Management & Performance division). PMS, BMS and Bridges are its folders.
  - The logo is the arch-bridge mark: `components/brand/AmpsMark.tsx`,
    `ui/public/amps.svg` (favicon), `ui/public/amps-logo.svg`.
  - Tab titles are `<page> · AMPS` (`usePageTitle`).
  - The Bridge Wizard's brand is **brgzrd** (logo concept 4, "badge"):
    `components/brand/BrgzrdMark.tsx` (`BrgzrdMark`, and `BrgzrdWordmark` —
    heavy lowercase with a gold "z"), `ui/public/brgzrd.svg`. The concepts
    it was chosen from are in `design/brgzrd-logo/`.
- **The look is plain MUI**: the blue `#0b6bcb` app bar, pages on `#f5f6f8`.
  There is **no hamburger or drawer**.
  - `AppLayout.tsx` puts every folder in the bar as a hover (or click) menu,
    in this order: PMS, BMS, Bridges, Brgzrd, Documents, System. Bridges
    (`/bridges`) and Brgzrd (the Bridge Wizard, `/bridges/wizard`) are plain
    links (`link` on the category), not menus. Documents' sub-folders fly
    out to the right.
  - A new page needs its entry in `CATEGORIES` there (and a folder
    `prefixes` entry if its path is new).
  - Users lives under **System**, with Profile.
- **Avatars follow the dot12 pattern**: initials (`utils/avatar.ts`,
  `components/UserAvatar.tsx`) on the colour each user picks on
  `/profile` (`app_users.avatar_color`).
  - The avatar is used in the app bar, on Users and on the Validate presence
    avatars.
  - Don't add another initials or colour helper.
- A DOT-12-style restyle of the page content was tried and rejected (it is
  kept in `git stash`). Don't restyle pages or the app shell unless asked.

## Deploying to mmsdev

**AMPS (this repo, v1.8+) is `~/amps` → the `amps` container on port 6100,
served at https://mmsdev.transportation.wv.gov/amps/** (OIDC client `amps`,
`SESSION_COOKIE_NAME=amps_session`, `VITE_BASE_PATH=/amps/`, database
`pms_test`). The Dockerfile clones from GitHub, so **push first**, then:

```sh
ssh mmsdev 'cd ~/amps && ./build.sh --branch engine'
```

- **The standalone `pms` (`/pms`, :6000) and `bms` (`/bms`, :6969) apps on
  mmsdev were decommissioned on 2026-09-27.** Their containers and images are
  gone, Apache no longer proxies `/pms` or `/bms`, and `~/pms/build.sh` /
  `~/bms/build.sh` are stubs that refuse to run (see `DECOMMISSIONED` in each
  folder). Don't rebuild, push to or re-proxy them; AMPS replaces both. The
  `bms-sandbox` container stays: it is AMPS's Bridge Wizard sandbox.
- `~/amps/build.sh` uses the shared `~/ops/build-lib.sh`: build a candidate
  image, stop the old container (kept as `amps-rollback-<ts>`), start the new
  one and health-gate it on `http://127.0.0.1:6100/health`. A failed gate
  rolls back automatically.
- The container runs with `--network host` (like `~/dot12`) so it can reach
  the TheHub tunnel on `127.0.0.1:11433`. Apache proxies `/amps` →
  `127.0.0.1:6100`.
- Runtime config is `~/amps/env.txt` (passed with `--env-file`, never baked
  into the image). `VITE_MAPTILER_KEY` in `env.txt` is passed as a build arg.
- The server Dockerfile installs Microsoft ODBC Driver 17 (same block as
  `~/dot12/Dockerfile`) for pyodbc.
- mmsdev (VM.Standard.E5.Flex, 4 OCPU / 16 GB, 150 GB boot volume, the same
  as mms): keep an eye on disk; clear old images / build cache before big
  builds or pushes.
- **Bridges need three mounts and a few env keys**, in `~/amps/build.sh`
  `RUN_ARGS` and `env.txt`:
  - Mounts:
    - `-v /bms_fixtures/bridges_all.duckdb:/app/data/bridges_all.duckdb:ro`
      (the inventory; never copy it). `python -m pipeline bridges push mmsdev`
      updates it and restarts `amps` and `bms-sandbox`;
    - `-v /bms_sandbox:/run/bms-sandbox` (the running `bms-sandbox` Wizard
      sidecar's socket);
    - a persistent `FLOOD3D_DATA_DIR` (`/amps_data/flood3d`).
  - `env.txt` keys: `INSPECT_DB=/app/data/bridges_all.duckdb`,
    `BRIGZARD_SANDBOX=socket:/run/bms-sandbox/sandbox.sock`,
    `ANTHROPIC_API_KEY`, `FLOOD3D_DATA_DIR`.
  - After a deploy that adds migrations, run `scripts/migrate.py --apply`
    in the container (`docker exec -w /app amps sh -c "PYTHONPATH=. python scripts/migrate.py --apply"`).
