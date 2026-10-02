# AMPS vs dTIMS: coverage of the 70 Percent Good Analysis runs

*2026-09-30 · AMPS runs 448, 449 and 445 (local) against WVDOT's 70 Percent Good Analysis (dTIMS, 2026-09-24)*

AMPS reproduced the three pavement scenarios of the 70 Percent Good Analysis with the dTIMS strategy optimizer, on dTIMS's analysis-set sections, with dTIMS's budgets and committed work. This report measures how much of each dTIMS program AMPS reproduces: spend by year, treatment by year, and section by section (same place, treatment and year).

## Summary

| | Interstates only | NHS non-Interstate, committed | NHS non-Interstate, no committed |
|---|---:|---:|---:|
| AMPS run | 448 | 449 | 445 |
| Spend, AMPS / dTIMS ($M) | 760.9 / 921.8 | 1,970.2 / 2,096.9 | 1,769.3 / 1,767.7 |
| Spend difference | -17.5% | -6.0% | +0.1% |
| Lane-miles treated, AMPS / dTIMS | 2,350 / 3,206 | 5,856 / 6,820 | 5,340 / 5,626 |
| dTIMS lane-miles: same treatment, same year in AMPS | 53% | 40% | 14% |
| dTIMS lane-miles: same treatment within ±2 years | 61% | 60% | 38% |
| dTIMS lane-miles: no AMPS work within ±2 years | 34% | 34% | 52% |
| Committed work: same treatment, same year | 98% | 98% | n/a |
| Other work: same treatment, same year | 18% | 18% | 14% |
| Other work: same treatment within ±2 years | 32% | 45% | 38% |

- **Committed work is reproduced.** 98% of dTIMS's committed lane-miles are the same treatment in the same year in AMPS; the rest is the joint / section boundary.
- **Spend follows dTIMS where nothing else differs.** Without committed work (run 445) AMPS spends within $2M of dTIMS every year. With it, AMPS underspends 2027–2030 on the Interstates and 2028–2033 on the NHS: it finds less worthwhile work than dTIMS in those years, not less budget.
- **The choices of where to work differ.** Outside committed work, only 14–18% of dTIMS's lane-miles get the same treatment in the same year in AMPS, and 32–45% within two years. The optimizer is the one that reproduced dTIMS's Non-NHS program from dTIMS's own starting state, so the difference is the starting condition: AMPS starts each joint from its own survey (raw network, joint average), per direction, where dTIMS starts a 2–5 mile section, and a divided road from its EB / NB survey only. Fair to Good, triggered by the MAP-21 rating, is the most sensitive to that.
- **Microsurfacing is a third to a half of dTIMS's** (lane-miles) on all three runs: AMPS does it 5–7 years after an overlay as dTIMS does, but chooses it less often.

dTIMS's Good / Fair / Poor export for these runs is unusable (one category at 100%), so condition is not compared; AMPS's % Good / Fair / Poor is shown for reference.

## How it was measured

- **Runs.** Config 408 (raw survey network, joint-average start, Nov–Dec 2024 County survey excluded, dTIMS treatment set and cracking for these analysis sets), dTIMS strategy optimizer (level 3, strategies two years past the run), dTIMS's yearly budgets, committed projects from dTIMS's network (run 445: none, as dTIMS's IncludeCommitted off), the 8 Interstate sections dTIMS's exclude rule leaves untreated held.
- **Network.** dTIMS's analysis set (its DEL_INTERSTATES / DEL_NHS filter evaluated: 446.09 / 1,410.62 mi, dTIMS's total measure). AMPS plans the raw-survey segments on those sections, on both directions where dTIMS counts both (`Lanes_Total` set, mostly Interstates); elsewhere dTIMS prices 2 lanes.
- **Lane-miles, not miles.** dTIMS carries a divided road once with both directions' lanes; AMPS carries each direction. Lane-miles (dTIMS: length × `Lanes_Total`, 2 when empty; AMPS: length × lanes) compare like with like.
- **Section matching.** Each dTIMS treatment's road (route and From / To milepoints, both directions where dTIMS counts both) is cut into 0.05-mile pieces; each piece takes the closest AMPS treatment on the same road: same treatment in the same year, ±1 year, ±2 years, another treatment in the same year or ±1 year, or nothing within ±2 years. Shares are weighted by dTIMS lane-miles. The reverse (AMPS's work against dTIMS's) is weighted by AMPS lane-miles.
- **Two AMPS totals.** The treatment tables add up the run's projects (each joint priced over its segments); the spend table is the run's yearly total. They differ by about 1% (Interstates $768.8M against $760.9M).

