# Analysis Segments Field Reference

Comprehensive reference for every field in the `analysis_segments` table and how it flows through the optimization engine.

---

## Route & Location

| Field | Type | Used By | Purpose |
|-------|------|---------|---------|
| `analysis_segment_id` | SERIAL PK | db.py, chunked.py, ibc.py, triggers.py, auc.py | Primary key; segment identifier used throughout the pipeline for joins, grouping, and output tracking |
| `route_id` | VARCHAR(20) | db.py, chunked.py, constraints.py, work_program.py | Route identification; grouping segments in work programs; route priority filtering in constraints |
| `begin_mp` | NUMERIC(10,3) | db.py, chunked.py, work_program.py | Beginning milepost; defines segment start; synthetic joint creation; project boundary reporting |
| `end_mp` | NUMERIC(10,3) | db.py, chunked.py, work_program.py | Ending milepost; defines segment end; project boundary calculation |
| `length_miles` | NUMERIC(10,4) | db.py, chunked.py, work_program.py, ibc.py, weighting.py | Segment length in miles; cost calculation (`unit_cost * length * lanes`), traffic-weighted benefit, project aggregation |

---

## Physical Attributes

| Field | Type | Used By | Purpose |
|-------|------|---------|---------|
| `lanes` | INTEGER | db.py, chunked.py, work_program.py, runner.py | Number of travel lanes; multiplied into treatment cost (`cost * lanes`); project summarization |
| `surface_type` | VARCHAR(20) | db.py, indices.py, deductions.py, models.py, auc.py | Surface type (ASP, JCP, CRC, GRV, etc.); determines pavement type inference (RC vs BC vs OT) when `pavement_type` is missing |

---

## Network Classification

| Field | Type | Used By | Purpose |
|-------|------|---------|---------|
| `pavement_type` | VARCHAR(4) | db.py, triggers.py, indices.py, models.py, constraints.py, work_program.py | Pavement type (BC=asphalt, RC=concrete, OT=other); determines which condition indices apply (PSI/RDI/SCI for BC, PSI/CSI/JCI for RC); gates trigger branch evaluation; lookup key for family deterioration curves |
| `district` | VARCHAR(10) | db.py, work_program.py, exports.py | District name/code; project reporting and export |
| `district_code` | INTEGER | db.py, constraints.py, chunked.py | District numeric code; constraint enforcement (district budget ceiling/floor/balancing) |
| `district_desc` | VARCHAR(100) | db.py | District description; display/reporting only |
| `county_code` | INTEGER | db.py, runner.py | County numeric code; metadata |
| `county_desc` | VARCHAR(100) | db.py, exports.py | County description; display/reporting |
| `nhs_code` | INTEGER | db.py, constraints.py | NHS designation (0=non-NHS, >0=NHS); gates NHS multiplier boost in constraint benefit adjustments |
| `nhs_desc` | VARCHAR(100) | db.py | NHS description; display only |
| `functional_class` | INTEGER | db.py, constraints.py, runner.py | Functional class code (1-7); route priority benefit multiplier in constraints |
| `functional_class_desc` | VARCHAR(100) | db.py | Functional class description; display only |
| `route_status` | INTEGER | db.py | Route status code; metadata only |
| `route_status_desc` | VARCHAR(100) | db.py | Route status description; display only |

---

## Condition Measurements (Raw)

These are the raw field measurements. They are kept in sync with their corresponding indices via post-reset and post-deterioration synchronization.

| Field | Type | Used By | Purpose |
|-------|------|---------|---------|
| `current_iri` | NUMERIC | db.py, indices.py, deductions.py, work_program.py, runner.py | International Roughness Index (in/mi); raw input to PSI calculation |
| `current_rut` | NUMERIC | db.py, indices.py, deductions.py, work_program.py, runner.py | Rut depth (inches); raw input to RDI calculation |
| `current_crack` | NUMERIC | db.py, deductions.py, work_program.py, runner.py | Cracking percent (0-100); raw input to SCI calculation |
| `current_faulting` | NUMERIC | db.py, chunked.py | Faulting (inches); optionally used to compute JCI for concrete pavement |

---

## Condition Indices (dTIMS 0-5 Scale)

