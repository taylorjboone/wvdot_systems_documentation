---
title: "Why Organizations Use ProjectWise as a Document Store"
subtitle: "Engineering information control, practical benefits, limitations, and the business case"
date: "Research current to September 7, 2026"
lang: en-US
toc-title: "Contents"
---

# Executive overview

**Organizations use ProjectWise because engineering documents need to remain connected to their project context, their dependencies, their authorized users, and the decisions made about them.** The practical value is the ability to manage information as it is created, reviewed, shared, revised, and delivered. Bentley positions ProjectWise around governed project delivery, design application integration, reference management, and managed workspaces. [1: Bentley product overview][S01]

Calling ProjectWise a document store is accurate, but incomplete. For an infrastructure organization, the useful unit of information is often a drawing together with its referenced design files, calculation report, approval status, issue history, and project identifier. A repository becomes more valuable when it helps people understand those relationships and use the right information for the right purpose.

This report's central assessment is that the strongest reasons for adopting ProjectWise fall into five groups:

| Organizational need | Why it creates a case for ProjectWise |
|:--|:--|
| Reliable engineering production | Teams need to work with related native files and consistent design resources. |
| Controlled information release | A new file must be distinguished from an approved or formally issued file. |
| Collaboration across organizations | Owners, consultants, and contractors need a defined place and process for exchanging work. |
| Accountability and continuity | Project information must remain understandable after revisions, personnel changes, and closeout. |
| Repeatable delivery | Standard structures and processes can reduce the administrative effort of starting and managing projects. |

These are reasons to evaluate the platform, not guarantees of a particular financial return. The benefits depend on the configuration, the applications being used, the quality of the information, and whether participants actually work through the agreed process.

Public agency evidence shows that the scope can extend well beyond drawings. A January 2026 USACE directive includes calculations, design and decision documentation, and correspondence in its engineering document-management policy. MnDOT's storage standard assigns active project files to ProjectWise and directs record files to eDOCS after closeout. These examples demonstrate both the breadth of the use case and the importance of defining where ProjectWise's responsibility ends. [17: USACE directive][S17], [18: MnDOT storage standard][S18]

The commercial case is strongest when the cost of information confusion is material: many contributors, frequent changes, complex file relationships, formal reviews, substantial deliverables, or an owner requirement to use ProjectWise. An organization mainly storing uncomplicated Office documents or occasional PDFs should compare other options carefully. Microsoft, Autodesk, and Oracle document overlapping controls in their own platforms. The assessment should focus on actual workflows, integration quality, administration, and total cost. [25: SharePoint controls][S25], [27: Autodesk overview][S27], [29: Oracle Aconex][S29]

# 1. What “document store” means in this context

## 1.1 A managed project document has several layers

For this report, a **file** is the digital content itself: for example, a DGN, DWG, PDF, spreadsheet, image, or report. A **managed document** is that content together with information that gives it identity and governs its use.

The following is a conceptual model for evaluating the repository. It is not a literal database schema or an assertion that every deployment implements every element identically.

| Layer | Questions it should answer |
|:--|:--|
| Content | What is the actual file, and can the intended user open it correctly? |
| Identity and metadata | Which project, discipline, document type, location, or asset does it concern? |
| Relationships | Which files does it depend on, and which deliverables depend on it? |
| Lifecycle and authority | Is it work in progress, under review, approved for a stated use, or superseded? |
| Access and history | Who can act on it, and what activities and decisions are retained? |

This distinction explains why “we already have somewhere to upload files” may not resolve the engineering problem. Uploading establishes possession of a file. The organization still needs to establish whether it is complete, relevant, usable, and authorized for the next task.

## 1.2 The repository is part of a common data environment

The UK BIM Framework's September 2020 Guidance Part C distinguishes a CDE workflow from the technical solutions that support it. It also recognizes that several organizations' solutions can participate in the overall CDE. Accordingly, a shared information process does not necessarily require every piece of project information to reside in one application. [24: CDE guidance][S24]

For example, an owner could use ProjectWise for engineering production, another platform for financial transactions, and an approved records system for long-term preservation. The design challenge is to define authoritative information, identifiers, handoffs, and responsibilities across those systems.

“Single source of truth” is most useful as a governance objective: people know which source is authoritative for a particular item and use. It should not be interpreted as proof that duplicates, local copies, conflicting approvals, or disconnected systems have ceased to exist.

## 1.3 Product names and deployment matter

ProjectWise documentation spans several generations of desktop clients, servers, web services, and cloud offerings. The current Bentley Infrastructure Cloud FAQ distinguishes Connect and ProjectWise entitlements and identifies cloud deployment prerequisites for several newer capabilities. An existing server installation should not be assumed to have every feature shown on today's product website. [32: Bentley Infrastructure Cloud FAQ][S32]

Throughout this report, **documented capability** means the cited source describes a function. **Expected benefit** means the report explains a reasonable way that function could help. **Recommended practice** means an implementation or evaluation approach proposed here. These categories should remain separate when preparing a procurement justification.

# 2. Why organizations choose ProjectWise

## 2.1 It can preserve the relationships that make engineering files usable

Engineering information often has dependencies. A sheet might reference a design model that in turn references survey, terrain, imagery, or another discipline's work. Having all the files somewhere on a server does not establish that the application can resolve the correct relationships.

Bentley's integration guidance explicitly distinguishes basic file storage, where dependencies are not managed, from deeper integration that manages linked or reference files. Its examples include maintaining reference relationships during import, export, and supported renaming operations. This is a substantial reason to evaluate ProjectWise for native engineering production. [2: Application integration levels][S02]

**Expected benefit:** less effort finding missing references, reconstructing a designer's working environment, or assembling an exchange package manually. The potential benefit grows as the number of relationships and collaborating teams grows.

**Practical qualification:** storing a file format and deeply integrating its authoring application are different capabilities. A pilot should open a real project, resolve nested references, rename or relocate supported items, and export a usable package. Test the exact application and integration versions that staff will use.

## 2.2 It establishes a controlled editing process

HDR's July 2024 ProjectWise manual describes check-out as downloading and locking a document for editing, check-in as returning the working file to the server, and copy-out as obtaining a local copy without preventing someone else from editing. It also distinguishes updating the server copy while retaining the check-out. [23: HDR user manual, p. 9][S23]

**Expected benefit:** participants have an explicit way to establish editing responsibility and return changes to the shared environment. This is especially useful for applications and file types where simultaneous independent edits would be difficult to reconcile.

For an illustrative two-person team, one designer checks out a plan file and the other sees that it is already being edited. The second person can coordinate the change instead of unknowingly creating a competing replacement.

**Practical qualification:** check-out introduces responsibility as well as protection. Teams need procedures for abandoned locks, staff absences, disconnected work, and unsent local edits. Exclusive editing is also different from application-specific coauthoring or model worksharing; determine the correct behavior for each workflow.

