# Migration Plan: PMS Engine to dTIMS Index-Based Model

## 1. Executive Summary

This document describes how to migrate the PMS optimization engine from its current raw-measurement condition model (IRI in/mi, rut inches, crack %, faulting inches composited into PCI 0-100) to the dTIMS index-based model (PSI, RDI, SCI, ECI, JCI, CSI, CCI on a 0-5 scale where 5 = best).

**What is changing:**
- **Condition metric:** PCI (0-100, weighted deduction formula) is replaced by CCI (0-5, MIN of component indices)
- **Deterioration model:** Raw-value power functions (`C(t) = C_0 + alpha * t^beta`) are replaced by index-based age curves where each index deteriorates from 5.0 downward
- **Treatments:** 7 current treatments are replaced by 14 dTIMS state-route treatments
- **Triggers:** Raw-measurement window checks with eligibility groups and veto conditions are replaced by 6-index window checks from a 25-row lookup table
- **Resets:** Raw-value ABSOLUTE/RELATIVE/PERCENTAGE resets are replaced by index-based ADDITIVE/ABSOLUTE/HOLD resets capped at 5.0
- **Benefit:** AUC of PCI difference (0-100 scale) becomes AUC of CCI difference (0-5 scale)
- **Cost model:** Single `unit_cost_per_lanemile` column becomes a treatment-by-pavement-type cost lookup

**Why:**
1. The 0-5 index model is the standard used by WVDOT and FHWA for condition reporting
2. Direct comparison with dTIMS results becomes possible, enabling validation and calibration
3. The `condition_history` table already stores `psi`, `rdi`, `sci`, `cci` -- the indices exist in the database today but are not used by the engine
4. The dTIMS trigger and reset model is simpler, more transparent, and easier to maintain than the current eligibility-group/veto system

**What is NOT changing:**
- The IBC optimization algorithm (metric-agnostic)
- The multi-year rolling work program structure
- The traffic-weighted benefit formula (`Benefit * Length * AADT^0.25`)
- The database platform (PostgreSQL) and ORM (SQLAlchemy)
- The computation framework (vectorized Polars)
- Raw measurements are kept in the database for reference and for computing PSI/RDI when survey indices are unavailable


---

## 2. Database Schema Changes

### 2.1 `analysis_segments` -- ADD index columns

```sql
-- Add condition index columns
ALTER TABLE analysis_segments ADD COLUMN current_psi DOUBLE PRECISION;
ALTER TABLE analysis_segments ADD COLUMN current_rdi DOUBLE PRECISION;
ALTER TABLE analysis_segments ADD COLUMN current_sci DOUBLE PRECISION;
ALTER TABLE analysis_segments ADD COLUMN current_cci DOUBLE PRECISION;
ALTER TABLE analysis_segments ADD COLUMN current_eci DOUBLE PRECISION;
ALTER TABLE analysis_segments ADD COLUMN current_jci DOUBLE PRECISION;
ALTER TABLE analysis_segments ADD COLUMN current_csi DOUBLE PRECISION;

-- Add pavement type (BC = Bituminous/Asphalt, RC = Rigid/Concrete)
ALTER TABLE analysis_segments ADD COLUMN pavement_type VARCHAR(4);

-- Add per-index age columns (each index has its own age variable)
ALTER TABLE analysis_segments ADD COLUMN age_psi INTEGER DEFAULT 0;
ALTER TABLE analysis_segments ADD COLUMN age_rdi INTEGER DEFAULT 0;
ALTER TABLE analysis_segments ADD COLUMN age_sci INTEGER DEFAULT 0;
ALTER TABLE analysis_segments ADD COLUMN age_eci INTEGER DEFAULT 0;
ALTER TABLE analysis_segments ADD COLUMN age_jci INTEGER DEFAULT 0;
ALTER TABLE analysis_segments ADD COLUMN age_csi INTEGER DEFAULT 0;

-- Populate pavement_type from surface_type
UPDATE analysis_segments
SET pavement_type = CASE
    WHEN surface_type IN ('JCP', 'CRC') THEN 'RC'
    ELSE 'BC'
END;

-- Populate PSI from IRI where PSI is null
UPDATE analysis_segments
SET current_psi = 5.0 * EXP(-0.0041 * current_iri)
WHERE current_psi IS NULL AND current_iri IS NOT NULL;

-- Populate RDI from rut where RDI is null
UPDATE analysis_segments
SET current_rdi = GREATEST(LEAST(5.0 - 6.65 * POWER(current_rut, 1.41), 5.0), 0.0)
WHERE current_rdi IS NULL AND current_rut IS NOT NULL;

-- Default SCI, ECI, JCI, CSI where not available from survey
-- SCI: default to 5.0 if no survey data (conservative -- assumes no structural cracking)
UPDATE analysis_segments SET current_sci = 5.0 WHERE current_sci IS NULL;

-- ECI: 5 for concrete (not applicable), default 5.0 for asphalt if no survey
UPDATE analysis_segments SET current_eci = 5.0 WHERE current_eci IS NULL;

-- JCI: 5 for asphalt (not applicable), default 5.0 for concrete if no survey
UPDATE analysis_segments SET current_jci = 5.0 WHERE current_jci IS NULL;

-- CSI: 5 for asphalt (not applicable), default 5.0 for concrete if no survey
UPDATE analysis_segments SET current_csi = 5.0 WHERE current_csi IS NULL;

-- Populate CCI = MIN of applicable indices
UPDATE analysis_segments
SET current_cci = CASE
    WHEN pavement_type = 'BC' THEN LEAST(current_psi, current_rdi, current_sci)
    WHEN pavement_type = 'RC' THEN LEAST(current_psi, current_csi, current_jci)
    ELSE LEAST(current_psi, current_rdi, current_sci)
END
WHERE current_cci IS NULL;

-- Initialize per-index ages from current_age (best we can do without history)
UPDATE analysis_segments SET age_psi = current_age WHERE age_psi = 0 OR age_psi IS NULL;
UPDATE analysis_segments SET age_rdi = current_age WHERE age_rdi = 0 OR age_rdi IS NULL;
UPDATE analysis_segments SET age_sci = current_age WHERE age_sci = 0 OR age_sci IS NULL;
UPDATE analysis_segments SET age_eci = current_age WHERE age_eci = 0 OR age_eci IS NULL;
UPDATE analysis_segments SET age_jci = current_age WHERE age_jci = 0 OR age_jci IS NULL;
UPDATE analysis_segments SET age_csi = current_age WHERE age_csi = 0 OR age_csi IS NULL;

-- DO NOT DROP raw measurement columns (keep for reference and PSI/RDI calculation)
```

**Resulting columns (relevant subset):**
```
analysis_segment_id, route_id, begin_mp, end_mp, length_miles, lanes, surface_type,
pavement_type, current_iri, current_rut, current_crack, current_faulting,
current_psi, current_rdi, current_sci, current_cci, current_eci, current_jci, current_csi,
aadt, lrs_aadt, family_id, current_age,
age_psi, age_rdi, age_sci, age_eci, age_jci, age_csi,
joint_id, district, district_code, ...
```


### 2.2 `treatments` -- Replace treatment rows

```sql
-- Mark all current treatments as inactive (preserve for history)
UPDATE treatments SET active = FALSE;

-- Add new columns
ALTER TABLE treatments ADD COLUMN IF NOT EXISTS interval_years INTEGER DEFAULT 0;
ALTER TABLE treatments ADD COLUMN IF NOT EXISTS treatment_order INTEGER DEFAULT 0;
ALTER TABLE treatments ADD COLUMN IF NOT EXISTS color VARCHAR(20);
ALTER TABLE treatments ADD COLUMN IF NOT EXISTS pavement_type_applicable VARCHAR(10);
  -- 'BC' = bituminous only, 'RC' = rigid only, 'BOTH' = either

-- Insert the 14 dTIMS state-route treatments (see Section 3 for data)
-- NOTE: unit_cost_per_lanemile is kept for backward compatibility but the
-- new treatment_costs_lookup table is the primary cost source
```


### 2.3 `treatment_triggers` -- Complete redesign

```sql
-- Create new table (keep old table renamed for reference)
ALTER TABLE treatment_triggers RENAME TO treatment_triggers_legacy;

CREATE TABLE treatment_triggers (
    trigger_id        SERIAL PRIMARY KEY,
    trigger_key       VARCHAR(50) NOT NULL,      -- e.g. 'CHIP_SEAL_1', 'THIN_OVERLAY_2'
    treatment_id      VARCHAR(50) NOT NULL REFERENCES treatments(treatment_id),
    trigger_branch    INTEGER NOT NULL DEFAULT 1, -- multiple branches per treatment (OR)
    pavement_type     VARCHAR(4),                 -- 'BC' or 'RC' or NULL (both)
    psi_lower         DOUBLE PRECISION DEFAULT 0.0,
    psi_upper         DOUBLE PRECISION DEFAULT 5.0,
    rdi_lower         DOUBLE PRECISION DEFAULT 0.0,
    rdi_upper         DOUBLE PRECISION DEFAULT 5.0,
    sci_lower         DOUBLE PRECISION DEFAULT 0.0,
    sci_upper         DOUBLE PRECISION DEFAULT 5.0,
    csi_lower         DOUBLE PRECISION DEFAULT 0.0,
    csi_upper         DOUBLE PRECISION DEFAULT 5.0,
    eci_lower         DOUBLE PRECISION DEFAULT 0.0,
    eci_upper         DOUBLE PRECISION DEFAULT 5.0,
    jci_lower         DOUBLE PRECISION DEFAULT 0.0,
    jci_upper         DOUBLE PRECISION DEFAULT 5.0,
    min_section_length DOUBLE PRECISION DEFAULT 0.0,  -- minimum length in miles
    description       TEXT
);

CREATE INDEX idx_triggers_treatment ON treatment_triggers(treatment_id);
CREATE INDEX idx_triggers_key ON treatment_triggers(trigger_key);
```


### 2.4 `treatment_resets` -- Redesign for index resets

```sql
-- Keep old table renamed for reference
ALTER TABLE treatment_resets RENAME TO treatment_resets_legacy;

CREATE TABLE treatment_resets (
    reset_id       SERIAL PRIMARY KEY,
    treatment_id   VARCHAR(50) NOT NULL REFERENCES treatments(treatment_id),
    variable       VARCHAR(10) NOT NULL,   -- 'psi', 'rdi', 'sci', 'eci', 'jci', 'csi', 'cci'
    reset_mode     VARCHAR(10) NOT NULL,   -- 'ADDITIVE', 'ABSOLUTE', 'HOLD'
    reset_delta    DOUBLE PRECISION,       -- for ADDITIVE: amount to add; for ABSOLUTE: target value
    -- ADDITIVE: new_value = MIN(current + reset_delta, 5.0)
    -- ABSOLUTE: new_value = MAX(reset_delta, current)  (only improve, never worsen)
    -- HOLD: no index change, but hold the age in place (used by Crack Seal)
    description    TEXT
);

CREATE INDEX idx_resets_treatment ON treatment_resets(treatment_id);
```


