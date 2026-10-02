# DOT-12 Flask API Documentation

A RESTful API for managing DOT-12 Daily Labor Reports with full support for deep nested create/update/delete operations.

## Base URL

```
http://localhost:5000
```

## Features

- ✅ **Full CRUD Operations** - Create, Read, Update, Delete forms
- ✅ **Deep Nested Updates** - Update entire form hierarchy in single request
- ✅ **Automatic Cascade Deletes** - Removing objects automatically cleans up related data
- ✅ **Pagination Support** - Efficient handling of large datasets
- ✅ **CORS Enabled** - Ready for frontend integration
- ✅ **Type Safe** - Proper handling of dates, decimals, and numeric types

## API Endpoints

### Health Check

#### `GET /health`

Check API and database connectivity.

**Response**:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-03-15T10:30:00"
}
```

---

### Forms

#### `GET /api/forms`

Get all DOT-12 forms with optional filtering and pagination.

**Query Parameters**:
- `start_date` (optional): Filter forms from this date (YYYY-MM-DD)
- `end_date` (optional): Filter forms to this date (YYYY-MM-DD)
- `home_unit` (optional): Filter by home unit
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 20, max: 100)

**Smart-search facet parameters** (values within one param OR together;
different params AND; all flow identically to `/api/forms/ids`,
`/api/forms/{id}/neighbors`, and `/api/forms/count`):
- `programs` (optional): Comma list of OASIS D2 program codes (case-insensitive), e.g. `D04AP,D02AP`
- `task_orders` (optional): Comma list of task order numbers
- `routes` (optional): **Pipe**-joined raw route queries, re-parsed with the
  route grammar (`CR 9`, `county route 21`, `I-77`, a county name, a BARS
  bridge number like `43A115`; components AND within one chip)
- `employees` (optional): Comma list of OASIS payroll ids — matches only
  forms where the person charged **hours > 0**
- `equipment` (optional): Comma list of ED numbers — hours > 0 required
- `materials` (optional): Comma list of `stock~suffix` tokens (empty suffix
  side = blank suffix) — quantity charged > 0 required

**Example Request**:
```bash
curl "http://localhost:5000/api/forms?start_date=2025-03-01&end_date=2025-03-31&home_unit=1055&page=1&per_page=20"
```

**Response**:
```json
{
  "forms": [
    {
      "id": 1,
      "form_date": "2025-03-15",
      "home_unit": "1055",
      "prepared_by": "John Doe",
      "...": "..."
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 45,
    "pages": 3,
    "has_next": true,
    "has_prev": false
  }
}
```

---

#### `GET|POST /api/forms/count`

Count of forms matching the current filters — the Smart Search modal's live
"N forms match" readout. Accepts the exact same filter params as
`GET /api/forms` (same `_apply_form_filters`); POST takes them as a JSON
body when the query string would exceed the request-line limit.

**Response**: `{ "count": 42 }`

---

#### `GET /api/forms/suggest`

Typeahead values for the smart-search facets (omni-search dropdown sections
+ Smart Search modal fields). Org-ACL-scoped: every section joins
`dot12_forms` and only offers values from non-archived forms the caller can
view. Sections rank by distinct-form count.

**Query Parameters**:
- `q` (required): The text being typed (blank → all sections empty)
- `fields` (optional): Comma subset of
  `programs,task_orders,routes,employees,equipment,materials` (default all)
- `limit` (optional): Per-section cap (default 5, max 10)

Minimum query length: 2 characters for employees / equipment / materials /
task_orders, 1 for programs / routes. People and equipment appear only with
hours charged > 0; materials only with a quantity charged. Route items carry
a canonical re-parseable `query` string plus `kind`
(`route` | `county` | `bridge`).

**Response** (only requested sections):
```json
{
  "programs":   [{ "value": "D04AP", "name": "District 04 Annual Plan", "forms": 12 }],
  "task_orders": [{ "value": "260206201003", "forms": 4, "last": "2026-08-14" }],
  "routes":     [{ "query": "CR 9", "label": "CR 9", "kind": "route", "forms": 7 }],
  "employees":  [{ "oasis_id": "0000000111", "name": "Smith, Jane", "forms": 9 }],
  "equipment":  [{ "ed_number": "1370201", "description": "CREW CAB", "forms": 5 }],
  "materials":  [{ "stock_item_number": "402001", "commodity_suffix": "A", "description": "#57 STONE", "forms": 3 }]
}
```

---

#### `GET /api/forms/{id}`

Get a specific DOT-12 form with all nested details.

**Example Request**:
```bash
curl "http://localhost:5000/api/forms/1"
```

**Response**:
```json
{
  "id": 1,
  "pay_period_start": "2025-03-01",
  "pay_period_end": "2025-03-15",
  "form_date": "2025-03-05",
  "home_unit": "1055",
  "receiving_unit": "1055",
  "ldpr_profile": "17279",
  "prepared_by": "John Doe",
  "approved_by": "Jane Smith",
  "entered_by_hrm": "HR Staff",
  "entered_by_fin": "FIN Staff",
  "form_details": "Additional notes",
  "created_at": "2025-03-05T08:00:00",
  "updated_at": "2025-03-05T08:00:00",
  "employees": [
    {
      "id": 1,
      "oasis_id": "12345",
      "first_name": "John",
      "last_name": "Worker",
      "temporary_upgrade": null,
      "display_order": 1,
      "charges": [
        {
          "id": 1,
          "task_asset_id": 1,
          "hours_charged": 8.0,
          "timei_document_id": "TD12345"
        }
      ]
    }
  ],
  "equipment": [
    {
      "id": 1,
      "ed_number": "401-1672",
      "equipment_description": "Dump Truck",
      "operator_initials": "JW",
      "ending_meter": 123456,
      "status_active": true,
      "display_order": 1,
      "charges": [
        {
          "id": 1,
          "task_asset_id": 1,
          "hours_charged": 8.0,
          "timei_document_id": "TD12346"
        }
      ]
    }
  ],
  "materials": [
    {
      "id": 1,
      "material_description": "Asphalt Mix",
      "org_whse": "HW",
      "stock_item_number": "11111600",
      "commodity_suffix": "064",
      "oc_doc_id": "OC12345",
      "display_order": 1,
      "charges": [
        {
          "id": 1,
          "task_asset_id": 1,
          "quantity_charged": 25.5,
          "oc_doc_id": "OC12345"
        }
      ]
    }
  ],
  "task_assets": [
    {
      "id": 1,
      "column_number": 1,
      "ldpr_profile": null,
      "receiving_unit": "1055",
      "activity": 260,
      "sub_activity": "P",
      "program": "202500206",
      "phase": "CN0001",
      "task_order_number": "260240046",
      "task_id_dtims": null,
      "route_bars": "10/50",
      "asset_id_dtims": null,
      "beg_measure": 0.0,
      "end_measure": 0.5,
      "accomplished": 30.0,
      "unit_of_measure": "TN",
      "weather": "Clear",
      "temperature": 45.0,
      "description": "Roadwork description",
      "traffic_control": true,
      "employee_charges": [
        {
          "id": 1,
          "employee_id": 1,
          "hours_charged": 8.0,
          "timei_document_id": "TD12345"
        }
      ],
      "equipment_charges": [
        {
          "id": 1,
          "equipment_id": 1,
          "hours_charged": 8.0,
          "timei_document_id": "TD12346"
        }
      ],
      "material_charges": [
        {
          "id": 1,
          "material_id": 1,
          "quantity_charged": 25.5,
          "oc_doc_id": "OC12345"
        }
      ]
    }
  ]
}
```

---

#### `POST /api/forms`

Create a new DOT-12 form with all nested objects.

**Request Body**: Complete form JSON with nested employees, equipment, materials, and task assets

**Example Request**:
```bash
curl -X POST http://localhost:5000/api/forms \
  -H "Content-Type: application/json" \
  -d '{
  "form_date": "2025-03-15",
  "pay_period_start": "2025-03-01",
  "pay_period_end": "2025-03-15",
  "home_unit": "1055",
  "receiving_unit": "1055",
  "prepared_by": "John Doe",
  "employees": [
    {
      "oasis_id": "12345",
      "first_name": "John",
      "last_name": "Worker",
      "display_order": 1,
      "temp_id": "emp1"
    }
  ],
  "equipment": [
    {
      "ed_number": "401-1672",
      "equipment_description": "Dump Truck",
      "operator_initials": "JW",
      "ending_meter": 123456,
      "status_active": true,
      "display_order": 1,
      "temp_id": "eq1"
    }
  ],
  "materials": [
    {
      "material_description": "Asphalt Mix",
      "stock_item_number": "11111600",
      "commodity_suffix": "064",
      "display_order": 1,
      "temp_id": "mat1"
    }
  ],
  "task_assets": [
    {
      "column_number": 1,
      "activity": 260,
      "route_bars": "10/50",
      "accomplished": 30.0,
      "unit_of_measure": "TN",
      "employee_charges": [
        {
          "employee_temp_id": "emp1",
          "hours_charged": 8.0
        }
      ],
      "equipment_charges": [
        {
          "equipment_temp_id": "eq1",
          "hours_charged": 8.0
        }
      ],
      "material_charges": [
        {
          "material_temp_id": "mat1",
          "quantity_charged": 25.5
        }
      ]
    }
  ]
}'
```

**Response**:
```json
{
  "message": "Form created successfully",
  "form": {
    "id": 2,
    "...": "... (full form object)"
  }
}
```

**Notes**:
- Use `temp_id` fields on employees, equipment, and materials to reference them in charges before they have database IDs
- All nested objects are created in a single transaction
- If any part fails, the entire operation is rolled back

---

#### `PUT /api/forms/{id}`

Update an existing DOT-12 form with deep nested updates.

Supports:
- Updating form header fields
- Adding new employees, equipment, materials
- Updating existing employees, equipment, materials
- Removing employees, equipment, materials (by omitting their IDs)
- Adding new task assets
- Updating existing task assets
- Removing task assets (by omitting their IDs)
- Adding/updating/removing all types of charges

**Example Request**:
```bash
curl -X PUT http://localhost:5000/api/forms/1 \
  -H "Content-Type: application/json" \
  -d '{
  "approved_by": "Jane Smith",
  "employees": [
    {
      "id": 1,
      "oasis_id": "12345",
      "first_name": "John",
      "last_name": "Worker Updated"
    },
    {
      "oasis_id": "67890",
      "first_name": "New",
      "last_name": "Employee"
    }
  ],
  "task_assets": [
    {
      "id": 1,
      "accomplished": 35.0,
      "employee_charges": [
        {
          "id": 1,
          "hours_charged": 10.0
        }
      ]
    }
  ]
}'
```

**Response**:
```json
{
  "message": "Form updated successfully",
  "form": {
    "id": 1,
    "...": "... (full updated form object)"
  }
}
```

**Update Logic**:
- Objects with IDs are updated
- Objects without IDs are created
- Objects missing from the array are deleted
- Applies recursively to all nested objects

---

#### `DELETE /api/forms/{id}`

Delete a DOT-12 form and all related data (cascading delete).

**Example Request**:
```bash
curl -X DELETE http://localhost:5000/api/forms/1
```

**Response**:
```json
{
  "message": "Form deleted successfully",
  "deleted_form": {
    "id": 1,
    "form_date": "2025-03-15",
    "home_unit": "1055"
  }
}
```

**Note**: This deletes the form and ALL related data:
- All employees and their charges
- All equipment and their charges
- All materials and their charges
- All task assets and their charges

---

### Reports & Summaries

#### `GET /api/forms/{id}/summary`

Get a summary of a form with totals.

**Example Request**:
```bash
curl "http://localhost:5000/api/forms/1/summary"
```

**Response**:
```json
{
  "form_id": 1,
  "form_date": "2025-03-15",
  "home_unit": "1055",
  "employee_count": 5,
  "equipment_count": 3,
  "material_count": 2,
  "task_asset_count": 2,
  "total_employee_hours": 45.0,
  "total_equipment_hours": 30.0
}
```

---

#### `GET /api/reports/daily`

Get daily summary report for all forms on a specific date.

**Query Parameters**:
- `date` (optional): Report date (YYYY-MM-DD, default: today)
- `home_unit` (optional): Filter by home unit

**Example Request**:
```bash
curl "http://localhost:5000/api/reports/daily?date=2025-03-15&home_unit=1055"
```

**Response**:
```json
{
  "date": "2025-03-15",
  "home_unit": "1055",
  "form_count": 3,
  "total_employee_hours": 120.5,
  "total_equipment_hours": 85.0,
  "unique_employees": 12,
  "unique_equipment": 8,
  "forms": [
    {
      "id": 1,
      "form_date": "2025-03-15",
      "home_unit": "1055",
      "...": "..."
    }
  ]
}
```

---

### Leave requests (DOP-L1)

WV Division of Personnel **DOP-L1 "Application for Leave With Pay"** requests,
bridged both ways to DOT-12 forms. Blueprint `routes/leave_requests.py`, URL
prefix **`/dot12/api/leave-requests`** — the `{id}` paths below are relative to
that prefix. Business rules live in `dot12-logic.md` §19.

**Gate (every route).** A blueprint-level `before_request` runs first:
- `401` — no session.
- `404` — the `leave_requests` feature flag (`dot12_feature_flags`, seeded
  **OFF**) is disabled. The feature is invisible while off; `GET /dot12/api/config`
  reports the flag.
- Each handler then re-checks the caller's scope itself (`403`) — this prefix
  is **not** covered by the `/dot12/api/forms/<id>` org-access middleware.
- Unexpected errors → `500 {"error": "<label> failed"}`; the server log carries
  the exception *type* only (never request remarks).

**Status** is derived, never stored: `draft` → `awaiting_signature` →
`submitted` → `approved` | `disapproved`; `withdrawn` is terminal (wins over
everything); `is_archived` is a separate soft-delete flag (an archived request
keeps its derived status).

**Bucket keys** (`bucket`) and the OASIS code each bridges to:

| bucket | DOP-L1 box | `ldpr_code` |
|---|---|---|
| `annual` | Annual | `ANNLV` |
| `annual_exhaustion_sl` | Annual (exhaustion of SL) | `ANNLV` |
| `military` | Military | `MLVPA` (or `MLVPB` when `military_code` = `MLVPB`) |
| `jury` | Witness/Jury Service | `JURYL` |
| `sick` | Sick | `SCKLV` |
| `sick_family` | Sick (Imm. Family) | `SCKLV` |
| `sick_death` | Sick (Death in Imm. Family) | `BRVUS` |
| `grievance` | Grievance Prep/Hearing | *none* — never bridges to a DOT-12 |

**Identity.** `oasis_id` is the OASIS labor code, canonicalized by
`normalize_labor_code` (digits → zero-padded to 10; anything else trimmed and
upper-cased). `employee.user_id` is the app user whose `users.labor_code`
matches (`null` when nobody does).

#### Leave request object

Full shape, returned by `GET /{id}` and every mutating route. List rows carry
only the **lite** subset (marked †).

```jsonc
{
  "id": 12,                                          // †
  "status": "submitted",                             // † derived
  "home_unit": "0260",                               // †
  "employee": {                                      // †
    "oasis_id": "0000161725", "user_id": 41,
    "first_name": "Pat", "last_name": "Doe", "has_account": true
  },
  "filed_by": { "id": 7, "first_name": "…", "last_name": "…", "e_number": "…",
                "user_color": "…", "signature_font": null },      // † user summary
  "filed_on_behalf": false,                          // †
  "period_from": "2026-09-07", "period_to": "2026-09-11",           // †
  "bucket_totals": { "annual": 40, "annual_exhaustion_sl": 0, "military": 0, "jury": 0,
                     "sick": 0, "sick_family": 0, "sick_death": 0, "grievance": 0 },   // †
  "total_hours": 40,                                 // †
  "linked_form_ids": [301, 302],                     // †
  "is_archived": false,                              // †
  "created_at": "…", "updated_at": "…",              // †
  "work_unit": "Bridge crew", "division": "District 2",
  "period_from_time": "07:00", "period_to_time": null,             // "HH:MM" | null
  "days": [
    { "id": 1, "leave_date": "2026-09-07", "bucket": "annual", "ldpr_code": "ANNLV",
      "hours": 8, "linked_form_id": 301 }
  ],
  "military_code": null,                             // "MLVPA" | "MLVPB" | null
  "family_relationship": null,
  "remarks": null,                                   // never in list rows, notifications, events or logs
  "physician_statement_provided": false,
  "supporting_docs_provided": false,
  "source": "manual",                                // "manual" | "dot12"
  "signature_requested_at": null,
  "employee_signed_by": { "…user summary…" }, "employee_signed_at": "…",
  "submitted_by": { "…" }, "submitted_at": "…",
  "decided_by": null, "decided_at": null, "decision": null,        // "approved" | "disapproved"
  "rejection_reason": null,
  "withdrawn_by": null, "withdrawn_at": null,
  "agency_authorized_by": null, "agency_authorized_at": null,      // reserved — always null in v1
  "archived_at": null,
  "linked_forms": [
    { "link_id": 5, "form_id": 301, "leave_date": "2026-09-07", "origin": "leave_to_dot12",
      "task_asset_id": 900, "form_status": "draft", "home_unit": "0260", "integrity": "ok" }
  ],
  "approval": { "scope": "chain", "approvers": [ { "id": 9, "display_name": "…" } ] },
  "policy_warnings": [
    { "code": "dop_l3_required", "severity": "warning", "message": "…",
      "details": { "consecutive_sick_workdays": 4 } }
  ],
  "policy_context": { "family_sick_hours_ytd": 16 },
  "can": { "view": true, "edit": false, "sign": false, "submit": false,
           "approve": true, "disapprove": true, "withdraw": false, "reopen": false,
           "archive": false, "create_dot12s": false, "link": true }
}
```

- `approval.scope` — `chain` (the employee's supervisor chain decides) or
  `org` (fallback: the DOT-12 org approvers of `home_unit`, minus the filer).
- `linked_forms[].origin` — `leave_to_dot12` | `dot12_to_leave` | `manual`.
- `linked_forms[].integrity` — computed at read time, never auto-repaired:
  `ok` | `hours_mismatch` | `code_mismatch` | `form_archived` | `form_rejected`
  | `column_deleted`.
- `policy_warnings[].code` — `dop_l3_required`, `bereavement_over_3_days`,
  `family_sick_over_80h` (severity `warning`); `supporting_docs_required`,
  `annual_retroactive` (severity `info`). Advisory only — nothing blocks.
- `can.*` is computed for the **calling** user.

#### `GET /dot12/api/leave-requests`

List the requests visible to the caller.

**Query Parameters**:
- `scope` (optional, default `mine`):
  - `mine` — I am the employee or the filer
  - `to_sign` — awaiting **my** signature
  - `queue` — submitted and awaiting **my** approval
  - `org` — requests whose `home_unit` is one of my viewable orgs (optionally narrowed with `home_unit`)
  - `all` — every request (admin only; `403` otherwise)
  - anything else → `400`
- `status` / `status[]` (optional): derived-status filter; repeated or comma-separated
- `home_unit`, `oasis_id` (normalized), `start` / `end` (period overlap), `ids` / `ids[]`, `q` (name, labor code, or `#id`)
- `page` (default 1), `per_page` (default 50, max 200)

