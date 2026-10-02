# WVDOT HUB — Paving Project Analysis Logic

Reference spec for the two workbooks produced:

- **Committed** → `NHS_Paving_2026_Segment_Cost_Breakdown.xlsx` (committed / committed-or-programmed paving)
- **Past / Done** → `Paving_DONE_RouteId_Cost_Distribution.xlsx` (completed paving)

Both share the same foundation (connection, paving definition, cost sourcing, route
distribution, Federal-Aid classification). They differ only in the **status filter** and the
**dates** used.

---

## 0. Connection

```
server   = 10.69.0.44        # IP, NOT the named host "dotb6pwsql" (which does not resolve here)
port     = 1433
database = Data-Warehouse
login    = DTIMS_Transactions
driver   = pymssql           # no ODBC / sqlcmd installed
```
Note: bracket the schema in queries — `[external].[BUD_STRU_PHASE_PROG2]` (`external` is reserved).
The login lacks `VIEW DATABASE STATE`, so use `COUNT(*)`, not `sys.dm_db_partition_stats`.

---

## 1. Key tables & join keys

| Table | Role | Key columns |
|---|---|---|
| `dbo.Project` | Project master | `Id` (internal), `ProjectId` (year-based number e.g. `2018000503`), `ConstructionCodeID`, `NHSId`, `ProjectName`, `StateProjectNo` |
| `dbo.ProjectPhase` | One row per phase | `Id`, `ProjectId`→`Project.Id`, `PhaseTypeId`, `PhaseStatusId`, `ParticipatingAmount`, `PhaseStartDate`, `PhaseEndDate`, `FMISStatusId`, `RemisAuthId` |
| `dbo.PhaseType` | Phase kind | 1=ENG, 2=ROW, **3=CON (construction)** |
| `dbo.PhaseStatus` | Phase status | `Code`: O=Open, **C=Closed**, I=Inactive, W=Withdrawn, T=Terminated |
| `dbo.ConstructionCode` | Work type | `Id`, `Code`, `Name`, `TAMPSubCategory` |
| `dbo.ProjectConstructionCode` | Project↔code (many-to-many) | `ProjectId`→`Project.Id`, `ConstructionCodeId` |
| `dbo.PhaseMilestone` | Phase milestones | `PhaseId`→`ProjectPhase.Id`, `MilestoneId`, `ActualDate`, `ScheduleDate` |
| `dbo.Milestones` | Milestone lookup | 31=START CONSTRUCTION, **32=COMPLETE CONST.**, 3=CONSTRUCTION PHASE END |
| `dbo.AuthorizationData` | FMIS authorization (= federal obligation) | `PROJ_KEY`=Project.ProjectId, `PHASE_TYPE` (CN/EN/RW), `AUTH_AMT`, `EXP_AMT` |
| `dbo.PhaseSTIP` | STIP programming | `PhaseChangeRequestId`, `CurrentObligationDate`, `OriginalObligationDate` |
| `dbo.PhaseChangeRequest` | links STIP→project | `Id`, `ProjectId`→`Project.Id` |
| `[external].[BUD_STRU_PHASE_PROG2]` | OASIS budget/execution | `PROG_CD`=Project.ProjectId, `PHASE_CD` (CN0001…), `CURR_BUD_AM`, `ACTU_EXP_AM`, `ENC_AM`, `ACT_FL` |
| `dbo.FMISStatus` | FMIS status names | `Name` ('Approved', …) |
| `dbo.RouteSegment` | Route segments per project | `ProjectId`→`Project.Id`, `RouteIdStr`, `RouteId`, `FASId`, `SignSystemId`, `NHFCId`, `WVFCLId`, `StartMilepoint`, `EndMilePoint`, `Length`(⚠ unreliable) |
| `dbo.FAS` | Federal-Aid System | 1=Interstate, 2=NHS, 3=STP, 4=Intermodal Connectors, 5=Non-Federal-Aid |

**The universal join key across systems** is the year-based project number:
`Project.ProjectId` == `BUD_STRU_PHASE_PROG2.PROG_CD` == `AuthorizationData.PROJ_KEY`.
Internal `Project.Id` joins to `ProjectPhase.ProjectId`, `RouteSegment.ProjectId`,
`ProjectConstructionCode.ProjectId`.

---

## 2. Paving definition (shared)

"Paving" = the **resurfacing / overlay program** (excludes new road, added lanes, interchanges).
`ConstructionCode.Id` set:

