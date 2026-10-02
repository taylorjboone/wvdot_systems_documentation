# dTIMS Proprietary Deterioration Curve Reference

> **Source data**: `dtims_dump.sqlite` (WVDOT dTIMS OData dump), `ExpressionFunctions` table, `RuntimeExpressions` table, `AnalysisVariableCurves` table, supplemented by Deighton documentation and pavement engineering literature.

---

## 1. Overview

All condition index deterioration in the WVDOT dTIMS instance is computed through a single Deighton proprietary function:

```
DAL_DCG_INDEXFROMAGE(curve_type, C1, C2, C3, index_max, age)
```

This function maps a pavement age (in years) to a condition index value using one of five supported regression curve types. A companion inverse function, `DAL_DCG_AGEFROMINDEX`, reverse-computes age from a target index value for use in treatment resets.

Both functions are built into the dTIMS engine and are not user-modifiable. Their behavior is controlled entirely through the parameters passed to them.

---

## 2. DAL_DCG_INDEXFROMAGE

### 2.1 Function Signature

From the `ExpressionFunctions` table in the WVDOT dTIMS instance:

```
INDEXFROMAGE(expC, expN1, expN2, expN3, vnpIndex_Max, vnpAge)
```

| Parameter | Name | Type | Description |
|:----------|:-----|:-----|:------------|
| `expC` | Curve Type | Text | Selects one of 5 regression curve types |
| `expN1` | Coefficient C1 | Numeric | First regression coefficient |
| `expN2` | Coefficient C2 | Numeric | Second regression coefficient |
| `expN3` | Coefficient C3 | Numeric | Third regression coefficient |
| `vnpIndex_Max` | Max Index | Numeric | Maximum value of the index (5 for WVDOT) |
| `vnpAge` | Age | Numeric | Years since construction or last treatment (an analysis variable) |

**Returns**: A numeric index value between 0 and `vnpIndex_Max`.

### 2.2 The Five Curve Types

The first parameter (`expC`) selects which regression model the function uses. The five supported types and their standard mathematical forms are:

#### Linear

```
Index = Index_Max - C1 * Age
```

Constant rate of decline. The index drops by `C1` units per year. Simple but unrealistic for most pavement deterioration, which tends to accelerate over time.

```
Index
  5 |*
    |  *
    |    *
    |      *
    |        *
    |          *
  0 +-------------> Age
```

#### Logarithmic

```
Index = Index_Max - C1 * ln(Age + C2)
```

Rapid initial deterioration that gradually slows. Useful for indices where the most dramatic change happens early in the pavement life (e.g., roughness on new asphalt).

```
Index
  5 |*
    |  ***
    |      ***
    |          ****
    |              ******
    |                    **********
  0 +-----------------------------> Age
```

#### Polynomial (Second Order)

```
Index = Index_Max - C1 * Age^2 - C2 * Age
```

Accelerating deterioration. The quadratic term causes the rate of decline to increase over time, modeling the reality that damage compounds.

```
Index
  5 |*****
    |      ***
    |         **
    |           **
    |             *
    |              *
  0 +-------------> Age
```

#### Power

```
Index = Index_Max - C1 * Age^C2
```

Flexible deterioration rate governed by the exponent `C2`. When `C2 > 1`, deterioration accelerates; when `C2 < 1`, it decelerates. This is the most commonly used type for general-purpose pavement performance modeling.

```
Index
  5 |****                       (C2 = 1.3: moderate acceleration)
    |     ****
    |         ***
    |            ***
    |               **
    |                 ***
  0 +--------------------> Age
```

#### Sigmoid

```
Index = Index_Max / (1 + exp(C1 + C2 * Age))
```

S-shaped deterioration. The pavement stays in good condition for an initial period (the "shoulder"), then deteriorates rapidly through the middle life, then the rate of decline levels off as it approaches failure. This models the empirically observed behavior of many pavement distress types.

```
Index
  5 |*****
    |      ****
    |          ***
    |             ***
    |                **
    |                  **
    |                    **
    |                      *****
  0 +-----------------------------> Age
```

### 2.3 Summary Table

| Curve Type | Formula | Parameters Used | Best For |
|:-----------|:--------|:----------------|:---------|
| Linear | `Max - C1 * Age` | C1 | Uniform degradation |
| Logarithmic | `Max - C1 * ln(Age + C2)` | C1, C2 | Early rapid decay, then leveling |
| Polynomial | `Max - C1 * Age^2 - C2 * Age` | C1, C2 | Accelerating decay |
| Power | `Max - C1 * Age^C2` | C1, C2 | General-purpose, flexible shape |
| Sigmoid | `Max / (1 + exp(C1 + C2 * Age))` | C1, C2 | Classic S-shaped pavement lifecycle |

