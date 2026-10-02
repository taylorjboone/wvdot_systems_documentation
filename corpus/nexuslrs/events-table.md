# Events Table — Frontend Behavior

This document catalogs the current behavior of the events table and its surrounding
configuration, filtering, editing, and persistence flows in the NexusLRS frontend.
It pairs with `dynamic-segmentation.md` (which covers the event-layer vector-tile
pipeline) and focuses on everything the user sees inside the **Table** sidebar tab.

The table is not a standalone feature — it sits on top of `eventsStore.config.events`,
drives the events map layer via `tableStore`, and doubles as a read/write editor for
browser-saved snapshots.

---

## 1. Entry points and data sources

Rows always come from `eventsStore.config.events` regardless of how they were loaded.
The table UI only owns overlay concerns (visibility, filters, selection, style, edit
state); the row payload is owned by the events store.

Three ways data lands there:

| Source        | Entry point                              | How it seeds rows                                                                                   |
| ------------- | ---------------------------------------- | --------------------------------------------------------------------------------------------------- |
| ESRI layer    | `tableStore.loadFromEsri(layerName)`     | Assumes `eventsStore.loadLayer()` already ran. Reads that config to build column defaults + style.  |
| Excel / CSV   | `tableStore.loadFromExcel(rows, name)`   | Pushes rows straight into `eventsStore.setConfig()` with `_idx` and random `COLORKEY` per row.      |
| Saved snapshot| `tableStore.loadFromSaved(name)`         | Reads a JSON payload from `localStorage['nexuslrs.savedTables.v1']` and hydrates both stores.       |

All three set `tableStore.needsConfig = true` (on fresh / ESRI / Excel loads) or
`false` (on saved-snapshot load, since the saved state already contains column config).

Loaded-saved sessions also set `tableStore.loadedSavedName` to the snapshot name,
which gates the rename input, the overwrite Save flow, and the URL sync.

---

## 2. State model

The table's store (`src/state/table.store.ts`) owns the following slices. Field types
are abbreviated — see the TypeScript source for exact shapes.

```text
tableStore = {
  open, source, sourceName, needsConfig
  columnConfig : Record<name, { name, used, role, displayFormat? }>
  geomfields    : { RouteID | BMP | EMP → column-name or null }
  layerStyle    : TableLayerStyle           // draft map-style the dialog edits
  columnFilters : Record<name, ColumnFilter>
  sorting       : TanStack SortingState

  // Snapshot integration
  loadedSavedName : string | null
  saveRequestToken: number              // Ctrl+S bumps; toolbar reopens modal

  // Editing model (only meaningful for loadedSavedName sessions)
  editMode       : 'off' | 'autosave' | 'diff'
  pendingDiffs   : {
    updates : Record<idx, Record<col, value>>
    added   : EventRecord[]           // negative _idx markers
    deleted : number[]                // real-row indices staged for removal
  }
  lrsEditRowIdx  : number | null     // LRS edit overlay target
  editingRowIdx  : number | null     // dbl-click row unlock

  // Grid UX
  selectedRowIdx, hoverRowIdx, filterText, filterByMapBounds
  columnConfigOpen, paginationModel
  showOnlyDiffs
}
```

`close()` resets everything AND calls `eventsStore.reset()` — never leaves cached
map layers or rows behind. `dismissConfig()` only flips `needsConfig: false` so the
user can back out of the config dialog without wiping the session.

---

## 3. The config dialog

`TableConfigDialog` opens automatically after a fresh (ESRI / Excel) load because
`needsConfig` starts true. For saved snapshots it's opt-in via the gear icon in the
toolbar (`reopenConfig()`).

Layout: left-rail nav + single section body + always-visible preview strip at the
bottom + "Load Table" button. Sections:

| Id          | Component                 | Purpose                                                    |
| ----------- | ------------------------- | ---------------------------------------------------------- |
| `columns`   | `ColumnConfigTab`         | Column visibility, role, display format, per-column filter |
| `filters`   | `ColumnFiltersTab`        | Big per-column filter editor (categorical or range)        |
| `style`     | `StyleSection`            | Color / line / casing / hover / selection style            |
| `management`| `ManagementTab`           | Rename + edit-mode (saved tables only)                     |
| `ide`       | Inline placeholder        | Reserved                                                   |

The body uses `overflow: hidden` when the Filters section is active (that section
manages its own internal scrolls); otherwise it's `overflow: auto`. The preview strip
(`TablePreviewStrip`) always shows the current column config + applied filters as a
20-row TanStack table — identical columns / order / formatting to what the main grid
will show once committed.

**Close behavior.** The dialog's X button and backdrop click call `dismissConfig()`
(just flips `needsConfig: false`). The full `close()` — which wipes the events store
— is reserved for the trash-can button in `TableToolbar`.

---

## 4. Columns tab

### 4.1 Header (single compact row)

- Stats: `N/M enabled · K filterable` with a blue chip showing active-filter count.
- Search input scoped to column names (Escape clears).
- Tri-state visibility segmented control: **All / Enabled / Not enabled**.
- **Enable / Disable** bulk buttons. Their labels say "visible" when a search filter
  narrows the list; otherwise "all".

### 4.2 Grid

Columns: `COLUMN · ACTIVE · FILTER TYPE · DISPLAY · FILTER`.

- **Role dot + name** on the left. Role → dot color comes from a shared palette
  (`ROLE_STYLE`) also used by the filter chips.
- **Active switch** — when flipping a column on for the first time (role is still the
  default `text`), `detectColumnRole` (`src/features/table/lib/columnDetect.ts`)
  classifies the values (`numeric` / `dropdown` / `text`) and a matching filter
  default is seeded via `inferFilterDefaults`.
- **Role select** — soft-tinted tablet (see `ROLE_STYLE`). Changing the role also
  seeds or clears a filter default when it enters / leaves the filterable set
  (`dropdown | range | numeric`).
- **Display select** — `auto / currency / integer / number / date / percent / text`.
  `auto` falls through to `inferCellFormat(name, role)` (name-pattern heuristics).
  The display value is written into `ColumnConfigEntry.displayFormat` and drives the
  cell-display formatter AND the numeric editor's start / end adornments (`$` / `%`).
- **Filter chip** — when the column is filterable:
  - No filter set → dashed "Add filter" pill. Clicking seeds defaults and opens an
    inline `FilterPopover`.
  - Filter active → solid blue chip with a live summary ("3 values" / "25–80").
    Clicking opens the same popover for editing.

### 4.3 Display format inference

`formatCell.ts` handles both the display formatter and the role inference used by
the editors (to decide adornments). Currency triggers on `cost|price|amount|benefit|
revenue|budget|fee|expense|spend|usd|dollars?` (or literal `$`). Percent on
`pct|percent|percentage|rate` (or `%`). Date on `date|time|installed|established|
expires|created|updated|modified`. Integer on `count|segments|num|qty|year|id|#`
when the role is numeric. The fallback for numeric roles is `number` (grouped,
up to 4 decimals).

---

## 5. Filters tab

Two-pane layout with NO nested scrolls:

- **Left pane.** Scrollable list of filterable columns (role `dropdown | range |
  numeric`). Each row shows name, role chip, and a one-line summary of the current
  filter (`"3 of 12 selected"` or `"25–80"`).
- **Right pane.** The editor for the selected column. Only ONE scroll region lives
  inside (the value list or the slider body); header + search are pinned.

### Categorical editor

Search input + **Select all / Clear** + dense checkbox list. `selected: []` means
"everything passes" (empty selection is not a filter). Search "visible selected"
count shows in the footer when the query narrows the list AND something is
selected inside that slice.

### Range editor

- 30-bin histogram across the value distribution, colored per-bin: blue for bins
  inside the current range, slate for outside.
- Two-thumb slider over `[bounds.lo, bounds.hi]`. Bounds are the full data range;
  `min / max` are the user's current selection.
