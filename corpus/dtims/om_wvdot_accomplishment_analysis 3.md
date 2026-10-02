# OM_WVDOT — Accomplishment & Data-Entry Analysis

*Source: live Deighton dTIMS production backend `OM_WVDOT` (read-only via the
TAMSDW linked server). All figures are current rows (`ValidTo IS NULL`) unless
noted. Generated 2026-06-25.*

---

## Executive summary

- **What an "accomplishment" is:** the unit of work logging in OM_WVDOT is the
  `DailyWorkReportLineItem` (**637,047** current rows). The `AccomplishmentEntry`,
  `Task_Accomplishment`, and `DailyWorkReport` *header* tables are empty/demo —
  the line items **are** the entries. They carry the task, the route/milepost,
  the accomplishment quantity, the creating user, and a real creation timestamp.
- **~1 in 3 accomplishments has no asset.** **223,249 of 637,047 (35%)** are
  entered with **no AssetReference** — they're logged straight against a task
  with nothing tying them to a road, bridge, or location.
- **These cluster almost entirely in administrative / overhead activities.**
  Field work (mowing, patching, stabilization, ditching) is ~0–3% asset-less;
  the **800-series "overhead" activities are 72–96% asset-less.**
- **"Blanket tasks" are a real, large pattern.** 8,242 current tasks (7.3%) have
  **no asset** at all, and they behave as *buckets*: **5,754 of them absorb
  3.94M labor hours — ~36% of all labor hours in the system** — at **~685
  hours per task** vs **75 hours** for an asset-linked task.
