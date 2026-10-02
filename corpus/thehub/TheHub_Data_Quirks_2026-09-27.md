# TheHub Data Quirks: Bridge and Pavement Projects

*27 September 2026. A read-only audit of TheHub (SQL Server) as AMPS reads it, with the pavement project segments checked against LRS layer 70.*

It started with **Laurel Creek Girder** (Mingo County):
- **Two project records for one job.** 2014000025 is the state-funded engineering, right-of-way and construction ($2.10M). 2020001593 is a federal-aid add-on for construction only ($347K).
- **Both linked to the wrong bridge.** They point at the neighbouring bridge 30A012 (1995, 73.5 ft, never touched). The structure actually replaced was 30A013, the 104 ft girder named in the scope. Its replacement is 30A294, built in 2020.
- **The cost looks like an overrun but isn't.** $1.55M programmed against $2.10M spent compares construction with all phases.

This document looks for the same patterns across TheHub.

## Summary

| # | Quirk | Where | How much | What AMPS shows |
|---|---|---|---|---|
| 1 | Replacement linked to the neighbouring bridge | Bridges | 13 projects, $16.9M (+31 linked to a bridge with no sign of work, $25.2M) | Cost and construction bands on the wrong bridge; the real new bridge shows nothing |
| 2 | Replacement linked to the retired BARS only | Bridges | 121 of 270 completed replacements, $234.6M | The new bridge has no TheHub history or cost |
| 3 | Project name matches nothing about its bridge | Bridges | 150 of 1,734 single-bridge projects (8.7%) | Some are memorial renames; others are wrong links |
| 4 | One job split across several records | Both | 77 records on 34 shared stems; 106 jobs split S2/S3/S6; 152 bridge + name groups | Money isn't double counted, but project counts and bands are |
| 5 | "Complete" engineering-only records | Bridges | 110 closed records with no construction phase, $51.8M | Shown as completed work |
| 6 | Programmed (construction) vs spent (all phases) | Bridges | 189 of 769 completed look over budget; 0 are on a construction basis | False overruns on project cards |
| 7 | Completion dates missing or estimated | Both | 60% of complete bridge and 58% of pavement projects have no COMPLETE CONST date | Paving year about 1 year late; bulk fiscal dates |
| 8 | Bridge-coded projects with no bridge | Bridges | 358 projects, $839.3M | Invisible on every bridge |
| 9 | Pavement projects outside AMPS's paving filter | Pavement | 855 Major HMA overlay (code 68) + 165 ultra-thin (67) projects | Missing from TheHub pavement list |
| 10 | Paved in TheHub, gravel on the LRS | Pavement | 147.6 mi under 200 projects | Never surveyed, so absent from PMS runs |
| 11 | Route IDs and milepoints layer 70 doesn't know | Pavement | 45 mi; 8 malformed route IDs | Segments can't be placed or rated |
| 12 | Overlapping projects | Pavement | 138 pairs within a year, 347 mi | Double work on the same road |
| 13 | Spend with no project | Both | 2,691 program codes, $1.86B (mostly 1998–2020) | Never seen |
| 14 | Converted records | Both | 6,123 records created 2021-10-18 | Scope text only, "see project file" |

**Method.** AMPS reads two sets of projects from TheHub:
- **Bridge projects:** the 2,280 matched by `bms/hub.py` `BRIDGE_CTE`, compared with the AssetWise extract (`qv_bridge_list`, `qv_nbi_timeseries`).
- **Pavement projects:** the 2,780 projects and 3,975 route segments matched by `api/hub_sql.py` `PAVING_CTE`, compared with LRS layer 70 (downloaded 2026-09-27) and the survey tables.

Everything was read-only. The scripts are in `scripts/hub_audit/`:
- `pavement_surface_check.py` does the layer 70 check.
- `thehub/` holds the rest: `fetch.py` pulls TheHub once into a local cache, and the `q*.py` scripts run the checks. Run them from the repo root.

---

## Bridges

### 1. Replacements linked to the neighbouring bridge

**The pattern.** A replacement project's TheHub bridge link points at another bridge nearby, on the same road or creek. That bridge is still in service and its ratings don't move, while a new BARS appears within 0.5 mi during the job.

**Size.** 13 projects, $16.9M. Another 31 projects ($25.2M) are linked to an in-service bridge that shows no sign of work, several with plainly different names.

