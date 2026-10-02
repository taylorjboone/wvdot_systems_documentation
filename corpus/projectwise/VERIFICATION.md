# Verification record

Verified September 7–8, 2026, on the local pilot in this workspace. The application is available at **http://127.0.0.1:5174** with real private OCI storage in **AIDevelopment / us-ashburn-1**. The ProjectWise report and pre-existing report artifacts were preserved.

## Results

| Check | Observed result |
|---|---|
| Python unit/integration suite | **55 passed** against native Postgres, one opt-in load test skipped in the regular suite. The load scenario was run separately and passed. |
| Browser acceptance | **13 browser scenarios passed** against the native app and real OCI storage, including group permission administration, complete-tree Trash/restore, URL navigation, and tagging. |
| Frontend compilation | TypeScript and Vite production build passed. API types generated from FastAPI OpenAPI. |
| Static checks | Ruff passed for backend and operational scripts. |
| Real storage smoke | Create-only upload, idempotent replay, exact OCI object-version retrieval and checksum verification passed. |
| Real embeddings | Cohere `cohere.embed-v4.0` in Ashburn returned 1,024-dimensional vectors. Permission-scoped live semantic searches succeeded for editors/viewers; the auditor received 403. |
| Runtime OCI privileges | Attempts to overwrite/delete a dedicated synthetic smoke object and write the operations bucket were denied (OCI 404). The original smoke bytes remained retrievable. |
| Exact upload limit | **262,144,000 bytes** uploaded and downloaded through the real API/OCI. SHA-256 matched: `cc7f451a21037c81d93b187a39c23d38df91403f55e1c76086ec140ecb527db2`. A 262,144,001-byte reservation received 413. The synthetic boundary document was archived afterward. |
| Abandoned-upload cleanup | One deliberately aged, unpublished synthetic upload was fenced and its OCI version removed. Later finalization received 409; the document remained unpublished. |
| Backup and audit export | Custom-format database backup and JSONL audit batch were written create-only to the private operations bucket. |
| Recovery | An actual dump restored into a uniquely named, network-isolated disposable Postgres container. All **13 file versions referenced by that snapshot**, including the 250 MB fixture, were retrieved from OCI and SHA-256 checked. The container was removed. |
| Local database privileges | Separate limited API, audit and indexing database roles use distinct connection pools and generated passwords. In local development these pools run inside one Python backend process; migrations run before startup. |

## Native local development

`./dev` runs the Python backend and Vite frontend directly on macOS; the backend runs indexing in a background thread. Postgres 17 and pgvector run natively in an isolated `.runtime/postgres` cluster. Normal startup does not invoke Docker.

The migration from the previous container database preserved all **16 documents, 22 versions, 14 grants, 10 folders and 1,026 audit events** present in the snapshot. Committed-version, audit-history and file-pointer checksums matched after restoration. Evidence: `.runtime/native-move-result.json`; the local safety backup is `.runtime/pre-native-move.dump`. Subsequent browser tests add synthetic records.

The backend and browser suites above passed against this native setup. The embedded-worker test verifies indexing and shutdown. Earlier recovery and load evidence below describes the previous pilot verification environment.

## Control coverage

The backend suite verifies:

- Allowed and denied metadata, download, history, checkout, comment, archive and audit operations for all ten seeded accounts.
- Bridge A, Road B, External and Restricted isolation; minimal external ancestor navigation without sibling listings.
- Unauthorized filenames, identifiers, snippets, returned counts, previews and historical content do not leak through tested branches.
- Revocation blocks pending finalization and later reads; managers cannot assign outside their boundary, and operational grants cannot assign global roles.
- Simultaneous checkout has one winner. Force-released tokens cannot commit. Concurrent and repeated finalization creates one new version.
- Metadata-only edits use `If-Match` and remain distinct from binary versions. Cross-document current-version pointers are rejected by foreign keys.
- Earlier versions download correctly. Restoration creates the next immutable version and retains current metadata.
- Known text changes and metadata snapshot differences appear in comparison; unsupported/incomplete extraction is explicit.
- Denials survive rollback; successful check-ins have matching events. Runtime audit updates/deletes are denied. Unavailable required auditing prevents protected downloads.
- Upload outage, checksum mismatch, incomplete transfer and database failure after OCI success preserve the current version and allow safe retry.
- No API transaction remains idle during tested object transfer or embedding-provider calls.
- Session logout/expiry invalidates access, checkout survives logout, CSRF is checked, and pooled connections do not retain the prior user’s identity.
- Worker failures preserve file usability, expired claims are fenced, retries recover, and an older indexing generation cannot replace a newer active generation.
- Long-document chunking covers every body range beyond 600 chunks; XLSX content beyond 2,000 rows is preserved. PDF, DOCX, XLSX, EML and explicit unsupported/incomplete extraction were exercised.