- Editable min / max numeric inputs + a Reset-to-full-range icon in the header.

Filters compose as AND via `applyColumnFilters(rows, filters)` (used by the main
grid, the preview strip, and `toMapLibreFilter` so the map layer hides the same
rows).

---

## 6. Style tab

Three collapsible accordions.

1. **Color** (expanded by default). Column selector, opacity slider, type radio
   (`range | mapping | other`). Mapping panel lists every distinct value with a
   `react-colorful`-powered `ColorSwatch`. Range panel computes numeric bins
   (`linear | distributed`) × a ramp (`whiteToRed | yellowToGreen | blueToRed |
   whiteToPurple`), bin count 3-20.
2. **Line**. Width multiplier (0.5×–2.5×) and dash pattern toggle + `[dash, gap]`
   inputs.
3. **Casing**. Tabbed sub-panel for **BASE / HOVER / SELECT** casings. Each has a
   toggle, color swatch, and extra-width stepper. Hover / select also get their
   own core-line color.

A small SVG "line sample" at the top of the section renders the current casing +
dash + width live.

`commitConfig()` translates the draft `layerStyle` into `eventsStore.config.eventStyle`
so the map layer updates.

---

## 7. Management tab (saved tables only)

Compact grid layout:

- **Status line.** Green badge showing the loaded-saved name when available; orange
  warning when not (points the user at the toolbar Save button).
- **Name input.** Rename the saved table. Commits on blur or Enter; reverts on
  Escape, empty, or duplicate name. Uses `renameSavedTable(old, new)`, updates
  `loadedSavedName` (which also updates the `?table=` URL param via
  `useSavedTableUrlSync`).
- **Edit mode.** Tri-state segmented control: **Off / Autosave / Diff**. Tooltips
  explain each mode. Switching `diff → off|autosave` discards the `pendingDiffs`
  buffer.
- **Pending summary** (diff mode only, when buffer is non-empty). Single-line readout
  of `X cells · Y rows [· N new] [· N removed] · Press Save to persist.`

---

## 8. Live table — TableGrid

The live grid lives in `TableGrid.tsx` (sidebar panel). Mounted components:
`TableToolbar` + `TableGrid` + `TableFooter` + `TableConfigDialog`.

### 8.1 Rows

- Rows come from `useTableRows` which applies, in order:
  `applyColumnFilters → map-bounds filter → text filter` (all ANDed).
- In diff mode the component-level `rows` memo additionally:
  1. Filters to rows with pending diffs when `showOnlyDiffs` is on (updates + deletions).
  2. Appends `pendingDiffs.added` rows (negative `_idx`) at the tail so they show
     alongside real events.

### 8.2 Columns

`buildTableColumns(columnConfig)` (shared with `TablePreviewStrip`):

- Geom columns (RouteID, BMP, EMP) come first and are pinned left via
  `position: sticky` with cumulative `left` offsets, using per-role fixed widths
  (`72 / 68 / 68`). Everything else is 140px wide.
- Meta fields: `pinnedLeft`, `isLastPinned`, `headerTitle`.

### 8.3 Pagination

Auto-fit: a `ResizeObserver` picks `pageSize = floor(availableH / MIN_ROW_HEIGHT)`
then stretches each row to `availableH / pageSize` so the page fills the container
exactly with no vertical scroll. Selecting a row off-page scrolls to the right page
first.

### 8.4 Selection + hover

- **Map → table.** The events layer's mousemove / click handlers set
  `tableStore.hoverRowIdx / selectedRowIdx`. TableGrid pages + scrolls the row into
  view on selection change.
- **Table → map.** The events layer subscribes to both and filters the
  `events/line-hovered` / `events/line-selected` layers to the matching `_idx`.
- **Selection side effects.** `useRowClickZoom` fetches the route feature and fits
  the map to the segment bbox. `useLrsEditSync` auto-clears LRS mode on row change.
  `TableGrid` itself auto-clears `editingRowIdx` on row change too.

### 8.5 Header extras

