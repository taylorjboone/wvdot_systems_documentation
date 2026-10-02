# Plan: addressing the v1.6 implementation review

> **Status (2026-09-25):** implemented in v1.7.0 (migrations 035–039). Decisions taken: config versions
> replace the run lock (runs keep their version; only deleting a config deletes runs); GFP profiles are
> select-only system profiles; the greedy look-ahead is removed; the per-year Poor cap became the
> MILP-assist `every_year` option, which holds **both** targets in every year as soft rows; the Turnpike
> is dTIMS's `PMS_abfOBJ_TP` (I-77 supplemental 16, and I-64 EB in Raleigh County from MP 117.93).
> Not done: `engine/runner.py` and the unused `/api/deterioration/*` routes still use the old projector;
> the cracking-source switch waits for survey data with PERCENT_CRACKING.

Written 2026-09-25 against `16ee759` (v1.6.0) plus the uncommitted MILP work: trigger-filtered candidates, Good-aware scope, Poor-first fallback, and jointless Poor length. It responds to [README.md](README.md) in this folder.

The review's verdict holds. The condition kernel is sound. What is weak is the contract around it: policy that lives in code, settings that don't reach every consumer, and paths that price, check eligibility or simulate differently. This plan makes the **configuration the single, compiled, versioned source of treatment and network policy**. Every consumer then reads that one compiled object. The mathematics (curves, inverse ages, the op interpreter, the solver) stays in code.

## 0. Principles

1. **Code owns operators; configuration owns policy.**
   - Code: curve formulas, the reset-op vocabulary, the predicate vocabulary, integration and discounting, the solver.
   - Configuration: which roads a rule applies to, the numbers, which treatment does what, fallbacks.
   - No WVDOT-specific literal remains in engine code; `I-68`, `sign == '1'`, `.15/.37/.56`, `2026`, drift coefficients and `RECONSTRUCT%` all move to tables.
2. **Compile once, then consume.** A run starts by compiling its config into an immutable `CompiledConfig`, which is validated, hashed and stored with the run. Greedy, MILP, commitments, Validate, exports and the outlook pages all take that object. None of them reads config tables on its own.
3. **One function per concept.** One pricing function, one eligibility evaluator, one annual transition, one GFP classifier. A second implementation of any of these is a bug.
4. **Fail loudly.**
   - An invalid config fails at compile time, with treatment/family/index context.
   - An execution error fails the run.
   - A best-effort result says what it relaxed.
5. **Every exposed setting has an effect test.** A setting that no test can show changes an output doesn't ship.

## 1. Configurable policy layer (the core of this plan)

This work adds new per-config tables (key includes `config_id`, run-locked, copied by `copy_config`, round-tripped by the workbook, shown on the Config page). They go in migrations 035–038.

### 1.1 Route groups: replacing `sign_rule`, `exclude_i68`, the Interstate cost test and the HPMS proxy

```
route_groups(config_id, group_key, label, description)
route_group_terms(config_id, group_key, term_order, field, op, value, negate)
```

- A group matches a segment when **all** its terms match. For an OR, define two groups and a third with `op = 'in_group'`.
- **Allowed fields:** a fixed allow-list of inventory columns: `sign_code`, `route_number`, `route_id`, `functional_class`, `nhs_code`, `district`, `county_code`, `special_system`, `lanes`, `pavement_type`.
- **Allowed ops:** `=`, `!=`, `in`, `not_in`, `between`, `prefix`, `in_group`.
- There is no SQL or Python text anywhere. Terms compile to a polars expression and to a SQL fragment (the pipeline and checks need the latter). Both come from one compiler, so they can't disagree.

Seed rows for config 1 and every copy, reproducing today's behaviour and fixing the IM_Funds gap:

| group_key | Terms | Replaces |
|---|---|---|
| `INTERSTATE` | `sign_code = '1'` | `sign_rule`, the Interstate cost test in `cost.py` |
| `TURNPIKE` | The dTIMS `IM_Funds` Turnpike exclusion. Its exact field and value come from `expressions.md` and must be confirmed before seeding. | — |
| `IM_FUNDS` | `in_group INTERSTATE`, `negate in_group TURNPIKE` | `sign_rule = 'im_funds'`; review item 8 |
| `I68` | `sign_code = '1'`, `route_number = '68'` | `exclude_i68` |
| `HPMS_1` | `functional_class between 1 and 3` | `hpms_flag` / `hpms_source = 'fc_proxy'` in `pipeline/dtims_inputs.py` |

Treatments reference groups by key:

