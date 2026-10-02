# Import Past Projects

Reference documentation for `scripts/import_past_projects.py` — the pipeline that loads historical pavement construction projects from the WVDOH Hub export into the PMS `projects` table.

---

## Source File

**`raw_pavements.xlsx`** — exported from the WVDOH Hub project management system. Contains one row per route-segment / project-phase / funding-line combination. A single physical segment can appear many times across multiple phases (Engineering, Right-of-Way, Construction) and multiple funding priorities within each phase.

The file has 112 columns organized into 10 groups: Route Segment Attributes, Project Attributes, Project Cost Estimates, Project Classification, Phase Attributes, Phase Funding, Participation Percentages, Obligation & Funding Flags, Federal & State Program Codes, and Federal Funding Detail. See `RAW_PAVEMENTS_COLUMNS.md` for full column documentation.

---

## Pipeline Steps

### Step 1 — Filter to Construction Phases

```
PhaseType == 'Construction'
```

The source file contains all project phases: Engineering (`EN0001`), Right-of-Way (`RW0001`), and Construction (`CN0001`, `CN0002`, `CN0003`). Only Construction phases represent actual treatments applied to pavement. Engineering and Right-of-Way are project overhead.

### Step 2 — Exclude Non-Treatment Categories

```
TAMPReportingCategory not in ('Initial Construction (New Road)', 'Routine Maintenance')
```

Two TAMP categories are excluded:

- **Initial Construction (New Road)** — new road construction, not a treatment on existing pavement. These segments have no prior condition to compare against.
- **Routine Maintenance** — minor activities (pothole patching, crack filling at maintenance level) that don't constitute a formal treatment in the PMS sense.

The remaining categories that pass through:
- Preservation & Preventative Maintenance
- Rehabilitation
- Replacement or Reconstruction

### Step 3 — Filter to Closed Phases Only

```
PhaseStatus == 'Closed'
```

Only completed work is imported. The four possible statuses in the source data are:

| Status | Meaning | Included? |
|--------|---------|-----------|
| Closed | Work completed | Yes |
| Open | Work in progress or planned | No |
| Withdrawn | Cancelled before completion | No |
| Terminated | Stopped before completion | No |

This is a critical filter. The PMS `projects` table also holds future/active projects (status = `planned`, `designed`, `awarded`, `in_progress`) that feed into the optimizer via `populate_committed_flags.py`. Importing historical projects as `CLOSED` keeps them separate — the optimizer ignores `CLOSED` records entirely.

### Step 4 — Deduplicate to One Row per Segment

A segment (`RouteSegment_Id`) can have multiple closed construction phases (e.g. `CN0001` completed in 2019, `CN0002` completed in 2023). We keep only the **most recent** closed phase:

1. Sort by `PhaseEndDate` descending (most recent first)
2. Drop duplicates on `RouteSegment_Id`, keeping the first (most recent) row

This gives us the last treatment applied to each segment, which is what matters for historical analysis and cost benchmarking.

### Step 5 — Compute Segment Length

```
Segment_Length = abs(EndMilePoint - StartMilepoint)
```

Recomputed from the raw milepoints rather than trusting the `Segment_Length` field in the source data, which can be stale, zero, or inconsistent with the milepoints.

### Step 6 — Distribute Project Cost to Segments

The source file has project-level cost estimates across four categories:

| Field | Description |
|-------|-------------|
| `EngEstimatedCost` | Engineering cost (~86% null) |
| `RowEstimatedCost` | Right-of-way cost (~98% null) |
| `ConEstimatedCost` | Construction cost (~48% null) |
| `OthEstimatedCost` | Other costs (~53% null) |

Since one project can span multiple segments, we need to allocate the total project cost down to each segment. The formula:

```
total_project_cost = sum of all four cost columns (nulls treated as 0)

segment_cost = total_project_cost * (segment_length / project_total_length)
```

If all segments in a project have zero length (rare — 3 segments in the dataset), the cost is distributed evenly across segments instead.

### Step 7 — Map Construction Codes to Treatment IDs

The Hub uses `ConstructionCode_Name` (17 unique values) to describe what was done. The PMS uses `treatment_id` from the `treatments` table. Each construction code maps **1:1** to exactly one treatment — no conflation or grouping.

The mapping is validated at runtime: only treatment_ids that exist in the database with `active = TRUE` are used. If a treatment is deactivated, segments mapped to it will get a null `treatment_id`.

#### Preservation Treatments