## Browser workflows

Chromium exercised a new real-OCI document through upload → checkout → download → metadata edit → check-in → extracted-text/metadata comparison → comment → restoration as version 3 → activity history. Separate workflows checked external navigation, administrator PDF previews/audit search, and the auditor’s metadata-only interface. No page JavaScript errors occurred in the complete edit workflow.

Screenshots are available locally in `.runtime/browser-documents.png`, `browser-preview.png`, `browser-comparison.png`, and `browser-external.png`. The comparison screenshot was inspected after its transition completed.

## Pilot load and recall

The disposable test database received **10,000 synthetic document/version records per load run**, with **500 representative searchable records** and deterministic 1,024-dimensional test embeddings. Ten users made 30 concurrent browser-list API requests. The successful measured run completed in approximately **6.7 seconds**, including fixture insertion and recall checks; the slowest user’s three requests took approximately **2.1 seconds**. The folder-only load verification used a fresh disposable database containing the regular integration fixtures.

For `pw4`, `pw5` and `pw6`, approximate top-20 candidates were checked against exhaustive ranking under the same SQL/RLS identity. Exact-ID overlap was 0.70, 0.70 and 0.65; tied synthetic distances allowed different IDs at the cutoff. All approximate candidates met the exact top-20 distance threshold (tie-aware distance recall 1.00). Underfilled filtered queries use exact fallback. These are pilot correctness/load results with synthetic vectors, not a claim of real-world semantic recall or a production throughput guarantee.

The first load run found that globally disabling index scans also disabled indexed permission lookups. The corrected exact fallback forces exhaustive distance ordering while retaining authorization/join indexes. The rerun passed. An actual worker run also caught extension-sensitive XLSX opening; the worker now preserves the source suffix in its bounded temporary path, and the real XLSX fixture is fully indexed.

## Evidence and limits

Machine-readable evidence is kept locally in `.runtime/pilot-load.json`, `boundary-result.json`, `oci-privilege-check.json`, `reconciliation-result.json`, `recovery-result.json`, `live-account-check.json`, and `oci-resources.json`. Backups, credentials and runtime artifacts are intentionally excluded from source control. Source adaptation hashes are in [foia-provenance.json](foia-provenance.json).

The 10,000-record load used the isolated Postgres test database and explicit test doubles for cloud calls. Real-cloud checks separately exercised storage permissions, small and 250 MB transfers, embeddings, browser version workflows, derived outputs, cleanup, exports and recovery. The recovery count describes the tested snapshot; subsequent browser tests can create additional synthetic versions.

The remaining boundaries are the agreed pilot scope: no CAD integration/reference management, simultaneous editing, visual diffs, formal approvals, transmittals or permanent deletion. Extraction and comparison limits are documented in [README](../README.md). Audit history is application-level append-only, and OCI service logging remains supplementary best-effort evidence.

## Folder-directory correction

The current schema has one Directory root, ordinary folders and mandatory folder grants. There is no `dms.projects` table or project column on any `dms` record; `/api/projects` returns 404. Existing Bridge A / Road B identities became ordinary folders. The old audit project field is retained only to preserve immutable historical records.

