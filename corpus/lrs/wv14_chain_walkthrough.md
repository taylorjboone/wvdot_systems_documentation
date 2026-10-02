# Wirt WV 14 — Complete Chain Walkthrough

**How LRS route `5340014230000` (the off-system child) connects back to `5330014000000` (the parent), traced through every layer-132 edit log entry in the 12-minute editor session on 2026-02-27.**

---

## Quick answer

The child route `5340014230000` is reached from the parent `5330014000000` via a **two-hop** chain through the **southbound** side of WV 14:

```
5330014000000 (NB)
   ⇅ overlap declared in OID 4332855 (NB RealignOverlap @ 12:06)
53300140000SB (SB)
   ⇅ overlap target declared in OID 4332899 (SB RealignOverlap @ 12:13)
5340014230000 (the child, off-system designation)
```

The NB-side XML (OID 4332855) **never directly names** `5340014230000`. The link only appears in the SB-side XML (OID 4332899), which is why a naive RouteId-only lookup against layer 132 misses it. Walking every nested `RouteId` / `NewRouteId` / `PriorityId` / `OriginatingRouteId` attribute across both edits is how the link surfaces.

---

## The Chain — Wirt WV 14 network re-cut, 2026-02-27 (with hyperlinks)

Every route ID and ObjectId below is a live link. Route IDs link to the full layer-132 edit history for that route; OIDs link to the specific layer-132 row.

<pre>
12:01:22  CreateRouteInfo                              filed: <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=RouteId%3D%275340014230000%27%20AND%20NetworkId%3D%271%27&outFields=*&orderByFields=TransactionDate%20DESC&returnGeometry=false&f=html">5340014230000</a>  (<a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4334355&outFields=*&returnGeometry=false&f=html">OID 4334355</a>)
          → child route published, empty (NaN measures, NaN length, just an ID reserved)

12:04:47  CalibrateRouteInfo × 10                      filed: 4 on NB, 4 on SB, 2 on Wirt CR 14/7
          → tiny floating-point recalibrations at 15.01 / 15.24 / 16.7 / 16.72 / 17.78
          → fixes 15.238642638… → 15.24,  16.720204285… → 16.72  etc.
          → no measure-shape change, just precision cleanup
          NB OIDs:  <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4334359&outFields=*&returnGeometry=false&f=html">4334359</a> <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4334360&outFields=*&returnGeometry=false&f=html">4334360</a> <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4334361&outFields=*&returnGeometry=false&f=html">4334361</a> <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4334545&outFields=*&returnGeometry=false&f=html">4334545</a>
          SB OIDs:  <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4334546&outFields=*&returnGeometry=false&f=html">4334546</a> <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4334547&outFields=*&returnGeometry=false&f=html">4334547</a> <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4334548&outFields=*&returnGeometry=false&f=html">4334548</a> <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4334549&outFields=*&returnGeometry=false&f=html">4334549</a>
          CR 14/7:  <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4334357&outFields=*&returnGeometry=false&f=html">4334357</a> <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4334358&outFields=*&returnGeometry=false&f=html">4334358</a>