### 2.5 `pavement_families` -- Restructure for per-index deterioration

```sql
-- Keep old table renamed for reference
ALTER TABLE pavement_families RENAME TO pavement_families_legacy;

CREATE TABLE pavement_families (
    family_id         VARCHAR(20) NOT NULL,
    family_name       VARCHAR(100),
    surface_type      VARCHAR(10),           -- 'ASP', 'JCP', 'CRC', 'COMP'
    pavement_type     VARCHAR(4),            -- 'BC' or 'RC'
    functional_class  VARCHAR(50),
    traffic_level     VARCHAR(10),
    index_type        VARCHAR(10) NOT NULL,  -- 'psi', 'rdi', 'sci', 'eci', 'jci', 'csi'
    alpha             DOUBLE PRECISION NOT NULL,
    beta              DOUBLE PRECISION NOT NULL,
    initial_value     DOUBLE PRECISION NOT NULL DEFAULT 5.0,  -- new pavement starts at 5.0
    description       TEXT,
    PRIMARY KEY (family_id, index_type)
);

-- The deterioration model for indices is:
--   Index(age) = initial_value - alpha * age^beta
--   Clamped to [0.0, 5.0]
--
-- This is an INVERSION of the current model (which adds deterioration).
-- Current: Condition(t) = C_0 + alpha * t^beta  (value increases = gets worse)
-- New:     Index(age) = 5.0 - alpha * age^beta   (value decreases = gets worse)
```


### 2.6 NEW `treatment_costs_lookup` -- Cost by treatment + pavement type

```sql
CREATE TABLE treatment_costs_lookup (
    cost_id          SERIAL PRIMARY KEY,
    treatment_id     VARCHAR(50) NOT NULL REFERENCES treatments(treatment_id),
    pavement_type    VARCHAR(4) NOT NULL,    -- 'BC' or 'RC'
    cost_per_lane_mile DOUBLE PRECISION NOT NULL,
    description      TEXT
);

CREATE INDEX idx_costs_treatment ON treatment_costs_lookup(treatment_id);
CREATE UNIQUE INDEX idx_costs_unique ON treatment_costs_lookup(treatment_id, pavement_type);
```


### 2.7 `condition_history` -- ADD missing index columns

```sql
-- Already has: psi, rdi, sci, cci
ALTER TABLE condition_history ADD COLUMN IF NOT EXISTS eci DOUBLE PRECISION;
ALTER TABLE condition_history ADD COLUMN IF NOT EXISTS jci DOUBLE PRECISION;
ALTER TABLE condition_history ADD COLUMN IF NOT EXISTS csi DOUBLE PRECISION;
```


---

## 3. Data Migration

### 3.1 Insert 14 dTIMS State-Route Treatments

```sql
INSERT INTO treatments (treatment_id, treatment_name, unit_cost_per_lanemile, service_life_years,
                        min_interval_years, budget_category, active, interval_years,
                        treatment_order, color, pavement_type_applicable, description)
VALUES
-- Asphalt (BC) treatments
('CRACK_SEAL',        'Crack Seal',           5000,    3, 2, 'PRESERVATION',   TRUE,  2,  1, '#A8D08D', 'BC',   'Seal surface cracks, holds ages in place'),
('PRESERVATION_BC',   'Preservation',        25000,    5, 3, 'PRESERVATION',   TRUE,  3,  2, '#92D050', 'BC',   'General preservation (placeholder)'),
('CAPE_SEAL',         'Cape Seal',           35000,    5, 3, 'PRESERVATION',   TRUE,  3,  3, '#00B050', 'BC',   'Chip seal + fog seal or slurry seal'),
('CHIP_SEAL',         'Chip Seal',           30000,    5, 3, 'PRESERVATION',   TRUE,  3,  4, '#548235', 'BC',   'Aggregate + emulsion surface treatment'),
('MICROSURFACING',    'Microsurfacing',      40000,    6, 3, 'PRESERVATION',   TRUE,  3,  5, '#FFC000', 'BC',   'Polymer-modified emulsion surface'),
('ULTRA_THIN_OVLY',   'Ultra Thin Overlay',  55000,    7, 4, 'PRESERVATION',   TRUE,  4,  6, '#ED7D31', 'BC',   '0.75-1.0 inch overlay'),
('THIN_OVERLAY',      'Thin Overlay',        80000,    8, 5, 'REHABILITATION',  TRUE,  5,  7, '#FF0000', 'BC',   '1.5-2.0 inch mill and overlay'),
('THICK_OVERLAY',     'Thick Overlay',      120000,   10, 6, 'REHABILITATION',  TRUE,  6,  8, '#C00000', 'BC',   '3+ inch structural overlay'),
('RECONSTRUCT_BC',    'Reconstruction',     350000,   20, 10,'RECONSTRUCTION', TRUE, 10,  9, '#7030A0', 'BC',   'Full depth reconstruction'),

-- Concrete (RC) treatments
('SAW_SEAL_JOINTS',   'Saw & Seal Joints',   15000,    5, 3, 'PRESERVATION',   TRUE,  3, 10, '#BDD7EE', 'RC',   'Reseal joints'),
('MINOR_CPR_DG',      'Minor CPR Diamond Grind', 75000, 8, 5, 'REHABILITATION', TRUE, 5, 11, '#2F75B5', 'RC',   'Diamond grinding + minor repairs'),
('MAJOR_CPR_DG',      'Major CPR Diamond Grind',120000,10, 6, 'REHABILITATION', TRUE, 6, 12, '#1F4E79', 'RC',   'Diamond grinding + major repairs'),
('PRESERVATION_RC',   'PM Concrete',         25000,    5, 3, 'PRESERVATION',   TRUE,  3, 13, '#9BC2E6', 'RC',   'General concrete preservation (placeholder)'),
('RECONSTRUCT_RC',    'Reconstruction',     400000,   25, 10,'RECONSTRUCTION', TRUE, 10, 14, '#7030A0', 'RC',   'Full concrete reconstruction');
```


### 3.2 Insert 25 Trigger Lookup Rows

```sql
-- Asphalt (BC) triggers
-- Each row defines: for this treatment + branch, all 6 indices must be in [lower, upper]
-- Indices not relevant to asphalt (CSI, JCI) use 0-5 (always pass)

INSERT INTO treatment_triggers
(trigger_key, treatment_id, trigger_branch, pavement_type,
 psi_lower, psi_upper, rdi_lower, rdi_upper, sci_lower, sci_upper,
 csi_lower, csi_upper, eci_lower, eci_upper, jci_lower, jci_upper,
 min_section_length, description)
VALUES
-- Crack Seal: good ride/rut, but cracking starting
('CRACK_SEAL_1',     'CRACK_SEAL',      1, 'BC',
 3.5, 5.0,  3.5, 5.0,  2.0, 4.0,
 0.0, 5.0,  2.0, 5.0,  0.0, 5.0,
 0.5, 'Crack seal: good PSI/RDI, moderate SCI/ECI'),

-- Cape Seal: moderate condition
('CAPE_SEAL_1',      'CAPE_SEAL',       1, 'BC',
 3.0, 5.0,  3.0, 5.0,  2.0, 4.0,
 0.0, 5.0,  2.0, 4.5,  0.0, 5.0,
 0.5, 'Cape seal: moderate condition range'),

-- Chip Seal: moderate condition
('CHIP_SEAL_1',      'CHIP_SEAL',       1, 'BC',
 3.0, 5.0,  3.0, 5.0,  2.5, 4.5,
 0.0, 5.0,  2.0, 4.5,  0.0, 5.0,
 0.5, 'Chip seal: moderate surface, good structure'),

-- Microsurfacing: moderate ride/rut issues
('MICRO_1',          'MICROSURFACING',  1, 'BC',
 2.5, 4.5,  2.5, 4.5,  2.0, 4.5,
 0.0, 5.0,  2.0, 4.5,  0.0, 5.0,
 0.5, 'Microsurfacing: moderate ride and rut'),

-- Ultra Thin Overlay: fair to moderate condition
('ULTRA_THIN_1',     'ULTRA_THIN_OVLY', 1, 'BC',
 2.0, 4.0,  2.0, 4.0,  1.5, 4.0,
 0.0, 5.0,  1.5, 4.0,  0.0, 5.0,
 0.5, 'Ultra thin overlay: fair to moderate range'),

-- Thin Overlay: branch 1 -- primarily ride/rut driven
('THIN_OVLY_1',      'THIN_OVERLAY',    1, 'BC',
 1.5, 3.5,  1.5, 3.5,  1.0, 4.0,
 0.0, 5.0,  1.0, 4.0,  0.0, 5.0,
 0.5, 'Thin overlay: poor ride/rut, fair structure'),

-- Thin Overlay: branch 2 -- primarily cracking/edge driven
('THIN_OVLY_2',      'THIN_OVERLAY',    2, 'BC',
 2.0, 4.0,  2.0, 4.0,  0.5, 2.5,
 0.0, 5.0,  0.5, 2.5,  0.0, 5.0,
 0.5, 'Thin overlay: ok ride/rut, poor surface/edge'),

-- Thick Overlay: poor overall condition
('THICK_OVLY_1',     'THICK_OVERLAY',   1, 'BC',
 1.0, 3.0,  1.0, 3.0,  0.5, 3.0,
 0.0, 5.0,  0.5, 3.0,  0.0, 5.0,
 0.5, 'Thick overlay: poor to fair overall'),

-- Thick Overlay: branch 2 -- structural cracking driven
('THICK_OVLY_2',     'THICK_OVERLAY',   2, 'BC',
 1.5, 4.0,  1.5, 4.0,  0.0, 1.5,
 0.0, 5.0,  0.0, 2.0,  0.0, 5.0,
 0.5, 'Thick overlay: severe cracking/edge failure'),

-- Reconstruction (BC): very poor condition
('RECONSTRUCT_BC_1', 'RECONSTRUCT_BC',  1, 'BC',
 0.0, 2.0,  0.0, 2.0,  0.0, 2.0,
 0.0, 5.0,  0.0, 2.0,  0.0, 5.0,
 0.5, 'Reconstruction: very poor overall'),

-- Reconstruction (BC): branch 2 -- total structural failure
('RECONSTRUCT_BC_2', 'RECONSTRUCT_BC',  2, 'BC',
 0.0, 3.0,  0.0, 3.0,  0.0, 1.0,
 0.0, 5.0,  0.0, 1.0,  0.0, 5.0,
 0.5, 'Reconstruction: extreme structural/edge failure'),

-- Preservation (BC): placeholder -- wide trigger
('PRESERVATION_BC_1','PRESERVATION_BC', 1, 'BC',
 2.5, 5.0,  2.5, 5.0,  2.0, 5.0,
 0.0, 5.0,  2.0, 5.0,  0.0, 5.0,
 0.5, 'Preservation (asphalt): general good-to-moderate'),

-- ===== Concrete (RC) triggers =====
-- For concrete: PSI, CSI, JCI are the active indices; RDI, SCI, ECI use 0-5 (always pass)

-- Saw & Seal Joints: good pavement, joint maintenance needed
('SAW_SEAL_1',       'SAW_SEAL_JOINTS', 1, 'RC',
 0.0, 5.0,  0.0, 5.0,  0.0, 5.0,
 3.0, 5.0,  0.0, 5.0,  2.0, 4.5,
 0.5, 'Saw & seal: good concrete, joint maintenance'),

-- Minor CPR Diamond Grind: fair to moderate ride or joint distress
('MINOR_CPR_1',      'MINOR_CPR_DG',    1, 'RC',
 2.0, 4.0,  0.0, 5.0,  0.0, 5.0,
 2.0, 4.0,  0.0, 5.0,  1.5, 4.0,
 0.5, 'Minor CPR: moderate PSI/CSI/JCI'),

-- Minor CPR Diamond Grind: branch 2 -- roughness driven
('MINOR_CPR_2',      'MINOR_CPR_DG',    2, 'RC',
 1.5, 3.0,  0.0, 5.0,  0.0, 5.0,
 2.5, 5.0,  0.0, 5.0,  2.0, 5.0,
 0.5, 'Minor CPR: poor ride, decent joints'),

-- Major CPR Diamond Grind: poor ride and joint condition
('MAJOR_CPR_1',      'MAJOR_CPR_DG',    1, 'RC',
 1.0, 3.0,  0.0, 5.0,  0.0, 5.0,
 1.0, 3.5,  0.0, 5.0,  0.5, 3.0,
 0.5, 'Major CPR: poor PSI/CSI/JCI'),

-- Major CPR Diamond Grind: branch 2 -- severe joint deterioration
('MAJOR_CPR_2',      'MAJOR_CPR_DG',    2, 'RC',
 1.5, 4.0,  0.0, 5.0,  0.0, 5.0,
 1.0, 4.0,  0.0, 5.0,  0.0, 1.5,
 0.5, 'Major CPR: severe JCI deterioration'),

-- Reconstruction (RC): very poor concrete
('RECONSTRUCT_RC_1', 'RECONSTRUCT_RC',  1, 'RC',
 0.0, 2.0,  0.0, 5.0,  0.0, 5.0,
 0.0, 2.0,  0.0, 5.0,  0.0, 2.0,
 0.5, 'Reconstruction: very poor concrete overall'),

-- Reconstruction (RC): branch 2 -- extreme joint failure
('RECONSTRUCT_RC_2', 'RECONSTRUCT_RC',  2, 'RC',
 0.0, 3.0,  0.0, 5.0,  0.0, 5.0,
 0.0, 3.0,  0.0, 5.0,  0.0, 1.0,
 0.5, 'Reconstruction: extreme joint failure'),

-- PM Concrete (placeholder)
('PRESERVATION_RC_1','PRESERVATION_RC', 1, 'RC',
 2.5, 5.0,  0.0, 5.0,  0.0, 5.0,
 2.5, 5.0,  0.0, 5.0,  2.0, 5.0,
 0.5, 'PM Concrete: general good-to-moderate');
```

