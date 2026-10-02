# Why the DOT-12 Interface Might Be the Most Important Interface for the West Virginia DOT

*West Virginia Department of Transportation · August 2026*

## The thesis

Every day, everything the DOH actually *does* — every crew, every operator-hour,
every ton of stone and foot of pipe — is recorded exactly once, at the source, on
a DOT-12. Then the state pays a second workforce to type it all again into OASIS.
The electronic DOT-12 interface ends that: capture the work once, at the crew
level, and let payroll, equipment charges, and material accounting flow
**upstream into OASIS** as machine-generated transactions. The interface isn't a
form-filler; it is the single funnel through which the entire operational side of
the DOT's finances passes.

## What the second workforce costs today

Active WVDOT labor inventory (dTIMS, queried 2026-08-05) — the secretarial and
county-office titles whose working day is dominated by timekeeping and re-entry:

| Role | Employees | Avg rate | Yearly total |
|---|---:|---:|---:|
| TADAS | 90 | $18.46/hr | $3,455,587 |
| TCOMGR | 55 | $24.98/hr | $2,857,504 |
| TOFASSC | 13 | $21.14/hr | $571,750 |
| TADCO | 12 | $27.41/hr | $684,133 |
| TADSEC | 3 | $23.50/hr | $146,619 |
| **Total** | **173** | | **$7,715,593** |

That is **$7.7M a year of skilled clerical capacity**, much of it spent
transcribing what a foreman already wrote down — for 5,295 field employees whose
time all has to land in OASIS every two weeks, one keystroke at a time.

## What changes when everything funnels through the interface

- **Time entry disappears as a job.** The DOT-12 already carries every
  employee-hour against the correct LDPR, activity, task order, program, and
  phase. The interface's timesheet-accounting engine renders those lines exactly
  as OASIS expects them — the nightly hand-off becomes a review-and-confirm, not
  a day of typing. The same record carries equipment hours and materials, so FIN
  entry rides the same rails.
- **The error surface collapses.** Re-keying is where the damage happens. Our
  July audit of one fragmented integration path found **~$10.9M in wrong
  quantities across ~6,400 transaction lines** — every one an artifact of data
  moving between systems without a single source of truth. When OASIS is fed
  from the DOT-12 record itself, transcription error classes cease to exist.
- **The pilot has already proven it.** Post-pilot surveys show 82% of users
  (40 of 49) now complete their daily DOT-12 in under ten minutes — down from
  10–30+ minutes on paper — and 78% say the system makes their job easier.
  With routes and accounting codes auto-populated from the task number,
  illegible and mis-coded forms have been virtually eliminated at the source.
- **Everything downstream inherits the quality.** Pay, cost accounting, federal
  reporting, dTIMS asset history, equipment utilization — all become views over
  one verified record instead of five partial copies.

## The bottom line

OASIS is the state's book of record, but it is a *destination*. The DOT-12
interface is the **origin** — the one place where the state's largest operational
workforce, its fleet, and its materials meet an accounting structure. Upstream
the entirety of OASIS through it, and the DOH trades a $7.7M shadow workforce of
re-entry for same-day truth: entered once, validated at the source, and trusted
everywhere else.

---
*Employee figures: dTIMS `OM_WVDOT` active labor inventory, 2026-08-05; yearly =
hourly rate × 2,080. Clerical roles won't vanish — they shift from typing time to
verifying it — but the typing does. Quantity-defect figure: July 2026 OC
integration audit.*
