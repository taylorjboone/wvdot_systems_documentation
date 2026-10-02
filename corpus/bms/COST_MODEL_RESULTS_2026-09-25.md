# Which bridge attributes predict treatment cost

*Scope: WVDOT-owned bridges (B.CL.01 = S01). Bridge attributes only — no
condition ratings. Treatments are the **BMS treatment catalogue**: each
TheHub construction code maps to the BMS treatment whose `hub_codes` claim
it (`/api/bms/treatments`). Code: `scripts/bridges/cost_model/build_dataset.py`,
`model.py`, `model_text.py`; tables in `results/`.*

## Data

- **TheHub bridge projects:** 2,280 in all — 1,040 completed, 1,103
  active, 137 programmed — covering 1,990 bridges.
- **Used here: 567 completed projects.** Each touched exactly one
  WVDOT-owned bridge, has construction-phase spend, and has a construction
  code the BMS catalogue claims. The primary code is tried first, then any
  other code on the project. Projects under codes no treatment claims (Other
  Bridge Work, Repair Damage, drainage, minor HMA) are left out. 562 remain
  after dropping construction spend under $5,000.
- **Target:** construction-phase (`CN*`) actual spend from OASIS, indexed to
  2026 dollars at 3% a year, modelled as log(cost).
- **Inputs:** 34 AssetWise attributes, SNBI first with NBI / WV backfill (see
  [`dtims_docs/Bridges_Cost_Drivers.md`](../../../dtims_docs/Bridges_Cost_Drivers.md)):
  - size: deck area, length, width, max span, spans, piers, abutments, beam lines
  - structure: family, material, span type, deck type, wearing surface,
    substructure, foundation, continuity, paint system
  - site: feature crossed, service under, skew, NHS, scour, historic, district
  - traffic: ADT, truck ADT, lanes, detour
  - element quantities where recorded (bearings, joint ft, steel coating sf, railing ft)
  - age, cost year

| BMS treatment | TheHub codes | Projects | Median cost | Median $/sf of deck |
|---|---|---:|---:|---:|
| BR1 Structure replacement | 31, 32, 70, 103 | 156 | $1.25M | $689 |
| SP6 Clean and paint | 40 | 155 | $27K | $32 |
| JT1 Joint replacement | 71 | 70 | $52K | $7.6 |
| SP2 Superstructure rehabilitation | 101, 36, 37 | 51 | $1.94M | $222 |
| DK1 Deck replacement | 38 | 48 | $792K | $116 |
| SP1 Superstructure replacement | 73 | 29 | $121K | $105 |
| SB2 Substructure rehabilitation | 74 | 25 | $139K | $76 |
| DK8 Membrane + HMA overlay | 42 | 15 | $879K | $147 |
| DK4 Modified PCC overlay | 46 | 13 | $1.01M | $121 |
| DK2 Deck renovation, CU2 Culvert rehab | 39, 102 | 0 closed single-bridge | — | — |
| DK5 Deck seal, SP7 Spot paint | none mapped | — | — | — |

DK8 and DK4 are too small to model alone; they're included in the pooled model.

## Models

Scored out-of-fold (5-fold cross-validation, repeated 3 times; every model
sees the same folds). **MdAPE** is the median error as a share of actual cost.
**R²** is on log cost.

- **Flat $/sf:** the treatment's median $/sf × deck area, which is the BMS
  catalogue today.
- **Ridge:** a regularised linear model; every effect is readable.
- **Boosted trees:** gradient boosting (HistGradientBoosting); handles missing
  values and categories natively; shallow, heavily regularised trees.
- **+ description:** adds TheHub's project text (see below).

| Scope | n | Flat $/sf | Ridge | Boosted | Boosted + description | Ridge + description | Best R² |
|---|---:|---:|---:|---:|---:|---:|---:|
| **All treatments, pooled** | 562 | 53% | 56% | 49% | **44%** | 53% | **0.82** |
| SP6 Clean and paint | 155 | 33% | 37% | 25% | **23%** | 34% | 0.89 |
| BR1 Structure replacement | 156 | 54% | 43% | 43% | 43% | **42%** | 0.42 |
| JT1 Joint replacement | 70 | 63% | 87% | 77% | **52%** | 77% | 0.38 |
| SP2 Superstructure rehabilitation | 51 | 75% | 71% | 79% | **64%** | 65% | 0.45 |
| DK1 Deck replacement | 48 | 74% | 74% | 78% | 70% | **67%** | 0.44 |
| SB2 Substructure rehabilitation | 25 | **66%** | 82% | 87% | 83% | **66%** | 0.14 |
| SP1 Superstructure replacement | 29 | 73% | 76% | 72% | 72% | 77% | 0.48 (flat) |

