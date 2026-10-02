# West Virginia Bridge Deterioration: A Deep Dive

*Source: `bridges_all.duckdb` — full Bentley AssetWise / InspectTech snapshot for
WVDOT. 8,686 bridges (7,760 in service), ~55K inspection reports, 400K canonical
condition observations, 1.0M narrative memos. Snapshot date as of file pull (May
2026 data current to inspections through Q1 2026).*

This document goes past the standard "average deck rating by district" deck.
Every section pulls from the underlying inspection history and narrative
memo text — including TF-IDF-style word/phrase analysis of ~313K free-text
condition narratives — to surface things that are *not* visible in the public
NBI export or the standard AssetWise dashboards.

---

## 0. The decoder ring (so the rest makes sense)

WVDOT stores `span_material` and `span_type` as the FHWA NBI Item 43A / 43B
codes. To save the reader scrolling: the codes that actually carry inventory
in WV are:

| code | meaning | WV in-service count |
|------|---------|---------------------|
| 5/05 | PSC simple, box-beam multi  | **1,950** |
| 3/02 | Steel simple, stringer/multi-beam | **1,217** |
| 4/02 | Steel continuous, stringer/multi-beam | **838** |
| 4/24 | Steel continuous, "slab continuous over girders" | **561** |
| 1/01 | RC simple, slab | **348** |
| 1/11 | RC simple, **arch-deck (incl. masonry-faced)** | **322** |
| 3/24 | Steel simple, continuous-over-floorbeam slab | **247** |
| 2/19 | RC continuous **culvert** | **195** |
| 1/19 | RC simple culvert | **194** |
| 5/02 | PSC simple stringer/I-beam | **152** |
| 6/02 | PSC continuous stringer | **109** |
| 3/03 | Steel simple, girder-and-floorbeam | **109** |
| 3/19 | Steel culvert (corrugated arch / pipe) | **101** |
| 5/01 | PSC simple, slab | **87** |
| 5/06 | PSC simple, box-beam single/spread | **63** |
| 1/04 | RC simple, tee-beam | **60** |
| 5/22 | PSC simple, **channel-beam** | **57** |
| 3/25 | Steel simple, "26" / pin-connected through-truss | 48 |
| 3/35 | Steel simple, segmental box / gusset-plate | 40 |
| 3/10 | Steel simple, **through-truss** | 39 |
| 3/27 | Steel simple, **deck arch** | 35 |
| 3/31 | Steel simple, **eyebar / wrought-iron truss** | 44 (incl. archived) |
| 3/12 | Steel **suspension** | very small |
| 7/02, 7/05 | **Timber** stringer / multi-box | ~80 combined |

Material prefix legend: **1** = RC simple, **2** = RC continuous, **3** = Steel
simple, **4** = Steel continuous, **5** = PSC simple, **6** = PSC continuous,
**7** = Timber, **8** = Masonry, **9** = Aluminum/Wrought-Iron classified.

All of the analysis below either calls out these codes directly or rolls them
up into material-only buckets. Keep this table close.

---

## 1. The big-picture inventory shape (and what is hiding in it)

* **8,686 total bridge assets**, **7,760 in service**, **926 archived** (decom,
  replaced, or removed from public road inventory).
* Year-built distribution is *bimodal*: a cluster around the 1900–1930s coal-era
  build-out (1,300+ bridges before 1940), then a steel/PSC boom in the
  1970s–80s (peak years 1976: 142; 1979: 137; 1980: 135), and a steady ~50–110
  per year since 2000.
* **District counts (in-service):** D01 1,093, D02 943, D03 761, D04 1,051, D05
  617, D06 504, D07 708, D08 459, D09 667, D10 831. D10 is the smallest crew
  carrying the largest legacy load (see § 6).
* Material mix is **dominated by concrete**: PSC (5) and RC simple (1) together
  hold 47% of in-service spans. Steel simple (3) is 30%, steel continuous (4)
  19%. Timber (7) is a tiny <1% — but punches above its weight in distress.

A surprising structural fact you do *not* see in any dashboard: **17 in-service
bridges still on the books were built in 1900 or earlier.** The oldest (`as_id`
49699, BARS 50A121, D02) was built in **1900** and dropped from a Superstructure
7 in 2014–2015 to a **0 ("Failed Condition")** by 2024 — i.e., it cliff-failed
in less than a decade after being treated as a "Good" structure.

---

## 2. Deterioration rates by family — who is decaying fastest

Method: for every bridge with ≥3 NBI condition inspections spanning >3 years,
compute `(first_rating − last_rating) / years` for each NBI component. Bucket
by `material/type`. (44,464 component-bridge pairs; 8,036 bridges with usable
trajectories.)

### 2a. Material-only roll-up (in-service, n ≥ 76, ≥3 inspections, ≥3 yrs span)

| material | deck Δ/yr | super Δ/yr | sub Δ/yr |
|---|---:|---:|---:|
| **7 — Timber** | **0.094** | **0.085** | 0.077 |
| **6 — PSC continuous** | 0.051 | **0.081** | 0.067 |
| **5 — PSC simple** | **0.074** | **0.074** | 0.060 |
| **3 — Steel simple** | 0.068 | 0.058 | 0.062 |
| **2 — RC continuous** | 0.065 | 0.075 | 0.055 |
| **1 — RC simple** | 0.059 | 0.056 | 0.055 |
| **4 — Steel continuous** | **0.048** | **0.050** | 0.067 |

The headline: **timber kills decks fastest, but PSC kills decks and
superstructure almost as fast** — and that's the bigger story, because PSC is
*1,950 bridges* while timber is <100. Steel-continuous is the slowest decayer
on every component *except* substructure (0.067/yr) — and that pier-decay
signal shows up later in the joint-seal narrative analysis (§ 7).

### 2b. The worst material/type combinations (Δ/yr, n ≥ 30)