## 2.3 It distinguishes ongoing work from historical snapshots

Bentley defines a ProjectWise version as a read-only snapshot. The active document can continue evolving while a version captures an earlier state. The help also distinguishes user-facing version labels from automatically assigned sequence numbers. [3: Working with Versions][S03]

**Expected benefit:** teams can preserve meaningful milestones without depending on a collection of loosely related filenames such as “final,” “final2,” and “final-approved-new.”

A useful organizational convention would specify when a snapshot is required: before an external issue, before a major redesign, or when a review package is established. It should also distinguish a technical snapshot from a contractual revision designation. Those may correspond, but the organization must define the relationship.

**Practical qualification:** neither the latest timestamp nor the highest technical version number proves approval. Approval and permitted use need their own agreed meaning. Ordinary saves and check-ins should not be assumed to create every historical snapshot that a records or delivery policy requires.

## 2.4 It can separate review, approval, and completion

ProjectWise workflows consist of ordered states defined by an administrator. Bentley documents state-level access settings and the possibility of notifications through a configured messaging agent. It also documents Final status, which makes a document read-only but can be removed by an appropriately authorized user. [4: Workflows and States][S04]

**Expected benefit:** a repository can express more than whether a file exists. It can help establish where that file sits in the delivery process and who is permitted to advance it.

For example, a calculation could move through drafting, independent check, approval, and issue preparation. A rejected item returns for correction with responsibility clearly assigned. The example states are an implementation choice, not universal ProjectWise defaults.

**Practical qualification:** changing a status is not itself evidence that an adequate technical review occurred. Define who approves, what they must examine, which evidence is retained, and what a subsequent content change does to the approval.

## 2.5 Metadata makes information easier to find and organize

Bentley's documentation describes environment attributes as configurable document information that users can modify through document interfaces. Its document-creation training also covers placeholders and metadata. These capabilities support an information structure more useful than filenames alone. [6: Environment attributes][S06], [33: Creating Documents][S33]

**Expected benefit:** someone who does not know the original folder location can still identify a relevant document through its business context.

An illustrative metadata standard might include a project number, document type, discipline, title, originating organization, revision, and intended use. Location or asset identifiers can be added where they answer an actual retrieval need. A bridge inspection attachment and a roadway calculation should not require an identical collection of irrelevant fields.

**Practical qualification:** custom metadata does not create itself merely because the software supports it. Required fields, controlled lists, sensible defaults, validation, and accountable ownership determine whether the information is trustworthy. Excessive entry requirements can encourage users to bypass the repository.

## 2.6 Search can answer project questions without manual browsing

Bentley documents quick search across document and project properties, full-text search, advanced searches using environment attributes, and saved searches. Full-text availability and behavior depend on the supporting configuration and components. [8: Performing and Saving Searches][S08]

**Expected benefit:** a recurring project question can become a repeatable query rather than an exercise in remembering folder paths.

Examples to implement and test include “all drainage calculations for this project,” “documents awaiting our team's review,” and “issued specifications associated with this contract.” Queries involving due dates or responsibility require those values to be captured in a suitable field or connected workflow.

**Practical qualification:** define the search population. A metadata search, a content search, and a search of correspondence may cover different information. Scanned files may need additional text extraction or OCR. Search should be checked against known examples and expected permissions before staff rely on it for completeness.

## 2.7 Access can reflect project responsibilities

Bentley's help documents controls for setting permissions on individual documents. These controls provide a mechanism for aligning access with the people who are meant to use or manage the information. [7: Document Access Control][S07]

**Expected benefit:** the project can establish appropriate boundaries between internal authors, reviewers, partner organizations, and participants who only need released information.

A recommended access model starts with reusable project roles and groups, followed by a small number of justified exceptions. A discipline reviewer might need access to a review package without needing authority to alter unrelated work. Sensitive project material may need a narrower group.

**Practical qualification:** access rights must be tested as ordinary users. Administrators should verify the effective result of the configuration, including state changes and external access. Repository permissions also do not automatically govern every copy after an authorized person downloads or forwards it. Endpoint and external-sharing practices remain relevant.

## 2.8 Activity history helps explain what happened

ProjectWise's document audit trail records selected activities. Bentley states that administrators determine which activities are logged and whether a user can see the history. Therefore, the existence of an audit-trail feature is different from confirmation that every event an organization needs has been retained. [5: Document Audit Trail][S05]

**Expected benefit:** staff can investigate how a document changed, follow up on an unexpected action, or reconstruct part of the delivery history without relying entirely on memory.

For a project team, useful evidence may include who created an item, who changed it, when an issue occurred, and which associated workflow or transmission record explains the event. The necessary evidence should be defined first, then demonstrated in the configured system.

**Practical qualification:** technical activity logs do not automatically establish engineering correctness, legal admissibility, nonrepudiation, or the meaning of a decision. Protect the logs, define their retention, and retain the actual review and issue evidence needed to interpret them.

## 2.9 Formal deliverables management reduces ambiguity at organizational boundaries

Bentley describes ProjectWise Deliverables Management as supporting controlled exchange between business entities. It includes recipient acknowledgment, review and responses, package status, and audit history. Documented package types include transmittals/submittals, RFIs, and general correspondence. [10: Deliverables][S10]

**Expected benefit:** the team can manage an exchange as an accountable transaction. It becomes easier to distinguish the authoring file from the package that another organization actually received.

For example, an engineer may continue revising a source calculation while the owner reviews a previously issued package. The project should retain the identity of that issued package and the response to it, even as new work proceeds.

**Practical qualification:** acknowledgment of receipt, completion of review, technical acceptance, and approval for a particular use are distinct events. Configure them deliberately. A link to a live working document should not be treated as a frozen issue record unless the implemented process actually preserves the intended version and evidence.

## 2.10 It can support distributed teams working with substantial engineering content

Bentley's remote-working guidance describes using local working directories and reusing current local copies to reduce network traffic. The published G-Cloud service definition also identifies file caching and delta file transfer among the design-integration mechanisms. [13: Working Remotely][S13], [15: G-Cloud service definition][S15]

**Expected benefit:** a geographically distributed team may avoid repeatedly transferring all of the same engineering content. This can make remote participation more practical and allow specialists to contribute across offices.

Legacy Bentley training explains delta transfer as transferring changed content when suitable existing copies are present. This is a mechanism to evaluate, not a claim that every file operation or client uses the same optimization. [35: Bentley User Essentials][S35]

**Practical qualification:** benchmark the actual workload. Measure the first open, later opens, check-in, reference discovery, workspace loading, and PDF production from representative locations. File sizes, reference counts, connectivity, storage, endpoint performance, and configuration all belong in the evaluation. A fast demonstration of one isolated file is insufficient.

## 2.11 Standard resources and publishing can make output more consistent

