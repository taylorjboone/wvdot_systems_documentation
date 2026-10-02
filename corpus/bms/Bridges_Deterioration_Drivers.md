# Deterioration Drivers — Do trucks, load rating and weather predict bridge decay?

*2026-09-27. A follow-up to [Family × District Deterioration](/docs/Bridges_Family_District_Deterioration),
which found that family, district and age explain little of a bridge's condition. This report adds three new
data sources — truck traffic, load rating and 34 years of weather — and asks whether they predict deterioration
better. Reproduce with `sandbox/.venv/bin/python scripts/bridges/deterioration_drivers.py`.*

## The short answer

- **Truck traffic barely helps.** Traffic, span and deck size lift the deck model's accuracy a little
  (R² 0.32 → 0.33) and hardly change the chance of a rating drop. District 10's weak PSC box beams are **not**
  explained by truck counts: their median truck traffic is the same as everywhere else.
- **Load rating helps, but it's circular.** Adding the NBI operating / inventory rating and posting lifts
  deck R² to 0.40 and superstructure to 0.55 — but a load rating is recalculated when members lose section, so
  it partly *is* the condition. Useful for filling in a missing rating; not evidence of a cause.
- **Weather adds nothing once you account for the year of the inspection.** The first cut made weather look
  like the biggest driver of deterioration. It wasn't: the weather figures were standing in for the calendar
  year, and the year itself carries a very large signal — see the next point.
- **The biggest predictor of a rating drop is *when* the bridge was inspected.** The statewide share of
  inspections that downgrade a deck swings from 8–12% in most years to **39% in 2013**, and upgrades jump to 12%
  in 2021. Bridges don't age three times faster in one year: these are waves of inspection practice. Adding the
  inspection year lifts prediction of a deck drop from AUC 0.77 to 0.82 — more than traffic, load rating and
  weather combined.

## Data

- **Bridges:** 7,030 WVDOT-owned in-service bridges with a family (material / design / span count), district,
  year built and a current deck (6,079), superstructure (6,390) or substructure (6,336) rating — the same
  population as the earlier report.
- **Truck traffic and load rating** (`qv_traffic_load_history`): at every inspection since 2001 — NBI 29 ADT and
  109 truck %, SNBI B.H.10 trucks per day, NBI 64 / 66 operating and inventory ratings (metric tons), NBI 41
  posting. Truck ADT = the SNBI count, else ADT × truck %.
- **Weather** (`ib_bridge_year`, FHWA InfoBridge): for every NBI year 1992–2025 at each bridge — freeze-thaw
  cycles, precipitation, precipitation and snow days, days below 0 °C, time of wetness, humidity, temperature.
  The weather is gridded (neighbouring bridges share values), so it is a regional measure, not a site one.
- **Inspection pairs:** 41,386 pairs of consecutive inspections 10 months to 4 years apart on the same rating
  standard (NBI or SNBI, never across the 2024–25 switch). Pairs where the rating *rose* (3.6–3.8%, i.e. work
  was done) are set aside.

## Method

Two questions, each answered with gradient-boosted trees (which find non-linear effects and interactions on
their own) and scored only on data the model did not see:

- **A. Condition now** — the earlier report's question: predict a bridge's current rating. Five-fold cross-validated
  R² (share of the variation explained; 1 is perfect) and mean absolute error in rating points. The earlier
  report's own method — a straight line against age inside each family × district cell — is re-run the same way
  for comparison.
- **B. Deterioration rate** — does the rating drop by the next inspection? Predict it from the rating then, age,
  time between inspections, family, district, and the traffic, load rating and weather of those years. Folds are
  split **by bridge**, so no bridge's inspections are on both sides. Scored by AUC (0.5 = no better than a coin,
  1 = perfect ranking of which pairs drop), log loss and Brier score (lower is better).

A plain logistic regression with family, district and year fixed effects gives the direction and size of each
factor (odds ratios).

## A. Condition now

Cross-validated R² (mean absolute error, rating points):

