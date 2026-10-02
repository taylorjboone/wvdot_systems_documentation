# ProjectWise access control

ProjectWise has fairly granular access control: you can assign permissions to users, groups, or access lists at the datasource, folder, subfolder, and individual-document levels, with additional permissions based on workflow state. It also separates **document metadata permissions from actual file-content permissions**.

This explanation describes the core **ProjectWise Design Integration / Explorer / Administrator** model. Bentley’s web collaboration and deliverables products have additional permission systems.

**The scope can be as broad as the entire repository or as narrow as one document.** Bentley calls the repository a *datasource*. Security can be configured in these places:

| Scope | What you control | Example |
|---|---|---|
| Datasource | Broad defaults for folders and documents | General employee access |
| Environment | Security associated with an environment configuration | Documents using a particular metadata environment |
| Work area / folder | Access to that organizational container | A transportation project |
| Subfolder | More specific access within a project | Design, ROW, utilities, construction |
| Documents within a folder | Default document actions for that folder | Designers can edit its files |
| Individual document | Exceptions for one document | Restrict a particular estimate |
| Workflow | Access associated with a document lifecycle | Design review workflow |
| Workflow state | Permissions at a particular lifecycle stage | Draft versus approved |

These are not all successive levels in one directory tree; workflow security is a separate hierarchy. Bentley configures the broader settings in Administrator and folder/document settings in Explorer. [Bentley: Access Control Concepts](https://docs.bentley.com/LiveContent/web/ProjectWise%20Administrator%20Help-v13/en/GUID-2E5A8115-BCC4-FDC0-DE56-624E7A1E13DD.html)

**A folder has two distinct sets of permissions: permissions for the folder itself, and permissions for documents inside it.**

The folder’s own permissions are:

| Folder permission | Meaning |
|---|---|
| Read | See the folder and inspect its properties |
| Write | Modify folder properties |
| Create subfolders | Add folders beneath it |
| Delete | Delete that folder |
| Change permissions | Modify access assignments |
| Full control | Enable every permission except No access |
| No access | Hide the folder and deny access |

Therefore, giving someone permission to modify a folder does not itself express permission to edit the files within it. Those actions belong to different permission sets. [Bentley: Access Control Security Permissions](https://docs.bentley.com/LiveContent/web/ProjectWise%20Administrator%20Help-v12/en/GUID-687490C3-E625-364B-333F-5E8FC75D9C5A.html)

**The document permissions are more detailed.** At the folder level, you specify the following permissions for documents in that folder:

| Document permission | Meaning |
|---|---|
| Read | See document records and properties |
| Write | Modify document properties |
| File Read | Open the attached file for viewing |
| File Write | Open the attached file for editing |
| Create | Create documents in the folder |
| Delete | Delete documents |
| Change Workflow State | Change documents’ lifecycle state |
| Free | Release documents locked by another user |
| Change permissions | Modify document access assignments |
| Full control | Enable all permissions except No access |
| No access | Hide documents and deny access |

The distinction between **Write** and **File Write** is especially useful: someone can maintain metadata without being allowed to edit drawing content. [Bentley: Folder Level Document Permissions](https://docs.bentley.com/LiveContent/web/ProjectWise%20Administrator%20Help-v9/en/GUID-304E94B1-02B5-C691-3A2D-2A3A02954079.html)

For an **individual document**, the same permissions are available except **Create**, which belongs to the containing folder. Individual document security can override inherited document security. Some permissions automatically enable prerequisites:

- **Write** enables Read.
- **File Read** enables Read.
- **File Write** enables Read and File Read.

File Write does not automatically imply permission to change metadata. [Bentley: Individual Document Permissions](https://docs.bentley.com/LiveContent/web/ProjectWise%20Explorer%20Help-v11/en/GUID-4E8D1EBB-179F-2F33-B57F-9DAD3A069983.html)

For example, the following are possible permission combinations, assuming the user’s broader settings and document status permit the action:

| Intended capability | Relevant document permissions |
|---|---|
| Find a document and inspect its metadata | Read |
| Maintain metadata without opening file contents | Read + Write |
| View a drawing without editing it | Read + File Read |
| Edit drawing content without changing metadata | Read + File Read + File Write |
| Edit both metadata and drawing content | Read + Write + File Read + File Write |
| Move a document through its workflow | Change Workflow State, plus necessary visibility |
| Administer another person’s checkout lock | Free, plus necessary access |

These combinations follow from Bentley’s separation of record access and file access. They are examples, not built-in named roles. [Bentley: Permission Definitions](https://docs.bentley.com/LiveContent/web/ProjectWise%20Explorer-v2024/Help/en/html5/topics/6365/GUID-687490C3-E625-364B-333F-5E8FC75D9C5A.html)

**ProjectWise has groups—and also a separate concept called user lists.**

| Principal | Purpose |
|---|---|
| Individual user | Directly assign access to one person |
| Group | Manage a collection of users with common access needs |
| Access list | Combine users, groups, and other access lists into an access-control collection |
| Mailing list | Collect messaging recipients; distinct from an access list |

The access-list feature allows you to assemble project membership from existing organizational groups. For example, an illustrative `Project_123_Design_Team` access list could contain a roadway group, a bridge group, a consultant group, and a few individually assigned staff. Permissions are assigned to the list instead of separately to each member. Bentley explicitly documents nesting access lists within other access lists. [Bentley: Managing User Lists](https://docs.bentley.com/LiveContent/web/ProjectWise%20Administrator-v2026/Help/en/topics/6365/GUID-A8134857-6C03-C5C6-F5A7-1EAA860D347C.html)

**Membership management can be delegated.** Groups and user lists can have multiple owners, who can manage their membership through Explorer’s User / Group Management dialog. Ownership and membership are separate: someone can manage a group without belonging to it, and ownership alone does not give that person access to folders assigned to the group.

This supports a project manager administering a project’s team membership without personally receiving every document permission that team has. [Bentley: Managing Groups and User Lists](https://docs.bentley.com/LiveContent/web/ProjectWise%20Explorer%20Help-v12/en/GUID-A5EC00D8-EE32-1BCB-61BA-F623F2DD0DC7.html)

Bentley also documents synchronizing a logical ProjectWise group with a matching Bentley IMS group using membership claims. Exact identity integration and nesting behavior should be checked against the installed release; Bentley’s documentation spans several generations. [Bentley: Managing Groups](https://docs.bentley.com/LiveContent/web/ProjectWise%20Administrator%20Help-v13/en/GUID-2473FF20-9B56-6AE1-D0DF-F72CAD9D6C55.html)

**Inheritance generally uses the nearest ancestor that has its own security defined.**

If an object has no explicit security entries, ProjectWise looks upward for defined security. Establishing its own security creates a new inheritance boundary; it is not simply a matter of continuously accumulating every ancestor’s entries. [Bentley: Workflow-based and Object-based Security](https://docs.bentley.com/LiveContent/web/ProjectWise%20Administrator%20Help-v9/en/GUID-2D2A39DF-EC1A-E74F-68FB-3851DD14A1EA.html)

For illustration:

| Location | Security configuration | Effect |
|---|---|---|
| `/Projects` | Explicit general project access | Provides an inherited baseline |
| `/Projects/Project-123` | Explicit project team access | Establishes a project-specific boundary |
| `/Projects/Project-123/Design` | No explicit entries | Inherits from Project-123 |
| `/Projects/Project-123/Design/Bridge` | No explicit entries | Also inherits from Project-123 |
| `/Projects/Project-123/ROW` | Explicit ROW team access | Establishes a separate boundary |
| `/Projects/Project-123/ROW/Acquisitions` | No explicit entries | Inherits from ROW |

When you change a parent, descendants still inheriting from it reflect the change; descendants with their own explicit security are not automatically replaced. Bentley notes that even applying a change to “this folder only” affects descendants that inherit that folder’s security. [Bentley: Permissions in ProjectWise](https://bentleysystems.service-now.com/community?id=kb_article_view&sysparm_article=KB0020684)

**Multiple group memberships generally contribute cumulative grants, while explicit No access overrides them.**

For example, if one applicable group grants file reading and another grants file editing, membership in both can provide both capabilities. An unchecked permission is not a separate per-action deny. Bentley describes the ordinary entries as Allow permissions, with **No access** functioning as deny-all.

That means a “read-only group” does not necessarily remove editing rights granted by another applicable group. Explicit No access, however, blocks access even when another assignment grants it. [Bentley: Permission Combination Rules](https://bentleysystems.service-now.com/community?id=kb_article_view&sysparm_article=KB0020684)

Another unusual default: Bentley documents a newly created datasource with no access control configured as accessible to all created users. Explicit access assignments then exclude users who are not covered. **An entirely unconfigured datasource should not be assumed to deny access by default.** [Bentley: Access Control Concepts](https://docs.bentley.com/LiveContent/web/ProjectWise%20Administrator%20Help-v13/en/GUID-2E5A8115-BCC4-FDC0-DE56-624E7A1E13DD.html)

**Workflow security can change what people may do to the same document as it progresses.**

An illustrative configuration might be:

| Workflow state | Designers | Reviewers | Approvers |
|---|---|---|---|
| Work in progress | Edit files and metadata | Read files | Read files |
| Internal review | Read files | Maintain review metadata | Read files |
| Approved | Read files | Read files | Control permitted state changes |
| Issued | Read files | Read files | Limited administrative actions |

These are example policy choices, not Bentley’s default roles.

The precedence is significant. For the inherited-security case Bentley documents:

- If only object security or workflow security is defined, use the defined hierarchy.
- If both are defined, an applicable **No access** in either takes priority.
- Otherwise, **workflow security takes precedence**.

So you should not assume that workflow security merely subtracts permissions from folder security. [Bentley: Workflow-based and Object-based Security](https://docs.bentley.com/LiveContent/web/ProjectWise%20Administrator%20Help-v9/en/GUID-2D2A39DF-EC1A-E74F-68FB-3851DD14A1EA.html)

**Checkout is a separate document condition, in addition to permission.**

To check out a document, Bentley requires:

- Read, File Read, and File Write privileges.
- A checked-in document.
- The active version.

Checkout downloads a working copy and locks the document against another checkout. Check-in commits changes and releases that lock. The person holding the checkout sees a check mark; other users see a lock. Older, non-active versions open read-only.

Thus, two designers can both have editing permission while only one can currently hold the checkout. [Bentley: Checking Out and Checking In Documents](https://docs.bentley.com/LiveContent/web/ProjectWise%20Explorer%20Help-v12/en/GUID-E99EF32D-CC69-B7F3-A664-1F5171EB66CB.html)

Managed export follows a similar requirement: the document must be checked in, and the user needs Read, File Read, and File Write. Reimporting is analogous to checking it back in. Bentley distinguishes this from unmanaged export of a copy. The core document permission list does not have a separate “Export” checkbox. [Bentley: Exporting and Importing Documents](https://docs.bentley.com/LiveContent/web/ProjectWise%20Explorer%20Help-v10/en/GUID-DC20255C-E1E9-9642-E2BC-6B5A238DFFFF.html)

**User-level settings add another layer of restrictions.** These include the ability to:

- Create documents and versions.
- Modify or delete documents.
- Free documents.
- Change workflow state.
- Set or remove final status.
- Create, modify, or delete folders.

Disabling document modification makes documents read-only to that user despite object-level write permissions. Freeing someone else’s checkout requires both the user’s freeing capability and the document’s Free permission. Setting or removing final status also requires Change Workflow State permission. Final documents are read-only while that status remains.

There is also a powerful **Use access control** user setting: turning it off bypasses folder/document access controls for that account. [Bentley: User Properties Settings](https://docs.bentley.com/LiveContent/web/ProjectWise%20Administrator%20Help-v11/en/GUID-4E1A21E3-8610-40DC-918C-F4D03881478C.html)

**Ownership has special behavior, so “owner” is not just a display field.** Bentley documents that, without workflow security, a folder owner has implicit permission-changing authority over that folder and its subfolders. With workflow security, that unconditional authority disappears; the owner can be excluded by the workflow’s settings. [Bentley: Ownership and Access Control](https://docs.bentley.com/LiveContent/web/ProjectWise%20Administrator%20Help-v12/en/GUID-687490C3-E625-364B-333F-5E8FC75D9C5A.html)

**Administrative permissions can also be delegated by function.** A Restricted Administrator can be granted access to selected nodes in ProjectWise Administrator, such as management of particular configuration areas, rather than receiving broad administrative control.

The administrative permission choices are:

| Administrative permission | Meaning |
|---|---|
| Change settings | Manage that Administrator node |
| Change permissions | Manage access to that node |
| Full control | Both of the above |
| No access | Hide the node |

These are administrative controls, separate from permissions to edit engineering documents. [Bentley: Granular Administrative Security](https://docs.bentley.com/LiveContent/web/ProjectWise%20Administrator%20Help-v9/en/pwa_granular_security_tab.html)

**ProjectWise also provides ways to inspect and maintain the result.** Explorer has a combined “Real (Workflow & Folder)” security view for reviewing the resolved permissions rather than looking only at one contributing hierarchy. [Bentley: Reviewing Combined Permissions](https://bentleysystems.service-now.com/community?id=kb_article_view&sysparm_article=KB0020684)

Folder security can also be exported into an Excel representation, with separate folder/document columns and workflow rows, using compact permission masks. This is useful for reviewing a large folder structure. [Bentley: Reviewing Exported Folder Security](https://docs.bentley.com/LiveContent/web/ProjectWise%20Explorer%20Help-v12/en/GUID-EA7C53C3-9BA8-9761-2401-316DEAB121D8.html)

**The core granularity stops at the folder/document and file-access level described above.** Those standard permission tables do not define separate ACL actions for editing an individual metadata field, editing particular CAD elements, printing, approving, or downloading. Additional workflow configuration, application behavior, or other Bentley products may provide further controls; those should not be confused with the base folder/document permission model.

If you are evaluating what a comparable document platform needs, the consequential design choices are **separate container and content permissions, separate metadata and file editing, reusable group membership, explicit inheritance boundaries, workflow-dependent access, and independent checkout ownership**. A permission editor that only offers “viewer/editor/admin” would conceal several distinctions ProjectWise explicitly supports.
