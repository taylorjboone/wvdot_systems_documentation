# OM_WVDOT → Your Database: Change-Detection & Sync Design

**Goal:** keep a copy of the operational entities — **Daily Work Report line items, Tasks,
Task↔Asset links, and Assets** — in your own database, picking up only the changes each cycle.
**No cost/transaction data is in scope.**

**Source:** WVDOT Deighton dTIMS, `TAMSDW.OM_WVDOT.operations`, read-only via the `TAMSDW` linked
server (you reach it as `TAMS_DW_Service_Account`; `rpc_out` is off, so SELECT/OPENQUERY only).

**TL;DR design:**
- 3 of the 4 entities support **true incremental CDC** (a timestamp watermark gets you the deltas).
- 1 entity — `TaskAssetReference` — has **no audit columns at all**, so it needs a **snapshot diff**.
- Total volume is **tiny** (~2,000–2,500 row-changes/day), so you can run this as often as you like;
  even a nightly batch is over-provisioned. Build for correctness, not scale.

---

## 1. What you're syncing, and how each one is tracked

| Entity (`operations.*`) | Rows | Has audit? | Change-detection method |
|---|---:|---|---|
| `DailyWorkReportLineItem` | ~633K | ✅ `CreatedOn`, `ValidFrom/ValidTo`, + `…History` | Watermark CDC |
| `Task` | ~116K | ✅ `CreatedOn`, `ValidFrom/ValidTo`, + `TaskHistory` | Watermark CDC |
| `AssetReference` family | ~567K | ✅ via `AssetReferenceHistory` + `AssetReferenceCurrent` | Watermark CDC + hash safety net |
| `TaskAssetReference` | ~268K | ❌ **two ID columns, nothing else** | **Snapshot diff (required)** |

### The temporal model (how dTIMS records change)
Most entities are **system-versioned**:
- The **current** version of a row has `ValidTo IS NULL`. Superseded versions get a `ValidTo`
  timestamp. **Always filter `ValidTo IS NULL`** to read "what is true now."