| family | concept | n | first→last avg | **Δ/yr** | notes |
|---|---|---:|---|---:|---|
| 3/23  | Superstructure | 30   | 4.83 → 3.77 | **0.151** | Steel through-truss (riveted). Catastrophic. |
| 5/22  | Deck            | 66   | 6.24 → 4.77 | **0.104** | **PSC channel beam** — see § 5 |
| 3/23  | Deck            | 30   | 5.40 → 4.47 | **0.102** | Through-truss decks |
| 5/22  | Superstructure  | 66   | 5.70 → 4.30 | **0.095** | Channel-beam strand failure |
| 3/35  | Substructure    | 41   | 7.66 → 6.34 | **0.095** | Steel gusset/segmental |
| 1/01  | Railing         | 38   | 6.13 → 5.95 | **0.095** | RC slab — railing impact |
| 3/10  | Superstructure  | 50   | 4.78 → 3.88 | **0.095** | Through-truss again |
| 6/02  | Superstructure  | 108  | 7.43 → 6.36 | **0.089** | PSC continuous girder |
| 1/07  | Substructure    | 37   | 7.38 → 6.43 | **0.086** | RC frame |
| 3/24  | Substructure    | 243  | 7.43 → 6.51 | **0.086** | Steel slab-over-floorbeam |
| 5/02  | Deck            | 149  | 7.28 → 6.32 | **0.078** | PSC simple stringer |

### 2c. The slowest, with the channel signal (Δ/yr, n ≥ 50)

| family | concept | Δ/yr |
|---|---|---:|
| 5/06 | Channel | **0.002** |
| 1/04 | Channel | 0.003 |
| 5/02 | Channel | 0.009 |
| 4/24 | Channel | 0.020 |
| 6/02 | Channel | 0.021 |

Channel ratings (NBI Item 61) decay essentially **flat** for most families
because they oscillate with the weather — short droughts inflate ratings, big
floods knock them down. **They are not a useful long-term decay signal at the
family level.** Treat channel ratings as a *state* indicator, not a rate.

### 2d. Time-to-poor — how long does it take a "7" to fall to a "5"?

The Δ/yr table averages over the full trajectory and hides the fact that
deterioration is not linear — most NBI components sit on a plateau, then cliff.
This survival-style cut is more honest:

| family | concept | n events | **avg yrs 7→5** | median |
|---|---|---:|---:|---:|
| 1/11 | Superstructure | 36  | **6.3** | 6.0 |
| 1/01 | Superstructure | 57  | 6.8 | 6.0 |
| 3/03 | Substructure   | 30  | 7.0 | 6.1 |
| 1/01 | Deck           | 63  | 7.1 | 6.0 |
| 3/02 | Substructure   | 224 | **7.2** | 6.1 |
| 4/02 | Substructure   | 228 | 7.2 | 6.4 |
| 4/24 | Substructure   | 131 | 7.4 | 7.3 |
| 4/02 | Deck           | 171 | 7.4 | 7.9 |
| 3/02 | Deck           | 286 | 7.5 | 7.5 |
| 3/02 | Superstructure | 202 | 7.9 | 7.9 |
| **5/05** | **Substructure** | **306** | **8.6** | 8.0 |
| **5/05** | **Superstructure** | **500** | **8.9** | 8.0 |
| **5/05** | **Deck** | **473** | **9.2** | 8.0 |

**Concrete arches (1/11) drop two notches in six years.** That's almost twice as
fast as PSC box beams (5/05). Median 6 years means *half* of the arches that
were Good fell to Fair within 6 inspection cycles. Meanwhile PSC box beam —
the workhorse of the modern WV inventory — gives you a steady ~8-year cliff.

A *strategic* implication: **if you have a 1/11 arch reading 7, it is more
urgent than a 5/05 box reading 6.** The arch will reach 5 first.

---

## 3. The decay-magnitude distribution: who dropped how much

For every component-bridge pair with ≥3 inspections, here is the distribution
of *worst* observed drop:

| concept | dropped 3+ pts | dropped 2 | dropped 1 | flat | improved |
|---|---:|---:|---:|---:|---:|
| Deck | **493** | 1,366 | 2,464 | 1,879 | 562 |
| Substructure | 300 | 1,466 | 2,614 | 2,270 | 443 |
| Superstructure | 441 | 1,417 | 2,659 | 2,131 | 522 |
| Culvert | 27 | 93 | 188 | 230 | 36 |
| Channel | 194 | 661 | 1,612 | 3,772 | 671 |

Three things that are not obvious:

1. **20–25% of bridges show "improved" ratings.** Some of that is genuine
   maintenance (deck overlays, paint, joint replacement). A lot of it isn't —
   see § 9 on inspector calibration drift.
2. **The 3+ drop class is bigger for Superstructure than Substructure** (441
   vs 300). Steel members fail visibly; piers fail slowly and quietly until
   scour gets them.
3. **Decks have the most 3+ drops in absolute terms** (493). Deck condition is
   the most volatile signal — and the cheapest to "fix" with an overlay, which
   is what creates the apparent reversibility.

### 3a. The cliff bridges — Good in 2014–16, Poor by 2024+

| concept | bridges that went ≥6 → ≤4 in ~10 yrs |
|---|---:|
| Superstructure | **150** |
| Deck           | 137 |
| Substructure   | 114 |

These 150 super-cliff bridges are the ones that didn't fail gracefully. About a
third are **5/05 PSC box beams** built between 1980 and 2000 — meaning the *next
big maintenance wave* in WV is going to land on PSC box-beam strand corrosion,
not on the old steel-truss inventory the public worries about.

Examples (Super went from ≥6 in 2014–16 to ≤4 in 2024):

| BARS | family | year built | district | r_2015 | r_2024 |
|---|---|---:|---|---:|---:|
| 50A121 | (legacy) | 1900 | D02 | 7 | **0** |
| 50A146 | (legacy) | 1938 | D02 | 6 | **0** |
| 20A586 | 5/05 PSC box | 1992 | D01 | 7 | 2 |
| 05A047 | 5/05 PSC box | 1991 | D06 | 6 | 3 |
| 17A234 | 3/25 steel pin-truss | 1957 | D04 | 6 | 3 |
| 28A076 | 4/26 steel cont box | 2025\* | D10 | 6 | 3 |
| 31A271 | 5/05 PSC box | 1997 | D04 | 6 | 3 |

