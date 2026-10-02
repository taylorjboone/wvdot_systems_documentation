# AssetWise fields that drive bridge treatment cost

> **Imported from the inspect_tech repo** (`analysis/BRIDGE_COST_DRIVERS_2026-09-25.md`) on 2026-09-25. File paths and
> commands below are that repo's. In PMS the AssetWise pipeline is
> `python -m pipeline bridges …` (`pipeline/bridges/`), the cost model is
> `scripts/bridges/cost_model/`, the saved API probes are in
> `bridges/analysis_reference/`, and the inventory is `INSPECT_DB`
> (`bridges_all.duckdb`). Other bridge reports: see **Documents → Bridges**.

*Scope: WVDOT-owned bridges (B.CL.01 = S01), 7,261 of 8,719. Coverage figures
are the share of those 7,261 with a usable (non-empty, non-zero) value, measured
against live AssetWise on 2026-09-25 and the 2026-09-24 DuckDB extract.*

## The short answer

With SNBI first and NBI / WV legacy data as the backfill, nearly every WVDOT
bridge has the core quantity drivers a treatment cost needs:

| Driver | Coverage | Where it comes from |
|---|---:|---|
| Deck area | **99.7%** | SNBI B.G.16 (backfill: WV length × width) |
| Number of spans | **99.6%** | WV span text → SNBI B.SP.02 → inventory |
| Number of piers / abutments | **99.5%** | SNBI Substructure data set (backfill: spans − 1, 2 abutments) |
| Span material and design | **99.4%** | SNBI B.SP.04/06 → NBI 43A/43B |
| ADT | **98%** | NBI 29 / inventory |
| Deck type | **87%** | SNBI B.SP.09 → NBI 107 |
| Beam lines | **86.5%** | SNBI B.SP.03 |
| Substructure and foundation type | **85%** | SNBI B.SB.04 / B.SB.06 |
| Length, width, maximum span | **84%** | WV legacy text (NBI-era), SNBI where present |
| Wearing surface | **71%** | NBI 108A → SNBI B.SP.10 |
| Skew | **43%** | NBI 34 |

The SNBI geometry items themselves (B.G.01–B.G.15: lengths, widths, skew,
height) are essentially **empty** in AssetWise (under 1%). Length, width and
span lengths therefore come from WVDOT's own NBI-era text fields, which parse
reliably (see §3).

## 1. Where bridge data lives in AssetWise

Three different structures, and cost modelling needs all three:

| Structure | What it is | How we read it |
|---|---|---|
| **Data types** (repeatable field groups) on the bridge | The bridge's inventory record: SNBI Span, Substructure, Feature, Route, Load Posting and Work Event data sets, WV's legacy OverUnderRow, and WV's **BMS Treatment** set | `POST /api/DataType/GetDataTypeValuesByObjectType/Asset/{dt_id}` — one paged call per data type returns every bridge |
| **Field values** on the bridge and on each inspection | Single fields: NBI items, SNBI items that aren't in a data set (B.G.*, B.C.*), WV fields | `/odata/AssetValues` (bridge) and report values (per inspection) — already in `bridges_all.duckdb` |
| **Structure elements** (AASHTO NBE) under span / pier / abutment segments | Element quantities with condition states: joint ft, bearings, railing ft, paint sq ft, pier columns, girder ft | `/odata/AssetElements`; segment names via `/api/StructureElement/GetSegments/Asset/{as_id}` |

The data types are the part the current extract does **not** pull. They are
the SNBI span and substructure records (86% and 85% of bridges) and give the
pier count directly.

**SNBI vs NBI.** Not every bridge has SNBI data yet. Every feature below is
built SNBI-first with an explicit NBI / WV fallback, and records which source
it used, so a model can learn whether the source matters.

### Data types on this tenant