**Reading it:**

- **One pooled model is the best single estimator:** typical error 44%,
  R² 0.82 with the description, against 53% for flat $/sf.
- **SP6 Clean and paint** is well explained by bridge size: typical error 23%.
- **BR1 Structure replacement** is moderately predictable (42–43% vs 54% flat).
- **JT1 and SP2 are only predictable with the description.** The code alone
  doesn't say how much work the project is.
- **SB2 and SP1 (25–29 projects) don't beat flat $/sf yet.**

## What predicts cost — bridge attributes

### Pooled model

Permutation importance of the boosted model (drop in R² when shuffled):

| Rank | Attribute | Importance | Coverage |
|---:|---|---:|---:|
| 1 | BMS treatment | 0.67 | 100% |
| 2 | **Deck area** | 0.16 | 99.7% |
| 3 | **ADT** | 0.05 | 98% |
| 4 | **Deck type** | 0.04 | 87% |
| 5 | Total length | 0.01 | 84% |
| 6 | Cost year | 0.01 | 100% |
| 7 | Age | 0.01 | 100% |
| 8 | Steel coating sf (NBE) | 0.01 | 29% |

**Spans and piers are in the model**, filled for every project. They score low
here only because they carry the same information as deck area and length:
across these projects, piers and spans correlate 0.95 with each other and
0.73–0.80 with deck area and length, so the importance measure gives the
credit to deck area. On their own they are strong (next table). For
substructure work they're the attribute the model reaches for.

### Per BMS treatment

Spearman correlation with log cost, significant at p < 0.05:

| BMS treatment | Strongest attributes (ρ) |
|---|---|
| SP6 Clean and paint | length +0.92, deck area +0.91, max span +0.90, truck ADT +0.83, steel coating sf +0.75, railing ft +0.74, ADT +0.73, **spans +0.72**, width +0.71 (**piers +0.71**) |
| BR1 Structure replacement | length +0.50, truck ADT +0.48, deck area +0.44, ADT +0.40, beam lines −0.32, **piers +0.31**, max span +0.31, **spans +0.30**, age +0.27 |
| JT1 Joint replacement | **width +0.65**, ADT +0.61, beam lines +0.53, truck ADT +0.49, lanes +0.43, deck area +0.39, spans +0.26 |
| SP2 Superstructure rehabilitation | steel coating sf +0.71, deck area +0.66, railing ft +0.61, length +0.60, max span +0.55, ADT +0.45, width +0.41, **piers +0.39** |
| DK1 Deck replacement | deck area +0.68, length +0.64, **piers +0.58**, ADT +0.56, steel coating sf +0.53, width +0.52, max span +0.46, **spans +0.45** |
| SP1 Superstructure replacement | **width +0.75, lanes +0.72**, deck area +0.61, **piers +0.58, spans +0.55**, ADT +0.54, length +0.54 |
| SB2 Substructure rehabilitation | deck area +0.56, width +0.52, cost year +0.46, **piers +0.44**, length +0.42, **spans +0.41** |
| DK8 Membrane + HMA overlay (15) | age +0.58 |

Boosted-model importances where there's enough data:

- **SP6:** deck area, then max span (girder depth → paint area).
- **BR1:** deck type, deck area, ADT, length, age, beam lines.
- **SP2:** deck area, max span, length, bearings.
- **DK1:** deck area, steel coating area, deck interaction, max span, piers.

## What the project description adds

