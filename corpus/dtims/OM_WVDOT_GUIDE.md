# OM_WVDOT — Deighton dTIMS Operations Database — Usage Guide

**What it is:** `OM_WVDOT` is WVDOT's live **Deighton dTIMS** (Deighton Total Infrastructure
Management System) operations backend — the maintenance-management system of record. It holds
~15.7M rows across 563 tables (all in the `operations` schema) covering work tasks, labor /
equipment / stockpile / other-cost transactions, maintenance plans, assets, and citizen requests.

**Server:** `TAMSDW` = `10.6.60.45` (SQL Server 2019 Enterprise, "TAMS DW" = Transportation Asset
Management System Data Warehouse).

> ⚠️ **You do not have a direct login to `10.6.60.45`.** All access is **read-only through the
> linked server `TAMSDW`** configured on the WVDOT Data-Warehouse box (`10.69.0.44`), reached via
> your SSH tunnel at `127.0.0.1:11433`. The linked server runs remote queries as
> `TAMS_DW_Service_Account` (a fixed mapping) — **not** as your `DTIMS_Transactions` login. You
> ride that one-way trust relationship; you are not authenticating to TAMSDW yourself.

---

## 1. How to connect

You connect to the **Data-Warehouse** as normal (this is what `list.py` already does), then reach
OM_WVDOT through the linked server.

```python
import pymssql
conn = pymssql.connect(
    server="127.0.0.1", port=11433,           # SSH tunnel -> 10.69.0.44:1433
    user="DTIMS_Transactions", password="dT1mS#t3@n8",
    database="Data-Warehouse", login_timeout=10, timeout=180,
)
cur = conn.cursor()
```

The tunnel is the systemd service `wvdot-mssql-tunnel`. If queries fail with a connect error,
the tunnel is likely down — check that service first.

---

## 2. Two ways to query OM_WVDOT through the link

### A. Four-part name (let local SQL Server federate the query)
Good for catalog/metadata browsing and small result sets.
```sql
SELECT TOP 10 * FROM [TAMSDW].[OM_WVDOT].[operations].[Task];
```

### B. OPENQUERY (run the work ON the remote — STRONGLY PREFERRED) ✅
The remote does the filtering/aggregation and ships back only the result. **Always use this for
COUNTs, GROUP BYs, joins, and date filters** — four-part-name federation can drag millions of rows
across the link first.
```sql
SELECT * FROM OPENQUERY([TAMSDW],
  'SELECT COUNT(*) FROM OM_WVDOT.operations.BaseTransaction');
```

**Python helper** (handles the single-quote escaping that OPENQUERY requires):
```python
def oq(cur, remote_sql):
    sql = "SELECT * FROM OPENQUERY([TAMSDW], '" + remote_sql.replace("'", "''") + "')"
    cur.execute(sql)
    return cur.fetchall()

rows = oq(cur, "SELECT COUNT(*) FROM OM_WVDOT.operations.Task WHERE ValidTo IS NULL")
```

> **Note:** `rpc_out` is **OFF** on this linked server, so you can run `SELECT`/`OPENQUERY` reads
> but not remote stored-procedure (`EXEC ... AT`) calls. Treat the whole thing as read-only.

---

## 3. Two conventions you MUST know

### 3a. Temporal versioning — filter `ValidTo IS NULL` for the *current* row
Almost every entity is system-versioned. Each logical record can have multiple historical rows;
the **live/current** version is the one with `ValidTo IS NULL` (older versions have a timestamp).
Many tables also have an explicit `*History` twin and occasional `backup_*` snapshots.

```sql
-- current tasks only (112,377 of 116,430 total rows are current)
SELECT * FROM OPENQUERY([TAMSDW],
  'SELECT * FROM OM_WVDOT.operations.Task WHERE ValidTo IS NULL');
```
**Forgetting `ValidTo IS NULL` will double-count.** Apply it to Task, BaseTransaction,
CoreMaintenancePlan, AssetReference, AccountCode, Material, DomainValue, etc.

### 3b. Coded values resolve through `operations.DomainValue`
Lookups are centralized. `DomainValue.Type` names the domain, `Code` is the stored value, `Decode`
is the human label. Filter by `Type`, then join on the code.
```sql
SELECT * FROM OPENQUERY([TAMSDW],
  'SELECT Type, Code, Decode FROM OM_WVDOT.operations.DomainValue
   WHERE ValidTo IS NULL AND Type = ''DomainValueActivityType'' ');
```
> Heads-up: some domains still contain Deighton **demo defaults** (e.g. `DomainValueCallType`
> shows `NZTA`, `Downer`, "Test - Road Patching") — confirm a domain reflects real WVDOT config
> before relying on it.

