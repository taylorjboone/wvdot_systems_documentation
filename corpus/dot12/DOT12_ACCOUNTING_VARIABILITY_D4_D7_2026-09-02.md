# DOT-12 accounting variability — Districts 4 & 7

**How often do a worker's accounting fields actually change?**

*Generated 2026-09-02 from production `dot12`. Window: 2026-06-01 – 2026-08-31.*

---

## 1. Can a default set of accounting codes work?

**The question:** for how many employees could the system hold a single default
set of accounting codes and have it be correct for **90% of the days they work**?

**The answer: 17 of 591 employees — 2.9%.** Mean coverage across
all 591 employees is only 32% of their days.

| A single default set would be correct for… | Employees | Share |
|---|---:|---:|
| ≥ 90% of the days they work | 17 | 2.9% |
| ≥ 80% of the days they work | 52 | 8.8% |
| ≥ 75% of the days they work | 66 | 11.2% |
| ≥ 50% of the days they work | 129 | 21.8% |

*Employees with fewer than 10 charged days in the window are excluded (163 of 754); a worker with three days is trivially 100%.*

### By district

| District | Employees | ≥90% | Share | ≥75% | Share | Mean coverage |
|---|---:|---:|---:|---:|---:|---:|
| District 4 | 205 | 11 | 5.4% | 29 | 14.1% | 35% |
| District 7 | 386 | 6 | 1.6% | 37 | 9.6% | 30% |

### Why it fails — and what would have to give

A worker touches a **median of 14 distinct task orders** (mean 17.2, p90 38) across the 13 weeks, over a median
of 36 worked days. Their individual days are simple — two thirds are a
single column — but they are simple in a *different* way each day. Task order is
what moves, and it moves constantly.

Relaxing the default set shows exactly which fields are the obstacle:

| Default set holds… | ≥90% of days | ≥75% | Mean coverage |
|---|---:|---:|---:|
| Task order + program + activity + receiving org + LDPR *(full set)* | 3% | 11% | 32% |
| Program + activity + receiving org + LDPR | 4% | 13% | 37% |
| Activity + receiving org + LDPR | 5% | 14% | 39% |
| Program + receiving org + LDPR | 13% | 34% | 58% |
| Receiving org + LDPR only | 16% | 38% | 65% |

Even stripped back to receiving org and LDPR — no task order, no activity, no
program — a stored default is right 90% of the time for only about one employee
in six.

**Conclusion.** Holding a per-employee default accounting set and generating the
DOT-12 from it is *not* viable as a general mechanism in these two districts. It
would serve a small minority of employees. The defensible version of the idea is
narrower: pre-fill the stable fields (receiving org, LDPR, sub-activity — see
§8), leave activity and task order to be chosen, and treat full auto-generation
as an opt-in for the specific orgs and individuals that measurably qualify.

---

## 2. Question and method

A DOT-12 column carries a full accounting coordinate — LDPR, receiving unit,
activity, sub-activity, program and task order. A worker's hours for a day are
split across however many columns the day required. This measures **how many
distinct accounting coordinates each worker actually touches**, per week and per
day, and which individual fields move versus stay put.

The practical question behind it: *if a worker reported only a pool of hours,
how much of the coding could the system supply on its own?*

**Scope**

| | |
|---|---|
| Districts | 4 (`04xx`) and 7 (`07xx`) |
| Window | 2026-06-01 → 2026-08-31 (13 complete weeks) |
| Charge rows | 35,860 |
| Workers | 754 |
| Worker-weeks | 4,789 |
| Worker-days | 20,509 |
| Joined to labor inventory | 35,520 / 35,851 (99.1%) |
| Carrying a TW short code | 25,179 / 35,851 (70.2%) |

September 2026 is excluded — both districts have only partial data (and some
forward-dated forms), which would understate per-week counts. D4 entered
service in August, D7 in June, so D7 contributes most of the history.

Headline figures were recomputed independently in SQL on the server and match
the Python pipeline exactly (20,509 worker-days, mean 1.45 columns, 67.9% single-column).

A **combination** below means one distinct set of *(task order, program, activity,
receiving org, LDPR)* — the five fields that identify what a column is charging.
Sub-activity is excluded from the set (it is blank on almost every column) but is
still reported in the defaultability table. Charges of 0 hours and
the `0000000000` placeholder employee (9 rows) are excluded.

