# How the raw pavement distresses behind Good / Fair / Poor actually deteriorate

**Study date:** 2026-09-29.

**Data:**
- the vendor survey files 2020–2025, raw (not re-conflated);
- TheHub projects;
- MMS (OM) work lines;
- LRS inventory from `analysis_segments`.

**Method:** route averages on untouched extents (not segment-to-segment matching), with years compared on the common milepoint span.

**Scripts and outputs:** `dtims_docs/raw-deterioration-study-2026-09-29/scripts/` and `results/`. How the whole study was done, step by step: [Raw Distress Study — Process](/docs/Pavement_Raw_Distress_Study). Follow-ups: [Treatment resets](/docs/Pavement_Treatment_Resets) and [Treatment strategies](/docs/Pavement_Treatment_Strategies).

---

## 1. Bottom line

| Raw value (MAP-21 metric) | How it deteriorates on untouched WVDOT pavement | Recommended model | What AMPS does today |
|---|---|---|---|
| **IRI, asphalt** | The rate depends strongly on the current IRI. It is almost flat below ~95 in/mi, ~2–7 in/mi/yr at 95–170, ~9–13 at 170–250 and 50+ above 300. Traffic, NHS and functional class add almost nothing once the level is known. | **State-based convex rate:** `dIRI/dt = 0.8 + 0.49·(IRI/100)^3.4` in/mi/yr, with a hold of ~⅓ of that rate for the first ~3 years after a resurfacing. Equivalent log form: `d ln IRI/dt = −0.36 + 0.080·ln IRI`, floored at 0.8 in/mi/yr. | IRI = g(PSI curve) + offset. That is too fast on smooth roads (+5/yr below 95, observed ≈0). It is right at 120–170 and too slow above 170 (+7.8 vs +13; +22 vs +53). |
| **Cracking, asphalt (FHWA % — the value GFP uses)** | ~2.2–2.6 points/yr on average. The rate rises with the square root of the current cracking. | **√C grows linearly in time:** `dC/dt = 0.85·√C`, i.e. **C(t) = (√C₀ + 0.42·t)²**. From 1% it takes 3 yr to reach 5% (loses Good) and 8 yr to reach 20% (Poor). | Linear +0.15 / 0.37 / 0.56 %/yr by route group. Those are **dTIMS Percent_Cracking factors applied to FHWA cracking**: 3–7× too slow above 5% cracking. |
| **Rut, asphalt** | **No measurable progression** on untouched pavement: −0.004 ± 0.003 in/yr. There is no level dependence and no traffic effect worth modelling. It adds ≈ +0.007 in in the first year after paving (densification). | **Hold rut constant** after a small early-life step (+0.01 in over the first 1–2 years). Rut is a property of the mix and the last treatment, not a clock. | +0.022 in/yr everywhere, from RDI + offset. On the validation extents that turns 15% of lane-miles from rut-Good to Fair in two years that the survey says stayed Good. |
| **Faulting, JCP** | +0.003 in/yr at ~0.03 in (2020–22 data only). The 2023+ vendor reports ~0 on most concrete. | Linear +0.003 in/yr. It practically never reaches Poor (0.15 in) within a planning horizon. | Held constant. That is harmless, but it is because the input is 0, not by design. |
| **IRI / cracking, JCP & CRC** | JCP IRI +1.5 to +4.8 in/mi/yr at IRI 80–100, cracking +0.15–0.5 %/yr. There are no clean CRC pairs. | Linear JCP IRI +3 in/mi/yr, cracking +0.3 %/yr. Use the JCP values for CRC until there is data. | IRI from PSI curves (+8.8 in/mi/yr on these RC segments). |

**Which inputs matter for GFP.** On 2024 asphalt, **Poor is IRI + cracking on 85%** of Poor lane-miles.

What keeps a lane-mile out of Good when only one metric fails:

| Metric | Share of lane-miles |
|---|---|
| IRI | 28.7% |
| Cracking | 3.8% |
| Rut | 1.0% (Interstate 6.5%) |

The IRI and FHWA-cracking models decide the GFP outlook; rut matters mainly on the Interstate, and faulting doesn't matter.

**The inventory fields asked about** (NHS, AADT, functional system, surface type, truck ADT):
- **Surface type is essential**: models are per surface.
- **The others do not improve prediction once the current level is in the model.** Cross-validated error changes by −2% to +17%, i.e. no gain or worse.
- Where they are "significant", the sign is backwards for a load effect: busier roads crack *slower* at the same level. That is the pavement structure and treatment history (thicker, better-built high-volume roads), which the inventory doesn't carry, not traffic protecting the road.

**Validation.** Applying these models to every 0.1-mi record of 715 clean miles moves the 2023 survey forward to 2025:

| | Predicted | Observed |
|---|---|---|
| % Poor | 20–22% | 22.1% |
| IRI-Poor | 38.4% | 38.5% |

A constant-rate model sends % Good to 0. Adding the current engine's rut growth takes 7 points off % Good.

**The data must be fixed before any of this goes into a model** (§3). In short:
- The vendor/method changed between 2022 and 2023: cracking ×4, rut +0.05 in, faulting → 0.
- The 2022 file's Interstate records are really the 2019 survey.
- The 2024 statewide survey reads rut ~0.02 in low.
- The 2023+ data has no usable faulting.

---

## 2. Data and method

### 2.1 Why route averages, not segment-to-segment matching

