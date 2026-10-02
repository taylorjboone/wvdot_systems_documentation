# Import Analysis Segments

> **Superseded for refreshing data:** the data refresh is now one staged command documented in [PMS — Data Pipeline](/docs/PMS_Data_Pipeline). This page is kept for background; where they disagree, the Data Pipeline page is right.


Reference documentation for `scripts/import_pavement_data.py` — the three-phase pipeline that ingests raw vendor pavement survey data, reconflates it onto the stable LRS grid, enriches it with network attributes, and loads the engine-ready `analysis_segments` table.

---

## Overview

The import pipeline transforms raw annual pavement survey CSVs into the `analysis_segments` table that the optimization engine reads. It runs in three phases that can be executed together or individually:

```
Phase 1: Raw CSVs → condition_history + segments (with GPS geocoding)
Phase 2: condition_history → reconflate_normalized (LRS conflation)
Phase 3: reconflate_normalized → analysis_segments (enrichment + load)
```

Each phase drops and recreates its target table, making the script fully idempotent.

---

## Usage

```bash
# Full pipeline (all three phases)
python scripts/import_pavement_data.py /path/to/csvs/

# Individual phases
python scripts/import_pavement_data.py /path/to/csvs/ --phase 1
python scripts/import_pavement_data.py /path/to/csvs/ --phase 2
python scripts/import_pavement_data.py /path/to/csvs/ --phase 3

# Skip LRS reconflation (use raw milepoints directly)
python scripts/import_pavement_data.py /path/to/csvs/ --skip-reconflate
```

### Prerequisites

- PostgreSQL database running with credentials in environment or hardcoded defaults
- `lrsops` CLI tool installed (for phases 2 and 3 LRS operations)
- Raw vendor CSV files (named by year: `2020.csv`, `2021.csv`, etc.)
- Pavement family deterioration parameters loaded (for equivalent age computation in phase 3)

---

## Phase 1: Raw Load

**Input:** Annual vendor CSV files (e.g. `2024.csv`)
**Output:** `condition_history` table, `segments` table

### What It Does

1. Reads each CSV file, extracting the survey year from the filename
2. Parses raw measurements: IRI, rut depth, faulting, cracking percentage, AADT
3. Parses pre-computed condition indices: PSI, RDI, SCI, ECI, JCI, CSI, CCI, NCI
4. Extracts GPS coordinates (start/end lat/lon) from each segment
5. Geocodes GPS coordinates against the WVDOT LRS API (`geometryToMeasure`) to get milepost-based locations when the raw data only has GPS
6. Inserts into `condition_history` (one row per segment per survey year) and `segments` (geometry reference)

### Key Fields Extracted

| CSV Column | DB Column | Description |
|-----------|-----------|-------------|
| `ROUTEID` | `route_id` | Route identifier |
| `BEG_MP` / `END_MP` | `begin_mp` / `end_mp` | Milepost range |
| `IRI_MEAN` | `iri_mean` | International Roughness Index |
| `RUT_MEAN` | `rut_mean` | Average rut depth (inches) |
| `Fault_Avg` | `faulting` | Average faulting (inches) |
| `FHWA_Percent_Cracking` | `fhwa_crack_pct` | Cracking percentage |
| `PSI` through `NCI` | `psi` through `nci` | Pre-computed condition indices |
| `SURF_TYPE` | `surface_type` | Surface type code |
| `GPSLatS/E`, `GPSLongS/E` | lat/lon columns | GPS coordinates |

### GPS Geocoding

For segments that have GPS coordinates but missing or unreliable milepoints, the script calls the WVDOT LRS `geometryToMeasure` API in batches of 1,000 points. This converts GPS lat/lon into route-aware milepost values. The geocoding is chunked to stay within API limits.

---

## Phase 2: Reconflation

**Input:** `condition_history` table
**Output:** `reconflate_normalized` table

### What It Does

Reconflation solves the fundamental problem that the vendor's measurement grid drifts year over year (see `WVDOT_PMS_Overview.md` section 5 for the full visual explanation). This phase:

1. Exports `condition_history` to CSV
2. Calls `lrsops reconflate` to length-weight-average raw measurements onto the stable 0.1-mile LRS target grid
3. Loads the reconflated output into `reconflate_normalized`

### Reconflation Method

- **Numerical fields** (IRI, rut, cracking, indices): length-weighted average across overlapping source segments
- **Categorical fields** (surface type, shoulder type): length-dominant rule (whichever source segment contributes the most length wins)
- **Coverage tracking**: each output row records what percentage of the target grid cell was covered by source data

### Output Table

One row per `(segment_id, survey_year)` on the stable grid, with:
- Route and milepost on the target grid (`actual_bmp`, `actual_emp`)
- All reconflated condition measurements
- Coverage percentage
- Grade flags (IRI, rutting, faulting, cracking, overall)

---

## Phase 3: Analysis Segments