> **Note:** These thresholds are representative starting points derived from dTIMS configuration patterns. They must be calibrated against the actual `Analysis_Lookup_Triggers` table from the dTIMS dump when it becomes available.


### 3.3 Insert Treatment Reset Rules

```sql
-- ===== Crack Seal: HOLD mode -- no index change, holds ages =====
INSERT INTO treatment_resets (treatment_id, variable, reset_mode, reset_delta, description)
VALUES
('CRACK_SEAL', 'psi', 'HOLD', NULL, 'Hold PSI age in place'),
('CRACK_SEAL', 'rdi', 'HOLD', NULL, 'Hold RDI age in place'),
('CRACK_SEAL', 'sci', 'HOLD', NULL, 'Hold SCI age in place'),
('CRACK_SEAL', 'eci', 'HOLD', NULL, 'Hold ECI age in place');

-- ===== Cape Seal: +0.25 to CCI, ECI, SCI =====
INSERT INTO treatment_resets (treatment_id, variable, reset_mode, reset_delta, description)
VALUES
('CAPE_SEAL', 'cci', 'ADDITIVE', 0.25, 'CCI +0.25'),
('CAPE_SEAL', 'eci', 'ADDITIVE', 0.25, 'ECI +0.25'),
('CAPE_SEAL', 'sci', 'ADDITIVE', 0.25, 'SCI +0.25');

-- ===== Chip Seal: +0.5 to CCI, ECI, SCI =====
INSERT INTO treatment_resets (treatment_id, variable, reset_mode, reset_delta, description)
VALUES
('CHIP_SEAL', 'cci', 'ADDITIVE', 0.5, 'CCI +0.5'),
('CHIP_SEAL', 'eci', 'ADDITIVE', 0.5, 'ECI +0.5'),
('CHIP_SEAL', 'sci', 'ADDITIVE', 0.5, 'SCI +0.5');

-- ===== Microsurfacing: +0.75 to CCI, ECI, SCI, PSI, RDI =====
INSERT INTO treatment_resets (treatment_id, variable, reset_mode, reset_delta, description)
VALUES
('MICROSURFACING', 'cci', 'ADDITIVE', 0.75, 'CCI +0.75'),
('MICROSURFACING', 'eci', 'ADDITIVE', 0.75, 'ECI +0.75'),
('MICROSURFACING', 'sci', 'ADDITIVE', 0.75, 'SCI +0.75'),
('MICROSURFACING', 'psi', 'ADDITIVE', 0.75, 'PSI +0.75'),
('MICROSURFACING', 'rdi', 'ADDITIVE', 0.75, 'RDI +0.75');

-- ===== Ultra Thin Overlay: +1.0 to CCI, ECI, SCI, PSI, RDI =====
INSERT INTO treatment_resets (treatment_id, variable, reset_mode, reset_delta, description)
VALUES
('ULTRA_THIN_OVLY', 'cci', 'ADDITIVE', 1.0, 'CCI +1.0'),
('ULTRA_THIN_OVLY', 'eci', 'ADDITIVE', 1.0, 'ECI +1.0'),
('ULTRA_THIN_OVLY', 'sci', 'ADDITIVE', 1.0, 'SCI +1.0'),
('ULTRA_THIN_OVLY', 'psi', 'ADDITIVE', 1.0, 'PSI +1.0'),
('ULTRA_THIN_OVLY', 'rdi', 'ADDITIVE', 1.0, 'RDI +1.0');

-- ===== Thin Overlay: +1.25 to CCI, ECI, SCI, PSI, RDI =====
INSERT INTO treatment_resets (treatment_id, variable, reset_mode, reset_delta, description)
VALUES
('THIN_OVERLAY', 'cci', 'ADDITIVE', 1.25, 'CCI +1.25'),
('THIN_OVERLAY', 'eci', 'ADDITIVE', 1.25, 'ECI +1.25'),
('THIN_OVERLAY', 'sci', 'ADDITIVE', 1.25, 'SCI +1.25'),
('THIN_OVERLAY', 'psi', 'ADDITIVE', 1.25, 'PSI +1.25'),
('THIN_OVERLAY', 'rdi', 'ADDITIVE', 1.25, 'RDI +1.25');

-- ===== Thick Overlay: +2.0 to all asphalt indices (estimated) =====
INSERT INTO treatment_resets (treatment_id, variable, reset_mode, reset_delta, description)
VALUES
('THICK_OVERLAY', 'cci', 'ADDITIVE', 2.0, 'CCI +2.0'),
('THICK_OVERLAY', 'eci', 'ADDITIVE', 2.0, 'ECI +2.0'),
('THICK_OVERLAY', 'sci', 'ADDITIVE', 2.0, 'SCI +2.0'),
('THICK_OVERLAY', 'psi', 'ADDITIVE', 2.0, 'PSI +2.0'),
('THICK_OVERLAY', 'rdi', 'ADDITIVE', 2.0, 'RDI +2.0');

-- ===== Reconstruction (BC): reset all to 5.0 =====
INSERT INTO treatment_resets (treatment_id, variable, reset_mode, reset_delta, description)
VALUES
('RECONSTRUCT_BC', 'psi', 'ABSOLUTE', 5.0, 'Reset PSI to new'),
('RECONSTRUCT_BC', 'rdi', 'ABSOLUTE', 5.0, 'Reset RDI to new'),
('RECONSTRUCT_BC', 'sci', 'ABSOLUTE', 5.0, 'Reset SCI to new'),
('RECONSTRUCT_BC', 'eci', 'ABSOLUTE', 5.0, 'Reset ECI to new'),
('RECONSTRUCT_BC', 'cci', 'ABSOLUTE', 5.0, 'Reset CCI to new');

-- ===== Preservation (BC): parametric reset (use ADDITIVE +0.5 as approximation) =====
INSERT INTO treatment_resets (treatment_id, variable, reset_mode, reset_delta, description)
VALUES
('PRESERVATION_BC', 'cci', 'ADDITIVE', 0.5, 'CCI +0.5'),
('PRESERVATION_BC', 'eci', 'ADDITIVE', 0.5, 'ECI +0.5'),
('PRESERVATION_BC', 'sci', 'ADDITIVE', 0.5, 'SCI +0.5'),
('PRESERVATION_BC', 'psi', 'ADDITIVE', 0.5, 'PSI +0.5'),
('PRESERVATION_BC', 'rdi', 'ADDITIVE', 0.5, 'RDI +0.5');

-- ===== Saw & Seal Joints: +1.0 to CCI, reset JCI =====
INSERT INTO treatment_resets (treatment_id, variable, reset_mode, reset_delta, description)
VALUES
('SAW_SEAL_JOINTS', 'cci', 'ADDITIVE', 1.0, 'CCI +1.0'),
('SAW_SEAL_JOINTS', 'jci', 'ABSOLUTE', 5.0, 'Reset JCI to new');

-- ===== Minor CPR Diamond Grind: set PSI, CSI, JCI to MAX(4.5, current) =====
INSERT INTO treatment_resets (treatment_id, variable, reset_mode, reset_delta, description)
VALUES
('MINOR_CPR_DG', 'cci', 'ABSOLUTE', 4.5, 'CCI to 4.5'),
('MINOR_CPR_DG', 'psi', 'ABSOLUTE', 4.5, 'PSI to 4.5'),
('MINOR_CPR_DG', 'csi', 'ABSOLUTE', 4.5, 'CSI to 4.5'),
('MINOR_CPR_DG', 'jci', 'ABSOLUTE', 4.5, 'JCI to 4.5');

-- ===== Major CPR Diamond Grind: same as Minor =====
INSERT INTO treatment_resets (treatment_id, variable, reset_mode, reset_delta, description)
VALUES
('MAJOR_CPR_DG', 'cci', 'ABSOLUTE', 4.5, 'CCI to 4.5'),
('MAJOR_CPR_DG', 'psi', 'ABSOLUTE', 4.5, 'PSI to 4.5'),
('MAJOR_CPR_DG', 'csi', 'ABSOLUTE', 4.5, 'CSI to 4.5'),
('MAJOR_CPR_DG', 'jci', 'ABSOLUTE', 4.5, 'JCI to 4.5');

-- ===== Reconstruction (RC): reset all to 5.0 =====
INSERT INTO treatment_resets (treatment_id, variable, reset_mode, reset_delta, description)
VALUES
('RECONSTRUCT_RC', 'psi', 'ABSOLUTE', 5.0, 'Reset PSI to new'),
('RECONSTRUCT_RC', 'csi', 'ABSOLUTE', 5.0, 'Reset CSI to new'),
('RECONSTRUCT_RC', 'jci', 'ABSOLUTE', 5.0, 'Reset JCI to new'),
('RECONSTRUCT_RC', 'cci', 'ABSOLUTE', 5.0, 'Reset CCI to new');

-- ===== PM Concrete: placeholder with moderate improvement =====
INSERT INTO treatment_resets (treatment_id, variable, reset_mode, reset_delta, description)
VALUES
('PRESERVATION_RC', 'cci', 'ADDITIVE', 0.5, 'CCI +0.5'),
('PRESERVATION_RC', 'csi', 'ADDITIVE', 0.5, 'CSI +0.5'),
('PRESERVATION_RC', 'jci', 'ADDITIVE', 0.5, 'JCI +0.5'),
('PRESERVATION_RC', 'psi', 'ADDITIVE', 0.5, 'PSI +0.5');
```