Non-admins never see archived rows. Sorted by `period_from` desc, `id` desc.

**Response**:
```json
{ "items": [ { "…lite object…": "" } ], "total": 3, "page": 1, "per_page": 50 }
```

---

#### `GET /dot12/api/leave-requests/employee-lookup`

Org roster for the on-behalf picker: the org's daily labor snapshot
(`labor_roster_for_org`) ∪ employees listed on that org's non-archived DOT-12s
in the last 120 days, with `has_account` resolved via `users.labor_code`.

**Query Parameters**: `home_unit` (required → `400`). Caller needs org edit on it
(`can_create_edit_form` + `can_edit`) → `403`.

**Response**:
```json
{ "home_unit": "0260",
  "employees": [ { "oasis_id": "0000161725", "first_name": "Pat", "last_name": "Doe",
                   "user_id": 41, "has_account": true } ] }
```

---

#### `POST /dot12/api/leave-requests`

Create a **draft** request.

**Request Body**:
```jsonc
{
  "oasis_id": "161725",            // omit (or send your own code) for self-service
  "home_unit": "0260",             // required on-behalf; self-service defaults to users.org
  "period_from": "2026-09-07",
  "period_to": "2026-09-11",       // defaults to period_from
  "bucket": "annual",              // default bucket for expanded rows (default "annual")
  "days": [ { "leave_date": "2026-09-09", "bucket": "sick", "hours": 4 } ],   // optional explicit rows
  "military_code": "MLVPA",        // optional, MLVPA | MLVPB
  "work_unit": "…", "division": "…",
  "period_from_time": "07:00", "period_to_time": "15:30",
  "family_relationship": "…", "remarks": "…",
  "source_form_id": 301            // optional: sets source="dot12" only — it does NOT link (use /links)
}
```