TheHub's Scope field is filled on every project. It starts "Work Type: …",
e.g. "PAINT REPLACE, DECK REPLACE, SUBSTRUCTURE REHAB". It's combined with the
name, the STIP type of work and the phase descriptions (89%). Comments are
excluded because they're written after the fact. The text goes in as work-type
flags, the **number of work items** on the Work Type line (1 for 59% of
projects, 2 for 26%, 3+ for 7%), and word patterns (TF-IDF), all fitted inside
each training fold.

- **It separates scope within a treatment code.**
  - JT1 goes from R² ≈ 0 to 0.38 (typical error 77% → 52%).
  - SP2 goes from 0.17 to 0.45 (79% → 64%).
  - For both, shuffling the description costs more R² than shuffling bridge
    size: 0.82 vs 0.01 for JT1, and 0.52 vs 0.17 for SP2.
- **More work items, more cost.** Replacement, deck, rehab and overlay
  wording pushes cost up. Joints-only, scour-only and culvert wording
  pushes it down.
- **Contract type shows through:** "DBE" (a federal-aid contract requirement)
  and "right of way" mark the larger contracted projects.
- **It barely changes SP6 and BR1**, where size already explains cost.

## More NBI / SNBI fields (screen)

`nbi_screen.py` added every other NBI / SNBI item that has a value for at least
40% of the project bridges. Zeros count, because 0 is a real code for many NBI
items (no median, not flared, not STRAHNET). Excluded: condition, appraisal,
posting, inspection-admin, identifiers, location, dates and work
recommendations. **36 new fields** were compared on identical folds:
clearances (NBI 47, 54A, 55A/B), route (NBI 26, 42A, 100, 102, 110, 19,
B.RT.03), layout (NBI 33, 35, 38, 101, B.SP.01, B.SP.13), a second
substructure configuration (B.SB.01–07), safety features (NBI 36A–D),
membrane (108B), and critical features (NBI 92A–C).

| Scope | Boosted, base 34: MdAPE / R² | Boosted, + 36 NBI/SNBI: MdAPE / R² |
|---|---:|---:|
| All treatments, pooled | 49% / 0.76 | 50% / 0.76 |
| BR1 | 43% / 0.34 | 45% / 0.35 |
| SP6 | 25% / 0.87 | 27% / 0.88 |
| DK1 | 78% / 0.28 | 73% / 0.29 |
| SB2 | 87% / 0.12 | 64% / 0.29 |
| JT1, SP1, SP2 | no change | no change |

- **No overall gain.** None of the 36 reaches 0.005 importance in the pooled
  model, whose top ranks are unchanged.
- **Small, plausible per-treatment effects:**
  - NBI 47 horizontal clearance for SB2 (roadway width again, n = 25, fragile);
  - B.SP.13 stay-in-place forms for DK1 (deck forming);
  - B.SP.13, the NBI 19 bypass and NBI 36A railings for BR1, each ~0.01.
- **Bottom line:** once treatment, size, traffic and deck type are in, the rest
  of the NBI / SNBI record carries no further cost information.

**Height above ground isn't in AssetWise.** SNBI B.G.13 Maximum Bridge Height
is empty, and the NBI 54B under-clearance value is mostly zeros. It would have
to come from terrain: a USGS 3DEP DEM, taking the relief under and around each
bridge (deck elevation minus the lowest ground within ~100 m). That's the most
promising attribute not yet tested, since high bridges need falsework and
cranes.

## Every NBI / SNBI field, evaluated (`nbi_full_screen.py`)

**The full dictionary was checked.** 596 NBI / SNBI fields have at least one
value on the 536 project bridges. Every one has a disposition in
`results/nbi_snbi_disposition.csv`:

| Disposition | Fields |
|---|---:|
| In the base model | 32 |
| **Tested in this screen** | **67** (+5 derived) |
| Too sparse (< 3% of project bridges) | 214 |
| Inspection administration (B.IE, NBI 63/65/90/91, 92 dates) | 93 |
| Load capacity / posting (NBI 41, 70, B.PS, B.EP) | 49 |
| Route / LRS ids, feature names | 36 |
| Second/third instances or constants | 31 |
| Identifiers, location, constants | 20 |
| Condition (B.C, B.AP, NBI 58–62, 67) | 20 |
| Years (age is already in) | 10 |
| Other: sparse repeats, raw work history (used as derived features) | 23 |

**Height / elevation: nothing to test.**

