# AMS API Entity Reference Guide

A comprehensive reference to the AASHTOWare AMS data model, documenting all 795 entities, their properties, relationships, and navigation patterns. This guide serves as your complete technical reference for understanding and working with the AMS API entity structure.

## Introduction to the AMS Data Model

Foundation

The AASHTOWare Asset Management Service data model represents one of the most comprehensive transportation infrastructure management schemas in existence. Think of it as a detailed blueprint that describes every aspect of highway construction and maintenance projects - from the initial contract award through daily work tracking to final payment processing. This entity model forms the backbone of state DOT operations, enabling them to manage billions of dollars in infrastructure projects with precision and accountability.

Understanding this data model is like learning a new language - one that describes the complex relationships between contractors, materials, inspections, payments, and compliance requirements. Each entity in the model serves a specific purpose, much like how different departments in a transportation agency each have distinct responsibilities that must work together harmoniously.

📊 Model Statistics

The AMS data model encompasses 795 distinct entity types, representing every aspect of transportation project management. These entities are interconnected through over 2,000 navigation properties, creating a rich web of relationships that mirror real-world project workflows. The model supports both simple lookups and complex multi-level queries that can traverse dozens of relationships to gather comprehensive project insights.

### Understanding Entity Categories

To help you navigate this extensive model, we've organized entities into logical groups based on their business function. Think of these categories as neighborhoods in a city - each has its own character and purpose, but they're all connected by roads (relationships) that allow data to flow between them. Let's explore each category to understand its role in the larger system.

📋

Core Business Entities

The foundation entities like Contract, Project, and Vendor that form the backbone of every transportation project.

⚙️

Operational Entities

Daily work reports, inspections, and field activities that track the actual execution of construction work.

💰

Financial Entities

Payment estimates, change orders, and financial tracking that ensure accurate project accounting.

✅

Compliance Entities

Civil rights, DBE participation, and regulatory compliance tracking required by federal and state law.

## Data Model Architecture Overview

Intermediate

The AMS data model follows a hierarchical structure where certain entities serve as anchors for entire subsystems. Imagine a tree where Contract entities form the trunk, with branches extending to Projects, Items, and ultimately to individual daily work records and material tests. This structure ensures that every piece of data can be traced back to its originating contract, providing complete audit trails and accountability.

Primary Entity Hierarchy

Contract

→

ContractProject

→

Project

Contract

→

ContractItem

→

RefItem

Contract

→

ContractVendor

→

RefVendor

### Key Design Principles

The data model embodies several important design principles that ensure consistency and maintainability. First, it uses a pattern of reference entities (prefixed with "Ref") that serve as master data sources - these are like encyclopedias that define standard items, vendors, and materials that can be reused across multiple contracts. Second, it employs association entities to manage many-to-many relationships, much like how a junction table in a database connects related records. Third, it implements temporal tracking through effective and expiration dates, allowing the system to maintain historical accuracy while supporting changes over time.

🔍 Navigation Property Patterns

Navigation properties in the AMS model follow consistent naming conventions that make relationships clear. Singular properties like "Contract" indicate a one-to-one or many-to-one relationship, while plural properties like "ContractItems" signify one-to-many relationships. Properties ending with "Id" are foreign keys that can be used for filtering and joining, while navigation properties without the "Id" suffix provide direct object access when expanded.

## Understanding Entity Relationships

Intermediate

Entity relationships in the AMS model mirror real-world business relationships in transportation project management. Just as a construction project involves contractors, subcontractors, materials, and inspectors all working together, the data model connects these elements through carefully designed relationships. Understanding these connections is essential for effective API usage, as they determine how you navigate from one piece of information to related data.

