# From Raw Measurements to Condition Indices: How WVDOT PMS Bridges the Gap

> How IRI, rutting, and cracking measurements become the PSI, RDI, SCI, and CCI condition indices — and how those relate to the dTIMS trigger indices (CSI, ECI, JCI, PSI, RDI, SCI).

---

## Table of Contents

1. [Overview](#1-overview)
2. [Raw Measurements in the Database](#2-raw-measurements-in-the-database)
3. [WVDOT Condition Indices — Exact Formulas](#3-wvdot-condition-indices--exact-formulas)
4. [Composite Condition Index (CCI)](#4-composite-condition-index-cci)
5. [The Local Engine Trigger System](#5-the-local-engine-trigger-system)
6. [The dTIMS Trigger System](#6-the-dtims-trigger-system)
7. [Mapping Between the Two Systems](#7-mapping-between-the-two-systems)
8. [Data Flow Diagram](#8-data-flow-diagram)
9. [Verification Against Live Data](#9-verification-against-live-data)
10. [Sources](#10-sources)

---

## 1. Overview

There are **two parallel trigger systems** in this PMS:

| System | Trigger Variables | Index Scale | Source |
|--------|-------------------|-------------|--------|
| **Local Engine** (`treatment_triggers` table) | Raw measurements: `iri_current`, `rut_current`, `crack_current`, `aadt` | IRI: inches/mile, Rut: inches, Crack: %, AADT: count | Custom Python engine |
| **dTIMS** (`Analysis_Lookup_Triggers.xlsx`) | Condition indices: CSI, ECI, JCI, PSI, RDI, SCI | All 0-5 (5 = best) | Deighton dTIMS application |

The **bridge** between raw measurements and condition indices is a set of conversion formulas. Three of these (PSI, RDI, SCI) are already computed and stored in the `condition_history` table, imported directly from WVDOT's condition survey CSV files.

---

## 2. Raw Measurements in the Database

### `analysis_segments` table (274,273 rows)

The primary analysis table stores **current raw condition values** per 0.1-mile segment:

| Column | Unit | Description | Example Values |
|--------|------|-------------|----------------|
| `current_iri` | inches/mile | International Roughness Index — ride quality/smoothness | 67-400+ |
| `current_rut` | inches | Mean rut depth — permanent deformation in wheelpaths | 0.01-1.0+ |
| `current_crack` | % area | Percentage of pavement surface area with cracking | 0-100 |
| `current_faulting` | inches | Mean joint faulting (concrete pavements only) | 0.01-0.50+ |
| `aadt` | vehicles/day | Annual Average Daily Traffic | 100-100,000+ |
| `surface_type` | code | Pavement type: ASP, JCP, CRC, CRCP, JOINTED | — |

### `condition_history` table (403,530 rows)

Stores **yearly condition surveys** with both raw measurements AND pre-computed indices:

| Column | Description |
|--------|-------------|
| `iri_mean`, `iri_max` | IRI measurements (inches/mile) |
| `rut_mean`, `rut_max` | Rut depth measurements (inches) |
| `crack_percent` | Total cracking percentage |
| `fhwa_crack_percent` | FHWA-definition cracking percentage |
| `faulting` | Joint faulting (inches) |
| **`psi`** | Present Serviceability Index (0-5) — **derived from IRI** |
| **`rdi`** | Rut Depth Index (0-5) — **derived from rut depth** |
| **`sci`** | Structural Cracking Index (0-5) — **derived from cracking survey** |
| **`cci`** | Composite Condition Index (0-5) — **derived from PSI, RDI, SCI** |

These indices arrive **pre-computed** in the condition survey CSV files (columns `PSI`, `RDI`, `SCI`, `CCI`) and are loaded by `db/load_condition_history.py`.

---

## 3. WVDOT Condition Indices — Exact Formulas

### 3.1 PSI — Present Serviceability Index

**Formula (confirmed against 398,324 database records, avg error = 0.0025):**

```
PSI = 5 * exp(-0.0041 * IRI)
```

| Parameter | Value |
|-----------|-------|
| **Input** | IRI in inches/mile |
| **Output** | 0 to 5 (5 = excellent ride quality) |
| **Coefficient** | -0.0041 (exponential decay rate) |
| **Avg Error vs DB** | 0.0025 (max 0.0063) |

**Interpretation:**

| IRI (in/mi) | PSI | Condition |
|-------------|-----|-----------|
| < 60 | > 3.9 | Very Good |
| 60-95 | 3.4-3.9 | Good |
| 95-170 | 2.5-3.4 | Fair |
| 170-270 | 1.7-2.5 | Poor |
| > 270 | < 1.7 | Very Poor |

**Background:** PSI was originally developed at the AASHO Road Test (1956-1960) as a subjective 0-5 panel rating. WVDOT uses an IRI-based conversion calibrated for West Virginia conditions. A Penn State / R3UTC research project (2022) calibrated the WVDOH IRI-based PSI equation.

### 3.2 RDI — Rut Depth Index

**Formula (confirmed against database records, avg error = 0.013):**

```
RDI = MAX( MIN( 5 - 6.65 * rut^1.41,  5 ),  0 )
```

| Parameter | Value |
|-----------|-------|
| **Input** | Mean rut depth in inches |
| **Output** | 0 to 5 (5 = no rutting) |
| **Coefficient a** | 6.65 |
| **Exponent b** | 1.41 |
| **Avg Error vs DB** | 0.013 (max 0.046) |

This is a power-law deduction model: as rut depth increases, RDI drops non-linearly. The formula was found referenced in the [WVDOH Pavement Data Dictionary](https://gis.transportation.wv.gov/ftp/TMA/HPMSManualsAndReferences/Data%20Dictionary(Pavement).pdf).

**Interpretation:**

| Rut Depth (in) | RDI | Condition |
|-----------------|-----|-----------|
| < 0.05 | > 4.9 | Excellent |
| 0.05-0.15 | 4.5-4.9 | Good |
| 0.15-0.30 | 3.8-4.5 | Fair |
| 0.30-0.50 | 2.8-3.8 | Poor |
| > 0.50 | < 2.8 | Very Poor |
| > 0.68 | 0.0 | Failed (capped at 0) |

### 3.3 SCI — Structural Cracking Index

**Formula: Pre-computed from detailed distress survey; NOT a simple function of `crack_percent`.**

The SCI values in the database show **high variance** at any given `crack_percent` value. For example, at `crack_percent = 5.0`, observed SCI values range from 0.43 to 2.80. This means SCI incorporates **more granular cracking data** than just the total percentage:

- Alligator (fatigue) cracking extent and severity
- Longitudinal cracking extent and severity
- Transverse cracking
- Block cracking
- Severity weighting factors for each type

The SCI equation was calibrated by WVDOH by analyzing historical alligator and longitudinal crack data collected from 1998 to 2021 (per the Penn State R3UTC calibration project).

| SCI Range | Condition |
|-----------|-----------|
| > 4.0 | Good (minimal cracking) |
| 3.0-4.0 | Fair |
| 2.0-3.0 | Poor |
| < 2.0 | Very Poor / Structural failure |

**Key point:** SCI comes pre-computed from the condition survey vendor's data processing. It cannot be reproduced from `crack_percent` alone — the vendor's raw distress data (by type and severity) is required.

---

## 4. Composite Condition Index (CCI)

**Formula (confirmed against 312,404 records at 94.3% exact match):**

```
CCI = MIN(PSI, RDI, SCI)
```

When not all sub-indices are available:
- If only PSI available: `CCI = PSI` (97.2% match on 11,595 records)
- If PSI + RDI available (no SCI): `CCI = MIN(PSI, RDI)` (68.6% match — some older data appears to use `CCI = PSI` as fallback)
- Outlier cases (~5.7%) appear to be data quality issues or version differences in the computation

**Interpretation:** CCI represents the **worst-performing aspect** of the pavement. A section with excellent ride (PSI=4.5) but severe rutting (RDI=2.0) gets CCI=2.0. This "weakest link" approach ensures no critical deficiency is masked.

| CCI Range | Condition | Action Needed |
|-----------|-----------|---------------|
| 4.0-5.0 | Good | Routine monitoring |
| 3.0-4.0 | Fair | Preventive maintenance |
| 2.0-3.0 | Poor | Rehabilitation |
| 0.0-2.0 | Very Poor | Major rehab or reconstruction |

---

## 5. The Local Engine Trigger System

The custom Python engine (`engine/treatments/triggers.py`) uses **raw measurements directly** rather than converted indices. Triggers are stored in the `treatment_triggers` PostgreSQL table.

### 5.1 Active Treatments (from `treatments` table)

| treatment_id | Treatment | Cost/Lane-Mile | Service Life | Budget Category |
|-------------|-----------|----------------|--------------|-----------------|
| CRACK-SEAL | Crack Sealing | $18,000 | 3 yr | preservation |
| MICRO-SURF | Microsurfacing | $42,000 | 5 yr | preservation |
| THIN-OVLY | Thin Overlay (1.5") | $85,000 | 7 yr | preservation |
| MILL-OL-2 | Mill & Overlay (2") | $145,000 | 11 yr | — |
| MILL-OL-3 | Mill & Overlay (3") | $195,000 | 14 yr | — |
| FDR | Full-Depth Reclamation | $280,000 | 17 yr | rehabilitation |
| RECONSTRUCT | Reconstruction | $450,000 | 22 yr | reconstruction |

### 5.2 Trigger Logic

Triggers use a **multi-dimensional feasibility envelope** with two types:

- **Eligibility triggers**: The segment must fall WITHIN the specified window. Multiple trigger groups exist (OR logic between groups, AND logic within a group).
- **Veto triggers**: If ANY veto condition is met, the treatment is disqualified regardless of eligibility.

### 5.3 Complete Trigger Rules

**CRACK-SEAL** — Crack Sealing
```
Eligibility Group 1: IRI [95, 120) AND crack [5, 15) AND rut < 0.25
Veto: IRI >= 120 OR crack >= 20 OR rut >= 0.25
```

**MICRO-SURF** — Microsurfacing
```
Group 1: IRI [95, 130] AND crack < 20
Group 2: IRI [95, 130] AND rut [0.15, 0.35]
Group 3: crack < 20 AND rut [0.15, 0.35]
```

**THIN-OVLY** — Thin Overlay (1.5")
```
Group 1: IRI [120, 150] AND crack [15, 30]
Group 2: IRI [120, 150] AND rut [0.25, 0.40]
Group 3: crack [15, 30] AND rut [0.25, 0.40]
Veto: IRI > 160 OR crack >= 40 OR rut >= 0.50
```

**MILL-OL-2** — Mill & Overlay (2")
```
Group 1: IRI [140, 180] AND crack [20, 40] AND AADT > 2000
Group 2: IRI [140, 180] AND rut [0.30, 0.50] AND AADT > 2000
Group 3: crack [20, 40] AND rut [0.30, 0.50] AND AADT > 2000
```

**MILL-OL-3** — Mill & Overlay (3")
```
Group 1: IRI [160, 200] AND crack [30, 50] AND AADT > 5000
Group 2: IRI [160, 200] AND rut [0.40, 0.60] AND AADT > 5000
Group 3: crack [30, 50] AND rut [0.40, 0.60] AND AADT > 5000
```

**FDR** — Full-Depth Reclamation
```
Group 1: IRI >= 180 AND rut >= 0.50 AND crack >= 40
```

**RECONSTRUCT** — Reconstruction
```
Group 1: IRI >= 200 AND rut >= 0.60
Group 2: IRI >= 200 AND crack >= 50
Group 3: rut >= 0.60 AND crack >= 50
```

### 5.4 Treatment Resets

When a treatment is applied, condition metrics are reset:

| Treatment | IRI Reset | Rut Reset | Crack Reset |
|-----------|-----------|-----------|-------------|
| CRACK-SEAL | No change | No change | -80% (relative) |
| MICRO-SURF | -15 (relative) | 0.05 (absolute) | -60% (relative) |
| THIN-OVLY | -30 (relative) | 0.08 (absolute) | -90% (relative) |
| MILL-OL-2 | 75 (absolute) | 0.05 (absolute) | 2% (absolute) |
| MILL-OL-3 | 70 (absolute) | 0.03 (absolute) | 1% (absolute) |
| FDR | 40 (absolute) | 0.02 (absolute) | 0% (absolute) |
| RECONSTRUCT | 40 (absolute) | 0.00 (absolute) | 0% (absolute) |

---

## 6. The dTIMS Trigger System

The `2025_12_17_Analysis_Lookup_Triggers.xlsx` file defines triggers used in the **Deighton dTIMS application** (the commercial software). These triggers use **six condition indices** on a 0-5 scale.

### 6.1 dTIMS Indices

| Index | Full Name | Derived From |
|-------|-----------|-------------|
| **PSI** | Present Serviceability Index | IRI (ride quality) |
| **RDI** | Rut Depth Index | Rut depth |
| **SCI** | Structural Cracking Index | Cracking distress survey |
| **CSI** | Cracking Severity Index | Cracking severity data |
| **ECI** | Edge Condition Index | Edge deterioration |
| **JCI** | Joint Condition Index | Joint faulting/spalling (concrete) |

### 6.2 Key Difference

The dTIMS system uses **six** indices while the WVDOT database stores only **four** (PSI, RDI, SCI, CCI). The additional indices (CSI, ECI, JCI) are:
- **CSI**: Likely a cracking severity measure separate from SCI — may distinguish between structural (alligator) cracking and surface cracking severity
- **ECI**: Edge condition — may be derived from edge cracking and shoulder drop-off measurements not currently in the database
- **JCI**: Joint condition — likely derived from faulting, joint spalling, and slab cracking for concrete pavements

These additional indices may be available in the full dTIMS deployment but are not currently loaded into the PostgreSQL database used by the local engine.

---

## 7. Mapping Between the Two Systems

### 7.1 Raw Measurement → Index Conversion

```
┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────┐
│   RAW MEASUREMENTS   │     │   WVDOT INDICES       │     │  dTIMS INDICES   │
│   (in database)      │────►│   (in condition_      │────►│  (in dTIMS app)  │
│                      │     │    history)            │     │                  │
├──────────────────────┤     ├──────────────────────┤     ├──────────────────┤
│ IRI (inches/mile)    │──── │ PSI = 5*e^(-0.0041   │────►│ PSI (same)       │
│                      │     │        * IRI)          │     │                  │
│ Rut depth (inches)   │──── │ RDI = max(min(5-6.65  │────►│ RDI (same)       │
│                      │     │       *rut^1.41,5),0)  │     │                  │
│ Cracking (% + type   │──── │ SCI = f(distress       │────►│ SCI (same)       │
│  + severity)         │     │       survey data)      │     │                  │
│                      │     │                        │     │ CSI = ?           │
│ Faulting (inches)    │     │ CCI = min(PSI,RDI,SCI)│     │ ECI = ?           │
│ Edge condition       │     │                        │     │ JCI = ?           │
│ Joint condition      │     │                        │     │                  │
└──────────────────────┘     └──────────────────────┘     └──────────────────┘
```

### 7.2 Approximate Index-to-Raw Equivalents

By inverting the PSI and RDI formulas, we can map dTIMS trigger thresholds back to raw measurement values:

**PSI → IRI** (inverting `PSI = 5 * exp(-0.0041 * IRI)`):
```
IRI = -ln(PSI / 5) / 0.0041
```

| PSI Threshold | Equivalent IRI (in/mi) |
|---------------|----------------------|
| 5.0 | 0 (new pavement) |
| 4.5 | 26 |
| 4.0 | 54 |
| 3.5 | 87 |
| 3.0 | 124 |
| 2.5 | 168 |
| 2.0 | 223 |
| 1.5 | 293 |
| 1.0 | 392 |

**RDI → Rut Depth** (inverting `RDI = 5 - 6.65 * rut^1.41`):
```
rut = ((5 - RDI) / 6.65) ^ (1/1.41)
```

| RDI Threshold | Equivalent Rut (inches) |
|---------------|------------------------|
| 5.0 | 0.000 |
| 4.5 | 0.056 |
| 4.0 | 0.117 |
| 3.5 | 0.183 |
| 3.0 | 0.253 |
| 2.5 | 0.328 |
| 2.0 | 0.409 |
| 1.0 | 0.598 |

### 7.3 Comparing Trigger Thresholds

Using the conversion tables above, we can roughly compare a dTIMS trigger to a local engine trigger:

**Example: dTIMS Thin Overlay Branch 1**
- PSI [2, 3.5] → IRI [87, 223]
- RDI [2.5, 5] → Rut [0, 0.328]
- SCI [2.5, 5] → moderate-to-good cracking

**Local Engine Thin Overlay**
- IRI [120, 150]
- Crack [15%, 30%]
- Rut [0.25, 0.40]
- Veto: IRI > 160 OR crack >= 40% OR rut >= 0.50

The local engine operates on a **narrower, more precisely tuned** window than dTIMS, with explicit veto conditions.

---

## 8. Data Flow Diagram

```
╔══════════════════════════════════════════════════════════════════╗
║                    FIELD DATA COLLECTION                         ║
║                                                                  ║
║  Automated survey vehicles collect:                              ║
║  • Longitudinal profile → IRI (in/mi)                           ║
║  • Transverse profile → Rut depth (inches)                      ║
║  • Pavement images → Cracking (% by type & severity)            ║
║  • Joint measurements → Faulting (inches, concrete only)        ║
╚══════════════════════════════════════════════════════════════════╝
                              │
                              ▼
╔══════════════════════════════════════════════════════════════════╗
║              CONDITION SURVEY CSV FILE                            ║
║                                                                  ║
║  Columns from vendor:                                            ║
║  ROUTEID, BEG_MP, IRI_MEAN, IRI_MAX, RUT_MEAN, RUT_MAX,        ║
║  PERCENT_CRACKING, HPMS_Cracking_Percent, FAULT_AVG,            ║
║  CCI, PSI, RDI, SCI  ← vendor pre-computes these indices        ║
╚══════════════════════════════════════════════════════════════════╝
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
╔═══════════════════════╗       ╔═══════════════════════╗
║  db/load_condition_   ║       ║  db/load_segments.py  ║
║  history.py           ║       ║                       ║
║                       ║       ║  Creates segments and ║
║  Loads raw + indices  ║       ║  analysis_segments    ║
║  into condition_      ║       ║  with current_iri,    ║
║  history table        ║       ║  current_rut, etc.    ║
╚═══════════════════════╝       ╚═══════════════════════╝
              │                               │
              ▼                               ▼
╔═══════════════════════╗       ╔═══════════════════════╗
║  condition_history    ║       ║  analysis_segments    ║
║  ─────────────────    ║       ║  ─────────────────    ║
║  iri_mean, rut_mean   ║       ║  current_iri          ║
║  crack_percent        ║       ║  current_rut          ║
║  faulting             ║       ║  current_crack        ║
║  PSI, RDI, SCI, CCI  ║       ║  current_faulting     ║
║  (pre-computed)       ║       ║  aadt, surface_type   ║
╚═══════════════════════╝       ╚═══════════════════════╝
              │                               │
              │                               ▼
              │               ╔═══════════════════════════════════╗
              │               ║  LOCAL ENGINE TRIGGERS              ║
              │               ║  (engine/treatments/triggers.py)   ║
              │               ║                                    ║
              │               ║  Uses RAW values directly:         ║
              │               ║  iri_current, rut_current,         ║
              │               ║  crack_current, aadt               ║
              │               ║                                    ║
              │               ║  Eligibility + Veto logic          ║
              │               ╚═══════════════════════════════════╝
              │
              ▼
╔═══════════════════════════════════════════╗
║  dTIMS APPLICATION (Deighton software)    ║
║                                           ║
║  Uses INDICES on 0-5 scale:               ║
║  PSI, RDI, SCI, CSI, ECI, JCI            ║
║                                           ║
║  Triggers from Analysis_Lookup_Triggers   ║
║  .xlsx — 25 rules across 13 treatments   ║
╚═══════════════════════════════════════════╝
```

---

## 9. Verification Against Live Data

### 9.1 PSI Formula Verification

Tested `PSI = 5 * exp(-0.0041 * IRI)` against 398,324 records in `condition_history`:

| Metric | Value |
|--------|-------|
| Records tested | 398,324 |
| Average absolute error | **0.0025** |
| Maximum absolute error | **0.0063** |
| Conclusion | **Formula confirmed** |

### 9.2 RDI Formula Verification

Tested `RDI = MAX(MIN(5 - 6.65 * rut^1.41, 5), 0)` against records with non-zero rut:

| Metric | Value |
|--------|-------|
| Average absolute error | **0.013** |
| Maximum absolute error | **0.046** |
| Conclusion | **Formula confirmed** |

### 9.3 CCI Formula Verification

Tested `CCI = MIN(PSI, RDI, SCI)`:

| Scenario | Records | Match Rate |
|----------|---------|-----------|
| All 3 indices available | 331,293 | **94.3%** |
| Only PSI available (RDI & SCI null) | 11,595 | **97.2%** (CCI = PSI) |
| PSI + RDI available (SCI null) | 48,452 | 68.6% (CCI = MIN(PSI, RDI)) |

The ~5.7% non-matches when all 3 indices are available appear to be data quality outliers (e.g., CCI = 0.12 when PSI = 4.20).

### 9.4 SCI — Cannot Be Reproduced

SCI does NOT follow a simple function of `crack_percent`. At `crack_percent = 5.0`, SCI values range from 0.43 to 2.80 across different segments. SCI requires the full **distress-by-type-and-severity** breakdown from the condition survey, which is not stored in the database. It arrives pre-computed from the survey vendor.

---

## 10. Sources

### WVDOT-Specific
- [Calibration of WVDOH IRI-Based PSI and SCI Equations (Penn State R3UTC, 2022)](https://rosap.ntl.bts.gov/view/dot/66523)
- [Calibration Technical Brief (R3UTC)](https://r3utc.psu.edu/research/core-research-projects/ciam-cor-r14/)
- [WVDOH Pavement Data Dictionary (with RDI formula)](https://gis.transportation.wv.gov/ftp/TMA/HPMSManualsAndReferences/Data%20Dictionary(Pavement).pdf)

### General Pavement Engineering
- [Present Serviceability Index — Pavement Interactive](https://pavementinteractive.org/reference-desk/pavement-management/pavement-evaluation/present-serviceability-index/)
- [Present Serviceability Index — Wikipedia](https://en.wikipedia.org/wiki/Present_serviceability_index)
- [FHWA Pavement Condition Rating Systems](https://www.fhwa.dot.gov/pavement/preservation/pubs/perfeval/chap06.cfm)
- [Hall & Munoz (1999): Estimation of PSI from IRI](https://journals.sagepub.com/doi/abs/10.3141/1655-13)
- [AASHO Road Test — Wikipedia](https://en.wikipedia.org/wiki/AASHO_Road_Test)
- [Michigan Tech Pavement Condition Indices Lecture](https://pages.mtu.edu/~balkire/CE5403/Lec12.pdf)

### dTIMS
- [NDDOT dTIMS Description](https://www.dot.nd.gov/sites/www/files/documents/construction-and-planning/dTIMS-Description.pdf)
- [Deighton — dTIMS for Pavement Management](https://www.deighton.com/dtims-blog/dtims-for-pavement-management)
- [UDOT dTIMS Usage](https://sites.google.com/utah.gov/pavementmanagement/home/dtims)

### Codebase Files Referenced
- `engine/condition/deductions.py` — IRI/rut/crack/faulting deduction curves (0-50 scale for PCI)
- `engine/condition/pci.py` — Composite PCI calculation (0-100 scale, separate from PSI)
- `engine/treatments/triggers.py` — Multi-dimensional trigger evaluation
- `engine/db.py` — Database loading (treatments, triggers, resets, segments)
- `db/load_condition_history.py` — CSV-to-database loader for condition survey data
- `api/models/condition_history.py` — SQLAlchemy model showing all stored fields