The vendor's 0.1-mi records don't line up between years: milepoints drift, records get re-split, and GPS jitters. Matching 1-1 mixes location error into the change. Instead, for each route and each pair of survey years:

1. **Common extent.** Keep only records inside the milepoint span both years covered (`max(min) … min(max)`, at least 0.4 mi).
2. **Drop event records:** `BRIDGE`, `CONSTR`, `LANEDEV`, `WET`, `RAILWAY`.
3. **Work mask** (§2.2).
4. **Average** each raw value over what is left, per year (at least 5 records = 0.5 mi each year). The change is route mean(y₂) − route mean(y₁).
5. **Time** is the difference of the two years' **median survey dates**, not the file years. 2024 ran from Apr 2024 to Jan 2025, so the intervals are 0.9–2.3 years.

The unit of analysis is a route pair. 4,639 route pairs were built, 1,520 consecutive pairs have ≥0.5 mi both years, and 807 of those are route-clean.

### 2.2 "No TheHub work": two definitions

**Work pulled for the mask:**
- **TheHub:** every project with a route segment and a construction phase, 11,001 projects / 16,089 route segments (`pull_hub_mms.py`). Withdrawn / terminated / reserve / hold and Technical Support projects are dropped.
  - Work window = start (milestone 18 actual → CN phase start → letting) to completion (milestone 20 actual → CN phase end → expected completion).
  - A project touches a pair when its window overlaps [survey 1 − 60 days, survey 2].
  - A completed project with no dates at all always counts.
  - Routes are matched on the first 11 characters of the route ID, so both directions of a divided route count.
- **MMS:** OM daily work lines for paving (210), skip patching (203), grinding (401), surface treatment / fog seal (204/205) and PCC work (240/241/245), dated between the two surveys. OM only starts in July 2024, so it only cleans 2024→2025. Patching tons (200/201/207/209) were kept as a covariate; they had no effect.

**The two samples:**

| Sample | Rule |
|---|---|
| **Route-clean** (primary, as asked) | No TheHub or MMS work **anywhere on the route** in the window. |
| **Extent-clean** (larger, confirmatory) | Work elsewhere on the route is allowed. Records within 0.3 mi of a project's or MMS line's milepoints are removed from both years. This keeps the untouched parts of Interstates and US routes. |

**Sample sizes (asphalt; the 2023+ files are the main ones):**

| Era | Sample | Route pairs | Routes | Miles | Composition |
|---|---|---|---|---|---|
| 2023–2025 | Route-clean | 533 | 311 | 1,497 | ≈64% County (66% of miles in District 4), ≈21% Interstate |
| 2023–2025 | Extent-clean | 808 | 453 | 4,213 | ≈US 45%, Interstate 19%, County 24%, WV 12% |
| 2020–2022 | Route-clean | 84 | 52 | 641 | Interstate / US / WV |
| 2020–2022 | Extent-clean | 296 | 173 | 3,100 | Interstate / US / WV |

Only 2024 covers the whole network (15,124 routes). The other years cover 250–1,000 routes: the Interstate / NHS / US system, plus mostly District 4 county roads in 2023 and 2025. So a route has a before and after only if it is in one of those.

### 2.3 Estimation

- **Every model is fitted on the change over the pair:** `Δ = Δt·(rate terms) + γ·off24`.
  - `off24` = +1 when the second survey is 2024 and −1 when the first is, which absorbs the 2024 offset (§3).
  - This handles unequal intervals and survey-year offsets properly.
- **Level terms use the pair's midpoint** (mean of the two years). A first-year level builds regression-to-the-mean into any "rate vs level" slope. This was checked with an independent level, the 2023 value for 2024→2025 pairs (§4.1, §4.2).
- **Weights** are the miles averaged. Standard errors are clustered by route. Model forms are compared by **5-fold cross-validation grouped by route**, predicting the second year's level from the first.
- **Rate-vs-level tables** show the annual change with the 2024 offset removed, grouped by midpoint level.
- **Inventory attributes** are length-weighted over the pair's extent from `analysis_segments`: NHS (FAS 1/2/4), functional class, AADT, single + combination truck ADT, truck %, district, coal route, lanes.

---

## 3. Data problems found — fix or handle before modelling

