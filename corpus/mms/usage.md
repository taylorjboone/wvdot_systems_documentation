# MMS — Usage Guide

The **Maintenance Management System (MMS)** is the web replacement for the
legacy Microsoft-SQL / OData maintenance application. It is the day-to-day
tool for planning, executing, and documenting road and bridge maintenance
work across the network.

This page is organized by screen. Each section says **what the screen
shows**, **what you can do there**, and **why you would go there**. Pages
are arranged in roughly the order most users encounter them.

## Map View

Path: `/map`

The Map View is the spatial workspace. It always shows whichever layer
you have made active in the Layer Sidebar, and it routes every interaction
(click, hover, sidebar query) through that layer's strategy.

### What you can see

- **Vector tiles** for the active layer — bridges as points, roads /
  CMPs / tasks as line segments, with zoom-aware rendering: bridges
  appear at zoom ≥ 5, roads at zoom ≥ 6, CMPs at zoom ≥ 10. A zoom
  indicator warns you when you are zoomed out too far for the active
  layer to render.
- **Per-layer sidebars** — Bridges, Roads, and CMP each have their own
  sidebar with three tabs: **Search**, **Visible** (everything in the
  current viewport), and **Collection** (your starred / clicked set).
- **Geomask overlay** — a translucent dimmer carves out everything
  outside your selected subject (the whole state, a WVDOT district, or
  a single county) and traces its boundary. Configure it in **User
  Settings → Map Preferences**.

### What you do there

1. **Find features.** Pan and zoom, or use the per-layer sidebar Search
   tab. Searches are fuzzy across multiple fields — route ID, label,
   county, bridge name. Press `Enter` on a highlighted match and the
   feature is added to your collection without losing keyboard focus,
   so you can chain dozens of adds in a few seconds.
2. **Build a collection.** Click features on the map to add them to the
   per-layer collection. `Shift`-click toggles multi-select mode for
   batch operations. Collections are per-layer and persist in
   `localStorage` across sessions.
3. **Open the task for a feature.** Click a feature with an existing
   task association — its summary popup includes the task ID; click the
   ID to open the Task Screen. `Cmd/Ctrl`-click opens in a new tab.
4. **Raise a task.** Right-click a road or use the road popup's **Raise
   Task from Line** / **Raise Task from Point** action to open
   `/task/create` pre-populated with that road as an asset reference,
   in a new tab.
5. **Switch to the table.** `Ctrl/Cmd + M` flips the same active layer
   into the Table View without losing filter state.

### How layers fit together

The active layer is the lens you are looking through. Switching it
changes both what you see on the map and which sidebar is active. The
five layer folders in the sidebar are:

- **Assets** — Roads, Bridges. The physical inventory the work happens
  on.
- **CMP** — Core Maintenance Plan variants. Planned segments tied to a
  plan year, surface type, and a maintenance type.
- **Inventory** — Auxiliary inventory layers (labor / equipment /
  stockpile / etc.) where applicable.
- **Work** — Tasks. Each task line on the map is a real work order
  with the geometry of its asset references.
- **Jobs** — Special entries that aren't map layers; they navigate to
  job pages (currently OASIS Integration, shortcut `C`).

## Task Screen

Path: `/tasks/:taskId` (existing task) or `/task/create` (new task)

The Task Screen is the editor for one Task — the central object that
ties everything together. Asset references, accomplishments, costs,
notes, and history all live here. Use it when you want to do anything
to a single task, end to end.

### What you can see (tabs)

| Tab | What it shows | Why you go there |
|---|---|---|
| **Details** | Organization, account code, activity, dates, status, description | Set the classification fields and lifecycle dates |
| **Accomplishments** | Daily work-report line items (one row per day per asset, with route, BMP, EMP, accomplishment, unit, activity-definition) | Record what was done on a given day, or fix a row a field crew got wrong |
| **CMP** | Core Maintenance Plan associations attached to this task | See which planned segments this task is "wrapping up" and remove ones that no longer apply |
| **Costs** | Labor, equipment, stockpile, and other transactions for this task | Inspect the cost detail behind a number you see in analytics — read-only, fed nightly by the OASIS interface |
| **Notes** | Text notes and photo/PDF attachments scoped to the task | Drop a comment, upload field photos, link an inspection report |
| **History** | Audit trail for the task and its associations | Find out who changed a field, when, and to what |