- SNBI B.G.01–B.G.15 are empty, including B.G.13 Maximum Bridge Height; only
  B.G.16 deck area is filled.
- The NBI 10 and 53 clearances store only the inches part.
- The NBI 54B under-clearance height isn't stored.
- The nearest proxies were tested: B.H.13 vertical clearance to the road
  underneath (12%), B.H.16 surface width of the road under (25%), B.H.09 ADT
  under (39%), and latitude/longitude.

**Method.** Out-of-fold residuals of the pooled model (treatment + 34
attributes) are the cost it can't explain. Each candidate was tested against
them: Spearman ρ for numbers, Kruskal–Wallis and η² for codes. The test was
run pooled and within BR1 and SP6, with Benjamini–Hochberg correction across
all candidates.

**Tested:**

- the second-screen fields (clearances, route class, layout, substructure and
  foundation configurations, safety features, membrane, critical features);
- route prefix / level of service / base network (NBI 5B, 5C, 12);
- truck % (109);
- the geometric appraisals NBI 68 (deck geometry), 69 (under-clearances),
  71 (waterway adequacy) and 72 (approach alignment);
- recommended work type and contract vs state forces (75A / 75B);
- the inspector's cost estimates (94 / 96);
- the road-under items (B.H.09, 13, 14, 15, 16), urban code, freight network;
- deck and reinforcing protective systems (B.SP.11 / 12);
- second / third span and substructure configurations;
- inspection intervals;
- prior work events and years since the last (before the project only);
- number of features crossed, latitude, longitude.

**Result:**

- **Pooled: no field is significant after correction.** The best is the SNBI
  detour length, q = 0.27. Adding the fields that pass anywhere leaves the
  pooled model unchanged (MdAPE 49.2% → 49.1%, R² 0.763 → 0.762).
- **Within one treatment (q < 0.10), plausible but not enough to improve its
  model:**
  - **SP6 Clean and paint:** fracture-critical bridges (NBI 92A, η² 0.07) and
    number of features crossed (ρ +0.31) cost more than size predicts —
    trusses and two-girder bridges have more steel and harder access; crossing
    road and water means more containment. Added to the SP6 model: 25% → 26%
    typical error.
  - **BR1 Structure replacement:** SNBI detour length (ρ −0.51). A short
    detour means dearer per sq ft: median $1,436/sf at ≤ 2 km (4 projects) vs
    $497/sf beyond 30 km — likely urban vs rural. It's filled for only 45
    replacements; the model gain is mixed (ridge 43% → 41%, boosted
    43% → 47%).

**Conclusion:** after treatment, size (deck area, length, width, spans,
piers), traffic (ADT) and deck type, nothing else in the NBI / SNBI record
predicts construction cost. The remaining cost differences come from scope,
which the project description captures, and from data AssetWise doesn't hold:
height above ground, site access, contract details.

## Cover photos (`fetch_cover_photos.py`, `photo_features.py`, `model_photo.py`)

**Photos:** for each project, the cover photo from the last inspection
**before** the project started (a later photo would show the new bridge),
walking back up to 4 inspections. **473 of 562 projects** have one; 85 have
no inspection before their start in the extract, and 4 have no cover photo.
The photos are elevation views showing the structure, what's under it and
the setting.

**Features:** CLIP ViT-B-32 (LAION-2B weights), in two forms:

- a 512-number image embedding, compressed to 10 components inside each
  training fold;
- 22 readable scores: height / what's under (low over a creek, tall over a
  valley, over a road, long over a river), setting (rural / town /
  interstate), crossing, structure type, size, and surface (rusty / clean /
  concrete).

The top labels skew as expected for WV: 340 "low", 310 "rural", 208 over a
river. Structure type is rough — many girder bridges are labelled "slab" — so
the scores are signals, not truth.

**Results** (boosted trees, the 473 projects with a photo; the base is
slightly worse than on all 562 because only 85 of 156 BR1 projects have a
pre-project photo):

