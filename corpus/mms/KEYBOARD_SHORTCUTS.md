# MMS Application - Keyboard Shortcuts

This document provides a comprehensive list of all keyboard shortcuts available in the MMS (Maintenance Management System) application.

## Global Shortcuts

These shortcuts work across the entire application:

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Ctrl/Cmd + K` | Toggle Layer Sidebar | Opens/closes the layer selection sidebar |
| `Ctrl/Cmd + X` | Clear All Filters | Clears all active filters without zooming the map |

## Layer Sidebar Shortcuts

When the layer sidebar is open (toggle with `Ctrl/Cmd + K`):

| Shortcut | Action | Description |
|----------|--------|-------------|
| `1` - `9` | Quick Layer Select | Press a number key to instantly select that layer |
| `C` | Open OASIS Integration Job | Navigates to the OASIS Integration Job page |

Layers are numbered 1-9 in display order. The number badge appears next to each layer name when the sidebar is open.

---

## Map View (`/map`)

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Ctrl/Cmd + M` | Switch to Table View | Switches from map view to table view for the active layer |
| `Escape` | Exit Multi-Select Mode | Cancels multi-select mode if active |

---

## Table View (`/table/:tableName`)

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Ctrl/Cmd + M` | Switch to Map View | Switches from table view to map view |

---

## Task Screen (`/tasks/:taskId`)

### Tab Navigation

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Ctrl/Cmd + 1` | Details Tab | Switch to the Details tab |
| `Ctrl/Cmd + 2` | Accomplishments Tab | Switch to the Accomplishments tab |
| `Ctrl/Cmd + 3` | CMP Tab | Switch to the Core Maintenance Plan tab |
| `Ctrl/Cmd + 4` | Costs Tab | Switch to the Costs tab |
| `Ctrl/Cmd + 5` | Notes Tab | Switch to the Notes tab |
| `Ctrl/Cmd + 6` | History Tab | Switch to the History tab |

### Sidebar Controls

| Shortcut | Action | Description |
|----------|--------|-------------|
| `~` (tilde) | Toggle Asset Sidebar | Opens/closes the left asset reference sidebar |
| `Ctrl/Cmd + K` | Toggle Layer Sidebar | Opens/closes the right layer sidebar |
| `Ctrl/Cmd + M` | Toggle Asset Sidebar | Alternative shortcut to toggle the asset reference sidebar |

### Asset Management
(These shortcuts only work when the asset sidebar is open)

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Ctrl/Cmd + A` | Add Asset | Opens the "Add Asset" dialog (only when sidebar is open) |
| `Ctrl/Cmd + S` | Save Asset List | Saves changes to the asset reference list (only when sidebar is open and not in create mode) |
| `Ctrl/Cmd + Arrow Left` | Previous Asset | Navigate to the previous road asset in the list (wraps around) |
| `Ctrl/Cmd + Arrow Right` | Next Asset | Navigate to the next road asset in the list (wraps around) |

---

## Data Grid Navigation

These shortcuts work in all DataGrid components (CMP tab, Costs tab, Accomplishments tab):

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Arrow Left` | Previous Page | Navigate to the previous page in the grid |
| `Arrow Right` | Next Page | Navigate to the next page in the grid |

### Components with DataGrid Navigation:
- **CMP Tab** - Core Maintenance Plan associations
- **Costs Tab** - Labor, Equipment, Stockpile, and Other costs
- **Accomplishments Tab** - Daily work report accomplishments

---

## Accomplishment Editor (`/accomplishment-editor`)

The Accomplishment Editor provides a spreadsheet-like interface for rapid bulk entry of Daily Work Report Line Items (accomplishments).

### Global Controls

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Ctrl/Cmd + A` | Focus Activity | Jumps focus to the Activity autocomplete filter at the top |
| `Ctrl/Cmd + O` | Focus Organization | Jumps focus to the Organization autocomplete filter at the top |
| `Ctrl/Cmd + D` | Focus Last Row | Jumps to the last row and focuses on the Task Order ID cell for editing |
| `~` (tilde) | Focus Route Search | Jumps focus to the Route search autocomplete in the current row |

### Cell Editing

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Enter` | Finish Editing Cell | Stops editing the current cell and saves changes |
| `Tab` | Finish Editing & Move Next | Stops editing, saves changes, and moves to next cell |
| `Tab` (on accomplishment column) | Add New Row | When on the last column (accomplishment), adds a new row to the grid |

### Workflow Tips

1. **Fast Data Entry**: Use `Ctrl/Cmd+D` to quickly jump to a new row after completing one
2. **Quick Filter Changes**: Use `Ctrl/Cmd+A` and `Ctrl/Cmd+O` to change activity/organization without mouse
3. **Route Selection**: Press `~` (tilde) to quickly search for a route when on any row
4. **Blanket Tasks**: Tasks without asset references automatically skip Route/BMP/EMP cells and focus on Accomplishment
5. **Single-Point Assets**: Assets where from_measure = to_measure auto-populate both BMP and EMP, then skip to Accomplishment

---

## Image Viewer (Notes Tab)

When viewing attachments/images in the Notes tab:

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Arrow Left` | Previous Image | Navigate to the previous image in the gallery |
| `Arrow Right` | Next Image | Navigate to the next image in the gallery |
| `Escape` | Close Viewer | Closes the image viewer |

---

## Platform-Specific Notes

- **Mac Users**: Use `Cmd` (⌘) key for all `Ctrl/Cmd` shortcuts
- **Windows/Linux Users**: Use `Ctrl` key for all `Ctrl/Cmd` shortcuts

---

## Sidebar Components

The following sidebar components are available:

- **Bridges Sidebar** - Search and browse bridge features
- **Roads Sidebar** - Search and browse road features
- **CMP Sidebar** - Search and browse Core Maintenance Plan features
- **Layer Sidebar** - Select and manage layers (toggle with `Ctrl/Cmd + K`, press `1`-`9` to quick-select layers)

---

## Tips

1. **Multi-Select Mode**: When in map view, you can enter multi-select mode by shift-clicking features. Press `Escape` to exit.

2. **Asset Navigation**: Use `Ctrl/Cmd + Arrow Left/Right` to quickly navigate between road assets in the Task Screen. This allows you to review and edit multiple assets without clicking. Note: This only navigates through road assets (bridges are skipped).

3. **Data Grid Pagination**: The arrow key navigation for DataGrid pages only works when no input field is focused. The application automatically blurs the active element before navigating.

4. **Context-Aware Shortcuts**: Some shortcuts (like `Ctrl/Cmd + A` and `Ctrl/Cmd + S` in Task Screen) only work when certain conditions are met (e.g., sidebar must be open).

5. **Keyboard Navigation Priority**: Form inputs and text fields take precedence over global shortcuts. Make sure to blur/unfocus input fields if global shortcuts aren't responding.
