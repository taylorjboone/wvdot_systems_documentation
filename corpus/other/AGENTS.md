# Dock agent instructions

These instructions apply to every agentic change in this repository. Dock is
**DOCK — Document Organization and Collaboration Keeper**. Develop locally with
`./dev`; do not introduce Docker as a development requirement.

## Required living documentation

**Every agentic code change MUST update all five documents below in the same
working-tree change, before presenting the work as complete.** Documentation is
part of implementation, not optional follow-up work. This applies even when the
user has not requested a commit; never defer documentation until commit time.

| Document | Canonical source | In-app URL |
| --- | --- | --- |
| High-level Usage guide for end users | `frontend/src/docs/usage.md` | `/docs/usage` |
| In-depth Business logic covering frontend and backend | `frontend/src/docs/business-logic.md` | `/docs/business-logic` |
| Frontend change log | `frontend/src/docs/frontend/change-log.md` | `/docs/frontend/change-log` |
| Backend change log | `frontend/src/docs/backend/change-log.md` | `/docs/backend/change-log` |
| Windows client change log | `frontend/src/docs/client/change-log.md` | `/docs/client/change-log` |

**Usage and Business logic are separate documents for different audiences.** Usage
explains everyday tasks to end users in plain language: where to click, what to expect,
and how to resolve common workflow problems. Keep code, schema, API, architecture,
internal algorithms and agent-maintenance rules out of its visible content.

Business logic is the in-depth reference for both frontend and backend behavior:
contracts, validations, state transitions, permissions, data models, integrations,
concurrency, failure handling and assumptions. Keep both application layers together
in that technical reference. Web frontend, backend and Windows client must each have a separate changelog.
Do not merge Usage with Business logic or create competing copies elsewhere.

These Markdown files are rendered directly in the web app's **Docs** section, using
FOIA's source-to-rendered-page pattern. Backend material lives under the frontend
docs directory so Vite can bundle it; it remains a backend maintenance responsibility.

For every code change:

1. Read Usage, Business logic and all three changelogs before editing.
2. Update end-user task instructions in Usage and the affected technical behavior in
   Business logic. Describe implemented behavior, correct stale statements and remove
   obsolete guidance. If end-user behavior is unchanged, update a dated maintenance
   comment in the Usage source to record that review; keep it out of the rendered guide.
3. Add a dated entry to Business logic's **Review history**, explaining the
   change and the reviewed impact on both layers. For a layer with no behavior change,
   explicitly say its contract was reviewed and remains unchanged.
4. Add or extend a `## YYYY-MM-DD` section at the TOP of **all three** changelogs, newest
   first. Group entries under `### Added`, `### Changed`, `### Fixed`, or `### Removed`
   as appropriate. Each bullet uses **bold summary (scope)** — then concrete detail;
   scope is `UI`, `backend`, `data`, `client`, or `both`. For an unaffected layer, record the
   reviewed unchanged impact and reference the companion change. Do not invent a
   runtime change merely to satisfy this rule. Preserve previous entries.
5. Keep all five documents accessible through their existing `/docs/...` URLs and
   rendered from these exact sources. Verify rendering, links, tables, heading anchors
   and URL navigation when changing the viewer. Docs must reach the same build as code.

This includes UI/API changes, migrations, workers, dependencies, configuration,
scripts, tests, refactors and fixes. Documentation-only changes must keep related
references consistent. Never put credentials, session tokens, private document
contents or environment secrets into bundled docs. These are application reference
pages, not protected DMS records or audit logs.

## Desktop changes

Windows client code lives in `desktop/windows`. Record desktop UI, Explorer integration,
local synchronization, native DLL, installer, build-script and packaging changes in
`frontend/src/docs/client/change-log.md`, displayed in the web app at
`/docs/client/change-log` through the existing Docs Markdown reader. Include the
applicable MSIX version, concrete behavior change and relevant validation or rollout
limitations. Use dated entries, newest first, with the same Added/Changed/Fixed/Removed
format as the other changelogs and `client` scope for client-only work.

Web frontend changes belong in the frontend changelog; server contract changes belong
in the backend changelog. For a companion change that does not affect a layer, record
its reviewed unchanged impact and link to the relevant changelog. Preserve previous
entries, including historical client entries in the frontend log; the dedicated client
log is the canonical location for future client update details. Do not claim a build
was deployed or installed unless verified. Every desktop code change updates all five
canonical documents above. Keep Usage high-level and protocol/state/security details
in Business logic.

Run the portable desktop core checks and cross-targeted WPF build where available.
Native DLL compilation, MSIX install and Explorer/CAD behavior require Windows; report
those separately and never call a cross-build Windows runtime verification. Preserve
pending local work, keep credentials encrypted for the Windows user, and never commit
signing keys or user caches. Consult `desktop/windows/ACCEPTANCE.md` for pilot gates.

## Verification and source control

- Run checks appropriate to the change and report actual results/limitations.
  `npm --prefix frontend run build` checks frontend compilation. Browser checks use
  `npm --prefix frontend run test:e2e` with the native app running.
- Backend integration tests use the isolated native database:
  `.venv/bin/python scripts/local_db.py --test`, then
  `PW_RUN_INTEGRATION=1 .venv/bin/pytest -q backend/tests`. Never use the application
  database as a disposable test database.
- Keep credentials, `.runtime/`, and
  `Why_Organizations_Use_ProjectWise_as_a_Document_Store*` artifacts out of Git.
- Do not create commits or push unless the user explicitly asks for that action for
  the current task. Earlier-task authorization does not carry forward. Complete
  implementation, documentation and verification without waiting for commit permission.
  When a commit is requested, include the corresponding documentation with the code;
  do not split them into separate commits.

Adapted from the user-provided FOIA `CLAUDE.md`. This repository's `CLAUDE.md` imports
this file so agents share one authoritative policy.