Bentley's digital-transformation guidance describes managed workspaces as a way to support engineering standards. Separately, Explorer help documents rendition generation through Bentley i-model Composition Server for PDF, with the resulting output stored in ProjectWise. The cited rendition capability covers several source formats and output types. [14: Bentley digital-transformation guide][S14], [9: Creating Renditions][S09]

**Expected benefit:** teams can reduce repetitive setup and publishing work and improve consistency between staff and projects.

For example, the same approved design resources and plotting configuration can form part of a reproducible production process. A document controller could then validate an automatically generated review set instead of assembling every output manually.

**Practical qualification:** standards need change control. A workspace modification should not silently alter the reproducibility of an older project. Automated output also needs validation for completeness, scale, fonts, references, title blocks, and the intended source revision. Rendering a file successfully does not mean that the deliverable is approved.

## 2.12 Project information can remain connected across file types and roles

Bentley's ProjectWise Drive guidance describes desktop access aimed particularly at non-CAD workflows, while retaining Explorer as the primary interface for deep CAD integration and advanced functions. This provides a reason to include non-design staff in the same governed project process. [11: ProjectWise Drive][S11]

**Expected benefit:** a designer, project manager, document controller, and technical reviewer can organize their related contributions around the same project context even though they use different applications.

The business value is the relationship among the information. A design assumption may be explained in a report, approved in correspondence, implemented in a model, and communicated in an issued PDF. Losing any of those connections can make later interpretation more difficult.

**Practical qualification:** choose an interface appropriate to the task. A person who reads occasional documents has different needs from someone managing a large reference set. Verify actual access, authoring, review, and licensing arrangements for each role.

## 2.13 Automation can reduce repetitive administration

Bentley documents a ProjectWise SDK for custom utilities and client event hooks. Microsoft's connector documentation lists ProjectWise operations for documents, references, versions, and workflow actions, with listed actions marked Preview. These are concrete integration mechanisms, though production suitability must be assessed for the selected route. [30: ProjectWise SDK][S30], [31: Microsoft connector][S31]

**Expected benefit:** organizations can standardize recurring tasks such as assembling document registers, checking metadata completeness, creating project structures, or identifying review exceptions.

These are proposed use cases, not a claim that a ready-made implementation is included for each one. Start with a high-volume task that has a clear owner and a measurable error or time cost.

**Practical qualification:** automation should preserve permissions, lifecycle rules, and traceability. It needs error handling, support ownership, and a way to identify incomplete or repeated operations. The presence of an API does not establish that two repositories can synchronize all content and meaning without loss.

## 2.14 An established owner environment can simplify participation

MnDOT's public CADD resources connect ProjectWise access to authorization, the applicable design standards, and external partners' licensing obligations. TxDOT's file-management guidance directs project files into ProjectWise using its standard structure. These are practical examples of an owner establishing a shared delivery environment. [19: MnDOT CADD resources][S19], [21: TxDOT file-management guidance][S21]

**Expected benefit:** consultants can work within an already specified delivery process, and owners can receive information in a more consistent structure across contracts.

An existing ecosystem also affects the economics. The skills, project templates, integrations, and historical information already in place have value. Replacing them has a transition cost that should be compared with the benefits of change.

**Practical qualification:** an owner mandate establishes a requirement for the applicable work; it does not establish that ProjectWise is the best repository for every activity in the consultant's business. Separate the costs of participating in someone else's environment from the costs of operating a new environment.

# 3. Why it is used for documents beyond CAD

Engineering decisions depend on more than graphical design content. The following table is an **illustrative repository scope**, proposed for discussion rather than presented as a universal ProjectWise configuration.

| Information category | Reason to keep it connected to the project | Governance question |
|:--|:--|:--|
| Calculations and technical reports | Explains assumptions, methods, and design decisions. | Which calculation revision supports the issued design? |
| Specifications and special provisions | Defines requirements that drawings alone may not convey. | Was the specification coordinated with the issue package? |
| Review comments and responses | Preserves the rationale for correction or acceptance. | Is each response associated with the item actually reviewed? |
| Meeting records and technical correspondence | Captures instructions and agreements that influence the work. | Which communications need formal capture and approval? |
| Permits and environmental documentation | Connects project activity with its documented constraints. | Who owns updates and determines the authoritative record? |
| Photos, inspection attachments, and test reports | Provides evidence associated with a location or activity. | Are location, date, subject, and project identity adequate? |
| Submittals, transmittals, and package registers | Establishes the content and status of exchanges. | Can the exact issued package and responses be reconstructed? |
| Native models, drawings, and issued PDFs | Connects editable source material with distributed output. | Which output corresponds to which approved source? |

The inclusion test should be relevance to the engineering or project process. A document belongs in the defined project repository when its identity, revision, availability, or relationship to other project information matters to delivery.

Conversely, payroll records, personal working notes, enterprise financial transactions, and unrelated corporate content may already have suitable authoritative systems. Moving them into ProjectWise solely to maximize the amount stored would create a weak business case.

For databases, multi-file application datasets, and specialist engineering formats, assess the complete dataset and application workflow. Successfully uploading individual files is not enough to demonstrate that the application can safely use or reconstruct the dataset.

# 4. A practical example: controlling a design change

Consider an illustrative roadway project in which a drainage change affects a model, a calculation, two plan sheets, and a specification. The example below is a recommended process design, not a Bentley default or a description of a particular agency's implementation.

| Stage | Controlled action | Evidence to retain |
|:--|:--|:--|
| Identify | Record the change request and identify affected information. | Change identifier, reason, responsible person, affected items. |
| Develop | Revise the source files in the agreed authoring environment. | Working content and relevant development history. |
| Check | Have the designated checker review the related items together. | Comments, responses, and the precise review baseline. |
| Authorize | Determine whether the package is suitable for its stated use. | Approver, decision, date, conditions, and package identity. |
| Issue | Generate and verify output, then transmit the selected package. | Issued files, revision register, recipients, and delivery evidence. |
| Respond and close | Track responses and prepare the next revision or close the change. | Accepted responses, supersession links, and final disposition. |

The failure this process addresses is subtle: each file could be correct in isolation, yet the assembled package could still mix an old specification, a new calculation, and a drawing that references the wrong baseline.

The proposed control is therefore at two levels. **Document control** establishes each item's identity and state. **Package control** establishes that the items belong together for a particular issue. ProjectWise's value should be evaluated at both levels.

Dependency history also deserves explicit attention. Bentley's legacy training documents selecting particular reference versions for a master document. The implementation should demonstrate how its actual baseline and reference-version configuration supports reproducible review and delivery. [35: Reference-version concepts][S35]

A useful acceptance exercise is to reopen an earlier issued package after subsequent work has progressed. The reviewer should be able to establish what was issued, what dependencies or outputs were included, who approved it, and how later changes relate to it. If only the latest source files can be located, the historical-control objective has not yet been demonstrated.

# 5. What public evidence says about actual use

