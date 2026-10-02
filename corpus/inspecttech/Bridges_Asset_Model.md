# The InspectTech Asset Object — Complete Reference

> **Imported from the inspect_tech repo** (`ASSET_MODEL.md`) on 2026-09-25. File paths and
> commands below are that repo's. In PMS the AssetWise pipeline is
> `python -m pipeline bridges …` (`pipeline/bridges/`), the cost model is
> `scripts/bridges/cost_model/`, the saved API probes are in
> `bridges/analysis_reference/`, and the inventory is `INSPECT_DB`
> (`bridges_all.duckdb`). Other bridge reports: see **Documents → Bridges**.

Deep research write-up of what an "Asset" actually is in Bentley AssetWise Inspections (InspectTech) on the WVDOT tenant — how inspections, sub-assets, elements, values, schedules, and attachments all hang off it. Companion to the [AssetWise Extract Reference](/docs/Bridges_AssetWise_Reference) (`DOCUMENTATION.md`) which covers the API/dumper/webapp at a higher level; this document drills into the data model.

Source data probed (raw responses in `analysis/asset_probes/`):
- `/api/Asset/{id}` (full row, plus by-GUID and by-name variants)
- `/api/AssetType/{id}`, `/api/AssetStatus` (lookup catalogs)
- `/api/StructureElement/GetSubAssets/{as_id}` (the sub-asset roster)
- `/odata/Assets` (with AssetDefinition filters), `/odata/AssetTasks`, `/odata/AssetElements`, `/odata/AssetValues`, `/odata/AssetViewTree`
- `/api/AssetInspectionTypeSchedule/*`, `/api/AssetActivityTypeSchedule/*`
- `/api/AssetFile/*`, `/api/AssetFilesReportMap/*`
- `/api/InspectionReport/GetMostRecentReportsForAsset`, `/api/InspectionReport/Download`

---

## 1. Concept — the Asset is the universal node

In InspectTech, almost everything that has a name, an ID, and a permission scope is an **Asset**. Bridges, tunnels, asset views, district groupings, individual spans, abutments, piers, element instances (each Elastomeric Bearing), and even defect observations (each *Cracking* observation) are all rows in the same `Asset` table, distinguished by an enum.

There are **~16,403 rows visible in `/odata/Assets`** on this tenant when no filter is applied, but only **8,686 of those are real, leaf, non-deleted Bridges**. The rest are: parent groupings ("WVDOT Assets", "District 1"…"District 10", "Asset Views", "DISTHELP", "Toll Road", and similar), asset views (saved cross-cuts), summary roll-ups, and the deleted/archived bridges.

Sub-assets (spans, abutments, piers, element instances, defects) are **not** in `/odata/Assets`. They live in the same physical table but are filtered out of that endpoint. To see them, call `/api/StructureElement/GetSubAssets/{as_id}` — that returns the sub-assets *for* a bridge.

So when you say "Asset", you need to be specific about which slice you mean:

| You mean… | Filter |
|---|---|
| One real bridge | `AssetTypeId=1 AND IsAssetParent=false AND IsAssetView=false AND IsDeleted=false` |
| The tree-level groupings | `IsAssetParent=true` (17 of these on this tenant) |
| Asset views (saved filters) | `IsAssetView=true` (2 of these) |
| Sub-asset groups (Abutment N, Span N, Pier N) | `/api/StructureElement/GetSubAssets/{bridgeAsId}` where `as_asset_def=3` |
| Element instances (each MBEI element) | same call, `as_asset_def=2`, has `as_code` = AASHTO element code |

---

## 2. The Asset row — every column, what it means

Single source: `GET /api/Asset/{as_id}` on bridge 02A021 (as_id=42998):

```json
{
  "as_id": 42998,
  "as_name": "02A021",
  "as_code": "02A021",
  "as_guid": "573b366b-b33a-4643-8a76-c10caa7f929c",
  "rt_id": 3,
  "as_parent_id": null,
  "as_parent": null,
  "as_asset_def": 0,
  "coordinates": null,
  "as_root": false,
  "as_deleted": false,
  "at_id": 1,
  "as_child_rt_id": 1,
  "as_child_at_id": null,
  "as_summary": false,
  "as_is_asset_view": false,
  "asset_status_id": 0,
  "as_corridor": false,
  "as_last_snapshot_date": null,
  "as_is_internal": false,
  "as_sub_asset_parent": true,
  "as_last_update_date": "2026-01-28T16:41:54.337",
  "as_default_file_set_date": null,
  "as_stage_pontis": false,
  "as_federal_submission_type": 0,
  "asset_segment_map": null,
  "corridor": null,
  "as_created_date": null,
  "as_created_by_in_id": null,
  "childCount": null
}
```

