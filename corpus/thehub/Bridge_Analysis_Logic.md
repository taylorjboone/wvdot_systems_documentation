# WVDOT HUB — Bridge Project Analysis Logic

Reference spec for the two bridge workbooks produced. This mirrors
`Paving_Analysis_Logic.md` (same connection, cost sourcing, commitment ladder, "done"
definition, Federal-Aid classification) and differs in two ways:

1. **Scope** = bridge construction codes (not the resurfacing/overlay set).
2. **Asset distribution** = each project's cost is split across its individual bridge
   **structures** weighted by **deck square footage**, not across route ids by length.

Deliverables:

- **Committed** → `Bridge_COMMITTED_2026_DeckArea_Cost_Breakdown.xlsx`
  (committed-or-programmed, construction-start 2026)
- **Past / Done** → `Bridge_DONE_DeckArea_Cost_Distribution.xlsx` (completed bridges)

---

## 0. Connection

```
server   = 127.0.0.1,1434     # SSH tunnel to the WVDOT SQL Server (per dot12 .env)
database = Data-Warehouse
login    = DTIMS_Transactions
driver   = pymssql
```
Bracket reserved schema names — `[external].[BUD_STRU_PHASE_PROG2]`. The login lacks
`VIEW DATABASE STATE`, so use `COUNT(*)`, not `sys.dm_db_partition_stats`.

Output: `openpyxl`. Build script: `build_bridge.py`.

---

## 1. Bridge scope (THE FIRST DIFFERENCE FROM PAVING)

"Bridge" = WVDOT's own asset class. A `ConstructionCode` is a bridge code when
`TAMPSubCategory = 'Bridge'`, plus the two unambiguous structure codes tagged `None`
(Pedestrian Bridge, Other Bridge Work). **24 `ConstructionCode.Id` values:**

