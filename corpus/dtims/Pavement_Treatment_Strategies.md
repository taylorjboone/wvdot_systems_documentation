# Treatment strategies and treatment order

**Study date:** 2026-09-29. This is the third part of the raw-distress study, after
- [Raw distress deterioration](/docs/Pavement_Raw_Distress_Deterioration) (how the raw values deteriorate), and
- [Treatment resets](/docs/Pavement_Treatment_Resets) (what each treatment does to them).

How the whole study was done: [Raw Distress Study — Process](/docs/Pavement_Raw_Distress_Study).

It asks three questions:
1. What treatment strategies WVDOT actually follows (from TheHub history).
2. What order of treatments the fitted curves and resets say is most cost-effective.
3. What that means for config 1's triggers and sequencing.

**Scripts** (in `dtims_docs/raw-deterioration-study-2026-09-29/`): `scripts/history.py`, `scripts/strategies.py`, `scripts/budget.py`. **Outputs:** `results/history_out.txt`, `results/strategies.csv`, `results/budget_orders.csv`.

---

## 1. Bottom line

1. **Treatment choice should follow a small decision tree on the raw values, per surface and route group:**

   | Condition (asphalt) | Treatment |
   |---|---|
   | cracking 1–5% **and** IRI < 110, non-Interstate, fewer than 2 seals since the last overlay | chip seal (AADT < 1,000) / cape seal |
   | cracking 5–20% **or** IRI 110–170 | thin overlay |
   | cracking > 20% **or** IRI > 170 | thick overlay |
   | IRI > 250 with high cracking repeatedly after overlays, or the base is failing | reconstruction (no survey signal separates it; project-level decision) |

   - Microsurfacing and ultra-thin overlays are **not** cost-effective on the survey evidence: they don't reset cracking (micro) or IRI comes back fast (ultra-thin).
   - Interstates skip seals: a thin overlay when Good is lost (cracking ≥ 5%) is the cheapest way to keep them Good.
2. **Order under a budget:** fund by **benefit/cost** (Good lane-mile-years gained plus Poor lane-mile-years avoided per dollar), not worst-first or cheapest-first.
   - At ~$15k per lane-mile per year:

     | Order | Average % Good | Average % Poor |
     |---|---|---|
     | worst-first | 8.5 | 13.7 |
     | cheapest-first | 37 | 39 |
     | **benefit/cost** | **27** | **22** |

   - At ~$25k, benefit/cost gets 39% Good / 1% Poor against worst-first's 29% / 1%.
   - Pure worst-first spends everything on thick overlays and never builds Good. Pure cheapest-first lets Poor run away.
3. **Life-cycle order:**

   | Route group | Recommended life cycle |
   |---|---|
   | Non-Interstate | new surface → seal at ~3 years → seal at ~6 → thin overlay at ~13–16 → repeat, with thick overlays once IRI is past ~170 |
   | Interstate | thin overlay every ~8 years as cracking reaches 5% |

   Two seals are the limit because seals don't lower IRI. IRI keeps climbing under them, and the overlay is what brings it back.
4. **WVDOT today** (TheHub):
   - **Low systems are worst-first:** County thin overlays go on at IRI ~246, cracking 24%, 48% Poor.
   - **Interstates are preventive:** thin overlays at IRI 70, cracking 0.5%, 52% Good.
   - **Almost no seal cycle:** seals are 4% of treated miles.
   - **Re-treatment is slow:** only ~36% of thin overlays are re-treated within 10 years.

   The biggest gain available is a **seal cycle on the low-volume system**, paid for by fewer late thin/thick overlays.
5. **Config 1:**
   - Its triggers are index windows (PSI / SCI / RDI …), not raw-value windows.
   - Its sequencing table allows almost any treatment after any other (138 pairs), so it doesn't encode an order.
   - Its counters (2 chip seals, 1 micro) match the seal limit above.
   - **Its triggers allow the treatment WVDOT actually chose on only ~48% of the miles of TheHub projects not yet built** (§5.3):
     - thin overlays 42%: the index windows send them to thick;
     - ultra-thin, reconstruction, seals and CPR 0%: committed-only, IM_FUNDS, the 3-mile minimum, the 1-lane / AADT gates.