All indices use a 0-5 scale where 5 = best condition. Indices not applicable to a pavement type default to 5.0 (sentinel "don't care" value).

| Field | Type | Used By | Purpose |
|-------|------|---------|---------|
| `current_psi` | DOUBLE PRECISION | db.py, chunked.py, triggers.py, indices.py, auc.py, models.py | Present Serviceability Index; derived from IRI; input to CCI; used in trigger evaluation for all pavement types |
| `current_rdi` | DOUBLE PRECISION | db.py, chunked.py, triggers.py, indices.py, auc.py, models.py | Rut Depth Index; derived from rut depth; input to CCI for asphalt; defaults to 5.0 for concrete |
| `current_sci` | DOUBLE PRECISION | db.py, chunked.py, triggers.py, indices.py, auc.py, models.py | Structural Cracking Index; derived from cracking %; input to CCI for asphalt; defaults to 5.0 for concrete |
| `current_eci` | DOUBLE PRECISION | db.py, chunked.py, triggers.py, indices.py, auc.py, models.py | Edge Condition Index; asphalt-only from survey; defaults to 5.0 for concrete |
| `current_jci` | DOUBLE PRECISION | db.py, chunked.py, triggers.py, indices.py, auc.py, models.py | Joint Condition Index; concrete-only from survey; input to CCI for concrete; defaults to 5.0 for asphalt |
| `current_csi` | DOUBLE PRECISION | db.py, chunked.py, triggers.py, indices.py, auc.py | Cracking Severity Index; concrete-only from survey; input to CCI for concrete; defaults to 5.0 for asphalt |
| `current_cci` | DOUBLE PRECISION | db.py | Composite Condition Index; MIN of applicable indices; computed by `indices.py:calculate_cci()` |

---

## Age Since Treatment (Per-Index)

Each condition index has its own age column, allowing index-specific treatment resets to zero only the affected index age.

| Field | Type | Used By | Purpose |
|-------|------|---------|---------|
| `age_psi` | INTEGER DEFAULT 0 | db.py, chunked.py, auc.py | Years since last treatment affecting PSI; input to deterioration curve projection |
| `age_rdi` | INTEGER DEFAULT 0 | db.py, chunked.py, auc.py | Years since last treatment affecting RDI |
| `age_sci` | INTEGER DEFAULT 0 | db.py, chunked.py, auc.py | Years since last treatment affecting SCI |
| `age_eci` | INTEGER DEFAULT 0 | db.py, chunked.py, auc.py | Years since last treatment affecting ECI |
| `age_jci` | INTEGER DEFAULT 0 | db.py, chunked.py, auc.py | Years since last treatment affecting JCI |
| `age_csi` | INTEGER DEFAULT 0 | db.py, chunked.py, auc.py | Years since last treatment affecting CSI |

---

## Traffic & Usage

| Field | Type | Used By | Purpose |
|-------|------|---------|---------|
| `aadt` | INTEGER | db.py, chunked.py, work_program.py, weighting.py, runner.py | Annual Average Daily Traffic (from LRS layer 2); critical input to traffic-weighted benefit (`AADT^0.25` dampening factor); aggregated to joint level in project summaries |
| `aadt_combination` | INTEGER | db.py | AADT combination vehicle count; used to derive `truck_pct` |
| `aadt_single` | INTEGER | db.py | AADT single unit vehicle count; metadata only |
| `truck_pct` | DOUBLE PRECISION | db.py | Truck percentage; used to determine `truck_load` classification (>=10% = H, <10% = L) |
| `truck_load` | VARCHAR(2) DEFAULT 'L' | db.py, work_program.py, runner.py | Truck load classification (L=low, H=high); part of composite `family_id` key |

---

## Deterioration Model & Treatment Family

| Field | Type | Used By | Purpose |
|-------|------|---------|---------|
| `family_id` | VARCHAR(20) | db.py, chunked.py, auc.py, families.py, runner.py | Composite family ID (e.g. `BC_Initial_H`); lookup key into `pavement_families` table for deterioration curves per index; drives deterioration projection and benefit calculation |
| `current_age` | INTEGER | db.py, auc.py, runner.py | Overall age in years since last treatment; used for initial condition projection; overridden by per-index `age_*` values when available |
| `rehab_type` | VARCHAR(10) DEFAULT 'Initial' | db.py, work_program.py, runner.py | Rehabilitation type (Initial, Minor, Major); part of composite `family_id` key |

