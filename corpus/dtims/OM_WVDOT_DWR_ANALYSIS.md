# OM_WVDOT — Daily Work Report Line Items: Completeness, Cadence & Throughput Analysis

**System:** WVDOT Deighton dTIMS production (`TAMSDW.OM_WVDOT.operations`), read-only via the
`TAMSDW` linked server.
**Primary table:** `operations.DailyWorkReportLineItem` (DWRLI) — **632,723 current rows**
(`ValidTo IS NULL`).
**Method:** all figures computed remotely via `OPENQUERY([TAMSDW], …)` against current rows.
Cadence uses `AccomplishmentDate` (when work was done) and `CreatedOn` (when it was entered).

> Companions: `OM_WVDOT_GUIDE.md` (connection/conventions) and `OM_WVDOT_TASK_ANALYSIS.md`
> (task/blanket-task behavior). This document focuses on the DWR line-item stream.

---

## 0. Executive summary

1. **One in three line items has no location at all.** 222,200 (35.1%) have **no asset reference,
   no mileposts, no From/To** — completely unlocated work. The remaining 64.9% are asset-anchored.
2. **Location is entirely gated on selecting an asset.** A milepost or From/To value *never* appears
   without an `AssetReferenceId`. There are exactly **three** states in the data (no other
   combination exists) — see §2.
3. **Even when an asset is chosen, mileposts are skipped 13.6% of the time.** 55,793 line items have
   an asset (and its auto-derived From/To extent) but the **BeginningMilePost/EndMilePost fields
   left blank.**
4. **4.5% of line items record zero accomplishment** (28,726 of 632,723) — work logged with no
   measured output. There are **no NULL and no negative** accomplishments.
5. **Zero-accomplishment is 6× more common on asset-linked items** (6.40%) than on blanket items
   (1.10%).
6. **Reporting is prompt and batched: 81% of work is entered 1–3 days after it's done** — almost
   never same-day, almost never real-time.
7. **Field work follows a clean Mon–Fri rhythm**; weekend activity is ~14% of a weekday (emergency
   / snow).
8. **"Completeness" is seasonal, not a data-quality trend.** Asset-fill swings from **86% (summer)
   to 42% (Jan, peak snow)** — driven by the winter shift to assetless blanket operations, not by
   changing data discipline.

---

## 1. Field fill rates (overall, 632,723 current line items)

| Field | Filled | % |
|---|---:|---:|
| `RouteName` | 630,158 | **99.6%** |
| `AssetReferenceId` | 410,523 | **64.9%** |
| `From` | 410,523 | 64.9% |
| `To` | 410,523 | 64.9% |
| `BeginningMilePost` | 354,730 | **56.1%** |
| `EndMilePost` | 354,730 | 56.1% |
| `Accomplishment` | 632,723 | 100% (never NULL) |

Two structural facts jump out of these counts:
- **`From`/`To` are filled exactly when `AssetReferenceId` is filled** (all three = 410,523). These
  are the **asset's linear-reference extent**, attached automatically with the asset — not a
  separate manual entry.
- **`BeginningMilePost`/`EndMilePost` always move together** (both 354,730 — never one without the
  other) and are a **separate, manually-entered** field that lags asset selection.
- **`RouteName` is nearly always present** (99.6%) — it's the one location field crews reliably fill
  even when everything else is blank.

---

## 2. THE COMPLETENESS MATRIX (asset reference × milepost) — core answer

Cross-tabulating asset reference, From/To, and mileposts yields **only three** combinations in the
entire 632,723-row table — no other state exists:

| State | Asset ref? | From/To? | Mileposts? | Line items | % of all |
|---|:---:|:---:|:---:|---:|---:|
| **Fully located** | ✅ | ✅ | ✅ | **354,730** | **56.1%** |
| **Asset but milepost blank** | ✅ | ✅ | ❌ | **55,793** | **8.8%** |
| **Unlocated** | ❌ | ❌ | ❌ | **222,200** | **35.1%** |

Reading this against your specific question:

- **Has an asset reference AND beginning+ending milepost filled in: 354,730 (56.1%).**
- **Has an asset reference but does NOT fill in the milepost: 55,793 (8.8%)** — i.e., **13.6% of all
  asset-linked line items** (55,793 / 410,523) skip the milepost even though an asset (with a
  From/To extent) is attached.
- **Has no asset reference at all — and therefore no location whatsoever: 222,200 (35.1%).**

**Key structural conclusion:** location data in dTIMS is **all-or-nothing on the asset**. You never
get a milepost or a From/To without an asset; choosing the asset is what populates the linear
extent. The only *optional* manual step is the milepost text, which is dropped on ~1 in 7
asset-linked items. The 222,200 unlocated items are the blanket/standing work (snow, routine
roadside) charged without any asset — they cannot be placed on the network at all.