| Project | Name | Linked BARS | Actual new bridge |
|---|---|---|---|
| 2014000025, 2020001593 | Laurel Creek Girder | 30A012 Alleen Ledson Memorial | 30A294 (old: 30A013) |
| 2018000102 | Tariff Bridge | 44A147 | 44A195 |
| 2018000066 | Capehart Bridge ($1.8M) | 27A192 | 27A198 |
| 2017001258 | Tague Br +1 ($2.7M) | 04A043 | 04A198 |
| 2011000735 | Anawalt Br #2 | 24A243 | 24A382 |

Examples of links with no sign of work:
- Tanner Creek Girder Br → 11A016 Pennzoil Box Beam.
- Spring Fork Culvert → 30A136 Little Buddy Bridge.
- Huff Creek Bridge #4 → 55A021 Steeles Bridge. That bridge also carries its own project, Steeles Bridge 2019000910.

**In AMPS.** Every per-bridge TheHub figure uses the link: the bridge list's spend, the bridge page's projects and NBI construction bands, BMS costs and Brgzrd. So the wrong bridge carries the money (30A012 shows $2.45M) and the real new one shows none.

### 2. Replacements linked to the retired BARS only

**The pattern.** 121 of 270 completed replacements (45%, $234.6M) are linked to the bridge they replaced, which is now archived in AssetWise. That is a fair link for TheHub, since the project replaced that asset. But nothing connects the job to the successor BARS, which we could identify for 113 of them.

| Project | Name | Linked (archived) | Successor |
|---|---|---|---|
| 2016000961 | Clifford Family Memorial Br ($7.0M) | 13A118 | 13A282 |
| 2016000978 | Sandy Creek Deck Girder ($2.9M) | 01A003 | 01A126 |
| 2021000016 | Lt Darwin K Kyle Mem Br ($5.4M) | 03A087 | 03A210 |
| 2019001122 | Extra Arch | 40A011 | 40A175 |

**In AMPS.** The new bridge's page has no TheHub history, no construction band and no cost. The bridge list hides archived bridges by default, so this spend effectively disappears.

A related case: 11 projects ($11.3M) keep the same BARS, and the bridge's ratings jump by 2 or more afterwards. These were probably rebuilt, but the year built in AssetWise was never updated.

### 3. Project names that match nothing about the bridge

150 of 1,734 checkable single-bridge projects (8.7%) share no word of their name with the linked bridge's name or the feature it crosses. Many are memorial renames. Others look like wrong links:

| Project name | Linked bridge |
|---|---|
| Loop Creek Br | 10A001 Johnson Fork |
| Lick Branch | 10A197 Rich Creek |
| Erbacon Box Girder | 51A020 Laurel Creek Bxbm |
| Barn Run Road | 34A134 Grassy Run |

The Treatment Effects report found the same rate independently: about 10% of TheHub bridge links fail a name check.

### 5. "Complete" projects that were only engineering

234 bridge records have no construction phase. 110 of them are "Complete and closed", 76 of those coded Replace, $51.8M in all:

| Project | Work | Phases | Spent |
|---|---|---|---|
| Mine Bridge 2021000244 | Replace | Engineering only | $22K |
| Van Metre Ford 2000000317 | Replace | Engineering + right-of-way | $1.44M |
| Ices Ferry #4763 | Replace | Engineering only | $1.15M |
| Old Hi Carpenter Br | Renovate | Engineering only | $1.46M |

**In AMPS.** These count as completed replacements, so they draw a construction band on the NBI chart and a completed project on the bridge, though nothing was built. Pavement has 10 such records, 4 of them complete.

### 6. False overruns: programmed vs spent

- **Programmed cost** is the construction phase only.
- **Actual spent** (`BUD_STRU_PHASE_PROG2`) covers every phase: engineering, right-of-way and construction.

**189 of 769 completed bridge projects look over budget, and none are when construction is compared with construction.** The whole gap is $59.0M of engineering and right-of-way spend. On closed projects, the programmed construction amount has been trued up to the actual construction cost.

| Basis | Spent ÷ programmed |
|---|---|
| Construction vs construction | 0.94 |
| AMPS's mixed basis | 1.03 |

Examples: Dingess Street Br ($12.2M programmed, $15.8M spent, of which engineering $2.6M and right-of-way $1.0M), John Blue Br, Wheeling Suspension Br. Pavement projects show no difference.