- **Sort arrow.** Click a header to toggle sort. The active direction is persisted
  (`tableStore.sorting`) so saved snapshots round-trip sort state.
- **Filter icon.** Filterable columns show a tiny filter icon to the right of the
  sort arrow. Click opens the same `FilterPopover` used on the Columns tab.

---

## 9. Editing model

Editing is only enabled for saved-snapshot sessions (`loadedSavedName` set).
`editMode` picks one of three strategies:

| Mode       | Behaviour                                                                                                                   |
| ---------- | --------------------------------------------------------------------------------------------------------------------------- |
| `off`      | Cells are read-only. Double-click is a no-op.                                                                               |
| `autosave` | Every commit writes through to `eventsStore.updateEventValue` — the map re-tiles on the next tick. Save persists to browser.|
| `diff`     | Commits stage into `pendingDiffs`; the map doesn't see them until Save. Yellow accents highlight pending cells.             |

### 9.1 Row unlock (double-click)

In `autosave` / `diff`, a row must first be **double-clicked** to become "edit-
unlocked". This prevents a stray cell click from dropping the user into an editor.
The state is `tableStore.editingRowIdx`. Double-click on a cell:

1. Calls `setEditingRowIdx(rowIdx)`.
2. Opens that exact cell's editor via `setActiveEdit({rowKey, columnId})`.

Cell-level double-click `stopPropagation`s so the tr's own handler doesn't fire
again. LRS-edit rows and pending-added rows are always implicitly unlocked — no
double-click required.

Selecting a different row clears `editingRowIdx` (via an effect in TableGrid).

### 9.2 EditableCell

`EditableCell` is stateless; the parent drives `editing`, `onRequestEdit`,
`onFinishEdit`, `onCommit`, `onAdvance`.

- **Text / numeric / dropdown / RouteID** editors are selected by `role`.
- Numeric shows `$` prefix for `currency` and `%` suffix for `percent` (resolved
  format — explicit or inferred).
- RouteID uses MUI Autocomplete backed by `/api/autocomplete`. Picking a RouteID
  commits AND advances focus to the row's BMP cell via
  `AdvanceHint { kind: 'role', role: 'BMP' }`.
- Geom roles (RouteID / BMP / EMP) are read-only unless `allowGeomEdit` is true
  (pending-added rows, LRS-edit rows).
- `onCommit` fires **only** when the value actually changed (prevents Tab-through
  no-ops from staging diffs).
- `onAdvance` fires on every Tab / Enter / role-jump even when the value didn't
  change — so focus still moves.
- Autocomplete editors get explicit `focus() + select()` in a mount effect so
  double-click → type-to-replace works without requiring a third click.
- Inputs fill the entire cell (no border of their own; the td's `.cell-editing`
  purple frame provides the boundary).

### 9.3 Tab navigation

`TableGrid.resolveAdvance({rowKey, columnId}, hint)` translates an `AdvanceHint`
into the next cell to open. `next` / `prev` walk through `visibleColumnIds`; `role`
jumps to the first `used` column matching that role in the same row. The caller
sets `activeEdit = target`; the new cell's auto-focus hook handles the caret.

### 9.4 LRS edit mode

Triggered by the MoreVert menu item "LRS edit selected row" OR `Cmd/Ctrl+L`.
`tableStore.lrsEditRowIdx = selectedRowIdx`. While set:

- Row painted green (`tr.lrs-edit`).
- RouteID/BMP/EMP unlocked (`allowGeomEdit: true`). Other cells on the LRS row
  are opened with the normal editor but stay LRS-mode-tracked; clicking any
  non-geom cell OR any other row drops LRS mode.
- `useLrsEditSync` flips the app into `flow: 'line'` and calls
  `roadStore.loadSegment(routeId)` so the on-map `SegmentSlider` appears. Dragging
  it writes back to the row's BMP/EMP as pending diffs (or autosave updates).
- Row → road is also bidirectional: typing BMP/EMP in the cell moves the slider,
  clamped to the route's `bmpEmpMax`.