---

## 3. Headline findings

1. **A worker averages 3.58 distinct accounting combinations per week** (median 3). But this is a long tail — 25% of worker-weeks use exactly one.

2. **Two-thirds of worker-days are a single column** — 67.9% of 20,509 worker-days carry exactly one accounting combination, mean 1.45. Since a DOT-12 is a *daily* form, this is the number that governs auto-generation.

3. **The fields split cleanly into stable and volatile.** Sub-activity and
receiving unit are effectively constant within an org; LDPR and program are
mostly stable; **activity and task order are what actually move.**

4. **Hours are highly predictable** — median 8.0 h/day, with 49% of worker-days at exactly 8.0 h.

5. **MEXPR is not the dominant program here.** In D4/D7 the mix is led by `D07AP` (31.5%), `D04AP` (13.7%), `2026870011` (7.8%) — MEXPR is 3.4%. District annual plans, not
maintenance expense payroll, are what these crews charge to.

---

## 4. Distinct accounting combinations per worker-week

| Combinations | Worker-weeks | Share | Cumulative |
|---:|---:|---:|---:|
| 1 | 1,204 | 25.1% | 25.1% |
| 2 | 926 | 19.3% | 44.5% |
| 3 | 717 | 15.0% | 59.4% |
| 4 | 574 | 12.0% | 71.4% |
| 5 | 463 | 9.7% | 81.1% |
| 6+ | 905 | 18.9% | 100.0% |

Mean 3.58 · median 3 · p90 7 · max 28

---

### District comparison

| District | Workers | W-weeks | Mean | Med | p90 | =1 | ≤2 | 6+ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| District 4 | 361 | 1265 | **2.98** | 2 | 6 | 32% | 53% | 12% |
| District 7 | 394 | 3524 | **3.80** | 3 | 7 | 23% | 41% | 21% |

District 4 is measurably more uniform than District 7 — but D4 has only been on
the system since August, so treat the gap as provisional.

---

## 5. By worker short code

The short code comes from the labor inventory job title (`LaborInventory.Description`)
mapped through the state pay schedule. Note `LaborClassification` is useless as a
dimension — every worker in dTIMS is class `TW`.

| Short code | Role | Workers | W-weeks | Mean | Med | =1 | ≤2 | 6+ | Task orders | Activities |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `TW4WELD` | Transportation Worker 4 Welder | 6 | 40 | **2.75** | 2 | 32% | 50% | 8% | 2.52 | 2.30 |
| `TW3BMW` | Transportation Worker 3 Bridge Maintenance Worker | 7 | 86 | **3.20** | 3 | 21% | 40% | 7% | 3.10 | 2.77 |
| `TW1LAB` | Transportation Worker 1 Laborer | 10 | 63 | **3.41** | 3 | 22% | 38% | 14% | 3.30 | 2.83 |
| `TW1EQOP` | Transportation Worker 1 Equipment Operator | 30 | 178 | **3.46** | 3 | 26% | 40% | 16% | 3.41 | 2.84 |
| `TW4CRCH` | Transportation Worker 4 Crew Chief | 7 | 80 | **3.50** | 4 | 16% | 36% | 12% | 3.38 | 2.85 |
| `TW2EQOP` | Transportation Worker 2 Equipment Operator | 240 | 1546 | **3.88** | 3 | 22% | 36% | 22% | 3.84 | 2.97 |
| `TW3EQOP` | Transportation Worker 3 Equipment Operator | 64 | 503 | **4.00** | 4 | 18% | 35% | 23% | 3.93 | 3.07 |
| `TW3CRCH` | Transportation Worker 3 Crew Chief | 41 | 247 | **5.11** | 5 | 11% | 22% | 43% | 5.08 | 4.28 |
| `TW3MECH` | Transportation Worker 3 Mechanic | 30 | 129 | **6.98** | 6 | 16% | 22% | 51% | 6.75 | 2.28 |
| `TW2MECH` | Transportation Worker 2 Mechanic | 14 | 80 | **7.33** | 7 | 11% | 14% | 61% | 7.20 | 2.38 |

