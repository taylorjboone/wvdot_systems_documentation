# How the WVDOT HUB Works & How It Interfaces With Other Systems

Derived from the `Data-Warehouse` database on `10.69.0.44` — primarily the `ExecutionInstance`
job log plus the integration columns, staging fields, and external-import tables found across the
schema.

> **Confidence note.** Interface *names, IDs, run counts, dates, statuses, and column names* are
> facts read directly from the database. Acronym expansions and the identity of some external
> systems (CAM, CAS, BGPHR, W43, I337/I338/I385) are **reasoned inferences** from WVDOT/federal
> naming conventions and the data's behavior; they're marked *(inferred)* where not certain.

---

## 1. What the "HUB" is

The HUB is WVDOT's **central project programming & federal-aid financial management application**
— the system of record for the project lifecycle (Project → Phase → Funding → Change Request →
STIP → obligation → construction → closeout). This `Data-Warehouse` database is its backing/
reporting store.

Its name is literal: it is the **hub** that sits between WVDOT's internal project data and a ring
of external state/federal systems, brokering data both ways. It does not own the money or the
contracts — it **packages project/funding actions, pushes them to the authoritative systems
(FMIS, wvOASIS, REMIS, AASHTOWare), and ingests their responses back.**

---

## 2. `ExecutionInstance` — the integration heartbeat

Every integration run — inbound or outbound — is logged as one row.

| Column | Meaning |
|---|---|
| `Id` | Surrogate run id (referenced by records the run touched) |
| `ProcessId` | Which interface/process ran (see catalog below) |
| `StartTime` / `EndTime` | Run window (sub-second for most; FMIS submits take ~20s) |
| `RunStatus` | **3 = completed** (56,816 of 56,910); 1 = not completed/aborted (81); 2 = in-progress/queued (13) |
| `ReturnCode` | **4 = success** (53,644); 6 = error/warning (350); 5 = partial/pending (234); 0 = ok-no-op (37); 1 = internal-job marker (2,641); 3 = (4) |
| `Name` | Interface name + date stamp, e.g. `FMIS_Response_20260618` |

**Cadence & history.** Go-live ≈ **2021-10-18**; jobs still running **2026-06-18** (current). The
financial response pollers (CAM/CAS) run roughly **every ~10 minutes**, all day, every day —
~7,200 runs each. This is a continuously-scheduled batch integration bus, not a one-off ETL.

**The request/response (async) pattern.** Each external system is driven by a **pair** of
processes: an *outbound action* job and an *inbound `_Response`* poller. The HUB writes a request,
the external system processes it on its own clock, and the `_Response` job later picks up the
acknowledgement (success/failure, assigned IDs) and updates the HUB record. This is classic
file/queue-based asynchronous EAI.

---

## 3. Interface catalog (from `ExecutionInstance.ProcessId` + `Name`)

