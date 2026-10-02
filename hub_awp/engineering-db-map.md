# The Engineering database — how vendors, agreements and invoices connect

*Surveyed 2026‑09‑05 against the live WVDOT SQL Server (`[Engineering]` and `[Data-Warehouse]` on
the Data‑Warehouse host, via the 1434 tunnel). Row counts are as of that day. Every relationship
below was confirmed by a declared foreign key or by a value‑overlap join; where a join is inferred
the match rate is given.*

`[Engineering]` holds **205 tables, 92 views and 201 declared foreign keys**. About forty tables make
up the consultant‑agreement tracker the portal imports from; the rest are project‑development
trackers (DDR/DDI/District milestones, permits, right‑of‑way status, STIP, TheHub requests, CWS
pavement bars) that share the same project key. `[Data-Warehouse]` (149 tables) is TheHub's project
master and the only place OASIS master data lands. All 92 view definitions are hidden from our
login, so the `*_ALL` unions were reconstructed from the tables they cover.

## 1. The core chain

```
Consultants (263) ──┐
                    ├── Agreements (1 344) ── Supplements (551)
                    │        │  │                 └── Supplements_Subcon (50)
                    │        │  └── Agreements_Subcon (718)
                    │        └── Invoices (9 416) ── Invoices_Subcon (1 336)
                    │                 │
PTSData (15 184 projects) ────────────┘   ← every agreement, supplement and invoice carries the 10‑digit project key
```

| Table | Rows | Key | Links (✔ = declared FK) |
|---|---|---|---|
| `Consultants` | 263 | `sqlid` | The vendor master for the Engineering Division. `CONSULTANT` (name), `CONSULTANT_NUMBER` (unique 2–4 digit Engineering‑internal number: Baker 275, HDR 210, Stantec 350), `isDBE`, office‑manager contact (17 filled). **No OASIS vendor number, address id or tax id.** |
| `Agreements` | 1 344 (1 150 distinct agreement numbers) | `SQL_id` | `Consultant_id` → Consultants ✔ · `ProjectID` → PTSData.PROJ_KEY (1 330/1 344, no FK) · 74 columns, see §3 |
| `Supplements` | 551 | `SQL_id` | `MasterAgreementIndex` → Agreements ✔ (551/551) · `Consultant_id` ✔ · `ProjectID` → PTSData ✔ · `Supp_Num`, `Amnt` (ceiling change), `Type` (SA/SA1), `supplemental_scope` Planned/Unplanned/NA, same procurement‑milestone columns as Agreements |
| `Invoices` | 9 416 | `SQL_id` | `MasterAgreementIndex` → Agreements ✔ (9 416/9 416) · `consultantID` → Consultants ✔ (equals the agreement's prime on 9 412) · `ProjectID` → PTSData ✔ (equals the agreement's project on all) · `Project_Manager` → Project_Managers (5 404/5 415) · `Log_Number_Assigned_by` → STAFF (5 057/5 057) · `Returned_From_Review_by` → STAFF (4 150/4 154) · 56 columns, see §4 |
| `Invoices_Subcon` | 1 336 | `sqlid` | `invoice_id` → Invoices ✔ · `subconsultant_id` → Consultants ✔ · `amount` = the sub's share of that invoice (the portal imports these as subconsultant line items) |
| `Agreements_Subcon` | 718 (319 agreements) | `sqlid` | `Agreement_id` → Agreements ✔ · `subconsultant_id` → Consultants ✔ · `amount` = sub's share of the agreement ceiling |
| `Supplements_Subcon` | 50 | `sqlid` | `Supplement_id` → Supplements ✔ · `subconsultant_id` ✔ |
| `Consultant_Target_Dates` | 1 123 | `sql_ID` | `agreement_id` → Agreements (1 109/1 123) · `consultant_id`, `ProjectKey` · estimated (`_E`) vs actual (`_A`) procurement milestones (LOI, shortlist, interviews, scope meeting, IEE, proposal, negotiation, agreement distributed, to auditing) |
| `Consultant_Evaluations` | 1 317 | `sql_ID` | `consultant_id` ✔ · `ProjectKey` ✔ · field/office/design ratings and comments |
| `Statewide_Agreement_Tracking` | 453 | `sql_ID` | `ProjectKey` → PTSData ✔ (→ Agreements.ProjectID on 417) · legacy tracker of master agreements and their letter agreements (`Master_Agreement` = service type, `Letter_Agreement` LA1…, `Order_LA`, `Responsibility` DDC/DDE/DT/D9, `Total_Fee`, `Actual_or_Estimated`) |
| `Prequal_Agreement_Tracking` | 170 | `sql_ID` | `ProjectKey` ✔ · pre‑qualified agreements (`Prequal_Agreement` PQ1/PQ2/"SA1 to PQ1", `Type_Prequal_Services`, `Effective_Date_Prequal_List`) |
| `Phase_Closure` / `Phase_Closure_Sub` | 156 / 103 | `IDsql` | closing the EN phase of a project: `Phase_Closure_Sub.Consultant_ID`, **`APO_Number`** (PAG), dates closure / final invoice / final evaluation / final audit (>$250k) requested, `APO_Closure_Date`; 74 of its 90 PAG numbers appear on invoices |