*Short codes with fewer than 25 worker-weeks are suppressed (4 of 14).*

**Mechanics are the outlier.** They carry two to three times the accounting
variety of any other field role — they charge across many equipment work orders
in a week. Equipment operators and laborers, the bulk of the workforce, sit
near the district average.

---

## 6. By job title — non-TW roles

Roles without a TW short code (county office, engineering, administration) also
appear on DOT-12s, and they are markedly **more** uniform than field crews.

| Title | Workers | W-weeks | Mean | Med | =1 | ≤2 |
|---|---:|---:|---:|---:|---:|---:|
| District Division Supply Specialist | 10 | 50 | **1.46** | 1 | 64% | 92% |
| Building Grounds Maintenance Worker Trainee | 4 | 35 | **1.49** | 1 | 57% | 94% |
| Administrative Assistant | 18 | 99 | **1.51** | 1 | 65% | 87% |
| Engineer Trainee 2 | 7 | 48 | **1.85** | 1 | 54% | 85% |
| County Office Manager | 11 | 77 | **2.04** | 2 | 43% | 69% |
| Engineer Associate | 8 | 42 | **2.26** | 2 | 31% | 67% |
| Business Operations Assistant 1 | 22 | 135 | **2.40** | 2 | 32% | 73% |
| Engineering Technician | 14 | 84 | **2.42** | 2 | 29% | 56% |
| Building And Grounds Maintenance Worker 2 | 6 | 45 | **2.47** | 2 | 22% | 64% |
| Engineering Technician Trainee | 7 | 47 | **2.53** | 2 | 17% | 55% |
| Engineering Technician Associate | 6 | 49 | **2.76** | 2 | 33% | 59% |
| Engineer Trainee 1 | 8 | 35 | **2.94** | 2 | 29% | 60% |
| County Supply Specialist | 11 | 74 | **2.95** | 1 | 51% | 69% |
| Engineering Technologist | 5 | 35 | **3.06** | 3 | 26% | 46% |

---

## 7. By org

| Org | Dist | Workers | W-weeks | Mean | Med | =1 | 6+ | 1-column days |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `0458` | 04 | 18 | 74 | **1.57** | 1 | 61% | 0% | 93% |
| `0758` | 07 | 15 | 81 | **1.68** | 2 | 44% | 0% | 89% |
| `0799` | 07 | 11 | 54 | **1.80** | 2 | 35% | 0% | 82% |
| `0760` | 07 | 18 | 86 | **1.92** | 2 | 36% | 0% | 84% |
| `0439` | 04 | 42 | 84 | **2.10** | 2 | 48% | 4% | 67% |
| `0431` | 04 | 36 | 123 | **2.49** | 2 | 37% | 4% | 74% |
| `0480` | 04 | 38 | 147 | **2.52** | 2 | 27% | 5% | 53% |
| `0417` | 04 | 45 | 137 | **2.66** | 2 | 36% | 9% | 62% |
| `0779` | 07 | 38 | 305 | **2.69** | 2 | 30% | 10% | 73% |
| `0460` | 04 | 25 | 55 | **2.95** | 2 | 38% | 15% | 46% |
| `0446` | 04 | 23 | 115 | **3.08** | 3 | 25% | 8% | 77% |
| `0780` | 07 | 32 | 221 | **3.13** | 2 | 24% | 13% | 62% |
| `0467` | 04 | 18 | 114 | **3.13** | 3 | 18% | 10% | 75% |
| `0798` | 07 | 12 | 100 | **3.27** | 3 | 24% | 19% | 75% |
| `0767` | 07 | 36 | 401 | **3.34** | 3 | 21% | 13% | 78% |
| `0425` | 04 | 33 | 124 | **3.57** | 3 | 25% | 22% | 62% |
| `0704` | 07 | 40 | 321 | **3.59** | 3 | 21% | 18% | 76% |
| `0701` | 07 | 35 | 304 | **3.79** | 3 | 24% | 20% | 66% |
| `0721` | 07 | 40 | 313 | **3.85** | 4 | 23% | 22% | 71% |
| `0751` | 07 | 32 | 280 | **4.05** | 3 | 25% | 30% | 67% |
| `0749` | 07 | 41 | 358 | **4.32** | 4 | 14% | 27% | 67% |
| `0409` | 04 | 33 | 175 | **4.75** | 4 | 22% | 34% | 52% |
| `0711` | 07 | 27 | 357 | **4.92** | 4 | 14% | 34% | 55% |
| `0770` | 07 | 37 | 295 | **5.83** | 4 | 21% | 42% | 54% |

