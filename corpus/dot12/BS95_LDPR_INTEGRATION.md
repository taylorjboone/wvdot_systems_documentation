# LDPR / BS95 Overhead Funding — Investigation & Integration

This documents the investigation into how **LDPR profiles** are derived for
**overhead programs**, and the resulting data + API integration. It is the
reference for why `bs95_crosswalk` exists and how the hub program API serves
overhead LDPRs.

---

## 1. The question

DOT-12 columns coded to an **overhead program** (a text Dimension-2 account
code like `MEXPR`, `EQPWO`, `AEXOH`, or a district annual plan `D07AP`) need an
**LDPR profile** — the labor-distribution funding key OASIS-HRM puts on a
timesheet line. For *project* (hub) columns the LDPR is derived from the
project phase's funding; for *overhead* there was no known source.

**LDPR formula** (confirmed in `routes/hub.py:_ldpr_profile`):
```
LDPR = last 2 digits of the State Fund + first 3 digits of the Appropriation
e.g. fund 9017 + appropriation 27900 -> "17279"
```
Overhead is all **fund 9017 ("DOH State Road Fund")**, so every overhead LDPR
is `17` + the appropriation's first 3 digits.

## 2. Where the funding is — and isn't

| Source | Has fund/appropriation? | Covers overhead programs? |
|---|---|---|
| **Deighton OData** (`/AccountCode`, dims D1–D5) | **No** — dims are MajorProgram / Program / Phase / **FiscalYear** / **Organization**; `Budget` resolves to "Budget Structure 95" which has the same 5 dims, no fund/appr | n/a |
| OData `Task.FundingSourceType` | a *category* (WVDOH / FEMA / Third-Party…), not fund/appr | maps to **P/N**, not LDPR |
| **TheHub** `PhaseFunding` + `StateFund`/`StateAppropriation` + `[external].BUD_STRU_PHASE_PROG2` | **Yes** | **Projects only** — keyed by project number; overhead programs are absent |
| **BS95 Crosswalk workbook** (`BS95 Crosswalk - Updated.xlsx`) | **Yes** (Appropriation per program×unit) | **Yes — this is the source** |

So neither OData nor TheHub carries overhead funding. The **BS95 Crosswalk**
spreadsheet does.

## 3. What TheHub *did* give us (the validated universe)

From TheHub's OASIS budget mirror (`[external].BUD_STRU_PHASE_PROG2`, `ACT_FL=1`)
the complete validated funding universe is small:

- **Fund 9017 "DOH State Road Fund"**, 6 appropriations →
  `17099` Unclassified · `17237` Maintenance/Non-Federal · `17277` General
  Operations · `17278` Interstate Construction · `17279` Other Federal Aid ·
  `17280` Appalachian.
- Bond/special funds (8330 Coal, 9031/9033 GARVEE, 9032/9035/9036 Roads to
  Prosperity, 9034/9037 State Road Construction, 9040 Industrial Access, 8812)
  → always Unclassified → `x099` LDPRs.

(See `validated_combinations.csv` / `validated_program_phase_funding.csv` at
repo root — the 154 validated `MajorProgram × Phase × Fund × Appropriation`
combos and the 6,902 per-project rows.)

## 4. The BS95 Crosswalk — the missing link

`BS95 Crosswalk - Updated.xlsx` (Change Log + a sheet per District + Divisions)
maps **`REMIS Org · Major Program · Program · Unit · Appropriation`**. Parsing
it (system `python3` + `openpyxl`) yielded:

- **155 distinct overhead/operating programs**, each → **exactly one
  appropriation** (0 programs have more than one → Program→LDPR is a clean 1:1
  function).
- **6 appropriations → 6 LDPRs:**

| LDPR | Appr | Meaning | Program families |
|---|---|---|---|
| `17276` | 27600 | Equipment Expense | `EQP*`, `EEX*`, BGEQP (most-used) |
| `17237` | 23700 | Maintenance / Non-Federal | `MEX*`, annual plans `D01AP`–`D10AP`, MEXBRIM, BGDTRD |
| `17277` | 27700 | General / Admin | `AEX*`, `ERP*`, `BGD01`–`BGD10`, BGSP |
| `17282` | 28200 | Litter Control | LITTER |
| `17319` | 31900 | Payment of Claims | CLAIMS |
| `17275` | 27500 | (only a `n/a`/"ALL" placeholder row) | — |