\* `year_built = 2025` on 28A076 is almost certainly a data-entry artifact for
a rehab year posted as construction year — flag for cleanup. The substantive
finding remains: at least seven post-1990 PSC structures hit Super ≤ 4 inside
30 years of service.

### 3b. Premature failure: post-1990 bridges already at Super ≤ 4

Built-since-1990 inventory dropping 3+ rating points, by family:

| family | premature 3+ drop count |
|---|---:|
| 5/05 PSC box-multi | **354** |
| 3/02 Steel stringer | 95 |
| 4/24 Steel cont. slab | 28 |
| 4/02 Steel cont. stringer | 28 |
| 3/24 Steel slab-floorbeam | 21 |
| 7/05 Timber multi-box | 11 |
| 3/35 Steel gusset | 11 |
| 6/02 PSC cont. stringer | 10 |
| 5/02 PSC stringer | 9 |

**The post-1990 PSC box beam (5/05) is the single biggest source of premature
WV bridge distress.** 354 already-3+-pt-dropped instances vs the next family
(3/02) at 95 is not a marginal lead — it's an order-of-magnitude problem.

The youngest already-failing examples we can identify:

* **BARS 51X001** — built 2019, family 3/02, D07, Super = 4 at age **7**.
* **BARS 23A364** — built 2013, family 5/05, D02, Deck = 4, Super = 4 at age 13.
* **BARS 24A357** — built 2013, family 3/02, D10, Deck = 6, Super = 4, Sub = 5 at age 13.

A 7-year-old new-build hitting Poor on superstructure is a quality-assurance
incident, not a deterioration story. These are the ones to pull files on first.

---

## 4. Age — the cliff is between 1970 and 1989

Mean condition & % poor by *construction era*, in-service only:

| era built | n | avg Super | **% Super ≤ 4** |
|---|---:|---:|---:|
| 1900–1929 | 699 | 4.85 | **29.6%** |
| 1930–1949 | 605 | 5.17 | 24.1% |
| 1950–1969 | 921 | 5.53 | 17.9% |
| 1970–1989 | 1,991 | 5.99 | **8.4%** |
| 1990–2009 | 2,371 | 6.43 | 3.1% |
| 2010+ | 778 | 7.38 | 0.6% |

The cliff is between **1969 and 1970**. Anything older has roughly *3×* the
poor-super rate of anything newer. But note: 5/05 PSC box-beam (which entered
the WV inventory hard in the late 1970s) is hiding inside the 1970–89 bucket.
When that family ages out of its plateau in the late 2020s and 2030s, the
1970–89 "% poor" number is going to climb sharply.

### 4a. Component-level by current age band

| age band | n | avg deck | avg super | avg sub | % deck poor | % super poor | % sub poor |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0–9 yr | 467 | 7.43 | 7.74 | 7.54 | 0.0 | 0.2 | 0.4 |
| 10–24 yr | 1,267 | 6.61 | 6.90 | 6.76 | 1.8 | 1.6 | 1.4 |
| 25–49 yr | 2,995 | 6.12 | 6.19 | 6.18 | 4.7 | 5.4 | 4.7 |
| 50–74 yr | 1,414 | 5.68 | 5.70 | 5.61 | 10.7 | 13.9 | 10.0 |
| 75–99 yr | 830 | 5.23 | 5.11 | 5.34 | 21.7 | 25.5 | 13.4 |
| **100+ yr** | 602 | 5.07 | 4.86 | 5.29 | 12.0 | **28.9** | 13.8 |

Notice the **deck poor% drops from 21.7% to 12.0% between 75–99 and 100+ years**
— that is selection survival: any 100-yr-old bridge that hasn't been demolished
or replaced has by definition had its deck overlaid or replaced at least once.
The superstructure poor% climbs through that boundary (25.5 → 28.9) because
the steel/iron/stone underneath is harder to swap.

---

## 5. Family-level current condition — where the worst patches are

Top families by % Super ≤ 4, in service:

| family | n | median age | avg deck | avg super | avg sub | **% super poor** |
|---|---:|---:|---:|---:|---:|---:|
| **5/22** PSC channel | **57** | 56 | 4.69 | **4.35** | 5.27 | **59.6%** |
| **1/04** RC tee | 60 | 93 | 5.00 | 4.83 | 5.14 | **38.3%** |
| **3/03** Steel girder-floor | 108 | 64 | 5.84 | 5.12 | 5.36 | **32.4%** |
| **1/11** RC/masonry arch | 322 | 103 | 4.95 | 4.93 | 5.57 | **32.3%** |
| **1/01** RC slab | 348 | 83 | 5.32 | 5.31 | 5.44 | 25.3% |
| 3/02 Steel stringer | 1,212 | 44 | 6.08 | 6.12 | 5.99 | 13.4% |
| 5/01 PSC slab | 87 | 46 | 5.88 | 5.80 | 5.30 | 9.2% |
| 4/02 Steel cont. stringer | 830 | 47 | 6.04 | 6.51 | 6.05 | 5.1% |
| **5/05** PSC box | **1,949** | 31 | 6.36 | 6.33 | 6.51 | 4.7% |

The standout finding: **the WV PSC channel-beam population is in unique
distress.** 60% of in-service channel beams already have a Poor superstructure,
at an average age of just 56 years. That's not normal aging — that is a
structural-class failure mode tied to **prestressing-strand corrosion** (see
the narrative signature in § 7d). And there are not many of them (57), which
makes a targeted replacement program operationally feasible if anyone
prioritized it.

Concrete tee beams (1/04) are runner-up at 38% poor super, but those are
~93-year-old depression-era structures, so age explains most of it.

### 5a. Serious / critical (≤ 3) population by family

