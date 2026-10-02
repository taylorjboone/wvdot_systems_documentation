# LRS Event-Behavior Report

## How a single 2026-02-27 network edit propagated through ~12 event layers on WV Route 14 (RTE_ID `5330014000000`) and its 1.5-mile concurrent designation `5340014230000`

**Source service.** WV DOH ArcGIS REST endpoint
`https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer`

**Routes analyzed.**
- `5330014000000` — the "big road" — 0.000 – 20.565 mi (currently active; 20.710 mi prior to 2026-02-27)
- `5340014230000` — the "little road" — 0.000 – 1.511 mi, a child/overlay route created 2026-02-27

**Layers analyzed.** 0 / 2 / 4 / 12 / 15 / 17 / 22 / 32 / 35 / 36 / 39 / 49 / 50 / 51 / 62 / 65 / 70 / 83 / 96 / 120 — twenty event layers in total, of which twelve carry records for one or both routes.

**Window.** All edit history available in the published service: 2019-03-14 → 2026-03-02 (today is 2026-05-19; nothing has been edited on either route in the two months since).

---

## 1. Executive Summary

Looking at seven years of edit history on this corridor across roughly a dozen event layers, **only one edit actually records a meaningful change in what the road *is*.** Every other dated record we observe is one of three flavors of plumbing:

| flavor | what it is | how often we see it here | example |
|--|--|--|--|
| **Network refresh** | The centerline is re-published with no measure or attribute change; every event layer gets a new record because dynamic segmentation re-cuts onto the (identical) new measures | once corridor-wide | 2022-11-01 |
| **Network re-cut** | The centerline is restructured (new splits, measure recalibration, new child route added). The new break stations are "candidate breaks" that propagate to every event layer; each event layer keeps the breaks where its own attribute differs across them and discards the rest | twice in three days | 2026-02-27, 2026-03-02 |
| **Layer-local attribute refresh** | A single event layer is republished — typically because the source dataset (urban areas, census codes) was updated upstream — without any value actually changing | sparsely | 2025-06-02 (urban layers), 2025-07-14 (census urban) |

The **one real attribute change** in the entire seven-year history of these two routes is:

> **2026-03-02**: `5340014230000`.FAS_TYPE flipped from `3` → `5`. This is the moment the LRS first correctly modeled the fact that the 1.51 miles of pavement covered by the child route is **not federal-aid eligible**, even though the parent corridor `5330014000000` is.

Everything else — the four-piece transient split on 02-27, the FC=9 / FAS=5 / WV-FC=6 sliver that lived for three days, the end-measure rolling back from 20.710 → 20.565, the cascade of new records across every event layer on the same date — is the LRS re-pressing itself into shape after a centerline edit. Once you can tell the network plumbing apart from genuine value changes, the corridor's actual history is exceptionally short.