### Two sidebars

- **Left — Asset Reference List** (toggle with `` ~ `` or `Ctrl/Cmd + M`).
  Where you add, edit, and remove the roads and bridges this task is
  performed on. Pull items in from the active-layer collection, or open
  the **Add Asset** dialog (`Ctrl/Cmd + A`). Roads carry a `From → To`
  measure range; bridges carry a single BARS ID.
- **Right — Layer Sidebar** (`Ctrl/Cmd + K`). The same layer switcher
  from the Map View, available without leaving the task — useful when
  you want to search for one more road to attach.

### Asset validation

Asset references are validated automatically as you edit:

- **Roads with the same `routeid`** may **touch** at a measure boundary
  (e.g. `0–1.5` and `1.5–2.5`) but may **not overlap** (`0–1.5` and
  `1.0–2.5`). Overlapping cards highlight red on defocus.
- **Bridges** must have a unique `BARS_SID` within the task — adding a
  duplicate is blocked.

### Edit permissions by status

The task's `entity_status` controls what is editable.

| Action | Open / Issued / Active / Completed | Closed |
|---|---|---|
| Add / edit / delete asset references | Yes | No |
| Add / edit / delete accomplishments | Yes | No |
| Add / edit / delete notes | Yes | No |
| Remove CMP associations | Yes | No |
| Edit Details-tab fields | Yes | No |
| Save Changes button | Enabled | Disabled |
| View any tab | Yes | Yes |

A **Closed** task is a finalized record. The status field on the header
is always disabled — status transitions happen via workflow, not by
direct edit.

## Raising tasks from the map

A "raised" task is a new task created with assets and/or CMPs already
attached, pre-populated from somewhere else in the app. This is the
fastest way to get from a planning artifact to an executable work order.

### Raise from a road

In Map View on the Roads layer, click a road and pick **Raise Task from
Line** (or **Raise Task from Point** when you want a point asset
instead). MMS opens `/task/create?routeids=…` in a new tab with that
road already on the asset list — fill in classification fields and save.

### Raise from a road collection

In the Roads sidebar's **Collection** tab, the kebab menu's **Raise
Task** option does the same thing for every starred road at once. Use
it after you have built up a multi-segment collection with the
Search-Enter pattern.

### Raise from a CMP collection

This is the most useful raise path and a load-bearing piece of the
plan-to-execution loop.

1. Switch to the **CMP** layer. Browse on the map or in the sidebar.
2. Click CMP segments (or use the Search tab) to build a Collection of
   planned segments you intend to execute together.
3. In the CMP sidebar's **Collection** tab, kebab menu → **Raise Task
   from CMPs**. MMS opens `/task/create?cmps=[…]` in a new tab.
4. The new task arrives with two things wired up:
   - **CMP associations** on the CMP tab — each picked CMP is now
     linked, with its original measure range and plan year recorded.
   - **Asset references** on the asset sidebar — each CMP's road
     geometry comes through as a task asset, with `bmp` / `emp` copied
     from the CMP's `from_measure` / `to_measure`.

That single action collapses the "find planned work → build asset
list → link to plan" workflow into one click. The asset measures can
still be edited if you only want to execute part of the CMP, and the
CMP tab still lets you remove an association if the scope drifts.

### CMP lifecycle inside a task

A CMP is created in planning and lives at first as a free-floating row
in the CMP layer. Its lifecycle inside MMS is:

1. **Planned** — visible on the CMP map layer, no task associations,
   `entity_status` = Open or Issued.
2. **Picked up** — one or more tasks reference the CMP via the CMP tab
   (either through a raise, or by adding it from the CMP sidebar's
   "Add to existing task" action against an entered task ID).
3. **In execution** — the linked task accumulates accomplishments and
   costs against the same routes the CMP covers. Analytics pages can
   now compare planned (from CMP / annual plan) vs. actual (from this
   task) for the same scope.
4. **Wrapped up** — when the task that references the CMP is closed,
   the CMP is "done" for that segment. Multiple CMPs may roll into one
   task, or one CMP may be split across several tasks; the
   associations table is the source of truth either way.

## Accomplishment Editor

Path: `/accomplishment-editor`