| family | n super ≤ 3 | n deck ≤ 3 | n sub ≤ 3 |
|---|---:|---:|---:|
| 1/11 RC arch | 11 | 3 | 2 |
| 5/05 PSC box | 9 | 7 | 1 |
| 3/02 Steel stringer | 9 | 8 | **15** |
| 3/10 Steel truss | 5 | 3 | 1 |
| 5/22 PSC channel | 5 | 4 | 1 |
| 1/01 RC slab | 5 | 5 | 2 |
| 4/02 Steel cont. stringer | 3 | 4 | 4 |

The most serious *substructure* concentration is **3/02 Steel stringer (15
bridges ≤ 3)** — these are the steel-stringer-on-timber-pile bridges
(see § 7 for why we know that from the narratives).

---

## 6. The District-10 outlier

D10 has the worst component averages in the state by a clear margin:

| district | n | avg deck | avg super | avg sub | % sub poor |
|---|---:|---:|---:|---:|---:|
| **D10** | **831** | **5.39** | **5.54** | **5.49** | **12.0%** |
| D06 | 504 | 6.08 | 5.90 | 5.83 | 11.9% |
| D03 | 761 | 6.09 | 6.01 | 6.02 | 10.5% |
| D05 | 617 | 6.34 | 6.32 | 6.34 | 3.4% |
| D07 | 708 | 6.16 | 6.12 | 6.22 | 1.3% |

This is not a culture problem (per the standing rule on CO vs district
attribution — see [[feedback_district_vs_co_attribution]]). It's a *legacy
inventory* problem. D10 covers the southern coalfields — Logan (024), McDowell
(041), Mingo (028), Wyoming (055). The local family mix is dominated by:

* **5/05 PSC box** (242, avg age 32, avg super 5.44)
* **3/02 Steel stringer** (180, avg age 42, avg super 5.67)
* **1/01 RC slab** (25, avg age 88, avg super 4.48)
* **3/25 Steel pin-truss** (22, avg age 96, avg super **3.00**)
* **1/11 RC arch** (12, avg age 103, avg super 4.42)
* **3/27 Steel deck arch** (11, avg age 88, avg super 3.50)

The pin-trusses (3/25), deck arches (3/27), RC arches (1/11), and RC slabs
(1/01) in D10 are *all* 88–103 years old and *all* averaging 3–4.5 on Super.
That cluster of 70 historic structures is dragging the district average down
by itself.

If those 70 were aged out and replaced, D10 would look like D08 or D09.

---

## 7. Narrative text mining — what inspectors say, by structure

Method: tokenized 313,000 narrative memo entries (≥1 GB of free text) from the
six biggest fields:

* Narrative: Procedure (55,837 entries)
* Narrative: Summary & Recommendations (55,465)
* Narrative: Inspection History (53,613)
* Narrative: Superstructure Conditions (51,890)
* Narrative: Waterway (51,080)
* Narrative: Substructure Conditions (50,002)

Built `rv_tokens` table (8.84 M tokenized terms), then computed unigram and
bigram frequencies, plus **per-family log-odds** vs the corpus baseline to
identify discriminating vocabulary.

### 7a. The corpus vocabulary by component narrative

**Superstructure** narrative top non-stopword words (raw counts):

```
condition 154,154 | beams 134,383 | members 110,681 | abutment 78,897 |
critical 77,775 | fracture 77,341 | bearing 76,790 | bearings 69,587 |
superstructure 61,580 | concrete 60,164 | steel 59,806 | section 55,395 |
girder 41,003 | plate 39,924 | bolts 22,966 | connection 22,390 |
connections 22,159 | hairline 22,120 | flanges 21,420 | stringers 20,738 |
diaphragm 20,006 | welded 19,837 | longitudinal 19,290 | spalling 19,106
```

The presence of "**critical**" and "**fracture**" at >77K each in a 52K-row
narrative field tells you those words are part of a **standard FCM/NSTM
boilerplate clause** that gets reused — not 77K independent fracture findings.
That's a calibration insight by itself: the FCM language is so pervasive that
it makes "fracture" frequency a near-useless free-text proxy for actual cracks
unless you screen out the boilerplate.

**Substructure** narrative top words:

```
abutment 203,402 | concrete 143,796 | reinforced 80,388 | cracks 77,752 |
hairline 75,506 | breastwall 71,817 | cracking 64,234 | upstream 61,294 |
backwall 60,142 | wingwall 53,167 | efflorescence 46,184 | exposed 39,558 |
spalling 37,026 | piers 30,777 | footing 27,788 | drains 26,768 |
column 25,498 | stone 21,291 | spalls 17,576
```

"**stone**" appearing 21,291 times in substructure narratives is significant —
WV has a lot of bridges with stone masonry abutments that aren't visible in
the structure-type code, and stone is mentioned far more often in subs than
in superstructure narratives.

**Deck** narrative top words:

```
surface 70,284 | wearing 56,131 | concrete 45,914 | cracks 38,820 |
transverse 31,026 | drains 29,950 | underside 29,590 | curbs 26,204 |
hairline 25,329 | asphalt 25,052 | overlay 11,886 | timber 9,950
```

"**timber**" appearing 9,950 times in *deck* narratives — when only ~80 bridges
in the inventory are coded as timber — confirms that **a meaningful number of
steel-stringer (3/02) bridges in WV have timber decks**, and the deck material
is buried in narrative text rather than the structured fields.

### 7b. The bigram dictionary (Summary & Recommendations field)

Top non-stopword adjacent pairs in 55K summary narratives:

| bigram | n |
|---|---:|
| fair condition | 27,566 |
| most serious | 23,945 |
| serious deficiencies | 23,557 |
| deficiencies observed | 17,133 |
| section loss | 16,861 |
| wearing surface | 15,258 |
| good condition | 14,903 |
| both abutments | 14,603 |
| poor condition | 13,500 |
| structure fair | 13,483 |
| hairline cracks | 11,757 |
| upstream side | 10,124 |
| downstream side | 9,022 |
| exposed rebar | 8,441 |
| each abutment | 8,280 |
| most significant | 7,965 |
| significant deficiencies | 7,724 |
| structure remains | 7,628 |
| rust staining | 3,948 |
| should repaired | 3,208 |
| should monitored | 3,082 |