| Model | Deck | Superstructure | Substructure |
|---|---:|---:|---:|
| Earlier report: straight line per family × district | 0.282 (0.77) | 0.406 (0.78) | 0.341 (0.70) |
| Family × district × age (trees) | 0.319 (0.74) | 0.444 (0.75) | 0.375 (0.68) |
| + traffic & size (no load rating) | **0.330** (0.73) | **0.480** (0.72) | **0.405** (0.66) |
| + load rating & posting only | 0.398 (0.69) | 0.551 (0.68) | 0.392 (0.67) |
| + traffic & load rating | 0.413 (0.68) | 0.569 (0.66) | 0.423 (0.65) |
| + climate | 0.320 (0.74) | 0.449 (0.75) | 0.375 (0.68) |
| + traffic, load rating & climate | 0.408 (0.68) | 0.569 (0.66) | 0.421 (0.65) |
| traffic, load rating & climate, **no district** | 0.382 (0.71) | 0.548 (0.68) | 0.408 (0.66) |
| traffic & climate (no load rating), **no district** | 0.303 (0.75) | 0.455 (0.75) | 0.384 (0.67) |

What it says:

- Letting the model bend with age (trees instead of one straight line per cell) is worth about as much as all the
  honest new data combined: deck 0.28 → 0.32.
- **Traffic and size** — truck ADT, ADT, truck %, cumulative trucks (truck ADT × age), truck growth, deck
  area, longest span, NHS — add a little: deck +0.01, superstructure +0.04, substructure +0.03.
- **Load rating** adds the most, especially to the superstructure (+0.11), which is exactly the component a load
  rating is calculated on. In the full deck model the inventory rating is the single most important input
  (ahead of district and age). Treat this as condition information leaking back in, not a cause.
- **Climate adds nothing** to condition now (0.319 → 0.320). And it can't stand in for district: without district,
  traffic and climate reach 0.303, below family × district × age alone. The district effects in the earlier
  report are not weather effects.

By family (deck), family × district × age vs. the full model (which includes load rating):

| Family | n | Base R² | Full R² |
|---|---:|---:|---:|
| PSC box beam multiple, 1 span (5/05/1) | 1,797 | 0.362 | 0.440 |
| Steel stringer, 1 span (3/02/1) | 1,080 | 0.201 | 0.229 |
| Steel continuous stringer, 1 span (4/02/1) | 511 | 0.326 | 0.441 |
| RC slab, 1 span (1/01/1) | 298 | 0.384 | 0.553 |
| Steel continuous slab-on-floorbeam, 1 span (4/24/1) | 288 | 0.233 | 0.280 |
| Steel slab-on-floorbeam, 1 span (3/24/1) | 225 | 0.318 | 0.459 |
| Steel continuous stringer, 2 spans (4/02/2) | 198 | 0.142 | 0.258 |

Simple steel stringers — the second-largest family — stay hard to predict with anything we have (0.23).

### District 10's PSC box beams — trucks don't explain it

The earlier report put District 10's poor single-span PSC box-beam decks (average 5.27 against 6.35–6.86
elsewhere) down to coal trucks. The NBI truck counts don't support that:

| District | n | Mean deck | Median trucks / day | Freeze-thaw cycles / yr | Residual without district* |
|---|---:|---:|---:|---:|---:|
| 1 | 266 | 6.54 | 12 | 84 | −0.08 |
| 2 | 310 | 6.49 | 9 | 85 | +0.07 |
| 3 | 170 | 6.81 | 13 | 88 | +0.15 |
| 4 | 237 | 6.86 | 15 | 91 | +0.09 |
| 5 | 106 | 6.56 | 24 | 98 | +0.06 |
| 6 | 82 | 6.35 | 27 | 94 | −0.06 |
| 7 | 142 | 6.54 | 19 | 88 | +0.00 |
| 8 | 136 | 6.54 | 4 | 96 | −0.03 |
| 9 | 115 | 6.45 | 14 | 92 | +0.09 |
| **10** | **233** | **5.27** | **13** | **91** | **−0.31** |