## Interstates only: AMPS run 448 vs dTIMS

dTIMS reference `pdf-2026-09-24-interstates`.

### Lane-miles treated by treatment and year (AMPS / dTIMS)

| Treatment | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2038 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Fair to Good | – | 90 / 113 | 10 / 1 | 8 / 39 | 17 / 31 | 103 / 94 | 45 / 14 | 45 / 24 | 61 / 37 | 79 / 58 | 100 / 109 | 35 / 93 | 18 / 82 | **611 / 693** |
| Thick overlay | 55 / 55 | 56 / 87 | 35 / 52 | 58 / 59 | 65 / 65 | 48 / 55 | 65 / 77 | 67 / 67 | 64 / 77 | 66 / 85 | 36 / 33 | – | – | **617 / 713** |
| Thin overlay | 17 / 26 | 19 / 33 | 9 / 9 | 40 / 40 | 46 / 48 | 62 / 68 | 41 / 49 | 33 / 21 | 5 / 29 | 11 / 15 | – | 0 / 9 | – | **284 / 348** |
| Microsurfacing | 116 / 124 | 69 / 130 | 76 / 76 | 99 / 102 | 50 / 50 | 95 / 142 | 17 / 111 | 45 / 138 | 0 / 27 | 27 / 32 | 68 / 54 | 99 / 199 | 64 / 244 | **825 / 1,429** |
| Major CPR / grind | – | 6 / 0 | 0 / 22 | – | – | – | – | – | – | – | – | 6 / 0 | – | **13 / 22** |
| **Total** | **189 / 205** | **240 / 364** | **131 / 161** | **204 / 239** | **179 / 194** | **308 / 358** | **169 / 251** | **189 / 250** | **131 / 171** | **184 / 190** | **204 / 196** | **141 / 301** | **82 / 327** | **2,350 / 3,206** |

### Cost ($M) by treatment and year (AMPS / dTIMS)

| Treatment | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2038 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Fair to Good | – | 33.0 / 41.6 | 3.6 / 0.2 | 2.9 / 14.7 | 6.7 / 12.0 | 41.0 / 37.2 | 18.3 / 5.7 | 18.4 / 9.9 | 25.7 / 15.8 | 34.1 / 24.8 | 44.0 / 47.7 | 15.8 / 41.5 | 8.4 / 37.5 | **252.0 / 288.6** |
| Thick overlay | – | 22.7 / 31.8 | 21.0 / 25.9 | 20.7 / 20.7 | 31.6 / 31.6 | 24.6 / 24.6 | 27.6 / 27.6 | 27.8 / 27.8 | 43.2 / 42.3 | 28.5 / 36.8 | 17.0 / 14.3 | – | – | **264.9 / 283.4** |
| Thin overlay | 6.0 / 6.0 | 5.3 / 8.5 | 3.0 / 3.0 | 12.3 / 12.3 | 20.7 / 20.7 | 23.8 / 25.2 | 21.8 / 23.9 | 14.6 / 11.7 | 1.4 / 7.5 | 3.0 / 3.9 | – | 0.0 / 2.5 | – | **111.8 / 125.2** |
| Microsurfacing | 4.5 / 4.5 | 9.1 / 15.5 | 16.9 / 16.9 | 22.1 / 22.1 | 8.9 / 8.9 | 13.0 / 18.3 | 2.0 / 12.8 | 9.3 / 19.7 | 0.0 / 3.3 | 3.3 / 3.9 | 8.5 / 6.8 | 12.7 / 25.4 | 8.4 / 31.9 | **118.6 / 190.1** |
| Major CPR / grind | – | 9.7 / 0.0 | 0.0 / 34.6 | – | – | – | – | – | – | – | – | 11.8 / 0.0 | – | **21.5 / 34.6** |
| **Total** | **10.5 / 10.5** | **79.8 / 97.4** | **44.6 / 80.6** | **58.0 / 69.9** | **67.9 / 73.1** | **102.4 / 105.4** | **69.7 / 70.0** | **70.1 / 69.1** | **70.3 / 68.8** | **68.9 / 69.4** | **69.5 / 68.7** | **40.3 / 69.4** | **16.8 / 69.5** | **768.8 / 921.8** |

