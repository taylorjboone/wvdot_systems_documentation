# AMPS — Asset Management & Performance System

**One place to see the condition of West Virginia's roads and bridges, plan the work that keeps them in service, and turn that plan into the program.** AMPS is built for WVDOT's Asset Management & Performance division.

## What it's for

WVDOT has to decide every year which pavements and bridges to treat, with what and when, within budgets that never cover everything. AMPS answers the questions behind those decisions:

- **Where are we now?** The current condition of every road section and every structure, from the latest pavement survey and bridge inspections.
- **Where are we heading?** How that condition changes over time if nothing is done, and with each possible treatment.
- **What should we do, and when?** A multi-year work plan: the treatments that give the most condition benefit per dollar within each year's budget, with committed projects forced in first.
- **What does it buy us?** The network's Good / Fair / Poor shares year by year, for the plan against doing nothing, and whether the performance targets are met.
- **Do we agree?** Districts and the central office review the plan together, adjust it, and commit the result to the program.

## What's inside

The folders are in the blue bar at the top, in this order.

| Folder | Covers | What you do there |
|---|---|---|
| **PMS** | Pavement, about 24,000 miles in 265,590 tenth-mile segments, grouped into 22,480 project sections | Configure treatments and deterioration (the dTIMS model), run multi-year optimizations, validate and commit the plan, look at any road section's history and outlook |
| **BMS** | Bridge planning for the 7,106 in-service bridges WVDOT owns | The same workflow for bridges: LISA priority scores, deterioration by bridge family, bridge treatments and budgets, plan runs, validation, committed projects |
| **Bridges** | The bridge inventory: 8,719 structures and 67,453 inspection reports | Find any bridge and see everything known about it: condition, inspections, rating history, elements, TheHub projects, MMS maintenance, traffic, load rating, flood exposure |
| **Brgzrd** | The Bridge Wizard | Ask questions about bridges in plain English and get answers built from the data, with the working shown |
| **Documents** | Guides and references | How to use each screen, how every number is calculated, the data pipeline and the bridge analysis reports |
| **System** | Your account | Your profile and, for admins, who can see and change what |

## Bridges

Bridges is the record of every structure in the state, not just the ones in a plan. It comes from **AssetWise**, WVDOT's bridge inspection system, which is refreshed into AMPS as a read-only copy: AMPS never changes an inspection. Of the 8,719 structures, 7,261 are owned by WVDOT and 7,106 of those are in service, with about 40 million square feet of deck. Unless a page says otherwise, bridge figures are for WVDOT-owned bridges.

**How condition is measured.** Inspectors rate the deck, superstructure and substructure (or the culvert), plus the channel and scour, on the NBI scale of 0 to 9. A bridge is **Good** when its lowest rating is 7 or more, **Fair** at 5–6 and **Poor** at 4 or less. Since 2023–24, inspections have moved to the new federal SNBI forms, which record the same ratings under different fields; AMPS reads both so the history is continuous. Inspectors also rate each element (joints, bearings, girders and so on) by condition state 1–4.

**The bridge list** (`/bridges`) finds bridges by BARS number, name, route or county, with suggestions as you type. Filter by district, bridge type, spans, Good / Fair / Poor for each component, inspection timing or spend, and open the map to see them in place. Totals of TheHub construction and MMS maintenance spend on each bridge are refreshed every night.

**A bridge's page** puts everything about one structure in tabs:

| Tab | Shows |
|---|---|
| Overview | Where it is on the map, what it is (type, spans, length, deck area, year built), and truck traffic and load rating over time |
| Inspections | Every inspection, newest first, with the inspectors' written findings; open one for the full report, photos and attachments |
| NBI history | Each component's rating at every inspection on record, with TheHub construction shaded in, so you can see what the work did |
| Elements | The condition of each element at the chosen inspection |
| TheHub projects | Construction projects on the bridge, with their dates, contract and change orders and this bridge's share of the cost |
| MMS work | Maintenance crews' tasks on the bridge, with the work done, hours and cost |
| 3D terrain & floods | The bridge in 3D terrain with modelled flood depths |

**Money is shared fairly.** A TheHub project often covers several bridges. Its cost is split among them by deck area, so a bridge is only charged its share, and bridge totals add up to the program's total.

The **bridge analysis reports** in Documents › Bridges go further: how each bridge family deteriorates by district and age, what drives deterioration (trucks, load rating, weather) and what each treatment type does to the ratings.

## Brgzrd — the Bridge Wizard

Brgzrd (say "bridge wizard") answers questions about bridges in plain English: *which district has the most Poor decks under 40 years old?*, *how did ratings change after deck overlays?*, *what did we spend on scour work in District 7?* It has its own link in the top bar.

It works like an analyst who can see all the data. For each question it writes and runs its own queries, looks at the results and keeps going until it can answer. It can reach:

- the whole inspection record: every bridge, inspection, rating and element;
- TheHub construction projects and MMS maintenance work and cost, including read-only queries of its own;
- truck traffic and load rating history, and historic weather (freeze-thaw cycles, rain, snow, temperature) at every bridge;
- a sealed Python workspace for statistics and charts.

**Every answer shows its working.** The steps it took, with each query and its results, are listed beside the answer and fold away when it's done. Answers can include charts and downloadable spreadsheets or reports. Each answer and each conversation has a link you can send to colleagues; they need to be signed in to open it.

