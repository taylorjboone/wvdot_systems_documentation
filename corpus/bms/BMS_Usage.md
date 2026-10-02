# Bridges & BMS — Usage Guide

The bridge side of **AMPS** (Asset Management & Performance System). Two folders in the blue app bar (point at one to open its pages):

- **Bridges** — the AssetWise bridge inventory and inspection record (read
  only), and the **Bridge Wizard**, an AI assistant that answers questions
  about it.
- **BMS** — Bridge Management System planning: plan runs, run validation,
  committed and programmed projects, LISA scores and the planning
  configuration. It works like the PMS folder, with bridges in place of
  pavement segments.

Sign-in, users, roles and districts are the same as for pavement: admins
change anything; district users see everything read-only and propose changes
to their districts' run plans. Bridge ratings are NBI/SNBI 0–9 (Good 7–9, Fair
5–6, Poor 0–4), not the pavement 0–5 indices; colour on these pages always
means a condition rating. The logic behind the pages is in
[BMS — Business Logic](/docs/BMS_Business_Logic).

## Contents

1. [Bridges](#1-bridges)
2. [Bridge Wizard](#2-bridge-wizard)
3. [BMS plan runs](#3-bms-plan-runs)
4. [Validating a BMS run](#4-validating-a-bms-run)
5. [BMS projects, committed projects, LISA and config](#5-bms-projects-committed-projects-lisa-and-config)
6. [Refreshing the bridge data](#6-refreshing-the-bridge-data)

## 1. Bridges

Every signed-in user can open every page below. The inventory isn't split by
district, the same as the PMS segment pages. Nothing on these pages changes
data: they read the AssetWise inventory extract.

#### Bridge List (`/bridges`)

The page lists every bridge in the AssetWise inventory, about 8,700 of them,
a page at a time.

**Search and filters.** The search box does both:

- Typing searches the BARS number, the local and bridge names, the route, the
  feature crossed, the county and the design type.
- It also suggests filters whose value matches, grouped as bridge type,
  district, county, material and status, each with its number of bridges.
  Picking one adds it as a chip.
- It suggests the first matching bridges too; picking one opens that bridge.
- It suggests condition bands (Good / Fair / Poor / Not rated) and the other
  filters of the advanced panel (NHS, overdue, scour critical, …) by name.
- With an empty box, the suggestions are the type families, the condition
  bands, the districts and the statuses.
- **Moving through the suggestions previews them.** With the arrow keys or the
  mouse, the list and the map show straight away what picking the highlighted
  filter would give (for example only District 2), and a blue "Previewing"
  bar says so. Enter or a click keeps it; moving on, typing, Escape or closing
  the list drops it. A highlighted bridge overrides your filters and search while
  it is highlighted: the list shows that bridge alone and the map zooms to it.
  Enter or a click opens it; moving off it brings your results back.
- Remove a chip with its ×, or with Backspace in an empty box.
- Several values of one kind (two counties, say) match either one. Different
  kinds must all match.

Under the search, one pill per **bridge type family** shows its icon and how
many bridges it has; click a pill to filter to that family (click again to
drop it). The families group the NBI design type (item 43B):

| Family | Design types |
|---|---|
| Beam / girder | stringer / multi-beam or girder, girder and floorbeam, tee beam, channel beam, orthotropic |
| Box beam | box beam or girders (multiple, single or spread), continuous and segmental box girders |
| Slab | slab, and slab continuous over floorbeams / stringers |
| Truss | through, deck and pony trusses, including pin-connected, riveted, eyebar and Bailey panel trusses |
| Arch | deck and through arches |
| Suspension / cable | suspension, stayed girder |
| Rigid frame | frame (not frame culverts) |
| Culvert | culverts, including frame culverts |
| Other | movable, tunnels, modular, mixed types, and bridges with no design type recorded |

**All / In service / Archived** in the header filters by status.

The **filter icon** left of the search box opens the advanced filters in a
compact two-column panel. Changes apply at once: the list and the map update behind
the panel, and its header counts the matching bridges. Each filter also
appears as a chip in the search box, where it can be removed. The badge on the
icon shows how many are set; **Clear** drops them.

- **Condition:** Good (7–9), Fair (5–6), Poor (0–4) or Not rated, on the
  lowest current deck, superstructure, substructure or culvert rating. Pick
  one or more.
- **Each component:** Good (7–9), Fair (5–6) or Poor (0–4) for deck,
  superstructure, substructure, culvert, channel and scour, each with its
  number of bridges. Two bands of one component keep either (deck Fair or
  Poor); bands of different components must both hold (deck Poor and
  superstructure Poor).
- **Structure and traffic:** sliders for year built, longest span, total
  length, deck area, traffic (ADT) and the year last inspected. Lengths, area and traffic slide on a log scale. A slider applies
  when released.
- **Inspection:** inspection overdue (the last inspection plus the bridge's
  inspection interval is before today), and the interval (12, 24 or 48
  months).
- **Network and spend:** on the National Highway System, WVDOT-owned, scour
  critical (scour rated 3 or below), MMS work recorded, TheHub projects.

Ratings are the current SNBI values where recorded, otherwise the legacy NBI
item.

**Each row** shows:

- **Bridge:** the BARS number, the local name, and the route over the feature
  crossed. An Archived tag appears when the bridge is not in service.
- **Type:** the family's icon and colour, then the material and the NBI design
  type.
- **Longest span:** the longest span in feet, the number of spans and the
  total length.
- **Built:** the year built and the bridge's age.
- **Location:** county and district.
- **Condition:** the lowest current deck, superstructure, substructure or
  culvert rating, coloured and labelled Good / Fair / Poor on the NBI ranges.
  Hover for the rating's description. "Not rated" means no current rating.
- **Last inspection:** the date, its workflow stage (Approved, In progress, …)
  and its inspection type (+n when there are more).
- **MMS work:** the cost of the maintenance work MMS (dTIMS OM) has recorded
  on the bridge, worked out the same way as the bridge page's MMS work tab.
  Hover for the exact amount, the number of tasks and the last day worked.
- **TheHub spend:** the bridge's share of the spend to date (OASIS, all
  phases) of the TheHub projects that are **BMS treatments** (their
  construction code maps to a bridge treatment: deck replacement, structure
  replacement, joints, painting, …). Underneath, **+$… insp.** (blue) is its
  share of bridge inspection projects (TheHub construction code 49) and
  **+$… other** (grey) its share of every other project TheHub links to the
  bridge (roadway, guardrail, bridge work no treatment covers). A project on several bridges
  is split between them by deck area, so the column adds up across bridges
  without counting a project twice. Hover for both amounts and the number of
  projects. The **TheHub treatments** filter keeps bridges with treatment
  spend.

The two spend columns are refreshed every night, around 2:30 am, from MMS
and TheHub; "Spend …" in the header says when (hover it for each source). The
bridge page's own MMS work and TheHub projects tabs are still read live. When
a nightly read fails, the previous night's totals stay until the next
successful read.

Click a column header to sort by BARS, type, longest span, year built, county,
condition, last inspection, MMS work or TheHub spend. Numbers sort largest
first on the first click.

The filters, the search, the sort, the page and whether the map is shown are
kept in the address, so a view can be bookmarked or shared. The table fits as
many rows as the window allows; Ctrl/⌘ + ← / → pages through it. When the
table is narrower (the map is wide, or the window small), the county and
district move under the bridge's name and MMS work and TheHub spend share one
**Spend** column; on a small window Built is left out. The reload button
fetches the list again. Click a row to open the bridge; the bridge page's
**Back to results** returns to this view, filters and all.

**Plan in BMS** (admins, once a filter or search is set) starts a BMS run for the bridges in the list: it
opens BMS → Runs with the New Run dialog, the matching WVDOT-owned, in-service bridges as its **bridge list**
(the others are left out, since runs plan only those). For example, filter to District 4 and Poor, then Plan in
BMS to plan those 184 bridges.

**Map.** **Map** in the header opens a map to the right of the table showing
the bridges the filters match (it is off until you open it); drag the divider
between the table and the map to make it wider or narrower (the width is
remembered in this browser).

- Each bridge is a dot in its type family's colour; Archived bridges are
  faded. The legend counts the bridges of each family on the map, and the
  top corner says how many of the matches have coordinates.
- Zoomed in, each dot is labelled "BARS - local name".
- Click a dot for a card with the type, spans, year built, county and
  district, condition and last inspection, and an **Open bridge page**
  button. Click the dot again, or the ×, to close the card.
- Hovering over a row in the table rings its bridge on the map.
- The map refits whenever the filters change, including while previewing a
  suggestion. Bridges without usable coordinates are left off.
- Light / Streets / Satellite switches the basemap.

#### Bridge (`/bridges/:bars`)

**Header.** Kept short so the tabs get the room. The header and the tab bar stay
at the top of the window while the page scrolls, on every tab:

- **Back to results** (or **Back**) and the breadcrumb with the BARS number.
  Both return to the bridge list as you left it: its search, filters, sort,
  page and map;
- the bridge's name and location ("BOONE County, 0.03 MI N OF CR 3/16,
  on CR 3/13");
- chips for service status, district and owner.

The asset page is linked from **Identification** on the Overview tab.

**Tabs.** The selected tab is kept in the address as `?tab=` (`inspections`,
`history`, `elements`, `hub`, `mms`, `flood3d`; Overview has none).

- **Overview**:
  - **key facts**:
    - year built and age;
    - the last inspection's date and workflow status;
    - the number of inspections and the first year;
    - the TheHub projects on the bridge;
    - the MMS work cost, with the task count and the last day worked;
  - **truck traffic** and **load rating**, two cards side by side across the page below the map and facts:
    - truck traffic: the latest trucks per day, its share of the ADT and its
      count year, the change since the first count, and a chart of trucks per
      day by count year from 2009 with the all-vehicle ADT shaded behind (the
      FHWA NBI figure for each year where InfoBridge has one). Trucks are the
      SNBI annual average daily truck traffic (B.H.10) where recorded,
      otherwise the NBI ADT × NBI item 109 (truck percentage);
    - load rating: the latest NBI operating and inventory ratings (items 64
      and 66, metric tons; hover for the rating method), a step chart of both
      over the inspections, the latest SNBI rating factors (inventory,
      operating, legal; B.LR.05–07) with the method and rating date, and a
      warning when NBI 41 says the bridge is posted or closed;
  - **condition**:
    - the Good / Fair / Poor classification, from the lowest of the latest
      deck, superstructure, substructure and culvert ratings;
    - a drawing of the bridge in elevation (a culvert drawn as a barrel
      through fill), each part in the colour of its rating;
    - the ratings with their meanings. Parts rated N, or not rated, are
      grey and dashed;
  - **identification**:
    - bridge name, BARS, control number, design number, year built, owner
      and federal type;
    - county, district, location, route, coordinates, the asset (linked)
      and last update;
  - **recent activity**: the latest inspection, the latest TheHub project and
    the latest MMS task, each with **See all** to its tab;
  - a small map of the bridge point, and the cover photo when the extract
    holds one.
- **Inspections**: two panes that fill the window and scroll on their own.
  - **Left (a third)**: every inspection, newest first, grouped by year. The
    year stays at the top while you scroll. Each row shows the date, report
    type, inspection types, inspectors, workflow status, the Deck / Super /
    Sub / Culvert / Channel / Scour ratings, and counts of narratives and
    attachments.
  - Click a row to read its narrative on the right. The pick is kept in the
    address (`?insp=`), so the link opens the same inspection.
  - **Right (two thirds)**: the selected inspection's narrative, the most
    recent inspection until you pick another.
    - Summary & Recommendations comes first, then the report's sections in
      order: procedure, traffic, waterway, substructure, superstructure,
      deck, railings and so on.
    - Each section shows who last edited it and when.
    - **Jump to** (left of Open inspection) lists the sections; pick one to scroll to it.
    - "Photo #N" references open that inspection's photos.
    - Sections the inspection didn't record are listed at the end.
    - **Open inspection** opens the full inspection viewer.
    - The older WVDOT Standard report (before 2014) captured no narratives,
      and the pane says so.
- **NBI history**: how the ratings moved, one inspection at a time. It uses
  SNBI values where recorded and the legacy NBI item otherwise.
  - A step chart draws every rating the bridge has (deck, superstructure,
    substructure, culvert, channel, scour) over shaded Good (7–9),
    Fair (5–6) and Poor (0–4) bands.
    - When an inspection didn't record a rating (for example an SNBI
      inspection with the component marked N), the line carries the last
      recorded value forward. The point is a hollow dot, and the tooltip
      says when the value was last recorded.
    - Equal ratings are drawn slightly apart so each line stays visible; the
      tooltip shows the real value.
    - Click a rating in the legend to hide or show it.
  - Below it, a grid of every rating at every inspection, coloured 0–9:
    - ▼ / ▲ marks a change from the inspection before;
    - NBI / SNBI marks the source;
    - click a date to open that inspection.
  - **TheHub projects** on the bridge are marked on both, in purple (a
    project colour, not a condition colour):
    - on the chart, the construction period is lightly shaded from the start
      (TheHub's start date, else the let date; a paler year when neither is
      recorded) to completion, with thin dashed edges and a small flag at
      completion; the legend names it "TheHub construction". Overlapping projects share one band. Work not
      finished yet is shaded to its expected completion;
    - in the grid, a thin line with a dot above it between the two
      inspections either side of the completion (dashed when expected);
    - pointing at a flag or line shows the project: its name and number, the
      work (construction type and work codes), the completion date (marked
      estimated when TheHub's date is an estimate), the start, contractor,
      spend against estimate (for a multi-bridge project, this bridge's
      deck-area share and the project total), and whether the bridge is the
      project's primary bridge. Clicking opens the TheHub projects tab;
    - projects that finished more than a year before the first inspection
      are left off.
- **Elements**: the AASHTO MBEI elements, rolled up by element and grouped by
  part of the bridge (deck, superstructure, substructure, other), worst first.
  - Summary tiles give the element count, the share in CS1 by quantity, and
    the worst element.
  - Each row shows the quantity, the unit and a CS1–CS5 bar.
  - Expand a row for its protective systems and defects.
- **TheHub projects**: every project TheHub links to this bridge, newest
  first, read live from TheHub each time the page asks, whatever its work or
  status. TheHub names a bridge in three ways, and all of them count: as the
  project's primary bridge, on a route segment, or on a federal funding line
  (where a multi-bridge job such as "I-70 BRIDGES" lists most of its bridges).
  - The header splits the projects into **BMS treatment projects**, **bridge
    inspections** (construction code 49) and **other linked projects**, each
    with this bridge's share of the estimate and the spend. A project that is
    both a treatment and an inspection counts as a treatment.
  - A project that is a BMS treatment carries a **treatment chip** (indigo for
    capital work, teal for preservation) with the treatment's name and code;
    hover for the TheHub construction code it comes from. An inspection
    project carries a sky-blue **Inspection** chip instead. The same chips are on
    the project's side panel, the Overview's latest-project card and the
    Committed Projects list.
  - Withdrawn, terminated and reserve projects are shown dimmed as
    **Inactive**, after the others.
  - Each card shows the stage, the project number and year, the name and
    work type, programmed / estimated / spent cost, and the let,
    construction and complete milestones.
  - "Listed on a route segment" / "named on a federal funding line" marks a
    project that names the bridge there rather than as its primary bridge.
  - **This bridge's share.** A project on several bridges is split between
    them by deck area: the card shows this bridge's percentage and its share
    of the estimate and the spend, and the tab's total counts only this
    bridge's shares. The project's own programmed / estimate / spent figures
    are labelled "Project". A bridge with no deck area recorded counts as the
    project's average.
  - A project let through AASHTOWare also shows its **construction contract**:
    the contract's current milestone, a small life-of-contract bar, the
    number and net amount of its change orders, and the contractor.
  - Click a card to open the project panel. It adds the full construction
    contract (see *The construction contract* below).
  - When TheHub can't be reached, the tab says so; the rest of the page
    still works.
- **MMS work**: the maintenance work MMS (dTIMS OM) has recorded on this
  bridge, read live each time the page asks. It is shown the way the
  smartcar-mms DDL (daily detail listing) shows it:
  - **summary**: total cost with a labor / equipment / material / other bar,
    the number of tasks, the accomplishments by unit with hours, and the
    first and last days worked;
  - **one row per task**:
    - the task order number, linked to the task in dTIMS OM;
    - the activity code and description, and the organization;
    - the accomplishment and its unit;
    - days worked and the date range;
    - labor and equipment hours;
    - the cost mix and the cost;
  - each row is the task's total on this bridge (no day-by-day breakdown;
    the task number opens the days in dTIMS OM);
  - **Refresh** reads OM again;
  - only the task's lines on this bridge count. A day with costs but no
    accomplishment line can't be placed on a bridge, so it isn't counted.
- **3D Terrain & Floods** (full width):
  - a 3D scene of the crossing: terrain at true 1× scale, the bridge alignment,
    an approximate or surveyed deck, and mapped waterways;
  - the 50 / 100 / 500-year flood surfaces, when a preliminary or reviewed
    model exists;
  - **Scene information** panel:
    - view controls: satellite or map basemap, viewing angle, water opacity,
      and toggles for waterways, deck, alignment and cross sections;
    - click the map to read ground, water surface and depth at that point;
    - the calculated flood profile (upstream, at the bridge, downstream), the
      drainage area and regression region, the boundary sensitivity and the
      assumptions;
    - provenance and the vertical datum;
  - **Camera presets**: Overview, Plan, Bridge side, Upstream and Downstream
    (the last two need a flow direction), plus reset and fullscreen.

  Scenes exist only for WVDOT-owned (S01), in-service bridges that have
  prepared terrain. For any other bridge the panel explains why there is no
  scene. Archived 01A003 links to the nearby current crossing, 01A126.

#### Asset (`/bridges/assets/:asId`)

This is the asset-centric view of a bridge, or of any AssetWise asset.

**Header:**

- the asset id and name;
- for a bridge: its BARS number, county, district and location;
- chips for kind, status, federal submission type and guid (hover over the
  guid chip to see all of it);
- built, owner and last inspection;
- **Bridge view**, which opens the bridge page.

**Tiles and tabs.** Tiles count each branch of the asset: inspections (with
the number of recorded values), sub-assets, elements, critical findings, files
(with their size) and segments (with the number of schedules). Click a tile to
open its tab. The selected tab is kept in the address as `?tab=`.

- **Inspections** (report tasks only): each row shows the date, report type,
  inspectors, types, status and the counts of values and files. Click a row
  to open the inspection.
- **Sub-assets**: the sub-asset groups and element instances.
- **Elements**: the MBEI condition states from the newest inspection.
- **Critical**: the critical findings (work-management items), each with
  when it was raised, its stage, owner and assignee.
- **Files**: every file of the asset, as a photo thumbnail or a file tile.
  Each tile shows its size and marks whether it is an orphan (not mapped to an
  inspection) or has no binary.
- **Schedules**: the inspection and maintenance schedules. WVDOT mostly relies
  on a statewide cycle policy, so this tab is usually empty.
- **Segments**: the asset's linear-reference segments.

#### Inspection (`/bridges/inspections/:astId`)

**Cover:**

- report type and workflow status;
- the rating generation: SNBI, legacy NBI, or both;
- bridge identification as inspected: name, BARS, local name, county,
  district, owner, year built;
- the inspection: date, report type, types, workflow stage, location, route
  and coordinates;
- the inspection-type chips;
- a condition snapshot of deck, superstructure, substructure, culvert,
  railing, channel, scour, condition classification and structural
  evaluation, each with its source (SNBI or NBI);
- the inspectors.

**Tabs.** The selected tab is kept in the address as `?tab=`.

- **Report**: the AssetWise report form, section by section. Each label is
  paired with its recorded value, and the narratives are shown as formatted
  text. "Photo #N" references in a narrative are links that open the Photos
  tab and highlight that photo. A reference to another year's report is shown
  greyed and isn't linked.
  - By default only recorded fields are shown. **Show empty fields** shows the
    whole form.
  - **Other recorded values**, at the end, lists values on fields the current
    form no longer places. These are mostly legacy NBI items from before the
    SNBI changeover.
- **NBI / SNBI ratings**:
  - one row per condition rating, taking the SNBI item when it was recorded
    and the legacy NBI item otherwise, with its source and field ids;
  - below that, the raw SNBI condition and appraisal items (B.C, B.AP) and the
    legacy NBI items 58–72 and 113.
- **Elements**: the MBEI condition states.
- **Photos**: every attachment.
  - Cover and "In report" flags and the file size are shown.
  - Click a photo to open it full size.
  - Older reports from the paper era often have no photos.
- **Raw values**: every value captured on the inspection. It can be searched
  by field name or content, and shows 100 rows per page.
- **Original PDF**: the rendered report, embedded, with **Open in new tab**.
  If no PDF was extracted for the inspection, the tab says so.

## 2. Bridge Wizard

#### Bridge Wizard (`/bridges/wizard`, **brgzrd** in the app bar)

The Wizard's name and logo — **brgzrd**, a gold wizard hat on the deck of a
white arch bridge on a blue tile — mark its entry in the app bar and the top
of its page.

An AI chat over the AssetWise bridge inspection record ("Brigzard"). Ask in
plain English; the Wizard queries the inventory and answers with tables, and
can draw a chart or build an Excel, CSV, PDF, JSON or Markdown report.

It can also look up the work on bridges: TheHub construction projects (one
bridge's, or statewide by stage, district, county, year or name), the MMS
maintenance recorded on a bridge (tasks, hours and cost), and the nightly MMS
and TheHub spend totals per bridge — so questions like "which Poor bridges in
District 3 have nothing programmed in TheHub?" or "what has MMS spent on
20A397?" work. It knows which county is in which district, and by default
leaves archived bridges, other owners, test reports and unrated components
out of its analysis (it says so when it does).

- **Opening screen:** the size of the record (bridges and inspection reports)
  and four starter questions, each labelled with what it hands back (Table,
  Chart, Excel). Click one to ask it.
- **Asking:** type in the box at the bottom; Enter sends, Shift+Enter adds a
  line. While an answer is being written you see the model's reasoning ("Working
  through it"; only the most recent part is kept, so very long reasoning can't slow the page down) and progress lines; **Stop** ends it (then **Ask again**).
  Follow-up questions in the same chat remember what came before ("now break
  that down by year").
- **Scope:** answers cover **WVDOT-owned bridges** (B.CL.01 Owner = S01) unless
  you ask about a specific bridge, another owner or the whole inventory; every
  aggregate answer states its scope in one line.
- **Evidence column** (right of each answer): every step the Wizard ran,
  numbered — click to see the SQL (or Python), copy it with the copy button —
  and the time taken (total, model, database). The steps scroll in their own
  box (a long analysis can have dozens), following the newest step while the
  answer is written unless you scroll up, and the column stays in view as you
  scroll the answer.
- **While it works:** the "Working through it" box shows the model's reasoning
  and the line under it what it's doing now. A model that says what it's about
  to do before each query (Grok does) stays in this working view until its
  final answer.
- **Charts** appear above the answer; click to enlarge, **PNG** downloads it.
  **Reports** appear as a file card with format, rows, sheets and size, and a
  **Download** button; a report that hit the 100,000-row limit says so.
- **Under each answer:** Helpful? thumbs up/down, **Copy** (the answer text),
  **Share** (copies a link to that one answer).
- **Rating box:** now and then, after an answer, a small "How useful was that answer?" box with five stars
  appears in the bottom-right corner (with an optional comment). Rate it or close it; it disappears on its own
  after half a minute. How often it appears is set on System → Brgzrd.
- **Header:** **Chats** opens your history; **Share chat** copies a link to the
  whole conversation; **+** starts a new chat.
- **Chats drawer:** your conversations, newest first (plus older ones imported
  from the standalone app). Click to reopen one — charts, downloads and the
  steps come back, reasoning does not. Rename (pencil) and delete (bin) on your
  own chats. Admins get a **Show every user's chats** switch and can rename or
  delete any chat.
- If the server has no API key for the model that is answering, a warning says questions can't be
  answered; earlier chats and share links still open.

Who can do what: any signed-in user can ask; you see and change your own chats
(admins: all). Deleting a chat keeps its per-answer share links working.

#### System → Brgzrd (`/system/brgzrd`, named people only)

Only the people named on the server (`BRGZRD_ADMINS`) see this page or its menu entry; other admins don't.

Settings and analytics for the Wizard. The header shows the model answering now.

- **Overview:** pick 7, 30 or 90 days or all time.
  - Tiles: answers, users, cost (and per answer), median and 90th-percentile time to answer, time to the
    first streamed word, rating (with how many were asked and answered, and thumbs), tool calls per answer,
    error rate and the share of prompt tokens served from cache.
  - **By model:** each model and effort used, with answers, speed, cost, tool calls, tokens, rating and errors.
  - Charts of answers per day by model, cost per day and median time per day.
  - Tools used, users, and the slowest, most expensive and lowest-rated answers. Click one to open it.
- **Answers:** every answer, newest first, filtered by model, rating (rated / not rated / low) or text, with
  time, time to first word, cost, tool calls, tokens, rating and how it ended.
- **Settings:**
  - **Model:** DeepSeek (Fireworks, US-hosted, zero data retention; the default), Claude Sonnet (Anthropic) or
    Grok (xAI Grok 4.7 on OCI Generative AI, with the server's OCI credentials), each with its
    model id and effort (DeepSeek defaults to `low`, which is much faster with little loss), and **extra
    instructions** added to the shared prompt only when that model answers (DeepSeek's keep it from
    over-thinking). A provider without its API key on the server can't be picked. Switching applies from the
    next question, and chats carry on. Every change saves by itself.
  - **Limits:** the most tool calls per question, the most output per model call, whether the Python
    sandbox may be used, and **Fall back to Claude** (if DeepSeek or Grok fails before it starts on a question,
    Claude answers it; on by default). The page header shows which model is answering, and says why if it's the
    fallback. The badge beside the Brgzrd name reads **DS-{effort}** (DeepSeek), **GK-{effort}** (Grok) or
    **SN-{effort}** (Claude Sonnet).
    For Grok there are also **Grok max output tokens** (8,000) and **Grok tokens per minute** (200,000, the OCI
    limit): after OCI refuses a call for going over it, Brgzrd paces Grok's calls under it for a couple of
    minutes and shows "Pacing Grok…" while it waits.
  - **Feedback:** whether to show the rating box, the chance of showing it after an answer, and the fewest
    answers between two boxes.
  - **Prices:** $ per million tokens, used for the cost figures.
  - Every change saves by itself (clicks at once, typed values a moment after you stop typing), with a
    status line; a section's **Reset to defaults**. The change history lists who changed what and when.

#### Shared answer (`/bridges/wizard/share/:shortId`)

One question and its answer, with total/model/database time, the number of
queries, when it was asked and whether it was marked helpful. **Copy link**,
and **Ask your own question** goes to the Wizard. Any signed-in PMS user with
the link can open it.

#### Shared chat (`/bridges/wizard/chat/:convId`)

The whole conversation read-only: every question, answer, chart and download,
but **not** the SQL (the server leaves it out). **Copy link**, **Ask your own
question**. Any signed-in PMS user with the link can open it.

## 3. BMS plan runs

#### BMS → Runs (`/bms/runs`)

The list of bridge plan runs, laid out like the PMS Runs page. Admins can also ask the **Run Assistant** (top right of the app bar) to run bridge studies and save the runs worth keeping here; see [Run Assistant — Usage](/docs/Run_Assistant_Usage).

- **Columns:** ID, Name, Status (pending / running / completed / failed / cancelled), Years (first–last program year and count), $/yr (preservation + capital budget per year; a range when it varies; hover for the total and inflation), Scope (All / NHS / Non-NHS / Non-Interstate NHS, districts, "N listed bridges" for a run with a bridge list, and the % poor target if one was set), Result, Time, Created.
- **Result** shows, for a running run, its current step and a progress bar. For a completed run it shows:
  - a sparkline of % poor by deck area per year (red when it rises);
  - the final % poor and its change from today;
  - ✓ or ✗ against the target;
  - total spend and the number of projects.
  - Hover for the start/end % poor and % good, the do-nothing % poor and how many years met the target.
- **Sorting, paging and search** happen on the server. Click a header to sort. The search box matches the run name, the scenario name or a run id. Page, sort and search are kept in the URL.
- **Refresh:** the list refreshes every 5 seconds. A refresh chip shows while a run on the page is pending or running.
- **Row menu (⋯):** Download xlsx (completed runs), View run, **New Run from Config** (opens the New Run dialog prefilled from that run), Delete run.
- **Multi-select:** tick rows for the header menu: Open run, Download Excel and View logs (one row), or Delete (any number). Deleting a pending or running run stops it first. A run's results, logs and Validate history go with it. Projects already committed from it stay.
- **+ New Run**, "New Run from Config" and Delete are admin-only.

#### New Run dialog

A 3-step wizard like PMS's.

- **Load budget scenario…** (under the title) fills in and locks the program years, inflation, budgets, scope and target from a saved scenario of the chosen configuration. The chip's × unloads it. If you have already edited those fields you are asked before they are replaced.

1. **Run settings**
   - **Configuration**: which BMS configuration the run uses (default: yours), with its model chip. Its rules and
     budget scenarios are used; the run records the version it was made with. Changing it unloads a loaded
     scenario (scenarios belong to a configuration). With a **dTIMS** configuration, loading one of its budget
     scenarios keeps its budgets per category (NHS, NON NHS, BKAMPP, …); without one, the budget is a single
     amount per year for all categories. Years and categories with no budget get no work.
   - **Start year** is the first year of work (as in PMS): a dTIMS run starting in 2026 projects from the
     inventory as the 2025 starting state and plans work from 2026. That first year is an **evaluation year**:
     only committed projects are placed in it (none committed: no work, the year just shows condition); the
     optimizer plans from the second year.
   - Run name. It is optional and defaults to the scenario name.
   - Start year, program years (1–30) and inflation (%/yr; treatment costs inflate from the start year).
   - Benefit horizon (5–40 years).
   - Benefit weighting: traffic CWF, or none.
   - Which committed-project statuses are **forced**: proposed, approved, committed, under construction, completed. The default is everything except proposed.
2. **Budget & targets**
   - Preservation and capital budget per year ($M).
   - **Edit individual years** sets each year's two budgets separately, with a "Copy year 1 to all" button; "Reset to uniform" undoes it.
   - Max % poor target, by deck area, and (dTIMS configurations) min % good target.
   - **Optimizer** (dTIMS configurations): **Benefit / cost** (dTIMS-style; targets are reported each year) or
     **MILP: meet targets**, which picks each bridge's strategy so both targets hold in every program year within
     the budget, then the most benefit. If they can't all hold, it meets as many target years as possible and the
     run log and Trajectory tab say which years were missed. Committed work is always placed, even over budget.
   - Network: All / NHS / Non-NHS / **NHS − I** (NHS bridges not carrying an Interstate: functional class B.H.01 ≠ 1, the bridge counterpart of the pavement non-Interstate NHS runs).
   - Forced statuses: untick them all to plan with no committed projects (the network as if nothing were programmed).
   - Districts: empty means statewide.
   - **Bridge list** (optional): paste BARS numbers (one per line, or separated by commas or spaces; a column
     copied from Excel works) or **Upload CSV** (any CSV or text file: the BARS numbers in it are picked out).
     The run then plans only those bridges, within the network and districts above. Leave those at All to plan
     exactly the list.
     - The list is checked as you type: "184 bridges, all WVDOT-owned and in service", or which ones can't be
       planned and why (not in the inventory, not WVDOT-owned, not in service), with **Remove them**.
     - Anything that looks like a mistyped BARS (a BARS is 2 digits, a letter and 3 digits, e.g. 16A128) is named
       under the box instead of being dropped.
     - A run whose list still has bridges it can't plan is refused with their BARS.
3. **Review**
   - A summary with Edit links back to each step.
   - **Save as budget scenario** saves the current years, budgets, scope and target as a new named scenario, then links the run to it.

The footer shows the live plan summary: total budget, years, scope and target.

#### Run detail (`/bms/runs/:id`)

- **Header:**
  - status, program years, scope, inflation, target and inventory snapshot date;
  - live refresh while the run is running;
  - **Export** and **Validate**, both for completed runs (Validate opens `/bms/runs/:id/validate`);
  - an actions menu with Download Excel, Copy log data, Cancel run (admin, while running) and Delete run (admin).
- A progress banner shows while the run is running. A failure banner shows the error.
- **Years** read as the program year with its calendar year, e.g. **Year 3 · 2028**: Year 1 is the scenario's start
  year. The starting condition (a dTIMS run's year before the start) is **Year 0 · start of 2026** for a run starting
  in 2026. Tables, the treatment pivot, the drill-in, the map's year picker and the chart tooltips all use this; chart
  axes show the calendar year. The Excel export has a `run_year` column (1 = the start year, 0 = the starting
  condition) beside each calendar `year` (and `placed_run_year` beside `placed_year` on Committed).

**Tabs:**

- **Overview**
  - Headline tiles:
    - % of deck area Poor and Good in the last year, with the change from today and the do-nothing value;
    - spend vs budget;
    - projects and deck area treated;
    - years the target was met.
  - Charts:
    - **Condition by deck area**: % poor and % good with the program (solid) vs doing nothing (dashed), with the target line;
    - **Spend vs budget**: stacked committed / capital / preservation spend per year against the budget;
    - **Treatment mix**.
  - **Projected condition map**: MapLibre. Pick the year, and "All bridges" or "With work". Each bridge is coloured by its most likely condition class after that year's work. Click a bridge to open the drill-in.
  - Cards for Configuration, Budget schedule (per year, with spend) and Run details.
    A run with a bridge list shows it in the Configuration card: how many bridges, the first BARS as links to the
    bridges, "+ N more", and **Copy list** (one BARS per line, to paste into another run).
- **Trajectory**
  - Start → end tiles for % Good, % Fair and % Poor, plus the target (or average LISA).
  - The condition chart.
  - A heat table per year: % Good / Fair / Poor, % Poor if nothing is done, and average LISA.
  - A spend-by-bucket table: capital and preservation budget vs spent, committed spend, projects, deck area treated, and whether the target was met.
- **Treatments**
  - A stacked bar per year by treatment. Committed projects with several treatments are grouped as "Committed bundles".
  - A treatment × year heat table.
  - Switch the measure between Cost, Count and Deck area.
  - **By district** shows treatment × district instead, for all years or one year.
- **Projects**
  - Every project in the run: optimised and committed.
  - Filters: Year, County and District dropdowns, plus treatment chips.
  - Columns:
    - Year and BARS (links to the bridge plan outlook `/bms/bridges/:bars`);
    - Bridge, District, County, NHS;
    - Treatment, Bucket, Committed;
    - Cost, Benefit, B/C (×1e6);
    - LISA and band;
    - expected Deck / Super / Sub / Culvert ratings (NBI colours);
    - deck area, family;
    - an "inventory" link to `/bridges/:bars`.
  - The footer totals projects, deck area, cost and $/sq ft.
  - **Click a row** to open the per-bridge drill-in.
- **Committed Projects**
  - The committed projects the run forced in: the program year, the year the run placed each one ("lock only" when it falls after the horizon and only keeps the bridge out of optimisation), status, treatments, bucket, programmed cost and what was charged to the run's budget, and the TheHub project.
  - New runs show the snapshot frozen when the run ran. Older runs join to today's committed projects, and say so.
- **Logs:** filter by level and search.
- **Strategies** (dTIMS runs only): the dTIMS model builds many multi-year strategies for each bridge and picks
  one. Find a bridge (the list starts with the largest selected spend) to see:
  - a cost-vs-benefit chart of the strategies kept (PV cost per sq ft against PV benefit), with the frontier
    dashed and the selected one highlighted;
  - the table: PV benefit, PV cost $/sq ft, dollars, the benefit/cost gain over the starting strategy, and the
    treatments by year;
  - click a strategy for its year-by-year table (ratings and the main variables before and after the work);
    **Do-nothing values** adds the do-nothing path, **All variables** every model variable.

**dTIMS runs** show spend by the scenario's budget categories (NHS, NON NHS, …) instead of preservation /
capital in the spend chart, the budget schedule, the Trajectory spend table and the Bucket columns. Condition
classes are exact (a bridge is Poor or not) rather than probabilities. Nothing is scheduled in the start year:
it is the starting state, and work begins the year after.

**Per-bridge drill-in** (a drawer from the map, Projects or Committed):

- the bridge's inventory facts and current ratings;
- its year-by-year path in the run: expected component ratings, composite rating, P(poor), LISA and band, and any work with its cost;
- the committed projects on it;
- links to the plan outlook and the inventory page.

**Who can do what.** Everyone signed in can see runs. Starting, cancelling and deleting runs is admin-only. District users see only their districts' bridges in Projects, Committed, the map, the drill-in, the by-district treatment table and the Excel export. The network-level condition and spend summaries are the same for everyone, as in PMS.

## 4. Validating a BMS run

#### Validate a BMS run (`/bms/runs/:runId/validate`)

Opened from the **Validate** button on a completed BMS run. It is the same page as pavement Validate, working on bridges.

**What's on it**

- **Year lanes** (default): one column per program year (Year 1 = the scenario's start year), headed with its calendar year (**Year 1 · 2026**). Each card is one bridge's work in that year; its hover card, project window and map popup label the year the same way.
  - The card shows the bridge (or committed project) name, then BARS · deck area · cost · district, and the treatment icon.
  - The stripe on the left is the bridge's condition class expected when that year arrives, if no work is done before then. It uses the lowest of deck / super / sub / culvert: Good 7–9, Fair 5–6, Poor 0–4.
  - Hover a card for its details: carries / crosses, ratings now, lowest rating by that year, LISA in that year, budget bucket, benefit, and source (optimizer, committed project #, or added by hand).
- **Table view** (grid icon): one sheet per year, with Excel-style tabs.
  - Columns: BARS, Treatment, Budget (preservation / capital), Deck area, Cost, Rating, Lowest (expected lowest rating), LISA, Benefit, NHS, District, County, Status.
  - Click a column header to sort.
  - Drag rows onto a year tab to move them. Ctrl+PageUp / PageDown switches sheets.
- **District drawers** (the Districts toggle, lanes view): groups each year into districts, with a count, deck area and cost per district, and a breadcrumb while scrolling.
- **Lane footers**: the year's cost against its total budget, then a line with **P**reservation and **C**apital spend against their budgets (red when over).
  - Below that are the Good / Fair / Poor shares **by deck area of every bridge in the run** at the end of that year, under the plan as edited, on each bridge's lowest NBI rating. Each band is labelled with its range (Good 7–9, Fair 5–6, Poor 0–4) and drawn in its green / amber / red; the card stripes and the table's rating dots use the same colours.
  - Each share shows its change against the run's own plan. A shimmer means the totals are recalculating.
- **Map** (right third): the planned bridges as points, coloured by kind of work: deck, joints, painting, superstructure, substructure, culvert, replacement.
  - Hovering a card or row rings the bridge; clicking a card or row flies the map to it; clicking a point opens the project.
  - The map can be hidden with the edge tab, or **popped out** into its own window (`/bms/runs/:runId/validate/map`). The popped-out map follows the filters, hover and selection of the Validate tab, and clicking a point there opens the project on the Validate tab. "Pop back in" returns it to the page.
- **Header**: search (BARS, name, route carried, feature crossed, county, treatment code), treatment filter, district filter, a Live / Offline chip, the avatars of everyone viewing the run, the selection chip, the view toggles, and the **Edit** menu (Review proposals, History, Revert all).

**Actions**

- **Drag** a card to another year to move it. Moving is repriced with the run's inflation; a committed project that the run forced in keeps its programmed cost.
  - Multi-select with Ctrl/⌘+click (or the table checkboxes) to move several at once under one comment. Each time the selection changes, the map zooms to fit every selected bridge. Esc clears the selection.
- **Open** a card (pencil, or double-click a row). The dialog has these tabs:
  - **Overview**: KPIs and the lowest-rating outlook, doing nothing vs this treatment.
  - **Condition**: each component's expected rating, and the chance the bridge is Poor or Good, year by year.
  - **Bridge**: the bridge's facts, its other planned work in this plan, and the run's own projection year by year.
  - **Cost**: the cost in every year at the run's inflation.
  - **History**.

  From the dialog you can change the year and/or the treatment (only treatments that fit this kind of bridge are listed), remove it, commit it, or uncommit it.
- **Add** (＋ on a lane or sheet): pick any bridge the run projected; ones not yet in the plan are listed first, worst condition first. Then pick a year and a treatment, and a cost estimate is shown.
  - A bridge can have only one piece of work per year, so a move or add into a year where that bridge already has work is refused.
- **Commit** a project (or a whole year from the lane menu) to put it into the committed bridge program (BMS Committed Projects). Later BMS runs then force it in.
  - Committed cards are locked (no move, remove or retreat) until they are uncommitted.
  - A committed project the run forced in from TheHub or the programme list cannot be committed again; it already is committed.
- Every change asks for a comment and is kept in **History**. Admins can **Revert** any applied change (which adds a revert entry) or **Revert all**; nothing is ever deleted.

**dTIMS runs** in Validate: the lane footers show each budget category the scenario funds; a move or add is
repriced by the configuration's own cost formulas, with the bridge's other planned work included, and goes to the
budget category its formula gives. The treatment list in the dialog has the majors and the Structure Maintenance
activities (deck overlay, joints, painting, …), the ones the bridge would trigger first; the others are marked
"not triggered". Work can't be put in Year 1 (the starting state). The Add dialog shows the cost after you save.

**Who can do what**

- **Admins**: their changes apply at once. They approve or deny proposals (a deny needs a reason), revert, and revert all.
- **District users**:
  - They see only their districts' bridges; the footers still cover the whole run.
  - Their changes (with a required comment) become proposals. These show as dashed "ghost" cards and "pending" chips for everyone until an admin approves or denies them.
  - They can withdraw their own proposals.
- Everyone viewing the run sees changes animate in live, with a notice naming who made them.

## 5. BMS projects, committed projects, LISA and config

Everyone who is signed in can open every page below. Only **admins** can change anything. For district users, the write buttons are hidden or disabled, and the API refuses the write with a 403.

#### BMS → Projects (`/bms/projects`)

This is the list of bridge projects that plan runs force into the plan. Each row is one `bms.committed_projects` row, which is one project on one bridge.

**What's on the page**
- **Status tiles:** one per status (Proposed, Approved, Committed, Under construction, Completed, Cancelled), showing the count and total cost. Click a tile to filter by that status.
- **Table columns:** ID, BARS, project name, district, program year, TheHub construction codes, BMS treatments, cost, status, and source.
  - The source is TheHub (with its project number), Program workbook, Manual, or the plan run it was committed from.
  - A BARS number shown grey with a warning icon is not a WVDOT-owned in-service bridge in the inventory. Runs skip those rows. The count of such rows appears under the tiles.
- **Filters:** search (BARS, name, codes, notes), status, source, district and year.
  - Filters, sort and page are kept in the URL.
  - Click a column header to sort.
  - "Clear all" resets everything.
- **Navigation:**
  - Click a row to open the project page.
  - Click the BARS number to open the bridge's plan outlook.

**Admin actions**
- **Seed from TheHub:** writes one row per TheHub bridge project × WVDOT-owned in-service bridge. Re-seeding updates those rows in place.
  - Program-workbook rows that duplicate a TheHub project are marked Cancelled, with a note saying so.
  - A summary of what was written or skipped is shown afterwards.
- **Import program .xlsx:** replaces the rows from `final_bridge_program.xlsx` ("Back to Michael" tab).
  - It reports how many BARS numbers matched and which construction codes have no treatment (those are cost-only).
- **New Project:** opens a form with BARS, program year, name, treatments (none means cost only), cost, status and notes.
- **Edit / Delete:** tick one row, then use the ⋯ menu. Delete asks for confirmation.

#### BMS → Committed Projects (`/bms/committed-projects`)

Bridge projects read live from TheHub. This is the bridge counterpart of the pavement Committed Projects page.

**Header**
- Stage toggle: Active / Programmed / Completed / All.
- Search (name, number, BARS), district, county and year.
- Everything is in the URL, including the selected project, so a view can be shared.

**KPI row**
- Projects (and, under All, the split by stage).
- Bridges, with their deck area.
- CN estimate.
- Spent to date (OASIS, all phases).
- Next letting, or the latest completion when showing Completed.
- A projects-per-year bar chart. Click a bar to filter to that year.

**Body**
- **The list:** each row has a colour strip showing the condition band of its worst bridge. The strip is faded for completed work.
- **The map:** the projects' bridges as points coloured Good / Fair / Poor. Completed work is faded.
- **Detail panel:** clicking a project opens it with:
  - stage and status, scope, work codes;
  - construction milestones (Let / Award / Start / Complete);
  - CN estimate vs spent;
  - the bridges with their lowest rating now (links to each bridge's outlook);
  - the phases.

**Refresh:** the refresh icon re-reads TheHub (admin only). If TheHub can't be reached, the page shows the SSH-tunnel hint.

#### The construction contract (project panel)

The TheHub project panel shows **Construction contract** under the project's
facts. It appears on BMS → Committed Projects, on the BMS project page's
TheHub tab and on the bridge page's TheHub projects tab.

A project has a contract when it was let through AASHTOWare (AWP) and TheHub
carries the AWP feeds under its project number. District, force-account and
emergency work usually has none, and the panel says so. It is read live from
TheHub each time the panel opens.

- **Header**: the contract number (the TheHub project number), its current
  milestone (for example Work began or Final estimate approved), and the
  revision when AWP revised the contract.
- **Life of the contract**: a bar drawn to scale in days, with a point for
  each milestone:
  - the milestones are Advertised, Let, Awarded, Executed, Fully executed
    agreement, Notice to proceed, Work began, Substantially complete and
    Final estimate approved;
  - milestones a few days apart share a label;
  - the shading shows the run-up to work, construction and the closeout to
    the final estimate;
  - the time between groups of milestones is written on the bar;
  - a dashed *today* line shows while the contract is open;
  - hover a point for its milestone and date. A dashed point is a planned
    date that hasn't been reached.
- **Key numbers**:
  - how long the contract ran, from advertised to final estimate (or how long
    it has been open);
  - how long construction took (or has been under way);
  - the E&C (engineering and contingency) rate, against the average for
    contracts let the same year;
  - the change orders' net amount, their count and the days they added.
- **Change orders**: number, reason and description, and the completion
  date when an order moved it.
  - Net amounts are shown with the running total. Increases are amber,
    decreases green.
  - The first five are shown; **Show all** lists the rest.
  - Hover an amount for its participating and non-participating split.
  - An order counts once it is imported into TheHub, before it is approved.
- **Milestones**: every date. Where AWP's two feeds disagree, the date feed's
  value is flagged next to it.
- **TheHub construction phase**:
  - the contractor, the participating and non-participating amounts, and the
    CN phase and its dates;
  - checks that TheHub's construction start matches AWP's work-begin date,
    and that the phase end matches the latest change-order completion.
- **Identifiers**: AWP contract ID, proposal ID, state project and federal
  project numbers.

#### Project page (`/bms/projects/:id`)

A TheHub project that bundles several bridges is shown as one project.

**Header**
- Status, TheHub stage, treatments, program year, TheHub number and SPN chips.
- "Committed from run #N" when the project came from a plan run.
- **KPIs:**
  - Bridges and deck area.
  - Condition now: the average lowest rating by deck area, with % Poor and the worst rating.
  - Expected cost: TheHub CN estimate, otherwise the project cost, otherwise the BMS model.
  - Actual cost (OASIS).
  - Letting / completion date. A pre-1990 TheHub placeholder date is shown as "—".
- **Buttons:**
  - Committed Projects (opens the live TheHub view).
  - Edit (admin).
  - Show / hide map.
- `?tab=` picks the tab and `?map=0` hides the map.

**Tabs**
- **Overview:**
  - bridge tiles coloured by condition;
  - the Good / Fair / Poor share bar (by deck area);
  - the treatment, with $/sf, minimum interval and construction codes;
  - location and inventory (districts, families, deck area, average LISA, notes);
  - the bridges table, with year, status, deck area, cost share and model cost.
- **Condition outlook:**
  - The project average (by deck area) of each component rating and of the lowest rating, over 20 years. It compares doing nothing with the chosen treatment applied now; the treatment can be switched.
  - The chance of Good / Fair / Poor each year, by deck area.
  - Alternatively a bridge × year grid for one rating, in either scenario.
- **Bridges:** lowest, deck, super, sub and culvert ratings, LISA and ADT, with a link to the bridge's inventory page.
- **Costs:**
  - expected vs actual vs BMS model vs "in the plan";
  - by phase (TheHub / OASIS);
  - the allocation to bridges, split by deck area.
- **TheHub:** the same live detail as the Committed Projects panel.

**Interaction:** hovering a bridge in any table highlights it on the map. Clicking opens its outlook.

#### Bridge outlook (`/bms/bridges/:bars`)

The bridge counterpart of the pavement segment page.

**Header**
- Family, district, NHS, year built and facility.
- A "Committed work" chip when an approved, committed or under-construction project exists.
- A button to the bridge's inventory and inspections (`/bridges/:bars`).
- **KPIs:** lowest rating now, each component rating, LISA with its band, and years to Poor.

**Sections**
- **Deterioration outlook:** one chart per component and one for the lowest rating.
  - Each chart shows do-nothing (dashed) against the treatment (solid), with the inspection history as dots.
  - The treatment picker defaults to the project's or committed treatment. Its options list only treatments applicable to this bridge, with their $/sf.
- **Cost:** the treatment's cost today (deck area × $/sf), and its cost if done in each of the next six years, with inflation.
- **Bridge:** deck and cost area, materials, ADT, feature, LISA S1/S2/S3, and work history.
- **Projects on this bridge:** click one to open it.

**Parameters and map**
- `?project=` keeps the project context: breadcrumb, and the map shows the whole project.
- `?treatment=` picks the treatment.
- `?map=0` hides the map.
- `?config=` picks the BMS configuration (default: yours). With a dTIMS configuration the outlook compares doing
  nothing with the treatment applied in the first treatment year, using that configuration's model and costs.

#### BMS → LISA Scores (`/bms/lisa`)

**What's on the page**
- **Tiles:** scored / not scored, and Preserve / Rehab / Replace counts using the active config's band limits. Click a tile to filter.
- **Distribution:** a histogram, 10 points per bar, coloured by band.
- **Table:** BARS, bridge, district, NHS, family, LISA, band, S1/55, S2/30, S3/15, the four component ratings, and scoring notes.
  - Filters: search, band, district, NHS.
  - Columns are sortable.
  - "Export CSV" downloads the filtered rows.
- **Breakdown:** clicking a BARS opens the full score, with S1 (A–D), S2 (J, G, H, I, and tables 1–3), S3 (ADT × detour, STRAHNET, detour length), the fallback notes, and every input value.
- Clicking the row opens the bridge's outlook.
- "Scoring config" opens Config → LISA scoring.

#### BMS → Config (`/bms/config`)

The BMS **configurations**, like PMS Config. Each configuration has its own **model** and its own rules and budget
scenarios:

- **AMPS** (Markov): the AMPS bridge planner, with treatments, deterioration models and LISA parameters.
  "AMPS Markov (current)" is the configuration everything used before.
- **dTIMS**: WVDOT's dTIMS bridge model (years at each rating, element condition states, the dTIMS treatments and
  budget categories), reproduced in AMPS. Two come seeded:
  - **WVDOT dTIMS BMS**: dTIMS's configuration with its known errors corrected (see
    [BMS Business Logic](/docs/BMS_Business_Logic#the-dtims-model) for the list);
  - **dTIMS exact (2026-09)**: dTIMS's configuration exactly as read, errors included, for comparing with dTIMS.

- The list shows each configuration's model, comments, active treatments, budget scenarios, current version,
  last change and how many runs used it; chips mark the **System default** and **Your default**.
- Row buttons: ☆ make it your BMS default (what bridge outlooks, LISA scores and new runs use), copy
  (admins), 🌐 make it the system default (admins; for users who haven't picked one), delete (admins; not the
  system default). Deleting a configuration lists the runs made with it and asks before deleting them too.
- **New configuration** copies the system default. A copy has its own copy of every table; editing one never
  changes another.
- Your BMS default is also on your Profile ("BMS default config").

#### One configuration (`/bms/config/:configId`)

Runs made with a configuration record the **version** of it they used, so editing it never changes a finished run.
While a run is running on the configuration, edits are refused until it finishes. `?tab=` picks the tab;
non-admins see everything read-only.

The tabs depend on the model. An **AMPS** configuration has the tabs below; a **dTIMS** one has its own
([further down](#a-dtims-configuration)).

- **Overview:** model, comments (Rename), make it your default; the **Check** (ready for a run, or the problems to
  fix); the stored **Versions** (one is stored whenever a run starts with new content, with how many runs used it);
  the **Runs** made with it (version, or "own copy" for runs from before configurations).
- **LISA scoring:**
  - the Preserve and Rehab band limits (defaults 75 / 45);
  - the "reproduce the Quick SR sheet exactly" switch;
  - every parameter as JSON;
  - Save, Load defaults, Discard.
- **Deterioration:**
  - Choose a component (Deck / Superstructure / Substructure / Culvert), then the models table: family, level, inspection pairs, bridges, bridges in the inventory, years from 7 to 5, and whether it has been edited.
  - A chart of the expected rating from new, against statewide.
  - Selecting a model shows its annual stay probabilities p9…p2, with years in each state. Admins can save an override, which survives refits, or revert to the fitted values.
  - "Refit from inspection history" refits every model of this configuration that is not overridden.
- **Treatments & costs:**
  - Every treatment: code, name, budget (preservation / capital), $/sf and cost basis, cost source (placeholders are highlighted), allowed LISA bands, minimum years between treatments, TheHub codes, how many bridges it fits, and whether it is active.
  - Admins edit a treatment with the pencil icon or by double-clicking. They can change costs and basis, codes, bands, active, and the applicability / trigger / effects JSON.
- **Budget scenarios:**
  - This configuration's scenarios: years, scope, inflation, preservation / capital / total budget, and the % poor target.
  - Admins can create (New scenario), edit and archive scenarios.
  - The form sets name, start year, horizon, inflation, % poor target, NHS / district scope, an optional bridge list and the per-year budgets in $M ("Copy year 1 to all").
  - The same form is used in the new-run dialog.
- **Export to Excel / Import from Excel** (top right, like PMS Config): the whole configuration as one workbook.
  - Sheets: **LISA Parameters** (one row per parameter, e.g. `s1.load_exponent`, with its default),
    **Deterioration Models** (p0…p9 per family and component), **Treatments** (every column, with the
    applicability / trigger / effects JSON), **Budget Scenarios** and **Scenario Budgets** (preservation and
    capital per year). A README sheet says what each sheet allows; blue headers are editable, grey ones
    read-only, and every header has a note. The file records which configuration it came from.
  - Edit the file and choose **Import from Excel** on the configuration to change (`/bms/config/:configId/import`).
    Every row is checked and shown (changed cells as old → new, problems in red with the reason); nothing changes
    until the file is clean and an admin clicks **Apply**. The checks: LISA values keep their shape (a number,
    TRUE / FALSE, a 10-number list…) and the bands stay ordered; probabilities are 0–1; treatment rules use known
    keys, components and 0–9 ratings, and an active treatment needs a $/sf; budget years fall inside the scenario's
    years; and the whole configuration must still pass its Check with the file's changes.
  - A file exported from another configuration is flagged ("would be applied to …"), and a file of the other model
    is refused. If the configuration changed since the file was checked, Apply asks you to check it again.
  - Treatments can be added but not removed (set `is_active` FALSE); scenarios are created on this page and
    edited or archived in the file; a model whose probabilities you edit becomes an override (reset it on the
    Deterioration tab).
  - Runs already made keep the version they were made with, so an import never changes them; the review lists
    those runs.

#### A dTIMS configuration

The rules are shown read-only; change them with **Export to Excel**, edit, then **Import from Excel** (the same
review and Apply as above). Every formula is shown as written, with named expressions as links: click one to
see its text, what it uses and what uses it.

- **Overview:** as for AMPS (check, versions, runs).
- **Component curves:** for each curve family (deck, protected deck, superstructure by material, substructure,
  culvert), a chart of the rating path from each starting rating and the table of years at each rating (CR0–CR9).
- **Element curves:** how each element's condition states CS1–CS4 move over the years.
- **Treatments:** the majors and ancillaries with interval, budget category and trigger. Click one for a side
  panel with its trigger, its costs and its reset operations in order, and the treatments that may follow it.
- **Variables & formulas:** every variable in evaluation order (order matters: a formula sees this year's value of
  a variable above it and last year's of one below), with its initial value and yearly formulas.
- **Lookups:** the model settings (analysis and treatment years, discount and inflation rates, generation depth,
  strategies kept per bridge, budget years mode) and the lookup tables (unit costs, CCR weights, deterioration
  modifiers, …).
- **Committed map:** how a committed project's TheHub or AMPS treatment codes become dTIMS work.
- **Budget scenarios:** the scenarios with their categories (NHS, NON NHS, BKAMPP, …) and budget per year.

**The workbook for a dTIMS configuration** has one sheet per part: Settings, Fields, Variables, Yearly Formulas,
Expressions, Treatments, Treatment Costs, Reset Operations, Treatment Links, a sheet per lookup table, Committed
Map, Budget Scenarios and Scenario Budgets (a column per category). A formula that doesn't parse, or names a
variable, field, treatment or function that doesn't exist, is shown in red on its cell with the reason.

## 6. Refreshing the bridge data

The inventory is an extract of AssetWise (Bentley InspectTech). It is
refreshed by the `python -m pipeline bridges` stages and pushed to mmsdev;
see [PMS — Data Pipeline §16](/docs/PMS_Data_Pipeline). Pages read whichever
extract the server has; a plan run records the extract it used, and the
Validate page says when the inventory has changed since the run.