| Scope | Base | + photo scores | + photo embedding | + both photo | + description | + photo + description |
|---|---:|---:|---:|---:|---:|---:|
| **Pooled** MdAPE | 54.0% | 52.6% | 55.6% | 54.0% | **47.9%** | 50.4% |
| **Pooled** R² (log) | 0.755 | 0.750 | 0.748 | 0.746 | **0.801** | 0.797 |
| BR1 MdAPE (85) | 52.5% | 54.4% | 51.3% | 59.8% | **48.8%** | 56.4% |
| SP6 MdAPE (154) | 26.7% | 28.0% | 29.0% | 29.6% | **24.7%** | 27.1% |
| JT1 MdAPE (70) | 77.3% | 81.0% | 86.3% | 81.5% | **52.5%** | 53.7% |
| DK1 R² (42) | 0.36 | **0.42** | 0.33 | 0.40 | 0.49 | 0.43 |

- **Photos don't improve cost prediction.** The pooled change is within noise
  (MdAPE −1.4 points with the readable scores, but R² slightly down). The
  embedding over-fits at this sample size. Per treatment it's mostly slightly
  worse; the exception is DK1, where the readable scores add a little.
- **The one readable signal is setting.** Against the cost the attributes
  can't explain, "rural" scores go with cheaper projects (ρ −0.14, q = 0.048)
  and "interstate" with dearer ones (ρ +0.13, q = 0.064). That's traffic
  control and staging, and ADT already carries most of it.
- **Height doesn't come through.** Almost no photo scores highest for "tall
  over a valley": these are mostly low creek crossings, and a side elevation
  view doesn't show height reliably. Height would need terrain data, not
  photos.
- **The project description remains the one addition that clearly helps**
  (pooled 54.0% → 47.9%, and JT1 77% → 53%).

## Every field in, and an LSTM (`all_fields.py`, `lstm_model.py`)

**Every field:** all 230 usable AssetWise fields (NBI, SNBI and WV; 38
numeric, 192 coded, a median of 104 per project), taken from the last
inspection before the project. Condition, capacity / posting,
inspection-admin, dates, IDs and narratives are excluded.

**LSTM:** a bridge record has no natural order, so it's read like a sentence
of "field = value" tokens:

- the sequence: treatment, cost year, the derived attributes, then every
  field (numbers as decile tokens), plus description words in the
  "+ description" variant — about 115 tokens, or 137 with the description;
- the network: embedding → bidirectional LSTM → mean + max pooling → cost;
- training: Huber loss, dropout, 10% token dropout, early stopping, 3 seeds
  per fold.

It's compared with boosted trees given the same fields as a wide table, on the
same 15 folds as every other model (562 projects, run in parallel on 14 cores).

| Model | MdAPE | R² (log) | Within ±25% | Within ±50% |
|---|---:|---:|---:|---:|
| Boosted trees, base 34 attributes | 49.2% | 0.763 | 27.3% | 50.5% |
| Boosted trees, all 230 fields | 49.0% | 0.755 | 27.4% | 50.9% |
| LSTM, all fields | 56.1% | 0.710 | 23.9% | 45.3% |
| **Boosted trees, all fields + description** | **43.5%** | 0.813 | 31.1% | **55.6%** |
| LSTM, all fields + description | 46.8% | 0.800 | 27.5% | 52.9% |
| Blend of the two "+ description" models | 44.3% | **0.832** | **31.4%** | 55.0% |

- **The LSTM loses to boosted trees on the same inputs:** 56% vs 49% on fields
  alone, and 47% vs 44% with the description. With 562 projects it can't learn
  good representations for ~3,000 field-value tokens. That's the expected
  result for small tabular data.
- **All 230 fields add nothing over the 34 attributes** (49.2% → 49.0%, R²
  slightly down). This confirms the field screens: the rest of the record
  carries no cost information.
- **Blending adds a little robustness.** The blend has the best R² (0.832)
  and within-±25% share, so fewer large misses, but its median error is
  slightly worse than the trees alone. The LSTM mostly re-learns what the
  trees know.
- **The description is still the lever:** 5–9 points off either model.

**Recommendation unchanged:** boosted trees with treatment, the core
attributes and the project description. An LSTM, or any deep model, is only
worth revisiting with several thousand projects, e.g. multi-bridge projects
split by deck area, or several more years of closed work.

## Multimodal: attributes + photo vector + description vector (`desc_embeddings.py`, `fusion_model.py`)