**Project master and funding.** `PTSData.PROJ_KEY` is the 10‑digit WVDOH project key (`YYYYNNNNNN`,
e.g. `2011000857`) with `PROJ_DESC`, `ST_PROJ_NO`, `CONSULTANT` (name text), `RESP_DIST`,
`PROJECT_MANAGER`, and per‑phase REMIS money (`ENG_AUTH_AMT`, `ENG_EXP_AMT`, `ENG_END`, same for
RW/CN/OT). `AuthorizationData` (17 711) lists each project's phase authorizations
(`PHASE_TYPE` EN/CN/RW, `AUTH_CODE`, `AUTH_AMT`, `EXP_AMT`, `END_DATE`). `AuthData_REMIS` (975) is a
REMIS authorization ledger (`AUTHORIZATION` e.g. `FE2463G`, `REC_ORG`, state/federal project,
`WORK_END_DATE`, `FINANCIAL_END_DATE`, `TOTAL_AUTHORIZED`, `EXPENDED`, `BALANCE`).
`RemisAuthIdsfromhub` (15 218) maps project → REMIS authorization id per CN/EN/RW phase.
`ENG_EXP_AMT` is **not** the sum of consultant invoices (Corridor H: $8.0M expended vs $7.97M
invoiced; Environmental Work: $45.5M vs $36.4M) — it includes non‑consultant charges.

**Lookups.** `Project_Managers` (77), `STAFF` (93, `Anumber` = state employee id, `DISTRICT`,
`Task_Categories`), `DDC_PM` (10), `DDC_Consultants` (74, `new_ID` → Consultants 73/74),
`PQ_Engineering_Consultants` (54 consultant numbers on the pre‑qualified list),
`Task_Categories`/`Task_Subcategories` (the division taxonomy in §6).

## 2. What every identifier means