12:06:42  RealignOverlapRouteInfo                      filed: <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=RouteId%3D%275330014000000%27%20AND%20NetworkId%3D%271%27&outFields=*&orderByFields=TransactionDate%20DESC&returnGeometry=false&f=html">5330014000000</a> (NB)  (<a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4332855&outFields=*&returnGeometry=false&f=html">OID 4332855</a>)
          ├─ RealignedPortion:    NB mi 15.24-16.72  →  NB mi 15.24-16.575  (compressed by 0.145)
          ├─ DownStreamPortion:   NB mi 16.72-20.71  →  NB mi 16.575-20.565 (downstream shifts -0.145)
          ├─ TargetOverlappedRoutes:
          │   └─ OverlappingRoutes @15.240-15.514:
          │       ├─ OverlappingSection RouteId="<a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=RouteId%3D%275340014070000%27%20AND%20NetworkId%3D%271%27&outFields=*&orderByFields=TransactionDate%20DESC&returnGeometry=false&f=html">5340014070000</a>"  ← LINK to sub-route Wirt CR 14/7
          │       │     mi 15.240-15.514 of NB = mi 0.000-0.293 of <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=RouteId%3D%275340014070000%27%20AND%20NetworkId%3D%271%27&outFields=*&orderByFields=TransactionDate%20DESC&returnGeometry=false&f=html">5340014070000</a>
          │       └─ OverlappingSection RouteId="<a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=RouteId%3D%275330014000000%27%20AND%20NetworkId%3D%271%27&outFields=*&orderByFields=TransactionDate%20DESC&returnGeometry=false&f=html">5330014000000</a>"  ← self
          └─ OverlappedPortions:
              └─ OverlappedPortion NewRouteId="<a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=RouteId%3D%2753300140000SB%27%20AND%20NetworkId%3D%271%27&outFields=*&orderByFields=TransactionDate%20DESC&returnGeometry=false&f=html">53300140000SB</a>"    ← LINK to SB
                  NB mi 15.240-16.720 ≡ SB mi 15.240-16.720 (same pavement, two designations)

12:11:14  RetireRouteInfo                              filed: <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=RouteId%3D%275340014070000%27%20AND%20NetworkId%3D%271%27&outFields=*&orderByFields=TransactionDate%20DESC&returnGeometry=false&f=html">5340014070000</a> (Wirt CR 14/7)  (<a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4332856&outFields=*&returnGeometry=false&f=html">OID 4332856</a>)
          ├─ OverlappedPortions:
          │   └─ OverlappedPortion NewRouteId="<a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=RouteId%3D%275330014000000%27%20AND%20NetworkId%3D%271%27&outFields=*&orderByFields=TransactionDate%20DESC&returnGeometry=false&f=html">5330014000000</a>"   ← LINK back to NB
          │       Wirt CR 14/7's mi 0.000-0.293 absorbed into NB mi 15.240-15.514
          ├─ RetiredPortion: 0-0.293 (the absorbed slice goes away as its own thing)
          └─ DownStreamPortion: 0.293-3.43 → 0-3.137 (the rest of Wirt CR 14/7 stays, renumbered)

12:13:14  RealignOverlapRouteInfo                      filed: <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=RouteId%3D%2753300140000SB%27%20AND%20NetworkId%3D%271%27&outFields=*&orderByFields=TransactionDate%20DESC&returnGeometry=false&f=html">53300140000SB</a> (SB)  ← <b>THE KEY EDIT</b>  (<a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4332899&outFields=*&returnGeometry=false&f=html">OID 4332899</a>)
          ├─ RealignedPortion:   SB mi 15.24-16.72  →  SB mi 15.24-16.575 (same shape as NB)
          ├─ DownStreamPortion:  SB mi 16.72-20.71  →  SB mi 16.575-20.565
          ├─ TargetOverlappedRoutes:
          │   └─ OverlappingRoutes @15.240-16.575:
          │       ├─ OverlappingSection RouteId="<a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=RouteId%3D%275330014000000%27%20AND%20NetworkId%3D%271%27&outFields=*&orderByFields=TransactionDate%20DESC&returnGeometry=false&f=html">5330014000000</a>"  ← LINK to NB
          │       │     mi 15.240-16.575 of SB ≡ mi 15.240-16.575 of NB
          │       └─ OverlappingSection RouteId="<a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=RouteId%3D%2753300140000SB%27%20AND%20NetworkId%3D%271%27&outFields=*&orderByFields=TransactionDate%20DESC&returnGeometry=false&f=html">53300140000SB</a>"  ← self
          └─ OverlappedPortions:
              └─ OverlappedPortion NewRouteId="<a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=RouteId%3D%275340014230000%27%20AND%20NetworkId%3D%271%27&outFields=*&orderByFields=TransactionDate%20DESC&returnGeometry=false&f=html">5340014230000</a>"    ← LINK to the child created at 12:01
                  SB mi 15.240-16.720 ≡ <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=RouteId%3D%275340014230000%27%20AND%20NetworkId%3D%271%27&outFields=*&orderByFields=TransactionDate%20DESC&returnGeometry=false&f=html">5340014230000</a> mi 0.000-1.511
                  ↑ THIS is where the child route gets its measures — it's published as
                    the OVERLAP TARGET of the SB realignment.