| # | Problem | Evidence | Consequence / handling |
|---|---|---|---|
| 1 | **The vendor / method changed between the 2022 and 2023 files** (different column layout: 2023+ has `IDLocator`, chainage, patching, potholes). | On the same untouched routes, 2022→2023:<br>• FHWA cracking +2.8 to +7.3 pts/yr (2020–22 routes average 1–2%, 2023+ 7–13%);<br>• Percent_Cracking −1.5;<br>• rut **+0.044 to +0.057 in in one step** (2020–22 changes are ±0.005);<br>• faulting 0.10 → 0.00. | **No distress model can use a pair that spans 2022→2023.** IRI is standardized (ASTM E1926) and crosses the change reasonably (+2.4 to +7.5 in/mi/yr), but it was also kept within an era. |
| 2 | **2020–22 cracking is not stable year to year.** | On the same untouched routes, FHWA cracking was 1.36% (2020), 0.30% (2021), 1.64% (2022). | The old files are usable for IRI (and faulting) only. |
| 3 | **The 2022 file's 11,084 Interstate records are stamped `COND_YEAR` 2019**, but dated 31 May – 4 Jun 2022. | • At the same milepoints their IRI is **10–11 in/mi lower** than both 2020 and 2021 (corr 0.59–0.66; 2020 vs 2021 corr 0.80).<br>• Untouched Interstates "improve" −3.1 in/mi/yr from 2021 to 2022 while other systems worsen +2.7.<br>• Not a copy of 2020/21 (0.3% identical values). | These are almost certainly the **2019 survey re-delivered**. `condition_history` stores them as 2022 (the pipeline takes the year from the file name). Ask the vendor or drop them. They were excluded from rates by the era split. |
| 4 | **The 2024 statewide survey is offset** (Apr 2024 – **Jan 2025**, including winter runs). Estimated offset vs 2023/2025, from the pairs and the three-survey triangle: | | Every model carries a 2024 offset term. Rates are anchored on 2023→2025. |
| | • rut | −0.017 to −0.021 in (t −7 to −15) | |
| | • IRI (unflagged) | −3 to −5 in/mi on route-clean, ≈0 on extent | |
| | • FHWA cracking | −0.7 on route-clean, 0 on extent | |
| | • Percent_Cracking | +0.1 to +0.24 | |
| 5 | **Faulting is effectively missing from 2023 on.** | • `Fault_Avg` is 0 on all asphalt (correct) and on 50–63% of JCP / ~98% of CRC records.<br>• JCP means 0.006 (2023), 0.020 (2024), 0.007 (2025) — inconsistent. | Faulting rates come from 2020–22 only. Get the vendor's faulting algorithm and data. |
| 6 | **IRI flags differ by year:** `IRI_FLAG` is on for 23% of 2024 records vs 6–9% in other years; flagged values are higher. | 2023→2024 IRI change: +7.2 (all) vs +3.8 (unflagged). | Rates use unflagged IRI. GFP shares use all records (as rated today). |
| 7 | **Date columns.** | 2023's `DATE` mixes Excel serials, ISO strings and d/mm/yyyy; 3,822 records have no date. | Parsed all three formats. Missing dates → the file's median date. |
| 8 | **Surface type.** | 2020–22 has only ASP / CON (no JCP/CRC split). 2023+ has ASP / JCP / CRC / OTH. | Concrete in the old era is "PCC". A route's surface must be ≥90% ASP in both years to count as asphalt (a surface change also flags unrecorded work). |

---

## 4. Results per raw value

### 4.1 IRI on asphalt

#### Annual change by IRI level

2024 offset removed; 2023–2025 files.

| Midpoint IRI (in/mi) | Route-clean pairs | Miles | Mean in/mi/yr | Median in/mi/yr | %/yr | Extent-clean miles | Mean in/mi/yr | %/yr |
|---|---|---|---|---|---|---|---|---|
| ≤60 | 5 | 85 | −6.7 | −8.9 | −12 | 221 | −5.2 | −9.5 |
| 60–80 | 24 | 301 | +0.9 | +0.2 | 1.4 | 987 | +0.2 | 0.3 |
| 80–95 | 9 | 45 | −0.7 | −1.8 | −0.8 | 571 | +0.2 | 0.3 |
| 95–120 | 23 | 81 | +2.6 | +4.5 | 2.4 | 940 | +2.4 | 2.3 |
| 120–145 | 41 | 159 | +5.1 | +4.6 | 3.9 | 469 | +2.4 | 1.8 |
| 145–170 | 46 | 149 | +6.5 | +5.5 | 4.1 | 229 | +7.1 | 4.5 |
| 170–220 | 88 | 193 | +9.0 | +5.9 | 4.6 | 274 | +8.9 | 4.6 |
| 220–300 | 123 | 202 | +11.8 | +12.3 | 4.6 | 228 | +13.0 | 5.1 |
| >300 | 174 | 283 | +53.6 | +46.6 | 14.1 | 295 | +53.1 | 14.0 |

**The 2020–22 files show the same shape** (extent-clean, 3,100 mi):

| Midpoint IRI | in/mi/yr |
|---|---|
| 60–80 | 0.0 |
| 80–95 | +2.3 |
| 95–120 | +2.9 |
| 120–145 | +3.7 |
| 145–170 | +5.0 |

**It isn't regression to the mean.** For 2024→2025 pairs, the slope of the annual change on the level is:

| Level used | Slope |
|---|---|
| Year-1 level | 0.24 |
| Midpoint | 0.24 |
| **Independent 2023 level** | **0.25** (t = 13) |

The very smooth band (≤60) goes negative. That is noise plus unrecorded work: the band is small and made of smooth Interstates.

#### Functional forms

Cross-validated RMSE of the second-year IRI, in/mi:

| Form | Route-clean | Extent-clean | Below IRI 170 (route / extent) |
|---|---|---|---|
| Constant rate (+14.7 / +6.7 in/mi/yr) | 34.2 | 23.0 | 17.4 / 10.1 |
| Exponential in time (constant %/yr, 3.8% / 2.1%) | 32.8 | 22.6 | — |
| Linear in level: `rate = a + b·IRI` | 27.8 | 18.1 | — |
| **Log-log: `d ln IRI/dt = a + b·ln IRI`** | **26.9** | **18.1** | 6.2 / 7.8 |
| **Floor + power: `rate = c₀ + c₁·(IRI/100)^p`** | 28.1 | 18.3 | 7.7 / 7.9 |

Fitted parameters:

| Form | Route-clean | Extent-clean | Bootstrap 90% |
|---|---|---|---|
| Log-log | a = −0.434, b = 0.0925 | a = −0.360, b = 0.0800 | |
| Floor + power | c₀ = 0.91, c₁ = 0.43, p = 3.46 | c₀ = 0.78, c₁ = 0.49, p = 3.38 | c₀ 0–1.7, c₁ 0.16–1.1, p 2.9–4.1 |

