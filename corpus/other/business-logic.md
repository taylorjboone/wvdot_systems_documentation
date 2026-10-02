# Business logic

This is the in-depth behavior reference for **WVDOT Dock**, covering frontend workflows and
backend rules, data, permissions, integrations and failure handling. For everyday
instructions, read [Usage](/docs/usage). Implementation history is recorded in the
[Frontend change log](/docs/frontend/change-log),
[Backend change log](/docs/backend/change-log), and
[Client change log](/docs/client/change-log).

## Name and purpose

The official name is **WVDOT Dock**. **DOCK** stands for **Document Organization
and Collaboration Keeper**; this reference uses Dock as the short name.

WVDOT Dock exists to give WVDOT teams and authorized collaborators a shared document
directory with controlled access, a clear current version, and an accountable history.
It addresses the practical questions behind document control: who can access a file,
who is editing it, which version is current, and how it changed over time.

Folder and group permissions define access and inheritance. Server-authorized
check-out and check-in coordinate file replacement, while immutable committed
versions preserve prior work. Access logs and change events record activity;
permission-aware search, contextual tags, and comments support discovery and
collaboration. Stable document identities connect these workflows even when a file
is renamed, moved, or revised. The sections below define the rules and limitations
that make those behaviors consistent across the web and Windows clients.

## Frontend business logic

### Application and navigation

Dock is one directory of folders and documents. Bridge A and Road B are ordinary
folders. Folder rows appear alongside file rows in the directory table. The
sidebar shows accessible folders and the minimal ancestor paths needed to reach them. It
opens the root and its direct children; deeper folders open on request, because they
lead to the folder being viewed, or because they are navigation-only and exist in the
tree only as the path to something reachable. An explicit collapse wins over all of
these, and a folder's children are listed a hundred at a time. Folder paths, parents
and children are looked up through an index built once per folder list, so a tree of
thousands costs a map lookup per row rather than a scan of the list. The upload queue
resolves each folder in a dropped path through `GET /api/folders/{id}/children`,
caching names for one run of the queue, instead of re-reading the whole tree for every
segment of every file.

React Router keeps pages in the URL. Links, breadcrumbs, browser Back/Forward,
and reload reopen the addressed view. The main routes are:

| URL | View |
| --- | --- |
| `/directory/:id` | Folder contents |
| `/directory/:id/permissions` | Group grants, individual exceptions, inheritance |
| `/documents/:id/:tab` | Preview, tags, metadata, versions, comments, activity |
| `/search` | Authorized filename, text, vector and tag results |
| `/admin/users` and `/admin/users/:id` | People list and account details |
| `/admin/groups` and `/admin/groups/:id` | Groups list and membership details |
| `/checkouts` | My checkouts; `scope=all` selects management view |
| `/trash` and `/trash/:id` | Deleted folder trees and retained contents |
| `/tags` | Tag catalog and administrative enrichment controls |
| `/profile` | My profile and appearance |
| `/login/callback` | Where the WVDOT sign-in round trip lands, before any session exists |
| `/docs/usage` | High-level end-user guide; default Docs page |
| `/docs/business-logic` | In-depth frontend and backend behavior reference |
| `/docs/frontend/change-log` | Frontend change log |
| `/docs/backend/change-log` | Backend change log |
| `/docs/client/change-log` | Windows client change log |

Document versions, comparisons, page selection, search scopes, history, tags,
directory sorting/pagination and People filters use query parameters where those
controls exist. `returnTo` names the page a document was opened from; the document is drawn over that
page, which stays mounted, and closing returns to it.
Dialog drafts and uploads in progress are temporary interface state.

### Window and pane layout

Dock is a shell, not a document: the window itself does not scroll. The sidebar has
always been fixed with its own overflow, and the main pane matches it, so both agree
where the bottom of the screen is. Long pages — the docs, the audit log, the tag
catalog — scroll inside the main pane beneath the sticky top bar.

A folder listing is a pane rather than a page. The listing card fills the space left
under the folder heading and scrolls its own rows, with the folder toolbar and the
column headings staying put. Previously the table grew to fit its contents and pushed
the page past the bottom of the window: seventeen rows overflowed a 900px screen by
510px, and a full page of a hundred would have run to roughly six thousand. Because
the card fills the pane whatever the folder holds, its bottom edge sits in the same
place every time and the area accepting dropped files is the whole pane rather than
just the occupied rows.

The documents, my-checkouts and managed-checkouts views mark themselves as panes with
a class. An earlier attempt matched `:has(.directory-surface)` in the stylesheet
instead; that is declarative but the sidebar tree and the listing are both large, and
invalidating that selector across them on every change made interaction several times
slower and destabilised a browser check. Anything reading scroll position must observe
the pane that actually scrolls rather than the window — the docs outline resolves its
nearest scrolling ancestor for that reason.

The shell itself uses `overflow: clip`, not `hidden`. A hidden overflow can still be
scrolled programmatically, and focusing something at the shell's end — the hidden file
inputs sit there — scrolled it and lifted the top bar by about 21px until a reload. A
clipped box is not a scroll container, so nothing can move it. The listing's footer
("Showing N of M files", **Load more**) and its end-of-list sentinel sit inside the
scrolling card, so the card still ends within the window.

### Sidebar, New and the folder header

The sidebar opens with the logo, then **New**, the Workspace links, the folder tree and
the Administration panel. Exactly one item is lit: the tree row of the folder being
viewed, or **Documents** only when that folder is not in the tree. On a phone the
sidebar is a drawer over a backdrop that closes it when tapped.

**New** is enabled on a folder page when the list is not showing archived files and
`canUpload` holds for the folder: not navigation-only, and a role of editor or above.
Its menu offers New folder, Upload files, Upload folder and Upload with comment; the
upload items reuse the hidden file inputs and the upload dialog. Elsewhere it is
disabled with the tooltip "Open a folder you can add to". At 700px and below the
sidebar button is hidden and a floating button named **New** opens the same menu; it
is not rendered where nothing can be added or while a document is open, and the
upload tray sits above it.

A folder page has no separate title: the breadcrumb is the title. Ancestors are links
and drop targets as before; the current folder is an `h1` whose only content is a
link marked `aria-current="page"`, so the heading's name is exactly the folder's. On a
phone the path collapses to its first and last two folders. The ▾ **Folder actions**
button beside the name lists what the account may do to the folder being viewed and is
not drawn when nothing applies:

| Item | Shown when |
| --- | --- |
| New folder | editor or above, not showing archived files, not navigation-only |
| Upload files, Upload folder | the same test as **New** |
| Download as ZIP | the folder is not navigation-only |
| Folder settings | controller or above |
| Manage access | an administrator or an account that can manage access; opens `/directory/{id}/permissions` |

A folder moves from its parent's listing or through **Parent folder** in Folder
settings, so the menu has no Move item. The checkout views use the shared page header:
one breadcrumb row (Dock › Checkouts), the title and one line of explanation, and their
toolbar reads "Checked-out files".

The listing uses a fixed table layout with set column widths, so columns keep their
places from folder to folder; a long name ends in an ellipsis and shows in full on
hover. Folder rows leave version, size and updated blank and say **Shared path** only
for a navigation-only folder. Row checkboxes are transparent until the row is hovered,
focused or selected, or anything is selected — they keep their place and name — and
are always shown on phones. A file's icon follows its MIME type or extension: PDF,
image, spreadsheet, drawing, archive, email, word processing or text. An empty listing
shows one empty state instead of an empty table. The toolbar's counts come from
`plural()` and the server's `total`, and are hidden while the listing reloads.

The search field is one rounded box: its magnifier is the submit button, Enter
searches, Escape or the × clears it, and it stays the textbox **Search documents**,
disabled for auditors. The page-wide error banner clears whenever the path changes,
so an error does not follow the person to an unrelated page.

### Page headers, empty states and errors

Every page but the folder listing and Docs draws the shared `PageHeader`: chevron
breadcrumbs, the title as the page's only `h1`, one line of explanation and the page's
main action at the right. Section and card titles are `h2`. The shell no longer adds a
generic "Dock / page" crumb. Empty lists use `EmptyState` (icon, title, hint), and
first loads use `LoadingState` placeholder rows. Trash, Tags, the Tagging pipeline and
the search filters report failures through the page-wide banner rather than boxes of
their own; a dialog still shows its own error.

Search filters apply as they change: scope, history, facets and dates live in the
address, so changing one searches again and there is no Apply button. The count reads
"1 result"; a hit mentions its index state only while its text is still being read.