```
7   Pave (HMA or PCC) on existing road        29  Cold In Place Recycling (CIR)
8   Minor HMA O/L 1½"-2"                       32  Micro Surfacing
9   Skip-Resurface (HMA or PCC)               33  Scarify (Pulverize)
15  Minor Diamond Grinding (code 104)         34  Remove Overlay(s)
19  Pave (Surface Treatment) (code 13)        65  HFST - High Friction Surface Treatment (code 59)
20  Resurface (Surface Treatment) (code 14)   73  Ultra Thin HMA O/L < 1½" (code 67)
21  Skip-Resurface (Surface Treatment)(15)    74  Major HMA O/L > 2" (code 68)
                                              81  Major Diamond Grinding w/ Concrete Rehab (75)
```
```sql
PAV = (7,8,9,15,19,20,21,29,32,33,34,65,73,74,81)

-- a project is "paving" if its primary OR any secondary construction code is in the set:
WHERE p.ConstructionCodeID IN PAV
   OR p.Id IN (SELECT ProjectId FROM dbo.ProjectConstructionCode WHERE ConstructionCodeId IN PAV)
```

---

## 3. Project cost (shared)

`ParticipatingAmount` is **only populated for ~542 of newer phases**; older/closed jobs store $0
there and the real cost lives in OASIS actual expenditure. Use a **best-available coalesce** and
record which source was used:

```
Project Cost = first non-zero of:
  1. ProjectPhase.ParticipatingAmount (CN phase)           -> "Participating"
  2. SUM(BUD_STRU.ACTU_EXP_AM) where PHASE_CD like 'CN%'    -> "OASIS actual exp"
  3. SUM(AuthorizationData.EXP_AMT) where PHASE_TYPE='CN'   -> "FMIS expended"
  4. SUM(BUD_STRU.CURR_BUD_AM) CN                           -> "OASIS budget"
  5. SUM(AuthorizationData.AUTH_AMT) CN                     -> "FMIS authorized"
```
When a project has multiple CN phases, pick ONE with
`ROW_NUMBER() OVER (PARTITION BY Project.Id ORDER BY ParticipatingAmount DESC, PhaseStartDate DESC)`
to avoid double-counting against the per-project OASIS sums.

---

## 4. Route-level cost distribution (shared) — THE IMPORTANT PART

Distribute each project's cost across its **individual Route IDs**, weighted by length.

1. **Segments**: `RouteSegment.ProjectId = Project.Id`.
2. **Segment length = `EndMilePoint - StartMilepoint`** (absolute value).
   ⚠ **Do NOT use `RouteSegment.Length`** — it frequently repeats the *project total* on every
   segment (e.g. all 13 segments showing `42.660`), which silently turns the split into an even
   split. The milepost span is the only reliable length.
3. **Group by `RouteIdStr`** — each distinct LRS route id is its own row. Do **not** group by the
   integer `RouteId` (route number); IDs like `1540011000000`, `1540011070000`, `1540011080000`
   are *separate* routes and must each get their own line.
4. Route length = Σ(segment spans) for that `RouteIdStr`. Project total = Σ(all route lengths).
5. **% of project** = route length / project total length.
6. **Allocated cost** = Project Cost × (% of project).
7. Zero-length project (all spans 0) → split evenly across its route ids.

`RouteIdStr` is stored/exported as **text** to preserve leading zeros.
Note: directional segments (NB/SB) under the same route id are summed, so divided highways count
both directions (directional miles, not centerline).

---

## 5. Federal-Aid System classification (shared)

Classify by `RouteSegment.FASId` (the FHWA federal-aid system), per the user's choice:

```
1 = Interstate     2 = NHS     3 = STP     4 = Intermodal Connectors     5 = Non-Federal-Aid
```
- **Route-id class** = dominant `FASId` within that route id (by length).
- **Project class** = dominant `FASId` across the whole project (by mileage).

Confirmed equivalences on this data: strict interstate via **SignSystemId=2 == FASId=1 == NHFCId in
(2,9)** — all identical (68/68 segments). `WVFCLId=1` ("Expressway") is *broader* (440 mi vs 197 mi)
because it includes non-interstate freeways (Corridor H, ADHS). FAS chosen for the cleaner hierarchy.

---

# PART A — COMMITTED projects logic

### The commitment ladder (point of no return)
"Committed" = the federal **construction obligation** has happened (or construction is already
executing). In federal-aid terms that is the legal point of no return.

| Tier | Meaning | Test |
|---|---|---|
| 0 Shell | CN phase, no budget | none of below |
| 1 Programmed | on STIP / funded, not obligated | `PhaseSTIP.CurrentObligationDate` set **or** CN `ParticipatingAmount > 0` |
| 2 **Obligated (COMMITTED)** | FMIS authorized | `AuthorizationData` CN row `AUTH_AMT>0` **or** `FMISStatus='Approved'` |
| 3 Contract Awarded (> committed) | CN encumbered | OASIS CN `ENC_AM > 0` |
| 3 Under Construction (> committed) | CN spending | OASIS CN `ACTU_EXP_AM > 0` |