**Recommendation: the floor + power form.** It cross-validates as well as the log-log form, never predicts a road getting smoother by itself, and has a direct reading.

Rate at a given IRI (extent fit):

| IRI | 60 | 80 | 95 | 120 | 150 | 170 | 200 | 250 | 300 | 400 |
|---|---|---|---|---|---|---|---|---|---|---|
| in/mi/yr | 0.9 | 1.0 | 1.2 | 1.7 | 2.7 | 3.7 | 5.8 | 11.5 | 20.7 | 53 |

IRI alone takes decades to go from 95 to 170 (~39 yr at these rates; ~20 yr using the 2020–22 rates, which are faster at 95–120). So **smooth asphalt does not lose Good or become Poor through roughness first — cracking gets there first** (§4.2).

#### Inventory fields

Level-adjusted, extent-clean. The "excess" is the observed rate minus the rate the level predicts.

| Field | Group | Excess in/mi/yr (90% CI) |
|---|---|---|
| System | US | **+1.0** (0.2 to 1.7) |
| System | Interstate | −0.1 |
| System | WV | −0.1 |
| System | County | −0.9 |
| NHS | NHS | +0.5 (n.s.) |
| NHS | non-NHS | −0.1 |
| AADT | 8–20k | **+1.8** |
| AADT | >20k | **−1.5** |
| AADT | other bands | n.s. |
| Truck ADT | 100–300 | +1.1 |
| Truck ADT | 1–3k | +2.0 |
| Truck ADT | >3k | **−1.6** |
| District | D1 | +1.5 |
| District | D9 | +1.4 |
| District | D5 | +0.5 |
| District | D8 | +0.7 |

None of these improves cross-validated error; the best block (functional class) changes it by +0.5%. There is **no consistent traffic gradient**. The heaviest-traffic routes (Interstates) roughen *slower* than their IRI predicts.

#### Early life and selection

- **Early life:** on extents paved by a TheHub project (mostly code 08 minor HMA overlay) 0–3 years before the first survey, IRI rose 1.5–3.1 in/mi/yr against 4.4–9.4 predicted from their level. That supports a ~3-year hold at ~⅓ rate after resurfacing.
- **Selection bias:** routes that got TheHub pavement work *after* the pair roughened faster than their level predicts: +1.2 in/mi/yr (extent) to +4.0 (route). Leaving out worked routes therefore understates the rate for the roads the program actually treats by about 1–2 in/mi/yr. That is inside the model's uncertainty, but add it if the model is used only on candidate segments.

### 4.2 FHWA cracking on asphalt (the GFP cracking value)

#### Annual change by cracking level

2024 offset removed.

| Midpoint cracking (%) | Route-clean miles | Mean pts/yr | Median | Extent-clean miles | Mean pts/yr | Median |
|---|---|---|---|---|---|---|
| ≤0.5 | 143 | 0.11 | 0.44 | 255 | 0.08 | 0.06 |
| 0.5–2 | 393 | 0.46 | 0.87 | 887 | 0.50 | 0.76 |
| 2–5 | 132 | 1.92 | 2.25 | 886 | 1.55 | 1.66 |
| 5–10 | 235 | 2.73 | 2.94 | 612 | 2.75 | 2.50 |
| 10–20 | 365 | 4.53 | 4.31 | 1,058 | 3.62 | 3.83 |
| 20–35 | 211 | 4.23 | 4.11 | 490 | 4.75 | 4.68 |
| >35 | 32 | 5.30 | 3.03 | 40 | 5.46 | 3.92 |

The average is 2.23–2.59 pts/yr (t = 8–14). The level dependence survives the regression-to-the-mean check (independent 2023 level: slope 0.12–0.13 vs 0.13–0.18 on the midpoint).

#### Functional forms

Cross-validated RMSE, points:

| Form | Route-clean | Extent-clean |
|---|---|---|
| Constant rate | 3.80 | 3.15 |
| Linear in level | 3.78 | 3.04 |
| Exponential | 4.94 | 4.65 |
| Logistic (constant logit rate k = 0.27–0.29/yr) | 3.65 | 3.11 |
| **Square root: `dC/dt = c₁·(C/10)^p`** | **3.56** | **2.95** |

Fitted square-root parameters:

| Sample | c₁ | p |
|---|---|---|
| Route-clean | 3.01 (90% 2.74–3.31) | 0.49 (0.40–0.57) |
| Extent-clean | 2.68 (2.53–2.86) | 0.53 (0.47–0.62) |

With p ≈ 0.5 this is `dC/dt ≈ 0.85·√C`, i.e. **√C rises by a constant 0.42/yr (extent; 0.48 route): C(t) = (√C₀ + 0.42·t)²**. It is simple, closed-form, bounded in practice and has no level-dependent bias across the bands. The logistic form under-predicts above 20% by 1.5 points over two years.

**Years to the MAP-21 thresholds** (extent fit):

| From | → 5% (loses Good) | → 10% | → 20% (Poor) | → 35% |
|---|---|---|---|---|
| 0.5% | 3.8 | 6.0 | 9.0 | 12.4 |
| 1% | 3.0 | 5.2 | 8.3 | 11.6 |
| 2% | 2.0 | 4.2 | 7.3 | 10.6 |
| 5% | — | 2.2 | 5.3 | 8.6 |