---

## 3. DAL_DCG_AGEFROMINDEX

### 3.1 Function Signature

```
AGEFROMINDEX(expC, expN1, expN2, expN3, vnpIndex_Max, vnpIndexNew)
```

| Parameter | Name | Type | Description |
|:----------|:-----|:-----|:------------|
| `expC` | Curve Type | Text | Same curve type as the forward function |
| `expN1` | Coefficient C1 | Numeric | Same C1 coefficient |
| `expN2` | Coefficient C2 | Numeric | Same C2 coefficient |
| `expN3` | Coefficient C3 | Numeric | Same C3 coefficient |
| `vnpIndex_Max` | Max Index | Numeric | Maximum index value |
| `vnpIndexNew` | Target Index | Numeric | The index value for which to find the equivalent age |

**Returns**: The age (in years) at which the deterioration curve reaches the target index value.

### 3.2 Inverse Formulas

| Curve Type | Inverse Formula |
|:-----------|:----------------|
| Linear | `Age = (Max - Index) / C1` |
| Logarithmic | `Age = exp((Max - Index) / C1) - C2` |
| Polynomial | Quadratic formula on `C1 * Age^2 + C2 * Age - (Max - Index) = 0` |
| Power | `Age = ((Max - Index) / C1) ^ (1 / C2)` |
| Sigmoid | `Age = (ln(Max / Index - 1) - C1) / C2` |

### 3.3 Purpose

This function is used exclusively in **treatment reset expressions** (the `Exp_*_AGE_FROM_INDEX` expressions). When a treatment improves a condition index, the system must find the equivalent age on the deterioration curve that corresponds to the new index value so that future deterioration resumes from the correct point.

---

## 4. How WVDOT Parameterizes the Curves

### 4.1 The Performance Coefficient Lookup Table

All curve parameters are stored in a dTIMS lookup table called **`Analysis_Lookup_Perf_Coef`**. This table is not exposed through the OData dump but is referenced by every deterioration expression.

The table has the following columns:

| Column | Description |
|:-------|:------------|
| `KEY` | Family identifier in the format `{pave_type}_{func_class}_{traffic_class}_{index}` |
| `CURVE_TYPE` | One of the five curve type strings |
| `C1` | Coefficient 1 |
| `C2` | Coefficient 2 |
| `C3` | Coefficient 3 |

Example keys:
- `BC_Interstate_High_PSI` -- Asphalt Interstate High-traffic PSI curve
- `RC_Primary_Low_JCI` -- Concrete Primary Low-traffic JCI curve
- `BC_Secondary_All_SCI` -- Asphalt Secondary SCI curve

### 4.2 Expression Mechanics

Each condition index has a deterioration curve expression that follows this pattern (shown here for SCI):

```
MAX(
  DAL_DCG_INDEXFROMAGE(
    DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef', 'CURVE_TYPE', 'KEY',
      {pave_type} + '_' + {func_class} + '_' + {traffic_class} + '_SCI', TRUE),
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef', 'C1', 'KEY',
      {pave_type} + '_' + {func_class} + '_' + {traffic_class} + '_SCI', TRUE)),
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef', 'C2', 'KEY',
      {pave_type} + '_' + {func_class} + '_' + {traffic_class} + '_SCI', TRUE)),
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef', 'C3', 'KEY',
      {pave_type} + '_' + {func_class} + '_' + {traffic_class} + '_SCI', TRUE)),
    5,
    PMS_nAAV_AGE_SCI
  ),
  0
)
```

The `MAX(..., 0)` wrapper ensures the index never goes below zero.

### 4.3 Surface-Type Guards

Concrete-only indices (CSI, JCI) and asphalt-only indices (RDI, SCI, ECI) are wrapped with surface-type guards:

```
-- CSI (concrete only):
IF(PMS_tDAV_Pave_Type <> 'RC',
   0,                          -- Force to 0 for asphalt (effectively 5.0 for CCI calc)
   MAX(DAL_DCG_INDEXFROMAGE(...), 0)
)

-- RDI (asphalt only):
IF(PMS_tDAV_Pave_Type = 'RC',
   0,                          -- Force to 0 for concrete
   MAX(DAL_DCG_INDEXFROMAGE(...), 0)
)
```

Note: In the actual trigger evaluation and CCI calculation, non-applicable indices are treated as 5.0 (perfect), so they never govern the composite.