| Relationship Type    | Description                                               | Example                                | Navigation Pattern                              |
|----------------------|-----------------------------------------------------------|----------------------------------------|-------------------------------------------------|
| **One-to-Many**      | A single parent entity relates to multiple child entities | Contract → ContractItems               | Use $expand=ContractItems to retrieve all items |
| **Many-to-One**      | Multiple child entities reference a single parent         | ContractItem → Contract                | Use $expand=Contract to include parent details  |
| **Many-to-Many**     | Entities relate through an association entity             | Vendor ↔ Material (via VendorMaterial) | Navigate through the association entity         |
| **Self-Referential** | Entity references itself for hierarchical structures      | ItemFamily → ParentItemFamily          | Traverse hierarchy with recursive $expand       |

Contracts & Projects Entity Group

The cornerstone of the AMS data model, these entities manage the fundamental business objects that define construction projects. Every activity in the system ultimately traces back to a contract, making this group essential for understanding the entire model.

Contract

The Contract entity serves as the primary organizing structure for all construction activities. Think of it as the master agreement that governs an entire construction project, containing terms, conditions, and specifications that all work must follow. A contract typically represents a legally binding agreement between a state DOT and a prime contractor, though it can also encompass various other agreement types such as maintenance contracts or emergency repairs.

#### Key Properties

| Property Name       | Type                                                                                   | Description                                                        |
|---------------------|----------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| Id                  | Edm.Int64 Key | Unique identifier for the contract                                 |
| ContractNumber      | Edm.String                                        | Human-readable contract identifier used in business communications |
| ContractDescription | Edm.String                                        | Detailed description of the contract scope and purpose             |
| AwardDate           | Edm.DateTimeOffset                                | Date when the contract was officially awarded                      |
| CompletionDate      | Edm.DateTimeOffset                                | Scheduled or actual completion date for all contract work          |
| ContractAmount      | Edm.Decimal                                       | Total monetary value of the contract                               |
| ContractStatus      | Edm.String                                        | Current lifecycle status (Active, Completed, Suspended, etc.)      |

#### Navigation Properties

**ContractProjects** (Collection) - All projects associated with this contract

**ContractItems** (Collection) - Line items defining work and materials

**ContractVendors** (Collection) - Prime and subcontractors working on the contract

**PayEstimates** (Collection) - Payment estimates submitted for work completed

**ChangeOrders** (Collection) - Modifications to the original contract terms

Project

The Project entity represents a distinct segment of work within a contract, often corresponding to a specific geographical location or functional component. For example, a single contract might include multiple projects for different highway segments or bridge structures. Projects help organize work for management, reporting, and federal funding purposes. Each project maintains its own schedule, budget allocation, and progress tracking independent of other projects in the same contract.

#### Key Properties

| Property Name    | Type                                                                                   | Description                                    |
|------------------|----------------------------------------------------------------------------------------|------------------------------------------------|
| Id               | Edm.Int64 Key | Unique identifier for the project              |
| ProjectNumber    | Edm.String                                        | Federal or state project identification number |
| ProjectName      | Edm.String                                        | Descriptive name for the project               |
| RouteNumber      | Edm.String                                        | Highway or route designation where work occurs |
| BeginMilePost    | Edm.Decimal                                       | Starting location of the project segment       |
| EndMilePost      | Edm.Decimal                                       | Ending location of the project segment         |
| FederalAidNumber | Edm.String                                        | Federal funding authorization identifier       |

#### Navigation Properties

**ContractProjects** (Collection) - Links to contracts containing this project

**ProjectFunding** (Collection) - Funding sources and allocations

**ProjectLocations** (Collection) - Detailed geographic information

ContractItem

ContractItem entities define the specific work items and materials that make up a contract. Each item represents a billable line item with its own quantity, unit price, and specifications. These items form the basis for payment calculations and progress tracking. Think of contract items as the detailed shopping list for a construction project - each one specifies exactly what needs to be built or supplied, in what quantity, and at what agreed-upon price.

#### Key Properties