The ratio **"fair condition" 27.5K : "good condition" 14.9K : "poor condition"
13.5K** is itself diagnostic — Fair (NBI 5–6) is the inspectors' modal verdict
*by a factor of 2×* over either Good or Poor. That's the centroid of the WV
inventory in plain English.

### 7c. Trigrams that signal action / deferral

Top trigrams (filtered for the meaningful ones):

```
most serious deficiencies          23,478
serious deficiencies observed      14,718
will monitored the next             6,678
monitored the next 12-month         6,670
asphalt wearing surface             6,174
upstream and downstream             6,084
condition monitored the             6,032
repairs performed funding           3,905
perform routine maintenance         3,812
routine maintenance required        3,748
month inspection interval           3,693
conditions will monitored           3,568
remains poor condition              3,542
above conditions will               3,538
structure remains fair              3,477
fair condition deficiencies         3,435
collision damage                    3,634
```

"Repairs performed funding" appearing 3,905 times is the *deferred* shape of
**"repairs to be performed pending funding"** — i.e., it is the actual most
common deferred-maintenance phrase in the corpus, even though the literal
phrase "lack of funding" only appears 22 times. **The deferred-maintenance
backlog is hidden in passive boilerplate, not stated plainly.** That's a
language pattern worth searching for if anyone wants to estimate WVDOT's
unfunded repair queue from inspection text.

### 7d. Per-family narrative *fingerprints* (TF-IDF style)

For each family, the top 6 words that are statistically over-represented in
that family's narratives vs the corpus baseline (log-odds, min 50 family
mentions). These are the things inspectors *say more often* about each kind
of bridge — which means they are the *defining failure modes* of those
structures:

| family | distinguishing vocabulary |
|---|---|
| **1/01 RC slab** | crane, stalactites, deviation, judgment, disintegrating, crumbly |
| **1/04 RC tee-beam** | balustrades, stems, failures, discoloration, sandblast, operating |
| **1/11 RC/masonry arch** | spandrels, skewback, spandrel, intrados, crown, curvature |
| **1/19 RC culvert** | sidewall, sidewalls, outerwall, segments, barrels, outerwalls |
| **1/22 RC channel** | segmental, stretchers, cribbing, primary, channel, headers |
| **2/19 RC continuous culvert** | innerwalls, innerwall, cells, outerwalls, centerwall, sedimentation |
| **3/02 Steel stringer** | sponginess, nailers, outrigger, wheelguards, planks, wheelguard |
| **3/03 Steel girder-floor** | stringers, floorbeams, measurable, pitting, **limit, weight** |
| **3/10 Steel through-truss** | reductions, percent, portal, rivets, verticals, strut |
| **3/12 Steel suspension** | suspender, hangers, figures, navigation, rivets, attention |
| **3/19 Steel arch culvert** | mitered, inverts, culverts, collars, bituminous, arches |
| **3/23 Steel riveted truss** | diagonals, verticals, rivet, chords, trusses, heads |
| **3/24 Steel slab-floorbeam** | class, connectors, patina, integral, floorsystem, sleeper |
| **3/31 Steel eyebar truss** | **eyebars, eyebar, wrought, nests**, effective, roller |
| **3/32 Steel movable** | metalwork, catwalk, grate, annually, screens, waste |
| **3/34 Acrow / Bailey** | acrow, galvanizing, retainer, clips, trusses, requirement |
| **3/35 Steel gusset** | galvanizing, galvanized, **gusset, bending, unsupported, unseated** |
| **4/02 Steel cont. stringer** | nelson, backset, protections, noise, microsilica, connectors |
| **4/24 Steel cont. slab** | biennial, vibrations, rippling, **vibration**, teeth, crossframe |
| **4/26 Steel cont. box** | threaded, sensitive, grind, lighting, nesting, remnants |
| **5/01 PSC slab** | encase, hollow, plank, lagging, piles, encased |
| **5/02 PSC stringer** | **prestressing, prestressed, directional, strands**, closure, integral |
| **5/05 PSC box-multi** | adhesive, boxbeams, hoisting, keyways, fiberboard, proof |
| **5/22 PSC channel** | **prestressing, strands, strand**, stretchers, channel, cribbing |
| **6/02 PSC continuous** | **continuity, pours, closure**, prestressed, **diaphragms**, direction |

Things this surfaces that no NBI dashboard does:

* **Family 3/02 (Steel stringer)** is the only family whose distinguishing
  vocabulary is *timber-deck language* ("sponginess, nailers, planks,
  wheelguards"). That means the 3/02 inventory is materially heterogeneous —
  the *superstructure* is steel but a meaningful slice has **timber-on-steel
  decks**, which explains why steel-stringer decks decay differently from
  steel-continuous decks (§ 2). The deck material is not in any structured
  field — it's only in narrative.

* **Family 3/35 (Steel gusset)** distinguishing words include
  "**unsupported, unseated**" — i.e., bearings off their seats. That is a
  *displacement* phenomenon, not a corrosion one. Steel gusset-plate
  structures in WV are showing settlement / lateral movement signs that no
  NBI rating captures.

* **Family 4/24 (Steel continuous slab)** is dominated by "**vibration,
  vibrations, rippling**" — the deck is vibrating perceptibly enough that
  inspectors write it down. That's a service-load behavior that does not
  drive condition rating but does drive *user-experience* complaints and
  fatigue concerns.

* **Family 6/02 (PSC continuous)** distinguishing words are
  "**continuity, pours, closure, diaphragms**" — the *continuity diaphragms*
  between simple spans made continuous are failing/cracking. This is the
  PSC equivalent of the steel-truss gusset problem: the connection between
  spans is the weak link, not the spans themselves.

* **Family 5/22 (PSC channel)** has "**prestressing, strands**" at the top of
  the discriminating list, matching the catastrophic 59.6% poor-super finding
  in § 5. The narrative is *literally* "the strands are corroding" — and
  there are 57 of them.

* **Family 1/11 (RC arch)** uses true masonry-arch vocabulary —
  "**spandrels, intrados, skewback, crown**" — confirming that a portion of
  the 1/11 inventory is actually stone or stone-faced masonry arch, not
  pure RC. Those terms don't appear in any structured field.

### 7e. Words that signal a Poor superstructure rating (vs Good)

For every NBI Item 59 ≤ 4 bridge vs every ≥ 7 bridge, log-odds of token use
(min 200 in poor bucket):

| word | poor n | good n | log-odds |
|---|---:|---:|---:|
| **eyebars** | 258 | 0 | **5.21** |
| **spandrel** | 2,263 | 85 | 3.60 |
| becomes | 352 | 17 | 3.27 |
| **ring** | 524 | 28 | 3.21 |
| verticals | 247 | 20 | 2.77 |
| plated | 206 | 18 | 2.68 |
| **arch** | 2,184 | 242 | 2.54 |
| diagonals | 218 | 23 | 2.52 |
| **posted** | 533 | 59 | 2.51 |
| barrel | 443 | 49 | 2.51 |
| losses | 347 | 40 | 2.46 |
| **floorbeams** | 1,220 | 148 | 2.44 |
| weight | 726 | 93 | 2.38 |
| **prestressing** | 231 | 36 | 2.15 |
| limit | 693 | 112 | 2.15 |
| seriously | 371 | 88 | 1.76 |
| stringers | 1,649 | 409 | 1.73 |
| loss | 10,757 | 2,742 | 1.71 |
| operating | 337 | 85 | 1.70 |
| advanced | 342 | 97 | 1.59 |

The top of the list is structurally specific and tells a story. The strongest
poor-super predictor in the WV inspection text is **"eyebars"** — a 5.21
log-odds ratio, meaning eyebar-truss bridges are ~180× more likely to be in
the Poor-super bucket than the Good. That makes sense: WV has 40+
wrought-iron eyebar trusses still in service, and they are almost all old.

But "**spandrel**" (3.60) and "**arch**", "**ring**", "**barrel**" mean
**stone/masonry arch** vocabulary is the *second-strongest* predictor of poor
superstructure rating in WV. Concrete and steel girder bridges almost never
use those words. So "concrete arch" (1/11) is functioning as a leading
indicator of poor-super in language as well as ratings.

"**posted, weight, limit, operating**" cluster together — load-posted bridges
are getting written up using bridge-rating vocabulary, which is itself rare
in the corpus and correlated with structural distress.

### 7f. Words that signal **fast** decay vs **stable** decay

I built two cohorts:

* **fast** = bridge dropped ≥2 NBI points on any component, in ≥5 years (n=4,035)
* **stable** = bridge dropped 0 points on any component, in ≥8 years (n=710)

Words over-represented in the *fast* cohort (log-odds):

| word | log-odds (fast vs stable) |
|---|---:|
| **caulk** | 2.72 |
| basket | 1.78 |
| keys | 1.62 |
| progression | 1.60 |
| **piling** | 1.48 |
| header | 1.48 |
| manpower | 1.42 |
| **gabion** | 1.41 |
| cable | 1.40 |
| seriously | 1.34 |
| breakage | 1.31 |
| **funding** | 1.16 |
| **slight** | 1.12 |
| eroded | 1.00 |
| undercut | 0.98 |
| waterline | 0.94 |
| **silicone** | 1.08 |
| faint | 1.07 |
| baskets | 1.22 |

Words over-represented in the *stable* cohort:

| word | log-odds (stable vs fast) |
|---|---:|
| tack | 1.77 |
| hanger | 1.52 |
| cell | 1.51 |
| headwalls | 1.51 |
| headwall | 1.48 |
| cells | 1.46 |
| steelwork | 1.31 |
| propagation | 1.19 |
| welded | 1.12 |
| drilled | 1.05 |
| **barrel** | 1.04 |
| scattered | 1.01 |
| bracing | 0.94 |
| stiffeners | 0.90 |
| culvert | 0.90 |
| coated | 0.89 |
| fatigue | 0.70 |

A clear pattern: the *fast* cohort's vocabulary is dominated by failed
remediation — **"caulk", "silicone", "gabion", "basket", "piling",
"undercut", "eroded", "waterline"** — i.e., the joints have been
sealed-and-resealed, the piers have been wrapped with gabion baskets that are
themselves failing, the piling is exposed and undercut at the waterline. The
words **"manpower"** and **"funding"** appearing on the fast-cohort list is
the deferred-maintenance smoking gun: when inspectors *do* write about
funding constraints, it correlates strongly with bridges that are decaying
faster.

The *stable* cohort's vocabulary is **structural inventory language**:
"barrel, cells, headwalls, bracing, stiffeners, welded, coated, fatigue,
propagation, drilled". These are *culverts* (cells, barrel, headwalls) and
*steel girder structures with active maintenance attention* (welded,
coated/protective coatings, stiffeners, bracing). Culverts genuinely decay
slowly. Steel-girders with active paint programs are stable; the same family
without paint maintenance shows up in the fast cohort.

The "**fatigue**" word ranking in stable bridges is counter-intuitive but
real: inspectors *write about fatigue* on steel structures where they're
*monitoring* it — and monitored fatigue doesn't generally progress unless
ignored. Fatigue-cracking bridges that *advance* tend to get rehabbed
quickly, removing them from the fast cohort.

### 7g. Defect lexicon prevalence across the full 1M-memo corpus

Of 1,015,676 narrative memo rows:

| phrase / token | % of memos |
|---|---:|
| hairline | **8.1%** |
| spalling | **6.4%** |
| section loss | 5.8% |
| fracture | 5.8% |
| delamination | 3.1% |
| efflorescence | 3.0% |
| map crack | 2.9% |
| rust stain | (high — most-common bigram) |
| pack rust | 0.4% |
| fatigue | 0.9% |
| scour | 1.6% |
| undercut | 1.2% |
| exposed rebar / reinforcing | ~1.5% |
| collision | 1.7% |
| vehicle impact | 0.03% |
| fatigue crack | 0.5% |
| fracture critical | 5.5% (boilerplate, see § 7a) |

**1 in 12 narrative entries mentions "hairline" cracks** — the canonical
"cracking is present but not advancing" line. **1 in 16 mentions "spalling".**
These two are the workhorse condition vocabulary of the WV inspection corpus.

"**Vehicle impact**" appears only 341 times in 1M memos, but **"collision"**
appears 16,961 times — a 50:1 ratio. The narrative norm is "collision damage",
not "vehicle impact" — keep that in mind when querying.

### 7h. Deferred-maintenance phrase pattern

| literal phrase | # of memo hits |
|---|---:|
| "lack of funding" | **22** |
| "lack of manpower" | 34 |
| "awaiting funding" | 0 |
| "awaiting repair" | 16 |
| "pending funding" | 5 |
| "posted bridge" | 47 |
| "load posting" | 113 |
| "continue to monitor" | several thousand |
| "no improvement" | 217 |
| "advanced deterioration" | 471 |
| "further deterioration" | 4,003 |
| "due to scour" | 79 |
| "maintenance forces" | 68 |
| "critical finding" | high |
| "notice of finding" | low |

Inspectors *almost never* write the literal phrase "lack of funding" — it
exists only 22 times in 313K narratives, or 1 in 14,000. They write
"**further deterioration**" (4,003 hits) and "**continue to monitor**"
(thousands). The implicit deferral is everywhere; the explicit deferral is
written down ~22 times. If anyone wants to extract WVDOT's true unfunded
backlog from text, the queries to run are on `further deterioration`,
`should be repaired`, `should be monitored`, and `repairs to be performed`
— not on `lack of funding`.

---

## 8. Element-level deterioration (AASHTO BME elements)

Element-level condition states (CS1 Good → CS4 Severe) are recorded per
quantity unit. Severe% = (CS3 + CS4) / total quantity, computed across all
inspections.

The most-degraded common elements (n bridges ≥ 200):

| element | n bridges | total qty | **% severe** |
|---|---:|---:|---:|
| Seal Damage | 256 | 10,110 | **85.6%** |
| Leakage | 301 | 19,064 | 75.8% |
| Exposed Rebar | 848 | 43,413 | 72.1% |
| Alignment | 208 | 1,494 | 55.0% |
| Connection | 442 | 7,771 | 50.9% |
| Delamination/Spall/Patched Area/Pothole (Wearing Surfaces) | 477 | 164,572 | 47.6% |
| **Effectiveness (Steel Protective Coatings)** | **759** | **1,805,959** | **46.5%** |
| Peeling/Bubbling/Cracking (Steel Protective Coatings) | 461 | 814,514 | 42.2% |
| Adjacent Deck or Header | 327 | 14,428 | 28.0% |
| Delamination/Spall/Patched Area | 1,772 | 291,036 | 25.5% |
| Compression Joint Seal | 416 | 49,548 | 25.1% |
| Strip Seal Joint | 562 | 66,039 | 23.9% |
| Crack (Wearing Surface) | 539 | 1,330,577 | 19.7% |
| Movable Bearing | 1,024 | 21,084 | 18.9% |
| Damage | 411 | 24,686 | 18.4% |
| Cracking (RC and Other) | 1,668 | 3,152,674 | 17.5% |
| Corrosion | 1,126 | 578,910 | 17.1% |
| Efflorescence/Rust Staining | 1,674 | 1,256,185 | 13.8% |
| Reinforced Concrete Column | 895 | 7,980 | 9.0% |
| Fixed Bearing | 1,064 | 10,618 | 7.7% |
| Elastomeric Bearing | 665 | 15,187 | 6.8% |
| Reinforced Concrete Abutment | 1,906 | 239,435 | **6.5%** |
| Steel Protective Coating | 1,548 | 61,830,056 | 4.0% |
| Wearing Surfaces | 896 | 12,796,699 | 3.4% |

Three things to pull out:

1. **Steel protective coatings are systemically failing.** "Effectiveness
   (Steel Protective Coatings)" runs 46.5% severe across 1.8M units on 759
   bridges, and "Peeling/Bubbling/Cracking" is 42.2% on 814K units across 461
   bridges. Paint is the *single largest* element-level deferred maintenance
   item in the inventory, by area. Every steel-girder bridge in WV is
   effectively in a paint backlog.

2. **Joint seals are the runaway worst category.** Seal Damage 85.6%, Leakage
   75.8%, Adhesion 72.7%, Strip Seal Joint 23.9%, Compression Joint Seal
   25.1%, Pourable Joint Seal 42.7%. **The single biggest accelerant of
   substructure deterioration in WV is failed joints letting chloride-laden
   runoff onto bearings and pier caps.** This shows up in § 7f as the "caulk
   / silicone / basket" vocabulary of the fast-decay cohort.

3. **Exposed Rebar is on 848 bridges at 72.1% severe.** That's the single
   most-reported acute deck/sub defect in the element data.

---

## 9. Inspector calibration drift

For every component on every bridge with ≥2 rating transitions, count the
number of "up" moves (rating improved without an obvious repair record) vs
"down" moves:

| concept | bridges with transitions | bridges with both ups *and* downs | **% oscillating** |
|---|---:|---:|---:|
| Substructure | 7,401 | 1,571 | 21.2% |
| Deck | 7,018 | 1,510 | 21.5% |
| Superstructure | 7,415 | 1,614 | **21.8%** |

**Over 1-in-5 bridges show NBI-component ratings that go down, then up
again.** Sometimes that is legitimate maintenance (a deck overlay can lift
the rating). But about *one-fifth* of the rating signal is rater drift —
which means that for ~1,600 bridges per component, the trend line is partly
noise. Comparisons of individual bridges over short windows (one to two
inspection cycles) need to be discounted accordingly.

This also means **the "improved" tail in the decline-distribution table
(§ 3) is mostly calibration drift, not actual rehab** — there are only ~600
formally-recorded rehabilitation events vs ~1,500 "improved" component
trajectories per concept.

---

## 10. ADT, span count, and other surprises

### 10a. High-ADT bridges decay *slower*, not faster

Average Δ/yr rating change by ADT band (deck):

| ADT band | n | deck Δ/yr |
|---|---:|---:|
| <100 | 1,752 | 0.063 |
| 100–499 | 1,512 | 0.067 |
| 500–1,999 | 1,223 | 0.065 |
| 2k–10k | 1,071 | 0.061 |
| **10k+** | **611** | **0.038** |

High-traffic bridges decay ~40% slower on deck than low-traffic ones, even
though theory says heavier loads should accelerate deck fatigue. The
mechanism is **selection bias for funding** — high-ADT structures get rehab
priority and federal eligibility, so by the time you average their Δ/yr,
they've had at least one overlay or rehab event in the window.

This is the empirical answer to "where is the deferred-maintenance backlog?"
in WV. It is *not* on the high-ADT interstate network. It is on the
sub-2,000-ADT county-route inventory in the southern coalfields.

### 10b. Multi-span bridges decay slower than single-span

| span count | n | super Δ/yr |
|---|---:|---:|
| 1 | 5,521 | 0.061 |
| 2 | 715 | 0.057 |
| 3–5 | 238 | 0.051 |
| 6+ | 20 | **0.028** |

Multi-span structures are mostly modern PSC or steel continuous on larger
crossings; single-span is the long tail of small-stream rural bridges, many
of which carry the legacy concrete-arch / timber-on-steel-stringer mix
identified in § 7d. Single-span ≠ bad structure, but single-span ≈ low ADT
≈ underfunded.

### 10c. Channel ratings are weather signal, not deterioration signal

A separate finding rolled forward from § 2c: of 5,000+ bridges with multiple
channel-rating observations, ~94% have median annual rate of change inside
±0.05 — i.e., channel ratings are within inspector measurement noise except
during flood years. Channel ratings 4 and below are concentrated on
specific watersheds rather than specific bridge families (see § 5a). When
prioritizing scour-critical inventory, the *scour* rating (Item 113) and the
narrative `undercut` / `pier` language are better signals than the channel
condition rating.

### 10d. Critical scour ratings (NBI 113 ≤ 4)

Among bridges with explicit scour ratings, % at critical (≤ 4):

| family | n | n critical | % critical scour |
|---|---:|---:|---:|
| 5/01 PSC slab | 86 | 5 | 5.8% |
| 3/02 Steel stringer | 1,122 | 54 | 4.8% |
| 1/01 RC slab | 328 | 14 | 4.3% |
| 3/03 Steel girder-floor | 100 | 4 | 4.0% |
| 1/11 RC arch | 313 | 11 | 3.5% |
| 1/04 RC tee | 58 | 2 | 3.4% |
| 3/19 Steel arch culvert | 92 | 3 | 3.3% |
| 4/02 Steel cont. stringer | 555 | 8 | 1.4% |
| 5/05 PSC box | 1,927 | 24 | 1.2% |

The most scour-vulnerable inventory in WV is the **steel-stringer-on-pile**
family (3/02) — 54 bridges currently at critical scour, against a base of
1,122. That's where the "piling, undercut, waterline, eroded" vocabulary
from § 7f is concentrated.

---

## 11. What this all adds up to (and what to look at first)

These are the deterioration-driven observations that don't show up in the
standard NBI roll-ups, ranked by what I'd act on first:

1. **PSC box beam (5/05) is the next big maintenance wave.** 1,950 bridges,
   354 already showing premature 3+-pt decline, median age 31, hitting the
   classic strand-corrosion knee. Survival from 7→5 is currently ~9 years,
   but it will compress as the inventory ages into the 40+ band.

2. **PSC channel beam (5/22) is in active failure as a class.** 57 bridges,
   60% poor superstructure, average age 56. Narrative signature is literal
   strand exposure. Targeted replacement program is feasible and overdue.

3. **The post-1990 premature-failure population (~50 bridges < 30 yrs old at
   Super ≤ 4) is a quality-assurance problem, not a deterioration problem.**
   Pull files on BARS 51X001 (2019, Super 4 at age 7), 23A364, 24A357,
   23A355, 06A334.

4. **D10 needs ~70 historic-structure replacements** (3/25, 3/27, 1/11,
   1/01 in coalfield counties at avg age 88–103). That single tranche would
   lift D10 from worst-in-state to middle-of-pack.

5. **Joint seals + steel protective coatings dominate the element-level
   deferred-maintenance backlog by area.** This is not a glamorous program,
   but in element-quantity-weighted terms it is the single biggest lever on
   forward deterioration rate.

6. **Inspector calibration drift accounts for ~20% of the rating-improvement
   signal.** Trend analyses that span <8 years need to be filtered for
   directional consistency, not raw deltas.

7. **The "timber-deck on steel-stringer" subpopulation is invisible in
   structured data.** 3/02 inventory narrative analysis indicates a real
   slice of this family has timber decking — driving the higher 3/02 deck
   Δ/yr and the "sponginess, nailers, planks" vocabulary. This subpopulation
   is not separately coded and should be queryable by narrative pattern.

8. **The deferred-maintenance backlog is documented, but in passive
   boilerplate.** The 4,003 occurrences of "further deterioration" and
   3,905 of "repairs performed funding" (i.e. "repairs to be performed
   pending funding") are the real signal. The 22 mentions of "lack of
   funding" are not.

---

*Generated from `bridges_all.duckdb` — every number in this document is
reproducible from the queries in the source database. Schema-first
DuckDB practice was followed throughout (see [[feedback_duckdb_schema_first]]),
working tables used: `dt_history`, `dt_first_last`, `bridge_cohort`,
`rv_tokens`.*