The Accomplishment Editor is the **bulk-entry surface for daily work
reports**. It exists because typing accomplishments through individual
Task Screens is far too slow for crews that need to log a day's worth
of work across dozens of tasks at once.

### What you can see

- A **filter strip** at the top: Date (defaults to today), Activity,
  Organization.
- A **spreadsheet-style DataGrid** with columns Task Order ID,
  Route, BMP, EMP, Accomplishment, Activity Definition, Unit.
- An auto-populating row of **Activity Definition** and **Unit** read
  from the EAD (Effective Activity Definition) table for the entered
  Task Order ID — so you don't have to type either.
- A **Save** button that posts every valid row atomically to
  `POST /api/daily-work-report-line-items/batch`.

### What you do there

1. Pick Date, Activity, and (optionally) Organization at the top.
2. In the first row, type a 12-digit **Task Order ID**.
3. `Tab` to **Route** — pick from the autocomplete dropdown or press
   `` ~ `` to focus the route search.
4. `Tab` through **BMP** / **EMP** — these auto-skip on **blanket tasks**
   (no asset references) and **single-point assets** (e.g. bridges,
   where `from_measure == to_measure`).
5. Enter the **Accomplishment** quantity.
6. `Tab` on the Accomplishment column adds a new row and focuses Task
   Order ID, ready for the next entry. Or press `Ctrl/Cmd + D` to jump
   straight to a new last row.
7. Click **Save** — all valid rows post atomically.

### Why you would go there (and not the Task Screen)

The Task Screen edits one task at a time. The Accomplishment Editor
edits one *day* at a time across many tasks. Crew leads use it to
upload an entire shift's daily report; data clerks use it to bulk-fix a
range of dates. If you only need to fix one row, the Task Screen's
Accomplishments tab is friendlier; for anything else, this is the right
tool.

## Analytics — Org Overview

Path: `/org-overview`

The **Org Overview** is the high-level analytics dashboard — the
"is the organization on track?" view. It is intentionally a single
scrollable page so you can read it top-to-bottom.

### What you can see

- A **filter strip** with date range (and granularity: day / week /
  month, or `auto`), a **scope** toggle (Statewide / District / Org),
  and Activity filter. Date pickers default to the trailing 30 days.
- **KPI tiles** — accomplishment, total cost, labor hours, equipment
  hours, cost per unit, and accomplishment per task-day. Each tile has
  a delta badge comparing the current window to the **immediately
  preceding window of the same length** (so a 30-day window compares
  to the previous 30 days). Up/down arrows are colored by
  direction-of-good (more accomplishment is good, lower CPU is good).
- **Org stacked charts** — cost breakdown over time, by org or
  district, with a tab per metric.
- **Breakdown table** — a sortable grid showing the same totals broken
  out by Org × Activity (or any other axis combination). Filter state
  for this table is mirrored to the URL with `bd_*` params so you can
  bookmark a view.

### What you do there

- **Read it.** This is the screen you open at the start of a meeting
  to answer "what is happening this month?" — and then you drill into
  the DDL when you spot something wrong.
- **Reframe quickly.** The scope toggle and date range let you flip
  from statewide → district → single-org context without leaving the
  page. Filters round-trip through the URL.
- **Drill in.** Click a chart bucket to jump to the DDL with the
  matching date range, scope, and activities already applied.

## Analytics — DDL (Drill-Down List)

Path: `/org-overview/ddl`

The **DDL is the analytics screen you spend the most time on when
something looks wrong upstairs.** Org Overview tells you the totals are
off; the DDL tells you exactly which day-level rows are producing the
numbers, and which of them fail validation.

### What you can see

- The same **filter strip** as Org Overview, plus an **Only show
  validation issues** checkbox and a **Rule** popover that lets you
  narrow to specific validation rules (with a `(n)` count badge on each
  rule so you can see how many rows would surface before you click).
- A **DataGrid** of accomplishment-day rows. Each row is one
  `(task_id, accomplishment_date)` slice, with task order ID, org,
  activity, account code, contractor (State Forces / Contractor),
  route, BMP, EMP, accomplishment, unit, allocation share, labor /
  equipment / stockpile / other costs, total cost, and a **flag column**
  showing error / warning badges from the validation engine.