### 3.4 Treatment Cost Lookup (Template)

```sql
-- Actual costs TBD from Analysis_Lookup_Trt_Costs table in dTIMS dump
-- These are placeholder values to be replaced with real data

INSERT INTO treatment_costs_lookup (treatment_id, pavement_type, cost_per_lane_mile, description)
VALUES
('CRACK_SEAL',      'BC',   5000,  'Placeholder'),
('PRESERVATION_BC', 'BC',  25000,  'Placeholder'),
('CAPE_SEAL',       'BC',  35000,  'Placeholder'),
('CHIP_SEAL',       'BC',  30000,  'Placeholder'),
('MICROSURFACING',  'BC',  40000,  'Placeholder'),
('ULTRA_THIN_OVLY', 'BC',  55000,  'Placeholder'),
('THIN_OVERLAY',    'BC',  80000,  'Placeholder'),
('THICK_OVERLAY',   'BC', 120000,  'Placeholder'),
('RECONSTRUCT_BC',  'BC', 350000,  'Placeholder'),
('SAW_SEAL_JOINTS', 'RC',  15000,  'Placeholder'),
('MINOR_CPR_DG',    'RC',  75000,  'Placeholder'),
('MAJOR_CPR_DG',    'RC', 120000,  'Placeholder'),
('PRESERVATION_RC', 'RC',  25000,  'Placeholder'),
('RECONSTRUCT_RC',  'RC', 400000,  'Placeholder');
```


---

## 4. Code Changes -- File by File

### 4.1 `engine/condition/indices.py` (NEW -- replaces `pci.py` and `deductions.py`)

Create a new file that provides all index calculation functions. The old `pci.py` and `deductions.py` are retained but no longer imported by the engine.

```python
"""
Condition index calculations for the dTIMS model.

All indices are on a 0-5 scale where 5 = best (new pavement).

Indices:
  PSI  - Present Serviceability Index (from IRI)
  RDI  - Rut Depth Index (from rut)
  SCI  - Structural Cracking Index (from survey -- cannot be computed from crack_percent)
  ECI  - Edge Condition Index (asphalt only, from survey)
  JCI  - Joint Condition Index (concrete only, from survey)
  CSI  - Cracking Severity Index (concrete only, from survey)
  CCI  - Composite Condition Index = MIN of applicable indices
"""

from typing import Optional, Dict
import polars as pl


# ---------------------------------------------------------------------------
# Scalar functions
# ---------------------------------------------------------------------------

def calculate_psi(iri: Optional[float]) -> Optional[float]:
    """PSI = 5 * exp(-0.0041 * IRI). Returns None if IRI is None."""
    if iri is None:
        return None
    import math
    return max(0.0, min(5.0, 5.0 * math.exp(-0.0041 * iri)))


def calculate_rdi(rut: Optional[float]) -> Optional[float]:
    """RDI = MAX(MIN(5 - 6.65 * rut^1.41, 5), 0). Returns None if rut is None."""
    if rut is None:
        return None
    return max(0.0, min(5.0, 5.0 - 6.65 * (rut ** 1.41)))


def calculate_cci(
    psi: Optional[float],
    rdi: Optional[float],
    sci: Optional[float],
    eci: Optional[float],
    jci: Optional[float],
    csi: Optional[float],
    pavement_type: str = "BC",
) -> Optional[float]:
    """
    CCI = MIN of applicable indices.
      Asphalt (BC): MIN(PSI, RDI, SCI)
      Concrete (RC): MIN(PSI, CSI, JCI)
    """
    if pavement_type == "RC":
        vals = [v for v in [psi, csi, jci] if v is not None]
    else:
        vals = [v for v in [psi, rdi, sci] if v is not None]
    if not vals:
        return None
    return min(vals)


# ---------------------------------------------------------------------------
# Vectorized Polars functions
# ---------------------------------------------------------------------------

def calculate_psi_vectorized(iri_expr: pl.Expr) -> pl.Expr:
    """Vectorized PSI = 5 * exp(-0.0041 * IRI), clamped to [0, 5]."""
    return (5.0 * (-0.0041 * iri_expr).exp()).clip(0.0, 5.0)


def calculate_rdi_vectorized(rut_expr: pl.Expr) -> pl.Expr:
    """Vectorized RDI = MAX(MIN(5 - 6.65 * rut^1.41, 5), 0)."""
    return (5.0 - 6.65 * rut_expr.pow(1.41)).clip(0.0, 5.0)


def calculate_cci_vectorized(
    psi_col: str, rdi_col: str, sci_col: str,
    eci_col: str, jci_col: str, csi_col: str,
    pavement_type_col: str = "pavement_type",
) -> pl.Expr:
    """
    Vectorized CCI.
      BC: MIN(psi, rdi, sci)
      RC: MIN(psi, csi, jci)
    """
    bc_cci = pl.min_horizontal(pl.col(psi_col), pl.col(rdi_col), pl.col(sci_col))
    rc_cci = pl.min_horizontal(pl.col(psi_col), pl.col(csi_col), pl.col(jci_col))

    return (
        pl.when(pl.col(pavement_type_col) == "RC")
        .then(rc_cci)
        .otherwise(bc_cci)
    )


def calculate_condition_indices_polars(
    df: pl.DataFrame,
    iri_col: str = "current_iri",
    rut_col: str = "current_rut",
    pavement_type_col: str = "pavement_type",
) -> pl.DataFrame:
    """
    Add all condition index columns to a DataFrame.

    Calculates PSI and RDI from raw measurements.
    SCI, ECI, JCI, CSI must already exist or will be defaulted to 5.0.
    CCI is computed as MIN of applicable indices.

    Args:
        df: Input DataFrame with raw measurement columns
        iri_col: Column name for IRI values
        rut_col: Column name for rut depth values
        pavement_type_col: Column name for pavement type ('BC'/'RC')

    Returns:
        DataFrame with added columns:
        - current_psi, current_rdi, current_cci
        - current_sci, current_eci, current_jci, current_csi (defaulted if missing)
        - condition_category: Good/Fair/Poor classification
    """
    result = df.clone()

    # Compute PSI from IRI
    if iri_col in result.columns:
        result = result.with_columns(
            calculate_psi_vectorized(pl.col(iri_col)).alias("current_psi")
        )
    elif "current_psi" not in result.columns:
        result = result.with_columns(pl.lit(None).cast(pl.Float64).alias("current_psi"))

    # Compute RDI from rut
    if rut_col in result.columns:
        result = result.with_columns(
            calculate_rdi_vectorized(pl.col(rut_col)).alias("current_rdi")
        )
    elif "current_rdi" not in result.columns:
        result = result.with_columns(pl.lit(None).cast(pl.Float64).alias("current_rdi"))

    # Default survey-based indices if not present
    for idx_col in ["current_sci", "current_eci", "current_jci", "current_csi"]:
        if idx_col not in result.columns:
            result = result.with_columns(pl.lit(5.0).alias(idx_col))

    # Ensure pavement_type column exists
    if pavement_type_col not in result.columns:
        if "surface_type" in result.columns:
            result = result.with_columns(
                pl.when(pl.col("surface_type").is_in(["JCP", "CRC"]))
                .then(pl.lit("RC"))
                .otherwise(pl.lit("BC"))
                .alias(pavement_type_col)
            )
        else:
            result = result.with_columns(pl.lit("BC").alias(pavement_type_col))

    # Compute CCI
    result = result.with_columns(
        calculate_cci_vectorized(
            "current_psi", "current_rdi", "current_sci",
            "current_eci", "current_jci", "current_csi",
            pavement_type_col,
        ).alias("current_cci")
    )

    # Condition category based on CCI thresholds
    # Good: CCI >= 3.5, Fair: 2.5 <= CCI < 3.5, Poor: CCI < 2.5
    result = result.with_columns(
        pl.when(pl.col("current_cci") >= 3.5)
        .then(pl.lit("Good"))
        .when(pl.col("current_cci") >= 2.5)
        .then(pl.lit("Fair"))
        .otherwise(pl.lit("Poor"))
        .alias("condition_category")
    )

    return result
```

**Key design notes:**
- `calculate_psi_vectorized` and `calculate_rdi_vectorized` return `pl.Expr` (not `pl.Series`), so they compose inside `with_columns()` -- same pattern as the current `calculate_iri_deduction_vectorized` but simpler math
- SCI, ECI, JCI, CSI are sourced from survey data; this module only defaults them to 5.0 when missing
- CCI thresholds for Good/Fair/Poor (3.5/2.5) replace the PCI thresholds (80/60)


### 4.2 `engine/deterioration/models.py` (REWRITE)

**Current state:** Projects raw values using `Condition(t) = C_0 + alpha * t^beta` (values increase = worse).

**New state:** Projects indices using `Index(age) = initial_value - alpha * age^beta` (values decrease = worse), clamped to [0, 5].

#### Changes to dataclasses

