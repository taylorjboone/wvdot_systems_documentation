# Integrating an app with the Identity Broker

A playbook for making an application a **relying party (RP)** of the identity
broker. The broker speaks standard **OpenID Connect (authorization code flow)**;
it authenticates users against the upstream Entra/SAML IdP and hands you signed
tokens. You never touch SAML — you speak OIDC to the broker.

This document is written for the **staging** deployment. For PROD, swap the host
and re-register a client; everything else is identical.

---

## 1. Broker coordinates

| Thing | Value (staging) |
|---|---|
| **Issuer** | `https://ocidev.transportation.wv.gov/auth` |
| **Discovery** | `https://ocidev.transportation.wv.gov/auth/.well-known/openid-configuration` |
| **JWKS** | `https://ocidev.transportation.wv.gov/auth/.well-known/jwks.json` |
| **Authorize** | `https://ocidev.transportation.wv.gov/auth/oauth/authorize` |
| **Token** | `https://ocidev.transportation.wv.gov/auth/oauth/token` |
| **UserInfo** | `https://ocidev.transportation.wv.gov/auth/oauth/userinfo` |

**Always drive your client library from the discovery URL** rather than
hard-coding endpoints — it returns everything above plus the supported
capabilities, and it's the single source of truth if anything moves.

Capabilities (from discovery, so you don't design against wrong assumptions):

- `response_types_supported`: **`code`** only
- `grant_types_supported`: **`authorization_code`** only — **no refresh tokens** (see §6)
- `id_token_signing_alg_values_supported`: **`RS256`**
- `scopes_supported`: `openid`, `profile`, `email`
- `token_endpoint_auth_methods_supported`: `client_secret_post`, `client_secret_basic`
- **No PKCE** — this is a *confidential* client; keep the secret server-side.

---

## 2. Register your client (one-time, broker-operator action)

Clients are registered via the broker's admin API (HTTP Basic with the broker's
`ADMIN_USER`/`ADMIN_PASS`, which live in the broker's `.env` — **the broker
operator runs this, not the RP app**). The plaintext secret is returned **once**;
store it immediately.

```bash
curl -s -u "$ADMIN_USER:$ADMIN_PASS" \
  -H 'Content-Type: application/json' \
  -X POST https://ocidev.transportation.wv.gov/auth/admin/clients \
  -d '{
        "name": "dot-dashboard",
        "allowed_redirect_uris": ["https://ocidev.transportation.wv.gov/dashboard/auth/callback"],
        "allowed_scopes": ["openid", "profile", "email"]
      }'
# -> {"client_id":"cl_...","client_secret":"<shown once>", ...}
```

Then configure your app with `client_id` + `client_secret` (as secrets, not in git).

**Critical: `redirect_uri` is matched by STRICT EQUALITY — no wildcards, no
trailing-slash fuzz.** The value you register must be byte-for-byte the callback
URL you send in the authorize request and exchange at the token endpoint. Pick
the final URL first (e.g. `https://ocidev.transportation.wv.gov/dashboard/auth/callback`).

To change a client's `allowed_redirect_uris`/`allowed_scopes`/`name`, or to
re-enable a disabled one: `PATCH /auth/admin/clients/{client_id}` with a JSON body
of just the fields to change (the secret and `client_id` are immutable). To retire
a client: `DELETE /auth/admin/clients/{client_id}` (soft-disable).

---

## 3. The flow

```
User hits a protected page (no app session)
      │
      ▼
App redirects to  /auth/oauth/authorize
      ?response_type=code
      &client_id=<your client_id>
      &redirect_uri=<your registered callback, exact>
      &scope=openid%20profile%20email
      &state=<random, CSRF>
      &nonce=<random, optional but recommended>
      │
      ▼
Broker runs the Entra/SAML login, then 302s back to:
   <redirect_uri>?code=<one-time>&state=<echoed>
      │
      ▼
App verifies `state`, then POSTs to  /auth/oauth/token
   grant_type=authorization_code
   code=<code>
   redirect_uri=<same exact value>
   client_id / client_secret   (form body OR HTTP Basic)
      │
      ▼
Broker returns JSON:
   { access_token, id_token, token_type:"Bearer", expires_in:900, scope }
      │
      ▼
App validates the id_token (§5), reads claims, and
ESTABLISHES ITS OWN SESSION (§6).
```

---

## 4. Flask integration (Authlib) — recommended

