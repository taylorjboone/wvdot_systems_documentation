# OM_WVDOT — Milepost-vs-Asset Extent & Cost-Without-Asset Analysis

**System:** WVDOT Deighton dTIMS production (`TAMSDW.OM_WVDOT.operations`), read-only via `TAMSDW`.
**Scope:** all current rows (`ValidTo IS NULL`); cost = `BaseTransaction.TransactionTotalCost`
summed across the four transaction subtypes (Labor / Equipment / Stockpile / Other), **totality
(planned + actual)** as requested.
**Activity code:** `operations.PerformanceStandard` (`Code` + `Description`), joined via
`Task.PerformanceStandardCodeId`.

> Companions: `OM_WVDOT_GUIDE.md`, `OM_WVDOT_TASK_ANALYSIS.md`, `OM_WVDOT_DWR_ANALYSIS.md`.

---

## 0. Executive summary

1. **Manually-entered mileposts just echo the full asset extent ~52% of the time.** Of the 354,730
   line items with both mileposts filled and an asset, **185,842 (52.4%) span the entire asset**,
   136,307 (38.4%) are genuine sub-segments, and 32,581 (9.2%) are zero-length points.
2. **The auto-derived `From`/`To` is the whole asset 99.3% of the time** — it is copied from the
   asset and almost never narrowed. So real, intentional location refinement only happens in the
   *milepost* fields, and even there only ~38% of the time.
3. **34.0% of all system cost — about $331.6M of ~$974.5M — is on tasks with no asset at all.**
4. **That no-asset money is concentrated and mostly legitimate**: ~$120M is winter Snow Removal &
   Ice Control (SRIC), and ~$140M is pure overhead/administration (equipment admin, org overhead,
   buildings, training, travel, meetings) — categories that *cannot* have a road asset.
5. **But there are real data gaps**: asset-type activities that should be asset-linked but largely
   aren't — Highway Lights (98.8% no-asset), ITS Device Repair (96.5%), Traffic Signals (78.9%),
   Sign Installation/Maintenance (71.8%), Bridge Inspection (37.8%).

---

## 1. Do the mileposts just cover the whole asset?

Two location representations exist on each Daily Work Report line item, both gated on having an
`AssetReferenceId`:
- **`From` / `To`** — auto-populated from the asset's linear extent.
- **`BeginningMilePost` / `EndMilePost`** — separately, manually entered.

### 1a. Mileposts vs the full asset extent (354,730 line items with mileposts + asset)
Comparing `BeginningMilePost`/`EndMilePost` to the asset's `From`/`To` (tolerance 0.0001):

| Milepost range | Line items | % |
|---|---:|---:|
| **= whole asset extent** | **185,842** | **52.4%** |
| Genuine sub-segment | 136,307 | 38.4% |
| Zero-length point (begin = end) | 32,581 | 9.2% |

**Just over half the time, the mileposts are nothing more than the beginning and ending measure of
the entire asset** — i.e., the crew accepted the asset's own extent rather than describing the
specific worked segment. Only ~38% carry real sub-asset detail, and ~9% collapse to a single point.

### 1b. From/To vs the full asset extent (410,523 line items with From/To + asset)
| From/To range | Line items | % |
|---|---:|---:|
| **= whole asset extent** | **407,825** | **99.3%** |
| Genuine sub-segment | 2,426 | 0.6% |
| Zero-length point | 272 | 0.07% |

**`From`/`To` is the whole asset 99.3% of the time** — confirming it is a system copy of the asset
extent, essentially never edited. All meaningful human location refinement lives in the milepost
fields (§1a), and even there the asset extent is taken verbatim about half the time.

**Net answer:** when location *is* captured, it is the entire-asset measure far more often than not
— 99% of the time for the auto `From`/`To`, and 52% (61% if you fold in zero-length points as
"not a real sub-segment") for the manual mileposts. True sub-segment precision exists on roughly
**38% of milepost-bearing line items** and **0.6% of From/To values**.

---

## 2. What percent of total cost has no asset?

Total system cost (all four transaction subtypes, current rows), split by whether the charging task
has any `TaskAssetReference`:

| Group | Tasks (with cost) | Total cost | % of cost | Avg cost / task |
|---|---:|---:|---:|---:|
| **No asset** | 6,806 | **$331,579,599** | **34.0%** | **$48,719** |
| Has asset | 95,189 | $642,912,275 | 66.0% | $6,754 |
| **Total** | 101,995 | **$974,491,874** | 100% | $9,554 |

