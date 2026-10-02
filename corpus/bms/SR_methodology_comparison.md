# Sufficiency Rating: Old vs New Methodology

A line-by-line technical comparison of WV DOH's legacy FHWA Sufficiency Rating ("Old SR") and the proposed new methodology ("New SR") that replaces it.

The Sufficiency Rating is a single number from 0 to 100 that ranks bridges by overall fitness for service. FHWA uses 50 as the threshold for "rehab eligible" and 80 for "replacement eligible" in federal funding programs. Lower number = worse bridge.

Both methodologies break the score into category buckets that are summed at the end:

| Category | Old | New | Maximum |
|---|---|---|---|
| **S1** Structural Adequacy & Safety | A + B | A + B + C + D | 55 |
| **S2** Functional Obsolescence | J + (G+H) + I | J + (G+H) + I | 30 |
| **S3** Essentiality for Public Use | A + B | A + B + C | 15 |
| **S4** Special Reductions | A + B + C | — *(removed)* | 13 |
| **Final SR** | S1 + S2 + S3 − S4 (only if S1+S2+S3 ≥ 50) | S1 + S2 + S3 | 0–100 |

The maximum within each category is the *unpenalized* value; penalties are subtracted from that ceiling.

---

## S1 — Structural Adequacy & Safety (55 pts max)

### Part A: Worst-rated component (super/sub/culvert)

**Identical** in both methodologies. Take the lowest condition rating among the superstructure, substructure, or culvert, and apply this table:

| Lowest rating | Penalty A |
|---|---|
| ≤ 2 | 55 |
| 3 | 40 |
| 4 | 25 |
| 5 | 10 |
| ≥ 6 | 0 |

Data sources: Old uses NBI items 59 (super), 60 (sub), 62 (culvert). New uses SNBI B.C.02, B.C.03, B.C.04.

### Part B: Load Capacity

**Different formula, different math.**

**Old:**
```
B = ((32.4 − IRm)^1.5) × 0.3254   capped at 0–55
```
where IRm is the Inventory Rating in **metric tons** (NBI item 66 × 0.907185). 32.4 mt = 35.7 US tons, the AASHTO design load. The 0.3254 coefficient and 1.5 exponent come from the legacy FHWA SR formula book.

**New:**
```
B = 55 × (1 − IRR)^1.8   capped at 0–55
```
where IRR is the Inventory Load Rating Factor (SNBI B.LR.05) directly — a ratio of capacity to AASHTO design load. The factor 35.7 is now embedded in IRR's definition rather than appearing as a tonnage threshold.

Effect: at IRR = 1.0 both formulas give B = 0. At IRR = 0 both give B = 55. In between, **the new curve is more lenient** — at IRR = 0.5, Old gives B ≈ 21, New gives B ≈ 16. The 1.5 → 1.8 exponent change deliberately softens the penalty to make room for the new C and D penalties.

### Part C: Structure / Span Type (NEW only)

The legacy formula had this penalty in S4 (Special Reductions). It was relocated to S1 in the new methodology because span type genuinely affects structural risk.

**New:**
- 8 pts if `B.SP.05 = 5` (cantilever with pin-and-hanger — special fatigue risk)
- 5 pts if `B.SP.06` is one of: `T02` (truss-through), `A04` (arch-through), `L01`-`L03` and `LX` (cable suspension/stayed/extradosed/other), `M01`-`M03` and `MX` (moveable: lift/bascule/swing/other)
- 0 pts otherwise

The 5-pt penalty applies to "fracture-critical-style" bridge geometries where a single member failure can collapse the structure.

Old: no equivalent in S1 — the legacy S4.B penalty used NBI item 43 codes (10, 12–17) for similar geometry, also capped at 5 pts, and was only subtracted from the total SR when S1+S2+S3 ≥ 50%.

### Part D: Scour (NEW only)

Old had no scour penalty in S1. New adds one based on **scour condition** (B.C.11) and **scour vulnerability** (B.AP.03):

**Scour condition penalty d1:**

| B.C.11 rating | d1 |
|---|---|
| 9 or "N" | 0 |
| 8 | 1 |
| 7 | 2 |
| 6 | 3 |
| 5 | 5 |
| 4 | 8 |
| < 4 | 10 |
| missing (blank) | 10 |
| non-numeric string ("MI-T" etc.) | 1 |

**Scour vulnerability penalty d2:**

| B.AP.03 | d2 |
|---|---|
| D, E, U | 10 |
| C | 8 |
| A, B, N | 0 |

`D = max(d1, d2)`, range 0–10.

### Final S1

```
S1 = max(0, 55 − (A + B + C + D))
```

---

## S2 — Functional Obsolescence (30 pts max)