- `treatments.require_route_group` (nullable) and `treatments.exclude_route_group` (nullable) replace `sign_rule` and `exclude_i68`.
  - Chip seal: exclude `INTERSTATE`, plus a second exclude for `I68`. Two exclude slots, or a group `CHIP_EXCLUDED = INTERSTATE ∪ I68`.
  - Reconstruction: require `IM_FUNDS`.
- `treatment_cost_adjustments(config_id, treatment_id, route_group, multiplier)` replaces `sign1_cost_multiplier`. The seed is thick overlay × 1.2 on `INTERSTATE`.

### 1.2 Condition initializers and start-age policy: replacing `DRIFT_*`, `MAX_START_AGE` and the 15-year default

```
condition_initializers(config_id, pavement_type, rehab_type,
                       new_base,            -- 5.0 / 4.5 when rehab is newer than the survey
                       drift_a, drift_b, drift_c,
                       max_start_age,       -- 15
                       missing_rehab_age)   -- 15 (dTIMS: missing year = 0)
```

Six seed rows (BC and RC × Initial, Major, Minor) come from today's constants. `pipeline/families.init_condition` and `dtims_state.initial_state` read them from `CompiledConfig`.

### 1.3 Cracking progression: replacing `.15 / .37 / .56`

```
cracking_rules(config_id, rule_order, route_group NULL, factor)
```

The first matching rule wins, and a row with a NULL group is the default. Seeds:

| rule_order | route_group | factor |
|---|---|---|
| 1 | `INTERSTATE` | 0.15 |
| 2 | `HPMS_1` | 0.37 |
| 3 | NULL (default) | 0.56 |

### 1.4 Counters: replacing the hard-coded `cnt_chip` / `cnt_micro`

```
treatment_counters(config_id, counter_key, label)
```

- State columns `cnt_<key>` are created from this table.
- `CNT_SET` / `CNT_INC` ops and `treatment_triggers.counter_name` become foreign keys to it.
- The compile step rejects an op or trigger that names an unknown counter.

### 1.5 Rehab history mapping: moving an interpretation out of the inventory

Today `REHAB_TYPE_SQL` hard-codes reconstruction → Initial, thick → Major, anything else → Minor, and stores the result on `analysis_segments`, which is inventory. Review item 13 asks for inventory facts and interpretations to be kept apart.

