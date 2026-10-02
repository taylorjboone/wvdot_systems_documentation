# WVDOT InspectTech — Analysis Notes

## Scope rule: WVDOT-owned bridges only

Every bridge analysis in this directory (deterioration, district / family breakdowns, inspector behavior, ratings, condition, cohorts, dashboards, exports) **must be filtered to bridges WVDOT owns** unless the user explicitly asks for a wider scope.

Ownership lives in the **B.CL.01: Owner** field — `asset_value.field_id = 2300201`.

Filter:

```sql
JOIN asset_value av_own
  ON av_own.as_id = a.as_id
 AND av_own.field_id = 2300201
WHERE av_own.value = 'S01'   -- State Highway Agency = WVDOT
```

Observed distribution in `bridges_all.duckdb`:

| value | count | meaning                              | in scope? |
|-------|-------|--------------------------------------|-----------|
| S01   | 7238  | State Highway Agency (WVDOT)         | **yes**   |
| R     | 176   | Railroad                             | no        |
| L03   | 124   | County / local                       | no        |
| S03   | 101   | Other State Agency                   | no        |
| P     | 47    | Private                              | no        |
| S02   | 21    | Other State (Turnpike etc.)          | no        |
| SX, LX, X, L01, L02, U | <15 each | misc / unknown          | no        |

**Why:** WVDOT can only act on bridges it owns. Mixing in railroad, private, or county-owned structures contaminates any "WVDOT performance" story — e.g. a third-party-rated railroad bridge is not a WVDOT inspector calibration signal.

**Don't confuse with B.CL.02 Maintenance Responsibility (field 2300202).** WVDOT sometimes maintains bridges it doesn't own and vice versa. Ownership is the default in-scope filter; maintenance responsibility is a separate analytic dimension.

If a report intentionally includes non-WVDOT bridges (inventory comparison, statewide totals), call it out at the top with a "scope: all owners" note.

## Other standing rules

- **DuckDB schema-first:** run `DESCRIBE <table>` before joining or casting. Views often expose BLOB-typed columns that need explicit casts; date math differs from SQLite.
- **District vs CO attribution:** if a per-district anomaly involves Central Office or CO-contracted inspectors (GAI, Baker, HDR, etc.), it's a CO / contractor calibration issue, not district culture. Check the inspector roster before naming a district.
