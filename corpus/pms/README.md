# NHS work-program comparison: local run 308 versus April dTIMS

**The programs spend almost the same amount over the same 13 years, but they select substantially different locations and schedules.** Thick overlay dominates both. On the precise shared footprint, the first treatment type agrees on 77.06% of mileage, but treatment and year both agree on only 7.00%.

## Inputs and boundaries of this comparison

- **Local:** `work_program_20260925_062225.xlsx`, run/scenario **308**, “VALIDATION UI TEST (copy of 270) - rerun on v1.6, 13 years to 2038, 90% Good + 5% Poor”. This replaces the earlier 061108 workbook; none of that older workbook’s numbers enter this report.
- **dTIMS:** `2026 04 27 ALL Network NHS Construction Program - DEL_STIP_2026_NHS_ONLY_NO_INTERSTATES_Budget_Scenario.xlsx`, analysis set `DEL_STIP_2026_NHS_ONLY_NO_INTERSTATE`.
- Local program years **1–13** are aligned to calendar years **2026–2038**, as identified by the local run name and application year convention. Both files therefore cover the same scheduled years.
- The local file records **20,413 analysis segments** and the exact non-Interstate NHS filter below. Its All Projects sheet contains selected work, not all input segments. The dTIMS workbook also contains scheduled work rather than the full analysis inventory.

```sql
NOT (SUBSTRING(route_id, 3, 1) = '1' AND LENGTH(route_id) = 13) AND SUBSTRING(route_id, 10, 2) <> '17' AND nhs_code > 0
```

No live database was queried and no run was recalculated. All comparisons below use the supplied workbook values. The dTIMS `Data` and `Data (2)` tabs repeat the same events; the local Year tabs repeat All Projects. Neither duplicate view is added to totals. Source hashes and raw event records are retained in SQLite.

## Overall similarities and differences

| Measure | April dTIMS | Local run 308 | Interpretation |
| --- | --- | --- | --- |
| Scheduled years | 2026–2038 | 2026–2038 | Same horizon |
| Scheduled cost | $765.09m | $767.22m | Local +$2.13m (+0.28%) |
| Selected rows | 382 | 590 | dTIMS section-treatment events versus local merged projects |
| Route IDs with selected work | 93 | 125 | Direction suffixes are preserved |
| Treatment miles (sum of row lengths) | 1,027.09 | 1,276.58 | Local +249.49 (+24.29%) |
| Scheduled cost / treatment mile | $744,912 | $600,995 | Not a matched unit-rate comparison; mix, lanes, commitments and timing differ |

“Treatment miles” count a section again if it is treated again. They are not unique network miles or lane-miles. Four dTIMS sections receive two treatments; local exported project envelopes do not overlap on the same exact route ID. Local has 590 project rows, while Condition Trajectory sums 672 selections: the exporter labels selected-joint counts as “Projects,” whereas All Projects uses merged project rows. The annual costs reconcile despite the count difference.

![Program spending, mix and timing](program-comparison.png)

## Annual spending and work volume

Local’s explicit schedule is **$50m in 2026 and $60m in each of 2027–2038**, totaling **$770m**. Local spends $767.22m (99.64% of that schedule). The dTIMS annual expenditures closely follow the same pattern; its workbook does not expose a separate authorized-budget table. Its spending is 99.36% of the local schedule, which is a comparison benchmark rather than proof of the vendor budget definition.

