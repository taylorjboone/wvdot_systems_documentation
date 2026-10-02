# Treatment Effects — What each BMS treatment actually does to NBI ratings

*2026-09-27. Measured from completed TheHub bridge projects and the AssetWise inspection record, and compared
with what the BMS configuration assumes (`bms.treatments.effects`). Reproduce with
`PYTHONPATH=. venv/bin/python scripts/bridges/treatment_effects.py` (needs the TheHub tunnel).*

## The short answer

| BMS treatment | BMS assumes | Measured on the target component (net of untreated bridges) | Lands |
|---|---|---|---|
| **SP1** Superstructure replacement | deck, super reset to 8 | super 5.0 → **7.4** (+2.4), deck 5.6 → **7.9** (+2.2), sub +0.8 | at completion |
| **BR1** Structure replacement | all components reset to 8 | super 5.3 → **6.3** (+1.2), deck 5.5 → **6.6** (+1.3); only 57–65% reach 7+ | at completion |
| **DK1** Deck replacement | deck reset to 8 | deck 4.7 → **6.1** (+1.4); 48% reach 7+ | at completion |
| **SP2** Superstructure rehabilitation | super +2, up to 7 | super 5.2 → **6.1** (+0.9) — and deck **+1.4**, sub **+1.1** | at completion |
| **SB2** Substructure rehabilitation | sub +2, up to 7 | sub 4.5 → **5.7** (+1.3) | the next inspection (+2 yr) |
| **SP6** Clean and paint | super +1 up to 7, held 5 yr | super 5.6 → **6.0** (+0.4), sub **+0.4**; fades after ~4 yr | the next inspection (+1 yr) |
| **JT1** Joint replacement | sub, super held 3 yr | super 6.1 → **6.6** (+0.5), deck +0.2 | +2 yr |
| **DK4** Modified PCC overlay (LMC / microsilica) | deck +2, up to 8 | deck 4.7 → **5.3** (+0.5, not significant) | +2 yr |
| **DK8** Waterproofing membrane with HMA overlay | deck +1 up to 7, held 3 yr | deck +0.4 (not significant); super +0.8, sub +0.7 | +2–4 yr |

Measured changes are **smaller than the BMS assumptions for every treatment except superstructure replacement**:
a structure or deck replacement typically moves the replaced components up about 1.2–1.4 points to the
low 6s, not to 8; rehabilitations and overlays deliver roughly half of the assumed +2. Painting and joints do a
little more than "hold": they lift the superstructure about half a point for four years or so.

## How it was measured

- **Projects:** every *completed* TheHub bridge project (construction codes 30–47, 70–74, 100–103, not
  cancelled or test) with a primary NBI bridge — 792 projects. Completion is the construction phase's
  "completed" milestone, else its end date.
- **Treatment types:** each project's construction codes (primary and additional) mapped to BMS treatments by
  `bms.treatments.hub_codes` (the same mapping as the committed-project seed). A project with several codes
  counts under each; codes with no BMS treatment are kept under their TheHub name.
- **Before and after:** for each component, the latest rating inspected 2–6 years before the completion year and
  the earliest 2–6 years after. The year either side is skipped, because the work reaches the ratings up to a couple
  of years before or after the recorded end date; with inspections every two years, the first rating two or more
  years out follows it.
- **Net of untreated bridges:** the same change for bridges of the same family (material / design / span count)
  with no completed TheHub project within 8 years, between the same calendar windows, is subtracted. This removes
  ordinary deterioration and the statewide rating waves found in
  [Deterioration Drivers](/docs/Bridges_Deterioration_Drivers) (the 2012–15 downgrades, the 2021 upgrades).
- **Link check.** TheHub sometimes names the wrong primary bridge: project "PANTHER GIRDER" (a box-beam
  replacement) is linked to 24A004 GEORGE BRANCH BRIDGE, a tee beam still rated 4 in 2026; "STONEY CREEK BR"
  to 38A082 CAMPBELLTOWN BRIDGE. A project counts as **linked** when a distinctive word of its name appears in
  the bridge's name, the feature it crosses or its route. 76 of 792 projects (10%) fail; their bridges show no
  change at all after the work (replacements −0.26, deck replacements −0.09), so they are mis-links. **The results
  here use linked projects only** (235 with usable before / after ratings).