- **Activity 801 ("Organizational Overhead – Maintenance")** is the textbook
  case: **66,605 accomplishments, 92% with no asset, spread over just 415
  tasks** (~160 accomplishments per task). One single overhead task (#12040)
  holds **1,749** accomplishments, every one asset-less.
- **Data entry happens in short daily "waves."** Across **50,627 user-days**
  (402 distinct users) and **all** accomplishments — blanket *and* asset-linked
  tasks — a typical session is **~10 entries in ~9 minutes**; **66% of sessions
  finish in under 30 minutes.** But there's a heavy tail — **18% of sessions run
  over 2 hours** (someone clearing a backlog), and the busiest users log
  7,000–11,000 accomplishments across 280–446 working days.
- **About 101 distinct users make entries on a typical working day** (median 105,
  range ~90–113, max 123) — roughly **a quarter of the 402-user roster active
  daily** — entering ~1,266 accomplishments/day. *(Note: employee-hours/labor
  rows are deliberately excluded from "data entry" — all 2,844,759 of them were
  created by a **single system account**, i.e. the cost integration bulk-loads
  them; they are not typed by users.)*

**On cost (§7):**

- **≈ $972M net actual spend (~$480M/yr) — but ≈ $1.85B gross.** There are
  **576,993 negative transactions totaling −$873M**; *half of all dollar activity
  is offsetting reversals.* Counting gross ledger value overstates real spend ~90%.
- **The biggest cost category is "Other" — and it's mostly an accounting
  construct.** $1.18B gross → **$360M net**, with **42% of its transactions
  negative**: contract orders (`ADO`) + journal vouchers (`JVC`) booked
  gross-then-reclassified. Real composition is ~37% contracts / 34% labor / 17%
  equipment / 12% materials.
- **Paving ($184M) is the single biggest activity**; a **retired code still posts
  $26M.** **A third of all spend ($330M) lands on "blanket" no-asset tasks**
  (6,684 buckets at ~$49k each, 7× a normal task) — and ~$186M of that is *field*
  work (mainly SRIC surface treatment) simply not tied to a road, not overhead.
- **Materials are violently seasonal (winter salt): ~$2–3M/month summer →
  $11–13M each January** (~$45M/winter), while total spend stays flat.
- **Blended loaded labor rate ≈ $30.6/hr.** Labor is constantly fixed: **10% of
  labor transactions are negative corrections** (TADJ adjustments). **Estimates
  barely exist** ($4.3M, only ~3 weeks ahead) — this is a recording ledger, not
  a forecasting one.

**On asset-on-demand (§8):**

- **~10% of asset-linked accomplishments are "fast followers"** — the asset was
  created **within the hour** before the entry (**6% within the same 10-minute
  sitting**, ~30% within the day). The rest reuse standing assets (51% more than
  a week old). For **single-use** assets the coupling is far tighter (60% same
  day). **73% of all assets ever created are used exactly once** — the asset
  inventory is overwhelmingly single-purpose, minted per task as work is logged.
- **On-demand asset creation concentrates in *reactive* work** — herbicide (24%),
  hazard trees (24%), debris (20%), potholes (18%) — where the location isn't
  known until the crew is on site; routine/planned work reuses known segments.
- **It's a per-user habit, not a system norm:** the median user fast-follows just
  **3%** of the time, but **8% of users do it ≥30%** (one **98%**) while **61%
  almost never** — and **asset creation rides the same afternoon human entry
  curve**, so these assets are minted live, mid-session.
- **Same-session, proven two ways:** of accomplishments whose asset was created
  the same day, **36% had the asset minted inside the user's own session window**.
  And **60% of multi-asset tasks are scoped upfront** while ~40% accumulate assets
  over time — the task-level shadow of "add it when you need it."

**On cost-without-accomplishment (§9):**

- **A quarter of all spend — $251M (26%) — sits on tasks with cost but ZERO
  accomplishments**, and **73% of it is contract invoice ("Other")**. You cannot
  infer "work done" from "money spent" on ~¼ of the ledger.
- **Paving (210) is the poster child: $92.9M, 100% contract, no accomplishments**;
  followed by embankment (412, $42M) and a *retired* code still invoicing $22.5M.
  A second flavor is **equipment/admin overhead (811, $56M, 0% contract)** — fleet
  charges with no field output. Single tasks hold **$1–3M of pure invoice with no
  labor and no work-report** (e.g. task 94799 = $2.84M).
- **Even where an accomplishment exists it's often a stub** — paving tasks
  carrying **$2.6M against a single token accomplishment** — so the real
  "cost-without-work-report" total exceeds the $251M zero-accomplishment figure.

---

## 1. Scope & data model

| Entity | Table | Rows (current) | Role |
|---|---|--:|---|
| Accomplishment | `operations.DailyWorkReportLineItem` | 637,047 | one logged line of work |
| Task | `operations.Task` | 112,987 | the work record an accomplishment hangs on |
| Activity | `operations.PerformanceStandard` | 122 | e.g. `801 = ORGANIZATIONAL OVERHEAD` |
| Asset link | `operations.TaskAssetReference` | 269,581 | task ↔ road/bridge/asset |
| Employee hours | `operations.LaborTransaction` | 2,844,759 | labor, **keyed to TaskId** |

**Key linkages used (verified against the data, not assumed):**
- Activity of an accomplishment = `DWRLI.TaskId → Task.PerformanceStandardCodeId
  → PerformanceStandard.Code`. *(The `DWRLI.PerformanceStandardId` column is
  populated on only 1 of 637,047 rows — activity lives on the task.)*
- Asset of an accomplishment = `DWRLI.AssetReferenceId` (null = no asset).
- A **blanket task** = a `Task` with **no** `TaskAssetReference` row.
- Labor ties to **TaskId** (the `DailyWorkReportLineItemId` link on
  `LaborTransaction` is 100% null), so "employee hours" roll up by task/activity.

---

## 2. Activities — where the work (and the logging) goes

Top activities by number of accomplishments, with the share entered **without an
asset** ("blanket"):

| Code | Activity | Accompl. | No-asset | Blanket % | Tasks |
|---|---|--:|--:|--:|--:|
| **801** | **Organizational Overhead – Maint.** | **66,605** | **61,601** | **92%** | **415** |
| 303 | Mowing – Non-Expressway | 66,415 | 30 | 0% | 13,583 |
| 341 | Application of Solid SRIC Mat'l | 41,605 | 22,377 | 54% | 565 |
| 261 | Stabilization – Roadway | 36,859 | 47 | 0% | 11,046 |
| 382 | Bridge Inspection & Analysis | 32,209 | 7,479 | 23% | 8,116 |
| 345 | SRIC Support Operations | 26,583 | 21,586 | 81% | 274 |
| **817** | **SWAT / Citizen Requests** | 19,945 | 18,425 | **92%** | 338 |
| 308 | Litter Pickup & Disposal | 18,706 | 469 | 3% | 853 |
| 200 | Pothole Patching | 18,633 | 6 | 0% | 2,835 |
| **816** | **Buildings & Grounds** | 18,418 | 17,309 | **94%** | 531 |
| 304 | Brush Control – Hand | 17,606 | 223 | 1% | 5,615 |
| **818** | **Core Maintenance Planning** | 17,339 | 12,417 | **72%** | 687 |
| 281 | Minor Drainage Structures | 15,564 | 152 | 1% | 4,249 |
| 288 | Pulling Shoulders / Ditches | 15,116 | 7 | 0% | 3,355 |
| **809** | **Training – Annual Plan Personnel** | 14,994 | 14,332 | **96%** | 394 |

**The split is categorical, not gradual.** "Doing something to a road" is
recorded against an asset ~100% of the time. "Overhead, training, citizen
requests, buildings, planning, equipment transport" — the 800-series and a few
support activities — are recorded against nothing ~70–96% of the time. That's
expected: there's no road to point training or overhead at. The data is
behaving sensibly; the blanket entries are **non-field time being parked on a
catch-all task.**

---

## 3. Blanket tasks — the "bucket" pattern

**Two views of "no asset":**

| Grain | With asset | No asset (blanket) | Blanket % |
|---|--:|--:|--:|
| Accomplishments (DWRLI) | 413,798 | 223,249 | **35%** |
| Tasks | 104,745 | 8,242 | **7.3%** |

**Why so few blanket *tasks* but so many blanket *accomplishments*:** the
blanket tasks are **buckets**. A handful of standing tasks per organization per
overhead activity absorb a whole year of everyone's non-field time.

**Labor hours confirm the concentration:**

| | Labor txns | Hours | Tasks | Hours/task |
|---|--:|--:|--:|--:|
| Blanket tasks | 1,135,980 | **3,939,683** | 5,754 | **685** |
| Asset tasks | 1,706,649 | 6,906,292 | 92,327 | 75 |

Blanket tasks are **0.6% of "labor-bearing" tasks but soak up 36% of all labor
hours.** A blanket task carries **~9× the hours** of a normal asset task.

**The biggest buckets (single tasks with the most accomplishments dumped on
them):**

| Task | Activity | Accompl. | No-asset |
|---|---|--:|--:|
| 12040 | 801 Organizational Overhead | 1,749 | 1,749 |
| 47741 | 341 Application of Solid SRIC | 1,678 | 0 |
| 96463 | 341 Application of Solid SRIC | 1,363 | 0 |
| 48912 | 345 SRIC Support Operations | 1,201 | 1,201 |
| 48897 | 341 Application of Solid SRIC | 924 | 924 |
| 78232 | 801 Organizational Overhead | 917 | 917 |

**Blanket tasks by activity (count of asset-less tasks):** Buildings & Grounds
(625), Solid-SRIC application (412), Equipment Transporting (391), **Organizational
Overhead 801 (386)**, Training (382), Snow Plowing (327), Sign Maintenance (327),
Materials Handling (313), Core Maint. Planning (305), SWAT/Citizen (253).

> **Read:** "blanket task" = a standing, location-less task — one per crew per
> overhead category — that the crew charges hours and daily entries against all
> year. Activity **801** is the purest example: a few hundred overhead buckets
> holding 66,605 entries and essentially no asset linkage.

---

## 4. Data-entry behavior — the daily "waves"

> **Scope of this section:** it covers **every** accomplishment entry — on
> blanket *and* asset-linked tasks (the full 637,047 DWRLI), not just the
> overhead buckets from §3. It **excludes** the labor / employee-hours rows: all
> **2,844,759** of those were created by a **single system account** (the cost
> integration loads them), so they are machine-imported, not human data entry,
> and including them would distort the burden (their "sessions" would be
> million-row bulk inserts, not typing).

Across **50,627 user-days** and **402 distinct users**, looking at each user's
first-to-last entry on a given day (sessions of ≥3 entries = 45,377):

| Metric | Median | p75 | p90 | Max |
|---|--:|--:|--:|--:|
| Entries per session | 10 | 17 | 26 | 858 |
| Session length (min) | **9** | 68 | 215 | — |
| Entries per minute | 0.66 (~91 s apart) | — | — | — |

- **A typical data-entry wave is ~10 entries in under 10 minutes** (~one entry
  per minute — about the pace of typing a route, milepost, quantity and labor).
- **66% of sessions finish in under 30 minutes; 74% under an hour.**
- **But 18% of sessions exceed 2 hours.** These are the backlog-clearing
  marathons — a clerk entering a whole crew's week, up to 858 entries in a
  sitting. The median's 9 minutes and the p90's 3.5 hours describe a strongly
  **bimodal** workflow: quick daily touches vs periodic catch-ups.

**Heaviest data-entry users** (by total accomplishments authored):

| Total | Active days | Median/day | Median session (min) | User (app id) |
|--:|--:|--:|--:|---|
| 10,893 | 389 | 21 | 44 | 00ug37bi… |
| 9,985 | 365 | 21 | 26 | 00ug2n0d… |
| 8,745 | 405 | 20 | 102 | 00uga7ri… |
| 8,450 | 279 | 13 | ~0* | 00ug884n… |
| 8,038 | 298 | 21 | 26 | 00ug88vo… |
| 7,987 | 427 | 17 | 25 | 00ufnoso… |
| 7,741 | 412 | 15 | 77 | 00ufxbu7… |
| 7,319 | 446 | 16 | 134 | 00ufvais… |
| 6,597 | 223 | 23 | 143 | 00ums5c9… |

\* a near-zero median session means most of that user's entries land at a single
timestamp per day — i.e. **bulk paste / import-style entry** rather than typed
one at a time.

**Two clear personas emerge:**
- **Typists** (median session 25–45 min, ~20/day) — entering steadily through
  the day as work happens.
- **Batchers** (median session ~0–15 min but high daily volume, or 100–143 min
  marathons) — entering many lines in one burst, likely transcribing paper
  timesheets for a crew.

---

## 5. Cadence — when the work is logged

**By weekday** (clean Mon–Fri business pattern; weekends are near-zero):

| Day | Accomplishments |
|---|--:|
| Mon | 123,852 |
| Tue | 133,705 |
| Wed | 126,999 |
| Thu | 127,544 |
| Fri | 116,130 |
| Sat | 2,764 |
| Sun | 3,488 |

**By hour of day** (Eastern): essentially nothing overnight, ramping from
~10–11am, **peaking 12pm–2pm**, then a long decline through the evening to ~8pm
— crews logging the day's work in the afternoon/after the shift. This curve is
what confirms `CreatedOn` reflects **genuine human entry time**, not a batch load.

**By day:** a normal weekday sees **~1,300–2,100 accomplishments entered by
~95–110 active users.** Recent weekdays (mid-June 2026) hold steady in that band;
weekend days drop to single digits. The system is in active, daily production use.

### Users making edits per day

Averaged over **496 working days** (weekdays with real activity):

| Distinct users entering data / working day | Value |
|---|--:|
| **Average** | **101** |
| Median | 105 |
| 10th–90th percentile | 90 – 113 |
| Max | 123 |
| Avg accomplishments entered / working day | 1,266 |

Against a roster of **402 users who have ever made an entry**, **~101 active on a
typical day ≈ a quarter of the user base in the system each working day.** That's
a **broad, distributed workload** — about a hundred field/clerical users each
doing a short daily wave — not a handful of heavy data-entry clerks carrying the
system. (This counts *human accomplishment entry*; the labor/cost rows are
excluded, per §4, because they're loaded by one integration account.)

---

## 6. What it means

1. **A third of all accomplishment entries — and over a third of all labor
   hours — are "blanket": time parked on location-less overhead tasks.** This is
   structurally driven by the activity catalog (overhead/training/citizen/
   buildings have no asset to attach to), not by sloppy entry on field work.
2. **Activity 801 and its 800-series siblings are the catch-alls.** If the goal
   is to push more hours onto asset-attributed work, the lever is the overhead
   activities, not mowing/patching (which are already ~100% asset-linked).
3. **The blanket tasks are few but enormous** (~685 hrs each). They function as
   per-crew annual buckets; any costing or productivity analysis should treat
   them separately from real asset work.
4. **Data entry is a light daily habit for most (≈10 lines / <10 min) with a
   batch-entry minority.** There is no evidence of a heavy nightly data-entry
   burden per user — the load is spread across ~100 users doing short waves,
   with occasional multi-hour catch-up sessions.

---

## 7. Cost deep-dive — where the money goes

*Cost ledger = `BaseTransaction` (5.2M rows) subtyped into Labor / Equipment /
Stockpile (materials) / Other. "Actual" = `Confirmed = 1`; figures are **net**
(positives + reversals) unless I say "gross."*

### 7.1 The headline — and a $873M illusion

**Net actual maintenance spend is ≈ $972M** across the live period (real
operations from **FY-start July 2024** through mid-2026 — roughly **$480M/year**).
But that net hides enormous churn:

| | Amount |
|---|--:|
| Gross **positive** transactions | **≈ $1.845 B** |
| Gross **negative** transactions (576,993 of them) | **−$873 M** |
| **Net actual** | **$972 M** |

**Nearly half of all dollar activity is offsetting reversals.** Any analysis that
counts gross transaction value (or transaction *count*) overstates real spend by
~90%. This matters for anyone sizing workload or cost from raw ledger rows.

### 7.2 Cost composition — "Other" (contracts) is the biggest bucket

| Type | Net actual | Share | Gross positive | Reversals | % txns negative |
|---|--:|--:|--:|--:|--:|
| **Other (contracts/JV)** | **$359.9 M** | **37%** | $1,178.9 M | −$819.0 M | **42%** |
| Labor | $332.2 M | 34% | $373.9 M | −$41.7 M | 10% |
| Equipment | $163.7 M | 17% | $170.3 M | −$6.7 M | 2% |
| Materials (stockpile) | $116.7 M | 12% | $122.5 M | −$5.8 M | 4% |

**The single most interesting structural fact in the ledger:** the largest cost
category isn't labor or equipment — it's **"Other," and it's almost entirely an
accounting construct.** Its line items are **`ADO – DOT…` (contract / detail
orders)** and **`JVC – …` (journal vouchers)**; **$819M of its $1.18B gross is
reversed out** via JV reclassifications, leaving **$360M of real contract cost**
buried inside a 3.2×-larger pile of offsetting entries. A single ADO contract
shows up as 80–125 separate lines, repeatedly posted and reversed across
accounts.

> **Read:** WVDOT books contract/financial costs gross-then-reclassify. The
> "Other" category is where the books are balanced, not where work is described.

### 7.3 Where the work money goes — activities

Net actual spend by activity (top of ~120):

| Code | Activity | Net actual | Tasks | $/task |
|---|---|--:|--:|--:|
| **210** | **Paving** | **$183.6 M** | 926 | **$198 k** |
| 341 | Application of Solid SRIC (surface treat.) | $113.2 M | 587 | $193 k |
| 811 | Administrative Cost for Equipment | $56.9 M | 207 | $275 k |
| 261 | Stabilization – Roadway | $48.9 M | 11,408 | $4.3 k |
| 412 | Embankment Stabilization | $46.6 M | 706 | $66 k |
| 200 | Pothole Patching | $40.6 M | 3,265 | $12 k |
| **801** | **Organizational Overhead** | **$37.3 M** | 469 | $79 k |
| 345 | SRIC Support Operations | $34.1 M | 282 | $121 k |
| 318 | Canopy Clearing | $26.7 M | 342 | $78 k |
| — | **`RETIRED – 413` (still posting!)** | **$26.0 M** | 156 | — |
| 303 | Mowing – Non-Expressway | $21.5 M | 13,674 | $1.6 k |

**Paving is the single biggest line ($184M)** at ~$198k/task — a few hundred big
jobs. Contrast **Mowing**: $21M across **13,674** tasks at $1.6k each — death by a
thousand cuts. **A retired activity code (`RETIRED – 413`) is still carrying
$26M** — a data-governance flag worth chasing.

### 7.4 Overhead & "blanket" spend — the money version

Two different cuts of "non-asset" cost, and they tell different stories:

| Cut | Net actual | Tasks | $/task |
|---|--:|--:|--:|
| **Blanket tasks** (no asset attached) | **$330.5 M (34%)** | 6,684 | **$49 k** |
| Asset-linked tasks | $639.2 M (66%) | 94,548 | $6.8 k |
| — | | | |
| **800-series** (overhead/admin activities) | **$144.0 M (15%)** | — | — |
| Field activities | $825.6 M (85%) | — | — |

- **A third of all spend — $330M — lands on "blanket" tasks with no asset
  attached**, concentrated in **6,684 bucket tasks at ~$49k each (7× a normal
  asset task).**
- But only **$144M of that is true overhead/admin** (800-series). The other
  **~$186M is *field* work logged with no asset** — overwhelmingly the
  **SRIC surface-treatment family** (341 is 54% blanket, 345 is 81% blanket).
  So it isn't all "overhead"; a large chunk is **real material/contract work that
  simply isn't being tied to a road.** If asset-level cost attribution matters,
  the SRIC activities are the biggest leak, not the overhead codes.

### 7.5 Seasonality — the winter-salt signal

**Total** monthly spend is remarkably flat (~$32–64M/month). **Materials, however,
are violently seasonal** — the de-icing cycle is unmistakable across both winters:

| Season | Materials $/month |
|---|--:|
| Summer (Jul–Sep) | **$2–3 M** |
| Ramp (Oct–Dec) | $1.7 M → $9.6 M |
| **Peak (Jan)** | **$11.5 M (2025), $13.1 M (2026)** |
| Late winter (Feb–Mar) | $10–11 M |
| Thaw (Apr–May) | back to $3–6 M |

Each winter pushes **~$45M of de-icing material** through the ledger — a **4–5×
swing** that labor and equipment smooth over (people and trucks are paid year
round; salt is not). This is the clearest operational rhythm in the data.

### 7.6 Rates, churn, and quality

- **Blended loaded labor rate ≈ $30.6/hour** ($332.2M labor ÷ 10.85M hours).
- **Cost per accomplishment entry ≈ $1,526** ($972M ÷ 637K) — but that average is
  meaningless on its own given the paving-vs-mowing spread above.
- **Labor is constantly corrected:** **10% of all labor transactions are negatives**
  (276,013 reversals, −$42M) — small individual timesheet/account adjustments
  (the TADJ mechanism), a steady background hum of fixes.
- **154,750 zero-cost actual transactions** sit in the ledger (≈3%), plus the
  `RETIRED – 413` $26M noted above — modest but real data-hygiene items.
- **Estimates barely exist:** only **$4.3M** of estimate (`Confirmed = 0`) cost,
  **all dated within ~3 weeks ahead** (2026-06-13 → 07-06). The system is used as
  a *recording* ledger, **not for forward cost forecasting** — there is no
  long-range estimate book to compare actuals against.

---

## 8. Asset-on-demand — is the accomplishment a "fast follower" of the asset?

**The question:** when a crew logs an accomplishment, was the asset already on
the task, or did they **add the asset on the spot** to support that entry — the
accomplishment as a *fast follower* of the asset?

**Why it's hard, and the signal that makes it possible:** `AssetReference` has no
`CreatedById`/`CreatedOn`. But it carries a **`ReferenceDate`** that is **100%
populated with millisecond-precision system timestamps** (range 2024-06 → 2026-06).
The give-away that it's a real *creation* stamp, not a user-entered "as-of" date:
**some accomplishments reference an asset within ~2 minutes of its ReferenceDate**
— impossible unless the stamp is system-set at creation, inside the same entry
session. Combined with the fact that asset references are **≈1:1 with task links**
(each task gets its own refs), "a new AssetReference" ≈ "an asset added to a
task." That gives two independent angles.

### 8.1 Structural — most "added" assets are used exactly once

413,798 asset-bearing accomplishments draw on **210,147 distinct assets** (1.97
accomplishments per asset):

| Accomplishments referencing the asset | Assets | Accomplishments |
|---|--:|--:|
| **1 (single-use)** | **153,534 (73%)** | 153,534 |
| 2 | 28,974 | 57,948 |
| 3–5 | 18,570 | 66,859 |
| 6–10 | 5,447 | 40,193 |
| 11+ (standing reused) | 3,622 | 95,264 |

**73% of assets are single-use** — created, used by exactly one accomplishment,
never touched again. That is the structural fingerprint of "added as needed for
this entry." At the other end, a small core of **3,622 standing assets absorbs
95,264 accomplishments** — the reused road segments (mow this stretch 12×/year).

**Single-use and "fast follower" overlap but aren't the same thing** (cross-tab):

| | Single-use asset | Multi-use asset |
|---|--:|--:|
| Fast (≤ 1 hr) | **31,023** | 10,921 |
| Not fast | 121,683 | 247,606 |

**74% of fast-followers are single-use** (the asset is minted, used once, gone) —
but **only 20% of single-use assets are fast.** So most single-purpose assets
are *pre-created and used once later*, not minted in the moment. The two lenses
agree on the workflow but measure different slices of it.

### 8.2 Temporal — the fast-follower gap

Gap = accomplishment `CreatedOn` − asset `ReferenceDate`:

| Gap (asset created → accomplishment entered) | All asset-acc. | Single-use assets |
|---|--:|--:|
| ≤ 2 min | 3.6% | 6.7% |
| ≤ 10 min (same sitting) | **6.0%** (cum) | **12.5%** (cum) |
| ≤ 1 hour | **10.2%** (cum) | **21%** (cum) |
| ≤ 24 hours (same day) | **30%** (cum) | **60%** (cum) |
| ≤ 7 days | 48% (cum) | 77% (cum) |
| > 7 days (standing/pre-existing) | **51%** | 21% |
| asset created *after* the accompl. (anomaly) | 1.3% | 1.7% |

**Reading the headline numbers:**
- **~1 in 10 asset-bearing accomplishments is a true fast follower** — the asset
  was created **within the hour** before the entry (~42,000 accomplishments).
- **~1 in 17 (6%) within 10 minutes** — the asset was added *in the same data-
  entry sitting* (~25,000 accomplishments).
- **~30% within the same day**; but **~51% reuse a standing asset** created more
  than a week earlier (routine work on known segments).
- **For single-use assets the coupling is far tighter** — **60% within a day,
  21% within an hour** — exactly what you'd expect from assets minted to carry a
  single piece of work.

### 8.3 Where it happens — reactive work creates assets on the spot

Fast-follower rate (asset created ≤1 hr / ≤24 hr before the accomplishment), by
activity (≥2,000 asset-bearing accomplishments):

| Code | Activity | Asset-acc. | ≤1 hr | ≤24 hr |
|---|---|--:|--:|--:|
| 307 | Herbicide Spraying | 2,290 | **24%** | 49% |
| 319 | Hazard / Impact-Threat Tree | 6,752 | **24%** | 49% |
| 818 | Core Maintenance Planning | 4,919 | 23% | 60% |
| 420 | Debris Removal | 5,585 | 20% | 56% |
| 200 | Pothole Patching | 18,627 | 18% | 39% |
| 262 | Ditching & Blading – Unpaved | 9,195 | 16% | 43% |
| 303 | Mowing – Non-Expressway | 65,338 | 15% | 42% |
| 261 | Stabilization – Roadway | 36,536 | 13% | 42% |
| 288 | Pulling Shoulders / Ditches | 14,988 | 10% | 27% |

**The on-demand pattern tracks how *predictable the location* is.** Reactive /
emergent work — **hazard trees, debris, herbicide, planning, potholes** — has the
highest fast-follower rates (you don't know the spot until you're there, so you
add it and log it). **Routine, planned work** (pulling shoulders, stabilization)
leans on standing assets and creates fewer on the fly.

### 8.4 Asset creation is *live and human*, not batch

If `ReferenceDate` were a bulk import it would clump at odd hours. It doesn't —
**asset creation follows the same human work-day curve as accomplishment entry**:

| Hour (ET) | Assets created |
|---|--:|
| overnight (0–8) | < 500/hr |
| 09–11 ramp | ~2k → 26k |
| **12–13 peak** | **41k / 38k** |
| 14–19 afternoon/evening | 16k–27k, tapering |
| 20–23 | 7k → 0.6k |

This is the §4 entry curve almost exactly. Assets are **minted by people, during
the afternoon/after-shift data-entry window** — which is what makes "the asset
was added in the same session as the accomplishment" a coherent claim at all.

### 8.5 It's a *per-user habit*, not a system-wide norm

Asset-on-demand is concentrated in a minority of users. Across 290 users with ≥50
asset-linked accomplishments:

| Per-user fast-follower (≤1 hr) rate | |
|---|--:|
| Median user | **3%** |
| 90th-percentile user | 29% |
| Max | **98%** |
| Users fast-following **≥30%** of the time | **24 (8%)** |
| Users who **almost never** (≤5%) | **176 (61%)** |

**Most users (61%) almost never create an asset on the fly** — they enter against
standing assets. But a **hard core of 24 users (8%) do it constantly** (one user
**98%** of the time). On-demand asset creation is a *behavior of specific
crews/clerks*, almost certainly the ones doing reactive field work (per §8.3),
not a uniform system practice. (This ties directly to the §4 "personas": the
on-demand users are live typists discovering locations as they go, not batch
transcribers working from pre-existing paperwork.)

### 8.6 Same-session proof — the asset is minted *mid-session*

The strongest test: of the accomplishments whose asset was created the **same
calendar day**, was that asset minted *inside the user's own entry-session window*
(between their first and last accomplishment that day)?

- **108,019** accomplishments had a same-day-created asset.
- **38,920 of them (36%)** had the asset's `ReferenceDate` fall **inside the same
  user's active session window** — i.e., the user created the asset *in the
  middle of the very session* in which they were logging accomplishments.

That's ~**9% of all asset-linked accomplishments demonstrably minting their asset
mid-session** — independent confirmation of the ≤1-hour temporal result from a
completely different angle (session windows rather than raw gaps).

### 8.7 At the task level — planned-upfront vs grown-incrementally

For the 24,435 tasks that carry **two or more** assets, how spread out (in time)
are those assets' creation dates?

| Spread of a task's asset-creation dates | Tasks | Share |
|---|--:|--:|
| **Same day (all added upfront)** | **14,652** | **60%** |
| Within a week | 3,389 | 14% |
| Within a month | 2,061 | 8% |
| 1–6 months | 3,650 | 15% |
| **6+ months (grown incrementally)** | 683 | 3% |

**60% of multi-asset tasks get all their assets in one shot** — planned/scoped
upfront. But **~40% accumulate assets over time**, and **~18% (4,333 tasks) grow
over a month-plus** — standing tasks (a route, a district program) that pick up
new asset references as the work reaches new spots. That long-tail incremental
growth is the task-level shadow of the same "add it when you need it" behavior.

### 8.8 Bottom line

Asset-added-as-needed is a **real, measurable, behaviorally-concentrated
workflow** that five independent angles all converge on:

1. **Timing** — ~10% of asset-linked accomplishments mint their asset within the
   hour (6% within the same 10-minute sitting), ~30% within the day.
2. **Session windows** — 36% of same-day-asset accomplishments had the asset
   created *inside the user's own active session*, ≈9% of all asset-linked
   entries minting an asset mid-session.
3. **Reuse** — 73% of all assets are single-use; 74% of fast-followers are
   single-use.
4. **People** — it's a habit of a hard core (8% of users do it ≥30% of the time,
   one at 98%) while 61% almost never; concentrated in reactive activities
   (herbicide, hazard trees, debris, potholes).
5. **Clock** — assets are created on the live human work-day curve, mid-session.

…**but it is the minority pattern.** The majority of work reuses standing assets,
60% of multi-asset tasks are scoped with their assets upfront, and most entries
fire against assets created days-to-weeks earlier. The deeper truth is a paradox:
*temporally*, tight fast-following is a slice (~10%); *structurally*, the asset
catalog is **overwhelmingly single-purpose** (73% used once) — assets are minted
per task as work is recorded, by a specific set of field crews, rather than
maintained as a durable reusable inventory. The org/district cut couldn't be
resolved cleanly (the `DWRLI.OrganizationId` link is unreliable, like the
activity column), so the *who/where* is characterized at the user and activity
level above rather than by district.

---

## 9. Cost without a work-report — the contractor / invoice gap

**The question:** where do you see a large amount of **cost** but the
**accomplishment you'd expect isn't there** — e.g. a massive invoice on a paving
job with no daily-work-report line? This is the cost-side mirror of everything
above: an accomplishment is what a *crew* logs; a contractor doesn't file one, so
their **invoice lands on the task with no accomplishment behind it.**

Joining every current task's **net actual cost** to its **accomplishment count**:

| | Tasks | Net cost |
|---|--:|--:|
| Cost-bearing tasks (net > 0) | 100,768 | $969.7 M |
| …**with cost but ZERO accomplishments** | **6,813 (7%)** | **$251.3 M (26% of all spend)** |
| …of that, "Other" (contract/invoice/JV) | — | **$184.6 M (73%)** |

**A full quarter of maintenance spend — $251M — sits on tasks that have cost but
no work-report**, and nearly three-quarters of it is contract/invoice money.
This is not an error; it's the structural seam between *crew work* (logged as
accomplishments) and *contracted work* (booked as invoices).

