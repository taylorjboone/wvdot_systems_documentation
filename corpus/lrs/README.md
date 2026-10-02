# fuzzyroad

Turns a fuzzy, human description of a West Virginia road location into hard
WVDOT linear-referencing references: **RouteID + milepoint + lat/lng**.

```
$ fuzzyroad resolve "On WV 622 next to the go mart and sissonville high school"

[1] SEGMENT  2030622000000  Kanawha WV 622   confidence 0.93
    street : Sissonville Dr  (KANAWHA)
    begin  MP 13.8654     38.4744486, -81.6717991
      end  MP 13.9400     38.4754685, -81.6710642
    via find_poi [34.63m]: Go Mart, 6302 Sissonville Dr (Mapbox)
    via find_poi [81.31m]: Sissonville High School (OSM node/356537355)
    rejected 2040021000000 (Kanawha CR 21): closest road to the Go Mart at
      17.82 m, but the user explicitly named WV 622
```

## Why it needs an agent

`operations.roads2` is a complete M-aware PostGIS network, so every spatial
primitive is a single SQL query. The geometry is not the hard part. This is:

```
Go Mart (38.47519595, -81.6708709) snapped against roads2:
  2040021000000  Kanawha CR 21     MP  7.9914   17.8 m   <- nearest, WRONG
  2040021080000  Kanawha CR 21/8   MP  0.0041   34.3 m
  2030622000000  Kanawha WV 622    MP 13.9400   34.6 m   <- correct
```

The nearest road is not the answer. The words *"WV 622"* are what pick it, and
no amount of spatial indexing recovers that. So the job is weighing evidence —
which is what the Opus loop does — over a set of deterministic primitives.

## Install

```bash
python3 -m venv .venv && ./.venv/bin/pip install -e .
./.venv/bin/fuzzyroad load          # build the sidecar (~10 s)
./.venv/bin/fuzzyroad api           # HTTP API on http://127.0.0.1:8765
```

`.env` supplies `POSTGRES_*`, `LRS_DB=mms`, `MAPBOX_TOKEN`, `ANTHROPIC_API_KEY`.

## Use

```bash
fuzzyroad resolve "US 60 Cabell"              # the agent
fuzzyroad resolve "..." --trace --json        # show every tool call
fuzzyroad gazetteer "Paint creek fayette county"   # every way of writing it (offline)
fuzzyroad gazetteer "..." --flat              # one search string per line
fuzzyroad api                                 # HTTP API on :8765, docs at /docs
fuzzyroad serve                               # MCP stdio server
fuzzyroad tool snap_point '{"lat":38.4,"lon":-81.6}'   # one primitive, no LLM
fuzzyroad tools                               # list primitives
fuzzyroad eval                                # golden regression set
```

`.mcp.json` registers the server for Claude Code, so Opus can drive the
primitives directly instead of going through `agent.py`.

## HTTP API

`fuzzyroad api` (or `uvicorn fuzzyroad.api:app`) serves everything over HTTP
with OpenAPI docs at `/docs`. Handlers call the same functions the agent and
the MCP server use, so the three surfaces cannot drift.

| Endpoint | Does |
|---|---|
| `GET /gazetteer?q=` · `POST /gazetteer` | Every way of writing the location(s) in the text — see below. Offline. |
| `GET /routes/{routeid}/gazetteer` | The same expansion for one known RouteID. |
| `POST /resolve` `{text, effort, trace}` | The Opus agent. Slow (tens of seconds); needs `ANTHROPIC_API_KEY`. |
| `GET /parse?text=` | Route reference → RouteID digits. |
| `GET /county?text=` | County named in text, with bbox. |
| `GET /routes?q=&county=` | Candidate routes, ranked (structural + lexical). |
| `GET /routes/bbox?min_lat=…` | Routes intersecting a bbox. |
| `GET /routes/{routeid}` | Decoded structure, catalog row, every street name. `?live=true` adds the roads2 row. |
| `GET /routes/{routeid}/point?measure=` | Milepoint → lat/lng. |
| `GET /routes/{routeid}/segment?mp_a=&mp_b=` | Clip between milepoints; GeoJSON. |
| `GET /routes/{routeid}/intersections?cross_name=` or `routeid_b=` | Where two routes meet. |
| `GET /routes/{routeid}/crossings?measure=` | Everything crossing within a window. |
| `GET /routes/{routeid}/describe?measure=` | Reverse context: names, crossings, cached POIs. |
| `GET /streets?name=&county=` | Fuzzy posted-street-name search. |
| `GET /poi?name=&bbox=` | Landmark search (Mapbox + OSM). `bbox=min_lat,min_lon,max_lat,max_lon`. |
| `GET /geocode?text=` | Address → lat/lng. |
| `GET /snap?lat=&lon=` | Coordinate → nearest routes with milepoints. |
| `GET /tools` · `POST /tools/{name}` | The raw primitive surface, by name, with a JSON body. |
| `GET /health` | Sidecar row counts, Postgres reachability, which keys are set. |