### Correction to an earlier conclusion
An earlier pass (using only TheHub's *project* appropriation table) wrongly
flagged `17275 / 17276 / 17282` as "phantom" LDPRs. **They are real** — they're
*operating/overhead* appropriations (`27600` Equipment, `28200` Litter, etc.)
that TheHub's project-only table doesn't contain. `17276` is in fact the
single most-used overhead LDPR. The BS95 crosswalk is the authoritative source.

### Reconciling the DOT-12 `ldpr-profiles.ts` dropdown
The app's 8 codes were `17237, 17275, 17276, 17277, 17278, 17279, 17280, 17282`:
- ✅ Real overhead: `17237, 17276, 17277, 17282`.
- ❓ `17275`: backed only by a placeholder row.
- 🏗️ `17278, 17279, 17280`: **project/construction** appropriations (Interstate /
  Federal-Aid / Appalachian), not overhead.
- ➕ Missing: `17319` (Claims) is a real overhead LDPR absent from the dropdown.

## 5. What was built

### 5.1 `bs95_crosswalk` table (both DBs)
Loaded into **both** `dot12` and `dot12_test` Postgres DBs (804 rows, 155
programs, 200 units). **`unit` is TEXT** to preserve leading zeros (`'0711'`).

- Model: `flask_models.py` → `BS95Crosswalk` (`bs95_crosswalk`), columns
  `major_program, program, program_name, unit (TEXT), appropriation, ldpr,
  fund ('9017'), remis_auth`, indexed on `program` and `(program, unit)`.
- Data: parsed from the `BS95 Crosswalk - Updated.xlsx` workbook and loaded
  directly into both DBs (the CSV is not kept in the repo).
- `db.create_all()` creates the table on fresh DBs; **data is loaded directly,
  there is no auto-seed at startup** (by request).

### 5.2 Hub program API — BS95 short-circuit
`routes/hub.py` `GET /dot12/api/hub/projects/<program_number>`:
- New optional query param **`home_unit`**.
- `_bs95_project_response(program, home_unit)` checks `bs95_crosswalk`
  (unit-specific row first, else any row — the mapping is unit-independent).
  If the program is a BS95 overhead code it returns a response in the **exact
  same `HubProjectDetail` schema** as a real TheHub project, but synthesized to
  carry **only the LDPR**: one phase with `ldpr_profiles: ["<ldpr>"]` (and a
  matching `funding_lines` entry with `state_fund 9017` + the appropriation),
  no routes, `status: "BS95 Overhead Program"`.
- If it's *not* a BS95 program, returns `None` and the endpoint falls through
  to the live TheHub project lookup unchanged.

> Schema parity is deliberate: the form's `enrichColumnFromHub` (and the
> `HubProjectDetail` type) consume `phases[0].ldpr_profiles` identically whether
> the data came from a real project or the BS95 crosswalk.

### 5.3 Frontend wiring
- `api/hub-client.ts` `getProject(projectNumber, homeUnit?)` — appends
  `?home_unit=…`.
- `pages/DOT12Detail.tsx`:
  - `enrichColumnFromHub` passes the form `home_unit` to `getProject`.
  - New `enrichBs95Ldpr(col, program, homeUnit)`: on an **overhead** account-
    code pick, fetches the BS95 LDPR via the hub API and **auto-fills the LDPR
    cell** (still editable; the column stays BS95 — no `hub_project_number` set).

## 6. How to use / verify

```bash
# BS95 overhead program -> same schema, just the LDPR
curl 'http://localhost:5000/dot12/api/hub/projects/EQPWO?home_unit=0103'
#   phases[0].ldpr_profiles == ["17276"], state_appropriation "27600"

curl 'http://localhost:5000/dot12/api/hub/projects/MEXPR'   # -> ["17237"]

# Non-BS95 (real project number) falls through to TheHub
curl 'http://localhost:5000/dot12/api/hub/projects/2021000890?home_unit=0711'
```

In the app: pick an overhead program in a column's Program cell → the LDPR cell
auto-fills from the BS95 crosswalk (editable), receiving unit = the home unit,
N/P = Non-participating, BS95 chip shown.

## 7. Artifacts (repo root)
- `bs95_program_ldpr.csv` — clean 155-program → appropriation → LDPR map (1:1).
- `bs95_full_detail.csv` — all 804 program×unit rows (= the seed).
- `validated_combinations.csv`, `validated_program_phase_funding.csv` — TheHub
  validated project funding (154 combos / 6,902 rows).