- **Timing:** for each treated component, the year of the largest rise between consecutive inspections within
  4 years of completion, and the average path from 4 years before to 6 years after.

Sample sizes are modest — the post-2023 projects (312) are too recent for an after rating, and 132 projects'
bridges have no ratings in the inventory (other owners, or replacements recorded under a new BARS). 95%
confidence intervals are given below; treat anything with n < 15 as indicative.

## Results by treatment

Mean rating before → after, net change (95% CI), share improved, share at 7+ afterwards. Linked projects only.

### SP1 — Superstructure replacement (34 projects; assumed: deck and super reset to 8)

| Component | n | Before → after | Net (95% CI) | Improved | 7+ after |
|---|---:|---|---|---:|---:|
| Superstructure | 10 | 5.00 → 7.40 | **+2.41** (+1.30, +3.52) | 80% | 80% |
| Deck | 9 | 5.56 → 7.89 | **+2.23** (+1.37, +3.10) | 89% | 89% |
| Substructure | 10 | 5.90 → 6.80 | **+0.83** (+0.50, +1.15) | 80% | 70% |

The one treatment that behaves as modelled: both deck and superstructure end near 7.5–8. The substructure also
rises (inspectors rate bearings / seats with the new superstructure).

### BR1 — Structure replacement (285 projects; assumed: every component reset to 8)

| Component | n | Before → after | Net (95% CI) | Improved | 7+ after |
|---|---:|---|---|---:|---:|
| Superstructure | 30 | 5.33 → 6.33 | **+1.22** (+0.60, +1.84) | 47% | 57% |
| Deck | 26 | 5.50 → 6.58 | **+1.33** (+0.71, +1.95) | 54% | 65% |
| Substructure | 30 | 5.83 → 6.10 | +0.38 (−0.01, +0.77) | 23% | 47% |
| Channel | 32 | 6.97 → 6.66 | −0.28 (−0.66, +0.10) | 16% | 59% |

A true replacement should read 8–9 afterwards; about half of these do (7–8) and half stay at 4–6. Of 285
replacement projects only about 40 bridges have ratings both sides under the same BARS — a replaced structure
usually gets a **new BARS**, and the old number goes on being inspected until it is archived, or is never updated.
So the measured +1.2 mixes real replacements with old structures. Where the link is clean, the reset-to-8
assumption is plausible; the problem is identifying the new structure, not the treatment.

### DK1 — Deck replacement (71 projects; assumed: deck reset to 8)

| Component | n | Before → after | Net (95% CI) | Improved | 7+ after |
|---|---:|---|---|---:|---:|
| Deck | 21 | 4.71 → 6.05 | **+1.37** (+0.63, +2.11) | 52% | 48% |
| Superstructure | 21 | 5.71 → 6.00 | +0.37 (−0.11, +0.84) | 29% | 43% |
| Substructure | 21 | 5.62 → 5.71 | +0.29 (−0.12, +0.71) | 24% | 29% |

Half the replaced decks reach 7+; on average the deck gains 1.4 points, to about 6. "Reset to 8" overstates it
for the typical project.

### SP2 — Superstructure rehabilitation (69 projects; assumed: super +2, up to 7)

| Component | n | Before → after | Net (95% CI) | Improved | 7+ after |
|---|---:|---|---|---:|---:|
| Superstructure | 19 | 5.21 → 6.05 | **+0.91** (+0.28, +1.53) | 58% | 42% |
| Deck | 19 | 5.00 → 6.32 | **+1.38** (+0.62, +2.13) | 53% | 47% |
| Substructure | 19 | 4.63 → 5.58 | **+1.13** (+0.25, +2.02) | 53% | 37% |

SP2 collects TheHub codes 36 / 37 / 101 (renovate / rehabilitate), which in practice touch the whole bridge:
the deck gains more than the superstructure. Modelling it as a superstructure-only +2 misses where the benefit
lands.

### SB2 — Substructure rehabilitation (31 projects; assumed: sub +2, up to 7)

| Component | n | Before → after | Net (95% CI) | Improved | 7+ after |
|---|---:|---|---|---:|---:|
| Substructure | 10 | 4.50 → 5.70 | **+1.33** (+0.39, +2.27) | 70% | 30% |
| Superstructure | 10 | 5.60 → 5.70 | +0.13 | 20% | 10% |

