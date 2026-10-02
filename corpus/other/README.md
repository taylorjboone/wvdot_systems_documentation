# Dock

**DOCK — Document Organization and Collaboration Keeper.**

## Run locally

```sh
./dev
```

Open **http://127.0.0.1:5174** and choose **Sign in with your WVDOT account**. Dock has no
password of its own, so `./dev` starts a development stand-in for the WVDOT identity broker on
**127.0.0.1:8099**: type an employee number at its form and you are that person. Use **pw1–pw10**
to reach the seeded demo accounts; `pw1` is the administrator and `pw10` the auditor. Any other
value creates a new account (see [Single sign-on](#single-sign-on)).

Vite and the Python/FastAPI backend run directly on your Mac with hot reload. Indexing runs in a background thread inside the backend. Postgres runs locally with its data in `.runtime/postgres`. **Docker is not needed for development.** The existing `.env`, Python environment, Node dependencies, and OCI credentials are configured here.

For background operation:

```sh
./dev start
./dev status
./dev stop
```

Logs: `.runtime/dev.log`. Ctrl+C stops a foreground `./dev`. The local database stays available between app restarts; `.venv/bin/python scripts/local_db.py stop` stops it too. `./dev` starts it again when needed.

Frontend: `127.0.0.1:5174`. API: `127.0.0.1:8081` ([API docs](http://127.0.0.1:8081/docs)). Database: `127.0.0.1:5546`. Use the explicit IPv4 address because another application listens on IPv6 `localhost:5174`.

## Single sign-on

Dock identifies people through the WVDOT identity broker over OpenID Connect. It holds no
password material: there is no password column, no password endpoint, and nothing to type or
store. The employee number the broker returns as the `sub` claim is the key a Dock account hangs
off; permissions stay entirely Dock's own.

> **Anyone who clears Entra becomes an administrator.** An employee number with no Dock account is
> provisioned as an **administrator**, on both the default and the mmsdev deployment. The
> population who can sign in is therefore the population who can authenticate against WVDOT Entra,
> and each of them arrives with full read, write and delete over every document, plus access
> control and the audit log. This is deliberate for the current pilot and was chosen knowingly;
> it is not a safe posture for a wider rollout. It is a
> setting rather than a constant, so tightening it is a configuration change: set
> `PW_OIDC_PROVISION_ROLE=` (empty, meaning access only through folders and groups), or
> `PW_OIDC_AUTO_PROVISION=false` to refuse anyone an administrator has not set up first.
> Narrowing it affects new arrivals only: a sign-in never rewrites an account's role, so accounts
> already created stay administrators until changed in **People & groups**. Administrators can
> prepare an account ahead of a first sign-in from **People & groups → Add person**, entering the
> employee number, and `authentication.provisioned` in the audit log shows who has been created.

### Registering a client

Registration is a broker-operator action, and the client secret is returned **once**. Decide the
callback URL first: the broker matches `redirect_uri` by strict equality — byte for byte, no
wildcards, no trailing-slash tolerance — and a mismatch consumes the authorization code, so each
attempt fails outright rather than being retryable.

For the mmsdev deployment the callback is
`https://mmsdev.transportation.wv.gov/dock/api/auth/sso/callback`, which is what Apache maps to
the API (see `infra/dock-apache.conf`).

```sh
curl -s -u "$ADMIN_USER:$ADMIN_PASS" -H 'Content-Type: application/json' \
  -X POST https://ocidev.transportation.wv.gov/auth/admin/clients \
  -d '{"name":"dock",
       "allowed_redirect_uris":["https://mmsdev.transportation.wv.gov/dock/api/auth/sso/callback"],
       "allowed_scopes":["openid","profile","email"]}'
```

Then configure the API. Keep the secret out of Git:

```sh
PW_OIDC_ENABLED=true
PW_OIDC_ISSUER=https://ocidev.transportation.wv.gov/auth
PW_OIDC_DISCOVERY_URL=https://ocidev.transportation.wv.gov/auth/.well-known/openid-configuration
PW_OIDC_CLIENT_ID=<from registration>
PW_OIDC_CLIENT_SECRET=<shown once at registration>
PW_OIDC_REDIRECT_URI=https://mmsdev.transportation.wv.gov/dock/api/auth/sso/callback
```

Single sign-on stays switched off until **all** of those are present, and the sign-in screen then
says so rather than offering a button that can only fail. The host also needs outbound HTTPS to
the broker for discovery, JWKS and the token exchange, with the broker's TLS chain trusted.

### Running the stand-in instead

`./dev` starts `scripts/fake_broker.py` automatically whenever `.env` does not configure a real
broker, and points the API at it. It serves real discovery, JWKS, authorize and token endpoints
and signs real RS256 tokens, so Dock's validation does actual work; only the sign-in page is
replaced by a one-field form. It is for a developer's machine and nowhere else.

## Use Dock

Everything lives in one **Directory**. Bridge A and Road B are ordinary folders.

- Folders and files share one directory table. Click a folder to open it; use the sidebar arrows to expand or collapse the tree.
- Drop files or whole folders into the current directory, onto a folder row, or onto a sidebar folder. **Upload → Upload files / Upload folder** also supports browsing from disk. Folder structure is preserved; folder drops include empty folders.
- The upload tray shows each item's progress and errors. **Retry failed** resumes failed items without duplicating successful uploads. Keep the tab open until uploads finish. Initial uploads use the comment “Initial upload”; choose **Upload with comment** for a custom check-in comment. Existing documents are never overwritten by directory imports.
- Editors can create inheriting subfolders with **New folder** or folder uploads. Folder rename/move/delete and permission management retain their controller/manager restrictions.
- Open the top-right account menu → **My profile** for appearance, folder access, and sign-out.
- **Folder settings → General** provides rename, move, and deletion of a complete folder tree. The confirmation shows affected folders, documents, and blocking checkouts. **Trash** lets managers browse retained contents and restore the tree, with an alternate name or destination when needed.
- **Folder settings → Permissions** or the dedicated permissions URL lets you assign group roles and individual exceptions. **Effective access** shows each person’s role, winning group/exception, and source folder. **People & groups** provides searchable user/group lists, account details, membership management, and explicit saves.
- Access inherits down the tree. The nearest folder with an applicable grant wins. At that folder, an individual exception takes precedence; otherwise the highest role from the person’s groups applies. Turn off **Inherit access from parent folder** to stop parent grants. Global administrator/auditor capabilities still apply.
- **Check out** a document, download and edit it locally, then **Check in** with a comment. **Versions** provides older downloads, text/metadata comparisons, and restoration as a new version.
- Search covers accessible folders, with optional folder scope, historical versions, and tag filters.
- Pages have real URLs: `/directory/:id`, `/directory/:id/permissions`, `/documents/:id/preview`, `/documents/:id/tags`, `/admin/users`, `/admin/groups`, `/trash`, `/tags`, `/search`, and `/profile`. Tabs, versions, comparisons and filters survive reload; breadcrumbs and browser Back/Forward preserve navigation.
- The document **Tags** tab shows automatic summaries and categorized labels from content, filenames, folder context and metadata. Add manual labels or remove inaccurate ones; regeneration preserves those corrections. Administrators can rename/merge labels and pause, resume, retry or backfill enrichment from **Tags & understanding**.
- The header theme button switches between the supplied light/dark design treatments. The product uses the supplied Dock wordmark and document/tray symbol.

Managers can change access within their management boundary. Moves require management rights over the moved subtree and destination; checked-out files block moves. Deleting a tree requires management rights throughout the subtree and no active checkouts. Trash preserves document IDs, versions, OCI references, grants, and logs; independently archived items remain archived when their parent tree is restored.

| Account | Access |
|---|---|
| pw1 | Global administrator |
| pw2 | Manager on Bridge A and Road B folders, including Restricted |
| pw3 | Document controller in both subtrees, including Restricted |
| pw4 / pw5 | Editor in Bridge A / Road B |
| pw6 | Editor only in Bridge A / Design / External |
| pw7 | Reviewer in Bridge A; can comment |
| pw8 / pw9 | Viewer in Bridge A / Road B |
| pw10 | Global auditor; metadata/logs, without file contents |

Restricted folders stop inheritance. Users see only accessible folders plus the ancestor path needed to reach them.

## Development

Edit `frontend/src/` for the React/TypeScript UI and `backend/pw_store/` for the Python API. Both reload during `./dev`. The database and OCI files persist across restarts; account seeding does not reset existing accounts or grants.

```sh
# Frontend compile and browser workflows
cd frontend
npm run build
npm run test:e2e
```

```sh
# Isolated native test database, never the application database
.venv/bin/python scripts/local_db.py --test
PW_RUN_INTEGRATION=1 .venv/bin/python -m pytest backend/tests -q
.venv/bin/python scripts/local_db.py --test stop
```

A fresh checkout needs Python 3.12+, Node 22+, and native Postgres 17 with [pgvector](https://github.com/pgvector/pgvector#installation). Create `.venv`, install `backend/requirements.lock` and the editable backend, copy `.env.example` to `.env`, configure your OCI profile, then run `scripts/configure_local.py`. `./dev` initializes its own database and installs frontend dependencies if needed. `PW_PG_BIN` can point to a Postgres 17 bin directory. The established `PW_` config prefix and `pw_store` database name remain stable.

Real private OCI buckets are in **AIDevelopment / us-ashburn-1**. Files remain in OCI; the 250 MB upload limit, immutable versions, permissions and audit logs remain enforced. No new cloud provisioning is needed to run this configured workspace.

## Reference

[Verification](docs/VERIFICATION.md) · [Adaptation/design provenance](docs/PROVENANCE.md) · [Optional maintenance operations](docs/OPERATIONS.md)

The original ProjectWise report, its Word lock file, report build scripts/styles/output, and research sources are preserved locally and excluded by `.gitignore`. Credentials, `.runtime`, caches and dependencies are excluded too. The committed fixtures are synthetic.

The former project-based schema was migrated into folder-only permissions without changing document IDs, versions, OCI keys, file pointers, checkouts or audit history. Historical audit project IDs remain only as immutable legacy context.

## Automatic document understanding

OCI Gemini 2.5 Flash supplies structured enrichment independently of FOIA. The native background worker queues analysis after extraction and when the file version, name, metadata or folder context changes. Documents remain downloadable while tags are pending or a provider fails. Large extracted bodies are processed in bounded sections; incomplete or unsupported extraction is labeled partial. Categories cover document type, discipline, location, organization, party, identifier and topic. Evidence quotes and validated page references accompany content tags.

`PW_TAGGING_ENABLED`, `PW_OCI_TAG_MODEL`, and `PW_OCI_TAG_MODEL_ID` control this feature. This workspace’s model and runtime permission are configured. For a new deployment using the generated OCI runtime group, `scripts/configure_tagging.py` installs a model-scoped chat policy using the administrator OCI profile and writes the model ID to the ignored local `.env`; it does not change bucket permissions. Restart `./dev` after configuration changes. Automatic tags and summaries are model outputs and remain editable through the catalog/document controls.

## Living application documentation

Open **Docs** in the sidebar for [Usage](http://127.0.0.1:5174/docs/usage), a high-level end-user guide. [Business logic](http://127.0.0.1:5174/docs/business-logic) is the separate in-depth reference covering frontend and backend behavior. [Frontend change log](http://127.0.0.1:5174/docs/frontend/change-log) and [Backend change log](http://127.0.0.1:5174/docs/backend/change-log) remain separate. The app renders the canonical Markdown in `frontend/src/docs/` directly, including tables, a table of contents and section links.

[AGENTS.md](AGENTS.md) requires updates to Usage, Business logic and both changelogs with every agentic code change, before completion and regardless of whether a commit was requested. `CLAUDE.md` imports the same policy.

## Windows client

The Windows 11 x64 client, Explorer integration and MSIX build instructions are in
[desktop/windows/README.md](desktop/windows/README.md). It uses the same folder/group
permissions and version APIs. See its acceptance record for Windows/Bentley checks
that still require actual Windows PCs.