## 5.1 USACE: enterprise engineering information and knowledge management

USACE's January 14, 2026 revision of ECB 2017-16 identifies ProjectWise as its corporate engineering data-management tool. The directive requires project/program/system identification and document-type metadata, minimum auditing of creation, modification and deletion, and caching arrangements for applicable virtual teaming. It also distinguishes managed native files from record documents that can be consumed by an appropriate EDRMS. [17: USACE directive, pp. 1–2][S17]

**What this establishes:** a major engineering owner has tied the repository to organizational procedures and information governance. It is evidence of adoption and intended function, not a quantified comparison against competing software.

## 5.2 West Virginia: construction documents as usable project evidence

Section 111.1.5 of WVDOH's August 2025 construction-manual file directs electronic project files into ProjectWise. It connects organized records with retrieval, payment support, material and work verification, federal-aid reimbursement, and disputes or claims. It also describes establishing the project filing structure before work begins. [20: WVDOH manual, section 111.1.5][S20]

**What this establishes:** the rationale includes day-to-day contract administration and evidence, extending beyond CAD production. The relevant passage was available through the search index; direct retrieval of the complete PDF did not finish during this research. This report does not assert that it verified every later manual change or any retention period.

## 5.3 MnDOT: a defined boundary between active work and records

MnDOT assigns CADD and other active project files to ProjectWise until closeout, then directs record files to eDOCS. Its broader storage policy explains efficiency and risk reasons for consistent information placement. [18: MnDOT storage standard][S18]

**What this establishes:** an organization can value ProjectWise highly while assigning long-term records to a different platform. Clear handoff rules can be a strength of the architecture.

## 5.4 NCDOT: the repository is an operated service

NCDOT's CADD Manual describes a support team responsible for configuration, maintenance, and access. It separately describes deleted-file restoration and rolling backups, including when support must involve Bentley. Consultant access is associated with specific work areas. [36: NCDOT CADD Manual, sections 2.4.4–2.4.6][S36]

**What this establishes:** recovery, access provisioning, and administration are explicit operating responsibilities. The recovery windows in NCDOT's manual describe that deployment and should not be generalized to all ProjectWise customers.

## 5.5 GAI: a reported performance improvement with a clear evidence limit

A Bentley-published GAI Consultants case study reports more than a 75% reduction in typical file-opening time in home and office testing and more than 25% on mobile devices. It also describes a subcontractor coordination example in which direct access to shared project information helped the team turn around late changes. The story is copyright 2024 and includes deployment context from September 2023. [22: GAI case study][S22]

**What this establishes:** there is a documented customer example of material workflow improvement. The source is a vendor-published success story without a controlled cross-product benchmark. Its percentages should not be used as a forecast for another organization.

# 6. How ProjectWise compares with other repository choices

## 6.1 Compare workflows and ownership costs

The following is an analytical comparison. The evaluation questions are recommendations, not claims that competitors lack the relevant feature.

| Option | Typical reason to evaluate it | Decisive evaluation question |
|:--|:--|:--|
| ProjectWise | Connected engineering production, owner standards, governed project delivery. | Does the exact design and document workflow work reliably with the deployed integrations? |
| Shared file server or network storage | Familiar access with existing infrastructure and administrative practices. | How will the organization establish revision, approval, issue, and dependency controls around it? |
| SharePoint / Microsoft 365 | General document collaboration and an existing enterprise information environment. | Can it meet the engineering workflow requirements, including any integrations, at a favorable total cost? |
| Autodesk Forma Data Management, formerly Autodesk Docs | Project information management within an Autodesk-centered delivery environment. | How well do the selected authoring, collaboration, review, and partner workflows fit together? |
| Oracle Aconex | Formal project documents, communications, exchange, and accountability across organizations. | Does the overall architecture also meet the native engineering-production requirements? |
| Dedicated records repository | Retention, preservation, disposition, and access to official records. | What should be transferred from active production, with what evidence and metadata? |

## 6.2 Versioning and approval are not exclusive to ProjectWise

Microsoft documents SharePoint version history, content approval, draft visibility, and required check-out. Microsoft Purview documentation separately describes retention policies and labels, including record-related controls and preservation behavior. Consequently, “ProjectWise has versions and SharePoint does not” is not a defensible selection argument. [25: SharePoint versioning][S25], [26: Microsoft retention][S26]

The useful comparison is whether each platform, with its required configuration and integrations, supports the work accurately and economically. General document capability alone does not prove engineering integration; engineering integration alone does not settle enterprise records requirements.

## 6.3 Other engineering and construction platforms have substantial controls

Autodesk now calls Autodesk Docs **Forma Data Management**. Its current overview describes a CDE for project information, version control, and standardized workflows; its own technical marketing also describes connections with authoring applications and document exchange. Oracle describes Aconex document governance, version histories, workflows, project communications, and an unalterable audit trail. [27: Autodesk product naming and scope][S27], [28: Autodesk collaboration explanation][S28], [29: Oracle Aconex][S29]

These are overlapping alternatives or potential components of a wider solution. ProjectWise's case should rest on demonstrated fit for the organization's applications, ownership model, project controls, and delivery requirements.

## 6.4 Coexistence requires explicit authority

A recommended coexistence design assigns an owner and purpose to each system. For example, the engineering team could maintain source design content in ProjectWise while a separate enterprise system remains authoritative for commercial transactions.

For each interface, define whether information is referenced, copied for a specific purpose, formally issued, or synchronized. Document what happens when a source changes, a permission is revoked, or an exchange fails. Copying data between systems without these rules can create two apparently authoritative versions.

# 7. The costs, constraints, and failure modes

## 7.1 Configuration determines how much value is realized

Bentley's ProjectWise Web troubleshooting documentation connects feature availability to permissions, environment settings, identity configuration, and plug-in versions. It provides a concrete reminder that two organizations can have noticeably different experiences with the same product family. [12: ProjectWise Web troubleshooting][S12]

Common implementation risks to assess include inconsistent folder structures, excessive metadata, obscure status names, missing search coverage, unclear review responsibilities, and interfaces that are poorly suited to occasional users. These are evaluation risks, not findings that every deployment has those defects.

Start with a small, coherent configuration that supports real tasks. Every required field, state, and exception should have a business reason and an owner.

## 7.2 Administration continues after deployment

A sustainable service needs someone to own templates, permissions, user provisioning, support, compatibility testing, capacity, and workflow changes. Engineering standards and records responsibilities also need named owners; these should not silently become the database administrator's job.

Cloud hosting can change the division of responsibility. Bentley's G-Cloud submission describes infrastructure, support, backups, and service-level arrangements for its specified offering. That does not eliminate the customer's need to govern its project information. [15: G-Cloud service definition][S15]

## 7.3 Integration and user experience must be validated