```python
# REPLACE DeteriorationParams
@dataclass
class IndexDeteriorationParams:
    """Parameters for a single condition index deterioration curve."""
    index_type: str          # "psi", "rdi", "sci", "eci", "jci", "csi"
    initial_value: float     # Starting value for new pavement (typically 5.0)
    alpha: float             # Deterioration rate coefficient
    beta: float              # Shape exponent (typically 1.0 - 2.0)

    def validate(self) -> bool:
        if self.alpha < 0 or self.beta < 0 or self.beta > 5:
            return False
        if self.initial_value < 0 or self.initial_value > 5:
            return False
        return True


# REPLACE YearlyCondition
@dataclass
class YearlyCondition:
    """Condition index values for a single year."""
    year: int
    psi: Optional[float] = None
    rdi: Optional[float] = None
    sci: Optional[float] = None
    eci: Optional[float] = None
    jci: Optional[float] = None
    csi: Optional[float] = None
    cci: Optional[float] = None
    condition_category: Optional[str] = None   # Good/Fair/Poor
```

#### Core deterioration function

```python
def calculate_index_at_age(
    initial_value: float,
    alpha: float,
    beta: float,
    age: int,
) -> float:
    """
    Calculate index value at a given age.

    Index(age) = initial_value - alpha * age^beta
    Clamped to [0.0, 5.0].

    Args:
        initial_value: Index value at age 0 (typically 5.0)
        alpha: Deterioration rate
        beta: Shape exponent
        age: Years since construction/treatment

    Returns:
        Index value at the given age
    """
    if age <= 0:
        return min(5.0, max(0.0, initial_value))
    deterioration = alpha * (age ** beta)
    return max(0.0, min(5.0, initial_value - deterioration))
```

#### Equivalent-age back-calculation

When a treatment improves an index from `current_value` to `new_value`, we must compute the equivalent age that corresponds to `new_value` on the deterioration curve:

```python
def compute_equivalent_age(
    new_index_value: float,
    initial_value: float,
    alpha: float,
    beta: float,
) -> float:
    """
    Reverse-compute the age that corresponds to a given index value.

    From: index = initial_value - alpha * age^beta
    Solve: age = ((initial_value - index) / alpha) ^ (1/beta)

    Returns 0 if new_index_value >= initial_value.
    """
    if new_index_value >= initial_value or alpha <= 0:
        return 0.0
    gap = initial_value - new_index_value
    return (gap / alpha) ** (1.0 / beta)
```

#### Vectorized projection (`project_deterioration_polars`)

Replace the current function. The new version:

1. Cross-joins segments with years `[0, 1, ..., analysis_years]`
2. Joins family parameters for each `(family_id, index_type)` pair
3. Computes `Index(age) = initial_value - alpha * (age_col + year)^beta`, clamped to `[0, 5]`
4. Computes CCI as `MIN(applicable indices)` per row
5. Assigns condition category

**Function signature (unchanged):**

```python
def project_deterioration_polars(
    analysis_df: pl.DataFrame,
    analysis_years: int = 20,
    family_params_df: Optional[pl.DataFrame] = None,
) -> pl.DataFrame:
```

**New required input columns on `analysis_df`:**
```
analysis_segment_id, family_id, pavement_type,
current_psi, current_rdi, current_sci, current_eci, current_jci, current_csi,
age_psi, age_rdi, age_sci, age_eci, age_jci, age_csi
```

**New output columns (per row = one segment x one year):**
```
analysis_segment_id, family_id, pavement_type, year,
psi, rdi, sci, eci, jci, csi, cci, condition_category
```

**Key vectorized operations:**

```python
# For each index type (psi, rdi, sci, eci, jci, csi):
# 1. Join params: alpha_{idx}, beta_{idx}, initial_{idx}
# 2. Back-calculate effective initial:
#    effective_initial = current_{idx} + alpha * age_{idx}^beta
#    (but clamp effective_initial to [0, 5])
# 3. Project:
#    {idx}(year) = effective_initial - alpha * (age_{idx} + year)^beta
#    Clamped to [0, 5]

# Example for PSI:
result = result.with_columns(
    (
        pl.col("psi_effective_initial")
        - pl.col("psi_alpha") * (pl.col("age_psi") + pl.col("year")).pow(pl.col("psi_beta"))
    ).clip(0.0, 5.0).alias("psi")
)

# CCI:
result = result.with_columns(
    pl.when(pl.col("pavement_type") == "RC")
    .then(pl.min_horizontal("psi", "csi", "jci"))
    .otherwise(pl.min_horizontal("psi", "rdi", "sci"))
    .alias("cci")
)
```

#### Family params DataFrame

Replace `create_family_params_dataframe()`:

```python
def create_family_params_dataframe() -> pl.DataFrame:
    """
    Create family params as a long-format DataFrame.

    Returns DataFrame with columns:
    - family_id, index_type, alpha, beta, initial_value
    """
    # Load from database if available, otherwise use DEFAULT_FAMILY_PARAMS
    rows = []
    for family_id, indices in DEFAULT_FAMILY_PARAMS.items():
        for index_type, params in indices.items():
            rows.append({
                "family_id": family_id,
                "index_type": index_type,
                "alpha": params.alpha,
                "beta": params.beta,
                "initial_value": params.initial_value,
            })
    return pl.DataFrame(rows)
```

**New DEFAULT_FAMILY_PARAMS structure:**

```python
DEFAULT_FAMILY_PARAMS: Dict[str, Dict[str, IndexDeteriorationParams]] = {
    "FAM-01": {  # Asphalt Interstate - High Traffic
        "psi": IndexDeteriorationParams("psi", 5.0, 0.08, 1.3),
        "rdi": IndexDeteriorationParams("rdi", 5.0, 0.06, 1.5),
        "sci": IndexDeteriorationParams("sci", 5.0, 0.10, 1.4),
        "eci": IndexDeteriorationParams("eci", 5.0, 0.07, 1.3),
    },
    # ... one entry per family, with per-index params
    # Concrete families include "psi", "csi", "jci" instead of "rdi", "sci", "eci"
    "FAM-06": {  # Concrete (JCP) Interstate
        "psi": IndexDeteriorationParams("psi", 5.0, 0.06, 1.1),
        "csi": IndexDeteriorationParams("csi", 5.0, 0.05, 1.2),
        "jci": IndexDeteriorationParams("jci", 5.0, 0.08, 1.3),
    },
}
```

> **Note:** The alpha/beta values for index deterioration must be calibrated from dTIMS model coefficients or from condition_history regressions. The values above are illustrative placeholders.


### 4.3 `engine/treatments/triggers.py` (REWRITE)

**Current state:** Complex multi-dimensional feasibility envelope with eligibility groups (AND within, OR between) and veto conditions, operating on raw measurements (`iri_current`, `rut_current`, `crack_current`, `aadt`, `age_years`, `structural_flag`).

**New state:** Simple 6-index window checks from the trigger lookup table. For each treatment branch, ALL 6 indices must be within `[lower, upper]`. Multiple branches per treatment are OR-ed.

#### New dataclasses

```python
@dataclass
class IndexTriggerBranch:
    """One branch of a treatment trigger (all 6 indices must be in range)."""
    trigger_key: str
    treatment_id: str
    trigger_branch: int
    pavement_type: Optional[str]     # 'BC', 'RC', or None
    psi_lower: float
    psi_upper: float
    rdi_lower: float
    rdi_upper: float
    sci_lower: float
    sci_upper: float
    csi_lower: float
    csi_upper: float
    eci_lower: float
    eci_upper: float
    jci_lower: float
    jci_upper: float
    min_section_length: float


@dataclass
class TreatmentEligibility:
    """Result of evaluating triggers for a treatment."""
    treatment_id: str
    treatment_name: str
    eligible: bool
    matched_branch: Optional[int] = None
```

#### Core scalar evaluation

```python
def evaluate_index_triggers(
    psi: float, rdi: float, sci: float,
    csi: float, eci: float, jci: float,
    pavement_type: str,
    section_length: float,
    branches: List[IndexTriggerBranch],
) -> Tuple[bool, Optional[int]]:
    """
    Check if segment indices satisfy any trigger branch.

    For each branch:
      1. Check pavement_type matches (or branch.pavement_type is None)
      2. Check section_length >= branch.min_section_length
      3. Check ALL 6 indices are within [lower, upper]
    Multiple branches are OR-ed.

    Returns:
        (eligible, matched_branch_number) or (False, None)
    """
    for branch in branches:
        if branch.pavement_type and branch.pavement_type != pavement_type:
            continue
        if section_length < branch.min_section_length:
            continue
        if not (branch.psi_lower <= psi <= branch.psi_upper):
            continue
        if not (branch.rdi_lower <= rdi <= branch.rdi_upper):
            continue
        if not (branch.sci_lower <= sci <= branch.sci_upper):
            continue
        if not (branch.csi_lower <= csi <= branch.csi_upper):
            continue
        if not (branch.eci_lower <= eci <= branch.eci_upper):
            continue
        if not (branch.jci_lower <= jci <= branch.jci_upper):
            continue
        return True, branch.trigger_branch
    return False, None
```

#### Vectorized evaluation (`evaluate_triggers_polars`)

**New function signature:**

```python
def evaluate_triggers_polars(
    analysis_df: pl.DataFrame,
    treatments_df: pl.DataFrame,
    triggers_df: pl.DataFrame,
) -> pl.DataFrame:
    """
    Vectorized trigger evaluation for all segment x treatment combinations.

    Args:
        analysis_df: DataFrame with columns:
            - analysis_segment_id
            - current_psi, current_rdi, current_sci, current_csi, current_eci, current_jci
            - pavement_type ('BC' or 'RC')
            - length_miles
        treatments_df: DataFrame with columns:
            - treatment_id, treatment_name, active
        triggers_df: DataFrame with columns (from treatment_triggers table):
            - trigger_key, treatment_id, trigger_branch, pavement_type,
            - psi_lower, psi_upper, rdi_lower, rdi_upper,
            - sci_lower, sci_upper, csi_lower, csi_upper,
            - eci_lower, eci_upper, jci_lower, jci_upper,
            - min_section_length

    Returns:
        DataFrame of eligible (analysis_segment_id, treatment_id) pairs
    """
```

**Vectorized strategy:**

```python
# 1. Cross join segments x trigger branches
combos = analysis_df.join(triggers_df, how="cross")

# 2. Filter by pavement_type match
combos = combos.filter(
    (pl.col("pavement_type_right").is_null()) |
    (pl.col("pavement_type") == pl.col("pavement_type_right"))
)

# 3. Filter by min_section_length
combos = combos.filter(pl.col("length_miles") >= pl.col("min_section_length"))

# 4. Check all 6 index windows (vectorized boolean columns)
combos = combos.filter(
    (pl.col("current_psi").is_between(pl.col("psi_lower"), pl.col("psi_upper"))) &
    (pl.col("current_rdi").is_between(pl.col("rdi_lower"), pl.col("rdi_upper"))) &
    (pl.col("current_sci").is_between(pl.col("sci_lower"), pl.col("sci_upper"))) &
    (pl.col("current_csi").is_between(pl.col("csi_lower"), pl.col("csi_upper"))) &
    (pl.col("current_eci").is_between(pl.col("eci_lower"), pl.col("eci_upper"))) &
    (pl.col("current_jci").is_between(pl.col("jci_lower"), pl.col("jci_upper")))
)

# 5. Deduplicate: one row per (segment, treatment) -- any branch match suffices
eligible = combos.select([
    "analysis_segment_id", "treatment_id"
]).unique()

return eligible
```