| dt_id | Data type | Bridges with data | Use |
|---:|---|---:|---|
| 1000 | SNBI Span (B.SP.01–13) | 6,671 | beam lines, span material/type, deck material/type, wearing surface, protective systems, continuity |
| 1001 | SNBI Substructure (B.SB.01–07) | 6,376 | **abutment / pier / wall units**, substructure material/type, foundation type |
| 1002 | SNBI Feature (B.F, B.H, B.N, B.RR) | 5,740 | what's crossed (water / highway / rail), traffic under, clearances, navigation |
| 1003 | SNBI Load Posting | 4,449 | posting status |
| 1004 | SNBI Work Event (B.W.02–03) | 1,984 | **treatment history**: SNBI work code + year |
| 1005 | SNBI Route | 6,801 | route on the bridge |
| 1006 | BMS Treatment (added 9/30/25) | 239 | recommended treatment, year needed, cost (21 bridges) |
| 2 | OverUnderRow (NBI-era) | 831 | legacy NBI 28/29/47/48/49 per over/under record |
| 3–4 | SpanRow / SpanContainer | per inspection | span-by-span number, material, design, length |
| 5 | Maintenance | 0 on bridges | — |
| 6, 8 | Cross section / fixed object columns | 0 on bridges | — |

Not useful for this question: work-management instances, maintenance item
summaries, projects and work specs, and ProjectWise documents all came back
empty for sample bridges. External data views need admin rights.

## 2. Every field worth using, by what it drives

Coverage is WVDOT-owned bridges. "→" is the fallback order.

### Size and quantity (scale the cost)

| Field(s) | Coverage | Drives |
|---|---:|---|
| Deck area: B.G.16 → NBI 49 × NBI 52 → WV length × width × 1.09 | 99.7% | every deck treatment, painting, replacement ($/sf basis) |
| Total length: B.G.02 → NBI 49 → WV "Total Length" | 84.2% | railing, girder length, replacement |
| Width: B.G.05 → NBI 52 / 51 → WV "Roadway Width" | 84.0% | joints, overlays, staging (lanes) |
| Maximum span: B.G.03 → NBI 48 → WV "Span Lengths" | 84.1% | girder depth → paint area, erection method, superstructure replacement |
| Number of spans: B.SP.02 → NBI 45+46 → WV "Span Lengths" → inventory | 99.6% | bearings, joints, mobilisation per span |
| Piers / abutments: B.SB.02 by B.SB.01.1 (P / A) → spans − 1 / 2 | 99.5% | substructure rehab, scour work, bearings |
| Beam lines: B.SP.03 | 86.5% | girder length, bearings, paint area |
| Lanes on structure: NBI 28A | 83% | staging / phased construction |

### Type and material (sets the unit cost and which treatments apply)

| Field(s) | Coverage | Drives |
|---|---:|---|
| Span material: B.SP.04 → NBI 43A | 99.4% | steel → painting applies; concrete → overlays, patching |
| Span design / type: B.SP.06 → NBI 43B | 99.4% | girder vs slab vs truss vs arch vs culvert — biggest unit-cost split |
| Deck material and type: B.SP.09 → NBI 107 | 86.7% | overlay vs replacement options; timber / steel grid decks |
| Wearing surface: NBI 108A → B.SP.10 | 71.4% | overlay removal quantity |
| Deck protection / membrane: NBI 108B/C | 18–51% | overlay prep; epoxy rebar lowers deck risk |
| Span continuity: B.SP.05 | 31% | fewer joints and bearings on continuous spans |
| Span protective system (paint system): B.SP.07 | 39% | lead paint → containment cost for SP6/SP7 |
| Deck reinforcing protection / stay-in-place forms: B.SP.12 / B.SP.13 | 7–15% | deck replacement method |
| Substructure material / type: B.SB.03 / B.SB.04 | 85% | substructure rehab unit cost |
| Foundation type: B.SB.06 | 85% | piles vs spread footing — scour repair and replacement cost |

### Site and access (multipliers on the same quantities)

| Field(s) | Coverage | Drives |
|---|---:|---|
| Feature crossed: B.F.01 (water / highway / rail) | 91% | work over water or traffic: containment, cofferdams, railroad flagging |
| Type of service under: NBI 42B | 83% | same, NBI-era |
| Under-clearances: NBI 54 / 55, B.H.12–15, B.RR.02–03 | 75–83% | access, falsework, rail coordination |
| Skew: NBI 34 | 43% | joint length (skewed joints are longer), formwork |
| ADT and trucks: NBI 29 / B.H.09–10 | 98% | traffic control and phasing |
| Detour length: NBI 19 / B.H.17 | 84% | whether a full closure is possible (much cheaper) |
| Scour critical: NBI 113 | 65% | countermeasures with substructure work |
| Navigation: B.N.01–06 | < 1% | navigation-channel constraints |
| Historical significance: NBI 37 | 83% | historic bridges limit options and cost more |
| District / county | 100% | regional price and access differences |

