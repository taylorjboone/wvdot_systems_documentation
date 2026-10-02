# wvOASIS Integration — Implementation Plan

**Scope:** Push approved DOT-12 data into wvOASIS (HRM timesheets, FIN equipment usage, FIN material consumption) via supervised browser automation, with a human approval gate preserved on the wvOASIS side.
**Companion doc:** `WVOASIS_INTEGRATION_PROPOSAL.md` (the business framing, peer examples, controls).
**Target system:** wvOASIS (CGI Advantage-based ERP) — `wvdotom.wvoasis.gov` is already used for OData reads; writes go through the human-facing web UI.
**Status:** Draft. Written before screen access — discovery activities are explicitly called out where the plan needs vendor-screen detail to firm up.

---

## At a glance — what the bot does every night

Every night, the bridge walks through one employee at a time for the target org and writes — for the day just past — one or more accounting-line rows into that employee's existing in-progress wvOASIS timesheet, then saves and moves to the next employee. **One employee at a time. One day at a time. Add or update the row(s) that cover today's work.** The clerk's final submit at end of pay period remains a human action.

The two screens below show the source and the destination. They were intentionally designed with matching columns and the same 14-day pay-period grid, so each DOT-12 row maps directly onto one wvOASIS accounting line.

**Source — DOT-12 Timesheet Accounting view (this app):**

![DOT-12 Timesheet Accounting report — source data the bot reads from](dot12_timesheet_accounting.png)

**Destination — wvOASIS HRM Timesheet edit screen (what the bot types into):**

![wvOASIS HRM Timesheet edit screen — what the bot types into](oasis_timesheet_edit.png)

Per-employee per-night: open the in-progress timesheet for the current pay period → find-or-create the accounting lines that match today's DOT-12 entries (matched by the `Event / LDPR Profile / Unit / Activity / Sub Activity / Program / Phase / Task Order` tuple) → type today's hours into today's day-cell → save (not submit). Repeat across the org.

---

## 1. Why this plan looks the way it does

A few facts about DOT-12 shape the entire design:

1. **The data is already validated and the shape already matches OASIS HRM.** The `/dot12/api/reports/timesheet-accounting` endpoint produces, per employee per pay period, exactly the row structure an OASIS HRM timesheet expects: one accounting line per `(event, LDPR profile, unit, activity, sub_activity, program, phase, task_order)` with hours bucketed across 14 day-columns. Nothing has to be re-derived; the bridge consumes that endpoint as-is.
2. **DOT-12 already has the workflow roles modeled.** `prepared_by`, `approved_by`, `entered_by_hrm`, `entered_by_fin` are first-class FKs to `users`. The bot is a user (a system user, governed differently — see §11), and the bot fills the `entered_by_hrm` / `entered_by_fin` roles exactly the same way a human clerk does today.
3. **Reads already use OData; writes don't.** DOT-12 already pulls inventory, account codes, employees, and equipment from the OData API. We do not need to replace any of that. The only thing missing is the write side, which OData on this tenant does not expose for HRM/FIN postings. That is the gap this bridge fills.
4. **CGI Advantage has a native "draft document" model.** Advantage transactions (timesheet, equipment usage, OC documents) are *documents* with a lifecycle: Draft → Pending → Submitted → Approved. The bot saves drafts. Humans submit. This maps perfectly to the human-approval-gate posture in the proposal and means we are not fighting the system; we are using it as designed.
5. **We do not have screen access yet.** The plan is structured so that everything which depends on a specific screen lives in **one isolated layer** (the Page Object Model, §7). The rest of the architecture can be designed, scaffolded, and even partially tested before discovery starts.

---

## 2. Where this fits in the existing architecture

```
                                    ┌────────────────────────────────┐
                                    │   wvOASIS (CGI Advantage)      │
                                    │   - HRM timesheet              │
                                    │   - FIN equipment usage        │
                                    │   - FIN material / OC docs     │
                                    └────────────────────────────────┘
                                               ▲   ▲
                              (read, OData)    │   │  (write, browser)
                                               │   │
┌──────────────────────┐                       │   │
│  React 19 / Vite     │   REST                │   │
│  dot12-frontend      │ ◀────────┐            │   │
└──────────────────────┘          │            │   │
                                  │            │   │
┌──────────────────────┐   REST   │            │   │
│  Flask / SQLAlchemy  │ ◀────────┤            │   │
│  dot12-backend       │          │            │   │
│  PostgreSQL :5433    │          │            │   │
│                      │          │            │   │
│  • forms             │          │            │   │
│  • employees         │   read   │            │   │
│  • equipment         │ ─────────┼──────► OData (existing,
│  • materials         │          │           unchanged)
│  • task_assets       │          │
│  • timesheet         │          │
│    accounting view   │          │
└──────────┬───────────┘          │
           │                      │
           │ posting envelopes    │
           │ (REST, signed)       │
           ▼                      │
┌──────────────────────────────┐  │
│  oasis-bridge (NEW)          │  │
│                              │  │
│  • posting queue             │  │
│  • workers (Playwright)      │  │
│  • Page Object Model         │  │
│  • read-back diff engine     │  │
│  • audit log (own DB)        │  │
└──────────────────────────────┘  │
                                  │
              status / audit ─────┘
```

**Key boundary:** `oasis-bridge` is a **separate service**, not Flask routes inside `dot12-backend`. Reasons:

- Different runtime — Playwright + browser binaries, headed-capable for debugging, not appropriate to colocate with the Flask request loop.
- Different security posture — the bridge holds wvOASIS credentials and a session vault; the Flask app does not need them.
- Different scaling characteristics — the bridge is queue-driven and slow (seconds per post); Flask is request-driven and fast.
- Different deploy cadence — vendor-screen changes will trigger bridge releases that have nothing to do with DOT-12 features.

**Why a service and not a script?** Because we need a queue, retries, audit, and a kill switch. A script can't give you those defensibly.

---

## 3. What we know vs. what we still need to discover

| Known | Source |
|---|---|
| wvOASIS is CGI Advantage; documents have Draft → Pending → Submitted lifecycle | Public CGI documentation; "Submitted-Final" status visible in Time and Leave Management list view |
| OData base URL `https://wvdotom.wvoasis.gov/omdata/odata` is reachable from our backend | `dot12-backend/app.py`, `routes/deighton.py` |
| Authentication for OData is bearer token | `project.md` |
| Pay periods are bi-weekly Sat–Fri | `TIMESHEET_ACCOUNTING_FEATURE.md` |
| The accounting-line shape we'd type into HRM (event, LDPR, unit, activity, sub_activity, program, phase, task_order, hours by date) | `routes/reports.py` |
| **The DOT-12 timesheet-accounting screen is a near-1:1 visual replica of the OASIS HRM timesheet edit screen** — same columns, same 14-day grid, same event-code chips | DOT-12 screenshot, OASIS screen recording |
| **The OASIS HRM Timesheet detail screen uses "Easy Fill" tab for bulk entry**, with per-line accounting fields and 14 day cells, plus visible Save / Cancel buttons | OASIS screen recording |
| **Transaction ID format `TMS1-<unit>-<seq>`** (e.g. `TMS1-0517-2020000000080213`) — an Advantage document identifier that can serve as the bot's reference key | OASIS screen recording |
| **Time and Leave Management list view** is the navigation entry point; lists existing TMS documents by employee, pay period, and status | OASIS screen recording |
| **Picker popups are real browser child windows** opened via `window.open()` (URL pattern `…/advantage/AMSImages/Empty.htm`, populated by JS post-open) | OASIS screenshot |
| **ist311.wvoasis.gov is the wvOASIS staging/integration test environment** — available for discovery and bot development | OASIS screenshot URL |
| Material posting uses `oc_doc_id` (OC = Order for Commodities, an Advantage doc type) | `flask_models.py` `DOT12Material.oc_doc_id` |
| Equipment posting uses ED number, ending meter, operator initials | `flask_models.py` `DOT12Equipment` |
| Org unit codes (e.g. `0838`) and home_unit drive scoping | throughout |

| Unknown — must be answered during discovery | Where the answer lives |
|---|---|
| The exact wvOASIS login flow (SSO? state IdP? MFA? service-account exemption?) | wvOASIS portal login |
| The HRM timesheet entry screen — fields, validation, save vs. submit, draft semantics | OASIS HRM |
| The FIN equipment usage doc — doc type code, header fields, line fields | OASIS FIN |
| The FIN material/OC document — how `oc_doc_id` is created, looked up, or referenced | OASIS FIN |
| Whether a service account can be issued with **scoped** roles (entry-only, not approve) | wvOASIS security admin |
| Session timeout duration and concurrent-session limits | wvOASIS portal |
| Whether the wvOASIS UI offers stable element IDs or proprietary ASE widget IDs only | DOM inspection |
| Whether the Advantage "Document ID" can be written by us (idempotency anchor) or is system-assigned | OASIS HRM/FIN doc create flow |
| Rate limits / throttling on the UI | observed behavior |

The plan is structured so that everything in the second table is confined to the **Discovery Phase (§13)** and the **Page Object Model layer (§7)**. The rest of the system can be built without those answers.

---

## 4. The five-layer architecture of `oasis-bridge`

The bridge is intentionally layered so that vendor-screen volatility is isolated to one layer.

### Layer 1 — Intake API (HTTP, stable)
A small REST surface called by `dot12-backend`:

- `POST /v1/postings` — submit a posting envelope (see §5). Returns a `posting_id`.
- `GET /v1/postings/{id}` — current state, latest screenshots, mismatch diffs.
- `POST /v1/postings/{id}/cancel` — cancel a queued or in-progress posting.
- `GET /v1/postings?dot12_form_id=...` — query by DOT-12 source row.
- `GET /v1/health` — liveness.

Authentication: mTLS or signed JWT issued by `dot12-backend`, scoped to the bot service identity. No human ever calls this directly.

