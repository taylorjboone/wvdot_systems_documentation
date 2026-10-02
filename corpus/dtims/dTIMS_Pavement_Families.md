# dTIMS Pavement Families: How Deterioration Curves Are Selected

Source: `dtims_dump.sqlite` (WVDOT dTIMS CT database, dumped 2026-04-10)

## Overview

dTIMS **does** support pavement families. Rather than using a single static concept called "family", dTIMS constructs a **composite lookup key** at runtime from three segment-level attributes and uses it to retrieve curve coefficients from the `Analysis_Lookup_Perf_Coef` table. The key structure is:

```
{Pave_Type}_{Rehab_Type}_{Truck_Load}_{Index}
```

This means every unique combination of pavement type, rehabilitation type, and truck loading class gets its own deterioration curve for each condition index. This **is** the family system -- it is just expressed as a dynamic lookup rather than a pre-assigned family ID.

---

## Family Key Components

### 1. Pavement Type (`PMS_tDAV_Pave_Type`)

A segment-level **Decision Analysis Variable** (DAV) that classifies pavement structure:

| Value | Description |
|-------|-------------|
| `BC`  | Bituminous (Asphalt) Concrete |
| `RC`  | Rigid (Portland Cement) Concrete |

This is the most important discriminator. It determines:
- Which condition indices apply (see [Index Applicability by Pavement Type](#index-applicability-by-pavement-type))
- Which deterioration curves are selected from the lookup table
- Which treatment costs are used
- Which trigger branches are evaluated

### 2. Rehabilitation Type (`PMS_tDAV_Rehab_Type`)

A segment-level DAV that captures the **last major treatment** applied to the pavement. Used as the second component of the family key to select the appropriate post-rehab deterioration curve.

### 3. Truck Load (`PMS_tDAV_Truck_Load`)

A segment-level DAV representing the traffic loading class. Heavier truck traffic produces steeper deterioration curves for load-sensitive indices (PSI, RDI).

### Resulting Family Key

At runtime, dTIMS evaluates:

```
STLOOKUP('Analysis_Lookup_Perf_Coef', 'C1', 'KEY',
         PMS_tDAV_Pave_Type + '_' + PMS_tDAV_Rehab_Type + '_' + PMS_tDAV_Truck_Load + '_PSI',
         TRUE)
```

For example, a bituminous pavement with rehab type "OL" and truck load class "M" looking up PSI coefficients would query:

```
KEY = 'BC_OL_M_PSI'
```

---

## The `Analysis_Lookup_Perf_Coef` Table

This is the central lookup table that stores all deterioration curve coefficients. Each row represents one family-index combination.

### Schema

| Column | Type | Description |
|--------|------|-------------|
| `Key` | nvarchar | Composite key: `{PaveType}_{RehabType}_{TruckLoad}_{Index}` |
| `Family` | nvarchar | Human-readable family label |
| `Index` | nvarchar | Full index name |
| `Index_Code` | nvarchar | Short index code (PSI, RDI, SCI, etc.) |
| `Curve_Type` | nvarchar | Regression model type name |
| `Curve_Type_Value` | Int | Numeric enum for `INDEXFROMAGE` function (see below) |
| `C1` | Float | Curve coefficient 1 |
| `C2` | Float | Curve coefficient 2 |
| `C3` | Float | Curve coefficient 3 |
| `Maximum` | Int | Maximum index value (always 5 for WVDOT indices) |
| `Curve_Equation` | nvarchar | Human-readable equation form |

### Curve Types

The `INDEXFROMAGE` function supports five regression curve types, selected by the `Curve_Type` string returned from the lookup:

| Curve_Type_Value | Name | Equation |
|-----------------|------|----------|
| 1 | Linear | `Index = Max - C1 * Age` |
| 2 | Logarithmic | `Index = Max - C1 * ln(Age + 1)` |
| 3 | Polynomial | `Index = Max - C1 * Age - C2 * Age^2` |
| 4 | Power | `Index = Max * (1 - (Age / C1)^C2)` or `Index = C1 * Age^(-C2)` |
| 5 | Sigmoid | `Index = Max / (1 + e^(C1 * (Age - C2)))` |

The `DAL_DCG_INDEXFROMAGE` function signature is:

```
INDEXFROMAGE(CurveType, C1, C2, C3, IndexMax, Age)
```

All WVDOT condition indices use `IndexMax = 5` (scale 0-5, where 5 = best).

---

## Condition Indices and Their Curve Assignments

### Index Applicability by Pavement Type

Not all six sub-indices apply to both pavement types. dTIMS enforces this through **filter-based curve branching** in `AnalysisVariableCurves`:

| Index | Full Name | Asphalt (BC) | Concrete (RC) | Slope |
|-------|-----------|:---:|:---:|-------|
| **PSI** | Present Serviceability Index (Roughness) | Yes | Yes | Down (D) |
| **RDI** | Rut Depth Index | Yes | No* | Down (D) |
| **SCI** | Structural Cracking Index | Yes | No* | Down (D) |
| **ECI** | Environmental Cracking Index | Yes | No* | Down (D) |
| **JCI** | Joint Condition Index | No* | Yes | Down (D) |
| **CSI** | Concrete Slab Index | No* | Yes | Down (D) |
| **CCI** | Composite Condition Index | Yes | Yes | Down (D) |

*\* When an index does not apply to a pavement type, dTIMS uses a fallback curve that returns a constant value of 5 (perfect condition). This is implemented via the `PMS_ancOBJ_ABS_5` expression (`Get_Number(5)`) as a secondary curve with `Order=1`.*

### How Curve Branching Works

Each analysis variable can have multiple curves in `AnalysisVariableCurves`, differentiated by `FilterID` and `Order`:

```
AnalysisVariableCurves for PMS_nAAV_CND_ECI:
  Order 0: Filter = PMS_abfOBJ_Asphalt  ->  ECI_INDEX_FROM_AGE (family lookup)
  Order 1: Filter = (None)              ->  ABS_5 (returns constant 5)
```

dTIMS evaluates curves in `Order` sequence. If the filter matches (segment is asphalt), the family-based deterioration curve is used. If no filter matches, the fallback returns 5.0 (index does not deteriorate for this pavement type).

The filter expressions:

| Filter | Expression | Meaning |
|--------|-----------|---------|
| `PMS_abfOBJ_Asphalt` | `PMS_tDAV_Pave_Type = 'BC'` | Asphalt segments only |
| `PMS_abfOBJ_Concrete` | `PMS_tDAV_Pave_Type = 'RC'` | Concrete segments only |

### Index-to-Filter Mapping from the Database

| Variable | Curve 0 Filter | Curve 0 Expression | Curve 1 (Fallback) |
|----------|---------------|-------------------|-------------------|
| `PMS_nAAV_CND_PSI` | (None) -- all types | `PSI_INDEX_FROM_AGE` via family lookup | N/A |
| `PMS_nAAV_CND_RDI` | (None) -- but expression checks `Pave_Type != 'RC'` | `RDI_INDEX_FROM_AGE` via family lookup | Returns 0 for RC |
| `PMS_nAAV_CND_SCI` | `PMS_abfOBJ_Asphalt` | `SCI_INDEX_FROM_AGE` via family lookup | `ABS_5` |
| `PMS_nAAV_CND_ECI` | `PMS_abfOBJ_Asphalt` | `ECI_INDEX_FROM_AGE` via family lookup | `ABS_5` |
| `PMS_nAAV_CND_JCI` | `PMS_abfOBJ_Concrete` | `JCI_INDEX_FROM_AGE` via family lookup | `ABS_5` |
| `PMS_nAAV_CND_CSI` | `PMS_abfOBJ_Concrete` | `CSI_INDEX_FROM_AGE` via family lookup | `ABS_5` |
| `PMS_nAAV_CND_CCI` | (None) -- all types | `CCI_INDEX_FROM_AGE` via family lookup | N/A |

### Special Cases

**RDI**: The expression itself contains an inline pavement type check rather than using a filter:
```
IF(PMS_tDAV_Pave_Type = 'RC', 0,
   MAX(INDEXFROMAGE(...), 0))
```
This returns 0 for concrete pavements (RDI does not apply to rigid pavements).

**CCI**: Despite being composite, CCI has its own independent family-based deterioration curve looked up from `Analysis_Lookup_Perf_Coef`. It is **not** calculated as a formula of the sub-indices during deterioration projection -- it is projected independently using its own `{PaveType}_{RehabType}_{TruckLoad}_CCI` curve.

---

## Per-Index Age Tracking

Each condition index has its own independent age variable, allowing treatment resets to affect indices independently:

| Index | Age Variable | Hold Variable | Slope |
|-------|-------------|---------------|-------|
| PSI | `PMS_nAAV_AGE_PSI` | -- | Up (U) |
| RDI | `PMS_nAAV_AGE_RDI` | -- | Up (U) |
| SCI | `PMS_nAAV_AGE_SCI` | `PMS_nAAV_AGE_SCI_Hold` | Up (U) |
| ECI | `PMS_nAAV_AGE_ECI` | `PMS_nAAV_AGE_ECI_Hold` | Up (U) |
| JCI | `PMS_nAAV_AGE_JCI` | `PMS_nAAV_AGE_JCI_Hold` | Up (U) |
| CSI | `PMS_nAAV_AGE_CSI` | `PMS_nAAV_AGE_CSI_Hold` | Up (U) |
| CCI | `PMS_nAAV_AGE_CCI` | `PMS_nAAV_AGE_CCI_Hold` | Up (U) |

**Age Variables** (`Slope = U`): Increment by 1 each year. When a treatment resets an index, the age is recalculated using `AGEFROMINDEX` (the inverse of `INDEXFROMAGE`) to find the equivalent age on the new curve for the post-treatment index value.

**Hold Variables** (`Slope = D`): Countdown timers set by certain treatments (e.g., Crack Seal sets `AGE_CCI_Hold = 4`). Each year the hold counter decrements by 1. While `Hold > 0`, the corresponding age variable does not advance, effectively freezing the index at its current value.

Hold counter curve expression:
```
IF(AGE_CCI_Hold > 1, AGE_CCI_Hold - 1, 0)
```

---

## Treatment Resets and Family Interaction

Treatment resets operate on indices directly, and the family system determines how fast the index re-deteriorates after treatment.

### Reset Patterns Observed in WVDOT Configuration

#### ADDITIVE Resets
The index is improved by a fixed delta, capped at 5.0:
```
MIN(current_index + delta, 5)
```

| Treatment | ECI | SCI | PSI | RDI | CCI |
|-----------|-----|-----|-----|-----|-----|
| Chip Seal | +0.50 | +0.50 | -- | -- | +0.50 |
| Cape Seal | +0.25 | +0.25 | -- | -- | +0.25 |
| Microsurfacing | +0.75 | +0.75 | +0.75 | +0.75 | +0.75 |
| Ultra Thin Overlay | +1.00 | +1.00 | +1.00 | +1.00 | +1.00 |
| Thin Overlay | +1.25 | +1.25 | +1.25 | +1.25 | +1.25 |

#### ABSOLUTE Resets
The index is set to a fixed value (5 = like-new):
```
Get_Number(5)
```

| Treatment | PSI | RDI | SCI | ECI | JCI | CSI | CCI |
|-----------|-----|-----|-----|-----|-----|-----|-----|
| Thick Overlay | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| Reconstruction | 5 | 5 | 5 | 5 | 5 | 5 | 5 |

#### HOLD Resets (via Hold Variables)
Some treatments (e.g., Crack Seal) set a hold counter instead of directly improving the index. This freezes deterioration for a number of years:

| Treatment | Hold Duration | Indices Affected |
|-----------|--------------|-----------------|
| Crack Seal | 4 years | CCI, ECI, SCI, JCI, CSI |

#### AGE_FROM_INDEX Resets
After an ADDITIVE reset, the age for each index is recalculated using the inverse deterioration function to find the corresponding age on the family curve:
```
AGEFROMINDEX(CurveType, C1, C2, C3, IndexMax, NewIndexValue)
```
This ensures the post-treatment index continues to deteriorate along the correct family curve from the improved index value, rather than simply resetting age to 0.

---

## How the Family System Connects to Optimization

### Treatment Triggers

Treatment eligibility is determined by the `Analysis_Lookup_Triggers` table, which defines 6-index window conditions:

| Column | Description |
|--------|-------------|
| `Key` | Lookup key |
| `Treatment` | Treatment name |
| `Trigger_Branch` | Branch number (OR logic between branches) |
| `PSI_Lower` / `PSI_Upper` | PSI window (AND logic within a branch) |
| `RDI_Lower` / `RDI_Upper` | RDI window |
| `SCI_Lower` / `SCI_Upper` | SCI window |
| `ECI_Lower` / `ECI_Upper` | ECI window |
| `JCI_Lower` / `JCI_Upper` | JCI window |
| `CSI_Lower` / `CSI_Upper` | CSI window |

A segment is eligible for a treatment if **any** trigger branch matches (all six index windows within a branch must be satisfied simultaneously).

### Treatment Costs

Costs are looked up from `Analysis_Lookup_Trt_Costs` using a key that includes pavement type:
```
STLOOKUP('Analysis_Lookup_Trt_Costs', 'Cost_Per_Lane_Mile', 'KEY',
         '{TreatmentShortName}_{District}_{PaveType}', TRUE)
```

The cost table schema includes:

| Column | Description |
|--------|-------------|
| `Key` | Lookup key |
| `Treatment` | Treatment name |
| `Pavement_Type` | BC or RC |
| `District` | District code |
| `Cost_Per_Lane_Mile` | Unit cost |
| `AVG` | Average cost |
| `S1`-`S7` | District-specific costs (7 WVDOT districts) |

### Benefit Calculation

The optimization benefit variable is **CCI** (Composite Condition Index). Analysis sets all use `PMS_nAAV_CND_CCI` as the condition variable:
```
ConditionVariableName = PMS_nAAV_CND_CCI
ConditionCategoryBoundary12 = 0.0
ConditionCategoryBoundary23 = 60.0
ConditionCategoryBoundary34 = 80.0
ConditionCategoryBoundary45 = 90.0
```

*(Note: These boundaries appear to be on a 0-100 scale, suggesting CCI may be rescaled for reporting. The raw CCI index is 0-5.)*

---

## Mapping to Our PMS Implementation

### Our `pavement_families` Table

Our system flattens the dTIMS family lookup into a static `pavement_families` table:

| Our Column | dTIMS Source |
|-----------|-------------|
| `family_id` | Composite: `{PaveType}_{RehabType}_{TruckLoad}` |
| `index_type` | `Index_Code` from `Analysis_Lookup_Perf_Coef` |
| `curve_type` | `Curve_Type` from `Analysis_Lookup_Perf_Coef` |
| `alpha` / `c1` | `C1` from `Analysis_Lookup_Perf_Coef` |
| `beta` / `c2` | `C2` from `Analysis_Lookup_Perf_Coef` |
| `c3` | `C3` from `Analysis_Lookup_Perf_Coef` |
| `initial_value` | `Maximum` (always 5) |

### Key Differences from dTIMS

1. **Static vs Dynamic**: We pre-assign a `family_id` to each segment. dTIMS constructs the key at runtime from three DAVs.

2. **CCI Calculation**: We compute CCI as a weighted minimum of sub-indices. dTIMS projects CCI independently on its own family curve.

3. **Age Reset**: dTIMS uses `AGEFROMINDEX` (inverse function) to back-calculate the age after an ADDITIVE reset. We reset age to 0 for non-HOLD resets.

4. **Hold Mechanism**: dTIMS uses countdown timer variables (`AGE_*_Hold`) that freeze the age counter. We model HOLD as a reset mode that skips the age reset.

---

## Summary

dTIMS implements pavement families through a **3-attribute composite key** looked up against the `Analysis_Lookup_Perf_Coef` table. This table provides per-index regression coefficients (C1, C2, C3) and curve type for each combination of:

- **Pavement Type** (BC = asphalt, RC = concrete)
- **Rehabilitation Type** (last major treatment applied)
- **Truck Load** class (traffic loading)

The family determines how fast each condition index deteriorates over time. Index applicability is filtered by pavement type (e.g., RDI/SCI/ECI for asphalt only; JCI/CSI for concrete only). Treatments reset indices via ADDITIVE, ABSOLUTE, or HOLD mechanisms, and the post-treatment deterioration follows the same family curve using age recalculation.
