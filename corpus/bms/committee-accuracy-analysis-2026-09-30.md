# Committee Model — Drop/Timing Accuracy Analysis

**Date:** 2026-09-30 · Data: live app's own files — `nbi_history.json.gz` (34 yr, 9,979 bridges, 1992–2025), `committee_predictions.json.gz` + `committee_summary.json.gz` (built 2026-09-02, 7,889 bridges). Scripts and raw outputs in this folder (`committee_drop_analysis.py`, `committee_timing.py`, `km_timing.py`, `*_results.txt`).

**Question asked:** the headline "MAE 0.157, 97.3% within ±1" is easy when ratings barely move — how accurate is it *actually* at predicting **drops** and **when** a component goes poor?

---

## 1. The ±1 critique is quantitatively correct

Persistence ("predict nothing changes") on their own ground truth, consecutive-inspection pairs (gap 1–4 y, 6 NBI components, 1.03M pairs):

| Baseline | n | exact | within±1 | MAE |
|---|---|---|---|---|
| Predict-no-change, 1992–2025 | 1,032,393 | 92.8% | **99.0%** | **0.101** |
| Predict-no-change, 2015–2025 | 326,000 | 92.0% | **98.6%** | **0.105** |
| Committee's own headline | 63,340 (8 comps) | — | 97.3% | 0.157 |

92–93% of consecutive inspections don't move. The committee's headline is **at or below the do-nothing baseline** on the six NBI components. (Caveat: their backtest covers 8 components — the element-level `bearings`/`joints`/`channel_protection` are noisier — and an unknown horizon mix, so not strictly apples-to-apples. But the headline number alone demonstrates no skill over persistence.)

## 2. Short-horizon drop probabilities: pessimistic ~1.2–2.2×

Fleet mean committee P(rating drops ≥1): **@1yr 0.074, @2yr 0.109** vs the actual per-cycle drop-any rate in history: **5.0%** (1992–2025) / **6.1%** (2015–2025). If 2 yr ≈ one 24-mo inspection cycle, the model overpredicts drops ~1.8–2.2×; at 1 yr (often mid-cycle), up to ~2.4×.

## 3. Timing to poor: good at the margin that matters, too thin from 6–7

Properly censored Kaplan-Meier time-to-poor (≤4) from each starting rating, pooled 6 NBI comps (~1.0M episodes), vs committee mean P(poor):

| current rating | Actual P(poor) @2y / 5y / 10y | Committee @2y / 5y / 10y | verdict |
|---|---|---|---|
| 5 | 0.073 / 0.168 / **0.315** | 0.064 / 0.156 / **0.262** | well calibrated, mildly optimistic (~0.85×) |
| 6 | 0.019 / 0.054 / **0.127** | 0.005 / 0.018 / **0.059** | ~2–4× optimistic; 10-yr tail too thin |
| 7 | 0.004 / 0.013 / 0.037 | 0.001 / 0.006 / 0.018 | ~2× optimistic |
| 8 | 0.002 / 0.005 / 0.011 | 0.001 / 0.002 / 0.007 | close |

Rating-5 components (the programming-critical margin) get a genuinely good timing estimate. From 6–7, the long-horizon tail is thin — consistent with their own GBT model card ("beyond about four years ahead, its answer stops changing") and slow markov/weibull tails dominating the blend there. Only **0.6%** of rating-5 components (and ~0% of 6+) are given a >50% chance of being poor within 10 yr, vs ~32% / ~13% historically.

## 4. Per-bridge discrimination: the real weakness — wrong-signed

