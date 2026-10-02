# Using Bridge Inspections

A guide to the app: browsing bridges and inspection reports, asking Bridge
Wizard questions about the fleet, and planning bridge work.

## What this app is

A browsable interface over West Virginia's bridge inspection record — roughly
8,600 bridges and 65,000 inspection reports extracted from Bentley AssetWise
Inspections, the system inspectors record their work in. Nothing you do in
this app changes the system of record. The one thing it stores is your
planning work: scenarios, plan runs and committed projects (see Planning).

## Signing in

The app asks you to sign in with your WVDOT account, the same one you use for
Windows and email. **Sign in with WVDOT** takes you to the state sign-in page
and brings you back to the page you were trying to open. A session lasts 12
hours. After that, or if you sign out in another tab, you get the sign-in
screen again.

Your initials at the top right open a menu with your name, email and employee
ID, and **Sign out**. For now everyone who signs in has full access.

## Getting around

One blue bar runs across the top of every page. The menu button at its left
opens the navigation:

- **Bridge Inventory** — the bridge list (the home page) and Bridge Wizard.
- **Bridge Management** — plan runs, Committed Projects, Projects, LISA scores
  and Configuration.
- **Help** — this guide, the logic reference and What's new. The running
  versions are at the bottom of the menu.

Next to the title the bar shows where you are, for example
*Bridge inventory / 01A003*; click an earlier part to go back up. The chip on
the right says what you're looking at: the inventory's bridge and inspection
counts, or "WVDOT-owned bridges" in Bridge Management. The sun/moon button
switches between light and dark.

## Finding a bridge

The home page lists every bridge in the inventory. You can:

- **Search** by BARS number, bridge name, or local name. The search waits until
  you stop typing.
- **Filter** by district or workflow status.
- **Sort** any column by clicking its header.

Each row shows the inspection count, the date and type of the most recent
inspection, and its workflow status. Click a row to open the bridge.

## The bridge page

A photograph from the most recent inspection, then identity — name, BARS
number, county, district, year built, owner — and a map at the recorded
coordinates.

Below that is the inspection history, grouped by year, newest first. Each entry
carries chips for the inspection types it covered and its workflow stage. Click
one to open the full report.

Four tabs cover the rest:

- **Overview** — the curated NBI and SNBI values for the bridge.
- **All Values** — every raw field captured against the bridge, searchable.
- **Elements** — element-level condition states (CS1–CS5) as stacked bars,
  where MBEI element data exists.

The gold **Asset** chip in the header opens the asset-centric view, which shows
everything hanging off the bridge at once: sub-assets, critical findings,
attachments, schedules, and linear-reference segments.

## The inspection report

Modelled on the printed report. The cover panel carries the identification
grid and a chip for each inspection type the report covered, then a condition
snapshot that prefers SNBI values and falls back to NBI 90, badging each cell
with which generation answered it.

Six tabs:

- **Report** — the report's forms and narrative sections, in the order they
  appear in the PDF. By default it shows only fields that have a value for
  this inspection; forms with nothing recorded are left out, and a note at the
  end says how many. Turn on **Show empty fields** to see the whole form, blank
  boxes included. Each form's header says how many of its fields are filled.
  Values recorded on fields the form doesn't lay out — mostly legacy NBI items
  on inspections from before the SNBI changeover — are listed under **Other
  recorded values** at the end, so nothing the inspector entered is hidden.
- **NBI / SNBI Values** — the reconciled ratings table with a source badge per
  row, then the raw SNBI and NBI 90 blocks where each exists.
- **Elements** — element condition states.
- **Photos** — every attachment, with cover and in-report badges. Non-image
  documents show as typed placeholders. Click any image to open the full file.
- **Raw Values** — every captured cell, searchable and paginated.
- **Original PDF** — the source document, embedded.

## Bridge Wizard

Open it from **Bridge Wizard** in the menu. Ask a question in plain English
and it queries the inspection database directly.

### Asking a question

Type into the box at the bottom and press Enter. Shift+Enter adds a new line.
The four suggestions on the opening screen each say what they will hand back —
a table, a chart, or an Excel file.

A question usually takes around half a minute, almost all of it the model
thinking rather than the database working. While you wait you can watch the
reasoning as it streams, and the queries appear in the margin as they run.
The page doesn't scroll on its own while an answer arrives, so you can read
the start of it in peace; scroll down when you're ready.

