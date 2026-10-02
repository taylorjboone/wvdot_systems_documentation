# Raw Distress Study — how it was done

**Study date:** 2026-09-29.

The study answers three questions:
1. How do the raw values behind MAP-21 Good / Fair / Poor (IRI, FHWA cracking, rut, faulting) deteriorate on WVDOT pavement?
2. What does each treatment do to them?
3. What treatment strategy and order does that imply?

It was worked out from the raw vendor survey, TheHub and MMS, independent of the dTIMS index model. The findings are in three reports:

| Report | Question |
|---|---|
| [Raw distress deterioration](/docs/Pavement_Raw_Distress_Deterioration) | How IRI, cracking, rut and faulting deteriorate, what drives the rate, which pavement classes they fall into, and how AMPS's model compares |
| [Treatment resets](/docs/Pavement_Treatment_Resets) | What each TheHub treatment does to the four raw values, by surface and class, and how config 1's resets compare |
| [Treatment strategies](/docs/Pavement_Treatment_Strategies) | What WVDOT actually does, which strategy and order the curves and resets favour, under a budget, and how config 1's triggers compare |

This page records **how** the study was done, step by step, so it can be rerun (e.g. when the 2026 survey arrives) and checked. The scripts and their outputs are in `dtims_docs/raw-deterioration-study-2026-09-29/` (`scripts/`, `results/`). Nothing in the engine, the configs or the database was changed by the study.

---

## 1. Ground rules

**Raw, not re-conflated, data.** The vendor's `<YYYY>.csv` files (0.1-mi records with the vendor's own milepoints) are used as delivered. The pipeline's re-conflation (`reconflate_normalized`, `analysis_segments`) is not used for condition, because it moves each record onto the LRS and mixes neighbours.

**Route averages, not record-to-record matching.** Vendor milepoints drift between years, so matching 0.1-mi records 1-1 mixes location error into the change. Every comparison between two surveys is between **route averages over the same milepoint span**:
1. take the overlap of the two years' vendor milepoints on the route;
2. drop bridge / construction / lane-deviation / wet / railway records;
3. average what's left in each year.

**"Untouched" comes from TheHub (and MMS).** A route or stretch counts as untouched between two surveys only when no TheHub project and no MMS paving / patching line touched it in that window. Two definitions are kept side by side:
- **route-clean:** nothing anywhere on the route;
- **extent-clean:** work masked out with a 0.3-mi buffer.

Results were accepted only where both agreed.

**Time is survey dates, not file years.** The 2024 survey ran April 2024 – January 2025, so the interval between two surveys is 0.9–2.3 years.

**Read-only throughout.** The database is read through `api.database`, TheHub through `api.hub_client`, MMS (OM) through the `[TAMSDW]` linked server. The engine was only called to measure what it predicts (do-nothing steps, resets, triggers); nothing was written.

---

## 2. Process

### Step 1 — Load the raw survey (`load_raw.py`)

- Reads the six vendor files 2020–2025 (`SURVEY_DIR`, default `~/Downloads/csvs`) into one record table.
- Keeps route, vendor milepoints, survey date, surface type, the event flags (`BRIDGE`, `CONSTR`, `LANEDEV`, `WET`, `RAILWAY`, `IRI_FLAG`, `RUT_FLAG`), IRI, rut, FHWA and dTIMS cracking, faulting, the vendor indices and patching.
- −1 means not measured.
- Dates: 2023 mixes Excel serials, ISO and d/mm/yyyy; missing dates get the file's median.

**What profiling the files turned up** (details in the deterioration report §3):

| Finding | Evidence |
|---|---|
| Coverage | 2020–22 and 2023 / 2025 cover 250–1,000 routes; only 2024 covers all 15,124 |
| **Vendor or method change between 2022 and 2023** | FHWA cracking ×4, rut steps up ~0.05 in, faulting goes to 0 on the same routes |
| **The 2022 Interstate records are the 2019 survey** | `COND_YEAR` 2019; 10–11 in/mi smoother than 2020 and 2021 at the same milepoints |
| **2024 is offset** | winter runs: rut reads ~0.02 in low |
| **2023+ faulting is unusable** | zeros on most JCP |