- A **detail drawer** that opens when you click a row, with five tabs:
  **Accomplishments**, **Labor**, **Equipment**, **Stockpile**, **Other**.
  Each tab lists the **constituent raw transactions** for that day —
  individual labor transaction rows, equipment hours, stockpile draws,
  miscellaneous costs — with creator, transaction date, unit cost, and
  the notes field.

### Validation rules

The DDL runs the same rule catalog the WV DOT workplan-backend has
historically used, plus the daily-production threshold checks the
Accomplishment Editor applies in real time. Current rules:

| Rule | Severity | Triggers when |
|---|---|---|
| `NO_ROUTE` | error | An accomplishment has no route name (except blanket / admin / SRIC activities) |
| `NO_LABOR` | error | An accomplishment has no labor hours reported (except activities where this is normal) |
| `NO_EQUIPMENT` | error | An accomplishment has no equipment hours (except activities where this is normal) |
| `SRIC_OUT_OF_SEASON` | error | An SRIC (snow & ice) activity logged outside Nov–Mar |
| `DAILY_PROD_ERROR` | error | Accomplishment > 20× standard daily production from the EAD |
| `NO_ACCOMP_WITH_EXPENDITURES` | warning | A task-day has labor / equipment / stockpile cost but zero accomplishment |
| `HOURS_SKEW` | warning | Labor and equipment hours differ by more than 50% (excluding hand-work activities) |
| `DAILY_PROD_WARNING` | warning | Accomplishment > 2× standard daily production from the EAD |

### What you do there

The DDL is **the intermediate analytical trail between Org Overview
totals and the raw source system records**. The flow is:

1. Spot something off in Org Overview (delta is too high, CPU looks
   wrong, total cost spiked).
2. Drill in. The DDL opens scoped to the same filters.
3. Toggle **Only issues** or pick specific rules to narrow to the
   suspect rows.
4. **Click a row.** The detail drawer opens and shows every individual
   raw record contributing to that day's totals — labor transactions,
   equipment hours, stockpile draws — with the original `created_on`,
   `created_by_id`, and notes.
5. From the drawer you can open the task in a new tab to **correct the
   error** at the source: fix a mis-entered accomplishment, attach a
   missing route, or remove a duplicate labor row. The rule that
   surfaced the row will clear automatically on the next DDL load.

This is why the DDL is vital for validation: it is the only place where
you can simultaneously see *what aggregate the number rolled up to*
and *which raw records that aggregate is built from*, with the
validation rules running over the top.

## Analytics — Org-Activity Burn Down

Path: `/org-activity-burndown`

A focused time-series for **one organization × one activity × one
fiscal year** (July 1 – June 30). Use it when the question is "are we
hitting our plan for this specific activity in this specific crew?"

### What you can see

- **Planned Accomplishment (blue dashed)** — cumulative planned units
  from the annual work plan's monthly schedule.
- **Actual Accomplishment (blue solid)** — cumulative actuals from
  daily work-report line items.
- **Planned Cost (red dashed)** — cumulative planned cost from the
  plan schedule.
- **Actual Cost (red solid)** — cumulative actual cost (labor +
  equipment + stockpile + other).
- A **summary header** with planned vs. actual accomplishment (% complete),
  total cost, CPU vs. planned CPU, and an efficiency badge.

### What you do there

- Pick **Organization**, **Activity**, and **Fiscal Year**.
- **Click-and-drag** on the chart to zoom into a date range. The chart
  switches into **Incremental** mode showing the slice relative to the
  zoom start. The brush slider below the chart tunes the window; the
  reset button returns you to the full year.

## Analytics — Activity-Org Comparisons

Path: `/accomplishments-per-unit`

A **heatmap grid** for comparing the same metric across many
organizations × activities at once. Useful for spotting outliers and
benchmarking districts against each other.

### What you can see

- **Rows** — maintenance activities (e.g. `201`, `815`), sorted by
  activity code.
- **Columns** — organizations grouped by district (first two digits of
  the org code). A district subtotal column appears at each group
  boundary.
- **Cells** — each cell shows a **Primary** value (large, top) and a
  **Secondary** value (small, bottom). A third **Style By** metric
  drives the heatmap color from cool teal (low) through amber (mid)
  to coral-red (high), scaled to the current view's maximum.
