# MMS Frontend — Claude / Repo Notes

This file documents durable conventions for the `mms-frontend` repo
that any contributor (human or AI) should follow.

## Repo layout

- The app lives under `mms/`. Run all `npm` commands from there
  (`mms-frontend/mms/`) — `package.json` is in that subdirectory,
  not at the repo root.
- The Vite app is mounted at the `/mms` base path (see
  `mms/vite.config.ts` `base: '/mms'` and the `<BrowserRouter
  basename="/mms">` in `src/main.tsx`). All Playwright route helpers
  in `mms/e2e/helpers/navigation.ts` include the `/mms` prefix.
- The Vite dev proxy forwards `/api`, `/auth`, and `/mms/assets` to
  the Flask backend on `http://localhost:5000`.
- The production build writes to `../../mms-backend/mms` so the
  Flask app serves the bundle directly.

## Node version

The CI workflow assumes **Node 20**. Local dev works on Node 18 too,
but the coverage provider was deliberately pinned to `istanbul`
(not `v8`) for Node-18 compatibility — see `mms/vite.config.ts`.
If we bump the minimum to Node 20+ in CI, switch to `provider: 'v8'`.

## Test documentation maintenance

> **Whenever tests are added, modified, or removed, update
> `TESTS.md` in the same PR.** Treat `TESTS.md` as the single source
> of truth for what this repo's test suite covers; drift makes it
> useless.

### How to update `TESTS.md`

1. Find the right section. Vitest tests are grouped by area
   (`utils`, `services`, `contexts`, `components`); Playwright
   tests are grouped one section per spec file.
2. **Adding a test**: add a bullet under the right file describing
   the scenario in one line. If the file is brand new, add a new
   subsection under the right area (and a brand new area subsection
   if needed).
3. **Removing a test**: delete the corresponding bullet (and the
   parent file/area heading if it ends up empty).
4. **Renaming or substantially rewriting a test**: update the
   bullet text. If only the assertion changed but the intent did
   not, no update is needed.
5. Update the **test counts** ("~185 tests / 19 files" and
   "~30 tests / 11 specs") at the top of the respective tier
   section.
6. If the change affects the **mocking strategy**, config defaults,
   reporters, env vars, or coverage scope, also update the
   "How to run", "Vitest tier" config note, or "Mocking strategy"
   sections so they stay accurate.

The goal is that a reader scanning `TESTS.md` can list out every
non-trivial scenario the suite exercises, without opening any
test file.

## Test tiers (cheat sheet)

- **Vitest** (`mms/src/**/*.test.{ts,tsx}`) — fast jsdom unit and
  component tests. Use for pure functions, API clients, contexts,
  small presentational components. Setup: `mms/src/test/setup.ts`;
  helpers: `mms/src/test/helpers.ts`.
- **Playwright** (`mms/e2e/*.spec.ts`) — real-browser E2E. Default
  mocks the Flask backend via `page.route()`; set `E2E_LIVE=1` for
  a live backend. Setup: `mms/e2e/helpers/`.

When choosing which tier a new test belongs in: if the behaviour
can be exercised without rendering MapContainer, TaskSidebar, or
the full router shell, prefer Vitest.

## Git commit policy

Do not create git commits unless the user explicitly asks. (This
mirrors the parent repo's `CLAUDE.md` policy.)

## Changelog

Backend and frontend changes share a single changelog file living in
the sibling `mms-backend` repo (`mms-backend/CHANGELOG.json`). When a
change in this repo lands, the corresponding entry goes in the
`frontend` array of that file. Coordinate with the backend agent if
a single PR spans both repos.