The consequences for everything that follows:
- Distress (cracking, rut, faulting) is compared only within one vendor era: 2020–22 or 2023–25.
- Models carry a 2024 offset term.
- Rates are anchored on 2023 → 2025.

### Step 2 — Pull the work that disqualifies a stretch (`pull_hub_mms.py`)

- **TheHub:** every project with a route segment (11,001 projects, 16,089 route segments), with status, work code, construction codes and the construction window.
  - Window start: milestone 18 actual → construction phase start → letting.
  - Window end: milestone 20 actual → construction phase end → expected completion.
- **MMS:** OM daily work lines for paving, skip patching, grinding, surface treatment / fog seal, PCC work and patching, with route and mileposts (48,218 lines).
  - OM starts in July 2024, so it only cleans 2024 → 2025.

### Step 3 — Build route-average pairs (`build_pairs.py`)

For every route and every pair of its survey years:
- **common extent:** at least 0.4 mi of overlap, and at least 5 records (0.5 mi) each year after flags and masks;
- **both years averaged** over the same extent;
- **work flags:** TheHub projects and MMS lines active in [survey 1 − 60 days, survey 2];
- **age since the last completed TheHub pavement project** covering ≥ 50% of the extent, where known;
- **inventory attributes** length-weighted from `analysis_segments`: NHS, functional class, AADT, single + combination truck ADT, truck %, district, coal route, lanes.

**Result:** 4,639 route pairs, 1,520 consecutive usable pairs, 807 route-clean. For asphalt, the 2023–25 set is:

| Sample | Pairs | Routes | Miles |
|---|---|---|---|
| Route-clean | 533 | 311 | 1,497 |
| Extent-clean | 808 | 453 | 4,213 |

### Step 4 — Deterioration forms per raw value (`prep.py`, `forms.py`, `nls.py`, `nls_cv.py`)

**How each candidate is fitted:**
- On the **change over the pair**: `Δ = Δt · (rate terms) + γ · off24`, where `off24` absorbs the 2024 offset.
- Level terms use the **midpoint** of the two years, to avoid regression to the mean.
- Weights are the miles; standard errors are clustered by route.
- Candidates are compared by **5-fold cross-validation grouped by route**, predicting the second year's level from the first.

**Candidates tried:**

| Raw value | Candidate forms |
|---|---|
| IRI | constant rate, constant % (exponential), linear in level, log-log (`d ln IRI/dt = a + b ln IRI`), floor + power |
| Cracking | constant, linear in level, exponential, logistic, logistic with level, square root (`dC/dt = c·C^p`) |
| Rut | constant, linear in level, exponential |

The parameters of the chosen forms (floor + power for IRI, square root for cracking) were bootstrapped by route. The **regression-to-the-mean check** re-fitted the rate-vs-level slope with the year-1 level, the midpoint, and an independent level (the 2023 value for 2024 → 2025 pairs).

**Other checks** (inline in the working session; their tables are in the report):
- **The three-survey triangle.** Routes clean in 2023, 2024 and 2025 were used to separate trend from the 2024 offset.
- **The 2020–22 files as a second era,** for IRI.
- **Young pavements:** extents with a known TheHub project 0–10 years before.
- **Later-treated routes,** for selection bias.

### Step 5 — Do the inventory fields matter? (`covs.py`, `multipliers.py`, `families.py`)

- **`covs.py`:** adds one block at a time to the best level form. The blocks are ln AADT, ln truck ADT, truck %, trucks per lane, NHS, Interstate, functional class, system, district, coal, lanes, AADT growth. Each is judged by a joint Wald test and the change in cross-validated error.
- **`multipliers.py`:** the level-adjusted excess rate by group (observed minus level-predicted), with 1,000 route-bootstrap intervals.
- **`families.py`:** tags each pair with config 1's pavement family (pavement type × rehab type × truck load) and the cracking route group (Interstate / HPMS_1 / other). It repeats the excess-rate test per class, and fits the cracking and IRI curves per route group.

