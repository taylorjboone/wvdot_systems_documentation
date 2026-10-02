# Consultant Invoice Portal — Business Logic Reference

This is the verbose reference for *how the Consultant Invoice Portal behaves*: the
data model, the intake and extraction pipeline, the financial checks, the workflow
state machine, routing, the OASIS keying-assist screen, and the report math. It is
written from the code that ships, not from the requirements wish-list — where the
two differ, this document describes what the app actually does today and flags the
gap. Every rule below names the module that implements it so it can be verified.

Companion documents: the **Changelog** (Docs → Changelog) records what changed and
when; `requirements-document.md`, `open-questions.md`, and `action-items.md` in the
project folder record what the August 11, 2026 kickoff asked for.

---

## Contents

- [1. Domain Vocabulary](#1-domain-vocabulary)
- [2. Data Model](#2-data-model)
- [3. Intake & Upload](#3-intake-upload)
- [4. BF-2 Extraction](#4-bf-2-extraction)
- [5. The Contract-ID Cross-Check](#5-the-contract-id-cross-check)
- [6. Workflow State Machine](#6-workflow-state-machine)
- [7. Routing & Approval Chains](#7-routing-approval-chains)
- [8. Financial Checks Engine](#8-financial-checks-engine)
- [9. Agreement Money Math](#9-agreement-money-math)
- [10. Allocations & Multi-Project Splits](#10-allocations-multi-project-splits)
- [11. OASIS Keying Assist](#11-oasis-keying-assist)
- [12. Reports](#12-reports)
- [13. The Invoice Page & Intake Wizard (frontend rules)](#13-the-invoice-page-intake-wizard-frontend-rules)
- [14. Authentication, Storage & Configuration](#14-authentication-storage-configuration)
  - [14.1 Sign-in methods](#141-sign-in-methods)
  - [14.2 WVDOT SSO (OIDC relying party)](#142-wvdot-sso-oidc-relying-party)
- [15. Demo Seed](#15-demo-seed)
- [16. Provisional Assumptions & Open Questions](#16-provisional-assumptions-open-questions)
- [17. Versioning & Changelog](#17-versioning-changelog)
- [18. Conventions to Remember](#18-conventions-to-remember)

---

## 1. Domain Vocabulary

**Invoice.** One consultant billing package: a WVDOT **FORM BF-2 Consultant
Voucher** cover sheet on top and backup documentation behind it (the vendor's own
cover invoice, task-level labor / other-direct-cost / subconsultant detail,
timesheets, vehicle logs, subconsultant invoices). The portal stores the PDF once
and models the BF-2 as columns on the `invoices` row.

**BF-2.** The agency cover sheet, revised 10/2023. It carries the vendor block,
`VENDOR'S INVOICE #`, `DATE OF INVOICE`, `DATES OF AGREEMENT AND SUPPLEMENTS`, the
**MAXIMUM AMOUNT PAYABLE** block (original agreement, supplementals, total), the
work period, `% FUNDS EXPENDED`, state/federal project, program, phase, project
name, a 4 × 3 amounts grid (INVOICE AMOUNT, LESS RETAINED OR ADJUSTMENT, PLUS
RETAINED OR ADJUSTMENT, BALANCE DUE × PREVIOUS TOTAL, AMOUNT CURRENT, AMOUNT TOTAL
TO DATE), `AMOUNT DUE CONSULTANT`, three stamp boxes, and comments. The grey
**WVDOT USE** block (LOG IN, PREVIOUS IN, APO, UNIT, FUNCTION, ACT + N or P,
SEQUENCE #) is filled by staff, not the vendor. The BF-2 does **not** carry the
agreement ID (stored as `contract_id`, labelled **Agreement ID** in the interface) or the OASIS document ID.

**Agreement.** The procurement instrument the invoice draws against. `kind` is
`master` (a letter agreement / ARQS-turned-contract spanning several projects, paid
through release orders) or `single_project` (a purchase order). Its `contract_id`
is the string printed on the vendor's cover page (for the sample,
`WVDOT AGT 08-22-2025`). Its **name** is exactly what the vendor prints on the BF-2
PROJECT NAME line (`Hardy Co 23/12 Waites Run Road`, `2025 D2 Area Eng and Cnst Sppt`):
it is shown in the agreements table, read from the executed PDF when an agreement is
created (§3.1), and used to link an invoice whose agreement id matched nothing (§5). An
agreement may exist in the portal before its OASIS
procurement document (`oasis_doc_type` / `oasis_doc_id`) has been created — that
is the "invoice arrived before the procurement document" case.

**Term.** The contract period: `term_start` (which may precede the execution date —
the Baker statewide master was executed Feb 13 2023 for a term from Jan 1 2023) to
`end_date`, extended by each supplemental's `term_end`. The **effective term end** is
the latest of those dates (`app/services/rates.py::effective_term_end`).

**Supplemental.** An amendment to an agreement. It may raise the ceiling (`amount`),
extend the term (`term_end`), revise the per-assignment / annual caps, and set new
rates for later periods (rows in `agreement_rates`); a rate- or term-only
supplemental carries `amount = 0.00`. Each carries its own `oasis_entered_at`; until
that is set the extra ceiling is *not* usable for payment (see
`SUPPLEMENTAL_NOT_IN_OASIS`).

**Rate schedule.** The consultant billing rates attached to an agreement: one row per
firm (the prime *and* each subconsultant) × classification × effective period, with a
regular, premium (overtime), regular-shift and premium-shift rate (hourly) or a per-day
rate (vehicle). On a master agreement that lists several companies, each company's rate
table is that firm's own schedule — those are the rates for that subconsultant, keyed to
the row's firm (§3.1). Read from the attached PDF and staged for review, or typed by hand
(§3.1, §9.3). **Provisional** — see §16 and open question #26.

**Max payable / ceiling.** `original_amount + Σ supplementals`.

**Billed to date.** The sum of `invoice_amount_current` over the agreement's
invoices in a *billed* status: `approved`, `keyed`, or `paid`. Received, logged,
routed, in-review, on-hold, rejected, and withdrawn invoices do not count.

**Allocation.** A split of one invoice's current amount across the projects of a
master agreement. Allocations must tie to the BF-2 current amount to the cent.

**Org unit.** A district (`D01`–`D10`) or central-office division (Engineering,
Traffic, Materials Control Soils & Testing, Contract Administration, Operations,
Right-of-Way, Environmental, Construction). Each has a provisional
`bf2_unit_code` and a responsible party. Routing rules hang off org units.

**Invoice type.** A provisional taxonomy (`CEI`, `ENG`, `MAT`, `TRF`, `ROW`, `ENV`,
`OTHER`) that, together with the org unit, selects the routing rule. The kickoff
explicitly deferred the real taxonomy.

**Check.** One result from the financial checks engine: a code, a severity
(`block`, `warn`, `info`), a message, and details. Blocking checks stop approval.

**Event.** One row in the invoice ledger (`invoice_events`): what happened, from
and to which status, who did it, and when. Every stage timestamp and every aging
report is computed from this ledger.

**OASIS entry.** The keying-assist record for an invoice: the header fields and
accounting lines a finance user copies into the OASIS payment document. The
payment document type defaults to `PRC` and is provisional.

---

## 2. Data Model

Backend models live in `backend/app/models/`. Money columns are `Numeric(14,2)`
and are handled as `Decimal` end to end; they serialize to JSON as numbers with two
decimals. Enumerations are Python `StrEnum`s stored as plain `VARCHAR` (validated
in pydantic, not Postgres). Every table has integer primary keys and
`created_at` / `updated_at` timestamps.

How the tables hang together (`──►` = foreign key, `1:*` = one-to-many, `?` = nullable):

```ascii
 REFERENCE & ACCOUNTS
 ┌───────────────┐  vendor_id? (SET NULL)  ┌─────────────────────┐  vendor_id (CASCADE)  ┌─────────────────────┐
 │ users         │────────────────────────►│ vendors             │◄──────────────────────│ vendor_name_history │
 │ role: admin   │                         │ oasis_vendor_number │                       │ former_name         │
 │ or vendor     │                         │ compliance dates    │                       └─────────────────────┘
 └───────────────┘                         └─────────────────────┘
 ┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌────────────────────────────┐
 │ org_units     │   │ invoice_types │   │ default_rates │   │ hub_projects  │   │ projects                   │
 │ D01… / divs   │   │ CEI, …        │   │ WVDOT fallback│   │ TheHub mirror │   │ number · name · contract_id│
 └───────────────┘   └───────────────┘   └───────────────┘   └───────────────┘   │ org_unit_id? ► org_units   │
                                                                                 └────────────────────────────┘
 AGREEMENT  (one contract / PO; a letter agreement points at its master — see the diagram below)
 vendors       ◄─┐ vendor_id
 org_units     ◄─┼─ org_unit_id     ┌──────────────────────┐ 1:*  ┌── agreement_supplementals   number · amount · term_end · caps
 invoice_types ◄─┘ invoice_type_id? │ agreements           │──────┼── agreement_documents ─supplemental_id?─► supplementals
 agreements ◄── parent_agreement_id?│ contract_id (Agr. ID)│      ├── agreement_rates     ─supplemental_id?─► supplementals
   (self: master → assignment)      │ division · name      │      │        └──────────────document_id?─► agreement_documents
                                    │ kind · status        │      ├── agreement_rate_aliases
                                    │ original_amount      │      └── agreement_projects  ─*:*─► projects
                                    │ term_start · end_date│
                                    └──────────────────────┘

 INVOICE  (one BF-2 package)
 vendors       ◄─┐ vendor_id?
 agreements    ◄─┼─ agreement_id?   ┌──────────────────────┐ 1:*  ┌── invoice_documents      the package PDF
 org_units     ◄─┼─ org_unit_id?    │ invoices             │──────┼── invoice_line_items     labor / ODC / sub rows
 invoice_types ◄─┼─ invoice_type_id?│ status · BF-2 fields │      ├── invoice_vehicle_usage  Vehicle Usage Report rows
 users         ◄─┘ created_by_id?   │ WVDOT USE block      │      ├── invoice_allocations   ─project_id─► projects
                                    │ checks · estimate    │      ├── invoice_events         the ledger (actor_id? ► users)
 invoices ◄── supersedes_invoice_id?│ stage stamps         │      ├── approval_steps         the chain (acted_by_id? ► users)
             (corrected package)    └──────────────────────┘      └── oasis_entries  1:1     keying assist (keyed_by_id? ► users)

 ROUTING TEMPLATES
 routing_rules ─org_unit_id?─► org_units          routing_rules ─1:*─► routing_rule_steps   order · role_label · assignee · can_delegate
               ─invoice_type_id?─► invoice_types  resolved when an invoice routes and copied into its approval_steps (§7)
```

The **master → letter-agreement (assignment)** structure. Engineering uses it for statewide
CEI / QAM masters (the imported Hico Bridge chain below is an **Engineering** example), and WVDOT's
Contract Administration division (WVDOT code **CF**) uses it too — the CF lane is **provisional**
(see §16 and the *CA agreements analysis* doc). A master holds rates/term/caps and is never billed;
each letter agreement is its own money-bearing agreement drawn off it (`agreements.parent_agreement_id`):

```ascii
 MASTER  (kind=master, division=EN)                     one master ── many assignments
 ┌──────────────────────────────────────────┐          via agreements.parent_agreement_id
 │ firm × service line (CEI / QAM / …)        │
 │ RATE SCHEDULE (prime + subconsultants)     │───┐ parent_agreement_id
 │ TERM · per_assignment_cap · annual_cap     │   │
 │ NO project · NO invoices · $0/"DUMMY" total│   │
 └────────────────────────────────────────────┘   │
        ▲  assignment inherits the master's         │
        │  rates in the estimate (refresh_estimate) │
        │                    ┌──────────────────────┼──────────────────────┐
        │                    ▼                       ▼                      ▼
 ┌──────────────────────────────────┐  ┌───────────────────────────┐   ┌─────────┐
 │ LETTER AGREEMENT / ASSIGNMENT #1  │  │ ASSIGNMENT #2             │   │  …      │
 │ kind=letter_agreement, division=EN│  │ own ceiling =            │   └─────────┘
 │ own term · agreement_projects ─►  │  │   original + Σ supplements │
 │ its one (or few) projects         │  │ funded by the project's    │
 └───────────────┬───────────────────┘  │   OASIS authorization (PAG)│
                 │                        └───────────────────────────┘
                 │ invoices (BF-2) bill the ASSIGNMENT — never the master
                 ▼
 ┌───────────────────────────────────┐   ceiling checks (CEILING_EXCEEDED/_NEAR) run on the
 │ invoices → agreement_id (this      │   assignment; a master is skipped (§8, §9). Provisional
 │ assignment); allocate like a       │   PER_ASSIGNMENT_CAP_EXCEEDED warns when an assignment's
 │ single_project agreement (§10)     │   ceiling tops the master's per-assignment cap.
 └───────────────────────────────────┘
```

`division` (`EN` / `CF`; NULL = EN) keeps the two lanes apart so a CF number can reuse an EN
contract number — uniqueness is `(division, contract_id)` (§16). Engineering agreements are
`master` / `single_project` and leave `parent_agreement_id` null.

| Table | Purpose | Notable columns |
|---|---|---|
| `users` | Portal accounts: WVDOT staff (`role = admin`) and vendor accounts (`role = vendor`, bound to one vendor through `vendor_id`, FK SET NULL) | `email` (unique), `password_hash` (bcrypt), `role`, `is_active`, `vendor_id` |
| `org_units` | Districts and divisions | `code`, `name`, `kind`, `bf2_unit_code` (provisional), `responsible_party_name/email`, `is_active` |
| `vendors` | Consultant firms | `oasis_vendor_number` (unique), `remit_address_id`, address, `workers_comp_expires`, `insurance_expires`, `is_active`, `is_subconsultant_only` |
| `vendor_name_history` | Prior names after acquisitions/renames | `former_name`, `changed_on` |
| `agreements` | Contracts / POs | `contract_id` (the **Agreement ID** as the UI labels it), `contract_id_normalized`, `division` (`EN` / `CA`; NULL = EN — see §16), `parent_agreement_id?` (a CA `letter_agreement`'s master — see §16), `vendor_id`, `org_unit_id`, `invoice_type_id`, `kind`, `oasis_doc_type`, `oasis_doc_id`, `original_amount`, `agreement_date`, `term_start`, `end_date` (original term end), `per_assignment_cap`, `annual_cap`, `name` (the BF-2 PROJECT NAME line), `state/federal_project_number`, `program`, `phase`, `status`. **Uniqueness is composite on `(COALESCE(division,'EN'), contract_id_normalized)`** (migration `0010`), not a global `contract_id`, because CA and EN number agreements identically |
| `agreement_supplementals` | Amendments (ceiling, term, caps, rates) | `number`, `amount` (may be 0), `supplemental_date`, `oasis_entered_at`, `term_end`, `per_assignment_cap`, `annual_cap` |
| `agreement_documents` | PDFs attached to an agreement + the state of their rate-schedule read | `supplemental_id?`, `kind` (`agreement`, `supplemental`, `other`), `storage_path`, `size_bytes`, `page_count`, `sha256`, `review_status` (`pending` → `running` → `ready` / `no_rates` / `failed`; `imported` / `dismissed`; `skipped` without an API key), `extraction_json`, `extracted_at`, `reviewed_at` |
| `agreement_rates` | The rate schedule | `supplemental_id?`, `supplemental_number` (0 = original), `document_id?`, `firm_name`, `firm_key`, `classification`, `classification_normalized`, `effective_from`, `effective_to?`, `seq`, `regular_rate`, `premium_rate?`, `regular_shift_rate?`, `premium_shift_rate?` (`Numeric(12,4)`), `unit` (`hour`, `day`), `source` (`extracted`, `manual`), `source_page`, `confidence`; unique on (agreement, supplemental number, firm, classification, effective_from, seq) |
| `agreement_rate_aliases` | Sticky "what the invoice calls it → schedule row" mappings | `firm_key` (`''` = any firm), `alias`, `alias_normalized`, `target_firm_key`, `target_classification_normalized` |
| `default_rates` | WVDOT fallback rates (provisional) | `classification`, `classification_normalized`, `effective_from`, `effective_to?`, the four rate columns, `unit`, `note`, `is_provisional` |
| `projects`, `agreement_projects` | Projects an agreement bills (one for `single_project` or a `letter_agreement`, several for `master`) | `number`, `name`, `contract_id` (as vendors print it on split sheets), `county`, `org_unit_id` |
| `hub_projects` | Read-only mirror of TheHub's project master, refreshed by the Engineering importer (§15.1); powers the "In TheHub" chip (§10) | `project_key` (10-digit WVDOH key, PK), `name`, `state_project_number`, `district_code`, `county`, `status`, `awp_contract_number` (the AASHTOWare construction contract under this project number, resolved by the importer's Hub SQL against `AWP_HUBDates` / `AWP_Dates` / `AWP_ChangeOrders`), `synced_at` |
| `invoice_types` | Provisional taxonomy | `code`, `name`, `is_provisional`, `sort_order` |
| `invoices` | One row per BF-2 package | every BF-2 field (`vendor_name_bf2` … `amount_due_consultant`), the WVDOT USE block (`wv_log_in`, `wv_previous_in`, `wv_apo`, `wv_unit`, `wv_function`, `wv_act_n_or_p`, `wv_sequence_no`), `contract_id_entered` / `contract_id_extracted` / `contract_id_match`, `status`, `held_from_status`, `supersedes_invoice_id`, extraction (`extraction_json`, `extraction_method`, `extraction_confidence`), `summary_text`, estimate cache (`estimate_json`, `estimated_total`, §9.3), checks cache (`checks_json`, `checks_run_at`, `checks_block_count`, `checks_warn_count`), `oasis_document_id`, `keyed_at`, `paid_at`, `warrant_number`, `rejection_reason`, `issue_note`, stage stamps (`received_at`, `logged_at`, `routed_at`, `review_started_at`, `approved_at`, `rejected_at`, `withdrawn_at`, `status_changed_at`), `submitted_at` (vendor-portal submission, §6) |
| `invoice_documents` | Stored PDFs | `kind` (`package`), `storage_path`, `size_bytes`, `page_count`, `sha256` |
| `invoice_line_items` | Labor / direct-expense (`odc`) / subconsultant rows read from the backup | `category`, `task_code`, `task_name`, `party_name`, `employee_id` (for a direct expense: the printed reference code), `classification` (for a direct expense: its kind — Lodging, Meals, Vehicle, …), `firm_name`, `rate_kind` (`regular`, `premium`, `regular_shift`, `premium_shift`), `project_number` (the program the line charges — stamped from a single allocation, or traced from the split sheet when unambiguous, §10), `work_date`, `hours`, `quantity`, `rate`, `amount`, `source_page`, `source` |
| `invoice_vehicle_usage` | Vehicle Usage Report rows read from the backup (§4.4) | `seq`, `vehicle_id`, `date_out`, `date_in`, `project_number`, `task_code`, `driver`, `odometer_out/in`, `category`, `quantity`, `bill_rate`, `bill_amount`, `source_page`, `source` |
| `invoice_allocations` | Project splits | `project_id`, `amount`, `task_order` (no longer captured in the UI, §11), `note` |
| `invoice_events` | The ledger | `action`, `from_status`, `to_status`, `actor_id`, `actor_label`, `note`, `data`, `created_at` |
| `routing_rules`, `routing_rule_steps` | Approval chain templates | `org_unit_id?`, `invoice_type_id?`, `min_amount?`, `priority`, `is_active`; steps: `order`, `role_label`, `assignee_name/email`, `can_delegate` |
| `approval_steps` | The chain generated for one invoice | `order`, `role_label`, `assignee_name`, `status` (`pending`, `active`, `approved`, `rejected`, `skipped`), `acted_at`, `note` |
| `oasis_entries` | One keying-assist record per invoice | `doc_type` (default `PRC`), `doc_id`, `vendor_code`, `address_code`, `vendor_invoice_number/date`, `invoice_received_date`, `service_from/to`, `procurement_doc_type/id`, `total_amount`, `accounting_lines` (JSON), `status` (`draft`, `ready`, `keyed`), `keyed_at` |

Statuses (`app/models/enums.py`):

```
received → logged → routed → in_review → approved → keyed → paid
side states: rejected · on_hold · withdrawn
OPEN     = received, logged, routed, in_review, approved, keyed, on_hold
TERMINAL = paid, rejected, withdrawn
BILLED   = approved, keyed, paid           (count toward billed-to-date)
```

---

## 3. Intake & Upload

Implemented in `app/services/invoices.py::create_from_upload` and
`app/services/storage.py`; exposed as `POST /api/invoices/upload` (multipart).

1. The upload is spooled and hashed (SHA-256) while it streams. A file over
   **50 MB** (`PORTAL_MAX_UPLOAD_MB`) is refused with `413 payload_too_large`. A
   file whose first bytes are not `%PDF-` is refused with `415 not_a_pdf`.
2. **Duplicate guard.** If any stored document already has the same SHA-256, the
   upload is refused with `409 duplicate_document` and the existing invoice id,
   unless `force=true` is passed. The wizard surfaces this as "Already uploaded —
   upload anyway?" so a genuine resubmission can proceed.
3. An `invoices` row is created in status `received` with `received_at = now`,
   `extraction_method = "none"`, and the optional `contract_id_entered`,
   `supersedes_invoice_id` (a resubmission after rejection points at the invoice
   it replaces), and `notes`.
4. The PDF is written to `backend/storage/invoices/{invoice_id}/{uuid}.pdf`
   (`PORTAL_STORAGE_DIR`), and an `invoice_documents` row records the original
   filename, size, page count (via pypdf), and hash.
5. An `uploaded` event is written, extraction runs (§4), a deterministic summary is
   generated (§4.6), and the checks engine runs (§8).

The contract ID is **never** pre-filled from the extraction — even when the
extraction found one and linked an agreement, `contract_id_entered` stays blank
until a person types it (§5).

The stored PDF is streamed back by `GET /api/invoices/{id}/documents/{doc_id}/file`.
That route accepts the bearer token either in the `Authorization` header or as a
`?token=` query parameter, because browser-native fetches (the PDF viewer
`<iframe>`, download links) cannot set headers.

**Vendor uploads (§13.6).** When a vendor account uploads, `create_from_upload(vendor_id=…)` pins
the invoice to that vendor and `link_references(pin_vendor=True)` refuses to link an agreement of
another vendor (the package's own vendor number or name is *not* trusted over the account).
`force`, `force_claude` and `notes` are ignored for vendors. The vendor then submits with
`POST /invoices/{id}/submit` (§6); nothing else changes in the pipeline.

### 3.1 Agreement documents & rate extraction

Implemented in `app/services/agreement_documents.py`, `app/services/llm/rate_schedule.py`
and `app/api/routes/agreement_rates.py`. An agreement can carry any number of PDFs — the
executed agreement, each supplemental (linked to its `agreement_supplementals` row), and
other papers — stored under `backend/storage/agreements/{agreement_id}/{uuid}.pdf` with the
same size / `%PDF-` / SHA-256 guards as invoice uploads (the duplicate guard is scoped to
the agreement). `GET /api/agreements/{id}/documents/{doc_id}/file` streams it back with the
same `?token=` rule. An agreement can be created and used without any PDF.

0. **Pre-fill the New-agreement form** (`POST /api/agreements/analyze`, stateless). When a
   PDF is dropped on the create dialog the **whole document** is sent to Claude Sonnet
   (`PORTAL_CLAUDE_MODEL_EXTRACT`; one call up to 40 pages, else 20-page chunks merged
   first-non-empty) with the `AgreementHeaderOut` schema, because term dates, caps and the
   execution date can sit deep in the recitals or an attachment. It returns every form field
   it found — agreement ID, consultant, district or division, title and
   project description, project numbers, state / federal project numbers, program, phase,
   execution date (used as the agreement date), term start / end, a fixed total when one is
   printed (statewide masters usually cap per assignment and per year instead), caps, vehicle
   daily rate, OASIS document type / id — plus `kind` (master / single project / letter agreement / supplemental).
   The server also offers a best-effort **vendor** match (normalized name or a former name,
   `agreement_documents.match_vendor`) and **org-unit** match ("District 5" → `D05`, or a
   division whose name the text contains) purely to pre-select the dropdowns; nothing is
   validated against them. The dialog fills only empty fields, tags each with "from PDF",
   offers the annual cap as the original amount when no total is printed, and warns when the
   PDF reads as a supplemental. Without an API key the PDF is simply attached after saving.
1. **Upload** (`POST /api/agreements/{id}/documents`, multipart `file`, `kind`,
   `supplemental_id?`; also attached from the create-agreement and add-supplemental dialogs).
   The row starts as `pending`, or `skipped` when no API key is configured.
2. **Background read.** A FastAPI background task renders nothing itself: the PDF is split
   into ≤6-page chunks (pypdf) and each chunk is sent to Claude
   (`PORTAL_CLAUDE_MODEL_RATES`, default `claude-opus-5`, effort `high`, structured output
   `AgreementDocOut`) as a `document` block, because the rate pages in these packages are
   **scanned images with no text layer**. Chunks run in parallel; rows are unioned and the
   first non-empty header fact wins (`term_start`, `term_end`, caps, vehicle daily rate,
   supplemental number, document kind, and for supplementals the **money added**
   (`supplemental_amount`) and the **new total compensation** (`total_compensation`) — the
   prompt tells the model these two facts and the new term end are what WVDOT checks first
   and to return `''` rather than guess). A printed YEAR becomes `effective_from = Jan 1`,
   `effective_to = Dec 31`; greyed cells become `NULL`; duplicate printed rows are kept.
   The result is stored as `extraction_json` and the status becomes `ready`, `no_rates`
   (a supplemental that only extends the term is normal) or `failed`. Cost is roughly
   $0.40–0.80 for a 22-page supplemental. The frontend polls the document list every 3 s
   while a read is in flight.
3. **Staged review** (`GET …/documents/{doc_id}/review`). Nothing read from a PDF is used
   until a person imports it. Each extracted row is diffed against the agreement's current
   schedule: `new`, `same` (identical row already on file), `changed` (same firm /
   classification / period with different rates — importing adds the row alongside, and it
   supersedes when it comes from a later supplemental), `duplicate` (the same key printed
   twice in the PDF — kept as `seq` 2, 3, …), `incomplete` (no year). Contract facts are
   proposed with the current value beside them; a fact is pre-selected to apply only when
   the agreement (or the supplemental the PDF belongs to) has nothing recorded yet — except
   the two supplemental checks below, which follow the PDF whenever it disagrees with what
   was typed.

   **Supplemental checks** (`term_check`, `money_check`; `DocumentReview.term` / `.money`,
   present only for a PDF of kind `supplemental`). Both are measured against the agreement
   *before* this supplemental — the agreement's own values plus every **other**
   supplemental — so a re-review after import still reads "extends":
   - **Term** — the PDF's `term_end` against the term end in force: `extends` (with the
     number of days), `shortens`, `unchanged`, or `not_stated`. `recorded_end` is the
     `term_end` typed on the linked supplemental row and `matches_recorded` says whether it
     agrees; `apply_field = "term_end"` (pre-selected) whenever the PDF and the record
     differ. A shorter term is never pre-selected and carries a warning note.
   - **Ceiling** — the money the supplemental adds against `max_payable` before it:
     `increase` is `supplemental_amount` when printed, else `total_compensation −
     current_max`; `proposed_max = current_max + increase`; status `increases`,
     `decreases`, `unchanged` or `not_stated`. When both money facts are printed and
     `current_max + supplemental_amount ≠ total_compensation` the note asks the reviewer to
     check the supplementals recorded so far (a missing or mistyped earlier supplemental
     shows up here). `recorded_amount` is the linked row's `amount`; `apply_field =
     "amount"` (pre-selected) when they differ.
   - A supplemental PDF **not linked** to a supplemental row still gets both checks, but
     nothing is proposed onto the agreement itself (its `end_date`, caps) and the note says
     to link or add the supplemental first. A master PDF never carries these checks.
   The review dialog shows the two checks first ("What this supplemental changes") with
   before → after, the delta, what is recorded, and an Apply switch; the remaining facts
   follow as "Other contract facts".
4. **Import** (`POST …/import`, `{rate_indexes, apply_fields}`) creates `agreement_rates`
   rows (`source = extracted`, `document_id`, `source_page`, `confidence`), applies the
   accepted facts (`term_start` / `end_date` on the agreement, `term_end`, `amount` and caps
   on the supplemental — applying `amount` moves max payable, so the agreement's open
   invoices are re-checked for `AGREEMENT_CEILING` — and a vehicle daily rate as a
   `unit = day` rate row), marks the document
   `imported`, bumps `agreement.updated_at`, and re-runs estimate + checks for the
   agreement's open invoices. `…/dismiss`, `…/reextract` and `DELETE` complete the life
   cycle; deleting a document keeps the rates imported from it.

Rates can also be typed by hand (`POST/PATCH/DELETE /api/agreements/{id}/rates`,
`source = manual`); an identical row is refused with `409 duplicate_rate`. Every rate,
alias or import change bumps `agreement.updated_at` and re-checks the agreement's open
invoices (`POST /api/agreements/{id}/recheck` does the same on demand).

**Master agreements that list several companies' rates.** A master (and sometimes a
supplemental) rate schedule prints a **separate rate table per company** — the prime and
one or more subconsultants named on the agreement. Each table is *that company's own
schedule*: those are the rates for that subconsultant, not shared across the team. Every
row is therefore stored against its firm (`agreement_rates.firm_name` / `firm_key`), and a
line billed by a subconsultant is priced against **that subconsultant's** rows, never the
prime's (§9.3 *Firm*). A firm-specific rate (and a firm-specific alias) always beats a
firm-agnostic one; when the same classification appears under several firms the estimate
does not guess across them. Import keeps each company's rows under its own firm, so the
schedule for a multi-firm master reads as one block of rows per company.

---

## 4. BF-2 Extraction

Implemented in `app/services/extraction.py` (text layer) and
`app/services/claude_client.py` (fallback). Every extracted value is an
`ExtractedField { value, confidence, source_page, method }`; the whole result is
stored on the invoice as `extraction_json` and shown in the wizard as per-field
tints and `p.N · 0.92` badges.

### 4.1 Page classification

`pdfplumber` reads every page with `extract_text(layout=True)`. A page is a *text
page* when it has more than 80 characters of text. The **BF-2 page** is the first
page matching `FORM BF-2` or `CONSULTANT VOUCHER` (case-insensitive). Pages after
the BF-2 up to the first `Vehicle Usage Report`, `Daily Work Record`, or
`Time and Miles` heading are treated as task-detail pages for line items.

The sample package (Michael Baker Invoice 1285907) has text on pages 1–5; pages
6–10 (the Quinn Consulting subconsultant invoice) are scanned images with no text
layer, so they are counted in `page_count` but not in `text_pages`.

### 4.2 Required fields and confidence

Seven fields are **required** for the text path to count as a success:

```
vendor_name_bf2, invoice_number, invoice_date, period_start, period_end,
invoice_amount_current, max_payable_bf2
```

Confidence rules:

| Source | Confidence |
|---|---|
| Label-anchored regex on the BF-2 page | 0.95 |
| Regex value corroborated by the vendor cover page (invoice number equal, or invoice amount equal) | 0.99 |
| Value supplied by the Claude fallback | min(model confidence, 0.90) |
| Field not found | 0.00 |

`extraction_confidence` on the invoice is the mean confidence over the seven
required fields. `extraction_method` is `text` when the BF-2 page was found and at
least one required field parsed, `claude` when the fallback supplied most of the
required fields, `manual` when a person typed the values, and `none` otherwise.

### 4.3 BF-2 field parsing

Regexes are anchored on the printed labels; columns on the same line are separated
by three or more spaces in the layout text. In brief:

- `NAME` / `ADDRESS` lines are cut before the WVDOT USE labels that share the row.
- `VENDOR NUMBER` = 6–12 digits or an OASIS `VS…` id (internal spaces removed:
  `VS000 004 6933` → `VS0000046933`); `REMIT ADDRESS ID` = 4–12 alphanumerics.
- `VENDOR'S INVOICE #`, `DATE OF INVOICE`.
- `ORIGINAL AGREEMENT`, `SUPPLEMENTALS`, and `TOTAL` are read **only inside** the
  block between `MAXIMUM AMOUNT PAYABLE` and `PROJECT / INVOICE INFORMATION` so the
  many other "TOTAL" labels on the page cannot be mistaken for the ceiling.
- The agreement date and any supplement dates are read from the block between
  `DATES OF AGREEMENT AND SUPPLEMENTS` and `PROJECT / INVOICE INFORMATION`.
- `INVOICING FOR WORK PERIOD <from> TO <to>`, `% FUNDS EXPENDED: <n>%`,
  `STATE PROJECT: … PROGRAM: …`, `FEDERAL PROJECT: … PHASE: …`, `PROJECT NAME:`.
- The amounts grid rows (`INVOICE AMOUNT`, `LESS RETAINED OR ADJUSTMENT`,
  `PLUS RETAINED OR ADJUSTMENT`, `BALANCE DUE`) are parsed by finding every money
  token on the line; when a row has fewer than three values (blank cells), the
  words are bucketed by the x-spans of the column headers (`PREVIOUS TOTAL`,
  `AMOUNT CURRENT`, `AMOUNT TOTAL TO DATE`) so a blank does not shift the others.
- `AMOUNT DUE CONSULTANT`.
- The WVDOT USE block is read from a cropped right-column bounding box.
- Money accepts `$` followed by any whitespace, thousands separators, integers without
  cents (`0`), dash placeholders (as zero), and parentheses for negatives; dates
  accept `m/d/Y`, `m/d/y`, `March 31, 2026`, and `24-Mar-26`. `N/A` and blanks
  become `null`.

### 4.4 Cover page and line items

Text pages before and after the BF-2 are scanned for the vendor's cover invoice or
transmittal letter (EXP's letter precedes the BF-2; Michael Baker's cover follows it).
`Agreement Number:` becomes `contract_id_extracted` (the BF-2 itself has no
contract ID); `Project Number:`, `Invoice No`, `Invoice Amount`, and `Invoice
Date` corroborate the BF-2 values.

Task-detail pages are parsed into line items: template junk (`#ROWDELETE`,
`#TSKDEL`, `#STOPTRAVERSE`, `#comm`, `#ARIAL18`, inline `#nf4`) is stripped;
`Task NN name` headers set the task; `Labor`, `Other Direct Costs`, and
`Subcontractors` section headers set the category; labor rows are
`Name, First - #id  date  Type  hours  $rate  $amount`, ODC rows carry a quantity
and rate, subcontractor rows an amount plus description continuation lines. The
sample yields 5 labor rows ($3,124.50, 15.00 h), 1 ODC row ($48.00), and 1
subconsultant row ($1,113.20) = $4,285.70, which ties to the BF-2.

Michael Baker's **"Lower Task" layout** (the Corridor H QAM invoices) is read too: task headers
without the word Task (`1.1 Project Manager`, `2.7 Level II Inspector`, `3 ODCs` —
`BARE_TASK_HEADER`, a one- or two-digit code so street numbers never qualify), an
`Employee No.` column caption, a bare classification line under it, and labor rows that carry
only the employee number (`#813463  6/5/2026  Regular 2.00 $269.37 $538.74` →
`LABOR_ROW_NO_NAME`; `party_name` becomes `Empl. # 813463`, matching how the same invoices name
the person on their ODC rows). A percentage add-on at the foot of an ODC section (`10% Markup
$115.35`, handling or administrative fees — `ODC_MARKUP_ROW`) is its own `odc` line with kind
`Markup`, so the section total ties.

Four more layouts met in the CEI mailbox are read by the same pass (`tests/test_extraction.py`
has one case each):

- **Baker rows with the employee number underneath** — `Bailey, Gregory -  6/2/2026 Regular …`
  followed by a bare `#819003` line (`LABOR_ROW` makes the number after the dash optional;
  `EMP_ID_LINE` back-fills it onto the row just read). An ODC row whose long name leaves a single
  space before the date (`Thorne, Zyndall 3/16/2026 Fleet (day)…`) is read too; `ODC_ROW` refuses a
  description that is a labor time type so a mis-sectioned labor row never becomes an expense.
- **Overprinted dates** — a date printed twice on top of itself reaches the text layer with every
  character doubled (`43//1233//22002266`); `DOUBLED_DATE` keeps the first print (`4/13/2026`).
  A stray leading apostrophe on a task header or fee row (`'1 Project Management`) is dropped.
- **Cost-plus Lower Task invoices** (Corridor H design reviews) — under each classification the
  labor detail is followed by `Overhead 155.3730% $4,286.87` and `Fee 13.0000% $358.67` lines
  (template tags `#OH%` / `#FEE%`); each becomes an `other` line with the percentage as its rate
  (`ADDON_ROW`). When a task prints no employee rows at all, its `Total Regular 7.00 $325.29` line
  stands in as the labor row (`LABOR_TYPE_TOTAL`, only while the task has no detail rows). A `FEE`
  section then carries credits in parentheses — `Effective Labor Rate Variance to Billing Rate
  Credit ($278.58)` → an `other` line of −278.58, kind `Fee adjustment` (`FEE_ROW`); the section
  closes at its `Total For FEE:` line because the next page re-itemises the same credit.
- **AMT's `Billing - Labor Detail`** — rows `6/23/2026 101864 Burris, David  Contract Manager  1.00
  201.02 201.02 [OT]` grouped under the construction contract they charge (`I-81 Signing Project
  (Contract ID: 2022020003)`, `Pallet Factory Bridge (CID 202333005)`). `DATED_LABOR_ROW` reads the
  classification from the row itself (hours may print as `.50`; an `OT` suffix makes the row
  Overtime) and `PROJECT_GROUP_LINE` stamps the contract id into the line's **`project_number`**
  and, when the page names no task, the project name into `task_name`. `project_number` on an
  extracted line survives into `invoice_line_items.project_number` and is the line's program (§10)
  when no split sheet says otherwise.

A blank BF-2 box runs into the next printed label on the same line (`NAME   APO`, `VENDOR'S
INVOICE #  MAXIMUM AMOUNT PAYABLE`); `BF2_LABEL_JUNK` blanks such captures on every BF-2 field, and
`(cid:87)`-style glyph tokens from fonts without a text map are stripped from values.

**Per-day rows first, subtotals as the fallback.** The goal is always the per-day row (person,
date, hours, rate, amount). When a package has no usable per-day rows — hours-only timesheets,
scanned backup, or rows that do not reconcile — the next best thing is the vendor's **subtotal
table**: one row per unique item (a person or classification with its total hours, rate and
amount; an expense type with units, unit price and amount) that ties to the BF-2. The vendor
layouts below (`app/services/extraction_layouts.py`) read that subtotal level and *claim* their
pages so the generic pass cannot read the same money twice; `_parse_line_items::_select_level`
then keeps the per-day rows when they reconcile to the BF-2 current amount (else the stated total,
else the summary's own total) and uses the subtotal rows only when the per-day rows are missing
or do not — warning `line_items_from_subtotals`. Every row carries its `level` (`detail` or
`subtotal`), and the per-day rows that lose to a subtotal table (or to the model's set) are **kept**
on the result as `superseded_rows` — supporting rows the reviewer can still see, never summed. WRA's
parser reconciles internally (employee
rows per project when they tie to the letter, else the letter's line) and returns final rows:

- **GPI** (Greenman-Pedersen): `LABOR` / `EXPENSES` / `Total Amount Due for GPI` pages, one per
  project headed `<project> CID# <key>` — labor rows `Name  Title  $rate  hours  $amount` under
  `Staff - Regular Hours` / `Staff - Overtime Hours`, expense rows `Daily Use  D Swaim  $48.00 19
  $912.00` (person optional). The overall page whose total equals the sum of the project pages is
  dropped; rows carry the project key as `project_number`.
- **CDM Smith / Mead & Hunt** attachments: `LABOR COSTS` tables with straight-time and overtime
  columns — by employee for CDM (`Moss, Thomas  Level III, #2503  95.06 143.00 $13,593.58 $115.77
  7.50 $868.28`, employee number from the title; `Hall,Kip` and `Farren William` name forms) and
  by classification for Mead & Hunt (`Level II Inspection/Technician $76.98 177.50 $13,663.95
  $95.41 23.00 $2,194.43`); each non-zero column is a labor row. `DIRECT COSTS` tables become
  `odc` rows (`Mileage (Auto Logs) 28.00 $48.000 $1,344.00`, `Lodging $1,864.50`, a continuation
  line with no description). A `CID 2023410012` in the attachment title is the rows'
  `project_number`. Amounts the text layer split (`$ 1 4,461.86`, `$ 3 5 , 5 3 3 . 0 6`) are
  re-joined first (`normalize.py::fix_split_money`, also applied to every generic backup line).
- **WRA** (Whitman, Requardt): the letter's per-project `Payroll: 59 Total Hours $6,559.73` and
  `Direct Costs: $480.00` lines, plus each other firm's `This Invoice` amount as a
  `subconsultant` row. For every project whose FIELD STAFF LABOR COST CALCULATION rows
  (`Dague, William 8  Level V Inspector / Supervisor ST $136.63 $1,093.04`, OT lines beneath) sum
  to the letter's payroll, the employee rows replace the summary row; the same rule applies to
  DIRECT COSTS CALCULATIONS vehicle rows. A mismatch keeps the letter's amount and warns
  (`wra_labor_detail_mismatch:<project>`).
- **CEC**'s own invoice page (fallback only): `Task 0003 Level III` / `Professional Fees`, then
  hours, rate and amount per person per `CID #: 2013000001` (the row's `project_number`) or per
  `State Project #: U325-79-131.72 00`, and `Veh Mileage $48/day` day rows; its `Total` /
  `Amount Due This Invoice` is the reconciliation target when the BF-2 is blank.

Two more detail layouts are read by the generic pass: **CEC**'s Deltek "Unbilled Detail" (`B
10/20/2025 35  002435  Wheeling, Joseph  4.00 234.82 939.28` under `Task Number: 0001 …` and
`Labor:` / `Expenses:` / `Units:`; the task name is the classification, and the free-text lines
under each row are never read as one — `CEC_LABOR_ROW`, `CEC_EXPENSE_ROW`, `CEC_UNIT_ROW`), and
**EXP**'s "Billing Backup" (`Phase 1300 Level IV Technician` heads rows `140 - Collins, James
7/14/2026 [Ovt] 10.00 192.34 1,923.40` — `PHASE_HEADER`, `EXP_LABOR_ROW`; the phase name is the
classification — and `Units` rows `Faisal Khan July 2026 27.0 Days @ 48.00 1,296.00`, read from
the detail pages only). Reading stops after the page that prints `Total This Project` /
`Total this Report`: what follows is receipts (`END_OF_BACKUP`).

**Direct expenses** (category `odc`, billed at cost). Besides the quantity × rate ODC rows,
the parser reads the expense-report layouts vendors attach under an `Expenses:`, `Direct
Expenses` or `Reimbursable Expenses` header (`EXPENSE_ROW_DATED`: `7/2/2026 000000018873
Lovejoy Lodging 07/01 (1 Night) … $124.3  124.30`; `EXPENSE_ROW_CODED`: `EX 000001006756
7/2/2026 Peyton, Victoria / Lodging 6/29-7/02  369.60`, also `JE …` rows). Each row becomes a
line item with `party_name` = the person (the text before the ` / `, or before the expense
keyword), `classification` = the **kind of expense** (`expense_kind`: Lodging, Meals, Vehicle,
Airfare, Parking & tolls, Fuel, Supplies, Other — first keyword wins), `employee_id` = the
printed reference / expense code, `quantity` = the nights / days / meals stated in the text,
`rate` = the unit price **only when printed** (`$124.3`, `@ $48.00 per day`; never derived),
`work_date`, `amount`, `description`. The Claude line-item pass is told the same mapping.
These rows are **reviewed, not validated**: every direct expense passes through the estimate at
its billed amount (§9.3) except a vehicle line that states days and a rate when the agreement
sets a day rate, and `DIRECT_EXPENSES_REVIEW` (§8) puts their total and by-kind breakdown in
front of the reviewer. The Line items tab lists them in their own **Direct expenses** section
(date, person, kind, description, ref, qty, unit — `≈` when implied from amount ÷ quantity —
amount, page) with subtotals by kind and a "Review only · not rate-validated" chip, keeping the
task grid for labor and subconsultant rows (`features/invoices/directExpenses.ts`).

Two more backup sheets are read from every page after the BF-2 (`extraction.py::
_parse_vehicle_usage`, `_parse_project_splits`):

- **Vehicle Usage Report** pages become `vehicle_usage` rows (vehicle id, date out / in,
  project #, task, driver, odometer out / in, category, quantity, bill rate, bill amount, page)
  and are stored in `invoice_vehicle_usage`; the report's printed total (or the row sum) is
  `vehicle_usage_total`. The report backs up the per-day vehicle ODC lines ("Fleet (day)"), so
  `VEHICLE_USAGE_SUM` (§8) ties the two and the Line items tab shows the rows with miles driven.
- **Project Split between Assignments** sheets — the CEI standardized invoice's per-project
  breakdown, often several pages with the header only on the first and "Split Total" on the last
  — become `project_splits`: one group per `Contract ID` line **in whatever format the vendor
  prints** (`2018001357`, `1729998`, `1729999R2`, `20245001R1`, `202530048` …), the project
  name on the next line, the rows charged to it (employee, date, Regular / Fleet …, quantity,
  rate, amount), and its "Project Total". These contract ids identify the **construction
  projects billed, not the agreement**: they are reported as `project_cid` candidates (§5),
  never chosen as the extracted contract id, and offered as allocations (§10). `Split Total`
  is `project_split_total`; `PROJECT_SPLIT_SUM` (§8) ties it to the BF-2 current amount.

Inside a `Labor` block a bare line with no money, date or `#` template marker (for the
sample, `Construction Manager`) is the **classification** the following employee rows are
billed under; it resets at the next task or section header and is stored on each row.
`rate_kind` is derived from the row's time type (`app/services/normalize.py::
rate_kind_from_description`): Regular / Straight → `regular`; Overtime / OT / Premium /
Double / Holiday → `premium`; a Shift or Night mention selects the shift-differential
column. The Sonnet line-item pass reports `classification` and `firm` for the same fields
(a firm only when the page is a subconsultant's own backup). The estimate (§9.3) uses these
three columns to match each row to the agreement's rate schedule.

### 4.5 Model-assisted analysis (Claude Sonnet)

Implemented in `app/services/llm/` and run for **every upload** when a key is configured (`PORTAL_ANTHROPIC_API_KEY` or `ANTHROPIC_API_KEY`) and
`PORTAL_LLM_ANALYSIS_ENABLED` is true. It is the semantic layer; the regex path stays the
judge for the standardized BF-2 grid. Three structured-output calls
(`client.messages.parse` with pydantic schemas, adaptive thinking, `effort` low for
classification and medium for extraction) on `PORTAL_CLAUDE_MODEL_CLASSIFY` /
`PORTAL_CLAUDE_MODEL_EXTRACT` (default `claude-sonnet-5`), text pages only, capped at
`PORTAL_LLM_MAX_PAGES` (60):

1. **Page classifier** → `page_labels[{page, kind, confidence, title}]` with kinds
   `transmittal_letter, bf2, vendor_invoice_summary, labor_detail, direct_costs,
   subconsultant_invoice, timesheet, vehicle_log, project_breakdown, other, scanned`
   (pages under 80 characters are `scanned` without a call). Heuristic labels are produced
   even without a key so the PDF tab always has named page chips.
2. **Identifier extraction** → `contract_id_candidates[{value, normalized, kind, source_page,
   evidence, confidence, method}]` with kinds `project_key, agreement_string, purchase_order,
   task_order, vendor_project_no, other`, plus vendor number, remit id, dates, amounts to fill
   gaps, and an `invoice_type_guess {code, confidence, rationale}` over the provisional
   taxonomy.
3. **Line-item normalization** of labor / direct-cost / subconsultant pages into the
   canonical categories, used only when the regex path found no line items; the
   `LINE_ITEMS_SUM` check still decides whether they tie.

Deterministic candidates exist regardless of the model: a printed `Agreement Number`, any
10-digit WVDOH project key printed as "CID" on any page (reported as `project_key`, never the agreement) (including pages before the BF-2), and a 10-digit value in the
BF-2 PROGRAM box (confidence 0.6). Merge rules: model values fill **only** fields the regex
left empty, carry `method: claude` and a confidence capped at 0.90 (0.85 for gap fills);
`contract_id_extracted` is the printed agreement number when present, else the best
candidate ranked agreement_string > purchase_order > task_order (never a `project_key` — the 10-digit WVDOH project key printed as "CID" — nor a vendor's own
project number). Usage is recorded in `llm {model, calls, input_tokens, output_tokens,
pages_classified, warnings}`; a refusal or SDK error becomes a warning, never an HTTP error.

**Timing.** The upload request returns as soon as the deterministic pass is done (a few
seconds); the model pass runs as a FastAPI background task (`invoices.run_llm_analysis`) with
`extraction.llm_pending = true` in the meantime. The wizard polls the invoice every 3 s while
pending and shows "Claude is reading the package…"; when the task finishes it fills only fields
the user has not set, re-links the agreement, refreshes the checks and writes an `extracted`
event. Each call is bounded to 90 s (line-item chunks of 3 pages: 180 s) and is sent once more
after a timeout, dropped connection, overload / 5xx answer, or a reply that was not valid JSON
for its schema (`llm/client.py::TRANSIENT_ERROR`); a 400 or refusal fails at once. Line-item and
classifier chunks run concurrently, so a 37-page package completes in roughly a minute or two.
The seed runs with the model off. Model-facing schemas use plain required strings ('' = not
printed) because the structured-output grammar caps union-typed properties at 16.

**When the model itemizes.** The Sonnet pass normalizes line items when the text pass found
none — and also when the text rows do **not tie** to the BF-2 current amount by more than
`TEXT_TIE_TOLERANCE` ($0.05 — a few cents is the vendor's own footing, not a missed row; a 2¢
difference had cost a 9-call itemization that changed nothing). In that case both sets exist and the one whose total is closer to the
BF-2 amount wins (`apply_llm_analysis`); rows that already tie are never replaced, and with no
BF-2 amount on file the text rows stand. `line_items_total_mismatch` in the warnings is what
this rule reacts to.

**Receipts are not backup.** Hotel folios, per-diem / travel logs ("Daily Total"), fuel and parking
slips back up amounts already listed on a direct-costs page; the classifier labels them `receipt`
(prompt rule plus the heuristic `Daily Total | Folio | Guest Name | Check-in | Room Rate |
Receipt | Gallons`) and `LINE_ITEM_PAGE_KINDS` excludes them, so the same cost is not itemized a
second time. **A page that came back empty is asked again.** After the chunked pass, any backup
page with no rows that prints its own `Total … $X` (`llm/line_items.py::printed_total`) is sent to
the model on its own (up to 8 pages; warning `line_items_reasked:<pages>`) — a 40-hour WRA
timesheet had been dropped from the middle of a 3-page chunk while its neighbours were itemized.
**Subtotal tables when the per-day rows fail.** If the model's detail rows are missing or do not
reconcile to the BF-2 current amount, the `vendor_invoice_summary` / `project_breakdown` pages are
itemized in *summary mode* (`SUMMARY_PREAMBLE`: one row per person / classification / expense type
with its total quantity, rate and amount) and used when they reconcile (`SUMMARY_PAGE_KINDS`,
warning `line_items_from_subtotals`). The whole-PDF fallback is told the same order of preference.

### 4.6 Whole-PDF fallback

The whole-PDF fallback (`PORTAL_CLAUDE_MODEL`, default `claude-opus-5`) runs only when no
BF-2 page was found, the BF-2 page has fewer than 200 characters of text (a scan), or the
caller passed `force_claude`. It is a silent no-op — recorded as the
warning `claude_unavailable` — when no `ANTHROPIC_API_KEY` /
`PORTAL_ANTHROPIC_API_KEY` is configured.

When it runs, the PDF is sent whole if it is ≤ 25 MB and ≤ 100 pages, otherwise
only its first three pages. The call is
`client.messages.parse(model=PORTAL_CLAUDE_MODEL (default claude-opus-5),
max_tokens=16000, …, output_format=Bf2Extraction)` with the PDF as a base64
`document` content block; a `stop_reason == "refusal"` returns nothing. Claude's
values fill **only** fields the text pass left empty, capped at 0.90 confidence,
and SDK errors surface as extraction warnings, never as HTTP 500s. The schema sent is not
`Bf2Extraction` itself but its **wire variant** (`schemas/extraction.py::bf2_wire_model`, built
with `create_model`): every nullable field becomes a required plain `str` (`''` when not printed)
or `int` (`0` when unknown), so the schema has zero optional and zero union-typed properties —
the structured-output API rejects more than 24 optional or 16 nullable properties, and the
fallback failed with exactly those errors on every scanned package. `bf2_from_wire` turns the
answer back into the nullable internal model and drops rows without an amount
(`test_claude_schema_has_no_optional_fields`). The prompt asks for **current-period rows only** —
take the CURRENT column of a PREVIOUS / CURRENT / TO DATE table, never a subtotal, total or
balance line, read a cost once even when the package repeats it, and return no rows rather than a
guess. `_merge_claude` then drops any row whose amount equals one of the package totals (the
model reading a total line) and, when the text pass already found rows, keeps whichever set is
closer to the BF-2 current amount — the same rule as the Sonnet pass.

A second whole-PDF read for line items (`claude_client.extract_lines_with_claude`,
`LINES_SYSTEM_PROMPT`): the model reads the package end to end and returns the cover fields plus
every billed row as printed — no subtotal / total / to-date lines, the current-period column only,
vehicle usage as one row per entry, rows that must sum to the BF-2 current amount, `notes` when a gap
remains — with one retry at double the output room when a reply is cut off mid-JSON. On 35 real CEI
invoices it tied the BF-2 within a nickel on 34 (Opus) and on 20 of 20 with Sonnet at `xhigh`, at
roughly 20k–45k input tokens per invoice.

This read is now **wired into the upload path** (`apply_llm_analysis`, `extraction.py`): when
`PORTAL_LINE_ITEMS_WHOLE_PDF` is on (default) and a key is configured, it **owns line items** and the
page-chunked Sonnet pass is asked only for identifiers, page labels and the invoice-type guess. To
keep the cost off clean invoices it runs **only when the text pass did not reconcile to the BF-2**
(same trigger the chunked pass used); when the text rows already tie, no model line-item read runs.
Its rows are merged by `_merge_claude` (drop total lines, keep the set closer to the BF-2 current
amount), and the model is `PORTAL_CLAUDE_MODEL_LINE_ITEMS` (default `claude-sonnet-5`) at
`PORTAL_CLAUDE_LINE_ITEMS_EFFORT` (default `xhigh`). It runs **first**, and is capped at
`PORTAL_CLAUDE_LINE_ITEMS_TIMEOUT` seconds (default 240) so a slow / dropped connection on a big
package **fails over to the chunked pass** rather than blocking the background extraction — the upload
never loses its line items. Set `PORTAL_LINE_ITEMS_WHOLE_PDF=false` to skip it entirely. The
`pull_lines run --claude pdf` CLI still exposes the same read for database-free CSV runs.

### 4.7 Invoice summary

`summarize_invoice()` builds the "here's the contents" brief deterministically:
vendor, invoice number and date, work period, agreement and project, max payable,
billed to date and % expended, the labor / direct-cost / subconsultant totals with
counts, the task breakdown, and any project split. It intentionally does not
include check counts (the checks panel is the live source). `POST
/api/invoices/{id}/summarize {enrich: true}` may ask Claude to polish the text;
this never happens on the upload path.

---

## 5. The Contract-ID Cross-Check

Requirement FR-7 says the contract ID is the *only* hand-typed field and the
system cross-checks it against the value read from the PDF.

- `contract_id_extracted` is the cover page's printed `Agreement Number:` when there is one,
  else the best-ranked candidate from §4.5 (an agreement string or PO number, for example).
- `contract_id_entered` is set in wizard step 2 from an **agreement autocomplete** (`GET
  /agreements?q=` matches the agreement id, agreement name and vendor; picking an option fills
  the id and links the agreement and vendor), or typed as printed when the agreement is not on
  file yet (minimum 3 characters after trimming). It is never pre-filled from the extraction, so
  the cross-check below stays independent. Typing past the picked agreement unlinks it; an exact
  match re-links.
- `compute_contract_match()` normalizes both sides (uppercase, alphanumerics only)
  and sets `contract_id_match` to `true` when the typed ID equals the extracted ID **or any
  non-vendor candidate** (in which case that candidate becomes `contract_id_extracted`),
  `false` on a mismatch, or `null` when nothing was extracted.
- A mismatch is the **warning** `CONTRACT_ID_MISMATCH` (the agreement-ID string is advisory —
  agreements are printed many ways); the wizard offers
  "Use extracted" or "Keep mine and explain…" (stored as
  `contract_id_override_reason`). No extracted value produces the informational
  `CONTRACT_ID_UNVERIFIED`.
- Whenever `contract_id_entered`, `vendor_id`, `agreement_id`, or `wv_unit`
  changes, the invoice is re-linked: `find_agreement()` matches the normalized
  entered ID, the extracted ID and the agreement-id candidates against
  `agreements.contract_id_normalized` only — a 10-digit CID is a WVDOH **project key** and
  never identifies an agreement (`agreements.cid` was dropped in migration 0006);
  a matched agreement supplies the vendor, org unit, and invoice type when those
  are still blank. `CONTRACT_ID_NOT_ON_AGREEMENT` warns when the typed ID does
  not belong to the linked agreement.

- **Link by name.** When no candidate matches an agreement, `find_agreement_by_name` links the
  vendor's single agreement whose `name` equals the BF-2 PROJECT NAME line (casefolded,
  punctuation collapsed). **The validation that matters:** once linked, the agreement's `name`
  must equal the BF-2 PROJECT NAME — `AGREEMENT_NAME_MISMATCH` **blocks** `log` and `submit`
  otherwise, because a different name means the wrong agreement was picked. The wizard's
  agreement search starts from the PROJECT NAME and auto-picks the agreement named on the BF-2.
- **Link by project key.** When id and name both miss, `find_agreement_by_project`
  (`link_references`) resolves the agreement the printed **project key** bills against, scoped to
  the invoice's vendor: a `letter_agreement` whose id is `‹projectkey›-…` or whose linked
  project matches one of the keys the invoice prints (`project_key`/`project_cid` candidates, the
  split-sheet contract ids, and the BF-2 program — `project_key_candidates`). It links only on a
  single unambiguous hit, so the user still confirms and `AGREEMENT_NAME_MISMATCH` still guards a
  wrong auto-resolve. This is what lets a CEI invoice that prints only its 10-digit CID pre-fill
  its assignment instead of forcing a manual search (business-logic §16).
- **Vendor match.** `find_vendor` matches the BF-2 vendor by OASIS number (leading zeros ignored),
  then an exact case-insensitive name, then a **single normalized-name** match that tolerates
  punctuation ("TRC Engineers, Inc" ≡ "TRC Engineers, Inc."). Resolving the vendor is what lets the
  vendor-scoped project-key agreement resolution above fire.
- **Vendor back-fill.** After the vendor is resolved, `backfill_vendor_from_bf2` (`link_references`)
  copies the BF-2 vendor block onto the Vendor record **when — and only when — the record's fields
  are blank**: `vendor_number_bf2` → `oasis_vendor_number` (skipped if another vendor already owns
  that unique number), `remit_address_id_bf2` → `remit_address_id`, and `vendor_address_bf2` parsed
  (`street` / `city, ST ZIP`) → `address_line1/2`, `city`, `state`, `postal_code`. It never
  overwrites a value already on file. This keeps OASIS keying (which already falls back to the BF-2
  values, §11) and the vendor record complete for imported vendors that arrived without an OASIS
  number or address.
- Contract ids printed per project on a split sheet are a different thing from the agreement
  id: they carry kind `project_cid`, are excluded from `best_contract_id` (like the vendor's own
  project numbers), and appear in the wizard under "Projects billed on the split sheet". Without
  this rule a D2-style package would extract one of its sixteen project ids as *the* contract id
  and warn on `CONTRACT_ID_MISMATCH` as soon as the real agreement id is typed.

---

## 6. Workflow State Machine

Implemented in `app/services/workflow.py`. The table below is the literal
`TRANSITIONS` map; an action not in the table for the current status is refused
with `409 illegal_transition` and the list of allowed actions.

| From | Action | To | Endpoint |
|---|---|---|---|
| `received` | log | `logged` | `POST /api/invoices/{id}/log` |
| `logged` | route | `routed` | `POST …/route` |
| `routed` | start_review | `in_review` | `POST …/start-review` |
| `in_review` | approve | `approved` (stays `in_review` while steps remain) | `POST …/approve`, `POST …/steps/{step}/act` |
| `logged`, `routed`, `in_review`, `approved` | reject | `rejected` | `POST …/reject` |
| `approved` | key | `keyed` | `POST …/key` |
| `keyed` | mark_paid | `paid` | `POST …/mark-paid` |
| any open status except `on_hold` | flag_issue | `on_hold` | `POST …/flag-issue` |
| `on_hold` | resolve_issue | the status it was held from | `POST …/resolve-issue` |
| `received`, `logged`, `routed`, `in_review` | withdraw | `withdrawn` | `POST …/withdraw` |

Every transition sets `status`, `status_changed_at`, the matching stage stamp
(`logged_at`, `routed_at`, `review_started_at`, `approved_at`, `keyed_at`,
`paid_at`, `rejected_at`, `withdrawn_at`), appends an `invoice_events` row with
`from_status` / `to_status` / actor / note, and re-runs the checks engine.

Per-action validation:

- **log** — requires `vendor_id`, `agreement_id`, `invoice_number`,
  `invoice_date`, `period_start`, `period_end`, `invoice_amount_current`, and
  `contract_id_entered` (else `422 missing_fields` listing them); recomputes the
  contract match; blocks (`409 blocking_checks`) on `PERIOD_INVALID`,
  `DUPLICATE_INVOICE_NUMBER`, or `AGREEMENT_NAME_MISMATCH` only.
- **route** — body `{org_unit_id?, invoice_type_id?, routing_rule_id?,
  responsible_party?}`; requires an org unit. For a **master agreement with more
  than one project**, allocations must exist and tie (`ALLOCATION_*` checks block
  routing). Resolves the routing rule (§7), deletes any prior approval steps, and
  creates a fresh chain with the first step `active`.
- **start_review** — requires at least one approval step (`422 no_steps`).
- **approve / act on a step** — `steps/{id}/act {decision: approve|skip, note?,
  delegated_to?}` acts on the *active* step only and activates the next pending
  step. When no pending steps remain (or `POST /approve` is used with none
  pending), approval is finalized: **any blocking check refuses it**
  (`409 blocking_checks`). Finalizing creates the OASIS entry draft.
- **reject** — a reason is required (`422 reason_required`). Rejection from
  `approved` models the downstream kick-back by accounts payable or the auditor.
  Payment is all-or-nothing; there is no partial approval.
- **flag_issue / resolve_issue** — a note is required to flag; `held_from_status`
  remembers where to return.
- **key** — body `{oasis_document_id, keyed_at?}`; the document ID is required.
  A `draft` OASIS entry is promoted to `ready` automatically if its accounting lines
  tie to the invoice total, otherwise `409 oasis_entry_not_ready`. Sets
  `oasis_document_id`, `keyed_at`, and marks the entry `keyed`.
- **mark_paid** — body `{warrant_number, paid_at}`; both required, and `paid_at`
  may not precede `keyed_at` (`422 paid_before_keyed`). The event is stamped with
  `paid_at` so aging reflects the real payment date.
- **withdraw** — no validation beyond the transition table.

**Editability by status** (`editable_fields`): `received`, `logged`, `routed`,
`in_review`, `on_hold` → `all` BF-2 fields; `approved` → only the WVDOT USE block
and comments (`PATCH` with anything else is refused); `keyed`, `paid`, `rejected`,
`withdrawn` → read-only. A `PATCH` that touches `contract_id_entered`, `vendor_id`,
`agreement_id`, or `wv_unit` re-links the agreement (§5); every `PATCH` writes a
`fields_updated` event with the diff and re-runs the checks.

**Resubmission.** A rejected invoice is not edited back to life; the vendor's
corrected package is uploaded as a new invoice with `supersedes_invoice_id`
pointing at the rejected one, so history is preserved.

---

**`submit` — the one ledger action that is not a transition.** A vendor (or staff) calls
`POST /invoices/{id}/submit` (`services/workflow.py::submit_invoice`) on an invoice still in
`received`. It requires the same fields as `log` (vendor, agreement, invoice number and date,
period, current amount, typed contract id), an agreement that belongs to the invoice's vendor
(422 `agreement_vendor_mismatch`), and none of the `SUBMIT_BLOCKERS` — the checks a vendor can
fix themselves: `PERIOD_INVALID`, `DUPLICATE_INVOICE_NUMBER`, `AGREEMENT_NAME_MISMATCH`,
`AGREEMENT_MISSING`, `BF2_ROW_ARITHMETIC`, `BF2_BALANCE_DUE`,
`BF2_AMOUNT_DUE`, `ALLOCATION_SUM_MISMATCH` (409 `blocking_checks`). Vendor-number and
compliance codes are WVDOT's to work and never block a submission.
It stamps `invoices.submitted_at`, writes a `submitted` event with `actor_label
"<Vendor name> (vendor portal)"` and `data.resubmit`, and **leaves the status `received`** —
WVDOT staff log and route it exactly as before. Re-submitting while still `received` is allowed
and recorded. `GET /invoices?submitted=true` picks vendor-submitted invoices out of the queue.

**What a vendor may change.** Only while the invoice is `received` (409 `vendor_locked`
afterwards), and only `VENDOR_EDITABLE_KEYS` — the BF-2 fields, `contract_id_entered` and an
`agreement_id` of its own vendor (403 `staff_fields` for anything else: vendor, routing, WVDOT
USE, notes). A vendor may `withdraw` while the invoice is `received` or `logged`; every other
transition is WVDOT's (`StaffUser`). Allocations are recorded by WVDOT; vendors only see them.

## 7. Routing & Approval Chains

Implemented in `app/services/workflow.py::resolve_routing_rule`.

Routing rules are templates keyed by org unit and/or invoice type, with an
optional `min_amount` floor and a `priority`. Resolution considers only active
rules whose org unit and type (when set) match the invoice and whose `min_amount`
(when set) is ≤ the invoice's current amount, then picks by:

1. **Specificity** — org unit *and* type (3) beats org unit only (2) beats type
   only (1) beats a global rule (0);
2. lower `priority` number;
3. lower rule id.

The winning rule's ordered steps become the invoice's `approval_steps`
(`role_label`, `assignee_name`, `assignee_email`); the first is `active`, the rest
`pending`. A caller may force a specific rule with `routing_rule_id`. With no
matching rule (or a rule with no steps) the invoice still routes, with a single
default step **"Responsible Party"** assigned to the org unit's responsible party
(`route_invoice`); the `routed` event records `routing_rule: "default (responsible
party)"`. Routing again deletes the existing steps and rebuilds the chain. An invoice
on a master agreement with more than one project must be allocated before it can
route (`ALLOCATION_REQUIRED`, §10). `start_review` still refuses an invoice with no
steps at all (a guard, not a reachable state through the API).
`GET /api/routing-rules/resolve?org_unit_id&invoice_type_id` previews the chain the
wizard shows in step 3.

```ascii
 RULE RESOLUTION  (resolve_routing_rule — runs when the invoice is routed)

   invoice: org_unit · invoice_type · current amount
                      │
                      ▼
   active routing_rules ─► keep a rule when  org_unit_id     is null or = the invoice's
                                          ∧  invoice_type_id is null or = the invoice's
                                          ∧  min_amount      is null or ≤ current amount
                      │
                      ▼
   sort by  specificity ▼  then priority ▲  then id ▲
            unit + type = 3 › unit only = 2 › type only = 1 › global = 0
                      │
          ┌───────────┴────────────┐
          │ a rule won             │ nothing matched (or the rule has no steps)
          ▼                        ▼
   copy its steps in order   one step: "Responsible Party"
   → approval_steps          ← org unit's responsible_party_name / email
          └───────────┬────────────┘
                      ▼
      step 1 = active · others = pending · status → routed
```

```ascii
 CHAIN LIFE CYCLE  (act_on_step — only while the invoice is in_review)

  routed ──start_review──► in_review
                              │
        ┌─────────────────────┴──────────────────────┐
        │  [1 active] ─ [2 pending] ─ [3 pending] …  │   exactly one step is active at a time
        └─────────────────────┬──────────────────────┘
                              │ decision on the active step  (note, optional "delegated to …")
        ┌─────────────────────┼──────────────────────┐
        ▼                     ▼                      ▼
     approve                skip                  reject
   step → approved       step → skipped        step → rejected
   event step_approved   event step_skipped    event step_rejected
        └──────────┬──────────┘                      │
                   ▼                                 ▼
        next pending step → active            invoice → rejected
        (stays in_review)                     rejection_reason = note
                   │
                   │ no pending step left
                   ▼
        _finalize_approval
          blocking checks open? ──yes──► 409 blocking_checks · stays in_review
                   │ no
                   ▼
        invoice → approved · approved_at · event approved · OASIS entry drafted (§11)

  approve_invoice on an invoice with no active step finalizes directly (same gate).
```

The seed ships a "District CEI — three eyes" style chain per district (Project
Engineer → District Construction Engineer → Administrative Review) and simpler
division chains. Real responsible parties are an open question (see §16).

---

## 8. Financial Checks Engine

Implemented in `app/services/checks.py` as a pure function over the invoice, its
agreement, vendor, allocations, line items, and the agreement's other invoices.
Money comparisons use a tolerance of **$0.005**. Results are cached on the invoice
(`checks_json`, `checks_run_at`, block and warn counts) and returned in every
invoice read as `checks {checks[], block_count, warn_count, info_count, run_at,
stale}`.

**When checks run.** On upload/extraction, on every `PATCH`, on allocation and
line-item saves, on every workflow transition, and lazily by
`GET /api/invoices/{id}/checks` when the snapshot is **stale** — i.e. when the
invoice, its agreement, its vendor, or (for invoices with line items) any WVDOT default
rate has an `updated_at` newer than `checks_run_at`. `GET /api/invoices/{id}` recomputes a
stale snapshot before answering; the invoice page requests a recompute when it sees
`stale: true`. Every run of the checks first refreshes the rate-schedule estimate (§9.3),
so the two are never out of step.

**Severity semantics.** `block` prevents final approval (and, for the three codes
listed in §6, logging); `warn` is shown but does not stop anything; `info` is
context.

| Code | Severity | Rule |
|---|---|---|
| `PERIOD_INVALID` | block | `period_start` is after `period_end`. |
| `BF2_ROW_ARITHMETIC` | block | For each grid row, previous + current ≠ total-to-date. |
| `BF2_BALANCE_DUE` | block | For each column, balance due ≠ invoice amount − less retained + plus retained. |
| `BF2_AMOUNT_DUE` | block | `amount_due_consultant` ≠ balance due (current). |
| `BF2_MAX_PAYABLE` | warn | BF-2 original + supplementals ≠ BF-2 total. |
| `AGREEMENT_MISSING` | block | No agreement is linked, so ceiling and sequence cannot be verified. |
| `AGREEMENT_INACTIVE` | block | Linked agreement is `closed` or `pending`. |
| `PROCUREMENT_DOC_MISSING` | block | Agreement has no `oasis_doc_id` — the invoice arrived before the OASIS procurement document exists. |
| `CEILING_EXCEEDED` | block | Total to date > max payable; a supplemental is required. **Not evaluated for a `master`** — its `original + Σ supplementals` is not a billing ceiling ($0 / "DUMMY" totals); the ceiling lives on each `letter_agreement` (§16). |
| `SUPPLEMENTAL_NOT_IN_OASIS` | block | The invoice fits under the ceiling only because of a supplemental whose `oasis_entered_at` is empty. Not evaluated for a `master`. |
| `CEILING_NEAR` | warn | Total to date ≥ 90 % of max payable. Not evaluated for a `master`. |
| `PER_ASSIGNMENT_CAP_EXCEEDED` | warn (provisional) | A `letter_agreement`'s ceiling exceeds its master's per-assignment cap (`services/rates.py::effective_caps`, resolved from the parent in `services/invoices.py::_agreement_cap`). Warn-only pending WVDOT confirmation the caps are real (§16). |
| `BF2_AGREEMENT_AMOUNT_MISMATCH` | warn | BF-2 original agreement amount ≠ the agreement's `original_amount`. |
| `PREVIOUS_TOTAL_MISMATCH` | block when prior invoices exist, else info | BF-2 previous total ≠ Σ current amounts of the agreement's approved / keyed / paid invoices. |
| `OUT_OF_SEQUENCE` | warn | An earlier-period invoice on the same agreement is still open (unpaid). |
| `PERIOD_OVERLAP` | warn | Work period overlaps another invoice on the agreement. |
| `PERIOD_GAP` | info | More than 45 days between the previous invoice's period end and this period start. |
| `DUPLICATE_INVOICE_NUMBER` | block | Same vendor and invoice number on another invoice that is not rejected or withdrawn. Vendor-scoped, not agreement-scoped — so it fires on imported history where a vendor numbers invoices `1`, `2`, `10` on every agreement (§15.1). |
| `CONTRACT_ID_MISMATCH` | warn | Normalized entered agreement ID ≠ normalized extracted ID (advisory). |
| `CONTRACT_ID_UNVERIFIED` | info | Nothing was extracted; the typed ID stands alone. |
| `CONTRACT_ID_NOT_ON_AGREEMENT` | warn | Typed ID is not the linked agreement's contract ID. |
| `VENDOR_MISSING` | block | No vendor linked. |
| `VENDOR_INACTIVE` | block | Vendor is inactive in the portal. |
| `VENDOR_WORKERS_COMP_EXPIRED` | block | `workers_comp_expires` is in the past — OASIS will place a compliance stop. |
| `VENDOR_WORKERS_COMP_EXPIRING` | warn | `workers_comp_expires` within the next 30 days. |
| `VENDOR_NUMBER_MISMATCH` | warn | BF-2 vendor number ≠ the vendor record's OASIS number. |
| `VENDOR_NUMBER_PLACEHOLDER` | info | The vendor record still carries an imported `ENG…` placeholder; the BF-2's OASIS vendor number is reported so WVDOT can record it. `VENDOR_NUMBER_MISMATCH` never fires against a placeholder. |
| `VENDOR_NAME_CHANGED` | info | BF-2 vendor name matches one of the vendor's former names. |
| `ALLOCATION_REQUIRED` | warn | A `master` (or a multi-project `letter_agreement`) covering several projects with no allocations recorded (becomes a block at routing time). |
| `ALLOCATION_SUM_MISMATCH` | block | Σ allocations ≠ current amount. |
| `PCT_FUNDS_EXPENDED` | warn / info | Stated % funds expended differs from the computed value by more than 5 points; info when the BF-2 leaves it blank. |
| `INVOICE_DATE_BEFORE_PERIOD_END` | warn | Invoice dated before the work period ended. |
| `LINE_ITEMS_SUM` | warn / info | Extracted line items do not sum to the current amount (info when they tie). |
| `DIRECT_EXPENSES_REVIEW` | info | The invoice carries direct-expense (`odc`) lines: their total, count and by-kind breakdown (Lodging / Meals / Vehicle / …) for the reviewer. Direct expenses are billed at cost and reviewed against receipts, never priced against the rate schedule (§4.4). Only when at least one `odc` line exists. |
| `VEHICLE_USAGE_SUM` | warn / info | The Vehicle Usage Report total differs from the invoice's vehicle ODC lines by more than $0.01 (info when it ties). Only when both exist. |
| `AGREEMENT_NAME_MISMATCH` | block | The linked agreement's name ≠ the BF-2 PROJECT NAME (normalized) — the wrong agreement was picked; blocks `log` and `submit`. |
| `PROJECT_SPLIT_SUM` | warn / info | The per-project split sheet's total differs from the BF-2 current amount by more than $0.01 (info when it ties). Only when a split sheet was read. |
| `RATE_MISMATCH` | warn | One or more labor lines bill a rate that differs from the agreement's rate schedule (tolerance $0.005). When the schedule lists several rates for the same classification the line passes if the billed rate equals any of them. Details carry each line and `overbilled_total`, the amount billed above the schedule. Never blocks — rates are provisional (§16). |
| `RATE_NOT_ON_AGREEMENT` | info / warn | Info when the agreement has no rate schedule on file (labor is compared to WVDOT default rates where available); warn when it has rates but some labor classifications have none — details list them with a fuzzy suggestion the reviewer can map (§9.3). |
| `PERIOD_OUTSIDE_TERM` | warn | The work period ends after the agreement's effective term end, or starts before its term start, when those dates are recorded. |

---

**Visible to vendors.** `services/vendor_view.py::VENDOR_VISIBLE_CHECK_CODES` lists the codes a
vendor account sees on its own invoices: the period, contract-id, agreement-name, BF-2
arithmetic, ceiling, sequence, allocation, line-item, vehicle, split, vendor-number,
name-changed and workers'-comp codes. Hidden: `AGREEMENT_INACTIVE`, `PROCUREMENT_DOC_MISSING`,
`SUPPLEMENTAL_NOT_IN_OASIS`, `VENDOR_MISSING`, `VENDOR_INACTIVE` (WVDOT-internal) and the rate
audit `RATE_MISMATCH` / `RATE_NOT_ON_AGREEMENT`. Counts are recomputed on the filtered list.

## 9. Agreement Money Math

Implemented in `app/services/agreements.py`.

- `max_payable(agreement) = original_amount + Σ agreement_supplementals.amount`. This is the
  billing ceiling for a `single_project` and for a `letter_agreement` (its own original +
  supplementals); a `master` is **not** billed against it — its total is a cap, not a ceiling, so
  the ceiling checks skip masters (§8, §16).
- `billed_to_date(agreement) = Σ invoice_amount_current` over the agreement's
  invoices in `approved`, `keyed`, or `paid`.
- `remaining = max_payable − billed_to_date`; the invoice page also shows
  `remaining_after_this = remaining − this invoice's current amount`.
- `pct_expended` is reported as a percent with one decimal (e.g. `26.1`), not a
  fraction.
- **Burn-down** (`GET /api/reports/burn-down/{agreement_id}` and the agreement
  summary) is the cumulative billed amount by invoice period end, with the ceiling
  as a reference line; supplementals appear as steps in the ceiling.
### 9.1 The agreements list

Every figure the list shows beyond the agreement row itself is derived, so `list_page`
(`app/services/agreements.py`) computes them as SQL expressions over two grouped subqueries
(supplemental totals; invoice totals, counts and last invoice date) rather than per row in
Python. That matters twice over: filters count the whole table, and a sort on a derived column
orders the whole result set — previously a sort on `remaining` could only reorder the page that
had already been fetched, and each row cost three extra queries.

Filters (`GET /api/agreements`): `vendor_id`, `org_unit_id`, `invoice_type_id`, `status_`,
`kind`, `q` (agreement ID, agreement name or vendor name), `has_open`, `never_invoiced`,
`no_oasis_doc`, `has_supplementals`, `over_ceiling` (billed beyond max payable), `pct_min` /
`pct_max`, `amount_min` / `amount_max` (over max payable), `date_from` / `date_to` (agreement
date), `last_invoice_from`, and `last_invoice_before` (nothing billed since a date;
never-invoiced agreements are included, so it reads as "stale").

Sorts: `contract_id`, `name`, `status`, `kind`, `agreement_date`, `original_amount`,
`vendor`, `max_payable`, `billed_to_date`, `remaining`, `pct_expended`, `open_invoice_count`,
`invoice_count`, `supplemental_count`, `last_invoice_date`; prefix `-` for descending, nulls
last either way.

- **Sequence** is the ordering of the agreement's invoices by `period_start`;
  `sequence_position / sequence_total` is shown on the invoice, and an invoice is
  flagged `out_of_order` when an earlier-period invoice is still open.

---

### 9.2 Term and caps

`app/services/rates.py`. The **effective term end** is the latest of the agreement's
`end_date` and every supplemental's `term_end` (`effective_term_end`); the **effective
caps** are the latest supplemental's non-null `per_assignment_cap` / `annual_cap`, else the
agreement's (`effective_caps`). Both appear on the agreement page and in the intake
wizard's agreement card. A supplemental's `term_end` and `amount` are normally set from its
PDF through the document review's term and ceiling checks (§3.1 step 3), which compare the
PDF with the term and max payable in force before that supplemental. The caps are recorded and displayed only — no check consumes them
yet, because "billed per calendar year" has no query behind it (§16). The term feeds
`PERIOD_OUTSIDE_TERM` (§8).

### 9.3 Estimated cost from the rate schedule

`app/services/estimate.py` (pure) + `app/services/rates.py` (matching) +
`app/services/invoices.py::refresh_estimate`. Every time the checks run, the invoice's
line items are priced against the rate schedule and the result is cached as
`estimate_json` / `estimated_total` and returned in every invoice read as `estimate`
(also folded into each `LineItemRead` as `expected_rate`, `expected_amount`, `variance`,
`rate_status`, `rate_source`). It answers "what do the agreement rates say this invoice
should cost?" next to what the vendor billed.

- **Period date** for a labor line: its `work_date`, else the invoice `period_end`, else
  the `invoice_date`.
- **Classification text**: the row's `classification`, else its `task_name`, else its
  `party_name`; normalized by `normalize.py::norm_classification` (casefold, punctuation
  and hyphen/slash variants collapsed, whole-token roman numerals → digits so `Level III`
  ≡ `Level 3`, abbreviations expanded: admin, asst, tech, sr, jr, mgr, engr, insp, const,
  lvl, coord, spec, env; `Surveyor Technician` ≡ `Survey Tech`).
- **Firm**: the row's `firm_name` when the backup named one, else the **prime** — the
  schedule firm whose normalized name is contained in the agreement vendor's name
  (`baker` ⊂ `Michael Baker International, Inc.`). A classification that exists only under
  one other firm is taken from that firm (`firm_inferred`); one that exists under several
  is not guessed.
- **Lookup order** (`rates.find_rate`): a sticky **alias** on the agreement (firm-specific
  beats firm-agnostic) → the agreement rate in effect for (firm, classification) from the
  **latest supplemental** → the same key's nearest earlier period ending within two years
  (`year_fallback`) → a **WVDOT default rate** in effect for the classification (`default`,
  informational) → nothing (`no_rate`: the billed rate stands, with the closest schedule
  classification offered as a suggestion — never applied automatically).
- **Rate column** by `rate_kind`; a NULL column for that kind is `no_rate`
  (`kind_not_offered`). With several candidate rows the line is `matched` when the billed
  rate equals any of them, else `ambiguous` (treated as a mismatch, all candidates listed).
- `expected_amount = hours × expected_rate` quantized to cents (`Decimal`). ODC lines whose
  description (or its part before a `/`, e.g. `Fleet (day)/Ryan`) aliases to a
  `unit = day` row are priced as `quantity × day rate`; every other non-labor line passes
  through at its billed amount. Labor billed by a subconsultant that also appears as a
  lump-sum `subconsultant` line is checked but excluded from the totals (`counted = false`)
  so it is not counted twice.
- Totals: `labor_estimate`, `passthrough`, `estimated_total`, `invoiced_total` (Σ counted
  line amounts, else the BF-2 current amount), `variance = invoiced − estimated`,
  `overbilled_total` (Σ positive variances on agreement-matched lines — the figure
  `RATE_MISMATCH` reports), counts by status, and the distinct unmatched classifications
  with suggestions. The wizard's review step, the invoice page's line-items tab and the
  agreement card show it; "Map to…" on an unmatched classification writes an alias
  (`POST /api/agreements/{id}/rate-aliases`) and the estimate recomputes.
- Default-rate comparisons never produce `RATE_MISMATCH`; they only inform.
- Each `EstimateLine` also carries `project_number` and `programs` (§10) so the estimate table
  can show which program every priced line charges.
- **Model-inferred role mapping (tooling only).** `services/llm/role_mapper.py` asks the model
  to map the role titles printed on invoices onto an agreement's role list (its schedule
  classifications; billed and schedule rates are optional hints), validates every answer against
  the list, and reports confidence and reasoning; `alias_rows` turns mappings at confidence ≥
  0.5 into firm-agnostic `AliasRow`s. The `pull_lines` command uses it to label lines with the
  master role — it does not price them. The portal itself still records aliases only through
  "Map to…" on the agreement page.

## 10. Allocations & Multi-Project Splits

**Single vs multi-project is a property of the agreement, not of the intake.** `agreements.kind`
decides it (`single_project` / `master` / `letter_agreement`); the wizard no longer asks. A
`letter_agreement` behaves like a `single_project` here — `single_project_of` accepts both — so a
one-project assignment auto-allocates and only a `master` (or a multi-project assignment) splits.

- A **`single_project` agreement (or a one-project `letter_agreement`) bills its one project in
  full.** The portal records that allocation itself: `sync_single_project_allocation`
  (`services/invoices.py`) runs whenever the
  invoice is linked (upload, manual create, `PATCH`) and writes one `invoice_allocations` row for
  the agreement's project at the BF-2 current amount, keeps the amount in step when the current
  amount changes, and logs an `allocation_updated` event with `data.auto =
  "single_project_agreement"`. Rows someone recorded against a different project are left alone.
  A single-project agreement with **no project on file** allocates nothing (the wizard says so;
  routing is not blocked).
- **Every line item bills the same project.** When an invoice has exactly one allocation,
  `stamp_line_item_projects` fills `invoice_line_items.project_number` on lines that have none
  (runs inside `refresh_checks`, so every mutation path inherits it). Split invoices leave it null.
- A **master agreement (or a multi-project `letter_agreement`) with more than one project must be
  allocated before it can be routed** (`ALLOCATION_REQUIRED`; the routing guard in
  `services/workflow.py` covers both kinds). One allocation row is acceptable when the whole amount
  goes to a single project; what matters is recording which project(s) are billed.
- Allocations are saved with `PUT /api/invoices/{id}/allocations {items[]}`. Free-typed project
  numbers are created as projects first. The response reports the sum, the current amount, and
  whether they tie; `ALLOCATION_SUM_MISMATCH` blocks approval when they do not.
- The intake wizard (step 4, `allocationMode()` in `IntakeWizard/allocationMode.ts`) shows a
  read-only "bills project …" card for a single-project agreement, the split editor for a master
  agreement (tie-out in integer cents; **Next** disabled until the rows tie), and a "link an
  agreement first" note when none is linked. Without an agreement nothing is saved.
- Line items (`PUT /api/invoices/{id}/line-items {items[]}`) are otherwise independent of
  allocations; they exist for reporting and audit (FR-9) and feed only the `LINE_ITEMS_SUM` check.

**TheHub validation (informational).** `hub_projects` (§2) mirrors TheHub's project master;
`services/hub.py` answers whether a printed project number is a project TheHub knows. A Hub key
is the 10-digit WVDOH project key (`2018001357`); anything else (`1729999R2`, `202460023`) cannot
be one. `GET /api/projects/hub-check?numbers=…` returns `validated` **true / false / null** per
number — null when the mirror is empty (demo data, import never run), in which case the UI shows
nothing rather than flagging everything. The same fields ride on `ProjectRead` (`hub_validated`,
`hub_name`, `hub_status`; matched through `contract_id` or `number`) and on each
`suggested_allocations` row. The wizard renders an **"In TheHub" / "Not in TheHub"** chip
(`components/hub/HubChip.tsx`) beside the agreement's project, on split-sheet rows and on
allocation rows; the invoice page's **Allocations tab** (`InvoicePage/tabs/AllocationsTab.tsx`)
asks `hub-check` for its rows the same way, puts the compact chip on each project row and sums it
up in the panel header ("All 9 in TheHub" in green, "7 of 9 in TheHub" in amber with the missing
numbers in the tooltip). Nothing blocks on it: a project that is not in TheHub can still be
allocated and routed — it is only noted.

**Programs per line item (`services/programs.py`).** On a real BF-2 the PROGRAM box carries the
10-digit project key, so a line's *program* is the project it bills. `line_programs(inv)` gives
every line item its `programs` (`ProgramShare`: project number and name, hours, amount, source):
on a single-allocation invoice every line charges that project (`allocation`); on a split
invoice each line is traced to the split sheet's rows by person (`norm_person` — "Boyd, Jason"
≡ "Jason Boyd"), work date and kind (Regular/Overtime ↔ labor rate kind; Fleet / Mileage /
Per Diem / Lodging ↔ the expense kind, loosened to any expense row that day), and the group's
printed contract id is resolved to the allocated project by number or by the project's own
`contract_id` (`resolve_program`; an id the invoice does not allocate to stays as printed). A
day the sheet divides between projects yields several shares. `stamp_line_item_projects` fills
`project_number` from the single allocation, else from the split sheet **only when a line
charges exactly one program**; lines that span programs stay unstamped and show the split.
The shares ride on `LineItemRead.programs` (computed on every read) and are copied onto
`EstimateLine.programs` when the estimate recomputes; the Line items grid and the estimate
table show a **Program** column (colour dot keyed to the allocation order, project key, short
name; a segmented bar with the split in the tooltip for multi-program lines). The estimate
table reads the live line-item programs first, so it is right before the checks next run.

**Suggested from the invoice.** When the package carries a per-project split sheet (§4.4),
`InvoiceRead.suggested_allocations` lists each group with its contract id, project name, hours,
amount, the matching project on file — matched by `projects.contract_id` (the WVDOH contract
id vendors print) or by project number — and its Hub validation. Step 4 of the wizard offers "Use
the invoice's split" on a master agreement, which seeds the allocation rows; groups without a
project are created on the fly with the contract id stored on the new project so the next invoice
matches automatically. On a single-project agreement the sheet is shown for information only.

---

## 11. OASIS Keying Assist

Implemented in `app/services/oasis.py`; the screen is the **OASIS entry** tab of
the invoice page. OASIS remains the financial source of truth; the portal produces
a screen-ready layout to key from (Phase 1 of the integration).

**Lifecycle.** `ensure_entry()` creates a `draft` entry when approval is finalized
(or on first `GET`). `draft → ready` happens when the accounting lines tie to the
invoice total (automatically during **key**, or explicitly via `PUT` with status
`ready`, which returns `422 lines_do_not_tie` otherwise). `ready → keyed` happens
when the invoice is keyed with an OASIS document ID.

**Header.** `doc_type` (default `PRC`, provisional), `vendor_code` (OASIS vendor
number), `address_code` (remit address ID), `vendor_invoice_number`,
`vendor_invoice_date`, `invoice_received_date`, `service_from` / `service_to`
(work period), `procurement_doc_type` / `procurement_doc_id` (from the agreement),
`total_amount` (amount due consultant, else current amount).

**Default accounting lines.** One line per allocation (amount, task order, project
name and number) or, without allocations, a single line for the full amount. Each
line carries `fund`, `unit` (BF-2 `wv_unit`, else the org unit's provisional
code), `activity` (`wv_act_n_or_p`), `sub_activity`, `program`, `phase`,
`task_order`, `amount`, `description`, `project_number`. Fund, activity, and
sub-activity are not known to the portal today and render as "needed before
keying" until a user fills them via **Edit accounting**. The allocation editor no longer captures a task order (frontend 0.5.3), so the task-order cell of a default line is blank until it is typed on the OASIS tab; allocations recorded earlier keep the value they had.

**Required before keying.** Header: `vendor_code`, `address_code`,
`vendor_invoice_number`, `vendor_invoice_date`, `procurement_doc_id`,
`total_amount`. Each line: `fund`, `unit`, `activity`, `amount`. Missing fields
are listed in `missing_fields`; the screen hides the hint once the entry is
keyed.

**Copy sheet.** `GET /api/invoices/{id}/oasis-entry/copy-sheet` returns the header
and lines as label/value pairs in screen order plus a tab-separated `tsv` for
pasting; every cell on the screen is click-to-copy.

---

## 12. Reports

Implemented in `app/services/reports.py`. All durations come from the event
ledger, never from wall-clock guesses.

### 12.1 Dashboard

Endpoint: `GET /api/reports/dashboard`.

| Field | Definition |
|---|---|
| `open_count`, `open_amount` | Invoices in an open status (`received` … `keyed`, `on_hold`). |
| `awaiting_action_count` | `received`, `logged`, `routed`, `in_review`, `approved`, `on_hold` — the navbar queue badge and the "In queue" tile. |
| `awaiting_review_count` | `routed` + `in_review`. |
| `awaiting_keying_count` | `approved`. |
| `blocking_count` | Open invoices whose cached checks have ≥ 1 block. |
| `paid_this_month`, `paid_last_30d` | Count and amount by `paid_at`. |
| `median_days_to_pay_90d` | Median of `paid_at − received_at` over invoices paid in the last 90 days. |
| `by_status` | Count and amount per status (the pipeline bar). |
| `aging_by_unit` | Per org unit: open count, median and max days open. |
| `volume` | Last 6 months: received and paid counts and dollars. |
| `attention` | Blocking checks, flagged issues, and compliance stops with the invoice, code, and age. |
| `compliance_alerts` | Vendors with expired or expiring workers' comp and their open invoice counts. |
| `oldest_open`, `recent_events` | Lists for the dashboard cards. |

### 12.2 Aging

Endpoint: `GET /api/reports/aging?group_by=stage|org_unit|vendor&date_from&date_to`.

Stage durations are measured between consecutive status events for each invoice
over the fixed stage pairs:

```
received→logged, logged→routed, routed→in_review,
in_review→approved, approved→keyed, keyed→paid
```

For each pair the report gives count, mean, median, and p90 days. Grouping by org
unit or vendor adds per-group open count and amount, mean days open, median days
to pay, paid count, and `stage_medians` (median per stage pair — the heat matrix
cells). `open_by_bucket` counts open invoices by days open: `0-7`, `8-30`,
`31-60`, `61-90`, `90+`. `slowest_stage` is the pair with the largest median.

### 12.3 Volume

Endpoint: `GET /api/reports/volume?months=12&group_by=org_unit|invoice_type|vendor`.

One row per month with received count and dollars (by `received_at`) and paid
count and dollars (by `paid_at`), optionally broken out `by_group`.

### 12.4 Budget forecast

Endpoint: `GET /api/reports/budget-forecast`.

Requirement FR-33: tell budget staff what is about to draw on encumbrances, by
purchase order. Open invoices (every status except `paid`, `rejected`,
`withdrawn`, and `keyed`) are grouped by agreement with the OASIS procurement
document, vendor, org unit, open amount, max payable, billed to date, and
remaining after these invoices. Each invoice is assigned a **WV fiscal year** from
its `period_end`: the year runs July 1 – June 30 and is named for the ending year
(a period ending 2026-08-31 is FY2027). `current_fy_amount` and `next_fy_amount`
split the open total; `digest_text` is a plain-text weekly digest for e-mail.

---

### 12.5 Vendor dashboard

`GET /api/reports/vendor-dashboard` (`services/reports.py::vendor_dashboard`) is built from one
vendor's rows only (a vendor account gets its own; staff must pass `vendor_id`):

| Field | Definition |
|---|---|
| `open_count`, `open_amount`, `by_status` | The vendor's invoices in `OPEN_STATUSES`, and counts/amounts for all ten statuses |
| `needs_attention_count`, `attention[]` | `rejected` in the last 90 days (message = the rejection reason), `on_hold`, `received` and not yet submitted, open with a vendor-visible blocking check, and certificate expiries (workers' comp / insurance expired or within 30 days) |
| `awaiting_wvdot_count` | submitted `received` + `logged` + `routed` + `in_review` |
| `awaiting_payment_count` | `approved` + `keyed` |
| `in_flight[]` | open invoices oldest first, each with `next_step` — plain-language copy that never names a unit or reviewer |
| `agreements[]` | every agreement of the vendor that is not closed-and-idle: `agreement_stats` plus `pending_amount` (open invoices on it) and `term_end_effective` |
| `payments` | `paid_fytd` (WV fiscal year, Jul–Jun), `paid_last_12m`, `last_payment` (with warrant), median days submitted→paid and received→paid over the last 12 months |
| `volume`, `recent` | 12 monthly points (§12.3) and the 10 most recent invoices |

## 13. The Invoice Page & Intake Wizard (frontend rules)

**Back goes back.** The navbar's Back button returns to the previous history entry
(`hooks/useBackTo.ts`), because a detail page is reached from several places — an invoice from
the invoices list, from an agreement's invoice grid, from the dashboard. It falls back to the
declared parent page (`/invoices`, the agreements list, `/vendors`) only when there is nothing to
go back to: React Router keys the first location of a session `'default'`, which is what a deep
link, a bookmark or a refresh lands on. Tab changes on the invoice and agreement pages replace
rather than push (`?tab=`), so Back leaves the record instead of stepping through its tabs; the
intake wizard is the exception — its steps push, so Back inside the wizard is "previous step" and
the navbar button leaves for the invoice.

These rules live in `frontend/src/features/invoices/`.

### 13.1 Primary action per status

Implemented in `features/invoices/workflow.ts`.

| Status | Primary action | Notes |
|---|---|---|
| `received` | Continue intake | Opens the wizard at step 2. |
| `logged` | Route invoice | Falls back to Continue intake when type or org unit is missing. |
| `routed` | Start review | |
| `in_review` | Approve for payment | Disabled while any blocking check exists; the count is shown. |
| `approved` | Key in OASIS | Switches to the OASIS tab; "Mark keyed" needs the document ID. |
| `keyed` | Mark paid | Dialog for paid date and warrant / EFT number. |
| `on_hold` | Resolve issue | Returns to `held_from_status`. |
| `paid`, `rejected`, `withdrawn` | none | Terminal. |

Secondary actions: **Reject…** (reason required) in `logged`, `routed`,
`in_review`, `approved`; **Flag issue…** in any open status except `on_hold`;
**Withdraw** in `received`, `logged`, `routed`, `in_review`; **Print BF-2**
always. The rail's "who's next" sentence names the responsible party or org unit.

### 13.2 BF-2 paper

Implemented in `features/invoices/bf2/`.

- Arithmetic runs in **integer cents** so the on-screen paper never drifts:
  total-to-date = previous + current per row; balance due = invoice − less + plus
  per column; amount due consultant = balance due (current); max payable =
  original + supplementals; % funds expended = balance due total ÷ max payable,
  rounded to one decimal.
- Computed cells that disagree with the stored / extracted value get a `.bf2-diff`
  outline with both numbers in the tooltip.
- Extraction tints: ≥ 0.85 confidence "read with confidence"; 0.40–0.85 "low
  confidence — check it"; a **required** field that was not found is rose "not
  found — type it" (optional blanks stay neutral); user edits are indigo.
- Editability follows §6; edits autosave 800 ms after the last keystroke via
  `PATCH`, with a "Saving… / Unsaved changes / Saved" line in the rail.
- **Print BF-2** switches fields to plain text and prints only the sheet at US
  Letter size.

### 13.3 Intake wizard

Step 1 uploads (§3). Steps 2–5 share one form (react-hook-form + zod); each
**Next** validates only that step's fields, saves them with `PATCH`, and advances
`?step=`, so the wizard is reload-safe and resumable while the invoice is
`received` or `logged`.

- **Step 2 Confirm BF-2** — the paper with tints; the agreement card (§5) is an
  autocomplete over agreements (search starts from the BF-2 PROJECT NAME; shows the
  agreement *name* once picked; free text allowed when the agreement is not on file).
  **Picking is the decision**: it sets the agreement ID and vendor, silences the ID
  cross-check, and — when the picked name differs from the BF-2 PROJECT NAME — asks for a
  reason (kept as `contract_id_override_reason`) and then sets the BF-2 PROJECT NAME to the
  agreement name so the name check passes. The Agreement card shows kind (single project /
  master · N projects), the single project with its "In TheHub" chip, max payable,
  billed to date, remaining, term, rate schedule, and a sequence hint when the BF-2
  previous total ≠ billed to date; extraction chips (`7 of 7 required`,
  `method: text`, `5/10 text pages`); "Re-run with Claude" when the backend reports
  Claude is available.
- **Step 3 Classify & route** — invoice type (provisional), org unit prefilled
  from `wv_unit` or the agreement (the source is captioned), responsible party,
  the approval-chain preview from `/api/routing-rules/resolve`, and the WVDOT USE
  block.
- **Step 4 Allocate** — §10: read-only project card for a single-project agreement,
  the split editor for a master agreement, Hub chips on every project shown.
- **Step 5 Review & submit** — summary card, line-item recap, checks panel;
  "Log & route invoice" performs `log` then `route`; any blocking check disables
  submit and offers "Flag an issue instead".

### 13.4 Status colours

`received` slate · `logged` sky · `routed` indigo · `in_review` amber ·
`approved` emerald gradient · `keyed` violet · `paid` brighter emerald gradient ·
`rejected` rose · `on_hold` orange (labelled "Issue") · `withdrawn` slate.
Translucent tints with matching borders; gradients are reserved for the two good
terminal states.

---

### 13.5 Agreement page

`frontend/src/features/agreements/AgreementPage.tsx`. The header and summary band (Term,
Original, Supplementals, Max payable, Billed to date, Remaining, % expended) stay on every
tab; the tab is kept in the URL as `?tab=` (`overview` is the default and omitted).

- **Overview** — burn-down, the invoices grid, a "Documents & rates" summary card (pending
  reviews are called out in amber and link to the tabs), supplementals (with term extension
  and caps), projects, details.
- **Edit** (staff only; `AgreementEditDialog.tsx`, `PATCH /agreements/{id}`) — every field is
  editable until something is charged to the agreement. Once a non-withdrawn invoice exists,
  the fields that define what was billed against — Agreement ID, vendor, kind, original amount
  and agreement date — lock in the dialog and on the server (409 `agreement_charged`; change
  the ceiling with a supplemental). The **OASIS procurement document type and ID are always
  editable**: the red "No OASIS procurement doc — set it" chip opens the dialog on them, and
  saving re-runs the invoices' checks so `PROCUREMENT_DOC_MISSING` clears.
- **Documents** — the attached PDFs on the left (kind / supplemental chip, page count, read
  status, rates found, "Review & import" when `ready`), the selected PDF open in the browser
  viewer on the right with Open / Download / Re-read / Remove and the facts read from it.
  Creating an agreement with a PDF, or adding a supplemental with one, lands on this tab.
- **Rates** — the rate schedule grid (§3.1, §9.3): firm and "in effect on" filters, a
  superseded toggle, add / edit / remove.
- **AWP** (`AwpTab.tsx`; shown only when a project on the agreement carries an
  `awp_contract_number`) — the AASHTOWare construction contract(s) behind the agreement, read
  live from TheHub by `GET /agreements/{id}/awp` (`services/awp.py`; nothing is stored). The
  header chip "AWP 2014000654" jumps to it; the summary band is untouched. The tab: a
  contract list for master agreements; the **life-of-contract rail** drawn to scale in days —
  Advertised → Let → Awarded → Executed → Fully executed agreement → Notice to proceed → Work
  began → Substantially complete → Final estimate approved — with the construction and closeout
  spans shaded, elapsed time between milestones, a *today* line while the final estimate is not
  approved — milestones that fall within days of each other on a multi-year rail share one
  code-only label whose dates are in the tooltip (`awp.ts::clusterMarks`), with the total span
  ("advertised → final estimate", or how long it has been open) in the card's top right; the
  change-order ledger with signed participating / non-participating amounts and a running net,
  its count and net in the card's top right ("✓" = imported into TheHub as a change request,
  which is not approval); each date with the
  feed that supplied it (rich contract feed, simple date feed, both, or a flagged conflict) and
  the feeds' update stamps; the identifier namespaces (AWP contract Id, proposal Id, revision,
  state / federal project numbers, Hub project Id); and TheHub's own construction phase with two
  cross-checks — construction start equals AWP work begin, phase end equals the latest
  change-order completion — carrying the **E&C percent** on top (a 0–20% bar with the
  letting-year average as a tick and the contract's share of the AWP population, since AWP keeps
  one value per contract and no history). When TheHub cannot be reached the tab says so and lists the contract
  numbers instead of failing the page (`available=false`, reason `no_credentials` /
  `driver_missing` / `connection_failed`).

### 13.6 Vendor portal

A `vendor` account lives under `/vendor/*` (`app/router.tsx`, `VendorLayout`); the navbar reads
**Vendor Portal** (`app/navConfig.ts::VENDOR_NAV`, blue bar) and page titles end in "— Vendor
Portal" (`hooks/usePageTitle.ts`). `lib/portal.ts::portalFor` decides the half from `user.role`
(anything but `vendor` is staff); `safeRedirect` honours `?redirect=` only inside the user's own
portal. `ProtectedRoute` sends a vendor who hits a staff URL to `/vendor` and shows staff who hit
`/vendor` a panel — never a redirect loop.

- **Dashboard** (`features/vendor/VendorDashboardPage.tsx`) renders §12.5: a ceiling band, KPI
  tiles that link into the invoice list, invoices in flight, the pipeline, needs-attention rows,
  agreement ceilings with term end, payments, recent invoices.
- **Invoices** — views All / In progress / Needs attention (`view=needs_attention`) / Paid;
  no vendor, unit or type filters; a "where it is" column (`vendorWorkflow.ts::vendorNextShort`).
- **Invoice** — tabs BF-2 (read-only paper, WVDOT USE box blank: `Bf2Sheet showWvdotUse`), Your
  PDF, Line items (no rate audit: `LineItemsTab hideEstimates`), Projects (allocations read-only);
  the rail shows the status sentence, a **progress timeline** Submitted → Logged → Routed → In
  review → Approved → Keyed → Paid dated from the ledger (`vendorTimeline.ts`; a returned / on
  hold / withdrawn state is appended after the last completed step), "Things to fix" (the
  server-filtered checks), the agreement's money, and the vendor's compliance. Actions: Continue
  intake (until submitted), Withdraw (`received` / `logged`), Resubmit corrected package
  (`rejected` → upload with `supersedes_invoice_id`), Print BF-2. Never shown: OASIS, approval
  chain, history notes.
- **Agreements** — the staff pages with `vendorView` / `readOnly`: no creation, supplemental,
  document or rate editing; the band shows the agreement name rather than the OASIS document.
- **Vendor info** — compliance with a plain-language payment consequence
  (`vendorFormat.ts::complianceAdvice`), remit address and contact (editable through
  `PATCH /vendors/me`), name history, counts, how payment works, contact WVDOT (provisional).
- **Intake** — one `IntakeWizardPage` with `variant` (`IntakeWizard/wizardVariant.ts`): the
  vendor runs Upload · Confirm BF-2 · Projects · Review & submit. The agreement autocomplete is
  server-scoped to the vendor; the Projects step shows the split read-only (a single-project
  agreement bills its project automatically, §10); the review hides the rate estimate and titles
  the checks "Things to fix before submitting"; the footer ends in **Submit to WVDOT**
  (`POST /submit`). `vendorIntakeSchema` drops the routing requirement and the tie rule. Staff
  URLs and behaviour are unchanged (`?step=2..5`).

## 14. Authentication, Storage & Configuration

**Roles.** `users.role` is `admin` (WVDOT staff, every permission) or `vendor` (one consultant
firm's account, `vendor_id` set). `core/deps.py`: `StaffUser` (403 `staff_only` for vendors),
`vendor_scope(user)` (`None` for staff; a vendor's id; 403 `vendor_unlinked` when a vendor
account has no vendor), `is_vendor`. Scoping happens at the object-fetch choke points
`routes/_common.py::get_invoice_or_404 / get_agreement_or_404` — another vendor's object reads
as **404**, never 403, so ids cannot be enumerated — and in the two list queries (the vendor's own
rows, whatever `vendor_id` the client asked for). `GET/PATCH /vendors/me` are the vendor's own
record (`VendorSelfUpdate`: address and contact only). Vendor responses pass through
`services/vendor_view.py`, which blanks the WVDOT USE block, notes, approval steps, OASIS entry,
the estimate and the estimate columns on line items, filters checks (§8) and collapses WVDOT
actors on events to "WVDOT". Error codes: `403 forbidden | staff_only | vendor_unlinked |
not_vendor | staff_fields`, `409 vendor_locked | agreement_charged`, `422 agreement_vendor_mismatch`. The seeded vendor
account is `PORTAL_DEV_VENDOR_EMAIL` (default `mbi@wv.gov`) with the dev password, linked to the
Michael Baker vendor.

- **Auth.** Two ways in — the WVDOT identity broker for staff, an email and
  password for consultant firms — both ending in the same 12-hour HS256 JWT from
  `app/core/security.py`. Every other route requires that bearer token; the
  frontend stores it in `localStorage` (`cip_token`) and signs out on any `401`.
  See §14.1 and §14.2.
- **Settings** are read from `backend/.env` with the `PORTAL_` prefix
  (`app/core/config.py`): `DATABASE_URL`, `JWT_SECRET`, `JWT_EXPIRE_HOURS`,
  `CORS_ORIGINS`, `STORAGE_DIR`, `MAX_UPLOAD_MB`, `ANTHROPIC_API_KEY`,
  `CLAUDE_MODEL`, `CLAUDE_EXTRACTION_ENABLED`, `EXTRACTION_MIN_REQUIRED_FIELDS`,
  `LLM_ANALYSIS_ENABLED`, `CLAUDE_MODEL_CLASSIFY`, `CLAUDE_MODEL_EXTRACT`, `LLM_MAX_PAGES`,
  and `CLAUDE_MODEL_RATES` (default `claude-opus-5`; the vision pass over attached
  agreement PDFs, §3.1).
  The database may instead be given in parts — `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`,
  `DB_PASSWORD` — and `Settings._assemble_database_url` builds `DATABASE_URL` from them
  (password percent-encoded) whenever `DATABASE_URL` itself is not set; an explicit URL wins.
  `start-dev.sh` resolves the server, port and database through these same settings, creates
  the database if it is missing, migrates, and starts the servers **without seeding**; `--import`
  runs the Engineering import (§15.1) and `--demo` the demo seed (§15) first.
- **Errors** are `{detail, code, …}`: `401 unauthenticated|bad_credentials`,
  `404 not_found`, `409 illegal_transition|blocking_checks|duplicate_document|
  oasis_entry_not_ready`, `413 payload_too_large`, `415 not_a_pdf`, `422
  missing_fields|reason_required|note_required|doc_id_required|warrant_required|
  paid_before_keyed|lines_do_not_tie|validation_error`.
- **Lists** return `{items, total, page, page_size}`; sorting uses a single `sort`
  parameter with a leading `-` for descending.
- **Storage** is the local filesystem under `backend/storage/` (`invoices/<id>/` for
  packages, `agreements/<id>/` for agreement PDFs); the directory is git-ignored and the
  demo seed's `--reset` wipes the invoice side.
- **Deployment (mmsdev).** One Docker image (`deploy/Dockerfile`) builds the frontend with
  Vite `base=/invoice-portal/` and runs the API with `PORTAL_ROOT_PATH=/invoice-portal` and
  `PORTAL_STATIC_DIR=/app/static`. `app/main.py::build_asgi` mounts the API and the SPA under
  the prefix; `/assets/*` are served as files and every other non-`/api` path returns
  `index.html`. Interactive API docs are at `/api/docs`. Apache forwards `/invoice-portal`
  unchanged to `127.0.0.1:8010` (same pattern as `/dot12` → `:5000`). `~/invoice-portal/build.sh`
  on the box pulls the repo over a read-only deploy key (or builds an rsync'd tree with
  `--local`), rebuilds, restarts with `--restart unless-stopped`, waits for the health check,
  and optionally seeds. Uploads persist in `~/invoice-portal/storage`; the database is
  `invoice_portal` on the shared WVDOT Postgres. Runbook: `deploy/README.md`.

### 14.1 Sign-in methods

Two populations, two paths, one session:

| Who | How they sign in | Identified by |
|---|---|---|
| **WVDOT staff** (`role = admin`) | The WVDOT identity broker — §14.2 | `users.windows_account_name` (the broker's `sub`: employee ID / Windows account) |
| **Consultant firms** (`role = vendor`) | Email + bcrypt password, `POST /api/auth/login` | `users.email` |

Both paths end at the same place: `routes/auth.py::_issue_token` mints the portal's
own 12-hour HS256 JWT (`core/security.py::create_access_token`). The broker's own
tokens are validated and discarded — §14.2 explains why.

`GET /api/auth/methods` (`AuthMethods`) tells the sign-in page what to render, read
at request time so the broker can be switched on **without a frontend rebuild**:
`password`, `staff_password`, `sso`, `sso_login_url`, `sso_label`.
`features/auth/LoginPage.tsx` shows the WVDOT button when `sso`, and puts the
password form behind a link — labelled "Consultant sign-in" once
`staff_password` is false.

**Passwords are retired per population, not globally.** `PORTAL_STAFF_PASSWORD_LOGIN_ENABLED=false`
refuses a password login for any non-vendor account (`401 staff_password_disabled`)
and leaves consultants untouched, because an external firm has no WVDOT account to
fall back on. An SSO-provisioned row has `password_hash IS NULL`, and `login()`
short-circuits on that before ever calling bcrypt, so it can never authenticate.

Identity columns are all nullable and `ck_users_identity` requires at least one of
`email` / `windows_account_name` (migration `0009_sso.py`). Uniqueness is
case-insensitive through the partial functional indexes `users_email_lower_idx` and
`users_windows_account_lower_idx`; `models/user.py` normalises on write —
`windows_account_name` upper-cased with any `DOMAIN\` prefix stripped, `email`
lower-cased. `User.label` (full name → display name → email → Windows account) is
what invoice events record as `actor_label`, since Entra does not always supply a name.

### 14.2 WVDOT SSO (OIDC relying party)

The broker at `https://ocidev.transportation.wv.gov/auth` fronts the Entra/SAML IdP
and speaks **OpenID Connect authorization-code flow**, so the portal never touches
SAML. Reference: `RELYING_PARTY_INTEGRATION.md`. Implemented by `app/core/oidc.py`
(the protocol), `app/services/sso.py` (claims → user row), `app/models/sso.py`
(`sso_login_states`) and `app/api/routes/auth.py` (the four endpoints).

**The round trip.**

1. `GET /api/auth/sso/login?redirect=<path>` writes an `sso_login_states` row with a
   random `state` + `nonce` and the sanitised return path, then 302s to the broker's
   `authorization_endpoint`. Only same-app paths survive `_safe_redirect` (no `//`,
   no absolute URLs), so the parameter cannot become an open redirect.
2. The broker runs the Entra login and 302s back to
   `GET /api/auth/sso/callback?code=&state=`.
3. The callback matches `state` (unknown, replayed or older than **10 minutes** all
   fail identically as `sso_bad_state`), marks it consumed, and exchanges the code
   **inline** — codes are single-use and expire in ~60 s.
4. The ID token is validated — all five checks of §5 of the integration doc:
   RS256 signature against the broker's JWKS matched on `kid`, exact `iss`, `aud` ==
   our `client_id`, unexpired, and `nonce` equal to the one we sent.
5. `services/sso.py::upsert_user_from_claims` resolves the row (below).
6. The browser is sent to `<frontend>/login/callback?code=<handoff>`. **The portal's
   own JWT is deliberately not in that URL** — it would be written to browser history
   and could leak in a `Referer`. `features/auth/SsoCallback.tsx` trades the
   single-use handoff code over `POST /api/auth/sso/exchange` (60-second window),
   clears the query cache and lands the user on `redirect_to`.

**Endpoints are never hard-coded.** `core/oidc.py::get_metadata` reads the discovery
document (cached one hour) and takes `authorization_endpoint`, `token_endpoint` and
`jwks_uri` from it — §1 of the integration doc calls that the single source of truth.

**The broker's tokens are not a session.** There are no refresh tokens and they live
15 minutes; §6 makes ongoing session management the relying party's job. They are
validated, read, and dropped.

**Resolving the user** (`upsert_user_from_claims`), in order:

1. Match on `windows_account_name` == `sub` — the stable, immutable key.
2. Otherwise match a **non-vendor** row on `email`, and adopt the `sub` onto it. This
   is the priming path: an administrator sets an account up knowing only an email
   address, and the first sign-in lands on *that* row instead of creating a duplicate.
3. If the matched row is a **vendor** account, refuse with `vendor_account_sso`. A
   consultant login is an external credential with its own vendor scoping; adopting
   one would hand a staff identity that firm's invoices, and provisioning alongside it
   is impossible anyway because email is unique. A human has to separate the two.
4. A disabled account is refused **before** the row is touched, so a rejected attempt
   never moves `last_login_at`.
5. Otherwise provision (`PORTAL_OIDC_AUTO_PROVISION`, default on) on
   `PORTAL_OIDC_PROVISION_ROLE` (default `admin`) with `vendor_id = NULL`. With
   auto-provision off, an unknown identity is refused with `account_not_provisioned`.

Only what the IdP owns is refreshed on each login — `display_name`, `email`,
`first_login_at` (once), `last_login_at`. **`role` and `vendor_id` are never
overwritten**, which is exactly what would otherwise undo an administrator's setup.
`full_name` falls back to `sub` because the broker nests both `name` and
`preferred_username` inside `if name:` and omits them when Entra sent no name.

**Error codes**, all surfaced as `?sso_error=<code>` on `/login` and mapped to
prose in `features/auth/ssoErrors.ts`: `sso_not_configured`, `sso_missing_code`,
`sso_bad_state`, `sso_no_id_token`, `sso_discovery_failed`, `sso_token_failed`,
`sso_bad_token`, `sso_bad_nonce`, `sso_bad_handoff`, `account_not_provisioned`,
`account_disabled`, `vendor_account_sso`, and `sso_<broker error>` (e.g.
`sso_access_denied`).

**Why the different subdomain is a non-event.** The portal is served from
`mmsdev.transportation.wv.gov/invoice-portal` and the broker from
`ocidev.transportation.wv.gov` — so §8 of the integration doc, which assumes a shared
host, does not apply. It does not need to: the portal authenticates with a bearer
token in `localStorage`, and `state`/`nonce` live in `sso_login_states` rather than a
cookie, so nothing crosses the origin boundary and no `SameSite` question arises. (The
table also works across uvicorn workers.) The one real requirement is **outbound HTTPS
from the app container to the broker** for discovery, JWKS and the token exchange —
the broker sets no CORS headers and answers `OPTIONS` with 405, so that exchange must
stay server-side, as it does.

**Configuration** (`PORTAL_` prefix, `core/config.py`): `OIDC_ENABLED`,
`OIDC_ISSUER`, `OIDC_DISCOVERY_URL`, `OIDC_CLIENT_ID`, `OIDC_CLIENT_SECRET`,
`OIDC_REDIRECT_URI`, `OIDC_SCOPES`, `OIDC_AUTO_PROVISION`, `OIDC_PROVISION_ROLE`,
`OIDC_HTTP_TIMEOUT`, `FRONTEND_BASE_URL`, `STAFF_PASSWORD_LOGIN_ENABLED`.
`Settings.oidc_configured` requires enabled **and** client id, secret, redirect URI
and discovery URL all present, so a half-filled `.env` cannot render a sign-in button
that could only 500. **`OIDC_REDIRECT_URI` must match the registered value byte for
byte** — the broker compares by strict equality, with no wildcards and no
trailing-slash tolerance. Registered value for the deployment:
`https://mmsdev.transportation.wv.gov/invoice-portal/api/auth/sso/callback`.

---

## 15. Demo Seed

`python -m app.seed [--reset]` (`app/seed/`) is idempotent by natural keys and
creates: the user (when the configured e-mail changes and exactly one account exists, the
seed renames that account and re-hashes its password instead of creating a second user);
10 districts and 8 divisions with responsible parties; 7
provisional invoice types; 9 vendors (including Michael Baker International with
OASIS vendor number `000000160331`, Quinn Consulting as a subconsultant-only
vendor, one vendor with expired workers' comp, one expiring within 30 days, and one
with a name-history row); 12 agreements from $180 k to $10.4 M with supplementals
(one not yet in OASIS), one with no OASIS procurement document, one closed, one
municipal-sponsored; routing rules per district and division; and about 30
invoices across every status with deliberately planted problems — a contiguous
sequence, an over-ceiling invoice, a contract-ID mismatch, a split that ties and
one that does not, a previous-total mismatch, before-procurement-document cases —
plus the **real Michael Baker Invoice 1285907** pushed through the same
`create_from_upload()` path as a live upload. Event timestamps are back-dated with
a seeded random generator so aging reports render on day one.

### 15.1 Engineering import (real data)

`python -m app.seed.engineering [--reset-all]` (`app/seed/engineering/`) replaces the demo data
with WVDOT's real consultant history, read over the SSH tunnel from the **Engineering** SQL Server
database (`Consultants`, `Agreements`, `Supplements`, `Invoices`, `Invoices_Subcon`,
`AuthorizationData`, `Project_Managers`, `DDC_PM`) and **TheHub** (`Data-Warehouse`: `Project`,
`ProjectPhase`, `County`, `District`). It writes into the schema of §2 unchanged; the demo seed is
reused only for the login user, the seven `invoice_types`, and the routing rules whose org unit
exists. The pipeline is `source.py` (extract) → `mapping.py` (pure transforms, unit-tested in
`tests/test_engineering_mapping.py`) → `load.py` (ORM upserts) → `report.py` (reconciliation;
exit code 2 if a count or the invoice total does not tie). The same run resolves, for every Hub project, whether the warehouse's AWP tables carry a construction contract under its number and stamps `awp_contract_number` on `hub_projects` and on the portal's `projects` (`--sync-hub` re-stamps existing projects; resolution never happens at request time). It also refreshes the `hub_projects`
mirror (all ≈15,000 TheHub projects) for the intake wizard's Hub validation (§10);
`python -m app.seed.engineering --sync-hub` refreshes only that mirror. A full load is ~9,300 invoices in about
90 seconds and is idempotent: invoices are keyed by the Engineering `SQL_id` carried in the
`uploaded` event's `data` (`{"source": "Engineering.dbo.Invoices", "sql_id": N}`) and repeated in
the row's `notes` as `[eng:SQL_id=N]`.

**Source-data rules the importer applies (all verified against the live data):**

- *Agreement duplicate rows.* 189 agreement numbers have more than one `Agreements` row (194
  extra rows), 182 with different amounts and no version marker. One row per number is canonical —
  ranked by in-scope invoice count, then a non-NULL `Amnt`, then the larger `Amnt`, then the lower
  `SQL_id` — and every invoice and supplement is re-pointed to it through `MasterAgreementIndex`
  (the FK), not the free-text agreement number. Merged rows are listed in `agreements.notes`.
- *Invoice rows.* Only rows with an `Invoice_Amount` load (drafts have none); voided rows load as
  `withdrawn`; non-void exact duplicates on (consultant, invoice number, amount) collapse to the row
  with the most lifecycle dates. Near-duplicates such as `33142` / `33142 Final` are kept so the
  checks can surface them.
- *Org units* come from the OASIS unit code in `REC_ORG` (`DDNN`: `01`–`10` → `D01`–`D10`;
  `0060` → `ENG`, `0085` → `TRF`, `0061` → `ENV`, other `00NN` → `CO`); districts take the most
  common code for their prefix as `bf2_unit_code` (e.g. `0160`, `0858`, `1060`). Agreements
  without invoices fall back to `Procurement_Responsible_Group` (`DD-N` → district, `DD-0` →
  `D10`, `DDE` → `ENV`, everything else → `ENG`). Responsible parties are not known.
- *Invoice type* comes from the agreement's prequalification category (`Traffic…` → `TRF`;
  `NEPA` / `Natural Resource` / `Cultural Resource` / `Asbestos` → `ENV`; management support and
  railroad → `OTHER`; everything else → `ENG`).
- *Vendors* have **synthetic** OASIS numbers (`ENG` + the Engineering consultant number
  zero-padded to nine digits, e.g. `ENG000000140`) because the source holds none; the
  `compliance_note` says so. Firms that only ever appear as subconsultants are
  `is_subconsultant_only`. Workers'-comp dates are unknown and left blank. **Only 6 of the 263
  consultants have an office address in the source** and none has a remit-address id or a real
  OASIS vendor number — there is no such column anywhere in the Engineering database — so the BF-2
  ADDRESS and REMIT ADDRESS ID boxes are blank for the rest. The six are parsed from free text by
  peeling ZIP → state → city off the right (comma placement is inconsistent in every one).
- *Agreements.* `contract_id` is the Engineering agreement number (`2025130049-1-A`); the 10-digit Engineering `ProjectID` is the WVDOH project key (`projects.number`), never an agreement identifier.
  the ten-digit project number when the project has exactly one agreement (the shape the fixtures
  use); `program` is that same ten-digit WVDOH project number — the BF-2 PROGRAM box (§4.5 reads a
  ten-digit value there as a contract-id candidate, and it also fills the OASIS accounting line's
  program column); `oasis_doc_type/id` is the `PAG` purchase-agreement document when one is recorded;
  `original_amount` is the executed `Amnt` (falling back to the approved estimate, the proposal,
  or the invoice total); `agreement_date` is the first available of the execution, distribution,
  drafting, legal, NTP dates, else 30 days before the first invoice, else the project year;
  `status` is `closed` when the source says so, `pending` for never-executed agreements without
  invoices, else `active`. No real agreement spans more than one project, so all are
  `single_project`.
- *Supplementals* keep zero and negative (deductive) amounts, are renumbered when a number
  repeats, and get `oasis_entered_at` set to their distribution date — the source never records
  OASIS entry and leaving it empty would block every historical invoice.

**Status is derived** from the Engineering lifecycle dates, first match wins:

| # | Condition | Status |
|---|---|---|
| 1 | Voided (`Scanned_or_Void = VOID` or a void date) | `withdrawn` |
| 2 | A paid date (`Paid_Date` or `Paid_Date_AppXtender`) | `paid` |
| 3 | Marked scanned and dated before `--legacy-cutoff` (2025-01-01) | `paid` (inferred: imaged at payment) |
| 4 | Agreement closed and no activity for 90 days | `paid` (inferred: agreement closed) |
| 5 | Submitted to OASIS | `keyed` |
| 6 | Back from review / to auditing / in auditing | `approved` |
| 7 | Sent for review | `in_review` |
| 8 | Otherwise | `logged` (the Engineering row *is* the log entry) |
| 9 | Still open and no activity for `--infer-paid-after-days` (365; `0` disables) | `paid` (inferred: stale) |

Every inference is written to `notes` and to the `paid` event's `data` (`inferred: true`,
`source`). Stage stamps come from the matching source dates, are placed at 15:00 UTC so they read
as the right calendar day in Eastern time, and are forced into order (a handful of rows record
payment before receipt) and never into the future. One `invoice_events` row is written per stage
actually reached — legacy rows go `received → logged → paid`. Approval steps exist only where the
source shows a review, using the portal's routing rules; the reviewer's name (from `DDC_PM`) is the
`approved` event's actor and the project manager (from `Project_Managers`) is `responsible_party`.

**BF-2 fields.** The WVDOT USE block gets LOG IN from the received date, PREVIOUS IN from the
previous invoice's received date on the same agreement, APO from the OASIS purchase-agreement
number, UNIT from `REC_ORG` and SEQUENCE # from `SeqNum`; FUNCTION and ACT + N or P have no source
column and stay blank. `invoice_amount_previous` is the sum of earlier *approved/keyed/paid* invoices
on the agreement — the same definition `PREVIOUS_TOTAL_MISMATCH` uses, so imported history chains
cleanly. `pct_funds_expended_bf2` is the hand-keyed `Percent_on_BF2` as printed (blank when the
source has none). The ceiling fields count only supplements dated on or before the invoice. Work
periods are the source's `Work_Start`/`Work_End` (swapped when inverted); when the source has none
(about a third of rows) they are **derived** — period end = invoice date, start = the day after the
previous invoice's period — and `comments` says so (`--no-derive-periods` leaves them blank).
Subconsultant pass-through lines from `Invoices_Subcon` become `subconsultant` line items (they do
not sum to the invoice, so `LINE_ITEMS_SUM` warns). Deliberately blank: OASIS payment document
ids, warrant numbers (the source's `warrant_no` is a flag, its `PO_Number` a pre-2022 encumbrance
code kept in `notes`), extraction, and documents (no PDFs exist).

**Checks run inline, in chronological order**, exactly as a live intake would have seen them.
Expected results on the imported history: `AGREEMENT_INACTIVE` and `PROCUREMENT_DOC_MISSING` on
most pre-OASIS, closed agreements (nearly all on already-paid invoices), `DUPLICATE_INVOICE_NUMBER`
where vendors reuse `1`, `2`, `10` across agreements, `CEILING_EXCEEDED` on a few hundred
historical rows, and warnings for `PCT_FUNDS_EXPENDED`, `CEILING_NEAR`, `LINE_ITEMS_SUM`,
`PERIOD_OVERLAP`, `OUT_OF_SEQUENCE`. No BF-2 arithmetic or previous-total blocks are produced.

---

**Accounts.** Both seeds create the vendor-portal account: `seed_vendor_user` binds
`PORTAL_DEV_VENDOR_EMAIL` to the vendor found by `find_vendor_by_name` (the prime whose name starts
"Michael Baker"). `python -m app.seed.accounts` does only that (plus the staff account) against
any database without touching data. The importer's `reset_all` no longer truncates `vendors` with
`CASCADE` — Postgres would truncate `users` too through `users.vendor_id` — it deletes vendor rows
instead (the FK is SET NULL, so vendor accounts survive unlinked until the vendor is re-imported).

## 16. Provisional Assumptions & Open Questions

These are modelled as placeholders and marked as such in the UI.

| Area | What the app does today | Open question |
|---|---|---|
| OASIS payment document | `doc_type` defaults to `PRC`; accounting columns are fund / unit / activity / sub-activity / program / phase / task order. | Which document (GAX vs PRC) the payment really becomes, and its exact fields (open-questions B4/B5). |
| BF-2 unit → org unit | Districts use `0100`…`1000`, divisions `065x`; the wizard prefills from `wv_unit`. | Real unit numbers and whether the unit alone determines routing (A2). |
| Invoice types | Seven codes flagged `is_provisional`. | The real taxonomy (A1). |
| Approval chains | One rule per district/division with 2–3 generic steps. | Real responsible parties and delegation rules (C11–C12). |
| Sequencing | `OUT_OF_SEQUENCE` and `PERIOD_OVERLAP` warn; `PREVIOUS_TOTAL_MISMATCH` blocks only when the portal knows earlier invoices. | Whether the auditor's rule should hard-block (C15). |
| Email ingestion | Not implemented; invoices are uploaded in the app. | Mailbox access model (D17–D19). |
| Vendor portal | Consultant firms sign in with a vendor account WVDOT issues (one seeded: `mbi@wv.gov` → Michael Baker), see only their firm, upload and submit invoices, and follow the status timeline (§13.6). No self-registration, no e-mail notifications, no vendor contact channel yet. | Who issues and approves vendor accounts (open question #29), what notifications vendors should get (G31), the contact channel for certificate renewals and returned invoices. |
| Model-assisted analysis | Sonnet 5 classifies pages, finds identifiers with evidence, normalizes line items and suggests the type on every upload when a key is configured (mmsdev has one). | Data-handling approval for sending vendor packages (which include remittance details) to the API; back-catalog batch runs. |
| Users & roles | Two roles as a string column (`admin`, `vendor`); every staff account can do everything, so a first-time SSO arrival is provisioned straight onto `admin` (`PORTAL_OIDC_PROVISION_ROLE`). | Real staff roles — a `user_roles` table with org scopes and per-permission overrides — are still parked work. Until they land, least privilege for WVDOT staff is not enforceable; set `PORTAL_OIDC_AUTO_PROVISION=false` if only pre-approved accounts should get in. SSO itself shipped (§14.2, migration `0009_sso.py`). |
| Synthetic vendor numbers (import) | Vendors loaded from the Engineering DB carry `ENG` + consultant number as their OASIS vendor number, flagged in `compliance_note`; `VENDOR_NUMBER_MISMATCH` cannot fire against them. | The real OASIS vendor numbers and remit-address ids for the 263 consultants. |
| Inferred statuses (import) | Historical invoices without a payment date load as `paid` when scanned before 2025, on a closed agreement, or idle for a year (`--infer-paid-after-days`); the inference is recorded on the row and the `paid` event. | Whether finance wants those left open instead, and the true paid dates from OASIS. |
| Derived work periods (import) | About a third of imported invoices have no work period in the source; the importer derives one from the invoice date and says so in `comments`. | Whether the BF-2 packages on file carry the real periods. |
| Rate schedules | Rates live per agreement (firm × classification × period), read from the attached PDF after review or typed by hand; rate disagreements are **warnings**, never blocks (§3.1, §9.3). | Where WVDOT keeps its rate tables, who maintains them, and whether the app should enforce rates (open question #26). |
| WVDOT default rates | A `default_rates` table (classification + effective dates) is the fallback when an agreement has no rate; the demo seed loads three labelled placeholders; comparisons are informational only. | No WVDOT default schedule has been provided yet — its shape (per classification? per year? per district?) is a guess. |
| Classification matching | Spelling variants are normalized (`Level 3` ≡ `Level III`, `Admin` ≡ `Administrative`, `Survey Tech` ≡ `Surveyor Technician`); anything else needs a one-time alias on the agreement. | Whether WVDOT wants a controlled list of labor classifications instead of free text. |
| Shift differential columns | Treated as **full billing rates** for shift work (the printed values sit ~2% above the base rates). | Whether the schedule means an add-on to the base rate instead. |
| Premium time | Overtime, OT, Premium, Double and Holiday rows all price at the premium column. | Whether holiday and double time have their own rates. |
| TheHub validation | Project numbers shown during intake are looked up in a mirror of TheHub's project master; the result is a chip, never a block. Only 10-digit WVDOH keys can validate — the `1729999R2`-style ids on CEI split sheets read as "not in TheHub". | What those non-standard ids are (district task numbers? old-format keys?) and whether TheHub should be queried live instead of mirrored. |
| Contract term & caps | `term_start` / `end_date` plus supplemental `term_end`; caps are recorded and displayed. A **provisional** warn-only check (`PER_ASSIGNMENT_CAP_EXCEEDED`, §8) compares a `letter_agreement`'s ceiling to its master's per-assignment cap; the annual cap is not yet enforced. | Whether "$X per agreement per year" should be enforced, and on which year (calendar vs. fiscal), and whether the $2.5M/$7.5M "DUMMY" master caps are real (see the master → letter-agreement row below). |
| **Master → letter-agreement model** | The two-tier master → letter-agreement (assignment) structure (diagrammed in §2). The foundation is built (migration `0010`) and is **live for Engineering** (`EN`): `AgreementKind.letter_agreement`, a `parent_agreement_id` self-FK (`models/agreement.py`), a `division` field (`EN`/`CF`) with `(division, contract_id)` uniqueness, ceiling checks skipped for masters, assignments auto-allocating like `single_project` (`services/invoices.py::single_project_of`) and inheriting the master's rates in the estimate (`refresh_estimate`). **Provisional part — the Contract Administration lane (WVDOT code `CF`):** an importer (`seed/engineering/ca.py`, stamps `division="CF"`) builds masters then assignments two-pass, but **no CF data is loaded yet** and it is not wired into the runnable seed. See the in-app **CA agreements analysis** doc for the full study. | Confirm the `AgreementsCA` schema and the master↔assignment linkage; finish the incomplete file copy (SSD dropped); confirm whether the master caps are real not-to-exceeds before enforcing them; how CF invoices identify their lane for linkage. |
| AWP E&C percent | `EandCPercent` is one value per contract (13% or 19% for almost every contract that has one, 77% have none); what it expands and how it moves the phase amount is not confirmed. The tab shows it as the rate AWP recorded, with population context, never as a trend | `services/awp.py`, `AwpTab.tsx` |
| AWP live read | The AWP tab reads TheHub at request time over the SQL Server connection; a deployment without warehouse credentials or the SSH tunnel shows the resolved contract numbers and an "not reachable" notice | `services/awp.py` |

---

## 17. Versioning & Changelog

Versions are kept in `frontend/src/data/changelog.ts` (`FRONTEND_VERSION`,
`BACKEND_VERSION`) alongside three logs: a per-day **summary** in end-user
language, and detailed **frontend** and **backend** release logs with typed
entries (`added`, `changed`, `fixed`, `removed`). The Docs → Changelog page
renders them; the avatar menu's "System info" links there. Every change that
ships must add to the changelog and, when it touches anything described in this
document, update the matching section here (see the repository `CLAUDE.md`).

---

## 18. Conventions to Remember

- Money is `Decimal` on the server and integer cents in the browser; never do
  authoritative arithmetic in floating point.
- Field names on the wire are the backend schema names (`invoice_number`,
  `invoice_amount_current`, `wv_unit`, …); the frontend types mirror them exactly.
- Statuses are the ten strings in §2; the UI label for `on_hold` is "Issue".
- Every user action that changes an invoice produces an `invoice_events` row —
  if a screen shows a time, it came from the ledger.
- The BF-2 never carries the contract ID or the OASIS document ID; both are
  portal data.
- White "paper" surfaces are reserved for documents and report tables (the BF-2,
  the OASIS keying table, the aging matrix); everything else stays on the dark
  shell.