| Property Name   | Type                                                                                   | Description                                  |
|-----------------|----------------------------------------------------------------------------------------|----------------------------------------------|
| Id              | Edm.Int64 Key | Unique identifier for the contract item      |
| ContractId      | Edm.Int64                                         | Reference to the parent contract             |
| ItemNumber      | Edm.String                                        | Line item number in the contract             |
| ItemDescription | Edm.String                                        | Detailed description of the work or material |
| Quantity        | Edm.Decimal                                       | Amount of work or material required          |
| UnitPrice       | Edm.Decimal                                       | Price per unit of measure                    |
| UnitOfMeasure   | Edm.String                                        | Measurement unit (CY, LF, EA, etc.)          |

Vendors & Subcontractors Entity Group

These entities manage information about companies and individuals involved in construction projects. From prime contractors to material suppliers, this group tracks capabilities, certifications, and participation across contracts. Understanding vendor relationships is crucial for compliance tracking and subcontractor management.

RefVendor

RefVendor serves as the master vendor record, containing all permanent information about a company or individual that does business with the DOT. This includes contractors, subcontractors, suppliers, consultants, and service providers. The "Ref" prefix indicates this is reference data - a single source of truth about each vendor that can be referenced by multiple contracts and projects. This design prevents data duplication and ensures consistency when vendor information changes.

#### Key Properties

| Property Name          | Type                                                                                   | Description                                            |
|------------------------|----------------------------------------------------------------------------------------|--------------------------------------------------------|
| Id                     | Edm.Int64 Key | Unique identifier for the vendor                       |
| VendorNumber           | Edm.String                                        | Business registration or tax ID number                 |
| VendorName             | Edm.String                                        | Legal business name                                    |
| VendorType             | Edm.String                                        | Classification (Prime, Sub, Supplier, DBE, etc.)       |
| PrequalificationStatus | Edm.String                                        | Current qualification to bid on contracts              |
| DBECertification       | Edm.Boolean                                       | Disadvantaged Business Enterprise certification status |

#### Navigation Properties

**ContractVendors** (Collection) - All contract participations

**VendorAddresses** (Collection) - Business locations and contacts

**VendorCertifications** (Collection) - Professional certifications and licenses

**SubcontractorAgreements** (Collection) - Subcontract relationships

Subcontract

The Subcontract entity manages the formal agreements between prime contractors and their subcontractors. These records are critical for tracking work delegation, ensuring proper payment flow, and maintaining compliance with subcontracting requirements. Each subcontract defines specific work items, payment terms, and performance obligations that the subcontractor must fulfill.

#### Key Properties

| Property Name        | Type                                                                                   | Description                                  |
|----------------------|----------------------------------------------------------------------------------------|----------------------------------------------|
| Id                   | Edm.Int64 Key | Unique identifier for the subcontract        |
| ContractId           | Edm.Int64                                         | Parent contract reference                    |
| SubcontractorId      | Edm.Int64                                         | Reference to the subcontractor vendor        |
| SubcontractAmount    | Edm.Decimal                                       | Total value of the subcontract               |
| ApprovalStatus       | Edm.String                                        | DOT approval status for the subcontract      |
| PercentageOfContract | Edm.Decimal                                       | Portion of total contract work subcontracted |

Daily Work Report (DWR) Entity Group

Daily Work Reports form the operational heartbeat of construction project tracking. These entities capture what happens on the job site each day - who worked, what they accomplished, which materials were used, and what equipment was deployed. This granular tracking enables accurate payment processing and provides the documentation needed for project analysis and dispute resolution.

DailyWorkReport

The DailyWorkReport entity serves as the daily journal for construction activities. Inspectors and project managers use these reports to document work progress, weather conditions, and any issues that arise. Think of it as the official diary of the construction site - a legal record that captures the story of how the project unfolds day by day. These reports become especially valuable when questions arise about delays, change orders, or payment disputes.

#### Key Properties

