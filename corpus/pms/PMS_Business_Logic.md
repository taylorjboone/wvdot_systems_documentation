# PMS — Business Logic

Internal reference for how the WVDOT Pavement Management System (the PMS part of **AMPS**, Asset Management & Performance System) turns survey data into condition, picks treatments and builds a work program. It describes what the **code does today**. Where the code and older docs disagree, the code wins, and the disagreement is listed under [Known gaps and discrepancies](#12-known-gaps-and-discrepancies).

The document follows the system in the order data flows: an end-to-end overview (1), the data model (2), how data gets in (3), the rules and parameters (4), how condition works (5–7), how the work program is chosen (8), and what happens to the plan afterwards (9–11). For how to use the screens, see the [Usage Guide](/docs/PMS_Usage); the [Data Pipeline](/docs/PMS_Data_Pipeline) and Optimization Logic pages go deeper on their topics.

## Contents

1. [How AMPS PMS works, end to end](#1-how-amps-pms-works-end-to-end)
2. [Data model](#2-data-model)
3. [Ingestion pipeline](#3-ingestion-pipeline)
4. [Configurations and engine parameters](#4-configurations-and-engine-parameters)
5. [Condition model](#5-condition-model)
6. [Treatments](#6-treatments)
7. [Benefits and cost](#7-benefits-and-cost)
8. [Optimization engine](#8-optimization-engine)
9. [Projects and commitments](#9-projects-and-commitments)
   - [9a. Run validation](#9a-run-validation)
10. [Potential projects](#10-potential-projects)
11. [Integrations](#11-integrations) (including sign-in)
12. [Known gaps and discrepancies](#12-known-gaps-and-discrepancies)

---

## 1. How AMPS PMS works, end to end

AMPS PMS answers one question: **given the road network as surveyed, a set of engineering rules and a question (a budget, or a condition target), which treatment goes on which road in which year, and what condition follows?** Everything in this document is a part of that answer. This section walks through the whole system once, in the order data flows; the later sections describe each part in full.

### 1.1 The five parts

| # | Part | What it is | Where it lives | Section |
|---|---|---|---|---|
| 1 | **Ingestion pipeline** | Turns the vendor's yearly survey files and the LRS into the network: 0.1-mile analysis segments with condition and traffic, grouped into joints (potential projects) | `python -m pipeline` (`pipeline/`, `scripts/import_pavement_data.py`); tables `reconflate_normalized`, `analysis_segments`, `pavement_joints` | [3](#3-ingestion-pipeline) |
| 2 | **Configuration** | The engineering rules and every engine parameter: families and curves, treatments with triggers / resets / costs / sequencing, route groups, cracking, initializers, rating profile, model constants | `configs` and its sub-tables; compiled by `engine/compiled.py`; edited through the Config page and its Excel round trip | [4](#4-configurations-and-engine-parameters) |
| 3 | **Condition model** | How a segment's condition starts (from the survey and the config) and moves through time, with and without treatment; how it is rated Good / Fair / Poor | `engine/condition/dtims_state.py` (the one condition model) | [5](#5-condition-model), [6](#6-treatments), [7](#7-benefits-and-cost) |
| 4 | **Optimization engine** | Chooses the work program: greedy incremental benefit / cost under yearly budgets, or MILP-assist to meet condition targets (most benefit, or least cost) | `api/routes/runs.py` → `engine/optimization/` | [8](#8-optimization-engine) |
| 5 | **Validation and projects** | Where people review, move and commit the plan; committed projects are locked into every later run | `api/validation/`, `projects` | [9](#9-projects-and-commitments) |

### 1.2 The cycle

<div class="diagram">

```text
  (every so often: new LRS or survey year)                                (changes rarely: admins edit or copy it)
+==============================================+                        +==============================================+
| [1] DATA REFRESH  -  the road network        |                        | [2] CONFIG  -  the engineering rules         |
+----------------------------------------------+                        +----------------------------------------------+
|                                              |                        |                                              |
| LRS routes, traffic and districts            |  the network           | TREATMENTS    what can be done and its cost  |
|   + the vendor's yearly condition survey     |----------------------->|   triggers    when a treatment fits          |
|   = 0.1-mile analysis segments with          |                        |   resets      what it does to the road       |
|     condition and traffic (plus LRS road     |                        | FAMILIES      how each kind of road ages     |
|     the survey missed, flagged unsurveyed)   |                        | FAMILY RULES  which family a road is in      |
|                                              |                        | CONSTANTS     economics, input policy        |
| PAVEMENT JOINTS: each route's pavement       |                        | BUDGETS       saved budget scenarios         |
| cut at its major crossing routes             |                        |                                              |
| (termini) = the potential project            |                        | Editing the rules or curves reruns only      |
| segments; a project treats whole joints.     |                        | the family step below, never the data.       |
+==============================================+                        +==============================================+
                                     \  after a refresh       after a rules or curve  /         |
                                      \  (every config)      edit (that config only) /          |
                                       v                                           v            |
                                   +================================================+           |
                                   | FAMILY STEP  -  runs on its own, in seconds    |           |
                                   +------------------------------------------------+           |
                                   | the config's family rules sort every segment   |-----------+
                                   | into a family, with its starting condition     |           |
                                   +================================================+           |
                                                                                                |  picked in New Run
                                                                                                v
+==============================================+                        +==============================================+
| [4] VALIDATE  -  the work plan, together     |                        | [3] RUN  -  optimize several years of work   |
+----------------------------------------------+                        +----------------------------------------------+
|                                              |      the PMS cycle     |                                              |
| Projects as cards, one lane per year.        |                        | You choose: the roads, the budget per        |
| Easy edits: move a year, remove, add,        |                        | year, or condition targets, the optimizer.   |
| change treatment; lane totals update.        |  the work plan         |                                              |
|                                              |<-----------------------| Greedy: each year roads age, treatments      |
| Every change is logged: who, why,            |                        | that fit compete, the best condition gain    |
| before -> after; everyone sees it live.      |                        | per dollar wins until the budget runs out.   |
| District users propose, admins approve.      |                        | MILP-assist: the plan that meets the         |
|                                              |                        | targets with the most benefit / least cost.  |
| COMMIT turns a card into a committed         |                        |                                              |
| project.                                     |                        | Produces: which treatment, where, in which   |
+==============================================+                        | year, and the condition that results.        |
                        |                                               +==============================================+
                        |           committed projects are locked into every later run          ^
                        +-----------------------------------------------------------------------+
```

</div>

### 1.3 One pass through the system

1. **Survey data arrives.** The vendor delivers one file per survey year (`<YYYY>.csv`): ~0.1-mile records with GPS, the vendor's route and milepoints, raw distress (IRI, rutting, faulting, two cracking measures) and indices (PSI, RDI, SCI, ECI, JCI, CSI, CCI, NCI). The LRS (roads2 and the R&H event layers) supplies routes, milepoints, traffic, district, county, Federal Aid, functional class and the pavement events that become joints.
2. **The pipeline builds the network** (section 3). Each record is placed on the LRS — by its GPS (conflated mode, `reconflate_normalized`) or on its own route and milepoints (raw mode, `reconflate_raw`); both can be kept, as two survey networks side by side, and each config reads one. Stage E lays a 0.1-mile grid on the LRS, keeps the newest survey per cell, adds unsurveyed LRS road on the state-system signs, splits the grid at joint and LRS-attribute boundaries and stores the result in `analysis_segments`. Stage E1 attaches the dTIMS inputs (vendor CCI and indices, rehab years, ADT growth, Federal Aid / NHS). Every stage is checked and swapped in atomically; every run of it is logged.
3. **Each config classifies the network** (the family step, sections 4–5). The config's family rules put every segment in a family (pavement type × rehab type × truck load) and compute its starting condition at the config's start year: projected indices, CCI, ages, raw distress, its MAP-21 rating. This is stored per config in `segment_families` and read, joined to the network, through `analysis_segments_cfg`.
4. **Someone asks a question** (a run, section 8): which roads (`segment_filter`), which config, which start year and horizon, and either budgets per year (greedy) or condition targets (MILP-assist), plus optional constraints. The run pins its config version and run spec, snapshots its starting inventory and loads the segments (unsurveyed road only if the config includes it).
5. **The engine simulates and chooses.** Segments are grouped into joints. Every year the condition model ages every segment (section 5); every treatment whose triggers and gates pass on a joint's segments becomes a candidate (section 6), with a benefit (condition gained over the horizon, traffic-weighted) and a cost (section 7). Greedy picks, year by year, the best incremental benefit per dollar until the year's budget is spent; MILP-assist chooses over all years at once to meet the targets. Chosen treatments reset the treated segments' condition, which then deteriorates on the new family's curves.
6. **The result is stored and verified.** The work program (projects by year and treatment), the yearly network condition (% Good / Fair / Poor by lane-miles) and costs go into `analysis_runs.result_summary`. MILP plans are replayed through the condition model and every target is re-checked on the replay.
7. **People work the plan** (section 9). Validate shows the projects by year; edits are logged, never deleted; commits write `projects`, which every later run forces in its year.

### 1.4 Principles the code keeps

- **One condition model.** Runs, benefits, MILP effects, Validate, exports and the outlooks all move condition through `dtims_state`; it reproduces saved dTIMS strategies to 1e-6.
- **One reader of policy.** Engine code reads config content only through the compiled config; runs record the version they used, so editing a config never changes a finished run.
- **One pricing function.** Every cost goes through `engine/optimization/cost.price_segments` / `price_joint_candidates`.
- **Policy in config tables, not code.** Route groups, factors, thresholds, rates and curves are config rows with a workbook sheet, a config check and a Config-page view.
- **Nothing silently falls back.** A run without triggers, resets or rates fails; the config check fails runs with the reasons; data stages stop on a failed check.
- **Data rebuilds are guarded.** Back up, build into a stage table, check, swap in one transaction; schema only through numbered migrations.

### 1.5 Terms used throughout

| Term | Meaning |
|---|---|
| **Segment** | One row of `analysis_segments`: an LRS piece of at most 0.1 mi with one condition and one set of attributes. The unit of condition. |
| **Joint** | A potential project: a route's pavement cut at its major crossing routes (`pavement_joints`, LRS layer 70). The unit of decision; a treatment applies to the whole joint. |
| **Survey mode** | How stage C places vendor records on the LRS: *conflated* (by GPS, re-weighted) or *raw* (on the vendor's route and milepoints, as dTIMS reads the file). |
| **Unsurveyed road** | LRS road on sign systems 1, 2, 3, 4, 7, 8 that the survey doesn't cover (`has_survey` FALSE). In runs only when the config's `unsurveyed_policy` is `dtims_defaults`. |
| **Config / version** | A complete set of rules and parameters; a version is an immutable snapshot of its compiled content that runs point at. |
| **Family** | Pavement type (BC asphalt, RC concrete, OT other) × rehab type (Initial, Minor, Major) × truck load (H, L); each has a curve per index. |
| **Program year** | Year 1 = the run's start year (a calendar year). Year 1 is the starting state; later years deteriorate one step first. |
| **MAP-21 / GFP** | The federal Good / Fair / Poor rating of raw distress (IRI, cracking, rutting or faulting); network shares are by lane-miles. |
| **CCI** | Composite condition index (0–5); its own curve; the benefit is measured on it. |
| **IBC** | Incremental benefit / cost: the greedy optimizer's selection rule. |
| **MILP-assist** | The mixed-integer optimizer (HiGHS) that meets condition targets exactly and verifies by replay. |
| **Pair** | A MILP candidate of two treatments on one joint (a first treatment and a re-treatment when it loses Good). |

---

## 2. Data model

**Route IDs** are 13 characters:

| Positions | Meaning |
|---|---|
| 1–2 | county code |
| 3 | sign system (1 Interstate, 2 US, 3 WV, 4 County, 0 MNS, 6 State Park, 7 FANS, 8 HARP) |
| 4–7 | route number |
| 8–9 | sub-route |
| 10–11 | supplemental |
| 12–13 | direction (`00`, EB, WB, NB, SB) |

Example: `01200330000EB`. Ramps use 17-character IDs. Milepoints are BMP/EMP along the route.

| Table | One row is… | Notes |
|---|---|---|
| `condition_history` | one raw 0.1-mi vendor record for one survey year | Vendor indices and raw IRI/rut/crack/faulting; −1 is stored as NULL; the survey year comes from the file name. |
| `reconflate_normalized` | one segment-year, geocoded onto LRS milepoints | Geocoded on roads2 (`lrs.geometry_to_measure`); length-weighted averages. Failed geocodes and dropped routes are recorded in `conflation_issues`. The source of the **conflated** survey network. See [the pipeline doc](/docs/PMS_Data_Pipeline). |
| `dtims_reference_*` (migration 061) | one dTIMS reference run / network | What AMPS needs to compare with and recreate the dTIMS scenario exports in `dtims_docs/`, loaded by `scripts/dtims_audit/store_reference_runs.py` (idempotent per run): `dtims_reference_runs` (settings, horizon, economics; the pavement run's curves and reset operations), `_budgets` (year × category), `_program` (element, year, treatment, cost), `_results` (yearly Good / Fair / Poor, spend, average condition, long form), `_strategies` (the pavement run's 5,700 selected strategies with PV benefit and cost), `_networks` / `_network_elements` (the dTIMS pavement analysis network, 29,427 sections with the fields the model reads; the bridge exports hold no network) and `_run_elements` (each run's subset: `analysis`, or a bridge run's treated bridges as `program`). Runs: DEL_STIP_2026 Non-NHS steady state (pms); the 70 Percent Good Analysis's (2026-09-24) Interstates only, NHS non-Interstate and NHS non-Interstate without committed work (pms: budgets, program, spend, average CCI and dTIMS's CCI categories, and the analysis set evaluated from its DEL_INTERSTATES / DEL_NHS filter, 446.09 / 1,410.62 mi = dTIMS's total measure; they share the stored network, to which the 2026-09-30 export adds each section's From / To milepoints and lane counts); BMS 2026 TAMP vetted run and +50 % (bms), BMS_Unlimited (settings only; dTIMS returned no results). Views: `dtims_reference_run_sections` (each run's sections with route, milepoints, lanes) and `dtims_reference_run_roads` (one row per AMPS route a section covers: its own and, on an EB / NB route, the opposite direction, for the segment filter that plans dTIMS's network; migrations 063, 065, 066). |
| `reconflate_raw` | one survey record as delivered | Stage C raw mode (`--survey-mode raw`, `pipeline/raw_survey.py`, migration 057): each record on the vendor's `ROUTEID` + `BEG_MP`/`END_MP` with its values as delivered (optionally only the newest file); same columns as `reconflate_normalized`; records off roads2, outside the route or of zero length go to `conflation_issues` (`raw_` reasons). The source of the **raw** survey network; coexists with the conflated one. |
| `analysis_segments` | one LRS piece of at most 0.1 mi, **the engine's input** | `length_miles = end_mp − begin_mp`; `survey_year` of its condition; `joint_build_id`. Latest condition (PSI…CSI, raw IRI/rut/crack/faulting), `current_age`, `joint_id`, district, county, NHS, functional class, AADT (including single/combination trucks), `truck_pct`, coal section, commitment flags. Family, pavement type, CCI and index ages are per config, in `segment_families`. |
| `configs` | one configuration | `name`, `comments`, `created_by(_name)`, `created_at`, `updated_at`, `updated_by_name`, `copied_from`, `is_system_default` (exactly one). Owns its treatments, triggers, resets, sequencing, family curves, family rules and budget scenarios (each has `config_id`, keys include it) and its `segment_families` partition. See [Configurations](#4-configurations-and-engine-parameters). |
| `segment_families` | one analysis segment in one config | `family_id`, `pavement_type` (BC asphalt / RC concrete / OT other), `rehab_type`, `truck_load`, `current_cci`, `age_psi … age_csi`, from that config's [family rules](#5-condition-model) and curves. LIST-partitioned by `config_id` (`segment_families_c<id>`). The view `analysis_segments_cfg` joins it to `analysis_segments` (with `config_id`); the engine and pages read that view. |
| `treatment_catalog` | one treatment id used by any config | Global foreign-key target for `projects`, `optimization_results` and legacy tables (treatments themselves are per config). |
| `pavement_joints` | one treatable project unit | The current joint build (`joint_builds`; older builds in `joint_builds_archive`, mapped by `joint_crosswalk`). The optimizer selects joints; segments without a `joint_id` are never treated. |
| `pavement_families` | one family × index curve of a config | `(config_id, family_id, index_type)` → C1 (`alpha`), C2 (`beta`), C3, curve type, initial value. |
| `pavement_family_rules` | one classification rule of a config | `priority` (unique per config), `family_id`, `match` (all/any), `conditions` (JSON, with any/all groups), `enabled`, `description`, `updated_by`. Decides each segment's starting family in that config. |
| `config_imports` | one applied Excel import | `config_id`, `applied_by`, `file_name`, `file_sha256`, `exported_at`, `diff_hash`, per-sheet `summary`, full `changes`, `reclassify_refresh_id` (migrations 028, 030). |
| `config_run_deletions` | one set of runs deleted with the config they used | `deleted_by`, `config_id`, `config_name`, `reason`, `runs` (JSON list). Only deleting a config deletes runs (since v1.7). |
| `config_versions` | one immutable snapshot of a config's compiled content | `(config_id, version)`, `content_hash`, `snapshot` (every table a run reads, JSON), `created_by_name`, `note`. Runs point at the version they used; `configs.current_version` is the latest (migration 037). |
| `treatments` | one treatment of a config | Key `(config_id, treatment_id)`. Display cost per lane-mile, same-treatment interval (`interval_years`), minimum joint length, required / excluded route group, ADT and lane limits, committed-only, wait after any treatment, life, order (severity), applicable pavement type. |
| `treatment_triggers` | one trigger branch of a treatment | Index windows `[lower, upper]` for PSI, RDI, SCI, CSI, ECI, JCI, optional CCI window, pavement type, branch kind (window / years-since), counter limit and an optional `min_length_override` (blank = the treatment's minimum length). |
| `treatment_reset_ops` | one ordered step of a treatment's reset | See [section 6](#6-treatments). Replaced `treatment_resets` (kept read-only as `treatment_resets_legacy_v15`). |
| `treatment_costs` | $/lane-mile per treatment and pavement type (BC, RC, OT) | dTIMS statewide rates; every active treatment needs all three. |
| `treatment_cost_adjustments` | a rate multiplier for a treatment on a route group | dTIMS: thick overlay × 1.2 on `INTERSTATE`. |
| `route_groups`, `route_group_terms` | a named set of roads of a config, and its terms | `match` all / any; terms `field op value` (optionally negated) or `in_group`. See [Policy](#46-parameter-reference). |
| `cracking_rules` | one cracking-progression rule of a config | First matching route group wins; a rule without a group is the default. |
| `treatment_counters` | one counter a config's resets and triggers may use | `cnt_chip`, `cnt_micro`. |
| `condition_initializers` | one dTIMS index initializer | per index group (asphalt / concrete) and rehab type: fresh value and drift a, b, c. |
| `project_treatment_map` | a Hub project treatment code → config treatment | For project history codes that aren't config treatment ids. |
| `gfp_profiles`, `gfp_profile_thresholds` | a named, versioned Good / Fair / Poor profile | Read-only system profiles; `MAP21_2017`. A config picks one (`configs.gfp_profile_key`). |
| `treatment_sequencing` | one allowed "previous → next" treatment pair of a config | `__NONE__` = never treated. dTIMS's allowed-subsequent lists (migration 033), including a treatment following itself; every run applies it. |
| `projects` | one real project, or one TheHub route segment for imported history | See [section 9](#9-projects-and-commitments). |
| `analysis_runs`, `run_logs` | one run started from the app, and its log lines | `config_id` / `config_version` are the config and version the run used (NULL `config_id`: before configs, read with the system default); `run_spec` the resolved start year, economics, rating profile and overrides; the run request is in `configuration` (with `config_id`, `config_name_snapshot`); the whole work program is in `result_summary` (JSON). |
| `run_snapshots` | one run's starting inventory | The analysed segments' inventory columns at the start (Parquet), so Validate replays the run exactly after a refresh (v1.7+). |
| `budget_scenarios` | one saved budget setup of a config | Budget, years, per-year budgets, carryover, district balancing; active names unique per config; archived rather than deleted. |
| `multi_year_segment_analysis`, `multi_year_condition_analysis` | one 0.1-mi cell with 2020–2025 values | Materialized views over conflated and raw data, with `project_id_YYYY` from CLOSED projects. |
| `potential_projects` | one detected unrecorded paving span | Rebuilt by `scripts/find_potential_projects.py`. |

Older `optimization_*` and `work_program_projects` tables are written only by the CLI script `scripts/run_optimization.py` and by legacy routes. Runs started from the app use `analysis_runs`. The old `segments`/`routes` tables are legacy and aren't read by the engine.

**How `analysis_segments`, the joints and `segment_families` are built**, stage by stage, is [section 3](#3-ingestion-pipeline); what a configuration owns and how it is versioned is [section 4](#4-configurations-and-engine-parameters).

---

## 3. Ingestion pipeline

This section describes how pavement data gets into AMPS: how the vendor's yearly condition survey and the WVDOT
LRS become the tables that runs, Validate and the browse pages read. It covers the pavement stages of
`python -m pipeline`. The bridge inventory has its own pipeline (`python -m pipeline bridges …`, `pipeline/bridges/`),
which writes `bridges_all.duckdb` and not these tables. It is covered in the BMS documents.

Code map:

| Piece | Where |
|---|---|
| Stage runner, command line | `pipeline/__main__.py`, `pipeline/stages.py` (`STAGES`, `ORDER`, `SEQUENCE`) |
| Refresh bookkeeping | `pipeline/refresh.py` (`Refresh`, `Refresh.stage`, `file_info`, `CheckFailed`) |
| Checks | `pipeline/checks.py`, `pipeline/raw_survey.raw_placement_checks` |
| Survey load, re-weighting, segment build | `scripts/import_pavement_data.py` (`phase1_condition_history`, `phase2_reconflate`, `phase3_analysis_segments`, `swap_in`) |
| Geocoding and cleaning (stage C) | `pipeline/conflate.py` on `lrs/geometry_to_measure.py` |
| Survey as delivered (stage C raw mode) | `pipeline/raw_survey.py` |
| Joints (stage D) | `pipeline/joints.py` |
| dTIMS inventory inputs (stage E1) | `pipeline/dtims_inputs.py` |
| Pavement families and starting state (stage E2) | `pipeline/families.py` |
| Committed flags (stage F) | `scripts/populate_committed_flags.py` |
| Potential projects (stage G) | `scripts/find_potential_projects.py` |
| Backups | `scripts/backup_pms.py` |
| Migrations | `scripts/migrate.py`, `db/migrations/` |
| roads2 connection and fingerprint | `lrs/db.py` (`lrs_engine`, `roads2_fingerprint`) |

### 3.1 Purpose and the shape of the flow

The pipeline turns four kinds of input into the network the engine runs on: the vendor survey files, the LRS
attribute and surface layers from the WVDOT R&H service, the roads2 LRS geometry, and the `projects` table. It is
one command with stages in a fixed order. Every stage can be run again on its own, and every stage is logged.

```text
 INPUTS                                  STAGE  (python -m pipeline <stage>)             OUTPUT
 ──────────────────────────────────      ─────────────────────────────────────────       ─────────────────────────────
 WVDOT R&H service (lrsops rhoverlay) ─► A  lrs        layers 2 12 15 18 22 35 49 77,  ─► refresh/<run>/ lrs_table.csv,
 intersections.sqlite, roads2              layer 70, intersections, roads2 print       <layer>.csv, 70.csv, …
 vendor <YYYY>.csv ────────────────────► B  survey     one survey year at a time       ─► condition_history
 vendor <YYYY>.csv + roads2 (+ 22.csv) ► C  conflate   GPS → LRS milepoints, re-weight ─► reconflate_normalized
                                           (or --survey-mode raw: as delivered)          conflation_issues
 70.csv + intersections.sqlite + 2.csv ► D  joints     merge, split long sections      ─► pavement_joints, joint_builds,
 `routes` table (route filter)                         at the highest-AADT termini       joint_builds_archive, joint_crosswalk
 reconflate_normalized + roads2 ───────► E  segments   0.1-mi grid + unsurveyed fill,  ─► analysis_segments
 pavement_joints + lrs_table.csv                       lrsops overlay, checks, swap
 2.csv + 22.csv + projects (CLOSED) ───► E1 inputs     dTIMS inventory facts           ─► analysis_segments (columns)
 each config's rules and policy ───────► E2 families   family + starting state         ─► segment_families_c<config>
 projects (planned … in_progress) ─────► F  commitments                                ─► analysis_segments.is_committed …
 condition_history, reconflate_… ──────► G  derived    multi-year views, detection     ─► multi_year_*, potential_projects

 every stage ─► data_refresh_log (inputs + sha256, roads2 fingerprint, counts, checks, status)

 How C and E replace live data:
   build <table>_stage ─► checks ─► pass: BEGIN; TRUNCATE <table> RESTART IDENTITY; INSERT … SELECT FROM <table>_stage; COMMIT
                                └─► fail: stop; the live table is unchanged (soft checks can be accepted with --accept)
```

`all` runs A, B, C, D, E, F, G (`ORDER`). E1 (`inputs`) and E2 (`families`) are not in `all` on their own; stage E runs
both after its swap. Named stages always run in pipeline order (`SEQUENCE`: lrs, survey, conflate, joints, segments,
inputs, families, commitments, derived), whatever order they are given in. If `all` is among the names, the other
names are ignored.

#### 3.1.1 The refresh folder

`--refresh-dir` (default `refresh/<YYYY-MM-DD_HHMM>` in the repo, created on start) holds everything one refresh
downloaded and produced: the LRS layer files, `70.csv`, `intersections.sqlite`, `pavement_joints_lrs_breakdown.csv`
(stage D), and stage E's working files `segments_base.csv`, `pavement_joints_lrs.csv`, `segment_overlay_ops.json` and
`segment_overlay_output.csv`. The folder's name is the refresh's label (`data_refresh_log.run_label`). `refresh/` is
git-ignored. Keep a folder until its refresh has been reviewed.

Which stage reads which file from where:

| File | Read by | If it isn't in the refresh folder |
|---|---|---|
| `lrs_table.csv` | E (overlay op 2) | E fails: "run stage A (lrs) first" |
| `70.csv`, `intersections.sqlite`, `2.csv` | D | D fails |
| `2.csv` (AADT, growth) | E1 | the repo root's `2.csv` (`stages._layer_file`) |
| `22.csv` (Federal Aid) | C (NHS gap fill), E1 | the repo root's `22.csv`; without either, C skips the NHS gap fill and E1 keeps the overlay's `fed_aid_code` |

So `python -m pipeline inputs families` works without a refresh folder, but `segments` and `joints` need
`--refresh-dir` pointing at a folder where stage A ran.

#### 3.1.2 `data_refresh_log`

`Refresh.stage` inserts one row per stage when the stage starts (`status = 'running'`, committed at once) and
updates it when the stage ends. Migration 026 created the table.

| Column | Meaning |
|---|---|
| `refresh_id` | serial; also written to `conflation_issues.refresh_id` |
| `run_label` | the refresh folder's name (families reruns from the app use their own labels, e.g. `config 1 import:…`) |
| `stage` | `A_lrs`, `B_survey`, `C_conflate`, `D_joints`, `E_segments`, `E1_inputs`, `E2_families`, `F_commitments`, `G_derived` (the bridge pipeline's `bridges_*` rows share the table) |
| `started_at`, `finished_at` | times |
| `status` | `running`, `ok`, `failed`, `dry_run`. A process killed mid-stage leaves `running`. |
| `inputs` | `{file: {path, bytes, sha256, mtime}}` per input file (`refresh.file_info`), or `{path, missing: true}`; stage C adds `survey_mode` / `raw_latest_only` in raw mode; E2 rows hold `config_id` and the rule set |
| `lrs_fingerprint` | the roads2 fingerprint (A, C) |
| `counts` | what the stage produced (per stage, below) |
| `checks` | every check's `{name, value, baseline, limit, ok, needs_accept, note}` |
| `message` | the exception text of a failed stage |

What each stage puts in `counts`:

| Stage | `counts` |
|---|---|
| A | `source` (downloaded, or reused from a folder) |
| B | `rows` loaded |
| C conflated | `rows`; per year `points`, `methods` (exact / prefix / fallback / none), `match_rate`, `dropped_records`, `dropped_routes`, `nhs_gap_as_is_records`, `nhs_gap_as_is_miles`; `swapped` |
| C raw | `mode`, `latest_only`, `files`, `rows`; per year `records`, `placed`, `placed_miles`, `placed_rate`, `dropped` by reason; `swapped` |
| D | `vendor_joints`, `sections`, `short`, `long`, `split`, `unsplit_long`, `joints`, `miles`, `len_p50`, `len_max`, `unchanged_from_current_build`, `build_id`, `crosswalk_old_joints` |
| E | `inserted`, `new` and `live` statistics (`checks.segment_stats`), `swapped`, `inputs` (the E1 counts), `families` (per config: changed segments, changed family) |
| E1 | segments, `inventory_cci`, `rehab_year`, `adt_growth_layer2`, `crack_pct_dtims`, `rehab_rows_updated`, `fed_aid_layer22`, `nhs_segments`, `nhs_miles`, `nhs_non_interstate_miles`, `no_fed_aid` |
| E2 (one row per config) | `config_id`, `changed_segments`, `changed_family`, `removed_segments`, `after` (segments and miles per family) |
| F | `committed_segments` |
| G | `survey_years`, `view_years`, row count of each view, `potential_projects` |

When stage E runs E1 and E2 itself, E1's counts go into E's row (no separate `E1_inputs` row); each config's family
rerun still writes its own `E2_families` row.

#### 3.1.3 Provenance

- **Input files**: path, size, sha256 and modification time of every file a stage reads (`refresh.file_info`).
- **roads2 fingerprint** (`lrs.db.roads2_fingerprint`): roads2 has no version or edit-date column, so the pipeline
  hashes its content: row count, distinct routes, and an md5 over `routeid | bmp | emp | ST_Length(geometry)` (bmp and
  emp to 4 decimals, length to 0.1 m), ordered by route. Stages A and C record it in `data_refresh_log`; stage D
  records it in `joint_builds.lrs_snapshot`; `backup_pms.py` records it in its manifest. Equal fingerprints mean the
  route ids, measure ranges and shape lengths are equal.
- **Per-row provenance**: `analysis_segments.survey_year` (the survey year of the row's condition),
  `.joint_build_id`, `.has_survey`; `reconflate_normalized.survey_year`; the `*_source` columns filled by E1
  (`adt_growth_source`, `rehab_source`, `iri_source`, `rut_source`, `flt_source`).

#### 3.1.4 Dry runs

`--dry-run` reads the inputs and logs a `dry_run` row, but changes no data. What each stage still does:

| Stage | In a dry run |
|---|---|
| A | No download. With `--reuse-lrs` the files are still copied into the refresh folder, and `intersections.sqlite` is still copied. Missing files are not an error. The fingerprint is recorded. |
| B | Hashes the survey files only. |
| C conflated | Hashes the files and records the fingerprint; no geocoding, no checks. |
| C raw | Places every record and runs the placement checks, logging where a real run would stop; nothing is inserted and `conflation_issues` is not written. |
| D | Builds the joints and writes `pavement_joints_lrs_breakdown.csv` to the refresh folder, compares them with the current build, and loads nothing. |
| E | Returns before building anything. |
| E1 | Hashes the layer files only. |
| E2 | A preview per config: segments and miles per family and how many rows would change; no `data_refresh_log` row. |
| F | Runs `populate_committed_flags.py` without `--apply` (it prints the SQL it would run). |
| G | Checks that every survey year is in the multi-year views; refreshes nothing. |

#### 3.1.5 `--accept` and stopping

Each check is either **hard** or **needs accept** (`needs_accept`, section 3.4). `checks.enforce` logs every check and
raises `CheckFailed` if a hard check failed, or a needs-accept check failed and `--accept` wasn't given. A hard check
can't be accepted. Use `--accept` only after someone has read the numbers in the log (`counts.new` / `counts.live`,
`conflation_issues`).

The runner stops at the first failed stage. `CheckFailed` ends the command with exit code 2 and the message
"STOPPED: … Live data was not changed by the failed stage"; any other exception is printed with its traceback and
ends the command with a non-zero code. The stage's log row is marked `failed` with the exception text. Later stages
don't run.

That message holds for the checks that run before a swap, but not for everything after one. Stage E commits its swap
of `analysis_segments` before E1 and the family reruns. If a config's family rules then leave segments unmatched, the
stage stops with the new `analysis_segments` already live and that config's `segment_families` partition not yet
rebuilt (section 3.3.5, step 8).

#### 3.1.6 Running one stage

Any stage can be named alone (`python -m pipeline segments --refresh-dir refresh/<run>`), or several together. Every
stage reads what earlier stages left in the database or the refresh folder, so running a later stage alone rebuilds
from the current state of its inputs. The dependencies are:

| Stage | Needs |
|---|---|
| A | network access to the R&H service (or `--reuse-lrs DIR`), `lrsops` on the `PATH` |
| B, C | `--survey-dir` |
| D | the refresh folder's `70.csv`, `intersections.sqlite`, `2.csv`; the `routes` table |
| E | the refresh folder's `lrs_table.csv`; `reconflate_normalized`; `pavement_joints`; roads2 |
| E1 | `analysis_segments`, `reconflate_normalized`, `projects`; `2.csv` and `22.csv` |
| E2 | `analysis_segments`, each config's rules and policy |
| F | `analysis_segments`, `projects` |
| G | `condition_history`, `reconflate_normalized` and views that cover every survey year |

### 3.2 Inputs

#### 3.2.1 Vendor survey files

One file per survey year, named `<YYYY>.csv`, in the folder given by `--survey-dir` (locally `~/Downloads/csvs`,
2020–2025). The **year comes from the file name**, never from `COND_YEAR`, which can be stale (a 2022 file with
`COND_YEAR = 2019`). Each row is one vendor record of about 0.1 mi of one route direction.

`stages._survey_files` requires at least one `20*.csv` file whose stem is a number. Stages B and C then read
**every** `*.csv` in the folder that doesn't start with a dot and convert each file stem to a year, so the folder
should hold only `<YYYY>.csv` files. Raw mode reads only the `<YYYY>.csv` files.

Columns used:

| Column | B `condition_history` | C conflated | C raw | Meaning |
|---|---|---|---|---|
| `ROUTEID` | yes | yes | yes | 13-character LRS route id as the vendor labels the road |
| `Unique` | – | yes (record key) | yes (record key) | the vendor's record id (e.g. `01200330000EB-000000` in 2025, `01200330000EB0` in 2020) |
| `BEG_MP`, `END_MP` | `BEG_MP` only (`emp = bmp + 0.1`) | the vendor window each record is re-weighted onto | the record's placement | vendor milepoints |
| `GPSLongS`, `GPSLatS`, `GPSLongE`, `GPSLatE` | stored | geocoded | ignored | start / end GPS of the record |
| `IRI_MEAN`, `IRI_MAX` | yes | yes | yes | roughness, in/mi |
| `IRIL`, `IRIR` | – | re-weighted, not stored | read, not stored | left / right wheel path IRI |
| `RUT_MEAN`, `RUT_MAX` | yes | re-weighted; only `RUT_MEAN` stored | same | rutting, in |
| `Fault_Avg` | yes | yes | yes | faulting, in |
| `JFAULT_L/M/H` | – | re-weighted, not stored | read, not stored | joint faulting counts |
| `FHWA_Percent_Cracking` | yes | yes | yes | FHWA percent cracking (HPMS measure) |
| `PERCENT_CRACKING` / `Percent_Cracking` | only the upper-case spelling | yes (both spellings) | yes (both spellings) | the vendor's percent cracking, what dTIMS read as PCRK. 2020–2022 files spell it `Percent_Cracking`, 2023 on `PERCENT_CRACKING`; C and raw mode rename it on read (`phase2_reconflate`, `raw_survey.read_survey_file`), B does not |
| `PSI`, `RDI`, `SCI`, `ECI`, `JCI`, `CSI`, `NCI`, `CCI` | yes | yes | yes | vendor indices, 0–5 |
| `SURF_TYPE` | – | dominant value | as delivered | surface (`ASP`, `JCP`, `CRC`, `OTH`, …) |
| `SHLD_TYPE` | – | dominant value | as delivered | shoulder type |
| `JNT_COUNT`, `SLAB_COUNT` | yes | – | – | joints and slabs counted |

A value of −1 (or anything ≤ −1) means "not measured" and becomes NULL in every table.

Not read by any stage: `THROUGH_LANES` / `THRU_LANES`, `LANE`, `LANEWIDTH`, `PATCH_L/M/H` (2025 file),
`COND_YEAR`, `DATE`, the distress quantities (`FALLIG_*`, `FLONG_*`, `FTRANS_*`, …) and the flags (`BRIDGE`, `CONSTR`,
`WET`, …).

#### 3.2.2 LRS attribute layers

Stage A downloads these layers from the WVDOT R&H service with `lrsops rhoverlay` (`RH_LAYERS = "15,35,22,12,18,49,77,2"`,
`--codes-add` adds each coded field's `_DESC`, `--carry-json {"77": ["AADT_COMBINATION", "AADT_SINGLE"]}`). It writes one
`<layer>.csv` per layer and their overlay, `lrs_table.csv` (one row per route piece with every layer's fields as
`<layer>_<FIELD>`).

| Layer | Field(s) used | Becomes | Used by |
|---|---|---|---|
| 2 AADT | `AADT` | `analysis_segments.aadt` | E (overlay); D (termini AADT, from `2.csv`) |
| 2 AADT | `AADT_ESCALATION_PCT`, `AADT`, `AADT_YEAR`, `FUTURE_AADT`, `FUTURE_AADT_YEAR` | `adt_growth_layer2` / `adt_growth_future` | E1 (`2.csv`) |
| 12 County | `COUNTY`, `_DESC` | `county_code`, `county_desc` | E |
| 15 Section | `SECTION_NO` | `coal_route` (a coal-route section when not null) | E; family rules (high truck load) |
| 18 District | `DISTRICT`, `_DESC` | `district_code`, `district_desc`, `district` | E |
| 22 Federal Aid | `FAS_TYPE`, `_DESC` | `fed_aid_code`, `fed_aid_desc`, and from them `nhs_code` / `nhs_desc` | E (overlay), E1 (refill from `22.csv`), C (NHS gap fill) |
| 35 Functional class | `NAT_FUNCTIONAL_CLASS`, `_DESC` | `functional_class`, `functional_class_desc` | E |
| 49 Route status | `ROUTE_STATUS`, `_DESC` | `route_status`, `route_status_desc` | E |
| 77 Truck AADT | `AADT_COMBINATION`, `AADT_SINGLE` | `aadt_combination`, `aadt_single`, and `truck_pct` | E |

The NHS designation comes from layer 22 (Federal Aid), as in dTIMS, not from layer 36 (NHS), which AMPS read before
v1.7.2 (migration 041). The `lrs_table.csv` in the repo root is the 2026-04-15 download and still carries `36_NHS`
columns, not `22_*`. On a refresh that reuses it (`--reuse-lrs .`), the overlay has no `22_FAS_TYPE` to carry, and E1's
refill from `22.csv` is what sets `fed_aid_code`. The code doesn't show how `lrsops overlay` treats a missing split
field.

`lrsops` downloads only when attached to a terminal, so `import_pavement_data._run(…, tty=True)` runs the download
commands under a pseudo-terminal.

#### 3.2.3 Layer 70 (pavement joints)

`lrsops rhoverlay -l 70 --lrs-database=false --redownload` writes `70.csv`, the surface-type events. Stage D reads only
`OBJECTID`, `ROUTE_ID`, `FROM_MEASURE`, `TO_MEASURE`: layer 70 says where pavement is, not which surface it has.
**Joints are built only from layer 70** (`pipeline.joints.read_layer70`). Earlier imports re-exported
`pavement_joints` as the joint input, which fed each build's output back in and lost the vendor boundaries.

#### 3.2.4 `intersections.sqlite`

The output of `lrsops intersections` over the roads mbtiles (`$LRSPATH/wv_roads12.mbtiles`): tables of nodes and
`node_routes` (node, route, measure). Stage A copies it from `--intersections` (default: the repo's
`intersections.sqlite`) into the refresh folder, or rebuilds it with `--rebuild-intersections`. Stage D uses it to
find the crossing routes where long pavement sections are split.

#### 3.2.5 roads2

`operations.roads2` in the `dot12_test` database (`ROADS_DB_NAME`) on the same Postgres server (10.0.1.229):
one `MULTILINESTRING ZM` per route in SRID 3747 (NAD83(HARN) / UTM 17N, metres), M = milepoint in miles, with `bmp` /
`emp` columns. It is maintained outside AMPS. `lrs.db.lrs_engine` connects read-only
(`default_transaction_read_only=on`, `statement_timeout` 120 s). Uses in the pipeline:

- stage C: geocoding (conflated mode) and route extents (NHS gap fill, raw mode);
- stage E: the unsurveyed-road fill and the `routes_not_on_roads2` check;
- stages A, C, D: the fingerprint.

At the time of writing roads2 has 98,253 routes with a positive length.

#### 3.2.6 Projects and the `routes` table

- **`projects`, CLOSED rows** (project history): loaded by `scripts/import_past_projects.py` from
  `raw_pavements.xlsx`, a TheHub export. The script deletes every `status = 'CLOSED'` row and inserts the export, with
  `construction_year` from `ProjectCompletionDate` and a treatment from `ConstructionCode_Name`. Stage E1 reads them
  for each segment's rehab year. The live TheHub endpoints (`/api/hub/*`, `api/routes/hub_projects.py`) feed the maps
  and project pages. They are not a pipeline input.
- **`projects`, committed rows** (`planned`, `designed`, `awarded`, `in_progress`): written mainly by Run Validation
  commits (`api/routes/validation.py`). Stage F reads them.
- **`routes`**: loaded by `db/load_routes.py`. Stage D uses it as a route filter: only layer-70 events on a route in
  this table become joints. It holds 15,124 routes today and none on sign system 8 (HARP).

### 3.3 The stages

#### 3.3.1 A `lrs`: LRS snapshot

`stages.stage_lrs`. Puts every LRS input into the refresh folder from **one** source, so later stages all use the same
LRS:

1. **Default: download now.** `import_pavement_data.run_lrsops_rhoverlay` writes `lrs_table.csv` and
   `2.csv, 12.csv, 15.csv, 18.csv, 22.csv, 35.csv, 49.csv, 77.csv`. Then `run_lrsops_layer70` writes `70.csv`.
2. **`--reuse-lrs DIR`**: copy `lrs_table.csv`, the eight layer files and `70.csv` from an earlier download (for
   example the repo root, which holds the 2026-04-15 download). A missing file stops the stage.
3. **`intersections.sqlite`**: copied from `--intersections` (default: the repo's copy), or rebuilt with
   `lrsops intersections -o …` when `--rebuild-intersections` is given.
4. Records every file's hash (a missing file stops the stage, except in a dry run) and the roads2 fingerprint.

Writes: files in the refresh folder only.

#### 3.3.2 B `survey`: raw survey → `condition_history`

`import_pavement_data.phase1_condition_history`. For each survey file:

1. Keeps rows with a non-empty `ROUTEID` and a `BEG_MP`.
2. `segment_id = <ROUTEID>-<BEG_MP as %07.3f>`, `bmp = BEG_MP`, `emp = bmp + 0.1` (the vendor's `END_MP` isn't used).
3. `survey_year` = the file name's year. Deletes that year's rows (`DELETE … WHERE survey_year = <year>`), so each year
   replaces only itself.
4. De-duplicates `(segment_id, survey_year)`, keeping the last row.
5. Turns −1 into NULL for the indices, IRI, rut, cracking and faulting.
6. Inserts in batches of 5,000 (`ON CONFLICT (segment_id, survey_year) DO UPDATE`).

Columns: `segment_id`, `route_id`, `bmp`, `emp`, `survey_year`, `data_source` (the file name), `iri_mean`, `iri_max`,
`rut_mean`, `rut_max`, `crack_percent` (`PERCENT_CRACKING`), `fhwa_crack_percent`, `cci`, `psi`, `rdi`, `sci`, `eci`,
`jci`, `csi`, `nci`, `faulting` (`Fault_Avg`), `joint_count`, `slab_count`, `lat_start`, `lon_start`, `lat_end`,
`lon_end`. `survey_date`, `aadt`, `truck_pct`, `coverage_pct` and `confidence_score` are always NULL.

`condition_history` keeps the vendor's own milepoints. No stage joins on them; the engine reads the conflated
milepoints of `reconflate_normalized`. Stage G's multi-year views read it. Because stage B doesn't rename
`Percent_Cracking`, `crack_percent` is empty for 2020–2022 (2023–2025 are complete).

Stage B isn't staged: each year is deleted and reinserted in its own transaction.

#### 3.3.3 C `conflate`: survey → LRS milepoints → `reconflate_normalized`

Stage C has two modes, and since migration 057 **their results coexist**: conflated mode writes `reconflate_normalized`,
raw mode writes its own table `reconflate_raw` (same columns and conventions), and neither touches the other. Stage E
then builds one **survey network** per mode (`analysis_segments.network` = `conflated` / `raw`, see 3.3.5), and each
config chooses the network its runs and pages read (`configs.survey_network`, section 4). **Switching a config to raw is
a config edit, not a rebuild**; rebuild a network only when its survey data changes.

| | `--survey-mode conflated` (default) | `--survey-mode raw` |
|---|---|---|
| Writes | `reconflate_normalized` (also feeds the multi-year views) | `reconflate_raw` |
| Stage E network | `analysis_segments.network = 'conflated'` | `analysis_segments.network = 'raw'` |
| Code | `import_pavement_data.phase2_reconflate` + `pipeline/conflate.py` | `pipeline/raw_survey.py` |
| Where a record goes | its start and end GPS located on roads2; values re-weighted from the located records overlapping its vendor window | the vendor's `ROUTEID` and `BEG_MP` / `END_MP`, values as delivered (as dTIMS reads the file) |
| Files | every survey file | every `<YYYY>.csv`, or only the newest with `--raw-latest-only` |
| Drops | unlocated records; whole routes with a record spanning > 1 mi | records that can't be placed |
| NHS gap fill | yes, latest file only | not needed |
| Checks | GPS match rate ≥ 97% per year (needs accept) | > 0 records placed per year (hard); ≥ 97% placed (needs accept) |
| Run time (2020–2025) | about an hour | about 4 minutes |
| Rows (2020–2025, 2026-09-30) | 431,684 | 454,807 |

##### Conflated mode

For each survey file, oldest first:

1. **Read.** The file is read with `Percent_Cracking` renamed to `PERCENT_CRACKING`.
2. **Geocode** (`conflate.add_lrs_milepoints`). The start points (`GPSLongS`, `GPSLatS`) and the end points (`GPSLongE`,
   `GPSLatE`) go through `lrs.geometry_to_measure.geometry_to_measure` with a 15 m tolerance (`conflate.TOLERANCE_M`),
   on one open roads2 connection, in chunks of 2,000 points. For each point, in one SQL statement:
   - the point is transformed to SRID 3747;
   - candidate routes are the roads2 routes within 15 m (`geometry && ST_Expand(p, tol)` on the GiST index, then
     `ST_DWithin`);
   - on each candidate the nearest part of its multi-line is used (roads2 routes can have up to 6 parts with gaps in M);
   - `measure = ST_InterpolatePoint(part, p)` (miles), `line_distance = ST_Distance(part, p)` (metres);
   - up to 10 candidates are kept, nearest first (ties by route id).

   A point with missing or out-of-range coordinates gets no candidate. Results stay aligned with their rows.
3. **Choose a measure** (`conflate.pick_measure`) for each point:

   | Method | Candidate used |
   |---|---|
   | `exact` | the nearest candidate whose route id is the record's `ROUTEID` |
   | `prefix` | else the nearest whose id starts with `ROUTEID` minus its trailing direction letters (N, B, E, S, W) |
   | `fallback` | else the nearest candidate of any route. It is kept, but not counted as located on its own route. The measure then comes from a different route while the record keeps its vendor `ROUTEID`. |
   | `none` | no route within 15 m. The measure is −1. |

   The results are `ActualBMP` (start) and `ActualEMP` (end). A point counts as matched (`status_bmp` / `status_emp`)
   for `exact` and `prefix`.
4. **Clean.** Every drop is recorded in the year's report, which goes to `conflation_issues`:
   - routes with fallback points are listed (`fallback_route`, records per route; the records are kept);
   - `ActualBMP > ActualEMP` is swapped;
   - records whose start or end wasn't located (measure < 0) are dropped (`not_located`);
   - **a whole route is dropped** if any of its records spans more than 1 mi after geocoding
     (`conflate.MAX_SPAN_MI`; `route_dropped_span_gt_1mi`). Such a span usually means a fallback onto the wrong part of
     a route.
5. **Re-weight** (`import_pavement_data.auto_conflate`). Per vendor route, for every remaining record (the "outer"
   record, window `[BEG_MP, END_MP]`):
   - every located record on the same `ROUTEID` whose `[ActualBMP, ActualEMP]` overlaps the window contributes the
     overlap clipped to the window;
   - weights are the overlap lengths, normalised to sum to 1 per outer record;
   - numeric fields (`NUMERICAL_FIELDS`, 3.3.3.1) take the weighted sum. If any contributor has −1 for a field, the
     result is −1 (missing);
   - categorical fields (`SURF_TYPE`, `SHLD_TYPE`) take the value with the largest total weight;
   - the outer record's result is `ActualBMP = min` and `ActualEMP = max` of the clipped pieces, `percent` = the sum
     of weights (1.0), keyed by the outer record's `Unique` (`NameOuter`).

   An expansion ratio above 2× (overlap rows per record) is logged as a warning.
6. **NHS gap fill, latest file only** (`conflate.nhs_gap_records`). This runs when `22.csv` is found (refresh folder,
   else the repo root). NHS stretches come from layer 22 with `FAS_TYPE` in 1, 2 or 4 (`conflate.nhs_intervals`,
   `dtims_inputs.NHS_FAS_TYPES`). A record of the newest file is added **as delivered** (`ActualBMP/EMP = BEG_MP/END_MP`,
   values unaveraged, `percent` 1.0) when all of these hold:
   - `END_MP > BEG_MP`, and its `ROUTEID` is on roads2 and has NHS stretches;
   - it lies inside the roads2 route (`BEG_MP ≥ route bmp − 0.01`, `END_MP ≤ route emp + 0.05`);
   - at least half of it lies in an NHS stretch of its route (by the vendor's milepoints);
   - the conflated output has nothing on that route over its window (overlap ≤ 0.001 mi).

   Each route's count is written as `nhs_gap_as_is`. This covers roads the vendor labels with an old route id. For
   example, Corridor H (US 48) east of Davis is labelled WV 93: its GPS falls on US 48, so geocoding drops the route
   every year, while dTIMS carries it as WV 93 MP 0–11.7. On the 2025 file the fill loads 376 records (37.3 mi) on 14
   routes.
7. **Grade and insert.** `add_gfp` maps `SURF_TYPE` (`JCP` → `JOINTED`, `CRC` → `CRCP`, others unchanged) and adds the
   legacy Good/Fair/Poor grades. `_insert_reconflate_batch` writes the rows to `reconflate_normalized_stage`
   (`ON CONFLICT (segment_id, survey_year) DO UPDATE`); −1 and NaN become NULL.
8. **Issues.** `conflate.write_issues` deletes the year's earlier `conflation_issues` rows and writes this run's rows
   plus one `summary` row (`records` = GPS points read). It commits per year, before the checks, so a run that later
   fails its checks still leaves its issues.

After every file, the stage runs `checks.conflation_checks` (match rate per year), then swaps
`reconflate_normalized_stage` into `reconflate_normalized` (`swap_in` with `RECONFLATE_COLS`) and commits.

##### Raw mode (`--survey-mode raw [--raw-latest-only]`)

`raw_survey.stage_conflate_raw`, logged as `C_conflate` with `survey_mode: raw`. No GPS is read, and there's no
geocoding, prefix/fallback matching, span drop or re-weighting.

1. `select_survey_files`: every `<YYYY>.csv`, oldest first, or only the newest with `--raw-latest-only`.
2. `read_survey_file`: `Percent_Cracking` → `PERCENT_CRACKING`.
3. `roads2_extents`: `(bmp, emp)` of every roads2 route.
4. `place_records`: each record is tested in this order, and the first failed test is its drop reason:

   | Reason | Test |
   |---|---|
   | `raw_no_route` | empty `ROUTEID` |
   | `raw_not_on_roads2` | the route id isn't in roads2 |
   | `raw_no_milepoints` | `BEG_MP` or `END_MP` missing or not a number |
   | `raw_zero_length` | `END_MP ≤ BEG_MP` |
   | `raw_outside_roads2_extent` | `BEG_MP < route bmp − 0.01` or `END_MP > route emp + 0.05` (the NHS-gap tolerances) |
   | `raw_duplicate_record` | a `Unique` already placed this year (the first is kept). Without a `Unique` column the key is `ROUTEID-<BEG_MP×1000>`. |

   Placed records get `ActualBMP/EMP = BEG_MP/END_MP`, `percent` 1.0, the numeric fields with −1 for "not measured",
   and the categorical fields, indexed by `Unique`, which is the shape of `auto_conflate`'s output.
5. `add_gfp` and `_insert_reconflate_batch` into `reconflate_normalized_stage`. Each year's report goes to
   `conflation_issues`: drops by reason and route, one `raw_mode_placed` row (records placed) and the `summary` row
   (records read).
6. `raw_placement_checks`, then `swap_in` into `reconflate_raw` (the conflated table is untouched). `conflation_issues`
   rows are replaced per mode: raw mode's reasons start with `raw_` (its summary row is `raw_summary`), and each mode
   deletes only its own rows of a year.

On the 2020–2025 files (2026-09-30), raw mode places 99.8–100% of each year's records. The difference from the
conflated rows is the records the conflated path drops (unlocated GPS, routes with a > 1 mi span), about 5,000 a year in
2020–2022 and 6,700 in 2024. On 2025 raw mode places all 48,516 records (4,782.0 mi, 987 routes). Where both modes have a
record, the milepoints are the same and IRI differs by 0.18 in/mi on average (the re-weighting).

**`--raw-latest-only` leaves only the newest year in `reconflate_raw`.** The raw network's grid then has survey data
only where the newest file surveyed (2025: 4,782 mi). Road that only older files covered becomes unsurveyed fill
(`has_survey` FALSE) instead of keeping its older condition. `condition_history` keeps every year. After such a run,
`conflation_issues` still holds the older years' raw rows from the last raw run that loaded them. The conflated network
is unaffected.

##### 3.3.3.1 Fields carried through stage C

`NUMERICAL_FIELDS`: `IRI_MEAN`, `IRI_MAX`, `IRIL`, `IRIR`, `RUT_MEAN`, `RUT_MAX`, `Fault_Avg`, `FHWA_Percent_Cracking`,
`PERCENT_CRACKING`, `PSI`, `RDI`, `SCI`, `ECI`, `JCI`, `CSI`, `NCI`, `CCI`, `JFAULT_L`, `JFAULT_M`, `JFAULT_H`.
`CATEGORICAL_FIELDS`: `SURF_TYPE`, `SHLD_TYPE`. Stored in `reconflate_normalized` (section 3.6.2): `IRI_MEAN`,
`IRI_MAX`, `RUT_MEAN`, `Fault_Avg`, `FHWA_Percent_Cracking` (`fhwa_crack_pct`), `PERCENT_CRACKING` (`pct_crack`, added to
the fields on 2026-09-25; before that it was dropped and `pct_crack` stayed empty), the eight indices, `SURF_TYPE`,
`SHLD_TYPE`. `IRIL`, `IRIR`, `RUT_MAX` and `JFAULT_*` are averaged but not stored.

#### 3.3.4 D `joints`: layer 70 → pavement joints (a versioned build)

`stages.stage_joints` → `pipeline.joints.build_joints` and `load_build`. A joint is the unit the optimizer selects: a
stretch of one route, about 0.2–4 mi.

**Inputs** (refresh folder): `70.csv`, `intersections.sqlite`, `2.csv`. `read_layer70` keeps events with
`TO_MEASURE > FROM_MEASURE` on routes in the `routes` table. Each event becomes a vendor joint `70_<OBJECTID>`.

**Algorithm** (the algorithm of `scripts/joint_breakdown_intersections.py`, constants unchanged):

1. **Merge** touching vendor joints on a route (`|bmp − previous emp| ≤ 0.001`) into continuous sections, whatever
   their surface. A section keeps its first vendor id. A section ends only where the pavement events have a gap or the
   route ends.
2. Sections ≤ 3 mi (`MAX_SEGMENT_LEN`) pass through whole.
3. **Candidates** for longer sections (`build_candidates`):
   - intersections strictly inside the section (0.01 mi from each end);
   - the crossing route has sign system 1, 2, 3, 4 or 7 (`VALID_SIGN_SYS`) and a 13-character id, so no ramps;
   - the crossing route isn't the same US route (sign 2) in the other direction (same first 11 characters);
   - the crossing route's AADT comes from `2.csv` at the crossing measure (±0.01 mi, else the nearest event within
     1 mi, else the highest AADT on the parent route with the sub-route zeroed, else 0);
   - each node keeps its highest-AADT crossing (stable sort), and nodes within 0.1 mi (`CLUSTER_THRESHOLD`) are
     clustered, keeping the highest AADT.
4. **Break points** (`select_best_breakpoints`): candidates are taken highest AADT first, each accepted if every piece
   stays ≥ 1 mi (`HARD_MIN_LEN`). Skipped candidates are then tried only inside pieces still longer than 4 mi
   (`TARGET_MAX_LEN`), again keeping every piece ≥ 1 mi.
5. **Ids**: `joint_id = 70_<routeid>_<n>`, n = 1-based order along the route by `bmp`. `parent_joint_id` is the vendor
   joint the piece came from, `sub_joint_id` its piece number. `termini_routeid` / `termini_aadt` are the crossing route
   at the piece's end break, and `termini_label` reads e.g. `Start -> US 19`.

**Loading:**

- The new joints are compared with `pavement_joints`. If the ids and spans are identical (every `bmp` and `emp` within
  0.0015 mi) and a current build exists, nothing is loaded and `counts.build_id` is the current build.
- Otherwise `load_build` runs in one transaction:
  1. a new `joint_builds` row (`build_id = max + 1`, `status 'current'`, the inputs with hashes, the roads2
     fingerprint, the algorithm parameters, the joint count);
  2. the joints go to `joint_builds_archive` (every build is kept);
  3. `joint_crosswalk` maps every joint of the previous current build to each new joint it overlaps on the same route
     (overlap > 0.0005 mi), with `overlap_mi` and `share_of_old`;
  4. the previous build is marked `archived`;
  5. `pavement_joints` is emptied (`DELETE`) and refilled from the new build.

`analysis_segments.joint_id` isn't changed here; stage E rebuilds the segments on the new joints. Ids are positional,
so a change on a route (a new AADT count, a new intersection, a changed surface event) can renumber the later joints on
that route. That is why builds are versioned: runs record `configuration.joint_build_id`, and Validate translates a
run's joints through the crosswalk. The current build is build 0 (22,480 joints on 15,120 routes), which the
2026-04-15 layer 70 reproduces exactly.

`python -m pipeline.joints --layer70 … --intersections … --aadt … --out …` writes the CSV without loading a build.

#### 3.3.5 E `segments`: the engine's network → `analysis_segments`

`stages.stage_segments` → `import_pavement_data.phase3_analysis_segments`, then checks, swap, E1 and E2. (The
function's docstring numbers its own sub-steps E1–E4. Those are not the stages E1 and E2.)

**Stage E builds one survey network per run** (migration 057): the one named by `--survey-mode` (default
`conflated`). The conflated network is built from `reconflate_normalized`, the raw network from `reconflate_raw`; its
rows carry `analysis_segments.network`, and the swap replaces only that network's rows. The other network's rows,
their `analysis_segment_id`s and their family rows are untouched, so both stay loaded and a config picks one with
`survey_network` (4.6.1). The view `analysis_segments_cfg` joins each config to its network only, so runs, Validate,
the condition pages and the ORM model all see one network.

1. **Stage table.** `analysis_segments_stage` is recreated `LIKE analysis_segments INCLUDING ALL`, plus a
   `current_cci` column used only while building.
2. **Surveyed grid** → `segments_base.csv`. From the network's source (`reconflate_normalized` or `reconflate_raw`) rows with a route, an `actual_bmp` and either
   `iri_mean` or `psi`:
   - one row per `(route_id, ROUND(actual_bmp, 1))` cell (`DISTINCT ON`);
   - the **most recent `survey_year` wins**; ties within a year go to the lowest `iri_mean`, then NULLs;
   - `bmp` = the cell (`ROUND(actual_bmp, 1)`), `emp = bmp + 0.1`, `lanes = 2`, `current_age = 0`, `has_survey = 1`;
   - condition: `surface_type`, `current_iri` ← `iri_mean`, `current_rut` ← `rut_mean`, `current_crack` ←
     `fhwa_crack_pct`, `current_faulting` ← `faulting`, `current_psi … current_csi` ← the vendor indices, `survey_year`.

   The stage fails if the grid is empty.
3. **Unsurveyed fill** (`_append_unsurveyed_cells`, migration 056). Every roads2 route whose sign system (the third
   character of its id) is in `UNSURVEYED_SIGNS = ("1", "2", "3", "4", "7", "8")` and has `emp > bmp` is cut into
   0.1-mi cells (`floor(bmp × 10) / 10` onward), each clipped to the route's ends. A cell is appended to the grid when
   the grid has no cell with the same route and `ROUND(bmp, 1)`. So routes the survey never drove are filled whole,
   and gaps inside surveyed routes are filled too. Fill rows get `lanes = 2`, `current_age = 0`, `has_survey = 0` and
   no condition or survey year. The six signs are Interstate, US, WV, County, federal-aid non-state (FANS) and HARP.
   They leave out sign 0 (MNS), 6 (State Park) and the letter codes. The fill matches on sign only, so ramp ids on
   those signs are included.
4. **Joints** → `pavement_joints_lrs.csv` (the current build).
5. **Overlay** (`lrsops overlay --operations segment_overlay_ops.json`):
   - op 1 splits the grid at joint boundaries, carrying `joint_id`;
   - op 2 splits the result at every change of the LRS fields in `lrs_table.csv`, carrying `2_AADT`, `15_SECTION_NO`,
     `18_DISTRICT(_DESC)`, `22_FAS_TYPE(_DESC)`, `35_NAT_FUNCTIONAL_CLASS(_DESC)`, `12_COUNTY(_DESC)`,
     `77_AADT_COMBINATION`, `77_AADT_SINGLE`, `49_ROUTE_STATUS(_DESC)`.

   A row can therefore be much shorter than 0.1 mi. The stage fails if the overlay fails or writes no output.
6. **Transform** (`_transform_overlay_output`, polars):
   - renames the overlay columns (e.g. `18_DISTRICT` → `district_code`, `15_SECTION_NO` → `coal_route`, `2_AADT` →
     `aadt`); an overlay column wins over a base column of the same name;
   - casts types; `current_jci` / `current_csi` NULL → 5.0; then every index column still NULL or NaN → 5.0
     (`current_psi`, `current_rdi`, `current_sci`, `current_eci`, `current_jci`, `current_csi`). The raw distress
     columns stay NULL where not measured;
   - `truck_pct = (aadt_single + aadt_combination) / aadt` (each NULL as 0), or 0 where `aadt` is NULL or 0;
   - `district` = `district_code` as text;
   - classifies every row with the **system default config's** family rules and starting state (`families.apply`).
     Only `current_cci` of that result is inserted, into the stage-only column. In practice this step checks that
     the default config's rules match every row: an unmatched row fails the stage before the swap. `current_age` is
     not recomputed, because the grid already carries it, so it stays 0 on every row;
   - `length_miles = end_mp − begin_mp`, rounded to 4 decimals; `joint_build_id` = the current build;
   - keeps only rows from the grid: surveyed pieces (a `survey_year` and `has_survey`) and fill pieces
     (`has_survey` false). The overlay also emits pieces of joints and LRS events outside the grid; those carry neither
     and are dropped, as are rows without a route or with zero length.
7. **Check and swap.** The rows go to `analysis_segments_stage` in batches of 5,000, every one tagged with the network.
   `checks.segments_checks` compares it with the live rows of the same network (section 3.4; on a network's first
   build, when it has no rows yet, with the other network). Then the swap copies every stage column except
   `analysis_segment_id` and `current_cci`: `DELETE FROM analysis_segments WHERE network = …; INSERT … SELECT` in one
   transaction (no `TRUNCATE`, so the other network survives), and the stage commits. Columns the
   stage table doesn't fill come in empty or at their defaults: the E1 columns (filled next), `is_committed` FALSE and
   the other commitment columns NULL (until stage F), `hpms_flag`, `patch_l/m/h` (until stage F2 `patching`).
8. **E1 and E2.** `stages._refresh_inputs` fills the dTIMS inputs on the new rows (3.3.6) and commits. Then
   `_reclassify_configs` reruns **every config's** family rules (3.3.7) over both networks' rows. The rebuilt
   network's rows have new `analysis_segment_id`s (the sequence continues; ids are not reused), so every partition of
   `segment_families` must gain rows for them; the family rows of the deleted ids are removed as orphans. Until it
   runs, the rebuilt network has no family rows and is invisible through `analysis_segments_cfg`. A config whose rules leave any segment unmatched stops the stage
   with `CheckFailed`. At that point the swap and E1 are committed, configs before it in `config_id` order are
   regenerated, and it and later configs are not. Fix the rules and run `python -m pipeline families`.

The stage-E grid carries no lane count: `lanes` is 2 on every row, and the engine's lane-miles use it
(`default_lanes` applies only where `lanes` is not positive).

#### 3.3.6 E1 `inputs`: the dTIMS model inputs

`pipeline/dtims_inputs.refresh_inputs`, in one transaction on the live `analysis_segments`. Stage E runs it after its
swap. `python -m pipeline inputs` runs it alone: after loading CLOSED projects, or a new `2.csv` / `22.csv`, follow it
with `families`. It fills inventory **facts** only. Each config's policy chooses among them when its starting state is
built (`dtims_state._apply_input_policy`): which growth source comes first, how much project coverage counts, and
which cracking measure is used.

| Column(s) | Rule | Source |
|---|---|---|
| `sign_code` | 3rd character of `route_id` | route id |
| `route_number` | characters 4–7, leading zeros removed (NULL if empty) | route id |
| `supp_code` | characters 10–11 when the id has ≥ 11 characters (the `TURNPIKE` route group reads it) | route id |
| `inventory_cci`, `raw_psi`, `raw_rdi`, `raw_sci`, `raw_eci`, `raw_jci`, `raw_csi` | the vendor's CCI and indices as delivered, −1 → NULL (NULL = not measured). From the `reconflate_normalized` row of the segment's grid cell: same route, same `survey_year`, cell = `FLOOR(midpoint × 10) / 10`. If a cell has several rows that year, the one with the lowest `iri_mean` (NULLs last). Unlike the grid, it doesn't require IRI or PSI, so in such a cell the two picks can differ. | `reconflate_normalized` |
| `crack_pct_dtims` | that row's `pct_crack` (PERCENT_CRACKING, dTIMS's PCRK) | `reconflate_normalized` |
| `adt_growth_layer2`, `adt_growth_future`, `adt_growth_event` | all cleared, then set from the layer-2 event that overlaps the segment the **longest** (ties: lowest `bmp`). `AADT_ESCALATION_PCT` when filled (source `layer2`; empty in the 2026 download); else `((FUTURE_AADT / AADT)^(1 / (FUTURE_AADT_YEAR − AADT_YEAR)) − 1) × 100` when both AADTs and the year span are positive (`layer2_future`). `adt_growth_event = route:from-to`. | `2.csv` (refresh folder, else repo root) |
| `adt_growth_district` | the district median of `COALESCE(adt_growth_layer2, adt_growth_future)`, per survey network | computed |
| `adt_growth_pct`, `adt_growth_source` | the default order: `layer2`, `layer2_future`, `district_median`, else 0 (`default0`). For browse pages; runs use the config's `adt_growth_fallback`. | computed |
| `fed_aid_code` | cleared and refilled from the layer-22 event overlapping the segment the longest. Without `22.csv` the overlay's value is kept. | `22.csv` |
| `fed_aid_desc` | `1 – Interstate`, `2 – NHS (National Highway System)`, `3 – STP (…)`, `4 – Intermodal Connectors`, `5 – Non-Federal-Aid` | `fed_aid_code` |
| `nhs_code`, `nhs_desc` | `fed_aid_code` when it is 1, 2 or 4, else 0 / `Not on the NHS`. `nhs_code > 0` = on the NHS; dTIMS's non-Interstate NHS set (`DEL_NHS`) is `nhs_code IN (2, 4)`. | `fed_aid_code` |
| `rehab_year`, `rehab_project_id`, `rehab_treatment_id`, `rehab_coverage`, `rehab_source` | cleared, then rebuilt from the latest CLOSED project (by `construction_year`, then `project_id`) on the same route whose `[bmp, emp]` overlaps the segment: its year, id, own treatment code, the share of the segment it covers (capped at 1), and `rehab_source = 'project'` | `projects` |
| `iri_source` | `dtims_default` when `current_iri` is NULL, else `survey` | computed |
| `rut_source`, `flt_source` | `dtims_default` when `current_rut` / `current_faulting` is NULL or negative, else `survey` | computed |

`inventory_rehab_type` is cleared and never set. `hpms_flag` / `hpms_source` and `patch_l/m/h` aren't written by any
stage (section 3.9).

Unsurveyed rows have no `survey_year`, so they get no vendor values (`inventory_cci` and `raw_*` NULL) and
`iri_source = 'dtims_default'`. They do get growth, Federal Aid, NHS and rehab values like any other row.

#### 3.3.7 E2 `families`: each config's family and starting state → `segment_families`

`pipeline/families.reclassify`, once per config (`families.config_ids`, every row of `configs`), or only `--config N`.
Stage E runs it for every config after its swap. `python -m pipeline families` runs it alone after
`pavement_family_rules` or `pavement_families` were changed outside the app, or after `inputs`. The app runs the same
function when an admin saves a config's family rules and when an Excel import changes a config
(`api/config_workbook.py`, in the import's transaction).

For one config:

1. Loads the config's rules and checks them (`validate_rules`: at least one enabled rule, unique priorities, family ids
   of the form `BC|RC|OT _ Initial|Minor|Major _ H|L` that have curves in `pavement_families`, known fields and
   operators). A problem raises.
2. Takes a transaction-level advisory lock per config (`hashtext('pms_family_reclassify')`). If another rerun holds
   it, the rerun fails ("try again in a minute").
3. Compiles the config as the transaction sees it (`engine.compiled.compile_cursor`).
4. Reads every analysis segment with the rule fields, the state inputs (`STATE_INPUTS`), the config's route-group
   fields and its current classification.
5. **Classifies** (`classify`): enabled rules in ascending `priority`; the first match sets `family_id`, and from it
   `pavement_type`, `rehab_type` and `truck_load`. Where the segment's latest CLOSED project counts
   (`rehab_year` set and `rehab_coverage ≥ min_rehab_coverage`, default 0.5), `rehab_type` is the one the config's
   treatment for that project's code sets (`cfg.rehab_type_of`: its `REHAB_SET`, or a `project_treatment_map` entry),
   and `family_id` is recomposed. Segments matching no rule make the rerun fail with nothing written. The log row says
   how many.
6. **Starting state** (`init_condition` → `engine.condition.dtims_state.initial_state` + `classify_gfp`, at the
   config's `start_year`, else the current year). This is covered in section 5: the seven indices (CCI = the vendor's
   CCI), fractional ages from the rehab year (capped at `max_start_age`; `missing_rehab_age` without one), raw
   distress, and its MAP-21 class.
   - **Unsurveyed rows** (`has_survey` FALSE): with `unsurveyed_policy = 'dtims_defaults'` they start as dTIMS starts
     its no-data sections: CCI 99, PSI and RDI at the index floor (−1), the other indices 0, IRI, rut and cracking 0.
     With `exclude` (the default), their family and `start_year` are stored but every other starting-state column
     is NULL, so browse pages don't rate them and runs don't load them.
7. **Writes** only rows that changed (`INSERT … ON CONFLICT (config_id, analysis_segment_id) DO UPDATE`), deletes the
   partition's rows for segments that no longer exist, creates the partition `segment_families_c<id>` if needed, and
   logs `E2_families` with the rule set and the counts. It all happens in one transaction.

A run takes a few seconds per config. `--dry-run` previews every config without writing or logging.

#### 3.3.8 F `commitments`: committed projects → `analysis_segments`

`stages.stage_commitments` runs `scripts/populate_committed_flags.py --base-year 2026 --apply` (`BASE_CALENDAR_YEAR`)
as a subprocess, in one transaction:

1. Resets every flagged segment (`is_committed` FALSE, `committed_treatment_id`, `committed_program_year`,
   `committed_project_id` NULL).
2. For every project with status `planned`, `designed`, `awarded` or `in_progress` and a treatment, route and
   `program_year`, flags the segments it overlaps on the same route **by milepoint**
   (`begin_mp < project.emp AND end_mp > project.bmp`). Flags therefore never depend on joint ids.
   `committed_program_year = program_year − 2026 + 1` (2026 = program year 1).

When several projects overlap one segment, the SQL doesn't define which one sets the flags: the script computes a
per-route rank but doesn't filter on it.

Because stage E's swap clears every commitment flag, run F after every E. `all` does.

#### 3.3.9 G `derived`: multi-year views and potential projects

`stages.stage_derived`:

1. Collects the survey years in `condition_history` and `reconflate_normalized`, and the years the view
   `multi_year_segment_analysis` has columns for (`_20YY` in its definition). If a data year is missing, the stage
   fails: extend the views (migrations 009 / 010) and `find_potential_projects.YEARS` in a new migration first.
2. `REFRESH MATERIALIZED VIEW CONCURRENTLY` `multi_year_segment_analysis` and `multi_year_condition_analysis` (both have
   unique indexes), committing after each.
3. Runs `scripts/find_potential_projects.main([])`, which rebuilds `potential_projects` (`TRUNCATE … RESTART IDENTITY`,
   then insert). It looks for NHS stretches where the raw distress dropped sharply between survey years.

### 3.4 The checks

A **hard** check can't be overridden. A **needs-accept** check passes with `--accept` after review. A failed check
stops the stage before it changes live data, except the family check after stage E's swap (last row).

| Stage | Check | What it measures | Limit | Kind |
|---|---|---|---|---|
| C conflated | `match_rate_<year>` | share of the year's GPS points (start and end) located on the record's own route (`exact` + `prefix`) | ≥ 97% (`MIN_MATCH_RATE`) | needs accept |
| C raw | `raw_rows_<year>` | records placed | > 0 | hard |
| C raw | `raw_placed_rate_<year>` | records placed ÷ records read | ≥ 97% (`MIN_PLACED_RATE`) | needs accept |
| E | `rows` | surveyed rows in the stage table | > 0 | hard |
| E | `unsurveyed_length_matches_milepoints` | Σ `length_miles` vs Σ(`end_mp − begin_mp`) on the fill rows. Its note gives the fill's rows, miles and rows without a joint. | within 0.1% | hard |
| E | `length_matches_milepoints` | the same on the surveyed rows | within 0.1% | hard |
| E | `pct_segments_without_joint` | % of surveyed rows with no `joint_id` | ≤ live + 0.5 pp (`SHARE_SLACK_PP`) | hard |
| E | `pct_segments_without_district` | % of surveyed rows with no `district_code` | ≤ live + 0.5 pp | hard |
| E | `routes_not_on_roads2` | stage route ids absent from roads2 | none that aren't already in the live table | hard |
| E | `network_pct_good` | network % Good of the surveyed rows: the MAP-21 rating of the raw IRI, cracking (`current_crack`, i.e. FHWA), rutting and faulting (`checks.gfp_sql`) on the **system default config's** rating profile, pavement type by surface (`JCP`/`CRC`/`JOINTED`/`CRCP` = RC), weighted by lane-miles (`lanes`, else the default config's `default_lanes`); stage vs live | change ≤ 2 pp (`GOOD_SHIFT_PP`) | needs accept |
| E (transform) | default config's family rules | every stage row matches a rule of the system default config (`families.apply`) | all | hard (the stage fails before the swap) |
| E (after the swap) | family rules of every config | every segment matches a rule | all | hard (`CheckFailed`, but after the swap; 3.3.5 step 8) |
| E2 alone | family rules of the config | every segment matches a rule | all | hard (nothing written for that config) |
| G | survey years in the views | every year in the data has columns in `multi_year_segment_analysis` | all covered | hard (stage fails) |

Stages A, B, D, E1 and F have no checks. D compares its output with the current build only to decide whether to load a
new one. The two length checks compare `length_miles` with the milepoint span it is computed from, so they catch type
or rounding faults, not a missing grid. The live table's statistics come from the same `segment_stats`. Before the first
refresh with the unsurveyed fill, its `unsurveyed_*` baseline is 0.

### 3.5 Safety rules

#### 3.5.1 Back up first: `scripts/backup_pms.py`

```sh
PYTHONPATH=. ./venv/bin/python scripts/backup_pms.py            # local database, all steps
PYTHONPATH=. ./venv/bin/python scripts/backup_pms.py --mmsdev   # also mmsdev's pms_test
PYTHONPATH=. ./venv/bin/python scripts/backup_pms.py --skip verify
```

Output goes to `~/pms_backups/<YYYY-MM-DD_HHMM>/` (`--out` to change), described by `backup_manifest.json`. It needs the
PostgreSQL 16 client (`/opt/homebrew/opt/postgresql@16/bin`, or `PG16_BIN`), because the server is PG 16 and older
`pg_dump` refuses.

| Step | What it does |
|---|---|
| `dump` | `pg_dump -Fc -Z 6` of the local database (the `.env` connection) to `<db>_local.dump`. With `--mmsdev`, also mmsdev's `pms_test`, streamed over ssh from a `postgres:16` container, so nothing is written to mmsdev's disk. Each dump gets a sha256 and a table of contents (`pg_restore --list` → `*.toc.txt`). |
| `verify` | **Restore rehearsal**: each dump is restored (`pg_restore -j 4 --no-owner --no-privileges`) into a scratch database `pms_restore_check` on the local server. For the local dump, the exact row count of every table outside `archive_*` schemas is compared with the source, and any mismatch stops the script. For the mmsdev dump, it only checks that tables were restored. The scratch database is dropped afterwards. `pg_restore` warnings are kept in the manifest. A backup that hasn't restored doesn't count. |
| `archive` | Copies the tables a rebuild replaces into the schema `archive_<YYYYMMDD>` of the local database (`CREATE TABLE AS`): `analysis_segments`, `pavement_joints`, `reconflate_normalized`, `condition_history`, `potential_projects`, `projects`, `routes`, and the two multi-year views as tables, plus the view definitions in `_matview_definitions`. A table already archived that day is not overwritten. It is used for before/after comparisons and quick rollback without a full restore. |
| `files` | Copies the file inputs from the **repo root** (`70.csv`, `2.csv`, `lrs_table.csv`, `intersections.sqlite`, the joints CSVs, `segments_base.csv`, `segment_overlay_output.csv`, `raw_pavements.xlsx`, `scripts/raw_pavements_deduped.xlsx`) and the survey files (`PMS_SURVEY_DIR`, default `~/Downloads/csvs`, `20*.csv`) to `inputs/`, with path, size, sha256 and mtime for each. It doesn't copy a refresh folder. |
| `lrs` | Records the roads2 fingerprint. |

Not archived in-database: `segment_families`, `joint_builds`, `joint_builds_archive`, `joint_crosswalk`,
`conflation_issues`, `data_refresh_log`. They are in the dump.

To restore one table from the archive (in one transaction), then refresh the views:

```sql
BEGIN;
TRUNCATE analysis_segments;
INSERT INTO analysis_segments SELECT * FROM archive_20260924.analysis_segments;
COMMIT;
REFRESH MATERIALIZED VIEW CONCURRENTLY multi_year_segment_analysis;
```

After restoring `analysis_segments`, rerun `python -m pipeline families`: the ids in `segment_families` belong to the
replaced table. Restoring `pavement_joints` also means marking the restored build `current` in `joint_builds` and the
newer one `archived`.

#### 3.5.2 Stage tables and `swap_in`

- `import_pavement_data.create_stage_table` drops and recreates `<table>_stage` as
  `CREATE TABLE … (LIKE <table> INCLUDING ALL)`. It carries the columns, defaults, constraints and indexes; `ON CONFLICT`
  needs the unique ones. Nothing depends on a stage table, so dropping it is safe.
- `import_pavement_data.swap_in` runs `TRUNCATE <table> RESTART IDENTITY` and `INSERT INTO <table> (cols) SELECT cols
  FROM <table>_stage` in the caller's transaction, which commits once.
- **Why not `DROP`**: `TRUNCATE` keeps the table and its OID, so everything that depends on it survives:
  `analysis_segments_cfg` and the multi-year materialized views. The old import's
  `DROP TABLE … CASCADE` silently dropped `multi_year_segment_analysis`. **No import code drops a live table**; only
  `*_stage` tables are dropped.
- Stages C and E are staged and swapped. Stage D replaces `pavement_joints` with `DELETE` + `INSERT` in one transaction
  (`load_build`). Stages E1, E2 and F update in place in one transaction each. Stage B replaces one survey year per
  transaction. Stage G refreshes the views concurrently and rebuilds `potential_projects` with `TRUNCATE` + insert.
- `RESTART IDENTITY` renumbers `analysis_segment_id` on every swap. Runs don't depend on those ids: each run stores
  its starting inventory (`run_snapshots`) and joint build, so Validate replays a run exactly after a refresh.

#### 3.5.3 Schema changes only through migrations

Schema changes are numbered files in `db/migrations/`, applied with `scripts/migrate.py --apply`, each in its own
transaction, and recorded in `schema_migrations` with a checksum. A file changed after it was applied is reported,
never re-run. 001–024 were recorded with `--baseline 024`, and only `.sql` files run (007 is a Python data script).
Apply pending migrations on every environment before running the pipeline there.

The pipeline-related migrations:

| Migration | What it adds |
|---|---|
| 025 | `joint_builds`, `joint_builds_archive`, `joint_crosswalk`, `pavement_joints.build_id` (build 0) |
| 026 | `schema_migrations`, `data_refresh_log`, `conflation_issues`, `analysis_segments.survey_year` / `joint_build_id` |
| 030 | configs; `segment_families` (LIST-partitioned by `config_id`); family columns moved off `analysis_segments`; `analysis_segments_cfg` |
| 031 | the dTIMS inventory columns on `analysis_segments` (`sign_code`, `route_number`, `hpms_*`, `adt_growth_pct/_source`, `patch_*`, `rehab_*`, `inventory_cci`, `raw_*`, `*_source`); starting-state columns on `segment_families` |
| 035 | `supp_code`, `rehab_treatment_id`, `rehab_coverage` |
| 038 | `reconflate_normalized.pct_crack`; `crack_pct_dtims`, `adt_growth_layer2/_future/_district/_event` |
| 039, 041, 056 | recreate `analysis_segments_cfg` (it expands `a.*` when created) for new columns |
| 041 | `fed_aid_code`, `fed_aid_desc` |
| 042 | `configs.min_length_exempt_below` (short joints skip the minimum-length check) |
| 055 | trigger gates on inventory fields (`inv_iri_above`, `patch_pct_min`, `adt_min`) and the MAP-21 class |
| 056 | `analysis_segments.has_survey` (default TRUE), `configs.unsurveyed_policy` (`exclude` / `dtims_defaults`, default `exclude`) |
| 057 | `reconflate_raw`, `analysis_segments.network`, `configs.survey_network`; the view joins each config to its network |
| 059 | `configs.condition_basis` (`segment` / `joint_average`, default `segment`) |
| 060 | `survey_date` on `reconflate_normalized`, `reconflate_raw` and `analysis_segments`; `configs.survey_cutoff_date` (renamed by 062) |
| 062 | `configs.survey_excluded_from` (was `survey_cutoff_date`), `survey_excluded_to`, `survey_excluded_signs` |
| 064 | `analysis_runs.dtims_ref_id` → `dtims_reference_runs`: the dTIMS run a run is compared with (`api/routes/dtims_reference.py`: GET `/api/dtims-reference/runs`, admin PUT `/runs/{run_id}/link`, GET `/runs/{run_id}/comparison`; the run page's **vs dTIMS** tab) |
| 065 | `dtims_reference_run_sections` on real milepoints (`From` / `To` where stored, else `FromMeasure` / `ToMeasure`, which are offsets on a route record that doesn't start at 0), with `paired_route_id` and `lanes_total` |
| 066 | `dtims_reference_run_roads`: a reference run's sections on each AMPS route they cover (own and opposite direction), hashable by route |
| 067 | index on `analysis_segments.committed_project_id` (deleting a project no longer scans every segment) |
| 068 | `configs.milp_min_year_share`: the config's default for MILP-assist's even-spending rule (every year ≥ share × the biggest year); a run's own setting overrides it |

The import code still carries some idempotent DDL: `CREATE TABLE IF NOT EXISTS` for `condition_history`,
`reconflate_normalized` and `analysis_segments`, and `ALTER TABLE … ADD COLUMN IF NOT EXISTS` for columns that
migrations already added. Stage B also runs `ALTER TABLE condition_history DROP CONSTRAINT IF EXISTS
condition_history_segment_id_fkey`. On a migrated database none of it changes anything.

#### 3.5.4 Geocoding only through `lrs/geometry_to_measure.py`

GPS → route + milepoint runs only on roads2, through `lrs.geometry_to_measure.geometry_to_measure`. The pipeline calls it
directly on a database connection, with no HTTP. Its HTTP face is `POST /api/lrs/geometryToMeasure`
(`api/routes/lrs.py`; session or service token `LRS_SERVICE_TOKENS`), which has the same request and response as the
dashcam service it replaced. The endpoint defaults to a 10 m tolerance and the pipeline uses 15 m. Nothing in AMPS
calls an external geocoder. On 500 random 2025 points the new code and the dashcam service gave identical results. On
19,264 records, 99.7% of the new milepoints were within 0.005 mi of the stored ones.

#### 3.5.5 Joints only through `load_build`

Joints come only from LRS layer 70 through `pipeline/joints.py`. They are loaded only by `load_build`, which creates a
new `joint_builds` row and the `joint_crosswalk` from the previous build. Runs store `configuration.joint_build_id`,
and validation translates older builds through the crosswalk (overlaps of at least 5%, composed across builds).
Commitment flags are applied by milepoint, so they don't depend on joint ids either.

#### 3.5.6 Other rules

- Pavement families come only from a config's `pavement_family_rules` (`pipeline/families.py`), written to that
  config's partition; no surface → family mapping is hard-coded.
- Database settings come from `.env` through `api.database`. `import_pavement_data` reads them from there, and
  `lrs.db` swaps in `ROADS_DB_NAME`.

### 3.6 The resulting tables

#### 3.6.1 `condition_history`

One vendor record of one survey year, on the vendor's milepoints. Key `(segment_id, survey_year)`. Columns are listed in
3.3.2. Readers: the multi-year views and stage G's year check. The engine doesn't read it.

#### 3.6.2 `reconflate_normalized`

One vendor record of one survey year on LRS milepoints. Key `UNIQUE (segment_id, survey_year)`. It holds 431,684 rows
for 2020–2025 (conflated).

| Column | Meaning | Source |
|---|---|---|
| `id` | serial (restarts on every swap) | – |
| `segment_id` | the vendor's `Unique` | survey file |
| `route_id` | the vendor's `ROUTEID` | survey file |
| `actual_bmp`, `actual_emp` | conflated: the located pieces over the record's vendor window (min start, max end); raw mode and the NHS gap fill: `BEG_MP`, `END_MP` | stage C |
| `survey_year` | the file name's year | file name |
| `coverage_pct` | the sum of the normalised weights (1.00) | stage C |
| `iri_mean`, `iri_max` | IRI, in/mi | `IRI_MEAN`, `IRI_MAX` |
| `rut_mean` | rut, in | `RUT_MEAN` |
| `faulting` | faulting, in | `Fault_Avg` |
| `fhwa_crack_pct` | FHWA percent cracking | `FHWA_Percent_Cracking` |
| `pct_crack` | the vendor's percent cracking (dTIMS PCRK) | `PERCENT_CRACKING` / `Percent_Cracking` |
| `surface_type` | dominant `SURF_TYPE`, with `JCP` → `JOINTED` and `CRC` → `CRCP` | `SURF_TYPE` |
| `shoulder_type` | dominant `SHLD_TYPE` | `SHLD_TYPE` |
| `iri_grade`, `rutting_grade`, `faulting_grade`, `cracking_grade` | legacy good / fair / poor bands (IRI 95 / 170; faulting 0.10 / 0.15; rut 0.20 / 0.40; cracking 5 / 20 asphalt, 5 / 15 jointed, 5 / 10 CRCP). No reader; the engine and the checks rate with the config's `gfp_profiles`. | `add_gfp` |
| `overall_grade` | always NULL | – |
| `aadt` | always NULL | – |
| `psi`, `rdi`, `sci`, `eci`, `jci`, `csi`, `cci`, `nci` | vendor indices (weighted in conflated mode) | survey file |

#### 3.6.3 `analysis_segments`

One piece of one route of at most 0.1 mi: a grid cell cut at joint and LRS-attribute boundaries. It is the engine's
network, the same for every config. Today it holds 265,590 rows and 23,935.1 mi, all surveyed, with condition from
2024 (19,151 mi), 2025 (4,710 mi) and older years (74 mi). That table was built before migration 056, so it has no
fill rows yet; the next stage E adds them.

| Column | Meaning | Source |
|---|---|---|
| `analysis_segment_id` | serial, renumbered from 1 on every swap | stage E |
| `route_id`, `begin_mp`, `end_mp` | route and LRS milepoints | grid + overlay |
| `length_miles` | `end_mp − begin_mp`, 4 decimals | stage E |
| `lanes` | 2 on every row | stage E grid |
| `has_survey` | TRUE: a surveyed cell; FALSE: the unsurveyed fill | stage E |
| `survey_year` | survey year of the row's condition (NULL on the fill) | `reconflate_normalized` |
| `surface_type` | `ASP`, `JOINTED`, `CRCP`, `OTH`, `CON`, `BRI`, … (NULL on the fill) | `reconflate_normalized` |
| `current_iri`, `current_rut`, `current_faulting` | raw IRI, rut, faulting (NULL = not measured) | `iri_mean`, `rut_mean`, `faulting` |
| `current_crack` | FHWA percent cracking | `fhwa_crack_pct` |
| `current_psi`, `current_rdi`, `current_sci`, `current_eci`, `current_jci`, `current_csi` | vendor indices; NULL filled with 5.0 on surveyed rows; NULL on unsurveyed rows (from the next stage E build: the 2026-09-30 build still has 5.0 there). The dTIMS starting state reads `raw_*`, not these. | `reconflate_normalized`, transform |
| `current_age` | 0 on every row (3.9) | stage E grid |
| `joint_id`, `joint_build_id` | the joint the piece lies in (NULL if none), and its build | overlay op 1 |
| `aadt` | total AADT | layer 2 |
| `aadt_single`, `aadt_combination` | single-unit and combination truck AADT | layer 77 |
| `truck_pct` | `(aadt_single + aadt_combination) / aadt` (0–1), 0 without AADT | stage E |
| `coal_route` | coal-route section number, NULL if none | layer 15 |
| `district_code`, `district_desc`, `district` | district (`district` = code as text) | layer 18 |
| `county_code`, `county_desc` | county | layer 12 |
| `fed_aid_code`, `fed_aid_desc` | Federal Aid type 1–5 | layer 22 (overlay, then E1) |
| `nhs_code`, `nhs_desc` | 1 / 2 / 4 on the NHS, else 0 | E1 from `fed_aid_code` |
| `functional_class`, `functional_class_desc` | national functional class | layer 35 |
| `route_status`, `route_status_desc` | LRS route status | layer 49 |
| `sign_code`, `route_number`, `supp_code` | parts of the route id | E1 |
| `inventory_cci`, `raw_psi … raw_csi` | vendor CCI and indices as delivered (NULL = not measured) | E1 |
| `crack_pct_dtims` | the vendor's PERCENT_CRACKING | E1 |
| `adt_growth_layer2`, `adt_growth_future`, `adt_growth_district`, `adt_growth_event`, `adt_growth_pct`, `adt_growth_source` | annual ADT growth facts, percent | E1 (layer 2) |
| `rehab_year`, `rehab_project_id`, `rehab_treatment_id`, `rehab_coverage`, `rehab_source` | latest CLOSED project over the segment | E1 (`projects`) |
| `iri_source`, `rut_source`, `flt_source` | `survey` or `dtims_default` | E1 |
| `is_committed`, `committed_treatment_id`, `committed_program_year`, `committed_project_id` | commitment flags | F |
| `hpms_flag`, `hpms_source` | legacy (migration 031 only; the `HPMS_1` route group replaces it) | – |
| `patch_l`, `patch_m`, `patch_h` | patching (sq ft): the stored dTIMS section's Patch_L / Patch_M / Patch_H × the segment's share of the section's length, so each segment carries its section's patching %; NULL off any section | stage F2 `patching` |
| `inventory_rehab_type` | always NULL | – |

#### 3.6.4 `segment_families`

One analysis segment in one config. Primary key `(config_id, analysis_segment_id)`, LIST-partitioned by `config_id`
(`segment_families_c<id>`). It has no foreign key to `analysis_segments`, which is why the swap can truncate it and E2
must rebuild the partitions. The view `analysis_segments_cfg` joins it to `analysis_segments`, and the engine loaders
and pages read that view, always with `config_id`.

| Column | Meaning | Source |
|---|---|---|
| `family_id` | `<pavement>_<rehab>_<truck>`, e.g. `BC_Initial_L` | first matching rule, rehab type from the latest CLOSED project where it counts |
| `pavement_type` | BC asphalt / RC concrete / OT other | family |
| `rehab_type` | Initial / Minor / Major | family or project |
| `truck_load` | H / L | family |
| `current_cci` | starting CCI: the vendor's CCI (0 if none); 99 on unsurveyed rows under `dtims_defaults`; NULL on them under `exclude` | `initial_state` |
| `age_psi … age_csi`, `age_cci` | starting ages (fractional years) | `initial_state` |
| `cnd_psi … cnd_csi` | starting indices at `start_year` | `initial_state` |
| `init_iri`, `init_rut`, `init_pcrk`, `init_flt` | starting raw distress | `initial_state` |
| `init_gfp` | starting MAP-21 class (G / F / P) | `classify_gfp` |
| `age_basis` | `rehab_year` or `no_rehab` | `initial_state` |
| `start_year` | the year the state is for (the config's `start_year`, else the year of the rerun) | `run_spec.resolve_start_year` |

Runs compute their own starting state at their own start year. These stored values are what the browse pages show for
the config.

#### 3.6.5 Joint tables

| Table | One row is | Key columns |
|---|---|---|
| `pavement_joints` | one joint of the current build | `joint_id`, `route_id`, `begin_mp`, `end_mp`, `length_mi`, `parent_joint_id`, `sub_joint_id`, `source_object_id` (the layer-70 OBJECTID), `termini_routeid`, `termini_aadt`, `termini_label`, `build_id`; `segment_count` is 0 |
| `joint_builds` | one build | `build_id`, `status` (`current` / `archived` / `failed`), `lrs_snapshot` (roads2 fingerprint), `inputs` (files with sha256), `parameters` (algorithm constants), `n_joints`, `notes` |
| `joint_builds_archive` | one joint of any build | `(build_id, joint_id)`, route, milepoints, parent, termini |
| `joint_crosswalk` | one old joint → one new joint it overlaps | `old_build_id`, `old_joint_id`, `new_build_id`, `new_joint_id`, `overlap_mi`, `share_of_old` |

#### 3.6.6 `conflation_issues`

One reason for one route in one survey year. Columns: `id`, `refresh_id`, `survey_year`, `route_id` (NULL on summary
rows), `reason`, `records`, `created_at`. Each stage C run replaces the rows of the years it loads.

| Reason | Mode | `records` counts |
|---|---|---|
| `fallback_route` | conflated | records with a point located on another route (kept) |
| `not_located` | conflated | records dropped: start or end not located |
| `route_dropped_span_gt_1mi` | conflated | records of a route dropped because one record spanned > 1 mi |
| `nhs_gap_as_is` | conflated, newest year | records loaded as delivered on an NHS gap |
| `raw_no_route`, `raw_not_on_roads2`, `raw_no_milepoints`, `raw_zero_length`, `raw_outside_roads2_extent`, `raw_duplicate_record` | raw | records dropped, by reason |
| `raw_mode_placed` | raw | records placed (route NULL) |
| `summary` | both | GPS points read (conflated) or records read (raw) |

#### 3.6.7 Useful queries

```sql
-- The last refresh, stage by stage
SELECT stage, status, finished_at - started_at AS took, counts, checks
  FROM data_refresh_log
 WHERE run_label = (SELECT run_label FROM data_refresh_log WHERE stage LIKE '_\_%' ORDER BY refresh_id DESC LIMIT 1)
 ORDER BY refresh_id;

-- What conflation dropped, by year and reason
SELECT survey_year, reason, count(*) AS routes, sum(records) AS records
  FROM conflation_issues WHERE reason <> 'summary' GROUP BY 1, 2 ORDER BY 1, 2;

-- Surveyed and unsurveyed network, and how old the condition is
SELECT has_survey, survey_year, count(*), round(sum(length_miles), 1) AS miles
  FROM analysis_segments GROUP BY 1, 2 ORDER BY 1, 2;
```

### 3.7 The AMPS network compared with dTIMS's

- **dTIMS** builds its analysis inventory from every road in the LRS (its Base table is roads2) and keeps the sign
  systems 1, 2, 3, 4, 7 and 8. Sections the survey never covered keep dTIMS's defaults (CCI 99, IRI 0, cracking 0) and
  rate Good.
- **AMPS** builds `analysis_segments` from the survey (`reconflate_normalized`), then adds the 0.1-mi cells of every
  roads2 route on the same six sign systems that the survey doesn't cover (`has_survey` FALSE, stage E step 3). Before
  migration 056 the fill didn't exist, and about 16,000 mi of that road was missing, mostly county routes and HARP.
  At the time of writing, roads2 has 39,912 route-miles on those sign systems (Interstate 1,320; US 4,129; WV 4,204;
  County 29,108; FANS 283; HARP 868), and the surveyed network is 23,935 mi.
- **Whether runs use unsurveyed road is a config decision**, `configs.unsurveyed_policy`:
  - `exclude` (default; every config today): `engine/db.py` loads only `has_survey` rows, the New Run segment count
    in `api/routes/runs.py` filters the same way, and the config's stored starting state is NULL on unsurveyed rows;
  - `dtims_defaults`: unsurveyed rows are in runs, starting as dTIMS starts them (CCI 99, PSI and RDI at the index
    floor, other indices 0, IRI, rut and cracking 0), which rates them Good. That is a modelling convention, not a
    measurement.
- **Other differences that follow from the inputs:**
  - AMPS carries condition where the survey was **conflated** onto the LRS. dTIMS reads each record on the vendor's
    route and milepoints. Raw mode reproduces dTIMS's reading, and the NHS gap fill does so for NHS stretches that
    conflation leaves empty.
  - Joints exist only on routes in the `routes` table (15,124 routes; none on HARP). Unsurveyed road on other routes
    has no `joint_id`, so the optimizer can't select it, even under `dtims_defaults`. Stage E's
    `unsurveyed_length_matches_milepoints` note reports how many fill rows lack a joint.
  - Under the shipped family rules (migration 029), a NULL surface type falls in the "other or unknown surface" rules,
    so unsurveyed rows are classified `OT_Initial_H` / `OT_Initial_L`. The surface codes `CON` (119 rows) and `BRI`
    (5 rows) are in neither the concrete nor the other list and fall to the asphalt catch-all.

### 3.8 Operating it

Run from the repo root on a machine with the database tunnel (`./start-dev.sh`), `lrsops` on the `PATH` (stage A and
the stage E overlay) and the survey files. Back up and migrate first:

```sh
PYTHONPATH=. ./venv/bin/python scripts/backup_pms.py            # --mmsdev to include pms_test
PYTHONPATH=. ./venv/bin/python scripts/migrate.py --apply
```

**Full refresh**, with a new LRS download and every survey year (conflated):

```sh
PYTHONPATH=. ./venv/bin/python -m pipeline all \
    --survey-dir ~/Downloads/csvs --refresh-dir refresh/$(date +%F)
```

**The same on LRS files already on disk** (to reproduce a build, or without access to R&H):

```sh
PYTHONPATH=. ./venv/bin/python -m pipeline all --survey-dir ~/Downloads/csvs \
    --refresh-dir refresh/$(date +%F) --reuse-lrs .
```

**Dry run** (reads and logs, changes nothing):

```sh
PYTHONPATH=. ./venv/bin/python -m pipeline all --survey-dir ~/Downloads/csvs --dry-run
```

**Build or refresh the raw network** (survey as delivered), on an existing refresh folder. It adds or replaces only the
raw network (`reconflate_raw`, the `raw` rows of `analysis_segments`); the conflated network, its segment ids and its
family rows stay as they are. Then set a config's `survey_network` to `raw` to use it — no further rebuild. Include
`commitments` so the new rows get their flags:

```sh
# every year, as delivered
PYTHONPATH=. ./venv/bin/python -m pipeline conflate segments commitments \
    --survey-dir ~/Downloads/csvs --survey-mode raw --refresh-dir refresh/<run>

# only the newest file (the rest of the network becomes unsurveyed fill; see 3.3.3)
PYTHONPATH=. ./venv/bin/python -m pipeline conflate segments commitments \
    --survey-dir ~/Downloads/csvs --survey-mode raw --raw-latest-only --refresh-dir refresh/<run>

# preview the placement and checks only
PYTHONPATH=. ./venv/bin/python -m pipeline conflate --survey-dir ~/Downloads/csvs \
    --survey-mode raw --raw-latest-only --dry-run
```

**Switch a config between the networks**: set `survey_network` (`conflated` / `raw`) on the Config page's Policy tab
or the workbook's Model Constants sheet. Nothing is rebuilt. Runs made earlier replay from their stored starting
inventory (`run_snapshots`), so they keep the network they were made on. A run's `segment_filter` that queries
`analysis_segments` directly (a sub-query) sees both networks, so filter it on `network` too.

**Refresh the conflated network** (new survey files) on the same folder; the raw network is left as it is:

```sh
PYTHONPATH=. ./venv/bin/python -m pipeline conflate segments commitments derived \
    --survey-dir ~/Downloads/csvs --refresh-dir refresh/<run>
```

**After loading new CLOSED projects** (`scripts/import_past_projects.py`), or a new `2.csv` / `22.csv`: refill the
rehab years and inputs, then every config's starting state:

```sh
PYTHONPATH=. ./venv/bin/python -m pipeline inputs families
```

**One config's families**, after editing its rules or curves outside the app:

```sh
PYTHONPATH=. ./venv/bin/python -m pipeline families --config 2 --dry-run   # preview
PYTHONPATH=. ./venv/bin/python -m pipeline families --config 2
PYTHONPATH=. ./venv/bin/python -m pipeline families                        # every config
```

**Joints only, then the segments on them:**

```sh
PYTHONPATH=. ./venv/bin/python -m pipeline joints segments commitments --refresh-dir refresh/<run>
```

**Commitment flags only** (e.g. after committing projects outside Validate):

```sh
PYTHONPATH=. ./venv/bin/python -m pipeline commitments
```

**Adding a survey year:** put `<YYYY>.csv` in the survey folder, add the year's columns to the multi-year views in a new
migration (009 / 010 define them) and to `find_potential_projects.YEARS`, then run `all`. Stage G refuses a year the
views don't cover.

**After a refresh**, read the log (3.6.7). A needs-accept check that failed shows its value, baseline and limit.
Rerun with `--accept` only after review. A full refresh of 2020–2025 takes about an hour, most of it stage C (about
0.9 million GPS points).

### 3.9 Known gaps in the current ingestion

Facts in the code that a reader of the tables should know. Each is either a limit or an open point.

- `analysis_segments.lanes` is 2 on every row: no stage reads a lane count (the survey's `THROUGH_LANES` isn't used).
- `analysis_segments.current_age` is 0 on every row. The transform only computes it when the column is missing, and the
  grid always provides it.
- Patching comes from dTIMS's network (stage F2 `patching`, the stored `dtims_reference_network_elements` Patch_L / M / H),
  not from the survey files' `PATCH_L/M/H`, so it covers the sections of dTIMS's pavement analysis network only.
- `condition_history.crack_percent` is empty for 2020–2022 because stage B doesn't rename `Percent_Cracking`
  (`reconflate_normalized.pct_crack` has those years).
- `reconflate_normalized.overall_grade` and `.aadt` are always NULL. The four grade columns have no reader.
- `hpms_flag` / `hpms_source` were filled once by migration 031 and aren't written by any stage. After the next swap
  they are NULL. `inventory_rehab_type` is cleared by E1 and never set.
- The unsurveyed fill's index columns (`current_psi … current_csi`) are 5.0, not NULL, because the transform fills
  every NULL index with 5.0. The starting state doesn't read them (it reads `raw_*`), but the column comment of
  migration 056 says they are NULL.
- When several committed projects overlap a segment, which one sets its flags isn't defined (3.3.8).
- A stage E family failure happens after the swap (3.3.5, step 8), although the runner's message says live data wasn't
  changed.
- Stages B and C read every `*.csv` in the survey folder, so a file that isn't `<YYYY>.csv` breaks them.

---

## 4. Configurations and engine parameters

### 4.1 What a configuration is

A **configuration** (`configs` row, migration 030; `api/configs.py`, `engine/config.py`) is the complete set of engineering rules the PMS engine runs with. Everything that is WVDOT policy, rather than an operator of the model, lives in the config's rows. The engine code keeps only the operators: curve formulas, the reset-operation and route-group vocabularies, benefit integration and the solvers.

A config owns:

- **Its model constants and input policy**: 16 columns of `configs` (section 4.6.1).
- **Its sub-tables.** Every row carries `config_id`, and every key includes it. The tables are `treatments`, `treatment_triggers`, `treatment_reset_ops`, `treatment_costs`, `treatment_cost_adjustments`, `treatment_sequencing`, `treatment_counters`, `route_groups`, `route_group_terms`, `cracking_rules`, `condition_initializers`, `project_treatment_map`, `pavement_families`, `pavement_family_rules` and `budget_scenarios`. The list is `api/configs.SUB_TABLES`.
- **Its rating profile**, chosen by `configs.gfp_profile_key`. It points at the read-only system tables `gfp_profiles` and `gfp_profile_thresholds`.
- **Its `segment_families` partition** (`segment_families_c<id>`, LIST-partitioned by `config_id`). This holds each analysis segment's family and its stored dTIMS starting state for this config (section 5.3.4).

`analysis_segments` (the network) is shared by all configs. It has no family or policy columns. Engine and browse reads go through the view `analysis_segments_cfg`, which joins the network to one config's `segment_families`. That view is recreated by migration 056 so that it carries `has_survey`.

**Current configs** (2026-09-30):

| config_id | Name | Notes |
|---|---|---|
| 1 | WVDOT dTIMS (default) | The system default (`is_system_default`, exactly one: unique partial index `configs_one_system_default`); `current_version` 4 |
| 41 | New Test | |
| 166 | pytest workbook … | Test leftover |
| 336 | dTIMS Non-NHS steady state (DEL_STIP_2026) | `start_year` 2026, `crack_source` `dtims_percent`, `min_length_exempt_below` 0 |
| 348 | dTIMS Non-NHS - Fair treatment only | as 336 |

### 4.2 Which config applies

| Caller | Config used |
|---|---|
| A new run (`POST /api/runs`) | The request's `config_id`, else the user's default (`_resolve_run_config`). It is stored in `analysis_runs.config_id` and `configuration.config_id` / `config_name_snapshot`. |
| A finished run's results, Validate, export, run detail | The run's `config_id` at its recorded `config_version` (section 4.4). A run with a NULL `config_id` (from before configs) uses the system default. |
| Browse pages (Segments, project / segment pages, network summaries) | The viewer's default: `app_users.default_config_id` if that config still exists, else the system default (`api/configs.user_config_id`). They also accept `?config_id=`. In local development without sign-in, the default is held in memory per worker (`set_dev_default_config_id`). |
| Engine code | The config pinned for the thread (`engine.compiled.use_compiled`), or `engine.config.use_config(id)`, or an explicit `config_id=`. With none of these, `current_config_id()` falls back to the `PMS_CONFIG_ID` environment variable (scripts), and otherwise **raises**. A new thread starts with no config, so code must set one inside the thread. |

### 4.3 The compiled config: the only reader of policy

`engine/compiled.py` turns a config into one validated, immutable object. **Every consumer reads policy through it**: the loaders in `engine/db.py` return its frames, the condition model gets its `CurveBook` and `ConditionPolicy`, and pricing gets its rate schedule. Greedy, MILP, Validate and the outlooks therefore cannot disagree about eligibility, cost, transitions or ratings.

- **`read_tables(conn, config_id)`** reads the config's name, the 16 constant columns (`CONSTANT_COLS`) and every table in `TABLES` as plain JSON-able rows. Volatile columns (timestamps, serial ids) are left out, so the content hash is stable. `TABLES` lists:
  - `treatments`, `treatment_triggers`, `treatment_reset_ops`, `treatment_costs`, `treatment_cost_adjustments`, `treatment_sequencing`;
  - `pavement_families`, `pavement_family_rules`;
  - `route_groups`, `route_group_terms`, `cracking_rules`, `treatment_counters`, `condition_initializers`, `project_treatment_map`;
  - `gfp_profile`: the thresholds of the profile the config's `gfp_profile_key` names, joined to its label and version.
- `read_tables_cursor` / `compile_cursor` do the same on a psycopg2 cursor. They see the caller's uncommitted writes, so an import or a rules save compiles exactly what it is about to commit.
- **`build(config_id, tables, check=True)`** produces the compiled object:
  - It compiles the route groups (`RouteGroups.from_rows`).
  - It builds the frames. Treatments are sorted by `unit_cost_per_lanemile`. Each trigger gets its effective `min_length_miles` (the branch override, else the treatment's, else 0) and the config's `length_exempt_below`. It also builds the reset ops, sequencing, costs, cost adjustments and family parameters.
  - It runs `validate` (section 4.9) and, with `check=True`, raises `CompileError` (a list of issues) when there are any.
  - It builds the `ConditionPolicy` and the `CurveBook`.
  - It computes `content_hash`: SHA-256 of the JSON of every table and the constants, **without the name**.
- **`CompiledConfig`** carries `config_id`, `name`, `content_hash`, `tables`, `constants`, `route_groups`, `policy`, `book`, `warnings`, `version` and `frames`. It also offers `treatments_df(active_only)`, `triggers_df(ids)`, `ops_df(ids)`, `sequencing_df`, `costs_df`, `cost_adjustments_df`, `family_params_df`, and `rehab_type_of`. That last one maps each treatment id to the rehab type of its unfiltered `REHAB_SET` op, and adds each Hub treatment code in `project_treatment_map` pointing at that treatment's rehab type.
- **Policy defaults inside `_policy`:**
  - An empty cracking-rule set becomes `((None, 0.56),)`.
  - An empty profile or initializer table falls back to the seeds (`engine/policy/seeds.py`). The config check refuses both cases anyway.
  - A stored version without `unsurveyed_policy` (from before migration 056) reads as `exclude`.
  - A version without `min_length_exempt_below` (from before migration 042) reads as 0.
- **Which config a call gets:**
  - **Pinned:** `use_compiled(cfg)` sets a context variable for the thread and also calls `use_config(cfg.config_id)`. `current_compiled(id)` returns the pinned object when its id matches, or when no id is given.
  - **Live:** otherwise `current_compiled` returns the live config compiled with `check=False`, cached per config id. Within 15 s (`_TTL`) the cache is returned as is. After that, a cheap SQL fingerprint of every table and the constant row (`_FINGERPRINT_SQL`: an md5 of md5s; the profile is excluded) is compared, and the config is recompiled only if the fingerprint changed. `clear_cache(id)` drops an entry; the Excel import calls it after applying.
- `engine/policy/seeds.py` holds the seeded policy as Python values. **Runs never read them**; they serve tests and fixtures without a database (`SEED_POLICY`). `tests/engine/test_policy_seeds.py` checks config 1 against them.

### 4.4 Versions, run specs and what a run records

**Config versions** (migration 037, `config_versions`):

- Key `(config_id, version)`, `UNIQUE (config_id, content_hash)`. Other columns: `snapshot` (the `read_tables` output, JSONB), `created_at`, `created_by_name`, `note`.
- `ensure_version(cfg)` takes an advisory transaction lock on (`pms_config_version`, config id). It returns the version whose `content_hash` equals `cfg.content_hash`, or appends `max(version) + 1` with the snapshot. It then sets `configs.current_version`.
- `load_version(config_id, version)` rebuilds a `CompiledConfig` from the stored snapshot with `check=False`, since it already ran once.
- `GET /api/configs/{id}/versions` lists a config's versions with the number of runs on each.
- Config 1 today: versions 1–4. Version 3 was written by `add_fair_treatment.py` "before: Excel import add-fair-treatment.xlsx"; version 4 by run 414.

**A run records** (`api/routes/runs._execute_run`), before any work:

1. `compile_config(config_id)` with `check=True`. A `CompileError` fails the run with `error_detail = {stage: "compile", config_id, issues}`.
2. `ensure_version` → `analysis_runs.config_version`.
3. `engine/run_spec.resolve(cfg, configuration, …)` → `analysis_runs.run_spec`.
4. Both are pinned for the run's thread (`use_compiled`, `use_run_spec`).
5. The starting inventory of the analysed segments is written to `run_snapshots` (`start_state`, Parquet; `row_count`). `engine/db.inventory_columns` lists the columns stored; they include `has_survey` and the rule/gate inputs (`inventory_iri`, `patch_*`).
6. `analysis_runs.gfp_basis = 'map21_raw'`. Runs from before v1.6 carry `'cci_band'`.

**The run spec** (`RunSpec`, `engine/run_spec.py`):

| Field | Source |
|---|---|
| `config_id`, `config_hash`, `config_version` | the compiled config and `ensure_version` |
| `start_year` | override `start_year`, else `configs.start_year`, else the calendar year the run is made |
| `inflation_rate` | override `inflation_rate`, else the config's |
| `discount_rate` | override `discount_rate`, else the config's (no request field sets it; see 4.7) |
| `adt_exponent` | override `power_exponent` or `adt_exponent`, else the config's |
| `benefit_integration` | the config's (no override) |
| `gfp_profile` | the config's `gfp_profile_key` |
| `joint_build_id` | `configuration.joint_build_id`: the current `joint_builds` row at request time |
| `model_version` | `BACKEND_VERSION` |
| `overrides` | the explicit overrides applied, keyed by spec field |

An override counts only when the request set it explicitly and it is not None (`OVERRIDABLE`). A request default must never shadow a config value.

- `resolve_start_year(explicit, cfg)` resolves in this order: the explicit value, then the pinned spec's, then the config's, then today's year.
- `economics(cfg)` returns inflation, discount, ADT exponent and integration: the pinned spec's, else the config's.

**Replay** (`api/validation/context.RunContext`) rebuilds a run with its version (`load_version`), its spec (`RunSpec.from_dict`) and its snapshot (`state_from_inputs`). The "today" mode uses the live config, a spec re-resolved from the run's configuration, and the current inventory. Runs without a snapshot (before v1.7) always use today's inventory.

### 4.5 Lifecycle

| Action | Endpoint / entry point | Rules |
|---|---|---|
| List / read | `GET /api/configs`, `GET /api/configs/{id}` | Anyone. The list returns usage counts: runs, users defaulting to the config, active treatments, family rules, active scenarios. The single read adds the runs that used the config. |
| Create = copy | `POST /api/configs {name, comments, copy_from}` (admin) | `copy_from` defaults to the system default. Names are unique, compared case-insensitively. `copy_config` inserts the `configs` row (copying the 16 constant columns, `copied_from`), copies every `SUB_TABLES` table parents-first (serial ids re-issued: `trigger_id`, `rule_id`, `scenario_id`), and copies the `segment_families` partition (`families.copy_partition`). |
| Rename / comment | `PATCH /api/configs/{id}` (admin) | Always allowed; no lock and no version. |
| Choose your default | `PUT /api/configs/default {config_id}` | Any user. |
| Make system default | `PUT /api/configs/{id}/system-default` (admin) | Clears the old default in the same transaction. |
| Check | `GET /api/configs/{id}/check` | Anyone. Returns `{ok, issues, warnings, content_hash}` (section 4.9). `GET /api/treatments/policy?config_id=` returns the policy tables, the constants and the same check for Config → Policy. |
| Rating profile | `GET /api/configs/{id}/gfp-profile` | The profile's thresholds for the UI (`ui/src/utils/gfpProfile.ts`). |
| Edit through Excel | `GET /api/config/workbook.xlsx?config_id=` → `POST /api/config/workbook/validate?config_id=` → `POST /api/config/workbook/apply?config_id=&diff_hash=` (admin) | Details below. |
| Edit family rules | `GET/PUT /api/pavement-family-rules?config_id=`, `POST …/preview`, `POST …/reclassify` (admin for writes) | Details below. |
| Edit budget scenarios | `/api/budget-scenarios` (create, update, archive, restore) and the workbook's three budget sheets | Always allowed. Not part of the compiled content, no run lock, no version. |
| Delete | `DELETE /api/configs/{id}?delete_runs=N` (admin) | Details below. |

**The edit lock (`api/configs.py`).** Every write to a config's sub-tables goes through these helpers. None of them commits; the caller owns the transaction.

- `check_lock(cur, id)` raises `ConfigLocked` (HTTP 409, `detail.code = "config_locked"`, `running: true`) while any run on the config is `pending` or `running`. Its `delete_runs` argument is accepted from older clients and ignored.
- `lock_for_edit(cur, id, reason=, user_label=)`:
  1. takes `pg_advisory_xact_lock('pms_config_edit', id)`, serialising edits;
  2. calls `check_lock`;
  3. if any run of the config has `config_version IS NULL`, writes a version of the **current** content (`ensure_version(compile_cursor(...))`, note `before: <reason>`) and points those runs at it.

  Since v1.7 every run records its version when it starts, so step 3 only catches runs that somehow lack one. **An edit never deletes or changes a finished run.**
- `touch(cur, id, user)` stamps `updated_at` / `updated_by_name`.

**Excel import** (`api/config_workbook.py`, format version 3):

- **Export.** The workbook has one sheet per table (`SHEETS`) plus a README and a hidden `_meta` sheet (source config, export time, fingerprint of the content). Header cells are blue when editable and grey when read-only.
- **Validate.** Each sheet row is compared with the stored row of the same key. Cells are coerced per `Col`: type, range, length, choices. Read-only cells must be unchanged.
  - Row checks: `_treatment_check`, `_trigger_check`, `_reset_op_check` (= `reset_op_errors`), `_term_check`, `_sequencing_check`, `_band_check`.
  - Then cross-sheet checks.
  - Then `compile_check`: the config the file describes is assembled from the sheets (the profile and anything the workbook doesn't carry come from the database) and run through `engine.compiled.validate`. Its issues are file errors that block the import; its warnings are reported.
  - **Warnings:** the file came from another config; the config changed since the export (the fingerprint differs); `_meta` is missing.
  - **File errors:** a sheet is missing, or the format version is different.
- **`diff_hash`**: md5 of the canonical JSON of the change set (per sheet: update / insert / delete, plus the recomputed configuration of each touched budget scenario). Apply refuses (`LookupError`) unless the recomputed `diff_hash` equals the one the user reviewed.
- **Apply** (`apply_workbook`):
  1. Take `pg_try_advisory_lock('pms_config_import', id)`; if another import holds it, refuse.
  2. Validate again. If any sheet other than the budget sheets changes (`needs_run_lock`), call `check_lock`.
  3. In the write transaction, re-check the fingerprint (refuse if the config changed meanwhile), call `lock_for_edit` when needed, write the changes, `touch`, and insert `config_imports` (`file_sha256`, `exported_at`, `diff_hash`, `summary`, `changes`).
  - Write order: deletes children-first, then updates and inserts parents-first, and deletes on Counters and Route Groups last.
  - New treatment ids also go into `treatment_catalog`.
  - Treatments can't be deleted (set `active` FALSE). Family Curves and Budget Scenarios can't be added or removed. Model Constants and Condition Initializers are values only.
  - **Reclassification.** When family rules, curve coefficients or any `RECLASSIFY_SHEETS` change, the writes run inside `pipeline.families.reclassify` (`on_write`). The config's `segment_families` is then rebuilt from the config as that transaction sees it, and a segment that matches no rule aborts everything. `RECLASSIFY_SHEETS` are Family Rules, Family Curves, Reset Operations, Route Groups, Route Group Terms, Cracking Rules, Condition Initializers, Hub Treatment Map, Model Constants and Counters. `config_imports.reclassify_refresh_id` links the `data_refresh_log` row (stage `E2_families`).
  4. Clear the family-parameter and compiled caches.

**Family rules API** (`api/routes/pavement_family_rules.py`):

- `preview` classifies without writing.
- `PUT` validates the rule set (`families.validate_rules`), refuses with 422 if a preview leaves segments unmatched, then in one transaction: `lock_for_edit` → replace the config's rules → `touch` → `reclassify`.
- `POST /reclassify` reruns the saved rules.
- `reclassify` takes `pg_try_advisory_xact_lock('pms_family_reclassify', id)` and logs `data_refresh_log` stage `E2_families`.

**Deletion** (`DELETE /api/configs/{id}`):

- The system default can't be deleted (409).
- `delete_runs_for_config_delete` takes the edit lock and refuses while a run is running. If runs used the config, it refuses (409, listing them) unless `delete_runs` equals their number.
- On confirmation it clears `projects.source_run_id` for those runs, deletes the runs (their `run_logs`, `run_plan_edits` and `run_plan_state` cascade), and logs `config_run_deletions`.
- `delete_config` then drops `segment_families_c<id>` and deletes the `configs` row. Sub-tables and `config_versions` cascade.
- Users whose default was this config fall back to the system default when their default is next resolved.
- **Only deleting a config deletes runs.**

### 4.6 Parameter reference

"Config 1" is the live value on 2026-09-30. "Read by" names where the engine consumes the value.

#### 4.6.1 Model constants and input policy (`configs` columns)

All 21 columns are in `CONSTANT_COLS`, copied with a config, in the content hash, and on the workbook's **Model Constants** sheet (one row).

| Column | Meaning | Default (DB) / config 1 | Allowed | Read by |
|---|---|---|---|---|
| `adt_exponent` | Exponent p of the benefit's traffic weight: each year's CCI gain × ADT(t)^p × length | 0.2 / 0.2 | DB ≥ 0; workbook 0–2 | `run_spec.adt_exponent` (overridable) → `engine/benefits/auc.py` (`weighted_gain`); runs pass it as `power_exponent` |
| `discount_rate` | Benefit discounting per year, (1 + r)^−t | 0.04 / 0.04 | DB 0 ≤ r < 1; workbook 0–0.5 | `run_spec.discount_rate` → `auc.py`; MILP `milp_cost_basis = present_value` |
| `inflation_rate` | Cost inflation per year, (1 + i)^(year − 1) | 0.02 / 0.02 | DB > −1; workbook −0.5–0.5 | `run_spec.inflation_rate` (overridable) → `engine/optimization/cost.py`, every optimizer |
| `benefit_integration` | Weights of the benefit sum over t = 0…horizon: `trapezoid` halves the first and last year, `sum` weights every year 1 | `trapezoid` / `trapezoid` | `trapezoid`, `sum` (DB check) | `run_spec.benefit_integration` → `auc.py` |
| `start_year` | Program year 1 as a calendar year; blank = the year the run is made | NULL / NULL (336, 348: 2026) | NULL or 2000–2100 | `run_spec.resolve_start_year` → starting state, pricing base; the stored browse state (`segment_families.start_year`) |
| `default_lanes` | Lanes assumed where the inventory has none (≤ 0 or NULL) | 2 / 2 | DB > 0; workbook 1–12 | `ConditionPolicy.default_lanes` (lane-miles for GFP shares); `cost.Pricing.default_lanes` (price) |
| `index_lower_bound` | Floor of a projected index | −1 / −1 | workbook −5–0 | `ConditionPolicy.lower_bound` → `idx_floor` column → `dtims_state.step` |
| `max_start_age` | Cap on the starting age min(start − rehab year, cap) | 15 / 15 | DB ≥ 0; workbook 0–100 | `initial_state` |
| `missing_rehab_age` | Starting age where no rehab year counts | 15 / 15 | DB ≥ 0; workbook 0–100 | `initial_state` |
| `min_qualifying_fraction` | Share of a joint's length whose segments must pass a treatment's branch | 0 / 0 | 0–1 | **Not read by runs.** `evaluate_triggers_segment_union_polars` takes it, but `chunked.prepare_strategies_chunked` → `_prepare_strategies_segment_union` never passes it, so it is always 0. |
| `min_rehab_coverage` | A CLOSED project sets a segment's rehab year (and rehab type) only when it covers at least this share of the segment; rows without a coverage keep their year | 0.5 / 0.5 | 0–1 | `dtims_state._apply_input_policy`; `families.classify` (rehab type) |
| `adt_growth_fallback` | Order of ADT growth sources, comma-separated: `layer2` (`adt_growth_layer2`), `layer2_future` (`adt_growth_future`), `district_median` (`adt_growth_district`), `zero` | `layer2,layer2_future,district_median,zero` / same | Those four words, at least one (config check) | `_apply_input_policy` → `adt_growth_pct` (first non-null; 0 if `zero` is listed; a null growth is treated as 0 by `step`) |
| `crack_source` | Starting cracking measure: `fhwa` = `current_crack` (FHWA_Percent_Cracking); `dtims_percent` = `crack_pct_dtims` (PERCENT_CRACKING) where measured, else `current_crack` | `fhwa` / `fhwa` (336, 348: `dtims_percent`) | `fhwa`, `dtims_percent` (DB check) | `_apply_input_policy` |
| `gfp_profile_key` | The Good / Fair / Poor profile | `MAP21_2017` / `MAP21_2017` | A `gfp_profiles` key; the profile must be complete (config check) | `ConditionPolicy.gfp`; recorded in `run_spec.gfp_profile` |
| `min_length_exempt_below` | Joints shorter than this (mi) skip every treatment's minimum length (migration 042); 0 = no exemption | 0.5 / 0.5 (336, 348: 0) | DB ≥ 0; workbook 0–10 | `compiled._frames` → trigger `length_exempt_below` → `triggers._length_ok` |
| `survey_network` | Which survey network the config's runs and pages read (migration 057): `conflated` = the GPS-conflated survey (`reconflate_normalized`); `raw` = the survey as delivered on the vendor's route and milepoints (`reconflate_raw`). Both are kept in `analysis_segments` (`network`), so switching is a config edit, not a rebuild; the chosen network must have been built (3.3.2, 3.3.5) | `conflated` / `conflated` (336: `raw` for the dTIMS comparison) | `conflated`, `raw` (DB check and config check) | `analysis_segments_cfg` (joins `a.network = c.survey_network`) → every loader, Validate, the condition and family-rule pages |
| `condition_basis` | Starting condition (migration 059): `segment` = each segment from its own survey; `joint_average` = the joint's survey averaged by length over its latest survey year and given to every segment of the joint, unsurveyed ones included, as dTIMS starts a section (5.4.1) | `segment` / `segment` (336: `joint_average`) | `segment`, `joint_average` (DB check and config check) | `dtims_state._apply_input_policy` → `_joint_average` (runs, replays, `families.init_condition`); `engine/db.survey_scope_sql` |
| `survey_excluded_from`, `survey_excluded_to`, `survey_excluded_signs` | Survey counted as not delivered (migrations 060, 062): dated from … to (`YYYY-MM-DD`; blank to = no end) on the listed sign systems (comma-separated; blank = all). The segment starts as road without survey data (5.4.1) | blank / blank (336: `2024-11-01`, `2024-12-31`, `4`) | dates or blank; `to` needs `from` (DB checks and config check) | `dtims_state._apply_input_policy` → `_survey_excluded`; `engine/db.survey_scope_sql` |
| `unsurveyed_policy` | LRS road without survey data (`analysis_segments.has_survey` FALSE): `exclude` = not loaded into runs, no stored starting state; `dtims_defaults` = loaded and started as dTIMS starts no-data sections (section 5.4.8) | `exclude` / `exclude` (every config) | `exclude`, `dtims_defaults` (DB check and config check) | `engine/db.load_analysis_segments_df` (`AND has_survey`); `families.init_condition`; `runs.py` segment count |

`configs` also has metadata that is not compiled: `name` (unique), `comments`, `created_by`, `created_by_name`, `created_at`, `updated_at`, `updated_by_name`, `copied_from`, `is_system_default` and `current_version`.

#### 4.6.2 Treatments (`treatments`, key `(config_id, treatment_id)`)

| Column | Meaning | Read by |
|---|---|---|
| `treatment_id` | Id: letters, digits, `_`, `-`. Also in the global `treatment_catalog` (the FK target of projects and results). | everything |
| `treatment_name`, `description`, `color`, `treatment_order` | Display. `treatment_order` is the display / severity order. | UI, exports |
| `active` | Only active treatments are loaded by runs (`treatments_df(active_only=True)`) and checked for rates, ops and triggers | compiled, loaders |
| `budget_category` | `PRESERVATION` / `REHABILITATION` / `RECONSTRUCTION`. Lower-cased where it is read. | mix floors (report), network-target boost scope |
| `pavement_type_applicable` | BC / RC / OT, or NULL = any. Must equal both the joint's length-dominant pavement type and the segment's own. | `triggers.py` `_ptype_ok` |
| `unit_cost_per_lanemile` | **Display rate only.** Runs price with `treatment_costs`. Frames are sorted by it. | UI |
| `service_life_years`, `alpha_post`, `beta_post` | Legacy; not read by the dTIMS model | — |
| `interval_years` | Years before the **same** treatment again (dTIMS IntervalYear): `year − yr_<id> ≥ interval` | `triggers._gate_exprs` |
| `min_length_miles` | Minimum joint length (mi). A branch's `min_length_override` replaces it. Skipped for joints shorter than `min_length_exempt_below`. | `_frames`, `triggers._length_ok` |
| `require_route_group` | Only on segments in this route group (`rg_<KEY>`) | `_gate_exprs` |
| `exclude_route_group` | Never on segments in this route group | `_gate_exprs` |
| `adt_max` | Only where the **modeled** (grown) ADT is strictly below this | `_gate_exprs` |
| `lanes_max` | Only where lanes ≤ this; unknown lanes pass | `_gate_exprs` |
| `committed_only` | Never an ordinary candidate; applied only as a committed project. Exempt from the trigger-branch requirement. | `triggers` (filtered out), config check |
| `min_years_since_last` | Wait after **any** treatment: `year − last_applied_year ≥ value`; a never-treated joint passes | `_gate_exprs` |

Config 1 active treatments:

| Treatment | Pave | Display $/ln-mi | Interval | Min length | Gates |
|---|---|---|---|---|---|
| CRACK_SEAL | BC | 2,217.6 | 3 | 0.5 | |
| SAW_SEAL_JOINTS | RC | 369,600 | 6 | 3.0 | |
| CAPE_SEAL | BC | 99,000 | 3 | 0.5 | exclude `INTERSTATE` |
| CHIP_SEAL | BC | 45,000 | 3 | 0.5 | exclude `INTERSTATE`, ADT < 1,000, lanes ≤ 1 |
| MICROSURFACING | BC | 103,000 | 2 | 3.0 | |
| ULTRA_THIN_OVLY | BC | 165,000 | 4 | 0.5 | committed only |
| THIN_OVERLAY | BC | 220,000 | 2 | 0.5 | |
| THICK_OVERLAY | BC | 300,000 | 2 | 0.5 | |
| FAIR_TO_GOOD | any | 300,000 | 0 | 0.0 | (added 2026-09-30; branches on MAP-21 Fair) |
| MINOR_CPR_DG | RC | 180,000 | 6 | 3.0 | |
| MAJOR_CPR_DG | RC | 1,500,000 | 6 | 3.0 | |
| RECONSTRUCT_BC | BC | 1,360,000 | 4 | 0.5 | require `IM_FUNDS` |
| RECONSTRUCT_RC | RC | 1,360,000 | 4 | 0.5 | require `IM_FUNDS` |

PRESERVATION_BC and PRESERVATION_RC are inactive (`min_years_since_last` 6). Fourteen older rows (RECONSTRUCT, MILL-OVLY-2, …) are inactive legacy ids.

#### 4.6.3 Trigger branches (`treatment_triggers`, unique `(config_id, trigger_key)`)

A treatment is a candidate on a joint when **any** of its branches passes on a member segment **and** every gate passes (`engine/treatments/triggers.evaluate_triggers_segment_union_polars`, `_gate_exprs`).

| Column | Meaning |
|---|---|
| `trigger_key`, `treatment_id`, `trigger_branch` | Key, owner, branch number (1–99) |
| `pavement_type` | BC / RC / OT, or NULL = any. Must equal the joint's length-dominant type **and** the segment's own. |
| `psi_lower` … `jci_upper` (PSI, RDI, SCI, CSI, ECI, JCI) | Inclusive windows `[lower, upper]`; −99 / 99 = open. All six must pass. |
| `cci_lower`, `cci_upper` | Optional inclusive CCI window (NULL = no gate) |
| `min_length_override` | This branch's minimum joint length; NULL = the treatment's |
| `branch_kind` | `window` (index windows only) or `years_since` (also the years since the latest listed treatment must be in `[years_since_min, years_since_max]`; a joint that never had one of them fails) |
| `years_since_min`, `years_since_max`, `years_since_trts` | For `years_since`: the range and a comma-separated list of treatment ids (each must exist) |
| `counter_name`, `counter_max` | Optional: the named counter's current value ≤ `counter_max` (counter NULL counts as 0). **A DB CHECK allows only `cnt_chip` and `cnt_micro`.** |
| `gfp_class` (055) | Optional: the segment's MAP-21 class **this year** (rated from the modeled raw distress) must be G, F or P |
| `inv_iri_above` (055) | Optional: the **inventory** IRI (survey value as loaded, `inventory_iri`) must be strictly above this; it does not move with the model |
| `patch_pct_min` (055) | Optional: inventory patching (patch_l + patch_m + patch_h, sq ft) ÷ (length_miles × 5280 × 8) × 100 must be ≥ this. Patching is loaded by stage F2 `patching` from dTIMS's network; segments off it have none, so the branch fails there. |
| `adt_min` (055) | Optional: the **inventory** AADT (not grown) must be ≥ this |
| `description` | Free text |

A missing value fails any of the 055 gates. `clamp_trigger_lowers` (section 4.7) rewrites the six index lower bounds to 0 at load time.

Config 1 examples:
- Reconstruction on BC: PSI 0–1, or ECI 0–1, or SCI ≤ 1 with ECI ≥ 0.
- Reconstruction on RC: PSI, CSI or JCI 0–1.
- MICRO_YEARS: `years_since` 5–7 after thin overlay, thick overlay or either reconstruction.
- Counter limits: CHIP_SEAL_1 `cnt_chip` ≤ 2; MICRO_1 `cnt_micro` ≤ 1.
- FAIR_GFP_BC / RC / OT: every window open, `gfp_class` F.
- The config check warns that CRACK_SEAL_1 (CSI 4.3–4.5 on BC) and PRESERVATION_1 (CSI 3.5–4 on BC) can never trigger.

#### 4.6.4 Reset operations (`treatment_reset_ops`, key `(config_id, treatment_id, op_order)`)

These are ordered steps run by `dtims_state.apply_treatments`. Section 5.8 has the exact expressions.

| Column | Meaning |
|---|---|
| `op_order` | Execution order (ascending) |
| `op` | One of 18 operations (DB CHECK, migration 055): `IDX_SET`, `IDX_ADD_CAP`, `IDX_FLOOR`, `IDX_FROM`, `CCI_FROM_MIN`, `AGE_SET`, `AGE_INVERSE`, `HOLD_SET`, `IRI_MIN_PSI`, `IRI_FROM_PSI`, `PCRK_MIN_AGE`, `PCRK_FROM_AGE`, `RUT_FROM_RDI`, `FLT_SET`, `CNT_SET`, `CNT_INC`, `PAVE_SET`, `REHAB_SET` |
| `target` | An index (`cci psi eci sci rdi csi jci`) for the `IDX_*`, `AGE_*` and `HOLD_SET` ops (`HOLD_SET` only `cci csi eci jci sci`). A counter for `CNT_*`. The fixed name (or blank) for the raw / family ops: `cci`, `iri`, `pcrk`, `rut`, `flt`, `pave`, `rehab`. |
| `value` | Numeric argument; required by `IDX_SET`, `IDX_ADD_CAP`, `IDX_FLOOR`, `IDX_FROM`, `CCI_FROM_MIN`, `AGE_SET`, `HOLD_SET`, `FLT_SET`, `CNT_SET`, `CNT_INC`. Workbook range −99…99. |
| `value_text` | `BC` / `RC` for `PAVE_SET`; `Initial` / `Minor` / `Major` for `REHAB_SET` |
| `source` | The source index of `IDX_FROM` |
| `pave_filter` | BC / RC: the step applies only to rows of that pavement type (the treatment is applied joint-wide; each member follows its own pavement's steps) |
| `description` | Free text |

Seeds: `engine/condition/dtims_ops.DEFAULT_RESET_OPS` (14 treatments, migration 032). `describe_op` gives the plain-English text used on the Config page.

#### 4.6.5 Costs

| Table | Columns | Meaning |
|---|---|---|
| `treatment_costs` | `treatment_id`, `pavement_type` (BC / RC / OT), `cost_per_lane_mile` (≥ 0) | $ per lane-mile by the segment's pavement type **before** treatment. Anything not BC / RC prices as OT. Every active treatment needs all three (config check). |
| `treatment_cost_adjustments` | `treatment_id`, `route_group`, `multiplier` (≥ 0; workbook ≤ 100) | Multiplies the rate on segments in the route group. Every matching adjustment applies. Config 1: THICK_OVERLAY × 1.2 and FAIR_TO_GOOD × 1.2 on `INTERSTATE`. |

Cost of a project (`engine/optimization/cost.price_segments`) = Σ over member segments of length × lanes (`default_lanes` where unknown) × rate(pavement) × Π adjustments × (1 + inflation)^(year − 1). A missing rate is an error.

Config 1 rates:
- Crack seal: 2,217.6 on BC and OT, 131,577.6 on RC.
- Saw & seal: 0 on BC and OT, 369,600 on RC.
- Every other active treatment: the same rate on all three types (see 4.6.2).

#### 4.6.6 Sequencing (`treatment_sequencing`)

| Column | Meaning |
|---|---|
| `previous_treatment_id` | The joint's last treatment, or `__NONE__` for never treated |
| `allowed_next_treatment_id` | A treatment allowed next. A treatment may follow itself; `interval_years` gates the timing. |
| `sequencing_order` | 1 = preferred (display) |
| `description` | Free text |

Every run applies it. A candidate whose treatment is not listed after the joint's last treatment is dropped.

#### 4.6.7 Pavement families (`pavement_families`, key `(config_id, family_id, index_type)`)

| Column | Meaning |
|---|---|
| `family_id` | `<Pave>_<Rehab>_<Truck>`: BC / RC / OT × Initial / Major / Minor × H / L = 18 families |
| `index_type` | `cci psi eci sci rdi csi jci` (read by the engine) and `nci` (stored, ignored: `CurveBook` keeps only the seven codes) |
| `family_name`, `description`, `pavement_type`, `traffic_level`, `surface_type`, `functional_class` | Labels (`traffic_level` = truck load) |
| `curve_type` | `polynomial`, `linear`, `sigmoid` (supported); `log` (accepted on the sheet; refused by the config check on any index that applies to a reachable family) |
| `alpha` (C1), `beta` (C2), `c3` (C3) | Curve coefficients (section 5.5) |
| `initial_value` | The curve maximum `mx` (NULL → 5; workbook 0–5) |

Config 1: every family has `initial_value` 5, and most curves are quadratic polynomials. The exceptions are:

| Family | Index | Curve | C1 / C2 / C3 |
|---|---|---|---|
| BC_Initial_H | SCI | sigmoid | 85 / 115 / 0.7 |
| BC_Initial_L | ECI | sigmoid | 85 / 120 / 0.6 |
| BC_Major_H | CSI | sigmoid (inapplicable on BC) | 85 / 115 / 0.7 |
| BC_Major_L | JCI | log (inapplicable on BC) | 3.1 / −11.5 / 1.7 |
| RC_Minor_H | CCI, PSI | linear | −0.1 |
| RC_Minor_L | JCI | linear | −0.1 |

#### 4.6.8 Family rules (`pavement_family_rules`, unique `(config_id, priority)`)

| Column | Meaning |
|---|---|
| `priority` | Rules are tried from the lowest up; the first **enabled** match wins |
| `family_id` | The family assigned (it must have curves; `validate_rules`) |
| `match` | `all` / `any` over the top-level conditions |
| `conditions` | JSON list of `{field, op, value}` or groups `{"any": [...]}` / `{"all": [...]}`. `[]` matches everything. |
| `enabled`, `description`, `updated_by` | |

Condition fields (`pipeline/families.FIELDS`):
- text: `surface_type`, `coal_route`, `route_id`;
- number: `truck_pct` (0–1), `aadt`, `aadt_single`, `aadt_combination`, `functional_class`, `nhs_code`, `fed_aid_code`, `district_code`, `county_code`, `route_status`, `lanes`.

Operators: `eq`, `ne`, `in`, `not_in`, `starts_with` (text), `lt`, `lte`, `gt`, `gte` (number), `is_null`, `not_null`. A NULL value satisfies only `is_null`.

Config 1 has the six shipped rules of migration 029:
- 10 `RC_Initial_H`: concrete surface and high truck.
- 20 `RC_Initial_L`: concrete surface.
- 30 `OT_Initial_H`: other or missing surface, and high truck.
- 40 `OT_Initial_L`: other or missing surface.
- 50 `BC_Initial_H`: high truck.
- 60 `BC_Initial_L`: everything else.

"High truck" is `coal_route` not null OR `truck_pct` ≥ 0.10.

#### 4.6.9 Route groups (`route_groups`, `route_group_terms`)

| Table | Columns | Meaning |
|---|---|---|
| `route_groups` | `group_key` (`^[A-Z][A-Z0-9_]*$`), `label`, `match` (`all` / `any`), `description` | A named set of roads |
| `route_group_terms` | `group_key`, `term_order`, `field`, `op`, `value` (JSON), `negate` | One term |

Fields (`engine/policy/route_groups.FIELDS`):
- text: `sign_code`, `route_number`, `route_id`, `supp_code`, `pavement_type`;
- number: `functional_class`, `nhs_code`, `fed_aid_code`, `district_code`, `county_code`, `lanes`, `begin_mp`, `end_mp`.

Ops: `eq`, `ne`, `in`, `not_in` (non-empty list), `between` ([low, high], inclusive), `gte`, `lte`, `prefix` (text only), `in_group` (no field; value = another group key). A NULL field never matches. Cycles are rejected.

One compiler produces both the polars expression (segments carry `rg_<KEY>` columns) and the SQL predicate (`RouteGroups.sql`).

Config 1 groups:
- `INTERSTATE`: sign 1.
- `TURNPIKE_I77`: sign 1, route 77, supplemental 16.
- `TURNPIKE_I64`: route_id `41100640000EB`, begin_mp ≥ 117.93.
- `TURNPIKE`: either Turnpike group (match any).
- `IM_FUNDS`: in `INTERSTATE` and not in `TURNPIKE`.
- `I68`: sign 1, route 68.
- `HPMS_1`: functional class 1–3, the stand-in for dTIMS HPMS = 1.

#### 4.6.10 Cracking rules, counters, initializers, Hub treatment map

| Table | Columns | Meaning / config 1 |
|---|---|---|
| `cracking_rules` | `rule_order`, `route_group` (NULL = default), `factor` (≥ 0), `description` | Cracking growth (% per year of crack age). The first matching rule wins. A default rule is required. Config 1: `INTERSTATE` 0.15, `HPMS_1` 0.37, default 0.56. |
| `treatment_counters` | `counter_key` (`^cnt_[a-z0-9_]+$`), `label` | Counters that resets may set or increase and branches may limit. Config 1: `cnt_chip`, `cnt_micro`. |
| `condition_initializers` | `index_group` (asphalt / concrete), `rehab_type` (Initial / Major / Minor), `new_base`, `drift_a`, `drift_b`, `drift_c` | The dTIMS starting-index initializer (section 5.4.2). All six rows are required. Config 1 in the table below. |
| `project_treatment_map` | `hub_treatment_code`, `treatment_id` | A project's own treatment code (not a config treatment id) → the config treatment whose `REHAB_SET` gives the rehab type. Config 1: empty. |

Config 1 initializers:

| Group | Rehab | new_base | a | b | c |
|---|---|---|---|---|---|
| asphalt | Initial | 5.0 | −0.0266 | 3e−5 | −5e−5 |
| asphalt | Major | 5.0 | −0.1404 | −0.0014 | 4e−5 |
| asphalt | Minor | 4.5 | −0.1289 | −0.002 | 0 |
| concrete | Initial | 5.0 | 0.0026 | −0.0026 | 2e−5 |
| concrete | Major | 5.0 | −0.0291 | −0.0032 | 4e−5 |
| concrete | Minor | 4.5 | 0.0189 | −0.0094 | 1e−4 |

#### 4.6.11 Rating profile (`gfp_profiles`, `gfp_profile_thresholds`)

These are read-only system tables, not config rows. A config picks one profile with `gfp_profile_key`.

| Table | Columns |
|---|---|
| `gfp_profiles` | `profile_key`, `version`, `label`, `is_system`, `description` |
| `gfp_profile_thresholds` | `profile_key`, `pavement_type` (BC / RC / OT), `metric` (`iri`, `rut`, `flt`, `pcrk`), `good_below`, `poor_above` (`good_below ≤ poor_above`), `used` |

`MAP21_2017` ("MAP-21 (23 CFR 490, 2017)", version 1) is the only profile. Section 5.9 has its values. The config check needs all 12 rows (3 pavements × 4 metrics).

#### 4.6.12 Budget scenarios (`budget_scenarios`)

| Column | Meaning |
|---|---|
| `scenario_id`, `name` (unique among active per config), `description` | |
| `configuration` (JSONB, `BudgetScenarioConfiguration`, extra keys forbidden) | `annual_budget` (≥ 0), `analysis_years` (1–50), `budgets_by_year` (calendar year → $; a missing year uses `annual_budget`), `allow_budget_carryover`, `district_balancing` (the `DistrictBalancing` model of 4.8) |
| `archived_at` | Archived instead of deleted |

A scenario is **copied** into a run's request when it is loaded (`budget_scenario`, `allow_budget_carryover`, `constraints.district_balancing`, plus `budget_scenario_id` and `budget_scenario_name_snapshot` for traceability). Editing a scenario later never changes a run. Scenarios are not compiled content: they are outside the hash and the run lock.

### 4.7 Run parameters

**`CreateRunRequest`** (`POST /api/runs`, `api/routes/runs.py`) is stored in `analysis_runs.configuration`.

| Field | Default | Meaning / where read |
|---|---|---|
| `run_name` | NULL | Label |
| `config_id` | The user's default | The config (4.2) |
| `annual_budget` | 50,000,000 | $ per year when `budget_scenario` is absent. Stored as the first year's budget for display. |
| `analysis_years` | 20 (1–50) | Horizon when `budget_scenario` is absent. With one, the horizon is the largest year in it. |
| `budget_scenario` | derived | `[{year, budget}]` with 1-based program years. `_extract_budgets_by_year` is the canonical per-year budget. A missing year has budget 0 in greedy (`budgets_by_year.get(year, 0)`). |
| `budget_scenario_id`, `budget_scenario_name_snapshot` | NULL | Traceability only |
| `power_exponent` | NULL = the config's | Override of `adt_exponent` → `run_spec` |
| `inflation_rate` | NULL (−0.5–0.5) | Override → `run_spec` |
| `start_year` | NULL (2000–2100) | Override → `run_spec` |
| `minimum_bc_ratio` | 0.0 | Minimum incremental B/C for a greedy step. MILP ignores it. |
| `allow_budget_carryover` | FALSE | Unspent budget carries to the next year (greedy). MILP-assist rejects TRUE (422). |
| `lookahead_years` | NULL | Accepted and ignored |
| `segment_filter` | NULL | SQL WHERE on `analysis_segments_cfg`, checked for safety (keywords, comments, `;`). ANDed with the district list of an enabled district balancing. |
| `network_filter` | NULL | UI preset (`all`, `interstate`, `nhs`, `non-interstate-nhs`, `non-nhs`). The UI turns it into `segment_filter`; the engine never reads it. |
| `use_faulting_for_jci` | FALSE | Stored and passed to `ChunkedProcessingConfig`, **but no engine path reads it**; it has no effect. |
| `optimizer` | `greedy` | `greedy` or `milp-assist`. MILP runs only when a network target is set (a Poor or a Good sub-target); otherwise greedy. MILP also needs `highspy`. |
| `constraints` | NULL | `ConstraintsConfig` (4.8), stored with `exclude_none` |

**Configuration keys with no request field.** `runs.py` reads these from `analysis_runs.configuration`, but `CreateRunRequest` has no field for them, and pydantic drops unknown keys. **They cannot be set through `POST /api/runs`**, only by writing the stored configuration directly (scripts):

- `strategy_prep`: default `segment_union`, the only supported value. Anything else raises "not supported", since the joint cascade was removed in v1.7.
- `clamp_trigger_lowers`: FALSE; TRUE rewrites every index lower bound to 0.
- `discount_rate`: `run_spec.OVERRIDABLE` accepts it, but no request field carries it.

**Added by the server:** `config_id`, `config_name_snapshot`, `joint_build_id`, and the Run Assistant's `assistant` tag.

**Fixed engine settings** (`ChunkedProcessingConfig` in `runs.py`):
- `minimum_project_length_miles` = 0.25: joints shorter than this are removed before selection every year;
- `joint_length_miles` = 0.2: only for synthetic joints when no joint ids exist;
- `chunk_size` = 500.

**Request-time checks (422):**
- An enabled network target with `target_year > analysis_years`. `poor_target_year` is not checked.
- `milp_objective = min_cost` without `milp-assist`.
- MILP with carryover, or without `highspy`.

### 4.8 Constraint parameters (`api/schemas/constraints.py`)

`ConstraintsConfig` has extra keys forbidden. `any_enabled()` decides the path:

1. MILP-assist, when `optimizer = milp-assist` and a network target is set.
2. Constrained greedy (`generate_constrained_work_program`), when any sub-constraint is enabled.
3. Plain greedy (`generate_work_program_chunked`) otherwise.

**District balancing** (`DistrictBalancing`):

| Field | Default | Meaning | Read by |
|---|---|---|---|
| `enabled` | FALSE | | |
| `bands[].district_code` | — | The listed districts are the **included network**: `runs.py` ANDs `district_code IN (…)` into the filter | all optimizers (load time) |
| `bands[].ceiling_pct` | NULL (0–1) | Hard: a selection that would take the district above ceiling × the year's budget is vetoed (`check_selection_quotas`) | greedy |
| `bands[].floor_pct` | NULL (0–1; Σ ≤ 1) | Reported in the constraint report only. The floor boost (`district_floor_boost`) is never computed by any caller. | report |
| `penalty_weight` | 1.0 | Not read by the engine | — |

**Network target** (`NetworkTarget`):

| Field | Default | Meaning | Read by |
|---|---|---|---|
| `enabled` | FALSE | Requires (`target_pct_good` + `target_year`) and/or (`max_pct_poor` + `poor_target_year`), each pair set together | both |
| `target_pct_good`, `target_year` | NULL (0–100; ≥ 1) | % Good (MAP-21, lane-miles) floor in program year `target_year` | both |
| `max_pct_poor`, `poor_target_year` | NULL | % Poor ceiling in program year `poor_target_year` | both |
| `max_iterations` | 8 (1–20) | Outer-loop repeats of greedy | constrained greedy |
| `damping` | 0.5 (0.1–10) | boost ← boost × (1 + damping × worst gap (pp) / 100). Rehab / reconstruction benefit × boost; preservation × √boost when a Poor target is set. Stops within 0.5 pp and keeps the best attempt. | constrained greedy |
| `every_year` | FALSE | A Poor ceiling and Good floor row for every year up to the target year | MILP |
| `every_year_from` | 1 | First year of those rows | MILP |
| `milp_objective` | `benefit` | `min_cost`: minimise total cost subject to the target rows; a year's budget of 0 = no limit | MILP |
| `milp_cost_basis` | `nominal` | `present_value`: each cost ÷ (1 + discount)^(year − 1) in the min-cost objective (run spec's discount rate) | MILP (min_cost) |
| `milp_max_actions` | 1 (1–2) | 2 allows a second treatment in the first year the treated joint loses Good lane-miles | MILP |
| `milp_retreat_window` | 0 (0–5) | With 2 actions: the second treatment may also come up to this many years after that first year | MILP |
| `milp_min_year_share` | NULL (0–1] | Hard: every year spends ≥ share × the plan's peak year; default from the config's `configs.milp_min_year_share` (migration 068) | MILP |
| `milp_min_year_spend` | NULL (≥ 0) | Hard: every year spends ≥ this ($ nominal) | MILP |
| `milp_time_limit_s` | 300 (10–14,400) | HiGHS wall-clock limit, shared across the phases; models over 100,000 variables solve their relaxations with interior point (`mip_lp_solver = ipm`) | MILP |
| `milp_mip_gap` | 1e−4 (1e−6–0.05) | Relative optimality gap | MILP |

**Other constraints:**

| Model / field | Default | Meaning | Read by |
|---|---|---|---|
| `treatment_caps.enabled`, `caps[].treatment_id`, `caps[].max_per_year` (≥ 0) | FALSE | Hard per-year count per treatment (quota veto) | greedy |
| `treatment_mix_floors.enabled`, `floors[].budget_category` (preservation / rehabilitation / reconstruction), `floors[].min_pct_of_spend` (0–1, Σ ≤ 1) | FALSE | **Reported only.** `category_boost` is never computed by any caller. | report |
| `treatment_mix_floors.boost_strength` | 1.5 (1–5) | Not read by the engine | — |
| `route_priority.enabled`, `nhs_multiplier` | FALSE, 1.25 (1–5) | Benefit × multiplier where `nhs_code > 0` | greedy |
| `route_priority.functional_class_multipliers` | {} | Benefit × multiplier by functional class | greedy |
| `route_priority.priority_route_ids`, `route_multiplier` | [], 1.25 | Benefit × multiplier on listed route ids | greedy |
| `bundling_bonus.enabled`, `bonus` (0.10, 0–1), `neighbor_window` (1, 1–5) | FALSE | **Reported only**: a count of same-year same-route selections. Not enforced. | report |

MILP-assist reads only the network target. District balancing still restricts its network through the load filter, and caps, floors and route priority do not act in it.

### 4.9 The config check

`engine.compiled.validate(tables)` → (issues, warnings). **Issues** stop a run (`compile_config(check=True)` at run start → the run fails listing them) and block an Excel import (`compile_check`). They are also shown by `GET /api/configs/{id}/check` and on Config → Policy. Browse pages compile with `check=False` and still work on a config with issues.

**Issues:**

| Area | Message (paraphrased) |
|---|---|
| Route groups | `match` not all / any; a group with no terms; a term with an unknown op; `in_group` with a field or naming a missing group; an unknown field; `in` / `not_in` without a non-empty list; `between` without `[low, high]` or with low > high; a scalar op without one value; `prefix` on a number field; a non-numeric value on a number field; a group that refers to itself (the first cycle found) |
| Treatments | `require_route_group` / `exclude_route_group` naming a missing group |
| Cost adjustments | Route group doesn't exist |
| Cracking rules | Route group doesn't exist; no default rule (no group) |
| Initializers | Any of the six (asphalt / concrete × Initial / Major / Minor) missing |
| Rates | An active treatment without a `treatment_costs` rate for BC, RC **and** OT |
| Reset operations | Unknown op; an `IDX_*` / `AGE_*` op without an index target (`HOLD_SET`: cci, csi, eci, jci, sci); `CNT_SET` / `CNT_INC` with a target not on the Counters sheet; a raw / family op with a target other than its own (`CCI_FROM_MIN` cci, `IRI_*` iri, `PCRK_*` pcrk, `RUT_FROM_RDI` rut, `FLT_SET` flt, `PAVE_SET` pave, `REHAB_SET` rehab); a value op without `value`; `IDX_FROM` without a source index; `PAVE_SET` value_text not BC / RC; `REHAB_SET` value_text not Initial / Minor / Major |
| Triggers | `gfp_class` not G / F / P; `counter_name` not on the Counters sheet; a `years_since_trts` id that isn't a treatment |
| Active treatments | No reset operations; no trigger branch (unless `committed_only`) |
| Curves | For every **reachable** family and every index that applies to its pavement type: no curve, or a curve type not polynomial / linear / sigmoid. Reachable = every combination of the pavement types and truck loads named by enabled family rules, and the rehab types Initial / Major / Minor, plus pavement / rehab values of any `PAVE_SET` / `REHAB_SET`. Applicable indices: BC cci psi eci sci rdi; RC cci psi csi jci; OT cci psi. |
| Constants | `adt_growth_fallback` empty or containing anything but `layer2`, `layer2_future`, `district_median`, `zero`; `unsurveyed_policy` not `exclude` / `dtims_defaults`; `survey_network` not `conflated` / `raw`; `condition_basis` not `segment` / `joint_average` |
| Rating profile | Fewer than 12 (pavement, metric) thresholds for the chosen profile |

**Warnings:** a trigger branch that can never pass (`never_triggers`). On BC, CSI and JCI don't apply; on RC, RDI doesn't. Such an index stays 0, or 5 after a full reset, so a window on it that contains neither 0 nor 5 can never pass.

The **workbook** adds per-row and cross-sheet checks before `compile_check`:
- trigger lower ≤ upper, CCI included;
- a `years_since` branch has its range and treatments;
- counter name and limit are given together;
- district band floor ≤ ceiling, at least one given;
- no duplicate keys or `(treatment_id, trigger_branch)`;
- references point at treatments on the sheet;
- family rules pass `validate_rules` against the Family Curves sheet;
- a family's name is the same on all its rows;
- active scenario names are unique;
- every touched scenario passes `BudgetScenarioConfiguration`.

The **database** enforces the CHECK constraints named in 4.6 (op list, `pave_filter`, pavement codes, `match`, key patterns, the constants' ranges, the counter list on `treatment_triggers`).

---

## 5. Condition model

### 5.1 One model

Since v1.6 PMS reproduces the dTIMS condition model found by the 2026-09-24 audit:
- `dtims_docs/treatment-audit-2026-09-24/pms-analysis.md` §9;
- reference model `scripts/dtims_audit/nhs_model.py`.

**One module moves condition through time for every path**: `engine/condition/dtims_state.py`. Its users are runs (greedy, MILP precompute and replay), benefits (`engine/benefits/auc.py`), Validate and the project / segment outlooks. It has no database access. Callers pass the compiled config's `CurveBook` (curves plus `ConditionPolicy`) and ordered reset operations. No other projector may be added. CCI is never computed as a minimum of the other indices, and Good / Fair / Poor is never derived from CCI.

The public functions are:

| Function | Purpose |
|---|---|
| `initial_state(inv, start_year, policy)` | The dTIMS starting state at the start year (5.4) |
| `prepare(state, book)` | Build `family_id`; attach the policy columns (`idx_floor`, rating thresholds) and bookkeeping; attach curves; anchor |
| `step(state)` | Advance every row one year (5.6) |
| `apply_treatments(state, treatment, ops, book, year)` | Ordered resets, new family, re-anchor (5.8) |
| `classify_gfp`, `network_gfp` | MAP-21 rating and network shares (5.9) |
| `simulate(state, book, ops, years, plan)` | A fixed plan through N program years (5.10) |

### 5.2 Indices and the state frame

Seven indices on 0–5 (5 = best). Each has its own age.

| Code | Index | Applies to (`applies`) | Holdable |
|---|---|---|---|
| `cci` | Composite condition, **on its own family curve** | all | yes |
| `psi` | Ride (present serviceability) | all | no |
| `eci` | Environmental cracking | BC | yes |
| `sci` | Structural cracking | BC | yes |
| `rdi` | Rutting | BC | no |
| `csi` | Slab cracking | RC | yes |
| `jci` | Joints | RC | yes |

- **An index that doesn't apply keeps its value.** It has no anchor offset (`off_<c>` NULL), so `step` leaves it alone.
- **Pavement type**: BC asphalt, RC concrete, OT other.

State frame, one row per segment:

| Columns | Meaning |
|---|---|
| `pavement_type`, `rehab_type`, `truck_load`, `family_id` | The family (`family_id = pave_rehab_truck`) |
| `current_<c>`, `age_<c>` (7 each) | Index values and ages (ages become fractional after `AGE_INVERSE`) |
| `hold_<h>` (cci, csi, eci, jci, sci) | Years of deterioration still held |
| `off_<c>` | Anchor offset (NULL where the index doesn't apply) |
| `current_iri` (in/mi), `current_rut` (in), `current_crack` (%), `current_faulting` (in) | Raw distress |
| `iri_off`, `rut_off`, `pcrk0`, `pcrk_age0`, `crack_factor` | Raw-distress anchors and the cracking rate |
| `adt`, `adt_growth_pct` | Modeled ADT (starts at `aadt`) and its growth, % per year |
| `cnt_chip`, `cnt_micro` (the config's counters) | Treatment counters |
| `last_applied_treatment_id`, `last_applied_year`, `yr_<TREATMENT>` | Treatment history (gates, sequencing, intervals) |
| `idx_floor` | The config's `index_lower_bound` |
| `k_<c>`, `c1_<c>`, `c2_<c>`, `c3_<c>`, `mx_<c>` | The row's family curves (from the `CurveBook`) |
| `gt_<metric>_{g,p,u}` | Rating thresholds by pavement type |
| `gfp_iri`, `gfp_rut`, `gfp_flt`, `gfp_pcrk`, `gfp` | The rating. `step` and `apply_treatments` drop these columns, so a stale rating is never trusted. |
| `rg_<KEY>` | Route-group membership |

### 5.3 Families and family rules

#### 5.3.1 Families

A family is `<Pave>_<Rehab>_<Truck>`, e.g. `BC_Initial_L`. That gives 18 families. Each has one curve per index in the config's `pavement_families` (section 4.6.7). The parts matter as follows:

- **Pavement type** chooses the indices that apply, the rating metrics (5.9), the trigger branches and rates, and the `CCI_FROM_MIN` operands.
- **Rehab type** (Initial / Major / Minor) chooses the curves and the initializer (5.4.2).
- **Truck load** (H / L) chooses the curves. **No treatment changes it.**

#### 5.3.2 Classification (`pipeline/families.classify`)

1. The enabled rules are tried in ascending `priority` (section 4.6.8). The first match gives `family_id` and its three parts. A segment that matches no rule fails the whole classification, and nothing is written.
2. **The rule's rehab type is replaced by the inventory's where a rehab counts.** A rehab counts when the segment has a `rehab_year` and its `rehab_coverage` is NULL or ≥ `min_rehab_coverage`. The replacement is the rehab type set by the config treatment matching the latest CLOSED project's `rehab_treatment_id`: its unfiltered `REHAB_SET`, or through `project_treatment_map` (`CompiledConfig.rehab_type_of`). An unmapped code keeps the rule's rehab type. The family id is then recomposed.

With the shipped rules, pavement type comes from the ARAN surface (JCP / CRC / JOINTED / CRCP → RC; −1 / OTH / GRV / BRK / UNP / missing → OT; everything else → BC). Truck load is H on a coal-route section or where `truck_pct` ≥ 0.10. Rehab type is Initial unless the inventory's project says otherwise.

#### 5.3.3 When classification reruns

`pipeline.families.reclassify(conn, config_id, …)` runs in one transaction and logs `data_refresh_log` stage `E2_families`. Its callers are:

- the data pipeline, for every config after a segment rebuild;
- `python -m pipeline families [--config N]`;
- the family-rules API (save, rerun);
- the Excel import, when rules, curves or any `RECLASSIFY_SHEETS` change.

It upserts only the rows that change and deletes rows of segments that no longer exist.

#### 5.3.4 The stored starting state (`segment_families`)

`init_condition` runs `initial_state` at the config's start year (else the current year) with the compiled policy, then `classify_gfp`, and stores the result. **Browse pages** read it through `analysis_segments_cfg`. **Runs recompute the state for their own start year** from the inventory (or the run's snapshot) and do not read these values.

| Column | Value |
|---|---|
| `family_id`, `pavement_type`, `rehab_type`, `truck_load` | From classification |
| `current_cci` | Starting CCI |
| `age_psi` … `age_csi`, `age_cci` | Starting ages |
| `cnd_psi` … `cnd_csi` | Starting indices |
| `init_iri`, `init_rut`, `init_pcrk`, `init_flt`, `init_gfp` | Starting raw distress and rating |
| `age_basis` | `rehab_year` or `no_rehab` |
| `start_year` | The year the state is for |

With `unsurveyed_policy = exclude`, unsurveyed rows keep their family but every state column is NULL, so browse pages don't rate them. Curve coefficients do not enter the stored state (ages come from rehab years, not from curves), so a curve-only edit changes no stored value.

### 5.4 Starting state (`initial_state`)

#### 5.4.1 Inputs and input policy

The inventory facts come from pipeline stage E1 (`pipeline/dtims_inputs.py`):

- `raw_psi` … `raw_csi`: vendor indices as delivered; NULL = not measured.
- `inventory_cci`: the vendor's CCI.
- `current_iri`, `current_rut`, `current_crack`, `current_faulting`: raw distress, NULL = not measured.
- `crack_pct_dtims`: PERCENT_CRACKING.
- `survey_year`.
- `rehab_year`, `rehab_treatment_id`, `rehab_coverage`: the latest CLOSED project overlapping the segment.
- `adt_growth_layer2`, `adt_growth_future`, `adt_growth_district`.
- `has_survey`, `aadt`, `lanes`, and the route-group fields.

`_apply_input_policy` then applies the config's choices:

1. `rehab_year` is kept only where `rehab_coverage` is NULL or ≥ `min_rehab_coverage`.
2. With `crack_source = dtims_percent`, `current_crack` = `crack_pct_dtims` where measured, else the FHWA value.
3. `adt_growth_pct` = the first non-null source in `adt_growth_fallback` order, with 0 appended when `zero` is listed.
4. With `survey_excluded_from` set (migrations 060, 062), a segment whose survey (`survey_date`) falls in the window
   `survey_excluded_from` … `survey_excluded_to` on a listed sign system (`survey_excluded_signs`) has
   its survey facts (IRI, rut, cracking, faulting, PERCENT_CRACKING, vendor indices and CCI, survey year and date)
   set to NULL and `has_survey` FALSE (`_survey_excluded`): it starts as road without survey data under the config's
   `unsurveyed_policy` (and a joint average, next, ignores it). This reproduces a dTIMS inventory that lacks a
   delivery. dTIMS's Non-NHS analysis never loaded the County roads surveyed in November–December 2024 (the vendor's
   "Delivery 2 County Roads" went into dTIMS only as a practice import on 2025-02-27; the 2024 condition dTIMS runs
   from is "Condition_History_Historic_2024_Final", 2025-04-10): 21,081 of the 22,114 records on its 1,209 no-data
   County sections (2,150 mi) are dated November–December 2024. US and WV roads surveyed then are in dTIMS (6,449 of
   their 6,475 late-2024 records lie on sections dTIMS rated), and so is the 2025 survey, so the window is County only:
   config 336 sets `2024-11-01` … `2024-12-31` on sign `4`.
5. With `condition_basis = joint_average` (migration 059), the joint's survey replaces each segment's own
   (`_joint_average`), as dTIMS starts a section:
   - per joint (and per survey network when the frame holds both), take the segments with survey data of the
     joint's **latest** survey year;
   - each of `current_iri`, `current_rut`, `current_crack` (after step 2), `current_faulting`, `inventory_iri`,
     `inventory_cci` and `raw_psi` … `raw_csi` becomes its length-weighted mean over those segments that measured
     it (a fact none measured stays NULL);
   - **every** segment of the joint takes those means and that survey year and gets `has_survey` TRUE, including
     segments no survey record covers; the joint is then rated per segment on identical values, so it rates as one;
   - segments without a joint and joints without survey data are unchanged; `rehab_year` stays per segment;
   - the mean is over the segments in the frame: a run's scope (its filter), or every segment for the stored
     starting state (`segment_families`).

   dTIMS rates each section (about 2.3 mi on the Non-NHS set) once on the average of its survey; AMPS's default
   rates every 0.1-mi cell on its own record. On the 2026 Non-NHS set (raw network) that alone moved the surveyed
   start from dTIMS's 4.2 / 81.1 / 14.7 % Good / Fair / Poor to 8.4 / 79.9 / 11.7, with 3,039 mi of partly
   surveyed dTIMS sections left as no-data (Good). With `joint_average` it is 4.0 / 82.1 / 13.9 (29.8 / 60.1 /
   10.1 with the no-data road, dTIMS 32.0 / 57.6 / 10.4), and 91.6 % of the dTIMS-surveyed miles start in the same
   class (72.2 % before). The rest: joints (1.32 mi on average) are shorter than dTIMS's sections, unsurveyed cells
   without a joint stay no-data, and 2,150 mi of 2024 County survey that AMPS has are no-data sections in dTIMS.

Route-group columns are attached when a cracking rule needs them.

#### 5.4.2 Indices

With S = start year, R = `rehab_year` (NULL → 0) and V = `survey_year` (NULL → 0):

```text
t       = S − max(R, V)
recent  = R ≥ V
base(c) = new_base(group, rehab)   if recent
          raw_c (NULL → 0)         otherwise
drift   = a·t + b·t² + c·t³        (a, b, c of group and rehab type)

PSI  = base + drift, group asphalt on BC, concrete otherwise
RDI  = 0 on RC;   else base + drift (asphalt)
ECI  = 0 where raw_eci is NULL;   else base + drift (asphalt)
SCI  = 0 where raw_sci is NULL;   else base + drift (asphalt)
CSI  = 0 unless RC;   else base + drift (concrete)
JCI  = 0 unless RC;   else base + drift (concrete)
CCI  = inventory_cci (NULL → 0)
```

- The group is chosen per index. Asphalt covers PSI on BC, and ECI, SCI and RDI. Concrete covers CSI, JCI, and PSI on RC and OT.
- `new_base` is 5 for Initial and Major and 4.5 for Minor in config 1.
- A starting index is not floored or capped here. The floor applies from the first `step` on.
- Some indices that don't apply are still computed: RDI on OT, and ECI / SCI on RC or OT where surveyed. Nothing uses them, because they carry no offset.

#### 5.4.3 Ages, holds, counters

```text
age_c = missing_rehab_age                  if rehab_year is NULL   (age_basis 'no_rehab')
        min(S − rehab_year, max_start_age) otherwise               (age_basis 'rehab_year')
```

- The same age is used for all seven indices. It is not floored at 0.
- Holds and counters start at 0. History columns start NULL.
- Config 1: 15 and 15.

#### 5.4.4 Raw distress

```text
IRI  = current_iri                         if measured
       65 − ln(raw_psi/5)/0.0066           if not measured and raw_psi > 0   (not capped)
       0                                   otherwise
RUT  = current_rut                         if measured and ≥ 0
       ((5 − raw_rdi)/6.65)^(1/1.41)       if not measured and raw_rdi > 0
       0                                   otherwise (also a negative measurement)
FLT  = current_faulting on RC where measured and ≥ 0, else 0
PCRK = current_crack (after crack_source), NULL → −1 (dTIMS default)
```

Missing raw distress is filled from the **survey** indices, not from the drifted starting indices.

#### 5.4.5 Cracking rate

`crack_factor` = the factor of the first cracking rule whose route group contains the segment. A rule without a group matches every segment. Config 1: 0.15 %/yr on `INTERSTATE`, 0.37 on `HPMS_1`, else 0.56.

#### 5.4.6 ADT

`adt` = `aadt` (float). It grows by `adt_growth_pct` % a year in `step`. `adt_max` gates read this modeled ADT; `adt_min` gates read the inventory `aadt`.

#### 5.4.7 Lane-miles

`lane_miles` = length × lanes, using `default_lanes` where lanes are missing or ≤ 0. Computed when `lanes` and `length_miles` are present.

#### 5.4.8 Road without survey data (`has_survey` FALSE, migration 056)

Stage E adds 0.1-mi grid cells of LRS road on the unsurveyed sign systems that the survey doesn't cover (`scripts/import_pavement_data._append_unsurveyed_cells`). They carry no condition and no surface type, so the shipped rules put them in `OT_Initial_*`. After the 2026-09-30 rebuild there are 183,308 such rows (16,352.4 mi).

- **`exclude`** (default; every config today): the run loader adds `AND has_survey`, and the stored state is NULL. Such road is not in runs at all.
- **`dtims_defaults`**: the rows are loaded. After the normal formulas, `initial_state` overrides every row with `has_survey` FALSE:

```text
CCI  = 99                                   (dTIMS Analysis->CCI for no-data sections)
PCRK = 0
PSI (and RDI on BC) = index_lower_bound (−1) when there is no rehab year
PSI, RDI, SCI, ECI, CSI, JCI = min(5, max(index_lower_bound, value from 5.4.2)) otherwise
IRI, RUT, FLT: from 5.4.4 with nothing measured → 0
```

The code applies the override whenever `has_survey` is present. The policy only decides whether the rows are loaded.

What these rows then do:
- With IRI, rut and cracking at 0, they rate **Good**.
- Any treatment that adds to or sets CCI lowers it (IDX_ADD_CAP caps at 5).
- Cracking grows at the default rate (0.56 %/yr on CCI age, since OT is not BC), so a row turns Fair once cracking passes 5 %.

> **Why the no-rehab-year case is set, not projected.** With neither a survey nor a rehab year, t equals the start year (about 2026) and the cubic drift dominates: dTIMS's asphalt Initial / Minor initializers run to −∞ (the floor, −1, which is what the saved dTIMS no-data sections hold), but the concrete and asphalt Major ones run to +∞ (PSI ≈ 155,660 on OT Initial, ≈ 326,617 on BC Major). dTIMS gives a section without a rehab year the Initial rehab type, so its no-data sections always sit at −1; AMPS sets that value directly for any family and keeps every unsurveyed index inside [−1, 5] (fixed 2026-09-30, `tests/engine/test_initial_state.py`). With a rehab year the projection runs from the fresh value over start − rehab year, as dTIMS does. The replays of saved dTIMS strategies contain no unsurveyed rows, so this part is matched to dTIMS's formulas, not to saved output.

### 5.5 Curves

#### 5.5.1 Forms

Each (family, index) curve has kind k, C1 = `alpha`, C2 = `beta`, C3 = `c3` and maximum mx = `initial_value` (NULL → 5). `CurveBook.from_params` pivots them to one wide row per family. `base_curve(code, age)`:

```text
polynomial  f(a) = mx + C1·a + C2·a²          (quadratic; C3 unused)
linear      f(a) = mx + C1·a
sigmoid     f(a) = mx                          for a ≤ 0
            f(a) = mx − C1·exp(−(C2/a)^C3)     for a > 0
other       f(a) = NULL (log and unknown kinds)

b(a) = max(0, f(a))
```

#### 5.5.2 Anchoring (curve shifting)

`anchor` records each row's offset from its family curve at the start, and again after every treatment (treated rows only):

```text
off_c     = I_c − b_c(age_c)        for each index that applies (else NULL)
iri_off   = IRI − g(PSI)
rut_off   = RUT − h(RDI)
pcrk0     = PCRK
pcrk_age0 = crack age (SCI age on BC, CCI age otherwise)
```

In later years, I_c = max(floor, b_c(age_c) + off_c), with floor = `idx_floor` (`index_lower_bound`, −1). A road that starts worse or better than its family's average stays that far from the curve.

#### 5.5.3 Inverse age (`inverse_age`, used by `AGE_INVERSE`)

This is the age at which the row's family curve (without offset or the `max(0, ·)` clamp) equals the index, on the descending branch. It returns NULL where no such age exists; `AGE_INVERSE` then keeps the current age.

```text
linear      a = (I − mx)/C1, clamped ≥ 0      (C1 = 0: 0 if I ≥ mx, else NULL)
polynomial  |C2| < 1e−14: as linear
            roots of C2·a² + C1·a + (mx − I) = 0 with a ≥ 0 and slope C1 + 2·C2·a ≤ 0,
            the larger valid root, clamped ≥ 0; NULL if the discriminant < −1e−10
sigmoid     I ≥ mx: 0
            q = (mx − I)/C1 in (0, 1): a = C2 / (−ln q)^(1/C3)
            otherwise NULL
```

### 5.6 The yearly step (`step`)

Each call advances every row one year, in dTIMS order:

1. Drop the stale rating columns.
2. **Holds** (cci, csi, eci, jci, sci): hold ← hold − 1 if hold > 1, else 0.
3. **Ages**: PSI and RDI +1. A holdable index gets +1 only when its hold (after step 2) is < 1.
4. **Indices** that apply: I_c = max(idx_floor, b_c(age_c) + off_c). Indices that don't apply are unchanged.
5. **Raw distress**, from the new indices and ages:

   ```text
   IRI  = g(PSI) + iri_off
   RUT  = h(RDI) + rut_off          (previous RUT kept where h is undefined, RDI > 5)
   PCRK = pcrk0 + crack_factor · (crack_age − pcrk_age0)
   FLT  unchanged
   ```

6. **ADT**: adt ← adt · (1 + adt_growth_pct/100), with NULL growth = 0.

So a `HOLD_SET` of 4 applied in year t freezes the held index's age, and therefore its value, through years t+1, t+2 and t+3. Ageing resumes at t+4, when the hold reaches 0. PSI and RDI are never held.

### 5.7 Raw distress models

```text
g(PSI) = min(500, 65 − ln(PSI/5)/0.0066)    for PSI > 0;   500 for PSI ≤ 0
h(RDI) = ((5 − RDI)/6.65)^(1/1.41)           for RDI ≤ 5;   undefined above 5
PCRK growth = crack_factor % per year of crack age
crack age   = age_sci on BC, age_cci on RC and OT
```

- The 500 cap applies to g before the offset is added.
- Cracking grows with the crack **age**, so it stops while that index is held (crack seal holds SCI and CCI).
- Faulting only changes through `FLT_SET`.
- `IRI_CAP` (500) and these formulas are model constants in code (part of the model version), not config policy.

### 5.8 Treatments: ordered resets (`apply_treatments`)

For each treated row (the `treatment` column; NULL = none), every treatment present must have reset operations, or the call raises. Then:

1. **For each treatment (in id order), its ops in `op_order`.** Each op writes one column for that treatment's rows, restricted to `pave_filter` rows when set. Ops run **sequentially**, so a later op sees earlier results: `IDX_FROM` reads the new source index, `PCRK_*` reads the ages set before it. `AGE_INVERSE` uses the **current, pre-treatment** family's curve, because curves are re-attached only after all ops.
2. **History**:
   - `last_applied_treatment_id` ← the treatment;
   - with a year, `last_applied_year` and `yr_<treatment>` ← year.
3. **Family**: `family_id` ← `pave_rehab_truck` from the (possibly changed) parts. Curves and rating thresholds are re-attached, and the rating is dropped.
4. **Re-anchor the treated rows on the new family** (5.5.2). Offsets become NULL for indices that no longer apply after a `PAVE_SET`, and are computed for indices that now apply.

The operations (v = `value`):

| Op | Effect |
|---|---|
| `IDX_SET` | I_target = v |
| `IDX_ADD_CAP` | I_target = min(5, I_target + v) |
| `IDX_FLOOR` | I_target = max(v, I_target) |
| `IDX_FROM` | I_target = min(5, I_source + v) |
| `CCI_FROM_MIN` (055) | CCI = max(0, m − v), where m = min(ECI, PSI, RDI, SCI) on BC, min(CSI, JCI, PSI) on RC, and −1 otherwise (so max(0, −1 − v) = 0 for v ≥ −1). This is dTIMS `PMS_ancCND_CCI_Annual`, PM Asphalt's CCI reset. |
| `AGE_SET` | age_target = v |
| `AGE_INVERSE` | age_target = inverse_age(current family, I_target); unchanged where undefined |
| `HOLD_SET` | hold_target = v |
| `IRI_MIN_PSI` | IRI = min(IRI, g(PSI)) |
| `IRI_FROM_PSI` | IRI = g(PSI) |
| `PCRK_MIN_AGE` | PCRK = min(PCRK, crack_factor · (crack_age + [crack hold < 1])) |
| `PCRK_FROM_AGE` | PCRK = crack_factor · (crack_age + [crack hold < 1]) |
| `RUT_FROM_RDI` | RUT = h(RDI), kept where undefined |
| `FLT_SET` | FLT = v |
| `CNT_SET` / `CNT_INC` | counter = v / counter + v |
| `PAVE_SET` | pavement_type = value_text (BC / RC) |
| `REHAB_SET` | rehab_type = value_text (Initial / Minor / Major) |

What config 1's treatments do, as stored:

| Treatment | Indices and ages | Raw | Counters | Family |
|---|---|---|---|---|
| THIN_OVERLAY | ECI, PSI, RDI, SCI, CCI +1.25 (≤ 5), then AGE_INVERSE each | IRI min, PCRK min, RUT from RDI | chip 0, micro 0 | Minor |
| MICROSURFACING | same with +0.75 | IRI min, PCRK **from** age, RUT | chip 0, micro +1 | Minor |
| ULTRA_THIN_OVLY | ECI, PSI, SCI, CCI +1; RDI = new PSI + 1 (≤ 5); AGE_INVERSE | IRI min, PCRK min, RUT | chip 0, micro 0 | Minor |
| CHIP_SEAL | ECI, SCI, CCI +0.5; AGE_INVERSE | PCRK min | micro 0, chip +1 | Minor |
| CAPE_SEAL | ECI, SCI, CCI +0.25; AGE_INVERSE | PCRK min | chip 0, micro 0 | Minor |
| CRACK_SEAL | Hold ECI, JCI, CSI, SCI, CCI 4 | IRI min, PCRK min, RUT | chip 0 | unchanged |
| THICK_OVERLAY | Ages 1 (CCI, PSI; ECI, SCI, RDI on BC; CSI, JCI on RC); all seven = 5 | IRI min, PCRK min, RUT | chip 0, micro 0 | Major |
| FAIR_TO_GOOD | Same ops as THICK_OVERLAY | same | same | Major |
| SAW_SEAL_JOINTS | JCI age 1, JCI 5; CCI +1 | IRI min, PCRK min | — | Minor |
| MINOR_CPR_DG / MAJOR_CPR_DG | CCI, PSI, CSI, JCI age 1; CSI, JCI, PSI, CCI ≥ 4.5 | IRI min, PCRK min, FLT 0 | — | Minor |
| PRESERVATION_BC / _RC (inactive) | All ages 1; all seven ≥ 4.5 | — | — | Minor |
| RECONSTRUCT_BC / _RC | All ages 1; all seven = 5 | IRI from PSI, PCRK from age, RUT, FLT 0 | chip 0, micro 0 | Initial, **pavement BC** |

The Non-NHS configs (336, 348) add PM_ASPHALT (`CCI_FROM_MIN` 0.5, Minor) and county treatments that copy ported resets (`scripts/dtims_audit/nonnhs_replay.py`, `TREATMENTS`).

A treatment applies to the whole joint. Each member segment follows its own pavement's ops (`pave_filter`) and pays its own pavement's rate.

### 5.9 MAP-21 Good / Fair / Poor

**The rating is always recomputed from the raw distress on the config's profile.** Every path uses it: runs, network targets, MILP effects, Validate, charts, maps and the project / segment pages.

- The per-row thresholds ride on the state as `gt_<metric>_{g,p,u}`, chosen by pavement type (anything not BC / RC uses OT). They are re-attached whenever the family changes.
- The SQL twin is `pipeline.checks.gfp_sql`.
- The UI reads the profile from `GET /api/configs/{id}/gfp-profile`. No copies of the thresholds exist.

`MAP21_2017`:

| Metric | Good if < | Poor if > | Used on |
|---|---|---|---|
| IRI (in/mi) | 95 | 170 | BC, RC, OT |
| Cracking (%) | 5 | 20 on BC; 15 on RC and OT | BC, RC, OT |
| Rutting (in) | 0.2 | 0.4 | BC, OT |
| Faulting (in) | 0.10 | 0.15 | RC |

```text
metric class = G if x < good_below;  P if x > poor_above;  F otherwise   (a value on a threshold is Fair)
overall      = G if every used metric is G
               P if two or more used metrics are P
               F otherwise
```

- There is no missing-value guard: an IRI of 0 rates Good, as in dTIMS. A missing starting cracking of −1 also rates Good.
- **Network shares** (`network_gfp`) are percentages of **lane-miles** (length × lanes, `default_lanes` where unknown), rounded to 0.01.
- CCI is reported as a number and a curve, never banded.
- Runs from before v1.6 (`gfp_basis 'cci_band'`) used CCI bands.

### 5.10 Timing conventions

- **Program year 1 is the starting state**, at the run spec's start year. No deterioration is applied in year 1.
- **Every later year first steps** (5.6). Treatments are then chosen on that year's stepped state (triggers, gates, benefits), applied to it (5.8), and the year is reported **after** its treatments.
- `simulate` classifies the rating each year after treatments. Greedy, MILP replay, Validate and the benefit paths follow the same order.
- Cost inflation is (1 + inflation)^(year − 1).
- The benefit's t = 0 is the treatment year: t runs 0 … horizon, t > 0 after t steps (`auc.py`).
- Runs also report a **year 0** row: the network before any treatment.

### 5.11 Worked example

This example runs through `simulate` with config 1's curves and ops.

The segment is BC_Initial_L with all ages 10, PSI 3.2, CCI 3.0, SCI 3.4, RDI 3.8, ECI 3.5, IRI 120, rut 0.15, cracking 6.0 % and crack factor 0.56. The relevant curves are:
- BC_Initial_L: PSI and CCI 5 − 0.004a², SCI 5 − 0.003a².
- BC_Minor_L: PSI 5 − 0.005a², CCI 5 − 0.006a².

The plan is a thin overlay in year 3.

```text
Year 1 (start):  b_psi(10) = 5 − 0.4 = 4.6        off_psi = 3.2 − 4.6 = −1.4
                 b_cci(10) = 4.6                  off_cci = −1.6
                 g(3.2) = 132.62                  iri_off = 120 − 132.62 = −12.62
                 rating: IRI 120 F, rut G, cracking 6 F → Fair

Year 2 (step):   age 11: PSI = 4.516 − 1.4 = 3.116;  CCI = 2.916
                 IRI = g(3.116) − 12.62 = 124.03
                 PCRK = 6 + 0.56·(11 − 10) = 6.56

Year 3 (step):   age 12: PSI = 4.424 − 1.4 = 3.024;  CCI = 2.824;  PCRK = 7.12
      (treat)    PSI = min(5, 3.024 + 1.25) = 4.274;  CCI = 4.074
                 AGE_INVERSE on BC_Initial_L: 5 − 0.004a² = 4.274 → age_psi = 13.47
                 IRI = min(IRI, g(4.274) = 88.77) = 88.77
                 PCRK = min(7.12, 0.56·(age_sci 12.68 + 1) = 7.66) = 7.12
                 RUT = h(RDI 4.874) = 0.060
                 REHAB_SET Minor → BC_Minor_L; re-anchor:
                 off_psi = 4.274 − (5 − 0.005·13.47²) = 4.274 − 4.093 = 0.181
                 rating: IRI 88.8 G, rut G, cracking 7.1 F → Fair

Year 4 (step):   age 14.47: PSI = 5 − 0.005·14.47² + 0.181 = 4.134
                 IRI = g(4.134) + (88.77 − g(4.274)) = 93.81
                 PCRK = 7.12 + 0.56·(13.68 − 12.68) = 7.68
```

The inverse age came from the old family's curve, but the offset is taken on the new one. So the segment lands 0.18 above its new curve rather than on it. This is the dTIMS behaviour the replays confirm.

### 5.12 Verification

- **NHS replay:** `tests/engine/test_dtims_state_replay.py`. The fixture is `tests/fixtures/dtims_nhs/fixture.json.gz`, built by `scripts/dtims_audit/extract_fixture.py` from the saved NEW705 strategies, slots After0–15. From each After0 state and the event schedule alone, the test replays with `CurveBook.from_dtims` and the default ops. Every applicable index, raw metric and MAP-21 class must match within **1e−6**. The audit's reference model reproduces 87,210 saved dTIMS values and 48,600 ratings.
- **Non-NHS replay:** `scripts/dtims_audit/nonnhs_replay.py`. It reads `dtims_docs/non-nhs-steady-state-2026-09-29/analysis.sqlite` read-only and covers the 5,700 captured selected strategies of DEL_STIP_2026_Non_NHS_ALL_NETWORK, slots After0–13. Rerun on 2026-09-30 with the archive's curves and the default ops:
  - 5,700 strategies replayed: 2,306 do-nothing and 3,394 treated;
  - 666,848 numeric comparisons, none over 1e−6 (the largest error was 5.7e−13, on IRI);
  - 370,500 rating comparisons with 0 mismatches.
  - `--config N` replays with a config's compiled curves and ops instead.
- The execution order of 5.6, 5.8 and 5.10 is exactly what these replays pin. Changes to `dtims_state.py` must keep both at 1e−6.

### 5.13 Open points

- Config 336 (the dTIMS Non-NHS study) uses `dtims_defaults` with `condition_basis = joint_average` on the raw network; every other config is `exclude` / `segment` / conflated. The 2026-09-30 build has 175,580 `has_survey` FALSE rows per network (15,662.2 mi); 114,540 of them have no joint, so `joint_average` can't fill them and they stay no-data.
- Patching comes from dTIMS's stored network (stage F2), not the survey files: segments off dTIMS's pavement analysis network have none, so the patching gate fails there.

---

## 6. Treatments

**Active treatments** (cost is $ per lane-mile). These are live database values, so the Config page is authoritative.

| Treatment | Pavement | $/lane-mi (asphalt / concrete) | Interval (yr) | Category |
|---|---|---|---|---|
| CRACK_SEAL | BC | 2,217.6 / 131,577.6 | 3 | preservation |
| SAW_SEAL_JOINTS | RC | 0 / 369,600 | 6 | preservation |
| CAPE_SEAL | BC | 99,000 | 3 | preservation |
| CHIP_SEAL | BC | 45,000 | 3 | preservation |
| MICROSURFACING | BC | 103,000 | 2 | preservation |
| ULTRA_THIN_OVLY | BC | 165,000 | 4 | preservation (committed only) |
| THIN_OVERLAY | BC | 220,000 | 2 | rehabilitation |
| THICK_OVERLAY | BC | 300,000 (× 1.2 on `INTERSTATE`) | 2 | rehabilitation |
| MINOR_CPR_DG | RC | 180,000 | 6 | rehabilitation |
| MAJOR_CPR_DG | RC | 1,500,000 | 6 | rehabilitation |
| RECONSTRUCT_BC | BC | 1,360,000 | 4 | reconstruction |
| RECONSTRUCT_RC | RC | 1,360,000 | 4 | reconstruction |

PRESERVATION_BC / PRESERVATION_RC are inactive.

**Unit costs** (`treatment_costs`, dTIMS statewide rates, $ per lane-mile, asphalt / concrete; other
surfaces (OT) pay the asphalt rate, stated explicitly as OT rows): thin overlay 220,000; thick overlay
300,000 (× 1.2 on `INTERSTATE`, a cost adjustment); microsurfacing 103,000; chip seal 45,000;
cape seal 99,000; crack seal 2,217.6 / 131,577.6; ultra-thin 165,000; saw & seal 0 / 369,600; minor CPR
180,000; major CPR 1,500,000; preservation 406,560 / 443,520; reconstruction 1,360,000. The table above
lists the treatments table's display rate. The Config page is authoritative.

**Triggers** (dTIMS decision logic, `engine/treatments/triggers.py`). A treatment is a candidate for a
joint when **any** of its trigger branches passes on a segment of the joint and every gate holds:

- **Pavement:** the branch's and the treatment's pavement type match both the segment's and the joint's
  length-dominant type.
- **Index windows:** each of the six indices inside `[lower, upper]` (inclusive; −99 / 99 = open), and
  the optional CCI window.
- **Branch kind `years_since`:** also 5–7 (min–max) years since the latest of the listed treatments
  (microsurfacing after thin / thick overlay or reconstruction); **counters** (the config's
  `treatment_counters`): chip seals ≤ 2 (chip seal), microsurfacings ≤ 1 (micro's window branch).
- **Branch gates on the MAP-21 class and inventory fields** (migration 055, all optional): `gfp_class`
  (the segment's MAP-21 class this year, G / F / P, rated from the raw distress as the network is);
  `inv_iri_above` (the survey IRI as loaded, strictly above); `patch_pct_min` (inventory patching,
  (L + M + H sq ft) ÷ (length · 5280 · 8) · 100, at least); `adt_min` (the inventory ADT, not the grown
  one, at least). Inventory values don't move with the model, and a missing value fails the gate. They
  carry the triggers of the dTIMS Non-NHS analysis: the Fair treatment (MAP-21 Fair) and the County
  thick / thin overlays (CCI < 1 with IRI_Mean > 150, or patching ≥ 15 %, with ADT ≥ 200; 1 ≤ CCI ≤ 2
  with ADT ≥ 250). Patching is loaded from dTIMS's network by stage F2 `patching`.
- **Treatment gates** (`treatments`): joint length ≥ `min_length_miles` (3 mi for micro, CPR and saw &
  seal; 0.5 otherwise; a branch's `min_length_override` replaces it for that branch), **except that a joint
  shorter than the config's `min_length_exempt_below` (0.5 mi; migration 042) skips the minimum length
  altogether**, so short ramps, connectors and isolated pieces can be treated (0 = no exemption; config
  versions stored before v1.7.2 read as 0); not in
  `exclude_route_group` (chip, cape: `INTERSTATE`, which includes I-68); in `require_route_group`
  (reconstruction: `IM_FUNDS`, Interstates except the Turnpike); modeled ADT < `adt_max` (chip: 1,000);
  lanes ≤
  `lanes_max` (chip: 1; unknown lanes pass); `committed_only` (ultra-thin: never an ordinary candidate);
  `min_years_since_last` (preservation's wait: 6); the same treatment again only after `interval_years`
  (dTIMS IntervalYear: thin, thick, micro 2; chip, cape, crack 3; ultra-thin, reconstruction 4; saw &
  seal, CPR 6).
- **Sequencing:** the joint's last treatment (or `__NONE__`) must list it in `treatment_sequencing` —
  dTIMS's allowed-subsequent lists, including a treatment following itself. Every run applies it.
- **Commitments:** a committed joint is locked before its year and gets its committed treatment in it.

Reconstruction triggers as authored in dTIMS: asphalt PSI 0–1, ECI 0–1, or ECI ≥ 0 with SCI ≤ 1;
concrete PSI, CSI or JCI 0–1; Interstates except the Turnpike (`IM_FUNDS`). **Every treatment that passes
is a candidate** (dTIMS
generates an alternative per eligible treatment); the IBC / MILP chooses among them. The run option
`clamp_trigger_lowers` still rewrites lower bounds to 0.

**Resets** are ordered operations per treatment (`treatment_reset_ops`, seeded from each treatment's dTIMS
counterpart in `engine/condition/dtims_ops.py`), applied in order:

| Operation | Effect |
|---|---|
| IDX_SET / IDX_ADD_CAP / IDX_FLOOR | index = v / index + v (at most 5) / at least v |
| IDX_FROM | index = source index + v, at most 5 (ultra-thin RDI = new PSI + 1, as authored) |
| CCI_FROM_MIN | CCI = the lowest of the pavement's indices − v, at least 0 (asphalt ECI, PSI, RDI, SCI; concrete CSI, JCI, PSI; dTIMS `PMS_ancCND_CCI_Annual`, PM Asphalt's CCI reset) |
| AGE_SET / AGE_INVERSE | age = v / the age at which the **current** (pre-treatment) family's curve reaches the new value |
| HOLD_SET | deterioration of that index held for v years |
| IRI_MIN_PSI / IRI_FROM_PSI | IRI = min(IRI, g(new PSI)) / g(new PSI) |
| PCRK_MIN_AGE / PCRK_FROM_AGE | cracking = min(cracking, rate·(age + 1 if not held)) / that value |
| RUT_FROM_RDI, FLT_SET | rut = h(new RDI); faulting = v |
| CNT_SET / CNT_INC | a counter of the config (`treatment_counters`) |
| PAVE_SET / REHAB_SET | new pavement type / rehab type (new family) |

After the operations the family is rebuilt and the treated segments are re-anchored on the new family's
curves. What each treatment does:

- **Thin overlay:** ECI, PSI, RDI, SCI, CCI +1.25 (at most 5), ages from the old family's curves; IRI,
  cracking min-protected; rut from RDI; counters 0; Minor.
- **Microsurfacing:** the same with +0.75, cracking set directly; micro count +1; Minor.
- **Ultra-thin:** ECI, PSI, SCI, CCI +1 and RDI = PSI + 1; ages; raw distress; Minor; committed only.
- **Chip / cape seal:** ECI, SCI, CCI +0.5 / +0.25; ages; cracking min-protected; counters; Minor.
- **Crack seal:** holds ECI, JCI, CSI, SCI, CCI for 4 years; IRI and cracking min-protected; rut from
  RDI; no index or family change.
- **Thick overlay:** applicable ages 1; all seven indices 5; IRI and cracking min-protected; rut; Major.
- **Saw & seal:** JCI age 1 and 5; CCI +1; IRI and cracking min-protected; Minor.
- **Minor / major CPR:** CCI, PSI, CSI, JCI age 1 and at least 4.5; IRI and cracking min-protected;
  faulting 0; Minor.
- **Preservation:** all ages 1, every index at least 4.5; Minor (no raw reset).
- **Reconstruction (BC and RC):** all ages 1, indices 5; IRI from PSI; cracking set; rut; faulting 0;
  becomes asphalt (BC) Initial.

Truck load never changes at a treatment.

**Eligibility summary.** A segment can be treated only if it has an active treatment whose trigger and
gates pass, a `joint_id` on a joint at least 0.25 mi long (the app's setting), no interval or sequencing
block, and no lock from a future commitment. A treatment applies to the whole joint; each member segment
follows its own pavement's reset operations (steps filtered to BC or RC) and pays its own pavement's rate.
`min_qualifying_fraction` (default 0) can require a share of the joint's length to qualify.

---

## 7. Benefits and cost

**Benefit** (`engine/benefits/auc.calculate_benefits_polars`): the discounted area between the treated and
do-nothing **CCI** paths over the remaining horizon, both from the dTIMS model (the treatment's reset
operations, new family and re-anchoring): Σₜ wₜ · max(0, CCI_treated(t) − CCI_do_nothing(t)) · (1 +
r)^−t, with trapezoid weights (the first and last year halved) and r = the run's discount rate (the
config's `discount_rate`, 4%; `benefit_integration`; dTIMS's exact GET4CAV_PVDIFF integration isn't
published).

**Traffic weighting (what the IBC ranks):** each year's gain is weighted by that year's modeled
ADT^p — ADT grows along the path — and multiplied by the segment's length; a joint's weighted benefit is
the sum over its member segments (the dTIMS benefit per mile, summed). p = the run's ADT exponent (the
config's `adt_exponent`, 0.2, unless the run overrides it). A segment without traffic counts at 50
vehicles a day. The joint's plain CCI benefit (length-weighted mean) is reported alongside.

**Cost** (`engine/optimization/cost.price_segments`, the one pricing function greedy, MILP-assist,
commitments, Validate and the project / segment pages use): for each member segment, length × lanes
(`default_lanes` where unknown) × the treatment's rate for the segment's own pavement type before
treatment (anything not BC / RC prices as OT) × every cost adjustment whose route group the segment is in
× (1 + inflation)^(year − 1); a project costs the sum over its segments. A missing rate is an error, never
a fallback to the display rate.

**B/C:** weighted benefit ÷ cost. The **IBC** (incremental B/C) ranks each step up a joint's efficiency
frontier: its cheaper-to-dearer alternatives, keeping only those that add benefit.

---

## 8. Optimization engine

A run turns three inputs into a work program:

- the **network**: the analysis segments the run loads, in the dTIMS starting state of the run's config;
- the **config**: treatments, triggers, reset operations, costs, curves and constants, compiled and pinned
  at a stored version;
- the **run request**: budgets, horizon, filters, optimizer and constraints.

There are three optimizers. All three share the loader, the trigger evaluator, the condition model
(`engine/condition/dtims_state.py`), the pricing function (`engine/optimization/cost.py`) and the output
format:

| Optimizer | Entry point | What it does |
|---|---|---|
| Greedy | `engine/optimization/chunked.generate_work_program_chunked` | Year by year: force the year's commitments, then buy incremental benefit / cost (IBC) steps from a max-heap until the year's budget is spent. |
| Constrained greedy | `engine/optimization/constrained_work_program.generate_constrained_work_program` | The same greedy with the run's soft constraints. With a network target it re-runs greedy with a growing benefit boost until the target is met. |
| MILP-assist | `engine/optimization/milp/pipeline.run_milp_assist` | Chooses (joint, treatment, year) for the whole horizon at once with HiGHS, against hard % Poor / % Good rows. |

This section describes the current working tree. Where the code and the older docs disagree, the code is
described.

### 8.1 A run end to end

```
POST /api/runs ──► validate request ──► store analysis_runs row (pending) ──► background thread
   │
   ▼
compile + check config ──► config version ──► run spec ──► pin both for the thread
   │
   ▼
status = running ──► run lock ──► load segments (filter, unsurveyed policy, starting state)
   │                                   │
   │                                   └──► run_snapshots (starting inventory)
   ▼
load treatments / triggers / reset ops / sequencing ──► dispatch: MILP-assist | constrained greedy | greedy
   │
   ▼
WorkProgramResult ──► summarize_work_program ──► result_summary ──► status = completed
   │
   ▼
run page (/configuration, /projects, /logs) · Validate (replay) · Excel export
```

#### 8.1.1 The request

`POST /api/runs` (`api/routes/runs.py:create_run`, body `CreateRunRequest`). Any signed-in user can
start a run. The Run Assistant saves runs through the same function (`assistant/tools.save_pms_run`).

| Field | Default | Meaning |
|---|---|---|
| `run_name` | — | Display name. |
| `annual_budget` | 50,000,000 | Used only when `budget_scenario` is absent: expanded to every year. |
| `analysis_years` | 20 (1–50) | Used only when `budget_scenario` is absent. |
| `budget_scenario` | — | `[{year, budget}]`, 1-indexed program years. When present it defines the horizon: `analysis_years` = its largest year and `annual_budget` = its year-1 budget (both stored for display). |
| `power_exponent`, `inflation_rate`, `start_year` | — | Explicit overrides of the config's ADT exponent, inflation and start year. Omitted means the config's value (8.1.4). |
| `minimum_bc_ratio` | 0 | Greedy only: the least incremental B/C a step must have (8.6.4). |
| `allow_budget_carryover` | false | Greedy only: unspent budget moves to the next year. MILP-assist rejects it. |
| `lookahead_years` | — | Accepted and ignored (greedy is yearly; see 8.6). |
| `segment_filter` | — | SQL `WHERE` fragment over `analysis_segments_cfg` (8.1.5). |
| `network_filter` | — | UI preset name (`interstate`, `nhs`, `non-interstate-nhs`, `non-nhs`). The UI ANDs its clause into `segment_filter` before sending. The engine never reads it; it is stored so "New Run from Config" can restore the dropdown. |
| `budget_scenario_id`, `budget_scenario_name_snapshot` | — | Traceability only. The scenario's values are copied into the run. |
| `use_faulting_for_jci` | false | Stored; not read by the engine. |
| `constraints` | — | `ConstraintsConfig` (`api/schemas/constraints.py`): district balancing, network target, treatment caps, mix floors, route priority, bundling bonus (8.7, 8.8). |
| `config_id` | user's default | The config the run uses (`api/configs.user_config_id`). |
| `optimizer` | `greedy` | `greedy` or `milp-assist`. |

The UI network presets (`ui/src/components/CreateRunDialog.tsx`) are these clauses:

| Preset | Clause |
|---|---|
| Interstate | `(SUBSTRING(route_id, 3, 1) = '1' AND LENGTH(route_id) = 13) AND SUBSTRING(route_id, 10, 2) <> '17'` |
| NHS | `nhs_code > 0` |
| Non-Interstate NHS | `SUBSTRING(route_id, 10, 2) <> '17' AND nhs_code IN (2, 4)` |
| Non-NHS | `(nhs_code = 0 OR nhs_code IS NULL)` |

#### 8.1.2 Request-time checks (HTTP 422)

- `network_target.target_year` greater than the request's `analysis_years`. The check compares against
  the request field, not the horizon derived from `budget_scenario`, and does not check
  `poor_target_year`.
- `optimizer = "milp-assist"` with `allow_budget_carryover = true`, or without `highspy` importable.
- `network_target.milp_objective = "min_cost"` with `optimizer = "greedy"`.
- Every schema rule of `ConstraintsConfig`, for example floors that sum above 1, `floor_pct > ceiling_pct`,
  a target value without its year, or an unknown key (`extra = "forbid"`).
- `segment_filter` with a disallowed keyword (`DROP DELETE INSERT UPDATE ALTER CREATE TRUNCATE EXEC
  EXECUTE GRANT REVOKE UNION INTO COPY pg_ information_schema`), SQL comments or `;`. The same guard runs
  again in the loader.
- `config_id` that does not exist.

The Create Run dialog also calls `POST /api/runs/validate-filter`, which applies the same guard, ANDs
the selected districts and the config's unsurveyed policy into the clause, and returns the row count, and
`POST /api/runs/validate-constraints`, which checks that capped treatments exist in the config, that banded
districts exist in `analysis_segments`, and warns about priority routes that aren't in the network.

#### 8.1.3 What is stored at creation

`create_run` writes an `analysis_runs` row with `status = 'pending'`, `progress_step = 'Queued'`,
`gfp_basis = 'map21_raw'`, `config_id`, and `configuration`. The `configuration` JSONB holds:

- `annual_budget`, `analysis_years` and `budget_scenario` (always the full per-year array);
- `minimum_bc_ratio`, `allow_budget_carryover`, `segment_filter`, `use_faulting_for_jci` and `optimizer`;
- the explicit overrides (`power_exponent`, `inflation_rate`, `start_year`), only when they were sent;
- `network_filter`, `budget_scenario_id` and `budget_scenario_name_snapshot`, when set;
- `constraints`, dumped with `exclude_none`;
- `config_id` and `config_name_snapshot`;
- `joint_build_id`, the `joint_builds` row with `status = 'current'`.

It then starts a daemon thread, `_execute_run`, and returns `{run_id, status}` at once.

#### 8.1.4 Config pin, version and run spec

`_execute_run`:

1. **Compiles** the config (`engine/compiled.compile_config`) and runs the config check. A config that
   fails the check fails the run: `error_message` holds the issues and `result_summary.error_detail`
   holds `{stage: "compile", config_id, issues}`. Check warnings, such as a trigger branch that can
   never pass, don't stop the run. They are copied into `result_summary.warnings`.
2. **Versions** it (`ensure_version`). The config's content hash is looked up in `config_versions`. When
   the content is new, a version is appended; either way the version number is written to
   `analysis_runs.config_version`.
3. **Resolves the run spec** (`engine/run_spec.resolve`) and stores it in `analysis_runs.run_spec`.
   Request field → spec field: `power_exponent` / `adt_exponent` → `adt_exponent`; `inflation_rate`;
   `discount_rate`; `start_year`. Only fields the request set explicitly override the config.

   | Run spec field | Source |
   |---|---|
   | `config_id`, `config_hash`, `config_version` | The compiled config |
   | `start_year` | Override, else the config's `start_year`, else the current calendar year. Program year 1 = this calendar year. |
   | `inflation_rate`, `discount_rate`, `adt_exponent` | Override, else the config's constants |
   | `benefit_integration`, `gfp_profile` | The config's constants (not overridable) |
   | `joint_build_id`, `model_version` (`BACKEND_VERSION`), `overrides` | The run |

4. **Pins** both for the thread (`use_compiled`, `use_run_spec`). From then on every loader, the
   condition model, pricing (`economics()`), benefit and Validate's replay read the same values.

While a run is running on a config, edits to that config are refused (`api.configs.check_lock`, 409).

#### 8.1.5 The run lock, loading and the starting state

`_execute_run_in_config` sets `status = 'running'` and then takes the **single-run lock**
(`engine/db.pms_run_lock`). The lock is a Postgres session advisory lock, key `42420001`, taken with
`pg_try_advisory_lock` on a dedicated connection held for the whole run. Only one PMS run executes at a
time across API workers and the CLI (`scripts/run_optimization.py`). A run that can't take the lock fails
at once with `error_message = "Run lock busy: …"` (naming the holder's pid) and
`progress_step = "Refused (another run in progress)"`. It is not queued. The lock is released in a
`finally` block, and by Postgres if the process dies. Deleting a running run (`DELETE /api/runs/{id}`)
terminates the backend holding the lock, then deletes the row.

**Segment filter.** The effective `WHERE` clause is built from three parts, ANDed together:

1. the request's `segment_filter` (which already contains the UI network preset);
2. when `district_balancing.enabled` and its bands name districts, `district_code IN (<band codes>)`,
   so unbanded districts are not in the run at all;
3. inside the loader, unless the config's `unsurveyed_policy` is `dtims_defaults`: `AND has_survey`, or with
   `condition_basis = joint_average` `AND (has_survey OR joint_id IN (<joints of the network with survey>))`, so
   the unsurveyed segments of a surveyed joint are loaded and start from its average (`engine/db.survey_scope_sql`,
   also used by the run-size count).

The loader (`engine/db.load_analysis_segments_df`) reads `analysis_segments_cfg WHERE config_id = :cfg`,
applies the keyword guard again, and orders by `route_id, begin_mp`. The filter can use any column of the
view, and subqueries are allowed. For example, the Non-NHS study runs used
`joint_id IN (SELECT joint_id FROM analysis_segments GROUP BY joint_id HAVING SUM(length_miles) >= 1)`.

**Unsurveyed road** (migration 056). The `unsurveyed_policy` constant decides what happens to
`has_survey = FALSE` rows, the LRS grid cells without survey data:

- `exclude` (the default) leaves them out.
- `dtims_defaults` loads them with dTIMS's no-data starting values: CCI 99, PSI and RDI at the index
  floor, other indices 0, IRI / rut / cracking 0. They rate Good. Because the benefit is clipped at 0
  (8.4), no treatment shows a gain on them until they deteriorate.

A config version stored before migration 056 reads as `exclude`.

**Starting state.** The loader turns the inventory rows into the dTIMS state at the run's start year
(`state_from_inputs`: route-group membership columns `rg_<KEY>`, the initializers, the curves and
anchors), with `adt` = AADT. From here on, `current_psi … current_cci` are modelled values, not survey
values (section 5). Every segment starts with an empty treatment history: no
`last_applied_treatment_id` (sequencing reads `__NONE__`), no `yr_<treatment>` columns, and counters at 0.
Real pre-run projects affect the start only through the rehab year and type.

**Snapshot.** `_store_start_state` writes the loader's inventory columns (`engine/db.inventory_columns`)
as zstd Parquet to `run_snapshots (run_id, start_state, row_count)`. Validate uses it to rebuild the
exact starting state after the inventory is refreshed.

**Policy frames.** The loader then reads the pinned config's frames:

- `load_treatments_df` (treatments with gates, interval, category and order);
- `load_triggers_df` (branches with their authored lower bounds; `configuration.clamp_trigger_lowers`
  rewrites lower bounds to 0);
- `load_resets_df` (the ordered reset operations);
- `load_treatment_sequencing_df` (allowed next treatments; an empty table means no sequencing filter,
  with a log warning).

A missing table fails the run. Nothing falls back to running without policy.

#### 8.1.6 Dispatch

The code evaluates these rules in order:

| # | Condition | Optimizer |
|---|---|---|
| 1 | `optimizer = "milp-assist"` and the network target is enabled with (`max_pct_poor` and `poor_target_year`) or (`target_pct_good` and `target_year`) | MILP-assist (8.8) |
| 2 | Otherwise, any constraint enabled (`ConstraintsConfig.any_enabled()`) | Constrained greedy (8.7). It iterates only when a network target is enabled. |
| 3 | Otherwise | Greedy (8.6) |

A `milp-assist` request without an enabled target runs greedy, constrained or not. The request field's
description still says MILP-assist needs `max_pct_poor`, but a Good floor alone is enough.

All three paths receive:

- the loaded segments, treatments, triggers, reset operations and sequencing;
- `budgets_by_year` (from `budget_scenario`, else `annual_budget` × `analysis_years`), with
  `analysis_years` = its largest key;
- `power_exponent = spec.adt_exponent`, `inflation_rate = spec.inflation_rate` and `minimum_bc_ratio`;
- `ChunkedProcessingConfig(chunk_size=500, minimum_project_length_miles=0.25, joint_length_miles=0.2)`;
- `strategy_prep = configuration.strategy_prep`, default `segment_union`. It is the only value accepted.
  The joint-averaged cascade was removed in v1.7 and any other value raises.

#### 8.1.7 Result assembly

When the optimizer returns a `WorkProgramResult`, the thread builds `result_summary` (fields in 8.9):

- the headline figures;
- `warnings`: the optimizer's warnings plus the config check's warnings;
- `config_version`;
- `work_program_summary` (`engine/optimization/work_program.summarize_work_program`);
- `constraint_report`.

Committed projects are read from `projects` at this point, statuses planned / designed / awarded /
in_progress with a treatment. They override the joint values in `project_summary` (8.9). Because this
happens at completion time, not at the start of the run, the reported cost, milepoints and name of a
committed project are whatever `projects` holds when the run finishes.

`log_optimization_summary` writes the "OPTIMIZATION RESULTS" block to the run log. The row is then saved
with `status = 'completed'`, `progress_pct = 100`, and non-finite floats stored as JSON null
(`_json_safe`).

#### 8.1.8 Progress and logs

`engine/progress.ProgressTracker` writes `progress_step` and `progress_pct` to `analysis_runs` on every
update. The UI polls `GET /api/runs/{id}/progress`. A `DatabaseLogHandler` copies every engine log line
into `run_logs` (`GET /api/runs/{id}/logs`).

| Path | Progress |
|---|---|
| All | 1 % "Starting", 2 % "Loading analysis segments", 4 % "Loading treatments" |
| Greedy | 10 % "Aggregating segments to joints"; each year Y: `10 + 80·Y/N` % "Processing year Y of N"; 100 % "Complete" |
| Constrained greedy with a target | Each iteration i of M owns the window `[100·i/M, 100·(i+1)/M]` (`NestedProgressTracker`). Its lines are prefixed `[iter i/M]` and suffixed with the best G / F / P so far. At each boundary: `[iter i/M] \| G..% F..% P..% \| best G..% F..% P..%`. |
| MILP-assist | 5 metadata, 10 scope, 40 target effects, 60 candidates, 90 during each solver step (the line shows step n, phase, elapsed, best, bound, gap, nodes and years met so far), 93 decoding, 95 replay, 100 complete. The same entries are kept in `milp_assist.phase_log`. |

#### 8.1.9 Failure behaviour

Every failure sets `status = 'failed'`, `error_message` and `completed_at`. `progress_step` is
`'Failed'`, except for a lock refusal, where it is `'Refused (another run in progress)'`. Where there is a
structured reason, `result_summary = {errors: [message], warnings: [], error_detail}`.

| Stage | Cause | `error_detail` |
|---|---|---|
| compile | The config check fails, or the config can't be compiled or versioned | `{stage: "compile", config_id, issues?}` |
| lock | Another run holds the lock | none (message "Run lock busy: …") |
| optimize | Any exception in loading, strategy preparation, pricing (a missing rate), the reset operations, the solver or the MILP pipeline (for example "Committed projects exceed the budget — …" or "MILP-assist found no plan …") | `{stage: "optimize", type, message, trace}` (the last 4,000 characters) |
| save | `result_summary` can't be written | `{stage: "save", type}` |

Errors are never swallowed into an empty year. A year with nothing affordable reports no projects.
Commitments that name a treatment the config lacks, or that cost more than the year's budget, are
warnings, not failures, in greedy. In MILP-assist, committed work above a year's budget fails the run.

The version and run spec are written before the lock is taken, and the snapshot before the policy frames
are loaded. A refused or failed run can therefore still have `config_version`, `run_spec` and a
`run_snapshots` row.

#### 8.1.10 After the run

- `GET /api/runs/{id}/configuration`: the configuration plus a summary. The summary includes
  `segments_treated` (the sum of `segment_count` over projects) and `joints_treated`
  (`result_summary.segments_treated`, which counts joints). It also returns the treatment distribution,
  the condition trajectory, `distribution_by_year`, `constraint_report`, `treatments_meta` (names,
  categories and display rates from the run's config), `gfp_basis`, `config_version`, `run_spec`,
  `warnings` and `error_detail`.
- `GET /api/runs/{id}/projects`: `project_summary` as `ProjectEntry` rows.
- `GET /api/runs`: the list. Headline outcomes are pulled out of `result_summary` in SQL: initial and
  final % Good / % Poor, cost, budget, utilisation, projects and the % Good by year.
- `GET /api/runs/{id}/export.xlsx`: the Excel workbook, rebuilt from `result_summary`
  (`engine/exports.work_program_result_from_summary`). The Configuration sheet shows the run's config
  tables, and there is a Constraints sheet when the run had constraints. It requires
  `status = 'completed'`.
- **Validate** (`api/validation/context.RunContext`, section 9a) rebuilds the run from its
  config version, run spec and `run_snapshots`, and replays `project_summary` with the fixed-plan
  simulator `_simulate_trajectory_with_milp_selections`. With no edits, the replay reproduces the stored
  yearly results; a difference is a bug. Runs from before v1.7 have no snapshot or spec and use today's
  inventory.
- `scripts/run_optimization.py` (CLI) takes the same lock and calls `generate_work_program_chunked` with
  the same `ChunkedProcessingConfig`.

### 8.2 The unit of decision

#### 8.2.1 Segments, joints, projects

| Grain | What it is | Role |
|---|---|---|
| Segment | An `analysis_segments` row, at most 0.1 mi | Condition, deterioration, reset operations, triggers, benefit, pricing and network % Good / Fair / Poor all work per segment. |
| Joint | `joint_id`, a piece of route between LRS layer-70 joints (`pipeline/joints.py`; the run records `joint_build_id`), typically about 0.2 mi | **The unit the optimizers choose.** One treatment per joint per year (greedy), or one per horizon, or one pair (MILP). A treatment applies to every member segment. |
| Project | Touching joints with the same treatment in the same year | Output only (8.2.4). |

Segments without a `joint_id` are dropped from the joint frames (logged as a warning). They stay in the
network, deteriorate, and count in % Good / Fair / Poor, but no optimizer can treat them. MILP-assist
includes them in its baseline (8.8.4).

#### 8.2.2 Joint aggregation (greedy)

`chunked.aggregate_segments_to_joints` runs at the start and again after every year's deterioration.
Each column is aggregated as follows:

| Joint column | Rule |
|---|---|
| `length_miles` | Σ member length |
| `lane_miles` | Σ length × lanes (the config's `default_lanes`, 2, where lanes ≤ 0 or unknown) |
| `segment_count` | Count |
| `current_psi … current_cci`, `current_iri`, `current_rut`, `current_crack`, `current_faulting` | Length-weighted mean |
| `aadt` | Length-weighted mean; 5,000 when undefined |
| `age_*`, `current_age` | Maximum |
| `begin_mp` / `end_mp` | Minimum / maximum |
| `route_id` | First |
| (`pavement_type`, `surface_type`, `family_id`) | **Length-dominant tuple**: the combination covering the most miles, kept together |
| `lanes`, `district` (from `district_desc`), `district_code`, `nhs_code`, `functional_class`, `county_code`, `county_desc` | Each length-dominant on its own |
| `is_committed` | Any member committed |
| `committed_treatment_id`, `committed_program_year`, `committed_project_id` | First committed member's |

The joint frame is used for:

- the joint's pool membership;
- its metadata (district, NHS and functional class for constraints; the output attributes);
- the joint length and lane-miles in reporting.

Triggers, benefit and cost are **not** computed from joint averages. They are computed per segment and
rolled up (8.3–8.5). Averaging would hide a distressed stretch inside a healthy joint.

**Minimum project length.** Greedy drops joints shorter than 0.25 mi
(`ChunkedProcessingConfig.minimum_project_length_miles`, fixed for app runs) from the pool every year.
Their segments stay in the network. This filter drops a committed joint too, so its commitment is not
forced (the due list comes from the pool). MILP-assist has no such filter (8.8.10).

#### 8.2.3 Length-dominant pavement

A joint's pavement type is its length-dominant one. The trigger evaluator requires the branch's and the
treatment's pavement type to match **both** the joint's dominant type and the member segment's own type
(8.3). A treatment's reset operations then run per segment, filtered by each segment's pavement
(`pave_filter`). Each segment is priced at its own pavement's rate (8.5). A concrete sliver in an asphalt
joint therefore can't make a concrete treatment a candidate, but it is still treated and paid for at the
concrete rate when an asphalt treatment is chosen for the joint.

#### 8.2.4 Projects in the output

`summarize_work_program` builds one row per selected joint. `engine/optimization/projects.merge_touching_projects`
then merges rows that meet all of these conditions:

- same `route_id`, `program_year` and `treatment_id`;
- sorted by milepoint, the gap between one's end and the next one's begin is at most 0.011 mi;
- not committed, and with a route and milepoints.

A merged project:

- keeps the first joint as `joint_id` and lists every member in `joint_ids`;
- spans the smallest `begin_mp` to the largest `end_mp`;
- sums `total_length_miles`, `segment_count`, `total_cost`, `total_benefit` and `gap_segments_filled`;
- takes surface, lanes, district and county from its longest member.

Treatment-mix counts and the year × treatment pivots count merged projects. Merging is idempotent.

### 8.3 Candidate generation

`engine/treatments/triggers.evaluate_triggers_segment_union_polars` is the one evaluator. Greedy calls it
every year on the current state. MILP-assist calls it on each joint's do-nothing state in every candidate
year, and for second actions on the treated state (8.8.3).

**Steps:**

1. **Committed joints** (segments with `is_committed`, a `committed_program_year` and a treatment):
   per joint, the earliest committed year governs and the first committed treatment is used.
   - Year = current year: the joint is emitted with its committed treatment only.
   - Year > current year: the joint is **locked** and emits nothing.
   - Year < current year: the commitment has expired, and the joint is evaluated normally.

   Committed and locked joints are removed from the ordinary pool. Greedy forces its due commitments
   before calling the evaluator (8.6.2), so the evaluator's committed rows are not used in greedy.
2. Active treatments only (`treatments.active`). Treatments with `committed_only` (ultra-thin) have no
   ordinary branch.
3. The MAP-21 class (`gfp`) is computed for the year when any branch has a `gfp_class`.
4. Every segment is crossed with every trigger branch. A branch passes on a segment when **all** of the
   gates in the table below hold.
5. A (segment, treatment) pair passes when any of its branches passes; the lowest branch number is kept
   as a diagnostic.
6. **Union to the joint.** A (joint, treatment) pair is a candidate when at least one member segment
   passes. `n_qualifying_segments`, `qualifying_length_miles` and `qualifying_pct` are recorded.
   `min_qualifying_fraction` can require a minimum `qualifying_pct`. The evaluator defaults to 0, and the
   config's `min_qualifying_fraction` constant is **not passed** to it on any run path (8.11).
7. **Sequencing.** When `treatment_sequencing` has rows, the pair survives only if
   (joint's last treatment, candidate) is listed. The last treatment is read from the joint's first
   segment, `__NONE__` when the joint has never been treated in the run.
8. Every surviving (joint, treatment) is a candidate. There is no priority cascade and no single winner;
   the optimizer chooses among them.

**Gates** (`_ptype_ok`, `_length_ok`, the index windows, and `_gate_exprs`):

| Gate | Source | Evaluated on | Passes when |
|---|---|---|---|
| Pavement | branch `pavement_type`, treatment `pavement_type_applicable` | segment and joint | each is null, or equals both the joint's length-dominant type and the segment's type |
| Length | branch `min_length_miles` (branch override, else the treatment's); config `min_length_exempt_below` | joint total length | joint length ≥ minimum, or joint length < exemption |
| Index windows | `psi/rdi/sci/csi/eci/jci _lower/_upper` | segment | lower ≤ index ≤ upper, inclusive, for all six |
| CCI window | `cci_lower/cci_upper` | segment | each null, or satisfied |
| Counter | `counter_name`, `counter_max` | segment `cnt_<name>` | null, or counter (0 if unset) ≤ max |
| Years since | `branch_kind = 'years_since'`, `years_since_trts`, `years_since_min/max` | segment `yr_<t>` | the latest listed treatment exists and `min ≤ year − latest ≤ max`; no history fails |
| Route group required / excluded | treatment `require_route_group` / `exclude_route_group` | segment `rg_<KEY>` | member / not member (a missing membership column raises) |
| Modeled ADT | treatment `adt_max` | segment `adt` (grown along the path) | `adt < adt_max`; unknown fails |
| MAP-21 class (055) | branch `gfp_class` (G / F / P) | segment `gfp` this year | equal; unknown fails |
| Inventory IRI (055) | branch `inv_iri_above` | segment `inventory_iri` (survey IRI as loaded) | `>`; missing fails |
| Patching (055) | branch `patch_pct_min` | segment `(patch_l + patch_m + patch_h) / (length_miles · 5280 · 8) · 100` | `≥`; missing fails |
| Inventory ADT (055) | branch `adt_min` | segment `aadt` (not grown) | `≥`; missing fails |
| Lanes | treatment `lanes_max` | segment `lanes` | null, unknown lanes, or `lanes ≤ max` |
| Wait after any treatment | treatment `min_years_since_last` | segment `last_applied_year` | null, never treated, or `year − last ≥ min` |
| Same-treatment interval | treatment `interval_years` | segment `yr_<this treatment>` | null, never had it, or `year − yr ≥ interval` |

"Year" is the 1-indexed program year. History columns (`last_applied_year`, `yr_<treatment>`) are stamped
with the program year when a treatment is applied (`dtims_state.apply_treatments(year=…)`). The inventory
gates of migration 055 read values that do not change during the run.

### 8.4 Benefit

The benefit of a candidate is the discounted CCI gain of treating now over doing nothing, over the
remaining horizon, computed per segment (`engine/benefits/auc.calculate_benefits_polars`) and rolled up
to the joint (`calculate_benefits_segment_to_joint_polars`).

For each member segment `s` of a candidate joint and treatment, two paths are simulated with
`dtims_state`:

- **do nothing**: `step` applied t times;
- **treated**: `apply_treatments` (ordered reset operations, new family, re-anchoring) at t = 0, then
  `step`.

```
H          = remaining horizon: analysis_years − Y + 1 in greedy program year Y
w_t        = 1 for t = 0 … H; 0.5 at t = 0 and t = H when benefit_integration = 'trapezoid'
r          = the run's discount_rate (config default 0.04)
p          = the run's adt_exponent (config default 0.2)
gain_s,t   = max(0, CCI_treated,s(t) − CCI_do_nothing,s(t))
ADT_s,t    = the do-nothing path's modelled ADT at t (grows each step); 50 where unknown; ≥ 0

B_s        = Σ_t  w_t · (1 + r)^−t · gain_s,t                              (rounded to 4 d.p.)
G_s        = Σ_t  w_t · (1 + r)^−t · gain_s,t · ADT_s,t ^ p
```

Joint roll-up. Every member segment counts, including those that did not qualify, because the treatment
is applied to the whole joint:

```
benefit (reported, "cci_benefit")   = Σ_s L_s · B_s  /  Σ_s L_s          CCI-years, length-weighted mean
weighted_benefit (ranked)           = round( Σ_s L_s · G_s , 4 )          dTIMS benefit, summed over the joint
benefit_cost_ratio                  = weighted_benefit / cost
```

Notes:

- The gain is clipped at 0 each year. A treatment that lowers CCI in some years earns nothing there, but
  it is not penalised.
- The horizon shrinks as the run advances. In the last program year, H = 1, so only t = 0 and t = 1 count.
  Late-year treatments therefore rank low against early-year ones in the same run, although greedy
  compares only candidates of the same year.
- dTIMS's own integration (GET4CAV_PVDIFF) isn't published. The trapezoid at the config's discount rate
  is the documented stand-in (`configs.benefit_integration`, `discount_rate`).
- Constraint boosts (8.7) multiply `weighted_benefit` before ranking, and the boosted value is what
  greedy stores and totals.
- MILP-assist does not use this benefit. Its objective is lane-miles of target effect, or cost (8.8.6).

### 8.5 Cost

`engine/optimization/cost.price_segments` prices every candidate on every path: greedy, commitments,
MILP (both actions of a pair), Validate, and the project and segment pages.

```
cost(segment, treatment, program year y) =
      length_miles × lanes                         (config default_lanes where lanes ≤ 0 / unknown)
    × rate[treatment, pavement]                    (treatment_costs; pavement = the segment's type before
                                                    treatment; anything not BC / RC prices as OT)
    × Π multiplier[treatment, g]  for every cost adjustment g the segment is in (rg_<g>)
    × (1 + inflation_rate) ^ (y − 1)               (the run's inflation; year 1 is base-year dollars)

cost(joint, treatment, y) = Σ over ALL member segments (price_joint_candidates)
```

- A missing rate for a (treatment, pavement) raises and fails the run. There is no fallback to the
  display rate `treatments.unit_cost_per_lanemile`.
- A cost adjustment naming a route group whose `rg_` column is missing raises.
- A mixed joint pays each pavement's own rate.
- Committed projects are priced the same way in their committed year. The run output later shows the
  project's `estimated_cost` from `projects` instead (8.9).
- `base_program_year` is accepted by the callers but not used; the exponent is always `y − 1`.
- Greedy and MILP-assist with the `benefit` objective, or `min_cost` with `milp_cost_basis = 'nominal'`,
  compare nominal dollars. MILP-assist with `present_value` discounts its cost objective only (8.8.6).
  The budgets and reported costs stay nominal.

### 8.6 Greedy incremental benefit / cost

#### 8.6.1 The year loop (dTIMS timing)

```
state_0 = starting state (8.1.5); record year 0 (% G/F/P, lane-miles, MAP-21)
joints  = aggregate(state_0), drop joints < 0.25 mi
for Y in 1 … N:
    if Y > 1: state = step(state); joints = aggregate(state), drop joints < 0.25 mi
    budget_Y = budgets_by_year[Y] (+ carryover if enabled)
    selections = plan_year(Y)                 # 8.6.2 – 8.6.5
    state = apply_treatments(state, selections expanded to member segments, year = Y)
    record year Y: % G/F/P of ALL loaded segments after treatment
```

Program year 1 is the starting state; treatments chosen in year 1 act on it. Every later year
deteriorates first, then chooses, then applies. The year's condition is reported after its treatments.
`generate_work_program_polars` in `work_program.py` is a thin wrapper around the same loop.

#### 8.6.2 One year (`chunked._plan_rolling_window`)

1. **Budget.** `budget = budgets_by_year.get(Y, annual_budget) + (carryover if allowed)`. The yearly
   record reads `budgets_by_year.get(Y, 0)`. The two defaults differ only for a year missing from a gappy
   `budget_scenario`.
2. **Commitments due this year.** Joints in the pool with `is_committed`, `committed_program_year = Y`
   and a treatment the config has are priced with `price_joint_candidates` and forced in with benefit 0.
   Commitments naming an unknown treatment are dropped with a warning. If their cost exceeds the budget,
   a warning is recorded, and nothing else is bought that year.
3. **IBC budget** = `max(0, budget − committed cost)`. The IBC pool is the remaining joints.
4. **Strategies** (`prepare_strategies_chunked` → `work_program._prepare_strategies_segment_union`):
   - candidates from the evaluator (8.3), limited to the pool;
   - per-segment benefit rolled up to the joint (8.4), with the horizon `N − Y + 1`;
   - the joint's price (8.5);
   - a `DO_NOTHING` row per pool joint (cost 0, benefit 0);
   - metadata: district, route, NHS, functional class and lower-cased `budget_category`;
   - when constraints are set, the benefit multipliers (8.7).
5. **IBC selection** on the strategies (8.6.3–8.6.4), with the year's quota state when constraints are set.
6. **One treatment per joint.** Where the IBC upgraded a joint through several frontier levels, the
   highest-cost row (the last level reached) is kept. The committed rows are prepended.

After the year: selections are stamped with `program_year`, expanded to member segments, and applied. The
(joint, treatment, year) history is kept for reporting. The interval itself is enforced through the
segments' `yr_<treatment>` columns (8.3).

#### 8.6.3 Efficiency frontier (`ibc.build_efficiency_frontier_polars`)

Per joint:

1. Sort the strategies (DO_NOTHING included) by cost ascending, then `weighted_benefit` descending.
2. Keep a strategy when its `weighted_benefit` equals the running maximum over itself and every cheaper
   strategy (`cum_max`). This removes strictly dominated strategies only.
3. Number the kept strategies `frontier_level` 0, 1, 2, … (DO_NOTHING is 0).
4. `incremental_cost = cost_n − cost_(n−1)`, `incremental_benefit = wb_n − wb_(n−1)`.
   `incremental_bc_ratio = incremental_benefit / incremental_cost` when `incremental_cost > 0`, else null.

The frontier is the non-dominated staircase, **not its convex hull**:

- **Ties are kept.** A dearer strategy with the same weighted benefit as a cheaper one stays on the
  frontier with an incremental ratio of 0. So does a treatment with zero benefit on a joint where nothing
  cheaper has any benefit.
- **Ratios need not decrease along the levels.** A low-ratio step can sit in front of a higher-ratio one.
  Because the heap offers a joint's next level only after its current one is bought (8.6.4), the
  higher-ratio step is reachable only once the low-ratio step has been bought.

  ```
  DO_NOTHING (0, 0) → A (100, 50) ratio 0.50 → B (150, 50) ratio 0.00 → D (300, 90) ratio 0.27
  ```

  D is offered only after B, and B is bought only once the budget can still pay for zero-ratio steps.
- **Equal-cost duplicates.** Two strategies with the same cost and the same weighted benefit are both
  kept. The second has an incremental cost of 0 and a null ratio, so it is never offered, and every level
  above it becomes unreachable. This is rare.

The in-memory reference implementation (`ibc.build_efficiency_frontier` / `run_ibc_optimization`) is not
on the run path.

#### 8.6.4 Selection (`chunked.run_ibc_optimization_chunked`, max-heap)

```
heap = { (−ratio_1(j), j, level 1, …) for every joint j whose level-1 ratio is not null
                                       and (minimum_bc_ratio ≤ 0 or ratio ≥ minimum_bc_ratio) }
remaining = IBC budget
while heap and remaining > 0:
    pop the highest ratio entry (ties: smallest joint id, then level, …)
    if level ≠ current_level(j) + 1: skip (stale)
    if incremental_cost > remaining: skip          # the joint is NOT re-offered this year
    if a quota vetoes it (8.7): skip                # the joint is NOT re-offered this year
    buy it: current_level(j) = level; remaining −= incremental_cost; update quotas
    push j's next level if its ratio is not null and passes the minimum_bc_ratio test
```

- **The budget is a hard ceiling.** A step is bought whole or not at all. An unaffordable step does not
  stop the loop, because cheaper steps of other joints may still fit. The joint whose step didn't fit
  keeps its current level for the year.
- **`minimum_bc_ratio`.** With the default 0 every step with a non-null ratio is eligible, including
  ratio-0 steps. With θ > 0, a joint whose first step is below θ never enters the heap, and a joint stops
  at the last level before its first step below θ, even if a later level's ratio is above θ.
- **The year's spend** is the sum of incremental costs bought plus committed cost. It equals the sum of
  the final rows' costs.
- **Recorded values.** For each kept row, `cost` and `weighted_benefit` are the final level's totals,
  and `incremental_bc_ratio` is the last step's ratio.

#### 8.6.5 Carryover

With `allow_budget_carryover`, the year's remaining budget (`budget − spend`) is added to the next year's
budget. Committed work that overspends makes it negative, and a negative remainder carries too. The
yearly record's `budget` includes the carryover. Without carryover, unspent budget is lost.

#### 8.6.6 Large or "unlimited" budgets

Greedy has no unlimited setting. An unlimited budget is a very large number (the Non-NHS study used
$10¹² a year). With a budget larger than every candidate's cost:

- every joint with any candidate is bought up its frontier to the highest level whose steps pass θ;
- with θ = 0, every joint reaches the top of its frontier, including ratio-0 steps, so the most expensive
  non-dominated treatment is bought;
- with a tiny θ (for example `1e-12`, as runs 410 and 415 used), the joint stops before its first
  zero-gain step.

So the plan treats every joint that qualifies, in the first year it qualifies, with its most beneficial
treatment. This overshoots any sensible target. Run 405 (Non-NHS, $1T a year) spent $9.8B in year 1 and
$23.6B over 13 years, taking % Good from 7 to 82 in year 1 and 99 by year 2. It measures what the
triggers allow, not a need.

#### 8.6.7 Treatment in later years

Greedy re-evaluates every year, so a joint can be treated again whenever its triggers, interval, wait,
counters and sequencing allow. There is no limit on treatments per joint over the horizon, but at most
one per year.

#### 8.6.8 Determinism

For identical inputs the heap order is deterministic: ties on ratio break on joint id, then on the
remaining tuple fields. The following can differ:

- Polars sorts and group-bys are not stable where lengths tie exactly. This affects the length-dominant
  pavement / district of a joint split exactly evenly, a joint's first segment for its last treatment,
  and the frontier order of equal-cost, equal-benefit strategies.
- Weighted benefits are rounded to 4 decimals, so near-equal candidates can tie.
- A different config version, run spec, inventory, joint build or filter changes the input.

### 8.7 Soft constraints and the greedy network-target loop

Constraints are optional sub-objects of `configuration.constraints` (`api/schemas/constraints.py`). A run
with none enabled takes the plain greedy path. Otherwise greedy runs through
`generate_constrained_work_program`, which calls `generate_work_program_chunked` once, or in a loop when
a network target is enabled. MILP-assist ignores every constraint except the network target (8.8.10).

#### 8.7.1 What each constraint actually does in greedy

| Constraint | Schema | Enforced during selection | Reported (`constraint_report`) |
|---|---|---|---|
| District balancing | `enabled`, `penalty_weight` (default 1), `bands[{district_code, floor_pct, ceiling_pct}]` | (1) **Filter**: only banded districts are loaded (8.1.5). (2) **Ceilings, hard, per year**: at the start of each year the quota state sets `ceiling_pct × budgets_by_year[Y]` (without carryover) per district. The heap vetoes a step when district spend so far + its incremental cost would exceed it. Committed cost is not counted against the ceiling. (3) **Floors: not enforced.** No code computes the floor boost, and `penalty_weight` is not read. | Per band: `spent_dollars` (all selected cost in the district over the horizon, committed included), `spent_pct` (÷ total budget over all years), `floor_met`, `ceiling_met`, `satisfied`; `total_budget`. A missed ceiling bumps severity to `violation`, a missed floor to `warning`. The report compares horizon totals, while enforcement is per year. |
| Network target | `target_pct_good` + `target_year`, and / or `max_pct_poor` + `poor_target_year`; `max_iterations` (8, 1–20); `damping` (0.5, 0.1–10) | The outer loop and benefit boost (8.7.2). `every_year` and the `milp_*` fields are ignored by greedy. | The target values; `achieved_pct_good` / `good_shortfall_pp` and / or `achieved_pct_poor` / `poor_excess_pp` (in the target years); `satisfied` (worst gap ≤ 0.5 pp); `iterations`. A miss is a `warning`. |
| Treatment caps | `caps[{treatment_id, max_per_year}]` | **Hard, per year**: each bought heap step of a capped treatment uses a slot, and a step is vetoed when the treatment has none left. A slot is used even when the joint is later upgraded past that treatment in the same year. A vetoed joint is not re-offered that year. | Per cap: `max_observed` (the most final joint rows of that treatment in one year), `satisfied`. A miss is a `violation`. |
| Treatment mix floors | `floors[{budget_category, min_pct_of_spend}]`, `boost_strength` (1.5) | **Not enforced.** No code computes the category boost, and `boost_strength` is not read. | Per floor: `achieved_pct_of_spend` (category cost ÷ total cost, committed included), `spent_dollars`, `satisfied`; `total_spend`. A miss is a `warning`. |
| Route priority | `nhs_multiplier` (1.25), `functional_class_multipliers {class: m}`, `priority_route_ids`, `route_multiplier` (1.25) | Multiplies `weighted_benefit` before ranking, compounded: × NHS multiplier where `nhs_code > 0`, × the class's multiplier, × the route multiplier on listed routes. The joint's length-dominant NHS code, class and first route are used. | `configured_multipliers`; `priority_route_spend` and `priority_route_project_count` (joint rows on listed routes). |
| Bundling bonus | `bonus` (0.10), `neighbor_window` (1) | **Not enforced** (diagnostic). | `adjacent_pairs_observed`: for every (year, route) with n ≥ 2 selected joints, n − 1 is added. This is a proxy count, not measured adjacency. |

**Severity** is the worst of the sub-reports: `ok` < `warning` < `violation`. The report also carries
`warnings`. For example, an empty work program adds "Work program is empty — …".

#### 8.7.2 The network-target loop (`generate_constrained_work_program`)

```
boost = 1.0;  best = none;  best_gap = +∞
for i in 0 … max_iterations − 1:
    result = greedy(…, constraints, network_target_boost = boost)
    good_gap = target_pct_good − %Good(result, target_year)            (if a Good target is set)
    poor_gap = %Poor(result, poor_target_year) − max_pct_poor           (if a Poor target is set)
    worst    = max(good_gap, poor_gap)
    if worst < best_gap: best = result; best_gap = worst
    if worst ≤ 0.5: stop
    if worst > 0:  boost = boost × (1 + damping × worst / 100)
return best   (the iteration with the smallest worst gap)
```

The boost is applied in `apply_benefit_adjustments_polars` by budget category:

| Category | Multiplier |
|---|---|
| rehabilitation, reconstruction | `boost` |
| preservation | `√max(1, boost)` when a % Poor ceiling is set, else 1 |
| other | 1 |

The loop then patches the best iteration's report: `iterations`, the achieved values and gaps, and
`satisfied` (best gap ≤ 0.5 pp). If severity was `ok` and the best gap is above 0.5 pp, severity becomes
`warning`.

Properties of the loop:

- **It measures only the target year(s)**, one year per sub-target. `% Good` and `% Poor` are read from
  the trajectory row of that year, falling back to the last row if the year is beyond the horizon.
- **Every iteration is a full greedy run**, so it takes about M times the time of one run.
- **The boost can only grow.** Nothing lowers it when a target is overshot, so a loop that overshoots
  keeps the overshooting result if its worst gap is the smallest.
- **The boost changes only the order of candidates within each year's budget.** It cannot spend more than
  the budget. An unreachable target returns the closest attempt with `warning`.

### 8.8 MILP-assist

`engine/optimization/milp/` chooses the whole horizon at once: which joints, which treatment, which year.
It solves a mixed-integer program with HiGHS against hard budget rows and hard (or counted) condition
target rows. It then replays the plan through the simulator to verify it.

#### 8.8.1 Preconditions and settings

- Preconditions:
  - `optimizer = "milp-assist"` and an enabled network target with a Poor ceiling and / or a Good floor
    (8.1.6);
  - `allow_budget_carryover = false`;
  - `highspy` installed;
  - the config has reset operations.
- Ignored: `minimum_bc_ratio`, `power_exponent`, `lookahead_years`, `strategy_prep`,
  `ChunkedProcessingConfig`, and every constraint other than the network target.

| `network_target` field | Default | Meaning in MILP-assist |
|---|---|---|
| `max_pct_poor`, `poor_target_year` | — | % Poor ceiling (MAP-21, lane-miles) in that program year |
| `target_pct_good`, `target_year` | — | % Good floor in that program year |
| `every_year` | false | A row for every year from `every_year_from` to each target year, not just the target year |
| `every_year_from` | 1 | The first year with rows (earlier years are free) |
| `milp_objective` | `benefit` | `benefit` or `min_cost` (8.8.6) |
| `milp_cost_basis` | `nominal` | `min_cost` only: `nominal` or `present_value` |
| `milp_max_actions` | 1 | 1: one treatment per joint over the horizon. 2: also treatment pairs (8.8.3). |
| `milp_retreat_window` | 0 (0–5) | With 2 actions: the second treatment may also come up to n years after the first year of Good loss |
| `milp_min_year_share` | — | Even spending: every year ≥ share × the plan's biggest year |
| `milp_min_year_spend` | — | Even spending: every year ≥ this many (nominal) dollars |
| `milp_time_limit_s` | 300 (10–14,400) | Wall-clock budget shared by the phases |
| `milp_mip_gap` | 1e-4 (1e-6–0.05) | HiGHS relative gap per phase |

**Budgets.**

- With `benefit`, `budgets_by_year` are ceilings, and a budget of 0 means no spending that year. A year
  with candidates but no entry in `budgets_by_year` raises.
- With `min_cost`, every year 1…N gets its budget, and a budget ≤ 0 (or missing) means **no limit**:
  there is no budget row, and the year's reported budget equals its cost.

#### 8.8.2 Scope

The measurement years are the union of the Poor and Good row years. With `every_year`, those are
`every_year_from … target year` per sub-target; otherwise they are the target year(s).

**Scope** (`at_risk.compute_at_risk_joints`):

- With a Good floor: every joint.
- With only a Poor ceiling: the joints at risk. A joint is at risk when a member segment's do-nothing
  CCI at the Poor target year is ≤ 2.7, or a member segment is rated Poor then. If fewer than 500 joints
  are at risk, every joint is used.

#### 8.8.3 Candidates (`prevention.compute_target_effects`)

`dn_state[a]` is the do-nothing network in year a (a − 1 steps from the start). For each apply year a
from 1 to the **last measurement year**:

1. **Ordinary candidates.** Scoped joints, without committed joints, go through the trigger evaluator
   (8.3) on `dn_state[a]` with `current_year = a` and sequencing. Only active treatments with reset
   operations are kept.
2. **Committed candidates.** From `_commitments`: per joint, the earliest `committed_program_year` in
   1…N and its treatment. Treatments the config lacks are left out with a warning. Each is a candidate
   with `committed = true` whatever its triggers say. Commitments after the last measurement year are
   added as candidates too, so they still spend budget.
3. **Pairs** (with `milp_max_actions = 2`). For each first treatment t in year a, the treated path is
   stepped year by year. The first year y > a in which a joint's Good lane-miles fall (compared with the
   year before) opens that joint's window, from y to y + `milp_retreat_window`. In each open year, the
   evaluator runs on the treated state, where the first treatment's interval, wait, counters and
   sequencing now apply. Every passing t2 becomes a pair candidate (joint, t, a, `variant = "t2@y"`,
   `treatment_id2 = t2`, `apply_year2 = y`). A joint's window opens only once per (a, t). A treatment
   that never gives the joint any Good lane-miles never opens a window. Committed joints get no pairs.

Consequences:

- **No first actions after the last measurement year.** A target year before the horizon end leaves the
  remaining years without ordinary candidates.
- **Committed joints get nothing else.** They are excluded from ordinary candidates in every year, so a
  committed joint can't also get another treatment in the run.
- **Eligibility is checked on do-nothing states.** A first action's eligibility ignores any other action
  the plan might take on that joint, which is correct because a joint has one variable.

#### 8.8.4 Effects and baseline

For every candidate and every measurement year y ≥ its apply year, the treated path is simulated (the
treatment applied in year a, then y − a steps) and compared with the do-nothing classification in year y,
segment by segment, weighted by lane-miles `w_s`:

```
d_poor[c, y] = Σ_{s ∈ joint} w_s · ( [s Poor at y | do nothing] − [s Poor at y | c] )
d_good[c, y] = Σ_{s ∈ joint} w_s · ( [s Good at y | c]          − [s Good at y | do nothing] )
```

- Positive values help the target. Negative values mean the treatment's family change makes a segment
  worse.
- A candidate has no row, and so a zero effect, in years before it applies.
- A pair's effects are the first treatment's before `apply_year2`, and the simulated effect of both from
  `apply_year2` on.

The **baseline** is computed once per measurement year over the whole loaded network doing nothing,
including segments without a joint:

```
baseline_poor[y], baseline_good[y]   (lane-miles)        total = network lane-miles
```

#### 8.8.5 Variables and rows (`model.build_milp_model`)

Variables are ordered by (joint, apply_year, treatment_id, variant):

- `x_c ∈ {0, 1}`, one per candidate (a pair is one variable). A committed joint takes exactly one of its
  committed candidates (row `committed[j] = 1`): its commitment alone, or, with `milp_max_actions` 2, the
  commitment and a second treatment once the treated joint loses Good lane-miles. Until v1.9.15 committed joints
  got their commitment and nothing else for the whole horizon, which made 70 % Good unreachable on the NHS
  (53 % of its road is committed).
- Indicator variables `z` for counted target rows (phase 3), then `P ≥ 0`, the peak-spend variable,
  when `milp_min_year_share` is set.

```
(1) one action per joint          Σ_{c ∈ joint j} x_c ≤ 1                                   for every joint
(2) budget per year               floor_y ≤ Σ_c cost_c,y · x_c ≤ budget_y                   (no row if ∞ and no floor)
        where cost_c,y = cost of the first action if its year is y, plus cost2 if apply_year2 = y
(3) Poor ceiling in year y        Σ_c d_poor[c,y] · x_c ≥ baseline_poor[y] − cap·total      cap = max_pct_poor / 100
    Good floor in year y          Σ_c d_good[c,y] · x_c ≥ floor·total − baseline_good[y]    floor = target_pct_good / 100
(4) counted row (phase 3)         Σ_c coef_c · x_c − M·z ≥ required − M,  z ∈ {0,1}
        M = max(0, required − Σ(negative coefs)) + 1e-6
    years met                     Σ_{z ∈ group} z ≥ n                                        (count_mins)
(5) even spending                 spend_y ≥ milp_min_year_spend                              every year 1…N
                                  spend_y − P ≤ 0,  spend_y − share·P ≥ 0                    every year 1…N
(6) extra rows (studies only)     lo ≤ Σ_c a_c · x_c ≤ hi                                    run_milp_assist(extra_rows=…)
```

- Every requested target row is emitted, even when doing nothing already meets it, because a harmful
  selection could use up the slack.
- The even-spending rows cover **every program year 1…N**, not just the years with candidates. A year
  with no possible spending, such as a year after the last measurement year with no late commitment,
  therefore forces P = 0 under a share rule. Under a spend floor, that year's row is infeasible. The
  settings are meant for target rows through the horizon's end.
- `extra_rows` exists only for Run Assistant studies (`analysis_worker/API.md`). App runs never pass it.

#### 8.8.6 Objectives

The **benefit objective** (`milp_objective = "benefit"`) maximises the target effects:

```
maximise Σ_c x_c · Σ_{y ∈ poor rows} d_poor[c,y] + Σ_{y ∈ good rows} d_good[c,y]
```

This is lane-miles of Poor avoided plus Good gained, summed over the target year(s), or over every row
year with `every_year`. It is not the CCI benefit of 8.4.

The **minimum-cost objective** (`milp_objective = "min_cost"`) finds the funding need. It maximises
`neg_cost_m`, the negated total cost in $ millions (so HiGHS's tolerances are sensible):

```
nominal        neg_cost_m(c) = −( cost_c + cost2_c ) / 1e6
present_value  neg_cost_m(c) = −( cost_c / (1+d)^(a_c − 1)  +  cost2_c / (1+d)^(a2_c − 1) ) / 1e6
               d = the run spec's discount_rate (outside a run: the config's)
```

Costs are already inflated to their year (8.5). Relative to year 1, a dollar of work in year y costs:

| Basis | Weight of year-y work | With 2 % inflation, 4 % discount |
|---|---|---|
| Nominal | `(1 + i)^(y−1)` | grows, so the cheapest plan does work **early** (front-loads) |
| Present value | `((1 + i) / (1 + d))^(y−1)` | shrinks, so the cheapest plan does work **just in time** |

The budget rows and all reported costs stay nominal. Present value changes only which plan is cheapest,
the way dTIMS compares strategies. No stored run uses `present_value` yet.

#### 8.8.7 Phases (`run_milp_assist`)

Feasibility is solved separately from the objective:

| Step | Rows | Objective | Time |
|---|---|---|---|
| 1. Feasibility | every target row hard | 0 | 25 % of the limit |
| 2a. If step 1 found a plan | every target row hard | benefit, or −cost | the rest (starts from step 1's plan) |
| 2b. If step 1 is `Infeasible`, or found no plan in its time: (i) most years with % Poor met | Poor rows counted (z, reward 1) | Σ z | 30 % |
| (ii) most years with % Good met | Poor and Good rows counted; `years_met[poor] ≥ n_poor` | Σ z (Good) | 30 % |
| (iii) keep the counts | both counted; `years_met ≥` both counts | benefit, or −cost | the rest |

- Each phase starts from the previous plan (a HiGHS start solution with z and P filled in).
- Phase time = `max(10 s, min(fraction × limit, time left))`. The 10-second floor means the total can
  run slightly past the limit.
- If step 2a finds no plan, step 1's plan is used.
- If step 2b(i) finds no plan, the run fails ("MILP-assist found no plan … while counting % Poor years;
  raise the time limit").
- The outcome is `targets_met` (step 2a) or `years_maximized` (step 2b). `fallback_reason` explains which
  target years were missed and by how many pp-years.
- Counting maximises the number of years met, by priority: Poor first, then Good. How far a missed year
  misses is not optimised; it is reported.

#### 8.8.8 Solver (`solver.solve_milp`)

HiGHS runs with `time_limit` and `mip_rel_gap`, and `passModel` errors raise. HiGHS's log goes to the
run log, prefixed `HiGHS [phase]`.

Two callbacks report progress:

- `cbMipImprovingSolution`: every new best plan, with its objective, bound, gap, nodes and plan vector;
- `cbMipInterrupt`: at most every 5 s (`progress_every_s=5.0`), a progress event.

The pipeline computes each plan's yearly shortfalls. It shows them on the progress line, logs "New best
plan — …" lines with % short by year, and appends them to `milp_assist.solver_trace` (capped at about 600
entries; older middle entries are dropped).

Status mapping:

| HiGHS status | Reported as |
|---|---|
| Optimal | `Optimal` |
| Infeasible, UnboundedOrInfeasible | `Infeasible` |
| TimeLimit | `TimeLimit` (the best plan found is used, if any) |
| iteration or solution limits, interrupt | `SubOptimal` |
| errors | `Error` |

When HiGHS stops on its time limit, results can differ between otherwise identical runs.

#### 8.8.9 Decoding, replay and verification

1. **Decode.** Each variable with `x ≥ 0.5` becomes a selection row with its `program_year` and cost. A
   pair adds a second row for `treatment_id2` in `apply_year2` with `cost2` and benefit 0. The rows are
   enriched with joint metadata (`_joint_metadata`: route, milepoints, length, lane-miles, segment count;
   surface is length-dominant, while lanes, district and county take the first segment's value).
2. **Replay.** `_simulate_trajectory_with_milp_selections` runs the plan through the simulator with the
   same timing as greedy (year 1 is the start; later years step first; each year's selections expand to
   member segments and apply). It records % G/F/P for years 0…N.
3. **Verify.** For every target row it compares:
   - `predicted_pct`: baseline ± the model's summed effects of the chosen candidates;
   - `achieved_pct`: from the replay.

   `satisfied` comes **only from the replay** (a small tolerance). A difference above 0.05 pp in any row
   sets `drift_warning` ("The replayed plan differs from the model's prediction … File a bug with this
   run id"). Severity is `ok` only if every row is satisfied and there is no drift.

With `every_year`, `achieved_pct_poor` reports the worst (highest) Poor year and `achieved_pct_good` the
worst (lowest) Good year.

#### 8.8.10 Differences from greedy to keep in mind

| Aspect | Greedy | MILP-assist |
|---|---|---|
| Treatments per joint | One per year, any number over the horizon | One over the horizon, or one pair |
| Joints < 0.25 mi | Never treated | Candidates (subject to the triggers' length gate and the exemption) |
| Commitments beyond the horizon | Joint locked for the whole run | Ignored (joint free) |
| Commitments in a joint < 0.25 mi | Not forced | Forced |
| Committed work over a year's budget | Warning; nothing else bought that year | Run fails |
| Other constraints (districts, caps, route priority, mix, bundling) | Applied as in 8.7 (district filter always) | Only the district filter (it acts at load time); nothing else |
| Carryover | Optional | Rejected |
| Years after the last target year | Planned normally | No first actions (only pair seconds and late commitments) |
| `total_benefit` | ADT-weighted CCI benefit (boosted) | Lane-miles of target effect |

#### 8.8.11 `constraint_report` of a MILP-assist run

`network_target`:

| Field | Meaning |
|---|---|
| `enabled`, `max_pct_poor`, `poor_target_year`, `target_pct_good`, `good_target_year`, `every_year`, `every_year_from` | The settings |
| `years_met` | `{poor: [years], good: [years]}`, satisfied in the replay |
| `achieved_pct_poor`, `poor_excess_pp`, `achieved_pct_good`, `good_shortfall_pp` | Target year, or the worst year with `every_year` |
| `poor_satisfied`, `good_satisfied`, `satisfied` | From the replay |
| `milp_objective`, `milp_min_year_share`, `milp_min_year_spend` | Echoed settings |

`milp_assist`:

| Field | Meaning |
|---|---|
| `solver_status`, `objective`, `mip_gap`, `objective_kind` | Of the final phase's solution. With `min_cost`, `objective` is −$M (e.g. −12,670.05 = $12.67B). |
| `annual_need` | `min_cost` only: `{year: cost}` of the plan |
| `solve_time_s`, `node_count`, `num_vars`, `num_rows` | Of the final phase |
| `candidate_joints`, `committed_projects` | Distinct joints among candidates; committed candidates |
| `scope` | `all joints` or `joints at risk of Poor` |
| `total_network_lane_miles`, `baseline` | Denominator; `{year: {poor, good}}` do-nothing lane-miles |
| `target_rows` | Per row: `row`, `label`, `year`, `limit`, `predicted_pct`, `achieved_pct`, `gap_pp`, `satisfied`, `counted`, `shortfall_lane_miles` |
| `drift_warning` | Null, or the rows where the replay and the model differ by more than 0.05 pp |
| `time_limit_s`, `mip_gap_tolerance` | Settings used |
| `outcome`, `fallback_used`, `fallback_reason` | `targets_met` / `years_maximized` and why |
| `phases` | Per phase: `phase`, `status`, `has_plan`, `objective`, `bound`, `gap`, `time_s`, `nodes`, `num_vars`, `num_rows`, `shortfall` (years met, pp-years short, years short, pp short by year) |
| `solver_trace` | Progress and incumbent events with their shortfall summaries |
| `phase_log` | `{pct, step, elapsed_s}` of every progress update |
| `total_pipeline_time_s` | Wall-clock time of the whole pipeline |

### 8.9 Outputs

`result_summary` (JSONB on `analysis_runs`, roughly 1 MB for a statewide run):

| Field | Meaning |
|---|---|
| `start_time`, `end_time`, `duration_seconds` | Optimizer wall clock (loading excluded) |
| `segment_count` | Segments loaded (after filter and unsurveyed policy) |
| `treatment_count` | Rows of the treatments frame |
| `total_cost` | Σ yearly spend, nominal (committed included) |
| `total_benefit` | Greedy: Σ `weighted_benefit` of the final selections (boosts included). MILP: Σ target-effect objective of the chosen candidates (lane-miles). |
| `segments_treated` | Selected **joint rows** (greedy: joints per year, summed; MILP: selection rows, pairs counting twice) |
| `budget_utilization_pct` | `total_cost / total_budget × 100` |
| `initial_pct_good`, `final_pct_good`, `pct_good_change` | Year 0 and year N (MAP-21, lane-miles) |
| `errors`, `warnings` | `errors` is always empty on success. `warnings` holds unknown / over-budget commitments and config-check warnings. |
| `config_version` | The compiled version |
| `work_program_summary` | Below |
| `constraint_report` | Null for plain greedy; 8.7.1 (greedy) or 8.8.11 (MILP) |
| `error_detail` | Failed runs only (8.1.9) |

`work_program_summary`:

| Field | Meaning |
|---|---|
| `analysis_years`, `total_budget`, `total_cost`, `total_benefit`, `budget_utilization_pct`, `average_annual_cost` | Totals. `total_budget` is Σ yearly budgets. For MILP `min_cost` years without a limit, the year's budget is its cost. |
| `segments_treated_total` | As `segments_treated` above |
| `projects_total` | Merged projects (8.2.4) |
| `yearly_summary[]` | One entry per year, 0 … N: `year`, `budget` (greedy: including carryover), `cost` (spend), `segments_treated` (joints selected that year), `pct_good`, `pct_fair`, `pct_poor` (after the year's treatments). Year 0 is the start (budget and cost 0). |
| `final_network_condition` | `{pct_good, pct_fair, pct_poor}` of year N |
| `treatment_mix` | `{treatment_id: {count, total_cost}}`. `count` is merged projects; `total_cost` is the engine's cost of that treatment's joint rows (committed projects at their priced cost, not `estimated_cost`). |
| `distribution_by_year` | Year × treatment pivots built from `project_summary`: `years`, `treatments`, `count` / `cost` / `miles` matrices (rows are treatments, columns are years), and row and column totals |
| `project_summary[]` | Below |

`project_summary[]` (one per merged project):

| Field | Meaning |
|---|---|
| `joint_id`, `joint_ids` | First member, and all members |
| `route_id`, `begin_mp`, `end_mp` | Span |
| `treatment_id`, `program_year` | The decision |
| `total_length_miles`, `segment_count` | Sums |
| `total_cost` | Σ joint costs (nominal, the year's dollars). Committed: `projects.estimated_cost` when set. |
| `total_benefit` | Greedy: Σ of the joints' `cci_benefit` (each a length-weighted CCI-years mean; summed when joints merge). MILP: the pair's target-effect lane-miles on its first action, 0 on its second. |
| `surface_type`, `lanes`, `district`, `county_code`, `county_desc` | Length-dominant (greedy). MILP: surface length-dominant, the rest from the first segment. Greedy's `district` is `district_desc` ("07-District 7"); MILP's is `district` ("7"). |
| `gap_segments_filled` | Always 0 (joint gap-filling is not implemented) |
| `is_committed`, `committed_project_id`, `project_name` | Committed projects. Their `begin_mp`, `end_mp`, `total_cost` and `total_length_miles` come from `projects` (bmp, emp, estimated_cost, length_mi) at completion time. Several joints of one committed project are reported once. |

A trimmed greedy example (run 410, Non-NHS, dTIMS yearly budgets):

```json
{"segment_count": 188066, "treatment_count": 19, "total_cost": 20530792453.84,
 "segments_treated": 16549, "initial_pct_good": 7.06, "final_pct_good": 98.93,
 "budget_utilization_pct": 2.01, "config_version": 1, "constraint_report": null,
 "work_program_summary": {"analysis_years": 13, "projects_total": 13653,
   "yearly_summary": [{"year": 0, "budget": 0, "cost": 0, "pct_good": 7.06, "pct_fair": 68.81, "pct_poor": 24.13, "segments_treated": 0},
                      {"year": 1, "budget": 102082000.0, "cost": 102074520.0, "pct_good": 7.95, "pct_fair": 68.23, "pct_poor": 23.82, "segments_treated": 111}],
   "treatment_mix": {"FAIR_TO_GOOD": {"count": 8593, "total_cost": 14108676164.85}},
   "project_summary": [{"joint_id": "70_0130092000000_3", "joint_ids": ["70_0130092000000_3"], "route_id": "0130092000000",
     "begin_mp": 8.167, "end_mp": 9.259, "treatment_id": "FAIR_TO_GOOD", "program_year": 1, "total_length_miles": 1.092,
     "segment_count": 13, "total_cost": 655200.0, "total_benefit": 31.9163, "surface_type": "ASP", "lanes": 2,
     "district": "07-District 7", "county_code": 1, "county_desc": "01 - Barbour", "gap_segments_filled": 0}]}}
```

The run's budget utilisation of 2 % reflects its $10¹² year-10 budget (8.6.6).

### 8.10 Choosing an optimizer

| Question | Use | Why | Watch out for |
|---|---|---|---|
| "What does a given budget buy?" | **Greedy** | Fast (about 1 minute for 188k segments × 13 years). Spends each year's money on the best incremental B/C. Allows treatment every year. | It measures CCI-area benefit, not % Good / % Poor. It is myopic: a year cannot save for the next without carryover. The benefit horizon shrinks toward the end. With a huge budget it buys every joint's top treatment (8.6.6). |
| "What budget meets a condition target?" | **MILP-assist, `min_cost`** | Finds the cheapest plan meeting every target row, checked by replay. A budget of 0 means no limit. | Nominal dollars front-load (see below). Set `milp_max_actions = 2` for long targets. Run past the target year if the steady state matters. |
| "What is the most condition a given budget buys?" | **MILP-assist, `benefit`**, or greedy with a network target | MILP maximises target lane-miles within hard budgets. The greedy loop is quicker but only nudges priorities. | MILP's benefit is lane-miles in the measured years only. The greedy loop checks the target year only and can't exceed the budget. |
| "What would dTIMS choose with these budgets?" | **dTIMS strategies** (`optimizer = "dtims-strategy"`, 8.12) | Whole-horizon strategies per joint, chosen as dTIMS chooses; on dTIMS's own Non-NHS inventory it reproduces the scenario's program ($18.56B vs $18.57B, every year within 0.1 point) | Ignores constraints and carryover. Its units are joints, not dTIMS's sections. |
| District shares, per-treatment caps, NHS / route priority | **Constrained greedy** | Only greedy applies ceilings, caps and multipliers. | District floors, mix floors and bundling are not enforced (8.7.1). |
| Equal-ish yearly spending | **MILP-assist** with `milp_min_year_share` / `milp_min_year_spend` | Hard rows. | Can make the targets infeasible (run 421). The rule applies to every program year (8.8.5). |

**Lessons from the Non-NHS steady-state study** (config 336, "dTIMS Non-NHS steady state (DEL_STIP_2026)",
2026–2038, 13 program years):

- **Unlimited-budget greedy overshoots.** With $10¹² a year (run 405), greedy bought every qualifying
  joint's top frontier treatment at once: $9.8B in 2026, $23.6B in total, 99 % Good by 2027. With dTIMS's
  yearly budgets (run 410; $10¹² in year 10), it spent $9.0B in year 10 alone. A huge greedy budget is
  the triggers' capacity, not a need. The zero-ratio steps of 8.6.3 add to it unless `minimum_bc_ratio`
  is a tiny positive number (runs 410 and 415 used `1e-12`).
- **One treatment per joint can't hold a long target.** 70 % Good every year 2028–2038, least cost, no
  cap, one action (run 411): 70 % was met in years 3–9 (2028–2034), then fell to about 1 % Good in 2035,
  because roads treated early cracked back to Fair and could not be treated again. The outcome was
  `years_maximized`, with Good met in 7 of 11 years for $7.38B.
- **Re-treatment pairs fix it.** The same target with `milp_max_actions = 2` (run 412): `targets_met`
  for $12.67B. Adding % Poor ≤ 10 changed almost nothing ($12.67B, run 418), and a two-year re-treatment
  window cost slightly less ($12.64B, run 419). The whole Non-NHS network without the ≥ 1-mile joint
  filter cost $15.74B (run 420).
- **Least cost in nominal dollars front-loads and spikes.** Run 412 spent $6.15B in 2026, then little,
  then $3.21B in 2032 and $1.67B in 2033: inflation makes every dollar of work cheapest in its earliest
  year, so the cheapest nominal plan does work as early as the targets allow and in waves when treated
  roads lose Good together. `milp_cost_basis = "present_value"` discounts each year's cost to 2026 at the
  run's discount rate (4 % against 2 % inflation). Later work then counts cheaper, and the cheapest plan
  moves toward just-in-time work, as dTIMS compares strategies.
- **Even spending can make the targets unreachable.** Run 421 (run 419 plus "no year below 30 % of the
  peak") spent about $810M every year and held % Poor ≤ 10 in all 11 years. It met % Good in none of
  them, reaching 41 % by 2038. The solver hit its time limit in three of four phases (outcome
  `years_maximized`).
- **The share rule is solved from a band seed (v1.9.15).** The rule ties every year to one peak variable,
  and HiGHS could not find a first plan with it on the Non-NHS network (runs 469, 470, 484 stalled in
  step 1). With `milp_min_year_share` set, the pipeline now (1) solves the problem without the rule at a 5 %
  gap (`estimate:` phase, about 100 s on Non-NHS) and reads its yearly spend; (2) solves the same problem with
  a plain band instead, every year between share × P and P (`seed:` phase, 5 % gap, 30 % of the time each).
  P starts at the larger of the free plan's fastest pace to date (the most spent by year y ÷ y: no year may
  exceed P, so a catch-up needs that much) and its average year centred in the band (× 2 / (1 + share)),
  + 5 %, then × 1.15, 1.35, 0.9, 1.6, 2 (a higher P also raises the floor); (3) solves the real model with
  the rule from the band plan, which already meets it, so the solver only has to improve the cost and may
  move the peak. A band plan meets the rule exactly. If no band works, the plain feasibility search runs as
  before. `constraint_report.milp_assist.share_seed` records the free plan's yearly spend, pace, average,
  starting peak and every band tried. Results: NHS without committed work, 70 % Good and ≤ 1 % Poor from 2028
  (run 485): plan in 98 s, $1,652.7M, every year $84–168M. Non-NHS, 70 % Good and ≤ 10 % Poor every year
  from 2028, only the half-of-peak rule (run 492): first band ($1,161M–$2,322M) found in 14 min, the rule's
  model proved it within 0.52 % of optimal; $21.40B nominal, every year $1.16–2.32B.
- **Last-year effects.** A least-cost plan lets the network fall exactly to the target in the last
  measured year and does no work after it (run 412 spends $0 in 2038). A 13-year need therefore
  understates the steady-state need beyond 2038. Measure a longer horizon when that matters.

### 8.11 Known gaps in this area

- **District floors and treatment-mix floors are not enforced** in any optimizer, only reported.
  `category_boost` and `district_floor_boost` are never computed; `penalty_weight` and `boost_strength`
  are not read. The bundling bonus is diagnostic only.
- **The IBC frontier is not a convex hull.** Ratio-0 and non-decreasing steps stay on it (8.6.3).
- **`min_qualifying_fraction`** (config constant) is not passed to the trigger evaluator on any run path,
  so it has no effect.
- **`use_faulting_for_jci`** and **`lookahead_years`** are accepted and ignored.
  `ChunkedProcessingConfig.fill_joint_gaps` / `joint_fill_threshold` are not implemented
  (`gap_segments_filled` is always 0).
- **Treatment history starts empty.** Sequencing, interval and years-since gates see only treatments
  applied inside the run.
- **Target-year validation.** `target_year` is checked against the request's `analysis_years`, not the
  budget scenario's horizon, and `poor_target_year` is not checked. A MILP target row beyond the horizon
  fails the run. Unclear whether the UI can send one.
- **Committed project figures** in `project_summary` are read from `projects` when the run completes,
  not frozen at its start.
- **MILP-assist ignores** caps, district ceilings and route priority, and has no 0.25-mi minimum project
  length (8.8.10).

---

### 8.12 dTIMS strategy optimizer (`optimizer = "dtims-strategy"`)

`engine/optimization/dtims_strategy.py`, run by `run_dtims_strategy` from `_execute_run`. dTIMS does not decide
year by year: it generates whole-horizon **strategies** for every element and picks one strategy per element. This
optimizer does the same with AMPS's condition model, triggers and prices. Run options: `strategy_level` (1–5,
default 3: dTIMS LevelOfGeneration), `strategy_extra_years` (0–10, default 0) and `hold_filter` (below). Every
optimizer also takes `include_committed` (default true; false = dTIMS's IncludeCommitted off: the run clears the
committed flags of its segments before it starts, and its stored start state carries that, so replays agree).

**Elements.** One per joint (`joint_elements`): the state of the joint's representative segment (its length-dominant
family, then its longest segment) with the joint's length, lanes (lane-miles ÷ length), length-weighted ADT and
summed patching (so the `patch_pct_min` gate reads the joint's patching share).
Segments without a joint are not elements; they stay in the network's condition, untreated. Treatments are priced over
the joint's member segments (each at its own pavement rate, route-group adjustments and lanes), cached at program
year 1 and inflated `(1 + i)^(y − 1)`.

**Timing.** `StrategySpec.for_run(N, …, extra_years = k)`:

| `k` | Strategies simulate | Treatments may start | Benefit summed over |
|---|---|---|---|
| 0 (default) | years 1 … N | every year | years 1 … N |
| k > 0 | years 1 … N + k | years 1 … N + k − 1 | years 1 … N + k − 1 |

Years past N have no budget, so no work is bought there; they only let a strategy's benefit count past the run, as
dTIMS's analysis period (DEL_STIP_2026: EndYear 2040, EndTreatmentApplicationYear 2039) runs past the years it reports.

**Generation** (`generate`, chunks of 400 elements, one row per partial strategy):

1. The Do-Nothing path is the root. Year 1 is the starting state; every later year steps first (`dtims_state.step`).
2. In the treatment years, a row with fewer than `level` treatments branches: every treatment whose trigger passes on
   that row's state that year makes a child with the treatment applied (`apply_treatments`) and priced (before its
   resets). The triggers are the config's branches, gates and subsequent-treatment table, evaluated by
   `evaluate_triggers_segment_union_polars` with each row as its own "joint". A row whose last treatment's
   `interval_years` has not passed does not branch (dTIMS: a subsequent treatment only after the previous one's
   interval; the trigger gates' same-treatment interval also applies). The parent carries on untreated, so every
   root-to-leaf path is a strategy.
3. Committed work (`joint_commitments`: the joint's committed treatment in every year it has one, the one covering the
   most of the joint where several share a year; until v1.9.15 only the joint's earliest, which lost the later one
   where a joint straddles two dTIMS sections committed in different years; or in the dTIMS harness
   the network's `Com_Trt` / `COM_TRT_2` with their `Com_Cost`) is applied to every row of the element in its year. It
   is not a branch and doesn't count towards `level`. Through the element's **last committed year** no other
   treatment branches (dTIMS's triggers: `IF(IS_COMMITTED() AND YR <= MAX(Com_Year, COM_YR_2 … 4), the committed
   treatment only, …)`; until v1.9.15 only the committed year itself was locked). A commitment's own cost
   is used when it has one, else the rate. In a run, a joint's committed cost is its share of each committed
   project's `projects.estimated_cost`: the cost × the joint's committed length on the project ÷ the project's length
   (`_committed_costs`), as dTIMS charges `Com_Cost`; a project without a cost is priced at the rate.

   The dTIMS Non-NHS analysis's own commitments (221 treatments on 220 sections, $102.1M in 2026, $35–41M a year in
   2027–2031) are loaded into `projects` by `scripts/dtims_audit/import_nonnhs_commitments.py` (status `planned`,
   calendar program year, `estimated_cost` = Com_Cost, `source_key` `dtims:DEL_STIP_2026:<section>:<n>`; re-running
   replaces only those rows), then `python -m pipeline commitments` flags the segments (13,178 across both networks on
   2026-09-30). They then apply to every optimizer's runs. The importer takes each section's milepoints from the
   2026-09-30 export's `From` / `To`: the Non-NHS archive's `FromMeasure` / `ToMeasure` are offsets on the route
   record, which put 43 of the 220 committed sections on the wrong stretch before v1.9.15.

   The Interstate and NHS analysis sets of WVDOT's 70 Percent Good Analysis (2026-09-24) carry theirs the same way
   (`Com_Trt` … `COM_TRT_4`); `scripts/dtims_audit/import_pdf_commitments.py` loads them (529 rows,
   `dtims:PDF-2026-09-24:…`). A commitment happens only through a treatment of the analysis set, so
   `PMS_PM_Preservation` (bound to neither set) is dropped, as in dTIMS's programs. On the Interstate scenario the
   allowable variable `PMS_bCAV_Exclude` drops every committed strategy that doesn't carry all of a section's
   commitments, so the 8 Interstate sections with a PM Preservation commitment get nothing at all: they are not
   loaded but written to `held-sections.json`, the run's `hold_filter`. dTIMS carries a divided Interstate once (EB /
   NB, `Lanes_Total` both directions), so such a commitment is one row per direction with half the cost each.

   Their configuration, "dTIMS Interstate & NHS (70 Percent Good, 2026-09-24)", is built by
   `scripts/dtims_audit/build_nonnhs_config.py --variant pdf`. The two archives' lookups (triggers, unit and County
   costs, curves) and shared treatments are identical; the differences are the treatment set (no County treatments)
   and cracking. dTIMS compares a coded field by its code (only that gives the Interstate set dTIMS's 446.09 mi), so
   `PMS_ancCND_PCRK`'s `Sign = '1'` holds on Interstate-signed road: 0.15 a year there, 0.56 elsewhere. A run plans
   dTIMS's set with `dtims_reference_run_roads`, the opposite direction only where the section has `Lanes_Total`
   (elsewhere dTIMS prices 2 lanes, one direction): 1,780 lane-miles against dTIMS's 1,898 on the Interstates (AMPS
   has fewer lanes on dTIMS's 5- and 6-lane sections), 3,531 against 3,562 on the NHS.

5. **dTIMS's inventory and units** (run options for reproducing a dTIMS run, not for planning).
   `inventory_from_dtims` (a reference run key): every segment starts from the facts of the dTIMS section it lies on
   (`engine/db.dtims_section_inventory`: vendor indices, CCI, IRI / rut / faulting / cracking, survey and rehab years,
   family, ADT and growth, lanes = `Lanes_Total` over the directions in the run), before the starting state is built,
   and the run's snapshot keeps those facts. `dtims_units` (with it): each segment's joint becomes its dTIMS section
   (`dtims:<section>`), so a section is planned, priced and rated whole; then a commitment belongs to the section
   holding most of it, is charged its whole cost (its direction rows together, however much of it the survey covers)
   and the project summary keeps the plan's cost. On the Interstates of the 70 Percent Good Analysis (run 458: dTIMS's
   direction only, the 8 sections dTIMS drops left out) this reproduces dTIMS: $917.7M against $921.8M, % Good the
   same to 0.1 point 2026–2032, 78% of dTIMS's lane-miles the same treatment in the same year. On AMPS's own inventory
   (run 451) the gap is mostly the rehab history: dTIMS has those sections last rehabilitated in 2014.8 on average,
   TheHub 2022.4.

4. **Held elements** (`hold_filter`, dtims-strategy only: a SQL WHERE clause on `analysis_segments_cfg`, like
   `segment_filter`). A joint with a matching segment stays in the network's condition but is never treated, its
   commitments included (a run warning counts them); Do Nothing is its only strategy.

**Scores**, dTIMS's `PMS_nCAV_PV_Benefit` and `PMS_nCAV_PV_COST`:

```text
benefit = Σ_{y = 1 … benefit years} ( max(CCI_y, 0) − max(CCI_y^DN, 0) ) · ADT_y^p / (1 + r)^y
cost    = Σ_events cost_y / (1 + r)^y / length_miles
ADT_y   = ADT · (1 + growth)^(y − 1)              (the state's adt, as step grows it)
```

`p` is the ADT exponent, `r` the discount rate (the run's). The benefit is **not** multiplied by length while the cost
is **per mile**, as in dTIMS, so a longer element has a proportionally higher benefit / cost. These formulas reproduce
dTIMS's PresentValueBenefits and PresentValueCost of all 3,394 treated strategies the Non-NHS scenario selected
(`scenario_strategy_budgets`) within 1e-4 (the benefit over slots 1 … 14 with the section's `ADT_20_Yr_Factor` as the
yearly growth %).

**Selection** (`select`). Every element starts at its base: Do Nothing, or its committed path (kept even if it
overdraws a year; the overdraw is a run warning). A max-heap on incremental benefit / cost walks each element up its
upper convex (cost, benefit) frontier (`_next`: the option with more benefit and the highest ratio; a cheaper or
equal-cost one counts as infinite; ties to the higher benefit). A step is taken only if every year's pooled spending
stays within that year's budget; if the frontier step doesn't fit, the element's best remaining option that fits is
offered instead. A year without a budget has $0. dTIMS's own procedure is proprietary; this is the multi-constraint
IBC it describes, the same procedure as `bms/dtims/select.py`.

**Output.** The chosen plan becomes the run's projects (joint, treatment, program year, cost; the strategy's PV benefit
is shown on its first treatment) and is replayed on every segment (`_simulate_trajectory_with_milp_selections`) for the
yearly condition. `constraint_report.dtims_strategy` records elements, strategies, the largest count for one element,
level, timing, committed treatments, IBC steps, spending and any overdraw by year, and times.

**Proof against dTIMS** (`scripts/dtims_audit/nonnhs_strategy_run.py`). The optimizer on dTIMS's own 11,676 Non-NHS
sections (dTIMS's starting state, config 336, the scenario's budgets, 2 extra years): 672,802 strategies in 59 s; every
one of the 5,700 strategies dTIMS selected is generated, each with dTIMS's PV benefit and cost; the program is $18.56B
against dTIMS's $18.57B, % Good / Fair / Poor within 0.1 point every year 2026–2038, and 10,223 of dTIMS's 11,646
treatments are the same (section, year, treatment). With the run ending in 2038 (no extra years) it is $18.66B and
within 0.5 point.

With the commitments loaded (run 434, strategies to 2040) the result hardly moves ($20.35B; % Good within 0.3 point of
run 433): 2026 is the committed work ($100.1M on 78 joints) and each later year's commitments come out of its budget.

**On AMPS's own inventory** (run 432: config 336, raw network, joint-average start, 11,458 joints, 663,162 strategies,
69 s) the spend matches dTIMS's year by year through 2034, and 2035 is $9.3B against $7.35B. % Good runs 2–7 points
under dTIMS's until 2034 and ends at 58.5 / 27.1 / 14.4 (dTIMS 57.5 / 29.0 / 13.5). The optimizer is the same as in
the proof, so the difference is the inventory: AMPS had no committed projects loaded (now loaded, above; they change
little), rates
2,150 mi of County road on its 2024 survey that dTIMS treats as no-data (Good), keeps about 2,500 mi of cells without a
joint as no-data that dTIMS has survey for, and plans joints (1.32 mi) rather than sections (2.33 mi).

## 9. Projects and commitments

**Statuses:** CLOSED, ACTIVE, HOLD, RESERVE, TERMINATED, WITHDRAWN, planned, designed, awarded, in_progress, completed. **Committed** means planned, designed, awarded or in_progress.

**Commitment flags:** `scripts/populate_committed_flags.py` (also import phase 3f) copies committed projects onto `analysis_segments.is_committed / committed_treatment_id / committed_program_year / committed_project_id`. A segment is matched when it is on the same route and its milepoints overlap the project's. Flags are cleared first. Editing projects in the app does **not** re-run this.

**In a run:**

- **Before** the committed year, the segment is locked (no other treatment).
- **In** the committed year, the committed treatment is forced. Its cost (unit cost × length × lanes × inflation) comes off the budget once, which can overspend. The year then reports budget used = committed + optimizer spend and remaining = budget − used (carried over when carryover is on).
- **After** the committed year, normal triggering resumes.
- Reports show the project's own milepoints, name and estimated cost.

**Past projects:** `scripts/import_past_projects.py` loads closed construction phases from a TheHub export (`raw_pavements.xlsx`) as `status = 'CLOSED'`.

- It creates one row per Hub route segment.
- Cost is split by length.
- Construction codes are mapped to treatments.
- The construction year comes from the phase end date.

CLOSED projects appear only as `project_id_YYYY` in the multi-year views (Multi-Year Analysis popovers). They don't change the engine's condition, ages or families.

**Project page** (`/projects/{id}`, `GET /api/projects/{id}/detail` and `/geojson`): a `projects` row is one Hub route segment, so rows sharing `hub_id` are shown together as one project. Covered analysis segments = same `route_id` with overlapping milepoints (`begin_mp < emp AND end_mp > bmp`). Condition summary is length-weighted (avg CCI, % Good / Fair / Poor by miles).

- **Expected cost** = TheHub `Project.ConEstimatedCost` (else the construction phase programmed amount). **Actual cost** = OASIS `ACTU_EXP_AM` summed over all phases (construction-only shown separately). PMS `projects.estimated_cost` is 0 for the imported history, so it isn't used.
- **PMS model estimate** = what a run would charge for the project's treatment on its covered analysis segments (the one pricing function, section 7: each segment's pavement rate, route-group adjustments, the config's inflation), at the config's start year and in the construction year (deflated for past years).
- Per-route-segment and per-segment shares of Hub costs are split **by length**.
- Hub detail by `hub_id`: `GET /api/hub/projects/by-hub-id/{hub_id}` uses the cached pavement set, else reads the project directly without the pavement/status filters (about 25% of PMS projects fall outside the set).

**Projects list filters** (`GET /api/projects`): repeatable `year` (construction year), `treatment`, `status`, `name` (exact project name), `hub_id` and `q` (free text, case-insensitive substring of name, route, Hub id or treatment; wildcards in it are matched literally). Values of one parameter are OR'ed, different parameters AND'ed; every `q` must match. `GET /api/projects/suggest?q=` returns up to 6 suggestions per kind (years and Hub ids by prefix, treatments by id or catalog name, statuses and names by substring), each with its row count, for the page's search box.

**Project condition outlook** (`GET /api/projects/{id}/outlook?treatment=&scope=project|segment`): runs the segment projection below for every covered analysis segment (doing nothing, and with the treatment applied now — default the project's treatment). `scope=segment` (also on `/detail` and `/geojson`) limits it to the one route segment (projects row) instead of the whole Hub project. The treated scenario exists only when `treatment_applies`: the project is not `CLOSED` and its `construction_year` is 2025 or later (`ACTIVE_FROM_YEAR`, `api/routes/project_detail.py`); otherwise the treatment is already in the surveyed condition, so the outlook is today's condition doing nothing and `treatment_options` is empty. The segment page defaults to a project's treatment only under the same rule. The **project average** of each index and raw measure is length-weighted over the segments that have it; **share of lane-miles** per year sums each segment's projected MAP-21 rating; **years to Poor** for the project = first year most of its lane-miles are Poor.

**Segment page** (`/segments/{id}`, `GET /api/analysis-segments/{id}/detail?treatment=&project_id=`): the outlook runs the dTIMS model (`dtims_state.simulate`, sections 2–4) from the segment's starting state in the current year, for 20 years.

- **Do nothing:** every index follows its anchored family curve (CCI on its own); IRI, rutting, cracking and faulting follow PSI, RDI and age, and give the year's MAP-21 rating.
- **With treatment (applied now):** the treatment's reset operations, then the new family and re-anchoring. The response carries the indices, `raw` (`iri`, `rut`, `pcrk`, `flt`) and `gfp` per year for both scenarios.
- Default treatment: the `?treatment=` choice, else the opening project's, else the most recent covering project's, else the committed treatment.
- **Years to Poor** = first projected year rated Poor (MAP-21). **Measured history** = length-weighted 2020–2025 values from `multi_year_segment_analysis` cells overlapping the segment.
- **Segment cost** = what a run would charge (the one pricing function) in the config's start year and the next five years.

**Committed Projects page:** reads TheHub live and is display-only. It does not write to `projects` or to the commitment flags. See [section 11](#11-integrations).

### 9a. Run validation

**Data** (migration `024_run_validation.sql`). A run's plan is `analysis_runs.result_summary.work_program_summary.project_summary`. Each row is one project (one or more touching joints, see *Projects* above) with one treatment in one program year. Each row becomes a **plan item**, which moves, simulates and commits all of its joints together:

- **Key:** `j<joint_id>@<original program year>`. The key stays the same when the item is moved. Added items use `add-<id>`.
- **Name:** county + route sign + number + direction + milepoints.
- **District:** the length-dominant `analysis_segments.district_code` of the joint's segments. If that is missing, it falls back to the county from the route ID's first two digits (`api/districts.py`, the DOT-12 county → district table).

**Diffs.** `run_plan_edits` is the log, and rows are **never deleted**. Each row stores:

- the **full item before and after** (`null` for an add or delete),
- a comment, the author and the target district,
- a status: `applied`, `proposed`, `denied`, `withdrawn` or `reverted`.

Applied edits carry a per-run `seq`. `run_plan_state.head_seq` is the version.

- **Current plan** = the optimizer's items, with every applied edit replayed in `seq` order (`plan[key] = after`). This lives in `api/validation/plan.py`.
- **Revert** appends an edit whose after is the original's before (like `git revert`) and marks the original `reverted`. It is refused unless the item still equals the original's after.
- **Reset** reverts every applied edit, newest first.
- **Conflicts:** an edit sent with a stale `base_seq`, when the item has changed since, gets 409. **Approve** re-checks that the item still matches the proposal's before.

**Cost** of a moved, re-treated or added item: what the optimizer would charge for its treatment on its joints in its year — the one pricing function (section 7) on the run's segments, with the run's config version and inflation (`RunContext.price`). An unchanged optimizer item costs exactly what the run stored.

**Project window outlook** (`GET /api/runs/{id}/validation/projects/{key}`, `_outlook` in `api/routes/validation.py`):
- It simulates the project's segments with `ds.simulate` over the plan horizon, doing nothing and with the item's treatment in its program year.
- It returns length-weighted project averages of every index and raw measure, and each year's lane-mile share Good / Fair / Poor.
- A raw measure (IRI, rutting, cracking, faulting) is averaged only over the segments whose rating uses it on their pavement (the profile's `gt_<metric>_u`). Before v1.8.9 every segment counted, so faulting and rutting were diluted by segments they don't rate.
- `by_segment` gives every segment's own condition per year, both ways. The window's Segments grid draws it. It is about 220 KB for an 80-segment, 14-year project. Per segment and year it carries:
  - the indices, null where `ds.applies` rules one out for the pavement;
  - the raw measures, null where the rating doesn't use them;
  - the MAP-21 rating.

**Card colour.** A card's condition stripe is the joint's length-weighted CCI projected, with no treatment, to the start of its lane's year (`RunContext.cci_paths`, one engine ageing step per year, cached per run), so the same road turns from Good to Poor as it's dragged into later years. The tooltip shows both today's CCI and the projected one.

**Replay.** Validate rebuilds the run as it was made: its config version (`config_versions`), its run spec (start year, economics) and its starting inventory (`run_snapshots`), all pinned while it simulates and prices. `GET /api/runs/{id}/validation?network=today` shows the plan on today's inventory and config instead (read-only view). Runs made before v1.7 have no snapshot or spec: they use today's inventory and their config as pinned at the first edit after v1.7 (`sanity.inputs` says which).

**Footers.** Per-year cost is the sum over items. **% Good / Fair / Poor** comes from re-simulating the **run's whole analysis network**: every segment the run analysed (its stored starting inventory, else loaded with the run's `segment_filter` and district-balancing clause).

- Each year the plan's treatments are applied to their joints' segments, then the whole network ages one year.
- This uses the engine's fixed-plan simulator, `_simulate_trajectory_with_milp_selections` (the dTIMS model, section 3 timing): MAP-21 Good / Fair / Poor, by lane-miles. Runs made before v1.6 stored CCI bands, so the stored-results check reports `reason: 'gfp_basis'` for them instead of a data change. Each card's stripe is the MAP-21 class covering most of its lane-miles in its year with no work before (`gfp_path`); the project window's outlook shows the indices, raw distress and share of lane-miles Good / Fair / Poor, doing nothing vs the treatment in its year.
- With no edits a replay reproduces the run's stored results exactly (0.0 pp for runs 309 and 310); a difference above 0.05 pp on a replay is reported as a bug. Older runs replayed on today's data warn that the data changed.
- The deltas are against the optimizer plan simulated the same way.
- The segment frame is cached per worker (the last 3 runs), and simulations are cached per set of selections.

**Commit.** Committing an item (admin, or an approved district request) inserts a `projects` row:

- `status = 'planned'`, the card's name, route and milepoints, treatment and cost;
- `program_year` = `construction_year` = the run's start year + program year − 1;
- `source_run_id` and `source_key`, which are unique together, so an item can't be committed twice.

It also sets `analysis_segments.is_committed / committed_treatment_id / committed_program_year / committed_project_id` on the joint's segments, so future runs lock it in (see above). Uncommitting, or reverting a commit, deletes that row and clears the flags.

**Roles** (`api/authz.py`). `app_users.role` is `admin` or `district`, and district users have rows in `app_user_districts`. Every validation endpoint scopes items, proposals, candidates and live events to the user's districts. A district user's edits are stored as `proposed` and must carry a comment. Approve, deny, revert, reset and the Users API are admin-only. New users start as admins (`SSO_DEFAULT_ROLE`).

**Live updates.** Each write runs `pg_notify('pms_run_validation', …)` in its transaction:

- Each API worker keeps one `LISTEN` connection and forwards events to its Server-Sent-Events clients (`GET /api/runs/{id}/validation/stream`).
- Events are filtered by district and include presence (who is viewing).
- Single edits carry the edit itself. Batches and payloads over 7.8 KB tell clients to refetch.
- Recomputed totals follow as a `totals` event tagged with `head_seq`, so a stale result is ignored.

---

## 10. Potential projects

`scripts/find_potential_projects.py` looks for spans where condition improved sharply between consecutive survey years (Y−1 → Y, for Y from 2021 to 2025). It uses NHS segments, working from raw condition history.

**Per-distress strength** = weight × (min(max((prior − current) ÷ big drop, 0), 1.5) + crossed), where *crossed* = prior ≥ "bad" and current < "good":

| Distress | Bad | Good | Big drop | Weight |
|---|---|---|---|---|
| IRI | 120 | 95 | 50 | 1.0 |
| Cracking % | 15 | 5 | 15 | 1.2 |

**When a segment counts as a reset:** IRI must fire (strength > 0.6, or > 0.3 when the following year stays low).

**How resets form a span:** segments are chained along the route. A chain breaks at gaps > 0.1 mi or after 5 quiet segments. A kept span needs:

- at least 5 segments
- at least 1.0 mi
- at least 5 resets
- no IRI rebound over 40 the next year

**Output:** the score is the mean strength over the span. Overlapping later detections are dropped. The table is rebuilt each time the script runs.

---

## 11. Integrations

**TheHub (SQL Server).** Read live through an SSH tunnel (`HUB_DB_*`; locally `127.0.0.1:1434`, on mmsdev `127.0.0.1:11433`), read-only and short-lived connections. If it can't be reached, the API returns 503 and the page shows a banner.

- **Pavement** = STIP Resurfacing program (6), or construction code 07, 08, 09, 13, 14, 15, 75 or 76 (primary or additional). Terminated, withdrawn, non-construction and reserve statuses (12–15, 50, 90–95) and migration-test rows are excluded.
- **Completed** = status 10 or 11, or an actual COMPLETE CONST. (20) milestone date.
- **Active** = status 07, AF, AI, HF or HI with the construction phase Open. Anything else is dropped.
- **Year:** completion year for completed projects (falling back to the construction phase end date, flagged as estimated), otherwise the letting year.
- **Milestones:** 14 Let, 15 Award, 18 Start, 20 Complete (construction phase).
- **Spending:** OASIS actuals from `[external].BUD_STRU_PHASE_PROG2`, all phases.
- **Caching:** 60 s for status, 5 min for projects; `POST /api/hub/refresh` clears it.

**roads2 LRS.** `operations.roads2` in the `ROADS_DB_NAME` database: one MULTILINESTRINGZM per route, SRID 3747, M = milepoint (miles). It has no version column; the pipeline records a fingerprint (row count + md5 of route ids, measure ranges and lengths) on every refresh.

- **Geocoding** (GPS → route + milepoint) runs on roads2 through `lrs/geometry_to_measure.py`, served as `POST /api/lrs/geometryToMeasure` (same request/response as the dashcam service; session or service-token auth; [LRS API](/docs/PMS_LRS_API)) and called directly by the data pipeline. Nothing in PMS calls an external geocoder.

- Each Hub segment is cut with `ST_LocateBetween(geometry, bmp, emp)` (or `ST_LocateAlong` for a point) and shown in WGS84. Segments whose route isn't in roads2 are flagged "not on LRS".
- `/api/hub/tiles/roads2/{z}/{x}/{y}.mvt` serves the context road layer, with fewer, simpler roads at low zoom.

**Sign-in (WVDOT identity broker).** PMS is a confidential OIDC client (`pms`) of the broker at `https://ocidev.transportation.wv.gov/auth`, which fronts Entra/SAML. PMS never handles SAML or passwords.

- **Flow:** `GET /api/auth/sso/login` → broker authorize (authorization code, scope `openid profile email`, with `state` and `nonce`) → Entra → `GET /api/auth/sso/callback`. The code is exchanged server-side with the client secret; the ID token is verified (RS256 against the broker JWKS, `iss`, `aud`, `exp`, `iat`, `sub`, and our `nonce`). Endpoints come from the discovery document (cached 1 h).
- **State/nonce** travel in a 10-minute signed cookie (`pms_sso_state`). Unknown, expired or replayed state is rejected.
- **Session:** a signed HttpOnly cookie (`pms_session`, HS256 with `SESSION_SECRET`, 12 h, `Secure` on mmsdev). There are no refresh tokens, and the broker has no logout endpoint, so **Sign out** ends only the PMS session.
- **Users** (`app_users`, migration 023): matched on `sub` (employee ID), falling back to email so an admin-created row is adopted. Login refreshes name, email and `last_login_at` only; **role is never overwritten**. New users get `SSO_DEFAULT_ROLE`, currently `admin` for everyone. Each user may pick an avatar colour on Profile (`app_users.avatar_color`, migration 047, `'#rrggbb'` or NULL for the default slate; `PUT /api/users/me/avatar-color`, profile at `GET /api/users/me`); it rides on `/api/auth/me` and on Validate presence events (`color`).
- **Enforcement:** when sign-in is configured, every `/api/*` request except `/api/auth/*` needs a valid session (401 otherwise); `/health` and the app shell stay public so the sign-in page can load. If any SSO setting is missing, sign-in is off and the API is open (local development without SSO).
- **Registered callbacks:** `https://mmsdev.transportation.wv.gov/pms/api/auth/sso/callback` and `http://localhost:8000/api/auth/sso/callback`. The redirect URI must match byte for byte.

**nexuslrs.** The route search boxes query `https://nexuslrs.com/api/autocomplete` directly from the browser.

**lrsops.** The pipeline uses `lrsops rhoverlay` (download the LRS attribute layers and layer 70), `lrsops intersections` (optionally, to rebuild `intersections.sqlite`) and `lrsops overlay` (split the grid by joints and attributes).

**Bridges and BMS (v1.8).** The app is **AMPS** (Asset Performance &
Expenditure); PMS is one of its folders. The bridge inventory, the Bridge Wizard and BMS
planning run in the same app and share its sign-in, `app_users` roles and
districts, TheHub client (`api/hub_client.py`) and roads2 tiles. Their state
lives in the `bms` schema of this database (migrations 043–046) and their
logic is documented separately in [BMS — Business Logic](/docs/BMS_Business_Logic).
Run validation is shared code: `api/validation/events.py` serves one LISTEN
hub per channel (`pms_run_validation` for pavement, `bms_run_validation` for
bridges), and the Validate page (`components/validation/ValidationWorkspace.tsx`)
takes a domain adapter (`pavementDomain` / `bridgeDomain`) for units, badges,
treatments and maps. Pavement behaviour is unchanged.

---

## 12. Known gaps and discrepancies

Where the code today differs from the intended model or the older docs. Fix the code or this list, but don't leave them out of sync.

**Runs and optimization**

- **MILP-assist** checks first treatments' triggers and sequencing against each joint's no-treatment state and allows one treatment per joint over the whole horizon (two with `milp_max_actions` = 2, the second only in the first year the treated joint loses Good), so a joint's committed project can't be followed by another treatment in the same run. There's no automatic fallback to greedy if it fails.
- `use_faulting_for_jci` is accepted by the API but not read by the engine.
- **Benefit integration is a stand-in.** dTIMS's GET4CAV_PVDIFF integration and discount timing aren't published; PMS uses trapezoid weights at 4% a year (configurable per config).
- **Ported from dTIMS on 2026-09-29/30:** the county treatments (County Thick / Thin Overlay, County MicroSurface: flat county rates; their inventory IRI, patching and ADT gates, migration 055), the Fair-GFP "70% Good" treatment (`FAIR_TO_GOOD`, MAP-21 Fair trigger; in config 1 and the Non-NHS configs) and PM Asphalt (`CCI_FROM_MIN`). **Not ported:** PM Concrete, the four committed slots (PMS has one), remaining service life, and dTIMS's scenario objective (PV cost normalisation; MILP-assist's `milp_cost_basis = present_value` discounts costs the same way but is not the same objective). Patching is loaded from dTIMS's network (stage F2), so the county thick overlay's patching branch can pass. The HPMS code is approximated by the `HPMS_1` route group (functional class 1–3).
- **Legacy code paths:** `engine/runner.py` (`run_optimization_pipeline`, used by `scripts/pms_cli.py optimize`) and the unused `/api/deterioration/*` forecasts still use the pre-v1.6 projector; the app, `scripts/run_optimization.py` and every page use `dtims_state`.
- **Cracking measure:** configs choose FHWA_Percent_Cracking (`fhwa`, federal HPMS measure) or the vendor's PERCENT_CRACKING (`dtims_percent`, what dTIMS read); both are on every survey year.
- **Unsurveyed road** carries no condition data; with `unsurveyed_policy = 'dtims_defaults'` it gets dTIMS's no-data defaults, which rate it Good — a modelling convention, not a measurement.

**Data and seeds**

- **Crack seal and preservation never trigger on asphalt** (as in dTIMS): their windows are on CSI, which is 0 on asphalt (or 5 after a full reset). Edit the windows per config to change that.
- `treatment_costs_lookup` isn't read by the engine. Costs come from `treatment_costs`.
- `potential_projects` has no migration (the script creates it), and migrations 016 and 017 are missing from the sequence.
- `multi_year_condition_analysis` isn't refreshed by the import scripts.

**Projects and commitments**

- **Commitment flags aren't re-synced** when projects are edited in the app. Overlapping committed projects pick a winner unpredictably.
- **A calendar-year `program_year`** (for example 2027) would lock a segment for the whole horizon, because it exceeds every program year.
- `budget_scenarios` comments describe calendar-year keys; the UI stores program years 1…N.

**Exports**

- The Excel **Configuration sheet** shows the *current* treatments, triggers, resets and families, not those in force when the run happened.

**Found in the 2026-09-30 review of the pipeline, configuration and optimizer code** (each is described as the code behaves in sections 3–8; none is fixed yet):

- **Soft constraints that are only reported.** District **floors** and treatment-**mix floors** never boost anything: no caller computes `district_floor_boost` / `category_boost`, and `penalty_weight` / `boost_strength` are not read. District ceilings, treatment caps, route priority and the network-target boost do act (section 8.7).
- **`min_qualifying_fraction` does nothing.** The config constant is never passed to the trigger evaluator on any run path, so it is always 0.
- **`use_faulting_for_jci` does nothing.** It is stored and passed into the engine settings but never read.
- **Greedy buys zero-benefit steps when money is left.** The frontier keeps steps with equal or zero benefit (ratio 0, only strictly dominated steps are dropped), and with the default `minimum_bc_ratio` 0 they are bought when budget remains. Set a tiny positive minimum (e.g. 1e-12) for large or unlimited budgets (section 8.6).
- **Committed joints under 0.25 mi aren't forced by greedy** (the minimum joint length filter drops them first); MILP-assist has no such filter.
- **MILP-assist ignores** treatment caps, district ceilings and route priority (district filters still apply at load). Its joint metadata takes the first segment's district / county / lanes (only surface is length-dominant), and its `district` value is the code (`7`) where greedy's is the label (`07-District 7`).
- **Even-spending rows apply to every year 1…N**, but first actions are offered only through the last target year: with a target year before the horizon end, a share-of-peak rule forces zero spending and a spend floor makes the model infeasible.
- **Target years:** only `target_year` is checked against the request's `analysis_years` (not the budget scenario's horizon); `poor_target_year` isn't checked.
- **Three run options have no request field** (`clamp_trigger_lowers`, `strategy_prep`, a `discount_rate` override): they work only when written into a stored run configuration; any `strategy_prep` other than `segment_union` raises.
- **Counter names are fixed by a CHECK constraint** on `treatment_triggers` (`cnt_chip`, `cnt_micro`) although counters are per-config data.
- **Carryover with committed overspend** carries a negative remainder into the next year.
- **Runs start with an empty treatment history**: sequencing, intervals and years-since gates see only treatments applied inside the run, not past projects.
- **Commitment ties:** where several committed projects overlap a segment the SQL ranks them but doesn't filter on the rank, so which one wins is undefined.
- **Columns never written by the pipeline:** `hpms_flag` / `hpms_source` (set once by migration 031, NULL after the next swap), `inventory_rehab_type`; `reconflate_normalized.overall_grade` and `.aadt` are always NULL; `analysis_segments.lanes` is 2 everywhere and `current_age` 0 everywhere.
- **Stage B doesn't rename `Percent_Cracking`** (the 2020–2022 spelling), so `condition_history.crack_percent` is empty for those years; stage C does rename it.
- **Stage E's failure message** says live data was unchanged, but a family-rule failure happens after the swap and the E1 / family reruns already committed.
- **A `segments` run alone clears the commitment flags** until `commitments` runs.
- **Joints exist only on routes in the `routes` table** (15,124 routes, none HARP), so most unsurveyed road (114,580 of 183,308 rows in the 2026-09-30 build) has no joint and can't be treated.
- **Stale descriptions in code:** the `pipeline/families.py` docstring and the Config page's CCI hover still say CCI = min(indices) and "equivalent ages"; the workbook's Family Curves help says a curve change recomputes ages (it changes nothing stored); some route and workbook docstrings still mention a `delete_runs` confirmation for edits; the `BundlingBonus` docstring says it is implemented in the heap loop (it is reported only); migration 031 lists `age_basis` value `default15` (the code writes `no_rehab`); `pipeline/__init__.py` lists LRS layer 36 (the code downloads 22); `backup_pms.py --mmsdev` still reads the decommissioned `~/pms/env.txt`.
- **Schema DDL outside migrations:** stage B still runs `ALTER TABLE … ADD COLUMN IF NOT EXISTS` / `DROP CONSTRAINT IF EXISTS` on `condition_history` (no effect on a migrated database). `scripts/import_past_projects.py` queries `treatments` without `config_id`.