\* Actual minus predicted deck rating from a model given family, age, traffic, load rating and climate but not
the district. District 10 is still 0.31 points worse than everything we can measure predicts.

Two caveats before discarding the coal-truck idea: NBI truck percentages on county routes are coarse estimates
that are rarely re-counted, and coal haul is concentrated on specific routes (the Coal Resource Transportation
System) rather than spread across a district. A proper test needs CRTS route membership or weigh-in-motion
counts, not NBI 109. What the data does say is that **District 10's gap is not a traffic, weather or load-rating
effect we can see**; practice (how D10 rates PSC box decks, or how they were built and maintained) remains an
equal candidate.

## B. Deterioration rate — does the rating drop by the next inspection?

Deck 32,918 pairs (18.6% drop), superstructure 35,719 (17.7%), substructure 35,070 (17.1%). AUC (log loss):

| Model | Deck | Superstructure | Substructure |
|---|---:|---:|---:|
| No model (the average drop rate) | 0.500 (0.481) | 0.500 (0.467) | 0.500 (0.458) |
| Rating, age, gap, family, district | 0.769 (0.406) | 0.772 (0.392) | 0.778 (0.381) |
| + traffic only | 0.772 (0.404) | 0.773 (0.392) | 0.779 (0.380) |
| + traffic & load rating | 0.774 (0.403) | 0.777 (0.389) | 0.782 (0.379) |
| + weather in the interval | 0.802 (0.378) | 0.812 (0.361) | 0.821 (0.347) |
| **+ inspection year & rating standard** | **0.817** (0.366) | **0.823** (0.352) | **0.838** (0.334) |
| + year + weather | 0.819 (0.365) | 0.824 (0.350) | 0.837 (0.334) |
| + year + local weather anomaly | 0.816 (0.367) | 0.823 (0.352) | 0.837 (0.334) |
| + year + traffic + local weather anomaly | 0.819 (0.365) | 0.824 (0.351) | 0.838 (0.334) |
| traffic, local weather anomaly & year, no district | 0.802 (0.379) | 0.809 (0.364) | 0.819 (0.350) |

### Why the weather looked important, and why it isn't

On its own, the weather of the years between two inspections raises deck AUC from 0.77 to 0.80 — apparently
the largest gain of any new data. Two things gave it away:

1. **The directions made no physical sense.** Holding everything else fixed, more freeze-thaw cycles and more
   snow days came out as *lowering* the odds of a rating drop by about 40%, while more days below 0 °C
   *tripled* them. Freeze-thaw damage can't be protective while cold days are three times as harmful.
2. **The inspection year does the same job better.** Every bridge in a year shares much of that year's weather,
   so the weather numbers work as a label for the year. Given the year itself, the model does better (deck
   0.817) — and adding the weather back on top gains almost nothing (0.819). Using only each bridge's
   *local* weather — its difference from the statewide average for the same years — adds nothing at all
   (0.816).

So the year carries the signal, and the weather was borrowing it. The weather effects that remain in the
logistic model still point in contradictory directions (freeze-thaw anomaly OR 0.66, snow-day anomaly 0.74,
below-zero-day anomaly 1.81 for the deck) — the signature of collinear regional measures, not of a physical
driver. With gridded weather, the model can't separate climate from geography.

### The year effect: waves of inspection practice

Share of deck inspections followed by a lower (or higher) deck rating at the next inspection, by the year of the
first one:

| Year | Pairs | Drop | Rise |
|---|---:|---:|---:|
| 2008 | 598 | 12.2% | 0.5% |
| 2009 | 975 | 11.9% | 1.3% |
| 2010 | 2,290 | 14.3% | 3.0% |
| 2011 | 2,778 | 18.7% | 1.9% |
| 2012 | 3,237 | 27.3% | 2.7% |
| **2013** | 2,984 | **38.7%** | 1.6% |
| 2014 | 2,782 | 28.8% | 2.0% |
| 2015 | 2,769 | 23.8% | 2.2% |
| 2016 | 3,097 | 19.3% | 2.0% |
| 2017 | 2,933 | 13.2% | 3.2% |
| 2018 | 2,868 | 9.3% | 3.3% |
| 2019 | 2,947 | 8.1% | 3.5% |
| 2020 | 2,835 | 9.7% | 6.2% |
| **2021** | 2,639 | 6.9% | **12.4%** |
| 2024 | 2,173 | 8.2% | 7.4% |