</pre>

**The link graph (with hyperlinks):**

<pre>
                   ┌────────────────────────────────────────────────────────┐
                   │  <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=RouteId%3D%275340014230000%27%20AND%20NetworkId%3D%271%27&outFields=*&orderByFields=TransactionDate%20DESC&returnGeometry=false&f=html">5340014230000</a>  (the child, FAS=5 off-system)           │
                   │  mi 0.000-1.511                                          │
                   └────────────────────────┬───────────────────────────────┘
                                            │ created via OverlappedPortion
                                            │ in <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4332899&outFields=*&returnGeometry=false&f=html">OID 4332899</a> (SB RealignOverlap)
                                            ▼
                   ┌────────────────────────────────────────────────────────┐
                   │  <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=RouteId%3D%2753300140000SB%27%20AND%20NetworkId%3D%271%27&outFields=*&orderByFields=TransactionDate%20DESC&returnGeometry=false&f=html">53300140000SB</a>  (Wirt WV 14 SB)                         │
                   │  mi 15.240-16.575 — the overlap section                 │
                   └────────────────────────┬───────────────────────────────┘
                                            │ overlap via OverlappingSection
                                            │ in <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4332899&outFields=*&returnGeometry=false&f=html">OID 4332899</a> AND in <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4332855&outFields=*&returnGeometry=false&f=html">OID 4332855</a>
                                            ▼
                   ┌────────────────────────────────────────────────────────┐
                   │  <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=RouteId%3D%275330014000000%27%20AND%20NetworkId%3D%271%27&outFields=*&orderByFields=TransactionDate%20DESC&returnGeometry=false&f=html">5330014000000</a>  (Wirt WV 14 NB)  ← the case-study        │
                   │  mi 15.240-16.575 — the overlap section                 │
                   └────────────────────────┬───────────────────────────────┘
                                            │ overlap via OverlappingSection
                                            │ in <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4332855&outFields=*&returnGeometry=false&f=html">OID 4332855</a> (NB RealignOverlap)
                                            ▼
                   ┌────────────────────────────────────────────────────────┐
                   │  <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=RouteId%3D%275340014070000%27%20AND%20NetworkId%3D%271%27&outFields=*&orderByFields=TransactionDate%20DESC&returnGeometry=false&f=html">5340014070000</a>  (Wirt CR 14/7, FC=9 sub-route)         │
                   │  mi 0.000-0.293  ≡  NB mi 15.240-15.514  (subset only)  │
                   │  retired-with-overlap in <a href="https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4332856&outFields=*&returnGeometry=false&f=html">OID 4332856</a>                    │
                   └────────────────────────────────────────────────────────┘
</pre>

---

## The full chain: 14 layer-132 operations in 12 minutes

All operations were filed on 2026-02-27 by a single editor against the WVDOH Publication LRS, NetworkId=1. Sorted chronologically:

| # | Time | OID | ActivityType | Filed under RouteId | Notes |
|--|--|--|--|--|--|
| 1 | 12:01:22 | **4334355** | CreateRoute | 5340014230000 | Birth certificate — empty child route reserved |
| 2 | 12:04:47 | 4334357 | Calibrate | 5340014070000 | Wirt CR 14/7 precision recalibration |
| 3 | 12:04:47 | 4334358 | Calibrate | 5340014070000 | Wirt CR 14/7 precision recalibration |
| 4 | 12:04:47 | 4334359 | Calibrate | 5330014000000 | NB precision recalibration |
| 5 | 12:04:47 | 4334360 | Calibrate | 5330014000000 | NB precision recalibration |
| 6 | 12:04:47 | 4334361 | Calibrate | 5330014000000 | NB precision recalibration |
| 7 | 12:04:47 | 4334545 | Calibrate | 5330014000000 | NB precision recalibration |
| 8 | 12:04:47 | 4334546 | Calibrate | 53300140000SB | SB precision recalibration |
| 9 | 12:04:47 | 4334547 | Calibrate | 53300140000SB | SB precision recalibration |
| 10 | 12:04:47 | 4334548 | Calibrate | 53300140000SB | SB precision recalibration |
| 11 | 12:04:47 | 4334549 | Calibrate | 53300140000SB | SB precision recalibration |
| 12 | 12:06:42 | **4332855** | RealignOverlap | 5330014000000 (NB) | NB overlap with Wirt CR 14/7 declared + SB overlap declared |
| 13 | 12:11:14 | **4332856** | Retire | 5340014070000 | Wirt CR 14/7 partial retire-with-overlap into NB |
| 14 | 12:13:14 | **4332899** | RealignOverlap | 53300140000SB (SB) | SB overlap with NB declared + child overlap declared ← **the key edit** |

Direct REST URLs for the four bolded edits (the ones that move pavement around, not just cleanup):

```
OID 4334355  Create child:               https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4334355&outFields=*&returnGeometry=false&f=html
OID 4332855  NB RealignOverlap:          https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4332855&outFields=*&returnGeometry=false&f=html
OID 4332856  Wirt CR 14/7 Retire:        https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4332856&outFields=*&returnGeometry=false&f=html
OID 4332899  SB RealignOverlap (KEY):    https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query?where=ObjectId%3D4332899&outFields=*&returnGeometry=false&f=html
```

---

## The link graph

```
                   ┌────────────────────────────────────────────────────────┐
                   │  5340014230000  (the child, FAS=5 off-system, FC=8)     │
                   │  mi 0.000-1.511                                          │
                   └────────────────────────┬───────────────────────────────┘
                                            │ created via OverlappedPortion
                                            │ in OID 4332899 (SB RealignOverlap)
                                            ▼
                   ┌────────────────────────────────────────────────────────┐
                   │  53300140000SB  (Wirt WV 14 southbound)                 │
                   │  mi 15.240-16.575 — the overlap section                 │
                   └────────────────────────┬───────────────────────────────┘
                                            │ overlap declared via OverlappingSection
                                            │ in OID 4332899 AND in OID 4332855
                                            ▼
                   ┌────────────────────────────────────────────────────────┐
                   │  5330014000000  (Wirt WV 14 northbound — the parent)    │
                   │  mi 15.240-16.575 — the overlap section                 │
                   └────────────────────────┬───────────────────────────────┘
                                            │ overlap declared via OverlappingSection
                                            │ in OID 4332855 (NB RealignOverlap)
                                            ▼
                   ┌────────────────────────────────────────────────────────┐
                   │  5340014070000  (Wirt CR 14/7, FC=9 sub-route)          │
                   │  mi 0.000-0.293  ≡  NB mi 15.240-15.514  (subset only)  │
                   │  retired-with-overlap in OID 4332856                    │
                   └────────────────────────────────────────────────────────┘
```

**All four routes describe the same physical pavement at WV 14 mile 15.240–16.575.** Some cover the whole overlap, some only a sub-section. The LRS records this as a four-way concurrency, with each route ID carrying a different attribute set (federal aid status, functional class, directional designation, off-system flag, etc.).

---

## Which edit links what to what