### Spend by year

| Year | Budget ($M) | AMPS ($M) | dTIMS ($M) | AMPS − dTIMS ($M) | AMPS committed ($M) | dTIMS committed ($M) | AMPS % Good / Fair / Poor |
|---|---:|---:|---:|---:|---:|---:|---|
| 2026 | 10.5 | 10.5 | 10.5 | 0.0 | 10.5 | 10.5 | 79.0 / 21.1 / 0.0 |
| 2027 | 110.0 | 81.8 | 97.4 | -15.6 | 32.5 | 41.6 | 76.7 / 23.3 / 0.0 |
| 2028 | 110.0 | 43.8 | 80.6 | -36.8 | 40.9 | 40.9 | 65.3 / 34.7 / 0.0 |
| 2029 | 110.0 | 55.4 | 69.9 | -14.4 | 55.1 | 55.1 | 64.0 / 36.0 / 0.0 |
| 2030 | 110.0 | 66.3 | 73.1 | -6.8 | 61.2 | 61.2 | 61.8 / 38.2 / 0.0 |
| 2031 | 110.0 | 98.9 | 105.4 | -6.5 | 56.9 | 56.9 | 66.2 / 33.6 / 0.2 |
| 2032 | 70.0 | 69.8 | 70.0 | -0.2 | 46.2 | 46.2 | 68.4 / 31.4 / 0.2 |
| 2033 | 70.0 | 69.9 | 69.1 | 0.7 | 47.3 | 47.3 | 70.8 / 28.6 / 0.6 |
| 2034 | 70.0 | 69.9 | 68.8 | 1.0 | 42.3 | 42.3 | 72.7 / 26.1 / 1.2 |
| 2035 | 70.0 | 68.3 | 69.4 | -1.1 | 28.5 | 28.5 | 79.5 / 14.6 / 5.9 |
| 2036 | 70.0 | 69.3 | 68.7 | 0.6 | 14.3 | 14.3 | 86.5 / 4.5 / 9.0 |
| 2037 | 70.0 | 40.3 | 69.4 | -29.1 | 0.0 | 0.0 | 87.4 / 1.3 / 11.3 |
| 2038 | 70.0 | 16.8 | 69.5 | -52.7 | 0.0 | 0.0 | 87.2 / 1.2 / 11.5 |
| **Total** | | **760.9** | **921.8** | **-160.9** | | | |

### Network

| | dTIMS | AMPS |
|---|---:|---:|
| Units | 133 sections (129 counted in both directions) | 413 joints, 9,834 segments |
| Miles | 446.1 (one per section) | 889.8 (each direction) |
| Lane-miles | 1,898 | 1,780 (-6.2%) |
| Surveyed | – | 100.0% of miles |
| Committed at the start | – | 674.2 mi |
| Treated in the program | 125 sections, 205 treatments | 343 treatments |

### How much of dTIMS's program AMPS reproduces (share of dTIMS lane-miles)

| dTIMS treatment | dTIMS lane-miles | Same trt, same yr | Same trt, ±1 yr | Same trt, ±2 yr | Other trt, same yr | Other trt, ±1 yr | Nothing within ±2 yr |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fair to Good | 693 | 27% | 11% | 7% | 2% | 2% | 51% |
| Thick overlay | 713 | 92% | 1% | 0% | 0% | 2% | 6% |
| Thin overlay | 348 | 75% | 0% | 0% | 2% | 8% | 14% |
| Microsurfacing | 1,429 | 42% | 5% | 3% | 1% | 3% | 45% |
| Major CPR / grind | 22 | 0% | 37% | 0% | 0% | 63% | 0% |
| **All** | 3,206 | 53% | 5% | 3% | 1% | 4% | 34% |
| **Committed** | 1,418 | 98% | 0% | 0% | 0% | 0% | 2% |
| **Not committed** | 1,788 | 18% | 9% | 5% | 2% | 6% | 59% |

### How much of AMPS's program dTIMS also does (share of AMPS lane-miles)