| PID | Interface | Runs | Direction | Target system |
|---:|---|---:|---|---|
| 14 | `FMIS` (submit) | 3,493 | out | FHWA **FMIS** |
| 12 | `FMIS_Approve` | 3,687 | out | FMIS |
| 11 | `FMIS_Reject` | 2,611 | out | FMIS |
| 2 | `FMIS_Delete` | 2,492 | out | FMIS |
| 19 | `FMIS_Unsign` | 856 | out | FMIS |
| 18 | `FMIS_W43` | 1,555 | out | FMIS *(W43 = a specific FMIS modification/voucher form, inferred)* |
| 25 | `FMIS_ApproveW43` | 696 | out | FMIS |
| 13 | **`FMIS_Response`** | 6,036 | in | FMIS (acknowledgements) |
| 9 | `CAM` | 3,590 | out | **wvOASIS** financial doc *(inferred)* |
| 10 | **`CAM_Response`** | 7,213 | in | wvOASIS |
| 5 | `CAS` | 3,609 | out | **wvOASIS** financial doc *(inferred)* |
| 6 | **`CAS_Response`** | 7,188 | in | wvOASIS |
| 22 | `I385_0803_FN_HUB` / `Generate BGPHR` | 2,576 | in/proc | wvOASIS finance feed (dept **0803**=DOH, **FN**=Finance) |
| 23 | **`BGPHR_Response`** | 5,145 | in | wvOASIS budget/grant-phase reconciliation |
| 17 | `ExternalTablesLoad` | 1,224 | in | Loads the `external.*` snapshot tables from wvOASIS |
| 26 | `M60ExternalTablesLoad` | 1 | in | Same, variant |
| 7 | `SiteManagerI337` | 1,929 | in/out | **AASHTOWare SiteManager** (construction) interface I337 |
| 8 | `SiteManagerI338` | 1,770 | in/out | AASHTOWare SiteManager interface I338 |
| 4 | `REMIS` | 1,169 | out/in | **REMIS** (right-of-way / real estate) |
| 1 | `INBOX_RECALCULATION` | 44 | internal | HUB recompute |
| 3 | `Import Table` | 24 | internal | Generic import |
| 24 | `Update FFD` | 1 | internal | Federal Funding Detail recompute |

---

## 4. The external systems, and how the HUB talks to each

### 4.1 FHWA **FMIS** — federal authorization & obligation *(the "commitment" engine)*
- **Purpose:** submit federal-aid project phases for FHWA authorization (obligation of federal
  funds). This is the system that makes a project "committed."
- **Outbound verbs:** submit (`FMIS`), `FMIS_Approve`, `FMIS_Reject`, `FMIS_Delete`,
  `FMIS_Unsign`, `FMIS_W43`, `FMIS_ApproveW43`. **Inbound:** `FMIS_Response`.
- **State machine** (`dbo.FMISStatus`, 27 states): `N/A → Ready → Submitted → (Pending/Failed) →
  Approved | Rejected`, plus a parallel **FFD-** track for Federal Funding Detail
  (`FFD-Ready → FFD-FMIS Submitted → FFD-FMIS Approved/Reject/Withdrawn`), and lifecycle verbs
  `Reject-Unsign`, `Reject-Delete`, `Reopen`, `Reestablish`.
- **HUB-side fields:** `ProjectPhase.IsSubmittedToFMIS`, `FMISStatusId`, `InitialFMISSubmitDate`,
  `IsInFMISReview`, `FMISSubmittedBy`, `BypassFMIS` (369 CRs bypass), `FMISSubmitGroupId`,
  `FMISProjectEndDate`; result of approval = `RemisAuthId` populated + a `dbo.AuthorizationData`
  CN/EN/RW row with `AUTH_AMT`.

### 4.2 **wvOASIS** — statewide ERP / accounting (CGI Advantage, *inferred*) — the money
- **Purpose:** the authoritative state financial system. The HUB sends financial documents
  (`CAM`, `CAS`) and budget/grant-phase reconciliation (`BGPHR`), and receives acknowledgements
  (`CAM_Response`, `CAS_Response`, `BGPHR_Response`) — the **highest-volume interfaces** in the
  system, polling every ~10 min.
- **Inbound master/snapshot loads** (`ExternalTablesLoad`):
  - `external.BUD_STRU_PHASE_PROG2` — the **budget-structure snapshot** (52K rows: budget,
    expenditure, encumbrance, fund/appropriation codes per project-phase-funding-line). Provenance
    columns `SourceFileName`, `SourceFileHash`, `ExecutionInstanceId`, `ImportedDate`.
  - `dbo.OasisCustomers` — customer/vendor master imported from OASIS (same provenance columns).
- **HUB-side fields:** `ProjectPhase.IsSubmittedToOASIS`, `Project.InterfacedToOasis`,
  `PhaseChangeRequest.OasisStagingId`, `OasisEffectiveToDate`; `BGPHRStatusId` across
  `PhaseFunding`, `PhaseFundingChangeRequest`, `PhaseChangeRequest`, `ProjectPhase`.