### 9.1 What's in the gap — by activity

| Code | Activity | Tasks | No-accompl cost | % Other |
|---|---|--:|--:|--:|
| **210** | **Paving** | 431 | **$92.9 M** | **100%** |
| 811 | Administrative Cost for Equipment | 205 | $56.3 M | **0%** |
| 412 | Embankment Stabilization | 285 | $42.2 M | 100% |
| — | `RETIRED – 413` (still invoicing) | 118 | $22.5 M | 100% |
| 318 | Canopy Clearing | 80 | $7.7 M | 99% |
| 421 | (drainage) | 23 | $3.5 M | 99% |
| 200 | Pothole Patching | 415 | $1.7 M | 77% |
| 261 | Stabilization – Roadway | 402 | $1.3 M | 48% |

**Two distinct kinds of "cost without accomplishment" fall out:**

1. **Contracted construction — the big one.** **Paving (210) is the textbook
   case: $92.9M of invoices, 100% "Other," zero accomplishments**, spread over
   431 tasks. Embankment stabilization (412, $42M), canopy clearing (318, $7.7M),
   and a *retired* code still invoicing $22.5M follow the same 99–100%-Other,
   no-work-report shape. These are **contractor jobs** — the work is real, the
   accomplishment line simply isn't WVDOT's to enter.