This is far simpler than the current approach which requires:
- Separating eligibility vs. veto triggers
- Pivoting variable names into columns
- Grouping by `trigger_group` with AND-within/OR-between logic
- Handling missing variables


### 4.4 `engine/benefits/auc.py` (MODIFY)

**What changes:**
- Replace PCI-based AUC with CCI-based AUC
- CCI is on a 0-5 scale (higher is better), so benefit = `with_treatment_cci - do_nothing_cci` integrated over time
- The trapezoidal integration function is unchanged
- `CurveData` stores CCI values instead of per-distress raw values
- `BenefitResult` uses `cci_benefit` instead of `pci_benefit`

#### Changes to `CurveData`

```python
@dataclass
class CurveData:
    """Data points for a condition curve (do-nothing or with-treatment)."""
    years: List[int]
    cci_values: List[Optional[float]] = field(default_factory=list)
    # Optionally retain per-index curves for detailed reporting:
    psi_values: List[Optional[float]] = field(default_factory=list)
    rdi_values: List[Optional[float]] = field(default_factory=list)
    sci_values: List[Optional[float]] = field(default_factory=list)
```

#### Changes to `BenefitResult`

```python
@dataclass
class BenefitResult:
    """Result of benefit calculation for a treatment."""
    treatment_id: str
    treatment_year: int
    analysis_years: int
    cci_benefit: Optional[float] = None    # CCI-years (REPLACES pci_benefit)
    total_benefit: Optional[float] = None  # Same as cci_benefit
    do_nothing_curve: Optional[CurveData] = None
    with_treatment_curve: Optional[CurveData] = None
    annual_benefits: List[float] = field(default_factory=list)
```

#### Changes to `calculate_benefit_auc`

Rename to `calculate_benefit_auc` (same name, new internals). The function:

1. Projects do-nothing CCI curve using `project_deterioration_polars` (or scalar equivalent)
2. Applies treatment resets to get post-treatment index values
3. Projects with-treatment CCI curve from new values
4. Computes annual CCI difference (with_treatment - do_nothing, higher is better)
5. Integrates via trapezoidal rule

#### Changes to `calculate_benefits_polars`

**New function signature (compatible):**

```python
def calculate_benefits_polars(
    analysis_df: pl.DataFrame,
    treatments_df: pl.DataFrame,
    analysis_years: int = 20,
    treatment_year: int = 0,
) -> pl.DataFrame:
    """
    Vectorized benefit calculation for all segment x treatment combinations.

    Returns DataFrame with columns:
    - analysis_segment_id, treatment_id
    - cci_benefit (REPLACES pci_benefit)
    - total_benefit (same as cci_benefit)
    """
```

**Key change in vectorized flow:**
- Currently computes do-nothing and with-treatment IRI/rut/crack/PCI curves, then takes PCI difference
- New version computes do-nothing and with-treatment CCI curves, then takes CCI difference
- The annual benefit is `CCI_with_treatment(year) - CCI_do_nothing(year)`, clamped to `>= 0`
- Integration is the same trapezoidal rule


### 4.5 `engine/benefits/weighting.py` (MINIMAL CHANGE)

The weighting formula is identical: `Weighted_Benefit = Benefit * Length * AADT^0.25`.

**Only change:** Update column name detection in `calculate_weighted_benefits_polars`:

```python
# OLD (line ~313):
for candidate in ["benefit_auc", "pci_benefit", "total_benefit"]:

# NEW:
for candidate in ["benefit_auc", "cci_benefit", "pci_benefit", "total_benefit"]:
```

And in `add_traffic_weighting_polars`:

```python
# OLD default:
benefit_col: str = "pci_benefit"

# NEW default:
benefit_col: str = "cci_benefit"
```


### 4.6 `engine/optimization/ibc.py` (NO CHANGE)

The IBC algorithm operates on abstract `cost` and `benefit` / `weighted_benefit` columns. It does not reference PCI, CCI, or any condition metric directly.

**No code changes required.** The algorithm:
1. Builds efficiency frontiers from `(analysis_segment_id, treatment_id, cost, weighted_benefit)`
2. Computes incremental B/C ratios
3. Greedy selection within budget

All of this is metric-agnostic.


### 4.7 `engine/optimization/work_program.py` (MODIFY)

#### `_calculate_network_gfp` (lines 86-127)

**Current:** Uses `pci_score` with thresholds 80/60.

**New:**

```python
def _calculate_network_gfp(
    conditions_df: pl.DataFrame,
    good_threshold: float = 3.5,
    poor_threshold: float = 2.5,
) -> Tuple[float, float, float]:
    """
    Calculate network % Good/Fair/Poor from CCI values.

    Good: CCI >= good_threshold (default 3.5)
    Fair: poor_threshold <= CCI < good_threshold
    Poor: CCI < poor_threshold (default 2.5)
    """
    cci_col = "current_cci" if "current_cci" in conditions_df.columns else "cci"

    if "length_miles" in conditions_df.columns:
        total_miles = conditions_df["length_miles"].sum()
        if total_miles <= 0:
            total_miles = len(conditions_df)
        good_miles = conditions_df.filter(pl.col(cci_col) >= good_threshold)["length_miles"].sum()
        fair_miles = conditions_df.filter(
            (pl.col(cci_col) >= poor_threshold) & (pl.col(cci_col) < good_threshold)
        )["length_miles"].sum()
        poor_miles = conditions_df.filter(pl.col(cci_col) < poor_threshold)["length_miles"].sum()
        return (
            round(good_miles / total_miles * 100, 2),
            round(fair_miles / total_miles * 100, 2),
            round(poor_miles / total_miles * 100, 2),
        )
    else:
        # Equal weight per segment (fallback)
        total = len(conditions_df)
        if total == 0:
            return 0.0, 0.0, 0.0
        return (
            round(conditions_df.filter(pl.col(cci_col) >= good_threshold).height / total * 100, 2),
            round(conditions_df.filter(
                (pl.col(cci_col) >= poor_threshold) & (pl.col(cci_col) < good_threshold)
            ).height / total * 100, 2),
            round(conditions_df.filter(pl.col(cci_col) < poor_threshold).height / total * 100, 2),
        )
```

#### `_apply_treatment_resets_polars` (lines 130-216)

**Current:** Joins `reset_iri`, `reset_rut`, `reset_crack`, `reset_faulting` from treatments_df and overwrites raw measurement columns. Resets age to 0.

**New:** Loads resets from `treatment_resets` table, applies per-index resets, computes equivalent ages.

```python
def _apply_treatment_resets_polars(
    conditions_df: pl.DataFrame,
    selected_df: pl.DataFrame,
    resets_df: pl.DataFrame,
) -> pl.DataFrame:
    """
    Apply index-based treatment resets to treated segments.

    Reset modes:
      ADDITIVE: new_value = MIN(current + delta, 5.0)
      ABSOLUTE: new_value = MAX(delta, current)  (only improve)
      HOLD:     no change to index value, but freeze the age

    After index resets, compute equivalent ages for each changed index.

    Args:
        conditions_df: Current conditions with:
            current_psi, current_rdi, current_sci, current_eci, current_jci, current_csi,
            current_cci, age_psi, age_rdi, age_sci, age_eci, age_jci, age_csi
        selected_df: Selected treatments (analysis_segment_id, treatment_id)
        resets_df: Reset rules (treatment_id, variable, reset_mode, reset_delta)

    Returns:
        Updated conditions DataFrame
    """
```

**Implementation sketch:**

```python
# Pivot resets_df from long to wide: one row per treatment_id
# Columns: treatment_id, psi_mode, psi_delta, rdi_mode, rdi_delta, ...
# (Use polars pivot or manual aggregation)

# For each index variable:
INDEX_VARS = ["psi", "rdi", "sci", "eci", "jci", "csi", "cci"]

for idx in INDEX_VARS:
    current_col = f"current_{idx}"
    mode_col = f"{idx}_mode"
    delta_col = f"{idx}_delta"
    age_col = f"age_{idx}"

    # ADDITIVE:
    result = result.with_columns(
        pl.when(pl.col(mode_col) == "ADDITIVE")
        .then((pl.col(current_col) + pl.col(delta_col)).clip(0.0, 5.0))
        .when(pl.col(mode_col) == "ABSOLUTE")
        .then(pl.max_horizontal(pl.col(current_col), pl.col(delta_col)).clip(0.0, 5.0))
        .when(pl.col(mode_col) == "HOLD")
        .then(pl.col(current_col))  # no change
        .otherwise(pl.col(current_col))
        .alias(current_col)
    )

    # For ADDITIVE and ABSOLUTE: compute equivalent age from new value
    # For HOLD: keep current age (don't advance in next step)
    # For treatments with no reset on this index: age advances normally

# Recompute CCI after all index resets
result = result.with_columns(
    pl.when(pl.col("pavement_type") == "RC")
    .then(pl.min_horizontal("current_psi", "current_csi", "current_jci"))
    .otherwise(pl.min_horizontal("current_psi", "current_rdi", "current_sci"))
    .alias("current_cci")
)
```

#### `_advance_deterioration_polars` (lines 219-279)

**Current:** Calls `project_deterioration_polars` which projects raw values.

**New:** Calls the rewritten `project_deterioration_polars` which projects indices. The structure is the same, but the columns are different.

```python
def _advance_deterioration_polars(
    conditions_df: pl.DataFrame,
    years_to_advance: int = 1,
) -> pl.DataFrame:
    """
    Advance deterioration for all segments by specified years.

    Increments each index age by years_to_advance, then recomputes
    index values from the deterioration curves.
    """
    # Increment ages
    for idx in ["psi", "rdi", "sci", "eci", "jci", "csi"]:
        age_col = f"age_{idx}"
        if age_col in conditions_df.columns:
            conditions_df = conditions_df.with_columns(
                (pl.col(age_col) + years_to_advance).alias(age_col)
            )

    # Project indices at new ages using family params
    projected = project_deterioration_polars(
        conditions_df,
        analysis_years=0,  # Just compute current year at new ages
    )

    # Update current index columns from projected values
    # ...
```

#### `_prepare_strategies_for_optimization` (lines 282-413)

**Column reference changes:**
- `"current_iri"` -> not used directly; conditions are in index columns
- `"pci_benefit"` -> `"cci_benefit"` in the rename at line 399
- The trigger condition mapping (lines 316-321) is no longer needed since triggers operate on index columns directly
- Do-nothing strategy creation (lines 403-408) is unchanged

