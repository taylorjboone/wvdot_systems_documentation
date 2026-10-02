# WVDOT dTIMS Pavement Management System: Treatment Subsystem Deep Dive

> **Data Sources**: `dtims_dump.sqlite` (live OData dump from WVDOT dTIMS instance), `2025_12_17_Analysis_Lookup_Triggers.xlsx` (trigger lookup table), `schema.xml` (OData EDMX schema)

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Analysis Variables](#2-analysis-variables)
3. [Deterioration Model](#3-deterioration-model)
4. [The 18 PMS Treatments](#4-the-18-pms-treatments)
5. [Trigger Expressions](#5-trigger-expressions)
6. [The Analysis\_Lookup\_Triggers Table](#6-the-analysis_lookup_triggers-table)
7. [County Treatment Triggers](#7-county-treatment-triggers)
8. [Cost Calculation](#8-cost-calculation)
9. [Treatment Resets](#9-treatment-resets)
10. [Treatment Sequencing](#10-treatment-sequencing)
11. [Analysis Configuration](#11-analysis-configuration)
12. [End-to-End Walkthrough](#12-end-to-end-walkthrough)

---

## 1. System Overview

The WVDOT Pavement Management System (PMS) is built on the Deighton dTIMS CT platform. At its core, the system models pavement deterioration over time, evaluates when sections become eligible for specific treatments, computes the cost and benefit of each treatment, and optimizes a multi-year work program under budget constraints.

The treatment subsystem is the engine that answers: **"What treatment should be applied to which road section, and when?"**

```
+---------------------+       +---------------------+       +---------------------+
|   INVENTORY DATA    |       | DETERIORATION MODEL |       |   TRIGGER ENGINE    |
| - Section geometry  | ----> | - Age-based curves  | ----> | - Condition bounds  |
| - Pavement type     |       | - Index computation |       | - Surface type      |
| - Traffic (AADT)    |       | - RSL calculation   |       | - Committed checks  |
| - District/Route    |       |                     |       | - Lookup tables     |
+---------------------+       +---------------------+       +---------------------+
                                                                      |
                                                                      v
+---------------------+       +---------------------+       +---------------------+
|   WORK PROGRAM      | <---- |    OPTIMIZATION     | <---- | COST & BENEFIT CALC |
| - Year-by-year plan |       | - Incremental B/C   |       | - Per-lane-mile     |
| - Budget allocation |       | - Budget constraints|       | - Inflation adj.    |
| - Treatment mix     |       | - Do-nothing base   |       | - PV computation    |
+---------------------+       +---------------------+       +---------------------+
```

**Key design principles:**

- **Six condition sub-indices** roll up into a single **Composite Condition Index (CCI)** via MIN.
- Treatments are selected based on **condition windows** -- each treatment targets a specific severity range.
- A **lookup-table-driven** architecture (via `DAL_DCG_STLOOKUP`) makes trigger thresholds configurable without modifying code.
- **Committed (programmed) treatments** override condition-based triggering -- if a section has pre-committed work, the system honors it.
- **State Route** and **County Route** treatments use different trigger mechanisms and cost tables.

---

## 2. Analysis Variables

The system tracks every pavement section through a set of analysis variables. Each variable has a GUID identifier used in all expressions.

### 2.1 Condition Indices (0-5 Scale, 5 = Best)

These are the primary decision variables. All descending -- a lower value means worse condition.

| GUID (short) | Variable Name | Description | Applies To |
|:-------------|:--------------|:------------|:-----------|
| `42943fcd` | `PMS_nAAV_CND_PSI` | Present Serviceability Index (ride quality derived from IRI) | All |
| `1c8052d3` | `PMS_nAAV_CND_RDI` | Rut Depth Index | Asphalt (BC) |
| `ee3c6523` | `PMS_nAAV_CND_SCI` | Structural Cracking Index | Asphalt (BC) |
| `52c46a28` | `PMS_nAAV_CND_CSI` | Cracking Severity Index | Concrete (RC); forced to 5 for asphalt |
| `1fe36102` | `PMS_nAAV_CND_ECI` | Edge Condition Index | Asphalt (BC); forced to 5 for concrete |
| `64b7d597` | `PMS_nAAV_CND_JCI` | Joint Condition Index | Concrete (RC); forced to 5 for asphalt |
| `b17f394f` | `PMS_nAAV_CND_CCI` | Composite Condition Index | All |

**CCI computation:**

```
CCI = MIN(PSI, RDI, SCI, CSI, ECI, JCI)
```

For asphalt pavements, CSI and JCI are forced to 5 (perfect), so they never govern:

```
CCI_asphalt = MIN(PSI, RDI, SCI, ECI)
```

For concrete pavements, RDI, SCI, and ECI are forced to 5:

```
CCI_concrete = MIN(PSI, CSI, JCI)
```

### 2.2 Raw Measurements

| GUID (short) | Variable Name | Description | Direction |
|:-------------|:--------------|:------------|:----------|
| `3ae48bd7` | `PMS_nAAV_CND_IRI` | International Roughness Index (in/mi) | Ascending = worse |
| `f3e74fb6` | `PMS_nAAV_CND_RUT` | Rut Depth (inches) | Ascending = worse |
| `af5bdd9f` | `PMS_nAAV_CND_PCRK` | Percent Cracking | Ascending = worse |
| `eeec27ce` | `PMS_nAAV_CND_FLT` | Faulting (concrete joints, inches) | Ascending = worse |

### 2.3 Age Variables (Deterioration Tracking)

Each condition index has a corresponding age variable. When a treatment resets an index, the system reverse-computes a new "equivalent age" so deterioration resumes from the correct point on the curve.

| GUID (short) | Variable Name | Tracks Age For |
|:-------------|:--------------|:---------------|
| `963cad98` | `PMS_nAAV_AGE_PSI` | PSI |
| `6426b3ef` | `PMS_nAAV_AGE_RDI` | RDI |
| `c4865c39` | `PMS_nAAV_AGE_SCI` | SCI |
| `ceb172c5` | `PMS_nAAV_AGE_CSI` | CSI |
| `981a9f97` | `PMS_nAAV_AGE_ECI` | ECI |
| `d467ebc5` | `PMS_nAAV_AGE_JCI` | JCI |
| `dbff2024` | `PMS_nAAV_AGE_CCI` | CCI |

### 2.4 Other Variables

| GUID (short) | Variable Name | Description |
|:-------------|:--------------|:------------|
| `93a9dd02` | `PMS_nAAV_CND_RSL` | Remaining Service Life (years until threshold breach) |
| `674cee68` | `PMS_nAAV_TRF_ADT` | Average Annual Daily Traffic (AADT) |
| `aa88ec97` | `PMS_tDAV_Pave_Type` | Pavement type: `"BC"` = bituminous/asphalt, `"RC"` = rigid/concrete |
| `7014cb8f` | `PMS_nDAV_CNT_CHIP_SEALS` | Cumulative count of chip seal applications |
| `1e9fd63b` | `PMS_nDAV_CNT_MICROSURFACE` | Cumulative count of microsurface applications |
| `9e42983d` | `PMS_nCAV_PV_Benefit` | Present Value of Benefit (computed for optimization) |
| `e8d463f4` | `PMS_nCAV_PV_COST` | Present Value of Cost (computed for optimization) |
| `478feca0` | `PMS_nAAV_Yrly_Cost` | Yearly Cost of applied treatment |

---

## 3. Deterioration Model

### 3.1 The Core Function: `DAL_DCG_INDEXFROMAGE()`

All condition indices are computed using a single Deighton proprietary function:

```
DAL_DCG_INDEXFROMAGE(param1, param2, param3, param4, max_value, age_variable)
```

This function maps an age (in years) to a condition index value using a parametric S-curve. The curve starts at `max_value` (always 5 for WVDOT) and decays toward 0 as age increases. The four parameters (`param1` through `param4`) control the shape, rate, and inflection point of the curve.

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
  0 +-----------------------------> Age (years)
    0         10        20       30+
```

### 3.2 Index-Specific Deterioration

Each condition index uses its own curve parameters and age variable:

| Index | Expression Pattern | Surface Filter |
|:------|:-------------------|:---------------|
| **PSI** | `DAL_DCG_INDEXFROMAGE(p1, p2, p3, p4, 5, PMS_nAAV_AGE_PSI)` | All pavements |
| **RDI** | `DAL_DCG_INDEXFROMAGE(p1, p2, p3, p4, 5, PMS_nAAV_AGE_RDI)` | Asphalt (BC) only; =5 for RC |
| **SCI** | `DAL_DCG_INDEXFROMAGE(p1, p2, p3, p4, 5, PMS_nAAV_AGE_SCI)` | Asphalt (BC) only; =5 for RC |
| **ECI** | `DAL_DCG_INDEXFROMAGE(p1, p2, p3, p4, 5, PMS_nAAV_AGE_ECI)` | Asphalt (BC) only; =5 for RC |
| **CSI** | `DAL_DCG_INDEXFROMAGE(p1, p2, p3, p4, 5, PMS_nAAV_AGE_CSI)` | Concrete (RC) only; =5 for BC |
| **JCI** | `DAL_DCG_INDEXFROMAGE(p1, p2, p3, p4, 5, PMS_nAAV_AGE_JCI)` | Concrete (RC) only; =5 for BC |
| **CCI** | `MAX(DAL_DCG_INDEXFROMAGE(p1, p2, p3, p4, 5, PMS_nAAV_AGE_CCI), 0)` | All (floored at 0) |

The curve parameters (`p1`-`p4`) vary by pavement family. Families are defined by combinations of pavement type, traffic class, and functional classification. Each family has its own calibrated deterioration curves.

### 3.3 Derived Raw Measurements

IRI and RUT are not modeled independently. They are **derived from their respective indices** using inverse formulas:

**IRI from PSI** (the classic AASHTO PSI-IRI relationship, inverted):

```
IRI = MIN(65 + (LOG(PSI / 5) / -0.0066), 500)
```

This caps IRI at 500 in/mi. When PSI = 5, IRI = 65 (new pavement). As PSI drops toward 0, IRI climbs toward 500.

**RUT from RDI** (the index-to-measurement inversion):

```
RUT = ((5 - RDI) / 6.65) ^ (1 / 1.41)
```

When RDI = 5, RUT = 0. As RDI drops, RUT increases.

### 3.4 Remaining Service Life (RSL)

RSL answers: "How many years until this section fails?" It is computed as the minimum number of years until **any** condition index breaches its threshold:

```
RSL = MIN(
    years_until PSI hits threshold,
    years_until RDI hits threshold,
    years_until SCI hits threshold,
    years_until CSI hits threshold,
    years_until ECI hits threshold,
    years_until JCI hits threshold
)
```

This is implemented using the Deighton function `DAL_DCG_MIN10()`.

The failure threshold varies by road classification, controlled by the field `RSL_Threshold_Code` (GUID `68ed04d3`):

| RSL Threshold Code | Threshold Value | Typical Road Class |
|:-------------------|:----------------|:-------------------|
| `'1'` | 2.5 | Interstate / high-priority |
| `'2'` | 2.0 | Major arterials |
| `'3'` | 1.5 | Minor arterials |
| `'4'` | 1.0 | Local / low-volume |
| Default | 2.5 | (fallback) |

A higher threshold means the road is considered "failed" at a higher (better) condition level, reflecting the higher standards applied to more critical routes.

---

## 4. The 18 PMS Treatments

### 4.1 State Route Treatments (14 treatments)

| # | Treatment ID | Display Name | Reapplication Interval | Budget Category | Surface Type |
|:--|:-------------|:-------------|:----------------------|:----------------|:-------------|
| 1 | `PMS_PM_Crack_Seal` | Crack Seal | 3 years | Rehabilition | Asphalt |
| 2 | `PMS_Preservation` | Preservation | 4 years | Rehabilition | Asphalt |
| 3 | `PMS_PM_Saw_Seal_Joints` | Saw & Seal Joints | 6 years | Rehabilition | Concrete |
| 4 | `PMS_PM_Cape_Seal` | Cape Seal | 3 years | Rehabilition | Asphalt |
| 5 | `PMS_PM_Chip_Seal` | Chip Seal | 3 years | Rehabilition | Asphalt |
| 6 | `PMS_PM_Microsurfacing` | Microsurfacing | 3 years | MicroSurface | Asphalt |
| 7 | `PMS_PM_Ultra_Thin_Overlay` | Ultra Thin Overlay | 4 years | Rehabilition | Asphalt |
| 8 | `PMS_Thin_Overlay` | Thin Overlay | 7 years | Rehabilition | Asphalt |
| 9 | `PMS_Thick_Overlay` | Thick Overlay | 4 years | Rehabilition | Asphalt |
| 10 | `PMS_Minor_CPR_Diamond_Grind` | Minor CPR Diamond Grind | 6 years | Rehabilition | Concrete |
| 11 | `PMS_Major_CPR_Diamond_Grind` | Major CPR Diamond Grind | 6 years | Rehabilition | Concrete |
| 12 | `PMS_Reconstruction` | Reconstruction | 4 years | Rehabilition | Both |
| 13 | `PMS_PM_Asphalt` | PM Asphalt (placeholder) | 3 years | Rehabilition | Asphalt |
| 14 | `PMS_PM_Concrete` | PM Concrete (placeholder) | 5 years | Rehabilition | Concrete |

### 4.2 County Route Treatments (4 treatments)

| # | Treatment ID | Display Name | Reapplication Interval | Budget Category |
|:--|:-------------|:-------------|:----------------------|:----------------|
| 15 | `PMS_County_Chip_Seal` | County Chip Seal | 3 years | Rehabilition |
| 16 | `PMS_County_MicroSurface` | County Microsurfacing | 3 years | MicroSurface |
| 17 | `PMS_County_Thin_Overlay` | County Thin Overlay | 6 years | Rehabilition |
| 18 | `PMS_County_Thick_Overlay` | County Thick Overlay | 6 years | Rehabilition |

### 4.3 Common Properties

All 18 treatments share these settings:

| Property | Value | Meaning |
|:---------|:------|:--------|
| `Type` | Major | Treatment is a discrete capital action (not routine maintenance) |
| `IsInitial` | 1 (True) | Can be the first treatment applied in the analysis |
| `ApplyAfterInitial` | 0 (False) | Is not restricted to only follow an initial treatment |
| `TriggerTemplate` | Maintenance Only | Treatment must satisfy its trigger conditions each year |

### 4.4 Treatment Severity Spectrum

The treatments form a progression from lightest preservation to heaviest rehabilitation:

```
LIGHTEST                                                              HEAVIEST
   |                                                                      |
   v                                                                      v

Crack Seal --> Cape Seal --> Chip Seal --> Microsurface --> Ultra Thin OVL
                                                                |
                                          Preservation <--------+
                                                                |
                                          Thin Overlay <--------+
                                                                |
                                          Thick Overlay <-------+
                                                                |
                                          Reconstruction <------+

CONCRETE PATH:
Saw & Seal --> Minor CPR Diamond Grind --> Major CPR Diamond Grind --> Reconstruction
```

---

## 5. Trigger Expressions

### 5.1 The Three-Part IF() Structure

Every State Route trigger expression follows an identical three-part structure. This is the most critical piece of the treatment subsystem -- it determines **when a treatment is eligible** for a given section in a given year.

```
IF(
    // GUARD: Does this section have committed (pre-programmed) treatments?
    IS_COMMITTED() AND YR <= MAX(committed_year_1, ..., committed_year_4),

    // PART 1 - COMMITTED BRANCH:
    // Only trigger if a committed treatment matches THIS treatment in THIS year
    (committed_treatment_1 = 'THIS_TREATMENT' AND committed_year_1 = YR) OR
    (committed_treatment_2 = 'THIS_TREATMENT' AND committed_year_2 = YR) OR
    (committed_treatment_3 = 'THIS_TREATMENT' AND committed_year_3 = YR) OR
    (committed_treatment_4 = 'THIS_TREATMENT' AND committed_year_4 = YR),

    // PART 2 - CONDITION-BASED BRANCH:
    // Standard eligibility logic when no committed treatment applies
    section_length >= 0.5
    AND is_correct_surface_type
    AND (
        // Branch 1 (condition window from lookup table)
        (PSI >= LOOKUP('PSI_LOWER', 'KEY_1') AND PSI <= LOOKUP('PSI_UPPER', 'KEY_1') AND
         RDI >= LOOKUP('RDI_LOWER', 'KEY_1') AND RDI <= LOOKUP('RDI_UPPER', 'KEY_1') AND
         SCI >= LOOKUP('SCI_LOWER', 'KEY_1') AND SCI <= LOOKUP('SCI_UPPER', 'KEY_1') AND
         CSI >= LOOKUP('CSI_LOWER', 'KEY_1') AND CSI <= LOOKUP('CSI_UPPER', 'KEY_1') AND
         ECI >= LOOKUP('ECI_LOWER', 'KEY_1') AND ECI <= LOOKUP('ECI_UPPER', 'KEY_1') AND
         JCI >= LOOKUP('JCI_LOWER', 'KEY_1') AND JCI <= LOOKUP('JCI_UPPER', 'KEY_1'))
        OR
        // Branch 2
        (PSI >= LOOKUP('PSI_LOWER', 'KEY_2') AND PSI <= LOOKUP('PSI_UPPER', 'KEY_2') AND ...)
        OR
        // ... Branch N
        (...)
    )
)
```

### 5.2 Key Functions Used in Triggers

| Function | Purpose | Example |
|:---------|:--------|:--------|
| `DAL_DCG_STLOOKUP(table, column, key_col, key_val, exact)` | Look up a value from a named table by key | `DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers', 'PSI_UPPER', 'KEY', 'THICK_OVL_1', TRUE)` |
| `GET_ANALVR(guid)` | Get the current value of an analysis variable | `GET_ANALVR('42943fcd...')` returns current PSI |
| `Get_Field(guid)` | Get an inventory (static) field value | `Get_Field('aa88ec97...')` returns pavement type |
| `Get_Exp(guid)` | Evaluate another named expression | Used for sub-expressions |
| `IS_COMMITTED()` | Check if section has pre-committed treatments | Returns TRUE/FALSE |
| `GET_TRTYR('treatment')` | Get the year a treatment was last applied | `GET_TRTYR('PMS_Thin_Overlay')` |
| `YR` | Current analysis year | Built-in variable |

### 5.3 How the Committed Branch Works

WVDOT pre-programs certain treatments (e.g., from a current construction letting). Up to 4 committed treatments can be stored per section, each with a treatment name and planned year.

When the analysis engine encounters a section with committed treatments:
1. It checks if the current year (`YR`) falls within the committed treatment horizon.
2. If yes, it **only** triggers the specific committed treatment in the exact committed year.
3. This prevents the optimizer from selecting a different treatment that might score better on benefit/cost but would conflict with the already-programmed work.

After the committed years pass, the section reverts to standard condition-based triggering.

### 5.4 How the Condition-Based Branch Works

For non-committed sections (or after committed years expire), the trigger evaluates:

1. **Minimum section length** (typically >= 0.5 miles) -- avoids treating very short segments.
2. **Surface type filter** -- asphalt treatments require `PMS_tDAV_Pave_Type = 'BC'`; concrete treatments require `'RC'`.
3. **Condition windows** -- each of the six condition indices must fall within a specific range defined in the `Analysis_Lookup_Triggers` table. Multiple branches (OR conditions) allow a treatment to trigger under different distress combinations.

The condition windows implement the engineering logic: "Apply a thin overlay when the pavement is in moderate distress (not too good, not too far gone)."

### 5.5 Multi-Branch Trigger Logic

Most treatments have multiple trigger branches to capture different distress scenarios. For example, **Thick Overlay** has 3 branches:

```
Branch 1: PSI is low (poor ride), other indices moderate
    --> Trigger because roughness alone warrants major rehab

Branch 2: SCI is low (severe cracking), PSI still acceptable
    --> Trigger because structural failure warrants major rehab

Branch 3: ECI is low (edge deterioration), other indices moderate
    --> Trigger because edge failure warrants major rehab
```

Each branch is an OR condition, so satisfying **any one** branch makes the treatment eligible.

---

## 6. The Analysis\_Lookup\_Triggers Table

This is the external lookup table (from `Analysis_Lookup_Triggers.xlsx`) that parameterizes all State Route treatment triggers. It has 25 rows, one per treatment-branch combination, and defines condition index windows using lower and upper bounds for all six indices.

### 6.1 Full Table

Each cell shows the range as `[lower, upper]` on the 0-5 scale.

| Key | Treatment | CSI Range | ECI Range | JCI Range | PSI Range | RDI Range | SCI Range |
|:----|:----------|:----------|:----------|:----------|:----------|:----------|:----------|
| `CAPE_SEAL_1` | Cape Seal | [0, 5] | [3, 4.5] | [0, 5] | [3, 5] | [3.5, 5] | [3, 4.5] |
| `CHIP_SEAL_1` | Chip Seal | [0, 5] | [2.5, 4.5] | [0, 5] | [0, 5] | [3.5, 5] | [3.5, 4.5] |
| `CRACK_SEAL_1` | Crack Seal | [4.3, 4.5] | [0, 5] | [0, 5] | [0, 5] | [0, 5] | [0, 5] |
| `MAJOR_CPR_DG_1` | Major CPR DG | [1, 5] | [0, 5] | [1, 5] | [1, 2.5] | [0, 5] | [0, 5] |
| `MAJOR_CPR_DG_2` | Major CPR DG | [1, 5] | [0, 5] | [1, 5] | [1, 5] | [0, 5] | [0, 5] |
| `MAJOR_CPR_DG_3` | Major CPR DG | [1, 5] | [0, 5] | [1, 3] | [1, 5] | [0, 5] | [0, 5] |
| `MICRO_1` | Microsurfacing | [0, 5] | [3.5, 4.9] | [0, 5] | [3.6, 4.5] | [3.5, 4.9] | [3.5, 4.9] |
| `MINOR_CPR_DG_1` | Minor CPR DG | [2.5, 5] | [0, 5] | [2.5, 5] | [2.5, 3] | [0, 5] | [0, 5] |
| `MINOR_CPR_DG_2` | Minor CPR DG | [2.5, 5] | [0, 5] | [2.5, 3.5] | [2.5, 5] | [0, 5] | [0, 5] |
| `MINOR_CPR_DG_3` | Minor CPR DG | [2.5, 3.5] | [0, 5] | [2.5, 5] | [2.5, 5] | [0, 5] | [0, 5] |
| `PRESERVATION_1` | Preservation | [3.5, 4] | [0, 5] | [0, 5] | [0, 5] | [0, 5] | [0, 5] |
| `RECON_1` | Reconstruction | [0, 1] | [0, 5] | [0, 5] | [0, 5] | [0, 5] | [0, 5] |
| `RECON_2` | Reconstruction | [0, 5] | [0, 1] | [0, 5] | [0, 5] | [0, 5] | [0, 5] |
| `RECON_3` | Reconstruction | [0, 5] | [0, 5] | [0, 1] | [0, 5] | [0, 5] | [0, 5] |
| `RECON_4` | Reconstruction | [0, 5] | [0, 5] | [0, 5] | [0, 1] | [0, 5] | [0, 5] |
| `RECON_5` | Reconstruction | [0, 5] | [0, 5] | [0, 5] | [0, 5] | [0, 1] | [0, 5] |
| `SAW_SEAL_1` | Saw & Seal | [3, 4] | [0, 5] | [3, 4] | [0, 5] | [0, 5] | [0, 5] |
| `THICK_OVL_1` | Thick Overlay | various | various | various | various | various | various |
| `THICK_OVL_2` | Thick Overlay | various | various | various | various | various | various |
| `THICK_OVL_3` | Thick Overlay | various | various | various | various | various | various |
| `THIN_OVL_1` | Thin Overlay | various | various | various | various | various | various |
| `THIN_OVL_2` | Thin Overlay | various | various | various | various | various | various |
| `THIN_OVL_3` | Thin Overlay | various | various | various | various | various | various |
| `THIN_OVL_4` | Thin Overlay | various | various | various | various | various | various |
| `ULTRA_THIN_1` | Ultra Thin Overlay | [0, 5] | [3.5, 4.5] | [0, 5] | [3.5, 5] | [4, 5] | [3.5, 4.5] |

### 6.2 Design Patterns

**Preservation treatments** (Crack Seal, Cape Seal, Chip Seal, Microsurfacing, Ultra Thin) target narrow condition windows near the top of the scale -- the pavement must still be in relatively good condition. This reflects the engineering principle of "right treatment at the right time."

**Rehabilitation treatments** (Thin Overlay, Thick Overlay) have wider windows that overlap with preservation at the upper end and extend into worse conditions. Multiple branches capture different failure modes (ride vs. structural vs. edge).

**Reconstruction** has 5 branches, each targeting a **single index at catastrophic failure** (0-1 range). Any one index reaching near-zero can independently trigger reconstruction.

**Concrete treatments** (Minor/Major CPR Diamond Grind, Saw & Seal) use CSI and JCI as their discriminating indices, with PSI as a secondary factor. RDI, SCI, and ECI are set to [0, 5] (always pass) since these are asphalt-specific indices that default to 5 for concrete.

### 6.3 Treatment Condition Windows (Visual)

```
Condition Index Scale:  0 -------- 1 -------- 2 -------- 3 -------- 4 -------- 5
                      FAILED     POOR     MARGINAL    FAIR       GOOD    EXCELLENT

Crack Seal (CSI):                                              |===|
                                                              4.3  4.5

Cape Seal (ECI):                                    |==========|
                                                   3.0        4.5

Chip Seal (SCI):                                       |======|
                                                      3.5    4.5

Microsurfacing (PSI):                                  |===|
                                                      3.6  4.5

Ultra Thin (RDI):                                          |===|
                                                          4.0  5.0

Thin Overlay (PSI):                      |=============|
                                        2.0           3.5

Thick Overlay (PSI):              |===============|
                                 1.0             2.5

Reconstruction (any):     |=======|
                         0.0     1.0

Minor CPR DG (PSI):                  |=====|
                                    2.5   3.0

Major CPR DG (PSI):           |========|
                             1.0      2.5
```

This illustrates how treatments tile the condition spectrum -- as a pavement deteriorates from 5 toward 0, it moves through the eligibility windows of progressively heavier treatments.

---

## 7. County Treatment Triggers

County Route treatments use a **different trigger mechanism**. Instead of referencing the `Analysis_Lookup_Triggers` lookup table, they use **hardcoded conditions** directly in their trigger expressions.

### 7.1 County Chip Seal

```
Eligible when:
    CCI >= 2.8 AND CCI <= 4.0
    AND AADT < 1000
    AND NOT on NHS (National Highway System)
    AND section_length >= 0.5 miles
    AND number_of_lanes <= 2
    AND chip_seal_count <= 1  (no more than 1 prior chip seal)
```

**Rationale**: Chip seals are a low-cost preservation treatment appropriate for low-volume county roads in fair condition. The AADT, NHS, and lane-count restrictions ensure they are only applied to roads where this treatment is operationally appropriate.

### 7.2 County Microsurfacing

```
Eligible when:
    County Thick Overlay was applied 5-7 years ago
    (time-based subsequent treatment, not condition-based)
```

**Rationale**: This is a **planned follow-up** treatment. After a County Thick Overlay, a microsurface is scheduled at the 5-7 year mark as a preservation measure to extend the overlay's life. This is not condition-triggered -- it fires on schedule.

### 7.3 County Thin Overlay

```
Eligible when:
    CCI >= 1.0 AND CCI <= 2.0
    AND AADT >= 250
    AND correct_surface_type
```

**Rationale**: Thin overlays address county roads in poor condition (CCI 1-2) that still have enough traffic volume (AADT >= 250) to justify the investment.

### 7.4 County Thick Overlay

```
Eligible when:
    (CCI < 1.0 AND IRI > 150)
    OR
    (cracking_percentage >= 15%)  -- calculated as raw_distress_lengths / section_area
    AND AADT >= 200
```

**Rationale**: Thick overlays are the heaviest county treatment, triggered by either catastrophic ride quality (CCI < 1 with high IRI) or extensive cracking (15%+ of surface area). The AADT floor of 200 ensures minimum traffic to justify the cost.

### 7.5 State vs. County Trigger Comparison

| Feature | State Route Triggers | County Route Triggers |
|:--------|:--------------------|:---------------------|
| Threshold source | Lookup table (`Analysis_Lookup_Triggers`) | Hardcoded in expressions |
| Condition variables | 6 individual indices (PSI, RDI, SCI, CSI, ECI, JCI) | CCI (composite) + raw measurements |
| Multi-branch logic | Yes (up to 5 branches per treatment) | Limited (1-2 conditions) |
| Traffic filtering | No (handled by analysis set segmentation) | Yes (AADT thresholds) |
| NHS filtering | No | Yes (County Chip Seal excludes NHS) |
| Lane filtering | No | Yes (County Chip Seal max 2 lanes) |
| Counter tracking | No | Yes (chip seal count limit) |
| Time-based triggers | No | Yes (County Microsurfacing) |

---

## 8. Cost Calculation

### 8.1 State Route Treatment Costs

All State Route treatments use the same cost formula:

```
Cost = section_length * lanes * cost_per_lane_mile * inflation_factor
```

Where:

- **`section_length`** = `Get_Field('341dd9ab...')` -- section length in miles from inventory
- **`lanes`** = number of lanes (defaults to 2 if missing)
- **`cost_per_lane_mile`** = looked up from `Analysis_Lookup_Trt_Costs` table using key format: `{treatment}_{branch}_{pavement_type}`
  - Example key: `Thin_Overlay_1_BC` (thin overlay, branch 1, asphalt)
  - Example key: `Major_CPR_DG_1_RC` (major CPR diamond grind, branch 1, concrete)
- **`inflation_factor`** = computed expression adjusting for the year of application relative to the analysis base year

```
Lookup: DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs',
                           'Cost_Per_Lane_Mile',
                           'KEY',
                           '{treatment}_{branch}_{pave_type}',
                           TRUE)
```

### 8.2 Committed Treatment Costs

When a section has pre-committed treatments, the cost is **not** calculated from the lookup table. Instead, it comes from pre-entered committed cost fields associated with the committed treatment record. This allows WVDOT to enter actual contract costs for programmed work.

### 8.3 County Route Treatment Costs

County treatments use a **separate** lookup table: `DEL_Analysis_Lookup_CountyTrt_Costs`

The lookup key format is: `{treatment}_{district_code}`

This allows costs to vary by WVDOT district, reflecting regional differences in contractor pricing and mobilization costs.

```
Lookup: DAL_DCG_STLOOKUP('DEL_Analysis_Lookup_CountyTrt_Costs',
                           'Cost_Per_Lane_Mile',
                           'KEY',
                           '{treatment}_{district}',
                           TRUE)
```

### 8.4 Present Value Computation

For optimization, raw costs are converted to present value:

```
PV_Cost = Cost / (1 + discount_rate) ^ (year - base_year)
```

Where the discount rate is typically **4%** (see Section 11).

---

## 9. Treatment Resets

When a treatment is applied, the system must update the section's condition to reflect the improvement. This involves resetting multiple variables in a specific sequence.

### 9.1 Variables Reset by Treatment Application

| Variable Category | What Gets Reset | How |
|:------------------|:---------------|:----|
| **Condition Indices** (CCI, CSI, ECI, JCI, PSI, RDI, SCI) | Reset to treatment-specific improved values | Via named reset expressions (e.g., `nRES_CCI_CHIP_SEAL`, `nRES_SCI_THICK_OVL`) |
| **Age Variables** (AGE_PSI, AGE_RDI, etc.) | Reverse-computed from new index value | Via `Exp_*_AGE_FROM_INDEX` expressions |
| **RSL** | Recalculated | MIN of years-to-threshold across all indices |
| **Raw Measurements** (IRI, RUT, PCRK, FLT) | Recalculated from new indices | Using inverse formulas (Section 3.3) |
| **Counters** (chip seal count, microsurface count) | Incremented | +1 when respective treatment applied |
| **GFP Ratings** | Recalculated | Good/Fair/Poor for IRI, RUT, Cracking, MAP-21, Faulting |
| **Yearly Cost** | Set to treatment cost | From cost calculation |
| **Yearly Treatment** | Set to treatment name | String identifier |

### 9.2 The Age Reset Mechanism

This is one of the most elegant aspects of the system. When a treatment improves a condition index (say, from 2.5 to 4.0), the system cannot simply continue deterioration from age = current_age. Instead, it must find the **equivalent age** on the deterioration curve that corresponds to the new (reset) index value.

```
Before treatment:              After treatment:
Index                          Index
  5 |                            5 |*
    |                              |  * <-- new starting point
  4 |                            4 |    *
    |                              |      *
  3 |                            3 |        *
    |          *                   |          *
  2 |            * <-- here        |            *
    |              *               |              *
  1 |                              |
  0 +----------+----> Age       0 +--+-----------> Age
    0         15                   0  5 (equiv.)

The treatment resets index from 2.5 to 4.0.
The "equivalent age" for index=4.0 is ~5 years.
Deterioration resumes from that point on the curve.
```

The `Exp_*_AGE_FROM_INDEX` expressions perform this reverse computation by inverting the `DAL_DCG_INDEXFROMAGE()` function.

### 9.3 Reset Magnitude by Treatment Type

Different treatments provide different levels of improvement. The general pattern:

```
Treatment Impact on Indices (conceptual):

                    PSI    RDI    SCI    ECI    CCI
                    ----   ----   ----   ----   ----
Crack Seal          ~      ~      +      ~      +
Cape Seal           +      +      +      +      +
Chip Seal           +      +      +      +      +
Microsurfacing      +      ++     +      +      +
Ultra Thin Overlay  ++     ++     +      +      ++
Thin Overlay        ++     ++     ++     ++     ++
Thick Overlay       +++    +++    +++    +++    +++
Reconstruction      5.0    5.0    5.0    5.0    5.0

~ = minimal/no improvement
+ = minor improvement
++ = moderate improvement
+++ = major improvement
5.0 = full reset to new condition
```

Reconstruction resets all indices to 5.0 (brand new). Lighter treatments provide partial improvements, with the magnitude depending on the specific index and the treatment-specific reset expression.

---

## 10. Treatment Sequencing

### 10.1 Subsequent Treatment Rules

Each treatment defines which treatments are **allowed to follow it** in the analysis. This prevents illogical sequences (e.g., applying a crack seal immediately after reconstruction).

| After This Treatment | Can Be Followed By |
|:---------------------|:-------------------|
| **Crack Seal** | Chip Seal, Cape Seal, Microsurfacing, Ultra Thin Overlay, Thin Overlay, Thick Overlay, Reconstruction, Saw & Seal |
| **Cape Seal** | Chip Seal, Microsurfacing, Ultra Thin Overlay, Thin Overlay, Thick Overlay, Reconstruction |
| **Chip Seal** | Cape Seal, Microsurfacing, Ultra Thin Overlay, Thin Overlay, Thick Overlay, Reconstruction |
| **Microsurfacing** | Chip Seal, Cape Seal, Ultra Thin Overlay, Thin Overlay, Thick Overlay, Reconstruction |
| **Ultra Thin Overlay** | Chip Seal, Cape Seal, Microsurfacing, Thin Overlay, Thick Overlay, Reconstruction |
| **Preservation** | Chip Seal, Cape Seal, Microsurfacing, Ultra Thin Overlay, Thin Overlay, Thick Overlay, Reconstruction |
| **Thin Overlay** | Crack Seal, Chip Seal, Cape Seal, Microsurfacing, Ultra Thin Overlay, Thick Overlay, Reconstruction |
| **Thick Overlay** | Crack Seal, Chip Seal, Cape Seal, Microsurfacing, Ultra Thin Overlay, Thin Overlay, Reconstruction |
| **Reconstruction** | Nearly all treatments (full reset enables any subsequent) |
| **Minor CPR Diamond Grind** | Major CPR Diamond Grind, Saw & Seal, Thin Overlay, Thick Overlay, Reconstruction |
| **Major CPR Diamond Grind** | Minor CPR Diamond Grind, Saw & Seal, Thin Overlay, Thick Overlay, Reconstruction |
| **Saw & Seal Joints** | Minor CPR Diamond Grind, Major CPR Diamond Grind, Reconstruction |

### 10.2 County Sequencing

| After This Treatment | Can Be Followed By |
|:---------------------|:-------------------|
| **County Thick Overlay** | County Microsurfacing (at 5-7 year interval), County Thin Overlay, County Thick Overlay |
| **County Thin Overlay** | County Chip Seal, County Microsurfacing, County Thick Overlay |
| **County Chip Seal** | County Thin Overlay, County Thick Overlay |
| **County Microsurfacing** | County Chip Seal, County Thin Overlay, County Thick Overlay |

### 10.3 Reapplication Intervals

The `Interval` field (Section 4) controls the **minimum time between treatments** of the same type. Combined with the sequencing rules, this creates realistic treatment timelines:

```
Example asphalt section lifecycle:

Year 0:  New construction (all indices = 5.0)
Year 8:  Crack Seal (SCI starting to drop)
Year 12: Microsurfacing (PSI and ECI declining)
Year 19: Thin Overlay (multiple indices in moderate distress)
Year 27: Thick Overlay (structural decline)
Year 35: Reconstruction (end of service life)
```

---

## 11. Analysis Configuration

### 11.1 Analysis Time Horizon

| Parameter | Typical Value |
|:----------|:-------------|
| Start Year | 2023-2025 (varies by analysis set) |
| End Year | 2040-2042 |
| Treatment Application End | 2035-2037 (treatments stop 5 years before end to allow observation of effects) |

### 11.2 Economic Parameters

| Parameter | Value | Purpose |
|:----------|:------|:--------|
| Discount Rate | 4% | Converts future costs/benefits to present value |
| Inflation Rate | 2% | Adjusts treatment costs for future years |

### 11.3 Optimization Configuration

| Parameter | Setting | Meaning |
|:----------|:--------|:--------|
| Optimization Type | `"B"` (Benefit-Cost) | Incremental benefit-cost ratio drives selection |
| Allow Do Nothing | Yes | Sections can receive no treatment if B/C ratio is unfavorable |
| Start IBC at Do Nothing | Yes | Incremental B/C is calculated relative to the do-nothing baseline |
| Benefit Variable | `PMS_nCAV_PV_Benefit` | Present value of condition improvement over analysis horizon |
| Cost Variable | `PMS_nCAV_PV_COST` | Present value of treatment cost |

### 11.4 Budget Structure

Budget scenarios define available funding per year:

| Budget Category | Description |
|:----------------|:------------|
| `Rehabilition` | Main category for most treatments (note: spelling from source system) |
| `MicroSurface` | Dedicated budget for microsurfacing treatments |
| `Preservation` | Preservation-specific budget |
| `Total` | Overall budget cap |
| `Pavement_NHS` | National Highway System pavement budget |
| `Pavement_Non_NHS` | Non-NHS pavement budget |
| `Pavement_Turnpike` | WV Turnpike specific budget |

Typical budget scenarios tested: $45M, $80M, $90M, $100M annual allocations.

### 11.5 How the Optimizer Works

The optimizer uses **Incremental Benefit-Cost (IBC)** analysis:

```
1. BASELINE: Run the do-nothing scenario for all sections
   - Project deterioration over the full analysis horizon
   - Compute the "area under the condition curve" (baseline benefit = 0)

2. FOR EACH SECTION, FOR EACH ELIGIBLE TREATMENT:
   - Apply the treatment at each feasible year
   - Re-project deterioration from the reset condition
   - Compute the improvement in area under the curve = Benefit
   - Compute the present value of cost
   - Calculate IBC = PV_Benefit / PV_Cost

3. RANK all section-treatment-year combinations by IBC ratio

4. SELECT treatments in IBC order until budget is exhausted:
   - Respect budget category constraints
   - Respect treatment sequencing rules
   - Respect reapplication intervals
   - Continue until no more treatments with positive B/C fit within budget
```

```
Condition
Index
  5 |    *****
    |   /     *****
    |  / BENEFIT   ****           <-- With treatment
    | /  (area)        ****
    |/                     ***
  3 +.........................***..........
    |                           ***
    | *****                        **
    |      *****                     **   <-- Without treatment (do-nothing)
    |           *****                  *
  0 +-------------------------------------------> Year
    2025      2030      2035      2040

Benefit = shaded area between the two curves
```

---

## 12. End-to-End Walkthrough

To illustrate how all components work together, consider a concrete example:

### Scenario: 1.2-mile asphalt section on a state route

**Year 2025 -- Initial Conditions:**
- PSI = 3.8, RDI = 4.2, SCI = 3.9, ECI = 4.0
- CSI = 5.0 (forced, asphalt), JCI = 5.0 (forced, asphalt)
- CCI = MIN(3.8, 4.2, 3.9, 5.0, 4.0, 5.0) = **3.8**
- No committed treatments
- Section length = 1.2 mi, 2 lanes

**Step 1: Deterioration**

The engine advances each age variable by 1 year and recomputes all indices via `DAL_DCG_INDEXFROMAGE()`. Suppose by Year 2027:
- PSI = 3.4, RDI = 3.8, SCI = 3.3, ECI = 3.6
- CCI = MIN(3.4, 3.8, 3.3, 3.6) = **3.3** (SCI governs)

**Step 2: Trigger Evaluation**

The engine evaluates all 14 State Route treatment triggers. Checking against `Analysis_Lookup_Triggers`:

- **Crack Seal**: CSI must be in [4.3, 4.5] -- CSI is 5.0 (asphalt forced). **Eligible? No** (CSI = 5 exceeds 4.5 upper bound).
- **Cape Seal**: ECI in [3, 4.5] = 3.6 passes. PSI in [3, 5] = 3.4 passes. RDI in [3.5, 5] = 3.8 passes. SCI in [3, 4.5] = 3.3 passes. **Eligible? Yes.**
- **Chip Seal**: SCI in [3.5, 4.5] = 3.3 fails (below 3.5). **Eligible? No.**
- **Microsurfacing**: PSI in [3.6, 4.5] = 3.4 fails (below 3.6). **Eligible? No.**
- **Ultra Thin Overlay**: RDI in [4, 5] = 3.8 fails. **Eligible? No.**
- **Thin Overlay (branch 1)**: Suppose PSI range is [2.0, 3.5] = 3.4 passes. SCI range check passes. **Eligible? Yes.**

So in Year 2027, this section is eligible for **Cape Seal** and **Thin Overlay**.

**Step 3: Cost & Benefit Calculation**

For each eligible treatment:

- **Cape Seal**: Cost = 1.2 mi * 2 lanes * $X/lane-mile * inflation = $A
  - Projects condition improvement, computes PV_Benefit
  - IBC = PV_Benefit / PV_Cost = ratio_A

- **Thin Overlay**: Cost = 1.2 mi * 2 lanes * $Y/lane-mile * inflation = $B
  - Projects larger condition improvement, computes PV_Benefit
  - IBC = PV_Benefit / PV_Cost = ratio_B

**Step 4: Optimization**

The optimizer ranks all section-treatment combinations across the entire network by IBC ratio. If the Thin Overlay on this section has a higher IBC than competing needs elsewhere, it gets selected. If not, the Cape Seal might be selected, or the section might receive no treatment this year.

**Step 5: Treatment Application (Thin Overlay selected)**

- PSI resets from 3.4 to ~4.5 (via `nRES_PSI_THIN_OVL`)
- RDI resets from 3.8 to ~4.6
- SCI resets from 3.3 to ~4.3
- ECI resets from 3.6 to ~4.4
- CCI recalculated: MIN(4.5, 4.6, 4.3, 4.4) = **4.3**
- Age variables reverse-computed to match new index values
- RSL recalculated (now much higher)
- IRI, RUT recalculated from new PSI, RDI
- Yearly Cost set to $B
- Treatment record logged

**Step 6: Continue**

Deterioration resumes from the reset condition. The section continues through the analysis horizon, potentially receiving another treatment when it deteriorates enough to trigger one from the allowed subsequent list.

---

## Appendix A: Variable GUID Quick Reference

For implementers working with the raw expressions, here is the complete GUID mapping:

```
CONDITION INDICES:
42943fcd  PMS_nAAV_CND_PSI      Present Serviceability Index
1c8052d3  PMS_nAAV_CND_RDI      Rut Depth Index
ee3c6523  PMS_nAAV_CND_SCI      Structural Cracking Index
52c46a28  PMS_nAAV_CND_CSI      Cracking Severity Index
1fe36102  PMS_nAAV_CND_ECI      Edge Condition Index
64b7d597  PMS_nAAV_CND_JCI      Joint Condition Index
b17f394f  PMS_nAAV_CND_CCI      Composite Condition Index

RAW MEASUREMENTS:
3ae48bd7  PMS_nAAV_CND_IRI      International Roughness Index
f3e74fb6  PMS_nAAV_CND_RUT      Rut Depth
af5bdd9f  PMS_nAAV_CND_PCRK     Percent Cracking
eeec27ce  PMS_nAAV_CND_FLT      Faulting

AGE VARIABLES:
963cad98  PMS_nAAV_AGE_PSI
6426b3ef  PMS_nAAV_AGE_RDI
c4865c39  PMS_nAAV_AGE_SCI
ceb172c5  PMS_nAAV_AGE_CSI
981a9f97  PMS_nAAV_AGE_ECI
d467ebc5  PMS_nAAV_AGE_JCI
dbff2024  PMS_nAAV_AGE_CCI

OTHER:
93a9dd02  PMS_nAAV_CND_RSL      Remaining Service Life
674cee68  PMS_nAAV_TRF_ADT      Traffic (AADT)
aa88ec97  PMS_tDAV_Pave_Type    Pavement Type (BC/RC)
7014cb8f  PMS_nDAV_CNT_CHIP_SEALS    Chip Seal Counter
1e9fd63b  PMS_nDAV_CNT_MICROSURFACE  Microsurface Counter

BENEFIT/COST:
9e42983d  PMS_nCAV_PV_Benefit   Present Value of Benefit
e8d463f4  PMS_nCAV_PV_COST      Present Value of Cost
478feca0  PMS_nAAV_Yrly_Cost    Yearly Cost

INVENTORY FIELDS:
68ed04d3  RSL_Threshold_Code    RSL threshold classification
341dd9ab  Section Length         Section length in miles
```

---

## Appendix B: Key Deighton dTIMS Functions

| Function | Signature | Purpose |
|:---------|:----------|:--------|
| `DAL_DCG_INDEXFROMAGE` | `(p1, p2, p3, p4, max, age)` | Compute condition index from age using parametric S-curve |
| `DAL_DCG_STLOOKUP` | `(table, column, key_col, key_val, exact)` | Look up a value from a named table |
| `DAL_DCG_MIN10` | `(v1, v2, ..., v10)` | Return minimum of up to 10 values (used for RSL) |
| `GET_ANALVR` | `(guid)` | Get current value of analysis variable |
| `Get_Field` | `(guid)` | Get inventory field value |
| `Get_Exp` | `(guid)` | Evaluate a named expression |
| `IS_COMMITTED` | `()` | Check if section has pre-committed treatments |
| `GET_TRTYR` | `(treatment_name)` | Get year a treatment was last applied |
| `YR` | (built-in) | Current analysis year |

---

## Appendix C: Data Source Details

| Source | Contents | Format |
|:-------|:---------|:-------|
| `dtims_dump.sqlite` | Full OData dump of the WVDOT dTIMS instance including analysis variables, expressions, treatments, triggers, costs, deterioration models, and analysis configurations | SQLite database |
| `2025_12_17_Analysis_Lookup_Triggers.xlsx` | The `Analysis_Lookup_Triggers` table with 25 rows of condition index bounds per treatment branch | Excel spreadsheet |
| `schema.xml` | OData EDMX schema defining all entity types and relationships | XML |
