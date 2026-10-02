# DOT-12 — Readiness Assessment for Federal-Aid Labor Documentation

**Date:** 2026-09-27
**Scope:** Whether DOT-12 labor records would hold up if FHWA, the OIG, or a Single Audit tested labor charges to federal-aid work (including Emergency Relief).
**Method:** Read-only review of the working tree at `dot12_elizabeth/` (backend, frontend, migrations, `oasis-bridge/`, in-app docs, and prior audit/remediation files). Nothing was modified. Findings come from five parallel area reviews. About a dozen of the highest-severity findings were then re-checked by hand against the code: B1, B3, C1, C2, C4, D2, A1, A4, and the chat and apply-template UI wiring.
**Not verified:** Production configuration (env vars, live `user_roles` rows, feature-flag states) and the deployed build. These are listed in [§9](#9-things-to-confirm-in-production).

---

## 1. Bottom line

FHWA does not certify timekeeping software. What gets tested is whether a sampled labor charge can be traced to an after-the-fact record of actual work, approved by an appropriate person, that has not been changed since, that covers the employee's whole day, and that reconciles to what payroll paid.

In that frame, DOT-12 has **the right skeleton**:

- per-employee, per-day, per-cost-line hours;
- full OASIS coding on every line;
- leave recorded on the same form as work;
- a submit → approve → HRM/FIN entry workflow with named signers and timestamps;
- server-side locks on the main edit path;
- SSO identity;
- a self-approval guard.

It is **not yet audit-defensible**. Six problems would each draw an audit finding:

1. **Approved or final time can still change.**
   - Three endpoints bypass the approval and pay-period locks: chat apply, apply-template, and enrich.
   - Reject has no state check, so it can un-approve a final form.
   - Submit can re-stamp the preparer on an approved form.
   - None of this leaves a record of what changed.
2. **Nothing records what was approved.**
   - Saves overwrite and hard-delete rows.
   - History is a coalesced "edited" event with no values.
   - Reopen and reject null out the signatures.
3. **Separation of duties has holes.**
   - A role without approval rights can approve through a hard-mode entry session.
   - Approvers can edit a submitted form, including their own hours, and then approve it.
   - Approvers can promote themselves to admin.
4. ~~No federal-aid or ER identifier on any charge~~. *Revised:* the TheHub program on each column carries this, because flood and ER work get their own TheHub programs. It is a live join, not a stored snapshot (see A1, now Low).
5. **No reconciliation to paid hours** and **no stable DOT-12 identifier in OASIS.** An auditor can trace only by employee + date + coding, done by hand.
6. **No retention policy or backup procedure** for labor records, and several ops scripts rewrite history without a trace.

Most of these are straightforward to fix. The list in [§8](#8-remediation-roadmap) is ordered so that fixing the P0 group alone would close most of what an auditor would write up.

---

## 2. The standard being measured against

This summary is from general knowledge of the Uniform Guidance and FHWA practice. Confirm specifics with WVDOT's federal-aid finance staff or the FHWA WV Division office.

| Source | What it requires of a time system |
|---|---|
| **2 CFR 200.430(i)** — documentation of personnel expenses | Charges supported by internal controls that give reasonable assurance they are accurate, allowable and properly allocated. The records must also: be incorporated into official records; cover **100 % of compensated activity**; support distribution across cost objectives; and reflect **actual work after the fact**, with budget estimates allowed only as interim figures that are later trued up. |
| **2 CFR 200.303** — internal controls | Effective controls over federal awards: segregation of duties, authorization, and safeguarding of records. |
| **2 CFR 200.334–.336** — record retention and access | Keep records generally 3 years from the final expenditure report (for FHWA, the final voucher), longer if an audit or litigation is open. Electronic records are acceptable. Auditors must be able to access them. |
| **2 CFR 200 Subpart F** — Single Audit | The state auditor tests payroll charged to the Highway Planning & Construction cluster every year. |
| **FHWA oversight** | Division office FIRE reviews and improper-payment sampling: pick billed transactions, then demand the timesheets behind the labor. |
| **FHWA Emergency Relief** (23 CFR 668) | State force-account labor on disaster repairs must be documented by site and event and tie to the damage inspection report. For WV flood events this is the most likely place DOT-12 would be examined line by line. |

---

## 3. Where DOT-12 sits in the payroll chain today

This matters because it decides **what an auditor would treat as the source document**.

```
Crew supervisor ─► DOT-12 form (daily, per crew)
                     │  submit → approve (DOT-12)
                     ▼
Timekeeper ─► Timesheet Accounting / Entry Session screen (DOT-12)
                     │  re-keys hours by hand
                     ▼
               wvOASIS HRM / Time I  ◄── system of record for PAID time
                     │
                     ▼
               OASIS cost accounting (PREXP/TIMEI) ─► FHWA billing
```

- **DOT-12 is the upstream source document, not the payroll system of record.**
  - Hours are keyed into OASIS by hand (`routes/entry_sessions.py:1-18`; `flask_models.py:2504-2512`; `WVOASIS_INTEGRATION_PROPOSAL.md:11`).
  - The timekeeper clicks **Enter HRM**, or confirms each employee-day in an entry session. That is the only record that keying happened.
- **The TADJ nightly export is built but inert.**
  - The scheduler runs, but `TADJ_EXPORT_UNITS` is empty, so it does nothing (`jobs/tadj_export.py:83-86, 554-557`).
  - The interface is marked "PROPOSED — not yet confirmed with the State / wvOASIS" (`dot12-frontend/src/docs/tadj-interface.md:3-5`).
  - Delivery is disk-only; SFTP is deferred (`jobs/delivery.py:1-17`).
- **oasis-bridge is dev-only.**
  - It has only run against UAT/IST, and only for material OC documents.
  - HRM timesheet posting is entirely stubbed (`oasis-bridge/src/oasis_bridge/pages/hrm/timesheet.py:30-62`).
  - DOT-12 has `BRIDGE_ENABLED=false` (`app.py:236`).

**What this means for an audit:**

- DOT-12 will be treated as the timesheet: the thing that proves the work happened and was approved.
- The OASIS keying step is a second control point, and today it has **no stored evidence of what was keyed**.
- Every gap below matters **more** once TADJ or the bridge goes live, because then DOT-12 content flows into payroll with no human re-keying in between.

---

## 4. Scorecard

| # | Requirement an auditor will test | Status | One-line reason |
|---|---|---|---|
| 1 | Hours by person / date / cost line | 🟢 Meets | `dot12_employee_charges` at employee × column grain, with the date on the form |
| 2 | Full accounting coding per line | 🟢 Meets | Activity, sub-activity, P/N, program, phase, task order, LDPR, unit, account code on `dot12_task_assets` |
| 3 | Federal-aid project / ER event identifiable per charge | 🟢 Mostly meets | `program` + `phase` = TheHub project/phase → FederalProjectNo, disaster number, DI line; a live join, not snapshotted |
| 4 | Total activity (100 % of the day) | 🟠 Partial | Leave and non-project time go on the same form, but nothing checks a person's full day or catches duplicates across forms |
| 5 | After-the-fact, not estimates | 🟠 Partial | Future dates accepted server-side; Copy Form clones hours; AI chat nudges "everyone 8"; no provenance recorded |
| 6 | Supervisory approval with identity and time | 🟢 Mostly meets | `approved_by` / `approved_at` stored server-side; approve requires `can_approve` + org write |
| 7 | Segregation of duties | 🔴 Gap | Approver can edit then approve; approver → admin self-escalation; admin self-approval. The hard-mode approval gap was fixed 2026-09-27. |
| 8 | Approved records protected | 🟠 Partial | Lock-bypass endpoints fixed 2026-09-27; reject/submit still have no state check |
| 9 | Change audit trail (who / when / old → new / why) | 🟢 Mostly meets (2026-09-27) — no "why" yet | No field-level history; edits coalesced; child rows hard-deleted; no reason on recall/reopen |
| 10 | Reconciles to paid hours | 🔴 Gap | No automated or stored reconciliation; one ad-hoc D7 run with no artifacts |
| 11 | Traceable from billed cost to source record | 🟠 Partial | Works by employee + date + coding only; no DOT-12 id in OASIS; `timei_document_id` never populated |
| 12 | Payroll feed only from approved time | 🔴 Gap (latent) | TADJ and entry-session eligibility include draft, submitted and rejected forms; latent until TADJ is live |
| 13 | Access control and unique identity | 🟢 / 🟠 | SSO is solid; no deprovisioning, no session revocation, no access review; PIN (not in prod) is weak |
| 14 | Retention ≥ 3 yrs after final voucher, retrievable | 🔴 Gap | No policy, no documented backups; logs 30 d; analytics 180 d; export ledger replaced nightly |
| 15 | Controls documented accurately | 🟠 Partial | Several in-app docs contradict the code (§7) |

---

## 5. Findings by area

Severity reflects how an auditor would likely treat the finding, **given production as it is today** (manual OASIS keying, TADJ and bridge off, chat panel not in the UI). Where a finding gets worse when an integration goes live, that is noted.

Unless shown otherwise, paths are relative to `dot12-backend/`. `FE/` means `dot12-frontend/src/`.

### 5.A Time capture and coding

#### A1 — Federal-aid / ER identity is carried by the TheHub program, not stored on the charge · **Low** (revised 2026-09-27)

> **Revised.** The original rating (High, "no identifier") missed that `program` **is** the TheHub project number (`dot12_task_assets.program` / `hub_project_number`, `flask_models.py:373, 382`; `FE/docs/dot12-logic.md:3448`). WVDOT sets up flood and disaster work as **its own TheHub programs**. `validated_program_phase_funding.csv` has 29 flood rows, e.g. `NATDIS 2022100028 "FAYETTE COUNTY AUG 14-15, 2022 FLOOD"` and `NATDIS 2024870011 "D7 OVERHEAD COST - APRIL 11 FLOOD EVENT"`.

**How the trace works.** Each charge's column carries `program` + `phase`. That key resolves in TheHub to:
- `ProjectPhase.FederalProjectNo` and `IsFederalProject`;
- `PhaseFunding.FederalProgram` and `FederalParticipationPercent`;
- `Project.ProjectDisasterNumber` (e.g. `DR-4783`) and `ProjectDILineItemNo` (the damage-inspection line), per `HUB_SCHEMA.md:176, 185, 199`.

So each charge **can** be tied to a federal project, a disaster declaration and a DI line through a join. That is how an ER claim would be assembled. The disaster tag on the form isn't needed for this, and shouldn't be relied on: it is free text, form-level, and can be edited after approval (`routes/tags.py:197-266`).

**What's left (minor):**
- **The identity is a live lookup, not a snapshot.**
  - DOT-12 reads `FederalProjectNo` from TheHub (`routes/hub.py:406-411, 532`) but doesn't save it.
  - TheHub has no system-versioning (`HUB_SCHEMA.md:43`), so a later change to a phase's federal number or funding can't be shown "as of" the work date from TheHub alone. Its change-request tables give partial history.
  - Freezing `federal_project_no`, the disaster number and the DI line on the column at approval would make the record self-contained. This is optional.
- **It depends on crews coding the right program.** Emergency work done before a flood program is set up in TheHub, or coded to a routine maintenance program, won't join. That is a business-process question, not a code one (see [§9](#9-things-to-confirm-in-production)).
- `program` can still change after approval through the lock-bypass paths (C1). This is covered there.

#### A2 — No total-activity or duplicate-day checks · **Medium**

- **Leave is on the same record as work** — good. It is a column with a leave LDPR code.
- **No stored per-employee daily total,** and no check that a person's hours across **all forms and units** match their scheduled or paid hours.
  - The only cap is a frontend, non-blocking per-form sum above 24 (`FE/utils/validation.ts:157-175`).
  - The backend accepts negative hours and hours above 24. There is no `CHECK` on `hours_charged`.
- **No duplicate-person or overlapping-hours check across forms.** The same person can appear on two forms for the same day with a combined 16 h.
- The Org View matrix is scoped to one `home_unit` (`routes/reports.py:151`), so time a person worked on another unit's form is not combined.
- `wv_holidays.py` is used only for leave requests, not DOT-12 validation.

#### A3 — "After the fact" is not enforced, and data origin isn't recorded · **Medium**

- **Future dates:**
  - `create_form` requires only `form_date` and `home_unit` (`services.py:618-621`). Submit and approve don't compare the date to today.
  - The only guard is a frontend warning when a form is dated in a future **pay period** (`FE/utils/pay-period.ts:98-118`). A future date inside the current pay period gets no warning.
  - For comparison, pre-trip inspections do reject future dates (`routes/pretrip.py:146-147`).
- **Copy Form** clones **every hour, quantity and code** to a new date (`FE/utils/copy-form.ts:69-107`). The new form is logged as a plain `create` event, with no record of what it was copied from.
- **AI chat:**
  - The system prompt says "BIAS TO ACTION … Don't ask for confirmation" (`chat_service.py:605`).
  - It suggests "everyone 8 hours" (`:450-452`) and equipment hours = labor hours.
  - The chat panel is **not currently mounted anywhere in the frontend.** `ChatPanel.tsx` is defined but never rendered, so today this path is reachable only by calling the API directly.
- **OCR import** (`POST /forms/import-pdf`):
  - It creates forms with hours straight from a scanned paper form.
  - No `created_by_user_id` and no `create` event are recorded.
  - Uncertainty warnings are returned but not saved.
  - The uploader is taken from a client-supplied header (`routes/forms.py:1046-1047`).
  - No frontend caller exists; the route is API-only.
- **Leave requests** create draft DOT-12s for future leave days, defaulting to 8.00 h (`leave_service.py:38, 200-206`). That is legitimate for approved leave, but the resulting DOT-12 hours are pre-entered, not after the fact.
- **No provenance on the record:** nothing on a charge says typed, copied, OCR or AI.

#### A4 — Leave misclassified as regular time on the export · **Medium (latent)**

- `timesheet_lines.LEAVE_CODES = {'SCKLV','ANNLV','FMSUS','HOLLD','BRVUS'}` (`timesheet_lines.py:23`). It is missing `JURYL`, `MLVPA` and `MLVPB`, which `leave_codes.py` and the UI treat as leave.
- The effect: jury and military leave would export as event `REG`, with the leave code sitting in the LDPR field.
- Chat-entered leave would default the LDPR to `17237` and be classified as REG maintenance time (`chat_service.py:635, 1828, 1856`).
- It is latent because TADJ is not live. It **does** affect the Timesheet Accounting screen that timekeepers key from.

#### A5 — Validation is advisory and client-side · **Medium**

- Coding cascades, the hour caps, temporary-upgrade eligibility and the meter/operator checks all run only in the browser.
- The doc states it directly: validations "never block save" (`FE/docs/dot12-logic.md` §7).
- The only server-side check at submit is the pay-period shape (`services.py:143-167`).
- Sample exports contain REG rows with a **blank task order** and rows with a blank unit or program (`dot12-frontend/public/sample-data/HRM_TADJ_REFRESH_0711_20260612.csv`; root `HRM_TADJ_REFRESH_0711_20260605.csv`).
- `validated_program_phase_funding.csv` and `validated_combinations.csv` are not used by any runtime code.

#### A6 — Smaller data-model issues · **Low**

- **Hour precision:** hours are stored at 0.01 h (`NUMERIC(5,2)`) while leave uses quarter-hours, and export sums are rounded as floats (`tadj_export.py:218`).
- **Equipment "operator" is inferred, not recorded.** On the export it is the employee with the most hours on the same line that day (`timesheet_lines.py:187-222`). The recorded `operator_initials` field is not exported.
- **Unpadded `oasis_id` on update:** create does `zfill(10)` (`services.py:688`) but update doesn't (`:910-911`). One employee can then appear under two IDs.

### 5.B Approval and segregation of duties

#### B1 — Hard-mode entry sessions approve without approval authority · **Critical** → ✅ fixed 2026-09-27 (uncommitted)

> **Status:** `_apply_hard_workflow` no longer approves. It HRM-enters only forms that are already approved, and skips unapproved ones (`not_approved` in the summary). This applies to every role, admin included. The org-**view** gate on session routes is unchanged and is still open (see P0 #3). The description below is kept as found.


- Entry sessions are restricted to `time_entry_approval` and `admin` (`routes/entry_sessions.py:55-56`). Scope is checked with **org view** only (`:124, :271`).
- Migration 016 deliberately removed `can_approve` from `time_entry_approval` (`migrations/016_realign_entry_roles.sql:17-18`).
- `_apply_hard_workflow` calls `apply_approve(form, user)` and then `apply_enter_hrm(form, user)` (`entry_sessions.py:480-483`). There is no `can_approve` check.
- `apply_approve` documents that "callers are responsible for the permission/eligibility guards" (`routes/workflow.py:30-33`).
- The event log records a plain `approve`, indistinguishable from a supervisor's approval.
- **This is a designed, visible feature, not hidden code.**
  - The Start Entry Session modal offers Soft/Hard (`FE/components/StartEntrySessionModal.tsx:84`).
  - The Complete dialog says fully-entered forms "get approved & HRM-entered" (`FE/pages/TimesheetAccounting.tsx:1320-1326`).
  - The changelog describes it too (`FE/data/changelog.ts:333`).
  - The problem is that it contradicts the role split in migration 016 and puts approve and post in the same hands.
- **Net effect:** a timekeeper can approve crew time and certify it as keyed at the Complete step of a hard session. The role design says that timekeeper cannot approve, and the server only requires them to be able to view the org.
  - **What drives the approval:** the timekeeper's per-employee "entered in OASIS" confirmations, not a review of the form's content.
  - **What limits it:** only submitted forms are approved (drafts and rejected forms are skipped), and the timekeeper's own submissions are skipped unless they are admin.

#### B2 — Approver can change content, then approve it · **High**

- A **submitted** form stays fully editable through `PUT` (the lock starts at `approved_by`; `routes/forms.py:1137`). Editing does not clear `prepared_by`.
- The separation-of-duties check compares only against `prepared_by`, meaning whoever last clicked Submit (`workflow.py:166-169`).
- So an approver can:
  - change hours on a colleague's submitted form, **including their own hours if they are on the crew**, and then approve it; or
  - have someone else click Submit on a form the approver wrote. Submit has no state check (below).
- There is **no check that the approver is not an employee on the form** (`users.labor_code` vs `dot12_employees.oasis_id`).
- **Admins may approve their own forms** (`workflow.py:166-169`). This is not flagged in the event log, unlike leave requests, which record "Self-approved (admin)".

#### B3 — Approvers can escalate to admin · **High** (confirm in prod)

> **Fixed 2026-09-27 (uncommitted):** approver `can_edit_user` is now set to FALSE by migration 044 and a startup realignment, and has already been applied to local `dot12_test`. The code-level guard (only admins may change role, e-number or email, and nobody their own) is still open.
>
> **Checked 2026-09-27 on local `dot12_test` (localhost:5435):** `approver` has `can_approve = t`, `can_view_user = t`, **`can_edit_user = t`**, so migration 008's grant is present there. The local `dot12` database's `user_roles` table is empty. Production (10.0.1.229) is still unverified.


- Migration 008 grants the `approver` role `can_edit_user = TRUE` (`migrations/008_expand_role_permissions.sql:14-19`).
- `PUT /users/<id>` lets any `can_edit_user` holder set **any** user's `role_id`, including their own, with no guard (`routes/users.py:197-220`).
- The same route can change another user's `e_number` or email. SAML matches on those, so this redirects whose SSO login lands on that row (`saml_routes.py:385-410`).
- Role changes are written only to the application log (`users.py:294`). There is no audit table.
- The docs disagree about whether approvers can edit users (§7). **Check the live `user_roles` row.**

#### B4 — Approval is scoped by org, not supervisory relationship · **Medium**

- Any approver with write access to the org can approve any of its forms. The supervisor chain is not used for DOT-12 approval (`FE/docs/dot12-logic.md` ~1231-1237).
- `FE/docs/USER_PERMISSIONS.md:126-139` still says it is.
- Crew members never confirm their own hours; the supervisor enters them on their behalf. That is normal for DOT daily reports, but an auditor will want the approver to be someone with first-hand knowledge.

#### B5 — The "signature" is display-only · **Medium**

- The approval signature is the approver's name rendered in their chosen font, read **live** from the current `users` row (`services.py:94-105`; `FE/utils/signature-block.ts:27-43`). A later name change alters how past signatures display.
- The "I certify…" text is a client-side checkbox only (`FE/components/SignatureConfirmModal.tsx:39-40, 247-248`). The approve POST has no body.
- No attestation text, re-authentication or hash of the approved content is stored.

### 5.C Protection of approved records

#### C1 — Lock-bypass write endpoints (SEC-05) · **Critical** → ✅ fixed 2026-09-27 (uncommitted)

> **Status:**
> - `chat/apply-actions` has been removed.
> - `apply-template` now returns 403 once the form is approved or its pay period has locked.
> - `enrich` now returns 403 once the form is approved.
>
> Tags are still not lock-gated. Only `PUT` records an edit event. The table below is kept as found.


The main `PUT /forms/<id>` correctly refuses edits once a form is approved or its pay period has locked. Three other endpoints do not check either lock, and **none records a form event or `updated_by`**:

| Endpoint | What it can change | Role check | In the UI today? |
|---|---|---|---|
| `POST /forms/<id>/chat/apply-actions` (`routes/chat.py:76-104` → `chat_service.py:1739-1787`) | Employee hours; activity, program, phase, LDPR, task order; header including `home_unit` and `form_date`; add or delete employees and columns. Applies **whatever actions the client sends** (SEC-06). | None | No. ChatPanel is not mounted, so API only. |
| `POST /forms/<id>/apply-template/<tid>` (`routes/templates.py:448-503`) | Deletes all employees, equipment and materials; their charges go with them via `ON DELETE CASCADE` | None | Yes. It is hidden when the form is locked (`FE/pages/DOT12Detail.tsx:3639`), but the **server** does not enforce that. |
| `POST /forms/<id>/enrich` (`routes/forms.py:1084-1105`) | Rewrites program and phase | `can_create_edit_form` | Not found in the UI |

- The only server check on these paths is org-edit middleware (`utils/auth.py:344-379`).
- This was reported as **SEC-05 (High)** in `SECURITY_AUDIT_2026-09-09.md:156-170`. The remediation deliberately left it open: "reaching approved and closed-period forms is intended behavior per the project owner" (`security-remediation-2026-09-09/verify_fixes.py:8-11`).
- `FE/docs/dot12-logic.md:667-673` says no bypass exists.
- **Why this is critical for federal purposes:** it means "approved" does not mean "unchanged since approval", and there is no record that would reveal a change. An auditor who finds even one such path will usually expand testing, or decline to rely on the approval control.
- **Recommendation:** revisit the SEC-05 decision. The shared mutation guard that was built and reverted is the fix.

#### C2 — Reject and submit have no state check · **High**

- **Reject** (`workflow.py:180-212`) checks role, org and preparer, but **not the form's state**.
  - An approver can reject an approved, HRM-entered, or **final** form, even after the pay-period lock.
  - That clears `prepared_by` and `approved_by` but leaves `entered_by_hrm` and `entered_by_fin` set (`workflow.py:79-88`).
  - Result: an inconsistent "rejected but entered" form.
  - It works as an undocumented way to un-approve.
- **Submit** (`workflow.py:98-137`) doesn't check state either. It re-stamps `prepared_by` / `prepared_at` on an already-approved form, changing who the record says prepared it.
- The UI shows these buttons only in the right states (`FE/components/Header.tsx:448, 458`). The server does not enforce it.

#### C3 — Reopen after OASIS entry · **Medium**

- `reopen` clears **all four** signatures, including `entered_by_hrm` and `entered_by_fin`. It is allowed for the creator, an admin, or any entry role until pay-period end + 7 days (`workflow.py:282-352`; `services.py:109-138`).
- Nothing checks or flags that the hours were already keyed into OASIS. Neither recall nor reopen captures a reason.
- A reopened form can then be archived, which removes its hours from reports and from any future export.
- `PERMISSION_CHANGES.md` says reopen is creator-only; the code also allows entry roles.

#### C4 — Approval isn't a precondition for the payroll feed · **High (latent) / Medium today**

- `timesheet_lines.query_charge_rows` filters only `NOT f.is_archived` (`timesheet_lines.py:59`). Draft, submitted and **rejected** forms therefore feed:
  - the Timesheet Accounting screen timekeepers key from;
  - entry-session eligibility;
  - the TADJ export.
- Reports default `approved_only` to off (`routes/reports.py:116-124`).
- Today a human timekeeper sits in between, and the session flow approves or rejects touched forms. Once TADJ is live, unapproved hours would reach OASIS automatically.

### 5.D Audit trail and change history

#### D1 — No record of old → new values · **Critical** → ✅ fixed 2026-09-27 (uncommitted)

> **Status:** `dot12_audit_log` is now filled by Postgres triggers on every labor table. It covers ORM saves, bulk deletes, cascades, ops scripts and psql. Each row holds `{column: [old, new]}` plus the user, source and request, and the table is append-only. The History tab's **Show changes** reads it. The description below is kept as found.


- A save **updates child rows in place and hard-deletes rows that were removed** (`services.py:887-891, 966-970, 1047-1051, 1161-1165`; charges at `:1287, :1299-1303`). This covers employees, equipment, materials, task assets and charges.
- Every charge foreign key is `ON DELETE CASCADE` (`migrations/000_full_schema.sql:111-112, 123-124, 135-136`).
- Only `dot12_forms` has `created_by`, `updated_by` and timestamps; employee, task-asset and charge rows have none.
- There are **no audit or history tables, no triggers, and no row versioning.** The only trigger in the schema updates `tags.updated_at`.
- **Consequence:** a prior hours value, a removed employee, or a changed task order **cannot be recovered** from the database. There is no way to show an auditor what the form looked like when it was approved.

#### D2 — The event log is thin and coalesced · **High** → ✅ fixed 2026-09-27 (uncommitted)

> **Status:** every save is now its own event (`is_autosave`, `request_id`, `source`), and runs of autosaves are merged only for display. Writes that no event explains show up as *data change* entries. The description below is kept as found.


- `dot12_form_events` stores `(form_id, user_id, event_type, description, occurrence_count, created_at)` (`flask_models.py:1387-1414`).
- **Consecutive edits by the same user collapse into one row.** The timestamp is moved forward and a counter is incremented (`services.py:186-197`), so the time of the first edit in a run is lost.
- `description` is filled in only for rejection reasons and leave links. No field names, values or edit reasons are stored.
- Events are `ON DELETE CASCADE` with the form.
- Alternate writers (chat, template, OCR, tags) write **no event at all** (OBS-05).

#### D3 — Entry-session confirmations store status, not content · **Medium**

- `dot12_entry_confirmations` records "entered" or "failed" per (unit, oasis_id, date), plus who and when (`flask_models.py:2557-2600`). It does **not** store the hours or coding that were keyed.
- A deny overwrites an existing row in place (`entry_sessions.py:329-338`).
- A later edit to the form does not invalidate a sticky "entered" confirmation (`entry_sessions.py:277-306`).
- Accounting overrides at entry time record free text and a line count only.

#### D4 — Logs are not an audit trail · **Medium**

- `requests.log` records who, endpoint, time and status only: no bodies or values (`app.py:514-553`).
  - Rotation is 30 days (`utils/file_logging.py:51, 83-94`).
  - Health and static paths are skipped.
  - One hardcoded account (e029568) is **excluded from request and error logs** (`app.py:526-529, 558-561`).
  - Operationally the log is lossy: about 19 % of Apache's request volume was retained in Aug–Sep 2026, because each gunicorn worker rotates its own handle.
- The analytics `user_events` table is purged after 180 days (`jobs/analytics_retention.py:36-47`).
- Neither of these should be presented as the change history. D1 and D2 need to be fixed in the database.

#### D5 — Ops scripts rewrite history without a trace · **High**

| Script | What it does |
|---|---|
| `reimport_0206.py:48`, `reimport_0471.py:82`, `reimport_0880.py:91` | Hard-delete every form for an org and date (cascading charges and events), then re-create the forms by OCR under user id 1. New form ids are assigned. |
| `apply_dot12_backup.py:27-41, 103-126` | Deletes all child rows **and `dot12_form_events`** for each form in a dump, then overwrites from the dump. |
| `dedup_employees.py:126-188` | Rewrites `oasis_id` and names on **every** `dot12_employees` row for an org, including approved and HRM-entered forms. No event is written and `updated_at` is not bumped. |

None of these writes an event, sets `updated_by`, or keeps a before-image. Their only record is stdout.

### 5.E Payroll trace and reconciliation

#### E1 — No reconciliation of DOT-12 to paid hours · **High**

- No automated or stored comparison of DOT-12 hours against OASIS HRM, PREXP/TIMEI or dTIMS `LaborTransaction`.
- The bridge's read-back and reconcile steps are stubbed (`oasis-bridge/src/oasis_bridge/reconcile/readback.py:23, 29`).
- The per-pay-period sum check exists only as a plan (`WVOASIS_INTEGRATION_IMPLEMENTATION_PLAN.md:668-673`).
- **One ad-hoc D7 reconciliation** was run (window 7/1–8/5/2026):
  - On shared (task order, date, employee) cells, hours matched to within +0.01 %: 98 % of cells matched exactly, r = 0.986.
  - The raw gap was +40 %. It was explained by out-of-district mutual-aid crews (~19 %), pre-go-live days (~14 %), and about 1.7 k hours not yet keyed.
  - That is a **strong result**, but no scripts or outputs were kept in the repo.
- `validate_tadj_export.py` checks only that the export conserves DOT-12 hours. It never compares against OASIS.

#### E2 — No stable DOT-12 identifier reaches OASIS · **Medium**

- The labor export groups by `(oasis_id, date, event, ldpr, acct, unit, activity, sub_activity, program, phase, task_order)` and drops `form_id` (`jobs/tadj_export.py:195-199`; `timesheet_lines.py:36`). The XML leaves `DOC_ID` blank (`jobs/serializers.py:103-113`).
- `dot12_employee_charges.timei_document_id` exists but **nothing ever populates it**.
- OASIS PREXP rolls labor up by program and phase and "appears to use the first [task order]" (`oasis_equipment_payroll_mechanics.md:224-236`). So a cost line may not carry the task order needed to trace back.
- **Materials are the exception:** `oc_doc_id` is stored per material, and the OC `doc_name` embeds `(DOT-12 #form_id)`.

#### E3 — Nothing keeps a copy of what was sent to payroll · **Medium (latent)**

- The TADJ line ledgers keep only the latest run and are replaced nightly (`tadj_export.py:400-402, 472-474`).
- Export files are date-stamped per day, so a same-day rerun overwrites them. They sit in `static/tadj_exports` inside the container, with no retention policy.
- `dot12_oasis_postings` stores a hash, not the payload. The bridge's own DB does keep full envelopes plus append-only `posting_events`.
- Duplicate protection depends on fixing the **5× scheduler problem**: each gunicorn process starts APScheduler, so 5 writers would share one file and ledger. There is no ack or reject handling and no retry sweep. The bridge callback is unauthenticated (`routes/oasis_postings.py:152-156`).

#### E4 — The Timesheet Accounting report as reconciliation evidence · **Partial**

- **Good:** it shows each employee's lines for a pay period at the HRM timesheet grain, with `form_refs_by_date` linking every cell back to DOT-12 forms (`routes/reports.py:1458-1680`). It uses the same query as the export, so the two cannot drift.
- **Limits:**
  - It is a live query, never snapshotted.
  - It includes unapproved forms (C4) and shows no approval state per line.
  - It has no OASIS-side column.
- With a snapshot at entry time and an OASIS column, it would become the reconciliation artifact.

### 5.F Access control and identity

#### F1 — What's solid

- **SAML SSO** against WV AD FS / Entra is the only production web sign-in (`routes/saml_routes.py:106-112`).
- The dev identity header and the shared dev password are refused in PROD/TEST, and startup fails on a bad environment value (`utils/environment.py:59-81, 93-137`). This was fixed and verified as SEC-03.
- The mobile code exchange is single-use, 120 s, hash-only (`utils/mobile_auth.py`).
- Workflow signers are server-derived user ids, not client-supplied.

#### F2 — Gaps · **Medium**

- **No deprovisioning:**
  - There is no `users.is_active`. Hard delete is blocked by foreign keys for anyone who ever signed a form.
  - SSO sessions cannot be revoked (SEC-16, Open); sessions last up to 6 h web and 24 h mobile.
  - Just-in-time provisioning admits any account the IdP accepts, as `viewer` with no orgs.
- **No periodic access review** was found.
- **Role and org grants are sometimes made by direct prod SQL,** which leaves no in-app trail.
- **Open protocol issues:**
  - SEC-13: no SAML request binding or replay store.
  - SEC-10: CORS accepts any origin with credentials, and there is no CSRF protection.
  - SEC-15: forms with a blank `home_unit` are open to every signed-in user.
- **PIN sign-in** (behind a flag, **not in prod**):
  - It uses a 4-digit PIN with trust-on-first-use enrollment. The first person to pick a never-enrolled name sets that name's PIN.
  - The `employee` role has no form rights, which is fine. But a PIN user promoted to a form-writing role would be signing payroll records behind a weak credential.

### 5.G Retention, backup and records management

#### G1 — No retention policy or documented backup for labor records · **High** → ✅ addressed 2026-09-27

> **Status:**
> - **Retention policy:** labor records are kept a minimum of **5 years** (documented in `dot12-logic.md` §22.1).
> - **Backups:** a nightly `pg_dump` at 2:00 AM ET is streamed to OCI Object Storage (`mms_bucket/dot12-db-backups/`). The newest 30 dailies are kept, plus a monthly copy at least 30 days apart that is kept forever. It runs on production only (`jobs/db_backup.py`, §22.2), and there is a host setup script.
> - **Still open:** restore drills, and records holds for open audits and claims (a process item).


- There is no retention rule, purge policy or legal-hold concept for forms, charges, exports or media. There is also no reference to 2 CFR 200.334.
- There is no backup procedure in the repo (searched for pg_dump, pgbackrest, wal-g, cron). The only artifact is the ad-hoc `gen_dot12_backup.py`, which keys on `updated_at` date.
- The database is the shared Postgres at 10.0.1.229, which also hosts MMS. Its backup regime needs to be documented and shown to meet the retention period.
- The related MMS inbound OASIS archive (not DOT-12) was bulk-purged on 2026-09-01 (116.9 GB). Some `job_run_artifact` rows now point at missing files. That shows the organization currently has **no records-retention guardrail** on payroll-adjacent files.

#### G2 — Timestamps · **Low**

- Timestamps are naive UTC in `TIMESTAMP` columns (no time zone), locks are computed in ET, and some tables default to database `NOW()`.
- These are consistent only if the database session time zone is UTC. Nothing in the repo guarantees that.

---

## 6. What's already strong

Credit where it's due. These are the things an auditor would view favorably, and they should be kept.

- **The grain is right.** Daily, per-person, per-cost-line hours with full OASIS coding. This is exactly the shape 2 CFR 200.430(i) needs for distributing time across cost objectives.
- **Leave sits on the same form as work**, so total activity *can* be demonstrated.
- **Main edit path is locked server-side:**
  - `PUT /forms/<id>` refuses edits after approval, with a narrow OC-doc-id carve-out for entry roles.
  - It refuses all edits after pay-period end + 7 days, evaluated in ET (`routes/forms.py:1130-1154`; `services.py:109-138`).
- **Approval is server-enforced** with `can_approve` + org write + a self-approval block, and records the approver's user id and UTC timestamp.
- **Form archive is soft delete.** It is blocked for approved and locked forms, restore is admin-only, and both are evented. No API hard-deletes a form.
- **Coding comes from systems of record** (DTIMS, TheHub, BS95 crosswalk) through picker cascades, not free text.
- **SSO identity with environment-bound dev bypasses.** Fixed and verified in the 2026-09-09 remediation.
- **The one reconciliation run was excellent:** a 0.01 % variance on shared cells. The system produces accurate data; what's missing is *proof* that it stays accurate.
- **The Timesheet Accounting report links every hour cell back to its source form(s).** This is most of a trace tool already.

---

## 7. Documentation that contradicts the code

An auditor building a control narrative from the in-app docs would get it wrong. These need fixing under the project's docs-in-sync rule, whichever way each finding is resolved.

| Doc | Says | Code does |
|---|---|---|
| `FE/docs/dot12-logic.md:667-673` | No path bypasses the approval lock | Chat apply, apply-template and enrich bypass it (C1) |
| `FE/docs/dot12-logic.md` §10.2 (~4476-4483) | Chat Accept applies "via the normal save path" | It calls `apply_form_actions` directly, with no locks and no event |
| `FE/docs/dot12-logic.md` ~1027-1028 | `time_entry_approval` cannot approve | It can, through a hard-mode session (B1) |
| `FE/docs/USER_PERMISSIONS.md:126-139` | Approval follows the supervisor chain | Approval is scoped by org write access only |
| `FE/docs/USER_PERMISSIONS.md:30` vs `dot12-logic.md:1059` vs `:1164-1165` | Conflicting answers on who can edit users | Migration 008 grants approvers `can_edit_user` |
| `PERMISSION_CHANGES.md` ~46-58, 104-113 | Reopen is creator-only | Creator, admin, or any entry role |
| `FE/docs/dot12-logic.md:1312-1333` | Sliding idle sessions, `touch_session`, 12 h prod | The working copy uses absolute lifetimes (6 h / 24 h / 4 h), and `touch_session` does not exist. The deployed build may differ. |

---

## 8. Remediation roadmap

Effort: **S** ≈ under a day, **M** ≈ a few days, **L** ≈ a week or more.

### P0 — needed before anyone can defend an audit sample

| # | Fix | Closes | Effort |
|---|---|---|---|
| 1 | **Shared mutation guard.** One `assert_form_mutable(form, user)` helper (approved? period-locked? archived? role?) called by `PUT`, chat apply, apply-template, enrich, tags, media and OCR. The version built on 2026-09-09 and reverted is the starting point. | C1, SEC-05 | S–M |
| 2 | **State checks on transitions.** Reject only from `submitted`. Submit only from draft or rejected. Enter-HRM / enter-FIN only if not already entered. | C2 | S |
| 3 | **Hard-mode sessions:** ✅ *done 2026-09-27 — the session never approves; only already-approved forms are HRM-entered.* Still open: require org **write**, not view, on session routes. | B1 | S |
| 4 | ✅ *done 2026-09-27.* **Audit table for labor data.** An append-only `dot12_audit_log` with (table, row id, form id, field, old, new, user, ts, source, reason). Two ways to fill it: Postgres triggers on the form, employee, charge, task-asset, equipment and material tables (catches ops scripts too), or a SQLAlchemy `before_flush` hook (also catches the source). Stop coalescing edit events. | D1, D2, D5 | M |
| 5 | ✅ *done 2026-09-27.* **Approval snapshot.** On approve (and on Enter HRM), store a JSON snapshot of the form plus a SHA-256 hash in `dot12_form_approvals` (form, approver, ts, hash, snapshot, attestation text version). Keep prior approvals when reopening. | B5, C3, D1 | S–M |
| 6 | **Close approver → admin escalation.** Only admins may change `role_id`, `e_number`, email or org grants, and nobody may change their own. Log role and org changes to the audit table. Confirm the prod `user_roles` row. | B3 | S |

### P1 — needed for federal-aid and ER claims specifically

| # | Fix | Closes | Effort |
|---|---|---|---|
| 7 | *(Optional)* **Snapshot TheHub federal identity at approval:** freeze `federal_project_no`, the disaster number and the DI line on the column so the record stands alone if TheHub changes. | A1 | S |
| 8 | ~~First-class ER event coding~~. **Dropped:** flood and ER work already get their own TheHub programs. Instead, add a report that groups approved hours by TheHub disaster number and DI line. | A1 | S |
| 9 | **Approved-only payroll feed.** Give `query_charge_rows` an `approved_only` parameter, and default the export and entry eligibility to approved. Show approval state per line on Timesheet Accounting. | C4 | S |
| 10 | **Reconciliation job.** Per pay period and unit, compare DOT-12 approved hours with OASIS paid hours (dTIMS `LaborTransaction` or a TAMSDW query) at the (employee, date, task order) grain. Store results and exceptions in a table, surface them to timekeepers, and keep the history. Productionize the D7 method. | E1 | M |
| 11 | **Snapshot what was keyed.** When a timekeeper confirms an employee-day, store the hours and coding lines they confirmed (from Timesheet Accounting) on the confirmation row. Invalidate the confirmation if the form changes afterwards. | D3, E4 | S–M |
| 12 | **Server-side validation on submit.** Block a blank task order, program, unit or LDPR on non-leave lines; negative hours; more than 24 h per person per form; and future `form_date` (with a leave-request exception). Warn on cross-form daily totals that are not equal to the scheduled shift and on duplicate person-days. | A2, A3, A5 | M |
| 13 | **Fix the leave-code set** in `timesheet_lines.py`: import from `leave_codes.py` instead of keeping a separate copy. | A4 | S |

### P2 — hardening and records management

| # | Fix | Closes | Effort |
|---|---|---|---|
| 14 | **Written retention policy** (≥ 3 yrs after final voucher, plus holds for open audits and ER claims) and a documented, tested Postgres backup with restore drills. Retain TADJ files and bridge envelopes under the same policy, outside `static/`. | G1, E3 | M |
| 15 | **Provenance on the record:** `source ∈ {typed, copied_from:<id>, template, ocr:<attachment>, ai_proposal:<msg id>, leave_request:<id>, mobile}` on the form and charge. Record `copied_from_form_id`. Require a signed-in user on OCR (not a header) and record the creator. | A3 | S–M |
| 16 | **Separation-of-duties extras:** block approving a form where the approver's `labor_code` is an employee on it; flag admin self-approval in the event; clear `prepared_by` when a submitted form is edited (forcing re-submission). | B2 | S |
| 17 | **Reason capture** on recall, reopen and post-approval OC edits. Warn on reopen when `entered_by_hrm` is set ("hours already in OASIS; a reversal is required"). | C3 | S |
| 18 | **Deprovisioning and access review:** `users.is_active`; server-side session revocation (auth_epoch for SSO too); a quarterly access-review export of roles and orgs. | F2, SEC-16 | M |
| 19 | **Ops scripts** (`reimport_*`, `apply_dot12_backup`, `dedup_employees`) should write through the audit log and refuse approved or HRM-entered forms unless given an explicit `--force-with-reason`. | D5 | S |
| 20 | **Stable DOT-12 reference in OASIS:** populate `timei_document_id`, or carry a DOT-12 line key in a free-text OASIS field once TADJ or the bridge goes live. Fix the 5× scheduler before enabling any export. | E2, E3 | M |
| 21 | **Fix the doc contradictions** in §7. | §7 | S |
| 22 | **Remaining open security items** that affect the integrity of time data: SEC-06, SEC-07, SEC-08, SEC-10, SEC-13, SEC-15. | F2 | M |

---

## 9. Things to confirm in production

These affect severity but could not be verified from the repo:

1. **The live `user_roles` row for `approver`.** Is `can_edit_user` TRUE, as migration 008 sets it? This decides whether B3 is live.
2. **`TADJ_EXPORT_UNITS` and `TADJ_EXPORT_ENABLED`** in the prod env. Expected: empty / unset.
3. **`BRIDGE_ENABLED` and `BRIDGE_EMIT_ON_SAVE`** in prod. Expected: false.
4. **Feature-flag states:** `pin_login` (expected OFF in prod), `leave_requests`.
5. **Whether any unit runs hard-mode entry sessions,** and how many forms have been approved through that path. A query on `dot12_form_events` near session completion times would show this.
6. **Whether anyone has called the chat apply-actions, enrich or import-pdf endpoints** in prod, given the UI doesn't expose them. Check the Apache access log (not `requests.log`, which is lossy).
7. **The Postgres backup regime and retention** on 10.0.1.229.
8. **Deployed build vs working copy** for the session-lifetime logic.
9. **Whether any federal-aid or ER labor currently flows through DOT-12** (P-flagged columns, NATDIS / flood programs). This decides how urgent P1 is.
10. **Emergency-work coding practice:** during the first days of a flood, before its TheHub program exists, what program do crews charge? If it's routine maintenance, are those hours later re-coded, and by what path?

---

## 10. Suggested talking points

For conversations with WVDOT finance, internal audit, or the FHWA Division:

- **What DOT-12 is:** the daily source record of actual work by crew, coded to the OASIS accounting string and approved by a supervisor before timekeepers key it into wvOASIS. It is not the payroll system of record.
- **Accuracy:** in the one measured comparison, D7 July–August 2026, DOT-12 hours matched OASIS-fed dTIMS labor to within 0.01 % on shared employee/day/task cells.
- **Controls in place:** SSO identity; role-based approval with a self-approval block; server-enforced lock after approval and after pay-period close; soft-delete archive with event history.
- **Controls being added (P0/P1):** a complete field-level audit log; approval snapshots; closing the alternate write paths; a disaster-number / DI-line labor report off the TheHub join; a stored per-pay-period reconciliation against OASIS; a written retention policy.

Don't make the "controls in place" claim about locking to an auditor until P0 #1 and #2 are done.
