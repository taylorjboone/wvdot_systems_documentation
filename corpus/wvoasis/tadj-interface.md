# TADJ or TIMEI Export — Proposed Interface Design (Condensed)

**Status:** **PROPOSED** — not yet confirmed with the State / wvOASIS. The
schemas and delete-and-replace behavior below are a proposal pending validation
against CGI's intake spec (§8).
**System:** CGI Advantage HRM · **Target:** **TIMEI** (timesheet) for labor — or
a custom TADJ intake, to be confirmed (§8)
**Strategy:** nightly full pay-period **Delete-and-Replace**, unified LDPR +
cost-accounting, with **labor and equipment as two separate feeds**, each
produced in **two formats** (CSV + XML).

> **Example files.** A real generated export for unit **0711**, pay period
> **2026-05-30 → 2026-06-12**, is linked as a working reference:
> labor [`HRM_TADJ_REFRESH_0711.csv`](/dot12/sample-data/HRM_TADJ_REFRESH_0711_20260612.csv)
> · [`HRM_TIMEI_0711.xml`](/dot12/sample-data/HRM_TIMEI_0711_20260612.xml) ;
> equipment [`HRM_EQUIP_0711.csv`](/dot12/sample-data/HRM_EQUIP_0711_20260612.csv)
> · [`HRM_EQUIP_0711.xml`](/dot12/sample-data/HRM_EQUIP_0711_20260612.xml).
> One full pay period of real field data, it exercises nearly every rule here at
> once — leave rows, temporary-upgrade events (`T495E`), mid-day task splitting,
> and equipment matched to its operator.
>
> This is some of the cleanest, highest-complexity time-entry data we know of —
> captured at the source and carried end-to-end through **entry → validate/save →
> nightly cycle → payroll**. Observing that full loop over a few pay periods,
> state-wide, is what turns confidence in these validations into a solid,
> empirical handle on the data.

## 1. Summary

A nightly job queries the active pay period for targeted units and produces, per
unit, **two feeds** — **labor** (employee time) and **equipment** (machine
usage) — each as a flat **CSV** (Delete **D** then Insert **I** rows) and a CGI
**document-import XML** (labor = **TIMEI** documents). Both formats are shipped
so the State can register whichever its intake prefers. The **Unified Model**
passes both the LDPR profile and explicit cost-accounting strings, mirroring
CGI's "Use LDPR with Entered Account" so a unit's labor distribution can be
overridden without touching the wider ledger.

**Equipment is its own feed, not merged onto the labor row.** CGI derives
equipment cost via its costing chain rather than carrying equipment on a labor
time line, and merging it onto labor is what errored in OASIS in 2024 (the
R/E-suffix rejections). Each equipment line instead carries its **operator** —
the employee who justified the machine that day — for reference (§4b).

> **Scope — who owns what.** This project controls the nightly query, file
> generation, and delivery to the landing zone. Everything past it — when CGI
> picks up, validates, and posts — runs on the **State-owned wvOASIS
> batch/payroll schedule**, which we do not control or precisely know. All
> downstream-timing statements below are assumptions to confirm with wvOASIS (§8).

## 2. Pipeline Flow

Generation/delivery runs nightly in a low-utilization window (~10 PM–2 AM ET) to
stage the files ahead of the State's overnight batch. Pickup, validation, and
posting after delivery are on the State's clock; until then the rows stay
staged/unposted.

```
[DOT-12 source]
   ▼ 1. Nightly query: active pay period, targeted units
[File-Generation Engine]   labor + equipment, each CSV + XML
   ▼ 2. Write atomically to the delivery directory
[Landing zone]                   ◄── boundary of what we control
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   ▼ 3. Batch pickup — State's schedule (timing uncertain)
[CGI Inbound Import]  ▼ 4. CSV: D purges first, then I loads
[CGI Staging / WIP] ──5. validate──► [Posted HRM Ledger]  (State schedule)
```

## 3. Delete-and-Replace (CSV) · current-state (XML)

Instead of daily diffs (which drift), each feed purges and re-writes the active
period's **unposted** rows each night:

* **CSV:** a **D** block removes what last night sent (matched on the natural
  key), then an **I** block writes the current authoritative state. D applies
  before I; a line dropped since last night gets a D and no I (drift
  self-corrects). **Only unposted rows are reachable** — once the State posts a
  document it is locked, and because posting timing is the State's, a later D is
  only authoritative over what is still unposted when the State processes our
  file (§8).
* **XML:** carries the **current state only** (`DOC_ACTION="New"`). The
  document-version correction model (Modification/Cancellation) is an open item
  with wvOASIS (§8), so the D/I delete-replace lives on the CSV side.

## 4. Labor feed

**CSV — 13 columns:**

| # | Field | Format | Rule |
|---|---|---|---|
| 1 | ActionCode | `D` or `I` | D = Delete, I = Insert. |
| 2 | EmployeeID | Alphanumeric | Native CGI employee id (leading zeros kept). |
| 3 | WorkDate | YYYY-MM-DD | Calendar day worked. |
| 4 | LineEvent | e.g. `REG`, `T495E` | Earning code / time type. |
| 5 | Hours | `0.00` | Labor hours (not HH:MM). |
| 6 | LDPRProfile | e.g. `17237` | Baseline Labor Distribution Profile id. |
| 7 | AcctMethod | `OVERRIDE` / `DEFAULT` | Worked = `OVERRIDE` ("Use LDPR with Entered Account"); leave = `DEFAULT`. |
| 8 | Unit | e.g. `0711` | Preserve leading zeros; org-unit boundary. |
| 9 | Activity | e.g. `303N` | COA activity with the OASIS **P/N suffix**. |
| 10 | SubActivity | e.g. `30ZZ` | Optional crosswalk modifier. |
| 11 | Program | e.g. `D07AP` | Funding program code. |
| 12 | Phase | Alphanumeric | Project/grant phase; empty if unassigned. |
| 13 | TaskOrder | e.g. `260711303175` | Task order for the work line. |

