# Deterioration curve diagnostics

Source: live test service, 2026-09-24. These numerical checks evaluate stored equations and lookup values, not the vendor DLL. Ages 0–50 are a diagnostic horizon, not an inferred validity range. Raw equations can fall below zero; the captured PSI wrapper explicitly floors its result at zero. The plot uses that lower floor for comparison, not a claim that every index has identical wrapping.

The referenced pavement table has 144 rows: 18 families × 8 indices. Its types are 137 Polynomial, 3 Linear, 3 Sigmoid, and 1 Log. The alternate table contains 187 rows and includes raw-measurement indices. See the formula catalog to establish references before replacing either table.

## Sampled curves

![Pavement equation samples](pavement-curves.png)

Polynomial and Linear curves use the exact stored `Curve_Equation` arithmetic. Sigmoid curves use the exact stored exponential expression for age > 0 and its analytical limit at age 0. The Log row is left unevaluated because vendor handling of its age-zero singularity is not established. The function catalog confirms that LOG is the natural logarithm. `audit_curve_samples` retains raw and lower-clipped values.

## Check results

Entity | Key | Check | Result | Detail
--- | --- | --- | --- | ---
Analysis_Lookup_Perf_Coef | BC_Minor_H_RDI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Minor_H_RDI | raw_range_ages_0_50 | observation | min=-5, max=5; first negative age=36
Analysis_Lookup_Perf_Coef | RC_Major_L_PSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Major_L_PSI | raw_range_ages_0_50 | observation | min=-2.5, max=5; first negative age=41
Analysis_Lookup_Perf_Coef | OT_Major_L_CCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Major_L_CCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | BC_Minor_H_SCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Minor_H_SCI | raw_range_ages_0_50 | observation | min=-12.5, max=5; first negative age=27
Analysis_Lookup_Perf_Coef | RC_Initial_L_SCI | monotonic_ages_0_50 | review | Increasing steps: [1, 2]
Analysis_Lookup_Perf_Coef | RC_Initial_L_SCI | raw_range_ages_0_50 | observation | min=-1.75, max=5.018; first negative age=44
Analysis_Lookup_Perf_Coef | BC_Major_H_CSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Major_H_CSI | raw_range_ages_0_50 | observation | min=-9.17077, max=5; first negative age=26
Analysis_Lookup_Perf_Coef | RC_Minor_H_CCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Minor_H_CCI | raw_range_ages_0_50 | observation | min=-5.9952e-13, max=5; first negative age=50
Analysis_Lookup_Perf_Coef | OT_Initial_H_NCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Initial_H_NCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | RC_Initial_H_ECI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Initial_H_ECI | raw_range_ages_0_50 | observation | min=2.20002e-12, max=5; first negative age=None
Analysis_Lookup_Perf_Coef | RC_Minor_L_SCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Minor_L_SCI | raw_range_ages_0_50 | observation | min=-2.5, max=5; first negative age=41
Analysis_Lookup_Perf_Coef | OT_Major_L_ECI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Major_L_ECI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | OT_Minor_H_ECI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Minor_H_ECI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | OT_Major_L_RDI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Major_L_RDI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | BC_Initial_L_CSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Initial_L_CSI | raw_range_ages_0_50 | observation | min=-4.85, max=5; first negative age=36
Analysis_Lookup_Perf_Coef | OT_Major_H_NCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Major_H_NCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | RC_Major_L_CCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Major_L_CCI | raw_range_ages_0_50 | observation | min=-5, max=5; first negative age=36
Analysis_Lookup_Perf_Coef | RC_Minor_H_RDI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Minor_H_RDI | raw_range_ages_0_50 | observation | min=-7.5, max=5; first negative age=32
Analysis_Lookup_Perf_Coef | BC_Minor_L_ECI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Minor_L_ECI | raw_range_ages_0_50 | observation | min=-10, max=5; first negative age=29
Analysis_Lookup_Perf_Coef | OT_Initial_H_SCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Initial_H_SCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | RC_Minor_H_ECI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Minor_H_ECI | raw_range_ages_0_50 | observation | min=-15, max=5; first negative age=26
Analysis_Lookup_Perf_Coef | RC_Initial_L_ECI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Initial_L_ECI | raw_range_ages_0_50 | observation | min=2.20002e-12, max=5; first negative age=None
Analysis_Lookup_Perf_Coef | BC_Minor_H_JCI | monotonic_ages_0_50 | review | Increasing steps: [1]
Analysis_Lookup_Perf_Coef | BC_Minor_H_JCI | raw_range_ages_0_50 | observation | min=-2.3, max=5.001; first negative age=42
Analysis_Lookup_Perf_Coef | BC_Initial_L_JCI | monotonic_ages_0_50 | review | Increasing steps: [1, 2, 3]
Analysis_Lookup_Perf_Coef | BC_Initial_L_JCI | raw_range_ages_0_50 | observation | min=-1.55, max=5.03; first negative age=45
Analysis_Lookup_Perf_Coef | BC_Minor_H_ECI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Minor_H_ECI | raw_range_ages_0_50 | observation | min=-10, max=5; first negative age=29
Analysis_Lookup_Perf_Coef | RC_Initial_H_CSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Initial_H_CSI | raw_range_ages_0_50 | observation | min=-7.5, max=5; first negative age=32
Analysis_Lookup_Perf_Coef | BC_Minor_L_NCI | equation_sampling | not_evaluated | Stored equation explicitly contains Not Predicted; no age variable is invented
Analysis_Lookup_Perf_Coef | BC_Initial_H_RDI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Initial_H_RDI | raw_range_ages_0_50 | observation | min=-5, max=5; first negative age=36
Analysis_Lookup_Perf_Coef | RC_Initial_L_CSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Initial_L_CSI | raw_range_ages_0_50 | observation | min=-7.3, max=5; first negative age=33
Analysis_Lookup_Perf_Coef | RC_Minor_L_CSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Minor_L_CSI | raw_range_ages_0_50 | observation | min=-10, max=5; first negative age=29
Analysis_Lookup_Perf_Coef | OT_Major_L_JCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Major_L_JCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | BC_Major_H_JCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Major_H_JCI | raw_range_ages_0_50 | observation | min=-2.5, max=5; first negative age=41
Analysis_Lookup_Perf_Coef | RC_Major_H_JCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Major_H_JCI | raw_range_ages_0_50 | observation | min=-2.5, max=5; first negative age=41
Analysis_Lookup_Perf_Coef | OT_Initial_L_NCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Initial_L_NCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | OT_Initial_L_JCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Initial_L_JCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | OT_Minor_H_RDI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Minor_H_RDI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | OT_Major_L_SCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Major_L_SCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | BC_Major_H_CCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Major_H_CCI | raw_range_ages_0_50 | observation | min=-10, max=5; first negative age=29
Analysis_Lookup_Perf_Coef | OT_Minor_L_SCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Minor_L_SCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | RC_Initial_H_PSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Initial_H_PSI | raw_range_ages_0_50 | observation | min=-5, max=5; first negative age=36
Analysis_Lookup_Perf_Coef | BC_Initial_L_ECI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Initial_L_ECI | raw_range_ages_0_50 | observation | min=-10.6695, max=5; first negative age=22
Analysis_Lookup_Perf_Coef | RC_Minor_H_SCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Minor_H_SCI | raw_range_ages_0_50 | observation | min=-15, max=5; first negative age=26
Analysis_Lookup_Perf_Coef | RC_Major_H_CSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Major_H_CSI | raw_range_ages_0_50 | observation | min=-10, max=5; first negative age=29
Analysis_Lookup_Perf_Coef | RC_Initial_L_RDI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Initial_L_RDI | raw_range_ages_0_50 | observation | min=2.20002e-12, max=5; first negative age=None
Analysis_Lookup_Perf_Coef | RC_Minor_L_JCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Minor_L_JCI | raw_range_ages_0_50 | observation | min=-5.9952e-13, max=5; first negative age=50
Analysis_Lookup_Perf_Coef | RC_Minor_H_NCI | equation_sampling | not_evaluated | Stored equation explicitly contains Not Predicted; no age variable is invented
Analysis_Lookup_Perf_Coef | RC_Initial_H_RDI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Initial_H_RDI | raw_range_ages_0_50 | observation | min=2.20002e-12, max=5; first negative age=None
Analysis_Lookup_Perf_Coef | OT_Major_H_JCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Major_H_JCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | RC_Initial_H_JCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Initial_H_JCI | raw_range_ages_0_50 | observation | min=-2.5, max=5; first negative age=41
Analysis_Lookup_Perf_Coef | BC_Initial_H_CCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Initial_H_CCI | raw_range_ages_0_50 | observation | min=-7.5, max=5; first negative age=32
Analysis_Lookup_Perf_Coef | BC_Initial_H_NCI | equation_sampling | not_evaluated | Stored equation explicitly contains Not Predicted; no age variable is invented
Analysis_Lookup_Perf_Coef | OT_Initial_L_ECI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Initial_L_ECI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | OT_Initial_H_PSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Initial_H_PSI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | OT_Major_H_RDI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Major_H_RDI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | BC_Minor_H_NCI | equation_sampling | not_evaluated | Stored equation explicitly contains Not Predicted; no age variable is invented
Analysis_Lookup_Perf_Coef | BC_Major_L_ECI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Major_L_ECI | raw_range_ages_0_50 | observation | min=-12.5, max=5; first negative age=27
Analysis_Lookup_Perf_Coef | RC_Initial_L_CCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Initial_L_CCI | raw_range_ages_0_50 | observation | min=-5, max=5; first negative age=36
Analysis_Lookup_Perf_Coef | RC_Major_L_JCI | monotonic_ages_0_50 | review | Increasing steps: [1, 2]
Analysis_Lookup_Perf_Coef | RC_Major_L_JCI | raw_range_ages_0_50 | observation | min=-1.95, max=5.01; first negative age=43
Analysis_Lookup_Perf_Coef | OT_Initial_L_CSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Initial_L_CSI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | BC_Initial_L_RDI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Initial_L_RDI | raw_range_ages_0_50 | observation | min=-5, max=5; first negative age=36
Analysis_Lookup_Perf_Coef | BC_Initial_L_PSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Initial_L_PSI | raw_range_ages_0_50 | observation | min=-5, max=5; first negative age=36
Analysis_Lookup_Perf_Coef | OT_Initial_H_CSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Initial_H_CSI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | OT_Minor_L_CCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Minor_L_CCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | OT_Initial_H_JCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Initial_H_JCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | OT_Major_H_SCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Major_H_SCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | RC_Minor_L_ECI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Minor_L_ECI | raw_range_ages_0_50 | observation | min=-2.5, max=5; first negative age=41
Analysis_Lookup_Perf_Coef | OT_Minor_L_ECI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Minor_L_ECI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | OT_Minor_H_JCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Minor_H_JCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | BC_Major_L_PSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Major_L_PSI | raw_range_ages_0_50 | observation | min=-25, max=5; first negative age=21
Analysis_Lookup_Perf_Coef | BC_Major_H_PSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Major_H_PSI | raw_range_ages_0_50 | observation | min=-7.5, max=5; first negative age=32
Analysis_Lookup_Perf_Coef | RC_Initial_L_NCI | equation_sampling | not_evaluated | Stored equation explicitly contains Not Predicted; no age variable is invented
Analysis_Lookup_Perf_Coef | RC_Minor_H_JCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Minor_H_JCI | raw_range_ages_0_50 | observation | min=-2.5, max=5; first negative age=41
Analysis_Lookup_Perf_Coef | RC_Major_H_CCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Major_H_CCI | raw_range_ages_0_50 | observation | min=-5, max=5; first negative age=36
Analysis_Lookup_Perf_Coef | BC_Major_L_CSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Major_L_CSI | raw_range_ages_0_50 | observation | min=-45, max=5; first negative age=16
Analysis_Lookup_Perf_Coef | RC_Major_H_ECI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Major_H_ECI | raw_range_ages_0_50 | observation | min=-2.5, max=5; first negative age=41
Analysis_Lookup_Perf_Coef | OT_Initial_H_CCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Initial_H_CCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | RC_Minor_L_RDI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Minor_L_RDI | raw_range_ages_0_50 | observation | min=-5, max=5; first negative age=36
Analysis_Lookup_Perf_Coef | RC_Minor_L_CCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Minor_L_CCI | raw_range_ages_0_50 | observation | min=-7.5, max=5; first negative age=32
Analysis_Lookup_Perf_Coef | RC_Minor_L_NCI | equation_sampling | not_evaluated | Stored equation explicitly contains Not Predicted; no age variable is invented
Analysis_Lookup_Perf_Coef | OT_Initial_L_SCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Initial_L_SCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | BC_Major_L_JCI | equation_sampling | not_evaluated | Vendor age-zero convention is not established; LOG is documented as natural logarithm
Analysis_Lookup_Perf_Coef | OT_Initial_H_RDI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Initial_H_RDI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | OT_Minor_L_NCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Minor_L_NCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | RC_Major_H_RDI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Major_H_RDI | raw_range_ages_0_50 | observation | min=-2.5, max=5; first negative age=41
Analysis_Lookup_Perf_Coef | OT_Minor_L_RDI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Minor_L_RDI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | OT_Minor_H_NCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Minor_H_NCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | BC_Minor_H_CSI | monotonic_ages_0_50 | review | Increasing steps: [1]
Analysis_Lookup_Perf_Coef | BC_Minor_H_CSI | raw_range_ages_0_50 | observation | min=-12.1, max=5.001; first negative age=28
Analysis_Lookup_Perf_Coef | BC_Major_L_CCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Major_L_CCI | raw_range_ages_0_50 | observation | min=-27.5, max=5; first negative age=20
Analysis_Lookup_Perf_Coef | BC_Minor_L_RDI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Minor_L_RDI | raw_range_ages_0_50 | observation | min=-5, max=5; first negative age=36
Analysis_Lookup_Perf_Coef | RC_Minor_H_CSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Minor_H_CSI | raw_range_ages_0_50 | observation | min=-9.9, max=5; first negative age=30
Analysis_Lookup_Perf_Coef | BC_Major_L_RDI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Major_L_RDI | raw_range_ages_0_50 | observation | min=-5, max=5; first negative age=36
Analysis_Lookup_Perf_Coef | RC_Minor_H_PSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Minor_H_PSI | raw_range_ages_0_50 | observation | min=-5.9952e-13, max=5; first negative age=50
Analysis_Lookup_Perf_Coef | RC_Major_L_NCI | equation_sampling | not_evaluated | Stored equation explicitly contains Not Predicted; no age variable is invented
Analysis_Lookup_Perf_Coef | RC_Major_H_SCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Major_H_SCI | raw_range_ages_0_50 | observation | min=-10, max=5; first negative age=29
Analysis_Lookup_Perf_Coef | RC_Initial_L_PSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Initial_L_PSI | raw_range_ages_0_50 | observation | min=-5, max=5; first negative age=36
Analysis_Lookup_Perf_Coef | OT_Minor_L_CSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Minor_L_CSI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | BC_Initial_H_JCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Initial_H_JCI | raw_range_ages_0_50 | observation | min=-2.5, max=5; first negative age=41
Analysis_Lookup_Perf_Coef | OT_Minor_H_SCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Minor_H_SCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | OT_Major_H_ECI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Major_H_ECI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | RC_Major_L_RDI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Major_L_RDI | raw_range_ages_0_50 | observation | min=-7.5, max=5; first negative age=32
Analysis_Lookup_Perf_Coef | OT_Minor_L_PSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Minor_L_PSI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | BC_Initial_H_CSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Initial_H_CSI | raw_range_ages_0_50 | observation | min=-7.5, max=5; first negative age=32
Analysis_Lookup_Perf_Coef | BC_Minor_L_CSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Minor_L_CSI | raw_range_ages_0_50 | observation | min=-10, max=5; first negative age=29
Analysis_Lookup_Perf_Coef | BC_Minor_H_CCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Minor_H_CCI | raw_range_ages_0_50 | observation | min=-12.5, max=5; first negative age=27
Analysis_Lookup_Perf_Coef | OT_Initial_L_CCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Initial_L_CCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | BC_Minor_L_JCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Minor_L_JCI | raw_range_ages_0_50 | observation | min=-2.5, max=5; first negative age=41
Analysis_Lookup_Perf_Coef | BC_Initial_H_PSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Initial_H_PSI | raw_range_ages_0_50 | observation | min=-7.5, max=5; first negative age=32
Analysis_Lookup_Perf_Coef | BC_Major_L_NCI | equation_sampling | not_evaluated | Stored equation explicitly contains Not Predicted; no age variable is invented
Analysis_Lookup_Perf_Coef | BC_Major_H_NCI | equation_sampling | not_evaluated | Stored equation explicitly contains Not Predicted; no age variable is invented
Analysis_Lookup_Perf_Coef | RC_Initial_H_CCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Initial_H_CCI | raw_range_ages_0_50 | observation | min=-5, max=5; first negative age=36
Analysis_Lookup_Perf_Coef | BC_Minor_L_CCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Minor_L_CCI | raw_range_ages_0_50 | observation | min=-10, max=5; first negative age=29
Analysis_Lookup_Perf_Coef | OT_Major_L_CSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Major_L_CSI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | OT_Major_H_CCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Major_H_CCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | RC_Initial_L_JCI | monotonic_ages_0_50 | review | Increasing steps: [1]
Analysis_Lookup_Perf_Coef | RC_Initial_L_JCI | raw_range_ages_0_50 | observation | min=-2.05, max=5.006; first negative age=43
Analysis_Lookup_Perf_Coef | BC_Initial_L_NCI | equation_sampling | not_evaluated | Stored equation explicitly contains Not Predicted; no age variable is invented
Analysis_Lookup_Perf_Coef | BC_Minor_L_PSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Minor_L_PSI | raw_range_ages_0_50 | observation | min=-7.5, max=5; first negative age=32
Analysis_Lookup_Perf_Coef | OT_Initial_L_PSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Initial_L_PSI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | OT_Major_L_PSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Major_L_PSI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | BC_Major_H_ECI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Major_H_ECI | raw_range_ages_0_50 | observation | min=-7.5, max=5; first negative age=32
Analysis_Lookup_Perf_Coef | OT_Initial_H_ECI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Initial_H_ECI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | BC_Initial_L_SCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Initial_L_SCI | raw_range_ages_0_50 | observation | min=-2.5, max=5; first negative age=41
Analysis_Lookup_Perf_Coef | BC_Minor_L_SCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Minor_L_SCI | raw_range_ages_0_50 | observation | min=-17.5, max=5; first negative age=24
Analysis_Lookup_Perf_Coef | BC_Major_L_SCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Major_L_SCI | raw_range_ages_0_50 | observation | min=-30, max=5; first negative age=19
Analysis_Lookup_Perf_Coef | RC_Minor_L_PSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Minor_L_PSI | raw_range_ages_0_50 | observation | min=-5, max=5; first negative age=36
Analysis_Lookup_Perf_Coef | BC_Minor_H_PSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Minor_H_PSI | raw_range_ages_0_50 | observation | min=-12.5, max=5; first negative age=27
Analysis_Lookup_Perf_Coef | OT_Minor_H_CCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Minor_H_CCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | BC_Major_H_RDI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Major_H_RDI | raw_range_ages_0_50 | observation | min=-2.5, max=5; first negative age=41
Analysis_Lookup_Perf_Coef | RC_Major_L_ECI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Major_L_ECI | raw_range_ages_0_50 | observation | min=-12.5, max=5; first negative age=27
Analysis_Lookup_Perf_Coef | RC_Initial_H_SCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Initial_H_SCI | raw_range_ages_0_50 | observation | min=-2.5, max=5; first negative age=41
Analysis_Lookup_Perf_Coef | BC_Initial_L_CCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Initial_L_CCI | raw_range_ages_0_50 | observation | min=-5, max=5; first negative age=36
Analysis_Lookup_Perf_Coef | OT_Major_H_PSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Major_H_PSI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | BC_Initial_H_ECI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Initial_H_ECI | raw_range_ages_0_50 | observation | min=-5, max=5; first negative age=36
Analysis_Lookup_Perf_Coef | BC_Major_H_SCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Major_H_SCI | raw_range_ages_0_50 | observation | min=-10, max=5; first negative age=29
Analysis_Lookup_Perf_Coef | BC_Initial_H_SCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | BC_Initial_H_SCI | raw_range_ages_0_50 | observation | min=-9.17077, max=5; first negative age=26
Analysis_Lookup_Perf_Coef | OT_Initial_L_RDI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Initial_L_RDI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | RC_Major_L_CSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Major_L_CSI | raw_range_ages_0_50 | observation | min=-9.8, max=5; first negative age=30
Analysis_Lookup_Perf_Coef | OT_Minor_L_JCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Minor_L_JCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | RC_Major_L_SCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Major_L_SCI | raw_range_ages_0_50 | observation | min=-12.5, max=5; first negative age=27
Analysis_Lookup_Perf_Coef | RC_Major_H_NCI | equation_sampling | not_evaluated | Stored equation explicitly contains Not Predicted; no age variable is invented
Analysis_Lookup_Perf_Coef | OT_Minor_H_CSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Minor_H_CSI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | OT_Minor_H_PSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Minor_H_PSI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | RC_Major_H_PSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | RC_Major_H_PSI | raw_range_ages_0_50 | observation | min=-5, max=5; first negative age=36
Analysis_Lookup_Perf_Coef | RC_Initial_H_NCI | equation_sampling | not_evaluated | Stored equation explicitly contains Not Predicted; no age variable is invented
Analysis_Lookup_Perf_Coef | OT_Major_H_CSI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Major_H_CSI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Analysis_Lookup_Perf_Coef | OT_Major_L_NCI | monotonic_ages_0_50 | pass | Increasing steps: []
Analysis_Lookup_Perf_Coef | OT_Major_L_NCI | raw_range_ages_0_50 | observation | min=0, max=0; first negative age=None
Bridge_Lookup_CR_Life | SUP_R_1 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_P_1 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | DCK_4 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | CUL_C_5 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_R_4 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_R_6 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | CUL_C_3 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_S_5 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | CUL_C_2 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_R_8 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | 70 | years_00_50 | observation | Numeric-key coefficient/CR template row; all YR cells null. Not treated as a missing component trajectory.
Bridge_Lookup_CR_Life | SUB_9 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_T_6 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | CUL_S_8 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_S_8 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | DCK_7 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_P_6 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_S_7 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_P_3 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | CUL_S_5 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | CUL_S_4 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_T_3 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | 40 | years_00_50 | observation | Numeric-key coefficient/CR template row; all YR cells null. Not treated as a missing component trajectory.
Bridge_Lookup_CR_Life | CUL_C_6 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_R_9 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | DCK_8 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_R_3 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_S_6 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_T_8 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_T_7 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_P_2 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_T_1 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | DCK_P_6 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_S_1 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | DCK_3 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | CUL_S_7 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUB_5 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_R_7 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_T_9 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUB_7 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_S_2 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | DCK_P_9 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | 50 | years_00_50 | observation | Numeric-key coefficient/CR template row; all YR cells null. Not treated as a missing component trajectory.
Bridge_Lookup_CR_Life | CUL_C_7 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | DCK_P_7 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | CUL_S_1 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_P_4 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | 30 | years_00_50 | observation | Numeric-key coefficient/CR template row; all YR cells null. Not treated as a missing component trajectory.
Bridge_Lookup_CR_Life | CUL_C_8 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | 80 | years_00_50 | observation | Numeric-key coefficient/CR template row; all YR cells null. Not treated as a missing component trajectory.
Bridge_Lookup_CR_Life | SUB_3 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_S_9 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_S_4 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_P_8 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | DCK_P_5 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | DCK_2 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | DCK_P_2 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_P_5 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | DCK_P_4 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUB_2 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_P_7 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | CUL_C_1 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_P_9 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | DCK_1 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_R_2 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | CUL_S_3 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | DCK_5 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUB_1 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUB_6 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_R_5 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUB_4 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_S_3 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | DCK_P_1 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | CUL_S_6 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | DCK_P_8 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_T_5 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | CUL_C_9 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | DCK_6 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | DCK_P_3 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_T_2 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUB_8 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | CUL_S_2 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | CUL_C_4 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | SUP_T_4 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | 60 | years_00_50 | observation | Numeric-key coefficient/CR template row; all YR cells null. Not treated as a missing component trajectory.
Bridge_Lookup_CR_Life | CUL_S_9 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Lookup_CR_Life | DCK_9 | years_00_50 | pass | missing=[]; increasing=[]; outside 0..9=[]
Bridge_Analysis_Lookup_Element_Curves | 306_CS1 | base_transition_row | pass | row=[1.0, 0.0, 0.0, 0.0]; factor=1.823; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 1130_CS4 | base_transition_row | pass | row=[0.0, 0.0, 0.0, 1.0]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 305_CS1 | base_transition_row | pass | row=[1.0, 0.0, 0.0, 0.0]; factor=0.556; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 515_CS2 | base_transition_row | pass | row=[0.0, 0.9330329915368074, 0.06696700846319259, 0.0]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 302_CS3 | base_transition_row | pass | row=[0.0, 0.0, 0.8705505632961241, 0.12944943670387588]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 300_CS4 | base_transition_row | pass | row=[0.0, 0.0, 0.0, 1.0]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 301_CS2 | base_transition_row | pass | row=[0.0, 0.9057236642639067, 0.09427633573609329, 0.0]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 300_CS3 | base_transition_row | pass | row=[0.0, 0.0, 0.8705505632961241, 0.12944943670387588]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 515_CS4 | base_transition_row | pass | row=[0.0, 0.0, 0.0, 1.0]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 305_CS2 | base_transition_row | pass | row=[0.0, 0.9792145972460015, 0.02078540275399865, 0.0]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 303_CS4 | base_transition_row | pass | row=[0.0, 0.0, 0.0, 1.0]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 304_CS4 | base_transition_row | pass | row=[0.0, 0.0, 0.0, 1.0]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 1080_CS1 | base_transition_row | pass | row=[1.0, 0.0, 0.0, 0.0]; factor=0.8558; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 300_CS2 | base_transition_row | pass | row=[0.0, 0.9057236642639067, 0.09427633573609329, 0.0]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 1130_CS3 | base_transition_row | pass | row=[0.0, 0.0, 0.8705505632961241, 0.12944943670387588]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 1080_CS3 | base_transition_row | pass | row=[0.0, 0.0, 0.7937005259840997, 0.20629947401590018]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 306_CS3 | base_transition_row | pass | row=[0.0, 0.0, 0.8705505632961241, 0.12944943670387588]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 305_CS3 | base_transition_row | pass | row=[0.0, 0.0, 0.9548416039104165, 0.045158396089583504]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 301_CS3 | base_transition_row | pass | row=[0.0, 0.0, 0.8705505632961241, 0.12944943670387588]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 303_CS2 | base_transition_row | pass | row=[0.0, 0.9170040432046713, 0.08299595679532878, 0.0]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 304_CS3 | base_transition_row | pass | row=[0.0, 0.0, 0.9330329915368074, 0.06696700846319259]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 300_CS1 | base_transition_row | pass | row=[1.0, 0.0, 0.0, 0.0]; factor=1.823; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 306_CS2 | base_transition_row | pass | row=[0.0, 0.9057236642639067, 0.09427633573609329, 0.0]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 515_CS3 | base_transition_row | pass | row=[0.0, 0.0, 0.8705505632961241, 0.12944943670387588]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 302_CS4 | base_transition_row | pass | row=[0.0, 0.0, 0.0, 1.0]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 304_CS2 | base_transition_row | pass | row=[0.0, 0.9438743126816935, 0.05612568731830647, 0.0]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 1130_CS1 | base_transition_row | pass | row=[1.0, 0.0, 0.0, 0.0]; factor=0.3225; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 1130_CS2 | base_transition_row | pass | row=[0.0, 0.9330329915368074, 0.06696700846319259, 0.0]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 306_CS4 | base_transition_row | pass | row=[0.0, 0.0, 0.0, 1.0]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 304_CS1 | base_transition_row | pass | row=[1.0, 0.0, 0.0, 0.0]; factor=0.556; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 1080_CS4 | base_transition_row | pass | row=[0.0, 0.0, 0.0, 1.0]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 302_CS2 | base_transition_row | pass | row=[0.0, 0.9057236642639067, 0.09427633573609329, 0.0]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 515_CS1 | base_transition_row | pass | row=[1.0, 0.0, 0.0, 0.0]; factor=0.20944; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 305_CS4 | base_transition_row | pass | row=[0.0, 0.0, 0.0, 1.0]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 303_CS3 | base_transition_row | pass | row=[0.0, 0.0, 0.8908987181403392, 0.10910128185966074]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 302_CS1 | base_transition_row | pass | row=[1.0, 0.0, 0.0, 0.0]; factor=1.823; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 301_CS1 | base_transition_row | pass | row=[1.0, 0.0, 0.0, 0.0]; factor=1.823; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 1080_CS2 | base_transition_row | pass | row=[0.0, 0.8908987181403392, 0.10910128185966074, 0.0]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 301_CS4 | base_transition_row | pass | row=[0.0, 0.0, 0.0, 1.0]; factor=0.0; dynamic factor adjustment lives in runtime expressions
Bridge_Analysis_Lookup_Element_Curves | 303_CS1 | base_transition_row | pass | row=[1.0, 0.0, 0.0, 0.0]; factor=0.85; dynamic factor adjustment lives in runtime expressions

