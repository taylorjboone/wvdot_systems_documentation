# DOT-12 — Usage Guide

DOT-12 is a digital daily labor reporting system for the West Virginia
Division of Highways. It replaces the paper DOT-12 form used to track daily
work activities, labor hours, equipment usage, and material consumption
across organizational units statewide.

This page is the day-to-day usage reference. For internal logic, validations,
and assumptions, see **DOT-12 Logic**.

## Signing In

DOT-12 lives at `https://mms.transportation.wv.gov/dot12` and is gated by
SAML SSO against your WV state account (sts.wv.gov, the same login used
for OASIS and other WV web apps).

- Visit the URL. On a site where **PIN sign-in** is switched on you first
  see a page with two buttons — **Sign in with SSO** and **Sign in with
  PIN** (see [Signing in with a PIN](#signing-in-with-a-pin) below);
  otherwise you're sent straight to the WV state sign-on page.
- Sign in with your WV credentials.
- You'll land back in DOT-12 with a session that lasts **12 hours of
  inactivity**. The clock is time since you last *did* something, so it
  keeps resetting while you work — you won't be signed out partway
  through a shift. After 12 idle hours you'll be sent through SSO again
  automatically. There's also a **24-hour ceiling** on any one sign-in, so
  you'll normally sign in once a day.

**If your session expires while a form is open:** if you leave a form
open and idle past the session window, your sign-in expires on the
server. The next time DOT-12 tries to save — a manual save, an autosave,
or a workflow action like Submit/Approve — it can no longer write to the
server. When this happens you'll get a **blocking "Session expired —
changes were not saved"** notice instead of the work failing silently in
the background. From it you can **Reload & sign in** (which re-runs SSO),
or **Dismiss** it. Important: reloading discards anything still on screen
that hadn't saved, so if you see unsaved edits, note them down before you
reload, then re-enter them after signing back in.

**First-time sign-in:** if an admin already created your account in
**Config → Users** (by e-number or email), your first sign-in lands on
that account with whatever role and org access the admin assigned. If no
account exists yet, DOT-12 provisions a **Viewer** record for you
(read-only across no orgs) and an admin needs to grant you organization
access and any elevated role before you can see forms or make edits.
Until that happens you'll see an empty form list.

**If sign-in doesn't complete:** when the round-trip through the state
sign-on page comes back without a valid session, DOT-12 shows a
"Sign-in didn't complete" screen with a **Retry sign-in** button rather
than bouncing you back and forth. If retrying doesn't help, contact an
administrator.

**Signing out:** the avatar dropdown in the navbar has a **Logout**
option. This clears your DOT-12 session but does *not* log you out of the
state SSO; closing the browser or clearing cookies does.

**Local development:** in local dev mode the SSO is replaced with a small
e-number + password form. The password is the shared dev password
configured in the dev environment. This mode requires **both** a local
backend (`ENVIRONMENT=DEV`, `LOCAL` or `STAG`) — on production the
server refuses the password form even if the page still offers it. Production
always uses SSO (or, where switched on, a PIN).

### Signing in with a PIN

*(Only where your site has switched PIN sign-in on.)* PIN sign-in is for
crew members who have **no state email or SSO account** — the normal case
for Transportation Workers filing a pre-trip from a shared tablet or their
own phone. Nothing to install and nothing to remember except four digits.

1. On the sign-in page tap **Sign in with PIN**.
2. **Find yourself** — start typing your last name (or your OASIS ID, with
   or without the leading zeros) and tap yourself in the list. Each match
   shows the name, **OASIS ID**, job title and home org, so two people with
   the same name are easy to tell apart. The list is the statewide labor
   roster from the daily inventory snapshot; if you're not on it, ask your
   supervisor to check the labor inventory.
3. **Enter your PIN.** The first time you pick your name you **choose a
   4-digit PIN** instead (and enter it twice to confirm). It can't be one
   digit repeated (`1111`) or a run (`1234`, `4321`). You'll use the same PIN
   every time after that.

You then land on **Pre-Trip** (or your Profile, where Pre-Trip is off).
Your account shows a small **PIN** chip beside the avatar as a reminder
that you're signed in on what is probably a shared device.

A few things worth knowing:

- **If your name says "sign in with SSO"** — that name is linked to a state
  account (email or e-number), so PIN sign-in is not offered for it. Use
  **Sign in with SSO** instead. If you *don't* have a state account and see
  this, an administrator needs to sort out the account under
  **Config → Users** (usually a labor code on the wrong row).
- **Wrong PIN** — after five wrong tries the PIN is locked for a minute,
  then five, fifteen and sixty minutes if it keeps happening. A correct PIN
  clears the count.
- **Forgot your PIN** (or someone set it before you did) — tap **Forgot your
  PIN? Ask your supervisor to reset it**. Your supervisor (or, if you have
  none set up, the people who approve DOT-12s for your org) gets a bell
  notification. Once they confirm, come back, pick your name, and choose a
  new PIN. Your old PIN stops working the moment they confirm.
- **Changing your PIN** — the **Profile** page has a *PIN Sign-in* card:
  current PIN, new PIN, confirm. Any other device you were signed in on is
  signed out.
- **Shared devices sign you out after 15 minutes of no activity**, and a PIN
  sign-in from a browser lasts at most 4 hours. Tap **Sign Out** in the
  avatar menu when you're done rather than walking away. An unsent pre-trip
  stays on that device as a draft either way.

### Confirming a PIN reset (supervisors)

When someone in your chain — or, for people with no supervisor set up in
**Config → Users**, someone in an org you approve DOT-12s for — asks for a
PIN reset, you get a bell notification and a **PIN Resets** entry appears
under **Config** (with a count). Open it, check the name and org, and
**Approve reset** or **Deny** (an optional note is kept with the request).
Approving clears their PIN and signs them out everywhere; they choose a new
PIN next time they sign in. Requests nobody acts on expire after 14 days.

Administrators (and anyone who could confirm a reset for that person) can
also reset a PIN directly from **Config → Users → edit → Reset PIN**. The
Users list shows each account's PIN status, and a **PIN reset pending** chip
filters to the people still waiting.

## What is DOT-12?

A DOT-12 is the daily labor report. Every DOT-12 represents one **org unit**
on one **calendar day**, and captures:

- Up to three **task asset columns** per cover sheet (more on subsequent
  sheets) — each column is one activity at one location.
- A roster of **employees** with hours charged per task asset.
- A roster of **equipment** with hours charged per task asset.
- A roster of **materials** with quantities charged per task asset.
- Header metadata: pay period, home unit, receiving unit, LDPR profile.

Forms move through an approval workflow that ends in HRM/FIN entry.

## Core Features

- Create, edit, and manage DOT-12 daily labor reports.
- Multi-column task tracking with activity codes, routes, and accomplishments.
- Employee, equipment, and material charge tracking per task.
- AI-powered chat assistant for form population and data lookup.
- PDF import with OCR for digitizing paper DOT-12 forms.
- Approval workflow: Draft → Submitted → Approved → HRM/FIN entry.
- Organization-scoped permissions with read/write access control.
- Supervisor hierarchy for the approval chain.
- Tag system for organizing and categorizing forms.
- Org View with employee hours matrix and pay period analytics.

## Creating a DOT-12 — the date is always yours to pick

**The DOT-12 date is always confirmed by you.** Every way of creating a
form — the **Create** button (forms list and My DOT-12s), the **Wizard**,
**Use as Template**, **Copy**, and the editor's **New Form** action —
first asks you to confirm the form date in a small prompt. Create-style
paths open with **today's date pre-filled** (change it or hit Enter to
accept); **Copy opens with an empty date box** — the copied form's date
is deliberately wiped. Nothing is created until you continue.

**Unusual dates ask you twice.** If the date you pick is outside the
current pay period — beyond the previous period's one-week late-entry
window, or in a future period — the prompt shows an amber warning ("you
probably don't intend this") and the first **Continue** only arms it;
you have to click **OK — use this date** a second time to go through.
This catches typos like entering 07/09 when you meant 07/29, which
would otherwise create a form that's locked the moment it exists.
Dates in the current period, or in the previous period while it's
still open for editing, continue with a single click as before.

- **Copying a form** copies everything *except* the date and the
  equipment **Ending Meter** readings — the date is wiped so the copy is
  dated consciously, and each meter is the new day's reading, entered by
  hand. You can copy
  from the list's row menu **or from inside a form**: **Actions → Copy
  DOT-12** copies the form you're looking at and opens the new copy.
- **Deleting from inside a form**: **Actions → Delete DOT-12** deletes the
  open form after a confirmation and returns you to the list. It's hidden
  once the pay period is closed (locked forms can't be deleted).
- **Changing the date on the form** (the DATE cell) now takes effect the
  moment you pick a day in the calendar — the pay-period start/end update
  immediately, no need to click away first.
- **The pay-period FROM/TO cells are read-only.** They always show the
  bi-weekly pay period that contains the DOT-12 date and can't be typed
  in or edited — to change the pay period, change the DATE cell.

## New DOT-12 Wizard

The forms list page has a **Wizard** button next to **Create**. Clicking
it launches a four-step modal that walks you through creating + setting
up a fresh DOT-12 end-to-end. A solid progress bar pinned to the top of
the modal tracks where you are in the flow, and Back / Next at the
bottom let you move between steps freely.

1. **Header** — pick the **Form Date** and your **Home Org**. Hitting
   Next creates the form (so it has a real id from this point on) and
   drops you on its page, where the wizard re-opens at Step 2.
2. **Task Assets** — the same Accomplishment View grid surface (LDPR,
   Task Order, Org, Activity, Route, BMP/EMP, Accomplishment, UOM).
   Add as many rows as you need; each row represents a column on the
   spreadsheet. **Don't worry about entering Accomplishment values for
   `EH` UOM rows** — those auto-compute later from employee hours.
3. **Workday Issues** — walks you through each task-asset column you
   just defined, one at a time. For each column you edit the long-form
   **Description**, **Weather**, **Temperature**, and **Traffic
   Control**. Weather, Temperature, and Traffic Control carry forward
   from the previous row unless you set them explicitly on the current
   one, so you only type them once when they're the same across
   columns. The header text reads: *"Document workday issues, such as:
   unauthorized absences, work rule violations and disciplinary
   action, work related injuries, supplemental reporting of work hours
   unreported within a week, etc. Fleet/Mechanics: Report
   Sub-Activities with notes, meter, WAC, Warranty, etc."*
4. **Rosters** — the same Manage Rosters tabs (Employee / Equipment /
   Material). Add everyone and everything you expect on this DOT-12.

You can close the wizard at any time — it doesn't lock anything, and
everything you've entered is already saved on the form. **Finish** on
the last step also just closes the modal; you continue working on the
form normally afterward.

## Using DOT-12 on a phone

The whole app now works on a phone-sized screen. Nothing changes on a
normal desktop screen — the phone layouts only appear on narrow
viewports (≤768px).

- **Navigation** — the top-bar links collapse into a **☰ menu button**
  on the left. It opens a drawer with everything the bar normally
  holds: My DOT-12s, your Approvals / Rejections queues (with counts),
  Reports, Config and Docs. The notification bell stays in the bar,
  and tapping your **avatar** slides your account menu up from the
  bottom of the screen (Approvals, Notifications, Profile, Send
  Feedback, System Info, Sign Out).
- **The forms list** shows each DOT-12 as a **card** instead of a table
  row — date, status, org, who created it, activity chips, description
  and tags. Tap a card to open the form; tap its **Summary** button to
  slide up the day's work summary. The toolbar wraps so search and the
  **Create** / **Wizard** buttons are always reachable.
- **Opening a form** shows a **read-only card view** of the whole
  DOT-12: a Read-only badge with an **Edit in the Wizard →** shortcut
  up top, the form header with its status, a **Checks** card listing
  any errors or warnings (tap one to jump to the problem column), one
  card per column — including participating flag, weather /
  temperature / traffic / description, and every employee, equipment
  and material charge with totals — plus the rosters, signatures and
  day summary. Locked fields carry the same color tints as the
  spreadsheet; fields with problems get a red or amber edge.
- **Want the real sheet?** Use the floating **Cards | Sheet** switch at
  the bottom. The sheet can be zoomed with a **two-finger pinch** or
  the **− / % / +** buttons (tap the % to reset). Your choice is
  remembered.
- **Entering data from a phone** — the spreadsheet itself stays
  read-only on phones; use the **Wizard** (from the list page, or
  Actions → Open Wizard on a form). It runs full-screen on phones with
  a step strip along the top, and covers the header, task assets,
  workday issues, all three rosters and final details. Submit /
  Approve / Reject and the rest of the form actions live in the
  **Actions** menu at the top right, same as on a narrow desktop
  window.
- **Save to PDF** works from the phone card view too — the exported
  PDF is identical to the desktop one (the sheet is rendered
  off-screen at full size). Because that off-screen render loads the
  full-size form first, it takes a few seconds — a **"Preparing
  PDF…"** note appears right away so you know it's working. This also
  applies to a *desktop* browser window that's narrow (or zoomed in)
  enough to show the card view.
- **Approvals on a phone** — the three queue counters at the top
  (Awaiting Approval / Pending HRM / Pending FIN) double as the queue
  switcher: tap a counter to change queues. On desktop the counters
  and the tab pills both remain.
- **Pre-Trip** *(when switched on)* is built for the phone first: big tap
  rows for the 21 checklist items, a **Check all** box at the top, and **Sign &
  submit** pinned to the bottom of the screen. Entries are kept on the phone
  until they're sent — see
  [Pre-Trip inspections](#pre-trip-inspections-config-pre-trip).
- **Reports & admin pages** (Org View, FMSUS, Timesheet Accounting,
  Production, Logs, Users, Tags, Archive, Analytics) scroll normally
  on phones; wide matrices scroll **sideways** — they keep their
  desktop shape rather than squeezing.

## Interactive Tutorial

Brand new and not sure where to start? Open the **Actions** menu and
choose **Tutorial**. It opens a guided, hands-on walkthrough on a
**throwaway practice form** — nothing you do in the tutorial is saved,
and it never touches real data.

You'll first pick how you want to learn:

- **Form View** — the full spreadsheet. The tutorial builds a complete
  DOT-12 in front of you: all five column types (**MMS, HUB, BS95, EQP,
  Leave**), a five-person crew (one with a temporary upgrade), three
  pieces of equipment, two materials, labor / equipment / material
  charges, the back pages (weather, temperature, notes), and signing.
- **Wizard & Compact** — the same form, built through the step-by-step
  wizard, then finished in Compact view for fast hour entry.

An animated pointer moves to each field, types in the value, and a glass
explainer card tells you what's happening and why. **Advance at your own
pace:**

| Key | Action |
|---|---|
| `Enter` or `→` | Run the current step and move on |
| `←` | Go back a step |
| `Esc` | Exit the tutorial |

A chapter rail on the right lets you jump straight to any section
(MMS column, Rosters, Charges, Back pages, …) or skip ahead. Exiting at
any time returns you to the forms list — nothing is left behind.

## Keyboard Shortcuts — Forms Table

| Shortcut | Description |
|---|---|
| `` ` `` | Focus the search bar |
| `` Shift + ` `` | Open remove-filter mode — lists every active filter to remove (tags, activities, orgs, creators, statuses, **pay period**, **DOT-12 date**, **By me**, and the awaiting-approval queue), with a **Remove all filters** entry pinned at the bottom when 2+ are active. Type to narrow, ↑/↓ + Enter to pick. |
| `Ctrl/Cmd + D` | Open and focus the **DOT-12 Date** filter (type `M/D` or `MMDD`, then Tab/Enter) |
| `Ctrl/Cmd + ←` | Previous page |
| `Ctrl/Cmd + →` | Next page |
| `Ctrl/Cmd + click` (on a row) | Open that DOT-12 form in a new tab |
| `Enter` | Select highlighted autocomplete suggestion (or the only suggestion) |
| `↑ / ↓` | Navigate autocomplete suggestions |
| `Escape` | Close autocomplete dropdown |

## Temp Upgrade dropdown

The **TEMP UPGRADE** column on the front of the form (column 3 of the
employee block) is filtered to the upgrade pay codes the employee's HR
job title is actually eligible for. The form looks the employee up by
their OASIS number in the home unit's labor inventory, then filters
against the HRM pay table. Each option is shown as
`{code} — {short description}` (for example `T495D — TW3CRCH`) so you
don't have to memorize the OASIS codes.

If the employee's title isn't on the pay table, or has no allowed
upgrades, the dropdown is disabled with an explanation in the
placeholder. Values that were saved before this gating still display so
you can clear them; new picks must come from the allowed set.

## Recently used picks

*Switched on per site (the `recent_picks` feature flag, off by default). When
it's off, none of this appears.*

The pickers you use most remember your **last picks** and show them at
the top of the dropdown the moment you click into the cell — before you
type anything. They're in their own **amber "Recently used" block** with a
clock icon, set apart from the normal blue search results under it.

| Field | Kept | Where it shows |
|---|---|---|
| Employee | last 10 | form name cell; Manage Rosters / template Employee picker |
| Equipment | last 10 | form ED# cell; Manage Rosters / template Equipment picker |
| Activity | last 5 | form Activity cell; Accomplishment View |
| Task order | last 5 (task orders and AssetWorks work orders) | form Task Order cell; Accomplishment View |
| Program | last 5 | form Program (account code) cell; Accomplishment View |
| Material | last 5 whole materials | form Org Whse / Description / Stock cells; Manage Rosters / template Description |

- **Only real picks count.** Something goes on the list when you pick it
  from a dropdown — not when you type, and not when the app fills a field
  in for you. Picking it again moves it back to the top. The oldest drops
  off once the list is full.
- **Each row says when you last used it** ("20 min ago", "yesterday",
  "Mar 3"), plus how many times when it's more than once ("· 3×").
  Hover the time for the exact date.
- **× removes** a row from your list without picking it.
- **Typing hides them.** The moment you type anything, the recent block
  disappears and the dropdown is just the normal search. Clear the box
  and they come back. Before you type, the arrow keys go through the
  recent rows first, and Enter on a highlighted one picks it. Enter with
  nothing highlighted does what it always did.
- **A material is the whole thing.** A recent material is its warehouse +
  description + stock item/suffix. Picking it fills all three on the row
  in one go.
- **A recent task order is re-read from DTIMS** when you pick it, so the
  column gets the task's current routes and accounting, the same as a
  typed pick.
- **Employees only show if they can go on this form**, meaning they're on
  the labor list the cell offers.
- **Kept in this browser, per person.** The lists live on this computer
  or phone, under your sign-in. They survive signing out and closing the
  browser, but they don't follow you to another device, and someone else
  signing in here sees their own list. Clearing the browser's site data
  clears them.
- The leave-request form's employee picker doesn't use or add to the
  list.

## Inventory pickers — daily refresh

Employee, equipment, and material pickers (both on the form and in
**Manage Rosters**) read from a **daily snapshot** of the OASIS labor /
equipment / stockpile feeds. The snapshot is regenerated every morning
at **7:30 AM Eastern**, after OASIS has finished its own overnight
refresh.

What this means in practice:

- **The first time you open the app each day**, the inventory snapshot
  downloads in the background. Pickers populate within a second or two.
  After that, switching forms or org units is instant — no spinner per
  cell, no per-org refetch.
- **Edits made directly in OASIS** (new hires, retired equipment, new
  warehouses, fresh stockpile quantities) appear in DOT-12 **the next
  morning**, not in real time. If you need an out-of-band refresh during
  the day, an admin can rebuild the snapshot via the backend's
  `POST /dot12/api/deighton/inventory/snapshot/refresh` endpoint — it starts
  the rebuild in the background and returns right away (the pull takes a few
  minutes); the new data appears once it finishes.
- Equipment shown in pickers is filtered to records whose ED# ends in a
  letter (the WV DOT type suffix — `A`, `R`, `E`, etc.). Records ending
  in a digit or symbol are dropped from the picker.
- Each equipment suggestion shows the **org unit the equipment belongs
  to** as a blue pill on the right edge of the row — handy when the same
  class of machine exists in several counties and you need yours.

## Equipment rows

When you pick an ED# in an equipment row, the form fills in the ED# and
its description — nothing else. **Ending Meter and Operator Initials are
entered by hand**; DOT-12 does not carry either over from an earlier form
for that piece of equipment. It does **check** the meter you type: if it's
lower than the last reading recorded for that ED# on an earlier-dated
DOT-12 (any org), the meter cell turns red and the Checks tab says which
reading it fell below (e.g. "lower than its last recorded reading, 10,400
on 09/21/2026 (DOT-12 #123)"). The initials cell helps: it drops down a
list of the **initials of everyone on the form's employee roster** — pick
one with the mouse or arrow keys + Enter, or just type anything (up to 10
characters).

After a successful ED# selection the cell **defocuses entirely** rather
than auto-moving down to the next cell.

In the equipment ED# search, pressing **Enter grabs the first suggestion**
(or the one you've arrow-keyed to) — the same as the employee search.

## Templates

From the form's **Actions** menu, **Save as Template** saves the current
form's employees, equipment, and materials as a reusable template. In that
dialog you can either:

- **New template** — name it and save a fresh template, or
- **Overwrite existing** — pick one of your existing templates and replace
  its contents with this form's rosters (its name/description are kept
  unless you change them).

**Apply Template** (Actions menu) replaces the current form's rosters with a
chosen template's — useful for recurring crews. The picker shows each
template as a card: its org chip, name, a bar showing the crew's make-up
(employees / equipment / materials), and its task order. Narrow the list
with the **search box** (matches name, description, task order, or org) and
the **org dropdown** — your own org is pinned to the top of the list.

The Overwrite picker (inside Save as Template) keeps its **"Only templates
from my home org"** checkbox. Templates remember the org of the form they
were saved from; older templates that predated this have had their org
filled in automatically from the org their crew predominantly works in
(templates whose people can't be matched show as "no org").

### The Templates page (Config → Templates)

**Config → Templates** opens a full management page for every saved
template. It uses the same card layout as the Apply Template picker —
org chip, name, crew make-up bar, task order — plus a **byline** showing
who created each template. Narrow the grid with the **search box**
(matches name, description, task order, org, or creator) and the **org
dropdown** (your own org pinned first).

Everyone signed in can browse and **View** a template — the detail view
lists its full employee, equipment, and material rosters. **Edit** and
**Delete** appear for anyone who can create DOT-12s (view-only accounts
just get View):

- **Edit** lets you rename the template, change its description and org,
  and add or remove roster rows directly — employees come from the org's
  labor roster, equipment from the ED# search, and materials from the
  same warehouse → description → stock-item picker as the form editor.
  Changes apply when you press **Save Template**; Cancel discards them.
- **Delete** permanently removes the template (after a confirmation).
  Forms it was previously applied to are not affected.

Each card shows a **byline** with who created the template (templates
saved before creator tracking existed show none). The byline is
informational — it doesn't restrict who can edit or delete — and
overwriting a byline-less template from a form records the overwriter as
its creator.

## Right Panel — Inspector

The form editor's right-side panel has five tabs, shown as icons with the
name beneath each (and a hover tooltip): **Inspector** (default), **Tasks**,
**Checks**, **Comments**, and **History**.

The **Inspector** tab is contextual — it shows details for the cell you
are **currently editing**, not just hovering. Click into a cell and the
Inspector pins to it; tab away and the last-edited cell stays pinned so
the context doesn't disappear between edits. The cell-id pill at the
top reads **editing** while the cell is in edit mode and **last edited**
afterward.

- **Employee row** — name, OASIS · upgrade, today's total hours, and a
  per-column hours breakdown.
- **Equipment row** — ED # · operator, description, ending meter ·
  status, today's total hours, per-column breakdown.
- **Material row** — description, WHSE · stock · commodity suffix, OC
  DOC ID, today's total quantity, per-column breakdown.
- **Task asset (column)** — LDPR · receiving unit, activity · work
  completed (e.g. `261 · 60 TN`), program · phase, task order # with a
  direct link to WVOasis OM, sub-activity, description, conditions
  (weather · temperature · participating · traffic-control).
- **Route & milepoints** — route, asset MP `From → To` (with display
  values dimmed in parentheses), lane, the user's input BMP `→` EMP on
  one line, plus pass/fail badges for the three milepoint rules in a
  single horizontal strip.
- **Charge** — when you focus a specific charge cell (employee hours,
  equipment hours, material quantity), the panel adds a focused card
  showing the resource and the exact charge value for that column.

The Inspector intentionally **omits** the raw account-code dimension
breakdown — the task-order link surfaces the same record in WVOasis OM
when needed.

The Inspector also surfaces a "View attachment" link when the form was
imported from a PDF.

### Checks tab

The **Checks** tab lists everything the live validation flags on the
form (the same problems that outline cells red/yellow in the sheet).
Click an entry to jump to the offending cell. Checks never block saving
— they're there so problems get fixed before submit. What gets flagged:

- **Milepoints** outside the selected route's range, or BMP > EMP.
- **Accomplishment** far above the activity's expected daily production
  (amber at ≥ 4× the average, red at ≥ 10×).
- **Column with data but no type** — pick a task order (MMS), work
  order (EQP), program (HUB/BS95), or leave code.
- **More than 24 hours in one day** on a single employee or a single
  piece of equipment, added up across every column.
- **Work-order column missing its sub-activity** (the one field you
  enter on an EQP column).
- **HUB / BS95 column missing its activity code.** (MMS and EQP columns
  aren't flagged — their activity comes from the task/work order.)
- **Equipment that worked today** but is missing **operator initials**,
  or — when the machine's class carries a meter (trucks, loaders,
  graders…) — missing its **ending meter** reading.
- **Ending meter lower than the last recorded reading** for that ED# on
  an earlier-dated DOT-12. Same-day forms aren't compared (there's no
  telling which came first). Flagged whether or not the machine worked
  today.
- **Leave hours with no leave request (DOP-L1)** covering that day — or
  only partly covered — for Annual / Sick / Bereavement / Jury / Military
  columns (Holiday and FMLA don't count), each with a **Create leave
  request →** link. Only when leave requests are switched on; see
  [Requesting leave (DOP-L1)](#requesting-leave-dop-l1).

#### When server-side checks are switched on

An administrator can switch on **server-side form rules**. They are off
by default. When they're on, the server applies the same rules every time
a DOT-12 is saved, whether from this page, the phone app, or another
system:

- **The server fills in what it owns.** Accounting from the task order,
  work order, hub project, BS95 program or leave code is filled in on the
  server, along with the pay period, the route from the task's asset, and
  EH accomplishment. If you typed something different in one of those
  cells, the server's value wins. A note pops up — *"Server updated 2
  fields"* — saying what changed.
- **Some saves are refused outright.** The save fails and the problem
  appears in the Checks tab when the data can't be right:
  - more than 24 hours in one cell
  - more than two decimal places
  - a meter reading that isn't a number
  - operator initials longer than 10 characters
  - a date in a pay period that's closed for editing
- **Submit waits for the red checks.** Errors like a column with no type,
  mileposts outside the route, or more than 24 hours in a day don't stop
  you saving a draft. They do stop **Submit**, and are marked *(blocks
  submit)*. A form can only be submitted once (again after a rejection).
- **New warnings.** The Checks tab also warns about:
  - an employee, piece of equipment or stockpile that is **retired** in
    OM_WVDOT as of the form date
  - an employee from another org
  - a temporary upgrade the employee's job title doesn't allow (this one
    blocks submit)
- **If OM_WVDOT or TheHub is unreachable,** nothing is blocked. Your values
  are kept, and the Checks tab notes they couldn't be verified.

### History tab

The **History** tab is the form's timeline. At the top, a process map
shows where the form sits in the workflow (**Prepared → Approved → HRM →
FIN**), with completed steps checked and the current step highlighted.
Below it, a newest-first list records what happened to the form:

- **Saved / Autosaved** — every save is recorded. A run of autosaves by
  the same person shows as one entry with the save count and when the run
  started (e.g. *"Autosaved · 14 saves · from 9:02 AM"*), so the list stays
  readable; pressing **Save** (or Cmd/Ctrl+S) shows as its own **Saved**
  entry. Tick **Show every save** above the list to see each save
  separately. Older entries from before this was recorded per save show as
  **Edited**.
- **Show changes** — under a save (or a run of autosaves), lists exactly
  what changed: which person, column or header field, and the old → new
  value (e.g. *"Employee hours · 0000000001 Able, Ann · Column 1 — hours:
  8 → 6.5"*), plus rows that were added or removed.
- **Changed outside the editor** — a change to the form that didn't
  come from saving it here (for example a correction made directly in the
  database, or a tag added or removed). **Show changes** lists what it
  changed.
- **Submitted / Approved / Entered in HRM / Submitted in FIN** — each
  workflow step, with who did it and when. Approved, HRM and FIN entries
  carry a **Snapshot** chip: the system keeps a copy of the form exactly as
  it was signed. Click it to see whether the form is **unchanged since
  signing** or, if not, each difference (an OC Document ID filled in after
  approval is shown as an allowed change). It also shows who signed, the
  statement they certified, and a fingerprint (SHA-256) of the signed copy.
  A grey chip means that signature was later cleared (the form was recalled
  or rejected); the copy is kept as a record.
- **Rejected** — shows the rejection reason as a quoted note.
- **Recalled to draft** — when the submitter pulls the form back.
- **Recalled to edit** — when the creator, an admin, or an HRM/FIN
  entry role (approver / timekeeper) pulls an approved form back to
  draft.

Each entry shows the person (with their avatar) and the date/time
(Eastern). **Hover any entry** for a tooltip with what occurred, who did
it, and how long ago. The tab is visible to anyone who can view the form.

## Keyboard Shortcuts — Form Editor

| Shortcut | Description |
|---|---|
| `Tab / Shift+Tab` | Navigate between cells in the spreadsheet |
| `Enter` | Confirm cell edit and move down |
| `Escape` | Cancel cell edit |
| `Ctrl/Cmd + S` | Save form |
| `Ctrl/Cmd + 1` | Switch to Normal View |
| `Ctrl/Cmd + 2` | Switch to Compact View |
| `Ctrl/Cmd + 3` | Switch to Compact-Task View |
| `Ctrl/Cmd + A` | Add Task-Asset (Column) |
| `Ctrl/Cmd + Shift + A` | Copy a Task-Order Column |
| `Ctrl/Cmd + H` | Toggle "Only Show Cover Sheets" |
| `Ctrl/Cmd + M` | Open / close the Manage Rosters modal |
| `Ctrl/Cmd + scroll` (or pinch) | Zoom the form in/out (Normal view only) |

**Zooming the form.** In **Normal view**, hold **Ctrl/Cmd and scroll** the mouse
wheel (or pinch on a trackpad) to zoom the form in or out for easier reading —
it's a view-only zoom and doesn't change the form. **Save to PDF always exports
at the standard size** regardless of your zoom, and zoom is disabled in Compact
/ Compact-Task views.

**Empty (greyed-out) columns.** Each sheet always shows three column
slots, but a form only has as many *real* task-asset columns as you've
added — any extra slots render greyed out. If you click into a greyed
slot that has no task asset behind it yet, DOT-12 pops a warning toast
("This column doesn't exist yet") in the bottom-left corner instead of
silently ignoring the click. The toast has a **+ Add column** button that
creates the task-asset column for you on the spot; you can also add one
via **Actions → Add Task-Asset (Column)** (or `Ctrl/Cmd + A`), or the
**Add column** button in the Accomplishment View. (On a locked form the
toast still appears but omits the Add button, since adding is disabled.)
However you add a column, if the new one lands **off-screen** the form
now scrolls it into view automatically.

**Copy a Task-Order Column (Actions → "Copy a Task-Order Column").**
A quick way to add a column that reuses a task order already on the form:
pick one of your existing columns from the dropdown (listed by column
number and task order), see an **Accomplishment-style preview** of the
column that's about to be added, and click **Create**. The new column
re-pulls that task order's accounting fresh from OASIS — hours, equipment
and materials are *not* copied. (Entering a brand-new, never-used task
order is done the normal way, by typing it into a column's Task Order
cell.)

**Save to PDF.** Found under **Actions → Save to PDF**. It renders the
form's sheets and **opens the PDF in a new browser tab** (rather than
forcing a download) with a logical default name — `DOT-12_<home unit>_<form
date>.pdf` — so you can preview it, then save or print from there.

**Bulk PDF download (one document).** From the **forms list**, tick the
checkboxes on the rows you want (or use the header **select-all** to grab
every form matching your current filters), then open the **⋮ menu** that
appears and choose **Download as one PDF**. Every selected form is rendered
with the same pipeline as the single **Save to PDF** and combined into **one
merged document** — `DOT-12_export_<date>.pdf` — with the forms in form-date
order (oldest first). The work runs **in your browser**, one form at a time,
with a progress bar you can cancel (canceling still downloads the forms
already captured) — so **keep the tab open and in focus** while it runs.
It's meant for batches up to **100 forms** at a time; if you select more,
narrow your selection first. (Large batches take a while — roughly a second
or two per form — so the bigger the selection, the longer the progress bar
runs.)

**Page numbers on multi-sheet forms.** A DOT-12 with more than three task
asset columns spans several sheets that all carry the **same document
number** — so each sheet now says which one it is. On the front of every
sheet, **Page 1 of 2** (and so on) sits right beside the **DOC #** in the
gray box, and the back of each sheet is labelled **DOC #… · Page 1 of 2 ·
back** in the blank strip across its top. The labels show on screen, in
**Save to PDF**, in bulk exports and when printed, and they only use space
that was already empty — no cell moves or resizes. (Single-sheet forms
simply read **Page 1 of 1**; with **cover sheets only** on, the back-page
label is hidden along with the back page.)

**Employee upgrades stand out on paper.** On every exported PDF (single or
bulk), any filled **OASIS TEMP UPGRADE** cell is printed with a **yellow
highlighter wash** so payroll can't miss an upgrade when keying from the
printed sheet.

**Header select-all respects your filters.** The select-all checkbox in the
list header selects **every form matching your current filters** (org, date
range, status, creator, pay period, tags, activity, search) across **all
pages** — so the count matches the "Showing X of N" total, not just the page
you can see.

**Bulk delete is capped at 25.** The ⋮ menu's **Delete** action removes up to
**25** DOT-12s at once. If you've selected more than 25 the dialog asks you
to deselect down to 25 first.

## Deleting a DOT-12

Deleting a DOT-12 — from the list's row menu, the bulk ⋮ menu, My DOT-12s,
or **Actions → Delete DOT-12** inside a form — removes it from every list,
report, and search.

- You can't delete a form that has been **approved**, or one whose **pay
  period is closed**.
- **Deleted something by mistake?** Ask an administrator — recently deleted
  DOT-12s can usually be restored with everything intact, including their
  workflow state. A restored form's History tab shows when it was deleted
  and restored.

**For administrators:** deleted forms land in the **Config → Archive** page
(admin role only), which lists them with org/date/search filters. From
there you can open one read-only to review its contents, and **Restore** it
back to exactly the state it was deleted in.

## Field-by-field, by column type

Every task-asset column resolves to one of four types — **MMS**,
**HUB**, **BS95**, or **EQP** — and the type decides which accounting
fields you fill in versus which the system fills and locks. The table
below is the at-a-glance summary; the sections that follow detail each
type.

**Legend:** ★ trigger (what the user picks first) · 🔒 locked · ✏️ user-editable · 🚫 disabled

| Accounting field | MMS | HUB | BS95 | EQP |
|---|---|---|---|---|
| **Program** (D2) | Auto — from task · 🔒 | ★ User-picked · ✏️ | ★ User-picked · ✏️ | Auto — EQPWO · 🔒 |
| **Task order** | ★ User-picked · ✏️ | — none (or an ED#) | — none (or an ED#) | ★ User-picked · ✏️ |
| **Activity** | Auto — from task · 🔒 (✏️ on CMR tasks) | ★ User-picked · ✏️ | ★ User-picked · ✏️ | Auto — work order · 🔒 |
| **Sub-activity** | 🚫 disabled | 🚫 disabled | 🚫 disabled | **User · ✏️** |
| **Phase** (D3) | Auto — from task · 🔒 | Auto — TheHub · 🔒 | Auto — always blank · 🔒 | 🚫 disabled |
| **Receiving unit** | Auto — task org · 🔒 | Auto — TheHub · 🔒 | Auto — D5 home unit · 🔒 | Auto — home unit · 🔒 |
| **N/P** (participating) | Auto — TheHub · 🔒 | Auto — TheHub · 🔒 | Auto — forced *Non-part.* · 🔒 | Auto · 🔒 |
| **LDPR profile** | Auto — TheHub · 🔒 | Auto — TheHub · 🔒 | Auto — BS95 crosswalk · 🔒 | Auto · 🔒 |
| **UOM** | Auto — from task · 🔒 | Auto — from activity · 🔒 | Auto — from activity · 🔒 | Auto — from activity · 🔒 |

**Net the user keys:** MMS → just the **task order**. HUB / BS95 → the
**Program**, plus **activity**. EQP → the **task order ID**, plus the
**sub-activity**. Everything else is system-populated and locked, so the
coding block that reaches the file is already internally consistent.

Sub-activity is normally greyed out outside EQP columns, with one
exception: activities that carry a **published sub-activity list of
their own** — like **568** "Miscellaneous Expenses (Overhead
authorization)" (IN00 General Overhead, IN01 Training, IN02 General
Cleaning, IN03 Supervision, IN04 Vehicle Shuttle, IN05 Meeting, IN06
Clerical, IN07 Inventory, IN08 Helping Operators). Type such an
activity in the Activity cell — **no work order needed** — and the
Sub-Activity cell opens the same searchable picker.

**CMR-task exception (MMS).** On a CMR task — a task order whose id
contains `CMR` — the **Activity** cell is *unlocked* so you can charge the
work to **any** activity, instead of being pinned to the task's standard
activity. Every other MMS-locked field (receiving unit, program, phase,
UOM, …) stays locked as usual; only Activity opens up.

The sections below detail the validation behind each filled field.

### Watch what gets filled in

When you pick a **task order**, **work order**, **program (account code)**,
or **activity**, the cells it auto-fills briefly **light up** — the trigger
cell first, then the populated cells ripple in — colored to the column type
(**MMS** indigo, **HUB** fuchsia, **BS95** amber, **EQP** green). A short
**toast** in the corner spells out exactly what was filled and why (e.g.
"Filled program, activity, phase, receiving unit, UOM and route from the
DTIMS task order — these are now locked"). Enrichment that takes a moment
(TheHub / BS95 LDPR) lights up its cells when it lands.

**Where the cursor lands after a task order.** To keep you moving, picking
a task order drops the cursor on the next field you actually need to fill:

- **Activity** — if the task didn't bring its own activity (so the cell is
  still empty).
- **DOT-12s made on a phone are marked.** A form created in the mobile
  app carries a small phone badge: spelled out as **Mobile** in the top
  bar when the form is open, and as just the phone symbol on the forms
  list and on the cards, where space is tight. Hover it to see the
  device's own record number. Forms made on the web show nothing — the
  badge only ever means "this came from the field".
- **Attach photos or videos to a column.** On the back sheet, each
  column's big description box has a **paperclip button in the bottom-right
  corner** — click it to attach a photo or a video of the work. Thumbnails
  appear in the **top-right** of the same box; click one to see it full
  size, download it, or remove it. With several on a column you can step
  through them with the **left and right arrow keys** (or the arrows on
  screen), and **Esc** closes the viewer. You can attach several to one
  column.
  Photos are shrunk automatically before they're sent, so they upload
  quickly even on a weak signal; videos have a size limit and you'll be
  told straight away if a clip is too long to send. Attachments follow the
  form: you can add and remove them while the DOT-12 is still editable,
  and they become view-only once it's approved. **They never appear on the
  printed or exported PDF** — the paper DOT-12 looks exactly as it always
  has. On a phone, the web view shows the attachments but doesn't add them
  (that's the phone app's job).
- **Dictate a column's description.** Next to the attach button, each
  back-sheet description box has a **microphone button**.
  - Click it and talk. While it's listening you'll see a red **Recording**
    panel with a timer and a sound meter that moves as you speak ("Hearing
    you — keep going"). The words themselves aren't shown while you talk.
  - Click **Stop recording** when you're done. DOT-12 then tidies what you
    said with **GK-4.7**, using what's already on the sheet: this column's
    route, program, activity and task order, plus the crew, equipment and
    materials. So "US sixty" or "county route fourteen slash two" comes out
    as **US 60** / **CR 14/2**.
  - Crew names are spelled the way they are on the DOT-12, so "jackson paw"
    becomes **Jackson Paugh**.
  - Road-work words that got mangled are fixed too: "milton" becomes
    **milled**, "coal patch" **cold patch**, "call vert" **culvert**. It
    only fixes words that were mis-heard. It doesn't add, reword, or put in
    anyone who wasn't mentioned.
  - You then see the tidied text, which you can edit, with **Heard:** and
    what was actually heard underneath.
  - **Insert** adds it to the end of the column's description. **Discard**
    throws it away. Nothing is written until you choose Insert.
  - If GK-4.7 is busy, you get exactly what was heard, with a note that the
    clean-up was skipped.
  - The recording is **never saved**. It goes straight to Oracle Cloud's
    speech service and is gone once transcribed.
  - Your browser asks for microphone permission the first time.
  - Like attachments, the mic only shows while the DOT-12 is editable, not
    on a phone-sized screen.
- **The back sheet shows the county above the route.** In each
  "COLUMN N ON FRONT" box on the back sheet, the county of the picked
  route appears on its own line directly above the route — e.g.
  **Harrison** over **US 19 SB** — on screen and on printed PDFs. It
  fills in automatically when a route is picked from the dropdown and
  clears with the route. Older forms show it after the route is
  re-picked once.
- **Optional: county inside the route cell.** There's also a compact
  display that puts the county in small type in the top-left corner of
  the route cell itself (US routes and Interstates only — they run
  across many counties). This one is **off by default** and controlled
  by the `route_cell_county_badge` feature flag; when off, route cells
  look the way they always have.
- **Route** — if the task has **more than one** asset reference, so you have
  to choose which one. The Route dropdown shows each asset's direction on a
  divided road (`Putnam US 60 EB` / `WB`), and typing in it is direction-aware
  — `us60eb`, `us 60 eb` or just `eb` all narrow to the eastbound segment. The
  route you pick is saved with its direction (e.g. `US 60 EB`).
- **BMP** — if a single route was auto-picked and it's a *segment* (not a
  point or bridge), so you enter the milepoints.
- **Accomplishment** — if there's nothing left to resolve (no asset
  references, or the auto-picked asset is a point/bridge whose BMP/EMP are
  already filled).

The advance **chains**: if it lands you on Activity, picking an activity then
carries you on to the same next stop (Route → BMP → Accomplishment) based on
what's still unfilled. So a task that doesn't bring its own activity flows
**task order → Activity → BMP** with no manual clicking in between. This same
behavior runs in both the front-page form and the **Accomplishment View**
modal.

## MMS-based columns

Task asset columns that came from MMS / Deighton (i.e. columns
populated via "Copy a Task-Order Column" or otherwise tied to a
DTIMS task) display a small indigo **MMS** chip in the top-left of
the column number strip. Hover the chip for a quick explanation.

Seven fields on an MMS-based column are **locked**: LDPR profile,
receiving unit, activity, N/P (participating), program, phase, and
unit of measure. They display the value MMS (or, for LDPR and N/P,
TheHub) gave you in a grayed-out style and won't accept edits. This
is intentional — those fields come from the source system. The chip
and the gray styling are screen-only; the values render normally on
the printed PDF.

If MMS didn't return a value for one of those fields, the cell stays
locked and blank — fix it upstream rather than typing it in here.

**Find a task order by road or bridge.** You don't have to know the
task-order number. In the **Task Order** cell you can type a **road** or a
**bridge** and the cell switches to a route search:

- A **road** — a sign system + number, optionally with a county, e.g.
  `us60 cabell`, `wv622 kanawha`, `I77`, `cr 9 wayne`. A route on its own is
  the **mainline** (sub-route `00`) — `cr21` finds CR 21, not CR 21/1; add the
  slash (`cr21/1`) to reach a sub-route.
- A **direction** on a divided road — add `eb` / `wb` / `nb` / `sb` to narrow
  to one direction, e.g. `us60eb` or `us 60 wb`. Divided roads show their
  direction on the tag (`Wayne US52EB` vs `Wayne US52WB`) so the two read
  apart.
- A **bridge** — its **BARS** number, e.g. `43A115` (two digits, a letter,
  three digits).

The dropdown then lists the **active dTIMS task orders that touch that
road/bridge**, each showing a road 🛣️ or bridge 🌉 tag, the **org**, the
**activity**, and the **last accomplishment date** recorded on that task —
newest first. If the column is **already coded** (it has an activity and/or
receiving unit), the list is **narrowed to matching task orders** — so you see
only the ones relevant to how you're charging the column. Pick one and it fills the column exactly as if you'd typed the
task-order number (same auto-fill + lock cascade). If the task order has a
**single asset on that route**, the route is auto-picked and the cursor moves
on to BMP/Accomplishment. If the route has **several milepost segments** (e.g.
two *US 60 EB* stretches), it doesn't guess — it drops you on the **Route**
cell with the dropdown already filtered to that route so you pick the right
segment. Typing a plain numeric task-order number still searches by
number as before, and `HW…` still searches AssetWorks work orders — the cell
picks the right search from what you type. Works the same in the **front-page
form** and the **Accomplishment View** modal.

**Use an equipment ED# as the task order.** For work charged to a piece of
equipment, the Task Order can hold the equipment's **ED#** instead of a
task-order number. Type 3–7 digits — with or without the dash (`137-0201` or
`1370201`) — and the dropdown lists **matching equipment** (tagged **ED#**,
with its class and org) after any task-order matches. Pick one, or press
**Enter** on an exact ED#, and the ED# goes in the Task Order — nothing else
fills in. The cursor moves to **Activity** (or **Program** if Activity is
already set): fill in Activity and Program as you normally would. **Picking
the Program keeps the ED#** — it still clears a real task order. Picking an
ED# on a column that was tied to an MMS task or an AssetWorks work order
unlinks it first, just like clearing the Task Order cell. Works the same in
the **front-page form**, the **Accomplishment View** modal and the wizard.

**Which cell controls the column.** Hover the **MMS** chip and the
**Task/Work Order** cell highlights (indigo, thick border); hover the
**HUB** chip and the **Program** cell highlights (fuchsia). That cell
is what dictates the column's type — to change or clear the type,
change or clear that field.

**LDPR + N/P from the project.** When the task order belongs to a
project (its program is a TheHub project number), the **LDPR profile**
and the **N/P (participating)** flag are filled in from that project's
phase automatically — they're the only things pulled from TheHub for a
task order; everything else still comes from MMS. Both cells are locked
(like the other MMS fields). If the project can't be reached or has no
profile, those values are left as-is.

## Leave columns (LEAV)

When you set a column's **LDPR profile** (row 1) to a leave code
(Annual, Sick, Holiday, Bereavement, Jury, Family/Medical, Military),
the column becomes a **leave column** and shows a bright **cyan LEAV
chip** in the top-left of the column strip — so leave columns stand out
from MMS (indigo), HUB (fuchsia), BS95 (amber) and EQP (green).

Picking a leave LDPR **clears the task order** and forces the canonical
leave shape: activity `003`, receiving unit = your home unit, EH units,
and the accounting fields (sub-activity, program, phase, route, BMP,
EMP) are wiped and locked. Change the LDPR back to a numeric profile to
turn it back into a normal column.

**One-click LDPR.** Click the LDPR cell once and the list pops open
immediately — pick a code and you're done (it then jumps you to the
Task/Work Order cell).

A LEAV column records the **hours**; the approval behind them is a **leave
request (DOP-L1)** — see [Requesting leave (DOP-L1)](#requesting-leave-dop-l1).
When that feature is on, the Checks tab warns about leave hours with no
request covering the day, and an approved request can create these columns
for you.

## Requesting leave (DOP-L1)

**Leave requests** are the digital version of the WV Division of Personnel
**DOP-L1 "Application for Leave With Pay"** — the paper form a supervisor
signs before annual, sick, military, jury or bereavement leave. They are a
different thing from the **LEAV columns** on a DOT-12 (see
[Leave columns (LEAV)](#leave-columns-leav)): a LEAV column is how the
*hours* reach payroll; a DOP-L1 leave request is the *approval* behind those
hours. The app links the two in both directions.

The feature is switched on **per site** by an administrator. When it's on, a
**Leave requests** link appears in the top bar (right after *My DOT-12s*; also
in the phone drawer and the avatar menu) with an **amber count** of the
requests waiting on *you* — to sign or to approve — and that count is folded
into the avatar badge too. When it's off, none of this appears and the leave
pages redirect back to the DOT-12 list.

### Starting a request

Click **New leave request** on the Leave requests page (or follow a
**Create leave request →** link from a DOT-12's Checks panel or from Org
View, which arrives pre-filled). The modal only asks *who* and *when*;
everything else is filled in on the form itself:

- **Myself** — available when your login is linked to a payroll ID (your
  **Labor Code**, set by an admin in User Management). Without one the
  button is disabled and explains: *"Your login isn't linked to a payroll ID
  yet — ask an admin to set your Labor Code."*
- **Someone in my org** — for timekeepers: pick the org (one you have
  **write** access to) and the employee from that org's labor roster.
  **The employee signs it themself** before it goes to their supervisor —
  with [PIN sign-in](#signing-in-with-a-pin) they can do that from any
  phone, and if they have no DOT-12 account yet one is created for them the
  moment you send it. (Only where PIN sign-in is *not* switched on does the
  old rule still apply: someone without a login gets certified by you.)
- **From / To** — the period of leave. The preview shows how many
  **workdays** that is — Monday–Friday, **not counting West Virginia state
  holidays** (New Year's Day, Martin Luther King Day, President's Day,
  Memorial Day, West Virginia Day, Independence Day, Labor Day, Columbus Day,
  Veterans Day, Thanksgiving, the Day After Thanksgiving, Christmas Day; a
  fixed-date holiday that lands on a Saturday is observed the Friday before,
  on a Sunday the Monday after). Weekends and holidays are skipped, but you
  can add either on the form for shift work. A request can span at most 60
  days.
- **Leave type** — the default type for every day; change individual days
  on the form afterwards.

**Start request** creates a **draft** and opens it.

### The form

The request page *is* the DOP-L1: a white, letter-size sheet with a slim
status rail beside it (above it on a phone). While the request is a draft you
edit straight on the paper — changes **autosave** a moment after you stop
typing, and the rail shows *Saving… / Saved · just now / Unsaved changes*.
Once it's signed the sheet becomes read-only and the signature boxes fill in
as it moves along.

- **NAME** is fixed to the employee (labor code beneath). **WORK
  UNIT/SECTION** and **DIVISION** are free text.
- **The eight hour boxes** — Annual · Annual (exhaustion of SL) · Military ·
  Witness/Jury Service · Sick · Sick (Imm. Family) · Sick (Death in Imm.
  Family) · Grievance Prep/Hearing — are **never typed into**. They total up
  from the **Days requested** table underneath; hovering a box highlights its
  days.
- **Days requested** — one row per workday in the period with a **Type** and
  **Hours** (default **8**, in **quarter-hour** steps, 0.25 to 24). Use
  **apply to all** on the first row to copy its type or hours down, **×** to
  drop a day (it then shows as *Not requested* with an **Add** link to put it
  back), and the *Add Sat …* / *Add Mon, Sep 7 (Labor Day)* links to include
  a weekend day or a state holiday (an added holiday row shows the holiday's
  name beside the date). Changing From/To re-lists the days but keeps
  anything you already edited. A day already
  linked to a DOT-12 is locked (🔗) — unlink that DOT-12 before changing it.
- **Military** shows an **A / B** choice once it has hours — which OASIS
  code (`MLVPA` / `MLVPB`) those days will carry; **A** is the default.
- **Sick (Imm. Family)** and **Sick (Death in Imm. Family)** show a
  **relationship** field (e.g. *spouse*); it prints in the Remarks.
- **PERIOD OF LEAVE** — the From/To dates with optional times; the A.M. /
  P.M. boxes tick themselves from the time.
- **REMARKS** — anything pertinent. **Do not include diagnoses or medical
  details** (the sheet says so). When a physician's statement has been
  provided, a ticked *Physician's statement (DOP-L3) provided* line prints
  beneath the remarks.
- The five DOP-L1 footnotes and the *FORM DOP-L1 · Page 1 of 1 · 04/25/17*
  footer print exactly as on the paper form.

### Signing and sending it for approval

**The person the leave is for signs it.** That is the default for every
request: your own you sign yourself; one a timekeeper files for you waits for
*your* signature, and you can give it from your phone after signing in with
your PIN. Find it under **Leave requests → To do** (the bell also tells you).

Signing works like a DOT-12: a confirmation dialog shows your name in your
signature font, you tick *"I certify that I am …, the person named above,
and I confirm I want to … and apply my signature"* and press the button; the
signature and date/time then write themselves into the box on the sheet.
The dialog's stepper shows the DOP-L1 route — **Employee → Supervisor →
Agency · not collected** — and, when it's going to a supervisor, *Routes to
… for approval*.

The rail offers one primary action depending on the situation:

| Situation | Button | What happens |
|---|---|---|
| Your own request (draft) | **Sign and submit** | Signs the EMPLOYEE box and sends it to your supervisor. |
| Filed for someone else (draft) | **Send to *Name* to sign** | They're notified and the request waits as **Awaiting employee signature**; when they sign (SSO or PIN — an account is created for them if they had none) it goes to their supervisor. If someone edits it while it's waiting it drops back to draft — send it again. |
| Filed for someone else (draft), **administrators only** | **Certify on their behalf (admin override)** | The exception, not the rule: you certify it in the employee's place (the sheet prints *Filed by you on behalf of Name*; the history records an administrator override) and it goes straight to the supervisor. Where PIN sign-in is not switched on, a timekeeper still gets **Sign and submit on their behalf** for someone with no login at all. |
| A request waiting on *your* signature | **Sign as employee** | Signs and submits it. |
| A submitted request you may decide | **Approve leave** / **Disapprove** | See *Who approves*. |

### Who approves

- If the employee has a **supervisor on file** (User Management → Supervisor),
  **anyone in that supervisor chain** — the direct supervisor or anyone above
  them — can approve or disapprove. No approver role is needed; being their
  supervisor is enough.
- If there's **no supervisor on file** (or the employee has no login), the
  request goes to an **administrator** instead — except whoever filed it.
  The rail says so: *"No supervisor is on file for this employee, so an
  administrator will review it."* Ask an admin to set the employee's
  supervisor in User Management so it routes to the right person.
- Admins can always approve. Nobody approves **their own** request.

### Who gets notified

Being able to approve a request and being **notified** about it are not the
same thing.

- When a request is submitted, the bell notification always goes to the
  employee's **direct supervisor**. The same goes for the notice that a
  pending request was withdrawn.
- People **higher up the chain** are notified only if they asked to be, under
  **Avatar → Profile → Email & notifications → Who you hear about**. The
  default there, **My people only**, stops at your direct reports;
  **Everyone below me** (or **Everyone in my orgs**) adds every level below
  you. See [Email & notifications](#email--notifications).
- The **Leave requests to approve** section of your email digest follows the
  same choice.
- This changes only what you're *told*. If you supervise supervisors, you
  can still open and decide any request from anyone below you: they all stay
  in **Avatar → Approvals → Leave to approve** and in the Leave requests
  **To do** view, and they still count on the badge.
- A request for someone with **no supervisor on file** still notifies the
  administrators, since they're the only ones who can act on it.

### Who can see a leave request

A leave request can be opened only by:

- the **employee** it's for,
- whoever **filed it on their behalf**,
- anyone in the employee's **supervisor chain** (direct supervisor and up),
- **admins**.

Having access to the employee's org is **not** enough — a timekeeper or
DOT-12 approver who isn't in the chain can't open it, and it doesn't appear
in their lists. Elsewhere they see only its **status**: the Org View glyph
still shows (pending / approved / approved and on a DOT-12) and still clears
missing time, but its sidebar reads *"On file · approved — only the
employee, their supervisor chain and admins can open it."* with no request
number, leave type, hours or link. On a DOT-12's Checks panel, a request they
can't see is reported as *"… hours are not fully covered by a leave request"*
without amounts.

The rail's *Waiting for … to approve* line names who's next. Approving signs
the IMMEDIATE SUPERVISOR box (**Approved**); **Disapprove** asks for a reason
(required), marks the box **Disapproved**, and notifies the employee and the
filer. The AGENCY-AUTHORIZED line stays blank — that signature isn't
collected in this system.

**Other actions.** **Withdraw** (employee, filer, or admin) cancels a draft,
awaiting, or submitted request — it leaves every queue and can be **Reopened
as draft** later. A **disapproved** request can also be reopened (by the
employee, the filer, or an approver) to fix and resubmit; reopening clears the
signatures and the decision, and isn't allowed while a linked DOT-12 is
already approved. **Delete draft** archives a draft (or a withdrawn /
disapproved request) — it disappears from every list and only an admin can
restore it. Approved requests can't be withdrawn or deleted in the app.

### Policy reminders

The rail lists reminders drawn from the DOP-L1 footnotes and DOP rules. They
are **advice only — nothing here blocks signing or approval**:

- **More than 3 consecutive sick workdays** (Sick or Sick (Imm. Family);
  Friday → Monday counts as consecutive and so does a run across a state
  holiday — neither is a break — and the employee's other open requests are
  counted too) → a **physician's statement (DOP-L3)** is
  required. The approver, the filer, or an editor ticks **Physician's
  statement (DOP-L3) provided** on the rail once it's in hand, which clears
  the reminder and prints the line on the sheet.
- **Death in immediate family over 3 days** — the allowance is 3 days per
  occurrence.
- **Family sick leave over 80 hours** in the calendar year, counting the
  employee's other requests in this app.
- **Family or bereavement leave with no relationship** entered (while
  editing).
- **Military or jury leave** — attach the orders / summons (info).
- **Annual leave for dates already past** — retroactive annual leave (info).

### Save to PDF

**Save to PDF** on the rail renders the sheet exactly as shown — signatures,
day table, footnotes — to a one-page US-Letter PDF named
`DOP-L1_LASTNAME_<from date>_<id>.pdf`, opened in a new tab (or downloaded if
the tab is blocked). Buttons and editing controls are left out.

### From an approved request to DOT-12s

Once a request is **approved**, the rail shows **Create N DOT-12s for
<dates>?** to anyone who can see the request (see *Who can see a leave
request*) **and** can edit DOT-12s for the employee's org — one per leave
day in the employee's org, with the hours and
leave code listed and the pay period noted. **Create N DOT-12s** makes one
**draft DOT-12 per day**, each with the employee's row and a **LEAV column**
in the canonical shape (activity `003`, EH, receiving unit = home unit — see
[Leave columns (LEAV)](#leave-columns-leav)) carrying the hours, and links
them to the request. You still open, review and **submit each DOT-12 as
usual** — the request never bypasses the timesheet workflow.

- If a DOT-12 for that day **already lists the employee with the same kind
  of leave**, it's **linked** instead of duplicated.
- Days whose **pay period has already closed** are skipped, and grievance
  days never create a DOT-12 (there's no OASIS code for grievance leave).
- Clicking again does nothing new — already-linked days are skipped.
- **Not now** hides the banner on this browser. Linked DOT-12s show as chips
  (**DOT-12 #id · date · status**); a chip turns amber with a note when the
  timesheet drifts from the request — *hours differ*, *leave code differs*,
  *archived*, *rejected*, *leave column removed*.

Anyone with **write access to the org** can create the DOT-12s — the same
right needed to create them by hand.

### From a DOT-12 to a leave request

The bridge runs the other way too, so leave hours don't reach payroll without
their DOP-L1:

- **Checks panel warning.** While you edit a DOT-12, the **Checks** tab warns
  *"Doe, Pat has 8 h ANNLV with no leave request (DOP-L1)."* for each
  employee whose leave column (Annual, Sick, Bereavement, Jury, Military —
  **Holiday and FMLA columns don't count**) has no request covering that
  day, and *"… has 8 h SCKLV covered for 4 of 8 h by a leave request
  (DOP-L1)."* when a request exists but is short. Each warning carries a
  **Create leave request →** link (or **Open leave request →** for the short
  case) that opens the New request modal pre-filled with the employee, org,
  date and leave type. Any request that isn't withdrawn or disapproved
  counts as covering — draft, awaiting signature, submitted or approved.
  These are soft warnings; they never block saving or submitting.
- **After you submit.** If the DOT-12 you just submitted still has uncovered
  leave hours, a **Leave requests for this DOT-12** checklist appears once
  (per form, per browser session). Each employee is listed with the
  uncovered hours and whether they *have a login → they'll be asked to sign*
  or *no login → you'll certify on their behalf*. **Create N draft
  requests** files a draft DOP-L1 **on their behalf** for that day,
  pre-filled and linked to the DOT-12 (find them under Leave requests →
  Mine); **Skip** does nothing. Your submission has already gone through
  either way.

### Leave requests in Org View

In **Reports → Org View** (Labor), the **Leave requests** pill marks each
leave day with a small triangle in the corner of its cell:

| Corner mark | Meaning |
|---|---|
| **Grey** | Leave hours on a DOT-12 but **no leave request** filed (holiday `HOLLD` and `FMSUS` hours never need one, so they get no mark) |
| **Amber** | A request is **pending** — draft, awaiting signature, or submitted |
| **Amber with a white notch** | **Approved**, but **no DOT-12 carries it yet** |
| **Green** | **Approved and carried by a DOT-12** |

Only the **green** state satisfies the red **missing time** flag — an
approved request isn't payroll until its DOT-12 exists. Days that have a
request but no hours yet appear as clickable zero cells. Click a cell and the
sidebar's **Leave request** block links to the DOP-L1 (*DOP-L1 #12 · approved
· 8.0 h ANNLV*) — if you're allowed to see it (see *Who can see a leave
request*); otherwise it shows the status only — with a **✓ DOT-12 #n** badge — or a *DOT-12 not created*
badge and a **Create the DOT-12 from the request →** link; when none is
filed it says so and, if you can edit the org, offers **Create leave request
→**. The pill state is remembered per browser and shared in the URL
(`leave=1`). The Org View Excel export includes a **leave_requests** sheet —
request hours per employee per day, green for approved-and-linked, amber for
anything else pending.

### Approvals page, To do, and notifications

- **Avatar → Approvals** gains a **Leave to approve** tile listing the
  submitted requests you may decide (employee · hours · leave types · status);
  clicking a row opens the request. The **Org** filter and **Direct reports
  only** switch apply; *My people only* is hidden because leave requests are
  already scoped to your supervisor chain. Supervisors who aren't DOT-12
  approvers still get the page while they have leave waiting. This list is
  everything you *may decide*, which can be more than you were notified
  about — your notifications and digest cover the people you chose under
  Profile → Email & notifications (see *Who gets notified*).
- On the **Leave requests** page, **To do** groups everything waiting on you
  — *Waiting for your signature* and *Waiting for your approval* — and opens
  first when something's there. **Mine** is what you filed or what's yours;
  **To approve**, **Org** (pick an org — it lists only the requests you're
  allowed to see there) and **All** (admins) are the wider views. Filter by status chip, date range, or *name, labor code, #id*.
- You're **notified** (bell and Notifications page — filter chip **Leave**)
  when a request needs your **signature** or **approval**, when yours is
  **approved**, **disapproved** (with the reason) or **withdrawn**, and when
  **DOT-12s are created** from it. Each notification opens the request.
  Remarks are never included in a notification.

## Pre-Trip inspections (Config → Pre-Trip)

*(Only when the Pre-Trip feature is switched on for your site.)* The paper
WVDOT **Operator's Daily and Weekly Checklist for Transportation and Heavy
Equipment** now lives in the app under **Config → Pre-Trip**. It's built for
the phone: operators file one for their truck each day before they drive, and
supervisors sign off the week the way they approve a DOT-12.

### Filing a pre-trip (operators)

1. **Config → Pre-Trip → New pre-trip.** (A link like
   `/dot12/pretrip/new?ed_number=3771602` — e.g. on a sticker or QR code in
   the cab — opens the form with that truck already filled in; `?ed=` works
   too. If you aren't signed in yet you're taken through sign-in — SSO or
   PIN — and land on the prefilled form afterwards.)
2. **ED number** — type the 7-digit equipment number (`377-1602` or
   `3771602`); matching trucks are listed under the box as you type. Once all
   7 digits are in, a green chip confirms the truck, its type and its org.
   - If the truck belongs to an **Equipment Shop** or the **Equipment
     Division**, you're asked **which org you're working for** (your own org is
     picked for you). Your pre-trip goes to that org's supervisors.
   - If the number **isn't in the equipment inventory yet** (brand-new
     equipment), you can still file it — pick your org and type what the
     equipment is.
3. **Date** — today by default. You can file for any day in the **last
   7 days** (to catch up on one you missed), never a future day.
4. **Hours / Miles** — type the current reading, hour meter or odometer,
   whichever the equipment has. It's never filled in for you; the last pre-trip
   reading for that truck shows underneath as a reminder, and you get a
   heads-up if your number is lower than it.
5. **Checklist** — tap each item you checked (the whole row is the button).
   The **Check all** box at the top ticks all 21 at once; tap it again to
   untick them all (it shows a dash when only some are ticked). Nothing is
   required — leave off anything that doesn't apply (e.g. *Air Pressure* on a
   truck without air brakes).
6. **Repair request submitted** — tick it if you turned in a repair request
   for the truck today. Your supervisors get a **bell notification** (never an
   email). Use **Remarks** to say what's wrong.
7. **Sign & submit** — confirm the certification ("I hereby certify the
   appropriate checks were performed…") in the signature dialog, exactly like
   signing a DOT-12.

**No signal? Nothing is lost.** Everything you enter is kept on your phone as
you go. If sending fails (no connection, or your sign-in expired), the form
says so and keeps your entries — try **Sign & submit** again when you have
signal. Tapping it twice, or retrying after a timeout, never files two copies.
If you close the page, the next **New pre-trip** offers to **restore** it.

**Fixing a mistake** — open your pre-trip and tap **Edit** (you sign again
when you save), or **Delete** it. Both are possible **until a supervisor signs
it**; after that it's locked. The ED number can't be changed — delete and
file a new one.

### The weekly sheet and PDF

Each truck's week (**Sunday–Saturday**) is shown as the paper form:

- the **OPERATOR** row carries each day's initials (two operators on one day
  show as `SE/RS`), and **REPAIR REQUEST SUBMITTED** is ticked on repair days;
- each checklist item is **✓** if it was checked that week. Nothing on the
  checklist is required, so an item nobody checked (e.g. *Air Pressure* on a
  truck without air brakes) is simply left **blank** — never marked as missed.
  When an item was checked on only some of the days inspected, a small grey
  note names them — e.g. `checked MO, WE`;
- **HOURS** shows the week's first → last reading;
- **REMARKS** lists each day's remarks, stamped with day, date and initials;
- the **Supervisor's Signature** line shows `/s/ Name` and the date once every
  inspection that week is signed, otherwise *Pending — 3 of 5 signed*.

Open it from any pre-trip (**Week sheet**) or a truck card; step between weeks
with **‹ ›**. **Download PDF** produces the same sheet as a one-page PDF
(Letter), opening in a new tab. An operator only sees their **own** days on
the sheet; if other operators also drove that truck, the sheet and PDF are
marked **Partial**.

### Signing off (supervisors)

If you're an **approver with write access** to the pre-trip's org (the same
rule as approving a DOT-12), you can sign:

- **One pre-trip** — open it and tap **Sign off**.
- **A whole week** — open the week sheet and tap **Sign week (n)**. It signs
  every inspection on the page you're looking at, and skips (and tells you
  about) any the operator changed after you opened the page, and your own —
  you can't sign your own pre-trip (admins excepted, as on a DOT-12). A
  pre-trip filed after you signed the week shows the week as *Pending* again.

Signing locks the pre-trip. The **To sign** view on the Pre-Trip page lists
every truck-week with unsigned inspections you can sign, with a count on the
tab.

### The Pre-Trip page: one card per truck, per week

Every view shows **one card for each truck's week** rather than a card for
each inspection. A card reads like the paper sheet's bottom row:

- **Top line** — the ED number, the equipment type and its org, and the
  week's status pill (*Signed*, *n awaiting sign-off*).
- **Day strip** — seven cells, Sunday to Saturday, each with the date and the
  operator's initials. A **green check** is an inspected day (the check fills
  solid once the supervisor has signed it); **red with a wrench** means a
  repair request was reported that day; **today with nothing filed** is an
  indigo dashed **+** — tap it to file this truck's pre-trip; days with no
  inspection are just blank (a truck that wasn't driven has nothing to file —
  nothing is ever marked as missed) and future days are dimmed.
- **Bottom line** — how many days were inspected, the first → last hours /
  miles reading (a small ↓ if a reading went backwards), who signed the week,
  and a *Repair request* tag when one was filed.

**Tapping**: the card opens the **week sheet**; an inspected day opens **that
day's pre-trip** (or the week sheet when several were filed that day). The
**⋯ button** in the card's top-right corner offers **New pre-trip for
<ED#>** — the form opens with that truck already filled in — and **Open
week sheet**. In **To sign**, where cards can come from different weeks, each
card also says which week it is.

### Who sees what

| View | Shows |
|---|---|
| **Mine** | Your trucks for the selected week (default) — one card per truck. |
| **To sign** | Unsigned pre-trips you're allowed to sign, any week, by truck. *(Approvers)* |
| **Org** | All pre-trips filed under your orgs for the week, by truck. *(Users with orgs)* |
| **All** | Every org. *(Admins)* |

A pre-trip belongs to the **org of the equipment** (from the equipment
inventory) — or, for shop-owned or not-yet-inventoried equipment, the org the
operator picked. Anyone signed in can file one; new sign-ins don't need an org
assigned first.

## Auto-pinned material (1:1 activities)

Some activities are measured the **same way the material is bought** —
e.g. **Paving** is accomplished in **tons**, and you charge **tons** of
asphalt; the two numbers should match. These are flagged as **one-to-one**
activities.

When you pick a task or activity that is one-to-one, the form **adds the
expected material for you and pins its quantity to the column's
Accomplishment**:

- A toast notification tells you which material was attached.
- If a material that fits is **already on the form**, that one is reused
  (pinned) instead of adding a duplicate — otherwise a **DIRECT BILL**
  material with the expected description is added.
- The pinned material's quantity cell is **read-only** (amber tint).
  Clicking it explains the pin. To change the quantity, change the
  **Accomplishment** (row 12) — the material follows automatically. To
  remove the pin, change the activity (or clear the task); the pinned
  material is dropped, and an auto-added DIRECT BILL material is removed
  if no other column is using it.

This keeps the material side of a 1:1 activity from being forgotten or
drifting out of step with the work accomplished.

## Milepoint & Accomplishment entry — live range check

When you edit a **BMP / EMP milepoint** or the **Accomplishment** cell, the
cell expands to double height and shows a small **valid range** in the top
right, validating as you type:

- **BMP / EMP** show the selected route's milepoint range (e.g. `4.36 – 7.68`);
  a value outside the route range turns **red**.
- **Accomplishment** shows the activity's expected **daily-production** range
  (top right) and the **unit of measure** (bottom right). It turns **amber**
  when the entry is **≥ 4×** the average expected production and **red** at
  **≥ 10×** — advisory flags for an unusually high day, not a hard block.
- **Tab** in BMP jumps to EMP (then to Accomplishment), so you can enter the
  pair without reaching for the mouse.

(Accomplishment cells whose unit is `EH` stay auto-calculated from employee
hours and don't show a range.)

## Back-page "Task or Work Order / Activity / Sub-Activity"

On the back page, the cell that identifies each column is now
**computed automatically and locked** (it used to be a free-typed copy
of the task order). It reads, by column type (each part on its own line):

- **MMS** → the task order, the activity, and the asset reference (route +
  milepoint range, or the BARS number for a bridge) when one is attached.
- **HUB** → the program, the activity, and (if an asset is attached) the
  asset reference.
- **BS95** → `program - activity`.
- **EQP** → the task order, the activity, and the sub-activity.
- **Leave** → the leave LDPR code.

The **activity** shows as the same colorful activity chip used elsewhere
in the form (it prints as the plain activity code on the PDF). To change
what shows here, edit the column's task/work order, program or activity
on the front page — the back-page cell follows automatically.

The back-page **Weather** cell is now a **dropdown** with the same
choices the wizard's Workday Issues step offers (Sunny, Cloudy,
Overcast, Rain, Snow, Fog, Windy, Hot, Cold) plus a "(none)" option to
clear it — no more free-typed weather spellings.

### Editing the long-form Description (hands-off)

The large back-page **Description** narrative is deliberately
**hands-off** so a long write-up never fights you:

- **A plain click-away doesn't close it.** If focus leaves because you
  clicked a button, the chat, or another app, the field **saves what
  you've typed** but stays open for editing — your work isn't interrupted.
- **Three things exit the field:** **Tab** (saves and moves to the next
  cell), **Esc** (reverts any unsaved change and closes), and **clicking
  a different cell** (saves and closes).
- **Your cursor is remembered.** When focus comes back to the field, the
  caret returns to **exactly where you left it** — no select-all, no jump
  to the end.

## Picking an account code (Program)

Typing in the **Program** cell searches OASIS account codes. The
dropdown only shows **valid** codes — retired or superseded codes
(which OASIS marks "INVALID") are filtered out so you can't accidentally
charge to one. If you're looking for a code you've used before and it's
not appearing, it has most likely been invalidated upstream in OASIS.

Once you pick an account code, the **Phase** is filled in from the code
(its Dimension-3 phase) and the **Phase cell is locked and grayed out** —
phase is set by the account code. Clicking it explains why; clear or
change the Program / account code to unlock it. The Task Order cell stays
editable. To keep you moving, the cursor jumps to the **Activity** cell
right after the pick **if Activity isn't filled in yet** — if you've
already set Activity, focus stays where it is. The same phase lock
applies in the Accomplishment View modal.

**Removing the account code** (clearing the Program cell) unlocks the
Phase cell again and also clears the **route, BMP and EMP** for that
column — the route was tied to the account-code accounting, so it's
wiped rather than left pointing at a code that's no longer there.

### Overhead programs (BS95 columns)

Some programs aren't projects at all — they're **overhead buckets** for
your unit (maintenance, equipment, admin, training, rest areas, etc.),
with text codes like **MEXPR**, **EQPWO** or **AEXOH**. When you start
typing one of these families in the Program cell (e.g. `me` for the
`MEX…` programs, `eq` for `EQP…`), the dropdown shows an **"Overhead
programs" section on top**, highlighted in amber. Your form's home
unit's own overhead codes are found first, but overhead programs that
belong to **another unit** are recognized too — e.g. typing `ppstan`
from a district org still finds `PPSTAN` (Right-of-Way, 0062) and
treats it as overhead.

Pick one and the column becomes a **BS95 column** (amber **BS95** chip
in the column header) — no matter which unit the program belongs to. It
automatically:

- fills in the **LDPR profile** (the funding profile for that overhead
  program, e.g. `17276` for equipment, `17237` for maintenance),
- sets the **receiving unit** to the **program's own unit** (your home
  unit for your own overhead codes; the owning unit — like `0062` for
  `PPSTAN` — for another unit's program),
- sets **N/P to Non-participating** (overhead is state-funded, not federal), and
- pins the **phase** (overhead programs usually have none).

All four of those cells lock to keep the overhead setup consistent. Hover
the BS95 chip to see "this column's program is associated with an overhead
program," and clear the Program cell to remove the BS95 state and unlock
everything. Overhead codes are **fiscal-year stamped**; the picker only
offers the fiscal year that matches the form's date.

## Equipment (EQP) columns

Equipment Division work — the **500-series activities** — is charged
against an **AssetWorks work order**, not a task order. You enter it right
from the **Task Order** cell: start typing the **task order ID** of the
work order (e.g. `012301260074`) and the dropdown shows matching
**AssetWorks work orders**, each with its equipment and activity. The
distinction is the leading digits: a task order ID that begins with a
**fiscal year** (e.g. `26…`) is a normal MMS/DTIMS search, while one that
begins with the **equipment's org-unit** (e.g. `0…`) is a work-order
search — so the two never collide. Hovering the **EQP** chip outlines the
task-order cell in green, the same way the other column types mark their
controlling cell.

Pick one and the column becomes an **EQP column** (a green **EQP**
chip in the header). It automatically:

- fills in and locks the **activity** (taken from the work order — e.g. a
  510 work order becomes activity `510`),
- sets the **receiving unit** to the equipment's **org unit** (looked up by the
  work order's ED number in the DTIMS equipment inventory),
- sets the **program** to **EQPWO** and the **account** to the equipment
  operating-expense account (appropriation **27600**),
- leaves the **phase blank and disabled** (equipment work orders have no
  phase), and there's **no route / milepoints**, and
- drops you on the **Sub-Activity** cell, where you pick from the
  sub-activities for that activity (grouped by their group headings).

The sub-activity is the only field you fill on an EQP column —
everything else comes from the work order and is locked (hover a locked
cell for the "Locked by AssetWorks work order" note). Clearing the work
order in the Task Order cell removes the EQP state and unlocks the column.
This all works the same way in the **Accomplishment View** modal.

### Refreshing the work-order list (admins)

The work-order list the dropdown searches is a snapshot, not a live
AssetWorks connection. **Admins** can refresh it from their **profile
page** (avatar menu → Profile): the **AssetWorks Work Orders** card has
an **Upload Work Order CSV** button that accepts the AssetWorks
*Work Order List* CSV export and **replaces the entire list** with the
file's contents. The upload is checked before anything is replaced — a
file with the wrong columns or one that looks truncated is rejected and
the existing list is left untouched. Work orders already picked on a
form keep working even if they've dropped off the newer export.

The card also shows **who last uploaded** the work-order list, when, and
how many work orders it loaded — so admins can tell at a glance whether
the snapshot is current and who refreshed it.

## Hub-project columns

When you pick an account code in the **Program** cell whose program is
a **TheHub project number** (e.g. `2021000890`), DOT-12 automatically
looks the project up in TheHub and fills in what the project already
knows for that phase:

- **LDPR profile** — derived from the phase's state fund +
  appropriation (e.g. fund `9017` + appropriation `27900` → `17279`).
- **Receiving unit** — the phase's responsible org unit.
- **N/P** — participating when the phase carries federal participation.
- **Routes** — the project's route segments (and bridges) become the
  options in the Route cell. If the project has exactly one route it is
  picked for you. Bridge assets are labeled with the bridge's **BARS
  number** (last 6 of the NBI structure number), which lands in the
  Route cell, and they auto-fill BMP/EMP to the bridge's single
  milepoint and lock them — just like bridge assets on task orders.

The column is marked with a bright fuchsia **HUB** chip in the column
number strip (hover it to see the project number) — distinct from the
indigo MMS chip. While the column is hub-linked, the **LDPR, receiving
unit, N/P and phase cells are locked** to the project's values; the
Program cell stays editable. Clearing or changing the program removes
the hub link, unlocks the cells and clears what it filled in.

The phase comes from the account code itself (the same Dimension-3
phase you picked), and the **activity is never auto-filled** — pick it
as usual.

If TheHub is unreachable (or the program isn't a hub project), nothing
changes: the Program cell behaves exactly as it always has, with no
errors. Columns that were hub-linked earlier keep their values, locks
and chip even while TheHub is down — only the route options list is
unavailable until it's back. Everything above applies identically in
the Accomplishment View modal.

## Other locks (not from MMS)

Three more locks apply on the same five-field row family, regardless
of whether the column is MMS-linked:

- **Accomplishment is locked when UOM = `EH`.** The cell auto-computes
  as the sum of employee hours entered inside that task-asset column,
  so the value tracks the timesheet automatically — you don't (and
  shouldn't) type it. Clicking the locked cell surfaces a toast:
  *"Accomplishment calculated from employee hours within this
  task-asset (column)."*
- **Receiving unit is locked when LDPR is a leave-event code.** Picking
  any non-numeric LDPR (`ANNLV`, `SCKLV`, `FMSUS`, `HOLLD`, `BRVUS`,
  `JURYL`, `MLVPA`, `MLVPB`) automatically sets the column's receiving
  unit to your form's home unit and locks the cell. Clicking the
  locked cell surfaces: *"Leave codes force the receiving unit to your
  home unit."* The same cascade still sets activity = `003`, UOM = `EH`,
  and clears program/phase/task/route/measures/accomplishment.
- **UOM is locked when activity or task order is set.** UOM is derived
  from the activity code (during the activity-code pick) and from the
  MMS task's `AccomplishmentUnit.Abbreviation` (during the task pick),
  so once either of those is filled in, UOM is no longer user-editable
  on that column. Clear the activity or the task order to re-edit UOM
  by hand. Clicking the locked cell surfaces: *"UOM auto-derived —
  Change the activity or task order to change UOM."*

All three locks apply identically in the form spreadsheet and in the
Accomplishment View modal.

## Accomplishment View

The **Accomplishment View** action (in the form's Actions menu, or
`Ctrl/Cmd + E`) opens a large grid where each row is one task asset
column from your form. It's the easiest way to bang through several
task assets quickly without bouncing between cells in the spreadsheet.

**It opens in every form state.** On a locked form (approved or past its
pay-period edit window) the grid opens **view-only**: a "View only" chip
shows in the title bar, and every cell, checkbox, Create Row and
copy/delete control is gone or inert — you can still read, compare
against the core plan, and reference the rows for DTIMS-side data entry,
but nothing can be changed.

Columns: Task Order, Org, Activity, Sub-Activity, Program, Phase, Route,
BMP, EMP, Accomplishment, UOM. The Task Order column stays pinned on
the left when you scroll horizontally.

### Creating rows

The **Create Row** button at the top of the modal opens a dialog with
three options:

- **Create New Row** — adds a blank task asset and focuses the Org cell.
  Pick everything manually using the same autocompletes the spreadsheet
  uses.
- **Create New MMS Row** — adds a task asset and focuses the Task Order
  cell. The search box is seeded with the current fiscal-year prefix
  plus your home unit (e.g. on 2026-05-16 with home unit `0260` the box
  opens to `260260`) with the caret placed at the end — the prefix is
  not highlighted, so typing appends to it instead of replacing it.
  Picking a task will auto-fill org, activity, program, phase, and UOM
  (same selectTask flow the spreadsheet uses), then focus jumps to
  Route. Picking a route advances focus to BMP.
- **Create New MMS Row (with task finder)** — coming in a later
  iteration; the button is visible but currently a no-op.

### Reading the cells

- **BMP / EMP** show a small caption above the value with the asset's
  allowed range, e.g. `0.00 - 4.32`. If you type a value outside the
  range, the caption and value turn red.
- **Accomplishment** shows daily-production helper text below the value.
  Gray when the value is within 2× of the activity's average daily
  production, yellow when 2–4×, and red at 4× or more. The cell
  background tints to match.

### MMS-locked rows

Rows tied to a task order (the "MMS" pill appears next to the task
order id and the row gets a faint indigo tint) lock the same five
fields the spreadsheet locks: org, activity, program, phase, and
UOM. Clicking a locked cell shows the same warning toast as the form.
To unlock, change or remove the task id either from this modal or from
the spreadsheet view.

### EH, leave-code, and UOM-derived locks

In addition to the MMS lock above, three more locks apply per row:

- **Accomp** is locked whenever **UOM = `EH`** — the value is computed
  as the sum of that task-asset's employee hours, so the field is
  read-only. Click for: *"Accomplishment calculated from employee
  hours within this task-asset (column)."*
- **Org (receiving unit)** is locked whenever LDPR is a leave-event
  code (`ANNLV` / `SCKLV` / `FMSUS` / `HOLLD` / `BRVUS` / `JURYL` /
  `MLVPA` / `MLVPB`). Picking a leave code in this modal sets Org to
  your form's home unit and locks it. Click for: *"Leave codes force
  the receiving unit to your home unit."*
- **UOM** is locked whenever **Activity** or **Task Order** is set on
  the row. UOM is derived from those — clear them to edit UOM
  directly. Click for: *"UOM auto-derived — Change the activity or
  task order to change UOM."*

### Closing

ESC or the × in the top right closes the modal. Pressing `Ctrl/Cmd + E`
again toggles it.

## Managing the roster

The **Manage Rosters** action (in the form's Actions menu, or `Ctrl/Cmd + M`)
opens a single tabbed surface for setting up the day's roster of
**employees**, **equipment**, and **materials** — handy when you'd
otherwise be hopping between many cells on the form.

Each tab has the same shape:

1. A picker on top — the same filtering rules as the corresponding
   in-cell autocomplete on the form.
2. An **Add Row** button next to the picker that's disabled until the
   picker has a complete selection. Clicking it adds the row to the form
   and clears the picker so you can add the next one without leaving
   the modal.
3. An inline-editable table below listing every existing row, with a
   delete button at the end of each row. Deletion asks for confirmation
   and warns that any charges attached to that row will also be removed.

**Employee tab.** Search the home unit's labor inventory by name or
OASIS ID. Once added, each row exposes a **Temp Upgrade** dropdown
filtered by the employee's HR title (same logic as the EMP3 cell on the
form).

**Equipment tab.** Type any 2+ characters of an ED number; the modal
runs the same two-pass startswith→contains Deighton search the form
uses (so "201" surfaces real ED# 201xxxx items first, with substring
matches like 1370201 listed after). A newly added row starts with an
empty **Ending Meter** — type the shift's reading; nothing carries over
from an earlier DOT-12. A reading lower than the ED#'s last recorded one
(on an earlier-dated DOT-12) is outlined red with that reading shown
under the field — the same check as the form's Checks tab, also in the
wizard's Equipment step. Rows expose **Initials** (3-char
text — typed input, force-uppercased as you type), **Ending Meter**
(numeric), and an **Operational** toggle.

**Material tab.** A cascading picker:

- **Org Whse** comes first. Picking a non–DIRECT BILL warehouse
  auto-focuses the Description field. The list is the same one the
  form's INV2 cell uses, including the DIRECT BILL sentinel pinned at
  the top.
- **Description** is server-searched scoped to the warehouse (or
  globally if none is set, or free-text in DIRECT BILL mode). Picking a
  description (when warehouse is set) auto-focuses Stock Item Suffix.
- **Stock Item Suffix** is disabled until both warehouse and description
  are set, then offers the deduped (stock #, suffix) pairs available at
  that warehouse.
- If you start with the description (no warehouse yet), the warehouse
  list is filtered down to warehouses that stock that description.
- After **Add Material Row**, the description and stock fields clear but
  the warehouse stays — so you can rip through several materials from
  the same warehouse in a row.

The **Document #** column on the material table is editable inline
(commits on blur or Enter), so you can paste in OC document numbers
without bouncing back to the form.

The action is hidden when the form is locked (approved or beyond),
matching how the form-cell add buttons behave.

### Blank rows are swept up on a manual save

When you press **Save** (the toolbar button or `Ctrl/Cmd + S`), any
employee, equipment, or material row you added but left **completely
empty** is dropped before the form is sent — so a row you clicked "add"
on and never used doesn't linger. A row only counts as empty when **all
of its own fields are blank _and_ nothing is charged to it** on any
column; a half-finished row (say, hours typed but the name not yet
picked) is kept, so saving never throws away data. At least one employee
row is always preserved.

**Autosave does not do this.** The 10-second autosave leaves your blank
rows alone, so a row you just added stays put while you're still filling
it in — only an explicit Save sweeps them.

### Your last edit is never lost on submit or when leaving

Cell edits are committed when you move off the cell, and the form
autosaves on a short delay — so the very last thing you type (for example
the **additional details** box at the bottom of the form) might not have
reached the server yet at the instant you act on the form. Two safety
nets cover that:

- **Pressing a workflow button saves first.** When you **Submit**,
  **Approve**, **Enter in HRM/FIN**, or **Reject**, the form first
  commits whatever you were typing and saves it, then performs the
  action — so the signed/submitted form always includes your latest
  changes. You don't have to click "off" the field or press Save
  beforehand.
- **Leaving with unsaved changes warns you.** If you try to close the
  tab, reload, hit **Back**, or jump to another form while you have
  changes that haven't been saved, DOT-12 stops and asks. For in-app
  navigation you get **Save & leave** (saves, then goes), **Leave
  without saving**, or **Stay on page**; closing or reloading the tab
  shows the browser's own "leave site?" prompt.

## Compact Views — Sticky Per-Column Header

In both the **Compact View** (`Ctrl/Cmd + 2`) and the **Compact-Task View**
(`Ctrl/Cmd + 3`), the per-column accounting metadata is shown **once** in
a sticky bar at the top of the page rather than being repeated above each
of the Employee, Equipment, and Material tables:

- **Compact View** (per task asset / column): the sticky bar shows the
  full accounting row for each column in the same order as the paper
  DOT-12 / main form — **LDPR Profile**, **Org**, **Activity** (with
  sub-activity), **E Program**, **Phase**, **Task Order #**, and
  **Route / MP**. The Employee, Equipment, and Material sections each
  show only their section name and numeric column labels (1, 2, 3, …) —
  they no longer repeat any accounting metadata.
- **Compact-Task View** (per task order): the sticky bar shows the same
  fields in the same order, minus Route (since each group can span task
  assets on different routes) — LDPR Profile, Org, Activity, E Program,
  Phase, Task Order. The Activity row carries the `(N)` badge when
  several task assets share the order. Equipment and Material follow
  the simplified column-number layout used by Employee.

Org falls back to the form's `home_unit` when a task asset's
`receiving_unit` is blank. Blank fields render as `—` so missing data is
visually obvious.

**Route / MP label.** The asset reference is shown on one line: a
**bridge** shows just its BARS number (e.g. `30A249`); a **road point**
shows `route @ milepost` (e.g. `CR68 @ 1.11`); a **road segment** shows
`route begin-end` (e.g. `CR68 0.00-1.49`). In Compact view the road
route's internal space is dropped (`CR 68` → `CR68`) so it fits the cell.

**Arrow keys stay in bounds.** Moving left/right with the arrow keys keeps
you in the **same row** — at the first or last column the selection stays
put and a toast tells you there's nothing further that way (it no longer
jumps to the start of the next/previous row). Use **Tab** if you want to
walk through every cell wrapping onto the next row.

The same sticky bar also shows a **selected-row chip** on the right for
the row you're editing — e.g. for a material it reads the description,
warehouse, stock item number, and commodity suffix. When a material's
stockpile combo has been selected, its **unit of measure** (TON, FT, EA,
…) appears as a small badge at the end of that chip, so you can see the
unit you're entering quantities in without leaving Compact view. (The
unit comes from the inventory and fills in once a stock item is picked.)

The sticky bar stays visible while you scroll between sections, so the
column you're typing into is always identified at a glance.

A purple summary bar sits **above** the accounting bar in the sticky
stack and is always visible. It shows the currently-selected column /
group's full summary when a cell is focused, or a "click any cell"
hint otherwise. The **info icon (ℹ︎) on its right edge** opens a popover
explaining what each compact view does and the keyboard shortcuts for
switching between views.

When the form is **locked** (approved or beyond, or past the pay-period
edit window — see *Form lifecycle & sign-off*), both compact views are
**read-only**: every charge cell is disabled and a **🔒 Read-only** badge
appears in the purple summary bar. This matches the main form editor —
you can still open the compact views to read a locked form, but you can't
change any hours or quantities. (The server enforces the same lock on
save, so a locked form can't be edited regardless of which view you use.)

### Horizontal scrolling — pinned edges

Each data cell renders at a fixed width (~110px) so values like task
order numbers and activity codes fit without being squeezed by the
number of columns. When you have more columns than fit on screen, the
section scrolls horizontally — and the **leftmost label column** (the
row of employee / equipment / material names) and the **rightmost total
column** (Total EMP / EQP / MAT plus the per-row totals) stay pinned to
the edges so you always see what row a cell belongs to and where its
total ends up.

All four blocks (the accounting bar at the top plus the three section
tables) scroll in lockstep, so the column under any cell lines up
across every section. Only the **accounting bar at the top** shows a
scrollbar — drag it to scroll all four blocks together. Arrow-key /
Tab navigation past the rightmost or leftmost visible column also
auto-scrolls everything to keep the focused cell out from under the
pinned label and total columns.

Each charge type uses a distinct accent color so Employee / Equipment /
Material rows are instantly distinguishable: **Employee** = amber,
**Equipment** = amber, **Material** = violet. The accent shows up on
the section header cell, the table border, and the total / grand-total
row.

## Keyboard Shortcuts — Users Table

| Shortcut | Description |
|---|---|
| `Ctrl/Cmd + ←` | Previous page |
| `Ctrl/Cmd + →` | Next page |

## Search & Filtering

- Click the search bar (or press `` ` ``) to see what you can search for —
  the focus-empty state shows the categories (Tags, Activity codes,
  Organizations, Created by, Programs, Task orders, Routes, People,
  Equipment, Materials, Form details) and one-click status chips
  (Draft / Submitted / Approved / HRM / FIN / Final / Rejected).
- Type in the search bar to filter by form details, summary, or org code.
- **Type a numeric form ID** (e.g. `1234`) and the table jumps straight to
  that form — no need to pick anything from the dropdown. The query still
  also matches form_details containing those digits, so if a form's details
  happen to mention "261" you'll see both that form and form #261.
- **Type a district** — `D7` (or `d7`, `D10`, …) as its own word filters to
  that district's timesheets (home units starting `07`, `10`, …). It
  combines with the rest of your search: `D7 patching` shows District 7
  forms whose details mention "patching", and `D7 D2` shows both districts.
- Autocomplete suggests Tags, Activity Codes, Organizations, Creators, and
  Statuses — plus six categories matched against **what's actually on the
  forms** (each pick becomes a chip that narrows the table):
  - **Programs** — OASIS program codes, matched by code or name
    (e.g. `D04AP` or "annual plan").
  - **Task orders** — the task order numbers keyed on form columns.
  - **Routes** — understands real route phrasing: `CR 21`,
    `county route 21`, `US 60`, `I-77`, a county name (all forms with work
    in that county), or a bridge number like `43A115`. `US 60 EB` narrows
    to the eastbound direction. A plain route chip like `CR 9` matches CR 9
    and its directional labels but NOT `CR 90` or the `CR 9/2` sub-route —
    pick the sub-route suggestion for that.
  - **People** — by name or OASIS payroll ID. A person only matches forms
    where they **charged more than zero hours** — being listed on the
    roster with no hours doesn't count.
  - **Equipment** — by ED number or description, again only where the
    machine has hours charged.
  - **Materials** — by the commodity/stock code + suffix pair
    (e.g. `402001 - A`) or the material description; only forms where a
    quantity was actually charged.
  Suggestions are ranked by how many forms carry the value, and only ever
  offer values from forms you can see.
- **Created By has its own dropdown** next to the search bar: click
  **Created By** and type a creator's **name or E-number** — the
  autocomplete lists every user who has created at least one DOT-12.
  Picking one adds the same green creator chip the omni-search produces
  (multiple creators OR together); selected creators are pinned at the
  top of the dropdown and click to remove.
- **See who's in a form right now.** A row glows with a soft green
  sheen when someone currently has that DOT-12 open, and small colored
  avatars appear at the right of its description showing exactly who
  (hover for names). It updates every few seconds — handy for avoiding
  two people editing the same form at once.
- **The table isn't blown away while you type.** If a mid-typing query matches
  no forms (e.g. a transient `0` on the way to picking an org or activity from
  the dropdown), the last non-empty results stay on screen instead of flashing
  an empty table. Once you select a suggestion, clear the box, or the query
  matches again, the table updates normally.
- Select a suggestion to add it as a chip filter.
- Multiple chip filters combine: **AND** for tags, **OR** for others.
  Different categories always AND together (a Program chip + a Person chip
  = forms with that program AND that person).
- **Smart Search** — the sliders button next to the search bar (or
  **`Ctrl/Cmd + Shift + F`**, or the "Advanced search…" row in the
  search-bar tips panel) opens a filter builder with one labeled field per
  category: Program, Task order, Route, Person, Equipment, Material, Org,
  Activity, Tag, Status, and a DOT-12 **date range** (a from/to pair — the
  only place a date *range* can be set; the `Ctrl/Cmd+D` popover stays
  single-day). Each field is its own autocomplete; picked values sit in the
  field as small chips. The footer shows a live **"N forms match"** count
  as you build — nothing changes on the page until you hit **Apply**
  (`Ctrl/Cmd + Enter`), which drops all the chips into the toolbar and
  filters the table. Cancel (or Esc) discards the draft.
- Status filters: Draft, Submitted, Approved, Rejected.
- **Pay Period** dropdown — pick a specific bi-weekly window.
- **DOT-12 Date** popover — pick a specific calendar date. Accepts free-form
  typing: `M/D` (e.g. `5/19`) or zero-padded `MMDD` (e.g. `0506`) defaults to
  the current year; `M/D/YY`, `M/D/YYYY`, `MMDDYY`, `MMDDYYYY`, and
  `YYYY-MM-DD` also work. Tab, Enter, or click outside to commit; Escape to
  cancel. **`Ctrl/Cmd + D`** opens and focuses this filter from anywhere on
  the page. Selected date appears as a chip.
- **By Me** toggle — show only forms whose creator is you.
- **Hide Final** toggle (next to By Me) — tucks away forms that are
  already fully entered (Approved + HRM + FIN). It combines with your
  other filters, applies to select-all and to the ◀ / ▶ prev/next
  arrows inside the form editor, shows as a removable chip while on,
  and is remembered across visits. Off by default.
- Click a sortable column header (Created, Form Date, Home Org, Form Details)
  to sort. Sorting is applied across the **whole** filtered result set, not
  just the current page, so paging through stays in order. A third click on
  the same column clears the sort back to newest-first.
- Filters persist in URL params (shareable links) and localStorage (across
  sessions).
- **Paging advances by the rows you actually saw.** The table fits as many
  rows as your window allows; **Next** (or `Ctrl/Cmd + →`) jumps to the first
  row *past the last one that rendered fully*, so a row clipped at the bottom
  edge isn't skipped — it leads the next page. **Previous** / **First** /
  **Last** work the same way. The footer shows the exact `Showing X–Y of N`
  range you're looking at.
- **Prev/next inside the form editor follows the table.** The ◀ / ▶ arrows in
  the open form step through the *same filtered + sorted set* you were viewing
  on the list — e.g. with the table filtered to **Approved** and sorted by
  Form Date, the next arrow goes to the next Approved form in that order, not
  the next form overall. If the form you're on isn't part of the active filter
  (you opened it directly), the arrows are disabled. Clearing the table's
  filters restores plain newest-first navigation. Opening a form **from the
  list** always uses the list's filter/sort for prev/next — even when that form
  also happens to be awaiting your approval. The approvals **review queue**
  (prev/next through the forms waiting on you) applies only when you open a
  form **from the Approvals page**.

## Permissions Model

- **Roles:** Viewer (read-only), Creator (create/edit/submit forms + tags),
  Approver (the **full pipeline** — Creator + approve/reject **and** HRM/FIN
  entry), Time-entry approval (**entry-only** — HRM/FIN entry and
  recalling approved forms back to draft, but cannot approve/reject and
  cannot author forms), Admin (everything, all orgs, including HRM/FIN
  entry), and **Employee** — the role PIN sign-in creates for crew members
  with no state account: signed in, can file a pre-trip, sees **no**
  DOT-12s (the forms list, Reports and Templates are hidden). An admin can
  promote an Employee to any other role later.
- **Org assignments:** each user gets specific orgs with **Read** or
  **Read + Write** access.
- Users only see forms for their assigned organizations (admin sees all).
- Write access is required to create/edit/submit forms for an org.
- Approving or rejecting a form requires **write access to that form's
  organization**, and you **can't approve/reject a form you submitted
  yourself**. (Admins can approve anything.)
- Maximum 2 districts per user for org assignments.
- **Pre-Trip** *(when switched on)*: **anyone signed in** can file a pre-trip
  (no role or org needed); you see your own plus every pre-trip under your
  orgs; signing one off takes the DOT-12 approval rule (approver role + write
  access to its org, not your own). See
  [Pre-Trip inspections](#pre-trip-inspections-config-pre-trip).
- **Home Org:** each user can have one of their assigned orgs marked as
  their home org (shown in the Users table). New DOT-12s the user
  creates start with the Home Unit pre-filled to this org (when it's one
  of their Read + Write orgs); without one, the form starts blank and
  the home unit is entered on the sheet.

### Creating / editing users (Config → Users)

The Create/Edit User dialog shows everything on one screen — identity on
the left, access on the right. To **pre-provision someone before their
first sign-in**, fill the fields tagged `PRE-PROVISION`:

- **E-Number or Email** (either is enough — first sign-in matches on
  e-number or email and links to this account),
- **Role**, and
- **Org Access** (Read / Write per org, max 2 districts).

Accounts created by **PIN sign-in** look different: no e-number, no email,
a **labor code**, a Home Org and **no** org access rows (that is what keeps
them from seeing DOT-12s). You can still edit them — set a supervisor so
their PIN resets route to the right person — without granting an org. If
such a person later gets a state account, their first SSO sign-in **adopts**
the PIN account (same name, labor code kept) rather than creating a second
one; the PIN stops working and the role is lifted to Viewer.

Optionally pick a **Home Org** from the assigned orgs. Name fields are
filled in automatically from the state sign-on (SAML) at first login, so
they can be left blank.

### Assigning supervisors (Config → Users → Assign Supervisors)

The **Assign Supervisors** tab builds one organization's reporting chart by
dragging. It is there for anyone who can edit users (administrators today).
Who reports to whom drives leave-request approval, PIN-reset approval and
the "my people" notification settings, so this is the fast way to set it
for a whole crew.

1. **Choose an organization.** Nothing can be assigned until you pick one.
   The list shows every org that has people, with how many of them already
   have a supervisor; search by code or name. **Organizations** in the top
   bar takes you back to the list. The org is part of the page address, so
   a link opens straight on it.
2. **Read the two panes.** On the left, **Not on the chart** holds the
   org's people who have no supervisor and nobody under them. On the right
   is the chart: each supervisor with their team beneath them. The org's
   people are its employees on the labor roster plus any account whose Home
   Org is that org.
3. **Drag a card onto a person.** The person you drop on becomes their
   supervisor. While you drag, the cards that can take the drop are
   outlined, the ones that cannot are dimmed, and the card you are carrying
   says what letting go will do ("Will report to …"). Dropping anywhere in
   a supervisor's team area counts as dropping on that supervisor. The
   change is **saved the moment the card lands** — there is no Save button.

More ways to move people:

- **Several at once.** Click cards to select them (a check replaces the
  initials), then drag any one of them: the whole selection travels
  together. Or use the bar that appears at the bottom — **Choose
  supervisor** lists everyone they may report to, **Remove supervisor**
  clears it. This is also the keyboard and touch-screen path: Tab to a
  card, Enter to select it. **Esc** backs out.
- **Start a chart from the top.** With an empty chart, drag the person who
  leads the org onto **Start the chart**. They sit at the top with no
  supervisor, ready to be dropped on. While you drag, **Top of the chart**
  at the top of the pane does the same for anyone.
- **Remove a supervisor.** Drag the card back to the left pane (a **Drop
  here to remove their supervisor** bar appears while you drag).
- **Someone from another organization.** If people here report to someone
  whose home is another org — a district office, say — use **Supervisor
  from another org**, search for them, and they appear on the chart with a
  dashed outline as someone to drop on. Only people who already have a
  DOT-12 account can be added this way, and they cannot be moved from here:
  change their own supervisor from their own organization.
- **Undo.** Every change shows a confirmation at the bottom right with an
  **Undo** button.

Rules the page enforces (and the server re-checks): nobody is their own
supervisor, and nobody can report to someone **below** them on the chart —
the page refuses the drop and says who is in the way. To swap two levels,
remove the lower person's supervisor first.

**Employees without an account.** Most roster employees have never signed
in, so they have no DOT-12 account (their card's initials have a dashed
ring). A supervisor is stored on the account, so the first time you place
one of them — or drop someone on them — DOT-12 creates the same bare
account PIN sign-in creates: their name, labor code and Home Org, **no
permissions and no org access**. The confirmation tells you when that
happened. Undo removes the supervisor but leaves the account.

Good to know: job titles on the chart drop the leading "Transportation"
to fit (hover for the full title); **Find a person** narrows the left pane
and dims everyone else on the chart; a wide chart scrolls, or drag its
background to pan. The **User Hierarchy** and **Org Chart** tabs show the
result across all organizations.

## Approval Workflow

| Status | Meaning |
|---|---|
| **Draft** | Form is being worked on, not yet submitted. |
| **Submitted** | Creator clicks Submit, setting `prepared_by`. Form is locked for approval. |
| **Approved** | Supervisor approves. Sets `approved_by`. Ready for HRM/FIN entry. |
| **Rejected** | Supervisor rejects with a reason. Form returns to draft state. |
| **Approved + HRM** | Approved form has been entered into the HRM system. |
| **Approved + FIN** | Approved form has been entered into the FIN system. |
| **Final** | Both HRM and FIN entry completed. |

**The Approvals page (Avatar → Approvals).** If your role can approve
**or** do HRM/FIN entry, the avatar dropdown has an **Approvals** item
(with a count badge) that opens a triage page at `/dot12/approvals`. It
shows a count tile for each queue you can act on — **Awaiting Approval**,
**Pending HRM Entry**, **Pending FIN Entry** — and a list of the forms in
each. Approvers and admins get all three tabs; the entry-only timesheet
(time-entry approval) role gets just **HRM** and **FIN** (no Approval
queue). Clicking a form opens it in the **form editor**, with prev/next
paging through the rest of that queue — approve, reject, and HRM/FIN
entry all happen in the editor as usual. The "Awaiting Approval" queue
contains submitted forms from orgs you have **write** access to,
excluding forms you submitted yourself. When **leave requests** are
switched on, a fourth **Leave to approve** tile lists the DOP-L1 requests
waiting on you; those rows open the request page instead of the editor
(see [Requesting leave (DOP-L1)](#requesting-leave-dop-l1)).

The queue tabs share one row with three **filters** on its right:

- **Org dropdown** — narrows the list to one home unit; it offers the
  orgs present across your queues, and the pick carries over as you
  switch tabs.
- **Direct reports only** switch — keeps just the forms **submitted by
  your direct reports** (people whose supervisor is you in the user
  hierarchy — see Avatar → User Management).
- **My people only** switch — keeps just the forms that **list at least
  one of your direct reports as an employee** (people whose supervisor
  is you in the user hierarchy — strictly one level down; people deeper
  in your chain, and you yourself, don't count). This is the filter for
  the proxy-submission pattern: someone else keys the DOT-12, but the
  workers on it are yours. Matching runs on each user's **Labor Code**
  (their OASIS payroll code, set by an admin in User Management); if
  some of your direct reports don't have one yet, the page shows a note
  with the count — their forms can't be matched until the code is
  filled in.

All the filters combine, and **every count follows them live** — the big
count tiles and the tab badges show the filtered count of each queue
while a filter is active (plus a `shown of total` readout), updating as
you change the org, flip the switch, or move between tabs. Opening a
form while filters are active pages prev/next through the **filtered**
list only.

The **avatar count badge** totals the queues your role actually acts on:

| Role | Avatar badge counts |
| --- | --- |
| **Approver** | Everything (Awaiting Approval + HRM + FIN) |
| **Time-entry approval** | HRM + FIN |
| **Admin** | Everything (Awaiting Approval + HRM + FIN) |

The badge keys off the **role** itself, since the approver and time-entry
approval roles act on different queues.

**Your rejections (Avatar → Rejections).** When a DOT-12 **you
submitted** is rejected, a **pulsing red count** appears on the
bottom-left of your avatar, and the avatar dropdown gains a pulsing
**Rejections** item (with the count). It opens a page at
`/dot12/rejections` listing each of your rejected forms — newest
rejection first — with the **reason it was sent back** shown right on
the card. Click a card to open the form in the editor, fix the issue,
and resubmit; once you resubmit, it drops off the list and the badge
count goes down. The badge and menu item only appear while you have at
least one rejected form. (This is scoped to forms **you created**, so it
follows your own work even though a rejection clears the submitter
field.)

**HRM/FIN entry is restricted.** Only the **approver**, **time-entry
approval**, and **admin** roles can mark a form entered in HRM or FIN. And
when a form
with **no materials** is entered into HRM, **FIN is completed
automatically** at the same time (there's nothing for FIN to enter) —
the signing dialog switches to **"Enter in HRM + FIN"** with amber FIN
highlights and a **Sign & Enter Both** button, so you can see one
signature completes both steps. On these forms the Actions menu shows
only **Enter in HRM** (no separate FIN action — it's automatic), and
they never appear in the Pending FIN queue.

**Editing the OC Document ID after approval.** Approving a form normally
locks every cell. The one exception: a **time-entry approval** user (or
an admin) can still edit the **OC Document ID** on material rows after
approval — and *only* that field — so OASIS doc numbers can be filled in
during entry. Everything else stays read-only. This window **closes**
once the form goes **Final** (both HRM and FIN entered) or the pay
period **locks** (~two weeks out); after either, the OC Document ID is
read-only too.

After you sign any step, the page scrolls to the signature section (if
it isn't already on screen) so you can watch your signature write
itself in — and when the **fourth and final** signature lands, the
whole signature section plays a brief violet celebration to mark the
form going **Final**.

**Signatures.** Each workflow box on the form — **Prepared By**,
**Approved By**, **Entered in HRM By**, **Submitted in FIN By** — shows
the signer's name as a signature once that step is done, with the
**date and time** it was applied in small text beneath it (Eastern
Time). The boxes are read-only; the signature and timestamp are stamped
automatically when you Submit / Approve / enter HRM / enter FIN. A long
name shrinks to fit its box rather than being cut off.

### Editing window — forms close after the pay period

You can edit a DOT-12 **through the Friday _after_ its pay period ends**
(the pay period itself ends on a Friday, so that's roughly one extra
week). After that the form is **permanently read-only ("stone")** — an
amber banner at the top says the pay period is closed for editing and
shows the cutoff date. Once closed you can't change cells, add columns,
apply a template, use the wizard, delete it, **or recall it** — it's
locked for good.

**Recall to Edit (only while the period is open).** An *approved* (or
further-along) form is locked by the sign-off workflow, so you can't just
type into it. If you need to fix one **before the window closes**, the
person who **created** it, an admin, **or anyone with an HRM/FIN entry
role** (approvers and timekeepers — the people working the approved
queue) can recall it: use **Recall to Edit** in the form's Actions menu,
or the button in the amber banner.
That pulls the form back to a **draft** and **clears all four sign-offs
(submission, approval, and any HRM/FIN entry), completely restarting the
approval process** — the form has to be re-submitted, re-approved, and
re-entered from the beginning. This only works while the pay period is
still open — once the Friday cutoff passes, even completed forms can no
longer be recalled. Recalls show up on the **History** tab as
*"Recalled to edit."* (This is separate from **Recall to Draft**, below.)

**Recall to Draft (submitted, not yet approved).** A *submitted* form
that hasn't been approved yet can be pulled back to draft with **Recall
to Draft** — by the **submitter** themselves, an admin, **or anyone with
an HRM/FIN entry role** (approvers and timekeepers), with no ownership
check for the entry roles. It clears the submission signature so the form
is editable again and simply drops out of the approvers' pending queue —
it is **not** a rejection (no reason is recorded and the submitter gets
no rejection notice), so use **Reject** instead when the submitter should
be told why it came back. Once the form is **approved**, Recall to Draft
goes away for entry roles and **Recall to Edit** (above) takes over.
History shows these as *"Recalled to draft."*

**Both recalls ask you to confirm first, and both restart the approval
process.** Choosing **Recall to Draft** or **Recall to Edit** (from the
Actions menu or the amber banner) opens a confirmation dialog that spells
out what will happen — the form drops back to a draft and its sign-offs are
cleared, so it must go through approval again. **Recall to Edit** shows an
extra highlighted warning because it discards the most progress (all four
sign-offs). Each has **Cancel** / **Recall** buttons, so nothing is
recalled by an accidental click.

**How a locked form looks.** When a form is locked (approved/further along,
or the pay period has closed), its cells are read-only but still **read like
a filled-in form**: every data-bearing and otherwise-editable cell —
including subtotals and the accounting/road-info block at the top of each
active column (receiving unit through unit of measure) — keeps its normal
white background with the text greyed to show it can't be edited. Only the
genuinely unusable cells (empty unused rows, fields that are disabled even on
an open form, e.g. a route's mile posts before a route is picked) keep the
solid grey fill. MMS/HUB/EQP/BS95-sourced cells keep their usual tinted lock
styling.

## Notifications & Comments

A **bell** in the top bar shows a red count of items that need your attention.
You're notified when:

- a DOT-12 you submitted is **approved** or **rejected** (the rejection reason
  is included),
- a DOT-12 you created is **recalled or reopened** by someone else (a
  timekeeper or admin pulling it back) — the notification tells you it's
  back in draft so you can edit and resubmit it,
- a form is **waiting on your approval** — you're an approver for its unit
  **and** the form is about the people you chose to hear about (by default,
  it lists one of your direct reports — see
  [Email & notifications](#email--notifications)),
- a form is **ready for time entry** — if you do HRM/FIN entry for a unit,
  you're notified when a form is approved (or when HRM entry is done and FIN
  entry still remains), again only for the people you chose to hear about,
- someone **comments** on one of your forms,
- a **leave request (DOP-L1)** needs your **signature** or **approval**, or
  one of yours is **approved**, **disapproved** or **withdrawn**, or
  **DOT-12s were created** from it (see
  [Requesting leave (DOP-L1)](#requesting-leave-dop-l1); only when that
  feature is on), or
- an operator files a **pre-trip with a repair request** for equipment in an
  org you sign off for (filter chip **Pre-Trip**; bell only — these are never
  in the email digest), or
- someone sends you a **message**, **replies** on a support request or message
  you're part of, or your request is **resolved or closed** (see
  [Feedback](#feedback)), or
- you're on the support team and someone files a **new support request**.

**The bell.** Point at (or tap) the bell to see your most recent items, in
two tabs: **Notifications** — things the system is telling you — and
**Messages** — things a person wrote to you. Each tab shows its own unread
count. Clicking an item marks it read and opens it: a notification jumps to
its form or request, a message opens the conversation so you can answer.
**Mark all read** clears the count, and the link at the bottom opens the full
page. Notifications arrive live, without refreshing.

**The Notifications page** (`/dot12/notifications`) has the same two tabs.

*Notifications* is one list grouped by day. **Search** it, or narrow it with
the chips (All, Unread, Approvals, Comments, Rejected, Leave, Pre-Trip — a
chip only appears when it has something in it). Click a row to open it.

- **Mark all read** marks this tab's notifications read.
- **Delete** one notification with the trash can at the end of its row.
- **Delete all** removes every notification on this tab. It asks first —
  *"Delete all 12 notifications? Messages are kept."* — and nothing is
  deleted until you confirm. Deleting only clears your own list: the DOT-12,
  leave request or comment it was about isn't touched, and your messages
  stay.

*Messages* is your conversations, with the list on the left and the open
conversation on the right (on a phone, one at a time with a back arrow).

- A **support request** you sent, with every reply. Type in the box at the
  bottom and press **Send reply** (or **Enter**; **Shift+Enter** starts a new
  line). Your own messages sit on the right; support's are tagged **Support**.
- A **direct message** someone on staff sent you. You can **reply** to it the
  same way, and they're notified.
- An **announcement** sent to everyone. These are read-only, so there's no
  reply box; you can **Delete** one to remove it from your own list.
- **New support request** (top of the page) starts a new one.
- Unread conversations show a count; opening one marks it read. Filter the
  list with All / Unread / Support / Direct / Announcements, or search it.

A notification about a message — in the bell, or in your email digest — opens
that conversation directly.

**Composing (staff).** Use **New message** — from the bell *or* the button on
the Notifications page — to broadcast to everyone or message one person. The
message box supports markdown and has a **Write / Preview** toggle so you can
see exactly how it'll render before sending. A message to **one person**
starts a conversation they can reply to; you're notified when they do, and it
appears under your own Messages.

**Comments.** Every form has a **Comments** tab in the right panel. Leave a note
or ask a question; the form's owner and anyone else who has already commented
are notified. Comments are visible to anyone who can view the form, and they
**appear in real time** — you'll see others' comments without refreshing.

**Who else is viewing.** When you open a DOT-12, the top bar shows a live count
of everyone currently viewing that same form (with their initials, like a shared
spreadsheet), so you can tell when someone else is in it at the same time.

**Messages from admins.** Admins can use **New message** to either
**broadcast to everyone** (useful for downtime notices or reminders) or
message **one person** — switch between *Everyone* and *One person* and search
for the recipient by name or e-number. A broadcast lands in everyone's
Messages as an announcement; a message to one person is a conversation they
can answer.

## Navigation

Navbar order, left to right:

- **DOT-12** — Main forms list with search, filters, and pagination.
  Clicking the **DOT-12** title always returns you to the **first page** of
  the list (it resets pagination even if you were partway through, or already
  on the list) — your search and filters are kept. Ctrl/Cmd-click opens the
  list in a new tab.
- **My DOT-12s** — A card gallery of just the DOT-12s **you** created, newest
  first. Each card shows the form date, status, home (and receiving) unit,
  activity codes, description, and tags at a glance; click a card to open that
  form. A **search box** filters your forms the same way the main list does
  (activity, unit, description, tag). The **All DOT-12s** button (and the
  navbar **Back** arrow) returns you to the default full table; **New DOT-12**
  creates a fresh form. Ctrl/Cmd-click a card to open it in a new tab.
- **Leave requests** — *(only when the leave-request feature is switched
  on)* your DOP-L1 leave requests: file one for yourself or on behalf of
  someone in your org, sign, approve, and turn approved requests into
  DOT-12s. The link carries an **amber count** of requests waiting on you
  (to sign or to approve); the same entry sits in the phone drawer and the
  avatar menu. See [Requesting leave (DOP-L1)](#requesting-leave-dop-l1).
- **Reports → Org View** — Employee and equipment hours matrix by org and
  pay period. The **Resource** toggle switches between Labor and Equipment;
  in Equipment mode an extra **Metric** toggle picks **Hours** (default) or
  **Meter** to show that day's ending-meter reading per ED#.
  It **opens on the current pay period** every time you come to it from the
  menu — it does not go back to the period you were looking at last time.
  Your org and view choices are remembered; the dates are not. A reloaded
  page or a shared link keeps its period. The current period is always in
  the list, even before anyone has entered a DOT-12 for it.
  **Click any cell** to open a sidebar with the day's summary, and — when
  the cell was filed across more than one DOT-12 — a breakdown grid
  pivoting forms (rows) against unique task-assets (columns) with row /
  column / grand totals. Cmd/Ctrl+click the form label to open that DOT-12
  in a new tab. In Equipment mode the form row label also carries the
  end-of-day meter reading (⏱) when one was logged.
  The sidebar's **Related DOT-12 Forms** links each carry an approval
  badge — green **✓ Approved** (signed off, not rejected) or amber
  **Needs approval** — with unapproved forms sorted to the top and the
  section header totaling how many still need approval. The breakdown
  grid's form rows carry the same ✓ / "needs appr." marks, so you can key
  through a cell's forms and see at a glance what's outstanding.
  The **Approval check** pill (Labor mode) paints **yellow** every day
  cell that includes at least one DOT-12 still needing approval — hours
  are never changed or hidden, and **red stays reserved for missing
  time**. Click a yellow cell and the sidebar's badges show exactly which
  form is the holdout. (This replaced the old "Approved only" pill that
  filtered the hour totals to approved forms.)
  The **Leave requests** pill (Labor mode, only when that feature is on)
  marks each leave day's cell with a corner triangle — grey = no DOP-L1
  filed, amber = pending, amber with a white notch = approved but no
  DOT-12 yet, green = approved and carried by a DOT-12 — and adds a
  **Leave request** block to the sidebar; see
  [Requesting leave (DOP-L1)](#requesting-leave-dop-l1).
  With a cell selected, the **arrow keys** move to the next filled cell
  along that axis — left/right stay in the same employee/equipment row,
  up/down stay in the same date column. Navigation never wraps to the
  next row or column: at the edge of the period (or when there's no
  further filled cell that way) the selection stays put and a toast says
  there's nothing further in that direction. The selected cell is always
  scrolled clear of the frozen Employee, Total, header, and totals
  panes so it's fully visible.
  The **download icon** in the top right of the filter bar exports the
  current org and **whatever date range you're viewing** — the selected
  pay period, the selected month, or your custom start/end dates — as a
  multi-sheet .xlsx — six sheets (seven when leave requests are enabled):
  *labor_total_time*, *labor_sick*, *labor_annual*, *leave_requests* (only
  with leave requests on — DOP-L1 request hours per employee per day,
  green = approved and carried by a DOT-12, amber = pending),
  *equipment_hours*, *equipment_meter_readings*, and a
  *metadata* sheet listing the exported date range, source URL,
  generation timestamp, and backend version. Every data sheet freezes
  the top row + leftmost column for scrolling. The button disables
  (with an explanatory tooltip) until an org and a valid range are
  picked — in Custom view that means both dates, start before end.
  In Labor mode an **All employees** checkbox adds every employee on the
  org's daily labor roster — even those with no DOT-12 hours this period —
  so they appear as all-zero rows (handy for spotting who hasn't logged
  any time). Off by default; the setting is remembered per browser and
  shared via the URL.
- **Reports → FMSUS Usage** — Family sick-leave usage matrix per employee
  per month, with the 80-hour calendar-year cap. The org picker only offers
  orgs you're assigned to (admins see every org with data) and defaults to
  **your home unit**.
- **Reports → Production Dashboard** — a live "what actually got done"
  board: units accomplished and hours charged **per activity per day**,
  for today plus the last few days (4-day or 7-day window). The top row
  of tiles shows today's labor hours, equipment hours, crews out (forms),
  people charging, and leave hours — each with a vs-yesterday delta and a
  per-day spark strip. The matrix below lists **every activity with work
  filed in the window**, sorted by activity code (code, name, unit of
  measure) with `units · hours` per day; leave and totals rows sit at
  the bottom. The **Scope** dropdown switches between
  your organization(s) and — for admins — any district or statewide.
  Next to the scope, two **accounting search fields** — **Task Order**
  and **Program** — narrow the whole board to one task order or program:
  start typing and matching values are suggested from forms **inside the
  selected window** (4d/7d) — so everything offered actually has work to
  show — each with its form count and last-filed date; pick one (or
  press Enter) and every tile and matrix row re-aggregates to just that
  work. You can still type a value that isn't suggested (e.g. an older
  task order) and press Enter to search it explicitly. An engaged filter
  glows green with an × to clear it, and the footer notes the active
  filter. Both fields can be combined. If the filtered work has nothing
  in the current window (e.g. a task order last used months ago), the
  matrix panel says so explicitly and shows the **last-activity date**
  instead of a silent all-zero table. The
  page **auto-refreshes every 15s or 30s** (or off) with a countdown
  ring; cells that changed since the last tick flash briefly, and today's
  column is highlighted. Polling pauses while the tab is hidden.
  **TV / wallboard mode**: the ⛶ button at the right of the Refresh
  control goes fullscreen — the app bar and controls drop away, the type
  scales up for distance reading, and the activity matrix becomes a
  slideshow that advances a page every 7 seconds (page dots top-right, a
  progress bar along the panel's bottom edge, leave + totals ride the
  last page). Live refresh keeps running, so it's made to be left up on
  a TV in the district office. Set your scope/filters/window first, then
  go fullscreen; **Esc** (or the ✕) exits back to the console.
  *Visibility*: the menu item and page only appear for entry roles
  (approver / time-entry / admin) and ops viewers; district and statewide
  scopes are admin-only. Today's numbers read **as-entered** — crews file
  through end of shift, so the today column grows during the day.
- **Reports → Timesheet Accounting** — Per-employee accounting line view
  for a pay period. The **All employees** checkbox adds everyone on the
  org's labor roster to the employee picker; choosing someone with no
  charges this period shows an empty accounting grid rather than hiding
  them. Off by default; remembered per browser and shareable via the URL.
  A **Labor / Equipment** toggle (like Org View's) switches the view: in
  **Equipment** mode you pick a piece of equipment (ED#) instead of an
  employee and see its accounting lines — which task order, activity,
  program and unit it ran, with daily hours. A day shown in **red** means
  that equipment ran an account no employee charged that day, so it can't
  be attached to a labor line for the nightly HRM hand-off (the cell's
  detail panel says whether it pins to an employee or is held back). The
  full org roster is always included (the *All employees* checkbox was
  removed). In **Labor** mode a **Standard / Clone** toggle also appears:
  **Clone** re-renders the selected employee's pay period as an OASIS-style
  **"Work Schedule"** timesheet — the same line blocks (Event, LDPR Profile,
  Unit/Activity/Sub-Activity/Program/Phase/Task Order), blue weekend entry
  boxes, daily HH:MM boxes, the **day-ahead** column tinted yellow, and a
  Total Hours footer — so it reads like the wvOASIS entry screen. Click a cell
  to crosshair its row + column; arrow keys hop between cells that have hours.
  The employee name + headers stay pinned on top and the Total Hours footer on
  the bottom. Leave lines show only their leave type.

  **Entry sessions.** In Labor mode, **Start Entry Session** opens a modal that
  explains the session, asks for the **entry day** (latest day you're entering
  through) and a **mode**, and shows readiness numbers (approved vs not-approved
  hours; how many timesheets with hours are still draft/submitted — so you can
  tell if it's worth starting). Once started, both the **Standard** and
  **Clone** views add **Confirm Entry** (records that this employee was keyed
  into OASIS and jumps to the next), **Report LDPR Issue** (logs a problem on
  the selected cell — doesn't block), and **Deny HRM Approval** (marks the day
  failed and, like Confirm, advances to the next employee). A **progress bar**
  in the top-right shows how far through the
  org you are. Confirm/Deny just mark the per-day status while you work;
  nothing happens to a DOT-12 form until you **Complete Session**, which first
  opens a **confirmation** spelling out how many employees are entered vs
  failed/denied (and, in hard mode, that it writes to real forms) — so it's
  never a one-click surprise. On confirm: in **soft** mode it records the
  status only; in **hard** mode it finalizes the **forms you actually worked
  on** — the fully-entered ones that a supervisor has **already approved** are
  **HRM-entered**, and any with a failed or not-yet-reviewed day are
  **rejected** (sent back to fix). A hard session **never approves**: a
  fully-entered form that is still draft/submitted is left as it is and counted
  under **Awaiting approval** on the summary card — HRM-enter it once its
  approver signs off. Forms you never touched are left alone. A session resumes where you left off. **Org
  View** (Labor) has its own **Entry Status** toggle: turn it on to mark each
  **(employee, day) cell** as a **green** box (entered) or **red** box (failed),
  with the entry date over the time (Eastern) beneath it.
- **Config → Pre-Trip** — *(only when the Pre-Trip feature is switched on;
  every signed-in user sees it)* the operator's daily and weekly equipment
  checklist: file one from your phone, view a truck's week, download the
  weekly sheet as a PDF, and sign off as a supervisor. See
  [Pre-Trip inspections](#pre-trip-inspections-config-pre-trip).
- **Config → Tags** — Create and manage tags for form categorization.
  Tags belong to a category (disaster / crew / misc). A form carrying any
  **disaster**-category tag shows a large red **DISASTER** stamp in the
  top-right corner of the timesheet — both on screen in normal form view
  and on the printed / exported PDF — so disaster-event labor reports
  (e.g. FEMA reimbursement) are unmistakable on paper.
- **Config → Users** — User management with org permissions and hierarchy.
- **Config → PIN Resets** — *(only when PIN sign-in is switched on)* the
  PIN reset requests waiting on you, with an amber count. Shown to approvers
  and admins, and to anyone with a request waiting on them. See
  [Confirming a PIN reset](#confirming-a-pin-reset-supervisors).
- **Config → Feature Flags** — *Restricted to the same two people who can see
  Logs and Analytics.* Turns the app's runtime feature switches on and off
  without a deploy or a restart — the next page load picks the change up.
  Each flag shows its key, what it does and when it was last changed.
  Two safeguards: a flag whose effect is big (**Email digest**, **Leave
  requests**) asks for a **second click** before it can be switched **on**
  (turning one off never asks), and if a flag would have no effect on this
  server — for example the email digest with no mail sender configured — the
  page says exactly why instead of letting you wonder. Flags are defined in
  the backend, so this page switches them but can't create or delete them.
- **Config → API Keys** — *Only for mms_user@wv.gov and
  bennett.murphy@wv.gov.* Issues keys that let another system (Timekeeper)
  use the DOT-12 API.
  - **Creating a key.** Name it, pick the app, a role (admin is allowed) and
    the orgs it may work in, an optional expiry, and whether it may proxy as
    other users. An admin key needs no orgs. On its own the key works as its
    own service account, with that role and those orgs.
  - **Copy it straight away.** The key appears **once** and isn't stored, so
    a lost key has to be replaced.
  - **Revoking** takes a second click and takes effect immediately.
  - **The list** shows each key's prefix, app, status, role, orgs, and when
    it was created, expires and was last used.
  - **Proxying a user.** The other system can name any DOT-12 user, by
    e-number, to act as. The request then runs as that person: their name on
    the form and its history, and their own role and orgs. They must already
    be a DOT-12 user.
  - **Timekeeper forms.** DOT-12s created through a Timekeeper key show a
    small **clock** marker in the forms list and a **Timekeeper** label at
    the top of the form.
- **Config → OASIS Postings** — *Only shown when the optional OASIS bridge is
  enabled, and only to the time-entry approval role / admins.* Tracks the
  automated postings the bridge stages into wvOASIS (queued / staged /
  reconciled / flagged / failed) and lets you retry ones that flagged or
  failed. When the bridge isn't enabled this page and the whole feature are
  hidden — the app works exactly as it does without it.
- **Docs → Usage** — This page.
- **Docs → DOT-12 Logic** — Internal business-logic and validation reference.
  The Usage and Logic pages share a left sidebar with a **table of
  contents** and a **search box** (press `/` to focus it): type to find
  matching sections, then click a result to jump to it — the matched
  words are highlighted and the section briefly flashes so it's easy to
  spot. `Esc` clears the search; `Enter` jumps to the top result.
- **Docs → Changelog** — Opens to a **Summary** view: a plain-language,
  per-day rundown of what's new (a few bullets a day, no jargon). Same
  data as the avatar's System Info modal, but full-page with a side TOC
  (by day) for quick jumping. Tab selection persists via `?tab=` so links
  survive a refresh. The detailed Frontend / Backend release logs (with
  per-entry type badges) are an additional set of tabs available to the
  operations account only.
- **Avatar → Approvals** — The approval/HRM/FIN triage page (shown when
  your role can approve **or** do HRM/FIN entry; see *Approval Workflow*
  above). The avatar badge totals the queues your role acts on:
  **approver** → all three (Awaiting Approval + HRM + FIN);
  **time-entry approval** → HRM + FIN; **admin** → all three.
- **Avatar → Profile** — Your permissions, orgs, supervisor, and direct
  reports. Also where you pick your **avatar color** (preset swatches at
  the bottom of the page) — available to every role; the color is only
  ever editable on your own account.
  The Profile page is also where you pick your **signature font**: ten
  cursive styles (the classic default plus nine scripts, from copperplate
  Pinyon Script to brush styles), each previewed with your own name. The
  live preview at the top replays your signature **exactly as it lands on
  a DOT-12** — the write-in animation, the date beneath, and the
  celebration sheen. Your choice applies everywhere your signature
  appears: the four signature boxes on every form you sign, the sign-here
  confirmation modal, and printed/exported PDFs. Like the avatar color,
  it's editable only on your own account, and other people's signatures
  keep *their* chosen fonts.
  **Upload your signature** (just below the fonts) lets you use your real
  handwritten signature instead.
  - Sign on plain white paper with a dark pen, then choose a straight-on
    photo or scan (PNG, JPG, GIF or WebP).
  - The paper is removed so only the ink shows. You see it on a
    checkerboard, where the checks mean "transparent", and **as it appears
    on a DOT-12**: an enlarged copy of the real signature box, so what you
    see is how much of the line it will cover.
  - It's drawn **as large as the signature box allows**. The whole picture
    has to fit, so a signature that's tall for its length (big loops, or two
    lines) fills the height and not the full width. If yours looks small,
    the picture probably has empty space or a stray mark above or below the
    writing — take a closer photo. Small marks well away from the writing
    (a speck, a bit of a printed line) are ignored automatically.
  - Adjust **Sensitivity** if faint strokes are missing (raise it) or paper
    specks show (lower it). Pick **Black**, **Blue** or **As photographed**
    ink, then **Use this signature**.
  - From then on it's drawn in every signature box you sign — DOT-12s, leave
    requests, pre-trips — in the sign-here preview, and in the DOT-12 and
    leave PDFs.
  - Your font isn't lost. **Remove — use my font** switches back, and
    **Replace…** uploads a new one.
  - **Tap any signature preview** on the Profile page (the font preview or
    your uploaded signature) to watch it sign again: the write-in, then the
    celebration glow, exactly as on a form.
  - Changing it also changes how forms you already signed display, the same
    as changing your font.
  (Rumor has it that clicking your avatar at the top of the page enough
  times makes signing considerably more patriotic. God bless.)
  Profile has a second tab, **Email & notifications** — see
  [Email & notifications](#email--notifications) just below.
- **Avatar → Send Feedback** — Opens the feedback modal (see below).
- **Avatar → System Info** — Version numbers and changelog (modal view).

## Email & notifications

**Avatar → Profile → Email & notifications** is where you decide how often
DOT-12 emails you and whose work you hear about. Each choice saves as soon as
you click it.

### How often we email you

Pick **Off**, **Once a day** (3:00 PM), **Twice a day** (6:00 AM and
3:00 PM) or **Four times a day** (6:00 AM, 11:00 AM, 3:00 PM and 10:00 PM),
all Eastern. The line underneath shows the day from midnight to midnight with
your send times lit.

The digest lists **what's awaiting your approval**, anything waiting on
**HRM/FIN time entry**, your **rejected** DOT-12s, any **leave requests**
needing you, and **what's new since your last digest**. Each line links
straight to the DOT-12 (or leave request) it's about. Two things worth
knowing: if you have nothing waiting and nothing new, **no email is sent at
all** — silence means you're clear; and the "new since" list is genuinely new
items only, not your whole unread history. Every email has a link back to
this tab.

### Who you hear about

This one choice decides whose DOT-12s and leave requests reach your **bell**
and the waiting lists in your **email**:

| Choice | DOT-12s | Leave requests |
|---|---|---|
| **My people only** *(default)* | Forms that **list one of your direct reports** as an employee | Your direct reports' |
| **Direct reports** | Forms **submitted by** one of your direct reports | Your direct reports' |
| **Everyone below me** | Forms that list **anyone under you**, at any level | Anyone below you |
| **Everyone in my orgs** | **Every** form in the orgs you approve for | Anyone below you |

- Each choice shows **how many people** it covers, with a bar so you can see
  how much wider one choice is than another. **Click the count** to see the
  list: each person's **name**, **org**, **short code** (their payroll ID
  without the leading zeros) and full **OASIS ID**. Search it by name, code
  or org.
- *My people only* and *Direct reports* cover the same people — the people
  whose supervisor is you. The difference is which forms count: the ones
  that *list* them, or the ones they *submit*. Use *My people only* when
  someone else keys DOT-12s for your crew.
- It only changes what you're **told about**. Everything you can approve,
  sign or enter still appears on the **Approvals** page and still counts on
  its badges, whatever you pick here.
- If someone has **no payroll ID** on file, DOT-12s that list them can't be
  matched, and the page tells you how many people that affects. An admin
  sets the Labor Code in User Management.
- If **nobody reports to you**, *My people only* sends you nothing about
  DOT-12s. Pick **Everyone in my orgs** to hear about every form in the orgs
  you approve for — that was how the bell worked for everyone before
  October 2026.
- Leave requests can never come from outside your own chain (they're private
  to the employee's supervisors), so *Everyone in my orgs* adds DOT-12s only.

## Feedback

Anyone can file feedback from **Avatar → Send Feedback**. The modal asks
you to pick a type — **Issue** (something's broken/wrong) or **Suggestion**
(an idea/improvement) — then a short **title** and optional **details**.
It automatically records **where you were** when you filed it (the page
you're on, its path, plus your app version, viewport, and — if you're in a
form — the form id), so you don't have to describe your location. Press
**⌘/Ctrl + Enter** in the title field to send. A confirmation appears and
the modal closes.

Operators (the Logs/Analytics allowlist) get a **Config → Feedback** inbox
that lists every ticket with KPI tallies (open / issues / suggestions /
total), filter chips by type and status, the author + the captured page,
and a per-ticket status dropdown (**Open → In progress → Resolved →
Closed**). Click a ticket to expand its details and full captured context.

### Replying — feedback is a conversation

A ticket is **two-way**. When someone files one, **the support team is
notified** right away (bell, and the next email digest). Open it from that
notification, from **Notifications → Messages** (which lists every request
for the support team), or by expanding the ticket in the operator inbox —
type a reply and the person who filed it gets a notification. They answer
from their own **Notifications → Messages**, which notifies the support team
again. Support replies are tagged **Support** so it's clear who's who.

You're also notified automatically when a ticket you filed is set to
**Resolved** or **Closed** (the in-between *In progress* step stays quiet, to
avoid noise). Opening any of these notifications takes you straight into the
conversation. See [Notifications & Comments](#notifications--comments).

### Experience rating prompt

Now and then, while you're actively using the app, a small **rating prompt**
appears in the bottom-right corner — tap a face (1–5, sad→happy) to rate your
experience. It never interrupts what you're doing (it's a corner toast, not a
popup), and you can dismiss it with the ✕. After you rate, it offers a quick
**4-question survey** (only if you choose "Sure"): how much easier/faster the
app is, how much it reduces data errors, whether you'd keep using it, and an
open comment. The prompt is occasional — at most once every few days, and not
again for a week after you complete the survey. Operators see the results in a
**CSAT** tab on the Feedback page (rating/answer distributions, conversion
rate, a trend, and recent comments).

### Restoring TheHub (admin only) — currently disabled

The admin **TheHub Database** restore card (an **Upload export zip &
restore** button that wiped and reimported the entire TheHub database
from an export `.zip`) has been **removed from the Profile page**. The
destructive restore feature is **dormant** — it isn't needed right now,
so there is no UI for it and the backend route is disabled. It can be
brought back later (the import logic is kept), but until then there is no
way to trigger a TheHub restore from the app.

## Logs (admin only)

**Config → Logs** opens the admin Logs viewer. The page surfaces five
on-disk JSONL files, with one tab each:

- **Requests** — one row per HTTP request handled by DOT-12. Columns:
  time, user, IP, method, path, status code, duration, response size.
  Filter by user, status class (2xx / 4xx / 5xx, etc.), or free-text
  search. The summary chip at the top shows total, ≥400 count, average
  and p95 duration for the current view.
- **Errors** — one row per unhandled server exception. Click a row to
  expand the full traceback inline.
- **Inventory** — one row per nightly Deighton inventory snapshot run,
  with `started` / `finished` / `failed` event types and the row counts
  pulled. The **Run snapshot now** button kicks off a fresh snapshot
  immediately (synchronous — usually under 30 seconds) without waiting
  for the next 7:30 AM ET fire. Useful when the previous nightly run
  failed.
- **Health** — one row per minute per app worker: a performance
  self-check. **Level** is `ok` or `warn`; a warn row is tinted and its
  **Issues** column says what crossed a threshold *and where to look*
  (e.g. "each open SSE stream pins an Apache thread", "lock table 78 %
  — MMS OASIS import?", "disk 3 % free"). The other columns are the raw
  tells: open live-update streams, request count / p95 / slow / 5xx for
  that minute, event-loop lag, DB pool use, the Postgres probe
  (connections, lock-table use, backends waiting on locks) and disk
  free. Expand a row for the full sample.
- **Host** — one row per minute from the server itself (a cron job, so
  it keeps recording even if the app is wedged): the Apache **:443
  accept backlog** (any number above 0 means users are waiting at the
  front door), connection counts to DOT-12 and MMS versus Apache's
  worker limit, load, memory, disk and which containers are up — with
  the same **Level / Issues** verdict.

**Auto-refresh** can be set to 5 s / 15 s / 30 s / 1 m or off. **Include
rotated** widens the read past today's live log into the previous days'
rotated files (`requests.log.2026-05-19`, etc., kept for 30 days).
Clicking any row expands it to show the full raw JSON entry — handy for
correlating fields the table doesn't show.

The page is hidden from non-admins. Logs persist across container
restarts because the directory is bind-mounted from the host; see the
deploy runbook for the mount path.

## Tally — analytics assistant

**Tally** is a conversational analytics assistant for your DOT-12 data.
Open it from the **Analytics** page via the **∑ Ask Tally** button in the
header, or go straight to `/dot12/analytics/tally`. Like the rest of the
Analytics surfaces, it's limited to the operator allowlist.

Ask questions in plain language — for example:

- "Labor hours by home unit for the last 30 days"
- "Which account-code combinations appear most across task assets?"
- "Forms filed per pay period this quarter, by org"
- "Top 10 employees by total hours charged this month"

Tally answers by querying the DOT-12 database directly and replies with
formatted markdown, using tables for tabular results. It's a **multi-turn
chat**: follow-up questions build on the conversation, so you can refine
("now just District 1", "break that out by week") without restarting.

- **Export to Excel.** Ask for a spreadsheet/report (or click **Download
  XLSX** when it offers one) and Tally builds an `.xlsx` you can download.
  A frozen header row plus a metadata sheet (the query, row count, and
  generation time) are included.
- **Conversation history.** Past conversations are saved privately to your
  account and listed in the left rail — click one to reopen it, or **New
  chat** to start fresh. The **×** on a row deletes it. There are no public
  share links.
- **Composing.** Press **Enter** to send, **Shift+Enter** for a newline,
  and **Stop** to abort a response that's still streaming.

**Which AI answers.** Tally normally uses Claude. An administrator can
switch it to **GK-4.7** (on Oracle Cloud) with the `tally_grok` feature
flag. Each new answer says which one wrote it ("Answered by …"). With
GK-4.7, each step's text appears all at once instead of word by word.

Tally is **read-only** — it can look at data but never change it, so it's
safe to explore freely. If a result is large it may be trimmed in the chat;
ask for an XLSX export to get the full set.

## Environment Indicator

The navbar color tells you which deployment you're looking at:

- **Blue navbar** — Production (`mms.transportation.wv.gov`). No badge.
  Sign in with WV state SSO (SAML).
- **Hot pink navbar with `STAGING` badge** — The staging instance
  (`mmsdev.transportation.wv.gov`). Data here is for testing only, and
  staging does **not** use WV SSO — you sign in with a dedicated app
  account (your e-number) and the shared staging password.
- **Teal navbar with `LOCAL` badge** — A developer's local machine
  (localhost / `*.local`). Same app-account password login as staging.

If you ever see hot pink or teal when you expect to be working in
production, **stop and check the URL** — you're not on the live system.

**The browser tab icon is colored to match.** Staging shows the WVDOT
seal on a hot pink square and local shows it on teal, so you can tell
several open instances apart from the tab strip without clicking into
them. Production keeps the standard blue icon — so if you have DOT-12
open in several tabs, the blue one is the live system.
