# Deterioration model and validation

## Inputs and independence

The primary validation reads each strategy’s After0 state once: condition, raw metrics, equivalent ages, holds, pavement type, rehab family and truck class. It reads treatment names and years from the event table. Later After values are used only as comparison targets. No later observed condition, age, family or reset value is supplied to the forward model.

A second check starts a new forecast from each saved post-treatment state and predicts the intervening untreated years. That isolates annual curve behavior from reset reproduction. Counts from these two checks overlap and must not be presented as independent samples.

The -1 final-index floor was selected using the earlier 24-strategy sample from other output tables, before evaluating NEW705. [Development evidence](model-development.json) compares -1, zero and no final floor. The fresh 144-row coefficient table has no C1/C2/C3/type/equation differences from that earlier same-day configuration snapshot. It contains more families than this validation exercises.

## Equations

For supported index family f and anchor age a0 / condition I0:

```text
offset = I0 - max(0, f(a0))
index(age) = max(-1, max(0, f(age)) + offset)
Polynomial f(age) = 5 + C1*age + C2*age^2
Linear f(age) = 5 + C1*age
Sigmoid f(age) = 5 - C1*exp(-(C2/age)^C3)
IRI base(PSI) = min(500, 65 - ln(PSI/5)/0.0066), or 500 for PSI <= 0
IRI = base(predicted PSI) + [anchor IRI - base(anchor PSI)]
Rut base(RDI) = ((5-RDI)/6.65)^(1/1.41)
Rutting = base(predicted RDI) + [anchor rutting - base(anchor RDI)]
Cracking = anchor cracking + factor*(current relevant age - anchor relevant age)
Faulting = anchor faulting until a treatment resets it
```

Cracking uses SCI age for BC and CCI age for RC. The factor is 0.15 for Sign code 1, 0.37 for other Sign with HPMS code 1, otherwise 0.56. Table-code display strings are explicitly decoded at the first hyphen for this input; the live comparisons test that convention. The code does not equate NHS membership with HPMS=1.

The model preserves IRI/rut/cracking offsets, so a base cap of 500 does not assert that final IRI can never exceed 500. The model advances holds before ages, duplicates slot 0 into slot 1 before any treatment, and applies resets after the annual deterioration step. Equivalent-age inversions use the analytic descending branch of the configured polynomial/linear/sigmoid equation. Log inversion is unsupported.

## Reset coverage

The 320 sampled events comprise 277 thick overlays, 31 thin overlays, seven minor CPR treatments, four microsurfacing treatments and one reconstruction. All are included in the full forward replay. A date/name match is not proof that a strategy was selected by the optimizer.

Thin and micro improve their five asphalt indices by 1.25 and 0.75 respectively, capped at 5, then invert equivalent ages in the old family before switching to Minor. Thick resets indices to 5 and relevant ages to 1, then changes to Major. Minor CPR preserves better condition using max(4.5,current), resets selected ages to 1 and faulting to zero, then uses Minor. Reconstruction sets ages to 1, indices to 5, raw faulting to zero, and changes to BC/Initial. Raw IRI and cracking reset behavior differs between treatments; the code implements direct versus minimum-protected assignments accordingly.

Truck class is held at the provided run value. Every sampled run has class H, which also persists through its saved resets. This does not validate how the vendor derives H from inventory defaults. Preservation, special Fair-GFP and major CPR branches in the code were not exercised by these 320 NHS events; preservation occurs in the supplied workbook but has no matching sampled event.

## Numerical results