- A debounced `map.fitBounds()` fires after every measure edit so the map always
  frames the current segment.
- Picking a new RouteID in the cell triggers a full `loadSegment(newId)`; if the
  row's prior BMP/EMP fall outside the new route's bounds, they reset to the full
  route.

Exits: selection change, cell focus on a non-geom cell of another row, the menu
item pressed again, or `Cmd/Ctrl+L` on the same row.

### 9.5 Pending diffs (diff mode)

Three buckets under `tableStore.pendingDiffs`:

- `updates[idx][column] = value` — real-row edits.
- `added[]` — new rows staged via the MoreVert "Add new row" menu item or
  `HomePanel`'s segment-mode Add chip. `_idx` is assigned negatively so the marker
  won't collide with real events.
- `deleted[]` — real-row indices staged for removal. Added rows slated for removal
  are dropped directly from `added` by `stagePendingDelete` (no deletion needed).

Row / cell visuals while diff mode is active:

- Updated cell → yellow wash + orange left-border inset.
- Any cell in a row with updates → the geom cells (RouteID/BMP/EMP) also get the
  yellow wash so the user can visually trace which row a single-cell diff belongs
  to.
- Pending-added row → green wash + green left-border on the first cell.
- Pending-deleted row → red wash, strikethrough text, reduced opacity + red
  left-border. Locked (not editable).
- Actively-edited cell → muted purple wash (`#f3e8ff`) + 1px lavender inset,
  padding zeroed so the editor fills edge-to-edge.
- Geom cells on an editing (dbl-click-unlocked) row → same muted purple as the
  active cell (signals that geom cells are ALSO unlocked for edit, not just free-
  form columns).

`applyPendingDiffs()` runs at Save time. Order:

1. Patch updates against original indices.
2. Drop deleted indices, keeping a new `kept[]` array.
3. Reassign `_idx` on `kept` so indices match positions.
4. Append pending-added rows with fresh `_idx`.
5. Write back via `eventsStore.setConfig({ events })` (single write → single
   rerender → single re-tile).

Returns `{ updates, added, deleted }` counts for the Save toast.

---

## 10. Toolbar

`TableToolbar` layout (top to bottom):

- **Global text filter** (`filterText`) — substring match across stringified values.
- **Icon row.** Left to right:
  - Saved-tables dropdown (disabled when empty). Shows each entry with row count +
    save date + per-row delete button. Picking one loads the snapshot.
  - **Map** checkbox — `filterByMapBounds`. Tooltip: filter to features currently on
    screen.
  - **Diffs** switch — `showOnlyDiffs`. Only visible when `editMode === 'diff'`.
    Toggles row filtering to pending-diff rows.
  - **MoreVert (ellipsis) — Diff actions menu.** Only visible when
    `editMode === 'diff'`. A yellow badge on the top-right of the button shows the
    pending-rows count. Menu items:
    - Header: "PENDING CHANGES — N cells · M rows" (stat tile).
    - **Add new row.**
    - **LRS edit selected row / Exit LRS edit mode.**
    - **Remove row / Restore row** (real rows stage deletion; added rows drop).
    - **Discard all changes** — clears the buffer AND turns off `showOnlyDiffs`.
  - **Save icon** — opens the Save modal. Turns orange when diff mode has pending
    changes; turns blue when a saved table is loaded (overwrite mode). Disabled
    when events are empty.
  - **Settings gear** — `reopenConfig`.
  - **Export menu** — CSV / XLSX.
  - **Trash** — `clearTableData` (full reset, wipes the events store).
  - Source chip (sourceName, "📄" / "🌐").
- **Active filter chips** (only shown when at least one column filter is active):
  dismissible chips per column + a "Clear all" dashed chip.

### 10.1 Save modal

`SaveTableModal` has two modes decided at open time:

- `new` — text field for name; Enter commits. Duplicate-name shows a warning
  (saving is still allowed but flips the button label to "Save (overwrite)").