#### Inventory fields

- Level-adjusted excess, extent-clean: nothing significant for system, NHS, AADT or district except District 7 (+0.8) and truck ADT >3k (−0.43).
- The route-clean sample shows Interstates / NHS / AADT >20k cracking slower at the same level, but adding any block makes cross-validation *worse* (+1% to +17%).
- The high-volume system is built and maintained differently; the inventory fields proxy for structure, not load.

#### Against the current engine

- The engine moves `current_crack`, which is FHWA cracking (`crack_source = 'fhwa'`), by the dTIMS `crack_factor` 0.15 / 0.37 / 0.56 %/yr. Those factors were built for dTIMS **Percent_Cracking**.
- Observed Percent_Cracking does grow ~0.64–0.81 %/yr, so the factors are right for that measure. On FHWA cracking the engine is **~0.5 vs 2.2–2.6 %/yr**, and 3–7× too slow above 5%.

### 4.3 Percent_Cracking (dTIMS PCRK), asphalt — reference

| Item | Value |
|---|---|
| Average rate | 0.64–0.81 %/yr |
| Square-root fit | `dC/dt = 1.82·(C/10)^0.50` (≈ 0.58·√C, √C +0.29/yr) |
| Logistic fit | k = 0.23–0.24 |
| Level-adjusted excess, County / non-NHS / AADT < 3k | +0.15 to +0.27 %/yr |
| Level-adjusted excess, AADT > 20k | −0.13 |

Only relevant if a config uses `crack_source = 'dtims_percent'`. GFP (MAP-21) is on FHWA cracking.

### 4.4 Rut on asphalt

Constant-rate fit: **−0.004 in/yr (route, t −1.7) and −0.005 (extent, t −4.7)**. The 2024 offset is −0.021 / −0.017 in (t −7 / −15).

Annual change by rut level (extent-clean):

| Midpoint rut (in) | ≤0.10 | 0.10–0.15 | 0.15–0.20 | 0.20–0.25 | 0.25–0.30 | 0.30–0.40 | >0.40 |
|---|---|---|---|---|---|---|---|
| in/yr | −0.003 | −0.006 | −0.006 | −0.008 | −0.018 | −0.020 | −0.004 |

- The apparent downward trend with level is regression to the mean: with the midpoint or the independent 2023 level the slope is 0 (t 0.4–0.8).
- The 2020–22 files agree: +0.002 to +0.003 in/yr.
- Inventory effects are all under 0.01 in/yr: NHS / Interstate −0.005, District 4 +0.004.
- Recently paved extents: +0.007 in in year 1, then ~0.

**Rut on WVDOT asphalt is set by the mix and the last treatment and doesn't grow measurably over 1–5 years.** Model it as a level reset by the treatment plus an early-life densification step.

Growing it +0.022 in/yr (current engine) adds 0.2 in in 10 years and walks 0.2-in pavement into Poor (0.4) by the clock alone. On the validation extents, the engine-style rut growth cut rut-Good from 72.8% to 59.8% in 2.26 years; the survey says 74.9%.

### 4.5 Concrete (JCP; CRC has no clean pairs)

| Sample | Miles | IRI level | IRI in/mi/yr | FHWA crack %/yr | Faulting in/yr |
|---|---|---|---|---|---|
| 2023–25 JCP, extent-clean | 134 | 98 | +1.5 (se 0.8) | +0.15 (se 0.10) | n/a (vendor zeros) |
| 2023–25 JCP, route-clean | 11 | 111 | ≈0 (se 3.2) | +0.23 | +0.008 (se 0.006) |
| 2020–22 PCC, extent-clean | 210 | 88 | +2.9 (se 1.9) | +0.50 (se 0.38) | **+0.003 (se 0.0005)** at 0.029 in |
| 2020–22 PCC, route-clean | 84 | 80 | +4.8 (se 3.2) | +0.37 | +0.002 |

- The concrete network is small: 332 mi JCP and 106 mi CRC surveyed (directional) in 2024, against 24,490 mi of asphalt.
- A linear model is enough:
  - IRI +3 in/mi/yr;
  - cracking +0.3 %/yr;
  - faulting +0.003 in/yr (from 0.03 in it takes ~23 years to reach 0.10).
- Refit when the vendor's concrete faulting is sorted out.

---

## 5. From route averages to Good / Fair / Poor

GFP is rated per 0.1-mi record and needs *two* Poor metrics for Poor. A route average can't be rated directly: a route averaging IRI 120 still has records above 170. Three ways to turn the route-level models into a rating were tested against the observed 2023→2025 change on **259 route-clean asphalt extents, 715 mi, median 2.26 years**. Every row starts from the same 2023 records; lane-mile weighted.