| AMPS treatment | AMPS lane-miles | Same trt, same yr | Same trt, ±1 yr | Same trt, ±2 yr | Other trt, same yr | Other trt, ±1 yr | Nothing in dTIMS within ±2 yr |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fair to Good | 611 | 27% | 12% | 8% | 4% | 13% | 37% |
| Thick overlay | 617 | 99% | 1% | 0% | 0% | 0% | 0% |
| Thin overlay | 284 | 87% | 0% | 0% | 0% | 1% | 12% |
| Microsurfacing | 825 | 70% | 8% | 3% | 0% | 3% | 17% |
| Major CPR / grind | 13 | 0% | 50% | 0% | 0% | 0% | 50% |
| **All** | 2,350 | 68% | 7% | 3% | 1% | 4% | 17% |

## NHS non-Interstate, with committed: AMPS run 449 vs dTIMS

dTIMS reference `pdf-2026-09-24-nhs-non-int`.

### Lane-miles treated by treatment and year (AMPS / dTIMS)

| Treatment | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2038 | 2039 | 2040 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Fair to Good | – | 512 / 441 | 268 / 419 | 154 / 124 | 131 / 124 | 153 / 137 | 113 / 170 | 133 / 135 | 190 / 147 | 191 / 147 | 181 / 136 | 336 / 323 | 313 / 306 | 323 / 282 | 313 / 287 | **3,312 / 3,179** |
| Thick overlay | 62 / 60 | 203 / 241 | 147 / 194 | 99 / 128 | 127 / 146 | 132 / 127 | 151 / 151 | 168 / 186 | 167 / 167 | 130 / 132 | 140 / 143 | 4 / 3 | 24 / 0 | – | – | **1,555 / 1,679** |
| Thin overlay | 79 / 79 | 41 / 59 | 70 / 95 | 43 / 55 | 92 / 92 | 37 / 37 | 33 / 23 | 0 / 14 | – | 18 / 18 | 24 / 21 | – | – | – | – | **439 / 494** |
| Microsurfacing | 22 / 22 | 43 / 118 | 41 / 51 | 15 / 9 | 7 / 7 | 9 / 33 | 62 / 118 | 62 / 131 | 37 / 157 | 43 / 172 | 46 / 177 | 23 / 64 | 14 / 99 | 36 / 151 | 44 / 99 | **503 / 1,408** |
| Reconstruction | 18 / 18 | – | 0 / 2 | – | – | – | – | – | – | – | – | – | – | – | – | **18 / 20** |
| Minor CPR / grind | 1 / 1 | 11 / 11 | – | – | – | – | – | – | – | – | – | – | – | – | 0 / 11 | **12 / 23** |
| PM asphalt | – | 17 / 17 | – | – | – | – | – | – | – | – | – | – | – | – | – | **17 / 17** |
| **Total** | **182 / 181** | **827 / 887** | **526 / 761** | **311 / 316** | **358 / 369** | **331 / 334** | **360 / 463** | **363 / 466** | **394 / 471** | **383 / 469** | **392 / 477** | **363 / 390** | **350 / 405** | **358 / 433** | **357 / 397** | **5,856 / 6,820** |

### Cost ($M) by treatment and year (AMPS / dTIMS)

