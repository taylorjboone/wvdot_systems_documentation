# The NBI Rating System: What It Is, What It Measures, and Why

A summary of the qualitative-vs-quantitative content of NBI bridge ratings, what inspectors actually record, and why the system looks the way it does.

---

## 1. What the ratings are made of

### Pure inspector judgment (0–9, no measurement thresholds in the spec)
The FHWA *Recording and Coding Guide* describes these in English only:

| Item | Component |
|---|---|
| 58 | Deck |
| 59 | Superstructure |
| 60 | Substructure |
| 61 | Channel / channel protection |
| 62 | Culvert |
| 113 | Scour critical |

A "5" vs a "4" on items 58/59/60/62 is the difference between *Fair* and *Poor* (formerly Structurally Deficient). That threshold gates federal funding, posting decisions, and political optics — and it sits entirely inside one inspector's head.

### Hybrid appraisal ratings (0–9, compared to current AASHTO standards)
Items 67, 68, 69, 71, 72. Inputs are measured geometry; the output code is still discretionary.

### Calculated / formula-driven
- **Sufficiency Rating (0–100)** — formula combining structural adequacy, serviceability, essentiality. *Looks* quantitative, but its largest input (S1, up to 55 pts) is built directly from the qualitative condition codes above.
- **Operating / Inventory Load Rating** (items 64, 66) — output of an LFR or LRFR analysis per AASHTO MBE. Uses measured section properties, but also a condition factor and assumption choices the engineer picks.

### Truly hard numbers
Structure length, deck width, vertical/horizontal clearance, year built, year reconstructed, ADT, skew, number of spans, material/design code, district, owner.

### Approximate split for "condition" questions
- **70–80% qualitative** (the four 0–9 condition codes)
- **15–20% hybrid** (appraisal + load rating)
- **5–10% truly hard** (geometry, age, ADT)

For inventory questions (how long, how wide, when built), it flips — those are nearly all hard numbers.

---

## 2. What inspectors actually record (beyond the 0–9 codes)

Quantitative data **does** exist — most of it just doesn't get submitted to the federal NBI. It lives in the state DOT's bridge file (NBIS 23 CFR 650.313 requires retention):

- **Steel section loss** — UT thickness gauges, calipers; inches or % loss.
- **Concrete spall / delamination / patched area** — chain-drag, hammer sounding; sq ft or % of element.
- **Crack widths** — comparator card / feeler gauges; lengths measured.
- **Scour soundings** — sounding rod, weighted tape, single-beam sonar; cross-sections compared year over year.
- **Pier plumb / tilt / settlement** — surveyed against benchmarks where available.
- **Joint openings** — with ambient temperature recorded for normalization.
- **Bearing displacement and rotation** — against reference marks.
- **Concrete cover / rebar location** — pachometer / GPR (in-depth inspections).
- **Coating condition** — % area in each SSPC class.

The inspector takes all of this and **picks a single 0–9 code**. The qualitative rating is a lossy summary — analog-to-digital conversion that throws away most of the underlying numbers.

### Element-level (AASHTO MBEI / SNBI) — the quantitative half that does get submitted

Since ~2013 nationally, and required across all bridges under SNBI rollout (2022–2024 phased), each element is quantified by condition state:

```
Element 12 Reinforced Concrete Deck — Total qty: 8,400 sq ft
  CS1 (Good):    7,200 sq ft
  CS2 (Fair):    1,100 sq ft
  CS3 (Poor):      100 sq ft
  CS4 (Severe):      0 sq ft
```

This is the most quantitative thing inspectors record at the federal level. Still inspector-observed (not instrumented), but quantities rather than a single digit.

### Photos

- **Required** in the bridge file under the 2022 NBIS final rule.
- **Coverage** specified by BIRM: each elevation, deck surface, each span underside, each pier/abutment face, bearings, joints, documented defects.
- **NOT federally required to be repeatable** from year to year — no fixed photo stations, no standard focal length, no required angle. State DOTs can mandate this; some do (PennDOT, NYSDOT, MnDOT), most don't.
- Defect photos *usually* include a scale (crack card, ruler, chalked dimensions) per BIRM guidance.

### Emerging instrumentation (still rare)
- **UAS / drone inspections** with georeferenced waypoints — repeatable photo points. MnDOT, FDOT, Caltrans, GDOT have programs.
- **Photogrammetry / lidar / structured-light scans** — dimensioned 3D models. Quantitative, repeatable, expensive.
- **Permanent crack monitors** — Avongard-style gauges glued to the structure, read each cycle.
- **Vibrating-wire strain gauges / structural health monitoring** — only on signature spans.

---

## 3. How gameable is it?

Easy in several specific ways:

1. **One-point hop at the SD boundary.** The Coding Guide language for "4" ("advanced section loss") vs "5" ("minor section loss") is fuzzy enough that a sympathetic inspector can hold a deteriorating bridge at 5 indefinitely.
2. **In-house QA.** State DOT inspectors rate bridges owned by the same state DOT. QC is internal. FHWA compliance reviews audit the *program*, not individual ratings.
3. **Load rating assumptions.** Switching LFR↔LRFR, picking a less conservative condition factor, or using more favorable distribution factors can lift a bridge out of posting territory without any physical change.
4. **Sufficiency formula quirks.** Built-in floors and special reductions create thresholds (SR=50, SR=80) that small input changes can cross.
5. **Inspection timing.** Schedule the inspection right after patching, not before. Extend the cycle from 24 to 48 months under risk-based inspection rules.
6. **Inspector anchoring.** The easiest path is to copy last year's code. ~70–85% of transitions are "no change," which is partly real and partly anchoring.

Harder to cheese: geometry, year built, ADT (audited against traffic counts), and any rating ≤ 2 (which triggers reporting requirements).

The quantitative data in the bridge file would catch a lot of cheesing *if anyone independently audited it*. They mostly don't.

---

## 4. Inspector noise — published evidence

FHWA's own 2001 study (Phares et al., FHWA-RD-01-020) had 49 inspectors rate the same bridges:
- Condition ratings within ±1 point of reference only **~68% of the time**.
- ±2 point spreads across inspectors on the same span were common.
- ~95% of variance was *not* explained by the bridge itself.

The WV panel in `nbi_history.json` corroborates this — the `reversal_rate` block in `analysis.py` counts down-then-up sequences in 3 consecutive inspections, a clean proxy for inspector noise (real bridges don't heal).

---

## 5. Why does the system exist in this form?

### Origin: Silver Bridge, 1967
December 15, 1967 — the Silver Bridge across the Ohio River at Point Pleasant, WV collapsed at rush hour. 46 dead. A single eyebar in the suspension chain had an undetected fatigue crack from manufacture in 1928. No standards required anyone to look for it.

Congress passed the Federal-Aid Highway Act of 1968 → FHWA wrote NBIS in 1971. Mission was narrow and explicit: **find bridges about to kill people, before they kill people.** Not asset management. Not life-cycle optimization. Triage.

### The scale problem
- ~620,000 bridges in inventory.
- ~90,000 inspections per year.
- ~5,000–7,000 certified inspectors nationally.

The math forces something cheap and fast. "Experienced human walks the bridge and assigns a 0–9 code" is what cheap-and-fast looked like in 1970s technology. Once you commit to that, you've committed to inspector-driven, categorical, noisy, and gameable.

You get triage. You don't get management.

### Federalism
FHWA can set minimum standards. It can't dictate how 56 reporting agencies (50 states + DC + PR + territories + federal lands + DoD) run their day-to-day programs — what cameras to buy, whether to install fixed photo stations, how to train inspectors. The lowest-common-denominator data is what you can demand from everyone.

### What the system actually does now

1. **Triage, as designed.** SD share has dropped from ~22% (1992) to ~6.8% (recent). Population-level signal is real even when individual ratings are noisy.
2. **Federal funding allocation.** Sufficiency rating became the political currency of the Highway Bridge Program. Changing it means redistributing money, which is politically expensive.
3. **Longitudinal data.** 30+ years of consistent-ish format is statistically useful in aggregate. The WV panel is interesting *because* the methodology hasn't changed since 1992.
4. **Public accountability theater.** "X% of bridges are structurally deficient" is a blunt but functional lever for moving infrastructure money.

### What it isn't
- A predictive maintenance system. (BMS like AASHTOWare BrM is layered on top, using element-level data.)
- A risk model. (Sufficiency rating ≠ probability of failure.)
- An engineering record. (Load rating calcs, repair drawings, scour analyses live in the state's bridge file.)
- Cheese-proof.

### The honest summary

The system was built when computing was expensive, instruments were heavy, and the bar was "no more Silver Bridges." It cleared that bar. It hasn't been redesigned for the world where computing is free and we'd like to manage a multi-trillion-dollar asset class with something better than a vibe check. SNBI and element-level data are chipping at this, but the headline metric is still the 1970s system — because the 1970s system is what 50 state DOTs know how to staff and what Congress knows how to read.

It catches the bridge that's about to fall down. Most of the time. Eventually. That was the original deal, and that's what it still delivers.

---

## 6. Implications for modeling the WV panel

(`analysis.py` is already set up for most of this.)

- The persistence baseline ("predict same as last year") is hard to beat for next-year regression on items 58–60, because ~70–85% of transitions are "no change."
- Big-drop (≥2) events are a mix of real deterioration and inspector handoff/recalibration. Hard to separate without inspector-ID metadata, which NBI doesn't publish.
- Up-jumps of +2 are reliable rehab signals; +1 up-jumps are a mix of real maintenance and noise.
- Treat sufficiency rating as a *partially endogenous* feature, not ground truth — it's a function of the condition codes you're trying to predict.
- Reversal rate by component is the cleanest available noise floor.
