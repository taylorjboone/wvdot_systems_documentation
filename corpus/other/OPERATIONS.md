# Optional maintenance

Normal development uses `./dev`, with native Vite, FastAPI (including background indexing), and Postgres. No Docker services are required. These commands are occasional maintenance, not part of starting the app.

## Local services

- `./dev`: foreground, hot reload; Ctrl+C stops frontend/backend.
- `./dev start`, `./dev stop`, `./dev status`: background operation.
- `.runtime/dev.log`: app output.
- `.runtime/postgres`: isolated native database data, ignored by Git.
- `.venv/bin/python scripts/local_db.py stop`: stop the database; `./dev` starts it when needed.
- `.venv/bin/python scripts/local_db.py --test`: separate native test cluster on port 5547. Add `stop` to stop that test cluster only.

The live database runs on port 5546 and contains the copied original data. The Docker-to-native transition preserved 16 documents, 22 committed versions, 14 folder grants, 10 folders and 1,026 audit events; version, audit and current-pointer checksums matched before and after. The pre-copy archive is `.runtime/pre-native-move.dump`, with evidence in `.runtime/native-move-result.json`. Subsequent use adds documents/events normally. The old Docker volume was retained but is not used by local development.

The native pgvector 0.8.2 extension was compiled from the upstream tag for the already installed Homebrew Postgres 17. Its installation adds extension files, without modifying other applications' databases. Dock uses its own `.runtime/postgres` cluster.

## Backups and audit export

```sh
PW_PG_DUMP=/opt/homebrew/opt/postgresql@17/bin/pg_dump .venv/bin/pw-store backup
.venv/bin/pw-store export-audit
.venv/bin/pw-store reconcile
```

Backups and audit batches are created in `.runtime` and uploaded to the private operations bucket. Use a pg_dump executable matching Postgres 17. `reconcile` cleans only fenced, abandoned, unreferenced uploads older than 24 hours, rechecking references before deleting the precise OCI version. It does not delete committed file history.

Restore backups into a separate, empty `pw_store` database instance before choosing to replace any live data. Do not restore over the running development database. Original file bytes remain in OCI; recovered version references must be fetched using their recorded OCI version IDs and SHA-256 checksums.

## Credentials and permissions

The explicit workspace `.env` contains application-specific `PW_` settings. It is not committed. The native API uses the limited `pw_api` account and append-only audit writer; its background indexer uses the separate `pw_worker` pool. Migration/startup uses `pw_migrate`. These are database roles within one Postgres instance, not separate services.

Runtime OCI configuration is `.runtime/oci-runtime/config`; maintenance configuration is `.runtime/oci-maintenance/config`. Runtime credentials can create/read original and derived objects but cannot overwrite/delete originals or write operations backups. Maintenance credentials support cleanup/backup operations. The existing buckets and credentials are already configured, so starting Dock does not provision cloud resources.

For a fresh installation only, `pw-store provision` and `scripts/provision_oci_identities.py` can prepare the private buckets and restricted OCI identities using an authorized operator profile. Do not mount or expose operator credentials to the frontend.

## Indexing

The local backend starts its own indexing loop (`PW_EMBEDDED_WORKER=true` in `./dev`). No separate worker command is needed. A shutdown during processing leaves a leased job that becomes retryable; claim fencing prevents stale publication. The API's existing reindex action creates a new generation. Text and semantic availability remain independent.

## Single sign-on on mmsdev

**Deployed 2026-09-09** (image `dock:20260910T015414Z`). Migrations `0025` and `0026`
applied; 646 documents, 668 versions and 17,994 audit events carried through, and the
password column is gone. The pre-deployment dump is
`.runtime/deployment/before-sso.dump` with per-table counts beside it in
`before-sso-counts.txt`, and the build log is `sso-deploy.log`. `runtime.env` was
copied to `runtime.env.before-sso` before the identity-broker block was appended.

**The deployment provisions openly, by explicit instruction.**
`PW_OIDC_AUTO_PROVISION=true` and `PW_OIDC_PROVISION_ROLE=administrator`: anyone who
can authenticate against WVDOT Entra may sign in, and a first sign-in creates an
account with the administrator role — full read, write and delete over all 646
documents, plus access control and the audit log. Nothing narrower gates it, so the
population who can reach Dock is exactly the population who can reach Entra.