### 8. Bridge-coded projects with no bridge

358 bridge-coded projects ($839.3M) have no bridge link, so no bridge page or bridge total sees them. The largest:

| Project | Cost |
|---|---|
| Nitro I/C 2006000303 | $286M |
| Wellsburg Br | $170M |
| Cheat River | $141M |
| Roaring Run | $39M |

**Other link checks:**
- **Links outside scope:** of 3,176 bridge links, 269 go to archived bridges and 346 to bridges WVDOT doesn't own. None point outside the inventory, and TheHub's bridge table (`PrimaryNBIBridge`) is clean.
- **Primary link vs route-segment link:** they disagree in only 1 of 645 cases (Hale Street Bridge: 24A909 vs 24A910).
- **Big bundles:** up to 47 bridges on one project (SFY 24 BKAMPP District 9 LMC). 11 of 721 bundled bridges have no deck area and get the project's average share.

---

## Both

### 4. One job, several records

TheHub splits a job across records in three ways:

| How | Scale | Examples |
|---|---|---|
| **By state project number suffix** (…00, …02) | 34 stems shared by 77 records; 19 of the non-00 records are construction-only federal-aid add-ons | Laurel Creek 26900 / 26902; Kelly Creek Bridge +1 58200 / 58202 |
| **By phase prefix** (S2 engineering, S3 construction, S6) with otherwise identical numbers | 106 jobs, 212 records | Harlan Run 2023020004 (S202) / 2023020005 (S302); Lower Ck Conc Girder 2022060050 (S206, closed) / 2022060053 (S306, let 2028) |
| **By name** | 152 bridge + name groups (303 projects, $119.6M); 76 route + name groups on the pavement side | |

**In AMPS.** Money isn't double counted, because each record carries its own spend. But these are inflated:
- project counts;
- the "projects on this bridge" list, which shows 19 bridges with more projects than jobs;
- NBI construction bands;
- the committed-projects seed.

A job key would fix it: the state project number with the stem and phase digit removed.

### 7. Completion dates

| | Bridges | Pavement |
|---|---|---|
| Complete projects with no COMPLETE CONST milestone | 553 of 918 (60%) | 1,303 of 2,265 (58%) |
| … and no construction end either | 110 | |
| Construction end later than the milestone, where both exist | > 1 yr in 159, > 2 yr in 84 | median **1.09 yr**; > 1 yr in 556, > 2 yr in 142 |
| Estimated completions on a few bulk fiscal dates | 189 on 7 dates | 854 on 24 dates (149 on 2023-06-28) |

**In AMPS.** When the milestone is missing, AMPS uses the construction phase's end date. That date is the financial close-out, a year or more after the paving on average. So:
- a TheHub paving job lands about a year late in AMPS's construction year, its history and the committed seed;
- hundreds share a handful of fiscal dates.

Newer records are no better: 315 of 369 completed bridge projects that aren't conversions also lack the milestone. Other date gaps on bridge projects:
- 547 complete projects have no let date;
- 64 are complete with a phase still open;
- 141 are active more than a year past their expected completion (Evans Br: expected June 2022);
- 100 were let more than 2 years ago with no completion.

### 13. Spend with no project

2,691 program codes in `BUD_STRU_PHASE_PROG2` ($1.86B, mostly 1998–2020) match no TheHub project, so AMPS never sees them:
- **507 are bridge-named ($378M):** Lilly Bridge Replace $33.3M, Keyser–McCoole Bridge Replace $30.3M, Thomas Buford Pugh Mem Br Resurface $20.4M.
- **677 are paving-named ($454M).**

Going the other way, 35 completed bridge projects and 37 completed paving projects show $0 spent.

### 14. Converted records

6,123 TheHub projects were created on 2021-10-18 in the move from the old system. Their right-of-way, utility and environment fields say "CONVERTED PROJECT – see project file". 1,804 of the audited projects are conversions, including both Laurel Creek records. They carry scope text and money but little structure, and most of the missing milestones above are theirs. Most, not all: new records miss them too.

---

## Pavement

### 9. Projects outside AMPS's paving filter

AMPS treats a TheHub project as pavement when either:
- it is in the STIP Resurfacing program; or
- its construction code is one of 07, 08, 09, 13, 14, 15, 75 or 76.

That leaves out codes TheHub itself classes as pavement work:

| Code | Name | Projects (complete) |
|---|---|---|
| 68 | Major HMA overlay 2" and greater | 855 (581) |
| 67 | Ultra-thin HMA overlay < 1" | 165 (126) |
| 26 | Micro surfacing | 37 |
| 59 | High-friction surface treatment | 30 |
| 02, 04, 24 | Reconstruction and widening | |

The committed `projects` table does include many of these: its 608 Thick Overlay rows come from an earlier, broader import. But the live TheHub pavement list doesn't. Of the 973 `projects` rows missing from it:
- 494 are code 68 and 116 are code 67;
- 270 point at `hub_id`s that no longer exist in TheHub.

Widening `PAVING_CODES` is a policy choice. At least 68 and 67 belong in.

**Treatment mapping.** `scripts/import_past_projects.py` maps TheHub construction **names** to treatments, and TheHub has since renamed them:

| The script expects | TheHub now says |
|---|---|
| `Minor HMA O/L 1½"-2"` | `Minor HMA O/L 1" to <2"` |

A re-import today would leave 2,504 of 2,780 projects unmapped. Mapping by construction **code** would be stable. The config-level map (`project_treatment_map`) is empty in the local database.

### 10. Paved in TheHub, gravel on the LRS (layer 70)

#### What was checked

Every route segment of every TheHub pavement project was overlaid on the LRS surface-type layer (layer 70). Pavement projects are the ones AMPS reads (`api/hub_sql.py`): the STIP Resurfacing program, or a paving construction code 07, 08, 09, 13–15, 75 or 76. Terminated and reserve statuses are left out. That is **2,780 projects and 3,975 route segments, 7,532 miles**.

Layer 70 was downloaded fresh from the LRS MapServer on 2026-09-27: 48,046 current records, 40,411 miles. Its surface codes group as follows:

| Group | Codes | Miles |
|---|---|---|
| Paved | 2.1 asphalt, 2.2 chip seal, 3–5 concrete, 6–10 overlays | 29,190 |
| Unpaved | 1.1 unimproved, 1.2 dirt, 1.3 gravel or stone, 99 primitive | 11,217 |
| Other | 11 | 3 |

#### Result

Most of it agrees. **97% of TheHub pavement mileage (7,338 mi) is paved on layer 70.** The exceptions:

| | Segments | Projects | Miles |
|---|---|---|---|
| Mostly unpaved on layer 70 (≥ 50% of the segment) | 110 | 97 | 124.8 (segment length) |
| Partly unpaved | 118 | 111 | 43.1 unpaved of 235.6 |
| &nbsp;&nbsp;of which only a sliver at one end (< 0.25 mi) | 68 | | 6.2 |
| No layer 70 record at all | 41 | | 45.3 |

**147.6 miles of TheHub paving sit on road the LRS calls unpaved.** 133.6 of those miles are 1.3 Gravel or Stone. All of them are county routes, apart from 3 mi of HARP and 0.1 mi of park road. Every district has some:

| District | Projects | Unpaved miles |
|---|---|---|
| 4 | 33 | 26.8 |
| 8 | 17 | 25.2 |
| 2 | 43 | 23.8 |
| 1 | 25 | 21.2 |
| 3 | 16 | 17.9 |
| 10 | 29 | 11.4 |
| 7 | 15 | 9.8 |
| 5 | 10 | 4.5 |
| 9 | 6 | 3.6 |
| 6 | 6 | 3.4 |

#### Most of these are overlays, which only exist on pavement

| Construction code | Segments | Projects | Unpaved miles |
|---|---|---|---|
| 08 Minor HMA overlay 1" to < 2" | 194 | 170 | 128.0 |
| 14 Resurface (surface treatment) | 18 | 15 | 12.6 |
| 07 Pave (HMA or PCC) on existing road | 8 | 8 | 5.7 |
| 09 Skip-pave | 3 | 3 | 0.9 |
| other | 5 | 4 | 0.4 |

Only 5.7 miles are first-time paving (code 07). The other 142 miles are overlays and resurfacing, work that only makes sense on a paved road. So either:
- the road was already paved and **layer 70 is wrong**; or
- a gravel road was paved for the first time and coded as a "minor overlay".

**Either way, once the work is complete the road is paved, and layer 70 should say so.**

#### The LRS isn't updated after paving