---

## 5. The Shift Curve Mechanism

### 5.1 What It Does

When the `ShiftCurve` property is set to `true` on an `AnalysisVariable` in dTIMS, the system adjusts the starting point on the deterioration curve to match the section's current observed condition.

### 5.2 How It Works

```
Step 1: Read current observed index value from inventory
        Example: current PSI = 3.8

Step 2: Use AGEFROMINDEX to find the equivalent age
        equivalent_age = AGEFROMINDEX('Power', C1, C2, C3, 5, 3.8)
        Example: equivalent_age = 7.2 years

Step 3: Set the age variable to the equivalent age
        PMS_nAAV_AGE_PSI = 7.2

Step 4: Deterioration proceeds forward from this point on the curve
        Year 1: age = 8.2  -> PSI = INDEXFROMAGE('Power', C1, C2, C3, 5, 8.2)
        Year 2: age = 9.2  -> PSI = INDEXFROMAGE('Power', C1, C2, C3, 5, 9.2)
        ...
```

### 5.3 Visual Representation

```
Index
  5 |*****
    |      ****
    |          ***              Standard family curve
    |             * (3.8)  <--- Current observed value anchors here
    |              ***
    |                 **
    |                   ***
  0 +--+---+---+---+---+----> Age
    0  2   4   6  7.2  10
                   ^
                   Equivalent age computed by AGEFROMINDEX
```

This horizontal shift ensures that each section follows the same family curve shape but starts from its actual current condition, rather than assuming it started at age 0 with index 5.0.

---

## 6. Treatment Reset and Age Recalculation

### 6.1 The Reset Cycle

When a treatment is applied:

1. **Reset the index**: The treatment's reset expression sets the index to a new (improved) value
   ```
   PSI: 2.5 -> 4.2  (via nRES_PSI_THIN_OVL expression)
   ```

2. **Reverse-compute equivalent age**: `AGEFROMINDEX` finds where on the curve the new value falls
   ```
   new_age = AGEFROMINDEX('Power', C1, C2, C3, 5, 4.2)
   Example: new_age = 4.1 years
   ```

3. **Resume deterioration**: The age variable is set to the new equivalent age, and deterioration continues forward from that point

### 6.2 Visual

```
Index
  5 |*****
    |      *                  Reset point
    |     / * (4.2) <-------- Treatment improves index
    |    /    ***
    |   /        **
    |  / (2.5)    ***         Original trajectory
    | * <-------- Pre-treatment condition
    |               ****
  0 +---+---+---+---+---+-> Age
    0   4.1  8  12  16  20
        ^
        New equivalent age after reset
```

---

## 7. Comparison: dTIMS vs. Current Engine Implementation

### 7.1 dTIMS (Production)

- Uses `DAL_DCG_INDEXFROMAGE` with **5 selectable curve types**
- Curve type and 3 coefficients stored per family per index in `Analysis_Lookup_Perf_Coef`
- Coefficients calibrated from historical condition data using regression analysis
- Curve type can differ between families and between indices within the same family

### 7.2 Current Engine (`engine/deterioration/models.py`)

- Uses the **Power curve type only**: `Index = initial_value - alpha * age^beta`
- Parameters (`alpha`, `beta`) hardcoded in `DEFAULT_FAMILY_PARAMS`
- Equivalent to `DAL_DCG_INDEXFROMAGE('Power', alpha, beta, 0, 5, age)`
- Does not support the Sigmoid, Logarithmic, Linear, or Polynomial curve types

### 7.3 Alignment Gap

| Feature | dTIMS | Current Engine |
|:--------|:------|:---------------|
| Curve types supported | 5 (Linear, Log, Poly, Power, Sigmoid) | 1 (Power only) |
| Parameter source | Lookup table (`Analysis_Lookup_Perf_Coef`) | Hardcoded defaults |
| Curve type per family/index | Yes (configurable) | No (always Power) |
| ShiftCurve initialization | Via `AGEFROMINDEX` | Via `compute_equivalent_age` (Power only) |
| Coefficient count | 3 (C1, C2, C3) | 2 (alpha, beta) |

---

## 8. Complete Index Deterioration Expressions

The following table shows the actual runtime expressions from the WVDOT dTIMS instance for each condition index:

| Index | Expression Name | Surface Guard | Floor |
|:------|:----------------|:--------------|:------|
| PSI | `PMS_ancCND_PSI_INDEX_FROM_AGE` | None (all pavements) | Clamped at 0 via IF |
| RDI | `PMS_ancCND_RDI_INDEX_FROM_AGE` | `IF(pave_type='RC', 0, ...)` | MAX(..., 0) |
| SCI | `PMS_ancCND_SCI_INDEX_FROM_AGE` | Asphalt filter | MAX(..., 0) |
| ECI | `PMS_ancCND_ECI_INDEX_FROM_AGE` | Asphalt filter | MAX(..., 0) |
| CSI | `PMS_ancCND_CSI_INDEX_FROM_AGE` | `IF(pave_type<>'RC', 0, ...)` | MAX(..., 0) |
| JCI | `PMS_ancCND_JCI_INDEX_FROM_AGE` | `IF(pave_type<>'RC', 0, ...)` | MAX(..., 0) |
| CCI | `PMS_ancCND_CCI_INDEX_FROM_AGE` | None | MAX(..., 0) |

Each expression follows the same pattern:
1. Look up `CURVE_TYPE`, `C1`, `C2`, `C3` from `Analysis_Lookup_Perf_Coef` using the family key
2. Call `DAL_DCG_INDEXFROMAGE(curve_type, C1, C2, C3, 5, age_variable)`
3. Clamp the result to a minimum of 0

---

## 9. Other Deighton Proprietary Functions

The `ExpressionFunctions` table contains the full catalog of `DAL_DCG_*` functions available in the dTIMS engine:

| Function | Purpose |
|:---------|:--------|
| `DAL_DCG_INDEXFROMAGE` | Compute condition index from age using parametric curve |
| `DAL_DCG_AGEFROMINDEX` | Reverse-compute age from condition index value |
| `DAL_DCG_STLOOKUP` | Fast lookup from a named dTIMS table by key |
| `DAL_DCG_TLOOKUP` | Standard table lookup (slower than STLOOKUP) |
| `DAL_DCG_MIN10` | Return minimum of up to 10 values |
| `DAL_DCG_MAX10` | Return maximum of up to 10 values |
| `DAL_DCG_GETPV` | Calculate present value of an analysis variable over a year range |
| `DAL_DCG_GETSUM` | Sum an analysis variable over a year range |
| `DAL_DCG_GETAVG` | Average an analysis variable over a year range |
| `DAL_DCG_GETMIN` | Minimum of an analysis variable over a year range |
| `DAL_DCG_GETMAX` | Maximum of an analysis variable over a year range |
| `DAL_DCG_GETSD` | Standard deviation of an analysis variable over a year range |
| `DAL_DCG_GETMEDIAN` | Median of an analysis variable over a year range |
| `DAL_DCG_MARKOV` | Predict future distress state using Markov Transition Probability Matrix |
| `DAL_DCG_XLUD` | Excel lookup returning a numeric value |
| `DAL_DCG_XLUS` | Excel lookup returning a string value |
| `DAL_DCG_XLUB` | Excel lookup returning a boolean value |
| `DAL_DCG_XLURNGD` | Excel range lookup returning a date |
| `DAL_DCG_XLURNGS` | Excel range lookup returning a string |

---

## Sources

- WVDOT dTIMS instance (`dtims_dump.sqlite`) -- `ExpressionFunctions`, `RuntimeExpressions`, `AnalysisVariableCurves` tables
- [Deighton -- dTIMS for Pavement Management](https://www.deighton.com/dtims-blog/dtims-for-pavement-management)
- [NDDOT Pavement Management Program](https://www.dot.nd.gov/construction-and-planning/transportation-plans-programs/pavement-management-program)
- [NDDOT dTIMS Description (PDF)](https://www.dot.nd.gov/sites/www/files/documents/construction-and-planning/dTIMS-Description.pdf)
- [Deighton dTIMS Help -- Database Expressions](https://demo.deighton.com/whitby/ba/help/Content/dTIMS/dt_dbase_expressions_intro.htm)
- [Deighton dTIMS Help -- Markov TPM Functions](https://demo.deighton.com/whitby/ba/help/Content/dTIMS/dt_functions_markov.htm)
- [FHWA LTPP Performance Prediction Models](https://www.fhwa.dot.gov/publications/research/infrastructure/pavements/ltpp/06121/appendb.cfm)
- [Sigmoidal Models for Predicting Pavement Performance (ASCE)](https://ascelibrary.org/doi/10.1061/%28ASCE%29CF.1943-5509.0000833)
- [SCDOT Pavement Performance Curves -- SPR-743](https://scltap-scdot.s3.amazonaws.com/documents/SPR-743-Final-Report.pdf)
- [UDOT Pavement Management -- dTIMS](https://sites.google.com/utah.gov/pavementmanagement/home/dtims)
