# Segment Breakdown by Intersections

> **Superseded for refreshing data:** the data refresh is now one staged command documented in [PMS — Data Pipeline](/docs/PMS_Data_Pipeline). This page is kept for background; where they disagree, the Data Pipeline page is right.


Reference documentation for `scripts/joint_breakdown_intersections.py` — the pipeline that takes raw pavement joint segments, combines them into continuous LRS sections, and subdivides oversized sections at significant intersections ranked by AADT.

---

## Overview

The WVDOT pavement management system groups pavement condition data into "joints" — contiguous segments on a route that share similar characteristics. These vendor-supplied joints can range from fractions of a mile to over 40 miles, making them impractical as individual paving project units. This script breaks them down into manageable 2-4 mile segments using real intersection locations, prioritizing the most significant intersections (highest traffic volume) as break points.

The pipeline has three stages:

```
Stage 1: Raw Joints → Continuous LRS Sections (preprocessing)
Stage 2: LRS Sections → Candidate Break Points (intersection + AADT lookup)
Stage 3: Candidate Break Points → Final Sub-Segments (greedy AADT-priority selection)
```

---

## Usage

```bash
python scripts/joint_breakdown_intersections.py
```

No arguments required. All paths are derived from the repository root.

---

## Input Files

### 1. `pavement_joints_lrs.csv`

The primary input file containing pavement joint segments on the LRS (Linear Referencing System).

| Column | Type | Description |
|--------|------|-------------|
| `routeid` | string (13 chars) | WVDOT route identifier |
| `bmp` | float | Beginning milepost |
| `emp` | float | Ending milepost |
| `joint_id` | string | Vendor-assigned joint identifier (e.g., `70_623232`) |

Typical row count: ~24,000 segments.

### 2. `intersections.sqlite`

SQLite database containing intersection geometry as a node-route graph. Two tables:

**`nodes`** — Unique geographic intersection points.

| Column | Type | Description |
|--------|------|-------------|
| `node_id` | INTEGER (PK) | Auto-increment identifier |
| `geohash` | TEXT (UNIQUE) | 9-character geohash encoding of location |

Indexed on `geohash`. Approximately 428,000 nodes.

**`node_routes`** — Junction table linking nodes to routes with their mile point positions.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER (PK) | Auto-increment identifier |
| `node_id` | INTEGER (FK) | References `nodes.node_id` |
| `route_id` | TEXT | 13-character WVDOT route identifier |
| `measure` | REAL | Mile point on the route where the node falls |

Indexed on `node_id` and `route_id`. Approximately 868,000 entries across 93,000 unique routes.

**How intersections are represented:** Two routes intersect when they share the same `node_id`. For example, if node 12345 has entries for both route A at measure 5.2 and route B at measure 11.7, then route A crosses route B at those respective mile points.

**Manual intersection additions:** If the database is missing a known intersection, it can be added manually by creating a new node and linking both routes:

```sql
INSERT INTO nodes (geohash) VALUES ('custom_label');
INSERT INTO node_routes (node_id, route_id, measure)
    VALUES ((SELECT node_id FROM nodes WHERE geohash = 'custom_label'),
            '2030622000000', 10.27);
INSERT INTO node_routes (node_id, route_id, measure)
    VALUES ((SELECT node_id FROM nodes WHERE geohash = 'custom_label'),
            '2040007000000', 0.0);
```

### 3. `2.csv`

Annual Average Daily Traffic (AADT) data exported from the WVDOT road inventory.

| Column | Type | Description |
|--------|------|-------------|
| `ROUTE_ID` | string | 13-character route identifier |
| `FROM_MEASURE` | float | Start milepost of the AADT segment |
| `TO_MEASURE` | float | End milepost of the AADT segment |
| `AADT` | integer | Annual Average Daily Traffic count (vehicles/day) |

Other columns exist (`AADTT`, `K_Factor`, `D_Factor`, `FUTURE_AADT`, etc.) but are not used by this script. Approximately 46,000 rows covering 26,700 unique routes.

---

## Output File

### `pavement_joints_lrs_breakdown.csv`

