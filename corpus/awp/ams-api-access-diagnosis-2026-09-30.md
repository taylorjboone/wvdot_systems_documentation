# WVDOT AASHTOWare AMS API — Access Diagnosis

> Date: 2026-09-30 · Environment: `.env` in `~/Downloads/awp_test`

## Summary

Authentication succeeds at the token endpoint, but every OData route returns 401 or 412. Three findings, taken together, explain why.

## Findings

### 1. The instance name in `.env` is the web-UI hostname, not the API gateway's instance identifier

`AMS_INTEGRATION_NAME=wvdot-pr-prod` matches the Infotech-hosted web UI (`wvdot-pr-prod.infotechinc.com`), but the API gateway at `api.aashtoware.org/ams` only recognizes two URL segments:

| Instance segment | Gateway behavior |
|---|---|
| `wvdot` | Reaches the AMS backend (401 or 500) |
| `wvdot-test` | Reaches the AMS backend (401, 404, or 500) |
| `wvdot-pr-prod`, `wv`, `wvdot-prod`, `wvdot-pr`, `westvirginia`, `wvdotpr`, `wvdotprj`, … | 412 "instance not supported" at the gateway |

`wvdot-pr-prod` is the *customer subdomain* on Infotech's shared web hosting, not the AMS API instance code. The login doc was written from the web-UI name and Step 2 (the `GET /Contracts?$top=5` call) was never actually tested end-to-end.

### 2. The token endpoint doesn't validate `IntegrationName`

`POST /integration_authorization_token` returns 200 for *any* `IntegrationName` I send. It just base64-encodes `<whatever>:<secret>` and hands it back, where `<secret>` is a deterministic function of the subscription key + username + password.

Verified: minting with `IntegrationName=wvdot`, `wvdot-test`, `wvdot-pr-prod`, `wvdot-pr`, `wvdot-prod` all returned 200, each with the same `<secret>` part and only the prefix changed.

Consequence: the login doc's "Verified working 2026-09-30" only proves the credentials are valid at the auth API. It says nothing about whether they're authorized against the OData API.

### 3. Even a correctly-shaped token is rejected on `/wvdot/`

With a token minted against `IntegrationName=wvdot` (so the decoded token is `wvdot:<secret>`, matching the Basic-auth wire format of `base64(user:pass)`), sent as `Authorization: Basic <token>` to `/wvdot/Contracts?$top=5`, the response is:

```
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic
X-Powered-By: ASP.NET
```

The `WWW-Authenticate: Basic` header confirms the backend expects Basic auth and understood the request — it received our credentials and rejected them. So the subscription key and/or the user account are not provisioned for the OData product on the `wvdot` instance, even though they can mint tokens on the shared auth endpoint.

## What was also ruled out

- **The Infotech-hosted host is not an API surface.** `https://wvdot-pr-prod.infotechinc.com/` redirects to `/Account/LogOn` (form-based sign-in). Every API-style path — `/Api`, `/api`, `/odata`, `/api/odata`, `/Contracts`, `/$metadata`, `/ams`, `/ams/`, `/ams/Contracts`, `/ams/$metadata`, `/ams/odata`, `/ams/api` — returns the same 1668-byte IIS 404 page. No OData exists there.
- **Auth-scheme variants don't matter.** `Bearer <token>`, `Basic <raw base64 token>`, `Basic base64(username:token)`, and `Basic base64(username:decoded_secret)` all return the same 401 on `/wvdot/Contracts`.
- **OData version headers don't matter.** Adding `OData-Version: 4.0` and `OData-MaxVersion: 4.0` changes nothing.

## What to ask the AASHTOWare / Infotech admin

1. Is subscription key `f883a5…` provisioned for the **AMS OData product** on the `wvdot` instance, and not just the auth API?
2. Does `<your-aashtoware-email>` have an **API integration role** on the `wvdot` production AMS instance? The web UI signs in through the WVDOT identity broker; the OData API typically needs a separate technical/service account configured on the AMS side, distinct from the interactive SSO login.
3. Confirm the URL segment: `wvdot` (production) vs. `wvdot-test` (test) — the gateway only routes these two.

## After access is granted

Change `.env`:

```
AMS_INTEGRATION_NAME=wvdot
```

Then `first_call.py` in this folder should return 200 with a Contracts payload — no code changes needed. The auth flow implemented in `ams_auth.py` (PascalCase fields, raw-base64 token response, `Basic <token>` on subsequent calls) is already correct.
