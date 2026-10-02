# The I385 / CAM-CAS / BGPHR Bus — WVDOT HUB ↔ wvOASIS Financial Integration

Everything established from the `Data-Warehouse` database (`10.69.0.44`), primarily the
`ExecutionInstance` job log plus the `BGPHRStatusId` footprint on change requests.

> **Confidence key:** **[FACT]** = read directly from the database. **[INFERRED]** = reasoned
> from naming conventions / behavior, not verified (payloads & job definitions live in
> `OasisFinance` and `msdb`, both denied to the `DTIMS_Transactions` login).

---

## 1. What this bus is

The **OASIS financial bus** connects the HUB to **wvOASIS** (the State of WV ERP / accounting
system). It is a **file-based (XML) batch integration** that runs on a fixed schedule. It is the
*live* financial bus — distinct from the AASHTOWare construction interfaces (I337/I338) and the
frozen legacy HWS mainframe feed.

It is a **trio of cooperating processes** plus their response pollers:

| Role | Process (ProcessId) | Direction |
|---|---|---|
| Inbound OASIS finance file | **`I385_0803_FN_HUB`** (22) | OASIS → HUB |
| Financial document push | **`CAS`** (5) | HUB → OASIS |
| Financial document push | **`CAM`** (9) | HUB → OASIS |
| Closeout reconciliation build | **`Generate BGPHR`** (22, variant) | internal |
| Ack poll | **`CAS_Response`** (6) | OASIS → HUB |
| Ack poll | **`CAM_Response`** (10) | OASIS → HUB |
| Ack poll | **`BGPHR_Response`** (23) | OASIS → HUB |

---

## 2. `I385_0803_FN_HUB` — the inbound OASIS finance file [FACT for structure]

- It is an **inbound XML file** ingested from wvOASIS. Each run processes exactly one file; the
  `ExecutionInstance.Name` *is* the filename.