It was briefly deployed refusing unknown employee numbers; that was reversed on
request. To narrow it again, set `PW_OIDC_PROVISION_ROLE=` (access only through
folders and groups) or `PW_OIDC_AUTO_PROVISION=false` (only accounts an administrator
sets up), then rebuild — the container reads its environment at `docker run`, so a
restart alone will not pick it up. Accounts already created keep the role they were
given: sign-in never rewrites `global_role`, so narrowing the setting affects new
arrivals only, and existing administrators stay administrators until changed in
**People & groups**. Review `authentication.provisioned` in the audit log to see who
has been created.

Dock has no password of its own, so if the identity broker is misconfigured nobody
can sign in at all. Configure it before or with the build, not afterwards.

The broker client was registered on 2026-09-09 as `cl_7UE0M_OOAk3RGPA2`, with the
single callback `https://mmsdev.transportation.wv.gov/dock/api/auth/sso/callback`.
The broker matches that URL by strict equality: a trailing slash is refused, and a
mismatch consumes the authorization code before the comparison, so each attempt
fails outright rather than being retryable. The secret was returned once at
registration and exists only in the private deployment configuration.

Append the identity-broker block to `.runtime/deployment/runtime.env` on the server,
preserving mode 0600 and keeping it out of image layers as with every other secret
there. `PW_ORIGIN=https://mmsdev.transportation.wv.gov`, `PW_PUBLIC_BASE_PATH=/dock`
and `PW_COOKIE_SECURE=true` must all be set: the callback is built from the first
two, and the session cookie is useless over HTTPS without the third.

The container needs **outbound HTTPS to `ocidev.transportation.wv.gov`** for
discovery, the key set and the token exchange, with that host's TLS chain trusted
inside the image. Without it the only symptom is a failure at the first sign-in.
Confirm it from the server, not from a workstation:

```sh
.venv/bin/python scripts/check_sso.py                       # the deployment's own .env
.venv/bin/python scripts/check_sso.py --env <runtime.env>   # or a specific file
```

That preflight reads the configuration, fetches discovery and the key set, confirms
the broker accepts this client and callback, confirms a near-miss callback is
refused, and confirms the client id and secret authenticate — it sends a
deliberately invalid authorization code, so `invalid_grant` is the success case and
`invalid_client` means the credentials are wrong. It consumes nothing and exits
non-zero on the first failure, so it can gate a deployment.

### Accounts on the first deployment

Migrations `0025` and `0026` drop `auth.users.password_hash` and add the employee
number that replaces it. **Every account that already exists gets a null employee
number**, and nothing can sign in to an account without one. Decide which of these
applies before announcing the change:

- **Existing accounts matter.** Attach each one to its employee number from
  **People & groups → the account → Edit account**, which offers the field while the
  account has none. The account's groups, access lists and folder permissions then
  follow that person on their first sign-in. This is one way: moving an employee
  number between accounts would hand over everything the account can reach, so it is
  a deliberate database operation rather than an edit.
- **They do not.** Leave them. The copied `pw1`–`pw10` demo accounts are unreachable
  and each real person arrives as a new account.

A person with no Dock account is currently provisioned as an **administrator**, so a
fresh deployment has someone who can grant access at all. That is more than a first
sign-in should carry. Once a known administrator has signed in, narrow it —
`PW_OIDC_PROVISION_ROLE=` for access only through folders and groups, or
`PW_OIDC_AUTO_PROVISION=false` to refuse anyone not set up first — and restart the
API. Provisioning is recorded in the audit log as `authentication.provisioned`;
review it after the first day.

### Rollback

Sign-in is configuration, not code: unsetting `PW_OIDC_ENABLED` leaves the sign-in
screen saying single sign-on is not configured, which is honest but admits nobody,
because there is no password path to fall back to. A real rollback means restoring
the previous container **and** its database, since `0025` dropped the password
column. Keep the pre-deployment dump until sign-in has been confirmed on the server.

## mmsdev Docker deployment

The server checkout is `/home/ubuntu/dock`. Use `sudo ./build.sh` there to build
and deploy the current source. The root Dockerfile builds the `/dock/` frontend
and the Python API together. This is a server workflow; keep using native `./dev`
for local development.

Host Apache owns HTTPS and static delivery. `infra/dock-apache.conf` is included
inside the existing mmsdev HTTPS virtual host before its root proxy. The active
file on this host is `/etc/apache2/sites-enabled/mms.conf` (a regular file, not a
symlink to the older sites-available copy). Apache serves
`/var/www/dock/current`, falls back to Dock's index for client routes, and proxies
`/dock/api/` to `127.0.0.1:8087`. No additional web server runs in the container.
Always run `sudo apache2ctl configtest` before reloading Apache.