| Treatment | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2038 | 2039 | 2040 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Fair to Good | – | 156.7 / 134.9 | 83.7 / 130.7 | 48.9 / 39.5 | 42.7 / 40.3 | 50.7 / 45.3 | 38.2 / 57.5 | 45.7 / 46.6 | 66.8 / 51.8 | 68.6 / 52.7 | 66.3 / 49.7 | 125.4 / 120.5 | 119.2 / 116.3 | 125.2 / 109.6 | 124.0 / 113.7 | **1,162.1 / 1,109.1** |
| Thick overlay | 36.5 / 36.5 | 72.3 / 84.0 | 51.4 / 66.1 | 40.0 / 63.5 | 48.7 / 54.6 | 51.0 / 49.3 | 53.1 / 53.1 | 57.6 / 63.9 | 59.1 / 59.2 | 46.6 / 47.4 | 51.3 / 52.3 | 1.6 / 1.2 | 9.0 / 0.0 | – | – | **578.4 / 631.2** |
| Thin overlay | 23.8 / 23.8 | 12.4 / 16.4 | 17.2 / 23.0 | 9.7 / 12.5 | 28.0 / 28.1 | 25.0 / 25.0 | 6.5 / 4.0 | 0.0 / 3.5 | – | 8.7 / 8.7 | 5.8 / 5.8 | – | – | – | – | **137.2 / 150.9** |
| Microsurfacing | 2.8 / 2.8 | 3.7 / 11.6 | 5.2 / 6.2 | 2.7 / 2.1 | 0.4 / 0.4 | 1.0 / 3.7 | 8.0 / 14.5 | 7.4 / 15.5 | 4.4 / 18.9 | 5.3 / 21.2 | 5.8 / 22.2 | 2.9 / 8.2 | 1.8 / 12.9 | 4.7 / 20.1 | 5.9 / 13.5 | **62.0 / 173.8** |
| Reconstruction | 12.6 / 12.6 | – | 0.0 / 8.0 | – | – | – | – | – | – | – | – | – | – | – | – | **12.6 / 20.6** |
| Minor CPR / grind | 6.0 / 6.0 | 2.0 / 2.0 | – | – | – | – | – | – | – | – | – | – | – | – | 0.0 / 2.6 | **8.0 / 10.5** |
| PM asphalt | – | 0.8 / 0.8 | – | – | – | – | – | – | – | – | – | – | – | – | – | **0.8 / 0.8** |
| **Total** | **81.7 / 81.7** | **247.9 / 249.7** | **157.6 / 234.0** | **101.4 / 117.6** | **119.8 / 123.5** | **127.7 / 123.4** | **105.8 / 129.1** | **110.7 / 129.5** | **130.3 / 129.9** | **129.2 / 130.0** | **129.1 / 130.0** | **130.0 / 129.9** | **130.0 / 129.2** | **130.0 / 129.7** | **130.0 / 129.7** | **1,961.1 / 2,096.9** |

### Spend by year

| Year | Budget ($M) | AMPS ($M) | dTIMS ($M) | AMPS − dTIMS ($M) | AMPS committed ($M) | dTIMS committed ($M) | AMPS % Good / Fair / Poor |
|---|---:|---:|---:|---:|---:|---:|---|
| 2026 | 81.7 | 83.0 | 81.7 | 1.4 | 81.7 | 81.7 | 48.6 / 51.2 / 0.1 |
| 2027 | 250.0 | 249.9 | 249.7 | 0.2 | 60.0 | 61.2 | 63.3 / 36.4 / 0.3 |
| 2028 | 250.0 | 158.8 | 234.0 | -75.2 | 50.4 | 59.4 | 68.3 / 31.2 / 0.5 |
| 2029 | 130.0 | 102.4 | 117.6 | -15.2 | 41.5 | 61.3 | 68.3 / 31.3 / 0.4 |
| 2030 | 130.0 | 120.5 | 123.5 | -3.0 | 71.9 | 71.9 | 70.7 / 29.1 / 0.1 |
| 2031 | 130.0 | 129.0 | 123.4 | 5.6 | 73.2 | 74.3 | 75.3 / 24.5 / 0.2 |
| 2032 | 130.0 | 106.1 | 129.1 | -23.0 | 60.0 | 60.0 | 80.4 / 19.4 / 0.2 |
| 2033 | 130.0 | 110.7 | 129.5 | -18.8 | 54.3 | 54.3 | 83.7 / 16.0 / 0.3 |
| 2034 | 130.0 | 129.9 | 129.9 | -0.1 | 59.1 | 59.2 | 80.1 / 19.5 / 0.4 |
| 2035 | 130.0 | 130.0 | 130.0 | 0.0 | 55.3 | 56.1 | 67.5 / 32.2 / 0.3 |
| 2036 | 130.0 | 130.0 | 130.0 | 0.0 | 57.1 | 58.1 | 70.7 / 29.2 / 0.1 |
| 2037 | 130.0 | 130.0 | 129.9 | 0.1 | 0.0 | 0.0 | 72.1 / 27.8 / 0.1 |
| 2038 | 130.0 | 130.0 | 129.2 | 0.8 | 0.0 | 0.0 | 74.0 / 25.9 / 0.1 |
| 2039 | 130.0 | 130.0 | 129.7 | 0.3 | 0.0 | 0.0 | 75.7 / 24.2 / 0.1 |
| 2040 | 130.0 | 130.0 | 129.7 | 0.3 | 0.0 | 0.0 | 75.8 / 24.1 / 0.1 |
| **Total** | | **1,970.2** | **2,096.9** | **-126.8** | | | |