### "Committed" filter (committed OR anything past it)
```sql
EXISTS (SELECT 1 FROM dbo.AuthorizationData a
        WHERE a.PROJ_KEY=Project.ProjectId AND a.PHASE_TYPE='CN' AND a.AUTH_AMT>0)        -- obligated
OR EXISTS (SELECT 1 FROM [external].[BUD_STRU_PHASE_PROG2] b
        WHERE b.PROG_CD=Project.ProjectId AND LEFT(b.PHASE_CD,2)='CN'
          AND (b.ACTU_EXP_AM>0 OR b.ENC_AM>0))                                            -- executing/awarded
OR (CN phase) FMISStatus.Name='Approved'                                                  -- FHWA approved
```
This is `>= committed` automatically (the OR captures awarded + under-construction + complete).
Completed-but-cancelled (`PhaseStatus` W/T) should still be excluded if you want live commitments.

### "Committed OR Programmed" (one step looser)
Add to the above:
```sql
OR EXISTS (SELECT 1 FROM dbo.PhaseSTIP s
           JOIN dbo.PhaseChangeRequest pcr ON pcr.Id=s.PhaseChangeRequestId
           WHERE pcr.ProjectId=Project.Id AND s.CurrentObligationDate IS NOT NULL)        -- on STIP
OR (CN phase) ParticipatingAmount > 0                                                     -- funded/budgeted
```

### Year for committed work
**Construction-start year** = `YEAR(ProjectPhase.PhaseStartDate)` for the CN phase (`PhaseTypeId=3`).
(Used `=2026` for the committed deliverable.)
⚠ Future years (2027/2028) return **0 committed** by design — federal obligation does not happen
1–2 years ahead, so those projects are only *programmed*, never yet committed.

---

# PART B — PAST / DONE projects logic

### "Done" definition (the best completion signal)
A construction job is **DONE** when its CN phase is **Closed**:
```sql
ProjectPhase.PhaseTypeId = 3                 -- construction
AND PhaseStatus.Code = 'C'                   -- Closed  (NOT W=Withdrawn, T=Terminated)
```
Why this one: best-populated (6,744 CN phases) and **98.7% corroborated** by OASIS budget lines
going inactive (`ACT_FL=0`). It means construction complete **and** financially closed out.

Secondary / corroborating signals (not the primary flag):
- `PhaseMilestone` `MilestoneId=32` ("COMPLETE CONST.") with `ActualDate` = physical completion
  (under-populated; ~3,234 phases; **filter `ActualDate <= today`** — some are future "actuals").
- OASIS `ACT_FL=0` + `ENC_AM=0` + fully expended = financially wound down.
- 479 phases are physically complete (have the milestone) but not yet Closed = closeout pending.

### Start & end years for done work
```
Year Started = YEAR( COALESCE( START CONSTRUCTION actual (MilestoneId=31, ActualDate<=today),
                               ProjectPhase.PhaseStartDate ) )
Year Ended   = YEAR( COALESCE( COMPLETE CONST. actual (MilestoneId=32, ActualDate<=today),
                               CONSTRUCTION PHASE END actual (MilestoneId=3, ActualDate<=today),
                               ProjectPhase.PhaseEndDate ) )
```

### Result shape
Done paving = 2,906 projects, $1.47B; 2,818 have route segments → distributed ($1.379B); 88 have no
segments (excluded from the route distribution; carry the ~$93M difference).

---

## 6. Funding LEFT (remaining balance) — OASIS

```sql
Remaining = CURR_BUD_AM - ACTU_EXP_AM - ENC_AM     -- per BUD_STRU_PHASE_PROG2 line
```
- `CURR_BUD_AM` = authorized budget, `ACTU_EXP_AM` = spent, `ENC_AM` = encumbered (under contract).
- Filter `LEFT(PHASE_CD,2)='CN'` for construction only; `ACT_FL=1` for active lines only.
- Construction-wide today: $13.77B budget − $11.02B spent − $0.05B encumbered = **$2.70B remaining**.
- ~170 lines are negative (overspent) — keep or floor at 0 depending on use.

---

## 7. Data-quality caveats (learned the hard way)

1. **`RouteSegment.Length` is unreliable** — often repeats the project total. Use `EndMP - BegMP`.
2. **Group by `RouteIdStr`, not `RouteId`** — the integer route number lumps distinct LRS routes.
3. **`ParticipatingAmount` is sparse** for older/closed phases → fall back to OASIS actual expenditure.
4. **Milestone `ActualDate` can be in the future** (expected dates mis-entered) → always `<= GETDATE()`.
5. **One CN phase per project** (ROW_NUMBER dedup) to avoid double-counting against OASIS per-project sums.
6. **Future fiscal years can't be "committed"** — they only reach "programmed."
7. **No-segment projects** can't be distributed (88 done, 6 in the 2026 committed set) — report separately.
8. **`PhaseStatus` W/T are cancelled**, not done — never count them as completed.
9. Strict interstate = SignSystem=2 = FAS=1 = NHFC interstate (identical); WVFCL Expressway is broader.