| Model | % Good | % Poor | IRI %G | IRI %P | Crack %G | Crack %P | Rut %G |
|---|---|---|---|---|---|---|---|
| 2023 observed | 32.1 | 15.4 | 39.3 | 32.8 | 67.3 | 12.1 | 72.8 |
| **2025 observed** | **33.0** | **22.1** | **36.3** | **38.5** | **53.4** | **23.0** | **74.9** |
| A. Each record moves with its own level (IRI log-log, cracking logistic, rut held) | 30.9 | 20.3 | 39.5 | 38.4 | 60.9 | 20.6 | 72.8 |
| B. Route mean moves by the model; every record scales with it | 30.5 | 20.2 | 38.8 | 38.6 | 61.0 | 20.8 | 72.8 |
| **F. Route mean moves; the within-route distribution comes from a library of route-years with that mean; records keep their rank** | 29.4 | **21.6** | 39.2 | 39.9 | **55.6** | **21.4** | 72.8 |
| C. Constant rates (+14.7 in/mi/yr, +2.6 %/yr) | 0.0 | 19.7 | 24.5 | 43.2 | 0.0 | 17.2 | 72.8 |
| D. No change | 32.1 | 15.4 | 39.3 | 32.8 | 67.3 | 12.1 | 72.8 |
| E. A + engine rut (+0.022 in/yr) | 25.8 | 21.5 | 39.5 | 38.4 | 60.9 | 20.6 | 59.8 |

- **Level-dependent models reproduce the GFP shift; constant rates are badly wrong.** A constant IRI rate sends every smooth record over 95.
- **Record-level and route-level application (A vs B) give the same answer**, so a multiplicative route-level rate can be applied to each segment's own value.
- **Cracking initiation needs the distribution.** A 0.1-mi record jumps from 0 to over 5% in one step. The route mean creeps up smoothly, but the share over 5% jumps. Quantile mapping (F) fixes most of that (crack-Good 55.6 vs 53.4 observed) and still uses route averages only.
- Observed % Good didn't fall (32.1 → 33.0) although IRI-Good and crack-Good both fell. The records that newly failed were mostly ones that were already not Good for another reason, which F reproduces best of the models (29.4). Part of the 2023 → 2025 Good share is also rating noise across three metrics.

---

## 6. The current AMPS model against the observations

The engine side is from `scripts/engine_rates.py`:
- System default config; `load_analysis_segments_df` → `dtims_state.simulate` with no plan.
- 11,266 `analysis_segments` on the 380 routes of the clean 2023+ extents, 1,025 mi.
- 84% of those miles have no rehab year, so they start at the capped age 15.

Asphalt (BC) segments, first do-nothing year, against the route-clean observations in the same IRI bands:

| IRI band | Engine ΔIRI in/mi/yr | Observed | Engine Δrut in/yr | Observed | Engine Δcracking pts/yr | Observed FHWA |
|---|---|---|---|---|---|---|
| ≤95 | +5.0 | −1.2 to +0.9 | +0.029 | −0.017 | +0.27 | +0.56 |
| 95–120 | +5.4 | +2.6 to +9.0 | +0.024 | −0.003 | +0.50 | +0.79 |
| 120–170 | +6.3 | +6.3 | +0.024 | +0.005 | +0.53 | +2.97 |
| 170–250 | +7.8 | +13.3 | +0.022 | +0.006 | +0.55 | +3.49 |
| >250 | +22.2 | +52.8 | +0.019 | −0.008 | +0.56 | +3.80 |

**What this does to the outlook.** Engine GFP on these segments, % of miles:

| Year | Good | Poor |
|---|---|---|
| Start | 22 | 26 |
| 1 | 21 | 27 |
| 3 | 14 | 31 |
| 5 | 1.4 | 34 |
| 10 | 0 | 61 |

On clean routes the survey shows Good holding and Poor rising ~3 points/yr.

The engine's Good collapse comes from IRI growing +5/yr on smooth roads and rut growing on everything. Its Poor growth is too slow on rough roads (IRI and cracking both under-predicted above IRI 170 / 5% cracking).

Other engine behaviours seen:
- IRI is derived from PSI + a fixed offset, so its shape follows the PSI curve.
- The "OT" family (28 mi here, IRI ~400) doesn't deteriorate at all except cracking.
- Faulting never moves.

---

## 7. Recommendations

### 7.1 Data (before re-estimating anything)

1. **Ask the vendor about the 2022 Interstate records** (`COND_YEAR` 2019). Until then, don't treat them as 2022 condition, including in `condition_history` / the 2022 grid.
2. **Treat 2020–22 and 2023+ as different measurement systems** for cracking, rut and faulting. Get the vendor's crack-detection and rut-method change notes. If a bridge is wanted, have the vendor re-process a 2022 sample with the 2023 algorithm.
3. **Get concrete faulting** for 2023+ (a 0 on 50–63% of JCP records is not a measurement).
4. **Record the survey date per record** in one format. Model on dates, not file years (2024 spans nine months).
5. **Carry a 2024-survey offset** (rut −0.02 in) in any future calibration, or have the vendor explain the winter runs.
6. **Survey a fixed panel of low-volume routes every year** (as District 4 county roads were in 2023 and 2025). That panel is what makes the rate-vs-level curves identifiable.

### 7.2 Model structure (how each raw value should be modelled)

1. **Model the MAP-21 raw values directly and state-based:** the annual change is a function of the current value, per surface type. Don't derive them from index curves by age.
   - Untouched routes have no construction age (84% of the clean miles have no rehab year).
   - The level already carries the stage of life.
   - This is also how the data can be recalibrated every survey without an age.
