# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

An identity broker that bridges SAML and OIDC: relying parties speak standard OAuth2/OIDC (authorization code flow) to this service, which authenticates users against an upstream SAML IdP (ADFS-style, keyed on `WindowsAccountName`) and mints RS256-signed JWTs. Built on FastAPI (ported from Flask in 2026-07 with byte-level response parity; see `KNOWN_QUIRKS.md` for post-cutover bug fixes and accepted divergences).

## Commands

```bash
# Run locally (dev server, port 8000)
python app.py                      # or: uvicorn app:app --port 8000

# Production-shape run
gunicorn -k uvicorn.workers.UvicornWorker -w 1 -b 0.0.0.0:8000 app:app

# Build + run in Docker (rebuilds image, restarts services)
./build.sh [--backend <branch>]

# Generate the JWT signing keypair (once per environment; refuses to overwrite)
python scripts/generate_jwt_keypair.py

# Parity harness (regression safety net; needs Flask installed and a main-branch
# worktree as the oracle, plus the throwaway Postgres from tests/parity/fixtures.py)
python tests/parity/golden_diff.py --oracle-dir <path-to-main-worktree>
python tests/parity/dump_routes.py   # route-table dump (run in each checkout)
```

There is no unit-test suite or linter; the parity harness in `tests/parity/` is the safety net.

Local setup: copy `env_template.txt` to `.env` (config.py loads `.env` via python-dotenv). The Docker build uses that same `.env` — docker-compose bind-mounts it read-only into the container at runtime, so config is **not** baked into the image (edit `.env` + restart to change it, no rebuild). The single `.env` also carries `GH_TOKEN` for the build-time clone (docker compose reads it; the app ignores it).

**Docker build quirk:** the Dockerfile does NOT copy local source. It `git clone`s the `BACKEND_BRANCH` branch from GitHub (using `GH_TOKEN` from `.env`), so local uncommitted changes never reach the container — push first, then build. `.env` is bind-mounted read-only into the container at runtime (not copied into the image); `certs/sp.{crt,key}` and `keys/jwt_*.pem` are still `COPY`'d into the image at build time from the build host.

## Architecture

The authentication flow spans three routers and is stitched together through the Starlette session cookie and the `auth_codes` table:

1. **`/oauth/authorize`** (`broker/blueprints/oauth/routes.py`) — validates client, redirect URI (strict equality against `clients.allowed_redirect_uris`, no wildcards), and scopes; stashes the pending request in `request.session['oauth_request']`; redirects to `/saml/login`.
2. **`/saml/login` → IdP → `/saml/acs`** (`broker/blueprints/saml/routes.py`) — python3-saml (OneLogin) drives the AuthnRequest/response. On success, ACS extracts `WindowsAccountName`/name/email, writes an `AuthCode` row (only the SHA-256 of the code is stored), and redirects back to the RP with `code` + `state`.
3. **`/oauth/token`** — verifies client secret (bcrypt), then claims the code with an atomic `UPDATE ... WHERE consumed_at IS NULL` (single-use guarantee), and mints access + ID tokens via `broker/utils/jwt_utils.py`.
4. **`/.well-known/openid-configuration`** and **`/.well-known/jwks.json`** (`broker/blueprints/discovery/`) — advertise endpoints and the RSA public key.

**`/admin/clients`** (basic auth via `ADMIN_USER`/`ADMIN_PASS`) registers OAuth clients; the plaintext client secret is returned once at creation and only its bcrypt hash is stored. DELETE disables (soft-delete), never removes; PATCH updates `name`/`allowed_redirect_uris`/`allowed_scopes`/`disabled` (setting `disabled:false` re-enables), never the secret or `client_id`.

Port-specific structure (the parts that differ from an ordinary FastAPI app):

- **Handlers are sync `def` on purpose** — psycopg2/python3-saml/requests are blocking; FastAPI runs them in a threadpool sized by the `THREADS` env var (default 8, set in the lifespan in `broker/__init__.py`) to match the old gunicorn `--threads`. Don't convert handlers to `async def` without making the whole call chain non-blocking.
- **No Pydantic request models** — request parsing is manual (`request.query_params`, `Depends(form_data)`) so malformed input yields the original OAuth-shaped 400s, never FastAPI's 422/`{"detail"}`. Async body parsing lives in `broker/deps.py`; `require_admin` raises `ApiError` (dependencies can't return responses).
- **`broker/http.py` is the Flask-compat wire layer**: `ApiJSONResponse` (sorted keys, compact separators, trailing newline), Werkzeug-style HTML error pages and redirect bodies, and `InternalErrorMiddleware` (answers unhandled 500s without killing the keep-alive connection, which FastAPI's default Exception handler would). All handlers return explicit responses; redirects are explicit 302 (Starlette's default 307 would replay the IdP's ACS POST against the RP).
- **Session** = stock Starlette `SessionMiddleware` (cookie name from `SESSION_COOKIE_NAME`, default `session`; 15-min max-age; `SameSite=None`+Secure in PROD/STAG so the IdP's cross-site ACS POST carries it, Lax in dev); its only content is the `oauth_request` stash between authorize and ACS.

Other structural points:

- `broker/__init__.py` holds the app factory; `broker/db.py` holds the engine/`SessionLocal`/`Base` and the `get_db` dependency (handlers commit explicitly; close rolls back). Config comes from the top-level `config.py` module, which reads `.env` — imported directly, no app.config.
- SAML settings are environment-selected in `config.py` (`ENVIRONMENT` = `PROD`/`STAG`/else-dev) from paired files in `saml/` (`settings*.json` + `advanced_settings*.json`); IdP details are merged at runtime from `IDP_METADATA_URL`. SP cert/key live in `saml/certs/` (git-ignored).
- Tokens are stateless JWTs — there is no token table and no revocation; only auth codes are persisted. name/email ride inside the access-token claims, so `userinfo` never touches the database.
- Schema is managed by `sql/init.sql` applied by hand to the shared Postgres (no migrations framework). Keep the SQLAlchemy models in `broker/model/` in sync with it.
- The JWT private key is cached with `@lru_cache` at first use; key rotation requires a restart and a new `JWT_KID`.