---

## 3. Accomplishment values

| Class | Line items | % |
|---|---:|---:|
| Positive | 603,997 | **95.5%** |
| **Zero** | **28,726** | **4.5%** |
| NULL | 0 | 0% |
| Negative | 0 | 0% |

**28,726 line items (4.5%) record zero accomplishment** — a crew/day entry exists but no quantity
of work was measured. The complete absence of NULLs/negatives indicates the field is required and
validated ≥ 0 at entry; "zero" is therefore a deliberate (or default-left) value, not missing data.

### Zero-accomplishment by asset linkage
| | Zero-acc | Total | % zero |
|---|---:|---:|---:|
| Asset-linked | 26,277 | 410,523 | **6.40%** |
| Blanket (no asset) | 2,449 | 222,200 | **1.10%** |

**Counter-intuitive but telling:** asset-linked line items are **~6× more likely to have zero
accomplishment** than blanket ones. Blanket entries exist specifically to log a quantity of standing
work, so they almost always carry a value; asset-linked entries are more often opened (asset picked)
and left at zero — e.g., inspections, no-work-found visits, or items where the quantity wasn't
captured.

---

## 4. Line items per task

Among 95,098 tasks that have at least one DWR line item:

| Line items / task | Tasks | Total line items | % of line items |
|---|---:|---:|---:|
| 1 | 48,364 | 48,364 | 7.6% |
| 2–5 | 30,934 | 87,685 | 13.9% |
| 6–20 | 10,996 | 111,668 | 17.6% |
| 21–50 | 2,616 | 82,628 | 13.1% |
| 51–200 | 1,764 | 165,653 | 26.2% |
| **200+** | **424** | **136,725** | **21.6%** |

Same power-law as transactions: **424 tasks (0.4%) hold 21.6% of all line items.** Roughly half of
all tasks (48,364) have a single line item — one-and-done jobs.

### Line items per task vs assets per task
| Assets on task | Tasks | Avg line items / task | Total line items |
|---|---:|---:|---:|
| 1 | 68,169 | 2.2 | 148,661 |
| 2–5 | 14,630 | 5.3 | 77,884 |
| 6–20 | 5,414 | 16.2 | 87,478 |
| 20+ | 1,571 | 63.4 | 99,591 |
| **0 (blanket)** | **5,314** | **41.2** | **219,109** |

Two drivers of line-item volume:
- **More assets → more line items** (one line per asset per day): 1-asset tasks average 2.2 items;
  20+-asset tasks average 63.
- **Blanket tasks are line-item factories on their own:** 5,314 zero-asset tasks average **41.2**
  line items each and account for **219,109 line items — 34.6% of the entire DWR stream** — by
  accumulating daily entries with no asset to spread across. (Note: of the 8,187 total blanket
  tasks, only 5,314 carry DWR line items; the rest are equipment/other-cost only.)

---

## 5. Cadence

### 5a. Reporting lag — how long after the work is it entered?
`DATEDIFF(day, AccomplishmentDate, CreatedOn)`:

| Lag | Line items | % |
|---|---:|---:|
| Negative (entered before/for future date) | 192 | 0.03% |
| Same day | 4,299 | 0.7% |
| **1–3 days** | **511,916** | **80.9%** |
| 4–7 days | 71,254 | 11.3% |
| 8–30 days | 28,499 | 4.5% |
| 30+ days | 13,998 | 2.2% |

**81% of work is entered 1–3 days after it's performed.** Crews do *not* enter in real time
(same-day is <1%); they batch entry within the same work-week. ~7% trickles in beyond a week (late
corrections/backfill). This is a healthy, consistent reporting discipline with a short, predictable
lag — good for near-real-time reporting as long as you allow a ~3-day settling window.

### 5b. Day-of-week rhythm (`AccomplishmentDate`)
| Day | Line items |
|---|---:|
| Sun | 17,042 |
| Mon | 116,217 |
| Tue | 125,047 |
| Wed | **127,119** |
| Thu | 122,717 |
| Fri | 106,761 |
| Sat | 17,820 |

A textbook Mon–Fri operation peaking midweek (Wed), tapering Friday. **Weekend activity is ~14% of
a weekday** (~35K weekend items total) — consistent with emergency call-outs and winter snow/ice
response rather than routine scheduled work.

