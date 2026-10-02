# WVDOT HUB ↔ wvOASIS Financial Reconciliation — End-to-End (incl. the TAMSDW `HUBTOON` materialization)

How project-phase financials flow from the **wvOASIS** state ERP, through the **HUB**
(`Data-Warehouse`, `10.69.0.44`) financial bus, into the **materialized `HUBTOON` reporting tables**
on **TAMSDW** (`DOTDataWarehouse`, `10.6.60.45`). Establishes the data lineage, the cross-server
join, and the direct correlation between closeout reconciliation status (`BGPHRStatusId`) and the
reconciled budget/expenditure/balance.

> **Confidence key:** **[FACT]** = read directly from the databases this session. **[INFERRED]** =
> reasoned from naming/behavior; payloads & job definitions live in `OasisFinance` and `msdb`, both
> denied to the `DTIMS_Transactions` login.

> Companion: the upstream bus mechanics (I385 / CAS / CAM / BGPHR processes, schedules, reliability)
> are documented separately. This document focuses on the **financial *result*** and its
> **cross-server materialization**, which IS readable even though the raw XML/`OasisFinance` is not.

---

## 1. The end-to-end picture

```
 wvOASIS (State ERP / accounting)
     │   file-based XML bus (3×/business day):
     │     inbound  I385_0803_FN_HUB_*.xml   →  HUB
     │     outbound CAS, CAM                  →  OASIS
     │     closeout Generate BGPHR + *_Response ack polls
     ▼
 HUB  =  Data-Warehouse @ 10.69.0.44
     │   • dbo.PhaseChangeRequest.BGPHRStatusId  ← closeout reconciliation status (the switch)
     │   • reconciliation views: HUBRemisAuthIdRW / …CN / …EN / …CNENRW,
     │     HUBPHASEAMOUNTS, Reconcilehub, VIEW_AUTH, VIEW_AUTHORIZED
     ▼   (materialized extract pushed cross-server)
 TAMSDW @ 10.6.60.45  →  DOTDataWarehouse.dbo.HUBTOONBASEROW / HUBTOONBASEROWCNDATA
     • flattened project-phase budget vs expended vs balance + OASIS auth codes
     • readable through the TAMSDW linked server (as TAMS_DW_Service_Account)
```

**[FACT]** Both ends are readable to you: `BGPHRStatusId` and the reconciliation views on the
primary server, and the `HUBTOON*` materialization on TAMSDW. The raw XML payloads and `OasisFinance`
payload tables are **not** (denied).

---

## 2. The `HUBTOON` tables (TAMSDW `DOTDataWarehouse`) [FACT]

Small, hand-maintained reporting database. Four objects:

| Object | Rows | Type | Content |
|---|---:|---|---|
| `HUBTOONBASEROW` | 12,763 | table | Project-phase financial snapshot (RW-authorization basis) |
| `HUBTOONBASEROWCNDATA` | 12,752 | table | Same grain, construction (CN) basis |
| `HUBTOONBASEROWupdateWITHCNPROJ` | — | view | Anti-join: CN projects **absent** from the ROW base (ETL gap-finder) |
| `PermitPortalChargesToTreasuryold` | 1 | table | Dead leftover (1 test row; carries applicant PII) — ignore |

### 2a. Schema (identical 24 columns on both tables)
`ProjectID` (numeric, **business** project number), `ProjectName`, `StateProjectID`, `County`,
`District`, `Project Manager`, `Development Resp`, `PhaseCode`, `RW Phase Status`,
`RW Phase Start/End Date`, `FederalProjectNo`, `Estimated or Auth`, `OASIS/HUB Auth`,
**`CURR_BUD_AM`** (money), **`ACTU_EXP_AM`** (money), **`Current Balance`** (money), **`RemisAuthId`**,
`CNPhaseStartDate`, `CNPhaseEndDate`, `EFEND_DT`, `CNFederalProjectNo`, `EXP_FUND_CD` (nchar10),
`EXP_APPR_CD` (nchar10). No keys/indexes.

> **[FACT] note:** despite the name, `HUBTOONBASEROW` is *not* purely Right-of-Way — its `PhaseCode`
> values include `RW0001`, `CN0001`, `CN0002`, `CN0003`. Each row merges RW status/dates **and** CN
> dates for a project-phase. **[INFERRED]** the two tables differ by the budget basis they sum
> (`HUBRemisAuthIdRW` vs `HUBRemisAuthIdCN` views) — hence the different totals below.