| Year | dTIMS cost $m | Local cost $m | Local − dTIMS $m | dTIMS treatment mi | Local treatment mi |
| --- | --- | --- | --- | --- | --- |
| 2026 | 49.84 | 49.81 | -0.026 | 47.61 | 122.25 |
| 2027 | 59.63 | 59.94 | 0.305 | 102.26 | 155.36 |
| 2028 | 59.78 | 59.91 | 0.122 | 86.29 | 110.24 |
| 2029 | 59.89 | 59.72 | -0.172 | 95.57 | 107.99 |
| 2030 | 59.68 | 59.50 | -0.176 | 92.35 | 104.23 |
| 2031 | 59.27 | 59.99 | 0.720 | 90.15 | 90.55 |
| 2032 | 59.87 | 59.93 | 0.059 | 87.83 | 88.69 |
| 2033 | 59.91 | 59.32 | -0.592 | 87.33 | 86.07 |
| 2034 | 59.45 | 59.46 | 0.015 | 82.13 | 84.58 |
| 2035 | 59.90 | 60.00 | 0.098 | 80.53 | 83.67 |
| 2036 | 59.43 | 59.93 | 0.496 | 66.90 | 81.93 |
| 2037 | 59.54 | 59.88 | 0.340 | 56.53 | 80.27 |
| 2038 | 58.90 | 59.84 | 0.939 | 51.62 | 80.75 |

In 2026 the spending differs by only **$25,930**, while local schedules **122.246 treatment miles** versus **47.610** in dTIMS. Similar budgets therefore do not imply the same work quantity, scope, or treatment pricing.

## Treatment mix

| Treatment | dTIMS rows | Local rows | dTIMS miles | Local miles | dTIMS cost $m | Local cost $m |
| --- | --- | --- | --- | --- | --- | --- |
| Thick overlay | 329 | 468 | 859.97 | 920.17 | 657.08 | 633.39 |
| Thin overlay | 36 | 87 | 101.39 | 221.89 | 56.46 | 100.01 |
| Microsurfacing | 6 | 23 | 26.74 | 91.22 | 14.09 | 19.22 |
| Minor CPR | 8 | 6 | 33.30 | 30.52 | 16.20 | 11.99 |
| Reconstruction | 2 | 0 | 5.54 | 0.00 | 20.60 | 0.00 |
| Preservation | 1 | 0 | 0.15 | 0.00 | 0.65 | 0.00 |
| Cape seal | 0 | 6 | 0.00 | 12.78 | 0.00 | 2.62 |

Thick overlay is 85.88% of dTIMS spending and 82.56% locally. Local schedules much more thin overlay and microsurfacing mileage. It includes cape seal, while dTIMS includes reconstruction and preservation absent from the local selected list. Absence from a selected list does not establish that a treatment was disabled or ineligible.

Treatment correspondence is explicit: `PMS_Thick_Overlay` → `THICK_OVERLAY`, `PMS_Thin_Overlay` → `THIN_OVERLAY`, `PMS_PM_Microsurfacing` → `MICROSURFACING`, and `PMS_Minor_CPR_Diamond_Grind` → `MINOR_CPR_DG`. Reconstruction and preservation retain their own categories; cape seal is not treated as equivalent to preservation.

## Selected locations: exact routes and directions

![Selected footprint comparison](footprint-comparison.png)

dTIMS has **1,010.040 unique selected miles**. Local lists **1,276.584 treatment miles**, within exported envelopes totaling **1,279.824 miles**. Six local rows have internal gaps totaling **3.240 miles** whose locations are not supplied.

Overlaying exact route IDs and exported From/To boundaries gives **768.871 shared envelope miles**, **510.953 local-only**, and **241.169 dTIMS-only**. Allowing for all unspecified local gaps, the actual shared footprint is bounded by **765.631–768.871 miles**, or **75.80–76.12%** of dTIMS's selected footprint. This bound assumes each row's listed treatment mileage lies within its exported envelope.

These selected-program overlaps should not be confused with the earlier full-inventory NHS overlay. Two models can share nearly all their input roads and still choose different roads for treatment. Opposite directions are not substituted into the primary match.