**XML (TIMEI):** one `AMS_DOCUMENT DOC_TYP="TIMEI"` per employee; a
`TIMEI_DOC_HDR` (employee + pay-period end) and one `TIMEI_DOC_LINE` per (day,
event) with hours + the account. `DOC_ID` blank (auto-number); `AMS_DOC_PHASE_CD=2`
(submit to Pending). *Element names are representative pending WV's XSD (§8).*

## 4b. Equipment feed

Equipment usage is charged against the **same accounting string** as labor, but
it ships as its **own** feed (CSV + XML), one row per machine per (day, account):

**CSV — 13 columns:**
`ActionCode, EquipmentID, WorkDate, Units, OperatorEmployeeID, LDPRProfile, AcctMethod, Unit, Activity, SubActivity, Program, Phase, TaskOrder`

* **OperatorEmployeeID** — the employee who charged that exact account the most
  that day (the justification). When no labor matched that account that day the
  machine is **unmatched**: it is still emitted, with a **blank** operator, and
  counted/flagged (it shows as a red cell in the Timesheet-Accounting *Equipment*
  view). Nothing is silently dropped.
* **XML** — a provisional `AMS_DOCUMENT DOC_TYP="EQUIP"` per machine; structure
  is a placeholder pending the State's equipment-intake format (§8).

## 5. Mid-day task splitting

One labor row per distinct accounting combo an employee charges that day
(same-combo charges are summed first). E.g. 3.00 h on `260711303175`/`303N` and
5.00 h on `260711287012`/`287N` → two rows reconciling to an 8-hour day:

```
I,0000012232,2026-06-05,REG,3.00,17237,OVERRIDE,0711,303N,,D07AP,,260711303179
I,0000012232,2026-06-12,REG,5.50,17237,OVERRIDE,0711,816N,,D07AP,,260711816000
```

## 5b. Leave rows ("Use Default Accounting")

When the LDPR is a leave code (ANNLV/SCKLV/FMSUS/HOLLD/BRVUS), the leave
classification drives posting: emit the code in **LineEvent only**, set
**AcctMethod = DEFAULT**, and leave **LDPRProfile, Unit, and Activity blank** (CGI
derives leave accounting from the event).

```
I,0000012232,2026-06-10,ANNLV,8.00,,DEFAULT,,,,,,
```

## 6. Example rows

**Labor** (`HRM_TADJ_REFRESH_0711_<date>.csv`):
```
ActionCode,EmployeeID,WorkDate,LineEvent,Hours,LDPRProfile,AcctMethod,Unit,Activity,SubActivity,Program,Phase,TaskOrder
I,0000012232,2026-06-01,REG,8.00,17237,OVERRIDE,0711,816N,,D07AP,,260711816000
I,0000012232,2026-06-10,ANNLV,8.00,,DEFAULT,,,,,,
```

**Equipment** (`HRM_EQUIP_0711_<date>.csv`) — machine `1310333` matched to its
operator each day:
```
ActionCode,EquipmentID,WorkDate,Units,OperatorEmployeeID,LDPRProfile,AcctMethod,Unit,Activity,SubActivity,Program,Phase,TaskOrder
I,1310333,2026-06-05,8.00,0000012232,17237,OVERRIDE,0711,303N,,D07AP,,260711303179
```

## 7. Delivery

Files are written to the delivery directory and handed to a **pluggable**
transport: **disk** (default) today, **SFTP** to a wvOASIS landing zone once the
State provisions the host + service account (built and config-ready, currently
deferred).

## 8. Validation & open items (State-owned downstream)

**Validation:**
* **Overwrite flag** — worked rows need `AcctMethod = OVERRIDE`; if blank, CGI
  reverts to profile defaults and ignores Activity/TaskOrder. Leave rows are the
  exception (`DEFAULT`, no entered account).
* **Profile cross-validation** — `Unit` must be authorized to run the
  `LDPRProfile`; mismatches drop to the exception ledger.
* **Empty fields** — bare commas only; `NULL`/`NONE`/`N/A` are read as codes.
* **Post valid, hold errors** — valid lines post; bad lines route to a WIP deck
  for manual fix without halting the batch. *When* that happens is the State's
  schedule.

**Open items — confirm with wvOASIS before go-live:**
* **Target & format** — CGI's documented HRM inbound is **TIMEI/XML**, and the
  TIMEI interface does **not** handle TADJ. Confirm whether we feed TIMEI
  (recommended) or a custom TADJ intake, and which format to register.
* **XSD / equipment intake** — provide the TIMEI XSD (and the equipment-intake
  format, if any) so we bind exact element names; ours are representative.
* **Correction model** — on the XML path, do you want Modification/Cancellation
  versions, or is nightly New + delete-replace of unposted documents acceptable?
* **Pickup / posting cadence** — the State's batch + payroll calendar; not
  guaranteed same-night.
* **Landing zone & numbering** — host, path, service account (to enable SFTP);
  and confirm auto-numbering (we leave `DOC_ID` blank).