| Column | Type | Description |
|--------|------|-------------|
| `routeid` | string | Route identifier (unchanged from input) |
| `bmp` | float (3 decimals) | Beginning milepost of the sub-segment |
| `emp` | float (3 decimals) | Ending milepost of the sub-segment |
| `joint_id` | string | Original joint identifier from the input |
| `sub_joint_id` | integer | Sequential sub-segment number within the joint (1, 2, 3...) |
| `termini_routeid` | string | Route ID of the intersecting road at this sub-segment's end milepost. Empty for the last sub-segment of each section (ends at original emp) and for unsplit segments. |
| `termini_aadt` | integer | AADT of the termini route. Empty when `termini_routeid` is empty. |
| `termini_label` | string | Human-readable label describing the sub-segment's extents. Format: `"Start -> CO 7"`, `"CO 7 -> US 19"`, `"US 19 -> End"`. Uses the route label generator ported from `routeIdParser.ts`. |

Example output for a split section:

```
routeid,bmp,emp,joint_id,sub_joint_id,termini_routeid,termini_aadt,termini_label
01201190000NB,0.0,1.937,70_669268,1,0140119150000,30,Start -> CO 119/15
01201190000NB,1.937,3.029,70_669268,2,0140011000000,600,CO 119/15 -> CO 11
01201190000NB,3.029,4.399,70_669268,3,0140119130000,90,CO 11 -> CO 119/13
01201190000NB,4.399,5.76,70_669268,4,0140036000000,300,CO 119/13 -> CO 36
...
01201190000NB,15.979,18.68,70_669268,11,,,CO 6 -> End
```

---

## Stage 1: Preprocessing — Combine into LRS Sections

**Function:** `combine_into_lrs_sections()`

Before any splitting logic runs, the raw joints are consolidated into continuous LRS sections. The input file contains many small, fragmented joints — often under 0.5 miles — that are artifacts of the vendor segmentation process. Adjacent joints on the same route that touch (one's `emp` equals the next's `bmp`, within a 0.001 mi tolerance) are merged into a single continuous section.

**Algorithm:**