2. **Asphalt IRI:** `dIRI/dt = 0.8 + 0.49·(IRI/100)^3.4`, integrated within the year (or the log-log equivalent with a 0.8 floor). Apply it multiplicatively to each segment's own IRI. Add a post-resurfacing hold of ~⅓ rate for 3 years.
3. **Asphalt FHWA cracking:** `C(t+1) = (√C(t) + 0.42)²`, i.e. √C +0.42/yr (0.48 on the county-heavy sample). The post-treatment starting value is ~0–1%. Report GFP either per segment, or from route means via the distribution library (F) so that initiation shows up.
4. **Asphalt rut:** held constant. The treatment sets it; add +0.01 in over the first 1–2 years after placement. No clock-driven growth.
5. **Concrete:** JCP/CRC IRI +3 in/mi/yr, cracking +0.3 %/yr, faulting +0.003 in/yr, all linear.
6. **Inventory splits:**
   - Keep separate models **by surface type**.
   - **Don't split rates by AADT, truck ADT, NHS or functional class.** They don't improve prediction once the level is known, and their apparent effects run the wrong way for load.
   - The one split the data supports is the **route group** (Interstate / HPMS_1 / other, §7a): Interstates run slower on IRI, cracking and rut, and other routes a little faster. A US-route IRI adder (+1 in/mi/yr) is the only other candidate.
   - Traffic still belongs in *treatment selection and cost*, not in the do-nothing rate.
7. **Validate any candidate model the way §5 does**: move the older survey's records forward and compare the rated distribution with the newer survey on untouched extents. It is cheap and it caught every failure mode here.

### 7.3 For AMPS specifically (proposals — nothing was changed)

The engine's condition contract is pinned: `dtims_state` is the only projector, and `tests/engine/test_dtims_state_replay.py` reproduces the dTIMS strategies to 1e-6. So these belong in a **new condition-model option on a config**, not an edit of the dTIMS path:
- raw-distress rate tables per surface (the parameters above, as config rows with a workbook `Sheet`, the config check, the Config page and docs, per `CLAUDE.md`);
- a rut hold;
- and, for the dTIMS path itself, the one clear inconsistency: the crack factor calibrated for Percent_Cracking is being applied to FHWA cracking. Either set `crack_source = 'dtims_percent'` on configs that keep the dTIMS factors, or scale the factors for FHWA cracking.

---

## 7a. Where the fits sit in the config's pavement classes

This section answers "what pavement classes do these fit into".

### How config 1 ("WVDOT dTIMS (default)") classes pavement

**18 families** = pavement type × rehab type × truck load (`pavement_family_rules`, `segment_families`):

| Axis | Values | Source |
|---|---|---|
| Pavement type | **BC** asphalt, **RC** concrete (JCP/CRC), **OT** other/unknown | surface type |
| Rehab type | **Initial**, **Minor**, **Major** | the segment's latest CLOSED project (no project → Initial) |
| Truck load | **H** = coal route or trucks ≥ 10%, else **L** | inventory |

The cracking factor has its own **route group**:

| Route group | Crack factor (%/yr) |
|---|---|
| INTERSTATE | 0.15 |
| HPMS_1 | 0.37 |
| Everything else | 0.56 |

Each clean pair was tagged with the family covering most of its extent. The median extent is 98–100% one family. Rates are compared with what the pooled level-only model predicts (script `scripts/families.py`, output `results/family_excess.csv`).

### Where the clean data falls

Asphalt pairs, miles averaged:

| Family | Network miles (config 1) | Route-clean | Extent-clean | Coverage |
|---|---|---|---|---|
| BC_Initial_L | 15,690 | 1,123 | 3,014 | good |
| BC_Initial_H | 1,753 | 171 | 665 | good (extent) |
| BC_Minor_L | 4,188 | 136 | 358 | fair |
| BC_Minor_H | 693 | 17 | 112 | thin |
| BC_Major_L | 886 | 49 | 62 | thin |
| BC_Major_H | 67 | 0 | 0 | none |
| RC_Initial_L / RC_Initial_H / RC_Minor_* | 289 / 52 / 61 | 13 | 96 | thin (§4.5) |
| OT_* | 253 | 31 (mixed surface) | 33 | none usable |

The fitted curves in §4 are therefore **BC_Initial curves** (88–93% of the clean miles), with some BC_Minor.

"Initial" on an untouched road means *no closed project on record*, i.e. unknown age, usually old. It does not mean newly built. Every family's pavement type agreed with the survey surface on the pairs (ASP → BC, JCP → RC).

### Do the family axes change the rate once the level is known?

Excess annual rate over the pooled level model, 90% route-bootstrap interval. Bold = interval excludes 0.

| Class | IRI in/mi/yr (route / extent) | FHWA cracking pts/yr (route / extent) | Rut in/yr (route / extent) |
|---|---|---|---|
| Truck H | −1.7 / −0.5 | **−0.58** / +0.10 | −0.003 / **−0.004** |
| Truck L | +1.0 / +0.4 | 0.0 / 0.0 | 0.000 / 0.000 |
| Rehab Initial | +0.9 / +0.4 | −0.16 / −0.02 | −0.001 / −0.001 |
| Rehab Minor | −1.2 / **−1.3** | +0.67 / +0.38 | +0.004 / +0.001 |
| Rehab Major | +0.8 / −1.1 | −0.44 / −0.42 | +0.007 / +0.005 |
| **Route group INTERSTATE** | **−4.0 / −2.7** | **−0.95 / −0.36** | **−0.010 / −0.005** |
| Route group HPMS_1 | −1.0 / +0.1 | −0.18 / **−0.42** | 0.001 / **−0.003** |
| **Route group OTHER** | **+2.1 / +1.2** | +0.16 / **+0.25** | 0.002 / 0.002 |

