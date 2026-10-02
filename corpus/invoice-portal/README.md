# Consultant Invoice Portal

A single intake point for WVDOT consultant invoices. Staff upload the invoice
package (FORM BF-2 Consultant Voucher on top, backup behind), the portal
extracts the BF-2, cross-checks the contract ID, runs the financial checks
(arithmetic, ceiling, sequence, multi-project splits, vendor compliance),
routes the invoice through a timestamped approval chain, and produces an
OASIS keying-assist screen. OASIS remains the financial source of truth.

This is the first demonstrable version: in-app upload (email ingestion
deferred) and seeded demo data. WVDOT staff sign in through the WVDOT identity
broker once a client is registered; consultant firms keep the account WVDOT
issued them.

## Layout

```
backend/    FastAPI + SQLAlchemy 2.0 + Alembic + PostgreSQL 16   (port 8000)
frontend/   Vite 7 + React 19 + TypeScript + Material UI 7        (port 5174)
*.md        Kickoff transcript, requirements, open questions, action items
```

## Run it

Prerequisites: Python 3.12, Node 20 (via nvm; `.nvmrc` is in `frontend/`),
PostgreSQL 16 running locally (`brew services start postgresql@16`) or
`docker compose up -d` for a container on port 5433.

```bash
./start-dev.sh            # creates the venv + DB (from backend/.env), migrates, starts both servers — no seeding
./start-dev.sh --import   # first wipe and re-import the real Engineering DB history (needs the SQL Server tunnel)
./start-dev.sh --demo     # first wipe and load the fictional demo seed instead
```

Then open http://localhost:5174 and sign in as
`invoice@wv.gov` / `hunter1` (override with `PORTAL_DEV_USER_EMAIL` / `PORTAL_DEV_USER_PASSWORD`).
  Vendor Portal: sign in as `mbi@wv.gov` / `hunter1` (the Michael Baker vendor account) to land in the consultant-facing half at `/vendor`.
API docs are at http://localhost:8000/api/docs.

### Single sign-on

WVDOT staff sign in through the **WVDOT identity broker** (OpenID Connect; see
`RELYING_PARTY_INTEGRATION.md` and the logic doc §14.2). The portal never touches
SAML — the broker does that against Entra and hands back signed tokens.

It is **off by default**, because registering a client is a broker-operator action
and the client secret is returned only once. Decide the callback URL first — the
broker matches `redirect_uri` by **strict byte equality**, with no wildcards and no
trailing-slash tolerance — then set:

```
PORTAL_OIDC_ENABLED=true
PORTAL_OIDC_CLIENT_ID=cl_...
PORTAL_OIDC_CLIENT_SECRET=...
PORTAL_OIDC_REDIRECT_URI=https://mmsdev.transportation.wv.gov/invoice-portal/api/auth/sso/callback
PORTAL_FRONTEND_BASE_URL=https://mmsdev.transportation.wv.gov/invoice-portal
# Optional:
PORTAL_OIDC_AUTO_PROVISION=false          # only accounts an admin set up may sign in
PORTAL_STAFF_PASSWORD_LOGIN_ENABLED=false # retire staff passwords once SSO is live
```

The two URLs the broker operator needs:

| | |
|---|---|
| **Register as the redirect URI** | `https://mmsdev.transportation.wv.gov/invoice-portal/api/auth/sso/callback` |
| Where the portal starts a login | `https://mmsdev.transportation.wv.gov/invoice-portal/api/auth/sso/login` |

Everything else — authorize, token and JWKS — is read from the broker's discovery
document, never hard-coded. The broker lives on a **different subdomain** from this
app; that costs nothing here (the portal uses a bearer token and a server-side
`sso_login_states` table, not cookies), but the app container **must** be able to
reach `ocidev.transportation.wv.gov` over HTTPS.

Consultant firms are unaffected by any of this: they have no state identity, so
`PORTAL_STAFF_PASSWORD_LOGIN_ENABLED=false` retires WVDOT staff passwords only.

### Claude-assisted extraction

The BF-2 grid is parsed locally with pdfplumber. When `PORTAL_ANTHROPIC_API_KEY`
(or `ANTHROPIC_API_KEY`) is set, Claude Sonnet classifies every page, finds the
contract identifiers wherever they appear (with the quoted evidence), normalizes
labor and direct-cost sheets, and suggests the invoice type; scanned BF-2s fall back
to a whole-PDF pass. Without a key the deterministic path runs alone and the wizard
asks for anything it could not read.

Agreement PDFs (the executed agreement and its supplementals) can be attached on the
agreement page. Their rate-schedule pages are usually scanned images, so Claude Opus
(`PORTAL_CLAUDE_MODEL_RATES`) reads them as a document in page chunks and stages the
contract term, caps and rate rows for review; nothing is used until someone imports it.
Invoices are then estimated against the imported schedule (or the provisional WVDOT default
rates under Config), and rate differences surface as warnings on the invoice.

## Develop

```bash
cd backend && source .venv/bin/activate && pytest -q          # backend tests
cd frontend && nvm use && npm run typecheck && npm run lint    # frontend checks
cd frontend && npm run test:run && npm run build
```

Backend settings are read from `backend/.env` with the `PORTAL_` prefix; see
`backend/.env.example`. The frontend proxies `/api` to the backend in dev.

## Deploy

The portal is deployed to the WVDOT `mmsdev` box the same way DOT-12 is: a per-app
directory (`~/invoice-portal`) with a `build.sh` that rebuilds one Docker image from
the repo and restarts the container behind Apache at
https://mmsdev.transportation.wv.gov/invoice-portal/. From a laptop:

```bash
deploy/deploy.sh            # build origin/main on the box
deploy/deploy.sh --local    # rsync this working tree instead
```

See `deploy/README.md` for the runbook.

## Provisional by design

The OASIS payment document type (GAX vs PRC) and its accounting columns, the
BF-2 unit codes used for routing, the invoice-type taxonomy, and the seeded
approval chains are placeholders pending the follow-up sessions listed in
`open-questions.md`.