Before the live upgrade, `scripts/check_directory_migration.py` restored a live dump into a network-isolated disposable database and applied the new migration. It verified all **70 effective roles** (ten users across seven original folders), unchanged current-version pointers/folder IDs, correct new parents, and byte-for-byte JSON checksums of committed versions, audit events, checkouts and pending upload sessions. Evidence: `.runtime/directory-migration-result.json`. A fresh pre-migration database backup was uploaded to the private operations bucket.

Six new backend acceptance tests cover arbitrary folder grants and inheritance, direct overrides and revocation fallback, effective-access source display, breaks in inheritance with minimal ancestor navigation, moving files into a different access subtree, retained OCI references/history, checkout move blocking, cycle rejection at API and database layers, stale folder revisions, controller rename, manager boundaries across hidden restricted descendants, empty-folder deletion with direct grants, and rejection of deletion when archived file history remains.

## Directory UI and uploads

The unified directory table displays folders and files together, uses the handoff's original outlined Dock logo, provides collapsible navigation, and adapts to a 390-pixel phone viewport without page overflow. The top-right account menu opens a profile page with persisted browser appearance, effective folder-access links, and sign-out.

Five additional browser tests cover desktop/mobile layout and profile appearance; a folder-row drop with nested and empty folders followed by an exact OCI byte download; partial upload failure and idempotent retry; a denied viewer drop without an upload request; and a real browser folder picker preserving nested paths. All ten browser tests passed against the native backend and real OCI storage. The synthetic folder-drop fixture emulates browser directory-entry callbacks; the picker test uses a temporary directory on disk.

An additional backend test verifies that editors can create inheriting nested folders while viewers and users outside the scope cannot. Editors still cannot rename folders or change inheritance. Migrations 0006–0007 update only folder insertion permissions. Uploads use the established size limit, audited upload lifecycle, and version finalization. Browser upload queues remain in memory; keep the page open while importing.

Inspected screenshots: `.runtime/ui-directory-desktop.png`, `.runtime/ui-directory-mobile.png`, and `.runtime/ui-profile-dark.png`.

## Groups, Trash, URL navigation and automatic tags

Migrations 0008–0012 add group membership and folder grants, recursive recoverable deletion, structured enrichment, tag aliases, and document/version integrity constraints. The group migration compares every existing user/folder role before and after conversion and aborts if effective access changes. It converts only matching original demo grants; custom individual exceptions remain. Stable document and file-version identities remain unchanged.

Nine additional backend tests verify nearest-folder/group/direct precedence, immediate membership revocation, subtree deletion with checkout blocking and name-conflict recovery, independent archived children, tag/search isolation, preserved manual labels/dismissals, canonical aliases across differently authorized corpora, blocked edits/restoration through a deleted child, and provider-failure/context fencing. The older management-boundary test now removes its temporary individual exception instead of recreating an obsolete demo grant.

The three new browser scenarios verify searchable People lists and user details, group creation/membership/folder grants, effective group-source display, recursive Trash browsing and restoration with a real OCI file, document tags/manual labels, tag-filtered search, URL-addressed document tabs, reload, and Back navigation. The upload retry test caught and now covers an immediate-navigation destination race. New API response types for groups and tags are generated from FastAPI OpenAPI.

A live synthetic I-79 inspection report completed OCI Gemini 2.5 Flash tagging with a summary and content/context labels, including Kanawha County, WVDOT, steel bearings, and the contract identifier. A read-only live queue check found 33 ready and 23 partial jobs, with no failed jobs at that time. Partial means incomplete/unsupported extraction or bounded summary consolidation, not a complete-content claim. Counts are a snapshot; new uploads queue further analysis. No bulk retry was needed or executed.

Inspected interface evidence: `.runtime/ui-people.png`, `.runtime/ui-group.png`, `.runtime/ui-trash-tree.png`, and `.runtime/ui-document-tags.png`. The earlier empty-folder-only deletion behavior described in historical verification sections has been replaced by recoverable tree deletion.

The group-aware 10,000-record load/recall scenario was rerun against native Postgres after migrations 0008–0012 and passed (7.57 seconds for the pytest invocation). It uses synthetic documents and deterministic embeddings; `.runtime/pilot-load.json` contains the updated measurements.
