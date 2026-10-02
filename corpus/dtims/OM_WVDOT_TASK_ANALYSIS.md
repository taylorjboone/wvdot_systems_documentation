# OM_WVDOT — Tasks, Daily Work Reports, Assets & Transactions: Behavioral Analysis

**System:** WVDOT Deighton dTIMS production (`TAMSDW.OM_WVDOT`, `operations` schema), read-only via
the `TAMSDW` linked server.
**Data window analyzed:** transactions **2024-04 → 2026-06** (the system went live mid-2024; rows
beyond "today" are *planned/scheduled* — this is a forward-planning system).
**Method:** all figures computed remotely via `OPENQUERY([TAMSDW], …)` against current rows
(`ValidTo IS NULL`) unless noted. Change frequency is measured from the `*History` change-log
tables (`HistoricObjectId`, `ModifiedOn`, `ChangeValue`) and from each row's `RowVersion`.

> See `OM_WVDOT_GUIDE.md` for connection mechanics, the `ValidTo IS NULL` temporal rule, and the
> `DomainValue` lookup convention. This document is the behavioral/analytical companion.

---

## 0. Executive summary (the headlines)

1. **Blanket tasks dominate throughput.** 8,187 tasks (7.3% of 112,377 current tasks) have **zero
   linked assets** yet carry **1,134,420 labor transactions — 40% of all labor activity** — at
   **~139 labor txns/task vs ~16 for asset-linked tasks** (≈8.5× the intensity).
2. **Throughput predicts "blanket-ness" almost perfectly.** The share of zero-asset tasks rises
   monotonically with transaction volume: **3% at 1–20 txns → 71% at 500+ txns.** The heaviest
   tasks are overwhelmingly assetless buckets.
3. **The work cadence inverts seasonally.** Summer = many discrete asset-linked tasks (~9,400
   active/month, few txns each). Winter = few tasks (~3,800/month) but a *flood* of transactions
   (Jan 2025: 230,691 txns on 3,780 tasks ≈ 61 txns/task) — the **snow & ice blanket-task
   signature.**
4. **Tasks are edited a handful of times; line items are write-once.** ~91% of tasks change 2–5
   times; **98.8% of Daily Work Report line items are never edited after creation** (append-only).
5. **Overtime is not tracked.** The `TimeCode` table holds a single entry ("Regular", multiplier
   1.0) and `LaborTransaction.TimeCodeId` is **100% NULL**. No overtime/premium dimension exists in
   this instance.
6. **Assets-per-task is stable over time** at ~2–2.5 (no drift), but with a heavy tail — individual
   network-level tasks reference 200–450 assets.

---

## 1. Entities & relationships used

```
Task (116,430 rows / 112,377 current)
 ├─ TaskAssetReference (267,582)   ReferenceObjectId = TaskId  ──► AssetReference (567,037)
 ├─ DailyWorkReportLineItem (632,723)  TaskId, AssetReferenceId, Accomplishment, AccomplishmentDate
 │     └─ DailyWorkReport (header)      DailyWorkReportId
 └─ BaseTransaction (5,230,120)  subtyped by TaskId-bearing children:
       ├─ LaborTransaction (2,838,031)      TaskId, (TimeCodeId = always NULL)
       ├─ EquipmentTransaction (1,585,233)  TaskId
       ├─ StockpileTransaction (184,606)    TaskId
       └─ OtherCost (622,250)               TaskId
Change logs:  TaskHistory (470,806) · DailyWorkReportLineItemHistory (658,949)
              keyed by HistoricObjectId, with ModifiedOn / ModifiedBy / ChangeValue
```
- `BaseTransaction.voa_class` is just the subtype discriminator (`LaborTransaction` /
  `EquipmentTransaction` / `OtherCost` / `StockpileTransaction`) — it matches the child row counts
  exactly and is **not** a cost-type/overtime flag.
- **"Blanket task"** here = a current Task with **zero rows in `TaskAssetReference`** (no asset is
  linked), yet meaningful labor/accomplishment throughput.

---

## 2. How often do they change?