**What it isn't.** Brgzrd only reads. It can't change an inspection, a plan or a project, and it's not an official record. Like any analyst it can misread a question, so check the working behind any figure you plan to rely on. By default it leaves out bridges that aren't WVDOT's, archived bridges and components that weren't rated; ask if you want them in.

## BMS / PMS: how a plan gets made

PMS and BMS follow the same yearly cycle. Only what's measured differs: pavement is rated on its distress (roughness, rutting, cracking) by lane-mile, and bridges on NBI ratings by deck area.

```
                         +-------------------------------+
                         | 1. DATA                       |
                         | pavement survey, LRS,         |
         +-------------->| AssetWise inspections,        |
         |               | TheHub program, MMS work      |
         |               +--------------+----------------+
         |                              |
         |                              v
+--------+-----------+   +-------------------------------+
| 6. DELIVER         |   | 2. CONFIGURE                  |
| TheHub lets and    |   | treatments, when each fits,   |
| builds the work;   |   | what it does, what it costs;  |
| MMS logs upkeep    |   | deterioration; budgets        |
+--------------------+   +--------------+----------------+
         ^                              |
         |                              v
+--------+-----------+   +-------------------------------+
| 5. COMMIT          |   | 3. RUN                        |
| validated work     |   | project every asset year by   |
| becomes committed  |   | year; pick the most benefit   |
| projects, fixed in |   | per dollar within each        |
| every later run    |   | year's budget                 |
+--------------------+   +--------------+----------------+
         ^                              |
         |                              v
         |               +-------------------------------+
         |               | 4. VALIDATE                   |<--+
         +---------------+ districts and central office  |   | move, add,
                         | review the plan together,     |   | change, drop,
                         | live; every edit logged       +---+ approve
                         +-------------------------------+
```

1. **Data.** The pavement survey, the road network (LRS), bridge inspections from AssetWise, projects from TheHub and maintenance from MMS are loaded and checked.
2. **Configure.** The rules come from dTIMS for pavement and, for bridges, either WVDOT's dTIMS bridge model or the AMPS bridge planner built from the WVDOT BMS notes. They are kept as editable configuration, which can also be edited as an Excel workbook, and say which treatments exist, when each fits, what it does to condition and what it costs.
3. **Run.** The optimizer projects every asset year by year and picks the work that gives the most benefit within each year's budget and scope. Committed projects are always included.
4. **Validate.** The plan appears as cards in one lane per year. People move, add, change or remove work; every change is logged with who and why, everyone sees it live, and district users' changes wait for an admin's approval.
5. **Commit.** Validated work becomes committed projects, which every later run treats as fixed.
6. **Deliver.** TheHub lets and builds the program, and MMS records the maintenance. Both come back in as data, so the next cycle starts from what is really happening.

### Why validation is in AMPS

Validation used to be a series of meetings with each district and spreadsheets passed back and forth between the central office, the vendors who ran the models, district stakeholders and executive administration:

```
   AM&P central office             vendors                   districts 1-10
   -------------------             -------                   --------------
   export inventory   ---- xlsx --> run the model,
                                    build the plan
   plan workbook      <--- xlsx ---
   split by district  ---------------- xlsx ---------------> mark up rows,
                                                             comment by email
   meetings, one      <--------------- xlsx ---------------- send back
   district at a time
   merge the markups,
   ask for a re-run   ---- xlsx --> re-run
                        ... and round again ...
   final workbook     ---- xlsx --> executive administration: sign-off
```

Each round took weeks. Copies drifted apart, a change made in one meeting could be lost in the next merge, and nobody could say afterwards who changed what, or why. Nor could anyone see what a change did to the network's condition until the vendor re-ran the model.

AMPS keeps one plan that everyone works on at the same time. Districts see their own projects and propose changes. The central office approves them. Every edit is recorded with its author and reason, and none is ever erased: an undo is a new, logged change. The effect on cost and condition shows as soon as a change is made, and executive administration can look at the same plan instead of a final workbook. The meetings still happen, but around the live plan rather than a file.

## Principles

- **One model per asset, used everywhere.** Pavement condition moves only through the dTIMS model, and bridge condition only through NBI ratings (0–9), moved by the bridge configuration's model (dTIMS's years at each rating, or AMPS's Markov deterioration). Runs, validation and every outlook use the same model, so the numbers agree from page to page.
- **One price.** Every cost goes through a single pricing function per asset type, so plans, validation and project pages always quote the same figure.
- **Reproducible.** A run records the configuration and data it used, so its results and its Validate page don't change later.
- **Accountable.** Plan changes and configuration imports are logged and never silently overwritten; an undo is a new, logged change.
- **Scoped.** Everyone signs in with their WVDOT account. District users work on their own districts' projects and propose changes; admins approve them, configure the rules and manage users.

## Where to start

| If you want to… | Open |
|---|---|
| Learn the pavement screens | [PMS Usage Guide](/docs/PMS_Usage) |
| Learn the bridge screens | [Bridges & BMS Usage Guide](/docs/BMS_Usage) |
| Understand how the numbers are calculated | [PMS Business Logic](/docs/PMS_Business_Logic) · [BMS Business Logic](/docs/BMS_Business_Logic) |
| Look up a bridge | Bridges |
| Ask a question about bridges | Brgzrd · how it works: [Bridge Wizard Logic](/docs/Bridge_Wizard_Logic) |
| See the latest plans | PMS → Runs · BMS → Runs |
| See what changed recently | [Changelog](/changelog) |