1. Sort all joints by `routeid` then `bmp`.
2. Walk each route sequentially. If the current segment's `bmp` matches the previous segment's `emp` (within tolerance), extend the current section's `emp`.
3. When a gap is found (segments don't touch), emit the current section and start a new one.
4. The merged section keeps the `joint_id` of its first constituent joint.

**Effect:** Typically reduces ~24,000 raw joints to ~15,700 LRS sections by merging ~8,700 touching segments. This ensures the splitter evaluates complete route corridors rather than artificial joint boundaries.

**Example:**

Route `0140005000000` has four raw joints:
```
0.000-0.110  (0.11 mi)  70_623142
0.110-1.500  (1.39 mi)  70_623141
1.500-1.960  (0.46 mi)  70_623144
1.960-3.560  (1.60 mi)  70_623143
```

All four touch end-to-end, so they merge into one section:
```
0.000-3.560  (3.56 mi)  70_623142
```

This 3.56-mile section now enters the splitter as a single unit to be evaluated.

---

## Stage 2: Build Candidate Break Points

**Function:** `build_candidates()`

For each LRS section longer than 3.0 miles, the script identifies every intersection within its extent and scores it by the AADT of the crossing route.

### Step 2a: Bulk Intersection Query

A single SQL query fetches all intersection pairs for every route that has at least one oversized section. The query self-joins `node_routes` on `node_id` to find cross routes:

```sql
SELECT nr1.route_id, nr1.node_id, nr1.measure,
       nr2.route_id AS cross_route, nr2.measure AS cross_measure
FROM node_routes nr1
JOIN node_routes nr2
  ON nr1.node_id = nr2.node_id AND nr1.route_id != nr2.route_id
WHERE nr1.route_id IN (...)
```

This bulk approach loads ~380,000 intersection pairs in approximately 1 second, versus running individual queries per segment.

### Step 2b: Filter Cross Routes

Not all intersecting routes are valid termini. The following filters are applied:

1. **Sign system filter:** Only cross routes with sign system (3rd character of route ID) in `{1, 2, 3, 4, 7}` are kept. This includes Interstates (1), US routes (2), WV state routes (3), County routes (4), and FANS routes (7). Minor systems like State Parks (6), HARP roads (8), and maintenance routes (0) are excluded.

2. **Ramp filter:** Cross routes longer than 13 characters are excluded. Ramp route IDs in the WVDOT system are 17 characters (e.g., `04100790026000048`).

3. **Opposite-direction filter:** For sign system 2 (US routes), a cross route with the same first 11 characters as the segment's route is excluded. This prevents `44201190000SB` from being listed as a termini for `44201190000NB` — they are the same road, just opposite directions.

### Step 2c: AADT Lookup

For each candidate intersection, the AADT of the cross route is looked up from `2.csv`:

1. **Direct match:** Find an AADT segment where `FROM_MEASURE <= cross_measure <= TO_MEASURE` (with 0.01 mi tolerance).
2. **Nearest match:** If no direct overlap, find the nearest AADT segment within 1.0 mile.
3. **Parent route fallback:** If the cross route has no AADT data (common for sub-routes like CO 7/8), the script derives the parent route by zeroing the sub-route digits (characters 7-8) of the route ID. For example, `2040007080000` (CO 7/8) falls back to `2040007000000` (CO 7). The maximum AADT on the parent route is used as a significance proxy.
4. **No match:** Candidates with no AADT from any lookup get AADT = 0. They can still serve as break points but rank lowest.

### Step 2d: Aggregate Per Node

A single physical intersection may have multiple cross routes (e.g., a 3-way junction). The script groups by `node_id` and keeps only the cross route with the highest AADT per node.

### Step 2e: Cluster Nearby Nodes

Nodes within 0.1 miles of each other on the target route represent essentially the same physical location (artifacts of geohash resolution or overlapping route geometries). These are clustered, keeping the entry with the highest AADT in each cluster.

---

## Stage 3: Break-Point Selection — Greedy AADT Priority

**Function:** `select_best_breakpoints()`

The selection algorithm is greedy and AADT-first: the most significant intersections are always placed as break points, and the segmentation is built around them.

### Phase 1: Seed

1. Sort all candidate break points by AADT descending (highest first).
2. Walk the ranked list. For each candidate, check if adding it as a break point would cause any resulting sub-segment to fall below the hard minimum length (1.0 mile).
3. If the spacing constraint is satisfied, the candidate is placed. If not, it is skipped for now.

This ensures the highest-AADT intersections are always used as break points, regardless of where they fall in the segment. The algorithm builds the segmentation around these anchor points.

### Phase 2: Fill

After seeding, some sub-segments may still exceed the target maximum length (4.0 miles) — particularly in stretches with few high-AADT intersections. The fill phase walks the skipped candidates (next-highest AADT) and places them if:

- They fall within a sub-segment that still exceeds 4.0 miles.
- Adding them doesn't violate the hard minimum spacing.

### Spacing Constraints

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `MAX_SEGMENT_LEN` | 3.0 mi | Threshold for splitting. Sections at or below this pass through unchanged. |
| `TARGET_MIN_LEN` | 2.0 mi | Preferred minimum sub-segment length |
| `TARGET_MAX_LEN` | 4.0 mi | Preferred maximum. The fill phase tries to break sub-segments exceeding this. |
| `EDGE_MIN_LEN` | 1.5 mi | Relaxed minimum for the first and last sub-segment of a section |
| `HARD_MIN_LEN` | 1.0 mi | Absolute floor. No sub-segment is ever created shorter than this. |

### Example

Consider a 17.45-mile section on route `2030622000000` with these candidate intersections:

```
mp=2.108   I 64    AADT=56,300
mp=4.228   CO 10   AADT=8,600
mp=13.940  CO 21   AADT=7,900
mp=5.758   WV 501  AADT=3,200
mp=10.270  CO 7    AADT=700
...
```

**Seed phase** (sorted by AADT):
1. I 64 @ 2.108 (AADT 56,300) — placed first (highest)
2. CO 10 @ 4.228 (AADT 8,600) — placed (2.12 mi from I 64, valid)
3. CO 21 @ 13.940 (AADT 7,900) — placed (9.71 mi from CO 10, valid)
4. WV 501 @ 5.758 (AADT 3,200) — placed (1.53 mi from CO 10, valid)
5. CO 7 @ 10.270 (AADT 700) — placed (4.51 mi from WV 501, valid)
6. ...additional lower-AADT candidates placed if spacing allows

**Fill phase:** Check remaining sub-segments > 4.0 mi and fill with next-best skipped candidates.

**Result:** The section is divided at I 64, CO 10, WV 501, CO 7, CO 21, and additional intersections — always anchored around the highest-traffic roads.

---

## Route Label Generation

**Function:** `route_label()`

Human-readable labels are generated from 13-character route IDs using logic ported from the frontend `routeIdParser.ts`. The route ID structure:

```
Position:  0  1  2  3  4  5  6  7  8  9  10 11 12
Example:   2  0  2  0  0  1  9  0  0  0  0  E  B
           │  │  │  │─────│  │──│  │──│  │──│
           │  │  │  route#   sub   suppl  direction
           │  │  sign system (2 = US)
           county code (20 = Kanawha)
```

**Sign system codes and labels:**

| Code | Label | Description |
|------|-------|-------------|
| 1 | I | Interstate |
| 2 | US | US Route |
| 3 | WV | WV State Route |
| 4 | CO | County Route |
| 7 | FANS | Federal Aid Non-System |
| 0 | MNS | Maintenance |
| 6 | STATE PARK | State Park Road |
| 8 | HARP | Highway Appalachian Regional Program |

**Label format:**
- `I 64` — Interstate 64 (sign system 1, route 0064, sub-route 00)
- `US 19` — US Route 19 (sign system 2, route 0019, sub-route 00)
- `CO 7/8` — County Route 7, sub-route 8 (sign system 4, route 0007, sub-route 08)
- `HARP 11/1` — HARP 11 sub-route 1 (sign system 8, route 0011, sub-route 01)

Leading zeros are stripped from route and sub-route numbers. Sub-route is omitted when it equals 0.

### Termini Label Construction

Each sub-segment gets a `termini_label` showing its extent in human-readable form:

- **First sub-segment:** `"Start -> {label at emp}"`
- **Middle sub-segments:** `"{label at bmp} -> {label at emp}"`
- **Last sub-segment:** `"{label at bmp} -> End"`
- **Unsplit segments:** `"Start -> End"`

The "label at bmp" of a sub-segment is the termini label of the previous sub-segment — i.e., the intersecting route at the shared break point.

---

## Edge Cases and Fallback Behavior

### Segments <= 3.0 miles

Pass through unchanged with `sub_joint_id = 1`, empty `termini_routeid` and `termini_aadt`, and `termini_label = "Start -> End"`.

### No intersection candidates found

Some routes have no intersections in the database within their extent, or all cross routes are filtered out by the sign system / ramp / opposite-direction rules. These sections pass through unsplit. Typically ~500 sections out of ~2,600 long sections.

### All candidates have AADT = 0

The algorithm still works — it seeds candidates in the order they appear (all tied at 0) and the fill phase breaks up long sub-segments. The result is a reasonable spatial distribution of break points, just without AADT-based prioritization.

### Gaps in the route (non-touching segments)

The LRS section combiner only merges touching segments. If two joints on the same route have a gap between them (one's `emp` < next's `bmp`), they remain separate sections and are processed independently.

### Very long sections (30+ miles)

The greedy algorithm handles these naturally. High-AADT intersections are placed first as anchors, then lower-AADT ones fill gaps. A 30-mile section might produce 10-15 sub-segments. The algorithm runs in under 1 second regardless of section length.

---

## Tunable Parameters

All parameters are defined as constants at the top of the script:

```python
MAX_SEGMENT_LEN = 3.0       # mi — sections above this get split
TARGET_MIN_LEN  = 2.0       # mi — preferred minimum sub-segment length
TARGET_MAX_LEN  = 4.0       # mi — preferred maximum; fill phase targets this
EDGE_MIN_LEN    = 1.5       # mi — relaxed minimum for first/last sub-segment
HARD_MIN_LEN    = 1.0       # mi — absolute floor, never create shorter
CLUSTER_THRESHOLD = 0.1     # mi — merge intersection nodes closer than this
VALID_SIGN_SYS = {"1", "2", "3", "4", "7"}  # allowed termini sign systems
```

---

## Performance

The script processes ~15,700 LRS sections (~2,600 requiring splitting) in approximately 2-3 minutes. The bottleneck is the per-segment AADT lookup via `DataFrame.apply()`. The intersection database query runs in ~1 second as a bulk operation.

Typical output: ~22,000-23,000 rows (up from ~15,700 input sections).