About two-thirds of the assumed gain, targeted where it should be.

### SP6 — Clean and paint (193 projects; assumed: super +1 up to 7, held 5 years)

| Component | n | Before → after | Net (95% CI) | Improved | 7+ after |
|---|---:|---|---|---:|---:|
| Superstructure | 75 | 5.59 → 5.96 | **+0.40** (+0.21, +0.60) | 36% | 32% |
| Substructure | 74 | 5.50 → 5.85 | **+0.40** (+0.16, +0.64) | 31% | 24% |
| Deck | 75 | 5.55 → 5.65 | +0.10 (−0.07, +0.26) | 21% | 20% |

The largest and best-measured group. Painting lifts the superstructure (and the painted substructure steel) by
under half a point, not a full point, and the lift has faded by about year 5 (see the path below).

### JT1 — Joint replacement (87 projects; assumed: sub and super held 3 years)

| Component | n | Before → after | Net (95% CI) | Improved | 7+ after |
|---|---:|---|---|---:|---:|
| Superstructure | 35 | 6.06 → 6.60 | **+0.51** (+0.21, +0.80) | 40% | 60% |
| Deck | 35 | 5.77 → 5.94 | **+0.22** (+0.02, +0.42) | 29% | 23% |
| Substructure | 35 | 5.80 → 5.94 | +0.14 (−0.18, +0.45) | 34% | 31% |

More than a hold: the superstructure (bearings, beam ends under the joint) improves about half a point.

### DK4 — Modified PCC overlay (29 projects; assumed: deck +2, up to 8) and DK8 — Membrane with HMA overlay (18; assumed: deck +1 up to 7, held 3 yr)

| Treatment | Component | n | Before → after | Net (95% CI) |
|---|---|---:|---|---|
| DK4 | Deck | 11 | 4.73 → 5.27 | +0.45 (−0.20, +1.11) |
| DK4 | Superstructure | 11 | 5.18 → 5.45 | +0.23 (−0.15, +0.61) |
| DK8 | Deck | 8 | 5.75 → 6.00 | +0.39 (−0.27, +1.05) |
| DK8 | Superstructure | 8 | 6.00 → 6.75 | +0.84 (−0.05, +1.74) |
| DK8 | Substructure | 8 | 6.12 → 6.62 | **+0.65** (+0.06, +1.23) |

Overlays move the deck rating less than half a point on the few bridges we can measure — an overlay covers the
deck's top surface, and the NBI deck rating is driven by the soffit and the concrete below. The assumed +2 for
LMC overlays is well above anything observed.

### Not measurable yet

- **CU2 Culvert rehabilitation** (TheHub 102), **DK2 Deck renovation** (39), **DK5 Deck sealing** and **SP7
  Spot painting** (no TheHub code): no completed, linked project with ratings both sides.
- TheHub codes with no BMS treatment: **35 Other Bridge Work** (23 projects; deck and super about +0.75 net,
  wide intervals), **43 Repair Damage** (16; no clear change), and a handful of one-off codes.

## When the work shows up

Average change in the target component from the bridge's own rating 3–6 years before, by year relative to the
recorded completion (· = fewer than 3 bridges):

| Treatment (component) | −4 | −3 | −2 | −1 | **0** | +1 | +2 | +3 | +4 | +5 | +6 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SP1 (super) | +0.2 | 0.0 | −0.3 | +0.3 | **+2.5** | +1.8 | +3.4 | +1.2 | · | · | · |
| BR1 (super) | 0.0 | 0.0 | +0.6 | +0.5 | **+1.1** | +1.4 | +1.1 | +1.0 | +0.8 | +1.8 | +1.2 |
| DK1 (deck) | 0.0 | 0.0 | −0.3 | +0.3 | **+0.7** | +1.3 | +1.1 | +1.1 | +1.2 | +0.7 | +2.2 |
| SP2 (super) | 0.0 | 0.0 | −0.2 | 0.0 | **+0.4** | +0.4 | +0.5 | +0.5 | +0.3 | +0.6 | +0.2 |
| SB2 (sub) | 0.0 | · | −0.5 | 0.0 | **−0.2** | · | +0.3 | +1.7 | +0.3 | +2.0 | · |
| SP6 (super) | 0.0 | 0.0 | −0.2 | −0.1 | **+0.1** | +0.1 | +0.2 | +0.1 | 0.0 | −0.2 | −0.8 |
| JT1 (super) | 0.0 | 0.0 | −0.1 | −0.1 | **+0.1** | +0.2 | +0.4 | +0.5 | +0.7 | +0.1 | · |
| DK4 (deck) | 0.0 | 0.0 | −0.2 | −0.1 | **0.0** | +0.2 | +0.7 | +0.6 | +0.3 | · | · |
| DK8 (deck) | 0.0 | 0.0 | −0.2 | · | **+0.2** | · | +0.6 | · | +0.8 | · | · |