| OID | Action | Routes named in the XML | Net effect |
|--|--|--|--|
| 4334355 | Create | `5340014230000` (self only) | Empty child route reserved |
| 4334357/4334358 | Calibrate ×2 | `5340014070000` (self only) | Wirt CR 14/7 measures cleaned |
| 4334359–4334361, 4334545 | Calibrate ×4 | `5330014000000` (self only) | NB measures cleaned |
| 4334546–4334549 | Calibrate ×4 | `53300140000SB` (self only) | SB measures cleaned |
| **4332855** | RealignOverlap | `5330014000000` + `5340014070000` + `53300140000SB` | NB declares concurrency with Wirt CR 14/7 (subset) and with SB (full overlap) |
| **4332856** | Retire | `5340014070000` + `5330014000000` | Wirt CR 14/7's mi 0-0.293 absorbed into NB mi 15.240-15.514; the rest stays as a renumbered 0-3.137 route |
| **4332899** | RealignOverlap | `53300140000SB` + `5330014000000` + `5340014230000` | SB declares concurrency with NB and with the child; child gets its measures here |

The transitive path from NB to child:

```
NB ─(named in 4332855, as OverlappedPortion NewRouteId)─▶ SB ─(named in 4332899, as OverlappedPortion NewRouteId)─▶ child
```

The NB's own XML never names the child directly. The link is one transitive hop away through the SB side.

---

## Full decoded XML for each link-carrying edit

### OID 4334355 — Create child route (12:01:22)

The child route's birth certificate. Note `FirstM="NaN" LastM="NaN"` — the route exists but has no measures yet. Measures get assigned 12 minutes later in OID 4332899.

```xml
<RouteEditModel xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                SchemaVersion="2">
  <RouteEditActivity xsi:type="CreateRouteInfo"
                     LrsId="e6cb38f1-462f-42f8-9079-665ff51ee4d6"
                     NetworkId="1"
                     RouteId="5340014230000"
                     NewRouteId="5340014230000"
                     OperationTime="2026-02-27T00:00:00"
                     FirstM="NaN"
                     LastM="NaN"
                     IsPerformDownstreamCalibration="false"
                     DoNotApplyEventBehaviors="true"/>
</RouteEditModel>
```

### OID 4332855 — NB RealignOverlap (12:06:42)

NB declares its mi 15.24–16.72 is recalibrated to mi 15.24–16.575, with the upstream portion realigned and the downstream tail shifting by –0.145. Two concurrency declarations: NB ↔ Wirt CR 14/7 (the small sub-route, at mi 15.24–15.514 only) AND NB ↔ SB (the whole 15.24–16.72 overlap region).

