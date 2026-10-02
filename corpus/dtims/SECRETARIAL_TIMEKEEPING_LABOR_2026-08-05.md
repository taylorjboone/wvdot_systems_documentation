# Secretarial / Timekeeping-Duty Labor — WVDOT Active Inventory

**Source:** dTIMS prod `OM_WVDOT.operations.LaborInventory` via
`OPENQUERY([TAMSDW])` (Data-Warehouse tunnel), queried 2026-08-05.
Active = current row version (`ValidTo IS NULL`); 5,295 active employees
statewide, one row per person (no duplicates in the selected set).

## Headline

| | |
|---|---|
| **Employees in secretarial / timekeeping-like titles** | **173** |
| **Total yearly salary (hourly rate × 2,080 hrs)** | **$7,715,593** |

## By title

| Title | Employees | Avg rate | Rate range | Yearly total |
|---|---:|---:|---|---:|
| Transportation Administrative Assistant | 90 | $18.46/hr | $16.39 – $24.16 | $3,455,587 |
| Transportation County Office Manager | 55 | $24.98/hr | $22.26 – $31.85 | $2,857,504 |
| Transportation Office Assistant Coordinator | 13 | $21.14/hr | $18.51 – $24.56 | $571,750 |
| Transportation Administrative Coordinator | 12 | $27.41/hr | $21.32 – $30.41 | $684,133 |
| Transportation Administrative Secretary | 3 | $23.50/hr | $21.47 – $25.32 | $146,619 |
| **Total** | **173** | | | **$7,715,593** |

## Scope — who counts as "secretary with timekeeping-like duties"

Included: the county/district office clerical family that in practice keys
DOT-12s and payroll — Administrative Assistants/Secretaries/Coordinators,
Office Assistant Coordinators, and County Office Managers (who run the
county office including timekeeping).

Deliberately **excluded**, with active headcounts, in case you want them in:

| Adjacent title (excluded) | Employees | Why excluded |
|---|---:|---|
| Transportation County Administrator | 57 | management, not clerical |
| Transportation Assistant County Administrator | 56 | management |
| Transportation District Administrator 1/2/3 | 43 | district management |
| Transportation Division Office Manager | 9 | central-office divisions, not county timekeeping |
| Department of Transportation Secretary / Deputy Secretary | 2 | the cabinet secretary — a `%SECRETARY%` match trap |

Notably, the classification table defines `TRANSPORTATION SECRETARY` and
`OFFICE ASSISTANT 1/2/3` titles, but **zero active employees** currently
carry them — the Administrative Assistant title has absorbed that role.

## Caveats

- `LaborCost` is the dTIMS hourly labor rate; yearly = rate × 2,080 hrs
  (a standard full-time year). It may differ from OASIS base payroll
  (no benefits/loading assumptions verified).
- Titles come from `LaborInventory.Description`; duty inference is by
  title only — actual timekeeping assignments aren't recorded in dTIMS.
- Inventory refreshes daily (last superseded versions stamped 2026-08-04).