`dot_dashboard` is Flask, so [Authlib](https://docs.authlib.org/)'s OIDC client is
the least-error-prone path — it drives everything from discovery and validates the
ID token signature/claims for you.

```python
# pip install "authlib>=1.2" requests
from authlib.integrations.flask_client import OAuth

oauth = OAuth(app)
oauth.register(
    name="broker",
    server_metadata_url="https://ocidev.transportation.wv.gov/auth/.well-known/openid-configuration",
    client_id=os.environ["BROKER_CLIENT_ID"],
    client_secret=os.environ["BROKER_CLIENT_SECRET"],
    client_kwargs={"scope": "openid profile email"},
)

@app.route("/dashboard/login")
def login():
    # Authlib generates+stores state and nonce for you
    return oauth.broker.authorize_redirect(
        redirect_uri="https://ocidev.transportation.wv.gov/dashboard/auth/callback"
    )

@app.route("/dashboard/auth/callback")
def callback():
    token = oauth.broker.authorize_access_token()   # exchanges code, verifies id_token
    claims = token["userinfo"]                        # parsed + validated id_token claims
    # Establish THIS app's own login session — see §6
    session["user"] = claims["sub"]                   # employee ID; your stable user key
    session["name"] = claims.get("name")
    session["email"] = claims.get("email")
    return redirect(url_for("dashboard_home"))
```

If you integrate manually instead of with Authlib, you **must** do §5 yourself.

---

## 5. Validating the ID token (non-negotiable)

If your library doesn't do it automatically, verify the `id_token` (a JWT):

1. **Signature** — RS256, against the broker's **JWKS** (`.../auth/.well-known/jwks.json`), matching the token's `kid`.
2. **`iss`** == `https://ocidev.transportation.wv.gov/auth` (exact).
3. **`aud`** == your `client_id`.
4. **`exp`** not passed (and `iat` sane).
5. **`nonce`** == the nonce you sent, if you sent one.

Never trust an unvalidated token, and never skip signature verification "because
it's internal."

---

## 6. Sessions & lifetime — read this

- **There are no refresh tokens.** Access/ID tokens live **15 minutes** (`expires_in: 900`). Do **not** try to keep a user logged in by holding the broker's token.
- **After a successful callback, mint your OWN app session** (a normal Flask
  `session`) and manage its lifetime yourself. The broker's job ends at "here is a
  verified identity"; ongoing session management is the RP's job. When your session
  expires, send the user back through `/auth/oauth/login` — re-auth is fast if their
  Entra session is still alive (often no re-prompt).
- **Auth codes are single-use and expire in ~60s** — exchange immediately in the
  callback; don't stash a code to use later.

---

## 7. Claims you receive

| Claim | Meaning |
|---|---|
| `sub` | **The user's employee ID** (Windows account name) — unique, immutable. **This is your stable user key.** |
| `preferred_username` | Same value as `sub`. |
| `name` | Display name (from Entra). |
| `email` | Email (from Entra). |
| `iss`, `aud`, `exp`, `iat`, `nonce` | Standard; validate per §5. |

`GET /auth/oauth/userinfo` with `Authorization: Bearer <access_token>` returns the
same `sub`/`preferred_username`/`name`/`email` — but the claims are already in the
tokens, so you rarely need it.

### The broker's `users` table
The broker maintains a `users` table keyed on `windows_account_name` (= `sub`),
refreshed on every login. You may reference it (e.g. to FK your app's rows to the
employee ID), **but treat it as a reference cache, not authority**: the broker only
learns of a user when they log in, so it never reflects departures. **Authorization
decisions ("is this person allowed / still employed") must come from the live
login / your own data — never from that table.**

---

## 8. Same-host notes (staging specifics)

- The dashboard (`/dashboard`) and broker (`/auth`) share the host
  `ocidev.transportation.wv.gov`. OIDC redirects are same-site top-level
  navigations, so your app's session cookie can stay **`SameSite=Lax`** (the broker
  needs `None` only for the IdP's cross-site POST — that's the broker's problem, not
  yours).
- **No cookie collision:** the broker's session cookie was renamed to
  **`broker_session`** specifically so it won't clash with the dashboard's Flask
  `session` cookie. Keep using `session` for your app; they coexist.

---

## 9. Test checklist

1. Register a client with the exact callback URL; store `client_id`/`client_secret`.
2. Hit your `/login` → expect a redirect to Entra; complete login.
3. Land on your callback with `code` + `state`; confirm `state` matches.
4. Confirm the token exchange succeeds and the `id_token` **validates** (sig/iss/aud/exp).
5. Confirm `sub` is the employee ID and `name`/`email` are populated.
6. Confirm your app session is created and survives navigation.

## 10. Troubleshooting

- **`invalid_redirect_uri` / `unauthorized_client`** → the `redirect_uri` doesn't
  byte-match the registered one, or the client is unknown/disabled.
- **`invalid_client` at /token** → wrong `client_secret` or `client_id`.
- **`invalid_scope`** → you requested a scope outside the client's `allowed_scopes`.
- **Code exchange fails / "already consumed"** → code expired (60s) or reused;
  codes are single-use and bound to the `client_id` + `redirect_uri`.
- **Redirected back to the broker instead of Entra, or a destination error** →
  infrastructure (reverse-proxy) issue on the broker side, not your app; report it
  to the broker operator.
