# dTIMS STIP 2026 NHS scenario vs PMS run #275: comparison

**Date:** 2026-09-24

**Files compared**

| | File | What it is |
|---|---|---|
| **dTIMS** | `2026 04 27 ALL Network NHS Construction Program - DEL_STIP_2026_NHS_ONLY_NO_INTERSTATES_Budget_Scenario.xlsx` | dTIMS analysis set `DEL_STIP_2026_NHS_ONLY_NO_INTERSTATE`, budget scenario `…_Budget_Scenario`, exported 2026-04-27. 382 treatment records, 2026–2038 |
| **PMS** | `work_program_20260924_215151.xlsx` | PMS run #275, *Re-run of #272 on corrected network lengths (v1.4.1)*. MILP-assist, NHS without interstates, 12 years, 901 projects, 2026–2037 (PMS year 1 = 2026) |

The dTIMS workbook has two sheets. **Data (2)** holds exactly the same 382 rows as **Data**, in a different order, plus two pivot tables (cost by treatment × year and by district × year). Its `Comments` column is empty. Everything below uses **Data**.

## Summary

1. **The money is the same, but it is spent very differently.** Both programs spend about $50M in 2026 and about $60M a year after that. Over the 12 years both cover (2026–2037), dTIMS spends **$706.2M** and PMS **$709.1M**. dTIMS adds a 13th year (2038, $58.9M), for $765.1M in total.
2. **Most of the dTIMS program is the STIP. None of the PMS run is.**
   - 329 of the 382 dTIMS records (**$646M, 84% of the money**) are `IsCommitted`. Their year and treatment match `Com_Year` and `Com_Trt` 98–99% of the time, so dTIMS optimises only the remaining **53 projects ($119M)**.
   - PMS run #275 had **no committed projects**: `is_committed` is 0 on the whole network. Every dollar was optimised freely.

   This is the single biggest reason the two programs differ.
3. **PMS treats about 1.8× the miles for the same money:** 1,741 mi against 976 mi for dTIMS in 2026–2037. Three things account for it:
   - **Ultra-thin overlays.** PMS uses 244 of them (614 mi for $69M, about $112k per mile). The dTIMS scenario uses none.
   - **Concrete repair.** PMS applies Major CPR / diamond grind to jointed and CRCP pavement: 179 projects, 294 mi, $80M. dTIMS has 8 Minor CPR projects covering 33 mi.
   - **Both directions of divided roads.** PMS includes the SB and WB routes (354 mi, $94M). dTIMS carries only the primary direction (`00`, `NB`, `EB`).
4. **Similar places, but different years.**
   - PMS treats **97%** of the dTIMS miles at some point in its 12 years.
   - Only **7%** are treated by both in the **same year**, 21% within ±1 year and 31% within ±2 years.
   - The year differences run both ways: of the overlapping section-to-project miles, PMS is earlier on 513, later on 415 and the same year on 71. PMS is not simply ahead of or behind dTIMS.
5. **2026 looks nothing alike.**
   - dTIMS: the 14 STIP projects (47.6 mi, $49.8M), including two reconstructions ($12.6M).
   - PMS: 143 projects on 421 mi, 135 of them ultra-thin overlays (411 mi). It uses year 1 for cheap preservation on roads still in good condition.

## Program by year

dTIMS "committed" is the part of each year's dTIMS money that belongs to `IsCommitted` projects.

