# DOT-12 → wvOASIS Time Interface — Request & Specification

**Status: DRAFT for wvOASIS review.** This is the spec DOT-12 hands the wvOASIS /
CGI team so they can stand up the **intake half** of the interface (landing zone
+ batch job + document mapping). DOT-12 owns the **producer half** (file
generation + delivery); it is built and running to disk today.

Background and the proposal-vs-CGI analysis behind these choices are in
`google_tadj.md` and `oasis_equipment_payroll_mechanics.md` §§14–15.

---

## 1. What DOT-12 produces

Each night (~11 PM ET), for each configured org unit, DOT-12 generates **two
feeds**, each in **two formats**, written atomically to a delivery directory:

| Feed | CSV | XML |
|---|---|---|
| **Labor** (employee time) | `HRM_TADJ_REFRESH_<unit>_<YYYYMMDD>.csv` | `HRM_TIMEI_<unit>_<YYYYMMDD>.xml` |
| **Equipment** (machine usage) | `HRM_EQUIP_<unit>_<YYYYMMDD>.csv` | `HRM_EQUIP_<unit>_<YYYYMMDD>.xml` |

Both formats are produced so wvOASIS can register whichever its intake prefers.
The **XML** mirrors CGI's documented document-import structure (labor = **TIMEI**
documents); the **CSV** is the flat delete-and-replace file.

## 2. Strategy — full delete-and-replace (per feed, per pay period)

Each feed re-sends the active pay period every night: a **D** (delete, value
`0.00`) block that cancels exactly what was sent the prior night, followed by an
**I** (insert) block of the current state. CGI applies **D first, then I**. A
line that disappeared since last night appears only as a `D` (drift
self-corrects). This applies only to **unposted** documents.

The **XML** carries the **current state only** (`DOC_ACTION="New"`); see Open
Question Q3 on the correction model.

## 3. Labor feed

**CSV columns (13):**
`ActionCode, EmployeeID, WorkDate, LineEvent, Hours, LDPRProfile, AcctMethod, Unit, Activity, SubActivity, Program, Phase, TaskOrder`

- `EmployeeID` = OASIS id (string; leading zeros preserved).
- `Activity` carries the OASIS **P/N suffix** (e.g. `261N`).
- `AcctMethod`: worked rows `OVERRIDE` ("Use LDPR with Entered Account"); leave
  rows `DEFAULT` ("Use Default Accounting") with blank LDPR/Unit/Activity.
- Empty = bare empty string (never `NULL`/`NONE`); `Hours` decimal `0.00`.

**XML:** one `AMS_DOCUMENT DOC_TYP="TIMEI"` per employee; `TIMEI_DOC_HDR`
(employee + pay-period end) + one `TIMEI_DOC_LINE` per (day, pay event) with
hours + the labor distribution / account. `DOC_ID` is blank (auto-number);
`AMS_DOC_PHASE_CD=2` (submit to Pending).

## 4. Equipment feed (provisional)

Equipment is its **own** feed — **not** merged onto the labor line. (CGI derives
equipment cost via the costing chain; equipment-on-the-labor-line is what errored
in 2024 — the R/E-suffix rejections.)

**CSV columns (13):**
`ActionCode, EquipmentID, WorkDate, Units, OperatorEmployeeID, LDPRProfile, AcctMethod, Unit, Activity, SubActivity, Program, Phase, TaskOrder`

- One row per machine per (day, account). `OperatorEmployeeID` = the employee who
  justified the machine that day (most hours on the same account); blank when no
  labor matched ("unmatched", still emitted + counted).

**XML:** provisional `AMS_DOCUMENT DOC_TYP="EQUIP"` per machine. Structure is a
placeholder pending the State's equipment-intake format (Q2).

## 5. Delivery

DOT-12 writes the files to disk today. SFTP delivery is **built but deferred** —
ready to switch on once wvOASIS provisions a **landing directory + service
account** (then `TADJ_DELIVERY=sftp` with `TADJ_SFTP_HOST/USER/KEY/REMOTE_DIR`).

---

## 6. Open questions for wvOASIS (please confirm)

1. **Target document & format.** CGI's documented HRM time inbound is **TIMEI**
   in **XML**, and the documentation states the *TIMEI interface does not handle
   TADJ*. Should DOT-12 feed **TIMEI** (recommended) or is there a **custom TADJ**
   inbound? Which **format** (XML vs CSV) should we deliver?
2. **XSD / field names + equipment intake.** Please provide the **TIMEI XSD**
   (and the equipment-time intake format, if any) so we can bind exact element
   names — ours are representative. How should equipment usage be submitted, given
   OASIS normally derives it via the costing chain?
3. **Correction model.** For the nightly refresh on the **XML** path, do you want
   document **Modification/Cancellation versions**, or is a nightly **New** +
   delete-replace of unposted documents acceptable?
4. **Landing zone.** Host, path, service account, key, and the **batch pickup
   schedule** for the inbound interface (so we can enable SFTP and align our
   cutoff to your run).
5. **Numbering.** Confirm **auto-numbering** for these documents (we leave
   `DOC_ID` blank) vs. a supplied/stable Document ID for the nightly overwrite.

---

*Producer status (DOT-12 side): implemented in `dot12-backend/jobs/tadj_export.py`
(+ `serializers.py`, `delivery.py`), ledgers `dot12_tadj_export_runs` /
`_lines` / `dot12_equip_tadj_export_lines`, migration `023_equip_tadj_export.sql`.
Tests in `tests/test_tadj_export.py`. Disk delivery active; SFTP config-ready.*
