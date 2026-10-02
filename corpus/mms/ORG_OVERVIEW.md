# Org Overview — what it is and why it exists

A short orientation for people new to this part of the system.

---

## Contents

- [What is a Task?](#what-is-a-task)
- [Why Accomplishment is the most important object](#why-accomplishment-is-the-most-important-object)
- [How it's charged in OASIS](#how-its-charged-in-oasis)
- [What's missing in DTIMS OM](#whats-missing-in-dtims-om)
  - [Validation on entry](#validation-on-entry)
  - [Accomplishment review and correction](#accomplishment-review-and-correction)
- [The DDL](#the-ddl)
  - [How a DDL row is built](#how-a-ddl-row-is-built)
- [What the new Org Overview is designed to do](#what-the-new-org-overview-is-designed-to-do)
  - [1. See / compare organizational accomplishment](#1-see--compare-organizational-accomplishment)
  - [2. Drill into specific filters](#2-drill-into-specific-filters)
  - [3. Consume DDL records](#3-consume-ddl-records)
  - [4. Debug issues or errors](#4-debug-issues-or-errors)
- [Quick navigation map](#quick-navigation-map)
- [Key data sources](#key-data-sources)
- [What's coming next: editing data from inside the app](#whats-coming-next-editing-data-from-inside-the-app)
- [A rule that has never been checked](#a-rule-that-has-never-been-checked)
- [How much accomplishment lives on the >20× rule's flagged rows?](#how-much-accomplishment-lives-on-the-20-rules-flagged-rows)
  - [Concrete example — what a 20× row actually looks like](#concrete-example--what-a-20-row-actually-looks-like)

---

## What is a Task?

A **Task** is the unit of planned maintenance work. Every other object in
the system hangs off a Task: organization (the crew/yard responsible),
activity / performance standard (what kind of work — pothole patching,
mowing, ditch cleaning, …), account code (where the money comes from),
asset references (which roads, bridges, or other assets the work is
done against), schedule, estimated cost, and so on.

Tasks are the "god object" — when you ask "who did what, where, with
what equipment and people, charged to what budget", the answer is
always rooted in a Task.

## Why Accomplishment is the most important object

A Task by itself is a plan. **Accomplishment** is the report of work
actually done against that plan. Concretely it's a row in
`daily_work_report_line_item` (DWRLI): one entry that says

> on **this date**, against **this Task**, on **this asset/route segment**
> (with BMP/EMP), my crew completed **N units** of work.

Accomplishment is the most important object in the system because it's
what everything else is measured against:

* **Productivity** — accomplishment ÷ days worked, accomplishment ÷
  labor hours, accomplishment ÷ equipment hours.
* **Cost efficiency** — total cost ÷ accomplishment ($/unit).
* **Plan vs actual** — annual work plan is in planned units;
  accomplishment is the actual delivery against it.
* **Asset history** — every road or bridge's maintenance record is
  effectively the set of accomplishments that touched it.

Without accomplishment, a Task is just a budget line. With
accomplishment, you can answer every "are we getting our money's worth"
question.

## How it's charged in OASIS

OASIS (the WV state financial system) is the source of truth for
spending. Crews don't enter dollars into the maintenance app
directly — they report time, equipment use, and stockpile draws against
a Task. Those entries flow nightly into OASIS, which **charges** them:

* **Labor transactions** → labor cost (hours × employee rate)
* **Equipment transactions** → equipment cost (hours × equipment rate)
* **Stockpile transactions** → material cost (quantity × unit cost from
  inventory)
* **Other costs** → miscellaneous one-off charges

What OASIS actually sees is the **task order ID** — a stable string token
on the Task that names the chargeable unit of work (e.g.
`250502303409`). Crews and the system never charge "task #internal-pk";
they charge the task order ID. The integration between this app and
OASIS is essentially a one-way handshake: **the only public API in the
whole stack is the call that creates a task order ID on the OASIS
side** so subsequent labor / equipment / stockpile / other entries have
something to reference. After that the cost flow is one-directional —
charges accumulate against the task order ID and get posted back into
the `base_transaction` family of tables here, keyed by
`(task_id, transaction_date)`. Those rows feed the `mv_task_day_costs`
materialized view that backs every cost number in the analytics screens.

The point is: **accomplishment is reported against a Task; cost arrives
afterward against the same Task** by way of its task order ID. They
join at `(task_id, date)`. Every analytic in this app is some form of
grouping that join.

## What's missing in DTIMS OM

DTIMS OM is the system of record where crews and supervisors enter
accomplishments. Two big gaps in how it handles that data — and the
second one is the most important capability the whole system is
missing:

### Validation on entry

DTIMS OM has no per-activity sanity checks on accomplishment input. No
ceiling against the standard daily production, no unit sanity test, no
"this looks suspiciously high" prompt. The system happily accepts 7,800
shoulder miles of mowing in a single day. The same is true for cost
records flowing in from the integration: nothing flags a row that
looks structurally fine but is wildly out of bounds (no route, no
labor against an accomplishment, etc.). So **bad data lands by
default**, and every downstream user of the data is on their own to
find it.

A couple of specific gaps worth calling out, because they're the ones
that show up most often when you try to do anything with the data
later:

* **Mileposts (BMP / EMP) aren't required.** A crew can attach a
  route name to an accomplishment without specifying which segment of
  that route the work was done on. For a 19-mile state route, that's
  ambiguous to the point of being unusable — was it the first mile,
  was it the last mile, was it the whole thing? In practice "the
  whole thing" is sometimes literally what happened (mowing the full
  length of CR 1, for example), but the system can't tell that case
  apart from the case where the crew just didn't fill the field in.
  We'd like BMP/EMP to be **explicitly required**, with a clear
  marker for "full route" rather than NULL — that way downstream
  tooling can map an accomplishment to a specific stretch of asset
  rather than guess.
* **Deighton (the upstream platform DTIMS OM is built on) allows
  overlapping asset references on a single Task.** A Task can carry
  two asset references that cover the same milepost range, or a road
  reference that overlaps a bridge reference, or two bridges that
  refer to the same span. This causes problems at two levels: at
  data-entry time, crews aren't sure which reference to charge a line
  item against; and at the schema level it makes "what work touched
  this asset" non-deterministic — you have to pick a tie-breaker, and
  every analytic that lands on an asset has to deal with the
  duplication. There's no `UNIQUE` over the asset segments per Task,
  so the bad state is allowed to exist by design.

### Accomplishment review and correction

This is the part the whole system most needs and most lacks.
Accomplishment is the root object — every productivity number, every
$/unit, every plan-vs-actual chart, every asset-history view derives
from accomplishment rows. If those rows are wrong, every KPI built
from them is wrong, and there's no amount of dashboard polish that
fixes a number whose underlying record was off by a factor of ten.

DTIMS OM gives you a record list to scroll through, but in practice:

* Records don't sort the way you'd expect (or sometimes don't sort at
  all). Finding a specific accomplishment by date or org or activity
  often means paging through hundreds of records visually. Most of the
  time spent "correcting" records is actually time spent finding them.
* There's no notion of *which* records you should be looking at first.
  Without per-row validation flags coming from somewhere, you can't
  filter to "the rows the system thinks are wrong" — you can only
  page through everything.
* Bulk corrections aren't really a thing. Each suspicious row is fixed
  one at a time, in a separate window, in the upstream UI, and only
  after you've already done the detective work to find it elsewhere.

The result is that **review and correction is the bottleneck of the
entire analytics pipeline**. The business intelligence sitting on top
of accomplishment data is only as good as the tail of records that
got reviewed and fixed — and that tail is short, because the workflow
to do it doesn't really exist. Closing this gap is the single highest
leverage thing on the roadmap; getting from "we can see the issues" to
"we can fix the issues from the same screen" is where everything else
gets compounding value.

### Validation against financial data

Accomplishments don't live alone. For most activities they're paired
with a financial record on the same task-day — labor hours from the
crew that did the work, equipment hours for the trucks/loaders/mowers
that ran, and material/stockpile transactions for whatever was
consumed. The accomplishment is the *output*; the labor/equipment
hours are the *input*. Cross-checking the two is one of the
highest-signal validations available, and DTIMS OM doesn't do it.

A few patterns are obvious bugs the moment you ask the question:

* **Accomplishment with no labor hours on the same task-day** for an
  activity that physically requires people (mowing, patching, ditch
  cleaning, etc.). 4 miles of mowed shoulder doesn't happen with zero
  labor charged. Either the accomplishment was logged against the
  wrong task, the labor was charged elsewhere, or the day was
  duplicated.
* **Accomplishment with no equipment hours** for an activity that
  physically requires a piece of equipment (anything involving a
  mower, dump truck, paver, loader). A "200 — pothole patching" row
  with zero truck-hours is at minimum suspect.
* **Labor / equipment hours far out of proportion to accomplishment**
  — e.g. 32 labor hours and 0.1 miles of patching on a single day, or
  the inverse (10 miles patched with 1 labor hour). The ratio
  shouldn't be hard-coded everywhere, but the standard production
  rate per activity gives a defensible expected band per unit.
* **Activity types that should never carry labor at all** (a few
  contractor-led activities) showing labor hours, and vice versa.

Today the app can *detect* all of this — every input is in the same
Postgres database the analytics queries run against — and surface it
as a per-row validation flag (the same DDL row-level error/warning
system already in place). What we **can't** do is fix it from inside
the app: the source of truth is OASIS, and the only way to update an
accomplishment, a labor transaction, or an equipment transaction is
to log into OASIS and edit it there. So the tool's reach today ends
at "we know this row is wrong, here's why, go fix it upstream."

The bigger idea, which is worth keeping on the table even though it's
larger in scope: **OASIS data could live in this database and the
dot12 app could be the editing surface for it**, either via the OASIS
APIs (where they exist and are reliable enough) or via headless
browser automation against the OASIS UI (where they aren't). The
shape of the workflow would be:

1. Pull OASIS data into the local DB on a schedule the same way the
   cost integration does today, so the validation rules can read it
   directly without round-tripping through OASIS.
2. Surface validation failures in the same DDL/Org Overview screens
   the rest of the app uses, with the offending row, the reason, and
   the *proposed correction* (e.g. "remove this duplicate, attach
   labor to task 250101101001 instead"). The proposed correction is
   computable for most of the obvious patterns above — the answer is
   often unambiguous given the surrounding rows.
3. A human reviews the proposed correction in-app and clicks
   **Approve**. The app then pushes the change back to OASIS, either
   through the OASIS API or by driving the OASIS web UI in a
   headless browser session, and waits for the round-trip to confirm
   the value landed.
4. The dot12-side row is marked corrected only after OASIS
   acknowledges the write — so the local copy and the source of
   truth never drift, and the human always retains the
   approve/reject veto on every push.

The cost-of-quality argument here is: getting from "good data in the
source system" to "good data in the destination system" is by far
the cheapest part of the pipeline once you have the validation
machinery and the human-in-the-loop UX. The machinery doesn't have
to write to OASIS perfectly on day one — even at "draft a corrected
row, surface it next to the bad one, the human pastes it into OASIS"
the time spent per fixed record drops by an order of magnitude vs
the current detective-work-then-edit cycle. Fully closing the loop
(button-press fixes the OASIS row directly) is the end state, but
every step along the way pays off independently.

## The DDL

DDL stands for **Daily Detail Listing** — the canonical "audit row"
used by central office and the districts. One DDL row =
one `(task_id, accomplishment_date, route, asset_segment)` combination.
It bundles:

* The accomplishment line item (units, route name, BMP/EMP)
* Labor / equipment / stockpile / other costs for that task-day,
  apportioned across the day's line items by their share of the day's
  total accomplishment (`perc`)
* Validation flags (no route name, no labor reported, hours skew,
  out-of-season SRIC, accomplishment that exceeds the standard
  daily production by 2× or 20×, etc.)

The DDL itself today is generated by a separate audit tool —
**built in-house by WVDOT IT staff (myself included)** to fill the
gap left by the upstream system — and consumed as a static export.
That tool gave us the rules, the apportionment math, and the
correction-response workflow, but by design it's an export-only
surface: no live drilling, no aggregation, no real-time filtering,
and no in-place editing of the records it surfaces. Bringing the DDL
inside this app, layering analytics on top of it, and (next) wiring
up the in-place edit workflow is the next step on top of the same
foundation.

### How a DDL row is built

A DDL row is the result of joining and apportioning two streams of
data — accomplishment line items and OASIS-charged cost transactions —
by `(task_id, accomplishment_date)`. The diagram below traces that
flow for a single task-day.

```
TASK 250502303409 — Org 0502 · Activity 303 (Mowing) · 2024-08-19
═══════════════════════════════════════════════════════════════════

  ACCOMPLISHMENT LINE ITEMS                COST TRANSACTIONS
  (operations.daily_work_         (operations.base_transaction +
   _report_line_item)              labor / equipment / stockpile /
                                   other, summed in
                                   mv_task_day_costs)

  ┌──────────────────────────┐    ┌────────────────────────────┐
  │ Berkeley CR 7  BMP 0–5   │    │ Labor      16.0 h  $1,234  │
  │   accomp = 3.5 MI        │    │ Equipment  12.0 h    $320  │
  ├──────────────────────────┤    │ Stockpile   0.0       $0   │
  │ Berkeley CR 7  BMP 5–8   │    │ Other                $50   │
  │   accomp = 2.0 MI        │    │                            │
  ├──────────────────────────┤    │ Day total           $1,604 │
  │ <no route>               │    └────────────────────────────┘
  │   accomp = 0.0 MI        │                  │
  └──────────────────────────┘                  │
              │                                 │
              │ GROUP BY                        │ keyed by
              │ (route, asset, BMP, EMP)        │ (task_id, date)
              │ SUM(accomp)                     │
              ▼                                 │
                                                │
   daily_total_accomp = 5.5 MI                  │
   row 1  perc = 3.5 / 5.5 = 0.636              │
   row 2  perc = 2.0 / 5.5 = 0.364              │
   row 3  perc = 0      (zero-accomp line)      │
              │                                 │
              └──────────┐         ┌────────────┘
                         │         │
                         ▼         ▼
                    multiply each row's
                    cost columns by its perc

                              │
                              ▼

  DDL ROWS (one per asset segment per task-day)
  ─────────────────────────────────────────────────────────────────
  ┌─────────────────────────────────────────────────────────────┐
  │ 2024-08-19  Task 250502303409  Org 0502  Act 303            │
  │ Berkeley CR 7  BMP 0–5   3.5 MI   perc 63.6%                │
  │   labor  10.2 h   $784   |   equipment  7.6 h   $204        │
  │   stockpile  $0          |   other  $32                     │
  │   TOTAL  $1,019                                             │
  │   flags  (none)                                             │
  └─────────────────────────────────────────────────────────────┘
  ┌─────────────────────────────────────────────────────────────┐
  │ 2024-08-19  Task 250502303409  Org 0502  Act 303            │
  │ Berkeley CR 7  BMP 5–8   2.0 MI   perc 36.4%                │
  │   labor   5.8 h   $449   |   equipment  4.4 h   $116        │
  │   stockpile  $0          |   other  $18                     │
  │   TOTAL  $585                                               │
  │   flags  (none)                                             │
  └─────────────────────────────────────────────────────────────┘
  (the third zero-accomp line is filtered out — perc 0,
   no allocated cost, no contribution to the day)
```

In words:

1. **Group accomplishment line items** for the task-day by their
   asset segment (`route_name`, `asset_reference_id`, `bmp`, `emp`).
   That's the row grain of the DDL — one row per distinct segment a
   crew touched on that task on that day.
2. **Compute `perc`** for each segment as its share of the
   task-day's total accomplishment (with a `1/N` fallback when the
   day's total accomp is zero so trans-only days still surface).
3. **Sum the day's costs** at `(task_id, transaction_date)` from the
   pre-aggregated `mv_task_day_costs` materialized view.
4. **Apportion** by multiplying each row's labor / equipment /
   stockpile / other cost (and quantity) by its `perc`. A row that
   accounts for 63.6% of a task-day's mowing carries 63.6% of that
   day's allocated labor, equipment, etc.
5. **Run validation** against the resulting row (route presence,
   labor / equipment expectations, hours-skew, SRIC season,
   accomplishment vs. EAD's `standard_daily_production`). Errors and
   warnings attach to the row.

The DDL row is what every analytic in this app eventually rolls back
up out of — KPI tiles, the bar chart, the breakdown tabs, the cost
mix bars, the rule-counts. Drill-throughs from any of those land
back here. **The DDL row is the atomic unit of the system.**

## What the new Org Overview is designed to do

Org Overview brings the DDL into the live system as the **bottom of an
analytics funnel**. It has three layers:

### 1. See / compare organizational accomplishment

The dashboard at `/org-overview` opens with KPI tiles, a stacked bar
chart, and a breakdown table that operate at whatever scope you pick:

* **Statewide** — the chart rolls up to the 10 districts (plus Central
  Office). Use this to see "which districts are pulling their weight"
  at a glance.
* **District** — pick one or more districts. The chart shows individual
  orgs within those districts.
* **Org** — pick specific orgs (county HQs, equipment shops, etc.) and
  compare them directly.

Every view accepts a date range and an optional activity filter, so
you can ask things like "show me April 2025's pothole patching costs by
district" without leaving the page.

### 2. Drill into specific filters

The chart and breakdown table are **navigation surfaces**. Click a
district segment in the bar chart, click an org row in the breakdown,
click a cell in the org × week pivot, click any row in the by-bucket
tab — every one of those interactions takes you to the DDL page with
the right filters preset (date range narrowed to the bucket, orgs
narrowed to the segment, activity preserved). The browser back button
returns you to the dashboard with your previous context intact.

The filter strip on the DDL page itself lets you broaden or narrow
further: change the date range, swap the org list, pick a different
activity. The filter state is in the URL so any view can be shared as a
link.

### 3. Consume DDL records

This is the bottom of the funnel. The DDL grid at
`/org-overview/ddl` is the same per-line-with-perc-allocation view the
DDL has always meant — but it's live, sortable, paginated, and
clickable. Each row has:

* All the validation flags (errors and warnings, with hover-explain
  tooltips), filterable via a "Rules" popover that surfaces per-rule
  occurrence counts for the active window
* A "cost mix" stacked-bar cell so you can see at a glance whether a
  row is mostly labor, mostly equipment, or mostly material
* The Task # cell hyperlinks straight to the underlying Task in this app
* Click a row to open a side drawer with the **constituent records**:
  every accomplishment line item (with its perc), every labor / equipment
  / stockpile / other transaction, in tabs

This is the layer where the analytics terminate. Charts and tables are
sums of these rows; clicking down through the funnel always lands here.
Anything that wants to get to the asset-level transaction is some path
through DDL.

### 4. Debug issues or errors

Because the DDL grid carries the validation engine, this is also the
**operational quality tool**. The "Only issues" checkbox restricts to
flagged rows; the rule popover narrows further to specific rule kinds
(e.g. "show me every State Forces accomplishment with zero labor cost
in this month"). The day-level filter rejects JV'd-to-zero task-days
so corrections don't appear as ghost rows. Daily-production thresholds
catch unit/data-entry mistakes (e.g. an accomp 50× the standard, which
is almost always a wrong unit).

In other words: instead of digging through DTIMS one unsorted record
at a time, a district maintenance supervisor can filter to their orgs,
flip on Only issues, page through the flagged rows directly with
arrow keys, see the constituent transactions in the drawer, and click
through to the underlying Task to fix it.

---

## Quick navigation map

```
/org-overview                — dashboard (KPIs · stacked chart · breakdown tabs)
   │
   ├── click chart segment    ─┐
   ├── click breakdown row    ─┤── all push to:
   └── click bucket-tab row   ─┘
                                │
                                ▼
/org-overview/ddl              — DDL grid (filters, rule filter, only-issues,
                                 sortable, ←/→ to page)
   │
   └── click row              → side drawer with constituent records
                                (Accomplishments · Labor · Equipment ·
                                 Stockpile · Other)
                                │
                                └── "Open Task" → /mms/tasks/<task_id>
```

## Key data sources

| What | Where |
|---|---|
| Tasks, orgs, activities, account codes | `operations.task` and friends |
| Accomplishment | `operations.daily_work_report_line_item` |
| Cost (post-OASIS-charging) | `operations.base_transaction` + `*_transaction` children, summed nightly into `operations.mv_task_day_costs` |
| Standard daily production (validation thresholds) | `operations.performance_standard_effective` |
| Annual work plan (planned vs actual) | `operations.annual_work_plan*` (used elsewhere; not central to DDL itself) |

---

## What's coming next: editing data from inside the app

Today the corrections loop is read-only here and edit-only in DTIMS,
which means flagged rows still have to be hand-corrected one at a time
in the upstream system — which, as noted above, is itself a slog.
The new direction is to bring the corrections workflow into the same
screen where the issue is found.

There are two intended editing modes:

**1. Inline DDL edits** — clicking a flagged DDL row opens the
constituent-records drawer. The next step is to make the rows in those
tabs editable: fix a labor entry's hours, swap an asset reference,
correct an accomplishment unit, mark a record as "JV submitted", etc.
The same validation engine that flagged the row re-runs after each save
so the user sees the issue clear in place.

**2. Bulk / batch edits** — once a "Rules" filter narrows the grid to
"every State Forces accomplishment with zero labor cost in March", the
operator should be able to apply a fix or response code to all the
selected rows at once. Same idea as bulk-marking emails — multi-select,
choose action, apply.

Both modes are opt-in by permission; the read-only DDL grid you see
today is the foundation.

## A rule that has never been checked

None of the existing tooling validates a reported accomplishment
against the activity's standard daily production. DTIMS doesn't, and
the audit-pass tooling doesn't. The new validation layer adds two such
checks by joining each row to its `EffectiveActivityDefinition`:
`>2× standard daily production = warning` and `>20× = error`.

This catches things nothing else can: a paving crew that reported
1,500 tons on a single day when the standard is 75 tons is almost
certainly a unit confusion (someone typed yards-cubed, or fat-fingered
a zero), and that mistake silently inflates the activity's reported
productivity for the whole fiscal year. Until now the only way to find
it was to spot a suspicious number by eye.

## How much accomplishment lives on the >20× rule's flagged rows?

The numbers below are scoped to the **accomplishment >20× standard
daily production** error specifically (rule ID `DAILY_PROD_ERROR`) —
rows where the reported per-line accomplishment exceeds the
activity's standard daily production by more than 20×. This is the
new check, and the one where a single bad row can move an activity's
productivity number disproportionately. The other rules (no route, no
labor/equipment, hours skew, SRIC season) are excluded from these
counts.

Whole dataset on this DB (2024-06-10 → 2026-09-16, the full DWRLI
date range), twelve sample maintenance activities. Accomplishment
numbers are in each activity's reported unit (TN, MI, EA, …); the
**percentage** is what's comparable. Where the DB has no current
`performance_standard_effective` row covering a date,
`EadLookup.find()` falls back to the most-recent prior EAD for the
same `(org, activity)` so the rule still fires across the full
window.

| Act | Description | Total accomp | Accomp on 20× rows | % | Rows | 20× rows |
|---|---|---:|---:|---:|---:|---:|
| 200 | Pothole Patching | 55,980 | 4,211 | **7.5%** | 12,983 | 1 |
| 201 | Patching Bituminous Pavements | 86,441 | 502 | **0.6%** | 18,466 | 1 |
| 260 | Stabilization — Shoulders | 283,577 | 0 | 0.0% | 9,481 | 0 |
| 261 | Stabilization — Roadway | 944,628 | 0 | 0.0% | 42,741 | 0 |
| 262 | Ditching & Blading — Unpaved Roadway | 8,274 | 682 | **8.2%** | 7,702 | 6 |
| 263 | Blading — Unpaved Roadway | 6,565 | 320 | **4.9%** | 6,165 | 2 |
| 287 | Removing Ditchline Obstacles | 4,359,323 | 273,388 | **6.3%** | 8,294 | 10 |
| 288 | Pulling Shoulders / Ditches Paved Roadway | 27,849 | 7,506 | **27.0%** | 15,947 | 17 |
| 303 | Mowing — Non-Expressway | 193,498 | 22,771 | **11.8%** | 60,254 | 10 |
| 307 | Herbicide Spraying | 56,377 | 46,080 | **81.7%** | 1,605 | 8 |
| 317 | Mowing — Expressway | 65,924 | 0 | 0.0% | 5,899 | 0 |
| 318 | Canopy Clearing | 518 | 40 | **7.8%** | 3,976 | 5 |
|   | **Total across these 12** | **6,088,953** | **355,500** | **5.8%** | **193,513** | **60** |

The shape this draws out is the whole reason for adding the rule:

* **Tiny number of rows, outsized share of accomplishment.** Just
  **60 rows out of 193,513** account for 355,500 reported units —
  over a third of a million units of accomplishment riding on
  three-hundredths of a percent of the row count. *Herbicide Spraying*
  (307) is the most extreme: 8 rows account for **81.7%** of the
  activity's entire reported volume across the dataset. *Pulling
  Shoulders / Ditches* (288) is right behind: 17 rows pull 27.0%.
  *Mowing Non-Expressway* (303) and *Removing Ditchline Obstacles*
  (287) each show 10 rows accounting for 12% and 6% of their
  respective activity totals. These are exactly the rows where one
  unit confusion or a stray zero meaningfully bends the productivity
  number for the whole activity.
* **Nothing else in the stack flags these.** DTIMS accepted them on
  the way in. Without a join to `EffectiveActivityDefinition` there's
  no per-activity ceiling to compare against, so the rows pass every
  structural check (route is filled, labor + equipment are charged,
  hours match) and look fine. They're usually a unit confusion
  (somebody typed yards-cubed, or fat-fingered an extra zero), and the
  inflation lives in the productivity numbers until someone notices
  by eye.
* **Some activities show 0** — Stabilization (260, 261) and Mowing
  Expressway (317). The rule doesn't catch every activity, and for
  these the standard daily production is high enough that nothing in
  the dataset tripped 20×. That's the right behavior: the rule should
  fire when something is obviously wrong, not on edge cases.

### Concrete example — what a 20× row actually looks like

Activity 303 (Mowing, Non-Expressway) reports in **shoulder miles**.
The standard daily production is **8.5 shoulder miles / day** — what
a single mowing crew with a tractor and a flagger can realistically
finish in a regular workday. The ten rows the rule flagged across
the whole dataset; the six worst:

| Date | Task # | Org | Route | Reported | × standard |
|---|---|---|---|---:|---:|
| 2025-07-28 | 260502303006 | 0502 | Berkeley CR 1 | **7,822.8 shoulder miles** | **920×** |
| 2025-07-08 | 260108303001 | 0108 | Clay CR 13/7 | 6,043.0 | 711× |
| 2025-10-15 | 260704303007 | 0704 | Braxton CR 19/48 | 5,384.0 | 633× |
| 2024-08-19 | 250502303409 | 0502 | Berkeley CR 7 | 1,394.0 | 164× |
| 2024-09-09 | 250206303253 | 0206 | Cabell CR 32 | 726.0 | 85× |
| 2025-06-24 | 250127303158 | 0127 | Mason WV 62 | 336.0 | 40× |

The top row says **one crew on Berkeley CR 1 mowed 7,822.8 shoulder
miles on July 28, 2025**. At the 8.5-mile-per-day standard, that
would represent **920 working days** of mowing — close to four full
calendar years of continuous mowing — done in a single calendar day.
Berkeley County has roughly 620 centerline miles of road total, so
the row claims more than ten times the entire county's road network
was mowed in a single shift.

This is almost certainly one of two things, both correctable in
seconds if you can see the row:

1. **A unit confusion** — the crew reported a *cumulative* number
   (e.g. total shoulder-feet for the season, or a project running
   total) on a single day's report, or filled in a different unit
   from the one the system expects.
2. **A data-entry slip** — an extra digit (the right number was
   78.23 or 782.28, not 7,822.8).

Either way, until somebody catches it the activity's productivity
math looks like this: this single row alone contributes 4.0% of
mowing-non-expressway's **entire reported volume on this database**
across more than two years of accomplishments. DTIMS accepted it on
entry, no audit tool has a rule to catch it, and the structural
checks all pass (route filled, labor charged, equipment charged,
hours match) — so today it's invisible until a manager notices by eye
that the productivity number is wrong.

The new validation surfaces it as an error with a clear rule
("Accomplishment is 920× standard daily production (8.5/day)"), and
the click-through-and-fix workflow (planned next) is what closes the
loop: open the row, change `7822.8` to `78.23` or whatever the right
value is, hit save, and the row clears.

These 60 rows across 12 activities are exactly the kind of
fix-target the edit-in-place workflow is built for.
