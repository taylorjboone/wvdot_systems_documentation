# Usage

**WVDOT Dock** is a shared place for WVDOT teams and authorized collaborators to
find documents, work on updates, and keep earlier versions. **DOCK** stands for
**Document Organization and Collaboration Keeper**.

WVDOT Dock exists to help people find the current file, know who is editing it, and
understand what changed. Folder access controls who can see and update documents;
check-out reserves a file for editing, and check-in saves the update with its history.
Search, tags, and comments help teams find information and work together without
losing track of earlier work.

This guide explains everyday tasks in WVDOT Dock, shortened to Dock below. For the
detailed rules behind the application, see [Business logic](/docs/business-logic).

## Open the development site

Open [Dock on mmsdev](https://mmsdev.transportation.wv.gov/dock/) and sign in with
your WVDOT account. The development site starts with a copy of the local
folders, documents, versions and permissions. Changes to either site’s document
list do not automatically appear in the other. Existing files remain available.

You can bookmark pages beneath `/dock/`, including all Docs pages.

## Sign in

Choose **Sign in with your WVDOT account**. Dock sends you to the WVDOT sign-in page
and brings you straight back. If you are already signed in to WVDOT on this computer,
it usually returns without asking you anything.

**Dock has no password of its own.** There is nothing to remember, nothing to change,
and nothing to reset — if you can sign in to other WVDOT systems, you can sign in to
Dock. Dock knows you by your employee number, and your folder access is attached to it.

If sign-in is refused, the message says why:

| Message | What to do |
| --- | --- |
| You do not have a Dock account yet | Ask a Dock administrator to set one up for your employee number. Sites that create accounts automatically never show this. |
| This Dock account has been deactivated | Ask a Dock administrator to restore it. |
| That sign-in attempt expired | Start again from the sign-in screen; an attempt is only good for ten minutes. |
| The WVDOT sign-in service is unreachable | Wait a moment and try again. If it continues, tell your administrator. |

Signing out of Dock ends your Dock session only. It does not sign you out of Windows
or of your WVDOT account, so signing back in may not ask you for anything. Dock
sessions last eight hours; after that, sign in again.

## Find and open a document

Choose **Documents**, then open a folder from the
sidebar or the list. Folders and files appear together. The folder's path runs across
the top of the page and ends with the folder you are in; click any folder in it to
move back up the directory.

The sidebar shows the first two levels of folders. Click the arrow beside a folder to
see what is inside; the folders leading to the one you are viewing open by themselves,
and so do the folders on the way to places you have been given access. A folder with
many subfolders lists them a hundred at a time — choose **Show more** for the next
hundred.

A folder's contents fill the space available and scroll within it, so the list never
runs off the bottom of the window and the column headings stay visible as you move
through it. You can drop files anywhere on that panel, including the empty space
below the last row. While a folder opens, grey placeholder rows show where its
contents will appear. A folder with more than a hundred files lists the first hundred
and says how many there are; the next hundred appear as you scroll to the end of the
list, and **Load more** at the end does the same. An empty folder says so and suggests
how to add to it.

To find a document by name or content, type in the search box at the top and press
**Enter**; press **Escape** or the **×** to clear it. You can narrow
results to a folder — type part of its name in **Search scope** and choose it from the
list — or include older versions. Results update as soon as you change a filter. Click
a result to open it.

You see the folders and actions available to your account. If something you need is
missing, ask your folder manager for access.

If a page cannot be displayed, Dock says so and offers **Try again** and **Reload**.
The sidebar and the other pages keep working.

## Open sidebar tools

**Administration** stays pinned to the bottom of the sidebar, leaving room for your
folders. Click it to open the panel above the button. Choose **Keep expanded** to
leave its links visible; click **Administration** again to collapse it to the bottom.
Dock remembers your choice on this browser for your account. Click outside the popup
or press Escape to close it without changing your preference.

The panel contains **Trash**, **Tags**, and **Docs**, plus the administration links
available to your role; administrators also see **Tagging pipeline**. Accounts without audit access see **Workspace tools** as the
button's name. On a small screen, open navigation using the top-left menu first; tap
the page beside it to close it again.

## Add files or folders

1. Open the folder where the files belong.
2. Choose **New** at the top of the sidebar, then **Upload files** or **Upload folder**.
   On a phone, **New** is the round **+** button at the bottom right. You can also drop
   files or a folder directly into the list or onto a folder in the sidebar. **New** is
   greyed out where you cannot add files, such as a folder you can only view.
3. Watch the upload tray until the files finish. Keep the browser tab open while
   uploads are running.

Folder uploads keep their nested structure. Dock sends up to eight files at a time, so a
folder of many small files finishes much sooner; a file over 250 MB goes one at a time
while smaller files keep moving. The upload tray shows one progress bar for the whole
upload, and the list of files catches up every 15 seconds and when the upload finishes.
For a very large upload the tray lists the files being sent, any that failed and the
most recent ones - up to a hundred - with a count of the rest and an estimate of the
time left, so it stays quick however many files you drop. If an item fails, choose **Retry failed**;
files that already finished stay saved. Each file can be up to 20 GB. For a file over 250 MB, Dock first
reads it through — the tray shows **Checking file** — and then sends it in pieces. If the
transfer stops, **Retry failed** checks the file again and carries on from the last
piece Dock received.

Uploading a file with the same name creates another document. To update an existing
document and keep its history together, use check-out and check-in instead.

## Select several items

Click a row to select it. Hold **Shift** and click another row to select everything
between the two, or hold **Ctrl** (**Command** on a Mac) and click to add or remove a
single row. The checkbox at the start of each row does the same, and the checkbox in
the heading selects everything listed. Press **Escape** to clear the selection. To
open an item, double-click its row or click its name.

A file opens over the folder, which stays just as it was behind it. While its preview
shows, press the **left** and **right arrow keys** — or **Previous file** and **Next
file** at the top — to move through the folder's files. Press **Escape**, choose **Close
document**, or use the browser's Back button to return to the folder.

Choose the grid button above the list to see folders and files as tiles instead of
rows, and the list button to switch back. Tiles select, drag and open just as rows do,
and Dock remembers your choice on this browser.

While items are selected, the bar above the list says how many and offers what you
can do with them: **Move to…**, **Download** for one file, **Download as ZIP** for one
folder, and **Archive** for files. Right-click a row, or choose its **⋮** button, for
the same actions; a right-click on a selected row acts on everything selected.

**Archive** takes files out of the folder list but keeps every version. Turn on
**Show archived** above the list to find them again and restore them.

You can do all of this from the keyboard. Click a row or press **Tab** to reach the
list, then use the **arrow keys** to move between rows, **Space** to select or clear a
row, **Shift** with an arrow key to extend the selection, **Enter** to open,
**Ctrl+A** to select everything listed, and **Shift+F10** or the menu key for the
actions.

## Move files and folders

Drag a file or folder from the list and drop it where it belongs:

- onto a folder in the list,
- onto a folder in the sidebar, or
- onto a folder name in the breadcrumbs above the list, to move it further up.

Dragging a selected row moves everything that is selected.

To move without dragging, choose **Move to…** from the bar above the list or from a
row's actions, type part of the destination folder's name and choose it from the list.

The destination is outlined while you hold the item over it. A folder that will not
accept the drop stays plain: you need permission to add items there and to remove
them from where they are now. Moving a folder into a part of the directory where different people
have access also needs permission to change access, because it changes who can reach
what is inside; within the same part of the directory it does not. The folder you are in, shown last in the breadcrumbs,
is not a destination.

A message confirms the move. If someone changed the item while you were dragging it,
Dock tries once more with the latest version; if it still cannot move it, the
message names the item and says why. A checked-out document cannot move until it is
checked in or the checkout is cancelled. Choose **Undo** in the message to put back
everything that moved.

## Download a folder

Right-click a folder's row, or open its **⋮** menu, and choose **Download as ZIP**. With
just that folder selected, the bar above the list offers it too. Dock first shows
how many files and how much data the folder holds, then **Download ZIP** starts the
transfer. The folder structure is kept inside the archive.

A folder download is one continuous transfer. It cannot be paused or resumed, so keep
the tab open until it finishes and start again if the connection drops. A folder with
more than 5,000 files or 25 GB cannot be downloaded in one piece; open a subfolder and
download that instead. Files you can see but are not allowed to open are left out, and
Dock tells you how many.

<!-- 2026-09-10: Reviewed the folder-listing speed-up and the change to how renamed
folders are re-tagged; finding, opening, check-out and check-in steps are unchanged for
end users. The per-file limit is now 20 GB, described under Add files or folders. -->

<!-- 2026-09-11: Reviewed moving several items at once, which now travels as one
request; what users do and see when moving is unchanged. -->

<!-- 2026-09-11: Reviewed parallel uploads and indexing on the server. Nothing users do
changes; several people's uploads no longer wait for one another. -->

<!-- 2026-09-10: Reviewed the faster Windows sync listing (what the client shows is
unchanged) and the in-page confirmation for switching off an account's access
control, which asks the same question as before. -->

## Update an existing document

1. Open the document and choose **Check out** to reserve it for your edit.
2. Choose **Download current**, open the downloaded file in your usual application,
   make your changes, and save it on your computer.
3. Return to Dock and choose **Check in**. Select your updated file. You may leave
   the check-in comment blank or add a description of your changes.

A large file takes a little longer: Dock checks it first and then sends it in pieces,
and the dialog shows each step. If downloading a large file is interrupted, your browser can
usually carry on where it stopped instead of starting again.

The new version becomes the current file and the earlier version stays in history.
Other people can still read the committed file while you edit. Use **Checked out by
me** in the sidebar to return to your reserved documents.

If you decide not to make an update, choose **Cancel checkout**. If another person
has the document checked out, ask them to check it in or contact a manager.

## Preview, history and comments

Open a document's **Preview** tab to view supported files or their extracted text; a
file with several pages turns with **Previous page** and **Next page**.
Use **Download current** to open the original file in your own application.

The **Metadata** tab holds the document's name and details. **Versions** shows earlier
files and check-in comments. Select two versions and choose **Compare selected** to see their text side by side and a
table of the details that changed. Restoring an earlier version makes it the basis of a new version, keeping
the intervening history. The comment for a restored version is optional too.

Use **Comments** to discuss the document and **Activity** to follow its changes.
Available editing and commenting controls depend on your access.

A file larger than 1 GB is not shown in the preview; download it to open it in its own
application.

## Use tags

The **Tags** tab shows a summary and facts found in the document: record types,
topics, people, organizations, roads, counties, districts, tracking numbers and dates.
Each automatic fact shows its supporting quotation and page. **Context suggestions**
come from names or folders rather than the document's contents, so they are kept out
of search until an editor chooses **Add as tag** to accept one.

Each automatic fact can also show how it was judged: whether it is a main subject of
the document, a supporting detail, or something mentioned only in passing, along with
how confident Dock is and whether the same fact appeared in several places. A fact
with no such note was published before that check could run; it is still supported by
its quotation.

Click a tag to open Search, then use **Filter by facets** to add more. **Match** sets
whether a result needs *every* selected facet or *any* of them; every selected facet
is the default. **Exclude facets** leaves out documents carrying a label you do not
want. Each choice shows how many documents you can open carry it, and the panel
reports how many match your current filters. You can search with filters alone. For
example, choose email, traffic signals, WV 51 and Leetown Road, then set **Document
dates from** to December 1, 2024. Date filters overlap the period described in the
document; records with unknown dates are excluded while a date filter is active.
Use the chips to remove individual selections, or **Clear all filters** to reset.
Bookmarks, reload and Back/Forward retain your selections.

Searching also looks at tags directly, so typing a road name or a tracking number
finds documents labelled with it even when the scanned text is hard to read, and two
spellings of the same contract number reach the same records. A result found only
through the document's generated summary says so, because that is a description
rather than words on a page.

Road facts can show a FuzzyRoad match, alternate names and supported milepost ranges.
The same name may belong to several road records. An **ambiguous** result has not
been automatically assigned a road identity. Editors can inspect the source, choose
**Review road identity**, and select **Confirm road**. Do not choose based on the
score alone; check the county, direction, route ID and the part of the road involved.
If road lookup is unavailable, the original tag still works and Dock retries later.

Browse labels from **Tags** in the bottom sidebar panel. Editors can add a tag with
its facet kind or remove an incorrect label. Manual labels, confirmed road identities
and removals survive automatic regeneration. **Regenerate automatic tags** also
refreshes road candidates, subject to the lookup cache. Old results stay available
while a replacement is being prepared; partial or failed analysis is identified.
If one suggested fact has no usable citation, Dock omits it and labels the analysis
partial while retaining the other supported facts.
Administrators can pause, retry failed work, or tag existing documents from the catalog.
If OCI is temporarily unavailable, the catalog shows the next automatic retry time.
Dock waits before resuming the queue; existing files and tags remain usable.
Existing documents keep the analysis they already have until an administrator chooses
**Tag existing documents**, so a change to how Dock reads records never re-runs the
whole library on its own.

## Watch the tagging pipeline

Administrators can open **Tagging pipeline** from the sidebar to see what Dock is
working on. It lists what is being read right now and which page or section it has
reached, what is queued and roughly when it will start, and what finished recently
with how many facts were kept and how many were refused. The view refreshes on its
own. A large scanned file can take a while; the page counter is how you tell reading
from stuck. If a worker stops partway the item is marked interrupted and picked up
again automatically.

The page also summarizes why facts were refused across the library. A suggested fact
whose quotation cannot be found on the page it cites is discarded rather than
published, so a rising count there usually points at unreadable scans rather than at
the documents themselves.

<!-- 2026-09-11: Reviewed supervisor dependency validation, dedicated controller deployment and cloud image-reference correction; administrator tasks below remain applicable. -->

<!-- 2026-09-11: Reviewed per-worker connection reuse; the capacity controls and user tasks below remain unchanged. -->

### Adjust processing capacity

Administrators can use **Processing capacity** on the Tagging pipeline page to choose
**Local only**, **Automatic cloud burst**, or **Pause new reading**, then select
**Save capacity**. Automatic capacity must first be configured by the deployment
administrator. It is configured on mmsdev with a normal limit of 64 and a maximum
of 128 extra readers. Normal and maximum worker limits control how much extra reading is
available for large imports. Cloud readers stop when their queue is empty. If repeated
cloud startup failures pause extra reading, the page explains the problem. Select
**Local only** and ask the deployment administrator to correct it before retrying;
local reading and previously available files continue. Cloud readers retry brief
server interruptions automatically. If Oracle temporarily refuses more readers,
Dock waits before retrying; existing readers and local processing continue.

Reading, search indexing, and tags/summaries have separate queue counts. Files remain
available while these stages finish. **Pause importing completed cloud results** holds
completed cloud work and pauses further cloud assignments until it is turned off and
saved. Model-region switches control which validated services can process text.
Each model region shows active calls and calls in the last minute against its limits.
Tags and summaries also show the token budget used or reserved in that minute. A full
budget means Dock is waiting for capacity, even when no call is active. These limits
are separate from the cloud reader count.
A region marked **Cooling down** will retry later; previously published results remain.
Long documents are read in smaller sections. A shortened combined summary is marked
partial; a missing relevance score does not remove a fact supported by the document.

A deployment administrator can publish and validate a worker release. Choose it under
**Validated release** and select **Activate** to use it, or select an earlier validated
release to roll back. Unfinished reading restarts automatically; finished results remain
available. Legacy Word, Outlook message and Excel files can now be read. Message
attachments and legacy spreadsheet formulas/embedded objects are not fully extracted;
Dock labels these results incomplete and retains the original for download.

## Organize folders and manage access

Choose **New → New folder** to create a folder inside the one you are viewing, when that
action is available. The **▾** beside the folder's name lists what you can do to the
folder itself — **New folder**, **Upload files**, **Upload folder**, **Download as ZIP**,
**Folder settings** and **Manage access**, as your permissions allow. **Folder settings**
provides rename and move controls according to your permissions: to move a folder,
type part of the new parent folder's name in **Parent folder** and choose it from the list.

### Two sets of permissions

Open **Permissions** from the bottom sidebar panel, **Manage access** in the folder's
**▾** menu, or **Manage who can use this folder** in Folder settings. Every folder has two separate sets:

- **This folder** — seeing the folder, renaming it, adding folders inside it,
  deleting it, and changing who has access.
- **Documents in this folder** — reading a document's record, editing its properties,
  opening the file, checking new versions in, and releasing someone else's checkout.

Permission to rename a folder is not permission to edit the drawings in it, and the
two are set separately.

The distinction that matters most day to day is between a document's **record** and
its **file**:

| You want someone to | Give them |
| --- | --- |
| Find a document and see its properties | Read |
| Keep properties up to date without opening drawings | Read and Write |
| Look at a drawing without changing it | Read and File Read |
| Edit drawing content without changing properties | Read, File Read and File Write |
| Edit both the drawing and its properties | Read, Write, File Read and File Write |
| Take over a file someone left checked out | Free |

Some permissions switch others on because they need them. File Write switches on Read
and File Read, because you cannot check a file in without being able to open it. Those
appear ticked but faded, with a note saying what requires them. File Write does **not**
switch on Write: editing a drawing and editing its properties stay separate.

### Assigning access

Each row is one person, group or access list. Use **Permission set** to apply a familiar
set in one step — Viewer, Reviewer, Editor, Controller or Manager — then adjust individual
boxes if you need something those do not cover. The set changes to **Custom** as soon as
you tick something off the pattern.

Permissions add up. If someone is in two groups, they get everything both groups allow.
To stop someone reaching a folder, tick **No access** for them: that denies
everything, whatever any group or list also grants. Clearing every box is not the same
thing — it simply contributes nothing.

Nothing is saved until you choose **Save changes**. The bar at the bottom lists what you
changed, and **Discard** puts it back.

### Where access comes from

The chain across the top of the page shows the folders above this one. A filled marker
means that folder sets its own access; an open marker means it takes what reaches it
from above. Selecting one opens its access.

A folder keeps inheriting until it has assignments of its own. The moment it has any,
it stops inheriting and its own list is the whole answer. So that this never quietly
removes anyone, Dock copies what the folder was inheriting into it when you start
assigning, and tells you it has done so. If you then remove one of those, Dock names
who would lose access before you save.

**Inherit access from the folder above** turns inheritance off for a folder that has no
assignments of its own, sealing it so that only the people you list can reach it.

### Checking who can do what

**Effective access** on the right answers the question directly. Type part of a person's
name or employee number, choose them, and it shows what they can do here, then explains how that was decided: which folder the access
came from, which group or access list carried it, and anything that took some of it away.
Use it before you change something and again afterwards.

**Export as CSV** produces a spreadsheet of the assignments on a folder and everything
beneath it, which is easier to review than opening folders one at a time.

### One document that needs different access

Open the document and choose the **Access** tab. While it has nothing of its own it
follows its folder, shown greyed out. Adding anyone gives that document its own access,
and its folder's document permissions stop applying to it. **Follow the folder again**
removes the exception.

### People, groups and access lists

Administrators use **People & groups** to find accounts, add or remove group members,
and save account changes. An account set up before Dock moved to WVDOT sign-in has no
employee number, and nobody can sign in to it; **Edit account** offers the field while
that is so. Attaching one keeps the account's groups and folder access with that
person, instead of starting them over on a new account. It can only be set once —
moving an employee number to a different account would hand over everything the first
account can reach, so ask your administrator to arrange that deliberately.

Choosing someone in **Add member**, **Add to group** or **Add an owner** adds them straight
away; the remove button beside a person takes them off. **Delete group** and **Delete
access list** ask you to confirm first.

**Add person**, at the top right of the Users tab, sets an account up before that person has ever signed in, so their folder access is ready on their first visit: enter their employee
number, and Dock fills in the name and address from their WVDOT account when they
arrive. People are listed under the name their WVDOT account carries, with the employee
number beneath it; searching finds them by either.

- A **group** collects people who need the same access.
- An **access list** combines groups, people and other access lists into one thing you
  can assign. Build a project team once from the groups you already have, then assign
  the list wherever that team works.

Both can have **owners**. An owner keeps the membership up to date without receiving the
access themselves, so a project manager can look after a team's membership without being
given every permission that team has.

### Account settings

An account's own settings, on its page in People, limit what that person can do
anywhere — whatever a folder allows. Turning off **Modify documents**, for example, makes
documents read-only to that account everywhere. These only take capability away; they
never add any.

A folder can also have an **owner**, who can always change access to that folder and the
folders inside it, stopping where a folder is sealed.

## Delete and restore a folder

With management access, open the **▾** beside the folder's name, then **Folder settings →
Delete folder**. Dock says how many
folders and documents would move to Trash; choose **Delete now** to confirm or **Keep
folder** to go back. If a document is checked out, resolve that checkout first.

Deleted folder trees appear in **Trash**. Open Trash, find the folder, and choose
**Restore folder** on its row — or open it to see what it holds and choose **Restore
folder** there. Choose where it should go and adjust the name if necessary.
Earlier versions are retained. Files archived separately before the folder was deleted
remain archived after restoration.

## Your profile and help

Open the top-right account menu and choose **My profile** to view your access,
change appearance, or sign out. It shows the name and employee number on your WVDOT
account; Dock refreshes both each time you sign in. The theme button also switches light and dark modes.

**Docs** contains this Usage guide, the detailed **Business logic** reference, and
separate **Frontend change log**, **Backend change log**, and **Client change log**
pages. Choose [Client change log](/docs/client/change-log) to see Windows client
updates by version, including changes to Explorer, check-in and installation.
Use **On this page**
to jump to a section. You can bookmark page and section links or use your browser's
Back and Forward buttons to return to what you were reading.

<!-- Maintenance review: 2026-09-08. Separated end-user instructions from the technical
business-logic reference. Existing document workflows remain unchanged. -->

<!-- Maintenance review: 2026-09-08. Rewrote "Organize folders and manage access" for the
permission-set model: two sets per folder, the record/file distinction, permissions that
accumulate, No access, inheritance boundaries with carry-forward, the effective-access
explanation, per-document exceptions, access lists and ownership, and account settings.
Finding, opening, uploading, checking out, checking in, searching and tagging are
unchanged for end users; only how access is described and assigned has changed. Kept
schema, API and resolution details out of this guide; they are in the business-logic
reference. -->

## Use Dock on Windows

<!-- 2026-09-11: Verified signed 0.1.14.0 installer delivery to pilot Downloads; installation remains pending. -->

For the updated server, use Windows client **0.1.14.0**. Exit Dock from its tray
menu, open the supplied installer, choose **Update**, then reopen Dock. Updating
keeps your current account and workspace. Folder destinations now reflect whether
you may add files or subfolders there; a move that changes access may still require
your administrator. The Windows upload limit remains **250 MiB per file** on the
development site. Oversized files stay local and show an upload error; they are not
published. The website’s larger-file feature does not raise this Windows limit.

The Windows pilot adds **Dock** to File Explorer. Install the pilot package supplied
by your administrator, open Dock, enter the server address, and choose **Sign in with
your WVDOT account**. Your browser opens the WVDOT sign-in page and returns you to
Dock; the client asks for no password and stores none. Leave Dock open while you
complete the sign-in in the browser. Dock returns to the foreground and opens your workspace; any setup error also appears beside the sign-in button. For a new workspace, choose an empty local folder under **Connection settings**. Your accessible folders appear there. The default
server is `https://mmsdev.transportation.wv.gov/dock`. A saved server address takes
precedence; check the sign-in screen if you previously used another server. The Windows/Bentley pilot still needs verification on actual PCs.

<!-- 2026-09-10: Reviewed 0.1.13.0 Explorer registration cleanup; account-switch instructions remain accurate. -->

Signing in with a **different account** replaces the selected account-bound local
workspace automatically. Dock removes its Explorer entry, downloaded files, **unsent
local changes**, pending uploads and local recovery copies, then opens the new account
in the same folder. Server documents remain. Signing out alone, or signing back in
with the same account, keeps local work. If a file is open and blocks removal, close
it and sign in again. A folder that Dock does not already own must still be empty.
Server checkouts are not released by removing a local workspace; ask an administrator
if a checkout under the old account needs releasing.

If sign-in stays on “Waiting for your WVDOT sign-in” without opening a browser and
then reports “A task was canceled,” Dock could not reach the server for that attempt.
Check the server address in **Connection settings**. If the website opens normally,
exit Dock from its tray menu, reopen it and try again. If the problem returns, ask
your administrator to check the client connection; do not delete the workspace.


With Dock running, double-click a document in your Dock workspace. Choose **Open
read-only**, **Check out and open**, or **Cancel** before the editing application
opens. The dialog comes forward with keyboard focus when you open a file from Explorer.
The checkout choice appears when you have editing access; files already
checked out in this workspace open directly. This also works for downloaded files.
Files outside Dock keep their usual opening behavior. You can also use
**right-click → Dock → Open**. For a file type without a default
editing app, choose an app in Windows first.
Install the packaged Windows build to enable Dock's Explorer menu and status display;
running the loose application executable does not install those shell extensions.
After installing an update, choose **Exit Dock** from the Dock tray icon, then open
**Dock from the Start menu**. Close any older copy started from a development folder;
closing its window with **X** only hides it in the tray. **Exit Dock** removes its
double-click action, so keep Dock running while using the workspace.
Explorer's **Dock status** tells you who has checked out a file and whether local
changes await check-in. Windows' cloud/download icon describes local availability;
it does not mean you own the checkout.

After editing, close the editing application, choose **Check in**, and optionally describe your
changes. Leave the comment blank to check in without one. Use **My checkouts** in the Dock window to return to work you reserved.
If a transfer or confirmed folder action fails, use **Transfers → Retry selected operation**. Keep your local
files until Dock confirms the new version. **Undo checkout** preserves a recovery
copy before restoring the committed file.

Choose **Keep offline** to download a file or the readable documents in a folder.
Files you have downloaded can be read offline. Previously checked-out files can be
edited offline, but new checkouts and check-ins require a connection. Use **Sign in
again** when the session expires; your browser opens once more and returns you to Dock. Cached status includes its last refresh time.
Background refresh keeps the Dock window responsive and avoids rereading unchanged
files on every poll. Use **Refresh** to force a full local check if a saved edit
has not appeared yet. Checkout, check-in and server changes also trigger full checks.
If the desktop feels slow while the web app is responsive, your administrator can
use the local diagnostic report to distinguish local file scanning from server waits.

Paste new files or folders into your active Dock workspace while Dock is running.
They upload automatically after copying finishes, normally within about 30 seconds
when connected. This also includes new items left in that workspace while Dock was
closed. You do not need to review or approve each upload.

In **WVDOT Dock**, use the left sidebar to switch between **Directory**, **My
checkouts**, **Pending changes**, **Transfers** and **Recovery**. Summary cards show
your document, checkout and pending-edit totals. Search filters the document lists;
those totals continue to describe the whole workspace. **Open Explorer** stays at
the top right. In Directory, **More** contains New folder, History, Rename / move,
Undo checkout and Delete. Use **Account settings** for sign-in, sign-out and Exit.
On the sign-in screen, expand **Connection settings** to change the server or folder.

<!-- 2026-09-09: Reviewed sign-out guidance after Windows 0.1.10.0 validation and installer delivery; installation remains pending. -->

**Account settings → Sign out** returns you to the sign-in screen and stops syncing
on this PC, even if your Dock session has already expired. Your downloaded files,
local edits, pending uploads and checkouts remain; signing out does not check work
in or release a checkout. Sign in again with the same account to resume.

If the server cannot be reached, Dock still signs out locally and tells you it could
not confirm the server sign-out. If Dock reports it could not remove the saved
sign-in, that sign-in may return after restarting; ask your administrator for help.
Signing out of Dock does not sign you out of Windows or your browser's WVDOT account.

Choose **Dark mode** at the bottom right of the Windows client for a darker workspace.
The button changes to **Light mode** so you can switch back. It is available on the
sign-in screen too, takes effect immediately, and Dock remembers it on this Windows
profile after closing or signing out. The web app and File Explorer keep their own
appearance settings. If Dock says it could not save the preference, the selected
mode still works until you exit.
If dark cards appear on a white background or headings remain black, install client
0.1.8.0 or later. This corrects the main window colors and keeps your saved theme.

The **Uploads** indicator at the bottom of Dock shows waiting, upload progress and
completion. Click it to open **Transfers** for each file's status; hovering over the
Dock tray icon also shows the upload state. Keep Dock running until the upload finishes.
If disconnected, sign in again or reconnect. Network interruptions retry automatically.
An access, size or naming error appears in Transfers; resolve it and use **Retry selected
operation** for a queued failure. A file still open for writing waits until copying or
saving finishes. **Pending changes → Check for new items now** checks the folder again.
Existing documents still require checkout and check-in to publish edits.

Temporary, lock, backup and Windows folder-settings files stay local. Folder names and
nested folders, including empty folders, are retained when possible.
If a Windows name needs adjustment, inspect its Dock name before relying on an exact
CAD reference path. Referenced files are not automatically checked out.

Use Dock's **Rename / move** and **Delete** commands to confirm directory changes.
An Explorer rename/delete may be paused while Dock asks for confirmation. Deleting
a folder sends its tree to Dock Trash; deleting a single file archives it. Restore
these through the web app. If your access changes or someone releases your checkout,
open **Recovery** to find retained edits. Dock does not automatically publish them.

If Explorer says **“The cloud file provider exited unexpectedly”**, reopen Dock and
wait for **Connected**, using **Sign in again** if requested, then retry. Keep the
workspace and any unsent edits in place. You can download committed files through
the web app while a desktop problem is investigated. If Dock closes again, open
**View reliability history** in Windows and give your administrator the crash's
technical details. Updated clients also keep a diagnostic report at
`%LOCALAPPDATA%\Dock\logs\desktop.log`; provide that report if requested.

Closing the Dock window leaves it in the tray. Enable Dock in Windows startup settings
if you want it to start when you sign in.

To uninstall Dock, check in or copy out unsent work first. Use **Keep offline** for
any server files you want to keep on this PC, and wait for downloads to finish.
Choose **Exit Dock** from its tray menu, then run the supplied Dock uninstall
script under the same Windows account. It removes the app and Dock's pinned
Explorer entries together. Your downloaded files, local edits and recovery copies
remain. Online-only entries disappear from this PC; their server documents remain
available in the web app. Uninstalling does not check in or release your checkouts.
If Windows has already removed the app but Dock entries remain in Explorer, your
administrator can run the same cleanup again.

<!-- Maintenance review: 2026-09-08. Verified the Docker/Apache development site
and copied data. Retried extraction preserves existing files when outputs differ
between computers. Reviewed search permission-query optimization; everyday
document workflows, opening files and accessible results remain unchanged. -->

<!-- Maintenance review: 2026-09-08. Reviewed schema-first server deployment;
end-user access and document controls are unchanged by the deployment script. -->

<!-- Maintenance review: 2026-09-08. Installed Windows 0.1.5.0; verified the Uploads
button/list and one synthetic automatic upload against the development server. -->

<!-- Maintenance review: 2026-09-08. Compact desktop windows hide summary cards
to leave more room for documents; all navigation and actions remain available. -->

<!-- Maintenance review: 2026-09-08. Reviewed tagging schema preparation in the
combined commit. Existing user controls remain unchanged; pipeline integration
limitations are documented in Business logic. -->

<!-- Maintenance review: 2026-09-08. Rewrote tag guidance for verification scores,
context-suggestion promotion, facet match modes, exclusions and counts, tag-aware
search, and the new administrator Tagging pipeline page. Everyday document workflows,
check-out, versions and folder access are unchanged. -->

<!-- Maintenance review: 2026-09-09. Noted that the "no Dock account yet" refusal does
not appear on a site that creates accounts automatically, which mmsdev now does. No
other everyday instruction changed; the provisioning posture itself is recorded in
Business logic and Operations, not here. -->

<!-- Maintenance review: 2026-09-09. Added guidance for attaching an account that
predates WVDOT sign-in to its employee number, and why that is set once. Sign-in,
finding, opening, uploading, checking out, checking in, searching, tagging and folder
access are otherwise unchanged. Deployment and preflight details stay in Operations. -->

<!-- Maintenance review: 2026-09-09. Rewrote sign-in for the WVDOT identity broker:
added the "Sign in" section, the refusal table, what signing out does and does not do,
the Windows browser round trip, the employee number shown on My profile, and Add person
for setting an account up ahead of a first sign-in. Removed every mention of a Dock
password; there is no longer one to type, store, change or reset. Finding, opening,
uploading, checking out, checking in, searching, tagging and folder access are
unchanged for end users. Kept protocol, token-validation and provisioning details out
of this guide; they are in the business-logic reference. -->

<!-- Maintenance review: 2026-09-09. Folder listings became a fixed pane that scrolls
its own rows rather than extending the page past the bottom of the screen; noted the
scrolling list, the headings that stay put, and that the whole panel accepts dropped
files. Signing in, opening, uploading, checking out, checking in, searching, tagging
and folder access are unchanged. Layout mechanics stay in Business logic. -->