### Network

| | dTIMS | AMPS |
|---|---:|---:|
| Units | 562 sections (113 counted in both directions) | 996 joints, 19,920 segments |
| Miles | 1,410.6 (one per section) | 1,765.6 (each direction) |
| Lane-miles | 3,562 | 3,531 (-0.9%) |
| Surveyed | – | 99.9% of miles |
| Committed at the start | – | 939.2 mi |
| Treated in the program | 558 sections, 1,055 treatments | 1,159 treatments |

### How much of dTIMS's program AMPS reproduces (share of dTIMS lane-miles)

| dTIMS treatment | dTIMS lane-miles | Same trt, same yr | Same trt, ±1 yr | Same trt, ±2 yr | Other trt, same yr | Other trt, ±1 yr | Nothing within ±2 yr |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fair to Good | 3,179 | 22% | 25% | 15% | 3% | 2% | 35% |
| Thick overlay | 1,679 | 85% | 2% | 1% | 5% | 3% | 4% |
| Thin overlay | 494 | 71% | 4% | 1% | 6% | 8% | 11% |
| Microsurfacing | 1,408 | 16% | 3% | 0% | 2% | 5% | 74% |
| Reconstruction | 20 | 88% | 0% | 0% | 0% | 12% | 0% |
| Minor CPR / grind | 23 | 53% | 0% | 0% | 0% | 0% | 47% |
| PM asphalt | 17 | 100% | 0% | 0% | 0% | 0% | 0% |
| **All** | 6,820 | 40% | 13% | 7% | 3% | 3% | 34% |
| **Committed** | 1,879 | 98% | 0% | 0% | 0% | 0% | 1% |
| **Not committed** | 4,941 | 18% | 18% | 10% | 4% | 4% | 46% |

### How much of AMPS's program dTIMS also does (share of AMPS lane-miles)

| AMPS treatment | AMPS lane-miles | Same trt, same yr | Same trt, ±1 yr | Same trt, ±2 yr | Other trt, same yr | Other trt, ±1 yr | Nothing in dTIMS within ±2 yr |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fair to Good | 3,312 | 20% | 23% | 14% | 4% | 5% | 34% |
| Thick overlay | 1,555 | 92% | 2% | 1% | 4% | 1% | 1% |
| Thin overlay | 439 | 81% | 5% | 1% | 2% | 4% | 7% |
| Microsurfacing | 503 | 44% | 9% | 3% | 4% | 8% | 32% |
| Reconstruction | 18 | 100% | 0% | 0% | 0% | 0% | 0% |
| Minor CPR / grind | 12 | 100% | 0% | 0% | 0% | 0% | 0% |
| PM asphalt | 17 | 100% | 0% | 0% | 0% | 0% | 0% |
| **All** | 5,856 | 47% | 15% | 8% | 4% | 4% | 23% |

## NHS non-Interstate, no committed: AMPS run 445 vs dTIMS

dTIMS reference `pdf-2026-09-24-nhs-non-int-no-com`.

### Lane-miles treated by treatment and year (AMPS / dTIMS)

| Treatment | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2038 | 2039 | 2040 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Fair to Good | – | 496 / 378 | 528 / 578 | 297 / 317 | 240 / 211 | 266 / 227 | 253 / 228 | 250 / 243 | 275 / 186 | 273 / 273 | 292 / 283 | 295 / 277 | 283 / 265 | 281 / 261 | 275 / 259 | **4,304 / 3,986** |
| Thick overlay | – | 239 / 347 | 188 / 136 | 40 / 28 | 79 / 114 | 57 / 101 | 72 / 95 | 70 / 56 | 18 / 25 | 6 / 0 | – | – | – | – | – | **767 / 902** |
| Microsurfacing | – | – | – | – | – | – | 0 / 7 | – | 59 / 234 | 82 / 98 | 27 / 52 | 0 / 53 | 19 / 69 | 6 / 66 | 7 / 23 | **201 / 603** |
| Minor CPR / grind | – | 0 / 18 | 8 / 9 | 14 / 0 | 33 / 22 | 14 / 0 | – | 0 / 32 | 0 / 36 | – | – | – | – | – | 0 / 18 | **69 / 136** |
| **Total** | **0 / 0** | **735 / 742** | **724 / 724** | **351 / 345** | **352 / 347** | **337 / 328** | **325 / 329** | **319 / 332** | **352 / 481** | **361 / 371** | **318 / 335** | **295 / 330** | **302 / 334** | **287 / 327** | **282 / 300** | **5,340 / 5,626** |