| Property Name     | Type                                                                                   | Description                                          |
|-------------------|----------------------------------------------------------------------------------------|------------------------------------------------------|
| Id                | Edm.Int64 Key | Unique identifier for the daily report               |
| ContractId        | Edm.Int64                                         | Contract this report belongs to                      |
| WorkDate          | Edm.DateTimeOffset                                | Date of the work being reported                      |
| WeatherConditions | Edm.String                                        | Weather impact on work activities                    |
| Temperature       | Edm.Decimal                                       | Temperature readings affecting concrete/asphalt work |
| WorkSuspended     | Edm.Boolean                                       | Whether work was halted for any reason               |
| InspectorComments | Edm.String                                        | Inspector's observations and notes                   |

#### Navigation Properties

**DWRItems** (Collection) - Work performed on specific contract items

**DWRLabor** (Collection) - Personnel who worked on site

**DWREquipment** (Collection) - Equipment used during the day

**DWRMaterials** (Collection) - Materials incorporated into the work

DWRItem

DWRItem entities track the actual quantities of work completed each day against specific contract items. This is where planned work meets reality - recording exactly how much of each contract item was installed, removed, or modified. These records feed directly into payment calculations and progress tracking, making them critical for financial accuracy.

#### Key Properties

| Property Name     | Type                                                                                   | Description                              |
|-------------------|----------------------------------------------------------------------------------------|------------------------------------------|
| Id                | Edm.Int64 Key | Unique identifier for the DWR item entry |
| DailyWorkReportId | Edm.Int64                                         | Parent daily work report                 |
| ContractItemId    | Edm.Int64                                         | Contract item being worked on            |
| QuantityToday     | Edm.Decimal                                       | Amount of work completed today           |
| StationBegin      | Edm.String                                        | Starting location of work                |
| StationEnd        | Edm.String                                        | Ending location of work                  |

Testing & Quality Acceptance Entity Group

Quality control is paramount in transportation infrastructure. This entity group manages the complex testing requirements, sampling procedures, and acceptance criteria that ensure materials and workmanship meet specifications. From concrete strength tests to asphalt density measurements, these entities track the science behind safe and durable infrastructure.

MaterialTest

MaterialTest entities record the results of laboratory and field tests performed on construction materials. Every critical material - from structural steel to paint - must pass specific tests before being incorporated into the project. These test results become part of the permanent project record, providing evidence that all materials met required standards. Failed tests trigger remediation processes and may result in material rejection or contract penalties.

#### Key Properties

| Property Name      | Type                                                                                   | Description                                     |
|--------------------|----------------------------------------------------------------------------------------|-------------------------------------------------|
| Id                 | Edm.Int64 Key | Unique identifier for the test record           |
| TestType           | Edm.String                                        | Standard test method (ASTM, AASHTO designation) |
| SampleDate         | Edm.DateTimeOffset                                | When the material sample was collected          |
| TestDate           | Edm.DateTimeOffset                                | When the test was performed                     |
| TestResult         | Edm.Decimal                                       | Numeric test result value                       |
| PassFail           | Edm.String                                        | Whether the test met specifications             |
| SpecificationLimit | Edm.Decimal                                       | Required value per specifications               |

#### Navigation Properties

**Material** - The material being tested

**TestLab** - Laboratory performing the test

**RetestRecords** (Collection) - Follow-up tests if initial test failed

AcceptanceAction

AcceptanceAction entities define the quality control procedures required for different types of work. These are the rules that determine when and how materials and workmanship are verified to meet standards. Think of these as quality checkpoints throughout the construction process - each one specifies what needs to be tested, when it should be tested, and what criteria determine acceptance. These actions ensure consistent quality control across all projects.

#### Key Properties

| Property Name     | Type                                                                                   | Description                                              |
|-------------------|----------------------------------------------------------------------------------------|----------------------------------------------------------|
| Id                | Edm.Int64 Key | Unique identifier for the acceptance action              |
| Name              | Edm.String                                        | Name of the acceptance procedure                         |
| Description       | Edm.String                                        | Detailed description of what's being verified            |
| EvaluationMethod  | Edm.String                                        | How compliance is determined (Statistical, Visual, etc.) |
| SamplingFrequency | Edm.String                                        | How often samples must be taken                          |