```
BR = (11,12,13,14, 36,37,38,39, 40,41, 42,43,44,45,46,48,49,50,52,53, 70,77,79,80)
```
| Id | Code | Name | | Id | Code | Name |
|---|---|---|---|---|---|---|
| 11 | 100 | Minor Superstructure Repair | | 44 | 38 | Replace or Renovate Deck |
| 12 | 101 | Major Superstructure Repair | | 45 | 39 | Renovate Deck |
| 13 | 102 | Slip Line Major Culverts | | 46 | 40 | Clean & Paint |
| 14 | 103 | Major Culvert Replacement | | 48 | 42 | HMA Overlay (bridge) |
| 36 | 30 | Widen Existing Bridge | | 49 | 43 | Repair Damage (bridge) |
| 37 | 31 | Replace (condition, no added cap.) | | 50 | 44 | Remove Overlay(s) (bridge) |
| 38 | 32 | Replace (roadway relocation) | | 52 | 46 | LATEX Modified Concrete O/L |
| 39 | 33 | Construct New Bridge | | 53 | 47 | Rehab w/Shotcrete |
| 40 | 34 | Pedestrian Bridge *(TAMP=None)* | | 70 | 70 | Replace Bridge (added cap. >12') |
| 41 | 35 | Other Bridge Work *(TAMP=None)* | | 77 | 71 | Repair/Replace Expansion Joints |
| 42 | 36 | Strengthen Sub/Superstructure | | 79 | 73 | Replace Superstructure |
| 43 | 37 | Renovate | | 80 | 74 | Repair Substructure |

```sql
-- a project is a "bridge" project if its primary OR any secondary code is in the set:
WHERE p.ConstructionCodeID IN BR
   OR p.Id IN (SELECT ProjectId FROM dbo.ProjectConstructionCode WHERE ConstructionCodeId IN BR)
```
*Excluded:* Tunnel-only (48 code), Bridge Inspection (49 code), Temporary Bridge (45 code),
Low-Water Crossing (41 code) are **not** in the set — they aren't capital bridge structures.
(Total bridge projects in the warehouse under this definition: 2,382.)

---

## 2. Project cost (shared with paving)

Best-available coalesce, recording which source was used. One CN phase per project
(`ROW_NUMBER() … ORDER BY ParticipatingAmount DESC, PhaseStartDate DESC`) to avoid
double-counting against per-project OASIS/FMIS sums.

```
Project Cost = first non-zero of:
  1. ProjectPhase.ParticipatingAmount (CN phase)            -> "Participating"
  2. SUM(BUD_STRU.ACTU_EXP_AM)  where PHASE_CD like 'CN%'    -> "OASIS actual exp"
  3. SUM(AuthorizationData.EXP_AMT) where PHASE_TYPE='CN'    -> "FMIS expended"
  4. SUM(BUD_STRU.CURR_BUD_AM)  CN                           -> "OASIS budget"
  5. SUM(AuthorizationData.AUTH_AMT) CN                      -> "FMIS authorized"
```

Universal join key: `Project.ProjectId` == `BUD_STRU.PROG_CD` == `AuthorizationData.PROJ_KEY`.
Internal `Project.Id` joins to `ProjectPhase.ProjectId` and `RouteSegment.ProjectId`.

---

## 3. Deck-area cost distribution (THE SECOND DIFFERENCE — THE IMPORTANT PART)

Distribute each project's cost across its **individual bridge structures**, weighted by
**deck area (square feet)** instead of route length.

1. **Source**: `dbo.RouteSegment` rows where `RouteSegment.ProjectId = Project.Id`.
2. **A bridge-bearing segment** has `BridgeLength > 0` AND `BridgeWidth > 0`.
3. **Deck area (sqft) = `BridgeLength` (ft) × `BridgeWidth` (ft)** per segment.
   `BridgeLength` = structure length, `BridgeWidth` = out-to-out deck width.
4. **Structure key = `RouteSegment.NBINumber`** (the NBI structure number, e.g.
   `00000000017A237`). **100% populated** on deck-bearing segments. Stored/exported as
   **text** to preserve leading zeros. Fall back to `RouteIdStr@StartMP` if ever blank.
5. **Per structure**: deck area = Σ(segment deck areas) for that NBI number. Directional
   (NB/SB) carriageways under one structure are **summed** → directional deck area, both
   decks counted (consistent with paving's directional summing).
6. **Project total deck area** = Σ(all structure deck areas).
7. **% of project** = structure deck area / project total deck area.
8. **Allocated cost** = Project Cost × (% of project).
9. **Fallbacks** (so no in-scope cost silently vanishes):
   - *Segments but no deck dims* → even split across distinct NBI structures (or routes).
     Marked `Has Deck Data = seg-no-deck`. (12 committed / 90 done projects.)
   - *No route segments at all* → cannot be distributed; carried in **Project Summary**
     only, not in the structure rows. Marked `N`. (15 committed / 83 done projects.)

Validation: allocated cost sums **exactly** to project cost for every distributed
project (0 mismatches, $0.00 worst diff).

---

## 4. Federal-Aid System classification (shared)

Classify by `RouteSegment.FASId`:
```
1 = Interstate   2 = NHS   3 = STP   4 = Intermodal Connectors   5 = Non-Federal-Aid
```
- **Structure class** = dominant `FASId` within that structure, weighted by deck area.
- **Project class** = dominant `FASId` across the project, weighted by deck area.

---

# PART A — COMMITTED bridges

### Filter (committed OR programmed) — identical ladder to paving
```sql
   EXISTS (AuthorizationData CN AUTH_AMT > 0)                       -- obligated (FMIS)
OR EXISTS (BUD_STRU CN  ACTU_EXP_AM > 0 OR ENC_AM > 0)              -- executing / awarded
OR (CN phase) FMISStatus.Name = 'Approved'                          -- FHWA approved
OR EXISTS (PhaseSTIP.CurrentObligationDate IS NOT NULL via PCR)     -- on STIP
OR (CN phase) ParticipatingAmount > 0                               -- funded / budgeted
```
### Year = construction-start year
`YEAR(ProjectPhase.PhaseStartDate)` for the CN phase (`PhaseTypeId = 3`) **= 2026**.

### LEVEL column (commitment tier, highest reached)
`PROGRAMMED` < `OBLIGATED` (FMIS AUTH>0 or FHWA Approved) < `CONTRACT AWARDED`
(OASIS CN `ENC_AM>0`) < `UNDER CONSTRUCTION` (OASIS CN `ACTU_EXP_AM>0`).

---

# PART B — PAST / DONE bridges

### "Done" = CN phase Closed (same as paving)
```sql
ProjectPhase.PhaseTypeId = 3 AND PhaseStatus.Code = 'C'    -- not W=Withdrawn, T=Terminated
```
### Start & end years
```
Year Started = YEAR( COALESCE( START CONSTRUCTION actual (MilestoneId=31, ActualDate<=today),
                               ProjectPhase.PhaseStartDate ) )
Year Ended   = YEAR( COALESCE( COMPLETE CONST. actual (MilestoneId=32, ActualDate<=today),
                               CONSTRUCTION PHASE END actual (MilestoneId=3, ActualDate<=today),
                               ProjectPhase.PhaseEndDate ) )
```
(`PhaseMilestone.ActualDate` is a `date`; always filter `<= today`.)

---

## 5. Workbook layout

**Committed** (`Bridge_COMMITTED_2026_DeckArea_Cost_Breakdown.xlsx`):
- `Structure Cost Breakdown` — one row per structure: Project No, Name, State Project No,
  **LEVEL**, Fed-Aid Class, Work Type, Project Cost, Cost Source, **NBI Structure No**,
  Route Id Str, Route, Sign System, County, Bridge Type, # Segs, **Deck Length (ft)**,
  **Deck Width (ft)**, **Deck Area (sqft)**, **% of Project**, **Allocated Cost**,
  Fed-Aid Class (structure).
- `Project Summary` — Project No, Name, LEVEL, Fed-Aid Class, Work Type, Cost, Cost Source,
  # Structures, Total Deck Area (sqft), **Cost per Sqft**, Has Deck Data.
- `Funding by FAS Class` — Structures, Allocated Cost, Deck Area, $/Sqft per class + TOTAL.
- `Notes`.

**Done** (`Bridge_DONE_DeckArea_Cost_Distribution.xlsx`): same shape, with **Year Started /
Year Ended** replacing LEVEL.

---

## 6. Results

| | Committed 2026 | Done |
|---|---|---|
| Projects in scope | 156 | 794 |
| — distributed (have deck data) | 129 | 621 |
| — even-split (segs, no deck dims) | 12 | 90 |
| — no segments (not distributed) | 15 | 83 |
| Structure rows | 169 | 1,036 |
| Total project cost | $845.4M | $773.3M |
| **Distributed allocated cost** | **$421.5M** | **$694.4M** |
| Total deck area | 1.43M sqft | 10.0M sqft |
| Blended $/sqft | $296 | $69 |
| On NHS/Interstate (projects) | 30 | 127 |

The gap between total project cost and distributed cost is the no-segment projects
(carried in Project Summary only) — notably ~$424M of large committed jobs that lack
route-segment records.

**Funding by FAS class — Done:** Interstate $89.1M / NHS $145.9M / STP $345.9M /
Intermodal Conn $0.4M / Non-Fed-Aid $108.8M / Unknown $4.3M.
**Committed:** Interstate $164.6M / NHS $41.9M / STP $168.5M / Non-Fed-Aid $44.8M /
Unknown $1.8M.

---

## 7. Data-quality caveats

1. **Deck dims live on `RouteSegment`** (`BridgeLength` × `BridgeWidth`), the same table
   paving used for length — kept the method consistent. The TAMSDW linked server
   (`10.6.60.45`) holds the authoritative full NBI/BrM inventory if a deck-area source
   independent of project route segments is ever wanted.
2. **`NBINumber` is the structure key** (100% on deck segments). `RoutePrimaryNbiBridgeID`
   is sparse (~37%) — don't key on it.
3. **Deck dimension coverage is ~80%** of in-scope projects (129/156 committed,
   621/794 done). The rest fall to even-split or are reported as no-segment.
4. **No-segment projects can't be distributed** — report separately; they carry the gap
   between total and distributed cost.
5. **Committed is all federal-aid classes, not NHS-only** (unlike the NHS-scoped paving
   committed file). Filter the Fed-Aid Class column for the NHS/Interstate subset.
6. **Future fiscal years can't be "committed"** — federal obligation doesn't happen 1-2
   years ahead; 2027/2028 would return only programmed work.
7. **`PhaseStatus` W/T are cancelled**, never count as done.
8. **One CN phase per project** (ROW_NUMBER dedup) against per-project OASIS/FMIS sums.