2. **Equipment/administrative overhead — a different animal.** **811
   "Administrative Cost for Equipment" is $56.3M with 0% Other** — i.e. it's
   *labor/equipment* charges (fleet admin, equipment rental/depreciation spread
   across the org) parked on standing admin tasks that, by their nature, produce
   no field accomplishment.

The smaller mixed activities (pothole 77% Other, stabilization 48% Other) are the
genuinely ambiguous ones — crew activities where a minority of tasks carry cost
with no logged work, the cases most worth a data-quality look.

### 9.2 The biggest "invoice, no accomplishment" tasks

| Task | Activity | Net cost | Mix |
|---|---|--:|---|
| 94799 | 412 Embankment | **$2,837,054** | 100% Other, $0 labor |
| 95289 | 412 Embankment | $2,288,094 | 100% Other |
| 38058 | 210 Paving | $1,330,218 | 100% Other |
| 92451 | 210 Paving | $1,289,535 | 100% Other |
| 23358 | 210 Paving | $1,196,246 | 100% Other |
| 82682 | 412 Embankment | $1,143,423 | 100% Other |

A clean signature: **single tasks holding $1–3M of pure contract invoice with no
labor and no accomplishment.**

### 9.3 Token accomplishments — the stub line

Even where an accomplishment *exists*, on big contracts it's often a **single stub
line** standing in for a multi-million-dollar invoice:

| Task | Activity | Net cost | Accompl. | $ / accomplishment |
|---|---|--:|--:|--:|
| 82222 | 210 Paving | $2,590,130 | **1** | **$2.59 M** |
| 19433 | 210 Paving | $1,964,750 | 1 | $1.96 M |
| 73131 | 210 Paving | $1,830,146 | 1 | $1.83 M |
| 29423 | 210 Paving | $1,770,813 | 1 | $1.77 M |

Every one is **210 paving, 100% Other, one accomplishment** carrying ~$2M. So the
true "contract cost with no real work-report" figure is **larger than the $251M
zero-accomplishment number** — add the mega-contracts that carry a lone token
line. **Paving is almost entirely a contract-invoice activity in this system**:
its $184M of spend is overwhelmingly "Other," landing on tasks with either no
accomplishment or a single placeholder.

### 9.4 Bottom line

**Cost-without-accomplishment is real, large, and overwhelmingly contractual.**
**$251M (26% of spend)** has cost but no accomplishment; **73% is contract
invoice** ("Other"), led by **paving ($93M) and embankment ($42M)** at 100%
contract. A second **$56M** is **equipment/administrative overhead** (811) with no
field output. The remainder is small and mixed — the only slice where "missing
accomplishment" might be a *reporting gap* rather than a *contractor*. And the
$251M understates the contract-with-no-real-work total, because the largest
paving contracts hide behind a **single token accomplishment** worth millions.
The headline for cost analytics: **you cannot read "work done" from "money spent"
on roughly a quarter of the ledger — it's invoices, not crews.**