Financial & Payment Processing Entity Group

Money flows through construction projects in complex patterns - from initial funding authorization through progress payments to final settlement. This entity group tracks every financial aspect, ensuring contractors get paid for completed work while maintaining strict accountability for public funds. Understanding these entities is essential for payment processing and financial reporting.

PayEstimate

PayEstimate entities represent periodic payment requests submitted by contractors for work completed. Typically processed monthly, these estimates calculate payment based on measured quantities of completed work multiplied by contract unit prices. The pay estimate process involves multiple levels of review and approval, with inspectors verifying quantities, engineers checking calculations, and administrators ensuring compliance with contract terms. Each estimate builds upon previous ones, creating a complete financial history of the project.

#### Key Properties

| Property Name         | Type                                                                                   | Description                                 |
|-----------------------|----------------------------------------------------------------------------------------|---------------------------------------------|
| Id                    | Edm.Int64 Key | Unique identifier for the pay estimate      |
| EstimateNumber        | Edm.Int32                                         | Sequential estimate number (1, 2, 3, etc.)  |
| EstimatePeriodBegin   | Edm.DateTimeOffset                                | Start of the work period covered            |
| EstimatePeriodEnd     | Edm.DateTimeOffset                                | End of the work period covered              |
| CurrentEstimateAmount | Edm.Decimal                                       | Payment requested this period               |
| TotalEarnedToDate     | Edm.Decimal                                       | Cumulative earnings including this estimate |
| RetainageAmount       | Edm.Decimal                                       | Amount withheld as retainage                |

#### Navigation Properties

**PayEstimateItems** (Collection) - Detailed breakdown by contract item

**PayEstimateDeductions** (Collection) - Deductions and adjustments

**ApprovalWorkflow** - Approval chain and signatures

ChangeOrder

ChangeOrder entities manage modifications to the original contract scope, schedule, or price. Construction projects rarely proceed exactly as planned - unforeseen conditions, design updates, and scope changes necessitate formal contract modifications. Each change order must be carefully documented, justified, and approved before work proceeds. These entities track both the business justification and the financial impact of changes, ensuring all parties agree to modified terms.

#### Key Properties

| Property Name         | Type                                                                                   | Description                                            |
|-----------------------|----------------------------------------------------------------------------------------|--------------------------------------------------------|
| Id                    | Edm.Int64 Key | Unique identifier for the change order                 |
| ChangeOrderNumber     | Edm.String                                        | Sequential change order identifier                     |
| Description           | Edm.String                                        | Explanation of what's being changed and why            |
| JustificationCategory | Edm.String                                        | Reason for change (Differing conditions, Errors, etc.) |
| CostImpact            | Edm.Decimal                                       | Net financial impact on contract value                 |
| TimeImpact            | Edm.Int32                                         | Days added to or subtracted from schedule              |

Civil Rights & DBE Compliance Entity Group

Federal regulations require detailed tracking of disadvantaged business enterprise (DBE) participation and civil rights compliance in federally funded projects. This entity group manages the complex reporting requirements that ensure equal opportunity in contracting. From DBE goal setting through actual utilization reporting, these entities help agencies meet their social and economic responsibilities.

DbeCommitment

DbeCommitment entities track promised DBE participation at the time of contract award. Contractors commit to using DBE firms for specific portions of work, and these commitments become contractual obligations. The system monitors whether contractors meet their commitments, with shortfalls potentially resulting in penalties or contract compliance issues. This tracking ensures that DBE participation goals translate into actual business opportunities for disadvantaged firms.

#### Key Properties

| Property Name       | Type                                                                                   | Description                            |
|---------------------|----------------------------------------------------------------------------------------|----------------------------------------|
| Id                  | Edm.Int64 Key | Unique identifier for the commitment   |
| ContractId          | Edm.Int64                                         | Contract containing the DBE goal       |
| DbeVendorId         | Edm.Int64                                         | DBE firm committed to perform work     |
| CommittedAmount     | Edm.Decimal                                       | Dollar value of work committed to DBE  |
| CommittedPercentage | Edm.Decimal                                       | Percentage of contract value committed |
| WorkDescription     | Edm.String                                        | Specific work the DBE will perform     |

