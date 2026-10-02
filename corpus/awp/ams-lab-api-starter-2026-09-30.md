# AASHTOWare AMS Lab API — quick starter

> Verified working: 2026-09-30 · Environment: lab (demo data)

## What works

- **Base URL:** `https://api.aashtoware.org/ams-lab`
- **Instance:** `awdemo`
- **Auth:** just your subscription key header — **no Authorization header, no token needed**
- **Data:** demo data (AASHTOWare Project "awdemo" instance, 765 entity sets)

## Minimal request

```bash
curl "https://api.aashtoware.org/ams-lab/awdemo/Contracts?\$top=5" \
  -H "Ocp-Apim-Subscription-Key: $AMS_SUBSCRIPTION_KEY" \
  -H "Accept: application/json"
```

Returns standard OData v4 JSON:

```json
{
  "@odata.context": "https://api.aashtoware.org/ams-lab/awdemo/$metadata#Contracts",
  "value": [
    {"Id": 3, "Name": "TEST Contract", "Description": "Hot mix asphalt base crushing, shaping and resurfacing,", ...}
  ]
}
```

## Discover entities

```bash
# Full model (1.3 MB XML, 765 entity sets) — already saved locally:
curl "https://api.aashtoware.org/ams-lab/awdemo/\$metadata" \
  -H "Ocp-Apim-Subscription-Key: $AMS_SUBSCRIPTION_KEY" -o awdemo_metadata.xml
```

Local copies in this folder: `awdemo_metadata.xml` (full model), `entity_sets.txt` (just the 765 entity set names).

Useful entity sets seen so far: `Contracts` (147), `Proposals` (10,915), `DailyWorkReports` (312), `Materials` (83), `ContractItems`, `Vendors`-style sets under `Contract*`, plus DWR children (`DwrWorkItems`, `DWRContractors`, `DwrNotes`, `DWRStaffRecords`, ...).

## OData query options (all verified working)

```
GET /ams-lab/awdemo/Contracts?$top=20&$skip=40        # paging
GET /ams-lab/awdemo/Contracts?$top=0&$count=true      # total count (147)
GET /ams-lab/awdemo/Contracts?$select=Id,Name,Description
GET /ams-lab/awdemo/Contracts?$filter=contains(Name,'Contract')&$orderby=Id desc
GET /ams-lab/awdemo/DailyWorkReports(2)?$expand=DWRContractors,DwrWorkItems,Contract
```

## Tiny Python example

```python
import os, requests

LAB = "https://api.aashtoware.org/ams-lab"
INSTANCE = "awdemo"
session = requests.Session()
session.headers.update({
    "Ocp-Apim-Subscription-Key": os.environ["AMS_SUBSCRIPTION_KEY"],
    "Accept": "application/json",
})

r = session.get(f"{LAB}/{INSTANCE}/Contracts", params={"$top": 5, "$count": "true"})
print(r.json()["value"], r.json()["@odata.count"])
```

## Gotchas

- `$` in query params gets percent-encoded to `%24` by HTTP clients — the server accepts both.
- The service root (`/awdemo/`) returns 500 — query entity sets directly instead.
- Every record carries audit fields (`CreatedDate/By`, `LastUpdatedDate/By`); AMS usernames appear as `CorporateDomain\user`, not emails.
- This is the **lab** gateway. The production gateway (`/ams/wvdot/...`) requires an additional Authorization step that is still unresolved (401) — see `ams-wvdot-contracts-401-support-ticket-2026-09-30.md`.
