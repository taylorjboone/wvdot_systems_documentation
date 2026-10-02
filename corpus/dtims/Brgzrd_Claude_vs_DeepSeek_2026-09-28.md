# Brgzrd: Claude Sonnet 5 vs DeepSeek V4.1 Flash

*2026-09-28 · A/B evaluation of the Bridge Wizard's model*

## Bottom line

- **Accuracy on questions with one right answer:** a tie.
  - Claude: 39 of 40 correct.
  - DeepSeek (`xhigh`): 36 of 40 correct and 4 partial.
- **Quality on the 13 real questions users asked:** DeepSeek's answers were judged better.
  - The Claude Opus judge preferred DeepSeek on 10 questions and Claude on 1; 2 split.
  - The DeepSeek judge preferred DeepSeek on 11; 2 split.
  - DeepSeek did deeper, more complete analyses. Claude made more mistakes in what it concluded from its own queries.
- **Cost:** DeepSeek is **about 14× cheaper** on real questions ($0.06 against $0.83 per answer) and about 5× cheaper on simple ones.
- **Speed:** DeepSeek is **much slower**.
  - Real questions: median **20 minutes** against **2.5 minutes**.
  - Simple questions: 53 s against 13 s.

  That is the main cost of switching.
- **Recommendation:**
  - DeepSeek is good enough to answer Brgzrd questions, and far cheaper.
  - Its speed was the blocker for everyday use, and the follow-up experiments below fixed most of it.
  - At `low` effort, with its own "work efficiently" instructions, DeepSeek answers heavy questions in about 4 minutes instead of about 20. It still beat Claude on 7 of 8 blind judgements, at about a sixtieth of Claude's cost.
  - Those are now DeepSeek's defaults, switchable on **System → Brgzrd**.

## What was compared