- `I385_0803_FN_HUB` = a **fixed-format interface file** (legacy "I###" naming), dept **0803**
  (Division of Highways), **FN**=Finance, feeding the HUB *(inferred)*.

### 4.3 **AASHTOWare Project / SiteManager** — letting & construction administration
- **Purpose:** contract letting, awards, and construction management. The HUB exchanges data via
  `SiteManagerI337` / `SiteManagerI338` (SiteManager interface file numbers).
- **Data landed:** `AWP_ChangeOrders`, `AWP_Dates`, `AWP_HUBDates` — contract/letting milestone
  dates: `FEPA_DT`, `WKBG_DT`, `NTP_DT` (notice to proceed), `SWKC_DT`, `LET_DT`, `PublicationDate`,
  `EXEC_DT`, `FEA_DT`, `AWARD_DT`; keyed by `AWPContractID`, `ProposalID`, `ContractNumber`,
  `StateProjectNumber`, `FederalProjectNumber`. ("AWP" = AASHTOWare Project.)

### 4.4 **REMIS** — Real Estate Management Information System (right-of-way)
- **Purpose:** right-of-way / real-estate authorizations. `REMIS` process (PID 4).
- **HUB-side fields:** `PhaseChangeRequest.IsSentToREMIS` (**57,578** CRs), `IsSentToREMIS` on
  `PhaseFundingChangeRequest`; `RemisAuthId` and the phase-split variants `RemisAuthIdCN/EN/RW`
  (view `HUBRemisAuthIdCNENRW`). The `HUBRemisAuthId*` views reconcile authorization IDs per phase.

### 4.5 **DTIMS** — Deighton Total Infrastructure Management System (pavement/asset mgmt)
- **Purpose:** pavement & asset management. `dbo.dtims_transactions` (≈650K rows) is the largest
  table; `dbo.DWHUBMaxTransDate` is a **watermark** of the last transaction date per
  `PROG_CD + PHASE_CD` (used to do incremental exports). `WORK_CODE_XWALK` maps `PT_WORK_CODE` to
  assets. *(This is the system the original `export_om_wvdot.py` feeds.)*

### 4.6 **PTS** — legacy Project Tracking System (predecessor)
- **Purpose:** the system the HUB replaced. `dbo.PTSData` holds pre-conversion project records
  (`PROJ_KEY`, federal numbers, obligations, dates). Migration artifacts: `MigratedData` flags,
  `CONVERSION USER` / `2021-10-18` created stamps, `FedProjNoSequenceFromConversion`, and
  "Historical PTS Only" allocation codes.

### 4.7 **eGov** — online payment portal
- `dbo.Credit_Card_Transactions_From_EGOV` — credit-card transactions imported from the state
  eGov payment system.

### 4.8 **TAMS** — Transportation Asset Management System / data warehouse (export target)
- Views `ExportforROWtoTAMSProjectData`, `ExportforROWtoTAMSDataExporttoTAMSDWH(addCNdata)` push
  ROW/project/authorization data (with `OASIS/HUB Auth`, `RemisAuthId`) out to the TAMS warehouse.

### 4.9 **STIP governance** — MPO / PRC (not a system, a workflow)
- `PhaseSTIP.SentToMPODate`, `MPOApprovalDate`, `SentToPRCDate`, `PRCApprovalDate` capture the
  Metropolitan Planning Organization and Programming Review Committee approvals that move a project
  onto the State Transportation Improvement Program.

### 4.10 **GIS / LRS**
- `IsGIS` flags and `RouteSegment` (linear referencing: `RouteIdStr`, mileposts, FAS/NHFC/sign
  system) tie projects to the geospatial network.

---

## 5. The audit trail — how a record links back to an interface run

The HUB stamps records with the run that last touched them:

- `ExecutionInstanceId` / `LastExecutionInstanceId` on `Project`, `ProjectPhase`,
  `PhaseChangeRequest`, `external.BUD_STRU_PHASE_PROG2`, `OasisCustomers` → FK to
  `ExecutionInstance.Id`. (4,867 change requests carry an `ExecutionInstanceId`.)
