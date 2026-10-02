# What the portal assumes about an invoice — and what it does not know

*Companion to `engineering-db-map.md` (the table-by-table survey) and to the business-logic
reference in the app (`/docs/logic`, §3, §5, §6, §10, §15.1, §16). Written 2026-09-05.*

## The picture

One consultant sends one BF-2 package that bills one agreement. Where it lands depends on the
unit in the BF-2 `UNIT` box (`Invoices.REC_ORG` in Engineering) — one of many:

```
                             one BF-2 package · one consultant · one agreement
                                                     │
                                                     ▼
                              ┌────────────────────────────────────────────┐
                              │ received by the unit in the BF-2 UNIT box  │
                              └──────────────────────┬─────────────────────┘
                                                     │
     ┌───────┬───────┬───────┬───────┬───────┬───────┴───────┬───────┬───────┬───────┬───────┬───────┐
     ▼       ▼       ▼       ▼       ▼       ▼       ▼       ▼       ▼       ▼       ▼       ▼       ▼
  Eng. HQ   D1      D2      D3      D4      D5      D6      D7      D8      D9      D10   Traffic Environ
   0060    0160    0260    0360    0460    0579    0679    0760    0858    0979    1060    0085    0061
     ▲
     │  the only receiving unit the portal has real data for (3 687 of 5 998 invoices);
        the districts also process invoices the tracker never sees ("D4 TO PROCESS", "NO PAG#")

 divisions with their own copy of the agreement/invoice tracker (not imported):
 Contract Administration (CA) · Materials (M) · Traffic Operations (TO) · IT · Performance
 Management (PM) · Operations (OD) · Planning (P) · Right of Way (RW) · Technical Support (TS)
```

Whoever receives it, every invoice type needs the same four things before money moves:

```
 ┌─ what every invoice needs ──────────────────────────────────────────────────────────────┐
 │                                                                                         │
 │  ① AGREEMENT / INVOICE LOGIC     ② LINE ITEMS                 ③ ACCOUNT CODES           │
 │  which agreement (the name       labor hours × rate against   fund · unit · activity ·  │
 │  printed on the BF-2), ceiling   the rate schedule; sub-       sub-activity · program · │
 │  and sequence, work period,      consultant lump sums;         phase · task order ·     │
 │  supplementals, procurement      direct expenses reviewed      project key — one set    │
 │  document (PAG), vendor number   at cost; a project on         per allocation           │
 │                                  every line                                             │
 │         │                                │                            │                 │
 │         └────────────────────────────────┴────────────────────────────┘                 │
 │                                          ▼                                              │
 │  ④ OASIS LINE(S) KEYED                                                                  │
 │  one payment document (PRC by default; GAX still open) — vendor code, address code,     │
 │  procurement document, service dates, total — with one accounting line per allocation   │
 │                                                                                         │
 └─────────────────────────────────────────────────────────────────────────────────────────┘

   portal today:  ① checked   ② extracted & priced   ③ drafted, mostly blank   ④ keying assist
   the unknowns in §3 and §4 sit almost entirely in ③ — who fills the codes, and from what
```

## 1. The one assumption everything hangs on

**An invoice is one BF-2 package, and it always bills exactly one agreement.**

Everything else follows from that:

- **One vendor.** The BF-2's consultant is the agreement's prime. Subconsultant work arrives as
  line items *inside* the prime's invoice (`Invoices_Subcon` in Engineering; the `subconsultant`
  category in the portal), never as an invoice of its own.
- **One name.** The BF-2 `PROJECT NAME` line is the agreement's name. That is the check that
  blocks (`AGREEMENT_NAME_MISMATCH`): the agreement the reviewer picks must be the one printed
  on the BF-2. A differently printed agreement *ID* is only a warning.
- **One ceiling.** Previous / current / total-to-date on the BF-2 are running totals against that
  agreement's max payable (original amount + supplementals). Sequence numbers, the ceiling check,
  billed-to-date and "remaining after this" are all computed per agreement.