The spread between orgs is far wider than the spread between job titles. That
matters: **auto-generation is an org-level decision, not a role-level one.**

---

## 8. Which fields could actually be defaulted

For each org, the share of its charges that carry that org's single most common
value for the field. High = the field is effectively a constant and safe to
pre-fill; low = it genuinely varies and must be chosen.

| Field | Median across orgs | Distinct values in play | Reading |
|---|---:|---:|---|
| Sub-activity | **100%** | 167 | Constant — safe to default |
| Receiving unit | **90%** | 71 | Near-constant — safe to default |
| LDPR | **71%** | 12 | Mostly stable — default with review |
| Program | **61%** | 173 | Mostly stable — default with review |
| Activity | **28%** | 115 | Genuinely varies — must be chosen |
| Task order | **26%** | 2,627 | Genuinely varies — must be chosen |

This is the core result. **The 'who and where' fields are stable; the 'what work'
fields are not.** A default profile per org can legitimately supply LDPR,
receiving unit, sub-activity and program — but activity and task order have to
come from somebody who knows what the crew did.

---

## 9. Per worker-day — what one DOT-12 actually covers

| Columns that day | Worker-days | Share |
|---:|---:|---:|
| 1 | 13,919 | 67.9% |
| 2 | 4,622 | 22.5% |
| 3 | 1,463 | 7.1% |
| 4 | 351 | 1.7% |
| 5+ | 154 | 0.8% |

Mean 1.45 columns per worker-day; median 1.

---

## 10. The hours pool

If a worker reported a single daily total, this is the shape of what they'd report.

| Hours | Worker-days | Share |
|---:|---:|---:|
| 8.0 | 10,030 | 48.9% |
| 10.0 | 4,316 | 21.0% |
| 12.0 | 1,167 | 5.7% |
| 9.0 | 682 | 3.3% |
| 11.0 | 620 | 3.0% |
| 14.0 | 608 | 3.0% |
| 8.5 | 450 | 2.2% |
| 10.5 | 322 | 1.6% |

Mean 9.28 h · median 8.0 h. The top three values alone cover 76% of all worker-days.

---

## 11. What this implies

**Simple is not the same as predictable.** 68% of worker-days are a single
accounting combination — the day itself is not complicated. But §1 shows a stored
default set is right for 90% of days for only 3% of employees. The day is simple;
it is simply a *different* simple thing each day. Generating a DOT-12 from a
remembered profile therefore fails as a general mechanism, and the single-column
statistic must not be read as evidence that it would work.

**Partial defaults still earn their keep.** They just cannot cover activity or task order.
Median defaultability is 26% for task order and 28% for activity. A system that guessed those
would be wrong most of the time. The honest design pre-fills the stable fields,
leaves the work fields empty, and asks one question instead of six.

**Target the uniform orgs first.** The org table shows the range — the most
uniform orgs run single-column days at over 85%, the most varied under 50%. A
pilot should start at the top of that list, not with a district-wide switch.

**Mechanics are the worst fit** and should be explicitly out of scope for any
auto-generation: they average the highest combination counts of any role and
their variety is real equipment work-order variety, not sloppiness.

---

## 12. Caveats

- **D4 is thin.** It entered service in August, so its weeks are fewer and
  its early-adoption behavior may not be representative.
- **9 charge rows** carry the placeholder employee id `0000000000`
  and were excluded. That is a data-quality issue worth chasing separately.
- **331 rows** (0.9%) could not be joined to the
  labor inventory — those workers are absent from the active dTIMS roster.
- Sub-activity is blank on the overwhelming majority of columns; its 100%
  'defaultability' means *reliably empty*, not reliably meaningful.
- Weeks are ISO (Monday-start), not the 14-day OASIS pay period.
- Counts are of *distinct coordinates touched*, not of effort. A worker with two
  combinations may still have spent the whole week on one of them.