An integration that works for a simple drawing may behave differently with complex references, specialist datasets, a different software release, or an external partner's environment. Set acceptance criteria around representative tasks and then retain a supported configuration baseline.

Training should cover the handful of decisions users repeatedly face: where to create information, how to identify the right item, when to check in, when to version, how to submit a review, and how to issue a package. Persistent workarounds deserve investigation because they may signal an unsuitable workflow or a missing capability.

## 7.4 A central dependency requires a continuity plan

When staff depend on one environment, access problems can affect many activities. A recommended continuity plan should address connectivity loss, authentication issues, unavailable services, recovery of local work, and access to critical issued information.

Define the recovery point objective, meaning the tolerable amount of lost work, and recovery time objective, meaning the tolerable interruption. Test them through the operating arrangement actually purchased. A stated service-availability percentage does not by itself answer either question.

## 7.5 Exporting files is only part of an exit plan

The Bentley-authored G-Cloud listing describes end-of-contract export and deletion arrangements. Those terms belong to the particular published offering and demonstrate why exit provisions should be examined during selection. [16: G-Cloud service listing][S16]

A recommended exit test should recover selected content together with document identifiers, metadata, versions, dependencies, issue records, and approval evidence. Identify any elements that require separate export, transformation, or an archive viewer. Also verify what the destination can actually import and interpret.

The cost of leaving includes mapping, validation, retraining, historical access, and parallel operation during transition. Treat that cost as part of the initial business case.

# 8. Document management, records, and security are related responsibilities

## 8.1 Versions, Final status, and backups serve different purposes

Bentley's version help says versions can be deleted unless permissions prevent it. Its workflow help says authorized users can remove Final status. Those documented behaviors mean that a normal version or Final flag should not be equated with immutable preservation. [3: Version deletion behavior][S03], [4: Final status][S04]

Use the following distinctions when designing the service:

| Control | Primary purpose | Separate question to resolve |
|:--|:--|:--|
| Version snapshot | Preserve a selected point in the document's development. | Can it be deleted, and is the required history captured? |
| Approval or completion status | Express the result of a defined workflow. | Who can reverse it, and what happens after a content change? |
| Backup and recovery | Restore information or service after loss or corruption. | How much work can be recovered, and how quickly? |
| Retention and disposition | Keep and dispose of records according to approved rules. | Which event starts retention, and who authorizes disposal? |
| Issued package history | Establish the information exchanged for a stated purpose. | Can exact content, recipients, and responses be reconstructed? |

These controls can work together, but one does not substitute for all the others.

## 8.2 Define the official record and the closeout handoff

A recommended records design identifies the official record categories, the responsible records authority, retention triggers, preservation requirements, and any hold or disposition process. It also specifies whether records remain in ProjectWise or transfer to another approved system.

The closeout package should be defined before closeout. For a complex design, an accepted record might require native content, verified readable outputs, a document register, associated review and issue evidence, and enough context to interpret dependencies. The exact scope belongs to the owner's approved information and records requirements.

This report does not certify legal, regulatory, archival, or ISO compliance for any particular installation. Such a conclusion would require examining that installation's controls against its actual obligations. The value of the repository is that it can support a controlled process; compliance remains a property of the complete implementation and its operation.

## 8.3 Evaluate security at the deployment boundary

Security review should examine the selected hosting arrangement, authentication, project permissions, external access, administrative privileges, logging, endpoint copies, backup protection, and data location. Obtain current evidence for the actual service scope and region being considered.

Bentley's gateway documentation describes an established architecture for routing access without directly exposing an integration server, including optional temporary caching. It illustrates that connectivity architecture is an engineered part of the service. It is not a recommendation to deploy a particular historical network configuration today. [34: Gateway/Connection Server][S34]

The same scope discipline applies to certifications and vendor statements. Evidence for one service or hosting environment should not be silently generalized to every customer-managed server, connector, endpoint, or external recipient.

# 9. Building a credible business case

## 9.1 Measure work saved and errors avoided

The main financial comparison is the total cost of producing and managing reliable project information. Storage capacity is one component.

Useful benefit categories include reduced search time, less package assembly, fewer repeated transfers, faster review administration, fewer incorrect-document incidents, and less effort reconstructing project history. These are measurement categories proposed by this report; no universal savings rate is assumed.

A useful annual model is:

**Annual net benefit = realized labor value + measured avoided costs + demonstrable retired costs − recurring platform and operating costs.**

Calculate first-year benefit separately by subtracting migration, implementation, and training costs. Treat potential schedule acceleration as a benefit only where the organization can explain its actual operational or financial effect.

## 9.2 Illustrative calculation, not a quotation or forecast

Suppose 100 regular users each save 10 minutes per working day across 220 days. Assume a loaded labor value of $80 per hour and that 50% of the released time becomes usable organizational capacity.

| Input or calculation | Illustrative value |
|:--|--:|
| Users | 100 |
| Minutes saved per user per day | 10 |
| Working days per year | 220 |
| Gross hours released | 3,666.7 |
| Gross labor value at $80/hour | $293,333 |
| Realized capacity value at 50% | $146,667 |

The 50% adjustment prevents treating every saved minute as cash. The result represents possible capacity value. Actual cash savings require a credible link to reduced expenditure; additional delivery capacity requires demand and the ability to redeploy staff.

The sensitivity is substantial. Under the same assumptions, five minutes saved per day produces approximately $73,333 of realized annual value; fifteen minutes produces approximately $220,000. These figures provide a scale for comparison with a real quotation and operating budget. They are entirely hypothetical and are not derived from the GAI case study.

## 9.3 Include the full cost structure

Budget for subscriptions and entitlements, environment or hosting charges, configuration, administration, training, migration, integrations, support, storage growth, recovery, security work, and eventual export. Include partners' participation costs where the project owner bears them.

Avoid comparing a fully governed ProjectWise deployment against the purchase price of raw storage alone. Equally, avoid comparing it against a hypothetical alternative that has been assigned every possible integration cost while ProjectWise administration is omitted. Use equivalent requirements and the same time horizon.

## 9.4 Use measures that reveal whether the service is working

| Measure | Recommended measurement approach |
|:--|:--|
| Time to find the right item | Timed tasks using known documents and ordinary project roles. |
| Time to assemble an issue | Start with the approved baseline; end with a verified package and register. |
| Review cycle time | Measure submission to completed response; distinguish waiting from active review. |
| Wrong-version incidents | Record incidents and causes per issue package or project period. |
| Metadata quality | Sample required values for completeness and correctness. |
| Engineering access performance | Measure first and repeat opens with representative references and workspaces. |
| Adoption and support effort | Track use of the intended process, recurring workarounds, and support hours. |
| Closeout completeness | Test whether an uninvolved reviewer can reconstruct a selected delivery record. |

# 10. When the fit is strong, conditional, or weak

## 10.1 Strong fit