- **Truck load (H/L) doesn't separate deterioration.** High-truck asphalt deteriorates no faster, and slower on cracking in one sample, at the same level. The H/L split is not supported as a do-nothing rate driver.
- **Rehab type matters a little, and only as early life.** Minor-rehab segments roughen ~1.3 in/mi/yr slower than their IRI predicts, which matches the post-overlay hold in §4.1. Major has too few miles to say.
- **The route group is the class that separates.** Interstates deteriorate slower on all three values; everything else (non-Interstate, non-HPMS) deteriorates a bit faster. This is the same ordering as the dTIMS cracking factors, so the split to keep is Interstate / HPMS / other, not truck load.

### Class-specific parameters

Asphalt, **BC_Initial and BC_Minor by route group**. Cracking: √C slope, C(t) = (√C₀ + s·t)². IRI: `dIRI/dt = c₀ + c₁·(IRI/100)^3.4`.

| Route group | √C slope s /yr (90%) | IRI model | Observed IRI range (p10–p90) |
|---|---|---|---|
| INTERSTATE | 0.20 route (−0.14–0.47), **0.35 extent (0.22–0.43)** | flat: observed −1.4 to −2.3 in/mi/yr at IRI ~65 (curve not identifiable in that narrow range) | 53–76 |
| HPMS_1 | 0.52 route (0.39–0.66), **0.37 extent (0.31–0.43)** | pooled curve (c₀ ≈ 0, c₁ 1.1–1.7), fits within noise | 64–176 |
| OTHER | **0.46–0.48 (0.43–0.53)** | c₀ = +2.0 to +2.7, c₁ = 0.45–0.46 | 97–414 |
| All (pooled) | 0.43–0.47 | c₀ = 0.8, c₁ = 0.47 | 70–410 |

Years from 1% to the cracking thresholds by route group (extent slopes):

| Route group | → 5% (loses Good) | → 20% (Poor) |
|---|---|---|
| Interstate | 3.5 | 9.9 |
| HPMS_1 | 3.3 | 9.4 |
| Other | 2.7 | 7.5 |

The dTIMS factors put Interstate cracking at ¼ of "other" (0.15 vs 0.56). The survey puts it at ~¾ in √C terms, and at ~⅓ in points per year only because Interstates sit at low cracking.

**No clean-data fit exists** for BC_Major_H, any OT family or RC_Major/Minor. Use the pooled BC curve for BC_Major (with the early-life hold), the §4.5 linear JCP rates for all RC families, and treat OT as its surface is resolved (most "OTH" records are asphalt-like county surfaces; 2024 has 287 mi).

**Recommended class structure for a raw-distress model:**
- **surface** (BC / RC) × **route group** (Interstate / HPMS_1 / other) for the rate curves;
- **rehab type** only as the post-treatment hold (the first ~3 years);
- **drop truck load** as a deterioration axis. Keep it for treatment cost and selection if wanted.

---

## 8. Limits

- **Short horizon.** Intervals are 0.9–2.3 years (the 2023+ files are the only consistent distress series). Long-run shapes are the integrals of short-run rates, not observed trajectories. Re-estimate with 2026.
- **Sample.**
  - The route-clean sample is 64% county routes, two-thirds of them in District 4 (the county roads surveyed in 2023 and 2025).
  - The extent-clean sample covers the NHS / US / Interstate network, but only on stretches away from work.
  - Results agree between the two for IRI, cracking and rut.
- **Survivorship.** Untouched routes are the ones that didn't need work. Later-treated routes ran +1–4 in/mi/yr IRI and +0.2–0.4 %/yr cracking faster than their level predicts (§4.1).
- **Unrecorded work.** County-forces paving before OM (July 2024) and any work not in TheHub can't be masked. Negative changes on smooth routes are partly that. Medians are shown next to means throughout.
- **Inventory is today's LRS** (the 2026 overlay), not the AADT in the survey year.
- **Milepoints are the vendor's.** Route-average comparison over the common span is insensitive to small shifts, but a route whose vendor milepoints moved a lot between years would average slightly different pavement. The ≥0.5 mi minimum and the ≥90% surface-agreement rule limit that.

---

## 9. Reproducing

Run from the repo root with the venv and the DB / TheHub tunnels up (`./start-dev.sh`). Everything is read-only.

```sh
export STUDY_DIR=/tmp/raw-deterioration-study          # working files (parquet) go here
S=dtims_docs/raw-deterioration-study-2026-09-29/scripts
python $S/load_raw.py            # vendor files ~/Downloads/csvs/<YYYY>.csv -> raw_records.parquet
python $S/pull_hub_mms.py        # TheHub projects + MMS work lines
python $S/build_pairs.py         # route-average pairs, work masks, inventory attributes
python $S/forms.py               # rate-by-level tables and functional forms      -> results/forms_out.txt
python $S/covs.py                # inventory covariate blocks                     -> results/covs_out.txt
python $S/multipliers.py         # level-adjusted excess rates by group           -> results/multipliers.csv
python $S/nls.py; python $S/nls_cv.py   # floor+power / square-root fits, bootstrap, CV
python $S/gfp_validate.py        # GFP validation (models A–F)                    -> results/gfp_validate.csv
PYTHONPATH=. python $S/engine_rates.py  # current engine, do-nothing (needs clean_new_era_extents.csv from build step)
```

`statsmodels` isn't in the project venv. It was installed into a separate target folder for this study; `pip install statsmodels` does the same. `build_pairs.py` also writes `clean_new_era_extents.csv` (route-clean pairs with `y1 >= 2023`), which `engine_rates.py` reads.