### Part J: General Rating Reductions

Sum of six condition-rating penalties, capped at 13 (Old) or 15 (New). The big change is **deck weight**:

| Sub-penalty | Old tiers (rating ≤3 / =4 / =5 / >5) | New tiers |
|---|---|---|
| Deck (NBI 58 / B.C.01) | 5 / 3 / 1 / 0 | **9 / 6 / 3 / 0** |
| Structural Eval (NBI 67) | 4 / 2 / 1 / 0 | 4 / 2 / 1 / 0 |
| Deck Geometry (NBI 68) | 4 / 2 / 1 / 0 | 4 / 2 / 1 / 0 |
| Underclearances (NBI 69) | 4 / 2 / 1 / 0 | 4 / 2 / 1 / 0 |
| Waterway Adequacy (NBI 71) | 4 / 2 / 1 / 0 (uses ≤3 / =4 / =5 thresholds) | New mapping: =6 → 4, =5 → 3, =4 → 2, =3 → 1, else 0 (uses B.AP.02 Overtopping Likelihood — inverted scale) |
| Approach Roadway Alignment (NBI 72 / B.AP.01) | Numeric scale 0–9 → 4 / 2 / 1 / 0 | Letter scale: P → 6, F → 2, G → 0 |

Deck condition's penalty tripled in the new methodology, signaling that WV considers driver experience and deck deterioration more important than the old formula's weight.

The Structural Evaluation (67), Deck Geometry (68), and Underclearances (69) values are **calculated**, not stored as raw inputs:

- **Table 1** (NBI 67 / "Structural Eval"): function of ADT bucket, inventory rating in metric tons, and worst of super/sub/culvert. Returns a 0–9 appraisal rating.
- **Table 2** (NBI 68 / "Deck Geometry"): function of bridge width, approach width, lanes, direction of travel, functional class, service type, and bridge length. Multi-scenario lookup — pick the worst rating across "main span 2A/2B/2C/2D" and "clearance 2E" sub-tables.
- **Table 3** (NBI 69 / "Underclearances"): function of vertical/horizontal underclearance values, functional class under, service under. Only applies if the bridge passes over something.

These three tables are carried over from legacy FHWA documentation. Both Old and New use the same tables; the value is plugged into different penalty tiers (which are identical for these three items anyway).

### Part G: Roadway-Width Narrowing

Both Old and New apply 5 pts if `BridgeRoadwayWidth + 0.6 m < ApproachRoadwayWidth` (in meters), excluding culverts.

**New adds two additional triggers** for multi-lane bridges (width per lane `Y = BRW / lanes / 3.28084` meters):
- 3 pts if `Y < 2.75 m` (lane width below 9 ft)
- 2 pts if `Y < 3.00 m`

The narrowing penalty is `max` of the applicable triggers (so 5 wins over 3 wins over 2).

### Part H: Traffic Capacity

**Completely different.**

**Old:** A lookup table indexed by ADT-per-lane (X) and width-per-lane in meters (Y). Six X buckets × five Y bands give a 0–15 pt penalty. Special 1-lane handling: if `Y < 4.3 m` → 15 pts; `4.3 ≤ Y < 5.5` → linear; `Y ≥ 5.5` → 0.

**New:** A continuous formula plus the 1-lane override:
```
Wf = 1               if 1 lane
   = 0.1             if Y ≤ 2.75 m
   = (Y − 2.75) / 0.85   otherwise (capped at 1)

H1 = min(15, 15 × ( ADT / (8000 × lanes × Wf) )^1.5 )

H2 = 15                       if 1-lane and Y < 4.3
   = 15 × (5.5 − Y) / 1.2     if 1-lane and 4.3 ≤ Y < 5.5
   = 0                        otherwise

H  = max(H1, H2)
```

The 8000 in the denominator is a reference ADT; 1.5 is the curve steepness. The width factor `Wf` rewards lane widths above the 9-ft minimum.

`G + H` is capped at 15 pts.

### Part I: Vertical Clearance

**Identical** in both methodologies. 2 pts if vertical clearance over the bridge roadway is below threshold (4.87 m / 16 ft for STRAHNET routes, 4.26 m / 14 ft otherwise), 0 otherwise.

### Final S2

```
S2 = max(0, 30 − (J + (G + H) + I))
```

---

## S3 — Essentiality for Public Use (15 pts max)

### Part A: ADT × Detour Length

**Different denominator.**

**Old:**
```
S3.A = 15 × (ADT × Detour_km) / (320000 × K)
K = (S1 + S2) / 85
```
The K factor amplifies the penalty if the bridge is already in bad shape — "punishing" a structurally deficient bridge that also has a long detour.