Mode | Metric | Comparisons | Within 1e-6 | MAE | Maximum error
--- | --- | --- | --- | --- | ---
between_treatments | CCI | 9400 | 9400 | 0 | 0
between_treatments | CSI | 263 | 263 | 0 | 0
between_treatments | ECI | 9137 | 9137 | 0 | 0
between_treatments | FLT | 9400 | 9400 | 0 | 0
between_treatments | IRI | 9400 | 9400 | 4.53538e-18 | 1.42109e-14
between_treatments | JCI | 263 | 263 | 0 | 0
between_treatments | PCRK | 9400 | 9400 | 3.28874e-16 | 3.55271e-15
between_treatments | PSI | 9400 | 9400 | 5.90544e-21 | 5.55112e-17
between_treatments | RDI | 9137 | 9137 | 0 | 0
between_treatments | RUT | 9400 | 9400 | 1.24014e-19 | 1.11022e-16
between_treatments | SCI | 9137 | 9137 | 0 | 0
from_initial_state | CCI | 9720 | 9720 | 0 | 0
from_initial_state | CSI | 270 | 270 | 0 | 0
from_initial_state | ECI | 9450 | 9450 | 0 | 0
from_initial_state | FLT | 9720 | 9720 | 0 | 0
from_initial_state | IRI | 9720 | 9720 | 4.38607e-18 | 1.42109e-14
from_initial_state | JCI | 270 | 270 | 0 | 0
from_initial_state | PCRK | 9720 | 9720 | 3.23575e-16 | 3.55271e-15
from_initial_state | PSI | 9720 | 9720 | 5.71102e-21 | 5.55112e-17
from_initial_state | RDI | 9450 | 9450 | 0 | 0
from_initial_state | RUT | 9720 | 9720 | 1.19931e-19 | 1.11022e-16
from_initial_state | SCI | 9450 | 9450 | 0 | 0

### Families represented in saved initial and later states

Family | Saved states
--- | ---
BC_Initial_H | 1423
BC_Major_H | 2605
BC_Minor_H | 6052
RC_Initial_H | 127
RC_Minor_H | 161

### Initializer differences

These are a separate conditional test using current inventory and numeric-NULL-to-metadata-default substitution. They do not weaken the exact curve replay from supplied After0, but they prevent a claim of complete initialization equivalence.

Segment | Variable | Saved initial | Replay
--- | --- | --- | ---
1930009000000-012.260-1 | PMS_nAAV_CND_CSI | 5 | 5.00002
1930009000000-012.260-1 | PMS_nAAV_CND_JCI | 5 | 5.00002
50200600000EB-000.000-1 | PMS_nAAV_CND_CSI | 5 | 5.00002
50200600000EB-000.000-1 | PMS_nAAV_CND_JCI | 5 | 5.00002
2030817000000-000.000-1 | PMS_nAAV_CND_SCI | -0.1309 | 0
30200520000EB-045.170-1 | PMS_nAAV_CND_SCI | -0.1309 | 0

## Limits

This is a condition/distress forecaster with prescribed treatments. It does not run treatment triggers, optimize budgets, reproduce PV/RSL functions, certify policy feasibility, or establish real-world predictive accuracy. It reproduces saved dTIMS model output on the stated sample. CCI/PSI/ECI/SCI/RDI are tested for applicable asphalt cases and CSI/JCI for applicable concrete cases; inapplicable dummy indices are not counted as modeled physical condition.

The April workbook omits equivalent ages, hold state, rehab type/year, survey year and raw rut/fault anchors. Its conditional forecast borrows missing context from matched live data, applies captured initializers to workbook measurements where possible, and records any fallback in model_exceptions. It must not be presented as the original April run or as independently validated forecasts for the 46 unmatched names.

## Reproduce

```sh
python3 scripts/dtims_audit/nhs_tabulate.py
python3 scripts/dtims_audit/nhs_evaluate.py
MPLCONFIGDIR=/private/tmp/pms-matplotlib .venv/bin/python scripts/dtims_audit/nhs_report.py
python3 scripts/dtims_audit/nhs_validate.py
```

The workbook preparation script requires openpyxl. The fetcher requires the SSH master and hidden credential prompts; it reuses this dated snapshot’s cache. Make a new output directory for a new observation date. Coefficient and original expression rows are in the database; the evaluator uses the same-day audit’s attribute/function metadata copied through a read-only connection.