### 2b. Totals [FACT]
| Table | Rows | Budget `CURR_BUD_AM` | Expended `ACTU_EXP_AM` | Balance |
|---|---:|---:|---:|---:|
| `HUBTOONBASEROW` | 12,763 | **$8.34 B** | $6.42 B | $1.92 B |
| `HUBTOONBASEROWCNDATA` | 12,752 | **$12.23 B** | $9.48 B | $2.75 B |

By phase status (both tables ~same project mix): **Closed** ~7,300 (budget≈expended, balance≈$0);
**Open** ~5,100 (the live balance); Withdrawn ~350; Terminated ~10; Inactive 2.

### 2c. The view, exactly [FACT]
```sql
CREATE VIEW dbo.HUBTOONBASEROWupdateWITHCNPROJ AS
SELECT <all CNDATA columns>
FROM   HUBTOONBASEROWCNDATA
       LEFT OUTER JOIN HUBTOONBASEROW ON CNDATA.ProjectID = BASEROW.ProjectID
WHERE  HUBTOONBASEROW.ProjectID IS NULL
```
Returns CN-phase project rows with **no matching ROW-base row** — i.e. the CN-only projects to append
when building a combined base. Pure reconciliation/ETL gap-finder; materializes nothing.

---

## 3. Lineage — what builds `HUBTOON` [FACT for the views, INFERRED for the exact ETL]

The build source is on the **primary server** as a family of reconciliation views, mapping
one-to-one onto the tables:

| HUBTOON table (TAMSDW) | Built from (Data-Warehouse view) |
|---|---|
| `HUBTOONBASEROW` | `HUBRemisAuthIdRW` |
| `HUBTOONBASEROWCNDATA` | `HUBRemisAuthIdCN` |
| (EN phase variants exist) | `HUBRemisAuthIdEN`, `HUBRemisAuthIdCNENRW` |
| supporting | `HUBPHASEAMOUNTS`, `Reconcilehub`, `Reconcilestipandhub`, `VIEW_AUTH`, `VIEW_AUTHORIZED` |

So: the bus reconciles HUB↔OASIS → results surface in the `HUBRemisAuthId*`/`Reconcile*` views →
a (manual/scheduled) extract materializes them into `HUBTOON*` on TAMSDW so the asset/dTIMS
reporting side can read project funding without reaching back into the HUB.

**Data flows both directions between the two servers:** dTIMS asset/maintenance data flows
TAMSDW → Data-Warehouse (`dtims_transactions`); project financials flow Data-Warehouse → TAMSDW
(`HUBTOON`).

---

## 4. The cross-server join (CRITICAL — different project keys) [FACT]

The two systems identify projects **differently**, so a naive `ProjectId = ProjectID` join returns
**zero rows**. You must bridge through `dbo.Project`:

| Side | Column | Range / form | = |
|---|---|---|---|
| HUB change requests | `PhaseChangeRequest.ProjectId` | int **6 – 14,326** | `Project.Id` (surrogate PK) |
| HUBTOON (TAMSDW) | `HUBTOON.ProjectID` | **year-prefixed** (e.g. `2008001284`) | `Project.ProjectId` (business no.) |

**Bridge:** `PhaseChangeRequest.ProjectId = Project.Id` **AND** `Project.ProjectId = HUBTOON.ProjectID`,
plus `PhaseCode` to align the phase.

**[FACT] validation** — the upstream-bus doc's worked example, project **2008001284** (PLINY–MASON
CO 42, RW0001, `RemisAuthId TR2117G`), appears in `HUBTOONBASEROW` as **Open, $13.54M budget,
$988,406.85 balance** — the exact mid-flight closeout described upstream. The `RemisAuthId` /
`OASIS/HUB Auth` / `EXP_FUND_CD` / `EXP_APPR_CD` values (e.g. `SR2309G`, `UR2050G`, `TR2174G`) are
the same wvOASIS/REMIS authorization keys the bus handshakes on.

---

## 5. The headline correlation — `BGPHRStatusId` → reconciled balance [FACT]

Joining closeout change requests (`IsCRClosure = 1`, deduped to `MAX(BGPHRStatusId)` per
project-phase) to the `HUBTOON` balance, via the `Project` bridge:

### RW basis (`HUBTOONBASEROW`)
| BGPHR | Phase status | Phases | Budget | Expended | **Balance** | Zero-balance |
|---:|---|---:|---:|---:|---:|---:|
| **0** (not reconciled) | Open | 181 | $607.7M | $491.3M | **$116.4M** | 24 / 181 |
| **1** (reconciled, non-fed) | Closed | 4,580 | $1.14B | $1.14B | **$0.83M** | 4,418 / 4,580 |
| 1 | Open *(backlog)* | 24 | $6.4M | $6.2M | $0.15M | 9 |
| 1 | Terminated | 9 | $0.14M | $0.02M | $0.12M | 8 |
| 1 | Withdrawn | 102 | $2.1M | $2.1M | $0 | 102 |
| **4** (reconciled + FMIS, fed) | Closed | 1,298 | $1.29B | $1.29B | **$1.78M** | 1,217 / 1,298 |
| 4 | Open *(backlog)* | 34 | $86.2M | $82.6M | $3.6M | 16 |
| 4 | Inactive | 2 | $3.5M | $3.5M | $0 | 2 |
| 4 | Withdrawn | 244 | $0.6M | $0.6M | $0 | 244 |
| **5** (canceled) | Closed | 5 | $3.2M | $3.2M | $0 | 5 |

### CN basis (`HUBTOONBASEROWCNDATA`) — mirrors RW
| BGPHR | Phase status | Phases | Budget | Expended | **Balance** |
|---:|---|---:|---:|---:|---:|
| **0** | Open | 205 | $763.2M | $637.0M | **$126.2M** |
| 1 | Closed | 4,338 | $1.23B | $1.23B | $0.85M |
| 4 | Closed | 1,390 | $1.77B | $1.77B | $2.03M |
| 4 | Open | 37 | $195.6M | $98.2M | $97.4M |
| 5 | Closed | 7 | $4.7M | $4.7M | $0.01M |

### What it proves [FACT]
1. **BGPHR is the switch that zeros the balance.** When a closure reconciles (`BGPHRStatusId` → 1
   non-federal, or 4 federal/FMIS-approved), the phase flips to **Closed** and balance collapses to
   ≈$0: **96.5%** of non-federal closed phases (4,418/4,580) and **93.8%** of federal closed phases
   (1,217/1,298) sit at **exactly zero balance**.
2. **`BGPHRStatusId = 0` is the unreconciled money.** Closure requested but the OASIS handshake
   hasn't completed → balances remain large: **~$116.4M (RW) + ~$126.2M (CN) ≈ $242M open balance
   on not-yet-reconciled closures.** This is the closeout backlog, in dollars.
3. **`BGPHR = 1/4` but still `Open`** (24 + 34 RW; 23 + 37 CN) = reconciled financially but the phase
   hasn't been flipped Closed yet — the small live tail of in-flight closeouts (notably one CN
   federal cluster still holding **$97.4M**).
4. **`BGPHR = 5`** = canceled closeout (handful, already at zero balance).

`BGPHRStatusId` (primary server) and `HUBTOON` budget/balance (TAMSDW) are the **input and output of
the same wvOASIS closeout reconciliation**.

---

## 6. Reusable queries (read-only; HUBTOON via the TAMSDW link)

**The cross-server correlation (run while connected to `Data-Warehouse`):**
```sql
WITH cr AS (
  SELECT p.ProjectId AS bizproj, pcr.PhaseCode, MAX(pcr.BGPHRStatusId) bgphr
  FROM dbo.PhaseChangeRequest pcr
  JOIN dbo.Project p ON p.Id = pcr.ProjectId      -- surrogate → bridge
  WHERE pcr.IsCRClosure = 1
  GROUP BY p.ProjectId, pcr.PhaseCode
)
SELECT cr.bgphr, h.[RW Phase Status],
       COUNT(*) phases, SUM(h.CURR_BUD_AM) budget,
       SUM(h.ACTU_EXP_AM) expended, SUM(h.[Current Balance]) balance
FROM cr
JOIN OPENQUERY([TAMSDW],
     'SELECT ProjectID, PhaseCode, [RW Phase Status], CURR_BUD_AM, ACTU_EXP_AM, [Current Balance]
      FROM DOTDataWarehouse.dbo.HUBTOONBASEROW') h
  ON h.ProjectID = cr.bizproj AND h.PhaseCode = cr.PhaseCode   -- business no. = Project.ProjectId
GROUP BY cr.bgphr, h.[RW Phase Status]
ORDER BY cr.bgphr, h.[RW Phase Status];
```