`build.sh` builds first, retains the former container as `dock-previous`, and checks
the new API/database health before publishing the matching frontend release. Failed
startup restores the previous container. Frontend releases remain under
`/var/www/dock/releases`. The API uses Docker's `unless-stopped` restart policy.
Do not delete the previous image/release until the replacement has been verified.

Since 2026-09-11 mmsdev indexes with `PW_EMBEDDED_WORKER=true` and
`PW_WORKER_CONCURRENCY=8`: eight loops inside the API container, each with up to four
database connections on the shared `instant-db` service and its own OCR and embedding
work. Lower the value in `runtime.env` and rebuild if the host or database strains;
the earlier files are kept as `runtime.env.before-worker-concurrency` and
`runtime.env.before-worker-8`.

The target database is the separate `pw_store` database in the local `instant-db`
PostgreSQL 16 service on port 5442. The service's existing Instant database and
bind-mounted data directory must be preserved. `infra/postgres.Dockerfile` builds
pgvector 0.8.2 against the same PostgreSQL 16 Alpine base. The explicit
`sudo bash infra/install-pgvector.sh` operation adds only extension files to the
running container; it requires operator authorization for the shared service.
It does not restart the database. Those files survive container restarts but must
be reinstalled after recreating `instant-db` from the stock image, before Dock
starts. Do not replace the shared database container as part of ordinary Dock builds.

Keep `pw_api`, `pw_worker`, `pw_audit`, `pw_maintenance` and the `pw_migrate` owner
separate. None needs superuser or BYPASSRLS privileges on the shared cluster.
Migration 0013 gives the owner explicit RLS access for its SECURITY DEFINER
functions; runtime startup rejects migration-role membership, including NOINHERIT
membership. Create `vector` and `pg_trgm` in the new database using its database
administrator before restoring the application-owned schema.

Private server configuration is in `.runtime/deployment/runtime.env`; the separate
`maintenance.env` also contains migration/maintenance connections. Build images
contain neither file. The API mounts only `.runtime/oci-runtime` read-only at
`/run/oci-runtime`; its files must be readable by container UID 10001. Maintenance
OCI credentials remain in `.runtime/oci-maintenance` and are mounted only for an
explicit maintenance command. Preserve mode 0600 on secret files and mode 0700
on private host directories. Never copy `.env` or `.runtime` into image layers.

For an initial copy, export a consistent local snapshot with pg_dump and capture
per-table row counts and checksums from that same snapshot. Restore into a new,
empty database only. PostgreSQL 17 exports require removing their unsupported
`SET transaction_timeout = 0` statement for PostgreSQL 16; omit extension entries
already created by the server administrator and restore with `SET ROLE pw_migrate`
so tables/functions keep the dedicated owner. Run checked migrations separately
before starting the API/worker, then compare all table checksums (allowing only
new migration-ledger rows). Run `ANALYZE` in `pw_store` after restore to populate
planner statistics. Validate runtime roles, OCI object versions/checksums,
login, downloads, previews, search, Docs links and browser reload through HTTPS.

The data copy retains the existing OCI originals, derived and operations buckets
and exact object/version references. After copying, local and server databases
evolve independently. Do not run object reconciliation against just one copy:
abandoned-upload cleanup must account for references in both databases. No cleanup
scheduler is installed. Account passwords and permissions are copied; no account
reset or seed command is part of deployment.

Migrations 0014–0015 change chunk/vector RLS to evaluate the existing per-document permission
function once per document/statement rather than for every chunk. No authorization
result is cached across requests. Targeted metadata/page lookups retain their
per-document checks. Extraction writes include the derived JSON digest
in the filename, so cross-platform OCR differences do not collide with the copied
generation’s existing OCI objects. Old references remain valid; original files are
unchanged. Retry only failed affected jobs after deploying that fix.

Deployment evidence is kept privately in `.runtime/deployment/`: the consistent
source archive and table fingerprints, database and OCI verification results,
Apache backup, and build/deploy logs. The initial copy matched all 27 data tables
exactly before workers started, with only the new migration-ledger entry differing.
Subsequent jobs, migrations and verification sessions naturally change operational
tables. Verification covered all 659 original references and 535 recorded derived
objects, sample SHA-256 downloads, and live HTTPS login, Docs, preview, semantic
search and authorization denials. Instant and dot12 continued serving throughout.
