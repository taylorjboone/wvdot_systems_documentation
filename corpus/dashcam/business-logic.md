# Dashcam Business Logic

> **This is the source of truth for how the three dashcam repos fit together.**
> If a change alters anything written here — a route or its guard, a page's API
> calls, a processing step, a status value, a threshold, an env var, or any
> assumption another repo relies on — update this file **in the same change**.
> Rendered in-app at **Admin → Business Logic** (`/dashcam/#/business-logic`).
> Source: `dashcam_frontend/dashcam/src/docs/business-logic.md`.
>
> This file ships inside the frontend JavaScript bundle. **Never put secrets
> here** — no passwords, PAR URLs, OCIDs, tokens or keys. Name the env var instead.

## How to keep this document current

The rule lives in every `CLAUDE.md` (root, frontend, backend, inference). In short:

| If you change… | Update this section |
|---|---|
| A route, its path, method, guard or response shape | [Backend route inventory](#backend-route-inventory), and [Frontend pages and their API calls](#frontend-pages-and-their-api-calls) if a page uses it |
| What a page calls, or a new page / nav entry | [Frontend pages and their API calls](#frontend-pages-and-their-api-calls) |
| Anything the worker does, sends, or expects | [Inference worker](#inference-worker) and [Processing pipeline](#processing-pipeline) |
| Auth, sessions, roles, permissions, feature flags | [Authentication and permissions](#authentication-and-permissions) |
| Queue, batch, upload-job, nightly or path logic | [Processing pipeline](#processing-pipeline) |
| Tables, invariants, buckets, env vars | [Data model and invariants](#data-model-and-invariants), [Object storage](#object-storage), [Environment variables](#environment-variables) |
| Something listed under core assumptions | [Core assumptions](#core-assumptions-cross-repo-contracts) — and every repo that depends on it |

Fix stale lines rather than appending contradictions, and add a line to
[Document history](#document-history).

## System at a glance

Three repos, one product. The **frontend** is a React SPA that the **backend**
serves as static files. The **backend** is a FastAPI app that owns Postgres, the
Redis work queue and worker scaling. The **inference** repo is a Python job that
runs on OCI Data Science: it pulls one video at a time from the backend, processes
it, and posts every result back over HTTP. Video bytes never pass through the backend.
The browser uploads straight to Object Storage and the worker reads from there.

```ascii
┌──────────────────────────────────┐           ┌──────────────────────────────────┐
│ Field crews · WVDOT staff        │           │ Azure AD / Entra ID  (SAML IdP)  │
│ Nextbase 622GW dashcams → *.MP4  │           │ WindowsAccountName → user id     │
│ browser → …/dashcam/#/           │           │ PROD + STAG only (DEV bypasses)  │
└──────────────────────────────────┘           └──────────────────────────────────┘
                  │                                              ▲
                  │                                              │ SSO · ACS · SLO
                  ▼                                              ▼
╔══════════════════════════════════╗           ╔══════════════════════════════════╗           ╔══════════════════════════════════╗
║ [1] dashcam_frontend             ║           ║ [2] dashcam_backend              ║           ║ [3] dashcam_inference            ║
║ React 19 · Vite · MUI · maps     ║           ║ FastAPI · gunicorn -w 1          ║           ║ OCI Data Science job run         ║
║ HashRouter → /dashcam/#/<page>   ║JSON+cookie║ /dashcam/* PROD·STAG · /* DEV    ║◄─ get-job ║ artifact/main.py · CPU or GPU    ║
╟──────────────────────────────────╢─ HTTPS ──►╟──────────────────────────────────╢─ video ──►╟──────────────────────────────────╢
║ Upload       pick·preview·PUT    ║           ║ auth/          SAML · cookie     ║           ║ 1 get-job       claim a video    ║
║ Path Viewer  paths·GPS·video     ║◄── JSON ──║ api/videos     frames · labels   ║◄─ upload_*║ 2 get_object    dashcam_videos   ║
║ Routes Map   coverage · tiles    ║           ║ api/paths      paths·GPS·MVT     ║ frames·gps║ 3 exiftool      GPS @ 10 Hz      ║
║ Label        review detections   ║           ║ api/routes_map route coverage    ║ lrs·detect║ 4 reject        no GPS / no move ║
║ Annotations  QA training labels  ║           ║ api/tags · admin · user          ║           ║ 5 geometryToMeasure → LRS        ║
║ Tags         paths·videos·images ║─ enqueue ►║ api/ds         ingest · queue    ║◄─complete─║ 6 min-distance frames → JPEG     ║
║ Processing   queue · batches     ║ add-files ║ api/embeddings SigLIP (admin)    ║           ║ 7 YOLO / RT-DETR / RF-DETR       ║
║ Admin        users · analytics · ║           ║ api/basemap    local mbtiles     ║◄─ webhook ║ 8 upload_*      rows → backend   ║
║              business logic      ║           ║                                  ║           ║ 9 complete-job  ok | failed      ║
║                                  ║           ║ WorkerManager  scale · batch     ║           ║                                  ║
║ state: App.tsx props +           ║           ║ APScheduler    nightly 01:00 ET  ║ network-  ║ idle 30 × 20 s polls → exit      ║
║        localStorage: db, filters ║           ║ guards         core/deps.py      ║ trust only║ sends NO backend credentials     ║
║                                  ║           ║                                  ║           ║                                  ║
╚══════════════════════════════════╝           ╚══════════════════════════════════╝           ╚══════════════════════════════════╝
          │                                            │                   │    │                                 ▲            │
          │                                            │                   │    │                                 │            │
          │                                            │ SQL               │    │    spawn job runs (ADS)         │ runs [3]   │
          │ direct PUT                                 │ db= bind          │    └───────────────────────┐         │            │
          │ via write                                  │                   │ queues                     │         │            │
          │ PAR URL                                    │                   │ locks                      │         │            │
          │                                            ▼                   ▼                            ▼         │            │
          │ never via                       ┌────────────────────┐  ┌──────────────┐    ┌────────────────────────────────┐     │
          │ the backend                     │ PostgreSQL         │  │ Redis        │    │ OCI Data Science               │     │
          │                                 │ PostGIS · pgvector │  │ REDIS_URL    │    │ OCI_JOB_ID · OCI_GPU_JOB_ID    │     │
          │                                 ├────────────────────┤  ├──────────────┤    ├────────────────────────────────┤     │
          │                                 │ prod · dev_* binds │  │ CPU queue    │    │ conda env + artifact zip       │     │
          │                                 │ route_new (LRS)    │  │ GPU queue    │    │ env  WVDOT_URL NAMESPACE       │     │
          │                                 │ MVs + MVT funcs    │  │ batch ids    │    │      BUCKET_* ENVIRONMENT      │     │
          │                                 │ job_run            │  │ locks        │    │ args -db -m -mt [-i --gpu]     │     │
          │                                 │ site_settings      │  │ pollers      │    │ CPU: -lrs  (GPU: -i)           │     │
          │                                 └────────────────────┘  └──────────────┘    └────────────────────────────────┘     │
          │                                                                              get video · put frames · get weights  │
          ▼                                                                                                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ OCI Object Storage   (namespace $NAMESPACE · us-ashburn-1)                                                                     │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ dashcam_videos    raw uploads, object = file name    dashcam_frames         <stem>_Frame_NNNN.jpg     dashcam_models  weights  │
│ dashcam_annotated_images  copied on label save       dashcam_invalid_files  rejects (prod db)         taylor-frontend-test DEV │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Reading the map**

1. Staff sign in. In PROD/STAG that is SAML against Entra ID. In DEV the backend fakes a session (see [Sign-in paths](#sign-in-paths)).
2. The frontend is built into `dashcam_backend/dashcam/` and served by the backend at `/dashcam/`. Routing is hash-based, so every page URL is `/dashcam/#/<page>`.
3. Uploads go **browser → Object Storage** through a write PAR URL that the backend hands out. The backend then records the video and enqueues it.
4. `WorkerManager` inside the backend watches the Redis queue and starts OCI Data Science job runs. Each run executes `dashcam_inference/artifact/main.py`.
5. The worker claims videos with `get-job`, reads the MP4 from `dashcam_videos`, and writes frame JPEGs to `dashcam_frames`. Every row it produces goes to the backend as JSON (`upload_*`, `complete-job`).
6. When the queue has been idle for 5 minutes, the backend closes the batch: it builds paths, saves the batch history and finishes the upload job. A nightly job then does tracking and refreshes the materialized views.

## Environments and deployment

| | DEV | STAG | PROD |
|---|---|---|---|
| `ENVIRONMENT` | `DEV` | `STAG` | `PROD` |
| Backend URL prefix | none (`/api/…`, `/auth/…`) | `/dashcam/…` | `/dashcam/…` |
| Public host | `localhost:5173` (Vite) → `127.0.0.1:5000` | `visdev.transportation.wv.gov/dashcam` | `vision.transportation.wv.gov/dashcam` |
| Sign-in | DEV bypass + demo login | SAML (Entra) | SAML (Entra) |
| Backend OCI auth | `~/.oci/config` | Instance principals | Instance principals |
| Worker OCI auth | `~/.oci/config` | Resource principal | Resource principal |
| Upload bucket (frontend) | `taylor-frontend-test` | `taylor-frontend-test` | `dashcam_videos` |

- **`create_app()` refuses to start** unless `ENVIRONMENT` is exactly `DEV`, `STAG` or `PROD`, and it also needs `FLASK_SECRET_KEY`. This is deliberate: any other value would be treated as dev.
- The **Vite dev proxy strips `/dashcam`**, so the frontend always calls `/dashcam/api/...` and DEV backends see `/api/...`. In PROD/STAG, Apache passes `/dashcam` through.
- The frontend picks its upload bucket from the **hostname**, not from `ENVIRONMENT`. Only `vision.transportation.wv.gov` targets `dashcam_videos`.
- **Production process:** `gunicorn -w 1 -k uvicorn.workers.UvicornWorker --max-requests 1000`. It must stay a **single worker** because `WorkerManager`, its threads and the in-memory fallback queue are per-process. The Docker health check hits `GET /dashcam/auth/metadata`.
- **Build:** `npm run build` in the frontend writes to `../../dashcam_backend/dashcam/` (base `/dashcam/`).
- **Inference artifact:** `build_artifact.sh <prod|staging>` zips `artifact/` together with `default_env.txt` (as `.env`) and `version.txt` (`<git sha>_<timestamp>`), then uploads it to the `artifactsb` bucket. The job's `artifact.config` names the conda environment and the entrypoint `artifact/main.py`.

## Authentication and permissions

### Sessions

- The session is Starlette `SessionMiddleware` with cookie name `session`, signed with `FLASK_SECRET_KEY`. It is **signed, not encrypted**, so the session dict can be read client-side.
  - Cookie settings: `same_site=lax`, `https_only=False` (TLS ends at Apache), and no `max_age`, so it is a browser-session cookie.
- **Session keys:** `user` (the e-number, e.g. `E025205`), `name`, `email`, `avatar_color`, `permissions` (cached at login), plus the SAML name-id/session-index keys.
- The frontend treats **any non-empty object** from `GET /auth/session` as logged in. The same call also backfills `name`, `email` and `avatar_color` from the `users` table.
- Rotating `FLASK_SECRET_KEY` invalidates every session.

### Sign-in paths

| Path | Environments | What it does |
|---|---|---|
| SAML — `GET/POST /auth/?sso · ?acs · ?slo · ?sls` | STAG, PROD | Azure AD / Entra. On ACS, `user` = `WindowsAccountName` claim, `name` = `Name` claim, `email` = `emailaddress` claim. It then runs `create_or_update_user()`, which gives new users the `default` role and caches their permissions in the session. `return_to` must be the same host or a relative path. IdP metadata is fetched from Microsoft on every call. |
| DEV bypass — `GET /auth/` | DEV only | Skips SAML, sets `session.user = $USER` and redirects to `http://localhost:5173`. |
| Demo login — `POST /auth/auth {user, password}` | DEV only | The route is **only registered when `ENVIRONMENT=DEV`**, so PROD/STAG return 404. The password comes from `DEMO_LOGIN_PASSWORD`. The username is upper-cased and anything from `@` on is removed. It clears the session before setting `user`. The frontend `Login` page uses it. |
| Logout — `GET /auth/logout` | all | Clears the session. The frontend then redirects to `/dashcam`. |

### Roles and permissions

- **Permissions** are the four boolean columns on `role`: `view`, `upload`, `label`, `delete`.
- A user's effective permissions are the **OR across all of their roles** (`user_role` join).

| Role (seeded) | view | upload | label | delete |
|---|:-:|:-:|:-:|:-:|
| `default` (auto-assigned on first login) | ✓ | ✓ | | |
| `label` | ✓ | ✓ | ✓ | |
| `admin` | ✓ | ✓ | ✓ | ✓ |

- **Admin is a role, not a permission.** Every admin check is `roles.includes('admin')`.
- **Roles are per database.** The frontend re-fetches `/api/admin/users/current/permissions?db=` whenever the database selector changes.
- **Server-side enforcement** covers only `upload`, `delete` and role `admin`. The `label` and `view` permissions only gate things in the UI.
- **Feature flags** live in `site_settings`: `admin_only_mode`, `routes_map_enabled`, `collection_map_enabled`, `path_view_video`, `flagship_model`.
  - `admin_only_mode` is enforced **only in the frontend**, which sends non-admins to `https://vision.transportation.wv.gov/`.

### Backend guards

Defined in `dashcam_backend/dashcam/core/deps.py`.


| Guard | Rule | Failure |
|---|---|---|
| `require_role('admin')` | `session.user` is set, the user exists in the **default DB**, and the user has the role | 401 / 404 / 403 → `{success:false, error}` |
| `require_permissions(upload=True)` etc. | `session.user` is set, the user exists, and `user.has_permission(name)` is true for each requested permission | 401 / 404 / 403 |
| `require_permissions()` | Logged in only | 401 |
| Session check (inline) | The handler reads `session['user']` itself | 401 |
| `_check_admin_in_selected_db` | Admin in the **request-selected** DB (site-setting PUTs only) | 403 |

`get_db_session*` is not auth. It picks the database bind from, in order: the `db` header, then `?db=`, then the JSON body key `db`, then the form field. **Unknown keys silently fall back to the default DB.**

### Frontend gating

- `ProtectedRoute` shows **Access Denied** unless `userPermissions[requiredPermission]` is true or `userRoles` includes `requiredRole`.
- Routes whose feature flag is off (`/map`, `/collection`) are simply not registered. Admins always get them.
- The nav hides links the user can't use. Delete buttons are hidden unless the user has `permissions.delete`.
- **The UI is not a security boundary.** Every rule that matters must also exist server-side.

### Worker trust model

The inference worker sends **no credentials**: no header, token, API key or cookie. Its `clientId` is a random 8-character id, not a secret. Every `api/ds/*` endpoint the worker calls is therefore open, and relies on network position only. The `oci-webhook` signature check exists in code but is never called. See [Known gaps and risks](#known-gaps-and-risks).

## Processing pipeline

```ascii
┌──────────┐                       ┌─────────┐               ┌─────────────┐              ┌───────────┐            ┌────────────────┐
│ frontend │                       │ backend │               │ Redis queue │              │ inference │            │ object storage │
└──────────┘                       └─────────┘               └─────────────┘              └───────────┘            └────────────────┘
      │                                 │                           │                           │                           │
══╡ UPLOAD  ·  browser → bucket, backend records it ╞═══════════════╪═══════════════════════════╪═══════════════════════════╪═══════════════
      │                                 │                           │                           │                           │
      ●── GET par_urls ────────────────►│                           │                           │                           │
      ●── POST start-upload-job ───────►│                           │                           │                           │
      │                                 │ upload_job = uploading    │                           │                           │
      ●── PUT <name>.MP4  (write PAR, one file at a time) ──────────┼───────────────────────────┼──────────────────────────►│
      ●── POST upload_video_data ──────►│                           │                           │                           │
      │                                 │ video row + tags          │                           │                           │
      │                                 ●── enqueue CPU ───────────►│                           │                           │
      ●── POST add-files {files,db} ───►│                           │                           │                           │
      │                                 ●── enqueue (dedupe) ──────►│                           │                           │
      ●── PUT complete-upload ─────────►│                           │                           │                           │
      │                                 │ upload_job = processing   │                           │                           │
      │                                 │                           │                           │                           │
══╡ SCALE  ·  WorkerManager every AUTOSCALE_INTERVAL_REAL ╞═════════╪═══════════════════════════╪═══════════════════════════╪═══════════════
      │                                 │                           │                           │                           │
      │                                 │ q = queued videos         │                           │                           │
      │                                 │ ideal = ceil(q ÷ (S/P))   │                           │                           │
      │                                 │ spawn ideal − running     │                           │                           │
      │                                 │ ≤ MAX_WORKERS → OCI job   │                           │                           │
      │                                 │                           │                           │                           │
══╡ PER VIDEO  ·  worker loop ╞═════════╪═══════════════════════════╪═══════════════════════════╪═══════════════════════════╪═══════════════
      │                                 │                           │                           │                           │
      │                                 │◄─ GET get-job?clientId= ──┼───────────────────────────●                           │
      │                                 ●── RPOPLPUSH → pending ───►│                           │                           │
      │                                 ●·· {video_name} ···········┼··························►│                           │
      │                                 │                           │                           ●── get_object video ──────►│
      │                                 │◄─ create_frames · upload_video_metadata ──────────────●                           │
      │                                 │◄─ upload_gps_metadata ────┼───────────────────────────●                           │
      │                                 │◄─ geometryToMeasure (tolerance 20 m) ─────────────────●                           │
      │                                 │◄─ upload_lrs_video_segments ──────────────────────────●                           │
      │                                 │                           │                           ●── put frames ────────────►│
      │                                 │◄─ add_image_names_to_frames ──────────────────────────●                           │
      │                                 │◄─ upload_detections ──────┼───────────────────────────●                           │
      │                                 │◄─ POST complete-job {status} ─────────────────────────●                           │
      │                                 ●── completed | failed ────►│                           │                           │
      │                                 │                           │                           │ no GPS / no motion →      │
      │                                 │                           │                           │ invalidate_video; prod    │
      │                                 │                           │                           │ moves the file to         │
      │                                 │                           │                           │ dashcam_invalid_files     │
      │                                 │                           │                           │                           │
══╡ CLOSE  ·  queue idle for 300 s ╞════╪═══════════════════════════╪═══════════════════════════╪═══════════════════════════╪═══════════════
      │                                 │                           │                           │                           │
      │                                 │ assign videos → paths     │                           │                           │
      │                                 │ batch history → flushed   │                           │                           │
      │                                 │ upload_job → completed    │                           │                           │
      │                                 │ queue reset               │                           │                           │
      │                                 │                           │                           │                           │
══╡ NIGHTLY  ·  01:00 US/Eastern, detached subprocess ╞═════════════╪═══════════════════════════╪═══════════════════════════╪═══════════════
      │                                 │                           │                           │                           │
      │                                 │ 1 requeue unprocessed     │                           │                           │
      │                                 │ 2 track detections        │                           │                           │
      │                                 │ 3 detection_tracks MV     │                           │                           │
      │                                 │ 4 detection index         │                           │                           │
      │                                 │ 5 road views              │                           │                           │
      │                                 │ 6 route geometry          │                           │                           │
      │                                 │ 7 video summary           │                           │                           │
      │                                 │ 8 prune job_run           │                           │                           │
      │                                 │                           │                           │                           │
```

### 1 · Upload (frontend `UploadV2`)

1. **Filename rule:** `^YYMMDD_HHMMSS_<n>_<CAM>.MP4$` (the Nextbase naming). Names that don't match are rejected in the browser.
2. **Duplicate check:** the page lists the upload bucket and `dashcam_invalid_files` through their PARs and skips any name that already exists in either.
3. **Browser preview:** runs 3 files at a time. It reads duration and resolution from a `<video>` element, grabs one preview frame, and builds a 10-frame hover GIF (gif.js). **No MD5 and no GPS parsing happen in the browser.**
4. `POST /api/ds/start-upload-job {file_count}` creates `upload_job` with status `uploading`. If this fails, the upload still continues.
5. **Per file, one at a time:**
   - `PUT <writePAR><file name>`. This is the whole file in one request, and the object name is the bare file name.
   - `POST /api/videos/upload_video_data {video_data:{user_id, video_name, tag_ids}, db}`. This inserts the `video` row, adds `video_tag` rows, and **immediately enqueues** the video on the CPU queue.
6. `POST /api/ds/add-files {files, db}` enqueues the batch again, this time with the user id. Duplicates are dropped because the Redis queue ignores names that already have a status key.
7. `PUT /api/ds/complete-upload` records `batch_id` and the duration, and moves `upload_job` to `processing`. The page then redirects to `#/batch-history/<batch_id>`.
8. Leaving the page is blocked while an upload is running.

### 2 · Queue and workers (backend `WorkerManager`)

- **Queue:** Redis when `REDIS_URL` connects; otherwise an in-memory queue that only works with a single worker.

| Queue | List keys | Per-file status key |
|---|---|---|
| CPU | `dashcam:video_queue`, `dashcam:pending_queue` | `dashcam:file:<name>` |
| GPU | `dashcam:gpu_video_queue`, `dashcam:gpu_pending_queue` | `dashcam:gpu_file:<name>` |

- **File status:** `queued` → `pending` (claimed by `get-job` through an atomic `RPOPLPUSH`) → `completed` | `failed` (set by `complete-job`, which only accepts a file that is currently `pending`).
- **Timeouts:** a pending file older than **600 s is auto-failed**, and this check runs first. The 1800 s "stall → requeue" branch therefore effectively never fires.
- **Autoscaling** runs every `AUTOSCALE_INTERVAL_REAL` seconds:
  - `videos_per_job = S / P`, where S = `WORKER_STARTUP_TIME_SIM` in minutes and P = `TARGET_AVG_DURATION_SIM` in minutes
  - `ideal = ⌈queued ÷ videos_per_job⌉`
  - spawn `ideal − running`, capped at `MAX_WORKERS`
  - spawns are serialized by the `dashcam:spawn_lock` Redis lock
- **Spawn modes:**
  - **OCI Data Science** (`USE_OCI_DATASCIENCE=TRUE`): ADS `Job.run()` on `OCI_JOB_ID` with `JOB_ARGS`. It passes `WVDOT_URL`, `NAMESPACE`, `BUCKET_*`, `ENVIRONMENT`, `PAR_URL_LOGS`, `CONDA_ENV_OBJECT_NAME` and `ARTIFACT_OBJECT` as env vars, and translates the overrides `WORKER_DB`, `WORKER_MODEL` and `WORKER_MODEL_TYPE` into `-db`, `-m` and `-mt`.
  - **Local:** Popens `dashcam_inference/artifact/main.py -lrs --dry`, adding `--dummy` when `WORKER_DUMMY_MODE=true`.
- **GPU jobs:** `add-files` with `job_type='gpu'` requires a model. The overrides go into `dashcam:gpu_env_overrides`, and one GPU worker (`OCI_GPU_JOB_ID`, args `-i … --gpu`) is spawned if none is running. The GPU queue is separate from the CPU queue.
- **Leaky-worker discovery:** at startup in OCI mode, the backend re-registers job runs that are still ACCEPTED or IN_PROGRESS.
- **Admin controls:** `cancel-batch`, `cancel-oci-workers`, `delete-batches` (`require_role('admin')`), and `spawn-workers` (upload permission).

### 3 · Per video (inference worker)

| # | Step | Flag | Backend call | Writes |
|---|---|---|---|---|
| 0 | Claim | server mode | `GET api/ds/get-job?clientId=&gpu=` → `{video_name}` | Redis: pending |
| 1 | Load | always | — (`get_object` on `dashcam_videos`) | temp `.mp4` |
| 2 | Info | always | — | fps, frame count, resolution (cv2) |
| 3 | Metadata | always | — | exiftool `-ee3 -n -G1 -a -s`; GPS from Track3 at 10 Hz |
| 4 | Frames | `-cf` | `POST create_frames {video_name, frame_count, db}` | `frame` rows 1…N; `video_processing_steps.create_frames` |
| 5 | Video metadata | `-v` | `POST upload_video_metadata` | `video_metadata` |
| 6 | GPS | `-e` | `POST upload_gps_metadata` | `gps_metadata` + frame links; step `extract_gps_metadata` |
| 7 | LRS | `-lrs` | `POST geometryToMeasure {locations, tolerance:20}`, then `POST upload_lrs_video_segments` | route/measure on GPS rows, `lrs_video_segment`; step `lrs` |
| 8 | Frame images | `-u` | `PUT` JPEGs to `dashcam_frames`, then `POST add_image_names_to_frames` | `image` rows linked to frames; step `frames_upload` |
| 9 | Inference | `-i` | `PUT` JPEGs, then `POST add_image_names_to_frames` and `POST upload_detections` | `detection` rows; step `inference` |
| 10 | Done | always | `POST complete-job {video_name, status, clientId, elapsed_time, logs, gpu}` | Redis: completed / failed; batch counters |

- **CPU runs** use `-lrs` by default. **GPU runs** use `-i` with a model.
- **Progress** is reported as `POST api/ds/oci-webhook` log events after each step. There is no separate heartbeat.
- **Success contract** for every call: HTTP 200 **and** a JSON body with `status: true`. Anything else stops the remaining steps for that video.
- **Rejections** (`InvalidVideoError`) happen when there is no GPS at all, or every `GPSSpeed < 1`.
  - Against `-db prod` the file is **moved** from `dashcam_videos` to `dashcam_invalid_files`.
  - `POST invalidate_video` then moves the row to `invalid_video` and deletes the `video` row.
  - The fps/resolution check exists in code but is commented out.
- **LRS matching** (`RoadSwitcher`):
  - 3 s confirmation window at 10 Hz, 20 m maximum distance to a route, hysteresis between routes
  - a segment is written wherever the route changes; zero-length segments are dropped
- **Frame sampling** is by **distance, not time**. Measures are snapped to 0.003-unit increments and the closest GPS row per `(route, increment, direction)` is flagged `is_minimum_distance`. Those rows' start frames are the ones extracted.
- **Idle exit:** 30 empty `get-job` polls, 20 s apart (about 10 minutes), then the process exits 0.

### 4 · Batch close

- **Batch creation:** a `processing_batch` (uuid, `environment`, `is_gpu`, status `active`) is created on demand the first time something is enqueued. Its pointer is `dashcam:cpu_batch_id:<ENV>` (or the GPU equivalent) in Redis, and counters live under `dashcam:batch:<id>:*`.
- **Auto-flush:** when a queue has had `queued + pending == 0` for **300 s**, the backend runs the closing sequence:
  1. **CPU batches only:** `assign_all_videos_to_paths()`
  2. `_save_batch_history`: stats plus de-duplicated `processing_file_result` rows, status `flushed` (or `cancelled`)
  3. `_populate_upload_job`: `files_succeeded/failed`, `error_summary`, `paths_generated`, `email_text`, status `completed`
  4. queue reset

**Status vocabularies** (the frontend matches these strings exactly):

```ascii
processing_batch   active ──► flushed                      (admin: ──► cancelled)
upload_job         uploading ──► processing ──► completed   (failed: declared, never set)
queue file         queued ──► pending ──► completed | failed
job_run            running ──► succeeded | failed | skipped
```

- **Email is a stub.** The text is built and stored, but `email_sent` is never set.

### 5 · Paths

- A **path** is one user's continuous drive: consecutive videos from the **same user** with **≤ 5 s** between them.
- **Incremental assignment** (`assign_video_to_path`) runs under advisory lock `8675309`. It appends to a neighbouring path, merges the left and right paths (the left one survives, and the right one's videos, GPS rows and tags move over), or creates a new path. It then renumbers `segment_id` (0-based order within the path) and recomputes `distance_traveled` / `time_elapsed`.
- **Bulk assignment** walks unpathed videos that have `is_minimum_distance` GPS rows, in time order, then refreshes `lrs_path_segment_mv`. That view merges same-route, same-direction LRS segments with gaps of ≤ 20 s and drops runs ≤ 0.003 mi.

### 6 · Nightly pipeline (01:00 US/Eastern)

APScheduler job `nightly_pipeline` runs with `max_instances=1`, `coalesce=True` and a 1-hour misfire grace. It launches a **detached subprocess** (`python -m dashcam.utils.nightly_runner`), so gunicorn's `--max-requests` recycling can't kill it mid-run. That protection was added after the staging incident on 2026-08-25.

- **Lock:** `dashcam:nightly_pipeline_lock` (6 h).
- **Bookkeeping:** every step writes a row to `job_run`.
- **Target DB:** `JOB_TARGET_DB`, which defaults to **`dev_bennett`**. Set it explicitly in every deployed environment.

| # | Step | Needs |
|---|---|---|
| 1 | `requeue_unprocessed_videos`: videos with no `video_processing_steps` row, or `lrs IS NULL` | — |
| 2 | `track_untracked_detections`: model `042226.pth`, classes 0 pothole / 1 sign, conf ≥ 0.4, ≤ 1000 videos | — |
| 3 | `refresh_detection_tracks` (MV) | 2 |
| 4 | `refresh_detection_index` | 2 |
| 5 | `refresh_road_views`: `road_traversal_summary`, then `road_collection_stats` | — |
| 6 | `refresh_captured_route_geometry` | — |
| 7 | `refresh_video_detection_summary` | — |
| 8 | `prune_job_runs` (> 1 year) | — |

A step is only **skipped** when a step it needs didn't succeed. Every other step still runs.

### 7 · Detection tracking

- **Online:** YOLO / RT-DETR runs use Ultralytics ByteTrack and send `track_id`. RF-DETR sends none.
- **Nightly:** step 2 of the nightly pipeline re-tracks whole videos with `DashcamTracker`. `track_id` is scoped to `(video, class_id, model)` and starts at 1 for each video.
- **A video is always tracked as a whole.** Partial re-tracking would collide ids.

## Inference worker

`dashcam_inference/artifact/main.py`. The code runs on OCI Data Science in a
published conda environment (Python 3.10, PyTorch, Ultralytics, rfdetr).

### Launch modes

| Mode | Trigger | Behaviour |
|---|---|---|
| Server | no positional file names | Loops on `get-job`; exits after about 10 minutes idle |
| Direct | positional file names | Processes exactly those. Note: the default `JOB_ARGS` `--dry -lrs x` makes `x` a file name. |
| Dummy | `--dummy` | Sleeps `dummy_sleep ± 50%`, then posts `complete-job` with status true. Used to exercise the queue. |
| Dry run | `-d/--dry-run` | Skips object-storage writes and most DB posts. It **still** claims a job, calls `geometryToMeasure`, sends webhooks and posts `complete-job`. |

### CLI flags

| Flag | Default | Meaning |
|---|---|---|
| `-cf` `-v` `-e` `-lrs` `-u` `-i` | off | Enable pipeline steps 4–9 (see table above) |
| `-c/--use-cache` | off | Read/write videos in `VIDEO_CACHE` |
| `-db` | `prod` | One of `prod`, `dev_bennett`, `dev_taylor`, `dev_test`, `dev_tyler`. Sent as `db` in **every** payload. |
| `-mt` | — | `YOLO`, `RTDETR` or `RFDETR` |
| `-m` | — | Weights object name in `dashcam_models`. Stored verbatim as `detection.model`. |
| `--confidence` / `--iou` / `--image-size` | 0.25 / 0.2 / 640 | Ultralytics thresholds. RF-DETR ignores iou and image size and uses resolution 672. |
| `--max-frames` | none | Stop inference after N frames |
| `--gpu` | off | Sends `gpu=true` on `get-job` / `complete-job` (GPU queue) |
| `--startup-delay` / `--dummy-sleep` | 0 / 10 s | Testing knobs |

### Endpoints the worker calls

All calls go to `{WVDOT_URL}api/ds/…`. `WVDOT_URL` must end with `/`.

| Method | Path | Body / response |
|---|---|---|
| GET | `get-job?clientId=&gpu=` | → `{video_name}` (empty means no work) |
| POST | `oci-webhook` | `{title, jobId, video_name, message, level, time_elapsed?}`; 50 s timeout |
| POST | `create_frames` | `{video_name, frame_count, db}` |
| POST | `upload_video_metadata` | `{video_name, video_metadata, db}` |
| POST | `upload_gps_metadata` | `{video_name, gps_metadata[], db}` |
| POST | `geometryToMeasure` | `{locations:[{geometry:{x:lon,y:lat}}], tolerance:20}` → `{locations:[{results:[{routeId, measure, lineDistance, geometry}]}]}` |
| POST | `upload_lrs_video_segments` | `{video_name, gps_metadata[], lrs_video_segments{}, db}` |
| POST | `add_image_names_to_frames` | `{video_name, image_filenames:[{frame_number, filename, width, height}], bucket_name, db}` |
| POST | `upload_detections` | `{video_name, detections:[{frame_number, class_id, x_center, y_center, width, height, confidence, model, track_id?}], db}` |
| POST | `invalidate_video` | `{video_name, fps, resolution, reason_rejected, db}` |
| POST | `complete-job` | `{video_name, status, clientId, elapsed_time, logs, gpu}` |

- The worker sends **no auth** with any of these calls.
- **Only the webhook has a timeout**, so a hung backend stalls the worker.

### Models and thresholds

- **Weights** come from the `dashcam_models` bucket and are chosen per job (`-m`). The model name is written on every detection.
- **Class ids** come from the backend's `detection_class` table. The worker does not filter classes (`CLASSES=None`).
- **Bounding boxes** are **normalized centre x/y + width/height, 0–1**. The worker sends them as strings and `confidence` as a float.
- **Frame upload rule:** during inference, a frame JPEG is uploaded only if it has at least one detection. With `-u`, the `is_minimum_distance` frames are uploaded.

## Backend route inventory

- Paths are shown in **DEV form**. PROD/STAG prefix every path with `/dashcam`.
- **Caller:** FE = frontend, W = inference worker, Int = internal/scripts, — = unused.
- **Guard:** "none" means no auth at all.

### auth — `/auth`

| Method | Path | Guard | Caller | Purpose |
|---|---|---|---|---|
| POST | `/auth/auth` | shared demo password · **DEV only** | FE | Demo login |
| GET, POST | `/auth/session` | none | FE | Current session (+ DB backfill) |
| GET | `/auth/logout` | none | FE | Clear session |
| GET, POST | `/auth/` | none | FE | SAML `sso / sso2 / acs / slo / sls`; DEV bypass |
| GET | `/auth/attrs` | none | — | SAML attribute debug page |
| GET | `/auth/metadata` | none | Int | SP metadata XML; health check |

### base

| Method | Path | Guard | Caller | Purpose |
|---|---|---|---|---|
| GET | `/` | session (else 302 to SSO) | FE | SPA `index.html` |
| GET | `/dashcam` | none | — | PROD/STAG 308 → `/dashcam/` |
| GET | `/gif.worker.js` | none | FE | gif.js worker script |
| GET | `/test`, `/test2` | none | — | Dev probes |
| GET | `/static/*` | none | FE | Built SPA assets |

### ds — `/api/ds` (ingest, queue, jobs)

| Method | Path | Guard | Caller | Purpose |
|---|---|---|---|---|
| GET | `/get-job` | none | W | Claim next file (CPU or GPU queue) |
| POST | `/complete-job` | none | W | Mark file completed/failed |
| POST | `/oci-webhook` | none | W | Worker log events |
| POST | `/create_frames` | none | W | Create frame rows 1…N |
| POST | `/upload_video_metadata` | none | W | EXIF metadata |
| POST | `/upload_gps_metadata` | none | W | GPS rows + frame links |
| POST | `/geometryToMeasure` | none | W | LRS matching (≤ 50,000 points, tolerance (0, 1000] m) — always uses the default DB |
| POST | `/upload_lrs_video_segments` | none | W | LRS segments + route/measure on GPS |
| POST | `/add_image_names_to_frames` | none | W | Image rows linked to frames |
| POST | `/upload_detections` | none | W | Detections per frame |
| POST | `/invalidate_video` | none | W | Move video → `invalid_video` |
| POST | `/add-files` | none | FE | Enqueue files (CPU or GPU; may spawn a GPU worker) |
| GET | `/queue-status` | none | — | Queue summary |
| GET | `/files-status` | none | FE | Per-file queue detail |
| GET | `/is-processing` | none | FE | Navbar processing badge |
| POST | `/flush-queue` | none | Int | Force close (only when idle) |
| POST | `/cancel-batch` | `require_role('admin')` | FE | Kill workers, save as cancelled |
| POST | `/delete-batches` | `require_role('admin')` | FE | Delete batch history rows |
| POST | `/cancel-oci-workers` | `require_role('admin')` | FE | Cancel OCI job runs |
| GET | `/batch-history` | upload | FE | Paginated batches |
| GET | `/batch-history/stats` | upload | FE | Batch aggregates |
| GET | `/batch-history/{batch_id}` | upload | FE | Batch + file results |
| GET | `/batch-live-status/{batch_id}` | upload | FE | Live (Redis) or saved status |
| POST | `/start-upload-job` | upload | FE | Create `upload_job` (uploading) |
| PUT | `/complete-upload` | upload | FE | Link batch, → processing |
| GET | `/upload-job/{id}` | upload | FE | Upload job detail + email text |
| GET | `/upload-history` | upload | FE | Paginated upload jobs |
| GET | `/model-weights` | upload | FE | List `dashcam_models` objects |
| POST | `/videos-for-job` | upload | FE | Bucket + DB video list for job creation |
| POST | `/spawn-workers` | upload | FE | Spawn CPU/GPU workers |
| POST | `/cascade-delete-videos` | delete | FE | Wipe processing data for reprocessing |
| POST | `/prepare-for-upload` | delete | FE | Delete ≤ 20 test videos (bucket `taylor-frontend-test` + DB); blocked in PROD only |
| POST | `/requeue_unprocessed` | none | Int | Nightly step 1 callback |
| POST | `/run_nightly_pipeline` | none | Int | Start nightly pipeline now |
| GET | `/update_paths`, `/generate_paths` | none | Int | Path generation |
| GET | `/process_new_videos` | none | — | Legacy OCI job launcher |
| GET | `/update_video_processing` | none | Int | Set a processing-step column |
| POST | `/create_detection_test_set`, `/generate_detection_dataset`, `/upload_dataset`, `/upload_detection_training_results` | none | Int | ML dataset / training bookkeeping |
| GET | `/mine` | none | — | Broken legacy launcher |

### videos — `/api/videos`

| Method | Path | Guard | Caller | Purpose |
|---|---|---|---|---|
| GET | `/videos` | none (reads session user if present) | FE | Video list with filters (Label) |
| GET | `/video/{id}/frames` | none | FE | Frames + GPS + detections |
| POST | `/upload_video_data` | none | FE | Create video row, tags, enqueue |
| POST | `/video/rename` | none | FE | Rename a video (dry by default) |
| POST | `/update_annotations` | none | FE | Replace annotations; copy frame to `dashcam_annotated_images` |
| POST | `/delete_annotations` | none | FE | Delete annotations |
| POST | `/add_replace_annotations` | none | FE (legacy) | Legacy upsert |
| GET | `/get_all_annotations` | none | FE | Annotation list (Validation) |
| POST | `/get_annotated_images` | none | FE | Annotated images by source/class |
| GET | `/get_false_negatives` | none | FE | False negatives |
| POST | `/add_image_dataset`, `/add_images_to_dataset` | none | FE | Image sources / datasets |
| GET | `/detection_classes` | none | FE | `{status, classes:[{class_id, class_name}]}` |
| GET | `/detection_models` | none | FE | Distinct models (MV `video_detection_summary`) |
| POST, DELETE | `/video/{id}/mark_reviewed` | session | FE | Per-user, per-class review marks |
| GET | `/video/{id}/detection_tracks` | none | FE | MV `detection_tracks` |
| GET | `/par_urls` | none | FE | PAR URLs (read **and write**) |
| GET | `/query_bucket_videos` | none | FE | List bucket objects |

### paths — `/api/paths`

| Method | Path | Guard | Caller | Purpose |
|---|---|---|---|---|
| GET | `/get_all_paths` | none | FE | All paths (`PathInfo[]`) |
| GET | `/path_gps_metadata/{id}` | none | FE | Points, LRS segments, videos |
| POST | `/update_path_info/{id}` | none | FE | Description / tags |
| GET | `/path/{id}/detections` | none | FE | Detections by frame for the player |
| GET | `/path/{id}/detection_tracks` | none | FE | Tracks for a path |
| GET | `/lrs_video_segment/{z}/{x}/{y}` | none | FE | MVT (`mvt_lrs_segments`) |
| GET | `/road_traversal/{z}/{x}/{y}` | none | FE | MVT (`mvt_road_traversal`) |
| GET | `/road_traversal/collection_stats` | none | FE | MV `road_collection_stats` |
| GET | `/lrs_video_segment_bbox/{id}`, `/segment_intersections`, `/get_routes` | none | FE / — | Geometry helpers |
| GET | `/dem/{z}/{x}/{y}.webp`, `/terraintile.json` | none | FE | Terrain from local mbtiles |

### routes_map — `/api/routes_map`

| Method | Path | Guard | Caller | Purpose |
|---|---|---|---|---|
| GET | `/route_list` | none | FE | Routes with coverage stats |
| GET | `/route_points/{routeid}` | none | FE | Captured points along a route |
| GET | `/route_bbox/{routeid}`, `/route_coverage/{routeid}` | none | FE / — | Route extent / coverage |
| GET | `/image_detections/{file_name}` | none | FE | Detections for one image |
| POST | `/batch_image_detections` | none | FE | Detections for ≤ 100 images |
| GET | `/video_detections/{id}`, `/detection_density` | none | — / FE | Detection summaries |
| GET | `/detection_index_tile/{class}/{z}/{x}/{y}` | none | FE | MVT (`mvt_detection_index`) |
| GET | `/heatmap_stops`, `/heatmap_stops/county` | none | — | Stop heatmaps |

### tags — `/api`

| Method | Path | Guard | Caller | Purpose |
|---|---|---|---|---|
| GET, POST | `/tags` | none | FE | List / create tags (`?category=`) |
| GET | `/tags/statistics` | none | FE | Usage counts |
| PUT, DELETE | `/tags/{id}` | none | FE | Edit / delete tag |
| GET, POST, DELETE | `/paths/{id}/tags[/{tag}]` | none | FE | Path tags |
| GET, POST, DELETE | `/videos/{id}/tags[/{tag}]` | none | FE | Video tags |
| GET, POST, DELETE | `/images/{id}/tags[/{tag}]` | none | FE | Image tags (annotation review presets) |

### admin — `/api/admin`

| Method | Path | Guard | Caller | Purpose |
|---|---|---|---|---|
| GET | `/users/current/permissions` | session | FE | `{user:{roles[], permissions{view,upload,label,delete}}}` |
| GET | `/users`, `/users/{id}`, `/users/{id}/permissions` | none | FE | User listing |
| PUT | `/users/{id}` | none | FE | Edit user |
| POST, DELETE | `/users/{id}/roles[/{role}]` | none | FE | Assign / remove role |
| GET, POST, PUT, DELETE | `/roles[/{name}]` | none | FE | Role CRUD |
| GET | `/site-settings/{admin-only · routes-map-enabled · path-view-video · flagship-model · collection-map-enabled}` | session | FE | Feature flags `{enabled}` |
| PUT | `/site-settings/admin-only`, `/site-settings/routes-map-enabled` | session + admin in selected DB | FE | Toggle flags |

### user, chat, embeddings, basemap

| Method | Path | Guard | Caller | Purpose |
|---|---|---|---|---|
| PUT | `/api/user/avatar-color` | session | FE | Save avatar colour |
| POST | `/api/chat` | `require_permissions()` | — | Stateless LLM chat (OCI GenAI; ≤ 50 messages, ≤ 8 images) |
| * | `/api/embeddings/*` | `require_role('admin')` (whole router) | own HTML pages | SigLIP search: `SearchUI`, `StatsUI`, `LabelUI`, `/search/{text,concept,similar}`, concepts, prompts, examples, `/embed`, `/status`, `/models` |
| GET | `/api/basemap/styles[…]`, `/tiles/{z}/{x}/{y}.pbf`, `/fonts/…` | none | FE | Local basemap from `DASHCAM_PATH` |

## Frontend pages and their API calls

All requests go through axios to relative `/dashcam/...` paths.

### Routes and navigation (`src/App.tsx`, `src/components/Navbar.tsx`)

| Route | Page | Guard | Nav |
|---|---|---|---|
| (logged out, any path) | `Login` | — | — |
| `/` | `UploadV2` | logged in | Upload |
| `/viewer`, `/viewer/:pathId` | `PathViewer` | logged in | Maps → Path Viewer |
| `/viewer/:pathId/metadata` | `PathMetadataPage` | logged in | — |
| `/map` | `RoutesMap` | flag `routes_map_enabled` or admin | Maps → Routes Map |
| `/collection` | `RoadTraversalMap` | flag `collection_map_enabled` or admin | Maps → Collection Map |
| `/label` | `LabelV2` | permission `label` | Label |
| `/annotation` | `Validation` | permission `label` | Annotations |
| `/tags` | `TagManagement` | logged in | Tags |
| `/processing-dashboard` | `ProcessingDashboard` | logged in | Processing → Active |
| `/batch-history[/:batchId[/file/:filename]]` | `BatchHistory` / `BatchDetail` / `FileDetail` | permission `upload` | Processing → History |
| `/upload-history[/:uploadJobId]` | `UploadHistory` / `UploadDetail` | permission `upload` | Processing → Uploads |
| `/users` | `UserManagement` | role `admin` | Admin → Users |
| `/analytics` | `UserAnalytics` | role `admin` | Admin → Analytics |
| `/business-logic` | `BusinessLogic` (this page) | role `admin` | Admin → Business Logic |
| `/settings` | `UserSettings` | logged in | avatar menu → Settings |
| `/project` | `Project` (Figma embed) | logged in | — |

### App shell (every page)

| Call | Why |
|---|---|
| `GET /auth/session` | Logged in? (non-empty object) |
| `GET /api/admin/users/current/permissions?db=` | Roles + permissions (re-run on `db` change) |
| `GET /api/admin/site-settings/{admin-only, routes-map-enabled, path-view-video, collection-map-enabled}` | Feature flags (errors → false) |
| `GET /api/videos/detection_classes?db=` | Class list, colours, visible classes |
| `GET /api/ds/is-processing` | Navbar badge (every 5 min) |
| `GET /auth/logout` | Sign out |

### Per page

| Page | Calls |
|---|---|
| **Login** | `POST /auth/auth`, `GET /auth/session` |
| **UploadV2** | `GET /api/tags`, `GET /api/videos/par_urls`, bucket listing via PAR, `POST /api/ds/start-upload-job`, `PUT <PAR>/<file>`, `POST /api/videos/upload_video_data`, `POST /api/ds/add-files`, `PUT /api/ds/complete-upload`, TagSelector `GET/POST /api/tags` |
| **PathViewer** (+ PathsTable, IntegratedPathPlayer) | `GET /api/paths/get_all_paths`, `GET /api/paths/path_gps_metadata/:id`, `POST /api/paths/update_path_info/:id`, path tag `GET/POST/DELETE`, MVT `/api/paths/lrs_video_segment/{z}/{x}/{y}`, `GET /api/paths/terraintile.json`, `GET /api/ds/model-weights`, `GET /api/paths/path/:id/detections`, images/videos from `dashcam_frames` / `dashcam_videos` read PARs |
| **PathMetadataPage** | `GET /api/paths/get_all_paths` (filters client-side), `POST update_path_info`, path tag add/remove |
| **LabelV2** | `GET /api/videos/detection_models`, `GET /api/videos/par_urls` (read-only PARs), `GET /api/videos/videos`, `GET /api/videos/video/:id/frames`, `POST /api/videos/update_annotations`, `POST/DELETE /api/videos/video/:id/mark_reviewed`, `POST /api/images/:id/tags`, review menu `GET /api/tags?category=Annotation Review` |
| **Validation** | `GET /api/videos/get_all_annotations`, `POST update_annotations`, `POST delete_annotations` (needs `delete`), `GET par_urls`, image tags |
| **RoutesMap** | `GET /api/videos/detection_models`, `GET /api/routes_map/route_list`, `GET /api/routes_map/route_points/:routeid`, `POST /api/routes_map/batch_image_detections`, MVT `/api/paths/road_traversal/…` and `/api/routes_map/detection_index_tile/…` |
| **RoadTraversalMap** | `GET /api/paths/road_traversal/collection_stats`, MVT `road_traversal` — **always `db=dev_bennett`** (no `db` prop passed) |
| **TagManagement** | `GET/POST /api/tags`, `PUT/DELETE /api/tags/:id` (delete needs `delete`) |
| **ProcessingDashboard** | every 15 s: `GET /api/ds/files-status`, `GET /api/ds/is-processing`; `POST /api/ds/cancel-batch` |
| **BatchHistory / BatchDetail / FileDetail** | `GET /api/ds/batch-history`, `GET /api/ds/batch-history/:id`, `GET /api/ds/batch-live-status/:id` (every 3 s while active), admin: `POST cancel-oci-workers`, `POST delete-batches` |
| **UploadHistory / UploadDetail** | `GET /api/ds/upload-history`, `GET /api/ds/upload-job/:id`, then batch calls above |
| **CreateJobModal** (admin button) | `GET /api/ds/model-weights`, `POST videos-for-job`, `POST cascade-delete-videos`, `POST prepare-for-upload`, `POST add-files {files, job_type, model?, model_type?}`, `POST spawn-workers` |
| **UserManagement** | `GET /api/admin/users`, `/roles`, `/site-settings/admin-only`; `PUT /users/:id`, `/roles/:role`; `POST /roles`, `/users/:id/roles`; `DELETE /roles/:role`, `/users/:id/roles/:role`; `PUT /site-settings/admin-only` |
| **UserAnalytics** | `GET /api/paths/get_all_paths`, `GET /api/admin/users` (aggregated in the browser) |
| **UserSettings** | `PUT /api/user/avatar-color`, then logout |
| **BusinessLogic** | none — markdown bundled at build time |

### Frontend business rules

- **Database selector:** `db` is stored in localStorage (default `prod`). It is sent as `?db=` on GETs and in the **JSON body** for `upload_video_data`, `update_annotations`, `delete_annotations`, `update_path_info`, `add-files` and `batch_image_detections`. Most `/api/ds/*` calls send no `db`.
- **Confidence filter:** global min 0.25 / max 1. `max_confidence` is only sent when it is below 1. The path player defaults to 0.7 and model `022026_signs.pt`.
- **Frame numbers are 1-based.** The video player uses `round(t × fps) + 1`, and detections must match the frame exactly. Label and Validation parse the number from the file name after `Frame_`. The source video name is `file_name.split('_Frame')[0] + '.MP4'`.
- **Saved annotations** carry `frame_number`, `model` (`'User'` when hand-drawn) and `user_id = session.user`. Boxes are normalized to 0–1.
- **Route ids** are 13 characters: county (2), sign system (1), route (4), sub-route (2), supplemental (2), direction (2). See `utils/routeIdParser.ts`.
- **Response envelopes:** admin, tag and user calls expect `{status, errors[]}`; `/api/ds/*` calls expect `{success}`.

## Data model and invariants

| Area | Tables | Key facts |
|---|---|---|
| Video chain | `video` → `frame` → `gps_metadata`, `image` → `detection` / `annotation` | `frame` PK is `(video_id, frame_number)`, **1-indexed**. A GPS row covers `start_frame…end_frame` inclusive. Detections hang off `image`, not `frame`. |
| Processing state | `video_processing_steps` (1:1 video), `invalid_video` | Step columns are the string `'Completed'` or NULL. `lrs IS NULL` gets a video requeued nightly. |
| LRS | `lrs_video_segment`, `public.route_new` | Segments carry `routeid, bmp, emp, is_increasing, seg_geometry`. `route_new` is LineStringZM in **SRID 3747**. |
| Paths | `path`, `path_tag`, MV `lrs_path_segment_mv` | Same-user, ≤ 5 s gap. `video.segment_id` is the order within the path. |
| Users | `users` (PK = e-number), `role`, `user_role`, `site_settings` | Permissions = OR over roles |
| Tags | `tag` + `path_tag`, `video_tag`, `image_tag`, `annotation_tag` | Colourless tags render `#00ff88` |
| Review | `user_video_review` | Per user, video, class |
| Processing history | `processing_batch` → `processing_file_result`, `upload_job`, `job_run` | Written to the **default DB** regardless of `db` |
| ML | `model`, `model_task`, `dataset`, `test_set*`, `detection_model_*_results`, `*_epoch_metrics`, `detection_class`, `image_source`, `bucket`, `par_url` | `par_url` has `object_read` / `object_write` flags |
| Vectors | `embed_model`, `image_vector`, `detection_vector` (`halfvec(1152)`), `concept`, `concept_prompt`, `concept_example` | SigLIP 2 via the embedding service on port 8100 |

- **Materialized views:** `detection_tracks`, `video_detection_summary`, `detection_index_*`, `road_traversal_summary`, `road_collection_stats`, `captured_route_geometry`, `lrs_path_segment_mv`.
- **Tile functions:** `mvt_lrs_segments`, `mvt_road_traversal`, `mvt_detection_index`, `mvt_route_geometry`.
- **Databases:** `SQLALCHEMY_BINDS` defines `prod` (`dashcam`), `dev_bennett`, `dev_taylor`, `dev_test`, `dev_tyler` and `schema`, all on one server.
- **Always on the default DB, whatever `db` says:** auth checks, batch history, upload jobs, `geometryToMeasure` and `/video/rename`.

## Object storage

| Bucket | Written by | Read by | Notes |
|---|---|---|---|
| `dashcam_videos` | Browser (write PAR) | Worker (SDK), path player (read PAR) | Object name = original file name |
| `taylor-frontend-test` | Browser on non-prod hosts | Worker | DEV/STAG uploads; `prepare-for-upload` deletes from here |
| `dashcam_frames` | Worker | Frontend via read PAR | `<video stem>_Frame_<NNNN>.jpg`, bucket root, no prefix |
| `dashcam_annotated_images` | Backend (`CopyObject` on annotation save) | ML training | |
| `dashcam_models` | Manual | Worker, `GET model-weights` | Weights, e.g. `*.pt`, `*.pth` |
| `dashcam_invalid_files` | Worker (prod db only) | Upload duplicate check | Rejected videos |
| `data-science-logs` | Worker via `PAR_URL_LOGS` | People | Crash logs |

PAR URLs live in the `par_url` table and are served by `GET /api/videos/par_urls`.
A few read PARs are also hard-coded in the frontend and backend. **Rotating a PAR
means updating the table and every hard-coded copy.**

## Core assumptions (cross-repo contracts)

Breaking any of these breaks another repo. Change them only together, and update this list.

1. **Frame numbers are 1-indexed** everywhere: worker `i+1`, `create_frames` 1…N, GPS `start_frame` / `end_frame`, the player's `round(t·fps)+1`, and `detections_by_frame` keys.
2. **Frame file names** are `<video stem>_Frame_<NNNN>.jpg`. The frontend parses the frame number from them and derives the video as `<stem>.MP4`.
3. **Video object name = file name = `video.video_name`** across the bucket, DB and queue. Upload names must match `YYMMDD_HHMMSS_<n>_<CAM>.MP4`.
4. **GPS is 10 Hz Nextbase Track3 metadata.** Videos without it, or without movement, are rejected, and the SQL assumes 10 rows per second.
5. **Boxes are normalized centre-x, centre-y, width, height (0–1)** for detections and annotations alike.
6. **Worker success contract:** HTTP 200 and `{"status": true}`. The frontend uses `{status}` for admin/tag/user calls and `{success}` for `/api/ds/*`.
7. **Every worker payload carries `db`**, and the backend binds that database for the write.
8. **URL prefix rule:** `/dashcam` in PROD/STAG, bare in DEV. The frontend always calls `/dashcam/...`.
9. **Status strings** for batches, upload jobs, queue files and `job_run` rows are matched literally by the frontend.
10. **One gunicorn worker.** Queue state, spawn locks and the scheduler assume one process.
11. **Detections are keyed by model name.** Filters, summaries and nightly tracking select on `detection.model`. The nightly tracker is pinned to `042226.pth`.
12. **`track_id` is per (video, class, model)** and is recomputed for whole videos only.
13. **`ENVIRONMENT` ∈ {DEV, STAG, PROD}** in both the backend and the worker. It controls prefixes, auth, OCI auth mode and Redis batch keys.

## Known gaps and risks

These are recorded so nobody builds on them by accident. Details and fixes are in the
security audit (`security_audit_2026-09-09_new_branches/`).

- **Worker endpoints are unauthenticated.** Anything that can reach the backend can claim jobs, write rows, invalidate videos, or trigger queue and pipeline operations. The fix needs a worker credential passed through `create_oci_job_run` and checked by every `api/ds` worker route.
- **Most read/write routes outside `api/ds` have no guard.** That includes user/role management in `api/admin`, annotations, tags and path edits. The frontend's `ProtectedRoute` is UI-only.
- **`GET /api/videos/par_urls` returns write-capable PARs** to any caller.
- **Dynamic SQL in some video filters** — tracked in the audit.
- **`ProtectedRoute` renders children while permissions are `null`** (still loading, or the fetch failed).
- **Pending jobs auto-fail after 600 s.** Long videos on slow workers can be marked failed while they are still processing.
- **`JOB_TARGET_DB` defaults to `dev_bennett`**, so nightly jobs run there unless it is set.
- **`/collection` is hard-wired to `dev_bennett`** in the frontend.
- **Worker gaps:**
  - No request timeouts except on the webhook.
  - Dry runs still post `complete-job`.
  - `-lrs -u` without `-e` raises `KeyError`.
- **Email notifications are not sent.** The text is only built and stored.

## Environment variables

Names only. Values live in each repo's `.env` / job configuration.

| Scope | Variables |
|---|---|
| Backend core | `ENVIRONMENT`, `FLASK_SECRET_KEY`, `BIND_IP`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASS`, `THREADPOOL_TOKENS`, `DISABLE_BACKGROUND_SERVICES`, `DEMO_LOGIN_PASSWORD` (DEV), `USER` (DEV bypass identity), `DASHCAM_PATH` |
| Object storage | `NAMESPACE`, `REGION`, `BUCKET`, `BUCKET_VIDEOS`, `BUCKET_FRAMES`, `PAR_URL`, `FRAMES_PAR_URL`, `MODEL_PAR_URL` |
| Workers / scaling | `USE_OCI_DATASCIENCE`, `WORKER_DUMMY_MODE`, `DUMMY_SLEEP_TIME`, `WORKER_STARTUP_DELAY`, `WORKER_STARTUP_TIME_SIM`, `TARGET_AVG_DURATION_SIM`, `AUTOSCALE_INTERVAL_REAL`, `MAX_WORKERS`, `MAX_GPU_WORKERS`, `OCI_JOB_ID`, `OCI_GPU_JOB_ID`, `JOB_ARGS`, `GPU_JOB_ARGS`, `OCI_COMPARTMENT_ID`, `OCI_PROJECT_ID`, `WVDOT_URL`, `CONDA_ENV_OBJECT_NAME`, `ARTIFACT_OBJECT`, `JOB_TARGET_DB` |
| Redis / scheduling | `REDIS_URL`, `NIGHTLY_APP_BASE_URL` |
| Chat | `CHAT_PROVIDER`, `GENAI_MODEL_ID`, `GENAI_ALLOWED_MODELS`, `GENAI_COMPARTMENT_ID`, `GENAI_REGION`, `GENAI_MAX_TOKENS`, `GENAI_TEMPERATURE`, `GENAI_SEED` |
| Embeddings | `EMBED_SERVICE_URL`, `EMBED_SERVICE_TIMEOUT` |
| Inference worker | `ENVIRONMENT` (required), `WVDOT_URL`, `NAMESPACE`, `BUCKET_VIDEOS`, `BUCKET_FRAMES`, `BUCKET_INVALID`, `BUCKET_WEIGHTS`, `PAR_URL_LOGS`, `EXIF_TOOL_PATH` (the code reads this — not `EXIFTOOL_PATH`), `BASE_PATH`, `VIDEO_CACHE`, `CREATE_LOGS`, `DEBUG` |

`dashcam_backend/docs/ENV_VAR_LIFECYCLE.md` traces how each variable flows from the backend into an OCI worker.

## Document history

| Date | Change |
|---|---|
| 2026-09-27 | First version: system map, sequence diagram, auth model, full route inventory, per-page API map, inference pipeline, invariants and known gaps. Demo login documented as DEV-only (SEC-01 fix). |
