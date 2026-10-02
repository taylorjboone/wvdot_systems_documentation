# Refresh comparison: live vs `archive_20260924`

## analysis_segments

| measure | before | after |
|---|---|---|
| rows | 263,039 | 265,590 |
| routes | 13,561 | 13,561 |
| length_miles | 26303.9 | 23935.1 |
| span_miles | 23935.1 | 23935.1 |
| pct_no_joint | 3.71 | 3.68 |
| pct_no_district | 3.38 | 3.35 |
| joints | 19,908 | 19,922 |
| pct_good_len | 23.26 | 24.24 |
| pct_poor_len | 48.10 | 46.72 |
| pct_good_span | 24.24 | 24.24 |

`pct_good_len` is the length-weighted % Good the engine and footers use (CCI ≥ 3); `pct_good_span` weights by milepoint span.

### Survey year of each segment's condition

| survey year | segments | miles |
|---|---|---|
| 2020 | 127 | 12.1 |
| 2021 | 1 | 0.1 |
| 2022 | 26 | 1.9 |
| 2023 | 694 | 60.3 |
| 2024 | 212,085 | 19151.1 |
| 2025 | 52,657 | 4709.6 |

## reconflate_normalized (conflation) by survey year

| year | records before | records after | routes before | routes after | GPS points | not located | routes dropped (>1 mi span) | fallback records |
|---|---|---|---|---|---|---|---|---|
| 2020 | 32,985 | 32,985 | 271 | 271 | 77,110 | 67 | 42 | 281 |
| 2021 | 24,476 | 24,476 | 216 | 216 | 58,132 | 150 | 35 | 365 |
| 2022 | 33,578 | 33,578 | 243 | 243 | 77,024 | 876 | 47 | 341 |
| 2023 | 47,344 | 47,344 | 896 | 896 | 96,316 | 80 | 8 | 239 |
| 2024 | 245,359 | 245,359 | 14,980 | 14,980 | 504,324 | 339 | 128 | 597 |
| 2025 | 47,567 | 47,567 | 981 | 981 | 97,032 | 77 | 4 | 128 |

## Joint builds

| build | status | joints | created | notes |
|---|---|---|---|---|
| 0 | current | 22,480 | 2026-09-24 | Joints present before versioned builds (last loaded by scripts/reimport_pavement_joints.py) |

## Last refresh (data_refresh_log)

| stage | status | seconds | message |
|---|---|---|---|
| A_lrs | ok | 1 |  |
| B_survey | ok | 93 |  |
| C_conflate | failed | 130 | InvalidColumnReference: there is no unique or exclusion constraint matching the ON CONFLICT specification
 |
| C_conflate | ok | 1395 |  |
| D_joints | ok | 0 |  |
| E_segments | failed | 77 | CheckFailed: checks failed: pct_segments_without_joint, pct_segments_without_district, routes_not_on_roads2, network_pct_good |
| E_segments | ok | 56 |  |
| F_commitments | ok | 1 |  |
| G_derived | ok | 18 |  |