```xml
<RouteEditModel xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                SchemaVersion="2">
  <RouteEditActivity xsi:type="RealignOverlapRouteInfo"
                     LrsId="e6cb38f1-462f-42f8-9079-665ff51ee4d6"
                     NetworkId="1"
                     RouteId="5330014000000"
                     NewRouteId="5330014000000"
                     OperationTime="2026-02-27T00:00:00"
                     FirstM="-0" LastM="20.71"
                     IsPerformDownstreamCalibration="true"
                     DoNotApplyEventBehaviors="false"
                     IsFirstPointTouches="true" IsLastPointTouches="true"
                     GapCalibrationType="SteppingIncrement"
                     GapCalibrationOffset="0">

    <RealignedPortion  OldFromMeasure="15.24" OldToMeasure="16.72"
                       NewFromMeasure="15.24" NewToMeasure="16.575"/>

    <TargetOverlappedRoutes>
      <OverlappingRoutes FromMeasure="15.240000027" ToMeasure="15.513815519"
                         OriginatingRouteId="5330014000000">
        <OverlappingRouteSections>
          <!-- LINK A: NB ↔ Wirt CR 14/7 sub-route -->
          <OverlappingSection RouteId="5340014070000"
                              FromValue="-2.7E-08" ToValue="0.293000013"
                              PriorityId="5330014000000">
            <MeasureTranslations>
              <ModifiedSegment OldFromMeasure="15.240000027" OldToMeasure="15.513815519"
                               NewFromMeasure="-2.7E-08"     NewToMeasure="0.293000013"/>
            </MeasureTranslations>
          </OverlappingSection>
          <OverlappingSection RouteId="5330014000000"
                              FromValue="15.240000027" ToValue="15.513815519"
                              PriorityId="5330014000000">
            <MeasureTranslations>
              <ModifiedSegment OldFromMeasure="15.240000027" OldToMeasure="15.513815519"
                               NewFromMeasure="15.240000027" NewToMeasure="15.513815519"/>
            </MeasureTranslations>
          </OverlappingSection>
        </OverlappingRouteSections>
      </OverlappingRoutes>
    </TargetOverlappedRoutes>

    <DownStreamPortion OldFromMeasure="16.72" OldToMeasure="20.71"
                       NewFromMeasure="16.575" NewToMeasure="20.565"/>
    <UpStreamPortion   OldFromMeasure="15.01" OldToMeasure="15.24"
                       NewFromMeasure="15.01" NewToMeasure="15.24"/>
    <NewGappedGroupsMeasures/>
    <PreviousGappedGroupsMeasures/>

    <OverlappedPortions>
      <!-- LINK B: NB ↔ SB (declared as OverlappedPortion target) -->
      <OverlappedPortion OldFromMeasure="15.240000027" OldToMeasure="16.719999975"
                         NewFromMeasure="15.240000027" NewToMeasure="16.719999975"
                         NewRouteId="53300140000SB">
        <MeasureTranslations>
          <ModifiedSegment OldFromMeasure="15.240000027" OldToMeasure="16.248641842"
                           NewFromMeasure="15.240000027" NewToMeasure="16.248641842"/>
          <ModifiedSegment OldFromMeasure="16.248641842" OldToMeasure="16.700000003"
                           NewFromMeasure="16.248641842" NewToMeasure="16.700000003"/>
          <ModifiedSegment OldFromMeasure="16.700000003" OldToMeasure="16.719999975"
                           NewFromMeasure="16.700000003" NewToMeasure="16.719999975"/>
        </MeasureTranslations>
      </OverlappedPortion>
    </OverlappedPortions>
  </RouteEditActivity>
</RouteEditModel>
```

### OID 4332856 — Wirt CR 14/7 Retire (12:11:14)

Wirt CR 14/7 (5340014070000) is partially retired. Its mi 0.000–0.293 portion is absorbed (as an OverlappedPortion target) onto NB mi 15.240–15.514. The remaining 0.293–3.430 stays alive but gets renumbered to 0.000–3.137 (the route loses its head but keeps the rest). This is what produced the FC=9 segment we saw on the parent in earlier analysis.

```xml
<RouteEditModel xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                SchemaVersion="2">
  <RouteEditActivity xsi:type="RetireRouteInfo"
                     LrsId="e6cb38f1-462f-42f8-9079-665ff51ee4d6"
                     NetworkId="1"
                     RouteId="5340014070000"
                     OperationTime="2026-02-27T00:00:00"
                     FirstM="-0" LastM="3.43"
                     IsPerformDownstreamCalibration="true"
                     DoNotApplyEventBehaviors="false"
                     IsUseWholeRoute="false">

    <OverlappedPortions>
      <!-- LINK C: Wirt CR 14/7 ↔ NB (the 0-0.293 piece becomes NB's 15.240-15.514) -->
      <OverlappedPortion OldFromMeasure="-0"     OldToMeasure="0.293"
                         NewFromMeasure="15.240000027" NewToMeasure="15.513815519"
                         NewRouteId="5330014000000">
        <MeasureTranslations>
          <ModifiedSegment OldFromMeasure="-0"   OldToMeasure="0.293"
                           NewFromMeasure="15.240000027" NewToMeasure="15.513815519"/>
        </MeasureTranslations>
      </OverlappedPortion>
    </OverlappedPortions>

    <RetiredPortion    OldFromMeasure="-0"    OldToMeasure="0.293"
                       NewFromMeasure="NaN"   NewToMeasure="NaN"/>
    <DownStreamPortion OldFromMeasure="0.293" OldToMeasure="3.43"
                       NewFromMeasure="0"     NewToMeasure="3.137"/>
  </RouteEditActivity>
</RouteEditModel>
```

