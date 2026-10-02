# DOT-12 API: integration guide for Timekeeper

**Audience:** Timekeeper developers calling the DOT-12 server from Timekeeper's backend.
**Covers:** API-key authentication, acting on behalf of a Timekeeper user ("proxying"), DOT-12 forms and workflow, accounting autofill and validation.
**API version:** DOT-12 backend 1.11.20 (frontend 1.14.20), 2 October 2026.

| Environment | Base URL | Status |
|---|---|---|
| Test (mmsdev) | `https://mmsdev.transportation.wv.gov/dot12/api` | Available. Use this first. |
| Production | Provided when production access is issued | Not yet released |

Every path in this guide is relative to the base URL. For example, `GET /forms` means `GET https://mmsdev.transportation.wv.gov/dot12/api/forms`.

---

## Contents

**Part 1: Getting started**
1. [What you need](#1-what-you-need)
2. [Your first call](#2-your-first-call)
3. [Call as one of your users](#3-call-as-one-of-your-users)
4. [Create your first DOT-12](#4-create-your-first-dot-12)
5. [Fill in accounting automatically](#5-fill-in-accounting-automatically)
6. [.NET 8 setup for Timekeeper](#6-net-8-setup-for-timekeeper)
7. [The ten rules](#7-the-ten-rules)

**Part 2: Authentication and proxying in depth**
8. [API keys](#8-api-keys)
9. [Proxying a user with X-DOT12-Act-As](#9-proxying-a-user-with-x-dot12-act-as)
10. [Permissions: roles and orgs](#10-permissions-roles-and-orgs)
11. [Attribution, audit and the Timekeeper flag](#11-attribution-audit-and-the-timekeeper-flag)
12. [Security checklist](#12-security-checklist)

**Part 3: Working with DOT-12 forms**
13. [How a DOT-12 is structured](#13-how-a-dot-12-is-structured)
14. [Pay periods and the edit window](#14-pay-periods-and-the-edit-window)
15. [Create a form](#15-create-a-form)
16. [Read and list forms](#16-read-and-list-forms)
17. [Update a form](#17-update-a-form)
18. [Workflow: submit, approve, reject, enter](#18-workflow-submit-approve-reject-enter)
19. [Locks and archive](#19-locks-and-archive)

**Part 4: Accounting fields (autofill and validation)**
20. [Why use the accounting API](#20-why-use-the-accounting-api)
21. [Resolve: autofill one or many blocks](#21-resolve-autofill-one-or-many-blocks)
22. [Validate: check stored activity codes](#22-validate-check-stored-activity-codes)
23. [Picker searches](#23-picker-searches)
24. [Building the UI on top of it](#24-building-the-ui-on-top-of-it)

**Part 5: Server-side form rules**
25. [What changes when the rules are on](#25-what-changes-when-the-rules-are-on)

**Part 6: Reference**
26. [Endpoint reference](#26-endpoint-reference)
27. [Status codes and error messages](#27-status-codes-and-error-messages)
28. [Field reference](#28-field-reference)
29. [Codes and constants](#29-codes-and-constants)
30. [Troubleshooting](#30-troubleshooting)

---

# Part 1: Getting started

## 1. What you need

Before writing any code, get these three things lined up:

1. **An API key from the DOT-12 owner.** Keys are created on DOT-12's Config → API Keys page; only the DOT-12 system owners can issue them. You will receive one string that looks like this:

   ```
   dot12_3f9a..
   ```

   It is shown once and never again. Store it as a secret (section 8.3).

2. **The base URL**, from the table at the top.

3. **Your users in DOT-12.** To act as one of your users, that person must already have a DOT-12 account with their **e-number** (for example `E123456`), plus the role and orgs that let them do the work. Accounts are created automatically the first time someone signs in to DOT-12 with their state account; the DOT-12 owner can also add them in User Management. Section 9.4 covers what happens when the person isn't there.

The API is **server-to-server only**. Calls come from Timekeeper's server, never from a browser. The key must never reach a web page.

## 2. Your first call

List one form to prove the key works:

```bash
curl -s https://mmsdev.transportation.wv.gov/dot12/api/forms?limit=1 \
  -H "Authorization: Bearer $DOT12_API_KEY"
```

A working key returns `200` with a page of forms:

```json
{
  "forms": [ { "id": 24909, "form_date": "2026-10-01", "home_unit": "0409", "...": "..." } ],
  "total": 1834,
  "offset": 0,
  "limit": 1
}
```

Without the `X-DOT12-Act-As` header (next section), you are calling as the **key's own service account**. You only see forms in the orgs that account was given.

If the call fails, look up the status and message in [section 27](#27-status-codes-and-error-messages). The most common first-call problem is a key with a stray space or line break: `401 Malformed API key.`

## 3. Call as one of your users

Add one header with the Timekeeper user's e-number:

```bash
curl -s https://mmsdev.transportation.wv.gov/dot12/api/forms?limit=1 \
  -H "Authorization: Bearer $DOT12_API_KEY" \
  -H "X-DOT12-Act-As: E123456"
```

The request now runs **as that DOT-12 user**, exactly as if they had signed in to DOT-12 themselves:

- They can see and do what **their own** DOT-12 role and orgs allow. The key's service-account role plays no part.
- Everything the request creates, submits or approves carries **their name** in DOT-12's records and history.

That's the whole proxy model. Part 2 explains it in depth.

## 4. Create your first DOT-12

Create an empty DOT-12 for a home unit and date, as your user:

```bash
curl -s -X POST https://mmsdev.transportation.wv.gov/dot12/api/forms \
  -H "Authorization: Bearer $DOT12_API_KEY" \
  -H "X-DOT12-Act-As: E123456" \
  -H "Content-Type: application/json" \
  -d '{
        "form_date": "2026-10-01",
        "home_unit": "0409",
        "pay_period_start": "2026-09-19",
        "pay_period_end":   "2026-10-02"
      }'
```

The response is `201 Created`:

```json
{
  "message": "Form created successfully",
  "form": {
    "id": 25012,
    "form_date": "2026-10-01",
    "home_unit": "0409",
    "pay_period_start": "2026-09-19",
    "pay_period_end": "2026-10-02",
    "is_time_keeper": true,
    "prepared_by": null,
    "employees": [], "equipment": [], "materials": [], "task_assets": [],
    "...": "..."
  }
}
```

Points to notice:

- **The pay period is required.** It is the Saturday-to-Friday, two-week period containing `form_date` ([section 14](#14-pay-periods-and-the-edit-window)).
- **`is_time_keeper: true`** marks the form as created by Timekeeper, because your key is registered as a Timekeeper key.
- **The user must be allowed to edit org `0409`**, or the call returns `403 You do not have edit permission for org 0409`.

## 5. Fill in accounting automatically

You never need to work out LDPR, receiving unit, activity, N/P, program or phase yourself. Send what the user picked and DOT-12 fills in the rest, the same way its own editor does:

```bash
curl -s -X POST https://mmsdev.transportation.wv.gov/dot12/api/accounting/resolve \
  -H "Authorization: Bearer $DOT12_API_KEY" \
  -H "X-DOT12-Act-As: E123456" \
  -H "Content-Type: application/json" \
  -d '{ "home_unit": "0198", "form_date": "2026-10-01", "TaskWorkOrder": "250198382504" }'
```

The response holds the complete block, already shaped like Timekeeper's `ActivityCode`:

```json
{
  "valid": true,
  "kind": "mms",
  "kind_label": "MMS task order",
  "timekeeper": {
    "Ldprprofile": "17279",
    "ReceivingUnit": "0198",
    "ActivityNp": "382P",
    "SubActivity": null,
    "Program": "2021000638",
    "Phase": "OT0001",
    "TaskWorkOrder": "250198382504"
  },
  "fields": { "program": { "value": "2021000638", "locked": true, "lock_reason": "mms",
                           "lock_message": "Set by the task order — change or clear the task order to change it." }, "...": "..." },
  "errors": [],
  "warnings": []
}
```

Part 4 covers this in full, including validating every activity code a section already has.

## 6. .NET 8 setup for Timekeeper

This setup attaches the key and the signed-in user's e-number to every call automatically, so the rest of the code just calls methods on a typed client.

**`appsettings.json`.** Put the base URL here. Keep the key **out of this file**: use user-secrets locally, and an environment variable or the server's secret store in deployed environments.

```json
"Dot12": {
  "BaseUrl": "https://mmsdev.transportation.wv.gov/dot12/api/",
  "TimeoutSeconds": 60
}
```

```bash
# Environment variable (double underscore = section separator)
Dot12__ApiKey=<redacted>
```

**Options, handler and client:**

```csharp
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text.Json;
using Microsoft.Extensions.Options;

public sealed class Dot12Options
{
    public string BaseUrl { get; set; } = "";
    public string ApiKey { get; set; } = "";
    public int TimeoutSeconds { get; set; } = 60;
}

/// Adds the API key to every request, plus X-DOT12-Act-As with the signed-in
/// user's e-number (unless the caller already set one, e.g. a background job).
public sealed class Dot12AuthHandler : DelegatingHandler
{
    public const string ActAsHeader = "X-DOT12-Act-As";
    private readonly IHttpContextAccessor _http;
    private readonly IOptions<Dot12Options> _options;

    public Dot12AuthHandler(IHttpContextAccessor http, IOptions<Dot12Options> options)
    {
        _http = http;
        _options = options;
    }

    protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken ct)
    {
        request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", _options.Value.ApiKey);

        if (!request.Headers.Contains(ActAsHeader))
        {
            var eNumber = Dot12Identity.CurrentENumber(_http.HttpContext);
            if (!string.IsNullOrEmpty(eNumber))
                request.Headers.Add(ActAsHeader, eNumber);
        }
        return base.SendAsync(request, ct);
    }
}

public static class Dot12Identity
{
    /// The DOT-12 e-number for the current Timekeeper user: "E123456".
    /// Prefer Account.Enumber from tkp.Account (see section 9.3); this falls back
    /// to the WindowsAccountName claim and strips any "DOMAIN\" prefix.
    public static string? CurrentENumber(HttpContext? ctx)
    {
        var raw = ctx?.User.FindFirst(AppClaims.ENumber)?.Value;
        if (string.IsNullOrWhiteSpace(raw)) return null;
        var bare = raw.Split('\\').Last().Trim().ToUpperInvariant();
        return System.Text.RegularExpressions.Regex.IsMatch(bare, @"^[A-Z]\d{6}$") ? bare : null;
    }
}

public sealed class Dot12Client
{
    public static readonly JsonSerializerOptions Json = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,   // DOT-12 is snake_case
        DefaultIgnoreCondition = System.Text.Json.Serialization.JsonIgnoreCondition.WhenWritingNull,
    };

    private readonly HttpClient _http;
    public Dot12Client(HttpClient http) => _http = http;

    public async Task<JsonDocument> GetFormAsync(int id, CancellationToken ct = default)
    {
        using var resp = await _http.GetAsync($"forms/{id}", ct);
        await Dot12Error.ThrowIfFailedAsync(resp, ct);
        return await JsonDocument.ParseAsync(await resp.Content.ReadAsStreamAsync(ct), cancellationToken: ct);
    }

    public async Task<JsonDocument> ResolveAccountingAsync(object block, CancellationToken ct = default)
    {
        using var resp = await _http.PostAsJsonAsync("accounting/resolve", block, Json, ct);
        await Dot12Error.ThrowIfFailedAsync(resp, ct);
        return await JsonDocument.ParseAsync(await resp.Content.ReadAsStreamAsync(ct), cancellationToken: ct);
    }
}

public sealed class Dot12Exception : Exception
{
    public int Status { get; }
    public JsonElement? Body { get; }
    public Dot12Exception(int status, string message, JsonElement? body) : base(message)
    {
        Status = status;
        Body = body;
    }
}

public static class Dot12Error
{
    public static async Task ThrowIfFailedAsync(HttpResponseMessage resp, CancellationToken ct)
    {
        if (resp.IsSuccessStatusCode) return;
        JsonElement? body = null;
        string message = $"DOT-12 returned {(int)resp.StatusCode}";
        try
        {
            body = await resp.Content.ReadFromJsonAsync<JsonElement>(cancellationToken: ct);
            if (body.Value.TryGetProperty("error", out var e)) message = e.GetString() ?? message;
            if (body.Value.TryGetProperty("message", out var m) && m.GetString() is { } mm) message = mm;
        }
        catch (JsonException) { }
        throw new Dot12Exception((int)resp.StatusCode, message, body);
    }
}
```

**`Program.cs`:**

```csharp
builder.Services.AddHttpContextAccessor();
builder.Services.Configure<Dot12Options>(builder.Configuration.GetSection("Dot12"));
builder.Services.AddTransient<Dot12AuthHandler>();
builder.Services.AddHttpClient<Dot12Client>((sp, http) =>
{
    var o = sp.GetRequiredService<IOptions<Dot12Options>>().Value;
    http.BaseAddress = new Uri(o.BaseUrl);
    http.Timeout = TimeSpan.FromSeconds(o.TimeoutSeconds);
})
.AddHttpMessageHandler<Dot12AuthHandler>();
```

**A background job acting for a specific person** (with no `HttpContext`) sets the header itself:

```csharp
var req = new HttpRequestMessage(HttpMethod.Post, $"forms/{formId}/submit");
req.Headers.Add(Dot12AuthHandler.ActAsHeader, crewLeader.Enumber);   // from tkp.Account
using var resp = await httpClient.SendAsync(req, ct);
```

## 7. The ten rules

1. **Server-side only.** The key lives on Timekeeper's server and never goes to a browser.
2. **Always send the user.** Every call made for a person carries `X-DOT12-Act-As: <their e-number>`. Leave it off only for system work that belongs to no one.
3. **The user's own DOT-12 rights apply.** If they can't do it in DOT-12, they can't do it through you.
4. **The user must exist in DOT-12.** An unknown e-number gets `403`. Have them sign in to DOT-12 once, or ask the DOT-12 owner to add them.
5. **Field names are snake_case,** dates are `YYYY-MM-DD`, and amounts are numbers.
6. **Always send the pay period** on create: Saturday to Friday, containing `form_date`.
7. **Updates replace whole sections** you send (employees, equipment, materials, task_assets). Send each section complete, or leave its key out.
8. **New roster rows can be referenced by `temp_id` only in the create call.** On updates, save the rows first, read back their ids, then charge to them.
9. **Let DOT-12 do the accounting.** Use `/accounting/resolve` and `/accounting/validate`; don't re-implement LDPR, N/P or program/phase rules.
10. **Read the `error` message.** Every failure returns JSON with an `error` explaining exactly what happened.

---

# Part 2: Authentication and proxying in depth

## 8. API keys

### 8.1 Sending the key

Send the key on every request, either as a bearer token (preferred) or in its own header:

```
Authorization: Bearer dot12_<prefix>_<secret>
```

```
X-API-Key: dot12_<prefix>_<secret>
```

- **Prefix and secret.** The `<prefix>` is a short public identifier that also appears on DOT-12's API Keys page; the `<secret>` is the confidential part.
- **Storage.** DOT-12 stores only a one-way hash of the secret, so nobody (including the DOT-12 owner) can look a key up after it is created.
- **Cookies are ignored.** When a key is present, any DOT-12 session cookie on the request is ignored; the key is the whole identity.

### 8.2 What a key is

Each key belongs to its own **service account**: a DOT-12 user record created alongside the key and named after it (for example "Timekeeper prod (API key)").

- **Its role and orgs** are set by the DOT-12 owner when the key is issued. Any role is possible, including admin.
- **They apply only when no user is named.** Calls without `X-DOT12-Act-As` run as this service account. Calls with it run as the named user ([section 9](#9-proxying-a-user-with-x-dot12-act-as)).
- **The key also records which app it belongs to.** Timekeeper's keys are registered as the **Timekeeper** app, which is what marks forms they create ([section 11](#11-attribution-audit-and-the-timekeeper-flag)).
- **Each key has an "act as users" setting,** on by default. A key with it switched off cannot use `X-DOT12-Act-As` (`403`).

### 8.3 Storing, rotating and revoking keys

| Topic | Practice |
|---|---|
| Where to keep it | User-secrets locally; an environment variable or the server's secret store when deployed. Never in source control, `appsettings.json`, logs or error messages. |
| One key per environment | Separate keys for test and production, and preferably per deployment, so one can be revoked without breaking another. |
| Expiry | A key can carry an expiry date (valid through that day). Calls after it get `401 This API key has expired.` |
| Rotation | Ask the DOT-12 owner for a new key, deploy it, confirm traffic on the new one (the API Keys page shows **Last used**), then ask for the old one to be revoked. |
| Revocation | Immediate. The next call with that key gets `401 This API key has been revoked.` |
| Lost or leaked key | Report it to the DOT-12 owner immediately for revocation. A key that may proxy can act as **any** DOT-12 user, so treat it like an admin password. |

### 8.4 What keys cannot do

- **Key administration.** Keys cannot list, create or revoke API keys; those endpoints answer `403 API keys cannot use this endpoint.`
- **Browser use.** Keys are not meant for browsers. DOT-12 sends no CORS headers for them, and a key in a web page is a leaked key.

## 9. Proxying a user with X-DOT12-Act-As

### 9.1 The header

```
X-DOT12-Act-As: E123456
```

- **Format:** one letter followed by six digits, case-insensitive (`e123456` is fine). Anything else gets `400 X-DOT12-Act-As must be an e-number like E123456.`
- **Effect:** the request runs as that DOT-12 user, with their identity, their role and their orgs, exactly as if they had signed in.

### 9.2 Which permissions apply

| Call | Who DOT-12 treats you as | Permissions used |
|---|---|---|
| No `X-DOT12-Act-As` | The key's service account | The service account's role and orgs |
| `X-DOT12-Act-As: E123456` | DOT-12 user E123456 | **E123456's own** role and orgs |

Some consequences:

- **The key's role doesn't widen anyone's rights.** A field user proxied through an admin key still has field-user rights.
- **The key's role doesn't narrow them either.** An admin proxied through a viewer key has admin rights.
- **DOT-12's own rules apply to the proxied person,** for example "you cannot approve a form you prepared".

### 9.3 Which e-number to send

Send the e-number of the **person the action is for**, the one who should appear in DOT-12's records:

- **Normal requests:** the signed-in Timekeeper user. The most reliable source is `tkp.Account.Enumber` for the account the user is signed in as. The `WindowsAccountName` claim also carries it; strip any `DOMAIN\` prefix.
- **Delegation in Timekeeper.** In Timekeeper's own model, while someone is delegating, the `ENumber` claim is the *actor* and `UserId` is the account they act for. Decide which person DOT-12 should record and send that account's e-number. Timekeeper blocks signing while delegating; keep the same rule for DOT-12 submit and approve calls.
- **Background jobs** (imports, scheduled syncs): send the e-number of the person the work is attributed to, such as the crew leader. Send none if it belongs to the system, and it will then be recorded as the key's service account.

### 9.4 When the person isn't in DOT-12

An e-number with no DOT-12 account gets:

```
403 {"error": "No DOT-12 user has e-number E654321 — add them in DOT-12 User Management first."}
```

DOT-12 does not create accounts from API calls. To fix it:

1. **The person signs in to DOT-12 once** with their state account (single sign-on creates the account), or the DOT-12 owner adds them in User Management.
2. **The DOT-12 owner gives them a role and org access** that match their job. Section 10 lists the roles.

In Timekeeper, map this `403` to a clear message, for example "Your DOT-12 account isn't set up yet — contact the DOT-12 administrator." Don't retry it automatically.

### 9.5 Proxy checklist

- [ ] Every user-initiated call sends `X-DOT12-Act-As`.
- [ ] The e-number is validated as `^[A-Z]\d{6}$` before sending.
- [ ] `403 No DOT-12 user …` is shown to the user, not retried.
- [ ] Background jobs set the header explicitly, or deliberately leave it out.
- [ ] Logs record the e-number used, never the API key.

## 10. Permissions: roles and orgs

What a proxied user can do is decided by their DOT-12 role and org access.

**Roles** (the common ones; the DOT-12 owner assigns them):

| Role | View forms | Create / edit forms | Approve | HRM / FIN entry | Notes |
|---|---|---|---|---|---|
| `viewer` | ✓ | | | | Read-only |
| `field_user` | ✓ | ✓ | | | Crew leaders, timekeepers |
| `approver` | ✓ | ✓ | ✓ | ✓ | Supervisors |
| `time_entry_approval` | ✓ | | | ✓ | HRM / FIN clerks |
| `admin` | ✓ | ✓ | ✓ | ✓ | Every org |
| `employee` | | | | | Staff without DOT-12 duties |

**Orgs:**

- **Read access.** A user sees forms for the orgs they are assigned, by 4-digit org code such as `0409`.
- **Edit access.** Editing needs *edit* access on the form's org.
- **Admins** see every org.

When a call is outside the user's rights, the API answers `403` with the reason, for example `You do not have edit permission for org 0409` or `Permission denied`.

## 11. Attribution, audit and the Timekeeper flag

- **Who did it.** Forms created, submitted, approved, rejected or entered through a proxied call record **that person**. This covers DOT-12's created-by, prepared-by and approved-by fields, the form history, notifications, and the field-by-field change log.
- **Where it came from.** DOT-12's change log also records that the change came through the API, from the Timekeeper app.
- **`is_time_keeper` on forms.**
  - It is `true` when the form was **created** through a Timekeeper key. It is never set from what you send, and never cleared.
  - It does **not** change when a Timekeeper key edits a form created elsewhere.
  - It appears on every form and in the forms list. DOT-12's screens show a small clock marker and a "Timekeeper" label on these forms.
- **Key usage.** DOT-12 records when each key was last used, shown to the DOT-12 owner on the API Keys page.

## 12. Security checklist

- [ ] The key is in a secret store, not in code, config files or logs.
- [ ] All calls go over HTTPS from Timekeeper's server; never from a browser.
- [ ] `X-DOT12-Act-As` is set from server-side identity (the signed-in user's account), never from anything the browser sends.
- [ ] Timekeeper checks its own permissions (managed sections, orgs) **before** calling DOT-12; DOT-12 then checks the user's DOT-12 rights again.
- [ ] Separate keys exist per environment, with a rotation plan (section 8.3).
- [ ] A suspected leak is reported to the DOT-12 owner at once for revocation.

---

# Part 3: Working with DOT-12 forms

## 13. How a DOT-12 is structured

A DOT-12 is one crew's day on one sheet:

```
form                     date, home unit, pay period, signatures, status
├── employees[]          the crew roster          (oasis_id, names, temporary upgrade)
├── equipment[]          equipment roster         (ED number, description, operator initials, ending meter)
├── materials[]          inventory roster         (description, warehouse, stock number + suffix, UOM)
└── task_assets[]        the columns, 1…n         one accounting line each
      ├── accounting     ldpr_profile, receiving_unit, activity, is_participating (N/P),
      │                  sub_activity, program, phase, task_order_number, …
      ├── road           route_bars, beg_measure, end_measure, accomplished, unit_of_measure
      ├── back page      weather, temperature, description, traffic_control
      ├── employee_charges[]    hours per employee in this column
      ├── equipment_charges[]   hours per equipment in this column
      └── material_charges[]    quantity per material in this column
```

A **charge** links a roster row to a column. For example, "employee 42 worked 8 hours on column 1" is one row in column 1's `employee_charges`.

**The form's status** is worked out from its sign-offs. There is no status field you can set:

| Status | Meaning |
|---|---|
| draft | Not yet submitted |
| submitted | `prepared_by` set, waiting for approval |
| rejected | Sent back with a reason (`is_rejected`, `rejection_reason`) |
| approved | `approved_by` set |
| approved-hrm / approved-fin | Entered in OASIS-HRM or -FIN |
| final | Approved and entered in both HRM and FIN |

## 14. Pay periods and the edit window

- **Pay periods are two weeks, Saturday to Friday,** on the WV Division of Administrative Services calendar. Example: `2026-09-19` to `2026-10-02`.
- **To compute one:** find the Friday that ends the two-week block containing the date, counting in 14-day steps from the anchor period ending Friday `2025-12-26`. Then `pay_period_start` is that Friday minus 13 days.

```csharp
static (DateOnly Start, DateOnly End) PayPeriod(DateOnly date)
{
    var anchorEnd = new DateOnly(2025, 12, 26);                        // a period's Friday
    var days = date.DayNumber - anchorEnd.DayNumber;
    var periods = (int)Math.Floor(days / 14.0);                        // floor, not truncate
    var end = anchorEnd.AddDays(periods * 14);
    if (date > end) end = end.AddDays(14);
    return (end.AddDays(-13), end);
}
```

> Use `Math.Floor`. Integer division truncates toward zero and puts dates before the anchor into the wrong period.

**The edit window.** A form can be changed until **7 days after** its pay period ends: through the following Friday, Eastern time. After that the pay period is closed and the form is **read-only for everyone**. Edits get `403 This pay period is closed for editing — the form is read-only.` Recall is no longer possible either.

Each form carries `period_edit_deadline` and `is_period_locked`, so you can show this ahead of time.

## 15. Create a form

`POST /forms` creates the form and its whole contents in one call. Roster rows can carry a **`temp_id`** (any string you choose), and charges in the same call refer to them with `employee_temp_id`, `equipment_temp_id` or `material_temp_id`:

```json
{
  "form_date": "2026-10-01",
  "home_unit": "0409",
  "pay_period_start": "2026-09-19",
  "pay_period_end": "2026-10-02",
  "form_details": "Pothole patching, CR 9",

  "employees": [
    { "temp_id": "e1", "oasis_id": "0000130836", "first_name": "Pat", "last_name": "Doe", "display_order": 1 },
    { "temp_id": "e2", "oasis_id": "0000161725", "first_name": "Sam", "last_name": "Roe", "display_order": 2 }
  ],
  "equipment": [
    { "temp_id": "q1", "ed_number": "1310293", "equipment_description": "TRACTOR, BOOM MOWER",
      "operator_initials": "PD", "ending_meter": 48211, "status_active": true, "display_order": 1 }
  ],
  "materials": [],

  "task_assets": [
    {
      "column_number": 1,
      "task_order_number": "250198382504",
      "ldpr_profile": "17279", "receiving_unit": "0198", "activity": "382", "is_participating": true,
      "program": "2021000638", "phase": "OT0001", "unit_of_measure": "LM",
      "route_bars": "CR 9", "beg_measure": 1.2, "end_measure": 1.9, "accomplished": 0.7,
      "weather": "Clear", "temperature": 61, "description": "Patched 14 potholes", "traffic_control": true,
      "employee_charges":  [ { "employee_temp_id": "e1", "hours_charged": 8 },
                             { "employee_temp_id": "e2", "hours_charged": 8 } ],
      "equipment_charges": [ { "equipment_temp_id": "q1", "hours_charged": 6.5 } ]
    },
    {
      "column_number": 2,
      "ldpr_profile": "SCKLV",
      "employee_charges": [ { "employee_temp_id": "e2", "hours_charged": 0 } ]
    }
  ]
}
```

- **Required fields:** `form_date`, `home_unit`, `pay_period_start`, `pay_period_end`; `column_number` on each column; `ed_number` on each equipment row.
- **`oasis_id`** is the 10-digit OASIS id. DOT-12 left-pads it with zeros on create.
- **Accounting:** get these values from `/accounting/resolve` ([Part 4](#part-4-accounting-fields-autofill-and-validation)) rather than computing them.
- **Charges:** `hours_charged` and `quantity_charged` allow 2 decimal places. A charge whose temp id doesn't match a roster row is dropped.
- **Response:** `201` with `{ "message", "form" }`. The `form` contains the real ids for every row and column; keep them for later updates.

## 16. Read and list forms

**One form:** `GET /forms/{id}` returns the full form. The top-level fields are:

```
id, form_date, pay_period_start, pay_period_end, home_unit, receiving_unit, ldpr_profile, form_details,
prepared_by, prepared_at, approved_by, approved_at, entered_by_hrm, entered_by_hrm_at, entered_by_fin, entered_by_fin_at,
is_rejected, rejection_reason, is_archived, is_created_mobile, is_time_keeper,
period_edit_deadline, is_period_locked, created_by_user_id, created_at, updated_at,
employees[], equipment[], materials[], task_assets[], tags[]
```

The signature fields (`prepared_by` and the others) are user summaries: `{ id, first_name, last_name, e_number, … }`.

**The list:** `GET /forms` returns the forms the user may see:

| Parameter | Example | Meaning |
|---|---|---|
| `offset`, `limit` | `offset=0&limit=50` | Paging (limit ≤ 200) |
| `home_unit` | `0409` | One org |
| `orgs` | `0409,0198` | Several orgs |
| `start_date`, `end_date` | `2026-09-19` | Form-date range |
| `status` | `submitted,rejected` | Any of: `draft`, `submitted`, `rejected`, `approved`, `approved-hrm`, `approved-fin`, `final` |
| `form_ids` | `25012,25013` | Specific forms |
| `search` | `CR 9` | Text in the description or the form id |
| `sort`, `dir` | `sort=form_date&dir=desc` | `created_at`, `form_date`, `form_details`, `home_unit` |

The response is `{ "forms": [...], "total", "offset", "limit" }`. For very long filters (hundreds of `form_ids`), `POST /forms/query` accepts the same parameters as a JSON body.

**Forms waiting on a person** (with `X-DOT12-Act-As` set to that person):

- `GET /forms/pending-approvals`: forms waiting for their approval.
- `GET /forms/pending-entries`: approved forms waiting for their HRM or FIN entry.
- `GET /forms/my-rejections`: their forms that were sent back.

## 17. Update a form

`PUT /forms/{id}` with the parts you are changing.

**How sections update:**

| You send | DOT-12 does |
|---|---|
| A header field (`form_date`, `form_details`, …) | Updates that field |
| A section key (`employees`, `equipment`, `materials`, `task_assets`) | **Replaces that whole section**: rows with an `id` are updated, rows without one are created, and existing rows you left out are **deleted** |
| No section key | Leaves that section untouched |
| `employee_charges` (or equipment / material) inside a column | Replaces that column's charges the same way |

So **always send a section complete**. To change one employee's name, send the full `employees` list with every row's `id`.

**Adding roster rows and charging them in one go.** Temp ids work only on **create**. On an update, do it in two steps:

1. `PUT` the section with the new row (no `id`). The response contains its new `id`.
2. `PUT` the column's charges using that real `employee_id`.

**Charges reference real ids on updates:**

```json
{
  "task_assets": [
    { "id": 88101, "column_number": 1, "...": "all the column's fields",
      "employee_charges": [ { "id": 990211, "employee_id": 77311, "hours_charged": 7.5 } ] }
  ]
}
```

- **Signatures** (`prepared_by`, `approved_by`, …) can't be set here; use the workflow calls in section 18.
- **Concurrency.** There is no version check: the last write wins. If DOT-12's own editor and Timekeeper can both edit the same form, re-read it (`GET /forms/{id}`) before saving, and keep edit sessions short.
- **Response:** `200` with `{ "message", "form" }`.

## 18. Workflow: submit, approve, reject, enter

All workflow calls are `POST`s with an empty body, except reject. They act as the proxied user and return the updated form.

| Call | Who may | Effect |
|---|---|---|
| `POST /forms/{id}/submit` | Create/edit rights on the org | Signs **Prepared by** and sends the form for approval. The pay period must be a valid Saturday-to-Friday period containing the form date. |
| `POST /forms/{id}/approve` | Approve rights on the org; **not** the person who prepared it | Signs **Approved by** |
| `POST /forms/{id}/reject` with `{"rejection_reason": "…"}` | Approve rights; not the preparer | Sends the form back; a reason is required |
| `POST /forms/{id}/recall` | The submitter or an admin (an HRM/FIN entry role too, while it is only submitted); not once entered in HRM or FIN, and not after the period closes | Pulls a submitted or approved form back to draft |
| `POST /forms/{id}/reopen` | Within the edit window | Clears all signatures; back to draft |
| `POST /forms/{id}/enter-hrm` | HRM entry roles (`approver`, `time_entry_approval`, `admin`) | Signs **Entered in HRM**; approved forms only |
| `POST /forms/{id}/enter-fin` | FIN entry roles | Signs **Submitted in FIN**; approved forms only |

- **Snapshots.** Each approve, HRM entry and FIN entry stores a permanent, tamper-evident snapshot of the form. `GET /forms/{id}/approvals` lists them.
- **History.** `GET /forms/{id}/timeline` is the form's history, and `GET /forms/{id}/changes` the field-by-field change log.

## 19. Locks and archive

| Situation | What happens on edit |
|---|---|
| Approved (or beyond) | `403`. Only the OC document id on materials can still change, and only by entry roles. |
| Pay period closed (section 14) | `403 This pay period is closed for editing — the form is read-only.` |
| Archived | `404` |

**Archive** (DOT-12's "delete") is `DELETE /forms/{id}`. The form is hidden everywhere but kept, and only a DOT-12 administrator can restore it. Approved and closed forms can't be archived.

---

# Part 4: Accounting fields (autofill and validation)

## 20. Why use the accounting API

DOT-12 fills accounting from many sources: MMS task orders, TheHub projects, BS95 overhead programs, AssetWorks equipment work orders, annual-plan programs, and leave codes. Each has its own rules about which fields it sets and which become locked. DOT-12's editor applies those rules as the user picks values.

The accounting API runs **the same rules on the server** and hands you the result, so Timekeeper never re-implements them.

- **Read-only.** It never saves anything.
- **Accepts Timekeeper's field names.** It takes Timekeeper's `ActivityCode` names directly and always answers with a `timekeeper` block in that shape.
- **Live sources.** Lookups go straight to OM_WVDOT (Deighton) and TheHub, so answers reflect today's data.

**Field mapping:**

| Timekeeper `ActivityCode` | DOT-12 column field | Notes |
|---|---|---|
| `Ldprprofile` | `ldpr_profile` | |
| `ReceivingUnit` | `receiving_unit` | 4 digits |
| `ActivityNp` (`"382P"`) | `activity` (`"382"`) + `is_participating` (`true`) | Split and joined for you |
| `SubActivity` | `sub_activity` | |
| `Program` | `program` | |
| `Phase` | `phase` | |
| `TaskWorkOrder` | `task_order_number` | |
| (none) | `account_code_id_dtims`, `task_id_dtims`, … | Returned in `ids`, for DOT-12 forms |

> Timekeeper has no account-code field, and doesn't need one. DOT-12 account codes are per fiscal year, so a stored one would go stale every July. Send `Program` + `Phase` and DOT-12 finds the right fiscal year's account code for the form date.

## 21. Resolve: autofill one or many blocks

`POST /accounting/resolve`

**One block:** the request fields plus `home_unit` (required) and `form_date` (optional; defaults to today, Eastern):

```json
{ "home_unit": "0409", "form_date": "2026-10-01", "TaskWorkOrder": "250409288000" }
```

**Many blocks** (up to 200): wrap them in `items`. `defaults` are merged into every item, and `key` is any value of yours, echoed back on the result:

```json
{
  "home_unit": "0409",
  "form_date": "2026-10-01",
  "defaults": { "ReceivingUnit": "0409" },
  "items": [
    { "key": "row-1", "TaskWorkOrder": "250409288000" },
    { "key": "row-2", "Ldprprofile": "ANNLV" },
    { "key": "row-3", "Program": "D04AP", "ActivityNp": "512N" }
  ]
}
```

**What you can send in a block:**

| Send | DOT-12 does |
|---|---|
| `TaskWorkOrder` / `task_order_number` (MMS task order) | Fills everything from the task: activity, program, phase, receiving unit, unit of measure, plus LDPR and N/P from TheHub, plus the route |
| `work_order` (`HW05-2026-12` or its task order id) | Equipment work order: program `EQPWO`, LDPR `17276`, activity from the repair reason, receiving unit from the equipment's org |
| `account_code` (display value) or `account_code_id_dtims` | Program and phase from the account code; BS95 or TheHub handling as applicable |
| `Program` (+ `Phase`), with no task order | Finds the account code for that program/phase in the form date's fiscal year, then as above |
| `Ldprprofile` = a leave code (`ANNLV`, `SCKLV`, …) | The leave pattern: activity `003`, N, unit EH, receiving unit = home unit, program blank |
| Any other field | Kept, then checked |

**The response** (one per block):

```json
{
  "key": "row-1",
  "valid": true,
  "kind": "mms",
  "kind_label": "MMS task order",
  "fields": {
    "task_order_number": { "value": "250409288000", "label": "Task / work order", "locked": false, "...": "..." },
    "ldpr_profile":   { "value": "17237", "locked": true,  "lock_reason": "mms",
                        "lock_message": "Set by the task order — change or clear the task order to change it.",
                        "required": false, "errors": [], "warnings": [] },
    "receiving_unit": { "value": "0409",  "locked": true,  "lock_reason": "mms", "required": true, "...": "..." },
    "activity":       { "value": "288",   "locked": true,  "...": "..." },
    "is_participating": { "value": false, "locked": true, "...": "..." },
    "sub_activity":   { "value": null,    "locked": false, "options": null, "...": "..." },
    "program":        { "value": "D04AP", "locked": true,  "...": "..." },
    "phase":          { "value": null,    "locked": true,  "...": "..." },
    "unit_of_measure":{ "value": "EA",    "locked": true,  "lock_reason": "mms", "...": "..." }
  },
  "ids": { "task_id_dtims": 10015, "account_code_id_dtims": 4471, "account_code_display_value": "…",
           "hub_project_number": null, "is_bs95": false, "assetworks_work_order": null },
  "route": { "route_bars": "CR 9", "route_county": "Wood", "asset_id_dtims": 77,
             "beg_measure": null, "end_measure": null,
             "options": [ { "asset_id_dtims": 77, "label": "CR 9", "county": "Wood", "from": 0.0, "to": 4.5, "is_bridge": false } ] },
  "timekeeper": { "Ldprprofile": "17237", "ReceivingUnit": "0409", "ActivityNp": "288N",
                  "SubActivity": null, "Program": "D04AP", "Phase": null, "TaskWorkOrder": "250409288000" },
  "changes": [ { "field": "program", "from": null, "to": "D04AP", "message": "program filled in as D04AP (task order 250409288000)." } ],
  "errors": [],
  "warnings": []
}
```

**`kind` values:**

| Kind | Meaning |
|---|---|
| `mms` | MMS task order |
| `eqp` | AssetWorks equipment work order |
| `hub` | TheHub project (program = project number) |
| `bs95` | BS95 overhead program |
| `leave` | Leave code |
| `account` | An account code with no project behind it |
| `none` | Untyped; DOT-12 will flag it |

## 22. Validate: check stored activity codes

`POST /accounting/validate` takes the same body as resolve but is **strict**: any field whose correct value differs from the one you sent is an **error** (`rule: "mismatch"`). Use it to check an activity code before saving it, or to audit a whole section's codes at once:

```json
{
  "home_unit": "0198",
  "form_date": "2026-10-01",
  "items": [
    { "key": 11, "TaskWorkOrder": "250198382504", "Program": "NOPE", "ActivityNp": "999N", "ReceivingUnit": "0198" },
    { "key": 12, "Ldprprofile": "ANNLV", "ActivityNp": "003N", "ReceivingUnit": "0198" }
  ]
}
```

```json
{
  "valid": false,
  "invalid_count": 1,
  "items": [
    { "key": 11, "valid": false,
      "errors": [
        { "rule": "mismatch", "field": "activity", "message": "Activity should be 382 for this MMS task order, not 999." },
        { "rule": "mismatch", "field": "program",  "message": "Program should be 2021000638 for this MMS task order, not NOPE." },
        { "rule": "mismatch", "field": "is_participating", "message": "N / P should be P for this MMS task order, not N." }
      ],
      "timekeeper": { "...": "the corrected block" } },
    { "key": 12, "valid": true, "...": "..." }
  ]
}
```

**The three validation layers:**

1. **Format** (Timekeeper's `ActivityCode` limits):
   - receiving unit is required and must be 4 digits
   - activity must be 3 digits
   - N/P is required
   - program, phase and task order are limited to 50 characters
   - a sub-activity over 50 characters, or an unknown LDPR, is only a warning
2. **DOT-12 column rules:**
   - the task order, work order, account code or TheHub project must exist
   - the account code must be valid in the form date's fiscal year
   - an equipment work order needs a sub-activity
   - a sub-activity must be on the published list for its activity
   - TheHub and BS95 lines need an activity
   - a line with accounting must have a type
3. **Mismatches** (validate only): every derived field must agree with what you sent.

**Warnings never make a block invalid.** If OM_WVDOT or TheHub can't be reached, the result carries a warning with `rule: "unverified"` and your values are kept. Retry later for a definite answer.

## 23. Picker searches

All picker searches take `GET`. Searches need `q` of at least 2 characters.

| Endpoint | Returns |
|---|---|
| `GET /accounting/catalog` | Field list (labels, required, max length, pattern, Timekeeper name), LDPR profiles with labels, leave / annual-plan / equipment patterns, lock messages. Cache it. |
| `GET /accounting/task-orders?q=2504&home_unit=0409` | Active MMS task orders: number, name, activity, program, phase, receiving unit, unit of measure, asset count, annual-plan flag |
| `GET /accounting/account-codes?q=D04AP&form_date=2026-10-01` | Account codes valid on that date, tagged `is_bs95` / `annual_plan` |
| `GET /accounting/work-orders?q=0526` | AssetWorks work orders by task order id or ED number |
| `GET /accounting/activities?q=pothole` | Activity codes with unit of measure, daily production and `has_sub_activities` |
| `GET /accounting/sub-activities?activity=510` | The published sub-activity list for an activity |

The OM_WVDOT-backed searches (task orders, account codes) answer `503` when OM_WVDOT is slow or down. Show "try again shortly".

## 24. Building the UI on top of it

A clean editor for an activity code or a DOT-12 line:

1. **On page load,** fetch `/accounting/catalog` once and cache it.
2. **When the user picks a source** (task order, work order, program/phase, leave code), call `/accounting/resolve` with what they picked and the home unit and date.
3. **Render each field from `fields`:**
   - `locked: true` → read-only, with `lock_message` as the tooltip.
   - `options` present → a dropdown (sub-activity, LDPR).
   - `errors` / `warnings` → shown under the field.
4. **Show `changes`** as "filled in by DOT-12" hints.
5. **On save,** call `/accounting/validate` for the block, and save `timekeeper` (for an `ActivityCode`) or the DOT-12 field values (for a DOT-12 line).
6. **For a section admin page,** run `/accounting/validate` over all its codes in one call (`items`, up to 200) and list the ones that aren't `valid`.

---

# Part 5: Server-side form rules

## 25. What changes when the rules are on

DOT-12 has a setting, `form_rules_enforce`, that makes the server apply the editor's rules on **every** save, from any client. **It is off today.** When the DOT-12 owner turns it on:

- **Saves autofill.** DOT-12 overwrites accounting fields it owns (as in Part 4), the pay period, EH accomplishment and similar. It tells you what changed in a `rules` block:

  ```json
  { "message": "Form updated successfully", "form": { "...": "..." },
    "rules": { "notices": [ { "id": "notice-program-1", "type": "notice", "field": "program",
                              "columnNumber": 1, "message": "Column 1 program changed from X to T123456 (task order …)." } ],
               "warnings": [ "..." ],
               "gates": [ "..." ] } }
  ```

  Take the values from the returned `form`; they are authoritative.

- **Impossible values are refused** with `422`, and nothing is saved:

  ```json
  { "error": "validation_failed", "message": "The form has values the server cannot accept.",
    "checks": [ { "id": "err-employee-charge-24-1-e1", "rule": "hours_cell", "type": "error", "mode": "reject",
                  "message": "Column 1: the employee e1 charge is 30 hours — one entry cannot exceed 24.",
                  "field": null, "columnNumber": 1, "fieldName": "" } ] }
  ```

  Refused values are:
  - one hours entry over 24
  - more than 2 decimal places
  - negative or non-numeric amounts
  - the same person charged twice in a column
  - operator initials over 10 characters
  - a non-numeric meter
  - a charge to another form's row
  - a date in a closed pay period

- **Submit waits for completeness.** "Gate" checks are reported on every save in `rules.gates` but only block **submit**, which then answers `422` with the list. Gate checks include:
  - a column with no type
  - mileposts outside the route
  - more than 24 hours in a day for one person
  - a missing meter or operator initials
  - a temporary upgrade the employee's title doesn't allow
  - an already-submitted form
- **Warnings** (retired employee or equipment, someone from another org, a lookup that couldn't be reached) never block.
- **Dry run.** `GET /forms/{id}/rules-check` returns what a save would change or block, without saving. It returns `404` while the rules are off.

**Get ready now:**

- Handle `422` with `checks`.
- Read `rules` when it's present.
- Always use the returned `form` after a save.

All of this costs nothing while the rules are off.

---

# Part 6: Reference

## 26. Endpoint reference

All paths are under `/dot12/api`. "Act-as" means the call uses the proxied user's rights.

**Forms**

| Method and path | Purpose |
|---|---|
| `GET /forms` · `POST /forms/query` | List (section 16) |
| `GET /forms/{id}` | One form |
| `POST /forms` | Create (section 15) |
| `PUT /forms/{id}` | Update (section 17) |
| `DELETE /forms/{id}` | Archive |
| `GET /forms/{id}/timeline` · `/changes` · `/approvals` | History, change log, approval snapshots |
| `GET /forms/{id}/prior-meters?ed=1310293` | Last recorded ending meter per ED number before this form |
| `GET /forms/{id}/rules-check` | Form rules dry run (rules on only) |
| `GET /pay-periods` | Pay periods that have forms |

**Workflow**

| Method and path | Purpose |
|---|---|
| `POST /forms/{id}/submit` · `/approve` · `/reject` · `/recall` · `/reopen` · `/enter-hrm` · `/enter-fin` | Section 18 |
| `GET /forms/pending-approvals` · `/pending-entries` · `/my-rejections` | Work waiting on the proxied user |

**Accounting**

| Method and path | Purpose |
|---|---|
| `GET /accounting/catalog` | Field and code catalog |
| `POST /accounting/resolve` | Autofill |
| `POST /accounting/validate` | Strict validation (batch ≤ 200) |
| `GET /accounting/task-orders` · `/account-codes` · `/work-orders` · `/activities` · `/sub-activities` | Picker searches |

## 27. Status codes and error messages

Every error is JSON with an `error` string. Validation failures also carry `checks`.

| Status | `error` (exact text) | Cause | Fix |
|---|---|---|---|
| 401 | `Not authenticated` | No key or session | Send `Authorization: Bearer …` |
| 401 | `Malformed API key.` | Not in `dot12_<prefix>_<secret>` form | Check for spaces, quotes or line breaks |
| 401 | `Invalid API key.` | Unknown prefix or wrong secret | Use the exact key you were given |
| 401 | `This API key has been revoked.` | Revoked | Get a new key |
| 401 | `This API key has expired.` | Past its expiry date | Get a new key |
| 400 | `X-DOT12-Act-As must be an e-number like E123456.` | Bad header value | Send `^[A-Z]\d{6}$` |
| 403 | `This API key may not act as a user (X-DOT12-Act-As).` | Proxying is disabled on this key | Ask for a key with proxying on |
| 403 | `No DOT-12 user has e-number E…` | Person not in DOT-12 | Section 9.4 |
| 403 | `Permission denied` | The user's role lacks the permission | Role change in DOT-12 |
| 403 | `You do not have edit permission for org NNNN` | Org access missing | Org access in DOT-12 |
| 403 | `This pay period is closed for editing — the form is read-only.` | Past the edit window | Nothing; the form is final |
| 403 | `API keys cannot use this endpoint.` | Key-administration endpoints | Not available to keys |
| 400 | e.g. `Missing required fields: form_date` · `rejection_reason is required` | Bad input | Fix the request |
| 404 | `Form N not found` | Wrong id, or archived | |
| 422 | `validation_failed` (+ `checks`) | Form rules refused the save or submit (rules on) | Fix each check |
| 503 | `OM_WVDOT is not responding — try again shortly` | Upstream slow or down (searches) | Retry with backoff |
| 500 | (message) | Unexpected server error | Report it with the time and form id |

**Retry policy:**

- **Retry** `503`, and network errors, with backoff.
- **Never retry** `400`, `401`, `403` or `422`. They won't change until something is fixed.

## 28. Field reference

**Form header**

| Field | Type | Notes |
|---|---|---|
| `form_date` | date | Required |
| `home_unit` | string(4) | Required. Org code. |
| `pay_period_start` / `pay_period_end` | date | Required. Saturday / Friday (section 14). |
| `receiving_unit`, `ldpr_profile` | string | Form-level defaults (optional) |
| `form_details` | text | Free-text description of the day |
| `is_time_keeper` | bool | Read-only (section 11) |

**Employee:** `id`, `temp_id` (create only), `oasis_id` (10 digits), `first_name`, `last_name`, `temporary_upgrade` (pay code, e.g. `T495E`), `display_order`.

**Equipment:** `id`, `temp_id`, `ed_number` (required; 7 digits, e.g. `1310293`), `equipment_description`, `operator_initials` (≤ 10), `ending_meter` (integer), `status_active` (bool; prints O / N), `display_order`.

**Material:** `id`, `temp_id`, `material_description`, `org_whse` (warehouse org, or `DIRECT BILL`), `stock_item_number`, `commodity_suffix`, `uom_abbreviation`, `oc_doc_id`, `display_order`.

**Column (`task_assets[]`)**

| Group | Fields |
|---|---|
| Identity | `id`, `column_number` (required) |
| Accounting | `ldpr_profile`, `receiving_unit`, `activity` (3 digits), `is_participating` (bool: P = true), `sub_activity`, `program`, `phase`, `task_order_number` |
| DOT-12 links | `task_id_dtims`, `account_code_id_dtims`, `account_code_display_value`, `hub_project_number`, `assetworks_work_order` (take these from `/accounting/resolve` `ids`) |
| Road | `route_bars`, `route_county`, `asset_id_dtims`, `beg_measure`, `end_measure` (3 decimals), `accomplished` (2 decimals), `unit_of_measure` |
| Back page | `weather`, `temperature` (number), `description`, `traffic_control` (bool) |
| Charges | `employee_charges[]` (`id`, `employee_id` or `employee_temp_id`, `hours_charged`); `equipment_charges[]` (same, `equipment_…`); `material_charges[]` (`material_…`, `quantity_charged`, `oc_doc_id`) |

## 29. Codes and constants

**LDPR profiles**

| Code | Meaning |
|---|---|
| `17237` | Annual Plan default (forced for `D01AP`–`D10AP` programs) |
| `17275`–`17280`, `17282` | Funding profiles |
| `17276` | Equipment work orders |
| `ANNLV` | Annual leave |
| `SCKLV` | Sick leave |
| `FMSUS` | Family / medical leave |
| `HOLLD` | Holiday |
| `BRVUS` | Bereavement |
| `JURYL` | Jury duty |
| `MLVPA` / `MLVPB` | Military leave |

**Leave lines** always become: activity `003`, N, unit of measure `EH`, receiving unit = the home unit, program blank, and no phase, task order or route.

**Annual-plan programs** `D01AP`–`D10AP`: LDPR `17237`, no phase.

**Equipment work orders:** program `EQPWO`, LDPR `17276`, N, no phase, account `9017-27600`. The activity is the repair reason, and the route is the ED number.

**N/P:** `is_participating: true` is **P** (participating); `false` is **N**. In OASIS, activity and N/P print together as `382P`.

## 30. Troubleshooting

| Symptom | Likely cause | What to do |
|---|---|---|
| Every call is `401 Malformed API key.` | Whitespace or quotes around the key | Trim it; load it from a secret, not a pasted string |
| Calls work without act-as but `403` with it | That person isn't in DOT-12, or lacks rights | Section 9.4; check their role and orgs with the DOT-12 owner |
| Forms list is empty | The user (or service account) has no orgs | Ask for org access |
| A roster row you sent disappeared | An update sent the section without that row's `id` | Send sections complete, with ids (section 17) |
| New employee's hours were not saved | Charged by `temp_id` in an update | Two-step: save the row, then charge with the real id |
| Create fails with a server error | Missing `pay_period_start` / `pay_period_end` | Always send the pay period |
| Edits rejected after a while | Pay period closed (7 days after it ends) | Nothing to fix; final |
| `warnings` with `rule: "unverified"` | OM_WVDOT or TheHub was unreachable | Values were kept; validate again later |
| Accounting values change after save | Form rules are on and DOT-12 owns those fields | Use the returned form; don't fight it |
| Dates off by one day | Using UTC dates | Use Eastern-time calendar dates (`YYYY-MM-DD`) |

**Reporting a problem:** send the DOT-12 owner the time (Eastern), the endpoint, the HTTP status, the `error` text, the form id if any, and the e-number you sent. **Never include the API key.**