**Input:** `reconflate_normalized` table + LRS attribute overlays
**Output:** `analysis_segments` table

This is the most complex phase. It builds the engine-ready table through five sub-steps.

### Sub-step 3a: Export Base Segments

Queries `reconflate_normalized` to get the **most recent survey year** for each segment:

```sql
SELECT ... FROM reconflate_normalized rn
INNER JOIN (
    SELECT segment_id, MAX(survey_year) as max_year
    FROM reconflate_normalized GROUP BY segment_id
) latest ON rn.segment_id = latest.segment_id
    AND rn.survey_year = latest.max_year
WHERE rn.actual_emp - rn.actual_bmp > 0
```

This produces `segments_base.csv` with ~260K rows of current-year condition data.

### Sub-step 3b: Export Pavement Joints

If the `pavement_joints` table exists, exports joint boundaries to `pavement_joints_lrs.csv` for the overlay step. Joints group segments into project-sized units for the optimizer.

### Sub-step 3c: LRS Reference Overlay (`lrsops rhoverlay`)

Calls `lrsops rhoverlay` to download and overlay seven LRS attribute layers:

| Layer | Code | Fields Extracted |
|-------|------|-----------------|
| Coal Routes | 15 | `SECTION_NO` → `coal_route` |
| Functional Class | 35 | `NAT_FUNCTIONAL_CLASS`, `_DESC` |
| NHS | 36 | `NHS`, `_DESC` |
| County | 12 | `COUNTY`, `_DESC` |
| District | 18 | `DISTRICT`, `_DESC` |
| Route Status | 49 | `ROUTE_STATUS`, `_DESC` |
| AADT | 2 + 77 | `AADT` (total), `AADT_COMBINATION`, `AADT_SINGLE` |

Output: `lrs_table.csv` — a reference table with all network attributes keyed by route + milepost.

### Sub-step 3d: LRS Overlay (`lrsops overlay`)

Runs a two-operation overlay pipeline defined in `segment_overlay_ops.json`:

1. **Op 1:** Overlays `segments_base.csv` with `pavement_joints_lrs.csv` to attach `joint_id`
2. **Op 2:** Overlays the result with `lrs_table.csv` to attach all network attributes (district, county, NHS, AADT, coal route, functional class, route status)

Output: `segment_overlay_output.csv`

**Fallback:** If `lrsops` is not available or fails, the script loads `segments_base.csv` directly without LRS enrichment. The resulting segments will have null values for district, county, NHS, etc.

### Sub-step 3e: Transform and Load

The `_transform_overlay_output()` function performs all column transformations in Polars before bulk inserting into the database. No SQL UPDATEs are needed after insert.

#### Column Renaming

| Overlay Column | analysis_segments Column |
|---------------|------------------------|
| `routeid` / `RouteID` | `route_id` |
| `bmp` / `BMP` | `begin_mp` |
| `emp` / `EMP` | `end_mp` |
| `2_AADT` | `aadt` |
| `18_DISTRICT` / `_DESC` | `district_code` / `district_desc` |
| `36_NHS` / `_DESC` | `nhs_code` / `nhs_desc` |
| `35_NAT_FUNCTIONAL_CLASS` / `_DESC` | `functional_class` / `functional_class_desc` |
| `12_COUNTY` / `_DESC` | `county_code` / `county_desc` |
| `49_ROUTE_STATUS` / `_DESC` | `route_status` / `route_status_desc` |
| `77_AADT_COMBINATION` / `_SINGLE` | `aadt_combination` / `aadt_single` |
| `15_SECTION_NO` | `coal_route` |

#### Condition Index Derivation

Indices that are null in the source data are derived from raw measurements:

| Index | Formula | Source |
|-------|---------|--------|
| PSI | `5.0 * exp(-0.0041 * IRI)` | IRI (in/mi) |
| RDI | `5.0 - 6.65 * rut^1.41`, clipped [0, 5] | Rut depth (inches) |
| SCI | `5.0 - 0.05 * crack_pct`, clipped [0, 5] | Cracking % |
| ECI | `SCI + 0.3` for asphalt, `5.0` for concrete | SCI or survey |
| JCI | `5.0` default (concrete-only, from survey) | Survey only |
| CSI | `5.0` default (concrete-only, from survey) | Survey only |

Any index still null after derivation is set to `5.0` (pristine baseline).

#### Composite Condition Index (CCI)

```
Asphalt (BC): CCI = MIN(PSI, RDI, SCI)
Concrete (RC): CCI = MIN(PSI, CSI, JCI)
```

#### Pavement Type Classification

| Surface Type Codes | Pavement Type |
|-------------------|--------------|
| JCP, CRC, JOINTED, CRCP | RC (rigid concrete) |
| -1, OTH, GRV, BRK, UNP, NULL | OT (other) |
| Everything else | BC (bituminous/asphalt) |

#### AADT and Truck Classification

