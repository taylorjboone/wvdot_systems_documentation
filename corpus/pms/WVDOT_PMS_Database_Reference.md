# WVDOT PMS Database Reference

> Every Postgres table in the WVDOT PMS, grouped by functional area. Column types, primary keys, foreign keys, indexes, and — most importantly — **which tables the analysis engine actually reads and writes during a run**. If you are trying to trace a value back to where it came from, this is the doc.

The database lives on `localhost:5434/pms` by default (see `.env`). The schema is bootstrapped by `db/schema.sql` and evolved forward via `db/migration_to_dtims.sql` + `db/migrations/001-008*.sql`.

---

## Table of Contents

1. [Functional groups](#1-functional-groups)
2. [Network / LRS tables](#2-network--lrs-tables)
3. [Condition tables](#3-condition-tables)
4. [Treatment catalog tables](#4-treatment-catalog-tables)
5. [Deterioration model tables](#5-deterioration-model-tables)
6. [Analysis runtime tables](#6-analysis-runtime-tables)
7. [Legacy / QA tables](#7-legacy--qa-tables)
8. [Views](#8-views)
9. [Foreign-key graph](#9-foreign-key-graph)
10. [Which tables the engine reads on every run](#10-which-tables-the-engine-reads-on-every-run)
11. [Where each table is populated](#11-where-each-table-is-populated)

---

## 1. Functional groups

| Group | Tables | Written by | Read by |
|-------|--------|------------|---------|
| Network / LRS | `routes`, `segments`, `pavement_joints`, `segment_joints` | Offline loaders (`db/load_*.py`), `create_analysis_segments.py` | Engine (indirect, via `analysis_segments`), API (segment / route / joint endpoints) |
| Condition | `condition_history`, `reconflate_normalized` | `db/load_condition_history.py`, `lrsops` overlay | `create_analysis_segments.py` to populate `analysis_segments` |
| Treatment catalog | `treatments`, `treatment_triggers`, `treatment_resets`, `treatment_costs_lookup` | `db/seed_treatments.sql`, `db/migration_to_dtims.sql`, `db/migrations/007_refresh_triggers_from_2025_12_17.py` | Engine (every run, via `engine/db.py`) |
| Deterioration models | `pavement_families`, `deterioration_models` *(legacy)* | `db/seed_pavement_families.py`, `db/migrations/002_add_deterioration_models.sql` | Engine (every run, via `engine/db.py`) |
| Analysis runtime | `analysis_segments`, `analysis_runs`, `run_logs` | `analysis_segments`: offline ingest. `analysis_runs` + `run_logs`: `api/routes/runs.py` + engine | Engine (reads `analysis_segments`), API (reads `analysis_runs` / `run_logs` for the UI) |
| Legacy / QA | `projects`, `project_segments`, `optimization_scenarios`, `optimization_results`, `work_program_projects`, `normalization_audit`, `joint_alignment_issues` | Pre-dTIMS pipeline (mostly unused) | Some still referenced by segment / QA endpoints |

> ⚠️ Some of the tables in `db/schema.sql` were written in the **pre-dTIMS** era (early 2026) and have been *superseded* by tables created in `db/migration_to_dtims.sql`. The legacy tables still exist but the engine does not read them. Where that applies, the section notes "**Legacy**" explicitly.

---

## 2. Network / LRS tables

### `routes`

Master dimension for highway routes. One row per route_id (e.g. `"I-77"`, `"US-60"`, `"WV-16"`).

| Column | Type | Notes |
|--------|------|-------|
| `route_id` | `VARCHAR(20)` **PK** | Canonical route key used everywhere else |
| `route_name` | `VARCHAR(100)` | Human-readable |
| `system_type` | `VARCHAR(20)` | `Interstate` / `US` / `WV State` / `County` |
| `functional_class` | `INTEGER` | FHWA functional class 1–7 |
| `nhs_type` | `INTEGER` | 0 = not-NHS; 1–9 = NHS subtype |
| `total_length_mi` | `DECIMAL(10,3)` | Precomputed mileage |
| `district` | `INTEGER` | WVDOT district (1–10) |
| `county` | `VARCHAR(50)` | Primary county |
| `created_at` / `updated_at` | `TIMESTAMP` | Audit |

**Indexes**: none beyond the PK.
**FKs referenced**: `segments.route_id`, `pavement_joints.route_id`, `projects.route_id`.
**Populated by**: `db/load_routes.py` (`extract_routes_from_csv`, lines 96-168).
**Read by**: `api/routes/routes.py` list/detail endpoints. The engine never reads `routes` directly — the route metadata it needs is already denormalized onto `analysis_segments`.

### `segments`

Normalized 0.1-mile LRS segments of the WV state system. This is the base geometry table — *not* the one the engine reads during a run.

| Column | Type | Notes |
|--------|------|-------|
| `segment_id` | `VARCHAR(50)` **PK** | `{route_id}-{begin_mp:07.3f}` |
| `route_id` | `VARCHAR(20)` → `routes(route_id)` | |
| `begin_mp` / `end_mp` | `DECIMAL(10,3)` | Nominal 0.1-mile grid |
| `actual_bmp` / `actual_emp` | `DECIMAL(15,10)` | LRS-reconciled milepoints from reconflate |
| `length_mi` | `DECIMAL(10,4)` | |
| `lanes` | `INTEGER` | |
| `lane_width` | `DECIMAL(5,2)` | |
| `surface_type` | `VARCHAR(10)` | `ASP` / `JCP` / `CRC` |
| `direction` | `VARCHAR(5)` | `EB` / `WB` / `NB` / `SB` / null |
| `lat_start` / `lon_start` / `lat_end` / `lon_end` | `DECIMAL(12,8)` | For map rendering |
| `county`, `district` | denormalized | |
| `family_id` | `VARCHAR(10)` → `pavement_families(family_id)` | Added by migration 002 |
| `pavement_joint_id` | `VARCHAR(50)` | Added by migration 004; logical FK to `pavement_joints` (constraint commented out) |
| `created_at` | `TIMESTAMP` | |

**Indexes**: `idx_segments_route(route_id)`, `idx_segments_surface(surface_type)`, `idx_segments_district(district)`, `idx_segments_family(family_id)`, `idx_segments_joint(pavement_joint_id)`.
**Populated by**: `db/load_segments.py`.
**Read by**: `api/routes/segments.py`. **Not** read by the engine.

### `pavement_joints`

Contiguous groups of segments that are managed and optimized as a single project. This is the unit of work the optimization actually operates on — a "project" in the engine output is a joint.

| Column | Type | Notes |
|--------|------|-------|
| `joint_id` | `VARCHAR(50)` **PK** | `{route_id}-J{source_object_id}` |
| `route_id` | `VARCHAR(20)` → `routes(route_id)` | |
| `direction` | `VARCHAR(10)` | |
| `begin_mp` / `end_mp` | `DECIMAL(8,3)` | Joint extent |
| `length_mi` | `DECIMAL(6,3)` | |
| `segment_count` | `INT` | How many 0.1-mi segments are in the joint |
| `surface_type` | `VARCHAR(20)` | |
| `functional_class` | `VARCHAR(20)` | |
| `district` | `INT` | |
| `current_iri`, `current_rut`, `current_crack`, `current_aadt` | *Denormalized — legacy*, not used by the engine | |
| `source_object_id` | `VARCHAR(50)` | Original vendor `70_OBJECTID` |
| `last_treatment_year` | `INT` | *Not* updated by the engine during a run |
| `notes` | `TEXT` | |

**Indexes**: `idx_joints_route(route_id)`, `idx_joints_district(district)`.
**Populated by**: `db/load_pavement_joints.py`.
**Read by**: `api/routes/segments.py` (for the joint QA view). The engine does **not** read this table directly during a run — it aggregates segments → joints in-memory using the `joint_id` column that's already on `analysis_segments`. The table is used as ground truth for `joint_id` assignment during ingest.

### `segment_joints`

Many-to-one mapping from segments to joints (a segment can theoretically be split across two joints but in practice is in one). **Legacy**: not used by the engine; the `joint_id` is already on `analysis_segments`.

| Column | Type |
|--------|------|
| `segment_id` | `VARCHAR(50)` |
| `joint_id` | `VARCHAR(50)` → `pavement_joints(joint_id)` |
| `overlap_pct` | `DECIMAL(5,2)` |

**PK**: `(segment_id, joint_id)`.

---

## 3. Condition tables

### `condition_history`

Yearly condition survey fact table — one row per `(segment_id, survey_year)`. Holds both raw measurements and the computed indices.

| Column | Type | Notes |
|--------|------|-------|
| `id` | `SERIAL` **PK** | |
| `segment_id` | `VARCHAR(50)` | Logical FK to `segments.segment_id` |
| `survey_year` | `INTEGER` | |
| `survey_date` | `DATE` | |
| `data_source` | `VARCHAR(50)` | vendor name / year |
| **Raw measurements** | | |
| `iri_mean`, `iri_max` | `DECIMAL(8,2)` | in/mi |
| `rut_mean`, `rut_max` | `DECIMAL(6,4)` | inches |
| `crack_percent` | `DECIMAL(6,2)` | |
| `fhwa_crack_percent` | `DECIMAL(6,2)` | |
| `faulting`, `joint_count`, `slab_count` | rigid-specific | |
| **Composite indices** | | |
| `cci`, `psi`, `rdi`, `sci` | `DECIMAL(5,2)` | 0–5 scale |
| `eci`, `jci`, `csi` | `DECIMAL` | added by `migration_to_dtims.sql` §6 |
| `pci_score` | `DECIMAL(5,2)` | 0–100 legacy PCI (migration 001) |
| `iri_deduction`, `rut_deduction`, `crack_deduction`, `faulting_deduction` | `DECIMAL(5,2)` | legacy PCI deductions (migration 001) |
| `gfp_rating` | `VARCHAR(10)` | `Good` / `Fair` / `Poor` (migration 001) |
| **Traffic** | | |
| `aadt` | `INTEGER` | |
| `truck_pct` | `DECIMAL(5,2)` | |
| **Data quality** | | |
| `coverage_pct`, `confidence_score` | `DECIMAL(5,2)` | |
| `created_at` | `TIMESTAMP` | |

**Unique**: `(segment_id, survey_year)`.
**Indexes**: `idx_condition_segment_year(segment_id, survey_year)`, `idx_condition_year(survey_year)`, `idx_condition_pci(pci_score)`, `idx_condition_gfp(gfp_rating)`.
**Populated by**: `db/load_condition_history.py` + `db/migrate_condition_indices.py`.
**Read by**: `create_analysis_segments.py` when rebuilding the `analysis_segments` working table. Not read during a run.

### `reconflate_normalized`

LRS-overlay output: weighted-average normalized condition metrics per target segment per year, produced by the external `lrsops` CLI.

| Column | Type | Notes |
|--------|------|-------|
| `id` | `SERIAL` **PK** | |
| `segment_id` | `VARCHAR(50)` | |
| `route_id` | `VARCHAR(20)` | |
| `actual_bmp`, `actual_emp` | `DECIMAL(15,10)` | |
| `survey_year` | `INTEGER` | |
| `coverage_pct` | `DECIMAL(5,4)` | |
| `iri_mean`, `rut_mean`, `faulting`, `fhwa_crack_pct` | weighted averages | |
| `surface_type`, `shoulder_type` | length-dominant | |
| `iri_grade` / `rutting_grade` / `faulting_grade` / `cracking_grade` / `overall_grade` | `VARCHAR(10)` | |
| `pci_score`, `*_deduction`, `gfp_rating` | (migration 001) | |

**Unique**: `(segment_id, survey_year)`.
**Indexes**: `idx_reconflate_segment`, `idx_reconflate_year`, `idx_reconflate_route`, `idx_reconflate_pci`, `idx_reconflate_gfp`.
**Populated by**: `lrsops overlay` → CSV → `\COPY` into this table during `create_analysis_segments.py`.
**Read by**: the `segment_condition_by_year` view, and `create_analysis_segments.py`. Not read during a run.

---

## 4. Treatment catalog tables

These are the tables the analysis engine loads at the **start of every run**. They define *what treatments exist*, *when each one can be applied*, and *what happens to the condition indices when one is applied*.

### `treatments`

One row per treatment. Post-dTIMS migration there are **14 active treatments** (9 BC + 5 RC) seeded by `db/migration_to_dtims.sql` §8.

| Column | Type | Notes |
|--------|------|-------|
| `treatment_id` | `VARCHAR(30)` **PK** | e.g. `CRACK_SEAL`, `THICK_OVERLAY`, `RECONSTRUCT_BC` |
| `treatment_name` | `VARCHAR(100)` | Display name |
| `unit_cost_per_lanemile` | `DECIMAL(12,2)` | Flat cost per lane-mile applied |
| `service_life_years` | `INTEGER` | Horizon over which the treatment's benefit persists |
| `min_interval_years` | `INTEGER` | Cooldown between applications on the same segment/joint |
| `budget_category` | `VARCHAR(30)` | `PRESERVATION` / `REHABILITATION` / `RECONSTRUCTION` |
| `alpha_post`, `beta_post` | `DECIMAL(6,3)` | Post-treatment deterioration parameters (legacy — engine uses `rehab_type` → family lookup instead) |
| `description` | `TEXT` | |
| `active` | `BOOLEAN` | Pre-dTIMS treatments were `UPDATE`-d to FALSE by the migration |
| `interval_years` | `INTEGER` | Added by dtims migration §7 — how many years between same-family treatments |
| `treatment_order` | `INTEGER` | Display sort (1–14) |
| `color` | `VARCHAR(20)` | Hex color used by the UI |
| `pavement_type_applicable` | `VARCHAR(10)` | `BC` or `RC` — enforces pavement-type compatibility at trigger time |
| `created_at` | `TIMESTAMP` | |

**Cost calculation** (`engine/optimization/work_program.py:584-589`):
```
if lane_miles available:    total_cost = unit_cost_per_lanemile × lane_miles
else:                       total_cost = unit_cost_per_lanemile × length_miles × lanes
```

**Populated by**: `db/seed_treatments.sql`, then migrated by `db/migration_to_dtims.sql` §7-8. Can be refreshed by `db/migrations/007_refresh_triggers_from_2025_12_17.py`.
**Read by**: `engine/db.py : load_treatments_df` at the start of every run.

### `treatment_triggers`

**Index-based triggers** (the table was completely redesigned by `migration_to_dtims.sql` §2; the pre-dTIMS version is preserved as `treatment_triggers_legacy` and ignored by the engine).

A trigger row says: "for this treatment, branch *B*, pavement_type *PT*, the segment qualifies if all six condition indices fall inside their respective `[lower, upper]` windows". A treatment may have multiple *branches* — a segment qualifies for the treatment if it passes **any** branch (OR logic between branches, AND logic within a branch).

| Column | Type | Notes |
|--------|------|-------|
| `trigger_id` | `SERIAL` **PK** | |
| `trigger_key` | `VARCHAR(50)` | Human-readable key, e.g. `THICK_OVERLAY_BR2` |
| `treatment_id` | `VARCHAR(50)` → `treatments(treatment_id)` | |
| `trigger_branch` | `INTEGER` | 1, 2, 3… — multiple rows per treatment, one per OR-branch |
| `pavement_type` | `VARCHAR(4)` | `BC` / `RC` / null (any) |
| `psi_lower`, `psi_upper` | `DOUBLE PRECISION` | Default `[0.0, 5.0]` |
| `rdi_lower`, `rdi_upper` | `DOUBLE PRECISION` | Default `[0.0, 5.0]` |
| `sci_lower`, `sci_upper` | `DOUBLE PRECISION` | Default `[0.0, 5.0]` |
| `csi_lower`, `csi_upper` | `DOUBLE PRECISION` | Default `[0.0, 5.0]` |
| `eci_lower`, `eci_upper` | `DOUBLE PRECISION` | Default `[0.0, 5.0]` |
| `jci_lower`, `jci_upper` | `DOUBLE PRECISION` | Default `[0.0, 5.0]` |
| `min_section_length` | `DOUBLE PRECISION` | Minimum joint length for the treatment to apply |
| `description` | `TEXT` | |

**Indexes**: `idx_dtims_triggers_treatment(treatment_id)`, `idx_dtims_triggers_key(trigger_key)`.
**How the engine evaluates it**: `engine/treatments/triggers.py : evaluate_triggers_polars` (lines 187-507) cross-joins segments × triggers and applies vectorized bounds checks. Sentinel 5.0 values mean "index not applicable to this pavement type, pass trivially" — see [Raw Measurements to Condition Indices](Raw_Measurements_to_Condition_Indices.md) for why.
**Populated by**: `db/migration_to_dtims.sql` §2 (seed), `db/migrations/007_refresh_triggers_from_2025_12_17.py` (refresh from vendor Excel).

**Legacy table** (`db/schema.sql:87-97`): the original `treatment_triggers` used `variable_name` + `operator_min` + `threshold_min` + `operator_max` + `threshold_max` + `trigger_group` + `trigger_type`. That version was renamed to `treatment_triggers_legacy` by the migration and **is not read by the current engine**.

### `treatment_resets`

What happens to each condition index when a treatment is applied. One row per `(treatment_id, variable)` — typically ~6 rows per treatment (one per index).

| Column | Type | Notes |
|--------|------|-------|
| `reset_id` | `SERIAL` **PK** | |
| `treatment_id` | `VARCHAR(50)` → `treatments(treatment_id)` | |
| `variable` | `VARCHAR(10)` | `psi`, `rdi`, `sci`, `eci`, `jci`, `csi`, `cci` |
| `reset_mode` | `VARCHAR(10)` | `ADDITIVE` / `ABSOLUTE` / `HOLD` (and legacy `PERCENTAGE` / `RELATIVE`) |
| `reset_delta` | `DOUBLE PRECISION` | The value used by the mode |
| `description` | `TEXT` | |

**Reset semantics** (`engine/treatments/resets.py`):
- `ADDITIVE` — `new = MIN(current + reset_delta, 5.0)`
- `ABSOLUTE` — `new = MAX(reset_delta, current)` (only ever improves)
- `HOLD` — `new = current` (crack seal, saw-and-seal joints: condition unchanged but age is frozen)
- `PERCENTAGE` — `new = current × reset_delta` clamped `[0, 5]` (legacy)

**Age columns are NOT reset** by this function. See the [Analysis Engine doc §5e](WVDOT_PMS_Analysis_Engine.md#5e-apply-treatment-resets) for how age and family migration (Initial → Major etc.) are handled separately.

**Index**: `idx_dtims_resets_treatment(treatment_id)`.
**Populated by**: `db/migration_to_dtims.sql` §3.
**Read by**: `engine/db.py : load_resets_df` → applied in `engine/optimization/work_program.py : _apply_treatment_resets_polars` (lines 223-372).

### `treatment_costs_lookup`

Per-pavement-type cost override. Lets a treatment have one `unit_cost_per_lanemile` for BC and another for RC.

| Column | Type |
|--------|------|
| `cost_id` | `SERIAL` **PK** |
| `treatment_id` | `VARCHAR(50)` → `treatments(treatment_id)` |
| `pavement_type` | `VARCHAR(4)` |
| `cost_per_lane_mile` | `DOUBLE PRECISION` |
| `description` | `TEXT` |

**Unique**: `(treatment_id, pavement_type)`.
**Index**: `idx_dtims_costs_treatment`, `idx_dtims_costs_unique`.
**Populated by**: `db/migration_to_dtims.sql` §5.
**Read by**: engine cost layer (optional override; when absent, fall back to `treatments.unit_cost_per_lanemile`).

---

## 5. Deterioration model tables

### `pavement_families`

The per-family, per-index deterioration curve table — redesigned by `migration_to_dtims.sql` §4 to support the 5 dTIMS curve types (linear / log / polynomial / power / sigmoid).

There are **18 families** × **up to 8 index types** = **144 coefficient rows** total. The family key is a composite of `pavement_type` × `rehab_type` × `truck_load`, e.g. `BC_Initial_L` for "asphalt, newly constructed, low-truck traffic".

| Column | Type | Notes |
|--------|------|-------|
| `family_id` | `VARCHAR(20)` | Part of PK |
| `family_name` | `VARCHAR(100)` | Human-readable |
| `surface_type` | `VARCHAR(10)` | `ASP` / `JCP` / `CRC` / `COMP` |
| `pavement_type` | `VARCHAR(4)` | `BC` / `RC` |
| `functional_class` | `VARCHAR(50)` | e.g. `Interstate`, `Primary` — classification for curve selection |
| `traffic_level` | `VARCHAR(10)` | `High` / `Low` / `All` |
| `index_type` | `VARCHAR(10)` | Part of PK — `psi`, `rdi`, `sci`, `eci`, `jci`, `csi`, `cci` |
| `alpha` | `DOUBLE PRECISION` **NOT NULL** | C1 coefficient |
| `beta` | `DOUBLE PRECISION` **NOT NULL** | C2 coefficient |
| `c3` | `DOUBLE PRECISION` **NOT NULL** default 0 | C3 coefficient (used by sigmoid / log) |
| `curve_type` | `VARCHAR(20)` | `polynomial` / `linear` / `sigmoid` / `logarithmic` / `power` |
| `initial_value` | `DOUBLE PRECISION` | Index value at age 0 (typically 5.0) |
| `description` | `TEXT` | |

**PK**: `(family_id, index_type)`.
**Read by**: `engine/db.py : load_pavement_families_df` at the start of every run, passed to `engine/deterioration/models.py : advance_conditions_one_year`.
**Populated by**: `db/seed_pavement_families.py` (from the dTIMS dump).

See [dTIMS Pavement Families](dTIMS_Pavement_Families.md) and [dTIMS Pavement Family Coefficients](dTIMS_Pavement_Family_Coefficients.md) for the full list of families and their numeric coefficients.

### `deterioration_models`

*Legacy — raw-measurement era.* Per-distress alpha/beta/initial_value for IRI / rut / crack / faulting, used before the dTIMS migration. Still exists in the schema but not read by the current engine.

| Column | Type |
|--------|------|
| `family_id` | `VARCHAR(20)` → `pavement_families(family_id)` |
| `variable_name` | `VARCHAR(30)` (`iri`, `rut`, `crack`, `faulting`) |
| `initial_value`, `alpha`, `beta` | `DECIMAL` |
| `units` | `VARCHAR(20)` |

**PK**: `(family_id, variable_name)`. **Index**: `idx_deterioration_family`.
**Populated by**: `db/migrations/002_add_deterioration_models.sql` (seeded for 7 pre-dTIMS families only).

---

## 6. Analysis runtime tables

These are the three tables that are actually read and written **on every analysis run**.

### `analysis_segments`

**The engine's primary input table.** One row per LRS segment (~260 K rows on the full WV state network), fully denormalized with every column the engine needs so it doesn't have to join on routes / segments / condition_history / joints at run time. Built by `create_analysis_segments.py` + `scripts/import_pavement_data.py` and then mutated in-place by the dTIMS migration. The definitive DDL is in `scripts/import_pavement_data.py:811-868`.

| Column | Type | Notes |
|--------|------|-------|
| `analysis_segment_id` | `SERIAL` **PK** | |
| `route_id` | `VARCHAR(20)` | Denormalized from `routes` |
| `begin_mp`, `end_mp` | `NUMERIC(10,3)` | |
| `length_miles` | `NUMERIC(10,4)` | |
| `lanes` | `INTEGER` | Default 2 if vendor missing |
| `surface_type` | `VARCHAR(20)` | `ASP` / `JCP` / `CRC` |
| `district` | `VARCHAR(10)` | |
| `district_code`, `district_desc` | | |
| `county_code`, `county_desc` | | |
| `nhs_code`, `nhs_desc` | | |
| `functional_class`, `functional_class_desc` | | |
| `route_status`, `route_status_desc` | | |
| **Raw measurements (last survey year)** | | |
| `current_iri` | `NUMERIC(10,2)` | in/mi |
| `current_rut` | `NUMERIC(10,4)` | inches |
| `current_crack` | `NUMERIC(10,2)` | % |
| `current_faulting` | `NUMERIC(10,4)` | inches |
| **Condition indices (0–5 scale, sentinel 5.0 if N/A)** | | |
| `current_psi` | `DOUBLE PRECISION` | from IRI |
| `current_rdi` | `DOUBLE PRECISION` | from rut |
| `current_sci` | `DOUBLE PRECISION` | from crack |
| `current_eci` | `DOUBLE PRECISION` | asphalt edge |
| `current_jci` | `DOUBLE PRECISION` | concrete joint, default 5.0 |
| `current_csi` | `DOUBLE PRECISION` | concrete cracking, default 5.0 |
| `current_cci` | `DOUBLE PRECISION` | composite = `MIN(...)` — see engine docs |
| `pavement_type` | `VARCHAR(4)` | `BC` / `RC` — derived from `surface_type` |
| **Per-index age (years since this index was "new")** | | |
| `age_psi`, `age_rdi`, `age_sci`, `age_eci`, `age_jci`, `age_csi` | `INTEGER` default 0 | Initially back-calculated from index value via `compute_equivalent_age()` |
| `current_age` | `INTEGER` default 0 | Global age counter (legacy) |
| **Traffic** | | |
| `aadt` | `INTEGER` | |
| `lrs_aadt` | `INTEGER` | |
| `aadt_combination`, `aadt_single` | `INTEGER` | |
| `truck_pct` | `DOUBLE PRECISION` | |
| `truck_load` | `VARCHAR(2)` default `'L'` | `L` (low) / `H` (high) — drives family selection |
| **Pavement family** | | |
| `rehab_type` | `VARCHAR(10)` default `'Initial'` | `Initial` / `Minor` / `Major` |
| `family_id` | `VARCHAR(20)` | Composite `{pavement_type}_{rehab_type}_{truck_load}` — FK to `pavement_families(family_id)` |
| **Joint grouping** | | |
| `joint_id` | `VARCHAR(50)` | References `pavement_joints.joint_id` (logical FK, no constraint) |
| `coal_route` | `VARCHAR(50)` | Is this part of the coal network? |
| **Committed project columns** — added by migration 008 | | |
| `is_committed` | `BOOLEAN NOT NULL DEFAULT FALSE` | True if this segment has a pre-programmed treatment |
| `committed_treatment_id` | `VARCHAR(50)` → `treatments(treatment_id)` | Which treatment is locked in |
| `committed_program_year` | `INTEGER` | 1-indexed program year it must be applied |

**Indexes**: `idx_analysis_segments_joint(joint_id)`, `idx_analysis_segments_family(family_id)`, `idx_analysis_segments_district(district_code)`, partial index `idx_analysis_segments_committed(committed_program_year) WHERE is_committed = TRUE`.
**Populated by**: `create_analysis_segments.py` + `scripts/import_pavement_data.py` + dtims migration. Refreshed on each ingest cycle.
**Read by**: every analysis run (`engine/db.py : load_analysis_segments_df`, lines 521-604). This is the single heaviest read in the system.

### `analysis_runs`

One row per analysis run kicked off through the API. Created `pending`, flipped to `running` by the worker thread, then to `completed` or `failed`.

| Column | Type | Notes |
|--------|------|-------|
| `run_id` | `SERIAL` **PK** | |
| `run_name` | `VARCHAR(200)` | Optional display name |
| `status` | `VARCHAR(20)` default `pending` | `pending` / `running` / `completed` / `failed` |
| `created_at` | `TIMESTAMP` default NOW | |
| `started_at` | `TIMESTAMP` | Set when thread claims the advisory lock |
| `completed_at` | `TIMESTAMP` | Set when the run finishes (success or failure) |
| `configuration` | `JSONB` | Full `PipelineConfig` as JSON — budget, years, power exponent, minimum BC, carryover, `lookahead_years` (rolling-horizon window, default 3), segment filter |
| `progress_step` | `VARCHAR(200)` | Human-readable current step, e.g. `"Processing year 5 of 10"` |
| `progress_pct` | `INTEGER NOT NULL` default 0 | Updated in-place by `ProgressTracker` |
| `result_summary` | `JSONB` | The full summary blob — see the [Analysis Engine doc](WVDOT_PMS_Analysis_Engine.md) |
| `error_message` | `TEXT` | Populated on `failed` |

**Indexes**: `idx_analysis_runs_status(status)`, `idx_analysis_runs_created(created_at DESC)`.
**Populated by**: `api/routes/runs.py` (`create_run` + `_execute_run` thread).
**Read by**: the UI via `/api/runs` (list), `/api/runs/{id}/progress`, `/api/runs/{id}/configuration`, `/api/runs/{id}/projects`, `/api/runs/{id}/export.xlsx`.

#### The `configuration` blob

The keys `api/routes/runs.py : create_run` writes when assembling the row:

```json
{
  "annual_budget": <float>,
  "analysis_years": <int>,
  "power_exponent": <float>,
  "minimum_bc_ratio": <float>,
  "allow_budget_carryover": <bool>,
  "lookahead_years": <int>,
  "segment_filter": <string | null>
}
```

- `lookahead_years` is the rolling-horizon (MPC) window size. `1` means legacy greedy single-year behavior (bit-identical to the pre-rolling-horizon engine). `>1` plans over a k-year window each outer year and commits only year 1. Default `3`, clamped `[1, 10]`. See [Optimization Logic §12](WVDOT_PMS_Optimization_Logic.md#12-rolling-horizon-look-ahead).
- `segment_filter` is an optional SQL WHERE fragment applied to `analysis_segments` at load time.

#### The `result_summary` blob

Since every downstream view reads from this JSONB column, its shape is part of the public contract between the engine and the UI:

```json
{
  "segment_count": <int>,
  "treatment_count": <int>,
  "total_cost": <float>,
  "total_benefit": <float>,
  "segments_treated": <int>,
  "budget_utilization_pct": <float>,
  "initial_pct_good": <float>,
  "final_pct_good": <float>,
  "pct_good_change": <float>,
  "duration_seconds": <float>,
  "work_program_summary": {
    "analysis_years": <int>,
    "total_budget": <float>,
    "total_cost": <float>,
    "total_benefit": <float>,
    "segments_treated_total": <int>,
    "projects_total": <int>,
    "yearly_summary": [{"year": <int>, "budget": <float>, "cost": <float>, ...}],
    "treatment_mix": {"TREATMENT_ID": {"count": <int>, "total_cost": <float>}, ...},
    "project_summary": [{"joint_id": ..., "route_id": ..., "treatment_id": ..., "program_year": ..., ...}],
    "distribution_by_year": {"years": [...], "treatments": [...], "count": [[...]], "cost": [[...]], "miles": [[...]]}
  }
}
```

Built by `engine/reporting.py : summarize_work_program` (and `_build_distribution_pivots` for the year × treatment heatmaps used by the Treatments tab).

### `run_logs`

Streaming log capture for the Run Detail page's log tail. One row per log record, batched into Postgres by `DatabaseLogHandler`.

| Column | Type |
|--------|------|
| `id` | `SERIAL` **PK** |
| `run_id` | `INTEGER NOT NULL` → `analysis_runs(run_id) ON DELETE CASCADE` |
| `timestamp` | `TIMESTAMP NOT NULL` default NOW |
| `level` | `VARCHAR(10) NOT NULL` (`INFO` / `WARNING` / `ERROR` / `DEBUG`) |
| `message` | `TEXT NOT NULL` |

**Index**: `idx_run_logs_run_id(run_id, timestamp)` — supports the tailable `GET /api/runs/{id}/logs` endpoint.
**Populated by**: `engine/log_capture.py : DatabaseLogHandler` attached to the `engine` and `api` loggers at run start, flushing every 25 records.
**Read by**: `api/routes/runs.py : get_run_logs` (paginated), hit by the UI's live log tail while the run is running.

---

## 7. Legacy / QA tables

These tables exist in the schema but are either unused or only touched by read-only QA endpoints. Kept here for completeness.

### `projects` *(legacy)*
Pre-dTIMS "real projects" (letting). One row per programmed work item. Superseded by the work program generated per run and stored in `analysis_runs.result_summary`. Still referenced by `api/routes/projects.py`.

Columns: `project_id`, `project_name`, `route_id`, `begin_mp`, `end_mp`, `length_mi`, `treatment_id`, `estimated_cost`, `actual_cost`, `funding_source`, `program_year`, `design_year`, `construction_year`, `completion_date`, `status`, `priority_rank`, `benefit_score`, `bc_ratio`. Indexes: `idx_projects_route`, `idx_projects_status`, `idx_projects_year`.

### `project_segments` *(legacy)*
`(project_id, segment_id)` with `segment_cost` + `segment_benefit`. PK: `(project_id, segment_id)`. Same era as `projects`.

### `optimization_scenarios` + `optimization_results` *(legacy)*
Pre-dTIMS persistent optimization results. `optimization_scenarios` holds the run config + top-level results (one row per "scenario"), `optimization_results` holds the per-segment output (selected or not). The current engine writes its results into `analysis_runs.result_summary` as JSONB instead, so these tables are not written during live runs. Some older views (`work_program_summary`, `treatment_mix_summary`) still reference them.

Columns, indexes, and views are defined in `db/schema.sql:224-270` and evolved by `db/migrations/003_add_program_year.sql`.

### `work_program_projects` *(legacy)*
`db/migrations/004_pavement_joints.sql:54-90` defined this as the "primary output" table for work program projects. The current engine does **not** write to it — it writes the work program to `analysis_runs.result_summary` instead. The `work_program_projects_view` + `work_program_yearly_summary` views built on top of it are consequently empty on modern runs.

### `normalization_audit`
Audit trail of LRS normalization events — segments with weird offsets or length discrepancies from the reconflate process. Populated offline by the ingest pipeline; not read by the engine.

### `joint_alignment_issues`
QA records of gaps / overlaps / misalignments detected when merging segments into joints. Populated offline; read by the frontend's Joint Alignment QA view.

---

## 8. Views

All in `db/schema.sql` unless noted.

### `segment_condition_by_year` — `schema.sql:366-445`
Flat 2020–2024 pivot of each segment's raw condition metrics per year, plus `iri_change` and `years_with_data`. Used by the "Segment condition by year" UI.

### `work_program_summary` — `db/migrations/003_add_program_year.sql:62-77` *(legacy)*
Aggregates `optimization_results` by `scenario_id` + `program_year`. Empty on modern runs.

### `treatment_mix_summary` — `db/migrations/003_add_program_year.sql:84-99` *(legacy)*
Aggregates `optimization_results` by `scenario_id` + `treatment_id` + `program_year`. Empty on modern runs.

### `work_program_projects_view` — `db/migrations/004_pavement_joints.sql:97-123` *(legacy)*
Joins `work_program_projects` + `optimization_scenarios` + `treatments`. Empty on modern runs.

### `work_program_yearly_summary` — `db/migrations/004_pavement_joints.sql:129-143` *(legacy)*
Aggregates `work_program_projects` by `scenario_id` + `program_year`. Empty on modern runs.

---

## 9. Foreign-key graph

```
routes (PK: route_id)
   ▲
   │
   ├── segments.route_id
   ├── pavement_joints.route_id
   └── projects.route_id

pavement_families (PK: family_id, index_type)
   ▲
   ├── segments.family_id        (added by migration 002, the constraint type is VARCHAR(10) vs VARCHAR(20))
   └── deterioration_models.family_id  (legacy)

treatments (PK: treatment_id)
   ▲
   ├── treatment_triggers.treatment_id
   ├── treatment_resets.treatment_id
   ├── treatment_costs_lookup.treatment_id
   ├── projects.treatment_id
   ├── optimization_results.treatment_id
   ├── analysis_segments.committed_treatment_id  (via analysis_segments_committed_treatment_fkey)
   └── (legacy) treatment_triggers_legacy, treatment_resets_legacy

pavement_joints (PK: joint_id)
   ▲
   └── segment_joints.joint_id        (legacy)

optimization_scenarios (PK: scenario_id)
   ▲
   ├── optimization_results.scenario_id   (legacy)
   └── work_program_projects.scenario_id  (legacy)

analysis_runs (PK: run_id)
   ▲
   └── run_logs.run_id  (ON DELETE CASCADE)

projects (PK: project_id)
   ▲
   └── project_segments.project_id  (legacy)
```

**Logical (no constraint) FKs** — referenced by the loaders/engine but not enforced by Postgres:

- `segments.pavement_joint_id → pavement_joints.joint_id` (migration 004 left the constraint commented out)
- `analysis_segments.joint_id → pavement_joints.joint_id`
- `analysis_segments.family_id → pavement_families.family_id`
- `condition_history.segment_id → segments.segment_id`
- `reconflate_normalized.segment_id → segments.segment_id`
- `run_logs` — the only strict `ON DELETE CASCADE` relationship in the system

---

## 10. Which tables the engine reads on every run

If you're debugging a run and need to know "what is the engine actually looking at right now", the answer is exactly these tables, via `engine/db.py`:

| Function | Table | What it loads |
|----------|-------|---------------|
| `load_analysis_segments_df(engine, segment_filter=None)` | `analysis_segments` | The full ~260 K segment working table, optionally filtered by a SQL WHERE fragment supplied in the run config |
| `load_treatments_df(engine)` | `treatments` | All `active=TRUE` treatments with cost, interval, pavement_type_applicable |
| `load_triggers_df(engine)` | `treatment_triggers` | All trigger branches (index windows + pavement type) |
| `load_resets_df(engine)` | `treatment_resets` | All reset rows (mode + delta per treatment × variable) |
| `load_treatment_costs_df(engine)` | `treatment_costs_lookup` | Per-pavement-type cost overrides (optional) |
| `load_pavement_families_df(engine)` | `pavement_families` | All 18 families × 6 indices of deterioration curves |

Everything else the engine needs is already denormalized onto `analysis_segments` during the ingest pipeline.

---

## 11. Where each table is populated

| Table | Populated by | When |
|-------|--------------|------|
| `routes` | `db/load_routes.py` | Ingest (once per vendor release) |
| `segments` | `db/load_segments.py` | Ingest |
| `pavement_joints` | `db/load_pavement_joints.py` | Ingest |
| `segment_joints` | `db/load_pavement_joints.py` *(legacy)* | Ingest |
| `condition_history` | `db/load_condition_history.py` | Ingest |
| `reconflate_normalized` | `create_analysis_segments.py` (via `lrsops`) | Ingest |
| `treatments` | `db/seed_treatments.sql` → `db/migration_to_dtims.sql` §7-8 | Once; refreshable |
| `treatment_triggers` | `db/migration_to_dtims.sql` §2, `db/migrations/007_refresh_triggers_from_2025_12_17.py` | Once; refreshable from vendor Excel |
| `treatment_resets` | `db/migration_to_dtims.sql` §3 | Once |
| `treatment_costs_lookup` | `db/migration_to_dtims.sql` §5 | Once |
| `pavement_families` | `db/seed_pavement_families.py`, `db/migration_to_dtims.sql` §4 | Once |
| `deterioration_models` *(legacy)* | `db/migrations/002_add_deterioration_models.sql` | Once |
| `analysis_segments` | `create_analysis_segments.py` + `scripts/import_pavement_data.py` + `db/migration_to_dtims.sql` §1 | Ingest; refreshed when condition data changes |
| `analysis_runs` | `api/routes/runs.py : create_run` (insert), `_execute_run` thread (update) | Every run |
| `run_logs` | `engine/log_capture.py : DatabaseLogHandler` | Every run, batched inserts |
| `projects` / `project_segments` *(legacy)* | Pre-dTIMS ETL | — |
| `optimization_scenarios` / `optimization_results` *(legacy)* | Pre-dTIMS runner | — |
| `work_program_projects` *(legacy)* | Pre-dTIMS runner | — |
| `normalization_audit` / `joint_alignment_issues` | Ingest QA scripts | Ingest |