- **One project set.** The money on an invoice is split only across the agreement's own
  projects. A single-project agreement stamps its project onto the invoice and every line item;
  a master agreement requires an allocation across its projects that ties to the current amount.
- **One procurement document.** The agreement carries the OASIS document (`PAG23*266`); the
  invoice's `wv_apo` is that number.
- **Corrections replace, they do not merge.** A corrected package is a new invoice that
  supersedes the old one on the same agreement.

Not supported, by design: a package containing several BF-2s, an invoice that charges two
agreements, or a subconsultant invoicing WVDOT directly.

## 2. The Engineering joins the import relies on

The Engineering tracker makes the same one-agreement assumption, which is why the import works
at all. What the importer (`backend/app/seed/engineering/mapping.py`) actually joins:

| Join | Key | How firm |
|---|---|---|
| invoice → agreement | `Invoices.MasterAgreementIndex` = `Agreements.SQL_id` | declared FK; 9 416 of 9 416 resolve |
| invoice → vendor | `Invoices.consultantID` = `Consultants.sqlid` | declared FK; equals the agreement's prime on 9 412 of 9 416 — the four exceptions are treated as the agreement's prime |
| invoice → project | `Invoices.ProjectID` = `PTSData.PROJ_KEY` | declared FK; equals the agreement's `ProjectID` on every row |
| agreement → vendor / project | `Agreements.Consultant_id`, `Agreements.ProjectID` | FK / 1 330 of 1 344 match `PTSData` |
| supplement → agreement | `Supplements.MasterAgreementIndex` | declared FK, 551 of 551 |
| sub line → invoice | `Invoices_Subcon.invoice_id`, `.subconsultant_id` | declared FKs |
| agreement name | TheHub `Project.ProjectName` via `ProjectID` | inferred; falls back to `PTSData.PROJ_DESC` |

Rules the importer *invents* because the source does not state them (each is written into the
row's notes so it is auditable in the UI):

- **Agreement identity** is `AgreementNumberGenerated` (`2011000857-275-A` = project + consultant
  number). 194 rows repeat a number; they are merged into one agreement, keeping the row with
  the executed date / amount.
- **Master vs single-project** is not a column. An agreement is `master` when its invoices carry
  more than one distinct `ProjectID`, else `single_project`. This is the weakest inference in
  the chain: a master agreement whose invoices so far all hit one project reads as single.
- **Status** comes from a decision table over the lifecycle dates (`Invoice_Rec_Date` →
  `Date_Sent_for_Review` → `Date_back_from_Review` → `Invoice_Sub_to_OASIS` → `Paid_Date`).
  Voided invoices become `withdrawn`; legacy invoices marked SCANNED, or on a closed agreement
  with no activity for 90 days, are *assumed paid* and the assumption is recorded on the row.
- **Vendor numbers** are placeholders `ENG<consultant number>`; Engineering has no OASIS vendor
  number, address id or tax id. The `VENDOR_NUMBER_PLACEHOLDER` note flags them.
- **Org unit** is the modal `REC_ORG` code across the agreement's invoices (`0060` = Engineering
  Division HQ, `1060` = District 10, `0460` = District 4 …), else the responsible group /
  prequal type.
- **OASIS document** is parsed from `OASIS_APO_Number`, whose spellings vary (`PAG23*17` vs
  `PAG23*017`, `PAG 25*171`).

Not imported: the REMIS authorization (`FE2441G` — the key OASIS reconciliation would need),
`AgreementNumberKeyed`, fee type, prequal / selection type, the sub share of the ceiling
(`Agreements_Subcon`), target dates, evaluations, PAG closure, and the eight other division
copies of the tracker (Contract Administration, Materials, Traffic Operations, IT …).

## 3. What I do not know about construction