### Tasks — change events per task (from `TaskHistory`)
| Change events | Tasks | Share |
|---|---:|---:|
| 1 | 1,335 | 1.1% |
| **2–5** | **104,528** | **90.4%** |
| 6–10 | 8,107 | 7.0% |
| 11–25 | 1,977 | 1.7% |
| 26–50 | 345 | 0.3% |
| 50+ | 138 | 0.1% |

Cross-checked against `Task.RowVersion` (saves per row): the mass sits at 6 and 8 edits
(30,975 and 24,993 tasks respectively), with a long thin tail out past 50. **Most tasks are touched
a few times during their lifecycle, then go quiet.** A tiny cohort (138 tasks with 50+ change
events) is under near-constant revision — these are long-running blanket/standing tasks (see §6).

### Daily Work Report line items — essentially immutable
| Change events | Line items | Share |
|---|---:|---:|
| **1** | **642,821** | **98.8%** |
| 2–5 | 7,906 | 1.2% |
| 6–10 | 1 | ~0% |

DWR line items behave as **append-only event records**: once a crew's daily accomplishment is
posted, it is almost never edited. This makes the DWR stream a clean, trustworthy audit of field
activity. **Use DWR line items, not task edits, to reconstruct "what actually happened in the
field."**

---

## 3. Transaction rate per task

Labor transactions per task (tasks that have ≥1 labor txn; 97,927 tasks, 2.84M txns):

| Labor txns / task | Tasks | Total txns | Share of all txns |
|---|---:|---:|---:|
| 1–5 | 43,349 | 124,107 | 4.4% |
| 6–20 | 35,902 | 373,955 | 13.2% |
| 21–50 | 10,341 | 324,539 | 11.4% |
| 51–100 | 3,852 | 269,402 | 9.5% |
| 101–500 | 3,479 | 712,488 | 25.1% |
| **500+** | **1,004** | **1,033,540** | **36.4%** |

**Extreme concentration:** ~1% of tasks (the 1,004 with 500+ txns) generate over a third of all
labor transactions. The distribution is classic power-law — and §6 shows these heavy tasks are
mostly assetless blankets.

---

## 4. Cadence over time

### Labor-transaction cadence (actuals to date)
| Month | Labor txns | Labor cost | Active tasks | txns/task |
|---|---:|---:|---:|---:|
| 2024-07 | 94,931 | $12.9M | 9,430 | 10 |
| 2024-08 | 100,175 | $13.4M | 9,333 | 11 |
| 2024-12 | 124,574 | $12.6M | 4,657 | 27 |
| **2025-01** | **230,691** | **$22.8M** | **3,780** | **61** |
| 2025-02 | 177,123 | $16.2M | 5,972 | 30 |
| 2025-06 | 100,530 | $13.1M | 7,143 | 14 |
| 2025-07 | 103,409 | $13.6M | 7,196 | 14 |
| **2025-12** | **157,995** | **$15.5M** | **3,782** | **42** |
| **2026-01** | **189,508** | **$19.1M** | **4,227** | **45** |

**The seasonal inversion is the key cadence finding.** Monthly *cost* is fairly flat (~$13M), but
the *shape* of the work flips:

- **Summer (Jun–Sep):** ~7,000–9,400 active tasks, ~10–14 txns each → **many discrete,
  asset-linked jobs** (paving, drainage, signs, bridge work).
- **Winter (Dec–Feb):** active tasks collapse to ~3,800–6,000 while transaction volume **spikes 2×**
  (Jan 2025 hit 230K txns) and txns/task jumps to 40–61 → **a few standing snow-&-ice blanket tasks
  absorbing enormous daily crew/equipment charging.**

This is the operational fingerprint of a northern DOT: discrete capital-style maintenance in the
warm months, concentrated emergency/cyclic operations in winter.

### Field-work cadence (DWR line items by `AccomplishmentDate`)
Steady **~20,000–35,000 line items/month**, accomplishment volume **$1.2M–3.6M units/month**,
modestly higher in summer (more discrete jobs each generating their own line items). Unlike labor
txns, DWR line items do **not** spike in winter — because blanket snow operations post huge numbers
of *transactions* against *few* line items.

---

## 5. Overtime — NOT TRACKED (important caveat)