**$331.6M — 34.0% of all cost in the system — is attached to no asset whatsoever.** And it is
intensely concentrated: the 6,806 no-asset tasks are **6.7% of costed tasks but carry a third of the
money**, averaging **$48,719 each — 7.2× the $6,754 average of an asset-linked task.** These are the
blanket/standing operations identified in the task analysis, now measured in dollars.

---

## 3. No-asset cost broken down by activity code

Top activities ranked by **no-asset cost** (PerformanceStandard `Code` — `Description`):

| Code | Activity | Total cost | No-asset cost | % no-asset |
|---|---|---:|---:|---:|
| 341 | APPLICATION OF SOLID SRIC MATERIALS | $113.2M | **$87.0M** | 76.9% |
| 811 | ADMINISTRATIVE COST FOR EQUIPMENT | $56.9M | $56.9M | **100.0%** |
| 801 | ORGANIZATIONAL OVERHEAD - MAINTENANCE | $37.5M | $35.0M | 93.4% |
| 345 | SRIC SUPPORT OPERATIONS | $34.1M | $30.5M | 89.4% |
| 412 | EMBANKMENT STABILIZATION | $46.6M | $21.4M | 45.9% |
| 816 | BUILDINGS AND GROUNDS | $19.6M | $18.4M | 94.3% |
| 210 | PAVING | $183.6M | $15.9M | 8.7% |
| 382 | BRIDGE INSPECTION & ANALYSIS | $20.9M | $7.9M | 37.8% |
| 809 | TRAINING - ANNUAL PLAN PERSONNEL | $8.2M | $7.9M | 95.8% |
| 814 | HANDLING OF MATERIALS (NON-SRIC) | $5.9M | $5.3M | 89.6% |
| 364 | SIGN INSTALLATION / MAINTENANCE | $7.3M | $5.3M | 71.8% |
| RETIRED-413 | RETIRED - EMBANKMENT STABILIZATION | $26.0M | $4.8M | 18.3% |
| 817 | SWAT / CITIZEN REQUESTS | $4.4M | $3.9M | 88.8% |
| RETIRED-815 | RETIRED - CLEANING OF EQUIPMENT | $2.9M | $2.7M | 93.4% |
| 318 | CANOPY CLEARING | $26.7M | $2.6M | 9.8% |
| 342 | SNOW PLOWING OR BLOWING | $3.6M | $2.6M | 73.3% |
| 503 | CLEANING OF EQUIPMENT | $2.7M | $2.5M | 91.5% |
| 818 | CORE MAINTENANCE PLANNING & REVIEW | $2.7M | $2.4M | 88.6% |
| 542 | EQUIPMENT TRANSPORTING - ALL | $4.2M | $2.3M | 55.1% |
| 805 | TRAVEL TIME - MAINTENANCE | $2.3M | $1.7M | 72.5% |
| 365 | TRAFFIC SIGNALS | $1.2M | $0.92M | 78.9% |
| 307 | HERBICIDE SPRAYING | $1.8M | $0.88M | 48.2% |
| 822 | NATURAL DISASTER ADMIN OVERHEAD | $0.84M | $0.84M | 100.0% |
| 303 | MOWING-NON EXPRESSWAY | $21.5M | $0.65M | 3.0% |
| 369 | HIGHWAY LIGHTS | $0.61M | $0.61M | 98.8% |
| 362 | ITS DEVICE REPAIR | $0.36M | $0.35M | 96.5% |
| 200 | POTHOLE PATCHING | $40.6M | $0.33M | 0.8% |

### 3a. The no-asset cost falls into three buckets

**A. Winter Snow Removal & Ice Control (~$120M, the single biggest driver).**
Codes 341 (solid materials, $87.0M), 345 (SRIC support, $30.5M), 342 (plowing, $2.6M),
340 (liquid materials, $0.55M). SRIC is performed route-wide as blanket operations — there is no
single asset to attach. **This is expected, not a defect.**

**B. Overhead / administrative (~$140M, almost entirely no-asset by definition).**
811 Equipment Admin ($56.9M, 100%), 801 Org Overhead ($35.0M), 816 Buildings & Grounds ($18.4M),
809 Training ($7.9M), 814 Material Handling ($5.3M), plus 818/805/806/803/822/550/503/535/RETIRED-815.
**These activities cannot have a road asset** — training, meetings, equipment maintenance, travel
time, HR. Correctly assetless.