### Cost ($M) by treatment and year (AMPS / dTIMS)

| Treatment | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2038 | 2039 | 2040 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Fair to Good | – | 151.8 / 115.7 | 165.0 / 180.5 | 94.6 / 100.9 | 77.9 / 68.4 | 88.2 / 75.1 | 85.5 / 77.0 | 86.0 / 83.9 | 96.7 / 65.3 | 97.9 / 98.0 | 106.6 / 103.4 | 110.0 / 103.2 | 107.5 / 101.0 | 109.2 / 101.2 | 108.9 / 102.6 | **1,485.7 / 1,376.1** |
| Thick overlay | – | 73.2 / 106.0 | 58.5 / 42.6 | 12.7 / 8.9 | 25.7 / 37.2 | 18.9 / 33.5 | 24.2 / 32.0 | 24.0 / 19.2 | 6.2 / 8.9 | 2.0 / 0.0 | – | – | – | – | – | **245.4 / 288.3** |
| Microsurfacing | – | – | – | – | – | – | 0.0 / 0.8 | – | 7.1 / 28.3 | 10.1 / 12.0 | 3.4 / 6.6 | 0.0 / 6.8 | 2.5 / 9.0 | 0.8 / 8.8 | 1.0 / 3.1 | **24.9 / 75.5** |
| Minor CPR / grind | – | 0.0 / 3.3 | 1.4 / 1.8 | 2.7 / 0.0 | 6.4 / 4.3 | 2.8 / 0.0 | – | 0.0 / 6.7 | 0.0 / 7.6 | – | – | – | – | – | 0.0 / 4.2 | **13.3 / 27.9** |
| **Total** | **0.0 / 0.0** | **225.0 / 225.0** | **224.9 / 224.9** | **110.0 / 109.8** | **110.0 / 109.9** | **109.9 / 108.6** | **109.8 / 109.8** | **110.0 / 109.8** | **110.0 / 110.0** | **110.0 / 110.0** | **110.0 / 110.0** | **110.0 / 110.0** | **110.0 / 110.0** | **110.0 / 110.0** | **109.9 / 110.0** | **1,769.3 / 1,767.7** |

### Spend by year

| Year | Budget ($M) | AMPS ($M) | dTIMS ($M) | AMPS − dTIMS ($M) | AMPS committed ($M) | dTIMS committed ($M) | AMPS % Good / Fair / Poor |
|---|---:|---:|---:|---:|---:|---:|---|
| 2026 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | – | 44.8 / 55.0 / 0.2 |
| 2027 | 225.0 | 225.0 | 225.0 | 0.0 | 0.0 | – | 58.2 / 41.8 / 0.1 |
| 2028 | 225.0 | 224.9 | 224.9 | 0.1 | 0.0 | – | 70.3 / 29.6 / 0.1 |
| 2029 | 110.0 | 110.0 | 109.8 | 0.1 | 0.0 | – | 71.6 / 28.3 / 0.1 |
| 2030 | 110.0 | 110.0 | 109.9 | 0.0 | 0.0 | – | 73.6 / 26.4 / 0.1 |
| 2031 | 110.0 | 109.9 | 108.6 | 1.2 | 0.0 | – | 78.7 / 21.3 / 0.1 |
| 2032 | 110.0 | 109.8 | 109.8 | 0.0 | 0.0 | – | 85.4 / 14.6 / 0.1 |
| 2033 | 110.0 | 110.0 | 109.8 | 0.2 | 0.0 | – | 92.5 / 7.5 / 0.1 |
| 2034 | 110.0 | 110.0 | 110.0 | -0.0 | 0.0 | – | 82.8 / 17.1 / 0.1 |
| 2035 | 110.0 | 110.0 | 110.0 | -0.0 | 0.0 | – | 65.7 / 34.3 / 0.1 |
| 2036 | 110.0 | 110.0 | 110.0 | 0.0 | 0.0 | – | 64.9 / 35.1 / 0.1 |
| 2037 | 110.0 | 110.0 | 110.0 | 0.0 | 0.0 | – | 64.9 / 35.0 / 0.1 |
| 2038 | 110.0 | 110.0 | 110.0 | 0.0 | 0.0 | – | 63.8 / 36.1 / 0.1 |
| 2039 | 110.0 | 110.0 | 110.0 | 0.0 | 0.0 | – | 63.3 / 36.7 / 0.1 |
| 2040 | 110.0 | 109.9 | 110.0 | -0.1 | 0.0 | – | 62.2 / 37.7 / 0.1 |
| **Total** | | **1,769.3** | **1,767.7** | **1.6** | | | |