(Years with fewer than 500 pairs left out.) Nearly four in ten decks inspected in 2013 were rated lower at the
next inspection; by 2019 it was one in twelve. No physical process does that statewide. It looks like a
recalibration — a push around 2012–2015 to rate decks more severely, followed by a period in which inspections
of 2020–21 raised as many ratings as they lowered. The earlier report's District 7 "rating compression" finding
is the same phenomenon seen at district level.

**This matters for any deterioration curve fitted to WV data:** a curve fitted across 2009–2025 absorbs this
wave and will overstate decay for bridges rated during it and understate it for the recent years. Deterioration
models (BMS family curves, Markov transitions) should carry an inspection-era term, or be fitted within stable
periods, before any physical driver is added.

### Traffic and load rating in the rate model

From the logistic model with family, district and year fixed effects (odds ratio per standard deviation):

| Factor | Deck | Superstructure | Substructure |
|---|---|---|---|
| Truck ADT (log) | 1.16 (p = 0.08) | 0.95 (n.s.) | 0.98 (n.s.) |
| Truck % | 0.99 (n.s.) | **1.08** (p = 0.007) | 1.04 (n.s.) |
| Inventory rating | **0.89** (p = 0.002) | **0.87** (p < 0.001) | **0.92** (p = 0.02) |
| Posted for load | **1.21** (p = 0.008) | **1.27** (p < 0.001) | 1.03 (n.s.) |
| Time between inspections (+0.8 yr) | 1.40 | 1.31 | 1.31 |
| Age (+26–28 yr) | 1.21 | 1.38 | 1.31 |
| Rating at the first inspection (+1.2 pts) | 2.86 | 3.02 | 2.97 |

Trucks show at most a small effect (a slightly higher truck share on the superstructure). Bridges with a lower
inventory rating, and posted bridges, are more likely to drop — consistent with a weaker structure losing
condition sooner, but again partly the same information as the rating.

## What this means

1. **The earlier report's conclusion stands:** family, district and age leave most of the variation in bridge
   condition unexplained, and this report's new data doesn't change that much. The honest improvement is
   modest — deck R² from 0.28 to 0.33, and the prediction of a deck drop barely moves with traffic (AUC 0.769 → 0.772).
2. **The largest thing standing between WV and a better deterioration model is rating consistency over time**,
   not missing covariates. The 2012–2015 downgrade wave and the 2021 upgrade wave dwarf every physical effect we
   can measure. Before fitting family curves, correct for (or exclude) those eras.
3. **Load rating is a good stand-in for a missing condition rating**, not a driver. Use it to impute, not to
   explain.
4. **Traffic needs better data to be tested properly.** NBI truck percentages are coarse. CRTS route membership,
   weigh-in-motion stations and permit-load records would let the coal-truck hypothesis for District 10 be
   tested directly.
5. **Weather needs finer data to be tested properly.** InfoBridge's climate is regional; what differs between
   neighbouring bridges is exposure — de-icing salt application, drainage, deck joints, water under the
   bridge. Salt-route and snow-and-ice treatment records from MMS would be the next dataset to try.

## Reproducing

```sh
sandbox/.venv/bin/python scripts/bridges/deterioration_drivers.py --out drivers.json
```

`scripts/bridges/deterioration_drivers.py` assembles the data from `bridges_all.duckdb`
(`qv_bridge_decoded`, `qv_bridge_list`, `qv_traffic_load_history`, `qv_bridge_climate`, `ib_bridge_year`,
`qv_nbi_timeseries`); `scripts/bridges/deterioration_models.py` fits the models (about ten minutes on a
laptop). The Bridge Wizard can query the same tables.