- **Replacements land in the completion year** (the largest rise is at year 0 for BR1, SP1, DK1, SP2). Some
  appear a year or two *early* (BR1 +0.5 at −2 / −1): the recorded end date lags the work, or the new
  structure is rated before the phase is closed.
- **Maintenance treatments land at the next inspection**, 1–2 years after the end date (paint +1, joints and
  overlays +2, substructure rehabilitation +2–3).
- Ratings often **dip in the year or two before** the work (−0.1 to −0.5 at −2): the inspection that
  documents the distress that triggered the project.
- **Paint fades**: back to the pre-work level by year 5 and below it by year 6.
- How soon a completed project is re-inspected differs by treatment — see the next section.

## Re-inspection after the work — what the policy appears to be

There is no written WVDOT rule in this data, so this is inferred from what happens. For every linked completed
project, the first inspection after the completion date: how many months later it came, whether it came
**earlier than the bridge's regular cycle** (the last inspection before completion plus its inspection interval,
by more than four months), what **type** it was, and whether it moved the treated component. The comparison is
every inspection of bridges with no completed project in the previous three years.

| Treatment | n | Months to next inspection (median) | Early vs. its cycle | Next is special / interim | Next is inventory / initial | Inventory / initial within 2 years | First inspection raises the target rating |
|---|---:|---:|---:|---:|---:|---:|---:|
| SP1 Superstructure replacement | 22 | 14.5 | 27% | 0% | 50% | **82%** | 27% (+0.8) |
| BR1 Structure replacement | 64 | 12.6 | 33% | 17% | 20% | **45%** | 16% (+0.3) |
| DK1 Deck replacement | 37 | 7.5 | 27% | 5% | 27% | **41%** | 33% (+0.8) |
| SP2 Superstructure rehabilitation | 40 | **6.5** | **42%** | **23%** | 12% | 23% | 36% (+0.6) |
| SB2 Substructure rehabilitation | 19 | 7.5 | 16% | 16% | 16% | 16% | **72% (+1.4)** |
| SP6 Clean and paint | 144 | 8.6 | 12% | 7% | 7% | 10% | 28% (+0.3) |
| JT1 Joint replacement | 64 | 9.8 | 14% | 6% | 2% | 2% | 23% (+0.3) |
| DK4 Modified PCC overlay | 14 | 10.5 | 7% | 14% | 7% | 14% | 43% (+0.6) |
| DK8 Membrane + HMA overlay | 11 | 7.2 | 9% | 0% | 0% | 9% | 45% (+0.5) |
| TheHub 35 Other bridge work | 18 | 5.8 | 50% | **39%** | 6% | 17% | — |
| TheHub 43 Repair damage | 12 | 11.7 | 50% | **33%** | 8% | 33% | — |
| *Untreated bridges (base rate)* | *50,117* | — | *22%* | *17%* | *4%* | — | — |

With a 24-month cycle and a completion date at a random point in it, the next routine inspection would come a
median 12 months later; a median well under 12 with a high "early" share points to a deliberate re-inspection.

What each treatment's pattern suggests:

- **SP1 Superstructure replacement — re-inventory the bridge.** Eight in ten get an *Inventory* (initial)
  inspection within two years, twenty times the base rate, and half the first post-work inspections are that
  inventory inspection. It doesn't come quickly (median 14.5 months — likely timed to acceptance or opening
  rather than the construction end date). This matches the NBIS expectation of an initial inspection when a
  bridge is replaced or its structure changes, and it is where the new ratings get set (up to +2.4).