- A **detail popover** for any cell you click, with the underlying
  numbers and a link to drill into the DDL for that slice.

Available metrics: Cost / Unit (CPU), Total Cost, Accomplishments,
Planned Accomplishments, Planned CPU, and CPU Multiplier (actual ÷
planned). Use the **Orgs** and **Activities** buttons to scope the
grid; selections persist in `localStorage`.

### What you do there

Pick what to show in Primary / Secondary / Style By, scope the grid,
and read the colors. When a cell looks anomalous, drill in.

## Analytics — Annual Plan Comparison

Path: `/annual-plan-comparison`

The **deepest planned-vs-actual table** in MMS. Every activity is one
row, with both a **Planned** block (blue headers) and an **Actual**
block (green headers), plus a monthly schedule running across the
right-hand columns.

### What you can see

- **Planned columns** — accomplishment, CPU (LBR / EQP / STK / Total),
  total cost.
- **Actual columns** — accomplishment, CPU or cost subtotals, total
  cost.
- **Cost-Unit columns** — LBR (labor hours), EQP (equipment hours),
  STK (stockpile units). EH-type activities also surface a `% Δ LBR`
  and `Δ LBR` pair comparing accomplishment to labor hours; TN-type
  activities do the same against stockpile.
- **Monthly schedule** — 12 columns showing cumulative or incremental
  planned-vs-actual completion, plus a Δ column for the gap. Toggle
  with the **Cumulatives** switch.

### What you do there

Use the **CPU / Subtotals**, **Cumulatives**, **Zeros** (hide rows
with no accomplishment and no cost), and **District** rollup toggles
to reshape the table. Sortable columns and bookmarkable URLs let you
share a specific view. The Export button writes the full table to
Excel — the most common artifact for end-of-period reporting.

## OASIS Integration Job

List: `/jobs/oasis` (or press `C` from anywhere). Detail:
`/jobs/oasis/:jobRunId`.

OASIS integration ingests labor (LBR), equipment (EQP), stockpile
(STK), materials (MAT), and accounting (ACC) CSVs from the WVOasis SFTP
drop and merges them into MMS so that cost transactions show up on
tasks, on the Costs tab, and in analytics. Only admins can start a
run; everyone can watch the table.

### Jobs list — what you can see

- A `DataGrid` of recent `JobRun` rows: status pill (PENDING /
  RUNNING / SUCCEEDED / FAILED / CANCELLED), start time, duration, who
  started it. While any visible row is RUNNING the table polls every 5
  seconds so progress shows up without a manual refresh.
- A **Run Integration** button (admin only) that opens a confirm modal
  and posts `POST /api/jobs`. The backend enforces `@require_admin`
  regardless of UI state, so the button is a courtesy not a security
  boundary.

### Job detail — what you can see

The detail page mirrors the Task Screen layout with URL-driven tabs
(`?tab=summary|interfaces|cost|files|logs`):

- **Summary** — overall status, owner, duration, progress bar.
- **Interfaces** — one row per source (LBR / EQP / STK / MAT / ACC)
  with files processed, files failed, and an `OK` / `FAILED(n)` pill
  per source.
- **Cost** — cost breakdowns for I.386 and I.388 broken out by cost
  type: estimates, actuals, total inserts, estimates deleted.
- **Files** — every CSV the job touched, with its disposition.
- **Logs** — per-file log tail, capped at 200 warnings per file with a
  "suppressed N additional" footer. ERROR rows are highlighted.

### What you do there

- Watch a nightly run for trouble.
- **Cancel a running job** (admin) if a bad CSV is causing damage.
- **Inspect a failure** — go to the Logs tab and scroll to the
  per-file marker that failed. Most errors are row-level data issues
  (missing org code, malformed cost line) and surface there verbatim.
- If a job died mid-run, the next backend boot's reconciliation sweep
  flips the dangling `PENDING` / `RUNNING` row to `FAILED` with an
  explicit `error_message`, so the partial-unique-index lock that
  blocks new runs clears automatically.

## Table View

Path: `/table/:tableName`

The Table View is the data workspace mirror of the Map View. Same
active layer, same filters, no map. Use it when the question is
attribute-shaped instead of spatial-shaped: "how many tasks are
Open in District 5?" rather than "where is the work happening?"

### What you can see