CEI (construction engineering & inspection) is where the one-agreement assumption is thinnest.
A statewide CEI master agreement is one agreement, but the work is done on many **construction
contracts**, and the vendor's split sheet is organised by those contracts, not by our projects.

- **The split-sheet "Contract ID" is a construction contract number**, not an agreement or a
  project. Older ones are seven digits (year + sequence) with a re-let suffix — `1322506R2` is
  the second re-let of the Kerens–US 219 Connector contract (Corridor H Section 1, Kokosing,
  District 8, awarded 11/25/2015); `1605051RFP` is a design-build contract. Since roughly 2020
  the contract number *is* the 10-digit project key (`2017001491`), which is the only reason most
  of them validate against TheHub. The mapping lives in `Data-Warehouse.[HWS.PTS.REP].CONT_NO` and
  `AWP_ChangeOrders.ContractID`; the portal does not read either yet.
- I do not know whether CEI cost must be reported **per construction contract** for federal
  reimbursement (participating vs non-participating), or whether the project-level allocation the
  portal records is enough for OASIS and FHWA.
- I do not know how a **re-let** (`R2`) or a **change order / supplemental agreement** on the
  construction contract affects the consultant's billing — whether it is the same project for our
  purposes or a new one.
- I do not know whether the **Contract Administration** copy of the tracker (130 agreements,
  68 invoices, no supplements after 2023) is where district CEI invoices live, or an abandoned
  fork. Its consultant list drifts from Engineering's.
- Two databases that almost certainly answer these questions are visible but locked to our
  login: `Agreement-Invoice-Tracking` and `OasisFinance` (also `BFCheckLog`, `DistrictProjectTracking`).
- `AWP_HUBDates` (5 490 contracts) does not contain every contract the change-order table does,
  so I do not know which AASHTOWare table is authoritative for contract dates.

## 4. What I do not know about the districts

- **Who reviews and approves.** The approval chains in the portal ("three eyes" per district)
  are seeded placeholders. Engineering's `Procurement_Responsible_Group` shows the shape
  (DD-C 789 agreements, then Other, OS, DS-N, DD-1 … DD-9) but not the people, and
  `Invoices.Project_Manager` / `Returned_From_Review_by` name individuals without roles.
- **Which invoices never reach Engineering.** 40 invoice rows and 12 agreement rows carry notes
  like `D4 TO PROCESS`, `NO PAG#`, `DO NOT PROCESS INV'S` in place of an OASIS number: the
  districts process those themselves, somewhere I cannot see. Only 2 300 of 6 000 receiving-org
  codes are district codes; I do not know whether that is the true district share or just what
  HQ happened to log.
- **The BF-2 UNIT codes.** `REC_ORG` gives real codes for HQ and the districts that appear, but
  the portal's seeded `bf2_unit_code` values for the rest were guesses and have not been
  confirmed against a district-keyed BF-2.
- **Whether districts key OASIS themselves** (and if so from which document type — GAX vs PRC is
  still open), or forward everything to Engineering / Auditing.
- **District contract administration data** lives in `DistrictProjectTracking` and the
  Contract Administration tracker copy, neither of which the portal reads.

## 5. Where to change things if an assumption breaks

| If it turns out that… | Touch |
|---|---|
| an invoice can bill two agreements | the data model (`invoices.agreement_id`), `AGREEMENT_NAME_MISMATCH`, allocations, the vendor portal scope — a deep change |
| construction contract ids must be first-class | `projects.contract_id` (already exists, empty) + a `CONT_NO` → project-key map loaded with the Hub mirror (`services/hub.py`) |
| master/single must not be inferred from invoices | `mapping.py::build` (`kind = "master" if …`) — ask Engineering for a column or a rule |
| a district's chain is known | `routing_rules` / `routing_rule_steps` via Config, no code |
| the real BF-2 unit codes are confirmed | `org_units.bf2_unit_code` via Config; `mapping.py::normalize_rec_org` |