### Step 6 — Can route-level models reproduce Good / Fair / Poor? (`gfp_validate.py`)

On 259 route-clean asphalt extents (715 mi, 2023 → 2025), the 2023 records are moved forward by each candidate and rated with MAP-21. The rated distribution is compared with the 2025 records of the same extents, distribution against distribution with no 1-1 matching.

Candidates:
- record-level;
- route-level shift;
- route mean plus a library of within-route distributions (quantile mapping);
- constant rates;
- no change;
- the engine's rut growth.

### Step 7 — The current AMPS model on the same ground (`engine_rates.py`)

- The `analysis_segments` of the clean extents were loaded with config 1 (`load_analysis_segments_df`).
- They were projected do-nothing with `dtims_state.simulate` (1, 3, 5 and 10 steps).
- The implied annual changes in IRI, rut, cracking and faulting were compared band by band with the observed rates.

### Step 8 — Treatment resets (`resets.py`, `resets_analyze.py`, `engine_resets.py`)

- **Projects:** every completed TheHub pavement project from 2015, with its construction code grouped into treatments (thin 08, thick 68, ultra-thin 67, surface treatment 13/14/59, micro 26, new / reconstruct 07/02/04/24/66, CPR 75).
- **Extent:** the project's milepoints, trimmed 0.1 mi at each end.
- **View A — before → after:** the last survey ≤ 4 years before construction started, against the first survey after completion. Pairs with other work between them are dropped, and distress is compared within one vendor era.
  - Result: 304 extents, 218 clean.
  - Reset form: `after = a + b·before`, fitted by weighted and median regression, to tell a full reset (b ≈ 0) from a partial one.
- **View B — after only:** every 2023–25 survey after completion, by age. The age-0 intercept is the reset level; the slope is early-life growth.
  - Result: 1,996 readings on 1,402 projects.
  - Split by surface, route group, truck load and family.
- **Composite check:** HMA overlays on extents that had concrete in an earlier survey. Too few (4) to conclude.
- **Engine comparison (`engine_resets.py`):** every active config 1 treatment was applied through the engine (`dtims_state.simulate(plan=…)` → `apply_treatments`) to ~61,000 segments, and the before → after raw values were compared with the observed resets.

### Step 9 — Strategies and order (`history.py`, `strategies.py`, `budget.py`, `engine_trigger_check.py`)

- **Observed practice (`history.py`)** from TheHub (4,571 project segments):
  - **what follows what:** the next / previous pavement project covering ≥ 50% of the extent, with the gap in years;
  - **time to the next project:** Kaplan-Meier, miles-weighted, for each treatment and by system;
  - **condition at selection:** the raw condition at the last survey ≤ 3 years before construction, by treatment and system.