- A `DataGrid` with the active layer's columns, sorted, filtered,
  and paginated. The same column filter state used here drives the
  equivalent OData query against the backend.
- Standard arrow-key pagination (`←` / `→`) when no input is focused.

### What you do there

- Apply column filters to scope the rows. Filters round-trip to the
  URL and survive a flip back to the Map View.
- Export the filtered view as CSV from the sidebar's Export button.
- `Ctrl/Cmd + M` returns to the Map View for the same active layer.

## Layer Sidebar

Open with `Ctrl/Cmd + K` or the hamburger icon at the far-left of the
navbar. While open:

| Shortcut | Action |
|---|---|
| `1` – `9` | Select the layer at that position |
| `0` | Select the layer at position 10 |
| `Esc` | Close the sidebar |

The Layer Sidebar is the only way to switch the active layer. It groups
layers into the five folders described in the Map View section
(**Assets**, **CMP**, **Inventory**, **Work**, **Jobs**). The selected
layer is highlighted with the primary color, an active left border, and
a small chip showing its hotkey position. The OASIS Integration Job
entry under **Jobs** lights up the same way when you are on any
`/jobs/oasis` route.

## Geomask — staying focused on your area

The **Geomask** is a single setting that ties together the map view,
the table view, and the Organization filter so you only have to say
"I care about District 5" (or one county, or just WV) once and the
rest of the app stays focused there.

Set it in **User Settings → Map Preferences → Map Mask**. The choices
are **Off**, **West Virginia** (default), **WVDOT District** (1–10),
or **County**.

### What it does for the map

- Draws a translucent dimmer over everything outside the subject and
  traces its boundary in black. The work area pops; the rest of the
  state recedes.
- Optionally re-centers the map to the subject's representative point
  (a point guaranteed to lie inside concave shapes — important for
  oddly-shaped counties and districts). Toggle **Re-center on geomask
  change** off if you want the mask without the camera move.
- The geomask centroid is persisted to `localStorage` as your
  "current location" so the next time you open MMS the map starts
  there.

### What it does for the Organization filter

When the geomask narrows to a district or county, the backend reports
back which organizations actually live inside that area. The
**Organization** dropdown across the app (Map View filter strip,
Table View, analytics filter strips) auto-scopes to that list — so
instead of scrolling through hundreds of statewide orgs you only see
the ones relevant to where you are looking.

Pick a different geomask, or set it back to **WV**, to widen the list.
This is how MMS keeps "what I'm looking at on the map" and "what I'm
filtering by in the dropdowns" consistent without you having to
maintain two filter states.

### What it does for the Table View

The Table View's underlying OData query is scoped by the same
`geomaskOrgIds` set. Rows for organizations outside the geomask are
filtered out server-side — so when you flip from Map → Table with
`Ctrl/Cmd + M`, the table you land on contains exactly the same scope
of records the map was showing, not the full statewide list. The CMP
map layer's tile query is scoped the same way, so the segments you see
on the map and the rows you see in the table line up.

### How it helps you stay fixed

- Set the geomask once at the start of your session and every screen
  inherits the scope — Map, Table, Analytics filter dropdowns, even
  the CMP and Organization queries.
- Switch scopes (statewide → district → county) without losing your
  active layer, your filters, or your selection.
- Because the centroid is persisted, the next session opens at the
  same place — you don't have to re-find your district every morning.

If you ever feel like you are seeing the wrong data, the geomask is
the first place to check. **User Settings → Map Mask → WV (default)**
resets the scope to the whole state without touching anything else.

## User Settings

Path: `/settings`

User Settings cover personal preferences and map defaults. They are
stored in `localStorage` under `mms_user_settings` and migrate forward
on schema bumps (current version: 2).

- **Theme** — light / dark / system.
- **Display name / email / organization** — header identity (display
  only; the authoritative identity comes from the auth layer).
- **Default map zoom** — initial zoom on first map load.
- **Measurement unit** — imperial or metric.
- **Date format** — controls how dates are rendered across the app.
- **Notifications / email notifications** — toggle the in-app and
  email notification streams.