### Layer 2 — Posting Queue (workflow, stable)
- Enqueues envelopes; assigns a worker; manages retries with backoff; emits state transitions.
- State machine per posting: `received → queued → in_progress → staged_in_oasis → reconciled | flagged | failed`, plus `in_progress → removed` for a delete-action envelope (the line's draft OC was discarded).
- Persisted in the bridge's own Postgres database (separate from DOT-12 DB; the bridge owns its history).
- Tech: Postgres + a small lock-based dispatcher (pg `SELECT … FOR UPDATE SKIP LOCKED`) — no need for Redis/Celery for the volume we're targeting (low thousands per night). Simpler is better here.

### Layer 3 — Session Manager (slightly volatile)
- Maintains a pool of authenticated browser sessions.
- One session per bot identity per wvOASIS subsystem (HRM / FIN).
- Handles login, MFA prompt (if any), session-keepalive pings, re-login on session expiry.
- Hands a "live page" to a worker when it picks up an envelope; returns it after.
- All credentials pulled from a vault (HashiCorp Vault, AWS Secrets Manager, or whatever the state already runs); never on disk in the bridge image.

**Session acquisition is abstracted behind one interface so dev and prod differ in exactly one place.** A worker never launches a browser itself; it asks a `SessionProvider` for a live page and returns it when done:

```python
class SessionProvider:
    def acquire(self, subsystem: str) -> Page: ...   # "hrm" | "fin"
    def release(self, page: Page) -> None: ...

# prod: managed, headless, pooled, vault-auth, keepalive (this section)
class PooledSessionProvider(SessionProvider): ...
# dev: attach to a human's already-logged-in, headed browser over CDP (Layer 3a)
class AttachedSessionProvider(SessionProvider): ...
```

The page objects (Layer 4) and workers are identical in both modes — they receive a `Page` and drive it. Only the provider changes, selected by `BRIDGE_MODE` (`prod` | `dev`).

### Layer 3a — Development mode: live-browser workers (dev/discovery only)

**What it is.** In dev mode the worker does **not** spin up an isolated headless context from the pool. It **attaches over CDP to a real, headed browser that a developer is already logged into** (`chromium.connect_over_cdp("http://localhost:9222")`), finds the wvOASIS tab, and drives that live Advantage screen. You watch every click, every field write, every row-flip rebuild happen in front of you, and can pause with the Playwright Inspector mid-posting to inspect DOM/state.

**This is not speculative — it is how discovery and the FIN/OC automation were already built.** The `oasis-*.mjs` bots (OC document creation, inventory-adjustment entry, the Final-doc scraper) run exactly this way against a logged-in Brave on `uat311`: `connectOverCDP` → grab the Advantage tab → drive it. Dev mode formalizes that into the `AttachedSessionProvider` so the *same page objects* the prod pool uses can be developed and debugged against a live, human-authenticated session.

**How it works:**
```bash
# 1. Developer launches a headed browser with a debug port + a persistent
#    profile, and signs in once (SSO / MFA done by the human, by hand):
chromium --remote-debugging-port=9222 \
         --remote-debugging-address=127.0.0.1 \
         --user-data-dir="$HOME/.oasis-dev-profile"
#    → log in to ist311/uat, leave the tab on the HRM/FIN landing screen.
# 2. Run the bridge with BRIDGE_MODE=dev. AttachedSessionProvider.acquire()
#    does connect_over_cdp(:9222), picks the tab whose Main Display frame is
#    present, and hands that Page to the worker.
```

**Why it makes debugging dramatically easier:**
- **No bot credentials, no vault, no keepalive during dev.** The worker borrows the human's live SSO session — exactly the auth path that's hardest to stand up headlessly. SSO/MFA is solved once, by hand, and the worker just uses the open session.
- **You see the row-flip defect (§9a) happen and watch the snapshot/rebuild repair it** in real time, instead of reconstructing it from a trace after the fact.
- **Selector authoring against the real screen.** Pair with `playwright codegen` / the Inspector to capture and refine `name="..."` / label-then-input selectors live (this is literally how the OC page recipe was authored).
- **Pause-and-poke.** Drop `page.pause()` (or `await page.pause()` in JS) anywhere in a page-object method to freeze the worker and step through the rest by hand.

**Hard boundaries (enforced, not conventions):**
- **Dev mode is `uat`/`ist311` only.** `AttachedSessionProvider` refuses to attach if the tab's URL host is a production wvOASIS host — a guard in `acquire()`, not a runbook note.
- **One live browser = one worker, no concurrency.** Dev mode forces queue concurrency to 1; you are driving a single human-shared tab.
- **Save-not-submit still holds** — dev mode changes how the session is acquired, nothing about the posting discipline (drafts only, read-back, flag-on-mismatch all run unchanged).
- **Never in production.** Production always uses `PooledSessionProvider` (headless, vault-auth, pooled, keepalive). `BRIDGE_MODE=dev` is rejected by config when the bridge's environment is `prod`. This is the inverse of the §12 incident-viewing CDP port: there, on-call *watches* a prod headless session read-only; here, the worker *drives* a developer's live session — a dev-only capability.

### Layer 4 — Page Object Model (volatile — this is the layer that changes)
- One object per wvOASIS screen we touch. E.g. `HrmTimesheetListPage`, `HrmTimesheetPage`, `FinEquipmentUsagePage`, `FinMaterialOcDocPage`.
- Each object exposes **business-level methods** (`find_timesheet_for(employee_id, pay_period)`, `find_or_create_line(accounting_tuple)`, `set_day_hours(line, date, hours)`, `save_draft()`, `read_back()`), not raw selector calls.
- All selectors live inside these objects and **only** inside these objects. If wvOASIS changes a field name, exactly one file changes.
- Selectors are ranked by stability:
  1. Data attributes / aria-label / visible label-then-input lookup (most stable)
  2. Backend field name (Advantage usually exposes `name="...."` attributes that match the doc-type field code — these survive UI redesigns because the doc type definition is the source of truth)
  3. CSS / structural (last resort, with comment explaining why)
- Every page object includes a `self_test()` method that, given a known live test record, walks the screen and asserts every selector it depends on still resolves. The daily canary (§14) calls these.

**Direct-type-and-validate is the primary entry mode.** Confirmed: the accounting-dimension fields (LDPR Profile, Activity, Sub Activity, Program, Phase, Task Order, Home Unit, etc.) accept direct keyboard input. When the bot types a valid code and the field loses focus (`Tab` or `blur`), OASIS validates against its lookup tables and auto-formats the entry. The picker popup is the *fallback* path — it's what a clerk uses when they don't know the code and want to browse. Because the DOT-12 data the bot is posting was pre-validated against the same OData lookup tables (via the autocomplete components in the dot12-frontend), every value the bot writes should already be a valid code, and the picker fallback should rarely if ever fire in steady state.

**Bot's per-field write pattern (primary path):**
```
field.click()           # or focus
field.fill("261")       # type the validated code from DOT-12
field.press("Tab")      # commit, trigger OASIS-side validation + auto-format
# expect: field is now formatted ("261 - Patching of Bituminous Pavements" or
# whatever OASIS's canonical display is) and no error indicator
```

A `validate_field_accepted()` helper checks for absence of OASIS's invalid-value indicator (red border / inline error / cleared field) after the focus-change; if the input was rejected, the bot fails the line into `flagged` and a human reviews. The bot does not retry the picker — a rejection means the source data is wrong, not that the bot mistyped.

**Pop-up search ("Pick") windows — fallback / discovery-time only.** When a clerk needs to browse for a value, clicking a search/lookup icon opens a **native browser child window** via `window.open()` (titled e.g. *"Search - Google Chrome"*, URL pattern `https://ist311.wvoasis.gov/isthrm11/advantage/AMSImages/Empty.htm`, content populated by JS after open). These are not iframes and not in-page modals. The bot has a `PickerDialog` helper class so discovery-time fixture capture and the rare runtime fallback both work the same way:

```
with page.context.expect_page() as popup_info:
    page.click(picker_link_selector)
popup = popup_info.value
popup.wait_for_load_state()
popup.fill(criteria_field, search_term)
popup.click(search_button)
popup.click(result_row_for(target_value))
# popup auto-closes; parent field becomes populated
page.wait_for_function("...parent field has value...")
```

Each picker gets a small subclass declaring its criteria fields, search button, and result-row selector. The picker subclasses are nice-to-have for resilience, not required for steady-state operation.

### Layer 5 — Reconciliation (stable)
- After a worker stages a draft in wvOASIS, it re-reads the draft (via the same page object's `read_back()` or an OData query if the doc is queryable post-draft) and diffs against the source envelope.
- Mismatches → posting state goes to `flagged`, with a structured diff and a screenshot. Item routes to a human. **Does not retry automatically** — a mismatch means the data in wvOASIS does not match DOT-12, so retrying without human review would just re-stage bad data.
- Matches → state goes to `staged_in_oasis`. Posting is then *visible* in wvOASIS as a draft document, awaiting human submit.
- A second reconciliation pass runs after submission to confirm the document was actually posted (state → `reconciled`).

---

## 5. Data contract: the Posting Envelope

The envelope is the only thing `dot12-backend` ever sends to the bridge. It is the contract: if it parses, the bridge owes a result.

```jsonc
{
  "envelope_id": "uuid",                    // bridge-side idempotency key
  "source": {
    "system": "dot12",
    "dot12_form_id": 12345,
    "line_key": "mc:4821",                  // stable per-line id (survives edits)
    "dot12_form_updated_at": "2026-05-09T14:32:11Z",  // optimistic concurrency
    "snapshot_hash": "sha256:..."           // hash of the payload below
  },
  "kind": "hrm_timesheet" | "fin_equipment" | "fin_material",
  "action": "create" | "update" | "delete", // §6c lifecycle (default create)
  "oasis_doc_id": "2600077820",             // the doc an update/delete reuses; null on create
  "scope": {
    "home_unit": "0838",
    "pay_period_start": "2026-04-25",
    "pay_period_end":   "2026-05-08",
    "form_date": "2026-05-02"               // for non-timesheet kinds
  },
  "actor": {
    "bot_identity": "dot12-oasis-bridge",
    "human_sponsor_user_id": 17,            // accountable person per OMB M-19-17
    "approved_by_user_id": 9,               // who pressed "approve" inside DOT-12
    "approved_at": "2026-05-09T14:30:02Z"
  },
  "payload": { ... kind-specific, see §6 ... },
  "constraints": {
    "leave_in_draft": true,                 // never submit; humans submit
    "max_runtime_seconds": 600,
    "abort_on_mismatch": true
  }
}
```

A few non-obvious decisions:

- **`dot12_form_updated_at` + `snapshot_hash` are mandatory.** If the DOT-12 row changes after the envelope is queued, the bridge refuses to post and asks the caller to re-submit. We never want to post stale data.
- **`leave_in_draft: true` is the default and cannot be disabled in v1.** The submit button stays human. Eventually we may add a delegated-submit path for narrow doc types after a long supervised period; not in initial scope.
- **`envelope_id` is idempotent end-to-end.** Re-posting the same envelope returns the same `posting_id` and state — never creates a second wvOASIS draft.
- **`line_key` + `action` drive the lifecycle (§6c).** dot12 diffs each line against what it has already posted and emits `create` / `update` / `delete`. An update/delete carries the `oasis_doc_id` it must reuse, so a quantity edit re-drives the *same* OC and a removed row discards its OC — never a duplicate document. `action` defaults to `create`, so a caller that only ever adds lines need not set it.

---

## 6. The three posting flows

### 6a. HRM timesheet posting

**Source data:** the timesheet-accounting endpoint, per employee, scoped to one or more form-dates (typically yesterday's DOT-12 forms for nightly runs).

**Operating model — incremental daily entry, with rebuild-on-flip discipline.** The bot does what a clerk does today: for each employee in the org, open the in-progress timesheet for the current pay period, append the day's hours to the appropriate accounting lines, save, move on. **However**, per §9a, the wvOASIS row-flip defect means that every Insert Row wipes the LDPR sub-detail of every existing row on the timesheet. The bot therefore operates in two phases per timesheet: (1) capture a full snapshot of every existing row, (2) do all the night's Insert Rows back-to-back, (3) rebuild every row's LDPR sub-detail from the snapshot (existing rows) or the source envelope (newly-added rows), (4) fill the new rows' day-cell hours, (5) save and read-back. This is heavier than the proposal's "fast clerk" framing implied, and the proposal should be updated to acknowledge that the bot does meaningfully more work per night than a clerk because it operates around a vendor defect. The bot still does **not** wait until end of pay period and dump the full 14-day grid in one pass — daily incremental entry remains the model.

**Trigger condition:** for the form-date being posted, all covering DOT-12 forms for that (employee, date) are in `approved` state. Approved-only data flows; partial-day approvals are deferred to the next run.

**Per-employee, per-night flow:**

1. From the Time and Leave Management list view, locate the **in-progress** timesheet for `(employee.oasis_id, current pay_period)`. If no in-progress timesheet exists for the current pay period (rare — clerks normally have one already), create one. **Never** open a timesheet already in `Submitted-Final`; if found in that state, flag for human review and skip.
2. Open the timesheet detail screen. Click the **"Easy Fill"** tab if not already active.
3. For each accounting line in today's DOT-12 timesheet-accounting endpoint output for this employee:
   - **Find-or-create the matching OASIS accounting line.** Two lines match iff they have the same `(Event, LDPR Profile, Activity, Sub Activity, Program, Phase, Task Order)` tuple. If a matching line already exists in the timesheet (from a prior night's run or a clerk's earlier entry), reuse it. Otherwise add a new line and **type each accounting dimension directly into its field**. OASIS validates the typed value against its lookup tables and auto-formats on accept (`blur` / `Tab`); the picker popup (§7) is only needed as a fallback for invalid input — and because the bot has pre-validated values from DOT-12, the fallback should almost never fire in steady state. LDPR Profile does not auto-populate the other dimensions, so each of the six is still typed independently, but each one is a single text-input write followed by a focus-change, not a window-open round-trip.
   - **Enter today's hours into today's day-cell on that line.** Do not touch cells for other dates.
4. Save (not submit). The timesheet remains in non-final state for the clerk's eventual submit.
5. Read back the saved timesheet. Verify the day-cells we wrote match the source envelope for today's date. Other day-cells are out of scope for read-back (they were entered by humans or earlier bot runs).
6. Mark the posting `staged_in_oasis`. The submit/Submitted-Final transition is the clerk's job at end of pay period.

**Idempotency anchor:** every Advantage document has a free-text "comments" / "description" field. We write a tagged token there: `[DOT12-ENV:<envelope_id>]`. Subsequent runs find the existing draft by searching for that token before creating a new one. If we lose the bridge DB tomorrow, we can rebuild posting state from this tag alone.

**Event derivation** is already implemented backend-side per `routes/reports.py`:
- LDPR is a leave code (SCKLV, ANNLV, FMSUS, HOLLD, BRVUS) → event is the leave code
- `temporary_upgrade` set → event is the upgrade code
- otherwise → event is `REG`

The bridge consumes the derived value; it does not re-derive.

### 6b. FIN equipment usage posting

**Source data:** for a given `(form_date, home_unit, equipment.ed_number)`:
- The equipment header (ED number, ending meter, operator initials)
- Per-task-asset hours from `dot12_equipment_charges` joined to `dot12_task_assets` (so every charge carries its task accounting dimensions)

**Trigger condition:** the form is `approved`.

**Flow:**

1. Open the FIN equipment usage doc for the form date and home unit.
2. Either create a new doc or open the existing draft (by idempotency tag).
3. Header: ending meter, operator initials.
4. For each (equipment, task_asset, hours) tuple, add a line with the task accounting code and hours.
5. Save as draft.
6. Read back, diff, mark staged.

**Open question for discovery:** whether equipment usage is one document per form, one per equipment, or one per home_unit per day. This determines envelope granularity. The plan supports any of the three — we just choose at build time.

### 6c. FIN material consumption / OC document posting

**Source data:** for each material on a form, the per-task-asset quantity charged.

**Two cases:**

- **Inventory materials** — `org_whse`, `stock_item_number`, `commodity_suffix` are all set, and `oc_doc_id` is set or to-be-created.
- **Direct-bill materials** — `org_whse == "DIRECT BILL"`, no inventory tracking. These may post to a different doc type entirely (e.g. an asphalt direct-billing flow). Discovery item.

**A material row IS an OC transaction.** Each `(material, task_asset, quantity)` tuple becomes one **commodity line + its accounting line** on an OC (Over-The-Counter) document — the document that issues that quantity from the inventory warehouse against the task order. The create-and-fill flow is **already proven** (the `oasis-create-oc-*.mjs` bots): create OC (Code `OC`, Dept `0803`, Unit = issuing org, Auto Numbering) → Header (Document Name, Warehouse = `org_whse`, Requesting Unit, Issuer) → Commodity line (Stock Item, Suffix, Requested Quantity; OASIS auto-populates the unit price from the warehouse) → Accounting (per §6c-acct) → Validate → leave as Draft.

**§6c-acct — the accounting values and where they come from (proven + abstracted in `oasis_oc_source.py`):**
- **Event Type** `ST11`, **Object** `8201`, **Sub Object** `0000` — fixed OC / material codes.
- **Department** `0803`, **Unit** = issuing org — structural.
- **Activity** = the DOT-12 `activity` **+ P/N suffix** (`is_participating ? P : N`, e.g. `261N`). The bare number fails OASIS's reference-table check — this is a general OASIS rule, not OC-specific.
- **Fund** + **Appropriation Unit** = resolved from the DOT-12 `ldpr_profile` by joining **TheHub** `StateFund` / `StateAppropriation` (LDPR `17237` → Fund `9017`, Appropriation `23700`). Never assumed/derived arithmetically — looked up. Annual-plan codes (D0xAP) are not TheHub *projects*, so the lookup goes straight to those tables.
- **Task Order / Program / Phase** — from the DOT-12 task asset.

`dot12-backend/oasis_oc_source.py` is the single retrieval step that assembles all of the above (dot12 commodity/accounting + the TheHub Fund/Appropriation lookup) into one payload per material entry; the bridge consumes it rather than re-deriving.

**The OC lifecycle is the fork for every operation.** An OC is `Draft → Submitted → Approved`, and **Approved means inventory has physically left the warehouse** — a closed financial transaction. The bot only ever edits **Drafts**. So every material-row mutation branches on the OC's state, located via the two anchors: `dot12_material_charges.oc_doc_id` (dot12 side) and the `[DOT12-ENV:<envelope_id>]` token in the OC description (OASIS side). Each app-side change bumps `dot12_form_updated_at` → new `snapshot_hash` → fresh envelope; a stale hash is refused, so a mutation can never race a half-posted draft.

**Operations (`FinOcDocumentPage` methods):**

- **ADD a material row.** `find_or_create_oc()` by tag: if no Draft OC exists for the form, create one (flow above) and tag it; if one exists (an earlier material already posted), **append** this commodity + accounting line to it. Write `oc_doc_id` back onto the charge. Read-back, mark staged. Re-running the same envelope finds the line by tag and never duplicates.
- **UPDATE a material row** (qty, or stock / suffix / warehouse):
  - *OC still Draft* → cheap, bot-safe. Find the matching commodity line (stock item + suffix + task asset) and `update_line()`: retype Requested Quantity for a qty change; rebuild line identity + accounting for a stock/suffix change; for an `org_whse` change, re-key the Header warehouse so OASIS re-pops the unit price (warehouse drives price). Re-validate, save.
  - *OC already Submitted/Approved* → **cannot edit a posted OC.** The correction is a *new* document — a corrective/delta OC for an increase, or a **return/reversal** for a decrease (the same inventory-adjustment shape the `oasis-rebuild-line.mjs` flow already drives). The bot detects the post-draft state and routes to `flagged` for a human / generates the correcting transaction per policy — it never silently rewrites issued inventory.
- **REMOVE a material row:**
  - *OC still Draft* → `delete_line()` on that commodity line (+ its accounting); if it was the only line, `discard()` the whole Draft OC. Clear `oc_doc_id` on the dot12 side.
  - *OC already Submitted/Approved* → a **return/reversal OC** (inverse quantity, puts the material back). Flag for human; generate the reversing transaction.

**Row-mutation guard (discovery item).** The HRM timesheet has the row-flip defect (§9a) where Insert/Delete Row wipes other rows' sub-detail. We have **not** confirmed whether the OC commodity grid shares that postback-rebuild behaviour. Until characterized on ist311 (§13, item 5 — Delete Row), OC `add_line` / `update_line` / `delete_line` get the same defensive **snapshot-before / read-back-and-rebuild-after** treatment as the timesheet.

**Net posture:** changes to a *Draft* OC are ordinary bot edits; changes to a *posted* OC are new correcting/reversing documents and stay human-gated. That boundary is the financial-correctness property — it is deliberate, not a limitation to engineer away.

**Lifecycle identity & doc-id binding.** The stable anchor per material line is the
**charge row** — line_key `mc:<charge_id>` (charge ids survive form edits). The
envelope carries `action` (create | update | delete), `source.line_key`, and the
`oasis_doc_id` an update/delete reuses (§5). `emit_for_form` **diffs the form's
current material lines against the postings already sent** and emits exactly the
deltas: a never-seen line → create, a changed line that already has an OASIS doc →
**update the same doc** (no second OC), a line that vanished → **delete** (discard)
its draft OC. On the create/update staged callback the bridge's returned doc id is
**bound back onto `dot12_material_charges.oc_doc_id`** (and mirrored to the visible
INV4 `dot12_materials.oc_doc_id` for single-charge materials), so the OC DOC ID
appears inside the form; on a `removed` callback that binding is cleared.

**Implementation status (2026-06-13).** The **full create / update / delete
lifecycle is VERIFIED end-to-end on uat311** for FIN material (live test:
`oasis-bridge/tests/integration/test_oc_lifecycle_live.py`, `OASIS_LIVE=1`).
dot12-backend `emit_for_form` emits action-tagged envelopes per the diff above
(on approve, and on save when `BRIDGE_EMIT_ON_SAVE`); the bridge worker dispatches
on `action` and the callback binds / clears `oc_doc_id` on the charge. Confirmed
uat behaviours now baked into the page object:
- **Open existing OC by id:** the catalog has **no "Edit" link** — `open_doc`
  does default catalog → **Search** → fill Code/Dept/Unit/ID → **Browse**
  (executes) → click the doc-id link in the results grid.
- **Update reuses the same OC:** a catalog-opened OC is **read-only**, so
  `update_line` clicks the toolbar **Edit** to enter edit mode before re-driving
  the commodity Requested Quantity (without this the field is read-only and the
  edit silently no-ops). Verified the qty change (10→5) persists across re-open.
- **Delete:** `discard()` removes the draft. Advantage's Discard raises a native
  `confirm()` dialog — the bridge auto-accepts page dialogs (Playwright otherwise
  cancels them, which silently blocked the discard). Verified the doc is gone
  (re-open fails) after discard.
- **Robustness:** Create/open poll for the OC header (slow postbacks) and Create
  retries once.

Still **pending discovery (§13 item 5):** non-quantity edits (warehouse / stock /
task-order → accounting re-drive; today `update_line` covers the quantity case
the form surfaces), the row-level **Delete Line** label (one OC per charge today,
so a removed line discards the whole document rather than a single grid line), the
tag-based `find_or_create_oc` (still **always creates** a fresh OC, §13.6/§13.7),
and the draft-vs-posted edit boundary / reversal generation. HRM and FIN-equipment
envelopes are not yet emitted (their bridge page objects are stubbed).

**Flow (direct-bill case):** TBD pending discovery (`org_whse == "DIRECT BILL"`, no inventory issue, likely a different doc type). Plan captures it as a separate page-object subclass with the same envelope shape and the same staged/reconciled lifecycle.

### 6d. DOT-12 application changes (frontend + backend) — bridge-optional by design

**Hard design rule: the bridge is an optional satellite. The DOT-12 app must run identically to today with no bridge present, and light up automated posting only when one is configured.** Every change below sits behind a single capability flag. Flag **off** (or bridge unreachable) → the app behaves exactly as it does now: humans click **Enter HRM** / **Enter FIN**, there are no outbound calls, no new UI, and the new mirror table simply stays empty. Flag **on** → the same workflow gains automated posting plus read-only status visibility. **No code path may assume a bridge exists** — this keeps the app independently shippable and lets the bridge be added, removed, or taken down for maintenance with zero impact on the core workflow.

**Backend (`dot12-backend`):**

1. **Capability flag + config.** `BRIDGE_ENABLED` (default **false**), `BRIDGE_URL`, and outbound auth (mTLS or signed JWT). A `GET /dot12/api/capabilities` response (or a field on `/me`) exposes `{ "bridge_enabled": bool }` so the frontend renders conditionally. When false, none of items 2–4 do anything.
2. **Outbound emission on approval (guarded).** When enabled, the `approve` transition (or a dedicated "queue for OASIS" admin action) writes posting envelopes to a **local outbox table** and best-effort POSTs them to the bridge `POST /v1/postings`. Envelopes are built from the data contracts that already exist: `/reports/timesheet-accounting` (HRM) and `oasis_oc_source.py` (FIN material/equipment). Emission is **never on the critical path** — a bridge outage leaves the outbox row pending and approval still succeeds. When disabled, `approve` just stamps `approved_by` exactly as today.
3. **Posting-status mirror.** A new `dot12_oasis_postings` table (`envelope_id, form_id, kind, line_key, action, state ∈ {queued,in_progress,staged_in_oasis,reconciled,flagged,failed,removed}, oasis_doc_id, snapshot_hash, message, emit_pending, updated_at`) that mirrors bridge state for display. It is a **read-mirror only** — the bridge owns the authoritative history (§4 Layer 2); this is empty and inert when no bridge. `line_key`/`action` let `emit_for_form` diff current lines against prior dispatches (create vs update vs delete); the existing `dot12_material_charges.oc_doc_id` is the binding the bridge writes back.
4. **Inbound callback (guarded).** `POST /dot12/api/oasis/postings/callback` (bridge→app, authenticated) updates the mirror and, for FIN material, **binds the returned `oasis_doc_id` onto the line's `dot12_material_charges.oc_doc_id`** (mirrored to the visible INV4 `dot12_materials.oc_doc_id` for single-charge materials) on a create/update staged callback, and **clears it** on a `removed` callback. The route is registered only when `BRIDGE_ENABLED`. *(Stamping `entered_by_hrm` / `entered_by_fin` is deferred until a bot system-user is provisioned, §11 — writing an `*_at` with a null signer would corrupt the form's signature state, so the callback updates only the mirror + the bound doc id for now.)*
5. **Manual workflow is preserved, unchanged.** The existing `/enter-hrm` and `/enter-fin` endpoints (and their role lock) stay. With a bridge, the callback drives the same state transition; without one, the timesheet/admin user drives it by hand. The data model does **not** fork — there is one `entered_by_hrm` field whether a human or the bot set it (the audit/event log records which actor).
6. **Staleness anchor.** Expose `dot12_form_updated_at` + a `snapshot_hash` (over the posting-relevant fields) on the form/charge so the bridge's stale-data guard (§5) works. Mostly present already; formalize the hash.

**Frontend (`dot12-frontend`):**

1. **Capability-gated rendering.** `UserContext` reads `bridge_enabled`; every bridge UI element is wrapped so it is **absent entirely** when false. With the flag off the app is visually identical to today.
2. **Posting-status chips.** In the form list and form detail, when the bridge is enabled, show a small OASIS-posting status per form (Queued / Staged / Reconciled / **Flagged**) sourced from the mirror, alongside the existing Prepared/Approved/HRM/FIN signature chips. When disabled, the signature chips are the only status — today's behavior.
3. **Postings / exceptions admin page.** A new `/dot12/oasis-postings` page (the exceptions queue referenced in §9) — gated to the timesheet/admin roles **and** `bridge_enabled` — lists `flagged`/`failed` postings with the structured diff + screenshot and **retry / cancel** actions (proxied to the bridge API). Hidden and unrouted when no bridge.
4. **HRM/FIN entry UI adapts.** With a bridge, the manual **Enter HRM / Enter FIN** actions are relabeled/auto-driven ("auto-posted via OASIS bridge"), with a retained admin manual-override; without a bridge they are the normal actions (same `SignatureConfirmModal`, conditionally shown). No second modal, no duplicated logic.
5. **Docs in sync.** `usage.md` gains a "Bridge mode" note (what the status chips and postings page mean); `dot12-logic.md` documents the capability flag, the mirror table, the callback, and the bridge-optional rule. Per the repo's docs-and-changelog discipline, these ship in the same change.

**Net:** one flag separates "DOT-12 as it is today" from "DOT-12 + automated OASIS posting." Turning the bridge off — or losing it — degrades cleanly to exactly today's manual workflow: the mirror stops updating, the chips and postings page disappear, and the Enter HRM / Enter FIN buttons are back to being human-driven. Nothing breaks, because nothing in the core app depends on the bridge being there.

---

## 7. Page Object Model strategy

This is the layer that absorbs vendor changes. Treat it as the most volatile code in the project and design accordingly.

```
oasis-bridge/
  src/oasis_bridge/
    pages/
      __init__.py
      base.py                  # BasePage: navigation, auth, wait, screenshot
      hrm/
        timesheet.py           # HrmTimesheetPage
      fin/
        equipment_usage.py     # FinEquipmentUsagePage
        oc_document.py         # FinOcDocumentPage
        direct_bill.py         # (post-discovery)
    selectors/
      hrm.py                   # Selectors: HRM_TIMESHEET = { ... }
      fin.py                   # Selectors: FIN_EQUIPMENT = { ... }
                               # selector dicts are versioned per UI release
```

**Rules:**

- **No selector outside `selectors/`.** Workers and Page objects import from there. Lint rule enforces it.
- **Every page object exposes business methods.** `add_accounting_line(line: AccountingLine)`, not `click(selector)`.
- **Every page object has `self_test()`.** It walks every selector against a known fixture record on a non-production wvOASIS instance (or, if no non-prod, a designated test-employee record on prod). Run nightly.
- **Selectors carry comments.** Each selector declares which Advantage doc-type field it maps to (`# HRM TS doc, field LDPR_PROF`). When wvOASIS publishes a UI patch, we know what we're looking for.
- **Versioning.** When a screen changes, bump the selector dict version (`HRM_TIMESHEET_V2`) and keep the old one available for 60 days so we can replay/repair posts that staged on the old screen.

---

## 8. State machine

Per posting:

```
                       ┌────────────────────────┐
                       │       received         │
                       └───────────┬────────────┘
                                   │ envelope validates, hash & updated_at fresh
                                   ▼
                       ┌────────────────────────┐
                       │        queued          │
                       └─────┬──────────┬───────┘
                             │          │ canceled by caller
                             │          ▼
                             │  ┌─────────────┐
                             │  │  canceled   │
                             │  └─────────────┘
                             │
            worker picks up  │
                             ▼
                       ┌────────────────────────┐
                       │     in_progress        │
                       └─────┬──────────┬───────┘
                             │          │ runtime / login / nav error
                             │          ▼
                             │   ┌─────────────┐
                             │   │  failed     │── retry policy applies (§9)
                             │   └─────────────┘
        write succeeds       │
                             ▼
                       ┌────────────────────────┐
                       │  staged_in_oasis       │
                       └─────┬──────────┬───────┘
                             │          │ read-back diff fails
                             │          ▼
                             │   ┌─────────────┐
                             │   │  flagged    │── routed to human, no retry
                             │   └─────────────┘
                             │
        human submits in wvOASIS
                             ▼
                       ┌────────────────────────┐
                       │     reconciled         │
                       └────────────────────────┘
```

`flagged` and `failed` are different on purpose:

- `failed` = transient or environmental (login flake, network blip). Retried with backoff.
- `flagged` = data mismatch detected after we wrote. Never retried automatically. A human reviews.

---

## 9. Idempotency, retries, and exception handling

**Idempotency:** `envelope_id` is the user-facing key. Inside wvOASIS, the `[DOT12-ENV:<envelope_id>]` tag in the document description is the durable anchor. Together they make every operation safely re-runnable.

**Retry policy:**

| State transition | Retry? | Backoff |
|---|---|---|
| `queued → in_progress` failure (worker crash) | yes | immediate, up to 3x |
| `in_progress → failed` (login error, navigation timeout) | yes | exponential, max 5 attempts, max 30 min |
| `in_progress → failed` (selector miss) | **no** | escalate to on-call; selector miss means the screen changed |
| `staged → flagged` (read-back diff) | **no** | human review |
| `staged → reconciled` failure (post-submit verification) | yes | exponential, max 3 attempts |

**Exception escalation:** any state transition into `failed` after retry exhaustion or into `flagged` ever:
1. Page on-call (or, in v1, email a defined alias).
2. Post a row to an exceptions queue visible inside DOT-12 admin UI (the `/dot12/oasis-postings` page — see §6d, capability-gated so it only appears when a bridge is configured).
3. Halt the queue if the failure rate exceeds a threshold (default: 5% in 10 minutes) — circuit breaker.

**Manual recovery path:** every flagged or failed posting can be:
- Re-driven (human clicks "retry" in DOT-12 admin) once the underlying issue is resolved.
- Marked "do not auto-post" if the human chooses to enter it manually instead.
- Linked to a manually-created wvOASIS document by pasting the doc ID — at which point the bridge marks it `reconciled` and walks away.

---

## 9a. Known wvOASIS row-flip defect (the "Use Accounting Override" bug)

**Status: known operational hazard. Must be characterized fully in §13 before any production writes.**

**Description.** On certain postbacks in the CGI Advantage Time and Leave Management timesheet edit screen, **every existing accounting line on the timesheet simultaneously and atomically flips** its `Choose Accounting` selector from `Use LDPR with Entered Accounting` to `Use Accounting Override`. The sub-detail block under each row rebinds: `LDPR Profile / Unit / Activity / Show LDPR Split` is replaced by `Override / Show AORD`. The flip is server-side, not a render glitch — the rows are now genuinely in Override mode and will book against whatever the override defaults point to.

**Confirmed trigger.** Clicking **Insert Row** from the Other Functions menu. Diagnosis from frame-by-frame analysis of a prior screen recording: a server-side row-list-rebuild defect (default-on-rebuild, lifted state, dropdown name collision, or a valueChangeListener that fans out across siblings). Deterministic, atomic, action-bound — not a race.

**Suspected additional triggers** (not yet confirmed; high priority for discovery):
- Copy Row / Paste Row / Delete Row (same Other Functions menu, almost certainly same rebuild path)
- Easy Fill template application
- View Default Accounting
- **Save / Validate / Submit** — **the existential question.** If any full-form postback triggers the rebuild, the bot has no safe path and the plan changes substantially.
- Tab-out partial postbacks from hour cells or accounting-dimension fields (CGI Advantage time grids often autosubmit on blur for total recalculation)

**Why this is more dangerous for the bot than for clerks.**
- The bot is the highest-volume Insert-Row caller in the system; the defect surface concentrates on it.
- The bot has no visual channel; it can only detect the flip if read-back explicitly checks each row's accounting-method state.
- A flipped-but-saved timesheet survives to clerk submit and books hours against override defaults instead of LDPR-derived accounts — a financial-data correctness problem with an audit trail pointing at the bot.

**Bot-side mitigations — two strategies, chosen based on §13.A discovery.**

The bot always does these two things regardless of strategy:

- **Pre-action snapshot.** Before any postback-triggering action, the bot captures `Choose Accounting`, LDPR Profile, Unit, Activity, Sub Activity, Program, Phase, Task Order, and day-cell hours for *every existing row* on the timesheet. Held in bridge DB for the duration of the posting.
- **Post-action diff.** After each action, re-read the same fields. A row whose `Choose Accounting` changed without the bot touching that row is a flip detection.

What the bot does on detection depends on which strategy §13.A says is operationally available:

**Strategy A — Detect and rebuild from snapshot (preferred if §13.A allows).** Confirmed by operator: when a row flips from LDPR to Override, the LDPR sub-detail values (LDPR Profile / Unit / Activity) are **removed**, not just hidden. They do not rehydrate by flipping `Choose Accounting` back. The bot must re-type the values from its pre-action snapshot. Strategy A is therefore "rebuild the LDPR row content from snapshot," not "just toggle the dropdown."

Operational pattern for a per-employee nightly run:

1. **Capture a full snapshot** of every existing row on the timesheet *before any postback-triggering action*: `Choose Accounting`, LDPR Profile, Unit, Activity, Sub Activity, Program, Phase, Task Order, and the 14 day-cell hours. Persist in bridge DB keyed by `(timesheet doc id, snapshot timestamp)`.
2. **Batch all Insert Row clicks first** before any value entry. If the bot needs to add three new lines tonight, do three Insert Rows back-to-back. Each Insert flips the world to Override; that's tolerable because the bot is going to rebuild everything anyway.
3. **Once all needed rows exist on the document**, walk every row (both pre-existing and bot-added) and rebuild:
   - Flip `Choose Accounting` back to `Use LDPR with Entered Accounting`.
   - Re-type LDPR Profile, then Tab. Verify acceptance (no validation error indicator).
   - Re-type Unit, Activity, Sub Activity, Program, Phase, Task Order — one field per Tab, the direct-type-and-validate pattern from §7.
   - Day-cell hours: confirm they survived the flip; re-type if missing (open §13.A item).
4. **After all rebuilds, re-read every row and diff against snapshot+new-rows.** Every row's LDPR sub-detail must match either the snapshot (for pre-existing rows) or the source envelope (for bot-added rows). Any residual mismatch → Strategy B.
5. **Save.**
6. Final read-back per §10, including per-row accounting-method verification.

This is closer to "rebuild the whole timesheet from the bot's snapshot" than "patch a single dropdown." The cost per posting scales with **total row count** on the timesheet, not just the rows the bot is adding. A 12-row timesheet with 2 new lines costs the bot 12 dropdown flips + ~70 LDPR field-writes + 2 sets of new-row hour entries — roughly 90 writes plus the postbacks they trigger. At a human-plausible cadence of ~1.5s per write, that's ~2.5 minutes per employee. For an org of 30 employees, ~75 minutes nightly. Tractable but not free, and the proposal's controller-office framing should be updated to acknowledge that the bot does meaningfully more work per night than a clerk would, *because* it operates around a vendor defect.

The auditor's view of Strategy A: "the bot rebuilds entire timesheets from its own snapshot every time it adds a row, because wvOASIS wipes LDPR sub-detail on Insert Row. The rebuild is logged write-by-write, before-and-after screenshots are captured, day-cell hours are preserved or re-typed, and no rows are saved in a flipped state." This is defensible — the bot does what a careful clerk would do — but it's a higher-touch posture than the proposal's "bot is a fast clerk" framing implied, and that should be on the table for the controller's office to see.

**Critical preconditions still gated on §13.A:**

- (a) Day-cell hours must survive the flip (or the bot must have hour values in its snapshot for every row, including clerk-authored ones — which it does for any row whose data flowed from an approved DOT-12 form, but may not for legacy / clerk-only rows).
- (b) Flipping `Choose Accounting` back to LDPR (item #13 in §13.A) must not fan out and re-flip siblings.
- (c) Re-typing LDPR sub-detail values (Tab-out partial postbacks) must not re-trigger the flip. This is a new discovery item — added to §13.A.
- (d) The bot must have snapshot data for every row it needs to rebuild. For rows authored by clerks outside the DOT-12 pipeline (leave, overtime adjustments, mid-pay-period corrections the clerk entered manually), the snapshot the bot captured at the *start* of tonight's run is the source of truth. Strategy A only works if that snapshot is faithful, which it is for the screen state but may not be for any underlying invariants the bot doesn't read.

If any of (a)–(d) fails, Strategy A is not safely available for the affected case and Strategy B (halt-and-escalate) is the only path.

**Strategy B — Halt and escalate (fallback).** When a flip is detected and Strategy A is unavailable or fails mid-repair:

1. Cancel the document without saving.
2. Mark the posting `flagged` with structured detail and pre/post screenshots.
3. Circuit-break the queue for this org. Page on-call.
4. No automatic retry. A human reviews, fixes the source timesheet, and decides whether to re-attempt.

**Which strategy applies is decided by §13.A's findings.** The three conditions that make Strategy A viable:
- (a) LDPR sub-field values survive the flip server-side (rehydrate when `Choose Accounting` is set back to LDPR), *or* are lost but the bot has the snapshot and can re-type them.
- (b) Changing one row's `Choose Accounting` dropdown does not fan out and flip siblings (no `valueChangeListener` siblings-loop bug).
- (c) The patch-back postbacks do not themselves trigger the same defect.

If (a) fails for clerk-authored rows the bot has no source data for, Strategy A is unavailable for those timesheets specifically and Strategy B fires. If (b) or (c) fail at all, Strategy A is unavailable globally and Strategy B is the only path.

**Always-on guards regardless of strategy:**
- **Read-back must include per-row accounting-method**, not just day-cells. See §10.
- **Halt-on-flip circuit breaker remains armed even under Strategy A.** A flip-rate above an agreed threshold (e.g. one in ten timesheets) trips the breaker — the defect must be fixed upstream, not papered over indefinitely.
- **Never reuse a timesheet the bot just saved without re-reading the full row state.** Multi-pass nightly runs must re-verify from scratch.

**Open existential question for discovery (§13.A).** If **Save with no edits flips rows**, the bot cannot operate safely against this OASIS instance in its current state. That outcome forces one of three responses, all of which require WVDOT-level decisions before the bot writes anything to production:
- (a) WVDOT files the defect with CGI / Deighton / wvOASIS support and waits for a fix.
- (b) WVDOT identifies a workaround at the configuration level (e.g., changing a system default so the bug-induced default matches what we want anyway — Override may already point somewhere acceptable for some orgs).
- (c) The plan is scoped down to only orgs/employees where every line is already in Override mode (so a flip changes nothing) — narrow but possibly useful.

This question is so central that **it should be the very first discovery item** — run a controlled "open a multi-row timesheet, hit Save without changes" test on ist311 and observe. If it doesn't flip, the plan proceeds with the row-action mitigations above. If it does flip, the plan needs to stop and replan.

---

## 10. Read-back verification

Two passes:

**Pass 1 — Immediately after `save_draft()`:**
- Re-open the draft via the same page object.
- For HRM timesheet: walk each accounting line and each day-cell; assert exact equality with the envelope. **Additionally verify the `Choose Accounting` selector value on every row (including rows the bot did not write tonight) matches its pre-action snapshot.** Any unexpected `Use Accounting Override` value where source says `Use LDPR with Entered Accounting` is a §9a row-flip detection — halt the posting, capture full-state screenshot, page on-call, do not retry.
- For FIN equipment / material: walk each line; assert quantity, accounting code, ED/material identity.
- Capture a full-page screenshot. Store in object storage with `posting_id` as part of the path.
- If any field mismatches → `flagged`, with a structured diff in the audit log.

**Pass 2 — After human submits (next polling cycle):**
- Query Advantage's "Documents I just submitted" list (or the OData equivalent if available for the doc type) for documents containing our idempotency tag.
- Verify the document is in submitted state.
- Mark `reconciled`. Done.

**Per-pay-period sanity check (Phase 3 onward):**
- Sum hours posted for each org unit and pay period from the wvOASIS read-back side.
- Sum hours from DOT-12 source for the same scope.
- Diff. Anything beyond a fractional rounding tolerance → human alert.

This pattern (Treasury reconciliation pattern) is what makes the bridge defensible in audit: every number that ended up in wvOASIS has a trace back to a specific approved DOT-12 row, and every approved DOT-12 row that was supposed to post is accounted for.

---

## 11. Bot identity and security controls

Mirrors OMB M-19-17 and GSA CIO-IT-Security-19-97 from the proposal.

**Identities.** Three named bot accounts, not one:
- `dot12-bot-hrm` — only the wvOASIS HRM permissions needed for timesheet entry.
- `dot12-bot-fin-equip` — only the FIN permissions needed for equipment usage.
- `dot12-bot-fin-mat` — only the FIN permissions needed for material/OC docs.

Splitting them limits blast radius and lets us disable one workflow at a time without touching the others. Each is registered to a named human sponsor (likely the controller's office for FIN; HR for HRM).

**Credential storage.** Vault (state-approved; HashiCorp Vault or AWS Secrets Manager). Bridge fetches at session-establish time, never persists, never logs. Rotation: 90 days, automated, with a graceful handoff (new password staged, sessions established with both, old password expired).

**Permissions.** Each bot account is provisioned with the **minimum** wvOASIS roles required to (a) read inventory it needs to type, (b) create draft documents in its scope, (c) save drafts. Specifically excluded: submit/approve, role assignment, configuration changes, anything financial-system administrative.

**Hosting.** Dedicated hardened VM (or container in a hardened cluster). Not a workstation. Patched on the same cadence as production servers. Egress firewalled to only `wvoasis.gov` plus the bridge API.

**Network.** mTLS between `dot12-backend` and `oasis-bridge`. Bridge does not accept inbound traffic from anywhere else.

**MFA.** If wvOASIS requires MFA for the bot account, the operationally viable options are:

| # | Method | Automatable | Recommended for this project? |
|---|---|---|---|
| 1 | **Service-account exemption** from wvOASIS security; MFA suppressed for the bot identity at the IdP level | n/a — MFA isn't challenged at all | **First ask.** Standard practice for properly-attested NPEs per OMB M-19-17. Bring the GSA RPA Security Guide CIO-IT Security-19-97 as the reference for "this is how government bot accounts work." |
| 2 | **TOTP secret in vault** (`pyotp.TOTP(secret).now()` at challenge time) | Yes — ~10 LOC | Strong fallback if exemption is denied. The vault is already the single trust boundary; holding TOTP in it alongside the password is functionally equivalent to a password-only service account. |
| 3 | **Client certificate** (machine cert / smart-card auth via Playwright's `clientCertificates` browser-context option) | Yes — standard PKI | Cleanest if WV's IdP supports machine-cert auth and the PKI infrastructure exists. |
| 4 | **YubiKey on the bot host** with a local agent for touch emulation, or YubiKey OTP via YubiCloud / self-hosted validator | Yes — but unusual operational pattern | Acceptable if security team specifically wants physical-token attestation. |
| 5 | **FIDO2 / WebAuthn via Playwright's Virtual Authenticator** (`addVirtualAuthenticator` + `addCredential`) | Yes — but IdP-side enrollment required | Escape hatch if the IdP enforces FIDO2 and won't allow TOTP. |
| 6 | **Push-based MFA** (Duo, Okta Verify, MS Authenticator push, SMS) | **No** — designed to require a human | Not viable for unattended bot. If wvOASIS security insists on push and refuses #1, the project does not have a path. |

**Recommended sequencing:**

1. One email to wvOASIS security on day one of discovery, asking which methods their bot account can enroll. The answer is usually 1–2 sentences and decides everything else.
2. If exemption is granted (#1), no MFA code in the bot at all — the login page never challenges. Best case.
3. If TOTP is on the table (#2), code is:
   ```python
   import pyotp
   totp = pyotp.TOTP(vault.get(f"{bot_identity}/totp_secret"))
   await page.fill("[name=otp]", totp.now())
   ```
   Secret enrolled once at bot-account provisioning time (read the base32 setup key from the IdP enrollment page; do not scan the QR with a phone). Stored in the same vault path as the password. Rotated on the same cadence.
4. If only client certs are offered (#3), Playwright config:
   ```python
   context = await browser.new_context(
       client_certificates=[{
           "origin": "https://wvoasis.gov",
           "certPath": "/run/secrets/bot.crt",
           "keyPath": "/run/secrets/bot.key",
       }]
   )
   ```
   Cert + key in vault-mounted tmpfs, not on disk.
5. If only push is offered, escalate to the service-account-exemption conversation with the §11 framing. State DOTs that run automation against state IdPs have been through this. If after escalation the answer is still "push only," the project does not have a path; reconvene on scope.

**Audit trail.** §12.

**Kill switch.** A single config flag (`POSTING_ENABLED=false`) drains in-progress postings, stops the queue, and prevents the API from accepting new envelopes. A second flag per kind lets us shut HRM down without touching FIN.

---

## 12. Audit log and observability

Two audit surfaces:

**(a) Posting audit table** (in the bridge's DB):

```
postings
  id (uuid)
  envelope_id (uuid, unique)
  kind, state, state_changed_at
  dot12_form_id, dot12_form_updated_at, snapshot_hash
  bot_identity, human_sponsor_user_id, approved_by_user_id
  oasis_doc_id (nullable, set when staged)
  oasis_doc_state (draft / pending / submitted)
  created_at, updated_at

posting_events
  posting_id, occurred_at, event, detail (jsonb)
  -- one row per state transition, retry, screenshot capture, diff

posting_screenshots
  posting_id, kind (pre_save, post_save, error), captured_at, blob_uri

posting_diffs
  posting_id, captured_at, diff (jsonb)
```

**(b) DOT-12-side mirror** — small additions to `dot12-backend` so the form list shows posting status next to each form: not posted / queued / staged / reconciled / flagged / failed. Click-through opens a modal with the latest screenshot and diff (proxied from the bridge so the bridge doesn't have to be exposed to the frontend). One new table:

```
dot12_oasis_postings
  id, dot12_form_id, kind, latest_state, latest_envelope_id, updated_at
```

Updated by the bridge calling back via webhook on every state transition.

**Metrics (Prometheus or whatever the state runs):**
- Postings per hour, by kind and state.
- p50 / p95 / p99 time from `received → reconciled`.
- Selector miss rate (page object self-test failures) per page object.
- Login failure rate.
- Mismatch rate (read-back diffs).
- Queue depth.

**Daily summary email** to the human sponsors: yesterday's counts in each terminal state, with links to anything in `flagged` or `failed`.

**Live + post-mortem viewing of bot activity:**

- **Playwright traces on every production posting.** Configure each `BrowserContext` with `tracing.start(screenshots=True, snapshots=True, sources=True)` at session establish and `tracing.stop(path=<posting_id>.zip)` on completion. Trace stored alongside screenshots in object storage; URI written to `posting_events`. Lets the on-call open `playwright show-trace <uri>` and scrub action-by-action through any past posting with full before/after DOM snapshots.
- **CDP port exposed for live viewing during incidents.** The bot host runs Chromium with `--remote-debugging-port=9222 --remote-debugging-address=127.0.0.1`. The port is *not* network-exposed by default; on-call engineers tunnel in via SSH (`ssh -L 9222:localhost:9222 bot-host`) and open `http://localhost:9222` in their own browser to watch a live mirror of any open page. Documented in the runbook. Never exposed to the public internet — CDP grants full remote control, not just view.
- **Headed mode locally** during all of §13 discovery, selector authoring, and dev work. `headless=False, slow_mo=300` for human-watchable pace. Never enabled in production. The fuller form of this is **development mode (Layer 3a)** — workers attach over CDP to a developer's live, logged-in browser and drive it, so the same page objects can be built and stepped through against a real human-authenticated session (how the OC/FIN automation was authored).
- **Video recording** opt-in via config flag, used sparingly for compliance demos. Heavier than traces; traces are the default audit artifact.

---

## 13. Discovery phase (the activities we run as soon as we have screen access)

This is the only phase that **requires** the wvOASIS UI. Scoped tightly so it does not block design or scaffolding.

**Discovery environment:** `ist311.wvoasis.gov` (the wvOASIS integration / staging test environment, confirmed visible in popup URLs) is the right target for all discovery and bot development. No production data, no production credentials, no real financial impact during selector authoring or page-object self-tests. Bot development can run end-to-end against ist311 before any production access is requested.

### §13.A — Row-flip defect characterization (PRECONDITION — must complete before any other discovery)

Per §9a, the project's safe-to-proceed conditions depend on understanding the full trigger set of the row-flip defect. **This is gate-zero for the project.** Run on ist311 with a test timesheet seeded with three LDPR rows. After each action, screenshot, capture the `Choose Accounting` value for every row, and DevTools-Network the postback payload + response.

| # | Test | Pass = no flip | Fail action |
|---|---|---|---|
| 1 | Open the timesheet, do nothing, wait 60 s | no flip | n/a |
| 2 | Toggle Show Accounting Details twice | no flip | confirms baseline |
| 3 | **Save with no edits** | no flip | **PROJECT-BLOCKING if it flips. Stop the plan and replan.** |
| 4 | Insert Row (Other Functions menu) | flip expected per prior recording | confirms baseline reproducer |
| 5 | Delete Row | unknown | informs row-mutation guard |
| 6 | Copy Row → Paste Row | unknown | informs row-mutation guard |
| 7 | Easy Fill | unknown | could be safer alternative path |
| 8 | View Default Accounting | unknown | |
| 9 | Tab out of an hours cell (no edit) | unknown | informs partial-postback risk |
| 10 | Tab out of an hours cell with an edit | unknown | **PROJECT-BLOCKING if it flips** — bot can't avoid editing hours |
| 11 | Change one row's `Choose Accounting` dropdown and Tab | unknown | tests valueChangeListener fan-out |
| 12 | Validate / Submit (in non-production timesheet) | unknown | |
| 13 | **After an Insert-Row-induced flip, set one row's `Choose Accounting` back to LDPR. Do sibling rows re-flip?** | no fan-out | **decides whether Strategy A (rebuild from snapshot) is available** |
| 14 | **Confirmed by operator: LDPR sub-fields (Profile / Unit / Activity) are *removed* on flip and do not rehydrate when `Choose Accounting` is set back to LDPR.** Strategy A must re-type from snapshot. Re-confirm on ist311 for the current build. | confirmed | this is *the* fact that turns Strategy A from "patch a dropdown" into "rebuild from snapshot" |
| 15 | **Do day-cell hours survive the flip, or are they wiped too?** | hours survive | if hours are wiped, snapshot must include hours for every row, including clerk-authored rows |
| 16 | **After the flip+rebuild, type an LDPR Profile value and Tab. Does the resulting partial postback re-trigger the flip on already-rebuilt rows?** | no re-flip | confirms Strategy A doesn't loop indefinitely |
| 17 | **Repeat #16 for the Activity, Sub Activity, Program, Phase, Task Order fields.** Each Tab is a postback; verify none re-triggers the flip. | no re-flip on any | each accounting dimension must be type-safe for Strategy A |
| 18 | **Batch test: add 3 rows back-to-back (3 Insert Rows in sequence). Does the third Insert wipe the values typed for the first two?** | first two values survive | if not, Strategy A must rebuild after every Insert, increasing per-row cost ~3× |

**Outputs:** a defect characterization memo listing which actions are safe, which trigger the flip, whether Strategy A (detect-and-repair) is available, and what (if any) action sequence allows the bot to add a new accounting line to a multi-row timesheet without permanently corrupting existing lines. **Until this memo exists, the project does not enter Phase 1.**

If the answer is "no safe sequence exists in current wvOASIS state," the plan halts and one of the §9a alternative responses (vendor fix, configuration workaround, scope reduction) is escalated to WVDOT leadership. The plan does not proceed to writes against production under any other condition.

1. **Login walkthrough.** Capture the actual login flow (SSO redirect, MFA prompt, post-login landing) against ist311 first, then confirm parity in production. Decide whether a service-account exemption is needed.
2. **HRM timesheet recording.** With a non-production employee on ist311, walk the entire entry flow on screen. Record:
   - DOM structure (HAR + screenshots) for the Time and Leave Management list view and the Timesheet detail screen (including the Easy Fill / Use Default Accounting / Show Average Time tab states).
   - Each field's `name`, `id`, label text.
   - Save vs. submit semantics. Confirmed from screen captures: timesheets persist in non-final states across days and submit-final is a separate, terminal action — the bot only saves; clerks submit.
   - **Direct-type-and-validate behavior for each accounting field.** Confirm that typing a valid code + Tab is sufficient (no picker popup needed) and capture: the field's invalid-value indicator (red border / inline error / cleared field) so the bot knows when validation failed, the auto-format pattern (does OASIS rewrite "261" to "261 - Patching of Bituminous Pavements"?), and the timing — does validation fire on `blur`, on `Tab`, or only on form-level save?
   - The picker popups are a fallback only. Record their selectors anyway (criteria fields, search button, result-row pattern, parent-field write-back) so the `PickerDialog` helper exists in code, but the bot's primary path is direct typing.
   - **Note:** LDPR Profile selection does *not* auto-populate downstream accounting fields. Each of the six dimensions is typed independently — but each is a one-keystroke-burst-plus-Tab, not a window-open round-trip.
   - How a new line is added (button, auto-on-blur, keyboard shortcut?).
   - Validation rules (required fields, format constraints, totals).
   - What happens on duplicate-line creation and how find-or-create should distinguish matching lines.
3. **FIN equipment doc recording.** Same as above. Determine envelope granularity (per form / per equipment / per home_unit).
4. **FIN OC document recording.** Largely de-risked — the create-and-fill flow and the accounting derivation are proven (§6c, `oasis_oc_source.py`). Remaining: confirm `oc_doc_id` is the system-assigned doc number written back onto the charge; characterize the **OC commodity grid's row-mutation behaviour** (does Add/Delete Line trigger the §9a-style postback rebuild? — drives whether `update_line`/`delete_line` need snapshot-rebuild); and pin the **draft-vs-posted edit boundary** (confirm a Submitted/Approved OC cannot be edited and that corrections must be a return/reversal OC).
5. **Direct-bill flow recording.** Same. Determine doc type.
6. **Read-back path discovery.** Confirm that drafts can be re-opened by document ID and that fields can be read back. Confirm that submitted docs are queryable (preferably via OData) for Pass-2 reconciliation.
7. **Idempotency tag placement.** Confirm a free-text field exists on each doc type for the `[DOT12-ENV:...]` tag. Pick one per doc type and document it.
8. **Selector stability test.** Open the same screen twice and diff the DOM to see which IDs are stable across sessions and which are session-scoped.
9. **Session-timeout characterization.** Idle the session and measure logout time. Determine keepalive cadence.
10. **Permissions request.** Submit the minimum-permissions list to wvOASIS security based on the recordings.

Output of discovery: three "page recipes" (HRM, FIN equip, FIN material), one "auth recipe", one "permissions ask", and a DOM snapshot per page in the repo for regression testing.

---

## 14. Phased rollout

Mirrors the proposal but adds engineering content per phase.

### Phase 0 — Build (parallel to proposal sign-off; ~3 weeks)
- Stand up `oasis-bridge` repo and CI.
- Layers 1, 2, 5 (intake API, queue, reconciliation skeleton) — fully testable with a fake page object.
- Audit tables, observability dashboards, kill switch.
- DOT-12-side mirror table and status column in the form list.
- End-to-end test against a fake page object that simulates HRM/FIN screens.

**Exit criteria:** posting envelope round-trips through the queue, fake page object stages a fake doc, reconciliation flips state, all visible in DOT-12 form list. **No real wvOASIS contact.**

### Phase 1 — Discovery + read-only shadow (~3–4 weeks after wvOASIS access)
- Run discovery (§13).
- Implement real Page Object Models against captured fixtures.
- Run the bridge in **shadow mode**: it logs in, navigates to the relevant entry screens, and **reads back what humans entered manually that day**. Diffs against DOT-12. Produces a daily reconciliation report. **No writes.**

**Exit criteria:** 14 consecutive shadow days with selector self-tests passing, agreement rate between manual entries and DOT-12 above an agreed threshold (target: 99%+, with the gap explainable by known timing differences), zero unauthorized writes attempted.

### Phase 2 — Single-district pilot, single doc type (~6–8 weeks)
- Pick one district + HRM timesheet only. Bridge writes drafts. Humans submit.
- Run alongside the existing manual entry process for 2 pay periods (overlap), comparing output.
- After 2 clean pay periods of overlap, switch the district to bridge-only entry.

**Exit criteria:** zero financial discrepancies in the post-submit reconciliation report for 60 days. Selector self-tests pass daily. Mean staffing time per pay period for that district drops by the targeted amount.

### Phase 3 — Expansion
- Add a doc type or a district at a time. Each addition has its own go/no-go gate (60 days of clean reconciliation on the previous expansion).
- Order of additions (recommended): more districts on HRM → FIN equipment → FIN material inventory → FIN material direct-bill.

### Phase 4 — Steady state
- Quarterly control review with the controller's office.
- Selector regression test included in nightly canary.
- Annual table-top of the kill switch.

---

## 15. Repo layout

```
smartcar-mms/                       # the future home (per the wvOASIS proposal merger plan)
  mms-backend/
  mms-frontend/
  dot12-backend/                    # merged in
  dot12-frontend/                   # merged in
  oasis-bridge/                     # NEW
    pyproject.toml
    src/oasis_bridge/
      api/                          # FastAPI app for intake (Layer 1)
        v1/postings.py
        auth.py
      queue/                        # Layer 2
        dispatcher.py
        models.py                   # SQLAlchemy: postings, posting_events, etc.
      sessions/                     # Layer 3
        manager.py
        vault.py
      pages/                        # Layer 4
        base.py
        hrm/
          timesheet.py
        fin/
          equipment_usage.py
          oc_document.py
          direct_bill.py
      selectors/
        hrm.py
        fin.py
      reconcile/                    # Layer 5
        diff.py
        readback.py
      audit/
        screenshots.py
        events.py
      observability/
        metrics.py
        logging.py
      cli.py                        # admin commands: replay, drain, self-test
    tests/
      unit/
      integration/                  # against fake wvOASIS
      fixtures/                     # captured DOM snapshots from discovery
    deploy/
      Dockerfile
      compose.dev.yml
      kustomize/                    # or whatever the state runs

  dot12-backend/
    routes/
      oasis_postings.py             # NEW: enqueue, status proxy, webhook receiver
    flask_models.py
      DOT12OasisPosting             # NEW: mirror table
  dot12-frontend/
    src/pages/
      DOT12List.tsx                 # NEW status column
      OasisPostingDetail.tsx        # NEW modal with screenshot + diff
```

**Why FastAPI for the bridge instead of Flask** (despite Flask being the rest of the stack): the bridge is async-friendly (Playwright, queues), has zero coupling to the existing Flask app, and FastAPI's request-validation story is cleaner for the envelope contract. If the team prefers Flask for consistency, the plan still works — it is not load-bearing on FastAPI.

---

## 16. Tech stack choices and rationale

| Concern | Choice | Rationale |
|---|---|---|
| Browser automation | Playwright (Python) | Same language as `dot12-backend`. Better than Selenium at handling proprietary widget toolkits (auto-wait, network interception, frame handling). MIT-licensed, no per-bot fees. |
| Browser binaries | Chromium (default), Firefox as fallback | Chromium is best-supported; we keep Firefox available because some Advantage screens render slightly differently and a fallback is worth having. |
| Service framework | FastAPI | Async-native, validation via Pydantic matches the envelope contract, lightweight. |
| Queue | Postgres + `SELECT ... FOR UPDATE SKIP LOCKED` | Volume is low thousands/night. No need for Redis/Celery and the operational overhead. Postgres is already standard. |
| Secrets | HashiCorp Vault or AWS Secrets Manager | Whatever WV already runs. Hard requirement: not in env files, not in code, not in images. |
| Object storage (screenshots) | S3-compatible | Whatever the state runs. Lifecycle policy: 7 years (matches financial record retention). |
| Metrics | Prometheus + Grafana | Standard. |
| Logs | Structured JSON to stdout, scraped by whatever the state runs. | |
| Headed mode for debugging | Available locally only via env flag | Dev convenience; never enabled in production. |

---

## 17. Open decision points (things to align before Phase 0 finishes)

1. **Bridge runtime location.** Same cluster as `dot12-backend`, separate cluster, or state-managed VM? Driven by where wvOASIS network access is allowed from.
2. **Bot accounts: one or three?** Plan recommends three (HRM / FIN-equip / FIN-mat) for blast-radius control. Will require three permission requests instead of one.
3. **MFA path.** Service-account exemption vs. hardware token vs. TOTP. Driven by what wvOASIS security will grant.
4. **Direct-bill material posting** — same doc type as inventory materials, or different? Discovery item, but flag for vendor confirmation early.
5. **Submit delegation, ever?** v1 says no. After 12 months of clean operation, do we revisit for narrow doc types where the human approval is already gathered upstream in DOT-12? Document the criteria now; don't build it.
6. **Form-148 / paving form integration** — out of scope for this plan, but the same bridge pattern would apply if/when needed. The `populate_*.py` scripts in this directory already produce the populated outputs; only the entry path into wvOASIS would be new.
7. **Per-pay-period sanity diff** — how strict, what tolerance? Probably 0.01 hours; confirm with controller's office.
8. **Webhook authentication from bridge → DOT-12 backend** — shared HMAC key (simple, fine) vs. mTLS (heavier, rarely worth it for inside-cluster traffic).

---

## 18. Risk register

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| 1 | Vendor pushes a UI change that breaks page objects | High over time | Medium (queue stalls; humans fall back to manual) | Daily canary with self-test, selector versioning, on-call rotation, kill switch |
| 2 | Bridge writes a draft that wvOASIS rejects on submit (validation we don't know about) | Medium (early); Low (steady state) | Low — drafts that fail to submit just route back to humans | Capture all validation rules during discovery; treat new validation errors as a learning signal, not a defect |
| 3 | DOT-12 row changes after envelope queued (race) | Low | Medium — potentially stale data in OASIS | `dot12_form_updated_at` + `snapshot_hash` mandatory; bridge refuses stale envelopes |
| 4 | Credentials leak | Low (Vault, hardened host) | High | Vault, rotation, no logging of secrets, scoped permissions, separate accounts per kind |
| 5 | Bot identity flagged for "abnormal" volume by wvOASIS security tooling | Medium | Medium | Coordinate with wvOASIS security up-front; throttle to a human-plausible rate (e.g. 1 line per 1.5s); operate in batch windows; named whitelist |
| 6 | Read-back can't fully verify a field (e.g. write-only password field on a doc) | Low for our doc types; Medium for edge cases | Low — flagged, human reviews | Document any unverifiable field in the page object and raise its review cadence |
| 7 | Vendor migrates wvOASIS to a different platform | Low (multi-year horizon) | High but slow | Whole bridge is replaceable; envelope contract survives any backend swap |
| 8 | Pay-period boundary edge cases (an employee changes home_unit mid-period; a leave correction lands after submission) | Medium | Medium | Idempotency anchor + per-pay-period sanity diff catch these; corrections re-enter as new envelopes |
| 9 | Selector miss without canary catching it | Low (canary covers all selectors) | High | Self-test must walk every selector; CI gate prevents merging selector additions without a self-test entry |
| 10 | Human submits a wvOASIS doc the bridge created and then DOT-12 changes the source row before reconciliation | Medium | Medium | Reconciliation Pass 2 uses snapshot_hash; mismatch → flagged for human; new envelope can be issued for the corrected row |
| 11 | **wvOASIS row-flip defect: every existing accounting line silently flips from LDPR to Use Accounting Override on certain postbacks (confirmed: Insert Row; suspected: Save, Copy/Delete Row, Easy Fill, blur partial postbacks)** | High that *some* triggers exist; the only question is which | Severe — hours get booked against wrong accounts, audit trail points at the bot, financial-data correctness problem | (a) §13.A discovery characterizes the full trigger set and whether Strategy A (detect-and-repair) is operationally available BEFORE any production writes. (b) Bot snapshots all rows' `Choose Accounting` + LDPR sub-fields pre-action, diffs post-action, repairs back to LDPR if Strategy A is available, halts otherwise (§9a, §10). (c) Halt-on-flip rate breaker remains armed even under Strategy A. (d) If Save itself triggers the flip and no repair path works, project halts and escalates per §9a. **Single biggest risk in the plan; treat as gate-zero.** |

---

## 19. Effort and milestones (rough order-of-magnitude)

| Milestone | Effort | Dependencies |
|---|---|---|
| Phase 0 build (everything except real page objects) | ~3 eng-weeks | none |
| Discovery (§13) | 1–2 eng-weeks | wvOASIS test access, sponsor named, bot account stub |
| Real page objects + shadow mode | 3–4 eng-weeks | discovery output |
| Phase 1 shadow run | 14 calendar days minimum | shadow mode live |
| Phase 2 single-district HRM pilot | 6–8 calendar weeks | Phase 1 exit criteria, district sponsor named |
| Phase 3 expansion | ongoing, ~1 doc type per quarter | Phase 2 stable |

Numbers assume one engineer focused; double-up speeds Phase 0 / discovery. Phase 1 and 2 are calendar-bound (need real pay periods to elapse), not engineer-bound.

---

## 20. What this plan does *not* try to do

- It does not try to be a one-pass cutover. Phased rollout with overlap is mandatory.
- It does not try to remove humans from the wvOASIS submit step. v1 cannot.
- It does not try to replace OData reads. Reads stay on OData; only writes go through the bridge.
- It does not try to handle Form-148 or other paving-form workflows. Same pattern would apply but separate doc.
- It does not try to make the bridge a general-purpose RPA platform. It is a single-purpose bridge between two known systems with a known contract. Resist the urge to generalize.

---

## 21. Immediate next actions

1. Review this plan with the controller's office and HR (they will ultimately own the human sponsor role for FIN and HRM bot accounts respectively).
2. Submit the wvOASIS access request for **discovery only** (read-only test access, no write privileges, ideally a non-prod tenant).
3. Stand up the `oasis-bridge` repo and start Phase 0 build in parallel.
4. Schedule the discovery sessions for the moment access lands.
5. Open the three bot-account permission requests once discovery confirms scope.
