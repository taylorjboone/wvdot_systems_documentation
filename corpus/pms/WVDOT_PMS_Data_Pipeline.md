# WVDOT PMS Data Pipeline

> **Superseded for refreshing data:** the data refresh is now one staged command documented in [PMS — Data Pipeline](/docs/PMS_Data_Pipeline). This page is kept for background; where they disagree, the Data Pipeline page is right.


> How raw vendor data (LRS shapefiles, condition surveys, Excel treatment catalogs) becomes the `analysis_segments` working table that the analysis engine reads on every run. This is the "before the engine runs" story.

Unlike the analysis flow — which runs many times per day as users submit runs from the UI — the ingest flow runs rarely (once per vendor data drop, maybe a few times per year). But when it does run, it touches the entire Postgres state, rebuilds `analysis_segments`, and can invalidate every saved run's assumptions if the treatment catalog or segment geometry changes.

---

## Table of Contents

1. [What changes, and when](#1-what-changes-and-when)
2. [Overview of the pipeline](#2-overview-of-the-pipeline)
3. [Stage 1 — Base geometry](#3-stage-1--base-geometry)
   - [3.1 Routes](#31-routes)
   - [3.2 Segments](#32-segments)
   - [3.3 Pavement joints](#33-pavement-joints)
4. [Stage 2 — Condition measurements](#4-stage-2--condition-measurements)
   - [4.1 `condition_history`](#41-condition_history)
   - [4.2 LRS overlay via `lrsops`](#42-lrs-overlay-via-lrsops)
   - [4.3 `reconflate_normalized`](#43-reconflate_normalized)
5. [Stage 3 — Treatment catalog](#5-stage-3--treatment-catalog)
6. [Stage 4 — Deterioration families](#6-stage-4--deterioration-families)
7. [Stage 5 — Build `analysis_segments`](#7-stage-5--build-analysis_segments)
8. [Stage 6 — dTIMS migration (one-time)](#8-stage-6--dtims-migration-one-time)
9. [Stage 7 — Committed projects](#9-stage-7--committed-projects)
10. [QA / audit tables](#10-qa--audit-tables)
11. [Refreshing after a new vendor drop](#11-refreshing-after-a-new-vendor-drop)

---

## 1. What changes, and when

| Data class | Frequency | Source | Landing table(s) |
|------------|-----------|--------|------------------|
| Route dictionary | Rarely — when WVDOT renumbers a route or adds a new one | WVDOT LRS | `routes` |
| Segment geometry | Rarely — LRS master table is stable | LRS shapefiles + WVDOT grid | `segments` |
| Pavement joints (project groupings) | When the vendor reshuffles joint IDs | Vendor `70_OBJECTID` field | `pavement_joints`, `segments.pavement_joint_id` |
| Condition surveys | Annually | Vendor CSV/Excel (ARAN, Pathway, etc.) | `condition_history`, `reconflate_normalized` |
| Treatment catalog | When WVDOT updates costs/rules | `2025_12_17_Analysis_Lookup_Triggers.xlsx` etc. | `treatments`, `treatment_triggers`, `treatment_resets`, `treatment_costs_lookup` |
| Pavement families | Rarely — when dTIMS curves are re-fit | `dtims_dump.sqlite` | `pavement_families` |
| Committed projects | Whenever WVDOT programs work | Project list (CSV) | `analysis_segments.is_committed` / `.committed_treatment_id` / `.committed_program_year` |

The common case is step 4: a new year's condition survey comes in, you re-run stages 2 and 5 (`condition_history` → `analysis_segments`), and you're done.

---

## 2. Overview of the pipeline

```
Raw CSVs + Excel + LRS shapefiles + dTIMS dump
                │
                ▼
┌────────────────────────────────────────────────────────┐
│ Stage 1: Base geometry                                 │
│   db/load_routes.py       → routes                     │
│   db/load_segments.py     → segments                   │
│   db/load_pavement_joints → pavement_joints +          │
│                              segments.pavement_joint_id│
└────────────────────────────────────────────────────────┘
                │
                ▼
┌────────────────────────────────────────────────────────┐
│ Stage 2: Condition measurements                        │
│   db/load_condition_history.py → condition_history     │
│   lrsops rhoverlay + lrsops overlay                    │
│                               → reconflate_normalized  │
└────────────────────────────────────────────────────────┘
                │
                ▼
┌────────────────────────────────────────────────────────┐
│ Stage 3: Treatment catalog                             │
│   db/seed_treatments.sql (once)                        │
│   db/migration_to_dtims.sql §7-8 (once, then refresh)  │
│   db/migrations/007_refresh_triggers_from_...py        │
│                               → treatments             │
│                               → treatment_triggers     │
│                               → treatment_resets       │
│                               → treatment_costs_lookup │
└────────────────────────────────────────────────────────┘
                │
                ▼
┌────────────────────────────────────────────────────────┐
│ Stage 4: Deterioration families                        │
│   db/seed_pavement_families.py                         │
│   db/migration_to_dtims.sql §4                         │
│                               → pavement_families      │
└────────────────────────────────────────────────────────┘
                │
                ▼
┌────────────────────────────────────────────────────────┐
│ Stage 5: Build analysis_segments                       │
│   scripts/import_pavement_data.py ANALYSIS_SEGMENTS_DDL│
│   create_analysis_segments.py (reconflate + overlay)   │
│                               → analysis_segments      │
└────────────────────────────────────────────────────────┘
                │
                ▼
┌────────────────────────────────────────────────────────┐
│ Stage 6: dTIMS migration (one-time per schema version) │
│   db/migration_to_dtims.sql §1 → analysis_segments     │
│                                    index columns +     │
│                                    per-index ages      │
└────────────────────────────────────────────────────────┘
                │
                ▼
┌────────────────────────────────────────────────────────┐
│ Stage 7: Committed projects (as needed)                │
│   scripts/populate_committed_flags.py                  │
│                               → analysis_segments.*    │
└────────────────────────────────────────────────────────┘
                │
                ▼
                Ready for the analysis engine
```

---

## 3. Stage 1 — Base geometry

### 3.1 Routes

**Script**: `db/load_routes.py`.

Extracts a unique set of route IDs from the raw vendor CSV, classifies each route's `system_type` and `functional_class` from lookup maps (`SYSTEM_TYPE_MAP`, `FUNCTIONAL_CLASS_MAP`), and inserts into `routes`. Entry point is `extract_routes_from_csv()` at lines 96–168.

Output rows have `route_id`, `route_name`, `system_type`, `functional_class`, `district`, `county`, `total_length_mi`. `nhs_type` comes later from the `lrsops` overlay.

### 3.2 Segments

**Script**: `db/load_segments.py`.

Builds the 0.1-mile LRS grid. For each route, generates segments at the normalized mile-post grid (0.0, 0.1, 0.2, …) up to `total_length_mi`. Segment IDs follow the pattern `{route_id}-{begin_mp:07.3f}` — e.g. `I-77-003.200`.

Each segment gets its `lanes`, `lane_width`, `surface_type`, `direction`, and latitude/longitude from the LRS source. `actual_bmp` / `actual_emp` (LRS-reconciled milepoints) are backfilled later during the condition-reconflate stage.

### 3.3 Pavement joints

**Script**: `db/load_pavement_joints.py`.

Pavement joints are contiguous groups of segments that share a `70_OBJECTID` from the vendor's joint layer. The loader walks the vendor file, assigns `joint_id = {route_id}-J{object_id}`, and does two writes:

1. INSERT into `pavement_joints` with `route_id`, `begin_mp`, `end_mp`, `length_mi`, `segment_count`.
2. UPDATE `segments.pavement_joint_id` to tag each segment with its joint.

The `segments.pavement_joint_id` column is an informal FK — migration 004 deliberately left the constraint commented out because joints may be loaded after segments.

> **Why joints matter.** The engine optimizes at the joint level (see the [Optimization Logic doc §9](WVDOT_PMS_Optimization_Logic.md#9-joint-level-vs-segment-level-selection)). Without a sensible `joint_id` on every row of `analysis_segments`, the engine falls back to synthetic joint IDs, which still works but produces less-realistic project sizes.

---

## 4. Stage 2 — Condition measurements

### 4.1 `condition_history`

**Script**: `db/load_condition_history.py`.

Reads per-segment annual condition records directly from the vendor CSV and inserts one row per `(segment_id, survey_year)` into `condition_history`. Fields: `iri_mean`, `iri_max`, `rut_mean`, `rut_max`, `crack_percent`, `fhwa_crack_percent`, `faulting`, `aadt`, `truck_pct`, and the pre-computed `cci` / `psi` / `rdi` / `sci`.

Later migrations added `eci`, `jci`, `csi` (migration_to_dtims.sql §6) and the legacy `pci_score` + deduction columns (migration 001_add_pci_columns.sql).

### 4.2 LRS overlay via `lrsops`

The vendor's condition data is usually collected against a slightly different LRS grid than ours — segments drift by a few feet, the joint boundaries don't quite line up, a new route extension moved the end mile post. Rather than trying to reconcile by segment ID directly, the pipeline uses an external tool called **`lrsops`** (not part of this repo) to perform LRS overlays.

`create_analysis_segments.py:119-150` shells out to two `lrsops` commands:

1. **`lrsops rhoverlay`** — generates an LRS reference table combining segment geometry with a handful of traffic/coal-route/district/county/NHS attribute layers. Layers used (from `_run_lrsops_rhoverlay`):
   - `15` coal route
   - `35` functional class
   - `36` NHS type
   - `12` county
   - `18` district
   - `49` route status
   - `77` AADT (combined)
2. **`lrsops overlay`** — takes the vendor condition CSV + the LRS reference table and produces a length-weighted normalized condition record for each target segment: IRI, rut, faulting, crack percent, dominant surface type, coverage fraction.

### 4.3 `reconflate_normalized`

The output of `lrsops overlay` is `COPY`'d into the `reconflate_normalized` table. This is the "condition data snapped to our 0.1-mile grid" table, with one row per `(segment_id, survey_year)`.

Columns include:

- Geometry: `actual_bmp`, `actual_emp`, `coverage_pct`
- Metrics: `iri_mean`, `rut_mean`, `faulting`, `fhwa_crack_pct`
- Categorical: `surface_type`, `shoulder_type`
- Grades: `iri_grade`, `rutting_grade`, `faulting_grade`, `cracking_grade`, `overall_grade`

The `segment_condition_by_year` SQL view in `db/schema.sql:366-445` reads `reconflate_normalized` and pivots it by year (2020–2024) for the segment-condition UI.

> **Segments with low coverage.** If the vendor data covers less than some fraction of a segment (e.g. 80 % of the 0.1-mile span), the overlay still emits a row but flags it via the grade columns. The pipeline does not currently reject low-coverage segments — they flow through into `analysis_segments` with the best data available.

---

## 5. Stage 3 — Treatment catalog

The treatment catalog is rebuilt by a handful of scripts that all land data in the four treatment tables:

| Script | What it does | Target tables |
|--------|--------------|---------------|
| `db/seed_treatments.sql` | Initial seed of pre-dTIMS treatments | `treatments`, `treatment_triggers` (legacy), `treatment_resets` (legacy) |
| `db/migration_to_dtims.sql` §2–§8 | Replace legacy tables with index-based dTIMS tables and seed 14 WV state-route treatments | `treatments` (rows re-inserted), `treatment_triggers`, `treatment_resets`, `treatment_costs_lookup` |
| `db/migrations/007_refresh_triggers_from_2025_12_17.py` | Refreshes `treatment_triggers` from the latest vendor Excel (`2025_12_17_Analysis_Lookup_Triggers.xlsx`) | `treatment_triggers` |
| `db/seed_treatments.py` | Alternative loader for treatments + families from the dtims dump | `treatments`, `treatment_triggers`, `treatment_resets`, `treatment_costs_lookup` |

The dTIMS migration is *idempotent for the rebuild case*: it renames the old tables to `*_legacy` and re-creates fresh tables, so re-running it on a machine that's already migrated will fail unless you drop the new tables first. In practice it's a once-per-environment operation.

For a routine *trigger refresh* you run the Python migration (`007_*`), which UPSERTs rows into `treatment_triggers` without touching `treatments` or `treatment_resets`. That's the common path when WVDOT publishes a new lookup Excel.

### The 14 dTIMS state-route treatments

From `db/migration_to_dtims.sql` lines 240–255:

| ID | Name | Pavement type | Service life | Interval | Unit cost per lane-mi |
|----|------|---------------|-------------:|---------:|----------------------:|
| CRACK_SEAL       | Crack Seal            | BC | 3  | 2  | $5 000    |
| PRESERVATION_BC  | Preservation          | BC | 5  | 3  | $25 000   |
| CAPE_SEAL        | Cape Seal             | BC | 5  | 3  | $35 000   |
| CHIP_SEAL        | Chip Seal             | BC | 5  | 3  | $30 000   |
| MICROSURFACING   | Microsurfacing        | BC | 6  | 3  | $40 000   |
| ULTRA_THIN_OVLY  | Ultra Thin Overlay    | BC | 7  | 4  | $55 000   |
| THIN_OVERLAY     | Thin Overlay          | BC | 8  | 5  | $80 000   |
| THICK_OVERLAY    | Thick Overlay         | BC | 10 | 6  | $120 000  |
| RECONSTRUCT_BC   | Reconstruction (BC)   | BC | 20 | 10 | $350 000  |
| SAW_SEAL_JOINTS  | Saw & Seal Joints     | RC | 5  | 3  | $15 000   |
| MINOR_CPR_DG     | Minor CPR Diamond Grind | RC | 8 | 5  | $75 000   |
| MAJOR_CPR_DG     | Major CPR Diamond Grind | RC | 10 | 6 | $120 000  |
| PRESERVATION_RC  | PM Concrete           | RC | 5  | 3  | $25 000   |
| RECONSTRUCT_RC   | Reconstruction (RC)   | RC | 25 | 10 | $400 000  |

---

## 6. Stage 4 — Deterioration families

**Script**: `db/seed_pavement_families.py` (for the pre-dTIMS version) + `db/migration_to_dtims.sql` §4 (for the current dTIMS-based schema).

Populates `pavement_families` with 18 families × up to 8 index types = 144 rows. The families are defined as `{pavement_type}_{rehab_type}_{truck_load}`:

```
BC_Initial_L, BC_Initial_H, BC_Minor_L, BC_Minor_H, BC_Major_L, BC_Major_H,
RC_Initial_L, RC_Initial_H, RC_Minor_L, RC_Minor_H, RC_Major_L, RC_Major_H,
OT_Initial_L, ..., OT_Major_H
```

- `pavement_type`: `BC` (asphalt), `RC` (concrete), `OT` (other)
- `rehab_type`: `Initial` (new), `Minor` (preserved), `Major` (overlaid)
- `truck_load`: `L` (low) or `H` (high)

The 144 `(alpha, beta, c3, curve_type)` tuples come from the dTIMS `Analysis_Lookup_Perf_Coef` table (144 rows) dumped from the live WVDOT instance. For the full numerical reference, see [dTIMS Pavement Family Coefficients](dTIMS_Pavement_Family_Coefficients.md).

---

## 7. Stage 5 — Build `analysis_segments`

This is the big one. `analysis_segments` is the fully-denormalized working table the engine reads on every run — one row per LRS segment with *everything* baked in: geometry, lanes, traffic, route metadata, the current condition indices, per-index ages, pavement family, joint ID. No joins at run time.

The definitive DDL lives in `scripts/import_pavement_data.py:811-868`:

```sql
DROP TABLE IF EXISTS analysis_segments CASCADE;
CREATE TABLE analysis_segments (
    analysis_segment_id  SERIAL PRIMARY KEY,
    route_id             VARCHAR(20),
    begin_mp             NUMERIC(10,3),
    end_mp               NUMERIC(10,3),
    length_miles         NUMERIC(10,4),
    lanes                INTEGER,
    surface_type         VARCHAR(20),
    district             VARCHAR(10),
    district_code        INTEGER,
    district_desc        VARCHAR(100),
    county_code          INTEGER,
    county_desc          VARCHAR(100),
    nhs_code             INTEGER,
    nhs_desc             VARCHAR(100),
    functional_class     INTEGER,
    functional_class_desc VARCHAR(100),
    route_status         INTEGER,
    route_status_desc    VARCHAR(100),
    current_iri          NUMERIC(10,2),
    current_rut          NUMERIC(10,4),
    current_crack        NUMERIC(10,2),
    current_faulting     NUMERIC(10,4),
    current_psi          DOUBLE PRECISION,
    current_rdi          DOUBLE PRECISION,
    current_sci          DOUBLE PRECISION,
    current_cci          DOUBLE PRECISION,
    current_eci          DOUBLE PRECISION,
    current_jci          DOUBLE PRECISION DEFAULT 5.0,
    current_csi          DOUBLE PRECISION DEFAULT 5.0,
    pavement_type        VARCHAR(4),
    age_psi              INTEGER DEFAULT 0,
    age_rdi              INTEGER DEFAULT 0,
    age_sci              INTEGER DEFAULT 0,
    age_eci              INTEGER DEFAULT 0,
    age_jci              INTEGER DEFAULT 0,
    age_csi              INTEGER DEFAULT 0,
    aadt                 INTEGER,
    lrs_aadt             INTEGER,
    aadt_combination     INTEGER,
    aadt_single          INTEGER,
    coal_route           VARCHAR(50),
    truck_pct            DOUBLE PRECISION,
    truck_load           VARCHAR(2) DEFAULT 'L',
    rehab_type           VARCHAR(10) DEFAULT 'Initial',
    family_id            VARCHAR(20),
    current_age          INTEGER DEFAULT 0,
    joint_id             VARCHAR(50)
);
CREATE INDEX idx_analysis_segments_joint    ON analysis_segments(joint_id);
CREATE INDEX idx_analysis_segments_family   ON analysis_segments(family_id);
CREATE INDEX idx_analysis_segments_district ON analysis_segments(district_code);
```

The build happens in two passes:

### Pass 1 — `create_analysis_segments.py`

1. **Export to CSV**. The script exports three queries as CSVs via `psql COPY`:
   - `lrs_table.csv` — the LRS reference table (route × milepoint grid)
   - `segments_base.csv` — segment geometry + lanes + surface type + metadata
   - `pavement_joints_lrs.csv` — joint geometry
2. **Run `lrsops rhoverlay`** — generates the enriched LRS table with traffic layers (`_run_lrsops_rhoverlay`).
3. **Run `lrsops overlay`** — combines the LRS table + vendor condition data → `segment_overlay_output.csv`.
4. **Load the overlay output** back into Postgres via psycopg2 bulk insert (`load_overlay_output`, lines 153–267).
5. **Transform the DataFrame** (`transform_dataframe`): derive `pavement_type` from `surface_type`, derive `family_id` from `pavement_type`/`rehab_type`/`truck_load`, fill missing `lanes`, etc.
6. **INSERT into `analysis_segments`** — the big fact table is populated.
7. **Post-load index + family update** (lines 415–450): build the composite `family_id`, set `pavement_type`, create the indexes above.

The whole pipeline is orchestrated by `scripts/import_pavement_data.py` (or `create_analysis_segments.py` when run standalone).

### Pass 2 — dTIMS migration (`db/migration_to_dtims.sql` §1)

At this point `analysis_segments` has raw-measurement data (`current_iri`, `current_rut`, `current_crack`) and possibly the legacy `current_cci` / `current_psi`. The dTIMS migration then:

1. **Adds the six per-index columns** (`current_psi`, `current_rdi`, `current_sci`, `current_eci`, `current_jci`, `current_csi`) if they don't exist.
2. **Adds `pavement_type` + per-index ages** (`age_psi` … `age_csi`).
3. **Derives index values from raw measurements** using the PSI/RDI/SCI formulas:
   ```sql
   UPDATE analysis_segments
      SET current_psi = LEAST(5.0, GREATEST(0.0, 5.0 * EXP(-0.0041 * current_iri)))
    WHERE current_psi IS NULL AND current_iri IS NOT NULL;
   ```
   (see `engine/condition/indices.py:33-80` for the full formulas and [Raw Measurements to Condition Indices](Raw_Measurements_to_Condition_Indices.md) for the derivation).
4. **Back-fills sentinel 5.0** for indices not applicable to the pavement type (e.g. `current_jci` on asphalt).
5. **Back-calculates per-index ages** from current index values using the family curves (`compute_equivalent_age`). If a BC segment has `current_psi = 3.2`, the migration figures out at what age on the `BC_Initial_L` PSI curve the value 3.2 appears, and sets `age_psi` accordingly.

After the migration, `analysis_segments` is ready for the engine — it has the dTIMS-style indices + ages alongside the raw measurements (which are kept for display and diagnostic purposes).

---

## 8. Stage 6 — dTIMS migration (one-time)

The dTIMS migration (`db/migration_to_dtims.sql`) is a 700-line SQL script that rewrites the legacy raw-measurement tables into dTIMS index-based tables. It runs once per environment and has the following sections:

| § | Purpose | Tables affected |
|---|---------|-----------------|
| 1 | Add index columns + ages to `analysis_segments` | `analysis_segments` |
| 2 | Redesign `treatment_triggers` around 6-index windows | `treatment_triggers`, `treatment_triggers_legacy` |
| 3 | Redesign `treatment_resets` around `ADDITIVE`/`ABSOLUTE`/`HOLD` modes | `treatment_resets`, `treatment_resets_legacy` |
| 4 | Restructure `pavement_families` to per-index curve rows | `pavement_families`, `pavement_families_legacy` |
| 5 | Create `treatment_costs_lookup` for per-pavement-type cost overrides | `treatment_costs_lookup` |
| 6 | Add `eci`, `jci`, `csi` columns to `condition_history` | `condition_history` |
| 7 | Mark pre-dTIMS treatments inactive, add `interval_years` / `treatment_order` / `color` / `pavement_type_applicable` | `treatments` |
| 8 | Seed the 14 dTIMS state-route treatments | `treatments` |

After the migration, the engine reads exclusively from the new tables. The `*_legacy` tables are kept as an audit trail but never referenced by code.

For the full story of why this migration happened and what it changed semantically, see [Migration to dTIMS Model](Migration_to_dTIMS_Model.md).

---

## 9. Stage 7 — Committed projects

**Script**: `scripts/populate_committed_flags.py` (~175 lines).

WVDOT frequently programs specific work that the optimizer must respect. If the department has already decided "we're reconstructing I-77 MP 42.1–48.7 in 2027", the engine should lock that segment to that treatment in year 2027 and leave it untouched in all earlier years.

The script takes a CSV of committed projects (route, begin MP, end MP, treatment ID, absolute year) and, optionally, a `--base-year` flag that maps absolute years to 1-indexed `program_year`s:

1. For each committed project, it finds every segment in `analysis_segments` whose geometry overlaps the project's route + MP range.
2. Sets `is_committed = TRUE`, `committed_treatment_id = <treatment_id>`, `committed_program_year = <1-indexed year>`.
3. If multiple projects overlap the same segment, the earliest year wins.

The trigger evaluator then short-circuits eligibility based on these columns (see [Analysis Engine §5b](WVDOT_PMS_Analysis_Engine.md#5b-trigger-evaluation)). Migration 008 created the columns and a partial index:

```sql
CREATE INDEX IF NOT EXISTS idx_analysis_segments_committed
    ON analysis_segments(committed_program_year)
    WHERE is_committed = TRUE;
```

Committed projects are part of the *data pipeline*, not the engine, because they're a stable property of a segment for a given planning horizon. If WVDOT re-programs a project, you re-run `populate_committed_flags.py` and the engine's next run picks up the new commitments.

---

## 10. QA / audit tables

Two tables in the pipeline are purely for human review, never read by the engine:

### `normalization_audit`

Populated during the LRS reconflate process. One row per segment × source-data record showing how much of the source overlapped the target segment. Useful for diagnosing "why did my condition data look wrong on this joint" problems — the answer is usually "the source record covered 40 % of the segment".

Columns: `segment_id`, `source_route`, `source_bmp`, `source_emp`, `overlap_length`, `overlap_pct`, `position_offset_ft`, `length_discrepancy_ft`.

### `joint_alignment_issues`

Populated during joint loading. One row per segment that has a gap, overlap, or misalignment against its assigned joint's stated extent. Severity is `low` / `medium` / `high`. Read by the Joint Alignment QA view in the UI.

Columns: `joint_id`, `segment_id`, `issue_type` (`gap` / `overlap` / `misalignment`), `severity`, `offset_distance_ft`, `description`, `resolved`.

---

## 11. Refreshing after a new vendor drop

The common case — annual condition survey arrives. What to run:

```bash
# 1. Load the raw survey into condition_history (one row per segment × year)
python db/load_condition_history.py --csv path/to/new_vendor.csv --year 2025

# 2. Rebuild reconflate_normalized + analysis_segments via lrsops
python create_analysis_segments.py

# 3. (Optional) Re-apply the dTIMS index columns if analysis_segments was dropped
psql -f db/migration_to_dtims.sql   # only §1 runs; others are idempotent no-ops

# 4. (Optional) Refresh committed projects if WVDOT re-programmed work
python scripts/populate_committed_flags.py projects.csv --base-year 2026
```

For a treatment catalog refresh (rarer):

```bash
# If only the trigger windows changed (most common)
python db/migrations/007_refresh_triggers_from_2025_12_17.py

# If the full catalog changed — use with caution, this rewrites treatments too
psql -f db/migration_to_dtims.sql   # §7-8
```

For pavement-family coefficient updates (very rare):

```bash
python db/seed_pavement_families.py   # truncate + reload from dtims_dump.sqlite
```

After any of these, the engine's next run will reflect the new data — there's no cache to invalidate, no background refresh, nothing to restart. `engine/db.py` reads live on every run.