#### `aggregate_segments_to_joints` (lines 416-510)

**Column reference changes in aggregation expressions:**
- Replace `current_iri`, `current_rut`, `current_crack` weighted averages with `current_psi`, `current_rdi`, `current_sci`, `current_eci`, `current_jci`, `current_csi` weighted averages
- Add `current_cci` aggregation (length-weighted average)
- Add per-index age aggregations (take first or max)
- Add `pavement_type` (take first)


### 4.8 `engine/db.py` (MODIFY)

#### `load_analysis_segments_df` (lines 381-478)

**Add new columns to the SELECT query:**

```python
query = """
    SELECT
        analysis_segment_id, route_id, begin_mp, end_mp,
        length_miles, lanes, surface_type, pavement_type,
        -- Raw measurements (kept for reference and PSI/RDI computation)
        current_iri, current_rut, current_crack, current_faulting,
        -- Condition indices
        current_psi, current_rdi, current_sci, current_cci,
        current_eci, current_jci, current_csi,
        -- Per-index ages
        age_psi, age_rdi, age_sci, age_eci, age_jci, age_csi,
        -- Other
        aadt, lrs_aadt, family_id, current_age, joint_id,
        district, district_code, district_desc,
        county_code, county_desc, nhs_code, nhs_desc,
        functional_class, functional_class_desc,
        route_status, route_status_desc
    FROM analysis_segments
    ORDER BY route_id, begin_mp
"""
```

**Add cast expressions for new columns:**

```python
df = df.with_columns([
    # ... existing casts ...
    pl.col("current_psi").cast(pl.Float64),
    pl.col("current_rdi").cast(pl.Float64),
    pl.col("current_sci").cast(pl.Float64),
    pl.col("current_cci").cast(pl.Float64),
    pl.col("current_eci").cast(pl.Float64),
    pl.col("current_jci").cast(pl.Float64),
    pl.col("current_csi").cast(pl.Float64),
    pl.col("age_psi").cast(pl.Int32),
    pl.col("age_rdi").cast(pl.Int32),
    pl.col("age_sci").cast(pl.Int32),
    pl.col("age_eci").cast(pl.Int32),
    pl.col("age_jci").cast(pl.Int32),
    pl.col("age_csi").cast(pl.Int32),
])
```

**Add fallback computation if index columns are null:**

```python
# After loading, compute PSI/RDI from raw measurements if indices are null
from engine.condition.indices import calculate_psi_vectorized, calculate_rdi_vectorized

if "current_psi" in df.columns:
    df = df.with_columns(
        pl.when(pl.col("current_psi").is_null() & pl.col("current_iri").is_not_null())
        .then(calculate_psi_vectorized(pl.col("current_iri")))
        .otherwise(pl.col("current_psi"))
        .alias("current_psi")
    )
```

#### NEW: `load_trigger_lookup_df`

```python
def load_trigger_lookup_df(
    engine: Optional[Engine] = None,
) -> pl.DataFrame:
    """
    Load treatment trigger lookup table.

    Returns DataFrame with columns:
        trigger_key, treatment_id, trigger_branch, pavement_type,
        psi_lower, psi_upper, rdi_lower, rdi_upper,
        sci_lower, sci_upper, csi_lower, csi_upper,
        eci_lower, eci_upper, jci_lower, jci_upper,
        min_section_length, description
    """
    if engine is None:
        engine = get_engine()

    query = """
        SELECT
            trigger_key, treatment_id, trigger_branch, pavement_type,
            psi_lower, psi_upper, rdi_lower, rdi_upper,
            sci_lower, sci_upper, csi_lower, csi_upper,
            eci_lower, eci_upper, jci_lower, jci_upper,
            min_section_length, description
        FROM treatment_triggers
        ORDER BY treatment_id, trigger_branch
    """

    with engine.connect() as conn:
        result = conn.execute(text(query))
        rows = result.fetchall()
        columns = list(result.keys())

    if not rows:
        logger.warning("No trigger lookup rows found in database")
        return pl.DataFrame()

    data = {col: [row[i] for row in rows] for i, col in enumerate(columns)}
    df = pl.DataFrame(data)

    # Cast numeric columns
    numeric_cols = [
        "psi_lower", "psi_upper", "rdi_lower", "rdi_upper",
        "sci_lower", "sci_upper", "csi_lower", "csi_upper",
        "eci_lower", "eci_upper", "jci_lower", "jci_upper",
        "min_section_length",
    ]
    df = df.with_columns([
        pl.col(c).cast(pl.Float64) for c in numeric_cols
    ])

    logger.info(f"Loaded {len(df)} trigger lookup rows from database")
    return df
```

#### NEW: `load_treatment_costs_lookup_df`

```python
def load_treatment_costs_lookup_df(
    engine: Optional[Engine] = None,
) -> pl.DataFrame:
    """
    Load treatment costs by pavement type.

    Returns DataFrame with columns:
        treatment_id, pavement_type, cost_per_lane_mile
    """
    if engine is None:
        engine = get_engine()

    query = """
        SELECT treatment_id, pavement_type, cost_per_lane_mile
        FROM treatment_costs_lookup
        ORDER BY treatment_id, pavement_type
    """

    with engine.connect() as conn:
        result = conn.execute(text(query))
        rows = result.fetchall()
        columns = list(result.keys())

    if not rows:
        logger.warning("No treatment cost lookup rows found")
        return pl.DataFrame()

    data = {col: [row[i] for row in rows] for i, col in enumerate(columns)}
    df = pl.DataFrame(data)
    df = df.with_columns(pl.col("cost_per_lane_mile").cast(pl.Float64))

    logger.info(f"Loaded {len(df)} treatment cost lookup rows from database")
    return df
```

#### `load_resets_df` (lines 245-297)

**Update to load from new `treatment_resets` table:**

```python
query = """
    SELECT treatment_id, variable, reset_mode, reset_delta
    FROM treatment_resets
    ORDER BY treatment_id, variable
"""
```

#### `load_treatments_with_resets_df` (lines 481-612)

**Complete rewrite.** Instead of computing raw-value resets from `ABSOLUTE`/`RELATIVE`/`PERCENTAGE`, this now loads index resets and pivots them to wide format:

```python
def load_treatments_with_resets_df(
    engine: Optional[Engine] = None,
    active_only: bool = True,
) -> pl.DataFrame:
    """
    Load treatments with index reset rules pivoted to wide format.

    Returns DataFrame with columns:
        treatment_id, treatment_name, cost_per_lane_mile,
        psi_mode, psi_delta, rdi_mode, rdi_delta,
        sci_mode, sci_delta, eci_mode, eci_delta,
        jci_mode, jci_delta, csi_mode, csi_delta,
        cci_mode, cci_delta
    """
```

#### `load_pavement_families_df` (lines 615-666)

**Update query to SELECT from new schema:**

```python
query = """
    SELECT family_id, family_name, surface_type, pavement_type,
           functional_class, traffic_level,
           index_type, alpha, beta, initial_value, description
    FROM pavement_families
    ORDER BY family_id, index_type
"""
```


### 4.9 `engine/runner.py` (MODIFY)

#### Imports (lines 51-65)

```python
# OLD:
from engine.condition.pci import calculate_pci_polars

# NEW:
from engine.condition.indices import calculate_condition_indices_polars
```

#### `PipelineConfig` (lines 77-98)

Add CCI threshold configuration:

```python
@dataclass
class PipelineConfig:
    # ... existing fields ...
    cci_good_threshold: float = 3.5
    cci_poor_threshold: float = 2.5
    discount_rate: float = 0.04    # For present value (future use)
    inflation_rate: float = 0.02   # For present value (future use)
```

#### `PipelineResult` (lines 100-133)

Replace PCI references:

```python
@dataclass
class PipelineResult:
    # ... existing fields ...
    # REPLACE:
    # initial_pct_good: float (was based on PCI >= 80)
    # final_pct_good: float (was based on PCI >= 80)
    initial_pct_good: float = 0.0   # Now based on CCI >= 3.5
    final_pct_good: float = 0.0
    pct_good_change: float = 0.0
```

#### `validate_analysis_df` (lines 136-180)

**Update required/default columns:**

```python
defaults = {
    "family_id": "FAM-01",
    "surface_type": "ASP",
    "pavement_type": "BC",
    "current_psi": None,
    "current_rdi": None,
    "current_sci": 5.0,
    "current_eci": 5.0,
    "current_jci": 5.0,
    "current_csi": 5.0,
    "current_cci": None,
    "age_psi": 0,
    "age_rdi": 0,
    "age_sci": 0,
    "age_eci": 0,
    "age_jci": 0,
    "age_csi": 0,
    "current_age": 0,
    "length_miles": 1.0,
    "lanes": 2,
    "aadt": 5000,
    # Keep raw measurements as optional (for PSI/RDI computation)
    "current_iri": None,
    "current_rut": None,
}
```

#### `validate_treatments_df` (lines 183-221)

**Update default columns:**

```python
defaults = {
    "treatment_name": None,
    "cost": 0.0,
    # Old: "reset_iri", "reset_rut", "reset_crack"
    # New: reset data comes from resets_df, not columns on treatments_df
}
```

#### `run_optimization_pipeline` (lines 224-299)

**Step 2 change:**

```python
# OLD (lines 291-298):
# Step 2: Calculate current PCI if not present
if "pci_score" not in analysis_df.columns:
    pci_input = analysis_df.rename({...})
    pci_result = calculate_pci_polars(pci_input)
    analysis_df = pci_result.rename({...})

# NEW:
# Step 2: Calculate condition indices if not present
if "current_cci" not in analysis_df.columns or analysis_df["current_cci"].null_count() > 0:
    analysis_df = calculate_condition_indices_polars(analysis_df)
```

**Condition tracking throughout:**
- Replace all references to `pci_score` with `current_cci`
- Replace `gfp_rating` with `condition_category`


### 4.10 `engine/__init__.py` (MODIFY)

Add new imports:

```python
from engine.db import (
    # ... existing ...
    load_trigger_lookup_df,
    load_treatment_costs_lookup_df,
)

# Add condition indices module
from engine.condition.indices import (
    calculate_psi,
    calculate_rdi,
    calculate_cci,
    calculate_condition_indices_polars,
)
```

Update `__all__` list accordingly.


### 4.11 `engine/deterioration/families.py` (MODIFY)

Update `FAMILY_DEFINITIONS` to use index-based parameters instead of per-distress raw-value parameters. The family assignment logic (mapping surface_type + functional_class + traffic_level to family_id) remains the same.


### 4.12 `create_analysis_segments.py` (MODIFY)

When creating analysis segments from overlay operations:
- Compute `current_psi` from `current_iri` using the PSI formula
- Compute `current_rdi` from `current_rut` using the RDI formula
- Pull `current_sci`, `current_eci`, `current_jci`, `current_csi` from condition_history if available
- Compute `current_cci` from the applicable indices
- Set `pavement_type` from `surface_type`
- Initialize per-index ages from `current_age`