**Rules**:
- Self-service requires `users.labor_code` (`400` with the "ask an admin to set
  your Labor Code" message) and a home org.
- On-behalf requires org edit on `home_unit` (`403`) and the employee on that
  org's roster (`403`; admins may bypass the roster check).
- Without `days`: one row per **workday** — Mon–Fri that is not a West
  Virginia state holiday (`wv_holidays.py`; observed dates, e.g. Independence
  Day 2026 → Fri Jul 3) — in the period, 8.00 h each, in `bucket`. With
  `days`: rows are taken as posted (weekends / holidays allowed) and
  validated — date inside the period, known bucket, no duplicate (date, bucket).
- Period ≤ 60 calendar days; hours 0.25–24 in quarter-hour steps.

**Responses**: `201` full object · `400` validation · `403` scope.

---

#### `GET /dot12/api/leave-requests/{id}`

`200` full object · `403` not visible · `404` unknown, or archived and the caller is not an admin.

Visible to: admins · the employee (matched by user id **or** labor code) · the
filer · anyone in the approver scope · anyone whose viewable orgs include the
request's `home_unit`.

---

#### `PATCH|PUT /dot12/api/leave-requests/{id}`

Partial update while the request is `draft` or `awaiting_signature`, by an
admin, the employee, the filer, or an org editor (`403` otherwise).

**Request Body** (any subset): `work_unit`, `division`, `family_relationship`,
`remarks`, `military_code` (re-derives every day's `ldpr_code`),
`physician_statement_provided`, `supporting_docs_provided`, `period_from`,
`period_to`, `period_from_time`, `period_to_time`, `days` (replaces **all**
rows — a day already linked to a DOT-12 must be resent with the same bucket and
hours, else `400`).

- `oasis_id` / `home_unit` are immutable → `400` ("start a new request").
- Editing an `awaiting_signature` request clears `signature_requested_at`, so it
  drops back to `draft` and must be re-sent to the employee.

**Response**: `200` full object.

---

#### `PATCH /dot12/api/leave-requests/{id}/flags`

Set `physician_statement_provided` / `supporting_docs_provided` in **any**
non-archived status. Allowed for a party (employee / filer), an approver, an org
editor, or an admin (`403`). Records an `edit` event naming the flags changed.
Returns the full object.

---

#### `POST /dot12/api/leave-requests/{id}/submit`

Alias: `POST /{id}/request-signature` (same handler). From `draft` only
(`400`; also `400` with no days or a day outside the period). Caller must be
able to edit the request (`403`). What happens depends on who is calling:

| Caller | Result | Notification |
|---|---|---|
| The employee themself | signs + submits → `submitted` | `leave_approval_needed` → approver scope |
| Someone else, employee **has** an account | `signature_requested_at` set → `awaiting_signature` | `leave_signature_needed` → employee |
| Someone else, employee has **no** account | `filed_on_behalf = true`; filer certifies on their behalf → `submitted` | `leave_approval_needed` → approver scope |

**Response**: `200` full object.

---

#### `POST /dot12/api/leave-requests/{id}/sign`

The employee named on the request signs it (`403` for anyone else). From
`draft` or `awaiting_signature` (`400`). Signs + submits → `submitted`; notifies
the approver scope. `200` full object.

---

#### `POST /dot12/api/leave-requests/{id}/approve` · `POST /dot12/api/leave-requests/{id}/disapprove`

From `submitted` only (`400`). Caller must be in the approver scope or an admin
(`403`); the employee can never decide their own request unless they are an
admin (recorded as an extra `approve` event "Self-approved (admin)").

**Request Body** (optional): `{ "rejection_reason": "…", "physician_statement_provided": true }`
— `rejection_reason` is **required** for disapprove (`400`).

Stamps `decided_by/at` + `decision`; notifies the filer and employee
(`leave_approved` / `leave_disapproved`). `200` full object.

---

#### `POST /dot12/api/leave-requests/{id}/withdraw`

From `draft`, `awaiting_signature` or `submitted` (`400`). Employee, filer, or
admin (`403`). Terminal → `withdrawn`. Unless it was still a draft, the other
party and the approvers get `leave_withdrawn`. `200` full object.

---

#### `POST /dot12/api/leave-requests/{id}/reopen`

From `disapproved` or `withdrawn` (`400`) back to `draft`: clears the decision,
submission, employee signature, signature request and withdrawal stamps
(the old reason is kept in the `reopen` event). Allowed for a party or admin; an
approver may reopen a **disapproved** request only (`403`). `409` when any
linked DOT-12 is approved and not archived ("recall it first").

---

#### `DELETE /dot12/api/leave-requests/{id}`

Archive (soft delete). From `draft`, `withdrawn` or `disapproved` (`400` —
"withdraw it instead"). Party, admin, or org editor (`403`).

**Response**: `{ "ok": true, "id": 12 }`. Archived requests are `404` to non-admins.

---

#### `POST /dot12/api/leave-requests/{id}/restore`

Admin only (`403`; `404` unknown id). Clears the archive flag and returns the full object.

---

#### `GET /dot12/api/leave-requests/{id}/events`

History, oldest first.

```json
{ "events": [ { "id": 1, "event_type": "create", "description": null, "occurrence_count": 1,
                "user": { "…user summary…": "" }, "created_at": "…" } ] }
```

`event_type`: `create`, `edit` (consecutive edits by one user coalesce, bumping
`occurrence_count`), `request_signature`, `employee_sign`, `submit`, `approve`,
`disapprove`, `withdraw`, `reopen`, `archive`, `restore`, `link_dot12`,
`unlink_dot12`, `create_dot12s`.

---

#### `GET /dot12/api/leave-requests/coverage`

Which employees on a DOT-12 charged leave hours with / without a covering leave
request — drives the editor's Checks-panel warning and the post-submit checklist.

**Query Parameters**: `form_id` (required → `400`). Needs **view** permission on
the form (`403`); `404` unknown or archived form.

**Rules**:
- A "leave column" is a charge whose `COALESCE(ta.ldpr_profile, form.ldpr_profile)`
  **or** `ta.activity` is one of `ANNLV, SCKLV, BRVUS, JURYL, MLVPA, MLVPB`
  with `hours_charged > 0`. `HOLLD` / `FMSUS` columns are ignored (no DOP-L1 bucket).
- Matching is by code **family** (`ANNLV`→annual, `SCKLV`→sick, `BRVUS`→
  bereavement, `MLVPA|MLVPB`→military, `JURYL`→jury) against **active**
  requests — draft, awaiting signature, submitted or approved; withdrawn,
  disapproved and archived never cover — that have a day row on the form's date
  for that labor code (`home_unit` is not part of the match).
- `uncovered_codes` = families with no request day at all; `short_codes` =
  families where the request hours are less than the DOT-12 hours.

**Response**:
```jsonc
{
  "form_id": 301, "form_date": "2026-09-07", "flag_enabled": true, "uncovered_count": 1,
  "employees": [ {
    "employee_id": 55, "oasis_id": "0000161725", "first_name": "Pat", "last_name": "Doe",
    "user_id": 41, "has_account": true,
    "leave": [ { "ldpr_code": "ANNLV", "hours": 8, "task_asset_id": 900, "column_number": 1 } ],
    "covered_by": [ { "leave_request_id": 12, "status": "approved", "bucket": "annual",
                      "hours": 4, "linked": true } ],
    "uncovered_codes": [],
    "short_codes": ["ANNLV"]
  } ]
}
```

---

#### `POST /dot12/api/leave-requests/from-dot12`

Create **draft** on-behalf requests for a DOT-12's uncovered employees and link them.

**Request Body**: `{ "form_id": 301, "oasis_ids": ["161725"], "force": false }`
(`oasis_ids` optional = all; `force` also re-files covered employees).

Needs **edit** permission on the form and `can_create_edit_form` (`403`);
`404` unknown/archived form; `400` missing `form_id`. Per selected employee
with `uncovered_codes` (or every leave employee with `force`): one request with
`source: "dot12"`, period = the form date, one day row per bucket (hours summed
per code, quantized to ¼ h, minimum 0.25; an `MLVPB` column sets
`military_code`), `filed_on_behalf` unless the employee is the caller, plus a
link (`origin: "dot12_to_leave"`, `task_asset_id` = the first matching column).
Each employee is serialized under `pg_advisory_xact_lock(hashtext('leave:<oasis>'))`
so a double-submit cannot double-create. Covered employees are skipped.

**Response** (`201` when anything was created, else `200`):
```json
{ "created": [ { "…full object…": "" } ], "skipped": [ { "oasis_id": "…", "reason": "covered" } ] }
```

---

#### `POST /dot12/api/leave-requests/{id}/create-dot12s`

Turn an **approved** request into DOT-12s (`400` in any other status). Caller
needs org edit on the request's `home_unit` (`403`).

**Request Body** (optional): `{ "dates": ["2026-09-07"] }` restricts the run.

For each day that carries an OASIS code (grievance days are skipped) and is not
already linked:
1. If a non-archived DOT-12 in `home_unit` on that date already lists the
   employee with a same-family leave column → **link** it (`linked[]`,
   `origin: "leave_to_dot12"`) instead of creating a duplicate.
2. Else if that day's pay period is past its edit deadline → `skipped`
   (`"pay period locked"`).
3. Else create one **draft** DOT-12 (`form_date` = the day, pay period from the
   2025-12-26 anchor) with the employee row and **one LEAV column per distinct
   code that day**: `ldpr_profile` = code, `activity "003"`,
   `is_participating false`, `program ""`, `unit_of_measure "EH"`,
   `receiving_unit` = `home_unit`, task order / route / BMP / EMP / account code
   null, `accomplished` = the hours, one employee charge for the hours;
   `form_details` = "Leave request #N — 8 h ANNLV (Doe, Pat)". Linked with
   `task_asset_id` = the first column.

Single transaction; re-running is a no-op (`"already linked"`). Creation
notifies the filer and employee (`leave_dot12s_created`).

**Response**:
```json
{ "created": [ { "form_id": 310, "leave_date": "2026-09-07" } ],
  "linked":  [ { "form_id": 301, "leave_date": "2026-09-08" } ],
  "skipped": [ { "leave_date": "2026-09-09", "reason": "already linked" } ],
  "request": { "…full object…": "" } }
```

---

#### `POST /dot12/api/leave-requests/{id}/links` · `DELETE /dot12/api/leave-requests/{id}/links/{link_id}`

Manual link / unlink to a DOT-12.

- **POST** body `{ "form_id": 301, "leave_date": "2026-09-07" }`. Not allowed on a
  withdrawn request; caller must be able to edit or approve the request, or be
  an admin or org editor, **and** have edit rights on the form (`403`). `404`
  unknown/archived form · `400` the form doesn't list the employee · `409`
  already linked. `origin: "manual"`.
- **DELETE**: party, admin, or org editor (`403`); `404` unknown link.

Both return the full object and record `link_dot12` / `unlink_dot12` on the
request plus `leave_link` / `leave_unlink` on the DOT-12 timeline.

---

#### Additions to existing endpoints

**`GET /dot12/api/forms/ui-summary`** gains two buckets (zeros when the flag is
off or the lookup fails):
```json
{ "leave_to_sign":    { "count": 1, "ids": [12] },
  "leave_to_approve": { "count": 2, "ids": [14, 9] } }
```
`leave_to_sign` = active requests naming the caller as employee with a signature
requested and not yet submitted; `leave_to_approve` = submitted requests the
caller may decide (chain / org-fallback / admin rule, one supervisor-edge query
shared across the walk).

**`GET /dot12/api/reports/hours-matrix?…&leave=1`** (labor matrix):
- every `employee_hours[oasis]` entry now carries `leave_hours` and
  `leave_codes` (`{code: hours}` over all eight leave codes) regardless of the
  flag; with `leave=1` it also carries `leave_request`:
  - `null` — no leave hours and no request that day;
  - `{ "id": null, "status": "none", … }` — DOT-12 leave hours but no request;
  - `{ "id", "status", "hours", "request_ids", "buckets", "codes", "linked", "linked_form_id" }`
    — the highest-precedence active request (approved > submitted >
    awaiting_signature > draft); `linked` = that day is linked to a
    **non-archived** DOT-12.
- top-level `leave_by_cell` (`"oasis|YYYY-MM-DD"` → the same cell object, so
  the grid can paint days with a request but zero hours) and `leave_requests`
  (`id` → `{ id, status, period_from, period_to, oasis_id, employee_name, decided_by, decided_at }`).
- employees / dates present only through a request are added (`employees[].source = "leave"`, zero-hour cells).
- The overlay is non-fatal: if the leave tables are absent it is simply omitted.

**`GET /dot12/api/reports/employee-day-detail`** adds
`leave_requests: [ { id, status, bucket, ldpr_code, hours, decided_by, decided_at, linked_form_ids } ]`
(active requests only; empty when the flag is off).

#### Leave notification types

| type | recipients | when |
|---|---|---|
| `leave_signature_needed` | the employee | filed on their behalf and sent for signature |
| `leave_approval_needed` | approver scope (minus the actor) | request submitted |
| `leave_approved` | filer + employee (minus the actor) | approved — body notes how many days can become DOT-12s |
| `leave_disapproved` | filer + employee (minus the actor) | disapproved — body is the reason |
| `leave_withdrawn` | other party + approvers | a non-draft request withdrawn |
| `leave_dot12s_created` | filer + employee (minus the actor) | draft DOT-12s created from the request |

All carry `link = /dot12/leave/{id}` and `dot12_notifications.leave_request_id`
(plain indexed integer, like `ticket_id`). Remarks are never included.

### PIN sign-in

Org → name → 4-digit PIN for staff with no state account. Blueprint
`routes/pin_auth.py`; rules in `dot12-logic.md` §21. Two prefixes:

**`/dot12/api/auth/pin` — public** (these *are* the sign-in). Every route:
`404` while the `pin_login` flag is off; `503 {"error": "PIN sign-in is not
configured on this server"}` while `DOT12_PIN_PEPPER` is unset; `429
{"error", "retry_after"}` (+ `Retry-After`) past the per-address hourly budget
(search 300, orgs/roster 120, lookup 60, enroll+login+change 100 and 30 per name, reset 20).

A member is `{token, display_name ("LAST, FIRST"), oasis_id (10-digit),
oasis_short (leading zeros dropped), title (job title, title-cased), org_code,
org_name}`. `token` = HMAC of the labor code and is the only identifier the
sign-in endpoints accept.

| Method | Path | Body | Response |
|---|---|---|---|
| GET | `/search?q=` | — | `{q, snapshot_available, total_matches, members: [...]}` — statewide, `q` = ≥2 letters of a name or ≥3 digits of an OASIS ID (leading zeros optional), ≤20 matches, last-name hits first; `400` below the minimum |
| GET | `/orgs` | — | `{orgs: [{code, name}], source: deighton\|snapshot\|users\|none}` |
| GET | `/roster?org=0260` | — | `{org, snapshot_available, members: [...]}` — one org, same member shape |
| POST | `/lookup` | `{token}` | `{status: enroll\|pin\|sso_required, reason, display_name}`; `404` when the token is not on the roster |
| POST | `/enroll` | `{token, pin, pin_confirm}` | `200 {message, user, session, home_path}` and a session cookie; `400` policy / mismatch; `409 {status, reason}` when the name is not in `enroll` state (incl. `sso_required`) |
| POST | `/login` | `{token, pin}` | `200` as above; `401 {"error": "Incorrect PIN", attempts_left}`; `423 {locked_until, retry_after}` while locked; `409` when no PIN is set / SSO-linked |
| POST | `/reset-request` | `{token}` | `200 {ok, already_pending, requested_at, notified}` (or `{ok, status: "enroll"}` when the name never enrolled); `409` for an SSO-linked name |
| POST | `/change` | `{current_pin, new_pin, new_pin_confirm}` | **session required** — `200 {ok}`; `401` wrong current PIN; `423` locked; `409` no PIN |

`status` values: `enroll` (choose a PIN — `reason` `new_account` /
`new_pin` / `reset_approved`), `pin` (enter it), `sso_required` (the name is
linked to a state account — `sso_linked`, or an SSO account of the same name
exists in this org — `name_match`). Lockout and pending resets are **not**
reported by `/lookup`. `/dot12/api/auth/mode` gains `pin_login: bool`; `/me`
gains `has_pin` and `session.auth_method`.

**`/dot12/api/admin/pin` — session-gated** (`401`, then flag `404`). The
caller may decide a request when they are an admin, in the employee's
supervisor chain, or — only when the employee has no chain — an approver
(`can_approve` + `can_edit`) for the employee's home org (`403` otherwise).

| Method | Path | Response |
|---|---|---|
| GET | `/reset-requests?status=pending\|approved\|denied\|expired\|all` | `{requests: [...], can_decide}` scoped to what the caller may decide; pending > 14 days are marked `expired` first |
| POST | `/reset-requests/{id}/approve` | body `{note?}` → the request, `approved`; nulls the PIN, sets `must_reset`, clears the lockout, bumps `users.auth_epoch` (live PIN sessions end); `409` if already decided |
| POST | `/reset-requests/{id}/deny` | body `{note?}` → the request, `denied` |
| POST | `/users/{user_id}/reset` | direct reset, no request needed (UserAdmin); `409` for an SSO-linked user |

A request row looks like `{id, user_id, org_code, status, requested_at,
decided_by, decided_at, note, employee: {id, first_name, last_name,
display_name, labor_code, org}, decider_name}`. `GET /forms/ui-summary` carries
`pin_resets: {count, ids}`; `GET /users` rows carry `has_pin`, `pin_set_at`,
`pin_locked_until`, `pin_must_reset`, `pin_reset_pending` (never the hash).

Notifications (bell only — never emailed): `pin_reset_requested` → the
confirmers, `link` `/dot12/pin-resets`; `pin_enrolled` → the confirmers when a
name is first claimed, `link` `/dot12/users?tab=config`.

---

## Error Responses

All endpoints return standard HTTP status codes:

- `200 OK` - Success
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `404 Not Found` - Resource not found
- `401 Unauthorized` - No session (leave-request routes)
- `403 Forbidden` - Session present but the caller's role / org scope does not allow the action
- `409 Conflict` - The action conflicts with current state (e.g. reopening a leave request whose linked DOT-12 is already approved; linking a DOT-12 twice)
- `500 Internal Server Error` - Server error

**Error Response Format**:
```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

**Examples**:
```json
{
  "error": "Not Found",
  "message": "Form 999 not found"
}
```

```json
{
  "error": "Bad Request",
  "message": "Missing required fields: form_date, home_unit"
}
```

---

## Data Types

### Date Fields
Format: `YYYY-MM-DD`
```json
{
  "form_date": "2025-03-15"
}
```

### DateTime Fields
Format: ISO 8601 with timezone
```json
{
  "created_at": "2025-03-15T10:30:00+00:00"
}
```

### Decimal/Numeric Fields
Sent as numbers, precision maintained
```json
{
  "hours_charged": 8.5,
  "accomplished": 30.25,
  "temperature": 45.5
}
```

### Boolean Fields
```json
{
  "status_active": true,
  "traffic_control": false
}
```

---

## Deep Update Examples

### Example 1: Add Employee and Charge to Existing Form

```bash
curl -X PUT http://localhost:5000/api/forms/1 \
  -H "Content-Type: application/json" \
  -d '{
  "employees": [
    ... existing employees with their IDs ...,
    {
      "oasis_id": "NEW123",
      "first_name": "New",
      "last_name": "Person",
      "display_order": 6
    }
  ]
}'
```

### Example 2: Update Employee Hours on Task Asset

```bash
curl -X PUT http://localhost:5000/api/forms/1 \
  -H "Content-Type: application/json" \
  -d '{
  "task_assets": [
    {
      "id": 1,
      "employee_charges": [
        {
          "id": 1,
          "hours_charged": 10.0
        }
      ]
    }
  ]
}'
```

### Example 3: Remove Employee (by omitting from list)

```bash
curl -X PUT http://localhost:5000/api/forms/1 \
  -H "Content-Type: application/json" \
  -d '{
  "employees": [
    {"id": 1, ...},
    {"id": 2, ...}
    // Employee ID 3 is omitted, so it will be deleted
  ]
}'
```

---

## Best Practices

### 1. Creating Forms

- Use `temp_id` to reference newly created objects in charges
- Provide all required fields: `form_date`, `home_unit`
- Include `pay_period_start` and `pay_period_end` for complete data

### 2. Updating Forms

- Always include object IDs for items you want to update
- Omit objects you want to delete
- For partial updates, you can send only the fields that changed
- Deep updates are transactional - all or nothing

### 3. Querying Forms

- Use pagination for large datasets
- Filter by date range to improve performance
- Use the summary endpoint for dashboard data

### 4. Performance

- Batch operations when possible
- Use `include_details=false` (list endpoint) for faster responses
- Create indexes on frequently queried fields

---

## Running the API

### Start the Server

```bash
python app.py
```

Server runs on `http://localhost:5000` by default.