ProjectWise deserves serious consideration when several of the following conditions are present: substantial native engineering production, complex file dependencies, frequent multidisciplinary changes, geographically distributed contributors, formal owner standards, significant review and issue requirements, or an existing Bentley-oriented delivery environment.

The rationale is cumulative. One feature alone may be available elsewhere. A reliable combination of production integration, document controls, partner participation, and repeatable standards can be more difficult and costly to reproduce.

## 10.2 Conditional fit

Mixed application environments, occasional external participation, or organizations already operating a mature CDE require a more specific assessment. ProjectWise may be the engineering-production component, the owner environment for selected projects, or an unnecessary additional repository.

Resolve that question through a workflow demonstration and a clearly defined boundary between systems. An enterprise preference should not conceal application-specific problems or force every department into a process that adds little value for its work.

## 10.3 Weaker fit

The case becomes weaker when the main requirement is low-cost storage of uncomplicated files, when collaboration is limited, when formal lifecycle controls are unnecessary, or when another established platform already satisfies the required workflows with lower total effort.

It is also weaker when the organization is unwilling to fund administration and information governance. Buying an advanced repository without operating it properly can preserve the appearance of control while leaving the underlying information problems unresolved.

## 10.4 A practical decision rule

Proceed when a representative pilot demonstrates the required engineering and document tasks, the operating responsibilities are funded, and the measured benefits justify the full cost. If those conditions do not hold, narrow the scope, improve the design, or select another approach.

# 11. An implementation approach that preserves the business purpose

The following is a recommended sequence for an organization adopting ProjectWise or improving an existing installation.

1. **Define the information problem.** Identify specific incidents, delays, retrieval failures, or owner requirements. State the desired result in terms users recognize.
2. **Assign system responsibility.** Decide which information belongs in ProjectWise, which systems remain authoritative elsewhere, and how closeout works.
3. **Define a minimum information standard.** Establish project identifiers, document types, titles, responsibilities, revision conventions, and permitted-use terminology.
4. **Design a small number of useful workflows.** Define review evidence and exception handling. Remove states that do not change responsibility, authority, or a meaningful project outcome.
5. **Configure and test access.** Use representative internal and external accounts. Test onboarding, changes of role, offboarding, and access to issued content.
6. **Validate authoring integrations.** Exercise real references, workspaces, output settings, and specialist application datasets.
7. **Pilot with both frequent and occasional users.** Include designers, project managers, document controllers, reviewers, IT support, and an external participant where relevant.
8. **Migrate deliberately.** Inventory source data, map identifiers and metadata, preserve required history, and validate dependencies. Decide how duplicate and obsolete content will be handled under approved rules.
9. **Demonstrate recovery and exit.** Restore a representative item or package and export a usable historical set with its required context.
10. **Roll out and measure.** Provide task-based guidance, maintain support ownership, review the metrics, and improve the configuration based on observed difficulties.

Migration deserves a separate acceptance record. File counts alone do not demonstrate success. Reconcile expected documents and versions, verify content integrity where appropriate, confirm metadata and permissions, and open representative dependent datasets. Document any history or relationship that cannot be carried across automatically.

Recommended accountability is similarly concrete: a business owner decides the service's purpose; a platform owner operates it; engineering standards owners govern application resources; document controllers govern delivery conventions; project managers manage participation; and the records authority determines official-record obligations.

# 12. Pilot acceptance questions

Use the following questions to turn a product demonstration into an evaluation of actual organizational needs. The answers should be observed, not merely asserted.

| Area | Evidence the pilot should produce |
|:--|:--|
| Retrieval | A user finds the correct document without knowing its folder path. |
| Dependencies | A realistic design opens with the intended references and resources. |
| Editing | Two users can explain and correctly use the supported editing behavior. |
| History | A reviewer can locate a selected prior milestone after further changes. |
| Review | A submitted item reaches the correct reviewer with the necessary context. |
| Approval | The team can establish what was approved, by whom, and for which use. |
| Issuance | The exact issued package and its recipients can be reconstructed. |
| Access | A partner sees the intended scope; unauthorized access is denied. |
| Recovery | A representative loss is recovered through the documented support process. |
| Export | A destination user can interpret selected content and required metadata. |
| Performance | Representative locations meet agreed task-time thresholds. |
| Usability | Occasional users complete common tasks with the planned training and interface. |

Define pass criteria before the pilot. Record the application versions, dataset characteristics, user roles, connection conditions, manual steps, and exceptions. This makes the result repeatable and prevents a polished demonstration from substituting for operational evidence.

# 13. Common questions and misconceptions

**Is ProjectWise only for CAD files?** No. Bentley explicitly describes non-CAD participation through Drive. Whether a given document belongs there depends on the agreed project-information scope. [11: ProjectWise Drive][S11]

**Does the newest file mean the approved file?** No. The organization must establish which revision was approved and what its permitted use is. This is a governance rule that should be demonstrated in the configured workflow.

**Does every participant need the same interface and subscription?** Do not assume so. Current Bentley offerings distinguish Connect and ProjectWise capabilities, and deployment prerequisites matter. Specify each role's required tasks before pricing access. [1: Bentley product overview][S01], [32: Bentley FAQ][S32]

**Does an audit trail mean the repository is an immutable archive?** No. Audit coverage, preservation, permissions, recovery, and official-record controls are separate design questions. The presence of a history screen does not answer all of them.

**Can ProjectWise support an ISO 19650-oriented process?** Bentley describes such configurations in its service materials. A compliance determination still requires matching the actual workflow and information requirements to the applicable standard and project obligations. [15: G-Cloud service definition][S15]

**Does using ProjectWise require abandoning Microsoft 365 or another project system?** The recommended approach is to define each system's purpose and the handoffs between them. The right architecture depends on requirements and demonstrated integration behavior.

**Are AI search and summaries the main reason to adopt it?** They may add value, but the underlying control of source content remains essential. Bentley lists newer AI capabilities in its current offerings; verify entitlement, deployment availability, and output reliability for the intended task. [1: Bentley product overview][S01]

**Will storing everything in ProjectWise guarantee better information?** No. A repository can faithfully store incomplete, contradictory, or poorly classified content. Improvement requires standards, competent review, ownership, and consistent use.

# 14. Assessment

People use ProjectWise as a document store because they need more confidence in how engineering information is produced and used. The strongest business case connects the repository to specific project outcomes: usable native files, recognizable revisions, clear review responsibility, accountable exchanges, retrievable history, and consistent delivery across teams.

The researched documentation supports a substantial engineering document-management use case. Public agency policies demonstrate that the repository can encompass calculations, reports, correspondence, and construction records as well as design files. The boundaries vary by organization, including whether official records remain in ProjectWise or transfer elsewhere.

A sound adoption decision therefore has three parts: demonstrate the important project workflows, fund the operating responsibilities, and measure benefits against the full cost. When those conditions are met, ProjectWise can provide a durable foundation for controlled engineering information throughout project delivery.

