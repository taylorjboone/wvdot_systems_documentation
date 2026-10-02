# NBI Rating: Qualitative vs. Quantitative Components

## TL;DR
The headline ratings — the 0-to-9 component condition codes that drive "Poor / Fair / Good" and Structurally Deficient status — are **almost entirely qualitative inspector judgment** with no measurement thresholds in the spec. The hard numbers (length, width, ADT, year built, load ratings) are real measurements but contribute relatively little to the *condition* story most people care about. The system is moderately easy to cheese, and there is published evidence that it routinely is.

---

## 1. What's in an NBI record, by data type

### Pure qualitative (inspector eyeball, 0–9 integer)
The FHWA *Recording and Coding Guide* defines these with English descriptions only — no measured thresholds, no required instruments:

| Item | What it is |
|---|---|
| 58 Deck | "Minor cracking", "advanced section loss", etc. |
| 59 Superstructure | Same descriptive language |
| 60 Substructure | Same |
| 62 Culvert | Same |
| 61 Channel / channel protection | Judgment on scour, debris, alignment |
| 113 Scour critical | Engineering opinion of foundation vulnerability |

A "5" vs a "4" on any of items 58/59/60/62 is the difference between *Fair* and *Poor* (formerly Structurally Deficient). That boundary controls federal funding eligibility, posting decisions, and political optics — and it sits entirely inside one inspector's head.

### Hybrid appraisal ratings (0–9, but compared to current design standards)
Items 67 (structural evaluation), 68 (deck geometry), 69 (underclearances), 71 (waterway adequacy), 72 (approach alignment). Inspector compares measured geometry to current AASHTO standards and picks a code. Inputs measurable, output still discretionary.

### Calculated / formula-driven
- **Sufficiency Rating** (0–100): formula combining S1 structural adequacy, S2 serviceability, S3 essentiality. Looks quantitative — but S1 is *built from the qualitative condition ratings above*. Garbage in, garbage out.
- **Operating / Inventory Load Rating** (items 64, 66): output of an LFR or LRFR analysis per AASHTO MBE. Uses measured section properties but also a "condition factor" the inspector/engineer picks, and assumption choices (HS-20 vs HL-93, distribution factors, deterioration reductions).

### Genuinely hard numbers
Structure length, deck width, vertical/horizontal clearance, year built, year reconstructed, ADT, skew, number of spans, material/design code, district/owner. These are measured or administrative and not really up for debate.

### Status flags
Posted, closed, open (item 41 / 103). Factual *in principle*, but the *decision* to post is upstream of the load rating, which is upstream of the condition ratings — so subjectivity propagates.

---

## 2. Rough split for the rating that matters

For the "is this bridge in good shape" question:

- ~**70–80% qualitative** — the four 0–9 condition codes drive Poor/Fair/Good classification and feed the sufficiency formula's largest term (S1, up to 55 points).
- ~**15–20% hybrid** — appraisal ratings and load rating, both of which incorporate inspector/engineer judgment via condition factors and standard-comparison codes.
- ~**5–10% truly hard** — geometry, age, ADT.

For administrative inventory questions (how long, how wide, when built) it flips — those fields are nearly all hard numbers.

---

## 3. Evidence that the qualitative part is noisy

FHWA's own 2001 study (Phares et al., FHWA-RD-01-020) had 49 inspectors rate the same bridges:

- Condition ratings were within ±1 point of the reference only ~**68% of the time**.
- Spread of ±2 points across inspectors on the same span was common.
- ~95% of variance was *not* explained by the bridge itself.

Your WV panel (1992–2025, all bridges in `nbi_history.json`) is well set up to corroborate this — the `reversal_rate` block in `analysis.py:122-139` counts down-then-up sequences in 3 consecutive inspections, which is a clean proxy for inspector noise (a real bridge does not heal). Across deck/super/sub, expect reversal rates in the low-to-mid single-digit percent — small per-transition but huge in aggregate, and asymmetric: a single bad day can drop a bridge into SD and cost a state federal dollars.

---

## 4. How easy is it to cheese?

**Easy, in several different ways:**

1. **The one-point hop at the SD boundary.** Going from 5 → 4 reclassifies a bridge as Poor. Going 4 → 5 reclassifies it back. The Coding Guide language for 4 ("advanced section loss") vs 5 ("minor section loss") is genuinely fuzzy. A friendly inspector reading "minor" generously can hold a deteriorating bridge at 5 indefinitely. Several state-level audits (incl. OIG reports on TX, PA) have flagged this exact pattern.

2. **In-house QA.** State DOT inspectors rate bridges owned by the same state DOT. QC is internal. FHWA does compliance reviews of the *program*, not re-inspections of individual bridges. The Phares study itself was only possible because FHWA brought outside inspectors to a controlled site.

3. **Load rating assumptions.** Switching from LFR to LRFR, picking a less conservative condition factor (φc), or using a higher operating-level lane distribution can lift a bridge out of posting territory without touching a stone of concrete.

4. **Sufficiency formula quirks.** The formula has built-in floors and special reductions; small changes to inputs near a threshold (especially the ADT / detour-length terms in S3) can move a bridge across the SR=50 / SR=80 lines that gate HBP funding eligibility.

5. **Inspection cadence and timing.** NBIS allows 24-month routine cycles (or 48 for good-condition bridges under risk-based inspection per the 2022 final rule). Timing an inspection right after a deck patching project legitimately bumps ratings; doing it before — or skipping the post-storm/post-scour special inspection — keeps numbers high.

6. **Element-level (SNBI) is harder to cheese but not used as the headline.** Counting square feet of CS3 spalling is more falsifiable, but the public-facing "Poor" classification and the federal funding formulas still key off the 0–9 component codes.

**Harder to cheese:**

- Geometry, year built, ADT (AADT is audited against traffic counts).
- Closure status once a bridge is physically closed.
- A catastrophic-defect rating (≤2): once written, it triggers reporting requirements and is hard to walk back without documented repairs.

---

## 5. What this means if you're modeling this data

(`analysis.py` is already set up to surface most of this.)

- The persistence baseline ("predict same as last year") will be surprisingly hard to beat for next-year regression on items 58–60, because ~70–85% of transitions are "no change" — which is partly real and partly inspector anchoring on the prior rating. Anchoring is itself a form of cheesing: easier to copy last year's code than to fight about it.
- Big-drop (≥2) events look like real deterioration *or* an inspector handoff/recalibration. Hard to separate without inspector-ID metadata, which NBI doesn't publish.
- Up-jumps of +2 in one cycle are reliable rehab signals; +1 up-jumps are a mix of real maintenance and noise.
- Treat sufficiency rating as a *partially endogenous* feature, not ground truth — it is a function of the qualitative codes you're trying to predict.

---

## Bottom line

The NBI condition story is mostly a 1–2 person opinion encoded as a single digit, lightly audited, with formula-based downstream metrics that look quantitative but are anchored on that opinion. The system survives because (a) most inspectors are conscientious and (b) statistical aggregation across ~620k bridges washes out a lot of noise. But for any individual bridge near a threshold, it is very gameable, and there is no realistic way to detect cheesing from the published data alone without a parallel independent inspection program — which doesn't exist at scale.