- `aadt` comes from LRS layer 2 (`2_AADT`), the canonical total traffic count
- `truck_pct = (aadt_single + aadt_combination) / aadt`
- `truck_load` is currently hardcoded to `'L'` (low) for all segments. The H (high) designation based on coal routes and truck percentage is disabled pending calibration

#### Deterioration Family Assignment

```
family_id = pavement_type + '_' + rehab_type + '_' + truck_load
```

Example: `BC_Initial_L` (bituminous, initial construction, low truck load)

- `rehab_type` is currently hardcoded to `'Initial'` for all segments
- `truck_load` is currently hardcoded to `'L'`

This family_id is the lookup key into the `pavement_families` table for deterioration curves.

#### Equivalent Age Computation

For each condition index, the script back-calculates the age on the deterioration curve that corresponds to the current index value. This is the dTIMS `AGEFROMINDEX` inverse:

**Polynomial curves** (most families):
```
index = 5 + c1*age + c2*age²
Solving: age = (-c1 ± sqrt(c1² - 4*c2*(5 - index))) / (2*c2)
```

**Linear curves**:
```
age = -(5 - index) / c1
```

The result is six per-index age columns (`age_psi`, `age_rdi`, `age_sci`, `age_eci`, `age_jci`, `age_csi`), each representing how far along its deterioration curve the segment currently is. `current_age` is set to the maximum of all six.

#### District Field

The `district` column (VARCHAR 10) is populated from `district_code` cast to string. If neither `district` nor `district_code` is available, it defaults to null.

#### Committed Project Columns

Three columns are created with defaults but not populated during import:

| Column | Default | Populated By |
|--------|---------|-------------|
| `is_committed` | `FALSE` | `scripts/populate_committed_flags.py` |
| `committed_treatment_id` | `NULL` | `scripts/populate_committed_flags.py` |
| `committed_program_year` | `NULL` | `scripts/populate_committed_flags.py` |

These are filled in a separate step after import, based on the `projects` table.

### Bulk Insert

Rows are inserted in batches of 5,000 using `psycopg2.extras.execute_values` with verbose logging showing batch number, row range, and running totals.

### Post-Insert Summary

After loading, the script prints:
- Total segment count
- Average condition indices (PSI, RDI, SCI, ECI, CCI)
- Count of segments with real SCI data (not the 5.0 default)
- Truck load H count, coal route count, joint_id count
- Family distribution breakdown

---

## Output Table Schema

The `analysis_segments` table created by this pipeline has 47 columns. See `ANALYSIS_SEGMENTS_FIELD_REFERENCE.md` for complete field documentation including how each column is used by the optimization engine.

### Indexes

| Index | Column(s) | Purpose |
|-------|----------|---------|
| Primary key | `analysis_segment_id` | Auto-increment row ID |
| `idx_analysis_segments_joint` | `joint_id` | Fast joint-level aggregation |
| `idx_analysis_segments_family` | `family_id` | Deterioration curve lookups |
| `idx_analysis_segments_district` | `district_code` | District-based constraint queries |
| `idx_analysis_segments_committed` | `committed_program_year` (partial, WHERE is_committed = TRUE) | Committed project lookups |

---

## External Dependencies

### lrsops CLI

The `lrsops` tool is a custom CLI for LRS (Linear Referencing System) operations. It's used in two places:

1. **`lrsops rhoverlay`** — downloads and overlays LRS attribute layers from the WVDOT GIS services
2. **`lrsops overlay`** — performs the segment-to-attribute spatial overlay using a JSON operations file

If `lrsops` is not installed or fails, phase 3 falls back to loading `segments_base.csv` directly. The resulting segments will lack network attributes (district, county, NHS, AADT from LRS, coal route, joint_id) but will still have condition data.

### WVDOT LRS API

Phase 1 optionally calls the WVDOT `geometryToMeasure` API for GPS-to-milepost geocoding. This requires network access to `vision.transportation.wv.gov`.

---

## Data Flow Diagram

```
Vendor CSVs (2020.csv, 2021.csv, ...)
    │
    ▼  Phase 1
condition_history          Raw measurements per segment × year
    │                      GPS geocoded to LRS milepoints
    ▼  Phase 2
reconflate_normalized      Length-weighted onto 0.1-mi grid
    │                      Year-over-year comparable
    ▼  Phase 3a
segments_base.csv          Most recent year per segment
    │
    ├──── lrsops rhoverlay ──── lrs_table.csv (network attributes)
    │
    ▼  Phase 3d (lrsops overlay)
segment_overlay_output.csv  Segments + joints + network attributes
    │
    ▼  Phase 3e (transform)
    │  Column renaming
    │  Index derivation (PSI from IRI, RDI from rut, etc.)
    │  Pavement type classification
    │  AADT / truck classification
    │  Family ID assignment
    │  Equivalent age computation
    │
    ▼
analysis_segments          Engine-ready, ~260K rows, 47 columns
```