- **Filename anatomy:**
  ```
  I385_0803_FN_HUB_ 2026 06 18 56901 .xml
  └──interface────┘  └──date──┘ └seq┘
  ```
  - `I385` = the legacy WVDOT interface-file id **[FACT it's used; INFERRED what 385 means]**
  - `0803` = Division of Highways **[INFERRED]**
  - `FN` = Finance **[INFERRED]**
  - `HUB` = destination application
  - date = file date; the **5-digit sequence increments globally and tracks alongside
    `ExecutionInstance.Id`** (e.g. file …56901 with run id ~56916) **[FACT]**
- **Volume / span:** 2,576 runs, **2023‑03‑01 → 2026‑06‑18** (current). Avg ~2s, max 41s. **[FACT]**
- **Outcome codes:** `ReturnCode = 1` on every run (its own "file processed" code, ≠ CAS/CAM's
  rc=4). `RunStatus = 3` (completed) on 2,564; `= 2` on the 12 `Generate BGPHR` runs. **[FACT]**
- It fires **first** in each outbound bus slot, then CAS, then CAM. **[FACT]**

**Real examples (from the log):**
```
2026-06-18 14:30:00  I385_0803_FN_HUB_2026061856901.xml   rc=1
2026-06-18 09:30:01  I385_0803_FN_HUB_2026061856879.xml   rc=1
2026-06-18 06:30:02  I385_0803_FN_HUB_2026061856867.xml   rc=1
2023-03-01 11:57:42  I385_0803_FN_HUB_2023030112752.xml   (earliest)
```
The XML **content is not stored in this database** — only the filename + run result. Payloads live
on the integration server / `OasisFinance`. **[FACT]**

---

## 3. CAM & CAS — the financial document push [FACT for behavior, INFERRED for meaning]

- `CAS` (5) and `CAM` (9) fire **together** in each outbound slot — CAS first, CAM a **median 17 s
  later** (range 12 s–4 min). They do real work: CAS avg **5.9 s**, CAM avg **8.7 s**.
- `CAS_Response` (6) and `CAM_Response` (10) are fast pollers (~700 ms) that ingest OASIS
  acknowledgements.
- **Volumes:** CAS 3,609 / CAS_Response 7,188 / CAM 3,590 / CAM_Response 7,213.
- **What CAM vs CAS carry is unverified.** They leave **zero footprint** in `Data-Warehouse` — no
  `UpdatedBy` stamp, no `ExecutionInstanceId` FK, no proc/view reference, only background-noise
  timing overlap. Their payloads are the XML files outside the DB. The only loosely-related column
  anywhere is `CASH_EXP_AM` in the OASIS budget snapshot. **[FACT they're untraceable here;
  INFERRED they're OASIS financial document interfaces]**

---

## 4. BGPHR — the financial closeout reconciliation [FACT for behavior]

**BGPHR is the phase-closeout reconciliation with OASIS.** The decisive evidence:
**100% of records with `BGPHRStatusId > 0` are phase-closure change requests (`IsCRClosure = 1`).**
Nothing that isn't a closure ever gets a BGPHR status. **[FACT]**

- `Generate BGPHR` builds the records; `BGPHR_Response` (23, 5,145 runs) polls back the result.
- BGPHR rides the **same bus and bursts as CAM/CAS** (response trio: CAS_Response +
  BGPHR_Response + CAM_Response). **[FACT]**
- `BGPHR ≈ "Budget/Grant PHase Reconciliation"` **[INFERRED expansion]**

### `BGPHRStatusId` decode (on `dbo.PhaseChangeRequest`) [FACT counts, INFERRED labels]

| Status | Count | Pattern | Meaning |
|---|---:|---|---|
| **0** | 61,253 | not a closure | **Not in BGPHR** (open/active CRs) |
| **1** | 5,788 | all closures; FMIS mostly **N/A** | **Closeout reconciled — non-federal.** 5,612 drove the phase to Closed (terminal success); **42 still Open = the real backlog** |
| **4** | 2,259 | all closures; FMIS mostly **Approved** | **Closeout reconciled + FMIS-approved — federal** |
| **5** | 7 | closures, not sent to REMIS, mostly canceled | **Canceled closeout** (rare) |

Progression: **1 (submitted/reconciled) → 4 (federally approved)**, with **5** = cancel. BGPHR
status lives almost entirely on `PhaseChangeRequest` (only 3 stray rows on
`PhaseFundingChangeRequest`; none on `PhaseFunding`). **Updated live** — most recent change
2026‑06‑18 13:19. **[FACT]**

`BGPHRStatusId` is the **only readable fingerprint of this bus inside `Data-Warehouse`.**

---

## 5. Schedule & rhythm [FACT]

```
OUTBOUND (HUB → OASIS), 3×/business day @ ~06:30 / 09:30 / 14:30:
   I385_0803_FN_HUB_*.xml   (file in, ~2s, rc=1)
   → CAS                    (~6s)
   → CAM                    (~9s)         (CAS leads CAM by ~17s)

INBOUND poll bursts ~90 min later (@ ~08:00 / 11:00 / 16:00), two rounds ~10–20 min apart:
   CAS_Response  →  BGPHR_Response  →  CAM_Response   (each ~<1s, rc=4)
```
- The "~10-minute" cadence people notice = the two response rounds within each burst.
- Median inter-run gap for the response pollers ≈ 20 min; outbound ≈ every 300 min (3×/day).

---

## 6. Reliability [FACT]

- **~99.7% clean.** Response pollers: **zero** failures ever.
- Outbound CAS/CAM: only ~18 lifetime non-success runs (`ReturnCode=6` warnings), clustered on a
  few dates (3-day CAS blip Jan 22–24 2024; CAM Sep 19 & Dec 1 2023). **Last failure 2025‑10‑20.**
- One outlier: a **49-minute** CAS run on 2026‑02‑16 (vs usual ~6s); a cluster of multi-minute CAM
  runs early Feb 2025 (smells like fiscal-period processing).
- Health query:
  ```sql
  SELECT ProcessId, COUNT(*) runs,
         SUM(CASE WHEN RunStatus<>3 OR ReturnCode NOT IN (0,1,4) THEN 1 ELSE 0 END) problems,
         MAX(StartTime) last_run
  FROM dbo.ExecutionInstance
  WHERE ProcessId IN (5,6,9,10,22,23) AND StartTime > DATEADD(day,-30,GETDATE())
  GROUP BY ProcessId;
  ```

---

## 7. Lifecycle context — why the bus exists [FACT + INFERRED]

When a project **phase is closed**, its final budget/expenditure must be reconciled with the OASIS
accounting line (and, for federal phases, the FMIS side) before it can financially close. The bus
does that handshake:

1. A user files a **closure** change request (`IsCRClosure=1`) — e.g. *"Close as is. No final
   invoice."*
2. **`Generate BGPHR`** builds the reconciliation; the **I385/CAS/CAM** push sends it to OASIS.
3. **`BGPHR_Response`** brings back the result → `BGPHRStatusId` set to **1** (non-federal) or
   **4** (federal, FMIS-approved).
4. Once OASIS/FMIS finish, the phase flips to `PhaseStatus = Closed` (the "done" signal).

**Worked example (CR Id 41419, touched 2026‑06‑18):**
- Project `2008001284` **PLINY – MASON CO 42** (US-35, on NHS), phase **RW0001**, $12.75M.
- Closure CR #3, reason *"Close as is. No final invoice. SLR"*, `BGPHRStatusId = 4`.
- 13:19 — staff work the closure (BGPHR → 4); 16:45 — `FMIS_Response Interface` confirms the
  federal side (`RemisAuthId TR2117G`, `HPP0035173`). Phase still Open = closeout mid-flight.

---

## 8. The cutover story [FACT for dates, INFERRED for causation]

- Bus go-live **2023‑03‑01** (BGPHR added then; the HUB app itself launched ~Oct 2021).
- The legacy **HWS mainframe maintenance-charge feed (`HWS.DMAINT`, 11.2M rows, $2.14B)** is
  **frozen at 2024‑06‑28** (end of WV FY2024) — re-stamped daily but receiving no new transactions.
- **Inference:** WVDOT shifted financial/maintenance accounting onto **wvOASIS**, and this bus is
  the live successor. The OASIS side is current (BGPHR edits 2026‑06‑18; OASIS budget snapshot
  `EFBGN_DT` to 2026‑07‑15).

---

## 9. What is NOT in this database [FACT]

- **The XML payloads** (`I385_0803_FN_HUB_*.xml`) — only filenames are logged.
- **What CAM vs CAS specifically carry** — no table/column/proc reveals it.
- **The job definitions** — `msdb.sysjobs` SELECT denied.
- **Any blob/binary data at all** — zero `varbinary`/`image` columns; files live on the server
  filesystem (`C:\inetpub\HUB_PRD\HubAttachments\…`) with only path pointers stored.
- To go deeper requires access to **`OasisFinance`** (payload tables) or **`msdb`** (job steps),
  both denied to the `DTIMS_Transactions` login.

---

## 10. Quick reference — process IDs on this bus

| ProcessId | Name | Runs | Role |
|---:|---|---:|---|
| 22 | `I385_0803_FN_HUB` / `Generate BGPHR` | 2,576 | inbound OASIS XML / BGPHR build |
| 5 | `CAS` | 3,609 | outbound financial push |
| 9 | `CAM` | 3,590 | outbound financial push |
| 6 | `CAS_Response` | 7,188 | ack poll |
| 10 | `CAM_Response` | 7,213 | ack poll |
| 23 | `BGPHR_Response` | 5,145 | closeout-reconciliation ack poll |
