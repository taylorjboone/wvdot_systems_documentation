# WVDOT PMS Analysis Engine

> End-to-end walkthrough of what happens inside one analysis run, phase by phase. Every section cites the concrete `file:line` so you can put a breakpoint wherever the narrative leaves a hole.

The engine is pure Python + Polars. It can run standalone from the CLI (`example_full_workflow.py`, `run_wv_optimization.py`) or, more commonly, be driven by the FastAPI layer which spawns a daemon thread, pipes logs and progress to Postgres, and reports back to the UI. Both entry points call the same orchestrator.

---

## Table of Contents

1. [Entry points](#1-entry-points)
2. [The top-level orchestrator](#2-the-top-level-orchestrator)
3. [Phase 1 — Validate + load](#3-phase-1--validate--load)
4. [Phase 2 — Joint aggregation](#4-phase-2--joint-aggregation)
5. [Phase 3 — Year-by-year rolling loop](#5-phase-3--year-by-year-rolling-loop)
   - [3a. Build treatment strategies](#5a-build-treatment-strategies)
   - [3b. Trigger evaluation](#5b-trigger-evaluation)
   - [3c. Benefit + cost + weighting](#5c-benefit--cost--weighting)
   - [3d. IBC selection](#5d-ibc-selection)
   - [3e. Apply treatment resets](#5e-apply-treatment-resets)
   - [3f. Advance deterioration](#5f-advance-deterioration)
   - [3g. Network GFP](#5g-network-gfp)
6. [Phase 4 — Build `result_summary`](#6-phase-4--build-result_summary)
7. [Phase 5 — Write results + XLSX export](#7-phase-5--write-results--xlsx-export)
8. [Data structures in flight](#8-data-structures-in-flight)
9. [Live progress + log capture](#9-live-progress--log-capture)
10. [Single-run advisory lock](#10-single-run-advisory-lock)

---

## 1. Entry points

### Via the API

```
POST /api/runs                       ──▶ create_run               api/routes/runs.py:684+
  ├─ INSERT analysis_runs row        (status=pending, configuration=<config JSONB>)
  └─ spawn daemon thread               _execute_run               api/routes/runs.py:352+
```

`create_run` is fire-and-forget: it writes the row, starts the thread, and returns `{ run_id }` immediately. The UI then polls `/api/runs/{run_id}/progress` to follow along.

### Via the CLI

```python
from engine.runner import run_analysis
result = run_analysis(
    annual_budget=100_000_000,
    analysis_years=10,
    power_exponent=0.25,
    minimum_bc_ratio=0.5,
    allow_budget_carryover=True,
    segment_filter=None,
)
```

`run_analysis` is a thin wrapper over `generate_work_program_chunked`. CLI runs skip the `analysis_runs` row and the `DatabaseLogHandler` — the output is a Python object you can pickle or serialize yourself.

---

## 2. The top-level orchestrator

`engine/optimization/chunked.py : generate_work_program_chunked()` (line 1063) is the function every entry point ultimately calls. Its job:

1. Validate and normalize the input Polars frames.
2. Aggregate segments → joints.
3. Run the year-by-year rolling loop.
4. Return a `WorkProgramResult` object holding the joint-level work program plus per-year summaries.

Signature (simplified):

```python
generate_work_program_chunked(
    analysis_df:     pl.DataFrame,        # ~260 K segments
    treatments_df:   pl.DataFrame,        # ~14 rows
    triggers_df:     pl.DataFrame,
    resets_df:       pl.DataFrame,
    family_params_df: pl.DataFrame,       # 18 families × 6 indices
    *,
    annual_budget:   float,
    analysis_years:  int,
    power_exponent:  float = 0.25,
    minimum_bc_ratio: float = 0.0,
    allow_budget_carryover: bool = False,
    segment_filter:  str | None = None,
    progress_tracker: ProgressTracker | None = None,
) -> WorkProgramResult
```

The rest of this doc walks through what that function does, top to bottom.

---

## 3. Phase 1 — Validate + load

**Progress: 1–10 %**

The very first thing a run does is pull data from Postgres into Polars and normalize it.

| Step | Function | What it does |
|------|----------|--------------|
| Load segments | `engine/db.py : load_analysis_segments_df()` | `SELECT` from `analysis_segments`, optionally with the user's `segment_filter` SQL fragment |
| Load treatments | `engine/db.py : load_treatments_df()` | Active treatments + cost + interval + pavement_type_applicable |
| Load triggers | `engine/db.py : load_triggers_df()` | All index-window trigger branches |
| Load resets | `engine/db.py : load_resets_df()` | One row per `(treatment, variable)` with mode + delta |
| Load families | `engine/db.py : load_pavement_families_df()` | 18 families × 6 indices of curve coefficients |
| Validate segments | `engine/runner.py : validate_analysis_df()` (line 147) | Add missing columns, backfill defaults, rename legacy columns |
| Derive CCI | `engine/condition/indices.py : calculate_condition_indices_polars()` | If any index is missing, derive it from the raw measurement using the PSI/RDI/SCI formulas below |
| Validate treatments | `engine/runner.py : validate_treatments_df()` (line 204) | Sync `unit_cost_per_lanemile` / `cost`, fill missing `min_interval_years` with 0 |

> `ProgressTracker.update("Validating inputs", 5)` fires at the start of this phase (`runner.py:317`), and `"Calculating condition indices"` at `pct=8` (`runner.py:346`).

### How condition indices are derived (if missing)

If `analysis_segments.current_psi` is null but `current_iri` has a value, the engine computes:

| Index | Formula | File:line |
|-------|---------|-----------|
| PSI | `5 × exp(−0.0041 × IRI)` clamped `[0, 5]` | `engine/condition/indices.py:33-55` |
| RDI | `MAX(MIN(5 − 6.65 × rut^1.41, 5), 0)` | `engine/condition/indices.py:58-80` |
| SCI | `MAX(0, MIN(5, 5 − 0.05 × crack_pct))` | `engine/condition/indices.py:177-195` |
| ECI | `MIN(5, SCI + 0.3)` for BC, else `5.0` (sentinel) | `engine/condition/indices.py:198-222` |
| JCI | from joint survey (RC only), sentinel `5.0` for BC | `engine/condition/indices.py:409-417` |
| CSI | from crack survey (RC only), sentinel `5.0` for BC | `engine/condition/indices.py:409-417` |
| CCI | BC: `MIN(PSI, RDI, SCI)` · RC: `MIN(PSI, CSI, JCI)` | `engine/condition/indices.py:83-123` (scalar) / `:225-272` (Polars) |

Index values are always `[0, 5]` with 5 = best. A value of exactly `5.0` for an index that doesn't apply to a pavement type (e.g. JCI on asphalt) acts as a sentinel and passes every trigger bound trivially — that's why dTIMS trigger rows default lower/upper to `[0, 5]`.

See [Raw Measurements to Condition Indices](Raw_Measurements_to_Condition_Indices.md) for the full derivation rationale.

---

## 4. Phase 2 — Joint aggregation

**Progress: 10 %**

The engine optimizes at the **joint level**, not the segment level. A joint is a contiguous group of segments that share geometry and a single `joint_id` (set during the ingest pipeline — see the [Data Pipeline doc](WVDOT_PMS_Data_Pipeline.md#33-pavement-joints)). Think of a joint as "the thing that gets let as a single contract".

`aggregate_segments_to_joints()` (`engine/optimization/chunked.py:173`, reused from `engine/optimization/work_program.py:627`) converts the ~260 K-row segment DataFrame into a much smaller joint DataFrame — typically on the order of many thousands of joints, depending on how the vendor partitions pavement sections into `70_OBJECTID` groups:

| Joint column | Rule |
|--------------|------|
| `joint_id` | Group key |
| `route_id`, `begin_mp`, `end_mp` | First segment's route, min of begin_mp, max of end_mp |
| `length_miles` | Sum of segment lengths |
| `segment_count` | Row count |
| `lane_miles` | Sum of `length × lanes` |
| `aadt` | Length-weighted average |
| `current_psi`, `current_rdi`, `current_sci`, `current_eci`, `current_jci`, `current_csi`, `current_cci` | Length-weighted averages across the joint's segments |
| `pavement_type` | Length-dominant (BC or RC) |
| `family_id` | Length-dominant |

The engine keeps the segment-level DataFrame around too, because resets need to be applied at the segment level (a joint can contain segments with different `family_id`s) and deterioration advances per segment with its own curve.

---

## 5. Phase 3 — Year-by-year rolling loop

**Progress: 10 % → 90 %**

> **Two planning modes.** The outer loop supports a `lookahead_years` config parameter (default `3`). When `lookahead_years = 1`, each iteration solves a **single-year greedy IBC** — the "beating heart" described below. When `lookahead_years > 1`, each iteration solves a **k-year rolling-horizon (MPC) plan** via `_plan_rolling_window()` in `chunked.py`, committing only the year-1 selections and re-planning with a fresh window on the next iteration. The sub-steps 3a–3g described below all still run — they just run *inside* each offset of the window. See [Optimization Logic §12 "Rolling-horizon look-ahead"](WVDOT_PMS_Optimization_Logic.md#12-rolling-horizon-look-ahead) for the window semantics, and [Other Optimization Strategies](WVDOT_PMS_Other_Optimization_Strategies.md) for *why* this mode exists.

This is the beating heart of the engine. A simple `for year in range(1, analysis_years + 1):` loop (`chunked.py:1231`) runs seven sub-steps per year:

```
      ┌─────────────────────────────────────────────┐
      │  Per-year loop (year = 1 … analysis_years)  │
      └─────────────────────────────────────────────┘
                        │
                        ▼
        ┌──────────────────────────────────┐
        │ 3a. prepare_strategies_chunked   │  cross join joints × treatments
        │     → strategies parquet chunks  │  millions of rows
        └──────────────────────────────────┘
                        │
                        ▼
        ┌──────────────────────────────────┐
        │ 3b. evaluate_triggers_polars     │  keep only joints that pass
        │     (inline inside strategies)   │  an index-window branch
        └──────────────────────────────────┘
                        │
                        ▼
        ┌──────────────────────────────────┐
        │ 3c. calculate_benefits +          │  AUC benefit, AADT weighting
        │     calculate_weighted_benefits  │  cost per strategy
        └──────────────────────────────────┘
                        │
                        ▼
        ┌──────────────────────────────────┐
        │ 3d. run_ibc_optimization_chunked │  pick joints greedily by IBC
        │     → selected_joints_df          │  until the budget runs out
        └──────────────────────────────────┘
                        │
                        ▼
        ┌──────────────────────────────────┐
        │ 3e. _apply_treatment_resets       │  update indices on selected
        │     _polars                        │  segments per reset mode
        └──────────────────────────────────┘
                        │
                        ▼
        ┌──────────────────────────────────┐
        │ 3f. _advance_deterioration_polars │  age every segment +1 year
        │     → advance_conditions_one_year │  along its family's curves
        └──────────────────────────────────┘
                        │
                        ▼
        ┌──────────────────────────────────┐
        │ 3g. _calculate_network_gfp        │  pct_good / pct_fair / pct_poor
        └──────────────────────────────────┘
                        │
                        ▼
        ┌──────────────────────────────────┐
        │ 3h. re-aggregate to joints,       │  feed into year + 1
        │     apply min_interval cooldown   │
        └──────────────────────────────────┘
```

> `progress_tracker.update(f"Processing year {year} of {analysis_years}", 10 + int(80 * year / years))` runs at the top of each iteration (`chunked.py:1233`).

### 5a. Build treatment strategies

`prepare_strategies_chunked()` (`chunked.py:551`) builds a DataFrame of every feasible `(joint_id, treatment_id)` pair for this year, cross-joining the joint DataFrame against the treatment catalog. The result is hundreds of thousands to several million rows for a full WV state system (scale: ~260 K segments × 14 treatments before trigger filters, compressed after aggregation + eligibility evaluation), which is why chunked mode streams the output to parquet files and processes them in slices.

Output columns: `joint_id`, `treatment_id`, `cost`, `benefit`, `weighted_benefit`, `incremental_bc_ratio`.

Before emitting a row the function applies three filters:

1. **Trigger eligibility** — see [5b](#5b-trigger-evaluation).
2. **Pavement-type compatibility** — a `treatment.pavement_type_applicable = 'BC'` treatment can't be applied to an `RC` joint.
3. **Cooldown** — a joint that was treated in year `Y − k` for `k < min_interval_years` is excluded this year.

### 5b. Trigger evaluation

`engine/treatments/triggers.py : evaluate_triggers_polars()` (lines 187–507).

The function cross-joins the joint DataFrame against the trigger DataFrame, then applies vectorized bounds checks:

```
eligible = (
    psi_lower <= current_psi <= psi_upper AND
    rdi_lower <= current_rdi <= rdi_upper AND
    sci_lower <= current_sci <= sci_upper AND
    eci_lower <= current_eci <= eci_upper AND
    jci_lower <= current_jci <= jci_upper AND
    csi_lower <= current_csi <= csi_upper AND
    pavement_type matches AND
    length_miles >= min_section_length
)
```

Each trigger row is a **branch**. A joint qualifies for a treatment if it passes **any** branch of that treatment (OR logic between branches, AND logic within a branch). Multiple branches let you express "crack seal is eligible either when the pavement is borderline (PSI 3.5–4.5) OR when it's already preservation-window (SCI 3.0–4.0)".

**Committed projects** (added by `db/migrations/008_add_committed_columns.sql`) short-circuit this logic:

- If a segment has `is_committed = TRUE` and `committed_program_year == year`, the committed treatment is forced and the window checks are bypassed (emitted with `trigger_branch_passed = 0`).
- If `current_year < committed_program_year`, the segment is **locked** — no treatment is emitted for it. You can't "pull forward" a commitment.
- If `current_year > committed_program_year`, the commitment has expired and normal condition-based triggering resumes.

The committed-project guard lives in `engine/treatments/triggers.py:198-212, 276-316`.

### 5c. Benefit + cost + weighting

For every surviving `(joint, treatment)` strategy, the engine computes three numbers: **cost**, **benefit**, and **weighted benefit**.

**Cost** (`engine/optimization/work_program.py:584-589`):

```
if lane_miles available:   total_cost = unit_cost_per_lanemile × lane_miles
else:                      total_cost = unit_cost_per_lanemile × length_miles × lanes
```

When `treatment_costs_lookup` has a row for `(treatment_id, pavement_type)` it overrides the flat `treatments.unit_cost_per_lanemile`.

**Benefit — area-under-curve CCI difference** (`engine/benefits/auc.py:179-270`):

```
Benefit = ∫[ CCI_with_treatment(t) − CCI_do_nothing(t) ] dt,   t = 0 … service_life_years
```

Both curves are projected forward from the current segment state using `project_condition_multi_year()`. The "with treatment" curve starts from the reset indices (e.g. ADDITIVE adds delta, ABSOLUTE clamps to at least the delta value) and then deteriorates forward along the *new* family's curves (because the treatment also migrates the segment's `rehab_type` → `Initial`/`Minor`/`Major`). The trapezoidal integration is in `auc.py:66-87`.

**Traffic weighting** (`engine/benefits/weighting.py`):

```
traffic_weight   = AADT ^ power_exponent      (power_exponent defaults to 0.25)
weighted_benefit = benefit × length_miles × traffic_weight
```

The power exponent dampens high-AADT dominance: with `p = 0.25` a 100 K-AADT interstate gets ~3.2× the weight of a 1 K-AADT local road rather than 100× the raw ratio. Length is folded in so long joints don't get penalized against short joints with the same condition.

`calculate_weighted_benefits_polars()` (lines 268–350) vectorizes all three across the full strategy frame in one pass.

### 5d. IBC selection

**IBC = Incremental Benefit-Cost ratio.** The algorithm lives in `engine/optimization/ibc.py`.

The core idea: for each joint there's a menu of possible treatments (including *do-nothing*) with increasing cost. We don't want to pick the "best" treatment for each joint independently — we want to spend each marginal dollar where it buys the most marginal benefit, across the whole network.

For each joint, after [5c](#5c-benefit--cost--weighting) gives us `(cost, benefit)` for every candidate treatment, the engine:

1. **Builds the efficiency frontier** (`ibc.py:150-203`) — sorts the joint's options by cost, then drops any option that a cheaper option already dominates on benefit. The surviving points form a cost-increasing, benefit-increasing staircase.
2. **Computes incremental ratios** (`ibc.py:206-258`) — for each remaining option `n`, `IBC_n = (benefit_n − benefit_{n−1}) / (cost_n − cost_{n−1})`. The first step is `IBC_1 = benefit_1 / cost_1`.
3. **Greedy selection loop** (`ibc.py:261-434`) — the scheduler scans every joint's available upgrade step across the whole network and picks the one `(joint, treatment)` with the highest incremental ratio *that fits in the remaining budget*. It applies the upgrade (commits that joint to that treatment), deducts the incremental cost, and repeats.
4. **Stopping conditions**:
   - Budget exhausted.
   - No option affordable with remaining budget.
   - Best remaining incremental ratio falls below `minimum_bc_ratio` (the run config's floor).

The loop is **not** heap-based — it's a scan per selection. That's fine because the total number of `(joint, treatment)` options is small (~10 K) and each selection is cheap after polars vectorizes the scan.

**Joint-level selection, segment-level execution.** The selected output is a `selected_joints_df` with one row per selected joint. The engine then joins it back against the segment DataFrame to produce a `selected_segments_df` where every segment in a selected joint is tagged with the chosen treatment. Resets and deterioration apply at the segment level.

**Budget carryover** (`work_program.py:938-995`): if `allow_budget_carryover=True`, unused budget at the end of a year is added to next year's allotment. Otherwise it's lost — "use it or lose it".

### 5e. Apply treatment resets

For every segment in a selected joint, `_apply_treatment_resets_polars()` (`engine/optimization/work_program.py:223`) applies each reset rule for the chosen treatment:

| Mode | Rule |
|------|------|
| `ADDITIVE` | `new = MIN(current + reset_delta, 5.0)` — e.g. a thin overlay adds 0.5 to PSI |
| `ABSOLUTE` | `new = MAX(reset_delta, current)` — only improves, never worsens, e.g. reconstruction forces PSI ≥ 4.8 |
| `HOLD` | `new = current` — no index change (crack seal, saw-and-seal joints), but the segment's age clock freezes for this year |

Age behavior:

- For `ADDITIVE` / `ABSOLUTE`, the relevant `age_{index}` columns are back-calculated to the age at which a pristine-family curve would give this new value (`compute_equivalent_age()` in `engine/deterioration/models.py:366-466`). So a newly-overlaid segment effectively re-enters its new family's curve at the age where the curve intersects the reset value.
- For `HOLD`, age is literally frozen — it doesn't increment during the advance step that follows.

**Family migration** — applying a treatment changes `rehab_type` (e.g. reconstruction sends a segment to `Initial`, a thick overlay to `Major`). That means the segment is now on a different `pavement_families` row, with different curve coefficients. The mapping is `TREATMENT_REHAB_TYPE_MAP` in `engine/deterioration/models.py:281-286`.

After resetting each individual index, the segment's `current_cci` is recomputed as `MIN(PSI, RDI, SCI)` or `MIN(PSI, CSI, JCI)` — `apply_treatment_resets()` does not do this itself, it's the caller's responsibility (handled by `_apply_treatment_resets_polars` immediately after).

### 5f. Advance deterioration

`_advance_deterioration_polars()` (`work_program.py:373`) calls `engine/deterioration/models.py : advance_conditions_one_year()` (lines 869–999), which:

1. Takes the segment DataFrame and every segment's `family_id`.
2. Looks up the per-index curve coefficients (alpha=C1, beta=C2, c3=C3, curve_type, initial_value) from `pavement_families`.
3. Computes the one-year deterioration delta for each index:
   - **polynomial**: `delta = C1·1 + C2·((age+1)² − age²)`
   - **linear**: `delta = C1`
   - **sigmoid / Weibull**: `delta = value(age) − value(age + 1)` using `Max − C1·EXP(−(C2/age)^C3)`
   - **logarithmic**: `delta = value(age) − value(age + 1)` using `Max − EXP(C1 + C2·C3^LOG(1/age))`
   - **power**: fallback power law
4. Subtracts the delta from the current index, clamps `[0, 5]`, increments the per-index age.
5. Recomputes `current_cci` from the six indices.

Untreated segments are advanced too — they get a year's worth of extra wear. Treated segments start this step from their post-reset values (step [5e](#5e-apply-treatment-resets)).

### 5g. Network GFP

`_calculate_network_gfp()` (`work_program.py:97`) computes the three numbers that drive the trajectory chart on the Run Detail page:

- `pct_good`  — share of network where `CCI ≥ 3.5`
- `pct_fair`  — share of network where `2.5 ≤ CCI < 3.5`
- `pct_poor`  — share of network where `CCI < 2.5`

GFP is computed *by lane-miles*, not by segment count, so a long interstate joint counts more than a short secondary-route joint.

### 5h. Feed into next year

The updated segment DataFrame is re-aggregated to joints (same `aggregate_segments_to_joints` function), the `min_interval_years` cooldown table is updated to mark each selected joint's last-treatment year, and the loop continues with `year + 1`.

---

## 6. Phase 4 — Build `result_summary`

**Progress: 95 %**

When the yearly loop finishes, `engine/optimization/work_program.py : summarize_work_program()` (line 1273) collapses the accumulated output into a single JSON blob that matches the shape in [Database Reference §6.1](WVDOT_PMS_Database_Reference.md#6-analysis-runtime-tables).

Key sub-functions:

| Function | File:line | What it builds |
|----------|-----------|----------------|
| `summarize_work_program` | `work_program.py:1273` | Top-level dict |
| `_build_distribution_pivots` | `work_program.py:1367` | The year × treatment heatmaps (`distribution_by_year.count`, `.cost`, `.miles`) consumed by the Treatments tab |
| `joint_work_program_df.group_by('treatment_id')...` | `work_program.py` | `treatment_mix` |
| `joint_work_program_df.rows(named=True)` | `work_program.py` | `project_summary` |
| `yearly_results` serialization | `work_program.py` | `yearly_summary` |

This blob is what eventually gets written to `analysis_runs.result_summary` and becomes the single source of truth for every read on the UI side. No separate result tables.

---

## 7. Phase 5 — Write results + XLSX export

**Progress: 100 %**

Back in `api/routes/runs.py : _execute_run` (lines 352–675):

```python
UPDATE analysis_runs
   SET status = 'completed',
       progress_pct = 100,
       progress_step = 'Complete',
       result_summary = :summary,
       completed_at = NOW()
 WHERE run_id = :run_id
```

The thread then detaches its `DatabaseLogHandler` (flushing the log buffer first), releases the advisory lock, and exits.

### XLSX export

When the user clicks *Download Excel*, `api/routes/runs.py : export_run_xlsx` (lines 1326+) calls `engine/exports.py : export_work_program_to_excel()` (line 105). The export reads `analysis_runs.result_summary` and writes a temporary XLSX with these sheets:

- **Configuration** — budget, analysis years, power exponent, duration, treatments table
- **Work Program** — joint-level project list (route, MP, treatment, year, length, cost, benefit)
- **Yearly Summary** — GFP trajectory + segments treated + cost per year
- **Treatment Mix** — aggregate counts and cost by treatment
- **By Year — Count / Cost / Miles** — three pivot heatmaps (treatments × years)

The temp file is deleted after FastAPI finishes streaming the response.

---

## 8. Data structures in flight

Knowing the shape of the frames moving through the engine makes debugging much easier. Everything is Polars; nothing is pandas.

### Segment-level DataFrame (`analysis_df`)

~260 000 rows. Key columns:

```
analysis_segment_id (PK) · joint_id · route_id · begin_mp · end_mp · length_miles · lanes
current_psi · current_rdi · current_sci · current_eci · current_jci · current_csi · current_cci
age_psi · age_rdi · age_sci · age_eci · age_jci · age_csi · current_age
current_iri · current_rut · current_crack                (kept for display / back-sync)
aadt · pavement_type · family_id · rehab_type · truck_load
is_committed · committed_treatment_id · committed_program_year
```

Mutated in-place each year (well — Polars is immutable, so each year produces a new frame the engine keeps as its "current state"). By the end of the run the frame reflects the network condition at year `analysis_years`.

### Joint-level DataFrame (`current_joint_conditions`)

Many thousands of rows (one per unique `joint_id`; exact count depends on the vendor's `70_OBJECTID` partitioning of the network). Length-weighted aggregates of the segment frame:

```
joint_id (PK) · route_id · begin_mp · end_mp · length_miles · segment_count · lane_miles
current_psi · current_rdi · current_sci · current_eci · current_jci · current_csi · current_cci
aadt · pavement_type · family_id
```

### Strategies DataFrame

Built once per year, then dropped. Potentially very wide (hundreds of thousands to several million rows = joints × feasible treatments per year, at WV state network scale). Columns:

```
joint_id · treatment_id · cost · benefit · weighted_benefit · incremental_bc_ratio
```

In chunked mode this is written to parquet files and read back in slices to avoid OOM on large networks (`engine/optimization/chunked.py:551`).

When the engine runs with `lookahead_years > 1`, this frame is built **once per window offset** inside `_plan_rolling_window` against a *projected* joint state (segments aged forward by the offset, no treatments applied during projection). Only the strategies for offset 0 produce commitments; the rest are planning-scratch and are discarded at the end of each outer year.

### Selected joints (`selected_joints_df`)

~50–200 rows per year. Same columns as strategies plus a `selection_rank` and the year.

### Joint work program (`joint_work_program_df`) — primary output

Accumulated across all years. One row per *(joint, year-it-was-selected)*. A joint can appear in multiple years if `min_interval_years` allows it. Columns:

```
program_year · joint_id · route_id · begin_mp · end_mp · treatment_id · treatment_name
length_miles · segment_count · lane_miles · cost · benefit · weighted_benefit
incremental_bc_ratio · selection_rank · aadt
```

### Yearly results

A Python list of `YearlyWorkProgramResult` dataclasses, one per year `0 … analysis_years`. Each holds: `program_year`, `budget`, `budget_used`, `segments_treated`, `pct_good`, `pct_fair`, `pct_poor`, `cumulative_cost`, `cumulative_benefit`. Year 0 is the pre-optimization baseline — that's where the "% Good" trajectory starts.

---

## 9. Live progress + log capture

The Run Detail page in the UI is live — you can watch the progress bar tick and the log tail stream while the engine is running. Two small pieces of plumbing make that work.

### `ProgressTracker` — `engine/progress.py:22-56`

A lightweight class constructed with the run ID and a SQLAlchemy engine. `tracker.update(step, pct)` runs:

```sql
UPDATE analysis_runs
   SET progress_step = :step,
       progress_pct  = :pct
 WHERE run_id = :run_id
```

No session, no ORM — just a one-shot `engine.execute` so the write is immediately visible to any reader.

Call sites:

| Step | pct | Where | File:line |
|------|-----|-------|-----------|
| "Validating inputs" | 5 | Start of validation | `runner.py:317` |
| "Calculating condition indices" | 8 | Right before CCI derivation | `runner.py:346` |
| "Aggregating segments to joints" | 10 | Start of joint aggregation | `chunked.py:1199` |
| "Processing year N of Y" | 10 + 80·(y/years) | Top of each yearly iteration | `chunked.py:1233` |
| "Finalizing results" | 95 | Before summarization | `runner.py:389` |
| "Complete" | 100 | Written by `_execute_run` | `runs.py:~675` |

### `DatabaseLogHandler` — `engine/log_capture.py:25-86`

A `logging.Handler` that gets attached to the `engine` and `api` loggers at the start of `_execute_run` (`runs.py:385`) and detached at the end (`runs.py:675`). It buffers log records in memory (default 25 records), flushes with a single batched `INSERT INTO run_logs` when the buffer fills or when `close()` is called.

The UI reads log lines via `GET /api/runs/{id}/logs?offset=&limit=` — the endpoint is paginated and can be tailed by polling.

---

## 10. Single-run advisory lock

Only one analysis run can execute per process at a time. `_execute_run` acquires a Postgres advisory lock via `pg_try_advisory_lock(<literal>)` at the top of the thread and releases it at the end. If a second run is submitted while one is in progress, its thread will block on the lock. This is a deliberate simplification: the engine uses a lot of memory and CPU when a run is in flight, and running two in parallel on one box produces unpredictable results. Scale-out (across processes / machines) is a future concern.

The lock also ensures the `ProgressTracker` and `DatabaseLogHandler` writes from different runs never interleave — each run owns the global handlers for its duration.
