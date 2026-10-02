# WVDOT PMS Optimization Logic

> How the engine decides which pavement joints get treated each year. The algorithm is an **incremental benefit-cost (IBC) heap** running on an efficiency frontier per joint, constrained by an annual budget with optional carryover. This doc walks through the math, the code, and a worked example.

If you've read the [Analysis Engine doc](WVDOT_PMS_Analysis_Engine.md) already, this is the deep dive on step **5d** — IBC selection — plus the budget machinery around it. If you haven't, start there for context on where selection fits in the per-year loop.

---

## Table of Contents

1. [The problem, stated precisely](#1-the-problem-stated-precisely)
2. [Why IBC instead of plain B/C](#2-why-ibc-instead-of-plain-bc)
3. [The efficiency frontier per joint](#3-the-efficiency-frontier-per-joint)
4. [Computing incremental ratios](#4-computing-incremental-ratios)
5. [The selection loop](#5-the-selection-loop)
6. [Cost enforcement + budget carryover](#6-cost-enforcement--budget-carryover)
7. [Minimum B/C filter](#7-minimum-bc-filter)
8. [The same-treatment interval](#8-the-same-treatment-interval)
9. [Joint-level vs segment-level selection](#9-joint-level-vs-segment-level-selection)
10. [Worked example](#10-worked-example)
11. [Code map](#11-code-map)
12. [Look-ahead (removed in v1.7)](#12-look-ahead-removed-in-v17)
13. [dTIMS condition model and candidates (v1.6)](#13-dtims-condition-model-and-candidates-v16)

---

## 1. The problem, stated precisely

Per year, given:

- `J` = set of joints currently eligible for treatment (after trigger evaluation, pavement-type compatibility, and cooldown filters).
- For each joint `j` and each feasible treatment `t`: a cost `c_{j,t}` and a benefit `b_{j,t}`.
- An annual budget `B`.
- A minimum acceptable benefit-cost ratio `θ` (default 0).

Choose a subset `S ⊆ (joint × treatment)` with at most **one treatment per joint** (MILP-assist with `milp_max_actions` = 2: one treatment or one treatment-plus-re-treatment pair per joint) such that:

- `∑_{(j,t) ∈ S} c_{j,t}  ≤  B`
- the chosen treatment for each joint has incremental B/C at least `θ`,
- `∑_{(j,t) ∈ S} b_{j,t}` is (approximately) maximized.

This is a variant of the 0/1 knapsack problem and is NP-hard in the general case. The engine uses a greedy IBC heuristic that is optimal on the convex hull of the per-joint efficiency frontiers and near-optimal in practice.

---

## 2. Why IBC instead of plain B/C

The naive approach is to sort all `(joint, treatment)` pairs by `benefit / cost` and fill the budget from the top. That produces a well-known pathology: it **over-prefers cheap preservation treatments**. For a joint that's close to poor, `CRACK_SEAL` at $5 K has a very high B/C ratio, but crack sealing a ready-to-reconstruct joint is wasted money — the right treatment is reconstruction, which is cheaper per unit of benefit than the alternative of eventually reconstructing it anyway.

IBC fixes this by asking a different question: "for each joint, starting from the cheapest reasonable treatment, what's the marginal return on *upgrading* to the next one?" A joint's treatment menu is not a flat list of options — it's a **staircase of increasingly expensive, increasingly beneficial** interventions, and we want to spend each marginal dollar where it buys the most marginal benefit across all staircases.

The key property IBC preserves: we never pay for a more expensive treatment unless the extra benefit it buys is competitive with spending the same marginal dollar elsewhere on the network.

---

## 3. The efficiency frontier per joint

`engine/optimization/ibc.py : build_efficiency_frontier()` (lines 150–203).

For each joint `j`, start from the full list of feasible treatments:

```
[(do-nothing, 0, 0), (CRACK_SEAL, 3200, 0.8), (MICROSURFACING, 21000, 1.6),
 (THIN_OVERLAY, 55000, 2.4), (THICK_OVERLAY, 96000, 3.1), (RECONSTRUCT_BC, 280000, 4.2)]
```

1. **Sort by cost ascending.**
2. **Drop dominated points.** A point `(c_a, b_a)` is dominated by `(c_b, b_b)` if `c_b ≤ c_a` and `b_b ≥ b_a`. In practice a "dominated" treatment is one where a cheaper alternative already delivers equal or better benefit, which means you'd never pick the dominated treatment under any budget.
3. **Keep only the convex hull.** After removing dominations, walk the points and drop any middle point whose slope from its predecessor is lower than the slope from its predecessor to its successor — that is, a middle point that lies *below* the line joining its neighbors.

The result is a piecewise-linear, monotonically-increasing staircase:

```
benefit ▲
        │             ●──── RECONSTRUCT
        │           ╱
        │          ●──── THICK_OVERLAY
        │        ╱
        │       ●──── THIN_OVERLAY
        │      ╱
        │     ●──── MICROSURFACING
        │    ╱
        │   ●──── CRACK_SEAL
        │  ╱
        │ ● (do-nothing, 0, 0)
        └────────────────────────▶ cost
```

Each step on the staircase is a candidate selection for this joint.

---

## 4. Computing incremental ratios

`engine/optimization/ibc.py : compute_incremental_bc_ratios()` (lines 206–258).

For the staircase `[(c_0=0, b_0=0), (c_1, b_1), (c_2, b_2), …]`:

```
IBC_1 = b_1 / c_1                          (first step from do-nothing)
IBC_2 = (b_2 - b_1) / (c_2 - c_1)          (upgrading to the second option)
IBC_n = (b_n - b_{n-1}) / (c_n - c_{n-1})  (upgrading to the n-th option)
```

Each `IBC_n` says: "the marginal benefit per marginal dollar if I upgrade this joint from treatment `n-1` to treatment `n`". Because the frontier is convex, the sequence `IBC_1 > IBC_2 > IBC_3 > …` is strictly decreasing — you get diminishing returns, as expected.

---

## 5. The selection loop

`engine/optimization/ibc.py : run_ibc_optimization()` (lines 304–434).

In plain words:

```
remaining_budget = annual_budget
selected = {}                     # joint_id → current treatment rank (0 = do-nothing)

while True:
    best = None                   # (joint_id, next_step_index, IBC)
    for j in eligible_joints:
        rank = selected.get(j, 0)
        next_step = j.frontier[rank + 1]
        if next_step is None:
            continue              # already at top of this joint's staircase
        incremental_cost = next_step.cost - j.frontier[rank].cost
        incremental_benefit = next_step.benefit - j.frontier[rank].benefit
        if incremental_cost > remaining_budget:
            continue              # can't afford the upgrade
        ibc = incremental_benefit / incremental_cost
        if ibc < minimum_bc_ratio:
            continue              # fails the floor
        if best is None or ibc > best.ibc:
            best = (j, rank + 1, ibc)

    if best is None:
        break                     # nothing fits → stop
    selected[best.joint_id] = best.next_rank
    remaining_budget -= next_step.cost - j.frontier[rank].cost
```

A few things to notice:

- The outer `while True` runs once per *selected upgrade*, not once per joint. A joint can be upgraded multiple times in a single year — first from do-nothing to CRACK_SEAL, later (if budget allows) from CRACK_SEAL to MICROSURFACING — because each upgrade is evaluated on its own incremental ratio.
- The scan is *not* a heap. On each iteration it recomputes the best affordable next step across all joints. This sounds slow but the inner loop is vectorized over Polars — the whole selection loop for a 10-year WV run takes single-digit seconds.
- The stopping conditions are: (a) budget exhausted, (b) no affordable option, or (c) best remaining incremental ratio below `minimum_bc_ratio`.
- When two options have identical IBC, the first match wins (order-dependent on the polars scan order). There's no explicit tie-breaker.

`run_ibc_optimization_chunked()` (`engine/optimization/chunked.py:1506`) is the parquet-streaming variant used when the strategies frame is too big to hold in memory. It operates on the same frontier + selection logic, just reads the strategies in slices.

---

## 6. Cost enforcement + budget carryover

Cost enforcement is a hard cap: no option with `incremental_cost > remaining_budget` is ever chosen. There's no partial selection, no "do some fraction of the joint" — you either take the whole upgrade or nothing.

At the end of the year, whatever budget wasn't spent goes one of two places:

- **Carryover on** (`allow_budget_carryover=True`): unused budget is added to next year's allotment. `work_program.py:938-995`.
- **Carryover off** (default, matches most real DOT practice): unused budget is lost. Next year starts fresh with `annual_budget`.

Carryover is a powerful lever. With carryover enabled, the engine can "save up" for a year where several large reconstruction projects line up, spending below budget in the lean years and above in the fat years. Without carryover it gets forced into suboptimal preservation picks just to hit the budget target.

There is no *under-spend penalty*. If the network is so healthy that no treatment meets the `minimum_bc_ratio` threshold, the engine will happily spend $0 that year.

---

## 7. Minimum B/C filter

`minimum_bc_ratio` is a per-run floor applied *after* the incremental ratio is computed. Any step with `IBC < minimum_bc_ratio` is skipped. The effect is equivalent to "don't do treatments whose marginal benefit per marginal dollar falls below this threshold".

Why you'd set it above 0:

- **Force unspent budget into later years** (with carryover on). Set `minimum_bc_ratio = 0.5` and the engine will leave money on the table when nothing's really worth doing, saving it for more productive years.
- **Prune preservation on nearly-new pavement**. Crack sealing a joint with `CCI = 4.7` is cheap but the marginal benefit is tiny — a floor knocks out those picks.
- **Sensitivity analysis**. Running a scenario with `minimum_bc_ratio = 1.0` shows you how the work program degrades when you only fund "really worth it" projects.

Setting it too high produces empty work programs. The default is 0, which means "spend every dollar that produces any positive benefit".

---

## 8. The same-treatment interval

Every treatment has an `interval_years` (dTIMS IntervalYear: thin, thick, micro 2; chip, cape, crack 3; ultra-thin, reconstruction 4; saw & seal, CPR 6). It is one of the **trigger gates** (`engine/treatments/triggers._gate_exprs`): a treatment is not a candidate on a joint while fewer than `interval_years` have passed since that joint last got the same treatment, read from the segments' treatment history (`yr_<treatment>`, stamped when a treatment is applied). Before v1.7 a separate `min_interval_years` cooldown filter ran as well; the two values are merged into `interval_years` (migration 036) and the separate filter is gone. `min_years_since_last` is the wait after *any* treatment (preservation: 6).

---

## 9. Joint-level vs segment-level selection

Selection is done at the **joint level** — one row per joint. But pavement condition and deterioration are tracked at the **segment level** (0.1-mile resolution). The engine spans both:

1. At the start of the yearly loop, segments are aggregated to joints (length-weighted averages of each condition index) — see [Analysis Engine §4](WVDOT_PMS_Analysis_Engine.md#4-phase-2--joint-aggregation).
2. IBC runs on the joint DataFrame. One treatment per joint.
3. After selection, the chosen treatments are *expanded* back to every segment in the selected joints (`engine/optimization/work_program.py:770-789`). Resets and deterioration then apply segment-by-segment.
4. Re-aggregation produces the fresh joint DataFrame for the next year.

The reason selection is at the joint level: that's how contracts are actually let. A DOT doesn't resurface 0.1 miles of pavement — it resurfaces a multi-mile joint in one contract. Operating at the joint level produces realistic project sizes even though the physics (deterioration, condition) lives at the segment level.

---

## 10. Worked example

Let's run a tiny example by hand. Suppose we have three joints:

| Joint | CCI | Length (mi) | AADT | Feasible treatments |
|-------|-----|-------------|------|---------------------|
| J1 | 3.2 | 2.0 | 40 000 | CRACK_SEAL, MICROSURFACING, THIN_OVERLAY |
| J2 | 2.1 | 1.0 | 8 000  | THICK_OVERLAY, RECONSTRUCT |
| J3 | 4.0 | 4.0 | 60 000 | CRACK_SEAL, MICROSURFACING |

Suppose the per-joint strategy frames come out as (numbers made up for illustration):

| Joint | Treatment | Cost ($) | Benefit (CCI·yr) |
|-------|-----------|---------:|----:|
| J1 | Do nothing       | 0       | 0.0 |
| J1 | CRACK_SEAL       | 20 000  | 3.0 |
| J1 | MICROSURFACING   | 160 000 | 11.0|
| J1 | THIN_OVERLAY     | 320 000 | 15.0|
| J2 | Do nothing       | 0       | 0.0 |
| J2 | THICK_OVERLAY    | 240 000 | 9.0 |
| J2 | RECONSTRUCT      | 700 000 | 15.5|
| J3 | Do nothing       | 0       | 0.0 |
| J3 | CRACK_SEAL       | 40 000  | 2.5 |
| J3 | MICROSURFACING   | 320 000 | 6.0 |

Annual budget: **$600 000**, `minimum_bc_ratio = 0`.

### Efficiency frontiers

After sorting and pruning dominated points:

- **J1**: `(0, 0) → (20k, 3.0) → (160k, 11.0) → (320k, 15.0)` — no dominations to drop.
- **J2**: `(0, 0) → (240k, 9.0) → (700k, 15.5)` — also clean.
- **J3**: `(0, 0) → (40k, 2.5) → (320k, 6.0)` — clean.

### Incremental ratios

```
J1:  IBC_1 = 3.0 / 20 000         = 0.000150   ← best step for J1
     IBC_2 = (11.0 - 3.0) / 140k  = 0.0000571
     IBC_3 = (15.0 - 11.0) / 160k = 0.0000250
J2:  IBC_1 = 9.0 / 240 000        = 0.0000375
     IBC_2 = (15.5 - 9.0) / 460k  = 0.0000141
J3:  IBC_1 = 2.5 / 40 000         = 0.0000625
     IBC_2 = (6.0 - 2.5) / 280k   = 0.0000125
```

(The units are benefit per dollar — tiny numbers, which is why we care about *relative* ordering, not absolute magnitudes.)

### Selection loop

| Iteration | Best candidate | Decision | Remaining budget |
|-----------|----------------|----------|-----------------:|
| 1 | J1 upgrade to CRACK_SEAL (IBC = 0.000150, cost = 20k) | Take it | 580 000 |
| 2 | J3 upgrade to CRACK_SEAL (IBC = 0.0000625, cost = 40k) | Take it | 540 000 |
| 3 | J1 upgrade to MICROSURFACING (IBC = 0.0000571, cost = 140k) | Take it | 400 000 |
| 4 | J2 upgrade to THICK_OVERLAY (IBC = 0.0000375, cost = 240k) | Take it | 160 000 |
| 5 | J1 upgrade to THIN_OVERLAY (IBC = 0.0000250, cost = 160k) | Take it | 0 |
| 6 | Nothing fits (the cheapest remaining step is J3→MICROSURFACING at 280k > 0 remaining) | Stop |

**Final selection:**

- J1 → THIN_OVERLAY (cumulative cost $320k, cumulative benefit 15.0)
- J2 → THICK_OVERLAY (cost $240k, benefit 9.0)
- J3 → CRACK_SEAL (cost $40k, benefit 2.5)

**Totals:** cost = $600 000 exactly, benefit = 26.5.

Notice that the engine ended up choosing the *top* treatment for J1 even though each incremental upgrade beyond MICROSURFACING had a lower IBC than the first J2 upgrade — the algorithm kept coming back to J1 across iterations and upgrading it one step at a time, and the J2 upgrade was eventually picked because it became affordable. That's the key to IBC: we don't commit to a joint's treatment up front; we keep revisiting every joint's next marginal step until the budget runs out.

### What `minimum_bc_ratio` would do

If we set `minimum_bc_ratio = 0.00004`, the last two steps (J1 THIN_OVERLAY at 0.0000250 and J2 THICK_OVERLAY at 0.0000375) would fail the filter:

- J1 would stay at MICROSURFACING ($160k).
- J2 would stay at do-nothing.
- J3 would stay at CRACK_SEAL ($40k).

Total spent: $200 000 of the $600 000 budget, benefit 13.5. **$400 000 left on the table.** With carryover on, that $400 000 rolls forward to next year. Without carryover, it's lost — which is exactly the point of the minimum B/C filter when you're fine with leaving money unspent.

---

## 11. Code map

| Topic | File | Function / line |
|-------|------|-----------------|
| Build efficiency frontier | `engine/optimization/ibc.py` | `build_efficiency_frontier()` 150–203 |
| Compute incremental ratios | `engine/optimization/ibc.py` | `compute_incremental_bc_ratios()` 206–258 |
| Find best next option | `engine/optimization/ibc.py` | `_find_best_incremental_option()` 261–301 |
| Run selection loop (in-memory) | `engine/optimization/ibc.py` | `run_ibc_optimization()` 304–434 |
| Run selection loop (chunked) | `engine/optimization/chunked.py` | `run_ibc_optimization_chunked()` 1506 |
| Frontier build (Polars-optimized) | `engine/optimization/ibc.py` | 644–725 |
| Per-year strategy preparation | `engine/optimization/chunked.py` | `prepare_strategies_chunked()` 551 |
| Joint aggregation | `engine/optimization/work_program.py` | `aggregate_segments_to_joints()` 627+ |
| Segment expansion of selected joints | `engine/optimization/work_program.py` | `expand_joint_selections_to_segments()` 770–789 |
| Apply treatment resets | `engine/optimization/work_program.py` | `_apply_treatment_resets_polars()` 223 |
| Advance deterioration | `engine/optimization/work_program.py` | `_advance_deterioration_polars()` 373 |
| Network GFP calculation | `engine/optimization/work_program.py` | `_calculate_network_gfp()` 97 |
| Same-treatment interval | `engine/treatments/triggers.py` | `_gate_exprs()` (`interval_years`) |
| Budget carryover | `engine/optimization/work_program.py` | 938–995 |
| Benefit AUC integration | `engine/benefits/auc.py` | 179–270 (+ trapezoidal helper 66–87) |
| Traffic weighting | `engine/benefits/weighting.py` | 54–82 (weight) / 85–144 (full formula) / 268–350 (vectorized) |
| Top-level orchestrator | `engine/optimization/chunked.py` | `generate_work_program_chunked()` 1063 |
| Yearly planner | `engine/optimization/chunked.py` | `_plan_rolling_window()` — forces the year's commitments, then one IBC pass; errors fail the run |
| Pricing | `engine/optimization/cost.py` | `price_segments()` / `price_joint_candidates()` — the one cost function |

---

## 12. Look-ahead (removed in v1.7)

Until v1.7 a `lookahead_years` setting planned a window of *k* years at each outer year on a projected copy of the network and kept only the first year's selections. The 2026-09-25 implementation review showed it could not improve the first decision: the first year was chosen before the later years were simulated, and nothing fed back into it, so the window only added work. The greedy optimizer is now plainly **yearly**: each year forces its committed projects and runs one IBC pass over every eligible candidate. The `lookahead_years` field is still accepted (older clients, "New Run from Config") and ignored. Multi-year selection with real feedback is what MILP-assist does (§13).

---

## 13. dTIMS condition model and candidates (v1.6)

From v1.6 the frontiers are built on the dTIMS model (`engine/condition/dtims_state.py`; PMS Business Logic §§ 2–5):

- **Candidates:** every treatment whose trigger branch and gates pass on a joint becomes an alternative on its frontier (the old "one dominant treatment per joint" pick is gone). Gates: pavement per segment and joint, index and CCI windows, counters, years since a listed treatment, route class / I-68, modeled ADT, lanes, committed-only, the wait after any treatment, the treatment's interval and `treatment_sequencing` (now passed by every run).
- **Benefit:** discounted (4%), trapezoid-integrated CCI gain of treating now vs doing nothing, both simulated with the treatment's ordered reset operations, new family and re-anchoring; weighted by length × AADT^0.2 (the config's `adt_exponent`).
- **Benefit weighting (v1.7):** each year's gain is weighted by that year's modeled ADT^p and by length, summed over the joint's segments (the run spec's discount, integration and ADT exponent).
- **Cost (v1.7):** the one pricing function — each member segment at its own pavement's rate (BC, RC, OT), × the cost adjustments of its route groups (thick overlay × 1.2 on `INTERSTATE`), × lanes (the config's default where unknown) × (1 + inflation)^(year − 1), summed to the joint. Greedy, MILP-assist, commitments, Validate and the project / segment pages all use it.
- **Timing:** program year 1 is the starting state; each later year deteriorates first, then selection, then treatments; the year's condition is reported after them.
- **Targets:** % Good / % Poor are the MAP-21 rating of raw IRI, cracking and rutting / faulting, as shares of lane-miles — in the target-chasing loop, the constraint report and MILP-assist's rows (whose precompute uses the same model and timing).
- **MILP-assist (v1.7):**
  - *Candidates:* a (joint, treatment, year) candidate exists only when the treatment passes the trigger evaluation (gates, pavement match, sequencing) on the joint's no-treatment state in that year; a committed joint takes exactly one of its committed candidates (the commitment, or with two actions the commitment and a second treatment after it); committed work that alone exceeds a year's budget fails the run with the list.
  - *Effects:* for every candidate and every measured year, the signed change it makes to network lane-miles Poor and Good in that year (zero before it is applied; negative when it makes a segment worse), against a whole-network do-nothing baseline (segments without a joint included).
  - *Rows:* the Poor ceiling in the Poor target year and the Good floor in the Good target year, each in its own year, always emitted, with signed coefficients.
  - *Every year* (`network_target.every_year`): one Poor row and one Good row per year from 1 to the target year; the benefit sums Poor avoided and Good gained over those years.
  - *Phases (feasibility separate from benefit):* (1) feasibility — all target rows hard, zero objective; (2) if feasible, the rows stay hard and benefit is maximised from that plan; (3) otherwise each row gets a binary "met" variable z (`Target(indicator=True)`: Σ coef·x − M·z ≥ required − M, with M the most the row's activity can fall short) and the solver maximises the number of Poor rows met, then — with `count_mins={"poor": n}` — the number of Good rows met, then benefit with both counts (`build_milp_model(benefit_weight=…, count_mins=…)`). Each phase starts from the previous plan (`solve_milp(start=…)`).
  - *Even spending* (`milp_min_year_share`, `milp_min_year_spend`): `build_milp_model(spend_floors=…, min_share_of_peak=…, spend_years=…)` gives each program year a lower bound on its budget row and, for the share, one continuous peak variable P (last) with rows spend[y] − P ≤ 0 and spend[y] − share·P ≥ 0; warm starts set P to the start plan's biggest year. With the share set, `run_milp_assist` first solves without the rule (5 % gap), then seeds a plan from a band (every year between share·P₀ and P₀; P₀ from that plan's fastest pace to date and its average year, then searched) and solves the rule's model from it; the config's `milp_min_year_share` is the default. `extra_rows` (studies only) appends any `(coefficients, lower, upper, label)` rows in every phase.
  - *Minimum cost* (`network_target.milp_objective = "min_cost"`): phase 2 and the last step of phase 3 maximise `neg_cost_m` (−cost / 1e6, so HiGHS works in $M) instead of benefit (`build_milp_model(objective_column=…)`). A year with budget ≤ 0 gets `budget = inf` and no budget row; its cost is reported as its budget and in `milp_assist.annual_need`. Positive budgets stay ceilings.
  - *Progress:* `solve_milp(on_progress=…)` subscribes to HiGHS's improving-solution and interrupt callbacks: each event carries the best objective, the bound, the gap and nodes, and the pipeline adds the plan's yearly shortfalls; events go to the progress tracker and run log and are stored in `milp_assist.solver_trace`, per-phase summaries in `milp_assist.phases`.
  - *Verification:* the plan is replayed through the simulator; every row's predicted and achieved share is reported (`milp_assist.target_rows`), and "satisfied" comes from the replay only.

## 14. Soft constraints

Greedy IBC has well-known weaknesses (laid out in the companion [Other Optimization Strategies](WVDOT_PMS_Other_Optimization_Strategies.md) doc): no district equity, no network targets, no treatment-mix control, no route priority, no contract bundling. The constraint system layered on top of the engine in 2026-Q2 fixes the *soft* version of all of these without touching the core greedy algorithm. Hard guarantees are still out of scope — that requires MILP or Lagrangian, both of which are research tracks.

### Constraint types

Six constraint families, each opt-in via a sub-object on `analysis_runs.configuration["constraints"]` (JSONB). The pydantic schema lives in `api/schemas/constraints.py`:

| Constraint | Enforcement | Where it lives in the engine |
|---|---|---|
| **Treatment caps** (`max N selections of treatment X per year`) | Hard quota inside the heap loop | `engine/optimization/constraints.py:check_selection_quotas` |
| **District ceilings** (`spend in district D ≤ X% of annual budget`) | Hard quota inside the heap loop | `engine/optimization/constraints.py:check_selection_quotas` |
| **District floors** (`spend in district D ≥ X% of annual budget`) | Soft boost on under-floor districts via `apply_benefit_adjustments_polars` | Pre-IBC, per chunk |
| **Treatment mix floors** (`spend on category C ≥ X% of total`) | Soft boost on under-floor categories | Pre-IBC, per chunk |
| **Route priority / NHS boost** (multipliers on weighted_benefit) | Multiplicative boost in `apply_benefit_adjustments_polars` | Pre-IBC, per chunk |
| **Network % Good target** (`pct_good ≥ T% by year Y`) | Outer-loop target chasing — re-runs the engine with an increasing rehab/recon boost until the target is met or `max_iterations` is reached | `engine/optimization/constrained_work_program.py:generate_constrained_work_program` |
| **Bundling bonus** (adjacent joints same year get a bonus) | Reported diagnostically only; v2 will enforce inside the heap loop | `engine/optimization/constraints.py:check_constraint_satisfaction` |

### Per-constraint reference

Every constraint is opt-in. Setting `enabled = false` (or omitting the sub-object entirely) is a no-op — a run with no enabled constraints is bit-identical to a run with `constraints = None`. The same is true of an `enabled = true` constraint with no bands/caps/floors populated: the enforcement loop has nothing to check and short-circuits. See `tests/test_constrained_runs.py::TestBackwardCompat::test_three_unconstrained_forms_are_bit_identical` for the gate.

All examples below are JSONB excerpts that go inside `analysis_runs.configuration.constraints`. The frontend builds the same shape from `ui/src/components/ConstraintsSection.tsx`.

#### 14.1 District balancing — per-district budget bands

**Purpose.** Prevent any one district from hogging the budget and (softly) nudge under-served districts to get a fair share. Districts are identified by `district_code`; the engine reads per-candidate `district_code` off `analysis_segments`.

**Schema** (`DistrictBalancing` in `api/schemas/constraints.py`):

```json
{
  "district_balancing": {
    "enabled": true,
    "penalty_weight": 1.0,
    "bands": [
      { "district_code": 1,  "floor_pct": 0.08, "ceiling_pct": 0.12 },
      { "district_code": 2,  "floor_pct": 0.08, "ceiling_pct": 0.12 },
      …
    ]
  }
}
```

| Field | Type | Default | Meaning |
|---|---|---|---|
| `enabled` | bool | `false` | Master switch. When false the whole sub-object is ignored. |
| `penalty_weight` | float ≥ 0 | `1.0` | How aggressively under-floor districts get boosted (see math below). |
| `bands` | list of `DistrictBudgetBand` | `[]` | One entry per district the user wants to constrain. Districts *not* in `bands` have no floor and no ceiling. |
| `bands[].district_code` | int | — | WVDOT district code (1–10 for the WV network). |
| `bands[].floor_pct` | float in `[0, 1]` or `null` | `null` | Minimum fraction of the *annual* budget to spend in this district. `null` = no floor for this district. |
| `bands[].ceiling_pct` | float in `[0, 1]` or `null` | `null` | Maximum fraction of the *annual* budget. `null` = no ceiling. |

**Validation.** Across the run, `sum(floor_pct)` must be ≤ 1.0 (otherwise the floors mathematically can't all be satisfied); a model validator enforces this at submit time. For any single band, `floor_pct ≤ ceiling_pct` if both are set.

**How the engine uses it.**

- **Ceilings (hard, per-year).** `initialize_quota_state` pre-computes `ceiling_dollars = ceiling_pct × annual_budget` for each banded district at the start of every year. Inside the heap loop, `check_selection_quotas` vetoes any candidate whose incremental cost would push `district_spent[d] + cost` above that ceiling — the candidate is dropped from the heap and the loop moves on. O(1) overhead per selection check.
- **Floors (soft, pooled over the horizon).** `check_constraint_satisfaction` runs after each multi-year pass, aggregates total spend per district, and compares each band's `floor_pct × annual_budget × analysis_years` against actual spend. Under-floor districts get a multiplicative boost on their candidates' `weighted_benefit` on the *next* outer iteration via `apply_benefit_adjustments_polars`. Floors are therefore only effective when combined with `network_target` (which has its own outer loop) OR when the user re-runs after seeing the constraint report. A single-pass constrained run with only floors configured will fail the floor check visibly in the report but won't fix itself.

**When to use.** Any run where district equity matters more than pure network B/C. Typical setup: every district gets an equal-share band with a 2–5% tolerance (computed via the UI's *Tolerance ±%* control, which auto-fills every checked row with `{ floor: 1/n × (1-tol), ceiling: 1/n × (1+tol) }`).

**Gotchas.**

- **Unchecked districts are FILTERED OUT of the network entirely.** The UI treats an unchecked district as "not in bands", and the engine's segment loader ANDs `district_code IN (...)` into the WHERE clause at run time using the union of banded district codes. A run with District Balancing enabled but only 3 districts checked will only see segments from those 3 districts. See `api/routes/runs.py` lines 458–475 where this injection happens.
- **Ceilings are per YEAR, floors are pooled over the HORIZON.** This asymmetry is not a bug — it's deliberate. A per-year floor would force bad spending in districts with no good candidates that year; pooling lets under-served districts catch up in later years. But the UI shows both as percentages and some users miss the distinction.
- **`penalty_weight` only affects floors, not ceilings.** Ceilings are hard and don't need a weight.

---

#### 14.2 Network condition target — soft `pct_good` target

**Purpose.** "Get the network to X% Good by year Y." Used when condition outcomes matter more than raw B/C efficiency — a network in terrible shape often needs rehab/recon heavily weighted to recover.

**Schema** (`NetworkTarget`):

```json
{
  "network_target": {
    "enabled": true,
    "target_pct_good": 75,
    "target_year": 10,
    "max_iterations": 8,
    "damping": 0.5
  }
}
```

| Field | Type | Default | Meaning |
|---|---|---|---|
| `enabled` | bool | `false` | Master switch. |
| `target_pct_good` | float `[0, 100]` | — (required) | Network-wide % Good target. The network's ending `pct_good` at `target_year` must land within 0.5 pp of this. |
| `target_year` | int ≥ 1 | — (required) | Program year to evaluate the target at. Typically the final analysis year. |
| `max_iterations` | int `[1, 20]` | `8` | Hard ceiling on outer-loop retries. The loop always terminates. |
| `damping` | float `[0.1, 1.0]` | `0.5` | Shrinks each iteration's boost update so the loop doesn't oscillate. 1.0 = aggressive (can overshoot), 0.1 = slow and steady. |

**How the engine uses it.** This is the ONLY constraint that triggers the target-chasing outer loop in `constrained_work_program.py:generate_constrained_work_program`. Every other constraint takes a single-pass call path.

Each iteration:

1. Run the full yearly greedy engine with the current `network_target_boost` (starts at 1.0).
2. Read `pct_good` at `target_year` from `condition_trajectory`.
3. Compute `shortfall_pp = target_pct_good − achieved`.
4. If `shortfall_pp ≤ 0.5` → break, success.
5. Otherwise apply a damped multiplicative update: `boost ← boost × (1 + damping × shortfall_pp / 100)` and re-run.

The boost is applied *only* to candidates whose `budget_category` is `rehabilitation` or `reconstruction` inside `apply_benefit_adjustments_polars`. Boosting preservation doesn't help close a target gap — preservation holds the line but rarely flips Fair/Poor segments to Good in the WVDOT family curves. The loop also tracks the best (highest `pct_good`) result across iterations, so even an infeasible target returns a usable plan.

**When to use.** Policy-driven runs ("the legislature mandates 75% Good by 2030"). Pair with `district_balancing` when equity also matters — the target-chasing loop will respect district ceilings while iterating.

**Gotchas.**

- **Infeasible targets don't fail the run.** If the budget genuinely can't achieve the target, the loop exhausts its iterations and returns the best it got. The report flags this as `severity = "warning"` so the user can see it missed.
- **Each iteration is a full engine run.** Setting `max_iterations = 20` on a 20-year 500k-segment run will take ~20× the engine runtime. 8 is the default because most feasible targets converge in 3–5 iterations.
- **Progress bar appears to restart.** Each iteration owns a sub-window of the parent `ProgressTracker` via `NestedProgressTracker` (`engine/progress.py`), so the bar advances monotonically 0→12.5%→25%→… across 8 iterations rather than resetting to 0 each time.

---

#### 14.3 Treatment caps — hard per-year per-treatment ceiling

**Purpose.** Cap how many times the optimizer can select a specific treatment in a single program year. Used for hard limits driven by operational reality: "we only have crews to lay crack seal on 200 joints a year", "there are only 3 contractors certified for mill-and-overlay in this district".

**Schema** (`TreatmentCaps`):

```json
{
  "treatment_caps": {
    "enabled": true,
    "caps": [
      { "treatment_id": "CRACK_SEAL",     "max_per_year": 200 },
      { "treatment_id": "MILL_OVERLAY_2", "max_per_year": 40  }
    ]
  }
}
```

| Field | Type | Default | Meaning |
|---|---|---|---|
| `enabled` | bool | `false` | Master switch. |
| `caps` | list of `TreatmentCap` | `[]` | One entry per capped treatment. Treatments *not* in the list are uncapped. |
| `caps[].treatment_id` | str | — | Must match a `treatments.treatment_id` value. |
| `caps[].max_per_year` | int ≥ 0 | — | Maximum number of selections per program year. 0 effectively disables the treatment. |

**How the engine uses it.** At the start of every program year, `initialize_quota_state` populates `treatment_slots[treatment_id] = max_per_year` for each capped treatment. The heap loop calls `check_selection_quotas` before each selection; if `treatment_slots[tid] <= 0`, the candidate is vetoed and the next B/C ranking is tried instead. O(1) dict lookup.

The cap is independent of budget — a capped treatment can still be selected up to its cap regardless of how much budget remains, and uncapped treatments continue to compete for budget normally.

**When to use.** Crew/contractor/materials availability constraints. Also useful for research studies: "what's the plan if we can only do 100 reconstructions over 20 years?".

**Gotchas.**

- **Caps are PER YEAR, not total.** A cap of 40 mill-and-overlays means 40 per year, up to 800 over a 20-year horizon. There's no cumulative cap today.
- **A treatment with no cap entry is UNLIMITED.** Not capping it is not the same as setting it to 0.
- **Vetoed candidates don't get re-pushed.** Once a joint is rejected at a given treatment level due to a cap, it stays out of the heap for this year. The optimizer won't try a lower-cost alternative on the same joint — it moves on to the next-best joint.

---

#### 14.4 Treatment mix floors — minimum % of spend per budget category

**Purpose.** Force a minimum share of annual spend into each budget category (`preservation`, `rehabilitation`, `reconstruction`). Prevents the optimizer from collapsing into "only preservation" (cheap B/C wins) or "only reconstruction" (high benefit per segment) — both failure modes of pure IBC on bimodal networks.

**Schema** (`TreatmentMixFloors`):

```json
{
  "treatment_mix_floors": {
    "enabled": true,
    "floors": [
      { "budget_category": "preservation",   "min_pct_of_spend": 0.30 },
      { "budget_category": "rehabilitation", "min_pct_of_spend": 0.40 },
      { "budget_category": "reconstruction", "min_pct_of_spend": 0.10 }
    ],
    "boost_strength": 1.5
  }
}
```

| Field | Type | Default | Meaning |
|---|---|---|---|
| `enabled` | bool | `false` | Master switch. |
| `floors` | list of `TreatmentMixFloor` | `[]` | One entry per budget category with a floor. Categories not listed have no floor. |
| `floors[].budget_category` | `"preservation" \| "rehabilitation" \| "reconstruction"` | — | Case-normalized to lowercase inside the engine. |
| `floors[].min_pct_of_spend` | float in `[0, 1]` | — | Minimum fraction of total spend that must go to this category. |
| `boost_strength` | float in `[1.0, 5.0]` | `1.5` | How aggressively under-floor categories get their `weighted_benefit` boosted. |

**Validation.** `sum(min_pct_of_spend)` must be ≤ 1.0 — otherwise the floors can't coexist.

**How the engine uses it.** Soft constraint, evaluated via the constraint report after each pass: any category with `achieved_pct_of_spend < min_pct_of_spend` gets a `boost_strength×` multiplier on all its candidates' `weighted_benefit` on the *next* iteration. The boost is applied in `apply_benefit_adjustments_polars` via a `budget_category == ...` polars expression. Like district floors, this is effective when paired with `network_target`'s outer loop; in a single-pass run the user sees the violation in the report but the engine doesn't self-correct.

**When to use.** Rehab-heavy networks where preservation would starve without a floor. Also useful for policy runs: "we've committed to spending 10% on reconstruction annually".

**Gotchas.**

- **The engine reports achieved mix as a % of total *cost*, not count.** A hundred $10k crack seals ($1M total) count less toward the preservation floor than five $200k mill-and-overlays ($1M in rehabilitation).
- **`boost_strength = 1.0` disables the boost while keeping the floor tracked.** Useful for "measure the mix but don't actively enforce it".
- **Categories are read from `treatments.budget_category`.** If your treatments table has a treatment with a blank or non-standard category, it won't contribute to any floor — audit the table with `SELECT budget_category, COUNT(*) FROM treatments GROUP BY 1;` before enabling this.

---

#### 14.5 Route priority — NHS / functional class / explicit route boosts

**Purpose.** Give preferential weight to important routes without hard-capping anything else. All boosts are multiplicative and compound.

**Schema** (`RoutePriority`):

```json
{
  "route_priority": {
    "enabled": true,
    "nhs_multiplier": 1.25,
    "functional_class_multipliers": {
      "1": 1.30,
      "11": 1.30,
      "2": 1.15
    },
    "priority_route_ids": ["I77", "I79", "US50"],
    "route_multiplier": 1.50
  }
}
```

| Field | Type | Default | Meaning |
|---|---|---|---|
| `enabled` | bool | `false` | Master switch. |
| `nhs_multiplier` | float in `[1.0, 5.0]` | `1.25` | Applied to every candidate where `nhs_code > 0`. |
| `functional_class_multipliers` | `Dict[int, float]` | `{}` | Sparse mapping: only listed functional classes get a multiplier. Missing classes = 1.0 (no change). Typical use: classes 1 (rural interstate) + 11 (urban interstate). |
| `priority_route_ids` | `List[str]` | `[]` | Explicit allow-list of `route_id` values that get an extra boost. |
| `route_multiplier` | float in `[1.0, 5.0]` | `1.25` | Applied to every candidate in `priority_route_ids`. |

**How the engine uses it.** Pure multiplicative boost on `weighted_benefit`, applied inside `apply_benefit_adjustments_polars` before the heap is built. A segment on I-77 (NHS, functional_class 1, in `priority_route_ids`) gets:

```
weighted_benefit' = weighted_benefit × nhs_multiplier × fc_multiplier[1] × route_multiplier
                  = weighted_benefit × 1.25 × 1.30 × 1.50
                  = weighted_benefit × 2.44
```

All multipliers default to 1.0 when the field is absent, so partial configuration is safe.

**When to use.** Any run where the user has political or policy reasons to favor certain routes. Also useful as a "soft" way to steer toward strategic corridors without filtering others out entirely.

**Gotchas.**

- **Multipliers COMPOUND.** A segment matching all three boosts at default settings gets a 2.44× weighted_benefit. Users asking "why is I-77 getting so much spend" usually haven't noticed this.
- **NHS boost only fires when `nhs_code > 0`.** `nhs_code` can be `NULL` in the WV data; nulls are treated as non-NHS.
- **`priority_route_ids` is case-sensitive.** The underlying `analysis_segments.route_id` is upper-cased already in the WV data, so use `"I77"` not `"i77"`.
- **Route priority does NOT change district or budget constraints.** It only changes the ordering the heap sees.

---

#### 14.6 Bundling bonus — adjacency boost (diagnostic only today)

**Purpose.** Encourage contiguous selections — if a joint's MP neighbors on the same route are already being treated this year, give the neighbor a benefit bonus so it tends to join the same contract bundle.

**Schema** (`BundlingBonus`):

```json
{
  "bundling_bonus": {
    "enabled": true,
    "bonus": 0.10,
    "neighbor_window": 1
  }
}
```

| Field | Type | Default | Meaning |
|---|---|---|---|
| `enabled` | bool | `false` | Master switch. |
| `bonus` | float in `[0, 1]` | `0.10` | Multiplicative bonus on `weighted_benefit` per adjacent neighbor already selected this year. |
| `neighbor_window` | int in `[1, 5]` | `1` | How many MP-adjacent joints on each side to consider. |

**How the engine uses it.** **Current status: diagnostic only.** As of the 2026-Q2 shipping branch, `check_constraint_satisfaction` walks the final selections and counts adjacent pairs, writing the count into the constraint report as `adjacent_pairs_observed`. The actual boost is not applied inside the heap loop yet — doing so correctly requires a per-year adjacency map that updates as selections are made, since adjacency depends on *what's already been selected*. That change is tracked in the engine TODO list.

**When to use.** Turn it on to measure how much natural bundling the optimizer already produces. The diagnostic value is useful even without enforcement: runs that show high `adjacent_pairs_observed` organically are good candidates for contract-bundled procurement without any intervention.

**Gotchas.**

- **The boost is not actually applied yet.** Runs with `bundling_bonus.enabled = true` behave identically to runs without it, aside from the extra post-run report field. Don't rely on it to actually shape selections.
- **"Adjacency" is defined by MP proximity on the same route_id, not by joint ID.** Joints from different routes that happen to be near each other geometrically don't count as adjacent.
- **`neighbor_window > 1` means "this joint plus its two/three/… neighbors on each side count as bundled".** At `neighbor_window = 3` a single joint can be boosted by up to 6 neighbors × `bonus`.

---

### Where each piece plugs in

The constraint system is **fully additive**. The core greedy heap loop in `engine/optimization/chunked.py:run_ibc_optimization_chunked` is unchanged except for two new branches gated on `quota_state is not None`:

1. After the affordability check, `check_selection_quotas` is called. A vetoed candidate is dropped from the heap (the segment is *not* re-pushed at the next level) and the loop moves on. Worst case the joint gets treated next year. The quota check is O(1) — three dict lookups and one comparison — so the overhead on a 500k-iteration WV run is well under 150 ms.
2. After a successful selection, `update_quota_state` decrements counters.

When `quota_state is None` (the normal unconstrained path) both branches short-circuit on their first line and the loop is bit-identical to the pre-constraint engine. This is locked in by the integration test `tests/test_constrained_runs.py::TestBackwardCompat::test_three_unconstrained_forms_are_bit_identical`, which compares three forms — no `constraints` key, `constraints=None`, and an empty `ConstraintsConfig()` — against each other. All three must produce identical `total_cost` and `segments_treated`. **This test must pass on every CI run.**

### Pre-IBC benefit adjustments

`apply_benefit_adjustments_polars` is called inside `_plan_rolling_window`, between `prepare_strategies_chunked` and `run_ibc_optimization_chunked`, on each strategy chunk. It's a pure function — given a strategies DataFrame and the current boost dictionaries, it returns a new DataFrame with `weighted_benefit` adjusted by the configured multipliers. The multipliers compound, so a segment that's both NHS *and* in a priority-route allow-list gets `weighted_benefit × nhs_multiplier × route_multiplier`.

Each adjustment is gated on the relevant sub-constraint being enabled. When everything is disabled, the function returns the input unchanged.

### Target-chasing outer loop

`generate_constrained_work_program` wraps `generate_work_program_chunked` in a retry loop *only* when `network_target.enabled = True`. Other constrained runs (caps, floors, route priority, etc.) take a single-pass path that calls the engine exactly once with the constraints attached.

For target-chasing runs, each iteration:

1. Calls `generate_work_program_chunked` with the current `network_target_boost` (starts at 1.0).
2. Reads the achieved `pct_good` for the target year from the resulting `condition_trajectory`.
3. If within 0.5 pp of the target → break, success.
4. Else compute `boost' = boost × (1 + damping × shortfall_pp / 100)` and re-run.
5. Track the best (highest pct_good) result across iterations and return that, even if no iteration hit the target. This guarantees the user always gets a usable plan.

`max_iterations` is 8 by default and capped at 20. Damping is 0.5 by default. Both are configurable per run. The boost is applied only to candidates whose `budget_category` is `rehabilitation` or `reconstruction` — those are the categories whose resets actually flip Fair/Poor segments to Good in the WVDOT family curves. Boosting preservation treatments wouldn't help close a target gap.

Progress reporting is nested: each outer-loop iteration owns a sub-window of the parent `ProgressTracker` via `NestedProgressTracker` (in `engine/progress.py`), so the global progress bar advances monotonically across the loop instead of resetting to 0 each iteration.

### Constraint report

After every constrained run, `check_constraint_satisfaction` builds a `ConstraintReport` and attaches it to `WorkProgramResult.constraint_report` (None for unconstrained runs). The API layer copies this into `analysis_runs.result_summary["constraint_report"]` and exposes it on `RunConfigurationResponse.constraint_report`. The frontend renders it on the Run Detail page's Overview, Trajectory, and Treatments tabs.

The report has one sub-key per constraint family with achieved-vs-target metrics:

- **treatment_caps**: per-cap `max_observed`, `satisfied`
- **district_balancing**: per-band `spent_dollars`, `spent_pct`, `floor_met`, `ceiling_met`
- **network_target**: `achieved_pct_good`, `shortfall_pp`, `satisfied`, plus an `iterations` array showing the per-iteration boost history from the target-chasing loop
- **treatment_mix_floors**: per-floor `achieved_pct_of_spend`, `satisfied`
- **route_priority**: spend distribution across NHS / priority routes (diagnostic only, no satisfaction concept)
- **bundling_bonus**: `adjacent_pairs_observed` (diagnostic only)

Severity is bumped to `warning` when a soft constraint misses (district floor, network target, treatment mix floor) and `violation` when a hard constraint fails (treatment cap, district ceiling — these *should* never violate because they're enforced in the heap loop, but the report catches it if something breaks upstream).

### See also

- `api/schemas/constraints.py` — full pydantic schema
- `engine/optimization/constraints.py` — quota state, benefit adjustments, satisfaction reporting
- `engine/optimization/constrained_work_program.py` — target-chasing outer loop
- `tests/test_constraints.py` — unit tests for the pure functions
- `tests/test_constrained_runs.py` — end-to-end integration tests + the bit-identical backward-compat gate
- [Other Optimization Strategies](WVDOT_PMS_Other_Optimization_Strategies.md) — design rationale for going with soft constraints over MILP/Lagrangian