Questions about WVDOT's bridges are answered over the bridges WVDOT owns
(B.CL.01 Owner = S01), about 7,300 of 8,700. Each answer says its scope in
a line. Ask about "all owners", another owner, or a specific BARS number and
it answers over those instead.

### Checking the answer

Every answer carries its evidence in the right-hand margin: each query that ran,
numbered in order, with the row count it returned. Click any step to see the
SQL, or use the copy button to take the query somewhere else. Python steps
show their code the same way. Underneath is the
timing breakdown — total, model, and database.

This is the point of the layout. Bridge Wizard does not invent figures, and the
margin is how you check that for yourself.

### Charts and reports

Ask for a chart and it renders inline; click it to view full size, or download
the PNG. Ask for a report and you get a download card with the format, row
count and size — Excel, CSV, JSON, Markdown or PDF, and Excel supports multiple
sheets.

Excel workbooks are ready to hand on: a Summary sheet first (what's in it,
the scope, the data snapshot date), numbers and money formatted, dates as real
dates, condition ratings coloured Good / Fair / Poor, and Total rows that are
live formulas, so they follow Excel's filters.

If an export hits the row limit the card says so. An incomplete spreadsheet
that looks complete is worse than an error, so narrow the question and ask
again.

### Deeper analysis (Python)

For questions SQL can't answer on its own — how fast decks deteriorate by
material, survival curves of time to Poor, a regression, clustering, a
simulation, or a workbook laid out a particular way — the Wizard writes and
runs Python. You'll see a Python step in the margin with the code, and any
charts or files it makes appear with the answer.

The Python runs in a locked-down sandbox on the server: it can read the bridge
database and nothing else, has no internet, can't install anything, and is
stopped after 2 minutes. Ask for the method and caveats if they aren't in
the answer.

### Following up

Bridge Wizard remembers the conversation. You can say "now break that down by
year" or "just District 3 of those" without repeating yourself.

**Chats** in the header opens your history. Conversations are saved
automatically and named from your first question; you can rename or delete any
of them. Reopening a chat restores its charts and downloads along with the text.

### Sharing and feedback

There are two ways to share.

**Share chat**, in the header, copies a link to the whole conversation — every
question, answer and chart in the thread. **Share**, under the timings on a
single answer, links to just that one question and answer.

Either link works for anyone who can sign in to the app, meaning any WVDOT
employee who has the link. Someone outside WVDOT sees the sign-in screen and
can't open it.

A shared chat shows the answers, charts and downloads, but **not** the SQL
behind them. The evidence rail is for the person asking, not for everyone they
forward the link to.

Also under the timings: thumbs up or down records whether the answer was
useful, and **Copy** takes the answer as markdown.

### Stopping

The send button becomes a stop button while an answer is being written. If you
stop one, the answer says so and offers to ask again.

## Planning

The **Bridge Management** section of the menu is the planning area. It works
on the bridges WVDOT owns and that are in service, about 7,100 of them.

### LISA scores

Every bridge gets a LISA score from 0 to 100: structural (up to 55),
functional (up to 30) and essentiality (up to 15). It is the "New SR" from the
Quick SR workbook, calculated from the current inventory. The score puts each
bridge in a band:

| LISA | Band | Treatments allowed |
|---|---|---|
| 75 and above | Preserve | preservation, most rehab |
| 45 to 75 | Rehab | preservation, rehab |
| below 45 | Replace | preservation, replacement |

Click a BARS number to see how the score was built: each penalty, the inputs,
and a note wherever the score leans on a legacy NBI field or a gap in the data.

### Starting a plan run

**Plan runs → New run.** Pick a saved budget scenario or set up a new one:

- start year, number of years and inflation (the program workbook uses 3%)
- scope: all bridges, NHS or non-NHS, and optionally some districts
- a preservation budget and a capital budget for each year
- optionally, a target for the most poor deck area you'll accept; each year
  reports whether it was met

Choose which committed-project statuses to force in; approved, committed and
completed are forced by default. Then **Start run**. A statewide 6-year run
takes a few seconds, and the page follows it while it runs.

### Reading the results

- **Tiles**: total program cost (with the committed share), number of
  projects, and % poor and % good by deck area in the final year next to what
  doing nothing would give.