| Year | dTIMS projects | dTIMS mi | dTIMS cost | of which committed | PMS projects | PMS mi | PMS cost |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2026 | 14 | 47.6 | $49.8M | $49.8M | 143 | 421.3 | $50.0M |
| 2027 | 45 | 102.3 | $59.6M | $53.3M | 91 | 167.9 | $60.0M |
| 2028 | 37 | 86.3 | $59.8M | $53.6M | 86 | 147.8 | $59.9M |
| 2029 | 34 | 95.6 | $59.9M | $51.9M | 75 | 142.0 | $59.9M |
| 2030 | 33 | 92.4 | $59.7M | $53.9M | 72 | 121.1 | $59.9M |
| 2031 | 33 | 90.2 | $59.3M | $53.6M | 65 | 110.1 | $59.7M |
| 2032 | 35 | 87.8 | $59.9M | $52.4M | 59 | 102.4 | $59.9M |
| 2033 | 29 | 87.3 | $59.9M | $49.3M | 68 | 112.1 | $60.0M |
| 2034 | 28 | 82.1 | $59.4M | $51.7M | 58 | 99.7 | $60.0M |
| 2035 | 27 | 80.5 | $59.9M | $48.3M | 65 | 109.7 | $60.0M |
| 2036 | 27 | 66.9 | $59.4M | $44.8M | 46 | 96.6 | $59.8M |
| 2037 | 22 | 56.5 | $59.5M | $46.2M | 73 | 110.6 | $60.0M |
| 2038 | 18 | 51.6 | $58.9M | $37.1M | — | — | — |
| **2026–2037** | **364** | **975.5** | **$706.2M** | | **901** | **1,741.4** | **$709.1M** |
| **All years** | **382** | **1,027.1** | **$765.1M** | **$646.0M** | | | |

In PMS, projects are about half as big and about twice as many: median length 1.65 mi against 2.36 mi for dTIMS. 46 PMS projects are shorter than the run's 0.25-mile minimum project length. They are leftover pieces of joints, the smallest 0.0 mi.

## Treatments

| dTIMS treatment | Projects | Miles | Cost | $/mi |
|---|---:|---:|---:|---:|
| Thick overlay | 329 | 860 | $657.1M | $764k |
| Thin overlay | 36 | 101 | $56.5M | $557k |
| Minor CPR / diamond grind | 8 | 33 | $16.2M | $487k |
| PM microsurfacing | 6 | 27 | $14.1M | $527k |
| Reconstruction | 2 | 6 | $20.6M | $3.72M |
| Preservation | 1 | 0.15 | $0.65M | — |

| PMS treatment | Projects | Miles | Cost | $/mi |
|---|---:|---:|---:|---:|
| Thick overlay | 468 | 821 | $554.6M | $675k |
| Ultra-thin overlay | 244 | 614 | $69.0M | $112k |
| Major CPR / diamond grind | 179 | 294 | $79.8M | $272k |
| Thin overlay | 10 | 13 | $5.7M | $445k |

- **Thick overlay dominates both**: 86% of dTIMS money and 78% of PMS money. PMS's thick overlays cost about 12% less per mile. PMS prices 2 lanes at $300k per lane-mile, inflated 2% a year. dTIMS gives one lane per record and no usable lane count (`Lanes_Total` is blank on 333 of 382 rows).
- **PMS picked no reconstruction or microsurfacing, and few thin overlays** (10, all in 2026–2027). Instead, PMS covers much more road with ultra-thin overlays and CPR.
- **Where both treat the same stretch**, whatever the year:

| dTIMS picked | PMS picked | Miles |
|---|---|---:|
| Thick overlay | Thick overlay | 580 |
| Thick overlay | Ultra-thin overlay | 184 |
| Thick overlay | Major CPR | 66 |
| Thin overlay | Thick overlay | 58 |
| Thin overlay | Ultra-thin overlay | 38 |
| Minor CPR | Major CPR | 29 |
| Microsurfacing | Ultra-thin overlay | 20 |

## Network coverage

| | dTIMS | PMS |
|---|---|---|
| Routes | 93 | 190 (89 in common) |
| Directions | Primary only: `00` 154 records, `NB` 132, `EB` 96 | Both: `NB` 487 mi, `EB` 431, `00` 468, **`WB` 196, `SB` 158** |
| Sign systems (records / projects) | US 228, WV 150, County 2, Federal-aid non-state 2 | US 623, WV 266, County 8, Federal-aid non-state 4 |
| Surface | Asphalt 373, JCP 9 | Asphalt 776, Jointed 106, CRCP 19 |
| PMS miles on dTIMS locations | | 981 of 1,741 mi (56%) |

- The PMS filter is NHS (`nhs_code > 0`) with interstates and one special route series excluded. The dTIMS analysis set is "NHS only, no interstates". The scopes are close, but **PMS treats each direction of a divided highway as its own route** and dTIMS does not.
- Of PMS's 760 miles away from dTIMS locations, 354 are the SB/WB directions. The rest is on 101 routes (or parts of routes) that dTIMS never treats.