---

## 10. Method & caveats

- **`CreatedOn`** is the row's creation time in OM. Its weekday + hour-of-day
  shape (business hours, afternoon peak) demonstrates it tracks real data entry,
  so session timing is meaningful. A session's length is measured **first entry
  → last entry that day**; it includes idle gaps, so it is an *envelope* of the
  data-entry window, not pure keystroke time (true active time is shorter,
  especially for the long tail).
- **Current rows only** (`ValidTo IS NULL`); OM is system-versioned. Historical
  edits/superseded versions are excluded.
- **"Blanket"** is reported two ways and kept distinct: accomplishment-level
  (`DWRLI.AssetReferenceId IS NULL`) and task-level (no `TaskAssetReference`).
- **Users** are identified by their application id (Okta-style `00u…` GUID), not
  resolved to names. Counts/medians are descriptive of the data only.
- **Cost figures** are **net** actual (`Confirmed = 1`): positive postings plus
  their reversals. This is the right basis for "what was actually spent," but it
  means gross transaction value and transaction *counts* are far larger (the
  −$873M of reversals). "Estimate" cost (`Confirmed = 0`) is excluded from spend
  totals. `TransactionDate` can be future-dated (planning); spend-to-date figures
  are bounded at `<= today`. Activity is resolved via the task
  (`Task.PerformanceStandardCodeId`), same as the accomplishment analysis.
- **Asset creation time (§8)** is proxied by `AssetReference.ReferenceDate` —
  `AssetReference` has no `CreatedOn`/`CreatedById`. ReferenceDate is 100%
  populated with millisecond system timestamps and lands within seconds of some
  accomplishment entries, so it behaves as the asset's creation instant; but it
  is a proxy, and a small share (≈1.3%) of accomplishments predate their asset's
  ReferenceDate (back-dated entries or a later ref update). "Fast follower" is
  measured as accomplishment `CreatedOn` minus asset `ReferenceDate`.
- Read-only analysis against shared production; no rows were modified.