---

## 2. What WVDOT does — TheHub history

**Data:**
- 4,571 pavement project segments, 3,511 projects (2,880 completed).
- The construction code grouped into treatments as in the resets study.
- Completions start in earnest in 2019 (2019: 160, 2023: 684, 2025: 608), so histories are at most ~7 years deep.
- The next / previous treatment on an extent is the next / previous pavement project covering ≥ 50% of it on the same route (both directions), more than 90 days apart.

### 2.1 What follows what

Miles of project segments, previous treatment (rows) → this treatment (columns):

| Previous ↓ / next → | Surface trt | Micro | Ultra-thin | Thin | Thick | Reconstruct |
|---|---|---|---|---|---|---|
| Surface treatment | 12 | 5 | | 48 | 28 | |
| Ultra-thin | 12 | | 3 | 35 | 2 | 6 |
| **Thin overlay** | 72 | 46 | 31 | **428** | 98 | 23 |
| Thick overlay | 25 | 5 | 2 | 71 | 30 | 1 |
| Reconstruction | | | | 14 | 2 | 13 |

**Median years between the two, [p25–p75]:**

| Previous → next | n | Median years [p25–p75] |
|---|---|---|
| thin → thin | 128 | 3.0 [1.3–4.6] |
| thin → thick | 33 | 3.7 |
| thin → micro | 13 | 4.5 |
| thin → reconstruct | 14 | 3.6 |
| ultra-thin → thin | 11 | 4.0 |
| surface trt → thin | 16 | 1.6 |
| thick → thin | 17 | 1.1 |

These gaps are **short because the history is short** (only re-treatments inside 2019–2026 can be seen). The 1–2-year ones are mostly TheHub route segments that list more of the route than was paved, or follow-on phases, not real re-treatments.

- The dominant pattern is **overlay on overlay**. A thin overlay is followed by another thin overlay (60% of the miles), a thick overlay (14%) or a seal / micro (17%).
- **Seals are rarely a planned step between overlays.**

### 2.2 How long a treatment lasts before the next project

Share of miles re-treated within N years of completion (Kaplan-Meier, completions 2012+; later years rest on fewer projects):

| Treatment | n | ≤ 2 y | ≤ 4 y | ≤ 6 y | ≤ 8 y | ≤ 10 y |
|---|---|---|---|---|---|---|
| Surface treatment | 250 | 0.06 | 0.20 | 0.23 | 0.37 | 0.61 |
| Microsurfacing | 31 | 0.00 | 0.25 | 0.48 | 0.53 | 0.53 |
| Ultra-thin | 161 | 0.04 | 0.08 | 0.15 | 0.23 | 0.57 |
| **Thin overlay** | 2,409 | 0.05 | 0.12 | 0.19 | 0.30 | **0.36** |
| Thick overlay | 680 | 0.08 | 0.22 | 0.26 | 0.43 | 0.66 |

Thin overlays by system, ≤ 10 years: County 0.29, WV 0.49, US 0.54, Interstate 0.18 (thin sample).

So the **observed thin-overlay life is > 10 years on County routes** and ~9–10 years on US / WV routes. That is longer than config 1's service lives (thin 8, thick 10, seals 5), and much longer than the ~6–8-year cycle the curves say keeps a segment Good (§3). The low system is run to Poor before it is resurfaced.

### 2.3 Condition when WVDOT chose each treatment

Last survey ≤ 3 years before construction started, route-average over the project extent. Asphalt; miles-weighted median [p25–p75]. Includes projects not yet built.