#### Navigation Properties

**DbePayments** (Collection) - Actual payments made to DBE

**DbeSubstitutions** (Collection) - Approved DBE replacements

CertifiedPayroll

CertifiedPayroll entities ensure compliance with prevailing wage requirements on federal-aid projects. Contractors must submit weekly certified payrolls documenting that all workers received at least the minimum wages determined by the Department of Labor. These records include detailed information about each worker's classification, hours worked, and wages paid. False statements on certified payrolls can result in criminal prosecution, making accuracy critical.

#### Key Properties

| Property Name          | Type                                                                                   | Description                              |
|------------------------|----------------------------------------------------------------------------------------|------------------------------------------|
| Id                     | Edm.Int64 Key | Unique identifier for the payroll record |
| WeekEnding             | Edm.DateTimeOffset                                | Last day of the payroll week             |
| PayrollNumber          | Edm.Int32                                         | Sequential payroll number                |
| ContractorId           | Edm.Int64                                         | Contractor submitting the payroll        |
| CertificationStatement | Edm.Boolean                                       | Contractor's certification of compliance |

## Complete Entity Index

Reference

This comprehensive index lists all 795 entities in the AMS data model, organized alphabetically with their primary purpose and key relationships. Use this reference when you need to quickly locate specific entities or understand the full scope of available data structures. Each entity name links to its detailed documentation in the OData metadata, allowing you to explore properties and relationships in depth.

💡 Using the Entity Index

Entity names in the AMS model follow consistent naming patterns that reveal their purpose. Entities prefixed with "Ref" contain reference data shared across contracts. Those containing "Association" manage many-to-many relationships. Entities with temporal suffixes like "History" or "Archive" store historical records. Understanding these patterns helps you navigate the model more effectively and predict entity behavior based on naming alone.

### Core Business Entities (A-C)

| Entity Name                 | Category     | Primary Purpose                                  | Key Relationships                          |
|-----------------------------|--------------|--------------------------------------------------|--------------------------------------------|
| **AccActionOptionRateFreq** | Quality      | Acceptance action frequency and rate definitions | AcceptanceActionOption, ActionRelationship |
| **AcceptanceAction**        | Quality      | Quality acceptance procedures and criteria       | AcceptanceActionOptions, MaterialTests     |
| **AccountTransaction**      | Financial    | Financial account transaction records            | SecurityAccount                            |
| **ActionRelationship**      | Quality      | Relationships between quality actions            | MaterialTest, AcceptanceAction             |
| **Address**                 | Reference    | Physical and mailing addresses                   | Vendor, Office, PersonInfo                 |
| **AdministrativeOffice**    | Organization | DOT offices and organizational units             | Contracts, UserRoles                       |
| **Attachment**              | Document     | File attachments and documents                   | Various entities via AttachmentRole        |
| **Bidder**                  | Procurement  | Companies bidding on contracts                   | Proposal, Letting, RefVendor               |
| **BidItem**                 | Procurement  | Individual items in a bid proposal               | Bid, RefItem                               |
| **ChangeOrder**             | Contract     | Contract modifications and amendments            | Contract, ChangeOrderItems                 |
| **CertifiedPayroll**        | Compliance   | Weekly wage compliance documentation             | Contract, PayrollWorker                    |
| **CivilRightsReview**       | Compliance   | Civil rights compliance reviews                  | Contract, ReviewFindings                   |
| **Contract**                | Core         | Primary construction contract record             | Projects, Items, Vendors, PayEstimates     |
| **ContractItem**            | Core         | Line items in a contract                         | Contract, RefItem, DWRItems                |
| **ContractProject**         | Core         | Links contracts to projects                      | Contract, Project                          |
| **ContractTime**            | Schedule     | Contract schedule and time charges               | Contract, TimeExtensions                   |
| **ContractVendor**          | Core         | Vendors working on a contract                    | Contract, RefVendor                        |