**Inputs, as raw embedding vectors:**

- **photo:** the pre-project cover photo's CLIP ViT-B-32 image embedding (512);
- **description:** the TheHub text (name, Scope / Work Type, STIP work, phase
  descriptions) embedded by `BAAI/bge-large-en-v1.5` (1,024), run locally so
  project text never leaves the machine;
- **attributes:** the 34 attributes + treatment + cost year as tokens through
  a BiLSTM.

Each branch has its own dense layer; the branches are fused and trained end to
end. The comparison uses 473 projects (those with a photo), the same 15 folds
throughout, with boosted-tree references (vectors compressed by PCA inside
each fold). The run took 102 s on 14 cores.

| Model | MdAPE | R² (log) | Within ±50% |
|---|---:|---:|---:|
| Boosted trees: attributes | 54.0% | 0.755 | 46.9% |
| **Boosted trees: attributes + description TF-IDF** | **47.9%** | **0.801** | **51.4%** |
| Boosted trees: attributes + description vector | 49.7% | 0.783 | 50.4% |
| Boosted trees: attributes + photo + description vectors | 52.9% | 0.779 | 47.6% |
| LSTM: attributes | 55.5% | 0.728 | 45.5% |
| Photo vector only | 91.3% | 0.201 | 19.1% |
| Description vector only | 58.4% | 0.697 | 42.6% |
| LSTM + photo | 57.1% | 0.720 | 43.4% |
| LSTM + description vector | 51.5% | 0.787 | 48.6% |
| LSTM + photo + description vectors (full fusion) | 52.6% | 0.786 | 48.0% |

- **The description vector carries real cost information.** On its own it's
  nearly as good as all the bridge attributes (R² 0.70 vs 0.73–0.76). Added
  to the LSTM it takes 4 points off (55.5% → 51.5%), and added to the trees
  4.3 points (54.0% → 49.7%).
- **But the plain word counts (TF-IDF) still beat the dense vector**
  (47.9% vs 49.7%). A sentence embedding blurs the specifics that set cost:
  "REPL EXP DAMS" vs "REPL BR", and the dimensions some scopes carry
  ("80.5 X 181.7 SSPG"). The counts keep those exact tokens.
- **The photo vector hurts every combination** it's added to (full fusion
  52.6% vs 51.5% without it; trees 52.9% vs 49.7%). On its own it's close to
  no information (R² 0.20).
- **Best model overall is unchanged:** boosted trees with the attributes and
  the description as word counts. A combined description input (word counts
  + vector) is the only variant still worth trying.

## Conclusions

1. **Size drives cost.** Deck area (99.7% coverage) comes first for every
   treatment. Length, width, spans and piers add the shape:
   - width for work across the deck (JT1, SP1);
   - piers for substructure and deck work (SB2, DK1).
2. **Traffic comes second:** ADT and truck ADT (traffic control and phasing,
   and route class).
3. **Type matters mainly for BR1**, through deck type and structure.
4. **The project's scope, from its description, is the third driver** for
   joints and superstructure rehab.
5. **For the BMS:**
   - Replace flat $/sf with the pooled model (BMS treatment + deck area +
     ADT + deck type + length). Add the Work Type list and its item count when
     a project has a scope.
   - Keep flat $/sf as the fallback for SB2, SP1, DK4 and DK8 until more
     projects close.

## Caveats

- **Costs are OASIS construction-phase actuals.** They include anything
  charged to the project, so some SP6 and SP1 costs are very low (medians
  $27K and $121K): likely state-force or partly charged jobs. A scope check
  on the cheapest 10% of each treatment is worth doing.
- **Geometry is the bridge as recorded today.** For BR1 that's the new
  bridge, which is what the money bought.
- **Beam lines correlate negatively with BR1 cost (ρ −0.32).** More beam lines
  usually means a slab or box-beam bridge, which is cheaper per deck foot. Read
  it through structure type.
- **Description words that are places** (e.g. "raleigh") pick up location,
  not cause. Phase descriptions can be edited during construction, so there's
  a small leak.
- **The validation split is random, not by time or district.** With 25–156
  projects per treatment, a time split isn't possible yet.