## By district

| District | dTIMS mi | dTIMS cost | PMS mi | PMS cost |
|---|---:|---:|---:|---:|
| 1 | 151.4 | $104.1M | 209.3 | $93.2M |
| 2 | 150.2 | $111.2M | 260.9 | $124.8M |
| 3 | 74.3 | $62.0M | 124.4 | $39.0M |
| 4 | 55.3 | $52.7M | 133.3 | $60.6M |
| 5 | 115.6 | $79.9M | 220.7 | $67.8M |
| 6 | 134.5 | $90.3M | 164.3 | $89.4M |
| 7 | 12.0 | $12.9M | 68.2 | $20.2M |
| 8 | 106.1 | $69.7M | 154.9 | $48.2M |
| 9 | 87.7 | $76.6M | 182.5 | $77.1M |
| 10 | 140.0 | $105.7M | 222.8 | $88.8M |

dTIMS figures are for all 13 years; PMS figures are for 12. PMS spends more in **Districts 2, 4 and 7** and less in **Districts 1, 3, 5, 8 and 10**, and treats more miles in every district. District 7 gets only 12 miles in dTIMS against 68 in PMS.

## Condition at selection (dTIMS)

The dTIMS rows carry the section's condition:

| dTIMS treatment | Mean CCI | Mean PSI | Mean IRI |
|---|---:|---:|---:|
| Thick overlay | 2.79 | 3.24 | 111 |
| Thin overlay | 3.22 | 3.41 | 97 |
| Microsurfacing | 3.47 | 3.76 | 72 |
| Minor CPR | 3.10 | 3.10 | 119 |
| Reconstruction | 2.71 | 2.75 | 152 |

- Thick overlays go to Fair roads on average: CCI 2.79, just under the 3.0 Good line.
- The PMS export has no condition columns. PMS run #275 starts at 66.8% Good / 13.8% Poor on its network. It ends 2037 at 73.4% Good / 7.1% Poor, which meets its ≤ 10% Poor target but misses its ≥ 90% Good target.
- The dTIMS file has no network condition trajectory, so the outcomes can't be compared directly.

## Why they differ, most important first

1. **STIP commitments.** dTIMS locks 84% of its money into STIP projects at fixed years and treatments. PMS had none loaded, so it was free to reschedule everything. This alone explains most of the year disagreement.
2. **Treatment menu and unit costs.** PMS can use the ultra-thin overlay (about $55k per lane-mile) and Major CPR (about $120k per lane-mile), and its MILP targets network % Poor / % Good. So it spreads money over many more miles of lighter work. The dTIMS scenario mostly buys thick overlays.
3. **Network definition.** PMS includes both directions of divided highways and more jointed/CRCP pavement, adding about 350+ miles of candidates that dTIMS doesn't have.
4. **Horizon.** 12 years in PMS against 13 in dTIMS.
5. **Data vintage.** The dTIMS file is from April 2026. PMS runs on the 2025 survey, conflated on roads2, with the corrected segment lengths from the 2026-09-24 refresh.

## To make a like-for-like comparison

- **Load the same STIP commitments into PMS**, either from TheHub or from this file's `Com_Trt` / `Com_Year`, and re-run. PMS would then optimise only the same ~$119M that dTIMS does.
- **Match the scope:** either restrict PMS to the primary direction (`00` / `NB` / `EB`), or confirm dTIMS's one-lane records are meant to stand for both directions.
- **Match the treatment menu:** turn ultra-thin overlay and Major CPR off in PMS, or add them to the dTIMS scenario, to see how much of the mileage gap comes from treatment choice alone.
- **Run PMS for 13 years** (2026–2038).
- **Compare in the same units:** cost per lane-mile, using the same lane counts in both.

## Method

- **dTIMS records** use `RoadName`, `From`, `To`, `Year`, `Treatment`, `Cost` and `Length` from sheet **Data**.
- **PMS projects** use `Route`, `Begin MP`, `End MP`, `Year` (+2025), `Treatment`, `Cost` and `Miles` from sheet **All Projects**.
- **Location overlap** is the milepoint overlap on the same 13-character route ID, counting only overlaps over 0.01 mi. A dTIMS section can overlap several PMS projects.
