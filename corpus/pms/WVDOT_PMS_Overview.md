# WVDOT PMS Overview

> A 100-foot view of the West Virginia DOT Pavement Management System — what the main tables are, where they come from, how annual vendor data gets stitched onto a stable network, and how the analysis output loops back into real-world work. Start here before diving into any of the deeper docs.
>
> The PMS is the pavement part of **AMPS** (Asset Management & Performance System), WVDOT's asset management app, alongside the Bridges and BMS (bridge planning) folders — see the [Bridges & BMS Usage Guide](/docs/BMS_Usage).

If you want the full story of how any one piece works, each section links to its deep-dive doc. This page is the **map**, not the manual.

---

## Table of Contents

1. [What the PMS is, in one paragraph](#1-what-the-pms-is-in-one-paragraph)
2. [The five main tables at a glance](#2-the-five-main-tables-at-a-glance)
3. [How everything connects](#3-how-everything-connects)
4. [Where processing starts](#4-where-processing-starts)
5. [The conflation story](#5-the-conflation-story)
   - [5.1 Why conflation is needed](#51-why-conflation-is-needed)
   - [5.2 Visualizing the reconflation — step by step](#52-visualizing-the-reconflation--step-by-step)
6. [Projects and committed work](#6-projects-and-committed-work)
7. [Closing the LRS loop](#7-closing-the-lrs-loop)
8. [Where to go next](#8-where-to-go-next)

---

## 1. What the PMS is, in one paragraph

WVDOT collects pavement condition data every year — roughness (IRI), rutting, cracking, faulting — on every mile of the state-maintained highway network. The PMS takes that raw survey data, snaps it onto a stable 0.1-mile LRS grid, enriches it with traffic and network attributes, runs an optimization engine to pick which pavement segments to treat over the next 10–20 years under a budget, and hands the resulting **work program** back to planners and engineers so they can let real contracts. The same database holds the history, the analysis runs, and the programmed work — all five of the main tables below play one of those roles.

---

## 2. The five main tables at a glance

| # | Table | Contains | Where it comes from | Used by |
|---|-------|----------|---------------------|---------|
| 1 | **`routes`** | The LRS "skeleton" — one row per state-route ID, with system type, functional class, district, county, total mileage. | WVDOT's Linear Referencing System (LRS) master. Populated by `db/load_routes.py` from the route dictionary. | Everything. It's the dimension every other table joins to. |
| 2 | **`condition_history`** | **Raw, unconflated** annual condition measurements — IRI, rut, crack %, faulting, AADT, and pre-computed indices per segment per year. One row per `(segment_id, survey_year)`. | The vendor's annual survey file (CSV/Excel). Loaded by `db/load_condition_history.py`. | The reconflation stage reads this to produce the normalized table. |
| 3 | **`reconflate_normalized`** | The **same measurements**, but **snapped onto the stable 0.1-mile grid** via length-weighted averages. One row per `(segment_id, survey_year)`. Includes a coverage percentage so you can flag partial data. | Output of the external `lrsops overlay` tool operating on `condition_history` + the LRS reference table. Loaded by `create_analysis_segments.py`. | Feeds into `analysis_segments`. |
| 4 | **`analysis_segments`** | The **engine's working table**. Fully denormalized: geometry, lanes, AADT, pavement type, deterioration family, and the six condition indices (PSI, RDI, SCI, ECI, JCI, CSI) ready to optimize. One row per LRS segment (~260 K rows on the full WV state network). | Built by `create_analysis_segments.py` — takes `reconflate_normalized` and **layers LRS attribute overlays** on top (district, county, NHS, coal-route flag, AADT from traffic counts). | Every analysis run. This is the ~260 K-row frame the engine pulls into memory. |
| 5 | **`analysis_runs`** | The **output** side. One row per analysis run the user kicks off. Holds the run configuration, progress state, and — when complete — the full work program as a JSONB blob. | Written by `api/routes/runs.py` when a user clicks *New Run* in the UI. The engine updates it live as it runs. | The UI (Runs list, Run Detail page, Excel export). Also the audit trail for "what work program did we produce on 2026-04-01?". |

Plus one sidecar table — **`projects`** — for programmed work, described in [§6](#6-projects-and-committed-work).

---

## 3. How everything connects

```
                     VENDOR DATA (annual survey file)
                     IRI · rut · crack · faulting
                              │
                              ▼
                   ┌────────────────────┐
                   │ condition_history  │  raw, one row per
                   └─────────┬──────────┘  segment × year
                             │
                             │  lrsops overlay
                             │  (length-weighted averages
                             │   onto the 0.1-mi target grid)
                             ▼
                   ┌────────────────────┐
                   │reconflate_normalized│ normalized —
                   └─────────┬──────────┘  year-over-year comparable
                             │
                             │  LRS attribute overlays
                             │  (AADT, district, county,
                             │   NHS, coal route, lanes)
                             ▼
                   ┌────────────────────┐
                   │ analysis_segments  │  engine-ready,
                   └─────────┬──────────┘  ~260 K rows, 40+ columns
                             │
                             │  user clicks "New Run"
                             │  → run_optimization_pipeline()
                             ▼
                   ┌────────────────────┐
                   │   analysis_runs    │  work program stored
                   └─────────┬──────────┘  in result_summary (JSONB)
                             │
                             │  export to Excel / review
                             ▼
                    LRS-let contracts
                             │
                             │  (become programmed work...)
                             ▼
                   ┌────────────────────┐
                   │      projects      │ ──┐  feedback loop:
                   └────────────────────┘   │  committed projects set
                             ▲              │  is_committed flags on
                             │              │  analysis_segments, which
                             └──────────────┘  the optimizer honors
                                              on the next run

       ┌────────────────┐
       │    routes      │   ◀─── dimension table, joined to everything
       └────────────────┘
```

At the bottom of the page, `routes` sits off to the side as the dimension table that every other table joins to for things like route name, district, and functional class.

---

## 4. Where processing starts

The whole pipeline kicks off when **a new year of vendor survey data lands on disk** — typically an annual CSV drop from the ARAN/Pathway vendor. A WVDOT engineer runs the ingest pipeline (`scripts/import_pavement_data.py` or the `db/load_*.py` helpers). In sequence:

1. **Route dictionary refresh** — `db/load_routes.py` pulls any new/renamed routes into `routes`.
2. **Raw load** — `db/load_condition_history.py` reads the vendor CSV and inserts one row per `(segment_id, survey_year)` into `condition_history`. The values here are **exactly what the vendor reported** — IRI in inches/mile, rut depth in inches, crack percentage, etc., on the vendor's own measurement grid.
3. **Reconflate** — `create_analysis_segments.py` shells out to the external `lrsops` tool. This is the conflation step ([§5](#5-the-conflation-story) below). The output lands in `reconflate_normalized`.
4. **Attribute enrichment** — the same script runs LRS attribute overlays (AADT, district, county, NHS type, coal-route flag, lanes) from other LRS sources on top of the normalized condition frame. The result is then bulk-loaded into `analysis_segments`.
5. **Ready to analyze** — from this point on, any user can click *New Run* in the UI and the engine will read from `analysis_segments` and write results into `analysis_runs`.

Steps 1–4 are offline operations that only run when new data is available. Once `analysis_segments` is rebuilt, the rest of the system (API + UI + optimizer) is completely live — no rebuild needed per run.

See the [Data Pipeline deep dive](WVDOT_PMS_Data_Pipeline.md) for the exact SQL, shell commands, and refresh runbook.

---

## 5. The conflation story

### 5.1 Why conflation is needed

Here's the awkward thing about pavement condition data: **the vendor's measurement grid isn't the same as our analysis grid**, and it drifts a little every year.

When the vendor drives an ARAN van down I-77, it records IRI and rut depth in fixed time or distance intervals from the van's own GPS. That produces segments like "I-77 MP 12.003 to 12.051" — bounded by whatever the GPS happened to read. Next year they drive the same road and get slightly different bounds, because GPS isn't perfect, milepost signs move, and new pavement patches shift the reference.

Meanwhile, the WVDOT analysis grid is **stable 0.1-mile segments**: `I-77 MP 12.000–12.100`, `12.100–12.200`, and so on. Those bounds never move — they're the unit of management, the unit of work programming, the unit everything gets joined to.

If we just compared last year's IRI value on "I-77 12.003–12.051" against this year's IRI value on "I-77 12.002–12.049" and called it a trend, we'd be lying: the numbers are for slightly different chunks of pavement. The trend is noise.

**Conflation** is how we fix that: we length-weight-average the vendor's raw measurements onto our stable target grid, so year-over-year comparisons are apples-to-apples.

### 5.2 Visualizing the reconflation

Six pictures to show the whole thing. One short stretch of I-77 (MP 0.09 → 0.38), three years of vendor surveys.

```text
STEP 1 — Raw collected segments drift year over year
──────────────────────────────────────────────────────

Year 2020:  ├──────── Seg A ────────┤├───── Seg B ─────┤
            0.11                   0.23              0.38
            IRI=85                 IRI=120

Year 2021:     ├──── Seg A ────┤├────── Seg B ──────┤
               0.12           0.21                 0.35
               IRI=90         IRI=115

Year 2022:  ├─────── Seg A ─────────┤├───── Seg B ─────┤
            0.09                   0.25              0.36
            IRI=82                 IRI=118
```

The vendor boundaries move each year. Comparing raw IRI values is apples-to-oranges.

```text
STEP 2 — Target 0.1-mile grid (fixed forever)
──────────────────────────────────────────────────────

            ├─────────┼─────────┼─────────┼─────────┤
            0.0      0.1       0.2       0.3       0.4
            │ Bin 1  │  Bin 2  │  Bin 3  │  Bin 4  │
```

```text
STEP 3 — Split each source segment into the bins it overlaps
──────────────────────────────────────────────────────

            ├─────────┼─────────┼─────────┼─────────┤
            0.0      0.1       0.2       0.3       0.4
                      ◄══════════════════►
                      │   Seg A (IRI=85)  │
                      ▼                   ▼
                 Bin 2: 0.09 mi       Bin 3: 0.03 mi
                                ◄═══════════════════►
                                │   Seg B (IRI=120)  │
                                ▼                    ▼
                           Bin 3: 0.07 mi       Bin 4: 0.08 mi
```

```text
STEP 4 — Length-weighted average per bin (numeric fields)
──────────────────────────────────────────────────────

Bin 3, Year 2020:

    Seg A: 0.03 mi @ IRI=85
    Seg B: 0.07 mi @ IRI=120

                    (0.03 × 85) + (0.07 × 120)
    Weighted IRI = ─────────────────────────── = 109.5
                           0.03 + 0.07
```

```text
STEP 5 — Length-dominant rule (categorical fields)
──────────────────────────────────────────────────────

Surface type in Bin 3:

    Asphalt:   ██░░░░░░░░  0.03 mi (30%)
    Concrete:  ███████░░░  0.07 mi (70%)  ← winner

    → Surface Type = "Concrete"
```

```text
RESULT — four stable reconflate_normalized rows per year
──────────────────────────────────────────────────────

            ├─────────┼─────────┼─────────┼─────────┤
            0.0      0.1       0.2       0.3       0.4
            │  N/A   │ IRI=85  │IRI=109.5│ IRI=120 │
            │        │ Asphalt │Concrete │Concrete │
```

Every year produces the same four bins on the same `(route, bmp, emp)` keys.

```text
STEP 6 — Join years on the stable key (trivial relational join)
──────────────────────────────────────────────────────

    Year 2020          Year 2021          Year 2022
    ┌────────────┐     ┌────────────┐     ┌────────────┐
    │ rt│bmp│emp │     │ rt│bmp│emp │     │ rt│bmp│emp │
    │I77│0.0│0.1 │     │I77│0.0│0.1 │     │I77│0.0│0.1 │
    │I77│0.1│0.2 │     │I77│0.1│0.2 │     │I77│0.1│0.2 │
    │I77│0.2│0.3 │     │I77│0.2│0.3 │     │I77│0.2│0.3 │
    └──────┬─────┘     └──────┬─────┘     └──────┬─────┘
           │                  │                  │
           └──────────────────┼──────────────────┘
                              ▼
              JOIN ON (route, bmp, emp)
                              ▼
             ┌──────────────────────────┐
             │  Unified multi-year set  │
             └──────────────────────────┘
```

Year-over-year queries become a plain relational join — `WHERE iri_2024 > iri_2020` just works. The `segment_condition_by_year` view in `db/schema.sql` does exactly this.

---

## 6. Projects and committed work

The `projects` table holds **programmed work** — things WVDOT has already decided to do. Typical rows:

- "Reconstruct I-77 MP 42.1–48.7 in 2027, estimated $24 M."
- "Thin overlay US-60 MP 120.3–125.8 in 2026, under contract."

It's a separate table (not derived from the engine's output) because the inputs come from outside the PMS — from WVDOT's programming office, from budget commitments, from political priorities, from federal-aid pipelines. The engine doesn't invent these; they're facts-of-life the engine has to respect.

**How they feed back into the analysis:**

Every so often, `scripts/populate_committed_flags.py` scans the `projects` table and, for each programmed project, finds every `analysis_segments` row whose route + MP range overlaps it. On each overlapping segment, it sets:

- `is_committed = TRUE`
- `committed_treatment_id = <whatever treatment is planned>`
- `committed_program_year = <1-indexed year>`

When the engine runs, it honors those flags: in the committed year it forces the committed treatment (bypassing the usual trigger-eligibility rules); in earlier years it locks the segment (no eligibility at all — you can't "pull a project forward"); after the committed year it reverts to normal behavior.

That means the work program the engine produces is always a mix of:

1. **Committed projects** — the ones WVDOT already decided. Non-negotiable.
2. **Optimizer picks** — everything else, chosen to maximize network benefit under the remaining budget around the commitments.

This is how the PMS stays aligned with real-world programming constraints instead of spitting out pretty work programs that ignore the six reconstruction projects already under contract.

---

## 7. Closing the LRS loop

The engine's output lives in `analysis_runs.result_summary` as a JSONB blob. Inside that blob is a `project_summary` array, and every entry has:

- `joint_id` — the group of contiguous segments the optimizer selected
- `route_id`, `begin_mp`, `end_mp` — LRS coordinates pointing straight back at the network
- `treatment_id` — which treatment to apply
- `program_year` — which year of the analysis horizon
- `cost`, `benefit`, `length_miles`, `segment_count` — the totals

Those LRS coordinates are the **bridge back to the real world**. When a planner exports a run to Excel (`GET /api/runs/{id}/export.xlsx`), the resulting workbook has one sheet that's literally a list of `(route, begin_mp, end_mp, treatment, year)` rows — the same format WVDOT uses to scope and let contracts. An engineer takes that sheet, scopes the work, lets the contract, and eventually the contract gets entered into `projects` as a new programmed row.

Once that row exists in `projects`, the next time `populate_committed_flags.py` runs, the new project's segments get flagged as committed. The *next* analysis run sees those commitments and plans around them.

**That's the loop**: vendor data → condition_history → reconflate_normalized → analysis_segments → analysis_runs → LRS contracts → projects → back into analysis_segments as commitments → analysis_runs again. The pavement network keeps getting surveyed, the engine keeps re-planning around what's already committed, and the work program stays current.

```
              ┌──── new vendor survey ────┐
              │                           │
              ▼                           │
      condition_history                   │
              │                           │
              ▼                           │
   reconflate_normalized                  │
              │                           │
              ▼                           │
     analysis_segments ◀─── is_committed ─┤
              │                           │
              ▼                           │
       analysis_runs                      │
              │                           │
              ▼                           │
       LRS contracts                      │
              │                           │
              ▼                           │
          projects ─────────────────────── loop closes
```

It's not a one-way pipeline — the `projects` feedback is what makes the system an actual management loop instead of a one-shot optimization.

---

## 8. Where to go next

- [System Architecture](WVDOT_PMS_System_Architecture.md) — how the five subsystems (DB / engine / API / UI / docs) fit together as code.
- [Database Reference](WVDOT_PMS_Database_Reference.md) — every column of every table, with FKs and indexes.
- [Data Pipeline](WVDOT_PMS_Data_Pipeline.md) — the step-by-step ingest runbook (shell commands, `lrsops` invocation, refresh cadence).
- [Import Past Projects](Import_Past_Projects.md) — loading historical closed projects from the WVDOH Hub export into the projects table.
- [Import Analysis Segments](Import_Analysis_Segments.md) — the three-phase pipeline from raw vendor CSVs to the engine-ready analysis_segments table.
- [Analysis Engine](WVDOT_PMS_Analysis_Engine.md) — phase-by-phase walkthrough of what happens inside a single run.
- [Optimization Logic](WVDOT_PMS_Optimization_Logic.md) — the IBC algorithm, rolling-horizon look-ahead, budget enforcement, with worked examples.
- [Other Optimization Strategies](WVDOT_PMS_Other_Optimization_Strategies.md) — the downfalls of greedy IBC and the alternative approaches on the roadmap.
