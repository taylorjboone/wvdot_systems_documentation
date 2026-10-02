# NHS download and model validation

Check | Result | Evidence
--- | --- | ---
SQLite integrity | PASS | Read-only integrity check
Rows NEW705_STRATS | PASS | 80533 materialized / 80533 source records / 80533 expected
Rows NEW705_STRATS_T | PASS | 176870 materialized / 176870 source records / 176870 expected
Rows NEW705_STRATS_Y | PASS | 29808 materialized / 29808 source records / 29808 expected
Rows Analysis | PASS | 562 materialized / 562 source records / 562 expected
Rows Analysis_Lookup_Perf_Coef | PASS | 144 materialized / 144 source records / 144 expected
Complete primary tabular download | PASS | Reported and captured counts agree
Inventory associations complete | PASS | All strategies resolve to one of 562 downloaded inventory records
Annual sample is complete for requested identities | PASS | 648 strategies × all 46 variables; not all 3,704,518 source annual rows
Successful response hashes | PASS | 175 responses; mismatches=[]
Known read limitations retained | PASS | 31 retained failures; oversized inventory reads recovered using smaller requests
Original workbook unchanged | PASS | Original external workbook hash matches
Workbook event coverage | PASS | 382 events, 378 names; duplicate sheet is not double-counted
Workbook sheets agree | PASS | Same event signatures and all compared costs/conditions
Live name matching retained | PASS | No approximate matches silently promoted to exact
Changed segment geometry distinguished | PASS | 283 identical extents, 49 changed extents, 46 unmatched names
Matched event signatures and cost differences | PASS | 320 events across 316 alternatives, 269 matching costs
Numerical replay between_treatments | PASS | 84337 comparisons; max error 1.42e-14
Numerical replay from_initial_state | PASS | 87210 comparisons; max error 1.42e-14
GFP replay between_treatments | PASS | 47000 classifications
GFP replay from_initial_state | PASS | 48600 classifications
Initialization differences preserved | PASS | Numeric-NULL default hypothesis; six differences explicitly retained
No skipped requested forecast paths | PASS | All sampled paths evaluated; six initializer comparison differences are separate
Conditional workbook forecast coverage | PASS | 332 matched names; missing context is disclosed, no April accuracy claim
Comparison targets match downloaded output | PASS | Every scored actual value equals the corresponding original dAfter slot
Large CSV export row counts | PASS | All four main data tables match SQLite counts
Review workbook package | PASS | 12 worksheet XML parts; ZIP CRC integrity
Documentation links | PASS | All local links resolve
No HTTP credentials in text artifacts | PASS | No supplied bearer/cookie values persisted

The six initialization differences and failed service endpoints are preserved coverage findings, not erased by passing integrity checks. Exact model-output reproduction is not evidence of real-world predictive accuracy or a certified reconstruction of the April optimization.
