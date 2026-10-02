# WVDOT PMS System Architecture

> Implementation-level documentation for the West Virginia DOT Pavement Management System (this repo). This is the "start here" doc: it maps every component to its directory, describes how data flows from raw vendor files to the rendered Run Detail page, and links to the deeper topic-specific docs.

---

## Table of Contents

1. [What the PMS does](#1-what-the-pms-does)
2. [The five subsystems](#2-the-five-subsystems)
3. [Directory layout](#3-directory-layout)
4. [Data flow — from raw files to work program](#4-data-flow--from-raw-files-to-work-program)
5. [Lifecycle of a single analysis run](#5-lifecycle-of-a-single-analysis-run)
6. [Technology choices](#6-technology-choices)
7. [Where to go next](#7-where-to-go-next)

---

## 1. What the PMS does

The WVDOT Pavement Management System answers one question:

> **Given N dollars per year for Y years, which treatments should we apply to which pavement segments to maximize the long-run condition of the West Virginia state highway network?**

Inputs:

- **Network geometry** — every 0.1-mile LRS segment of the WV state system (~260 K segments), with lanes, AADT, pavement type, and a pavement family for the deterioration model.
- **Condition measurements** — yearly IRI, rutting, cracking, and faulting surveys, converted into six dTIMS-style condition indices: PSI, RDI, SCI, ECI, JCI, CSI (each 0–5 scale, 5 = best), plus a composite CCI.
- **Treatment catalog** — 14 state-route treatments (9 BC + 5 RC) with unit costs, trigger windows, condition-reset rules, and minimum re-application intervals.
- **Deterioration models** — per-family, per-index regression curves from dTIMS (polynomial, linear, sigmoid, log) that describe how each index decays with age.
- **Budget & horizon** — an annual budget, analysis period in years, and optional carryover / minimum-B/C filter.

Outputs:

- **Year-by-year work program** — for each of the Y years, which pavement *joints* (contiguous groups of segments) should receive which treatment, at what cost and benefit.
- **Network condition trajectory** — `% Good / Fair / Poor` across the network at the end of each year.
- **Treatment distribution** — how spend, projects, and lane-miles are split across treatment types and across years.
- **Excel export** — the same data downloadable as a multi-sheet XLSX.

The system is accessed through a React web UI backed by a FastAPI service that calls a pure-Python optimization engine.

---

## 2. The five subsystems

| # | Subsystem | Where it lives | Responsibility |
|---|-----------|----------------|----------------|
| 1 | **Data pipeline** | `scripts/import_pavement_data.py`, `db/load_*.py`, `create_analysis_segments.py` | Pulls raw LRS data, vendor surveys, joints, and treatment catalog into Postgres; produces the `analysis_segments` working table that the engine reads. |
| 2 | **Database** | Postgres 15, `db/schema.sql` + `db/migrations/*.sql` | Single source of truth for the network, treatment catalog, condition history, deterioration models, and analysis-run bookkeeping. |
| 3 | **Analysis engine** | `engine/` (pure-Python + Polars) | The optimization engine. Loads `analysis_segments` + the treatment catalog, runs year-by-year rolling optimization, writes results + logs + progress back to Postgres. |
| 4 | **API layer** | `api/` (FastAPI) | REST endpoints for launching runs, polling progress, reading run results, serving the work program as JSON or Excel, serving documentation markdown. |
| 5 | **Web UI** | `ui/` (React + Vite + MUI + TanStack Query) | Runs list, Create-Run dialog, live Run Detail page (trajectory chart, treatments heatmaps, projects grid, log stream), this documentation viewer. |

```
┌──────────────────────────────────────────────────────────────────────┐
│                              Web UI (React)                         │
│     Runs list · Create Run dialog · Run Detail (live) · Docs        │
└──────────────┬───────────────────────────────────────┬──────────────┘
               │ REST + JSON                           │
               ▼                                       ▼
        ┌────────────────┐                      ┌────────────────┐
        │   FastAPI      │                      │   FastAPI      │
        │ /api/runs/*    │   spawn thread ──▶   │ /api/docs/*    │
        │ /api/segments/*│                      │ (markdown)     │
        └───────┬────────┘                      └────────────────┘
                │
                ▼
    ┌───────────────────────┐        ┌─────────────────────────┐
    │  Analysis engine      │◀──────▶│      Postgres           │
    │  runner · chunked     │        │ analysis_segments       │
    │  optimization · IBC   │        │ treatments / triggers / │
    │  deterioration models │        │   resets / families     │
    │  benefits / weighting │        │ analysis_runs / run_logs│
    └───────────┬───────────┘        └─────────────────────────┘
                │
                ▼
       ┌──────────────────┐
       │  Data pipeline   │
       │  import_pavement │
       │  lrsops overlay  │
       │  CSV → Postgres  │
       └──────────────────┘
                ▲
                │
        raw vendor files
      (LRS, joints, survey)
```

The boundary between the engine and the API is intentionally thin: the engine can run standalone from the CLI (`example_full_workflow.py`, `run_wv_optimization.py`) — the API is basically a thread pool + progress reporter wrapped around it.

---

## 3. Directory layout

```
pms/
├── api/                        # FastAPI service
│   ├── main.py                 # app factory, CORS, router registration
│   ├── database.py             # SQLAlchemy session + SessionLocal
│   ├── models/                 # SQLAlchemy ORM models
│   └── routes/
│       ├── runs.py             # POST /runs, GET /runs/{id}/*, export
│       ├── docs.py             # GET /docs (markdown whitelist)
│       ├── segments.py, routes.py, treatments.py, ...
│       └── ...
│
├── engine/                     # Pure-Python / Polars optimization engine
│   ├── runner.py               # Top-level orchestrator
│   ├── db.py                   # Load treatments / triggers / resets / segments
│   ├── exports.py              # Excel export
│   ├── progress.py             # ProgressTracker (writes to analysis_runs)
│   ├── log_capture.py          # DatabaseLogHandler (writes to run_logs)
│   ├── reporting.py            # summarize_work_program → result_summary JSON
│   ├── polars_utils.py         # Polars helpers
│   ├── condition/              # PSI/RDI/SCI/ECI/JCI/CSI/CCI computation
│   │   ├── indices.py
│   │   ├── deductions.py
│   │   └── pci.py              # legacy PCI 0-100
│   ├── deterioration/          # Curve families + year-by-year projection
│   │   ├── families.py
│   │   └── models.py
│   ├── treatments/             # Trigger evaluation + reset application
│   │   ├── triggers.py
│   │   └── resets.py
│   ├── benefits/               # AUC benefit + AADT-power weighting
│   │   ├── auc.py
│   │   └── weighting.py
│   └── optimization/           # Work program + IBC
│       ├── work_program.py     # generate_work_program_polars (in-memory)
│       ├── chunked.py          # generate_work_program_chunked (parquet)
│       ├── ibc.py              # Incremental B/C heap selection
│       ├── constraints.py      # Soft constraint enforcement (quotas, boosts)
│       ├── constrained_work_program.py  # Target-chasing outer loop
│       └── scenarios.py
│
├── db/                         # Schema + migrations + loaders
│   ├── schema.sql              # Phase-1 tables (created first)
│   ├── migration_to_dtims.sql  # Convert raw-measurement → index-based
│   ├── migrations/
│   │   ├── 001_add_pci_columns.sql
│   │   ├── 002_add_deterioration_models.sql
│   │   ├── 003_add_program_year.sql
│   │   ├── 004_pavement_joints.sql
│   │   ├── 005_add_trigger_type.sql
│   │   ├── 006_analysis_runs.sql
│   │   ├── 007_refresh_triggers_from_2025_12_17.py
│   │   ├── 008_add_committed_columns.sql
│   │   ├── 009_multi_year_segment_analysis.sql
│   │   └── 010_multi_year_condition_analysis.sql
│   ├── load_routes.py
│   ├── load_segments.py
│   ├── load_pavement_joints.py
│   ├── load_condition_history.py
│   ├── load_actual_milepoints.py
│   ├── load_reconflate_normalized.py
│   ├── migrate_condition_indices.py
│   ├── seed_pavement_families.py
│   ├── seed_treatments.py
│   └── seed_treatments.sql
│
├── scripts/
│   ├── import_pavement_data.py # Top-level orchestrator for raw → Postgres
│   ├── import_past_projects.py # Load historical projects from WVDOH Hub
│   ├── populate_committed_flags.py
│   ├── joint_breakdown.py      # Joint-level analysis utilities
│   ├── joint_breakdown_intersections.py
│   ├── pms_cli.py              # CLI entry point
│   └── run_optimization.py     # CLI optimization runner
│
├── create_analysis_segments.py # End-to-end build of analysis_segments
├── run_wv_optimization.py      # CLI run harness
├── example_full_workflow.py    # End-to-end example
│
├── ui/                         # React frontend (Vite)
│   └── src/
│       ├── pages/              # RunsPage, RunDetailPage, DocPage, ...
│       ├── components/         # DataTable, HeatmapPivot, CreateRunDialog
│       ├── hooks/              # useRuns, useDocs, ...
│       ├── api/client.ts       # axios client
│       ├── types/runs.ts       # TS mirror of API response shapes
│       └── layouts/AppLayout.tsx   # AMPS app bar: folder menus (hover), avatar menu
│
├── dtims_docs/                 # Markdown documentation served to the UI
│   ├── WVDOT_PMS_Overview.md
│   ├── WVDOT_PMS_System_Architecture.md   ← this file
│   ├── WVDOT_PMS_Database_Reference.md
│   ├── WVDOT_PMS_Analysis_Engine.md
│   ├── WVDOT_PMS_Optimization_Logic.md
│   ├── WVDOT_PMS_Other_Optimization_Strategies.md
│   ├── WVDOT_PMS_Data_Pipeline.md
│   ├── dTIMS_PMS_Documentation.md
│   ├── dTIMS_Treatment_System_Deep_Dive.md
│   ├── dTIMS_Pavement_Families.md
│   ├── dTIMS_Pavement_Family_Coefficients.md
│   ├── dTIMS_Proprietary_Curve_Reference.md
│   ├── Raw_Measurements_to_Condition_Indices.md
│   ├── Migration_to_dTIMS_Model.md
│   ├── Import_Analysis_Segments.md
│   ├── Import_Past_Projects.md
│   └── Segment_Breakdown_Intersections.md
│
└── tests/
```

---

## 4. Data flow — from raw files to work program

There are three distinct data flows in the system. Keep them separate in your head — the same Postgres database holds all three, but the code paths are independent.

### 4.1. Ingest flow (offline, rarely run)

Triggered when a new vendor survey, LRS update, or treatment catalog lands. Source: `scripts/import_pavement_data.py` + the `db/load_*.py` helpers + `create_analysis_segments.py`.

```
raw CSVs + shapefiles + Excel catalog
         │
         ▼
   load_routes.py           ──▶  routes
   load_segments.py         ──▶  segments
   load_pavement_joints.py  ──▶  pavement_joints
   load_condition_history   ──▶  condition_history, reconflate_normalized
   seed_treatments / seed_pavement_families / migration_to_dtims.sql
                            ──▶  treatments, treatment_triggers,
                                 treatment_resets, pavement_families
         │
         ▼
   lrsops overlay (external CLI)
         │
         ▼
   create_analysis_segments.py
                            ──▶  analysis_segments  (working table)
```

See [Data Pipeline doc](WVDOT_PMS_Data_Pipeline.md) for the full step-by-step.

### 4.2. Analysis flow (every run)

Triggered by `POST /api/runs` from the UI, or directly from the CLI. The engine reads from the tables the ingest flow filled in, and writes results back to `analysis_runs` + `run_logs`.

```
POST /api/runs   ──▶   api/routes/runs.py : create_run + _execute_run thread
                                 │
                                 ▼
         engine/runner.py : run_analysis / generate_work_program_chunked
                                 │
              ┌──────────────────┼──────────────────┐
              ▼                                     ▼
     READ                                    WRITE (incrementally)
   analysis_segments                       analysis_runs.progress_pct
   treatments                              analysis_runs.progress_step
   treatment_triggers                      run_logs (batched inserts)
   treatment_resets
   pavement_families
              │
              ▼
       year-by-year rolling loop
       (see Analysis Engine doc)
              │
              ▼
     WRITE FINAL
   analysis_runs.status     = 'completed'
   analysis_runs.result_summary = <JSON blob>
   analysis_runs.completed_at
```

`result_summary` is a single JSONB blob containing the entire work program, yearly summary, treatment mix, distribution pivots, and project list. The UI reads it through `GET /api/runs/{id}/configuration` and renders every view from it — no separate result tables on the read path.

See [Analysis Engine doc](WVDOT_PMS_Analysis_Engine.md) for the full phase-by-phase breakdown.

### 4.3. Read flow (UI polling a run)

```
GET /api/runs/{id}/progress        ──▶  analysis_runs (progress_pct, status)
GET /api/runs/{id}/configuration   ──▶  analysis_runs.configuration + .result_summary
GET /api/runs/{id}/projects        ──▶  analysis_runs.result_summary.project_summary
GET /api/runs/{id}/logs            ──▶  run_logs (paginated, tailable while running)
GET /api/runs/{id}/export.xlsx     ──▶  engine/exports.py → tmpfile → stream
```

While the run is in-progress the UI polls `/progress` at ~1 Hz so the progress bar and log tail stay live. The engine's `ProgressTracker` writes `progress_pct` / `progress_step` directly to the `analysis_runs` row as it advances (`engine/progress.py:22-56`), and `DatabaseLogHandler` batches log records into `run_logs` (`engine/log_capture.py:25-86`).

---

## 5. Lifecycle of a single analysis run

End-to-end, one run executes roughly like this:

1. **UI submits form** — `CreateRunDialog` in `ui/src/components/CreateRunDialog.tsx` builds a `PipelineConfig`-shaped body (annual_budget, analysis_years, power_exponent, minimum_bc_ratio, allow_budget_carryover, **lookahead_years**, segment_filter, run_name) and `POST /api/runs`. `lookahead_years` is the rolling-horizon (MPC) window size — default 3, clamped `[1, 10]`. Setting it to 1 reproduces the legacy greedy single-year engine bit-for-bit; higher values plan over a k-year window each outer year and commit only year 1. See [Optimization Logic §12](WVDOT_PMS_Optimization_Logic.md#12-rolling-horizon-look-ahead).
2. **API creates the row** — `api/routes/runs.py : create_run` (`runs.py:684+`) inserts an `analysis_runs` row with `status='pending'`, stores the config as JSONB, then spawns a daemon thread calling `_execute_run` and returns `{ run_id }` immediately.
3. **Thread acquires lock** — `_execute_run` (`runs.py:352+`) grabs a Postgres advisory lock so only one run executes at a time per process, attaches a `DatabaseLogHandler` to the `engine` + `api` loggers, and flips the row to `status='running'`.
4. **Engine loads inputs** — `engine/runner.py` calls `engine/db.py` to pull `analysis_segments`, `treatments`, `treatment_triggers`, `treatment_resets`, and (optionally) `pavement_families` into Polars DataFrames.
5. **Engine runs the rolling year loop** — see the [Analysis Engine doc](WVDOT_PMS_Analysis_Engine.md) for the full step-by-step. Each year: aggregate segments → joints, build treatment-strategy table, run IBC selection, apply resets to selected joints' segments, advance the rest by one year of deterioration, recompute network `% Good/Fair/Poor`, then loop.
6. **Engine writes results** — `engine/reporting.py : summarize_work_program` collapses the output into the JSON structure that ends up in `analysis_runs.result_summary`. The thread updates the row with `status='completed'` + `completed_at` + the summary.
7. **UI detects completion** — the `/progress` poll returns `status='completed'`, the front-end invalidates queries and reloads the Run Detail page from `/configuration`, rendering the trajectory chart, treatment heatmaps, projects grid, and condition trajectory.
8. **User downloads XLSX** — clicking *Download Excel* hits `GET /api/runs/{id}/export.xlsx`, which calls `engine/exports.py : export_work_program_to_excel` to build a multi-sheet workbook from the stored `result_summary` and streams it back.

If anything in step 4–6 throws, the thread catches it, writes `status='failed'` + the exception message to `error_message`, and the UI surfaces the failure with the recent log lines.

---

## 6. Technology choices

| Layer | Stack | Why |
|-------|-------|-----|
| DB | Postgres 15 | JSONB for `configuration` and `result_summary`; advisory locks for single-run serialization; array + window functions used in a few views. |
| Engine compute | **Polars** (not pandas) | The engine joins 260 K segments × ~14 treatments (~3.6 M-row cross joins before eligibility filters) on every year for a 20-year run. Polars' lazy + vectorized execution is ~10× faster than pandas and lets us stream strategies to parquet chunks when memory is tight (`engine/optimization/chunked.py`). |
| Engine I/O | SQLAlchemy + psycopg2 | Single connection string via `.env` or `PMS_DATABASE_URL`, lazy engine in `engine/db.py:_load_env_file`. |
| API | **FastAPI** + Pydantic v2 | Async-friendly, auto-docs, Pydantic response models mirror the engine's summary dict. |
| Background work | Daemon `threading.Thread` (not Celery) | One run at a time is enforced with a Postgres advisory lock. No broker needed; the UI polls for progress. |
| Frontend | React 19 + Vite + TypeScript + MUI + TanStack Query + Recharts + react-data-grid | MUI for layout, TanStack Query for polling + cache invalidation, Recharts for the trajectory chart, react-data-grid for the projects grid, custom `HeatmapPivot` component for the treatments table. |
| Docs | Markdown + `react-markdown` + custom heading-slug + scroll-spy breadcrumb | Docs are flat `.md` files in `dtims_docs/`, served raw via `/api/docs`, rendered client-side. See `ui/src/pages/DocPage.tsx` for the slug-generation and scroll-spy logic. |

### Why "index-based" and not raw measurements?

Historically the engine worked in the raw-measurement domain (IRI in/mi, rut inches, crack %). In February 2026 the engine was migrated to the dTIMS 6-index model (PSI/RDI/SCI/ECI/JCI/CSI) via `db/migration_to_dtims.sql`. Reasons:

1. **Alignment with WVDOT's dTIMS instance** — WVDOT's canonical curves, triggers, and family coefficients are all defined in the 0–5 index domain. Staying in raw measurements meant constantly converting back and forth.
2. **One curve type per index** — the dTIMS `DAL_DCG_INDEXFROMAGE` expression library gives per-family, per-index deterioration curves (polynomial / linear / sigmoid / log), and those curves operate on indices, not raw measurements.
3. **Composite CCI is simpler** — CCI is just `MIN(PSI, RDI, SCI)` for BC and `MIN(PSI, CSI, JCI)` for RC, which makes the "worst-case" semantics clearer than a weighted deduction-style PCI.

See [Migration to dTIMS Model](Migration_to_dTIMS_Model.md) and [Raw Measurements to Condition Indices](Raw_Measurements_to_Condition_Indices.md) for the full story.

---

## 7. Where to go next

- **[Database Reference](WVDOT_PMS_Database_Reference.md)** — every table, column, FK, and index, grouped by functional area, with a full FK graph.
- **[Analysis Engine](WVDOT_PMS_Analysis_Engine.md)** — phase-by-phase walkthrough of what happens inside a run, with the exact `file:line` of each step.
- **[Optimization Logic](WVDOT_PMS_Optimization_Logic.md)** — the IBC algorithm, budget enforcement, carryover, minimum-B/C filter, and worked examples.
- **[Data Pipeline](WVDOT_PMS_Data_Pipeline.md)** — how raw LRS data, vendor surveys, and the treatment catalog get into Postgres and produce the `analysis_segments` working table.
- **[dTIMS Treatment System Deep Dive](dTIMS_Treatment_System_Deep_Dive.md)** — the WVDOT dTIMS treatment model this engine mirrors (triggers, resets, costs, reset semantics).
- **[dTIMS Pavement Families](dTIMS_Pavement_Families.md)** + **[Family Coefficients](dTIMS_Pavement_Family_Coefficients.md)** — the 18 pavement families and 144 curve coefficients driving deterioration.
- **[dTIMS Proprietary Curve Reference](dTIMS_Proprietary_Curve_Reference.md)** — background on the proprietary dTIMS curve expressions the engine evaluates.
