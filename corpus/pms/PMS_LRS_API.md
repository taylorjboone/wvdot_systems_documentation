# PMS — LRS API (geometryToMeasure)

Converts GPS points into WVDOT route milepoints on the roads2 LRS geometry. The request and response are **the same as the dashcam service** (`https://vision.transportation.wv.gov/dashcam/api/ds/geometryToMeasure`), so a client of that service can switch by changing only the URL and adding authentication.

Related: [Data Pipeline](/docs/PMS_Data_Pipeline) (the main user of this API) · [Business Logic](/docs/PMS_Business_Logic)

## Endpoint

```
POST /api/lrs/geometryToMeasure          (https://mmsdev.transportation.wv.gov/pms/api/lrs/geometryToMeasure)
```

**Authentication:** either one works.
- A WVDOT sign-in session (the `pms_session` cookie).
- A service token: `Authorization: Bearer <token>`, for scripts and other services that call it during rebuilds.
  - Create one with `python scripts/lrs_token.py new`. It prints the token once, plus its sha256.
  - Append the sha256 to `LRS_SERVICE_TOKENS` (comma-separated) in `.env` locally or `~/pms/env.txt` on mmsdev, then restart.
  - PMS stores only the hash. Remove the hash to revoke the token.
  - Tokens are valid for `/api/lrs/*` only.

Anything else gets `401 {"detail":"Not signed in"}`.

## Request

JSON body:

```json
{
  "locations": [
    {"geometry": {"x": -81.6326, "y": 38.3498}},
    {"geometry": {"x": -80.0, "y": 37.0}}
  ],
  "tolerance": 10
}
```

| Field | Type | Default | Notes |
|---|---|---|---|
| `locations` | list of `{"geometry": {"x": lon, "y": lat}}`, **or the same list as a JSON string** | `[]` | WGS84 (EPSG:4326). A location without a usable geometry finds no route |
| `tolerance` | number, metres | `10` | Search radius around each point; `0 < tolerance ≤ 100` |
| `inSR`, `outSR`, `f` | — | — | Accepted and ignored: input and output are always 4326 JSON |

- **Esri-style form bodies** (`application/x-www-form-urlencoded`, with `locations` as a JSON string) are accepted too.
- **Limits:** at most 10,000 locations per request.
- **Errors:** anything malformed returns `400 {"error":"Bad Request"}`, the same as dashcam.

## Response

One entry per input location, **in input order**, each with up to 10 candidate routes, nearest first:

```json
{"locations":[{"results":[{"geometry":{"x":-81.63257170664752,"y":38.349771125942105,"z":0},"lineDistance":4.046936547442864,"measure":0.3077618288332261,"routeId":"2071025001900"},{"geometry":{"x":-81.63250774879872,"y":38.34984533287769,"z":0},"lineDistance":9.501826056464992,"measure":17.335669305460254,"routeId":"20200600000EB"}],"status":"esriLocatingMultipleLocation"},{"results":[],"status":"esriLocatingCannotFindRoute"}]}
```

| Field | Meaning |
|---|---|
| `status` | `esriLocatingMultipleLocation` when at least one route was found (even exactly one, as dashcam does), otherwise `esriLocatingCannotFindRoute` |
| `results[].routeId` | 13-character LRS route ID (`<county><sign system><number><sub-route><supplemental><direction>`) |
| `results[].measure` | Milepoint on that route, in miles (the M value at the point's closest location) |
| `results[].lineDistance` | Distance from the point to the route, in metres |
| `results[].geometry` | The snapped point on the route, WGS84, with `z` always `0` |

The body is serialised like dashcam's: sorted keys, compact separators, ASCII only, trailing newline. There is no `spatialReference` or `geometryType` key. A NaN is never emitted; a candidate without a finite measure is left out.

**Choosing among candidates** is up to the client. The data pipeline (`pipeline/conflate.py`, `pick_measure`) takes:
1. the record's own route ID,
2. else the route ID with its direction letter stripped, as a prefix,
3. else the nearest route, counted as not located.

## Examples

```sh
# With a service token
curl -s -X POST https://mmsdev.transportation.wv.gov/pms/api/lrs/geometryToMeasure \
  -H "Authorization: Bearer $PMS_LRS_TOKEN" -H "Content-Type: application/json" \
  -d '{"locations":[{"geometry":{"x":-81.6326,"y":38.3498}}],"tolerance":10}'

# Esri-style form body
curl -s -X POST …/api/lrs/geometryToMeasure -H "Authorization: Bearer $PMS_LRS_TOKEN" \
  --data-urlencode 'locations=[{"geometry":{"x":-81.6326,"y":38.3498}}]' --data-urlencode tolerance=10
```

From Python inside PMS, no HTTP is needed:

```python
from lrs.geometry_to_measure import geometry_to_measure
cands = geometry_to_measure([(-81.6326, 38.3498)], tolerance_m=10)   # [[Candidate(route_id, measure, line_distance, x, y), …]]
```

## How it works

Everything runs as one SQL statement per batch of up to 2,000 points, with bound parameters only (`lrs/geometry_to_measure.py`), against `dot12_test.operations.roads2`. That table has one `MULTILINESTRING ZM` per route, SRID 3747 (NAD83(HARN) / UTM 17N, metres), and M in miles. PMS reads it over a read-only connection.

1. Transform each point once to SRID 3747, in a `MATERIALIZED` CTE.
2. Find candidate routes with `geometry && ST_Expand(point, tol)`, which uses the GiST index `idx_roads2_geometry`, then filter with `ST_DWithin(geometry, point, tol)`.
3. For each candidate, take the route's **nearest part** (`ST_Dump`). 2,243 routes have 2–6 parts, with gaps in M between them. On that part:
   - `measure = ST_InterpolatePoint(part, point)`
   - `lineDistance = ST_Distance(part, point)`
   - the snapped point is `ST_ClosestPoint`, transformed back to 4326
4. Rank by distance (then route ID, for a stable order) and keep 10 per point.

**Speed:** about 1.2 ms per point.

**Parity with dashcam:**
- Dashcam's `closest_route_candidates_3747_batch` does the same computation against its own `route_new` table, which holds dominant routes only.
- On 500 random 2025 survey points, both services located the same route for every point, with zero measure difference (`scripts/compare_lrs_dashcam.py`).
- roads2 also contains non-dominant routes, so it can return extra candidates.

**Tests:** `tests/test_lrs_measure.py` covers request parsing, the exact response bytes, NaN refusal and the service-token scope. When roads2 is reachable, it also runs a vertex round trip on the second part of a multi-part route, returning the exact M at 0 m.