**C. Field activities that *should* be asset-linked but largely aren't — the real data gaps.**
These reference physical assets that exist in the inventory, yet most of the spend is unattached:
| Code | Activity | % no-asset | Why it's a gap |
|---|---|---:|---|
| 369 | HIGHWAY LIGHTS | 98.8% | Lights are discrete assets |
| 362 | ITS DEVICE REPAIR | 96.5% | ITS devices are assets |
| 365 | TRAFFIC SIGNALS | 78.9% | Signals are assets |
| 364 | SIGN INSTALLATION / MAINTENANCE | 71.8% | Signs are assets |
| 382 | BRIDGE INSPECTION & ANALYSIS | 37.8% | Bridges are assets |
| 412 | EMBANKMENT STABILIZATION | 45.9% | Locatable embankment segments |

Bucket C is where asset-linking discipline could be improved — work is being done on inventoried
assets but charged to a blanket/assetless task. By contrast, the core pavement programs are
already well-linked: PAVING 8.7%, CANOPY CLEARING 9.8%, MOWING 3.0%, POTHOLE PATCHING **0.8%**.

### 3b. Quick interpretation
- **~$260M of the $331.6M no-asset cost (≈78%) is legitimately assetless** (winter SRIC + overhead).
- **The remaining ~$70M is the addressable gap** — field activities on real assets that weren't
  linked, led by signs/signals/lights/ITS/bridges.
- The "RETIRED-" activity codes (413, 815) still carry ~$29M combined — deprecated codes that are
  still being charged against; worth a cleanup conversation.

---

## 4. Reusable queries (read-only via OPENQUERY)

**Mileposts vs whole-asset extent (§1a):**
```sql
SELECT * FROM OPENQUERY([TAMSDW], '
SELECT CASE WHEN ABS(li.BeginningMilePost-ar.[From])<0.0001 AND ABS(li.EndMilePost-ar.[To])<0.0001
            THEN ''whole_asset''
            WHEN ABS(li.BeginningMilePost-li.EndMilePost)<0.0001 THEN ''point''
            ELSE ''sub_segment'' END kind, COUNT(*) n
FROM OM_WVDOT.operations.DailyWorkReportLineItem li
JOIN OM_WVDOT.operations.AssetReference ar ON ar.AssetReferenceId=li.AssetReferenceId
WHERE li.ValidTo IS NULL AND li.BeginningMilePost IS NOT NULL AND li.EndMilePost IS NOT NULL
GROUP BY CASE WHEN ABS(li.BeginningMilePost-ar.[From])<0.0001 AND ABS(li.EndMilePost-ar.[To])<0.0001
            THEN ''whole_asset''
            WHEN ABS(li.BeginningMilePost-li.EndMilePost)<0.0001 THEN ''point''
            ELSE ''sub_segment'' END');
```

**Total cost split by asset presence (§2) and by activity (§3):** build a per-task cost CTE that
`UNION ALL`s the four subtype tables joined to `BaseTransaction` (filter `bt.ValidTo IS NULL`),
`GROUP BY TaskId`; LEFT JOIN a `GROUP BY ReferenceObjectId` of `TaskAssetReference` to flag
no-asset; for §3 also JOIN `Task` → `PerformanceStandard` on `PerformanceStandardCodeId` and group
by `ps.Code, ps.Description`. (Full SQL was executed during analysis; replicate the CTE from the
task-analysis doc.)

> Note: figures are **totality** (planned + actual). To restrict to actuals, add
> `AND bt.TransactionDate <= SYSDATETIMEOFFSET()` inside each subtype join.

---

*All figures computed directly against `TAMSDW.OM_WVDOT` at analysis time.*

---
---

# PART II — The "Golden Record": Cost + Accomplishment + Asset

The question that actually matters for a maintenance management system isn't "does it have an
asset" — it's whether a **cost** can be tied to a **measured accomplishment** *and* an **asset**, so
you can compute unit cost ($/accomplishment), productivity, and asset-level spend. This part
measures that, by cost.

## 5. The linkage reality (read this first)

dTIMS provides a column to tie each cost transaction directly to its daily-work-report line
(`LaborTransaction.DailyWorkReportLineItemId`, etc.). **It is 100% NULL on all 5.2M transactions —
never populated** (the same fate as `TimeCodeId`). Therefore cost and accomplishment **cannot** be
joined at the row/line level. The only available join is **Task + date**: a transaction carries
`TaskId` + `TransactionDate`; a DWR line carries `TaskId` + `AccomplishmentDate` + asset +
accomplishment. All Part II figures use that grain.

> Incidental confirmation: the analysis collapses to **654,894 task-days**, which is exactly the row
> count of `Data-Warehouse.dbo.dtims_transactions` — so that export is one row per task-day.

## 6. Same-day: does cost land on a day with an asset+accomplishment DWR line?

Cost classified by what exists **on the same task, same day**:

| Same-day record on the task | Cost | % of all cost | Task-days |
|---|---:|---:|---:|
| ✅ **GOLDEN — accomplishment + asset** | **$295.4M** | **30.3%** | 241,089 |
| Accomplishment, but no asset | $182.4M | 18.7% | 171,206 |
| DWR exists, zero accomplishment | $15.5M | 1.6% | 8,872 |
| ❌ No same-day DWR at all | $481.3M | **49.4%** | 233,727 |
| **Total** | **$974.5M** | 100% | 654,894 |

**Only 30.3% of the money is a golden record.** Nearly half (49.4%, $481M) has no field
accomplishment recorded on the day it was charged — and it's the *expensive* work (49% of cost on
36% of task-days).

## 7. Generous: same task, within ±7 days

| Match (within a week) | Cost | % of all cost | Task-days |
|---|---:|---:|---:|
| ✅ **GOLDEN — accomplishment + asset** | **$366.9M** | **37.7%** | 321,784 |
| Accomplishment, no asset | $208.6M | 21.4% | 199,601 |
| DWR, zero accomplishment | $11.0M | 1.1% | 5,322 |
| ❌ No DWR within 7 days | $387.9M | **39.8%** | 128,187 |

**Widening to a full week buys only ~7 points** (golden 30.3% → 37.7%). **~40% of cost still has no
DWR within a week.** The gap is structural — the asset/accomplishment link was never captured, not
captured late — so no time window fixes it. Even generously, **fewer than 4 of 10 dollars are fully
analyzable**, and **~6 of 10 can't be tied to an asset within a week.**

---

# PART III — Where is the drop-off coming from?

Drop-off = cost that is **not** golden (no asset+accomplishment within 7 days). Broken down by the
activity code (`PerformanceStandard`) on the task.

## 8. Drop-off by activity (within-7-day golden test)

Sorted by non-golden ($) — the biggest holes first:

| Code | Activity | Total cost | Golden | **Drop-off** | % golden |
|---|---|---:|---:|---:|---:|
| **210** | **PAVING** | $183.6M | $23.7M | **$159.9M** | **12.9%** |
| 341 | APPLICATION OF SOLID SRIC MATERIALS | $113.2M | $24.1M | $89.1M | 21.3% |
| 811 | ADMINISTRATIVE COST FOR EQUIPMENT | $56.9M | $0 | $56.9M | 0.0% |
| 412 | EMBANKMENT STABILIZATION | $46.6M | $2.8M | $43.8M | 6.0% |
| 801 | ORGANIZATIONAL OVERHEAD - MAINT. | $37.5M | $2.1M | $35.4M | 5.6% |
| 345 | SRIC SUPPORT OPERATIONS | $34.1M | $3.5M | $30.6M | 10.3% |
| RETIRED-413 | RETIRED - EMBANKMENT STABILIZATION | $26.0M | $0.2M | $25.8M | 0.9% |
| 816 | BUILDINGS AND GROUNDS | $19.6M | $0.9M | $18.7M | 4.5% |
| 318 | CANOPY CLEARING | $26.7M | $12.8M | $13.9M | 48.1% |
| 261 | STABILIZATION - ROADWAY | $49.0M | $36.6M | $12.4M | 74.6% |
| 382 | BRIDGE INSPECTION & ANALYSIS | $20.9M | $12.5M | $8.4M | 59.8% |
| 809 | TRAINING - ANNUAL PLAN PERSONNEL | $8.2M | $0.3M | $7.9M | 3.6% |
| 201 | PATCHING BITUMINOUS PAVEMENTS | $31.3M | $23.6M | $7.7M | 75.3% |
| 200 | POTHOLE PATCHING | $40.6M | $34.6M | $6.0M | 85.2% |
| 282 | INSTALL PIPE CULVERTS | $18.9M | $13.2M | $5.7M | 69.7% |
| 364 | SIGN INSTALLATION / MAINTENANCE | $7.3M | $1.7M | $5.7M | 23.0% |
| 405 | STEEL PILING WALL INSTALLATION | $12.1M | $7.4M | $4.7M | 61.0% |
| … | (well-documented, smaller drop-offs below) | | | | |
| 288 | PULLING SHOULDERS/DITCHES - PAVED | $26.9M | $25.1M | $1.7M | **93.5%** |
| 203 | SKIP PATCHING | $9.9M | $9.1M | $0.7M | **92.6%** |
| 281 | MINOR DRAINAGE STRUCTURES | $11.9M | $10.8M | $1.1M | **90.6%** |
| 304 | BRUSH CONTROL - HAND | $8.8M | $7.9M | $1.0M | **89.2%** |
| 303 | MOWING - NON EXPRESSWAY | $21.5M | $18.9M | $2.6M | **87.7%** |