- **Staging queues:** `InterfaceStagingId` (4,867 CRs), `OasisStagingId` (5) — records parked in a
  staging area awaiting/holding an interface action.
- **`ChangeCheck`** (rowversion/timestamp) on nearly every table → optimistic concurrency + change
  detection for "what changed since the last interface run."
- **Import provenance:** `SourceFileName` + `SourceFileHash` + `ImportedDate` on the OASIS-loaded
  tables → idempotent, hash-verified file ingestion.

So for any phase you can answer *"which interface run last acted on this, when, and did it
succeed?"* by joining `LastExecutionInstanceId → ExecutionInstance`.

---

## 6. End-to-end lifecycle as an integration flow

```
 HUB (this app)                         External systems
 ─────────────                          ────────────────
 1. Create Project + Phases
 2. Program on STIP  ───────────────▶   MPO approval / PRC approval (dates recorded)
 3. Build PhaseFunding
 4. Submit funding  ───────────────▶    FMIS (FMIS_*), status Ready→Submitted
        ◀── FMIS_Response ──────────    FMIS returns Approved  ⇒ federal OBLIGATION
                                        ⇒ RemisAuthId + AuthorizationData  (= "COMMITTED")
 5. Mirror financials  ─────────────▶   wvOASIS (CAM/CAS), IsSubmittedToOASIS
        ◀── CAM/CAS/BGPHR_Response ─    OASIS acks; budget structure flows back
        ◀── ExternalTablesLoad ─────    external.BUD_STRU_PHASE_PROG2 (budget/actuals/encumbrance)
 6. Right-of-way  ──────────────────▶   REMIS (IsSentToREMIS, RemisAuthId CN/EN/RW)
 7. Let & build  ◀──────────────────    AASHTOWare Project / SiteManager (I337/I338)
                                        AWP_* dates: LET → AWARD → NTP → EXEC
 8. Expenditures accrue in OASIS  ──▶    imported back: BUD_STRU actuals, DWHUBMaxTransDate
 9. Pavement/asset work  ──────────▶    DTIMS (dtims_transactions)
10. Closeout  ⇒ PhaseStatus = Closed
```

This is exactly why the earlier analyses work the way they do:
- **"Committed"** = the FMIS obligation step (4) succeeded — read from `AuthorizationData` /
  `FMISStatus=Approved` / OASIS execution.
- **"Done"** = step 10, `PhaseStatus=Closed`, corroborated by OASIS lines going inactive.
- **Cost / funding-left** = the OASIS budget structure imported in step 5/8
  (`CURR_BUD_AM − ACTU_EXP_AM − ENC_AM`).

---

## 7. Operational health (what the log tells you)

- **99.7%** of runs complete (`RunStatus=3`); failures/warnings concentrate in `FMIS`
  (`ReturnCode` 5 ×226, 6 ×5) and `FMIS_Reject`/`FMIS_ApproveW43` — i.e., the federal interface is
  the most error-prone, as expected (FHWA-side validation).
- The **OASIS pollers (CAM/CAS) dominate volume** and run cleanly (`ReturnCode=4` almost always).
- To monitor: query `ExecutionInstance` for `RunStatus<>3 OR ReturnCode NOT IN (0,1,4)` over the
  last N days, grouped by `ProcessId`, to surface failing interfaces.

```sql
-- interface health, last 30 days
SELECT ProcessId, MAX(Name) sample, COUNT(*) runs,
       SUM(CASE WHEN ReturnCode NOT IN (0,1,4) OR RunStatus<>3 THEN 1 ELSE 0 END) problems,
       MAX(StartTime) last_run
FROM dbo.ExecutionInstance
WHERE StartTime > DATEADD(day,-30,GETDATE())
GROUP BY ProcessId ORDER BY problems DESC, runs DESC;
```