Field map:

| Field | Type | Meaning |
|---|---|---|
| `as_id` | int | **Primary key.** Unique across bridges, sub-asset groups, element instances, defect observations, and views — they all share the same `as_id` space. |
| `as_name` | string | Display name. For bridges = the BARS number ("02A021"). For sub-asset groups = "Abutment 1", "Span 1", … For element instances = the AASHTO element name ("Elastomeric Bearing"). |
| `as_code` | string | Same as name for bridges. For element instances = the **AASHTO element ID** as a string ("310"). For tree groupings = same as name. |
| `as_guid` | uuid | Stable cross-system identifier. Used for the mobile-sync round-trip. |
| `rt_id` | int | Default `ReportType` for inspections on this asset. `1` = WVDOT Standard (legacy), `3` = WVDOH Report (modern). Null for sub-asset groups and element instances. |
| `as_parent_id` | int? | Parent in the **bridge tree** (District → bridge), not the sub-asset hierarchy. Real bridges typically have null here on this tenant; the parent relationship is captured via `AssetViewTree` instead. |
| `as_asset_def` | enum | What KIND of asset this is. See §3. |
| `as_root` | bool | True only for the topmost root asset of the tenant. |
| `as_deleted` | bool | Soft-delete flag. Excluded by default in most queries. |
| `at_id` | int | `AssetType` — `1` = Bridge, `2` = Test, `3` = Tunnel. Null on sub-asset groups/instances. |
| `as_child_rt_id` | int? | Default ReportType for *children* of this asset (e.g. if the asset is a District, children are bridges → rt_id=1=WVDOT Standard). |
| `as_child_at_id` | int? | Default AssetType for children. |
| `as_summary` | bool | True for summary-roll-up assets. Excluded from most reports. |
| `as_is_asset_view` | bool | True for saved-search "Asset Views". |
| `asset_status_id` | int | Foreign key to `AssetStatus`. `0` = Archived, `1` = In Service. See §4. Note: the asset_status_id values on this tenant are **0 and 1**, while in our SQLite dump the `status` column stores the *name* ("Archived" / "In Service") because that's how `/odata/Assets` returns it. |
| `as_corridor` | bool | True if this asset is a Corridor (a linear collection of bridges). |
| `as_is_internal` | bool | Internal-only assets (test/staging). |
| `as_sub_asset_parent` | bool | **True if this asset has sub-assets attached.** Real bridges that have element-level data captured have this `true`. So do the sub-asset groups (Abutment 1, Span 1) because they themselves are parents of element-instance assets. |
| `as_last_update_date` | datetime | Last write to the asset's metadata. |
| `as_last_snapshot_date` | datetime? | Last "Current Value" snapshot. |
| `as_default_file_set_date` | datetime? | Last reset of the default attachment set. |
| `as_stage_pontis` | bool | "Staged for Pontis" flag — whether this asset is queued for the FHWA Pontis export. |
| `as_federal_submission_type` | enum int | `0` = NotRequired, `1` = NationalBridge, `2` = NationalTunnel. Drives whether the row gets exported to FHWA. |
| `coordinates` | string? | "lat,lon" — usually null on the asset row itself; the real coordinates live in `AssetValue` (field 2300105 / 2300106 or NBI 16 / NBI 17 — see [AssetWise Extract Reference §5.3](/docs/Bridges_AssetWise_Reference#53-cross-generation-ratings--nbi-90-vs-snbi)). |
| `childCount` | int? | Hint count of children. Often null — populated lazily. |

The OData view (`/odata/Assets`) is a *denormalized* version of this row: it joins `AssetType.at_name`, `ReportType.rt_name`, `AssetStatus.asset_status_name`, then renames everything to PascalCase. The dumper's `asset` table preserves the OData column names — both views are isomorphic.

---

## 3. `AssetDefinition` enum — what KIND of asset

| Int | Enum string | Where you see it | Meaning |
|---:|---|---|---|
| 0 | `ReportableAsset` | `/odata/Assets` (default) | A real bridge, tunnel, or culvert. The unit on which inspections live. |
| 1 | (unobserved on this tenant) | — | Reserved. Possibly used on other tenants for non-reportable structural items. |
| 2 | (no enum string returned for sub-assets) | `/api/StructureElement/GetSubAssets/{id}` | **Sub-asset element instance** — a specific Elastomeric Bearing on this bridge, a specific Cracking observation. Carries `as_code` = AASHTO element id and `as_name` = element name. |
| 3 | (no enum string returned for sub-assets) | same call | **Sub-asset group** — a structural grouping. Names look like "Abutment 1", "Span 1", "Pier 2". One per structural unit of the bridge. |

The two un-named enum values (2, 3) only appear when you query a bridge's sub-assets; they don't show up in `/odata/Assets`.

`AssetDefinition` is what makes the "everything is an Asset" pattern usable: a defect observation is still an Asset row (with its own `as_id`, `as_guid`, last-updated timestamp) — but you filter for `as_asset_def=2` to find it.

---

## 4. `AssetType` and `AssetStatus` lookup tables

### AssetType (`/api/AssetType`)

```
at_id  at_name  default_rt_id  at_deck_length_fe_id  at_deck_width_fe_id  at_federal_submission_type
-----  -------  -------------  --------------------  -------------------  --------------------------
  1    Bridge   3              2004900 (NBI 49)      2005200 (NBI 52)     1 (NationalBridge)
  2    Test     ?              -                     -                    0
  3    Tunnel   ?              -                     -                    2 (NationalTunnel)
  4    ?
```

Only `Bridge` is meaningfully populated on this tenant (16,403 assets). The interesting bits on the AssetType row:

- `default_rt_id` → which ReportType new inspections of this asset type default to (Bridge → WVDOH Report).
- `at_deck_length_fe_id` and `at_deck_width_fe_id` → which `Field` IDs hold the canonical deck-length and deck-width values for this asset type. The web UI reads these for the Bridge Detail dashboard's geometry callouts. On this tenant: NBI 49 (Structure Length) and NBI 52 (Deck Width, Out-to-Out).
- `at_federal_submission_type` matches `as_federal_submission_type` semantics.

### AssetStatus (`/api/AssetStatus`)

```
asset_status_id  asset_status_name  hide_reports  exclude_query  exclude_search  is_default
0                Archived           true          true           true            false
1                In Service         false         false          false           true
```

Each status carries a sheaf of "exclude from X" booleans:

- `hide_reports` — don't render this asset's inspection reports
- `exclude_sum_rpt`, `exclude_query`, `exclude_fhwa` — drop from rollups, query exports, FHWA submission
- `excl_mgr_brdg_det`, `excl_col_brdg_det` — hide from manager/collector bridge-detail screens
- `excl_search` — hide from BARS search

So **`asset_status_id=0` (Archived)** is the system's way of saying "we used to maintain this bridge, but it's been demolished/decommissioned — keep the row for historical reference but exclude it from everything operational."

On bridges100.db: **92 In Service, 8 Archived** out of 100.

---

## 5. The Asset hierarchy — three independent trees

There are **three different "tree" relationships** rooted at the Asset row, and they don't share the same parent column. This is critical and easy to confuse.

### 5.1 The administrative / districting tree (via `IsAssetParent`)

```
WVDOT Assets (id=1, IsAssetParent=true)
├── District 1 (id=14791, IsAssetParent=true)
├── District 2 (id=15517, IsAssetParent=true)
├── …
├── District 10 (id=15525, IsAssetParent=true)
├── DISTHELP (id=62083, IsAssetParent=true)
├── Asset Views (id=50939, IsAssetView=true, IsAssetParent=true)
└── (others: Toll Road, etc.)
       └── thousands of real Bridges (IsAssetParent=false, leaves)
```

This is the navigation tree in the InspectTech UI's left sidebar. It's used for:

- Permission scoping (an inspector can be granted access to "all of District 5")
- Cross-cut roll-ups
- "Working set" definitions (which bridges show up in an inspector's mobile collector)

The membership is **not** captured on the bridge's `as_parent_id` (which is null for real bridges) — it's in the **`AssetViewTree`** odata entity. Each row of `AssetViewTree` is `(RootAssetId, ParentAssetId, AssetId)` — a flattened ancestor table.

### 5.2 The sub-asset / element tree (via `/StructureElement/GetSubAssets`)

```
Bridge (as_asset_def=0)
├── Sub-asset Group (as_asset_def=3, e.g. "Abutment 1")
│   ├── Sub-asset Instance/PhysicalElement (as_asset_def=2, "RC Abutment")
│   │   ├── Sub-asset Instance/Defect (as_asset_def=2, "Cracking")
│   │   ├── Sub-asset Instance/Defect (as_asset_def=2, "Efflorescence/Rust Staining")
│   │   └── …
│   └── Sub-asset Instance/ProtectiveSystem (as_asset_def=2, "Steel Protective Coating")
└── …
```

Real example — bridge 02A021 (as_id=42998), an arched 2-span concrete bridge:

- **5 sub-asset groups** (as_asset_def=3): Abutment 1, Span 1, Pier 1, Span 2, Abutment 2
- **135 sub-asset instances** (as_asset_def=2):
  - 14 PhysicalElement instances (RC Slab, RC Open Girder/Beam, RC Top Flange, Metal Bridge Railing, RC Abutment, RC Pier Wall, Elastomeric Bearing — multiple instances of each one for each span/abutment)
  - 115 Defect instances (Cracking, Spalling, Scour, Efflorescence, etc.)
  - 6 ProtectiveSystem instances (Wearing Surface, Steel Protective Coating)

The relationships (parent → child) are captured in the `AssetElement` table:
- `AssetId` = bridge as_id
- `SubAssetId` = the sub-asset's as_id (an element instance or group)
- `ParentSubAssetId` = the parent's as_id (a group, or another instance for defects)

The element-level inspection data (quantities in each Condition State 1–5) lives on the `AssetElement` row itself — see §7 below.

### 5.3 The corridor tree (via `as_corridor`)

If a bridge is part of a **Corridor** (a contiguous run of bridges along one route), `as_corridor=true` on the corridor parent and the corridor itself shows up in the `corridor` field of member bridges. Not heavily used on WVDOT — we observed `as_corridor=false` on all sample bridges.

---

## 6. AssetValue — the "current state" of every bridge cell (EAV)

The bridge's inventory and condition data is stored EAV-style in `AssetValue`. **6.1 million rows tenant-wide; ~750 rows per typical bridge** (sparse — only the fields meaningful to the bridge's report type).

```
AssetValue
  key:    (AssetId, FieldId, UserId)
  cols:   FieldName, FieldDataType, Value, PlainText, ReportId,
          UpdatedByUserId, UpdatedByUser, LastUpdatedDate,
          ChangeLocation, Guid
```

- `AssetId` = the bridge's as_id (note: NOT a sub-asset id — current values are aggregated to the bridge level).
- `FieldId` joins to the `Field` dictionary (11,884 rows on this tenant).
- `Value` is always a string; `FieldDataType` says how to interpret it (`String`, `Integer`, `Decimal`, `Date`, `Memo`, `Signature`).
- `PlainText` is the rich-text Memo fields stripped of HTML.
- `UserId` is the requesting user's id (the OData feed is scoped — composite-keyed on UserId).
- `ChangeLocation` = `online` | `mobile` | `import` etc.
- `LastUpdatedDate` = when this cell was last touched.
- `ReportId` = the ast_id of the inspection that produced the value (NOT the `Asset.rt_id`). Null = legacy/auto-populated.

**Why this matters:** every "field" you see on a bridge detail screen — from the Bridge Name down to the latest channel sounding — is a row in this table. The `Asset` row carries the identity and tree position; `AssetValue` carries the *data*.

When a new inspection is created with `ast_prepopulate=-1`, the system snapshots every relevant `AssetValue` cell into the inspection's `ReportValue` rows. When the inspection is approved (`it_can_update_cdv=true`), the updated `ReportValue` cells flow back into `AssetValue`, becoming the new current state.

---

## 7. AssetElement — element-level condition state

When an inspection is performed using AASHTO MBEI element-level methods (any modern WVDOH Report inspection), each element instance on the bridge gets a condition row.

```
AssetElement
  key:    (AssetId, SubAssetId, ParentSubAssetId, UserId)
  cols:   AssetName, ParentElementId, ParentElementName,
          ParentEnvironmentId, ElementId, ElementName,
          ElementEnvironmentId, ElementType, ElementSubmissionType,
          Classification, Unit, TotalQuantity,
          State1, State2, State3, State4, State5
```

Example — bridge 02A021's Elastomeric Bearing instance on Abutment 1:

```json
{
  "AssetId": 42998,
  "ParentSubAssetId": 60694,        // Abutment 1
  "SubAssetId":      60699,         // this bearing instance
  "AssetName": "02A021",
  "ElementId":   310,               // AASHTO 310 = Elastomeric Bearing
  "ElementName": "Elastomeric Bearing",
  "ElementType": "NationalBridge",
  "Classification": "PhysicalElement",  // also: Defect, ProtectiveSystem
  "Unit": "each",
  "TotalQuantity": 4,
  "State1": 4, "State2": 0, "State3": 0, "State4": 0, "State5": 0
}
```

Key invariants:
- **`State1 + State2 + State3 + State4 + State5 = TotalQuantity`** for any PhysicalElement row. Enforced by the system.
- **State 1 = Good, 2 = Fair, 3 = Poor, 4 = Severe** for the AASHTO 4-state. State 5 is reserved (rarely used).
- For `Classification='Defect'` rows, the parent (via `ParentSubAssetId`) is the PhysicalElement the defect was found on. `TotalQuantity` is the quantity *with* the defect; `State1` is therefore always 0.
- For `Classification='ProtectiveSystem'` rows, they hang off the parent like a defect, but `State1` represents quantity of working protection.

Distribution on bridge 02A021 (135 element rows):

| Classification | Count |
|---|---:|
| Defect | 115 |
| PhysicalElement | 14 |
| ProtectiveSystem | 6 |

Bridges with no element-level inspection (older bridges, simple stone arches) have zero rows here. Bridge 01A001 (Little Cove Run Arch) has zero `AssetElement` rows even though it has 9 inspections — its inspections rely entirely on `AssetValue` / `ReportValue` and NBI 58/59/60 ratings.

---

## 8. AssetTask — inspections, critical findings, work orders

`AssetTask` is the umbrella for anything that happens *to* an asset. On this tenant we see two `Type` values:

| Type | Count (sample) | What it represents |
|---|---:|---|
| `Report` | 67,000+ | An inspection report. PK `ast_id`. Drives the workflow, narratives, ReportValues, signatures, PDF render. |
| `WorkManagementInstance` | ~30 in a 1000-row sample | A critical-finding work order. Uses workflow `Critical Finding` with stages `CF Open` → `CF Review` → `CF Confirmed` → `CF Completed`. Carries no narratives or ReportValues. |

There's only **one** AssetTask schema, but the meaning of the columns varies by Type:

| Column | When Type=Report | When Type=WorkManagementInstance |
|---|---|---|
| `ast_inspection_date` | The field visit date | The date the finding was raised |
| `rt_id` | The report type (1=WVDOT Standard, 3=WVDOH Report) | -1 (no report) |
| `ast_current_wfs_id` | Inspection workflow stage (-1, -3, **-5**, -10, …) | Critical-finding stage (6=CF Completed, 7=Confirmed, 8=Open, 9=Review) |
| `ast_assigned_in_id` | The inspector | The engineer assigned to address the finding |

A critical finding is a way for an inspector to escalate "this bridge needs attention NOW" outside the regular inspection cycle. It gets its own task ID and workflow, often references a parent inspection via `ast_changed_by_ast_guid`.

Our dumper currently captures only Type=Report tasks (filters client-side). To add WorkManagementInstance support, the filter at `fetch_inspections_for_asset` would change from `r.get("Type") == "Report"` to `r.get("Type") in ("Report", "WorkManagementInstance")` and a new `task_type` column would distinguish them.

---

## 9. AssetFile — every photo, defect doc, and attachment

Each Asset can have any number of files attached. For an inspection-day photo set, files are also mapped to the inspection via `AssetFilesReportMap` so they print on the right page of the PDF.

### The two tables (in our SQLite schema):

```
asset_file
  key:    af_id
  cols:   af_guid, as_id, ft_id (file type),
          af_filename, af_extension, af_content_type, af_size,
          af_subfolder, af_deleted, af_date_inserted, af_originator_ast_guid,
          af_timestamp, af_map_image,
          af_blob BLOB,        -- the actual bytes (only when --file-blobs)
          af_thumbnail BLOB,
          fetched_at, raw_json

asset_file_report_map
  key:    (ast_id, af_id)
  cols:   afrm_guid, af_order, af_cover, af_print,
          af_filename, af_date, af_description,
          af_parent_af_guid, pw_document_id
```

### What we observed on bridge 01A001's 9 inspections

| Inspection year | Type | Files mapped | Mix |
|---|---|---:|---|
| 2009 (WVDOT Standard) | Periodic | 0 | (paper-era) |
| 2011 (WVDOT Standard) | Periodic | 8 | mostly Nikon photos |
| 2013–2025 | various | 15–25 each | photos + .docx defect summaries + .xls channel profiles + .dgn drawings |

154 files / 43 MB on disk for that one bridge's full history. Files in InspectTech are content-sniffed (`\xffd8ff` JPEG, `%PDF` PDF, `PK\x03\x04` for docx/xlsx zip containers) — the server doesn't always return a correct `Content-Type`.

### Map row flags

- `af_cover=true` — this is the bridge-cover photo on PDF page 1.
- `af_print=true` — this file gets embedded in the printed PDF (vs being a working attachment that stays in the database).
- `af_order` — display order within the report.

### Backend exposes them as

- `GET /api/inspections/{ast_id}/attachments` — list, ordered cover-first.
- `GET /api/files/{af_id}/data` — stream the binary, MIME-sniffed.
- `GET /api/bridges/{bars}/cover` — most-recent cover photo for the bridge (used by the bridge detail hero banner).

---

## 10. Schedules — recurring inspections and maintenance

Two parallel "schedule" mechanisms on Asset rows:

### 10.1 `AssetInspectionTypeSchedule`

```
PUT  /api/AssetInspectionTypeSchedule              (create/update recurring schedule)
GET  /api/AssetInspectionTypeSchedule/GetAssetScheduledInspectionTypes/{as_id}
```

For a given Asset, lists the inspection types (`it_id`) that have recurring schedules configured (e.g. "Routine every 24 months, NSTM every 12 months"). Each schedule carries frequency unit/length, next-due date, last-completed date, and an optional assigned inspector.

On bridges100.db: most bridges had no recurring schedules in our 10-bridge sample probe. WVDOT appears to rely on a global cycle policy rather than per-bridge schedules.

### 10.2 `AssetActivityTypeSchedule`

```
GET  /api/AssetActivityTypeSchedule/GetRecurringMaintenance/{as_id}
```

For maintenance activities (paint, seal, patch) rather than inspections. Schedule rows carry `act_id` (activity type) and similar frequency fields. Like above, sparse on this tenant.

Together these two schedule tables drive the "Upcoming Work" / "Overdue Inspections" reports — the system rolls them up nightly to flag bridges that need attention.

---

## 11. Working sets and inspector access

`InspectorAssetMap` (junction `(as_id, in_id)`) controls who can edit which assets. Carries:

- `iam_asset_access_level` (read/write/admin)
- `iam_working_set` (boolean — does this asset show in this inspector's mobile working set)
- `iam_report_access_level`, `iam_asset_create`, `iam_report_create`
- `iam_workingset_added_date`

The working set is what controls the offline-collector experience: an inspector heading to the field downloads everything for the bridges in their working set, then syncs back when they return to the office.

`/api/InspectorWorkingSetMap/CanManageWorkingSet` returns whether the current user can modify working sets (a permission-gated feature).

---

## 12. The Asset → InspectionReport relationship — full chain

This is the path you walk to get "everything ever recorded about a bridge":

```
Asset (one row)
  │
  ├──► AssetValue (~750 rows)  ──── current cells, EAV
  │      └──► Field (dictionary)
  │
  ├──► AssetElement (0..N hundred rows) ──── current element state, EAV
  │      └──► Asset rows for sub-asset groups + element instances
  │            (as_asset_def=2 or 3)
  │
  ├──► AssetTask Type=Report (one per inspection)
  │      │
  │      ├──► ReportValue (~750 rows per inspection) ──── captured cells
  │      │      └──► Field (same dictionary)
  │      │
  │      ├──► InspectionReportInspTypeMap → InspectionType
  │      │      (one inspection can be multiple types: NBI Routine + NSTM)
  │      │
  │      ├──► InspectionInspector → User
  │      │      (one or more inspectors per visit)
  │      │
  │      ├──► WorkflowStage / WorkFlow
  │      │      (-5 = "Approve Final Report" terminal)
  │      │
  │      └──► AssetFilesReportMap → AssetFile
  │             (photos, defect docs, channel profiles for THIS visit)
  │
  ├──► AssetTask Type=WorkManagementInstance (critical findings)
  │
  ├──► AssetFile (every photo ever attached, even unmapped)
  │
  ├──► AssetInspectionTypeSchedule (recurring inspection cadence)
  ├──► AssetActivityTypeSchedule    (recurring maintenance cadence)
  ├──► InspectorAssetMap           (who can edit this asset)
  └──► AssetSegmentMap             (linear-reference segmentation)
```

Read in the other direction: a single ReportValue belongs to one inspection (`ast_id`); the inspection belongs to one Asset (`as_id`); the Asset has 0..N inspections.

---

## 13. Real-data example — bridge 02A021 fully expanded

(All queries run against `analysis/bridges100.db`, which now contains both 01A001 and 02A021.)

### Identity
- `as_id` = **42998**, `as_name` = **02A021**, `as_guid` = `573b366b-…-c10caa7f929c`
- `at_id=1` (Bridge), `rt_id=3` (WVDOH Report)
- `asset_status_id=0` → **Archived** (out of service)
- `as_federal_submission_type=0` → NotRequired (excluded from FHWA submission)
- `as_sub_asset_parent=true` → has sub-assets attached
- `as_last_update_date` = 2026-01-28

### Counts
- **5 sub-asset groups** (Abutment 1, Span 1, Pier 1, Span 2, Abutment 2)
- **135 sub-asset element-instance + defect rows** in `AssetElement`
  - 14 PhysicalElements
  - 6 ProtectiveSystems
  - 115 Defects
- **~720 AssetValue rows** (current state)
- **5 inspections** (in our `--limit 5` dump; the bridge has more in the tenant)
- **~52 attachments** across the 5 inspections (photos + defect docs)

### Sub-asset group breakdown

```
as_id=60694  "Abutment 1"    (def=3)  parent=42998 [implicit]
as_id=60695  "Span 1"        (def=3)
as_id=60696  "Pier 1"        (def=3)
as_id=60697  "Span 2"        (def=3)
as_id=60698  "Abutment 2"    (def=3)
```

Each contains a roster of physical-element instances (e.g., Abutment 1 contains a "RC Abutment" instance, an "Elastomeric Bearing" instance with quantity 4, etc.) and each physical-element instance has child Defect rows underneath it via `ParentSubAssetId`.

### Element condition rollup

| Element type | Instances | Total qty | Mostly in CS… |
|---|---:|---:|---|
| Elastomeric Bearing (310) | 3 | 16 each | CS1 (all good) |
| RC Abutment (215) | 2 | 116 ft | CS1/CS2 |
| RC Pier Wall (210) | 1 | 45 ft | CS2/CS4 (**11 ft in severe**, driven by scour) |
| RC Open Girder/Beam (110) | 2 | 185 ft | CS1/CS2 |
| RC Top Flange (16) | 2 | 554 sq ft | CS1 |
| RC Slab (38) | 2 | **1046 sq ft, 743 in CS3 (poor)** | the deck is the worst part |
| Metal Bridge Railing (330) | 2 | 103 ft | CS1 |
| Steel Protective Coating (515) | 2 | 652 sq ft | CS1 |
| Wearing Surfaces (510) | 4 | 1531 sq ft | CS1 |

Notable defect observations:
- Pier Wall scour: 2 ft in CS3, **11 ft in CS4** → the trigger for Archived status
- RC Slab efflorescence/rust staining: 378 + 315 sq ft in CS3 across two spans
- RC Slab delamination/spall: 21 + 29 sq ft in CS3

### Inspection generations on 01A001 vs 02A021

| Year | rt_id | Inspection types | Narratives | NBI 58/59/60 | B.C.01-15 |
|---|---|---|---:|:---:|:---:|
| 2009 | 1 WVDOT Standard | Periodic | 0 | ✓ | — |
| 2011-2013 | 1 WVDOT Standard | Periodic | 11–12 | ✓ | — |
| 2015 | 3 WVDOH Report | Hands-On Routine | 12 | ✓ | — |
| 2017-2023 | 3 WVDOH Report | ROUTINE-NBI 90 | 13 | ✓ | — |
| 2025 | 3 WVDOH Report | **Routine (SNBI)** | 16 | ✓ | ✓ |

Both NBI and SNBI fields coexist on the 2025 inspection because the form templates carried the legacy NBI fields forward (the system writes to both during the transition window).

---

## 14. Useful query patterns

### Get "everything that hangs off bridge X" in one query

```sql
WITH bridge AS (SELECT * FROM asset WHERE name = '02A021' LIMIT 1)
SELECT
  (SELECT as_id FROM bridge) AS as_id,
  (SELECT name FROM bridge) AS bars,
  (SELECT COUNT(*) FROM asset_value WHERE as_id = (SELECT as_id FROM bridge)) AS values,
  (SELECT COUNT(*) FROM asset_element WHERE as_id = (SELECT as_id FROM bridge)) AS elements,
  (SELECT COUNT(*) FROM inspection WHERE as_id = (SELECT as_id FROM bridge)) AS inspections,
  (SELECT COUNT(*) FROM asset_file WHERE as_id = (SELECT as_id FROM bridge)) AS files,
  (SELECT SUM(length(af_blob)) FROM asset_file WHERE as_id = (SELECT as_id FROM bridge)) AS bytes_stored;
```

### Walk an inspection's element tree from the bridge down

```sql
-- All physical elements on bridge 02A021 with their defects rolled up
SELECT
  pe.element_name,
  pe.classification,
  pe.unit,
  pe.total_quantity,
  pe.state1 || '/' || pe.state2 || '/' || pe.state3 || '/' ||
    pe.state4 || '/' || pe.state5 AS cs1_5,
  (SELECT GROUP_CONCAT(d.element_name, ', ')
     FROM asset_element d
     WHERE d.as_id = pe.as_id AND d.parent_sub_as_id = pe.sub_as_id
       AND d.classification = 'Defect' AND d.total_quantity > 0) AS defects
FROM asset_element pe
WHERE pe.as_id = 42998 AND pe.classification = 'PhysicalElement'
ORDER BY pe.element_id;
```

### Find bridges with the most severe element conditions

```sql
SELECT a.name, ae.element_name, ae.state4 AS severe_qty, ae.unit
FROM asset_element ae
JOIN asset a USING (as_id)
WHERE ae.state4 > 0 AND ae.classification = 'PhysicalElement'
ORDER BY ae.state4 DESC LIMIT 20;
```

### Trace an inspection's full graph

```sql
SELECT
  i.ast_id, i.ast_inspection_date,
  a.name AS bars, rt.rt_name AS report_type,
  (SELECT GROUP_CONCAT(it.it_name, ', ')
     FROM inspection_inspection_type iit
     JOIN inspection_type it USING (it_id)
     WHERE iit.ast_id = i.ast_id) AS types,
  (SELECT GROUP_CONCAT(u.fname || ' ' || u.lname, ', ')
     FROM inspection_inspector ii
     JOIN user u USING (in_id)
     WHERE ii.ast_id = i.ast_id) AS inspectors,
  (SELECT COUNT(*) FROM report_value WHERE ast_id = i.ast_id) AS captured_values,
  (SELECT COUNT(*) FROM asset_file_report_map WHERE ast_id = i.ast_id) AS attachments,
  ws.wfs_name AS stage
FROM inspection i
JOIN asset a ON a.as_id = i.as_id
LEFT JOIN report_type rt USING (rt_id)
LEFT JOIN workflow_stage ws ON ws.wfs_id = i.ast_current_wfs_id
WHERE a.name = '02A021'
ORDER BY i.ast_inspection_date;
```

---

## 15. Gotchas, again

- **Three trees, three columns.** The administrative tree (`AssetViewTree`), the sub-asset tree (`ParentSubAssetId` on `AssetElement`), and the corridor membership (`corridor` field). Don't conflate them.
- **`as_parent_id` is almost always null on real bridges.** Don't use it to find the bridge's district — use `AssetViewTree.RootAssetId`.
- **Sub-asset rows DO exist in the Asset table** (you can `GET /api/Asset/60699` and get back an as_asset_def=2 row), but they are filtered out of `/odata/Assets`. Use `GET /api/StructureElement/GetSubAssets/{bridgeAsId}` to find them.
- **`AssetElement` keys by `(AssetId, SubAssetId, ParentSubAssetId, UserId)`**, NOT just `(AssetId, SubAssetId)`. The `ParentSubAssetId` is part of the key because the same element instance can show up under multiple parent groups in defect/protective-system relationships.
- **`childCount` is rarely populated** on Asset rows. It's a hint, not a source of truth. Count children with `COUNT(*) FROM asset_element WHERE as_id = ?` instead.
- **The 2009-era WVDOT Standard report (rt_id=1) does not capture narratives** — only structured `AssetValue` cells. The Narrative tabs in the InspectTech UI will be empty for those inspections; that's the data, not a UI bug.
- **The same bridge can have both NBI and SNBI condition values populated** on a single recent inspection (the form templates carry both forward during the transition window). The canonical-ratings logic in our backend picks SNBI first, falls back to NBI.
- **A "merge" inspection** has `IsMerged=true` and is a synthetic AssetTask that consolidates two parallel inspections (e.g., one inspector did the deck, another did the substructure). Treat it as a single inspection for display purposes.
- **`as_stage_pontis=true`** is the export flag for the FHWA Pontis system. Setting it kicks off a nightly job that exports the bridge's MBEI data to Pontis-compatible XML.

---

## 16. File inventory for this research

Raw API responses captured for §1 in `analysis/asset_probes/`:

| File | Contents | Size |
|---|---|---:|
| `01_asset_full.json` | `/api/Asset/42998` | 763 B |
| `02_asset_by_guid.json` | same, via GUID | 763 B |
| `05_subassets.json` | `/api/StructureElement/GetSubAssets/42998` — 140 rows | 122 KB |
| `13_all_asset_tasks_odata.json` | `/odata/AssetTasks?filter=AssetId eq 42998` | 7.2 KB |
| `14_all_inspections_for_asset.json` | `/api/InspectionReport/GetMostRecentReportsForAsset/42998` | 231 KB |
| `15_asset_files.json` | `/api/AssetFile/GetByAssetId/42998` | 1.7 KB |
| `18_assettype_full.json` | `/api/AssetType/1` | 800 B |

Persistent memory updates to make later: the WV.gov tenant only uses `Bridge` AssetType (1) meaningfully; all other AssetType IDs return little data. SubAssets are queried via `StructureElement` not `Asset`. Type=WorkManagementInstance is the critical-finding workflow, separate from inspections.