- **Inventory** (`analysis_segments`) keeps facts only: `rehab_year`, `rehab_project_id`, the project's own treatment code, and `rehab_coverage` (the share of the segment the project covers).
- **Per config** (`segment_families`, computed in the families step): the rehab type is the `REHAB_SET` op of the matching config treatment. That is one source of truth, the same one the resets use.
- Hub treatments that don't map to a config treatment go through `project_treatment_map(config_id, hub_treatment_code, treatment_id)`. An unmapped code is reported as a coverage gap, not silently set to Minor.
- `refresh_inputs` rebuilds every assignment from the current spatial matches instead of patching old ones (review item 13's stale-assignment risk). It also applies a configurable minimum coverage (see 1.7).

### 1.6 Good/Fair/Poor classification profiles: replacing `GFP_*` in three places

```
gfp_profiles(profile_key, version, label, is_system)
gfp_profile_thresholds(profile_key, pavement_type, metric, good_below, poor_above, used)
configs.gfp_profile_key
```

- `MAP21_2017` is seeded as a read-only system profile.
- A config selects a profile rather than editing thresholds inline, because thresholds are federal policy (review item 8).
- The Python classifier, the SQL twin (`pipeline/checks.MAP21_SQL`) and the UI (`rawBands.ts`, `format.ts`) all read the profile: Python and SQL through `CompiledConfig`, the UI from a new `GET /api/configs/{id}/gfp-profile`. The "keep in step" rule in `CLAUDE.md` then goes away.
- Runs record `gfp_profile_key@version`, which supersedes the `gfp_basis` string. Old runs map to `cci_band`.

### 1.7 Model constants and input policy: completing migration 034

These columns join `configs` alongside `adt_exponent`, `discount_rate`, `inflation_rate` and `benefit_integration`:

| Column | Today | Default |
|---|---|---|
| `start_year` | `DEFAULT_START_YEAR = 2026` in code | NULL, meaning the current calendar year at run creation. It is resolved and stored in the run spec. |
| `default_lanes` | `2.0` in `lane_miles_expr` | 2 |
| `index_lower_bound` | `LOWER_BOUND = -1` | −1 |
| `min_qualifying_fraction` | 0 (hidden argument) | 0. This is the joint-coverage rule from review item 13, made visible. |
| `min_rehab_coverage` | any overlap | 0.5 |
| `adt_growth_fallback` | fixed chain | `'layer2,layer2_future,district_median,zero'` (an ordered list from a fixed vocabulary) |
| `cost_basis` | joint-level pavement | `'segment'`: each member priced at its own pavement's rate (review item 2) |

`IRI_CAP = 500` and the curve formulas stay in code as model-version constants. They are part of the dTIMS model, not WVDOT policy.

### 1.8 Remove the duplicated fields (review item 7)

| Duplicate | Resolution |
|---|---|
| `treatments.min_length_miles` vs `treatment_triggers.min_section_length` | The treatment value is authoritative. Rename the branch column `min_length_override` (nullable); the effective value is the override if set, else the treatment's. Migration 035 nulls overrides that equal the treatment value. |
| `interval_years` vs `min_interval_years` | Keep `interval_years` (dTIMS IntervalYear, same treatment) and `min_years_since_last` (any treatment). Drop `min_interval_years`; the cooldown filter in `chunked.py` reads `interval_years`. The workbook rejects the old column with a clear message. |

### 1.9 The config compiler: `engine/config/compiled.py` (new)

`compile_config(conn, config_id) -> CompiledConfig` is a frozen dataclass holding:

- the treatments, triggers, ops, costs, sequencing, curves, family rules, route-group expressions, initializers, cracking rules, counters, GFP profile and constants
- a `content_hash` over the canonical serialisation of all of the above

Validation happens there, once (review item 5):

- **Reachable families.** All families produced by the family rules, closed under every `PAVE_SET` / `REHAB_SET` op, need a supported curve (polynomial, linear, sigmoid) for every index that applies to their pavement type. Log is rejected. The error message names the treatment → family → index path.
- **Applicability is separate from missing data.** `CurveBook` gets an explicit `applicable_<idx>` flag. A null offset on an applicable index becomes a compile error, not a silent freeze. Inverse-age domain misses are clamped and counted, and the count is reported in the run's warnings.
- **Every reference resolves:** route groups, counters, sequencing IDs, costs for every (active treatment × applicable pavement), and initializers for every (pavement × rehab).
- **Contradictions and dead rules:** a branch override longer than the treatment minimum, a treatment that can never trigger (keeps today's warning), and a cracking rule with no default.

Everything uses the compiler:

- The workbook import dry-run compiles the would-be config before the diff is accepted.
- The Config page shows compile status.
- A run refuses to start on a compile error.

### 1.10 Config versions instead of deleting runs

Today, editing a config that runs have used forces deleting those runs (the run lock). Once runs need to pin their inputs (review item 11), a better model is available:

- **`config_versions(config_id, version, content_hash, snapshot JSONB, created_at, created_by)`.** Compiling an edited config appends a version, and runs reference `(config_id, version)`.
- **Editing is safe.** An edit never changes a finished run, because the run reads its snapshot.
- **The run lock can be relaxed** from "delete the runs" to "these runs will keep the old version". This is a product decision; see open decisions.

### 1.11 UI, workbook and docs for 1.1–1.10

- **Config page:** new tabs for Route Groups, Initializers, Cracking, Counters and Constants (extended), plus a GFP profile picker and a compile-status banner that links errors to the offending row.
- **Workbook:** `FORMAT_VERSION` 3, with one sheet per new table, a `Col` per new column, and version-2 workbooks rejected with a message.
- **Docs:**
  - Business Logic: a policy-layer section and the table reference.
  - Usage: the Config page tabs.
  - Data Pipeline: rehab facts vs interpretation.
  - `CLAUDE.md`: "policy lives in config tables; the compiler is the only reader".

## 2. Run specification and effective settings (review item 4)

`analysis_runs.run_spec JSONB` is written once at run creation and is immutable:

```
{ config_id, config_version, config_hash,
  start_year, economics: {inflation_rate, discount_rate, adt_exponent, benefit_integration},
  gfp_profile, joint_build_id, inventory_refresh_id, model_version (BACKEND_VERSION + kernel hash),
  overrides: {field: value}  # only what the request explicitly set }
```

- **Request fields become Optional with no default.** `CreateRunRequest.power_exponent` defaults to None and resolves to the config's `adt_exponent`. The same applies to inflation and start year. Today's 0.25 default silently beats the config's 0.2.
- **Consumers take `RunSpec` + `CompiledConfig`** instead of loose keyword arguments: chunked, constrained, MILP, `calculate_benefits_polars` (discount, integration, exponent), Validate and exports.
- **Benefit weighting uses the evolving ADT.** Integrate `ADT_t^p` year by year from the simulated `adt`, not the static `aadt` after integration.
- **Effect tests.** A parametrised test walks every workbook `Col` flagged `affects_run=True`, perturbs only that value on a small fixture network, and asserts the documented output changes. For example, discount rate changes benefit, cracking factor changes year-5 `pcrk`, and a route-group term changes eligibility.

## 3. One pricing function (review item 2)

In `engine/optimization/cost.py`:

```
price(segments, treatment_id, program_year, cfg: CompiledConfig, spec: RunSpec)
    -> per-segment cost, summed project cost
```

- **Rate:** `treatment_costs[treatment, segment pavement before treatment]`. A missing rate is a compile error. There is no fallback to `unit_cost_per_lanemile`, which becomes display-only or is dropped.
- **Adjustments:** × the matching `treatment_cost_adjustments` for the segment's route groups, × `(1 + inflation)^(program_year − 1)`, × lane-miles with `default_lanes`.
- **Mixed joints:** the cost is the sum over member segments (`cost_basis = 'segment'`).
- **Every pricer calls it:** greedy candidate pricing, `_treatment_lane_mile_cost_map` in MILP (deleted), the forced-commitment block in `chunked.py`, `api/validation/plan.py` (the `INFLATION = 0.02` constant is deleted), exports and manual Validate edits.
- **Cross-path test:** the same joint × treatment × year has the same cost through all of them.

## 4. MILP correctness (review items 1 and 3)

1. **Per-target, per-year signed coefficients.**
   - The precompute evaluates every (metric, measurement year) pair that is configured: Poor at `poor_target_year`, Good at `good_target_year`, and every year if a per-year cap is added.
   - A candidate applied after a measurement year has coefficient 0 for that year.
   - The candidate horizon is the latest target year, not the Poor year.
2. **Keep net effects.** Insert negative coefficients, and always emit each requested target row, even when the baseline already satisfies it, because a harmful candidate can use up the slack.
3. **Commitments are mandatory.**
   - Committed (joint, treatment, year) rows become fixed variables (lb = ub = 1). Their cost is charged to the budget row, and their effects are included in the baseline the other candidates are measured against.
   - Conflicting or over-budget commitments raise an explicit error listing the projects.
   - A commitment followed by another treatment on the same joint is rejected with a clear message while MILP stays one treatment per joint.
4. **Verify after solving.** Replay the selected plan through `simulate`, recompute every target row, and report the predicted vs achieved values per row. Declare "satisfied" only from the replay. The 0.5-point tolerance becomes a reported margin, not a pass.
5. **Optional every-year Poor cap.** `max_pct_poor_every_year` adds one row per year; this addresses the gap seen in run 307, where Poor exceeded 5% in years 6–11.
6. **Tests:** unequal target years, a harmful candidate against a baseline sitting exactly at the ceiling, forced commitments with a zero budget (the run must fail rather than skip them), and a comparison of predicted and replayed values.

## 5. Fail on errors, not empty programs (review item 6)

- **Rolling window.** Delete the catch-all in `_plan_rolling_window`. An exception fails the run with `status='failed'` and a structured `error_detail` (stage, treatment, family, message).
- **Distinct outcomes in the result**, e.g. `outcome: 'no_eligible' | 'optimal_zero' | 'infeasible_relaxed' | 'optimal'`:
  - no eligible candidates
  - a feasible optimum that treats nothing
  - infeasible targets that were relaxed
  - an optimal plan
- **Required policy.** A failure to load triggers, ops, costs or curves aborts the run. There is no `triggers_df=None` path.
- **UI.** The Runs page and Run detail show "Completed with relaxed targets" or "Failed: <reason>" from these fields.

## 6. One simulator, no stale classifications (review item 10)

- **One annual loop.** `generate_work_program_polars` becomes a thin wrapper over the chunked loop's annual transition, so year 1 is the starting state with no advance, or it is removed with its callers. `engine/runner.py` and the legacy projector are deleted or redirected.
- **No trusted `gfp` column.** `step` and `apply_treatments` drop the `gfp` / `gfp_*` columns, and `network_gfp` always classifies from the raw state. It never trusts an existing `gfp` column.
- **Cross-path test.** One state and one plan go through chunked, MILP replay, Validate and the project outlook, and each must give the same yearly GFP shares.

## 7. Validate: replay vs "today's network" (review item 11)

- **Replay mode (the default).** `RunContext` loads the run's `config_version` snapshot, `run_spec` economics and start year, and the joint build. For inventory, keep a compressed per-run starting-state snapshot of the analysed segments, `run_start_state` (Parquet in a bytea column, a few MB per run). Keeping every inventory refresh indefinitely would be too heavy.
- **"Apply to today's network".** This is an explicit toggle that reloads current inputs and labels the page accordingly.
- **Sanity check.** Compare Validate's replay with the stored yearly results; a mismatch there is now a bug, not drift.

## 8. Data definitions (review items 9 and 13)

- **Cracking source.**
  - Import both `FHWA_Percent_Cracking` and `PERCENT_CRACKING` (the source dTIMS used) with their units.
  - Add a per-config input policy `crack_source` with the values `fhwa` and `dtims_percent`.
  - Rerun the NHS overlay comparison. It needs the 2025 vendor population, which blocks the final decision; until then the default stays at today's value and the docs say so.
- **Rehab rebuild.** Section 1.5 covers this.
- **Joint coverage.** `min_qualifying_fraction` becomes visible (1.7). Mixed-pavement joints apply each member segment's own pavement-filtered ops, as already happens, and are priced per segment (section 3). The docs state that a treatment applies to the whole joint.
- **Growth matching.** Replace midpoint matching with a length-weighted overlap of layer-2 events. Store the source event ID.

## 9. The rolling window (review item 12)

Recommendation: be honest now and improve later.

- **Now:** relabel the greedy optimizer as "yearly greedy (IBC)". Remove the `lookahead_years` simulation, which costs time and doesn't change the first choice, and delete the API text claiming it "catches better-timed treatments".
- **Later, if wanted:** real multi-year selection belongs in MILP, via a multi-treatment strategy generator (sequences per joint rather than one treatment). That is a separate project.

## Phasing

| Phase | Scope | Review items | Depends on |
|---|---|---|---|
| **A. Policy tables + compiler** | 1.1–1.9: migrations 035–038, seeds that reproduce today's results (plus the IM_Funds Turnpike fix), `CompiledConfig`, workbook v3, Config page tabs, docs | 5, 7, 8 | — |
| **B. Run spec + pricing + constants** | 2, 3: `run_spec`, Optional overrides, the single `price()`, effect tests | 2, 4 | A |
| **C. MILP semantics** | 4: signed per-year rows, commitments, post-solve verification, every-year cap | 1, 3 | B |
| **D. Fail loudly + one simulator** | 5, 6 | 6, 10 | B |
| **E. Versions + Validate replay** | 1.10, 7 | 11 | A, B |
| **F. Data definitions** | 8 (cracking needs the vendor data) | 9, 13 | A |
| **G. Optimizer honesty** | 9 | 12 | D |

**Acceptance criterion for phase A:** a regression gate. With the seeded tables, config 1 must reproduce today's run 307, apart from the IM_Funds change, which the gate reports separately. The replay test stays within 1e-6.

**Acceptance for the whole plan:** the cross-path suite passes. It covers eligibility, cost, transition and GFP through greedy, MILP, Validate and the outlook pages, plus the effect tests, unequal target years, harmful candidates, forced commitments, missing and Log curves, and replay after a data refresh.

**Rough size:** A is the largest (about 8 files of engine and API, 4 migrations, the workbook and the Config page). B and C are medium. D, E and G are small to medium. F is mostly waiting on data.

## Open decisions

1. **Config versions (1.10).** Replace "editing deletes runs" with "runs keep their version"? Recommended; it also removes the main pain of the run lock.
2. **GFP profile editability.** Select-only system profiles (recommended), or allow custom profiles per config?
3. **Rolling window (9).** Remove the look-ahead now (recommended), or keep it until a multi-treatment MILP exists?
4. **Every-year Poor cap (4.5).** Offer it as an option or make it the default for Poor targets?
5. **Turnpike term.** Confirm which inventory field identifies the Turnpike before seeding `TURNPIKE`. Today's Sign-1 rule treats the Turnpike as Interstate.

## Mapping to the review

| Review item | Plan section |
|---|---|
| 1. MILP target equations | 4.1, 4.2, 4.4 |
| 2. Pricing not shared | 3, 1.1 (cost adjustments), 1.7 (`cost_basis`) |
| 3. Commitments optional in MILP | 4.3 |
| 4. Constants don't propagate | 2 |
| 5. Missing or Log curves freeze condition | 1.9 |
| 6. Exceptions become empty programs | 5 |
| 7. Duplicated fields | 1.8 |
| 8. Policy embedded in code | 1.1–1.7 |
| 9. Cracking input | 8 |
| 10. One simulator | 6 |
| 11. Validate replays current inputs | 1.10, 7 |
| 12. Rolling window | 9 |
| 13. Joint and refresh semantics | 1.5, 1.7, 8 |
