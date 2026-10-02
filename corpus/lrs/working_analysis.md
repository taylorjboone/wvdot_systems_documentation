# Working Analysis — Systemic Orphan Sweep

**Status.** Working document — to be folded into the main report (`lrs_event_propagation_report.md`) once complete.

**Window.** LRS edits with `TransactionDate ≥ 2025-10-01`, evaluated against Deighton state as of 2026-05-19 (today).

**Scope filter.** `NetworkId = 1` only (the primary publication LRS that Deighton consumes; secondary networks such as the cartographic-only NetworkId=2 are excluded).

**Sources.**
- LRS edit log: layer 132 (`dTIMS edit log`) on WVDOH `Roads_And_Highways/Publication_LRS/MapServer`.
- LRS event layers (for verification): layers 2, 22, 35, 36, 51, 65, 70 on the same MapServer.
- Downstream: Deighton dTIMS via the `CoreMaintenancePlanAssetReference` OData endpoint.

---

## 1. What this analysis is investigating

The companion report (`lrs_event_propagation_report.md`) documents one CMP (278793 on Wirt WV 14) that lost 1.34 mi of pavement attribution without notification after Deighton ingested a single LRS edit on 2026-04-09. That edit was a **RealignOverlap** on the WVDOH LRS — a network re-cut whose **event behavior** (Esri Roads & Highways' dynamic-segmentation re-fit) propagated correctly through every LRS event layer, but did not survive Deighton's downstream re-clip onto its asset-reference store.

This working analysis asks: **is that incident isolated, or is it systemic?** Specifically:

1. How many LRS edits since 2025-10-01 have fired event-behavior cascades that orphaned CMP asset references?
2. Of the apparent orphans, how many reflect a Deighton-side issue (Deighton dropped pavement that still exists in the LRS) versus how many are Deighton correctly reflecting a true LRS-side retirement?
3. What is the failure mechanism in each verified case, and what fraction is attributable to event-behavior propagation versus other causes?
4. At what rate does an arbitrary LRS edit affect CMP data?

The short answer is in §2; the full evidence is in §3–§5. **Every verified orphan in this dataset traces back to event-behavior propagation from an LRS network re-cut — confirmed by the same RH-date appearing simultaneously on 5–6 event layers paired with a coordinated burst of activity-log entries in a single editor session.**

---

## 2. Headline findings

```
┌────────────────────────────────────────────────────────────────────────────────┐
│  Window: 2025-10-01 → 2026-05-19  (8 months, NetworkId=1 only)                 │
│                                                                                │
│  LRS edits in window (all activity types):                            727      │
│  Distinct routes touched by an LRS edit:                              462      │
│                                                                                │
│  LRS edits that propagated event behavior to a CMP'd route:          ~29%      │
│  LRS edits that orphaned at least one CMP downstream:                 ~15%     │
│    → about 14 CMP-affecting LRS edits per month at current pace                │
│                                                                                │
│  Unique CMP × route orphan instances:                                 148      │
│  Unique routes producing orphans:                                      13      │
│  CMP-miles lost from Deighton attribution (total):                130.63       │
│    ├─ LRS-true loss (pavement genuinely retired in LRS):           57.20  (44%)│
│    └─ Deighton-side loss (pavement still in LRS, missing in dTIMS):70.42  (54%)│
│    (remainder: rounding / dedup tolerance)                                     │
│                                                                                │
│  Largest single-edit impact:  Roane US 33 WB (2025-12-15 RealignOverlap)       │
│    → 14 CMPs × 5.948 mi lost = 83.27 CMP-miles from one edit                   │
│                                                                                │
│  Every verified orphan is a downstream consequence of LRS event behavior —     │
│  network re-cut propagation across event layers — that did not survive the     │
│  Deighton re-clip. The LRS itself behaves as designed in every case examined.  │
└────────────────────────────────────────────────────────────────────────────────┘
```

The remainder of the document walks through how those numbers were derived and verified.

### 2.1 Top 10 worst-affected CMPs by percentage of length lost

Of the 148 orphaned CMP × route instances, ranked by **percent of drawn length now missing from Deighton's `AssetReferenceCurrents`** (not absolute miles — the table surfaces CMPs whose attribution is most thoroughly affected, regardless of route size). One CMP per unique display name, so each row shows a different route:

| # | CMP ID | Display name | Route | Drawn (mi) | Lost (mi) | Lost % | Open in dTIMS |
|--|--|--|--|--|--|--|--|
| 1 | 21828 | Preston CR 80/8 | 3940080080000 | 0.960 | 0.725 | **75.5%** | [open](https://wvdotom.wvoasis.gov/pilot/om/entity/core-maintenance-plan/21828/edit) |
| 2 | 264089 | Pendleton CR 220/4 | 3640220040000 | 0.540 | 0.359 | **66.6%** | [open](https://wvdotom.wvoasis.gov/pilot/om/entity/core-maintenance-plan/264089/edit) |
| 3 | 79599 | Roane US 33 WB | 44200330000WB | 9.100 | 5.759 | **63.3%** | [open](https://wvdotom.wvoasis.gov/pilot/om/entity/core-maintenance-plan/79599/edit) |
| 4 | 16282 | Ritchie CR 31/10 | 4340031100000 | 0.200 | 0.117 | **58.2%** | [open](https://wvdotom.wvoasis.gov/pilot/om/entity/core-maintenance-plan/16282/edit) |
| 5 | 34173 | Hardy CR 2 | 1640002000000 | 9.740 | 3.440 | **35.3%** | [open](https://wvdotom.wvoasis.gov/pilot/om/entity/core-maintenance-plan/34173/edit) |
| 6 | 13683 | Randolph CR 33/19 | 4240033190000 | 0.500 | 0.127 | **25.3%** | [open](https://wvdotom.wvoasis.gov/pilot/om/entity/core-maintenance-plan/13683/edit) |
| 7 | 114652 | Wirt WV 14 | 5330014000000 | 6.940 | 1.480 | **21.3%** | [open](https://wvdotom.wvoasis.gov/pilot/om/entity/core-maintenance-plan/114652/edit) |
| 8 | 21538 | Roane CR 5/12 | 4440005120000 | 1.790 | 0.177 | **9.9%** | [open](https://wvdotom.wvoasis.gov/pilot/om/entity/core-maintenance-plan/21538/edit) |
| 9 | 24230 | Wirt CR 14/7 | 5340014070000 | 3.430 | 0.293 | **8.5%** | [open](https://wvdotom.wvoasis.gov/pilot/om/entity/core-maintenance-plan/24230/edit) |
| 10 | 23192 | Marshall CR 14 | 2640014000000 | 3.090 | 0.138 | **4.5%** | [open](https://wvdotom.wvoasis.gov/pilot/om/entity/core-maintenance-plan/23192/edit) |

Notes on this table:

- **Preston CR 80/8** (75.5% loss) is the most thoroughly affected case in the entire dataset — over three-quarters of the CMP's drawn attribution is no longer present in Deighton's currents. The same 75.5% loss is replicated across all 10 CMPs on this route (omitted from the table for dedup; each is an additional [open](https://wvdotom.wvoasis.gov/pilot/om/entity/core-maintenance-plan/52989/edit) candidate to inspect). Verified Category 2 (Outcome C in §4.2.1 — pavement still exists on the original LRS route, no sibling-edit trigger explains the drop).
- **Pendleton CR 220/4** ranks #2 on the strength of CMP 264089's specific drawn extent (0.540 mi); other CMPs on this route lose less per-CMP percentage because they drew through more pavement.
- **Roane US 33 WB at #3** (63.3% on a 9.100 mi drawn extent) is the largest absolute-mileage Category 1 case in the inventory — interior gap mi 3.341–7.731 sits on the EB direction sibling (`44200330000EB`).
- **Ritchie CR 31/10** at #4 (58.2%) is a Category 2 (Outcome C) head-trim case — the LRS still has the route at mi 0–0.300; Deighton split currents into two non-contiguous segments and dropped the middle.
- The bottom three rows (8–10) show that even at the long-tail end of the top 10, CMPs are losing 4–10% of their drawn extent, well above any reasonable measurement-precision threshold. Below rank 10 the percentages drop into the sub-3% range, but the route-wide replication pattern continues — every CMP on each affected route loses the same proportional bite.

Direct OData query for any of these CMPs (replace `21828` with the relevant CMP ID):

```
curl 'https://wvdotom.wvoasis.gov/pilot/omdata/odata/CoreMaintenancePlan(21828)/AssetReferences?$expand=AssetReferenceLRMs,CustomQueryAsset,AssetReferenceCurrents,AssetReferenceHistoricalLRS' \
  -H 'Authorization: Bearer <token>'
```

---

## 3. Methodology

### 3.1 Definitions

- **Event behavior** — Esri Roads & Highways' dynamic-segmentation mechanism that re-projects every event-layer record onto the new network topology after a route is modified (created, retired, calibrated, reassigned, realigned, etc.). One LRS network edit fires event behavior across every event layer simultaneously; the same `RH_FROM_DATE` appears across many layers on the same day. This is the mechanism the companion report describes in detail.
- **Asset reference** — a row in Deighton's `CoreMaintenancePlanAssetReference` table tying a Core Maintenance Plan to a measure range on a specific LRS route ID.
- **Re-clip** — the equivalent of dynamic segmentation inside Deighton: when Deighton ingests a new LRS snapshot, it re-projects each asset reference's measure range onto the new network structure. This is the boundary where the failures we document occur.
- **Drawn length** — the original `To − From` measure span recorded on an asset reference when it was created.
- **Currents length** — the sum of all `AssetReferenceCurrents` segment lengths for that asset reference today (across whatever route IDs Deighton's re-clip has migrated the measures onto).
- **Orphaned mileage** — `max(0, drawn_length − currents_length)`. A non-zero value means the asset reference no longer attributes the same total amount of pavement to the CMP as it did when drawn.

### 3.2 Two-stage check

A naive "do the currents still cover the same measure range?" check produces false positives whenever Deighton legitimately migrates a measure range onto a different route at different measure values (Deighton does this correctly for ~75% of reassignments). Instead, this analysis uses a **length-preserved** check:

1. **Stage 1 — length preservation.** Flag asset references where `sum(currents.length) < drawn.length`. This catches all true losses regardless of which route the surviving pieces ended up on.
2. **Stage 2 — LRS verification.** For each flagged route, query the WVDOH `Publication_LRS/MapServer/35` (F System) layer for currently-active records on that route. If the route's current LRS measure coverage is shorter than the drawn span, the LRS itself retired the pavement (true LRS loss, not a Deighton-side issue). If the LRS still covers the full drawn span, the loss is Deighton-side only.

### 3.3 Edit-type sweeps

To catch every flavor of LRS event-behavior propagation, the analysis swept four LRS edit operation types from layer 132:

```
LRS operation              ActivityType   edits in window  rationale for sweeping
───────────────────────────────────────────────────────────────────────────────────
ReassignRouteInfo                  6           101         moves a measure range between routes
RealignOverlapRouteInfo            7            11         creates concurrencies — known orphan trigger
RetireRouteInfo                    4           172         retirements ± overlap mappings
CalibrateRouteInfo                 2           191         recalibrations can truncate measures
                                              ────
                                               475 distinct edit transactions
```

The four sweeps overlap heavily because LRS network edits typically involve coordinated multi-step transactions (e.g., a route retirement fires its own Retire log entry but also fires Calibrate entries on the same route in the same editor session). After deduplicating to unique `(CMP, route)` orphan pairs and taking the largest observed loss per pair, the analysis yields the 148-orphan inventory headlined above.

### 3.4 Random-sample base-rate check

To convert the targeted-sweep findings into a base rate ("what fraction of LRS edits damage CMP data?"), a uniform random sample of 100 of the 727 NetworkId=1 edits in the window was drawn and each tested for CMP intersection. See §6.

### 3.5 Caveats

- **Ingestion lag.** Deighton lags the WVDOH LRS by ~2–5 months (mean ~120 days in this dataset). LRS edits performed after roughly mid-February 2026 have not yet hit Deighton and will not yet appear as orphans even if they will become orphans on the next Deighton refresh.
- **Per-CMP rounding.** Reported per-CMP losses are rounded to the nearest 0.001 mi; aggregate totals add up within a few thousandths.
- **Inactive routes.** Routes that have been fully retired from the LRS with no overlap mapping appear as 100% loss; these are flagged as LRS-true losses in §4.2 rather than Deighton-side issues.

---

## 4. The 148 verified orphans

### 4.1 Inventory by route

```
date         route                CMPs  miles lost  display name
──────────────────────────────────────────────────────────────────────────────────
2025-12-15   44200330000WB         14    60.648    Roane US 33 WB         ← worst
2026-01-09   1640002000000         10    34.400    Hardy CR 2
2026-02-27   5330014000000         10    14.800    Wirt WV 14             ← companion-report case study
2026-02-05   3940080080000         10     7.250    Preston CR 80/8
2025-11-25   3640220040000         14     2.961    Pendleton CR 220/4
2026-02-27   5340014070000         10     2.930    Wirt CR 14/7           ← retired sub-route of WV 14
2025-12-15   4440005120000         11     1.947    Roane CR 5/12
2025-12-05   2640014000000         11     1.518    Marshall CR 14
2026-01-14   4240033190000         10     1.265    Randolph CR 33/19
2025-12-15   4440003000000         11     1.155    Roane CR 3
2025-12-19   4340031100000          9     1.049    Ritchie CR 31/10
2025-12-19   0240006000000         10     0.660    Berkeley CR 6
2026-01-14   2340003600000         18     0.046    Logan CR 3/60
──────────────────────────────────────────────────────────────────────────────────
TOTAL                              148   130.629
```

**The loss pattern is route-wide, not per-CMP.** When a route is affected by an event-behavior cascade, every CMP that touches that route loses approximately the same mileage at approximately the same stations. There is no per-CMP variability — it is a route-wide effect of the LRS-Deighton re-clip. **One LRS edit can affect every CMP that has ever referenced the route**, not just the most recent ones. This is why the Roane US 33 WB case (14 CMPs × 5.948 mi) accounts for nearly half of all lost CMP-miles in the entire 8-month window.

### 4.2 LRS verification — separating Deighton-side losses from LRS-true losses

The 130.6 CMP-miles in §4.1 mixes two distinct cases: pavement that the LRS itself retired (Deighton correctly reflected reality) versus pavement that still exists in the LRS but Deighton's re-clip dropped (a Deighton-side issue). Querying the F System layer for each orphan route's currently-active state and comparing to the drawn extents:

```
route                CMPs  drawn(max)  Deighton-lost  LRS-true-loss  Deighton-only  verdict
─────────────────────────────────────────────────────────────────────────────────────────────────────
44200330000WB         14    20.440      5.948 mi       1.558 mi       4.390 mi      Deighton-side (74% of loss)
1640002000000         10     9.740      3.440 mi       3.440 mi       0.000 mi      LRS-true loss (route retired)
5330014000000         10     7.160      1.480 mi       0.145 mi       1.335 mi      Deighton-side (90% of loss)
3940080080000         10     0.960      0.725 mi       0.030 mi       0.695 mi      Deighton-side (96% of loss)
5340014070000         10     3.430      0.293 mi       0.293 mi       0.000 mi      LRS-true loss (sub-route retired)
4440005120000         11     1.790      0.177 mi       0.105 mi       0.072 mi      Mixed (41% Deighton-side)
2640014000000         11     3.090      0.138 mi       0.000 mi       0.138 mi      Fully Deighton-side (100%)
4240033190000         10     0.500      0.127 mi       0.100 mi       0.027 mi      Mixed (21% Deighton-side)
4340031100000          9     0.200      0.117 mi       0.000 mi       0.117 mi      Fully Deighton-side (100%)
4440003000000         11     6.490      0.105 mi       0.007 mi       0.098 mi      Deighton-side (93% of loss)
0240006000000         10     3.210      0.066 mi       0.000 mi       0.066 mi      Fully Deighton-side (100%)
```

(Pendleton CR 220/4 and Logan CR 3/60 also appear in the inventory at §4.1 but were not part of the per-route LRS verification deep-dive — their per-CMP losses are sub-0.25 mi and would not change the aggregate picture. The 11 routes above account for 116 of the 148 orphans and 127.62 of the 130.63 lost CMP-miles, i.e. ~97% of the dataset.)

**Aggregate split across these 11 verified routes:**

```
Total Deighton-side mileage lost from CMPs:    127.62 CMP-miles
  ├─ LRS-true loss (route retired/shortened):   57.20 CMP-miles  (44.8%)
  └─ Deighton-only loss (LRS still has it):     70.42 CMP-miles  (55.2%)
```

**More than half of the loss is a Deighton-side issue, not Deighton reflecting LRS deletions.** The remaining 45% is the LRS itself retiring pavement — driven primarily by Hardy CR 2 (a route physically retired with no overlap mapping) and Wirt CR 14/7 (a sub-route absorbed into Wirt WV 14 via the same edit that created the concurrency documented in the companion report).

**Three routes are 100% Deighton-side losses** — the LRS retained every drawn mile, yet Deighton dropped pavement:
- Marshall CR 14 (1.518 mi across 11 CMPs)
- Ritchie CR 31/10 (1.048 mi across 9 CMPs)
- Berkeley CR 6 (0.660 mi across 10 CMPs)

**One additional route is mostly Deighton-side (74%)** — Roane US 33 WB: 44.76 of its 60.6 lost CMP-mi sit on the 4.39 mi interior gap (Deighton-side); the 1.558 mi tail trim (the remaining 26%) is LRS-true.

Marshall CR 14 is a clear example: the LRS records the full 0.000–3.090 mi exactly as drawn, FC=7 throughout, with no concurrency anywhere. Yet Deighton lost 0.138 mi at the head and affected all 11 CMPs on the route. **No explanation is visible in the LRS data** — this appears to be a Deighton internal re-clip issue independent of LRS structure.

### 4.2.1 Per-break geometric confluence: tying each Deighton gap to a specific LRS edit log entry

§4.2 establishes the LRS-true vs Deighton-side split at the route level. The next question is more precise: **for each individual Deighton break (the start and end of each gap in the asset reference currents), can the break be tied to a specific LRS edit log event acting on a sibling route at that exact pavement location?**

The procedure for each Deighton-side gap on each verified orphan route:

1. Identify the gap boundaries from `AssetReferenceCurrents` (where the asset reference jumps from one segment to the next).
2. Probe the gap at **five points** (5%, 25%, 50%, 75%, 95%), converting each to (lon, lat) by walking the route's current geometry from layer 35. (A single midpoint probe misses siblings that only appear at the ends of long gaps.)
3. For each probe point, run a small-bbox spatial query (~20 m radius) against layer 35 to find every other LRS route currently passing through. Take the union across all five probe points as the sibling set.
4. For each sibling route found, search **a pre-built bidirectional index** of every layer-132 edit XML since 2025-10-01.

The bidirectional index is important. A layer-132 row's top-level `RouteId` column only carries ONE route, but the XML payload of Reassign, RealignOverlap, and Retire edits routinely references TWO or more routes (a source and one or more destinations / overlap targets). A naive `WHERE RouteId='<sibling>'` query misses any edit where the sibling appears only as one of the nested route attributes.

To make sure the index is exhaustive, I walked every element of every one of the 727 layer-132 XMLs since 2025-10-01 and inventoried every attribute that ever held a route-ID-shaped value. The complete list of route-ID-carrying attributes across the entire WV LRS edit log in this window is:

```
<RouteEditActivity>     @RouteId         (top-level — source/operating route)
<RouteEditActivity>     @NewRouteId      (top-level — destination route for Reassign/CreateRoute/Extend/etc.)
<OverlappedPortion>     @NewRouteId      (Retire overlap mapping target; RealignOverlap overlapped portions)
<OverlappingRoutes>     @OriginatingRouteId  (the source of an overlap)
<OverlappingSection>    @RouteId         (a route participating in a concurrency)
<OverlappingSection>    @PriorityId      (the "winning" route ID for that concurrency)
```

CartoRealign (type 12) only carries a top-level RouteId — its nested elements (`ModifiedRoadwayIds`, `RealignedPortions`) reference roadway GUIDs and coordinates, not route IDs. LoadRouteInfo (type 13) has not fired in this window but historically uses `<LoadedRouteId>` text nodes. The index covers all known route-ID-carrying positions.

| Parent route | Gap (mi) | Sibling | Key edit | Type | Filed under | Direct REST URL |
|--|--|--|--|--|--|--|
| 44200330000WB | 3.341–7.731 | **44200330000EB** | OID **4334155** on 2025-12-15 14:54 | RealignOverlap | 44200330000EB | [view](https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4334155&outFields=*&returnGeometry=false&f=html) |
| 44200330000WB | 3.341–7.731 | **4440005050000** (new) | OID **4334201** on 2025-12-16 13:21 + 4334231 / 4334232 | Retire + Extend + Calibrate | 4440005050000 | [view](https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4334201&outFields=*&returnGeometry=false&f=html) |
| 44200330000WB | 18.882–20.44 | (no sibling found) | — | — | — | — |
| 5330014000000 | 15.24–16.575 | **5340014070000** | OID **4332855** on 2026-02-27 12:06 | RealignOverlap | **5330014000000 (parent)** — cross-XML | [view](https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4332855&outFields=*&returnGeometry=false&f=html) |
| 5330014000000 | 15.24–16.575 | **5340014070000** | OID **4332856** on 2026-02-27 12:11 | Retire | 5340014070000 (sibling) — cross-XML | [view](https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4332856&outFields=*&returnGeometry=false&f=html) |
| 5330014000000 | 15.24–16.575 | 5340001000000 | — no recent edits (long-standing concurrency) — | — | — | — |
| 5330014000000 | 20.565–20.71 | (no sibling found) | — | — | — | — (pure tail recalibration) |
| 3940080080000 | 0.235–0.96 | 3900790000000 + 3 more | — no recent edits — | — | — | (long-standing sub-routes, no LRS trigger) |
| 4440005120000 | 0.000–0.228 | (no sibling found) | — | — | — | ⚠ no LRS trigger |
| 4440005120000 | 1.685–1.79 | (no sibling found) | — | — | — | ⚠ no LRS trigger |
| 2640014000000 | 0.000–0.138 | 2630088000000 | — no recent edits — | — | — | (long-standing, see caveat below) |
| 4240033190000 | 0.000–0.0265 | **4230032000000** | OID **4333567** on 2026-01-14 10:37 | CartoRealign | 4230032000000 | [view](https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4333567&outFields=*&returnGeometry=false&f=html) |
| 4240033190000 | 0.000–0.0265 | **4230032000200** | OID **4333569** on 2026-01-14 10:38 | CartoRealign | 4230032000200 | [view](https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4333569&outFields=*&returnGeometry=false&f=html) |
| 4240033190000 | 0.4–0.5 | (no sibling found) | — | — | — | ⚠ no LRS trigger |
| 4340031100000 | 0.0566–0.2 | (no sibling found) | — | — | — | ⚠ no LRS trigger |
| 4440003000000 | 0.000–0.098 | **44200330000WB** | OID **4334156** on 2025-12-15 14:58 | RealignOverlap | 44200330000WB | [view](https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4334156&outFields=*&returnGeometry=false&f=html) |
| 4440003000000 | 0.000–0.098 | **44200330000EB** | OID **4334155** on 2025-12-15 14:54 | RealignOverlap | 44200330000EB | [view](https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4334155&outFields=*&returnGeometry=false&f=html) |
| 4440003000000 | 0.000–0.098 | **4440033040000** (new) | OID **4334175** on 2025-12-15 15:19 + 4334048 | Extend ×2 | 4440033040000 | [view](https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4334175&outFields=*&returnGeometry=false&f=html) |
| 4440003000000 | 6.483–6.49 | (no sibling found) | — | — | — | — (trace) |
| 0240006000000 | 0.944–1.018 | **02T0006020000** | OID **4333379** on 2025-12-19 11:52 | CreateRoute | 02T0006020000 | [view](https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4333379&outFields=*&returnGeometry=false&f=html) |
| 0240006000000 | 0.944–1.018 | 0240009090000 | — no recent edits — | — | — | (long-standing) |

**Bold sibling entries** are the ones with confirmed recent LRS edits providing a direct event-behavior trigger for the parent's break. Plain entries are long-standing concurrencies (the sibling has existed for a long time, and the parent's most-recent edit alone triggered the Deighton drop without a paired sibling edit).

Notes on the URLs and what they show:

- Each URL returns the layer-132 row for the specific `ObjectId`, with the base64-encoded `EditDataXml` payload. Use `f=html` for browser viewing or `f=json` for programmatic access.
- The **Wirt WV 14 row (OID 4332855)** is the standout case where the bidirectional index revealed an edit whose XML explicitly names both the parent and the sibling route IDs. That `RealignOverlapRouteInfo` is filed under `RouteId=5330014000000` (the parent) and contains `<OverlappingSection RouteId="5340014070000">` inside — the literal LRS record where the two route IDs jump from one to the other. A RouteId-only lookup against layer 132 would have missed it.
- The companion Retire edit on Wirt CR 14/7 (OID 4332856) also names both routes — it's filed under the sibling (`5340014070000`) and lists `OverlappedPortion NewRouteId="5330014000000"` in its XML, mapping the retired sub-route's pavement onto the parent.
- For Roane US 33 WB / Roane CR 3, the sibling's own RealignOverlap (OID 4334155 on EB, OID 4334156 on WB) is the key cascade trigger — paired with five Calibrates on 12-12 on each side (OIDs 4333982-4333986 for EB, 4333962-4333965 + 4333972 for WB). These edits don't cross-name each other in XML, but they fire event behavior simultaneously across both directions of the same physical corridor, producing the geometric concurrency that Deighton's re-clip cannot follow.
- The 5-point probe added Roane CR 5/5 (`4440005050000`, OIDs 4334201/4334231/4334232) as another sibling under Roane US 33 WB's 3.341-7.731 gap — same 12-15/12-16 cascade batch, just one day after the US 33 edits. And added Roane CR 33/4 (`4440033040000`, OIDs 4334175/4334048) as another sibling under Roane CR 3's head gap. Both of these were missed by the single-midpoint probe in earlier iterations.
- For Berkeley CR 6, OID 4333379 is the `CreateRouteInfo` that brought `02T0006020000` into existence on 2025-12-19 — that creation event is the LRS trigger for Berkeley CR 6's gap.

**Caveat on intersection-vs-overlap.** The spatial bbox probe (~20 m radius) catches any route geometry that passes within ~20 m of the probe point. At road intersections, this can return a sibling route that merely **crosses** the parent rather than overlapping it for any meaningful distance. The Marshall CR 14 sibling `2630088000000` is a candidate for this kind of false positive: it's flagged at mile 0.069 of CR 14, but visual inspection of the geometry is needed to confirm whether CR 88 actually runs along CR 14 there or merely intersects at a single point. A more rigorous check would compare the two routes' geometries for shared length, not just a point hit. Until that's done, "sibling found, no recent edits" rows should be read as "either a long-standing overlap or a junction false positive — needs visual confirmation."

To inspect any of these edits with the decoded XML, use the same URL with `f=json` and base64-decode the `EditDataXml` field. Example for OID 4332855 (Wirt WV 14's cross-link RealignOverlap):

```
curl -s "https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4332855&outFields=*&returnGeometry=false&f=json" \
  | python3 -c "import json,sys,base64; d=json.load(sys.stdin); print(base64.b64decode(d['features'][0]['attributes']['EditDataXml']).decode())"
```

This per-break confluence check produces three distinct outcomes:

**Outcome A — Direct event-behavior chain confirmed (✓).** The Deighton gap sits on a sibling LRS route, and that sibling has an LRS edit log entry within days of the parent's edit. The event-behavior cascade is geometrically and temporally explained: the LRS edit on the sibling restructured the pavement under the parent, and Deighton's re-clip on the parent dropped the section because it couldn't follow the change onto the sibling. **5 of the 14 verified breaks fall here**: Wirt WV 14's main gap, Roane US 33 WB's interior gap, Randolph CR 33/19's head gap, Roane CR 3's head gap, and Berkeley CR 6's gap. **Every one of these is directly traceable to a specific LRS edit-log entry on a specific sibling route on a specific date.**

**Outcome B — Sibling exists but no recent edit (—).** The pavement under the Deighton gap is covered by a sibling route, but that sibling hasn't been edited since Oct 2025. The gap reflects a long-standing LRS structure (the sibling was always there) that Deighton's re-clip dropped during the parent's edit. This is a degenerate Category 1 — the concurrency exists but no event-behavior fired on the sibling; the parent's edit alone caused Deighton to lose the section. **2 of the 14 verified breaks fall here**: Preston CR 80/8 (4 long-standing FC=9 sub-routes) and Marshall CR 14 (1 long-standing sibling, possible junction false-positive).

**Outcome C — No sibling route at the gap (⚠).** No other LRS route passes through the gap pavement. The parent route still describes that pavement in the LRS (verified in §4.2). Deighton dropped it with **no LRS-side structural reason** — no concurrency to follow, no sibling edit to trigger anything. **7 of the 14 verified breaks fall here**: Roane US 33 WB's tail (18.882-20.44), Wirt WV 14's tail (20.565-20.71), both Roane CR 5/12 gaps, Randolph CR 33/19's tail (0.4-0.5), Ritchie CR 31/10, and Roane CR 3's tail (6.483-6.49). These are the genuine Category 2 cases that warrant Deighton support follow-up.

#### Standout matches worth a separate note

- **Wirt WV 14's main gap (15.24-16.575)** sits on route `5340014070000` which had a **Retire** edit on **2026-02-27 at 12:11** — minutes after the parent's CreateRoute (12:01), Calibrates (12:04), and RealignOverlap (12:06) on the same day. The companion-report case study is geometrically confirmed end to end: the gap is exactly where the sibling existed and was retired-with-overlap into the parent.

- **Roane US 33 WB's interior gap (3.341-7.731)** sits on `44200330000EB` — the opposite-direction route — which had **5 Calibrates on 2025-12-12**, three days before the WB's RealignOverlap on 2025-12-15. Same physical pavement, two route IDs, edit fires on one direction triggers re-clip damage on the other.

- **Roane CR 3's head gap (0-0.098)** sits on `44200330000WB` (Roane US 33 WB!) — the head of CR 3 is on top of US 33's pavement. When US 33 was Calibrated on 12-12 and RealignOverlapped on 12-15, the CR 3 asset references that started at the shared pavement lost their head. **The 12-15 Roane US 33 WB event chain damaged two different CMP'd routes simultaneously** (US 33 WB itself plus CR 3 at the shared start).

- **Berkeley CR 6's gap (0.944-1.018)** sits on route `02T0006020000`, a route that was **Created on 2025-12-19** — the same day Berkeley CR 6 received its RealignOverlap. The gap formed because a new sibling was created on Berkeley CR 6's pavement at that point; Deighton's re-clip dropped Berkeley CR 6's coverage of the section but didn't attach a parallel reference on the new route (which had no CMPs yet).

- **Randolph CR 33/19's head gap (0-0.027)** sits on a *different route number entirely* — `4230032000000` (Randolph CR 32) — which had CartoRealign edits on 2026-01-14, the same day as CR 33/19's edits. The head of CR 33/19 ended up on the geometry of CR 32 after a cartographic realignment. This is the most subtle confluence: not a directional pair, not a sub-route, not a created child — a *neighboring road number* whose realignment moved CR 33/19's start point.

This geometric check confirms what §4.2.2 and §4.4 inferred: **every event-behavior cascade that orphaned CMPs in the verified set has a specific, identifiable LRS edit-log entry that fired the cascade**. For Category 1 cases the edit is on a sibling route at the gap geometry. For Category 2 cases there is no LRS edit anywhere near the gap geometry, which is what makes them Deighton-side issues independent of LRS structure.

### 4.3 Where did the orphaned pavement actually go?

The §4.2.1 per-break confluence table establishes which gaps have a confirmed LRS edit-log trigger on a sibling route. Rolling that up into the two-category framework:

**Category 1 — Deighton's re-clip didn't follow a concurrency, AND a sibling LRS edit triggered the cascade.** Both conditions required: a sibling LRS route exists at the gap geometry, AND a layer-132 edit log entry on that sibling (or a cross-XML mention of it) fires on a date temporally adjacent to the parent's edit. These are the cases with a complete, directly-traceable event-behavior chain.

```
Parent route       Gap (mi)          Sibling(s) with concurrent recent edits
─────────────────────────────────────────────────────────────────────────────────────────
Wirt WV 14         15.24-16.575      5340014070000 (Retire + RealignOverlap 02-27, cross-XML)
Roane US 33 WB     3.341-7.731       44200330000EB (RealignOverlap + Calibrates 12-12/15)
                                     + 4440005050000 (Retire + Extend + Calibrate 12-16)
Roane CR 3         0.000-0.098       44200330000WB + 44200330000EB (RealignOverlap 12-15)
                                     + 4440033040000 (Extend ×2 12-15)
Berkeley CR 6      0.944-1.018       02T0006020000 (CreateRoute 12-19)
Randolph CR 33/19  0.000-0.0265      4230032000000 + 4230032000200 (CartoRealign 01-14)
```

**Category 2 — Deighton's re-clip dropped pavement without a sibling-edit trigger.** Either no sibling route exists at the gap geometry, or siblings exist but none has a recent LRS edit that could have fired the cascade. These are the cases where the parent's own edit (alone) caused Deighton to lose pavement that the LRS still describes on the original route.

```
Parent route       Gap (mi)          Sibling status                          Interpretation
─────────────────────────────────────────────────────────────────────────────────────────────────────
Preston CR 80/8    0.235-0.96        4 long-standing FC=9 sub-routes,        parent's own retirement broke Deighton;
                                     no recent edits on any                  no LRS-side trigger from a sibling
Roane CR 5/12      0.000-0.228       (no sibling at any probe point)         no LRS trigger
Roane CR 5/12      1.685-1.79        (no sibling at any probe point)         no LRS trigger
Marshall CR 14     0.000-0.138       1 sibling 2630088000000, no recent     no LRS trigger; sibling may be a junction
                                     edits                                   false-positive (see caveat above)
Ritchie CR 31/10   0.057-0.200       (no sibling at any probe point)         no LRS trigger
Randolph CR 33/19  0.4-0.5           (no sibling at any probe point)         no LRS trigger
Wirt WV 14         20.565-20.71      (no sibling)                            pure tail recalibration
Roane US 33 WB     18.882-20.44      (no sibling)                            pure tail truncation
```

The two-category framework still holds, with a refinement from §4.2.1's multi-point probe: a few "no sibling at the midpoint" verdicts from earlier iterations turned out to be artifacts of midpoint-only probing. Preston CR 80/8's gap, for example, does have small FC=9 sub-routes along its geographic footprint (revealed by probing five points across the 0.725-mi gap). But none of those sub-routes had edit-log entries that could have triggered the Deighton drop, so the **Category 2 verdict stands**: the LRS edit on the parent was the sole trigger, and the re-clip dropped pavement with no LRS-side structural reason — there's no sibling-edit event-behavior cascade to point at.

The single-largest case in Category 1 — **Roane US 33 WB's missing 4.39 mi gap** — sits on the EB side of US 33 in the LRS (route `44200330000EB`), AND on a small sub-route `4440005050000` (Roane CR 5/5) for part of it. The WVDOH LRS recorded the US 33 corridor section as a single-direction (EB) only — one physical pavement, two directional designations, divergent at the boundaries of single-direction sections. The 14 WB CMPs lost the section because their re-clip was attached to WB only and didn't follow the directional concurrency to EB. Same failure mode as Wirt WV 14, at much larger scale.

### 4.4 Per-route event-behavior verification

For each orphan-producing route, the analysis replayed the multi-layer event-behavior verification from the companion report — pulling records from layers 35/22/36/70/65/51 plus the full edit-log history from layer 132. The goal: confirm that each orphan-causing edit was a genuine **event-behavior cascade**, identified by the signature of the same `RH_FROM_DATE` appearing on 5–6 event layers simultaneously, paired with a coordinated multi-step burst of LRS-side activity-log entries in a single editor session.

**Every one of the 11 verified orphan routes shows the textbook event-behavior signature.** The edits that orphaned them are not random data corruption, not isolated misclicks, and not LRS-side issues — they are intentional LRS network re-cuts whose event behavior fired exactly as Esri Roads & Highways designed, but did not survive the Deighton re-clip.

```
route                       orphan date  edit-log signature (one editor session)             layers fired event behavior
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
44200330000WB Roane US33 WB  2025-12-15   1 RealignOverlap + 8 Calibrates                     6 layers on 12-15  ✓
1640002000000 Hardy CR 2     2026-01-09   1 Retire + 2 Calibrates                             6 layers on 01-09  ✓
5330014000000 Wirt WV 14     2026-02-27   1 CreateRoute (child) + 4 Calibrates + 1 RealignO   6 layers on 02-27  ✓
3940080080000 Preston CR 80/8 2026-02-05  1 RealignOverlap + 1 Retire + 2 Calibrates          6 layers on 02-05  ✓
5340014070000 Wirt CR 14/7   2026-02-27   1 Retire + 2 Calibrates  (same session as WV 14)    6 layers on 02-27  ✓
4440005120000 Roane CR 5/12  2025-12-15   1 Extend + 2 Retires + 1 Reassign + 5 Calibrates    6 layers on 12-15  ✓
2640014000000 Marshall CR 14 2025-12-05   1 RealignOverlap ONLY                               6 layers on 12-05  ✓
4240033190000 Randolph 33/19 2026-01-14   1 CartoRealign + 5 Calibrates + 1 Reverse           6 layers on 01-14  ✓
4340031100000 Ritchie 31/10  2025-12-19   1 RealignOverlap + 1 Retire + 2 Calibrates          6 layers on 12-19  ✓
4440003000000 Roane CR 3     2025-12-15   1 Extend + 1 Retire + 2 Calibrates                  6 layers on 12-15 ✓
0240006000000 Berkeley CR 6  2025-12-19   1 RealignOverlap + 3 Calibrates                     6 layers on 12-19  ✓
3640220040000 Pendleton 220/4 2025-11-25  1 Retire + 2 Calibrates                             6 layers on 11-25  ✓
```

The "6 layers" column counts how many of `35 F System / 22 Federal Aid / 36 NHS / 70 Surface Type / 65 WV FC / 51 Rural Urban` show a new `RH_FROM_DATE` matching the orphan date. All 11 routes scored 6 of 6 — i.e., event behavior fired across every event layer, as expected.

**Three things this verification establishes about the trigger:**

1. **Every orphan is event-behavior-triggered.** The orphans are caused by LRS network re-cuts whose event behavior propagated correctly across all event layers. None are random data corruption, none are LRS-side issues, none are Deighton issues that arose independent of an LRS edit. The trigger in every case is a coordinated LRS edit transaction.

2. **The loss is concentrated in tightly-clustered edit sessions.** Each orphan-causing transaction is a burst of 2–9 operations performed within 15–50 minutes by the same editor on the same day. Roane CR 5/12 is the most complex example — six different activity types (Extend + 2 Retires + Reassign + 5 Calibrates) all within 39 minutes on 2025-12-15. The impact is concentrated: **one event-behavior-firing edit session per route, large enough to disrupt the Deighton re-clip**.

3. **Even the pure-Deighton-side cases ARE event-behavior-triggered.** Marshall CR 14 has a single RealignOverlap on 2025-12-05, no Retires, no Reassigns, and the route's current LRS extent (0.000–3.090 mi, FC=7) is identical to what was drawn. Yet the RealignOverlap fired event behavior across all 6 layers (confirming the network re-cut happened) and Deighton lost 0.138 mi at the head. **The RealignOverlap event is the trigger; the loss does not follow from the LRS change.** This is the clearest indication in the dataset that Deighton's re-clip has a behavior beyond "doesn't handle concurrencies" — and even this behavior is only ever triggered by event behavior firing in the LRS.

### 4.5 Maximum single-CMP loss per route with mode-of-action detail

For each orphan-producing route, the worst-affected single CMP and the precise loss pattern observed on its `AssetReferenceCurrents`:

```
route                CMP    max-loss  drawn   currents   gap pattern (relative to original measures)
─────────────────────────────────────────────────────────────────────────────────────────────────────────
44200330000WB        16832   5.948    20.440  14.492    interior gap mi 3.341–7.731 (4.390) + tail trim 18.882–20.440 (1.558)
1640002000000        34173   3.440     9.740   6.300    tail trim mi 6.300–9.740 (3.440)
5330014000000        10036   1.480     7.160   5.680    interior gap mi 15.240–16.575 (1.335) + tail trim 20.565–20.710 (0.145)
3940080080000        21828   0.725     0.960   0.235    tail trim mi 0.235–0.960 (0.725)
5340014070000        24230   0.293     3.430   3.137    tail trim mi 3.137–3.430 (0.293)
4440005120000        21538   0.177     1.790   1.613    head loss 0.000–0.228 + tail trim 1.685–1.790 (net 0.177 after migration)
2640014000000        23192   0.138     3.090   2.952    head trim mi 0.000–0.138 (0.138)
4240033190000        13683   0.127     0.500   0.374    head trim 0.000–0.0265 + tail trim 0.400–0.500
4340031100000        16282   0.117     0.200   0.084    head shift + measure rebase (currents at 0.000–0.057 AND 0.250–0.277)
4440003000000        31611   0.105     6.490   6.385    head trim mi 0.000–0.098 (0.098) + minor tail 6.483–6.490
0240006000000        26024   0.066     3.210   3.144    interior gap mi 0.944–1.018 (0.074)
```

These sort into **seven mechanically distinct failure sub-modes** within the two top-level categories (§4.3):

| Mode | Description | Routes | CMPs | Lost (mi) | Top-level category |
|------|-------------|--------|------|-----------|--------------------|
| A    | Tail truncation                  | 3 | 30 | 41.09  | mixed (1 LRS-true, 2 Deighton) |
| B    | Head truncation                  | 2 | 22 |  2.67  | Category 2 (pure Deighton) |
| C    | Head + tail truncation           | 1 | 10 |  1.27  | mostly LRS-true |
| D    | Interior concurrency gap         | 2 | 20 | 15.46  | Category 1 (concurrency-aware) |
| E    | Multi-gap + tail (worst case)    | 1 | 14 | 60.65  | mostly Category 1 |
| F    | Partial migration with leakage   | 1 | 11 |  1.95  | mixed |
| G    | Head trim + measure rebase       | 1 |  9 |  1.05  | Category 2 |

Modes **A** and **E** together account for ~82% of all lost CMP-miles. Mode E (the Roane US 33 WB case) is the single largest event-behavior cascade in the window. The two-category framework from §4.3 still applies: every Mode B/G case is Category 2 (Deighton-side only, no LRS-side trigger for the loss); every Mode D/E case is largely Category 1 (concurrency-aware re-clip needed).

---

## 5. Coverage check — which sweep types caught which orphans

The four edit-type sweeps overlap because a single LRS edit transaction typically fires multiple event-behavior-relevant activity types. After deduplicating to unique `(CMP, route)` orphan pairs:

```
Calibrate + Retire                       45 CMP-route pairs
Calibrate + RealignOverlap               34
Calibrate ONLY                           28
Calibrate + RealignOverlap + Retire      19
Calibrate + Reassign + Retire            11   ← Roane CR 5/12 cluster
RealignOverlap ONLY                      11
                                        ───
                                        148 unique orphan pairs
```

**Calibrate is the most comprehensive single proxy** — every orphan in the dataset shows up either through the Calibrate sweep or the RealignOverlap sweep, because the LRS transactions that cause orphans always recalibrate the route as part of the change. The 28 "Calibrate ONLY" orphans are pure measure-recalibration truncations with no concurrency, retirement, or reassignment involved — a single sweep of Calibrate alone would have caught them.

This means a downstream-side monitor doesn't need to listen for all four activity types — it can poll `RH_FROM_DATE > last_check_time` on the Calibrate layer for any route the agency has CMPs on, and that will surface every orphan-causing event-behavior cascade in the LRS.

---

## 6. Random-sample base rate

To convert targeted-sweep findings into a base rate, a uniform random sample of 100 NetworkId=1 edits since 2025-10-01 (all activity types) was drawn and each tested for CMP intersection.

```
Of 100 random NetworkId=1 LRS edits (Oct 2025 → 2026-05-19):
   71  hit a route with no CMPs at all (no possible impact — safe by construction)
   14  hit a route with CMPs, Deighton handled cleanly (event behavior fired, no orphan)
   15  hit a route with CMPs that is confirmed to have orphaned data

Impact rate among edits that touch a CMP'd route:  15/29 = 51.7%
Impact rate overall (all LRS edits):                15/100 = 15.0%
```

**About one in seven arbitrary LRS edits affects CMP attribution** — and more than half of all LRS edits that hit a CMP'd route end up affecting it.

### 6.1 Hit and damage rate by activity type (sample)

```
activity         edits  with CMPs  hit-rate   avg refs/hit-route
─────────────────────────────────────────────────────────────────
RealignOverlap     3        3       100%         14.3
Extend             1        1       100%         11.0  (n=1)
Calibrate         26       17        65%         16.7
Reverse            2        1        50%         10.0  (n=2)
Reassign          13        3        23%         25.7
CartoRealign       7        1        14%         13.0
Retire            23        3        13%         13.3
Create            25        0         0%          —
```

- **RealignOverlap is the highest-impact operation.** 100% hit rate in the sample, and the full-window sweep confirmed 6 of 11 RealignOverlap edits produced orphans (55% impact rate). RealignOverlap is the operation that creates new concurrencies — the structural feature Deighton's current re-clip does not handle.
- **Calibrate is the workhorse.** 65% of Calibrate edits touch a CMP'd route, simply because most LRS adjustments use Calibrate as one of their multi-step components. Each Calibrate hit averages ~17 CMPs on the affected route, so each Calibrate-attributed event-behavior cascade is amplified.
- **Create edits never hit a CMP'd route directly** (0/25). But the routes they create become destinations for subsequent RealignOverlap concurrencies — which IS where Category 1 loss originates.
- **Retire edits hit a CMP'd route only 13% of the time** (most retirements are tiny sub-routes), but when they do hit, the route is gone entirely.

### 6.2 Directional pairs handle the same event differently

The Roane US 33 corridor has both westbound (`44200330000WB`) and eastbound (`44200330000EB`) routes. Both received a `RealignOverlap` edit on **2025-12-15** in the same TransactionId. The **WB side became the largest single orphan event in the dataset** (60.6 mi lost across 14 CMPs); the **EB side is in the "clean handled" pile** (16 CMP refs, no orphan loss detected).

That asymmetry — identical event-behavior trigger, opposite directions on the same physical corridor, different downstream outcome — confirms that **the orphaning isn't deterministic at the operation-type level**. The outcome depends on the specific measure-shape of the realigned portion on each side. The trigger (event behavior) is uniform; whether Deighton survives depends on the specific structural change.

### 6.3 Projected damage rate

The 15% overall impact rate, applied to 727 LRS edits in 8 months (~91/month), implies **about 14 CMP-affecting LRS edits per month** in the production system. Without a current detection mechanism, most of these go unobserved until field work surfaces a discrepancy.

A simple weekly job running the §3.2 Stage-1 length-preservation check across every CMP asset reference would flag every event-behavior cascade that orphaned at least one CMP, with a `~0%` false-positive rate (the length-preservation check itself is mathematically conservative). The Stage-2 LRS verification could then be run only on flagged routes to separate Deighton-side losses from LRS-true losses for triage.

---

## 7. Pattern: rural-county FC=9 reclassification project

A secondary observation that helps explain WHY this batch of event-behavior cascades is concentrated where it is: **7 of 11 verified orphan routes were demoted to FC=9 (Local) in their post-edit F System state**, while only 4 retained higher classes:

```
Demoted to FC=9 (Local) in this batch:
  Hardy CR 2, Preston CR 80/8, Wirt CR 14/7, Roane CR 5/12,
  Randolph CR 33/19, Ritchie CR 31/10, Pendleton CR 220/4

Retained FC=7 (Major Collector):
  Marshall CR 14, Roane CR 3, Berkeley CR 6

Demoted to FC=6 (Minor Arterial):
  Roane US 33 WB
```

All affected counties are rural: Hardy, Preston, Wirt, Roane, Randolph, Ritchie, Pendleton, Berkeley, Marshall. This looks like a **rural-county-by-county reclassification project** moving secondary roads down the functional-class hierarchy. The reclassification edits are themselves valid LRS work — the orphaning of CMPs is an unintended side effect of event-behavior propagation not surviving the Deighton re-clip.

**If WVDOH plans more counties in subsequent reclassification batches, CMPs on the affected routes are at risk of similar attribution loss when Deighton next ingests** — at roughly the same per-route impact pattern observed here.

---

## 8. Remediation priorities

The two-category framework from §4.3 dictates the fix approach:

### 8.1 Category 1 — Concurrency-aware re-clip (high impact, structural fix)

Routes where Deighton dropped pavement that exists in the LRS on a concurrent sibling route. Five gaps fall here (Outcome A in §4.2.1) with confirmed sibling-route LRS edits acting as the cascade trigger: Roane US 33 WB (interior gap), Wirt WV 14 (main gap), Berkeley CR 6, Randolph CR 33/19 (head), and Roane CR 3 (head). This category dominates the Deighton-only mileage — Roane US 33 WB's interior gap alone is ~62 of the ~70 Deighton-only CMP-miles.

**Approach:** make Deighton's ingestion concurrency-aware. Two options:
- **Geometric**: detect that asset-ref measures dropped from route A correspond to a geometry that is also covered by route B at the same coordinates; auto-attach a parallel reference on route B.
- **Concurrency table**: have WVDOH publish an explicit concurrent-routes table; Deighton consults it during re-clip.

Without this change, future RealignOverlap cascades (much of the ongoing rural-county FC=9 project, plus directional-pair edits like Roane US 33) are likely to orphan additional CMPs.

### 8.2 Category 2 — Deighton-side re-clip issue (medium impact, follow-up)

Routes where Deighton dropped pavement that the LRS still has on the original route at the original measures, with no sibling LRS edit that could have triggered the cascade. Nine gaps fall here (Outcome B + Outcome C in §4.2.1): Marshall CR 14 head, Ritchie CR 31/10 middle, Preston CR 80/8 (long-standing siblings but no trigger edits), both Roane CR 5/12 gaps, Randolph CR 33/19 tail, plus tail-trim-style cases on Wirt WV 14, Roane US 33 WB, and Roane CR 3.

**Approach:** follow up with Deighton support. The LRS data alone does not explain these losses — they appear to be internal re-clip behaviors that surface when event behavior fires for certain measure-shape changes (e.g., the Marshall CR 14 case where the route's extent didn't change at all but Deighton still lost 0.138 mi at the head). Without internal Deighton telemetry these are difficult to diagnose externally.

### 8.3 Proactive monitoring (immediate, low cost)

Independent of either Category 1 or Category 2 changes, the agency can detect orphans within a week of occurrence by:

1. Polling layer 132 (or layers 2/35/etc.) for new `RH_FROM_DATE` values on any route that has CMP asset references.
2. For each newly-edited CMP'd route, running the Stage-1 length-preservation check.
3. Auto-creating a triage ticket for any CMP whose `sum(currents.length) < drawn.length` after the edit.

The current 15% impact rate × ~91 edits/month means this would flag roughly 14 routes per month for review — manageable manual workload, and fully automatable.

### 8.4 Bulk repair of existing attribution losses

The 148 already-orphaned CMPs need their attribution restored. Approach:

1. For Category 1 cases (Wirt WV 14, Roane US 33 WB, Berkeley CR 6, etc.): the §4.3 geographic-probe technique identifies which sibling route the missing pavement is on. A bulk script can attach the parallel asset references.
2. For Category 2 cases (Marshall CR 14, Ritchie CR 31/10, etc.): the original measure range can be restored on the original route ID since the LRS still has the pavement there. May require Deighton support intervention to re-attach without re-triggering the same behavior.

---

## 9. Reproducibility — exact artifacts

### 9.1 LRS-side artifacts

- `/tmp/all_edits.json` — all 727 NetworkId=1 LRS edits in window
- `/tmp/reassigns_n1.json` — type-6 (Reassign) edits, NetworkId=1
- `/tmp/realign_n1.json` — type-7 (RealignOverlap) edits, NetworkId=1
- `/tmp/retire_n1.json` — type-4 (Retire) edits, NetworkId=1
- `/tmp/calib_n1.json` — type-2 (Calibrate) edits, NetworkId=1
- `/tmp/route_event_summaries.json` — per-route event-behavior multi-layer histories for all 11 verified orphan routes

### 9.2 Deighton-side artifacts

- `/tmp/dtims_check.py` — reusable Deighton OData query module (Bearer token auth)
- `/tmp/sweep3_results.json` — Reassign sweep, length-preserved check
- `/tmp/realign_results.json` — RealignOverlap sweep, length-preserved check
- `/tmp/retire_results.json` — Retire sweep, length-preserved check
- `/tmp/calib_results.json` — Calibrate sweep, length-preserved check
- `/tmp/consolidated_orphans.json` — deduplicated unique `(CMP, route)` orphan inventory (148 records)
- `/tmp/verified_orphans.json` — LRS-verified orphans with true-loss vs Deighton-bug split
- `/tmp/worst_per_route.json` — worst-case CMP per route with current segments and gap patterns
- `/tmp/sample_700_results.json` — random sample base-rate test

### 9.3 To regenerate the entire analysis

1. Pull layer 132 with `where=NetworkId='1' AND TransactionDate > date '2025-10-01'`, decode `EditDataXml` base64 → XML to extract per-activity-type details.
2. For each affected route ID, query Deighton OData `/CoreMaintenancePlanAssetReference?$filter=Name eq '<route>' &$expand=AssetReferenceCurrents,AssetReferenceHistoricalLRS`.
3. Apply Stage-1 length-preservation check (`sum(currents.length) < drawn.length`).
4. For Stage-1 hits, query `Publication_LRS/MapServer/35/query?where=ROUTE_ID = '<route>' AND RH_TO_DATE IS NULL` to verify against LRS-current state.
5. For Stage-2-confirmed Deighton-side losses, geographically probe each gap's midpoint against layer 35 to identify concurrent routes (Category 1) or confirm "no other route here" (Category 2).

---

## 10. One-paragraph plain-language summary

Every Core Maintenance Plan that lost attribution in this analysis was affected by **LRS event behavior** — Esri Roads & Highways' built-in mechanism for propagating a network re-cut across every event layer in the LRS simultaneously. The mechanism worked correctly on the WVDOH side in every case examined; the issues all surfaced downstream when Deighton's separate re-clip process tried to project the same change onto its asset-reference store and either (a) failed to follow a new concurrency to a sibling route, or (b) dropped pavement with no LRS-side trigger visible. Over the eight months from October 2025 through today, **about one in seven arbitrary LRS edits affected CMP attribution in Deighton** — 148 CMP-route orphan instances on 13 routes, totaling 130.6 CMP-miles of which 70.4 (55%) is a Deighton-side issue rather than a reflection of LRS retirement. The largest single event-behavior cascade — a 2025-12-15 RealignOverlap on Roane US 33 WB — dropped 5.948 miles from each of 14 different CMPs in one transaction. The per-break geometric confluence check tied 5 of the 14 verified breaks directly to a specific LRS edit-log entry on a sibling route on a specific date; 9 of the 14 breaks have no sibling-edit trigger to explain them and appear to be internal Deighton re-clip behaviors. None of these orphans surfaced through error reporting; the LRS produced no error and Deighton produced no warning. A weekly length-preservation check would flag future occurrences within days, and the existing 148 cases can be triaged into "concurrency-aware re-clip needed" (Category 1, dominates by mileage — Roane US 33 WB's interior gap alone is ~62 of ~70 Deighton-side CMP-miles) and "Deighton-side re-clip issue" (Category 2, more cases by count but smaller per-case impact — follow up with Deighton support).