- **Condition by deck area**: % poor and % good each year, with the program
  (solid) and without it (dashed).
- **Spending by year**: committed, optimised capital and optimised
  preservation spending against the budget.
- **Map**: every bridge coloured by its most likely condition after that
  year's work. Larger outlined points get work that year. Choose the year at
  the top right.
- **Program**: every project by year. Filter, search, sort, or **Export
  .xlsx** for the list plus a by-year summary.

The run recommends; it doesn't decide. Tick projects in the Program table and
**Promote to committed** to send them to Projects as *proposed*.
There they can be vetted and moved on to approved or committed.

### Committed Projects (live from TheHub)

**Committed Projects** in the Planning menu shows the bridge projects in
TheHub, WVDOT's project programming system, as they are right now. The list
is read-only and refreshes every five minutes, or immediately with the
refresh button.

- **Stage:** *Active* projects have an open construction phase, whether
  they've been let or are funded to let. *Programmed* ones aren't funded for
  construction yet. *Completed* ones are finished.
- **Filters:** search, district, county and year. Clicking a bar in the
  year chart filters to that year.
- **Map:** each bridge is a dot coloured by its condition now. Completed work
  is faded, and the selected project's bridges get a dark ring.
- **Details:** click a project in the list or on the map to see its scope,
  construction milestones (let, award, start, complete), estimate against
  OASIS spend, its bridges and its phases.

Some projects include county or railroad bridges; they are listed but
planning leaves them out.

### Projects

**Projects** is the list plan runs use: the work that has to happen in a
given year, whatever the optimiser would pick.

- **Seed from TheHub** copies TheHub's bridge projects in, one row per
  WVDOT-owned bridge. Seeding again updates the rows in place. A project's
  cost is split across its bridges by deck area.
  - Finished work comes in as *completed*.
  - Let contracts come in as *under construction*.
  - Other active projects come in as *committed*.
  - Programmed ones come in as *approved*.
  - Rows from the program workbook that describe the same work are marked
    *cancelled*, so the money isn't counted twice.
- **Import program .xlsx** loads the district-vetted program workbook.
- **Add project** is for work the optimiser won't find on its own.
- **Editing:** double-click a year, cost or status to change it.
- **Opening a project:** click the `#` to open it.

In a run, a project always goes in its year and its cost comes off that year's
budget. Completed and under-construction work cost $0, because the money is
already spent or committed. The bridge isn't offered to the optimiser before
its year.

### A project's page

The project's name and status, its treatments, and tiles for its bridges,
condition now, expected cost, OASIS actual cost and letting or completion
date. There are five tabs:

- **Overview:** each bridge as a coloured tile (click one to open it), the
  Good/Fair/Poor split by deck area, the treatment and its cost per square
  foot, and a table of the bridges with each one's share and model cost.
- **Condition:** the outlook for the next 20 years, doing nothing against
  doing the treatment now. Pick another treatment to compare.
  - *Project average* shows each rating over time and the chance of Good,
    Fair or Poor each year.
  - *Bridge grid* shows every bridge by year.
- **Bridges:** every bridge's ratings, LISA score and traffic.
- **Costs:** TheHub's estimate, OASIS spend by phase, the BMS model estimate
  (deck area × cost per square foot, plus 3% a year), and the cost allocated
  to each bridge.
- **TheHub:** the live TheHub record.

### A bridge's planning page

Open one from a project, from the Committed Projects panel, or from a BARS
link in Projects. It shows:

- **Tiles:** the bridge's ratings, its LISA score and how many years until
  it is Poor.
- **Outlook:** a chart for each component with past inspections as dots.
  Pick a treatment to see its effect and cost.
- **Cost:** what the treatment would cost if done in each of the next six
  years.
- **Projects:** every project on the bridge.

**Inspections** jumps to the bridge's inspection record.

### Configuration

What every new run uses. A run keeps a frozen copy, so changing the
configuration never changes a finished run.

- **LISA scoring**: the band limits, whether to reproduce the workbook's Excel
  quirks exactly, and every other parameter as JSON.
- **Deterioration**: the fitted model for each bridge family and component,
  with its forecast from new. You can edit the yearly probabilities; edits
  survive **Refit from inspection history**.