| Direction | dTIMS treatment miles | Local treatment miles | dTIMS cost $m | Local cost $m |
| --- | --- | --- | --- | --- |
| 00 | 398.30 | 344.64 | 262.92 | 219.17 |
| NB | 349.51 | 377.94 | 270.32 | 220.32 |
| SB | 0.00 | 109.53 | 0.00 | 58.73 |
| EB | 279.28 | 320.05 | 231.86 | 200.68 |
| WB | 0.00 | 124.42 | 0.00 | 68.33 |

Local schedules **233.953 treatment miles and $127.057m** on SB/WB route IDs absent from the dTIMS selected list. This is not proof of extra two-way physical coverage: some dTIMS NB/EB rows carry total lanes for both directions. As a separate sensitivity check, dropping only the NB/SB/EB/WB suffixes gives **777.006 shared corridor-envelope miles**, **293.083 local-only**, and **233.034 dTIMS-only**. That diagnostic assumes comparable opposing-direction milepoints and is not used for treatment or timing agreement. Even under this simplification, substantial selection differences remain.

### Treatment and timing agreement on precise shared geometry

The following uses **757.210 unique shared miles**, excluding every overlapping portion of the six local rows with length/span discrepancies. On repeated dTIMS sections, timing means the **first** scheduled treatment; complete sequence equality is checked separately.

| Comparison | Miles | Share of precise shared mileage |
| --- | --- | --- |
| Same first treatment type | 583.478 | 77.06% |
| Same first treatment year | 65.478 | 8.65% |
| Same treatment and year | 52.983 | 7.00% |
| Identical complete treatment sequence | 52.983 | 7.00% |
| First treatment within ±2 years | 272.514 | 35.99% |
| Local first treatment earlier | 305.083 | 40.29% |
| Local first treatment later | 386.649 | 51.06% |

The mileage-weighted average signed delay is **0.34 years later locally**, but the average **absolute** timing difference is **4.26 years**. Earlier and later choices largely cancel in the signed average; it would be misleading to describe the schedules as only four months apart.

Largest treatment-type disagreements on that shared subset:

| dTIMS first treatment | Local first treatment | Miles |
| --- | --- | --- |
| THICK_OVERLAY | THIN_OVERLAY | 51.835 |
| THIN_OVERLAY | THICK_OVERLAY | 51.371 |
| THICK_OVERLAY | MICROSURFACING | 31.001 |
| THICK_OVERLAY | CAPE_SEAL | 12.775 |
| THIN_OVERLAY | MICROSURFACING | 11.388 |
| MICROSURFACING | THICK_OVERLAY | 4.688 |
| RECONSTRUCTION | THICK_OVERLAY | 4.490 |
| MICROSURFACING | THIN_OVERLAY | 4.403 |

## Commitments are a major difference in what the files describe

dTIMS marks **329 of 382 events (86.13%)** as committed: **876.350 treatment miles** and **$646.02m (84.44% of spending)**. Of these, **325** match the row's `Com_Trt` and `Com_Year` treatment/year metadata. Four are later follow-up treatments on those same sections and retain the commitment flag despite differing from the committed treatment/year. Thus 329 flagged rows should not be described as 329 independently forced treatment events. Another 53 rows have a false commitment flag.

| dTIMS Data row | Section | Scheduled treatment/year | Committed treatment/year |
| --- | --- | --- | --- |
| 88 | 20200600000EB-002.440-1 | PMS_PM_Microsurfacing / 2038 | PMS_Thick_Overlay / 2027 |
| 165 | 2730002000000-007.690-1 | PMS_Thick_Overlay / 2034 | PMS_Thin_Overlay / 2026 |
| 167 | 2730002000000-012.670-1 | PMS_Thick_Overlay / 2033 | PMS_Thin_Overlay / 2026 |
| 377 | 5530016000000-004.250-1 | PMS_Thick_Overlay / 2035 | PMS_Thin_Overlay / 2026 |

The local export has no per-project commitment flag and no Committed Projects tab. It cannot establish that the same commitments were loaded, forced, or represented identically. A large part of the vendor schedule is explicitly committed, so this is not a clean comparison between two unconstrained optimal selections.