- Every change also writes a row to a `*History` table: `HistoricObjectId` (the entity's id),
  `ModifiedOn` (datetimeoffset), `ModifiedBy` (user email), and `ChangeValue` (a **JSON snapshot**
  of the entity at that moment). The history row exists for the *create* too — so
  `…History` is a complete change feed, inserts included.
- Timestamps are **`datetimeoffset`** (US Eastern with offset). Normalize to UTC on your side.

> **The watermark you sync on is `ModifiedOn`** (from the History tables) for updates, plus
> `CreatedOn` for inserts. `ValidTo IS NULL` tells you the *current* shape to copy.

---

## 2. How you see that an ASSET has changed (the part you asked about)

Assets are modeled across a few tables — know which is which:

| Table | Role |
|---|---|
| `AssetReferenceCurrent` | **Canonical current state** of each asset reference. Has `AssetId`, the linear-ref fields (`From/To`, `DisplayFrom/To`, `Lane`), `MaintenanceClass`, `ReferenceDate`, an **`IsValid` bit**, and `Geometry`. **Sync from here.** |
| `AssetReferenceHistory` | Superseded versions. Has the asset fields + a **`ValidTo`** marking when that version ended. This is your "what changed" feed. |
| `AssetReference` | The working references actually attached to tasks/plans (what `TaskAssetReference` and `DailyWorkReportLineItem.AssetReferenceId` point at). Has only `ReferenceDate` for timing. |
| `AssetReferenceLRM`, `AssetReferenceHistoricalLRS` | Linear-referencing-method variants. Ignore unless you specifically need LRS geometry history. |

There is **no `ModifiedOn` on the asset base tables**, so detect asset change three ways, combined:

**(a) New / updated assets — watermark on `ReferenceDate`:**
```sql
SELECT * FROM OPENQUERY([TAMSDW], '
  SELECT AssetId, NetworkName, DisplayName, MaintenanceClass,
         [From], [To], DisplayFrom, DisplayTo, Lane, ReferenceDate, IsValid
  FROM OM_WVDOT.operations.AssetReferenceCurrent
  WHERE ReferenceDate > ''2026-06-20T00:00:00-04:00'' ');   -- > your last watermark
```

**(b) Superseded versions — anything closed since last run (catches edits & invalidations):**
```sql
SELECT * FROM OPENQUERY([TAMSDW], '
  SELECT DISTINCT AssetId
  FROM OM_WVDOT.operations.AssetReferenceHistory
  WHERE ValidTo > ''2026-06-20T00:00:00-04:00'' ');   -- these AssetIds changed; re-pull from Current
```
Take the `AssetId`s from (b) and re-read their current row from `AssetReferenceCurrent` (or mark
them deleted if they no longer appear / `IsValid = 0`).

**(c) Hash safety net (because asset CDC has no clean ModifiedOn) — periodic, cheap:**
Pull a lightweight fingerprint of every current asset and compare to what you stored. Anything whose
hash differs (or is missing/new) gets re-synced. At ~567K rows this is seconds.
```sql
SELECT * FROM OPENQUERY([TAMSDW], '
  SELECT AssetId,
         CONVERT(varchar(34), HASHBYTES(''MD5'',
           CONCAT(NetworkName,''|'',DisplayName,''|'',MaintenanceClass,''|'',
                  [From],''|'',[To],''|'',Lane,''|'',IsValid)), 1) AS h
  FROM OM_WVDOT.operations.AssetReferenceCurrent ');
```
Run (a)+(b) every cycle for speed; run (c) nightly (or weekly) to self-heal anything the watermark
missed. **This three-legged approach is the robust way to know an asset changed** when the source
doesn't give you a single reliable `ModifiedOn`.

---

## 3. Change detection per entity (the delta queries)

Keep a **watermark per entity** in your DB (last `ModifiedOn`/`CreatedOn`/`ReferenceDate` you
successfully ingested). Each cycle: pull rows newer than the watermark, upsert, then advance the
watermark to the max timestamp you saw. Use a small **overlap/lookback** (e.g. watermark minus 1
hour) and idempotent upserts so a late-arriving or clock-skewed row is never lost — duplicates are
harmless because you upsert on the primary key.

### 3a. DailyWorkReportLineItem — watermark CDC
Inserts and the current shape:
```sql
SELECT * FROM OPENQUERY([TAMSDW], '
  SELECT DailyWorkReportLineItemId, TaskId, AssetReferenceId, RouteName,
         BeginningMilePost, EndMilePost, [From], [To], Accomplishment, UnitOfMeasureId,
         AccomplishmentDate, OrganizationId, PerformanceStandardId, DailyWorkReportId,
         CreatedOn, RowVersion
  FROM OM_WVDOT.operations.DailyWorkReportLineItem
  WHERE ValidTo IS NULL AND CreatedOn > ''<watermark>'' ');
```
Updates (rare — DWRLI is ~99% write-once) via the history feed:
```sql
SELECT * FROM OPENQUERY([TAMSDW], '
  SELECT DISTINCT HistoricObjectId
  FROM OM_WVDOT.operations.DailyWorkReportLineItemHistory
  WHERE ModifiedOn > ''<watermark>'' ');   -- re-pull these ids from the table above
```

### 3b. Task — watermark CDC (same pattern)
```sql
-- inserts / current shape
SELECT * FROM OPENQUERY([TAMSDW], '
  SELECT TaskId, Name, Description, EntityStatusId, TaskTypeId, PriorityId,
         PerformanceStandardCodeId, OrganizationId, FiscalYearId, AccountCodeId,
         ScheduledStart, ScheduledEnd, ActualStart, ActualEnd, CompletedOn,
         Accomplishment, AccomplishmentTotal, CreatedOn, RowVersion
  FROM OM_WVDOT.operations.Task
  WHERE ValidTo IS NULL AND CreatedOn > ''<watermark>'' ');

-- updates: ids modified since last run (TaskHistory.ModifiedOn), then re-pull current
SELECT * FROM OPENQUERY([TAMSDW], '
  SELECT DISTINCT HistoricObjectId
  FROM OM_WVDOT.operations.TaskHistory
  WHERE ModifiedOn > ''<watermark>'' ');
```
> `TaskHistory.ChangeValue` is a full JSON of the task at that revision — handy if you ever want a
> field-level audit in your DB, but for plain replication you only need the id + re-pull.

### 3c. AssetReference — see §2 (watermark on `ReferenceDate` + history `ValidTo` + nightly hash).

### 3d. TaskAssetReference — SNAPSHOT DIFF (no other option)
This table is just `(AssetReferenceId, ReferenceObjectId)` — `ReferenceObjectId` is the `TaskId`.
**No timestamp, no `ValidTo`, no history**, so you cannot ask "what changed since X." You must
compare the full current set to your copy:

```sql
-- pull the entire link set (cheap: ~268K rows, a few MB)
SELECT * FROM OPENQUERY([TAMSDW], '
  SELECT ReferenceObjectId AS TaskId, AssetReferenceId
  FROM OM_WVDOT.operations.TaskAssetReference ');
```
Then in your DB:
- rows in source **not** in yours → **insert**
- rows in yours **not** in source → **delete** (this is the only way you'll ever catch an unlink)
- (no "update" — the row is just the pair)

A `MERGE`/`EXCEPT` against a staging table does this in one pass. Because it's a full compare it's
also self-correcting. Run it every cycle if you want links fresh, or nightly if hourly link drift is
acceptable.

> Optional optimization: only diff links for tasks you saw change this cycle (from §3b) — but the
> full diff is so cheap here it's usually not worth the complexity.

---

## 4. Reference architecture

```
                 ┌─────────────────────────── every N minutes (or nightly) ──────────────┐
                 │                                                                          │
  watermark store ──▶ for each entity:                                                      │
  (per-entity      │     1. SELECT … WHERE <ts> > watermark   (OPENQUERY, read-only)        │
   last_ts)        │     2. land rows in a STAGING table in your DB                          │
                 │     3. UPSERT staging → target (idempotent, keyed on PK)                  │
                 │     4. advance watermark = MAX(ts seen)                                   │
                 │  TaskAssetReference: full snapshot → EXCEPT diff → insert/delete          │
                 │  Assets (nightly): hash compare → re-sync mismatches                      │
                 └──────────────────────────────────────────────────────────────────────────┘
```

**Target tables (your DB):** mirror the columns you actually need + two bookkeeping columns:
`_synced_at` (UTC) and `_source_rowversion` (or hash). Keep the source PKs
(`DailyWorkReportLineItemId`, `TaskId`, `AssetId`, and the `(TaskId, AssetReferenceId)` pair) as your
keys so upserts are trivial.

**Watermark table:**
```
sync_watermark(entity varchar PK, last_ts datetimeoffset, last_run_utc datetime2, rows_ingested int)
```

**Upsert pattern (per entity):** `MERGE target USING staging ON pk WHEN MATCHED…UPDATE WHEN NOT
MATCHED…INSERT`. For TaskAssetReference also `WHEN NOT MATCHED BY SOURCE THEN DELETE` (within the
diff scope).

---

## 5. Volumes you're designing for

Steady-state, per workday (recent 90 days):

| Feed | Typical/day | Peak/day | Notes |
|---|---:|---:|---|
| DWRLI inserts | ~960 | ~2,150 | ~99% write-once, so updates are negligible |
| DWRLI updates | ~30 | — | from history |
| Task inserts | ~155 | ~350 | |
| Task updates | ~535 | ~2,150 | each task edited ~4× over its life |
| Asset new/changed | ~340 | ~860 | ignore the one-time 107K go-live bulk |
| TaskAssetReference | ~410 net new | — | full-set diff each run regardless |

**~2,000–2,500 row-changes on a normal day; under ~8,000 on a heavy day** (big snow event, bulk task
generation). This is trivial. A 5-minute poll moves a few hundred rows; a nightly batch a few
thousand. Don't over-engineer — a single-threaded job is plenty.

---

## 6. Gotchas & rules (the stuff that will bite you)

1. **`ValidTo IS NULL`** — forget it and you'll pull every historical version and badly over-count.
2. **`datetimeoffset` everywhere** — store UTC, compare in UTC, render in Eastern. Don't compare a
   naive date to these or you'll silently drop/duplicate rows around midnight.
3. **Future-dated rows are real** — dTIMS is a planning system; `ScheduledStart`/`AccomplishmentDate`
   can be in the future. Filter on `CreatedOn`/`ModifiedOn`/`ReferenceDate` (entry time), **not** on
   the business dates, when driving the watermark.
4. **Watermark overlap** — always re-pull a small window (e.g. `watermark − 1h`) and rely on
   idempotent upserts. Cheap insurance against clock skew / long-running source transactions.
5. **TaskAssetReference deletes are invisible to CDC** — the snapshot diff in §3d is the *only* way
   to detect an asset being unlinked from a task. Skip it and your links drift stale forever.
6. **Asset CDC has no clean `ModifiedOn`** — that's why §2 uses three legs (ReferenceDate watermark +
   history `ValidTo` + nightly hash). Don't rely on any single one.
7. **`geometry` columns** (`AssetReferenceCurrent.Geometry`, `Task.Mapping`) may not marshal over the
   OLE DB link — select `.STAsText()` or skip geometry unless you need it.
8. **Linked-server scope** — read-only, `rpc_out` off, runs as a service account. Don't design
   anything that needs to write back or call remote procs.
9. **Go-live bulk loads** — the first import day shows huge counts (107K assets, 6K links). On first
   full load, take a complete snapshot of every table; only run incrementally afterward.
10. **`ChangeValue` JSON** — if you want field-level history in your DB, store it; otherwise just use
    `HistoricObjectId` to know *which* rows to re-pull and ignore the payload.

---

## 7. Suggested cadence

- **Tasks + DWR line items:** incremental watermark pull every **5–15 min** (or hourly — your call;
  volume is nothing).
- **Assets:** incremental (ReferenceDate + history `ValidTo`) each cycle; **nightly hash
  reconciliation** to self-heal.
- **TaskAssetReference:** full snapshot diff **each cycle if you want live links**, otherwise
  nightly. It's a few MB; either is fine.
- **First run:** full snapshot of all four, set watermarks to the max timestamps seen, then switch to
  incremental.

---

*Source structure verified against `TAMSDW.OM_WVDOT` at design time. Replace `''<watermark>''`
placeholders with your stored per-entity timestamp (UTC-normalized, in `datetimeoffset` literal
form). All reads are via `OPENQUERY([TAMSDW], …)`; remember single-quotes double inside OPENQUERY.*
