# NBI Ratings in West Virginia — Comprehensive Analysis

A quantitative analysis of 9,979 WV bridges × 34 years of NBI ratings, with notes on what the data is — and isn't — built to do. The NBI was originally designed as a triage system, and that lineage shapes how the data behaves; we touch on the implications for BMS-style use where relevant rather than dwelling on them.

**Data**: 9,979 bridges × 34 annual snapshots (1992–2025) = **260,954 inspection records**, plus 7,698 metadata records with inspector narratives.

**Artefacts in this directory** (see Section 11 for the full table):
- `analysis.py`, `text_analysis.py` — modeling pipelines
- `model_results.json`, `text_results.json` — raw metrics
- `REPORT.md` — this document (supersedes the earlier standalone `nbi_system_summary.md`)

---

## Table of contents

- [TL;DR (headline findings)](#tldr-headline-findings)
- [1. The data](#1-the-data)
- [2. What NBI ratings actually are](#2-what-nbi-ratings-actually-are)
  - [2.1 Composition of the rating system](#21-composition-of-the-rating-system)
  - [2.2 What inspectors actually record but doesn't get submitted to NBI](#22-what-inspectors-actually-record-but-doesnt-get-submitted-to-nbi)
  - [2.3 Element-level (AASHTO MBEI / SNBI) — the quantitative half that does get submitted](#23-element-level-aashto-mbei--snbi--the-quantitative-half-that-does-get-submitted)
  - [2.4 Photos and emerging instrumentation](#24-photos-and-emerging-instrumentation)
- [3. Temporal trends 1992–2025](#3-temporal-trends-19922025)
- [4. Noise / variability](#4-noise--variability)
  - [4.1 Year-to-year transition distribution](#41-year-to-year-transition-distribution)
  - [4.2 Inspector-noise fingerprint (within-panel)](#42-inspector-noise-fingerprint-within-panel)
  - [4.3 Intervention/rehab events](#43-interventionrehab-events)
  - [4.4 Deterioration rate by age](#44-deterioration-rate-by-age-deck-excluding-rehab-jumps)
  - [4.5 Inter-rater noise — published evidence](#45-inter-rater-noise--published-evidence)
- [5. Gameability of the system](#5-gameability-of-the-system)
- [6. Predictive modeling](#6-predictive-modeling)
  - [Task A — predict the next inspection's rating](#task-a--predict-the-next-inspections-component-rating-regression)
  - [Task B — P(drop to SD next inspection)](#task-b--pcomponent-drops-to-sd-4-next-inspection--currently-5)
  - [Task C — P(drop ≥2 points)](#task-c--prating-drops-2-points-next-inspection)
  - [Task D — 3-class same/down/up](#task-d--3-class-samedownup-next-inspection)
  - [6.1 Feature importances](#61-feature-importances-superstructure--sd-drop-gbm)
- [7. How predictable is the system, really?](#7-how-predictable-is-the-system-really)
- [8. Inspector narratives — TF-IDF text models](#8-inspector-narratives--tf-idf-text-models)
  - [8.1 Coverage](#81-coverage)
  - [8.2 Four experiments](#82-four-experiments-7525-stratified-split-seed-42)
  - [8.3 Caveat — partial tautology](#83-caveat--partial-tautology)
  - [8.4 Top weighted terms](#84-top-weighted-terms-lexicon--numeric-model-3e)
  - [8.5 Top words ranking SD vs not-SD](#85-top-words-ranking-sd-vs-not-sd-tf-idf-experiment-1)
  - [8.6 Implications for forecasting (BMS use)](#86-implications-for-forecasting-bms-use)
- [9. Context: what NBI was designed for, and how it maps to BMS use](#9-context-what-nbi-was-designed-for-and-how-it-maps-to-bms-use)
  - [9.1 Origin: Silver Bridge, 1967](#91-origin-silver-bridge-1967)
  - [9.2 Scale and federalism](#92-scale-and-federalism)
  - [9.3 What the system does well](#93-what-the-system-does-well)
  - [9.4 Where BMS use benefits from additional layers](#94-where-bms-use-benefits-from-additional-layers)
  - [9.5 What our analysis adds](#95-what-our-analysis-adds)
  - [9.6 Summary](#96-summary)
- [10. Recommendations](#10-recommendations)
- [11. Files in this directory](#11-files-in-this-directory)

---

## TL;DR (headline findings)

1. **The data is very stationary year-to-year.** ~91% of consecutive inspections report the same rating; only ~7% drop by 1; only ~1% drop by 2+. Predicting *next year's rating* is dominated by a trivial "same as last year" baseline.
2. **Inspector noise on the WV panel is real but small.** "Reversal" events (down-then-up across 3 inspections — a fingerprint of subjective inspector disagreement) occur in only ~0.1% of bridge-year triples. Most observed drops are signal, not noise. *Caveat:* the FHWA 2001 inter-rater study (Section 4.5) shows much higher between-inspector variance; the WV panel mostly tracks *same-inspector* drift.
3. **There is a clear methodology shift around 2015–2018.** Mean deck rating fell from 6.64 to 5.97 in four years; SD share jumped from 12.8% to 21.3%. This is the FHWA SNBI / coding-rule transition, not deterioration. Any model crossing 2017–2018 must control for it.
4. **The next-year rating is *not* meaningfully predictable beyond persistence.** GBM cannot beat "predict same as last year" on 1-year MAE.
5. **The interesting prediction is "will this Fair-rated bridge drop to Poor?"** Base rate ~1%/yr; GBM AUC ≈ 0.82, AP ≈ 0.04. Useful as a top-N watch list, not as an alarm.
6. **Dominant predictive features:** lag-1 component rating, age, year, cross-component ratings, ADT, load capacity. Owner / district / NHS add little.
7. **Inspector narratives are extraordinarily predictive.** TF-IDF + L2 logistic reaches AUC 0.96–0.98 for SD classification. A 50-word severity lexicon alone reaches AUC 0.94. The *previous-cycle* narrative predicts current SD at AUC 0.981.
8. **The NBI's heritage matters.** ~70–80% of the "condition" content is discretionary 0–9 codes — a design choice rooted in the system's 1971 triage origins. Element-level SNBI data + narrative + photos round it out for BMS-style use.

---

## 1. The data

| File | Records | What it is |
|---|---:|---|
| `nbi_history.json` | 9,979 bridges × 26 median yearly snapshots = **260,954 rows** | Compact NBI codes; longitudinal spine |
| `bridges_data.json` | 7,698 bridges | Latest snapshot + rich free-text inspector narratives (incl. `_prev`) |

Key fields in the history: `deck`, `superstructure`, `substructure`, `culvert`, `channel`, `scour` (all 0–9); `sufficiency` (0–100); `adt`, `operating_rating`, `inventory_rating`, `status` (A/P/K/…), `inspect_date`, `year_built`, `year_reconstructed`, `structure_kind`, `structure_type`.

Population: ~92% state-owned, ~16% on the National Highway System. Build-decade peak: **1970s–1990s** (~3,800 bridges). Median **effective age** (using `max(year_built, year_reconstructed)`): **44 years**.

---

## 2. What NBI ratings actually are

Before modeling, it's worth being honest about what's *in* the input data. The condition portion of NBI — the part that determines SD classification, posting decisions, and federal funding — is dominantly **qualitative inspector judgment encoded as a digit**.

### 2.1 Composition of the rating system

**Pure inspector judgment (0–9, no measurement thresholds in the FHWA *Recording and Coding Guide*):**

| Item | Component |
|---|---|
| 58 | Deck |
| 59 | Superstructure |
| 60 | Substructure |
| 61 | Channel / channel protection |
| 62 | Culvert |
| 113 | Scour critical |

A "5" vs a "4" on items 58/59/60/62 is the difference between *Fair* and *Poor* (formerly Structurally Deficient). That threshold gates federal funding, posting decisions, and political optics — and it sits entirely inside one inspector's head.

**Hybrid appraisal ratings (0–9, compared to current AASHTO standards):** items 67, 68, 69, 71, 72. Inputs are measured geometry; the output code is still discretionary.

**Calculated / formula-driven:**
- **Sufficiency Rating (0–100)** — looks quantitative, but its largest input (S1, up to 55 pts) is built directly from the qualitative condition codes above. **Treat as endogenous, not as ground truth.**
- **Operating / Inventory Load Rating** (items 64, 66) — output of LFR/LRFR per AASHTO MBE. Uses measured section properties, but also a condition factor and assumption choices the engineer picks.

**Truly hard numbers:** structure length, deck width, vertical/horizontal clearance, year built, year reconstructed, ADT, skew, number of spans, material/design code, district, owner.

**Approximate split for "condition" questions:**
- **70–80% qualitative** (the four 0–9 condition codes)
- **15–20% hybrid** (appraisal + load rating)
- **5–10% truly hard** (geometry, age, ADT)

For *inventory* questions ("how long? how wide? when built?") it flips — those are nearly all hard numbers. For *condition* questions ("how bad is it? when will it fail?") the data is mostly subjective.

### 2.2 What inspectors actually record but doesn't get submitted to NBI

Quantitative data **does** exist — most of it just doesn't get federated up to the NBI. It lives in the state DOT's bridge file (NBIS 23 CFR 650.313 requires retention):

- **Steel section loss** — UT thickness gauges, calipers; inches or % loss.
- **Concrete spall / delamination / patched area** — chain-drag, hammer sounding; sq ft or % of element.
- **Crack widths** — comparator card / feeler gauges; lengths measured.
- **Scour soundings** — sounding rod, weighted tape, single-beam sonar; cross-sections compared year over year.
- **Pier plumb / tilt / settlement** — surveyed against benchmarks where available.
- **Joint openings** — with ambient temperature recorded for normalisation.
- **Bearing displacement and rotation** — against reference marks.
- **Concrete cover / rebar location** — pachometer / GPR (in-depth inspections).
- **Coating condition** — % area in each SSPC class.

The inspector takes all of this and **picks a single 0–9 code**. The qualitative rating is a lossy summary — analog-to-digital conversion that throws away most of the underlying numbers. The richer information exists; it just doesn't get federated.

### 2.3 Element-level (AASHTO MBEI / SNBI) — the quantitative half that *does* get submitted

Since ~2013 nationally, and required across all bridges under the SNBI rollout (2022–2024 phased), each element is quantified by condition state:

```
Element 12 Reinforced Concrete Deck — Total qty: 8,400 sq ft
  CS1 (Good):    7,200 sq ft
  CS2 (Fair):    1,100 sq ft
  CS3 (Poor):      100 sq ft
  CS4 (Severe):      0 sq ft
```

This is the most quantitative thing inspectors record at the federal level. Still inspector-observed (not instrumented), but quantities rather than a single digit. BMS workflows generally lean on this layer more than on items 58/59/60. The element-level data is *not* in the provided WV panel.

### 2.4 Photos and emerging instrumentation

- **Photos** are required in the bridge file under the 2022 NBIS final rule. BIRM specifies coverage (each elevation, deck surface, each span underside, each pier/abutment face, bearings, joints, documented defects). They are **not federally required to be repeatable** from year to year — no fixed photo stations, no standard focal length, no required angle. State DOTs can mandate this; some do (PennDOT, NYSDOT, MnDOT), most don't.
- **UAS / drone inspections** with georeferenced waypoints — repeatable photo points. Programs at MnDOT, FDOT, Caltrans, GDOT.
- **Photogrammetry / lidar / structured-light scans** — dimensioned 3D models. Quantitative, repeatable, expensive.
- **Permanent crack monitors** (Avongard-style gauges) — read each cycle.
- **Vibrating-wire strain gauges / structural health monitoring** — only on signature spans.

---

## 3. Temporal trends 1992–2025

```
year      n     deck   super   sub   scour   suff    SD%    posted%  closed%
1992    6732    6.37   6.16   6.26   6.25   5.37   25.2%   14.7%    2.2%
2000    7045    6.56   6.46   6.54   7.13   5.91   17.0%    7.8%    1.5%
2010    7028    6.64   6.57   6.64   7.77   6.13   13.8%    9.5%    0.4%
2013    7087    6.66   6.61   6.67   7.80   6.19   12.7%    9.1%    0.4%   ← floor
2015    7167    6.55   6.48   6.52   7.83   6.06   14.7%   10.1%    0.4%
2017    7179    6.18   6.15   6.14   7.84   5.74   18.7%   10.9%    0.3%   ← cliff
2018    7221    6.06   6.05   6.05   7.85   5.65   19.9%   11.6%    0.3%
2020    7228    5.93   5.94   5.96   7.84   5.57   21.3%   12.1%    0.4%
2023    7254    5.95   5.97   5.98   7.59   5.57   19.7%   12.1%    0.5%
2025    7275    6.08   6.11   6.12   7.47   5.66   17.7%   12.2%    0.4%
```

**Three regimes:**

1. **1992–2013: gradual improvement.** Mean deck climbs 6.37 → 6.66; SD share halves from 25% to 13%. Posted share falls 14.7% → 9.1%. Post-Silver-Bridge-era public investment story.
2. **2015–2018: methodology cliff.** Mean deck/super/sub all drop ~0.6 points in 4 years. SD share jumps 12.7% → 19.9%. Scour did *not* move (already on its modernised scale). This coincides with the FHWA's MAP-21 recoding requirements and WV's transition toward SNBI element-level inspection. **It is not deterioration.**
3. **2020–2025: post-recalibration plateau** with mild improvement (mean deck 5.93 → 6.08; SD share 21% → 18%).

**Implication for modeling**: a year covariate or explicit pre-2018/post-2018 split is essential. Training a deterioration model across this boundary without controls will produce inflated deterioration coefficients. The shift also matters for longitudinal BMS reporting — KPIs anchored on the rating definition before 2015 are not directly comparable to those after 2018.

Side note: the `scour` rating climbs almost monotonically 1992 → 2014 (6.25 → 7.83). That's the FHWA's scour evaluation program rolling out, not bridges getting safer.

---

## 4. Noise / variability

### 4.1 Year-to-year transition distribution

For each pair of consecutive non-null observations on the same bridge:

| Component | n pairs | Same | Drop 1 | Drop ≥2 | Up 1 | Up ≥2 | mean &#124;Δ&#124; | Var(Δ) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| deck | 180,069 | **90.2%** | 6.3% | 1.3% | 1.3% | 0.8% | 0.13 | 0.24 |
| superstructure | 194,852 | **91.2%** | 5.8% | 1.0% | 1.4% | 0.6% | 0.11 | 0.19 |
| substructure | 193,402 | **91.6%** | 5.3% | 1.0% | 1.5% | 0.6% | 0.11 | 0.17 |
| culvert | 15,443 | 94.3% | 3.8% | 0.8% | 0.9% | 0.2% | 0.07 | 0.09 |
| scour | 195,361 | 96.6% | 0.2% | 0.9% | 0.2% | 2.1% | 0.08 | 0.21 |

The standard deviation of one-year change is **0.41–0.49 points** for deck/super/sub. Persistence ("predict same") is therefore an extremely strong baseline.

### 4.2 Inspector-noise fingerprint (within-panel)

A natural signature of subjective noise is **non-monotonic short-window movement** — rating drops one year, then comes back up the next (real bridges don't heal):

| Component | Reversal triples | Rate |
|---|---:|---:|
| deck | 210 / 186,804 | **0.112%** |
| superstructure | 257 / 200,936 | **0.128%** |
| substructure | 196 / 199,534 | **0.098%** |

This is **remarkably low**. Most rating drops are followed by either more drops or stability — consistent with real deterioration, not inspector whim. *Caveat:* this measures only *reversed* drops; quiet drift in either direction would not appear.

### 4.3 Intervention/rehab events

Jumps of ≥+2 points in one cycle are very likely real maintenance interventions:

| Component | +2 jumps | Rate |
|---|---:|---:|
| deck | 1,494 | 0.83% |
| superstructure | 1,116 | 0.57% |
| substructure | 1,205 | 0.62% |

In modeling, treat these as intervention events, not natural evolution.

### 4.4 Deterioration rate by age (deck, excluding rehab jumps)

| Age band | Mean annual Δ | Std | n |
|---|---:|---:|---:|
| 0–10 | **−0.125** | 0.42 | 29,312 |
| 10–25 | −0.069 | 0.35 | 54,516 |
| 25–50 | −0.077 | 0.38 | 55,118 |
| 50–75 | −0.059 | 0.34 | 24,740 |
| 75–100 | −0.062 | 0.33 | 12,960 |
| 100+ | −0.072 | 0.37 | 1,926 |

Two surprises:
- **Fastest decline is in the first 10 years** — bedding-in / first-rating-cut effect. Bridges are typically rated 9 at construction and almost guaranteed to drop within their first inspection cycle.
- **Old bridges (>75 years) deteriorate slowly** — survivor bias. A bridge that's lasted 75 years without dropping below ~5 has self-selected as resilient (or has been quietly rehabbed).

### 4.5 Inter-rater noise — published evidence

FHWA's own 2001 inspection-reliability study (Phares et al., FHWA-RD-01-020) had 49 inspectors rate the same bridges:

- Condition ratings within **±1 point of the reference only ~68% of the time**.
- ±2-point spreads across inspectors on the same span were common.
- **~95% of variance was *not* explained by the bridge itself.**

This is much worse than what the WV panel implies. The reconciliation: the WV panel measures the same inspector (or a tight cadre) returning to the same bridge, so it captures **within-inspector temporal drift**, not the bigger **between-inspector** dispersion the FHWA study captured. Both are real. For a BMS, **between-inspector variance is the more damning number** — it means that if two different inspectors visited the same bridge today they'd disagree about its rating ~32% of the time at the ±1 level.

The published evidence and our own measurements point the same direction: ratings are usefully informative *in aggregate over a fixed inspector cadre*, and noisier at the individual-bridge level — worth keeping in mind for single-bridge decisions.

---

## 5. Gameability of the system

Several specific exploit paths exist; any BMS-style use needs to assume some of these are happening:

1. **One-point hop at the SD boundary.** Coding Guide language for "4" ("advanced section loss") vs "5" ("minor section loss") is fuzzy enough that a sympathetic inspector can hold a deteriorating bridge at 5 indefinitely. This is the single most consequential discretionary decision in the entire system.
2. **In-house QA.** State DOT inspectors rate bridges owned by the same state DOT. QC is internal. FHWA compliance reviews audit the *program*, not individual ratings.
3. **Load rating assumptions.** Switching LFR↔LRFR, picking a less conservative condition factor, or using more favourable distribution factors can lift a bridge out of posting territory without any physical change.
4. **Sufficiency formula quirks.** Built-in floors and special reductions create thresholds (SR=50, SR=80) that small input changes can cross.
5. **Inspection timing.** Schedule after patching, not before. Extend the cycle from 24 to 48 months under risk-based inspection rules.
6. **Inspector anchoring.** The easiest path is to copy last year's code. Our finding that ~91% of transitions are "no change" is partly real and partly anchoring.

Harder to cheese: geometry, year built, ADT (audited against traffic counts), and any rating ≤2 (which triggers reporting requirements). The quantitative data in the bridge file (Section 2.2) provides natural audit trail when used.

For BMS use, the takeaway is to anchor decisions on element-level quantities and the underlying bridge file where possible, rather than the single rating digit alone.

---

## 6. Predictive modeling

**Train/test split**: pre-2018 (n_train ≈ 130k) train; ≥2018 (n_test ≈ 42k) test. Features: lagged ratings (lag-1, lag-2), age, ADT, operating/inventory rating, sufficiency, cross-component ratings, year, year gap to next inspection, plus one-hot encoded nhs/functional_class/owner/district where available.

### Task A — predict the next inspection's component rating (regression)

| Component | Persistence MAE | Persistence exact-match acc | GBM MAE | GBM rounded acc |
|---|---:|---:|---:|---:|
| deck | **0.108** | **91.3%** | 0.239 | 89.8% |
| superstructure | **0.097** | **91.8%** | 0.214 | 90.5% |
| substructure | **0.090** | **92.3%** | 0.208 | 91.5% |

**Persistence wins.** A GBM trained on lags + structural features cannot beat "same as last year." At the 1-year horizon, the rating *level* is essentially a Markov chain with a very strong "stay put" diagonal.

### Task B — P(component drops to SD ≤4 next inspection | currently ≥5)

| Component | Base rate | LR AUC | LR AP | GBM AUC | GBM AP |
|---|---:|---:|---:|---:|---:|
| deck | 1.08% | 0.818 | 0.042 | 0.815 | 0.039 |
| superstructure | 1.10% | 0.818 | 0.033 | **0.829** | 0.040 |
| substructure | 0.81% | 0.806 | 0.024 | 0.804 | 0.026 |

- AUC ≈ 0.82 → top-decile list captures roughly half of next-year SD transitions.
- AP ≈ 0.04 → precision is low at any reasonable threshold. Use as a ranked watch list, not an alarm.
- LR ≈ GBM → signal is largely additive in the lag-features.

### Task C — P(rating drops ≥2 points next inspection)

| Component | Base rate | GBM AUC | GBM AP | AP/base |
|---|---:|---:|---:|---:|
| deck | 0.76% | **0.784** | 0.039 | 5.2× |
| superstructure | 0.61% | 0.749 | 0.019 | 3.1× |
| substructure | 0.49% | 0.749 | 0.020 | 4.0× |

These "big drop" events are partially *discovery* events — an inspector finds something previously missed. ~5× base rate lift is useful for inspection prioritisation.

### Task D — 3-class (same/down/up) next-inspection

| Component | "Predict same" baseline | GBM acc |
|---|---:|---:|
| deck | 91.3% | 90.9% |
| superstructure | 91.8% | 91.5% |
| substructure | 92.3% | 92.0% |

Persistence wins again. The deterioration signal is too rare per year for a generic classifier to outperform "nothing will change."

### 6.1 Feature importances (superstructure → SD drop, GBM)

| Feature | Importance |
|---|---:|
| superstructure_lag1 | 19.4% |
| age | 13.5% |
| year | 13.1% |
| superstructure (current) | 7.8% |
| adt | 7.8% |
| operating_rating | 7.3% |
| inventory_rating | 5.8% |
| deck (current) | 3.8% |
| owner_nan (missing flag) | 3.6% |
| substructure (current) | 3.0% |
| superstructure_lag2 | 2.3% |
| scour | 1.7% |
| district_nan | 1.1% |
| sufficiency | 1.1% |

History + age + cross-component ratings + load capacity dominate. The prominence of `year` is exactly the 2015–2018 recalibration leaking into the model.

---

## 7. How predictable is the system, really?

| Question | Answer |
|---|---|
| Will next year's rating equal this year's? | Yes, ~91% of the time. Trivial to predict. |
| Will next year's rating be lower? | ~7% probability; persistence misses these. |
| Will it drop ≥2 points? | ~0.5–0.8% — rare. AUC ≈ 0.75 achievable. |
| Will it cross from Fair (5) to Poor (4)? | ~1% — AUC ≈ 0.82, AP 0.04. **Useful for ranking, not alarms.** |
| Can we predict the level (0–9)? | Not better than persistence. |
| What does the noise floor look like? | Within-inspector reversal ~0.1%; published between-inspector spread ~32% at ±1. |
| What's the biggest confound? | The 2015–2018 SNBI methodology transition. Mean ratings fell ~0.6 points NOT from deterioration. |

The data is **moderately predictable but in a specific way**: short-horizon rating levels are dominated by persistence; what's predictable is the *risk of crossing thresholds* over a multi-year window. AUC ≈ 0.82 on the 1-year SD-flip task is the realistic ceiling with numeric features.

---

## 8. Inspector narratives — TF-IDF text models

The `bridges_data.json` file contains rich free-text inspector narratives per component, plus `_prev`-suffixed versions from the prior inspection cycle. We tokenise these into TF-IDF (1–2 grams, min_df=5, max_features=30k, English stopwords removed) and train an L2-regularised logistic regression — which **is** gradient descent: convex log-loss minimised by L-BFGS, one learned weight per n-gram. Pipeline: `text_analysis.py`.

### 8.1 Coverage

| Field | Non-empty | Median chars |
|---|---:|---:|
| `narrative_summary` | 7,346 | 859 |
| `narrative_deck` | 5,861 | 683 |
| `narrative_superstructure` | 7,173 | 1,182 |
| `narrative_substructure` | 6,858 | 1,143 |
| `narrative_substructure_prev` | 6,773 | 1,138 |

Merged-text length: median **4,455 characters**, p90 **9,480**. 7,321 / 7,698 bridges have ≥200 characters of usable text.

### 8.2 Four experiments (75/25 stratified split, seed 42)

| # | Setup | Target | Base | AUC | AP | Lift |
|---|---|---|---:|---:|---:|---:|
| 1 | Merged text → SD | any rating ≤4 | 16.7% | **0.976** | 0.909 | 5.5× |
| 2 | Merged text → substructure poor | substructure ≤4 | 7.9% | 0.955 | 0.668 | 8.5× |
| 3A | Numeric only (deck/super/age/ADT) → substructure poor | ≤4 | 7.6% | 0.821 | 0.309 | 4.0× |
| 3B | **Severity lexicon (50 words) only** | ≤4 | 7.6% | **0.941** | 0.594 | 7.8× |
| 3C | TF-IDF only | ≤4 | 7.6% | **0.963** | 0.700 | 9.1× |
| 3D | TF-IDF + numeric | ≤4 | 7.6% | 0.948 | 0.636 | 8.3× |
| 3E | Lexicon + numeric (interpretable combo) | ≤4 | 7.6% | 0.945 | 0.590 | 7.7× |
| 4 | **Previous-cycle narrative → current SD** | any ≤4 now | 16.5% | **0.981** | 0.928 | 5.6× |

- **The narrative alone beats the structural numeric model.** TF-IDF (3C, AUC 0.963) > numeric-only (3A, AUC 0.821) by 14 AUC points.
- **A 50-keyword lexicon also beats numeric** (3B, AUC 0.941). Predictive content concentrates in a small number of severity terms.
- **Naive text + numeric does not improve** over text alone, because 30k sparse text features overwhelm the few numeric ones under uniform L2. Group-wise regularisation or model stacking would fix this.
- **Previous-cycle narrative → current SD: AUC 0.981.** What an inspector wrote one cycle ago almost perfectly predicts the next rating. **This is the key result for forecasting.**

### 8.3 Caveat — partial tautology

Inspectors literally write phrases like "structure poor", "rated fair", "poor condition" — restatements of the numeric rating. Experiments 1 and 2 include some tautological signal. Cleaner reads:
- **Experiment 2** (8.5× lift): the narrative does NOT directly state the substructure rating; the model has to infer it from descriptions of decay.
- **Experiment 4** (AUC 0.981): the prior narrative was written *before* the current rating existed — genuine forecasting performance.

### 8.4 Top weighted terms (lexicon + numeric model 3E)

```
SD-direction (positive weights):
  poor condition         +1.07
  heavy spall            +0.47
  undercut               +0.46
  delaminated            +0.33
  delamination           +0.24
  undermining            +0.24
  settlement             +0.17
  scour critical         +0.17
  rust                   +0.15
  spall                  +0.13

Not-SD direction (negative weights):
  fair condition         −0.69
  crack                  −0.52    (cracks appear in nearly all narratives → weak alone)
  heavy spalling         −0.43    (register effect)
  minor                  −0.39
  satisfactory           −0.20
  section reduction      −0.19
  crazing                −0.16
  hairline               −0.11

Numeric (in same model):
  superstructure_rating  −0.31    (higher super rating → less likely substructure SD)
```

Quirks:
- **`heavy spall` (+0.47) vs `heavy spalling` (−0.43)** — singular/gerund split into opposite signs because of register difference between terse SD reports and verbose routine descriptions. Stemming would collapse this.
- **`crack` (−0.52)** — cracks are in almost every narrative, so the unmodified word has near-zero discriminative content; the negative weight is a residual.

### 8.5 Top words ranking SD vs not-SD (TF-IDF, Experiment 1)

Most positive (push toward SD):
```
poor, poor condition, loss, structure poor, remains poor, spalling, heavy,
superstructure poor, section, exposed, corroded, reinforcing, section loss,
deterioration, rated poor, deteriorated, deck poor, beam, reinforcing steel,
strands, spandrel, rebar, exposed corroded
```

Most negative (push toward not-SD):
```
good, good condition, fair, fair condition, culvert, structure fair,
remains fair, faint, minor, satisfactory, hairline, insignificant, box,
satisfactory condition, rated good, cell, rated fair, superstructure fair,
box beams, headwall, abutments, faint medium, parapets
```

### 8.6 Implications for forecasting (BMS use)

The Experiment 4 result (AUC 0.981 with prior-cycle text) is the operational headline. To turn it into a true forecasting tool:

1. Join `bridges_data.json` narratives onto `nbi_history.json` by `bars_number` so each historical year carries a text snapshot.
2. Build per-year TF-IDF + numeric features for the panel.
3. Re-run the drop-to-SD model with text features added — expected substantial lift over the structural-only AUC 0.82.
4. **Stem the tokens first** ("spall", "spalling", "spalls" → one token).
5. **Train per-component vectorisers** (one each for deck/super/sub) to avoid cross-component leakage.
6. Optional next steps: character n-grams (3–5) for typo robustness; sentence embeddings if (1–5) leave signal on the table.

For BMS use, the narrative recovers a substantial fraction of the information that the single rating digit compresses away — and it's already collected. Combining element-level data, narrative, and photographs gives a richer working picture than items 58/59/60 alone.

---

## 9. Context: what NBI was designed for, and how it maps to BMS use

A brief design-history note so the strengths and limits of the data are easier to keep in mind. The takeaway is short: NBI is excellent at what it was built for, and for BMS-style decisions it works best when paired with the richer layers (element-level, narrative, bridge file) that already exist alongside it.

### 9.1 Origin: Silver Bridge, 1967

The Silver Bridge collapse (Point Pleasant, WV, December 1967, 46 fatalities) prompted the Federal-Aid Highway Act of 1968 and FHWA's NBIS in 1971. The mission was narrow and well-defined: identify bridges at risk of failure across the national inventory. Triage, not life-cycle management.

### 9.2 Scale and federalism

~620,000 bridges, ~90,000 inspections per year, ~5,000–7,000 certified inspectors. With 56 reporting agencies operating independently, FHWA set a lowest-common-denominator data standard everyone could meet. An "experienced inspector assigns a 0–9 code" was the cheap, scalable answer in 1970s technology, and it has remained the federal layer's spine.

### 9.3 What the system does well

1. **Triage at the population level.** SD share has dropped from ~22% (1992) to ~6.8% (recent, nationally). The aggregate signal is real even when individual ratings are noisy.
2. **Federal funding allocation.** Sufficiency rating is the operative currency of the Highway Bridge Program.
3. **Longitudinal consistency.** 30+ years of broadly comparable format — what makes the WV panel statistically useful at all.
4. **Public accountability.** "% structurally deficient" is a blunt but functional headline metric.

### 9.4 Where BMS use benefits from additional layers

For asset-management workflows, pairing NBI with the broader bridge-file ecosystem tends to add the most leverage. Concretely:

| BMS need | What the NBI digit alone provides | What helps fill the gap |
|---|---|---|
| Stable longitudinal KPI | Confounded by 2015–2018 definition shift (§3) | Pre/post-2018 normalisation; element-level CS1–CS4 tracking |
| Per-bridge confidence | Inter-rater variance ~32% at ±1 (§4.5); within-inspector drift small (§4.2) | Element-level quantities, inspector ID controls, repeated inspections |
| Individual-bridge deterioration prediction | Persistence wins at 1-yr; AUC ≈ 0.82 / AP ≈ 0.04 at the SD-flip task (§6, §7) | Narrative features (§8); 5-yr horizons; survival models |
| Element-level quantities | The federal submission compresses to one digit (§2.1) | AASHTOWare BrM / SNBI element data — already collected post-2022 |
| Intervention-effect modelling | NBI doesn't tag rehabs; only the ≥+2 jump proxy (§4.3) | State bridge file work-history records |
| Risk model `P(failure | state) × consequence` | Sufficiency rating is endogenous to the condition codes (§2.1) | Component-level deterioration + scour + load-rating models stacked |

Commercial BMS platforms (AASHTOWare BrM, dTIMS, Agile Assets, Bentley AssetWise) sit on top of the NBI spine and add deterioration, life-cycle cost, program optimisation, and treatment-effectiveness models that the items-58/59/60 digits alone don't carry. The WV data we analysed is the federal-submission layer — a high-value backbone, and a starting point rather than a complete BMS substrate.

### 9.5 What our analysis adds

1. **Persistence dominates 1-year prediction** (§6) → for individual-bridge programming, plan around multi-year horizons.
2. **The 2015–2018 cliff** (§3) → reserve longitudinal comparisons for windows within a single methodology regime.
3. **Inspector narratives carry strong signal** (§8) → the cheapest BMS upgrade available in this data is wiring narratives into the model alongside the numeric ratings.
4. **The `year` feature carries ~13% of model weight** (§6.1) → models are partly fitting the coding regime; control for it explicitly.
5. **Sufficiency is endogenous** (§2.1) → useful as a summary, less useful as an optimisation target.

### 9.6 Summary

NBI was designed to find bridges at risk of failure, at national scale, in 1970s technology — and it does that well. SNBI and element-level data are the natural complements for asset-management questions; combining them with narrative and the state bridge file is where BMS-style models get most of their lift. Treat the NBI digit as a solid summary feature, and pair it with the richer layers when individual-bridge decisions are on the line.

---

## 10. Recommendations

### What to predict (for BMS-style use)
1. **5-year probability of any component dropping to ≤4**, not 1-year. The 1-year framing is saturated by persistence; 5-year matches both the inspection cycle and the capital-planning cycle, has a base rate of ~5–10%, and is more learnable.
2. **Probability of becoming Posted/Closed within N years.** This is what owners actually decide on; `status` gives clean labels.
3. **Deterioration rate (slope) by cohort** — useful for portfolio-level capital planning, not individual bridges.

### How to make models stronger
1. **Control for the 2018 recalibration explicitly.** Train pre/post separately, include a methodology-regime flag, or restrict training to 2020+.
2. **Use survival analysis, not single-step classification.** Time-to-SD-flip naturally handles censoring.
3. **Mine the inspector narratives.** Single biggest unexploited signal in this dataset (Section 8).
4. **Engineer cross-component dependencies as features.** Substructure problems cause deck problems with a lag; explicit "X_lag1 − Y_lag1" features will help.
5. **Add climate/location proxies.** District alone is too coarse; lat/lon × freeze-thaw cycles would matter.
6. **Treat ≥+2 jumps as intervention events**, not natural evolution.

### Applying to BMS-style workflows
1. **NBI digits work well for triage and reporting**; pair them with element-level and narrative data when driving individual-bridge programming decisions.
2. **Use SNBI element CS1–CS4 quantities** (AASHTOWare BrM or equivalent) where available — they carry the quantitative detail the rating digit compresses away.
3. **Ingest the inspector narrative as a feature.** Section 8 shows it's the largest unused signal in this data.
4. **Inspector fixed-effects** (where state DOT data permits) reduce the FHWA-2001 between-inspector variance.
5. **Use sufficiency rating as a summary, not an optimisation target** — it's endogenous to the condition codes (§2.1). Optimise against expected life-cycle cost or posting/closure probability.

### What this is *not* good for
- **Same-year rating estimation from non-NBI signals** — the SNR at 1-point granularity is bounded by inspector subjectivity.
- **Catastrophic failure prediction** — sub-2 events are <100 in the panel; not enough positives.

---

## 11. Files in this directory

| File | Purpose |
|---|---|
| `bridges_data.json` | Source: 7,698 bridges with metadata + narratives (latest + `_prev`) |
| `nbi_history.json` | Source: 9,979 bridges × 1992–2025 inspection time series |
| `analysis.py` | Reproducible structural-model pipeline (panel, transitions, models A–D) |
| `text_analysis.py` | Reproducible TF-IDF / lexicon pipeline (experiments 1–4) |
| `model_results.json` | Raw metrics from `analysis.py` |
| `text_results.json` | Raw metrics from `text_analysis.py` |
| `nbi_system_summary.md` | Original standalone summary of the NBI rating system. **Superseded by Sections 2, 4.5, 5, and 9 of this report.** Keep for provenance. |
| `REPORT.md` | This document |
