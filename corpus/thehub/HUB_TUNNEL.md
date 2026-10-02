# Hub / Data-Warehouse Tunnel — Quick Start

Connects to the WVDOT **Data-Warehouse** SQL Server (TheHub project data,
plus the `[TAMSDW]` linked server that fronts dTIMS prod `OM_WVDOT`).
Used by dot12-backend hub features, `reimport_om.py`, and ad-hoc analysis.

## 1. Start the tunnel

```bash
ssh -f -N -o ConnectTimeout=10 -o ExitOnForwardFailure=yes \
    -L 1434:10.69.0.44:1433 cputest
```

- `cputest` is defined in `~/.ssh/config` (157.151.165.58, key `~/Downloads/cpu-test.key`).
- Forwards **local 127.0.0.1:1434** → Data-Warehouse SQL Server `10.69.0.44:1433`.
- Do **not** forward to `localhost:1433` on cputest — that endpoint resets the TLS handshake.

```bash
# verify          # stop
nc -z 127.0.0.1 1434
lsof -nP -iTCP:1434 -sTCP:LISTEN
pkill -f "ssh.*-L 1434"
```

The tunnel dies on laptop sleep — if queries hang or fail to connect, check the
listener first and restart it.

## 2. Credentials

`HUB_DB_*` in `dot12-backend/.env` (never hard-code them):

| Var | Value |
|---|---|
| `HUB_DB_SERVER` | `127.0.0.1,1434` |
| `HUB_DB_NAME` | `Data-Warehouse` |
| `HUB_DB_USER` / `HUB_DB_PASS` | `DTIMS_Transactions` / see `.env` |

## 3. Connect (pyodbc — the only installed driver)

Use the dot12-backend venv (`pymssql` is not installed anywhere):

```python
import pyodbc
cn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=127.0.0.1,1434;"
    "DATABASE=Data-Warehouse;UID=<HUB_DB_USER>;PWD=<HUB_DB_PASS>;"
    "TrustServerCertificate=yes;", timeout=15)
# datetimeoffset (type -155) isn't supported natively — decode or CONVERT() remotely
cn.add_output_converter(-155, lambda b: b.decode("utf-16-le") if b else None)
```

In-app, use `utils/hub_client.hub_query()` (handles timeouts + gevent offload).

## 4. Query patterns

**Local Data-Warehouse** tables directly (TheHub: `Project`, `StateFund`, …
— bracket the `[external]` schema, it's a reserved word).

**dTIMS prod (OM_WVDOT)** goes through the linked server — double any single
quotes inside the remote SQL:

```sql
SELECT * FROM OPENQUERY([TAMSDW], '
  SELECT TOP 10 t.TaskOrderId, bt.TransactionQuantity, bt.TransactionTotalCost
  FROM OM_WVDOT.operations.BaseTransaction bt
  JOIN OM_WVDOT.operations.StockpileTransaction st ON st.BaseTransactionId = bt.BaseTransactionId
  LEFT JOIN OM_WVDOT.operations.Task t ON t.TaskId = st.TaskId AND t.ValidTo IS NULL
  WHERE bt.ValidTo IS NULL AND bt.IntegrationColumn1 = ''OC''')
```

OASIS doc fields live in `BaseTransaction.IntegrationColumn1–13`
(1=DOC_CD, 2=DOC_DEPT_CD, 3=DOC_ID, 4=DOC_VERS_NO, 6=COMM_LN_NO,
7=ACTG_LN_NO, 9=activity). For big
pulls, keyset-page on `BaseTransactionId` (`WHERE … AND BaseTransactionId >
:last ORDER BY BaseTransactionId`, `TOP 5000`) — ~190K rows ≈ 1 min.

## 5. Access limits / gotchas

- Reachable via `[TAMSDW]`: `OM_WVDOT`, `DOTDataWarehouse`, `BA_WVDOT_OMAssets*`.
  **Denied**: `OasisFinance`, `OBPROD`; `OM_PROD` is offline; the `DOTB6PWSQL`
  linked server has no data access.
- `BaseTransaction` looks row-versioned but isn't (`RowVersion` always 0);
  `Task` **is** versioned — filter `ValidTo IS NULL`.
- Worked example of all of this: `~/Downloads/fwdddlanddtimserror/scripts/`.