### Operational Entities (D-M)

| Entity Name             | Category    | Primary Purpose                       | Key Relationships                       |
|-------------------------|-------------|---------------------------------------|-----------------------------------------|
| **DailyWorkReport**     | Operations  | Daily construction activity records   | Contract, DWRItems, DWRLabor            |
| **DbeCommitment**       | Compliance  | DBE participation commitments         | Contract, RefVendor                     |
| **Document**            | Document    | Project documents and specifications  | Contract, DocumentSubmission            |
| **DWREquipment**        | Operations  | Equipment used in daily work          | DailyWorkReport, Equipment              |
| **DWRItem**             | Operations  | Work quantities by contract item      | DailyWorkReport, ContractItem           |
| **DWRLabor**            | Operations  | Labor hours and classifications       | DailyWorkReport, LaborClassification    |
| **Equipment**           | Resources   | Construction equipment catalog        | VendorEquipment, DWREquipment           |
| **EstimateItem**        | Financial   | Payment details by contract item      | PayEstimate, ContractItem               |
| **ForceAccount**        | Financial   | Extra work performed outside contract | Contract, ForceAccountLabor             |
| **FundingSource**       | Financial   | Federal and state funding sources     | ProjectFunding, Contract                |
| **Inspection**          | Quality     | Field inspection records              | Contract, Inspector, InspectionFindings |
| **ItemFamily**          | Reference   | Hierarchical item categorization      | RefItem, ParentItemFamily               |
| **LaborClassification** | Reference   | Worker trade classifications          | DWRLabor, PrevailingWage                |
| **Letting**             | Procurement | Bid letting events                    | Proposals, Contracts                    |
| **Material**            | Resources   | Construction materials catalog        | MaterialTest, ContractMaterial          |
| **MaterialSource**      | Resources   | Approved material suppliers/sources   | Material, SourceApproval                |
| **MaterialTest**        | Quality     | Material testing results              | Material, TestMethod, Contract          |

### Administrative & Reference Entities (N-Z)

| Entity Name              | Category     | Primary Purpose                     | Key Relationships                   |
|--------------------------|--------------|-------------------------------------|-------------------------------------|
| **NonComplianceIssue**   | Compliance   | Contract compliance violations      | Contract, Resolution                |
| **Office**               | Organization | Physical office locations           | AdministrativeOffice, Address       |
| **PayEstimate**          | Financial    | Periodic payment requests           | Contract, EstimateItems             |
| **PayrollWorker**        | Compliance   | Individual worker payroll records   | CertifiedPayroll, PersonInfo        |
| **PersonInfo**           | Reference    | Individual person records           | UserInfo, VendorPersonnel           |
| **Project**              | Core         | Transportation improvement projects | ContractProjects, ProjectFunding    |
| **ProjectFunding**       | Financial    | Project funding allocations         | Project, FundingSource              |
| **Proposal**             | Procurement  | Contractor bid proposals            | Letting, Bidder, Contract           |
| **RefItem**              | Reference    | Master item catalog                 | ContractItem, ItemFamily            |
| **RefVendor**            | Reference    | Master vendor records               | ContractVendor, VendorCertification |
| **Retainage**            | Financial    | Payment retainage tracking          | PayEstimate, RetainageRelease       |
| **Role**                 | Security     | System security roles               | UserRole, RolePermission            |
| **StockpileInventory**   | Resources    | Material stockpile quantities       | Material, StockpileLocation         |
| **Subcontract**          | Contract     | Subcontractor agreements            | Contract, RefVendor                 |
| **SubcontractorPayment** | Financial    | Payments to subcontractors          | Subcontract, PayEstimate            |
| **TestMethod**           | Quality      | Standard test procedures            | MaterialTest, Specification         |
| **UserInfo**             | Security     | System user accounts                | UserRole, PersonInfo                |
| **VendorCertification**  | Compliance   | Vendor licenses and certifications  | RefVendor, CertificationType        |
| **VendorEquipment**      | Resources    | Equipment owned by vendors          | RefVendor, Equipment                |
| **Workflow**             | Process      | Business process workflows          | WorkflowPhase, WorkflowStep         |