**New:**
```
S3.A = 15 × (ADT × Detour_mi) / 100000
```
The K factor is removed. ADT and detour have constant weight regardless of bridge condition. Denominator 100000 was chosen so that a 50,000-ADT bridge with a 2-mile detour gets the full 15-pt penalty (50000 × 2 / 100000 = 1 → ×15 = 15).

Both capped at 0–15.

### Part B: STRAHNET Highway Designation

**Identical:** 2 pts if NBI 100 / B.H.05 is not "N" / 0.

### Part C: Detour-Only (NEW only — moved from S4)

The legacy formula's S4.A was `Detour_km^4 × 7.9e-9` capped at 5 pts — and was only applied as a *reduction* to the final SR when the bridge already scored ≥ 50.

The new formula moves a softened version into S3 as a standalone penalty that always applies:
```
S3.C = 3 × (Detour_mi / 100)^0.585   capped at 0–3
```
Calibrated so a 100-mile detour = 3 pts (the new cap), and shorter detours scale gently. This ensures low-traffic bridges with long detours still get penalized for inconvenience — the K factor removal would otherwise neutralize their S3.A.

### Final S3

```
S3 = max(0, 15 − (S3.A + S3.B + S3.C))
```

---

## S4 — Special Reductions (Old only — REMOVED in New)

Legacy S4 was applied as a separate subtraction at the very end, and **only when S1+S2+S3 ≥ 50**. It contained three sub-penalties:

- **S4.A** Detour-only penalty: `Detour_km^4 × 7.9e-9`, capped 0–5. Moved into S3 as S3.C in the new formula.
- **S4.B** Bridge type penalty: 5 pts if NBI 43 code is in {10, 12, 13, 14, 15, 16, 17} (thru-truss, thru-arch, suspension, etc.). Moved into S1 as S1.C in the new formula and broadened.
- **S4.C** Traffic safety features (NBI 36 A–D): 1 / 2 / 3 pts for 2 / 3 / 4 zero ratings. **Removed entirely** in the new formula.

Quirk to be aware of: the legacy spreadsheet reads NBI 36 A–D as a concatenated 4-digit number (column 27 of the NBI tab). Because Excel stores `"0000"` as the integer `0`, bridges with all-zero safety ratings get scored as "1 zero" instead of 4, producing a 0-pt S4.C penalty when it should be 3. Either way, S4 is gone in the new formula.

---

## Final SR Formula

**Old:**
```
SR = max(0, min(100, S1 + S2 + S3 − (S4 if S1+S2+S3 ≥ 50 else 0)))
```

**New:**
```
SR = max(0, min(100, S1 + S2 + S3))
```

---

## Data-Handling Quirks Preserved in Both

The spreadsheet relies on Excel's blank-cell and type-coercion behavior in several places. To match its output exactly, the same conventions apply:

1. **Missing IR** → treat as IRR = 0 → maximum load penalty B.
2. **Missing super/sub/culvert ratings** in some chained lookups → treated as 0 → worst-case A.
3. **Missing scour condition (B.C.11) blank** → max penalty (10), but **non-empty string codes like "MI-T"** → only 1 pt (Excel's quirky text-vs-number comparison treats any string as "greater than" 8).
4. **Missing bridge roadway width (BRW = 0)** for culverts → still feeds the H lookup with Y = 0, producing a high traffic penalty for a "no-width" structure.
5. **Missing underclearance values ("N")** → the Excel error from `"N" × 0.3048` causes the IF chain to short-circuit to 0 (no penalty), not max penalty.

These aren't documented in the change spec but are baked into the production spreadsheet.

---

## Summary of What Changed

| Change | Old | New | Reason |
|---|---|---|---|
| Load capacity curve | exponent 1.5 | exponent 1.8 | Softer penalty leaves room for new C and D |
| Structure type | 5-pt special reduction at end | 5-pt (up to 8) S1 penalty | Always counted, not just when SR ≥ 50 |
| Scour | not penalized | up to 10-pt S1 penalty | New SNBI fields make it codeable |
| Deck condition weight in J | 5 / 3 / 1 / 0 | 9 / 6 / 3 / 0 | Driver experience emphasized |
| Traffic penalty H | discrete lookup table | continuous formula | Avoid table-edge discontinuities |
| Detour ADT formula | divided by (S1+S2) | constant denominator | Detour weight independent of condition |
| Detour-only penalty | 0–5 pt S4, conditional | 0–3 pt S3.C, always applied | Captures inconvenience even on low-ADT bridges |
| Traffic safety features | up to 3-pt S4 | removed | Penalty was buggy and rarely meaningful |
| S4 conditional subtraction | applied only if SR ≥ 50 | removed entirely | Simpler, no discontinuity at 50 |