## Differences between the two pavement coefficient tables

Differences below compare matching keys. They are configuration differences, not evidence that the alternate table is used.

Key | Field | Referenced table | Alternate table
--- | --- | --- | ---
BC_Initial_H_CCI | C2 | -0.00499999999999912 | -0.005525
BC_Initial_H_CCI | Maximum | 5 | 4.0
BC_Initial_H_CSI | C1 | 0.0 | -0.135824
BC_Initial_H_CSI | C2 | -0.00499999999999912 | 0.0
BC_Initial_H_CSI | Curve_Type | Polynomial | Linear
BC_Initial_H_ECI | C2 | -0.00399999999999912 | -0.004653
BC_Initial_H_JCI | C2 | -0.00299999999999912 | -0.019828
BC_Initial_H_NCI | C2 | -0.00499999999999912 | -0.002725
BC_Initial_H_PSI | C2 | -0.00499999999999912 | -0.012472
BC_Initial_H_RDI | C2 | -0.00399999999999912 | -0.010001
BC_Initial_H_SCI | C1 | 85.0 | -0.011
BC_Initial_H_SCI | C2 | 115.0 | 1.892
BC_Initial_H_SCI | C3 | 0.7 | 0.0
BC_Initial_H_SCI | Curve_Type | Sigmoid | Power
BC_Initial_H_SCI | Maximum | 5 | 4.77
BC_Initial_L_CCI | C2 | -0.00399999999999912 | -0.003183
BC_Initial_L_CCI | Maximum | 5 | 4.0
BC_Initial_L_CSI | C1 | 0.003 | -0.135824
BC_Initial_L_CSI | C2 | -0.00399999999999912 | 0.0
BC_Initial_L_CSI | Curve_Type | Polynomial | Linear
BC_Initial_L_ECI | C1 | 85.0 | 0.0
BC_Initial_L_ECI | C2 | 120.0 | -0.007084
BC_Initial_L_ECI | C3 | 0.6 | 0.0
BC_Initial_L_ECI | Curve_Type | Sigmoid | Polynomial
BC_Initial_L_JCI | C1 | 0.019 | 0.0
BC_Initial_L_JCI | C2 | -0.00299999999999912 | -0.016005
BC_Initial_L_NCI | C2 | -0.00299999999999912 | -0.005041
BC_Initial_L_PSI | C2 | -0.00399999999999912 | -0.011904
BC_Initial_L_RDI | C2 | -0.00399999999999912 | -0.009384
BC_Initial_L_SCI | C1 | 0.0 | -0.009
BC_Initial_L_SCI | C2 | -0.00299999999999912 | 1.892
BC_Initial_L_SCI | Curve_Type | Polynomial | Power
BC_Initial_L_SCI | Maximum | 5 | 4.805
BC_Major_H_CCI | C2 | -0.00599999999999912 | -0.002514
BC_Major_H_CCI | Maximum | 5 | 4.0
BC_Major_H_CSI | C1 | 85.0 | -0.135824
BC_Major_H_CSI | C2 | 115.0 | 0.0
BC_Major_H_CSI | C3 | 0.7 | 0.0
BC_Major_H_CSI | Curve_Type | Sigmoid | Linear
BC_Major_H_ECI | C2 | -0.00499999999999912 | -0.004143
BC_Major_H_JCI | C2 | -0.00299999999999912 | -0.012103
BC_Major_H_NCI | C2 | -0.00499999999999912 | -0.005665
BC_Major_H_PSI | C2 | -0.00499999999999912 | -0.012549
BC_Major_H_RDI | C2 | -0.00299999999999912 | -0.008371
BC_Major_H_SCI | C1 | 0.0 | -0.008
BC_Major_H_SCI | C2 | -0.00599999999999912 | 1.892
BC_Major_H_SCI | Curve_Type | Polynomial | Power
BC_Major_H_SCI | Maximum | 5 | 4.823
BC_Major_L_CCI | C2 | -0.0129999999999991 | -0.002679
BC_Major_L_CCI | Maximum | 5 | 4.0
BC_Major_L_CSI | C1 | 0.0 | -0.135824
BC_Major_L_CSI | C2 | -0.0199999999999991 | 0.0
BC_Major_L_CSI | Curve_Type | Polynomial | Linear
BC_Major_L_ECI | C2 | -0.00699999999999912 | -0.006435
BC_Major_L_JCI | C1 | 3.1 | 0.0
BC_Major_L_JCI | C2 | -11.5 | -0.014027
BC_Major_L_JCI | C3 | 1.7 | 0.0
BC_Major_L_JCI | Curve_Type | Log | Polynomial
BC_Major_L_NCI | C2 | -0.0139999999999991 | -0.004912
BC_Major_L_PSI | C2 | -0.0119999999999991 | -0.013202
BC_Major_L_RDI | C2 | -0.00399999999999912 | -0.01572
BC_Major_L_SCI | C1 | 0.0 | -0.008
BC_Major_L_SCI | C2 | -0.0139999999999991 | 1.892
BC_Major_L_SCI | Curve_Type | Polynomial | Power
BC_Major_L_SCI | Maximum | 5 | 4.832
BC_Minor_H_CCI | C2 | -0.00699999999999912 | -0.004467
BC_Minor_H_CCI | Maximum | 5 | 4.0
BC_Minor_H_CSI | C1 | 0.008 | -0.135824
BC_Minor_H_CSI | C2 | -0.00699999999999912 | 0.0
BC_Minor_H_CSI | Curve_Type | Polynomial | Linear
BC_Minor_H_ECI | C2 | -0.00599999999999912 | -0.007474
BC_Minor_H_JCI | C1 | 0.004 | 0.0
BC_Minor_H_JCI | C2 | -0.00299999999999912 | -0.019051
BC_Minor_H_NCI | C2 | -0.00799999999999912 | -0.008212
BC_Minor_H_PSI | C2 | -0.00699999999999912 | -0.012017
BC_Minor_H_RDI | C2 | -0.00399999999999912 | -0.011139
BC_Minor_H_SCI | C1 | 0.0 | -0.009
BC_Minor_H_SCI | C2 | -0.00699999999999912 | 1.892
BC_Minor_H_SCI | Curve_Type | Polynomial | Power
BC_Minor_H_SCI | Maximum | 5 | 4.808
BC_Minor_L_CCI | C2 | -0.00599999999999912 | -0.00603
BC_Minor_L_CCI | Maximum | 5 | 4.0
BC_Minor_L_CSI | C1 | 0.0 | -0.135824
BC_Minor_L_CSI | C2 | -0.00599999999999912 | 0.0
BC_Minor_L_CSI | Curve_Type | Polynomial | Linear
BC_Minor_L_ECI | C2 | -0.00599999999999912 | -0.005705
BC_Minor_L_JCI | C2 | -0.00299999999999912 | -0.01653
BC_Minor_L_NCI | C2 | -0.00999999999999912 | -0.006585
BC_Minor_L_PSI | C2 | -0.00499999999999912 | -0.013994
BC_Minor_L_RDI | C2 | -0.00399999999999912 | -0.011576
BC_Minor_L_SCI | C1 | 0.0 | -0.01
BC_Minor_L_SCI | C2 | -0.00899999999999912 | 1.892
BC_Minor_L_SCI | Curve_Type | Polynomial | Power
BC_Minor_L_SCI | Maximum | 5 | 4.793
RC_Initial_H_CCI | C2 | -0.00399999999999912 | -0.003333
RC_Initial_H_CCI | Maximum | 5 | 4.0
RC_Initial_H_CSI | C1 | 0.0 | -0.135824
RC_Initial_H_CSI | C2 | -0.00499999999999912 | 0.0
RC_Initial_H_CSI | Curve_Type | Polynomial | Linear
RC_Initial_H_ECI | C2 | -0.00199999999999912 | -0.006604
RC_Initial_H_JCI | C2 | -0.00299999999999912 | -0.00516
RC_Initial_H_NCI | C2 | -0.00299999999999912 | -0.005902
RC_Initial_H_PSI | C2 | -0.00399999999999912 | -0.011485
RC_Initial_H_RDI | C2 | -0.00199999999999912 | -0.00635
RC_Initial_H_SCI | C1 | 0.0 | -0.008
RC_Initial_H_SCI | C2 | -0.00299999999999912 | 1.892
RC_Initial_H_SCI | Curve_Type | Polynomial | Power
RC_Initial_H_SCI | Maximum | 5 | 4.834
RC_Initial_L_CCI | C2 | -0.00399999999999912 | -0.003002
RC_Initial_L_CCI | Maximum | 5 | 4.0
RC_Initial_L_CSI | C1 | 0.004 | -0.135824
RC_Initial_L_CSI | C2 | -0.00499999999999912 | 0.0
RC_Initial_L_CSI | Curve_Type | Polynomial | Linear
RC_Initial_L_ECI | C2 | -0.00199999999999912 | -0.006604
RC_Initial_L_JCI | C1 | 0.009 | 0.0
RC_Initial_L_JCI | C2 | -0.00299999999999912 | -0.00516
RC_Initial_L_NCI | C2 | -0.00299999999999912 | -0.005902
RC_Initial_L_PSI | C2 | -0.00399999999999912 | -0.010162
RC_Initial_L_RDI | C2 | -0.00199999999999912 | -0.005945
RC_Initial_L_SCI | C1 | 0.015 | -0.008
RC_Initial_L_SCI | C2 | -0.00299999999999912 | 1.892
RC_Initial_L_SCI | Curve_Type | Polynomial | Power
RC_Initial_L_SCI | Maximum | 5 | 4.824
RC_Major_H_CCI | C2 | -0.00399999999999912 | -0.003122
RC_Major_H_CCI | Maximum | 5 | 4.0
RC_Major_H_CSI | C1 | 0.0 | -0.2
RC_Major_H_CSI | C2 | -0.00599999999999912 | 0.0
RC_Major_H_CSI | Curve_Type | Polynomial | Linear
RC_Major_H_ECI | C2 | -0.00299999999999912 | -0.006604
RC_Major_H_JCI | C2 | -0.00299999999999912 | -0.007293
RC_Major_H_NCI | C2 | -0.00599999999999912 | -0.005902
RC_Major_H_PSI | C2 | -0.00399999999999912 | -0.011934
RC_Major_H_RDI | C2 | -0.00299999999999912 | -0.010181
RC_Major_H_SCI | C1 | 0.0 | -0.008
RC_Major_H_SCI | C2 | -0.00599999999999912 | 1.892
RC_Major_H_SCI | Curve_Type | Polynomial | Power
RC_Major_H_SCI | Maximum | 5 | 4.827
RC_Major_L_CCI | C2 | -0.00399999999999912 | -0.002107
RC_Major_L_CCI | Maximum | 5 | 4.0
RC_Major_L_CSI | C1 | 0.004 | -0.052555
RC_Major_L_CSI | C2 | -0.00599999999999912 | 0.0
RC_Major_L_CSI | Curve_Type | Polynomial | Linear
RC_Major_L_ECI | C2 | -0.00699999999999912 | -0.006604
RC_Major_L_JCI | C1 | 0.011 | 0.0
RC_Major_L_JCI | C2 | -0.00299999999999912 | -0.007293
RC_Major_L_NCI | C2 | -0.00899999999999912 | -0.005902
RC_Major_L_PSI | C2 | -0.00299999999999912 | -0.012678
RC_Major_L_RDI | C2 | -0.00499999999999912 | -0.006487
RC_Major_L_SCI | C1 | 0.0 | -0.007
RC_Major_L_SCI | C2 | -0.00699999999999912 | 1.892
RC_Major_L_SCI | Curve_Type | Polynomial | Power
RC_Major_L_SCI | Maximum | 5 | 4.852
RC_Minor_H_CCI | C1 | -0.100000000000012 | 0.0
RC_Minor_H_CCI | C2 | 0.0 | -0.001995
RC_Minor_H_CCI | Curve_Type | Linear | Polynomial
RC_Minor_H_CCI | Maximum | 5 | 4.0
RC_Minor_H_CSI | C1 | 0.002 | -0.05
RC_Minor_H_CSI | C2 | -0.00599999999999912 | 0.0
RC_Minor_H_CSI | Curve_Type | Polynomial | Linear
RC_Minor_H_ECI | C2 | -0.00799999999999912 | -0.006604
RC_Minor_H_JCI | C2 | -0.00299999999999912 | -0.005513
RC_Minor_H_NCI | C2 | -0.00899999999999912 | -0.005902
RC_Minor_H_PSI | C1 | -0.100000000000012 | 0.0
RC_Minor_H_PSI | C2 | 0.0 | -0.010648
RC_Minor_H_PSI | Curve_Type | Linear | Polynomial
RC_Minor_H_RDI | C2 | -0.00499999999999912 | -0.00641
RC_Minor_H_SCI | C1 | 0.0 | -0.008
RC_Minor_H_SCI | C2 | -0.00799999999999912 | 1.892
RC_Minor_H_SCI | Curve_Type | Polynomial | Power
RC_Minor_H_SCI | Maximum | 5 | 4.828
RC_Minor_L_CCI | C2 | -0.00499999999999912 | -0.005133
RC_Minor_L_CCI | Maximum | 5 | 4.0
RC_Minor_L_CSI | C1 | 0.0 | -0.135824
RC_Minor_L_CSI | C2 | -0.00599999999999912 | 0.0
RC_Minor_L_CSI | Curve_Type | Polynomial | Linear
RC_Minor_L_ECI | C2 | -0.00299999999999912 | -0.006604
RC_Minor_L_JCI | C1 | -0.100000000000012 | 0.0
RC_Minor_L_JCI | C2 | 0.0 | -0.004917
RC_Minor_L_JCI | Curve_Type | Linear | Polynomial
RC_Minor_L_NCI | C2 | -0.00399999999999912 | -0.005902
RC_Minor_L_PSI | C2 | -0.00399999999999912 | -0.013521
RC_Minor_L_RDI | C2 | -0.00399999999999912 | -0.009234
RC_Minor_L_SCI | C1 | 0.0 | -0.01
RC_Minor_L_SCI | C2 | -0.00299999999999912 | 1.892
RC_Minor_L_SCI | Curve_Type | Polynomial | Power
RC_Minor_L_SCI | Maximum | 5 | 4.784