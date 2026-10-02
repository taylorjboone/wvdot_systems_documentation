# Dock for Windows

Windows 11 x64 client for **Document Organization and Collaboration Keeper**. Uses
WPF/.NET 10, SQLite, Cloud Files placeholders, and a native Explorer command DLL.
No OCI credentials belong on a Windows workstation. All transfers use Dock's API.

## Build and install the pilot

On Windows 11 x64, install .NET SDK 10, Visual Studio 2026 Build Tools with Desktop C++,
CMake, and a Windows 11 SDK. From PowerShell:

```powershell
.\desktop\windows\scripts\build.ps1 -DevelopmentCertificate
.\desktop\windows\scripts\install-pilot.ps1 `
  -Package .\desktop\windows\artifacts\Dock-0.1.3.0-x64.msix `
  -DevelopmentCertificate .\desktop\windows\artifacts\Dock-development.cer
```

The build script creates a local development signing identity only when explicitly
requested. For organizational signing use `-CertificateThumbprint` instead. Do not
commit signing keys. Installation trusts the supplied pilot certificate for the
computer’s TrustedPeople store; run the certificate installation step as administrator
and verify its publisher before doing so. Restart Explorer after upgrading
the shell extension if Windows retains the old DLL.

For an upgrade, reuse the existing pilot signing certificate with
`-CertificateThumbprint` so the publisher identity stays the same. The corrected
package is version **0.1.3.0**, and its filename comes from the package manifest.
The build runs native CTest checks and the Windows desktop integration harness before
packaging. The latter invokes Explorer’s default action on isolated synthetic files
and checks inside/outside routing, explicit editor Open, and registration cleanup.
Close Dock before installing the update, retaining the workspace and local edits.

The native DLLs **must** be built and included. A successful cross-targeted WPF build
on macOS is not an installable or Windows-verified client. Pilot runtime verification
is recorded in [ACCEPTANCE.md](ACCEPTANCE.md), including outstanding Windows/CAD checks.

## Server setup

The default server is `https://mmsdev.transportation.wv.gov/dock`. Its live discovery
endpoint advertises `/dock/api`; saved client settings override the default. The
server deployment uses:

```text
PW_ORIGIN=https://mmsdev.transportation.wv.gov
PW_PUBLIC_BASE_PATH=/dock
PW_COOKIE_SECURE=true
```

Build the web frontend using `VITE_BASE_PATH=/dock/`. Configure the HTTPS proxy to
forward `/dock/api/...` to `/api/...` on the native API, serve the frontend under
`/dock/`, and route `/dock/*` browser page reloads to its index. The desktop discovery
URL is `/dock/api/desktop/config`. Keep the API private behind that proxy; the client
does not disable certificate validation. Local `./dev` retains `/` and `/api` defaults.

## First use

Open Dock, enter the server URL, and choose **Sign in with your WVDOT account**.
Your browser opens the WVDOT sign-in page and returns you to Dock; there is no Dock
password to type or store. Then select an empty NTFS
folder (default `%USERPROFILE%\Dock`). Windows permissions restrict the workspace
and its journals to the current Windows user and SYSTEM. An existing workspace is
bound to its original Dock account/server; use a different empty root when switching.

Explorer shows Dock and its accessible directory. With Dock running, double-click
a document for the read-only/check-out choice before the editor starts. Dock → Open
provides the same choice. Files outside the workspace retain their default action.
Exit Dock removes its scoped verbs; unregister also removes stale owned registrations.
Cloud download state and Dock checkout state are separate properties. Use the tray
window for check-ins, pending additions, transfers, and recovery. Sessions last eight
hours. Cached reading and previously checked-out edits remain available offline.
Enable Dock in Windows **Settings → Apps → Startup** to start it at sign-in.

Drop additions into the directory and use **Pending changes → Review and upload**.
Rename/move/delete callbacks block the raw operation and ask for confirmation in Dock;
no dialog waits inside a Cloud Files callback. File deletion means archive; folder
deletion means Dock Trash. Close editing applications before check-in/undo/recovery.

CAD references are ordinary permission-checked files, never automatically checked out.
Windows-invalid or colliding names use encoded local names; references needing exact
names may need correction by a user. Automatic CAD reference rewriting is not included.

## Verification and contracts

```powershell
dotnet run --project desktop/windows/Dock.Core.Tests
dotnet build desktop/windows/Dock.Desktop
```

The core checks run on macOS/Linux too. Regenerate desktop wire types with the repo's
Python environment: `python desktop/windows/scripts/generate_contracts.py`. It exports
FastAPI OpenAPI and deterministic C# desktop models without opening database/cloud
connections. Do not hand-edit `Contracts.g.cs`.

Before uninstalling, check in or copy out pending work and finish **Keep offline**
for any server files you want to retain locally. Choose **Exit Dock** from the tray.
Run the combined cleanup/uninstaller in 64-bit Windows PowerShell under the same
Windows account, elevated when required to remove machine-level root registrations:

```powershell
.\scripts\unregister.ps1 -WhatIf
.\scripts\unregister.ps1
```

