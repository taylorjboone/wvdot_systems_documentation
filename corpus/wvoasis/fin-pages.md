# FIN pages — wvOASIS OC (Over-The-Counter) document reference

Field notes for driving the **FIN material / OC document** screens on
`uat311.wvoasis.gov` (CGI Advantage). Everything here is **confirmed live** while
building `pages/fin/oc_document.py`. Selectors live in `selectors/fin.py`; the
design/contract lives in `../WVOASIS_INTEGRATION_IMPLEMENTATION_PLAN.md` (§6c, §7).
When a UI fact here is contradicted on ist311/uat, fix the code **and** this doc
**and** the plan (CLAUDE.md rule).

An OC issues inventory from a warehouse to a task order — the FIN equivalent of a
DOT-6. One OC per DOT-12 material **charge** (`mc:<charge_id>` line_key). The bot
only ever edits **Drafts**; humans Submit (`leave_in_draft` is always true).

---

## 1. The Advantage shell — things that bite every screen

- **`#advpageload` loader mask.** A full-frame overlay that intercepts clicks
  during *every* postback. **Wait it out before every action** (`wait_loader()`,
  waits for it to be `hidden`). This was the #1 source of flakiness. If you click
  through it you get the alert *"An action is currently being performed. Please
  wait for the action to complete…"* — which means your click was **rejected**,
  not queued.