For the vendor events carrying the commitment flag, **48.072 treatment-event miles** have an exact-route overlapping local treatment of the same type in the same year—about **5.49%** of their 876.35 event-miles. This is a spatial agreement statistic, not a compliance verdict: exported project aggregation, direction representation, input dates and commitment loading can differ. The event comparison sheet identifies each case for review.

## Pricing similarities and differences

Removing an assumed **2% annual escalation** from each event produces these rate fingerprints. This is a diagnostic normalization, not a claim that every committed dollar was generated by that formula.

| Treatment | Local normalized $ / treatment mile | dTIMS frequent normalized $ / treatment mile |
| --- | --- | --- |
| Thick overlay | $600,000 on all 468 rows | $600,000 on 296 rows; $1,200,000 on 26 rows; seven other values |
| Thin overlay | $440,000 on all 87 rows | $440,000 on 21 rows; $880,000 on nine rows; six other values |
| Minor CPR | $360,000 on all six rows | $360,000 on six rows; $720,000 on two rows |
| Microsurfacing | $206,000 on all 23 rows | $580,000 on four rows; $290,000 on one; $390,909 on one |
| Cape seal | $198,000 on all six rows | No selected rows |

Every local project row has two lanes. Vendor lane totals are missing on 333 of 382 events; 45 rows explicitly have four total lanes. The common overlay/CPR fingerprints show that many base pricing conventions align, while doubled vendor densities are consistent with different lane scope. Commitment amounts and the April pricing vintage also differ. Microsurfacing has a particularly different density; all six vendor rows carry the commitment flag, including one later follow-up event. The files alone cannot separate all these causes or establish a cost-engine error.

## Condition outcomes: available locally, absent for dTIMS

![Local condition trajectory](local-condition-trajectory.png)

The local workbook reports Good **38.07% → 59.58%**, Fair **58.45% → 35.46%**, and Poor **3.48% → 4.97%**. Its **90% Good target is missed by 30.42 percentage points**. The final Poor value is below the 5% target named in the run title, although Poor rises to 8.60% in year 11. A terminal-year target is different from a ceiling in every year.

The April workbook has inventory-like CCI, PSI, IRI and cracking columns on scheduled sections, but no annual network GFP results, untreated baseline trajectory, equivalent ages, or complete analysis-network denominator. Those values cannot be compared to local final-year GFP or treated as conditions measured at the scheduled treatment year. The local All Projects sheet has no per-project condition fields either. Consequently these two workbooks do **not** establish which program produces better condition, and no vendor annual curve was invented. Local Total Benefit also has no equivalent vendor field in this workbook.

## Workbook reconciliation and export issues

1. **Local Configuration Total Budget is wrong/inconsistent:** it says **$650m**, while the detailed schedule and Summary both say **$770m**. The $120m discrepancy equals using 13 × the first-year $50m instead of the explicit schedule. Calculations in this report use $770m.
2. **“Projects” means two different things:** All Projects and Summary contain 590 merged projects; Condition Trajectory sums 672 selected joints. Costs match year by year. This is a labeling/granularity issue, not 82 additional cost rows.
3. **Six local geometry envelopes contain 3.240 miles of unspecified gaps.** They are isolated below and excluded from exact treatment/timing statistics.
4. **Duplicate tabs:** all dTIMS Data/Data (2) events and shared fields reconcile; every local Year tab reconciles to All Projects.
5. **Target disclosure is incomplete:** the local Constraints tab reports the missed Good target but does not separately display the Poor target named in the run title. Its final Poor value is available in Condition Trajectory.

