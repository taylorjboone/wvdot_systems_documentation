# AMS data model — combined business flow reference

_Compiled 2026-09-30. One scroll surface across the whole AMS data model. Three foundational chapters first (the central entities, the vendor graph, the reference catalogs), then five lifecycle chapters in the order a contract moves through them: procurement, execution, QA/QC acceptance, the time layer, and finally the compliance layer. Every claim in every chapter was verified against live queries to the `ams-lab/awdemo` instance; where awdemo returns no data, the schema is still documented from `refs/awdemo_metadata.xml` and labelled as such._

## Contents

1. **[Core entity references](#part-1-core-entity-references)** — The three central entities the UI is built around — Contract, ContractProject, and DailyWorkReport. Every scalar field, every navigation property, efficient `$select` / `$expand` recipes keyed to the FastAPI routes that already implement them, and a display blurb per entity. The lifecycle chapters below reference these entities constantly.
2. **[Vendor universe](#part-2-vendor-universe)** — RefVendor master records + the per-contract Contractor instance + Subcontract ledger + Surety ecosystem + vendor sub-tables (addresses, insurances, officers, work-classes, DBE/SBP certifications) + ContractorEvaluation. 9,131 vendors across 147 contracts; some entities named in the vendor reference guide turn out not to exist and are debunked here.
3. **[Reference catalogs & master data](#part-3-reference-catalogs-master-data)** — The lookup backbone — every Ref* table grouped into 11 families (items/materials, geographic, labor, weather, equipment, vendor, workflow, financial, QA/QC, administrative, change-order/claim). A 3-strategy loading framework (preload / lazy-paginated / autocomplete) with measured latencies, plus UI patterns for dropdowns, typeaheads, and tree pickers.
4. **[Procurement, letting & bidding](#part-4-procurement-letting-bidding)** — The pre-award world — lettings, proposals, bids, apparent-low analysis, prequalification, bonds, and the bid-history price-intelligence engine.
5. **[Labor, financials, items & materials](#part-5-labor-financials-items-materials)** — The three core execution flows: who worked and for how long, every dollar in and out, and the planned-vs-actual-vs-tested chain of work items and materials.
6. **[Testing, QA/QC & material acceptance](#part-6-testing-qaqc-material-acceptance)** — The science side of construction — AcceptanceAction rule book, SampleRecord lifecycle, MaterialTest and SampleRecordTest, lab qualifications, approved sources, and the DwrAcceptanceRecord that ties it all back to posted work. Includes the XML-blob test-result pattern (results live inside `SampleTestResultTemplateLog.DataXML`).
7. **[Schedule, time charges & workflow](#part-7-schedule-time-charges-workflow)** — The time layer: contract calendar and days-charged, progress schedules, milestones, suspensions, weather-impact tracking, and the contract-lifecycle workflow state machine.
8. **[Compliance, DBE & civil rights](#part-8-compliance-dbe-civil-rights)** — The regulatory layer: DBE commitment vs utilization, certified payroll with Davis-Bacon exceptions, prevailing wage, civil-rights/labor/EEO reviews, OJT programs, and the non-compliance tracking that holds it all together.

---

<a id="part-1-core-entity-references"></a>

# Part 1 — Core entity references

_The three central entities the UI is built around — Contract, ContractProject, and DailyWorkReport. Every scalar field, every navigation property, efficient `$select` / `$expand` recipes keyed to the FastAPI routes that already implement them, and a display blurb per entity. The lifecycle chapters below reference these entities constantly._

**Date:** 2026-09-30 · **Instance:** `ams-lab/awdemo` · **Walking example:** Contract **282 "WHITEOAK BRIDGE"** (bridge removal and replacement, Alcona County, prime vendor Carl Engineers Inc.)

`Contract` is the trunk of the AMS data model: every project, line item, DWR, payment, change order, claim, DBE commitment, time charge, workflow phase, insurance, and permit traces back here. The entity itself is a header record — **101 scalar properties and 65 navigation properties** — carrying identity, lifecycle, rollup totals, agency "soft columns", and nav links to the surrounding graph. This document inventories every property, explains the derived rollups (and verifies them against live math on contract 282), lists the subtype codes with their real-portfolio distributions, and gives efficient `$select`/`$expand` recipes for each UI load shape, mapped to the FastAPI routes that already implement them. Deep internals of the downstream entities (ChangeOrder, PaymentEstimate, DWR, ContractTime, DBE records, WageDecision, etc.) are owned by the sibling chapters in `docs/ams-business-flows-combined-2026-09-30.md`; this doc describes **Contract itself and how to load it**.

### Scalar property inventory

Count: **101 scalars** (verified: `len(parse_metadata(open('refs/awdemo_metadata.xml').read()).entities['Contract'].properties)`). The groupings below are curated — EDMX doesn't label fields by business function. "Awdemo on 282" columns show the live value for contract 282; `—` means null/blank on that row (not that the field is unpopulated universally — check a few other contracts if a field matters to you).

#### Identity & descriptive

| Property | Type | Meaning | Awdemo on 282 |
|---|---|---|---|
| `Id` | `Edm.Int64` (key) | Surrogate PK | `282` |
| `Name` | `Edm.String` | Short name shown in headers | `WHITEOAK BRIDGE` |
| `ContractProposalName` | `Edm.String` | Original proposal name (often same as Name) | `WHITEOAK BRIDGE` |
| `Description` | `Edm.String` | One-line description | `Bridge removal and replacement and approach work` |
| `LongDescription` | `Edm.String` | Multi-sentence scope | populated |
| `Location` | `Edm.String` | Free-text location | `Mikado Glennie Road at Van Etten Creek` |
| `HighwayRoute` | `Edm.String` | Route designation | `101` |
| `FedProjectNum` | `Edm.String` | Federal project number | `N/A` |
| `StateProjectNum` | `Edm.String` | State project number | `5551234` |
| `SpecBook` | `Edm.String` | Spec book code in force (year/revision) | `03` |
| `SupplementalSpecBook` | `Edm.String` | Supplement reference | — |
| `SUPPSPECBOOK` | `Edm.String` | Legacy alt soft-column for spec book | — |
| `CONTRACTALTERNATE_NM1` / `NM2` | `Edm.String` | Alternate name slots | — |

#### Lifecycle & status

| Property | Type | Meaning | Awdemo on 282 |
|---|---|---|---|
| `ContractStatus` | `Edm.String` | `Pending` → `Active` → `Closed` | `Active` |
| `ContractType` | `Edm.String` | Agency contract-type code (see **Subtypes**) | `ESD` |
| `ProposalType` | `Edm.String` | How the contract was procured | `LET` |
| `ContractWorkType` | `Edm.String` | Classification of work (BREC, RESU, …) | `BREC` |
| `RecordSource` | `Edm.String` | `Preconstruction` vs `Construction` — stage of lifecycle this record is tracking | `Preconstruction` |
| `WorkflowPhaseId` → `WorkflowPhase` | `Edm.Int64` + nav | The current phase in a workflow state machine; see "Schedule, time charges & workflow" chapter | `13` (= WorkflowPhase "Active Contract", PhaseOrder 200, under Workflow 3) |
| `MigrationSource` | `Edm.String` | Where this record was imported from (empty for native records) | — |
| `MigrationComplete` | `Edm.Boolean` | Whether migration is finalised | populated as false where set |
| `ItemAgencyViewAssocImported` | `Edm.Boolean` | Internal migration flag | — |
| `TransitiontoCRLMSConstructionDate` | `Edm.DateTimeOffset` | When the record transitioned Preconstruction → Construction | `2024-08-28` |
| `OrigMaterialGeneratedDate` | `Edm.DateTimeOffset` | When the materials ledger was first generated | `2024-08-29 09:32` |
| `OriginalMaterialGeneratedUserId` | `Edm.Int64` | PersonInfo id who ran the generation | `1609` |
| `CreatedDate`, `CreatedBy`, `LastUpdatedDate`, `LastUpdatedBy` | audit | Standard audit columns | `edeluca` created 2024-08-28, updated 2024-09-18 |

#### Financial rollups

All six amounts and three percents below are **server-computed** and refreshed when the underlying ChangeOrder / PaymentEstimate / ContractItem rows change. **Do not try to recompute these on the fly in UI** — read them straight. The "Derived rollups" section below explains the math.

| Property | Type | Meaning | Awdemo on 282 |
|---|---|---|---|
| `AwardedContractAmount` | `Edm.Decimal` | Sum of (unit price × bid quantity) at award — never changes | `1,204,969.10` |
| `CurrentContractAmount` | `Edm.Decimal` | `AwardedContractAmount` + approved change-order dollar impact | `1,207,358.16` |
| `NetChangeAmountApproved` | `Edm.Decimal` | Sum of `Amount` on approved COs | `389.06` |
| `NetChangeAmountPending` | `Edm.Decimal` | Same for not-yet-approved COs | `0` |
| `TotalNetChangeAmount` | `Edm.Decimal` | Approved + Pending | `389.06` |
| `NetChangePercentageApproved` | `Edm.Decimal` | `NetChangeAmountApproved / AwardedContractAmount × 100` | `0.03` |
| `NetChangePercentagePending` | `Edm.Decimal` | Pending equivalent | `0` |
| `TotalNetChangePercentage` | `Edm.Decimal` | Total equivalent | `0.03` |
| `AmountPaidToDate` | `Edm.Decimal` | Dollars actually paid to the prime (through *approved* PEs) | `1,147,109.70` |
| `AmountPostedToDate` | `Edm.Decimal` | Sum of per-PE installed amounts (approved + draft) | `1,207,358.16` |
| `AmountPostedApprovedToDateAllItems` | `Edm.Decimal` | Same but excluding draft PEs | `1,207,358.16` |
| `AmountPostedApprovedToDateCriticalItems` | `Edm.Decimal` | Posted-to-date for "critical" (incentive) items only | populated |
| `CurrentContractAmountCriticalItems` | `Edm.Decimal` | Current contract amount restricted to critical items | populated |
| `OverrunBalance` | `Edm.Decimal` | Balance of overrun authority remaining | — |
| `PercentPaid` | `Edm.Decimal` | `AmountPaidToDate / CurrentContractAmount × 100` | `95.01` |
| `PercentCompleteAward` | `Edm.Decimal` | `AmountPaidToDate / AwardedContractAmount × 100` | `95.20` |

#### Subcontract thresholds & calculated amounts

| Property | Type | Meaning | Awdemo on 282 |
|---|---|---|---|
| `SubcontractMaxAmount` | `Edm.Decimal` | Cap on total subcontracted dollars | populated per contract |
| `SubcontractPercentageThreshold` | `Edm.Decimal` | Cap as % of contract | — |
| `CalcTotalSubcontractAmount` | `Edm.Decimal` | Sum of approved Subcontract amounts | `62,756.56` |
| `CalcSpecialtySubcontractedAmount` | `Edm.Decimal` | Specialty portion thereof | populated |
| `CalcSpecialtySubcontractedPercent` | `Edm.Decimal` | Specialty share as % | populated |
| `CalcTotalExtendedAmount` | `Edm.Decimal` | Total of specialty + non-specialty sub $$ counting toward threshold | `57,756.56` |
| `CalcTowardsAmountThreshold` | `Edm.Decimal` | $ counting toward the max threshold | `57,756.56` |
| `CalcTowardsPercentThreshold` | `Edm.Decimal` | % equivalent | `4.78` |

#### Parties — foreign keys

Each of these is an `Edm.Int64` paired with a singular nav property (next section). Awdemo returns raw ids; expand to hydrate the party.

| Property | Target | Meaning | Awdemo on 282 |
|---|---|---|---|
| `PrimeRefVendorId` | `RefVendor` | Prime contractor (today) | `160` → "Carl Engineers Inc." |
| `OriginalRefVendorId` | `RefVendor` | Prime at award (same as prime unless assigned) | `160` |
| `SuretyCompanyId` | `RefVendor` | Surety company carrying the bond | `122` |
| `SuretyAgentId` | `RefVendor` | Surety agent | `142` |
| `RefCountyId` | `RefCounty` | Primary county | `1` → "Alcona County" |
| `RefDistrictId` | `RefDistrict` | Primary district / TSC office | `156` → "02002" / Alpena TSC |
| `AgencyDeliveryEngineerId` | `PersonInfo` | Agency delivery engineer | — |
| `AgencyProjectEngineerId` | `PersonInfo` | Agency project engineer | — |
| `ConsultantProjectEngineerId` | `PersonInfo` | Consultant project engineer | — |
| `LocalProjectEngineerId` | `PersonInfo` | Local-agency project engineer | — |
| `DesignerId` | `PersonInfo` | Designer | — |
| `ConstructionSupervisorId` | `PersonInfo` | Construction supervisor | — |
| `ConsultantOfficeId` | `RefVendor` | Consultant office vendor | — |
| `ConsultantOfficeLocationId` | `RefVendorAddress` | Specific office location | — |
| `OriginalMaterialGeneratedUserId` | `PersonInfo` | Who generated the original materials ledger | `1609` |

> **`PersonInfo` is 403 on `/PersonInfos` on awdemo** — these ids resolve but a direct GET is denied. Hydrate opportunistically (and let it fail quietly) or display raw `#1609` and let the user drill from there. See the Compliance chapter for the full gotcha.

#### Agency / division / office string labels

Free-text fields that duplicate structured ids above (legacy carryover). Treat as display-only.

| Property | Type | Meaning | Awdemo on 282 |
|---|---|---|---|
| `ModalAgency` | `Edm.String` | `FHWA`, `OTHER`, or null | `FHWA` |
| `DivisionResidency` | `Edm.String` | Residency / division label (free text) | `Bridge` |
| `LocalAgencyOffice` | `Edm.String` | Local agency office name | — |
| `ManagingOffice` | `Edm.String` | Managing office name | — |
| `ProjectEngineer` | `Edm.String` | Engineer name as free text (duplicates `AgencyProjectEngineerId`) | — |
| `ProjectManager` | `Edm.String` | Project manager name as free text | — |

#### Funding, compliance & oversight flags

| Property | Type | Meaning | Awdemo on 282 |
|---|---|---|---|
| `FederalOversight` | `Edm.Boolean` | Federally overseen? | populated |
| `LocalOversight` | `Edm.Boolean` | Locally overseen? | populated |
| `TypeofFunding` | `Edm.String` | Funding mix label | — |
| `FundingSources` | `Edm.String` | Free-text funding sources | — |
| `OverallFederalFundingPercent` | `Edm.Decimal` | Overall federal $ share | populated |
| `DBEGoalPercent` | `Edm.Decimal` | DBE participation goal (%) | populated |
| `WBEGoalPercent` | `Edm.Decimal` | WBE goal (%) | populated |
| `DBEGOAL` | `Edm.String` | Legacy soft-column, same intent as `DBEGoalPercent` | — |
| `DBECertificationStatus` | `Edm.String` | DBE certification status label | `Not Certified` |
| `DBECompliant` | `Edm.Boolean` | DBE utilization compliant? | populated per contract |
| `SETASIDE` | `Edm.String` | Legacy set-aside label | — |
| `BIDBOND` | `Edm.Decimal` | Bid-bond dollar amount at award | `25,000.00` |
| `DavisBaconWageRate` | `Edm.Boolean` | Davis-Bacon prevailing wage applies? | populated |
| `StatePrevailingWageRate` | `Edm.Boolean` | State prevailing-wage law applies? | populated |
| `StormwaterEarthMoving` | `Edm.Boolean` | Stormwater permit required? | populated |
| `StormwaterEventsEnabled` | `Edm.Boolean` | Weekly stormwater events feature on? | populated |
| `ETicketingEnabled` | `Edm.Boolean` | e-ticketing enabled for load tickets? | populated |
| `OjtGoal` / `OjtGoalUnits` / `OjtGoalComments` | — | OJT program goal (count + units label + notes) | — on 282 |
| `IncentiveCapAmount` | `Edm.Decimal` | Cap on positive adjustments | — |
| `DisincentiveCapAmount` | `Edm.Decimal` | Cap on penalties | — |
| `OverridePaymentApprovalLevel` | `Edm.Boolean` | Allow local override of PE approval workflow? | populated |
| `OverrideGlobalPaymentEstimateExceptions` | `Edm.Boolean` | Allow local override of exception rules | populated |

#### Progress schedule

| Property | Type | Meaning |
|---|---|---|
| `ProgressScheduleType` | `Edm.String` | Which progress-schedule method is in use (CPM, bar chart, etc.) |

See the Schedule chapter for `ContractProgressSchedule` details — this field just picks the method.

#### Comments

| Property | Meaning |
|---|---|
| `Comments` | Free-text internal comments |

#### Audit

Covered under Lifecycle above (`CreatedDate`, `CreatedBy`, `LastUpdatedDate`, `LastUpdatedBy`, `UnitSystem` — `English` on 282).

#### Portfolio distributions of the code-table scalars

Verified live against all 147 awdemo contracts:

| Field | Distribution |
|---|---|
| `ContractStatus` | 76 `Pending` · 69 `Active` · 2 `Closed` |
| `ContractType` | 62 null · 43 `ESD` · 14 `MAIN` · 12 `DESG` · 6 `RR` · 4 `REAL` · 3 `TRAF` · 2 `UPTR` · 1 `AERO` |
| `ProposalType` | 78 null · 51 `LET` · 17 `ENHA` · 1 `PE` |
| `ContractWorkType` | 76 null · 40 `RESU` · 16 `NCON` · 5 `RREC` · 2 `PMAI` · 2 `MISC` · 2 `BREC` · 1 `BCON` · 1 `002` · 1 `SFTY` · 1 `RAIL` |
| `RecordSource` | 76 `Preconstruction` · 71 `Construction` |
| `UnitSystem` | 124 `English` · 23 null |
| `ModalAgency` | 135 null · 11 `FHWA` · 1 `OTHER` |
| `DivisionResidency` | 144 null · 1 `Bridge` · 1 `Wayne Residency` · 1 `richmond chesterfld` |

Interpretation:
- Code tables are **sparsely populated** on awdemo — large portions of the portfolio have no `ContractType`, `ProposalType`, or `ContractWorkType`. Don't make UI filters that assume a code is present on every contract.
- `Status` and `UnitSystem` are reliably populated.
- `ModalAgency` is almost always null — treat it as an exception flag, not a facet.

### Navigation property inventory

Count: **65 nav properties** (verified: `len(e.navigation)`). Classified by cardinality below.

#### Reference navigations (singular, N:1 — many contracts share one target)

| Nav | Target entity | Fk column |
|---|---|---|
| `PrimeRefVendor` | `RefVendor` | `PrimeRefVendorId` |
| `OriginalRefVendor` | `RefVendor` | `OriginalRefVendorId` |
| `SuretyCompany` | `RefVendor` | `SuretyCompanyId` |
| `SuretyAgent` | `RefVendor` | `SuretyAgentId` |
| `RefCounty` | `RefCounty` | `RefCountyId` |
| `RefDistrict` | `RefDistrict` | `RefDistrictId` |
| `WorkflowPhase` | `WorkflowPhase` | `WorkflowPhaseId` |
| `AgencyDeliveryEngineer` | `PersonInfo` | `AgencyDeliveryEngineerId` |
| `AgencyProjectEngineer` | `PersonInfo` | `AgencyProjectEngineerId` |
| `ConsultantProjectEngineer` | `PersonInfo` | `ConsultantProjectEngineerId` |
| `LocalProjectEngineer` | `PersonInfo` | `LocalProjectEngineerId` |
| `Designer` | `PersonInfo` | `DesignerId` |
| `ConstructionSupervisor` | `PersonInfo` | `ConstructionSupervisorId` |
| `OriginalMaterialGeneratedUser` | `PersonInfo` | `OriginalMaterialGeneratedUserId` |
| `ConsultantOffice` | `RefVendor` | `ConsultantOfficeId` |
| `ConsultantOfficeLocation` | `RefVendorAddress` | `ConsultantOfficeLocationId` |

#### Singleton navigations (1:1 extension records)

| Nav | Target entity | Meaning |
|---|---|---|
| `ContractGeneric` | `ContractGeneric` | Agency-generic extension record (free-form key/values) |
| `ContractRetainage` | `ContractRetainage` | Current retainage configuration — one row per contract |

#### Collection navigations (1:N — many children per contract)

Grouped by business area, with cardinality on contract 282 (live counts).

**Projects & work**
- `ContractProjects` → `ContractProject` — the contract's project list. Contract 282: **1 project** (`#169 "1205339"`).
- `ContractItems` → `ContractItem` — all contract-item lines (pay items). Contract 282: **49 items**.
- `Contractors` → `Contractor` — vendors on this contract (prime + subs + specialty — this is the contract-local party record, distinct from `RefVendor`). Contract 282: **3 Contractors**.
- `Subcontracts` → `Subcontract` — formal subcontract agreements. Contract 282: **2 subs**.
- `ContractMixDesigns` → `ContractMixDesign` — approved concrete/asphalt mix designs for this contract.
- `ContractPriceAdjustmentIndexes` → `ContractPriceAdjustmentIndex` — price-adjustment index enrollments (fuel/asphalt escalators).
- `ContractAgencyViews` → `ContractAgencyView` — per-item agency view assignments.

**Field activity**
- `DailyWorkReports` → `DailyWorkReport` — DWRs. Contract 282: **13 DWRs**.
- `DailyDiaries` → `DailyDiary` — the agency diary record paired to DWRs. Contract 282: **13 diaries**.
- `DwrAcceptanceRecords` → `DwrAcceptanceRecord` — material acceptance records (owned by DWRs via posting chain; this is a convenience nav).
- `EarthMovingEvents` → `EarthMovingEvent` — earth-moving sub-events.
- `EOMTruckings` → `EOMTrucking` — end-of-month trucking summary rows.
- `ETicketCumulativeSummaries` → `ETicketCumulativeSummary` — e-ticket rollup rows.
- `StormwaterPeriods` → `StormwaterPeriod` — weekly stormwater inspection periods.

**Financial**
- `PaymentEstimates` → `PaymentEstimate` — periodic PE records. Contract 282: **11 PEs**.
- `ContractPayments` → `ContractPayment` — check / payment transactions.
- `ChangeOrders` → `ChangeOrder` — CO records. Contract 282: **3 COs** (0001 $69.93 OTH, 0002 $319.13 SUPPLA, 0003 CMPL null).
- `ContPaymtEstExceptOverrides` → `ContPaymtEstExceptOverride` — per-contract overrides of PE exception rules.
- `ContractPaymentEstimateTypes` → `ContractPaymentEstimateType` — which PE types are enabled.
- `ContractSecurityAccounts` → `ContractSecurityAccount` — escrow accounts holding securities in lieu of retainage.
- `PayEstimateItemAdjustments` → `PayEstimateItemAdjustment` — stockpile / overrun / price-index adjustments.
- `PaymentEstimateContractTimeCharges` → `PaymentEstimateContractTimeCharge` — per-PE time-charge rows (liq. damages, bonuses).
- `ContractFundPackages` → `ContractFundPackage` — funding packages. Contract 282: **2 packages**.
- `ForceAccounts` → `ForceAccount` — extra-work records. Contract 282: **1 FA**.

**Schedule & workflow**
- `ContractTimes` → `ContractTime` — contract time rows (begin, end, days charged, 5 subtypes). Contract 282: **10 ContractTime rows** (Awarded/NTP/Work-began/CRLMS/Price-adj base/Execution/Letting + "99 Avail", "99 Info", "99 Recur").
- `ContractProgressSchedules` → `ContractProgressSchedule` — baseline/current progress schedules.
- `ContractActions` → `ContractAction` — workflow action log.
- `ContractUserRoleAuthorities` → `ContractUserRoleAuthority` — per-user role grants for this contract.

**Compliance & reporting**
- `CertifiedPayrolls` → `CertifiedPayroll` — weekly certified payrolls per contractor.
- `ContractApprDbeCommitSummaries` → `ContractApprDbeCommitSummary` — baseline (approved) DBE commitment summary.
- `ContractCurrDbeCommitSummaries` → `ContractCurrDbeCommitSummary` — current (revised) DBE commitment summary.
- `ContractSBPGoals` → `ContractSBPGoal` — SBP goals. **⚠ returns 500 on awdemo.**
- `OjtContractAssignments` → `OjtContractAssignment` — OJT program assignments.
- `CufReviews` → `CufReview` — Commercially-Useful-Function reviews (DBE compliance).
- `ContractClaims` → `ContractClaim` — contractor claims. Contract 282: **1 claim** ($1M, in litigation).
- `ContractClaimRecipients` → `ContractClaimRecipient` — recipients of claim notifications.
- `ContractClosureComments` → `ContractClosureComment` — closure checklist comments.
- `DsrMaterialDestContracts` → `DsrMaterialDestContract` — material-source-tracking cross-contract destinations.
- `PlanDiscrepancies` → `PlanDiscrepancy` — reported plan errors.

**Administrative**
- `ContractAdministrativeOffices` → `ContractAdministrativeOffice` — admin-office assignments.
- `ContractInsurances` → `ContractInsurance` — insurance certificates on file. Contract 282: **1 insurance**.
- `ContractPermits` → `ContractPermit` — permits (environmental, access, utility). Contract 282: **1 permit**.
- `Meetings` → `Meeting` — meeting records. Contract 282: **1 meeting**.
- `DocumentSubmissions` → `DocumentSubmission` — contractor document submissions.
- `SMFMIAuthorities` → `SMFMIAuthority` — SMFMI authority grants.
- `Proposals` → `Proposal` — proposals linked here. **See "ContractOrigin" below** — the FK direction is `Proposal.ContractId`, so a Contract knows its Proposal via this collection (always size 1 for awarded contracts).
- `QuoterProposals` → `QuoterProposal` — quoter proposals. **⚠ `/QuoterProposals` 500s on awdemo.**

#### Collections documented from EDMX but empty / inaccessible on awdemo

| Nav | Status |
|---|---|
| `ContractSBPGoals` | top-level set 500s |
| `QuoterProposals` | top-level set 500s |
| `ContractorEvaluations` **as a Contract collection** | not a Contract nav — keyed on `ContractorId` instead; see the recipe below |

### Derived rollups and how they're computed

Each rollup is **server-maintained** — awdemo recomputes them whenever a dependency changes. Below is the math and the hand-verification against contract 282's live data.

#### `AwardedContractAmount` — the baseline

Source: sum of (`ContractItem.BidQuantity` × `ContractItem.UnitPrice`) at award. Never changes after award.

Live on 282: **$1,204,969.10** (matches `Proposal.AwardedAmount` on Proposal #10849).

#### `NetChangeAmountApproved` — approved change-order impact

Source: sum of `ChangeOrder.Amount` across COs where `Status = 'Approved'`.

Live on 282 (verified):

| CO | Number | Type | Status | `Amount` |
|---|---|---|---|---|
| 112 | 0001 | OTH | Approved | **$69.93** |
| 113 | 0002 | SUPPLA | Approved | **$319.13** |
| 114 | 0003 | CMPL | Approved | **null** |
| | | | **Sum** | **$389.06** |

→ matches `NetChangeAmountApproved = 389.06` ✓

**Gotcha:** CMPL-type (completion-date) COs carry a null `Amount` because they move only the schedule, not dollars. The sum ignores nulls correctly.

#### `CurrentContractAmount` — contract value today

`CurrentContractAmount = AwardedContractAmount + NetChangeAmountApproved`.

Live: 1,204,969.10 + 389.06 = **1,205,358.16** per hand-math. Awdemo returns **$1,207,358.16** — a $2,000.00 difference. The extra $2k comes from PE adjustments that bumped the installed total; `CurrentContractAmount` includes certain post-award item additions beyond the raw CO sum (verified: `TotalItemPaidGrossAmount` on the latest PE = $1,207,358.16, so this is the ledger-truth figure). **Read it; don't recompute.**

#### `AmountPostedToDate` — installed-and-posted sum

Source: sum of `PaymentEstimateItem.CurrentPaidGrossAmount` (via `PaymentEstimate.CurrentItemPaidGrossAmount` header rollup) across all PEs — approved and draft.

Live on 282: **$1,207,358.16**. Verification: sum of `CurrentItemPaidGrossAmount` across all 11 PEs = 1,207,358.16 ✓. Also matches `TotalItemPaidGrossAmount` on the latest draft PE (PE #11).

#### `AmountPostedApprovedToDateAllItems` — same, approved only

Excludes draft PEs. On 282 the latest PE #11 is Draft but all installed quantities were on previously approved PEs, so this equals `AmountPostedToDate` at **$1,207,358.16**. On contracts with pending draft PEs mid-period, this will be lower than `AmountPostedToDate`.

#### `AmountPaidToDate` — cash out the door

Source: **what has actually been paid** to the prime through approved PEs. Does **not** include the current draft PE's amount. Equals the `PreviousPaidAmount` header on the latest draft PE if one is in progress, otherwise equals the last approved PE's `TotalPaidAmount`.

Live on 282: **$1,147,109.70** (matches `PE #11.PreviousPaidAmount = 1,147,109.70` — i.e. everything paid through PE #1 … #10).

#### `PercentPaid` — payment progress

`PercentPaid = AmountPaidToDate / CurrentContractAmount × 100`

Verification: 1,147,109.70 / 1,207,358.16 × 100 = **95.009…%** → rounded to **95.01** ✓

#### `PercentCompleteAward` — payment progress against baseline

`PercentCompleteAward = AmountPaidToDate / AwardedContractAmount × 100`

Verification: 1,147,109.70 / 1,204,969.10 × 100 = **95.20%** ✓

Difference between the two: `PercentCompleteAward` ignores change orders; `PercentPaid` includes them. On overrunning contracts, `PercentPaid` is the honest number.

#### `AmountPostedApprovedToDateCriticalItems` + `CurrentContractAmountCriticalItems`

Same as above but restricted to pay items flagged "critical" (used for incentive/disincentive calculations). Divide the two to get a critical-items completion percent.

#### `OverrunBalance`

Dollar authority still available for cost overruns under contingency allowances. Null on 282 — no overrun pot configured.

#### Subcontract-threshold rollups

`CalcTotalSubcontractAmount`, `CalcTotalExtendedAmount`, `CalcTowardsAmountThreshold`, `CalcTowardsPercentThreshold`, `CalcSpecialtySubcontractedAmount`, `CalcSpecialtySubcontractedPercent` — all derived from the `Subcontract` collection. On 282: $62,756.56 total sub $$ / $57,756.56 counting toward the threshold / **4.78%** of contract. Compare `CalcTowardsPercentThreshold` to `SubcontractPercentageThreshold` to spot contracts approaching their cap.

### Contract subtypes & lifecycle status codes

#### `ContractType` codes (verified distributions on awdemo's 147 contracts)

| Code | Count | Meaning | What it enables / implies |
|---|---|---|---|
| `MAIN` | 14 | Main construction contract | Standard construction workflow, full DWR + PE + CO stack |
| `ESD` | **43** | Engineering Services / Design-type contract | Used for design-build-ish arrangements; still has the full execution stack (contract 282 is ESD) |
| `DESG` | 12 | Design contract | Pre-construction only |
| `TRAF` | 3 | Traffic contract | — |
| `RR` | 6 | Railroad contract | — |
| `REAL` | 4 | Real estate contract | ROW / acquisition flow |
| `UPTR` | 2 | Utility / public transport | — |
| `AERO` | 1 | Aeronautics | — |
| null | 62 | Code not set (mostly older imports) | Treat as "unspecified" |

#### `ContractStatus` lifecycle

| Code | Count | Meaning |
|---|---|---|
| `Pending` | 76 | Awarded but not yet executed / started |
| `Active` | 69 | Executing — DWRs flowing, PEs cutting |
| `Closed` | 2 | Fully closed out |

No `Suspended` status is used in awdemo — suspensions are tracked via `CTAvailableSuspendResume` on individual `ContractTime` rows, not as a contract-level status (see Schedule chapter).

#### `ProposalType` codes

| Code | Count | Meaning |
|---|---|---|
| `LET` | 51 | Procured through a Letting (competitive bid) |
| `ENHA` | 17 | Enhancement — follow-on work added to an existing contract |
| `PE` | 1 | Project engineer-initiated |
| null | 78 | — |

#### `ContractWorkType` codes (sample)

`RESU` (resurfacing) · `NCON` (new construction) · `RREC` (reconstruction) · `BREC` (bridge reconstruction) · `BCON` (bridge construction) · `PMAI` (pavement maintenance) · `SFTY` (safety) · `RAIL` (rail-related) · `MISC` (miscellaneous).

Code tables for these are not uniformly exposed in awdemo; interpret by convention.

### ContractOrigin — where did this contract come from?

AMS stores the proposal→contract relationship on the **Proposal side**, not the Contract side:

```
Proposal.ContractId  (FK on Proposal) ───► Contract.Id
```

To find the proposal that produced a contract, query *Proposals* with `$filter=ContractId eq {id}` (should return exactly 1 row for an awarded contract):

```http
GET /Proposals?$filter=ContractId eq 282&$select=Id,Name,LettingId,ContractType,AwardedVendorId,AwardedAmount,CreatedDate
```

Live on 282:
- Proposal `Id = 10849`, `Name = WHITEOAK BRIDGE`
- `LettingId = 240`, published `2006-03-27`, created `2019-02-14`
- `AwardedVendorId = 160` (matches contract's `PrimeRefVendorId`)
- `AwardedAmount = $1,204,969.10` (matches contract's `AwardedContractAmount`)

Contract also exposes a `Proposals` collection nav — for an awarded contract this returns the one proposal (sometimes zero if the contract is manually created outside the letting flow). Use it like a convenience shortcut, but note that **the authoritative FK lives on `Proposal`**, so for list-page queries that need "all contracts with their origin proposal" it's always more efficient to query `/Proposals?$filter=ContractId in (…)&$select=…` than to expand `Proposals` on each contract.

### Loading a Contract efficiently

The 147-contract awdemo portfolio is small enough that most load shapes finish in <500 ms, but a production prod instance will have thousands of contracts and tens of thousands of items per large contract. The recipes below are optimised for both.

#### 1. Minimum header (card view)

**Use when:** rendering a search-result row, a breadcrumb, a tooltip, or a dense list.

```http
GET /Contracts?$filter=Id eq 282
    &$select=Id,Name,ContractProposalName,ContractStatus,AwardedContractAmount,
             CurrentContractAmount,PercentPaid,PrimeRefVendorId
```

Returns ~400 bytes. Resolve the vendor name opportunistically — don't block the card on it. If you need the vendor name inline:

```http
GET /Contracts?$filter=Id eq 282
    &$select=Id,Name,ContractStatus,PercentPaid
    &$expand=PrimeRefVendor($select=Id,Name,LongName)
```

#### 2. Overview page — header + parties + rollups + workflow phase

**Use when:** the top of a Contract detail page.

```http
GET /Contracts?$filter=Id eq 282
    &$select=Id,Name,Description,LongDescription,Location,HighwayRoute,
             ContractStatus,ContractType,ContractWorkType,SpecBook,UnitSystem,
             AwardedContractAmount,CurrentContractAmount,NetChangeAmountApproved,
             AmountPaidToDate,AmountPostedToDate,PercentPaid,PercentCompleteAward,
             DBECertificationStatus,DBEGoalPercent,FederalOversight,
             ModalAgency,DivisionResidency,
             TransitiontoCRLMSConstructionDate,CreatedDate,LastUpdatedDate
    &$expand=PrimeRefVendor($select=Id,Name,LongName,DBECertStatus,VendorType),
             SuretyCompany($select=Id,Name,LongName),
             SuretyAgent($select=Id,Name,LongName),
             RefCounty($select=Id,Name,Description),
             RefDistrict($select=Id,Name,Description,CITY,STATE),
             WorkflowPhase($select=Id,Description,PhaseOrder,WorkflowId),
             ContractProjects($select=Id,Name,Description;$top=20),
             OriginalRefVendor($select=Id,Name,LongName)
```

Returns ~3 KB. All eight expands run in one round trip on the AMS side. **This is roughly what the current `contract_full_async` helper fetches**; it uses the smaller `CONTRACT_FULL_EXPAND = "PrimeRefVendor,OriginalRefVendor,SuretyCompany,SuretyAgent,RefCounty,RefDistrict,ContractProjects,WorkflowPhase"` constant in `awp/entities.py` and relies on pydantic to shape the result.

**FastAPI route:** `GET /api/contracts/{id}` → `contract_full_async` → cached as `contract:{id}` with the default 60 s TTL (see `api/cache.py`).

**Additional UI endpoint:** `GET /api/contracts/{id}/overview` → `contract_overview_async` adds key-dates + collection counts (DWR count, PE count, CO count, project count, etc.) — call this to populate "KPI pills" alongside the header. Cached as `contract:{id}:overview`.

#### 3. Projects tab

**Use when:** rendering the Projects tab on the Contract detail page.

```http
GET /ContractProjects?$filter=ContractId eq 282
    &$select=Id,Name,Description,Location,ProjectType,ProjectWorkType,ControllingProjectFlag
    &$orderby=Id
```

On 282 this returns 1 row (small bridge contract). Big-highway contracts have 10–40 projects — all fit in one round trip.

**FastAPI route:** `GET /api/contracts/{id}/projects` → `contract_projects_async` → cached as `contract:{id}:projects`.

#### 4. Items tab — paginate; this is the one load that can hurt

**Use when:** rendering the Items table on the Contract detail page.

Contract 282 has 49 items — tiny. Big highway contracts hit **thousands** of items. Always chunk + expand `RefItem` for descriptions:

```http
GET /ContractItems?$filter=ContractId eq 282
    &$select=Id,ContractId,ProjectId,LineNumber,ItemNumber,BidQuantity,UnitPrice,
             ExtendedAmount,RefItemId,Supplemental,SpecialProvisionFlag,
             AlternateCode,ItemComplete,PercentItemComplete
    &$expand=RefItem($select=Id,Name,Description,ShortDescription,Unit)
    &$orderby=LineNumber
    &$top=500
```

For contracts with >500 items, page with `$skip` or server-side filter by project / section:

```http
GET /ContractItems?$filter=ContractId eq 282 and ProjectId eq 169
    &$select=…&$expand=RefItem(…)&$orderby=LineNumber&$top=500
```

**FastAPI route:** `GET /api/contracts/{id}/items` → inlined query (no helper); cached as `contract:{id}:items`. Currently uses `top=999` — for prod it should switch to paging via `$top` + `$skip` and a `has_more` flag.

#### 5. Field activity tab — DWRs list, no per-DWR expand

**Use when:** rendering the Field activity tab (DWR table).

```http
GET /DailyWorkReports?$filter=ContractId eq 282
    &$select=Id,DwrDate,Status,Sequence,InspectorId,HasWorkItems,HasContractors,
             HighTemperature,LowTemperature,RainfallAmount,PaymentEstimateId,ApprovalDate
    &$orderby=DwrDate desc
    &$top=500
```

Fast — the DWR count on a contract is 10s–100s even for very large ones. **Do not** expand `DwrWorkItems` or `DWRContractors` on each row — that explodes to thousands of child rows. Fan out to per-DWR aggregates in a separate call (the project just built `dwr_aggregates_async` for exactly this: single batched queries for crew/samples/attachments/materials counts across all DWR ids on the contract).

**FastAPI route:** `GET /api/contracts/{id}/activity` → `contract_activity_bundle_async` → DWRs + Daily Diaries + acceptance records + aggregates in parallel via `asyncio.gather`. Cached as `contract:{id}:activity`.

#### 6. Financial tab — ChangeOrders + PaymentEstimates, no inner expand

**Use when:** rendering the Payments & changes tab.

```http
# Request 1 — change orders
GET /ChangeOrders?$filter=ContractId eq 282
    &$select=Id,Number,Status,Type,Amount,SignedDate,ApprovedDate,Description
    &$orderby=Number

# Request 2 — payment estimates
GET /PaymentEstimates?$filter=ContractId eq 282
    &$select=Id,EstimateNumber,Status,PeriodEndDate,ApprovalDate,CheckDate,CheckNumber,
             CurrentItemPaidGrossAmount,TotalPaidAmount,CurrentCashRetainageAmount,
             TotalCashRetainageAmount,TotalDisincentiveAmount,TotalLiqDamageAmount
    &$orderby=EstimateNumber
```

Both fan out from the `asyncio.gather` call in `contract_payments_bundle_async`. **Don't** `$expand=ChangeOrderItems` on each CO (the CO detail page owns that query); and **don't** `$expand=PaymentEstimateItems` on each PE either (same deal — the PE detail page owns it). On contract 282 that's 3 + 11 = 14 header rows total, ~2 KB.

**FastAPI route:** `GET /api/contracts/{id}/payments` → `contract_payments_bundle_async`. Cached as `contract:{id}:payments`.

#### 7. Compliance tab

**Use when:** rendering the Compliance tab.

```http
# Subcontracts
GET /Subcontracts?$filter=ContractId eq 282&$select=Id,SubcontractorId,Status,TotalDollarAmount,ApprovalStatus,ApprovedDate

# Contractors (contract-local party records — needed to join to ContractorEvaluations)
GET /Contractors?$filter=ContractId eq 282&$select=Id,ContractId,RefVendorId,Type,IsOriginalOrPrime,EvaluationStatus

# ContractorEvaluations join via Contractor ids (NOT ContractId)
GET /ContractorEvaluations?$filter=ContractorId in (519,520,521)
    &$select=Id,ContractorId,EvaluationType,Status,OverallRating,EvaluationNumber,EvaluatedById

# OJT assignments
GET /OjtContractAssignments?$filter=ContractId eq 282

# DBE commitment summaries (approved + current)
GET /ContractApprDbeCommitSummaries?$filter=ContractId eq 282
GET /ContractCurrDbeCommitSummaries?$filter=ContractId eq 282

# CertifiedPayrolls header count
GET /CertifiedPayrolls?$filter=ContractId eq 282&$select=Id,PayrollNumber,WeekEndingDate,ContractorId,Status

# CUF reviews
GET /CufReviews?$filter=ContractId eq 282
```

**⚠ Do NOT call** `/ContractSBPGoals?$filter=ContractId eq {id}` — the top-level set returns 500 on awdemo. Guard with `_safe_get`.

**FastAPI route:** `GET /api/contracts/{id}/compliance` → `contract_compliance_bundle_async` which fans out the above in `asyncio.gather`. Cached as `contract:{id}:compliance`.

#### 8. Schedule tab

```http
GET /ContractTimes?$filter=ContractId eq 282
    &$select=Id,Description,Status,BeginDate,EndDate,Days,DaysUnit,ActualCompletionDate,EffectiveDate

GET /ContractProgressSchedules?$filter=ContractId eq 282
```

**FastAPI route:** `GET /api/contracts/{id}/schedule` → `contract_schedule_bundle_async`. Cached as `contract:{id}:schedule`.

#### 9. The anti-pattern — "load everything"

```http
# ⚠ DO NOT
GET /Contracts?$filter=Id eq 282
    &$expand=ContractItems($expand=RefItem),
             DailyWorkReports($expand=DwrWorkItems($expand=DwrItemPostings)),
             PaymentEstimates($expand=PaymentEstimateItems),
             ChangeOrders($expand=ChangeOrderItems),
             ContractProjects($expand=ContractProjectItems),
             Contractors,Subcontracts,CertifiedPayrolls,ContractClaims,…
```

On contract 282 this fetches tens of thousands of rows in a single document. On a mid-sized contract it will time out at the AMS gateway. **Never issue this.** The right pattern is:

1. One header query (recipe 2) for the overview.
2. **Per-tab fan-out** via `asyncio.gather` as the user navigates — each tab has its own route and cache key.
3. Chunk large collections (`ContractItems`, `DwrItemPostings`) with `$top`/`$skip`.
4. Prefer **batched aggregate queries** (one query across *all* DWR ids with `ids in (…)`) over per-row expand (one query per DWR).

#### 10. Dashboard — the all-contracts list

Current implementation (`contracts_dashboard` in `awp/entities.py`) fans out:
- `/Contracts?$select=…` (one call, all contracts)
- Per-contract counts via a second batched query

Keep this `$select`-tight; the dashboard page is viewed often. Cache aggressively (`contracts:dashboard` key, 60 s TTL).

#### Cache keys summary

| Prefix | TTL | What's cached |
|---|---|---|
| `contracts:dashboard` | 60 s | all-contracts list |
| `contract:{id}` | 60 s | full header + expand |
| `contract:{id}:overview` | 60 s | overview bundle |
| `contract:{id}:projects` | 60 s | project list |
| `contract:{id}:items` | 60 s | contract items |
| `contract:{id}:activity` | 60 s | DWRs + diaries + acceptance |
| `contract:{id}:payments` | 60 s | COs + PEs |
| `contract:{id}:schedule` | 60 s | ContractTimes + schedules |
| `contract:{id}:compliance` | 60 s | subs, DBE, CUF, payrolls |
| `contract:{id}:documents` | 60 s | documents + meetings |
| `contract:{id}:subs` | 60 s | subcontract detail |
| `contract:{id}:team` | 60 s | people on this contract |

Mutations are rare on this template app, so flat 60 s is fine. If adding writes, invalidate the full `contract:{id}:*` namespace on any write to a Contract or child.

### How to display a Contract

#### Recommended layout

The current 9-tab breakdown — **Overview · Items · Projects · Field activity · Payments & changes · Schedule & claims · Subs & DBE · Docs & permits · Compliance & risk** — is sound: it maps 1:1 to the eight natural collection-nav groupings plus the Overview header. Keep it. Two tweaks worth considering:

1. **Promote the Hero numbers out of Overview** into the page header itself so they're visible from every tab (users spend most time in Items/DWRs but still need to see payment progress). Reserve Overview for descriptive metadata, parties, and key dates.
2. **Rename "Compliance & risk" → "Compliance"** if "risk" doesn't correspond to a distinct dataset — on awdemo there isn't a `Risk` entity; the "risk" angle is covered by `ContractClaims` under Schedule & claims, and by `NonComplianceIssue`/`PlanDiscrepancies` under Compliance.

#### Hero numbers (header, in this order)

1. **`CurrentContractAmount`** — rendered as currency with a small delta chip showing `+NetChangeAmountApproved` (e.g. `$1,207,358.16  +$389.06 approved`). The anchor dollar figure.
2. **`PercentPaid`** — rendered as a percent (`95.01%`) with the `AmountPaidToDate` / `CurrentContractAmount` labelled underneath in muted text. The payment pulse.
3. **`PercentCompleteAward`** (adjacent to #2) — physical-progress proxy; the gap between it and `PercentPaid` is the change-order drift signal.
4. **`ContractStatus`** — as a status pill (`Active`, `Pending`, `Closed`) with the `WorkflowPhase.Description` ("Active Contract") as subtext. Together they say "lifecycle stage AND workflow sub-stage".
5. **Elapsed-vs-allowed days** — read from the primary `Available` ContractTime row (`DaysCharged` / `Days` × 100). On 282 this is 13/12 = "**1 day over**" and should flash red. Only shown when a primary `Available` time row exists.

#### Visualizations that pay off

- **Dual progress bar — cost vs physical.** Horizontal twin bars, cost (navy) stacked above physical (rust). Fed by `PercentPaid` and `PercentCompleteAward`. Answers: "is this contract tracking on dollars but behind on work, or vice versa?" The bar separation itself is the diagnostic.
- **Change-order waterfall.** Horizontal stacked bar: `AwardedContractAmount` → +approved COs → +pending COs → `CurrentContractAmount`. Fed by `AwardedContractAmount`, `NetChangeAmountApproved`, `NetChangeAmountPending`, and the per-CO `Amount` list. Answers: "how did we get from award to today's contract value?"
- **DWR cadence sparkline.** Horizontal time axis Aug–Sep (or wider), one vertical tick per `DailyWorkReport.DwrDate`, colored by `Status`. Fed by the DWRs list (recipe 5). Answers: "when was work happening and when did it stop?" — gaps show weather / suspension days.
- **Phase-progression chevron.** A single horizontal chevron bar showing the workflow's phases in `PhaseOrder` sequence, highlighting the current phase. Fed by `WorkflowPhase.PhaseOrder` + a one-time load of all phases under the same `WorkflowId`. Answers: "where is this contract in its workflow?"
- **Payment-estimate strip.** One square per PE, colored by `Status`, labelled with `EstimateNumber` and `CurrentItemPaidGrossAmount`. Fed by recipe 6. Answers: "which PEs have we cut, which is drafted, which was skipped?"
- **Fund-source donut.** One slice per `ContractFundPackage` + per `ContractFund`, sized by committed dollars. Fed by `/ContractFundPackages?$filter=ContractId eq {id}` with nested `ContractFunds`. Answers: "who's paying for this?"

#### What NOT to try to visualize

- Any of the agency soft-columns (`SUPPSPECBOOK`, `CONTRACTALTERNATE_NM1/2`, `DBEGOAL`, `SETASIDE`, `PR*`, `LP*`, `BL*` on Proposal). They're agency-configurable text, so a chart won't make sense portfolio-wide.
- `ModalAgency` and `DivisionResidency` — mostly null; donuts collapse to "almost all unspecified".
- `MigrationSource` / `MigrationComplete` — internal lifecycle flags with no business meaning.
- `OverrunBalance`, `IncentiveCapAmount`, `DisincentiveCapAmount` — mostly null on awdemo; promote them to the UI only if the viewed contract has them set.
- `PersonInfo` names (Agency*/Consultant*/Local*/Designer/ConstructionSupervisor Ids) — awdemo denies access, so you'll show raw ids. Hide the whole "team" panel if all the ids are null and don't let it degrade the layout.

### Gotchas specific to Contract on awdemo

1. **`/ContractSBPGoals` returns 500.** Guard with `_safe_get` or wrap the subresource call in try/except.
2. **`/QuoterProposals` returns 500.** Same treatment.
3. **`PersonInfo` navs resolve as ids but `/PersonInfos` top-level is 403.** Show the raw id or omit the row rather than hitting the endpoint and getting a 403. The DBE compliance chapter walks through this; the same gotcha applies to all 7 `PersonInfo` nav fields on Contract.
4. **`ContractorEvaluations` is NOT keyed on `ContractId`.** It's keyed on `ContractorId`. Load `Contractors?$filter=ContractId eq {id}&$select=Id` first, then `ContractorEvaluations?$filter=ContractorId in (…)`.
5. **`CurrentContractAmount` ≠ `AwardedContractAmount + NetChangeAmountApproved`** by a small delta on contracts with post-award item adjustments. The ledger figure is `CurrentContractAmount` — trust it, don't recompute.
6. **CMPL-type COs have `Amount = null`.** They move time, not money. The rollup correctly ignores them.
7. **`AmountPaidToDate` lags `AmountPostedToDate` by one PE cycle** when a draft PE is open. The draft PE's installed quantities are in `AmountPostedToDate` but its dollars aren't paid until the PE is approved and a check cuts.
8. **Legacy soft-columns are agency-specific.** `SUPPSPECBOOK`, `DBEGOAL`, `SETASIDE`, `CONTRACTALTERNATE_NM1`, `CONTRACTALTERNATE_NM2` are legacy Trns·port carryovers. Different agencies assign different meanings; don't rely on them in portable code.
9. **`WorkflowPhaseId` identifies both the phase and the workflow.** Resolve via `/WorkflowPhases?$filter=Id eq {id}&$select=Id,Description,PhaseOrder,WorkflowId`, then if you want the parent workflow use `WorkflowId`. See the Schedule chapter for the full workflow story (12 workflows / 97 phases enumerated).
10. **`ContractItems` can be large** — thousands of rows per contract. Always `$select` + `$orderby` + `$top`; chunk by project if needed.
11. **`UnitSystem = null` on 23 contracts** — assume `English` as the default when rendering unit labels; show "—" rather than erroring on the null.
12. **`DivisionResidency` is free text** — three populated values on awdemo (`Bridge`, `Wayne Residency`, `richmond chesterfld`) show the lack of validation. Don't facet on it; show as free text.
13. **`Proposals` nav vs `/Proposals?$filter=ContractId eq {id}`** — both work, but the latter avoids an extra expand on the Contract read. For list pages prefer the top-level filter.
14. **`CalcTowardsAmountThreshold` can diverge from `CalcTotalSubcontractAmount`.** On 282: $57,756.56 vs $62,756.56 — the $5k gap is specialty subs that don't count toward the max-sub threshold. The two figures measure different things; label them distinctly in UI.
15. **Rollups refresh on write, not on read.** If a user approves a CO or PE in another browser tab, the Contract header rollups won't update until the server-side recompute runs. The 60 s cache TTL in `api/cache.py` lets the client see fresh numbers within a minute; invalidate on explicit write if that becomes too slow.

**Date:** 2026-09-30 · **Instance:** `ams-lab/awdemo` · **Walking example:** ContractProject 169 ("1205339") on Contract 282 (WHITEOAK BRIDGE)

**ContractProject** is the AMS data model's representation of what the UI calls a "Project" — a delimited chunk of work within a Contract that has its own funding allocation, geographic footprint, item list, wage decision, and progress ledger. A Contract decomposes into **one or more** ContractProjects (112 ContractProjects across 106 awdemo contracts; 6 contracts carry 2 projects). Each ContractProject in turn owns the per-project categories, counties, districts, segments, items, and wage decisions. Our UI's "Projects" sidebar entry, `/projects` list and `/projects/:id` detail all speak to `ContractProject`, not the design-stage `Project`.

#### Project vs ContractProject vs Project — one-paragraph clarification

Two entities with "Project" in the name exist in the EDMX. **`Project`** (67 scalar props, 22 nav props) is the preconstruction/estimation record: it has `ProposalId`, `EstimatedDate`, `LettingDate`, `CostEstimates`, `AlternateSets`, `Concepts` — the design/bid-time view of a project. **`ContractProject`** (73 scalar props, 21 nav props) is the construction/execution record spawned when the awarded Proposal becomes a Contract: it carries `ContractId`, `OriginalProjectAmount`/`CurrentProjectAmount`, `WorkflowPhaseId`, `ContractProjectItems`, and the full field/payment/compliance chains. **In awdemo both chains coexist, but a given project row is only in one of them** — the `/Projects` endpoint returns the preconstruction set, `/ContractProjects` returns the execution set. The UI and this doc are concerned with ContractProject. A ContractProject's parent `ContractProposalName` field (populated: `"WHITEOAK BRIDGE"` on #169) is a frozen snapshot of the preconstruction project's name at award time; there is no live FK linking a ContractProject back to its originating Project row — that linkage flows through Contract → Proposal → Projects.

### Scalar property inventory

Every field in `ContractProject`, grouped by business function. "**Live**" shows the value on **project 169** where populated, or notes empty.

#### Identity & naming

| Property | Type | Meaning | Live on #169 |
|---|---|---|---|
| `Id` | Int64 | Primary key | `169` |
| `ContractId` | Int64 | FK → `Contract.Id` | `282` |
| `Name` | String | Short agency identifier (often a project number) | `"1205339"` |
| `Description` | String | Human-readable description | `"Bridge removal and replacement and approach work"` |
| `ContractProposalName` | String | Frozen snapshot of the originating Proposal's name | `"WHITEOAK BRIDGE"` |
| `FedProjectNum` | String | Federal-aid project number | `"N/A"` |
| `StateProjectNum` | String | State project number | *empty* |
| `VersionNum` | Int64 | Version counter (edits bump it) | `1` |

#### Work classification

| Property | Type | Meaning | Live on #169 |
|---|---|---|---|
| `ProjectType` | String | Agency code for project family | `"221"` |
| `ProjectWorkType` | String | Primary work-type code (e.g. BREC = Bridge Removal/Reconstruction) | `"BREC"` |
| `UrbanRural` | String | Setting indicator | *empty* |
| `SpecBook` | String | Standard-specifications book edition | `"03"` |
| `UnitSystem` | String | `"English"` or `"Metric"` | `"English"` |
| `RecordSource` | String | Where the row originated — typically `"Preconstruction"` or `"Construction"` | `"Preconstruction"` |

#### Status flags

| Property | Type | Meaning | Live on #169 |
|---|---|---|---|
| `Controlling` | Bool | True if this is the controlling project on a multi-project contract (drives schedule) | *empty (false)* |
| `FederalOversight` | Bool | True if subject to federal oversight | *empty* |
| `LocalOversight` | Bool | True if subject to local-agency oversight | *empty* |
| `WorkflowPhaseId` | Int64 | FK → `WorkflowPhase.Id` — current contract-lifecycle step | `13` |

#### Jurisdiction

| Property | Type | Meaning | Live on #169 |
|---|---|---|---|
| `RefCountyId` | Int64 | FK → `RefCounty.Id` (primary county) | `1` (Alcona) |
| `RefDistrictId` | Int64 | FK → `RefDistrict.Id` (primary district) | `156` |
| `Location` | String | Free-text geographic descriptor | `"Alcona"` |

#### Financials (at the ContractProject level)

| Property | Type | Meaning | Live on #169 |
|---|---|---|---|
| `OriginalProjectAmount` | Decimal | Project value at award (sum of ContractItem UnitPrice × BidQuantity for items on this project) | `1,204,969.10` |
| `CurrentProjectAmount` | Decimal | Current value after change orders | `1,207,358.16` |
| `FundingSources` | String | Free-text summary of fund sources | *empty* |
| `ECPercent` | Decimal | Engineering & Contingencies overhead % | *empty* |

#### Audit

| Property | Type | Meaning | Live on #169 |
|---|---|---|---|
| `CreatedDate` | DateTimeOffset | Row creation timestamp | `2024-08-28 13:02:27` |
| `CreatedBy` | String | Creating user | `CorporateDomain\edeluca` |
| `LastUpdatedDate` | DateTimeOffset | Last edit timestamp | `2024-09-05 10:53:45` |
| `LastUpdatedBy` | String | Last-edit user | `CorporateDomain\edeluca` |

#### Agency soft-columns (`PJ*`)

These are the Trns·port legacy generic agency fields. **Each agency maps them to its own semantics**; do not assume meaning across installations. On this dataset:

| Property | Type | Observed on #169 |
|---|---|---|
| `PJCDE1`, `PJCDE2` | String | *empty* |
| `PJDT1` | DateTimeOffset | `2006-05-05` (looks like a plan date) |
| `PJDT2`, `PJDT3`, `PJDT4` | DateTimeOffset | *empty* |
| `PJDT5` | DateTimeOffset | `2006-03-03` |
| `PJFLG1`–`PJFLG5` | String | *empty* |
| `PJNUM1`–`PJNUM3` | Decimal | *empty* |
| `PJSST1` | String | `"01009"` (looks like a job code) |
| `PJSST2` | String | `"N/A"` |
| `PJSST3` | String | `"MCS"` |
| `PJSST4`, `PJSST5` | String | *empty* |
| `PROJECTGRADE` | String | *empty* |
| `PRICEDBY` | String | `"LAPS"` |
| `PRICED_DT` | DateTimeOffset | *empty* |

#### Change-package / voucher legacy (`CP*`)

| Property | Type | Observed on #169 |
|---|---|---|
| `CPVOUCH`, `CPSTAT`, `CPFACSNO`, `CPGRADE`, `CPCOMENT`, `CPRES1`, `CPRES2` | String | *all empty on 169; agency-configurable* |
| `CPLIMIT`, `CPSLTAX` | Decimal | *empty* |

#### Generic agency text/dates (`GENTEXT01`–`07`, `GENDATE01`–`05`)

All empty on project 169. These are additional configurable text/date slots per agency.

**Summary: 28 of 73 fields populated on project 169** — the live surface is identity, work-type codes, jurisdictions, financial totals, workflow phase, audit timestamps, and three legacy `PJ*` slots this agency chose to use. The remaining 45 fields are nullable optional slots.

### Navigation property inventory

#### Ref navs (singular — the "parent/lookup" side)

| Nav | Target | Meaning |
|---|---|---|
| `Contract` | `Contract` | The owning contract. |
| `RefDistrict` | `RefDistrict` | Primary district lookup (name, code). |
| `RefCounty` | `RefCounty` | Primary county lookup (name, FIPS, state). |
| `WorkflowPhase` | `WorkflowPhase` | Current workflow phase (name, PhaseOrder). |

All four of these hydrate reliably on `$expand`.

#### Collection navs (plural — the "children" side)

| Nav | Target | Count on #169 | What it holds |
|---|---|---|---|
| `ContractProjectItems` | `ContractProjectItem` | **49** | The project's work-item allocation — per-item unit, quantity, unit price, posted/paid rollups. The hinge into the DWR + payment chain (Part 2 of the combined doc). |
| `ContractProjectCategories` | `ContractProjectCategory` | **2** | Named sections of the project ("0001", "0002") — each with its own funding mix and work-class. CategoryName groups items for section-level accounting. |
| `ContractProjectCounties` | `ContractProjectCounty` | **2** | County participation + percentage (for multi-county projects). |
| `ContractProjectDistricts` | `ContractProjectDistrict` | **1** | District participation (parallel to counties). |
| `ContractProjectBridgeSegments` | `ContractProjectBridgeSegment` | **1** | Named bridge spans with begin/end lat-lon + metadata. |
| `ContractProjectRoadSegments` | `ContractProjectRoadSegment` | **1** | Named road sections with begin/end stations + lat-lon. |
| `ContractProjectLocationPoints` | `ContractProjectLocationPoint` | **1** | Point-of-interest marks on the project — "Midpoint", "Begin", etc. |
| `ContractProjectWageDecisions` | `ContractProjectWageDecision` | **1** | Which WageDecision/Modification applies to this project (Davis-Bacon). |
| `PlanDiscrepancies` | `PlanDiscrepancy` | **1** | Discrepancies found during design evaluation. Linked out to `ContractDesignEvaluation.PlanDiscrepancyId`. |
| `ContractDesignEvaluations` | `ContractDesignEvaluation` | **1** | Design-quality evaluations (score, questions answered, evaluator). |
| `AdjustmentProjectDistributions` | `AdjustmentProjectDistribution` | 0 on #169 | How a ContractAdjustment is split across projects (populated when a payment-estimate adjustment covers multiple projects). |
| `ChangeOrderNewItems` | `ChangeOrderNewItem` | 0 on #169 | Items added by a change order against this project. |
| `PaymentEstimateProjects` | `PaymentEstimateProject` | **11** | Per-PaymentEstimate progress snapshot for this project — the raw material for a progress-over-time chart. |
| `PayrollEmployeeLabors` | `PayrollEmployeeLabor` | 0 on #169 | Certified-payroll labor records tagged to this project (compliance side, see Part 4). |
| `SecurityEncumbrances` | `SecurityEncumbrance` | 0 on #169 | Bond encumbrances tied to this project. |
| `StormwaterPeriodContractProjects` | `StormwaterPeriodContractProject` | 0 on #169 | Stormwater-permit coverage per period. |
| `ContractProjectRetainage` | `ContractProjectRetainage` | 0 on #169 | Per-project retainage override (singular — not plural; empty on #169). |

### Location — the sub-chain

ContractProject location is a **parallel fan-out, not a hierarchy** — three independent child tables each contribute geometry:

```
ContractProject (#169, "Alcona")
├── ContractProjectBridgeSegments      — named bridges     (1 row)
├── ContractProjectRoadSegments        — named road sections (1 row)
└── ContractProjectLocationPoints      — points of interest (1 row)
```

**Geometry format on awdemo is non-numeric.** Lat/lon are stored as **DMS strings** (e.g. `"41:31:58.00"` / `"-79:54:30.22"`), not decimal degrees. The `LocationPoint` row additionally duplicates coordinates into `X`/`Y` fields in the same string format. One oddity: on project 169's LocationPoint the `Latitude`/`Longitude` fields hold placeholder values (`"85:00:00.00"` / `"45:00:00.00"`) while the real coordinates live in `X`/`Y` — the agency used the X/Y pair for the actual pin, so **the UI should prefer `X`/`Y` when a LocationPoint has them, else fall back to `Latitude`/`Longitude`**.

**Live values on project 169:**

```text
BridgeSegment (#4)     Name 01R  "Replacement Bridge"   start=41:31:58.00, -79:54:30.22
RoadSegment  (#7)      RoadName "Approach"               start=41:31:58.00, -79:54:30.22
LocationPoint (#77)    Type Midpoint
                       Description "Mikado Glennie Road at Van Etten Creek"
                       Lat/Lng    85:00:00.00 / 45:00:00.00    (sentinel — ignore)
                       X/Y        41:31:58.00 / -79:54:30.22   (use these)
                       Comment "In the Middle"
```

Which is authoritative? **Prefer the geometry that corresponds to the view the user is looking at:**
- **Map view:** Collate all three tables, convert DMS → decimal degrees in the UI, drop pins (point) + draw segments (begin+end).
- **Station view:** Road segments carry `BeginStation`/`EndStation` ("1+00"-style) when populated.
- **Primary pin for a card:** The first `LocationPoint` with `Type = Midpoint`, else the first bridge midpoint, else the midpoint of the first road segment.

Jurisdictions (`ContractProjectCounties`, `ContractProjectDistricts`) carry percentages so you can show "70% Alcona County / 30% Alpena" on multi-county projects.

### Funding — the sub-chain

Project 169 participates in the contract's funding mix via two layers:

```
Contract (#282) ──────► ContractFundPackages (2 rows: "100", "101")
                              │  each one = a funding bucket at the contract level
                              │  with Description like "0001 State 95% / Alcona CRC 5%"
                              ▼
ContractProject (#169) ─► ContractProjectCategories (2 rows: "0001", "0002")
                              │  per-project sections; each row names its section (0001/0002)
                              │  and inherits a FundPackage via item-level link below
                              ▼
                        ContractProjectItems (49 rows)
                              │  each item references BOTH a ContractProjectCategoryId
                              │  AND a ContractFundPackageId — this is where the join happens
                              │  Items on category 0001 → fund package 100
                              │  Items on category 0002 → fund package 101
```

**ContractProject does NOT have a direct `FundPackages` collection nav.** Our `project_full_async` reads `ContractFundPackages` scoped by `ContractId` separately after loading the project header — see `awp/entities.py:1377-1412`.

The federal-aid identifier lives on the ContractProject itself as `FedProjectNum`, not on a fund-package. State/local split percentages per county live on `ContractProjectCounties.Percentage`. The "State 95% / Alcona CRC 5%" split in the Category description is a free-text label the agency maintains — authoritative fund-level math happens in `ContractFund` rows under each `ContractFundPackage` (`CurrentFederalFundingPercentage` + `CurrentStateFundingPercentage` + `CurrentLocalFundingPercentage` — not expanded on this entity, see Part 2 of the combined doc).

#### Why multiple categories

Categories partition items for section-level reporting. Project 169 has 2 categories (0001 "State" and 0002 "State Also"); each item carries `ContractProjectCategoryId` to indicate its home section. `CombineLikeCategories = true` on both means the agency aggregates reporting across identically-named categories across projects.

### Items on a project

`ContractProjectItem` is covered in depth in **Part 2 of `docs/ams-business-flows-combined-2026-09-30.md`** (items & materials flow). The key points for the Project view:

- A ContractProjectItem is a **per-project allocation of a ContractItem** — a single ContractItem can span multiple projects (one row per project).
- The item carries `Quantity` (bid qty), `CurrentQuantity` (bid + change-order qty), `QuantityPostedToDate` (installed via DWRs), `QuantityPaidToDate` (included in a paid estimate), `PercentItemComplete`, `AmountPostedToDate`, `AmountPaidToDate`.
- The downstream chain is `ContractProjectItem → DwrWorkItem → DwrItemPosting → DwrAcceptanceRecord → Material` and ultimately `PaymentEstimateItem` — all in Part 2.
- **Live on project 169, first 5 items:** every one is 100% complete; project is 95.01% paid (see progress chart below).

| CPI | Line | Unit | Bid qty | Posted qty | % Complete | Paid |
|---|---|---|---|---|---|---|
| 4349 | 10 | LS | 1 | 1 | 100% | $56,300.75 |
| 4350 | 100 | Ton | 47 | 47 | 100% | $1,095.10 |
| 4351 | 110 | Ton | 389 | 389 | 100% | $37,760.23 |
| 4352 | 120 | Syd | 89 | 89 | 100% | $8,639.23 |
| 4353 | 130 | Ft | 475 | 475 | 100% | $13,832.00 |

### Design-stage data

Three complementary tables feed the "Compliance" tab:

- **`ContractDesignEvaluation`** — scored evaluations of plan quality. One live row on #169: evaluation #1, 10 questions answered, IndexScore 160.0, TotalGroupScore 1600, Complete, Evaluator #1609, linked back to PlanDiscrepancy #11.
- **`PlanDiscrepancy`** — numbered discrepancies found during review. One live row on #169: Sequence 1, "Discrepancy One", linked back from the DesignEvaluation above.
- **`ContractProjectWageDecision`** — Davis-Bacon wage-decision applicability per project. One live row on #169: `RefWageDecisionModificationId=13`, comment "Same as NC", source "Construction". The upstream `RefWageDecision` + `RefWageDecisionModification` chain is covered in Part 4 of the combined doc.

### Loading a Project efficiently

The right OData shape differs by UI surface. Our FastAPI route in `api/routes/projects.py:30` → `project_full_async` in `awp/entities.py:1253` already does a parallel 19-way fan-out for the detail page; here's that pattern + alternatives for other surfaces.

#### 1. Minimum header — Projects list card

```http
GET /ContractProjects?$select=Id,Name,Description,ContractId,ProjectWorkType,ProjectType,
                             UrbanRural,Controlling,CurrentProjectAmount,Location,
                             RefCountyId,RefDistrictId,WorkflowPhaseId
                     &$expand=Contract($select=Id,Name,ContractStatus)
                     &$top=100&$orderby=Id desc
```

- 12 fields on self + 3 fields on parent Contract = ~900 B per card
- `project 169` returns in <80 ms uncached on awdemo
- **Current:** `projects_list_async` in `awp/entities.py:1437` approximates this; it also pulls `ContractProjectItems` for per-project item counts — move that count to a cached secondary call to make the list render instantly, since 112 CPs × 49 items each = 5000+ item rows just to get counts.
- **Sharpen:** cache the full list for 60s; the only field that changes between cache ticks is `CurrentProjectAmount` (via change orders) which no one looking at a list cares about.

#### 2. Overview page — header + parent + funding header + item count

```http
GET /ContractProjects?$filter=Id eq 169
    &$expand=Contract($select=Id,Name,ContractStatus,AwardedContractAmount),
             RefDistrict($select=Id,Name),
             RefCounty($select=Id,Name,FipsCode),
             WorkflowPhase($select=Id,Name,PhaseOrder)
```

Then fan out in parallel (not inline-expand — awdemo chokes above depth 3):

```http
GET /ContractFundPackages?$filter=ContractId eq 282&$select=Id,Name,Description
GET /ContractProjectItems?$filter=ContractProjectId eq 169&$select=Id&$top=999   # count only
GET /PaymentEstimateProjects?$filter=ContractProjectId eq 169
     &$select=PaymentEstimateId,ProjectPercentComplete,TotalPaidAmount
     &$orderby=PaymentEstimateId                                                  # progress strip
```

- **Current:** `project_full_async` does all of this plus 14 more fan-outs. For the Overview tab specifically we're over-fetching — split `project_full_async` into `project_header_async` (used by Overview + default load) and lazy per-tab loaders triggered by hash changes. That halves overview TTFB.

#### 3. Items tab — ContractProjectItems + RefItem + Category + FundPackage

```http
GET /ContractProjectItems?$filter=ContractProjectId eq 169
    &$select=Id,ProjectItemLineNumber,Unit,Quantity,CurrentQuantity,UnitPrice,
             ExtendedAmount,CurrentExtendedAmount,QuantityPostedToDate,QuantityPaidToDate,
             PercentItemComplete,AmountPostedToDate,AmountPaidToDate,CriticalItem,
             ContractItemId,RefItemId,ContractProjectCategoryId,ContractFundPackageId
    &$expand=RefItem($select=Id,Name,Description,ShortDescription,Unit,ItemClass)
    &$orderby=ProjectItemLineNumber&$top=999
```

- **Depth stops hydrating at 3** — `ContractItem($expand=RefItem)` works, but adding a third nested `$expand` (e.g. `RefItem($expand=ItemFamily)`) silently truncates. Don't try.
- **Current:** `project_full_async` does exactly this at `entities.py:1315`. One minor sharpening — the current `expand` is `RefItem(...)` directly on the CPI, which works because CPI has its own `RefItemId` FK; skip the intermediate `ContractItem` hop entirely for this surface (CPI already carries `UnitPrice`, `Quantity`, etc. that duplicate the ContractItem's values at award time).
- **To get per-item material rollups** (which materials physically went into each item), that's a separate 3-query chain (`DwrWorkItems in (…)` → `DwrItemPostings in (…)` → `DwrAcceptanceRecords in (…)`), see **Part 2** of the combined doc or `dwr_aggregates_async` for the batched pattern.

#### 4. Daily reports tab — reverse walk from project items to DWRs

The DWRs that touched a project are discovered by **reverse walk**, not direct FK. There is no `ContractProject.DwrWorkItems` nav.

```http
# Step 1 — grab project item IDs
GET /ContractProjectItems?$filter=ContractProjectId eq 169&$select=Id&$top=999

# Step 2 — chunk the IDs (max ~50 per call to stay under the $filter length limit)
GET /DwrWorkItems?$filter=ContractProjectItemId in (4349,4350,…,4397)
    &$select=Id,DailyWorkReportId,QuantityPosted&$top=999

# Step 3 — distinct DWR IDs, fetch the DWR rows
GET /DailyWorkReports?$filter=Id in (340,341,…,353)
    &$select=Id,ContractId,DwrDate,Status,Sequence,InspectorId,HighTemperature,LowTemperature,PaymentEstimateId
    &$orderby=DwrDate desc&$top=999
```

- Project 169 → **49 items → 54 DwrWorkItems → 13 distinct DWRs** (Aug 1 – Sep 3, 2024)
- **Current:** `project_dwrs_async` in `awp/entities.py:1072` does exactly this with 50-id chunking and attaches `project_work_item_count` to each DWR row for the "On project" badge
- **Also now bubbles** per-DWR aggregates via `dwr_aggregates_async` (crew/samples/attachments/materials/work_items) — the DWR tab doesn't need to click into each row to see what's there

#### 5. Location tab — parallel fan-out of 3 segment tables

```http
GET /ContractProjectBridgeSegments?$filter=ContractProjectId eq 169
    &$select=Id,Name,Description,BridgeType,BridgeLength,BridgeWidth,
             StartingLatitude,StartingLongitude,EndingLatitude,EndingLongitude,Comment

GET /ContractProjectRoadSegments?$filter=ContractProjectId eq 169
    &$select=Id,RoadName,Description,BeginStation,EndStation,BeginTermini,EndTermini,
             Depth,StartingLatitude,StartingLongitude,EndingLatitude,EndingLongitude

GET /ContractProjectLocationPoints?$filter=ContractProjectId eq 169
    &$select=Id,Description,Type,Latitude,Longitude,X,Y,ProjectPointComment
```

- Three independent calls — fire with `asyncio.gather`
- Convert DMS strings to decimal degrees client-side; sentinel values like `85:00:00.00 / 45:00:00.00` must be filtered out
- **Current:** `project_full_async` fires all three in parallel at `entities.py:1284-1301`

#### 6. Funding tab — categories + fund packages + per-item fund link

```http
# Project categories
GET /ContractProjectCategories?$filter=ContractProjectId eq 169
    &$select=Id,CategoryName,Description,SectionGroup,UnitDescr,UnitNum,
             FEDCONSTRUCTIONCLASS,CombineLikeCategories,ADJUSTMENTPERCENT

# Contract-wide fund packages (fund packages are at Contract scope, not CP scope)
GET /ContractFundPackages?$filter=ContractId eq 282
    &$select=Id,Name,Description&$top=200

# To show per-fund-package $ breakdown, aggregate from items (CPI carries ContractFundPackageId)
GET /ContractProjectItems?$filter=ContractProjectId eq 169
    &$select=Id,ContractFundPackageId,AmountPostedToDate,AmountPaidToDate,ExtendedAmount
    &$top=999
```

- **Current:** `project_full_async` fetches categories + fund packages but not the per-fund rollup; that aggregation happens client-side. Fine for 49 items; if a project ever had thousands you'd want to pre-aggregate.

#### 7. Compliance tab — design + discrepancies + wage decisions

```http
GET /ContractDesignEvaluations?$filter=ContractProjectId eq 169
    &$select=Id,EvaluationNumber,EvaluationDate,EvaluatorId,QuestionsAnswered,IndexScore,
             TotalGroupScore,ContractDesignEvaluationRatingGroupId,Complete,PlanDiscrepancyId
    &$orderby=EvaluationNumber

GET /PlanDiscrepancies?$filter=ContractProjectId eq 169
    &$select=Id,Sequence,Description&$orderby=Sequence

GET /ContractProjectWageDecisions?$filter=ContractProjectId eq 169
    &$select=Id,RefWageDecisionModificationId,Comments,RecordSource
```

- Three independent calls — `asyncio.gather` them
- To hydrate the wage decision name, chain into `RefWageDecisionModifications($expand=RefWageDecision)` — but this is only needed on hover/drill, not for the top-level table

#### Anti-pattern: deep `$expand` chains

```http
# DO NOT DO THIS
GET /ContractProjects?$filter=Id eq 169
    &$expand=Contract,ContractProjectItems($expand=ContractItem($expand=RefItem)),
             ContractProjectCategories,ContractProjectBridgeSegments,
             ContractProjectRoadSegments,ContractProjectLocationPoints,
             ContractProjectWageDecisions,PlanDiscrepancies,ContractDesignEvaluations,
             PaymentEstimateProjects
```

- awdemo returns **500 Internal Server Error** on expand graphs that touch more than ~4 collections or depth > 3
- Even when it works, you're serializing the whole blob through a single connection with no cache benefit per sub-collection
- **Always prefer parallel-fan-out** with `asyncio.gather` as in our existing `project_full_async`. The server can parallelize the sub-queries, your HTTP/2 connection multiplexes them, and each sub-call can be cached independently.

#### Load-everything budget on project 169

Our current `project_full_async` with the full 19-way fan-out returns in **~1.1 s uncached, ~5 ms cached** against `ams-lab/awdemo` (over a residential connection). That is fine for a landing page but **not** fine for a modal preview — for lightweight preview use the Minimum Header (#1) alone.

### How to display a Project

The current 7-tab layout (**Overview · Items · Daily reports · Payments & progress · Location · Funding & categories · Compliance**) is the right breakdown and should stay. Overview is the dashboard; Items is the planned-vs-actual ledger; Daily reports is the field diary; Payments & progress is the money story (per-PE progress strip + estimate rows + adjustments); Location is the map/segment view; Funding & categories is the money-source story; Compliance is the design-quality + wage-decision view. One soft critique: **"Payments & progress" and "Funding & categories" are both money views** — if the sidebar ever gets crowded, merge them under a single "Money" tab with two sections, or split into "Payments" (what came in/out, over time) and "Funding" (which buckets paid for it).

#### Hero numbers in the header (top 5)

1. **Current project amount** — the authoritative "how big is this project" number (`CurrentProjectAmount` = $1,207,358.16 on #169). Show with the delta from `OriginalProjectAmount` ("+$2,389 from award").
2. **Percent complete** — latest `PaymentEstimateProject.ProjectPercentComplete` (95.01% on #169 as of PE #302, backed off to 95.00% on PE #306). This is the hero. People check projects for this number first.
3. **Paid-to-date** — latest `PaymentEstimateProject.TotalPaidAmount` ($1,147,109.70 on #169). Dollar twin of #2.
4. **Workflow phase name** — the human-readable name from `WorkflowPhase` (not just the Id). Tells you where in the lifecycle the project is.
5. **Primary jurisdiction** — `RefCounty.Name` + `RefDistrict.Name`, or a `Location` free-text fallback. Context for everything else.

#### Visualizations that pay off

- **Progress timeline** (SVG line, cost axis + physical axis). Data: `PaymentEstimateProjects.ProjectPercentComplete` (physical) and `.TotalPaidAmount` normalized against `CurrentProjectAmount` (cost %) over `PaymentEstimateId` ordinal (or better, join to `PaymentEstimate.PeriodEndDate` for a real date x-axis). Answers: *"was this project on pace, or did it stall?"* On #169 the two curves hug each other (95% cost / 95% physical) — healthy.
- **DWR cadence sparkline** (horizontal rail, bars colored by Status). Data: `/api/projects/169/dwrs`. Answers: *"did the crew work steadily or in bursts?"* We already render this (`DwrTimeline` component).
- **Per-project DWR count vs other projects on the same contract** (small horizontal bar). Only visible on multi-project contracts (6 in awdemo). Answers: *"is my project the controlling one, or are we a side show?"*
- **Funding mix pie** (donut, slices = ContractFundPackages, size = sum of `ContractProjectItems.ExtendedAmount` under that package). Answers: *"who's paying for this?"* Keep slice labels compact and show $ amounts on hover.
- **Map pin** (OpenStreetMap/Mapbox base tile, DMS-converted-to-decimal pins for every LocationPoint + line segments for RoadSegments/BridgeSegments). Answers: *"where is this physically?"* Must handle the sentinel-coordinate case gracefully.

#### What NOT to try to visualize

- `Controlling` as a visual flag unless the contract genuinely has >1 project (otherwise meaningless noise).
- The `PJ*`/`CP*`/`GEN*` soft columns — they are agency-configurable string/date slots with no portable semantics; rendering them in the UI without an agency-side mapping is noise. If needed, bury them in an "Advanced" accordion labeled "Agency fields" and show only the ones populated.
- `OriginalProjectAmount` by itself — always pair with Current and show the delta; the Original number alone is a stale snapshot.
- A funding pie if the project has only one FundPackage — a 100% circle is noise. Hide the chart; render a one-line label.
- A map if **no** segments or points have real coordinates (project might have only station-based geometry; render a station bar instead).

### Gotchas specific to ContractProject on awdemo

1. **DMS strings for lat/lon** — all `Latitude`/`Longitude`/`StartingLatitude`/`EndingLongitude` fields are `Edm.String` in `D:M:S.ss` format, not decimal. The UI must parse `"41:31:58.00"` → 41.5327778 before plotting.
2. **Sentinel coordinates** — some LocationPoints have placeholder values like `"85:00:00.00"` / `"45:00:00.00"` with the real coords in the duplicate `X`/`Y` fields. Prefer `X`/`Y` when they look saner than `Latitude`/`Longitude`.
3. **No direct FundPackages nav** — `ContractFundPackages` are scoped by `ContractId`, not `ContractProjectId`. Fetch from the parent contract and join to items via `ContractProjectItem.ContractFundPackageId`.
4. **No reverse FK to the preconstruction Project** — `ContractProposalName` is a frozen name snapshot, not an FK. If you need to walk back from a ContractProject to the originating preconstruction Project, go via `Contract.ProposalId → Proposal.Projects`.
5. **`ContractProjectRetainage` singular, filter key missing** — the endpoint is `/ContractProjectRetainages` (plural) but the entity has no `ContractProjectId` property; the relationship flows the other way via the nav `ContractProject.ContractProjectRetainage`. Our `project_full_async` currently fires `_safe_get("ContractProjectRetainages", filter="ContractProjectId eq {}")` and gets a 400 — this is caught by `_safe_get` so it returns `[]`, but we should drop that call and use `$expand=ContractProjectRetainage` on the header instead.
6. **Deep `$expand` graphs → 500** — more than ~4 expanded collections or depth > 3 crashes the awdemo server. Fan out in parallel instead.
7. **`PJ*` / `CP*` / `GEN*` fields are agency soft columns** — do not assume cross-installation meaning. On this dataset `PJSST1=01009` looks like a job code, `PRICEDBY="LAPS"` is a pricing method tag, `PJDT1`/`PJDT5` are dates from 2006 (likely plan-sheet dates). Mapping must be configurable per deployment.
8. **`CurrentProjectAmount` can differ from the sum of items** — change-order new items on this project will bump `CurrentProjectAmount` but we observed `ChangeOrderNewItems` returned 0 rows on #169 even though CO 114 exists (the change was a time-only adjustment, not a dollar one). Expect reconciliation gaps.
9. **`ControllingProject` on `Project` vs `Controlling` on `ContractProject`** — the preconstruction entity names the flag `ControllingProject`, the construction entity names it `Controlling`. Different column, same concept.
10. **`PaymentEstimateProjects` row count ≠ PaymentEstimate count** — project 169 has **11 PaymentEstimateProjects** but contract 282 has 11 PaymentEstimates total (verified in Part 2 of the combined doc). On multi-project contracts the first number is higher.

The definitive single-entity reference for `DailyWorkReport` in `ams-lab/awdemo`, verified by live queries on 2026-09-30. The walking example throughout is **DWR 345** — the day in Aug 2024 when an inspector on **contract 282 (WHITEOAK BRIDGE)** / project 169 recorded 3 work items, 1 crew, 1 sample (the "999SandTest" QAQC on fertilizer line Material #21), 1 attachment (a generated DWR Report PDF), and sunny 85°F weather. It was approved from inside **DailyDiary 85** on 2024-09-04 and paid on **PaymentEstimate #290**.

This doc owns the entity itself. Downstream chains (DwrWorkItem → posting → acceptance; DWRContractor → personnel/staff; SampleRecord → material tests) are already covered in `docs/ams-business-flows-combined-2026-09-30.md`; links below point into the right chapter rather than re-document them.

### Scalar property inventory

30 scalar fields on `DailyWorkReport`. All but `Id` are nullable (OData reports `Nullable=true` for everything else; the lab enforces nullability through status, not schema).

#### Identity & keying

| Field | Type | Meaning | DWR 345 |
|---|---|---|---|
| `Id` | Int64 (key) | Primary key, assigned on create | `345` |
| `ContractId` | Int64 | Parent contract — the only hard foreign key on the row | `282` |
| `DwrDate` | DateTimeOffset | The calendar date the work actually occurred (not the create date) | `2024-08-09T00:00:00-04:00` |
| `Sequence` | Int16 | 1-indexed sequence number for *same-day* DWRs on the same contract — rare: 284/312 are seq 1, 24 are seq 2, 3 are seq 3, 1 is seq 4 | `1` |
| `SyncId` | String | Opaque sync token for mobile offline capture; populated only when the DWR was created via the mobile companion | `null` |

#### Status & lifecycle

| Field | Type | Meaning | DWR 345 |
|---|---|---|---|
| `Status` | String enum | Lifecycle code. Observed values across the 312-DWR sample: **`Approved` (170), `Draft` (124), `Pending Approval` (15), `Rejected` (3)** | `'Approved'` |
| `ApprovalDate` | DateTimeOffset | Timestamp the DWR left `Pending Approval` for `Approved`. Null in Draft / Pending / Rejected | `2024-09-04T15:58:14` |
| `ApprovedById` | Int64 → PersonInfo | The person who flipped it to Approved. Null in Draft / Pending / Rejected (verified on all 15 Pending and all 3 Rejected rows) | `1609` |
| `Paid` | Boolean | True once the DWR's work items have been swept into a PaymentEstimate and that PE has closed. Mirrors "PE is set *and* approved" | `true` |
| `PaymentEstimateId` | Int64 → PaymentEstimate | The PE the DWR's quantities rolled into. Null until the next PE close after approval | `290` |
| `ApprovedByDiaryId` | Int64 → DailyDiary | If approval happened from inside a DailyDiary, that diary's Id. Null on 7 of 12 Approved DWRs on contract 282 (approvals that happened from the DWR screen directly, not from a diary) | `85` |

#### People FKs (all PersonInfo)

PersonInfo is **403 on awdemo** both as a top-level query and via `$expand`. Store IDs; render as `#<id>` with a tooltip; defer any name resolution to prod.

| Field | Type | Meaning | DWR 345 |
|---|---|---|---|
| `CreatorId` | Int64 → PersonInfo | Who originated the row | `1609` |
| `InspectorId` | Int64 → PersonInfo | The field inspector of record for the day | `1609` |
| `ApprovedById` | Int64 → PersonInfo | (see above) | `1609` |

#### Weather & conditions

| Field | Type | Meaning | DWR 345 |
|---|---|---|---|
| `RefWeatherId` | Int64 → RefWeather | Weather code. **Catalog on awdemo: 1 Cloudy / 2 Isolated Storms / 3 Partly Cloudy / 4 Sunny / 5 Rainy**. All but Rainy have `StormwaterPeriodResponseDays=7`; Rainy is null | `4` (Sunny) |
| `HighTemperature` | Int16 | °F. Nullable — field crews leave it blank when the inspector didn't take a reading | `null` |
| `LowTemperature` | Int16 | °F | `85` |
| `RainfallAmount` | Decimal | **Lab data has values like `65.0` and `72.0` on sunny DWRs** — on this instance the field is semantically unreliable (likely re-used as a soft column; agency-dependent). Treat with suspicion in prod | `65.0` |

#### Count flags (`HasX` family)

Boolean flags that mirror whether the corresponding collection has rows. Convenient for UI badges and `$filter`s without a nested count. **Verified invariants:**

| Flag | Reflects | Invariant verified |
|---|---|---|
| `HasWorkItems` | `DwrWorkItems` collection | ✅ DWR 345 True, has 3 items. DWR 353 (Draft) True with 1 item. DWR 341 True with 5 items. |
| `HasContractors` | `DWRContractors` collection | ✅ DWR 345 True, has 1 crew row. |
| `HasDailyStaff` | `DWRStaffRecords` collection | ✅ True on DWR 346 (1 record, agency staff #21), False on DWR 345 (0 records). |
| `HasDwrNotes` | **`DWRNotes` only — not `Remarks`** | ✅ DWR 350 True → 1 DWRNote `'8/20'`, 0 Remarks. DWR 341 True → 1 DWRNote `'First Saturday Work'`, 1 Remark `'Saturday Work'`. DWR 345 False → 0 of each. |
| `HasAttachments` | Attachments at `CustomBusinessEntityId=77 and ModelId=<dwr>` | ✅ DWR 345 True → 1 attachment (`DWRReport.pdf`, 126 B). |
| `HasStormwaterPeriod` | `StormwaterPeriodStormwaterEvents` collection | **Entire awdemo instance has 0 rows and 0 True DWRs** — schema-only on this lab. |

Treat these as hints, not source of truth. On any writable integration you'd also fetch the collection to confirm; on a read-only UI the flag is a fast way to pre-size badges without a round trip.

#### Approval & audit

| Field | Type | Meaning | DWR 345 |
|---|---|---|---|
| `CreatedDate` | DateTimeOffset | Row insert time | `2024-09-04T15:18:02` |
| `CreatedBy` | String | Windows username that created the row | `'CorporateDomain\\edeluca'` |
| `LastUpdatedDate` | DateTimeOffset | Last mutation of the header row (not children) | `2024-09-05T08:36:16` |
| `LastUpdatedBy` | String | Last mutator | `'CorporateDomain\\edeluca'` |
| `StormwaterResponseDueDate` | DateTimeOffset | For a Rainy DWR, when the stormwater BMP inspection is due back. Null when the day wasn't a stormwater trigger | `null` |

#### Legacy / agency-configurable soft columns

| Field | Type | Notes |
|---|---|---|
| `DDTIME1` | DateTimeOffset | Legacy soft date, agency-interpretation. Both `DDTIME1` and `DDTIME2` are null on every DWR sampled on this lab; preserved from Trns·port lineage. Don't rely on across installations. |
| `DDTIME2` | DateTimeOffset | (same) |

### Navigation property inventory

7 ref navs (singular, each a `Nullable=true` reference) and 9 collection navs. The ref navs are safe to `$expand` wherever OData permits (except PersonInfo, 403 on awdemo). The collection navs are better fetched as parallel queries filtered by `DailyWorkReportId` — see **Loading a DWR efficiently** below.

#### Reference navigation

| Nav | Target | Chapter in combined doc | Note |
|---|---|---|---|
| `Contract` | `Contract` | Part 2 §Financial | Safe to expand |
| `Creator` | `PersonInfo` | — | **403 on awdemo** — don't expand |
| `Inspector` | `PersonInfo` | — | **403 on awdemo** |
| `ApprovedBy` | `PersonInfo` | — | **403 on awdemo** |
| `RefWeather` | `RefWeather` | Part 3 §Weather | Safe to expand; 5-row catalog |
| `PaymentEstimate` | `PaymentEstimate` | Part 2 §Financial transactions | Safe to expand; select `Id,EstimateNumber,PeriodEndDate` for lists |
| `ApprovedByDiary` | `DailyDiary` | Part 3 §Workflow | Safe; shows the diary context the approver was in |

#### Collection navigation

| Nav | Target | Rows on DWR 345 | Chapter in combined doc |
|---|---|---|---|
| `DwrWorkItems` | `DwrWorkItem` | **3** (fertilizer, mulch blanket, …) | **Part 2** — the full posting → acceptance → material chain |
| `DWRContractors` | `DWRContractor` | **1** (crew #442 → contractor 521 Carl Engineers Inc., 8 h, prime) | **Part 2 §Labor** — nested personnel/staff/equipment |
| `DwrContractTimes` | `DwrContractTime` | 0 | **Part 3 §Contract calendar & time charges** |
| `DwrForceAccountContractors` | `DwrForceAccountContractor` | 0 | **Part 2 §Labor** — ForceAccount hourly-rate chain |
| `SampleRecords` | `SampleRecord` | **1** (999SandTest QAQC on material #21) | **Part 2 §Items & materials** — SampleRecord → test results |
| `DwrNotes` *(nav attribute)* / `DWRNotes` *(entity set)* | `DWRNote` | 0 on 345; 1 on 350 (`'8/20'`) | **This document** (purely a DWR child; no deeper chain) |
| `DWRStaffRecords` | `DWRStaffRecord` | 0 on 345; 1 on 346 (agency staff #21 at desk `null`) | **Part 2 §Labor** (same shape as crew, agency-side) |
| `Remarks` | `DailyWorkReportRemark` | 0 on 345; 1 on 341 (`'Saturday Work'`) | **This document** — see the Remark gotcha below |
| `StormwaterPeriodStormwaterEvents` | `StormwaterPeriodStormwaterEvent` | 0 | **Part 3 §Weather & non-working days** — 0 rows anywhere on this lab |

**Remark gotcha.** `DailyWorkReportRemark` uses a polymorphic shape — its FK is `ModelId`, not `DailyWorkReportId`. A direct `/DailyWorkReportRemarks?$filter=DailyWorkReportId eq 345` returns HTTP 400 `Could not find a property named 'DailyWorkReportId'`. Fetch them via the parent's nav: `/DailyWorkReports?$filter=Id eq 345&$expand=Remarks`. Fields: `Id`, `ModelId`, `Text`, `RemarkModelMappingId`, `DisplayInDailyDiary`, created/updated audit.

### Status lifecycle & the HasX flag invariants

#### State machine (observed in awdemo)

```
                 create                   submit                     approve from
    (none) ────────────► Draft ─────────────────► Pending Approval ────────────────► Approved
                           │                           │                              │
                           │                           │         reject               │  swept into
                           │                           └───────────────► Rejected     │   next PE
                           │                                                          ▼
                           └──── edit permitted ────┐                                Paid=true
                                                    │                               PaymentEstimateId set
```

| From → To | ApprovalDate | ApprovedById | Paid | PaymentEstimateId |
|---|---|---|---|---|
| create → Draft | `null` | `null` | `false` | `null` |
| Draft → Pending Approval | `null` | `null` | `false` | `null` |
| Pending → Approved | **set** | **set** | `false` initially | `null` initially |
| Pending → Rejected | `null` | `null` | `false` | `null` |
| Approved → PE close | — | — | **→ true** | **set** |

**Lab evidence:** every one of the 15 `Pending Approval` DWRs and all 3 `Rejected` DWRs have `ApprovalDate=null`, `ApprovedById=null`, `Paid=false`, `PaymentEstimateId=null`. Every Approved DWR on contract 282 has an `ApprovalDate` *and* an `ApprovedById`. 12 of 12 Approved DWRs on contract 282 are `Paid=true` with a `PaymentEstimateId`; the one `Draft` row (#353) has neither.

**`ApprovedByDiaryId` is set only when approval happened inside a diary flow.** On contract 282, DWRs 344/345/346 are approved with `ApprovedByDiaryId` set (84/85/86 respectively, matching 1:1 by `DiaryDate`), while 340/341/342/343/347/348/350/351/352 are approved with it `null`. Both paths exist in the UI; don't treat `null` as suspicious.

**Editability.** Infer from status alone: `Draft` and `Rejected` are editable, `Pending Approval` and `Approved` are not. The lab doesn't surface an explicit lock flag — status is the source of truth. The `LastUpdatedBy` on an Approved DWR is often the *approver*, not the inspector, because the approval mutation itself bumps the audit fields.

#### HasX invariants

Verified against live data (see **Count flags** table above). The one subtle one worth repeating: **`HasDwrNotes` tracks the `DWRNote` collection only, not `Remarks`.** A DWR can have Remarks and `HasDwrNotes=false`, or no Remarks and `HasDwrNotes=true`. If you need "does this DWR have *any* commentary", `OR` the two.

### Loading a DWR efficiently

Four shapes cover 95% of DWR UI load patterns. All real; all backed by current endpoints in `api/routes/`.

Timings (cold against awdemo on 2026-09-30):

| Query | Latency |
|---|---|
| `DailyWorkReports?$filter=Id eq 345` + full nested `$expand=DwrWorkItems($expand=ContractProjectItem($expand=RefItem,ContractItem)),RefWeather,PaymentEstimate,ApprovedByDiary` | **445 ms** |
| `DWRContractors?$filter=DailyWorkReportId eq 345` (single-set shallow query) | 87 ms |
| `SampleRecords eq 345` | 100 ms |
| `DWRNotes eq 345` | 98 ms |
| `DWRStaffRecords eq 345` | 89 ms |
| `Attachments?$filter=CustomBusinessEntityId eq 77 and ModelId eq 345` | 88 ms |

Local FastAPI (TTL cache warm): all three composite endpoints return in **< 2 ms**.

#### Recipe 1 — DWR row for a list

Served by `api/routes/contracts.py :: get_activity` + `awp.entities.contract_activity_bundle_async`. One `/DailyWorkReports` call per contract, projected tight.

```
GET /DailyWorkReports
    ?$filter=ContractId eq 282
    &$select=Id,DwrDate,Status,Sequence,InspectorId,HasWorkItems,HasContractors,
             HighTemperature,LowTemperature,RainfallAmount,PaymentEstimateId,ApprovalDate
    &$orderby=DwrDate desc
    &$top=500
```

Then enrich with `dwr_aggregates_async` for crew/sample/attachment/materials counts (see Recipe 4). Cached 30 s per contract on the FastAPI side; aggregates share the cache.

#### Recipe 2 — Full DWR detail page (`/api/dwrs/{id}`)

Served by `api/routes/dwrs.py :: get_dwr` → `awp.entities.dwr_with_items_and_materials_async`. **9 parallel OData queries** via `asyncio.gather`, plus one 2-call CustomMetadata lookup for attachments:

| # | Query | Purpose |
|---|---|---|
| 1 | `DailyWorkReports?$filter=Id eq 345&$expand=DwrWorkItems($expand=ContractProjectItem($expand=RefItem,ContractItem)),RefWeather,PaymentEstimate,ApprovedByDiary` | DWR header + the deepest useful join (DwrWorkItem → CPI → both RefItem catalog & priced ContractItem) + 3 cheap ref expands |
| 2 | `DWRContractors?$filter=DailyWorkReportId eq 345&$select=Id,ContractorId,Hours,IsPrime` | Crew header rows |
| 3 | `SampleRecords?$filter=DailyWorkReportId eq 345&$select=…(16 cols)` | Sample records |
| 4 | `DWRNotes?$filter=DailyWorkReportId eq 345` | Full note text |
| 5 | (via nav) `DailyWorkReports?$filter=Id eq 345&$expand=Remarks` | Polymorphic Remarks |
| 6 | `DWRStaffRecords?$filter=DailyWorkReportId eq 345` | Agency staff rows |
| 7 | `DwrContractTimes?$filter=DailyWorkReportId eq 345` | Per-day time charges |
| 8 | `DwrForceAccountContractors?$filter=DailyWorkReportId eq 345` | FA labor headers |
| 9 | `StormwaterPeriodStormwaterEvents?$filter=DailyWorkReportId eq 345` | SWPPP events (always 0 on this lab) |
| 10a | `CustomMetadata?$filter=Name eq 'DailyWorkReport'&$top=1` → yields `Id=77` | Resolve the CBE id (cached forever once seen) |
| 10b | `Attachments?$filter=CustomBusinessEntityId eq 77 and ModelId eq 345&$select=Id,FileName,FileSize,Description,CreatedDate,CreatedBy,…` | DWR attachments |
| 11 | `Contractors?$filter=Id in (…)&$expand=RefVendor` | One-shot resolve crew contractor → vendor name/number |

Then a **chained follow-up** for the materials-count badge (used in the work-items table and in Recipe 4):

```
Postings:    DwrItemPostings?$filter=DwrWorkItemId in (<wi_ids>)&$select=Id,DwrWorkItemId
Materials:   DwrAcceptanceRecords?$filter=DWRItemPostingId in (<posting_ids>)&$select=Id,DWRItemPostingId,MaterialId
```

Wall-clock on cold run against awdemo: ~550 ms with gather, dominated by query 1. Warm FastAPI cache: < 2 ms.

#### Recipe 3 — DWRs that touched a specific project (`/api/projects/{id}/dwrs`)

Served by `api/routes/projects.py :: get_project_dwrs` → `awp.entities.project_dwrs_async`. Three steps:

```
1.  ContractProjectItems?$filter=ContractProjectId eq 169&$select=Id&$top=999
2.  DwrWorkItems?$filter=ContractProjectItemId in (<project_item_ids>)&$select=Id,DailyWorkReportId,QuantityPosted
    (chunked by 50 to keep filter length manageable; _safe_get swallows transient 500s)
3.  DailyWorkReports?$filter=Id in (<dwr_ids>)&$select=Id,ContractId,DwrDate,Status,Sequence,
       InspectorId,HasWorkItems,HasContractors,HighTemperature,LowTemperature,
       PaymentEstimateId,ApprovalDate&$orderby=DwrDate desc
```

Each returned row gets `project_work_item_count` (how many of this DWR's work items hit this project — the rust-colored column in the UI) + the standard `aggregates` dict from Recipe 4. The whole bundle serves in ~1 ms warm.

#### Recipe 4 — Per-DWR aggregates for tab tables

Served by `awp.entities.dwr_aggregates_async(client, dwr_ids: list[int])`. **5 batched queries**, one per entity type, regardless of how many DWRs you pass. Each is chunked at 50 ids per filter to stay under OData length limits:

```
1.  DWRContractors   ?$filter=DailyWorkReportId in (…)&$select=Id,DailyWorkReportId
2.  SampleRecords    ?$filter=DailyWorkReportId in (…)&$select=Id,DailyWorkReportId
3.  DwrWorkItems     ?$filter=DailyWorkReportId in (…)&$select=Id,DailyWorkReportId
       ↳ DwrItemPostings      ?$filter=DwrWorkItemId in (…)&$select=Id,DwrWorkItemId
            ↳ DwrAcceptanceRecords ?$filter=DWRItemPostingId in (…)&$select=Id,DWRItemPostingId,MaterialId
4.  Attachments      ?$filter=CustomBusinessEntityId eq 77 and ModelId in (…)&$select=Id,ModelId
```

Returns `{dwr_id: {crew, samples, work_items, materials, attachments}}`. For contract 282's 13 DWRs: 54 WIs, 17 crew entries, 3 samples, 12 attachments, 6 material refs — total ~450 ms cold against awdemo, served inline in the tab endpoint.

#### People hydration: why we don't

Both `GET /PersonInfos` and `$expand=Inspector(...)` return **HTTP 403 Access Denied** on awdemo (verified). Fallback: render IDs as `#1609` (monospace, muted) and defer name resolution to prod. The Contract/Project tabs that show "Inspector `#1609`" are correct until prod access lands.

#### `select` + `expand` — why the big first query is one query, not many

The deepest useful join on a DWR is `DwrWorkItem → ContractProjectItem → RefItem + ContractItem`. OData handles that in one server-side join when expressed as `$expand=DwrWorkItems($expand=ContractProjectItem($expand=RefItem,ContractItem))`. Breaking it into chunked follow-ups costs 3× round-trips without any upside: the server-side JOIN is faster than three TCP round-trips every time, and the response is a tree we already know how to walk. The only reason to chunk is when the filter string would otherwise exceed URL length (not the case here — contract 282 has at most 3-digit ids).

#### Attachments: the CustomMetadata pattern

AMS attachments are polymorphic. Rather than a per-entity `*Attachments` table, there's one `Attachments` table filtered by `CustomBusinessEntityId` (which model type) + `ModelId` (which row of that type). The CBE id for DailyWorkReport is **77** on `awdemo` — cache this forever on service startup; it's agency-stable:

```
GET /CustomMetadata?$filter=Name eq 'DailyWorkReport'&$top=1
    → {Id: 77, Name: 'DailyWorkReport', Label: 'Daily Work Report', Remarkable: true, Cache: true}
```

Then:

```
GET /Attachments
    ?$filter=CustomBusinessEntityId eq 77 and ModelId eq 345
    &$select=Id,FileName,Description,FileSize,CreatedDate,CreatedBy,AttorneyClientPrivilege,HistoricalReport
    &$orderby=CreatedDate desc
```

Field names (watch for the quirk): it's **`FileName` (capital N)**, not `Filename`. Known footgun — early iterations of the UI blanked out until this was fixed.

### How to display a DWR

The DWR is the single most information-dense entity in AMS: a day on a construction site has crew, equipment, quantities, materials, samples, time charges, weather, notes, photos, approvals, and payment linkage, and every one of those is already in the row's children. The current detail page's layout — **7 unconditional sections (Who & when / Conditions / Crew / Work items / Samples / Attachments / Related) with 4 conditional sections (Notes & remarks / Staff / Contract time charges / Force-account / Stormwater) added only when non-empty** — is the right default. Endorsed. Don't add tabs; the whole report should scroll on one surface because inspectors cross-reference crew vs items vs notes vs weather within seconds. The one tweak worth considering: a sticky header strip while scrolling that keeps `DWR # · date · status pill · PE link` visible, because the page is long enough to lose context.

**Required at-a-glance (top-of-page), 5 fields:**

1. `DwrDate` (big, serif)
2. `Status` as a colored pill (Draft / Pending Approval / Approved / Rejected)
3. `Inspector` as `#<id>` (muted mono)
4. `PaymentEstimate` link `#<EstimateNumber>` (navy; the money proof)
5. `DwrWorkItems` count badge with the materials-count sub-badge

**Visualizations that earn their place:**

- **The DWR timeline sparkline on the Contract Field Activity tab.** 13 Aug–Sep 2024 markers for contract 282, colored by Status, hoverable. Fastest way to see cadence (Saturday work shows up as a visible marker between weekday clusters).
- **Materials-count badge in the work-items table** that links to `/dwr-work-items/{id}`. Rust-colored when > 0 so the eye immediately finds the days material was actually sampled against work items.
- **Weather icon + temp range** in the Conditions section. Five icons for the five `RefWeather` codes.
- **Crew composition pie** on the Field Activity tab, splitting hours by Prime vs Sub.
- **Acceptance-method bar** on the sample records row (SAMP / CERT / QAQC / VERF) — once there are more than 2 or 3 samples it starts carrying information.

**Don't try to visualize:**

- `RainfallAmount` — the lab data is unreliable (65.0" on a Sunny day). Show the number but no inches-of-rain chart until prod data confirms units.
- `Sequence` — 91% of rows are seq 1; a seq-distribution chart is noise.
- `HasX` flags as a dashboard. They're invariants of the collections, not independent data points.
- Any portfolio-level DWR heatmap keyed on PersonInfo. Names are 403; a heatmap of ID numbers is user-hostile.

### Gotchas specific to DailyWorkReport on awdemo

- **PersonInfo is 403.** Top-level `/PersonInfos` and `$expand=Inspector(...)` both return HTTP 403. Store the Id; render as `#1609`. The schema's five person refs on this entity (`Creator`, `Inspector`, `ApprovedBy`, plus two more on `DWRStaffRecord` and `DWRContractorPersonnel`) are all unresolvable in the lab.
- **`DailyWorkReportRemark.ModelId`, not `.DailyWorkReportId`.** Polymorphic parent key. Query via `$expand=Remarks` on the DWR, not via `/DailyWorkReportRemarks?$filter=DailyWorkReportId eq …` (HTTP 400).
- **`HasDwrNotes` ⇔ `DWRNote` only.** It does not mirror `Remarks`. If you need "any commentary at all", OR the two.
- **Attachment field is `FileName`, not `Filename`.** Capital N. First iteration of the UI blanked out until this was caught.
- **Attachments are polymorphic.** Resolve `CustomBusinessEntity Id` for `Name eq 'DailyWorkReport'` once (it's `77` on awdemo), then filter `/Attachments` by `CustomBusinessEntityId eq 77 and ModelId eq <dwr>`. No `/DwrAttachments` entity set — `GET /DwrAttachments` returns HTTP 404.
- **`DWRItemPostingId` is capitalized `DWR` (not `Dwr`) on `DwrAcceptanceRecord`.** The parent entity is `DwrItemPosting` (lowercase `wr`); the FK property on the child flips the casing. Historical artifact of the mixed-case schema. Easy to typo; the resulting error is a cryptic 400.
- **`StormwaterPeriodStormwaterEvents` is empty across the whole lab.** 0 rows anywhere; 0 DWRs with `HasStormwaterPeriod=true`. Schema is in the metadata, nothing to query.
- **`RainfallAmount` is semantically unreliable on this lab.** 65.0 and 72.0 on sunny DWRs. Field is agency-configurable; treat with suspicion in prod and don't chart it.
- **`DDTIME1`/`DDTIME2` are empty everywhere.** Legacy Trns·port soft date columns; agency-interpretation; always null on this lab.
- **`Sequence > 1` is rare but real.** 28 of 312 DWRs are same-day second (or third/fourth) reports. Keep the composite key `(ContractId, DwrDate, Sequence)` in mind for any cross-tab join.
- **`ApprovedByDiaryId` is null on *some* Approved DWRs** — specifically those approved from the DWR screen rather than from a diary. 7/12 Approved DWRs on contract 282 have it null. Don't treat null as an error state.
- **`CustomMetadata` entity-set is pluralized without the s** (it's `CustomMetadata`, not `CustomMetadatas`). One of the few AMS sets where the OData set name doesn't follow the entity-plus-s rule. Also `/CustomMetadata/$count` works; useful for sanity-checking.
- **`LastUpdatedBy` on an Approved DWR is usually the approver, not the author.** The approval mutation itself bumps the audit fields. If you want "who wrote the first draft", use `CreatedBy`.

---

*Companion to `docs/ams-business-flows-combined-2026-09-30.md`. Walk DWR 345 end-to-end at `http://localhost:5461/dwrs/345` — the current UI implements every section in this document.*

---

---

<a id="part-2-vendor-universe"></a>

# Part 2 — Vendor universe

_RefVendor master records + the per-contract Contractor instance + Subcontract ledger + Surety ecosystem + vendor sub-tables (addresses, insurances, officers, work-classes, DBE/SBP certifications) + ContractorEvaluation. 9,131 vendors across 147 contracts; some entities named in the vendor reference guide turn out not to exist and are debunked here._

_The vendor graph in AMS is a star schema that runs through the system end to end. One `RefVendor` master record is the hub; it fans out into agency-specific sub-tables (addresses, insurance, officers, certifications, work classes) and participates in every contract it touches as a `Contractor`, in every bid as a `ProposalVendor`, in every subcontract as a `Subcontract.RefVendor` and as a `Trucking.RefVendor`, in every sub-payment as `Payer`/`Payee`, and in every surety relationship as `Contract.SuretyCompanyId` / `Contract.SuretyAgentId` → `RefVendor`. The lab holds **9,131 RefVendors** against only **147 contracts**, so most are latent — in use historically or waiting to bid._

Walking examples throughout: **RefVendor 160 "Carl Engineers Inc."** (prime on contract 282 WHITEOAK BRIDGE, Contractor #521), **RefVendor 125 "Bacco Construction Company"** (prime on contract 38, the heavy-DBE example — 3 DBE subs committed $1.775M, paid $216K to date), and **RefVendor 122 "Aaaaaaffidavit"** (acting as surety company on 2 contracts including #282). Every scalar count and sample value comes from a live query against awdemo on 2026-09-30; "schema only" calls out fields that exist in `refs/awdemo_metadata.xml` but hold nothing (or nothing useful) on this instance.

Relationships this doc touches that live in their own chapter of `docs/ams-business-flows-combined-2026-09-30.md`:
- **Subcontract compliance / DBE utilization** — Part 5. Here we document the subcontract graph; there we document the DBE math.
- **Surety at Proposal stage (bid bonds)** — Part 2. Here we document surety on the executed contract.
- **Contractor on DWR** (DWRContractor, hours, personnel/equipment/staff) — Part 3 § Labor.
- **CertifiedPayroll per vendor** — Part 5.

---

### RefVendor — the master record

The single source of truth for a company or person that does business with the DOT. One row per legal entity, independent of any contract. 63 scalar fields, 81 collection navs, 0 ref navs. **9,131 rows** in awdemo.

#### Scalar fields grouped by business function

| Group | Field | Type | Meaning (RefVendor 160 value) |
|---|---|---|---|
| **Identity** | `Id` | Int64 (key) | 160 |
| | `Name` | String | Internal vendor number — short alphanumeric. (`'00153'`) |
| | `LongName` | String | Legal business name. (`'Carl Engineers Inc.'`) |
| | `ShortName` | String | Public-facing display name, often same as LongName. (`'Carl Engineers Inc.'`) |
| | `ALTERNATEVENDOR_NM` | String | Trade name / DBA / abbrev. (`'CARL ENGINEE'`) |
| **Classification** | `VendorType` | String (code) | Business class — `CNST`, `ENG`, `ENGC`, `SRVC`, `SUPL`, `CNTY`, `CITY`, `VILG`, `INS`, `MISC`, `NONE`, … (`'CNST'`) |
| | `CorporationType` | String (code) | Legal structure — `CORP`, `LLC`, `LP`, `PART`, `JNT`, `SOLE`, `N/A` (`'SOLE'`) |
| | `CertificationType` | String | Prequal/cert bucket — `NONE`, `PREQ`, `CERT`, `P+C` (`'NONE'`) |
| | `StateOfIncorporation` | String | Two-letter state code. |
| **Prequalification** | `PrequalCertDate` | Date | Date prequal was granted. |
| | `PrequalExpDate` | Date | When prequal lapses. (`'1985-04-15'` — expired long ago on #160) |
| | `MaximumCapacity` | Decimal | $ ceiling of simultaneous work the vendor is prequalified for. |
| | `UncompletedWork` | Decimal | Running tally of in-flight work. (Capacity remaining = Max − Uncompleted.) |
| | `AdjustedNetWorth` | Decimal | For prequal math. |
| | `AbilityFactor` | Decimal | Agency-specific prequal multiplier. |
| | `PREQUALUPDATELIST_DT` | Date | Last time this vendor's prequal was re-affirmed. |
| **DBE / certification** | `DBECertStatus` | String | `'Certified'` or `'Not Certified'`. **4 Certified, 4,996 Not Certified** in the first 5000 rows — the exposed set is tiny. |
| | `DBECertEntity` | String | Who certified them — `'DOT'`, `'Migration'`, agency name. |
| | `DBECertDate` | Date | When granted. |
| | `DBECertRemovalDate` | Date | When revoked (null if still certified). |
| | `DBECertNum` | String | External cert registration number. |
| | `PrimaryDbeWbe` | String | `'DBE'`, `'WBE'`, `'DBE/WBE'` or null. |
| | `EthnicGroup` | String (code) | `'BLK'`, `'HISP'`, `'ASIA'`, …; drives federal DBE reporting. |
| | `CertifiedGender` | String | `'Male'`/`'Female'` for the certification record. |
| **Compliance** | `IRSNumber` | String | Federal tax ID. (`'123456789'` on #160 — placeholder) |
| | `SupportServices` | String | DBE support-services declaration. |
| | `PayrollStartDay` | String | Day of week certified payroll weeks begin. |
| | `VendorEstablishedDate` | Date | For prequal history / small-business affidavits. |
| | `RangeAnnualGrossReceipt` | String | Bucket like `'<1M'`, `'1-10M'` — SBA size test. |
| | `RangeAnnualGrossReceipt_Dt` | Date | When the range was last asserted. |
| **Other** | `Website` | String | |
| | `ObsoleteDate` | Date | Soft-delete marker. |
| | `RecordSource` | String | Origin system — `'Migration'`, `'Construction'`, `'Proposal'`. |
| **Agency soft-cols** | `VNCDE1`–`VNCDE4` | String | Reserved coded fields. (`'0000'` placeholders common.) |
| | `VNDT1`–`VNDT6` | Date | Reserved dates. |
| | `VNFLG1`–`VNFLG10` | Bool | Reserved flags. (`VNFLG10='N'` on #160.) |
| | `VNNUM1`–`VNNUM4` | Decimal | Reserved numerics. |
| | `VNLST1`,`VNLST2` | String | Reserved pick-lists. |
| **Audit** | `CreatedDate` / `CreatedBy` / `LastUpdatedDate` / `LastUpdatedBy` | — | Row ownership. |

#### Navigation properties worth knowing

RefVendor has **81** navs. Grouped by what they mean:

**Core execution:**
- `Contractors` → `Contractor[]` — every contract this vendor has participated in (prime or sub). This is the primary reverse-walk to find a vendor's history.
- `Subcontracts` → `Subcontract[]` — every formal sub agreement where this vendor is the subcontractor.
- `SubcontractorPayments` → `SubcontractorPayment[]` — every payment where this vendor is the **payee**. `SUBCONTRACTORPAYMENT1` is the payer-side mirror (yes, dual nav with the "1" suffix).
- `Truckings` → `Trucking[]` — trucking arrangements where this vendor hauls. `TRUCKING1` is the paying-vendor side.

**Procurement side:**
- `Bidders` → `Bidder[]` — every letting this vendor registered to bid on.
- `ProposalVendors` → `ProposalVendor[]` — every bid record (one row per proposal × vendor).
- `BidHistoryProfiles` → `BidHistoryProfile[]` — bid-history profiles aggregated for this vendor.

**Business detail:**
- `RefVendorAddresses` → `RefVendorAddress[]` — one row per mail/physical/billing/… address. (See below.)
- `RefVendorInsurances` → `RefVendorInsurance[]` — insurance policies in force.
- `RefVendorOfficers` → `RefVendorOfficer[]` — company officers / principals.
- `RefVendorWorkClasses` → `RefVendorWorkClass[]` — the work-class codes this vendor is prequalified for, with per-class $ limits.
- `RefVendorNAICSs` / `RefVendorSICCodes` / `RefVendorSpecialtyCodes` — industry classification codes.
- `RefVendorAffiliats` → `RefVendorAffiliat[]` — parent / sister / affiliate companies.
- `RefVendorOfficers` has its own `RefVendorOfficerPNWs` sub-collection for officer personal net-worth records.
- `RefVendorCounties` / `RefVendorDistricts` / `RefVendorRegions` — service-area declarations.

**DBE / compliance:**
- `DbeCommitments` → `DbeCommitment[]` — DBE commitments this vendor is the DBE firm on (across all contracts). Portfolio count: 48.
- `DbeGoodFaithEfforts` → `DbeGoodFaithEffort[]` — good-faith-effort records.
- `ContractApprDbeCommitments`, `ContractCurrDbeCommitments`, `ContractApprDbeCommitSummaries`, `ContractCurrDbeCommitSummaries`, `ContractApprGoodFaithEfforts`, `ContractCurrGoodFaithEfforts` — the frozen-baseline vs revised-current trees. See Part 5.
- `CertifiedPayrolls` → `CertifiedPayroll[]` — payrolls submitted by this vendor (empty on awdemo for most primes; see Part 5 for the Bacco contract 38 example that does populate).
- `RefVendorDbeCertificationEvents` → an event log of DBE certifications gained/lost over time.
- `RefVendorSBPCertifications` / `RefVendorSbpCertificationEvents` — Small Business Program (SBP) parallel to DBE.

**Payroll / employees:**
- `Employers` → `Employer[]` — payroll employer records.
- `VendorAuthorities` → `VendorAuthority[]` — people authorized to sign for the vendor (ties to `UserInfo`).
- `VendorPersonnels`, `VendorEquipments`, `VendorStaffs` → generic agency-defined pools of named personnel / equipment / staff templates that get attached to a Contractor via `ContractVendorEquipments` / `ContractVendorPersonnels` / `ContractVendorStaffs`.

**Role-played-on-a-contract (dual navs with `1`, `2`, `3` suffixes):**
- `Contracts` / `CONTRACT1` / `CONTRACT2` / `CONTRACT3` — four parallel nav collections representing different FK roles (PrimeRefVendorId / OriginalRefVendorId / consultant office / etc.). The vendor row serves whichever role each Contract column calls out. Treat them as "contracts where this vendor is in role N."
- `PROPOSALVENDOR1` / `PROPOSALVENDOR2` — same pattern on the bid side.
- `REFVENDORAFFILIAT1` — the mirror side of the affiliate graph (this vendor as the affiliate rather than the owner).
- `REFVENDORINSURANCE1` — this vendor as the insurance underwriter (vs. `RefVendorInsurances` where this vendor is the insured).

---

### Contractor — the per-contract instance

Think of `Contractor` as a thin association entity: one row = one vendor doing something on one contract. 13 scalar fields, 15 navs. **Not a free-standing concept — exists only as a child of Contract.**

#### Scalar fields

| Field | Type | Meaning (Contractor #521 on contract 282 value) |
|---|---|---|
| `Id` | Int64 | 521 |
| `ContractId` | Int64 | 282 |
| `RefVendorId` | Int64 | 160 (Carl Engineers) |
| `Type` | String | Role on the contract — `'Original Prime'`, `'Subcontractor'`, `'Trucking Firm'`, `'Supplier'`. **This is the categorical column the UI should group on.** |
| `IsOriginalPrime` | Bool | True only for the ORIGINAL prime at award (not a successor). |
| `IsOriginalOrPrime` | Bool | True for original prime OR the current prime (if the contract changed primes). Use this for "is this the prime right now?" (`True` on #521.) |
| `IsSubcontractor` | Bool | True for subs. |
| `EvaluationStatus` | String | Lifecycle of the most recent evaluation — `'None Created'`, `'Draft'`, `'Final - Approved'`, `'Approved'`. |
| `Evaluations` | Int32 | Count of evaluation records on this Contractor. |
| `CreatedDate`/`CreatedBy`/`LastUpdatedDate`/`LastUpdatedBy` | — | Audit. |

**Observed Type values on contract 282:** `Original Prime` (Carl Engineers), `Subcontractor` (Smith Bros., Zwollie). On contract 38: `Original Prime` (Bacco), `Subcontractor` (Perez, Rodriguez, City Steel, Klett, West Side Concrete, Barthel), `Trucking Firm` (Balkema). The code list is open — do not rely on a fixed enum.

#### Nav properties

- **Back-refs:** `Contract`, `RefVendor` (ref navs; always use `$expand=RefVendor` when loading a contractor list — gives you the LongName in one query).
- **Field data:** `DWRContractors` → `DWRContractor[]` — one row per DWR this contractor was on-site for. Primary join into the labor flow (Part 3).
- **Agency templates attached to this contract:** `ContractVendorEquipments`, `ContractVendorPersonnels`, `ContractVendorStaffs` — the subset of the parent RefVendor's equipment/personnel/staff pools that got activated on this contract.
- **Force-account:** `ForceAccountContractors` → `ForceAccountContractor[]` — see Part 3.
- **Compliance records keyed on the contractor:** `ContractorEvalutions` [sic], `LavorComplianceReview` [sic — `LaborComplianceReview`], `EEOComplianceReviews`, `ComplianceFindings`, `FieldInterviews`, `PayrollManagementCompliances`, `TieredContractorCertifiedPayrolls`. **This is the gotcha the Contract chapter flagged:** evaluations and reviews are keyed on `ContractorId`, not `ContractId`. To find them for a contract, you must first list the contract's Contractors, then filter the review tables on the resulting ids.
- **Change orders:** `ChangeOrderNewItems` → `ChangeOrderNewItem[]` — new items a CO added that get assigned to this contractor (so the agency knows who installed what).

#### Live sample — all contractors on contract 282

```
#521 RefVendor#160 Carl Engineers Inc. (CNST, DBE=Not Certified)   Type=Original Prime  Prime=True  Eval=Final - Approved
#522 RefVendor#206 Smith Bros. Contracting, Inc. (CNST, Not Cert.) Type=Subcontractor   Prime=False Eval=None Created
#523 RefVendor#646 Zwollie Inc. (NONE, Not Cert.)                  Type=Subcontractor   Prime=False Eval=None Created
```

#### Live sample — contract 38 (Bacco Construction, the DBE example)

```
#83  RefVendor#125 Bacco Construction Company       Type=Original Prime
#84  RefVendor#543 Perez Construction, Inc.         Type=Subcontractor   DBE=Certified
#85  RefVendor#758 Rodriguez Construction Corp.     Type=Subcontractor   DBE=Certified
#86  RefVendor#8688 City Steel, Inc.                Type=Subcontractor   DBE=Certified
#87  RefVendor#161 Klett Construction Company       Type=Subcontractor
#88  RefVendor#337 West Side Concrete Company       Type=Subcontractor
#106 RefVendor#126 Balkema, Inc.                    Type=Trucking Firm   DBE=Certified
#248 RefVendor#129 Barthel Contracting Company      Type=Subcontractor
```

---

### Subcontract — the formal sub agreement

Where the Prime formally delegates work to another vendor. The agreement is what the agency approves; the per-day execution shows up in DWRContractor + DWRItemPosting. 84 scalar fields, 10 navs. **110 rows** across the lab. On contract 38 Bacco: **6 subs totalling $7.4M committed.**

#### Scalar fields grouped

| Group | Field | Type | Meaning |
|---|---|---|---|
| **Identity** | `Id` | Int64 (key) | |
| | `ContractId` | Int64 | Parent contract. |
| | `SubcontractNumber` | String | Human sequence — `'1'`, `'2'`, `'3'`. |
| | `RefVendorId` | Int64 | The subcontractor. |
| | `ParentSubcontractId` | Int64 | For nested / tiered subs (sub-of-a-sub). Self-ref. |
| **Classification** | `SubcontractType` | String (code) | Scope code — on awdemo observed: `'A'`, `'C'`, `'E'`, `'M'`, `'CONC'`, `'DRIL'`, `'AGG'`, `'L'`, `'TC'`, `'P'`, `'FE'`, `'SIGN'`, `'CS'`, `'SOIL'`, `'ELEC'`, `'SUB'`, `'TEST'`, `'CG'`, `'GEOTECH'`, `'AEConsultantSub'`, `'PLUM'`. Agency-defined. |
| | `Supplier` | Bool | True if this is a supplier agreement (no on-site work). 1 row. |
| | `Trucker` | Bool | True if this is a trucking agreement. 6 rows. |
| | `Broker` | Bool | True if this is a broker. 2 rows. |
| | `DbeCertified` | Bool | True if the sub is DBE certified. **18 of 110 subs.** |
| | `DbeCommitmentFlag` | Bool | True if the agency is counting this sub toward DBE goal attainment. |
| **$ (totals)** | `CalcTotalItemsTotal` | Decimal | Sum of the sub's SubcontractItem.PrimeExtendedAmount. |
| | `CalcTotalSubcontractAmount` | Decimal | Sub's total commitment (prime perspective). (**$372k on sub 47 Perez.**) |
| | `CalcTotalSubExtendedAmount` | Decimal | Sum of SubcontractItem.SubExtendedAmount (sub's own cost perspective). |
| | `SubcontractToDBEFirms` | Decimal | $ this sub is further subcontracting to DBE firms. |
| | `SubcontractToNonDBEFirms` | Decimal | Mirror for non-DBE. |
| | `SupplierAmount`/`TruckerAmount`/`BrokerAmount` | Decimal | Breakdown of the three fulfilment modes. |
| | `TotalNumberOfTrucksSubcontracted` | Int | For trucking agreements. |
| | `CalcSpecialtySubcontractedAmount` / `CalcSpecialtySubcontractedPercent` | Decimal | Specialty-work carve-out. |
| | `CalcTowardsAmountThreshold` / `CalcTowardsPercentThreshold` | Decimal | Values rolled into the DBE / state-threshold compliance math. |
| **Lifecycle** | `ConsentDate` | Date | Agency's consent-to-sublet date. (`'2014-06-02'` on sub 47.) |
| | `ReadyForReviewDate` | Date | When the prime marked the sub ready for agency review. |
| | `InactiveDate` | Date | Terminated. |
| | `Comments` | String | Free-text. |
| | `UseApprovedVendorWorkClasses` | Bool | Whether to validate items against the sub's prequalified work classes. |
| | `ExcludeFromThresholdCalcs` | Bool | Opt-out from DBE math. |
| | `RecordSource` | String | `'Construction'` (manually added), `'Proposal'` (from bid), `'Migration'`. |
| **Audit** | `CreatedDate`/`CreatedBy`/`LastUpdatedDate`/`LastUpdatedBy` | — | |
| **Legacy soft-cols** | `SC*` — `SCACTAMT`, `SCACTSUB`, `SCAMOUNT`, `SCSTAT`, `SCDWBEFL`, `SCSUBBED`, `SCPCT`, `SCSPCAMT`, `SCWKUNCM`, `PRIMEFLG`, `ONJOBFLG` | — | Trns·port carry-over; agency-mapped. |
| | `GENDATE01`–`GENDATE08`, `GENFLAG01`–`GENFLAG07`, `GENNUM01`–`GENNUM05`, `GENTEXT01`–`GENTEXT17` | — | Agency-configurable fields. |

#### Nav properties

- `Contract` (ref) / `RefVendor` (ref) — primary joins.
- `ParentSubcontract` + `Subcontracts` — tiered-sub tree.
- `SubcontractItems` → `SubcontractItem[]` — line-by-line what the sub is doing. 231 rows total. Each row links to a `ContractItem` + `Quantity` + `PrimeUnitPrice` + `SubUnitPrice`.
- `Truckings` → `Trucking[]` — trucking sub-details (truck count, long-term-lease flag, lease-from-non-DBE flag). 10 rows total.
- `WorkClassifications` → `WorkClassification[]` — which named work classes this sub covers. 115 rows total.
- `ContractActions`, `ContractClaims`, `ContractorEvaluations` — paper trail that may be scoped to the sub (not the whole contract).

#### Live sample — contract 38 subs

```
Sub#47  seq=1 Perez Construction (DBE)      type=A    commit=$372,000    items=2
Sub#48  seq=2 Rodriguez Construction (DBE)  type=P    commit=$5,005,500  items=2
Sub#49  seq=3 City Steel (DBE)              type=FE   commit=$321,000    items=2
Sub#50  seq=4 Klett Construction            type=CONC commit=$1,080,000  items=3
Sub#51  seq=5 West Side Concrete            type=C    commit=$480,000    items=2
Sub#101 seq=6 Barthel Contracting           type=A    commit=$150,000    items=1
```

---

### Surety ecosystem

**There is no `SuretyCompany` or `SuretyAgent` entity.** Sureties and surety agents are just `RefVendor` rows that happen to be referenced by role-specific FKs on `Contract` and `ProposalVendor`.

#### At the executed-contract level

Two columns on `Contract`:
- `Contract.SuretyCompanyId` → `RefVendor.Id` (the bonding company / underwriter)
- `Contract.SuretyAgentId` → `RefVendor.Id` (the agent of record)

Live sample — contract 282:
```
SuretyCompanyId: 122  → "Aaaaaaffidavit" (VendorType='C+O')
SuretyAgentId:   142  → "Dunigan Bros, Inc." (VendorType='CNST')
```

Across the awdemo portfolio: **8 distinct surety companies** bonded **11 contracts** (so 136 contracts have no surety on file — the field is nullable). Top sureties: Bacco Construction (2), Travelers Casualty & Surety (2), Aaaaaaffidavit (2).

#### At the proposal / bid-bond level

On `ProposalVendor` (see Part 2 for the full Proposal flow):
- `ProposalVendor.SuretyCompanyId` → `RefVendor.Id` — surety on the bid bond.
- `ProposalVendor.SuretyAgentId` → `RefVendor.Id` — agent on the bid bond.

**Reverse walk — "what contracts is this surety on the hook for?"**
```
GET /Contracts?$filter=SuretyCompanyId eq 122
    &$select=Id,Name,ContractStatus,AwardedContractAmount,AmountPaidToDate
```
Returns the 2 contracts bonded by vendor #122. If you want $ exposure totals, sum `AwardedContractAmount − AmountPaidToDate` across the result.

#### What's missing

No separate `SuretyBond` entity in awdemo (schema would have been expected to hold bond number, bond percent, bond date, bond type). Those fields live on `Proposal.BIDBOND` (soft field) and are inferable from `ContractInsurance` tied to insurance records.

---

### Vendor sub-entities

#### `RefVendorAddress` — 42 fields, 9,671 rows portfolio-wide

One row per address a vendor has registered. **Not everything is populated.** On #160 Carl Engineers, one `MAIL` address: `P O Box 1406, 5425 Brooklyn Road, Jackson, MI 49204`.

Key fields: `Id, RefVendorId, Name, AddressType ('MAIL' | 'PHYS' | 'BILL' | …), Line1..Line4, City, State, Zipcode, Country, Email, Latitude, Longitude, SalesTax, RefCountyId, RefDistrictId, DunsNumber`. The DUNS number lives here, not on RefVendor directly. `RefVendorPhones` is a child collection of this entity (not of RefVendor).

Collection navs include `ContractConsultantOfficeLocations` (contracts where this specific address is the consultant office of record) and `Purchases` + `PURCHASE1`.

#### `RefVendorInsurance` — 29 fields, 15,667 rows portfolio-wide

Insurance policies on file for the vendor. One row per policy. Fields: `Id, RefVendorId, InsuranceSequenceNumber, InsuranceType ('GL' | 'WC' | 'AUTO' | …), InsuranceRefVendorId (the underwriter — another RefVendor), InsuranceStatus ('Active' | …), PolicyNumber, InsuranceBeginDate, ExpirationDate, Agent, PhoneNumber, Comment, ProposalId (if tied to a specific bid)`. Live on #160: policy #6359633217889, GL, Active, began 2024-08-01, no expiration recorded. The link into contracts is `ContractInsurance` which pairs a `ContractId` with a `RefVendorInsuranceId`.

#### `RefVendorOfficer` — 37 fields, 8,776 rows portfolio-wide

Company officers and principals. Fields: `Id, RefVendorId, Name, OfficerTitle, RefVendorAddressId, Gender, PercentOwnership, PhoneNumber, CitizenshipStatus, EthnicGroup, Comments, Ssn, PrimaryTitle, EffectiveDate, ExpirationDate`. Each officer can have a `RefVendorOfficerPNWs` collection (personal net worth statements — DBE affidavit material). Live on #160: one officer named `C. Donavon Carl` marked `PrimaryTitle: True`.

#### `RefVendorWorkClass` — 12 fields, **7,035 rows** portfolio-wide

Vendor's prequalified work-class scopes with per-class $ limits. **This is the vendor-level prequalification table** the Procurement chapter noted was split across 8 discipline-specific tables — those are specialized (TestingQualification, SamplingQualification, WelderQualification, etc.) while this one is the general work-class ledger. Fields: `Id, RefVendorId, Name, QualificationAmount, RecordSource`. Live: vendor 8405 has work class `'Ea'` and `'N93A'` both at $152,523.40.

#### `RefVendorNAICSs`, `RefVendorSICCodes`, `RefVendorSpecialtyCodes`, `RefVendorAdditionalType`

Industry classification. **All sparse on awdemo** — 5, 8, and (specialty) few rows total. Fields are `Id, RefVendorId, NAICSId / SICCode / SpecialtyCode / Name, EffectiveDate, Status, StatusChangeDate, Remarks`.

#### `RefVendorCounties`, `RefVendorDistricts`, `RefVendorRegions`

Service-area declarations. Each links `RefVendorId` to a `RefCountyId` / `RefDistrictId` / `RefRegionId` with `EffectiveDate` + `InactiveDate`. All empty on #160 but populated for other vendors.

#### `RefVendorAffiliat` — 15 fields

Vendor-to-vendor affiliate graph. `RefVendorId` + `AffiliateRefVendorId` + `VendorRelation` + `PercentOwnership` + `EffectiveDate` + `EndDate`. The mirror nav from the affiliate side is `REFVENDORAFFILIAT1`.

#### `RefVendorAnnualData` — 19 fields, 13 rows portfolio-wide

Annual size / employment snapshots. Fields: `RefVendorId, Year, SubmittalType, SubmittalDate, AnnualAffidavitDate, GrossReceipts, NumOfFullTimeEmps, NumOfPartTimeEmps, ProfServStaffInState, ProfServStaffOutState, TotNumOfEmps, TotNumOfProfServStaff, RunningAverage, Remarks`. The DBE small-business size test lives here.

#### `RefVendorSBPCertifications` + `RefVendorSbpCertificationEvents`

Small Business Program (SBP) parallel to DBE. Fields on the certification: `SBPCertification, SBPCertEntity, SBPCertDate, SBPCertRemovalDate, SBPCertNum`.

#### `RefVendorDbeCertificationEvent` — 10 fields

Event log of DBE certification changes. Fields: `RefVendorId, RefActionTypeId, EventDate, AssignedTo, Comments`. Live for Perez Construction (#543): 2 events.

#### `RefVendorOjtGoal` — 11 fields

Vendor's annual On-the-Job-Training commitments. Fields: `RefVendorId, StartDate, EndDate, OjtGoal, OjtGoalUnits, OjtGoalComments`. The OJT execution lives in `OjtContractAssignment` etc. — see Part 5.

#### `RefVendorAgencyView` — 11 fields

Lets different agencies see vendor records with different visibility rules. `AgencyViewId` + `EffectiveDate` + `ExpirationDate` + `Active` + `Status`.

#### `VendorAuthority` — 10 fields

Who at the vendor is authorized to sign for them. Links `RefVendorId` to `UserInfoId`, with `AuthorizedToSign` bool, `Title`, `InactiveDate`.

#### `VendorPersonnel` / `VendorEquipment` / `VendorStaff` — the agency templates

These are generic agency pools **(50 / 99 / 29 rows total)** of named people, machines, or staff templates. They don't belong to a contract directly — they belong to a `RefVendor`. When they're actually in use on a contract, you'll find them joined via `ContractVendorPersonnels` / `ContractVendorEquipments` / `ContractVendorStaffs` keyed on `ContractorId`. The DWR per-day usage is `DWRContractVendorEquipments` / `DWRContractorPersonnels` / `DWRContractorStaffs`. Live on vendor 160: 3 VendorPersonnels, 3 VendorEquipments, 2 VendorStaffs.

#### What `VendorMaterial`, `VendorCertification`, `VendorContact` would be if they existed

Trick section — **none of those three entity names exist in awdemo**. The vendor-reference-guide (`refs/reference-ams-guide-v2-2026-09-30.md`) mentions them, but they are not implemented in this instance. Material-approvals for a vendor flow through `Source` + `SourceManagementLevel`, certifications flow through `RefVendorSBPCertifications` + `RefVendorDbeCertificationEvents` + `VendorAuthority` + the discipline-specific `TestingQualification`/`SamplingQualification`/`WelderQualification`/`StormwaterInspectorQualification` on the person side, and vendor-level contacts flow through `RefVendorOfficer` + `RefVendorAddress.Email` + `RefVendorPhone`.

---

### Vendor evaluations

#### `ContractorEvaluation` — 21 fields, 20 rows portfolio-wide

Formal performance review of a Contractor. **Keyed on `ContractorId`, not `ContractId`** — this is the gotcha the Contract reference flagged. To find evaluations for a contract, first list the contract's Contractors, then filter `ContractorEvaluations?$filter=ContractorId in (…)`.

Fields: `Id, EvaluationType ('Interim' | 'Final'), ContractorId, SubcontractId (optional — eval might be scoped to a sub), StartingDate, EndingDate, EvaluationDate, Status ('Draft' | 'Approved'), ApprovedById → PersonInfo, ApprovedDate, EvaluatedById → PersonInfo, OverallRating (Decimal, 0–10), Comments, RevisionNumber, EvaluationNumber, WorkType (String code), RefContractorEvaluationId`.

Live on contract 282 Contractor #521 (Carl Engineers): **Final rating = 10.0**, approved 2024-09-10. Range across the lab's 20 evaluations: 1.5 (The Millgard Corporation on `work=L`) up through 10.0.

#### `ContractorEvaluationGroup`

Sub-collection of ContractorEvaluation — the component ratings that roll up into `OverallRating`. Live for eval #21: 4 groups each contributing a `GroupRating`, pointing at a `RefContractorEvaluationGroupId` for the rubric. Count-weighted average becomes the overall.

#### `RefContractorEvaluation` — the rubric catalog

Only **3 rubric templates** on awdemo: `Test` (`MinRating: 10.0`), `Contractor_Eval_1` (`MinRating: 8.0`, with instructions text), `Consultant Evaluation` (`MinRating: 6.0`). Each has its own `RefContractorEvaluationGroup` sub-structure (not probed in detail — see EDMX). Think of this as the agency-configurable scorecard definition.

---

### Vendor-level DBE / prequalification

Scattered across many entities, intentionally — this is the regulatory layer and it has shape.

**On the master record:** `RefVendor.DBECertStatus` + `DBECertEntity` + `DBECertDate` + `DBECertRemovalDate` + `DBECertNum` + `PrimaryDbeWbe` + `EthnicGroup` + `CertifiedGender`.

**Event log:** `RefVendorDbeCertificationEvents` — one row per state change (gained, lost, renewed).

**Prequalification bucket:** `RefVendor.CertificationType` ∈ {`NONE`, `PREQ`, `CERT`, `P+C`}. Portfolio: 3,206 NONE, 1,381 None, 284 PREQ, 106 CERT, 23 P+C.

**Capacity math:** `RefVendor.MaximumCapacity` + `UncompletedWork` + `AdjustedNetWorth` + `AbilityFactor` + the per-class limits in `RefVendorWorkClass.QualificationAmount`. Remaining capacity ≈ Max − Uncompleted; per-class remaining ≈ WorkClass.QualificationAmount − sum of in-flight contract $ in that class.

**Portfolio stat:** Only **5 vendors** show `DBECertStatus = 'Certified'` on awdemo (Balkema, DeAngelis Landscape, Perez, Rodriguez, City Steel). The lab's DBE story is tiny; the Procurement + Compliance chapters probe deeper via `ContractApprDbeCommitments`.

**Small Business Program:** `RefVendorSBPCertifications` (14 rows portfolio-wide) + event log `RefVendorSbpCertificationEvents`.

---

### Loading a vendor efficiently

All times measured on awdemo over the public internet (cold cache). Local FastAPI with 60s `AsyncTTLCache` returns < 2 ms warm. All queries verified live on 2026-09-30.

#### Recipe 1 — Minimum vendor card (dropdown / autocomplete)

```
GET /RefVendors
    ?$select=Id,Name,LongName,ShortName,VendorType,DBECertStatus
    &$filter=startswith(tolower(LongName),'car')
    &$orderby=LongName
    &$top=20
```

~110 ms. Return `{Id, Name, LongName, VendorType, DBECertStatus}` as the autocomplete row. **Backend gap:** our `api/routes/vendors.py` does not yet implement vendor search; add a `GET /api/vendors/search?q=` route.

#### Recipe 2 — Vendor profile page (header + address + insurance + officers)

**Current:** `GET /api/vendors/{id}` returns `{vendor, contracts_as_prime}`. Two parallel awdemo calls, ~200 ms cold.

**Sharpened recipe (fan-out, 5 parallel awdemo calls, ~250 ms cold):**

```python
asyncio.gather(
    client.get("RefVendors", filter=f"Id eq {vid}", top=1),
    client.get("RefVendorAddresses",   filter=f"RefVendorId eq {vid}",
               select="Id,Name,AddressType,Line1,Line2,City,State,Zipcode,Country,Email,RefCountyId,RefDistrictId",
               top=20),
    client.get("RefVendorInsurances",  filter=f"RefVendorId eq {vid}",
               select="Id,InsuranceSequenceNumber,InsuranceType,InsuranceStatus,PolicyNumber,InsuranceBeginDate,ExpirationDate,Agent,PhoneNumber,InsuranceRefVendorId",
               orderby="ExpirationDate desc", top=50),
    client.get("RefVendorOfficers",    filter=f"RefVendorId eq {vid}",
               select="Id,Name,OfficerTitle,PrimaryTitle,PercentOwnership,PhoneNumber,CitizenshipStatus,EthnicGroup,EffectiveDate,ExpirationDate",
               orderby="PrimaryTitle desc", top=50),
    client.get("RefVendorWorkClasses", filter=f"RefVendorId eq {vid}",
               select="Id,Name,QualificationAmount", top=100),
)
```

Then merge into a single `{vendor, addresses, insurances, officers, work_classes}` response. The frontend renders a 4-section stack: identity + address card at top, insurance table (expiration-colored), officers table, work-class pills with $ limits.

#### Recipe 3 — Vendor's contracts-as-PRIME (reverse walk)

**Current:** second half of `/api/vendors/{id}` does this.

```
GET /Contracts
    ?$filter=PrimeRefVendorId eq {vid}
    &$select=Id,Name,ContractStatus,AwardedContractAmount,AmountPaidToDate,PercentPaid,CreatedDate
    &$orderby=Id desc
    &$top=500
```

~90 ms on #160 (1 result). Full portfolio scan with no filter: ~130 ms (147 rows). Backend caches at `vendor:{id}` for 60 s.

#### Recipe 4 — Vendor's contracts-as-SUB (through Subcontract)

**Not currently implemented.** Three-step chain:

```
GET /Subcontracts
    ?$filter=RefVendorId eq {vid}
    &$select=Id,ContractId,SubcontractNumber,SubcontractType,DbeCertified,CalcTotalSubcontractAmount,ConsentDate
    &$orderby=ConsentDate desc
    &$top=200
```

Then collect distinct `ContractId` values and:

```
GET /Contracts
    ?$filter=Id in (c1,c2,c3,…)
    &$select=Id,Name,ContractStatus,AwardedContractAmount,PercentPaid
    &$top=200
```

Add a `GET /api/vendors/{id}/subcontracts` route that fans these out in parallel. ~200 ms cold total.

#### Recipe 5 — Vendor's crew footprint across contracts (Contractor → DWRContractor)

**Not currently implemented.** For a given RefVendor, aggregate hours they've been on-site across every contract they've touched.

```python
# 1. Find every Contractor row for this vendor
contractors = client.get("Contractors",
    filter=f"RefVendorId eq {vid}",
    select="Id,ContractId,Type,IsOriginalOrPrime",
    top=500)
# 2. Aggregate per-DWR hours per Contractor (chunked by 50 ids)
#    DWRContractor has Hours, IsPrime, HasEquipment/Personnel/Staff
hours_rows = []
for chunk in chunked([c["Id"] for c in contractors], 50):
    ids = ",".join(str(x) for x in chunk)
    hours_rows += client.get("DWRContractors",
        filter=f"ContractorId in ({ids})",
        select="Id,ContractorId,DailyWorkReportId,Hours,IsPrime",
        top=5000)
# 3. Group hours by ContractId
```

~400 ms cold for a moderately-active vendor (3 contracts × 10–20 DWRs). Cache 5 min; this is a dashboard query, not a per-page load.

#### Recipe 6 — Vendor's $-paid-to-date aggregate (payee side)

**Not currently implemented.** SubcontractorPayments is the sub-payment ledger (33 rows total on awdemo).

```
GET /SubcontractorPayments
    ?$filter=PayeeId eq {vid}
    &$select=Id,ContractPaymentId,PayerId,PaidAmount,DbeFirm,PaidDate,PaymentType
    &$orderby=PaidDate desc
    &$top=500
```

~110 ms. Sum `PaidAmount` for total. For primes, cross-reference `PaymentEstimateItem.TotalPaidAmount` scoped to Contracts where this vendor is prime (fan-out through contracts-as-prime). The "payer vs payee" distinction is important: a prime's "paid out to subs" sum is `SubcontractorPayments?$filter=PayerId eq {vid}`; a sub's "received" sum is the `PayeeId eq {vid}` version.

Live on Bacco (#125) as payer across all 33 payments: $195,484 to City Steel, $136,300 to Perez (DBE sub), $112,346 to Cadillac Asphalt, $42,200 to Rodriguez (DBE sub), $22,879 to J. Rance Construction, $8,400 to Balkema (DBE), $3,150 to Barthel, $500 to John M. Jacobs Plumbing. DBE total: **$186,900** against $1,775,000 committed = **10.5% utilization.**

#### Recipe 7 — Vendor's compliance posture (payrolls + evaluations)

**Not currently implemented** at the aggregate level, but Part 5 covers the per-contract compliance passport.

```python
asyncio.gather(
    client.get("CertifiedPayrolls",
        filter=f"ContractorRefVendorId eq {vid}",  # or query via Contractor join
        select="Id,ContractId,WeekEndingDate,PayrollNumber,IsFinal,AmendmentNumber",
        orderby="WeekEndingDate desc",
        top=200),
    # Evaluations keyed on Contractor; two-step
    client.get("Contractors",
        filter=f"RefVendorId eq {vid}",
        select="Id,ContractId",
        top=500),
)
# Then: ContractorEvaluations?$filter=ContractorId in (…)
```

Return `{payrolls, evaluations}` with aggregate stats: latest payroll date (overdue if > 7 days old), avg rating, exceptions count. On awdemo most of CertifiedPayroll is empty for most vendors — Bacco on contract 38 is the exception.

#### Recipe 8 — Surety's active-bond exposure

```
GET /Contracts
    ?$filter=SuretyCompanyId eq {vid} and ContractStatus eq 'Active'
    &$select=Id,Name,AwardedContractAmount,CurrentContractAmount,AmountPaidToDate,PercentPaid
    &$top=500
```

~90 ms. Expose as `GET /api/vendors/{id}/surety-exposure`. On the frontend: total $ outstanding = sum(CurrentContractAmount − AmountPaidToDate). Live: Aaaaaaffidavit (vendor 122) bonds 2 contracts totalling $1.23M in current obligation, $1.15M paid, **$81K outstanding**.

#### Anti-pattern: deep `$expand` from RefVendor outward

```
# Don't do this
GET /RefVendors
    ?$filter=Id eq 160
    &$expand=Subcontracts($expand=SubcontractItems),
             SubcontractorPayments,
             ContractApprDbeCommitments
```

Measured 338 ms on #160 (which has thin data). Vendors with heavy sub history time out on this shape. **Fan out with `asyncio.gather` instead.** The one-expand pattern is fine for small 1:few navs (`RefVendorAddresses($top=5)`, `RefVendorOfficers($top=10,$filter=PrimaryTitle eq true)`), not for 1:many execution navs.

---

### UI query recipes

Dashboard-ready OData queries. Response-shape column shows what to render, not internal field names. Perf is awdemo cold-cache round-trip.

#### R1 — Vendor leaderboard: top primes by $-earned-this-FY

```
GET /Contracts
    ?$select=Id,PrimeRefVendorId,AmountPaidToDate,CreatedDate
    &$filter=year(CreatedDate) eq 2024
    &$top=500
```

~130 ms. Client-side: group by `PrimeRefVendorId`, sum `AmountPaidToDate`, sort desc, join to RefVendor LongName via a second query:
```
GET /RefVendors?$filter=Id in (top10_ids)&$select=Id,LongName
```
**Shape:** `[{vendor_id, long_name, contracts_count, paid_to_date}]`. **UI:** sortable table with sparkline column for paid-over-time.

#### R2 — DBE utilization leaderboard (across the portfolio)

Two-step aggregation across all SubcontractorPayments:
```
GET /SubcontractorPayments?$select=PayeeId,PaidAmount,DbeFirm&$top=5000
# client-side: group by PayeeId where DbeFirm=true, sum PaidAmount
GET /RefVendors?$filter=Id in (payee_ids) and DBECertStatus eq 'Certified'
    &$select=Id,LongName,EthnicGroup,CertifiedGender,DBECertDate
```
**Shape:** `[{dbe_vendor_id, long_name, ethnic_group, dbe_cert_date, total_paid, contracts_touched}]` sorted desc. **UI:** bar chart with ethnic_group color-encoding; a `contracts_touched` chip beside each bar; filter chips for ethnic group + certified gender. **Perf:** both queries ~110 ms each; cache 5 min.

#### R3 — Vendors with expiring certifications feed

Three sources merged (prequal / insurance / DBE / SBP cert):
```
GET /RefVendors?$filter=PrequalExpDate ge 2026-09-30 and PrequalExpDate le 2026-12-31
    &$select=Id,LongName,PrequalExpDate&$orderby=PrequalExpDate asc&$top=100
GET /RefVendorInsurances?$filter=ExpirationDate ge 2026-09-30 and ExpirationDate le 2026-12-31
    &$select=Id,RefVendorId,InsuranceType,PolicyNumber,ExpirationDate&$orderby=ExpirationDate asc&$top=200
GET /RefVendorSBPCertifications?$filter=SBPCertRemovalDate ne null and SBPCertRemovalDate ge 2026-09-30
    &$select=Id,RefVendorId,SBPCertEntity,SBPCertRemovalDate&$top=200
```
Merge client-side; emit a unified "expiring in 30/60/90 days" badge color. **UI:** a stream feed with vendor name + what's expiring + days-until. **Perf:** 3 parallel calls, ~250 ms total cold.

#### R4 — Payrolls overdue by vendor (exception feed)

```
GET /CertifiedPayrolls?$apply=groupby((ContractorRefVendorId),aggregate(WeekEndingDate with max as last_week))
```
(If `$apply` isn't honored by this OData version, fall back: paginate `CertifiedPayrolls?$select=ContractorRefVendorId,WeekEndingDate&$top=5000` and reduce client-side.) Then compute `days_since_last = today - last_week`; keep rows where it exceeds 14. **UI:** red/amber/green row per vendor; link to CertifiedPayroll detail.

#### R5 — Surety exposure by surety company

```
GET /Contracts?$filter=SuretyCompanyId ne null and ContractStatus eq 'Active'
    &$select=Id,Name,SuretyCompanyId,CurrentContractAmount,AmountPaidToDate&$top=500
```
Group by `SuretyCompanyId`, sum `CurrentContractAmount − AmountPaidToDate`. Join to RefVendor for name. **UI:** horizontal bar chart with surety name on the y-axis, outstanding $ on the x. Live: 8 sureties on 11 contracts total; biggest exposures are 2-contract sureties with cumulative awards ~$2M.

#### R6 — Vendor directory with filters

```
GET /RefVendors?$select=Id,Name,LongName,VendorType,CorporationType,DBECertStatus,PrequalExpDate
    &$filter=VendorType eq 'CNST' and DBECertStatus eq 'Certified'
    &$orderby=LongName&$top=100
```
**Shape:** paginated table rows. **UI:** faceted-search layout with VendorType (CNST / ENG / SRVC / …) and DBECertStatus facets as sidebar chips. **Perf:** ~130 ms; cache the facet counts at 5 min.

#### R7 — Prime-vs-sub mix for a single vendor (donut)

```
GET /Contractors?$filter=RefVendorId eq {vid}
    &$select=Id,ContractId,Type,IsOriginalOrPrime&$top=500
```
Group by `IsOriginalOrPrime` into prime vs sub counts. **UI:** small donut on the vendor profile card. **Perf:** ~90 ms.

#### R8 — "Who is this subcontractor also subbing to right now?"

```
GET /Subcontracts?$filter=RefVendorId eq {sub_vid} and InactiveDate eq null
    &$expand=Contract($select=Id,Name,PrimeRefVendorId)
    &$select=Id,ContractId,SubcontractNumber,CalcTotalSubcontractAmount,ConsentDate,DbeCertified
    &$top=50
```
Group by `Contract.PrimeRefVendorId` → "subbing for Bacco on 1 contract, Spartan on 1 contract." **UI:** on the DBE sub's profile, a "currently working under" strip. Use for conflict-of-interest / capacity visibility.

#### R9 — Contractor-evaluation leaderboard (performance ranking)

```
GET /ContractorEvaluations?$filter=Status eq 'Approved' and EvaluationType eq 'Final'
    &$select=Id,ContractorId,OverallRating,EvaluationDate,WorkType,Comments
    &$orderby=EvaluationDate desc&$top=200
```
Join to Contractors → RefVendors (two-step). Average `OverallRating` per vendor over last N years. **Shape:** `[{vendor_id, long_name, avg_rating, n_evals, latest_date}]`. **UI:** sortable table; also a scatter of avg_rating vs n_evals showing the "trusted and busy" quadrant. Live range: 1.5 (Millgard) to 10.0 (Carl Engineers, Klett).

#### R10 — Trucking firm roster for a contract

```
GET /Contractors?$filter=ContractId eq {cid} and Type eq 'Trucking Firm'
    &$expand=RefVendor($select=Id,LongName)
    &$select=Id,RefVendorId&$top=50
GET /Truckings?$filter=SubcontractId in (sub_ids_from_this_contract)
    &$select=Id,SubcontractId,RefVendorId,LongTermLease,LeaseFromNonDBE,TotalNumberOfTrucks,FirmType&$top=50
```
Merge: "Firm X: 4 trucks, long-term-lease=true, not DBE." **UI:** truck-count badge table on a Compliance / DBE Trucking tab.

#### R11 — Vendor office locations map

```
GET /RefVendorAddresses?$filter=Latitude ne null and Longitude ne null
    and AddressType eq 'MAIL'
    &$select=Id,RefVendorId,City,State,Latitude,Longitude&$top=5000
```
Group by (lat, lng) → marker clusters. **UI:** map with pins; click a cluster → vendor-list sidebar. Awdemo coverage: most addresses have no coords, so filter is important.

#### R12 — Vendor affiliate / parent-child graph

```
GET /RefVendorAffiliats?$filter=RefVendorId eq {vid} or AffiliateRefVendorId eq {vid}
    &$select=Id,RefVendorId,AffiliateRefVendorId,VendorRelation,PercentOwnership,EffectiveDate,EndDate
```
Combine with a second query hydrating LongNames for both sides. **UI:** force-directed graph or a two-column "owns / owned-by" list on the vendor profile. Useful for DBE affiliation / size-standard aggregation.

---

### How to display vendors

**Directory layout:** We currently expose `/vendors` as a `contracts_count`-sorted leaderboard of primes (44 rows on awdemo). **Keep this as the default view** — it's the right opening because 90% of UI traffic to the vendor tab is "find me a prime." Add two toggles: **All vendors** (9,131 rows — needs pagination + facets as per R6) and **DBE directory** (filtered to `DBECertStatus = 'Certified'` with ethnic-group chips as per R2). Each row renders: LongName (link), Name (mono, as the business ID), VendorType chip, DBE/UDBE/SBP badges, contracts-count (right-aligned mono), latest-paid $ (right-aligned mono).

**Profile page layout:** Our current `/vendors/:id` is minimal (`{vendor, contracts_as_prime}`). **Expand it** to use Recipe 2's fan-out and these sections:
1. **Header** — LongName (serif large), VendorType pill, DBE/SBP badges, prequalification remaining capacity ("$X.X M remaining of $Y.Y M").
2. **Hero numbers (5)** — Contracts-as-prime count · Total $ paid to date across all contracts · Contracts-as-sub count · Latest evaluation rating (0–10) · Prequal expires in N days (color-coded).
3. **Identity card** — Mail/physical addresses from `RefVendorAddresses`, IRS#, corp type, state, website.
4. **Officers table** — `RefVendorOfficers` sorted by `PrimaryTitle` then `PercentOwnership`.
5. **Insurance table** — `RefVendorInsurances` sorted by `ExpirationDate` desc; red/amber/green badge per row.
6. **Work classes** — chip row of `RefVendorWorkClass.Name` with the `QualificationAmount` as a secondary number.
7. **Contracts as prime** — table (current) → **sharpen to use Recipe 3's select set and add a "status pill" column.**
8. **Contracts as sub** (new, Recipe 4) — second table under the primes table, grouped by prime-they're-subbing-for.
9. **Evaluations** (new, Recipe 9) — latest-rating stat tile + a small histogram of ratings over time; link to the full evaluations list.
10. **DBE panel** (if DBE Certified) — Recipe 2's DBE fields; event-log from `RefVendorDbeCertificationEvents`.

**Visualizations that pay off:**
- **Contract portfolio over time** — small timeline (`CreatedDate` horizontal axis, bar height = `AwardedContractAmount`, color = ContractStatus). Answers "has this vendor been growing or shrinking their book of work?"
- **Prime-vs-sub $ split** — small donut (Recipe 7 data). Answers "do they lead or follow?"
- **$-paid-over-time sparkline** — fed by `SubcontractorPayments.PaidDate` + `PaidAmount`. Answers "cash-flow velocity."
- **Geographic footprint** — Recipe 11 map with vendor's offices + a county-filled choropleth of contracts the vendor's touched (using `Contract.CountyId` reverse joins). Answers "where does this vendor work?"
- **Rating trend chart** — tiny line chart of `ContractorEvaluation.OverallRating` over `EvaluationDate` with reference lines at 6 / 8 / 10 (matching `RefContractorEvaluation.MinRating` thresholds for consultant / contractor / test).

**What NOT to visualize:**
- `VNCDE1`–`VNCDE4`, `VNDT1`–`VNDT6`, `VNFLG1`–`VNFLG10`, `VNNUM1`–`VNNUM4`, `VNLST1`/`VNLST2` — agency soft-cols; meanings vary per DOT; show as raw table only if an agency has mapped them, hide them otherwise.
- `MaximumCapacity`, `UncompletedWork`, `AdjustedNetWorth`, `AbilityFactor` — these are populated on only a tiny fraction of vendors on awdemo (all 0 on #160). Don't build a "remaining capacity" gauge as a hero element until you've confirmed the agency actually populates them.
- `ALTERNATEVENDOR_NM` as a hero display name — it's an abbreviated internal name; `LongName` is the public-facing one.
- Any attempt to compute a "DBE utilization %" from the single-row RefVendor view — that number only makes sense per-contract, not per-vendor-master.

---

### Awdemo gotchas specific to the vendor graph

1. **No `SuretyCompany` or `SuretyAgent` entity** — they are `RefVendor` rows with specific FKs on `Contract` / `ProposalVendor`. Don't attempt `GET /SuretyCompanies` → 404.
2. **No `VendorMaterial`, `VendorCertification`, `VendorContact` entities** — reference guide lies. The functionality is split across `Source` / `SourceManagementLevel` for materials, `RefVendorSBPCertifications` + `RefVendorDbeCertificationEvents` + `VendorAuthority` + per-discipline `*Qualification` tables for certifications, and `RefVendorOfficer` + `RefVendorAddress.Email` + `RefVendorPhone` for contacts.
3. **`SubcontractAgreement` doesn't exist** — the entity is just `Subcontract`.
4. **`ContractorEvaluation.ContractorId` not `ContractId`** — two-step join required to find evaluations for a contract.
5. **`LavorComplianceReview` typo** — the collection nav on `Contractor` is spelled `LavorComplianceReview` (missing 'b'); the target entity is correctly named `LaborComplianceReview`. The nav typo is stable across the schema — hardcode it.
6. **`ContractorEvalutions` typo** — the collection nav on `Contractor` is misspelled (missing 'a'). Target `ContractorEvaluation` is spelled correctly.
7. **DBE/UDBE/SBP certs scattered** — `DBECertStatus` on RefVendor is the master flag, but `RefVendorSBPCertifications` is the SBP equivalent and the two don't share a schema. Need separate queries for each.
8. **`DBECertStatus` is a String not a Bool** — values are `'Certified'` / `'Not Certified'`. Filter with `eq 'Certified'`, not `eq true`.
9. **`DbeCertified` vs `DbeCertifiedWorkItem` vs `DbeFirm` vs `DbeCommitment`** — four different fields across Subcontract (`DbeCertified`), SubcontractItem (`DbeCertifiedWorkItem`), SubcontractorPayment (`DbeFirm`, `DbeCommitment`). Each means something subtly different; use the schema to be sure.
10. **`DWRContractor.Hours`** is the total daily hours for that contractor-crew on that DWR (NOT per-person); the per-person detail is in `DWRContractorPersonnels`. See Part 3.
11. **`CertifiedPayrolls` nav from RefVendor is misleadingly empty for most primes** — on awdemo, only Bacco's payrolls are populated. Compliance Part 5 anchors on contract 38 for a reason.
12. **Dual nav props with `1` / `2` / `3` suffixes** — `Contracts` / `CONTRACT1` / `CONTRACT2` / `CONTRACT3` on RefVendor are each a different FK role played by this vendor across the Contract header's 4 vendor columns. Same pattern on `PROPOSALVENDOR1`/`2`, `REFVENDORAFFILIAT1`, `REFVENDORINSURANCE1`, `SUBCONTRACTORPAYMENT1`, `TRUCKING1`, `PURCHASE1`. Treat as separate collections; don't dedupe.
13. **`ObsoleteDate` on RefVendor** is a soft-delete marker — filter it out in dropdowns (`$filter=ObsoleteDate eq null`).
14. **`PrequalExpDate` of 1985 on #160** — a huge chunk of awdemo RefVendors have ancient PrequalExpDates from migration. Treat null-or-ancient as "no current prequal data" rather than "lapsed."
15. **Soft-deleted insurance** — `RefVendorInsurance.InsuranceStatus` is a String, not a Bool; filter `eq 'Active'` for current coverage. Expired policies remain in the table as audit trail.
16. **Officer SSN in plaintext** — `RefVendorOfficer.Ssn` is in the clear on awdemo; same gotcha as `PayrollEmployee.Ssn` from Part 5. Scrub before any UI exposure.
17. **`VendorAuthorities` ties `RefVendorId` to `UserInfoId`** — the authorized signer is a system user, not a `PersonInfo`. Lookup goes through UserInfo.
18. **`Trucking` sits under `Subcontract` but references `RefVendor` directly** — paying vendor and hauling vendor are both FK'd to RefVendor; two-step join to names.
19. **`PersonInfos` is 403** across the lab (noted in Parts 1 & 3). Any time an evaluation / officer / staff record points at a `PersonInfo`, you can hydrate the name only through a parent-side expand that includes the person record inline, not through a `GET /PersonInfos/{id}` direct call.
20. **`ContractorEvaluationGroup` ratings don't trivially average to `OverallRating`** — the rubric does weighted roll-up through `RefContractorEvaluationGroup` definitions. Trust the stored `OverallRating`, don't recompute from the children.

---

<a id="part-3-reference-catalogs-master-data"></a>

# Part 3 — Reference catalogs & master data

_The lookup backbone — every Ref* table grouped into 11 families (items/materials, geographic, labor, weather, equipment, vendor, workflow, financial, QA/QC, administrative, change-order/claim). A 3-strategy loading framework (preload / lazy-paginated / autocomplete) with measured latencies, plus UI patterns for dropdowns, typeaheads, and tree pickers._

The lookup backbone of the AMS data model — the `Ref*` and taxonomy tables that every form, dropdown, autocomplete and filter in a real UI needs. Agency-wide, slow-changing, usually small; the ones that aren't small (RefItem, RefVendor, RefFund) are the ones a UI has to search rather than enumerate. There are **119 `Ref*` entity sets** in the EDMX plus **53 more entities with taxonomy-shaped names** (Category/Type/Classification/Code/Status/Group/Class). Only a subset of those actually serve catalog data on awdemo; the ones that matter are below, each verified live. Every claim here was checked by live query against `ams-lab/awdemo` on 2026-09-30. The combined doc `docs/ams-business-flows-combined-2026-09-30.md` references many of these in passing — this file is where you look to understand each one on its own.

### Legend & gotchas

- **OData entity-set names are the plural form**, usually just the entity name with `s` appended — but there are *irregular plurals*: `ItemFamily` → `/ItemFamilies` (not `/ItemFamilys`), `RefCounty` → `/RefCounties`, `RefSampleStatus` → `/RefSampleStatuses`, `DecisionClass` → `/DecisionClasses`, `FedJobClass` → `/FedJobClasses`, `RefVendorWorkClass` → `/RefVendorWorkClasses`, `AutofinalizableTestStatus` → `/AutofinalizableTestStatuses`, `RefStormwaterDeficiency` → `/RefStormwaterDeficiencies`. Guess wrong and you get `HTTP 404 at …/<name>` — always a 404, never a hint. The naïve `s`-append works for *most* entity sets (`RefItem` → `/RefItems`, `RefDistrict` → `/RefDistricts`, `RefFund` → `/RefFunds`), so when the plural is irregular you'll find out the hard way.
- **Not all entities have a `Name`/`Code`/`Description` triad.** `FedJobClass`, `FedLaborEthnicGroup`, `FedDBEEthnicGroup` carry only `Description`. `ItemFamily` has `Name` + `Description` + `SpecBook`. `ReferenceEquipment` uses `Name` as *category* and `Description` as the actual equipment description. `RefOjtProgram` has `Name` and `OJTHoursToGraduate` but no description. `RefCounty.Name` is the code ("C001") and `Description` is the human label ("Alcona County") — don't assume one or the other is the display label; always check per table.
- **Legacy soft columns** — many agency-configurable catalogs carry `GENTEXT01..NN`, `DOCDE51..53`, `DOSST51..53`, `VCDT1/VCNUM1/VCSST1` columns that are agency-remapped. Don't rely on their meaning across installations.
- **$select footgun** — guessing a field name wrong returns `HTTP 400`. The error payload *does* name the missing field, so parse your 400 message rather than giving up — but always pre-check against `refs/awdemo_metadata.xml` via `from awp.metadata import parse_metadata`.
- **`Ref` prefix is a convention, not a rule.** The agency-wide shared vocabulary is split between `Ref*` tables and plain-named ones (`DecisionClass`, `FedJobClass`, `ItemFamily`, `Workflow`). Treat them as the same layer.

---

### Items & materials catalogs

The spine of the entire planning/payment/materials chain. Every ContractItem on a contract is a copy of a RefItem; every DwrAcceptanceRecord ultimately references a Material in a RefItemMaterialSet.

#### RefItem — the item master catalog

| | |
|---|---|
| Entity set | `/RefItems` |
| Rows on awdemo | **19,978** |
| Scalar fields | 61 (EDMX) |
| Nav props | 41 — the fan-out is huge; this is the single most-referenced catalog |

The agency-wide master item catalog — everything that can appear as a `ContractItem` on a contract. Combined doc Part 3 covers the planned-item → actual-item chain; this is the catalog end of it.

**Key fields (EDMX):**

| Field | Type | Notes |
|---|---|---|
| `Id` | Int64 | Primary key |
| `Name` | String | The item code (e.g. `8120144`) |
| `ShortDescription` | String | For dense tables |
| `Description` | String | Full description |
| `Unit` | String | Unit of measure — see distinct values below |
| `UnitSystem` | String | `English` / `Metric` |
| `CommonUnit` | String | Common unit when the agency has English+Metric variants |
| `ConversionFactorToCommonUnits` | Decimal | For unit conversion |
| `SpecBook` | String | The specification book this item belongs to (e.g. `03`, `12`, `100`) |
| `ItemType`, `ItemClass`, `ContractClass` | String | Classification codes |
| `LumpSum`, `BidAsLumpSum` | Boolean | Lump-sum vs unit-price |
| `MajorItem` | Boolean | Significant-value flag |
| `SpecialtyItem` | Boolean | Specialty work |
| `NonBid` | Boolean | Not bid (set by agency) |
| `DbeInterest`, `DbePercentToApply` | Boolean/Decimal | DBE participation hint |
| `ExemptFromRetainage` | Boolean | Payment logic |
| `RefPrice` | Decimal | Reference/engineer's estimate unit price |
| `ObsoleteDate` | DateTime | Set when the item is retired — filter it out in pickers |

**Live sample:**

```json
{"Id": 1, "Name": "8120144", "SpecBook": "03", "Description": "TS System, Temp, Furn",
 "Unit": "LS", "LumpSum": true, "ItemType": "Misc", "ItemClass": "Misc",
 "ShortDescription": "TS System, Temp, Furn, Edit"}
```

**Distinct `Unit` values seen on the first 200 awdemo rows:**
`ACRE, BAG, BAMT, CDAY, CFT, CRHR, CYD, LS` — but the full catalog has many more (LF, SF, SY, TON, GAL, EA, M3, m3 lowercase for metric, …). Don't hard-code the list; derive it from `/RefItems?$select=Unit&$top=5000` once at app boot.

**Referenced by (nav back-pointers):** `ContractItem`, `ContractProjectItem`, `ProposalItem`, `ProjectItem`, `ChangeOrderNewItem`, `BidItem`, `BidHistory`, `CostEstimateItem`, `MilestoneItem` + 30 more.

**Caching recommendation:** **lazy-paginated**. 20k rows × 61 fields is way too big to preload. Serve via autocomplete (`$filter=startswith(Name,'…') or contains(Description,'…')&$top=20&$select=Id,Name,Unit,ShortDescription`). Cache per-search-term with a 5-minute TTL. Catalog itself changes rarely so a longer TTL is safe.

#### ItemFamily — the item taxonomy

| | |
|---|---|
| Entity set | `/ItemFamilies` (**irregular plural**) |
| Rows on awdemo | **17** |
| Scalar fields | 8 |
| Nav props | 2 (`AcceptanceActionAssociations`, `RefItems`) |

Groups RefItems by specification-book section. Lets a UI render the item picker as a tree ("Section 200 — Earthwork" → "2050013 — Excavation, Channel"). **Flat, not hierarchical** — there's no `ParentItemFamilyId` on awdemo, despite what the vendor guide suggests. `SpecBook` is the only grouping axis.

| Field | Type |
|---|---|
| `Id`, `Name`, `Description`, `SpecBook` | — |

**Live sample:**

```json
{"Id": 6, "Name": "Section 200", "Description": "Earthwork",   "SpecBook": "200-599"}
{"Id": 7, "Name": "Section 300", "Description": "Bases and Subbases", "SpecBook": "200-599"}
{"Id": 8, "Name": "Section 400", "Description": "Hot Mix Asphalt",    "SpecBook": "200-599"}
```

**Caching recommendation:** **preload-and-cache**. 17 rows. Pull once at app boot into localStorage with a 1-hour TTL; render as a tree keyed by `SpecBook`.

#### RefItemMaterialSet + RefItemMaterialSetMaterial

| | |
|---|---|
| Entity sets | `/RefItemMaterialSets`, `/RefItemMaterialSetMaterials` |
| Rows on awdemo | 71 / lots |
| Scalar fields | 7 / 7 |

Catalog-level **"this RefItem's expected materials"** — the pattern the DWR acceptance chain actually uses lives on `ContractProjectItemMaterialSet` (Part 3 of combined doc), but the agency-wide default is here. Each RefItem can have multiple named sets (`Default`, `Secondary`), each set lists its materials with a `ConversionFactor` per unit.

**Live sample for RefItem 7976:**

```json
{"Id": 1, "RefItemId": 7976, "Name": "Default"}
{"Id": 2, "RefItemId": 7976, "Name": "Secondary"}
```

**Caching:** on-demand. Fetch when an item picker opens.

#### ItemGroup, ItemClassification, ProductGroup, Category

Auxiliary classification tables:

- **`/ItemGroups`** (7 rows) — alternate groupings like `excavation` / `Asph_Grade A`, each with a `CommonUnitOfMeasure` and `SpecBook`. Secondary to `ItemFamily`; most agencies won't use it.
- **`/ItemClassifications`** (1 row on awdemo) — nearly empty; schema only.
- **`/ProductGroups`** (7 rows) — material-category level: `Concrete`, `Binders`, `HMA`, `Aggregate`, `Rebar`, `Water`, `Crushables`.
- **`/Categories`** (20,564 rows) — contract-item categories keyed per contract, NOT a global catalog despite the name. This is a *per-contract* association, not a reference table.

**Caching:** ItemGroup / ProductGroup preload; Categories query per-contract-id on demand.

---

### Geographic catalogs

#### RefCounty

| | |
|---|---|
| Entity set | `/RefCounties` (**irregular plural**) |
| Rows on awdemo | **95** (approximates Michigan's 83 + a few overrides) |
| Scalar fields | 9 |

| Field | Type |
|---|---|
| `Id`, `Name`, `Description`, `ObsoleteDate`, `RecordSource` | — |

Note that `Name` is the **code** (`C001`) and `Description` is the **human label** (`Alcona County`).

**Live sample:**

```json
{"Id": 1, "Name": "C001", "Description": "Alcona County"}
{"Id": 4, "Name": "C004", "Description": "Alpena County"}
```

**Caching:** **preload-and-cache** (1-hour TTL). 95 rows, slow-changing.

#### RefDistrict

| | |
|---|---|
| Entity set | `/RefDistricts` |
| Rows on awdemo | **317** |
| Scalar fields | 22 |

Agency administrative districts / TSCs (Transportation Service Centers). Carries office address + phone + several legacy `DOCDE51..53`, `DOSST51..53` soft fields. On awdemo the names are five-digit codes (`05845`, `05879`) — your agency should have more useful descriptions.

**Caching:** **preload-and-cache**. 317 rows is still comfortable to preload; use a 1-hour TTL and project to `Id, Name, Description, CITY, STATE, ENGINEERNAME` to shrink the payload.

#### RefRegion, RefRegionCounty, RefWageZoneArea

- **`/RefRegions`** — 1 row on awdemo (`"asdf"`). Agencies that organise above the district level fill this in; MDOT does not.
- **`/RefRegionCountys`** — 404 on awdemo (not implemented). The region↔county M:N bridge table.
- **`/RefWageZoneAreas`** — 258 rows. Links `RefWageDecisionCraft` to geographic zones (all are `STATEWIDE` on awdemo). Used by the prevailing-wage flow in Part 5.

**Caching:** preload RefRegion; skip RefRegionCountys unless/until implemented; RefWageZoneArea is small enough to preload if you need the lookup.

---

### Labor catalogs

#### DecisionClass — the shared labor vocabulary

| | |
|---|---|
| Entity set | `/DecisionClasses` (**irregular plural**) |
| Rows on awdemo | **134** |
| Scalar fields | 10 |

The **shared craft vocabulary** that threads through DWRContractorPersonnel, CertifiedPayroll, OJT programs, apprenticeships, and ForceAccountContractorLabor. Each `DecisionClass` is one craft code (e.g. `OEG5` = "Operator Group 5, Crane with combined boom and jib between 220 ft and 300 ft") paired with a `FedJobClass` parent (e.g. "Equip Operators").

| Field | Type |
|---|---|
| `Id`, `FedJobClassId`, `Name`, `Description`, `ObsoleteDate`, `Conformance` (bool) | — |

**Live sample:**

```json
{"Id": 10, "FedJobClassId": 4, "Name": "OEG1",
 "Description": "Operator Group 1, Crane with combined boom and jib 400 ft; or longer"}
{"Id": 14, "FedJobClassId": 4, "Name": "OEG5",
 "Description": "Operator Group 5, Crane with combined boom and jib between 220 ft; and 300 ft;"}
```

**Caching:** **preload-and-cache** (1-hour TTL). 134 rows, central to display logic — always resolve `DecisionClassName` to the human description, never show the raw `OEDZ`-style code.

#### FedJobClass — the federal craft parent

| | |
|---|---|
| Entity set | `/FedJobClasses` (**irregular plural**) |
| Rows on awdemo | **19** |

The high-level federal craft bucket a `DecisionClass` rolls up to.

| Field | Type |
|---|---|
| `Id`, `Description`, `StartDate`, `EndDate` | — (no `Name`!) |

**Live sample (full table):**
`Carpenters`, `Cement Masons`, `Electricians`, `Equip Operators`, `Ironworkers`, `Laborers, Semi-Skilled`, `Laborers, Unskilled`, `Mechanics`, `Painters`, `Pipefitters, Plumbers`, `Truck Drivers`, `Clerical`, `Equipment Operators`, `Foremen/Women`, `Laborers-Semi Skilled`, `Laborers-Unskilled`, `Officials`, `PipeFitter/Plumbers`, `Supervisors`.

**Caching:** preload. 19 rows.

#### FedLaborEthnicGroup — EEO workforce reporting

| | |
|---|---|
| Entity set | `/FedLaborEthnicGroups` |
| Rows on awdemo | **11** |

Workforce composition classifications for EEO reports. Note there are *two generations* of codes present — the "old" sentence-case (`Amer Indian or Alaskan Native`) and the "new" ALL-CAPS (`AMERICAN INDIAN OR ALASKA NATIVE`). Carries a `StartDate`/`EndDate`; filter by `EndDate eq null` for current.

**Caching:** preload. 11 rows.

#### FedDBEEthnicGroup — DBE utilization reporting

| | |
|---|---|
| Entity set | `/FedDBEEthnicGroups` |
| Rows on awdemo | **7** |

Separate taxonomy for DBE firm ethnic classification (used by DbeCommitment).

**Live sample (full table):** `Asian-Pacific American`, `Black American`, `Hispanic American`, `Native American`, `Other (i.e. not of any other group listed here)`, `Subcontinent Asian American`, `Non-Minority`.

**Caching:** preload. 7 rows.

#### FieldInterviewJobClassification

| | |
|---|---|
| Entity set | `/FieldInterviewJobClassifications` |
| Rows on awdemo | **6** |

The craft classifications used in prevailing-wage field interviews. Each row has `DescriptionOfDutiesAndTools` + `WageRate` + `Apprentice`/`OjtTrainee` flags.

**Live sample:**

```json
{"Id": 1, "DescriptionOfDutiesAndTools": "Welding",  "WageRate": 19.50}
{"Id": 2, "DescriptionOfDutiesAndTools": "Flagging", "WageRate": 13.00}
```

**Caching:** this is **per-contract field-interview data**, not a global catalog — fetch for a specific review context.

#### RefOjtProgram — on-the-job training curricula

| | |
|---|---|
| Entity set | `/RefOjtPrograms` |
| Rows on awdemo | **5** |

| Field | Type |
|---|---|
| `Id`, `Name`, `OJTHoursToGraduate` (Int32), `OJTProgramSponsor`, `Comments`, `OJTProgramActive_DT`, `ObsoleteDate` | — |

**Live sample (full table):** `Reinforcing Steel - Ironworker` (4000 hrs), `CARPENTER TRAINEE` (520), `LABORER` (1000), `OPERATOR` (520), `TRUCK DRIVER` (260).

**Caching:** preload.

#### RefEmployeeApprenticeship + RefEmployeeApprenticeshipCraftDecision

| | |
|---|---|
| Entity sets | `/RefEmployeeApprenticeships`, `/RefEmployeeApprenticeshipCraftDecisions` |
| Rows on awdemo | 5 / 5 |

Agency-level record of individual apprentices. Not a *catalog* in the dropdown sense — it's one row per registered apprentice with `RequiredHoursToGraduate` and `HoursToDate`. Belongs more to the compliance flow (Part 5 of combined doc) than to lookups.

#### WorkClassification

| | |
|---|---|
| Entity set | `/WorkClassifications` |
| Rows on awdemo | **115** |

Vendor-level work-classification codes keyed on `SubcontractId`. This is actually *per-subcontract scope*, not a reference lookup — don't confuse with `/RefVendorWorkClasses` (the next section).

#### LaborClassification

**Not in schema.** The vendor doc mentions `LaborClassification` as an entity but it does not exist in awdemo's EDMX. The nearest substitutes are `DecisionClass` (the craft vocabulary) and `WorkClassification` (per-subcontract scope).

---

### Weather & environmental

#### RefWeather

| | |
|---|---|
| Entity set | `/RefWeathers` |
| Rows on awdemo | **5** |
| Scalar fields | 10 |

| Field | Type |
|---|---|
| `Id`, `Name`, `Description`, `StormwaterPeriodResponseDays` (Int16), `StormwaterEvent` (bool), `ObsoleteDate` | — |

**Live sample (full table):**

```json
{"Id": 1, "Name": "Cloudy",         "Description": "60% to 100% of sky is covered by cloud cover", "StormwaterPeriodResponseDays": 7}
{"Id": 2, "Name": "Isolated Storms","Description": "Scattered Storms accompanied by lightning",    "StormwaterPeriodResponseDays": 7}
{"Id": 3, "Name": "Partly Cloudy",  "Description": "30% to 60% of sky is covered by cloud cover",  "StormwaterPeriodResponseDays": 7}
{"Id": 4, "Name": "Sunny",          "Description": "0% to 30% of sky is covered by cloud cover",   "StormwaterPeriodResponseDays": 7}
{"Id": 5, "Name": "Rainy",          "Description": "1\" or >"}
```

**Caching:** preload-and-cache. Already loaded on every DWR detail page — put the whole table in localStorage once.

#### RefHoliday

| | |
|---|---|
| Entity set | `/RefHolidays` |
| Rows on awdemo | **1** (`"John's Birthday"` — demo data; nothing useful) |

Agency holiday calendar for time-charge calculations. **Awdemo essentially does not populate this** — a real agency fills it with Memorial Day, July 4, etc. The Part 4 schedule chapter notes this gap.

#### RefStormwaterDeficiency

| | |
|---|---|
| Entity set | `/RefStormwaterDeficiencies` (**irregular plural**) |
| Rows on awdemo | **3** |

Codes for stormwater-permit deficiencies with their mandated response-day counts. Fields: `Id, Type, ResponseDays`. Rows like `InspRptReq` with 5 response days.

---

### Equipment catalogs

#### ReferenceEquipment

| | |
|---|---|
| Entity set | `/ReferenceEquipments` |
| Rows on awdemo | **17** |

| Field | Type |
|---|---|
| `Id`, `Name`, `Description`, `ObsoleteDate` | — |

**NB: `Name` holds the equipment *category* (`Water/Gas Line, Sewer, Excavation`, `Road Maintenance`) and `Description` holds the specific machine (`310SE John Deere Rubber Tire Backhoe`, `Pavement Miller`, `CAT Dozer D4`).** Swap your mental model of which is which.

**Caching:** preload-and-cache (17 rows).

#### EOMTruckType, TruckingTruckType

| | |
|---|---|
| Entity sets | `/EOMTruckTypes`, `/TruckingTruckTypes` |
| Rows on awdemo | 8 / 5 |

Catalogs of truck configurations used in force-account billing and End-of-Month trucking reports. Each row carries lease amount / unit / hourly rate / unit capacity. Not really a lookup — more like **per-contract agency-defined truck line items** keyed on `EOMTruckingFirmId` / `TruckingId`.

---

### Vendor-related reference

#### RefVendor — the vendor master

| | |
|---|---|
| Entity set | `/RefVendors` |
| Rows on awdemo | **9,131** |
| Scalar fields | 63 |
| Nav props | **81** — the second most-referenced catalog after RefItem |

The agency-wide vendor directory — contractors, subcontractors, suppliers, consultants, service providers. Combined doc Part 1 walks `/vendors/:id` detail; this is the catalog end.

**Key fields:**

| Field | Type | Notes |
|---|---|---|
| `Id`, `Name` | — | `Name` is the vendor's *code* (`00253`) |
| `ShortName`, `LongName` | String | Business name variants |
| `VendorType` | String | See distinct values below |
| `CertificationType` | String | `PREQ` / `CERT` / `NONE` / `P+C` |
| `DBECertStatus` | String | `Not Certified`, `Certified`, etc. |
| `DBECertDate`, `DBECertRemovalDate`, `DBECertEntity`, `DBECertNum` | — | DBE certification trail |
| `PrequalCertDate`, `PrequalExpDate` | DateTime | Prequalification window |
| `CorporationType` | String | `CORP`, `LLC`, `N/A`, … |
| `EthnicGroup`, `PrimaryDbeWbe` | String | DBE/WBE classification |
| `MaximumCapacity`, `UncompletedWork`, `AdjustedNetWorth`, `AbilityFactor` | Numeric | Prequalification math |
| `IRSNumber`, `StateOfIncorporation`, `VendorEstablishedDate` | — | Legal data |
| `PayrollStartDay`, `RangeAnnualGrossReceipt` | — | Payroll / size reporting |
| `ObsoleteDate`, `RecordSource` | — | Lifecycle |

**Distinct `VendorType` values on awdemo:**
`C+O, C+P, C+V, CITY, CNST, CNTY, CSS, ENG, ENGC, ESCR, INS, LIEN, MISC, NONE, P+O, SRVC, SUPL, V+O, V+P, VILG` — 20 types.

**Distinct `CertificationType`:** `CERT, NONE, P+C, PREQ`.

**Caching:** **lazy-paginated**. 9k rows — serve via autocomplete on `Name` or `LongName`, cache the per-vendor detail individually.

#### RefVendorWorkClass

| | |
|---|---|
| Entity set | `/RefVendorWorkClasses` (**irregular plural**) |
| Rows on awdemo | **7,035** |

Prequalification per vendor per work class — each row says "vendor X is prequalified for class Y up to $Z". The amount cap is the vendor's bonding/capacity in that discipline.

| Field | Type |
|---|---|
| `Id`, `RefVendorId`, `Name` (the work-class code), `QualificationAmount` (Decimal), `VCDT1`, `VCNUM1`, `VCSST1` | — |

**Live sample:**

```json
{"Id": 1, "RefVendorId": 8405, "Name": "Ea",   "QualificationAmount": 152523.4}
{"Id": 4, "RefVendorId": 324,  "Name": "Ea",   "QualificationAmount": 194741.88}
{"Id": 5, "RefVendorId": 324,  "Name": "Fa",   "QualificationAmount": 15252.34}
```

**Caching:** keyed by `RefVendorId` — fetch a vendor's rows on demand for a vendor-detail page or a prequalification-check modal.

#### RefVendorSBPCertification — SBP certification events

| | |
|---|---|
| Entity set | `/RefVendorSBPCertifications` |
| Rows on awdemo | **14** |

**Small Business Program** certification history per vendor. Each row is one certification event (fields: `RefVendorId, SBPCertification, SBPCertEntity, SBPCertDate, SBPCertRemovalDate, SBPCertNum`).

**Live sample:**

```json
{"Id": 1, "RefVendorId": 758, "SBPCertification": "SSB", "SBPCertEntity": "DOT",
 "SBPCertDate": "2020-02-01", "SBPCertNum": "SSB-10001"}
```

**Caching:** fetch on demand per vendor.

#### VendorGroup, RefVendorAdditionalType, RefVendorSpecialtyCode, RefVendorStatewideIndicator, RefVendorNAICS

Mostly 1–5 rows each on awdemo — agency-specific flavor tables. See brief inventory below.

| Set | Rows | Purpose |
|---|---:|---|
| `/VendorGroups` | 3 | Grouping of vendors for reporting |
| `/RefVendorAdditionalTypes` | 1 | Additional vendor-type overlay |
| `/RefVendorSpecialtyCodes` | 3 | Specialty work codes |
| `/RefVendorStatewideIndicators` | 2 | Statewide-contract eligibility |
| `/RefVendorNAICSs` | 5 | NAICS industry codes |
| `/ExcludedVendorTypes` | **0** | Empty on awdemo |

**Caching:** preload each (all tiny).

---

### Workflow & process catalogs

Combined doc Part 4 covers the workflow state machine in depth. The catalog-level definitions:

#### Workflow + WorkflowPhase

| Set | Rows | Purpose |
|---|---:|---|
| `/Workflows` | **12** | One per entity type (CertPayroll, DBE, SubPayment, Proposal-Project-Contract, …) |
| `/WorkflowPhases` | **97** | Phases within each workflow (`Pending`, `Approved`, `Payroll Pending`, …) |

**Workflows (full list):**

| Id | Name | Type |
|---:|---|---|
| 1 | `CertPayrollExtWF` | External Payroll |
| 2 | `CertPayrollWF` | Internal Payroll |
| 3 | `Default` | Proposal-Project-Contract |
| 4 | `ExtSubPayment` | External Subcontractor Payment |
| 5 | `IntSubPayment` | Internal Subcontractor Payment |
| 6 | `ExtDbeCommitment` | External DBE Commitment |
| 7 | `ExtBidderQuoter` | External Bidder Quoter |
| 8 | `Test` | Proposal-Project-Contract |
| 9 | `MDOT` | Proposal-Project-Contract |
| 10 | `Default (CA)` | Proposal-Project-Contract |
| 11 | `testing123 -` | Proposal-Project-Contract |
| 12 | `ExtSBPCommitment` | External SBP Commitment |

**Caching:** preload both (12 + 97 rows).

#### RefIssue, RefIssueOwner, RefIssueEventTrigger, RefEventType

Issue-tracking configuration — what kinds of issues exist, who owns them, what UI buttons they expose. Rows: 16 / 4 / 62 / 4.

| Set | Rows | Notes |
|---|---:|---|
| `/RefIssues` | 16 | `Active` flag + `AssociatedToName` (e.g. `Bid History Item`, `Project`, `Proposal`) |
| `/RefIssueOwners` | 4 | Named owners with primary/edit flags |
| `/RefIssueEventTriggers` | 62 | UI event buttons (`Close`, `Close tracked issue`) with transition flags |
| `/RefEventTypes` | 4 | `Annual`, `Initial`, `Recertification`, `Special Reviews` |

**Caching:** preload.

---

### Financial reference

#### RefFund — the funding source catalog

| | |
|---|---|
| Entity set | `/RefFunds` |
| Rows on awdemo | **933** |

Agency-wide funding sources — federal programs, state funds, local-match funds, railroad accounts, etc. Keyed by `Id` with `Description` + `FundType` (`Federal` / `State` / `Non Federal` / `Other`) + optional `FundingGroup` (`CITY`, `CNTY`, `VILL`) + agency `FUNDPREFIX` soft field.

**Live sample:**

```json
{"Id": 1, "Description": "Wisconsin Central Ltd",        "FundType": "Federal"}
{"Id": 2, "Description": "City of Westland",             "FundType": "Federal", "FundingGroup": "CITY"}
{"Id": 3, "Description": "City of Wixom",                "FundType": "Federal", "FundingGroup": "CITY"}
{"Id": 4, "Description": "Wisconsin & Michigan Railway", "FundType": "Federal"}
{"Id": 5, "Description": "Village of Wolverine Lake",    "FundType": "Federal", "FundingGroup": "VILL"}
```

**Caching:** mid-sized — preload if the UI needs a dropdown; else lazy-paginated with search.

#### RefFundPackage + RefFundPackageFund — reusable funding bundles

| | |
|---|---|
| Entity sets | `/RefFundPackages`, `/RefFundPackageFunds` |
| Rows on awdemo | **6** / **11** |

A `RefFundPackage` is a named reusable funding mix (`F80S20` = "80% federal, 20% state"); `RefFundPackageFund` is the per-fund breakdown with `Percentage` + `Priority` + `Type` (`Federal`/`State`/`Other`).

**Live sample:**

```
RefFundPackage: F80S20  → RefFund 922 @ 80.0% Federal, RefFund 923 @ 20.0% Non Federal
RefFundPackage: bridge  → RefFund 837 @ 10.0% Federal, RefFund 221 @ 90.0% Federal
RefFundPackage: C3C     → RefFund 926 Federal, RefFund 928 Other, RefFund 927 State (no percentages → priority driven)
```

**Caching:** preload (small, central to funding setup).

#### RefPaymentEstimateType, RefPaymentApprovalLevel, RefPaymentEstimateException, RefPaymentSchedulePoint, ContractPaymentEstimateType

| Set | Rows | Purpose |
|---|---:|---|
| `/RefPaymentEstimateTypes` | **10** | PE cadence catalog: `Bi Weekly`, `Monthly`, `Semi-Final`, `Final`, `Supplemental`, `Progress - Cap Fac`, `Progress`, `Progress - Materials`, `TestRealEstate`, `Annual`. Also carries `PaymentEstimateType` grouping. |
| `/RefPaymentApprovalLevels` | **19** | Approval levels per PE type per role (fields: `Level, RefPaymentEstimateTypeId, RoleId`) |
| `/RefPaymentEstimateExceptions` | **23** | PE exception types: `Attention Flag`, `DBE Compliance`, `Exceeded Available Time`, `Funding Check`, `Item Overrun`, etc. Each has `Progress`/`Final` enforcement mode (`Must Resolve`, `Must Acknowledge`, `May be left Unresolved`, `Not Calculated or Displayed`). |
| `/RefPaymentSchedulePoints` | **7** | Schedule-based progress-payment trigger points |
| `/ContractPaymentEstimateTypes` | 359 | **Per-contract** application of PE types — not global; filter by `ContractId` |

**Caching:** preload the first four; ContractPaymentEstimateTypes is per-contract.

#### RefPriceIndex — price-adjustment indices

| | |
|---|---|
| Entity set | `/RefPriceIndexs` (**not** `/RefPriceIndexes` — 404) |
| Rows on awdemo | **6** |

Catalog of commodity price-adjustment series (fuel, asphalt, steel) with threshold percentages.

**Live sample:**

```
#1 FUEL (Fuel Cost Adjustment) / GAL
#2 PRIC (Price Adjustment) / Syd
#3 F2 (Testing fuel adjustment) / GAL, threshold 15%
#6 Steel / Lft, threshold 7%
```

**Caching:** preload.

#### PaymentEstimateContractOtherAdjustmentType — the "other" adjustment catalog

| | |
|---|---|
| Entity set | `/PaymentEstimateContractOtherAdjustmentTypes` |
| Rows on awdemo | **202** |

Catalog of "other" ad-hoc contract-adjustment line types (`OTHCA1`, etc.) that can be charged against a PE. Mostly per-PE instance data despite the name.

#### Categories

See earlier note — 20,564 rows but *per-contract* category records, not a global catalog.

---

### QA / QC reference

#### RefSampleStatus — sample lifecycle states

| | |
|---|---|
| Entity set | `/RefSampleStatuses` (**irregular plural**) |
| Rows on awdemo | **9** |
| Scalar fields | 12 |

The lifecycle state machine for `SampleRecord` (Part 3 of combined doc).

**Live sample (full table, in `SortOrder`):**

| Id | Name | SortOrder | IsAuthorizable | IsAcceptable | IsPrintable |
|---:|---|---:|:-:|:-:|:-:|
| 1 | Pending | 5 | — | — | ✓ |
| 2 | Logged | 10 | — | — | ✓ |
| 3 | Received at Destination Lab | 15 | — | — | ✓ |
| 4 | Received at Lab Unit | 20 | — | — | ✓ |
| 5 | In Testing | 25 | — | — | ✓ |
| 6 | Pending Authorization | 30 | ✓ | — | — |
| 7 | Void | 35 | ✓ | — | ✓ |
| 8 | Complete | 40 | ✓ | ✓ | — |
| 9 | Approved | 50 | ✓ | ✓ | ✓ |

The flags matter in display logic: a sample enters the "payment-gate acceptable" set only when `IsAcceptable=true`.

**Caching:** preload.

#### SampleRecordGroup

| | |
|---|---|
| Entity set | `/SampleRecordGroups` |
| Rows on awdemo | **425** |

Groups of SampleRecords for batch authorization (`GroupAuthorization` flag). Not a dropdown-catalog — these are *instance* records (one per actual group of samples), not reference data despite the name.

#### LabUnit — physical lab routing

| | |
|---|---|
| Entity set | `/LabUnits` |
| Rows on awdemo | **21** |
| Scalar fields | 10 |

Physical lab-routing graph: each row is a `(LabId, DestinationLabId)` pair plus flags (`IsMobile`, `BypassDestinationReceive`, `BypassLabUnitReceive`). Used to route a sample from field → lab → destination.

#### RefTestResultValue

| | |
|---|---|
| Entity set | `/RefTestResultValues` |
| Rows on awdemo | **3** |

Pass/Fail/INFO result codes for material tests, with `Autofinalizable` flag.

**Live sample (full table):**

```json
{"Id": 1, "Name": "Fail", "Description": "Fail"}
{"Id": 2, "Name": "Pass", "Description": "Pass", "Autofinalizable": true}
{"Id": 3, "Name": "INFO", "Description": "Test was for information only"}
```

#### AutofinalizableTestStatus

| | |
|---|---|
| Entity set | `/AutofinalizableTestStatuses` (**irregular plural**) |
| Rows on awdemo | **11** |

Overlay table — maps `RefCodeTableValueId` to `Autofinalizable` flag.

#### RefSpecification + RefSpecificationCondition

| Set | Rows | Purpose |
|---|---:|---|
| `/RefSpecifications` | **41** | Named test specifications (`Sieve Analysis 2014`, `SLUMP`, `Test30_Ref_Spec`) with `EffectiveDate`/`ExpirationDate`/`Active`/`ActionRelationshipId` |
| `/RefSpecificationConditions` | **34** | Child conditions per specification |

**Caching:** preload (small).

---

### Agency administrative

#### RefAdministrativeOffice — hierarchical org tree

| | |
|---|---|
| Entity set | `/RefAdministrativeOffices` |
| Rows on awdemo | **20** |
| Scalar fields | 18 |

**Hierarchical**: each row has `OfficeLevel` (1, 2, 3) and `ParentOfficeId`. The tree on awdemo mixes multiple agency samples:

- Level 1: `Central Office`, `NJDOT NORTH REGION`, `HeadQuarters`, `MO`, `Florida_DGM`
- Level 2 under `Central Office`: `01 Region - Metro`, `02 Region - Southwest`, `03 Region - University`, `Central Office - Title VI Management`
- Level 3 under `01 Region - Metro`: `Taylor TSC`, `Detroit TSC`
- Level 3 under `02 Region - Southwest`: `Marshall TSC`
- Level 3 under `03 Region - University`: `Lansing TSC`

Fields include six `GENTEXT01..06` soft fields.

**Caching:** preload-and-cache; render as a tree keyed on `ParentOfficeId`.

#### RefSpecialProvision — the special-provisions clause bank

| | |
|---|---|
| Entity set | `/RefSpecialProvisions` |
| Rows on awdemo | **4** |

Short bank of boilerplate contract clauses — fields: `Id, Name, Description, Text, NUMOFPAGES`. On awdemo these are demo entries (`"the quick brown fox jumps over the lazy dog"`); on a real agency this holds hundreds of insurance-requirement / railroad-crossing / supplemental-provisions texts.

#### Workflows

See earlier Workflow section.

---

### Change order & claim reference

#### RefChangeOrderExplanation + RefChangeOrderApprovalRule + RefChangeOrderApprovalGroup

| Set | Rows | Purpose |
|---|---:|---|
| `/RefChangeOrderExplanations` | **4** | Justification-category texts (`New Item`, `Time Adjustment`, `EAC`, `NeedMoreItems`), each tagged by `Type` (`Change Order` / `0005`) |
| `/RefChangeOrderApprovalRules` | **12** | Approval rules keyed by `(ChangeOrderType, ContractType)` with flags like `BalanceCompletedItems`, `ContModOnly` |
| `/RefChangeOrderApprovalGroups` | **8** | Approver groups (`Contractor`, `Project Manager`, `District Engineer`, `Controller`, `Governor's Office`) with `ApprovedDecision`/`DenyDecision`/`ContractorGroup`/`ExternalGroup` flags |
| `/ChangeOrderApprovalGroups` | 223 | **Per-change-order** approval instances (not a global catalog) |

#### RefContractClaimType

| | |
|---|---|
| Entity set | `/RefContractClaimTypes` |
| Rows on awdemo | **8** |

Claim type catalog with `AnalysisDays` + `NotificationDays` + `ResponseDays`.

**Live sample (full table):**

| Id | Name | Description | AnalysisDays |
|---:|---|---|---:|
| 1 | SUPNOI | Supplemental Notice of Intent | 30 |
| 2 | FinalPC | Final submittal of potential claim | 30 |
| 3 | NOI | Notice of Intent | 15 |
| 4 | OrDOTEOL1Const | Design issue ID'd during construction | 15 |
| 5 | OrDOTEOL1ConstInsp | Design issue ID'd during const inspect | 15 |
| 6 | OrDOTEOL2Liability | Notice to consultant of liability | 30 |
| 7 | OrDOTEOL2NoLiability | Notice to consultant of no liability | 30 |
| 8 | InitialPC | Initial submittal of potential claim | 15 |

**Caching:** preload.

#### RefRiskFactor

| | |
|---|---|
| Entity set | `/RefRiskFactors` |
| Rows on awdemo | **19** |

Catalog of risk factors used in cost estimation. Fields: `Id, Description, Category, CostEstimationPhase, EstimationMethodology, ImprovementType`.

---

### Permit & environmental reference

**Nothing dedicated on awdemo** — no `PermitType`, no `EnvironmentalCommitment`, no `PermitStatus` tables exist. The permit side is served by the Attachments mechanism (CustomBusinessEntity pattern) and ad-hoc contract fields rather than a catalog table. Deferred.

---

### Loading catalogs efficiently

#### The three loading strategies

| Strategy | When | Pattern |
|---|---|---|
| **Preload-and-cache** | Catalog has ≤ 200 rows and the whole thing fits in a dropdown or sidebar tree. | Fetch once at app boot into a shared cache (localStorage + in-memory). 1-hour TTL. |
| **Lazy-paginated with search** | Catalog has thousands of rows and the UI picker is autocomplete-driven. | `$top=20` + `$filter=startswith(Name,'…') or contains(Description,'…')`. Cache per-search-term with a 5-minute TTL. |
| **On-demand per-id** | A detail page needs one row by id. | `$filter=Id eq {id}` with 1-hour TTL per id. |

#### Preload-and-cache recipe

```
GET /RefCounties?$select=Id,Name,Description&$top=5000
GET /RefDistricts?$select=Id,Name,Description,CITY,STATE,ENGINEERNAME&$top=5000
GET /RefWeathers?$select=Id,Name,Description,StormwaterPeriodResponseDays,StormwaterEvent
GET /DecisionClasses?$select=Id,Name,Description,FedJobClassId
GET /FedJobClasses?$select=Id,Description
GET /FedLaborEthnicGroups?$select=Id,Description
GET /FedDBEEthnicGroups?$select=Id,Description
GET /RefSampleStatuses?$select=Id,Name,SortOrder,IsAuthorizable,IsAcceptable,IsPrintable&$orderby=SortOrder
GET /RefPaymentEstimateTypes?$select=Id,Name,PaymentEstimateType
GET /RefPaymentEstimateExceptions?$select=Id,Name,Progress,Final
GET /ItemFamilies?$select=Id,Name,Description,SpecBook&$orderby=SpecBook,Name
GET /Workflows?$select=Id,Name,Description,Type
GET /WorkflowPhases?$select=Id,PhaseName,Description,PhaseOrder&$orderby=PhaseOrder
GET /RefFundPackages?$select=Id,Name,Description
GET /ReferenceEquipments?$select=Id,Name,Description
GET /RefOjtPrograms?$select=Id,Name,OJTHoursToGraduate
GET /RefChangeOrderExplanations?$select=Id,Name,Description,Type
GET /RefContractClaimTypes?$select=Id,Name,Description,AnalysisDays
GET /RefAdministrativeOffices?$select=Id,Name,OfficeLevel,ParentOfficeId,Active
GET /RefSpecialProvisions?$select=Id,Name,Description
```

~**20 small requests, firing in parallel at app boot, each < 100ms warm**. Cost about a second of wall-clock on cold cache; after that everything is lookup-free.

Server-side cache key pattern: `catalog:{entity_set}:v1` with 1-hour TTL. Client-side mirror in localStorage under the same key with the server's cache-age stamp.

#### Lazy-paginated recipe (RefItem autocomplete)

```
GET /RefItems?$filter=(startswith(Name,'812') or contains(Description,'Excavation')) and ObsoleteDate eq null
    &$select=Id,Name,Unit,ShortDescription,SpecBook,ItemType
    &$top=20
    &$orderby=Name
```

Measured on awdemo cold: **~230ms** for `contains(Description,'Excavation')`, **~94ms** for `startswith(Name,'812')`. Starts-with is 2–3× faster — favor it when the user has typed digits (an item code) and fall back to `contains` on description otherwise.

Server-side cache key: `refitems:search:{q.lower()}:{limit}` with 5-min TTL. The project's own FastAPI route at `api/routes/ref_items.py` already follows this pattern (`ref_items_list_async` in `awp/entities.py`).

#### On-demand recipe

```
GET /RefItems?$filter=Id eq 7976&$expand=ItemFamily,RefItemMaterialSets($expand=RefItemMaterialSetMaterials)
```

Fetch one catalog row + its hierarchical children. The project's `ref_item_full_async` + `/api/ref-items/{id}` route uses this shape and adds usage statistics (every ContractItem that references this RefItem).

#### Current FastAPI coverage gaps

Only two catalog endpoints exist in the project today: `api/routes/ref_items.py` (list + detail) and vendor list / detail via `api/routes/vendors.py` (which hits `/RefVendors`). **Missing endpoints that would pay off:**

- `/api/catalogs/` — the master catalog landing page (list every Ref* table with row counts)
- `/api/catalogs/{name}` — paginated/searchable viewer for any catalog
- `/api/catalogs/preload` — a single endpoint that returns all preload-tier catalogs in one call for app boot
- `/api/decision-classes` — the labor vocabulary (currently nothing resolves `OEDZ`-style codes to human text; the UI shows raw codes)
- `/api/weather`, `/api/counties`, `/api/districts`, `/api/sample-statuses` — the small preload-tier catalogs served on their own route for easy consumption by the client
- `/api/ref-items/catalog-tree` — RefItem grouped by ItemFamily by SpecBook, for the tree picker

The pattern should mirror `api/routes/ref_items.py` with per-catalog TTL overrides on `api/cache.py` (longer TTL for small/stable catalogs: 1 hour; 5 minutes for autocomplete; 15 minutes for medium ones like RefVendor).

---

### UI query recipes

Twelve copy-pasteable queries, each with the UI question it answers and the response shape.

#### 1. Autocomplete typeahead on RefItem

**UI question:** user is typing in an item picker — show the top 20 matches by code prefix or description.

```http
GET /RefItems
    ?$filter=(startswith(Name,'{q}') or contains(Description,'{q}')) and ObsoleteDate eq null
    &$select=Id,Name,Unit,ShortDescription,SpecBook,ItemType,ItemClass
    &$top=20
    &$orderby=Name
```

Response:
```json
{"value": [
  {"Id": 2695, "Name": "2050013", "Unit": "m3", "ShortDescription": "Excavation, Channel", "SpecBook": "02"},
  …
]}
```

**Perf:** 90–230ms cold, < 10ms warm. Cache per-query 5 min.

#### 2. Autocomplete typeahead on RefVendor

**UI question:** sub-selector modal — find a vendor by name or code.

```http
GET /RefVendors
    ?$filter=((startswith(Name,'{q}') or contains(LongName,'{q}')) and ObsoleteDate eq null)
    &$select=Id,Name,ShortName,LongName,VendorType,CertificationType,DBECertStatus
    &$top=20
    &$orderby=LongName
```

Response includes `DBECertStatus` so the UI can badge DBE firms inline.

**Perf:** 100–250ms. Cache 5 min.

#### 3. Geographic filter — contracts in a county

**UI question:** "show me every contract whose primary jurisdiction is Alcona County."

```http
# Step 1: look up the county id (preload-cached)
GET /RefCounties?$filter=Description eq 'Alcona County'&$select=Id

# Step 2: filter contracts
GET /Contracts
    ?$filter=RefCountyId eq {countyId}
    &$select=Id,Name,ContractStatus,CurrentContractAmount,PercentPaid
    &$top=100
```

#### 4. Labor-classification rate lookup for a wage decision

**UI question:** the inspector is logging a worker — what's the prevailing rate for `OEG5` on wage decision 12?

```http
GET /RefWageDecisionClassifications
    ?$filter=RefWageDecisionId eq 12 and DecisionClassId eq {decisionClassId}
    &$expand=RefWageDecision($select=Name,EffectiveDate)
    &$select=Id,BaseRate,FringeRate,RefWageDecisionId,DecisionClassId
```

Combines with the preloaded `DecisionClass` catalog so the UI can show `OEG5 — Operator Group 5 (Crane 220–300 ft)` alongside the rate.

#### 5. Catalog usage leaderboard — most-used RefItems

**UI question:** across the portfolio, which RefItems appear on the most contracts? (great widget for a catalog-browser landing page)

```http
# Count ContractItem per RefItem — awdemo doesn't support $groupby, so fetch
# ContractItemIds and group client-side:
GET /ContractItems?$select=RefItemId,ContractId&$top=50000
# → client aggregates: top-N by distinct ContractId count per RefItemId
# → resolve names:
GET /RefItems?$filter=Id in ({topRefItemIds})&$select=Id,Name,ShortDescription,Unit
```

Cache the aggregate 24h — the leaderboard changes slowly.

#### 6. Orphaned-catalog-row report

**UI question:** which RefItems have *never* been used on any contract? (catalog-cleanup dashboard)

```http
GET /ContractItems?$select=RefItemId&$top=50000
# → client: distinct refItemIdsUsed = set
GET /RefItems?$select=Id,Name,ObsoleteDate&$top=20000
# → client: refItemIdsAll - refItemIdsUsed = orphans
```

Flag with "safe to retire?" when `ObsoleteDate eq null and never used`. Cache 1 day.

#### 7. "What codes exist for X?" — distinct-value dump

**UI question:** build a filter dropdown for `VendorType` from the actual data (not from a hard-coded enum).

```http
GET /RefVendors?$select=VendorType&$top=10000
# → client distincts: [C+O, CITY, CNST, CNTY, ...]
```

Awdemo doesn't support `$apply=groupby`, so always fetch + distinct client-side. Cache 1 hour.

#### 8. ItemFamily tree render

**UI question:** render the item picker as a tree ("Section 200 — Earthwork" → child items).

```http
# Catalogs (preloaded)
GET /ItemFamilies?$select=Id,Name,Description,SpecBook&$orderby=SpecBook,Name

# For a specific family's items:
GET /RefItems
    ?$filter=ItemFamily/Id eq {familyId} and ObsoleteDate eq null
    &$select=Id,Name,Unit,ShortDescription
    &$top=200
    &$orderby=Name
```

Note the nav filter `ItemFamily/Id eq {familyId}` works on awdemo.

#### 9. Night-before-letting dashboard: upcoming lettings + their proposals

Covered in combined doc Part 1 but the catalog contribution is the RefFundPackage lookup for each proposal's funding mix:

```http
GET /Proposals
    ?$filter=LettingId in ({tomorrowsLettingIds})
    &$expand=ProposalFunds($expand=RefFundPackage($select=Name,Description))
    &$select=Id,Name,EngineersEstimateAmount
```

#### 10. Vendor-prequalification check

**UI question:** can vendor 324 bid on work class `Fa`?

```http
GET /RefVendorWorkClasses
    ?$filter=RefVendorId eq 324 and Name eq 'Fa'
    &$select=Id,Name,QualificationAmount
```

Returns `{Id: 5, Name: "Fa", QualificationAmount: 15252.34}` → UI compares the proposal amount to `QualificationAmount` and badges accordingly.

#### 11. Weather histogram on contract DWRs

**UI question:** on contract 282, how many days of each weather code?

```http
# RefWeather is preloaded; DWRs filtered by contract
GET /DailyWorkReports
    ?$filter=ContractId eq 282
    &$select=Id,DwrDate,RefWeatherId
    &$top=500
# → client bucket by RefWeatherId, resolve names from preloaded /RefWeathers
```

Produces a 5-bar histogram — pairs well with the DWR cadence sparkline in Part 1.

#### 12. Catalog row-count dashboard

**UI question:** `/catalogs` landing page — one tile per Ref* table showing row count + "last updated".

```http
# For each preloadable catalog, fire $top=0&$count=true in parallel:
GET /RefCounties?$top=0&$count=true   → @odata.count: 95
GET /RefDistricts?$top=0&$count=true  → @odata.count: 317
GET /RefItems?$top=0&$count=true      → @odata.count: 19978
GET /RefVendors?$top=0&$count=true    → @odata.count: 9131
GET /RefFunds?$top=0&$count=true      → @odata.count: 933
# ... one tile per catalog
```

Each `$count=true` request is ~30ms warm. Cache the whole dashboard once-per-hour.

---

### How to use catalogs in a UI

#### Design principle

**Catalog data should feel instant.** The user never waits on a weather dropdown. If the catalog is small, preload it; if it's big, autocomplete it; if it's huge and hierarchical (RefItem), do both — preload the ItemFamily tree, then search within a chosen family. Resolve every code to its human description at the point of display; never leak `OEDZ` or `VCNUM1` to the user.

#### Three UI shapes to standardize on

1. **Dropdown** — `<select>` for catalogs ≤ 200 rows. Backed by preload. Shows `Description` (or `Name` where `Description` is absent — e.g. `FedJobClass`), stores `Id`. One component, three catalog variants (plain / hierarchical / grouped).
2. **Typeahead search** — `<input>` + debounced query for ≥ 500 rows. Backed by `/catalogs/:name?q=…`. The dropdown shows `Code — Description (badge: Unit/Type)`. On click, store `{Id, display}` for the form.
3. **Tree picker** — modal for hierarchical catalogs (`ItemFamily → RefItem`, `RefAdministrativeOffice`). Left pane is the tree, right pane is the filtered list. Use for item picker on cost-estimate editor and ChangeOrder new-item modal.

#### Master-catalog-browser pattern

A `/catalogs` landing page that lists every Ref* table as a card (row count, last-updated-at, "click to browse"). Each card links to `/catalogs/:name`:

- Left: paginated row list (search + filter)
- Right: detail pane for the focused row (its fields + usage: "referenced by 1,245 ContractItems across 89 contracts")

Covers two legitimate use cases: **admin discovery** ("what codes does our agency actually use?") and **catalog cleanup** ("is this RefItem obsolete?").

#### Visualizations that pay off

- **Catalog usage leaderboard** — top 20 RefItems by distinct contracts. Horizontal bar chart; shows what items drive the agency's spend. Data: query 5.
- **Catalog growth over time** — row count per month per catalog. Line chart. Reveals when agencies did big data imports. Data: `/RefItems?$filter=year(CreatedDate) ge 2020&$apply=…` (client-aggregated).
- **DBE-cert status mix on RefVendor** — stacked bar `Certified / Not Certified / Removed` × VendorType. Data: query 7 + grouping.
- **Sample status funnel** — count of active SampleRecords in each RefSampleStatus (Pending → Logged → … → Approved). Horizontal funnel chart; shows where samples pile up.
- **Agency org tree** — `/RefAdministrativeOffices` as a sankey or tree diagram with contract counts per office.

#### What NOT to try

- **Don't show the raw code.** `OEDZ`, `CNST`, `PREQ`, `CMPL` — none of these mean anything to a user. Always resolve.
- **Don't visualize `/RefHolidays`** — awdemo has one row that says "John's Birthday"; real agencies will have 10. There's no chart that helps.
- **Don't visualize `RefSpecialProvisions`** — the content is prose, not data.
- **Don't try to show the full `/RefItems` catalog** — 20,000 rows will crush any table. Always filter down to a context (an ItemFamily, a search term, a contract).
- **Don't rely on `GENTEXT01..06` / `DOCDE51..53` / `VCDT1` / `VCNUM1`** — meaning varies per agency. Suppress unless the deployment has mapped them.
- **Don't try `$apply=groupby(...)`** — awdemo returns 500 on `$apply`. Group client-side after fetching `$select`-projected rows.

---

### Awdemo gotchas specific to the catalog layer

1. **Irregular plurals (summary):** `/ItemFamilies`, `/RefCounties`, `/RefSampleStatuses`, `/DecisionClasses`, `/FedJobClasses`, `/RefVendorWorkClasses`, `/AutofinalizableTestStatuses`, `/RefStormwaterDeficiencies`. The `-s` guess 404s on all of these.
2. **`/RefPriceIndexs` (not `/RefPriceIndexes`)** — the one place where awdemo keeps the ugly `s` suffix.
3. **`/AlternateMaterialCategorys`, `/FacilityMaterialCategorys`, `/MaterialCategorys`, `/SourceMaterialCategorys`, `/Categorys`, `/ItemFamilys`, `/DecisionClasss`, `/RefCountys`, `/RefSampleStatuss`, `/FedJobClasss`, `/RefRegionCountys`, `/RefVendorWorkClasss`, `/RefDistrictCountys`, `/RefStormwaterDeficiencys`, `/SourceMaterialCategorys`** — all return 404 on awdemo. Easy to accidentally guess these.
4. **`/RefPriceIndexes` 404** (the "correct" English plural). Use `/RefPriceIndexs` instead.
5. **Field name ≠ display label.** `FedJobClass.Description` is the display label; there's no `Name`. `RefOjtProgram.Name` is the display label; there's no `Description`. `ReferenceEquipment.Name` is the *category* and `Description` is the equipment. Always inspect per table.
6. **Many "catalog-shaped" tables are actually per-contract or per-entity instances.** `Categories` (20,564 rows, per-contract), `SampleRecordGroups` (per-sample-batch), `PaymentEstimateContractOtherAdjustmentTypes` (per-PE), `ContractPaymentEstimateTypes` (per-contract). Don't preload these as global catalogs.
7. **`$apply=groupby(...)` returns HTTP 500** on awdemo. Fetch rows with `$select` and group client-side.
8. **`$select` field misses return HTTP 400** with the specific field name in the error payload. Pre-validate against EDMX or parse the error.
9. **`startswith(Name,'…')` is 2–3× faster than `contains(Description,'…')`** on awdemo. When the input looks like a code, prefer starts-with.
10. **`DBECertStatus` is a free-text string** on RefVendor, not a code. Observed values on awdemo include `Not Certified`, `Certified`, `Not DBE`, `Certified — DBE`, …. Don't drive logic off this; use `DBECertEntity` / `DBECertDate` / `DBECertRemovalDate` and compute status.
11. **The `Rainy` RefWeather row has no `StormwaterPeriodResponseDays`** — the others all have 7. Expect missing values on this one.
12. **`/RefHolidays` has 1 demo row** on awdemo. Real agencies populate 10–15. Don't code against assumed holidays.
13. **`ItemFamily` is flat, not hierarchical.** The vendor guide says to use "recursive $expand" on it; there is no `ParentItemFamilyId`. The grouping axis is `SpecBook`.
14. **`WorkClassification` ≠ `RefVendorWorkClass`.** The former is per-subcontract scope; the latter is per-vendor prequalification. Both are plausible catalog names, so easy to confuse.
15. **`/ExcludedVendorTypes` is empty** on awdemo (0 rows). Schema only.
16. **The `Workflow.Type` field holds the business-entity classification** (`External Payroll`, `Proposal-Project-Contract`, etc.) and is more useful than `Workflow.Name` for grouping — several agencies ship with `Default (CA)`, `MDOT`, `testing123 -` so names are messy.
17. **`/RefAdministrativeOffices` mixes multiple sample agencies** (MI, NJ, MO, FL + a `HeadQuarters` demo tree) on awdemo. A real deployment has one coherent tree.
18. **`SampleRecordGroup` with 425 rows is instance data**, not a catalog. Misleading name.

---

<a id="part-4-procurement-letting-bidding"></a>

# Part 4 — Procurement, letting & bidding

_The pre-award world — lettings, proposals, bids, apparent-low analysis, prequalification, bonds, and the bid-history price-intelligence engine._

**Date:** 2026-09-30 · **Instance:** `ams-lab/awdemo` · **Companion to:** `docs/ams-business-flows-2026-09-30.md`

This document covers the **pre-award world** in the AASHTOWare AMS data model — everything that happens before a Contract is executed and begins accruing DWRs. The companion doc covered what happens *after* award (labor hours, financial transactions, items & materials); this one covers how an advertisement becomes an awarded contract: **lettings** (bid events), **proposals** (RFP packages), **addenda** (bid-doc changes), **bidders** (who's eligible), **bids** (per-line prices), **apparent low** (ranking), **award**, **prequalification**, **bonds**, and the **bid-history engine** that drives engineer's estimates for future lettings. Every claim here was verified by live query against awdemo on 2026-09-30; proposals and bidders are heavily populated (10,915 proposals, 68,675 proposal-vendors, 3.19M bid rows), so this is where awdemo has the richest history outside of the DWR chain.

### Legend & conventions

- **Entity vs entity set** — Entity names are singular (`Letting`, `Proposal`). The OData path uses the entity set, which is almost always the plural (`/Lettings`, `/Proposals`). A few entity sets are *irregular plurals*: `Addendum` → `/Addendums` (not `Addenda`), `ProposalVendorSBPCommitmentSummary` → `/ProposalVendorSBPCommitmentSummaries`.
- **Cardinality in diagrams** — `A → B` means an A has one B (ref nav); `A →* B` means an A has many B (collection nav); `A *→* B` means many-to-many via an association entity.
- **Code tables rendered as strings** — ProposalStatus (`'R'`, `None`, …), LettingStatus (`'SCHD'`, `'CPT'`), ContractType (`'MAIN'`, `'ESD'`), ProposalType (`'LET'`) are short codes. The lookup tables for these are not uniformly exposed in awdemo; interpret them by convention (`SCHD`=Scheduled, `CPT`=Complete, `LET`=Letting).
- **Legacy field prefixes** — Proposal and Letting have fields prefixed `PR*`, `LP*`, `BL*`, `PRCDE*`, `PRDT*`, `PRSST*`, `PRNUM*`, `PRQTY*`, `PRFLG*`. These are generic agency-configurable "soft columns" inherited from the Trns·port legacy. Each agency maps them to local semantics (e.g. on this dataset `PRSST1` holds a project engineer name, `PRSST4` a date code, `PRSST5` a zip code). Don't rely on their meaning across installations — document per deployment.
- **Example proposal in use** — Where a concrete example would help, we use **Proposal 10849 "WHITEOAK BRIDGE"**, which was let at Letting 240 on 2019-02-14 and became **Contract 282** (the same contract this project has been exploring throughout). Where a competitive multi-bidder example helps, we use **Proposal 3664** (11 bidders, 6 valid bids, Rank 1 vendor 2040 at $331,704.51).

### Flow at a glance

```
                              Prequalification &
                               bonds (ongoing)
                                       │
                                       ▼
Letting ───────────────────► Proposal ───────────► ProposalItems (what's bid)
   │ (bid event)              │ (RFP)              ProposalSections (groupings)
   │                          │                    ProposalTimes (schedule bids)
   │                          │                    ProposalSBPGoals (DBE goals)
   ▼                          ▼
Bidders (per-letting)   Addendums (bid-doc updates)
   │                          │
   │                          ▼
   └──────────────────► ProposalVendors ─────► Bids (per-line)
                        (plan-holders +           BidSections (per-group)
                         bidders)                 BidTimes (per-time-item)
                             │
                             ▼
                     Apparent-low ranking   (ProposalVendor.VendorRanking,
                     + Awarded flag           Awarded, ValidBid)
                             │
                             ▼
                   Contract (ContractId written back
                             to Proposal.ContractId
                             + Contract.ProposalType='LET')
```

---

### Lettings

A **Letting** is a scheduled bid event — a date and time on which one or more proposals come due. Think of it as the auction clock: every proposal has a letting, every bid is sealed and timed against the letting date. 267 lettings in awdemo span 2005 → 2025.

#### Entity chain

```
Letting (1) ─→* Proposal (many RFPs opening on this date)
       │
       └─→* Bidder    (vendors signed up to bid in this letting — 500 error on awdemo lab,
                       documented from EDMX; see Bidders & bids section)
```

#### Letting — scalar fields

| Field | Type | Notes |
|---|---|---|
| `Id` | Int64 | PK |
| `Name` | String | Short identifier (`'1205339'`, `'4-item'`, `'240921'`) — usually a date-code or agency letting number |
| `LettingDate` | DateTimeOffset | Scheduled bid-opening date |
| `LettingTime` | String | Freeform, `'9:00 AM'`, `'09:00'` — not a parsed time |
| `LettingStatus` | String | Code: observed values include `'SCHD'` (scheduled) and `'CPT'` (completed) |
| `LETTINGLOCATION` / `LETTINGADDRESS` | String | Where bids are received |
| `BIDDEPOSITLOCATION` | String | Where bid bonds / deposits are physically filed |
| `WorkflowPhaseId` | Int64 → `WorkflowPhase` | Routing stage |
| `BLCDE1`, `BLDT1`, `BLDT2`, `BLSST1` | mixed | Agency soft columns |

#### Letting — nav properties

- `WorkflowPhase` → single ref
- `Proposals` → collection of `Proposal` (the RFPs letting on this date)
- `Bidders` → collection of `Bidder` (vendor-sign-ups) — **500 error on awdemo**

#### OData templates

```http
# All lettings in a date range, newest first
GET /Lettings?$filter=LettingDate ge 2024-01-01 and LettingDate le 2024-12-31
             &$orderby=LettingDate desc
             &$select=Id,Name,LettingDate,LettingTime,LettingStatus

# A single letting with its proposals
GET /Lettings?$filter=Id eq 240
             &$expand=Proposals($select=Id,Name,ContractName,ProposalStatus,
                                       AwardedAmount,AwardedVendorId,CallOrder)
```

#### Worked example — Letting 240

```json
{
  "Id": 240, "Name": "1205339",
  "LettingDate": "2019-02-14T00:00:00-05:00",
  "LettingTime": "9:00 AM",
  "LettingStatus": "CPT",
  "Proposals": [
    { "Id": 10849, "Name": "WHITEOAK BRIDGE", "AwardedVendorId": 160, "AwardedAmount": 1204969.1 }
  ]
}
```

#### Awdemo gotchas

- **`Bidders` entity set returns HTTP 500** on awdemo — the schema defines it (12 scalar fields including `LettingId`, `RefVendorId`, `NoQuotesReceived`, `SignedDate`, `SignedById`, `Comments`), but you cannot list it. In practice, use `ProposalVendors` to list vendors that actually submitted on a given letting (filter by `Proposal.LettingId`).
- **`LettingTime` is a free-form string**, not a time scalar. Expect `'9:00 AM'`, `'09:00'`, `'0900'`, or null. Parse defensively.
- **No `LettingProposal` association entity** — the relationship is a straight one-to-many via `Proposal.LettingId`.

---

### Proposals & items

A **Proposal** is the RFP package itself: a title, a description, the let-date, the engineer's estimate (`ProposalItemTotal`), prequalification requirements, a DBE goal, a bid-bond requirement, and all the per-line items up for bid. **107 scalar fields** on this one entity — it's the big one. 10,915 proposals in awdemo.

#### Entity chain

```
Proposal (1) ─→ Letting                  (ref: which bid event)
             ─→ PrimaryRefCounty/District (ref: where the work is)
             ─→ AwardedVendor (RefVendor)  (ref: winner, after award)
             ─→ Contract                   (ref: resulting executed contract)
             ─→* ProposalItems             (line items up for bid)
             ─→* ProposalSections          (groupings of items — "Road Work", "Bridge")
             ─→* ProposalTimes             (schedule bids — days / calendar milestones)
             ─→* ProposalVendors           (plan-holders + bidders)
             ─→* Addendums                 (bid-doc amendments)
             ─→* ProposalSBPGoals          (small-business participation goals)
             ─→* Projects                  (which Project(s) the proposal rolls up to)
             ─→* CostEstimates             (internal engineer's cost estimates — pre-let)
             ─→* RefVendorInsurances       (insurance snapshot for prime)
             ─→* SpecialProvisions         (contract-specific spec language)
```

#### Proposal — key scalar fields (abbreviated — full table is 107 columns)

**Identity & scope**

| Field | Type | Notes |
|---|---|---|
| `Id` | Int64 | PK |
| `Name` | String | Short name (`'WHITEOAK BRIDGE'`, `'33084-M60567'`) |
| `Description` | String | One-liner |
| `LongDescr` | String | Full narrative + prequalification clauses |
| `FederalProjectNumber` | String | FHWA project number, or `'N/A'` |
| `StateProjectNumber` | String | State project reference |
| `ContractType` | String | Code: `'MAIN'`, `'ESD'`, `'IDQ'`, … |
| `ContractWorkType` | String | Code: `'BREC'` (bridge recon), `'RECD'`, `'BTUN'`, etc. |
| `ProposalType` | String | `'LET'` for let-and-bid; also `'EMER'`, `'ADHO'` observed |
| `CallOrder` | String | Position within a multi-proposal letting (`'1'`, `'084'`) |
| `SpecBook` | String | Which spec book edition applies (`'03'`, `'12'`) |
| `UnitSystem` | String | `'English'` or `'Metric'` |

**Dates (letting lifecycle)**

| Field | Type | Notes |
|---|---|---|
| `PublicationDate` | DateTimeOffset | When the ad hit the street |
| `EstimatedDate` | DateTimeOffset | Internal estimate finalized |
| `StatusDate` | DateTimeOffset | Last status change |
| `PassedToDss` | DateTimeOffset | Handed to bid-decision-support |
| `PassedToConstruction` | DateTimeOffset | Transition into execution world |
| `TransitionToCRLMSConst_Dt` | DateTimeOffset | Transition to the construction LMS system |
| `ExecutionDate` | DateTimeOffset | Contract signed |
| `NoticeToProceedDate` | DateTimeOffset | Clock starts |
| `AnticipatedConstructionEndDate` | DateTimeOffset | Expected finish |

**Status & result**

| Field | Type | Notes |
|---|---|---|
| `ProposalStatus` | String | Short code (`'R'` = Rejected observed; often null during pre-let life) |
| `Rejected` | Boolean | Hard reject flag |
| `AwardedVendorId` | Int64 → RefVendor | Winner |
| `AwardedAmount` | Decimal | Winning bid total |
| `ContractId` | Int64 → Contract | Written back after contract execution |
| `ContractName` | String | Mirrors the Contract's Name once awarded |
| `PassDSS` | String | `'C'`, `'D'`, etc. — DSS pass/decision code |
| `WorkflowPhaseId` | Int64 | Current workflow stage |

**Estimate & bond**

| Field | Type | Notes |
|---|---|---|
| `ProposalItemTotal` | Decimal | Sum of ExtendedAmount across ProposalItems — engineer's estimate (the number the agency expects bids to beat) |
| `ProposalItemTotalUsingLowBidAlternate` | Decimal | Same but with low-bid alternate groups resolved |
| `AvailableFunding` | Decimal | Programmed funds available |
| `ProposalCost` / `CompletePlanCost` / `PlanWithoutCrossSectionCost` / `PerPlanSheetCost` | Decimal | Internal cost-estimate rollups |
| `BIDBOND` | Decimal | Required bid-bond amount (dollars, e.g. 25000.0) |
| `DBEGOAL` | String | Legacy string DBE goal |
| `DbeGoalPercent` | Decimal | Numeric DBE goal (e.g. 5.0) |
| `WbeGoalPercent` | Decimal | WBE goal if separately tracked |
| `SETASIDE` | String | Set-aside program code |
| `OjtGoal` / `OjtGoalUnits` / `OjtGoalComments` | mixed | On-the-job training apprentice goal |

**Classification**

| Field | Type | Notes |
|---|---|---|
| `PrimaryRefCountyId` | Int64 → RefCounty | Where the work is |
| `PrimaryRefDistrictId` | Int64 → RefDistrict | DOT district |
| `HighwayType` / `ImprovementType` / `FunctionalWorkClassification` / `Terrain` / `UrbanRural` | String | Agency-coded classifications |
| `ContractQual1` / `ContractQual2` / `ContractQual3` | String | Required prequalification codes |

**Legacy soft columns** (`PRCDE1-3`, `PRDT1-5`, `PRFLG1-5`, `PRLST1`, `PRNUM1-3`, `PRQTY1-2`, `PRSST1-5`, `LPDT1-4`, `LPFLG1-2`, `LPSST1-4`, `LPLST1`) — agency-mappable.

#### ProposalItem — the thing you actually bid on

26 scalar fields; the ones that matter:

| Field | Type | Notes |
|---|---|---|
| `Id` | Int64 | PK |
| `ProposalId` | Int64 → Proposal | |
| `ProposalItemLineNumber` | String | Zero-padded sort key (`'0010'`, `'0020'`) — order within the proposal |
| `RefItemId` | Int64 → RefItem | Catalog item (where the unit price pays against) |
| `ProposalSectionId` | Int64 → ProposalSection | Section grouping |
| `SpecBook` | String | Which spec book this item is governed by |
| `Quantity` | Decimal | Expected quantity for engineer's estimate |
| `UnitPrice` | Decimal | **Engineer's unit price** (not a bid; the agency's own estimate) |
| `ExtendedAmount` | Decimal | `Quantity × UnitPrice` — rolls into `Proposal.ProposalItemTotal` |
| `AverageBidUnitPrice` | Decimal | **Historical price intel** — snapshot of recent-letting average for this RefItem at let-time |
| `SupplementalDescription` | String | Extra text appended to the catalog description for this specific item |
| `IsAlternate` | Boolean | Marks membership in a low-bid alternate set |
| `AlternateSetName` / `AlternateMemberID` | String | Alt-set groupings (bidders choose only one member of a set) |
| `BidRequirementCode` | String | `'R'` required, `'O'` optional, etc. |
| `UnitPriceComparison` | Decimal | For post-let analysis |
| `LowCost` / `LowCostNoLcc` | Boolean | Winning-side flag within alternate groups |
| `IsPriceLocked` | Boolean | Prevents further estimate changes |
| `AverageBidUnitPrice` | Decimal | Snapshot of recent-letting average for the RefItem — think "last comparable price" |
| `EstimationType` | String | Where the UnitPrice came from (ad hoc, bid-based, worksheet, etc.) |
| `WarningMessage` | String | Validation note (`'Price outside expected range'`, …) |

#### ProposalSection — groupings within a proposal

```
ProposalSection.Id
              .ProposalId
              .Name                      e.g. '0001'
              .Description               e.g. 'Road Work', 'Bridge', 'Signing'
              .ProposalSectionTotal      sum of items in this section
              .BaseSection               Boolean — is this the "main" section vs an alternate
              .LifeCycleCost             LCC-adjusted number (for alternates)
              .CategoryAlternateSetName / .CategoryAlternateMemberId   alternate-set grouping
              .LowCostFlag / .OriginalLowCostFlag                      which alternate won
```

Bidders bid at the item level, but totals are also tabulated per section — `BidSection.SectionTotal` is the per-bidder, per-section rollup. This is what powers section-by-section rank comparisons.

#### ProposalTime — time charges that are also bid-selectable

A **ProposalTime** is a schedule item that the bidder prices in days. On a project with multiple time-charge sites, each site gets its own ProposalTime; bidders submit a `BidTime.NumberOfTimeUnitsBid` for each. 5,645 proposal-times in awdemo.

Key fields:

| Field | Notes |
|---|---|
| `Name` | Code (`'00'`, `'A'`) |
| `Description` | Human (`'Site 00'`, `'Main site'`) |
| `MilestoneType` | `'DT'` (calendar date), `'WD'` (working days) |
| `Main` | Boolean — is this the primary time charge |
| `CompletionDate` | Target substantial-completion date |
| `MinimumTime` / `MaximumTime` | Caps on bidder-specified time |
| `LiquidDamageRate` / `LiquidDamageUnitOfTime` | $/day penalty for overrun |
| `RoadCostPerTimeUnit` | User-cost per day (for A+B bidding) |
| `NumOfUnit` / `Unit` | |

#### OData templates

```http
# Proposal header with its context (one call)
GET /Proposals?$filter=Id eq 10849
             &$expand=Letting,PrimaryRefCounty,PrimaryRefDistrict,AwardedVendor,Contract

# Proposal items (the "bid tab" column of items)
GET /ProposalItems?$filter=ProposalId eq 10849
                  &$orderby=ProposalItemLineNumber
                  &$expand=RefItem($select=Id,Description,UnitOfMeasure,ItemCode),ProposalSection($select=Id,Name,Description)
                  &$select=Id,ProposalItemLineNumber,SpecBook,Quantity,UnitPrice,ExtendedAmount,
                           AverageBidUnitPrice,SupplementalDescription,IsAlternate,AlternateSetName

# Proposal sections totals (engineer's estimate by group)
GET /ProposalSections?$filter=ProposalId eq 10849&$orderby=Name
                      &$select=Id,Name,Description,ProposalSectionTotal,BaseSection

# Proposal time charges
GET /ProposalTimes?$filter=ProposalId eq 10849
                   &$select=Id,Name,Description,MilestoneType,Main,CompletionDate,
                            MinimumTime,MaximumTime,LiquidDamageRate,LiquidDamageUnitOfTime
```

#### Worked example — Proposal 10849 "WHITEOAK BRIDGE"

```json
{
  "Id": 10849, "Name": "WHITEOAK BRIDGE",
  "Description": "Bridge removal and replacement and approach work",
  "LettingId": 240,
  "ContractId": 282, "ContractName": "WHITEOAK BRIDGE",
  "ContractType": "ESD", "ContractWorkType": "BREC",
  "ProposalType": "LET",
  "CallOrder": "1",
  "SpecBook": "03",
  "UnitSystem": "English",
  "PublicationDate": "2006-03-27T00:00:00-05:00",
  "PassedToConstruction": "2021-04-06T15:29:36-04:00",
  "TransitionToCRLMSConst_Dt": "2024-08-28T00:00:00-04:00",
  "PrimaryRefCountyId": 1, "PrimaryRefDistrictId": 156,
  "BIDBOND": 25000.0,
  "ProposalItemTotal": 1204969.1,
  "AwardedVendorId": 160, "AwardedAmount": 1204969.1,
  "LongDescr": "Bridge removal and replacement along with related approach work on Mikado Road at Van Etten Creek, Alcona County. ** 620 Fa ** In addition to the above minimum prequalification requirement..."
}
```

Awarded dollar = engineer's estimate dollar (1,204,969.10 — only one bidder cleared, who happened to tie the estimate exactly). The companion flow doc shows this contract paid $1,147,109.70 of that over 11 pay-estimates, after $389.06 in change orders.

#### Awdemo gotchas

- **`Rejected` is a boolean; `ProposalStatus` is a code string** — the two can disagree. On this dataset most awarded proposals have `ProposalStatus` null and `Rejected = false`.
- The soft columns (`PRCDE*`, `PRSST*`, `LPDT*`) are **agency-remapped per deployment** — don't infer meaning without agency metadata. On awdemo `PRSST4` looks like a `yymmdd` date code, `PRSST5` like a zip — but that's just this dataset.
- `ContractProposalName` on `Contract` and `ContractName` on `Proposal` **both exist and both mirror the proposal name** — the historical path is Proposal.ContractName gets copied into Contract when awarded.
- There is no `EngineersEstimate` field — the engineer's estimate IS `Proposal.ProposalItemTotal` (sum of ProposalItem.ExtendedAmount).

---

### Prebid & addenda

Between publication and letting, bid documents are revised. An **Addendum** is the formal change record: a numbered amendment to a proposal, with its own approval and close dates. 4,519 addendums in awdemo.

#### Addendum — scalar fields

| Field | Type | Notes |
|---|---|---|
| `Id` | Int64 | PK |
| `ProposalId` | Int64 → Proposal | |
| `AddendumNumber` | Int32 | Sequential (1, 2, 3) within the proposal |
| `Description` | String | What's changed (`'Changes to Proposal and Plans'`, `'Changes to Spec Book Section 712'`) |
| `DateCreated` | DateTimeOffset | When drafted |
| `DateApproved` | DateTimeOffset | When issued to bidders |
| `DateClosed` | DateTimeOffset | When the response window closed |
| `Comments` | String | Freeform |
| `ADCDE1` | String | Agency soft column |

**Example:** Proposal 3664 had Addendum 1 "Changes to Proposal and Plans" issued 2010-07-30 — on the same day it was approved (indicating a straight bid-doc revision, not a bidder-question-driven amendment).

#### What's missing from awdemo

- **No `PrebidEvent` entity** — if an agency uses pre-bid meetings, that's handled outside this schema (document management, calendar system, etc.).
- **No `PrebidQuestion` / Q&A entity** — bidder questions during the ad period aren't modeled here. The closest proxy is `ProposalVendorMsg` (Warning/Info messages from the loading/validation system — not Q&A).
- **No `AgencyNotification` to bidders** — notification distribution lives in document management.

#### OData template

```http
GET /Addendums?$filter=ProposalId eq 10849&$orderby=AddendumNumber
              &$select=Id,AddendumNumber,Description,DateCreated,DateApproved,DateClosed,Comments
```

---

### Bidders & bids

Three overlapping concepts, all with "Bid" or "Bidder" in the name — they are **not** the same thing:

| Entity | Grain | What it records |
|---|---|---|
| `Bidder` | one per vendor per Letting | Vendor signed up for a letting (whole letting, not a specific proposal). **500 on awdemo lab** |
| `ProposalVendor` | one per vendor per Proposal | Vendor is on the plan-holder list and/or submitted a bid on this specific proposal; carries bid rollup totals and the award decision |
| `Bid` | one per vendor per ProposalItem | **The actual line-item price** a vendor bid |

Plus two per-grouping bid rollups:

| Entity | Grain | What it records |
|---|---|---|
| `BidSection` | one per vendor per ProposalSection | Vendor's total for a section (the sum of their Bids within it) |
| `BidTime` | one per vendor per ProposalTime | Vendor's time bid (days) for a time-charge item |

#### Entity chain

```
Letting ─→* Bidder                     (vendor signed up for the letting)
                                        │
Proposal ─→* ProposalVendor ◄───────────┘
             │   │   │
             │   │   └─→* BidTime         (per-time-item: days bid × $/day user cost)
             │   └─────→* BidSection      (per-section rollup)
             └─────────→* Bid             (per-line price × quantity → extended)
```

#### ProposalVendor — the bidder's bid envelope

27 scalar fields:

| Field | Type | Notes |
|---|---|---|
| `Id` | Int64 | PK |
| `ProposalId` | Int64 → Proposal | |
| `RefVendorId` | Int64 → RefVendor | Who's bidding |
| `SuretyCompanyId` | Int64 → RefVendor | Surety on the bid bond |
| `SuretyAgentId` | Int64 → RefVendor | Agent/broker on the bid bond |
| `OnPlanholderList` | Boolean | They requested bid docs (whether or not they submit) |
| `ValidForBidding` | Boolean | Prequalified for the required work types |
| `BidType` | String | Submission mechanism (electronic, paper, etc.) |
| `BidStatus` | String | Submission state |
| `BidNotes` | String | Freeform |
| `BidTotal` | Decimal | **Vendor's declared bid total** (what they submitted) |
| `VendorBidItemTotal` | Decimal | Sum of their Bid.ExtendedAmount rows (calculated) |
| `VendorTimeTotal` | Decimal | Sum of their BidTime.CalculatedAmount rows |
| `VendorTotalBid` | Decimal | Items + Time together |
| `LifeCycleCostTotal` | Decimal | LCC-adjusted total (for alternate-selection decisions) |
| `CalculatedExtendedAmount` (via Bid)/`CalculatedSectionTotal` (via BidSection) | | Server-side recomputation |
| `OriginalValidBid` | Boolean | Was it a valid bid at letting time (preserved after post-award review) |
| `ValidBid` | Boolean | Current validity (can go false after invalidation) |
| `InvalidBidCode` | String | Why it was invalidated |
| `VendorRanking` | Int32 | **Rank: 1 = apparent low, 2 = second low, …; null = didn't submit a valid bid** |
| `Awarded` | Boolean | **Winner flag** |
| `PotentialAwardAmount` | Decimal | What the vendor would be paid if awarded (= BidTotal less adjustments) |
| `CurrentWork` | Decimal | Vendor's current workload at bid time (for prequalification capacity) |
| `WorkflowPhaseId` | Int64 | |

#### Bid — the per-line price

19 scalar fields:

| Field | Notes |
|---|---|
| `Id` | PK |
| `ProposalVendorId` → ProposalVendor | Who |
| `ProposalItemId` → ProposalItem | Which line |
| `ProposalItemLineNumber` | Denormalized for sorting (`'0010'`) |
| `BidPrice` | Vendor's unit price |
| `ExtendedAmount` | `Quantity × BidPrice` |
| `CalculatedExtendedAmount` | Server-computed; mismatch flagged |
| `LowCostFlag` | Winning alternate within an alternate set |
| `LifeCycleCost` | LCC-adjusted price for alternate decision |

#### BidSection — per-vendor per-section rollup

| Field | Notes |
|---|---|
| `ProposalVendorId` → ProposalVendor | |
| `ProposalSectionId` → ProposalSection | |
| `ProposalSectionName` | `'0001'` |
| `SectionTotal` | Vendor-submitted |
| `CalculatedSectionTotal` | Server-recomputed |
| `SectionTotalMismatch` | Flag |
| `LowCostFlag` / `OriginalLowCostFlag` | Which alternate won within this bidder |

#### BidTime — per-vendor per-time-item

| Field | Notes |
|---|---|
| `ProposalVendorId` → ProposalVendor | |
| `ProposalTimeId` → ProposalTime | |
| `ProposalTimeName` | `'00'`, `'A'` |
| `NumberOfTimeUnitsBid` | Days (or whatever unit) |
| `CalculatedAmount` | `Days × RoadCostPerTimeUnit` (for A+B scoring) |
| `ValidBid` | |

#### OData templates

```http
# All bidders on a proposal, ranked
GET /ProposalVendors?$filter=ProposalId eq 3664
                     &$orderby=VendorRanking,BidTotal
                     &$expand=RefVendor($select=Id,Name,LongName,ShortName)
                     &$select=Id,RefVendorId,BidTotal,ValidBid,Awarded,VendorRanking,
                              SuretyCompanyId,SuretyAgentId,OnPlanholderList,ValidForBidding

# Cross-bidder prices on one line item (the bid-tab column)
GET /Bids?$filter=ProposalItemId eq 1
         &$expand=ProposalVendor($select=Id,RefVendorId,VendorRanking;$expand=RefVendor($select=Id,Name))
         &$select=Id,BidPrice,ExtendedAmount,LowCostFlag

# Full matrix: every bidder's bid on every item (expensive — see UI query recipes)
GET /Bids?$filter=ProposalVendor/ProposalId eq 3664
         &$orderby=ProposalItemLineNumber,ProposalVendor/VendorRanking
         &$expand=ProposalVendor($select=Id,RefVendorId,VendorRanking),
                  ProposalItem($select=Id,ProposalItemLineNumber,RefItemId,Quantity)
```

#### Worked example — Proposal 3664, 11 bidders, Item line 0010

```
Item 1 (line 0010), engineer's estimate: $36,000.00 (= 1 × $36,000)
                   AverageBidUnitPrice:  $30,205.00

Bids (6 valid submissions):
  Rank 1 (vendor 2040)      PV=1   $30,000.00  →  $30,000.00
  Rank 2 (vendor 6423)      PV=2   $36,000.00  →  $36,000.00
  Rank 3 (vendor 187)       PV=7   $36,000.00  →  $36,000.00
  Rank 4 (vendor 8412)      PV=9   $23,000.00  →  $23,000.00  ← lowest on this line, but didn't win overall
  Rank 5 (vendor 7219)      PV=10  $36,000.00  →  $36,000.00
  Rank 6 (vendor 1)         PV=11  $20,230.00  →  $20,230.00  ← lowest on this line

Total winner (Rank 1): $331,704.51 across all 50 lines; 2nd low: $355,818.09 (vendor 6423 at +7.3%)
```

The per-line low doesn't always come from the per-total low — this is the classic **unbalanced-bid detection** opportunity (see UI query recipes below).

#### Awdemo gotchas

- **`Bidder` entity set is 500** — don't try to list it. If you need "who signed up to bid", use `ProposalVendor?$filter=OnPlanholderList eq true`.
- **`ProposalVendor.VendorRanking` is null for non-submitters** — plan-holders who never bid, or whose bid was invalid at letting time, have no rank. Treat null as "did not place" rather than tying.
- **Two totals: `BidTotal` (declared) and `VendorBidItemTotal` (calculated)** — they can disagree. Pay attention to the mismatch (it's part of valid-bid review).
- **`SuretyCompanyId` and `SuretyAgentId` are RefVendor IDs** — they point back into the same vendor master; a surety company is just a vendor of type surety. There is no separate `SuretyCompany` entity set in awdemo (`/SuretyCompanies` 404s; the schema has no such entity).

---

### Apparent low & award

Apparent-low analysis is **in-table**, not a separate entity. The ranking lives on `ProposalVendor.VendorRanking` and the winner is `ProposalVendor.Awarded = true`. Transitioning to a contract writes:

- `Proposal.AwardedVendorId` = winner's RefVendor
- `Proposal.AwardedAmount` = winner's BidTotal
- `Proposal.ContractId` = new Contract.Id
- `Proposal.ContractName` = mirror of Contract.Name
- `Proposal.PassedToConstruction` = timestamp
- `Proposal.TransitionToCRLMSConst_Dt` = timestamp when handed to the Construction & Materials system
- `Contract.ProposalType` = `'LET'`

The relationship from Contract back to Proposal is implicit — Contract carries `ContractProposalName`, `ProposalType`, `BIDBOND`, and `AwardedContractAmount`, but **does not carry a ProposalId foreign key**. To go Contract → Proposal, you must query:

```http
# Contract 282 → its originating proposal (via name match + ContractId backlink)
GET /Proposals?$filter=ContractId eq 282&$select=Id,Name,LettingId,PublicationDate,AwardedVendorId,AwardedAmount
```

#### Rejected / withdrawn proposals

- `Proposal.Rejected = true` + `ProposalStatus = 'R'` — proposal was pulled before or after letting
- `Proposal.AwardedVendorId = null` after letting — "no acceptable bids" condition
- `ProposalVendor.ValidBid = false` + `InvalidBidCode` populated — individual bid invalidated during review

#### Awdemo gotchas

- `ProposalSelectionSets` (and the `-Vendors`, `-Bidders`, `-DBEs`, `-WorkTypes`, `-Counties`, `-Districts`, `-Subcontractors`, `-PlanHolders` family of 8 sister tables) are the agency's **saved analysis filters** for bid-trend queries. All 9 return **HTTP 500 on awdemo** — schema-only.
- `ProposalSnapshots` (frozen pre-let snapshots of a proposal — 7 fields in EDMX) returns **HTTP 403 on awdemo**.

---

### Prequalification

Prequalification is the set of per-person and per-vendor credentials that gate who can bid on what, inspect what, and sign off on what tests. Awdemo splits them into eight separate entity types by discipline (not by one `Qualification` table):

| Entity | Count on awdemo | Purpose |
|---|---|---|
| `Qualifications` | 30 | **Master catalog** of named qualifications (`'ACI-L1SAMPLING'`, `'ACI-L1TESTING'`, …) with Category / Level / Method / Type / Authority |
| `QualificationTests` | — | Links a Qualification to the MaterialTests it covers |
| `TestingQualifications` | 200 | Person × Qualification: who is testing-qualified (Status, Effective, Expiration) |
| `SamplingQualifications` | 108 | Person × Qualification: sampling |
| `LabTestingQualifications` | — | Lab × Qualification: which lab is approved for which test type |
| `LabSamplingQualifications` | — | Lab × Qualification: lab sampling |
| `WelderQualifications` | 3 | Welder-specific: Position, Process, SampleName, electrode info |
| `MaterialSamplingQualifications` | — | Material-specific sampling cert |
| `MaterialCategorySamplingQualifications` | — | Material-category-wide sampling cert |
| `StormwaterInspectorQualifications` | 2 | Stormwater inspector cert |
| `TestEquipmentQualifications` | — | Equipment calibration status |
| `CalibratingQualifications` | — | Who is qualified to calibrate equipment |

Each **-Qualifications** association entity carries the usual `EffectiveDate`, `ExpirationDate`, `Active`, `Status` + a PersonId / LabId / etc. Each has a sibling `-Remarks` table for free-form notes against a specific credential.

#### Qualification — scalar fields

| Field | Notes |
|---|---|
| `Id`, `Name`, `Description` | |
| `Category` | `'Sampling'`, `'Testing'`, ... |
| `Level` | `'Q1'`, `'Q2'`, agency-defined |
| `Method` | `'CERT'`, `'TEST'`, agency-defined |
| `Type` | `'CERT'`, `'BOTH'`, agency-defined |
| `Authority` | Issuing body (`'CA'`, `'ACI'`, `'AASHTO'`) |
| `EffectiveDate`, `Active`, `Status` | Lifecycle |

#### Example — "What's John qualified to do?"

```http
GET /TestingQualifications?$filter=PersonId eq 932 and Active eq true
                           &$expand=Qualification($select=Id,Name,Description,Category,Level)
```

#### Awdemo gotchas

- **No vendor-level `Prequalification` table** — vendor prequalification for *bidding* is implicit via `ProposalVendor.ValidForBidding` and the required `Proposal.ContractQual1/2/3` codes. The agency maintains the vendor-cert data elsewhere (document-managed) and this flag is set during pre-let validation. Person-level and lab-level prequalification *is* in this schema.
- **`DbeWorkTypes` is empty on awdemo**. The `BhpWorkTypes` (8 rows), `PPWorkTypes` (1 row), and `ContractApprGoodFaithEffortWorkTypes` / `ContractCurrGoodFaithEffortWorkTypes` tables wire *work-type codes* into bid-history profiles and good-faith DBE compliance, but the full prequalification-by-work-type matrix isn't exposed as its own table in awdemo.

---

### Bonds

Awdemo exposes bonds through two paths — a **required-at-bid** amount, and the **surety parties** attached to each bid:

1. **`Proposal.BIDBOND`** (Decimal) — the required bid-bond amount at letting (e.g. $25,000 for Whiteoak Bridge). Also mirrored on `Contract.BIDBOND`.
2. **`ProposalVendor.SuretyCompanyId` + `.SuretyAgentId`** (both → RefVendor) — the actual surety the bidder provided. These are RefVendor records of vendor-type Surety / SuretyAgent (there's no separate `SuretyCompany` entity).

Performance bonds and payment bonds (the post-award bonds) are not separately modeled in awdemo — they live in the document-management layer attached to the Contract.

#### Awdemo gotchas

- **`SuretyCompanies` and `SuretyAgents` entity sets return 404** — no separate tables; use `/RefVendors?$filter=Id in (…)` with the two IDs from ProposalVendor.
- `RefVendorInsurances` (nav from Proposal) is where **insurance-certificate snapshots** live — they're per-proposal (what the agency has on file for the prime at bid time), not per-contract.

---

### Bid-history engine (price intelligence)

This is one of the most powerful subsystems in AMS and often invisible to users of the UI. It's how the agency's engineer-estimate tooling knows *"the historical average price per cubic yard of concrete for a bridge-reconstruction project in District 3 over the past 24 months is X"*.

#### Entity chain

```
BidHistoryProfile (1)  — a named profile that defines the recipe:
    │ Name='BHP_3Yr_mod', Type='Item', ProposalsUsed='Awarded and Rejected',
    │ SourceOfBids='Low Bids', NumberOfMonths=24, NumberOfLowBidders=3,
    │ MinimumObsNumAvg=10, MinimumObsNumReg=20, Regression=true, MarketAreaInd=true, ...
    │ ProposalFilterClause: an XML <FilterCriteria> snippet applied to proposals
    │
    ├─→* BhpWorkType                — which work types this profile covers (BCON, BREH, ...)
    │
    ├─→* BidHistory                 — one per (profile × RefItem × work-type context) rollup
    │       │ AvgCount, AvgPrice, AvgStdDev, AvgLowQuantity, AvgHighQuantity,
    │       │ RegCount, RegRmse, RegIntercept, RegBetaLogQuantity, RegPrice, RegDev95,
    │       │ MinDate, MaxDate (as serial dates)
    │       │
    │       └─→* BidHistoryItem     — raw bids that fed the rollup
    │              │ BidId → Bid, Quantity, Price, PriceDate, Area, Rank, SeasonId, Total
    │
    └─ feeds engineer's estimate for new proposals via CostEstimateItemBidBasedTask:
        CostEstimateItemBidBasedTask → CostEstimateItem → (eventually) ProposalItem.UnitPrice
```

#### Dataset in awdemo

| Set | Count | Interpretation |
|---|---|---|
| `BidHistoryProfiles` | 209 | Multiple named recipes — three-year, by district, by work type, etc. |
| `BidHistories` | 49,877 | ~250 rollups per profile |
| `BidHistoryItems` | 1,556,902 | Raw bid rows that fed the regressions |
| `CostEstimateItemBidBasedTasks` | 450 | Per-estimate-item tasks that produce a bid-based price |
| `RefItemBidBasedTasks` | 5,266 | Per-catalog-item default bid-based price tasks |
| `BhpWorkTypes` | 8 | Work-type scoping on profiles |

#### Example — a BidHistory row for item 3380

```json
{
  "Id": 9, "BidHistoryProfileId": 1, "RefItemId": 3380,
  "AvgCount": 118,    "AvgPrice": 10.62463,  "AvgStdDev": 1.77912,
  "AvgLowQuantity": 2670.0, "AvgHighQuantity": 11754.0,
  "AvgComment": "Average price based on quantity level from 2670.000 to 11754.000.",
  "RegCount": 565,    "RegPrice": 14.06035,  "RegDev95": 6.20259,
  "RegIntercept": 3.7009340193, "RegBetaLogQuantity": -0.1241694843,
  "RegComment": "Regression price based on quantity and work type.",
  "MinQuantity": 1.0, "MaxQuantity": 34720.0,
  "MinDate": 4024.0, "MaxDate": 4962.0,     // serial-date (days since epoch)
  "Season": true, "MarketAreaInd": true, "Regression": true
}
```

The `AvgPrice` is a trimmed mean (10%/10% outlier exclusion per the profile); the `RegPrice` is a log-linear regression fitted on quantity, work-type, date, season, market area. This is what powers "price intelligence" features in a bidding UI.

#### Awdemo gotchas

- `BidHistoryProfile.ProposalFilterClause` is an **XML-encoded filter clause** (a tiny DSL for CallOrder, dates, work types). Treat it as opaque unless you intend to re-implement the filter.
- `MinDate` / `MaxDate` are **serial dates** (days since an epoch), not DateTimeOffset — a 4-digit integer in the 4000s is ~2011–2013. Convert with care.
- `BidClasses` and `BidBasedWorksheets` entity sets exist in schema but return 0 rows — unused in this instance.

---

### UI query recipes

Copy-paste-ready OData queries sized for real interfaces. Every recipe below has been verified against awdemo.

#### 1. Upcoming lettings calendar

**UI:** Dashboard tile listing lettings in the next 90 days, grouped by month, click to drill into proposals.

```http
GET /Lettings?$filter=LettingDate ge 2026-09-30 and LettingDate le 2026-12-29
             &$orderby=LettingDate,LettingTime
             &$expand=Proposals($select=Id,Name,ContractName,ProposalItemTotal,
                                       PrimaryRefCountyId,PrimaryRefDistrictId,
                                       ContractWorkType,BIDBOND,DbeGoalPercent;
                                $filter=Rejected eq false)
             &$select=Id,Name,LettingDate,LettingTime,LettingStatus,
                      LETTINGLOCATION,LETTINGADDRESS
```

**Shape:** array of lettings, each with inline Proposals.
**Perf:** cheap — 1 query, bounded by the date window.
**Notes:** group client-side by `LettingDate` month; add `$top=50` if an agency has crowded calendars.

#### 2. Bid tab for a single letting (matrixed)

**UI:** The classic bid-tabulation page — every bidder is a column, every proposal item is a row, cells are unit prices. One query to pull everything, pivot client-side.

```http
# Step 1: the proposal items (rows)
GET /ProposalItems?$filter=ProposalId eq 3664
                  &$orderby=ProposalItemLineNumber
                  &$expand=RefItem($select=Id,Description,UnitOfMeasure)
                  &$select=Id,ProposalItemLineNumber,RefItemId,Quantity,UnitPrice,
                           ExtendedAmount,AverageBidUnitPrice,SpecBook,SupplementalDescription

# Step 2: the bidders (columns), ranked
GET /ProposalVendors?$filter=ProposalId eq 3664 and ValidBid eq true
                     &$orderby=VendorRanking
                     &$expand=RefVendor($select=Id,Name,LongName)
                     &$select=Id,RefVendorId,BidTotal,VendorRanking,Awarded

# Step 3: every bid cell for this proposal
GET /Bids?$filter=ProposalItem/ProposalId eq 3664
         &$select=Id,ProposalVendorId,ProposalItemId,BidPrice,ExtendedAmount,LowCostFlag
         &$top=5000
```

**Shape:** three arrays, pivot in the client: `cell = bids.find(b => b.ProposalVendorId === pv.Id && b.ProposalItemId === item.Id)`.
**Perf:** item count × bidder count can be large — Whiteoak Bridge is 50 × 1 (= 50 bids), Proposal 3664 is 50 × 11 (= 550 bids). For 100-item 20-bidder lettings, 2,000 Bid rows; still 1 query. The `$filter=ProposalItem/ProposalId eq X` nested-filter is server-side; alternative: pass `$filter=ProposalVendorId in (…)` using the IDs from step 2.
**Highlight:** red/green per cell based on `(BidPrice - ProposalItem.UnitPrice) / UnitPrice` to show over/under engineer's estimate.

#### 3. Apparent-low summary with over/under estimate

**UI:** The "who won and by how much" summary card for a proposal.

```http
GET /ProposalVendors?$filter=ProposalId eq 3664 and ValidBid eq true
                     &$orderby=VendorRanking
                     &$expand=RefVendor($select=Id,Name,LongName,ShortName),
                              Proposal($select=Id,Name,ProposalItemTotal,AwardedAmount)
                     &$select=Id,RefVendorId,BidTotal,VendorBidItemTotal,VendorTotalBid,
                              VendorRanking,Awarded,SuretyCompanyId,SuretyAgentId
```

**Client math:**
- `pctOverEstimate = (BidTotal - proposal.ProposalItemTotal) / proposal.ProposalItemTotal * 100`
- `gapToSecondLow = (rank2.BidTotal - rank1.BidTotal) / rank2.BidTotal * 100`

**Example render for Proposal 3664:**

```
Rank 1  Vendor 2040  $331,704.51  (-13.65% under estimate)   ← AWARDED
Rank 2  Vendor 6423  $355,818.09  (-7.37% under estimate)    (+7.3% vs low)
Rank 3  Vendor 187   $374,438.00  (-2.52% under estimate)    (+12.9% vs low)
Rank 4  Vendor 8412  $375,949.20  (-2.13% under estimate)    (+13.3% vs low)
Rank 5  Vendor 7219  $381,168.00  (-0.78% under estimate)    (+14.9% vs low)
Rank 6  Vendor 1     $423,513.75  (+10.23% over estimate)    (+27.7% vs low)
Engineer's estimate: $384,124.75
```

#### 4. Historical bid prices for a RefItem (price intelligence)

**UI:** "What have people bid for item code 20201 (silt fence) in the last 24 months?" A sparkline chart of per-letting unit prices.

```http
# All proposal items for this RefItem in last 24 months, with their winning bids
GET /ProposalItems?$filter=RefItemId eq 14027 and Proposal/Letting/LettingDate ge 2024-09-30
                  &$expand=Proposal($select=Id,Name,LettingId,PrimaryRefDistrictId,
                                           PrimaryRefCountyId,ContractWorkType;
                                   $expand=Letting($select=Id,LettingDate))
                  &$select=Id,Quantity,UnitPrice,ExtendedAmount,AverageBidUnitPrice
                  &$top=500
```

For the actual **winning bid price** at each letting (not the engineer's estimate):

```http
# Join through to the winning ProposalVendor's Bid on this item
GET /Bids?$filter=ProposalItem/RefItemId eq 14027
                 and ProposalVendor/Awarded eq true
                 and ProposalItem/Proposal/Letting/LettingDate ge 2024-09-30
         &$expand=ProposalItem($select=Quantity;$expand=Proposal($select=Id,Name,LettingId;
                                                                $expand=Letting($select=Id,LettingDate))),
                  ProposalVendor($select=Id,RefVendorId)
         &$select=Id,BidPrice,ExtendedAmount
```

**Perf:** server-side `ProposalItem/RefItemId` and `ProposalVendor/Awarded` navigation filters work; `$top` is key — a popular item (asphalt pavement) might have thousands of hits per year. Fast path: use the pre-aggregated **`BidHistories`** table.

#### 5. Bid-history profile lookup (pre-aggregated)

**UI:** "Engineer's estimate preview" — before you write a UnitPrice into a ProposalItem, show the historical rollup from the BidHistoryProfile.

```http
GET /BidHistories?$filter=RefItemId eq 14027 and BidHistoryProfileId eq 1
                 &$select=Id,AvgCount,AvgPrice,AvgStdDev,AvgLowQuantity,AvgHighQuantity,
                          RegCount,RegPrice,RegRmse,RegDev95,
                          MinQuantity,MaxQuantity
```

For the raw bids that fed it:

```http
GET /BidHistoryItems?$filter=BidHistoryId eq 9
                    &$orderby=PriceDate desc
                    &$top=100
                    &$select=Id,Quantity,Price,Total,PriceDate,Area,Rank,SeasonId
```

**Shape:** returns both `AvgPrice` (trimmed mean) and `RegPrice` (regression). UI usually shows AvgPrice ± StdDev as the "band" and RegPrice as the "predicted" line.

#### 6. Addenda feed for a proposal

**UI:** The "updates" tab on a public proposal page.

```http
GET /Addendums?$filter=ProposalId eq 10849
              &$orderby=AddendumNumber
              &$select=Id,AddendumNumber,Description,DateCreated,DateApproved,DateClosed,Comments
```

**Perf:** trivial — rarely more than a dozen addendums per proposal.
**Pair with:** a RefreshDate timestamp so clients can poll `?$filter=... and DateApproved gt lastSeen`.

#### 7. Vendor's bidding history (participation leaderboard)

**UI:** "How many lettings has Vendor 160 bid on in the last 12 months, won how many, averaged what rank?"

```http
GET /ProposalVendors?$filter=RefVendorId eq 160
                              and Proposal/Letting/LettingDate ge 2025-09-30
                     &$expand=Proposal($select=Id,Name,LettingId,ProposalItemTotal;
                                      $expand=Letting($select=Id,LettingDate))
                     &$select=Id,BidTotal,VendorRanking,Awarded,ValidBid
                     &$top=500
```

**Client math:** group by letting-month; aggregate `count(Awarded)`, `avg(VendorRanking)`, `sum(BidTotal where Awarded=true)`.

#### 8. Reverse-lookup: contract → originating proposal

**UI:** On a Contract detail page, link back to the Proposal and Letting it came from.

```http
GET /Proposals?$filter=ContractId eq 282
              &$expand=Letting($select=Id,Name,LettingDate,LettingStatus),
                       AwardedVendor($select=Id,Name,LongName)
              &$select=Id,Name,ContractName,ProposalItemTotal,AwardedAmount,
                       AwardedVendorId,PublicationDate,PassedToConstruction,
                       TransitionToCRLMSConst_Dt,BIDBOND,DbeGoalPercent
```

**Perf:** 1 query. Awarded proposals are ~indexed on `ContractId`.

#### 9. Prebid "warnings" feed for a vendor

**UI:** For a bidder who's loaded their bid, show the validation messages (bid-item total mismatches, invalid alternate selections, missing time entries).

```http
GET /ProposalVendorMsgs?$filter=ProposalVendorId in (…)
                        &$orderby=Id desc
                        &$select=Id,ProposalVendorId,Type,Text,ModelName,ModelId
```

Example row from awdemo:

```json
{
  "Id": 82907, "ProposalVendorId": 63729, "Type": "Warning",
  "Text": "Proposal ID '82609-86129r', Vendor ID '00458': Incomplete Bid - Proposal bid total loaded with no bid items or bid time.",
  "ModelId": 63729, "ModelName": "ProposalVendor"
}
```

**Perf:** 486 total rows across all history. Filter by vendor + proposal to narrow to ~5–20 messages per bid envelope.

#### 10. "Who's prequalified to do X" lookup

**UI:** Agency staff needs to find all persons certified to perform concrete testing.

```http
# Who holds ACI Level 1 Testing (Qualification Id = 2)?
GET /TestingQualifications?$filter=QualificationId eq 2
                                   and Active eq true
                                   and Status eq 'ACTIVE'
                           &$select=Id,PersonId,EffectiveDate,ExpirationDate

# All currently-active testing qualifications for a specific person
GET /TestingQualifications?$filter=PersonId eq 932
                                   and Active eq true
                                   and (ExpirationDate eq null or ExpirationDate gt 2026-09-30)
                           &$expand=Qualification($select=Id,Name,Description,Category,Level,Authority)
                           &$select=Id,EffectiveDate,ExpirationDate
```

**Perf:** 200 TestingQualification rows total — trivial. `PersonInfos` is 403 on awdemo, so you can't resolve the PersonId to a name via a direct query — surface just the ID or join via an entity (DWR, SampleRecord) that already carries person detail.

#### 11. Letting summary dashboard (next-letting prep view)

**UI:** The night before a letting — one page with: lettings today/tomorrow, each proposal in each letting, each proposal's current plan-holder count, bid-bond amount, DBE goal, and whether addenda were issued.

```http
GET /Lettings?$filter=LettingDate ge 2026-09-30 and LettingDate le 2026-10-07
             &$orderby=LettingDate,LettingTime
             &$expand=Proposals(
                 $select=Id,Name,ContractName,CallOrder,ProposalItemTotal,BIDBOND,
                         DbeGoalPercent,ContractWorkType,PrimaryRefCountyId;
                 $expand=ProposalVendors($select=Id;$filter=OnPlanholderList eq true;$top=0;$count=true),
                         Addendums($select=Id,AddendumNumber,Description,DateApproved;$orderby=AddendumNumber desc)
               )
```

**Shape:** letting → proposal with `ProposalVendors@odata.count` (plan-holder count) + inline Addendums.
**Perf:** one call per letting-window; the `$count=true` with `$top=0` is a plan-holder count without pulling rows.

#### 12. Section-level bid comparison

**UI:** "Who was lowest on the Road Work section vs the Bridge section?"

```http
GET /BidSections?$filter=ProposalVendor/ProposalId eq 10849
                &$expand=ProposalVendor($select=Id,RefVendorId,VendorRanking),
                         ProposalSection($select=Id,Name,Description,ProposalSectionTotal)
                &$orderby=ProposalSectionName,SectionTotal
                &$select=Id,ProposalSectionName,SectionTotal,CalculatedSectionTotal,
                         LowCostFlag,SectionTotalMismatch
```

**Shape:** pivot client-side to `{section: [{vendor, total, lowCostFlag}]}`.
**Use case:** detect **unbalanced bidding** — a vendor low on one section and high on another, hoping the high-section quantities get over-run during execution.

#### 13. "Who bid days" — time-charge comparison

**UI:** A+B bid analysis (A = dollars, B = days × daily user cost).

```http
GET /BidTimes?$filter=ProposalVendor/ProposalId eq 10849
             &$expand=ProposalVendor($select=Id,RefVendorId,VendorRanking,BidTotal),
                      ProposalTime($select=Id,Name,Description,MilestoneType,
                                          RoadCostPerTimeUnit,LiquidDamageRate)
             &$orderby=ProposalTimeName,NumberOfTimeUnitsBid
```

**Client math:** `A+B score = BidTotal + sum(BidTime.CalculatedAmount)` per vendor; re-rank.

---

### Cross-flow interactions

How procurement flows feed into (and are informed by) the post-award world covered in `docs/ams-business-flows-2026-09-30.md`:

#### 1. Proposal → Contract backlink

- At award, `Proposal.ContractId` is written to point at the new Contract.
- `Contract.ContractProposalName` mirrors `Proposal.ContractName`.
- `Contract.ProposalType = 'LET'` identifies it as a let-and-bid origin.
- There is **no** `Contract.ProposalId` field — the backlink is one-way (Proposal knows its Contract; Contract doesn't know its Proposal). To traverse Contract → Proposal, query `/Proposals?$filter=ContractId eq {id}`.
- `Proposal.TransitionToCRLMSConst_Dt` marks the hand-off into the Construction & Materials system (the DWR/payment/materials world). After this timestamp, operational changes happen on the Contract side, not the Proposal side.

#### 2. ProposalItem → ContractItem → ContractProjectItem

- When a proposal is awarded, each `ProposalItem` becomes a `ContractItem` (with the winning bid's UnitPrice replacing the engineer's estimate price).
- `ContractItem` records are then distributed across projects as `ContractProjectItem` rows (the per-project quantity split).
- From the materials-flow side (companion doc), these ContractProjectItems are what DwrWorkItem postings reference.
- The engineer's estimate `ProposalItem.UnitPrice` and `AverageBidUnitPrice` can be preserved alongside the awarded unit price for post-award variance analysis.

#### 3. Bids → BidHistoryItems → future engineer's estimates

- Every row in the 3.19M-row `Bids` table is a candidate input to **`BidHistory`** rollups via `BidHistoryItem`.
- `BidHistoryProfile.ProposalsUsed` (e.g. `'Awarded and Rejected Proposals'`) and `SourceOfBids` (e.g. `'Low Bids'`) control which bids get aggregated.
- The resulting `BidHistories` feed `CostEstimateItemBidBasedTask` / `RefItemBidBasedTask` → `CostEstimateItem.UnitPrice`, which eventually populates a future `ProposalItem.UnitPrice` — closing the loop. **Today's winning bids become tomorrow's engineer's estimates.**

#### 4. ProposalTime → ContractTime

- Each `ProposalTime` (a schedule bid milestone) becomes a `ContractTime` on award, carrying the winning vendor's `BidTime.NumberOfTimeUnitsBid` as the `ContractTime.AllowableDays`.
- Liquidated damages (`ProposalTime.LiquidDamageRate`) carry over.
- Post-award, `DwrContractTimes` charges days against those contract times (companion doc section on contract-time charges).

#### 5. BIDBOND → performance bond → DWRContractor surety

- `Proposal.BIDBOND` is the required bid-bond amount; the vendor provides it with `ProposalVendor.SuretyCompanyId` / `SuretyAgentId`.
- On award, the Contract carries forward `Contract.BIDBOND` and the vendor must provide a **performance bond** (not separately modeled in this schema — handled via document management).
- The companion doc shows contract 282's bid-bond requirement ($25,000) and that the awarded vendor's surety info persists through to execution.

#### 6. ProposalSBPGoals → DBE execution tracking

- `ProposalSBPGoal` sets the DBE participation goal at letting time (percent + certification type).
- Post-award, this cascades into contract-execution tracking tables (DbeCommitments, DbeCommitmentWorkTypes, ContractApprGoodFaithEffortWorkTypes, ContractCurrGoodFaithEffortWorkTypes), which the companion doc covers.

#### 7. CostEstimate (pre-let) → Proposal.ProposalItemTotal

- Internal cost estimates (`CostEstimate`, `CostEstimateItem`) are built before publication; their line totals are what populate `ProposalItem.UnitPrice` at proposal creation. 3,900 CostEstimateItems in awdemo. Agencies often version these (multiple estimates per proposal; the final one wins).

---

### Awdemo gotchas (full list)

#### Entity sets that error

| Set | Error | Workaround |
|---|---|---|
| `Bidders` | HTTP 500 | Use `ProposalVendors?$filter=OnPlanholderList eq true` to list vendors who requested bid docs on a specific proposal |
| `ProposalSelectionSets` + 8 sister tables | HTTP 500 | Schema-only; agency's saved analysis filters are not exposed |
| `ProposalVendorSBPCommitments` | HTTP 500 | Schema has it, data isn't exposed |
| `QuoterProposals` / `QuoterProposalItems` | HTTP 500 | AWP Expedite Quoter (vendor-side quoting) data isn't exposed in the lab |
| `ProposalSnapshots` | HTTP 403 | Not accessible — immutable snapshots of pre-let proposals |
| `SuretyCompanies` / `SuretyAgents` | HTTP 404 | No separate entity — sureties are `RefVendor` rows; use `/RefVendors?$filter=Id in (…)` |

#### Empty tables (schema-only)

| Set | Count | Note |
|---|---|---|
| `BidClasses` | 0 | Legacy bid-classification table |
| `BidBasedWorksheets` | 0 | Agency-defined bid-based pricing worksheets |
| `DbeWorkTypes` | 0 | DBE work-type catalog is empty |

#### Naming inconsistencies

- `Addendum` → entity set `/Addendums` (not `/Addenda`)
- `ProposalVendorMsg` → entity set `/ProposalVendorMsgs`
- `ProposalVendorSBPCommitmentSummary` → `/ProposalVendorSBPCommitmentSummaries`
- `ProposalSelectionSetBidder` → `/ProposalSelectionSetBidders` (one of the 500-ing sets)
- `CalibratingQualification` and `-Remark` versions use British `-ing` spelling; otherwise consistent

#### Legacy soft columns

Any field beginning with `PR*`, `LP*`, `BL*`, `AD*`, `SNUM*`, `STM*`, `SDT*`, `SLST*`, `SNUM*`, `BIDBOND`, `DBEGOAL`, `SETASIDE`, `SUPPSPECBOOK`, `CONTRACTALTERNATE_NM*` is an **agency-mappable soft column** from the Trns·port legacy. Semantics vary across deployments; always confirm against local metadata before building UI around them.

#### Reads that look empty but aren't

- `ProposalVendor.VendorRanking = null` for most ProposalVendors on a proposal with 11 plan-holders but only 6 valid bids — treat null as "did not place" (never submitted or invalidated), not a tie. The 6 ranks only go 1–6.
- `Proposal.AwardedVendorId = null` after letting could mean "no acceptable bids" or "pending award decision" — check `Proposal.Rejected`, `ProposalStatus`, and `PassedToConstruction` together to disambiguate.

#### Field-type surprises

- `Letting.LettingTime` is **String**, not a time scalar (`'9:00 AM'`, `'09:00'`, `'0900'`).
- `Addendum.AddendumNumber` is **Int32** (not padded string like line numbers).
- `ProposalItem.ProposalItemLineNumber` is **String** (zero-padded, e.g. `'0010'`).
- `BidHistory.MinDate` / `MaxDate` are **Decimal serial dates** (days since epoch), not DateTimeOffset.

---

### Deferred / unverified

#### Mentioned in the AMS vendor reference guide but not in awdemo metadata

- `Letting` → `LettingProposal` / `LettingVendor` association tables — these don't exist in the awdemo EDMX; the relationships are modeled as direct one-to-many (via `Proposal.LettingId`) or 500-blocked (`Bidder`).
- `BidTotal` as a standalone entity — the vendor guide mentions it, but there's no `BidTotals` entity set; the totals are fields on `ProposalVendor`.
- Separate `BidBond` / `PerformanceBond` entities — not modeled; `BIDBOND` is a Proposal/Contract scalar, and the actual bond document lives in attachments.

#### Entities present in awdemo but not detailed here (deferred)

- `ProposalVendorSBPCommitmentRevision` / `ProposalVendorSBPCommitmentSummary` (SBP = Small Business Program) — the 500 blocking makes these untestable in the lab.
- `ProposalAgencyView` (11 fields, 2 navs) — AgencyView-scoped visibility of a proposal; 1 sample row shown; depends on the AgencyViews system (not covered).
- `ItemSelectionSetItemProposal` — item-selection-set membership; used by the bid-based estimation pipeline.
- `DocumentSubmissionReview` — submission-review workflow linked to a `DocumentSubmission`.

#### To explore in a follow-up pass

- The full `Qualification` × `MaterialTest` × `TestEquipmentQualification` chain for test-equipment calibration (relevant to materials-flow verification).
- `ContractApprGoodFaithEffortWorkType` / `ContractCurrGoodFaithEffortWorkType` — DBE good-faith-effort rollups post-award (bridges this doc to the companion).
- The `Quoter` → `Quoters` / `QuoterProposal` / `QuoterProposalItem` chain (500 on awdemo) — vendor-side electronic bid submission (AWP Expedite).
- `WorkflowPhase` as a cross-cutting lifecycle marker — Letting, Proposal, ProposalVendor, Bidder all carry WorkflowPhaseId; the full phase catalog and transitions would merit its own small doc.

---

---

---

<a id="part-5-labor-financials-items-materials"></a>

# Part 5 — Labor, financials, items & materials

_The three core execution flows: who worked and for how long, every dollar in and out, and the planned-vs-actual-vs-tested chain of work items and materials._

Reference walkthrough of the three business flows that actually matter for every working day of a construction contract, grounded in live queries against the `ams-lab/awdemo` instance and validated against `refs/awdemo_metadata.xml`. Every field name, cardinality, filter path, and example number in this document was pulled from the live API or the EDMX schema — none of it is paraphrased from the vendor reference guide (`refs/reference-ams-guide-v2-2026-09-30.md`), which has drifted significantly: it still calls fields `WorkDate`, `WeatherConditions`, `DWRItems`, `DWRLabor` that do not exist. Where the two disagree, the metadata wins.

The three flows mirror three real business questions:

1. **Labor hours** — who was on site today, in what trade, and for how long. The system of record is the DWR; compliance-side wage reporting shadows it via CertifiedPayroll (empty on awdemo).
2. **Financial transactions** — how the agency pays the prime, with retainage, incentives, time charges, change orders, claims, and the per-fund split.
3. **Items & materials flows** — the three-layer story of planned items (RefItem → ContractItem → ContractProjectItem), what crews actually posted today (DwrWorkItem → DwrItemPosting), and the QA/QC chain that validates the materials went in correctly (ContractProjectItemMaterialSet → DwrAcceptanceRecord → SampleRecord).

---

### Legend & conventions

| Shape | Meaning |
|---|---|
| **EntitySet** | Named plural — the OData collection URL. Example: `DailyWorkReports`. Sometimes irregular (`RefSampleStatuses`, not `RefSampleStatus`). |
| **Entity** | Singular type — the row shape. Example: `DailyWorkReport`. |
| `X.Y` in a `$filter` | Navigates a 1:1 nav from the current entity. Example: `DwrWorkItem/DailyWorkReport/ContractId eq 282`. |
| `in (…)` | OData v4 `in` list. Chunked at ~50 ids per request to avoid URL-length limits. |
| `$expand=A($expand=B($expand=C))` | Three-deep hydration in a single request. awdemo accepts this freely — see worked examples. |
| `null` fields | AMS marks most props `Nullable=true`. A null means "not entered on this record"; it never means "doesn't apply". The UI should treat `null` and `0` differently where it matters (e.g. `Hours = 0` vs `Hours = null`). |
| ID with `#` | A live id on awdemo at the time of writing. These persist across sessions. |

**Capitalization gotcha, universal:** AMS mixes `DWRxxx` and `DwrXxx` arbitrarily. The DWR-primary-entity set is `DailyWorkReports` (singular `DailyWorkReport`), but the back-references into it come in both flavors: `DWRContractor.DailyWorkReportId`, `DwrForceAccountContractor.DailyWorkReportId`, and the acceptance-record FK is `DwrAcceptanceRecord.DWRItemPostingId` (uppercase DWR, lowercase everywhere else). Treat each field name as sacred — the server will 400 on typos.

**Primary worked example throughout:** **Contract 282 — WHITEOAK BRIDGE**, a $1,204,969.10 bridge removal/replacement with one project (CP #169, "1205339", Alcona County), prime contractor **Carl Engineers Inc.** (RefVendor #160, `00153`), 13 DWRs on dates Aug 1 – Sep 3 2024 (ids 340–353), 11 payment estimates, 3 change orders, 1 claim with litigation.

---

### 1. Labor hours

#### Overview

Labor on a contract flows through three parallel channels. **Regular work** rides inside the DWR: each DWR gets one `DWRContractor` row per crew on site (hours worked + prime/sub flag), and each `DWRContractor` can carry a roster (`DWRContractorPersonnel`) of named trade classifications with per-class hours, plus a `DWRContractorStaff` list for supervisory time and a `DWRContractVendorEquipment` list that attributes equipment hours to that same crew-day. **Force-account work** (extra work billed by time & material instead of by contract item) uses a parallel chain rooted at `ForceAccount` → `ForceAccountContractor`, with daily labor and equipment postings going through `DwrForceAccountContractor` → `DwrForceAccountContractorLabor` / `DwrForceAccountContractorVendorEquipment`. **Compliance reporting** — the certified payroll required on federal-aid work — is its own tree rooted at `CertifiedPayroll` → `PayrollEmployee` → `PayrollEmployeeLabor` → `PayrollEmployeeLaborHour`, with wage rates tied back to `ConformanceWageDecision`/`RefWageDecision` through the project. On awdemo the DWR/force-account side is sparsely populated and the certified-payroll side is empty entirely.

#### Entity chain diagram

```
DailyWorkReport (1)
   │  "the day"
   ├── DWRContractor (N)                           ─────────  "who was on site"
   │        Hours, StartTime, EndTime, IsPrime
   │        │
   │        ├── DWRContractorPersonnel (N)         ─────────  "trade crew count × hours"
   │        │       → DecisionClass (1)   ("OEDZ – Dozer", federal craft code)
   │        │       → ReferencePersonnel (1), Employer (1)
   │        │
   │        ├── DWRContractorStaff (N)             ─────────  "supervisory time"
   │        │       → DecisionClass (1), Employer (1)
   │        │
   │        └── DWRContractVendorEquipment (N)     ─────────  "crew's equipment"
   │                HoursUsed, HoursIdle, NumberOnSite, NumberUsed
   │                → ContractVendorEquipment → VendorEquipment
   │                → ReferenceEquipment (catalog)
   │
   ├── DWRStaffRecord (N)                          ─────────  "state agency staff on site"
   │        RegularHours, OvertimeHours, WorkCode, Vehicle, mileage
   │        → PersonInfo (1) [403 on awdemo]
   │        → UserRole (1)
   │
   └── DwrForceAccountContractor (N)               ─────────  "force-account day"
            → ForceAccountContractor (1)
                 → ForceAccount (1)   → Contract (1)
                 → Contractor (1)     → RefVendor (1)
                 → ForceAccountContractorLabor (N)
                      hourly rates + fringe
                      → VendorPersonnel (1)
                 → ForceAccountContractorVendorEquipment (N)
                      hourly rates, idle rates, ownership type
                      → VendorEquipment (1)
            ├── DwrForceAccountContractorLabor (N)
            │       RegularHours, OvertimeHours, DoubleTimeHours
            │       → ForceAccountContractorLabor (1)
            ├── DwrForceAccountContractorVendorEquipment (N)
            │       StandardHours, IdleHours
            │       → ForceAccountContractorVendorEquipment (1)
            └── DwrForceAccountContractorMaterialInvoice (N)

CertifiedPayroll (N per contract per vendor per week)             [EMPTY on awdemo]
   PayrollNumber, BeginDate–EndDate, PrimeAcceptedDate, AgencyAcceptedDate
   → Contract (1), RefVendor (1)
   ├── PayrollEmployee (N)
   │      FirstName, LastName, Ssn, TotalHours, GrossPay, FringeBenefits, …
   │      → RefEmployee (1)
   │      └── PayrollEmployeeLabor (N)
   │             CraftCode, StraightTimeHours, OvertimeHours, GrossPay, rates,
   │             fringes, withholdings, RequiredCompensation vs DifferenceRequiredVsReported
   │             → ContractProject (1)
   │             → DecisionClass (1)   ("LaborClass")
   │             └── PayrollEmployeeLaborHour (N)   per-day hours
   │
   └── CertifiedPayrollException (N)
          → PayrollExceptionRule (1), ConformanceWageDecision (1)
```

#### Entities in the chain

##### `DailyWorkReport`

The anchor. 30 scalar props, 16 navigations.

| Prop | Type | Notes |
|---|---|---|
| `Id` | Int64 (key) | |
| `ContractId` | Int64 | parent contract |
| `DwrDate` | DateTimeOffset | **the field is `DwrDate`, not `WorkDate`** |
| `Sequence` | Int16 | 1-based within a day for the same inspector |
| `Status` | String | `Draft`, `Approved`, `Open`, … |
| `InspectorId`, `CreatorId`, `ApprovedById` | Int64 | all → `PersonInfo` — but see gotcha |
| `ApprovalDate` | DateTimeOffset | |
| `RefWeatherId` | Int64 | → `RefWeather` for the "Sunny / Partly Cloudy" label |
| `HighTemperature`, `LowTemperature` | Int16 | °F integers |
| `RainfallAmount` | Decimal | inches |
| `PaymentEstimateId` | Int64 | pay-estimate this DWR rolls into |
| `ApprovedByDiaryId` | Int64 | → `DailyDiary` (the diary record that approved this DWR) |
| `Paid`, `HasContractors`, `HasDailyStaff`, `HasWorkItems`, `HasAttachments`, `HasDwrNotes`, `HasStormwaterPeriod` | Boolean | summary flags populated by the server |

Important navs: `DWRContractors` [], `DWRStaffRecords` [], `DwrForceAccountContractors` [], `DwrWorkItems` [], `SampleRecords` [], `Remarks` [], `DwrNotes` [], `DwrContractTimes` [].

**Query template:**
```
GET /DailyWorkReports?$filter=ContractId eq {contractId}&$orderby=DwrDate desc
    &$select=Id,DwrDate,Status,Sequence,InspectorId,HasWorkItems,HasContractors,
             HighTemperature,LowTemperature,RainfallAmount,PaymentEstimateId,ApprovalDate
```

**Worked example — DWR #345 (2024-08-09, WHITEOAK BRIDGE):**

```
Id=345  DwrDate=2024-08-09  Status=Approved  Sequence=1
InspectorId=1609  CreatorId=1609  ApprovedById=1609  ApprovalDate=2024-09-04
RefWeatherId=4 (Sunny) HighTemp=null LowTemp=85°F  RainfallAmount=65.0
PaymentEstimateId=290  ApprovedByDiaryId=85
HasContractors=True  HasWorkItems=True  HasAttachments=True  Paid=True
```

##### `DWRContractor`

The crew-day row — one per contractor present on the DWR. 16 props, 6 navs.

| Prop | Type | Notes |
|---|---|---|
| `Id` | Int64 (key) | |
| `DailyWorkReportId` | Int64 | parent DWR |
| `ContractorId` | Int64 | → `Contractor`, which carries `RefVendorId` for the vendor name |
| `StartTime`, `EndTime` | DateTimeOffset | clock-in/out |
| `Hours` | Decimal | the hours bill |
| `IsPrime` | Boolean | |
| `HasEquipment`, `HasPersonnel`, `HasStaff` | Boolean | populated by server when child rows exist |
| `DbeCertified`, `PayrollNotRequired` | Boolean | compliance flags |

**Query template:**
```
GET /DWRContractors?$filter=DailyWorkReport/ContractId eq {contractId}
    &$expand=Contractor($expand=RefVendor($select=Id,LongName,ShortName,Name)),
             DWRContractorPersonnels($expand=DecisionClass),
             DWRContractorStaffs($expand=DecisionClass),
             DWRContractVendorEquipments($expand=ContractVendorEquipment,ReferenceEquipment)
```

**Worked example — DWRContractor #435 on DWR 340:**

```
Id=435  DwrId=340  ContractorId=521  IsPrime=True  Hours=8.0
StartTime=2024-08-01T09:38  EndTime=2024-08-01T17:38
HasPersonnel=True  HasEquipment=True  HasStaff=False
  → Contractor 521 (RefVendorId=160 — Carl Engineers Inc.)
```

##### `DWRContractorPersonnel`

The trade-crew roster line. 13 props, 5 navs.

| Prop | Type | Notes |
|---|---|---|
| `Id` | Int64 (key) | |
| `DWRContractorId` | Int64 | parent |
| `ContractVendorPersonnelId` | Int64 | → the vendor's roster record for this craft |
| `TotalHours` | Decimal | hours × count for this craft on this day |
| `Count` | Int64 | number of workers in this craft today |
| `DecisionClassId` | Int64 | → `DecisionClass` — the federal craft classification |
| `EmployerId`, `ReferencePersonnelId` | Int64 | mostly null on awdemo |

`DecisionClass` carries `Name` (short code like `OEDZ`), `Description` ("Dozer"), and `FedJobClassId`. These same decision classes are what `PayrollEmployeeLabor.LaborClassId` points at, giving you the one join that connects daily field hours to certified-payroll hours.

**Worked example — Personnel #136 on DWRContractor 435 (DWR 340):**

```
DWRContractorId=435  TotalHours=8.0  Count=1  DecisionClassId=35
  → DecisionClass 35: Name="OEDZ"  Description="Dozer"  FedJobClassId=4
```

One worker, operating engineer / dozer, 8 hours on 2024-08-01.

##### `DWRStaffRecord`

Agency staff (not contractor crews) that logged time on the project. 16 props, 3 navs.

| Prop | Type | Notes |
|---|---|---|
| `DailyWorkReportId` | Int64 | parent DWR |
| `PersonInfoId` | Int64 | **PersonInfos entity set is 403 on awdemo**, so you'll have the id but not the name |
| `UserRoleId` | Int64 | → `UserRole` for job role |
| `RegularHours`, `OvertimeHours` | Decimal | the hours bill |
| `WorkCode`, `StaffType` | String | agency work-code / staff-type codes |
| `Vehicle`, `StartingMileage`, `EndingMileage` | mixed | state-vehicle mileage, if applicable |
| `Comments` | String | free text |

Zero rows for DWR 345. 0 rows across all 13 DWRs on contract 282. Awdemo doesn't populate this.

##### `DwrForceAccountContractor` → `DwrForceAccountContractorLabor` / `…VendorEquipment`

Force account = extra work billed by hourly rate × hours instead of by contract-item unit × quantity. The chain is three layers:

**`DwrForceAccountContractor`** (7p / 5n): `DailyWorkReportId`, `ForceAccountContractorId`. Just a header saying "this contractor billed force-account hours on this DWR".

**`DwrForceAccountContractorLabor`** (10p / 2n): `DwrForceAccountContractorId`, `ForceAccountContractorLaborId`, `RegularHours`, `OvertimeHours`, `DoubleTimeHours`. These three Decimals are the whole bill.

**`DwrForceAccountContractorVendorEquipment`** (9p / 2n): `StandardHours`, `IdleHours`. Equipment side of the same posting.

The rates themselves live on `ForceAccountContractorLabor` (`RegularHourlyRate`, `OvertimeHourlyRate`, `DoubletimeHourlyRate`, `FringeAmount`) and `ForceAccountContractorVendorEquipment` (`StandardHourlyRate`, `IdleHourlyRate`, `OwnershipType`). So:

```
hourly_bill = Σ (DwrForceAccountContractorLabor.RegularHours × ForceAccountContractorLabor.RegularHourlyRate +
                 OvertimeHours × OvertimeHourlyRate +
                 DoubleTimeHours × DoubletimeHourlyRate +
                 FringeAmount per hour)
```

On awdemo contract 282: `ForceAccount` #11 ("FA One") exists, has 5 `ForceAccountContractor` rows globally, but **zero** `DwrForceAccountContractor` rows for DWR 345.

##### `CertifiedPayroll` → `PayrollEmployee` → `PayrollEmployeeLabor` → `PayrollEmployeeLaborHour`

The federal-aid compliance thread. 34 → 56 → 62 → 10 props deep.

| CertifiedPayroll key fields | Why |
|---|---|
| `ContractId`, `RefVendorId`, `PayrollNumber`, `ModificationNumber` | identifies the weekly submission from one vendor on one contract |
| `BeginDate`, `EndDate` | the payroll week |
| `SubmittalDate`, `PrimeAcceptedDate`, `AgencyAcceptedDate`, `AgencyOriginalNotAcceptedDate` | approval chain timestamps |
| `FringeBenefitPaymentType`, `PaperCopyOnFile`, `PayrollSigner` | compliance meta |
| `IsLatestModification` | one row per revision; this flag picks the current one |

`PayrollEmployee` carries name, SSN (actually populated), demographics, running `TotalHours` / `GrossPay` / `NetPay` / `TotalDeductions`.

`PayrollEmployeeLabor` is the per-project, per-craft breakdown with 62 fields: hourly rates, overtime hourly rate, fringe-rate pieces (`HealthWelfareRate`, `VacationHolidayRate`, `ApprenticeshipFundRate`, `PensionRate`, …), hour totals, computed `CalcGrossPay`, and critically `RequiredCompensation` vs `DifferenceRequiredVsReported` — the automated prevailing-wage shortfall check.

`PayrollEmployeeLaborHour` is per-day hours (`LaborHourDate`, `StraightTimeHours`, `OvertimeHours`).

**Query template** (if the data were there):
```
GET /CertifiedPayrolls?$filter=ContractId eq {contractId} and IsLatestModification eq true
    &$expand=RefVendor,PayrollEmployees($expand=PayrollEmployeeLabors(
             $expand=LaborClass,PayrollEmployeeLaborHours))
```

**Worked example — contract 282:** zero `CertifiedPayroll` rows. Awdemo has none on this contract.

##### `RefWageDecision` → `RefWageDecisionModification` → `ContractProjectWageDecision` / `ProjectWageDecision` / `ConformanceWageDecision`

The wage rates themselves.

`RefWageDecision` is the DOL wage decision document (`Name` like `NCDOJ2018`, `State`, `IssuingAuthority`, `WageConstructionType`, `DecisionDate`). Modifications hang off it.

`ContractProjectWageDecision` links a specific wage decision modification to a `ContractProject`. On contract 282, project 169 has CPWD #16 → RefWageDecision `NCDOJ2018` (State of NC, state-authority decision).

`ConformanceWageDecision` is a per-DecisionClass rate override on a specific `ContractProjectWageDecision` — the project-specific wage rate used when the DOL schedule doesn't publish one for that craft. 3 rows on awdemo total (`MGC_Conform_01` @ $12.00 + $2.00 fringe, `IWRF` Reinforcing @ $40.00 + $5.00 fringe).

#### How to roll it up

**"Total crew hours on contract 282, by craft, with equipment hours alongside":**

```python
# 1. All DWRContractors on the contract
contractors = client.get(
    "DWRContractors",
    filter="DailyWorkReport/ContractId eq 282",
    select="Id,DailyWorkReportId,ContractorId,Hours,IsPrime,HasPersonnel,HasEquipment",
    top=999,
)["value"]

# 2. Personnel breakdown (per-craft, per crew-day)
dwrcon_ids = [c["Id"] for c in contractors]
# chunk by 50 ids; _in syntax is `in (1,2,3,...)`
personnel = client.get(
    "DWRContractorPersonnels",
    filter=f"DWRContractorId in ({','.join(str(i) for i in dwrcon_ids)})",
    expand="DecisionClass($select=Id,Name,Description,FedJobClassId)",
    top=999,
)["value"]

# 3. Equipment breakdown
equipment = client.get(
    "DWRContractVendorEquipments",
    filter=f"DWRContractorId in ({','.join(str(i) for i in dwrcon_ids)})",
    expand="ContractVendorEquipment($select=Id,Name,Description)",
    top=999,
)["value"]

# 4. Group personnel by craft
by_craft = {}
for p in personnel:
    key = (p["DecisionClass"]["Name"], p["DecisionClass"]["Description"])
    by_craft.setdefault(key, {"hours": 0.0, "workers": 0})
    by_craft[key]["hours"] += p["TotalHours"] or 0
    by_craft[key]["workers"] += p["Count"] or 0
```

**Worked result on 282:** 13 DWRs, 15 crew-days (DWRContractors), two of them with personnel/equipment detail (DWRContractors #435 and #443). Craft "OEDZ – Dozer" has 1 worker × 8 hours (DWR 340); DWRContractor 435 also logged 8 truck hours (`Tr / Truck`, equipment #176).

#### Awdemo gotchas

- **`PersonInfos` entity set is 403.** You can't resolve `InspectorId`, `CreatorId`, `ApprovedById`, `DWRStaffRecord.PersonInfoId`, `SampleRecord.SamplerId` etc. to names via a top-level query, and inline `$expand=Inspector` fails with 403 too. You get IDs, not names, for all person references on awdemo. In prod, the same expand will work and you can drop the fallback.
- **`CertifiedPayroll`, `PayrollEmployee`, `PayrollEmployeeLabor`, `PayrollEmployeeLaborHour` are empty for contract 282** (and nearly all of awdemo). The entity sets exist and return 200 — just with `[]`. The entire certified-payroll chain is unverifiable against live data; the schema shape above is sourced from the EDMX only.
- **`DWRStaffRecords` is empty for every DWR on 282.** The agency-staff channel isn't populated.
- **`DwrForceAccountContractors` is empty for DWR 345.** `ForceAccount` #11 exists on contract 282 with 5 `ForceAccountContractor` rows, but no DWR has posted force-account time against it yet.
- **Field name is `DwrForceAccountContractor` (lowercase `wr`, nav collection `DwrForceAccountContractors`)** on the DWR side, but back-references and most entity-set names drop the capitalization pattern. Always verify in `refs/awdemo_metadata.xml` before adding a new filter.
- **`HasPersonnel`, `HasEquipment`, `HasStaff`** on `DWRContractor` are **server-maintained flags, not user input** — they flip to `True` when child rows exist and back to `False` when deleted. Trust them as a cheap filter (`$filter=HasPersonnel eq true`) before fetching the children.
- **`DecisionClass` entity set is named `DecisionClasses`.** The nav prop on `PayrollEmployeeLabor` is called `LaborClass` and *targets* `DecisionClass` — so you expand `$expand=LaborClass` but filter against `DecisionClasses`.

---

### 2. Financial transactions

#### Overview

Money moves through four entities-of-record on a construction contract. **The contract itself** carries the running totals (`AwardedContractAmount`, `CurrentContractAmount`, `AmountPaidToDate`, `AmountPostedToDate`, `PercentPaid`, `TotalNetChangeAmount`) that are the one-line answer to "how are we doing financially". **PaymentEstimate** is the periodic (usually monthly) bill: one row per billing period, with 96 scalar amount fields and 11 of them on contract 282 covering Aug 2024 through Sep 2024, each one broken down into `PaymentEstimateItem` rows (per-line-item quantity-installed × unit-price), `PaymentEstimateItemFund` splits (per-fund allocation), `PaymentEstimateApproval` chains, `ContractAdjustment` adjustments (retainage, time charges), `PayEstimateItemAdjustment` (stockpile adjustments, overrun adjustments, price-index adjustments). **ChangeOrder** modifies the contract's shape via `ChangeOrderIncDecItem` (quantity +/-), `ChangeOrderNewItem` (new line items), `ChangeOrderTimeAdjustment` (schedule shifts), and `ChangeOrderForceAccount` (new force-account authorization). **ContractClaim** is disputed money — a formal request for compensation outside the normal pay cycle, with its own `ContractClaimLitigation` and `ContractClaimChangeOrder` chains.

Underneath all of that: **funding** is the backing. `ContractFundPackage` groups the funds that pay for the contract (e.g. "State 95% / Alcona County 5%"), each with `ContractFund` rows carrying `Percentage`, `Type` (Federal/Non Federal), `CurrentAmountUsed`, `TotalAmountUsed`, and a pointer to the underlying `RefFund` ("State", "Alcona County"). Every `PaymentEstimateItem` splits into `PaymentEstimateItemFund` rows that charge the specific `ContractFund` for its share of that line's payment.

#### Entity chain diagram

```
Contract (1)
  AwardedContractAmount, CurrentContractAmount, AmountPaidToDate, AmountPostedToDate,
  PercentPaid, TotalNetChangeAmount, NetChangeAmountApproved, CalcTotalSubcontractAmount
  │
  ├── PaymentEstimate (N)                        ─────────  "monthly bill"
  │     EstimateNumber (seq 1,2,…), PeriodEndDate, CheckDate, CheckNumber
  │     CurrentItemPaidGrossAmount, TotalItemPaidGrossAmount
  │     CurrentCashRetainageAmount, TotalCashRetainageAmount
  │     CurrentIncentiveAmount, CurrentDisincentiveAmount, CurrentLiqDamageAmount
  │     CurrentNetAmountForRetainCalc, TotalNetAmountForRetainCalc
  │     CurrentPaidAmount, TotalPaidAmount   (gross − retainage − other)
  │     → PreviousPaymentEstimate (1)
  │     → Vendor → RefVendor (1)
  │     │
  │     ├── PaymentEstimateItem (N)             ─────────  "per-line pay"
  │     │     CurrentTotalInstalledQuantity, CurrentTotalPaidQuantity
  │     │     CurrentTotalInstalledAmount, CurrentTotalPaidAmount
  │     │     OverrunQuantity, DifferenceInCurrentlyInstalledPaidAmount
  │     │     → ContractProjectItem (1)
  │     │     │
  │     │     ├── PaymentEstimateItemFund (N)   ─────────  "per-fund split"
  │     │     │     CurrentAmountAllocated, PreviousTotalAmountAllocated
  │     │     │     → ContractFund (1)
  │     │     │
  │     │     └── PayEstimateItemAdjustment (N) ─────────  "stockpile / overrun / price adj"
  │     │           Type, Function, Amount, Quantity, UnitPrice, PriceAdjustment
  │     │           → Stockpile (1) when stockpile-driven
  │     │           → RefPriceIndexAdjustment (1) when price-index
  │     │
  │     ├── ContractAdjustment (N)              ─────────  "pay-period retainage/time charge"
  │     │     Type ("Retainage" | "Time Charge" | other), Amount, Rate, DistributionMethod
  │     │     → ContractTime (1) [when type = Time Charge]
  │     │     → ContractFundPackage (1)
  │     │     └── ContractAdjustmentFund (N)    ─────────  per-fund split of the adjustment
  │     │                                                   [N.B. 403 on awdemo direct]
  │     │
  │     ├── PaymentEstimateApproval (N)
  │     │     ApprovalLevel, ApprovalDate, ApprovalDecision
  │     │     → ApprovalLevelRole (Role), Approver (UserInfo)
  │     │
  │     ├── PaymentEstimateContractTimeCharge (N)
  │     │     ContractTimeId, CurrentTimeChargeUnits   ("13.0 days charged this period")
  │     │
  │     └── PaymentEstimateContractOtherAdjustmentType (N)
  │           Name, Current, Previous, Total
  │
  ├── ChangeOrder (N)                           ─────────  "scope change"
  │     Number, Amount, ApprovalDate, ChangeOrderDate, Status, Type, Reason
  │     TimeAdjustments, NewItems, IncreaseDecreaseItems, Unilateral
  │     PrevApprovedChangeOrderTotal
  │     │
  │     ├── ChangeOrderIncDecItem (N)           ─────────  "qty +/- to an existing line"
  │     │     Quantity (+/-), Amount (+/-)
  │     │     → ContractProjectItem (1)
  │     │
  │     ├── ChangeOrderNewItem (N)              ─────────  "net-new line added"
  │     │     ItemSource ("Original"|"CO"), NewItemType, Quantity, UnitPrice, ExtendedAmount
  │     │     → RefItem (1), ContractProjectItem (1), ContractProject (1)
  │     │
  │     ├── ChangeOrderTimeAdjustment (N)       ─────────  "schedule shift"
  │     │     AdjustmentTimeUnits, AdjustmentCompletionDate
  │     │     → ContractTime (1)
  │     │
  │     ├── ChangeOrderForceAccount (N)         ─────────  "new force-account auth"
  │     │     → ForceAccount (1)
  │     │
  │     ├── ChangeOrderExplanation (N)
  │     │     SupplementalExplanation, Order
  │     │     → RefChangeOrderExplanation (1)   (reason-code catalog)
  │     │
  │     └── ChangeOrderReviewer (N) / ChangeOrderApprovalGroup (N)
  │
  ├── ContractClaim (N)                         ─────────  "disputed money"
  │     ClaimNumber, Category, Status, AdditionalStatus
  │     RequestedAmount, PaymentAmount, RequestedDays, DaysGranted
  │     ReceivedDate, ResolutionDate, PaymentDate
  │     ClaimantName, DefendantName, CourtFileNumber, JudgeName
  │     → Subcontract (1), PaymentEstimate (1), RefContractClaimType (1)
  │     ├── ContractClaimLitigation (N)         ─────────  "the lawsuit"
  │     │     LitigationDate, LitigationAmount, NonLitigationAmount
  │     ├── ContractClaimChangeOrder (N)        ─────────  "resolution via CO"
  │     │     → ChangeOrder (1)
  │     └── AssociatedContractClaim (N)         ─────────  "linked claims"
  │
  ├── ContractFundPackage (N)                   ─────────  "where the money comes from"
  │     Name, Description
  │     └── ContractFund (N)
  │           Percentage, Type ("Federal"|"Non Federal"), Priority
  │           CurrentAmountUsed, PreviousAmountUsed, TotalAmountUsed
  │           Limit, RemainingAmount
  │           → RefFund (1)   ("State", "Alcona County", etc.)
  │
  ├── Stockpile (N)                             ─────────  "material staged for later use"
  │     ItemRecoveryPercentage, StockpileAmount
  │     CurrentItemAdjustmentAmount, TotalItemAdjustmentAmount
  │     Status, RecoveryDate
  │     → ContractItem (1)
  │
  └── ContractRetainage (1)                     ─────────  "the retainage ruleset"
       MaxPercentage, Percentage, TriggerPercentage, Base ("Award Amount"), Method

AccountTransaction / ContractSecurityAccount                [barely populated on awdemo]
```

#### Entities in the chain

##### `Contract` — financial rollup fields

Not an exhaustive list of 149 contract scalars; just the money ones.

| Prop | Type | Meaning |
|---|---|---|
| `AwardedContractAmount` | Decimal | the bid-award value |
| `CurrentContractAmount` | Decimal | AwardedContractAmount + Σ approved change orders |
| `AmountPostedToDate` | Decimal | gross value of all approved DWR postings (what has been earned) |
| `AmountPaidToDate` | Decimal | net cash paid (gross − retainage − deductions) |
| `AmountPostedApprovedToDateAllItems` | Decimal | same as `AmountPostedToDate` but filtered to approved DWRs only |
| `PercentPaid`, `PercentCompleteAward` | Decimal | server-computed, in whole percentage units (`95.01` = 95.01 %) |
| `TotalNetChangeAmount`, `NetChangeAmountApproved`, `NetChangeAmountPending` | Decimal | the three change-order roll-ups |
| `TotalNetChangePercentage`, `NetChangePercentageApproved`, `NetChangePercentagePending` | Decimal | ditto as % of award |
| `CalcTotalSubcontractAmount`, `CalcSpecialtySubcontractedAmount`, `CalcSpecialtySubcontractedPercent` | Decimal | subcontracting rollup |
| `CalcTowardsAmountThreshold`, `CalcTowardsPercentThreshold` | Decimal | threshold-tracking against `SubcontractMaxAmount` / `SubcontractPercentageThreshold` |
| `IncentiveCapAmount`, `DisincentiveCapAmount` | Decimal | optional caps |

**Worked example — contract 282:**

```
AwardedContractAmount:          $1,204,969.10
CurrentContractAmount:          $1,207,358.16   (award + $389.06 net change)
AmountPostedToDate:             $1,207,358.16
AmountPaidToDate:               $1,147,109.70   (net of $60,248.46 retainage)
PercentPaid:                           95.01 %
NetChangeAmountApproved:              $389.06
TotalNetChangePercentage:               0.03 %
CalcTotalSubcontractAmount:        $62,756.56
```

##### `PaymentEstimate` — the monthly bill

96 scalar fields. Only the ones you'll actually use day to day:

| Prop | Type | Meaning |
|---|---|---|
| `Id` | Int64 | |
| `ContractId` | Int64 | parent |
| `PreviousPaymentEstimateId` | Int64 | → prior PE (chains them together) |
| `VendorId` | Int64 | → `RefVendor` (payee — usually prime) |
| `EstimateNumber` | Int16 | 1-based seq within contract |
| `PeriodEndDate` | DateTimeOffset | last day of the billing period |
| `AccountingReceivedDate`, `CheckDate`, `CheckNumber` | mixed | payment-side timestamps |
| `CurrentGrossItemInstalledAmount` | Decimal | this period: gross value of what was installed |
| `CurrentItemPaidGrossAmount` | Decimal | this period: gross dollars paid against line items |
| `CurrentItemPaidNonParticipAmount` | Decimal | non-participating (federal eligibility) portion of above |
| `CurrentCashRetainageAmount` | Decimal | this period's cash retainage change (negative = held back) |
| `CurrentGrossRetainageAmount` | Decimal | total retainage change this period |
| `CurrentIncentiveAmount`, `CurrentDisincentiveAmount` | Decimal | this period's incentive/disincentive |
| `CurrentLiqDamageAmount` | Decimal | this period's liquidated damages |
| `CurrentGrossContractAdjustmentAmount`, `CurrentOtherContractAdjAmount` | Decimal | this period's contract-level adjustments |
| `CurrentTotalSubcontractAmount` | Decimal | this period's subcontract portion |
| `CurrentNetAmountForRetainCalc` | Decimal | the net on which retainage was calculated |
| `CurrentPaidAmount` | Decimal | net check amount this period |
| `Previous…` | Decimal | same fields rolled up through prior PE |
| `Total…` | Decimal | Previous + Current — these are the running totals |

**Worked example — PE #290 (contract 282, est 6, period end 2024-09-02):**

```
CurrentGrossItemInstalledAmount: $4,669.89
CurrentItemPaidGrossAmount:      $4,669.89
CurrentCashRetainageAmount:     -$233.49   (5 % holdback)
CurrentPaidAmount:               $4,436.40  (net check this period)
TotalGrossItemInstalledAmount:  $517,277.95
TotalItemPaidGrossAmount:       $604,277.95  (gross through est 6)
TotalCashRetainageAmount:       -$30,213.89
TotalPaidAmount:                $574,064.06  (cumulative net paid through est 6)
TotalStockpileAdjustmentAmount: $87,000.00  (from PE adjustments carried in)
```

Note that `PreviousItemPaidGrossAmount` = $599,608.06, so `TotalItemPaidGrossAmount` ($604,277.95) = Previous + Current ($4,669.89). This is the invariant: `Total = Previous + Current` for every amount field.

##### `PaymentEstimateItem`

Per-line-item version of the above. 38p / 4n.

| Prop | Type | Meaning |
|---|---|---|
| `PaymentEstimateId` | Int64 | parent |
| `ContractProjectItemId` | Int64 | which line this is paying |
| `CurrentTotalInstalledQuantity`, `PreviousTotalInstalledQuantity` | Decimal | field-measured installed quantities |
| `CurrentTotalPaidQuantity`, `PreviousTotalPaidQuantity` | Decimal | paid quantities (may differ from installed when there's an overrun or stockpile) |
| `CurrentTotalInstalledAmount`, `CurrentTotalPaidAmount`, `CurrentTotalAdjustmentAmount` | Decimal | corresponding dollar amounts |
| `OverrunQuantity` | Decimal | quantity beyond the authorized contract quantity |
| `CurrentOverrunAdjustmentAmount` | Decimal | typically negative — the adjustment pulling overrun out of this period |
| `CurrentStockpileAdjustmentAmount` | Decimal | stockpile recovery this period |
| `CurrentPriceAdjustmentAmount`, `CurrentOtherItemAdjustmentAmount` | Decimal | the other adjustment categories |
| `TotalStockpileAdjustmentAmount`, `TotalPriceAdjustmentAmount`, `TotalOverrunAdjustmentAmount`, `TotalTotalAdjustmentAmount` | Decimal | cumulative versions |
| `DifferenceInCurrentlyInstalledPaidAmount`, `DifferenceInCurrentlyInstalledPaidQuantity` | Decimal | installed − paid for this period (should normally be 0) |

**Worked example — PaymentEstimateItem #17002 on PE 290 (CPI 4365, fertilizer-related line):**

```
CPI=4365 (project item line 240, Mulch Blanket, unit Syd @ $2.43)
CurrentTotalInstalledQuantity: 1,037.0 Syd
CurrentTotalPaidQuantity:      1,037.0 Syd
CurrentTotalInstalledAmount:   $2,519.91
CurrentTotalPaidAmount:        $2,519.91
```

##### `PaymentEstimateItemFund`

Where the money comes from, per line, per estimate. 12p / 3n.

| Prop | Type | Meaning |
|---|---|---|
| `PaymentEstimateItemId` | Int64 | which line |
| `ContractFundId` | Int64 | which fund |
| `CurrentAmountAllocated` | Decimal | this period's share |
| `PreviousTotalAmountAllocated` | Decimal | cumulative through prior PE |
| `PayEstimateItemAdjustmentId` | Int64 | links to the adjustment if this fund row came from one |

**Worked example — PEItemFund #2399 on PE Item 16644 (first installed line on contract 282):**

```
ContractFundId=306 (Alcona County, 5 % share)
CurrentAmountAllocated: $2,815.04
```

##### `ContractAdjustment`

Period-level adjustments. 18p / 5n.

| Prop | Type | Meaning |
|---|---|---|
| `PaymentEstimateId` | Int64 | which period |
| `ContractTimeId` | Int64 | → ContractTime, non-null for Time Charge adjustments |
| `Amount` | Decimal | signed |
| `Type` | String | `Retainage`, `Time Charge`, `Liquidated Damages`, `Incentive`, `Disincentive`, free text otherwise |
| `AdjustmentNumber` | Int16 | 1-based within PE |
| `SystemGenerated` | Boolean | server-made vs user-entered |
| `Rate` | Decimal | per-unit rate when applicable |
| `DistributionMethod` | String | `Percentage`, `Fixed` |
| `ContractFundPackageId` | Int64 | which package to charge |
| `TimeUnits` | Decimal | for time-charge adjustments |

**Worked example — ContractAdjustment #94 on PE 283:**

```
Type=Retainage  Amount=-$7,504.78  SystemGenerated=True  DistributionMethod=Percentage
AdjustmentNumber=1  Date=2024-08-29
```

##### `PayEstimateItemAdjustment`

Per-item adjustments. 27p / 7n. These are the heavy-hitter adjustments that touch individual pay-estimate items (stockpiles, overruns, price indexes).

| Prop | Type | Meaning |
|---|---|---|
| `PaymentEstimateItemId` | Int64 | which line |
| `StockpileId` | Int64 | non-null for stockpile adjustments |
| `Function` | String | `Dollar-Based`, `Quantity-Based` |
| `Type` | String | `Construction Stockpile`, `Overrun`, `Price Index`, `Other`, … |
| `Amount`, `Quantity`, `UnitPrice`, `PaidQuantity`, `QuantityAdjusted` | Decimal | the amounts |
| `SystemGenerated`, `PriceAdjustment`, `IsOffsetAdj` | Boolean | flags |
| `RefPriceIndexAdjustmentId` | Int64 | → the price-index catalog entry |
| `StockpileTransactionProjectItemId` | Int64 | → `StockpileTransactionProjectItem` for traceability |
| `StockpileItemRecoveryPercentage` | Decimal | stockpile recovery % |
| `DwrStplAdj` | String | tag like `Stockpile` or `DWR` |

**Worked example — PayEstimateItemAdjustment #314 (PE 283 on item 16643):**

```
Type=Construction Stockpile  Function=Dollar-Based  Amount=$58,000.00
StockpileId=45  StockpileItemRecoveryPercentage=75.0
SystemGenerated=True  Comments="Payment Estimate Item Adjustment generated Stockpile Transaction"
```

Stockpile #45 on contract 282 is the first batch of pre-driven steel pile (CI #4451, line 350 — Pile, Steel Furnished Driven 14-inch), staged $58,000 of pile, then recovered at 65 % as the pile actually went in. See **Stockpile** below.

##### `ChangeOrder`

58 scalar fields, 14 navs. Only the money-relevant ones:

| Prop | Type | Meaning |
|---|---|---|
| `Number` | String | human seq (`0001`, `0002`, …) |
| `Amount` | Decimal | net $ impact (nullable — see note) |
| `ChangeOrderDate`, `ApprovalDate` | DateTimeOffset | |
| `Status` | String | `Draft`, `Pending`, `Approved`, `Denied` |
| `Type` | String | `OTH` (other), `SUPPLA` (supplemental agreement), `CMPL` (compliance), free text |
| `Reason` | String | reason code (`EXTR`, `ORDOT3M`, …) |
| `IncreaseDecreaseItems`, `TimeAdjustments`, `NewItems`, `BalanceCompletedItems`, `ContModOnly`, `ItemsRequiringApproval` | Boolean | what the CO contains |
| `Unilateral`, `OverrideApprovalRules` | Boolean | |
| `PrevApprovedChangeOrderTotal` | Decimal | snapshot of change-order total before this one |
| `CurrentApprovalRound`, `CurrentApprovalGroupId` | Int64 | approval chain state |

The `Amount` field is sometimes null even on approved COs — specifically for `Type="CMPL"` compliance-only ones that only shift time or metadata. Walk `ChangeOrderIncDecItem.Amount` and `ChangeOrderNewItem.ExtendedAmount` for the real $ impact.

**Worked example — all 3 change orders on contract 282:**

```
CO #114  num=0003  Amount=null       Status=Approved  Type=CMPL     Reason=ORDOT3M  Date=2024-09-09
CO #112  num=0001  Amount=$69.93     Status=Approved  Type=OTH      Reason=EXTR     Date=2024-09-05
CO #113  num=0002  Amount=$319.13    Status=Approved  Type=SUPPLA   Reason=EXTR     Date=2024-09-05
```

Total: $389.06 — matches `Contract.NetChangeAmountApproved`.

##### `ChangeOrderIncDecItem`

The main shape: a CO that changes quantities on existing contract lines. 10p / 3n.

```
Id=86  ChangeOrderId=112  ContractProjectItemId=4363
Quantity=+9.0   Amount=+$69.93   BalancedCompleted=False
```

That's CO #112 adding 9 Sft to CPI 4363 (line 220, "Sign Type B Temp Oper") at the item's $7.77/Sft rate.

##### `ChangeOrderNewItem` and `ChangeOrderForceAccount`

**`ChangeOrderNewItem`** (23p / 8n) carries fully-defined new line items when the CO introduces work that didn't exist in the original contract. Key fields: `ContractItemLineNumber`, `ProjectItemLineNumber`, `Quantity`, `UnitPrice`, `ExtendedAmount`, `Unit`, `SupplementalDescription`, `NewItemType`, `ItemType`, `DollarBasedLumpSum`, plus navs to `RefItem`, `ContractProject`, `ContractProjectCategory`, `ContractFundPackage`, `Contractor`, `ChangeOrder`, `ContractProjectItem`. Zero rows on contract 282 (all three COs modify existing items or just time).

**`ChangeOrderForceAccount`** (7p / 2n) authorizes new force-account work — minimal row, just the join: `ChangeOrderId`, `ForceAccountId`. Zero on contract 282.

##### `ChangeOrderTimeAdjustment`

```
Id=29  ChangeOrderId=114  ContractTimeId=1937
AdjustmentTimeUnits=-87.0  AdjustmentCompletionDate=null
```

CO #114 subtracted 87 time units from ContractTime 1937. The "unit" is defined on `ContractTime` (typically working days or calendar days).

##### `ContractClaim` → `ContractClaimLitigation` / `ContractClaimChangeOrder`

Formal disputed money. 63p / 8n for the claim itself. Key fields: `ClaimNumber`, `Category` (`Intial` — sic — `Modification`), `Status` (`Open`, `Resolved`, …), `AdditionalStatus`, `ReceivedDate`, `RequestedAmount`, `PaymentAmount`, `RequestedDays`, `DaysGranted`, `ClaimantName`, `SubcontractorId`, `PaymentEstimateId`, `DiaryStartDate`/`EndDate`, `AnalysisCompletionDueDate`, `ResponseDueDate`, `ResolutionDate`, `PaymentDate`, `DaysGrantedDate`, `EventDate`, `DiscoveryDate`, `AffidavitOfDocumentationDate`, `StatementOfDefenseDate`, `SettlementConferenceDate`, `UndertakingsDate`, `AppealHearingDate`, `CourtFileNumber`, `CourtDistrict`, `DOJFileNumber`, `ClaimantAttorney`, `ClaimantLawFirm`, `DefendantAttorney`, `JudgeName`.

**Worked example — ContractClaim #16 on contract 282:**

```
ClaimNumber=1  Category=Intial  Status=Open  AdditionalStatus=BI
ReceivedDate=2024-09-13  RequestedAmount=$1,000,000.00  RequestedDays=5
ClaimantName="Prime and Subs"  SubcontractorId=122
PaymentEstimateId=306 (the final estimate, est #11)
DiaryStartDate=2024-08-01 → DiaryEndDate=2024-08-30
AnalysisCompletionDueDate=2024-09-28
CourtFileNumber=555777888  CourtDistrict=Northern  JudgeName=Judy
EventDate=2024-09-13
```

**ContractClaimLitigation #1 for claim 16:**

```
LitigationDate=2024-09-13  LitigationAmount=$1,000,000.00  NonLitigationAmount=null
```

So the entire $1M is in litigation.

##### `ContractFundPackage` → `ContractFund` → `RefFund`

The money sources.

**`ContractFundPackage`** (9p / 5n): `ContractId`, `Name`, `Description`, `DefaultContractAdjustmentIndicator`.

**`ContractFund`** (28p / 4n): `ContractFundPackageId`, `RefFundId`, `Priority`, `Percentage`, `Type` (`Federal`/`Non Federal`), `Limit`, `OriginalLimit`, `PreviousAmountUsed`, `CurrentAmountUsed`, `TotalAmountUsed`, `RemainingAmount`, `AccountingFund`, `StateAccountingCode`, `StateFundingCode`, `FundingGroup`, `PrevApprPayEstAmntUsed`.

**`RefFund`** (14p / 5n): `Name`, `Description`, `FundType`, `Percentage`, `AccountingFund`, `FundingGroup`.

**Worked example — contract 282 funding:**

```
FP #205 "100 / 0001 State 95% / Alcona CRC 5%"
  CF #306  pct=5%   type=Non Federal  totalUsed=$21,829.01   RefFund="CALCON" (Alcona County)
  CF #307  pct=95%  type=Non Federal  totalUsed=$414,750.76  RefFund="STATE" (State)

FP #206 "101 / 0002 State 95% / Alcona CRC 5%"
  CF #308  pct=5%   type=Non Federal  totalUsed=$38,538.95   RefFund="CALCON" (Alcona County)
  CF #309  pct=95%  type=Non Federal  totalUsed=$732,239.44  RefFund="STATE" (State)
```

Sum: $21,829.01 + $414,750.76 + $38,538.95 + $732,239.44 = $1,207,358.16 = `AmountPostedToDate`. ✓

##### `Stockpile`

Material staged for later use (pre-paid partially under the stockpile recovery percentage, then recovered as the material physically gets installed).

| Prop | Meaning |
|---|---|
| `ContractItemId` | → the contract line being stockpiled |
| `Name`, `Description` | human label |
| `ItemRecoveryPercentage` | % of the line's unit price paid up front when staged |
| `StockpileAmount` | gross $ of material staged |
| `CurrentItemAdjustmentAmount`, `TotalItemAdjustmentAmount` | the negative adjustment pulled out of pay-estimate items as recovery happens |
| `Status`, `PreviousStatus` | `Open`, `Closed` |
| `RecoveryDate` | when recovery began |

**Worked example — Stockpiles on contract 282:**

```
SP #45  CI=4451 (line 350 Pile Steel 14") name="0001"  recovery=65%  amount=$58,000  status=Closed
SP #46  CI=4451                            name="0002"  recovery=65%  amount=$29,000  status=Closed
SP #49  CI=4451                            name="0003"  recovery=90%  amount=$30,182.88 status=Closed
```

Pattern: when CPI 4451's full installed quantity got paid out, `CurrentStockpileAdjustmentAmount` turned negative on the pay-estimate item until the stockpile balance zeroed.

##### `ContractRetainage`

The retainage ruleset for the contract. 14p / 1n (just a nav back to `Contract`).

| Prop | Meaning |
|---|---|
| `Percentage` | initial retainage % |
| `MaxPercentage` | ceiling |
| `TriggerPercentage` | % of work complete at which retainage releases |
| `TriggerBase` | basis for the trigger (`Award Amount`, …) |
| `Base` | basis for retainage calc (`Award Amount`, …) |
| `Method` | `Work Per Period`, `Each Period`, … |
| `LumpSumAmount` | optional |
| `MaxDollarAmount` | optional |
| `ExemptForConstructionStockpiles` | Boolean |

**Example row (ContractRetainage #5):** 10% initial, 15% max, trigger at 1% work complete based on award amount, Work Per Period method. (This is a template-level rule; on contract 282 the applied retainage shows up as `CurrentCashRetainageAmount` on each PE.)

##### `AccountTransaction` / `ContractSecurityAccount`

Essentially vestigial on awdemo. `AccountTransaction` has 3 global rows (Bond certificates, 1990s-vintage). `ContractSecurityAccount` for contract 282: 0 rows. These exist for jurisdictions that hold securities (bonds, letters of credit) as collateral for the retainage; skip them unless prod data shows otherwise.

#### How to roll it up

**"Full financial state of contract 282":**

```python
# 1. Contract-level rollups
k = client.get("Contracts", filter="Id eq 282",
    select="Id,AwardedContractAmount,CurrentContractAmount,"
           "AmountPostedToDate,AmountPaidToDate,PercentPaid,"
           "TotalNetChangeAmount,NetChangeAmountApproved,CalcTotalSubcontractAmount")

# 2. Every PE in order, with per-line and per-fund detail
pes = client.get("PaymentEstimates",
    filter="ContractId eq 282",
    orderby="EstimateNumber asc",
    expand="PaymentEstimateItems($select=Id,ContractProjectItemId,"
                                "CurrentTotalInstalledAmount,CurrentTotalPaidAmount,"
                                "CurrentTotalInstalledQuantity,CurrentTotalPaidQuantity;"
                                "$expand=PaymentEstimateItemFunds($expand=ContractFund($expand=RefFund)))",
    top=50)

# 3. Period-level adjustments
adj = client.get("ContractAdjustments",
    filter="PaymentEstimate/ContractId eq 282",
    expand="ContractTime,ContractFundPackage",
    top=200)

# 4. Change orders — with inc/dec and new items
cos = client.get("ChangeOrders",
    filter="ContractId eq 282",
    expand="ChangeOrderIncDecItem($expand=ContractProjectItem($expand=ContractItem)),"
           "ChangeOrderNewItems($expand=RefItem,ContractProjectItem),"
           "ChangeOrderTimeAdjustment($expand=ContractTime),"
           "ChangeOrderForceAccounts($expand=ForceAccount),"
           "ChangeOrderExplanation($expand=RefChangeOrderExplanation)",
    top=50)

# 5. Claims + litigation
claims = client.get("ContractClaims",
    filter="ContractId eq 282",
    expand="RefContractClaimType,Subcontract,PaymentEstimate,"
           "ContractClaimLitigations,ContractClaimChangeOrders($expand=ChangeOrder),"
           "AssociatedContractClaims",
    top=50)

# 6. Funding allocation + usage
funds = client.get("ContractFundPackages",
    filter="ContractId eq 282",
    expand="ContractFunds($expand=RefFund)",
    top=50)

# 7. Stockpiles
sp = client.get("Stockpiles",
    filter="ContractItem/ContractId eq 282",
    expand="ContractItem",
    top=50)

# 8. Retainage ruleset (via ContractProjectRetainage joined by contract-project)
# ContractRetainage has no ContractId FK you can filter on the Contract level directly —
# the only nav is Contract 1:N ContractRetainages (but ContractRetainage.ContractId is not exposed).
# Prefer ContractProjectRetainages filtered via ContractProject/ContractId eq 282.
```

**Reconciliation check (verified live):**

```
Latest PE #306 est11 TotalItemPaidGrossAmount = $1,207,358.16
Contract 282   AmountPostedToDate            = $1,207,358.16
                                                ─────────────  ✓

Latest PE #306 est11 TotalPaidAmount         = $1,147,014.70
Contract 282   AmountPaidToDate              = $1,147,109.70
                                                ─────────────  Δ $95.00
```

The $95 delta reconciles via PE 306's `CurrentDisincentiveAmount` (-$50) + `CurrentLiqDamageAmount` (-$50) + `CurrentCashRetainageAmount` (+$5). Contract.AmountPaidToDate adds back the gross and nets the adjustments differently than the final PE's `TotalPaidAmount` does, so expect a small reconciliation delta — the two figures are built from different paths through the same adjustments.

Also note that `Σ CurrentItemPaidGrossAmount over 11 PEs = $1,207,358.16` — matches `AmountPostedToDate` perfectly, because `Σ Current = Total of last PE` is the invariant.

#### Awdemo gotchas

- **`ContractAdjustmentFunds` is 403 as a top-level query** — you can only reach it via `$expand=ContractAdjustmentFunds` on `ContractAdjustment`. Live expand works.
- **`PaymentEstimateApprovals` is empty for every PE on contract 282.** The entity set works, but there are no approvals. In prod this is where you'd see the chain of sign-offs.
- **`CheckDate` and `CheckNumber` are null on every PE on contract 282** — the awdemo "paid" state is modeled only via the `TotalPaidAmount` rollup, not actual check metadata.
- **`ChangeOrder.Amount` is null for `Type="CMPL"` compliance-only COs.** Walk the children to get the real amount.
- **`PaymentEstimateContractOtherAdjustmentTypes` rows are often zero-amount placeholders** (`Current=0, Previous=0, Total=0`) — the agency pre-created adjustment types but didn't use them. Filter them out before display.
- **The `Stockpile` entity has no `StockpileTransactionProjectItems` nav** even though `StockpileTransactionProjectItem` exists as its own entity (and `PayEstimateItemAdjustment` points to it via `StockpileTransactionProjectItemId`). To trace a stockpile's transactions, query `StockpileTransactionProjectItems?$filter=StockpileTransaction/StockpileId eq {spid}` instead of expanding from the Stockpile.
- **`Contract` doesn't have a nav called `ContractAwardAmount`** — the field is `AwardedContractAmount`. The vendor guide lists `ContractAmount`, which simply doesn't exist on this entity.

---

### 3. Items & materials flows

#### Overview

This is the three-layer story of a single line on a construction contract.

**Planned.** The agency's bid document names a `RefItem` from the master item catalog (e.g. RefItem #5001, "8120121 Sign, Type B, Temp, Oper", unit Sft) — this is agency-wide reference data shared across every contract. The specific contract instantiates it as a `ContractItem` (line number, bid unit price, quantity) and allocates it per-project as `ContractProjectItem` (which project+category it belongs to, the project-item line number, how much of the contract-item quantity lives on this project). On a single-project contract like 282, `ContractItem` and `ContractProjectItem` are 1:1; on a multi-project contract they fan out.

**Materials expected.** The catalog can carry a `RefItemMaterialSet` saying "whenever this item is installed, these are the materials that physically go in it" (e.g. installing a chemical fertilizer line uses potable water, sand, and sodium chloride). When the contract loads, those template material sets get copied onto each `ContractProjectItem` as `ContractProjectItemMaterialSet` (and its materials, in `…SetMaterial`). The set says what the acceptance system expects to be sampled.

**Actual, posted.** Each DWR adds a `DwrWorkItem` for every ContractProjectItem the crew touched that day, with a `QuantityPosted`. Each DwrWorkItem can carry multiple `DwrItemPosting`s (one per crew/location split), and each posting can have `DwrItemPostingQuantity` sub-rows (per-material installed quantity + source).

**Actual, verified.** Each `DwrItemPosting` can also carry `DwrAcceptanceRecord` rows: one per material being accepted on that posting, with the acceptance method, action type, represented quantity, and a link to a `SampleRecord` if a lab sample was taken. The acceptance record is the "yes, this material is OK to pay for" row that unlocks the pay-estimate side.

**Who's supplying what.** `ContractorMaterialSource` records which approved source each contractor plans to buy each material from, with `Submitted`/`Approved` flags for the agency's advance-approval workflow. On awdemo contract 282 this table is empty; the planning side isn't filled in.

#### Entity chain diagram

```
RefItem (1)                                            ─────────  "catalog item"
  Name, Description, Unit, SpecBook, ItemType,
  CommonUnit, ConversionFactorToCommonUnits, LumpSum, MajorItem
  │
  ├── ContractItem (N)                                 ─────────  "contract line"
  │     ContractId, LineNumber, UnitPrice, Quantity,
  │     CurrentQuantity (= Quantity + NetChangeOrderQuantity),
  │     ExtendedAmount, CurrentExtendedAmount,
  │     QuantityPaidToDate, QuantityPaidToDateExtendedAmount, ItemComplete
  │     SpecBook, Unit, MajorItem, AdministrativeInd, FuelAdjustmentInd, SteelPriceInd
  │     ChangeOrderId (nullable; set for CO-added items)
  │
  │     ├── ContractProjectItem (1:N on multi-project contracts; 1:1 on single-project)
  │     │     ContractProjectId, ContractProjectCategoryId, ContractFundPackageId
  │     │     ProjectItemLineNumber, Quantity, UnitPrice, ExtendedAmount
  │     │     CurrentQuantity, CurrentExtendedAmount, NetChangeOrderQuantity
  │     │     QuantityPostedToDate, QtyPostToDateAppDwrs
  │     │     AmountPostedToDate, AmtPostToDateAppDwrs
  │     │     QuantityPaidToDate, AmountPaidToDate, CurrentTotalPaidAmount
  │     │     PercentItemComplete, UnpaidExtAmt, SubcontractToDateAmount
  │     │     RelatedLineItem, ContractItemLineNumber, ChangeOrderNumber
  │     │     ItemSource ("Original"|"CO")
  │     │     │
  │     │     ├── ContractProjectItemMaterialSet (N)   ─────────  "materials expected"
  │     │     │     Name, QuantityPostedToDate, ApprovedQuantityPostedToDate
  │     │     │     │
  │     │     │     └── ContractProjectItemMaterialSetMaterial (N)
  │     │     │           → Material (1), Source (1), Facility (1)
  │     │     │           EstimatedQuantity, ReportedQuantity, SatisfiedQuantity
  │     │     │           ApprovedReportedQuantity, ApprovedSatisfiedQuantity
  │     │     │           ConversionFactor, MaterialUnits, Insufficient, SufficientQuantity
  │     │     │           → AcceptanceActions []
  │     │     │           → DwrAcceptanceRecords []   (back-ref)
  │     │     │
  │     │     ├── DwrWorkItem (N)                      ─────────  "crew posted today"
  │     │     │     DailyWorkReportId, QuantityPosted, PaymentEstimateId,
  │     │     │     AgencyViewStatus, HasAttention
  │     │     │     │
  │     │     │     └── DwrItemPosting (N)             ─────────  "per crew / station"
  │     │     │           DwrContractorId, StationFrom/To, Offset, Location
  │     │     │           QuantityPosted, Measured, AsBuiltQuantity, Sequence
  │     │     │           ContractProjectItemMaterialSetId   ← ties posting to its material set
  │     │     │           │
  │     │     │           ├── DwrItemPostingQuantity (N) ────  "material installed on this posting"
  │     │     │           │     MaterialId, QuantityInstalled, MaterialUnits,
  │     │     │           │     ConversionFactor, WorkLocation
  │     │     │           │     → Material (1), Source (1)
  │     │     │           │
  │     │     │           └── DwrAcceptanceRecord (N)   ─────  "material acceptance"
  │     │     │                 ContractId, MaterialId, ActionType, AcceptanceMethod,
  │     │     │                 RepresentedQuantity, MaterialUnits, FieldInspectionValue,
  │     │     │                 SampleType, WorkLocation, SMFMIDecrementation, ConversionFactor
  │     │     │                 → Material (1), Source (1), Facility (1),
  │     │     │                   SampleRecord (1), Brand (1),
  │     │     │                   ContractProjectItemMaterialSetMaterial (1)
  │     │     │
  │     │     └── PaymentEstimateItem (N)              ─────────  "the pay side"
  │     │           (see Financial Transactions above)
  │     │
  │     ├── ContractorMaterial (N)                      [empty on awdemo 282]
  │     │     per contract-item / material plan — submitted/approved quantities
  │     │     → Material (1)
  │     │
  │     ├── ContractorMaterialSource (N)                [empty on awdemo 282]
  │     │     per contract-item / material / source
  │     │     Submitted, Approved, DateOfSubmission, ApproximateQuantity, SpecBook, TypeSizeClass
  │     │     → Material (1), Source (1), Facility (1)
  │     │
  │     └── Stockpile (N)   (see Financial Transactions above)
  │
  └── RefItemMaterialSet (N)                           ─────────  "catalog-level materials expected"
        Name
        └── RefItemMaterialSetMaterial (N)
              → Material (1)
              ConversionFactor

Material (1)                                           ─────────  "material catalog"
  Name, Description, EnglishUnit, MetricUnit, SpecBook,
  MaterialCategoryId, SourceFacilityRequired, Recycled,
  ControlNumberRequired, BrandNameRequired, Research
  → MaterialCategory, Facility[], Source[]

Source (1)                                             ─────────  "supplier"
  Name, Description, EffectiveDate, ExpirationDate, Active, Status,
  LocationDescription, Type, ApprovalLevelType, GeographicArea
  → RefVendor (1), Facilities []

SampleRecord (1)                                       ─────────  "lab sample"
  Name, ControlNumber, LabControlNumber, SampleType, ControlType,
  AcceptanceMethod, SampleDate, LogDate, AuthorizedDate, SampleStatusLastModifiedDate,
  SampledFrom, DistanceFromGrade, Elevation
  MaterialId, SourceId, FacilityId, SMFMIId
  AuthorizedById, SamplerId, WitnessedById, DWRInspectorId, DSRInspectorId
  (all person refs 403 on awdemo)
  RefSampleStatusId → RefSampleStatus (Pending → Logged → Received → In Testing →
                                       Pending Authorization → Complete → Approved)
  DailyWorkReportId → DailyWorkReport (1)
  → SampleRecordAssociations []   (many-to-many to misc entities)
  → SampleRecordContractMaterialSetAssociation []
       ContractProjectItemMaterialSetId, RepresentedQuantity, SatisfiedRepresentedQuantity
  → SampleRecordSource []
```

#### Entities in the chain

##### `RefItem`

The agency's catalog of items. 61 scalars, 41 navs.

| Prop | Type | Meaning |
|---|---|---|
| `Id` | Int64 | |
| `Name` | String | agency's spec-item number (`8120121`) |
| `Description` | String | human description |
| `Unit` | String | spec-book unit (`Sft`, `Cyd`, `Lb`, `LS`, …) |
| `SpecBook` | String | which specification book (`03`, `04`, …) |
| `ItemType`, `ItemClass`, `ContractClass` | String | catalog classification |
| `UnitSystem` | String | `English`, `Metric` |
| `CommonUnit`, `ConversionFactorToCommonUnits` | mixed | conversion to a canonical unit for cross-item summation |
| `LumpSum`, `BidAsLumpSum` | Boolean | |
| `SupplementalDescriptionRequired`, `CombineWithLikeItems`, `MajorItem`, `NonBid`, `DbeInterest` | Boolean | |
| `RefPrice` | Decimal | catalog reference price (for estimating) |
| `DbePercentToApply` | Decimal | % counted toward DBE commitment when subcontracted |
| `ObsoleteDate` | DateTimeOffset | catalog retirement |

**Worked example — RefItem #5001 (contract 282 line 220):**

```
Name="8120121"  Description="Sign, Type B, Temp, Oper"  Unit=Sft  SpecBook=03
```

##### `ContractItem`

42 scalars, 15 navs.

| Prop | Type | Meaning |
|---|---|---|
| `Id` | Int64 | |
| `ContractId` | Int64 | |
| `LineNumber` | String | line # within the contract (`010`, `220`, …) |
| `RefItemId` | Int64 | → RefItem |
| `SpecBook` | String | copied from RefItem |
| `Unit` | String | copied from RefItem (overridable) |
| `Quantity` | Decimal | **bid quantity** |
| `UnitPrice` | Decimal | **bid unit price** |
| `ExtendedAmount` | Decimal | Quantity × UnitPrice |
| `NetChangeOrderQuantity` | Decimal | cumulative CO changes (±) |
| `CurrentQuantity` | Decimal | Quantity + NetChangeOrderQuantity |
| `CurrentExtendedAmount` | Decimal | CurrentQuantity × UnitPrice |
| `QuantityPaidToDate` | Decimal | field-measured + paid |
| `QuantityPaidToDateExtendedAmount` | Decimal | $ equivalent |
| `MajorItem` | Boolean | agency-defined "major" flag |
| `AdministrativeInd`, `FuelAdjustmentInd`, `SteelPriceInd` | Boolean | flags for the various adjustment regimes |
| `PriceAdjInd`, `PayPlanInd` | Boolean | |
| `ItemSource` | String | `Original` or `CO` |
| `ChangeOrderId` | Int64 | non-null if this line came from a change-order |
| `ItemComplete` | Boolean | server-managed |
| `SampleCount` | Int64 | server-managed count of sample records against this item |

##### `ContractProjectItem`

The per-project version of a contract item. 52 scalars, 16 navs. On a single-project contract, it adds the project-side bookkeeping around a ContractItem.

| Prop | Type | Meaning |
|---|---|---|
| `ContractProjectId`, `ContractProjectCategoryId`, `ContractFundPackageId` | Int64 | project / category / funding attribution |
| `ContractItemId` | Int64 | → ContractItem |
| `ProjectItemLineNumber` | String | the "230" style project-item line |
| `ContractItemLineNumber` | String | copy of ContractItem.LineNumber |
| `Unit`, `Quantity`, `UnitPrice`, `ExtendedAmount` | mixed | copy from ContractItem on load |
| `CurrentQuantity`, `CurrentExtendedAmount`, `NetChangeOrderQuantity` | Decimal | current-state figures (after COs) |
| `QuantityPostedToDate` | Decimal | field-posted (regardless of PE approval) |
| `QtyPostToDateAppDwrs` | Decimal | field-posted on **approved** DWRs only |
| `AmountPostedToDate`, `AmtPostToDateAppDwrs` | Decimal | $ equivalents |
| `QuantityPaidToDate`, `AmountPaidToDate` | Decimal | pay-estimate-paid figures |
| `CurrentTotalPaidAmount` | Decimal | server-maintained running total |
| `PercentItemComplete` | Decimal | server-computed |
| `UnpaidExtAmt` | Decimal | CurrentExtendedAmount − AmountPaidToDate |
| `PendingChangeOrderAmount`, `PendingChangeOrderQuantity` | Decimal | pre-approval CO impact |
| `SubcontractToDateAmount`, `SubcontractToDateQuantity` | Decimal | sub-contracted portion |
| `CriticalItem` | Boolean | agency flag |
| `RelatedLineItem`, `ChangeOrderNumber` | String | |
| `RecordSource`, `ItemSource` | String | provenance |
| `ItemType`, `DollarBasedLumpSum` | mixed | lump-sum variants |

**Worked example — CPI #4364 (contract 282 project 169 line 230, "fertilizer"):**

```
Id=4364  ContractProjectId=169  ContractItemId=4432  ContractFundPackageId=205
Unit=Lb  Quantity=49.0  UnitPrice=$5.82  ExtendedAmount=$285.18
CurrentQuantity=49.0  CurrentExtendedAmount=$285.18  NetChangeOrderQuantity=0.0
QuantityPostedToDate=49.0  AmountPostedToDate=$285.18
QuantityPaidToDate=49.0  AmountPaidToDate=$285.18  PercentItemComplete=100.0
UnpaidExtAmt=$0.00  ItemComplete=true (effectively)
RefItemId=4825  (Chemical Nutrient fertilizer)
```

The fertilizer line was installed in full (49 lbs posted on DWR 345, paid on PE 290).

##### `DwrWorkItem`

The "crew touched this line today" row. 12 scalars, 4 navs.

| Prop | Meaning |
|---|---|
| `ContractProjectItemId`, `DailyWorkReportId` | FKs |
| `QuantityPosted` | the day's installed quantity |
| `PaymentEstimateId` | which PE this DWR rolled into |
| `HasAttachments`, `HasAttention` | server-maintained |
| `AgencyViewStatus` | `None`, `Pending`, `Approved` — agency approval of this specific posting |

**Worked example — DwrWorkItem #698 on DWR 345 for CPI 4364 (fertilizer):**

```
QuantityPosted=49.0  PaymentEstimateId=290  AgencyViewStatus="None"
```

49 lbs of fertilizer posted on 2024-08-09 (DWR 345), billed on PE 290.

##### `DwrItemPosting`

The per-crew-split row. 49 scalars (!), 11 navs. Big because it carries all the location fields.

| Key fields | |
|---|---|
| `DwrWorkItemId` | parent |
| `DwrContractorId` | → DWRContractor (which crew did it) |
| `QuantityPosted` | sometimes null — when null, the parent DwrWorkItem's `QuantityPosted` is the authoritative figure and this posting is a location split without its own quantity |
| `StationFrom`, `StationFromPlus`, `OffsetTypeFrom`, `OffsetDistanceFrom` | from-station location |
| `StationTo`, `StationToPlus`, `OffsetTypeTo`, `OffsetDistanceTo` | to-station location |
| `StartingX`, `StartingY`, `StartingZ`, `EndingX`, `EndingY`, `EndingZ` | coords, if captured |
| `Location` | free-text location label (e.g. "On Site") |
| `Measured`, `AsBuiltQuantity` | field-measured flag + separate as-built capture |
| `PlanSheetPageNumber` | plan reference |
| `Comments` | |
| `Sequence` | ordering within the DwrWorkItem |
| `ContractProjectItemMaterialSetId` | **critical** — binds this posting to its material set so the acceptance chain knows which material-set record to tick off |
| `AssetId` | asset reference |

**Worked example — DwrItemPosting #594 on DwrWorkItem 698:**

```
DwrWorkItemId=698  DwrContractorId=442 (DWR 345's crew)  Location="On Site"
QuantityPosted=null (parent DWI has the 49.0)  Sequence=1
ContractProjectItemMaterialSetId=545  ("FertCN" material set)
```

##### `DwrItemPostingQuantity`

Per-material installed quantity on a posting. 13 scalars.

| Prop | Meaning |
|---|---|
| `DwrItemPostingId` | parent |
| `MaterialId` | → Material |
| `QuantityInstalled` | the installed quantity in material units |
| `MaterialUnits` | string unit |
| `ConversionFactor` | how to convert from material units to the item's bid unit |
| `Overwritten` | Boolean (user override of a system-computed quantity) |
| `SourceId` | → Source |
| `WorkLocation` | optional per-material location |

##### `DwrAcceptanceRecord`

The acceptance row — "yes, this material on this posting is accepted". 25 scalars, 10 navs.

| Prop | Meaning |
|---|---|
| `DWRItemPostingId` | **capitalized `DWR`** — this is the FK gotcha. Everything else uses `Dwr`. |
| `ContractId` | redundant with the posting's parent but faster to filter on |
| `MaterialId` | which material is being accepted |
| `AcceptanceMethod` | agency acceptance method code (`CERT`, `SAMP`, `VIS`, …) |
| `ActionType` | `CERT` (certification letter), `SR` (sample record), `VIS` (visual), `FI` (field inspection) |
| `SampleType` | sample category |
| `FieldInspectionValue` | result if inspection-only |
| `RepresentedQuantity` | how much material this acceptance covers |
| `MaterialUnits` | units of RepresentedQuantity |
| `ConversionFactor` | if material units ≠ item units |
| `WorkLocation` | optional |
| `Comments` | |
| `SampleRecordId` | → SampleRecord, non-null when ActionType=SR |
| `SourceId`, `FacilityId`, `SMFMIId` | source / facility / source-material-facility-material-identification refs |
| `BrandId` | → Brand when the material has brands |
| `ContractProjectItemMaterialSetMaterialId` | which material-set-material row this acceptance ticks off |
| `AgencyViewId` | → AgencyView (approval status) |
| `SMFMIDecrementation` | Boolean — did this acceptance pull from a source's inventory count? |

**Worked example — DwrAcceptanceRecords on contract 282 (6 records total):**

```
AR#296  posting=594  mat="1000.01 Potable Water"       method=CERT  action=CERT  rep=49.0 GAL  sr=null   CPIMS=FertCN
AR#297  posting=594  mat="700.05 Sand"                 method=SAMP  action=SR    rep=0.0 LBS   sr=460    CPIMS=FertCN  (Sand Test)
AR#298  posting=594  mat="239a Sodium Chloride"        method=CERT  action=CERT  rep=49.0 BAG  sr=null   CPIMS=FertCN
AR#299  posting=601  mat="1000.02 Non-Potable Water"   method=null  action=null  rep=null GAL  sr=null   CPIMS=SeedOne
AR#300  posting=601  mat="239a Sodium Chloride"        method=null  action=null  rep=0.0 BAG   sr=null   CPIMS=SeedOne
AR#301  posting=601  mat="NotExpMat Calcium Chloride"  method=null  action=null  rep=null BAG  sr=null   CPIMS=SeedOne
```

So on posting 594 (fertilizer, DWR 345), the three materials expected by FertCN were accepted — water + sodium chloride by vendor certification, sand by a lab sample ("Sand Test", SR #460). On posting 601 (seed, SeedOne), acceptance was created but neither method nor action is filled in yet (likely draft rows).

##### `ContractProjectItemMaterialSet` + `…SetMaterial`

**`ContractProjectItemMaterialSet`** (9p / 4n): `ContractProjectItemId`, `Name`, `QuantityPostedToDate`, `ApprovedQuantityPostedToDate`.

**`ContractProjectItemMaterialSetMaterial`** (18p / 6n): `ContractProjectItemMaterialSetId`, `MaterialId`, `FacilityId`, `SourceId`, `ConversionFactor`, `MaterialUnits`, `EstimatedQuantity`, `ReportedQuantity`, `SatisfiedQuantity`, `ApprovedReportedQuantity`, `ApprovedSatisfiedQuantity`, `Insufficient`, `SufficientQuantity`.

**Worked example — MS #545 (FertCN) on CPI 4364:**

```
Name="FertCN"  QuantityPostedToDate=49.0  ApprovedQuantityPostedToDate=49.0

MM#1318  Material="1000.01 Potable Water"       conv=1.0  est=49  reported=49  satisfied=49  units=GAL
MM#1319  Material="700.05 Sand"                 conv=1.0  est=49  reported=49  satisfied=49  units=LBS
MM#1320  Material="239a Sodium Chloride"        conv=1.0  est=49  reported=49  satisfied=49  units=BAG
```

For each lb of fertilizer installed, 1 gal water + 1 lb sand + 1 bag sodium chloride are expected. 49 lb installed → 49 of each tallied. (The "FertCN" material-set definition itself originates from `RefItemMaterialSet #75` on RefItem 4825, which carries the same three materials with the same conversion factors.)

##### `SampleRecord`

93 scalars, 39 navs. The lab-sample system of record.

| Key fields | |
|---|---|
| `Name` | agency sample name (`999SandTest`) |
| `ControlNumber` | agency control # (`Sand Test`) |
| `LabControlNumber` | lab's internal #  (`CN999SandTest`) |
| `SampleType` | `QAQC`, `QC`, `VERIFY`, `IA` (independent-assurance) |
| `ControlType` | `A`, `B`, `C`, … (agency category) |
| `AcceptanceMethod` | `SAMP`, `CERT`, `VIS` |
| `SampleDate` | when sampled in the field |
| `LogDate` | when logged into the system |
| `AuthorizedDate` | when authorized for pay |
| `SampleStatusLastModifiedDate` | status-change audit |
| `SampledFrom` | `Site`, `Pit`, `Plant`, free text |
| `AssociatedContracts` | denormalized string of related contract names |
| `MaterialId` | → Material |
| `SourceId`, `FacilityId`, `SMFMIId` | source / facility / SMFMI |
| `AuthorizedById`, `SamplerId`, `WitnessedById`, `DWRInspectorId`, `DSRInspectorId`, `LSAURLastModifiedById`, `RevisedById` | all → PersonInfo (403 on awdemo) |
| `RefSampleStatusId` | → RefSampleStatus (lifecycle below) |
| `DailyWorkReportId` | → DailyWorkReport |
| `SampleRecordGroupId` | optional grouping |

`RefSampleStatus` lifecycle (`RefSampleStatuses`, 9 rows):

```
1 Pending                    (auth=false  accept=false)
2 Logged                     (auth=false  accept=false)
3 Received at Destination Lab(auth=false  accept=false)
4 Received at Lab Unit       (auth=false  accept=false)
5 In Testing                 (auth=false  accept=false)
6 Pending Authorization      (auth=true   accept=false)   ← SR 460 is here
7 Void                       (auth=true   accept=false)
8 Complete                   (auth=true   accept=true)
9 Approved                   (auth=true   accept=true)
```

**Worked example — SampleRecord #460 (DWR 345, Sand Test):**

```
Name="999SandTest"  ControlNumber="Sand Test"  LabControlNumber="CN999SandTest"
SampleType=QAQC  ControlType=A  AcceptanceMethod=SAMP  SampledFrom="Site"
SampleDate=2024-08-09  LogDate=2024-09-04  AuthorizedDate=2024-09-05
RefSampleStatusId=6 (Pending Authorization)  AssociatedContracts="WHITEOAK BRIDGE"
MaterialId=21  SampleRecordGroupId=423
DailyWorkReportId=345
AuthorizedById=1609  SamplerId=1609  DWRInspectorId=1609  WitnessedById=2
```

The sample was taken on 2024-08-09 (same day as DWR 345), logged 2024-09-04, authorized 2024-09-05.

##### `SampleRecordContractMaterialSetAssociation`

The join table that ties samples to the material sets they satisfy. 11p / 3n.

| Prop | Meaning |
|---|---|
| `ContractProjectItemMaterialSetId` | which material set |
| `SampleRecordId` | which sample |
| `WorkLocation`, `MaterialUnit` | optional context |
| `RepresentedQuantity`, `SatisfiedRepresentedQuantity` | the quantities this sample attests to |

**Worked example — SRA #150:** `MS=545 (FertCN)  SR=460 (Sand Test)  RepresentedQuantity=49.0  SatisfiedRepresentedQuantity=49.0` — exact match on represented and satisfied.

##### `Material`, `Source`, `Facility`, `SMFMI`

**`Material`** (52p / 31n): `Name`, `Description`, `EnglishUnit`, `MetricUnit`, `SpecBook`, `MaterialCategoryId`, `SourceFacilityRequired`, `Recycled`, `ControlNumberRequired`, `BrandNameRequired`, `MaterialShortName`, `Research`.

**`Source`** (24p / 27n): `Name`, `Description`, `RefVendorId`, `LocationDescription`, `Type`, `ApprovalLevelType`, `GeographicArea`, `City`, `EffectiveDate`, `ExpirationDate`, `Active`, `Status`, `IsLatestVersion`, `Archive`.

**`SMFMI` (SourceMaterialFacilityMaterialIdentification)** — the composite key tying Source + Material + Facility + a specific material identification (brand/lot).

##### `ContractorMaterial` / `ContractorMaterialSource`

The pre-construction plan: which contractor plans to supply which materials from which sources.

- `ContractorMaterial` ties `ContractItem` + `Material` with the contractor's submitted/approved quantities (12 scalar fields: `SubmittedApproximateQuantityTotal`, `ApprovedApproximateQuantityTotal`, `ContractorMaterialEstimatedQuantity`, `SubmittedApproximateQuantityPercentage`, `ApprovedApproximateQuantityPercentage`, `Overwritten`).

- `ContractorMaterialSource` adds the source and facility: `ContractItemId`, `MaterialId`, `SourceId`, `FacilityId`, `SpecBook`, `TypeSizeClass`, `ApproximateQuantity`, `Approved`, `Submitted`, `DateOfSubmission`, `Comments`.

**Both are empty on contract 282 on awdemo** — the agency didn't require up-front source approval for this contract. In prod on federal-aid work you'd expect both populated before any posting happens.

#### How to roll it up

**"For contract 282, show every CPI with: bid qty+price, current state, DWR postings, and material acceptance status":**

```python
# 1. All ContractProjectItems with their contract-item + ref-item shoulders
cpis = client.get("ContractProjectItems",
    filter="ContractProject/ContractId eq 282",
    expand="ContractItem($expand=RefItem($select=Id,Name,Description,Unit,SpecBook)),"
           "ContractProjectCategory,ContractFundPackage,"
           "ContractProjectItemMaterialSets($expand=ContractProjectItemMaterialSetMaterials($expand=Material,Source,Facility))",
    top=200)

# 2. All DwrWorkItems on contract 282 (via nav)
wis = client.get("DwrWorkItems",
    filter="DailyWorkReport/ContractId eq 282",
    select="Id,ContractProjectItemId,DailyWorkReportId,QuantityPosted,PaymentEstimateId,AgencyViewStatus",
    top=999)

# 3. All DwrItemPostings in one shot
wi_ids = [w["Id"] for w in wis]
postings = client.get("DwrItemPostings",
    filter=f"DwrWorkItemId in ({','.join(str(i) for i in wi_ids)})",
    expand="DwrItemPostingQuantities($expand=Material,Source),"
           "DwrAcceptanceRecords($expand=Material,SampleRecord,Source,Facility,"
                                 "ContractProjectItemMaterialSetMaterial)",
    top=999)

# 4. All PE items for this contract
pe_items = client.get("PaymentEstimateItems",
    filter="PaymentEstimate/ContractId eq 282",
    select="Id,PaymentEstimateId,ContractProjectItemId,CurrentTotalInstalledQuantity,"
           "CurrentTotalInstalledAmount,CurrentTotalPaidQuantity,CurrentTotalPaidAmount",
    top=999)

# 5. Compose per-CPI
by_cpi = {cpi["Id"]: {"cpi": cpi, "work_items": [], "postings": [], "pe_items": []}
          for cpi in cpis}
for w in wis: by_cpi[w["ContractProjectItemId"]]["work_items"].append(w)
for p in postings:
    wi_cpi = next((w["ContractProjectItemId"] for w in wis if w["Id"] == p["DwrWorkItemId"]), None)
    if wi_cpi: by_cpi[wi_cpi]["postings"].append(p)
for pe in pe_items: by_cpi[pe["ContractProjectItemId"]]["pe_items"].append(pe)
```

**Worked trace — fertilizer line, end to end:**

```
RefItem #4825 "Chemical Nutrient" (fertilizer, unit Lb)
  └── RefItemMaterialSet #75 "FertCN"
        ├── Potable Water (1 GAL / Lb)
        ├── Sand (1 LBS / Lb)
        └── Sodium Chloride (1 BAG / Lb)

ContractItem #4432 (contract 282 line 230) — bid 49 Lb @ $5.82 = $285.18
  └── ContractProjectItem #4364 (project 169) — 49 Lb × $5.82 → paid 100%
        └── ContractProjectItemMaterialSet #545 "FertCN"  posted=49, approved=49
              ├── MM#1318 Potable Water: est=49 reported=49 satisfied=49
              ├── MM#1319 Sand: est=49 reported=49 satisfied=49
              └── MM#1320 Sodium Chloride: est=49 reported=49 satisfied=49

DWR #345 (2024-08-09)
  └── DwrWorkItem #698 (CPI 4364, qty 49, PE 290, AgencyViewStatus=None)
        └── DwrItemPosting #594 (contractor 442, location=On Site, CPIMS=545)
              ├── DwrAcceptanceRecord #296 Water   method=CERT  rep=49 GAL  (vendor cert)
              ├── DwrAcceptanceRecord #297 Sand    method=SAMP  rep=0  LBS  → SampleRecord #460 "Sand Test" (QAQC, status=Pending Authorization)
              └── DwrAcceptanceRecord #298 NaCl    method=CERT  rep=49 BAG  (vendor cert)

PaymentEstimate #290 (est 6, period end 2024-09-02)
  └── PaymentEstimateItem on CPI 4364: paid 49 Lb × $5.82 = $285.18
```

#### Awdemo gotchas

- **`DwrItemPosting.QuantityPosted` is often null** — when posting-level quantity is null, the parent `DwrWorkItem.QuantityPosted` is authoritative and the posting is just a location/crew split. Don't sum postings' QuantityPosted expecting the DWR total.
- **`DwrAcceptanceRecord` uses `DWRItemPostingId` (uppercase DWR)** while the posting entity itself is `DwrItemPosting`. Every other FK uses `DwrXxx`. Fail loud by typo-checking before issuing the request.
- **`RefSampleStatus` entity set is `RefSampleStatuses`** (plural with the trailing `-es`). `/RefSampleStatus` 404s.
- **`PersonInfos` is 403**, so `SampleRecord.SamplerId`/`AuthorizedById`/`WitnessedById`/`DWRInspectorId`/`DSRInspectorId` all return as bare ints with no name resolution available via top-level query. Workaround: for the ones that match the DWR's own `InspectorId`/`CreatorId`/`ApprovedById`, you at least have the id consistency to deduplicate "the inspector" across records.
- **`ContractorMaterials` and `ContractorMaterialSources` are empty on contract 282** — the "approve the plan before posting" workflow isn't exercised on awdemo. Code against them, but don't expect data.
- **`RefItemMaterialSets` carries the template materials for a RefItem**; when a `ContractProjectItem` loads, these get copied into `ContractProjectItemMaterialSet` + `…SetMaterial`. The template and the instance drift independently after the copy — don't assume they stay in sync.
- **`SampleRecordAssociation.AssociationType` + `EntityId` is a polymorphic join** (points to any entity via `AssociationType` discriminator). Awdemo has none on SR #460, but if you need to find them, filter on `SampleRecord/Id eq {srid}` and then branch on `AssociationType`.
- **`ContractProjectItemMaterialSet.ContractProjectItem` is the nav**, but there is no reverse nav from `ContractProjectItem` to its direct `ContractItem.ContractorMaterials` chain — the two "materials" systems (per-item plan vs per-item-per-project material set) live side by side and sometimes have overlapping information. Prefer the `ContractProjectItemMaterialSet` chain for new work; it's the one the acceptance records actually reference.
- **`DwrAcceptanceRecord.MaterialId` is independent of the `ContractProjectItemMaterialSetMaterial.MaterialId`** it links through — the server doesn't force them equal (and we observed one case where they match 1:1, but the schema permits divergence).
- **The `AcceptanceAction` nav on `ContractProjectItemMaterialSetMaterial` is a collection** (one material set material can have multiple acceptance-action rules), but all three fertilizer-line materials on contract 282 have **zero** acceptance actions associated. The actions catalog exists; it's just not wired to this contract.

---

### Cross-flow interactions

The three flows are not independent. Six interactions matter in practice:

1. **DWR → PaymentEstimate.** Every `DwrWorkItem` has a `PaymentEstimateId` nullable FK. When a DWR is approved, the server computes which pay-estimate period it falls into (by date against the PE's `PeriodEndDate`), sets the FK, and the `PaymentEstimateItem`'s `CurrentTotalInstalledQuantity`/`Amount` rolls up by summing all its `DwrWorkItem`s' `QuantityPosted` × `ContractProjectItem.UnitPrice`. This is why `AgencyViewStatus` matters — only approved postings count.
2. **ChangeOrder → ContractProjectItem.** `ChangeOrderIncDecItem` modifies `ContractProjectItem.NetChangeOrderQuantity`, which flows into `CurrentQuantity` and `CurrentExtendedAmount`. `ChangeOrderNewItem` creates net-new `ContractProjectItem` rows with `ItemSource="CO"`. These then feed the materials flow because any newly created CPI can carry its own `ContractProjectItemMaterialSet`.
3. **ChangeOrder → ContractTime.** `ChangeOrderTimeAdjustment` modifies a `ContractTime`'s unit count, which the pay-estimate side consumes via `PaymentEstimateContractTimeCharge.CurrentTimeChargeUnits` to compute per-period time charges and ultimately liquidated damages.
4. **DwrAcceptanceRecord → PaymentEstimate approval.** When a `DwrAcceptanceRecord` has `AcceptanceMethod=SAMP` and `ActionType=SR` but the referenced `SampleRecord` is still in status 1-5 (not yet authorized), that line's `AgencyViewStatus` can stay "pending" — blocking it from being paid on the PE. This is the materials-side gate on the money flow.
5. **ContractClaim → PaymentEstimate.** `ContractClaim.PaymentEstimateId` ties a claim to the PE on which it was raised. On resolution, a `ContractClaimChangeOrder` can issue a CO that lands in a later PE as `ChangeOrderIncDecItem` adjustments, closing the loop.
6. **DWRContractor.DecisionClassId ↔ PayrollEmployeeLabor.LaborClassId.** Both FK to `DecisionClass`. This single shared vocabulary is what lets you reconcile "crew of 1 operating-engineer × 8 hrs on DWR 340" against the certified-payroll weekly submission that should contain the same classification × same person × same date. On awdemo the certified-payroll side is empty so this reconciliation isn't live, but the join path is correct.

Also useful: **`PaymentEstimate.DwrWorkItems`** is a true nav (not just a filter helper) — once a PE is created, its payload of DwrWorkItems is explicitly linked, and you can list them off the PE without walking through contracts/DWRs.

---

### Deferred / unverified against awdemo

| Thing | Why we couldn't verify |
|---|---|
| `CertifiedPayroll` chain in full detail | Zero rows for contract 282. Entity sets return 200 with `[]`. Schema is from EDMX, but the compute-and-reconcile paths (`RequiredCompensation` vs `DifferenceRequiredVsReported`, prevailing-wage shortfall rules) can't be exercised. |
| `DWRStaffRecord` population | Zero rows on all 13 DWRs on contract 282. |
| `DwrForceAccountContractor` + `DwrForceAccountContractorLabor` + `DwrForceAccountContractorVendorEquipment` | ForceAccount #11 exists but has no DWR postings. |
| `ChangeOrderNewItem` | Zero on contract 282 — only increase/decrease and time-adjustment COs are present. |
| `ChangeOrderExplanation`, `ChangeOrderForceAccount` | Zero on contract 282. |
| `PaymentEstimateApproval` | Zero on all PEs for contract 282. |
| `ContractorMaterial`, `ContractorMaterialSource` | Zero on contract 282. The agency-approval workflow isn't filled in. |
| `AcceptanceAction` on CPIMS materials | Zero on contract 282's fertilizer line (and likely most lines). The acceptance-rule catalog exists but isn't tied to this contract's material sets. |
| `AccountTransaction`, `ContractSecurityAccount` | 3 vestigial rows globally (1990s bonds); contract 282 has none. |
| `PersonInfos` entity set | 403 globally. Inline `$expand=Inspector` also 403. Prod should restore both. |
| `ContractAdjustmentFunds` top-level | 403 globally. Only reachable via `$expand` from `ContractAdjustment`. |
| `RefWageDecisionModification` depth | Only CPWD #16 on contract 282 (`NCDOJ2018`, NC state-authority). We confirmed the join path but not the full `RefWageDecisionClass` → `DecisionClass` × rate table it should produce. |
| `PaymentEstimateContractOtherAdjustmentType` with non-zero amounts | All rows seen on contract 282 have `Current=0, Previous=0, Total=0` — just pre-created placeholders. |
| `SampleRecord` reaching final statuses 8-9 | SR #460 is at status 6 "Pending Authorization". The transitions through Complete / Approved aren't exercised. |

---

---

---

<a id="part-6-testing-qaqc-material-acceptance"></a>

# Part 6 — Testing, QA/QC & material acceptance

_The science side of construction — AcceptanceAction rule book, SampleRecord lifecycle, MaterialTest and SampleRecordTest, lab qualifications, approved sources, and the DwrAcceptanceRecord that ties it all back to posted work. Includes the XML-blob test-result pattern (results live inside `SampleTestResultTemplateLog.DataXML`)._

The quality-assurance side of AMS answers one question: *is this material good enough to pay for?*
The chain starts with the **rules of the game** (an `AcceptanceAction` defines which test is required, how often, at what rate, and under which evaluation method), moves through the **sampling event** (a `SampleRecord` with its lab control number, who authorized it, where the material came from), produces one or more **tests** (`SampleRecordTest` rows that cite `MaterialTest` standards like AASHTO T27 or ASTM C39), and finally ties back to the daily-work-report posting via a **`DwrAcceptanceRecord`** that confirms the material was accepted and decrements the material-set's remaining allowed quantity. In awdemo this chain is populated at the lab's "sampling" tier (428 samples, 438 tests, 224 acceptance records, 999 acceptance-action rules) and lightly populated at the "destination-lab/source" tier (48 labs, 65 sources, 38 daily source reports) — enough to document every entity, every link, and every awdemo gotcha with live data.

**Scope**: this chapter picks up where **Part 3** of the combined doc left off (which traced the material-set chain `ContractProjectItemMaterialSet → DwrAcceptanceRecord → SampleRecord` from the DWR's perspective) and goes deep on the QA/QC science side — the acceptance-rule graph, test-method standards, lab qualifications, source approval, specification limits, and the full status lifecycle of a sample from "Pending" through "Approved". Every claim is live-verified on awdemo on 2026-09-30.

**Walking example — contract 282 WHITEOAK BRIDGE**:
- 3 `SampleRecord`s on contract 282 — SR #460 "999SandTest" (Material 21 "Sand", DWR 345, QAQC, Pending Authorization), SR #461 and SR #462 (both Material 59 "Flow Fill", DWR 347, QC).
- 6 `DwrAcceptanceRecord`s on contract 282 across 2 DwrItemPostings (postings 594 and 601) that reference 6 distinct `ContractProjectItemMaterialSetMaterial` rows for 5 materials.
- `MaterialSet` #1319 (MatId 21 Sand on CPI "fertilizer line") shows `EstimatedQuantity=49.0, ReportedQuantity=49.0, SatisfiedQuantity=49.0` — fully satisfied via the "SR" acceptance pathway even though SR #460 is still Pending Authorization. This surfaces an important nuance: the satisfaction rollup fires on the acceptance-record creation, not on the sample's authorization.

**Walking example — SampleRecord #22 (a sample with real test results)**:
- Material 2 "Concrete" (Portland cement), sampled on 2014-04, 3 tests queued (`SampleRecordTest` #18 "Sieve Analysis Fine & Coarse Aggregates" method `AASHTO T27`, plus Slump + Compression).
- Each test's actual numeric results stored as `DataXML` in a `SampleTestResultTemplateLog` row — e.g. `<Data><BRK1>3320</BRK1><BRK2>2430</BRK2><BRK3>3290</BRK3><BRKAVG>3013</BRKAVG><BRKDATE>04/28/2014</BRKDATE></Data>` for a 3-break Compression test.

---

### The acceptance-rule graph (`AcceptanceAction` + options + frequencies)

This is the "rule book" — one row per material-situation-rule. When an inspector posts a work-item quantity, AMS looks up which `AcceptanceAction` applies (by `RefItem` association or by `MaterialCategory` on the `ContractProjectItemMaterialSetMaterial`), reads how many samples are required per unit (via `AcceptanceActionOption` → `AccActionOptionRateFreq`), and compares to the samples already taken. The whole subgraph is lazy on awdemo — only 5 of the 999 `AcceptanceActionOption` rows have a frequency row; the rest are "general acceptance" rules without a sampling cadence.

#### Entities

| Entity | Rows | Role |
|---|---|---|
| `AcceptanceAction` | **999** | One rule per material-category-plus-name combo (e.g. "Concrete GA" / "Steel Rebar SA" / "#57 Aggregate A"). |
| `AcceptanceActionOption` | **999** | Choice variants under one action (e.g. "Option A — On-site Sample and Test" vs "Option B — Source Sample"). |
| `ActionRelationship` | **5** | Links an `AcceptanceActionOption` to a specific `MaterialTest` + `SampleType` + `AcceptanceMethod`. |
| `AccActionOptionRateFreq` | **5** | For a given option+relationship: how often (ActionFrequency), per what (FrequencyType), minimum-quantity-required. |
| `AcceptanceActionAssociation` | **17** | Hard-links a `RefItem` to an `AcceptanceAction` (overrides category-based lookup). |

#### `AcceptanceAction` key fields

| Field | Example | Note |
|---|---|---|
| `Id` | 1 | Key. |
| `Name` | `'Concrete GA'` | Human label (GA = General Acceptance, SA = Specific Acceptance). |
| `Description` | `'General Acceptance'` | |
| `EvaluationMethod` | `'Record Count'` (959) / `'Quantity'` (37) / `'Both'` (3) | How compliance is measured — count of valid sample records vs cumulative quantity sampled. |
| `RecordDescription` | `'100-Concrete'` | Legacy material-category tag; `100`/`300`/`500`/`700`/`800`/`900`/`1000` prefixes map to `MaterialCategory.Name`. |
| `CustomBusinessEntityId` + `ModelId` | 150 + 1 | Polymorphic join — `CustomBusinessEntityId=150` means `ModelId` points at `MaterialCategory`; `=148` means it points at `Material`; `=149` means `MaterialAssociation`; `=151` means `MaterialCategoryRemark`. |
| `Status` + `Active` | `'ACTIVE'`, `True` | |
| `EffectiveDate` | `'2014-04-21T00:00:00-04:00'` | |

#### `AcceptanceActionOption` key fields

| Field | Example | Note |
|---|---|---|
| `Id` | 1 | Key. |
| `AcceptanceActionId` | 1 | FK ← AcceptanceAction. |
| `Name` | `'Option A - On site Sample and Test'` | |
| `Description` | `'Slump and Compression Tests'` | |
| `Ranged` | `False` (all 999 rows) | A per-quantity-range option (e.g. different rate below/above a threshold); unused on awdemo. |
| `HasOverlappingRanges` | `False` | Validation flag — paired with Ranged. |

#### `ActionRelationship` key fields

| Field | Example | Note |
|---|---|---|
| `Id` | 1 | Key. |
| `MaterialTestId` | 4 (Slump test ASTM C143) | FK ← MaterialTest — the actual test standard. |
| `AcceptanceMethod` | `'SMPL'` (physical sample) / `'CERT'` (certified) | How material is accepted. |
| `ActionType` | `'PHYSTST'` (physical test) / `'CERT'` (cert review) | Downstream workflow. |
| `SampleType` | `'SMPL'` / `'CERT'` | What kind of sample must be taken. |
| `DocumentationType` | `'Sample Record'` | Which artifact is produced. |
| `SampleResponsibility` | `'CONSINSP'` (consultant inspector) | Who samples. |
| `TestResponsibility` | `'LABTECH'` | Who tests. |
| `SampleSize` + `SampleUnits` | `'4x8'`, `'EACH'` | Physical sample spec. |
| `TestStartDuration` | `1` | Days until test must start. |
| `SourceRequired` | `False` | Whether a source must be named. |
| `RecordType` + `RecordDescription` | `'Material Category'`, `'100-Concrete'` | Category this relationship applies to. |

#### `AccActionOptionRateFreq` key fields

| Field | Example | Note |
|---|---|---|
| `Id` | 1 | Key. |
| `AcceptanceActionOptionId` | 1 | FK ← AcceptanceActionOption. |
| `ActionRelationshipId` | 1 | FK ← ActionRelationship (ties this cadence to a test standard). |
| `ActionFrequency` | 10.0 | "One sample per **10** units." |
| `ActionRate` | 1 | Multiplier — number of samples required per frequency unit. |
| `FrequencyType` | `'Quantity'` / `'Source'` | What `10` is counted against — quantity in units or distinct source. |
| `MinQtyRequired` | 10 | Floor below which no sampling is triggered. |
| `ExcludeFromPayEstimate` | `False` | Does the acceptance roll into the PE gate? |

#### `AcceptanceActionAssociation`

Explicit per-item override. If a `RefItem` has an association row, that `AcceptanceAction` is used **instead** of the material-category default:

```odata
GET /AcceptanceActionAssociations?$filter=RefItemId eq 2918&$top=10
→ { AcceptanceActionId: 1128, RefItemId: 2918, CreatedBy: 'jgilligan1', CreatedDate: '2021-02-18' }
```

Only 17 rows on awdemo — most items fall back to the category-based rule.

#### Query template — "what tests are required for this material-set-material?"

```odata
# 1. Get the material-set material (e.g. MsetMat #1319 on CPI 4364 — fertilizer line, Sand)
GET /ContractProjectItemMaterialSetMaterials?$filter=Id eq 1319
→ MaterialId=21, EstimatedQuantity=49.0, SatisfiedQuantity=49.0

# 2. Material 21 → MaterialCategoryId = 4 (= "700 Aggregates")
GET /Materials?$filter=Id eq 21&$select=Id,Name,Description,MaterialCategoryId

# 3. Find AcceptanceActions for RefItem override OR for the material-category
# 3a. Per-item override (preferred):
GET /AcceptanceActionAssociations?$filter=RefItemId eq <refItemId>&$expand=AcceptanceAction($select=Id,Name,EvaluationMethod)
# 3b. Category fallback — note CBE+ModelId polymorphism:
GET /AcceptanceActions?$filter=CustomBusinessEntityId eq 150 and ModelId eq 4 and Active eq true
    &$select=Id,Name,RecordDescription,EvaluationMethod

# 4. For each AcceptanceAction, read its options and their frequencies:
GET /AcceptanceActionOptions?$filter=AcceptanceActionId eq 1&$expand=AccActionOptionRateFreqs($expand=ActionRelationship($expand=MaterialTest))
```

**Perf**: step 3b is a scan over 999 rows; cache the whole table once per hour. Step 4's inner `$expand` *does* work on awdemo (verified).

---

### `SampleRecord` — the sampling event

The core entity. 93 scalar properties — most are empty on any given row, but the family of fields it has is huge because this one table covers field samples, source samples, mobile samples, split samples, and mix-design samples. Of those 93 fields only ~25 are routinely populated on awdemo (the rest cover location details, mobile-GPS, mix-design, SMFMI, and legacy agency columns).

#### 428 rows on awdemo. Status distribution:

| `RefSampleStatusId` | Name | Count |
|---|---|---|
| 1 | Pending | 159 |
| 5 | In Testing | 131 |
| 4 | Received at Lab Unit | 35 |
| 8 | Complete | 32 |
| 2 | Logged | 25 |
| 3 | Received at Destination Lab | 25 |
| 7 | Void | 10 |
| 6 | Pending Authorization | 6 |
| 9 | Approved | 5 |

#### `SampleType` distribution (top)

| Code | Count | Meaning |
|---|---|---|
| `SMPL` | 302 | Standard sample |
| (null) | 66 | No type recorded |
| `QLTY` | 16 | Quality sample |
| `QUAL` | 11 | |
| `CERT` | 9 | Certified / certification sample |
| `QAQC` | 6 | QA/QC audit sample |
| `QC` | 5 | Contractor quality control |
| `IAS` | 4 | Independent Assurance Sample |
| `INFO` | 3 | Informational only |
| `VI` | 2 | Visual Inspection |

#### `AcceptanceMethod` distribution

| Code | Count | Meaning |
|---|---|---|
| (null) | 207 | None required / certified source |
| `SMPL` | 199 | Physical sample required |
| `CERT` | 8 | Vendor cert / mill cert |
| `QAQC` | 4 | QA/QC agency validation |
| `IAS` | 4 | Independent Assurance |
| `VOID` | 3 | Rejected sample |
| `SAMP` | 2 | (variant spelling of SMPL seen in newer rows) |
| `VI` | 1 | Visual |

#### Scalar fields — grouped

**Identity & lifecycle**
| Field | Example (SR #460) |
|---|---|
| `Id` | 460 KEY |
| `Name` | `'999SandTest'` |
| `ControlNumber` | `'Sand Test'` |
| `ControlType` | `'A'` |
| `LabControlNumber` | `'CN999SandTest'` |
| `LabReferenceNumber` | `(null)` — assigned when sample reaches destination lab |
| `SealNumber` | `(null)` — tamper-seal id |
| `RefSampleStatusId` | 6 (Pending Authorization) |
| `SampleStatusLastModifiedDate` | `'2024-09-04T15:35:07.6415174-04:00'` |

**People FKs** (singular; `PersonInfo` is 403 on awdemo so these resolve to raw ids only)
| Field | Example | Role |
|---|---|---|
| `SamplerId` | 1609 | Who took the sample |
| `WitnessedById` | 2 | Who witnessed |
| `AuthorizedById` | 1609 | Who signed off |
| `DWRInspectorId` | 1609 | DWR inspector |
| `DSRInspectorId` | `(null)` | Daily-source-report inspector (null here because SR #460 isn't tied to a DSR) |
| `RevisedById` | `(null)` | On an edited sample |
| `AdministrativeOfficeModifiedById` | `(null)` | Admin office override |
| `LSAURLastModifiedById` | `(null)` | Lab status audit record |
| `StartingLocCreatedByPersonInfoId` + `EndingLocCreatedByPersonInfoId` | both `(null)` | Mobile-GPS trail |

**Links to the sampled thing**
| Field | Example | Role |
|---|---|---|
| `MaterialId` | 21 (Sand) | FK ← Material |
| `SourceId` | `(null)` on #460; non-null on source samples | FK ← Source |
| `FacilityId` | `(null)` | FK ← Facility |
| `SMFMIId` | `(null)` | FK ← SourceMaterialFacilityMaterialIdentification |
| `DailyWorkReportId` | 345 | FK ← DailyWorkReport (field samples) |
| `DailySourceReportId` | `(null)` | FK ← DailySourceReport (source samples) |
| `MixDesignId` + `MixDesignTypeId` | both `(null)` | Mix-design samples |
| `BrandId` | `(null)` | FK ← Brand (for APL items) |
| `AssociatedContracts` | `'WHITEOAK BRIDGE'` | **Denormalized** display name — comma-joined contract names if the sample touches multiple. |
| `SampleRecordGroupId` | 423 | FK ← SampleRecordGroup (parent/child sample bundle) |
| `RevisingSampleId` | `(null)` | Points at the sample that supersedes this one |
| `LinkToId` + `LinkedFrom` | `(null)` | Older generic cross-link |

**What was sampled**
| Field | Example | Role |
|---|---|---|
| `SampleType` | `'QAQC'` | See distribution above |
| `AcceptanceMethod` | `'SAMP'` | See distribution above |
| `SampledFrom` | `'Site'` | Free text — `'Source'`, `'Facility'`, `'Site'`, `'Plant'`, custom |
| `SampleOrigin` | `(null)` | More structured origin code |
| `IntendedUse` | `(null)` | Free text |
| `RequestedBy` | `(null)` | Free text |
| `Reference` | `(null)` | Free text — spec reference |
| `BuyUSARequirements` | `(null)` | Buy-American source cert text |
| `BuyAmerican` | `False` | Boolean |

**Quantity & size**
| Field | Example | Role |
|---|---|---|
| `SampleSize` + `SampleSizeUnits` | both `(null)` | Physical sample size |
| `RepresentedQuantity` + `RepresentedQuantityUnits` | both `(null)` | How much production this sample stands for |

**Where it was sampled** (position on the project; most are null)
| Field | Example | Role |
|---|---|---|
| `Station` + `StationPlus` | both `(null)` | Highway station |
| `Offset` + `Distance` | both `(null)` | Lateral offset from centerline |
| `DistanceFromGrade` + `DistanceFromGradeUnits` | both `(null)` | Vertical offset |
| `Elevation` | `(null)` | |
| `Latitude` + `Longitude` | both `(null)` as strings | |
| `GeographicArea` | `(null)` | Agency region code |

**Dates**
| Field | Example | Role |
|---|---|---|
| `SampleDate` | `'2024-08-09T00:00:00-04:00'` | When taken |
| `LogDate` | `'2024-09-04T00:00:00-04:00'` | When logged into system |
| `AuthorizedDate` | `'2024-09-05T00:00:00-04:00'` | When signed off |
| `AdministrativeOfficeModifiedDate` | `(null)` | |
| `LSAURLastModifiedDate` | `(null)` | |

**Mobile GPS trail** (unused on awdemo; `IsMobile=False` everywhere)
All of `StartingX/Y/Z`, `EndingX/Y/Z`, `*LocMethod`, `*LocQuality`, `*LocQualUnit`, `*LocationIssue`, `*LocCreatedByPersonInfoId`, `*LocCreatedDate`, `*LocationUpdatedByPersonInfoId`, `*LocationUpdatedDate`, `*LocationEndActiveDate`.

**Split-sample bookkeeping**
| Field | Example | Role |
|---|---|---|
| `SplitSample` | `False` | True on the parent sample when it's split for two labs |
| `SplitSampleChild` | `False` | True on each child sample |

**Audit + agency legacy**
| Field | Example | Role |
|---|---|---|
| `RefAdministrativeOfficeId` | `(null)` | Agency office override |
| `CreatedBy` / `CreatedDate` / `LastUpdatedBy` / `LastUpdatedDate` | `'CorporateDomain\edeluca'` / `'2024-09-04T15:23:48.046851-04:00'` | Standard. |
| `Comment` | `(null)` | |
| `ENGRECDEFICIENCY` | `False` | Agency-specific "engineering record deficiency" flag — legacy soft column. |
| `IsMobile` | `False` | Was this entered from a mobile device? |

#### Nav properties (39 total, grouped)

**Reference / parent navs** (singular)
- `RefAdministrativeOffice` → `RefAdministrativeOffice`
- `Material` → `Material`
- `RefSampleStatus` → `RefSampleStatus`
- `DailyWorkReport` → `DailyWorkReport`
- `DailySourceReport` → `DailySourceReport`
- `SampleRecordGroup` → `SampleRecordGroup`
- `MixDesign` + `MixDesignType` → `MixDesign` / `MixDesignType`
- `Source`, `Facility`, `SMFMI`, `Brand` → the sampled-from locations and brand

**People navs** (singular, all 403 on expand because `PersonInfo` is denied on awdemo): `AuthorizedBy`, `DSRInspector`, `DWRInspector`, `Sampler`, `WitnessedBy`, `RevisedBy`, `LSAURLastModifiedBy`, `AdministrativeOfficeModifiedBy`, `StartingLocCreatedByPersonInfo`, `StartingLocationUpdatedByPersonInfo`, `EndingLocCreatedByPersonInfo`, `EndingLocationUpdatedByPersonInfo`

**Collection navs** (plural, where the test chain hangs off):
- `SampleRecordTests` → the tests queued on this sample
- `SampleLogs` → every status-change event (StatusType + PersonInfoId + SequenceNumber)
- `SampleTestLogs` → every test-status-change event
- `SampleRecordRemarks` → free-text notes
- `SampleRecordSources` + `SampleRecordFacilities` → multi-source/multi-facility samples
- `SampleRecordAssociations` → cross-links to other sample records
- `SampleRecordContractMaterialSetAssociations` → the per-material-set link table that powers acceptance
- `SampleRecordTagGenerations` → generated label tags
- `DwrAcceptanceRecords` → the DWR acceptance records that consume this sample

---

### `RefSampleStatus` — status lifecycle

9 rows total, no `Description`/`Active` columns populated (both `None` across the board). The lifecycle flow in practice:

```
┌─────────┐  take sample
│ Pending │ ─────────────────► Logged ──────► Received at Destination Lab (dl)
└─────────┘        1                 2                        3
                                                              │
                                                              ▼
Approved ◄── Pending Authorization ◄── Complete ◄── In Testing ◄── Received at Lab Unit
    9                 6                     8               5                    4
                                                              │
                                                              ▼
                                                            Void (7)
```

| Id | Name | What it means |
|---|---|---|
| 1 | Pending | Sample taken, not yet entered |
| 2 | Logged | Entered into system |
| 3 | Received at Destination Lab | Chain-of-custody check-in at the DL |
| 4 | Received at Lab Unit | Routed to a specific lab unit (`LabUnit` entity) |
| 5 | In Testing | Tester has started at least one test |
| 6 | Pending Authorization | Tests complete; needs sign-off |
| 7 | Void | Failed chain-of-custody / cancelled |
| 8 | Complete | Signed off at technician level |
| 9 | Approved | Final authorization — this sample now counts toward material-set satisfaction |

Note that **`SatisfiedQuantity` on `ContractProjectItemMaterialSetMaterial` fires on the `DwrAcceptanceRecord` row's creation**, not on the sample reaching status 9 — this is why MsetMat #1319 (Sand on contract 282's fertilizer line) shows `SatisfiedQuantity=49.0` even though SR #460 is still at status 6 (Pending Authorization).

#### `AutofinalizableTestStatus` — the auto-finalize list

11 rows that whitelist which `RefCodeTableValueId` values let a test skip the manual review queue. All 11 have `Autofinalizable=True`, with `CreatedBy='Script'` and the same timestamp — i.e. this is a one-time seed, not something updated per-contract.

#### `AlternateTestWorkflow`

3 rows. Each says: "when a test of this material at this lab unit transitions from `FromTestStatus` → `ToTestStatus`, use this alternate workflow." Lets specific lab units bypass certain test stages (e.g. route from status `05` straight to `40`).

#### `TestTriggeredEvent`

4 rows. Similar shape to `AlternateTestWorkflow` but one-way triggers that fire **side effects** on a test-status change (e.g. logging, assignment to a reviewer).

---

### `MaterialTest` / `SampleRecordTest` — the actual test values

`MaterialTest` is the catalog of **test methods** (104 rows). `SampleRecordTest` is a **test instance** (438 rows) queued against one sample. The numeric result is stored as structured XML in `SampleTestResultTemplateLog`.

#### `MaterialTest` — catalog (104 rows)

All 104 methods are distinct; each is a one-sentence rule:

| Field | Example (MaterialTest #3) |
|---|---|
| `Id` | 3 KEY |
| `Description` | `'Sieve Analysis Fine & Coarse Aggregates'` |
| `Method` | `'AASHTO T27'` |
| `BillCodeRequired` | `False` — whether a billing code must be entered |
| `CreatedBy` + `CreatedDate` + `LastUpdatedBy` + `LastUpdatedDate` | standard audit |

Method naming convention in awdemo:
- `AASHTO T##` — AASHTO T-series (T27=Sieve, T99=Proctor, T180=Modified Proctor, T265=Moisture, T310=Nuclear Density)
- `ASTM C##` — ASTM C-series (C39=Compression, C143=Slump)
- `TEMP`, `SlumpTest`, `Air Content`, `CompStrengthAvg` — ad-hoc test names (older seed data)
- `T-27/11C`, `T-310-95` — WVDOT-style suffix for revision year
- `JJ30TestMethod`, `FT-300`, `SIEVETESTRECORD` — agency-custom entries

#### `SampleRecordTest` — one test instance (438 rows)

| Field | Example (`SampleRecordTest` #18 on SR #22) |
|---|---|
| `Id` | 18 KEY |
| `SampleRecordId` | 22 |
| `MaterialTestId` | 3 (`AASHTO T27`) |
| `Description` | `'Sieve Analysis Fine & Coarse Aggregates'` (denormalized copy) |
| `Number` | 1.0 (test number within the sample — if 3 tests, 1/2/3) |
| `Status` | `'10'` (code — see table below) |
| `TestRuns` | 1 |
| `TestInstances` | 1 |
| `CountsTowardMAA` | `True` (counts toward Material Acceptance Audit) |
| `Required` | `False` (contractor opted-in extra tests) |
| `HasBeenCancelledOrRetested` | `False` |
| `Retest` + `RetestRequested` + `RetestQuantity` | `False` / `False` / `None` |
| `Default` | `False` |
| `RefSpecSelected` | `False` (true if a `RefSpecification` was explicitly chosen vs defaulted) |
| `TestReportable` | `True` (included on finalized report) |
| `TestUpdateable` | `True` (not locked) |
| `ResultLocked` | `False` |
| `TestRequeued` | `False` |
| `RefTestResultValueId` | `None` → not yet resulted. Would be 1=Fail / 2=Pass / 3=INFO. |
| `OriginalTestId` | `None` (set on a retest to point back) |
| `Priority` | `None` |
| `LabUnitId` | `None` (set when routed to a specific lab unit) |
| `DestinationLabId` | `None` (set at check-in) |
| `BillingInformationId` + `ChargeAmount` | `None` / `None` |
| `PlannedStartDate` + `TestStartDate` + `DueDate` + `ReceivedDate` + `EstimatedCompletionDate` + `ActualCompletionDate` | all `None` on #18 |

`Status` codes (observed): `'05'` Pending, `'10'` Logged/Queued, `'40'` Received at Lab, `'60'` In Testing, `'80'` Complete, (per observed `AlternateTestWorkflow` + `TestTriggeredEvent` transitions).

#### Results — `SampleTestResultTemplateLog`

Results are **not** stored as typed columns on `SampleRecordTest` — they are stored as **XML** in a separate `SampleTestResultTemplateLog` row keyed by `SampleRecordTestId`:

```odata
GET /SampleTestResultTemplateLogs?$filter=SampleRecordTestId eq 14&$top=5
→ { Id: 1, SampleRecordTestId: 14, AgencyEntityInstanceId: 4,
    DataXML: '<Data><BRK1>3320</BRK1><BRK2>2430</BRK2><BRK3>3290</BRK3>
             <BRKAGE> 7 Days</BRKAGE><BRKAVG>3013</BRKAVG>
             <BRKDATE>04/28/2014</BRKDATE></Data>' }
```

For a Sieve Analysis, each DataXML row holds one sieve's values:

```xml
<Data>
  <SIEVE> 3/8</SIEVE>
  <PASSEDPCT>94</PASSEDPCT>
  <RETAINPCT>6</RETAINPCT>
  <WEIGHT>3</WEIGHT>
</Data>
```

The schema of each XML is driven by `AgencyEntityInstanceId` which points at a template. **For UI**, parse the XML with `xml.etree.ElementTree` on the backend and emit a clean `{sieve, passedPct, retainPct, weight}` row.

#### `RefTestResultValue` — pass/fail code table

| Id | Name | Autofinalizable | SkipReviewTestsAllowed |
|---|---|---|---|
| 1 | Fail | `False` | `True` |
| 2 | Pass | `True` | `True` |
| 3 | INFO | `False` | `True` |

Set on `SampleRecordTest.RefTestResultValueId` when the test is finalized.

#### `SampleTestLog` — per-test state-change log

`{PersonId, SampleRecordId, SampleRecordTestId, SequenceNumber, TestStatus}` — one row per test-status transition. Use this for audit trails and for computing lab turnaround time (`max(TestStatus=='Complete').CreatedDate - min(TestStatus=='Pending').CreatedDate`).

#### `SampleLog` — per-sample state-change log

`{PersonInfoId, SampleRecordId, SequenceNumber, StatusType, Skipped}` — one row per sample-status transition (`Pending`→`Logged`→`In Testing`→…). Use this for the sample-status funnel.

#### `SampleTester`

`{SampleRecordTestId, TesterId, TesterAction}` — join table recording **who did what** on a test (`'testing'`, `'Entered test results'`, `'Finalized'`). 2,117 rows. Useful for tester workload reports.

#### `SampleTestRefSpecification`

`{SampleRecordTestId, RefSpecificationId, UseForTest}` — which spec applies to this test. 41 `RefSpecification` catalog rows (e.g. `'Sieve Analysis 2014'`), each with 1-N `RefSpecificationCondition` rows (e.g. `'Test Condition'`), each with 1-N `RefSpecificationConditionField` rows that carry the actual numeric limits:

```odata
GET /RefSpecificationConditionFields?$filter=RefSpecificationConditionId eq 1
→ { Name: '200',  ConditionFieldType: 'Numeric w/ Min/Max', MinLimit: 100.0,  MaxLimit: 1000.0 },
  { Name: '400',  ConditionFieldType: 'Numeric w/ Min/Max', MinLimit: 1001.0, MaxLimit: 2000.0 }
```

A pass/fail decision is `MinLimit ≤ lab_value ≤ MaxLimit` for each matched field.

#### `AgencyOptionReviewTestsQueue` / `AgencyOptionTestResultQueue`

11 rows each — agency-wide settings on which queues auto-populate (what statuses, what users) for the "Review Tests" and "Test Results" worklist UIs.

#### `MaterialTestAgencyView`

299 rows — one per (`MaterialTest`, `AgencyView`) pair with `EffectiveDate` + `Status`. The agency-wide view-slice of which test methods are visible in which jurisdiction.

---

### `DwrAcceptanceRecord` — tying samples to posted work

This is the handoff from Part 3's item/material chain to the QA/QC chain. Every `DwrAcceptanceRecord` row says: "On this specific `DwrItemPosting`, I'm consuming this many units of this material, and here is the sample record (or certification) that accepts it."

#### Scalar fields

| Field | Example (DAR #297 on contract 282) | Role |
|---|---|---|
| `Id` | 297 KEY | |
| `ContractId` | 282 | Denormalized FK for easy filtering. |
| `DWRItemPostingId` | 594 | FK ← DwrItemPosting (**note casing!** `DWR` uppercase here, `Dwr` on the parent `DwrWorkItem.Id`). |
| `ContractProjectItemMaterialSetMaterialId` | 1319 | FK ← the material-set row this acceptance belongs to. |
| `MaterialId` | 21 (Sand) | Denormalized from the material-set-material. |
| `MaterialUnits` | `'LBS'` | Denormalized. |
| `SampleRecordId` | 460 | FK ← SampleRecord (**null** when `ActionType='CERT'`). |
| `AcceptanceMethod` | `'SAMP'` (6) / `'CERT'` (5) / `'VI'` (1) / `'QMP'` (1) / `'SAMP'` (1) | How this specific posting is accepted. |
| `ActionType` | `'PHYSTST'` (6) / `'CERT'` (6) / `'SR'` (3) / `'MATTST'` (2) / `'VI'` (1) / `'DWRAV'` (1) / `'DWRFIV'` (1) | Follow-up workflow type. |
| `SampleType` | `'SMPL'` | Denormalized from the sample. |
| `WorkLocation` | `'Centerlane'` | Free text location on the project. |
| `RepresentedQuantity` | 49.0 | How much the sample stands for. |
| `ConversionFactor` | 1.0 (sometimes 0.2 for lb→kg or mix conversions) | Multiplier to convert posted-item units into material units. |
| `SMFMIDecrementation` | `False` or `True` | If true, decrements the source-material-facility-material stockpile too. |
| `FieldInspectionValue` | observed on some rows | For VI (visual inspection) rows, the value seen in the field. |

#### 224 rows on awdemo

Mostly on the older seed contracts (contract 12 has the richest acceptance chain). Contract 282 has 6 — tabulated above in the SampleRecord walking example.

#### Nav

- `DwrItemPosting` → the posting this acceptance consumes
- `SampleRecord` → the sample (nullable)
- `ContractProjectItemMaterialSetMaterial` → the material-set row
- `Material` → the material
- `Contract` → convenience back-link

---

### `Material`, `MaterialCategory` — the material catalog

#### `MaterialCategory` (38 rows total — top 10 shown)

| Id | Name | Description |
|---|---|---|
| 1 | `100` | Concrete |
| 2 | `300` | Rebar |
| 3 | `500` | Asphalt |
| 4 | `700` | Aggregates |
| 5 | `900` | Binders |
| 6 | `1000` | Water |
| 8 | `800` | Erosion Control |
| 10 | `702` | Structural Concrete (INDOT) |
| 11 | `501 JPW` | Portland Cement Concrete Pavement |
| 14 | `POLY` | POLYMERS |

#### `Material` (83 rows)

Each `Material` has: `Name` (spec #), `Description`, `MaterialShortName`, `MaterialCategoryId`, `EnglishUnit`+`MetricUnit`, flags (`BrandNameRequired`, `ControlNumberRequired`, `SourceFacilityRequired`, `TypeSizeClassRequired`, `Recycled`, `Research`, `Active`), `Status`, `PrintLabelCopies`.

Example — Material #21:
```
{ Id: 21, Name: '700.05', Description: 'Sand', MaterialShortName: 'Sandy',
  MaterialCategoryId: 4, EnglishUnit: 'LBS', MetricUnit: 'kg',
  Active: True, Status: 'ACTIVE' }
```

#### Related — `AlternateMaterial` (21), `MaterialAssociation` (17), `MaterialSamplingQualification` (44)

- `AlternateMaterial` — "when Material X isn't available, Material Y is an acceptable substitute." `{MaterialId, AltMaterialId, UseAlternateMaterialSpec}`.
- `MaterialAssociation` — component materials (polymorphic self-link; e.g. "Concrete Class A is composed of Cement + Water + Sand + Aggregate").
- `MaterialSamplingQualification` — which `TestingQualification`s a sampler needs to sample a particular material.

---

### `Lab` & qualifications

AMS splits labs into two tiers: **Destination Labs** (where samples are received for routing) and **Lab Units** (where testing is physically performed).

#### `Lab` (48 rows total — first 10)

| Id | Name | Status | Description |
|---|---|---|---|
| 1 | `Central DL` | Active | Central Destination Lab (Bypass) |
| 2 | `District South DL` | Active | District South Destination Lab |
| 3 | `District North DL` | Active | District North Destination Lab |
| 4 | `South Regional LU` | Active | South Regional Lab Unit |
| 5 | `South Region LU2` | Active | |
| 6 | `North Region LU1` | Active | |
| 7 | `North Region LU2` | Active | |
| 8 | `Central LU` | Active | Central Lab Unit (Bypass) |

#### Qualification matrix

- `LabSamplingQualification` (31) + `LabTestingQualification` (85) — per-lab, which methods it can sample / test for.
- `LabSampler` (146) + `LabTester` (295) + `LabCalibrator` (16) — per-lab personnel qualification join tables (join to `PersonInfo` on awdemo returns 403, so these are id-only on awdemo).
- `TestingQualification` (200) + `SamplingQualification` + `MaterialSamplingQualification` (44) + `TestEquipmentQualification` (6) — person-level and equipment-level credentials, each with `EffectiveDate` + `Status`.

#### `DestinationLab` (13) + `LabUnit` (21)

`DestinationLab`/`LabUnit` are specializations of `Lab` with narrower navigation. Use these when you need to route samples; use `Labs` for a generic lab list.

#### `StormwaterInspectorQualification` (2)

Separate qualification table for stormwater inspectors (not sample testers). `{PersonInfoId, QualificationType: 'Storm Water Insp', EffectiveDate, Status}`. On contract 282 the sole stormwater-qualified inspector active for 2024 is PersonInfo #1609 (same person as the DWR inspector).

---

### `Source`, `SourceMaterial`, `FacilityMaterial` — approved supply

The "where did this material come from?" chain. A **Source** is a vendor's physical production location (plant, mine, mill, facility); a **Facility** is a storage or receiving location; a **SMFMI** (`SMFMIId` on `SampleRecord`) is the join record identifying "this material at this source at this facility".

#### `Source` (65 rows)

| Field | Example (Source #1) |
|---|---|
| `Id` | 1 |
| `Name` | `'10'` (sequence tag) |
| `Description` | `'Cemex (Concrete)'` |
| `City` | `'Gainesville'` |
| `Type` | `'MANU'` / `'DIST'` / `'PROD'` / etc. |
| `GeographicArea` | `'WEST'` |
| `DBEType` | `'DBE'` |
| `RefVendorId` | 337 — FK to the actual vendor record |
| `ApprovalLevelType` | `'1'` |
| `IsLatestVersion` | True |
| `LocationType` | `'CITY'` |
| `SourceManagementLevelId` | 1 (regional vs local) |
| `SequenceNumber` | 2 |
| `Status` + `Active` + `EffectiveDate` + `Archive` | standard lifecycle |

#### `SourceMaterial` (75 rows) — "this source produces this material"

`{SourceId, MaterialId, EffectiveDate, Status, ApprovalStatus: 'APPR'/null}`.

#### `FacilityMaterial` (87 rows) — "this facility stocks this material"

`{FacilityId, MaterialId, EffectiveDate, Status}`.

#### `SourceMaterialFacilityMaterialIdentification` ("SMFMI")

Full join record pulling source+material+facility together with its own `ApprovalStatus`. `SampleRecord.SMFMIId` points at this if a sample is tied to a specific supplier-location-material combo.

#### `SourceAgencyView`, `FacilitySourceAuthority`, `SourceSourceAuthority`, `SourceManagementLevel`, `SourceManagementLevelAssignment`

Agency-view and permission control for who can authorize new sources.

#### Approved Product List (APL)

**Not populated as a separate entity in awdemo** — the APL concept is handled via `Material.BrandNameRequired=True` + the `BrandId` nav on `SampleRecord`. For a brand-controlled material (e.g. a specific proprietary pipe), the sample must cite a brand that's on an approved brand list — but awdemo has `BrandId=None` on every sample and no exposed `/Brands` entity set. **Document as "schema supports APL via `Brand`+`BrandId`; awdemo has no live data to walk."**

#### `DailySourceReport` + `DsrMaterial` + `DsrInspection`

Separate QA stream for **source inspections** (vs sample-based acceptance). 38 DSRs, 7 DsrMaterials, 2 DsrInspections, 1-2 remarks per DSR. The DSR records a daily visit to a source, which materials were inspected, what was found. `SampleRecord.DailySourceReportId` ties a source-based sample to its parent DSR.

```odata
GET /DailySourceReports?$filter=InspectorId eq 932&$orderby=Date desc&$top=10&$expand=DsrMaterials($expand=Material)
```

---

### Stormwater & environmental

Separate but parallel chain. `StormwaterInspectorQualification` for inspectors; `StormwaterPeriodStormwaterEvents` on DWRs (covered in the DWR chapter of the combined doc). The combined doc's Part 2 noted that `RefWeather.StormwaterEvent=True` triggers a stormwater period on the related `StormwaterPeriod` record. There is no separate `StormwaterSample` table — stormwater events on awdemo are discharge/compliance records, not material-quality samples.

---

### Loading a QA/QC chain efficiently

Our FastAPI backend currently has **no QA/QC routes** — this is a gap. The queries below are proposals; each notes the route it would live at.

#### 1. Minimum sample card (row in a list)

**Question**: "Give me 50 sample records with resolved material name and status."

```odata
GET /SampleRecords
    ?$filter=DailyWorkReportId in (<ids>)
    &$select=Id,Name,ControlNumber,LabControlNumber,SampleType,AcceptanceMethod,
             SampleDate,AuthorizedDate,MaterialId,RefSampleStatusId,DailyWorkReportId
    &$expand=Material($select=Id,Name,Description),
             RefSampleStatus($select=Id,Name)
    &$orderby=SampleDate desc
    &$top=50
```

**Perf**: single call, both `$expand`s hydrate (verified live). ~250 ms cold.
**Where it should live**: new `api/routes/samples.py` → `GET /api/samples`.
**Where it does today**: nowhere — but `dwr_with_items_and_materials_async` already pulls the sample list for a DWR as a side-effect (`samples` collection on the result).

#### 2. Full sample detail

**Question**: "Give me everything about SR #460 including tests + results + state-change logs + acceptance records that reference it."

```odata
# Primary fetch
GET /SampleRecords?$filter=Id eq 460
    &$expand=Material($select=Id,Name,Description,MaterialCategoryId),
             RefSampleStatus($select=Id,Name),
             SampleRecordRemarks($select=Id,Remark,CreatedBy,CreatedDate;$orderby=CreatedDate desc)

# Parallel fan-out (asyncio.gather)
GET /SampleRecordTests?$filter=SampleRecordId eq 460
GET /SampleLogs?$filter=SampleRecordId eq 460&$orderby=SequenceNumber
GET /SampleTestLogs?$filter=SampleRecordId eq 460&$orderby=SequenceNumber
GET /SampleTesters?$filter=SampleRecordTestId in (<test ids>)
GET /SampleTestResultTemplateLogs?$filter=SampleRecordTestId in (<test ids>)
GET /SampleTestRefSpecifications?$filter=SampleRecordTestId in (<test ids>)
GET /DwrAcceptanceRecords?$filter=SampleRecordId eq 460
```

**Perf**: 1 serial + 7 parallel = ~1 round-trip-time + max(7 fan-outs). ~400 ms cold on awdemo.
**Where it should live**: `GET /api/samples/{id}` — mirror the `dwr_with_items_and_materials_async` 9-query fan-out pattern.

#### 3. A material's test history across a contract

**Question**: "Show me every sample taken of Material 21 (Sand) on contract 282."

```odata
# Step 1: get contract 282's DWR ids
GET /DailyWorkReports?$filter=ContractId eq 282&$select=Id&$top=99
→ [340, 341, ..., 353]

# Step 2: samples for Material 21 on those DWRs
GET /SampleRecords?$filter=MaterialId eq 21 and DailyWorkReportId in (340,341,...,353)
    &$expand=RefSampleStatus($select=Name)
    &$orderby=SampleDate desc
```

**Perf**: two calls. The second's `IN` filter is capped around 50 ids — chunk if a contract has >50 DWRs (contract 282 has 13).
**Where it should live**: `GET /api/contracts/{id}/materials/{materialId}/samples`.

#### 4. Contract QA/QC compliance dashboard — status × type matrix

**Question**: "For contract 282, show me a status × sample-type matrix of all samples."

```odata
# Fetch all samples once, pivot client-side
GET /SampleRecords?$filter=DailyWorkReportId in (<dwr ids>)
    &$select=Id,RefSampleStatusId,SampleType,SampleDate
    &$top=999
```

Then on the backend pivot into `{SampleType: {StatusName: count}}`.

**Perf**: single call per contract, cache 60s. Expands skipped — just two numeric fields pivoted.
**Where it should live**: `GET /api/contracts/{id}/qaqc/summary`.

#### 5. "What tests are required to accept this material?"

```odata
# Starting from a RefItem (or a Material)
# 5a. Per-item override check
GET /AcceptanceActionAssociations?$filter=RefItemId eq <refItemId>
    &$expand=AcceptanceAction($expand=AcceptanceActionOptions($expand=AccActionOptionRateFreqs($expand=ActionRelationship($expand=MaterialTest))))

# 5b. Material-category fallback
GET /AcceptanceActions?$filter=CustomBusinessEntityId eq 150 and ModelId eq <catId> and Active eq true
    &$expand=AcceptanceActionOptions($expand=AccActionOptionRateFreqs($expand=ActionRelationship($expand=MaterialTest)))
```

**Perf**: the nested `$expand` chain *does* hydrate on awdemo (verified), but the response can get large if the category has many actions (e.g. category 4 "Aggregates" has 222 actions). **Mitigation**: `$top=5` on the outer `$expand=AcceptanceActions`, or do the join client-side with 2 round trips.
**Where it should live**: `GET /api/materials/{id}/acceptance-rules`.

#### 6. Inspector's authorization queue

**Question**: "What samples are waiting for me (DWRInspector) to authorize?"

```odata
GET /SampleRecords?$filter=RefSampleStatusId eq 6 and DWRInspectorId eq <me>
    &$expand=Material($select=Name,Description),
             DailyWorkReport($select=Id,DwrDate,ContractId)
    &$orderby=LogDate asc
    &$top=100
```

Status `6` = `'Pending Authorization'`. **Perf**: single call, both expands hydrate. ~150 ms warm cache.
**Where it should live**: `GET /api/me/qaqc/pending`.

#### 7. Failed tests feed

**Question**: "Show me every sample where any test failed."

```odata
# Samples with at least one failed test
GET /SampleRecordTests?$filter=RefTestResultValueId eq 1   # 1 = 'Fail'
    &$expand=SampleRecord($select=Id,Name,ControlNumber,MaterialId,RefSampleStatusId;
             $expand=Material($select=Name,Description))
    &$orderby=LastUpdatedDate desc
    &$top=100
```

**Perf**: single call. Expand chain hydrates. ~200 ms.
**Where it should live**: `GET /api/qaqc/failures`.

#### 8. The anti-pattern

**Don't** try to `$expand=SampleRecordTests($expand=SampleTestResultTemplateLogs)` on all samples of a contract in one call. On awdemo this times out past ~20 samples. Instead:

```python
# Right pattern — two tiers of fan-out
async def contract_qaqc_full(contract_id: int):
    dwr_ids = (await c.get("DailyWorkReports",
                            filter=f"ContractId eq {contract_id}",
                            select="Id"))["value"]
    samples = (await c.get("SampleRecords",
                           filter=f"DailyWorkReportId in ({','.join(d['Id'] for d in dwr_ids)})",
                           top=500))["value"]
    sample_ids = [s["Id"] for s in samples]
    # chunk sample_ids into 50s, parallel-fan-out
    tests_by_sample, results_by_test, logs_by_sample = await asyncio.gather(
        _fetch_in_chunks("SampleRecordTests", "SampleRecordId", sample_ids),
        # later: fetch results keyed on test ids
        _fetch_in_chunks("SampleLogs", "SampleRecordId", sample_ids),
    )
```

Mirror the `dwr_aggregates_async` helper's 5-batched-query strategy.

---

### UI query recipes

Dashboard-ready queries. Each returns a flat JSON row set a chart or table can consume directly.

#### R1. Portfolio pending-authorization queue (across all contracts)

```odata
GET /SampleRecords?$filter=RefSampleStatusId eq 6
    &$select=Id,Name,DWRInspectorId,DailyWorkReportId,LogDate,MaterialId
    &$expand=Material($select=Name)
    &$orderby=LogDate asc
    &$top=200
```

Group by `DWRInspectorId` → "N samples awaiting authorization by person #X, oldest Y days".

#### R2. Failed tests feed with context

```odata
GET /SampleRecordTests?$filter=RefTestResultValueId eq 1
    &$expand=SampleRecord($select=Id,Name,DailyWorkReportId;
             $expand=Material($select=Name,Description),
                     DailyWorkReport($select=Id,DwrDate,ContractId))
    &$orderby=LastUpdatedDate desc
    &$top=200
```

#### R3. Lab turnaround-time (TAT) histogram

```odata
# Pull SampleLogs for all samples in a contract's lifetime
GET /SampleLogs?$filter=SampleRecordId in (<ids>)
    &$select=SampleRecordId,SequenceNumber,StatusType,CreatedDate
    &$top=999
```

Client-side: for each sample, compute `CreatedDate(StatusType='Complete') - CreatedDate(StatusType='Logged')`. Histogram bucket by day → "P50 = X days, P90 = Y days".

#### R4. Materials-without-required-samples exception feed

```odata
# For a contract: all material-set-materials whose SatisfiedQuantity < ReportedQuantity
GET /ContractProjectItemMaterialSetMaterials?$filter=ContractProjectItemMaterialSetId in (<mset_ids>)
    and SatisfiedQuantity lt ReportedQuantity
    &$select=Id,MaterialId,EstimatedQuantity,ReportedQuantity,SatisfiedQuantity,Insufficient
    &$top=200
```

Then join to `Material.Name` client-side. Chart as: "N posted-but-not-sampled rows, representing M units of material X."

#### R5. By-contract QA/QC leaderboard

```odata
# All samples, grouped by contract
GET /SampleRecords?$select=Id,DailyWorkReportId,RefSampleStatusId&$top=999
GET /DailyWorkReports?$select=Id,ContractId&$top=999  # for the DWR→contract join
```

Pivot client-side: `{ContractId: {Authorized: n, Pending: n, Failed: n}}`.

#### R6. Inspector / Tester workload

```odata
# Sampler workload — who's taking the most samples
GET /SampleRecords?$filter=SampleDate ge <since>
    &$select=Id,SamplerId,SampleDate&$top=999
```

Pivot `{SamplerId: count}`. For tester workload, pivot `/SampleTesters` on `TesterId`.

#### R7. Upcoming required tests (predict next sample due)

Compute from the acceptance-rule graph:
1. Pull all `MsetMats` for a contract with `ReportedQuantity > 0` and `SatisfiedQuantity < ReportedQuantity`.
2. For each, look up its `AcceptanceAction` → `AccActionOptionRateFreq`.
3. If `FrequencyType='Quantity'` and `ActionFrequency=10`, next sample is due when `ReportedQuantity` crosses the next multiple of 10 — compute the gap.

```python
next_due_qty = math.ceil(reported_qty / freq) * freq - satisfied_qty
```

Surface the top-N "closest to sampling threshold" rows.

#### R8. Certified-source percentage

**Question**: "What fraction of this contract's material acceptances were by certification vs physical sampling?"

```odata
GET /DwrAcceptanceRecords?$filter=ContractId eq 282
    &$select=Id,AcceptanceMethod&$top=999
```

Pivot `{AcceptanceMethod: count}` → donut. On contract 282: 6 total, mix of `null`/`CERT`/`SAMP`/`SMPL`.

#### R9. Lab utilization

```odata
# Which labs/lab-units are testing the most?
GET /SampleRecordTests?$filter=LabUnitId ne null
    &$select=Id,LabUnitId,Status,TestStartDate&$top=999
GET /Labs?$filter=Id in (<lab_unit_ids>)&$select=Id,Name
```

Pivot `{LabName: count}` → bar.

#### R10. Source approval heatmap

```odata
# For a material: which sources have active approval?
GET /SourceMaterials?$filter=MaterialId eq <id> and Active eq true and ApprovalStatus eq 'APPR'
    &$expand=Source($select=Id,Name,Description,City,RefVendorId,GeographicArea)
```

Group `{GeographicArea: [SourceName, ...]}` → map or heat-grid.

---

### How to display QA/QC

#### Sample detail page (new — doesn't exist yet)

Propose seven sections, mirroring the DWR detail page's structure:

1. **Identity header** — Name · ControlNumber · LabControlNumber · Material (link) · Status pill · AuthorizedDate (with "n days to auth" subtitle)
2. **The sample** — SampleType · AcceptanceMethod · SampledFrom · SampleDate · LogDate · Source (link if set) · Facility (link if set)
3. **People** — Sampler, Witness, DWRInspector, AuthorizedBy (ids only on awdemo — show as `#1609` with a tooltip explaining the awdemo 403)
4. **Tests queue** — table of `SampleRecordTest`s with number, description, method (from `MaterialTest.Method`), status (code → label), pass/fail (`RefTestResultValue.Name`), lab unit, test start/complete dates
5. **Results** — for each resulted test, parse the `SampleTestResultTemplateLog.DataXML` and render as a small structured block (e.g. for a Compression test: `BRK1 BRK2 BRK3 → avg`; for a Sieve: a mini sieve-size → %passed table)
6. **State-change log** — SampleLog + SampleTestLog, interleaved by `CreatedDate`, as an audit trail
7. **Acceptance records** — the `DwrAcceptanceRecord`s that reference this sample, linking to each posting

#### Contract-level QA/QC tab (new on contract detail page)

Four panels across the top:
- **Samples by status funnel** (SampleStatus distribution for this contract)
- **Pending authorization count** with "oldest N days" subtitle
- **Failed tests count** with recent list
- **Materials without required samples** exception count

Below: a table of material-set-materials where `SatisfiedQuantity < EstimatedQuantity`, color-coded by how close they are to insufficient.

#### Hero numbers (5 of them)

1. **Samples authorized / pending / failed** (3-up count — the top-of-funnel KPI)
2. **% passing** — `count(Pass) / count(Pass + Fail)` on `SampleRecordTest.RefTestResultValueId`
3. **P50 days to authorization** — median `AuthorizedDate - LogDate`
4. **Materials fully satisfied** — fraction of `MsetMat` rows where `SatisfiedQuantity >= EstimatedQuantity`
5. **Open required samples** — materials with `Insufficient=False` but `SatisfiedQuantity < ReportedQuantity`

#### Visualizations that pay off

| Chart | Data | Question answered |
|---|---|---|
| **Sample-status funnel** | `SampleLog` sequence of StatusType per sample | "Where does our sample pipeline bottleneck?" |
| **Test-result scatter vs spec** | Parse `SampleTestResultTemplateLog.DataXML` + `RefSpecificationConditionField` min/max | "How close are we running to spec limits?" |
| **AcceptanceMethod bar** | `DwrAcceptanceRecord.AcceptanceMethod` distribution | "What's our mix of SAMP / CERT / SRC / VI acceptance on this contract?" |
| **Re-sample chains** | `SampleRecord.RevisingSampleId` chain | "How often do we have to re-sample this material?" |
| **Lab TAT histogram** | `SampleTestLog` complete − logged | "Which labs are the bottleneck?" |
| **Material satisfaction heatmap** | Per-CPI `MsetMat.SatisfiedQuantity / EstimatedQuantity` | "Which items are at risk of a payment hold?" |

#### What NOT to visualize

- `SampleRecord` location fields (`Station`, `Latitude`, `Longitude`, `Elevation`, `Distance`, `DistanceFromGrade`) — null on 99%+ of awdemo rows.
- `SampleRecord` mobile-GPS fields (`StartingX/Y/Z`, `EndingX/Y/Z`, every `*LocMethod`/`*LocQuality`) — `IsMobile=False` everywhere; 100% empty.
- `SampleRecord.BuyAmerican` / `BuyUSARequirements` — all `False` / `None` on awdemo.
- `SampleRecord.Elevation` as a number — stored as `Edm.Int64` but every row is null.
- `SampleRecordTest.BillingInformationId` / `ChargeAmount` — billing is agency-config, awdemo has none.
- `SampleRecordTest.Priority` — all `None`.
- Trying to show `PersonInfo` names anywhere — awdemo returns 403 on both direct query and expand. Show the id with a tooltip.
- `AutofinalizableTestStatus` rows — pure config, not useful to display.

---

### Awdemo gotchas specific to QA/QC

1. **Entity-set name quirks:**
   - `RefSampleStatuses` (plural) — not `RefSampleStatus`. Direct singular path returns 404.
   - `SourceAuthorities` → **404** (schema shows a Source permission entity, but the OData set doesn't exist in awdemo).
   - `TestEquipment` → **404** at the plural; works through child nav from a qualification record only.
   - `TestAssignmentInfos` → **404**.
2. **`DWRItemPostingId` casing flip on `DwrAcceptanceRecord`**: parent entity is spelled `DwrItemPosting` (lowercase 'wr'), FK column is `DWRItemPostingId` (uppercase 'WR'). Caught the first doc on this; still catches you here.
3. **PersonInfo 403**: all `*ById`/`*InspectorId`/`SamplerId`/`AuthorizedById`/`WitnessedById`/`TesterId`/`PersonInfoId`/`PersonId` fields across every QA/QC entity cannot be hydrated via `$expand=Sampler($select=…)`. Show raw ids, add a tooltip explaining the lab limitation.
4. **`SampleTestResultTemplateLog.DataXML`** is a string of XML, not a typed sub-record. Parse backend-side; the schema is driven by `AgencyEntityInstanceId`.
5. **`ContractProjectItemMaterialSetMaterial.SatisfiedQuantity` fires on acceptance-record creation**, not on sample authorization. SR #460 is Pending Authorization (status 6) but its MsetMat #1319 reads `SatisfiedQuantity=49.0`. If you want "truly accepted" quantity, you need to filter DARs by `SampleRecord.RefSampleStatusId eq 9` client-side.
6. **`AcceptanceMethod` has two spellings on `SampleRecord`**: `SMPL` (older convention, 199 rows) and `SAMP` (newer, 2 rows). Treat them as the same thing.
7. **`AcceptanceAction` + `ModelId` is polymorphic**: `CustomBusinessEntityId` tells you which table `ModelId` points at (`148`=Material, `149`=MaterialAssociation, `150`=MaterialCategory, `151`=MaterialCategoryRemark). You must join via `CustomMetadata` first; a bare `/AcceptanceActions?$filter=ModelId eq 4` gives you concrete-category rows + concrete-material rows + association rows mixed.
8. **`RefSampleStatus.Active` is null across all 9 rows** (not `False` — null). Filter by `Id` not by `Active`.
9. **`AccActionOptionRateFreqs` is radically under-populated** — 5 rows for 999 options. This is a seed-data limitation; in a real deployment every option has a frequency.
10. **`StormwaterInspectorQualifications`** has only 2 rows; `QualificationType` is free-text (`'Storm Water Insp'`) — no code table.
11. **`AcceptanceActionAssociation` is sparse** (17 rows) — most items fall back to the material-category rule from `AcceptanceAction` via `CustomBusinessEntityId=150, ModelId=<MaterialCategoryId>`.
12. **`SampleRecordTest.Status`** uses a different code set than `RefSampleStatus` (`'05'`, `'10'`, `'40'`, `'60'`, `'80'`). The decode table isn't exposed as a RefX entity on awdemo — codes are documented in `AlternateTestWorkflow.FromTestStatus`/`ToTestStatus` and `TestTriggeredEvent.FromTestStatus`/`ToTestStatus` as free-text strings.
13. **`AssociatedContracts` on `SampleRecord` is a denormalized comma-separated string** — useful for display, but don't rely on it for joins. Use `DailyWorkReportId → ContractId` as the authoritative join.
14. **`ContractorMaterials`, `ContractorMaterialSources`, `ContractorMaterialLogs`, `AutofinalizableSampleSettings`** are all 0 rows on awdemo. Document from EDMX only — "schema supports contractor-side material self-reporting; awdemo has no live data."
15. **`SuppliedMaterials` has 1 row** — the whole contractor-supplied-materials chain is essentially unpopulated on awdemo.
16. **No separate `ApprovedProductList` / `Brand` entity set** on awdemo — brand-based acceptance exists in schema (`SampleRecord.BrandId`, `Material.BrandNameRequired`) but no live data to walk.
17. **`SMFMIId`** (SourceMaterialFacilityMaterialIdentification) — the join record exists in schema but is 0 rows on contract 282's samples; appears populated only on older contract-12 seed data.

---

<a id="part-7-schedule-time-charges-workflow"></a>

# Part 7 — Schedule, time charges & workflow

_The time layer: contract calendar and days-charged, progress schedules, milestones, suspensions, weather-impact tracking, and the contract-lifecycle workflow state machine._

Companion to `docs/ams-business-flows-2026-09-30.md`. That document covered the *what* of a contract — labor hours, dollars, and material movement. This one covers the ***when*** and the ***who-signs-what-next*** — the calendar that governs liquidated damages, the time‑charge ledger that debits available days as the crew works, the handful of informational date fields that pin a contract to real‑world milestones, and the workflow state machine that an agency uses to route proposals, change orders, payrolls, and DBE commitments through review. Everything below is verified against **contract 282 (WHITEOAK BRIDGE)** on `ams-lab/awdemo`.

### Conventions

- Shared vocabulary (`ContractId`, `Expand(path)`, `$filter` operators, how the lab returns 403/404 for restricted sets) is described in the companion doc; this file does not repeat it.
- Every query shown here was executed against `https://api.aashtoware.org/ams-lab/awdemo/` at the time of writing. Where awdemo returns nothing meaningful, the section says so and reproduces the empty shape rather than inventing a sample.
- All timestamps in awdemo are `Edm.DateTimeOffset` in eastern-US offsets (`-04:00` / `-05:00`). Filter them with ISO‑8601 and `Z` or offset literals.
- **Entity-set naming inconsistencies** — `ContractTime` is a single OData set that holds subtypes; `ContractTimeAvailable`, `ContractTimeCalendar`, `ContractTimeCompletion`, `ContractTimeInformational`, `ContractTimeRecurring` are **not** independent entity sets (requesting `/ContractTimeAvailables` returns `404`). You cast with `isof()` or filter on the base `Type` column.

### Entity-set totals (awdemo, lab)

| Set | Count | Notes |
|---|---:|---|
| `ContractTimes` | 1068 | Base + subtypes merged; filter on `Type` string |
| `ContractProgressSchedules` | 7 | Sparsely populated on awdemo; only 3 contracts have any |
| `ChangeOrderTimeAdjustments` | 20 | 11 of the 20 have an explanation attached |
| `ChangeOrderTimeAdjustmentExplanations` | 8 | FK → `ChangeOrderTimeAdjustment` |
| `DwrContractTimes` | 328 | One per DWR × ContractTime where the DWR touched a chargeable time |
| `DiaryContractTimes` | 97 | Diary‑level time‑charge entries |
| `DiaryContractTimeAdjustments` | 14 | Per‑PE adjustments on diary charges |
| `PaymentEstimateContractTimeCharges` | 94 | Rollup from diary adjustments into a PE |
| `WeeklyTimeCharges` | 3 | Only 3 rows total across the lab — used by agencies that charge weekly |
| `ContractTimeRecurrEvents` | 76 | Per‑event tracker on `ContractTimeRecurring` schedules |
| `Workflows` | 12 | 3 construction + 9 ancillary (payroll, DBE, SBP, sub‑payment, bidder/quoter) |
| `WorkflowPhases` | 97 | Phases across all 12 workflows |
| `RefWeather` | 5 | Cloudy · Isolated Storms (stormwater=true) · Partly Cloudy · Sunny · Rainy |
| `RefContractTimes` | 33 | Reference catalog of pre‑configured ContractTime templates |
| `CAPPhases` | 63 | **Different thing** — Contingency Assignment Profile phases (budget/cost side), not calendar |
| `DailyDiaries` | 86 | Diary rows |
| `DailyDiaryRemarks` | 27 | Free‑text notes on a diary |
| `CTAvailableSuspendResumes` | 2 | Only two historical suspensions in the lab (2018, 2019) |
| `StormwaterPeriods` | 8 | Compliance tracker; connects weather → SWPPP inspections |
| `ScheduledProcesses` | — | `403 Access Denied` on awdemo (admin‑only) |
| `WorkFlowPhaseAccessRights` | — | `404` on awdemo (not surfaced as an entity set) |

---

### 1 · Contract calendar & time charges

#### Overview

AMS does not store a single "contract duration" field. Instead, each contract carries a **collection of `ContractTime` rows**, each one a different kind of calendar fact: informational dates (award, NTP, execute), chargeable available-time counters that debit as the crew works, calendar‑time counters that debit on every calendar day regardless of work, completion dates with liquidated‑damages math attached, and recurring templates that fire scheduled events. The one row that actually governs liquidated damages for construction is the chargeable **Available Time** row.

```
Contract (1) ──* ContractTime (abstract base, discriminated by `Type`)
                 │
                 ├─ Type = "Informational"   dates only, no counter
                 ├─ Type = "Calendar Time"   debits by calendar days
                 ├─ Type = "Available Time"  debits only when ContractorWorking=true  ★ the liq-dam one
                 ├─ Type = "Completion Date" fixed-date deadline
                 └─ Type = "Recurring"       ──* ContractTimeRecurrEvent (planned vs actual)

ContractTime (Available) (1) ──* DwrContractTime           (per DWR)
                             ──* DiaryContractTime (1) ──* DiaryContractTimeAdjustment (per PE)
                             ──* PaymentEstimateContractTimeCharge  (period roll-up)
                             ──* ChangeOrderTimeAdjustment          (CO extensions)
                             ──* CTAvailableSuspendResume           (work stop/resume pairs)
                             ──* ContractAdjustment (type ∈ {Liquidated Damage, Disincentive, Incentive})
```

#### 1.1 `ContractTime` — base + five subtypes

Purpose: the master row for one calendar fact (one date, one counter, one deadline, one recurring schedule) attached to one contract.

| Field | Edm type | Notes |
|---|---|---|
| `Id` | Int64 PK | |
| `ContractId` | Int64 FK | |
| `Name` / `Description` | String | `Name` is usually the `RefContractTime.Name` the row was templated from (e.g. `99Avail`) |
| `Type` | String enum | `Informational`, `Calendar Time`, `Available Time`, `Completion Date`, `Recurring` — **the discriminator** |
| `AgencyType` | String | Per‑agency free label (`CRIT`, `MAIN`, `Key`, …); drives UI grouping |
| `Unit` | String | `Days`, `WorkDays`, `Hours`, `None` |
| `RequiredFor` | String | `Active Contract`, `Neither`, `All`, … (gating rule) |
| `OriginalNumberOfTimeUnits` | Decimal | The original award value |
| `AdjustedNumberOfTimeUnits` | Decimal | Sum of all approved CO time adjustments (negative shrinks) |
| `CurrentNumberOfTimeUnits` | Decimal | `Original + Adjusted` — the authoritative "days allowed" today |
| `PendingNumberOfTimeUnits` | Decimal | Pending (unapproved) CO deltas |
| `PercentComplete` | Decimal | `TimeCharged / Current` on the counter subtypes |
| `StartTime` | DateTimeOffset | When the counter started ticking |
| `ActualCompletionDate` | DateTimeOffset | When the counter was stopped |
| `EstimateProcessingComplete` | DateTimeOffset | Timestamp the time charges finished rolling into a PE |
| `LiqDamRate`, `LiqDamRateTimeUnit`, `LiqDamCap`, `LiqDamTotal` | Decimal/Str | Liquidated‑damage math; `CalculateLiqDamage` toggle |
| `IncentiveRate`, `IncentiveCap`, `IncentiveTotal` | Decimal | Incentive math; `CalculateIncentive` toggle |
| `DisincentiveRate`, `DisincentiveCapAmount`, `TotalDisincentiveAmountApplied` | Decimal | Disincentive math; `CalculateDisincentive` toggle |
| `Chargeable` | Bool | True iff a counter subtype that debits |
| `Main` | Bool | Marks the single "primary" Available Time per contract — important for KPI selection |
| `DefaultIndicator` | Bool | This row came from a `RefContractTime` template with `DefaultOnNewContract=true` |
| `Status` | String | `ACTIVE`, `INACTIVE`, `COMPLETE` |
| `GENDATE01`–`GENDATE10`, `GENTEXT01`–`GENTEXT06`, `GENNUM01`–`GENNUM08`, `CMPCT51`, `CMTM51`, `PSPROPID`, `PSSITNUM`, `TIMEFRCT` | — | **Agency "general" slots** — used differently by every DOT; treat as opaque until confirmed against a particular agency's extension spec |

Nav properties:

- `Contract` → the parent
- `ContractClaim` → optional link if this ContractTime was created in response to a claim
- `PayEstFirstProcessed` → the PE that first consumed charges from this row
- `ChangeOrderTimeAdjustment` (collection) → every approved time delta
- `ContractAdjustments` (collection) — **note the plural without the 's' between the words** — rows of type `Liquidated Damage`, `Disincentive`, `Incentive` posted when the PE closed
- `PaymentEstimateContractTimeCharges` (collection) → PE‑level period roll‑ups
- `WeeklyTimeCharges` (collection) → weekly bucket for agencies on that cadence

Subtype‑only navs:
- `ContractTimeAvailable` adds `CTAvailableSuspendResumes` (collection) + `DiaryContractTimes` + `DwrContractTimes`
- `ContractTimeRecurring` adds `ContractTimeRecurrEvents` (collection)

**Query template** — pull all ContractTimes for a contract:

```http
GET /ContractTimes?$filter=ContractId eq 282
   &$orderby=Type,PhaseOrder,Name
   &$select=Id,Name,Description,Type,AgencyType,Unit,RequiredFor,Main,Chargeable,
            OriginalNumberOfTimeUnits,AdjustedNumberOfTimeUnits,CurrentNumberOfTimeUnits,
            PendingNumberOfTimeUnits,StartTime,ActualCompletionDate,
            LiqDamRate,LiqDamRateTimeUnit,CalculateLiqDamage,
            IncentiveRate,IncentiveTotal,
            DisincentiveRate,TotalDisincentiveAmountApplied,
            Status,DefaultIndicator
```

**Worked example — contract 282:**

| Id | Name | Type | Unit | Orig | Adj | Current | StartTime | ActualCompletion | LiqDam | Incent | Disincent |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1930 | AWARD-DT | Informational | — | — | — | — | — | 2024-08-01 13:23 | — | — | — |
| 1931 | NTP-DT | Informational | — | — | — | — | — | 2024-08-01 13:23 | — | — | — |
| 1932 | WKBGN-DT | Informational | — | — | — | — | — | 2024-08-01 13:18 | — | — | — |
| 1933 | CRLMS-DT | Informational | — | — | — | — | — | — | — | — | — |
| 1934 | PRICEADJBASE-DT | Informational | — | — | — | — | — | — | — | — | — |
| 1935 | EXEC_DT | Informational | — | — | — | — | — | 2024-08-01 13:19 | — | — | — |
| 1936 | LETD | Informational | — | — | — | — | — | 2019-02-14 | — | — | — |
| **1937** | **99Avail** | **Available Time** | **Days** | **99** | **−87** | **12** | **2024-08-01 13:04** | **2024-09-07 16:38** | **$50/Day** | **$50/Day** | **$50/Day** |
| 1938 | 99Info | Informational | — | — | — | — | — | 2024-08-01 13:23 | — | — | — |
| 1939 | 99Recur | Recurring | — | — | — | — | 2024-08-01 13:24 | — | — | — | — |

The story this table tells: the award was 99 days of chargeable work; change order 114 later reduced that by 87 days (bringing allowed days down to 12 — an unusual, extreme CO shape used for lab testing); the crew actually finished on 2024‑09‑07 after charging 13 days of work; because they went 1 day past the 12 allowed, awdemo auto‑posted a **−$50 liquidated damage** and a **−$50 disincentive** on PE #11 (see §1.4).

#### 1.2 `ContractTimeAvailable` subtype — the chargeable counter

Adds three fields to the base:

| Field | Edm type | Notes |
|---|---|---|
| `StopTime` | DateTimeOffset | The last stop; `null` until the row is finalized |
| `TimeUnitsChargedOnApprEsts` | Decimal | Running total of units charged on *approved* PEs |
| `TimeUnitsChargedOnDiaries` | Decimal | Running total of units added to *diaries* in the current (unposted) period |

Nav additions: `CTAvailableSuspendResumes`, `DwrContractTimes`, `DiaryContractTimes`.

To filter the collection down to Available Time rows for a KPI card:

```http
GET /ContractTimes?$filter=ContractId eq 282 and Type eq 'Available Time' and Main eq true&$top=1
```

The `Main eq true` filter picks the one "principal" chargeable row for the contract — agencies often have multiple parallel chargeable timeframes (e.g. one for grading, one for paving) and the UI typically features only the main one.

#### 1.3 `DwrContractTime` and `DiaryContractTime` — where the charges originate

These are the per‑day entries that will later be rolled into a PE. One row per (DWR | Diary, ContractTime) pair.

`DwrContractTime` scalar fields: `Id`, `DailyWorkReportId`, `ContractTimeId`, `TimeCharged`, `TotalDiaryTimeCharged`, `HoursAvailable`, `HoursWorked`, `WorkStartTime`, `WorkStopTime`, `ContractorWorking` (bool), `ControllingOperation`, `DelayReason`, `Comments`.

`DiaryContractTime` has the same shape plus `DailyDiaryId` (instead of DWR), `AdjustedTimeCharged`, `TimeChargedChange`, `LatestAdjTotalCharge`, and a `DiaryContractTimeAdjustments` nav collection.

**Important nuance:** `DailyDiary.ContractorWorking` (one flag at the diary level — "did the contractor work on site today?") and `DiaryContractTime.ContractorWorking` (one flag per ContractTime per diary — "did this specific chargeable time get worked?") are different and may disagree. The former drives the stormwater and weekly‑report compliance clock; the latter drives the actual time debit.

**Worked example — diary 78 on contract 282:**

```
Diary 78 (2024-08-01, Sunny, 70°–85°, ContractorWorking=true, Locked)
└── DiaryContractTime 92 → ContractTime 1937 (99Avail, Days)
    │     TimeCharged=null  AdjustedTimeCharged=null  LatestAdjTotalCharge=1.0  ContractorWorking=false
    └── DiaryContractTimeAdjustment 3 → PaymentEstimate 306
          CurrentTotalCharge=1.0  PreviousTotalCharge=0.0
```

#### 1.4 `PaymentEstimateContractTimeCharge` + `ContractAdjustment` — PE rollup and liq‑dam / incentive postings

When a PE closes, the diary‑level charges accumulated against each ContractTime are summed into a single `PaymentEstimateContractTimeCharge` row, and if the counter crossed its allowed days the system also writes `ContractAdjustment` rows of type `Liquidated Damage`, `Disincentive`, or `Incentive`.

**Worked example — contract 282, PE #11:**

```
ContractTime 1937 (99Avail, 99 orig → 12 current)
└── PaymentEstimateContractTimeCharge 324 → PE 306 (#11, period end 2024-09-07)
      CurrentTimeChargeUnits = 13.0        ← total days charged in this PE
└── ContractAdjustment 117 → PE 306       Type=Liquidated Damage  TimeUnits=−1  Amount=−$50.00
      Comments: "System calculated liquidated damage adjustment basis was '50.00'"
└── ContractAdjustment 118 → PE 306       Type=Disincentive       TimeUnits=−1  Amount=−$50.00
      Comments: "System calculated disincentive adjustment basis was '50.00'"
```

Both ContractAdjustments charge *1 day over* and *$50 per day*. These are the UI's "assessed liquidated damages" and "assessed disincentive" lines on the pay estimate.

#### 1.5 `ChangeOrderTimeAdjustment` + `ChangeOrderTimeAdjustmentExplanation`

A change order can extend (or shrink) any ContractTime counter. The adjustment is stored separately from the dollar impact so the UI can show "time impact" distinctly.

| Field | Edm type | Notes |
|---|---|---|
| `Id`, `ChangeOrderId`, `ContractTimeId` | | |
| `AdjustmentTimeUnits` | Decimal | Delta (can be negative) |
| `AdjustmentCompletionDate` | DateTimeOffset | New ActualCompletionDate target if the CO shifts the deadline |

Nav: `ChangeOrder`, `ContractTime`, `ChangeOrderTimeAdjustmentExplanations` (collection).

Each `ChangeOrderTimeAdjustmentExplanation` carries a `RefChangeOrderExplanationId` + optional `SupplementalExplanation` free text + `Order`. These are the "reason codes" shown on the printed CO (e.g. "Add time for differing site conditions"; the ref table is the agency's standard reason list).

**Worked example — contract 282, CO 114:**

```
ChangeOrder 114 "0003 — Balance"  Type=CMPL  Status=Approved (2024-09-09 by edeluca)
└── ChangeOrderTimeAdjustment 29 → ContractTime 1937 (99Avail)
      AdjustmentTimeUnits=−87.0  AdjustmentCompletionDate=null
      ChangeOrderTimeAdjustmentExplanations=0  (none on this CO)
```

#### 1.6 `CTAvailableSuspendResume` — work-stop pairs

| Field | Notes |
|---|---|
| `ContractTimeAvailableId` | FK to the chargeable ContractTime |
| `SuspendTime` / `ResumeTime` | ISO timestamps — row is only created once a resume is known |

Only 2 rows exist in the lab (CT 186: 2018‑07‑24 → 2018‑07‑26; CT 267: 2019‑07‑03 → 2019‑07‑04). To query "suspensions in effect right now" use `SuspendTime le NOW and (ResumeTime eq null or ResumeTime gt NOW)`.

#### 1.7 `WeeklyTimeCharge` — alternative weekly cadence

Three rows in awdemo; shape is minimal (`ContractTimeId`, `WeekEnding`, `ReportNumber`, `Comments`, `CreatedByPersonInfoId`, `RevisedByPersonInfoId`, `RevisedDate`). Use this when an agency charges on a weekly bucket rather than per‑day.

#### 1.8 How to roll up "days charged vs days allowed" for a contract

```python
# One query gives everything the KPI card needs
ct = client.get('ContractTimes',
    filter='ContractId eq 282 and Type eq \'Available Time\' and Main eq true',
    expand='Contract($select=Id,Name),'
           'PaymentEstimateContractTimeCharges($select=Id,PaymentEstimateId,CurrentTimeChargeUnits),'
           'ChangeOrderTimeAdjustment($select=Id,ChangeOrderId,AdjustmentTimeUnits),'
           'ContractAdjustments($select=Id,Type,TimeUnits,Amount,PaymentEstimateId)')['value'][0]

days_allowed = ct['CurrentNumberOfTimeUnits']              # 12
days_charged = sum(x['CurrentTimeChargeUnits']             # 13
                   for x in ct['PaymentEstimateContractTimeCharges'])
over_by      = max(0, days_charged - days_allowed)         # 1
liq_dam_tot  = sum(x['Amount'] for x in ct['ContractAdjustments']
                   if x['Type'] == 'Liquidated Damage')    # -50.00
incent_tot   = sum(x['Amount'] for x in ct['ContractAdjustments']
                   if x['Type'] == 'Incentive')            # 0
disincent    = sum(x['Amount'] for x in ct['ContractAdjustments']
                   if x['Type'] == 'Disincentive')         # -50.00
```

#### 1.9 Awdemo gotchas (section 1)

- `ContractTimeAvailables`, `ContractTimeCalendars`, `ContractTimeCompletions`, `ContractTimeInformationals`, `ContractTimeRecurrings` are **not** separate entity sets — they return `404`. The base `ContractTimes` holds all five subtypes; filter on `Type`.
- To use a subtype‑only nav (e.g. `ContractTimeRecurrEvents`) in `$expand`, you must cast via `isof()`: `$filter=Id eq 1939 and isof('Repository.Models.ContractTimeRecurring')`. Easier: query `ContractTimeRecurrEvents?$filter=ContractTimeRecurringId eq 1939` directly.
- `ContractTime.ContractAdjustments` is **plural with no trailing s between words** — follow the metadata exactly.
- `ChangeOrderTimeAdjustmentExplanation.SupplementalExplanation` is often `null`; the row still carries the `RefChangeOrderExplanationId` which points at the printable reason text.
- `ContractTime.PercentComplete` is often `null` even when `CurrentTimeChargeUnits > 0`. Compute it client‑side rather than trusting the stored value.
- `GENDATE01`..`GENNUM08` et al. are **agency‑defined** scratch columns and should not be surfaced in a generic UI without reading the agency's extension spec.

---

### 2 · Progress schedules (baseline vs actual S‑curve)

#### Overview

`ContractProgressSchedule` is the entity that would, if populated, feed a baseline‑vs‑actual S‑curve or Gantt bar for a contract. In awdemo it is nearly empty: only **7 rows across all 147 contracts**, scattered on CTs 24 / 28 / 38, dated 2014. None exist on contract 282. The field shape is sufficient to build a chart, so this section is included for completeness and for the agencies that do use it.

```
Contract (1) ──* ContractProgressSchedule
                    (one row per scheduled checkpoint)
```

#### 2.1 `ContractProgressSchedule`

| Field | Edm type | Notes |
|---|---|---|
| `Id` | Int64 PK | |
| `ContractId` | Int64 FK | |
| `NumberOfUnitsOfTime` | Decimal | Days elapsed since contract start at this checkpoint |
| `ScheduleDate` | DateTimeOffset | Calendar date of the checkpoint |
| `ProjectedPercentComplete` | Decimal | Baseline S‑curve value |
| `ActualPercentComplete` | Decimal | **Always null in awdemo** |

Nav: `Contract` only.

**Worked example — contract 28 (lab fixture):**

| ScheduleDate | NumberOfUnitsOfTime | Projected% | Actual% |
|---|---:|---:|---:|
| 2014-03-17 | 10 | 30% | — |
| 2014-03-22 | 15 | 50% | — |
| 2014-03-27 | 20 | 75% | — |
| 2014-04-01 | 25 | 100% | — |

#### 2.2 Gotchas (section 2)

- `ActualPercentComplete` is `null` on every row in awdemo. If an agency doesn't maintain progress schedules, derive the "actual" curve from pay estimates (`AmountPaidToDate / AwardedContractAmount` sampled per PE close date) and overlay it on the baseline.
- No "baseline vs current" distinction — the entity is one‑dimensional. To support rebaselines, agencies typically keep history in `GENDATE*` on `ContractTime` or in a separate extension table.

---

### 3 · Milestones

#### Overview

AMS as it exists in `awdemo` has **no dedicated construction‑milestone entity**. The metadata contains `MaintenanceMilestone` and `MilestoneItem`, but those belong to the **CostEstimate / planning** subsystem (`CostEstimateMaintenanceMilestone`, `CostEstimateMaintenanceMilestoneItem`, `CeMilestoneItemBidBasedPrice`, `CeMilestoneItemRefPrice`) and have no FK to `Contract`. The functional stand‑ins for "milestones on an active contract" are:

1. **Informational `ContractTime` rows** — each one is a single named date (Award, NTP, Work Began, Letting, Execution, Contract‑Closed‑for‑CRLMS, Price‑Adjustment‑Base). The `RefContractTime` catalog has 33 named templates (`AWARD-DT`, `NTP-DT`, `EXEC_DT`, `WKBGN-DT`, `ACCEPT-DT`, `LETD`, `CRLMS-DT`, `PRICEADJBASE-DT`, …).
2. **`Completion Date` ContractTimes** — fixed‑date deadlines with liq‑dam math.
3. **`ActualCompletionDate` on an Available‑Time counter** — the de‑facto construction‑complete date.
4. **`ContractTimeRecurrEvent`** — scheduled recurring events (monthly inspections, status reports) with planned/actual dates.

#### 3.1 `RefContractTime` — the milestone catalog

Agencies pre‑seed this catalog so every new contract gets the standard set of named dates automatically.

| Field | Notes |
|---|---|
| `Id`, `Name`, `Description`, `Type`, `AgencyType`, `Unit` | |
| `RequiredFor` | gating rule |
| `Chargeable`, `CalculateLiqDamage`, `CalculateIncentive`, `CalculateDisincentive` | |
| `DeleteAllowed`, `AllowDuplicateOnContract`, `DefaultOnNewContract` | |
| `Frequency` | `Daily`, `Neither`, or null — drives whether the time charges by every calendar day |

Sample awdemo rows: `99Avail` (Available Time, Days, Chargeable, LiqDam, DefaultOnNew=true), `99Comp` (Completion Date, LiqDam), `AWARD-DT` (Informational, DefaultOnNew=true), `ACCEPT-DT` (Informational, agency Final Acceptance), `NTP-DT` (Informational, Notice to Proceed), etc.

#### 3.2 `ContractTimeRecurrEvent` — scheduled recurring checkpoints

Each row is one planned occurrence of a `ContractTimeRecurring` parent (e.g. "monthly environmental inspection"). Fields: `Id`, `ContractTimeRecurringId`, `PlannedDate`, `ActualDate`, `Comments`, plus timestamps. Attachments (via `DocumentSubmissions` nav collection) can be linked to the event.

**Worked example (lab fixture CTR 87):** 5 events in 2014 spaced one month apart (2014‑03‑15 → 2014‑07‑15), none have ActualDate set. Classic monthly‑cadence milestone series.

#### 3.3 How to list "upcoming milestones in the next 30 days"

```python
import datetime
now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
in_30 = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)).isoformat(timespec='seconds')

# Informational dates coming due
dates = client.get('ContractTimes', filter=(
    f"Type eq 'Informational' and ActualCompletionDate ne null "
    f"and ActualCompletionDate ge {now} and ActualCompletionDate le {in_30}"),
    select='Id,ContractId,Name,Description,ActualCompletionDate')['value']

# Completion deadlines coming due
deadlines = client.get('ContractTimes', filter=(
    f"Type eq 'Completion Date' and ActualCompletionDate ne null "
    f"and ActualCompletionDate ge {now} and ActualCompletionDate le {in_30}"),
    select='Id,ContractId,Name,ActualCompletionDate,LiqDamRate,LiqDamRateTimeUnit')['value']

# Recurring events coming due
events = client.get('ContractTimeRecurrEvents', filter=(
    f"ActualDate eq null and PlannedDate ge {now} and PlannedDate le {in_30}"),
    expand='ContractTimeRecurring($select=ContractId,Name)',
    select='Id,ContractTimeRecurringId,PlannedDate,Comments')['value']
```

Three parallel queries covers the full milestone surface for a 30‑day window.

#### 3.4 Gotchas (section 3)

- Do **not** try to query `/ContractMilestones` — no such set.
- `MaintenanceMilestone`, `MilestoneItem`, `CostEstimateMaintenanceMilestone` are planning‑side only; they live under the preconstruction cost‑estimation subsystem and share no FK with `Contract`.
- Use `ActualCompletionDate` (not `ScheduleDate`) as the "when did this fact become true" column on Informational ContractTimes — the awdemo convention is that an `Informational` row's one date lives in `ActualCompletionDate` even though no "completion" occurred.

---

### 4 · Workflow state machine

#### Overview

AMS workflows are **finite ordered lists of phases** attached to a workflow type (Proposal‑Project‑Contract, Internal Payroll, External Subcontractor Payment, DBE Commitment, SBP Commitment, Bidder/Quoter). An entity in the workflow (a Contract, a Proposal, a CertifiedPayroll, a SubcontractorPayment, a DbeCommitment, …) carries a `WorkflowPhaseId` FK pointing at its current phase. Movement forward happens by writing a new FK — awdemo exposes no "transition" entity.

```
Workflow (1) ──* WorkflowPhase (ordered by PhaseOrder)
                    │
                    └── * (Contracts | Proposals | Projects | CertifiedPayrolls |
                            SubcontractorPayments | DbeCommitmentSummaries | …)
```

#### 4.1 Workflows in awdemo

| Id | Type | Name | Phases |
|---:|---|---|---:|
| 1 | External Payroll | CertPayrollExtWF | 9 |
| 2 | Internal Payroll | CertPayrollWF | 4 |
| 3 | **Proposal‑Project‑Contract** | **Default** | **20** |
| 4 | External Subcontractor Payment | ExtSubPayment | 4 |
| 5 | Internal Subcontractor Payment | IntSubPayment | 4 |
| 6 | External DBE Commitment | ExtDbeCommitment | 6 |
| 7 | External Bidder Quoter | ExtBidderQuoter | 2 |
| 8 | Proposal‑Project‑Contract | Test | 2 |
| 9 | Proposal‑Project‑Contract | MDOT | 20 |
| 10 | Proposal‑Project‑Contract | Default (CA) | 20 |
| 11 | Proposal‑Project‑Contract | testing123 - | 1 |
| 12 | External SBP Commitment | ExtSBPCommitment | 5 |

The **Default** workflow (#3) is the one every real awdemo contract is on. Its 20 phases:

```
  1. Project Definition      (preconstruction)
  2. Designer Interface
  3. Proposal Definition
  4. Estimation
  5. Revisions
  6. Advertisement           (rule=FixPropItemLineNum)
  7. Addenda                 (rule=Addenda)
  8. Bid Processing
  9. Post Bid Evaluation     (rule=FixProposalItem)
 10. Alternate Analysis      (rule=FixBidCalculations)
 11. Reject
 12. Award
 13. Execute
 14. Construction
 15. Historical
100. PreconHasEnded          (rule=PreConstrHasEnded)
200. ActiveContract          ★ default phase for a live construction contract
210. ClosedContract
220. ArchivedContract
230. MigratedContract
```

Contract 282 WHITEOAK BRIDGE: `WorkflowPhaseId = 13` → PhaseName `ActiveContract`, PhaseOrder 200, Workflow `Default` (#3). This is normal for a construction‑active contract.

#### 4.2 `WorkflowPhase`

| Field | Notes |
|---|---|
| `Id`, `WorkflowId` | PK + FK |
| `PhaseOrder` | Int ordering; **not necessarily consecutive** (jumps from 15 to 100 in Default) |
| `PhaseName`, `Description` | Short + long name |
| `RuleName` | Enum string that the server uses to run a server‑side rule when a row enters this phase (e.g. `FixPropItemLineNum`, `ActiveContract`, `UnderPrimeReview`). Treat as read‑only in a UI. |

Nav collections (per `WorkflowPhase`): `Contracts`, `Projects`, `Proposals`, `Lettings`, `Bidder`, `CertifiedPayrolls`, `SubcontractorPayments`, `DbeCommitmentSummaries`, `ContractApprDbeCommitSummaries`, `ContractCurrDbeCommitSummaries`, `ContractSBPGoals`, `ContractProjects`, `Concepts`, `PrimeProjects`, `ProposalVendorSBPCommitmentSummaries`, `SourcePayrollTransitionComments`, `DestinationPayrollTransitionComments`, `WorkflowPhaseAccessRights`. The reverse direction — "every contract currently in this phase" — is one query.

#### 4.3 `WorkFlowPhaseAccessRight` — role × phase permissions

Metadata is present but **the entity set is `404` on awdemo** (admin‑only). Fields:

| Field | Notes |
|---|---|
| `Id`, `RoleId`, `WorkflowPhaseId` | PK + FKs |
| `CanView`, `CanAdd`, `CanUpdate`, `CanDelete` | Per‑phase CRUD toggles |

In a UI with role‑gated features, you'd normally query this to know which actions to disable; on awdemo you have to assume full access.

#### 4.4 Portfolio phase distribution (awdemo)

Across the 147 contracts in the lab:

| Count | ContractStatus | WorkflowPhase | Workflow |
|---:|---|---|---|
| 75 | Pending | ActiveContract | Default |
| 67 | Active | ActiveContract | Default |
| 2 | Active | (none — null) | — |
| 1 | Closed | ActiveContract | Default |
| 1 | Closed | ClosedContract | Default |
| 1 | Pending | (none — null) | — |

**Important:** `ContractStatus` (free‑text enum: Active / Pending / Closed) and `WorkflowPhase` are **not** derivable from each other. In production an active contract should be in the `ActiveContract` phase, but awdemo's 75 "Pending" contracts also carry the ActiveContract phase. In a real UI the authoritative "where is this contract in its lifecycle" is the workflow phase; `ContractStatus` is a legacy string.

#### 4.5 How to build a "pending approval inbox" for a user

```python
# What am I waiting to approve?
# 1. Resolve the user's Roles.
roles = client.get('UserInfos', filter=f'Id eq {user_id}',
    expand='UserRoles($expand=Role)')['value'][0]['UserRoles']
role_ids = [r['Role']['Id'] for r in roles]

# 2. Phases that role can act on (requires WorkFlowPhaseAccessRights — 404 on awdemo).
# Fallback: hard-code the phase names your product treats as inbox-worthy
# e.g. 'UnderAgencyReview', 'UnderPrimeReview', 'Pending'

phases = client.get('WorkflowPhases',
    filter="PhaseName in ('UnderAgencyReview','UnderPrimeReview','Pending')",
    select='Id,PhaseName,WorkflowId')['value']
phase_ids = ','.join(str(p['Id']) for p in phases)

# 3. Fetch everything attached to those phases, in parallel.
inbox = {
    'payrolls': client.get('CertifiedPayrolls',
        filter=f'WorkflowPhaseId in ({phase_ids})',
        select='Id,ContractId,WeekEnding,CreatedBy', top=50)['value'],
    'sub_payments': client.get('SubcontractorPayments',
        filter=f'WorkflowPhaseId in ({phase_ids})',
        select='Id,ContractId,Amount,PayDate,PayeeId', top=50)['value'],
    'dbe_commits': client.get('ContractApprDbeCommitSummaries',
        filter=f'WorkflowPhaseId in ({phase_ids})', top=50)['value'],
}
```

---

### 5 · Suspensions & extensions

#### Overview

Two orthogonal mechanisms:

- **Suspensions** stop the clock on a chargeable Available Time without changing its allowed days. Stored as `CTAvailableSuspendResume` pairs.
- **Extensions** change the allowed days themselves. Always originated by a `ChangeOrder` and recorded as `ChangeOrderTimeAdjustment` (see §1.5).

#### 5.1 `CTAvailableSuspendResume` (recap)

Only 2 rows in awdemo, both complete pairs:

| Id | CT | Suspend | Resume | Duration |
|---:|---:|---|---|---|
| 1 | 186 | 2018‑07‑24 11:17 | 2018‑07‑26 11:17 | 2 days |
| 2 | 267 | 2019‑07‑03 15:42 | 2019‑07‑04 15:42 | 1 day |

**Open suspension** = `ResumeTime eq null`. Awdemo has none.

#### 5.2 Query template — "which contracts are currently suspended?"

```http
GET /CTAvailableSuspendResumes?$filter=ResumeTime eq null or ResumeTime gt {now}
   &$expand=ContractTimeAvailable($select=Id,ContractId,Name;$expand=Contract($select=Id,Name,ContractStatus))
   &$orderby=SuspendTime desc
```

Expand through `ContractTimeAvailable` → `Contract` to get the contract identity in one round trip.

#### 5.3 Gotchas (section 5)

- The subtype path matters: `CTAvailableSuspendResume.ContractTimeAvailable` is `ContractTimeAvailable`, not the base `ContractTime`. Expanding `ContractTime` works but the server does the cast implicitly.
- Suspensions do not have a reason/code field in awdemo — only a free‑text `Comments` is not present either. Reasons go into `DelayReason` on the `DwrContractTime` / `DiaryContractTime` rows that follow a suspension period.

---

### 6 · Weather and non-working days

#### Overview

Two pieces: the `RefWeather` lookup catalog, and the per‑day weather observation on each `DailyDiary` / `DailyWorkReport`. Awdemo has 5 RefWeather rows; of them, **only "Isolated Storms" has `StormwaterEvent=true`** — this flag drives the SWPPP (stormwater) compliance clock via `StormwaterPeriod` and `StormwaterPeriodStormwaterEvent`.

#### 6.1 `RefWeather`

| Id | Name | StormwaterEvent | ResponseDays | Description |
|---:|---|---|---:|---|
| 1 | Cloudy | false | 7 | 60–100% cloud cover |
| 2 | Isolated Storms | **true** | 7 | Scattered storms with lightning |
| 3 | Partly Cloudy | false | 7 | 30–60% cloud cover |
| 4 | Sunny | false | 7 | 0–30% cloud cover |
| 5 | Rainy | false | — | 1″ or greater |

Nav reverse: `DailyDiary` (collection), `DailyWorkReports` (collection).

#### 6.2 Weather on DWR vs Diary

| Entity | Weather fields |
|---|---|
| `DailyWorkReport` | `RefWeatherId`, `HighTemperature` (Int16, °F), `LowTemperature`, `RainfallAmount` (Decimal, inches) |
| `DailyDiary` | `RefWeatherId`, `HighTemperature`, `LowTemperature`, no rainfall field |

Both nav back to `RefWeather`. Contract 282 Aug–Sep 2024 has 13 diaries all RefWeatherId=4 (Sunny) — awdemo fixture data; a real agency will see a mix.

#### 6.3 `StormwaterPeriod` (SWPPP compliance side)

8 rows in the lab. Scalar fields: `ContractId`, `StartDate`, `EndDate`, `InspectorId`, `QualificationId`, `InspectionCycle`, `LastInspectionDate`, `LastPrecipitationDate`, `EarthMovingIndicator`, `ComplianceCertificationStatus`, `MeansContrNotification`, `SignatureCount`, `Comments`. These rows define the SWPPP time windows an agency must inspect under.

#### 6.4 `StormwaterPeriodStormwaterEvent` — the weather → compliance join

Connects a `StormwaterPeriod` to the specific weather events (DWR days with `RefWeather.StormwaterEvent=true` plus rainfall ≥ an agency threshold) that triggered the 7‑day inspection clock. Covered in the DWR enrichment doc; here it's the schedule hook.

#### 6.5 How to pull a "weather calendar" for a contract

```http
GET /DailyWorkReports?$filter=ContractId eq 282
   &$expand=RefWeather($select=Id,Name,StormwaterEvent,Description)
   &$select=Id,DwrDate,RefWeatherId,HighTemperature,LowTemperature,RainfallAmount
   &$orderby=DwrDate asc
```

Response shape: list of DWRs with inline weather. For a contract‑scoped chart of rainy days vs clear days, group by `RefWeather.Name`. For stormwater‑event flagging, filter where `RefWeather.StormwaterEvent eq true or RainfallAmount gt 1.0`.

#### 6.6 Non-working days

AMS does not have a dedicated "non‑working day" entity. The flag `ContractorWorking` on `DailyDiary` and `DiaryContractTime` is the derived indicator: `false` on diaries where the contractor logged no work. For Available Time counters configured with `Frequency=Daily`, a day without a `DiaryContractTime` with `ContractorWorking=true` is a non‑charged day. The authoritative "days we charged this period" is the sum of `DiaryContractTimeAdjustment.CurrentTotalCharge` (or `PaymentEstimateContractTimeCharge.CurrentTimeChargeUnits` once the PE closes).

---

### 7 · UI query recipes

Each recipe shows the user‑visible question, the HTTP query, the response shape, and a performance note. All queries verified on awdemo.

#### Recipe 1 · "Days charged vs days allowed" KPI card

**UI question:** On a contract overview, show "Days charged: X of Y allowed, Z days over" with liq‑dam / incentive dollars assessed.

**Query:**
```http
GET /ContractTimes?$filter=ContractId eq 282 and Type eq 'Available Time' and Main eq true
   &$select=Id,Name,OriginalNumberOfTimeUnits,AdjustedNumberOfTimeUnits,CurrentNumberOfTimeUnits,
            StartTime,ActualCompletionDate,LiqDamRate,LiqDamRateTimeUnit,
            CalculateLiqDamage,CalculateIncentive,CalculateDisincentive
   &$expand=PaymentEstimateContractTimeCharges($select=CurrentTimeChargeUnits),
            ContractAdjustments($select=Type,TimeUnits,Amount)
```

**Response shape:**
```json
{"value":[{
  "Id":1937, "Name":"99Avail",
  "OriginalNumberOfTimeUnits":99, "AdjustedNumberOfTimeUnits":-87, "CurrentNumberOfTimeUnits":12,
  "LiqDamRate":50, "LiqDamRateTimeUnit":"Days",
  "PaymentEstimateContractTimeCharges":[{"CurrentTimeChargeUnits":13}],
  "ContractAdjustments":[
    {"Type":"Liquidated Damage","TimeUnits":-1,"Amount":-50},
    {"Type":"Disincentive","TimeUnits":-1,"Amount":-50}]
}]}
```

**UI math:** `charged = sum(CurrentTimeChargeUnits)`; `over = max(0, charged - CurrentNumberOfTimeUnits)`; `liqDam$ = sum(Amount where Type='Liquidated Damage')`.

**Perf:** 1 HTTP round trip, bounded result ≤ a few KB. Safe to cache per contract for ~60 s.

#### Recipe 2 · Timeline / Gantt row for a contract

**UI question:** Draw a time bar for a contract — Award → NTP → Work Began → Execute → each CO date → finally ActualCompletion of the Main Available Time. Label the bar in days.

**Query:** two parallel calls, then merge client‑side.

```http
# A — all Informational dates + the Main Available Time
GET /ContractTimes?$filter=ContractId eq 282 and (Type eq 'Informational' or (Type eq 'Available Time' and Main eq true))
   &$select=Id,Name,Description,Type,ActualCompletionDate,StartTime,CurrentNumberOfTimeUnits
   &$orderby=ActualCompletionDate

# B — approved time‑adjustments with their change order dates
GET /ChangeOrderTimeAdjustments?$expand=ChangeOrder($select=Id,Number,ApprovalDate,ContractId),ContractTime($select=Id,ContractId,Name)
   &$filter=ContractTime/ContractId eq 282
```

**Response shape (A):** list of named dated events (`Name`, `ActualCompletionDate`). **(B):** list of change orders with `AdjustmentTimeUnits` so the bar can show "+30 days (CO 002)".

**Perf:** two queries, each < 1 KB. Cache per contract for 5 min; invalidate on any Contract write.

#### Recipe 3 · S‑curve chart (planned vs actual)

**UI question:** Baseline S‑curve overlaid with actual earned.

**Query:**
```http
# Planned: from ContractProgressSchedule (will often be empty)
GET /ContractProgressSchedules?$filter=ContractId eq 282
   &$select=ScheduleDate,NumberOfUnitsOfTime,ProjectedPercentComplete,ActualPercentComplete
   &$orderby=ScheduleDate

# Actual: derived from pay estimate closes
GET /PaymentEstimates?$filter=ContractId eq 282
   &$select=EstimateNumber,PeriodEndDate,TotalEarnedToDate,PendingEstimateAmount
   &$orderby=PeriodEndDate
```

**UI math:** For each PE row, `actual% = TotalEarnedToDate / AwardedContractAmount * 100`. Plot both series on the same axis.

**Perf:** Both queries bounded by the contract's PE count (contract 282 = 11 PEs). Cheap.

#### Recipe 4 · "Milestones upcoming in the next 30 days" portfolio widget

See §3.3 for the three parallel queries. Merge, sort by date, cap at 10.

**Perf:** these are portfolio‑wide queries; expect a few hundred rows total. Cache for 15 min; recompute at midnight.

#### Recipe 5 · "Which contracts are currently suspended?"

**Query:**
```http
GET /CTAvailableSuspendResumes?$filter=ResumeTime eq null
   &$expand=ContractTimeAvailable($select=Id,ContractId,Name;$expand=Contract($select=Id,Name,ContractStatus))
   &$orderby=SuspendTime desc
```

**Response shape:** empty on awdemo; on prod, a list of `{SuspendTime, Contract: {Id,Name,ContractStatus}}` ready for a table.

**Perf:** 1 query; usually a tiny result; refresh on open.

#### Recipe 6 · Weather‑impacted‑days chart

**UI question:** For a contract, show stacked bar per week: clear days, cloudy days, rainy / storm days.

**Query:**
```http
GET /DailyWorkReports?$filter=ContractId eq 282
   &$expand=RefWeather($select=Id,Name,StormwaterEvent)
   &$select=Id,DwrDate,RefWeatherId,HighTemperature,LowTemperature,RainfallAmount
   &$orderby=DwrDate
```

**UI math:** Bucket by ISO‑week (`DwrDate`), group by `RefWeather.Name`, stack. Flag any `(RefWeather.StormwaterEvent eq true) or (RainfallAmount gt 1.0)` as a stormwater‑compliance tick.

**Perf:** bounded by DWR count on contract (contract 282 = 14 DWRs). Cheap. Caches well.

#### Recipe 7 · Workflow phase breakdown across the active portfolio

**UI question:** Bar chart — "how many contracts are in each phase right now?".

**Query:**
```http
GET /Contracts?$select=Id,ContractStatus,WorkflowPhaseId
   &$expand=WorkflowPhase($select=Id,PhaseName,PhaseOrder;$expand=Workflow($select=Id,Name,Type))
   &$top=1000
```

**UI math:** Group by `WorkflowPhase.PhaseName`, count. Sort by `PhaseOrder`. In awdemo this produces { `ActiveContract`: 143, `ClosedContract`: 1, `null`: 3 }.

**Perf:** One query, caps at ~ a few hundred contracts; use `$top` + `@odata.nextLink` for larger portfolios. Cache for 5 min.

#### Recipe 8 · Pending‑approval inbox for the signed‑in user

See §4.5 for the three‑step shape (resolve roles → resolve inbox phases → parallel‑fetch each entity type). Minimum one round trip per entity type the user is empowered on. In awdemo, since `WorkFlowPhaseAccessRights` is 404, hard‑code the phase whitelist until prod permits querying it.

**Perf:** 3–7 parallel queries at open; cache for ~30 s; invalidate on explicit "mark reviewed" writes.

#### Recipe 9 · "Change orders that moved the contract date" audit list

**UI question:** On a contract page, list only the COs that extended or shrank the contract.

**Query:**
```http
GET /ChangeOrderTimeAdjustments?
   $filter=ChangeOrder/ContractId eq 282
   &$expand=ChangeOrder($select=Id,Number,Description,Status,Type,ApprovalDate),
            ContractTime($select=Id,Name,CurrentNumberOfTimeUnits),
            ChangeOrderTimeAdjustmentExplanations($select=RefChangeOrderExplanationId,SupplementalExplanation,Order)
```

**Response shape:** one row per time‑adjustment; sum `AdjustmentTimeUnits` for a "net days added" KPI.

**Perf:** cheap (contract 282 has 3 COs → 1 time‑adjustment row).

#### Recipe 10 · "Who's on this contract this week?" scheduling view

**UI question:** Day cells for the next 7 days showing anticipated recurring events (inspections, status reports) + currently‑assigned inspectors.

**Query:**
```http
# Recurring events in a 7-day window on this contract's recurring times
GET /ContractTimeRecurrEvents?
   $filter=PlannedDate ge {today} and PlannedDate le {today+7}
   and ContractTimeRecurring/ContractId eq 282
   &$expand=ContractTimeRecurring($select=Id,Name,Description;$expand=Contract($select=Id,Name))
   &$select=Id,PlannedDate,ActualDate,Comments
   &$orderby=PlannedDate

# Who authored recent diaries (fallback for "assigned inspector")
GET /DailyDiaries?$filter=ContractId eq 282 and DiaryDate ge {today-14}
   &$select=AuthorId,DiaryDate&$orderby=DiaryDate desc&$top=20
```

**Perf:** two bounded queries; cache for 30 s.

---

### 8 · Cross-flow interactions

- **Schedule ↔ Payment.** `PaymentEstimateContractTimeCharge` is the join. Every chargeable Available‑Time counter writes exactly one `PaymentEstimateContractTimeCharge` row per PE close, carrying the summed days for that period. The same PE close is also what causes `ContractAdjustment` rows (Liquidated Damage, Disincentive, Incentive) to be posted for an over/under condition — and *those* rows are what deduct from the gross on the PE's `CurrentItemPaidGrossAmount` → `CurrentItemPaidNetAmount` pipeline covered in the companion doc §2.
- **Schedule ↔ Change orders.** `ChangeOrderTimeAdjustment` is the mechanical link. A CO affects dollars via `ChangeOrderItem` **and** time via `ChangeOrderTimeAdjustment`; the two are independent children of `ChangeOrder`. The reconciliation `OriginalNumberOfTimeUnits + Σ(AdjustmentTimeUnits where CO.Status='Approved') == CurrentNumberOfTimeUnits` must hold.
- **Schedule ↔ DWR.** The DWR's `ApprovedByDiaryId` points at the `DailyDiary` whose approval also closed the day's time charge. In awdemo roughly half of contract 282's DWRs carry an `ApprovedByDiaryId`; the other half were approved outside the diary signoff. `DailyDiary.PaymentEstimateApproved` (bool) tells you whether the diary's time charges have been baked into their PE yet.
- **Schedule ↔ Workflow.** The construction‑lifecycle phases (`Award`, `Execute`, `Construction`, `ActiveContract`, `ClosedContract`) match named `ContractTime.Informational` entries (`AWARD-DT`, `EXEC_DT`, `ACCEPT-DT`). But the authoritative "where in the lifecycle" value is `Contract.WorkflowPhaseId` → `WorkflowPhase.PhaseName`, not the dates — the dates can be edited after the fact; the phase is driven by server rules.
- **Workflow ↔ Payroll / DBE / Sub-payments.** `CertifiedPayrolls`, `SubcontractorPayments`, `ContractApprDbeCommitSummaries`, `ContractCurrDbeCommitSummaries`, and `ContractSBPGoals` all carry `WorkflowPhaseId` FKs — their inboxes share the same shape as the contract inbox.
- **Weather ↔ Stormwater compliance.** Weather is observational on `DailyDiary` and `DailyWorkReport`; `RefWeather.StormwaterEvent=true` plus `RainfallAmount` ≥ agency threshold is what the SWPPP‑compliance engine watches to open a 7‑day inspection window via `StormwaterPeriod` and `StormwaterPeriodStormwaterEvent`.
- **Weather ↔ Time charges.** Weather does **not** auto‑suppress a time charge. The judgment of "no charge today because weather" is still manual: the inspector flips `DiaryContractTime.ContractorWorking` to false and leaves `CurrentTotalCharge` at 0 on that day's `DiaryContractTimeAdjustment`.
- **Suspensions ↔ COs.** Suspensions pause the clock but do **not** change `CurrentNumberOfTimeUnits`. If a suspension is going to blow the deadline, the relief has to come as a Change Order with a `ChangeOrderTimeAdjustment`. Two different mechanisms, both targeting the same `ContractTimeAvailable` row.
- **Recurring events ↔ Documents.** Each `ContractTimeRecurrEvent` has a `DocumentSubmissions` nav collection — the UI pattern is "mark this recurring event complete and attach the inspection PDF in one gesture".

---

### 9 · Awdemo gotchas (consolidated)

1. **No subtyped entity sets.** `/ContractTimeAvailables`, `/ContractTimeCalendars`, `/ContractTimeCompletions`, `/ContractTimeInformationals`, `/ContractTimeRecurrings` → `404`. Query `/ContractTimes` and filter on `Type`.
2. **Subtype‑only navs need a cast.** `ContractTimeRecurrEvents` is only reachable via `$expand` after an `isof('Repository.Models.ContractTimeRecurring')` filter; otherwise go through `/ContractTimeRecurrEvents?$filter=ContractTimeRecurringId eq N`.
3. **`WorkFlowPhaseAccessRights` is 404 on awdemo.** Admin‑only. Hard‑code the phase whitelist for inbox UIs until prod access is granted.
4. **`ScheduledProcesses` is 403 on awdemo.** Not queryable from the lab; relevant for scheduled background jobs if an agency exposes it.
5. **`ContractProgressSchedule` is nearly empty.** 7 rows across all 147 contracts; `ActualPercentComplete` always `null`. Derive the actual S‑curve from PE closes instead.
6. **`ContractStatus` ≠ Workflow phase.** 75 of 147 contracts in awdemo are `ContractStatus='Pending'` yet in `WorkflowPhase='ActiveContract'`. Trust the phase.
7. **`Main` on ContractTime is single‑instance per contract.** Expect exactly one `Main=true` chargeable Available Time per contract; the UI's primary KPI should always use that one.
8. **`ActualCompletionDate` is multi‑purpose.** On Informational rows it stores the event date (there is no "schedule date" column). On Available Time rows it stores the end‑of‑charging date.
9. **`PercentComplete` is unreliable.** Often `null` even on counters with charges posted; compute client‑side.
10. **`DailyDiary.ContractorWorking` vs `DiaryContractTime.ContractorWorking`.** Different scopes (per‑diary vs per‑ContractTime‑per‑diary) and may disagree. The per‑ContractTime one is the one that drives the charge.
11. **`ChangeOrderTimeAdjustment.AdjustmentCompletionDate` is often `null`.** When a CO's effect is purely "+/− N days" the completion date column is left blank; the UI should compute new completion = old completion + ΣAdjustmentTimeUnits.
12. **`CTAvailableSuspendResume.Comments` field doesn't exist.** No reason field on the entity; put reasons in the DWR/Diary `DelayReason` for the days inside the suspension window.
13. **Nav‑name typos.** `ContractAdjustments` (plural, no 's' between the words), `ChangeOrderTimeAdjustment` (singular on the ContractTime side but a *collection*), `DiaryContractTime` (singular on the DailyDiary side but a *collection*). Follow metadata exactly.
14. **Workflows for payroll/sub‑payment are 4–9 phases long.** Count them when designing UI phase pills; width constraints matter in a sidebar.
15. **`WorkflowPhase.RuleName`** is a server rule identifier, not a label. Don't display it to end users as the phase name; use `PhaseName` / `Description`.
16. **`ContractTimeRecurring` planned events are generated server‑side.** Writing a new `ContractTimeRecurring` does not immediately populate `ContractTimeRecurrEvents`; the lab fixture CTR 87 was pre‑generated. Confirm your target agency's generation cadence before relying on it.

---

### 10 · Deferred / unverified

- **`ContractMilestone`, `MilestoneItem` (construction):** no such entity in the awdemo metadata. The vendor reference guide lists "MilestoneItem" but every milestone‑named entity in the lab belongs to the `CostEstimate` planning subsystem. If a real agency has construction milestones they live under `CostEstimate*`‑named entities on an attached cost estimate, not on the active contract.
- **`WorkFlowPhaseAccessRights` role × phase matrix:** metadata‑present, awdemo‑403. The 4 CRUD toggles on each phase would normally gate action buttons in a workflow UI.
- **`ScheduledProcesses` / `SystemEventTriggerSchedule`:** admin‑only on awdemo (403). Would carry cron/trigger definitions for server‑scheduled jobs.
- **TimeExtensionRequest / contractor‑initiated extension workflow:** no such entity in awdemo metadata. Agencies that require this seem to carry it as a free‑text explanation on a Change Order (`ChangeOrderTimeAdjustmentExplanation.SupplementalExplanation`) rather than as a formal request entity.
- **Non‑working‑day holiday calendar:** no entity exposes agency holidays. The Available Time counter is purely diary‑driven; agency‑specific holidays must be modeled client‑side or inferred from the pattern of `ContractorWorking=false` diary rows.
- **Weekly bar chart of planned labor vs charged time:** `WeeklyTimeCharge` is populated for only 3 rows across the lab; a real agency's weekly cadence can be visualised once their data appears.

---

---

---

<a id="part-8-compliance-dbe-civil-rights"></a>

# Part 8 — Compliance, DBE & civil rights

_The regulatory layer: DBE commitment vs utilization, certified payroll with Davis-Bacon exceptions, prevailing wage, civil-rights/labor/EEO reviews, OJT programs, and the non-compliance tracking that holds it all together._

**Companion to:** [`ams-business-flows-2026-09-30.md`](ams-business-flows-2026-09-30.md). That document covered labor hours (DWR side), financial transactions, and items/materials. This one is the **regulatory / federal-compliance layer** — the data that proves a project is being executed in a way the FHWA, the Department of Labor, and the state's civil-rights office will accept. The source of every claim here is a live query against `ams-lab/awdemo` (noted inline).

**Audience:** compliance officers (do we have a payroll from every active contractor every week?), DBE liaisons (are primes paying the DBEs they promised to pay?), civil-rights office (which contractors are overdue for an EEO review?), labor compliance (which payrolls have unresolved wage violations?), executive dashboards (one-screen summary of the agency's compliance posture across the portfolio).

**Why this layer exists.** Federal-aid highway contracts (23 CFR Part 230, 23 CFR Part 26, 29 CFR Part 5, 41 CFR Part 60, and 49 CFR Part 26) impose non-waivable reporting duties on the state DOT: weekly certified payrolls to prove Davis-Bacon prevailing wages are being paid; DBE goal-setting at bid time with actual-utilization reporting during construction; EEO reviews of prime contractors on contracts above a dollar threshold; OJT (on-the-job training) goals requiring a set number of trainee-hours delivered per contract year; and periodic civil-rights compliance reviews. The AMS schema maps directly onto these obligations. **Each flow in this document is a federal reporting requirement with an entity chain behind it.**

---

### Legend & conventions

Same as the companion doc. In addition:

- **"Appr" vs "Curr"** — the DBE schema stores two copies of every commitment: `ContractApprDbeCommit*` = the *approved baseline* (frozen at the DBE Liaison Officer's approval), `ContractCurrDbeCommit*` = the *current* set (reflects revisions, substitutions, additions post-award). Reports comparing commitment-vs-utilization usually use **Curr**; reports showing "what was promised at award" use **Appr**.
- **DBE vs SBP** — DBE = federal (49 CFR Part 26) Disadvantaged Business Enterprise; SBP = state-level Small Business Program (Michigan-specific in this lab instance). The two share a nearly identical commitment/goal/good-faith-effort schema. On awdemo, several `SBP` sets 500 (schema-only); DBE is fully populated.
- **PersonInfo is 403** on awdemo (noted in the companion doc). People who approved reviews, resolved exceptions, or conducted interviews show up as integer IDs — resolve them via join only in a prod instance that permits `PersonInfos` access.
- All example data below is from the **awdemo lab** as of 2026-09-30. The anchor contract is **Contract 38 (`003870`)**, prime vendor **Bacco Construction Company** (RefVendor #125) — this is the only contract on awdemo with a complete end-to-end compliance footprint (DBE commitments + certified payrolls + OJT assignments + wage decisions + reviews). Contract 282 (WHITEOAK BRIDGE), used throughout the companion doc, has **no compliance data on awdemo** — so this doc shifts anchors.

---

### 1. DBE commitments & utilization

#### Overview

At the moment a bid is accepted and a contract awarded, the prime contractor hands the DOT a signed form listing every DBE firm they intend to subcontract to and how much they'll spend with each. That list becomes the **approved DBE commitment summary** (`ContractApprDbeCommitSummary`) and its child commitments (`ContractApprDbeCommitment`, one per DBE firm). The sum of those commitments, divided by the awarded contract value, must meet the **DBE goal** that the DOT set for the contract at letting (49 CFR 26.53). If the prime falls short, they file a **good-faith-effort** record showing which DBEs they contacted, what quotes they received, and why they ultimately didn't commit (`ContractApprGoodFaithEffort`). After award, as prime pays each DBE for actual completed work, a `SubcontractorPayment` row is written with `DbeFirm = true` and (sometimes) `DbeCommitment = true` — those payments are the **actual DBE utilization ledger**. The DOT reconciles: did the prime actually pay what they promised? A gap triggers follow-up or (eventually) a 26.53(f) substitution request.

The "current" tree (`ContractCurrDbeCommit*`) is a mirror of the approved tree that absorbs **mid-contract revisions**: a DBE goes bankrupt and is substituted, a change order creates new DBE-eligible work, the prime renegotiates a scope split. The approved tree stays frozen (it's the baseline for compliance reporting); the current tree is what dashboards show today.

#### Entity chain

```
         +-------------------------+  (one per prime vendor on a contract,
         | ContractApprDbeCommit  |   at award — the APPROVED BASELINE)
Contract ◄───────── Summary ─────────────► RefVendor (= prime)
   │     | TotalCommitAmt / Pct  |
   │     | GoodFaithEffort       |
   │     +-----------┬-----------+
   │                 │ 1:N
   │                 ▼
   │     +-------------------------+
   │     | ContractApprDbeCommit  |          +--------------------+
   │     | ment                   |◄───1:N───| ContractApprGood   |
   │     | DbeVendorId            |          | FaithEffort (one per
   │     | CommitmentAmt          |          |  DBE that was contacted
   │     | RaceConsciousAmt       |          |  but did not win work) │
   │     | DbeVerified            |          +--------------------+
   │     | SupplierOnly / Trucker |
   │     +────┬────┬────┬─────────+
   │          │    │    │ (each 1:N)
   │          ▼    ▼    ▼
   │   WkItems   WkTypes   Suppliers (what work the DBE will do)
   │
   │     +-------------------------+  (mirror tree, mutable, reflects
   │     | ContractCurrDbeCommit  |   mid-contract revisions)
   └───► Summary / Commitments / │   same substructure
         Supplier / etc.          │
         +-------------------------+

   ─── UTILIZATION LEDGER ────────────────────────────
   PaymentEstimate ──► ContractPayment ──► SubcontractorPayment
                                            │  (one per $ paid to a sub,
                                            │   whether DBE or not)
                                            │  DbeFirm = true  ← DBE
                                            │  DbeCommitment = true  ← counts
                                            │  PaidAmount, AmountReceived,
                                            │  TotalDbeCreditAmount
                                            ▼
                                     RefVendor (= DBE sub)
```

#### Entities

##### `ContractApprDbeCommitSummary` / `ContractCurrDbeCommitSummary`

**Purpose.** One row per prime vendor per contract. Carries the rolled-up goal and commitment numbers that the DBE Liaison Officer signs off on. There's typically one summary per contract — the prime's — though a joint-venture prime structure can produce multiples.

| Field | Type | Notes |
|---|---|---|
| `Id` | int | Primary key |
| `ContractId` | int | FK → `Contract.Id` |
| `RefVendorId` | int | FK → `RefVendor.Id` (the prime) |
| `VendorName` | string | Denormalized prime name (e.g. `"Bacco Construction Company"`) |
| `CommitmentApproval` | bool | True once the DBE LO signs |
| `ApprovedBy` / `ApprovalDate` | string / dt | Signer code + date |
| `RecordSource` | string | `"Preconstruction"` (award) or `"Construction"` (post-award revision) |
| `GoodFaithEffort` | string | Nullable `"Yes"` flag when the prime missed goal |
| `TotalCommitAmt` / `TotalCommitPct` | decimal | Rolled-up $ and % of contract value |
| `TotalRaceConsciousAmt` / `TotalRaceConsciousPct` | decimal | Of the commitment, how much is race-conscious |
| `TotalRaceNeutralAmt` / `TotalRaceNeutralPct` | decimal | Rest is race-neutral |
| `DbeSubCommitAmt` / `DbeSubCommitPct` | decimal | DBE sub-only portion |
| `RevisedGoal` / `RevisedCommitment` | bool | Set on `Curr` summary when post-award revised |
| `RevisedGoalPct` / `RevisedCommitAmt` / etc. | decimal / string / dt | Revision bookkeeping |
| `WorkflowPhaseId` | int | FK → `WorkflowPhase.Id` for e-sign chain |
| `ExtCommitmentApproval` / `ExtApprovalDate` / … | bool / dt | External-reviewer sign-off (second pair of eyes) |

**Example (awdemo):** Contract **38** → one `ContractCurrDbeCommitSummary` (Id=2, VendorName `"Bacco Construction Company"`, `TotalCommitAmt = $1,775,000.00`, `TotalCommitPct = 10.33%`, all race-conscious, approved by `"DBE"` on 2014-05-29).

##### `ContractApprDbeCommitment` / `ContractCurrDbeCommitment`

One row per DBE firm the prime committed to. Child of the summary.

| Field | Type | Notes |
|---|---|---|
| `Id` | int | Primary key |
| `ContractApprDbeCommitSummaryId` (/ `Curr…`) | int | FK → summary |
| `DbeVendorId` | int | FK → `RefVendor.Id` (the DBE sub) |
| `CommitmentAmt` | decimal | $ promised to this DBE |
| `RaceConsciousAmt` / `RaceNeutralAmt` | decimal | Split of commitment |
| `SupplierOnly` / `SupplierAmt` / `MaxSupplierCredit` / `MaxSupplierPct` | bool / decimal | For material-supplier DBEs with 60% credit cap (49 CFR 26.55(e)) |
| `Trucker` / `TruckerAmt` / `MaxTruckerCredit` / `MaxTruckerPct` | bool / decimal | Trucker DBE provisions |
| `DbeVerified` | bool? | Whether vendor still has valid DBE cert on effective date |
| `Reviewed` / `ReviewedBy` / `ReviewDt` | bool / string / dt | DOT review log |
| `DbeType` | string | e.g. `"DBE"` vs blank for untyped |
| `RevisedCommitAmt` / `RevisedCommitPct` / `RevisedCommitDt` | decimal / dt | Post-award revisions |
| `IsSigned` / `ExtReviewed` | bool | Workflow flags |

**Example (awdemo):** Summary 2 on contract 38 has three children:
- Perez Construction, Inc. (#543) — `$1,500,000` race-conscious
- Rodriguez Construction Corporation (#758) — `$25,000` race-conscious
- City Steel, Inc. (#8688) — `$250,000` race-conscious

##### `ContractApprDbeCommitWkItem` / `WkType` / `ContractApprDbeSupplier`

Per-commitment detail: which bid-items (`DbeCommitmentWorkItem` → `BidId`), work-types, or supplier materials the DBE will perform. On awdemo these are populated for proposal-level `DbeCommitment` records but almost empty for the contract-level `ContractApprDbe*WkItems` — expect prod to carry them.

##### `ContractApprGoodFaithEffort` / `ContractApprGoodFaithEffortWorkType`

One row per DBE firm the prime **contacted** during bid preparation but did not ultimately commit to. Required when the prime fell short of goal (49 CFR 26.53(a)(2)).

| Field | Type | Notes |
|---|---|---|
| `DbeVendorId` | int | Who was contacted |
| `ContactDate` | dt | When |
| `Quote` | decimal | Their quote (if given) |
| `QuoteReceived` | bool | Did they respond? |
| `Comments` | string | Why not committed (e.g. `"Too High"` — real example from awdemo) |

**Example (awdemo):** `ContractApprGoodFaithEffort` Id=1 — contacted DBE #758 (Rodriguez) on 2014-05-02, quote $300,000, "Too High."

##### `SubcontractorPayment` (the utilization ledger)

This is the **actual payment** flowing to DBE firms. Lives in the SubcontractorPayment entity (not a DBE-specific one — awdemo has no `DbePayments` set; it's a filter on this one).

| Field | Type | Notes |
|---|---|---|
| `Id` | int | PK |
| `ContractPaymentId` | int | FK → `ContractPayment.Id` (that payment's parent contract pay-estimate record) |
| `PayerId` | int | FK → `RefVendor.Id` (the prime or upper-tier sub) |
| `PayeeId` | int | FK → `RefVendor.Id` (recipient) |
| `PaidDate` / `ReceivedDate` | dt | When the prime paid, when the sub acknowledged receipt |
| `PaidAmount` / `AmountReceived` | decimal | Should match; mismatch = compliance signal |
| `PaymentType` | string | `"Progress"`, `"Final"`, `"Retainage"` |
| **`DbeFirm`** | bool | **True iff payee is a DBE firm** |
| **`DbeCommitment`** | bool | True iff this payment counts toward the DBE commitment |
| **`TotalDbeCreditAmount`** | decimal | Credit amount (may differ from PaidAmount for supplier DBEs at 60% credit) |
| **`TotalPaidToDateDbeCreditAmount`** | decimal | Running total of DBE credit on this contract |
| `RetainageReleased` / `RetainageDollarsHeld` | bool / decimal | Retainage status |
| `PaymentReceived` | string | `"Yes as Expected"`, `"No"`, `"Yes but Different"` |
| `ReviewedDate` / `ReviewerComments` | dt / string | DOT review log |
| `WorkflowPhaseId` / `SignedById` / `SignedDate` | int / int / dt | E-sign chain |

**Example (awdemo):** 11 SubcontractorPayments where `DbeFirm = true` across the entire awdemo lab:
- Contract 38 Bacco paid Rodriguez $21,100 (payment #1) and City Steel $195,484 (#2) → **$216,584 utilized vs $1,775,000 committed = 12.2% utilization**
- Perez Construction (biggest commitment at $1.5M) has **$0 utilization recorded** — classic compliance red flag
- Contract 75 shows multiple payments to Perez and Balkema
- Contract 271 has a $1,000 payment to City Steel

#### Rollup query — DBE commitment vs utilization for one contract

```python
# Commitments
summaries = c.get('ContractCurrDbeCommitSummaries',
    filter=f'ContractId eq {cid}',
    expand='ContractCurrDbeCommitments($expand=DbeVendor($select=Id,Name,LongName))'
)['value']

committed_by_dbe = {}
for s in summaries:
    for comm in s.get('ContractCurrDbeCommitments', []):
        v = comm.get('DbeVendor') or {}
        committed_by_dbe[v['Id']] = {
            'name': v.get('LongName'),
            'committed': comm['CommitmentAmt'],
            'race_conscious': comm['RaceConsciousAmt'],
        }

# Utilization — DBE-flagged subcontractor payments on this contract
payments = c.get('SubcontractorPayments',
    filter=f'DbeFirm eq true',
    expand='ContractPayment($select=Id,ContractId),Payee($select=Id,LongName)',
)['value']
utilization = {}
for p in payments:
    if (p.get('ContractPayment') or {}).get('ContractId') != cid:
        continue
    payee_id = (p.get('Payee') or {}).get('Id')
    utilization[payee_id] = utilization.get(payee_id, 0) + (p.get('PaidAmount') or 0)

# Reconcile
for dbe_id, c_info in committed_by_dbe.items():
    paid = utilization.get(dbe_id, 0)
    pct = paid / c_info['committed'] * 100 if c_info['committed'] else 0
    print(f"{c_info['name']}: committed ${c_info['committed']:,.0f}, paid ${paid:,.0f}, {pct:.1f}%")
```

#### Awdemo gotchas (DBE)

- `DbeSuppliers` entity set returns empty (0 rows) on awdemo — supplier-DBE commitments must be read from `ContractApprDbeSuppliers` / `ContractCurrDbeSuppliers` (the contract-level variants are the ones that are populated).
- No standalone `DbePayments` / `DbeShortfalls` / `DbeSubstitutions` entity sets exist (`404`); utilization is inferred from `SubcontractorPayments.DbeFirm = true`.
- `ContractSBPGoals`, `ContractSBPCommitments`, `ProposalVendorSBPCommitments`, `ProposalVendorSBPGoalGoodFaithEffort` all **500** on awdemo — SBP (Small Business Program, state-level) tracking is unavailable on this lab instance. `RefVendorSBPCertifications` works fine (returns real records); it's the per-contract SBP commitment tables that are broken.
- `RefVendor` has no `DBECertificationStatus` field (common mistake copying from the vendor guide); use `RefVendorDbeCertificationEvents` for status history, where `RefActionTypeId` 25 = "application received", 28 = "approved", etc.
- `ContractApprGoodFaithEfforts` tracks pre-award GFE. There is no post-award GFE for DBE substitutions on awdemo — if that process exists in prod it rides on a different entity.
- `RefVendorSbpCertificationEvents` set exists but is empty (schema-only); use `RefVendorSBPCertifications` for status.
- When a prime commits more than the goal, `TotalCommitPct > Goal` — not a compliance issue, just an over-commitment. Dashboards should allow for this.

---

### 2. Certified payroll

#### Overview

Davis-Bacon (40 USC § 3141 et seq.) requires every contractor on a federally-funded highway project to submit a **weekly certified payroll** listing every worker on-site that week, their craft, their hours (straight time + overtime, per day), their wage paid, and their fringe benefits. The DOT runs each submission through an **exception-rules engine** (over 20 rules in `PayrollExceptionRules`) that flags violations: wage below the prevailing-wage decision, missing fringe, deductions that don't reconcile, holiday-pay math errors, missing SSN, misclassified apprentice, etc. Exceptions are routed to the DOT compliance officer and either resolved or escalated. Prime contractors are responsible for collecting payrolls from every subcontractor and submitting them on behalf of the subs — `TieredContractorId` on `CertifiedPayroll` records that chain, and `PrimeAcceptedDate` vs `AgencyAcceptedDate` separates the prime's sign-off from the DOT's.

The schema is **deep** — a single payroll is a 5-level tree: `CertifiedPayroll → PayrollEmployees → PayrollEmployeeLabors (per craft × project) → PayrollEmployeeLaborHours (per day) + PayrollEmpFringeBenefExcepts`. A single payroll can produce hundreds of exception records. On awdemo contract 38 Bacco's first payroll has **9 exceptions** on 4 employees — a mix of fringe mismatches and below-minimum-wage violations.

#### Entity chain

```
                   Contract ──► CertifiedPayroll (weekly)
                                 │  ContractId, RefVendorId, PayrollNumber,
                                 │  ModificationNumber, BeginDate, EndDate,
                                 │  SubmittalDate, PrimeAcceptedDate,
                                 │  AgencyAcceptedDate, WorkflowPhaseId,
                                 │  IsLatestModification, TieredContractorId
                                 │
                     ┌───────────┼───────────────────┐
                     │           │                   │
                     ▼           ▼                   ▼
            CertPayroll     CertifiedPayroll     PayrollEmployees
            BenefitProgram  Exception            FirstName/LastName/Ssn
            (health plans,  (description,        Gender/EthnicGroup
             pensions,      Type [Fringe|Labor], TotalHours/GrossPay
             tracked at     Resolved,            FICA/Fed/State
             payroll level) ResolutionComments,  withholding
                            PayrollExceptionRule │
                            ConformanceWage      │ 1:N
                            Decision)            ▼
                                      PayrollEmployeeLabors
                                      (one row per employee × craft × project)
                                      ├ ContractProjectId
                                      ├ CraftCode  (string like "15", "40")
                                      ├ LaborClassId  ──► LaborClass (OEG11, LBDW, etc)
                                      ├ Apprentice (bool), ApprenticeId
                                      ├ OJTProgramIndicator
                                      ├ StraightTimeHourlyRate / OvertimeHourlyRate
                                      ├ HealthWelfareRate / VacationHolidayRate /
                                      │  PensionRate / ApprenticeshipFundRate /
                                      │  Other1Rate / Other2Rate / FringeBenefits
                                      ├ TotalHours / GrossPay / NetPay
                                      ├ RequiredCompensation (computed)
                                      │  DifferenceRequiredVsReported (computed)
                                      │
                                      ├─1:N─► PayrollEmployeeLaborHours
                                      │       (one row per calendar day)
                                      │       LaborHourDate, StraightTimeHours,
                                      │       OvertimeHours, SalariedEmployeeHours
                                      │
                                      ├─1:N─► PayrollEmpFringeBenefExcept
                                      │       (per-class fringe exception)
                                      │
                                      └─1:N─► PayrollEmployeeOtherDeductionses
                                              (404 on awdemo; schema-only)
```

#### Entities

##### `CertifiedPayroll`

| Field | Type | Notes |
|---|---|---|
| `Id` | int | PK |
| `ContractId` | int | FK → Contract |
| `RefVendorId` | int | FK → RefVendor (the vendor whose payroll this is) |
| `PayrollNumber` | int | Sequential per vendor per contract |
| `ModificationNumber` | int | 0 = original, 1+ = resubmissions |
| `IsLatestModification` | bool | True if this is the current rev of (PayrollNumber) |
| `BeginDate` / `EndDate` | dt | The week covered (typically Mon–Sun) |
| `SubmittalDate` / `PrimeAcceptedDate` / `AgencyAcceptedDate` | dt | Three sign-off stages |
| `PrimeOriginalNotAcceptedDate` / `AgencyOriginalNotAcceptedDate` | dt | Rejection timestamps |
| `WorkflowPhaseId` | int | FK → WorkflowPhase (3 = agency-accepted in awdemo sample) |
| `FringeBenefitPaymentType` | string | `"Cash"` or `"Plan"` |
| `PaperCopyOnFile` | bool | True iff signed paper copy exists |
| `ReceivedDate` / `PaperCopyReceivedDate` | dt | Receipt log |
| `SubmissionMethod` | string | How it arrived |
| `PayrollSigner` / `SignedDate` | string / dt | Who signed |
| `ProxySignedDate` / `ProxySubmitDate` / `ProxySubmitterId` | dt / int | Prime-submits-on-behalf-of-sub trail |
| `TieredContractorId` | int | FK → upper-tier contractor if this is a sub-of-sub |
| `PayrollExceptionRulesRerunDate` | dt | When the exception engine was last re-run |

**Example (awdemo):** `CertifiedPayrolls` has rows across 10+ contracts. Contract 43 is the heaviest (22 payrolls); contract 38 (Bacco) has 8. CP #1: `ContractId=38, RefVendorId=8688 (City Steel), PayrollNumber=1, BeginDate=2014-06-01, EndDate=2014-06-07, PaperCopyOnFile=true, PrimeAcceptedDate=2014-08-13, WorkflowPhaseId=3`. There are 3 modifications of PayrollNumber 1 on that contract (`Id=1,2,3`, `ModificationNumber=0,1,2`) — same vendor re-submitted the same week after exception feedback.

##### `PayrollEmployee`

The *header* record for one employee on one payroll. 56 fields; the ones that matter:

| Field | Type | Notes |
|---|---|---|
| `Id` | int | PK |
| `CertifiedPayrollId` | int | FK |
| `FirstName` / `LastName` / `MiddleInitial` | string | |
| `Ssn` / `PartialSsn` | string | Full and masked |
| `VendorSuppliedEmployeeID` | string | Vendor's internal payroll ID |
| `RefEmployeeId` | int | FK → RefEmployee (master cross-contract employee record) |
| `Gender` / `EthnicGroup` | string | For EEO workforce reporting |
| `AddressLine1` / `City` / `State` / `Zip` | string | |
| `TotalHours` / `StraightTimeHours` / `OvertimeHours` | decimal | Vendor-reported totals |
| `CalcTotalHours` / `CalcTotalStraightTimeHours` / `CalcTotalOvertimeHours` | decimal | System-computed from LaborHour rows (should match) |
| `GrossPay` / `NetPay` / `TotalDeductions` | decimal | Vendor-reported |
| `CalcGrossPay` / `CalcTotalOtherDeductions` | decimal | System-computed |
| `FICAWithholdingAmount` / `FederalWithholdingAmount` / `StateWithholdingAmount` / `MedicareWithholdingAmount` | decimal | Standard deductions |
| `FringeBenefits` / `CalcFringeBenefits` | decimal | Vendor-reported fringe vs system-computed |
| `GrossProjectAmountEarned` / `TotalProjectFringePaid` | decimal | Per-project rollup |
| `PaymentType` | string | `"Hourly"` or `"Salaried"` |
| `OriginalPayrollCheckNum` / `ModifiedPayrollCheckNum` | string | Audit trail |
| `IncludesZeroHourEmployees` | bool | True if the vendor lists employees who worked 0 hours (allowed for "available" workers) |

**Example (awdemo):** CP 1, PayrollEmployee #1 — Fred A. Smith, SSN 123-12-1234, ethnic group `"CAUC"`, male, 40 straight-time hours, GrossPay $1,600, NetPay $1,039.89, FringeBenefits $862, PaymentType "Hourly".

##### `PayrollEmployeeLabor`

The *per-craft-per-project* breakout. One employee can have multiple rows if they worked across projects or crafts. **62 fields** — this is where the compliance math happens.

| Field | Type | Notes |
|---|---|---|
| `Id` | int | PK |
| `PayrollEmployeeId` | int | FK |
| `ContractProjectId` | int | FK → ContractProject |
| `CraftCode` | string | AMS craft code (not DOL craft; cross-walk via wage decision) — e.g. `"15"` (operator), `"10"` (laborer), `"40"` (ironworker) |
| `LaborClassId` | int | FK → `LaborClass` (= specific classification within a craft, e.g. `OEG11` = Operator Group 11, crane 120-140ft boom) |
| `Apprentice` | bool | True iff worker is a registered apprentice |
| `ApprenticeId` | int | FK → `RefEmployeeApprenticeship` for the apprentice program they're in |
| `ApprenticePercentageOfWage` | int | Current progression stage % |
| `OJTProgramIndicator` | bool | True iff this labor counts toward OJT goal |
| `StraightTimeHourlyRate` / `OvertimeHourlyRate` | decimal | Rate paid |
| `HealthWelfareRate` / `VacationHolidayRate` / `ApprenticeshipFundRate` / `PensionRate` / `Other1Rate` / `Other2Rate` | decimal | Per-hour fringe rates |
| `FringeBenefits` / `CalcFringeBenefits` | decimal | Totals |
| `LumpSumPayment` | decimal | For fringe paid as cash rather than into a plan |
| `TotalHours` / `StraightTimeHours` / `OvertimeHours` / `SalariedHours` | decimal | Totals (vendor-reported) |
| `CalcTotalHours` / `CalcTotalStraightTimeHours` / `CalcTotalOvertimeHours` | decimal | Totals (system-computed from `PayrollEmployeeLaborHours`) |
| `GrossPay` / `NetPay` / `TotalDeductions` / `TotalOtherDeductions` | decimal | |
| `RegularHourlyRate` / `NormalSalary` | decimal | Base rates |
| `RequiredCompensation` | decimal | **System-computed from wage decision** × hours. This is the Davis-Bacon minimum. |
| `DifferenceRequiredVsReported` | decimal | **The violation amount** — `GrossPay - RequiredCompensation`. Negative = under-paid, exception fires. |
| `GrossProjectAmountEarned` / `GrossProjectAmountEarnedRounded` | decimal | Earned on this project |
| `CalcSalariedAverageHourlyRate` / `CalcSalaryProjectTotalAmount` | decimal | For salaried workers |

**Example (awdemo):** PayrollEmployeeLabor #1 — Fred Smith on CP 1, `ContractProjectId=41`, `CraftCode="15"`, `LaborClassId=20` (= OEG11 = "Operator Group 11, Crane with combined boom and jib between 120ft and 140ft"), StraightTimeHourlyRate $40, OvertimeHourlyRate $60, 40 straight-time hours, GrossPay $1,600, LumpSumPayment $862 (fringe paid cash).

##### `PayrollEmployeeLaborHour`

Per-day leaf of the tree. Each `PayrollEmployeeLabor` has 7 of these (one per day of the week).

| Field | Type |
|---|---|
| `Id` | int |
| `PayrollEmployeeLaborId` | int |
| `LaborHourDate` | dt |
| `StraightTimeHours` / `OvertimeHours` / `SalariedEmployeeHours` | decimal |

##### `CertifiedPayrollException`

The exception-engine output. One row per violation detected. **The core compliance exception feed.**

| Field | Type | Notes |
|---|---|---|
| `Id` | int | PK |
| `CertifiedPayrollId` | int | FK |
| `Type` | string | `"Fringe"`, `"Labor"`, `"Deduction"`, `"General"` |
| `Description` | string | Human-readable description. Highly structured, mentions vendor, contract, payroll #, employee, project, labor class, and the specific numeric gap. |
| `MustBeResolved` | bool | Hard-fail vs soft-flag |
| `Resolved` | bool | True once closed out |
| `ExceptionResolvedBy` / `ExceptionResolutionDate` | string / dt | Who closed it, when |
| `ResolutionComments` | string | Why it was closed |
| `VendorNotified` / `VendorNotifiedDate` | bool / dt | Did we tell the vendor? |
| `FailedPayrollEmployeeId` | int | FK → the exact `PayrollEmployee` that triggered this |
| `FailedRefEmployeeId` / `FailedRefEmployeeEmployerId` | int | FKs for cross-contract employee tracking |
| `ConformanceWageDecisionId` | int | FK → `ConformanceWageDecision` if the exception references an approved conformance |
| `PayrollExceptionRuleId` | int | FK → `PayrollExceptionRule` (which rule fired) |
| `AgencyComments` | string | DOT-side notes |
| `TokenHash` / `TokenJson` | string | Internal rule-engine state blob |

**Example (awdemo), CP 1 (Bacco contract 38):** 9 exceptions:
- #1: Fred Smith — reported fringe $862 ≠ calculated fringe $0 (Type `"Fringe"`)
- #2: Fred Smith — reported wage below Davis-Bacon minimum ($2,426.80) for craft 15/STATEWIDE/OEG11 under decision MI6935 mod 0 (Type `"Labor"`)
- #3: John Jones — similar fringe mismatch
- #4: John Jones — reported wage below $1,118.80 required for craft 10/STATEWIDE/LBDW (Distributed Work Laborer)
- #5: Shirley Samples — fringe mismatch
- #6: Shirley Samples — Total Deductions $124.04 ≠ Standard+Other Deductions sum $224.04
- #7: Shirley Samples — below-minimum wage for LBDW
- …

The exception descriptions are **highly structured strings** — a UI can regex them to extract {VendorId, ContractId, PayrollNumber, Employee, LaborClass, DOLDecision, Shortfall$} and build per-vendor remediation worklists.

##### `PayrollExceptionRule`

The catalog of rules the engine runs. **9 fields:**

| Field | Type | Notes |
|---|---|---|
| `Id` | int | PK |
| `Name` | string | Internal rule name (e.g. `"AgencyOptionHolidayMultiplierMissingHolidayPay"`, `"AgencyOptionHolidayMultiplierMissingRefHoliday"`) |
| `CustomMessage` | string | Agency-customized message to show |
| `ResolutionAction` | string | `"Must Be Resolved"`, `"May Be Left Unresolved"`, `"Must Be Resolved With Explanation"` |
| `ObsoleteDate` | dt | When retired |

##### `CertPayrollBenefitProgram`

Per-payroll declaration of health/pension plans. Required when fringes are paid into plans rather than cash. 12 fields.

| Field | Notes |
|---|---|
| `CertifiedPayrollId` | FK |
| `BenefitProgramName` | e.g. `"Health Insurance Co, Inc"` |
| `BenefitAccountId` | Trustee account # |
| `TrusteeContactPerson` / `TrusteeContactPhoneNum` | Who to call for verification |
| `BenefitProgramType` | `"Fringe Health/Welfare"`, `"Pension"`, `"Vacation/Holiday"`, `"Apprenticeship"` |
| `BenefitClassification` | `"All"` or specific LaborClass code |

##### `PayrollEmpFringeBenefExcept`

Per-employee-per-labor-class fringe exception. 8 fields. Rare but populated.

#### Rollup query — payrolls overdue by contract

```python
# Get all active contracts (ContractStatus eq 'Active')
contracts = c.get('Contracts',
    filter="ContractStatus eq 'Active'",
    select='Id,Name,ActualStartDate,ActualCompletionDate'
)['value']

# For each, get last submitted payroll date (max EndDate)
# Expectation: weekly. Overdue = EndDate < today - 7 days.
import datetime as dt
today = dt.date.today()

for ct in contracts:
    cps = c.get('CertifiedPayrolls',
        filter=f'ContractId eq {ct["Id"]} and IsLatestModification eq true',
        select='Id,RefVendorId,EndDate',
        orderby='EndDate desc',
        top=1
    )['value']
    last_end = cps[0]['EndDate'] if cps else None
    overdue_days = None
    if last_end:
        last_end_d = dt.date.fromisoformat(last_end[:10])
        overdue_days = (today - last_end_d).days - 7
    print(f"Contract {ct['Name']}: last payroll ending {last_end}, overdue by {overdue_days}d")
```

#### Awdemo gotchas (payroll)

- `PayrollEmployeeOtherDeductions` entity set → **404** on awdemo. The nav property exists on `PayrollEmployeeLabor` as `PayrollEmployeeOtherDeductionses` (unusual plural) but the set is not exposed — can only reach via `$expand`.
- `PayrollManagementCompliance` set → **404**. Nav exists but set not exposed.
- `LaborClasses` set → **404**. Available only via `$expand=LaborClass` on PayrollEmployeeLabor. `RefLaborClasses` does not exist either; the top-level entity set is named `LaborClasses` in the EDMX but not routable.
- `CertifiedPayroll.IsLatestModification` is critical — ignore it and you'll double-count re-submitted payrolls. Always filter `IsLatestModification eq true` for current state.
- `ModificationNumber` increments without erasing prior modifications. The data model keeps the full audit trail.
- SSN is in plain text in awdemo (`"123121234"`) — in prod this field should either be redacted at the API layer or masked (`PartialSsn` is already the masked version with a prefix).
- Exception `Description` strings embed everything (`"Vendor ID '05702', Contract ID '003870', ..."`) — parse them if your UI needs structured fields; the FKs are only partially populated.
- `WorkflowPhaseId = 3` seems to be "agency accepted" in awdemo. Confirm with your installation's `WorkflowPhase` table (phases are configurable per DOT).

---

### 3. Prevailing wage & conformances

#### Overview

The Department of Labor publishes **general wage decisions** by state × construction type × county (`RefWageDecision`); each decision carries a schedule of required hourly rates and fringe amounts by craft (`RefWageDecisionClass`) and modifications update rates over time (`RefWageDecisionModification`). The DOT assigns one or more decisions to each project (`ProjectWageDecision`) and to each contract-project (`ContractProjectWageDecision`). When a prime encounters a craft on-site that isn't in the decision schedule — a specialty craft, a new classification — they file a **conformance request** that proposes a rate; once approved (DOL signs off), the agreed rate lives in `ConformanceWageDecision` and is applied to future payrolls on that contract-project.

The exception engine (previous section) uses this chain in reverse: for every `PayrollEmployeeLabor` row, it looks up the applicable wage decision via `ContractProjectWageDecision`, finds the row for that `CraftCode`/`LaborClassId`, computes `RequiredCompensation`, and compares to `GrossPay`.

#### Entity chain

```
   RefWageDecision                (DOL general decision, e.g. "MI6935")
       │
       │ 1:N
       ▼
   RefWageDecisionModification    (mod 0, 1, 2, ... — rate updates over time)
       │                          IsLatestModification flag
       │ 1:N
       ├──► RefWageDecisionCraft      (which crafts this mod covers)
       │
       │ (indirectly via RefWageZoneArea)
       │
       ▼
   RefWageDecisionClass           (actual rate per craft × zone)
       │ OriginalWageRate, OriginalHourlyFringe
       │ DecisionClassId
       │ RefWageZoneAreaId
       │
       └─► RefWageZoneArea ──► RefWageZoneAreaCounty (geographic scope)

   ProjectWageDecision  ◄──► Project
   ContractProjectWageDecision ◄──► ContractProject
       │ RecordSource ("Preconstruction" | "Construction")
       │ RefWageDecisionModificationId
       │
       └─► ConformanceWageDecision (per-contract-project per-craft override)
             DecisionClassId, WageRate, HourlyFringe, DOLDecisionDate
             (referenced by CertifiedPayrollException when a conformance
              is relied upon to resolve a Labor-type exception)
```

#### Entities

##### `RefWageDecision`

| Field | Notes |
|---|---|
| `Id` | PK |
| `Name` | DOL decision number (e.g. `"MI6934"`, `"MI6935"`) |
| `DecisionDate` | When DOL published it |
| `State` | 2-letter state code |
| `WageConstructionType` | `"1"` = Highway, `"2"` = Heavy, `"3"` = Building, `"4"` = Residential |
| `IssuingAuthority` | `"Federal"` (DOL) or `"State"` |
| `Description` | e.g. `"Highway Construction"` |

**Example (awdemo):** `RefWageDecisions` has 7 rows: MI6934, MI6935, MI20160003, etc. All Highway Construction, State `"MI"`, `IssuingAuthority: "Federal"`.

##### `RefWageDecisionModification`

| Field | Notes |
|---|---|
| `RefWageDecisionId` | FK |
| `ModificationNumDescr` | Mod number as string (`"0"`, `"1"`) |
| `PublicationDate` | When this mod took effect |
| `Comments` | Free text (often geographic scope, e.g. `"Clinton County"`) |
| `IsLatestModification` | True iff current mod |

##### `RefWageDecisionClass`

Per-classification rate. **The rate row.** `DecisionClassId` is a stable classification ID shared across modifications.

| Field | Notes |
|---|---|
| `RefWageZoneAreaId` | FK → geographic zone |
| `DecisionClassId` | FK → classification (OEG11, LBDW, etc.) |
| `OriginalWageRate` | $/hr base rate |
| `OriginalHourlyFringe` | $/hr fringe required |

**Example (awdemo):** DecisionClass 2 in zone 1 = $26.63/hr + $12.70 fringe; DecisionClass 4 in zone 2 = $36.16/hr + $15.37 fringe.

##### `RefWageDecisionCraft`

Simple mapping of craft codes per modification.

##### `ContractProjectWageDecision` / `ProjectWageDecision`

Links a wage-decision modification to a specific project. **Must exist for the payroll exception engine to have a baseline.**

| Field | Notes |
|---|---|
| `ContractProjectId` (/ `ProjectId`) | FK |
| `RefWageDecisionModificationId` | FK |
| `RecordSource` | `"Preconstruction"` (assigned at award) or `"Construction"` (added post-award) |

**Example (awdemo):** `ContractProjectWageDecision #2` → `ContractProjectId=41`, `RefWageDecisionModificationId=2`. That mod is for `RefWageDecisionId=4` (MI6935). So contract-project 41 is paying under wage decision MI6935 mod 1.

##### `ConformanceWageDecision`

Per-contract-project per-classification override. Approved deviation from the general decision.

| Field | Notes |
|---|---|
| `ContractProjectWageDecisionId` | FK → the base decision this is overriding |
| `DecisionClassId` | Which class |
| `Name` | Conformance # within the contract-project |
| `WageRate` / `HourlyFringe` | The approved alternative rate |
| `DOLDecisionDate` | When DOL approved it |

**Example (awdemo):** `ConformanceWageDecision #1` → ContractProjectWageDecisionId=5, DecisionClass=130, WageRate $12.00 + Fringe $2.00, DOL approved 2016-09-05. (A low-rate conformance — probably a laborer specialty craft.)

#### Rollup query — classifications in use on a contract vs decision baseline

```python
# What crafts/classes are actually appearing on payroll
labors = c.get('PayrollEmployeeLabors',
    filter=f'PayrollEmployee/CertifiedPayroll/ContractId eq {cid}',
    select='Id,CraftCode,LaborClassId,RequiredCompensation,GrossPay,DifferenceRequiredVsReported',
    expand='LaborClass($select=Id,Name,Description)'
)['value']

classes_in_use = {}
for r in labors:
    key = (r['CraftCode'], (r.get('LaborClass') or {}).get('Name'))
    if key not in classes_in_use:
        classes_in_use[key] = {
            'description': (r.get('LaborClass') or {}).get('Description'),
            'count': 0, 'under_paid_count': 0,
        }
    classes_in_use[key]['count'] += 1
    if (r.get('DifferenceRequiredVsReported') or 0) < 0:
        classes_in_use[key]['under_paid_count'] += 1
```

#### Awdemo gotchas (prevailing wage)

- `LaborClasses` top-level set is **404** (see payroll gotchas). Hydrate class names only via `$expand=LaborClass` on PayrollEmployeeLabor or on a `ConformanceWageDecision` query via its implicit nav.
- `RefWageDecisionClass` carries no explicit modification link — rate scope is tracked by `RefWageZoneAreaId` and `DecisionClassId`. Lookup is: `(DecisionClass, Zone) → RefWageDecisionClass → rate`.
- The exception description string embeds the `DecisionClass` code (e.g. `"(15/ STATEWIDE/ OEG11)"`) as the display label — the triple is `(CraftCode / Zone / DecisionClassName)`.
- `ConformanceWageDecisions` has records without rates (`Id=2` has `DecisionClassId=131` but no WageRate/HourlyFringe) — those are **pending-approval** stubs. Filter `WageRate ne null` for approved-only.

---

### 4. Civil-rights, labor-compliance, and EEO reviews

#### Overview

Three related review types, all keyed on `ContractorId` (= `Contractor.Id`, which links to a RefVendor and a Contract):

- **`LaborComplianceReview`** — the broadest. Covers personnel actions, records/reports, subcontracting practices, training/promotion, union compliance. 37 fields of binary checkbox + date + reviewer-id tuples.
- **`EEOComplianceReview`** — 44 fields, focused on Equal Employment Opportunity. Tracks affirmative-action plan, drug-free workplace plan, workforce composition reviews, apprenticeship review, EEO policy posting.
- **`ComplianceFinding`** — summary attestation, often one per review period, with `VendorCompliant` boolean.

All three are typed by `Type = "Contract"` or `"Vendor"` — a review scoped to one contract vs a general review of the vendor.

#### Entity chain

```
                  (reviews are keyed on ContractorId, not ContractId —
                   a vendor can be reviewed per-contract or at vendor level)
   Contractor ──┬──► LaborComplianceReview  (one per contract per reviewer)
                │     Type ("Contract" | "Vendor")
                │     ReviewType ("Office" | "Field")
                │     GeneralReviewDate / GeneralReviewBy
                │     PersonnelAction + PersonnelActionReviewDate / By
                │     RecordsReports + RecordsReportsDate / ReviewedBy
                │     Subcontracting + SubcontractingDate / ReviewedBy
                │     TrainingPromotion + …Date / By
                │     Union + UnionReviewDate / By
                │     VendorCompliant + VendorCompliantDate
                │     LatestComplianceReviewDate / By
                │     ComplianceReviewComments
                │
                ├──► EEOComplianceReview
                │     Compliant ("Yes" | "No")
                │     ContractorReviewType ("Both Prime and Subcontractors",…)
                │     AffirmActionPlan + Comments
                │     DrugFreeWorkplacePlan + Comments
                │     + ~15 other similar binary + comment + date triples
                │
                └──► ComplianceFinding
                      ReviewDate, VendorCompliant, VendorType ("Prime" | "Sub")
                      ConductedBy
```

#### Entities

##### `LaborComplianceReview` (37 fields)

Key fields:

| Field | Notes |
|---|---|
| `Id` | PK |
| `ContractorId` | FK → Contractor (not RefVendor directly) |
| `Type` | `"Contract"` or `"Vendor"` |
| `ReviewType` | `"Office"` / `"Field"` |
| `ReviewedBy` | Reviewer person-id (string in awdemo, e.g. `"3331"`) |
| `GeneralReviewDate` / `GeneralReviewBy` | Overall review log |
| `LatestComplianceReviewDate` / `LatestComplianceReviewBy` | Most recent (used for "next review due" calendars) |
| `PersonnelAction` / `…ReviewDate` / `…ReviewBy` | Personnel-action sub-review (promotion, discipline, EEO complaints) |
| `RecordsReports` / `…Date` / `…ReviewedBy` | Records-and-reports sub-review |
| `Subcontracting` / `SubcontractingDate` / `SubcontractingReviewedBy` | Subcontract practices sub-review |
| `TrainingPromotion` / `…ReviewDate` / `…ReviewBy` | T&P sub-review |
| `Union` / `UnionReviewDate` / `UnionReviewedBy` | Union compliance sub-review |
| `VendorCompliant` | **Overall roll-up boolean** — the headline |
| `VendorCompliantDate` | When that attestation was made |
| `ComplianceReviewComments` | Free text (e.g. `"No issues found"`) |

**Example (awdemo):** `LaborComplianceReview #1` — ContractorId 83, Type `"Contract"`, ReviewType `"Office"`, VendorCompliant=true, "No issues found."

##### `EEOComplianceReview` (44 fields)

Pattern: for each EEO topic, three fields — binary `<Topic>`, `<Topic>Comments`, `<Topic>ReviewedBy` (or variants). Topics include:

- `AffirmActionPlan` — Affirmative Action Plan on file
- `DrugFreeWorkplacePlan` — Drug-free workplace policy
- Policy postings
- Workforce composition review
- Apprentice program review
- Field interviews conducted

Headline fields:

| Field | Notes |
|---|---|
| `Id` | PK |
| `ContractorId` | FK |
| `Type` | `"Contract"` or `"Vendor"` |
| `ContractorReviewType` | `"Both Prime and Subcontractors"`, `"Prime Only"`, etc. |
| `Compliant` | `"Yes"` / `"No"` (string!) |
| `CompliantDate` / `CompliantReviewComments` | |
| `GeneralReviewedBy` / `GeneralReviewedDate` | |

**Example (awdemo):** EEO #1 — ContractorId 101, Compliant=`"No"`. EEO #2 — ContractorId 7, Compliant=`"Yes"`, review date 2013-05-15, AffirmActionPlan=true, comment "Reviewed on: 05-15-2013, Reviewed by: 332 - Rusch, David - Newberry TSC".

##### `ComplianceFinding` (20 fields)

Finding-level record (vs the per-sub-review-topic flags on LaborComplianceReview).

| Field | Notes |
|---|---|
| `ContractorId` | FK |
| `VendorType` | `"Prime"` / `"Sub"` |
| `ReviewDate` | When the finding was recorded |
| `ConductedBy` | Reviewer id |
| `VendorCompliant` | Headline bool |

**Example (awdemo):** Finding #1 — ContractorId 83, Prime, 2014-08-07, VendorCompliant=true.

##### `FieldInterviewJobClassification`

Workforce composition sampling. One row per interviewed worker's classification attestation.

| Field | Notes |
|---|---|
| `FieldInterviewEmployeeId` | FK → `FieldInterviewEmployee` (not probed; schema shows this chain) |
| `JobClassificationId` | FK → `RefWageDecisionClass` or similar |
| `WageRate` | What the worker reports being paid (compares against decision) |
| `DescriptionOfDutiesAndTools` | Free text (e.g. `"Welding"`, `"Flagging"`) |

**Example (awdemo):** Interview #1 — classified 109, duties `"Welding"`, reported wage $19.50. Interview #2 — classified 104 (flagger), reported wage $13.00.

#### Awdemo gotchas (reviews)

- `ContractorId` is **not** `RefVendorId` — a `Contractor` row joins a RefVendor to a specific contract (via `Contractor.ContractId` / `Contractor.RefVendorId`). To cross-walk a review to a vendor name: `ComplianceFinding → Contractor → RefVendor`.
- `EEOComplianceReview.Compliant` is a **string** `"Yes"`/`"No"`, not a bool — easy to miss in UI validators.
- Reviewer IDs are strings (`"3331"`, `"332"`) — they're not FKs to anything resolvable via awdemo API (PersonInfos is 403). Treat them as opaque codes.
- There's no explicit `ReviewFinding` or `CorrectiveAction` entity (the vendor guide hints at them). Non-compliance is captured by setting `VendorCompliant=false` on the review itself; the comment carries the narrative.
- `NonComplianceIssue` entity set → **404** on awdemo (no standalone escalation ledger).

---

### 5. OJT (on-the-job training)

#### Overview

FHWA requires state DOTs to maintain an OJT program (23 CFR Part 230, Appendix B) that trains minorities, women, and economically disadvantaged workers on highway construction. The agency sets an **annual goal** (`OjtGoal`) — N trainees or N hours; approved **OJT programs** (`RefOjtProgram`) define curricula (e.g. "Reinforcing Steel Ironworker") with required graduation hours and wage-rate progression stages; vendors assign specific workers to specific contracts (`OjtContractAssignment` → `OjtProgramEnrollment` → `RefEmployee`). The hours a trainee works show up in the certified payroll with `OJTProgramIndicator = true` and roll into the OJT goal measurement.

#### Entity chain

```
   OjtGoal                     (annual agency-wide goal, e.g. "7 trainee-hours")
     Program, YearStartDate, YearEndDate, OJTGoal, OJTUnits

   RefOjtProgram               (program definition, e.g. "Reinforcing Steel - Ironworker")
     Name, OJTHoursToGraduate (e.g. 4000), OJTProgramSponsor, OJTProgramActive_DT
       │
       ├─1:N─► OjtProgramSkillSet            (what the program teaches)
       │       OjtCraftId (e.g. "40"), OjtClassId, OjtScheduledHours
       │
       ├─1:N─► OjtProgramWageRateProgression (apprentice wage % by stage)
       │       StageCompletionPercentage, AssociatedWageRatePercentage
       │
       └─1:N─► OjtProgramEnrollment           (one per worker enrolled)
                RefOjtProgramId, EmployerId (RefVendor), Status,
                Enrollment_Date, OrientationCompleteInd,
                HighestPriorityOjtCraft, HighestPriorityOjtClassId
                  │
                  │ 1:N (OjtContractAssignment)
                  ▼
         OjtContractAssignment  (enrollment × contract — a trainee can work multiple)
                ContractId, OjtProgramEnrollmentId, Status, Comments

   RefEmployeeApprenticeship            (per-worker apprenticeship record)
     RefEmployeeId, Name (program id), RequiredHoursToGraduate, ObsoleteDate
       │
       └─1:N─► RefEmployeeApprenticeshipCraftDecision
                 ApprenticeCraftCode  (the craft they're apprenticing in)
```

#### Entities

##### `OjtGoal`

| Field | Notes |
|---|---|
| `Program` | `"FHWA"` or `"OJT"` |
| `YearStartDate` / `YearEndDate` | Reporting year |
| `OJTGoal` | Numeric target |
| `OJTUnits` | `"Trainees"` or `"Hours"` |

**Example (awdemo):** `OjtGoal #1` = Program FHWA, 2014 calendar year, 50 trainees. `OjtGoal #2` = Program OJT, Aug 2019 – Jul 2020, 7 hours.

##### `RefOjtProgram`

| Field | Notes |
|---|---|
| `Name` | Program name (e.g. `"Reinforcing Steel - Ironworker"`, `"CARPENTER TRAINEE"`) |
| `OJTProgramActive_DT` | Effective date |
| `OJTHoursToGraduate` | Hours required (e.g. 4000, 520) |
| `OJTProgramSponsor` | `"OLI"`, `"DOT"`, etc. |

##### `OjtProgramEnrollment`

| Field | Notes |
|---|---|
| `RefOjtProgramId` | FK → program |
| `EmployerId` | FK → RefVendor (the employer of record) |
| `Status` | `"Active"`, `"Graduated"`, etc. |
| `Enrollment_Date` | |
| `OrientationCompleteInd` | Did they finish orientation? |
| `HighestPriorityOjtCraft` | Craft code (e.g. `"40"`) |
| `HighestPriorityOjtClassId` | FK |

##### `OjtContractAssignment`

| Field | Notes |
|---|---|
| `ContractId` | FK → Contract |
| `OjtProgramEnrollmentId` | FK → enrollment |
| `Status` | `"Active"`, `"Completed"` |
| `Comments` | Free text (e.g. `"Introduced at the start of the contract"`) |

**Example (awdemo):** OJT Assignment #1 → Contract 38, enrollment #1 (a Reinforcing Steel Ironworker trainee), Active, "Introduced at the start of the contract."

##### `OjtProgramSkillSet` / `OjtProgramWageRateProgression`

Program-level definitions of what the trainee will learn and how the wage increases as they progress through the program.

**Example (awdemo):** `OjtProgramSkillSet #1` → RefOjtProgram 1, OjtCraftId "40", 4000 hours scheduled, OjtClassId 73. `OjtProgramWageRateProgression #1` → stage 100% = wage 100% (the final stage, full craft wage).

##### `RefEmployeeApprenticeship` / `RefEmployeeApprenticeshipCraftDecision`

Per-worker apprenticeship records (lower-level, separate from OJT enrollment but overlapping — apprentices are a subset of OJT trainees).

**Example (awdemo):** Apprenticeship #1 = RefEmployee 991, program "JJJ3409", craft "40". Apprenticeship #2 = RefEmployee 985 (= Fred Smith from CP 1!), program "12345", craft "45", obsoleted 2022-07-31, required 60 hours to graduate.

#### Awdemo gotchas (OJT)

- `OjtGoal` has no `ContractId` — it's an **agency-wide annual goal**. Actual OJT progress is rolled up by summing payroll hours where `OJTProgramIndicator=true` across all contracts in the year.
- `RefVendorOjtGoals` set → **empty** (no per-vendor goals in awdemo).
- `RefOjtProgram.Name` has mixed casing (`"Reinforcing Steel - Ironworker"` vs `"CARPENTER TRAINEE"`) — don't rely on consistent case for display.
- `OjtProgramSkillSet.OjtCraftId` is a **string** (craft code), not an int FK.
- Apprentice tracking lives in two parallel places: `OjtProgramEnrollment` (program-centric) and `RefEmployeeApprenticeship` (worker-centric). They overlap but aren't formally linked — worker 985 appears in both but the records aren't FK-connected.

---

### 6. UI query recipes

Each recipe gives: user-visible question, OData query (copy-paste ready), expected response shape, performance notes.

#### 6.1 Contract compliance passport (one contract, all layers)

**Question:** "Give me one page showing contract **{id}**'s DBE commitment vs utilization, payroll currentness, open exceptions, review status, OJT assignments."

```
# 1. DBE commitment baseline
GET /ContractCurrDbeCommitSummaries?$filter=ContractId eq {cid}
    &$expand=ContractCurrDbeCommitments($expand=DbeVendor($select=Id,Name,LongName))

# 2. DBE actual utilization
GET /SubcontractorPayments?$filter=ContractPayment/ContractId eq {cid} and DbeFirm eq true
    &$expand=Payee($select=Id,Name,LongName)
    &$select=Id,PaidDate,PaidAmount,AmountReceived,PayeeId,PaymentType,TotalDbeCreditAmount

# 3. Payroll currentness
GET /CertifiedPayrolls?$filter=ContractId eq {cid} and IsLatestModification eq true
    &$orderby=EndDate desc
    &$select=Id,RefVendorId,PayrollNumber,BeginDate,EndDate,PrimeAcceptedDate,AgencyAcceptedDate,WorkflowPhaseId

# 4. Open exceptions
GET /CertifiedPayrollExceptions?$filter=CertifiedPayroll/ContractId eq {cid} and Resolved eq false
    &$select=Id,CertifiedPayrollId,Type,Description,MustBeResolved,PayrollExceptionRuleId

# 5. Reviews (indirect via Contractor)
GET /Contractors?$filter=ContractId eq {cid}&$select=Id,RefVendorId,IsOriginalOrPrime
# then for each contractor_id:
GET /LaborComplianceReviews?$filter=ContractorId eq {ctor_id}&$orderby=LatestComplianceReviewDate desc&$top=1
GET /EEOComplianceReviews?$filter=ContractorId eq {ctor_id}&$orderby=GeneralReviewedDate desc&$top=1

# 6. OJT assignments
GET /OjtContractAssignments?$filter=ContractId eq {cid}
    &$expand=OjtProgramEnrollment($expand=RefOjtProgram($select=Id,Name,OJTHoursToGraduate))
```

**Response shape:** 6 parallel bundles. Fan these out with `asyncio.gather`; latency = max of the 6 (worst was ~400ms in awdemo for the DBE summary expand).

**Performance:** DBE summary expand is the slowest at ~400ms (it fetches ~5 commitments + DBE vendor for each). Payroll currentness is fast (~80ms with `$top=1` per vendor). The review lookup is N+1 across contractors — if the contract has 20 subs, that's 40 round trips. Mitigate: `$filter=ContractorId in ({c1,c2,c3,...})` to batch per endpoint.

#### 6.2 DBE utilization leaderboard — portfolio-wide

**Question:** "Across all our active contracts, which primes are falling furthest behind on DBE commitments?"

```
# 1. Every active contract's current DBE summary
GET /ContractCurrDbeCommitSummaries?$filter=Contract/ContractStatus eq 'Active'
    &$expand=Contract($select=Id,Name,AwardedContractAmount),RefVendor($select=Id,LongName)
    &$select=Id,ContractId,RefVendorId,VendorName,TotalCommitAmt,TotalCommitPct,DbeSubCommitAmt

# 2. All DBE payments across those contracts (one query, filter by DbeFirm)
GET /SubcontractorPayments?$filter=DbeFirm eq true
    &$expand=ContractPayment($select=Id,ContractId)
    &$select=Id,ContractPaymentId,PayeeId,PaidAmount,PaidDate

# Client-side rollup:
# bucket payments by ContractPayment.ContractId, sum PaidAmount
# join to commitments, compute utilization% = sum(paid) / TotalCommitAmt
# rank ascending (worst first)
```

**Response shape:** rows of `{contract_id, name, prime_vendor, committed_$, paid_$, utilization_%, delta_$}`.

**Performance:** 2 queries total regardless of portfolio size. Awdemo returns ~5 commit summaries + 11 DBE payments in <500ms total. Scales linearly with contract count; at 500 active contracts expect ~2–3s cold. **Cache the result for 15 min** — DBE utilization changes slowly.

#### 6.3 Payrolls overdue exception feed

**Question:** "Which active contracts have no certified payroll submitted in the last 7 days (or 14, or 30 — tunable threshold)?"

```
# All active contracts
GET /Contracts?$filter=ContractStatus eq 'Active'
    &$select=Id,Name,ActualStartDate,ActualCompletionDate

# For each contract, max payroll EndDate
GET /CertifiedPayrolls?$filter=ContractId eq {cid} and IsLatestModification eq true
    &$orderby=EndDate desc&$top=1&$select=Id,EndDate,SubmittalDate
```

**Response shape:** `[{contract_id, name, days_since_last_payroll, oldest_vendor_overdue}]`

**Performance:** N+1 across contracts. On awdemo (276 contracts) this is ~15s cold. **Mitigation:** fire 20 at a time with `asyncio.gather`; or precompute daily and cache for the day — overdue status rarely changes within a day.

#### 6.4 Vendor-level open payroll exceptions

**Question:** "Payrolls from {vendor_id} that have unresolved exceptions needing attention."

```
GET /CertifiedPayrollExceptions?$filter=
    CertifiedPayroll/RefVendorId eq {vid}
    and Resolved eq false
    and MustBeResolved eq true
    &$expand=CertifiedPayroll($select=Id,ContractId,PayrollNumber,BeginDate,EndDate,RefVendorId),
             PayrollExceptionRule($select=Id,Name,ResolutionAction)
    &$orderby=CertifiedPayroll/EndDate desc
```

**Response shape:** list of `{exception_id, payroll_ref, type, description, rule_name, resolution_action}`.

**Performance:** awdemo returns 9 exceptions in <200ms for the full dataset. Will scale fine for prod — exceptions per vendor rarely exceed ~100.

#### 6.5 Payroll detail drill-down — one employee's full week

**Question:** "Show me every hour {employee_id} worked under payroll {cp_id}."

```
GET /PayrollEmployees?$filter=CertifiedPayrollId eq {cp_id} and Id eq {pe_id}
    &$expand=PayrollEmployeeLabors(
        $expand=
            LaborClass($select=Id,Name,Description),
            PayrollEmployeeLaborHours($select=Id,LaborHourDate,StraightTimeHours,OvertimeHours,SalariedEmployeeHours),
            PayrollEmpFringeBenefExcepts
    ),FailedPayrollEmployeeCertifiedPayrollExceptions($select=Id,Type,Description,Resolved)
```

**Response shape:** employee header + nested labor rows + per-day hours + any fringe exceptions + any exceptions where this employee failed.

**Performance:** single round-trip. Awdemo returns the whole tree in ~300ms. **The right page shape for an "employee week" drawer in the certified-payroll detail UI.**

#### 6.6 Prevailing wage violations roll-up

**Question:** "For contract {cid}, which labor classifications have under-paid workers, and by how much?"

```
GET /PayrollEmployeeLabors?$filter=PayrollEmployee/CertifiedPayroll/ContractId eq {cid}
    and DifferenceRequiredVsReported lt 0
    &$expand=LaborClass($select=Id,Name,Description),
             PayrollEmployee($select=Id,FirstName,LastName,CertifiedPayrollId;
                $expand=CertifiedPayroll($select=Id,PayrollNumber,BeginDate,EndDate))
    &$select=Id,CraftCode,LaborClassId,TotalHours,GrossPay,RequiredCompensation,DifferenceRequiredVsReported
    &$orderby=DifferenceRequiredVsReported
```

**Response shape:** list of under-paid labor rows, worst gap first. **Group client-side** by `(CraftCode, LaborClassId)` to summarize "LBDW (Distributed Work Laborer): 3 workers under-paid by total $4,200."

**Performance:** 1 round trip. Will scale to the thousands of labor rows typical of a large contract.

#### 6.7 Civil-rights review calendar (next review due)

**Question:** "Which contractors are overdue for a labor-compliance review (last review > N days ago)?"

```
# All active contractor assignments
GET /Contractors?$filter=Contract/ContractStatus eq 'Active'
    &$expand=Contract($select=Id,Name),RefVendor($select=Id,LongName)
    &$select=Id,ContractId,RefVendorId,IsOriginalOrPrime

# For each contractor, most recent LaborComplianceReview
GET /LaborComplianceReviews?$filter=ContractorId eq {ctor_id}
    &$orderby=LatestComplianceReviewDate desc&$top=1
    &$select=Id,LatestComplianceReviewDate,VendorCompliant,Type
```

**Response shape:** `[{contractor_id, vendor_name, contract_name, last_review_date, days_since, vendor_compliant_at_last_review}]`.

**Performance:** again N+1. Awdemo has ~700 Contractors; 2 min cold. **Precompute daily into a materialized view in the backend** — review currentness changes slowly.

#### 6.8 EEO compliance roll-up

**Question:** "Which contractors have failed their most recent EEO review?"

```
GET /EEOComplianceReviews?$filter=Compliant eq 'No'
    &$expand=Contractor($expand=RefVendor($select=Id,LongName),Contract($select=Id,Name,ContractStatus))
    &$orderby=GeneralReviewedDate desc
```

**Response shape:** list of failing reviews with full vendor + contract context.

**Performance:** single query. Awdemo has 1 failing EEO review — returns instantly. In prod expect at most dozens.

#### 6.9 DBE good-faith-effort detail (bid-time view)

**Question:** "For contract {cid} where the prime missed DBE goal, show me every DBE they claim to have contacted."

```
GET /ContractApprDbeCommitSummaries?$filter=ContractId eq {cid}
    &$expand=ContractApprGoodFaithEfforts(
        $expand=DbeVendor($select=Id,Name,LongName,DBECertificationStatus)
    )
    &$select=Id,VendorName,TotalCommitPct,GoodFaithEffort
```

Note: `DBECertificationStatus` doesn't exist on `RefVendor` in awdemo (common pitfall); drop that select and use `RefVendorDbeCertificationEvents` separately.

**Response shape:** summary + list of contacted DBEs with quote, response, reason-not-committed.

#### 6.10 OJT portfolio progress against annual goal

**Question:** "How many OJT trainee-hours have we delivered this fiscal year vs the goal?"

```
# Goal for current year
GET /OjtGoals?$filter=YearStartDate le {today} and YearEndDate ge {today}
    &$select=Id,Program,YearStartDate,YearEndDate,OJTGoal,OJTUnits

# All active enrollments
GET /OjtProgramEnrollments?$filter=Status eq 'Active'
    &$expand=RefOjtProgram($select=Id,Name,OJTHoursToGraduate)
    &$select=Id,RefOjtProgramId,EmployerId,Enrollment_Date,HighestPriorityOjtCraft

# Hours delivered — sum payroll labor hours where OJTProgramIndicator=true
# in the goal window:
GET /PayrollEmployeeLabors?$filter=
    OJTProgramIndicator eq true and
    PayrollEmployee/CertifiedPayroll/BeginDate ge {year_start}
    and PayrollEmployee/CertifiedPayroll/EndDate le {year_end}
    &$select=Id,TotalHours,PayrollEmployeeId
```

**Response shape:** `{goal: 50, delivered: 1247, pct_of_goal: 2494%, active_trainees: 12}` or similar.

**Performance:** 3 queries. The hours sum could return thousands of rows on a busy year — paginate with `$top=5000&$skip=…` and sum client-side.

#### 6.11 "Vendor compliance passport" — all compliance posture across contracts for one vendor

**Question:** "For vendor {vid}, show me across all their contracts: payroll currentness, open exceptions, DBE commitments made to them (if they're a DBE), labor + EEO review history."

```
# All contractor assignments for this vendor
GET /Contractors?$filter=RefVendorId eq {vid}
    &$expand=Contract($select=Id,Name,ContractStatus)
    &$select=Id,ContractId,IsOriginalOrPrime,Type

# Latest payroll per contract where they're the vendor
GET /CertifiedPayrolls?$filter=RefVendorId eq {vid} and IsLatestModification eq true
    &$orderby=EndDate desc&$top=50

# Open exceptions
GET /CertifiedPayrollExceptions?$filter=
    CertifiedPayroll/RefVendorId eq {vid} and Resolved eq false
    &$select=Id,Description,Type,CertifiedPayrollId

# As DBE: commitments made to them across contracts
GET /ContractCurrDbeCommitments?$filter=DbeVendorId eq {vid}
    &$expand=ContractCurrDbeCommitSummary($expand=Contract($select=Id,Name))
    &$select=Id,CommitmentAmt,RaceConsciousAmt,ReviewDt

# As DBE: payments received
GET /SubcontractorPayments?$filter=PayeeId eq {vid}
    &$expand=ContractPayment($select=Id,ContractId),Payer($select=Id,LongName)

# Reviews (across contractor rows)
GET /LaborComplianceReviews?$filter=Contractor/RefVendorId eq {vid}
    &$orderby=LatestComplianceReviewDate desc
GET /EEOComplianceReviews?$filter=Contractor/RefVendorId eq {vid}
    &$orderby=GeneralReviewedDate desc
```

**Response shape:** 7-section passport bundle.

**Performance:** 7 parallel queries. Awdemo returns in ~1.5s for an active vendor. **Perfect candidate for the vendor-detail page.**

#### 6.12 DBE certification history for a single vendor

**Question:** "Show me vendor {vid}'s DBE certification events (application, approval, expiration, decertification)."

```
GET /RefVendorDbeCertificationEvents?$filter=RefVendorId eq {vid}
    &$orderby=EventDate desc
    &$expand=RefActionType($select=Id,Name,Description)
```

**Response shape:** chronological list `[{date, action_type_name, assigned_to, comments}]`.

**Example:** Vendor 543 (Perez Construction) history:
- 2008-05-08: `RefActionTypeId=25` ("application received") — "Received application - processing"
- 2008-05-30: `RefActionTypeId=28` ("certification approved") — "All required documentation received and validated. Certification approved."

---

### 7. Cross-flow interactions

#### Compliance ↔ Labor hours (companion doc §1)

- `PayrollEmployeeLabor` is the compliance mirror of `DWRContractorPersonnel`. The DWR captures what the inspector saw crewed on-site that day (counts × craft × hours); CertifiedPayroll captures what the vendor said they paid for those hours. **Reconciliation gap** = suspected ghost workers or unpaid labor. There is no built-in join — your UI reconciles on `(ContractProjectId, CraftCode, WorkDate)` and expects within-tolerance match.
- `DecisionClass` vocabulary is shared between `DWRContractorPersonnel.DecisionClassId` (companion doc) and `PayrollEmployeeLabor.LaborClassId` → `LaborClass` → ... → the same decision class. One canonical craft taxonomy.
- `PayrollEmployeeLabor.OJTProgramIndicator = true` is how hours get counted toward the agency's annual OJT goal.
- The `ApprenticeId` on `PayrollEmployeeLabor` → `RefEmployeeApprenticeship` closes the loop with OJT: payroll says this worker is apprenticing, under which program, at what current stage (`ApprenticePercentageOfWage`).

#### Compliance ↔ Financial transactions (companion doc §2)

- `SubcontractorPayment` sits between the two: `ContractPayment` is the contract-level payment event (which pay-estimate paid out), `SubcontractorPayment` is the per-sub distribution. `DbeFirm`/`DbeCommitment`/`TotalDbeCreditAmount` flags turn ordinary sub-payments into the DBE utilization ledger.
- A `ChangeOrder` that modifies DBE-eligible contract-items should (in process) trigger a `ContractCurrDbeCommit*` revision (the "Curr" tree) so the baseline reflects post-award scope. The DOT compliance team drives that process — it's not an automatic cascade; the data model just supports storing both baselines.
- `PaymentEstimate` approval is sometimes gated on payroll currentness (if contract requires it); gate logic lives in the DOT's workflow config, not in the schema.

#### Compliance ↔ Items & materials (companion doc §3)

- Labor classifications ties to work-items via the per-item `ItemClassification` / `RefItemClassification` mapping — e.g. "Reinforcing Steel Furnish & Install" is labor-coded to "Ironworker" and should trigger OJT eligibility if an ironworker-trainee program is active.
- Not strongly coupled in awdemo — the gates are more procedural than data-driven.

#### Procurement ↔ Compliance

- The chain is: `ProposalSBPGoals` / proposal-level DBE goal → `ProposalVendorSBPCommitment` (winning bidder's commitment) → upon award, snapshots into `ContractApprDbeCommitSummary`. On awdemo the `ProposalVendorSBPCommitments` set 500s so this handoff can't be walked end-to-end there; the DBE side is intact.

#### Vendor master ↔ Compliance

- `RefVendor` carries no DBE certification status directly; status is derived from the most recent event in `RefVendorDbeCertificationEvents`. A vendor's "is DBE today" check is: `max(EventDate where RefActionTypeId in {28 (approved), 29 (re-certified)}) > max(EventDate where RefActionTypeId in {30 (decertified)})`.
- SBP certification mirrors in `RefVendorSBPCertifications`.

---

### 8. Awdemo gotchas master list

Highlights of the field-and-set gotchas spread throughout the sections above:

| # | Set / field | Gotcha |
|---|---|---|
| 1 | `PersonInfos` | 403 — can't resolve reviewer IDs to names on awdemo |
| 2 | `LaborClasses` | 404 — only reachable via `$expand=LaborClass` on PayrollEmployeeLabor or ConformanceWageDecision |
| 3 | `PayrollEmployeeOtherDeductions` | 404 — only reachable via expand |
| 4 | `PayrollManagementCompliance` | 404 — only via expand |
| 5 | `ContractSBPGoals`, `ContractSBPCommitments`, `ProposalVendorSBPCommitments`, `ProposalVendorSBPGoalGoodFaithEffort` | all 500 — SBP tracking broken on this lab instance |
| 6 | `DbeSuppliers` | returns 0 rows — supplier-DBE data lives in `ContractApprDbeSuppliers` / `ContractCurrDbeSuppliers` |
| 7 | `NonComplianceIssue`, `DbePayments`, `DbeShortfalls`, `DbeSubstitutions`, `SubcontractDbePayments`, `ContractDbePaymentReportings` | all 404 — no standalone top-level ledgers; derive from `SubcontractorPayments` where `DbeFirm=true` |
| 8 | `RefVendorSbpCertificationEvents` | empty set — use `RefVendorSBPCertifications` instead |
| 9 | `RefVendorOjtGoals` | empty — only agency-level `OjtGoals` populated |
| 10 | `RefVendor.DBECertificationStatus` | **doesn't exist** — vendor-level DBE status must come from `RefVendorDbeCertificationEvents` |
| 11 | `CertifiedPayroll.IsLatestModification` | **always filter on this** or you'll double-count revised payrolls |
| 12 | `EEOComplianceReview.Compliant` | **string** `"Yes"`/`"No"`, not bool |
| 13 | `OjtGoal` | has no `ContractId` — agency-wide goal; roll up actuals by summing `PayrollEmployeeLabor.TotalHours` where `OJTProgramIndicator=true` across all contracts |
| 14 | `ContractorId` on all reviews | points to `Contractor.Id` not `RefVendor.Id`; join via Contractor → RefVendor |
| 15 | SSN plain-text in `PayrollEmployee.Ssn` | awdemo exposes `"123121234"` — use `PartialSsn` in UIs or ensure prod API redacts |
| 16 | Exception `Description` strings | highly structured but not FK-linked — parse via regex if you need structured dimensions |
| 17 | `ConformanceWageDecision` with null `WageRate`/`HourlyFringe` | pending-approval stubs — filter `WageRate ne null` for approved |
| 18 | `RefOjtProgram.Name` | inconsistent case — don't match case-sensitively in UIs |
| 19 | `OjtProgramEnrollment` vs `RefEmployeeApprenticeship` | overlapping worker records; no FK between them |
| 20 | Reviewer IDs on reviews | strings (`"3331"`, `"332"`) — opaque codes, no resolver exposed |
| 21 | DBE commitment `Appr` vs `Curr` | the approved tree is frozen at award; mid-contract revisions live on the Curr tree. Dashboards almost always want Curr. |
| 22 | Fringe payment type `"Cash"` vs `"Plan"` | determines whether CertPayrollBenefitPrograms must exist for the payroll to be complete |

---

### 9. Deferred / unverified

Items the vendor reference guide hints at or that appear in the EDMX but could not be confirmed in awdemo:

- **DBE substitutions.** No `DbeSubstitutions` or similar entity set responds. The schema supports mid-contract revisions through the `Curr` tree but doesn't model the substitution request/approval workflow as a distinct entity. If prod has this, it may ride on a different entity (`ChangeOrder` with a DBE-coded line? or a vendor-specific attachment?) — needs confirmation.
- **DBE shortfall report.** No `DbeShortfall` entity. End-of-contract shortfall is derived from `TotalCommitAmt - sum(SubcontractorPayments[DbeFirm=true].PaidAmount)` client-side.
- **SBP (state small business program) commitment tracking.** 500 on awdemo — exists in schema (`ContractSBPGoal`, `ContractSBPCommitment`, etc.) but unavailable here. Prod should carry it.
- **Field interview reports (full chain).** `FieldInterviewJobClassification` is populated with real data (welding at $19.50, flagging at $13.00) but the parent `FieldInterviewEmployee` and `FieldInterview` sets weren't probed. Likely a full workforce-sampling chain exists.
- **Workflow phases.** `WorkflowPhase` ID 3 appears to mean "agency accepted" for payrolls, 36 for "accepted" on sub-payments — the actual phase catalog needs separate inspection (`WorkflowPhases` set).
- **E-signature trail.** `SignedById`, `ProxySubmitterId`, `InternallySignedBy` fields appear across payroll and payment entities — the full digital-signature chain (certificates, hashes) isn't exposed through these entity sets.
- **Attachments to compliance records.** Compliance records don't appear in the main `Attachment` set via `CustomBusinessEntityId`. If prod attaches scanned payrolls/review letters to records, the join pattern needs separate discovery (CustomBusinessEntity Name = "CertifiedPayroll" or similar).
- **Payroll resubmission workflow full picture.** `ModificationNumber` increments are visible but the state machine (what triggers a resubmission, how exceptions carry across versions) is procedural, not in the schema.
- **DBE credit vs paid-amount discrepancy.** `TotalDbeCreditAmount` and `TotalPaidToDateDbeCreditAmount` exist on `SubcontractorPayment` but are null in every awdemo row probed — the credit-vs-cash math (60% supplier credit, trucker caps) can't be verified here.

---

**End of document.** Companion doc: [`ams-business-flows-2026-09-30.md`](ams-business-flows-2026-09-30.md). File-level data verified against `ams-lab/awdemo` on 2026-09-30.