People & access puts **Add person** and **New group** in the header, sizes the filters
equally, capitalises roles and uses two-letter initials. **Add member**, **Add to group**
and **Add an owner** add on choosing — the same `PUT` endpoints as before, without a second
button. Removal is an icon button whose accessible name keeps the old wording ("Remove
pw9", "Remove Bridge A viewers"). Deleting a group or an access list confirms in a dialog
whose button is **Delete now**; an access list is deleted outside the reloading helper,
which would otherwise ask for the list it had just removed. An access list's page is
titled and crumbed with the list's name.

The access editor's **Permission set** control is bordered, **No access** is a checkbox,
and Effective access uses a typed person picker. Profile aligns with other pages and
shows a folder's role only where it differs from the account's. Docs puts contents and
article on one surface, shows section links on hover and scrolls its page switcher
sideways on phones. Sign-in focuses nothing at rest.

### Documents over the listing

A document route (`/documents/:id/:tab`) no longer replaces the page it was opened from.
`App` reads the background address from `returnTo`, checked by `safeReturn` and never
another document; without one it uses the document's own folder once `onLoaded` reports
it, and the root folder until then. The folder, view, sort, archive switch, search terms
and search filters are all read from that background address, so the listing, its
cursor, selection and scroll position stay exactly as they were: opening, stepping and
closing fetch nothing for the listing, and `DocumentPanel.onChange` refreshes it quietly.
The document renders in `DocumentOverlay` — fixed at z-index 70, `role="dialog"` with
`aria-modal`, labelled by the document's title — while the sidebar and main pane are
`inert` and `aria-hidden`. The upload tray and MUI dialogs sit above it.

Escape closes, unless focus is in a text field or a menu or dialog is open. On the
Preview tab the left and right arrow keys, and **Previous file** / **Next file**, step
through the listing's documents, or the search results; stepping replaces the history
entry, so Back leaves the document. Closing pushes the background address and returns
focus to that document's link. Links, tabs and **Download current** keep their
`/documents/...` addresses.

### Grid view

The listing toggle (**List view** / **Grid view**) is stored in `localStorage` as
`dock.listing.view`; list is the default. `DirectoryGrid` shows folders, then files, as
tiles over the same entries as the table — `directoryEntries` holds `useEntries`,
`useEntrySelection`, `dropIntent`, `readInternal` and `EntryMenu` for both — so click,
Shift and Ctrl/Command selection, dragging, dropping onto folder tiles, the actions menu
and end-of-list loading behave the same. It is a `listbox` named **Directory contents**
with multi-select options; the arrow keys move by the columns drawn, measured with a
`ResizeObserver`, and cross between the folders and the files.

### Bottom sidebar panel

Administration defaults to a compact button anchored below the independently scrolling
folder tree. Clicking opens a popover above the button; outside clicks, Escape and
link selection dismiss it. Keep expanded renders its links inline at the bottom;
clicking the expanded header collapses it. The expanded preference is stored in
browser localStorage per user ID and survives reload; storage failures fall back to
in-memory behavior. Popup visibility is transient. Expanded links scroll within a
bounded panel on short screens, preserving the bottom control and folder navigation.

Audit log, Permissions and People & groups retain their session-derived visibility.
Trash, Tags and Docs are available in the same panel to all signed-in users, labeled
Workspace tools for accounts without audit access. Links retain their existing URLs
and active-page indicators; mobile link selection closes navigation. Preferences
never grant capabilities. Backend authorization and navigation contracts are unchanged.

### Sessions and visible actions

The sign-in screen precedes application views and offers exactly one action: sign in
with a WVDOT account. Dock has no password of its own, so when the identity broker is
not configured the screen says so rather than offering a control that can only fail;
`GET /api/auth/methods` is read on each mount, so enabling the broker needs no rebuild.

Signing in is a full page navigation to `/api/auth/sso/login`, not a fetch: the broker
answers with a redirect the browser has to follow. The current path and query travel
as `redirect`, so a deep link is restored afterwards. A refused round trip returns to
`/?sso_error=<code>`; `src/ssoErrors.ts` maps those codes to sentences and mirrors
`backend/pw_store/sso.py`, with an unrecognised code falling back to a generic failure.

`/login/callback` is handled inside the authentication guard rather than the view
router, because the guard replaces the whole application while there is no session. It
trades the one-time code for a session over POST and then navigates to the stored
destination. The exchange is latched behind a ref: React mounts effects twice in
development and the code is single use, so a second attempt would report a failure that
did not happen.

After that nothing about the session differs from before. The server identifies the
user through an HttpOnly session cookie; mutation requests include the CSRF token. A
401 clears application session state and returns to sign-in — except on `/api/auth/*`,
where a refusal is that attempt failing rather than a session ending. The profile menu
provides account details, appearance and sign-out. Sign-out ends the Dock session only:
the broker publishes no `end_session_endpoint`, so the upstream WVDOT session is
untouched and signing in again often completes without a prompt.

The UI exposes actions according to the current user's capabilities. This is an
affordance, not authorization: every protected operation is checked again by the API
and database. Auditors see metadata and logs, with content controls unavailable.
Managers see scoped permission and checkout controls. Global account/group management
is administrator-only.

Routed content sits inside an error boundary, `src/ErrorBoundary.tsx`. A render error
shows a notice with **Try again** and **Reload** in place of the page, logs the error
and component stack to the console, and leaves the navigation usable; changing page
resets it. While a folder's documents load, the listing shows placeholder rows,
announced as "Loading folder", instead of the empty-folder message. Destructive
confirmations are in-page dialogs, never `window.confirm`; switching off access
control for an account is one.

### Directory uploads

Users with edit access can upload multiple files or select a folder, or drop files
and folders onto the current directory, a folder row, or a sidebar folder. Import
preserves relative paths; directory drops preserve empty directories too. Imports
create new document identities and do not replace a matching filename automatically.

The upload queue captures the destination folder, displays per-item progress and
errors, and retries failed items with their existing idempotency identities. Saved
items remain saved. Navigating immediately before choosing files must use the new
folder as the destination. Every browser upload — dropped files, **Upload files**, **Upload
folder**, **Upload with comment** and check-in — goes through `src/transfer.ts`. Files
up to 250 MiB are sent in one request. Larger files, up to
20 GiB, are first read and hashed in the browser (the tray shows **Checking file**),
then reserved with that hash and sent as ordered parts of `part_size` bytes. A failed
part is retried up to three times with backoff; a 409 re-reads the session and follows
its `next_part`; **Retry failed** re-hashes the file and resumes from the last part the
server holds, because the retried reservation reuses the idempotency key. Files above
20 GiB are rejected before anything is sent. The upload dialog shows the same phases and keeps its
idempotency key in `sessionStorage` per file, so a retry, or a reload of the same tab,
resumes the same session. The browser hashes with the
incremental implementation in `src/sha256.ts`, because `crypto.subtle.digest` accepts
only a whole buffer; it is checked against Node's `crypto` at every padding boundary
and past 512 MiB, where the 64-bit length's high word first becomes non-zero.

The queue sends up to eight items at once. A file above the single-request limit is
read through and sent in parts, so at most one of those is in flight while smaller
files continue on the other lanes. Files bound for the same folder share one
children listing, and each folder path is created once however many files wait on
it; a 409 re-reads the parent, since someone else may have created it first. The
tray redraws at most every 100 ms and shows one progress bar for the whole queue,
weighted by bytes: finished files count in full, files being sent by their progress
and a large file's hashing pass not at all. While files finish, the listing
refreshes at most once every 15 seconds and once more when the queue goes idle.
Each of these refreshes is quiet: it asks for as many rows as are loaded, keeps them
on screen until the new ones arrive and shows no error for a missed refresh. The
folder tree is fetched again only if the upload created folders, and the listing
reloads when the folder being viewed changes, not whenever the tree does. The server already takes these in
parallel: content and part requests wait for one of `PW_UPLOAD_CONCURRENCY` slots
(8 per API process) rather than failing, and the upload pipeline shares the write
fence. One browser's eight lanes can fill those slots, so a second person's uploads
wait for a free one rather than failing.

The page does not hold the upload list. `ImportQueue` keeps its counts and byte
totals as items change state - one `transition` function is the only place a state
changes - and publishes a frozen `UploadSnapshot` at most every 100 ms: totals,
failures, bytes, whether work remains, an estimate of the time left, and at most 100
`rows`. The rows are what is sending, then failures, then the most recently finished
(newest first), then the next to start. The tray reads the snapshot with
`useSyncExternalStore`, so a 15,000-file upload draws a hundred rows and re-renders
only the tray. The next file comes from two first-in-first-out index queues, small
files and files above the single-request limit, taking whichever head was added first
and the large one only when no large file is in flight: the order a scan from the start
would find, at constant cost. `retry()` and `dismiss()` rebuild those queues. The time
left is taken from the last 20 seconds of progress once 5 have passed, as the slower of
the byte rate and the file rate. Sign-out and the before-unload warning ask the queue
whether it `hasWork`.

The queue is in memory: keep the tab open until transfers complete. Sign-out is
blocked during active transfers. Use **Upload with comment** for a custom initial
comment; directory imports use **Initial upload**.

### Moving items and downloading folders

Folder rows, sidebar folders and breadcrumb ancestors accept two kinds of drop. A drag
from the desktop carries `Files` and uploads, as described under Directory uploads. A
drag of a row inside Dock carries `application/x-dock-entries` — JSON
`{version: 1, sourceFolderId, items: [{kind, id, name, revision}]}` — plus a plain-text
list of names as a fallback outside Dock. Every handler branches on the type, so
neither can be taken for the other.

The listing keeps a selection of `kind:id` keys over its rendered order, folders
first and then documents. A click replaces the selection; Shift-click extends it from
the anchor, the last row chosen; Ctrl- or Command-click and the row checkboxes toggle
one row; the heading checkbox selects or clears everything listed; Escape clears.
Rows use a roving `tabindex`, so exactly one row is in the tab order: arrow keys,
Home and End move focus, adding Shift extends the range from the anchor, Space
toggles, Enter opens, Ctrl/Command+A selects all listed rows, and Shift+F10 or the
ContextMenu key opens the actions menu against the row. Keys are handled only when the
row itself has focus, so the name link and checkbox keep their own Enter and Space. A
polite live region announces the count. The selection is cleared when the folder, the
view or the Show archived switch changes, and after a move or archive completes. The
focused index is clamped to the listing, which shrinks when rows move out.

A right-click, or a row's **Actions** button, opens one menu: for the whole selection
when the row belongs to it, otherwise for that row alone. It offers Open, Download for
a single document (an anchor to the download endpoint), Download as ZIP for a single
folder, Move to… and Archive (documents only) when rows in the current folder are
draggable, and Folder settings for a single folder the account controls. The selection
bar that replaces the folder summary in `.document-toolbar` offers the same actions.
Dragging a selected row carries the whole selection. **Archive** asks for confirmation,
then posts `POST /api/documents/{id}/archive` per document and reports how many
succeeded; a checked-out document refuses.

Rows are draggable when the account's resolved role for the current folder is
administrator, manager or controller, the presets that include deleting documents
there and Write on folders; see Folder moves for when a folder move also needs Change
permissions. A target accepts a move only if it would accept an upload, is not an item being
dragged, and is not the folder the items are already in. The current folder's crumb
carries `aria-current="page"` and is never a target. Browsers expose only a drag's
types during `dragover`, so hover feedback reads the payload from a module-level slot
set at `dragstart`; the drop reads only its own `DataTransfer`, which is what lets a
synthesised drop in a browser check perform a real move.

Moves go to `POST /api/moves` in batches of up to 200 items: a destination and
`{kind, id, revision}` per item. The whole request is one write transaction, so it
takes the write fence once rather than once per item. Each item runs in its own
savepoint under exactly the checks its single-item endpoint applies —
`check_document_move` (Delete here, Create there, no checkout) and
`check_folder_move` (Write on the folder, then Create subfolders or, when access
would change, Change permissions at both ends), shared with `PATCH /api/documents/{id}`
and `PATCH /api/folders/{id}` so the two paths cannot drift. A refused item is rolled
back to its savepoint and reported with the status and message its single request
would have had, while the rest commit; database refusals map exactly as the global
handler maps them. Each refusal is also written as an `access.denied` event on the
audit connection, as a refused single request is, because the bulk response itself is
a 200. A destination the account cannot see refuses the whole request with 404. The
client retries each item refused with 409 once, with the revision the server now
holds, and a second failure is reported by name and reason. The confirmation distinguishes all moved, some moved and
none moved. The confirmation offers **Undo**, which moves only the items that actually
moved back to the folder they came from, with the revisions the first move returned.
Undo is an ordinary move under the same rules, so it can fail and say why. **Move to…**
chooses the destination with the folder picker, leaving out the source folder, the
folders being moved and navigation-only folders.

Every folder chooser is `src/FolderPicker.tsx`: Move to…, the search scope, a
document's **Folder** field, **Parent folder** in Folder settings, the audit log's
**Folder subtree** and the Access page's folder chooser. It is an autocomplete over
`GET /api/folders/search`, debounced by 250 ms and limited to 50 results labelled by
`path_names`. These choosers used to render a menu item per folder of the whole tree.
A preset value is labelled from `GET /api/folders/{id}/path`. Each caller narrows the
results to what it can use, and the server still authorises the action: the document
Folder field offers folders that accept uploads, the Access chooser offers folders the
account manages, and Parent folder offers any folder but the one being edited, with
the move rule applied on save. The Access chooser navigates inside the app, so it
keeps the `/dock` prefix; before, it set `window.location` to a root-relative path.

A folder row's actions menu offers **Download as ZIP**. The dialog reads
`GET /api/folders/{id}/download-preview`, shows the file count, total bytes and the
number withheld, states that the transfer cannot be paused or resumed, and offers no
download over the configured limits. The confirm control is an anchor to
`GET /api/folders/{id}/download`, not a fetch, so the browser owns the transfer and no
archive is buffered in the page.

### Controlled edits and history

Check-in comments are optional for uploads, updates and restored versions. The API
accepts an omitted `comment` or an empty string and normalizes whitespace-only values
to `""`; nonempty values are trimmed. The 4000-character input limit and NUL rejection
still apply. Migration 0019 permits empty comments in upload sessions and immutable
version records without rewriting existing comments or changing their NOT NULL
contract. Both clients allow submitting a blank comment. Discussion comments and
force-release reasons retain their separate nonblank requirements.

Opening a document uses a dedicated page. Editors check out, download, edit locally,
then check in an updated file with an optional comment. Ownership, cancellation,
force release and conflict errors come from the backend. Committed versions remain
available to authorized readers while a file is checked out.

Metadata editing uses the document revision for optimistic concurrency. Version
history supports older downloads and restoration as a new version. Comparisons show
extracted text and metadata snapshots; they are not visual CAD/PDF differences.
Preview, extraction and semantic indexing statuses are shown independently. Unsupported
or incomplete extraction must not be represented as complete.

### Access editing

**People & groups** provides searchable lists and dedicated user, group and access-list
detail pages. Account, group and list edits use explicit saves. Membership actions take
effect through the API; effective-access displays identify the boundary folder and every
contributing assignment.

The access editor at `/directory/:folderId/permissions` presents one folder at a time.
It renders entirely from `GET /api/permissions`, so the permission vocabulary, the
implication rules and the named presets are never restated in client code and cannot
drift from the database.

- Rows are principals; columns are permissions. The two permission sets are separate
  tabs over the same rows, because a principal is one thing to the person editing even
  though the sets are stored independently. A row contributes to a set only when it
  grants something there.
- Ticking a permission also ticks whatever it requires; clearing one clears anything
  that only required it. Implied permissions render distinctly and name what requires
  them. The client applies the closure for display, and the database applies it again
  on write, so a hand-made request cannot store an inconsistent set.
- Presets stamp a known pattern and revert to Custom on any change off-pattern.
- **No access** is a per-principal checkbox at the end of the row that writes a denial
  into both sets and disables the row's other boxes. It is presented as categorically different from an empty row.
- Saves are whole-set and carry `acl_revision`; a concurrent edit returns 409 and the
  editor reloads rather than merging silently.

The lineage strip draws the chain of ancestors, marking which folder supplies access and
whether it flows or is only a path. While a folder inherits, its inherited assignments
are shown read-only and identified as belonging to the folder above.

Because any assignment makes a folder a boundary, the editor copies the inherited set in
as soon as the first principal is added, and says that it has. A warning naming the
affected principals appears only when a pending save would actually remove access from
someone, and offers to carry the inherited set forward again.

**Effective access** asks the server rather than recomputing: the client has neither the
group closure nor the account layer, and a second implementation would be a second answer.
It shows saved state and says so plainly while edits are pending. The person is chosen
from a typed picker that matches employee numbers and names, not a menu of every account.

The UI must not suggest that adding a group membership can bypass a denial or an
inheritance boundary, or that clearing permissions is equivalent to No access.

### Trash and archived files

Managers delete a complete folder tree from Folder settings. **Delete folder** turns the
dialog into a confirmation step from `GET /api/folders/{id}/deletion-preview`: folder and
document counts, any blocking checkouts, **Delete now** and **Keep folder**. Deletion moves the tree to Trash.
Trash supports browsing retained metadata and restoring the tree — from its row, or from
the page of a tree deleted as a whole; a folder inside a deleted tree comes back with it — with a different
name or active destination when needed. Independently archived content stays archived.
The UI provides no permanent deletion. Individually archived files remain a separate
document-control workflow; restoring a deleted containing tree is required first.

### Search and automatic tags

Search results come from authorized backend retrieval, not browser-side permission
filtering. Folder, historical-version and tag filters are reflected in the URL.
Results label versions, snippets, page references and indexing status.

The Tags tab shows a generated summary, categorized labels, source/evidence, and
available page references. Editors can add manual labels, dismiss labels, and request
regeneration. Manual labels and dismissals survive regeneration. The catalog links
to tag-filtered search. Administrators can rename/merge labels and pause, retry or
backfill enrichment. Pending, failed and partial analysis are visibly distinct.


## Backend business logic

### Runtime and data ownership

Local development uses `./dev`: a native FastAPI backend, Vite frontend and dedicated
native Postgres 17 database with pgvector. The embedded service and `cli worker` run
independent extraction, embedding, enrichment and artifact-import stages with bounded
shared connection pools. One local parser handles routine uploads; optional OCI jobs
provide burst extraction capacity. App ports are API 8081, frontend 5174 and database
5546, bound locally.
Integration tests use an independent native test database on 5547.

Application settings use the `PW_` prefix. Migrations and runtime connections must
target `pw_store`. Dock does not load FOIA settings, records or embeddings and has
no runtime dependency on the FOIA checkout. Source adaptations are documented in
the repository provenance documents.

| Schema | Responsibility |
| --- | --- |
| `auth` | Users, sessions, roles, groups and group membership |
| `dms` | Folder hierarchy/grants, documents, immutable versions, checkouts, uploads, comments |
| `search` | Index generations/jobs, extracted pages/chunks, vectors, enrichment jobs, tags and corrections |
| `audit` | Application access and change events |

Documents have stable identities independent of their content hashes. Identical
files in separate folders remain distinct documents. A version records its author,
timestamp, check-in comment, metadata snapshot, hash, byte count and exact OCI object
reference. Foreign keys prevent cross-document version and enrichment references.

### Server deployment and copied data

The mmsdev server uses a Docker image built by root `Dockerfile` and `build.sh`;
local development remains native through `./dev`. The image builds the frontend
with `VITE_BASE_PATH=/dock/`. Host Apache serves the extracted immutable build
release and proxies `/dock/api/` to the loopback Docker API on port 8087. SPA
fallback preserves nested routes. The API uses `PW_PUBLIC_BASE_PATH=/dock`, the
HTTPS origin, Secure cookies scoped to `/dock`, and its embedded background worker.
The build script runs additive database migrations in a temporary container using
private maintenance configuration before replacing the API container. It checks
API/database health before publishing frontend assets and
retains the previous container for rollback if a replacement fails to start.

The server has a separate `pw_store` database in the local PostgreSQL 16 Docker
service also used by Instant. The service adds pgvector 0.8.2; Instant retains its
existing database. Dock on the developer workstation uses PostgreSQL 17. All five
Dock database roles remain separate. Migration 0013 grants
only the dedicated `pw_migrate` owner an explicit policy on RLS tables, so existing
SECURITY DEFINER functions also work without superuser or BYPASSRLS privileges.
Runtime startup rejects membership in `pw_migrate`, including NOINHERIT membership;
the runtime roles’ authorization policies and non-owner restrictions remain unchanged.

Initial migration copies all application schemas and data from a consistent local
snapshot, preserving IDs, users, grants, versions, audit history, jobs, vectors and
exact OCI references. Database changes then evolve independently. The same OCI
runtime and maintenance identities and original/derived/operations buckets are
retained; secrets are transferred outside the image and source control. Only the
runtime OCI identity is mounted into the app container. No bucket is provisioned
and original objects are not recopied. Do not run abandoned-upload reconciliation
against either database independently while shared object references can diverge;
cleanup requires checking both databases. No automatic cleanup service is deployed.

### Authentication and request identity

Dock is a relying party of the WVDOT identity broker at
`https://ocidev.transportation.wv.gov/auth`, which fronts the Entra/SAML identity
provider and speaks OpenID Connect. Dock speaks OIDC to the broker and never touches
SAML. **Dock holds no password material of any kind**: there is no password column, no
password endpoint, and no way to present one. Demo mode still seeds ten accounts, now
keyed on employee numbers `pw1`–`pw10`; seeding does not reset existing accounts or
permissions.

Everything downstream of sign-in is unchanged. Sessions remain server-side, expire
after eight hours, use an HttpOnly `pw_session` cookie paired with a readable
`pw_csrf`, and are invalidated by logout. Mutations require the CSRF token and an
exact `Origin` match. Account edits invalidate that user's sessions. Only the proof of
identity in front of `auth.create_session` has changed.

**Configuration.** `PW_OIDC_ENABLED`, `PW_OIDC_ISSUER`, `PW_OIDC_DISCOVERY_URL`,
`PW_OIDC_CLIENT_ID`, `PW_OIDC_CLIENT_SECRET`, `PW_OIDC_REDIRECT_URI`,
`PW_OIDC_SCOPES`, `PW_OIDC_AUTO_PROVISION`, `PW_OIDC_PROVISION_ROLE` and
`PW_OIDC_HTTP_TIMEOUT`. `Settings.oidc_configured` is true only when the broker is
enabled *and* client id, secret, redirect URI and discovery URL are all present, so a
half-filled environment cannot render a sign-in control that can only fail — and with
no password path there is nothing for it to fall back to. The settings loader ignores
unknown variable names silently, so a test asserts the documented names actually bind.
`PW_OIDC_REDIRECT_URI` is validated to be an absolute `https` URL, or `http` on
loopback for development, with no query or fragment.

**Endpoints are never hard-coded.** `pw_store/oidc.py` reads the authorize, token and
JWKS addresses from the discovery document and caches it for an hour, so nothing
breaks if the broker moves one.

**The round trip.** Three routes carry it, and the web app and the Windows client use
the same three:

| Route | Behavior |
| --- | --- |
| `GET /api/auth/methods` | Whether sign-in is available, read per request |
| `GET /api/auth/sso/login` | Records `state` and `nonce`, redirects to the broker |
| `GET /api/auth/sso/callback` | Verifies state, exchanges the code, resolves the account, redirects on with a one-time handoff code |
| `POST /api/auth/sso/exchange` | Trades the handoff code for the Dock session cookie |

`auth.sso_login_states` holds `state` and `nonce` across the round trip. They cannot
live in a cookie: the web app authenticates with a cookie it cannot read, the Windows
client has no browser session at all, and the broker is on another host. The row then
carries the one-time handoff code. `state` and the handoff code are stored as SHA-256
hashes, as `auth.sessions.token_hash` and `csrf_hash` are — no live credential is ever
written down.

**Single use is enforced in the database, not in Python.** `auth.sso_claim` and
`auth.sso_redeem` are each one `UPDATE … RETURNING` guarded on the unspent state and
its expiry, so a replayed callback finds nothing rather than racing another request.
A state is good for ten minutes and a handoff code for sixty seconds. Unknown,
replayed and expired are one indistinguishable failure. Abandoned rows are swept
opportunistically when the next sign-in starts; there is no scheduler.

**The handoff code exists so the session credential never enters a URL.** A callback is
a browser redirect: its address is written to history and can leak in a `Referer`.
Redirecting with a one-time code instead, and setting the cookie on the subsequent
same-site POST, also means the cookies keep `SameSite=strict` unchanged. Responses
already carry `Referrer-Policy: no-referrer`.

**Validating the identity token** is non-negotiable and all of it happens in
`oidc.validate_id_token`: RS256 signature against the broker's JWKS matching the
token's `kid`, exact issuer, audience equal to the client id, unexpired with a sane
`iat`, and a nonce equal to the one issued. PyJWT performs the first four; the nonce
comparison is Dock's, because PyJWT has no notion of one. Signature verification is
never skipped on the grounds that the network is internal.

**Broker properties Dock is built around.** Authorization codes are single use and
expire in about sixty seconds, so the exchange runs inline in the callback and a code
is never stored. A `redirect_uri` mismatch consumes the code before the comparison, so
a misconfigured URI produces one hard failure per attempt rather than a retryable
error, and `redirect_uri` must match the registered value byte for byte. There are no
refresh tokens and broker tokens live fifteen minutes; they are validated, read and
discarded, and Dock manages its own session afterwards. The broker publishes one
signing key with no rotation overlap. It sends no CORS headers and answers `OPTIONS`
with 405, so the token exchange is necessarily server-side; there is no PKCE and the
client secret stays on the server.

**Claims.** `sub` is the employee number — the Windows account name — unique and
immutable, and the key a Dock account hangs off. `name` and `preferred_username` are
emitted together and only when the directory supplied a name, so neither can be the
only source of anything Dock relies on; `sub` is the fallback. `email` may be absent.
The broker's own `users` table is a refresh-on-login cache that never learns of
departures, and nothing here reads it.

**Resolving an identity to an account.** `auth.sso_identify` matches on `upper(subject)`
first. Failing that it adopts a row an administrator primed — one whose `username` is
the employee number and whose `subject` is still null — so setting an account up ahead
of a first sign-in lands on *that* row with its access, rather than duplicating it. A
`DOMAIN\` prefix is stripped; a partial unique index on `upper(subject)` prevents a
second row for one person. An inactive account is refused *before* the row is touched,
so a rejected attempt cannot move `last_login_at`.

Sign-in refreshes only what the directory owns: `display_name`, `email`,
`first_login_at`, `last_login_at`. It never writes `global_role`, `capabilities`,
`use_access_control` or any ACL row. Rewriting those on each sign-in is precisely what
would undo an administrator's setup.

**Provisioning is a decision, and the current one is provisional.** Clearing Entra
proves someone is a state employee, which is not the same as being authorized for
Dock. With `PW_OIDC_AUTO_PROVISION` on, an unknown employee number is created with
`PW_OIDC_PROVISION_ROLE`, which currently defaults to `administrator` so that a fresh
deployment has someone who can grant access at all. **That is more than a first
sign-in should carry and is expected to be narrowed before wider rollout**; because it
is a setting rather than a constant, tightening it — to an empty role, or to refusing
unknown identities outright — is a configuration change. Provisioning is recorded in
the audit log as `authentication.provisioned`.

**Accounts are created by employee number.** `POST /api/users` is administrator-only
and calls `auth.create_user`, which re-checks `auth.global_role()` itself. It exists
because access has to be arrangeable before a first sign-in; without it, an
administrator could prepare nothing.

**An account that predates single sign-on has no employee number**, and nothing can
sign in to one that has none — only a first sign-in fills it in, and only for an
account whose username already happens to be that employee number. `PUT
/api/users/{id}/subject` calls `auth.set_subject` so an administrator can attach one,
and the groups, access lists and folder permissions already arranged for that account
follow the person rather than being rebuilt around a new one. It is administrator-only
and **one way**: it refuses an account that already has an employee number, and
refuses one already in use, both as `23505` and so `409` to the caller. Moving an
employee number between accounts would hand over everything the first account can
reach, which is not something a form should be able to do; it is a deliberate
database operation with a reason recorded elsewhere. Attaching one invalidates that
account's sessions, because its identity changed.

**Database privileges are unchanged in shape.** `pw_api` holds no table privileges in
the `auth` schema. Every identity operation — `sso_begin`, `sso_claim`, `sso_identify`,
`sso_handoff`, `sso_redeem`, `create_user`, `create_session`, `session_info`,
`user_names`, `update_user` — is a `SECURITY DEFINER` function with `search_path`
pinned to `pg_catalog`, revoked from `PUBLIC` and granted explicitly. `sso_redeem`
returns the account with the spent code for the same reason: the API role cannot read
`auth.users`. `auth.sso_login_states` is granted to no runtime role at all, like
`auth.users` and `auth.sessions`.

**Unauthenticated routes.** The access middleware skips the session lookup and the
CSRF comparison for the four sign-in routes, but still builds a request context so a
refused attempt is audited — `separate_event` writes through the append-only audit
connection with a null actor, which is required because there is no session yet and
the audit policy demands `actor_id = auth.uid()`. The `Origin` equality check still
applies to the exchange, the only mutating route among them; the Windows client sends
a matching `Origin` already.

**Failures never explain more than they should.** `SsoError` carries a machine code
that both the web app and the Windows client turn into a sentence; the underlying
reason is logged server-side. Discovery, token-endpoint and validation failures are
distinguishable in the log and deliberately not to the caller beyond the sentence.

Every pooled transaction clears the previous identity and identifies the current
authenticated session transaction-locally. Runtime roles are neither table owners
nor superusers/BYPASSRLS accounts. API, worker, audit and migration responsibilities
use separate database roles. Protected metadata, content and related records use RLS.

### Access control

There is one Directory root and no project permission layer. Access is expressed as
independent permission sets, not as an ordinal role ladder.

**Two vocabularies.** Folder permissions describe the container: `folder.read`,
`folder.write`, `folder.create_subfolder`, `folder.delete`, `folder.change_permissions`.
Document permissions describe its contents: `doc.read`, `doc.write`, `doc.file_read`,
`doc.file_write`, `doc.create`, `doc.delete`, `doc.free`, `doc.comment`, `doc.audit`,
`doc.change_permissions`. `doc.change_state` is declared and reserved; Dock has no
workflow model, so it is never granted or enforced. The catalog lives in
`auth.permission_bits` with the presets in `auth.permission_presets`, and is served by
`GET /api/permissions`.

Both sets are stored as integer masks. `auth.close_mask` applies the implications:
`doc.write`, `doc.file_read` and `doc.comment` each require `doc.read`; `doc.file_write`
requires `doc.read` and `doc.file_read`; every folder permission requires `folder.read`.
`doc.file_write` deliberately does not imply `doc.write` — maintaining metadata and
editing file content are separate capabilities, and that separation is the point of the
model.

**Assignments.** `dms.acl_entries` holds one row per (object, permission set, principal).
Exactly one object — a folder or a document — and exactly one principal — a user, a group
or an access list — per row, enforced by check constraints. `target` is `folder` for the
folder's own set, `documents` for the default applied to documents inside it, and
`document` for an individual document's own set. `no_access` denies and cannot carry
permissions.

**Principals.** `auth.groups` collects users. `auth.access_lists` nests users, groups and
other access lists, with a trigger rejecting any nesting that would make a list its own
ancestor. `auth.principals_of(user)` returns the transitive closure and is `STABLE`, so
Postgres evaluates it once per statement. `auth.principal_owners` delegates membership
management: an owner may change who belongs to a group or list and receives none of its
access.

**Inheritance.** A folder with any assignment of its own is a boundary and stops
inheriting; otherwise the nearest such ancestor supplies the set. `break_inheritance`
seals a folder that has no assignments, so it inherits nothing. The rule does not depend
on who is asking, so the boundary is materialized per folder and per set in
`dms.folders.folder_acl_source` and `document_acl_source`, maintained by triggers on
folder insert, move and inheritance changes and on assignments appearing or disappearing.
The cache is a cache: `test_final_invariants` recomputes it from scratch and requires
equality. The two sets carry independent boundaries, so a folder defining only document
permissions still inherits its own folder permissions.

**Resolution**, in `auth.access_mask(folder, user, set)` and `auth.document_mask`:

1. An inactive account resolves to nothing.
2. A global administrator receives every permission. An auditor receives `folder.read`,
   `doc.read` and `doc.audit` — metadata and log access, never file content, previews or
   content search.
3. An account with `use_access_control` off bypasses object security entirely.
4. Otherwise, at the boundary, every assignment naming any of the account's principals
   applies. **Any applicable No access denies outright.** Otherwise the masks are
   combined with `bit_or`: permissions accumulate across every group and list, and an
   unticked permission is not a denial. Removing access is expressed with No access.
5. A document carrying its own assignments is its own boundary, overriding the document
   security it would otherwise inherit.
6. An owner of the folder, or of an ancestor up to the nearest sealed folder, gains
   `folder.change_permissions`. Ownership is assigned deliberately and is never a
   by-product of creating a folder, which would let anyone who can add a subfolder grant
   themselves access inside it.
7. The account's own capability mask is applied last and only ever narrows the result.

**Enforcement.** `auth.can(folder, action)` and `auth.document_can(document, action)`
remain the only authorization predicates, so every RLS policy, trigger and API call site
resolves through the same engine. `auth.action_map` translates a requested action into
the bits that satisfy it and carries the archived-folder and archived-document guards.
It also keeps the previous verbs — `meta`, `read`, `comment`, `edit`, `control`, `manage`,
`audit`, `force` — answering as unions of the precise permissions, so the Windows client's
capability checks and any unmigrated caller behave as before. Policies and call sites name
precise permissions; `dms.check_document_change` decides which change a document update
actually made, because a row policy cannot distinguish a rename from a check-in.

Checkout requires `doc.read`, `doc.file_read` and `doc.file_write`; the implication rules
make the triple follow from File Write alone. Releasing another person's checkout requires
`doc.free` and the account's Free capability. Only minimal ancestor navigation is returned
for users granted access deep in the tree; hidden siblings and their counts must not leak,
and a folder where the person is denied is not revealed by that path. Changing access
requires `folder.change_permissions` on the object, enforced by the row policies on
`dms.acl_entries` rather than by the API alone. Only administrators manage global roles,
accounts, group and list definitions, and account capabilities. Permission and membership
changes affect subsequent requests and pending finalization, not merely new logins.

**Account settings.** `auth.users.capabilities` gates create documents, create versions,
modify documents, delete documents, free documents, and create, modify and delete folders.
It intersects after resolution and never widens. `auth.users.use_access_control` bypasses
object security for the account; it is administrator-only, audited under its own action
name, and confirmed in the UI before it is set.

### Folder moves

Moving a folder needs **Write** on it — which the row policy on `dms.folders` enforces
for every update — and **Create subfolders** at the destination, provided the move
leaves access unchanged. It changes access when the folder is not sealed and either
inherits a permission set whose boundary differs at the destination, or would come
under a different set of owners: the owners whose authority reaches a folder, from
the deepest sealed ancestor down, gain Change permissions inside it. A sealed folder,
or one defining its own security for both sets, carries them unchanged.
`dms.move_changes_access(folder, destination)` makes that judgement against the tree as
it stands before the move. A move that changes access is a permission change and
needs **Change permissions** on the folder, on every folder in the moved subtree and at
the destination, exactly as every move did before migration 0031. The API and
`dms.check_folder_tree` both apply the rule, so a request made directly as the API's
database role meets it too. Descendants move with the folder: a manager can relocate a
folder that contains a sealed subfolder they cannot see, because moving it changes no
one's access to it. Controllers and managers can therefore reorganise folders within
one area of access; editors, who hold no folder Write, cannot. Document moves keep
their Delete-here, Create-there rule.

### Upload and check-in transactions

Uploads use reservation, content transfer and finalization endpoints. New uploads
reserve an unpublished document identity. Existing-document uploads must identify
the checkout owner, unpredictable token and starting version. Reservation/finalization
idempotency prevents duplicate versions after retries.

The API streams to bounded temporary disk, enforces `PW_SINGLE_PUT_LIMIT` (250 MiB), computes SHA-256,
and creates a unique OCI original object with checksum verification. It does not
treat ETag as SHA-256. Database transactions do not remain open during file transfer
or embedding calls.

Finalization freshly checks permissions, locks and validates the checkout/current
version, verifies the object reference, inserts the next immutable version, advances
the current pointer, releases the checkout, writes the event and queues indexing in
one short transaction. Failure must preserve the previous committed version. OCI
success followed by database failure leaves an unpublished upload that can be retried.

### Large uploads in parts

Migration 0028 raises the database checks on `dms.document_versions.byte_count` and
`dms.upload_sessions.expected_bytes` to 20 GiB (`PW_UPLOAD_LIMIT`, 21,474,836,480
bytes), adds `declared_sha256`, `part_size`, `multipart_upload_id`, `received_bytes`
and `next_part` to upload sessions, and adds `dms.upload_parts`, one append-only row
per accepted part. A session either declares the part protocol completely or not at
all.

A reservation carrying `sha256`, the whole-file SHA-256, uses the part protocol and
may declare up to `PW_UPLOAD_LIMIT`. One without it uses the single-request path and
is limited to `PW_SINGLE_PUT_LIMIT` (250 MiB), which is also the `upload_limit`
reported to the Windows client, so an installed client is never told it may send a
file the proxy would refuse partway through. An empty file must use the
single-request path. The session view carries `protocol`, `part_size`
(`PW_UPLOAD_PART_SIZE`, 16 MiB), `next_part` and `received_bytes` — what a
reconnecting client needs to resume. The idempotency fingerprint omits `sha256` when
it is absent, so a body an installed client sent before the field existed still
matches on retry.

`PUT /api/upload-sessions/{id}/parts/{n}` accepts only part `next_part`; any other
number is a 409 and the client re-reads the session. Every part is exactly
`part_size` bytes except the last. The request leases the session, streams the part to
a temporary file no larger than one part, relays it with its MD5 to the OCI multipart
upload — created on the first part with the declared hash as `opc-meta-sha256` and
`If-None-Match: *` — records it in `dms.upload_parts` and advances `next_part`. Each
part renews the lease, so no heartbeat is needed, and no transaction is open while
bytes move. At most `PW_UPLOAD_CONCURRENCY` (8) parts are received at once, and a part
is refused with 503 when free temporary space is below one part plus 16 MiB. Part
requests write no `access.start` row — a 20 GiB file is 1,280 parts — while
`upload.start` and `upload.verified` record the upload.

The API hashes the parts it relays, in order, in process memory.
`POST /api/upload-sessions/{id}/complete` requires every byte to have arrived. If the
running hash differs from the declared one, the multipart upload is aborted, the part
rows are discarded and the upload restarts from part 1: nothing is committed.
Otherwise it commits create-only and checks the committed object's length and
`opc-meta-sha256`. If the process restarted during the upload the running hash is
lost; the remaining parts still upload, and completion reads the committed object
back once and hashes it before marking the session verified, leaving it unverified and
unpublished on a mismatch. Either way `dms.document_versions.sha256` is a hash the
server computed over the stored bytes. The existing finalize transaction then
publishes the version unchanged.

A multipart object does not get the whole-object `Content-MD5` check a single PUT gets
twice. OCI's per-part MD5, the committed length, the declared hash and the server's own
SHA-256 replace it. The declared hash has to exist before any byte is sent because OCI
fixes an object's metadata when the multipart upload is created, which is why the
browser hashes the file first. The runtime identity has no delete permission, so an
abort it attempts can fail; abandoned multipart uploads are left for the maintenance
identity.

**Deployment prerequisite.** Against the development tenancy, `CreateMultipartUpload`
is refused with `404 BucketNotFound` under the runtime identity's policy, which grants
only `OBJECT_CREATE`, `OBJECT_READ` and `OBJECT_INSPECT` on the originals bucket; single
PUTs succeed under the same policy. Until that policy is extended, a file above
250 MiB cannot be stored there: its first part fails with 503 and nothing is committed.
The opt-in browser check `e2e/large-upload.spec.ts` (`DOCK_REAL_OCI=1`) exercises this
path against the real bucket. No policy has been changed.

Oracle's permission reference requires `OBJECT_CREATE` and `OBJECT_OVERWRITE` for
`CreateMultipartUpload` and `UploadPart`, and `BUCKET_READ`, `OBJECT_CREATE`,
`OBJECT_READ` and `OBJECT_OVERWRITE` for `CommitMultipartUpload`. `OBJECT_OVERWRITE` is
exactly the permission the runtime identity was denied so that it can never replace an
original. Granting it moves the create-only guarantee from IAM into the application,
which sends `If-None-Match: *` on every create and commit; bucket versioning would still
retain any version an overwrite displaced, since the runtime identity cannot delete
versions. A narrower statement conditioned on `request.operation` for the three
multipart operations may confine the grant: Oracle documents that variable for every
request but gives no Object Storage example, so it must be tested in the tenancy before
it is relied on.

### Checkout, metadata and restoration

Exactly one checkout can exist per document. Concurrent requests produce one winner;
conflicts return 409. Checkouts persist across logout and restarts and do not expire
automatically. Owners can cancel; managers/administrators can force release with a
reason. Released tokens cannot finalize an old upload.

Restoring an older file requires a checkout and creates a new version with a source
reference; it never rewinds history. It copies the source version through temporary
disk and a single PUT, so a version above `PW_SINGLE_PUT_LIMIT` (250 MiB) is refused
with 409 and the advice to download it and check it in as a new version. Metadata changes use `If-Match` revision checks,
record before/after values, and do not create binary versions. Active checkouts block
document move/archive and relevant folder-tree operations.

### Folder deletion and Trash

Tree deletion requires management rights throughout the subtree and no active
checkouts. Scope mutations and document commits serialize through the write fence
(see Write fence). Root deletion, stale revisions, cycles and invalid destinations
are rejected.

Deletion marks previously active descendants and files with a shared trash batch.
Versions, OCI references, grants and logs are retained. Restore is performed on the
deleted batch root into an active managed destination outside that tree. A name
collision rolls back the operation; a different name/destination can be supplied.
Only items in that batch are restored, so independently archived items stay archived.
Deleted folder edits and creation beneath a deleted parent are rejected. The UI has
no permanent deletion operation.

### Write fence

Every write transaction takes a transaction-scoped advisory lock, `(809173, 2)`,
before anything else. Its purpose is narrow: a mutation checks permission early and
commits later, and a permission change must not commit in between. The upload
pipeline — reserving a session, sending its content or parts, completing and
finalizing — takes the fence shared (`tx(ctx, "shared")`), so uploads and check-ins
run beside one another while each still waits for, and holds off, an exclusive
holder. Every other write takes it exclusively, as all writes did before: every
permission change (access entries, owners, presets, accounts and groups) and every
folder move, rename or trash among them. The database takes the fence itself in only
three places — `dms.check_folder_tree` on any folder row change other than its
ancestry cache, `dms.trash_tree` and `search.queue_facet_refresh`. A shared holder that
reached one of them would have to upgrade to exclusive, and two such upgrades
deadlock, so shared mode is confined to transactions that touch sessions, parts,
documents and versions and never those. `test_mutation_fence.py` proves the three
properties: an upload proceeds while another holds the fence shared, an owner
assignment waits for an in-flight upload, and an upload waits while the fence is held
exclusively. The desktop manifest reads under the shared fence too.

### Storage and recovery

Private OCI originals, derived and operations buckets reside in the configured
AIDevelopment compartment in Ashburn. Credentials stay on the backend. Files and
previews pass through the API; v1 does not provide public/pre-authenticated file links.
Folder archives stream through the API the same way.
Originals use opaque unique version keys and create-only writes. Renaming or moving
metadata does not move stored originals. OCI originals-bucket versioning supplements
the authoritative application history.

Maintenance uses a separate identity for backups, audit exports and reconciliation.
Abandoned unpublished uploads are eligible for cleanup after 24 hours, with database
state rechecked before deletion. Runtime identities cannot overwrite/delete originals.
Backup recovery must verify exact referenced OCI versions and file hashes.

### Tree ancestry and per-statement authorization

`dms.folders.path` (migration 0027) is the ancestor chain from the root including the
folder itself, so `path[1]` is the root and the last element is the folder's own id,
enforced by `folder_path_ends_at_self`. `dms.check_folder_tree` sets it on insert and
on a parent change; the `folder_ancestry` AFTER trigger re-roots every descendant by
replacing the old prefix. Triggers of one timing fire alphabetically, so paths are
correct before `folder_boundary` refreshes ACL sources. `path` and `updated_at` are
deliberately outside the tree trigger's early-exit tuple: maintaining the cache bumps
no revision and repeats no authorization. `updated_at` is new; folders that existed
before the migration carry the migration time.

`auth.in_subtree(f, ancestor)` keeps its signature and meaning — true when `f` is
`ancestor` or beneath it — and is now one indexed lookup. The move trigger's cycle,
checkout and subtree-permission checks, `dms.tree_info` and `dms.trash_tree` use
`path @> ARRAY[f]` as a set predicate. Search, the audit folder filter and the
security export still call `auth.in_subtree`, which is now cheap. `auth.owns_folder`
probes the owner index first and then slices `path` at the deepest sealed ancestor,
reproducing the rule that ownership stops at a sealed folder.

`auth.principal_closure` (migration 0029) caches each account's transitive groups and
access lists. Triggers on `auth.group_members` rebuild the affected account, triggers
on `auth.access_list_members` rebuild every account because a list can nest groups and
other lists, and a trigger on `auth.users` seeds new accounts. `auth.principals_of`
reads the table; `auth.principals_of_live` keeps the recursive definition that builds
it and proves it. Because triggers maintain it, a membership change is visible to the
next statement in the same transaction.

The folder read policy is `auth.can(id,'folder.read') OR id IN (SELECT
auth.navigable_folder_ids())`, and the set is computed once per statement: folders
named in a non-denying, non-empty assignment for one of the account's principals that
resolve to `folder.read`, together with each one's ancestors. The seed stays "named and
readable" rather than "readable" so that owning a folder does not reveal its
ancestors, and descendants are never added, because a folder beneath a reachable one
may carry its own No access. `auth.navigate` answers from the same set and
`auth.navigate_reference` keeps the previous body as its oracle. `auth.has_management()`
is true for administrators, accounts with access control switched off, owners of an
active folder, and accounts holding an assignment that grants
`folder.change_permissions` at an active boundary; it no longer scans every folder.

`auth.folder_masks()` (migration 0030) returns both resolved masks for every folder for
the current account in one pass, reproducing `auth.access_mask`: a denial wins before
ownership adds anything, a folder with no boundary can still gain Change permissions
through ownership, and a zero mask stays zero. `auth.folder_ids_for_action(a)` is the
set of folders where `auth.can(f, a)` holds. The document read policy is
`folder_id IN (SELECT auth.folder_ids_for_action('doc.read'))` plus the existing
unpublished-draft rule; document insert and update stay per row, since they touch one
row. `auth.authorized_document_ids(action)`, behind the search content policies and
folder archives, joins documents to their folder's masks and resolves only documents
carrying their own entries through `auth.document_mask`. Its previous body is kept as
`auth.authorized_document_ids_reference`.

`auth.can` and `auth.document_can` are unchanged and remain the definition of access.
`test_final_invariants.py` recomputes `path` and the principal closure from scratch,
compares `auth.in_subtree` with the recursive walk for every pair of folders,
`auth.navigate` with its reference for every account and folder, both masks with
`auth.access_mask` for every account and folder, the folder sets with `auth.can` for
every action, and the document sets with the reference for every account and document
action, including a per-document exception.

Measured with `scripts/scale_fixture.py` and `scripts/scale_bench.py` on 14,944
folders, 100,000 documents and 200 boundary folders — database time only, best of
three:

| Query | Account | Before | After | Changed by |
| --- | --- | --- | --- | --- |
| `GET /api/folders` | scoped | over 60 s (timed out) | 0.48 s | 0029 |
| `GET /api/folders`, 14,944 rows | administrator | — | 0.39 s | 0029 |
| Document listing in a 60,000-document folder | scoped | 1.71 s | 0.02 s | 0030 |
| `authorized_document_ids('doc.file_read')` | scoped | 6.34 s | 0.06 s | 0030 |
| `authorized_document_ids('doc.file_read')`, 100,000 rows | administrator | 1.68 s | 0.07 s | 0030 |
| Folder archive manifest, 60,615-document subtree | scoped | 6.83 s | 0.18 s | 0030 |
| Folder archive manifest, 60,615-document subtree | administrator | 5.76 s | 3.12 s | 0030 |
| `has_management()`, every `GET /api/session` | any | scan of every folder | 1.3 ms | 0029 |

The administrator's manifest figure counts the whole subtree; the endpoint stops at
`PW_ARCHIVE_MAX_FILES` + 1. Listings still compute `auth.effective_role` per row and
still return the whole folder tree, and document listings still page by offset, which
costs 0.6–0.7 s at offset 5,000 in the largest folder. Keyset paging and a lazily
loaded tree are not implemented yet.

Renaming or moving a folder changes the context the tagger reads. The
`folder_enrichment` trigger now records the folder once in
`search.folder_reindex_queue` instead of inserting an enrichment row for every
document beneath it inside the request. When no index job is waiting, the worker calls
`search.expand_folder_reindex(500)`, a SECURITY DEFINER function that claims one queued
subtree, enqueues its next 500 documents in id order, advances the cursor and removes
the entry once the subtree is exhausted. The worker holds no read privilege on
`dms.folders`.

### Document downloads

`GET /api/documents/{id}/download` advertises `Accept-Ranges: bytes` and an `ETag` equal
to the version's quoted SHA-256 — a strong validator, since a version never changes. A
single byte range, open-ended or suffix ranges included, is answered with 206 and
`Content-Range`, streamed with a ranged `get_object`. Several ranges, a malformed
header, or an `If-Range` that does not match the `ETag` get the whole file with 200; a
range starting past the end gets 416 with `Content-Range: bytes */size`.
`X-Content-SHA256` always describes the whole object. Every request, partial or not,
writes its own `download.start` and `transfer.end`, so a resumed download appears in
the log as several transfers.

### Folder tree endpoints

`GET /api/folders/{id}/children` returns one page of a folder's direct, non-archived
children in `lower(name), id` order, each with `has_children`, paged by an opaque cursor
that carries Postgres's own `lower(name)`; an invalid cursor is 422.
`GET /api/folders/{id}/path` returns the chain from the root, and
`GET /api/folders/search?q=` matches names case-insensitively, with `%` and `_` escaped,
returning each match's `path_names`. All three read through the folder read policy: a
folder the caller cannot see is 404, `has_children` counts only visible children, and a
path through navigation-only ancestors appears as the sidebar shows it. The whole-tree
`GET /api/folders` remains.

### Folder document pages

`GET /api/folders/{id}/documents` lists a folder's documents a page at a time —
`{items, next_cursor, total}`, 100 by default and at most 500. It sorts by `updated_at`
or by `lower(name)`, either direction, with the document id as the tie-break in the
same direction. `next_cursor` encodes the order and the last row's key and id; the
next page asks for rows strictly after that pair, with a redundant bound on the sort
key alone so the `(folder_id, updated_at DESC)` and `(folder_id, lower(name), id)`
indexes seek straight to it. A deep page therefore costs what the first does: on
the 100,000-document fixture, 5,000 rows into a folder of 33,336, 53 ms against
661 ms by offset for an administrator. A cursor used with another order, or one that
does not decode, is refused with 400. `total` counts the folder's current documents
whose records the account can read; it can include a document a per-document rule
hides from the list, since the list also needs the current version to be readable.
The folder's role is resolved once per request, not per row. Archived documents page
separately and only for an account with Delete in the folder.

The web listing uses this endpoint. The first page loads with the folder; the next is
appended when a sentinel after the last row comes within 600px of the listing card's
bottom edge — an `IntersectionObserver` rooted at the card, observed again after each
page — or on **Load more**. "Showing N of M files" and **Load more** sit in the card's
footer. `appendInFlight` holds the cursor being fetched, so the sentinel and the
button never ask for the same page twice, and a reload that replaces the list clears
the cursor and total first, so a folder switch cannot append the previous folder's
next page. The checkout
views stay on `GET /api/documents`, which keeps its offset paging for them and for
existing callers; they are short, and there **Load more** asks for the next offset.

### Folder archives

`GET /api/folders/{id}/download-preview` and `GET /api/folders/{id}/download` require
`folder.read` on the folder and resolve the archive in one read transaction: every
non-archived document in the non-archived subtree whose current version the caller may
read, through `auth.authorized_document_ids('doc.file_read')`, ordered by relative path
and name and limited to `PW_ARCHIVE_MAX_FILES` + 1. The transaction closes before any
byte is sent. `withheld` counts only documents the caller can see but not read;
documents hidden by row security are never counted, because the count would disclose a
denied folder's contents.

Entries are stored, with ZIP64 records and data descriptors. Local headers,
descriptors and central-directory entries have fixed sizes, so the exact
`Content-Length` is known before streaming. Relative paths start at the requested
folder, replace characters Windows rejects, strip trailing dots and spaces, prefix
reserved device names, cap segment and total length, and de-duplicate equal names in a
folder as `name (2).ext`, since Dock allows equal filenames in one folder. If an object
cannot be read after streaming has begun, that entry is padded to its declared length
so the archive stays well formed; extraction reports that one file's CRC.

Above `PW_ARCHIVE_MAX_FILES` (5,000) or `PW_ARCHIVE_MAX_BYTES` (25 GiB) the download
returns 413 with the counts and names a subfolder as the remedy; an empty result
returns 404. At most `PW_ARCHIVE_CONCURRENCY` (2) archives stream at once and a further
request returns 503. The slot is a `threading.BoundedSemaphore`, because Starlette
drives the synchronous generator on a worker thread and the release in its `finally`
runs there. One `download.folder` event records the file count, bytes and withheld
count; the middleware records `access.start` and `transfer.end` for the `/download`
path as it does for documents. No per-document `download.start` is written.

### Cloud extraction and regional model capacity

The stage-aware queue has a unique `(generation_id, kind)` pair: `extract` publishes
pages/chunks and queues `embed`; embedding failure cannot roll back committed text.
Migration 0033 transfers already committed text to embedding jobs and revokes old
monolithic claims. Stop old workers before migrating. One local parser, sixteen embedding
loops, twelve enrichment loops and two artifact importers share a twelve-connection
pool; the fleet API uses four connections and model admission another shared four.
`PW_EMBED_WORKERS` (default 16) and `PW_TAG_WORKERS` (default 12) each allow 1–64
consumers; regional permits remain shared across every consumer/process. Increasing
consumers does not increase database pool limits or CPU cloud readers.
`PW_WORKER_CONCURRENCY` is retained for configuration compatibility but no longer
multiplies these stage services. API identity/audit pools retain their separate roles.

Cloud execution is off by default (`local`). Administrators select `auto` after a
validated release and OCI job are configured. The controller targets one run per eight
queued files, up to the normal limit (64), or up to the maximum (128) when at least
10,000 files wait. Each E6 Flex run defaults to one OCPU, 8 GiB RAM, 50 GiB disk and a
six-hour lifetime. Runs claim one file at a time and exit after two idle minutes.
Creation intents and OCI retry tokens are persisted before launch. A PostgreSQL
session advisory lock elects one controller; creation is limited to four concurrent
requests. Accepted, starting, cancelling and uncertain launches remain counted until
OCI reports a terminal state. Uncertain launch requests older than the retry window
are retained for operator reconciliation, never blindly replaced. Explicit first
request refusals can be canceled locally without stranding capacity; a prior timeout
remains uncertain. OCI creation-limit/429 responses pause new launches and retries
for one minute while healthy runs continue. Late-discovered OCI runs remain subject
to reconciliation and cancellation even after an absent intent was resolved locally. Three failed starts
without a heartbeat within fifteen minutes suspend new run creation until the window
clears; the frontend displays that backoff and sanitized launch errors. Dock runs use
a dedicated private VCN/subnet with NAT and an OCI service gateway. Network IAM is
scoped to the dedicated Dock compartment; shared Dashcam networks are unchanged.

`/api/workers/*` requires a hashed run-scoped bearer credential and worker ID, checked
before dispatch; human sessions do not authorize these routes. Workers have no database
credentials. The controller encrypts stored launch credentials and the exact OCI launch request using the host's
`PW_FLEET_CONTROLLER_KEY`; this key is never in the image or bundled documentation.
On mmsdev the deployment script maintains a dedicated restartable controller container
with a separate protected environment file; the API receives only the nonsecret Job ID.
The controller key is not copied into the API environment.
Resource principals read originals/releases and write immutable derived artifacts.
The parser child receives a sanitized environment, a local file and extraction limits;
the supervisor retains service credentials. This is process separation, not a sandbox
against a malicious administrator-authored release. Linux parsers enforce a 6 GiB
address-space limit, 256 MiB per-output limit, and bounded file descriptors. Parser
process groups are terminated on cancellation/deadline. Original downloads verify
version, length and SHA-256; result imports verify compressed SHA-256/size, expanded
size, page ordering and exact source-span coverage without forcing one chunk size.

Claim requests retry transport failures, HTTP 429 and server errors for up to two
minutes, allowing warm workers to survive brief API restarts; other client errors
fail promptly. Extraction leases last three minutes and renew every ten seconds. Lost leases and
release epochs fence publication. Completed remote manifests are idempotent and enter
an `importing` stage; two importers publish database rows. At 256 pending/importing
results remote claims stop until import catches up. Pausing result import also stops
new cloud claims. Existing downloads and published search data remain available.

Worker releases are immutable, content-addressed Python ZIPs paired with an OCIR image
digest. The release stores `image:tag@sha256:digest`; OCI receives the tagged image and
digest in their separate API fields. An untagged repository is insufficient for BYOC startup. Publishing does not activate a release. Validation runs representative fixtures
for every supported format before activation. Activation increments the fleet epoch,
revokes unfinished extraction/import claims and requeues them without consuming a
failure attempt. Running supervisors download the new release and start a fresh parser;
a changed runtime image replaces runs while retaining the same OCI Job definition.
An earlier validated release can be activated to roll back. The supervisor uses the locked HTTPX client; the image build imports both entrypoints
to catch missing runtime dependencies. Diagnostics include exception types, not document
contents or credentials. The supervisor and installed dependencies themselves require an image rebuild. `deploy/workers` contains the build
and operations instructions. No source-control or OCI private key is copied into an image.

Regional inference admission uses database permits shared across server processes.
Embedding allows Ashburn and Chicago with the same Cohere Embed v4 identity and
1,024-dimensional validation; Phoenix embedding is deliberately absent after a real
inference request returned 404 despite catalog availability. Gemini 2.5 Flash permits
Ashburn, Chicago and Phoenix. Additional regions remain disabled until live compatibility
validation and administrator enablement. Migration 0036 raises unchanged initial budgets using tenancy limits verified on
2026-09-11: embedding has eight concurrent calls per region, 470 background RPM in
Ashburn and 970 in Chicago; chat has four concurrent calls, 500 RPM and 100,000 TPM
per region. The embedding totals including the interactive reserve are 500/1,000 RPM.
Custom operator budgets and region enablement are preserved. These are ceilings,
not promised throughput: OCI can dynamically throttle below its listed limits. Interactive embedding has one
reserved concurrent lane and 30 requests per minute. Reservations expire after 150
seconds, longer than the inference request timeout. No database transaction spans
inference. Each server thread reuses its regional OCI client, signer and keep-alive
connections; SDK sessions are never shared across threads. Restart server workers
after rotating OCI config or signing keys. Chat reserves UTF-8 input bytes plus maximum output before dispatch; a
successful response settles the reservation to OCI `usage.total_tokens`, including
reasoning usage reported by the provider. Missing/invalid usage or a failed request
retains its reservation. Settlement locks the endpoint like admission does; a larger
reported total increases recorded usage and blocks further calls until capacity returns.
The fleet API/UI reports background calls and active lanes against their limits, plus
actual/reserved tokens across all lanes, over the rolling minute. Provider throttling/failure cools that endpoint and allows a different
compatible region; exhausted capacity defers work without consuming its retry budget.
Regional enrichment uses 8,000-character sections with full-body coverage to leave
room for schema, Unicode input and output in the budget. Summary consolidation uses
the same cap and marks truncation partial. A request larger than every enabled
region’s token budget fails promptly instead of waiting forever; oversized verification
falls back to grounded, unscored facts. Oversized context requires operator correction.
Background calls wait up to 75 seconds for a regional permit before deferring, so a
multi-step analysis can retain its work while the minute budget replenishes.
Independent enrichment heartbeats maintain its lease during this wait; interactive
search embeddings do not wait for background capacity. Controller log permissions
are restricted to the dedicated Dock log-group OCID, and regional chat IAM grants
name only the configured Gemini model IDs. Only extracted text for model calls crosses regions; CPU extraction and originals stay
in Ashburn. Summaries continue through the separate bounded enrichment service.

Legacy DOC uses headless LibreOffice with a fresh profile, macros disabled and Writer
link updates disabled, then the DOCX reader. MSG reads headers/body and explicitly
marks omitted attachments incomplete. XLS reads cached cell values with xlrd and marks
formula/embedded-object limitations incomplete. Originals are never changed. An explicit `worker_release retry-legacy` operation
queues current unsupported DOC/MSG/XLS versions in batches of at most 5,000, preserving
the published generation and avoiding duplicates where a newer generation exists. The
container includes LibreOffice and Tesseract; native development needs these executables
for DOC conversion and scanned-PDF OCR. Unavailable converters or malformed files fail
explicitly rather than publishing a misleading complete result.

### Extraction and search

Extraction downloads the whole original to temporary disk before parsing it, so a file
larger than `PW_EXTRACTION_MAX_BYTES` (1 GiB) is never fetched for indexing: it is marked
**unsupported** with the reason "Too large to index", and metadata search and download
remain available. The page preview fetches the whole original too, inside the request,
so above `PW_PREVIEW_MAX_BYTES` (1 GiB) `GET /api/documents/{id}/preview` answers 413
without fetching anything and the page offers the download instead.

Chunk and chunk-vector RLS resolve authorized document IDs once per statement
using the existing `auth.document_can` checks, then filter their rows by that set.
Metadata, page and document-vector lookups retain per-document checks so opening
one document does not scan the full corpus. This avoids repeating folder and role lookups for every chunk while
retaining exact permission, archive and publication rules. The set is not cached
across requests, so later requests see changed grants and memberships.

Derived extraction filenames include a SHA-256 of their compressed JSON bytes within the
existing version/generation folder. Retries on different platforms can preserve
different OCR outputs without overwriting a shared OCI object. The generation
records the exact successful key; existing keys remain valid. Original file
checksums, create-only writes and publication fencing remain enforced.

Supported extraction includes PDF, DOCX, XLSX, EML, TXT, CSV, DOC, MSG and XLS, with local OCR for
scanned PDFs. Other formats retain metadata/download support with explicit unsupported
content status. Extraction has configured safety limits; incomplete results must be
labeled. Chunks preserve extracted body ranges rather than silently sampling away
long-document content.

Indexing is asynchronous and version/generation-specific. New versions are usable
for download and metadata search immediately. Text and semantic statuses are separate.
Leases, retry handling and publication checks prevent an old job replacing a newer
active generation. File usability must not depend on successful embedding.

Retrieval combines filename, English/identifier lexical and cosine vector branches
using reciprocal rank fusion. OCI Cohere Embed 4 vectors must have 1,024 dimensions.
Each candidate branch enforces current permissions in SQL/RLS before returning
snippets, counts or content. Query embeddings are cached per user. Current versions
are the default; history explicitly includes labeled older versions. Filtered vector
retrieval uses iterative HNSW scans with exact fallback for underfilled results.

### Automatic tagging and human corrections

Independent enrichment jobs use OCI Gemini 2.5 Flash after extraction. Extractor
version 3 adapts FOIA's catalog metadata and facet fields: document types, distinctive
topics, people, organizations, roads, counties, districts, other locations, typed
identifiers (permit/contract/project/claim/po/other), and content dates. Existing tag
categories and IDs remain compatible; assignment JSON carries the more specific kind.
The provider sees page-aware sections covering the full extracted body, with overlap
at split pages. Untrusted document text and metadata never become instructions.

`facets.EXTRACTOR_VERSION` is the single definition of the interpretation version. It is
stamped when a job is claimed, when a superseded job is requeued and when results are
published, and it keys the road-lookup cache and `search.queue_facet_refresh()`. Those
values must never diverge: a function selecting a version published rows never reach
would re-queue the entire corpus on every backfill.

Version 3 adds a closed `discipline` vocabulary, cross-section corroboration, a
verification pass, the decision ledger and the catalog vector. Existing version-2
analyses remain published and are not re-processed automatically. There is no
startup backfill; only an administrator's **Tag existing documents** queues them,
while newly uploaded or changed documents claim version 3 immediately.

Disciplines are validated against a fixed list rather than accepted as written, because
a discipline is an axis people filter on and open-ended values fragment it. Topics are
rejected when every word is a corpus-wide generic term, and any label is rejected when
its shape is a sentence rather than a facet.

Automatic facts require a nonblank supporting quotation on the cited source page;
validation tolerates whitespace/case differences. Invalid individual model items
(such as a date missing its page citation) are omitted while other validated facts
remain usable, with partial status. Malformed JSON or an invalid root object still
fails the job and retains the previous active results. Filename, folder and metadata
suggestions must match their declared source and are stored separately from searchable
tags. County hints must occur in the same supporting passage as the road. Dates retain
YYYY, YYYY-MM or YYYY-MM-DD precision and original evidence; validated bounds use the
beginning/end of the stated period. Invalid dates are discarded. Upload times and
request exclusions are not document-date facts. Summaries remain generated descriptions.

#### Corroboration, verification and the decision ledger

Section results are merged on the catalog identity returned by `search.ensure_tag`, not
on the model's spelling: "WV 51" and "West Virginia Route 51" are one tag, so support
counted per spelling would not match what is published. Repeated appearances increment
a support count; losing spellings are recorded as accepted with reason `merged`.

A verification pass then reads the whole grounded candidate set and assigns each fact a
salience of primary, supporting or incidental, plus a confidence. Corroboration raises
that confidence by five percent per additional section, capped at four extra sections
and at 0.99, and never lowers it. Verification may only demote or reject; it cannot
restore a fact that failed its citation check, because the citation is verified against
stored page text and a model opinion is not evidence.

Verification is not a precondition for publication. Provider failures propagate so the
existing cooldown and attempt refund apply; any other failure publishes the grounded
facts unscored and records reason `verification_unavailable`. Such a run does **not**
mark the analysis partial: every grounded fact is still published and only the score is
missing, whereas partial states that source content could not be analyzed. A run whose
verification failed does not reset the provider failure counter, so a breaker can still
trip when only that call is failing.

`search.tag_decisions` records every proposed fact per enrichment as accepted, suggested
or rejected, with a reason from a fixed vocabulary, its page, quotation, support count,
confidence and salience. Rows are written in one statement inside the publishing
transaction. Ledger rows for a published analysis are retained; rows belonging to an
analysis that is no longer active are pruned after ninety days by idle worker
maintenance, bounded per pass. Retention keys on `active`, not on status, because
publication deactivates the previous analysis without changing its status. Read access
follows the document's own read permission.

#### Pipeline visibility

`search.index_generations` and `search.enrichments` carry advisory `stage`, page and
section counters and a `progress_at` timestamp. These are display state only;
`text_status`, `enrichments.status` and `lease_until` remain authoritative. Progress is
written best-effort in short transactions, guarded by a short lock timeout and a fence
that prevents a late write from resurrecting a finished stage. A failure to record
progress never fails a job. Extraction reports pages through a callback that performs no
I/O; the existing heartbeat thread publishes it, on a separate transaction from the lease
so a blocked display write can never delay the lease.

Whether work is live is decided by the same lease predicate the reclaimers use, so the
view and the queue cannot disagree: a claimed row whose lease is current is working, and
one whose lease has expired is stalled and awaiting reclaim. Stage and page counters are
meaningful only for a live row. Reclaiming resets them so an abandoned job stops
advertising the page it died on.

`GET /api/pipeline` requires the administrator role and is served by
`search.pipeline_status()`, a security-definer function that enforces the role itself and
raises `42501` otherwise. Corpus-wide counts run inside that function so they do not pay
a per-row permission check over every generation, and they exclude superseded history so
the cost does not grow with the number of times documents have been re-analyzed.
`GET /api/documents/{id}/decisions` returns one document's ledger under ordinary
row-level security.

Enrichments store extractor version, source generation, date bounds and structured
date/context evidence. Jobs retain claim tokens, leases, retries and context/version
checks; publication also rejects a changed extraction generation. Version-aware startup
backfill queues existing current documents without duplicating pending work or successful
version-2 results. Failed jobs use the retry control. Prior active results remain visible
until successful atomic replacement. A changed extraction generation queues a fresh
job instead of publishing stale facts. Historical versions are not bulk reprocessed.

Provider service failures (429/5xx, transport timeouts, or an open OCI circuit breaker)
put the claimed job back into pending without consuming its attempt budget. A shared
persisted enrichment-control cooldown backs off from one to fifteen minutes across
workers. Successful publication resets the cooldown; the admin catalog exposes its
retry time and sanitized exception type. Validation/content failures retain per-document
bounded retries. Pausing remains independent of the provider cooldown.

#### Road resolution and review

The backend uses explicitly configured `PW_FUZZYROAD_URL` and `PW_FUZZYROAD_KEY`,
sending only extracted road mentions and evidence-supported county hints. The key is
private runtime configuration; it is neither bundled into the frontend nor logged.
The FOIA checkout is a development reference, not a runtime configuration dependency.
The client calls `/health` (two-second timeout) and `/gazetteer` (four seconds), requests
three candidates, and bounds responses. API failures retain the original tag.

Returned route IDs, counties, scores, names, aliases and milepost spans remain attached
to the document fact. Repeated IDs are deduplicated. Exact route IDs may resolve directly;
otherwise the best score must be at least 80 and lead the next distinct ID by eight
points. Ties remain ambiguous, including high-scoring mainline/turn-lane candidates.
No automatic catalog merge follows a shared road name. Structured street-name objects
retain their segment spans; only supported spans participate in identity expansion.

The worker-only lookup cache expires successful/ambiguous responses after seven days
and unavailable/unmatched responses after fifteen minutes. Unavailable assignments retry
in the background without language-model or extraction work; compare-and-swap publication
protects concurrent regeneration and manual review. Ambiguity requires editor review or
regeneration. Review accepts only a route ID in the server's existing protected candidate
list and persists the chosen association as a manual tag. Audits record tag and route IDs,
not keys, lookup text or provider payloads.

#### Search and compatibility

`POST /api/search` accepts up to 30 `tag_ids` plus the legacy `tag_id`; IDs are deduplicated
and every selected facet is required on the returned document version. Normalized route
spellings and tracking numbers retain existing canonical IDs and aliases. Road aliases
can additionally match through equal resolved route IDs with overlapping supported
milepost ranges. A manual association overrides the automatic association for that tag.
Authorized effective assignments are materialized once per search to compute matching
versions. All retrieval branches enforce those facet/date conditions and their own
current RLS checks before ranking and limiting results.

Optional `date_start` and `date_end` select inclusive overlap with an active enrichment's
content range; unknown document dates do not match an active date filter. Reversed search
ranges return 422. Empty text permits filter-only searches. Search selections use repeated
`tag` URL parameters plus `date_start`/`date_end`, preserving navigation and old links.
Existing filename, PostgreSQL English/identifier text ranking and HNSW vectors remain;
this is not BM25 or a FOIA responsiveness classifier.

#### Ranking branches and weights

Retrieval fuses six branches with weighted reciprocal rank fusion. Filename, text and
exact-tag branches are gated by a predicate, so a top-ranked row is a real match. The
two vector branches have no relevance predicate and always return a full page of rows,
and they are correlated because both score the same query vector from the same model.
Equal weights would therefore let two floor-ranked vector rows outrank the best filename
match in the corpus and would count one signal twice. Weights are configuration
(`PW_RRF_*`), not literals, so ranking can be tuned without a deployment. The catalog
branch carries the lowest weight of the pair because its input is generated text with no
citation to check. Exact identifier matches additionally receive a flat anchor bonus,
which rank position alone cannot express.

Branch order determines the displayed snippet: a row carrying a snippet replaces one
without, and the grounded branches are fused before the generated ones so a model-written
summary never displaces a page-cited quotation. Results report which branches found them.

The tag branch matches the normalized tag key, the identifier core and a whole-word
trigram similarity, each as its own indexed probe. `search.identifier_core` returns an
empty string when a label has no long digit run, so comparisons must reject the empty
value; without that guard every identifier lacking a digit run would match every query
lacking one. The trigram tier is bounded by a similarity floor, a cap on how many tags
may match, and a specificity cap: a label carried by more authorized documents than the
configured limit is a category rather than an answer and cannot introduce documents on
its own. Exact matches are exempt, because a user who typed a label meant it.

The catalog branch embeds a generated digest of the title, type, summary, facets and date
range, one vector per enrichment, fenced on the active analysis. It deliberately does not
require chunk embeddings: a scanned record whose text is unusable can still be found by
what it is about. It reuses the same query vector as the semantic branch and adds no
provider call, so both degrade together when the embedder is unavailable, while filename,
text and tag matching continue. Candidates beyond a relative distance band of the nearest
are dropped in the application rather than in SQL, because a distance predicate under
iterative index scanning would walk the whole index for a distant query.

A published analysis with no catalog vector is invisible to that branch, which degrades
ranking silently and with a bias toward older documents. `GET /api/enrichment` therefore
reports how many active analyses lack one, rather than warning on every query.

#### Facet filtering and counts

`tag_mode` selects whether a document must carry every requested facet or any of them and
defaults to `all`, because a selected facet is a narrowing instruction and existing saved
links mean exactly that. `exclude_tag_ids` removes documents carrying a facet, using the
same canonical, alias and road-overlap equivalences as inclusion so an excluded route
excludes the segments it would have matched.

Facet counts are served by `POST /api/search/facets`, not by search itself. The
authorized-assignment query is the most expensive in the system and today runs only when
a facet or date is selected; returning counts inline would put it on every search. Counts
are computed once over the already-materialized intermediate, reflect the caller's own
access, are post-filter, and are capped.

Document-tag responses add assignment facets, dates, extractor version, context suggestions
and refresh status. Manual input adds an optional subtype. Editors review roads with
`POST /api/documents/{id}/tags/{tag_id}/road`; its route ID must belong to the authorized
current document's candidates. Manual labels belong to the stable document; dismissals,
explicit re-add, aliases and existing permission rules remain authoritative. Catalog
counts, evidence and road associations remain SQL/RLS constrained. Auditors cannot read
document enrichment content. New tables explicitly grant access to the restricted
migration owner and required runtime role only.

### Auditing and errors

Protected access requires an access-start event before data is served. Successful
mutations and their change events commit together; denied attempts are recorded
separately so rollback cannot erase them. Downloads record server completion/failure,
not proof that a person read a document. Audit failure blocks protected delivery.
Events exclude passwords, session tokens and document bodies.

Administrators, auditors and scoped managers have detailed audit visibility.
Ordinary document activity shows change history rather than other users' access
events. Runtime database roles cannot update or delete audit history. This is
application-level append-only history, not immunity from database/cloud administrators.

| Status | Meaning |
| --- | --- |
| 401 | Authentication required or expired |
| 404 | Resource missing or inaccessible |
| 403 | Disallowed action on a visible resource |
| 409 | Checkout, revision, state or naming conflict |
| 413 | Upload exceeds the limit |
| 422 | Invalid request fields |
| 503 | Required dependency unavailable |

### Documentation delivery and scope

Usage is a separate high-level end-user guide. This business-logic reference contains
the detailed frontend and backend contracts. Each layer also has its own changelog.
All four Markdown sources are rendered by the frontend Docs reader. There is no new backend
documentation endpoint, database table or permission bypass. The source files must
contain only shareable application reference text because they are bundled assets.

The implemented pilot excludes CAD application integration/reference management,
simultaneous editing, visual CAD/PDF diffs, formal approvals, transmittals and permanent
UI deletion. Documentation must distinguish those exclusions from implemented behavior.


## Reading and maintaining these docs

Choose **Docs** in the sidebar to open **Usage**, the end-user guide. **Business logic**
is the separate technical reference for the web frontend, backend and Windows client.
**Frontend change log**, **Backend change log** and **Client change log** record each
layer’s changes. The client log lives at `frontend/src/docs/client/change-log.md`, is
imported as raw Markdown by the existing reader, and is available at
`/docs/client/change-log` (under `/dock/` on mmsdev). All five pages render their
canonical repository Markdown directly through Vite; there is
no duplicate HTML copy, publishing service or documentation database.

Use **On this page** to jump to sections. A heading's `#` link gives it a bookmarkable
URL. Breadcrumbs and document links switch pages. Heading anchors, Back/Forward and
reload work through the URL. Tables, lists and code blocks render as Markdown. The
reader supports light/dark appearance and narrow screens. Repeated headings get
unique anchors. Unknown documentation paths show an unavailable page.

The signed-in interface makes these application reference pages available to every
account, including auditors. Bundled reference text must never contain credentials,
session tokens or private DMS records. Raw HTML is not rendered. The reader loads
separately from the main document-browser bundle.

For **every agentic code change**, agents must update **Usage**, this **Business logic**
reference and **all three** changelogs before presenting the change as complete, even without
a commit. Keep Usage focused on end-user tasks; record technical rules here. Update
the affected sections and add a dated entry to this review history. If end-user behavior
is unchanged, record that review in a maintenance comment in Usage instead of adding
implementation details to the user guide. When
one layer is unaffected, its changelog must explicitly record the reviewed unchanged
impact rather than inventing a runtime change. Changelog entries are dated, newest
first, and grouped under Added, Changed, Fixed or Removed. Root AGENTS.md is the
canonical agent policy; CLAUDE.md imports it. Client changes use `client` scope and
record the applicable MSIX version, behavior and verified rollout status. The client
log covers desktop UI, Explorer integration, local synchronization, native DLLs and
packaging; the frontend log covers the web UI. Historical entries remain intact.
Companion logs reference client changes and note unchanged contracts where appropriate.

### Tagging pipeline schema

Migration `0020_tagging_pipeline.sql` adds advisory extraction and enrichment progress
fields, the `search.tag_decisions` ledger, the prune marker on `search.enrichment_control`
and `search.pipeline_status()`, and sets `queue_facet_refresh()` to extractor version 3.
Migration `0021_catalog_and_retrieval.sql` adds permission-scoped catalog embeddings with
an HNSW index, `search.identifier_core()` and the tag-lookup indexes retrieval needs,
including a `tag_id`-leading index on `search.document_tags` that every tag catalog read
already benefited from. Both are additive and written idempotently.

The worker claims, publishes and requeues at the same extractor version the queue selects
on, so the earlier queue/worker version mismatch no longer exists and tagging does not
need to be paused. `search.document_embeddings` is no longer written; it is retained this
release so a rollback to the previous image still succeeds, and is dropped in a later one.
Document access, version storage and desktop upload contracts are independent of tagging.

## Review history

### 2026-09-11 — Inference utilization

Raised stage consumers and initial regional budgets to the verified tenancy limits,
settled successful chat reservations to provider usage, reused regional connections
within each worker thread, and exposed utilization
against limits on the web pipeline. Reviewed frontend controls and backend admission,
lease and retry behavior. Windows 0.1.14.0 upload, SSO and Explorer contracts remain
unchanged; no desktop code or installer changes accompany this deployment.

### 2026-09-11 — Cloud extraction and regional capacity

Validation: 217 isolated backend tests passed, one optional test skipped; three browser checks and the frontend build passed. Ten synthetic Linux format/OCR canaries passed. The runtime image and live JobRun pilot passed; same-run warm activation and rollback both imported results. mmsdev is deployed with automatic limits of 64 normal / 128 maximum.

Separated extraction publication from embedding; added cancellable parsers, legacy
Office/email readers, authenticated cloud claims/imports, durable fleet reconciliation,
immutable releases and shared regional inference permits. Reviewed frontend controls
and stage reporting together with backend leases, RLS and publication contracts.
The Windows upload, hydration, checkout and SSO contracts remain unchanged by this
companion server feature; no client package was built or installed for it.


### 2026-09-11

**Windows architecture compatibility, 0.1.14.0.** Client: precise action capabilities
replace ambiguous legacy unions in command visibility, checkout, imports and move
destinations. Folder retry reconciliation uses child pages and the target ancestry
path; large manifest writes reuse a prepared SQLite command. Frontend and backend
contracts were reviewed and remain unchanged, including cursor listings, bulk moves,
SSO, permissions, upload sessions and the existing 250 MiB desktop discovery limit.
The browser’s eight upload lanes and multipart protocol are not enabled in this
client. No migration or server deployment is required. Windows build validation passed
32 core checks, both native tests and compiled UI/Explorer regressions. The signed
0.1.14.0 installer was verified and delivered to pilot Downloads; no installation
or web/server deployment was performed.

**Cursor paging and bulk moves.** Backend: `GET /api/folders/{id}/documents` pages a
folder by cursor with a count, computing the folder's role once; `POST /api/moves`
moves up to 200 items in one transaction with a savepoint and a result per item, under
checks now shared with the single-item endpoints, and audits each refusal. Frontend:
the listing loads more on request with a count instead of Previous and Next, and moves
go through the bulk endpoint with one retry for stale items. The Windows client does
not call either endpoint; its contract was reviewed and is unchanged.

**Uploads share the write fence; indexing runs in parallel loops.** Backend: the
upload pipeline takes the write fence shared, so uploads no longer queue behind one
another, while every permission change still takes it exclusively and waits for them;
`PW_WORKER_CONCURRENCY` runs that many indexing loops, embedded or under `cli worker`.
Proven by tests for concurrent uploads, a permission change waiting for an upload, an
upload waiting for a permission change and two loops each claiming a job once.
Frontend contract reviewed and unchanged. The Windows client's uploads go through the
same session endpoints and benefit without a change; its contract was reviewed and is
unchanged.

**Folder uploads run four at a time.** Frontend: the browser upload queue sends up to
four files at once, one large file at a time, shares folder lookups and creates
between files, and refreshes the listing and tree at most once a second instead of
after each file. Backend contract reviewed and unchanged: concurrent uploads already
wait for an upload slot and share the write fence. The Windows client's upload path
is unaffected; its contract was reviewed and is unchanged.

**Upload refreshes every 15 seconds, with one progress bar.** Frontend: the once-a-second
refresh fetched the whole tree, and every tree change blanked and reloaded the
listing. The listing now refreshes quietly at most every 15 seconds and at the end,
the tree only when folders were created, and a tree change no longer reloads the
listing; the tray shows one bar for the whole upload. Backend and Windows client
contracts reviewed and unchanged.

**Eight upload lanes.** Frontend: the upload queue keeps eight files in flight instead
of four, still one large file at a time, matching the server's eight upload slots per
API process. Backend and Windows client contracts reviewed and unchanged; mmsdev runs
eight indexing loops.

**Upload tray that scales.** Frontend: the upload queue publishes a snapshot with counts
kept as items change and at most 100 rows, the page no longer holds the upload list,
the tray subscribes to the snapshot, and the next file is picked in constant time. The
header, one progress bar, Retry failed and Open are unchanged in behaviour. Backend
and Windows client contracts reviewed and unchanged.

**Drive-like shell and folder page.** Frontend: **New** in the sidebar (a floating
button on phones) and a ▾ menu beside the folder's name replace the header's Upload,
New folder and Folder settings buttons; the breadcrumb is the folder's title; one
sidebar item is lit, the footer is gone and the phone drawer has a backdrop; search is
one rounded field; errors clear on navigation; checkouts have one breadcrumb row. The
listing has fixed columns, blank folder cells, hover checkboxes, type icons, an empty
state and a footer inside the card, and loads the next page as its end comes into
reach, one request per cursor. The shell is clipped so focus cannot scroll it. Backend
and Windows client contracts reviewed and unchanged.

**Every other page.** Frontend: one page header, empty state and loading state across
Search, Profile, People & access, Trash, Tags, the Tagging pipeline, the Audit log, the
access editor, Docs and the unavailable page; errors go to the page-wide banner; search
filters apply as they change; members and owners are added on choosing; group and
access-list deletion confirms in a dialog; folder deletion is a step in Folder settings;
the access editor gains a bordered preset control, a No access checkbox and a typed
person picker. Backend and Windows client contracts reviewed and unchanged.

**Documents over the listing and the grid view.** Frontend: a document opens in an
overlay above the page named by `returnTo`, which stays mounted and is read for every
listing and search parameter, so nothing reloads on open, step or close; Escape, the
arrow keys and Previous/Next file navigate; the listing gains a grid view sharing the
table's entries, selection, drag and menu code. The document page loses its label and
indexing chips, names its page buttons, and shows metadata differences as a table.
Backend and Windows client contracts reviewed and unchanged.

### 2026-09-10

**Scale, folder archives, drag-to-move and a stylesheet sweep.** Frontend: rows can be
dragged onto folders, sidebar folders and breadcrumb ancestors to move them; a folder
downloads as a ZIP after a size preflight; the palette and layout metrics are declared
once and checked by a browser test; the stylesheet's duplicate layers, fragile
selectors and breakpoint mismatch are removed; sizes format up to TB. Backend: folder
ancestry is materialised and subtree checks use it; principals are cached in a
trigger-maintained closure; the folder read policy and `has_management` are evaluated
per statement; folder renames queue re-enrichment for the worker instead of fanning out
inside the request; the schema ceiling for versions and upload sessions is 20 GiB with
multipart tables in place; folder archives stream through the API. Authorization rules
are unchanged, and the new caches and set functions are proved equal to the previous
definitions by recomputation tests. Files above 250 MiB, up to 20 GiB, travel through the part
protocol from the web client's upload queue, and document authorization is resolved
per statement (migration 0030). The Windows client is still told 250 MiB and still
sends one request; its contract was reviewed and is unchanged.

**Relaxed folder moves, selection and folder pickers.** Backend: migration 0031 lets
a folder move go ahead with Write on the folder and Create subfolders at the
destination unless it would change who can reach the contents, in which case Change
permissions is required as before; the API and `dms.check_folder_tree` apply the same
rule. Restoring a version above 250 MiB is refused with advice instead of failing in the
single-request path. Frontend: the directory has a selection with keyboard operation,
a right-click and row actions menu, a selection bar, **Move to…**, **Undo** after a move
and bulk **Archive**; every folder chooser searches the server instead of listing the
whole tree; the Access chooser keeps the `/dock` prefix. The Windows client makes
folder moves through the same endpoint, so the relaxed rule reaches it without a client
change; its contract was reviewed and is unchanged.

**Desktop manifest in bulk, loading rows and an error boundary.** Backend: migration
0032 adds `auth.document_masks()`; the desktop manifest takes masks in bulk, computes
capabilities once per mask pair, fetches current versions by index and drops the
unused role column, with identical rows and fingerprint, proven against the previous
statements. Frontend: placeholder rows while a folder loads, an error boundary around
routed content, an in-page dialog for switching off an account's access control, and
a test assertion that could never fail removed. The Windows client receives the same
manifest faster; its contract was reviewed and is unchanged.

- Investigated the installed 0.1.13.0 sign-in timeout. Credential-free traces located
  repeated twenty-second discovery timeouts before the browser callback. Windows
  HTTPS and a separate .NET request with matching client headers succeeded; restarting
  the idle signed-out process cleared the failure without a new package or network
  setting changes. The underlying cause of that process state is unconfirmed. Web
  frontend and backend contracts were reviewed and remain unchanged. Document the
  recovery and the current misleading pre-discovery “Waiting” label.

- Fixed Windows 0.1.13.0 SSO stopping after successful exchange because the selected
  root belonged to the former account. Per explicit user instruction, replace that
  local workspace on authenticated account changes, including unsent edits and local
  recovery state, while preserving server data and unrelated roots. Return Dock to
  the foreground, show setup status beside sign-in, and clarify the browser handoff
  page. Web frontend and backend contracts reviewed and unchanged; no migration,
  account reassignment or server checkout mutation is part of this change.

### 2026-09-09

- Contained the application within the window. The main pane now matches the sidebar
  it sits beside — fixed height, its own overflow — so the window itself never
  scrolls, and a folder listing fills its pane and scrolls its own rows instead of
  running past the bottom of the screen. Measured before and after at 1280x720
  through 2560x1440: a directory of seventeen rows overflowed a 900px window by
  510px and now overflows by none at any size, while the listing keeps its full
  width and its column headings stay visible as rows move under them. Two defects
  found and fixed during the pass rather than shipped: `margin: 0 auto` on a flex
  item opts out of stretching, which had quietly narrowed the content column; and
  `:has()` selectors spanning the sidebar tree and the listing made interaction about
  five times slower and destabilised a browser check, so the views mark themselves
  with a class instead. The docs outline was repointed at the pane that scrolls,
  since it had been listening to the window. Backend contract reviewed and unchanged;
  the Windows client is untouched and its contract remains as recorded for 0.1.9.0.

- Fixed Windows 0.1.10.0 sign-out after server logs showed `/api/logout` returning
  401: the old handler stopped before local cleanup. Expired sessions now count as
  already revoked. Local sign-out, saved-token removal and provider teardown complete
  independently of server availability, with honest failure feedback. Added portable
  API and compiled-window/menu regressions including retained pending work. Reviewed
  the web frontend and backend contracts: both remain unchanged, including logout
  authorization, cookies, WVDOT SSO, storage and checkout ownership.
  Windows native, core, compiled-menu/appearance and Explorer routing checks passed;
  signed 0.1.10.0 was signature-verified and copied to pilot Downloads with matching
  SHA-256. Installation and installed-client restart acceptance remain pending.

- Deployed single sign-on to mmsdev. Migrations `0025` and `0026` applied to the
  server database, with a full dump and per-table counts taken first because `0025`
  drops a column and a rollback needs them; 646 documents, 668 versions and 17,994
  audit events carried through unchanged, and the password column is gone. The
  preflight passes from inside the deployed container, including outbound HTTPS to
  the broker and its TLS chain. The deployment provisions openly by explicit
  instruction — `PW_OIDC_AUTO_PROVISION=true`, `PW_OIDC_PROVISION_ROLE=administrator`
  — so the population who can sign in is the population who can clear WVDOT Entra,
  and each first sign-in creates an administrator with full rights over all 646
  documents, access control and the audit log. It was briefly deployed refusing
  unknown employee numbers; that was reversed on request, and the concern is recorded
  here rather than in the setting. Narrowing it later affects new arrivals only,
  because sign-in never rewrites an account's role. A real
  end-to-end sign-in still requires a WVDOT account and a browser and is not something
  this change could exercise. Frontend and Windows client contracts reviewed and
  unchanged by the deployment itself.

- Registered the mmsdev broker client and prepared the deployment. `scripts/check_sso.py`
  preflights a configuration from the host that will use it: it reads the settings,
  fetches discovery and the key set, confirms the broker accepts this client and
  callback, confirms a near-miss callback is refused, and confirms the client id and
  secret authenticate — it sends a deliberately invalid authorization code, so
  `invalid_grant` is the success case and `invalid_client` means the credentials are
  wrong. It consumes nothing and gates a deployment by exit code. Run against the real
  broker with the registered client, every check passes, including strict callback
  matching. Migration `0026` and `PUT /api/users/{id}/subject` close a gap the previous
  change left: accounts that predate single sign-on had no employee number and could
  never be signed into, stranding the permissions arranged for them. The frontend
  offers the field from the account editor while an account has none. Backend contract
  reviewed and otherwise unchanged; the Windows client is untouched by this change and
  its contract remains as recorded for 0.1.9.0.

- Replaced password authentication with the WVDOT identity broker (OpenID Connect) in
  every surface, and removed password material from Dock entirely. **Backend:**
  migration `0025_sso_identity.sql` drops `auth.users.password_hash` and
  `auth.login_candidate`, adds `subject`, `display_name`, `email`, `first_login_at`
  and `last_login_at` with a partial unique index on `upper(subject)`, and adds
  `auth.sso_login_states` plus `SECURITY DEFINER` functions for the round trip and for
  creating an account by employee number. `POST /api/login` is gone; four sign-in
  routes replace it, and `argon2-cffi` is no longer a dependency. Sessions, CSRF,
  cookies, `auth.identify`, the access-control model and every row-level-security
  policy are unchanged — only the proof of identity in front of `auth.create_session`
  differs. **Frontend:** the sign-in screen has one action and no fields, a
  `/login/callback` route trades the one-time handoff code for the session, People &
  groups gained **Add person** and lists people by the name their WVDOT account
  carries, and the profile shows the employee number. **Windows client:** 0.1.9.0
  signs in through the system browser and a loopback listener; the credential fields
  are removed and the plaintext saved username with them. Everything downstream of the
  cookie is untouched, so no C# outside `DockApi`, `SsoSignIn` and the sign-in panel
  changed. **Provisional and flagged as such:** an unknown employee number is
  currently provisioned as an administrator so a fresh deployment has someone who can
  grant access; that must be narrowed before wider rollout, and is a setting rather
  than a constant. Verified with the whole backend suite and the browser suite signing
  in through a stand-in broker, the portable desktop core checks including the
  loopback listener, the cross-targeted WPF build, and a live round trip against the
  running development stack. Not verified: the real broker (no client is registered
  yet), MSIX packaging, installation and Explorer or Bentley runtime behavior.

- Fixed Windows 0.1.8.0 main-window style inheritance after an installed 0.1.7.0
  screenshot showed dark cards on a white canvas with black headings. Explicitly
  apply the shared Window style to the compiled MainWindow class. Regression checks
  now instantiate that class with isolated state and exercise the actual theme action
  across its five views. The earlier plain-Window preview did not cover derived-type
  implicit-style lookup. Reviewed web frontend and backend contracts: both remain
  unchanged, including API, authorization, storage and sync behavior. The signed
  correction was installed on the Windows pilot; the real theme action and dark
  Transfers window were verified after upgrade.

### 2026-09-08

- Added Windows 0.1.7.0 light/dark appearance with an always-available footer switch,
  shared dynamic palettes and themed native title bars. Persisted appearance separately
  from credentials, retaining a session-only choice if persistence fails. Reviewed
  web frontend and backend contracts: navigation, API, authorization, storage and
  synchronization remain unchanged. See Windows desktop appearance below.

- Replaced the ordinal role ladder with ProjectWise-shaped access control: independent
  permission sets, a folder's own permissions kept separate from those for the documents
  inside it, per-document exceptions, nestable access lists beside groups, explicit
  denial, permissions that accumulate across principals, account-level settings and
  deliberate ownership. The previous model could not express the distinctions this
  repository exists to serve — a records clerk maintaining document properties without
  opening drawings, a designer editing drawing content without touching properties, or
  someone who administers a folder but not its contents — because `controller` was forced
  to include `editor` and one role won per folder. Backend: `auth.permission_bits`,
  `auth.permission_presets` and `auth.action_map` define the vocabulary, the presets and
  the translation from a requested action; `dms.acl_entries` stores assignments;
  `auth.access_mask` and `auth.document_mask` resolve them; `auth.can` and
  `auth.document_can` keep their signatures, so RLS, triggers, search, the manifest and
  the worker moved to the new engine together rather than one caller at a time. Three
  findings came out of doing it. Adopting ProjectWise's rule that any assignment makes a
  folder a boundary would have silently cut off everyone inheriting, so the conversion
  flattens first and the editor carries the inherited set forward before the first
  assignment lands; the migration then compares `auth.can` and `auth.document_can` for
  every account, folder, document and legacy verb before and after, aborts on any loss and
  records any gain in the audit log. Defaulting a folder's owner to whoever created it —
  the obvious reading of Bentley's ownership rule — would have let anyone who can add a
  subfolder grant themselves access inside it, contradicting this repository's existing
  contract that creating a folder conveys no authority over access; ownership is therefore
  an explicit designation, and an owner's authority stops where a folder is sealed.
  Retargeting `folder.create_subfolder` dropped the archived-folder guard that the
  overloaded `edit` verb had carried, which allowed creating folders inside the Trash until
  the existing Trash test caught it. Two pre-existing behaviours were also corrected while
  reading the paths they sit on: `SELECT ... FOR UPDATE` is filtered by the update policy,
  so checking a permission after taking the row lock reported a denial as a conflict, and
  `auth.has_management` counted folders sitting in the Trash, so a deleted folder conferred
  audit access. Frontend: the access workspace replaces the role-and-grant form with a
  permission matrix, an inheritance chain drawn as nodes and connectors, a carry-forward
  warning that fires on actual loss of access rather than on the boundary change, an
  effective-access panel that asks the server for the resolved answer and its reasoning
  rather than reimplementing resolution, a per-document Access tab, access-list
  administration, group and list ownership, and account capability settings. Both layers
  changed. The Windows client is unchanged: it authorizes by capability name, and the
  legacy names still answer as unions of the precise permissions; see the
  [Client change log](/docs/client/change-log).

- Completed extractor version 3 and added the administrator Tagging pipeline, resolving
  the version-3 queue against version-2 worker mismatch recorded in the previous entry:
  `facets.EXTRACTOR_VERSION` is now the single definition, used by the claim, requeue,
  publish, road-cache and queue paths together. Left unresolved, that mismatch would have
  re-queued the whole corpus on every backfill, because published rows could never reach
  the version the queue function selected on. Backend: closed discipline vocabulary,
  topic and label hygiene, corroboration merged on catalog identity, a verification pass
  scoring salience and confidence, the `search.tag_decisions` ledger with a fixed
  rejection vocabulary and ninety-day retention for unpublished analyses, advisory stage
  and page progress, `search.pipeline_status()` with `GET /api/pipeline` restricted to
  administrators, and `GET /api/documents/{id}/decisions` under existing document
  permissions. Backfill is administrator-triggered only; existing analyses are never
  re-run automatically. Retrieval gained a tag branch, an identifier-core anchor, a
  catalog-vector branch and weighted rank fusion, plus `tag_mode`, facet exclusions and
  `POST /api/search/facets`. Two pre-existing defects found while reading the pipeline
  were corrected: per-row page and chunk inserts held the job row lock long enough on
  large documents to starve the heartbeat and expire the lease, and
  `search.document_embeddings` was written for every generation and read by nothing.
  Frontend: the Tagging pipeline page, verification scores and suggestion promotion on
  the Tags tab, and facet match mode, exclusions and counts. Both layers changed. The
  Windows client's generated wire models are unchanged, though the shared OpenAPI
  document was regenerated; see the [Client change log](/docs/client/change-log).

- Redesigned the Windows client for 0.1.6.0 with WVDOT branding, sidebar navigation,
  summary cards, table/empty-state styling, a focused toolbar and consistent dialogs.
  Reviewed web frontend and backend: rendered documentation updates only; APIs,
  authorization, storage, synchronization and checkout behavior remain unchanged.

- Added automatic Windows imports and upload status for 0.1.5.0: stable-copy
  detection, nested folders, durable retry/backoff and per-item errors. Existing
  edits still require check-in. Reviewed web frontend and backend contracts:
  unchanged; the client uses the existing authorized upload/folder endpoints.
  Passed 26 core checks on macOS/Windows and installed 0.1.5.0 on the pilot PC.
  Verified the upload UI and a live synthetic automatic upload with matching server
  checksum, then archived the test document.

- Extended the Windows unregister script into a current-user uninstaller: remove
  Cloud Files registrations, stale owned Explorer namespaces and default-action
  verbs, then remove the MSIX package. Documented Windows' removal of online-only
  placeholders and preservation of downloaded files and external client state.
  Reviewed web frontend and backend contracts: runtime behavior, permissions,
  checkouts, server documents and schema remain unchanged.

- Added the dedicated Windows Client change log and fifth Docs navigation link,
  using the same Markdown reader, anchors, tables, history and responsive layout.
  Seeded known pilot updates through 0.1.4.0 from verified repository history.
  Updated AGENTS.md and CLAUDE.md to require all five references and distinguish
  web frontend, backend and client changelogs. Reviewed backend and Windows runtime
  contracts: unchanged; this adds web documentation, not a new client package.

- Corrected Explorer command focus handoff: the newly launched instance grants
  foreground permission specifically to the connected named-pipe server before
  forwarding its command. The running instance activates the modal dialog after
  rendering and focuses its first control; repeated activation targets an existing
  modal instead of its disabled owner. No permanent topmost setting or synthetic
  keyboard input is used. Reviewed web UI and backend contracts: unchanged alongside
  the optional-version-comment change in this release.

- Made version comments optional across web uploads/check-in/restoration, Windows
  check-in/import, API validation and database constraints (migration 0019).
  Omitted, empty and whitespace-only API comments normalize to an empty string;
  supplied text is trimmed, limited to 4000 characters and rejects NUL. Version and
  upload rows retain non-null comments; existing history is preserved. Reviewed both
  layers: checkout ownership/base-version checks, immutable versions, idempotent
  finalization and audit events remain unchanged. Discussion posts and force-release
  reasons remain required. Windows package advances to 0.1.4.0.

- Added the requested Explorer double-click checkout gate in MSIX 0.1.3.0.
  Conditional default verbs apply only beneath the active workspace for document
  types with a registered Open action. The existing editor association is retained,
  and explicit Open after the decision prevents recursion. Reviewed web UI and
  backend checkout/authentication/storage contracts: all remain unchanged. The
  pilot installer now uses the required machine TrustedPeople store when explicitly
  supplied a development certificate; exit/unregister clean up Dock-owned verbs.
  Verification passed: 20 core checks, native tests, actual default-only Shell
  invocation inside/outside a synthetic workspace, editor bypass and cleanup, and
  the workstation's existing Word association. The signed MSIX installed successfully;
  the older loose EXE has exited, a live workspace Word file selects Dock's default
  action, and the user confirms seeing the prompt. Its foreground placement required
  the subsequent focus-handoff correction above.

- Windows investigation confirmed repeated `STG_E_ACCESSDENIED` while writing
  custom properties to read-only documents. Replaced those writes with an MSIX
  custom-state handler backed by a same-user registry cache; status queries never
  open or hydrate the document or change its read-only flag. Reviewed both layers:
  web UI and backend authorization, storage, schema and API contracts are unchanged.
  Both native tests and 19 core checks passed on Windows; isolated real Cloud Files
  reads also matched synthetic content. MSIX schema/signature validation and
  installation passed after approved trust of the existing signer in LocalMachine
  TrustedPeople. Packaged launch was observed; full Explorer behavior remains
  pending verification after exiting the older loose EXE.

- Investigated reported desktop slowness using live server logs and timed manifest
  and document reads. Reduced repeated Windows hashing, per-file journal commits,
  duplicate presentation and unchanged Explorer property writes; moved refresh
  reconciliation off the UI thread and added slow-stage diagnostics. Reviewed
  backend API, authorization, schema and storage contracts: all remain unchanged.
  Confirmed Explorer's existing Dock → Open checkout choice; default file
  associations and native double-click behavior remain unchanged.

- Fixed Windows Cloud Files completion structure sizes, failure status, ticket
  lifecycle and cancellation re-entry; added local diagnostics and regression
  harnesses. Reviewed desktop download, cleanup and notification handling. Web UI,
  backend download/authorization contracts, storage and schema remain unchanged.
  The reported Windows crash cause still requires the faulting-module/exception
  record; these corrections do not constitute Explorer runtime sign-off. Integrated
  the latest main-branch Windows SDK header fixes and Visual Studio 2026 generator
  setting; reviewed the packaging contract alongside the desktop fixes.

- Corrected OCI outage handling observed during bulk refresh. Backend workers now
  share a persisted cooldown and preserve attempt budgets; frontend queue controls
  show the next automatic retry. Both layers retain document access and prior tags.

- Verified live deployment and corrected a missing-page date response: backend
  validation now retains independent valid facts with partial status; frontend
  partial-state and evidence contracts were reviewed and remain unchanged.

- Replaced generic enrichment with grounded document facets and FuzzyRoad associations;
  added combined tag/date filters, road review and version-aware refresh. Reviewed both
  frontend navigation/correction workflows and backend validation, RLS, retries and
  publication fencing. Existing document control, OCI object storage and desktop contracts
  remain unchanged; search/tag APIs gain backward-compatible fields and road review.

- Documented the official WVDOT Dock name and DOCK expansion, Document Organization
  and Collaboration Keeper, in Usage and Business logic. Explained the shared purpose
  for end users and the supporting document-control rules in the technical reference.
  Reviewed both layers: frontend controls and backend API, permissions, data, and
  audit contracts remain unchanged by this documentation update.

- Verified the server data copy and OCI references, corrected Apache handling of
  the bare `/dock` URL, bounded repeated search permission work per document, and made derived extraction filenames content-addressed
  so copied indexing jobs can retry across platforms. Reviewed both layers: UI
  document controls and backend original-version/authorization contracts remain
  unchanged; indexing preserves both differing derived outputs.

- Verified the portable client with 12 checks, the backend with 60 regression checks,
  local/subpath navigation with 10 browser checks, and a 10,000-record/ten-user load
  run. The full/unchanged manifest pair peaked at 7.39 seconds. Native DLL compilation,
  MSIX installation, Explorer and Bentley acceptance still require Windows.

- Added the Windows client implementation, native Explorer bridge, durable local
  workflows and Windows packaging instructions. Added authenticated desktop manifest
  and discovery interfaces, operation audit attribution and configurable deployment
  subpaths; kept the existing permission/check-in authority. Actual Explorer/Bentley
  acceptance and MSIX installation remain Windows pilot checks.

- Added the mmsdev Docker build/deploy workflow with host Apache routing and a
  copied, isolated database in the server’s local PostgreSQL service. Reviewed frontend paths, docs,
  sessions and backend RLS/worker/storage contracts. Migration-owner policies
  support a restricted database owner; runtime authorization and file-version contracts
  remain unchanged. Local development remains native.

- Added compact bottom Administration/Workspace tools navigation, an upward popup,
  a remembered expanded layout and independently scrolling folders. Reviewed backend
  authorization, API, data and audit contracts; all remain unchanged.

- Separated Usage into a high-level end-user guide at `/docs/usage`; retained the
  detailed frontend/backend contracts here at `/docs/business-logic`. Docs now opens
  Usage by default and links to all four documents.
- Updated AGENTS.md and CLAUDE.md to require the separate audiences and maintenance
  of all four documents. Backend API, data, authorization and storage behavior are
  unchanged by this documentation split.

- Established the whole-app usage and business-logic baseline from the implemented
  UI, API, migrations, worker and verification records.
- Added the Docs reader with this single combined document and separate frontend
  and backend changelogs, all rendered from their canonical Markdown sources.
- Reviewed backend impact: the documentation viewer does not change API, schema,
  authorization or storage behavior and requires no new backend endpoint.

## Windows desktop client

### Architecture, identity and deployment

`desktop/windows` contains a .NET 10 WPF/Windows 11 x64 application, a portable core,
SQLite operation journal, and native C++ Cloud Files and IExplorerCommand DLLs. A
Windows build script compiles the DLLs and packages the self-contained application
as MSIX; signing is explicit. The manifest disables filesystem/registry write
virtualization with the unvirtualizedResources capability so journals and recovery
data remain outside package-managed uninstall cleanup. Native runtime, installation and Bentley validation
must happen on Windows. Cross-targeted WPF compilation is not that validation.

`desktop/windows/scripts/unregister.ps1` is the combined current-user cleanup
and package uninstaller, including for installations through MSIX 0.1.4.0. It runs
in 64-bit Windows PowerShell and requires Dock to exit from its tray first; it
never force-closes editors or the client. `-WhatIf` inventories and previews without
changing registrations or packages. Actual cleanup preflights write access to the
owned machine registry keys; elevation must use the same Windows account.

Discovery reads `SyncRootManager` directly and selects only `Dock!<current SID>!`
entries, rejecting shared user mappings. It also uses locally saved workspace paths
to identify orphaned namespace CLSIDs whose display name is Dock and whose folder
instance points to one of those paths. It does not select arbitrary entries solely
because they display “Dock.” Windows' packaged-root enumeration is not relied on,
since it can omit broken registrations. Existing workspace paths are checked for
redirects and for the Dock Cloud Files provider before unregistration. The Cloud
Files API converts hydrated placeholders to ordinary files and removes online-only
placeholders; no workspace or client-state directory is recursively deleted by the
script. Downloaded files, local edits, SQLite journals and recovery data remain.

Cleanup removes the captured Dock namespace classes, navigation entries and
hide-desktop values, only marked Dock default-action verbs, and Dock's Shell display
cache. It then removes `Dock.DocumentKeeper` packages for the current user and
checks that the package is gone. Other users, editor associations, certificates and
server data are untouched. Failures stop with an error; rerunning handles an already
removed package or missing entries. An in-use package can fail removal after Shell
cleanup; close the application using it and rerun. This script change does not
produce a new MSIX version or change the web viewer/API contracts.

A workspace is bound to server URL, Dock account and local root. Existing nonempty
unbound roots are rejected. From 0.1.13.0, successful interactive sign-in with a
different server/account replaces the selected previously bound root: stop polling,
disconnect the old provider, remove the saved session, validate the path and overlapping
roots, unregister the exact Windows-user/root identity, remove its verified
SyncRootManager registry key and owned Explorer entries,
and delete local files plus that root's old journal, snapshots and checkout secrets.
Only then remove the old binding and register the new workspace at the same path.
The user explicitly requested deletion of unsent work when accounts differ; no copy,
merge or second folder is created. Other saved roots remain untouched. Deletion does
not traverse symlinks/junctions or hydrate files, and refuses drive/profile/state
roots and overlapping registrations. Locked files or cleanup failures abort the switch;
the retained old binding makes retry complete cleanup before any new-account sync.
Cached/offline startup cannot trigger replacement; same-account sign-in preserves
local work. No server document deletion or checkout release is sent. Root state keys
retain the existing hash inputs so previously stored journals are found. Its NTFS files and local state
are restricted to the Windows user and SYSTEM. Session credentials and checkout
tokens are protected with Windows DPAPI; OCI credentials are not saved, and there is
no password to save — the client neither asks for one nor has anywhere to put one.

The client signs in through the WVDOT identity broker, using the system browser. Only
a real browser can complete that round trip: it carries the Windows sign-in state, and
an embedded view would neither see it nor be trusted with it. `Dock.Core/SsoSignIn.cs`
binds a `TcpListener` on `127.0.0.1:0`, and `auth/sso/login?port=<port>` tells the
server where to return; the return address is built server-side from the port, so the
parameter cannot be turned into a redirect anywhere else. The listener receives a
one-time code — never a session — and `DockApi.SignInWithSso` trades it at
`auth/sso/exchange` for the ordinary cookie and CSRF pair. This is the shape RFC 8252
recommends for a native application. A raw socket rather than `HttpListener`, because
HTTP.SYS wants a URL reservation for an unelevated process and a socket keeps the
exchange exercised by the portable checks on any machine. The wait is five minutes,
which allows for a second factor, and the listener stops as soon as it has an answer.
The client is a single interactive tray process, so a browser is always available; the
Explorer extension and the Cloud Files callbacks never touch credentials.

Authentication retains the same eight-hour cookie/CSRF session, the
same `Origin` check, the same DPAPI-protected `ExportSession`/`RestoreSession` blob —
which now also carries the display name — and therefore the same polling, hydration,
upload and Explorer behavior. Expiry pauses server actions while retaining cached files
and edits; **Sign in again** opens the browser once more and renews access.

`PW_PUBLIC_BASE_PATH` scopes backend root_path and cookies. `VITE_BASE_PATH` scopes
assets, browser routing, previews, downloads and requests. Default local paths remain
`/` and `/api`. The mmsdev deployment uses `/dock` and `/dock/api` behind Apache
that strips `/dock` from API requests. The Origin is the HTTPS authority without the
path. Discovery advertises deployment URLs; the client rejects a different origin,
unsupported protocol, or remote HTTP. No TLS bypass or pre-authenticated OCI links.

### Manifest and permission enforcement

From Windows 0.1.14.0, precise manifest capabilities take precedence whenever any
`doc.*` or `folder.*` actions are present. Legacy-only manifests retain their old
verb mapping. File reads need `doc.file_read`, checkout/check-in need
`doc.file_write`, file imports need `doc.create` and creating folders needs
`folder.create_subfolder`. Navigation-only entries never grant an action. Explorer
organize/delete commands use the matching write/delete permissions. Move destinations
need `doc.create` for documents or `folder.create_subfolder` for folders; the current
parent remains available for rename-only operations. Self/descendant destinations
are omitted. The server remains authoritative on source permissions, revisions,
checkouts and access-changing folder moves.

Folder creation reconciles a lost response through `GET /folders/{id}/children`,
following opaque encoded cursors with at most 1,000 rows per page, then creates only
when no matching parent/name is found. Missing items or repeated cursors stop the
operation. Existing folder mutations resolve the target from `/folders/{id}/path`.
Only 404/405 on these newer routes can fall back to the existing whole-tree routes
for older servers; permission/service failures propagate. Document mutations keep
their existing detail/PATCH routes and revision guards. Manifest replacement reuses
one prepared SQLite statement within the existing entry/fingerprint transaction;
pending operations and removed identities remain durable. Addition discovery reads
one journal snapshot for both known and removed paths. The client still receives a
complete manifest, scans the local workspace and sends automatic uploads serially;
the 100,000-document journal test is not a full Explorer scalability sign-off.

`GET /api/desktop/config` exposes only protocol version, public URLs, Origin, upload
limit, poll interval and session lifetime. `POST /api/desktop/manifest` authenticates
and audits the request, returning a complete user-scoped folder/document manifest
or an unchanged result for an opaque content fingerprint. Its queries run under RLS
and the shared scope-mutation fence, with no transaction held during response transfer.
Manifests include effective action capabilities, versions, hashes, sizes, revisions
and checkout summaries; they exclude checkout secrets and global change counters.

The manifest's two statements resolve permissions in bulk (migration 0032). Folder
masks come from `auth.folder_masks()`. Document masks come from
`auth.document_masks()`, which gives each document its folder's document mask and
resolves the few documents with their own access entries through
`auth.document_mask`, so exceptions and document ownership keep their meaning.
Capabilities are computed once per distinct pair of masks rather than per row. The
current version is fetched by one indexed lookup per visible document, so the
version read policy runs only for documents the account can see. That policy stays
`auth.document_can` per row, because the set form costs every statement a pass over
the whole corpus and most statements touch a few rows. The unused
`auth.effective_role` column is no longer computed. The response and its fingerprint
are unchanged, so installed clients keep their cached fingerprint.
`test_desktop.py` runs the replaced per-row statements beside the new ones for every
account, including a document with its own entry, and requires identical rows;
`test_final_invariants.py` proves `auth.document_masks()` equal to the per-row
functions, including for an owned document. Measured as database time on 14,944
folders and 100,000 documents: documents 7.1 s to 2.6 s for an administrator, 6.4 s
to 2.7 s for an auditor and 0.35 s to 0.14 s for a scoped account; folders 0.81 s to
0.21 s, 0.66 s to 0.18 s and 0.53 s to 0.46 s. An account that sees the whole corpus
still spends most of that time authorising each current version; a change-based
protocol, not yet built, is what removes it.

Connected clients reconcile every 15 seconds and refresh after actions, with bounded
backoff on failure. Complete manifest validation precedes local removal. Interrupted
responses and invalid/missing ancestors cannot empty a workspace. SQLite updates the
entry set and fingerprint transactionally; failed local reconciliation forces a full
retry. Backend checks remain authoritative on every transfer and mutation. Ancestor
navigation does not grant content access, and auditor entries cannot hydrate content.
Desktop requests can carry a UUID `X-Dock-Operation-Id`, recorded in mutation/access
audit details without session or checkout tokens.

### Windows desktop presentation

Version 0.1.6.0 uses WVDOT Dock in the native window title, sign-in surface, tray
label, dialog titles and package display name. The package identity, application ID,
execution alias and Cloud Files registration identity remain stable across upgrades.
A left navigation rail controls the existing five view indices; programmatic Explorer
and upload navigation keeps the selected navigation item and page heading in sync.
Workspace summaries count all non-removed entries independently of the current text
filter. Transfers hides the document search field because transfers are not filtered.

Shared WPF resources define rounded controls, table rows, file/folder icons, status
badges, empty states, hover/disabled states and visible keyboard focus. Data grids
retain row/column virtualization and sorting. Advanced Directory commands move into
More; account actions and graceful exit are in Account settings. Sign-in connection
fields remain available inside an expander. Dialogs use the same visual resources
while preserving foreground activation, cancel behavior and optional comments.
Native window chrome remains available for resizing and standard Windows controls;
the initial window fits the current work area and navigation/sign-in can scroll.
Automatic uploads, checkout/check-in, retry, recovery and backend contracts are unchanged.

At window heights below 700 logical pixels, the desktop hides summary cards and
reduces sidebar spacing to keep the document list and five navigation choices usable.

### Windows sign-out

Client 0.1.10.0 detaches the current workspace from the UI and shows sign-in immediately
when Sign out begins. The existing busy guard prevents sign-in or another document
command during teardown. It clears account rows, summary counts, upload display,
queued activation and tray status. Callbacks from the detached workspace cannot
replace the sign-out status or dispatch stale structural commands.

Remove only `session` from the private client settings, writing through a unique
same-directory temporary file and atomic replacement so an interrupted write does
not truncate server, root and ownership settings. If persistence fails, explain that
the saved sign-in could return after restart. Appearance has its own file and is
unaffected. Cancel and drain polling before requesting server logout; preserve the
operation journal, snapshots, local bytes and checkout tokens. Dispose Explorer
opening integration and the workspace/provider off the UI thread, leaving the sync
root registration and cached files intact. New sign-in remains disabled until cleanup
finishes.

`DockApi.SignOut` posts to the existing `/api/logout` with Origin and CSRF headers
and a ten-second request deadline. It accepts successful responses without requiring
JSON, and treats HTTP 401 as an already-invalid server session. Its finally block
clears cookies, identity and CSRF in memory. Other HTTP/transport/cancellation failures
are reported as unconfirmed server revocation while local sign-out still completes;
do not claim the server session was revoked in that case. It may remain valid until
its ordinary expiry. The main handler preserves this status instead of replacing it
with Ready.

The web sign-out flow and backend endpoint contract are unchanged. No global WVDOT
or browser logout is requested; the next SSO round trip may reuse that browser's
existing identity. No check-in, checkout release, document deletion or account change
occurs as part of sign-out.

### Windows desktop appearance

Version 0.1.8.0 provides an immediate Light mode / Dark mode footer action before and
after sign-in. Light is the default, including when the saved value is unknown or
malformed. The preference is per Windows profile, not per Dock account or server;
sign-out preserves it. It is independent of Windows and the web app's theme.

`Appearance` swaps the first application merged resource dictionary between matching
Light/Dark palettes. Brushes use dynamic references so existing cards, labels, fields,
selection/focus states, lists, upload progress, context menus and modal dialogs update
without recreating the workspace or starting network work. Brand panels retain their
dark teal identity. MainWindow explicitly references the shared Window style because
WPF implicit style lookup uses the concrete type; a style targeting Window alone does
not apply to the derived MainWindow. This fixes its canvas, inherited text, font and
layout defaults in both modes. Tests use the compiled MainWindow with a supplied
private temporary state directory and no session initialization, rather than changing
its runtime type to Window. Native Windows 11 title bars use documented DWM caption/text
attributes; resize, close, activation and dialog focus behavior stay native. Explorer,
external editors and the Windows tray menu retain their own appearance.

The only persisted value is `theme: light|dark` in `%LOCALAPPDATA%\Dock\appearance.json`,
beneath the existing private client state directory. A unique temporary file is moved
over that file on save; credentials, `client.json` and the workspace journal are never
rewritten by switching appearance. Missing/invalid JSON or read failure falls back to
light with local diagnostics for errors. Write failure keeps the selected mode for the
session and displays a persistence warning; no sync or document operation is retried.
The footer's accessible name describes the next mode, and it supports keyboard use.

Web rendering/navigation, backend API/schema, permission checks, desktop synchronization,
checkout, upload and recovery contracts were reviewed and remain unchanged.

### Desktop refresh cost and diagnostics

Refresh runs on a thread-pool task under the existing workspace semaphore, keeping
SQLite scans, filesystem reconciliation and Explorer presentation off the WPF
thread. The UI loads one entry snapshot per redraw for all lists and connection
status. Full manifests present each successful entry once; unchanged manifests
still repair missing placeholders and retry blocked reconciliation/removal.

Background polls reuse in-memory file hashes only while path, byte length,
last-write time and creation time match and the sample is less than five minutes
old. Restart, explicit Refresh, checkout/check-in, and a changed server manifest
force fresh hashing. The latter precedes permission-loss recovery or replacement,
so a metadata-preserving edit is not discarded based on a cached hash. With an
unchanged manifest, edits preserving all sampled metadata can take up to five
minutes to appear without explicit Refresh. Files changing during a hash are
retried; cache entries disappear when their paths leave the active document set.
Only hydrated files are scanned. A scan batches changed local states in one durable
SQLite transaction and leaves unchanged rows untouched; upload/checkout operation
journaling and snapshot/checksum verification keep their existing ordering.

The Windows provider caches command masks and displayed status/icon values, skips
identical writes, and serializes status publication to `HKCU\Software\Dock\Status`.
Each path holds an atomic multi-string value containing display text and a bounded
icon name. The MSIX custom-state COM handler reads this same-user cache only for
paths within the configured root, exposes property ID 1, and accepts only bundled
icon names. It never opens a document, performs network IO or reads credentials.
Changed values notify Explorer asynchronously; connection-wide updates run off the
UI thread. Recreated/converted placeholders invalidate the in-memory cache, and
removals delete the persisted value. Failed writes remain eligible for retry.
This replaces `StorageProviderItemProperties.SetAsync`, which returned
`STG_E_ACCESSDENIED` on read-only files in a Windows reproduction. Read-only flags
are never relaxed for status display; checkout pinning and server authorization
remain enforced. The packaged app must be installed to register this handler and
the Explorer commands. Running a loose EXE does not install shell integration.

The local diagnostic log records scan, manifest-request and reconciliation timings
when a stage takes at least one second, plus polling exception types/stacks. These
records contain no document names, paths, content or credentials. A successful
server response does not measure workstation scan, Explorer or WAN delays; Windows
runtime measurements remain necessary before claiming a particular speedup.

### Local file lifecycle

Cloud Files supplies full-file, on-demand hydration; the client verifies exact version
size and SHA-256 before transferring staged bytes to the placeholder. Concurrent
hydrations are bounded. Callback hydration has a 50-second deadline, below Windows'
callback timeout; a slow or failed fetch fails without serving unverified bytes and
can be retried. This deadline needs testing with the pilot's 250 MiB files and network.

The bridge passes the exact active-member size to `CfExecute`. Failed transfers
use `STATUS_CLOUD_FILE_UNSUCCESSFUL`, never the sync-root-metadata-corruption code.
A staged file must match the placeholder size before transfer; local read failures
and failed data submissions send a terminal failure before discarding the ticket.
Cancellation matches both transfer and request keys, removes the ticket under its
mutex, and invokes managed cancellation after releasing the mutex. This permits
synchronous completion re-entry and keeps other requests for the same file alive.
Callbacks copy their borrowed arguments, contain ordinary C++/managed exceptions,
and deny structural operations when dispatch fails. This does not recover from
native memory corruption or establish the cause of any particular process crash.

Managed transfer cleanup, cancellation races and error observers cannot propagate
ordinary exceptions through the reverse callback boundary. Local diagnostics in
`%LOCALAPPDATA%\Dock\logs\desktop.log` record operation labels, exception types,
HRESULTs and stacks without source paths, exception messages, document contents or
credentials. Entries are capped at 16,000 characters; at 256 KiB the log rotates to
one previous file. Logging failures are contained. Unexpected UI/process exceptions
are recorded without marking them handled or assuming continued execution is safe;
Windows Reliability History remains needed for native crashes. Logs are local and
are not uploaded. The server URL defaults to the mmsdev `/dock` site, with saved
settings taking precedence; discovery still validates the advertised authority.

The Windows build runs a native bridge harness with intercepted `CfExecute` calls
before packaging: operation sizes, exact transferred bytes, empty/multi-chunk files,
failed submission, wrong-size staging, cancellation re-entry and request isolation,
and exception-to-denial behavior. The harness uses real Windows headers and file IO
but does not replace an installed-provider Explorer test. The current
MSIX version is `0.1.14.0`, retaining optional comments and foreground activation; the artifact
filename is derived from that version.
Upgrades must reuse the previous publisher/signing identity and retain local state.


Explorer properties show Dock checkout/edit/error state separately from Windows
hydration state. Explorer double-click and Dock → Open reach the same checkout
choice before the editor launches. The client resolves each document extension's
current ProgID and adds its own `Dock.DocumentKeeper.Open` verb beneath HKCU Classes.
`AppliesTo` and `DefaultAppliesTo` restrict it to the canonical workspace path plus a
trailing separator, preserving default behavior in sibling/outside folders. Neither
UserChoice, the type's normal default verb nor the editor's Open command is replaced.
Types without an existing Open verb are not intercepted. Registration updates run
off the UI thread, prune unused associations, and remove only owned verbs on clean
exit/sign-out; unregister also removes stale owned entries after a crash. The
packaged execution alias supplies a quoted raw filename, converted into an escaped
protocol request. After a read-only choice or successful checkout, the client invokes
explicit `open`, bypassing its conditional default action. Already-owned checkouts
open directly; unknown local additions open in their editor without server checkout,
and removed entries remain blocked. Cancellation launches nothing. A file opened
from an editor's own File → Open dialog does not use this Explorer verb.
Open-completion callbacks are not used for the human decision. The shell DLL
performs no network or credential work; it forwards
encoded commands to a same-Windows-user client. Cached command availability follows
capabilities, and the API rechecks authorization. Read-only attributes are guidance,
not server authorization.

Checkout ownership and base version are persisted before enabling writes. Another
workspace's checkout requires explicit resume confirmation. Check-in snapshots deny
concurrent writers/replacement during the copy, journal the upload identity, and reuse
reservation/content/finalization endpoints. Lost responses retry the same upload.
The working copy and token remain until publication is confirmed. New edits after the
snapshot are retained separately, never marked committed with the uploaded snapshot.

Polling detects dirty hydrated files, including replacement saves, and startup uses
the persisted journal rather than relying only on watcher events. Dirty/checked-out
files are not eligible for ordinary dehydration. Revocation, server changes and force
release preserve recoverable edits, stop automatic publication, and remove inaccessible
clean items where possible. Open files can postpone cleanup. Cached bytes or copies
already made cannot be recalled from an offline machine.

### Structural changes and CAD boundaries

In Windows 0.1.5.0, each successful background manifest reconciliation scans unknown
local additions and automatically imports stable files plus nested/empty folders.
The normal poll interval is 15 seconds. Two unchanged size/last-write observations
at least five seconds apart are required; an open writer blocks snapshot creation.
The immutable snapshot excludes writers/deleters throughout the copy. Additions
present at startup are included. Existing identities (including removed entries)
and revoked folder subtrees are excluded, preserving checkout/check-in and recovery
boundaries. Temporary/lock/backup trees, desktop.ini, Thumbs.db, .DS_Store, and symbolic
links/junctions are skipped; imports also validate ancestor redirection.

A serialized import pass shares the mutation gate for preparation and execution.
Automatic operations persist their origin, attempt count and retry deadline along
with the existing snapshot/upload identity. Network failures, HTTP 408/429/5xx and
interrupted requests retry after 15–120 seconds; permanent upload errors remain for
explicit retry in Transfers. One failed item does not stop the remaining queue.
A failed pre-network snapshot is discarded and rediscovered on a later scan;
no incomplete automatic operation is sent. Pending operations survive restart, and
execution reloads durable state to avoid repeating a completed stale UI selection.

A dedicated footer, progress bar, tray tooltip and Transfers list display discovery,
preparation, bytes sent, finalization, completion and errors separately from command
status. Pending operations remain in the existing retry list. Completed display rows
are session-local; the durable operation journal retains completion across restarts.
The web frontend and backend upload, authorization, version, storage and schema
contracts remain unchanged. Folder creation reconciles an ambiguous response by matching the accessible
parent and case-insensitive name. Upload operations retain stable retry identities.
Rename/move/delete reconcile the desired server state after an ambiguous response
and otherwise use existing revision and permission checks. Raw Explorer structural
callbacks deny the operation and dispatch a Dock confirmation rather than waiting for
a dialog in a filesystem callback. A checked-out document's replacement-save operations
are treated as local edits; they do not publish server rename/delete operations.

Document IDs remain stable independently of local paths. Invalid Windows characters,
reserved names, trailing dots/spaces and case-insensitive sibling collisions receive
safe local names, with ID suffixes preserving extensions. Relative CAD references are
preserved only where those names map unchanged; there is no automatic reference rewrite
or automatic checkout of dependencies. MicroStation/OpenRoads versions and two Windows
PCs must be supplied for the recorded acceptance matrix.