**The $242M unreconciled-closeout backlog (BGPHR = 0, balance > 0):**
```sql
WITH cr AS (
  SELECT p.ProjectId AS bizproj, pcr.PhaseCode
  FROM dbo.PhaseChangeRequest pcr
  JOIN dbo.Project p ON p.Id = pcr.ProjectId
  WHERE pcr.IsCRClosure = 1 AND pcr.BGPHRStatusId = 0
  GROUP BY p.ProjectId, pcr.PhaseCode
)
SELECT h.* FROM cr
JOIN OPENQUERY([TAMSDW],
     'SELECT ProjectID, ProjectName, PhaseCode, [RW Phase Status], RemisAuthId,
             CURR_BUD_AM, ACTU_EXP_AM, [Current Balance]
      FROM DOTDataWarehouse.dbo.HUBTOONBASEROW WHERE [Current Balance] <> 0') h
  ON h.ProjectID = cr.bizproj AND h.PhaseCode = cr.PhaseCode
ORDER BY h.[Current Balance] DESC;
```

**HUBTOON totals snapshot:**
```sql
SELECT * FROM OPENQUERY([TAMSDW], '
  SELECT ''RW'' tbl, COUNT(*) rows, SUM(CURR_BUD_AM) budget, SUM(ACTU_EXP_AM) expended,
         SUM([Current Balance]) balance FROM DOTDataWarehouse.dbo.HUBTOONBASEROW
  UNION ALL SELECT ''CN'', COUNT(*), SUM(CURR_BUD_AM), SUM(ACTU_EXP_AM), SUM([Current Balance])
  FROM DOTDataWarehouse.dbo.HUBTOONBASEROWCNDATA');
```

---

## 7. Gotchas & caveats

1. **Two project keys** — always bridge `PhaseChangeRequest.ProjectId (=Project.Id)` ↔
   `Project.ProjectId (=HUBTOON.ProjectID)`. Direct id-to-id joins silently return nothing.
2. **`HUBTOONBASEROW` is not RW-only** — it carries mixed `PhaseCode` (RW0001 + CN000x). Filter by
   `PhaseCode` when you mean a specific phase; the two tables differ by **budget basis**, not by a
   clean RW/CN row split.
3. **Multiple closure CRs per phase** — dedupe with `MAX(BGPHRStatusId)` per (project, phase) or you
   will double-count `HUBTOON` dollars.
4. **`money` precision** — `CURR_BUD_AM`/`ACTU_EXP_AM`/`Current Balance` are SQL `money`; "Closed at
   $0 balance" can show sub-dollar residue — treat `< $1` as effectively zero.
5. **Hand-maintained reporting DB** — `DOTDataWarehouse` is small, key-less, with a dead `…old`
   table and Management-Studio-formatted views. Treat `HUBTOON` as a **snapshot**, not a governed
   live source; refresh cadence is unknown (likely batch, alongside the bus).
6. **PII** — `PermitPortalChargesToTreasuryold` holds applicant name/address/phone/email (one test
   row). `HUBTOON` itself exposes only project-manager names.
7. **Read-only** — TAMSDW reached via linked server as a service account; `rpc_out` off. No writes.
8. **What stays locked** — XML payloads, `OasisFinance` payload tables, and `msdb` job definitions
   are denied. You can analyze the **reconciled outcome** (this doc), not the raw transport.

---

## 8. Bottom line

The wvOASIS financial bus and the TAMSDW `HUBTOON` tables are **one system observed at two points**:
`PhaseChangeRequest.BGPHRStatusId` records *whether* a phase closeout has been reconciled with OASIS
(and FMIS for federal), and `HUBTOON.Current Balance` records the *dollar result* of that
reconciliation. Reconciled (1/4) → Closed → balance ≈ $0; not-yet-reconciled (0) → **~$242M of open
balance** waiting on the handshake. Joinable only through `dbo.Project`. Both ends are readable to
the `DTIMS_Transactions` login even though the raw OASIS payloads are not.

*All figures verified against `Data-Warehouse` (10.69.0.44) and `TAMSDW.DOTDataWarehouse`
(10.6.60.45) at analysis time.*