Errors are JSON `{"error": ...}`: 404 for an unknown route, 422 for bad
arguments, 503 when Postgres or an API key is missing. CORS is open by default
(`FUZZYROAD_CORS_ORIGINS` to restrict). There is no auth — put it behind
whatever fronts the dot12 app.

```bash
curl 'localhost:8765/gazetteer?q=Paint+creek+fayette+county&limit=1' | jq .search_strings
curl 'localhost:8765/snap?lat=38.4744486&lon=-81.6717991&limit=3'
curl -X POST localhost:8765/resolve -H 'content-type: application/json' \
     -d '{"text": "US 60 Cabell", "effort": "medium"}'
curl -X POST localhost:8765/tools/find_street_name -H 'content-type: application/json' \
     -d '{"name": "Sissonville Dr", "county": "Kanawha"}'
```

## Gazetteer

A FOIA request, a work order and a complaint can all mean Fayette CR 23 and
write it differently. The gazetteer takes the fuzzy description and returns,
per candidate route, every alias the LRS knows how to write, so one search can
cover all of them:

```
$ fuzzyroad gazetteer "Paint creek fayette county" --limit 1
query: Paint creek fayette county
read as: county=FAYETTE (10)  name='Paint creek'

[1] 1040023000000  Fayette CR 23  MP 0.0-8.75  score 98.0
    via street_name:Paint Creek Rd, street_name:PAINT CREEK - PAX
    routeid                  1040023000000
    designation              CR 23 | CO 23 | County Route 23 | CR-23 | CR23 | Co. Rt. 23 | County Road 23 | Secondary Route 23 | Route 23 | Rt 23 ...
    label                    Fayette CR 23 | CR 23 - FAYETTE
    designation_county       CR 23 Fayette | CR 23 Fayette County | Fayette County CR 23 | CR 23, Fayette County, WV | Fayette CO 23 ...
    street_name              Paint Creek Rd | Paint Creek Road | Paint Creek
    street_name_designation  Paint Creek Rd (CR 23) | CR 23 Paint Creek Rd | CR 23 - Paint Creek Rd ...
    street_name_county       Paint Creek Rd, Fayette County | Paint Creek Road in Fayette County ...
    extent                   CR 23 MP 0-8.75 | Paint Creek Rd MP 0-8.75 | Fayette CR 23 MP 0-8.75
    description              PAINT CREEK - PAX
```

It is offline and takes a few milliseconds: candidates come from the sidecar
(structural RouteID match, the 117/118 street-name layer, the roads2 label
catalog), merged and ranked with `routeid.sort_key()`. A route hit by more
than one source is corroborated and moves up. Ambiguity surfaces as multiple
entries — "Paint Creek" alone returns Kanawha CR 83, Fayette CR 23 and four
more, "Route 23 Fayette" returns CR 23, MNS 23 and the CR 23/n side roads.

The response carries `interpretation` (designator, county, leftover name
words), `entries` (one per route: decoded RouteID, label, milepoint extent,
bbox, every street name with `matched` flags, `aliases` tagged by kind, and a
flat `search_strings` list) and a top-level `search_strings` union. Pass
`use_agent=true` to run the Opus resolver first when the text names a
landmark or address; the gazetteer then expands whatever it resolved.

Alias kinds: `routeid` · `designation` · `label` · `designation_county` ·
`street_name` · `street_name_designation` · `street_name_county` ·
`description` (117-layer text such as "PAINT CREEK - PAX") · `extent`.

## Data

| Source | Role |
|---|---|
| `mms.operations.roads2` (Postgres, **read-only**) | The LRS. 98,253 routes, `MultiLineStringZM` in EPSG:3747 where **M is the milepoint in miles**. All geometry maths runs here. |
| `fuzzyroad.sqlite` (built locally) | 120,959 street names from `117/118.csv`, a 98,253-route catalog mirrored from roads2, 421,293 intersection nodes from `intersections.sqlite`, and a growing POI cache. FTS5 + rapidfuzz for name matching. |
| Mapbox Search Box + OSM Overpass + Nominatim | Landmarks and addresses. |

Postgres is never written to — no schema, no extensions, no privileges beyond
the existing `SELECT`.

## The 13 primitives

`parse_route_query` · `resolve_county` · `find_routes` · `find_street_name` ·
`find_poi` · `geocode_address` · `snap_point` · `measure_to_point` ·
`segment_between` · `route_intersection` · `crossings_near` · `routes_in_bbox` ·
`describe_location` — plus `gazetteer`, which expands rather than resolves.