- `overwrite` — no name field; just a confirm button auto-focused so Enter commits.

A `Dialog.onKeyDown` captures Enter globally so Cmd/Ctrl+S → Enter works without
reaching for the mouse. Escape closes.

Save flow:

1. If `editMode === 'diff'`, `applyPendingDiffs()` runs first.
2. `saveTable(snapshot)` writes to `localStorage['nexuslrs.savedTables.v1']`
   (schema version 1). Snapshot includes events, geomfields, columnConfig,
   columnFilters, filterText, filterByMapBounds, sorting, layerStyle, eventStyle,
   editMode.
3. `setLoadedSavedName(name)` updates the store, which propagates to the URL
   (`?table=<name>`) and flips the Save icon's overwrite affordance.

The global `Cmd/Ctrl+S` shortcut bumps `saveRequestToken` on the store; the
toolbar subscribes with a ref-sentinel useEffect and opens the modal. The shortcut
always calls `preventDefault()` (even from inside an input) so the browser's "Save
Page" never fires; if the active element is typing, it's blurred first so any
cell editor commits its draft.

### 10.2 Saved-table URL sync

`useSavedTableUrlSync` (mounted in MapPage):

- **On mount.** Reads `?table=<name>`. If the snapshot exists, calls
  `loadFromSaved(name)` and flips active panel to Table. If it doesn't exist,
  strips the stale param.
- **While mounted.** Subscribes to `loadedSavedName`; writes (or clears) the param
  via `history.replaceState` so no navigation / back-button entry is created.

### 10.3 Sidebar width persistence

`uiStore.panelWidth` is seeded from `localStorage['nexuslrs.appSettings.v1']`
(clamped `[200, 900]`). The setter persists through the store action so resize
drags survive reloads. Kept separate from the saved-tables key so clearing
snapshots doesn't wipe the width preference.

---

## 11. Footer

One line: rows-per-page chip + prev/next pager + summary text.

- No active filter: `Showing {pageSize} of {total} rows` (sub text.secondary).
- Active filter: `Filtered: {visible} of {total} rows` (blue + semibold).

"Active filter" means any `columnFilter` with a non-full-bounds range or a
non-empty categorical selection. Text / map-bounds filters don't flip the label
(they're temporary and always visible in the toolbar).

---

## 12. Events map layer integration

`src/features/events/layer.ts` declares six line layers drawn in strict bottom-to-
top order so casings sit under cores:

```
events/line-casing
events/line
events/line-selected-casing
events/line-selected
events/line-hovered-casing
events/line-hovered
```

All layers use `line-cap: 'butt'` + `line-join: 'miter'` (the "flat end adornment"
look). Widths come from `lineWidthExpression` / `casingWidthExpression` in
`events/paint.ts`, scaled by `eventStyle.widthScale` and with `+widthDelta` added
for each casing.

Filter composition for the base layers (`line-casing` + `line`):

```
['all',
   ['in', ['get', '_idx'], ['literal', cfg.filter]],  // idx allowlist (if any)
   toMapLibreFilter(columnFilters),                   // per-column filters
]
```

Selected / hovered layers filter only by `_idx` so the highlight survives even if
the row would otherwise be filtered out.

The `select` / `apply` cycle rewires paint props (color expressions, opacity,
dash, casing color, widths) every tick; MapLibre's paint-property identity cache
makes unchanged values cheap.

---

## 13. Keyboard shortcuts (table-scoped)

Defined in `useGlobalShortcuts` (ignored when typing into most inputs unless
noted):

| Shortcut                    | Action                                                                            |
| --------------------------- | --------------------------------------------------------------------------------- |
| `Cmd/Ctrl+S`                | Request Save; always `preventDefault`s. Blurs the active input first so the       |
|                             | pending cell edit lands in the buffer before the snapshot.                        |
| `Cmd/Ctrl+L`                | Toggle LRS edit mode on the selected row. Flips editMode to `diff` if it was off. |
| `Cmd/Ctrl+ArrowLeft/Right`  | Paginate when the Table tab is active. No toast; silent at page boundaries.       |
| `Cmd/Ctrl+1..4`             | Switch sidebar tab (Home / History / Analyze / Help).                             |
| `Cmd/Ctrl+C`                | Copy map link (routehash).                                                        |
| `Cmd/Ctrl+O`                | Flip playback direction.                                                          |
| `Cmd/Ctrl+M`                | Toggle hover readout.                                                             |

---

## 14. Integrations to the rest of the app

### 14.1 HomePanel segment-mode "Add"

In line mode with a road segment selected, the `Add` action chip is enabled when
a table is loaded. It:

1. Stages a pending-added row via `stagePendingAddedRow({RouteID, BMP, EMP})`
   using the table's actual `geomfields` names (not hardcoded `RouteID`/`BMP`/`EMP`).
2. Auto-flips `editMode` to `diff` if it wasn't already (so the green highlight
   shows on the new row).