| Treatment | n | IRI | FHWA cracking % | Rut in | % Good | % Poor |
|---|---|---|---|---|---|---|
| Microsurfacing | 28 | 88 [55–106] | 3.0 [0.5–6.4] | 0.12 | 41 | 0 |
| Ultra-thin | 53 | 112 [97–212] | 4.7 [0.7–18.3] | 0.15 | 24 | 20 |
| Surface treatment | 43 | 128 [91–161] | 5.7 [1.0–23.9] | 0.16 | 13 | 9 |
| **Thin overlay** | 643 | **155 [113–244]** | **13.6 [2.8–30.5]** | 0.18 | 12 | 26 |
| **Thick overlay** | 398 | **252 [145–353]** | **24.6 [12.8–34.5]** | 0.23 | 5 | 49 |
| Reconstruction | 33 | 116 [76–157] | 4.6 [1.9–19.9] | 0.19 | 28 | 10 |

Thin overlays by system:

| System | n | IRI | Cracking | % Good | % Poor |
|---|---|---|---|---|---|
| Interstate | 32 | 70 | 0.5 | 52 | 1 |
| US | 153 | 110 | 3.2 | 24 | 4 |
| WV | 112 | 142 | 17.4 | 11 | 16 |
| **County** | 345 | **246** | **24.3** | 1 | **48** |

- **Worst-first on the low system:** half of a County thin-overlay project is already Poor when it is paved.
- **Preventive on the high system:** Interstate thin overlays go on while half the extent is still Good.
- **County thin overlays can't bring those roads back to Good.** They go on at IRI ~246, and a thin overlay keeps ~42% of the roughness above ~80, leaving ~150, which is Fair (resets study §3.2). Rough County roads need a thick overlay to reach Good on IRI.
- **Reconstruction is not chosen on condition** (median IRI 116, cracking 4.6%). The Reconstruction group here is widening / added lanes / realignment (codes 02, 04, 24, 66), driven by capacity and safety.

---

## 3. Which strategy — life-cycle simulation

### 3.1 Set-up

- **Population:** 2024 statewide asphalt survey records (0.1 mi), 3,000 per route group.

  | Route group | Start % Good / % Poor | Median IRI | Median cracking |
  |---|---|---|---|
  | Interstate | 68 / 0.1 | 61 | 0 |
  | HPMS_1 | 36 / 4 | 89 | 2 |
  | Other | 7 / 26 | 190 | 7 |

- **Deterioration** (deterioration study §4, §7a):
  - IRI: `0.78 + 0.49·(IRI/100)^3.4` + route-group adder, run at ⅓ rate for 3 years after thin / thick overlays and reconstruction.
  - Cracking: √C + s/yr, with s = 0.35 / 0.37 / 0.46 by route group, then scaled by the last treatment.
  - Rut: flat after its reset.
- **Resets** from the resets study §5. Seals add +3 in/mi/yr IRI (observed +5.6 after seals) and ultra-thin +8/yr for 4 years.
- **Costs:** config 1 `treatment_costs` (BC): chip $45k, cape $99k, micro $103k, ultra-thin $165k, thin $220k, thick $300k (×1.2 on Interstate) per lane-mile.
- **Other settings:** 30 years, MAP-21 Good / Poor per record weighted by lanes, treatments at least 3 years apart.

### 3.2 Strategies with enough money

Unconstrained: the strategy's rules are applied wherever they trigger. Average over 30 years.