- **Main content frame.** Resolve it as
  `page.get_by_title("Main Display").content_frame` — **not**
  `frame_locator('iframe[title="Main Display"]')`, which matches **0** elements
  (it isn't a plain `<iframe title=…>`). `BasePage.main()` does this.
- **Field writes (`set_text`)** resolve in order: `input[title="X"]` →
  `input[name="X"]` → `get_by_role("textbox", name="X")` (with and without a
  trailing `" :"`). It **skips read-only / auto-populated fields** (e.g. Unit
  Price, Major Program) instead of timing out — which is also why a *legitimately*
  read-only field (see Edit mode, §4) is silently not written.
- **Checkboxes** must be found by the checkbox **role** + `name` attribute, never
  `input[name=…]` — the latter matches a hidden twin input and Playwright says
  "Not a checkbox or radio button". See `_checkbox_by_name`.
- **Components (sections)** expand/collapse via an `<img alt="Expand {section}">`
  / `"Collapse {section}"` control (`open_component` / `collapse_component`).
  Sections: **Header, Commodity, Commodity Detail, Accounting Distribution,
  Accounting, Posting**.
- **Native dialogs** — see §6. They must be **accepted deterministically**;
  Playwright auto-*cancels* unhandled ones.

---

## 2. The Document Catalog has TWO views (the big gotcha)

Both views share a **Code field** and a **"Create" link**, so a naive
"am I on the catalog?" check (`_on_catalog`: code field + Create link present)
**cannot tell them apart**. They behave very differently:

| | **Create view** (default) | **Search view** |
|---|---|---|
| Reached by | landing / clicking **Create** from Search | clicking **Search** |
| Sections | Document Identifier + **Other Options** (Auto Numbering / Create Template) | Document Identifier + **User Information** + **Document State** |
| Actions | **Create** (makes the doc) | **Browse** / Clear / **Open** / Validate / Submit / Copy + results grid |
| Auto Numbering | **present** | **absent** |
| What "Create" does | **creates** a document | **switches to the Create view** (no doc created) |

Consequences:
- **Create only works on the Create view** — the Search view has no Auto
  Numbering, so Create there asks for a manual ID and fails. This caused the
  "create always retries once" bug: the worker landed on the Search view (left
  there by a prior `open_doc`), attempt 0 failed, the failed Create bounced to the
  Create view, attempt 1 worked. Fix: `_ensure_create_view()` clicks the top
  **Create** link to switch Search→Create *without* creating a doc.
- **Open-an-existing-doc only works from the Search view** (Browse + grid). Fix:
  `open_doc` clicks **Search** first if Browse isn't present.

---

## 3. Create an OC  (`_create_oc`)

1. `_ensure_catalog()` — get onto *a* catalog view (closes an open doc via
   **Close** if needed, accepting the unsaved-changes confirm).
2. `_ensure_create_view()` — if on the Search view, click **Create** to switch.
3. Set **Code = `OC`**, **Dept = `0803`**, **Unit = `<org>`**, **ID = blank**.
4. `_ensure_auto_numbering()` — expand **Other Options** (collapsed by default;
   `DOC_AUTO_NUM` isn't present/visible until expanded), then **check Auto
   Numbering**. Uncheck **Create Template** (`CREATE_TMPL`).
5. Click **Create** → the doc opens **in edit mode**.
6. Read the assigned id from the header strip via
   `oc_header_re = Over-The-Counter\(OC\)\s*Dept:\s*\d+\s*ID:\s*(\d+)`.

**Flaky postback:** the Create postback occasionally returns to the catalog
without opening the doc. `_create_oc` **polls** for the header id (`_await_doc_id`,
loader-wait + re-read, ~15 s) and **retries once**. With the view fix this is now
rarely exercised, but kept as a safety net.

---

## 4. Open an existing OC for edit/delete  (`open_doc`) — and Edit mode

The catalog has **no "Edit" link**. To re-open a draft by id:

1. `_ensure_catalog()`; if **Browse** isn't present, click **Search** to reach
   the Search view.
2. Set Code `OC` / Dept `0803` / Unit `<org>` / **ID = `<doc_id>`**.
3. Click **Browse** — executes the query and **populates the results grid**.
4. Click the **doc-id link** in the matched row → the doc opens **read-only**.

**Fail-fast (do not loop):**
- doc-id link absent after Browse → `DocumentNotFound` (stale id / already
  discarded). **Permanent** → the worker flags it, never retries (§9 of the plan).
- opened id ≠ requested → `DocumentNotEditable` (already Submitted/Approved →
  corrections need a reversal, §6c).

### Edit mode is REQUIRED before any field is writable

A catalog-opened OC is **read-only**. You **must click the toolbar `Edit` link**
(`_enter_edit_mode`) before writing anything — otherwise fields are read-only and
`set_text` silently skips them (this was the "quantity never changed" bug). After
**Save**, the doc stays in edit mode.

Also: the **grid cell** for Requested Quantity (and friends) is **always
read-only**. The editable input is in the line's **General Information** detail
sub-form *below* the grid. Both carry `title="Requested Quantity"`; `set_text`
hits the editable one once you're in edit mode. `commodity_qty()` reads it back.

---

## 5. Fill / update / delete

### Header (`fill_header`)
Document Name, **Warehouse** (drives the auto-populated Unit Price), Requesting
Unit, Issuer ID → **Save**.

### Commodity line (`add_commodity_line`)
Open **Commodity**; if the section has 0 lines, click **Insert New Line**; set
Stock Item, Stock Item Suffix, Requested Quantity → **Save**. Unit Price
auto-populates from the warehouse (read-only — not written).

### Accounting (`add_accounting_line`)
Open **Accounting**, ensure an accounting line exists/selected, then:
- **General Information** tab → Event Type = `ST11`, Budget FY → **Save** → re-select the line.
- **Fund Accounting** tab → Fund, Sub Fund `0000`, Object `8201`, Sub Object
  `0000`, Department `0803`, Unit `<org>`, Appr Unit = appropriation.
- **Detail Accounting** tab → Activity (**code + P/N**, e.g. `261N`), Task Order,
  Program, Phase → **Save**.

### Update a line (`update_line`)
`_enter_edit_mode()` → open **Commodity** → set **Requested Quantity** (the
General Information detail input) → **Save**. Today only the **quantity** is
re-driven (the "amount changed" case the form surfaces); non-quantity edits
(warehouse/stock/task-order → accounting re-drive) are **pending discovery**.

### Delete (`discard`)
A single-commodity OC is removed by **discarding the whole document** (one OC per
charge). `discard()` clicks the toolbar **Discard** and accepts the native confirm
(§6). For the worker's delete action: if `open_doc` raises `DocumentNotFound`, the
doc is already gone → that's **success** (`removed`), not an error.
(`delete_line` for a single grid line exists but isn't exercised yet — label
unconfirmed.)

---

## 6. Native dialogs (`confirm()` / `alert()`)

Advantage uses **native browser dialogs**, and **Playwright auto-DISMISSES
(cancels) any unhandled dialog** — which silently no-ops the action. A global
`page.on("dialog", lambda d: ensure_future(d.accept()))` handler is **racy** (it
fire-and-forgets and loses the race / double-accepts → *"No dialog is showing"*).

Use `BasePage.click_accepting_dialog(locator)`: registers a **one-shot** handler,
clicks, and **awaits** the accept before continuing. Dialogs seen:

- **Discard** → `confirm`: *"You have selected to discard the current document
  version. If that was your intention, select OK. If not, select Cancel…"*.
  Must **accept** or the draft survives.
- **Close with unsaved edits** → `confirm` (accept = proceed/close).
- *"An action is currently being performed. Please wait…"* → `alert`. This is
  **not** a confirm to accept past — it means you acted before the loader settled.
  The real fix is `wait_loader()` between actions, not accepting the alert.

---

## 7. Validation  (`validate`)

Click **Validate**; read the banner:
`validation_banner_re = View All\s+1 of\s+(\d+)\s*\|\s*([^|]+?)\s+Over-The-Counter`
→ `(message_count, first_message)`. `count == 0` is clean.

Known messages:
- **Benign on uat:** *"…Task Order does not exist on the Task Order Table…"* — the
  DOT-12 task orders aren't loaded in uat's Task Order Table. Treated as clean
  (`_BENIGN_VALIDATION = ("task order does not exist",)`).
- **Real errors observed:**
  - *"Funding Total does not equal Commodity Total"* — the accounting line
    amount doesn't match the commodity line total (a real accounting bug to fix).
  - *"Budget line not found for Department/Major Program/Program Period/…"* —
    incomplete accounting (e.g. the commodity/accounting didn't fill because the
    doc was still read-only).
  - *"Document validated successfully"* sometimes appears **with `count > 0`** —
    a likely false-positive flag in the banner parse; worth confirming.

The bot **Validates then leaves the draft** (`staged_in_oasis`); it never Submits.

---

## 8. Fixed accounting codes (material OC)  (`OC_FIXED`, §6c-acct)

| Field | Value |
|---|---|
| Event Type | `ST11` |
| Object | `8201` |
| Sub Object | `0000` |
| Sub Fund | `0000` |
| Dept | `0803` |
| Activity | DOT-12 activity **+ P/N** (`is_participating ? P : N`, e.g. `261N`) |
| Fund / Appropriation Unit | from **TheHub** via the 5-digit LDPR (last-2-of-fund + first-3-of-appropriation; e.g. LDPR `17237` → Fund `9017`, Appr `23700`) — looked up, never derived arithmetically |

Built once by `dot12-backend/oasis_oc_source.py` (`--org 0711`), which emits one
ready JSON payload per material entry; the bridge consumes it.

---

## 9. Document lifecycle & states

OC: **Draft → Submitted → Approved**. *Approved means inventory has physically
left the warehouse* — irreversible. The bot edits **Drafts only**; a
Submitted/Approved OC is human-gated and corrections are a separate
reversing/correcting document (§6c, not yet built).

Posting state machine the worker drives per envelope:
`received → queued → in_progress → staged_in_oasis → reconciled | flagged | failed`,
plus `in_progress → removed` for a successful delete. **Permanent** failures
(`DocumentNotFound`, `DocumentNotEditable`, stubs) → **`flagged`** immediately
(never retried); transient → `failed` (bounded backoff retry).

---

## 10. Failure-mode cheat-sheet (what we hit & the fix)

| Symptom | Cause | Fix |
|---|---|---|
| Create always retries once | Worker on the **Search view** (no Auto Numbering) | `_ensure_create_view()` switches to Create view |
| "OC … not found in Browse results" loops forever | Stale `oasis_doc_id` + worker treated not-found as transient | `DocumentNotFound` (permanent) → `flagged`, no retry |
| Quantity edit doesn't stick | Doc opened **read-only**; grid cell read-only | `_enter_edit_mode()` (toolbar **Edit**) before writing the detail field |
| Discard "works" but draft survives | Native confirm **auto-cancelled** by Playwright | `click_accepting_dialog` one-shot deterministic accept |
| "Connection closed while reading from the driver" | Long-lived worker reused a **dead** cached browser handle (`is_connected()` lies) | `acquire()` reconnects on dead-connection errors |
| "An action is currently being performed…" | Clicked before the `#advpageload` postback settled | `wait_loader()` between actions |
| Two workers / scripts on one tab → erratic failures | Concurrent drivers on the **same** Advantage tab | run **one** browser driver at a time |

---

## 11. Selector index → `selectors/fin.py`

- **`CATALOG`** — `code_field`/`dept_field`/`unit_field`/`id_field`,
  `auto_number_checkbox` (`DOC_AUTO_NUM`), `create_template_checkbox`
  (`CREATE_TMPL`), `other_options_link`, `create_link`, `browse_link`,
  `search_link`, `close_link`, `edit_link`.
- **`DOC_SHELL`** — `loader_mask` (`#advpageload`), `main_display_frame_title`,
  `expand_img`/`collapse_img`, `insert_new_line_text`, `save_link`,
  `validate_link`, `submit_link`, `edit_doc_link`, `delete_line_text`,
  `discard_link`, and the regexes `oc_header_re` / `line_count_re` /
  `validation_banner_re`.
- **`OC_HEADER`** — `document_name`, `warehouse`, `requesting_unit`, `issuer_id`.
- **`OC_COMMODITY`** — `stock_item`, `stock_item_suffix`, `requested_quantity`,
  `unit_price` (read-only).
- **`OC_ACCOUNTING`** — the three tabs + `event_type`, `budget_fy`, `fund`,
  `sub_fund`, `object`, `sub_object`, `department`, `unit`, `appr_unit`,
  `activity`, `task_order`, `program`, `phase`.
- **`OC_FIXED`** — the fixed codes in §8.

> Catalog fields resolve by their accessible **name with a trailing `" :"`**
> (`"Code :"`, `"Dept. :"`, `"Unit :"`, `"ID :"`); the `title` attribute is just
> `"Code"` etc. `set_text` handles both.