There is **no usable overtime dimension** in this dTIMS instance:

- `operations.TimeCode` contains **exactly one row**: `Code='Regular'`, `Multiplier=1.0`
  (created 2025-07-17). No "Overtime", "Premium", "Double-time" codes exist.
- `LaborTransaction.TimeCodeId` is **NULL for all 2,838,031 rows.**
- No `DomainValue` types match time/labor/overtime/premium.

**Implication:** you cannot compute overtime hours or OT premium from OM_WVDOT as configured. Labor
cost is recorded as a flat rate × quantity with no time-multiplier breakout. The winter
transaction surge (§4) is real *volume*, but the data **cannot tell you how much of it was OT** —
that distinction was never captured. If OT analysis is required, it must come from a payroll/HR
source, not dTIMS.

---

## 6. Assets per task

### Distribution (tasks that have ≥1 asset; 107,109 task-references)
| Assets / task | Tasks |
|---|---:|
| 1 | 82,849 |
| 2–5 | 16,697 |
| 6–20 | 5,916 |
| 21–100 | 1,506 |
| 100+ | 141 |

Most asset-linked tasks point at a **single** asset (a road segment, bridge, culvert). A small tail
of network-level tasks references hundreds (max ≈ 450).

### Assets per task *over time* (by task creation-month cohort)
Average assets-per-task is **flat at ~2.0–2.5 across the entire history** (range 1.6–3.4, with mild
summer highs — e.g. 2025-06 cohort 3.4). **No drift**: WVDOT's asset-linking behavior has been
consistent since go-live; tasks are not getting systematically more or less asset-rich. Each
monthly cohort also produces a steady ~130–745 zero-asset (blanket) tasks.

---

## 7. Blanket tasks (zero assets, high throughput) — the core finding

### 7a. Aggregate: blanket vs asset-linked
| Group | Tasks | Labor txns | DWR line items | Accomplishment | Labor txns/task |
|---|---:|---:|---:|---:|---:|
| **Zero assets (blanket)** | **8,187** (7.3%) | **1,134,420** (40%) | 218,720 | 5.25M | **≈139** |
| Has assets | 104,190 (92.7%) | 1,701,481 (60%) | 413,128 | 44.63M | ≈16 |

A blanket task carries **~8.5× the labor transactions, ~6.7× the DWR line items, and ~1.5× the
accomplishment** of a typical asset-linked task. They are the high-throughput "buckets" the field
charges routine/standing work against.

### 7b. The decisive gradient: throughput tier → % blanket
| Labor txns / task | Tasks | Zero-asset tasks | **% blanket** |
|---|---:|---:|---:|
| 1–20 | 79,251 | 2,521 | **3.2%** |
| 21–50 | 10,341 | 949 | **9.2%** |
| 51–100 | 3,852 | 582 | **15.1%** |
| 101–500 | 3,477 | 1,058 | **30.4%** |
| **500+** | **1,006** | **712** | **70.8%** |

**The busier a task is, the more likely it has no assets at all.** Among the 1,006 heaviest tasks,
**71% are pure blankets** — confirming these are standing operational accounts (snow/ice, routine
roadside, district-wide activities), not asset-specific jobs.

### 7c. Top blanket tasks (zero assets, by labor-txn throughput)
| TaskId | Name | Labor txns | Labor cost |
|---|---|---:|---:|
| 48912 | 4VSQA7E | 6,644 | $335,289 |
| 103812 | Q081T12 | 5,471 | $309,005 |
| 81181 | KDFRVBV | 4,648 | $444,954 |
| 48897 | W8CIAWX | 4,569 | $356,305 |
| 46322 | AS1HEZ5 | 3,948 | $397,034 |
| 12040 | G98H9BH | 3,572 | $331,954 |
| … | (all `Description = NULL`) | … | … |

These carry **3,000–6,600 labor transactions and $300K–450K each, with no asset linkage and no
description** — textbook standing/blanket activity codes. (Names are dTIMS smart-codes; the lack of
a Description is itself a marker of system-generated/standing tasks.)

