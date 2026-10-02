# AssetWise reverse-engineering references

Saved responses and files from the 2026-05 reverse-engineering of WVDOT's
**Bentley AssetWise Inspections** (InspectTech) tenant — the web app at
`wvdot-it.bentley.com` and its OData / REST API at `wvdot-it-api.bentley.com`.
They are what the bridge pipeline (`pipeline/bridges/`, `python -m pipeline
bridges …`) and the inventory DuckDB (`INSPECT_DB`) were built from. Copied
from inspect_tech `analysis/` on 2026-09-25.

Nothing in the app reads these files at runtime. They are reference material
for anyone changing the dumper (`pipeline/bridges/dump_bridge.py`), the raw
OData dumper (`pipeline/bridges/godump/`) or the queries over the DuckDB. The
narrative write-ups that go with them are in the app under **Documents →
Bridges**: `/docs/Bridges_AssetWise_Reference` (the API, the dumper, the
schema) and `/docs/Bridges_Asset_Model` (the Asset object in depth).

## What's here

| Path | What it is |
|---|---|
| `ANALYSIS_RULES.md` | Standing rules for bridge analysis: WVDOT-owned scope (B.CL.01 field 2300201 = `S01`), district vs Central Office attribution, DuckDB schema-first (inspect_tech `analysis/CLAUDE.md`) |
| `endpoints.txt` | Every route the API advertises, one `VERB path` line plus its summary — the input of `extract-reads` |
| `swagger_v1.json`, `swagger_index.html` | The API's Swagger document and its index page |
| `odata_metadata.xml` | The OData `$metadata` EDMX: entity types, keys, properties |
| `reads.json`, `reads.csv`, `reads.md` | The 494 GET endpoints, grouped by surface and controller, enriched from Swagger and the EDMX. Rebuild with `python -m pipeline bridges extract-reads` |
| `odata_samples/` | `$top=3` from each OData entity set (Assets, AssetTasks, AssetValues, AssetElements, Fields, ReportValues, …) |
| `asset_probes/` | One bridge (02A021) through every asset endpoint: full record, GUID lookup, coordinates, sub-assets, elements, segments, asset tree, schedules, tasks, files, counts, type. Empty files are probes that returned nothing |
| `template_probes/` | Report-type → template maps, report sections, repeating field groups, data types and form layouts behind the inspection report |
| `inspection_272398/` | One complete inspection (ast_id 272398, bridge 01A001) pulled endpoint by endpoint: core record, bridge, inspectors, types, workflow, report values, form layouts, and `20_form_layout_with_values.md`, the captured values laid out form by form. `forms/` has each mobile form's elements |
| `report_summary_view.html` | The AssetWise report summary page as the browser receives it; it is where the bearer token (`window.AwiPageOptions.accessToken`) was found |
| `bundle_*.js` | The page's webpack bundles (commons, vendors, report grid, top navigation, token refresh), read to find the API calls and the token-refresh flow |
| `district_family_breakdown.csv` | Per district × bridge family: counts, age, current deck / super / sub ratings, ADT and the fitted deck-deterioration slope — the table behind `/docs/Bridges_Family_District_Deterioration` |

## What was left out or redacted

- `inspection_272398/272398_report.pdf` (22 MB rendered PDF): over the 10 MB
  limit for this folder. Inspection PDFs are fetched on demand by the app.
- The SQLite / DuckDB dumps from the same work (`01A001.db`, `all_sample.db`,
  `bridges100.db`, `bridges_new.db`, `odata_raw.db`, `output.db`,
  `bridges_all.db`, `bridges_all*.duckdb` and their `-wal`/`-shm` files): data,
  not references; the live inventory is `INSPECT_DB`.
- Credentials: no cookie, token or password files were copied. In
  `report_summary_view.html` the two embedded bearer tokens, the ASP.NET
  `__VIEWSTATE` / `__EVENTVALIDATION` values and the signed-in user's name are
  replaced with `REDACTED…`.

Inspection records (`inspection_272398/03_inspectors.json`, the form layouts)
name the WVDOT inspectors who worked on that inspection, with their wv.gov
e-mail addresses, as AssetWise stores them.