Each returns a **ranked list with scores**, never a bare answer. The agent
combines them; `describe_location` is the self-check — if the user said
"Sissonville Dr" and it reports Sissonville Dr at that milepoint, the route
choice is corroborated by something other than proximity.

## Things the data does that will bite you

These are all handled in `pg.py` and `side.py`, and are why the SQL looks the
way it does:

- **M is not a linear rescale of length.** On WV 61, milepoint 10.0 is at
  fraction 0.3506 of the line, not 10/28.44 = 0.3516. Use `ST_LocateAlong` /
  `ST_InterpolatePoint`; never `ST_LineInterpolatePoint` / `ST_LineLocatePoint`.
- **`ST_ClosestPoint` silently drops the M value.** `ST_InterpolatePoint` is the
  one that reads a milepoint off a line.
- **2,243 routes are multi-part.** `ST_InterpolatePoint` rejects a
  MultiLineString, and `ST_GeometryN(geom,1)` quietly answers from the wrong
  part. Dump to parts, pick the nearest.
- **374 routes have `bmp > 0`.** `ST_LocateAlong` returns an *empty geometry*,
  not an error, outside the M range. Clamp to `[bmp, emp]`.
- **`ST_Force2D` is required for route × route intersection** — the two lines
  carry different M at the same XY, so a 4D intersection finds nothing.
- **Labels lie.** `1030061000000` is structurally FAYETTE WV 61 but is labelled
  `MACCORKLE AVE`; 131 routes have an empty label, 13 say `UNKNOWN`. Match on
  RouteID digits as well as text.
- **Bare route numbers are ambiguous.** "622 in Kanawha" matches 42 routes, 41
  of them CR 622/n side roads. The sign system is the discriminator.
- **Street names are many-to-many.** "Sissonville Dr" is carried by three routes
  across two counties. Ambiguity surfaces as multiple candidates.
- **Names tie constantly, so the tie-break *is* the ranking.** Twenty Kanawha
  streets are named "Greenbrier St" and every one scores 100. Candidates are
  ordered by match score, then `mainline_rank`, then sign system, then how far
  the name runs.
- **Neither POI source is sufficient.** Mapbox found the Sissonville Go Mart and
  OSM did not; OSM found Sissonville High School cleanly and Mapbox returned
  three unrelated "High School Drive" streets. Both are queried and merged.
  (Mapbox's older `geocoding/v5/places` endpoint returns *zero* results for
  "Go Mart" — `search/searchbox/v1/forward` is used instead.)

## Candidate ordering

`routeid.sort_key()` is used by both `find_routes` and `find_street_name`:

1. **match score**
2. **`mainline_rank`** — sub-route, supplemental code and direction are all
   `00` on the through route. Anything else is a derivative of it: a sub-route
   is a different road (`CR 622/17`), a supplemental code is a crossover or
   turn lane, a direction is one carriageway of a dual, extra characters are a
   ramp. When someone names a road they mean the mainline.
3. **sign system** — a signed state route beats a non-state stub of the same name
4. **length** — the longest run of the name

This is what makes `"Greenbrier St"` return `2030114000000` (WV 114, which *is*
Greenbrier Street for 5.99 mi) rather than the 0.027-mile non-state stub that
scores identically, and `"WV 622"` return the 17-mile mainline rather than the
0.006-mile crossover `2030622002500`.

## RouteID grammar

```
2 0 3 0 6 2 2 0 0 0 0 0 0
|-| | |-----| |-| |-| |-----|
 |  |    |     |   |     +--- [11:13] direction  00 | NB | SB | EB | WB
 |  |    |     |   +--------- [9:11]  supplemental code
 |  |    |     +------------- [7:9]   sub-route
 |  |    +------------------- [3:7]   route number, zero-padded to 4
 |  +------------------------ [2:3]   sign system
 +--------------------------- [0:2]   county  01-55, 99 = statewide
```

Sign systems: `0` MNS/Non-State · `1` I · `2` US · `3` WV · `4` CR · `6` PF ·
`7` FANS · `8` HARP · `R` Railroad · `T` Trail · `U` USFS. The last three are
in the data but not in `routeid_prolbem.md`.

## Layout

```
fuzzyroad/
  routeid.py     RouteID grammar: decode, label, free-text parse (+ residual words)
  pg.py          read-only PostGIS against operations.roads2
  side.py        the SQLite sidecar + its loader
  toolspec.py    one schema definition, shared by the agent, MCP and the API
  gazetteer.py   location -> every alias: designations, names, county combos
  agent.py       the Opus loop + system prompt + answer schema
  api.py         FastAPI app: every primitive, the agent, the gazetteer
  server.py      MCP stdio server
  cli.py         fuzzyroad ...
  evalset.py     golden regression cases
  tools/         route · names · geo · lrs · intersect
```