# Appendix A. Working glossary

| Term | Meaning used in this report |
|:--|:--|
| CDE | Common data environment: the agreed information-management workflow and supporting solutions. |
| EDMS | Electronic document management system. |
| EDRMS | Electronic document and records management system. |
| Engineering WIP | Engineering work in progress before its relevant review or delivery milestone. |
| Metadata | Information describing an item, such as project identity, type, responsibility, or intended use. |
| Native file | Content in an authoring application's working format. |
| Reference or dependency | Another file or resource needed to use or interpret an item correctly. |
| Version | A stored point in a document's development; exact software semantics must be checked. |
| Revision | A project-defined designation used to communicate a document's evolution or issue. |
| Rendition | Output generated from source content for a different viewing or delivery purpose. |
| Transmittal | A documented exchange identifying information sent to recipients for a stated purpose. |
| Baseline | A specifically identified collection of information used for review, change, or issue. |
| Record | Information designated for retention as evidence under the organization's approved rules. |
| RPO / RTO | Recovery point objective / recovery time objective: tolerable data loss and interruption. |

# Appendix B. Research method and source limitations

Research used publicly accessible Bentley product material, Bentley technical help and support articles, public agency policies and manuals, a customer-authored operating guide, standards-framework guidance, and competing vendors' documentation. The reference list contains 36 sources. All were consulted on September 7, 2026, through direct page or PDF retrieval or, where expressly noted, relevant search-index content.

Bentley's documentation is the primary evidence for product behavior. Agency documents establish how particular owners prescribe or operate their information processes. Vendor success stories establish reported customer experiences and are identified accordingly. Supplier-authored procurement listings are treated as supplier statements, even when hosted on a government marketplace.

Older sources are used only for established mechanisms and conceptual explanations. They are not presented as current installation instructions, compatibility matrices, licensing schedules, or universal contractual terms. Search crawl dates were not treated as publication dates. Product names and current positioning were checked separately; exact suitability still depends on the selected configuration.

This report is a researched explanation and evaluation framework. It is not an inspection of a particular ProjectWise installation, a procurement quotation, a controlled performance benchmark, or an organizational compliance assessment. Illustrative workflows, business-case arithmetic, tables of proposed scope, and pilot criteria are the report's analysis and recommendations.

# Appendix C. Linked source register

<!-- SOURCE_REGISTER -->

**[1. Bentley Systems — ProjectWise product overview][S01]**  
Current product positioning and Connect/ProjectWise distinction; accessed September 7, 2026.

**[2. Bentley Systems — The Levels of ProjectWise Design Integration Application Integration][S02]**  
Technical distinctions among basic storage, in-application access, dependency management, and workspace integration.

**[3. Bentley Systems — Working with Versions — ProjectWise Explorer Help][S03]**  
Read-only snapshots, active versions, sequence numbers, and deletion behavior; Help v11.

**[4. Bentley Systems — Working with Workflows and States — ProjectWise Explorer Help][S04]**  
Workflow states, state security, notifications, and reversible Final status; Help v11.

**[5. Bentley Systems — Using Document Audit Trail — ProjectWise Explorer Help][S05]**  
Administrator-selected activity logging and access to history; Help v11.

**[6. Bentley Systems — Modifying Environment Attributes — ProjectWise Explorer Help][S06]**  
Editing custom document attributes and attribute-record configuration; Help v11.

**[7. Bentley Systems — Modifying Document Permissions (Access Control) — ProjectWise Explorer Help][S07]**  
Document-level access-control interfaces; Help v11.

**[8. Bentley Systems — Performing and Saving Searches][S08]**  
Quick, full-text, advanced, and saved searches; includes version-specific prerequisites.

**[9. Bentley Systems — Creating Renditions — ProjectWise Explorer Help][S09]**  
Composition-server rendition generation and storage; Help v11.

**[10. Bentley Systems — Bentley Infrastructure Cloud — Deliverables][S10]**  
Deliverables Management, transmittals, submittals, RFIs, and correspondence.

**[11. Bentley Systems — ProjectWise Drive][S11]**  
Desktop access for non-CAD workflows and distinction from Explorer integration. Historical licensing wording is not used as a current quotation.

**[12. Bentley Systems — Troubleshooting ProjectWise Web Common Issues][S12]**  
Configuration, permissions, identity, indexing, and plug-in prerequisites affecting feature availability.

**[13. Bentley Systems — Working Remotely with ProjectWise][S13]**  
March 2020; pp. 2–3 on local working directories and reuse of local copies. Used for established mechanisms, not current compatibility.

**[14. Bentley Systems — Your Guide to Digital Transformation with ProjectWise][S14]**  
Vendor guidance on engineering work in progress, standards, and managed workspaces.

**[15. Bentley Systems UK Limited — ProjectWise Lot 2 — Cloud Software Services Definition, G-Cloud 14][S15]**  
Dated May 7, 2024; pp. 3–6. Public procurement submission; service and contractual claims apply to the described offering.

**[16. UK Digital Marketplace / Bentley Systems UK Limited — ProjectWise — G-Cloud 14 service listing][S16]**  
Supplier-authored listing covering service scope, support, export, and end-of-contract processes; not an independent evaluation.

**[17. U.S. Army Corps of Engineers — ECB 2017-16, Revision 3: Bentley ProjectWise as the Corporate Tool for Engineering Data Management in USACE][S17]**  
January 14, 2026; two pages; stated expiration January 14, 2028. Policy paragraphs 2, 4, and 6.

**[18. Minnesota Department of Transportation — Digital File Storage — Standards][S18]**  
Agency assignment of active project files to ProjectWise and closeout record files to eDOCS.

**[19. Minnesota Department of Transportation — MnDOT CADD and ProjectWise Resources][S19]**  
Agency standards, authorized partner access, and external licensing requirements.

**[20. West Virginia Department of Transportation / Division of Highways — 2022 Construction Manual, August 2025 file][S20]**  
Section 111.1.5, printed p. 104. Relevant text was available through the search index; direct PDF retrieval did not complete during research. No claim of reviewing the entire manual or verifying all subsequent revisions.

**[21. Texas Department of Transportation — 3.3.5 File Management Best Practices][S21]**  
ProjectWise standard folder structure, shared files, and closeout archiving.

**[22. Bentley Systems / GAI Consultants — GAI Consultants Achieves Unprecedented Productivity and Collaboration by Implementing ProjectWise][S22]**  
Copyright 2024; three pages; deployment context includes September 2023. Vendor-published customer case study, not an independently controlled benchmark.

**[23. HDR — ProjectWise Quick Start Manual][S23]**  
Updated July 2024; especially p. 9, documenting check-out, check-in, copy-out, and server-copy updates.

**[24. UK BIM Framework — Guidance Part C: Facilitating the Common Data Environment (Workflow and Technical Solutions)][S24]**  
Edition 1, September 2020; conceptual guidance, especially printed pp. 7–14. Not used as a substitute for the current ISO standard or national annex.

