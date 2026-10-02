# The analysis worker and `amps`

`run_python` runs your code in a fresh Python process: `import amps` plus the AMPS code (`engine`, `bms`,
`bridges`, `api`), polars, numpy, pandas, matplotlib, highspy. The database is **read-only** (writes
fail: save runs with the save tools, not SQL). No internet, no files kept between calls, no secrets.
Print what you want to read; `amps.result(x)` hands a value back as JSON. Anything saved in `out/`
(`amps.save_chart`, `amps.save_table`) is shown in the chat. Each call re-loads what it needs, so do a
whole study in one call. Don't start your own process pools.

**Years.** Year 1 is the run's start year (2026 unless told otherwise); Year 0 is the network before any
work, at the start of that year. Say "2026", never "FY".

## Basics

| Call | Does |
|---|---|
| `amps.sql(q, params=None)` | read-only query → polars DataFrame; named params `:r` with `{"r": 1}`; jsonb → JSON text |
| `amps.rows(q, params=None)` | the same as a list of dicts (jsonb stays dicts) |
| `amps.progress(msg, pct=None)` | a live progress line in the chat |
| `amps.result(value)` | return a dict / list / DataFrame / `.to_dict()` to yourself |
| `amps.save_chart(fig, name)` | matplotlib figure → `out/name.png` |
| `amps.save_table(df, name)` | DataFrame → `out/name.xlsx` (or `.csv`) |
| `amps.calendar_year(y, start)`, `amps.year_label(y, start)` | 3, 2026 → 2028; "Year 3 · 2028" |

PMS tables are in `public` (`analysis_runs`, `analysis_segments`, `configs`, `projects` …); BMS tables in
`bms.` (`bms.runs`, `bms.configs`, `bms.committed_projects` …).

## Pavement — `amps.pms`

```python
net = pms.load_network(network="non-interstate-nhs", where=None, config_id=None, start_year=None,
                       inflation_rate=None)
```
Presets: `all`, `interstate`, `nhs`, `non-interstate-nhs`, `non-nhs` (the run dialog's). `where` adds SQL on
`analysis_segments` (e.g. `"district_code = 4"`). `config_id` defaults to the system default; start year and
inflation default to the config's, as a run's would. ~5 s. `net.describe()` → segments, miles, lane-miles.

```python
pms.baseline(net, years=10)          # do nothing: year, calendar_year, pct_good, pct_fair, pct_poor
```

```python
r = pms.optimize(net, years=10, max_pct_poor=None, min_pct_good=None, every_year=True, target_year=None,
                 objective="benefit", budget=None, time_limit_s=600, mip_gap=0.001,
                 min_year_share=None, min_year_spend=None, extra_rows=None)
```
The app's MILP-assist (exact, HiGHS). Condition is MAP-21 Good / Fair / Poor by lane-miles.
- `objective="min_cost"`: the **cheapest** plan that meets the targets. `budget=None` means no limit
  (each year's spend is that year's need); a number, a list of per-year amounts or `{year: $}` is a ceiling.
- `objective="benefit"`: the most benefit within `budget`, which is required.
- `every_year=True` holds the targets in every year from 1 to `target_year` (default `years`).
- **Even spending** (hard, in every year): `min_year_share=0.5` = no year spends less than half of the
  plan's biggest year; `min_year_spend=35e6` = at least $35M every year. Combine with `budget` (the cap).
- **Anything else linear** — `extra_rows=fn`. `fn(cands)` gets the candidate frame (one row per
  joint × treatment × apply year, in the model's order: `analysis_segment_id` = the joint, `treatment_id`,
  `apply_year`, `cost`, `committed`, and `poor_y{n}` / `good_y{n}` = the candidate's signed lane-mile effect
  on Poor / Good in year n) and returns `[(coefficients, lower, upper, label), …]`, one coefficient per row
  (None = unbounded). Examples: a treatment cap, a district's share of spend (join `net.segments` on
  `pavement_joint_id` for district), a year-over-year change limit, more Good lane-miles than a number in
  one year. These rows hold in every solve step, so the result respects them exactly.
- If the targets can't all be met, `summary["outcome"]` is `years_maximized`: % Poor is met in as many
  years as possible, then % Good; `summary["fallback_reason"]` says which years missed.

