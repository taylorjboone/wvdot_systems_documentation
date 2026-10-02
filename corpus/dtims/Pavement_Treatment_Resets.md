# Treatment resets of the raw pavement values, from past TheHub projects

**Study date:** 2026-09-29. This is the companion to [Raw distress deterioration](/docs/Pavement_Raw_Distress_Deterioration) (the deterioration curves); how the study was done is in [Raw Distress Study — Process](/docs/Pavement_Raw_Distress_Study). Same data, same route-average method:
- raw vendor survey 2020–2025;
- TheHub projects;
- MMS lines.

**Scripts** (in `dtims_docs/raw-deterioration-study-2026-09-29/`): `scripts/resets.py`, `scripts/resets_analyze.py`. **Output:** `results/resets_out.txt`.

---

## 1. Recommended resets

What each treatment does to the four MAP-21 raw values on the surveyed pavement, and the logical reset rule.

| Surface / class | Treatment (TheHub code → config treatment) | IRI | FHWA cracking | Rut | Faulting | Class after |
|---|---|---|---|---|---|---|
| **BC** | Thin overlay 1"–<2" (08 → THIN_OVERLAY) | **Partial:** `IRI′ = 80 + 0.42·(IRI − 80)`; Interstate → ~57 | **→ 0** | **→ 0.08** | n/a | BC, rehab Minor |
| **BC** | Thick overlay ≥2" (68 → THICK_OVERLAY) | **Partial, lower floor:** `IRI′ = 45 + 0.42·(IRI − 45)` | **→ 0** | **→ 0.08** | n/a | BC, rehab Major |
| **BC** | Ultra-thin <1" (67 → ULTRA_THIN_OVLY) | Partial like thin: `IRI′ = 80 + 0.45·(IRI − 80)`, but IRI climbs back **+10 in/mi/yr** | **→ 0** | **→ 0.08** | n/a | BC, Minor |
| **BC** | Surface treatment: chip / cape / HFST (13, 14, 59 → CHIP_SEAL / CAPE_SEAL) | **Small:** `IRI′ ≈ 0.93·IRI − 17` (≈ −10 to −20) | **→ ~0.5** | **→ 0.08–0.10** | n/a | BC, Minor |
| **BC** | Microsurfacing (26 → MICROSURFACING) | **None** (×0.94) | **no reset** (0.5 → 0.5), then reflective cracking **+3 pts/yr** | no change | n/a | BC, Minor |
| **BC** | New pavement / reconstruction (07, 02, 04, 24, 66 → RECONSTRUCT_BC) | **Full:** `IRI′ ≈ 50–60` (thin data) | **→ 0** | **→ 0.08–0.09** | n/a | BC, Initial |
| **RC** | Diamond grind / CPR (75 → MINOR/MAJOR_CPR_DG) | **Full:** `IRI′ ≈ 50–75` (n = 3) | → ~0.4–1 (slabs not replaced stay cracked) | n/a | **→ ~0.02** | RC, Minor |
| **RC → composite** | HMA overlay on concrete (08/68 on JCP/CRC) | `IRI′ ≈ 0.86 × IRI` (86 → 74, n = 6) | → ~0.2 | → 0.09 | **not measured** after (vendor rates it as ASP) | **BC** (composite), Minor/Major |

**The four rules behind the table:**
1. **Cracking is a full reset** for anything that places a new wearing course: every HMA overlay and every chip / cape seal. After the work it is about 0 whatever it was before (median 0.01%; slope on the before-value 0.00). Microsurfacing is the exception: it does not reset cracking, and cracking returns fast.
2. **Rut is a fixed reset** of about 0.08 in for HMA overlays and seals, whatever the rut was before (median-regression slope 0.00). Microsurfacing, sold as rut-fill, did not change rut here (0.12 → 0.13).
3. **IRI is a partial reset toward a floor.** It keeps ~42–45% of the before-roughness above the floor. Thick overlays have a lower floor than thin ones, and Interstates reset to ~57 almost regardless of the before-value. Seals and microsurfacing barely change IRI.
4. **Faulting** resets only with concrete grinding / CPR. An HMA overlay on concrete moves the segment to BC (composite), and faulting stops being a rated metric.

