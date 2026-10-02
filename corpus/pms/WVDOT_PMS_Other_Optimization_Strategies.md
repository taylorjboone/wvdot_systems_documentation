# WVDOT PMS — Other Optimization Strategies

> The WVDOT PMS engine uses a **greedy Incremental Benefit-Cost (IBC)** optimizer. That choice is a practical one — it's fast, it's easy to explain, it scales to the WV state system in single-digit seconds — but it has well-understood limitations, and the pavement-management literature has several alternatives ranging from "small tweak" to "full research project". This doc lays out **what's wrong with greedy IBC, what else you could use, and which upgrade is worth shipping next**.

If you're here because you want to understand *why* the current engine makes the choices it makes, start with the [Optimization Logic doc](WVDOT_PMS_Optimization_Logic.md). That one explains the IBC algorithm itself. This doc is its honest companion — a critique plus a menu of alternatives.

---

## Table of Contents

1. [Downfalls of greedy IBC](#1-downfalls-of-greedy-ibc)
2. [Alternative approaches](#2-alternative-approaches)
   - [A. Rolling-horizon / receding-horizon (MPC)](#a-rolling-horizon--receding-horizon-mpc)
   - [B. Mixed-integer linear programming (MILP)](#b-mixed-integer-linear-programming-milp)
   - [C. Lagrangian relaxation](#c-lagrangian-relaxation-of-the-budget-constraint)
   - [D. Markov Decision Processes (MDPs)](#d-markov-decision-processes-mdps)
   - [E. Simulation-optimization + scenario analysis](#e-simulation-optimization--scenario-analysis)
   - [F. Two-stage stochastic programming](#f-two-stage-stochastic-programming)
   - [G. Metaheuristics — GA / simulated annealing](#g-metaheuristics--genetic-algorithms--simulated-annealing)
   - [H. Per-segment life-cycle cost analysis (LCCA)](#h-life-cycle-cost-analysis-lcca-per-segment-then-budget-sort)
3. [Recommendations for this codebase](#3-recommendations-for-this-codebase)
4. [What we're actually shipping first](#4-what-were-actually-shipping-first)

---

## 1. Downfalls of greedy IBC

This list is in descending order of how much the current algorithm's pathologies hurt the WVDOT PMS in practice.

### 1.1. It's myopic — the year-by-year loop has no look-ahead

This is by far the biggest one. Each year the optimizer solves a *single-year* problem: "given this year's budget and today's condition, pick the best projects right now". It never asks "would I be better off **skipping** this cheap preservation and saving for a thick overlay in year 3?"

Concretely: a joint with CCI=3.6 today might look like a screaming deal for microsurfacing at a high B/C ratio. But that same joint, left alone for 2 years, would drop to CCI=2.9 and become eligible for a *thin overlay* that has 5× the lifetime benefit. The current engine has no way to "hold" the cheaper option in reserve and wait for the better-ROI window to open. It makes a locally optimal choice every year and calls it done.

### 1.2. It's greedy on the efficiency frontier, not optimal on the knapsack

Even within a single year, greedy IBC only provably matches the **LP relaxation** of the budget-constrained knapsack — the fractional solution. The actual problem is 0/1 (you can't do half a joint), and the integrality gap can be meaningful, especially when:

- The budget is small relative to the cheapest high-ROI project (one expensive pick eats the whole budget).
- There are near-tie IBCs between very different cost scales (a $20k crack seal vs a $280k reconstruction).
- The last selection "just barely fits" and excludes a much better combination you could have picked instead.

In the worst case the gap can be O(most expensive project / budget), which for a small-budget scenario is not nothing.

### 1.3. No backtracking

Once a joint is upgraded to MICROSURFACING mid-year, the algorithm never says "actually, given that I later selected J47 for reconstruction, it would have been better to *not* have microsurfaced J12 and use that money on J83 instead". Every decision is final as soon as it's made. This compounds with §1.1: bad early decisions get locked in.

### 1.4. It treats joints as independent

Two adjacent joints on the same route that both want a thick overlay should ideally be let as one contract — mobilization, MOT, and traffic control are cheaper per lane-mile when you do them together. The engine has no notion of **project bundling** or **adjacency bonus**. It sees them as two separate decisions, and if one edges out a different joint 50 miles away on raw IBC, the contract-bundling saving is invisible.

Related: there's no notion of "district equity" or "region balance". All ~3600 joints across all 10 districts compete in one flat heap. Nothing prevents the algorithm from loading 80% of the budget into District 3 three years in a row if that's where the IBCs happen to line up.

### 1.5. Deterministic — no uncertainty modeling

The deterioration curves in `pavement_families` are *point estimates*. Real deterioration has variance — weather, freeze-thaw, truck loading, construction quality all matter, and they're stochastic. The engine's benefit calculation assumes the curves are ground truth. When they're not (and they aren't), the work program is optimal under an unlikely deterministic scenario rather than robust across a distribution of likely futures.

### 1.6. No network-level target constraints

You can't tell the engine "maintain at least 80% Good by year 10" or "get poor pavements below 5% by year 5". You can only nudge it indirectly via `minimum_bc_ratio`, which is a blunt knob — it doesn't know *why* you're raising it. The network GFP comes out as whatever-it-comes-out-as, not as a constraint that shapes the selection.

### 1.7. Single-objective — maximizes weighted benefit only

The objective is `Σ weighted_benefit`. That's it. Real PMS decisions trade off:

- Expected condition
- Safety (skid, rut depth)
- User cost (IRI directly affects vehicle wear)
- Freight corridor priority (coal route, NHS)
- Equity across districts
- Smoothness of the year-over-year spend curve

All of those either get jammed into `power_exponent × AADT^p × length` (crude) or are simply ignored.

### 1.8. Tie-breaking is order-dependent and opaque

From the [Analysis Engine doc](WVDOT_PMS_Analysis_Engine.md): when two `(joint, treatment)` pairs have identical IBC, "the first match wins (order-dependent on the Polars scan order)". That's not a bug per se, but it means the same inputs can give slightly different outputs on a different Polars version or after a column reorder, which makes runs non-reproducible in a subtle way.

### 1.9. The per-year budget is assumed pre-allocated

Carryover is the only flexibility. The engine can't ask "is this a year where we should *underspend* because next year's projects are much better?" — with carryover on it gets that effect *accidentally* when `minimum_bc_ratio` prunes weak picks, but there's no explicit multi-year budget re-balancing.

---

## 2. Alternative approaches

Roughly ordered from "small tweak" to "full research project".

### A. Rolling-horizon / receding-horizon (MPC)

Solve the next **k years** together each year, commit only year 1, then re-optimize with a fresh k-year window in year 2. This is Model Predictive Control applied to PMS. It fixes §1.1 and partially §1.3 without having to rewrite the objective.

Implementation: instead of `for year in 1..Y: optimize(this_year)`, do:

```
for year in 1..Y:
    plan = optimize(years = year..year+k-1)
    commit(plan[year])
    advance_one_year()
```

The inner `optimize` can still be IBC — you just give it a k-year budget and let it distribute projects across the k years with the inter-year `min_interval_years` constraint built in.

**Practical choice**: `k = 3–5` captures the major "wait a year" effects without blowing up the solve time. **This is the cheapest upgrade that fixes the worst behavior**, and it's what this repo is shipping — see [§4](#4-what-were-actually-shipping-first).

### B. Mixed-integer linear programming (MILP)

Formulate the full problem as an integer program and hand it to a solver (HiGHS is open-source and fast, Gurobi/CBC are options):

- **Variables**: `x_{j,t,y} ∈ {0, 1}` = "apply treatment `t` to joint `j` in year `y`"
- **Objective**: `max Σ x_{j,t,y} · weighted_benefit_{j,t,y}`
- **Constraints**:
  - `Σ_{t,y} x_{j,t,y} ≤ 1` for the cooldown window (at most one treatment per joint in any `min_interval_years` window)
  - `Σ_{j,t} x_{j,t,y} · cost_{j,t} ≤ budget_y` for each year
  - Deterioration linearization — harder. You'd typically pre-compute `(j,t,y)` benefit as the AUC under the curves already, and bake the state-dependent benefit into the coefficient. That loses fidelity for "what if I do nothing this year" paths unless you introduce state variables.
  - **Equity** / **target** constraints are natural: `Σ_{j ∈ District_d, t, y} cost ≥ 0.08 × total_budget`, `pct_good_y ≥ 0.80` (as a linear constraint over segment-level indicator variables).

**Advantages**: provably optimal (up to solver gap), arbitrary constraints, multiple objectives via weighted sum or lexicographic ordering.

**Drawbacks**: the variable count is (joints × treatments × years) = ~3.6 K × 14 × 10 ≈ 500 K binaries. HiGHS/CBC will struggle past ~100 K binaries without careful formulation (column generation, valid inequalities, Dantzig-Wolfe). Gurobi can handle it but it's commercial. The **deterioration path is inherently non-linear** — pretending each `(j,t,y)` has a fixed benefit coefficient is an approximation, and modeling the coupling between years correctly requires mixing state variables into the integer program.

### C. Lagrangian relaxation of the budget constraint

Sweet spot between IBC and full MILP. You "soften" the budget constraint by a penalty multiplier `λ`:

```
max Σ (benefit_{j,t} - λ · cost_{j,t})
```

Without the budget constraint, each joint's sub-problem is independent: pick the treatment that maximizes `benefit - λ·cost`. You tune `λ` until the total spend hits the budget. The tuning loop is a 1D bisection; the inner solve is trivially parallel per joint.

**Why it's better than greedy IBC**: at the right `λ`, the per-joint choices are **simultaneously optimal** under a shadow price, rather than being filled in greedy-order. It's still a relaxation, so it doesn't give you 0/1-optimal integer solutions, but it gives you a *dual bound* and a clean parallelization story. It naturally handles equity constraints too (add per-district Lagrangian terms).

### D. Markov Decision Processes (MDPs)

The mathematically "correct" way to model this: each segment (or joint) is a system whose state evolves stochastically based on the treatment you apply and the curve family. The decision problem is to find a **policy** — a mapping from state → action — that maximizes expected discounted reward.

```
V(s) = max_a [ R(s,a) + γ · E[V(s')] ]
```

This is what AASHTOWare Pavement ME and early dTIMS solver versions used. Solved via value iteration or policy iteration.

**Advantages**:

- **Naturally handles uncertainty** — curves become transition probabilities, not deterministic trajectories.
- **Multi-year horizon is baked in** — the value function `V(s)` encodes "how good is this state" over the full future, so picking treatments greedy on `R(s,a) + γV(s')` is automatically forward-looking.
- **Infinite horizon possible** — steady-state policies via discounting.

**Drawbacks**:

- **State space explosion**. Even discretizing each index to 10 buckets gives `10^6` states for a single joint, and the joint doesn't evolve independently once you have a joint-level budget. In practice you solve it per-segment and then layer budgeting on top, which re-introduces the myopia.
- **Budget constraints are awkward** — you have to fold them into the state (remaining budget), which explodes the state space further, or handle them via Lagrangian methods (see C).

### E. Simulation-optimization + scenario analysis

Admit that the deterministic model is wrong and run Monte Carlo:

1. Sample `K` plausible 10-year futures from the family curves' uncertainty distributions.
2. For each future, run the greedy IBC and record the work program + end-state GFP.
3. Look at the *distribution* of outcomes, not a point estimate.

Useful for **robustness checking** existing runs ("does my work program break if deterioration is 20 % faster than expected?"). It doesn't itself pick a better policy, but it tells you how bad the current greedy policy is in expectation vs. worst-case.

Combined with **scenario-specific policies**: run greedy IBC on the pessimistic scenario, the median scenario, and the optimistic scenario, and present all three to decision-makers.

### F. Two-stage stochastic programming

Specialization of E. Solve:

```
max  E[ benefit(x, ω) ]     subject to  budget constraints
```

where `x` is the year-1 decisions (what you commit to *now*) and `ω` is the random future, with year-2+ decisions as recourse variables that depend on the realized `ω`. Lots of papers in the transportation literature do this for PMS. Harder to implement but philosophically closer to what real DOT planners actually want.

### G. Metaheuristics — genetic algorithms / simulated annealing

Represent a work program as a chromosome (a list of `(joint, treatment, year)` tuples), define mutation/crossover, drive toward high total benefit while penalizing budget violations. Handles non-convex objectives and arbitrary constraints (including bundling bonuses, equity) gracefully.

**Drawbacks**: no optimality guarantees, slow to converge on a specific answer, and **hard to explain to an engineering manager** — "the algorithm said so" doesn't sit well with people who have to defend decisions publicly. Usually a last resort when the formulation is too messy for MILP.

### H. Life-cycle cost analysis (LCCA) per segment, then budget-sort

The "bottom-up" approach used by older DOT methods: for each segment independently, compute the **minimum-NPV treatment sequence** over the analysis horizon (a per-segment DP problem — fast). Rank segments by "NPV improvement per dollar committed" and fill the budget by that rank.

This is basically what greedy IBC approximates in one year, but by doing the per-segment DP over the full horizon up front, you get the multi-year look-ahead that IBC lacks. Intermediate between rolling-horizon and full MILP.

---

## 3. Recommendations for this codebase

Ordered by effort ÷ value.

| Option | Effort | Value | Notes |
|---|---|---|---|
| **A. Rolling-horizon (k ≈ 3)** | Low | **High** | Biggest bang for buck. Minimal changes to `generate_work_program_chunked` — call IBC with a k-year window, commit year 1, advance, repeat. Fixes the myopia without touching the core data model. **This is what we're shipping — see below.** |
| **C. Lagrangian budget relaxation** | Low–medium | Medium | Parallelizes cleanly; makes per-joint choices coherent under a shadow price. Would replace `run_ibc_optimization` with an inner "pick best treatment for each joint given λ" + a λ-search outer loop. |
| **E. Monte Carlo scenario suite** | Low | Medium | Doesn't improve the optimizer but improves *trust* in its outputs. Run N=100 scenarios with perturbed curve coefficients, report the distribution in the UI's Run Detail page. Great for sensitivity analysis. |
| **B. Full MILP via HiGHS** | High | High if it scales | WVDOT's 3.6 K joints × 14 treatments × 10 years = ~500 K binaries. HiGHS would likely need column generation or problem decomposition to solve in reasonable time. Best kept as a "research mode" entry point you run occasionally to benchmark how close greedy IBC gets to the LP bound. |
| **D. MDP per segment** | High | Medium | Good academic fit; hard to combine with a network-level budget. Would probably end up reinventing option C on top of it. |

If I had one afternoon to invest, I'd do **A**. The change is structurally tiny — you're just replacing the outer `for year in range(...)` with a rolling-window solve — and it directly addresses the most visible pathology of the current output (early-year preservation that you wish you'd deferred).

If I had one week, I'd add **C** alongside A and compare the two on a WV 10-year run to see how much better the network trajectory is. The engine is already fast enough in Polars that rerunning both variants for every user submission is trivial compared to the `lrsops` pipeline.

And regardless of which optimizer you pick, **E** is worth doing because right now the headline `total_benefit` number in every run has zero uncertainty bars on it, which hides a lot of modeling risk.

---

## 4. What we're actually shipping first

**Rolling-horizon optimization** ([Option A](#a-rolling-horizon--receding-horizon-mpc)) is the first improvement we're putting in the engine. Default `lookahead_years = 3`, configurable in the Create Run dialog, stored in `analysis_runs.configuration` JSONB, and surfaced on the Run Detail Configuration card. When `lookahead_years = 1` the engine produces bit-identical output to the current greedy IBC (backward compatible).

See [§12 "Rolling-horizon look-ahead" in the Optimization Logic doc](WVDOT_PMS_Optimization_Logic.md#12-rolling-horizon-look-ahead) for the operational details — what code path gets taken, how strategies are built over the window, and how carryover interacts with per-year budget caps within the window.

The other options on the menu above remain open research tracks. If we decide to revisit optimization in the future, this doc is the place to update first.