- **Treatments & costs**: cost per square foot of deck, contract or state
  force, which LISA bands a treatment is allowed in, what kind of bridge it
  fits, when it's triggered and what it does to condition. Costs marked
  *placeholder* have no figure in the source documents; replace them before
  relying on a run.
- **Budget scenarios**: edit or archive saved scenarios.

## Docs

- **Usage** — this page.
- **Logic** — the internal reference: rating scales, the scope rule, inspector
  attribution, and how the agentic loop works.
- **Changelog** — what has shipped, by day.


## 3D terrain and flood views

Open a bridge's **3D Terrain & Floods** tab to explore its landscape. The pilot
began with Sandy Creek Girder (01A126), Rattlesnake (20A577), and Bloomingrose
(03A030); additional prepared WVDOT-owned crossings now use the same tab. Drag to pan, use the compass or Shift + arrow keys to rotate/tilt,
and scroll or use +/− to zoom. Overview, Plan, and Bridge side restore useful
views; the information panel controls the viewing angle, basemap and overlays.
Fullscreen expands the landscape. Elevations remain at true scale (1×).

The 50-, 100-, and 500-year buttons mean 2%, 1%, and 0.2% annual exceedance
probability. The three pilots have **preliminary calculated floods**: select a
period to change the water surface and flooded footprint for **200 feet upstream
and downstream** of the crossing. The headline shows estimated water elevation
at the bridge; the panel shows upstream/downstream elevations, discharge,
drainage area, assumptions and downstream-boundary sensitivity. Normal mapped
waterways continue outside this local flood reach.

Calculations use USGS regional flood discharges, DEM cross sections, Manning
conveyance and a steady standard-step water profile. They are estimates with
assumed roughness and boundary conditions; submerged channel geometry and
bridge pressure flow are not resolved. Big Coal River's flat local DEM slope
makes its results especially sensitive to the boundary assumption. Published
reviewed HEC-RAS results take precedence when available.

Click the map to inspect elevations and flood depth in feet. Missing flood
values mean unmodeled/unavailable, not dry. Preliminary samples use the 2 m
calculation grid. Freeboard requires reviewed low-chord inputs. Upstream and
downstream cameras follow the flow direction inferred from the terrain profile.

The alignment is cut from route milepoints and is not a measured deck elevation.
Mapped waterways are visible independently of flood scenarios. The **3D bridge
deck** uses the inventory width and approximate elevations from the DEM at the
bridge ends, with schematic thickness and edge rails. It spans the channel
instead of following terrain down into it. A reviewed surveyed mesh replaces
this preview when available. Use **Mapped waterways**, **3D bridge deck**, and
**Bridge alignment** to control each layer; water opacity also affects mapped
water vectors. These vectors do not represent a measured water level or flood.
The information panel names data sources, vertical reference and review status.
Archived 01A003 retains its own identity and links to nearby current 01A126;
the link does not establish a replacement relationship or show a historical model.

Links preserve the selected tab, for example `/bridges/20A577?tab=flood3d`.
Unprepared bridges explain that terrain is not yet available. A prepared site
whose calculation fails shows the reason in scene information; it does not get
a substitute flood surface. Batch scenes use a local terrain archive for the
surroundings and a separate lidar patch for the bridge and flood calculations.
Preparation now covers additional USGS flood regions and retries floods needing
wider terrain coverage. A bridge near a stream confluence may still need a
tributary/river boundary study before its flood surfaces can be shown. Batch
retry reports show recovered bridges alongside each site's original gap.
Revalidation can also withhold an earlier flood surface when its modeled
extent clips the water; that remains a modeling gap, not an absence of flooding.

If the mapped stream cannot be matched to the recorded bridge waterway, flood
results are withheld until the crossing is reconciled.
The hydraulic solver also checks for ambiguous solutions around overbanks.
When it cannot establish a unique valid water level, scene information explains
the modeling gap and the affected flood surfaces remain unavailable.

When older stream mapping is missing or cannot match the bridge waterway,
preparation checks USGS high-resolution centerlines before reporting the gap.
The same stream-identity and confluence checks still apply. If the main flood
calculation succeeds but the alternate downstream boundary does not, the scene
explicitly reports **boundary sensitivity unavailable**. That is an unresolved
uncertainty, not zero change in water level.