### 8a. The four sources of drop-off
1. **PAVING ($160M) — the #1 hole and the most actionable.** See §9; it has assets but no daily
   accomplishment.
2. **Winter SRIC / snow & ice (~$122M)** — codes 341, 345, 342. Route-wide blanket ops; no single
   asset. Expected.
3. **Overhead / administration (~$135M)** — equipment admin (811, 100% non-golden), org overhead
   (801), buildings (816), training (809), material handling (814), travel (805), etc. **Cannot**
   carry an asset/accomplishment. Legitimately unanalyzable — exclude from unit-cost work.
4. **Geotechnical / embankment (~$80M)** — 412, RETIRED-413, 405, 421, 285. Locatable in principle
   but largely not asset-linked and accomplishment-light; partial real gap.

### 8b. Activities that ARE well-documented (the model to copy)
Routine force-account maintenance is excellent: Pulling Shoulders/Ditches 93.5%, Skip Patching
92.6%, Minor Drainage 90.6%, Brush Control 89%, Mowing 87.7%, Pothole Patching 85.2%, Bituminous
Patching 75.3%, Roadway Stabilization 74.6%. These crews reliably file DWR accomplishments against
assets. The drop-off is **not** a system-wide discipline problem — it's concentrated in specific
programs.

## 9. PAVING diagnosis — the most important single finding

Paving is 91% asset-linked at the task level (§3, only 8.7% no-asset) yet only **12.9% golden**.
Decomposing its $159.9M drop-off:

| Paving cost bucket (within 7d) | Cost |
|---|---:|
| Golden (asset + accomplishment) | $23.7M |
| DWR exists, no accomplishment | $4.1M |
| Accomplishment, no asset | $0.1M |
| **No DWR within 7 days at all** | **$155.7M (97% of the drop-off)** |

**The paving gap is missing *accomplishment*, not missing *assets*.** The asset is on the task, but
there is essentially no daily-work-report production recorded near the cost. Almost certainly because
paving is **contract / pay-item work** that doesn't flow through force-account daily work reports the
way in-house maintenance does. Implication: **you cannot compute paving productivity or unit cost
($/ton, $/lane-mile) from OM_WVDOT** — the largest single maintenance activity ($184M) is a
cost-only black box. If paving analytics matter, the accomplishment data must come from the
contract/pay-item system, not dTIMS DWRs.

## 10. Program breakdown — NOT AVAILABLE (another unused dimension)

`Task.ProgramId` does not resolve to the `Program` table: **100% of cost ($971.7M) maps to
"(no program)".** Like `DailyWorkReportLineItemId` and `TimeCodeId`, the Program linkage is
unpopulated. **Program-level cost rollups are not possible** from this data as configured. (Activity
code via `PerformanceStandard` IS populated and is the usable program/work dimension — use §8.)

---

# PART IV — Consolidated data-completeness scorecard

| Capability | Available? | Coverage |
|---|---|---|
| Total cost | ✅ | $974.5M, 100% |
| Cost → asset (task level) | ⚠️ partial | 66% of cost |
| Cost → accomplishment + asset, same day | ⚠️ weak | **30.3%** |
| Cost → accomplishment + asset, within 7 days | ⚠️ weak | **37.7%** |
| Cost → DWR line (row-level link) | ❌ | 0% (`DailyWorkReportLineItemId` all NULL) |
| Cost → Program | ❌ | 0% (`ProgramId` unmapped) |
| Cost → Activity code | ✅ | populated (`PerformanceStandard`) |
| Overtime | ❌ | not tracked (single "Regular" 1.0× code) |
| Unit cost / productivity (paving) | ❌ | accomplishment absent ($156M no-DWR) |
| Unit cost / productivity (routine maint.) | ✅ | 85–93% golden for patching/ditching/brush/mowing |

**One-line takeaway:** the system is genuinely analytics-ready for routine in-house force-account
maintenance (~85–93% golden), but **only ~30–38% of total dollars are fully analyzable**, with the
shortfall driven by (1) paving recorded as cost-only, (2) winter SRIC blanket ops, and (3) overhead
that can't be asset-linked. Fixing paving accomplishment capture and the unused Program link would
be the highest-leverage data improvements.

*All Part II–IV figures computed directly against `TAMSDW.OM_WVDOT` at analysis time; golden test =
same task with a DWR line carrying an asset and Accomplishment>0 within the stated date window.*