`r.summary` keys: total_cost, max_year_spend, outcome, targets_met, years_met, worst_pct_good /
worst_pct_poor, start_pct_good / start_pct_poor, projects, solver_status, mip_gap_pct, solve_time_s,
start_year, years, config_id, lane_miles, inflation_rate, warnings. Also:
- `r.years`: year, calendar_year, spend, budget, projects, pct_good / fair / poor; Year 0 is the start.
- `r.mix`: treatment_id, joints, cost, miles.
- `r.plan`: one row per treated joint.
- `r.targets`: each target row with achieved_pct and satisfied.
- `r.to_dict()` (add `plan=True` for the plan).

Speed: ~10 s for 10 years on non-Interstate NHS (~20k segments); the first call precomputes candidate
effects and later calls with the same years reuse them.

```python
f = pms.min_flat_budget(net, years=10, max_pct_poor=5, min_pct_good=45, every_year=True, lo=0, hi=None,
                        tol=250_000, probe_time_limit_s=180, cheapest_within=True,
                        min_year_share=None, min_year_spend=None, extra_rows=None)
```
The smallest **flat** annual budget — the lowest per-year cap — that meets the targets every year, by
bisection: it lowers the cap until the MILP proves it infeasible. The even-spending rules and `extra_rows`
hold in every probe and in the final plan, so pass the user's current rules to keep them. It returns:
- `f["flat_budget"]`, and `f["infeasible_below"]` (the largest budget proven short)
- `f["probes"]`
- `f["min_cost"]`: the unconstrained minimum-cost study, which sets `hi`
- `f["at_flat"]`: the cheapest plan within the flat budget

`f.get("note")` explains a $0 answer (doing nothing already meets the targets) or a target that can't
be met at any budget. A probe that meets takes ~5–15 s. A probe that falls short takes 30–110 s, because it then counts years
met. Use `tol=1_000_000` for a quick answer.

```python
pms.list_runs(limit=20, search=None)   # saved runs (run_id, name, status, network, years, start_year, total_cost_m)
pms.run_summary(run_id)                # a saved run's settings, yearly results (with calendar_year), mix
```

Limits to state when they matter:
- MILP-assist allows **one treatment per joint** over the whole horizon, so it can't plan repeated cheap
  preservation. That can overstate cost on long horizons.