It unregisters Dock cloud folders, removes owned Explorer pins and opening actions,
and removes the current user's Dock MSIX package. It also handles stale entries
when Windows has already removed the app. Downloaded files, local edits, journals
and recovery data remain; Windows removes online-only placeholders during Cloud
Files unregistration. Server documents and checkout ownership are unchanged.
The script never deletes workspace/state directories or removes signing certificates.
If an editor or Shell host keeps the package in use, close it and rerun after the
reported error. A preview can run while Dock is open; actual removal cannot.

The manifest declares unvirtualizedResources and disables filesystem/registry write
virtualization to keep state outside package-managed cleanup. Windows helper checks:

```powershell
.\scripts\tests\unregister.Tests.ps1
```

## Provenance

Cloud Files and shell patterns follow Microsoft's documentation and the
[Cloud Mirror reference sample](https://github.com/microsoft/Windows-classic-samples/tree/main/Samples/CloudMirror).
No Cloud Mirror implementation was copied into the client; the native bridge and
state machine are Dock-specific. Branding assets derive from this repository's
`frontend/public/dock-logo-dark.svg` and `favicon.svg`.

Canonical end-user and technical documentation remains in the web app's separate
Usage and Business logic pages, with desktop changes in the frontend changelog.

Explorer status is supplied by the packaged custom-state handler from Dock’s local
cache, including for read-only and online-only documents. Install the MSIX to
register that handler and the Dock context menu; launching a loose EXE is insufficient.

## Automatic uploads (0.1.5.0)

New files and nested/empty folders pasted into the active workspace upload after
copying finishes. Dock also scans additions left while it was closed. The footer's
Uploads button opens per-item progress and errors in Transfers; the tray tooltip
shows overall upload state. Interrupted transfers retry automatically. Resolve
permanent errors and retry their queued operation. Existing document edits still
require check-in. Temporary/backup files and trees, folder-settings files and
redirected or revoked paths are excluded. Keep Dock running until uploads finish.

## WVDOT desktop layout (0.1.6.0)

The redesigned client uses a sidebar for Directory, My checkouts, Pending changes,
Transfers and Recovery. Open Explorer stays at the top; Directory's More menu holds
less frequent actions. Account settings contains sign-in/out and graceful exit.
Summary cards describe the whole workspace and hide in compact windows to leave
room for documents. Shared styles cover sign-in, tables, status badges and dialogs.
The visible application title is WVDOT Dock; its package and workspace identities
remain unchanged so upgrades retain the existing account and sync registration.


## Windows appearance — 0.1.7.0

Use **Dark mode** at the bottom right, including before sign-in. Choose **Light mode**
to return. The choice takes effect immediately and is saved per Windows profile in
`%LOCALAPPDATA%\Dock\appearance.json`, separately from accounts and workspace state.
The default is light; a failed save keeps the current session's choice and explains
that it could not be remembered. The website, Explorer and external editors keep
their own themes. See the web-rendered [Client change log](../../frontend/src/docs/client/change-log.md)
for release details and `ACCEPTANCE.md` for actual Windows verification.


### Main-window appearance correction — 0.1.8.0

Upgrade to 0.1.8.0 if dark cards appear within a white window or counters/headings
remain black. The main window now explicitly uses the shared Window style, keeping
the canvas and inherited text consistent with the selected palette. Your existing
appearance preference is retained. Verification uses the compiled MainWindow with
isolated state; a plain Window preview cannot validate this inheritance boundary.


### Sign-out cleanup — 0.1.10.0

Sign out works even when the server session has expired. It stops synchronization,
clears local sign-in state and returns to the sign-in screen, preserving downloaded
files, pending work and checkouts. An unreachable server produces a warning that
remote revocation could not be confirmed. WVDOT/browser sign-in is independent.
`Dock.Core.Tests` covers API success, expiry, errors and cancellation; the desktop
harness exercises the real menu and retained state with a synthetic workspace.

### Switching accounts (0.1.13.0)

Successful SSO with a different account replaces the selected previously bound
workspace at the same location, deleting downloaded files, unsent changes, snapshots
and its old local journal. The old Explorer root is unregistered. Same-account
sign-in and sign-out retain local work; server documents and checkouts are unchanged.
Close files that block cleanup and retry. Unbound nonempty folders are not erased.

## Architecture compatibility — 0.1.14.0

Build from the current architecture revision with `scripts/build.ps1` and the
existing signing certificate. The client uses precise manifest permissions and
paged child/ancestry lookups for folder reconciliation, preserving the manifest,
SSO, immutable single-request uploads and revision-guarded mutation contracts.
The default server remains `https://mmsdev.transportation.wv.gov/dock`.

The development server advertises 250 MiB to Windows clients. This release does
not implement the web client's multipart sender or eight concurrent upload lanes.
Oversized local files remain local with a clear limit error. OCI multipart policy
limitations are described in the canonical Business logic reference. Full-file
hydration still has a 50-second callback deadline; multi-gigabyte and 100,000-file
Explorer runtime acceptance remain pending even when core scale checks pass.

Update the existing package after exiting Dock; retain its publisher and package
identity. Do not uninstall or clear the workspace to update. Same-account state
is retained; a different-account sign-in intentionally removes the old bound
workspace as documented in the canonical Usage guide.
