# Non-cost progress signals in the AASHTOWare AMS API

> Environment: `ams-lab` / `awdemo` · Verified: 2026-09-30

## Why look past `PercentPaid`

`Contract.PercentPaid` and `Contract.PercentCompleteAward` are both dollar-derived: they answer "how much money has been posted against this contract?", not "how much of the physical work is finished?". Cost lags physical completion (retainage, unpaid finals, billing cadence) and can also *lead* it (mobilization payments, stored materials). To triangulate real progress, the API exposes six other signals — this document describes each, shows how to query it, and prints its value for three example contracts that span the lifecycle.

## The three example contracts

Chosen from `awdemo` to cover a pre-construction, mid-flight, and near-complete state.

| Id | Name | Status | Prime vendor | Awarded | Paid | `PercentPaid` |
|---:|---|---|---|---:|---:|---:|
| **283** | 00378_KE | Pending | Bacco Construction Company | $17,865,175 | $0 | — |
| **269** | 120157-JAF4 | Active | Van Buren County Road Commission | $1,454,677 | $90,814 | 6.24 |
| **282** | WHITEOAK BRIDGE | Active | Carl Engineers Inc. | $1,204,969 | $1,147,110 | 95.01 |

All three sit in the same `WorkflowPhase` ("Active Contract", phase order 200). That flatness is itself a finding — see signal #6.

---

## 1. `ContractProgressSchedule.ActualPercentComplete`

The cleanest non-cost signal on paper: a dated time series of physical progress recorded by the engineer, with matching `ProjectedPercentComplete` for the plan. One row per progress reading (typically monthly).

**Fields:** `Id`, `ContractId`, `ScheduleDate`, `ActualPercentComplete`, `ProjectedPercentComplete`, `Description`.

**Query:**

```
GET /awdemo/ContractProgressSchedules?$filter=ContractId eq 282&$orderby=ScheduleDate
```

**Example results:**

| Contract | Rows | Notes |
|---:|---:|---|
| 283 | 0 | Nothing recorded |
| 269 | 0 | Nothing recorded |
| 282 | 0 | Nothing recorded |

**Caveat.** No `ContractProgressSchedule` rows exist for any of the three demo contracts. The field is present in the model and this is the metric to prefer *when it is populated*, but production coverage will depend on whether the agency's project engineers actually log it — expect gaps.

---

## 2. `ContractProjectItem.PercentItemComplete`

Per-item physical completion, expressed 0–100. Rolled up across a contract's project items this gives an average or a "done / total" ratio that's independent of dollars.

**Fields:** `Id`, `ContractProjectId`, `RefItemId`, `PercentItemComplete`, plus `Quantity`/`CurrentQuantity` fields for the underlying take-off.

**Query (join via `ContractProjects` because there is no direct `ContractId`):**

```
GET /awdemo/ContractProjects?$filter=ContractId eq 282&$select=Id
GET /awdemo/ContractProjectItems?$filter=ContractProjectId in (<ids>)
    &$select=PercentItemComplete
```

**Example results:**

| Contract | ≥100% complete / total items | Average `PercentItemComplete` |
|---:|:---:|---:|
| 283 | 0 / 24 | 0.0% |
| 269 | 0 / 76 | 0.2% |
| 282 | 49 / 49 | 100.0% |

**Interpretation.** Contract 282's 100% here vs. 95% cost-paid is the classic "physically done, waiting on final estimates and retainage" pattern. Contract 269's 0.2% average with $90k paid says mobilization has been billed but almost no items have been posted as physically placed — the money-based `PercentPaid` of 6.24% overstates on-the-ground progress here.

---

## 3. `ContractItem.ItemComplete`

The boolean cousin of signal #2: one flag per contract line item, set when all planned quantities have been placed. Cheaper to query (no project-item join needed) but coarser.

**Fields:** `Id`, `ContractId`, `LineNumber`, `ItemComplete`, `Quantity`, `QuantityPaidToDate`.

**Query:**

```
GET /awdemo/ContractItems?$filter=ContractId eq 282
    &$select=LineNumber,ItemComplete,Quantity,QuantityPaidToDate
```

**Example results:**

| Contract | `ItemComplete = true` / total items |
|---:|:---:|
| 283 | 0 / 24 |
| 269 | 0 / 76 |
| 282 | 49 / 49 |

**Interpretation.** Same story as signal #2, one bit per item instead of a percentage. Useful for a quick "is everything done?" flag; use signal #2 when you want partial-completion resolution.

---

## 4. `ContractTime` records

Not a percentage — a table of dated milestones and time trackers. Every contract has ~7–10 rows in one of four subtypes:

- **Informational** — key dates: Awarded, Notice to Proceed, Work Began, Execution, Letting, Contract Closed For CRLMS, Price Adjustment Base.
- **Available Time** — the time-tracking rows that *do* carry a `PercentComplete` (0.0 in every demo case observed).
- **Completion Date** — milestone deadlines (e.g. "Roadway open").
- **Recurring** — periodic events.

**Fields:** `Description`, `Type`, `Name`, `EffectiveDate`, `ActualCompletionDate`, `PercentComplete`, `Status`.

**Query:**

```
GET /awdemo/ContractTimes?$filter=ContractId eq 282
```

**Example results (Informational rows with an actual date):**

| Milestone | Contract 283 | Contract 269 | Contract 282 |
|---|:---:|:---:|:---:|
| Letting Date | 2014-05-22 | 2020-10-12 | 2019-02-14 |
| Awarded Date | 2021-01-01 | 2022-07-11 | 2024-08-01 |
| Notice to Proceed | 2021-01-02 | 2022-07-11 | 2024-08-01 |
| Execution Date | — | 2022-07-11 | 2024-08-01 |
| Work Began | — | — | 2024-08-01 |
| Contract Closed for CRLMS | — | — | — |

**Interpretation.** Contract 283 shows the "awarded but not executed" gap (no Execution or Work Began). Contract 269 is executed but no Work Began Date. Contract 282 has Work Began but not Contract Closed. Combined with a planned end date these dates would give a time-elapsed %, but the demo `Available Time.PercentComplete` fields all sit at 0.0, so on this dataset you'd compute it yourself from the milestone dates.

---

## 5. `DailyWorkReports`

Count and date range of DWRs filed by the field inspector. The single strongest "boots-on-the-ground" signal — a contract that stops receiving DWRs is either finished or stalled, regardless of the dollar state.

**Fields:** `Id`, `ContractId`, `DwrDate` (not `ReportDate`), `Status`, `Sequence`, `InspectorId`, `HasContractors`, `HasWorkItems`.

**Query:**

```
GET /awdemo/DailyWorkReports?$filter=ContractId eq 282
    &$orderby=DwrDate
    &$select=Id,DwrDate,Status,Sequence
```

**Example results:**

| Contract | DWR count | First | Last |
|---:|---:|---|---|
| 283 | 0 | — | — |
| 269 | 3 | 2021-09-21 | 2023-01-04 |
| 282 | 13 | 2024-08-01 | 2024-09-03 |

**Interpretation.** Contract 283 (Pending) has never seen a DWR, consistent with pre-construction. Contract 269 has three DWRs spread over 16 months — very sparse, suggests the contract hasn't really been active in the field. Contract 282's 13 DWRs in one month look like a normal short bridge job. **DWR cadence** — count per month over the last N months — is often more informative than the raw count.

---

## 6. `WorkflowPhase` (categorical, not a percentage)

Each contract has a `WorkflowPhaseId` pointing at a lifecycle phase with a `PhaseOrder` integer (`Preconstruction` early, `Closed` late). Coarse but useful for filtering.

**Fields:** `Id`, `Description`, `PhaseName`, `PhaseOrder`, `WorkflowId`, `RuleName`.

**Query:**

```
GET /awdemo/Contracts?$filter=Id eq 282&$expand=WorkflowPhase&$select=Id,WorkflowPhaseId
```

**Example results:**

| Contract | `WorkflowPhase.Description` | `PhaseOrder` |
|---:|---|---:|
| 283 | Active Contract | 200 |
| 269 | Active Contract | 200 |
| 282 | Active Contract | 200 |

**Interpretation.** All three sit in the same phase, which is why the signal has low resolution here — `WorkflowPhase` is a good coarse filter ("only active contracts") but doesn't distinguish 5%-done from 100%-done inside a phase. Combine it with signals 2/3/5 for anything finer.

---

## Recommended composite

For a single "physical progress" number per contract, in priority order:

1. If `ContractProgressSchedules` has recent rows → use the latest `ActualPercentComplete`.
2. Else if any project items have `PercentItemComplete > 0` → use their average or completion ratio (signal #2).
3. Else fall back to `count(DWRs in last 30 days)` as an activity proxy.
4. Always carry `WorkflowPhase.PhaseOrder` alongside so consumers can distinguish "0% because it hasn't started" from "0% because it's stalled".

Cost-side percentages (`PercentPaid`, `PercentCompleteAward`) belong in the same dashboard row as these — they answer a different question, and the gap between them and the physical signals is often the most interesting cell.