| Identifier | Format | Where | Meaning |
|---|---|---|---|
| Project key | `YYYYNNNNNN` (10 digits) | `PTSData.PROJ_KEY`, `*.ProjectID`, `*.ProjectKey`, Data‑Warehouse `Project.ProjectId` | The WVDOH project. **This is what vendors print as "Contract ID" on CEI split sheets** (`2018001357`) and as "CID" on transmittal letters (`2020000635`): both fit the format and both are project keys, not agreement numbers. The portal's `projects.number` already holds it. |
| Consultant number | 2–4 digits, unique | `Consultants.CONSULTANT_NUMBER` | Engineering's own vendor number. The portal imports it as the placeholder OASIS vendor number `ENG<n>`. |
| Agreement number | `<ProjectKey>-<ConsultantNumber>-A` | `Agreements.AgreementNumberGenerated` | 1 102 of 1 344 follow it exactly (`2011000857-275-A` = Baker on project 2011000857). Variants: `-001-A` (2020 on‑call batch), `-750-A` (EnviroScience), `-1-A`. The portal's `contract_id`. |
| Supplement number | `<ProjectKey>-<ConsultantNumber>-<Agreement SQL_id>-s` | `Supplements.AgreementNumberGenerated` | 416/551 exact |
| Invoice agreement ref | `<agreement number>-<Agreement SQL_id>` | `Invoices.AgreementNumberGenerated` | 9 415/9 416; `masteragreementnumber` is the plain agreement number |
| REMIS / FIMS authorization | 2 letters + 4 digits + letter (`FE2441G`, `XE2107W`, `UE2336G`) | `Invoices.Authorization` (6 297), `Agreements.AuthorizationNum` (510), `Supplements.AuthorizationNum` (377), `AuthData_REMIS.AUTHORIZATION`, `RemisAuthIdsfromhub.RemisAuthId*`, `HUB_Projects.Auth` | The state financial‑system authorization the invoice charges. Second letter is the phase (E engineering, C construction, R right‑of‑way, D/O other); 6 242 of 6 297 invoice values equal the agreement's. Of 442 distinct invoice authorizations, 218 appear in `AuthData_REMIS`, 186 in `RemisAuthIdsfromhub`, 121 in `HUB_Projects`. **Not imported today.** |
| Keyed agreement number | `<Authorization><ConsultantNumber>[suffix]` (`UE2336G335`, `TD2114M165CRS`) | `Agreements.AgreementNumberKeyed` (329), `Supplements.AgreementNumberKeyed` (323) | The agreement id as keyed into FIMS/REMIS (309/329 compose exactly; CRS/NRS suffixes = cultural / natural resources sub‑agreements). **Not imported.** |
| Legacy PO number | `<Authorization><SVC>` (`FE2346GPAG`) | `Invoices.PO_Number` (2 796, essentially pre‑2022) | FIMS‑era purchase‑order id. The 3‑letter service code: PAG 1 964 (professional agreement), **QAM 303 (quality‑assurance management, i.e. CEI — Baker's cover says `WVDOH_CEI_QAM`)**, PDS 103, NEP 70 (NEPA), GAI 53, CRS 45, WVU 37, NRS 31, TSL 18, RDW 17, RDA 16, CSX 12, SUR 8, and a tail of one‑offs. Imported only as the fallback for `wv_apo`. |
| OASIS agreement document | `PAG<FY>*<seq>` (`PAG23*266`) | `Invoices.OASIS_APO_Number` (4 625), `Agreements.OASIS_APO_Number` (334), `Phase_Closure_Sub.APO_Number` | The wvOASIS procurement document since FY23 (2 373 rows FY23, 875 FY24, 831 FY25, 445 FY26, 11 FY27). One PAG per agreement (4 539 of 4 565 invoice/agreement pairs agree; the exceptions are typos like `PAG23*17` vs `PAG23*017`). Free‑text values (`D4 TO PROCESS`, `NO PAG#`, `DO NOT PROCESS INV'S`) mark invoices the districts process. The importer parses it into `oasis_doc_type = "PAG"` / `oasis_doc_id` and the BF‑2 `wv_apo`. |
| Receiving org | 4 digits | `Invoices.REC_ORG` (5 998), `AuthData_REMIS.REC_ORG` | The unit that receives the invoice: `0060` Engineering Division HQ (3 687), `1060` District 10, `0160` D1, `0460` D4, `0858` D8, `0579` D5, `0679` D6, `0360` D3, `0760` D7, `0979` D9, `0085` statewide/central, `0061`… The importer maps it to `wv_unit` and derives each agreement's org unit from the modal code — these are the real BF‑2 UNIT codes, whereas the portal's seeded `bf2_unit_code` values (`0100`…`1000`, `065x`) were guesses. |
| Sequence | int | `Invoices.SeqNum` | Running number within the agreement (1…133); the importer writes it to `wv_sequence_no`. |
| Vendor invoice number | small ints mostly | `Invoices.Invoice_Number` | The consultant's own numbering (1, 2, 3…), 96 nulls. |

## 3. `Agreements` — the 74 columns

*Identity:* `SQL_id`, `AgreementNumberGenerated`, `AgreementNumberKeyed`, `ProjectID`,
`Consultant_id`, `Consultant_ID_Alternate_1/_2` (592/586 filled — alternates or subs),
`AuthorizationNum` (510), `OASIS_APO_Number` (334), `agreement_link` (ProjectWise URL, 731),
`Comment` (758).
*Money and hours:* `Amnt` (1 148 — the portal's `original_amount`), `Est_Amount_Appd` (818),
`Proposed_Amount` (703), `Proposed_Man_Hours` (768), `Man_Hours_Appd` (839), `NegotiatedManHrs` (759).
*Type:* `Fee_Type` (COST PLUS / LUMP SUM / Specific Rate), `Selection_Type` (PQ / EA / PDS),
`prequal_type` (Engineering Services, Traffic Engineering Services, NEPA…),
`Procurement_Responsible_Group` (DD‑C / Other / OS), `Agreement_Type_PID` (always "Initial"),
`Project_Scope_PID`, `Supplemental_Scope_PID`, `Negotiator`, `PQ_Num`, `Dev_Proj_Man_ID`.
*Flags* (`-1`/`0` text): `isClosed`, `isLet`, `Agreement_Executed`, `SOWReq`, `Est_Reqd_Yes/No`,
`Proposal_Requested`, `Initiate_Draft_Agreement`, `Final_Div_Audit`, `Final_Desk_Audit`.
*Procurement dates:* `Org_Agmt_Date` (850 — the portal's `agreement_date`), `distributed_date`,
`Agreement_Drafted`, `Sent_To_Legal`, `NTP` (28), `Negotiation_Complete`, `Selected`,
`LOI_Advertised`, `Short_Listed`, `Scoped`, `Initial_Estimate(_Approved)`, `Initial_Prop_Requested`,
`Initial/Final_Proposal_Recvd`, `Negotiate_Memo`, `Final_Audit_Reqd/Received`, `Fee_Memo_Drafted`;
approvals `Appr_By_Lawyer/Director/HD/HP/CH/CC` (≈270 each); planned schedule `*_E` (10 columns).
*Empty:* `Task_SubCatogery`, `Invoiced_Under_Separate_Project_ID`.

**There is no agreement name and no contract term.** The portal's agreement `name` comes from
TheHub's project name via `ProjectID`; term dates exist only as procurement milestones.

## 4. `Invoices` — the 56 columns and the payment trail

*Header:* `Invoice_Number`, `Invoice_Date` (9 272), `Invoice_Amount` (9 302), `Percent_on_BF2`
(8 799 — the BF‑2 "% funds expended"), `Work_Start`/`Work_End` (5 847/6 263), `Final_Invoice`,
`NO_SUB`, `Shop_Drawings`, `Waiting_for_Info`, `In_Auditing`, `Notes` (2 696), `Project_Manager`,
`Authorization`, `PO_Number`, `REC_ORG`, `OASIS_APO_Number`, `SeqNum`.

*Lifecycle dates (fill counts) — the order the importer uses to reconstruct status:*

| Step | Column | Filled | Portal status |
|---|---|---|---|
| received | `Invoice_Rec_Date` (1 432, since 2025), `Invoice_submit_Date` (17) | | `received` |
| logged / sent to reviewer | `Date_Sent_for_Review` | 7 805 | `routed` |
| information requested / received from consultant | `Info_Req_from_Cons` (130), `Info_Rec_from_Cons` (66) | | |
| back from reviewer | `Date_back_from_Review` | 6 697 | `in_review` → `approved` |
| to auditing | `Date_Scanned_to_Auditing` (3 104), `Date_Rcvd_From_Audit` (98) | | |
| **keyed into OASIS** | **`Invoice_Sub_to_OASIS`** | 1 380 (since 2025) | `keyed` |
| **paid** | **`Paid_Date`** (1 434, since 2025) / `Paid_Date_AppXtender` (6 335, older, from the ApplicationXtender imaging system) | | `paid` |
| scanned / voided | `Scanned_or_Void` (SCANNED 6 644, VOID 305, a few stray dates), `Scanned_or_Void_Date` (4 056), `Void_Date` (88), `Void_Amount` (151) | | `withdrawn` for VOID |

The gap between `Invoice_Sub_to_OASIS` and `Paid_Date` is unreliable (average 1 day, range −4 741 to
+1 098 days) — the two dates are keyed by hand.

*Cost breakdown columns exist but are unused:* `overhead_percent`, `direct_labor_costs`,
`direct_costs`, `net_fixed_fees`, `fccm`, `rounding` are filled on ≈1 679 rows and are almost all
`0.00`; `boring_costs`, `prime_cph_cst`, `drilling_costs`, `special_handling`, `oldid`,
`Project_ID_For_Invoicing`, `Supplemental_Task_ID`, `Submit_Date` are empty. **`warrant_no` is `0`
on every row** — no warrant/check numbers were ever recorded. `RecapData` (the intended
cost‑recap table, `Inv_ID` → Invoices) is empty.

## 5. OASIS trails — everything that exists

**In `[Engineering]`:**

- `Invoices.OASIS_APO_Number` and `Agreements.OASIS_APO_Number` — the PAG document (§2).
- `Invoices.Invoice_Sub_to_OASIS`, `Paid_Date`, `Paid_Date_AppXtender` — when an invoice was keyed
  and paid (§4).
- `Invoices.PO_Number` — the FIMS‑era purchase order (`<authorization><service code>`).
- `Invoices.Authorization` / `Agreements.AuthorizationNum` / `Supplements.AuthorizationNum` — the
  REMIS authorization the charges post to; joins to `AuthData_REMIS`, `RemisAuthIdsfromhub`,
  `HUB_Projects.Auth`.
- `Invoices.REC_ORG` — the receiving unit code that the BF‑2 UNIT box carries.
- `Phase_Closure_Sub.APO_Number` / `APO_Closure_Date` — closing the PAG when the EN phase ends.
- `Agreements.AgreementNumberKeyed` — the id keyed into FIMS/REMIS.

**In `[Data-Warehouse]`:**

- `OasisCustomers` (457) — OASIS *customer* codes for DOH local billing (`000000109230`,
  `VC0000131699`) with `AddressId` (`AD000001`, `CV10001`), `BPRO_NM`, `AD_TYPE`. Same code
  and address‑id formats the BF‑2 prints as VENDOR NUMBER / REMIT ADDRESS ID, but the list holds
  MPOs, associations and agencies — **not the consultants**.
- `AWP_ChangeOrders.VendorID` / `AddressID` — OASIS vendor ids of *construction contractors*
  (`000000166791`, `CV10002`) from AASHTOWare Project, keyed by construction `ContractID`.
- `EmployeeinfofromOASIS` (15 801) — staff directory (`EmployeeIDOASIS`, org, position).
- `Project.InterfacedToOasis` (all False/NULL), `ProjectPhase.IsSubmittedToOASIS` (14 820 True /
  3 828 False) and `OasisEffectiveToDate`, `PhaseFunding.IsSubmittedToOASIS`,
  `PhaseChangeRequest.OasisStagingId` / `OasisEffectiveToDate` — TheHub → OASIS project/phase
  interface flags.
- `PhaseSTIP.SentToPRCDate` / `PRCApprovalDate` and `STIP.PRC_APPROVE` — "PRC" here is the
  Program Review Committee, not the OASIS PRC payment document.
- `dtims_transactions_detail.OasisActivity` — maintenance activity codes.

**What does not exist anywhere:** a consultant → OASIS vendor number mapping, OASIS payment
document ids (PRC/GAX) or warrant numbers, per‑invoice accounting lines (fund/activity/task
order), labor rates, and contract terms. Those have to come from OASIS itself or from the BF‑2
packages.

## 6. Nine copies of the tracker — the division suffixes

Every core table exists once per division, unioned by hidden `*_ALL` views. The suffix map comes
from `Task_Categories`:

| Suffix | Division | Agreements | Invoices | Supplements | Subcon rows |
|---|---|---|---|---|---|
| *(none)* | Engineering Division (EN) | 1 344 | 9 416 | 551 | 718 |
| `CA` | **Contract Administration** (construction CEI, inspection, CPM schedules, finalization) | 130 | 68 | 78 | 0 (11 `Invoices_SubSupCA`) |
| `M` | Materials (asphalt / pavement / cathodic / environmental lab testing, CEI materials facility) | 58 | 211 | 0 | 0 |
| `TO` | Traffic Operations (bridge inspection, buildings & grounds) | 12 | 74 | 0 | 9 |
| `IT` | Information Technology | 4 | 16 | 1 | 0 |
| `PM` | Performance Management | 1 | 5 | 0 | 0 |
| `OD` | Operations Division | 1 | 0 | 0 | 0 |
| `P` | Planning | 0 | 0 | 0 | 0 |
| `RW` | Right of Way (appraisal, attorney, railroad, utility) | 0 | 0 | 0 | 0 |
| `TS` | Technical Support (NEPA, noise, cultural/natural resources, surveying, aerial) | 0 | 0 | 0 | 0 |

Each division has its own `Consultants<suffix>` copy (237 rows each). They are **not** in sync
with the EN list: only 215 of 237 match by id and name, and ids run to 334 in EN vs 272 in the
copies — match across divisions by `CONSULTANT_NUMBER` or name, never by `sqlid`. The CA and M
copies have the same columns as EN but `OASIS_APO_Number`, `AgreementNumberKeyed` and
`AuthorizationNum` are empty in every sample row.

**The portal imports the EN tables only.** Contract Administration (130 agreements, 68 invoices)
is the construction‑inspection work the portal exists for, and Materials (211 invoices) is the
division flagged at kickoff as the complicated one; both are loadable with the same mapping plus a
division tag on the agreement.

## 7. How this maps onto the portal

| Portal field | Engineering source | Status |
|---|---|---|
| `vendors.name`, `oasis_vendor_number` | `Consultants.CONSULTANT`, `ENG<CONSULTANT_NUMBER>` placeholder | imported (placeholder flagged) |
| `agreements.contract_id` | `AgreementNumberGenerated` (194 duplicate rows merged to 1 150) | imported |
| `agreements.name` | TheHub `Project.ProjectName` via `ProjectID` | imported |
| `agreements.original_amount`, `agreement_date`, `status` | `Amnt`, `Org_Agmt_Date`, `isClosed` | imported |
| `agreements.oasis_doc_type/id` | `OASIS_APO_Number` → `PAG` / `PAG23*266` | imported (parsed) |
| `agreement_supplementals` | `Supplements` (`Supp_Num`, `Amnt`, dates) | imported |
| `projects.number`, `contract_id` | `PTSData.PROJ_KEY` / TheHub `ProjectId` | `number` imported; `contract_id` new and empty — the split‑sheet "Contract ID" is the same key, so matching by `number` already works |
| `invoices.*` header, `wv_apo`, `wv_unit`, `wv_sequence_no`, `pct_funds_expended_bf2` | `Invoices` (`OASIS_APO_Number`/`PO_Number`, `REC_ORG`, `SeqNum`, `Percent_on_BF2`) | imported |
| invoice status + events | lifecycle dates (§4) | imported (inferred `paid` recorded on the row) |
| subconsultant line items | `Invoices_Subcon` | imported |
| REMIS authorization (`Authorization`, `AuthorizationNum`) | — | **not imported**; the natural key for the BF‑2 keying block and for OASIS reconciliation |
| `AgreementNumberKeyed`, `Fee_Type`, `prequal_type`, `Selection_Type`, alternates, ProjectWise link | — | not imported (Fee_Type is read but not stored) |
| `Agreements_Subcon` (sub share of the ceiling) | — | not imported |
| `Consultant_Target_Dates`, `Consultant_Evaluations` | — | not imported |
| `Phase_Closure_Sub` (PAG closure) | — | not imported |
| org units' `bf2_unit_code` | `REC_ORG` codes (§2) | derived per agreement, but the seeded district codes differ from the real ones |
| CA / M / TO divisions | suffix tables (§6) | not imported |

## 8. Data‑quality notes for whoever imports next

- 194 of 1 344 `Agreements` rows repeat an agreement number (same project + consultant entered
  twice); the importer merges them. Five `Invoices` rows are exact duplicates.
- `Scanned_or_Void` is free text: 55 blanks and a handful of typed dates alongside SCANNED/VOID.
- `OASIS_APO_Number` needs normalisation (`PAG23*17` vs `PAG23*017`, `PAG 25*171`, trailing
  `115P`); 40 invoice rows and 12 agreement rows carry district‑processing notes instead of a
  number.
- `Consultants.CONSULTANT` still contains HTML entities (`&amp;`).
- `Percent_on_BF2` is a percent (0–100), `Man_Hours_Appd` is text on agreements and float on
  supplements, the `-1`/`0` flags are `nchar(10)` with trailing spaces.
- Backup and test tables (`Agreementsbackup6-4-24`, `AuthData_REMIS_backup`, `PTSData12-1-21`,
  `PTSDatabk5-2-25`, `PTSDataDEV`, `PTSDatatest*`, `PW_PROJ_Req_Created*`,
  `PROJSTATUS_RWStatusLogbackup`, `Consultant_Target_DatesTest`) should never be read.

## 9. Everything else in the database (not consultant‑related)

Project‑development trackers keyed by the same project key: `DDR_Projects` / `DDR_SubProjects` /
`DDR_RelatedProjects` / `DDR_PM` / `DDR_tConsultants` (design‑review milestones),
`DDD_DDE_Design_Studies(_PMD)`, `District_Projects` (84 columns of district design milestones),
`Planning_*` (planning projects, agreements, consultants, PMs, statuses), `IEPTS_*` (structures),
`APD_*` (alternative project delivery), `PROJSTATUS_*` (right‑of‑way status, parcels, comments,
"invoices" = deed/option paperwork, not money), `Permit_Tracking_*`, `Phase_Closure*`,
`PHASE_DATES`, `PW_PROJ_Req_Created` (ProjectWise folder requests), `HUB_Projects` /
`HUB_Requests` / `Hub_*` (TheHub workflow), `HUB_VS_STIP(_NEW)` and the `STIP*` views,
`DataWarehouse_*` (snapshots of TheHub tables), `CWS_PB_*` and `Dtimsinon_reordered` (pavement
bars), `BMS_TreatmentCosts`, `BRIDGE_WORKFLOW`, `EO_Tracking` (engineering orders / change orders
with `EO_CO_Number`, `EO_CO_Amount`), `County_Ref`, `KPI_Access`, `Notifications`, `VersionStatus`.
