# Labor time entry: batch file interface vs. UI automation

A build-vs-automate sketch for the **HRM labor** side of the DOT-12 → wvOASIS
integration. The premise (see the chat that prompted this): the bridge is the
right tool for the *document-centric, low-volume* FIN work (OC materials), but
labor/timesheet is the **high-volume** side, and a batch **time-import file**
interface — if OASIS-HRM exposes one — is usually the more robust path there.

This doc enumerates what one labor record must carry, shows it's the *same*
field set the bridge already keys, and compares the two delivery mechanisms so
the decision is concrete.

> Status: analysis only. It does **not** change the plan or the bridge's
> expected behaviour — both options post the same data. If we commit to a file
> interface, *that* would be a §6 contract change and the plan must be updated.

---

## 1. The unit of work

One **labor record** = one employee's hours against one accounting line for the
pay period. That's exactly the bridge's existing `HrmLine`:

```
HrmTimesheetPayload(employee_oasis_id, lines[])
  HrmLine(accounting: AccountingTuple, hours_by_date: {date: hours})
    AccountingTuple(event, ldpr_profile, unit, activity, sub_activity,
                    program, phase, task_order)
```

**Grain / squash.** Within one DOT-12 (one day, one org) the report already
groups charges by the accounting tuple — so columns that share a task order (and
the rest of the coding) collapse into one line, hours summed. Across the period
the same tuple for the same employee is one record with `hours_by_date`. Measured
example: org 0711, pp 2026-05-16 → **576 raw employee×column charges squash to
395 labor lines across 27 employees / 95 forms.**

## 2. What a record must carry (and where each field comes from)

The file layout and the bridge's keystrokes need the **identical** fields. Source
is the dot12 schema (`dot12_employees`, `dot12_task_assets`, `dot12_employee_charges`),
the same derivation the `timesheet-accounting` report does.

| Field | Source in DOT-12 | Notes |
|---|---|---|
| **Employee** | `dot12_employees.oasis_id` | the OASIS person key |
| **Home unit (org)** | `dot12_forms.home_unit` | header / file group key |
| **Pay period** | `dot12_forms.pay_period_start/_end` | header |
| **Pay code / event** | derived | leave code (`ANNLV`…) if LDPR is a leave code; else `temporary_upgrade`; else `REG` |
| **Hours** | Σ `employee_charges.hours_charged` | per work date (`hours_by_date`) or period total |
| **LDPR / funding profile** | `task_asset.ldpr_profile` (else form) | the labor-distribution key |
| **Charge (receiving) unit** | `task_asset.receiving_unit` | |
| **Activity (+ P/N)** | `task_asset.activity` + `is_participating` → `P`/`N` | OASIS validates `activity+suffix`; bare code fails (see app memory) |
| **Sub-activity** | `task_asset.sub_activity` | |
| **Program (D2)** | `task_asset.program` | |
| **Phase (D3)** | `task_asset.phase` | often blank (overhead) |
| **Task order** | `task_asset.task_order_number` | the squash key; blank for overhead/leave |
| **Fund / Appropriation / FY** | derived from LDPR (`fund 9017` + appr) and form date | needed only if the file wants the explicit funding string instead of just the LDPR |
| **Audit / lineage** | `form_id`, squashed `column_number`s, snapshot hash, approver | for reconcile + who-authorized |

Everything above already exists on the envelope's `AccountingTuple` (coding) +
`employee_oasis_id` + `hours_by_date` + `Scope`/`Actor` (header/audit). **No new
data is needed to feed a file interface — only a new emitter.**

## 3. A flat-record sketch

If OASIS-HRM accepts a positional/delimited time-import (typical for ERP payroll),
one line per `(employee, accounting tuple, work date)` — or per period if it sums:

```
HOME_UNIT | PP_START | PP_END | OASIS_ID | WORK_DATE | PAY_CODE |
LDPR | CHARGE_UNIT | ACTIVITY_PN | SUB_ACT | PROGRAM | PHASE | TASK_ORDER |
FUND | APPR | FY | HOURS | SRC_FORM_ID | SRC_COLUMNS
```

The bridge's `HrmTimesheetPayload` serializes to this almost 1:1 (explode
`hours_by_date` into per-date rows; map `event`→`PAY_CODE`, `unit`→`CHARGE_UNIT`,
`activity`+P/N→`ACTIVITY_PN`).

## 4. The comparison

| Dimension | **Batch time-import file** | **UI automation (bridge)** |
|---|---|---|
| **Throughput** | Thousands of lines in one drop; scales across all orgs trivially | One browser, serialized; ~hundreds of lines/period/org is already slow |
| **Brittleness** | Stable — a fixed record format; only changes on a deliberate interface rev | Breaks on any wvOASIS UI reskin; needs selector maintenance + canaries |
| **Server-side validation** | Batch edits run at ingest; **may bypass some interactive edits** | Exact same edits a clerk gets (account-code combos, "task order doesn't exist") |
| **Error feedback** | Asynchronous **return/reject file** the next cycle; per-line, but delayed | Immediate, per-field, at key-time |
| **Idempotency / reconcile** | File-level keys + reject handling; still need post-batch read-back | Per-doc idempotency + your `reconcile/` read-back (already built) |
| **Auth / session** | Service account + SFTP creds; no live browser | Borrowed/pooled logged-in session; MFA, session expiry, kill-switch |
| **Audit / compliance** | Clean: a signed file with lineage; standard SOX-friendly pattern | Acting *as a user*; needs the human-sponsor/approver trail you model |
| **Latency to "posted"** | Next batch cycle (same as UI submit, really) | Stages a draft; posts on the next batch too |
| **Initial build** | Need WVDOT/CGI to **define + accept** the format (org/political effort) | Self-serve; you control it end-to-end |
| **Ongoing maintenance** | Low | Higher (selectors, dialogs, UI drift) |

**Reads as:** the file wins decisively on **throughput, brittleness, audit, and
maintenance** — the things that matter at labor volume. The bridge wins on
**self-service** (no vendor dependency) and **validation parity**. The single
biggest *unknown/risk* for the file path is non-technical: **getting CGI/WVDOT to
stand up and accept the interface.**

## 5. Recommendation

- **Labor / timesheet:** pursue the **batch time-import file** first. You already
  have every field; it's a new emitter over the `timesheet-accounting` grouping,
  not new data. Volume + brittleness make UI keying of hundreds-to-thousands of
  lines the wrong long-term tool. **Open question to confirm with WVDOT/CGI: does
  OASIS-HRM have a time-entry import interface, and what's its record layout?**
- **FIN OC / materials (+ equipment):** keep the **bridge**. Lower volume,
  document-centric, benefits from live validation, and has no obvious batch path.
- **Either way:** the post-batch **reconcile/read-back** is non-negotiable —
  submit ≠ posted; the truth lands in the nightly cycle.

So: don't pick one tool for the whole integration. **File for labor (if it
exists), bridge for documents** — and the field inventory above shows the build
cost for the file emitter is small because the contract is already modelled.