| Strategy | Interstate %G / cost / G-yrs per $1M | HPMS_1 %G / cost / G-yrs per $M | Other %G / %P / cost / G-yrs per $M / P-yrs avoided per $M |
|---|---|---|---|
| 0. Do nothing | 13.5 / 0 / — | 6.7 / 0 / — | 1.2 / 66 / 0 / — / — |
| 1. Worst-first (today's pattern): thick if IRI > 250 or crk > 25; thin if Poor, crk > 13 or IRI > 155 | 64.9 / $16.1k / 32.0 | 53.8 / $18.9k / 24.9 | 11.0 / 0 / $26.7k / 3.7 / 24.8 |
| 2. Thin when Good is lost (crk ≥ 5 or IRI ≥ 95); thick if IRI > 170 | **98.8** / $25.5k / **33.5** | **96.6** / $29.9k / **30.1** | **86.8** / 0 / $46.9k / 18.3 / 14.1 |
| 3. Thin at crk ≥ 5 only; thick if IRI > 170 or crk > 20 | 97.9 / $25.6k / 32.9 | 86.7 / $27.5k / 29.1 | 59.5 / 0 / $39.7k / 14.7 / 16.7 |
| **4. Seal-first:** seal at crk 1–5 & IRI < 110 (≤ 2 seals); thin at crk 5–20 or IRI 110–170; thick at IRI > 170 or crk > 20 | 98.2 / $25.7k / 33.0 (no seals on Interstate) | 79.6 / $25.5k / 28.6 | 76.1 / 0 / **$32.2k** / **23.3** / 20.5 |
| 5. Seal-first, late overlays (thin crk ≥ 10 or IRI ≥ 140; thick IRI > 200 or crk > 25) | 73.2 / $18.2k / 32.7 | 62.9 / $23.3k / 24.2 | 53.8 / 0 / $26.4k / 19.9 / **25.0** |
| 6. Fixed thin cycle every 10 years | 80.0 / $22.0k / 30.2 | 66.1 / $22.2k / 26.8 | 10.7 / 0 / $24.0k / 4.0 / 27.6 |
| 7. Ultra-thin first (crk 2–8 & IRI < 120) | 66.5 / $37.2k / 14.2 | 25.1 / $45.3k / 4.1 | 15.3 / 0 / $59.4k / 2.4 / 11.2 |
| 8. Microsurfacing first (crk 1–5 & IRI < 110) | 84.9 / $45.6k / 15.6 | 77.7 / $47.3k / 15.0 | 53.9 / 0 / $53.6k / 9.8 / 12.4 |

**By route group:**
- **Interstate / HPMS_1:** resurface when Good is lost (2 / 3). About 30–34 Good-years per $1M. Seals add nothing on the Interstate (excluded anyway) and little on HPMS.
- **Other (the County / low-volume system):**
  - **Seal-first (4)** gives the most Good per dollar (23 Good-years per $M, 76% Good, at $32k per lane-mile-year).
  - Resurfacing whenever Good is lost (2) buys 87% Good but costs 45% more, because IRI 95 is hard to hold on these roads.
  - The worst-first pattern (1) and a fixed 10-year cycle (6) avoid Poor cheaply but leave the system Fair (~11% Good).
- **Microsurfacing and ultra-thin are the worst buys everywhere.** Microsurfacing doesn't reset cracking (+3 pts/yr after it); ultra-thin loses its IRI gain in ~4 years.

**Simulated life cycles**, starting right after a thin overlay:

| Route group / AADT | Strategy 2 (thin when Good lost) | Strategy 4 (seal-first) |
|---|---|---|
| Interstate, 30,000 | thin every 8 years (cracking ~6% each time) | the same (no seals) |
| HPMS_1, 6,000 | thin every 8 years | cape at y3, cape at y6, thin at y16, cape y20, cape y23, thin y33 → **~14–17-year overlay cycle with 2 seals** |
| Other, 600 | thin every 5–6 years (held back by IRI ≥ 95) | chip at y3, chip at y6, thin at y14, chip y17, chip y20, thin y28 → **14-year overlay cycle with 2 chip seals** |

Annualised:
- Interstate: 220k / 8 = **$27.5k** per lane-mile-year.
- HPMS seal-first: (2 × 99k + 220k) / ~15 = **$28k**, the same money for a similar % Good.
- Other at AADT < 1,000:
  - thin every ~6 years: 220k / 6 = **$37k**;
  - chip-chip-thin every 14 years: (2 × 45k + 220k) / 14 = **$22k**.

### 3.3 Order under a fixed budget

This is the treatment-order question: with less money than the rules would spend, which segments get funded first?

**Set-up:**
- Network sample in proportion to 2024 asphalt lane-miles by route group (9,000 records).
- Each year every record's candidate comes from the decision tree (strategy 4).
- Candidates are funded in one of three orders until the budget runs out.

**The three orders:**

| Order | How candidates are ranked |
|---|---|
| Worst-first | IRI + 5 × cracking, highest first |
| Preservation-first | cheapest treatment class first (seal < thin < thick), best condition first within it |
| Benefit/cost | Good lane-mile-years gained plus Poor lane-mile-years avoided over a 10-year look-ahead, per dollar |

**Current spend:** WVDOT's 2021–25 TheHub pavement volume works out to roughly **$20k per lane-mile-year** on ~34,600 asphalt lane-miles. That assumes 2 lanes per project mile, config unit costs, and no MMS county-forces paving.

Average over 30 years; the mix is the share of treated lane-miles:

| Budget per lane-mile-yr | Order | Avg % Good | Avg % Poor | Year-30 % Good / % Poor | Mix seal / thin / thick |
|---|---|---|---|---|---|
| $8k | worst-first | 2.6 | 34.1 | 0 / 56 | 0 / 0 / 100 |
| $8k | preservation-first | 23.1 | 50.3 | 24 / 67 | 55 / 43 / 2 |
| $8k | **benefit/cost** | 20.2 | **43.8** | 18 / 60 | 48 / 28 / 24 |
| $15k | worst-first | 8.5 | **13.7** | 7 / 19 | 0 / 0 / 100 |
| $15k | preservation-first | **37.0** | 38.7 | 37 / 42 | 54 / 39 / 6 |
| $15k | **benefit/cost** | 26.5 | 22.1 | 25 / 29 | 41 / 19 / 39 |
| $25k | worst-first | 28.8 | 1.1 | 38 / 0 | 0 / 5 / 95 |
| $25k | preservation-first | **52.6** | 19.3 | 53 / 11 | 53 / 32 / 14 |
| $25k | **benefit/cost** | 38.6 | **1.1** | 51 / 0 | 42 / 23 / 35 |

- **Worst-first** minimises Poor at mid budgets but spends everything on thick overlays. Good collapses (8.5% at $15k) and never recovers.
- **Preservation-first** maximises Good but abandons the worst roads (Poor 39% at $15k).
- **Benefit/cost** is the balanced order:
  - at ~$20k (between the $15k and $25k rows) it should hold roughly 30–35% Good and 5–15% Poor;
  - at $25k it gets worst-first's 1% Poor with 10 points more Good.
  - Its mix is about 40% seals, 20% thin, 35–40% thick by lane-mile.
- **The weights set the answer.** Benefit/cost here counts a Good-year and an avoided Poor-year equally. MAP-21 targets are set separately for % Good and % Poor. If the Poor target binds (NHS non-Interstate Poor ≤ 10%, Interstate ≤ 5%), weight Poor-years higher, or add the target as a constraint — that is what AMPS's MILP-assist targets already do.

---

## 4. Recommended strategy and order

### 4.1 Decision tree

Asphalt, raw values of the 0.1-mi segment or project average:

```
if IRI > 250 and cracking > 20 after two overlays in 15 years  -> reconstruction / thick with base repair (project review)
elif IRI > 170 or cracking > 20                               -> THICK overlay
elif cracking >= 5 or IRI >= 110                              -> THIN overlay
elif cracking >= 1 and IRI < 110 and route group != Interstate
     and seals since last overlay < 2                         -> CHIP seal (AADT < 1,000) / CAPE seal
else                                                          -> nothing (or crack seal as routine maintenance)
Interstate: THIN overlay when cracking >= 5 or IRI >= 95; THICK when IRI > 170
Concrete (JCP/CRC): CPR / diamond grind when IRI > 120 or faulting > 0.10; HMA overlay -> composite (BC) when cracked slabs > 15%
```

### 4.2 Sequencing

What may follow what:

| After | Allowed next | Minimum gap |
|---|---|---|
| Thin / thick overlay, reconstruction | seal, thin, thick | seal ≥ 3 years (cracking needs to be ≥ 1% for a seal to have anything to do); thin/thick ≥ 5 years unless IRI > 170 |
| Seal (1st) | seal, thin, thick | ≥ 3 years |
| Seal (2nd in a row) | thin, thick (**no third seal**: IRI has climbed ~20–30 in/mi under the two seals) | ≥ 3 years |
| Microsurfacing / ultra-thin | only if kept as options: thin / thick next, never a second in a row | ≥ 3 years |

### 4.3 Budget order

1. Rank candidates by benefit/cost, with a Poor weight that meets the MAP-21 Poor targets.
2. Hold ~35–45% of lane-miles in seals and ~20% in thin overlays on the low system.
3. Stop using thin overlays on segments above IRI ~200. They leave the road Fair, so thick it or leave it.

---

## 5. Config 1 against this

### 5.1 How the config encodes strategy today

- **Triggers** are windows on the dTIMS indices.

  | Treatment | Trigger window |
  |---|---|
  | THIN_OVERLAY | PSI 2–3.5 or 2.8–5 with SCI / ECI ≤ 3.5 |
  | THICK_OVERLAY | PSI 1–3.5 with SCI ≤ 3, or SCI / ECI ≤ 2.55 |
  | CHIP_SEAL | RDI ≥ 3.5, SCI 3.5–4.5, ECI 2.5–4.5 |
  | CAPE_SEAL | PSI ≥ 3, SCI 3–4.5, ECI 3–4.5 |
  | MICROSURFACING | PSI 3.6–4.5 and indices 3.5–4.9, or 5–7 years after an overlay |

  They are not raw-value windows, so they can't be read directly as "cracking 1–5%" or "IRI < 110".
- **Sequencing** (`treatment_sequencing`, 138 rows) allows every asphalt treatment after every other, so it doesn't encode an order. The order comes only from the triggers, counters and intervals.
- **Counters:** chip seals ≤ 2 (`cnt_chip`) and microsurfacing ≤ 1 (`cnt_micro`) since the last other treatment. That matches the two-seal limit above.
- **Intervals:** `interval_years` is thin 2, thick 2, seals 3, ultra-thin 4, CPR 6. The 2-year minimum on thin and thick overlays allows overlay-on-overlay within 2 years, which the survey says buys little (the IRI hold lasts 3 years).
- **Other gates:**
  - chip seal AADT ≤ 1,000 and 1 lane;
  - cape and chip seals exclude the Interstate;
  - reconstruction requires the `IM_FUNDS` route group.

### 5.2 Suggested config changes

Proposals only; nothing was changed.

1. **Express the tree in raw terms** (a raw-value trigger branch kind) or re-derive the index windows so they match the §4.1 raw windows.
2. **Set `interval_years` for thin / thick to 5**, with an exception above IRI 170.
3. **Add a seal → overlay rule:** after 2 seals only thin / thick (the counter already stops a 3rd chip; add cape to the same counter).
4. **Drop or restrict MICROSURFACING and ULTRA_THIN_OVLY** as optimizer options. Or keep them with the observed resets (no cracking reset / IRI regain), and the optimizer will stop picking them.
5. **Rank by benefit per dollar, with a Poor weight or MAP-21 targets.** AMPS's greedy / MILP already optimise benefit under budget; the point is the benefit definition. Count Good and Poor lane-mile-years from the raw values, rather than index area.

### 5.3 Trigger check against TheHub projects not yet built

**Method** (`scripts/engine_trigger_check.py`):
- Projects: 593 Active TheHub pavement projects not yet built (start or letting 2025-07 or later), matched to 15,357 analysis segments and 1,103 joints. Today's state is their "before".
- The optimizer's own candidate generation (`engine.treatments.triggers.evaluate_triggers_segment_union_polars`: index windows, gates, minimum length on the joint, sequencing) was evaluated for program year 1 with config 1.
- Blocking gates were found by relaxing one gate at a time, then pairs and triples.

**Config 1 allows WVDOT's chosen treatment on only ~48% of the miles:**

| WVDOT chose | Projects | Miles | % miles the engine triggers it | IRI | Cracking | % G / F / P | What blocks it / what the engine offers instead |
|---|---|---|---|---|---|---|---|
| THIN_OVERLAY | 307 | 710 | **42** | 195 | 16.9 | 6 / 59 / 35 | Index windows (ECI, PSI, SCI). The engine offers **thick** on 280 of the 395 blocked joints, nothing on 98. |
| THICK_OVERLAY | 185 | 395 | **89** | 185 | 18.1 | 7 / 54 / 39 | SCI/ECI window on 58 joints; nothing triggers on 53. |
| MICROSURFACING | 12 | 97 | 25 | 79 | 0.1 | 47 / 53 / 0 | 3-mile minimum length on the joint. |
| RECONSTRUCT_BC | 25 | 92 | **0** | 89 | 8.5 | 28 / 63 / 9 | `require_route_group = IM_FUNDS`, plus PSI/ECI/SCI ≤ 1 windows. These are widening / capacity projects, not condition. |
| ULTRA_THIN_OVLY | 13 | 44 | **0** | 99 | 3.9 | 20 / 75 / 5 | `committed_only = true`: the optimizer can never choose it. |
| CHIP_SEAL | 6 | 24 | 0 | 149 | 0.0 | 5 / 86 / 9 | AADT ≤ 1,000, 1 lane, not Interstate, windows. |
| CAPE_SEAL | 3 | 23 | 0 | 74 | 0.0 | 53 / 47 / 0 | Not-Interstate gate and windows; 43% of the miles are RC. |
| MAJOR_CPR_DG | 3 | 8 | 0 | 110 | 19.9 | 5 / 86 / 9 | 3-mile minimum length. |

**What this shows:**
- **WVDOT's thin and thick overlays go on pavement in the same condition** (IRI 195 vs 185, cracking 17 vs 18, 35–39% Poor). The config splits them sharply by index window and sends almost all of it to thick. The survey resets say thick buys ~20 in/mi more smoothness for 36% more cost. So the split should be about roughness (IRI > 170 → thick), as in §4.1, not the SCI/ECI windows.
- **Several treatment rows are 0% for configuration reasons, not condition:**
  - ultra-thin is committed-only;
  - reconstruction needs IM_FUNDS;
  - micro and CPR have a 3-mile joint minimum;
  - chip seal is limited to 1-lane roads with AADT ≤ 1,000.
- **On 198 joints of planned WVDOT pavement projects the engine triggers nothing at all.** Before an AMPS plan is compared with the STIP, the windows need to cover the conditions WVDOT actually paves at.

---

## 6. Limits

- **The history is short** (TheHub completions from 2019). Re-treatment intervals beyond ~7 years are Kaplan-Meier extrapolations, and seal → seal → overlay cycles can't be observed directly because WVDOT rarely does them.
- **The simulation is a model.** It inherits the deterioration and reset fits, including their small samples for seals, micro and ultra-thin, and has no crack-seal or MMS patching effect.
  - Costs are config 1 unit costs, not bid prices.
  - The ~$20k per lane-mile-year current spend is a rough estimate.
- **Seal performance on higher-volume roads (AADT > 5,000) is untested here.** Most observed seals are on low-volume routes, so seal-first on HPMS routes is an extrapolation. Pilot it before adopting it there.
- **Only asphalt is simulated.** Concrete strategies rest on 3–30 extents.

---

## 7. Reproducing

After the deterioration study's steps 1–3 (same `STUDY_DIR`):

```sh
S=dtims_docs/raw-deterioration-study-2026-09-29/scripts
python $S/history.py        # sequences, Kaplan-Meier re-treatment, condition at selection  -> results/history_out.txt
cd $S && python strategies.py && python budget.py && cd -   # life-cycle and budget-order simulations -> results/*.csv
PYTHONPATH=. python $S/engine_trigger_check.py              # config 1 triggers vs TheHub projects not yet built
```