- **Auto-save** — auto-persist task-screen edits.
- **Map Preferences → Map Mask (Geomask)** — pick what the map should
  focus on: **Off**, **West Virginia** (default), **WVDOT District**
  (1–10), or **County**. Selecting a district or county eases the map
  to that subject's representative point (a point guaranteed to lie
  inside concave shapes) and persists it as your "current location" in
  `localStorage`. Toggle **Re-center on geomask change** off if you
  want the mask to dim the map without moving it.

When the geomask narrows to a district or county, the Organization
dropdown across the app auto-scopes to organizations inside that area.

## Authentication

- **Production deployments** use SAML SSO — protected routes initiate
  SSO automatically if you are not authenticated.
- **Development deployments** show a username/password form at
  `/login`. The choice is driven by the backend's `AUTH_MODE`.
- Sessions are cookie-based with a 24-hour expiration. The app
  re-validates the session on every refresh and redirects to login if
  it has lapsed.
- After login, the app routes you back to your last visited page
  (saved in `localStorage` as `lastLocation`); if no last-location is
  recorded it falls back to `/map`.

## Versioning & Changelog

System Info in the avatar menu reads `/api/version` and shows backend
and frontend versions as colored chips. **View Changelog** opens the
in-app changelog modal, which renders `mms-backend/CHANGELOG.json`.

Backend changes land in the `backend` array; frontend changes land in
the `frontend` array. Versions are kept in sync between
`mms-backend/VERSION`, `mms-frontend/mms/VERSION`, and the `version`
field of `mms-frontend/mms/package.json`.

## Keyboard Shortcuts — Global

| Shortcut | Action |
|---|---|
| `Ctrl/Cmd + K` | Toggle Layer Sidebar |
| `Ctrl/Cmd + X` | Clear all filters (without moving the map) |
| `C` | Jump to the OASIS Integration Job page |

Global shortcuts are suppressed while the focused element is an
`<input>` or `<textarea>` so you can still type literal `k` or `c`
characters into search boxes.

## Keyboard Shortcuts — Map View

| Shortcut | Action |
|---|---|
| `Ctrl/Cmd + M` | Switch to Table View for the active layer |
| `Esc` | Exit multi-select mode |
| `1` – `9` | Select feature N from a multi-feature popup |
| `` ` `` | Focus the CMP / Roads sidebar search (when active) |

## Keyboard Shortcuts — Table View

| Shortcut | Action |
|---|---|
| `Ctrl/Cmd + M` | Switch to Map View for the active layer |
| `←` / `→` | Previous / next page in the grid |

## Keyboard Shortcuts — Task Screen

| Shortcut | Action |
|---|---|
| `~` | Toggle Asset Reference sidebar |
| `Ctrl/Cmd + M` | Toggle Asset Reference sidebar (alt) |
| `Ctrl/Cmd + K` | Toggle Layer Sidebar |
| `Ctrl/Cmd + A` | Add asset (sidebar open) **or** add accomplishment (Accomplishments tab active) |
| `Ctrl/Cmd + S` | Save asset list changes |
| `Ctrl/Cmd + 1` – `Ctrl/Cmd + 6` | Jump to Details / Accomplishments / CMP / Costs / Notes / History |
| `Ctrl/Cmd + ←` | Previous road asset in the list (wraps) |
| `Ctrl/Cmd + →` | Next road asset in the list (wraps) |
| `←` / `→` | Previous / next DataGrid page (CMP, Costs, Accomplishments) |

`Ctrl/Cmd + A` is context-sensitive — it routes to the asset sidebar's
add action or to the accomplishment modal depending on what is visible,
and it respects the task's edit permissions (no-ops when **Closed**).

## Keyboard Shortcuts — Accomplishment Editor

| Shortcut | Action |
|---|---|
| `Ctrl/Cmd + A` | Focus the Activity filter |
| `Ctrl/Cmd + O` | Focus the Organization filter |
| `Ctrl/Cmd + D` | Jump to the last row and focus the Task Order ID cell |
| `` ~ `` | Focus the Route search autocomplete in the current row |
| `Tab` / `Shift + Tab` | Move between cells |
| `Enter` | Confirm cell edit (stay in place) |
| `Tab` on the Accomplishment column | Add a new row |

## Keyboard Shortcuts — Image Viewer (Notes Tab)

| Shortcut | Action |
|---|---|
| `←` / `→` | Previous / next image |
| `Esc` | Close the viewer |