### 5c. Monthly volume & seasonal completeness (the important nuance)
| Month | Line items | % w/ asset | % w/ mileposts | % zero-acc |
|---|---:|---:|---:|---:|
| 2024-07 | 31,367 | 73.3 | 61.8 | 9.5 |
| 2024-08 | 35,348 | 76.3 | 55.7 | **21.2** |
| 2024-10 | 29,280 | 72.7 | 64.2 | 5.4 |
| 2024-12 | 23,439 | 54.6 | 44.8 | 2.5 |
| **2025-01** | 31,490 | **42.5** | **33.6** | 1.7 |
| 2025-06 | 28,650 | 75.2 | 67.6 | 1.8 |
| 2025-07 | 31,043 | 76.0 | 68.5 | 2.3 |
| 2025-12 | 24,832 | 48.7 | 40.0 | 4.0 |
| **2026-01** | 26,926 | **45.1** | 36.7 | 2.1 |
| 2026-06 | 17,283 | 73.7 | 68.8 | 2.2 |

Volume is steady (~20K–35K items/month), but **asset/milepost completeness swings hard with the
seasons**: ~75% asset-linked in summer, collapsing to **~42–48% every January** (peak snow & ice,
when work shifts to assetless blanket operations). **This is a work-mix effect, not deteriorating
data quality** — crews aren't getting sloppier in winter; they're doing fundamentally
non-asset-located work (plowing routes, spreading salt).

**One genuine data-quality artifact:** **Aug 2024 zero-accomplishment hit 21.2%** — a clear go-live
adoption anomaly (the system started mid-2024). It settles to a stable 2–5% from Sep 2024 onward.

---

## 6. Practical guidance & flags for stakeholders

- **35% of field work cannot be placed on the network** (no asset, no milepost, no From/To). For any
  geospatial / per-asset analysis, this third of the data is invisible. Most of it is legitimate
  blanket operations — but it caps the achievable map coverage at ~65%.
- **Milepost capture is optional and inconsistently done** — 13.6% of asset-linked items skip it. If
  mileposts matter downstream, this is a targeted data-entry fix (the asset/From-To extent is
  already there; only the milepost text is missing).
- **Use `RouteName`** (99.6% filled) as the most reliable coarse-location field; mileposts/From-To
  only for the located 56–65%.
- **Expect a ~3-day reporting lag**; build a settling window into dashboards rather than reading the
  last 72 hours as final.
- **Treat winter completeness dips as expected**, not as a quality regression — segment by season or
  by blanket-vs-asset before judging data discipline.
- **Investigate the Aug 2024 zero-accomplishment spike** only if you need clean go-live history; it's
  isolated and self-corrected.
- **Asset-linked zero-accomplishment (6.4%, 26K items)** is worth a look — these are asset visits
  logged with no measured output (inspections vs. genuinely incomplete entries).

---

## 7. Reusable queries (read-only via OPENQUERY)

**The completeness matrix (§2):**
```sql
SELECT * FROM OPENQUERY([TAMSDW], '
SELECT
  CASE WHEN AssetReferenceId IS NOT NULL THEN ''asset'' ELSE ''no_asset'' END asset,
  CASE WHEN BeginningMilePost IS NOT NULL AND EndMilePost IS NOT NULL THEN ''both_mp''
       WHEN BeginningMilePost IS NOT NULL OR EndMilePost IS NOT NULL THEN ''partial_mp''
       ELSE ''no_mp'' END mp,
  COUNT(*) n
FROM OM_WVDOT.operations.DailyWorkReportLineItem WHERE ValidTo IS NULL
GROUP BY CASE WHEN AssetReferenceId IS NOT NULL THEN ''asset'' ELSE ''no_asset'' END,
  CASE WHEN BeginningMilePost IS NOT NULL AND EndMilePost IS NOT NULL THEN ''both_mp''
       WHEN BeginningMilePost IS NOT NULL OR EndMilePost IS NOT NULL THEN ''partial_mp''
       ELSE ''no_mp'' END');
```

**Zero accomplishments:**
```sql
SELECT * FROM OPENQUERY([TAMSDW], '
SELECT SUM(CASE WHEN Accomplishment=0 THEN 1 ELSE 0 END) zero_acc, COUNT(*) total
FROM OM_WVDOT.operations.DailyWorkReportLineItem WHERE ValidTo IS NULL');
```

**Reporting lag:**
```sql
SELECT * FROM OPENQUERY([TAMSDW], '
SELECT DATEDIFF(day, AccomplishmentDate, CreatedOn) lag_days, COUNT(*) n
FROM OM_WVDOT.operations.DailyWorkReportLineItem
WHERE ValidTo IS NULL AND AccomplishmentDate IS NOT NULL
GROUP BY DATEDIFF(day, AccomplishmentDate, CreatedOn)');
```

**Line items per task & per-asset-bucket:** see §4 (group `DailyWorkReportLineItem` by `TaskId`;
LEFT JOIN a `GROUP BY ReferenceObjectId` of `TaskAssetReference`).

**Monthly completeness/cadence:** see §5c (group by `CONVERT(char(7), AccomplishmentDate, 126)`).

---

*All figures computed directly against `TAMSDW.OM_WVDOT` at analysis time. Re-run §7 to refresh.*
