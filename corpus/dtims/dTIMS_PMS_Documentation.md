# dTIMS Pavement Management System (PMS) — Comprehensive Documentation

> Deduced from `schema.xml` (OData EDMX v4.0 configuration schema) and `2025_12_17_Analysis_Lookup_Triggers.xlsx` (treatment trigger lookup table), supplemented by public dTIMS documentation from Deighton Associates, NDDOT, UDOT, and SDDOT.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Core Data Model](#3-core-data-model)
4. [Condition Indices](#4-condition-indices)
5. [Deterioration Modeling](#5-deterioration-modeling)
6. [Treatments](#6-treatments)
7. [Treatment Triggers](#7-treatment-triggers)
8. [Strategies](#8-strategies)
9. [Optimization — Incremental Benefit-Cost (IBC)](#9-optimization--incremental-benefit-cost-ibc)
10. [Budget Scenarios](#10-budget-scenarios)
11. [Analysis Workflow End-to-End](#11-analysis-workflow-end-to-end)
12. [Supporting Subsystems](#12-supporting-subsystems)
13. [Complete Treatment Trigger Table](#13-complete-treatment-trigger-table)
14. [Entity Reference](#14-entity-reference)

---

## 1. Overview

**dTIMS** (Deighton Total Infrastructure Management System) is a commercial, off-the-shelf infrastructure asset management platform developed by Deighton Associates Ltd. It is the industry-standard pavement management system used by numerous state DOTs (Departments of Transportation) across North America and road authorities worldwide.

### Purpose

dTIMS provides infrastructure managers with the ability to:

- **Inventory** — store and manage pavement section data with full linear referencing
- **Assess condition** — track multiple condition indices across the network
- **Model deterioration** — forecast future pavement condition using expression-based deterioration curves
- **Define treatments** — configure maintenance, rehabilitation, and reconstruction treatments with triggers, costs, and resets
- **Optimize spending** — determine the most cost-effective combination of treatments across the network under budget constraints using Incremental Benefit-Cost (IBC) analysis
- **Produce construction programs** — output year-by-year work plans with mapped locations

### Two Core Components

In its simplest form, dTIMS comprises:

1. **Database Component** — stores inventory data (pavement sections, attributes, condition history) and analysis configuration (treatments, variables, curves, triggers)
2. **Analysis Component** — executes the optimization engine that determines the best preservation and improvement actions for each pavement section given budgetary and technical constraints

---

## 2. Architecture

### OData API Layer

The system exposes its configuration through an **OData v4.0 EDMX** service (as documented in `schema.xml`). The primary namespace is:

```
DataServices.Configuration.Models
```

All configuration entities are accessed via this API, which supports standard OData operations (CRUD, filtering, navigation properties, batch operations). The API enables external applications (including custom analysis engines) to read and write all configuration data programmatically.

### Technology Stack

From the schema, the following technology components are evident:

| Component | Technology |
|-----------|-----------|
| API Protocol | OData v4.0 (EDMX) |
| Database | SQL Server or Oracle (configurable via `DataServicesConfiguration`) |
| Authentication | Windows Auth or custom (`UseWindowsAuth`, role-based ACLs) |
| GIS | ArcGIS integration, WMS/WFS layers, SRID-aware geometry |
| Reporting | Telerik Reports, Power BI embedded |
| Spatial | Geometry types with SRID, linear referencing (LRM) |
| Execution | Async execution service with scheduling (`ExecutionRequest`, `ServiceStatus`) |

### Key Namespaces in the Schema

| Namespace | Purpose |
|-----------|---------|
| `DataServices.Configuration.Models` | Core entity types (60+ entities) |
| `DataServices.Configuration.Models.ProjectHistory` | Asset forms and field lookups |
| `DataServices.Configuration.Models.Unmapped.AnalysisResults` | Analysis output types (strategies, charts, costs) |
| `DataServices.Database.Security.Audit` | Audit logging |
| `dTIMS.Data.Dependency` | Dependency tracking |
| `dTIMS.Data.Import` | Import result types |

---

## 3. Core Data Model

### 3.1 Inventory Layer

#### `dTIMSEntity` — Tables
The foundational entity representing a data table in the system. Every inventory table, strategy table, history table, and child table is a `dTIMSEntity`.

Key properties:
- `TableID` (Int32) — internal table identifier
- `TableTypeID` → `TableType` — classification (base, historic, lane, child, etc.)
- `BaseTableID` — parent table for derived/child tables
- `UnitOfMeasure` — measurement system
- `Historic` / `HistoricID` — links to time-series history table
- `Lane` / `LaneID` — links to lane-level detail table
- `Schema`, `TableName`, `DatabaseTableName` — physical DB mapping
- `HasRowSecurity`, `IsLogged` — security and audit controls
- Specialized flags: `IsInspectionTable`, `IsWorkOrder`, `IsTask`, `IsProject`, `IsSchedule`, `IsAssetGroup`, `IsDefect`, `IsChecklist`

Navigation properties connect to: Attributes, Expressions, ChildRelations, AnalysisSets, Treatments, DataImports, GIS integrations, Map layers, etc.

#### `dTIMSAttribute` — Columns
Defines individual columns/fields on a `dTIMSEntity`.

Key properties:
- `EntityID` → parent table
- `Type` / `TypeID` → `dTIMSAttributeType` — data type (numeric, string, date, decimal, boolean)
- `Size`, `Decimal` — precision
- `StringDefault`, `DoubleDefault`, `DateTimeDefault`, `DecimalDefault` — default values
- `DoubleMinimum/Maximum`, `DecimalMinimum/Maximum`, `DateTimeMinimum/Maximum` — validation ranges
- `IsNullable`, `IsRequired`, `IsReadOnly`, `IsInternal`, `IsPrimary`
- `ExpressionID` — computed column formula
- `ValidationExpressionID` — validation rule
- `TableCodeAttributeID` → lookup table for coded values
- `TransformationClass` — data transformation type

#### `AttributeTableCode` — Coded Value Lookups
Maps attribute values to human-readable decodes with display colors:
- `AttributeID` — which attribute
- `Code` — stored value
- `Decode` — display value
- `Color` — visualization color

#### `EntityRelation` — Table Relationships
Defines parent-child relationships between entities:
- `ParentEntityID`, `ChildEntityID`, `RelationAttributeID` — the foreign key joining them

### 3.2 Expression System

dTIMS has a powerful expression engine used throughout the system for formulas, filters, transformations, and computed values.

#### `dTIMSExpression` — Database Expressions
Stored expressions that operate at the database level. Used for filters, computed columns, and transformations.

Key properties:
- `Expression` (String) — the formula text
- `AttributeTypeID` → result data type

Referenced by: Analysis variables, treatments, filters, cross-tab queries, dataview columns, GIS mappings, and more.

#### `RuntimeExpression` — Analysis-Time Expressions
Expressions evaluated during the analysis engine execution (runtime). Structurally identical to `dTIMSExpression` but evaluated in the analysis context where analysis variables and deterioration state are available.

Used for: Deterioration curves, treatment costs, treatment resets, trigger filters, initialization expressions, and discard filters.

#### `dFragExpression` — Defragmentation Expressions
Specialized expressions used in the project defragmentation (dFrag) process.

#### `ExpressionFunction` — Built-in Functions
Catalog of available functions that can be used in expressions:
- `Name`, `Description`, `Syntax`

### 3.3 Analysis Configuration

#### `AnalysisSet` — The Central Analysis Definition

This is the most important configuration entity. An `AnalysisSet` defines a complete analysis run.

Key properties:

| Property | Purpose |
|----------|---------|
| `StartYear`, `EndYear` | Analysis time horizon |
| `EndTreatmentApplicationYear` | Last year treatments can be applied |
| `EndPerformancePlotYear` | Last year for performance plotting |
| `DiscountRate`, `InflationRate` | Economic parameters for present value calculations |
| `InventoryID` → `dTIMSEntity` | The pavement inventory table |
| `StrategyID` → `dTIMSEntity` | The strategy output table |
| `ConditionVariableID` → `AnalysisVariable` | Primary condition variable (e.g., PCI) |
| `TrafficVariableID` → `AnalysisVariable` | Traffic variable (e.g., AADT) |
| `FilterID` | Subset of inventory to analyze |
| `ConditionCategoryBoundary12..45` | Thresholds dividing condition into 5 categories |
| `ConditionCategory1Name..5Name` | Labels for each category (e.g., "Very Good", "Good", "Fair", "Poor", "Very Poor") |
| `IntervalValue1..50` | Up to 50 year-interval budget values |
| `UsesAdvanced` | Whether advanced analysis features are enabled |
| `GenerateCommittedOnly` | Only generate committed strategies |
| `ConstraintType` | Type of constraint applied |
| `LevelOfGeneration` | Strategy generation depth |
| `ElementList` | Specific elements to analyze |

Navigation properties:
- `Treatments` → `Collection(AnalysisSetTreatment)` — treatments included in this analysis
- `Variables` → `Collection(AnalysisSetPerformanceIndex)` — performance indices tracked
- `BudgetScenarios` → optimization scenarios
- `SAMscenarios` → Strategic Asset Management scenarios

#### `AnalysisSetTreatment` — Treatment Inclusion
Links a `Treatment` to an `AnalysisSet` with an `Order` field controlling evaluation priority.

#### `AnalysisSetPerformanceIndex` — Variable Inclusion
Links an `AnalysisVariable` (performance index) to an `AnalysisSet` with ordering.

#### `AnalysisVariable` — Performance Variables

Each measurable aspect of pavement condition is an `AnalysisVariable`. This includes condition indices (PCI, PSI, RDI, etc.), traffic measures (AADT), and computed benefit/cost variables.

Key properties:

| Property | Purpose |
|----------|---------|
| `AttributeID` → `dTIMSAttribute` | Source data column in inventory |
| `ParentTableID` | Which inventory table |
| `Slope` | Deterioration direction ("ascending" or "descending") |
| `ShiftCurve` | Whether to shift the deterioration curve to match current condition |
| `Keep` | Whether to retain this variable's values between analysis years |
| `InitializeExpressionID` / `InitializeAttributeID` | How to set the initial value |
| `fromAttribute` | Initialize from attribute value |
| `IsReset` | Whether this variable can be reset by treatments |
| `AreValuesSupplied` | Whether values are user-supplied rather than modeled |
| `DiscardFilterID` | Expression to discard sections from analysis |
| `LookupID` → self-reference | Lookup to another analysis variable |
| `UseInROI` | Include in Return on Investment calculations |
| `Type` | Variable classification |

Navigation properties:
- `Curves` → `Collection(AnalysisVariableCurve)` — deterioration curves
- `TreatmentResets` — how treatments affect this variable

#### `AnalysisVariableCurve` — Deterioration Curves

Defines how an analysis variable changes over time (deterioration or improvement).

Key properties:

| Property | Purpose |
|----------|---------|
| `AnalysisVariableID` | Which variable this curve applies to |
| `FilterID` → `RuntimeExpression` | Condition for when this curve applies (e.g., surface type = "asphalt") |
| `ExpressionID` → `RuntimeExpression` | The deterioration formula |
| `Order` | Priority when multiple curves could match |
| `WorstTolerable` | Minimum acceptable value — triggers action |
| `BenefitCutoff` | Year beyond which benefits are not counted |

The system evaluates curves in order; the first matching filter wins. This allows different deterioration rates for different pavement types, traffic levels, or climate zones.

### 3.4 Condition Categories

#### `ConditionCategory` — Rating Bins

Defines how continuous condition values are binned into discrete categories for reporting and visualization.

- Up to 8 categories with configurable `Range1..8` boundaries
- Each category has `Name1..8`, `DisplayName1..8`, and `Color1..8`
- Can be scoped to a specific `AnalysisVariable`, `BudgetScenario`, `AnalysisSet`, or `Filter`

The `AnalysisSet` itself also defines 5 condition category boundaries (`ConditionCategoryBoundary12..45`) with names, establishing the primary condition rating scale (typically: Very Good / Good / Fair / Poor / Very Poor).

---

## 4. Condition Indices

### 4.1 Index Definitions

The `Analysis_Lookup_Triggers` spreadsheet reveals six condition sub-indices used to characterize pavement health. Based on pavement engineering conventions and the trigger patterns observed:

| Index | Full Name (Deduced) | Measures | Scale |
|-------|---------------------|----------|-------|
| **PSI** | Present Serviceability Index | Ride quality, roughness (related to IRI) | 0-5 (5 = best) |
| **RDI** | Rutting/Ride Distress Index | Rutting depth, ride distress | 0-5 (5 = best) |
| **CSI** | Cracking Severity Index | Surface cracking extent and severity | 0-5 (5 = best) |
| **ECI** | Edge Condition Index | Edge deterioration, shoulder dropoff | 0-5 (5 = best) |
| **JCI** | Joint Condition Index | Joint spalling, faulting (concrete pavements) | 0-5 (5 = best) |
| **SCI** | Structural Condition Index | Overall structural capacity, deflection | 0-5 (5 = best) |

### 4.2 Scale Interpretation

All indices use a **0 to 5 scale** where:
- **5.0** = Excellent / New condition
- **4.0-5.0** = Good condition
- **3.0-4.0** = Fair condition
- **2.0-3.0** = Poor condition
- **1.0-2.0** = Very Poor condition
- **0.0-1.0** = Failed / Critical

Some triggers use **-1** as a lower bound (e.g., Thick_Overlay_1), which effectively means "any value including below zero" — likely representing severely deteriorated pavements where index calculations can produce negative values.

### 4.3 Composite Condition

These sub-indices are typically combined into a composite **PCI (Pavement Condition Index)** or overall condition rating. The `AnalysisSet` entity supports this through its `ConditionVariableID` (pointing to the primary composite condition variable) and `ConditionCategoryBoundary12..45` properties (defining the category thresholds).

In dTIMS, condition data is collected at fine intervals (often 0.1-mile) and aggregated at the section level to compute these indices.

---

## 5. Deterioration Modeling

### 5.1 How Deterioration Works

Each `AnalysisVariable` can have one or more `AnalysisVariableCurve` entries that define how that variable changes over time. The deterioration model:

1. **Initializes** the variable from the current inventory value (`InitializeAttributeID` or `InitializeExpressionID`)
2. **Optionally shifts** the standard deterioration curve to pass through the current observed value (`ShiftCurve = true`)
3. **Applies** the matching curve expression each year to project future values
4. **Respects** the `Slope` property — indicating whether the variable increases or decreases over time
5. **Stops** at the `WorstTolerable` value — the floor/ceiling beyond which the variable cannot deteriorate further

### 5.2 Curve Selection

When multiple curves exist for a variable, the system evaluates them in `Order`:
- Each curve has a `FilterID` (RuntimeExpression) that acts as a guard condition
- Common filters include surface type (asphalt vs. concrete), traffic class, functional class, or climate zone
- The **first curve whose filter evaluates to true** is used for that section

### 5.3 Benefit Cutoff

The `BenefitCutoff` property on `AnalysisVariableCurve` defines the year beyond which condition improvements from treatments are not counted in benefit calculations. This prevents unrealistically large benefits from being assigned to treatments applied early in the analysis period.

---

## 6. Treatments

### 6.1 Treatment Entity

A `Treatment` in dTIMS represents a specific maintenance, rehabilitation, or reconstruction action that can be applied to a pavement section.

Key properties from the schema:

| Property | Purpose |
|----------|---------|
| `Type` | Classification: "Preventive", "Rehabilitation", "Reconstruction", etc. |
| `IntervalYear` | Minimum years between applications of this treatment |
| `BudgetCategoryID` → `BudgetCategory` | Which budget pool funds this treatment |
| `TriggerFilterID` → `RuntimeExpression` | Condition-based eligibility rule |
| `TriggerTemplate` | Template for auto-generating trigger expressions |
| `ApplyAfterInitial` | Can only be applied after an initial treatment |
| `IsInitial` | This is an initial/construction treatment |
| `PerspectiveID` | Analysis perspective (lane, direction) |
| `OverrideBudgetCategory` | Whether this treatment can use a different budget pool |
| `Color` | Visualization color on maps and charts |

### 6.2 Treatment Components

Each treatment has three critical sub-components:

#### Costs (`TreatmentCost`)
Defines the financial and economic cost of applying the treatment:
- `FinCostExpressionID` → RuntimeExpression — financial cost formula (what the agency pays)
- `EcoCostExpressionID` → RuntimeExpression — economic cost formula (user costs, delay costs)
- `FilterID` — conditional: different costs for different conditions
- `Order` — priority when multiple cost rules match

Cost expressions can reference inventory attributes (lane-miles, width, thickness) and analysis variables to compute per-section costs.

#### Resets (`TreatmentReset`)
Defines how applying the treatment changes (improves) an analysis variable:
- `AnalysisVariableID` — which variable is affected
- `ExpressionID` → RuntimeExpression — the reset formula (e.g., "set PSI to 4.5" or "improve CSI by 1.2")
- `FilterID` — conditional resets based on section characteristics

#### Subsequents (`TreatmentSubsequent`)
Defines follow-up treatments that are automatically applied after this treatment:
- `SubsequentID` → Treatment — the follow-up treatment
- `Order` — sequence of follow-ups

#### Ancillaries (`TreatmentAncillary`)
Additional treatments applied concurrently:
- `AncillaryID` → Treatment — the companion treatment

### 6.3 Treatment Catalog (from Trigger Data)

The trigger spreadsheet reveals 13 distinct treatment types organized from least to most invasive:

| # | Treatment | Type (Deduced) | Description |
|---|-----------|----------------|-------------|
| 1 | **Crack Seal** | Preventive | Fill surface cracks to prevent water infiltration |
| 2 | **Preservation** | Preventive | General preservation activity for pavements with moderate cracking |
| 3 | **Saw and Seal Joints** | Preventive | Cut and seal joints in concrete pavement |
| 4 | **Cape Seal** | Preventive/Surface | Chip seal followed by slurry seal or micro-surfacing |
| 5 | **Chip Seal** | Preventive/Surface | Apply aggregate chips with binder |
| 6 | **Micro Surfacing** | Preventive/Surface | Polymer-modified slurry applied to address minor distresses |
| 7 | **Ultra Thin Overlay** | Light Rehab | Very thin hot-mix overlay (<1") |
| 8 | **Thin Overlay** | Rehabilitation | Hot-mix overlay (1-2") for moderate deterioration |
| 9 | **Thick Overlay** | Rehabilitation | Structural overlay (>2") for significant deterioration |
| 10 | **Minor CPR Diamond Grind** | Concrete Rehab | Concrete pavement restoration with diamond grinding (minor) |
| 11 | **Major CPR Diamond Grind** | Concrete Rehab | Concrete pavement restoration with diamond grinding (major) |
| 12 | **Reconstruction** | Reconstruction | Full pavement removal and rebuild |

---

## 7. Treatment Triggers

### 7.1 How Triggers Work

Treatment triggers define **when a treatment becomes eligible** for a pavement section. In dTIMS, triggers are implemented as `RuntimeExpression` filters attached to the `Treatment.TriggerFilterID` property.

The `Analysis_Lookup_Triggers` spreadsheet defines these triggers as **multi-dimensional condition index bounds**. A treatment is eligible when **ALL six condition indices simultaneously fall within their specified [Lower, Upper] ranges**.

**Trigger Logic:**

```
Treatment is eligible IF:
    CSI_Lower <= CSI <= CSI_Upper  AND
    ECI_Lower <= ECI <= ECI_Upper  AND
    JCI_Lower <= JCI <= JCI_Upper  AND
    PSI_Lower <= PSI <= PSI_Upper  AND
    RDI_Lower <= RDI <= RDI_Upper  AND
    SCI_Lower <= SCI <= SCI_Upper
```

### 7.2 Trigger Branches

Many treatments have **multiple trigger branches** (numbered 1, 2, 3, etc.). Each branch represents a **different condition pathway** that leads to the same treatment. For example:

- **Reconstruction** has 5 branches — it can be triggered by failure in PSI (branch 1), SCI (branch 2), ECI (branch 3), JCI (branch 4), or CSI (branch 5). Each branch targets a different failure mode.
- **Thin Overlay** has 4 branches — different combinations of moderate degradation in ECI, SCI, and RDI.
- **Thick Overlay** has 3 branches — different combinations of degradation in PSI, SCI, and ECI.

Branches are OR'd together: a treatment is eligible if **any** of its branches match.

### 7.3 Trigger Pattern Analysis

#### Preventive Treatments (triggered by early/moderate degradation)

**Crack Seal (1 branch):** Only triggered by a very narrow CSI window (4.3-4.5), meaning early-stage cracking. All other indices are unconstrained (0-5). This is the most selective preventive treatment — only applied when cracking just begins.

**Preservation (1 branch):** Triggered by slightly more advanced cracking (CSI 3.5-4.0). Everything else unconstrained.

**Saw and Seal Joints (1 branch):** Triggered by moderate CSI (3-4) AND moderate JCI (3-4). This targets concrete pavements with joint and cracking issues.

#### Surface Treatments (triggered by moderate surface degradation)

**Cape Seal (1 branch):** Requires moderate-to-good ECI (3-4.5), PSI (3-5), RDI (3.5-5), and SCI (3-4.5). This is a comprehensive surface treatment for pavements that are still in fair-to-good condition but showing multiple moderate issues.

**Chip Seal (1 branch):** Similar to Cape Seal but slightly broader ranges — notably PSI is unconstrained (0-5) and CSI is unconstrained. Focused on ECI (2.5-4.5), RDI (3.5-5), and SCI (3.5-4.5).

**Micro Surfacing (1 branch):** Tight bounds on most indices — ECI (3.5-4.9), PSI (3.6-4.5), RDI (3.5-4.9), SCI (3.5-4.9). This is for pavements still in good condition needing a light treatment.

**Ultra Thin Overlay (1 branch):** Requires good ECI (3.5-4.5), PSI (3.5-5), RDI (4-5), SCI (3.5-4.5). This is a premium preventive treatment for good-condition pavements.

#### Rehabilitation Treatments (triggered by significant degradation)

**Thin Overlay (4 branches):**
- Branch 1: Moderate ECI (2.5-4), PSI (2-3.5), RDI and SCI both 2.5-5
- Branch 2: Lower ECI (2.5-3.5), higher PSI (2.8-5), SCI dropping (2.5-3.5)
- Branch 3: ECI (2.5-3.5), PSI (2.8-5), broader SCI (2.5-5)
- Branch 4: ECI (2.5-3.5), PSI (2.8-5), lower RDI (2.5-4)

**Thick Overlay (3 branches):**
- Branch 1: PSI (1-3.5), SCI dropping to below 3 — most common trigger
- Branch 2: ECI (1-5), SCI (1-2.55) — structural degradation driving
- Branch 3: ECI (1-2.55), broader PSI — edge condition driving

**Minor CPR Diamond Grind (3 branches):**
- Branch 1: PSI in poor range (2.5-3), CSI and JCI moderate (2.5-5)
- Branch 2: JCI dropping (2.5-3.5), PSI broader (2.5-5)
- Branch 3: CSI dropping (2.5-3.5), JCI and PSI broader

**Major CPR Diamond Grind (3 branches):**
- Branch 1: PSI very poor (1-2.5), CSI and JCI poor (1+)
- Branch 2: PSI broader (1-5), unconstrained
- Branch 3: JCI dropping (1-3)

#### Reconstruction (triggered by failure)

**Reconstruction (5 branches):** Each branch targets a single-index failure:
- Branch 1: PSI 0-1 (ride failure)
- Branch 2: SCI 0-1 (structural failure)
- Branch 3: ECI 0-1 (edge failure)
- Branch 4: JCI 0-1 (joint failure)
- Branch 5: CSI 0-1 (cracking failure)

This ensures reconstruction is triggered when **any** single index reaches the failure threshold.

---

## 8. Strategies

### 8.1 Strategy Generation

During analysis, dTIMS generates **strategies** for each pavement section. A strategy is a complete sequence of treatments over the analysis period. The system:

1. Evaluates all treatment triggers for each section in each year
2. Generates all feasible treatment combinations (subject to `IntervalYear` constraints, `ApplyAfterInitial` rules, and `TreatmentSubsequent` chains)
3. For each strategy, projects condition over the full analysis period using deterioration curves and treatment resets
4. Calculates the present value of benefits and costs for each strategy

### 8.2 Strategy Properties

The `StrategyData` complex type in the schema reveals what the analysis outputs per strategy:

| Property | Description |
|----------|-------------|
| `StrategyID` | Unique strategy identifier |
| `ElementID` | Pavement section this strategy applies to |
| `PVBenefits` | Present value of benefits over analysis period |
| `PVCost` | Present value of treatment costs |
| `BenefitByCost` | Benefit-cost ratio |
| `IBC` | Incremental Benefit-Cost ratio |
| `FirstMajor` | Name of the first major treatment in the strategy |
| `Year` | Year of first major treatment |
| `IsSelected` | Whether this strategy was selected by the optimizer |
| `IsBackupSelected` | Alternative selection |
| `IsDoNothing` | This is the do-nothing baseline strategy |
| `IsCommitted` | Committed (locked-in) treatment |
| `IsBaseCommitted` | Base committed treatment |
| `IsMinimumCost` | Lowest-cost strategy |

### 8.3 Strategy Treatments

`StrategyTreatments` provides the year-by-year treatment details:

| Property | Description |
|----------|-------------|
| `StrategyID` | Parent strategy |
| `BudgetScenarioID` | Budget scenario context |
| `Year` | Treatment year |
| `Treatment` | Treatment name |
| `TreatmentType` | Treatment classification |
| `FinancialCost` | Actual agency cost |
| `EconomicCost` | Total economic cost |
| `BudgetCategory` | Funding source |
| `IsSelected` / `IsBackupSelected` | Selection status |

---

## 9. Optimization — Incremental Benefit-Cost (IBC)

### 9.1 What is IBC?

**Incremental Benefit-Cost (IBC)** is dTIMS's primary optimization algorithm. It answers two questions for every pavement section:

1. **Should this section be improved now?**
2. **If so, which treatment is optimal?**

The IBC approach finds the combination of treatments across the entire network that maximizes total network benefit within a given budget.

### 9.2 How IBC Works

#### Step 1: Benefit Calculation (Area Under the Curve)

For each strategy, the **benefit** is calculated as the present value of the area between the strategy's condition curve and the do-nothing condition curve over the analysis period:

```
Benefit = PV( Area_under_strategy_curve - Area_under_do_nothing_curve )
```

This "area under the curve" (AUC) approach captures the cumulative improvement in pavement condition that a treatment provides over its service life. A treatment that improves condition significantly and maintains it longer generates more benefit.

#### Step 2: Cost Calculation

For each strategy, the **cost** is the present value of all treatment financial costs, discounted at the `DiscountRate` and adjusted for `InflationRate` defined in the `AnalysisSet`.

#### Step 3: Strategy Ranking

Strategies for each section are sorted by increasing cost. The IBC ratio between consecutive strategies is:

```
IBC = (Benefit_i - Benefit_{i-1}) / (Cost_i - Cost_{i-1})
```

If the incremental benefit of stepping up to a more expensive treatment is high relative to the incremental cost, it represents good value.

#### Step 4: Network Optimization

The optimizer selects one strategy per section such that:
- Total cost across all sections stays within the budget
- Total network benefit is maximized
- The IBC frontier is respected (`IBCFrontier` property — the minimum acceptable IBC ratio)

### 9.3 IBC Configuration Properties

From the `BudgetScenario` entity:

| Property | Purpose |
|----------|---------|
| `OptimizationType` | "IBC" or other optimization method |
| `IBCFrontier` (Double) | Minimum IBC ratio threshold |
| `StartIBCAtDoNothing` (Boolean) | Whether IBC calculation starts from the do-nothing strategy |
| `AllowDoNothing` (Boolean) | Whether "do nothing" is a valid strategy selection |
| `UseBruteForce` (Boolean) | Use brute-force search (slower but more thorough) |
| `BruceForceTime` (Int32) | Time limit for brute-force search (minutes) — note: likely a typo in schema for "BruteForceTime" |
| `IncludeCommitted` (Boolean) | Include pre-committed treatments |
| `UnlimitedBudget` (Boolean) | Run without budget constraint |
| `TotalBudget` (Boolean) | Use total budget vs. per-category budgets |
| `Continue` (Boolean) | Continue optimization from previous run |
| `UseInROI` (Boolean) | Include in Return on Investment calculations |
| `AnalysisVariableBenefitsID` → `AnalysisVariable` | Which variable measures benefits |
| `AnalysisVariableCostsID` → `AnalysisVariable` | Which variable measures costs |
| `AnalysisVariableAllowableID` | Allowable condition threshold variable |
| `AnalysisVariableMaximizeID` | Variable to maximize |
| `FilterID` | Subset of sections for this scenario |

### 9.4 SAM (Strategic Asset Management)

For cross-asset optimization, the `SAM` and `SAMScenarios` entities support multi-asset scenarios:

- `SAMScenarios` links an AnalysisSet to a Benefit variable, Cost variable, and budget parameters
- `MinimumFunding`, `MaximumFunding` — funding bounds per scenario
- `MultiPass` — multi-pass optimization
- `DoNothing` — include do-nothing option
- `Start_IBC_At_DoNothing` — IBC baseline
- `Number_Of_Minutes` — computation time limit
- `Type` — optimization type

---

## 10. Budget Scenarios

### 10.1 Budget Structure

Budgets are organized hierarchically:

```
BudgetScenario
  └── AnalysisSetBudgetScenario (per BudgetCategory, per Year)
        ├── BudgetYear1 through BudgetYear50
        └── Total
```

#### `BudgetCategory`
Represents a funding source or pool (e.g., "Preservation", "Rehabilitation", "Reconstruction", "Federal Aid"):
- `Level` — hierarchy level
- `Color` — visualization
- Links to Treatments (each treatment belongs to a budget category)

#### `AnalysisSetBudgetScenario`
The actual dollar amounts per category per year:
- `BudgetScenarioID` + `BudgetCategoryID` — composite key
- `BudgetYear1` through `BudgetYear50` — annual budget amounts (Decimal)
- `Total` — total budget across all years
- `IsNotFeasible` — whether this budget level is achievable

### 10.2 Budget Scenario Outputs

After optimization, each budget scenario produces:
- `OptimizationResult` — summary of optimization outcomes
- `OptimizationDate` — when optimization was run
- `Color` — scenario color for charts

The analysis results include:
- `ChartYearData` — condition trend over years per scenario
- `ProgramCost` — cost by year
- `BudgetData` — budget utilization by category

---

## 11. Analysis Workflow End-to-End

```
┌─────────────────────────────────────────────────────────────────┐
│                    1. CONFIGURATION                              │
│                                                                  │
│  AnalysisSet ──► defines year range, discount/inflation rates    │
│       │          condition boundaries, inventory table            │
│       ├── AnalysisVariable(s) ──► condition indices to track     │
│       │       └── AnalysisVariableCurve(s) ──► deterioration     │
│       ├── Treatment(s) ──► eligible M&R actions                  │
│       │       ├── TriggerFilter ──► when to apply                │
│       │       ├── TreatmentCost(s) ──► how much it costs         │
│       │       ├── TreatmentReset(s) ──► how it improves cond.    │
│       │       └── TreatmentSubsequent(s) ──► follow-up actions   │
│       └── BudgetScenario(s) ──► funding levels to evaluate       │
│               └── AnalysisSetBudgetScenario(s) ──► $/yr/category │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    2. INITIALIZATION                              │
│                                                                  │
│  For each section in inventory (filtered by AnalysisSet.Filter): │
│  • Initialize each AnalysisVariable from inventory attribute     │
│  • Optionally shift deterioration curves to current values       │
│  • Evaluate discard filters to exclude sections if needed        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    3. STRATEGY GENERATION                         │
│                                                                  │
│  For each section, for each year in [StartYear, EndYear]:        │
│  • Apply deterioration curves to project condition indices       │
│  • Evaluate treatment triggers against projected condition       │
│  • Generate all feasible treatment sequences (strategies)        │
│  • Apply treatment resets where treatments are applied           │
│  • Respect IntervalYear, ApplyAfterInitial, Subsequent rules    │
│  • Always include "Do Nothing" as a baseline strategy            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    4. BENEFIT-COST CALCULATION                    │
│                                                                  │
│  For each strategy:                                              │
│  • PV(Benefits) = discounted area between strategy and           │
│                   do-nothing condition curves                     │
│  • PV(Costs) = discounted sum of treatment financial costs       │
│  • B/C ratio = PV(Benefits) / PV(Costs)                         │
│  • IBC = incremental benefit-cost vs. next-cheaper strategy      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    5. OPTIMIZATION (per BudgetScenario)           │
│                                                                  │
│  IBC Algorithm:                                                  │
│  • Rank all strategies by IBC ratio                              │
│  • Select highest-IBC strategies until budget exhausted          │
│  • Respect budget category allocations                           │
│  • Apply IBCFrontier minimum threshold                           │
│  • Optionally use brute-force for better solutions               │
│  • Mark selected strategies (IsSelected = true)                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    6. OUTPUTS                                     │
│                                                                  │
│  • ConstructionProgram — year-by-year treatment plan with costs  │
│  • StrategyData — per-section selected strategy details          │
│  • ChartYearData — condition trends over time per scenario       │
│  • ProgramCost — total spending by year and category             │
│  • ConditionCategory distribution — % network in each category   │
│  • Map layers — spatial visualization of the work program        │
│  • Export to strategy tables and external formats                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 12. Supporting Subsystems

### 12.1 dFrag — Project Defragmentation

`dFrag` consolidates individual section-level treatment recommendations into practical construction projects. It addresses the reality that adjacent sections recommended for the same treatment in the same year should be combined.

Key properties:
- `RoadExpressionId` / `DirectionExpressionId` — group by road and direction
- `MinimumLength` / `MaximumLength` — project length bounds
- `CanSkipExpressionId` — can skip untreated sections to maintain project continuity
- `CanSwitchTreatmentExpression` — can change treatment within a project
- `CanSwitchYearExpression` — can shift year to combine with adjacent
- `UseEndOfRoadRule` — extend to road ends
- `ShouldCreateDrps` — create Detailed Rehabilitation Plans
- `IsJointToLast` — join to the previous dFrag result
- `KeepExistingSections` — preserve existing section boundaries

The system can consolidate across scenarios (`SourceBudgetScenario` → `TargetBudgetScenario`) and perspectives (`TargetPerspective`).

### 12.2 Data Import / Export

#### Data Import (`DataImport`)
Import external data into inventory tables:
- Source file/table mapping
- Column mappings (`DataImportColumnMapping`) with optional transformation expressions
- Options: import elements, attributes, attribute values, remove all existing

#### Strategy Export (`ExportStrategiesRequest`)
Export analysis results:
- Per budget scenario
- Variable selection (`ExportStrategiesRequestVariable`)
- Options: minimum information, selected strategies only, after-treatment values only

### 12.3 Queries and Transformations

| Entity | Purpose |
|--------|---------|
| `TableQuery` | Query data from an entity with filters |
| `NetworkQuery` | Query with road-based filtering |
| `SCDQuery` | Section Change Detection queries |
| `TimeDependentQuery` | Time-series data queries |
| `CrossTabQuery` | Pivot table / matrix queries with statistical transformations |
| `CrossTabTransformation` | Cross-tab data transformations |
| `FormulaTransformation` | Apply formula expressions to transform attribute values |
| `TableTransformation` | Copy/transform data between tables with statistical options (mean, SD multiplier) |

### 12.4 GIS and Mapping

#### GIS Integration (`GisIntegration`)
Full ArcGIS integration with:
- Feature service connection (REST endpoints for CRUD operations on routes)
- Cartographic realignment, route creation, calibration
- Coordinate system transformation (`ConvertFrom`, `ConvertTo`, SRID)
- Import geometry and attribute mapping (`GisIntegrationMapping`)
- Support for CSV, shapefiles, and ArcGIS feature classes

#### Map Layers
Multiple map layer types:
- `TableMapLayer` — basic entity visualization
- `AttributeTableCodeMapLayer` — color by coded attribute values
- `AttributeRangeMapLayer` — color by numeric ranges
- `UniqueValuesMapLayer` — color by unique values
- `ConstructionProgramMapLayer` — treatment program by year with treatment colors
- `WebMapServiceLayer` / `WebFeatureServiceLayer` — external WMS/WFS
- `ArcGISLayer` — ArcGIS REST service layers

#### Strip Maps (`StripMapConfiguration`)
Linear visualization of road data:
- Table layers, historic layers, lane layers
- Attribute graph layers (condition trends)
- Attribute value layers
- Construction program layers

#### Spatial Import (`SpatialImport`)
Import geometry from external sources with road-name, from/to, lat/lon, or geometry fields.

### 12.5 Decision Trees

`DecisionTree` — JSON-based rule sets (`JsonRules` property) that encode complex branching logic for treatment selection or other decisions. Linked to an entity and expression for evaluation context.

### 12.6 Workflows and Batch Operations

#### Workflow
XOML-defined workflow definitions that automate multi-step processes. Used as after-execute hooks on analysis sets, triggers on status changes, and automation of queries/transformations.

#### BatchOperation / BatchOperationItem
Chains multiple operations (analyses, queries, transformations, imports, exports) into a single batch:
- `ItemType` — `ExecutionType` enum
- `Order` — execution sequence
- Operations execute sequentially via the `ExecutionRequest` service

### 12.7 Execution Service

#### `ExecutionRequest`
Manages async execution of analyses and operations:
- `ExecutionType` — what kind of operation
- `ExecutionStatus` — queued, running, completed, failed
- `Progress` (0-100%)
- `ScheduledExecutionTime`, `ActualStartTime`, `CompletionTime`
- `Frequency` — one-time or recurring
- `PredecessorID` — chain dependencies between requests
- `LogLevel` — diagnostic detail level

#### `ServiceStatus`
Monitors the execution service:
- `IsExecuting`, `LastCheckIn`, `Version`
- Currently executing request

### 12.8 Access Control

Every major entity has a corresponding `*ACL` entity (e.g., `AnalysisSetACL`, `BudgetScenarioACL`, `TreatmentACL`, etc.) providing fine-grained access control:
- `AccessorUid` — user or role identifier
- `Permission` — permission level (integer)
- `IsGrant` — grant or deny
- `AclObjectId` — target entity instance
- `AclType` — permission type

Additionally, entities have role-based access at the type level:
- `SelectRole` — who can read
- `UpdateRole` — who can modify
- `DeleteRole` — who can delete

### 12.9 Reporting

| Report Type | Technology |
|-------------|-----------|
| `TelerikReport` | Embedded Telerik report definitions (binary `ReportDefinition`) |
| `CustomReport` | URL-based or embedded reports (ReportType enum) |
| Power BI | `Microsoft.PowerBI.Api.Models.Report` — embedded Power BI with workspace integration |
| `BIConfiguration` | Business intelligence dashboard configuration |

### 12.10 Audit Logging

`AuditLog` tracks all changes:
- `UserId`, `ModifiedBy` — who
- `ModifiedOn` — when
- `Action` — `AuditAction` enum (create, update, delete)
- `ObjectId` — what was changed
- `ChangeValueJson` — JSON diff of changes

### 12.11 Location Referencing

The `LocationReference` system provides precise linear referencing:
- `NetworkId`, `ElementId` — route/section identity
- `From`, `To` — milepost measures
- `Location` (Geometry, SRID=0) — spatial geometry
- `LrmFromName/Offset`, `LrmToName/Offset` — LRM (Linear Reference Method) coordinates
- Extended type `LocationReferenceWithIntersectionAndClosest` adds intersection and closest-point calculations

### 12.12 Cross-Asset Optimization

`CrossAsset` and `CrossAssetScenarios` support optimization across multiple asset classes (e.g., pavement + bridges + signs):
- Each cross-asset links to multiple `BudgetScenario` instances across different analysis sets
- `AdditionalFunding` — extra funds available
- Budget allocation across asset classes optimized jointly

---

## 13. Complete Treatment Trigger Table

The following table contains all 25 trigger rules from the `2025_12_17_Analysis_Lookup_Triggers.xlsx` file:

| Key | Treatment | Branch | CSI Range | ECI Range | JCI Range | PSI Range | RDI Range | SCI Range |
|-----|-----------|--------|-----------|-----------|-----------|-----------|-----------|-----------|
| CAPE_SEAL_1 | Cape Seal | 1 | 0-5 | 3-4.5 | 0-5 | 3-5 | 3.5-5 | 3-4.5 |
| CHIP_SEAL_1 | Chip Seal | 1 | 0-5 | 2.5-4.5 | 0-5 | 0-5 | 3.5-5 | 3.5-4.5 |
| CRACK_SEAL_1 | Crack Seal | 1 | 4.3-4.5 | 0-5 | 0-5 | 0-5 | 0-5 | 0-5 |
| MAJOR_CPR_DG_1 | Major CPR Diamond Grind | 1 | 1-5 | 0-5 | 1-5 | 1-2.5 | 0-5 | 0-5 |
| MAJOR_CPR_DG_2 | Major CPR Diamond Grind | 2 | 1-5 | 0-5 | 1-5 | 1-5 | 0-5 | 0-5 |
| MAJOR_CPR_DG_3 | Major CPR Diamond Grind | 3 | 1-5 | 0-5 | 1-3 | 1-5 | 0-5 | 0-5 |
| MICRO_1 | Micro Surfacing | 1 | 0-5 | 3.5-4.9 | 0-5 | 3.6-4.5 | 3.5-4.9 | 3.5-4.9 |
| MINOR_CPR_DG_1 | Minor CPR Diamond Grind | 1 | 2.5-5 | 0-5 | 2.5-5 | 2.5-3 | 0-5 | 0-5 |
| MINOR_CPR_DG_2 | Minor CPR Diamond Grind | 2 | 2.5-5 | 0-5 | 2.5-3.5 | 2.5-5 | 0-5 | 0-5 |
| MINOR_CPR_DG_3 | Minor CPR Diamond Grind | 3 | 2.5-3.5 | 0-5 | 2.5-5 | 2.5-5 | 0-5 | 0-5 |
| PRESERVATION_1 | Preservation | 1 | 3.5-4 | 0-5 | 0-5 | 0-5 | 0-5 | 0-5 |
| RECON_1 | Reconstruction | 1 | 0-5 | 0-5 | 0-5 | 0-1 | 0-5 | 0-5 |
| RECON_2 | Reconstruction | 2 | 0-5 | 0-5 | 0-5 | 0-5 | 0-5 | 0-1 |
| RECON_3 | Reconstruction | 3 | 0-5 | 0-1 | 0-5 | 0-5 | 0-5 | 0-5 |
| RECON_4 | Reconstruction | 4 | 0-5 | 0-5 | 0-1 | 0-5 | 0-5 | 0-5 |
| RECON_5 | Reconstruction | 5 | 0-1 | 0-5 | 0-5 | 0-5 | 0-5 | 0-5 |
| SAW_SEAL_1 | Saw and Seal Joints | 1 | 3-4 | 0-5 | 3-4 | 0-5 | 0-5 | 0-5 |
| THICK_OVL_1 | Thick Overlay | 1 | -1-5 | -1-5 | -1-5 | 1-3.5 | -1-5 | -1-3 |
| THICK_OVL_2 | Thick Overlay | 2 | 0-5 | 1-5 | 0-5 | 1-5 | 0-5 | 1-2.55 |
| THICK_OVL_3 | Thick Overlay | 3 | 0-5 | 1-2.55 | 0-5 | 1-5 | 0-5 | 1-5 |
| THIN_OVL_1 | Thin Overlay | 1 | 0-5 | 2.5-4 | 0-5 | 2-3.5 | 2.5-5 | 2.5-5 |
| THIN_OVL_2 | Thin Overlay | 2 | 0-5 | 2.5-3.5 | 0-5 | 2.8-5 | 2.5-5 | 2.5-3.5 |
| THIN_OVL_3 | Thin Overlay | 3 | 0-5 | 2.5-3.5 | 0-5 | 2.8-5 | 2.5-5 | 2.5-5 |
| THIN_OVL_4 | Thin Overlay | 4 | 0-5 | 2.5-3.5 | 0-5 | 2.8-5 | 2.5-4 | 2.5-5 |
| ULTRA_THIN_1 | Ultra Thin Overlay | 1 | 0-5 | 3.5-4.5 | 0-5 | 3.5-5 | 4-5 | 3.5-4.5 |

---

## 14. Entity Reference

### Complete Entity Listing from schema.xml

#### Core Analysis Entities
| Entity | Purpose |
|--------|---------|
| `AnalysisSet` | Central analysis configuration |
| `AnalysisSetTreatment` | Treatment inclusion in analysis |
| `AnalysisSetPerformanceIndex` | Variable inclusion in analysis |
| `AnalysisVariable` | Performance variable definition |
| `AnalysisVariableCurve` | Deterioration curve |
| `Treatment` | M&R treatment definition |
| `TreatmentCost` | Financial/economic cost rules |
| `TreatmentReset` | Condition improvement rules |
| `TreatmentSubsequent` | Follow-up treatment chain |
| `TreatmentAncillary` | Companion treatments |
| `BudgetScenario` | Optimization scenario |
| `BudgetCategory` | Funding source category |
| `AnalysisSetBudgetScenario` | Annual budget allocations |
| `ConditionCategory` | Condition rating bins |

#### Data Management
| Entity | Purpose |
|--------|---------|
| `dTIMSEntity` | Inventory/data table |
| `dTIMSAttribute` | Column definition |
| `dTIMSAttributeType` | Data type definition |
| `AttributeTableCode` | Coded value lookup |
| `EntityRelation` | Table relationships |
| `Dataview` | Data view configuration |
| `DataviewColumn` | View column definition |
| `DataImport` | Import configuration |
| `DataImportColumnMapping` | Column mapping for imports |
| `DataImportError` | Import error log |

#### Expressions
| Entity | Purpose |
|--------|---------|
| `dTIMSExpression` | Database-time expression |
| `RuntimeExpression` | Analysis-time expression |
| `dFragExpression` | Defragmentation expression |
| `ExpressionFunction` | Expression function catalog |

#### Optimization
| Entity | Purpose |
|--------|---------|
| `CrossAsset` | Multi-asset optimization |
| `CrossAssetScenarios` | Cross-asset scenario budgets |
| `SAM` | Strategic Asset Management |
| `SAMScenarios` | SAM scenario configuration |
| `SAMBudgetScenario` | SAM budget link |

#### Project Management
| Entity | Purpose |
|--------|---------|
| `dFrag` | Project defragmentation |
| `DecisionTree` | JSON rule-based decisions |
| `BatchOperation` | Batch job definition |
| `BatchOperationItem` | Batch job step |
| `ExecutionRequest` | Async execution request |
| `RequestBatch` | Batch request group |
| `ServiceStatus` | Execution service health |

#### Queries & Transformations
| Entity | Purpose |
|--------|---------|
| `TableQuery` | Table data query |
| `NetworkQuery` | Road-filtered query |
| `SCDQuery` | Section change detection |
| `TimeDependentQuery` | Time-series query |
| `CrossTabQuery` / `CrossTabQueryCell` | Pivot queries |
| `CrossTabTransformation` / `CrossTabTransformationCell` | Pivot transforms |
| `FormulaTransformation` | Formula-based transforms |
| `TableTransformation` | Table-to-table transforms |

#### GIS & Mapping
| Entity | Purpose |
|--------|---------|
| `GisIntegration` | ArcGIS connection |
| `GisIntegrationMapping` | Field mapping |
| `SpatialImport` / `SpatialImportMapping` | Geometry import |
| `MapConfiguration` | Map layer configuration |
| `TableMapLayer` | Basic map layer |
| `AttributeTableCodeMapLayer` | Coded value map |
| `AttributeRangeMapLayer` / `AttributeRangeMapLayerRange` | Range-colored map |
| `UniqueValuesMapLayer` / `UniqueValuesMapLayerValue` | Unique value map |
| `ConstructionProgramMapLayer` / `...Treatment` | Treatment program map |
| `ConstructionProgramStripMapLayer` / `...Treatment` | Strip map program |
| `WebMapServiceLayer` | WMS layer |
| `WebFeatureServiceLayer` | WFS layer |
| `ArcGISLayer` | ArcGIS REST layer |
| `StripMapConfiguration` | Strip map setup |
| `StripMapTableLayer` / `HistoricTableLayer` / `LaneTableLayer` | Strip map layers |
| `StripMapAttributeLayer` / `GraphLayer` / `ValueLayer` | Strip map attributes |

#### Location & Geometry
| Entity | Purpose |
|--------|---------|
| `LocationReference` | Linear reference result |
| `LocationReferenceWithIntersectionAndClosest` | Extended location with intersection |
| `LocationReferenceUpdateRequest` / `UpdateResult` | Location update operations |

#### Reporting
| Entity | Purpose |
|--------|---------|
| `TelerikReport` | Embedded report definition |
| `CustomReport` | Custom/external report |
| `BIConfiguration` | BI dashboard config |
| Power BI `Report` | Embedded Power BI |

#### User & Security
| Entity | Purpose |
|--------|---------|
| `UserOption` | Per-user settings |
| `AuditLog` | Change audit trail |
| `*ACL` entities (20+) | Fine-grained access control per entity type |

#### Export & Miscellaneous
| Entity | Purpose |
|--------|---------|
| `ExportStrategiesRequest` / `...Variable` | Strategy export config |
| `AssetExportConfiguration` / `AssetExportRole` | Asset data export |
| `DuplicateTableConfiguration` / `DuplicateTableRole` | Table duplication |
| `Workflow` | XOML workflow definition |
| `StoredProcedure` | Custom SQL procedures |
| `Note` | User notes |

#### Analysis Result Types (ComplexTypes)
| Type | Purpose |
|------|---------|
| `StrategyData` | Per-section strategy results with PVBenefits, PVCost, IBC |
| `StrategyTreatments` | Year-by-year treatment details per strategy |
| `StrategyChartData` | Chart data: current, do-nothing, original, selected |
| `VariableData` | Variable values per strategy |
| `ChartYearData` | Condition trend per scenario per year |
| `ChartDistributionAndTreatmentData` | Distribution charts |
| `ProgramCost` | Cost per year |
| `GridMeasure` | Year/measure grid data |
| `BudgetData` | Budget utilization |
| `ConstructionProgram` | Treatment/section/year/cost program |
| `SectionConstructionProgram` | Section-based (From/To) program |
| `PointConstructionProgram` | Point-based (At) program |
| `StrategyExport` | Exported strategy summary |
| `AnalysisSetTreatmentStatistic` | Treatment generation statistics |
| `AnalysisSetStatistics` | Category-level statistics |

---

## Sources

- [NDDOT Pavement Management Program](https://www.dot.nd.gov/construction-and-planning/transportation-plans-programs/pavement-management-program)
- [NDDOT dTIMS Description (PDF)](https://www.dot.nd.gov/sites/www/files/documents/construction-and-planning/dTIMS-Description.pdf)
- [Deighton — dTIMS for Pavement Management](https://www.deighton.com/dtims-blog/dtims-for-pavement-management)
- [Pavement Analysis — DTIMS](https://www.pavementanalysis.com/dtims)
- [UDOT Pavement Management — dTIMS](https://sites.google.com/utah.gov/pavementmanagement/home/dtims)
- [AASHTO TAM Guide — Use of IBC](https://www.tamguide.com/practice-example/4-1-3-3-1-use-of-incremental-benefit-cost-to-demonstrate-long-term-benefits/)
- [Deighton — IBC Budget Scenarios Help](https://demo.deighton.com/whitby/ba/help/Content/dTIMS/dt_budget_scen_ibc.htm)
- [PIARC Asset Management Case Study 2](https://road-asset.piarc.org/en/data-and-modeling-lifecycle-planning-case-studies/case-study-2)
- [FHWA Pavement Management Primer](https://www.fhwa.dot.gov/pavement/pavementpolicy/linkages/pmprimer.pdf)