---

## 5. Performance Considerations

| Operation | Current (raw measurements) | New (condition indices) | Assessment |
|-----------|---------------------------|------------------------|------------|
| **Index computation** | Piecewise linear deduction curves (4 branches per distress, 4 distress types) | `5*exp(-0.0041*IRI)` and `5-6.65*rut^1.41` | **FASTER** -- simpler math, fewer conditionals |
| **CCI vs PCI** | Weighted sum of deductions | MIN of 3 indices | **FASTER** -- one `min_horizontal` vs multiply-add |
| **Trigger evaluation** | Variable-length eligibility groups, AND/OR grouping, veto evaluation, pivot from long format | 6 range checks per branch, cross-join + filter | **FASTER** -- simpler logic, no pivot needed |
| **Deterioration projection** | Power function on 3-4 raw values | Power function on 4-6 indices | **COMPARABLE** -- same math, slightly more columns |
| **AUC integration** | Trapezoidal on PCI curve | Trapezoidal on CCI curve | **IDENTICAL** |
| **IBC optimization** | Greedy selection on benefit/cost | Greedy selection on benefit/cost | **IDENTICAL** |
| **Memory** | 4 raw values + 1 PCI per segment per year | 6 indices + 1 CCI per segment per year | **SLIGHTLY MORE** (~2x per-year columns) |

**Expected overall performance: EQUAL OR BETTER than the current system.** The main speedup comes from simpler trigger evaluation and simpler condition scoring. The slight memory increase from more index columns is negligible for typical network sizes (5,000-50,000 segments).


---

## 6. What We Lose / Tradeoffs

### 6.1 SCI Cannot Be Computed from `crack_percent` Alone

The current system computes crack deductions directly from `crack_percent`. In the dTIMS model, SCI (Structural Cracking Index) is derived from a detailed distress survey that considers crack type, severity, and extent -- it cannot be computed from a single percentage.

**Mitigation:** When SCI is unavailable from survey:
- Default SCI to 5.0 (optimistic -- assumes no structural cracking)
- CCI will be governed by PSI and RDI only, which can be computed from IRI and rut
- Flag segments with defaulted SCI so analysts know the index is not from survey data

### 6.2 ECI, JCI, CSI Availability

These indices are only meaningful for specific surface types:
- ECI (Edge Condition Index): asphalt only, from survey
- JCI (Joint Condition Index): concrete only, from survey
- CSI (Cracking Severity Index): concrete only, from survey

When unavailable, they are set to 5.0 (non-applicable for that surface type). This means triggers referencing those indices will use the "always pass" range for non-applicable types.

### 6.3 Loss of Veto Mechanism Granularity

The current system supports veto conditions that hard-exclude treatments regardless of eligibility windows. The dTIMS trigger model uses only positive eligibility windows (6-index ranges) with OR between branches.

**Mitigation:** If a veto-like exclusion is needed, encode it as a tighter upper bound on the relevant index in all branches. For example, to exclude Chip Seal when structural condition is very poor, set `sci_lower = 2.0` in all Chip Seal branches.

### 6.4 Loss of Direct Raw-Measurement Triggers

The current system can trigger on `aadt`, `age_years`, and `structural_flag` in addition to condition measurements. The new trigger model uses only the 6 condition indices.

**Mitigation:** AADT and age-based differentiation moves to the family assignment (different families = different deterioration rates = different trigger eligibility). The `structural_flag` concept is absorbed into the SCI index.

### 6.5 Benefit Scale Change

Benefits change from PCI-years (0-100 scale) to CCI-years (0-5 scale). Benefit values will be ~20x smaller in absolute terms. This does not affect optimization (B/C ratios scale proportionally) but will require updating any hardcoded benefit thresholds or report formatting.


---

## 7. Migration Checklist

The tasks below are ordered by dependency. Tasks at the same level can be parallelized.

### Phase 1: Database Schema (no code changes yet)

- [x] **1.1** Run `ALTER TABLE` statements on `analysis_segments` to add index columns (Section 2.1) -- *in `db/migration_to_dtims.sql`*
- [x] **1.2** Run `ALTER TABLE` on `condition_history` to add `eci`, `jci`, `csi` (Section 2.7)
- [x] **1.3** Rename legacy tables: `treatment_triggers` -> `treatment_triggers_legacy`, `treatment_resets` -> `treatment_resets_legacy`, `pavement_families` -> `pavement_families_legacy`
- [x] **1.4** Create new `treatment_triggers` table (Section 2.3)
- [x] **1.5** Create new `treatment_resets` table (Section 2.4)
- [x] **1.6** Create new `pavement_families` table (Section 2.5)
- [x] **1.7** Create new `treatment_costs_lookup` table (Section 2.6)
- [x] **1.8** Add new columns to `treatments` table (Section 2.2)

> All Phase 1 SQL is in `db/migration_to_dtims.sql` — run with `psql -f db/migration_to_dtims.sql`

### Phase 2: Data Population (depends on Phase 1)

- [x] **2.1** Populate `pavement_type` on `analysis_segments` from `surface_type`
- [x] **2.2** Populate `current_psi`, `current_rdi` from raw measurements
- [x] **2.3** Default `current_sci`, `current_eci`, `current_jci`, `current_csi` to 5.0 where null
- [x] **2.4** Compute and populate `current_cci`
- [x] **2.5** Initialize per-index age columns from `current_age`
- [x] **2.6** Mark existing treatments as `active = FALSE`
- [x] **2.7** Insert 14 new treatments (Section 3.1)
- [x] **2.8** Insert 20 trigger lookup rows (Section 3.2) -- **revisit thresholds when dTIMS data available**
- [x] **2.9** Insert treatment reset rules (Section 3.3)
- [x] **2.10** Insert treatment cost lookup (Section 3.4) -- **placeholder values pending dTIMS cost table**

> All Phase 2 data is in `db/migration_to_dtims.sql` (same transaction as Phase 1)

### Phase 3: Core Engine Code (depends on Phase 2 for testing, but code changes can start in parallel)

- [x] **3.1** Create `engine/condition/indices.py` — scalar + vectorized PSI, RDI, CCI; `calculate_condition_indices_polars()`
- [x] **3.2** Rewrite `engine/deterioration/models.py` — `IndexDeteriorationParams`, `calculate_index_at_age()`, `compute_equivalent_age()`, 8-family `DEFAULT_FAMILY_PARAMS`, rewritten `project_deterioration_polars()`, new `advance_conditions_one_year()`
- [x] **3.3** Rewrite `engine/treatments/triggers.py` — `TriggerBranch` dataclass, 6-index window `evaluate_triggers_polars()` with branch OR logic
- [x] **3.4** Rewrite `engine/benefits/auc.py` — CCI-based `CurveData`/`BenefitResult`, `calculate_benefits_polars()` with ADDITIVE/ABSOLUTE/HOLD reset support
- [x] **3.5** Update `engine/benefits/weighting.py` — column priority `cci_benefit` first, docstring updates

> All Phase 3 code is written and passes integration tests.

### Phase 4: Database Layer + Orchestrator (depends on Phase 3)

- [x] **4.1** Update `engine/db.py` — `load_triggers_df()` for 6-index columns, `load_resets_df()` for ADDITIVE/ABSOLUTE/HOLD, `load_analysis_segments_df()` with +7 index cols, +6 age cols, +pavement_type
- [x] **4.2** Update `engine/runner.py` — imports, `validate_analysis_df()`, CCI-based network condition
- [x] **4.3** Update `engine/__init__.py` — new exports, v1.0.0
- [x] **4.4** Update `engine/condition/__init__.py` — index exports
- [x] **4.5** Update `engine/deterioration/__init__.py` — new model exports
- [x] **4.6** Update `engine/deterioration/families.py` — `IndexDeteriorationParams` import alias
- [x] **4.7** Update `engine/treatments/__init__.py` — new trigger exports
- [x] **4.8** Update `engine/benefits/__init__.py` — new AUC exports
- [x] **4.9** Update `engine/optimization/work_program.py` — `_apply_treatment_resets_polars` (ADDITIVE/ABSOLUTE/HOLD on indices), `_advance_deterioration_polars` (uses `advance_conditions_one_year`), `_prepare_strategies_for_optimization` (passes `resets_df`), `aggregate_segments_to_joints` (index-weighted aggregation), `generate_work_program_polars` (accepts `resets_df`). GFP kept on PCI via `derive_pci_from_indices_polars()` back-calculation.
- [x] **4.10** Update `engine/optimization/scenarios.py` — `ScenarioParameters` gains `triggers_df`/`resets_df`, threaded through all 3 `generate_work_program_polars` call sites
- [x] **4.11** `engine/optimization/chunked.py` — fully migrated: `aggregate_segments_to_joints` uses index-weighted averages, `_calculate_benefits_for_chunk` delegates to CCI-based `calculate_benefits_polars`, `prepare_strategies_chunked` uses 6-index triggers + `resets_df`, `generate_work_program_chunked` accepts `resets_df` + derives PCI from indices for GFP

### Phase 5: Supporting Code (depends on Phase 4)

- [x] **5.1** Update `scripts/run_optimization.py` — switched from `generate_work_program_chunked` to `generate_work_program_polars`, updated trigger display (6-index windows), reset display (ADDITIVE/ABSOLUTE/HOLD), family display (per-index params), removed `load_treatments_with_resets_df` dependency
- [ ] **5.2** Modify `create_analysis_segments.py`: compute and populate index columns during overlay
- [ ] **5.3** Update `engine/exports.py` (if applicable): column names in Excel/report output

### Phase 6: Testing and Validation

- [x] **6.1** Integration test: scalar PSI/RDI/CCI formulas verified against database (398K records)
- [x] **6.2** Integration test: vectorized index calculation, deterioration projection, trigger evaluation, advance_conditions — all pass
- [ ] **6.3** Unit tests for trigger evaluation: verify 20 trigger rows produce expected eligibility for sample segments
- [ ] **6.4** Integration test: run full pipeline on a small subset (100 segments) and verify work program structure
- [ ] **6.5** Regression comparison: run both old and new engines on the same network, compare treatment selections and network condition trajectories
- [ ] **6.6** Performance benchmark: verify < 5 minute runtime target for 5,000 joints x 20 years

### Phase 7: Calibration (ongoing, after code is functional)

- [ ] **7.1** Calibrate deterioration curve alpha/beta values for each (family_id, index_type) pair from `condition_history` regressions
- [ ] **7.2** Validate trigger thresholds against actual `Analysis_Lookup_Triggers` table from dTIMS dump
- [ ] **7.3** Populate actual cost values from `Analysis_Lookup_Trt_Costs` table
- [ ] **7.4** Validate treatment reset magnitudes against dTIMS before/after data
- [ ] **7.5** Adjust CCI Good/Fair/Poor thresholds (3.5/2.5) based on WVDOT reporting requirements