**[25. Microsoft — Enable and Configure Versioning for a List or Library][S25]**  
SharePoint version history, approvals, draft visibility, and check-out settings.

**[26. Microsoft Learn — Learn About Retention for SharePoint and OneDrive][S26]**  
Retention policies, labels, records, and Preservation Hold library behavior.

**[27. Autodesk — Forma Data Management — Formerly Autodesk Docs][S27]**  
Current name and common-data-environment positioning verified through Autodesk search-index content and the former Docs page redirect.

**[28. Autodesk — How Forma Data Management (Formerly Autodesk Docs) Improves Project Collaboration][S28]**  
Page carries February 16, 2024 byline and updated product naming; vendor explanation of authoring integrations and document controls.

**[29. Oracle — Aconex Construction Project Management Software][S29]**  
Vendor description of version control, document workflows, project communications, and audit trail.

**[30. Bentley Systems — Find Support for Software Developers — ProjectWise SDK][S30]**  
Client SDK and event hooks for custom ProjectWise utilities.

**[31. Microsoft Learn — ProjectWise Design Integration — Connectors][S31]**  
Document, version, reference, and workflow operations; listed actions are marked Preview.

**[32. Bentley Systems — Bentley Infrastructure Cloud — Frequently Asked Questions][S32]**  
Current entitlements and cloud-deployment prerequisites for recently announced enhancements.

**[33. Bentley Systems — Creating Documents][S33]**  
Published training overview covering document creation, placeholders, and metadata.

**[34. Bentley Systems — ProjectWise Gateway/Connection Server [TN]][S34]**  
Established routing, storage-access, and temporary-caching architecture; not a prescribed current network configuration.

**[35. Bentley Systems; hosted by Georgia DOT — ProjectWise V8i SELECTseries 4 User Essentials][S35]**  
Legacy Bentley training, copyright 2012, hosted 2013; reference-version handling and delta transfer concepts only. Not a current product-support matrix.

**[36. North Carolina Department of Transportation — NCDOT CADD Manual][S36]**  
Section 2.4.4, printed p. 10, and sections 2.4.5–2.4.6, p. 11; deployment-specific recovery, access, and administration practices.

[S01]: https://www.bentley.com/en/products/projectwise/
[S02]: https://bentleysystems.service-now.com/community?id=kb_article_view&sysparm_article=KB0019964
[S03]: https://docs.bentley.com/LiveContent/web/ProjectWise%20Explorer%20Help-v11/en/GUID-9514B218-CCCB-DBC7-C58B-3DA4BEE344EC.html
[S04]: https://docs.bentley.com/LiveContent/web/ProjectWise%20Explorer%20Help-v11/en/GUID-FCE60D0A-172E-356D-7190-EB4ECB1F4ABF.html
[S05]: https://docs.bentley.com/LiveContent/web/ProjectWise%20Explorer%20Help-v11/en/GUID-46D97588-9FA9-B070-C03E-86E78B4C760B.html
[S06]: https://docs.bentley.com/LiveContent/web/ProjectWise%20Explorer%20Help-v11/en/GUID-C3FE6A44-1A0D-EAF0-7B7B-FF8A10FABB96.html
[S07]: https://docs.bentley.com/LiveContent/web/ProjectWise%20Explorer%20Help-v11/en/GUID-C32A11C1-2D2C-3210-9B47-7F51E7CBC07C.html
[S08]: https://bentleysystems.service-now.com/community?id=kb_article&sysparm_article=KB0029362
[S09]: https://docs.bentley.com/LiveContent/web/ProjectWise%20Explorer%20Help-v11/en/GUID-B623F695-36C9-0F20-2D3C-26C51628042E.html
[S10]: https://bentleysystems.service-now.com/community?id=kb_article&sysparm_article=KB0036129
[S11]: https://bentleysystems.service-now.com/community?id=kb_article&sysparm_article=KB0029238
[S12]: https://bentleysystems.service-now.com/community?id=kb_article_view&sysparm_article=KB0046378
[S13]: https://www.bentley.com/wp-content/uploads/document-Working-Remotely-With-ProjectWise-LTR-EN-0320.pdf
[S14]: https://www.bentley.com/wp-content/uploads/ebook-projectwise-digital-transformation-en.pdf
[S15]: https://assets.applytosupply.digitalmarketplace.service.gov.uk/g-cloud-14/documents/711959/722749461633199-service-definition-document-2024-04-24-1303.pdf
[S16]: https://www.applytosupply.digitalmarketplace.service.gov.uk/g-cloud-14/services/722749461633199
[S17]: https://legacy.wbdg.org/FFC/ARMYCOE/COEECB/ecb_2017_16_rev_3.pdf
[S18]: https://www.dot.state.mn.us/policy/it-data/d-001.html
[S19]: https://www.dot.state.mn.us/digital-delivery/cadd.html
[S20]: https://transportation.wv.gov/highways/mcst/Documents/2022ConstructionManualAugust2025.pdf
[S21]: https://www.txdot.gov/manuals/des/pse/chapter-3--plan-set-development/section-3--drafting-guidelines/file-management-best-practices.html
[S22]: https://www.bentley.com/wp-content/uploads/gai-success-story-en.pdf
[S23]: https://projectwise.hdrinc.com/wp-content/uploads/2024/07/ProjectWiseQuickStartManual.pdf
[S24]: https://ukbimframework.org/wp-content/uploads/2021/02/Guidance-Part-C_Facilitating-the-common-data-environment-workflow-and-technical-solutions_Edition-1.pdf
[S25]: https://support.microsoft.com/en-us/sharepoint/lists/documents-and-library/enable-and-configure-versioning-for-a-list-or-library
[S26]: https://learn.microsoft.com/en-us/purview/retention-policies-sharepoint
[S27]: https://www.autodesk.com/products/forma-data-management/overview
[S28]: https://www.autodesk.com/blogs/aec/2024/02/16/how-autodesk-docs-improves-project-collaboration/
[S29]: https://www.oracle.com/construction-engineering/aconex/
[S30]: https://www.bentley.com/en/support/software-developers/
[S31]: https://learn.microsoft.com/en-us/connectors/bentley/
[S32]: https://bentleysystems.service-now.com/community?id=kb_article&sysparm_article=KB0036135
[S33]: https://www.bentley.com/en/webinars/creating-documents/
[S34]: https://bentleysystems.service-now.com/community?id=kb_article_view&sysparm_article=KB0021098
[S35]: https://www.dot.ga.gov/PartnerSmart/DesignManuals/ProjectWise/ProjectWiseV8iSs4UserEss_Georgia_DOT_17-Jul-2013.pdf
[S36]: https://connect.ncdot.gov/resources/CADD-Integration/Documents/NCDOT%20CADD%20Manual.pdf