### OID 4332899 — SB RealignOverlap (12:13:14) — the key edit

This is the one that **gives the child route its measures**. SB declares its mi 15.24–16.575 is concurrent with NB at the same measures, AND publishes the same pavement under a third designation (`5340014230000`) at mi 0.000–1.511. The child's measures are written as the OverlappedPortion mapping: SB mi 15.240–16.720 maps to child mi 0.000–1.511.

```xml
<RouteEditModel xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                SchemaVersion="2">
  <RouteEditActivity xsi:type="RealignOverlapRouteInfo"
                     LrsId="e6cb38f1-462f-42f8-9079-665ff51ee4d6"
                     NetworkId="1"
                     RouteId="53300140000SB"
                     NewRouteId="53300140000SB"
                     OperationTime="2026-02-27T00:00:00"
                     FirstM="-0" LastM="20.71"
                     IsPerformDownstreamCalibration="true"
                     DoNotApplyEventBehaviors="false"
                     IsFirstPointTouches="true" IsLastPointTouches="true"
                     GapCalibrationType="SteppingIncrement"
                     GapCalibrationOffset="0">

    <RealignedPortion OldFromMeasure="15.24" OldToMeasure="16.72"
                      NewFromMeasure="15.24" NewToMeasure="16.575"/>

    <TargetOverlappedRoutes>
      <OverlappingRoutes FromMeasure="15.240000027" ToMeasure="16.575"
                         OriginatingRouteId="53300140000SB">
        <OverlappingRouteSections>
          <!-- LINK D: SB ↔ NB (full overlap mi 15.240-16.575) -->
          <OverlappingSection RouteId="5330014000000"
                              FromValue="15.240000027" ToValue="16.575000004"
                              PriorityId="5330014000000">
            <MeasureTranslations>
              <ModifiedSegment OldFromMeasure="15.240000027" OldToMeasure="15.513815519"
                               NewFromMeasure="15.240000027" NewToMeasure="15.513815519"/>
              <ModifiedSegment OldFromMeasure="15.513815519" OldToMeasure="16.575"
                               NewFromMeasure="15.513815519" NewToMeasure="16.575000004"/>
            </MeasureTranslations>
          </OverlappingSection>
          <OverlappingSection RouteId="53300140000SB"
                              FromValue="15.240000027" ToValue="16.575"
                              PriorityId="53300140000SB">
            <MeasureTranslations>
              <ModifiedSegment OldFromMeasure="15.240000027" OldToMeasure="15.513815519"
                               NewFromMeasure="15.240000027" NewToMeasure="15.513815519"/>
              <ModifiedSegment OldFromMeasure="15.513815519" OldToMeasure="16.575"
                               NewFromMeasure="15.513815519" NewToMeasure="16.575"/>
            </MeasureTranslations>
          </OverlappingSection>
        </OverlappingRouteSections>
      </OverlappingRoutes>
    </TargetOverlappedRoutes>

    <DownStreamPortion OldFromMeasure="16.72" OldToMeasure="20.71"
                       NewFromMeasure="16.575" NewToMeasure="20.565"/>
    <UpStreamPortion   OldFromMeasure="15.01" OldToMeasure="15.24"
                       NewFromMeasure="15.01" NewToMeasure="15.24"/>
    <NewGappedGroupsMeasures/>
    <PreviousGappedGroupsMeasures/>

    <OverlappedPortions>
      <!-- LINK E: SB ↔ the child (THIS is how 5340014230000 gets its measures) -->
      <OverlappedPortion OldFromMeasure="15.240000027" OldToMeasure="16.719999975"
                         NewFromMeasure="-2.7E-08"     NewToMeasure="1.511000005"
                         NewRouteId="5340014230000">
        <MeasureTranslations>
          <ModifiedSegment OldFromMeasure="15.240000027" OldToMeasure="16.248641842"
                           NewFromMeasure="-2.7E-08"     NewToMeasure="1.031433824"/>
          <ModifiedSegment OldFromMeasure="16.248641842" OldToMeasure="16.700000003"
                           NewFromMeasure="1.031433824"  NewToMeasure="1.492991213"/>
          <ModifiedSegment OldFromMeasure="16.700000003" OldToMeasure="16.719999975"
                           NewFromMeasure="1.492991213"  NewToMeasure="1.511000005"/>
        </MeasureTranslations>
      </OverlappedPortion>
    </OverlappedPortions>
  </RouteEditActivity>
</RouteEditModel>
```

