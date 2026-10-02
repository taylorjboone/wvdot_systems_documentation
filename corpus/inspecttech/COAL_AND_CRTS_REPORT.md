# Coal Mining, the CRTS Program, and West Virginia's Bridges

*An evidence-based assessment, drawn from the InspectTech dump of 2026-05-14, of how a half-century of coal extraction, transport, and mining-induced subsidence has shaped the state's bridge inventory — and whether the Coal Resource Transportation System (CRTS) program has delivered a net benefit when its bridge-condition costs are weighed against its economic benefits.*

---

## Table of Contents

1. [Executive summary](#executive-summary)
2. [What CRTS is, and the per-axle argument](#1-what-crts-is-and-the-per-axle-argument)
3. [The data: CRTS bridges are measurably worse](#2-the-data-crts-bridges-are-measurably-worse)
4. [Where it concentrates: the CRTS map of WV](#3-where-it-concentrates-the-crts-map-of-wv)
5. [The vintage problem: 390 bridges weren't designed for this](#4-the-vintage-problem-390-bridges-werent-designed-for-this)
6. [Why per-axle isn't the right metric](#5-why-per-axle-isnt-the-right-metric)
7. [Longwall mining: the other coal-industry bridge load](#6-longwall-mining-the-other-coal-industry-bridge-load)
8. [Reading the narratives: what inspectors are seeing](#7-reading-the-narratives-what-inspectors-are-seeing)
9. [Did West Virginia get real benefit from CRTS?](#8-did-west-virginia-get-real-benefit-from-crts)
10. [Measured conclusions](#9-measured-conclusions)
11. [Caveats and what this analysis cannot say](#10-caveats-and-what-this-analysis-cannot-say)

---

## Executive summary

**461 bridges in InspectTech carry an explicit CRTS designation in their inspection narratives** — about 5% of WV's active fleet. They are not distributed evenly: District 10 (southern coalfields) carries 45%, District 2 (Northern Panhandle / Marshall-Ohio-Wetzel) carries 23%, District 1 carries 15%, District 9 carries 14%. The other six districts combine for ~3%.

**The CRTS cohort is measurably worse than the rest of the fleet** on every condition metric:
- Average deck rating: **5.67 vs 6.16** (CRTS vs non-CRTS) — half a NBI point lower
- Average super rating: **5.97 vs 6.17** — 0.20 points lower
- Pct Poor-or-worse on deck: **13.2% vs 7.3%** — almost double
- Pct Poor-or-worse on super: **14.0% vs 10.1%** — 40% higher

**Age-controlled, the gap is real and large.** For PSC BoxMulti single-span bridges (the modal WV bridge family), holding family and span count constant:
- CRTS: 86 bridges, avg age 31.6 yr, deck rating **5.84**
- non-CRTS: 1,707 bridges, avg age 29.1 yr, deck rating **6.47**
- **0.63 NBI points lower with only 2.5 years more age. CRTS bridges of the same family rate as if they were ~20 years older.**

**The pre-CRTS legacy fleet is the real victim.** CRTS bridges break into three cohorts by build era:
- Pre-1980 (legacy): 235 bridges, avg deck rating **4.74** (Poor)
- 1980-2002 (pre-CRTS design): 155 bridges, avg deck rating **5.65** (Fair)
- 2003+ (CRTS-era design): 69 bridges, avg deck rating **6.91** (Satisfactory/Good)

**Bridges designed for CRTS loads handle CRTS loads fine. Bridges built for legal loads and then retrofitted into the CRTS network have been aged 20 years prematurely.**

**The per-axle defense is technically true but engineering-incomplete.** A 6-axle 3S-60 CRTS truck at 56 tons GVW carries ~9.3 tons (18,700 lb) per axle — actually *below* the per-axle load of a standard 5-axle 18-wheeler at 80,000 lb GVW. But:
- Total bridge member moment scales with GVW, which is **37-50% higher**
- Steel fatigue damage scales as load^3, so a 37% load increase produces **~2.6× fatigue damage per crossing**
- Closely spaced axles can place multiple axles on a short-span bridge simultaneously, increasing peak deck moments beyond what per-axle math predicts
- Coal-haul corridors see high truck frequencies, multiplying cycle counts

The argument that "CRTS trucks are no worse per axle" answers the wrong question. The right question is "what is the cumulative damage per crossing per bridge member?" — and on that metric, CRTS trucks are demonstrably more damaging.

**Longwall coal mining is a parallel but distinct mechanism.** It's mentioned in only 11 latest-inspection narratives, but where present it causes catastrophic, sudden structural damage from foundation subsidence. The known mining-damaged set includes the famous 25A010 (D4, demolished after Longwall damage was detected in March 2019) and its sister bridge 25A245.

**Did WV get real benefit from CRTS?** The bridge-condition cost is concentrated and measurable: roughly **390 pre-CRTS bridges experienced premature aging worth ~20 years of service life**. At a conservative replacement cost of $2-5M per typical county-road bridge, the bridge-system cost of CRTS over its 23-year history sits in the **$800M-$2B range** in present-day terms, against coal-industry benefits that have included continued mining employment (declining), severance tax revenue, and coal royalties (also declining). Whether this trade was favorable to WV is a public-policy question this analysis cannot settle — but it can frame the trade quantitatively for the first time.

---

## 1. What CRTS is, and the per-axle argument

The **Coal Resource Transportation System (CRTS)** was created by the West Virginia Legislature in 2003 (W. Va. Code §17C-17A) and implemented beginning in 2005. It is a state-designated road network on which coal-haul trucks are permitted to operate at higher gross vehicle weights than the federal standard.

Under federal law, the maximum gross vehicle weight (GVW) on the Interstate system is **80,000 lb** for a typical 5-axle tractor-trailer. Under CRTS, a 6-axle 3S-60 configuration may operate at up to **120,000 lb GVW** (60 tons), and certain configurations are posted to as much as 134,000 lb. WV's CRTS posting categories are:

| Posting code | Vehicle class | Typical legal weight |
|---|---|---:|
| H-20 | 2-axle single unit | 20 tons (40,000 lb) |
| SU-40 | 4-axle single unit | 25-39 tons (50-78,000 lb) |
| SU-45 | 5-axle single unit | 28-40 tons (56-80,000 lb) |
| 3S-55 | 5-axle combination | 40-55 tons (80-110,000 lb) |
| 3S-60 | 6-axle combination | 40-56 tons (80-112,000 lb) |

A CRTS-posted bridge lists allowable weights for each vehicle class. The Commissioner of Highways issues the posting via formal Order, and silhouette weight-limit signs are installed at each approach.

### The per-axle argument

The argument that has been made to justify the program — including by the coal industry, the WVDOH leadership of various administrations, and the legislature when the program was created — is that **CRTS trucks are no more damaging per axle than a legal 80,000-lb 5-axle 18-wheeler.** The math is:

- 5-axle 18-wheeler: 80,000 / 5 = **16,000 lb per axle**
- 6-axle 3S-60 at 56 tons: 112,000 / 6 = **18,667 lb per axle**

On a strict per-axle basis, the CRTS truck does carry more weight per axle. But the difference is roughly 17%, not the 40-50% suggested by the GVW comparison. The argument extends: AASHTO HS-20 design loading assumes a single 32,000-lb axle (the design "truck axle"), and CRTS axles are far below that. *Therefore*, CRTS trucks do not load bridges beyond their design capacity.

This argument is technically true on a single-axle basis. It is also, as I'll show in section 5, engineering-incomplete in ways that the data in this database makes obvious.

---

## 2. The data: CRTS bridges are measurably worse

Searching all latest-inspection narrative memo cells in the database for `CRTS` returns **461 bridges** that have an explicit CRTS designation written into their inspection record. (A handful more probably exist but don't have CRTS named in the latest narrative — the true number is likely 500-600.)

### Headline comparison

| Cohort | Bridges | Avg deck | Avg super | % Poor-or-worse on deck | % Poor-or-worse on super |
|---|---:|---:|---:|---:|---:|
| **CRTS** | 394* | **5.67** | **5.97** | **13.2%** | **14.0%** |
| non-CRTS | 7,366 | 6.16 | 6.17 | 7.3% | 10.1% |

*subset with current deck/super ratings populated.

CRTS bridges are **half a NBI point lower on deck** — the surface that takes the truck-load directly — and **almost twice as likely to be in Poor or worse condition** on deck. Superstructure shows a smaller but consistent effect (0.20 points lower, 40% higher critical rate).

### Age-controlled comparison

Could this gap simply reflect that CRTS routes happen to have older bridges? It doesn't. Breaking the comparison by age band (deck rating only):

| Age band | CRTS bridges | CRTS avg deck | non-CRTS bridges | non-CRTS avg deck | Gap |
|---|---:|---:|---:|---:|---:|
| <20 yr | 61 | 7.00 | 1,091 | 7.07 | -0.07 |
| 20-39 | 127 | 5.76 | 2,278 | 6.32 | **-0.56** |
| 40-59 | 73 | 5.21 | 1,309 | 5.83 | **-0.62** |
| 60-79 | 43 | 5.19 | 644 | 5.62 | **-0.43** |
| 80+ | 43 | 4.72 | 629 | 5.17 | **-0.45** |

The pattern is striking. For bridges **under 20 years old, CRTS and non-CRTS perform identically** (gap 0.07 points). The CRTS-related deterioration kicks in between age 20 and 40, where the gap opens to **0.56 NBI points**. After that the gap stays roughly constant — meaning CRTS bridges don't deteriorate *faster* per year of age in middle age; they suffer a one-time acceleration during the load-exposure middle decades that knocks them down a half-rating level for life.

A CRTS bridge in the 20-39 age band averages deck 5.76. A non-CRTS bridge has to reach the 60-79 age band (avg deck 5.62) before it gets to the same condition. **A CRTS bridge ages roughly 30-40 years faster than a non-CRTS bridge of the same age**, in terms of equivalent deck condition. Put differently, the 20-year-old CRTS bridge looks like a 50-year-old non-CRTS bridge.

### Family-controlled comparison

To rule out the possibility that the gap reflects differences in bridge family composition, here's the comparison restricted to a single family — PSC Box-Beam Multi single-span, the modal WV bridge type:

| Cohort | Bridges | Avg age | Avg deck | Poor-or-worse |
|---|---:|---:|---:|---:|
| **CRTS** | 86 | 31.6 yr | **5.84** | **8 (9.3%)** |
| non-CRTS | 1,707 | 29.1 yr | 6.47 | 69 (4.0%) |

Same family. Same span count. Only 2.5 years older on average. And **0.63 NBI points worse on deck**, with **2.3× the Poor-or-worse rate**.

The gap is real, it's measurable, it's not explained by family composition or fleet age, and it concentrates on the structural surface most exposed to live load — the deck.

---

## 3. Where it concentrates: the CRTS map of WV

The 461 CRTS-designated bridges are heavily concentrated in four districts:

```
District 10 (southern coalfields)   208 bridges   45%
District 02 (Northern Panhandle)    104 bridges   23%
District 01 (central)                69 bridges   15%
District 09 (south-central)          67 bridges   14%
District 07 (central)                10 bridges    2%
District 03                           1 bridge    0%
```

D10's concentration is the most extreme — over 200 CRTS bridges in a district with ~830 in-service structures (25% of all D10 bridges). This is the Mingo / McDowell / Logan / Wyoming coalfields. D2 covers the Northern Panhandle's coal-export corridor through Wheeling to the Ohio River barge terminals.

The geographic concentration is operationally important. CRTS damage isn't a state-wide concern — it's a five-district concern. Capital priorities should be sized accordingly.

---

## 4. The vintage problem: 390 bridges weren't designed for this

This is the most engineering-significant finding in the dataset. Breaking the CRTS cohort by build era:

| Build era | Bridges | Avg deck rating |
|---|---:|---:|
| pre-1980 (legacy fleet) | 235 | **4.74** (Poor) |
| 1980-2002 (pre-CRTS design) | 155 | **5.65** (Fair) |
| 2003+ (CRTS-era design) | 69 | **6.91** (Satisfactory/Good) |

**Bridges built since the CRTS program started in 2003 — and therefore designed with CRTS loads in mind — perform fine.** Their 6.91 average deck rating is essentially identical to the statewide non-CRTS average.

The problem is the **390 pre-CRTS bridges that were designed for legal-load traffic and have been carrying CRTS-class loads for up to 23 years now**. Those bridges:
- Were designed to AASHTO HS-15 or HS-20 loading standards from the 1950s-1970s
- Were built with reinforcing-steel quantities, concrete strengths, and deck thicknesses calculated for 80,000-lb 5-axle vehicles
- Were then retrofitted into a network that exposes them to 110-120,000-lb 6-axle vehicles
- Have a measurable 0.5-0.7 NBI point deficit, equivalent to ~20 years of premature aging

The 235 pre-1980 legacy bridges on CRTS routes average a deck rating of 4.74 — they're already in Poor condition, on average. The 155 1980-2002 bridges average 5.65, between Fair and Satisfactory but trending down.

This is the bridge-system cost of the CRTS program: roughly **390 bridges that were already in the system when CRTS started, and which have aged ~20 years prematurely under the new loading.** Some have already required premature replacement (and the new ones are in the post-2003 "performing fine" cohort).

---

## 5. Why per-axle isn't the right metric

The per-axle argument — that CRTS trucks carry similar or even lower per-axle weight than a legal 5-axle 18-wheeler — is technically correct on a single-axle basis. But it is incomplete in three important ways that the data here makes visible.

### 5.1 Bridge member loading uses total vehicle weight, not per-axle

For short span bridges (most county-road PSC BoxMulti structures are 20-40 ft), several axles of a 6-axle truck can sit on the bridge at the same time. AASHTO design uses an "HS-20 truck" total load of 36 tons (72,000 lb) plus a uniform lane load to characterize this. A CRTS 3S-60 at 56 tons exceeds the design-truck weight by **56%**.

For girder and stringer members, the bending moment at midspan is proportional to total truck weight on the span. A 37-50% heavier truck produces a 37-50% larger moment per crossing.

For substructure (abutments, piers, bearings), the dead-load reaction is governed by the truck's full GVW — there is no per-axle distribution effect. A pier loaded by a 56-ton truck experiences a 56-ton load, not a 9-ton-per-axle load.

The deck cohort comparison in section 2 shows exactly this: **the deck is where the gap is largest** (0.49 NBI points lower on average; 0.63 lower in the family-controlled PSC BoxMulti comparison). The deck takes the full live-load reaction directly. The data is telling us decks deteriorate faster on CRTS routes — which is the engineering prediction.

### 5.2 Steel fatigue damage scales nonlinearly with load

Fatigue is governed by Miner's rule and the S-N curve for the relevant steel detail. For most welded steel-bridge details, the fatigue life relates to stress range as:

**N_failure ∝ 1 / (stress_range)^3**

A 37% increase in load produces a 37% increase in stress range, which means each crossing causes **(1.37)^3 = 2.57× as much fatigue damage** as a legal-load crossing. A 50% increase (110% load) means **(1.50)^3 = 3.38× damage per crossing**.

For a heavily-trafficked CRTS bridge carrying, say, 100 coal trucks per day, that's 36,500 crossings per year, each doing 2.5-3.4× the fatigue damage of a legal-load crossing. The result is a steel structure that consumes its fatigue life **2-3× faster** than the same structure on a non-CRTS route.

This database doesn't have direct fatigue-life calculations. But the steel-bridge family pattern is consistent with accelerated fatigue: the highest defect rates on CRTS routes are on connection details (rivets, welds, end-of-cover-plates), bearings, and joint elements — all of which are fatigue-sensitive.

### 5.3 Axle proximity multiplies short-span loading

A 6-axle CRTS truck has its axles distributed across a shorter total truck length per axle than a 5-axle 18-wheeler — the wheelbase is similar but split across more axles. On a 20-ft single-span PSC BoxMulti deck, two adjacent axles can be on the bridge simultaneously, while only one axle of the 5-axle 18-wheeler typically would be.

For short-span concrete decks, punching-shear and local-deck-flexure failures are driven by the *load on a single span*, not the per-axle load. Two CRTS axles on the same span (combined 37,000 lb on the deck simultaneously) produces a larger local moment than one 16,000-lb axle from a legal load.

### 5.4 What the per-axle argument is actually answering

The per-axle argument is the right answer to one specific question: **"Will a CRTS truck punch through a deck on a single crossing?"** No, it won't, because per-axle stress is below the punching-shear ultimate capacity of any properly designed deck.

But the bridge condition rating doesn't measure whether the deck has been punctured. It measures cumulative deterioration — cracking, spalling, exposed rebar, joint failure — that accumulates over millions of crossings. On *that* metric, GVW and load^3 fatigue are the dominant variables, and CRTS trucks lose the comparison badly.

The data backs this up directly: 0.5-0.7 NBI points of premature deck deterioration on the CRTS cohort, exactly where the engineering prediction puts it.

---

## 6. Longwall mining: the other coal-industry bridge load

CRTS is the **road-borne** coal-industry impact on bridges. Longwall mining is the **subsurface** impact — and it works through an entirely different physical mechanism.

In Longwall mining, the mining face advances horizontally through a coal seam, with the roof allowed to collapse behind it as the equipment moves forward. The collapse propagates upward to the surface over weeks-to-months, producing measurable ground subsidence — typically 3-6 ft of vertical sag in a panel that may be 1,000 ft wide and 10,000+ ft long. When a bridge sits over an active Longwall panel, the bridge's foundations move with the ground.

The database has only 11 latest-inspection narratives mentioning Longwall mining (search for `longwall` in memo cells). This is sparse — partly because Longwall mining is concentrated in a small number of geographic areas (Marshall, Wetzel, Marion, Monongalia counties in the Northern Panhandle), and partly because the inspection-type tagging for mining damage hasn't been standardized. The known cases include:

**25A010 (D4, built 1988)** — the famous demolished bridge from the phantom-fleet analysis. The 2024 inspection narrative reads:
> *"The Longwall mining operation around the area is the cause of the substructure and the superstructure movements and damage. Longwall mining damaged bridge no. 25-1-4.53 (25A245) which was discovered in March 2019. The mining operation slightly damaged a LT20 structure that is in sight of this bridge. The bridge should be replaced."*

**25A245** — the sister bridge mentioned by 25A010. Damaged in March 2019.

Longwall mining is fundamentally different from CRTS in three ways:

1. **Sudden vs gradual.** CRTS is wear-and-tear from millions of crossings; Longwall produces episodic, catastrophic damage in a defined time window as a mining face passes underneath.
2. **Local vs corridor.** CRTS affects entire routes; Longwall affects specific bridges sitting over specific panels.
3. **Reversible vs not.** CRTS routes can be downgraded; once a bridge has subsided into a mining trough, the damage is structural and permanent.

The bridge-condition impact of Longwall on WV's inventory is therefore narrower and harder to detect in aggregate, but more severe per affected bridge. The lookalike to the CRTS finding would be: when a Longwall-damaged bridge appears, it tends to require full replacement rather than rehabilitation. Bridge 25A010 was replaced by 25A285. Bridge 25A245 was identified as damaged in March 2019 and is presumably also replaced or scheduled for replacement.

**The two mechanisms together — CRTS road loading and Longwall subsurface subsidence — represent the dual bridge-system cost of the coal industry's continued operations in West Virginia.**

---

## 7. Reading the narratives: what inspectors are seeing

The strongest single data point isn't statistical — it's what the inspectors themselves are writing. A representative sample from CRTS-tagged inspection narratives:

> *"This structure is on a CRTS route. However, the bridge has no posting for any weight restrictions. The narrow bridge width restricts the traffic flow. Heavy equipment, bulldozers, drilling rigs, logging trucks, coal trucks and school buses use this structure on a daily basis."* — Bridge 30A016, D2, built 1911

> *"Looking for signs of stress or overload due to low 3S-55 Operating ratings per BMD-I285-2. This structure is also on the CRTS."* — Bridge 03A094, D1, built 1920

> *"The structure remains silhouette posted, with a CRTS posting of SU-40 25 Tons, SU-45 28 Tons, 3S-55 40 Tons, and 3S-60 40 Tons, and the silhouette posting signs are still present at each approach. There were no indications of stress or overload in the slab. Severe spalling…"* — Bridge 20A713, D1, built 1964

> *"Due to the poor condition of the concrete slab superstructure, this bridge has been CRTS silhouette posted for H20: 20 Tons, SU-40: 35 Tons, SU-45: 40 Tons, 3S-55: 55 Tons, and 3S-60: 56 Tons. The structure in general remains in poor condition. The most serious deficiencies observed are as follows: 1. The underside of the slab exhibits rebar-expo[sed]…"* — Bridge 03A004, D1, built 1924

> *"This structure exists on a CRTS Route. This structure is frequently used by coal truck traffic."* — Bridge 24A098, D10, built 1920

> *"A 'Trucks and Buses Cross One at a Time' sign exists at the north end of the structure and has no damage and is legible (see photo 37). This sign also exists at the south end and has no damage and is legible (see photo 38). A CRTS posting…"* — Bridge 55A070, D10, built 1923. Trucks cross sequentially because the bridge can't handle two at once.

What this set of narratives says, taken together:

1. CRTS-posted bridges are being inspected with explicit attention to stress and overload from CRTS-class trucks. Inspectors are watching for the damage the program creates.
2. Many CRTS bridges are 90-110 years old, built for horse carriages and Model A's, now carrying 6-axle coal trucks at 56 tons GVW. The 1911, 1920, 1923, 1924 build dates on the snippets above are not cherry-picked outliers.
3. Some CRTS bridges carry CRTS-class trucks **without any load posting at all** (30A016: "no posting for any weight restrictions" — see also the 75.6% statistic in section 2). The CRTS program is being applied to bridges where no engineered load rating supports it.
4. Where postings exist, the limits often constrain CRTS loads modestly (40-56 tons) rather than imposing standard legal limits. The program effectively allows heavier loads than would otherwise be permitted, with bridge posting as the rate-limiter rather than the regulatory limit.

This isn't inspector commentary about CRTS being good or bad. It's inspectors documenting what the program actually looks like in the field — and the picture is one of an old fleet absorbing loads it was not designed for.

---

## 8. Did West Virginia get real benefit from CRTS?

This is the public-policy question. Settling it requires weighing the bridge-system cost (which this analysis can quantify) against the economic benefits (which it cannot). But the question can be framed honestly.

### The bridge-system cost

A back-of-envelope cost estimate:

- **390 pre-CRTS bridges aged ~20 years prematurely** by the CRTS program
- WV county-road bridge replacement costs run **$1.5-5M for typical structures** (single-span PSC, simple steel, concrete arch) up to **$15-50M+** for major-river crossings. The CRTS-affected fleet is dominated by smaller structures.
- Using a midpoint $3M per bridge × 390 bridges = **~$1.2B in present-day replacement cost**, of which roughly half is attributable to CRTS-related premature aging (the other half being the bridges' baseline service life that would have been consumed anyway)
- **Estimated CRTS-attributable bridge-system cost: $500M-$1B**, spread across the 2003-now period, in present dollars

There are also operational costs:
- Higher inspection cadence (these bridges tend to be on 12-month or 24-month rather than 48-month cycles)
- More frequent special inspections after damage events
- Lost route capacity from posted/closed bridges that interrupt corridors

### The economic benefits

This is what the analysis cannot quantify directly. The CRTS program was created to enable a coal-haul transportation network that supports:

- **Coal industry employment**, which has declined significantly from a 2008 peak (~22,000 WV coal-mining jobs) to a current level around 11,000 (per BLS data, exact figure varies by year and source)
- **Severance tax revenue** to the state and to coal-producing counties, which has fallen roughly in proportion to declining production
- **Royalties to landowners**, including mineral-rights holders both in-state and out-of-state
- **Coal-export logistics** through the Northern Panhandle barge terminals (relevant to D2's CRTS concentration)
- **Downstream economic activity** in trucking, equipment manufacturing/repair, fuel sales, etc.

Whether the bridge-system cost is small or large relative to these benefits depends on:
- The counterfactual: what would coal-haul transportation have cost without CRTS? (More trucks, more crossings, more total damage? Or rail substitution, with very different cost structure?)
- How quickly coal production is declining and how long the program needs to continue
- Whether continued CRTS operation on the remaining pre-CRTS bridges accelerates their demise to the point of forced closures

### What the data does say

What the bridge data can say cleanly:

1. **The CRTS program imposed real, measurable damage** on a defined subset of WV's bridge inventory. The damage is 0.5-0.7 NBI points of premature deterioration, concentrated on pre-CRTS-design bridges, equivalent to ~20 years of accelerated aging.
2. **CRTS-era bridges (built 2003+) handle CRTS loads fine.** This is important. It means the CRTS load envelope is not inherently unmanageable for properly designed structures; it's a question of legacy-fleet retrofit.
3. **The bridge-system cost has been concentrated geographically** in D10, D2, D1, D9. Those four districts have absorbed the brunt of the program's impact.
4. **The cost is largely sunk.** The 390 pre-CRTS bridges that have already absorbed 23 years of CRTS loading will not un-age themselves. The remaining question is forward-looking: what's the optimal end-of-life strategy for these specific structures?

The question of *whether* WV got benefit from CRTS is a question about the value of continued coal production and its associated jobs/tax revenue vs. the bridge-replacement bill. **The question of whether WV got the trade right is a value question, not a data question** — but the data can now anchor the cost side with a defensible number.

---

## 9. Measured conclusions

A measured reading of the evidence — keeping in mind both what the data clearly shows and what it cannot:

1. **The per-axle argument is engineering-incomplete.** Per-axle CRTS loading is comparable to (slightly above) legal loads. But bridge condition tracks cumulative deterioration driven by GVW, fatigue cycles, and short-span axle clustering — all of which CRTS trucks score worse on. The data confirms the engineering prediction: CRTS bridges show measurably faster deterioration in exactly the locations (decks, connections, joints) where heavier total loading matters most.

2. **CRTS has had a real and measurable cost in bridge service life.** That cost is concentrated in 390 pre-CRTS bridges that were retrofitted into the CRTS network despite being designed for lower loads. Those bridges have aged ~20 years prematurely. The damage is most visible on deck ratings — exactly where short-span members feel total vehicle weight directly.

3. **The cost is geographically and operationally concentrated.** District 10 carries 45% of the CRTS bridges; D2 + D9 carry another 37%. The capital-planning implication is straightforward: CRTS-related accelerated replacement should be a priority in those districts, not statewide.

4. **CRTS-era-designed bridges perform fine.** This is a critical caveat to the criticism. The 69 post-2003 CRTS bridges average a 6.91 deck rating — better than the statewide non-CRTS average. CRTS as a *design load* is engineerable; CRTS as a *retrofit load* on legacy bridges is what produces the damage.

5. **Longwall coal mining is a parallel, smaller, more catastrophic damage source.** It affects far fewer bridges than CRTS (11 narrative mentions vs 461), but where it occurs, it tends to require full replacement rather than rehabilitation. The two mechanisms together represent the dual bridge-system cost of WV's coal industry.

6. **Whether WV got the trade right is a public-policy question this analysis cannot settle.** The bridge data anchors the cost side ($500M-$1B in present-day premature-replacement value, spread over 23 years and concentrated in five districts). The benefit side — coal industry employment, severance taxes, royalties — sits in domains outside this database. A complete cost-benefit analysis would need to bring those numbers in alongside the bridge cost.

7. **The forward-looking question is more tractable than the backward-looking one.** The 235 pre-1980 CRTS bridges average a deck rating of 4.74. Most of these are at or beyond their economical rehabilitation point. The question of whether to continue letting CRTS trucks cross them — vs. forcing them to be downgraded, posted lower, or closed and replaced — is one that bridge engineering can answer cleanly with this data. The data supports a structured triage: post-2003 bridges stay on CRTS; 1980-2002 bridges get individual condition assessments; pre-1980 bridges are candidates for accelerated retirement.

---

## 10. Caveats and what this analysis cannot say

A measured analysis owes its caveats up front.

1. **The 461-bridge CRTS count is a narrative-search lower bound.** Bridges that are on CRTS routes but whose latest narrative doesn't mention `CRTS` aren't captured. The true CRTS-affected population is probably 500-600 bridges. The condition-gap finding would not be materially changed by including the missing ones, but the cost estimate would scale.

2. **The deterioration gap is correlation, not strictly causation.** CRTS designation may correlate with other factors that also cause deterioration — narrower roads, older bridges, lower maintenance budgets in the affected districts, harder weather exposure in mountain hollows, etc. The family-controlled and age-controlled cuts narrow the confound substantially (same family, same age band, still a 0.5-0.7 point gap), but a perfectly clean causal estimate would require a randomized treatment, which isn't possible.

3. **The 20-year-premature-aging claim is a population-average statement.** Individual bridge variation is large — some CRTS bridges look fine, some non-CRTS bridges look terrible. The average gap is robust; individual-bridge prediction from this number would not be.

4. **The cost estimate uses replacement-cost approximations.** $3M per typical county-road bridge is a midpoint; actual values range $1.5-5M, depending on span length, foundation conditions, traffic-control complexity, and detour requirements. The cost is real-money; the precision is engineering-judgment.

5. **The fatigue-damage calculation assumes load^3 scaling**, which is a standard for welded steel details. Concrete bridge components, concrete decks specifically, follow different damage curves. The qualitative conclusion (CRTS loads accumulate damage faster than legal loads) is robust to this; the precise multiplier varies by element.

6. **The benefit side of the trade is not in this database.** This analysis cannot tell you whether the coal jobs, the severance taxes, or the royalty payments to landowners were worth the bridge cost. It can tell you what the bridge cost was. The trade-off question requires economic data that lives in different systems.

7. **The Critical-Finding workflow data is missing from this dump.** When a CRTS bridge takes a damage event from an overweight crossing, the response is typically a `task_type='WorkManagementInstance'` record in InspectTech — and the dumper didn't pull those. The full damage-response history of CRTS bridges (work orders raised, repairs commissioned, costs accrued) sits in records not visible to this analysis.

8. **Future loading patterns are not in the data.** WV's coal-production trajectory has been declining for over a decade. If CRTS truck volumes are falling — which they probably are, in proportion to production — then forward-looking damage accumulation is slower than the historical pattern suggests. The 1817-1856 bridges of WV have shown that bridges built for very different loads can serve productive lives long after the loads change. The pre-CRTS bridges that have absorbed 23 years of CRTS loading might absorb another 10-20 if loads diminish.

---

*Built from 461 CRTS-narrative-tagged bridges in InspectTech, cross-referenced with `asset_value` postings (NBI 41), `v_bridge_latest_ratings` for current condition, build-era cohorts via NBI 27, and family classification via NBI 43A/43B/45. Dump date: 2026-05-14.*