Does the model put drop-risk where drops are actually happening? (in-sample check vs each bridge's most recent observed transitions)

- Spearman(recent historical slope, P(drop@1yr)) = **+0.195** — *positive*, i.e. recently-**improving** bridges get more drop-risk, not declining ones.
- Mean P(drop@1yr) by last observed transition: improved **0.131** · stable 0.070 · dropped-1 **0.062** · dropped-2+ 0.065.
- The flagged set (P(drop@1yr) > 0.25, n=789) contains **2.0%** recent decliners — *fewer* than the confident-stable set (P < 0.05): **3.6%**.

### 4b. Direct detection metrics (drop_detection_auc.py)

| Metric | Value | Reading |
|---|---|---|
| AUC of P(drop@1yr) vs "last cycle was a drop" | **0.428** | anti-skill (< 0.5) |
| AUC of P(drop@1yr) vs "last cycle was an improvement" | **0.690** | it detects *improvements*, not drops |
| Flag top 1% by P(drop@1yr): precision / recall | **0.7%** / 0.2% | base rate 2.8% → **4× worse than picking at random** |
| Flag top 5% | 2.2% / 3.8% | below base rate |
| Flag top 10% | 1.9% / 6.8% | below base rate |

Momentum test (is the anti-tracking defensible?): history shows real regression-to-the-mean — P(next cycle drops | last was drop) = **0.8–0.9%** vs stable **5.3%**, so assigning recent droppers *low* P(drop) is defensible. But improved bridges historically drop **less** than stable (3.2% vs 5.3%), while the committee gives them the **highest** P (0.131) — the post-improvement "settling" prior overshoots the data ~4×, and the blend carries no other per-bridge signal.

So its per-bridge signal is essentially **cohort prior + post-improvement settling**, not bridge-specific decline tracking. That's structurally consistent with their own model cards: markov "knows nothing about this particular bridge beyond its current rating and group," weibull likewise, GBT uses static facts (age, material, water), and only the narrative member (weight ~0.21) sees trajectory — not enough to flip the blend. For "which bridge drops next," the model is not currently better than knowing the cohort and current rating.

## 5. `years_to_poor` is dead in production

`"years_to_poor": null` — **all 32,741** bridge×component entries, in both the full predictions file and the summary. The one field that directly answers "when" is never populated; the UI's timing story is implicitly the horizon curves (used above for §3).

---

## Verdict

The user's skepticism is borne out by the app's own data:

1. **Headline accuracy ≈ persistence baseline** (worse on NBI comps, 0.157 MAE vs 0.101).
2. **Drop event rates**: pessimistic ~1.2–2.2× at 1–2 yr.
3. **Timing to poor**: genuinely good from rating 5 (0.26 vs 0.32 at 10 yr), ~2–4× optimistic from 6–7.
4. **Which bridges**: no discrimination on observed decline — flags recently-improved, not recently-declined.
5. **The "when" field is null fleet-wide.**

What remains genuinely good engineering: full PMFs instead of point estimates, per-bridge blend weights, agreement scores, plain-English model cards that even self-diagnose the GBT's 4-year flatness, intervention detection, and backtest metrics shipped with the data. But on the specific question — *predicting when a given bridge drops* — the current blend mostly re-states cohort statistics with tight uncertainty bands. Recommended next steps if they want real drop skill: (a) report metrics on the drop-event subset (recall/precision/AUC at 1–2 cycles), not overall MAE; (b) let trajectory features into the blend (the narrative member already sees them — raise its weight or give GBT the rating history); (c) recalibrate long-horizon tails from 6–7; (d) populate `years_to_poor`; (e) score the persistence baseline in the shipped validation block so the bar is visible.

### Caveats

- Committee forecasts are for the future (built 2026-09-02); true out-of-sample drop skill is only scoreable after inspections land — everything here is in-sample vs history the model could see.
- Their backtest's horizon/component mix is unknown; my persistence baseline covers only the 6 NBI-mapped components (of their 8).
- My KM pools 1992–2025, including the deferred-maintenance 1990s (higher transition rates than today's fleet) — a model trained on recent data would look less optimistic in §3.
- Episodes chained per inspection record are not fully independent; ratings are integer and lumpy (24-mo cycles, inspector noise) — a 0.5-point "expected" change is not observable as such.