---

## Why the NB → child link is invisible to a naive lookup

If someone queried layer 132 with `where=RouteId='5340014230000'`, they would only find OID 4334355 — the empty CreateRoute. That returns no measures, no overlaps, no link to anything.

If they instead queried `where=RouteId='5330014000000'`, they would find OID 4332855 (the NB RealignOverlap) — but its XML only mentions `5340014070000` (Wirt CR 14/7) and `53300140000SB` (SB), **not** the child.

The only edit whose XML directly names the child is OID 4332899, filed under `53300140000SB`. So unless you walk **every** route-ID-carrying attribute across **every** edit in the chain, the NB→child relationship looks invisible. That's exactly the data-model trap that the bidirectional index in §4.2.1 of the working analysis exists to defeat.

---

## What the chain produces in the LRS event layers

After all 14 operations propagate event behavior, the WV 14 corridor's mile 15.240–16.575 region holds **four concurrent route IDs**, each carrying a different attribute set:

| Route ID | Direction | Functional class | Federal aid | Coverage of the overlap |
|--|--|--|--|--|
| 5330014000000 | NB mainline | FC=7 | FAS=3 (eligible) | full 15.240–16.575 |
| 53300140000SB | SB mainline | FC=7 | FAS=3 (eligible) | full 15.240–16.575 |
| 5340014230000 | child overlay | FC=8 | FAS=5 (off-system) | full 1.511 mi (= 15.240–16.575 of parent) |
| 5340014070000 | sub-route | FC=9 | FAS=5 (off-system) | partial — only 0.000–0.293 (= 15.240–15.514) |

All four describe the same physical pavement. They differ in:

- **Direction** (NB vs SB, which matters for traffic-side accounting on this stretch where US 33 has separated carriageways)
- **Functional class** (the sub-routes are reclassified down to Local)
- **Federal aid eligibility** (the parent mainlines are eligible; the child overlay and small sub-route are off-system)

The companion working analysis §4 shows how this four-way concurrency caused 14.80 CMP-miles of attribution loss in Deighton when the new LRS snapshot was re-clipped — specifically because Deighton's re-clip only follows one route ID at a time and can't propagate measure ranges across the four-way concurrency.

---

## Reproducibility

To pull the full chain yourself:

```
# All 14 edits on 2026-02-27 touching any of the four routes
curl 'https://gis.transportation.wv.gov/arcgis/rest/services/Roads_And_Highways/Publication_LRS/MapServer/132/query' \
  --data-urlencode "where=(RouteId IN ('5330014000000','53300140000SB','5340014230000','5340014070000')) AND TransactionDate > date '2026-02-26' AND TransactionDate < date '2026-02-28'" \
  --data-urlencode "outFields=*" \
  --data-urlencode "returnGeometry=false" \
  --data-urlencode "f=json" \
  -G
```

Each row's `EditDataXml` is base64-encoded. Decode in Python:

```python
import base64, json, urllib.request
url = "...(query URL above)..."
data = json.load(urllib.request.urlopen(url))
for f in data['features']:
    xml = base64.b64decode(f['attributes']['EditDataXml']).decode()
    print(xml)
```

To search for any route ID across the entire chain (or any subset of edits), parse the XML and walk every element's `RouteId`, `NewRouteId`, `PriorityId`, and `OriginatingRouteId` attributes — those four attribute names cover every route-ID-carrying position in the WV LRS edit schema.