- Costs are nominal (the run's inflation).
- A minimum over N years lets the network slide to exactly the targets in year N, because nothing after N
  counts. Check with a longer horizon, and compare the first N years.

## Bridges — `amps.bms`

```python
bms.configs()   # config_id, name, model ('dtims' | 'amps'), is_system_default, dTIMS years
net = bms.load_bridges(config_id=None, start_year=2026, scope="nhs_non_interstate", districts=None,
                       bars=None, committed=True)
```
- The default config is the first **dTIMS-model** config. That is the model with MILP targets on deck
  area; the system default "AMPS Markov" has no targets.
- `scope` is one of `all`, `nhs`, `non_nhs`, `nhs_non_interstate`. `districts` takes a list like `[4, 7]`.
- `bars` is a **bridge list**: BARS numbers as a list (`["16A128", "20A003"]`) or a text of them. A bridge
  is kept when it is on the list and in `scope` and `districts` (pass `scope="all"` to study exactly the
  list). A BARS that isn't a WVDOT-owned in-service bridge raises an error naming it. `net.bars` is the list;
  `bms.optimize` keeps it. Save the same list as `scope.bars` in save_bms_run.
- Committed projects are placed as a BMS run places them. Unmapped ones are printed.
- Loading takes ~3 s (658 bridges for non-Interstate NHS).

```python
r = bms.optimize(net, budget=50e6, years=13, max_pct_poor=None, min_pct_good=None, target_years=None,
                 optimizer=None, time_limit_s=900)
```
- `budget` is a flat $ per year for Years 1..`years`, a list of per-year amounts, or `{calendar year: $}`.
- Targets are % of **deck area** Poor / Good. They are held in every funded year except the first, which
  is an evaluation year: committed work only, no target row. `target_years` limits them to those calendar
  years.
- `optimizer` is `milp` by default when a target is set, else `ibc` (incremental benefit/cost).

The result:
- `r.summary`: total_spend, total_budget, targets_met, years_missed, milp (status, phase, rows_met,
  missed), totals, seconds.
- `r.years`: year, calendar_year, budget, spend, committed_spend, projects, pct_good, pct_poor,
  do_nothing_pct_good / do_nothing_pct_poor, target_met. Years run to the config's end year.
- `r.plan`: bars, year, calendar_year, treatment, cost, committed, district.

Committed work can overdraw a year's budget, as in a BMS run.

Speed: the first study generates every bridge's strategies (~45 s for 658 bridges). Later studies on
the same `net` with the same years and target years re-select from the cached strategies (~5 s).

```python
f = bms.min_flat_budget(net, years=13, max_pct_poor=13, min_pct_good=12, lo=0, hi=200e6, tol=250_000)
```
The smallest flat annual budget whose MILP plan meets the targets, by bisection. Returns flat_budget,
infeasible_below, probes and at_flat. **The BMS MILP has no minimum-cost objective**: it maximises
benefit within the budget. The funding need is therefore this budget search, not a cheapest plan.

```python
bms.list_runs(limit=20, search=None); bms.run_summary(run_id)
```

## Worked examples

**"How much do we need to spend to keep non-Interstate NHS ≤5% Poor and ≥45% Good every year for 10 years?"**
```python
import amps, polars as pl
from amps import pms
net = pms.load_network("non-interstate-nhs")
base = pms.baseline(net, 10)
print(net); print(base)                               # is the target already failing in Year 1?
low = pms.optimize(net, years=10, max_pct_poor=5, min_pct_good=45, objective="min_cost")
print(low)                                            # least total; often lumpy (front-loaded)
flat = pms.min_flat_budget(net, years=10, max_pct_poor=5, min_pct_good=45, tol=500_000)
long = pms.optimize(net, years=15, max_pct_poor=5, min_pct_good=45, objective="min_cost")
first10 = long.years.filter(pl.col("year").is_between(1, 10))["spend"].sum()
amps.result({"min_total": low.summary, "flat_budget": flat["flat_budget"],
             "infeasible_below": flat["infeasible_below"], "cheapest_within_flat": flat["at_flat"].summary,
             "first_10_of_15yr_plan": first10})
```
Reference: on config 1 from 2026, the least total is $456.7M, lumpy ($130.9M, $18.9M, $139.3M, $150.9M,
then little). The smallest flat budget is about $70.8M/yr. The 15-year plan spends ~$747M in its first 10
years.

**"Same, but capped at $70.8M a year and no year below half of the biggest year"** (MILP, cheapest)
```python
r = pms.optimize(net, years=10, max_pct_poor=5, min_pct_good=45, objective="min_cost",
                 budget=70.8e6, min_year_share=0.5)
print(r.years)                  # config 1 from 2026: $516.6M; $70.8M/yr in 2026-29, ~$35.4M/yr from 2031
```
Then save it with the same settings (`milp_min_year_share` in the run request) and wait for it.

**"Now lower the per-year cap until it's no longer feasible"** (keeping every rule: targets, 50% floor)
```python
f = pms.min_flat_budget(net, years=10, max_pct_poor=5, min_pct_good=45, min_year_share=0.5,
                        hi=70.8e6, tol=100_000)
print(f["flat_budget"], f["infeasible_below"])   # the lowest cap that works / the highest proven short
print(f["at_flat"].years)                        # the cheapest plan at that cap, every rule held
```
Report both numbers (the answer lies between them), then save `at_flat` with the same rules and
`annual_budget` = the flat budget.

**A custom requirement: at most 150 thick overlays over the whole plan**
```python
def cap_thick(c):
    return [([1.0 if t == "THICK_OVERLAY" else 0.0 for t in c["treatment_id"]], None, 150, "thick <= 150")]
r = pms.optimize(net, years=10, max_pct_poor=5, min_pct_good=45, objective="min_cost", extra_rows=cap_thick)
```

**A chart of the spend by year**
```python
import matplotlib.pyplot as plt
d = low.years.filter(pl.col("year") >= 1)
fig, ax = plt.subplots(figsize=(8, 3.5))
ax.bar([str(c) for c in d["calendar_year"]], d["spend"] / 1e6); ax.set_ylabel("$M")
amps.save_chart(fig, "spend_by_year")
```

**Bridges: the smallest flat budget for ≤13% Poor, ≥12% Good (deck area), non-Interstate NHS, 2026–2038**
```python
from amps import bms
net = bms.load_bridges(31, start_year=2026, scope="nhs_non_interstate")
f = bms.min_flat_budget(net, years=13, max_pct_poor=13, min_pct_good=12, hi=150e6, tol=1e6)
print(f["flat_budget"], f["probes"]); print(f["at_flat"].years)
```