- **BR1 Structure replacement — the same re-inventory rule, blurred by the BARS problem.** 45% show an
  inventory inspection within two years and a third are off-cycle, but only 16% of first inspections raise the
  rating: where the replacement got a new BARS, the old number's "next inspection" is a closing-out of the old
  structure, not the new one.
- **DK1 Deck replacement — often re-inventoried, soon.** 41% get an inventory inspection within two years and
  the next inspection comes a median 7.5 months after completion; a deck replacement changes the structure's
  record (deck type, wearing surface, dimensions), which is likely what triggers it.
- **SP2 Superstructure rehabilitation — an early follow-up look.** The strongest acceleration: next inspection a
  median 6.5 months after completion, 42% off-cycle, 23% special or interim. Consistent with a practice of
  inspecting rehabilitated structures shortly after the work to record the repaired condition (and, where the
  work changes the structure, re-inventorying — 23%).
- **SB2 Substructure rehabilitation — no special rule, but the next inspection records it.** Only modestly
  early, yet 72% of first post-work inspections raise the substructure rating — the repaired substructure is
  simply rated at the next visit.
- **SP6 Clean and paint, JT1 Joint replacement, DK4 / DK8 overlays — no re-inspection policy.** Early and
  special inspections at or below the base rate; the work is picked up at the next routine inspection. Their
  medians of 7–10 months reflect when completion dates fall in the season, not an accelerated visit.
- **Damage repairs (TheHub 43) and other bridge work (35) — a special inspection to verify.** A third or more
  are followed by a *special / interim* inspection, twice the base rate, and half come off-cycle — the pattern of
  an inspection to confirm a repair or lift a restriction.

In short: **replacement-type work is followed by an inventory (initial) inspection, rehabilitation by an early
look, damage repair by a special inspection, and preservation work by nothing beyond the routine cycle.** For
BMS modelling this means the benefit of a replacement or rehabilitation shows in the data within about a year of
completion, while preservation benefits only appear at the next routine inspection (up to two years later).

## What this means for the BMS configuration

The measured effects are an evidence base for `bms.treatments.effects` (BMS → Config). **Applied on
2026-09-27** with `scripts/bms_calibrate_effects.py` (through the configuration workbook, logged in
`bms.config_imports`), as below except DK1, which is set to **reset to 7** rather than +1.5: DK1 triggers on decks
rated 0–4, where +1.5 would leave a replaced deck at 1.5–5.5, and the measured after-rating (about 6–7 whatever
the deck started at) behaves like a reset. `improve` now accepts fractions (+0.5, +1.5). Several of these rest
on small samples:

| Treatment | Now | Suggested from the evidence |
|---|---|---|
| SP1 | deck, super reset 8 | keep; add sub +1 |
| BR1 | all reset 8 | keep (true replacements), but fix the BARS link for replaced structures before judging it |
| DK1 | deck reset 8 | deck +1.5, up to 7 (or reset to 7) |
| SP2 | super +2 up to 7 | super +1, deck +1.5, sub +1, up to 7 |
| SB2 | sub +2 up to 7 | sub +1.5, up to 7 |
| SP6 | super +1 up to 7, hold 5 | super +0.5 and sub +0.5, hold 4 |
| JT1 | sub, super hold 3 | super +0.5, hold 3 |
| DK4 | deck +2 up to 8 | deck +0.5, up to 7 — pending more projects |
| DK8 | deck +1 up to 7, hold 3 | deck +0.5, hold 3 — pending more projects |

Two data fixes would sharpen this more than any modelling:

1. **TheHub bridge links.** About 10% of completed bridge projects name the wrong primary bridge. A report of
   projects whose name doesn't match their bridge (this analysis's link check) would let the programme office
   correct them.
2. **Replacement → new BARS.** Record which structure replaced which, so a replacement's before (old BARS) and
   after (new BARS) can be joined. Today only ~15% of replacement projects can be measured.

## Reproducing

```sh
PYTHONPATH=. venv/bin/python scripts/bridges/treatment_effects.py --out effects.json
```

Reads TheHub live (`bms.hub` project, bridge and code queries), `bms.treatments` from Postgres, and
`qv_nbi_timeseries` / `qv_bridge_decoded` / `qv_bridge_list` from the bridge DuckDB. About a minute. Brgzrd can
repeat or extend it with `hub_sql` (`save_as`) joined to `qv_nbi_timeseries`.