### Condition (how much of the quantity needs work)

| Field(s) | Coverage | Drives |
|---|---:|---|
| Deck / super / sub / culvert ratings (SNBI B.C.01–04 → NBI 58–62) | ~99% | which treatment, and repair extent |
| Joint / bearing / railing ratings: B.C.05–08 | ~98% of SNBI bridges | joint and bearing replacement need |
| Element condition states (CS3 + CS4 quantities) | 29% (NBE bridges) | **repair quantity directly**: sq ft spalled, ft of joint in poor condition, sq ft of failed paint |
| Work history: B.W.02/03 (SNBI work code + year) | 26% | time since the last overlay / paint; links a treatment code to a year |
| BMS Treatment data set | 3% | WVDOT's own recommendations and cost notes (21 costed) |

## 3. Derived quantities: can we trust them?

### Length, width and spans from WV text

The NBI-era fields "Total Length", "Roadway Width" and "Span Lengths" are free
text (`49'-6"`, `(3)40'-0"`, `One SCBB Span @ 26'-0"`, `38 FT 0 IN`). A parser
recovers width and length on 84% of bridges and a span list on 83%. Checked
against the recorded deck area:

- deck area ÷ (roadway width × total length): median **1.09** (out-to-out
  deck is wider than curb-to-curb roadway), p10–p90 1.01–1.32;
- within ±25% of that ratio for **85%** of bridges, within ±50% for 92%.

### Element quantities from geometry

Element quantities exist only on the 2,093 NBE bridges (29%). For the rest
they must be estimated from geometry. Where both exist:

| Element quantity | Proxy | Median ratio | Within ±25% | log R² |
|---|---|---:|---:|---:|
| Deck element sq ft | deck area | 0.99 | 94% | 0.96 |
| Girder ft | beam lines × length | 0.98 | 90% | 0.82 |
| Wearing surface sq ft | deck area | 0.89 | 91% | 0.92 |
| Railing ft | 2 × length | 1.00 | 68% | 0.86 |
| Bearings (each) | beam lines × 2 × spans | 0.67 | 55% | 0.71 |
| Joint ft | width | 2.35 | 68% | 0.39 |
| Steel coating sq ft (steel spans) | beam lines × length | 11.3 | 47% | 0.57 |
| Pier columns | piers | 2.6 | 65% | 0.32 |

Deck, girder, wearing surface and railing quantities are safe to estimate.
Bearings improve once span continuity (B.SP.05) is used: continuous spans
share bearings. Joints need skew and continuity. Paint area needs girder
depth, estimated from maximum span. Pier columns need pier type (wall vs
column bent, B.SB.04).

## 4. Treatment → the fields that should drive its cost

Treatments are the 13 in the BMS catalogue (`webapp/backend/bms/treatments.py`).

| Treatment | Quantity driver | Unit-cost modifiers | Condition / extent |
|---|---|---|---|
| DK5 Deck seal | deck area | ADT (traffic control), lanes | deck rating |
| DK8 Membrane + HMA overlay | deck area | existing wearing surface (removal), width / lanes (phasing), ADT | deck rating, deck CS3/CS4 sq ft |
| DK4 Rigid (LMC / microsilica) overlay | deck area | deck type, wearing surface, skew, joints (count / length), ADT, detour | deck delamination (CS3/CS4) |
| DK2 Deck renovation | deck area | deck type, span material, beam lines, lanes | deck CS3/CS4 extent |
| DK1 Deck replacement | deck area | span type, beam lines, max span, skew, stay-in-place forms, lanes / detour | deck rating |
| JT1 Joint replacement | joint ft (≈ 2.35 × width; skew, continuity) | joint type (NBE 300–306), ADT | joint rating B.C.08, joint CS |
| SP7 Spot paint | failed coating sq ft (NBE 515 CS3/CS4) | paint system (lead?) B.SP.07, feature crossed (containment), under-clearance | coating condition |
| SP6 Clean and paint | steel coating sq ft (beam lines × length × depth factor) | paint system, feature crossed, under-clearance, rail under | coating condition |
| SP2 Superstructure rehab | girder ft (beam lines × length), bearings | span material/type, continuity, max span | super rating, girder CS |
| SP1 Superstructure replacement | deck area / girder ft | span type, max span, beam lines, spans, feature crossed, lanes / detour | super rating |
| SB2 Substructure rehab | piers + abutments (units), pier type | substructure material/type, foundation, water crossing, scour critical | sub rating, substructure CS |
| CU2 Culvert rehab | culvert length / cells | culvert material/type (B.SP.04/06 or NBI 43) | culvert rating |
| BR1 Structure replacement | deck area | span type, max span, spans, feature crossed (water / rail / highway), foundation, detour, ADT, historic | — |