| | Claude | DeepSeek |
|---|---|---|
| Model | `claude-sonnet-5` (Anthropic API) | `accounts/fireworks/models/deepseek-v4p1-flash` (Fireworks, US-hosted, zero data retention) |
| Effort | `xhigh` (Brgzrd's production setting) | `xhigh` (plus 20 runs at `max`, see below) |
| Price, $ per million tokens | input 2.00 · cache write 2.50 · cache read 0.20 · output 10.00 | input 0.22 · cached input 0.007 · output 0.66 |

Both models got **the same system prompt, the same tools and the same data**:
- **Tools:** Brgzrd's own tools, run by its own dispatch code (`bridges/wizard/brigzard.py`).
- **Data:** the AssetWise bridge database, plus live TheHub and MMS.
- **Only the model changed.**
- **Tool loop:** up to 50 tool calls per question and 64,000 output tokens per model call, as in production.
- **Concurrency:** four questions ran at a time for each model.

The prompt used was the one before the 2026-09-28 prompt changes (column types, worked queries and effort rules), so neither model had those.

### Questions

- **Gold set:** 20 questions with answers I computed and checked against the database, each run twice per model (40 runs per model).
  - 2 single-bridge lookups.
  - 11 counts and aggregates with the scope rules: Poor by district, deck-area shares, inspections in 2025, top inspector, inspection cycles.
  - 5 multi-step questions: element condition states, the top 20 bridges by traffic, InfoBridge freeze-thaw, a correlation, deck-area Poor by district.
  - 2 TheHub/MMS money questions.
- **Real set:** 13 questions people asked Brgzrd on mmsdev, run once per model. Two follow-ups that need the previous turn were left out. They include:
  - Poor by district with a chart;
  - the "hard truth" in the data;
  - inspection narratives;
  - TheHub treatment outcomes by bridge type;
  - MMS cost by activity;
  - inspection accomplishments;
  - inspector workload;
  - treatment classification and lag;
  - a bridge with recurring issues;
  - 12 inspections in one day.

### Grading

- **Gold set:** Claude Opus 5.5 compared each final answer with the verified value and its tolerance, and graded it CORRECT, PARTIAL, WRONG or NO_ANSWER.
- **Real set:** blind pairwise judging.
  - **What the judge saw:** the question, both final answers labelled A and B, and each run's tool trace (the SQL and the first 1,200 characters of every result).
  - **Scores:** correctness (are the numbers backed by its own results, was the logic right), completeness and usefulness, 1–10 each, plus a winner.
  - **Bias controls:** every pair was judged twice with A and B swapped, to cancel position bias. Two different judges, Claude Opus 5.5 and DeepSeek itself, check for self-preference.

## Results

### Gold set: questions with one right answer

| | Claude Sonnet 5 | DeepSeek V4.1 Flash |
|---|---|---|
| Correct | **39 / 40** | **36 / 40** |
| Partial | 1 | 4 |
| Wrong or no answer | 0 | 0 |
| Score (partial = ½) | 98.8% | 95.0% |
| Median / mean time | **13 s / 16 s** | **53 s / 107 s** (slowest 11 min) |
| Cost per answer | $0.040 | **$0.0085** |
| Tool calls per answer | 2.0 | 8.4 |
| Tool calls that errored | 5 | 31 (all recovered) |

**The partials:**
- **Claude, 1 partial:** county from the BARS prefix. It used the county-code field instead and got 508, not 511.
- **DeepSeek, 4 partials:**
  - **County:** used `county_name`, which is blank for about 1,100 bridges, and got 440.
  - **Truss share:** led with 58.3% measured over rated trusses only, instead of 49.6% over all trusses.
  - **Deck area Poor:** its D10 headline was 29.0% where the answer is 16.6%, though the other two districts and the order were right.
  - **Element 12 condition state 4:** led with 437 sq ft (a different definition), giving the right 1,471 only as an alternative.

**DeepSeek at `max` vs `xhigh`, on the same 20 gold runs:**

| | Correct | Median time | Cost per answer |
|---|---|---|---|
| `max` | 20 / 20 | 62 s | $0.0096 |
| `xhigh` | 18 / 20 | 39 s | $0.0068 |

Max effort bought a little accuracy for about 50% more time.

### Real questions: blind pairwise

| Judge | Judgements won (26) | Questions won, both orders agreeing (13) | Mean scores, Claude | Mean scores, DeepSeek |
|---|---|---|---|---|
| Claude Opus 5.5 | DeepSeek 22 · Claude 4 | DeepSeek 10 · Claude 1 · split 2 | 6.5 / 6.2 / 6.4 | **7.2 / 8.9 / 8.2** |
| DeepSeek V4.1 | DeepSeek 24 · Claude 2 | DeepSeek 11 · split 2 | 7.4 / 7.3 / 7.4 | **8.2 / 9.1 / 8.9** |

*Mean scores are correctness / completeness / usefulness, 1–10.*

**Why the judges preferred DeepSeek.** I checked their reasons against the answers.

- **Poor by district (R02):** Claude's table shows District 10 with 187 Poor bridges, but its text says District 4 (184) has "the single largest raw count". I confirmed this in the answer.
- **Inspection accomplishments (R10):** Claude ignored the "independent task order" half of the question.
- **Inspections vs MMS work (R13):** Claude concluded accomplishments are "essentially never logged" after checking the wrong field. DeepSeek joined inspections to MMS work lines and named the districts that lag.
- **TheHub treatments by bridge type (R07):**
  - Claude used only each project's primary bridge, so every other bridge on multi-bridge projects was dropped.
  - DeepSeek covered route-segment bridges and matched replaced bridges to their successors by location.
- **12 inspections in one day (R17):**
  - Claude guessed at the reason.
  - DeepSeek showed it with evidence: the report creation dates (a March 2025 backfill), the TheHub replacement projects, and a statewide check of how rare such days are.
- **Interesting inspection narratives (R05, R06):** DeepSeek gave more verified excerpts. Claude mislabelled a demolition as a collapse and pinned one quote to the wrong report.

**Where Claude won:**
- **Longest bridge (R11), a short question:** DeepSeek left a top-5 bridge out of its table and misattributed ratings.
- **"Hard truth" (R04):** the Opus judge was split. Claude's figures were better grounded; DeepSeek's were broader but partly unverifiable.

**DeepSeek's own recurring faults:**
- scope claimed but not filtered (e.g. "WVDOT-owned" with no ownership filter);
- loose date matching;
- inconsistent summary percentages;
- numbers the judge could not verify because the trace was cut off. With 30+ tool calls, later calls fell outside the 40,000-character trace. That's a limit of the harness, not necessarily fabrication.

### Speed, cost and tokens

| Per answer | Claude, gold | DeepSeek, gold | Claude, real | DeepSeek, real |
|---|---|---|---|---|
| Median time | 13 s | 53 s | **2.5 min** | **19.9 min** |
| Slowest | 43 s | 11.4 min | 7.3 min | 25.6 min |
| Cost | $0.040 | $0.0085 | **$0.83** | **$0.062** |
| Prompt tokens (cached share) | 112k (97%) | 198k (94%) | 652k (52%) | 773k (87%) |
| Output tokens (reasoning) | 1.1k | 7.2k (5.3k) | 14k | 53k (42k) |
| Model calls | 3.0 | 5.8 | 9.3 | 11.1 |
| Tool calls | 2.0 | 8.4 | 14.7 | 30.9 |
| Totals (13 real questions) | | | $10.83 | $0.80 |

- **Why Claude's real answers are expensive:** Brgzrd caches only the system prompt. Each step resends the growing tool results uncached, so about half of Claude's prompt tokens on long analyses are full price. Fireworks caches the repeated conversation automatically, so 87% of DeepSeek's are cached at $0.007/M.
- **Why DeepSeek is slow:** it takes about twice as many tool calls and writes about 4× the output, mostly reasoning, and each Fireworks call is slower to start.
- **Claude's cost is slightly flattering:** the runs were back to back, so Claude almost never paid the cache write for the system prompt (about $0.09 after 5+ idle minutes).

### Real-question detail

| Question | Claude min | DeepSeek min | Claude $ | DeepSeek $ | Opus judge |
|---|---|---|---|---|---|
| R02 Poor by district + chart | 0.4 | 1.4 | 0.05 | 0.006 | DeepSeek |
| R04 deepest hard truth | 3.0 | 20.1 | 0.61 | 0.08 | split |
| R05 bridge types with the wildest narratives | 3.4 | 19.9 | 2.04 | 0.09 | DeepSeek |
| R06 most interesting narratives | 2.5 | 16.5 | 1.34 | 0.08 | DeepSeek |
| R07 what each TheHub treatment gets us, by type | 7.3 | 22.0 | 3.42 | 0.11 | DeepSeek |
| R09 MMS cost by activity code | 1.4 | 22.1 | 0.21 | 0.09 | DeepSeek |
| R10 inspection accomplishments | 3.7 | 25.6 | 0.93 | 0.10 | DeepSeek |
| R11 longest bridge | 0.2 | 2.1 | 0.03 | 0.02 | **Claude** |
| R12 top inspector and cadence | 0.7 | 2.9 | 0.13 | 0.01 | DeepSeek |
| R13 inspections with MMS work, offending districts | 3.9 | 21.8 | 0.69 | 0.09 | DeepSeek |
| R14 treatments classified to BMS, lag | 4.3 | 20.5 | 0.66 | 0.07 | split |
| R16 a bridge that keeps having issues | 1.5 | 7.6 | 0.53 | 0.03 | DeepSeek |
| R17 12 inspections in one day | 1.3 | 13.3 | 0.17 | 0.10 | DeepSeek |

## Follow-up: DeepSeek prompt and effort experiments

**Why:** DeepSeek's slowness came from long reasoning before every step. The experiments tested two changes:
- **Effort:** `xhigh`, `high`, `medium`, `low`.
- **Prompt:** the current prompt (A), and the current prompt plus a DeepSeek-only "Working efficiently" section (B).

Section B tells DeepSeek to:
- keep its reasoning to a few sentences per step;
- not re-check clean results;
- keep to a query budget: 1–2 queries for a fact, about one per part for an analysis;
- answer once it has the figures.

Both prompts include the 2026-09-28 prompt improvements (column types, worked queries).

### Stage 1: 10 new held-out questions with verified answers

| Prompt | Effort | Correct | Median / slowest | Reasoning tokens | Tool calls |
|---|---|---|---|---|---|
| A | `xhigh` | 9/10 | 28 s / 456 s | 4,685 | 7.5 |
| A | `high` | 10/10 | 17 s / 59 s | 331 | 3.3 |
| A | `medium` | 9/10 | 15 s / 82 s | 331 | 4.0 |
| A | `low` | 10/10 | 15 s / 38 s | 273 | 3.2 |
| B | `xhigh` | 10/10 | 21 s / 72 s | 1,114 | 2.8 |
| B | `high` | 9/10 | 14 s / 62 s | 263 | 3.0 |
| B | `medium` | 9/10 | 14 s / 36 s | 157 | 2.7 |
| **B** | **`low`** | **10/10** | **15 s / 28 s** | 176 | 2.4 |

- The few partials are all one borderline answer: the busiest bridge is "unrated" but was headlined as "Fair" from older ratings.
- Effort sets the reasoning volume: `high` or lower cuts it 5–25× with no accuracy loss.
- Section B trims tool calls further.

### Stage 2: four heavy real questions

The questions were R05 (narratives), R07 (TheHub treatment outcomes), R10 (inspection accomplishments) and R13 (inspections vs MMS work). Each answer was blind-judged against Claude's by Claude Opus 5.5, both orders.

| Prompt | Effort | Beat Claude (8 judgements) | Median time | Cost per answer |
|---|---|---|---|---|
| **B** | **`low`** | **7 – 1** | **4.3 min** | $0.031 |
| B | `high` | 4 – 4 | 3.8 min | $0.024 |
| A | `high` | 4 – 4 | 5.1 min | $0.033 |
| B | `xhigh` (R07 only) | 2 – 0 | 27 min (79k reasoning tokens) | $0.125 |
| A | `xhigh` (the original eval) | 8 – 0 | ~21 min | $0.09 |
| Claude Sonnet 5 `xhigh` (the original eval) | — | ~3.6 min | ~$1.87 |

**Result:** prompt B at `low` effort is the sweet spot.
- It is about as fast as Claude (median 4.3 min against about 3.6) and about 60× cheaper.
- It was judged better than Claude on 7 of 8 judgements.
- It is nearly as good as the 20-minute `xhigh` runs.

**Where lower effort lost rigour:** the TheHub treatment question (R07). Claude won it against both `high` settings and split it with `low`. The judges cited Claude's WVDOT-owned filter and its exclusion of future-dated completions. Maximum effort remains available when rigour on a hard analysis matters more than time.

**Adopted:**
- DeepSeek's default effort is now `low`.
- Its extra instructions default to section B (`bridges/wizard/settings.py`).
- Claude keeps `xhigh` and no extra instructions.
- Both are editable on System → Brgzrd.

Scripts: `exp.py`, `grade_exp.py`, `judge_exp_real.py`, `questions_heldout.json`. Results are in `results/exp/`, with grades in `grades/exp_heldout.jsonl` and `grades/exp_real.jsonl`.

## Caveats

- **Small sample:** 13 real questions, run once each. The direction is clear across both judges and both orders, but the size of the gap isn't precise.
- **The judges are models:**
  - The DeepSeek judge could favour its own answers; the Opus judge could favour Claude's.
  - Both preferred DeepSeek, and I verified several of the cited Claude errors.
  - Judges may reward length. DeepSeek's answers were longer (median about 4,900 against 4,400 characters, up to 2.4× on one question), but the cited reasons were concrete errors and missed parts, not length.
- **Timing ran four questions at a time on Fireworks serverless**, which may add queueing. Time a few questions one at a time before relying on the 7× figure.
- **Old prompt:** the evaluation ran before the prompt changes. Those target exactly the faults seen here: text-typed columns, guessed columns, over-verifying simple questions, unrequested charts. They should cut DeepSeek's tool calls and time, and help Claude too.
- **Local data:** the nightly `bridge_spend` table is empty in the dev database, the same for both models.

## Next steps

1. **Time DeepSeek one question at a time,** at `xhigh` and `high`, on a few real questions, to separate Fireworks queueing from model speed.
2. **Rerun both models on the new prompt** with a fresh held-out gold set. The new worked queries overlap several of the current gold questions.
3. **Consider a split:**
   - Claude for quick questions (seconds, cheap on short answers).
   - DeepSeek for deep analyses, where a few more minutes buys a better answer at a fourteenth of the cost.

   This needs a simple rule for choosing the model per question; the current setting is one model for everything.
4. **Watch the live numbers** on System → Brgzrd (cost, time, ratings by model) after any switch.

## Files

In `dtims_docs/brgzrd-model-eval-2026-09-28/`:

| Files | What they are |
|---|---|
| `harness.py` | The A/B runner |
| `judge.py` | The graders |
| `questions.json`, `logged_questions.json` | The gold questions with verified answers, and the real questions |
| `results/*.jsonl` | Every run: answer, tool trace, tokens, timing, cost |
| `grades/*.jsonl` | Every grade and judgement with its reasons |