- **Life-cycle simulation (`strategies.py`):**
  - Population: 2024 asphalt records, 3,000 per route group.
  - Models: the fitted deterioration curves, the observed resets, config 1 unit costs.
  - Nine rule sets over 30 years (do nothing, today's worst-first pattern, thin when Good is lost, seal-first, fixed cycles, ultra-thin-first, micro-first).
  - Reported: % Good / % Poor, cost per lane-mile-year, Good-years and Poor-years-avoided per $1M.
- **Budget order (`budget.py`):**
  - The network sample in proportion to lane-miles; each year's candidates from the decision tree.
  - Funded under $8k / $15k / $25k per lane-mile-year in three orders: worst-first, preservation-first, and benefit/cost (a 10-year look-ahead of Good-years gained plus Poor-years avoided, per dollar).
- **Trigger check (`engine_trigger_check.py`):**
  - Projects: 593 TheHub pavement projects not yet built, whose "before" state is today's `analysis_segments`.
  - The optimizer's own candidate generation (`engine.treatments.triggers.evaluate_triggers_segment_union_polars`) was evaluated for program year 1.
  - Checked: whether it would allow the treatment WVDOT chose, and which gate blocks it.

---

## 3. What came out (short)

| Topic | Result | Report |
|---|---|---|
| IRI (asphalt) | Rate rises with the current IRI: `dIRI/dt ≈ 0.8 + 0.49·(IRI/100)^3.4`; ~⅓ rate for 3 years after an overlay; traffic / NHS / class add nothing once the level is known | Deterioration §4.1 |
| FHWA cracking (asphalt) | **√C grows ~0.42/yr**: C(t) = (√C₀ + 0.42 t)²; 1% → 5% in ~3 yr, → 20% in ~8 yr | §4.2 |
| Rut (asphalt) | Doesn't grow on untouched pavement; set by the last treatment | §4.4 |
| Faulting (JCP) | +0.003 in/yr (2020–22 only) | §4.5 |
| Classes | Surface and route group (Interstate / HPMS / other) matter; truck load doesn't; rehab type only as the early-life hold | §7a |
| GFP | Level-dependent models reproduce the observed 2023 → 25 shift (Poor 21.6 vs 22.1%); constant rates don't | §5 |
| Resets | Overlays and seals take cracking to ~0 and rut to ~0.08 in; IRI resets partially (thin: `80 + 0.42·(IRI − 80)`, thick: `45 + 0.42·(IRI − 45)`); micro doesn't reset cracking | Resets §1 |
| Practice | Worst-first on the county system (thin overlays at IRI ~246, 48% Poor); preventive on Interstates; almost no seal cycle; ~36% of thin overlays re-treated within 10 yr | Strategies §2 |
| Strategy | Seal → seal → thin (~14-yr cycle) off the Interstate, thin every ~8 yr on it; fund by benefit/cost, not worst-first | Strategies §3–4 |
| AMPS today | IRI too fast on smooth / too slow on rough roads; rut grows by the clock; cracking grows 3–7× too slowly (dTIMS PCRK factors on FHWA cracking); resets never zero cracking and overwrite rut from RDI; RECONSTRUCT_RC sets pavement to BC; triggers allow WVDOT's chosen treatment on ~48% of its planned miles | Deterioration §6, Resets §4, Strategies §5 |

All of the config and engine suggestions are proposals. Changing the condition model would go through a new config condition-model option (config tables, workbook, config check, Config page, docs), not the pinned dTIMS path.

---

## 4. Rerunning

From the repo root, with the venv and the tunnels up (`./start-dev.sh`), and `statsmodels` installed (not in `requirements.txt`: `pip install statsmodels`). Working files (parquet) go to `STUDY_DIR`.

```sh
export STUDY_DIR=/tmp/raw-deterioration-study     # working files
export SURVEY_DIR=~/Downloads/csvs                # vendor <YYYY>.csv files
S=dtims_docs/raw-deterioration-study-2026-09-29/scripts

# 1-3  data
python $S/load_raw.py
python $S/pull_hub_mms.py
python $S/build_pairs.py
# 4-7  deterioration
python $S/forms.py; python $S/covs.py; python $S/multipliers.py
python $S/nls.py;   python $S/nls_cv.py; python $S/families.py
python $S/gfp_validate.py
PYTHONPATH=. python $S/engine_rates.py
# 8    resets
python $S/resets.py; python $S/resets_analyze.py
PYTHONPATH=. python $S/engine_resets.py
# 9    strategies
python $S/history.py
(cd $S && python strategies.py && python budget.py)
PYTHONPATH=. python $S/engine_trigger_check.py
```

**When the 2026 survey arrives:**
1. Add `2026.csv` to `SURVEY_DIR`, and extend the year range in `load_raw.py` and the era filters in `prep.py`.
2. Rerun everything.
3. The 2025 → 2026 and 2024 → 2026 pairs roughly double the clean sample, and give the first before → after resets for the projects built in 2025.
4. Check first that 2026 is the same vendor format as 2023–25; that decides whether the era rules still hold.

The saved outputs of the 2026-09-29 run are in `results/`:
- `forms_out.txt`, `covs_out.txt`, `multipliers.csv`, `family_excess.csv`, `gfp_validate.csv`;
- `resets_out.txt`;
- `history_out.txt`, `strategies.csv`, `budget_orders.csv`.