## Best Practices for Working with the AMS Data Model

Advanced

Successfully working with the AMS data model requires understanding not just the structure of individual entities, but also the patterns and practices that lead to efficient, maintainable integrations. These best practices come from real-world experience building systems that process millions of transactions daily while maintaining data integrity and performance.

### Query Optimization Strategies

When querying the AMS API, remember that you're accessing a vast interconnected data model. Inefficient queries can impact not just your application's performance but also the overall system responsiveness for other users. Always use selective field projection with $select to retrieve only needed properties. When expanding navigation properties, be specific about which related entities you need rather than expanding everything. For large result sets, implement pagination using $top and $skip, and consider using $filter to reduce the dataset at the server rather than filtering in your application.

Efficient Query Example

```
// Good: Selective retrieval with specific expansions
GET /Contracts?$select=Id,ContractNumber,ContractAmount
    &$expand=ContractItems($select=ItemNumber,Quantity,UnitPrice;$top=100)
    &$filter=ContractStatus eq 'Active'
    &$top=20

// Avoid: Over-fetching with multiple deep expansions
GET /Contracts?$expand=ContractItems($expand=RefItem),
    ContractVendors($expand=RefVendor($expand=VendorCertifications)),
    PayEstimates($expand=EstimateItems)

```
### Data Integrity Patterns

The AMS model enforces business rules through its structure and relationships. When creating or updating entities, always validate that referenced entities exist and are in valid states. For example, before adding a DWRItem, verify that the referenced ContractItem is active and has remaining quantity available. Use batch operations when making related changes to ensure consistency - if creating a change order with multiple items, submit them together in a single batch to maintain transactional integrity.

⚠️ Common Pitfalls to Avoid

Several patterns commonly cause issues in AMS integrations. Never assume entity IDs are sequential or permanent - always use business keys like ContractNumber for long-term reference. Be aware that some entities have complex state machines - a Contract in "Suspended" status may not accept certain updates. Watch for cascading relationships - deleting a parent entity might remove related children. Always handle pagination properly - large contracts might have thousands of items, and attempting to retrieve them all at once will likely timeout.

### Performance Optimization Techniques

| Technique            | When to Use               | Example Implementation               | Performance Impact                   |
|----------------------|---------------------------|--------------------------------------|--------------------------------------|
| **Batch Operations** | Multiple related updates  | Group updates in $batch requests     | Reduces round trips by 90%           |
| **Delta Queries**    | Synchronization scenarios | Use delta tokens to get only changes | Reduces data transfer by 95%         |
| **Async Processing** | Large data operations     | Use async patterns with callbacks    | Prevents timeouts on long operations |
| **Caching**          | Reference data access     | Cache RefItem, RefVendor locally     | Reduces API calls by 70%             |
| **Index Hints**      | Complex filtering         | Filter on indexed fields first       | Query time reduced by 80%            |

### Integration Architecture Recommendations

When building systems that integrate with the AMS API, consider implementing a service layer that abstracts the complexity of the data model from your application logic. This layer can handle entity relationship navigation, enforce business rules, and manage caching strategies. Implement robust error handling that distinguishes between transient failures (which should be retried) and business rule violations (which require user intervention). Design your integration to be resilient to model changes by using field projection rather than assuming all properties will always be present.

Remember that the AMS data model represents decades of transportation industry experience codified into software. Each entity and relationship exists for specific business reasons, often driven by federal regulations or industry best practices. Taking time to understand not just the technical structure but also the business context will help you build more effective integrations that truly serve the needs of transportation agencies and their partners.