---

## Project Structure

| Field | Type | Used By | Purpose |
|-------|------|---------|---------|
| `joint_id` | VARCHAR(50) | db.py, chunked.py, ibc.py, work_program.py, runner.py | Pavement joint ID; fundamental project-level grouping key. Segments with the same `joint_id` are aggregated into one project for optimization. The optimizer selects entire joints, not individual segments. Either sourced from the database or synthetically generated by route + milepost bucketing. |

---

## Commitment State (Pre-Planned Treatments)

Populated by `scripts/populate_committed_flags.py` from the `projects` table. Only projects with status in (`planned`, `designed`, `awarded`, `in_progress`) are treated as commitments.

| Field | Type | Used By | Purpose |
|-------|------|---------|---------|
| `is_committed` | BOOLEAN DEFAULT FALSE | db.py, chunked.py, triggers.py | Commitment flag; when TRUE, the segment's treatment is locked to `committed_treatment_id` in `committed_program_year` |
| `committed_treatment_id` | VARCHAR(50) | db.py, chunked.py, triggers.py | The exact treatment to apply when `is_committed = TRUE` and `current_year == committed_program_year` |
| `committed_program_year` | INTEGER | db.py, chunked.py, triggers.py | Program year of commitment. Segments lock from year 1 until this year, then revert to normal trigger evaluation |

### Commitment Behavior by Year

| Year vs. Commitment | Behavior |
|---|---|
| `current_year < committed_program_year` | Segment **locked** — no treatment eligible; trigger evaluation returns zero rows |
| `current_year == committed_program_year` | **Forced** to `committed_treatment_id` (exactly one row emitted, branch=0) |
| `current_year > committed_program_year` | Falls back to normal condition-based trigger evaluation |

---

## Pipeline Flow

```
analysis_segments (DB)
    |
    v
engine/db.py                    Load all columns into Polars DataFrame
    |
    v
engine/condition/indices.py     Compute CCI from individual indices
engine/condition/deductions.py  Raw measurement -> index conversions
    |
    v
engine/treatments/triggers.py  Evaluate trigger windows per pavement type
                                Enforce commitment guards
    |
    v
engine/optimization/chunked.py Aggregate segments -> joints by joint_id
                                Length-weighted index averages
                                Propagate commitment flags
    |
    v
engine/deterioration/models.py Project future condition via family curves
    |
    v
engine/benefits/auc.py         Compute area-under-curve benefit per treatment
engine/benefits/weighting.py   Apply AADT^0.25 * length traffic weighting
    |
    v
engine/optimization/ibc.py     Incremental benefit-cost greedy selection
    |
    v
engine/optimization/           District balancing, NHS multiplier,
  constraints.py               functional class priority, treatment caps
    |
    v
engine/optimization/           Aggregate selected segments into projects
  work_program.py              Compute project-level metrics
    |
    v
engine/reporting.py            Dashboard summaries
engine/exports.py              CSV/Excel export
```

---

## Key Design Notes

1. **Composite Family Key:** `family_id = PavementType_RehabType_TruckLoad` (e.g. `BC_Initial_H`). This is the lookup into deterioration curve families for all six indices.

2. **Sentinel 5.0 Values:** Concrete-only indices (JCI, CSI) default to 5.0 on asphalt; asphalt-only indices (RDI, SCI, ECI) default to 5.0 on concrete. Trigger windows `[0, 5]` act as "don't care" wildcards.

3. **Joint = Project:** `joint_id` is the fundamental project unit. The optimizer selects entire joints, not individual segments. Segments within a joint are aggregated before IBC runs.

4. **Per-Index Ages:** Each index has its own age column. Treatment resets only zero the ages of affected indices, leaving others to continue aging on their own curves.

5. **Raw Measurement Sync:** IRI, rut, crack, and faulting are kept in sync with their corresponding indices (PSI, RDI, SCI) after resets and deterioration steps.