### Dates are `datetimeoffset`
`TransactionDate`, `CreatedOn`, etc. carry a timezone offset (US Eastern). The data is a planning
system, so **future-dated rows are normal** — the master ledger currently spans
**2024-01-24 → 2026-08-29**. Bound queries by date explicitly when you want "actuals to date."

---

## 4. The core data model

### The cost ledger (this is the big one — 5.2M rows)
`operations.BaseTransaction` is the master financial transaction table. Each row is one costed
event with `TransactionDate`, `TransactionQuantity`, `TransactionTotalCost`, `TransactionUnitCost`.
It is **subtyped** by exactly one of four child tables, each carrying a `TaskId` foreign key:

| Child table | Rows | Joins to BaseTransaction on | Adds |
|---|---|---|---|
| `operations.LaborTransaction` | 2.84M | `BaseTransactionId` | `TaskId`, `LaborInventoryId`, `TimeCodeId` |
| `operations.EquipmentTransaction` | 1.59M | `BaseTransactionId` | `TaskId`, `EquipmentInventoryId` |
| `operations.StockpileTransaction` | 0.18M | `BaseTransactionId` | `TaskId`, `StockpileInventoryId` |
| `operations.OtherCost` | 0.62M | `BaseTransactionId` | `TaskId`, `ItemName` |

This subtype layout is the source of the flattened `Data-Warehouse.dbo.dtims_transactions` export
(654K rows: `TaskId`, `TransactionDate`, Labor/Equipment/Stockpile/Other Quantity+Cost). When you
need raw detail, come here; when you need the pre-summarized version, use the warehouse table.

### Work management
- `operations.Task` (116K; 69 cols) — the central work record: `Name`, `Description`, status
  (`EntityStatusId`), `EstTotalCost`/`ActTotalCost`, scheduling, `ProgramId`, `AccountCodeId`,
  `OrganizationId`, `FiscalYearId`, and a `Mapping geometry` (GIS).
- `operations.CoreMaintenancePlan` (295K) — recurring/core maintenance plans, with
  `CoreMaintenancePlanAssetReference` (296K) linking plans to assets.
- `operations.DailyWorkReportLineItem` (633K) + history — daily crew reporting.
- `operations.AnnualWorkPlanLineItem` (23K), `operations.WorkSchedule*`, `operations.Workpack_Task`.

### Assets & location
- `operations.AssetReference` (567K) — assets referenced by work: `AssetId`, `NetworkName`
  (encoded County/Route/Mile, e.g. `2240068070000` = Lincoln CR 68/7), `DisplayName`
  (human-readable, e.g. "Kanawha I 79 Ramp NB 1B"), `From`/`To`/`Lane` (linear referencing),
  `Geometry`, `MaintenanceClass`, `ReferenceType`.
- `operations.TaskAssetReference` (268K) — junction: `AssetReferenceId` ↔ `ReferenceObjectId`
  (the Task/plan that references the asset).

### Reference / financial
- `operations.AccountCode` (19K) — chart of accounts; `DisplayValue` + 5 budget dimensions.
- `operations.Program` (15K) — `Code` + `Name`.
- `operations.Material` (12K), `operations.EquipmentInventory` (30K),
  `operations.LaborInventory` (8K), `operations.StockpileInventory` (63K).

### Citizen requests
- `operations.CustomerRequest` (1,449; 46 cols) — public complaints/requests: `ReferenceNo`,
  `Description`, dates (`DateReceived`/`DateDue`/`DateClosed`), `CountyId`, `Mapping`, SLA fields.

### Deighton application-config tables (the product's fingerprint)
- `operations.DeightonUIFormField` (1,066), `operations.DeightonUIFormFieldBasic` (1,039),
  `operations.DeightonAttributes` (797) — dTIMS UI/attribute customization metadata, not business
  data. Useful for understanding how WVDOT configured the app, not for reporting.

---

## 5. Verified example queries (all run read-only via OPENQUERY)

**Total maintenance spend by month (actuals through today):**
```sql
SELECT * FROM OPENQUERY([TAMSDW], '
  SELECT CONVERT(char(7), TransactionDate, 126) AS ym,
         COUNT(*) AS txns, SUM(TransactionTotalCost) AS total_cost
  FROM OM_WVDOT.operations.BaseTransaction
  WHERE ValidTo IS NULL AND TransactionDate <= SYSDATETIMEOFFSET()
  GROUP BY CONVERT(char(7), TransactionDate, 126)
  ORDER BY ym');
```