| ConstructionCode_Name | treatment_id |
|----------------------|--------------|
| Micro Surfacing | MICROSURFACING |
| HFST - High Friction Surface Treatment | CHIP_SEAL |
| Pave (Surface Treatment) | CHIP_SEAL |
| Resurface (Surface Treatment) | CAPE_SEAL |
| Ultra Thin HMA O/L < 1.5" | ULTRA_THIN_OVLY |

#### Rehabilitation Treatments

| ConstructionCode_Name | treatment_id |
|----------------------|--------------|
| Minor HMA O/L 1.5"-2" | THIN_OVERLAY |
| Major HMA O/L > 2" | THICK_OVERLAY |
| Major Diamond Grinding with Concrete Pavement Rehab | MAJOR_CPR_DG |
| Cold In Place Recycling (CIR) | PRESERVATION_RC |
| Reinforce Base | PRESERVATION_BC |
| Remove Overlay(s) | MINOR_CPR_DG |

#### Reconstruction Treatments

| ConstructionCode_Name | treatment_id |
|----------------------|--------------|
| Reconst/Upgrade on Exist Align | RECONSTRUCT_RC |
| Pave (HMA or PCC) on existing road | RECONSTRUCT_BC |
| Add Travel Lane(s) | RECONSTRUCT_RC |
| Add Auxiliary Lanes (Truck, climbing, passing) | RECONSTRUCT_RC |
| Add Auxiliary Lanes (Turning, storage) | RECONSTRUCT_RC |
| Widen Roadway (minor widening...) | RECONSTRUCT_RC |

### Step 8 — Compute Completion Date

Best available date for when the work was actually completed, using a fallback chain:

1. **PhaseEndDate** — preferred. For closed phases this is the actual completion date.
2. **ConstructionStartDate** — fallback if PhaseEndDate is null.
3. **PhaseStartDate** — last resort.

The `construction_year` field in the output is derived from this date's year.

### Step 9 — Load into Database

The load is **idempotent** — safe to re-run at any time:

1. **Delete** all existing rows where `status = 'CLOSED'`
2. **Insert** all rows from the import via bulk `execute_values`

Each row maps to the `projects` table as follows:

| projects column | Source |
|----------------|--------|
| `hub_id` | `Project_Id` (integer FK back to Hub) |
| `project_name` | `ProjectName` |
| `route_id` | `RouteIdStr` (composite route identifier) |
| `bmp` | `StartMilepoint` |
| `emp` | `EndMilePoint` |
| `length_mi` | Computed `Segment_Length` |
| `treatment_id` | Mapped from `ConstructionCode_Name` |
| `estimated_cost` | Computed `SegmentEstimatedCost` |
| `funding_source` | `Allocation` |
| `construction_year` | Year from `ProjectCompletionDate` |
| `completion_date` | `ProjectCompletionDate` |
| `status` | Always `'CLOSED'` |

---

## Interaction with the Optimizer

The optimizer's committed-project mechanism (`scripts/populate_committed_flags.py`) reads from the `projects` table to lock segments into pre-planned treatments. It only considers projects with status in:

```
('planned', 'designed', 'awarded', 'in_progress')
```

Since this import script sets all records to `status = 'CLOSED'`, the imported historical projects are **invisible to the optimizer**. They exist purely as reference data for:

- Historical treatment distribution analysis
- Cost benchmarking (actual vs. estimated)
- Treatment frequency tracking per route/district
- Network-level investment trend analysis

---

## Output Files

| File | Location | Contents |
|------|----------|----------|
| `raw_pavements_deduped.xlsx` | `scripts/` | Full deduped DataFrame with all 112 source columns plus computed fields, for manual inspection |
| `projects` table | PostgreSQL | Subset of fields loaded into the DB (see column mapping above) |

---

## Usage

```bash
python scripts/import_past_projects.py
```

### Prerequisites

- `raw_pavements.xlsx` in the project root
- `.env` with `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
- Active treatments loaded in the `treatments` table (the script queries `treatments WHERE active = TRUE` to validate the mapping)

### Expected Output

```
Imported 4028 segments (4028 closed, 0 not closed)
Saved to /path/to/scripts/raw_pavements_deduped.xlsx
Deleted 4028 CLOSED projects
Inserted 4028 projects
Done
```

---

## Data Quality Notes

- **Pre-2019 records** have no cost estimates (all four cost columns are null). These segments get `SegmentEstimatedCost = 0`.
- **3 segments** have zero-length milepoints (BMP == EMP). Their costs are distributed evenly within their project rather than by length ratio.
- The `RouteIdStr` values in the Hub export do not always match `route_id` values in the PMS `routes` table. The `route_id` foreign key constraint on `projects` was dropped to accommodate this mismatch.