- **155 of the projects are complete and closed**, covering 123.7 unpaved miles. The other 45 are active (23.8 mi).
Of the 90 completed segments that are mostly unpaved:
- **83 had their gravel record last re-established on 1–3 April 2024.** That looks like a bulk reload of an older surface inventory.
- **In 60 cases the gravel record is dated after the paving was finished.** The reload wrote gravel back onto roads paved in 2019–2023.
- **In the other 30 the record predates the paving.** The project finished after April 2024 and was never posted.
- The median project was finished 3.2 years ago.

Corrections are happening, slowly. Since the February 2026 export, the unpaved mileage under TheHub paving dropped from 172.6 to 147.6 miles, across 60 segments.

#### Why it matters: the survey follows layer 70

Across the state, the pavement survey collected:

| Layer 70 surface | Miles | Surveyed (latest cycle) | Share |
|---|---|---|---|
| Paved | 29,190 | 23,409 | **80%** (90% on county routes) |
| Unpaved | 11,217 | 87 | **1%** |

A paved road coded gravel is essentially never collected. Of the 110 TheHub segments that are mostly unpaved on layer 70, **101 (119.4 mi) have never been surveyed**. Only 5 have current survey data. These roads are therefore:
- missing from `analysis_segments`;
- absent from every PMS run;
- invisible to the optimizer, although WVDOT is paying to maintain them as pavement.

#### Largest cases (completed, mostly unpaved on layer 70)

| Project | Name | Code | District | Route | MP | Miles | Unpaved | Done | Surveyed |
|---|---|---|---|---|---|---|---|---|---|
| 2021000435 | Middle Mountain Rd | 08 | 8 | 4240010000000 | 0.00–17.17 | 17.17 | 14.30 | 2021-10 | never |
| 2023440022 | Grannies Creek Rd | 08 | 3 | 4440029010000 | 0.20–5.18 | 4.98 | 2.58 | 2023-10 | 2.5 mi |
| 2023430015 | Victory Ridge +2 | 14 | 3 | 4340016080000 | 0.00–4.49 | 4.49 | 3.85 | 2023-07 | 0.7 mi |
| 2022430010 | White Oak Road +2 | 08 | 3 | 4340022000000 | 4.60–8.68 | 4.08 | 3.29 | 2023-06 | 0.8 mi |
| 2022090004 | Porto Rico Rd | 08 | 4 | 0940054000000 | 0.00–3.48 | 3.48 | 2.14 | 2023-03 | never |
| 2024400013 | Coleman Creek Rd | 08 | 1 | 4040030010000 | 0.00–3.36 | 3.36 | 3.36 | 2024-09 | never |
| 2023540034 | Garrison Rd | 14 | 3 | 5440003120000 | 0.00–3.28 | 3.28 | 1.93 | 2023-10 | 1.3 mi |
| 2024490004 | Selbyville Rd +2 | 08 | 7 | 4940044000000 | 3.31–6.23 | 2.92 | 2.92 | 2024-06 | never |
| 2023390030 | Chestnut Ridge Heights Rd +1 | 08 | 4 | 3940064000000 | 0.64–3.36 | 2.72 | 2.72 | 2023-08 | never |
| 2020001090 | Mud Lick Right Fork | 08 | 1 | 4040034080000 | 1.95–4.47 | 2.52 | 2.52 | 2020-09 | never |
| 2021000766 | Beverlin Fork Rd +15 | 08 | 4 | 0940001000000 | 0.00–2.45 | 2.45 | 2.45 | 2023-06 | never |
| 2023390035 | McNair Rd | 08 | 4 | 3940026220000 | 0.00–2.18 | 2.18 | 2.18 | 2023-08 | never |

Active projects on layer 70 gravel include:
- Dry Ridge, D1 (2026200021): 3.3 of 5.4 mi.
- Ferguson Ridge Rd, D2 (2026500010): 3.0 of 3.0 mi.
- Elk Horn Road, D5 (2026120004): 1.9 of 3.1 mi.

These should be recoded when they finish.

The full list of 160 segments with 141.4 unpaved miles is in [`hub_pavement_segments_on_unpaved_lrs.csv`](hub_pavement_segments_on_unpaved_lrs.csv). It gives project, route, milepoints, unpaved miles, the layer 70 code and record date, completion and survey coverage. It leaves out the 68 end slivers.

### 11. Route IDs and milepoints layer 70 doesn't know (45 mi)