Which class the segment is in after the treatment matters only through **surface** (BC / RC / composite) and **route group**. The deterioration study found truck load doesn't change rates, and it doesn't change resets either (§3.3).

---

## 2. Data

### 2.1 Projects

- Every TheHub project with a route segment, not withdrawn / terminated / reserve, **completed** (milestone 20 actual, else the construction phase end on a closed phase) from 2015 on.
- It must carry a pavement construction code, or STIP program 6.

**Grouping of the TheHub construction codes:**

| Group | Codes |
|---|---|
| ULTRA_THIN | 67 (Ultra Thin HMA O/L < 1") |
| THIN_OVERLAY | 08 (Minor HMA O/L 1"–<2") |
| THICK_OVERLAY | 68 (Major HMA O/L ≥ 2") |
| SURFACE_TRT | 13 chip seal, 14 resurface (surface treatment), 59 HFST |
| MICROSURFACING | 26 |
| NEW_PAVE | 07 (pave HMA or PCC on existing road) |
| RECONSTRUCT | 02, 04, 24, 66 |
| SKIP_PAVE | 09 |
| BASE_REPAIR | 16 |
| CPR_GRIND | 75 |

The code names in TheHub today differ from `Import_Past_Projects.md`: 08 is "1" to <2"" (doc: 1.5"–2") and 67 is "< 1"" (doc: < 1.5").

### 2.2 Extent

- The project's route segment milepoints, with 0.1 mi trimmed at each end.
- Records flagged bridge / construction / lane deviation / wet / railway are removed.
- At least 5 records (0.5 mi) per survey.

### 2.3 Two views

| View | Definition | Size |
|---|---|---|
| **A. Before → after** | The last survey before construction started (up to 4 years before), against the first survey after completion (up to 3 years; used ≤ 2 years, median 0.65 years), over the same extent. Pairs with another pavement project or MMS paving on the extent in between are dropped. IRI may span the 2022/2023 vendor change; cracking and rut only within one vendor era (deterioration study §3). | 304 extents / 261 projects; 218 clean, 171 with IRI on asphalt |
| **B. Level by age since completion** | Every 2023–2025 survey after completion, with no later work on the extent. Gives the reset level (the age-0 intercept) and the early-life growth. It mostly shows the after-state: before-surveys are rare because only 2024 covers the whole network. | 1,996 readings on 1,402 projects (thin overlay 1,443 / 1,028) |

---

## 3. Results

### 3.1 Before → after on asphalt

View A: clean extents, after survey ≤ 2 years after completion, median of extents (miles-weighted).

| Treatment | n | IRI before → after | Ratio | FHWA crack before → after | Rut before → after |
|---|---|---|---|---|---|
| Surface treatment | 15 | 94 → 55 | 0.68 (reg. 0.93·IRI − 17) | 24.3 → 0.02 | 0.199 → 0.071 |
| Microsurfacing | 8 | 70 → 68 | 0.94 | 0.53 → 0.54 | 0.118 → 0.128 |
| Ultra-thin | 16 | 106 → 72 | 0.80 | 0.27 → 0.00 | 0.126 → 0.079 |
| **Thin overlay** | **133** | **100 → 86** | **0.84** | **4.55 → 0.03** | **0.166 → 0.077** |
| Thick overlay | 16 | 92 → 74 | 0.70 | 22.5 → 0.16 | 0.216 → 0.068 |
| New pavement (07) | 6 | 120 → 100 | 0.83 | 10.0 → 0.03 | 0.204 → 0.094 |
| Reconstruction | 3 | 77 → 52 | 0.67 | — | — |

### 3.2 IRI: partial reset

**Thin overlays, alone (n = 133):** `IRI′ = 31 + 0.47·IRI_before + 6.9·age` (t = 14 on the before-value). The median regression is 33 + 0.44·IRI.

**All HMA overlays (n = 171, R² 0.59):**

`IRI′ = 46.6 + 0.418·IRI_before − 20.9·[thick] − 13.4·[ultra-thin] − 13.9·[Interstate] + 4.5·age`

- Thick overlay: t = −2.5.
- Ultra-thin: t = −1.6.
- Interstate: t = −3.0.
- HPMS_1 and OTHER don't differ.

The same model in logs gives an elasticity of 0.51 (`IRI′ ∝ IRI^0.51`), so a multiplicative "keep ~half" rule fits about as well.

Written as the gap to a floor, `IRI′ = F + 0.42·(IRI − F)`:

| Case | Floor F |
|---|---|
| Thin | ≈ 80 |
| Ultra-thin | ≈ 57 |
| Thick | ≈ 45 |
| Interstates (thin overlay: before 65 → after 57, no dependence on before) | ≈ 57 |

The ultra-thin coefficient is weak (n = 16, t −1.6), so the table in §1 treats ultra-thin like thin (F = 80, keep 0.45).

**After the overlay** (view B, median regression over ages 0–6):

| Treatment | IRI after the overlay |
|---|---|
| Thin overlay | flat: −1.5 in/mi/yr |
| Thick overlay | flat: −1.3 in/mi/yr |
| Ultra-thin | back up +11.6 in/mi/yr |
| Surface treatment | +5.6 in/mi/yr |

That flat stretch after thin and thick overlays is the ~3-year IRI hold in the deterioration study.

### 3.3 IRI reset level by class

Thin overlays, age ≤ 2, view B, median after-level:

| Class | n | Miles | IRI after | FHWA crack after | Rut after | AADT |
|---|---|---|---|---|---|---|
| INTERSTATE | 26 | 80 | 57 | 0.03 | 0.089 | 19,500 |
| HPMS_1 | 62 | 218 | 86 | 1.36 | 0.092 | 4,400 |
| OTHER | 682 | 1,812 | 145 | 0.39 | 0.091 | 1,600 |
| Truck H | 88 | 289 | 100 | 1.20 | 0.087 | 5,400 |
| Truck L | 682 | 1,821 | 142 | 0.36 | 0.092 | 2,200 |

The IRI after a thin overlay depends on the road class (57 → 86 → 145). The before-roughness explains most of that, since low-volume roads start much rougher, and the partial-reset formula captures it. Cracking and rut reset to the same values in every class. Truck load separates nothing once the route group is known.

### 3.4 Cracking and rut after the reset

View B, asphalt after-surface. Median of extents by age since completion, number of extents in brackets.

**FHWA cracking (%):**

| Treatment | 0–1 yr | 1–2 | 2–3 | 3–4 | 4–6 | 6+ |
|---|---|---|---|---|---|---|
| Surface treatment | 0.64 [82] | 2.14 [27] | 1.36 [11] | 2.28 [8] | 1.96 [14] | 24.5 [4] |
| Microsurfacing | 0.71 [10] | 2.24 [2] | 8.57 [1] | 13.2 [3] | 19.0 [8] | — |
| Ultra-thin | 0.13 [11] | 0.78 [17] | 0.80 [18] | 4.36 [19] | 6.50 [32] | 1.67 [9] |
| Thin overlay | 0.13 [372] | 0.83 [410] | 1.87 [227] | 1.65 [185] | 3.04 [171] | 7.46 [49] |
| Thick overlay | 0.10 [76] | 2.00 [28] | 0.43 [21] | 1.17 [9] | 4.38 [14] | 7.70 [5] |

**Share of extents still crack-Good (< 5%):**

| Treatment | 0–1 | 1–2 | 2–3 | 3–4 | 4–5 | 5–6 | 6–8 |
|---|---|---|---|---|---|---|---|
| Surface treatment | 0.73 | 0.70 | 1.00 | 0.88 | 0.85 | — | 0.00 |
| Microsurfacing | 0.70 | 0.50 | 0.00 | 0.00 | 0.00 | — | — |
| Ultra-thin | 0.73 | 0.82 | 0.83 | 0.68 | 0.53 | 0.60 | 0.43 |
| Thin overlay | 0.92 | 0.86 | 0.70 | 0.72 | 0.60 | 0.57 | 0.42 |
| Thick overlay | 0.86 | 0.68 | 0.90 | 0.89 | 0.58 | 0.50 | — |

**Post-reset growth by treatment**, in the deterioration study's √C form C(t) = (√C₀ + s·t)²:

| Treatment | √C₀ | s /yr | Notes |
|---|---|---|---|
| Thin overlay | 0.27 | 0.36 | The same as untouched roads (0.42). After a reset, cracking follows the ordinary curve from ~0. |
| Thick overlay | ~0 | 0.39 | |
| Surface treatment | 0.35 | 0.19 | Seals slow the visible cracking. |
| Microsurfacing | | | Reflective: +3.3 pts/yr linear. Crack-Good is gone within 2–3 years. |
| Ultra-thin | | | Holds for ~3 years, then reflects (4.4% at 3–4 yr). |

**Rut after the reset**, 2024 offset absorbed:

| Treatment | Rut in / yr |
|---|---|
| Thin overlay | 0.004 |
| Thick overlay | 0.009 |
| Ultra-thin | 0.002 |
| Surface treatment | 0.022 (embedment) |

So rut starts about 0.08–0.10 in and stays near 0.10 for 6+ years on overlays.

### 3.5 Concrete and composite

| Case | Before → after | Source |
|---|---|---|
| CPR / diamond grind (75) | IRI → 49 (n = 2 at 0–1 yr), 75 at ~2.4 yr; faulting 0.021; FHWA cracking ~0.4–1.1 | view B, JCP after-surface |
| HMA overlay on PCC (6 extents, 30 mi, 2020–22 before) | IRI 86 → 74, crack 0.5 → 0.2, faulting 0.026 → 0.029, surface becomes ASP | view A |
| Thin overlay recorded on still-JCP surface (19 readings) | IRI 71, crack 1.7, faulting ~0 | view B; likely shoulders / partial coverage |

Only 4 extents could be shown to be composite (concrete in an earlier survey, asphalt after), too few to tell whether composites crack back faster than full-depth asphalt. Carry the assumption, and watch it, until the 2026 survey adds more.

---

## 4. Against the current AMPS resets

**Config 1 has no raw-distress resets.** Every treatment moves the dTIMS indices, and the raw values are re-derived from them:

| Op | What it does |
|---|---|
| `IDX_ADD_CAP` / `IDX_SET` | PSI / RDI / SCI / CCI +x or set to 5 |
| `IRI_MIN_PSI` / `IRI_FROM_PSI` | IRI from the new PSI |
| `RUT_FROM_RDI` | rut from the new RDI |
| `PCRK_MIN_AGE` / `PCRK_FROM_AGE` | cracking = crack factor × age |

The engine side (what those ops produce on real segments) is in §4.1.

### 4.1 Engine-implied resets

`scripts/engine_resets.py`: config 1, every active treatment applied through `dtims_state.simulate(plan=…)` → `apply_treatments` on 56,240 BC segments (5,071 mi) and 4,907 RC segments (404 mi). Fit is `after = a + b·before`; medians are length-weighted.

| Treatment | IRI: engine | IRI: observed | Cracking: engine | Cracking: observed | Rut: engine | Rut: observed |
|---|---|---|---|---|---|---|
| CHIP / CAPE SEAL | **unchanged** (1.00·b) | `0.93·b − 17` (−10 to −20) | chip 1.3 + 0.35b; cape 1.6 + 0.36b | **→ ~0.5** | unchanged | **→ 0.07–0.10** |
| MICROSURFACING | 37 + 0.51b | unchanged | 1.3 + 0.33b | unchanged, then +3/yr | **→ 0** | unchanged (0.12–0.13) |
| ULTRA_THIN_OVLY | 39 + 0.45b | ~26 + 0.49b | 0.6 + 0.33b | **→ 0** | **→ 0** | → 0.08 |
| THIN_OVERLAY | 38 + 0.40b (103 → 81) | 33 + 0.44b (100 → 86) — **close** | 0.4 + 0.31b (20% → 6–7%) | **→ 0** | **→ 0** | → 0.08 |
| THICK_OVERLAY | 57 + 0.04b (→ 65 flat) | 40 + 0.31b (92 → 74) | 0.4 + 0.02b | → 0 | → 0 | → 0.07 |
| RECONSTRUCT_BC | **65 fixed** | ~52–60 (n = 3) | 0.85 | → 0 | → 0 | → 0.09 |
| RECONSTRUCT_RC | 65 fixed, **pavement → BC** | — | 0.76 | — | → 0 | — |
| MINOR / MAJOR_CPR_DG (identical) | 70 + 0.05b (→ 81) | → 49–75 | → 0 | → 0.4–1.1 | unchanged | — |
| CRACK_SEAL | 19 + 0.79b | no data | 1.6 + 0.14b | no data | **raised** 0.121 → 0.146 (RUT_FROM_RDI drops the offset) | no data |
| SAW_SEAL_JOINTS | 25 + 0.75b | no data | unchanged | no data | unchanged | no data |

**Where the engine's resets are wrong for the raw values:**

1. **Cracking never resets to 0.** `PCRK_MIN_AGE` / `PCRK_FROM_AGE` set cracking to crack factor × (age + 1). So a reconstruction starts at 0.6–1.1%, and an overlay keeps ~⅓ of the before-cracking: 20% becomes 6–7%, and thin-overlay p95 is 18%. Observed, every overlay and seal takes FHWA cracking to ~0 (median 0.01%, slope 0.00).
2. **Rut is overwritten from RDI.** `RUT_FROM_RDI` replaces measured rut with h(RDI) and drops the offset:
   - treatments that set RDI to 5 give **rut = 0** (observed 0.08);
   - crack seal, which doesn't touch RDI, **raises** rut;
   - microsurfacing zeroes rut, although observed it doesn't change.
3. **IRI after overlays is about right for thin overlays** (the engine's 38 + 0.40b against the observed 33 + 0.44b). But:
   - thick overlays and reconstruction are pinned to a fixed 65 by PSI = 5 (observed: still partial for thick, ~52–60 for reconstruction);
   - chip and cape seals leave IRI untouched (observed −10 to −20);
   - microsurfacing improves IRI in the engine but doesn't in the survey.
4. **RECONSTRUCT_RC sets the pavement to BC** (op 220 `PAVE_SET BC`): all 404 RC mi come out asphalt and move onto BC curves. If WVDOT rebuilds concrete as concrete this is a bug. If reconstruction means an asphalt rebuild, the treatment is misnamed and should be the RC→BC composite / new-BC case.
5. **CPR / grinding treats Minor and Major identically** and lands every segment at IRI ~81 (g(PSI 4.5)), whatever it was before.
6. **Faulting never changes** (`FLT_SET 0` acts on a starting faulting that is already 0; §3 of the deterioration study).
7. **After the reset, cracking grows linearly** at the route-group factor (0.56/yr) for every treatment. Observed growth is the √C curve (0.36–0.39/yr in √C, i.e. ~3% at year 4–6, 7–8% at year 6+). Seals grow slower (0.19) and microsurfacing faster (+3 pts/yr).

---

## 5. Proposed reset table for a raw-distress model

One row per treatment × surface. Proposal only; nothing in the config or engine was changed.

| Treatment | Applies to | IRI | FHWA cracking | Rut | Faulting | Then (deterioration study curves) |
|---|---|---|---|---|---|---|
| CHIP_SEAL / CAPE_SEAL | BC | `0.93·IRI − 17`, min 45 | 0.5 | 0.09 | — | √C slope 0.19/yr; IRI +5.6/yr; rut +0.02/yr |
| MICROSURFACING | BC | unchanged | unchanged | unchanged | — | cracking +3 pts/yr for 3 yr, then the usual curve |
| ULTRA_THIN_OVLY | BC | `80 + 0.45·(IRI − 80)` if IRI > 80 | 0 | 0.08 | — | IRI +10/yr; cracking held 3 yr then √C 0.42/yr |
| THIN_OVERLAY | BC | `80 + 0.42·(IRI − 80)` if IRI > 80; Interstate 57 | 0 | 0.08 | — | IRI held 3 yr (⅓ rate); √C 0.36/yr |
| THICK_OVERLAY | BC | `45 + 0.42·(IRI − 45)`; Interstate 50 | 0 | 0.08 | — | IRI held 3 yr; √C 0.39/yr |
| RECONSTRUCT_BC | BC, RC (→ BC) | 55 | 0 | 0.08 | 0 | curves from new; rehab Initial |
| THIN/THICK_OVERLAY on RC | RC → **BC composite** | `0.86·IRI` | 0.2 | 0.09 | dropped (not rated on BC) | BC curves; watch reflective cracking |
| MINOR/MAJOR_CPR_DG | RC | 60 | ×0.3 (Minor) / ×0.1 (Major) | — | 0.02 | JCP linear rates |
| CRACK_SEAL / SAW_SEAL_JOINTS | BC / RC | unchanged | unchanged (sealed cracks are still rated) | unchanged | unchanged | a hold on cracking growth if wanted — there is no TheHub data for it (not a TheHub project type) |

**Notes on the proposal:**
- **Floors apply one way.** A reset never makes a road rougher: `IRI′ = min(IRI, rule)`.
- **CPR grinding cracking multipliers** assume slab replacement fixes the worst slabs. There are only 3 extents; refit when there are more.
- **Crack seal and joint seal** have no TheHub or MMS evidence here: 208 / 244 are MMS joint and crack sealing, only since mid-2024. Leave them as a hold, not a reset.
- **The class changes a treatment makes:**
  - an HMA overlay on RC → BC (composite);
  - reconstruction → the surface actually built (config 1's RECONSTRUCT_RC currently sets pave to BC — check that is intended);
  - rehab type Minor / Major / Initial as today.
  Truck load and route group don't change.

---

## 6. Limits

- **View A is small** (171 asphalt IRI pairs, 102 same-era distress pairs), because only 2024 surveys the whole network. It will more than double with the 2026 survey.
- **TheHub milepoints** are the project's route segments. They can be longer than the paved stretch, so a p90 after-cracking of 6% shows up in view A. Medians and median regression are used throughout.
- **Some routes are paved more than once in 2015–2025.** Later work is excluded from each reading, but an earlier treatment under the one studied isn't known.
- **Microsurfacing, surface treatment and concrete numbers rest on 3–30 extents each.** Thin overlays (1,000+ projects) and thick overlays (~100) are the solid rows.

---

## 7. Reproducing

After steps 1–3 of the deterioration study (`load_raw.py`, `pull_hub_mms.py`, `build_pairs.py`, with the same `STUDY_DIR`):

```sh
S=dtims_docs/raw-deterioration-study-2026-09-29/scripts
python $S/resets.py              # before/after and after-by-age datasets
python $S/resets_analyze.py      # the tables in §3                          -> results/resets_out.txt
PYTHONPATH=. python $S/engine_resets.py   # config 1 treatments applied by the engine (§4.1)
```