### Network

| | dTIMS | AMPS |
|---|---:|---:|
| Units | 562 sections (113 counted in both directions) | 996 joints, 19,920 segments |
| Miles | 1,410.6 (one per section) | 1,765.6 (each direction) |
| Lane-miles | 3,562 | 3,531 (-0.9%) |
| Surveyed | – | 99.9% of miles |
| Committed at the start | – | 0.0 mi |
| Treated in the program | 558 sections, 968 treatments | 1,163 treatments |

### How much of dTIMS's program AMPS reproduces (share of dTIMS lane-miles)

| dTIMS treatment | dTIMS lane-miles | Same trt, same yr | Same trt, ±1 yr | Same trt, ±2 yr | Other trt, same yr | Other trt, ±1 yr | Nothing within ±2 yr |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fair to Good | 3,986 | 14% | 16% | 13% | 2% | 2% | 53% |
| Thick overlay | 902 | 19% | 12% | 5% | 12% | 9% | 43% |
| Microsurfacing | 603 | 8% | 4% | 2% | 10% | 11% | 66% |
| Minor CPR / grind | 136 | 14% | 0% | 10% | 20% | 25% | 31% |
| **All** | 5,626 | 14% | 14% | 10% | 5% | 4% | 52% |

### How much of AMPS's program dTIMS also does (share of AMPS lane-miles)

| AMPS treatment | AMPS lane-miles | Same trt, same yr | Same trt, ±1 yr | Same trt, ±2 yr | Other trt, same yr | Other trt, ±1 yr | Nothing in dTIMS within ±2 yr |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fair to Good | 4,304 | 13% | 15% | 12% | 5% | 4% | 52% |
| Thick overlay | 767 | 22% | 14% | 5% | 11% | 7% | 41% |
| Microsurfacing | 201 | 23% | 12% | 6% | 0% | 7% | 51% |
| Minor CPR / grind | 69 | 28% | 0% | 20% | 0% | 0% | 52% |
| **All** | 5,340 | 15% | 15% | 11% | 5% | 5% | 50% |

## Why they differ

- **Starting condition.** dTIMS starts each section (2–5 mi) from its survey; AMPS starts each joint (about 1–2 mi, per direction) from the length-weighted average of its own survey. On divided roads dTIMS uses the EB / NB survey for both directions, AMPS each direction's own. Fair to Good (any section rated MAP-21 Fair) and Thick / Thin Overlay windows fire on different road as a result. dTIMS's Good / Fair / Poor export is unusable for these runs, so the starting ratings can't be compared directly.
- **Units.** AMPS plans joints, dTIMS sections. A joint only partly inside a committed section is locked as committed (about 104 mi more locked road than dTIMS on the NHS), and a joint can cross two dTIMS sections.
- **Lanes.** AMPS has fewer lanes than dTIMS's `Lanes_Total` on dTIMS's 5- and 6-lane Interstate sections (1,780 against 1,898 lane-miles), so its Interstate treatments cost less per section.
- **Committed sections with a later Preservation commitment** (8 on the NHS): dTIMS locks them until that year even though it never applies the Preservation; AMPS locks them only through the commitment it applies.

Data: AMPS runs 448, 449, 445 (local `pms`, project and yearly summaries, start-state snapshots); dTIMS `dtims_docs/pdf-analysis-runs-2026-09-30` (construction programs, network). The runs are linked to their dTIMS runs (vs dTIMS tab).