**Cost by transaction type (labor vs equipment vs stockpile vs other):**
```sql
SELECT * FROM OPENQUERY([TAMSDW], '
  SELECT ''Labor'' AS kind, SUM(bt.TransactionTotalCost) AS cost
    FROM OM_WVDOT.operations.LaborTransaction lt
    JOIN OM_WVDOT.operations.BaseTransaction bt ON bt.BaseTransactionId=lt.BaseTransactionId
   WHERE bt.ValidTo IS NULL
  UNION ALL
  SELECT ''Equipment'', SUM(bt.TransactionTotalCost)
    FROM OM_WVDOT.operations.EquipmentTransaction et
    JOIN OM_WVDOT.operations.BaseTransaction bt ON bt.BaseTransactionId=et.BaseTransactionId
   WHERE bt.ValidTo IS NULL');
```

**Spend rolled up to a Task:**
```sql
SELECT * FROM OPENQUERY([TAMSDW], '
  SELECT TOP 20 t.TaskId, t.Name, t.ActTotalCost,
         SUM(bt.TransactionTotalCost) AS ledger_cost
  FROM OM_WVDOT.operations.Task t
  JOIN OM_WVDOT.operations.LaborTransaction lt ON lt.TaskId=t.TaskId
  JOIN OM_WVDOT.operations.BaseTransaction bt ON bt.BaseTransactionId=lt.BaseTransactionId
  WHERE t.ValidTo IS NULL AND bt.ValidTo IS NULL
  GROUP BY t.TaskId, t.Name, t.ActTotalCost
  ORDER BY ledger_cost DESC');
```

**Find an asset by County/Route and its work:**
```sql
SELECT * FROM OPENQUERY([TAMSDW], '
  SELECT TOP 50 ar.AssetReferenceId, ar.DisplayName, ar.NetworkName, ar.[From], ar.[To]
  FROM OM_WVDOT.operations.AssetReference ar
  WHERE ar.ValidTo IS NULL AND ar.DisplayName LIKE ''%I 79%'' ');
```

**List a domain's coded values:**
```sql
SELECT * FROM OPENQUERY([TAMSDW], '
  SELECT Code, Decode FROM OM_WVDOT.operations.DomainValue
  WHERE ValidTo IS NULL AND Type=''DomainValueActivityType'' ORDER BY Code');
```

---

## 6. Gotchas / cautions

- **Read-only, shared, production.** This is the live system other people depend on. Keep queries
  cheap: prefer OPENQUERY, always add `WHERE ValidTo IS NULL`, filter by date, avoid `SELECT *` on
  the multi-million-row transaction tables, and don't hammer it.
- **Don't COUNT 563 tables with `COUNT(*)`.** For row counts use the partition stats DMV remotely:
  ```sql
  SELECT * FROM OPENQUERY([TAMSDW], '
    SELECT s.name, t.name, SUM(p.rows)
    FROM OM_WVDOT.sys.tables t
    JOIN OM_WVDOT.sys.schemas s ON s.schema_id=t.schema_id
    JOIN OM_WVDOT.sys.partitions p ON p.object_id=t.object_id AND p.index_id IN (0,1)
    GROUP BY s.name, t.name');
  ```
- **Quote escaping:** inside OPENQUERY, every literal single-quote must be doubled (`''`). The
  Python `oq()` helper above does the first level; nested string literals need `''''`.
- **`geometry` columns** (`Mapping`, `Geometry`) may not marshal cleanly over the OLE DB link —
  select them as `.STAsText()` or omit them.
- **`datetimeoffset`** comes back with an offset; normalize if comparing to naive dates.
- **Env siblings exist** on the same server: `OM_WVDOT_Pilot / _Staging / _UAT` (each 563 tables)
  and the analytics layer `BA_WVDOT_OMAssets*`. Make sure you're querying **`OM_WVDOT`** (prod).
  Some neighboring DBs (`Credit_Cards`, `OBPROD`, `PermitPortalLoginDB`, `OM_WVDOT_V1R5`) are
  **denied** even to the service account.

---

## 7. Architecture summary

```
Deighton dTIMS application
        │ (system of record)
        ▼
TAMSDW @ 10.6.60.45  ──►  OM_WVDOT  (prod ops backend: 563 tables, ~15.7M rows, operations schema)
                          ├─ BaseTransaction (5.2M)  + Labor/Equipment/Stockpile/Other subtypes
                          ├─ Task / CoreMaintenancePlan / DailyWorkReport
                          ├─ AssetReference / TaskAssetReference
                          └─ Deighton* config tables
        │
        │  [linked server TAMSDW, read-only, runs as TAMS_DW_Service_Account, rpc_out OFF]
        ▼
Data-Warehouse @ 10.69.0.44   ──►  dbo.dtims_transactions  (654K flattened export)
        ▲
        │  SSH tunnel  wvdot-mssql-tunnel
127.0.0.1:11433  (you / DTIMS_Transactions)
```

**Bottom line:** query OM_WVDOT through `OPENQUERY([TAMSDW], ...)`, always filter `ValidTo IS NULL`,
resolve codes via `DomainValue`, and remember it's a shared read-only production system you reach by
delegated trust — not by your own credentials.