These are TheHub route IDs or milepoints that layer 70 doesn't have:
- **Malformed route IDs:**
  - `06100640000eb` is West Pea Ridge – Huntington Mall. Layer 70 has `06100640000EB`; only the letter case differs.
  - `032` (Low Gap Branch) is a truncated route ID.
- **Gaps in layer 70:** on `5530016000000`, layer 70 has no surface from MP 11.54 to 22.52, although the route continues past it. Probably the stretch is shared with another route and layer 70 carries its surface on that route only. Two Itmann–Mullens projects sit in that gap: 2021550003 (MP 11.53–24.94) and 2022550012 (MP 11.53–23.49). They overlap each other too.
- **Milepoints past the end of the route:** Reynolds Gap Resurface (2023160025) is on `1640002000000` at MP 6.37–9.74, but layer 70 ends at MP 6.30.

### 12. Overlapping projects

138 pairs of pavement projects on the same route overlap within a year of each other, covering 347 mi. Another 11 segments (11.2 mi) overlap within a single project. Examples include Itmann–Mullens, 2021550003 and 2022550012, which share 11.96 mi. The list is in [`hub_pavement_project_overlaps.csv`](hub_pavement_project_overlaps.csv).

Other segment issues:
- 143 paving projects ($715M) have no route segments, so they can't be placed.
- 18 STIP-resurfacing projects carry a non-paving construction code.
- 14 projects are in both the bridge and the paving sets.

---

## What to fix

### In TheHub (ask the owners)

1. **Correct the bridge links.** Start with the 13 neighbour cases (list in §1), the 31 links to bridges with no sign of work, and the name mismatches that turn out to be wrong. Laurel Creek Girder should point at 30A294 (or 30A013), not 30A012.
2. **Link replacements to the new BARS as well as the old one,** so the new bridge carries its history.
3. **Record the COMPLETE CONST milestone** when construction ends. The construction-end date is the financial close-out, a year or more later.
4. **Fix the malformed route IDs:** `06100640000eb` and `032`.
5. **Give bridge-coded projects a bridge,** especially the large ones (Nitro I/C, Wellsburg, Cheat River).

### On the LRS (layer 70)

6. **Recode the 160 segments** in [`hub_pavement_segments_on_unpaved_lrs.csv`](hub_pavement_segments_on_unpaved_lrs.csv) that TheHub has paved, and review the 1–3 April 2024 reload for other gravel records that overwrote pavement.
7. **Post completed TheHub paving to layer 70 when the project closes.** A standing feed from TheHub to the LRS team would do it.
8. **Add the recoded roads to the next survey.** Until then, give the vendor the list rather than relying on layer 70.

### In AMPS

9. **A logged link-override / successor crosswalk** in the `bms` schema, used by every per-bridge TheHub figure. It covers mislinks (§1) and puts a replacement on its new bridge (§2).
10. **Count a TheHub record as completed work only if it has a construction phase** (§5).
11. **Compare construction with construction** on project cards, and show engineering and right-of-way separately (§6).
12. **Label construction-end dates as close-out,** and don't use bulk fiscal dates as a construction year (§7).
13. **Group split records into one job** by state project number without the stem and phase digit, for counts, bands and the committed seed (§4).
14. **Add codes 68 and 67 (at least) to `PAVING_CODES`,** and map TheHub treatments by construction code rather than name (§9).
15. **Flag TheHub pavement segments that sit on unpaved layer 70** in the pipeline checks (§10), so the gap shows up before a survey cycle rather than after.

## Files

| File | What |
|---|---|
| [`hub_pavement_segments_on_unpaved_lrs.csv`](hub_pavement_segments_on_unpaved_lrs.csv) | The 160 TheHub pavement segments on unpaved layer 70: project, route, milepoints, unpaved miles, layer 70 code and record date, completion, survey coverage |
| [`hub_pavement_project_overlaps.csv`](hub_pavement_project_overlaps.csv) | Overlapping pavement projects |
| `scripts/hub_audit/pavement_surface_check.py` | The layer 70 check (downloads layer 70 unless given a saved copy) |
| `scripts/hub_audit/thehub/` | The TheHub checks: `fetch.py` caches TheHub (set `HUB_AUDIT_CACHE`, default `cache/` beside the scripts), then `q1_mislinks.py` … `q8.py`; run from the repo root |