3. Switches the active panel to `table` so the user sees the row immediately.
4. Toasts `Added {routeId} {bmp}–{emp} as a pending row`.

Disabled otherwise with a tooltip explaining why (no table loaded, no segment
selected, etc.).

### 14.2 Left rail Table tab

Always clickable. When no table data is loaded, the panel shows an empty-state
pointer ("upload Excel or load an event layer to begin") and the toolbar still
renders — so the user can pick a saved table from the dropdown without needing
data loaded first.

---

## 15. localStorage layout

Two keys, both JSON:

- `nexuslrs.savedTables.v1` — map of `{ [name]: SavedTable }`. Each SavedTable
  includes `version`, `savedAt`, `source`, `sourceName`, the full `events` array,
  `geomfields`, `columnConfig`, `columnFilters`, `filterText`,
  `filterByMapBounds`, `sorting`, `layerStyle`, `eventStyle`, `editMode`. The
  `pendingDiffs` buffer is intentionally NOT persisted — staged edits must be
  applied via Save.
- `nexuslrs.appSettings.v1` — `{ panelWidth?: number }`. The only current key
  but the file shape is open-ended for future app-wide preferences.

---

## 16. Behavior matrix summary

Quick reference for the "what do I see when I interact with a cell?" question:

| Scenario                                    | Click        | Double-click     | Type after opening                                |
| ------------------------------------------- | ------------ | ---------------- | ------------------------------------------------- |
| `editMode: off`                             | Row selects  | No-op            | n/a                                               |
| `autosave` or `diff`, row not unlocked      | Row selects  | Unlocks + opens  | n/a                                               |
| `autosave` or `diff`, row already unlocked  | Cell opens   | Also opens       | Edits the cell                                    |
| Pending-added row                           | Cell opens   | Cell opens       | Edits the cell                                    |
| LRS-edit row, geom cell                     | Cell opens   | Cell opens       | Edits route / measures; slider syncs              |
| Pending-deleted row                         | Row selects  | No-op            | Locked                                            |
| `editMode: off` or no saved table           | Row selects  | No-op            | n/a                                               |

---

## 17. Visual styling reference

Colors / roles used across the feature (a cheat-sheet for future changes):

- **Role dots**: text `#3b82f6`, dropdown `#10b981`, numeric/range `#f59e0b`,
  RouteID `#06b6d4`, BMP `#22c55e`, EMP `#ef4444`.
- **Filter chips**: active `#dbeafe / #93c5fd / #1e40af`. Dashed empty slot
  `#cbd5e1`.
- **Diff accents**: updated cell `#fef9c3 + #f59e0b`. Added row `#ecfdf5 + #10b981`.
  Deleted row `#fef2f2 + #dc2626`.
- **Edit state**: active cell `#f3e8ff + #c4b5fd`. Row unlocked (tr.editing)
  `#eff6ff + #2563eb`. LRS row `#bbf7d0 + #16a34a`.
- **Hover on editable cell**: dashed `#93c5fd` outline on the td itself (so the
  affordance fills edge-to-edge).