### 7d. Edit-count vs throughput (why blankets also show up in the change data)
Average labor txns by task edit-count is **U-shaped**:
| Edits | Tasks | Avg labor txns |
|---|---:|---:|
| ≤5 | 12,150 | 63.2 |
| 6–10 | 75,788 | 13.7 |
| 11–25 | 18,646 | 27.8 |
| 26–50 | 3,493 | 55.7 |
| **50+** | **2,300** | **136.5** |

Two distinct heavy-throughput populations: (a) **lightly-edited blankets** (≤5 edits, set up once
and charged against heavily) and (b) **heavily-edited standing tasks** (50+ edits, ~137 txns each)
that are continually reopened/updated. The "normal" discrete task (6–10 edits) is the low-throughput
trough at ~14 txns.

---

## 8. Practical guidance

- **To find blanket tasks:** `Task` LEFT JOIN a `GROUP BY ReferenceObjectId` of
  `TaskAssetReference`; blanket = no match. Rank by labor-txn count or accomplishment.
- **To measure real field activity / cadence:** use `DailyWorkReportLineItem` by
  `AccomplishmentDate` (write-once, reliable) rather than task edits.
- **To measure cost/effort:** sum `BaseTransaction.TransactionTotalCost` through the four subtype
  tables on `TaskId`; always `ValidTo IS NULL` and bound by `TransactionDate <= SYSDATETIMEOFFSET()`
  for actuals (future-dated planning rows exist).
- **Do not attempt overtime analysis** from this source (§5).
- **Exclude/segment blanket tasks** in any per-asset cost or condition analysis — leaving them in
  will swamp asset-level metrics with unattributed standing-operation charges (they're 40% of labor
  activity).

---

## 9. Reusable queries (all read-only via OPENQUERY)

**Blanket vs asset-linked throughput:**
```sql
SELECT * FROM OPENQUERY([TAMSDW], '
WITH ass AS (SELECT ReferenceObjectId tid, COUNT(*) a FROM OM_WVDOT.operations.TaskAssetReference GROUP BY ReferenceObjectId),
     lab AS (SELECT TaskId tid, COUNT(*) txns FROM OM_WVDOT.operations.LaborTransaction GROUP BY TaskId)
SELECT CASE WHEN ass.a IS NULL THEN ''blanket'' ELSE ''asset-linked'' END grp,
       COUNT(*) tasks, SUM(COALESCE(lab.txns,0)) labor_txns
FROM OM_WVDOT.operations.Task t
LEFT JOIN ass ON ass.tid=t.TaskId LEFT JOIN lab ON lab.tid=t.TaskId
WHERE t.ValidTo IS NULL
GROUP BY CASE WHEN ass.a IS NULL THEN ''blanket'' ELSE ''asset-linked'' END');
```

**Throughput tier → % blanket:** (see §7b — `lab` CTE LEFT JOIN `ass`, bucket by `txns`, % where
`ass.tid IS NULL`).

**Monthly labor cadence (actuals):**
```sql
SELECT * FROM OPENQUERY([TAMSDW], '
SELECT CONVERT(char(7), bt.TransactionDate,126) ym, COUNT(*) txns,
       SUM(bt.TransactionTotalCost) cost, COUNT(DISTINCT lt.TaskId) active_tasks
FROM OM_WVDOT.operations.LaborTransaction lt
JOIN OM_WVDOT.operations.BaseTransaction bt ON bt.BaseTransactionId=lt.BaseTransactionId
WHERE bt.ValidTo IS NULL AND bt.TransactionDate <= SYSDATETIMEOFFSET()
GROUP BY CONVERT(char(7), bt.TransactionDate,126) ORDER BY ym');
```

**Task change frequency:** `GROUP BY HistoricObjectId` over `operations.TaskHistory`, bucket the
per-object `COUNT(*)`.

**Overtime check (returns the single Regular code):**
```sql
SELECT * FROM OPENQUERY([TAMSDW], 'SELECT Code, Name, Multiplier FROM OM_WVDOT.operations.TimeCode');
```

---

*All numbers above were computed directly against `TAMSDW.OM_WVDOT` during analysis and reflect the
production state at query time. Re-run the queries in §9 to refresh.*
