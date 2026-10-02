# PMS — Usage Guide

How to use each pavement screen of **AMPS** (Asset Management & Performance System), WVDOT's asset management app: its Pavement Management System (PMS) pages, plus how to get around the whole app. The bridge pages have their own [Bridges & BMS Usage Guide](/docs/BMS_Usage). For *why* the numbers come out the way they do, see [Business Logic](/docs/PMS_Business_Logic). For what changed recently, see the [Changelog](/changelog).

## Contents

0. [Signing in](#0-signing-in)
1. [Getting around](#1-getting-around)
2. [Runs](#2-runs)
3. [Creating a run](#3-creating-a-run)
4. [Run detail](#4-run-detail)
   - [4a. Validating a run](#4a-validating-a-run)
5. [Projects](#5-projects)
6. [Committed Projects (live from TheHub)](#6-committed-projects-live-from-thehub)
7. [Config](#7-config)
8. [Analysis Segments](#8-analysis-segments)
9. [Multi-Year Analysis](#9-multi-year-analysis)
10. [Detected Projects](#10-detected-projects)
11. [Documents and Changelog](#11-documents-and-changelog)
12. [Tips and known quirks](#12-tips-and-known-quirks)
13. [Profile and Users](#13-profile-and-users)
14. [Data refresh (administrators)](#14-data-refresh-administrators)

---

## 0. Signing in

AMPS uses your **WVDOT account** — the same sign-in as your state email and Windows.

- Opening AMPS without being signed in shows a **Sign in** page. Click **Sign in with WVDOT**. You may briefly see the Microsoft sign-in page; if you're already signed in to Microsoft in this browser, it goes straight through.
- You come back to the page you were trying to open.
- Your avatar (your initials) appears at the top-right. Point at it (or click it) for your name, email and role, **Profile**, **Changelog** and **Sign out**.
- A sign-in lasts about 12 hours. When it runs out, AMPS shows the Sign in page again.
- For now, everyone who signs in gets the **admin** role.
- If sign-in fails, the Sign in page explains why. The most common cause is taking too long on the Microsoft page; just click **Sign in with WVDOT** again.

## 1. Getting around

- The blue bar at the top has the **AMPS** logo on the left (click it for [About AMPS](/docs/AMPS_Overview), a one-page overview of what AMPS is and what it's for), the folders, and your avatar on the right. There is no side menu.
- **Point at a folder** (or click / tap it) to open its pages; click a page to go there. The folder you're in is underlined, and the page you're on is marked with a blue left border in its menu. Ctrl/Cmd-click opens a page in a new tab. Esc or clicking elsewhere closes a menu.
- The folders, left to right:
  - **PMS**: Runs, Projects, Config, Analysis Segments, Multi-Year Analysis.
  - **BMS**: bridge plan runs (with Validate), bridge projects, committed bridge projects, LISA scores and the bridge planning config. These work like the PMS pages; see the [Bridges & BMS Usage Guide](/docs/BMS_Usage).
  - **Bridges**: the bridge inventory and inspections, and the Bridge Wizard.
  - **Documents**: About AMPS, this Usage Guide, Business Logic, Data Pipeline, LRS API, the Bridges & BMS guides and Changelog, then sub-folders that open to the right when you point at them: **WVDOT PMS** (the technical docs), **Pavement Studies** (the [raw distress study](/docs/Pavement_Raw_Distress_Study): how IRI, cracking, rut and faulting deteriorate, what treatments do to them and which treatment strategy and order follow), **Extras** ([Committed Projects](#6-committed-projects-live-from-thehub) and [Detected Projects](#10-detected-projects)), **Bridges** (bridge analysis reports) and **DTIMS PMS** (background material).
  - **System**: your [Profile](#13-profile-and-users), and **Users** for admins.
- On a narrow window the folder row scrolls sideways.
- Opening the site, or any unknown address, takes you to **Runs**.
- Most pages keep their filters in the address bar, so you can bookmark a view or paste the link to a colleague.
- On the Runs, Projects and Analysis Segments tables, **Ctrl/Cmd + ← / →** moves between pages.

### How it all fits together

PMS works in four steps:

- **[1] Data refresh.** Every so often (a new LRS download or a new survey year), administrators rebuild the road network: 0.1-mile analysis segments with their condition and traffic. The **pavement joints** are the potential project segments: each route's pavement, with long stretches cut at major crossing routes (the termini), in pieces of up to a few miles. A project always treats whole joints. Every config uses the same network.
- **[2] Config.** The engineering rules: what treatments exist, when they fit, what they do to the road, and how each kind of road ages. Its family rules sort every segment into a family. When an admin changes the rules or curves, only this **family step** reruns (seconds, for that config only); the data isn't rebuilt.
- **[3] Run.** An optimization of several years of pavement work on the roads and budget you choose. It produces a list of treatments over time (which treatment, where, in which year) along with the condition that results.
- **[4] Validate.** The run's work plan as cards, one lane per year, that are easy to move, remove, add or change. Every change is logged with who and why, everyone sees it live, and district users' changes wait for an admin's approval. **Commit** turns a card into a committed project, which feeds back into the run step: every later run locks it in.

<div class="diagram">

```text
  (every so often: new LRS or survey year)                                (changes rarely: admins edit or copy it)
+==============================================+                        +==============================================+
| [1] DATA REFRESH  -  the road network        |                        | [2] CONFIG  -  the engineering rules         |
+----------------------------------------------+                        +----------------------------------------------+
|                                              |                        |                                              |
| LRS routes, traffic and districts            |  the network           | TREATMENTS    what can be done and its cost  |
|   + the vendor's yearly condition survey     |----------------------->|   triggers    when a treatment fits          |
|   = 0.1-mile analysis segments with          |                        |   resets      what it does to the road       |
|     condition and traffic                    |                        | FAMILIES      how each kind of road ages     |
|                                              |                        | FAMILY RULES  which family a road is in      |
| PAVEMENT JOINTS: each route's pavement       |                        | BUDGETS       saved budget scenarios         |
| cut at its major crossing routes             |                        |                                              |
| (termini) = the potential project            |                        | Editing the rules or curves reruns only      |
| segments; a project treats whole joints.     |                        | the family step below, never the data.       |
+==============================================+                        +==============================================+
                                     \  after a refresh       after a rules or curve  /         |
                                      \  (every config)      edit (that config only) /          |
                                       v                                           v            |
                                   +================================================+           |
                                   | FAMILY STEP  -  runs on its own, in seconds    |           |
                                   +------------------------------------------------+           |
                                   | the config's family rules sort every segment   |-----------+
                                   | into a family, with its CCI and ages           |           |
                                   +================================================+           |
                                                                                                |  picked in New Run
                                                                                                v
+==============================================+                        +==============================================+
| [4] VALIDATE  -  the work plan, together     |                        | [3] RUN  -  optimize several years of work   |
+----------------------------------------------+                        +----------------------------------------------+
|                                              |      the PMS cycle     |                                              |
| Projects as cards, one lane per year.        |                        | You choose: the roads, the budget per        |
| Easy edits: move a year, remove, add,        |                        | year, targets and other constraints.         |
| change treatment; lane totals update.        |  the work plan         |                                              |
|                                              |<-----------------------| Each year: roads age, treatments that fit    |
| Every change is logged: who, why,            |                        | compete, the best condition gain per         |
| before -> after; everyone sees it live.      |                        | dollar wins until the budget runs out.       |
| District users propose, admins approve.      |                        |                                              |
|                                              |                        | Produces: which treatment, where, in         |
| COMMIT turns a card into a committed         |                        | which year, and the condition that           |
| project.                                     |                        | results (% Good / Fair / Poor by year).      |
+==============================================+                        +==============================================+
                        |                                                                       ^
                        |           committed projects are locked into every later run          |
                        +-----------------------------------------------------------------------+
```

</div>

Details: [Data refresh](#14-data-refresh-administrators), [Config](#7-config), [Creating a run](#3-creating-a-run) and [Validating a run](#4a-validating-a-run).

### Good, Fair and Poor

Everywhere in PMS — run results and targets, Validate, maps, project and segment pages — **Good / Fair / Poor is the MAP-21 rating of the measured distress**, the same way dTIMS rates it. The thresholds are the config's rating profile (shown on **Config → Policy**); the pages load it when you sign in, so they always rate exactly as the runs do:

| Measure | Good | Poor |
|---|---|---|
| IRI (in/mi) | below 95 | above 170 |
| Rut depth (in, asphalt) | below 0.2 | above 0.4 |
| Faulting (in, concrete) | below 0.10 | above 0.15 |
| Cracking (%) | below 5 | above 20 on asphalt, above 15 on concrete |

A road is **Good** when all three of its measures (IRI, cracking, and rutting or faulting) are Good, **Poor** when two or more are Poor, and **Fair** otherwise. Network percentages are shares of **lane-miles**. CCI and the other 0–5 indices are still shown as numbers and curves; they drive which treatments fit and how much good a treatment does, but not the Good / Fair / Poor label. Runs made before v1.6 used CCI bands (CCI ≥ 3 Good, below 2 Poor) and are tagged **CCI-based**.

The future comes from the dTIMS model: each index follows its family's curve from today's value, IRI and rutting follow PSI and RDI, cracking grows each year, and a treatment resets what dTIMS says it resets (details in [Business Logic](/docs/PMS_Business_Logic)).

## 2. Runs

A run is one budget-constrained optimization of the network: given a budget and a set of rules, which treatments should go where, and in which year. The Runs page lists every run and is where you start new ones.

Admins can also ask the **Run Assistant** (the button at the top right of the app bar): it works out the study a question needs ("how much do we need to spend to keep non-Interstate NHS at ≤5% Poor and ≥45% Good every year?"), runs it, and saves the runs worth keeping here, tagged as its own. See [Run Assistant — Usage](/docs/Run_Assistant_Usage).

**The table** shows, for each run: ID, Name, Status (Pending, Running, Completed or Failed), analysis Years, Look-ahead (older runs only; runs are now planned year by year), annual budget ($/yr), **Network**, **Result**, run Time and when it was Created.

- **Network** names the part of the network the run covered (Full network, Interstate, NHS, Non-Interstate NHS, Non-NHS, or "+ custom filter"); a **MILP** tag marks runs that used the exact MILP-assist optimizer, a **dTIMS** tag runs that used the dTIMS strategy optimizer. Hover for the full SQL filter.
- **Result** summarises a completed run: a small line of % Good over the plan, the final % Good with its change from today, and the final % Poor and total spend underneath (hover for the full numbers). Runs made before v1.6 carry a **CCI-based** tag: their % Good / % Poor used the old CCI bands and can't be compared with newer runs (see [Good, Fair and Poor](#good-fair-and-poor)). While a run is working it shows the current step and a progress bar; a failed run shows its error in red.
- Hover over **$/yr** for the full annual figure and the total over the period. **Time** counts up live while a run is going.
- Click a **column header** to sort; click again to reverse. Sorting takes you back to page 1.
- **Click a row** to open that run. Tick the **checkboxes** to select runs without opening them.
- The table size adjusts to your window; use the page controls at the bottom to move through the list.
- While any run on the page is still working, a small chip at the top shows when the list will next refresh. Click it to refresh now.

**Actions**

- **New Run** opens the run wizard ([section 3](#3-creating-a-run)).
- Each row's **…** menu: **Download xlsx** (completed runs), **View run**, **New Run from Config** (completed runs; opens the wizard pre-filled from that run, named "Copy of …") and **Delete run**.
- With rows ticked, the **…** menu at the top offers Open run, Download Excel, View logs (one run) and **Delete N runs**.
- **Deleting** asks for confirmation and can't be undone. If a selected run is still running, you'll be warned that it will be stopped immediately.

**The Excel workbook** has sheets for Configuration, Summary, Committed Projects (if any), Treatment Distribution, Condition Trajectory, All Projects, one sheet per program year and Constraints (if used).

## 3. Creating a run

**New Run** opens a three-step wizard: **Run Settings → Constraints → Review**. Your entries are kept as you move back and forth between steps.

**Configuration** (under the run name) picks the [config](#7-config) the run uses: its treatments, triggers, resets, family curves and rules. It starts on your default config (or, for **New Run from Config**, the original run's config). Budget scenarios, the treatment lists in the constraints and the segment count all come from the chosen config; changing it unloads a loaded budget scenario. The run detail page shows the config under **Configuration**. Runs made before configs existed read the system default.

### Loading a budget scenario

**Load budget scenario…** (top of the dialog) copies a saved scenario's budget, years, per-year schedule, carryover and district balancing into the run. While a scenario is loaded, those fields are locked. Click the × on the "Scenario: …" chip to unload it: the values stay but become editable again. If you've already typed budget values, you'll be asked before they're replaced.

The footer of the wizard always shows a one-line **plan summary**: the total budget over the years, the network (with the approximate number of segments once the filter is checked), and whether constraints are on.

### Step 1 — Run Settings

| Field | What it does |
|---|---|
| Run name | Optional label, e.g. "2026 baseline". |
| Annual budget | In $ millions per year (default 50). |
| Analysis years | How many program years to plan (1–50, default 20). |
| Edit individual years | Opens a year-by-year budget table. **Reset to uniform** puts every year back to the annual figure. |
| Optimizer | **Greedy (IBC)**: year by year, the best condition gain per dollar. **MILP-assist**: the exact optimizer for % Good / % Poor targets (set them on the Constraints step). **dTIMS strategies**: chooses the way dTIMS does — for each joint it builds every plan over the whole period (up to **Treatments per strategy**, 3 as in dTIMS) and picks one plan per joint by benefit per dollar, keeping every year inside its budget. Use it to reproduce a dTIMS budget scenario. **Unfunded years after** lets the plans look past the run's last year (dTIMS analyses often run two years past the years they report); those years get no work. It follows the budgets only (constraints are ignored) and doesn't carry money over. |
| Advanced settings | Collapsed under the optimizer row ("· changed" shows when any is set). **Start year** and **Inflation** override the config's for this run. **Concrete JCI from measured faulting** rates rigid pavement from its faulting. Untick **Force committed projects** to plan every segment freely (as a dTIMS scenario with IncludeCommitted off). **Start from a dTIMS run's inventory** gives every segment the condition, rehab year, family, ADT and lanes of the dTIMS section it lies on (for reproducing a dTIMS run); **dTIMS sections as planning units** then plans each section whole. **Hold (never treat)** (dTIMS strategies only) is a SQL WHERE of segments kept in the network but never treated. All of these are kept by **New Run from Config**. |
| ADT exponent | How strongly traffic weights benefit. Leave blank to use the config's (0.2, as dTIMS). |
| Min B/C ratio | Fixed at 0. |
| Budget carryover | Lets unspent money roll into the next year. |
| Network filter | ALL, INTERSTATE, NHS, NON-INTERSTATE NHS or NON-NHS. The matching filter is shown underneath. NHS comes from the LRS **Federal Aid** layer, as in dTIMS: NHS = Interstate, NHS and Intermodal Connectors; NON-INTERSTATE NHS = NHS and Intermodal Connectors, the same set as dTIMS's non-Interstate NHS analysis. |

### Step 2 — Constraints

Optional rules layered on top of the optimizer. Each has an on/off switch; turning one on opens its settings. With every switch off, the run behaves exactly like an unconstrained run.

1. **District Balancing & Filtering**: tick the districts to include (unticked districts are left out of the run entirely) and give each a share % and optional minimum and maximum dollars. The summary line turns green when the shares add up to about 100%.
2. **Network Condition Target**: a **% Good floor** (target % Good by a year), a **% Poor ceiling** (maximum % Poor by a year), or both, as MAP-21 shares of lane-miles. At least one must be on. **Max iterations** and **Damping** control how hard the greedy optimizer pushes toward the target. With **MILP-assist**, tick **Try to meet the targets every year** to hold them in every year up to the target year, not just the last. MILP-assist first checks whether every target can be met within the budgets; if so it keeps them all and then gets the most benefit it can. If not — for example year 1, before any work has had an effect — it first meets % Poor in as many years as it can, then, keeping that many, meets % Good in as many years as it can, then gets the most benefit while keeping both. While it works, the run's progress line shows the best plan so far, how close to proven-best it is, and which years still miss a target. The run's Overview then has a **Target check** listing each year's target, what was achieved and whether it was met. Tick **Find the minimum cost** (MILP-assist) to ask how much the targets need instead: the plan is the cheapest one that meets them. Set the annual budget to **$0** for no limit — each year's budget then shows that year's funding need — or keep a budget (e.g. a flat amount) to get the cheapest plan within it. The cheapest plan spends early and lets the network reach exactly the targets in the last year, so a 10-year need understates what keeps the targets afterwards; use a longer horizon for a steady-state figure. To spread the money so no year is empty or thin, set **Even spending**: a minimum share of the plan's biggest year (e.g. 50% — no year below half the peak) and / or a minimum $ per year. Both are hard, like the budget; with Find the minimum cost the plan is then the cheapest one that is also spread out. Below them: **Targets from year** (with every year, the first year held, e.g. 3 for "from 2028"), **Treatments per joint** (2 lets a joint be re-treated, what holding a target for many years needs), **Re-treat window**, **Cost basis** (minimum cost in nominal dollars or present value), **Solver time limit** (up to 14,400 s, 4 hours) and **Optimality gap** (stop within this % of the best possible plan; 1–2 % is plenty for planning). A configuration can set the share as its default (Config page → Policy, **MILP even spending**), used by every MILP-assist run on it that sets none.
3. **Treatment Caps**: the maximum number of a treatment per year. **Add cap** adds a row.
4. **Treatment Mix Floors**: the minimum % of spending for a budget category. **Add floor** adds a row. The total can't exceed 100%.
5. **Route Priority / NHS Boost**: multiplies the benefit of NHS routes and of route IDs you list.
6. **Bundling Bonus**: a benefit bonus for treating neighbouring joints together.

### Step 3 — Review

- **Additional SQL WHERE clause** narrows the segments further (default `1=1`, meaning no extra filter). It's combined with the network filter and any district choices. The pill next to it checks the filter as you type and shows roughly how many segments it matches. Click an example to try it.
- The summary card lists everything the run will use. Each section's **Edit** link jumps back to that step.
- **Save as budget scenario** saves the current budget setup for reuse (see [Config](#7-config)).
- **Start Run** is disabled until the filter is valid. After starting, a message offers **Open** to jump to the new run; the Runs list updates on its own.

## 4. Run detail

Opened by clicking a run. The header shows the run name, its status and a one-line summary (network · years · optimizer · constrained), a **Validate** button on completed runs (see [4a](#4a-validating-a-run)), plus a **…** menu with **Download Excel** and **Copy log data**. While the run is working, a progress bar shows the current step; if it failed, the error is shown in red.

The tabs (the selected tab is kept in the address bar):

**Years** are shown with their calendar year everywhere on the run: Year 1 is the run's start year, so a run starting in 2026 reads **Year 1 · 2026**, **Year 2 · 2027** and so on (charts and grids use the short form **Y1 2026**). **Year 0** is the network before any work, at the **start of 2026**. The Excel export does the same: a **Calendar year** column next to each Year column, "Year 1 · 2026" in the distribution headers, one sheet per year named like **Year 1 (2026)**, and the start year on the Configuration sheet. Runs made before start years were stored show plain "Year n".

- **Overview**:
  - **Headline tiles**: network % Good and % Poor (MAP-21, share of lane-miles) at the end of the plan with their change from today, the amount spent against the budget (with a usage bar), the number of projects with miles and segments treated, and the size of the network analysed.
  - **Network condition over the plan**: the share of the network Good / Fair / Poor each year, stacked to 100%, with dashed target lines if a condition target was set.
  - **Spend vs budget**: the amount spent each year (bars) against that year's budget (dashed line).
  - **Treatment mix**: spend by treatment, largest first, with project counts.
  - **Target check** (MILP-assist runs with targets): each target, per year when "every year" was on, with the share the optimizer predicted, the share the replayed plan achieved, and whether it was met.
  - Warnings, if any (for example a trigger branch that can never fire, or committed work above a year's budget).
  - The **Constraints** results when constraints were used, the run's **Configuration**, and **Run details**. Configuration's **General** tab is in sections: **Data** (configuration, network, the segment filter — its first line, with **Show full filter** for the rest — committed projects, held segments, a dTIMS starting inventory), **Budget** (annual budget, years, carryover, the budget scenario it was loaded from), **Optimizer** (the optimizer and its settings: strategy level and extra years, or the MILP objective, targets, treatments per joint, even spending and solver limits) and **Economics** (start year, ADT exponent, inflation and discount, rating profile, minimum B/C, the **config version** the run used). **Budget schedule** lists every year's budget.
- **Trajectory**: start → end cards for % Good, % Fair and % Poor (and a ✓/✗ for each target), a chart of the three lines by year with the targets, and the same numbers as a table.
- **Treatments**: a stacked bar per year split by treatment, then the treatment × year table. Switch between **Cost**, **Count** and **Miles**, and between **No grouping** and **By district**. Cap and mix-floor results are listed underneath. Each treatment keeps the same colour everywhere.
- **Projects**: every project (touching pieces of the same road getting the same treatment in the same year are one project) with its route, milepoints, treatment, year, surface, lanes, district, county, length, cost, benefit). Pick a year with the **year tabs** along the bottom of the table (**All**, then each program year with its project count and cost, as in Validate's table mode), filter by **County** and **District** with the menus beside the tabs, click a **treatment chip** above the table to show only that treatment, and click a column header to sort. The status bar beside the tabs totals the projects, miles, cost and cost per mile shown.
- **Committed Projects**: the same table, year tabs and filters for the projects that were already committed and locked into this run, with each committed project's name, extent and cost (with an explanation when there are none). All three optimizers (greedy, MILP-assist, dTIMS strategies) mark them.
- **vs dTIMS** (only on a run linked to a dTIMS run): the run against the dTIMS run it reproduces. An admin links a run with **Link to dTIMS run** beside the tabs, picking one of the dTIMS runs kept in AMPS (Non-NHS steady state, …); the tab then shows total spend and the last year's % Good / Fair / Poor (AMPS / dTIMS), % Good and % Poor by year (AMPS solid, dTIMS dashed), spend by year, and the treatments by year — miles or cost, each cell AMPS / dTIMS, with totals. **Unlink** or pick another run to change it.
- **Logs**: the run's log, updating live while the run is working. Filter by level (All / Error / Warning / Info, with counts) or search the messages.

### 4a. Validating a run

**Validate** on a completed run opens its work program as **swim lanes**: one column per program year (Year 1 = the run's start year), each project a card. It replays the run exactly as it was made — the config version it used, its start year and money settings, and the road data it started from — so changing the config or refreshing the data later doesn't change what you see. Runs made before v1.7 didn't store their road data; for them Validate uses today's data and says so if the numbers moved. A map on the right (a third of the screen; the small tab on its lower-left edge hides it, and the same tab at the right edge brings it back; the ⧉ button in its top-right corner **pops it out into its own window**, e.g. for a second monitor) draws every project in its treatment colour. Hovering a card (or table row) highlights its project on the map in yellow without moving the map; **clicking** the card or row pans the map to it. **Ctrl+click** (⌘+click on a Mac) a card to **select** it: it stays outlined and its project stays yellow on the map until you Ctrl+click it again. Each time the selection changes, the map zooms to fit **every** selected project, not just the one clicked. The same happens with the table's row checkboxes and its select-all box. Select as many as you like, in any years. Drag any selected card into another year and every selected project moves with it (committed ones stay), with one comment for the lot. While anything is selected, a blue **N selected ×** chip in the header clears the whole selection, in every year and sheet; Esc does the same. Hovering a line on the map lights up its card, and clicking it opens the project.

**Cards** show the project name (route, direction and milepoints, or the committed project's name), miles, cost and district. The coloured stripe on the left is the MAP-21 rating (Good / Fair / Poor) the road is expected to have when that lane's year arrives if nothing is done before then — the rating covering most of its lane-miles — so the same road shows worse in later years; the details have today's CCI, the projected CCI and that rating. The icon at the end of the row is the treatment: layers for overlays, a slab for concrete repair, a house for reconstruction, a drop for seals. Hover the name for the details (route, joint, segments, lane-miles, CCI, benefit). Each lane lists its projects costliest first and loads more as you scroll: 25 at a time as you near the bottom. At most about 100 cards stay loaded; the earliest ones are let go from the top and come back when you scroll up (faint placeholders stand in for them meanwhile). Cards you (or others) move stay visible in their new lane either way.

**Districts** (the folder toggle in the top bar, lanes view; kept in the address bar as `?group=district`) groups every year into **district drawers**, all closed to start. Each drawer shows the district's number of projects, miles and cost, with a bar for its share of that year's cost. Click a drawer to open or close it; several can be open at once. While you scroll through an open district's cards, a breadcrumb at the top of the lane shows where you are (**All districts › District 2**, with its count and cost); **All districts** closes every drawer in that lane. The lane's **⋮** menu has **Expand all districts** and **Collapse all districts** (greyed out unless Districts is on) as well as **Commit all of year N**.

**Changing the plan.** Every change asks for a comment and shows what will change (for example "Y4 → Y6 · $1.20M → $1.25M"):

- **Move**: drag a card into another year — grab it anywhere on the row (on a touch screen, use the ⋮⋮ handle so swiping still scrolls); the lanes scroll when you drag near the edge, the target lane is outlined, and **Esc** cancels. The card lands in the new year while you write the comment; **Cancel** sends it back. The cost is re-inflated at 2% a year.
- **Remove**: the bin icon on the card, or **Remove** in the project window.
- **Change treatment**: open the card (pencil icon) and pick another treatment. Only treatments for the road's pavement type are offered, each with its cost.
- **The project window** (pencil icon) has these tabs. The curves run over the plan's years and compare the project's treatment in its year (blue) with doing nothing (orange, dashed).
  - **Overview:** cost, length, CCI now and at the end, benefit, and the CCI outlook. Under it, **Pavement measures** charts IRI, rutting, cracking and faulting, the raw distress behind the MAP-21 rating. Each is a length-weighted average over the project's segments that the measure rates (faulting only on concrete, for example), shaded Good / Fair / Poor.
  - **Condition:** **Pavement measures** first (the same IRI, rutting, cracking and faulting charts), then every condition index (CCI, PSI, RDI, …).
  - **Segments:** the condition of every 0.1-mi analysis segment in the project in every year of the analysis, as a grid: one row per segment, one column per year.
    - Pick the measure: the MAP-21 **Rating**, a condition index (CCI, PSI, RDI, SCI, ECI, CSI, JCI) or a raw measure (IRI, rutting, cracking, faulting).
    - Pick the scenario: **With** the project's treatment, or **Doing nothing**.
    - Each cell shows the value that year. A raw measure is coloured by its own Good / Fair / Poor band; an index or the rating is coloured by the segment's MAP-21 rating that year.
    - The treatment year's column is marked in blue.
    - An empty cell means the measure doesn't apply to that segment's pavement (faulting on asphalt, RDI on concrete, and so on).
    - Click a segment number to open it in a new tab.
  - **Cost** and **History**.
- **Add**: **+** at the top of a lane. Search any road in the run's network (roads not yet in the plan are listed first, worst condition first), then pick a treatment and year.
- **Commit**: in the project window, or **⋮ → Commit all of year N** on a lane. Committing puts the project into PMS's committed program (Projects page). Future runs then lock it in. Committed cards show a green lock and can't be moved; an admin can **Uncommit**.

**Lane footers** (always visible at the bottom of each lane) show the year's cost against its budget (red when over) and the change from the optimizer's plan. They also show **% Good / Fair / Poor of the whole analysed network** (MAP-21, share of lane-miles) in that year under the current plan (not just the listed projects), with the change in % Good and % Poor from the optimizer's plan. The bars shimmer for a second or two while the numbers are recalculated.

A long run name is cut short in the header; hover it for the full name with the plan at a glance (years, projects, cost against budget, the network's Good / Fair / Poor in the last year and any proposals waiting).

**Popped-out map.** The map window stays linked to the Validate page: it shows only the projects the page lists (filters included), hovering a card or row highlights the project there, and clicking one or selecting it pans the map to it. Hovering a line in the window lights up its card, and clicking a line opens the project on the Validate page. **Pop back in**, at the top right of the window or on the small tab at the page's right edge, closes the window and puts the map back on the page. Closing the window does the same. A dot in the window shows **Linked** while the Validate page is open; reloading either one re-links them. If the browser blocks the window, allow pop-ups for the site.

**Header filters** are compact: **Search** widens while you type, the treatment menu and **D all** district menu list how many projects each has, and when any filter is on a blue chip shows how many projects are listed (e.g. *42 of 564*); its × clears every filter.

**Table view.** The toggle at the top right (columns icon = lanes, grid icon = table; kept in the address bar as `?view=table`) shows the plan as a spreadsheet instead, one **sheet per year** with small tabs along the bottom as in Excel. Each tab shows the year and a tiny Good / Fair / Poor bar for the whole network at the end of that year (a red dot when the year is over budget). Hover a tab for its projects, miles, cost against budget and the % Good / Fair / Poor with the change from the optimizer's plan. The sheet lists every project in that year: project (pinned at the left while you scroll sideways), route, milepoints, treatment, miles, lane-miles, cost, the MAP-21 rating and projected CCI by that year, benefit, district, county and status (committed, added, pending proposals). Click a column header to sort (again to reverse, a third time for the default order). **Ctrl+click** (⌘+click on a Mac) a row, or tick its checkbox, to select it. Do the same again to deselect it. Selected rows stay highlighted, and the header checkbox selects or clears the whole sheet. A dark bar above the tabs shows how many are selected, their cost and an × to clear them. **Drag a row onto another year's tab** to move the project there. If the row is selected, every selected project moves with it, on any sheet (committed ones stay). It's the same move as dragging a card: the tab lights up under the pointer, **Esc** cancels, and one comment covers every project in the move. A plain click on a row pans the map to it; double-click it (or the pencil) to open it. The bar at the bottom right totals the sheet and has **+** (add a project to this year) and the lock (commit the whole year). **Ctrl+PageUp / PageDown** switch sheets.

**Roles.**

- **Admins** see every project, and their changes apply at once.
- **District users** see only projects in their districts. Their changes are **proposals**: a dashed "ghost" card in the target year, and a "pending" tag on the card it would change. A comment is required.
- **Edit ⋯ → Review proposals** (the red badge on **Edit** shows how many are waiting) lists proposals. Admins **Approve** them, or **Deny** them with a comment; you can also approve straight from a ghost card. Authors can **Withdraw** their own proposals.

For a run made before v1.6 a blue note says its stored numbers were CCI bands; the footers always use today's model.

**Edit ⋯ → History** lists every change ever made, newest first, with who made it, the comment, and the before → after. Admins can **Revert** an applied change. Reverting adds a new "revert" entry rather than erasing anything; a change that later changes depend on must have those reverted first. **Edit ⋯ → Revert all** (admins) resets to the optimizer's plan by reverting everything.

**Live.** The green **Live** chip means you're connected. Everyone viewing the run sees changes animate in as they happen, with a note in the bottom-left saying who made them. The avatars show who else is viewing.

If the run's data has changed since it ran, a yellow banner says so and the footers use today's data.

## 5. Projects

**Committed & Past Projects** is the PMS's own list of projects: work that is planned or under way (which runs treat as already committed) and past work (which feeds the multi-year history). Each row is one TheHub route segment of a Hub project.

- **Search** (top): type and pick from the suggestions — construction **years**, **treatments** (by id or name), **statuses**, **project names** and **Hub IDs**, each with how many rows it matches — to add a filter tag; press Enter on any text to add a **Contains** tag that matches the name, route, Hub ID or treatment. Tags of the same kind match any of them (Year 2013 or 2014); different kinds must all match (Year 2013 and Thin Overlay). Remove a tag with its ×; **Clear all** removes every tag and goes back to page 1.
- **Year tabs** along the bottom of the table: **All**, then each year with its number of projects and cost under the other tags. A project's year is its construction year, or for committed work (no construction year yet) its program year. Clicking a tab replaces any Year tags; the status bar beside the tabs shows the rows and their cost.
- The page number and the tags are in the address bar (`?year=2013&treatment=THIN_OVERLAY&page=2`), so a filtered view can be bookmarked or shared.
- **Click a row** (or its **#ID**) to open that route segment's **project segment page**; click the (blue) **project name** to open the whole **project page** (below). **New Project** opens a blank form; with one row ticked, the **…** menu offers Edit and Delete.
- Form fields: **Project name** (required), Hub ID, Route ID, **Status**, BMP and EMP (length is worked out automatically), Treatment ID (must be a treatment defined in Config), Program year, Estimated cost, Actual cost, Funding source and B/C ratio.
- Statuses **planned, designed, awarded and in_progress** count as committed work in new runs. **CLOSED** projects are past work.

> This page is PMS's own editable list. For WVDOT's official program straight from TheHub, use [Committed Projects](#6-committed-projects-live-from-thehub).

### 5a. Project page

Rows that share a Hub ID are one Hub project, so the project page shows the **whole Hub project**: all its route segments and every 0.1-mi analysis segment they cover. The **project segment page** (`/projects/<id>/segment`) shows the same tabs for **one route segment**: its title is the route and milepoints, with a link to the project; its Segments tab is called **Analysis segments** and lists its 0.1-mi segments; and Hub costs are shown as its share of the project by length.

**Only a current project gets a "with treatment" outlook.** A project that is **CLOSED** or was built before 2025 is already in the surveyed condition, so its Condition tab (on both pages) starts from today's condition and shows only how it deteriorates from here: there is no Treatment picker and no With / Do nothing switch, and a note says why.

- **Header:** status, treatment, construction year, Hub number and SPN, with **Edit**, **Committed Projects** (when the Hub project is in that list) and **Hide map / Show map**. The tiles show length, current condition (average CCI, and the % Good / % Poor of its lane-miles), **expected cost** (Hub construction estimate), **actual cost** (OASIS spending, all phases) and the completion date.
- **Map (right third):** every analysis segment coloured by its MAP-21 rating today (Good / Fair / Poor), with the full project extent as a grey outline. Hover a segment for its milepoints, CCI and rating; click it to open the segment page. **Hide map** gives the tabs the full width (kept in the address bar as `?map=0`).
- **Overview:** a **condition strip** per route segment — one block per 0.1 mi, coloured by its MAP-21 rating and drawn to the same miles scale. Hovering a block highlights it on the map; clicking opens it. Below: the treatment (unit cost, life, interval), location and traffic, and the route segments with lane-miles and model cost.
- **Condition:** how the project's condition is expected to change over the next 20 years, doing nothing vs applying a treatment now (the project's treatment by default; pick another with **Treatment**).
  - **Project average** (the default view): one chart per raw measure (IRI, rut depth, cracking, faulting) first, then per index, showing the project's length-weighted average, dashed orange for doing nothing and solid blue with the treatment, plus a sentence giving when most of its lane-miles are rated Poor in each case. The raw-measure charts are shaded with their MAP-21 Good / Fair / Poor ranges. Below, **Share of lane-miles Good / Fair / Poor (MAP-21) by year** shows one stacked bar per year for each scenario; hover a bar for the percentages.
  - **Segment grid** (project segment pages, and project pages with a single route segment): every analysis segment (rows) by year (columns), each cell showing the index value and coloured by that segment's MAP-21 rating in that year. For a current project, switch **With *treatment* / Do nothing** and pick the **Index** (CCI, PSI, RDI, SCI, or CSI / JCI for concrete). The last column is years until the segment is rated Poor. Hovering a row highlights the segment on the map; clicking opens its segment page. Values are truncated to one decimal so they always match their colour.
- **Segments** (project page): the project's route segments — route, milepoints, miles, lane-miles, average CCI with the rating covering most of its lane-miles, number of 0.1-mi segments and model cost. **Hovering** a row draws that whole route segment on the map as one continuous yellow line and zooms the map to it; moving off the table zooms back out to the whole project. Hovering a segment on the map highlights its route segment's row (without zooming). Click a row to open its project segment page. The route segments table on Overview works the same way.
- **Analysis segments** (project segment page): a table of the 0.1-mi analysis segments (CCI with its MAP-21 rating, the main sub-indices, the raw measures — IRI, rut depth, cracking and faulting, each shaded Good / Fair / Poor on the configuration's MAP-21 profile, and only those that rate the segment's pavement — and AADT). Hovering a row highlights the segment on the map in yellow; clicking opens the segment page.
- **Costs:** expected vs actual side by side — the Hub construction estimate, the PMS model estimate (what a run would charge for the treatment on the project's segments, in construction-year and start-year dollars), OASIS construction spending and all-phase spending — plus actual cost per lane-mile, the construction-vs-estimate variance, spending by phase, and each route segment's share (split by length).
- **Hub:** the live TheHub record (scope, milestones, contractor, phases). Projects outside the Committed Projects pavement list are looked up directly; if the Hub is unreachable you'll see a notice instead.

### 5b. Segment page

Opened from a project (or by address `/segments/<id>`), for one 0.1-mi analysis segment.

- **Header:** route and milepoints, pavement type, deterioration family, district, county and NHS, with tiles for **CCI now** (with today's MAP-21 rating), **PSI** (with IRI), the two other main sub-indices (with rut depth and cracking) and **years to Poor** doing nothing vs with the treatment.
- **Deterioration outlook:** 20 years ahead on the segment's dTIMS curves: one chart per index (CCI, PSI, and RDI, SCI & ECI for asphalt or CSI & JCI for concrete) and one per raw measure (IRI, cracking, and rut depth for asphalt or faulting for concrete). The **dashed orange** line is doing nothing; the **solid blue** line applies the treatment now; **dark dots** are measured survey values. The raw-measure charts are shaded with their MAP-21 Good / Fair / Poor ranges; the index charts have no bands. The sentence above the charts gives the years until the segment is rated Poor in each case. Pick a different **Treatment** to compare. The default is the project's treatment only when that project is current (not closed, built 2025 or later), else a committed treatment on the segment, else none.
- **Cost:** what the chosen treatment costs on this segment today (miles × lanes × $/lane-mile) and in each of the next five years with 2% inflation, plus the segment's length share of its project's Hub estimate and OASIS actual.
- **Segment** facts (functional class, AADT and trucks, joint, rehab type, faulting) and **Projects on this segment** — click one to open it.
- The **map** zooms to the segment within its project; click a neighbouring segment to move to it.

## 6. Committed Projects (live from TheHub)

In the menu under **Documents → Extras**. A read-only view of WVDOT's **pavement** projects, read live from TheHub and drawn on a map.

**Top bar**

- **Active / Completed / All**. *Active* means the construction phase is still open. *Completed* means construction is finished.
- **Search** by name, project number, route or county. You can also filter by **District**, **County** and **Year**.
- The ⟳ icon next to the "live from TheHub" time re-reads the Hub. Results are otherwise kept for about five minutes.

**Summary figures**

- Projects, route miles, construction (CN) estimate and spending to date (from OASIS, all phases).
- **Next letting**, or **Latest completion** when viewing Completed.
- **Projects by year** chart: letting year for active projects, completion year for completed ones. Hover over a bar for its totals. **Click a bar** to filter to that year, and click it again to clear.

**List and map**

- Each project in the list shows its route, miles and project number, plus the letting or completion date. Active projects are **blue** and completed ones **green**.
- Click a project in the list or on the map to select it. The map zooms to it and highlights it in **yellow**.
- Hover over a line on the map for a quick summary. **Light / Streets / Satellite** switches the basemap.
- A note at the top of the map says if any segments couldn't be placed on the roads2 LRS.

**Project detail panel**

- Status, project number and SPN, and the scope (**Show more** to expand it).
- Treatment, length, district and county, program, work code and contractor.
- **Construction milestones**: Let → Award → Start → Complete. A filled dot is an actual date. An amber outline means the planned date has passed. Italic dates are planned dates.
- **Cost**: CN estimate vs spent to date.
- **Route segments** with milepoints and miles (segments not on the LRS are flagged), and the project's **Phases** with budget and spending.
- Close the panel with ×.

**If you see "TheHub isn't reachable"**: the Hub is reached through a secure tunnel. The page checks again every 30 seconds; **Retry** checks immediately. In local development, rerun `./start-dev.sh`.

The address bar keeps the stage, filters and selected project, so you can share an exact view.

## 7. Config

A **config** is a complete set of settings a run can use: treatments (with their gates and costs), trigger branches, reset steps, treatment sequencing, family curves, family rules, budget scenarios and a few model constants (benefit traffic weight, discount rate, inflation). There can be several; each run records which one it used.

**Config** in the menu opens the **Configs** list:

- Each row shows the name, comments, who created it and when, when it was last changed and by whom, and how many runs used it. **System default** marks the config new users start with; **Your default** marks yours.
- **Click a row** to open that config.
- The star makes a config **your default**: the Analysis Segments page and the project and segment pages show families, pavement type, CCI and outlooks from your default, and new runs start with it selected. A small **Config:** chip on those pages says which config you're looking at.
- Admins: **New config** copies the system default; the copy icon copies any config (name and comments). Copying takes a few seconds and copies every table and the config's segment families; runs are not copied. The globe makes a config the **system default** (used by everyone who hasn't picked their own). The bin deletes a config; if runs used it, they are listed and deleted with it after you confirm (deleting is the only change that deletes runs). The system default can't be deleted, so make another config the system default first. Anyone who had a deleted config as their default goes back to the system default.

A config page shows the config's name at the top, with **Export to Excel** and **Import from Excel** top right, and seven tabs:

- **Overview** (opens first): System default / Your default (click **Make my default** to switch), **Rename** (admins), the comments, who created it and when, when it was last changed and by whom, a notice if runs used it (they keep the version they were made with), and counts (runs, active treatments, family rules, budget scenarios, users with it as their default).
- **Runs**: every run made with this config, newest first, with status, optimizer, years, total cost, final % Good and when it was created. Click a row to open the run.
- **Treatments**: every active treatment with its type, cost per lane-mile (asphalt / concrete; "×" when a route group pays a multiplier — hover for all three pavement rates and the multipliers), life, pavement type, **Gates** (minimum length and any per-branch override, "only IM_FUNDS" / "not INTERSTATE" route groups, ADT and lane limits, counter limits, years since another treatment, a MAP-21 class ("MAP-21 Fair"), survey IRI, patching and inventory ADT limits, committed only, years before it can repeat), and for each condition index (PSI, RDI, SCI, ECI, JCI, CSI, CCI) the trigger range (Min / Max) and what the treatment does to it (Reset: "= x" set to, "+x" add, "≥ x" at least, "min−x" the lowest index less x, "Hold ny"). Hover **Reset steps** for every step in order, including the IRI, cracking, rutting and faulting resets and the family change. A ⚠ on a branch means it can never trigger: it tests an index that doesn't apply to that pavement (crack seal and preservation on asphalt test CSI, which asphalt carries at 0 — as in dTIMS).
- **Policy**: the config check (green when runs can use the config; red with every problem a run would refuse, such as a family a treatment can move a road into without a usable curve), the model constants and input policy (start year, default lanes, **joints shorter than which the minimum length is skipped** (0.5 mi: a joint under half a mile can get any treatment its condition triggers, whatever the treatment's minimum), starting-age rules, how much of a segment a past project must cover, traffic-growth sources, which cracking measure, **what to do with road that has no survey data** (leave it out of runs, or include it starting as dTIMS does: rated Good until its cracking grows past 5 %), **which survey network** the config reads (conflated: the survey placed by GPS; raw: the vendor's records as delivered — both are kept, so switching is instant), **how road starts** (each 0.1-mi segment from its own survey, or each joint from its survey's length-weighted average, spread over the whole joint the way dTIMS starts a section), ADT exponent, discount, inflation), the **route groups** (named sets of roads such as `INTERSTATE`, `IM_FUNDS` — Interstates except the Turnpike — or `HPMS_1`) with what each is defined as, cost adjustments, cracking rules, treatment counters, the condition initializers, the Good / Fair / Poor profile, and the config's **versions** with how many runs used each.
- **Pavement Families**: the deterioration curve parameters for each family (surface type and traffic level) and each index. Hover over a value to see the curve type.
  - Hover a **family name** for its definition: pavement type, rehab type and truck load, its CCI formula, which of this config's family rules starts segments in it, which treatments move a segment into it, and whether the rules use it at all.
- **Family Rules**: the rules that decide which pavement family (and so which pavement type and deterioration curves) each road segment starts in, in this config.
  - Rules are checked top to bottom, and the first enabled rule whose conditions match wins. The shipped rules take pavement type from the surface type (concrete, other/unknown, otherwise asphalt) and make a segment **high truck** when it is on a coal route or trucks are at least 10% of its AADT.
  - Each rule shows how many segments and miles it assigns (first match), with a total. While editing, the counts update a moment after each change, before anything is saved, along with how many segments would change family.
  - When editing (see below), each rule has a family, **all of / any of**, conditions and an on/off switch; the arrows reorder rules. A condition tests one field (surface type, coal route, truck share, AADT, district, …); **Add group** adds a set of tests of which any (or all) must hold, e.g. *concrete and (coal route or trucks ≥ 10%)*. A rule with no conditions catches every segment that reaches it, so keep one last. **Save and reclassify segments** stores the rules and recomputes family, CCI and ages for this config only (a few seconds). **Load shipped rules** puts back the standard rules.
- **Budget Scenarios**: saved budget setups you can load into a run that uses this config.
  - Admins: **New scenario** or **Edit** opens a form: name, description, base annual budget, analysis years, per-year budgets, carryover and optional district balancing. **Archive** hides a scenario straight away; **Show archived** and **Restore** bring it back.

**Editing a config (admins).**

- **Edit rules…** on the Family Rules tab turns on the rules editor; **Done editing** turns it off. Treatments, triggers, reset steps, costs, sequencing, curves, route groups, cracking rules, counters, initializers and model constants are edited through Excel (below). Budget scenarios can be edited any time.
- **Editing never deletes runs.** Each run keeps the **version** of the config it was made with (Policy → Versions), so its results, Validate and Excel export don't change; new runs use the new version. The only thing that blocks an edit is a run still running on the config.
- Budget scenario changes never affect runs either: a run keeps its own copy of the budgets it started with.

### Export and import with Excel
### Export and import with Excel

**Export to Excel** (a config's Overview tab) downloads that config as one workbook: a README sheet, then Treatments, Trigger Branches, Reset Operations, Treatment Costs, Cost Adjustments, Treatment Sequencing, Family Curves, Budget Scenarios, Scenario Budgets (per-year budgets), District Balancing, Family Rules, Model Constants, Route Groups, Route Group Terms, Cracking Rules, Counters, Condition Initializers and Hub Treatment Map. Files exported before v1.7 can't be imported; export a new one.

- **Blue headers** are editable; **grey headers** are read-only (keys, values derived from the family id, and reference columns). Family rule conditions are written as JSON, e.g. `[{"field": "surface_type", "op": "in", "value": ["JCP"]}]`; `[]` matches every segment. Hover a header for what it holds and the allowed values; choice and TRUE/FALSE columns have drop-downs.
- What each sheet allows is listed on the README sheet. In short: edit any blue cell; add rows on Treatments, Trigger Branches, Reset Operations, Treatment Costs, Cost Adjustments, Treatment Sequencing, Scenario Budgets, District Balancing, Family Rules, Route Groups, Route Group Terms, Cracking Rules, Counters and Hub Treatment Map; delete rows on all of those except Treatments. Trigger Branches has optional **gfp_class** (G / F / P), **inv_iri_above**, **patch_pct_min** and **adt_min** columns for branches that test the MAP-21 class or inventory values. Route group terms take a JSON value, e.g. `"1"`, `117.93`, `["1","2"]`, `[1, 3]` for *between*, or a group key for *in_group*. The check also warns about trigger branches that can never trigger. Treatments can't be deleted (set **active** to FALSE); family curves can't be added or removed; new budget scenarios are made on the Budget Scenarios tab.
- Don't rename sheets or headers, and don't change the key of an existing row (that reads as one row removed and a new one added).

**Import from Excel** takes an edited copy to that config's import page, which **checks every row against this config before anything changes** (a file exported from another config can be imported; a warning says so):

- If there are problems, a red banner says nothing will be changed, and **Rows with problems** lists each one: sheet, Excel row number, key, column and what is wrong (for example *Expected a number*, *PSI lower bound 4.9 is above the upper bound 1*, *Treatment X is not on the Treatments sheet*, *Read-only column*). Click a line to jump to that row.
- Below, one tab per sheet shows the rows. Rows with problems are **red with a red bar**, and the cell at fault is **outlined in red** (hover it for the message). Changed cells are **yellow** and show the old value crossed out before the new one; added and removed rows are marked. **Changes and problems** / **All rows** switches between just those rows and the whole sheet.
- Fix the file in Excel and use **Upload another file** (or **Check again**).
- After the row checks, the whole config the file describes is checked exactly as a run would check it (the Policy tab's config check); anything a run would refuse is listed as a problem.
- When there are no problems, **Apply N changes** (admins) opens a summary of what changes per sheet; **Apply changes** writes it all at once. If curves, rules, reset steps or any of the starting-state policy change, the config's segment families and starting condition are recomputed as part of it (about 20 seconds). Runs that used the config are listed; they keep the version they were made with.
- If someone changed the configuration after your file was exported, a yellow warning says so: any row shown as changed that you didn't edit would undo their change, so re-export when in doubt. If the configuration changes between your check and your apply, the apply is refused and you check again.
- New runs with this config use the changes.

## 8. Analysis Segments

Browse the analysis segments that runs are built from, with each segment's current condition. The header shows which config's families and condition you're seeing (and the selected route, if any); the row count is at the bottom of the table.

- Type a route in **Route ID** to filter to it; press Enter when only one route matches. **Clear** resets the filter and sorting.
- Click a column header to sort.
- The first three columns (Route ID, BMP, EMP) stay in place when you scroll sideways.
- **IRI, Rut** and **Crack** are coloured Good / Fair / Poor with the MAP-21 thresholds; hover over a cell for them. The coloured index columns show PSI through CCI.
- The last columns show whether a segment is covered by a committed project, and by which treatment, in which year.
- Choose 25, 50, 100 or 200 rows per page at the bottom.

## 9. Multi-Year Analysis

Year-by-year condition (2020–2025) for one route: useful for spotting deterioration and past work.

- **Search routes** and pick a route. The address bar keeps it (`?route=`).
- **Indices** shows or hides the condition index columns.
- **LRS / Raw** switches between the conflated data (LRS) and the raw survey data. **Cmd/Ctrl + M** also switches.
- Each measure has one column per year plus a trend line (green improving, red worsening). Cells are coloured Good / Fair / Poor.
- A small blue corner on a cell means there was a project on that segment that year. **Click the cell** to see the project: status, name, route and milepoints, treatment and cost.

## 10. Detected Projects

In the menu under **Documents → Extras** (formerly Potential Projects). Stretches of road where the survey data jumped sharply better from one year to the next, which usually means paving that isn't recorded as a project. Use it to find missing past projects.

- Pick a detected project from **Select a detected project…**. The list is sorted by score, highest first, and each entry shows the year, route, milepoints, number of segments, length, IRI before → after and the score.
- The grid shows the whole route. **Rows inside the detected span are tinted purple**, and **purple outlines** mark the before/after cells that triggered the detection. You may need to scroll to find the purple rows.
- **Indices**, **LRS / Raw** and clicking project cells work as on Multi-Year Analysis.

## 11. Documents and Changelog

- **Documents** pages show a path at the top (Documentation › page › section). It follows you as you scroll, and each part is clickable. Links inside a page jump to that section; links to other sites open in a new tab.
- The **Changelog** lists what changed, newest first. **Summary** is a plain-language list for each day; **Detailed** is the technical record for each version. The current frontend and backend versions are shown at the top.

## 12. Tips and known quirks

- **Three kinds of "committed projects"**:
  - The **Projects** page is PMS's editable list (click a row for the project page).
  - **Committed Projects** is WVDOT's live program from TheHub.
  - A run's **Committed Projects** tab shows the projects locked into that run.
- The Multi-Year Analysis and Detected Projects grids may show a "missing license" watermark. It doesn't affect the data.
- Rut and cracking colour thresholds differ slightly between the Analysis Segments page and Multi-Year Analysis.
- On the Projects page, the **Year** column shows the construction year, but the form edits the program year.
- On Config, the selected tab isn't kept in the address bar, so a link to Budget Scenarios opens on Treatments.

## 13. Profile and Users

**System → Profile** (also in your avatar menu) shows your name, email, role and districts (with their counties), your default config, and when you first and last signed in. Pick your **avatar colour** there: one of the swatches, or **Custom** for any colour; **Reset to default** goes back to grey. The colour is used for your initials in the app bar, on Users, and on the Validate page, where the people viewing a run with you appear as avatars.

**System → Users** (admins only) lists everyone who has signed in, with their avatars. **Admin** users can see and change everything and review proposals. A **District** user sees and proposes changes only for the districts ticked for them (hover D1–D10 for the counties). Tick a district on an admin to make them a district user for that district. You can't change your own role. Everyone who signs in for the first time is an admin.

## 14. Data refresh (administrators)

The pavement condition, LRS attributes and joints behind every screen are refreshed outside the app, from the command line, with one command. See [Data Pipeline](/docs/PMS_Data_Pipeline) for the steps, the checks and how to back up and restore. After a refresh:

- Runs made earlier still open and validate. Their joints are mapped onto the new joints automatically.
- Segment lengths are the real milepoint span, so network miles and costs are more accurate than before v1.4.0.
- The inputs of the dTIMS model are refreshed with it: route class, the vendor's CCI, traffic growth and each road's last rehab (from the CLOSED projects). After loading new CLOSED projects on their own, run `python -m pipeline inputs families` so roads start from their new rehab years.

Other systems can turn GPS points into route milepoints with the [LRS API](/docs/PMS_LRS_API), which needs a service token.

