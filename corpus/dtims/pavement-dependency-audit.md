# Pavement deterioration, treatments, strategy, and reset audit

This audit covers the committed Interstate and Non-NHS scenarios. The original package contained the core authored deterioration/treatment model. Its zero-unresolved-formula count was too narrow to establish complete replication: it did not audit all supporting configuration references or supply proprietary engine implementations. The supplement adds field-code mappings, attribute/table types, the base-entity definition, and explicit checks of manual strategy and dFRAG configuration.

## Verified configuration

| Analysis set | Direct treatments | Reachable treatments | Variables | Curve bindings | Reset rules | Subsequent links |
|---|---:|---:|---:|---:|---:|---:|
| DEL_STIP_2026_INTERSTATES_ONLY | 10 | 15 | 47 | 45 | 310 | 111 |
| DEL_STIP_2026_Non_NHS_ALL_NETWORK | 12 | 19 | 46 | 44 | 408 | 148 |

Shared unique definitions: 19 treatments, 47 variables, 45 curve bindings, 408 resets, 148 subsequent links, 19 cost rules, and 201 expressions. Ancillary endpoints returned no attached ancillary rules. Reachable subsequent treatments are retained even when not directly attached to a set; this does not assert the proprietary engine will generate every possible path.

The audit checked 2,712 formula/binding/field/sequence references. There are 0 unresolved core references in these checks. Supporting metadata gaps are listed below. Full records and checks are in `csv/dependency-checks.csv` and `dependency-audit.json`.

## Deterioration and initialization

The capture includes ordered analysis-variable bindings, initial attribute/expression references, field defaults, curve order and applicability filters, ShiftCurve and slope settings, hold/age variables, raw IRI/rutting/cracking/faulting expressions, GFP classifiers, and cost/benefit variables. CCI has its own curve; raw IRI is not the PSI index. Family and coefficient selection expressions are present. `csv/variable-binding-catalog.csv` maps every bound variable to these definitions; `csv/expressions-resolved.csv` makes GUID formulas readable.

| Table referenced by formula | Captured rows | Complete |
|---|---:|---|
| Analysis_Lookup_Perf_Coef | 144 | True |
| Analysis_Lookup_Triggers | 25 | True |
| Analysis_Lookup_Trt_Costs | 481 | True |
| DEL_Analysis_Lookup_CountyTrt_Costs | 275 | True |

The active coefficient lookup is Analysis_Lookup_Perf_Coef. The separately captured Analysis_Lookup_Performance_Coefficients is not an interchangeable substitute. Capturing coefficients plus calls to DAL_DCG_INDEXFROMAGE / DAL_DCG_AGEFROMINDEX does not itself recover their compiled implementations, curve-shift mechanics, bounds, or timing. Those require a separately validated runtime implementation.

## Treatments, strategy generation, and resets

Treatment membership/order, trigger expressions and lookup thresholds, IsInitial, ApplyAfterInitial, interval years, ancillary checks, financial/economic cost expressions, budget categories, subsequent allowlists/order, and reset targets/filter/formula/order are captured. Committed-treatment branches refer to the four committed slots in Analysis; IncludeCommitted=true is captured for both scenarios. The full shared Analysis input and committed/defined-segment tables are present.

Use `csv/treatment-binding-catalog.csv`, `csv/subsequent-treatment-catalog.csv`, and `csv/ordered-reset-catalog.csv`. Apply resets in stored order while respecting filters and the engine’s evaluation semantics; do not replace the sequence with a single final condition reset.

Both sets store LevelOfGeneration=3, UsesAdvanced=false, GenerateCommittedOnly=false, the 2026–2040 configured horizon, and their StrategyID/table registrations. Both scenarios retain budgets, cost/benefit/allowable variables, optimizer settings, AllowDoNothing, and committed inclusion. Scenario target-constraint collections returned zero rows: the name “steady state by 2028” is not evidence of an explicit GFP target constraint in that table.

Additional scoped checks returned 0 AddStrategyConfigurations rows and 0 linked/direct dFRAG rows. The set after-execute hooks and scenario workflow hooks are null. These findings do not rule out separately invoked upstream preparation batches.

There are 2 groups with tied configuration order values; see `csv/configuration-order-ties.csv`. The records are preserved, but a secondary engine ordering rule is not exposed. Candidate strategy libraries and per-strategy annual states remain excluded as requested. Their absence does not remove the authored generation rules, but prevents exhaustive path-by-path validation of generated alternatives.

## Supporting references still unavailable

- attribute code source: `a83423ef-5753-49f6-9394-abb7ee3924a3`; referenced by Analysis->CCI, Analysis->CSI, Analysis->Com_Cost, Analysis->Com_Year, Analysis->ECI, Analysis->ESALs, Analysis->JCI, Analysis->NCI, Analysis->PSI, Analysis->RDI, Analysis->SCI. Direct ID queries returned no definition under the supplied credentials.
- budget category: `9768550f-636c-4787-a736-7b3fd4f2e945`; referenced by JLZ_STIP_2026_Interstates_Only_Steady_State_by_2028, JLZ_STIP_2026_Non_NHS_Steady_State_by_2028. Direct ID queries returned no definition under the supplied credentials.
- budget category: `9ef54d0a-bdbb-4b9b-ab3e-8277bd08b827`; referenced by JLZ_STIP_2026_Interstates_Only_Steady_State_by_2028, JLZ_STIP_2026_Non_NHS_Steady_State_by_2028, PMS_County_MicroSurface, PMS_PM_Microsurfacing. Direct ID queries returned no definition under the supplied credentials.
- budget category: `c39e94b8-5038-46b2-b773-688c3dd0b296`; referenced by JLZ_STIP_2026_Interstates_Only_Steady_State_by_2028, JLZ_STIP_2026_Non_NHS_Steady_State_by_2028. Direct ID queries returned no definition under the supplied credentials.

Do not invent a definition or infer deletion from an empty response. Budget values and treatment-side category names/IDs are preserved, but these missing category definitions prevent a claim of fully resolved budget metadata. The missing table-code source does not imply the underlying numeric input columns are absent.

## What is still needed for exact replication

1. A compatible implementation of the built-in curve/inverse functions, curve shifting, annual timing, reset evaluation, committed-path handling, and strategy generation/optimizer semantics. ExpressionFunctions supplies names, descriptions and signatures, not executable source. The downloaded configuration is not the dTIMS engine.
2. Historical input/configuration versions for the original saved execution. These captures are current service state. Matching the 26 annual PDF expenditures confirms the selected saved outputs, not identical original inputs or an independent engine replay.
3. Resolution of the supporting metadata gaps above and any relevant order-tie semantics. Original upstream segmentation/import SQL is outside a replay that begins from the included Analysis table; rebuilding Analysis from raw road sources would require that separate preparation pipeline.
4. Validation of your engine against saved outputs. The numeric condition-distribution endpoint returning Category1=100 for text GFP is not an interpretable 100%-good result. No end-to-end optimization equivalence was established by this download.

The practical answer: the core authored deterioration, treatment, sequence and reset configuration is captured and checked. It is a useful configuration/input/output replication package, not proof that every component needed for an exact dTIMS clone is available.