**This is not just an academic concern.** Section 8 of this report documents that the same network event, when consumed downstream in Deighton dTIMS, **silently orphaned 1.34 miles of pavement** from an existing Core Maintenance Plan (CMP 278793). The CMP was drawn on 2026-02-17 covering 7.16 miles of WV Route 14 (mi 13.55 – 20.71). After dTIMS ingested the new LRS on 2026-04-09, the CMP was re-clipped against the new topology, the 15.24 – 16.575 piece was dropped (because it now belongs to the child route, which the re-clip didn't follow), and the maintenance plan now covers only 5.68 miles — a **19% mileage reduction with no human in the loop**. This report walks through both the LRS-side mechanism that produced the propagation and the dTIMS-side consequence that resulted from a downstream consumer not knowing how to handle the concurrency the LRS correctly created.

---

## 2. Background: Linear Referencing Systems and Event Behavior

### 2.1 The two-tier R&H data model

WV DOH's Publication_LRS service is an Esri Roads & Highways implementation. R&H separates the world into two tiers:

1. **The route network** (centerlines + measures). A `ROUTE_ID` and a continuous `M`-value along it form the spatial reference. The network is authoritative — measures are calibrated to physical pavement, not derived from geometry length. (In our data we saw r1's stated measure-length of 20.710 mi against a haversine-geometry length of 20.359 mi: a ~1.7% discrepancy that is normal — calibrated measures track odometer/ground truth, not WGS84 chord distances.)

2. **Event layers** — attribute datasets stored as `(ROUTE_ID, FROM_MEASURE, TO_MEASURE, value, RH_FROM_DATE, RH_TO_DATE)`. Each event layer carries one "fact about the pavement" (functional class, surface type, AADT, ownership, etc.) and dynamic-segments onto the network on the fly.

Event layers do **not** carry their own geometry in the editing schema — they carry measures. When you query an event layer with `returnGeometry=true`, R&H computes the geometry by clipping the route centerline between FROM_MEASURE and TO_MEASURE at query time. This is why every currently-active feature we pulled with geometry had clean endpoint coordinates that exactly matched the parent route's calibration: the geometry is derived from the network, not stored independently.

### 2.2 Temporal versioning (`RH_FROM_DATE` / `RH_TO_DATE`)

Every event record has a half-open temporal validity interval `[RH_FROM_DATE, RH_TO_DATE)`. The currently-active records are the ones with `RH_TO_DATE = NULL`. Historical records are kept in the same table with `RH_TO_DATE` populated to whatever instant the record was superseded.

This is what enabled all of the temporal SLDs we built — every snapshot in time is reconstructable by filtering for records whose `[RH_FROM_DATE, RH_TO_DATE)` interval contains the snapshot instant.

A subtlety we encountered: some historical features in our pulls **had no geometry attached** (e.g. r1's `RH_FROM=2026-02-27 → RH_TO=2026-02-27` record). The service does not always materialize historical geometry; only the currently-active feature is guaranteed to have a path. Historical analysis sometimes has to fall back to measure ranges only.

### 2.3 Why network edits propagate

When the network is restructured — a route is split, merged, calibrated, or has a new child route created — R&H must re-fit every event record onto the new measure system. The two relevant operations are:

- **Dynamic segmentation re-fit.** Each event record's measure range is intersected with the new network structure. If a new break station falls inside a record's range, the record is split at that station so that each piece still aligns to a single network segment.

- **Publisher consolidation.** After the dynamic re-fit, adjacent records on the same event layer that share **all** attribute values are merged back into a single record. This is what filters the network's "candidate break" list down to the breaks each layer actually keeps.

The combined effect is what we observed: every event layer sees the same network edit on the same date, but the number of records each layer ends up with varies by how many of the candidate breaks survive consolidation.

---

## 3. Geographic and Geometric Context

```
WGS84 coordinates of the corridor (from layer 35 currently-active geometry):

  r1 mi  0.000   (-81.41498, 38.92070)      south end
  r1 mi 15.240   (-81.40831, 39.06901)  ←── r2 mi 0.000   (south end of overlap)
  r1 mi 15.514   (-81.40435, 39.07186)      the FC=9 sliver point
  r1 mi 16.575   (-81.41549, 39.08502)  ←── r2 mi 1.511   (north end of overlap)
  r1 mi 20.565   (-81.43921, 39.12690)      north end (= the old 20.710 endpoint, unchanged)

Corridor extent: ~0.035° lon × 0.206° lat, ~23 km north-south, in WV DOH District 5,
COUNTY=53 per layer 12 (both routes share the county code — the "33" vs "34" in the
route IDs is a route-type encoding, NOT a county code).
```

Distances we measured by haversine on the pulled paths:

| comparison | distance |
|--|--|
| r1 NEW main END ↔ r1 NEW tail START | 0.0 m (clean topology) |
| r1 NEW tail END ↔ r1 OLD full END | 0.0 m (the route did **not** physically shrink) |
| r1 NEW main END ↔ r2 END | 0.0 m (r2 ends exactly at r1's mi 16.575) |
| r1 transient FC=9 START ↔ r2 START | 0.0 m (r2 starts exactly at r1's mi 15.24) |
| r2 length on the ground | 1.509 mi haversine vs 1.511 mi LRS measure |
| r1 mi 15.24 → 16.575 along r1 | 1.429 mi (LRS measure) — same physical pavement |

**Conclusion**: r2 is not a separate piece of road. It is the same 1.51 miles of pavement as r1's miles 15.24 → 16.575, traced a second time under a different `ROUTE_ID`. This is a **concurrency** in LRS terms — one carriageway, two route designations.

---

## 4. The Edit Timeline, Reconstructed

### 4.1 All distinct `RH_FROM_DATE` values we observed across all layers

```
date        appears on (layers)                                  category
─────────────────────────────────────────────────────────────────────────────────
2019-03-14  2, 35, 36, 50, 51, 65, 83, 96, 22 ...  (every layer) NETWORK PUBLISH (original)
2019-07-30  2 (AADT)                                              attribute (AADT refresh)
2021-10-28  2                                                     attribute (AADT refresh)
2022-10-06  2                                                     attribute (AADT refresh)
2022-11-01  2, 35, 36, 50, 51, 65, 83, 96, 22 ...  (every layer) NETWORK REFRESH (identity)
2023-01-31  2                                                     attribute (AADT refresh)
2023-04-07  2                                                     attribute (AADT refresh)
2024-04-01  70 (Surface Type)                                     attribute (surface refresh)
2024-04-11  2                                                     attribute (AADT refresh)
2024-04-17  2                                                     attribute (AADT refresh)
2025-06-02  51, 83                                                LAYER-LOCAL (urban refresh)
2025-06-16  2                                                     attribute (AADT refresh)
2025-07-14  96                                                    LAYER-LOCAL (census urban refresh)
2026-02-27  2, 35, 36, 50, 51, 65, 70, 83, 96, 22 (every layer)  NETWORK RE-CUT (split + child route)
2026-03-02  35, 50, 51, 65, 70, 83, 96, 22, 36                    NETWORK CLEANUP (split merge-back)
```

### 4.2 The 2022-11-01 "identity refresh" — proof that network events propagate even without changes

This is the cleanest piece of evidence in the dataset that network edits propagate independently of attribute change. On **2022-11-01**, every event layer on `5330014000000` got a new record with:

- exactly the same `FROM_MEASURE = 0.000` and `TO_MEASURE = 20.710` as the prior record
- exactly the same value (NHS=0, FC=7, FAS=3, OWNERSHIP=1, etc.)
- a closing `RH_TO_DATE` of `2022-11-01` on the prior record and an opening `RH_FROM_DATE` of `2022-11-01` on the new one

For example, on layer 36 (NHS):

```
ROUTE 5330014000000 — NHS layer 36, partial history
FM     TM      NHS  RH_FROM      RH_TO
0.000  20.710  0    2019-03-14   2022-11-01    ← original
0.000  20.710  0    2022-11-01   2026-02-27    ← created by the 2022-11-01 network refresh
```

Nothing about the road or its NHS status changed on 2022-11-01. What changed was the **network publish** — the centerline was republished, all event layers re-fit themselves to the (numerically identical) new network, and the LRS dutifully closed every prior record and opened a new one. This is pure plumbing.

This pattern is repeated on **every layer that carries records for r1**, on the exact same date, with the exact same FM/TM/value preserved. It's a system-wide event.

### 4.3 The 2026-02-27 network re-cut — the busy day

Three things happened in one centerline edit on 2026-02-27:

1. **New splits at stations 15.24, 15.5138, and 16.575** on r1's measure system.
2. **End-measure recalibration**: r1's TO_MEASURE rolled from 20.710 to 20.565 (a 0.145-mi reduction in measure value), with **no change to the physical endpoint** — both old and new end records terminate at `(-81.43921, 39.12690)`. This is a calibration tightening, not a physical trim.
3. **A new child route** `5340014230000` was published, covering r1's miles 15.24 → 16.575, with its own measure system 0.000 → 1.511.

Every layer that carries r1 saw this propagate as a candidate break set `{15.24, 15.5138, 16.575}`. Different layers kept different subsets of those breaks based on whether their own attribute varied across each break:

```
break station →            15.24    15.5138   16.575    why kept on the layers that kept them
─────────────────────────────────────────────────────────────────────────────────
35  F System (federal FC)   ✓        ✓         ✓        FC=9 sliver was published at 15.24-15.5138
65  WV Func Class           ✓        ✓         ✓        WV-FC=6 sliver was published at the same station
22  Federal Aid             ✓        ✓         ✓        FAS=5 sliver was published at the same station
70  Surface Type            ✓        ✓         —        kept inner breaks for r2 boundary; outer break absorbed
36  NHS                     ✓        ✓         —        NHS=0 on both sides of 16.575 → no break needed
83  Urban Code              ✓        ✓         —        same — 99999 on both sides
51  Rural Urban             ✓        ✓         —        same — 0 on both sides
96  Census Urban            ✓        ✓         —        same — 99999 on both sides
50  Rural Municipal         ✓        ✓         —        same — 0 on both sides of 16.575
```

Three layers (35, 65, 22) received a transient incorrect-value sliver: a 0.27-mile FC/FAS anomaly at miles 15.24 – 15.5138. On 35 the bad value was `9`; on 65 it was `6`; on 22 it was `5`. All three are different ways of saying "non-major / off-system" in their respective classification schemes. The editor apparently tried to encode r2's federal-aid-ineligible status as a sliver on the **parent route** first, before realizing the correct model is to put it on the **child route** instead.

### 4.4 The 2026-03-02 cleanup — three days later

On 2026-03-02, the transient sliver was merged out and r2's FAS_TYPE was flipped from 3 to 5. This propagated through the network as a second event, with each layer absorbing it to a different depth:

```
layer       record count BEFORE 03-02   AFTER 03-02     note
────────────────────────────────────────────────────────────────────────────────────
35 F-Sys    4 records (0-15.24, 15.24-15.514, 15.514-16.575, 16.575-20.565)
                                        2 (0-16.575, 16.575-20.565)   kept r2-boundary break
22 FA       4 (same boundaries)         2 (same boundaries as 35)     same
65 WV-FC    4                           1 (0-20.565)                  consolidated fully — no value varies anymore
70 Surf     4                           1 (+ tiny pre-existing 3.0 slivers at 7.47 & 9.61)  consolidated
36 NHS      3                           1 (0-20.565)                  was already collapsed across 16.575; now fully one record
51 Rur/Urb  3 (with 19.723 break carried in from a 2025-06-02 urban refresh)
                                        1 record covering the recombined inner range
83 Urb      same as 51                  same as 51
96 Census   same                        same
50 RurMuni  3                           1 (14.866-20.565) (its pre-existing 13.728-14.866 RURAL_MUNI=1 record is untouched)
```

The layers that kept the 16.575 break on the 03-02 cleanup are exactly the layers where the **r2 concurrency endpoint** is a meaningful boundary: F System and Federal Aid. These are the only two layers where r1 and r2 have different values, so the network must hold a break there to allow distinct attribute values on either side via the r2 designation. Every other layer can collapse the break because both sides agree.

### 4.5 Layer-local refreshes (2025-06-02, 2025-07-14, 2024-04-01)

Three dates appear on only one or two layers. They show the other failure mode of "interesting-looking edits that are not real changes":

- **2025-06-02** appears on layers **51 (Rural Urban)** and **83 (Urban Code)** simultaneously. On both, r1's single 0-20.710 record was split into three pieces (0-1.228, 1.228-19.868, 19.868-20.710) — and **every piece kept the same value** (Rural Urban = 0; Urban Code = 99999). This is upstream urban-boundary data being re-published; the LRS dynamic-segmented r1 against the new urban polygon, found that none of r1 is in any urban area, but the network now carries the breakpoints from the urban polygon edges anyway.

- **2025-07-14** appears on layer **96 (Census Urban Code)** only, with the identical 3-piece split structure and the same `99999` value everywhere. This is the 2020 Census urban-area boundary refresh hitting WVDOH's LRS about six weeks after the WV-internal urban refresh. The fact that 51/83 fired on 06-02 and 96 fired on 07-14 with the **same break stations** is a strong tell that all three layers are downstream of related polygon refreshes.

- **2024-04-01** appears on layer **70 (Surface Type)** only. This is a one-off surface-type-data publish; nothing changed measure-wise, just new RH dates on the same 5-piece structure.

None of these dates appear on any layer except the ones listed. They are not network events.

### 4.6 Pure attribute edits (AADT)

The AADT layer (2) is the one event layer in our pull that carries a long history of **real attribute changes**. AADT counts genuinely change year over year as traffic volumes change, and the layer's history reflects that — different `AADT` values across different `RH_FROM_DATE` snapshots. The temporal SLD we built for AADT in an earlier step (10 snapshots, AADT values varying from 650 to 3900 across segments and time) is essentially the **only** layer where the temporal history reflects real-world change rather than network plumbing.

Even on AADT, however, the **2022-11-01** record appears as a network refresh — and on **2026-02-27** the AADT segments were re-split at the same {15.24, 15.5138, 16.575} candidate breaks introduced by the network edit. So even on a "real" attribute layer, you can see plumbing edits interleaved with substance.

---

## 5. The "Big vs Little Road" Resolved

After surveying twenty event layers we can state the difference between `5330014000000` and `5340014230000` succinctly. The two routes are **identical** in:

```
County (12)              53           both
Ownership (39)            1           both
ServiceOrg (32)        0353           both
TruckRoute (17)           4           both
SpecialSys (62)          01           both
RouteStatus (49)          5           both
NHS (36)                  0           both — neither on the National Highway System
NHFN (142)               n/a          (not in our pull but inferable from NHS=0)
Urban Code (83)       99999           both — neither in any urbanized area
Rural Urban (51)          0           both — both entirely rural
Census Urban (96)     99999           both
Rural Muni (50)           0           both (on the relevant overlap miles)
WV Func Class (65)        2           both — same WV-state functional class
Surface Type (70)       2.1           both — same pavement type
```

They differ in **two** layers only, and the two differences are not independent:

```
Layer                                  r1               r2
─────────────────────────────────────────────────────────────────────────
35 F System  (federal FC)              7                8
22 Federal Aid (FAS_TYPE)              3 (eligible)     5 (off-system)
```

Federal-aid eligibility follows federal functional class. FC=7 (Major Collector) is FA-eligible → FAS=3; FC=8 (Minor Collector) is not → FAS=5. So one semantic fact is being recorded twice, in two different layers, by two different attributes.

**The reason `5340014230000` exists as a separate route** is that the LRS needs to model the fact that 1.51 miles of pavement in the middle of `5330014000000` is **not federal-aid eligible**, even though the parent corridor as a whole is. This is required for HPMS reporting (which needs FA-eligible mileage queryable separately from off-system mileage) and for federal-aid project accounting. The dual designation lets a query for "all FA-eligible mileage in District 5" pick up the parent's full length, while a query for "all off-system mileage" picks up the child route's 1.51 miles, without either query having to descend into measure-range filtering.

The two-step publication is itself instructive about LRS modeling choices:

```
2026-02-27 — first attempt (incorrect model):
   r1: split into 4 pieces, FAS=5 dropped onto the inner 0.27-mi sliver only
   r2: created over the full 1.51-mi overlap, FAS=3 (same as parent → conveys no information)

2026-03-02 — corrected model:
   r1: consolidated back to 2 pieces, FAS=3 throughout
   r2: FAS_TYPE flipped 3 → 5
```

The first attempt would have technically encoded the 0.27 miles correctly but would have lost the FA-status of the other 1.24 miles of pavement covered by r2. The correction moves the entire FAS=5 fact to the child route, which is where it belongs semantically — r2 is the "off-system designation," and it should carry off-system FAS values across its full length.

---

## 6. The Esri Roads & Highways Mechanism, Restated

Putting the pieces together, the mechanism that produced everything we observed is:

1. **Edit sessions on the route network** generate a set of "centerline events": new routes, route splits, measure recalibrations, end-measure changes. These are the only edits that fire across all event layers.

2. **Dynamic segmentation re-fit.** When a network event is published, R&H's event-behavior engine intersects every event record's `[FROM_MEASURE, TO_MEASURE]` range with the new network structure. Where a new station station falls inside a record's range, the record is split there so each piece aligns to exactly one network segment.

3. **Per-layer publisher consolidation.** After the dynamic re-fit, adjacent records on the same event layer that share all attribute values are merged. This is what filters the candidate-break set down to the breaks each layer actually retains. Layers with uniform attributes (NHS=0 everywhere on this corridor) collapse aggressively; layers with attribute variation across the new breaks (F System with its transient FC=9) keep more breaks.

4. **RH versioning.** Every record affected — whether merged, split, or unchanged-but-republished — gets a closing `RH_TO_DATE` on the prior version and an opening `RH_FROM_DATE` on the new version. This is why a network edit produces a wall of new dated records across many layers on the same instant, even when no value changed.

5. **Independent attribute editing** on a single event layer (e.g. setting r2's FAS to 5 on 03-02, or AADT updates on layer 2) does **not** fire across other layers. It produces a single new record on the affected layer with new RH dates.

6. **Upstream source refreshes** (urban polygons, census boundaries) are handled by re-running dynamic segmentation against the new source dataset. This can produce new break stations on the affected event layer(s) without affecting the network or other event layers — exactly what we saw on 2025-06-02 (urban) and 2025-07-14 (census urban).

---

## 7. Distinguishing Signal from Noise

For any downstream consumer of this LRS (reporting tools, GIS analyses, dashboards), the practical implication is:

- **Counting "records changed" or "edits made" overstates real change by an order of magnitude or more.** On the two routes we examined, twelve layers × ~7 years of history produced dozens of records, of which **one** records an actual change in what the road is.

- **Looking only at currently-active records (`RH_TO_DATE IS NULL`) gives you a clean cross-section of the world today** — without noise from old network re-cuts. This is the right cross-section for most "what is the road like now" questions.

- **Looking at temporal history is most useful when restricted to layers that carry genuine over-time variation.** AADT (layer 2) is the standout example in our pull. F System and Federal Aid carry real history when network re-cuts coincide with reclassification events. Surface Type carries history when pavement is overlaid. Most other layers' history is dominated by plumbing.

- **A "new record on date X" on a layer should not be interpreted as a value change without checking the prior record's value.** If the value is unchanged across the RH break, the record is a network-edit artifact.

- **When tracking historical accuracy, the FROM_MEASURE/TO_MEASURE values are not stable across network re-cuts.** r1's miles 15.24 and 16.575 in the 03-02 records correspond to the same physical points as the pre-02-27 records — but the pre-02-27 records did not have stations at those mile values at all. Comparing "miles 15-17 in 2019" against "miles 15-17 in 2026" only works if the calibration hasn't moved; on r1 it has (the end-measure rolled from 20.710 to 20.565, which means **all** internal measures from the recalibration point northward may have shifted by some amount). Layer 0 (Calibration Point) and layer 33 (Measure Source) would carry the audit trail for those shifts.

---

## 8. Downstream Consequence — The CMP 278793 Orphaning

The previous seven sections concerned the LRS itself, where the event behavior is doing what it's designed to do. This section follows the same network edit one tier downstream, into WVDOH's asset-management system (Deighton dTIMS), and shows what happens when a consumer that wasn't built to handle concurrencies re-clips an existing asset reference against the new LRS.

### 8.1 The asset reference

Core Maintenance Plan **278793** in dTIMS carries a single asset reference (Id `515492`, "Wirt WV 14") that was drawn on **2026-02-17** — ten days before the LRS re-cut:

```
NetworkName:    5330014000000
DisplayName:    Wirt WV 14
From / To:      13.55 / 20.71 (LRS measures)
ReferenceDate:  2026-02-17T16:11:01-05:00
AssetId:        7e4c53d5-032d-ef11-b813-0050569a11ce   (= the OLD network's element ID)
```

That's **7.16 miles** of WV Route 14 — the upper third of the corridor, ending at the original LRS end-measure of 20.71.

### 8.2 The historical re-clip trail

dTIMS exposes the asset reference's history via the `AssetReferenceHistoricalLRS` and `AssetReferenceCurrents` collections. Each row is the snapshot of how the asset reference resolved against whichever LRS version dTIMS was running at the time. Eight historical rows and three current rows tell the story:

```
window (ReferenceDate → ValidTo)         segments held by the CMP                     network AssetId
─────────────────────────────────────────────────────────────────────────────────────────────────────────────
2026-03-26 → 2026-03-30   1 piece:  13.55 – 20.71                                     7e4c53d5…  (OLD)
2026-03-30 → 2026-04-09   1 piece:  13.55 – 20.71  (identity refresh, no re-clip)     7e4c53d5…  (OLD)
2026-04-09 → 2026-04-23   3 pieces: 13.55 – 15.240
                                    16.575 – 17.635
                                    17.635 – 20.565                                   ce6d18e9…  (NEW)
2026-04-23 → 2026-04-27   3 pieces: same as above (identity refresh)                  ce6d18e9…
2026-04-27 → CURRENT      3 pieces: same as above (AssetReferenceCurrents)            ce6d18e9…
```

Two distinct events:

- **2026-04-09** — dTIMS ingested the post-02-27 WVDOH LRS. The asset reference's underlying network element ID flipped from `7e4c53d5…` to `ce6d18e9…`, and the CMP was re-clipped onto the new topology. This is dTIMS's equivalent of R&H's dynamic-segmentation re-fit, but operating on its own internal asset-reference store.
- **2026-04-23 and 2026-04-27** — two more refresh cycles, each producing identity re-clips (same measures, same network ID). Same pattern as the WVDOH-side `2022-11-01` identity refresh documented in section 4.2 — pure plumbing, no real change.

### 8.3 What the 04-09 re-clip actually did

Three transformations were applied to the 13.55 – 20.71 asset reference in a single re-clip pass:

1. **The 15.24 – 16.575 piece (1.335 mi) was dropped entirely.** dTIMS walked the new topology of route `5330014000000`, found that the parent route is now stored as `[0 – 16.575] ∪ [16.575 – 20.565]` (the 16.575 break is the one F System / Federal Aid kept because that's the concurrency endpoint with `5340014230000`), but did **not** know to follow the concurrency across to the child route. The pavement is still there on the ground, the LRS still describes it (just under route `5340014230000` instead of `5330014000000`), but the asset reference no longer claims it.

2. **A new break at 17.635 was inserted.** This breakpoint does not appear on any WVDOH LRS event layer that I pulled — not F System, not NHS, not Federal Aid, not Surface Type, not any urban layer. It first appeared in the asset reference on the 04-09 re-clip. That makes it almost certainly a **Deighton-side segmentation rule** — most likely an internal pavement-management section boundary, a calibration anchor, or a value transition in some attribute that lives in dTIMS's own LRS-equivalent store rather than in WVDOH's published LRS. (The half-open boundary value `17.634999` repeated literally in the data — vs the clean `17.635` on the adjacent piece — is also a giveaway that this break was machine-inserted, not edited.)

3. **The 20.565 – 20.710 tail was silently truncated.** This one is benign in terms of physical pavement: the LRS end-measure was recalibrated, not the physical route end (both endpoints are at `(-81.43921, 39.12690)`). dTIMS correctly truncated the asset reference to the new max measure value.

### 8.4 The arithmetic

```
                    drawn   currently held    delta
Total mileage       7.160 mi   5.680 mi     −1.480 mi   (about 21% of the original CMP)
   = 13.55–15.240    1.690                              kept
   + 16.575–17.635   1.060                              kept (with the spurious 17.635 break)
   + 17.635–20.565   2.930                              kept
   --- missing ---
   − 15.240–16.575   1.335                              ORPHANED — now only on route 5340014230000
   − 20.565–20.710   0.145                              recalibration delta (no physical pavement lost)
```

The CMP, as it stands today in dTIMS, is **missing 1.34 miles of physical pavement** that it was originally drawn against. That pavement still exists, is still maintained by WVDOH, and is still described in the WVDOH LRS — just on a route ID that the CMP doesn't reference.

### 8.5 Why this happened — exactly the mechanism from sections 4–6

The dTIMS re-clip does the same thing R&H's publisher consolidation does (section 6 step 3): it intersects each existing measure range against the new network topology and keeps only the pieces that still lie on the route the reference was attached to. What it doesn't do — and what no naive measure-range clip can do — is follow concurrencies. Concurrent designations are a deliberate part of the LRS data model: the parent and child both validly describe the same pavement. But a re-clip against `route_id = '5330014000000'` will, by construction, miss anything that's been moved to a sibling route ID, even if the pavement is unchanged.

The WVDOH LRS published the concurrency for a real and correct reason — the 1.51-mile child route exists to record that those miles are **federal-aid ineligible** while the parent corridor as a whole is eligible (sections 5 and 4.3 of this report). The LRS modeling is right. The dTIMS re-clip just doesn't have the concept of "concurrency-aware" in its asset-reference resolver.

### 8.6 Practical consequences for CMP 278793

- **Reporting under-counts mileage by 19%.** dTIMS will report 5.68 mi of planned maintenance against this CMP; the field reality the plan was drawn for is 7.16 mi.
- **Field work on the orphaned 1.34 miles cannot be billed to this CMP.** A crew entering activity in dTIMS for a station between mi 15.24 and 16.575 of WV 14 will find that no CMP picker offers 278793 as a match — because dTIMS believes that pavement no longer belongs to the CMP.
- **The spurious 17.635 break is a cosmetic mess but not a correctness issue.** The CMP still covers all the pavement on either side of 17.635; it's just stored as two records instead of one.

### 8.7 Remediation options

Each of these would close the gap, in increasing order of effort and decreasing order of recurrence-risk:

- **Option A — manual fix per CMP.** Edit CMP 278793 in dTIMS to add a second asset reference on route `5340014230000` mi 0 – 1.511. The CMP would then span two route IDs but again cover the same physical pavement.
- **Option B — survey & repair.** Run a one-time query against dTIMS for every asset reference whose measure range straddles a known concurrency endpoint on the WVDOH LRS, and bulk-fix any that lost coverage on re-clip.
- **Option C — change dTIMS ingestion to be concurrency-aware.** Configure dTIMS to know which parent/child route pairs are concurrent, so a re-clip that drops measures on the parent automatically attaches an equivalent measure range on the child. This requires either WVDOH publishing an explicit concurrency table (layer 4 `ALT_ROUTE_NAME` is empty on these routes, so no signal is currently being sent) or dTIMS detecting concurrencies geometrically by comparing route geometries that overlap in space.
- **Option D — procedural gate at the LRS editor.** Have the WVDOH LRS publisher flag any centerline edit that introduces a new concurrency as requiring downstream dTIMS review. Any CMPs that touch the affected stations get held for human review before the new LRS is allowed to land in dTIMS.

### 8.8 Why this section belongs in the report

Sections 1–7 of this report document that LRS event behavior is, on its own, harmless and self-consistent: every edit produces a faithful, queryable trail of plumbing records, and the actual "what is the road" delta is small and explicable. The CMP 278793 case is the evidence that **event behavior is only harmless inside the LRS**. The same edit that the LRS handled correctly silently mutated an asset reference in dTIMS by ~19%, with no warning, no notification, and no human review. The fundamental problem isn't the propagation mechanism — it's that downstream consumers re-implement a piece of the propagation (the re-clip) without the concept of concurrency that the LRS uses to express the kind of edit that actually happened on 2026-02-27.

If WVDOH wants the LRS event-behavior model to be safe in practice rather than just safe in theory, the missing piece is **concurrency-aware re-clip** on every downstream consumer of the LRS, not just dTIMS. Anywhere else in the WVDOH ecosystem that holds measure-range references against route IDs (HPMS extracts, GIS dashboards, bridge inventory cross-references, the DOT-12 system itself) is at risk of the same silent orphaning whenever an LRS edit creates a new concurrency, and is at risk of the same silent measure shifts whenever the LRS recalibrates a route's measures (as happened on r1 with the 20.71 → 20.565 change). The CMP 278793 story is just the example we can document.

---

## 9. Reproducibility — Exact Queries Used

### 9.1 WVDOH Publication LRS (Esri R&H)

```
Service:         https://gis.transportation.wv.gov/arcgis/rest/services/
                 Roads_And_Highways/Publication_LRS/MapServer

Layer schema:    /{layer_id}?f=json
Layer features:  /{layer_id}/query?where=ROUTE_ID = '{route_id}'
                                  &outFields=*
                                  &returnGeometry={true|false}
                                  &outSR=4326           (for WGS84 geometry)
                                  &f=json

Routes:    5330014000000  (parent, 0–20.565 mi)
           5340014230000  (child overlay, 0–1.511 mi)

Layers examined:
  0   Calibration Point
  2   AADT                     ← real attribute history (traffic counts)
  4   ALT_ROUTE_NAME
 12   County Code
 15   CRTS Rt
 17   Truck Rt
 22   Federal Aid              ← the layer that explains r2's purpose
 32   WVDOT Maint Ops
 35   F System (federal FC)    ← the other layer that explains r2's purpose
 36   NHS                      ← uniform 0; confirms r2 not NHS-driven
 39   Ownership
 49   Route Status
 50   Rural Municipal
 51   Rural Urban
 62   Special Sys
 65   WV Functional Class
 70   Surface Type
 83   Urban Code
 96   CENSUS_URBAN_CODE
120   Jurisdiction (no records for either route)
```

### 9.2 Deighton dTIMS (CMP 278793 — section 8)

```
Service:         https://wvdotom.wvoasis.gov/pilot/omdata/odata
Auth:            Bearer token (Okta-issued, expires ~1 hour)

Asset references for a CMP:
  /CoreMaintenancePlan({cmp_id})/AssetReferences
     ?$expand=AssetReferenceLRMs,
              CustomQueryAsset,
              AssetReferenceCurrents,
              AssetReferenceHistoricalLRS

Key collections per asset reference:
  - AssetReferenceCurrents       — currently-valid measure ranges (the resolved state today)
  - AssetReferenceHistoricalLRS  — full audit trail of re-clips against LRS versions over time

Key fields to read:
  ReferenceDate    when the asset reference was last evaluated against the LRS
  ValidTo          when that evaluation was superseded (null = current)
  AssetId          underlying network element ID; flips when the LRS network is rebuilt
  From / To        measure range held by this piece of the asset reference
```

---

## 10. One-Paragraph Plain-Language Summary

WV Route 14 (LRS ID `5330014000000`) is a 20-mile rural corridor. In the middle of it, 1.5 miles of the same pavement are also published as a second route ID (`5340014230000`) so that the LRS can record that 1.5-mile stretch as **off the federal-aid system** while the parent route as a whole remains **on** the federal-aid system. On 2026-02-27 the agency made the centerline edit that created the second designation, and three days later on 2026-03-02 they cleaned up an attribute mistake that had been published with it. Those two dates are the only edits in the entire seven-year history of this corridor that record actual changes about what the road is. Every other dated record on every other layer of this LRS — and there are dozens of them — is a downstream effect of the network being re-published, dynamic segmentation re-cutting event ranges to fit, and the LRS's temporal versioning honestly recording that re-fit even when no value changed. The "event behavior" of Esri Roads & Highways is doing exactly what it's designed to do; what's surprising is how much of the apparent edit history on a typical LRS is actually plumbing rather than substance. The catch — documented in section 8 — is that downstream consumers like Deighton dTIMS re-implement a piece of the propagation (the re-clip) without the concept of concurrency that the LRS uses to express edits like the 2026-02-27 child-route publish. The same edit that the LRS handled correctly silently dropped 1.34 miles from Core Maintenance Plan 278793 when dTIMS ingested the new LRS on 2026-04-09, with no warning and no human review. The propagation mechanism inside the LRS is safe; the problem is what happens at the boundary where the LRS hands off to systems that don't know how to follow concurrencies.