| All Projects Excel row | Route | Begin MP | End MP | Listed miles | Envelope minus listed miles |
| --- | --- | --- | --- | --- | --- |
| 66 | 2630002000000 | 6.578 | 13.460 | 6.082 | 0.800 |
| 83 | 42202190000NB | 9.667 | 13.280 | 3.313 | 0.300 |
| 439 | 35200400000EB | 0.840 | 2.969 | 0.589 | 1.540 |
| 472 | 23201190000SB | 4.478 | 5.869 | 1.191 | 0.200 |
| 492 | 42202190000NB | 27.059 | 29.909 | 2.650 | 0.200 |
| 527 | 31201190000NB | 16.000 | 18.599 | 2.399 | 0.200 |

## Routes with the largest spending differences

This table preserves direction. A route absent from one selected list may still exist in that model’s input network.

| Route | dTIMS $m | Local $m | Local − dTIMS $m | dTIMS treatment mi | Local treatment mi |
| --- | --- | --- | --- | --- | --- |
| 34200190000SB | 0.00 | 13.41 | 13.41 | 0.00 | 28.39 |
| 54200500000WB | 0.00 | 13.25 | 13.25 | 0.00 | 20.58 |
| 16200480000WB | 0.00 | 11.41 | 11.41 | 0.00 | 22.85 |
| 03201190000NB | 18.56 | 7.60 | -10.96 | 12.35 | 12.13 |
| 10200190000SB | 0.00 | 10.36 | 10.36 | 0.00 | 20.39 |
| 09200500000WB | 0.00 | 10.00 | 10.00 | 0.00 | 17.53 |
| 34200190000NB | 8.65 | 18.16 | 9.51 | 6.21 | 31.85 |
| 23201190000NB | 18.01 | 9.09 | -8.92 | 12.12 | 14.70 |
| 32202190000NB | 22.14 | 13.40 | -8.74 | 33.34 | 25.71 |
| 3140857000000 | 8.65 | 0.00 | -8.65 | 1.20 | 0.00 |
| 28204600000WB | 0.00 | 8.37 | 8.37 | 0.00 | 16.96 |
| 10200190000NB | 23.10 | 15.63 | -7.48 | 13.90 | 26.29 |

## Interpretation and next comparison

The strongest similarity is the spending schedule and reliance on thick overlays. The strongest differences are selected footprints, first-treatment dates, direction/lane representation, vendor commitments, and the amount of thin overlay and microsurfacing. Similar total spending should not be interpreted as model parity.

To isolate engine differences, the next experiment should give both implementations the same segment geometry, directional/lane scope, initial condition definitions, committed projects, rate schedule and annual budgets. It should export annual condition for the same complete network. The prior [implementation review](../implementation-review-2026-09-25/README.md) identifies candidate causes to investigate, but this workbook comparison does not attribute these observed differences to a particular code defect or prove the producing run used the current checkout.

## Deliverables and reproduction

- [Comparison workbook](program-comparison.xlsx): annual spending, treatment/district/direction summaries, every route and event match, timing differences, geometry gaps and checks.
- [SQLite evidence](comparison.sqlite): normalized events, raw source records, exact boundary partitions, source sheet inventory and calculated summaries.
- [CSV tables](csv/), [numerical summary](summary.json), and [validation](validation.md).
- [Comparison chart SVG](program-comparison.svg), [footprint SVG](footprint-comparison.svg), and [local condition SVG](local-condition-trajectory.svg).

```sh
venv/bin/python scripts/dtims_audit/compare_program_workbooks.py
MPLCONFIGDIR=/private/tmp/pms-matplotlib .venv/bin/python scripts/dtims_audit/program_workbook_report.py
python3 scripts/dtims_audit/validate_program_comparison.py
```

Overlap uses exact route strings, direction suffixes and milepoint intervals, with endpoints rounded to one millionth of a mile. It assumes compatible linear references across the two workbook vintages; GPS/LRS alignment was not independently verified. Costs allocated to shared/unshared atomic intervals are proportional to exported span and are approximate for the six gap-containing local rows. The primary treatment/timing agreement excludes those rows. No opposite-direction matching or cost inflation adjustment is used in the nominal program totals.