### Environment Variables (Optional)

Create a `.env` file:
```
DATABASE_URL=<redacted-connection-string>localhost:5433/dot12
FLASK_ENV=development
FLASK_DEBUG=True
```

---

## Testing

See `test_api.py` for comprehensive test examples.

Quick test:
```bash
# Health check
curl http://localhost:5000/health

# Get all forms
curl http://localhost:5000/api/forms

# Get specific form
curl http://localhost:5000/api/forms/1
```

---

## Integration Notes

### DTIMS Integration
- Fields: `task_id_dtims`, `asset_id_dtims`, `route_bars`
- Store DTIMS references in task assets

**dTIMS task-asset lookup** — `GET /dot12/api/dtims/task-assets`
- Read-only search of active dTIMS tasks (`Task.ValidTo IS NULL`) by route /
  org / activity, reached through the `TAMSDW` linked server on the shared
  `Data-Warehouse` SQL Server (same connection as the Hub API,
  `utils/hub_client.py`).
- Query params (at least one of `query` / `org` / `activity` required):
  - `query` — free-text route search (`us60 cabell`, `I77 kanawha`,
    `cr 9 wayne`), or a BARS bridge number (`43A115`, exact match on the
    bridge). Parsed by `utils/route_id_parser.py`.
  - `org` — 4-digit org code (digits only).
  - `activity` — comma-separated activity code(s) (digits only).
  - `limit` — max rows, **default 50** (cap 1000).
- Returns `{filters, count, results}` — one row per task + route (deduped;
  `from_measure`/`to_measure` are the worked extent), each with a route
  `label`, `bars` (bridges only) and `last_accomp_on_task` (most recent
  accomplishment date for the task; `null` if none). DB down → `503`.
- See `dot12-logic.md` §8.15 for the full field decoding and join logic.

### OASIS HRM Integration
- Fields: `oasis_id`, `timei_document_id`
- Employee time tracking

### OASIS FIN Integration
- Fields: `ed_number`, `stock_item_number`, `oc_doc_id`
- Equipment and material tracking

---

## API Versioning

Current version: v1 (implicit)

Future versions will use URL prefix: `/api/v2/forms`