## 5. Gaps

- **SNBI geometry (B.G.01–15)** is essentially unrecorded; WV text fills
  length, width and span lengths for 84%. The remaining ~16% have deck area
  (99.7%) and span count, but not length or width separately.
- **Skew** is only 43% (NBI 34); treat it as optional with a missing flag.
- **Element quantities** only exist on NBE bridges (29%, mostly NHS). Everything
  else uses the proxies in §3.
- **Paint system** (lead or not) is only 39% (B.SP.07). It is a large cost driver
  for SP6/SP7, so it's worth a field campaign on steel bridges.
- **Work history** is 26% and is mostly recent SNBI-era entries.

## 6. Strategy to test it once cost / material data is available

### Step 1 — Freeze a feature table (build now, no cost data needed)

One row per WVDOT-owned bridge, SNBI-first with fallbacks and a `_src`
column for each feature (as in this analysis):

1. Add the data types to the regular extract: pull data types 1000–1006 (and
   2) with `GetDataTypeValuesByObjectType/Asset/{dt_id}` into a `data_type_value`
   table in `bridges_all.duckdb` during `sync_duckdb.py`.
2. Add the WV text parser (feet-inches, `(n)L`, "n Spans @ L", `FT/IN`) and
   keep the parsed list of span lengths.
3. Add segment names (Span N / Pier N / Abutment N) for NBE bridges from
   `GetSegments`, so element quantities can be split by span and pier.
4. Compute the derived quantities from §3, with a flag for "measured
   (element)" vs "estimated (proxy)".
5. Save the table as `qv_cost_features` with a snapshot date.

### Step 2 — Join the cost / material data

For each past treatment record: bridge (BARS), treatment (map its codes to the
13 BMS treatments, or the SNBI B.W.03 work codes), year, cost or quantities.
Join on BARS to the feature table **as of before the work** (the inspection
before the work year), not today's state: a replaced deck has new geometry
and condition afterwards.

### Step 3 — Two-stage model per treatment

1. **Quantity:** if the data has quantities (sq ft of overlay, ft of joint,
   sq ft of paint), predict quantity from the §4 driver and check against §3.
   This is where AssetWise matters most.
2. **Unit cost:** `log(cost / quantity)` from modifiers (type, material,
   feature crossed, ADT, lanes, detour, skew, district, year for inflation).
   Start with a regularised linear model, where every effect is readable, then
   try gradient boosting and keep it only if it clearly wins.

Total cost = quantity × unit cost. Compare against the current flat $/sf
catalogue (`treatments.py`) as the baseline to beat.

### Step 4 — Validation

- Hold out by **time** (train on older work, test on the latest years) and by
  **district**, not a random split. Otherwise the same contract leaks into both.
- Metrics: median absolute percentage error, share within ±25%, and a
  calibration plot of predicted vs actual by treatment.
- Report per treatment and per structure family; small treatments (e.g. CU2)
  may need to borrow strength from similar ones.
- Ablation: SNBI-only vs SNBI + NBI backfill vs + element quantities. This
  shows how much the backfill and NBE data are worth.
- Check residuals against the `_src` columns. If bridges whose length came from
  WV text are systematically off, the parser or the fallback needs work.

### Step 5 — Feed the BMS

Replace the flat $/sf in the planner with the per-treatment model (quantity ×
unit cost), keeping $/sf as the fallback when a bridge lacks drivers. Show
the source mix and error band next to each estimate on the bridge page.

## Appendix — how the numbers were produced

- Coverage: latest non-empty, non-zero value per bridge per field across the
  bridge record and all inspections (`bridges_all.duckdb`, 2026-09-24 sync),
  plus a live pull of all bridge-level data-type values on 2026-09-25
  (216,000 values).
- Fields that exist but are empty were excluded: B.G.* and NBI 45/46/48/51/52
  have thousands of rows with blank or zero values.
- Proxy checks: `asset_element` total quantities on NBE bridges vs derived
  geometry, WVDOT-owned only.
