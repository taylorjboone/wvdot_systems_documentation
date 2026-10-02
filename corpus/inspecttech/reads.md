# InspectTech read-only endpoints

Source: `endpoints.txt` (verb=GET) enriched from `swagger_v1.json`.

Total GET endpoints: **494**  
OData: **11 controllers, 20 endpoints**  
REST (/{apiType}): **96 controllers, 465 endpoints**  
Top-level: **9**


## OData entity sets

### `AssetElements`
_EntityType: `AssetElement` — Keys: `AssetId, ParentSubAssetId, SubAssetId, UserId`._

| Property | EDM type |
|---|---|
| UserId | `Edm.Int32` |
| AssetId | `Edm.Int32` |
| ParentSubAssetId | `Edm.Int32` |
| SubAssetId | `Edm.Int32` |
| AssetName | `Edm.String` |
| ParentElementId | `Edm.Int32?` |
| ParentElementName | `Edm.String?` |
| ParentEnvironmentId | `Edm.Int32?` |
| ElementId | `Edm.Int32` |
| ElementName | `Edm.String` |
| ElementEnvironmentId | `Edm.Int32` |
| ElementType | `Bentley.InspectTech.ORM.Models.StructElementType` |
| ElementSubmissionType | `Bentley.InspectTech.ORM.Models.StructElementSubmissionType` |
| Classification | `Bentley.InspectTech.ORM.Models.StructElementClass` |
| Unit | `Edm.String?` |
| TotalQuantity | `Edm.Int32?` |
| State1 | `Edm.Int32?` |
| State2 | `Edm.Int32?` |
| State3 | `Edm.Int32?` |
| State4 | `Edm.Int32?` |
| State5 | `Edm.Int32?` |

- `GET /odata/AssetElements` — Get the Asset Elements
- `GET /odata/AssetElements/$count` — Get the Asset Elements

OData query examples:
  - `GET https://wvdot-it-api.bentley.com/odata/AssetElements`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetElements?$top=10`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetElements?$top=10&$select=Id,Name`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetElements?$filter=IsDeleted eq false`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetElements?$orderby=Id desc&$top=50`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetElements/$count`

### `AssetTasks`
_EntityType: `AssetTask` — Keys: `Id, UserId`._

| Property | EDM type |
|---|---|
| Id | `Edm.Int32` |
| UserId | `Edm.Int32` |
| Type | `Bentley.InspectTech.ORM.Models.AssetTaskType` |
| AssetId | `Edm.Int32` |
| AssetName | `Edm.String` |
| AssetCode | `Edm.String` |
| AssetType | `Edm.String` |
| ReportTypeId | `Edm.Int32?` |
| ReportType | `Edm.String?` |
| CreatedByUserId | `Edm.Int32` |
| CreatedByUser | `Edm.String` |
| CreateDate | `Edm.DateTimeOffset` |
| LastEditDate | `Edm.DateTimeOffset` |
| Prepopulated | `Edm.Int32` |
| Guid | `Edm.String` |
| InspectionDate | `Edm.DateTimeOffset?` |
| BeginDate | `Edm.DateTimeOffset?` |
| EndDate | `Edm.DateTimeOffset?` |
| OwnerId | `Edm.Int32?` |
| Owner | `Edm.String?` |
| AssignedToId | `Edm.Int32?` |
| AssignedTo | `Edm.String?` |
| CurrentWorkFlowStageId | `Edm.Int32?` |
| CurrentWorkFlowStage | `Edm.String?` |
| CurrentWorkFlowId | `Edm.Int32?` |
| CurrentWorkFlow | `Edm.String?` |
| IsMerged | `Edm.Boolean` |
| WorkFlowStageEnteredDate | `Edm.DateTimeOffset?` |
| WorkFlowStageDueDate | `Edm.DateTimeOffset?` |

- `GET /odata/AssetTasks` — Get the Asset Tasks
- `GET /odata/AssetTasks/$count` — Get the Asset Tasks

OData query examples:
  - `GET https://wvdot-it-api.bentley.com/odata/AssetTasks`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetTasks?$top=10`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetTasks?$top=10&$select=Id,Name`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetTasks?$filter=IsDeleted eq false`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetTasks?$orderby=Id desc&$top=50`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetTasks/$count`

### `AssetTypes`
_EntityType: `AssetType` — Keys: `Id`._

| Property | EDM type |
|---|---|
| Id | `Edm.Int32` |
| Name | `Edm.String` |
| Description | `Edm.String?` |
| FederalSubmissionType | `Bentley.InspectTech.ORM.Models.FederalSubmissionType` |
| Guid | `Edm.String` |

- `GET /odata/AssetTypes` — returns list of data based on odata query
- `GET /odata/AssetTypes/$count` — returns list of data based on odata query

OData query examples:
  - `GET https://wvdot-it-api.bentley.com/odata/AssetTypes`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetTypes?$top=10`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetTypes?$top=10&$select=Id,Name`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetTypes?$filter=IsDeleted eq false`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetTypes?$orderby=Id desc&$top=50`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetTypes/$count`

### `AssetValues`
_EntityType: `AssetValue` — Keys: `AssetId, FieldId, UserId`._

| Property | EDM type |
|---|---|
| UserId | `Edm.Int32` |
| AssetId | `Edm.Int32` |
| FieldId | `Edm.Int32` |
| ReportId | `Edm.Int32?` |
| AssetName | `Edm.String?` |
| AssetType | `Edm.Int32?` |
| FieldName | `Edm.String?` |
| FieldDataType | `Bentley.InspectTech.ORM.Models.FieldDataType` |
| Value | `Edm.String?` |
| PlainText | `Edm.String?` |
| Guid | `Edm.String` |
| UpdatedByUserId | `Edm.Int32?` |
| UpdatedByUser | `Edm.String?` |
| LastUpdatedDate | `Edm.DateTimeOffset?` |
| ChangeLocation | `Edm.String?` |

- `GET /odata/AssetValues` — Get the Asset Values
- `GET /odata/AssetValues/$count` — Get the Asset Values

OData query examples:
  - `GET https://wvdot-it-api.bentley.com/odata/AssetValues`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetValues?$top=10`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetValues?$top=10&$select=Id,Name`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetValues?$filter=IsDeleted eq false`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetValues?$orderby=Id desc&$top=50`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetValues/$count`

### `AssetViewTree`
_EntityType: `AssetViewTree` — Keys: `AssetId, ParentAssetId, RootAssetId`._

| Property | EDM type |
|---|---|
| RootAssetId | `Edm.Int32` |
| ParentAssetId | `Edm.Int32` |
| AssetId | `Edm.Int32` |

- `GET /odata/AssetViewTree` — returns list of Assets based on odata query
- `GET /odata/AssetViewTree/$count` — returns list of Assets based on odata query

OData query examples:
  - `GET https://wvdot-it-api.bentley.com/odata/AssetViewTree`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetViewTree?$top=10`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetViewTree?$top=10&$select=Id,Name`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetViewTree?$filter=IsDeleted eq false`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetViewTree?$orderby=Id desc&$top=50`
  - `GET https://wvdot-it-api.bentley.com/odata/AssetViewTree/$count`

### `Assets`
_EntityType: `Asset` — Keys: `Id, UserId`._

| Property | EDM type |
|---|---|
| Id | `Edm.Int32` |
| UserId | `Edm.Int32` |
| Name | `Edm.String?` |
| Code | `Edm.String?` |
| AssetTypeId | `Edm.Int32?` |
| AssetType | `Edm.String?` |
| DefaultReportTypeId | `Edm.Int32?` |
| DefaultReportType | `Edm.String?` |
| ChildAssetTypeId | `Edm.Int32?` |
| ChildAssetType | `Edm.String?` |
| ChildReportTypeId | `Edm.Int32?` |
| ChildReportType | `Edm.String?` |
| IsDeleted | `Edm.Boolean` |
| IsAssetView | `Edm.Boolean` |
| IsAssetParent | `Edm.Boolean` |
| IsAssetSummary | `Edm.Boolean` |
| Status | `Edm.String?` |
| Guid | `Edm.String` |
| AssetDefinition | `Bentley.InspectTech.ORM.Models.AssetDefinitionType` |
| FederalSubmissionType | `Bentley.InspectTech.ORM.Models.FederalSubmissionType` |
| LastUpdatedDate | `Edm.DateTimeOffset?` |
| CreatedDate | `Edm.DateTimeOffset?` |
| CreateByUserId | `Edm.Int32?` |
| CreatedByUser | `Edm.String?` |

- `GET /odata/Assets` — returns list of data based on odata query
- `GET /odata/Assets/$count` — returns list of data based on odata query

OData query examples:
  - `GET https://wvdot-it-api.bentley.com/odata/Assets`
  - `GET https://wvdot-it-api.bentley.com/odata/Assets?$top=10`
  - `GET https://wvdot-it-api.bentley.com/odata/Assets?$top=10&$select=Id,Name`
  - `GET https://wvdot-it-api.bentley.com/odata/Assets?$filter=IsDeleted eq false`
  - `GET https://wvdot-it-api.bentley.com/odata/Assets?$orderby=Id desc&$top=50`
  - `GET https://wvdot-it-api.bentley.com/odata/Assets/$count`

### `Fields`
_EntityType: `Field` — Keys: `Id`._

| Property | EDM type |
|---|---|
| Id | `Edm.Int32` |
| Name | `Edm.String?` |
| Description | `Edm.String?` |
| IsSearchable | `Edm.Boolean` |
| FormLength | `Edm.Int32` |
| MaxCharacters | `Edm.Int32` |
| IsPrePopulated | `Edm.Boolean` |
| DataType | `Bentley.InspectTech.ORM.Models.FieldDataType` |
| Precision | `Edm.Int32?` |
| FieldChoiceType | `Bentley.InspectTech.ORM.Models.FieldChoiceType` |
| IsReadonly | `Edm.Boolean` |
| IsProtected | `Edm.Boolean` |
| Regex | `Edm.String?` |
| ParentFieldId | `Edm.Int32?` |
| IsRequired | `Edm.Boolean` |
| DefaultValue | `Edm.String?` |
| Guid | `Edm.String` |
| MimosaAttribute | `Edm.String?` |
| IsMultiSelect | `Edm.Boolean` |

- `GET /odata/Fields` — Get the Fields
- `GET /odata/Fields/$count` — Get the Fields

OData query examples:
  - `GET https://wvdot-it-api.bentley.com/odata/Fields`
  - `GET https://wvdot-it-api.bentley.com/odata/Fields?$top=10`
  - `GET https://wvdot-it-api.bentley.com/odata/Fields?$top=10&$select=Id,Name`
  - `GET https://wvdot-it-api.bentley.com/odata/Fields?$filter=IsDeleted eq false`
  - `GET https://wvdot-it-api.bentley.com/odata/Fields?$orderby=Id desc&$top=50`
  - `GET https://wvdot-it-api.bentley.com/odata/Fields/$count`

### `ReportElements`
_EntityType: `ReportElement` — Keys: `ParentSubAssetId, ReportId, SubAssetId, UserId`._

| Property | EDM type |
|---|---|
| ReportId | `Edm.Int32` |
| ParentSubAssetId | `Edm.Int32` |
| SubAssetId | `Edm.Int32` |
| UserId | `Edm.Int32` |
| AssetId | `Edm.Int32` |
| AssetName | `Edm.String` |
| AssetTypeId | `Edm.Int32` |
| ReportTypeId | `Edm.Int32?` |
| ReportType | `Edm.String?` |
| ParentElementId | `Edm.Int32?` |
| ParentElementName | `Edm.String?` |
| ParentEnvironmentId | `Edm.Int32?` |
| ElementId | `Edm.Int32` |
| ElementName | `Edm.String` |
| ElementType | `Bentley.InspectTech.ORM.Models.StructElementType` |
| ElementSubmissionType | `Bentley.InspectTech.ORM.Models.StructElementSubmissionType` |
| Classification | `Bentley.InspectTech.ORM.Models.StructElementClass` |
| ElementEnvironmentId | `Edm.Int32` |
| Unit | `Edm.String?` |
| TotalQuantity | `Edm.Int32?` |
| State1 | `Edm.Int32?` |
| State2 | `Edm.Int32?` |
| State3 | `Edm.Int32?` |
| State4 | `Edm.Int32?` |
| State5 | `Edm.Int32?` |

- `GET /odata/ReportElements` — Get the Report Elements
- `GET /odata/ReportElements/$count` — Get the Report Elements

OData query examples:
  - `GET https://wvdot-it-api.bentley.com/odata/ReportElements`
  - `GET https://wvdot-it-api.bentley.com/odata/ReportElements?$top=10`
  - `GET https://wvdot-it-api.bentley.com/odata/ReportElements?$top=10&$select=Id,Name`
  - `GET https://wvdot-it-api.bentley.com/odata/ReportElements?$filter=IsDeleted eq false`
  - `GET https://wvdot-it-api.bentley.com/odata/ReportElements?$orderby=Id desc&$top=50`
  - `GET https://wvdot-it-api.bentley.com/odata/ReportElements/$count`

### `ReportValues`
_EntityType: `ReportValue` — Keys: `FieldId, Id, UserId`._

| Property | EDM type |
|---|---|
| Id | `Edm.Int32` |
| FieldId | `Edm.Int32` |
| UserId | `Edm.Int32` |
| AssetId | `Edm.Int32` |
| AssetName | `Edm.String` |
| ReportTypeId | `Edm.Int32` |
| ReportTypeName | `Edm.String` |
| IsPrePupulated | `Edm.Boolean` |
| FieldName | `Edm.String` |
| FieldDataType | `Bentley.InspectTech.ORM.Models.FieldDataType` |
| Value | `Edm.String` |
| PlainText | `Edm.String?` |
| UpdatedByUserId | `Edm.Int32?` |
| UpdatedByUser | `Edm.String?` |
| LastUpdatedDate | `Edm.DateTimeOffset?` |
| ChangeLocation | `Edm.String?` |

- `GET /odata/ReportValues` — Get the Report Values
- `GET /odata/ReportValues/$count` — Get the Report Values

OData query examples:
  - `GET https://wvdot-it-api.bentley.com/odata/ReportValues`
  - `GET https://wvdot-it-api.bentley.com/odata/ReportValues?$top=10`
  - `GET https://wvdot-it-api.bentley.com/odata/ReportValues?$top=10&$select=Id,Name`
  - `GET https://wvdot-it-api.bentley.com/odata/ReportValues?$filter=IsDeleted eq false`
  - `GET https://wvdot-it-api.bentley.com/odata/ReportValues?$orderby=Id desc&$top=50`
  - `GET https://wvdot-it-api.bentley.com/odata/ReportValues/$count`


## OData service document & metadata

- `GET /odata` — odata/
- `GET /odata/$metadata` — odata/$metadata

## REST controllers (`/api/<controller>` and `/mobile/<controller>`)

### `ActivityType`  (5 GET endpoints)
- `GET /{apiType}/ActivityType` — Retrieves all ActivityTypes available in the system.
    - required params: `apiType` (path)
- `GET /{apiType}/ActivityType/GetByTdId/{td_id}` — Retrieves all ActivityTypes associated with a specific TaskDefinition.
    - required params: `td_id` (path), `apiType` (path)
- `GET /{apiType}/ActivityType/GetName/{act_id}` — Retrieves only the name of a specific ActivityType by its ID.
    - required params: `act_id` (path), `apiType` (path)
- `GET /{apiType}/ActivityType/{act_guid}` — Retrieves a specific ActivityType by its unique GUID identifier.
    - required params: `act_guid` (path), `apiType` (path)
- `GET /{apiType}/ActivityType/{act_id}` — Retrieves a specific ActivityType by its numeric ID.
    - required params: `act_id` (path), `apiType` (path)

### `AdvancedCalculationScript`  (2 GET endpoints)
- `GET /{apiType}/AdvancedCalculationScript/GetByFeId/{fe_id}` — Retrieves an Advanced Calculation Script associated with a specific form element (field).
    - required params: `fe_id` (path), `apiType` (path)
- `GET /{apiType}/AdvancedCalculationScript/GetByTmId/{tm_id}` — Retrieves an Advanced Calculation Script associated with a specific data type member.
    - required params: `tm_id` (path), `apiType` (path)

### `AdvancedScriptAffectedFields`  (2 GET endpoints)
- `GET /{apiType}/AdvancedScriptAffectedFields/GetByAdsId/{ads_id}` — Retrieves all fields affected by a specific Advanced Calculation Script.
    - required params: `ads_id` (path), `apiType` (path)
- `GET /{apiType}/AdvancedScriptAffectedFields/GetById/{asaf_id}` — Retrieves a specific affected field mapping by its unique ID.
    - required params: `asaf_id` (path), `apiType` (path)

### `Asset`  (11 GET endpoints)
- `GET /{apiType}/Asset` — Retrieves all assets accessible to the current user with default paging.
    - required params: `apiType` (path)
- `GET /{apiType}/Asset/GetAssetByAsCode/{as_code}` — Retrieves a specific asset by its asset code.
    - required params: `as_code` (path), `apiType` (path)
- `GET /{apiType}/Asset/GetAssetByGuid/{as_guid}` — Retrieves a specific asset by its globally unique identifier (GUID).
    - required params: `as_guid` (path), `apiType` (path)
- `GET /{apiType}/Asset/GetAssetById/{as_id}` — Retrieves a specific asset by its integer ID.
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/Asset/GetAssetByName/{as_name}` — Searches for assets by name with exact or partial matching.
    - required params: `as_name` (path), `apiType` (path)
- `GET /{apiType}/Asset/GetAssets` — Retrieves all assets accessible to the current user with default paging.
    - required params: `apiType` (path)
- `GET /{apiType}/Asset/GetCoordinates/{as_id}` — Retrieves the geographic coordinates (latitude/longitude) for a specific asset.
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/Asset/GetMaxWorkingSetAssetCount` — Retrieves the system-configured maximum number of assets a user can have in their working set.
    - required params: `apiType` (path)
- `GET /{apiType}/Asset/GetNonDeletedReportCount/{as_id}` — Retrieves the count of non-deleted reports associated with a specific asset.
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/Asset/{as_guid}` — Retrieves a specific asset by its globally unique identifier (GUID).
    - required params: `as_guid` (path), `apiType` (path)
- `GET /{apiType}/Asset/{as_id}` — Retrieves a specific asset by its integer ID.
    - required params: `as_id` (path), `apiType` (path)

### `AssetActivityTypeSchedule`  (10 GET endpoints)
- `GET /{apiType}/AssetActivityTypeSchedule/CalculateNextDate/{as_sch_freq_unit}/{as_sch_freq_length}/{date_from}` — Calculates the next due date by adding a frequency interval to a starting date.
    - required params: `as_sch_freq_unit` (path), `as_sch_freq_length` (path), `date_from` (path), `apiType` (path)
- `GET /{apiType}/AssetActivityTypeSchedule/Get/{as_id}/{act_id}/{sch_id}`
    - required params: `as_id` (path), `act_id` (path), `apiType` (path)
- `GET /{apiType}/AssetActivityTypeSchedule/GetActivities/{sch_id}/{act_id}/{as_id}` — Retrieves multiple activity schedules filtered by schedule, asset, and/or activity type.
    - required params: `sch_id` (path), `apiType` (path)
- `GET /{apiType}/AssetActivityTypeSchedule/GetLastApprovedMaintenanceDate/{as_id}/{td_id}` — Retrieves the date of the last approved maintenance/inspection for an asset and maintenance type.
    - required params: `as_id` (path), `td_id` (path), `apiType` (path)
- `GET /{apiType}/AssetActivityTypeSchedule/GetOpenActivities/{sch_id}/{act_id}` — Retrieves all open (not completed and not deleted) activities for a schedule.
    - required params: `sch_id` (path), `apiType` (path)
- `GET /{apiType}/AssetActivityTypeSchedule/GetRecurringMaintenance/{as_id}` — Retrieves all currently active recurring maintenance schedules for an asset (excludes ad-hoc).
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/AssetActivityTypeSchedule/GetRecurringMaintenance/{as_id}/{sch_id}/{td_id}` — Retrieves a specific open recurring maintenance schedule by asset, schedule, and task definition.
    - required params: `as_id` (path), `sch_id` (path), `td_id` (path), `apiType` (path)
- `GET /{apiType}/AssetActivityTypeSchedule/GetScheduledMaintenanceByAssetTask/{ast_id}/{td_id}` — Retrieves the currently scheduled (non-complete) maintenance for a specific asset task and inspection type.
    - required params: `ast_id` (path), `td_id` (path), `apiType` (path)
- `GET /{apiType}/AssetActivityTypeSchedule/GetScheduledMaintenanceByWorkflowEvent` — Gets a list of scheduled maintenance by the Workflow Event passed (Workflow Name / Stage / Action).
    - required params: `apiType` (path)
- `GET /{apiType}/AssetActivityTypeSchedule/GetScheduledMaintenances/{as_id}` — Retrieves all currently scheduled maintenances for an asset, including ad-hoc inspections.
    - required params: `as_id` (path), `apiType` (path)

### `AssetDataExtractUserLog`  (2 GET endpoints)
- `GET /{apiType}/AssetDataExtractUserLog/DownloadFile/{file_guid}` — Downloads the generated data extract file from Azure Blob Storage or local file system.
    - required params: `file_guid` (path), `apiType` (path)
- `GET /{apiType}/AssetDataExtractUserLog/GetCurrentUserAssetExtractLogs` — Retrieves the current user's data extraction job history with status and file information.
    - required params: `apiType` (path)

### `AssetDetailField`  (5 GET endpoints)
- `GET /{apiType}/AssetDetailField/Get/{at_id}/{adf_id}` — Retrieves a specific asset detail field definition by asset type and field ID.
    - required params: `at_id` (path), `adf_id` (path), `apiType` (path)
- `GET /{apiType}/AssetDetailField/GetDisplayFields/{as_id}` — Retrieves the display fields shown on the Asset Details (BridgeDetails) page with custom logic for computed values.
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/AssetDetailField/GetFieldsByAsGuid/{as_guid}` — Retrieves all detail fields for a specific asset by its GUID.
    - required params: `as_guid` (path), `apiType` (path)
- `GET /{apiType}/AssetDetailField/GetFieldsByAsId/{as_id}` — Retrieves all detail fields for a specific asset by its ID.
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/AssetDetailField/GetFieldsByAtId/{at_id}` — Retrieves all detail field definitions configured for a specific asset type.
    - required params: `at_id` (path), `apiType` (path)

### `AssetDetailFieldDetail`  (2 GET endpoints)
- `GET /{apiType}/AssetDetailFieldDetail/Get/{adf_id}` — Retrieves all detail metadata records for a specific Asset Detail Field.
    - required params: `adf_id` (path), `apiType` (path)
- `GET /{apiType}/AssetDetailFieldDetail/{adf_id}` — Retrieves all detail metadata records for a specific Asset Detail Field.
    - required params: `adf_id` (path), `apiType` (path)

### `AssetDetailMaintenanceField`  (3 GET endpoints)
- `GET /{apiType}/AssetDetailMaintenanceField/GetAssetDetailMaintenanceRecordsForListBox` — Retrieves maintenance field definitions for display in selection UI, including system metadata fields.
    - required params: `apiType` (path)
- `GET /{apiType}/AssetDetailMaintenanceField/GetByTdId` — Retrieves all maintenance field definitions configured for a specific Task Definition.
    - required params: `apiType` (path)
- `GET /{apiType}/AssetDetailMaintenanceField/GetMaintenanceFieldRecords` — Get asset detail maintenance field records for a task definition
    - required params: `apiType` (path)

### `AssetFile`  (19 GET endpoints)
- `GET /{apiType}/AssetFile/Download/{af_id}`
    - required params: `af_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFile/Download/{af_id}/{get_as_thumbnail}`
    - required params: `af_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFile/DownloadAssetFileMap/{as_id}`
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFile/GetAssetCoverImage/{as_guid}` — Downloads the cover image file for an asset identified by GUID.
    - required params: `as_guid` (path), `apiType` (path)
- `GET /{apiType}/AssetFile/GetAssetCoverImage/{as_id}` — Downloads the cover image file for an asset identified by ID.
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFile/GetAssetFileFieldMap/{af_id}` — Retrieves field mappings for a specific asset file.
    - required params: `af_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFile/GetAssetFileMap/{as_id}` — Retrieves the asset file ID designated as the asset's map image.
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFile/GetAssetFilesInstanceMap/{ast_id}` — Retrieves asset files mapped to data type instances on a specific report.
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFile/GetAssetFilesInstanceSubAssetMap/{ast_id}` — Retrieves asset files mapped to sub-asset instances on a specific report.
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFile/GetByAssetAfGuid/{af_guid}/{include_binary}/{include_file_type}/{include_asset_file_categories}` — Retrieves a specific asset file by its GUID.
    - required params: `af_guid` (path), `include_binary` (path), `include_file_type` (path), `include_asset_file_categories` (path), `apiType` (path)
- `GET /{apiType}/AssetFile/GetByAssetAfId/{af_id}/{include_binary}/{include_file_type}/{include_asset_file_categories}` — Retrieves a specific asset file by its ID.
    - required params: `af_id` (path), `include_binary` (path), `include_file_type` (path), `include_asset_file_categories` (path), `apiType` (path)
- `GET /{apiType}/AssetFile/GetByAssetId/{as_id}` — Retrieves all files attached to a specific asset.
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFile/GetByAssetId/{as_id}/{include_binary}` — Retrieves all files attached to a specific asset.
    - required params: `as_id` (path), `apiType` (path), `include_binary` (path)
- `GET /{apiType}/AssetFile/IsCover/{af_id}/{af_cover}/{objectType}/{as_id}` — Checks if a file is designated as the cover image.
    - required params: `af_id` (path), `af_cover` (path), `objectType` (path), `as_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFile/IsCover/{af_id}/{af_cover}/{objectType}/{as_id}/{ast_id}` — Checks if a file is designated as the cover image.
    - required params: `af_id` (path), `af_cover` (path), `objectType` (path), `as_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFile/IsPrinted/{af_id}/{af_cover}/{objectType}/{as_id}` — Checks if a file is marked for inclusion in printed reports.
    - required params: `af_id` (path), `af_cover` (path), `objectType` (path), `as_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFile/IsPrinted/{af_id}/{af_cover}/{objectType}/{as_id}/{ast_id}` — Checks if a file is marked for inclusion in printed reports.
    - required params: `af_id` (path), `af_cover` (path), `objectType` (path), `as_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFile/{af_guid}/{include_binary}/{include_file_type}/{include_asset_file_categories}` — Retrieves a specific asset file by its GUID.
    - required params: `af_guid` (path), `include_binary` (path), `include_file_type` (path), `include_asset_file_categories` (path), `apiType` (path)
- `GET /{apiType}/AssetFile/{af_id}/{include_binary}/{include_file_type}/{include_asset_file_categories}` — Retrieves a specific asset file by its ID.
    - required params: `af_id` (path), `include_binary` (path), `include_file_type` (path), `include_asset_file_categories` (path), `apiType` (path)

### `AssetFileCategory`  (2 GET endpoints)
- `GET /{apiType}/AssetFileCategory` — Retrieves all file categories for a specific category type.
    - required params: `apiType` (path)
- `GET /{apiType}/AssetFileCategory/GetAssetFileCategoriesForFileType/{ft_id}` — Retrieves all file categories mapped to a specific file type.
    - required params: `ft_id` (path), `apiType` (path)

### `AssetFilesFieldMap`  (5 GET endpoints)
- `GET /{apiType}/AssetFilesFieldMap/GetAllByAfId/{af_id}` — Retrieves all field mappings for a specific file.
    - required params: `af_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFilesFieldMap/GetAssetFilesFieldMaps/{ast_id}/{fe_id}` — Retrieves all files mapped to a specific field on a specific report.
    - required params: `ast_id` (path), `fe_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFilesFieldMap/GetAssetFilesFieldMaps/{ast_id}/{fe_id}/{af_id}` — Retrieves a specific file-to-field mapping by report, field, and file IDs.
    - required params: `ast_id` (path), `fe_id` (path), `af_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFilesFieldMap/GetAssetFilesFieldMapsByAfIdAndReport/{af_id}/{ast_id}` — Retrieves all field mappings for a specific file on a specific report.
    - required params: `af_id` (path), `ast_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFilesFieldMap/{affm_guid}` — Retrieves a single file-to-field mapping by its GUID.
    - required params: `affm_guid` (path), `apiType` (path)

### `AssetFilesInstanceMap`  (2 GET endpoints)
- `GET /{apiType}/AssetFilesInstanceMap/GetAssetFilesInstanceMaps/{ast_id}` — Retrieves all file-to-instance mappings for a specific report.
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFilesInstanceMap/GetAssetFilesInstanceSubAssetMaps/{ast_id}` — Retrieves all file-to-instance mappings for sub-assets on a specific report.
    - required params: `ast_id` (path), `apiType` (path)

### `AssetFilesReportMap`  (9 GET endpoints)
- `GET /{apiType}/AssetFilesReportMap/GetAssetFilesForAsset/{as_id}`
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFilesReportMap/GetAssetFilesReportMap/{af_id}` — Get files mapped to a report that are also mapped to a summary report
    - required params: `af_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFilesReportMap/GetAssetFilesReportMap/{af_id}/{object_id}/{object_type}` — Get files mapped to a report that are also mapped to a summary report
    - required params: `af_id` (path), `object_id` (path), `object_type` (path), `apiType` (path)
- `GET /{apiType}/AssetFilesReportMap/GetAssetFilesReportMapByAssetID/{as_id}/{af_id}` — Get files mapped to a report that are also mapped to a summary report
    - required params: `as_id` (path), `af_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFilesReportMap/GetAssetFilesReportMaps/{af_id}/{ast_id}` — Get files mapped to a report that are also mapped to a summary report
    - required params: `af_id` (path), `ast_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFilesReportMap/GetMapsForReportByAstId/{ast_id}`
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFilesReportMap/GetMapsForReportByAstIdAndFtId/{ast_id}/{ft_id}` — Get GetMapsForReport by ast_id and ft_id
    - required params: `ast_id` (path), `ft_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFilesReportMap/GetMapsForReportForSubAsset/{ast_id}/{sub_as_id}` — Get a list of asset file map records mapped to a report for a specific subasset
    - required params: `ast_id` (path), `sub_as_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFilesReportMap/GetMapsForReportMappedToSummary/{child_ast_id}/{summary_ast_guid}` — Get files mapped to a report that are also mapped to a summary report
    - required params: `child_ast_id` (path), `summary_ast_guid` (path), `apiType` (path)

### `AssetFilesWorkflowMap`  (3 GET endpoints)
- `GET /{apiType}/AssetFilesWorkflowMap/GetAssetFileWorkflowMap/{ast_id}/{af_id}/{wfs_id}` — Retrieves the workflow mapping for a specific file on a report.
    - required params: `ast_id` (path), `af_id` (path), `wfs_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFilesWorkflowMap/GetAssetFilesWorkflowMapByAfId/{af_id}` — Retrieves all report-workflow mappings for a specific file.
    - required params: `af_id` (path), `apiType` (path)
- `GET /{apiType}/AssetFilesWorkflowMap/GetAssetFilesWorkflowMapByAstId/{ast_id}` — Retrieves all file-to-workflow stage mappings for a specific report.
    - required params: `ast_id` (path), `apiType` (path)

### `AssetInspectionTypeSchedule`  (4 GET endpoints)
- `GET /{apiType}/AssetInspectionTypeSchedule/GetAssetInspectionTypeScheduleById/{as_id}/{it_id}/{sch_id}` — Retrieves a specific recurring inspection schedule by asset, inspection type, and schedule ID.
    - required params: `as_id` (path), `it_id` (path), `sch_id` (path), `apiType` (path)
- `GET /{apiType}/AssetInspectionTypeSchedule/GetAssetScheduledInspectionTypes/{as_id}` — Retrieves a list of all inspection type IDs that have scheduled inspections configured for an asset.
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/AssetInspectionTypeSchedule/UsesScheduleFrequency/{as_id}/{it_id}` — Checks whether the system and asset use schedule frequency options for a specific inspection type.
    - required params: `as_id` (path), `it_id` (path), `apiType` (path)
- `GET /{apiType}/AssetInspectionTypeSchedule/{as_id}/{it_id}/{sch_id}` — Retrieves a specific recurring inspection schedule by asset, inspection type, and schedule ID.
    - required params: `as_id` (path), `it_id` (path), `sch_id` (path), `apiType` (path)

### `AssetMaintenanceItemSummary`  (1 GET endpoints)
- `GET /{apiType}/AssetMaintenanceItemSummary/{as_id}/{description_fe_id}/{includeCompleted}` — Retrieves paginated maintenance item summaries for a specific asset.
    - required params: `as_id` (path), `description_fe_id` (path), `includeCompleted` (path), `apiType` (path)

### `AssetSegmentMap`  (1 GET endpoints)
- `GET /{apiType}/AssetSegmentMap/Get/{objectType}/{objectId}` — Retrieves all segments (child assets) mapped to a parent asset or report.
    - required params: `objectType` (path), `objectId` (path), `apiType` (path)

### `AssetStatus`  (5 GET endpoints)
- `GET /{apiType}/AssetStatus` — Retrieves all Asset Status definitions available in the system.
    - required params: `apiType` (path)
- `GET /{apiType}/AssetStatus/GetAssetStatusByGuid/{AssetStatusGuid}` — Retrieves a specific Asset Status by its unique GUID identifier.
    - required params: `AssetStatusGuid` (path), `apiType` (path)
- `GET /{apiType}/AssetStatus/GetAssetStatusById/{asset_status_id}` — Retrieves a specific Asset Status by its numeric ID.
    - required params: `asset_status_id` (path), `apiType` (path)
- `GET /{apiType}/AssetStatus/{AssetStatusGuid}` — Retrieves a specific Asset Status by its unique GUID identifier.
    - required params: `AssetStatusGuid` (path), `apiType` (path)
- `GET /{apiType}/AssetStatus/{asset_status_id}` — Retrieves a specific Asset Status by its numeric ID.
    - required params: `asset_status_id` (path), `apiType` (path)

### `AssetTask`  (13 GET endpoints)
- `GET /{apiType}/AssetTask/CanCreateReport` — Checks whether the specified inspector has permission to create inspection reports for an asset.
    - required params: `apiType` (path)
- `GET /{apiType}/AssetTask/GetAssetTaskByAsId/{as_id}` — Get AssetTask by as_id
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/AssetTask/GetAssetTaskByGuid/{ast_guid}` — Get AssetTask by ast_guid
    - required params: `ast_guid` (path), `apiType` (path)
- `GET /{apiType}/AssetTask/GetAssetTaskById/{ast_id}` — Retrieves a single inspection report or maintenance item by its unique identifier.
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/AssetTask/GetAssetTaskByWorkflowStageIdAndTaskDefinitionId/{wfs_id}/{td_id}`
    - required params: `wfs_id` (path), `td_id` (path), `apiType` (path)
- `GET /{apiType}/AssetTask/GetAssetTaskCountByTaskDefinition/{td_id}`
    - required params: `td_id` (path), `apiType` (path)
- `GET /{apiType}/AssetTask/GetAssetTaskSubAssetIds/{ast_id}` — Retrieves the list of sub-asset identifiers associated with an inspection report.
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/AssetTask/GetCountByTaskDefinition` — Gets the count of inspection reports and maintenance items for a specific task definition (alternate endpoint).
    - required params: `apiType` (path)
- `GET /{apiType}/AssetTask/GetMaintenanceItemById/{ast_id}` — Retrieves a single inspection report or maintenance item by its unique identifier.
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/AssetTask/GetMaintenanceItemByReportGuid/{ast_guid}` — Get AssetTask by ast_guid
    - required params: `ast_guid` (path), `apiType` (path)
- `GET /{apiType}/AssetTask/{ast_guid}` — Get AssetTask by ast_guid
    - required params: `ast_guid` (path), `apiType` (path)
- `GET /{apiType}/AssetTask/{ast_id}` — Retrieves a single inspection report or maintenance item by its unique identifier.
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/AssetTask/{wfs_id}/{td_id}`
    - required params: `wfs_id` (path), `td_id` (path), `apiType` (path)

### `AssetTree`  (3 GET endpoints)
- `GET /{apiType}/AssetTree` — Retrieves the asset tree without pagination (defaults to first page).
    - required params: `apiType` (path)
- `GET /{apiType}/AssetTree/GetMobileAssetTree` — Retrieves a mobile-optimized version of the asset tree for field use.
    - required params: `apiType` (path)
- `GET /{apiType}/AssetTree/GetMobileRootAssets` — Retrieves IDs of root-level assets in the asset tree for mobile navigation.
    - required params: `apiType` (path)

### `AssetType`  (5 GET endpoints)
- `GET /{apiType}/AssetType` — Retrieves all Asset Type definitions available in the system.
    - required params: `apiType` (path)
- `GET /{apiType}/AssetType/GetWithHealthIndex` — Retrieves all Asset Types that have Health Index calculations configured.
    - required params: `apiType` (path)
- `GET /{apiType}/AssetType/{at_guid}` — Retrieves a specific Asset Type by its unique GUID identifier.
    - required params: `at_guid` (path), `apiType` (path)
- `GET /{apiType}/AssetType/{at_id}` — Retrieves a specific Asset Type by its numeric ID.
    - required params: `at_id` (path), `apiType` (path)
- `GET /{apiType}/AssetType/{at_name}` — Retrieves a specific Asset Type by its name.
    - required params: `at_name` (path), `apiType` (path)

### `AssetTypeRoleMap`  (5 GET endpoints)
- `GET /{apiType}/AssetTypeRoleMap/GetAllAssetTypes/{rl_id}` — Retrieves all asset type mappings for a specific role.
    - required params: `rl_id` (path), `apiType` (path)
- `GET /{apiType}/AssetTypeRoleMap/GetAssetTypeAccessLevelsByUser/{at_id}` — Retrieves all role mappings for a specific asset type that apply to the current authenticated user.
    - required params: `at_id` (path), `apiType` (path)
- `GET /{apiType}/AssetTypeRoleMap/GetAssetTypeAccessLevelsByUser/{at_id}/{in_id}` — Retrieves all role mappings for a specific asset type that apply to a specified user.
    - required params: `in_id` (path), `at_id` (path), `apiType` (path)
- `GET /{apiType}/AssetTypeRoleMap/GetAssetViewAssetTypeAccessLevelByUser/{as_id}` — Retrieves all role mappings for an Asset View that apply to the current authenticated user.
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/AssetTypeRoleMap/GetAssetViewAssetTypeAccessLevelByUser/{as_id}/{in_id}` — Retrieves all role mappings for an Asset View that apply to a specified user.
    - required params: `in_id` (path), `as_id` (path), `apiType` (path)

### `CurrentValue`  (8 GET endpoints)
- `GET /{apiType}/CurrentValue/GetAllCurrentValues` — Retrieves all current values for all assets the user can view.
    - required params: `apiType` (path)
- `GET /{apiType}/CurrentValue/GetCurrentValueByGuid/{currentValueGuid}` — Retrieves a current value by its unique GUID identifier.
    - required params: `currentValueGuid` (path), `apiType` (path)
- `GET /{apiType}/CurrentValue/GetCurrentValueById/{as_id}/{fe_id}` — Retrieves the current value for a specific field on a specific asset.
    - required params: `as_id` (path), `fe_id` (path), `apiType` (path)
- `GET /{apiType}/CurrentValue/GetCurrentValuesByAssetId/{as_id}` — Retrieves all current values for a specific asset.
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/CurrentValue/GetCurrentValuesForFieldChoices`
    - required params: `apiType` (path)
- `GET /{apiType}/CurrentValue/{as_id}` — Retrieves all current values for a specific asset.
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/CurrentValue/{as_id}/{fe_id}` — Retrieves the current value for a specific field on a specific asset.
    - required params: `as_id` (path), `fe_id` (path), `apiType` (path)
- `GET /{apiType}/CurrentValue/{currentValueGuid}` — Retrieves a current value by its unique GUID identifier.
    - required params: `currentValueGuid` (path), `apiType` (path)

### `DataExtractor`  (4 GET endpoints)
- `GET /{apiType}/DataExtractor/GetDataExtractorModels` — Gets data extractor templates by type
    - required params: `apiType` (path)
- `GET /{apiType}/DataExtractor/GetFieldData` — Gets a list of fields mapped to inspection type
    - required params: `apiType` (path)
- `GET /{apiType}/DataExtractor/GetInspTypeModels` — Gets a list of inspection types
    - required params: `apiType` (path)
- `GET /{apiType}/DataExtractor/GetRfgData` — Gets a list of fields mapped to a repeating field group
    - required params: `apiType` (path)

### `DataType`  (8 GET endpoints)
- `GET /{apiType}/DataType/GetAllDataTypes` — Retrieves all Data Type (RFG) definitions configured in the system.
    - required params: `apiType` (path)
- `GET /{apiType}/DataType/GetAllInstanceMemberValues`
    - required params: `apiType` (path)
- `GET /{apiType}/DataType/GetDataType/{dt_id}` — Retrieves a specific Data Type definition by ID with full configuration details.
    - required params: `dt_id` (path), `apiType` (path)
- `GET /{apiType}/DataType/GetDataTypeDisplayPropMaps/{dt_id}` — Retrieves all display property mappings for a Data Type.
    - required params: `dt_id` (path), `apiType` (path)
- `GET /{apiType}/DataType/GetDataTypeDisplayProperties/{dt_id}` — Retrieves all display properties and their mappings for a Data Type.
    - required params: `dt_id` (path), `apiType` (path)
- `GET /{apiType}/DataType/GetDataTypeValuesByObjectIdAndObjectType/{objectType}/{objectId}/{dt_id}/{instanceCount}` — Retrieves the complete Data Type structure with instance data, member data, and values for a specific object.
    - required params: `objectType` (path), `objectId` (path), `dt_id` (path), `instanceCount` (path), `apiType` (path)
- `GET /{apiType}/DataType/GetDataTypes` — Retrieves a list of all Data Type definitions with configuration details.
    - required params: `apiType` (path)
- `GET /{apiType}/DataType/GetMobileRFG` — Retrieves Data Types that are mapped to mobile forms with their associated form definitions.
    - required params: `apiType` (path)

### `DataTypeInstance`  (2 GET endpoints)
- `GET /{apiType}/DataTypeInstance/GetDataTypeInstances/{dt_id}` — Get list of DataTypeInstance by DataType Id.
    - required params: `dt_id` (path), `apiType` (path)
- `GET /{apiType}/DataTypeInstance/GetDataTypeInstances/{dt_key}` — Retrieves all instances for a Repeatable Field Group identified by its unique key.
    - required params: `dt_key` (path), `apiType` (path)

### `DataTypeInstanceMember`  (3 GET endpoints)
- `GET /{apiType}/DataTypeInstanceMember/GetByDataTypeInstanceFieldMap/{ti_id}` — Retrieves all instance members for a specific data type instance, filtered by field mappings.
    - required params: `ti_id` (path), `apiType` (path)
- `GET /{apiType}/DataTypeInstanceMember/GetByMemberAndInstance/{tm_id}/{ti_id}` — Retrieves a specific data type instance member by member ID and instance ID.
    - required params: `tm_id` (path), `ti_id` (path), `apiType` (path)
- `GET /{apiType}/DataTypeInstanceMember/GetDataTypeInstanceMembersByDataType/{dt_id}` — Retrieves all instance members for a specific data type (RFG) across all instances.
    - required params: `dt_id` (path), `apiType` (path)

### `DataTypeMember`  (4 GET endpoints)
- `GET /{apiType}/DataTypeMember/GetDataTypeMember/{tm_id}` — Retrieves a specific data type member by its ID.
    - required params: `tm_id` (path), `apiType` (path)
- `GET /{apiType}/DataTypeMember/GetDataTypeMembers/{dt_id}` — Retrieves all data type members for a specific data type (RFG).
    - required params: `dt_id` (path), `apiType` (path)
- `GET /{apiType}/DataTypeMember/GetDataTypeMembers/{dt_id}/{tm_name}` — Retrieves data type members by data type ID and member name.
    - required params: `dt_id` (path), `tm_name` (path), `apiType` (path)
- `GET /{apiType}/DataTypeMember/GetRoleDataTypeMemberSecurity/{tm_id}` — Retrieves role-based security settings for a specific data type member.
    - required params: `tm_id` (path), `apiType` (path)

### `DefaultSection`  (1 GET endpoints)
- `GET /{apiType}/DefaultSection/GetAll` — Retrieves all available default report sections.
    - required params: `apiType` (path)

### `ElementDef`  (11 GET endpoints)
- `GET /{apiType}/ElementDef/GetChildElementCount/{parent_sub_as_id}` — Retrieves the count of child elements for a parent sub-asset.
    - required params: `parent_sub_as_id` (path), `apiType` (path)
- `GET /{apiType}/ElementDef/GetChildElements/{parent_sub_as_id}` — Retrieves child elements that match a parent sub-asset's environment and structure unit.
    - required params: `parent_sub_as_id` (path), `apiType` (path)
- `GET /{apiType}/ElementDef/GetChildElementsByGroup/{eg_id}/{parent_sub_as_id}/{at_id}` — Retrieves child elements filtered by element group, parent sub-asset, and asset type.
    - required params: `eg_id` (path), `parent_sub_as_id` (path), `at_id` (path), `apiType` (path)
- `GET /{apiType}/ElementDef/GetElementCount` — Retrieves the total count of element definitions available to the user's profile.
    - required params: `apiType` (path)
- `GET /{apiType}/ElementDef/GetElementDefFields` — Retrieves all field definitions used by element definitions.
    - required params: `apiType` (path)
- `GET /{apiType}/ElementDef/GetElementForAsset/{ed_id}/{reportable_as_id}` — Finds the sub-asset ID of an element that matches specific criteria under a reportable asset.
    - required params: `ed_id` (path), `reportable_as_id` (path), `apiType` (path)
- `GET /{apiType}/ElementDef/GetElementForAsset/{sub_as_id}` — Retrieves the element definition for a specific sub-asset element.
    - required params: `sub_as_id` (path), `apiType` (path)
- `GET /{apiType}/ElementDef/GetElementsByGroup/{eg_id}` — Retrieves all elements within a specific element group.
    - required params: `eg_id` (path), `apiType` (path)
- `GET /{apiType}/ElementDef/GetParentElementCount/{at_id}` — Retrieves the count of parent elements for a specific asset type.
    - required params: `at_id` (path), `apiType` (path)
- `GET /{apiType}/ElementDef/GetParentElements/{at_id}` — Retrieves all parent elements for a specific asset type.
    - required params: `at_id` (path), `apiType` (path)
- `GET /{apiType}/ElementDef/GetParentElementsByGroup/{eg_id}/{at_id}` — Retrieves parent elements within a specific group for a given asset type.
    - required params: `eg_id` (path), `at_id` (path), `apiType` (path)

### `ElementEnvironments`  (6 GET endpoints)
- `GET /{apiType}/ElementEnvironments` — Retrieves all element environment definitions.
    - required params: `apiType` (path)
- `GET /{apiType}/ElementEnvironments/GetDefaultEnvironmentForAnElement/{ed_id}` — Retrieves the default environment for a specific element definition.
    - required params: `ed_id` (path), `apiType` (path)
- `GET /{apiType}/ElementEnvironments/GetEnvironmentList/{ede_list_id}` — Retrieves element environments for a specific environment list.
    - required params: `ede_list_id` (path), `apiType` (path)
- `GET /{apiType}/ElementEnvironments/GetEnvironmentUsedCount/{ede_list_id}/{ede_id}` — Retrieves the usage count for a specific element environment.
    - required params: `ede_list_id` (path), `ede_id` (path), `apiType` (path)
- `GET /{apiType}/ElementEnvironments/GetEnvironmentsForAnElement/{ed_id}` — Retrieves all environments applicable to a specific element definition.
    - required params: `ed_id` (path), `apiType` (path)
- `GET /{apiType}/ElementEnvironments/GetEnvironmentsForSubAssetElement/{sub_as_id}` — Retrieves element environments for a specific sub-asset element.
    - required params: `sub_as_id` (path), `apiType` (path)

### `EnterpriseGuid`  (1 GET endpoints)
- `GET /{apiType}/EnterpriseGuid/GetAll` — Retrieves all registered Enterprise GUIDs.
    - required params: `apiType` (path)

### `Enum`  (1 GET endpoints)
- `GET /{apiType}/Enum/{enumName}` — Retrieves all values for a specific enumeration by name.
    - required params: `enumName` (path), `apiType` (path)

### `ErrorCheckDefinition`  (2 GET endpoints)
- `GET /{apiType}/ErrorCheckDefinition/CopyECD` — Creates a copy of an existing error check definition.
    - required params: `apiType` (path)
- `GET /{apiType}/ErrorCheckDefinition/ExportErrorCheckDefinitions` — Exports all error check definitions to an Excel file.
    - required params: `apiType` (path)

### `ExternalDataView`  (3 GET endpoints)
- `GET /{apiType}/ExternalDataView/ExternalDataViewById/{edv_id}` — Retrieves a specific external data view by its ID.
    - required params: `edv_id` (path), `apiType` (path)
- `GET /{apiType}/ExternalDataView/GetExternalDataViewByForm/{fm_id}` — Retrieves the external data view form mapping for a specific form.
    - required params: `fm_id` (path), `apiType` (path)
- `GET /{apiType}/ExternalDataView/GetExternalDataViews` — Retrieves all external data views with their associated asset type mappings.
    - required params: `apiType` (path)

### `Field`  (10 GET endpoints)
- `GET /{apiType}/Field`
    - required params: `apiType` (path)
- `GET /{apiType}/Field/Get`
    - required params: `apiType` (path)
- `GET /{apiType}/Field/GetFieldByGuid/{fe_guid}` — Retrieves a field definition by its GUID.
    - required params: `fe_guid` (path), `apiType` (path)
- `GET /{apiType}/Field/GetFieldById/{fe_id}` — Retrieves a field definition by its numeric ID.
    - required params: `fe_id` (path), `apiType` (path)
- `GET /{apiType}/Field/GetFieldByName/{fe_name}` — Retrieves field definitions by name.
    - required params: `fe_name` (path), `apiType` (path)
- `GET /{apiType}/Field/GetFormFields/{fm_id}` — Retrieves all fields for a specific form.
    - required params: `fm_id` (path), `apiType` (path)
- `GET /{apiType}/Field/GetMappedMaintFields`
    - required params: `apiType` (path)
- `GET /{apiType}/Field/{fe_guid}` — Retrieves a field definition by its GUID.
    - required params: `fe_guid` (path), `apiType` (path)
- `GET /{apiType}/Field/{fe_id}` — Retrieves a field definition by its numeric ID.
    - required params: `fe_id` (path), `apiType` (path)
- `GET /{apiType}/Field/{fe_name}` — Retrieves field definitions by name.
    - required params: `fe_name` (path), `apiType` (path)

### `FieldChoice`  (8 GET endpoints)
- `GET /{apiType}/FieldChoice/GetCertifiedBridgeInspectorFieldChoices/{feId}/{objectType}/{objectId}` — Retrieves field choices specific to Certified Bridge Inspector (CBI) selection for a given object.
    - required params: `feId` (path), `objectType` (path), `objectId` (path), `apiType` (path)
- `GET /{apiType}/FieldChoice/GetFieldChoiceByFCId/{fc_id}` — Retrieves a single field choice by its unique choice identifier.
    - required params: `fc_id` (path), `apiType` (path)
- `GET /{apiType}/FieldChoice/GetFieldChoiceByFeId/{fe_id}` — Retrieves all field choices for a specific field.
    - required params: `fe_id` (path), `apiType` (path)
- `GET /{apiType}/FieldChoice/GetFieldChoiceByFeIdAndParentFcId/{fe_id}/{parent_fc_id}` — Retrieves child field choices that belong to a specific parent choice (hierarchical/cascading dropdowns).
    - required params: `fe_id` (path), `parent_fc_id` (path), `apiType` (path)
- `GET /{apiType}/FieldChoice/GetFieldChoiceByIdAndValue/{fe_id}/{va_value}` — Retrieves a specific field choice by field ID and choice value.
    - required params: `fe_id` (path), `va_value` (path), `apiType` (path)
- `GET /{apiType}/FieldChoice/GetFieldChoiceNameByCurrentValue/{fe_id}/{as_id}` — Retrieves the display name of a field choice based on the current value stored for an asset.
    - required params: `fe_id` (path), `as_id` (path), `apiType` (path)
- `GET /{apiType}/FieldChoice/{fe_id}` — Retrieves all field choices for a specific field.
    - required params: `fe_id` (path), `apiType` (path)
- `GET /{apiType}/FieldChoice/{fe_id}/{va_value}` — Retrieves a specific field choice by field ID and choice value.
    - required params: `fe_id` (path), `va_value` (path), `apiType` (path)

### `FileType`  (7 GET endpoints)
- `GET /{apiType}/FileType` — Retrieves all file type definitions configured in the system.
    - required params: `apiType` (path)
- `GET /{apiType}/FileType/Get` — Retrieves all file type definitions configured in the system.
    - required params: `apiType` (path)
- `GET /{apiType}/FileType/GetImageFileTypes` — Retrieves file types designated as image file types.
    - required params: `apiType` (path)
- `GET /{apiType}/FileType/GetMapFileTypes` — Retrieves file types designated as map/location image types.
    - required params: `apiType` (path)
- `GET /{apiType}/FileType/GetMobileTypes` — Retrieves file types available for mobile device file uploads.
    - required params: `apiType` (path)
- `GET /{apiType}/FileType/GetRHSFileTypes` — Retrieves file types selectable in the right-hand sidebar file upload interface.
    - required params: `apiType` (path)
- `GET /{apiType}/FileType/GetReportFileTypes` — Retrieves file types designated for inspection reports.
    - required params: `apiType` (path)

### `Form`  (3 GET endpoints)
- `GET /{apiType}/Form` — Retrieves all forms accessible to the current user.
    - required params: `apiType` (path)
- `GET /{apiType}/Form/GetFormById/{fm_id}` — Retrieves a specific form definition by ID.
    - required params: `fm_id` (path), `apiType` (path)
- `GET /{apiType}/Form/IsFormReadOnly/{fm_id}`
    - required params: `fm_id` (path), `apiType` (path)

### `FormElement`  (8 GET endpoints)
- `GET /{apiType}/FormElement/GetDataTypeTemplateDisplaySettings/{tp_id}` — Returns display configuration settings for rendering a Repeatable Field Group template.
    - required params: `tp_id` (path), `apiType` (path)
- `GET /{apiType}/FormElement/GetElementsByForm/{fm_id}` — Retrieves all form elements for a specific form, ordered by parent and element order.
    - required params: `fm_id` (path), `apiType` (path)
- `GET /{apiType}/FormElement/GetElementsByTemplate/{tp_id}` — Retrieves all form elements for a specific RFG template, ordered by parent and element order.
    - required params: `tp_id` (path), `apiType` (path)
- `GET /{apiType}/FormElement/GetErrorCheckResultsForField/{ast_id}/{fe_id}` — Returns error check results for a specific field and all related fields on a report.
    - required params: `ast_id` (path), `fe_id` (path), `apiType` (path)
- `GET /{apiType}/FormElement/GetFieldAndValuesAffectedByField/{objectId}/{objectType}/{fe_id}/{subAsId}` — Returns all fields and their current values that are affected by changes to a specified field.
    - required params: `objectId` (path), `objectType` (path), `fe_id` (path), `apiType` (path)
- `GET /{apiType}/FormElement/GetFormsDesignerElements/{objectId}/{objectType}/{fm_id}` — Returns top-level form elements for the specified form with current values for forms designer.
    - required params: `objectId` (path), `objectType` (path), `fm_id` (path), `apiType` (path)
- `GET /{apiType}/FormElement/GetInspectionTypeElements/{objectId}/{objectType}/{it_id}` — Retrieves form elements configured for a specific inspection type on an asset or report.
    - required params: `objectId` (path), `objectType` (path), `it_id` (path), `apiType` (path)
- `GET /{apiType}/FormElement/GetRfgTemplateElements/{objectId}/{objectType}/{tp_id}` — Returns elements and instance data for a specific Repeatable Field Group template.
    - required params: `objectId` (path), `objectType` (path), `tp_id` (path), `apiType` (path)

### `FormTaskDefinitionMap`  (3 GET endpoints)
- `GET /{apiType}/FormTaskDefinitionMap` — Retrieves all form-to-task-definition mappings for bridge detail tasks.
    - required params: `apiType` (path)
- `GET /{apiType}/FormTaskDefinitionMap/GetMapsForBridgeDetail/{td_id}` — Retrieves all form mappings for a specific bridge detail task definition.
    - required params: `td_id` (path), `apiType` (path)
- `GET /{apiType}/FormTaskDefinitionMap/GetMapsForForm/{fm_id}` — Retrieves all task definition mappings for a specific form.
    - required params: `fm_id` (path), `apiType` (path)

### `GenericImporter`  (1 GET endpoints)
- `GET /{apiType}/GenericImporter/GetAllGenericImportTypes` — Retrieves all available generic import type configurations.
    - required params: `apiType` (path)

### `InspectionReport`  (15 GET endpoints)
- `GET /{apiType}/InspectionReport/Download/{ast_id}` — Downloads an inspection report as a PDF file.
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/InspectionReport/GetAllApproved/{as_id}` — Retrieves all approved inspection reports for an asset.
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/InspectionReport/GetAllApprovedByDateRange/{from}` — Retrieves approved inspection reports within a date range.
    - required params: `from` (path), `apiType` (path)
- `GET /{apiType}/InspectionReport/GetAllApprovedByDateRange/{from}/{to}` — Retrieves approved inspection reports within a date range.
    - required params: `from` (path), `to` (path), `apiType` (path)
- `GET /{apiType}/InspectionReport/GetByAssetTaskGUID/{ast_guid}` — Retrieves an inspection report by asset task GUID.
    - required params: `ast_guid` (path), `apiType` (path)
- `GET /{apiType}/InspectionReport/GetByAssetTaskID/{ast_id}` — Retrieves an inspection report by asset task ID.
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/InspectionReport/GetInProgressForAsset/{as_id}` — Retrieves all in-progress inspection reports for an asset.
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/InspectionReport/GetInspectors/{ast_id}` — Retrieves all inspectors assigned to an inspection report.
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/InspectionReport/GetInstances/{ast_id}` — Retrieves all sub-asset instances included in an inspection report.
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/InspectionReport/GetMostRecentApproved/{as_id}` — Retrieves the most recent approved inspection report for an asset.
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/InspectionReport/GetMostRecentReportsForAsset/{as_guid}` — Retrieves the most recent inspection reports for an asset by GUID.
    - required params: `as_guid` (path), `apiType` (path)
- `GET /{apiType}/InspectionReport/GetMostRecentReportsForAsset/{as_id}` — Retrieves the most recent inspection reports for an asset by ID.
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/InspectionReport/GetWorkSpecs/{ast_guid}` — Retrieves project work specifications mapped to an inspection report.
    - required params: `ast_guid` (path), `apiType` (path)
- `GET /{apiType}/InspectionReport/{ast_guid}` — Retrieves an inspection report by asset task GUID.
    - required params: `ast_guid` (path), `apiType` (path)
- `GET /{apiType}/InspectionReport/{ast_id}` — Retrieves an inspection report by asset task ID.
    - required params: `ast_id` (path), `apiType` (path)

### `InspectionReportInspTypeMap`  (8 GET endpoints)
- `GET /{apiType}/InspectionReportInspTypeMap/GetAllReportInspectionTypeMap/{ast_id}` — Retrieves all inspection type mappings for a report.
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/InspectionReportInspTypeMap/GetInProgressReportInspectionTypeMap/{as_id}/{it_id}` — Retrieves a specific in-progress inspection type mapping for an asset.
    - required params: `as_id` (path), `it_id` (path), `apiType` (path)
- `GET /{apiType}/InspectionReportInspTypeMap/GetInProgressReportInspectionTypeMaps/{as_id}/{ast_id}` — Retrieves all in-progress inspection type mappings for an asset and report.
    - required params: `as_id` (path), `ast_id` (path), `apiType` (path)
- `GET /{apiType}/InspectionReportInspTypeMap/GetInspRptInspTypeMapCount/{it_id}` — Retrieves the count of report-inspection type mappings for an inspection type.
    - required params: `it_id` (path), `apiType` (path)
- `GET /{apiType}/InspectionReportInspTypeMap/GetNotApprovedReportInspectionTypeMap/{as_id}/{it_id}` — Retrieves not-approved inspection type mapping for an asset.
    - required params: `as_id` (path), `it_id` (path), `apiType` (path)
- `GET /{apiType}/InspectionReportInspTypeMap/GetReportInspectionTypeMap/{ast_id}` — Retrieves a specific or primary inspection type mapping for a report.
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/InspectionReportInspTypeMap/GetReportInspectionTypeMap/{ast_id}/{it_id}` — Retrieves a specific or primary inspection type mapping for a report.
    - required params: `ast_id` (path), `it_id` (path), `apiType` (path)
- `GET /{apiType}/InspectionReportInspTypeMap/GetScheduledReportInspectionTypeMap/{ast_id}` — Retrieves scheduled inspection type mappings for a report.
    - required params: `ast_id` (path), `apiType` (path)

### `InspectionReportMaintenanceInstance`  (1 GET endpoints)
- `GET /{apiType}/InspectionReportMaintenanceInstance/IsMaintenanceExcluded/{ast_id}/{maint_ast_id}` — Checks if a maintenance item instance is excluded from (not linked to) an open inspection report.
    - required params: `ast_id` (path), `maint_ast_id` (path), `apiType` (path)

### `InspectionType`  (14 GET endpoints)
- `GET /{apiType}/InspectionType` — Retrieves all inspection types (non-paginated version calls paginated POST).
    - required params: `apiType` (path)
- `GET /{apiType}/InspectionType/GetByAstAndInspector/{ast_id}/{in_id}` — Retrieves inspection types for a report filtered by a specific user's role access.
    - required params: `ast_id` (path), `in_id` (path), `apiType` (path)
- `GET /{apiType}/InspectionType/GetByAstAndSelf/{ast_id}` — Retrieves inspection types for a report filtered by current user's role access.
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/InspectionType/GetByAstId/{ast_id}` — Retrieves inspection types for a specific report.
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/InspectionType/GetByRtId/{rt_id}` — Retrieves inspection types for a report type, filtered by current user's access.
    - required params: `rt_id` (path), `apiType` (path)
- `GET /{apiType}/InspectionType/GetDefaultInspectionType` — Retrieves the system default inspection type.
    - required params: `apiType` (path)
- `GET /{apiType}/InspectionType/GetInspectionTypeByGuid/{it_guid}` — Retrieves an inspection type by its GUID.
    - required params: `it_guid` (path), `apiType` (path)
- `GET /{apiType}/InspectionType/GetInspectionTypeById/{it_id}` — Retrieves an inspection type by its ID.
    - required params: `it_id` (path), `apiType` (path)
- `GET /{apiType}/InspectionType/GetInspectionTypesForSelf` — Retrieves inspection types assigned to the current user's roles.
    - required params: `apiType` (path)
- `GET /{apiType}/InspectionType/GetInspectionTypesForUser/{in_id}` — Retrieves inspection types assigned to a specific user's roles.
    - required params: `in_id` (path), `apiType` (path)
- `GET /{apiType}/InspectionType/GetInspectionTypesWithOptionalReportMaps`
    - required params: `apiType` (path)
- `GET /{apiType}/InspectionType/GetInspectionTypesWithPlatformTemplate/{platform}` — Retrieves inspection types that have mobile templates for a specific platform.
    - required params: `platform` (path), `apiType` (path)
- `GET /{apiType}/InspectionType/{it_guid}` — Retrieves an inspection type by its GUID.
    - required params: `it_guid` (path), `apiType` (path)
- `GET /{apiType}/InspectionType/{it_id}` — Retrieves an inspection type by its ID.
    - required params: `it_id` (path), `apiType` (path)

### `InspectorWorkingSetMap`  (4 GET endpoints)
- `GET /{apiType}/InspectorWorkingSetMap` — Retrieves the current user's complete working set.
    - required params: `apiType` (path)
- `GET /{apiType}/InspectorWorkingSetMap/CanManageWorkingSet` — Checks if the current user can manage working sets for an asset.
    - required params: `apiType` (path)
- `GET /{apiType}/InspectorWorkingSetMap/GetChildCount/{as_id}` — Retrieves child asset count and working set membership statistics.
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/InspectorWorkingSetMap/Has/{as_id}` — Checks if an asset is in a user's working set.
    - required params: `as_id` (path), `apiType` (path)

### `Logo`  (1 GET endpoints)
- `GET /{apiType}/Logo/GetLogos` — Retrieves all logos configured for a specific profile.
    - required params: `apiType` (path)

### `MobileForm`  (1 GET endpoints)
- `GET /{apiType}/MobileForm/{fm_id}` — Retrieves a mobile form definition by ID.
    - required params: `fm_id` (path), `apiType` (path)

### `MobileFormOSMap`  (1 GET endpoints)
- `GET /{apiType}/MobileFormOSMap/{fm_id}` — Retrieves operating system mappings for a mobile form.
    - required params: `fm_id` (path), `apiType` (path)

### `MobileReportTypeFormMap`  (5 GET endpoints)
- `GET /{apiType}/MobileReportTypeFormMap` — Retrieves all mobile report type form mappings.
    - required params: `apiType` (path)
- `GET /{apiType}/MobileReportTypeFormMap/GetMobileReportTypeFormMapByFgId/{fg_id}` — Retrieves mobile form mappings for a specific form group.
    - required params: `fg_id` (path), `apiType` (path)
- `GET /{apiType}/MobileReportTypeFormMap/GetMobileReportTypeFormMapByReportType` — Retrieves mobile form mappings for a report type (alternative endpoint).
    - required params: `apiType` (path)
- `GET /{apiType}/MobileReportTypeFormMap/GetMobileReportTypeFormMapByRtId/{rt_id}` — Retrieves mobile form mappings for a specific report type.
    - required params: `rt_id` (path), `apiType` (path)
- `GET /{apiType}/MobileReportTypeFormMap/{fm_id}` — Retrieves a single mobile report type form mapping by form ID.
    - required params: `fm_id` (path), `apiType` (path)

### `ObjectMetaData`  (7 GET endpoints)
- `GET /{apiType}/ObjectMetaData/GetAsset/{objectId}/{objectType}/{et_id}/{el_col_binding}` — Retrieves metadata for an asset with an asset-specific control binding.
    - required params: `objectId` (path), `objectType` (path), `et_id` (path), `el_col_binding` (path), `apiType` (path)
- `GET /{apiType}/ObjectMetaData/GetProject/{objectId}/{objectType}/{et_id}/{el_col_binding}` — Retrieves metadata for a project with a project-specific control binding.
    - required params: `objectId` (path), `objectType` (path), `et_id` (path), `el_col_binding` (path), `apiType` (path)
- `GET /{apiType}/ObjectMetaData/GetReport/{objectId}/{objectType}/{et_id}/{el_col_binding}` — Retrieves metadata for a report with a report-specific control binding.
    - required params: `objectId` (path), `objectType` (path), `et_id` (path), `el_col_binding` (path), `apiType` (path)
- `GET /{apiType}/ObjectMetaData/GetSuppWorkSpec/{objectId}/{objectType}/{et_id}/{el_col_binding}` — Retrieves metadata for a supplemental work specification with a supp work spec-specific control binding.
    - required params: `objectId` (path), `objectType` (path), `et_id` (path), `el_col_binding` (path), `apiType` (path)
- `GET /{apiType}/ObjectMetaData/GetWorkSpec/{objectId}/{objectType}/{et_id}/{el_col_binding}` — Retrieves metadata for a work specification with a work spec-specific control binding.
    - required params: `objectId` (path), `objectType` (path), `et_id` (path), `el_col_binding` (path), `apiType` (path)
- `GET /{apiType}/ObjectMetaData/{objectId}/{objectType}/{et_id}` — Retrieves metadata for any object type without specifying a control binding.
    - required params: `objectId` (path), `objectType` (path), `et_id` (path), `apiType` (path)
- `GET /{apiType}/ObjectMetaData/{objectId}/{objectType}/{et_id}/{el_col_binding}` — Retrieves metadata for any object type with an integer control binding.
    - required params: `objectId` (path), `objectType` (path), `et_id` (path), `el_col_binding` (path), `apiType` (path)

### `ObjectProperty`  (3 GET endpoints)
- `GET /{apiType}/ObjectProperty` — Retrieves all public business objects available in the InspectTech.Business.BIC assembly.
    - required params: `apiType` (path)
- `GET /{apiType}/ObjectProperty/{ObjectName}` — Retrieves property definitions for a specific business object, optionally filtered by property names.
    - required params: `ObjectName` (path), `apiType` (path)
- `GET /{apiType}/ObjectProperty/{ObjectName}/{filter}` — Retrieves property definitions for a specific business object, optionally filtered by property names.
    - required params: `ObjectName` (path), `apiType` (path)

### `PastImports`  (1 GET endpoints)
- `GET /{apiType}/PastImports/GetPastImports` — Retrieves all past bulk import records.
    - required params: `apiType` (path)

### `ProjectTaskDetails`  (12 GET endpoints)
- `GET /{apiType}/ProjectTaskDetails/Get` — Retrieves all projects with default pagination.
    - required params: `apiType` (path)
- `GET /{apiType}/ProjectTaskDetails/GetAllProjectTaskGUIDList` — Retrieves GUIDs of all projects (administrators only).
    - required params: `apiType` (path)
- `GET /{apiType}/ProjectTaskDetails/GetAvailableOpenProjects` — Retrieves all open projects available to the current user.
    - required params: `apiType` (path)
- `GET /{apiType}/ProjectTaskDetails/GetAvailableOpenProjectsForUser` — Retrieves open projects specifically available to the current user.
    - required params: `apiType` (path)
- `GET /{apiType}/ProjectTaskDetails/GetAvailableProjects` — Retrieves all projects available to the current user.
    - required params: `apiType` (path)
- `GET /{apiType}/ProjectTaskDetails/GetOpenProjectTaskDetailByAstID/{ast_id}` — Retrieves open project details by numeric ID.
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/ProjectTaskDetails/GetParentWorkTask/{work_spec_ast_guid}` — Retrieves the parent project/work task for a work specification.
    - required params: `work_spec_ast_guid` (path), `apiType` (path)
- `GET /{apiType}/ProjectTaskDetails/GetProjectDetailFromWorkSpecGuid/{work_Spec_GUID}` — Retrieves parent project details from a work specification GUID.
    - required params: `work_Spec_GUID` (path), `apiType` (path)
- `GET /{apiType}/ProjectTaskDetails/GetProjectTaskDetail/{ast_guid}` — Retrieves detailed project information by GUID.
    - required params: `ast_guid` (path), `apiType` (path)
- `GET /{apiType}/ProjectTaskDetails/GetProjectTaskDetailByAstID/{ast_id}` — Retrieves detailed project information by numeric ID.
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/ProjectTaskDetails/GetProjectsExpiringOnDate/{dt}` — Retrieves all projects expiring on a specific date.
    - required params: `dt` (path), `apiType` (path)
- `GET /{apiType}/ProjectTaskDetails/GetUserProjectTaskGUIDList` — Retrieves GUIDs of projects accessible to the current user.
    - required params: `apiType` (path)

### `ProjectWise`  (4 GET endpoints)
- `GET /{apiType}/ProjectWise/CanConnect` — returns if ProjectWise is connected
    - required params: `apiType` (path)
- `GET /{apiType}/ProjectWise/GetDocument` — Retrieves the document associated with the specified unique identifier.
    - required params: `apiType` (path)
- `GET /{apiType}/ProjectWise/GetParentAndProjectName/{as_id}` — returns Parent and Project name
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/ProjectWise/GetProjectWiseDocsForBridgeDetail/{as_id}` — Returns ProjectWise docs
    - required params: `as_id` (path), `apiType` (path)

### `ProjectWorkSpecAssetMap`  (3 GET endpoints)
- `GET /{apiType}/ProjectWorkSpecAssetMap/GetProjectWorkSpecAssetMap/{as_id}` — Retrieves all project work specifications associated with an asset.
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/ProjectWorkSpecAssetMap/GetProjectWorkSpecAssetMap/{ast_guid}` — Retrieves all asset mappings for a project work specification.
    - required params: `ast_guid` (path), `apiType` (path)
- `GET /{apiType}/ProjectWorkSpecAssetMap/GetUserProjectWorkSpecAssetMap/{ast_guid}` — Retrieves asset mappings for a work spec, filtered by current user's asset access.
    - required params: `ast_guid` (path), `apiType` (path)

### `ProjectWorkSpecDetails`  (6 GET endpoints)
- `GET /{apiType}/ProjectWorkSpecDetails/Get` — Retrieves all active work specifications with default pagination.
    - required params: `apiType` (path)
- `GET /{apiType}/ProjectWorkSpecDetails/GetProjectWorkSpecDetail/{ast_guid}` — Retrieves detailed information for a specific project work specification by GUID.
    - required params: `ast_guid` (path), `apiType` (path)
- `GET /{apiType}/ProjectWorkSpecDetails/GetProjectWorkSpecDetailsForUser/{parent_task_ast_guid}` — Retrieves all project work specifications for a parent project that the current user can access.
    - required params: `parent_task_ast_guid` (path), `apiType` (path)
- `GET /{apiType}/ProjectWorkSpecDetails/GetSuppWorkSpecsForProject/{project_ast_guid}` — Retrieves all supplemental work specifications associated with a specific project.
    - required params: `project_ast_guid` (path), `apiType` (path)
- `GET /{apiType}/ProjectWorkSpecDetails/GetWorkSpecsExpiringOnDate/{dt}` — Retrieves all work specifications expiring on a specific date.
    - required params: `dt` (path), `apiType` (path)
- `GET /{apiType}/ProjectWorkSpecDetails/GetWorkSpecsForProject/{project_ast_guid}` — Retrieves all work specifications (both primary and supplemental) for a specific project.
    - required params: `project_ast_guid` (path), `apiType` (path)

### `ProjectWorkSpecInspTypeMap`  (4 GET endpoints)
- `GET /{apiType}/ProjectWorkSpecInspTypeMap/GetAllInspectTypes` — Retrieves all inspection types associated with a project work specification.
    - required params: `apiType` (path)
- `GET /{apiType}/ProjectWorkSpecInspTypeMap/GetInspectionTypesForProjectWorkSpec/{ast_guid}` — Retrieves full inspection type objects (not just mappings) for a work spec.
    - required params: `ast_guid` (path), `apiType` (path)
- `GET /{apiType}/ProjectWorkSpecInspTypeMap/GetProjectWorkSpecInspectionTypeMap/{ast_guid}` — Retrieves inspection type mappings filtered by current user's role-based access.
    - required params: `ast_guid` (path), `apiType` (path)
- `GET /{apiType}/ProjectWorkSpecInspTypeMap/GetProjectWorkSpecInspectionTypeMap/{ast_guid}/{it_id}` — Retrieves a specific inspection type mapping for a work spec.
    - required params: `ast_guid` (path), `it_id` (path), `apiType` (path)

### `ReportType`  (12 GET endpoints)
- `GET /{apiType}/ReportType` — Retrieves report types with optional filtering.
    - required params: `apiType` (path)
- `GET /{apiType}/ReportType/Get` — Retrieves report types with optional filtering.
    - required params: `apiType` (path)
- `GET /{apiType}/ReportType/Get/{getAll}` — Retrieves report types with optional filtering.
    - required params: `getAll` (path), `apiType` (path)
- `GET /{apiType}/ReportType/GetForAsset/{as_id}` — Retrieves report types available for a specific asset.
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/ReportType/GetForAssetType/{at_id}` — Retrieves report types available for a specific asset type.
    - required params: `at_id` (path), `apiType` (path)
- `GET /{apiType}/ReportType/GetFormGroupCount/{rt_id}` — Retrieves the count of form groups attached to a report type.
    - required params: `rt_id` (path), `apiType` (path)
- `GET /{apiType}/ReportType/GetSummaryAssetReportTypes/{as_id}` — Retrieves report types for a summary asset in the context of a specific view.
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/ReportType/GetType/{rt_id}` — Retrieves a single report type by ID.
    - required params: `rt_id` (path), `apiType` (path)
- `GET /{apiType}/ReportType/GetTypeForAsset/{as_id}` — Retrieves the report type associated with a specific asset.
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/ReportType/GetTypeForAssetTask/{ast_id}` — Retrieves the report type associated with a specific inspection report.
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/ReportType/GetTypeForWorkflow/{wf_id}` — Retrieves all report types associated with a workflow.
    - required params: `wf_id` (path), `apiType` (path)
- `GET /{apiType}/ReportType/{rt_id}` — Retrieves a single report type by ID.
    - required params: `rt_id` (path), `apiType` (path)

### `ReportTypeAssetTypeMap`  (3 GET endpoints)
- `GET /{apiType}/ReportTypeAssetTypeMap/Get/{id_type}/{id}` — Retrieves report type to asset type mappings.
    - required params: `id_type` (path), `id` (path), `apiType` (path)
- `GET /{apiType}/ReportTypeAssetTypeMap/MobileMaps` — Retrieves mobile-specific report type to asset type mappings.
    - required params: `apiType` (path)
- `GET /{apiType}/ReportTypeAssetTypeMap/MobileMaps/{id_type}/{id}` — Retrieves mobile-specific report type to asset type mappings.
    - required params: `id_type` (path), `id` (path), `apiType` (path)

### `ReportTypeFormMap`  (2 GET endpoints)
- `GET /{apiType}/ReportTypeFormMap/GetFirstMapForReport/{ast_id}` — Retrieves the first form mapping for a specific report, used to determine the initial form to display.
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/ReportTypeFormMap/GetMap/{rt_id}/{fg_id}` — Retrieves all form mappings for a specific report type within a form group.
    - required params: `rt_id` (path), `fg_id` (path), `apiType` (path)

### `ReportTypeInspectionTypeMap`  (4 GET endpoints)
- `GET /{apiType}/ReportTypeInspectionTypeMap/GetDefaultMaps/{rt_id}` — Retrieves all inspection types mapped to a report type that are marked as default.
    - required params: `rt_id` (path), `apiType` (path)
- `GET /{apiType}/ReportTypeInspectionTypeMap/GetNextRTITOrderValue/{rt_id}` — Gets the next available order value for adding a new inspection type to a report type.
    - required params: `rt_id` (path), `apiType` (path)
- `GET /{apiType}/ReportTypeInspectionTypeMap/GetReportTypesMappedToInspectionType/{it_id}` — Retrieves all report types that can be created using a specific inspection type.
    - required params: `it_id` (path), `apiType` (path)
- `GET /{apiType}/ReportTypeInspectionTypeMap/GetReportTypesMappedToInspectionTypeByRtId/{rt_id}` — Retrieves all inspection type mappings for a specific report type.
    - required params: `rt_id` (path), `apiType` (path)

### `ReportTypes`  (9 GET endpoints)
- `GET /{apiType}/ReportTypes/GetDefaultReportSection` — Retrieves all system-defined default report sections.
    - required params: `apiType` (path)
- `GET /{apiType}/ReportTypes/GetDefaultReportSections/{rt_id}` — Retrieves default report sections for a report type.
    - required params: `rt_id` (path), `apiType` (path)
- `GET /{apiType}/ReportTypes/GetFormGroupsAndForms/{rt_id}` — Retrieves all form groups and their associated forms for a report type.
    - required params: `rt_id` (path), `apiType` (path)
- `GET /{apiType}/ReportTypes/GetFormIdByReportForm` — Retrieves the form ID for the special "report_forms" replacement page form.
    - required params: `apiType` (path)
- `GET /{apiType}/ReportTypes/GetReportTypeFormMapByReportTypeId/{rt_id}` — Retrieves form mappings for a report type.
    - required params: `rt_id` (path), `apiType` (path)
- `GET /{apiType}/ReportTypes/GetReportTypeTemplateMapByReportType/{rt_id}` — Retrieves template control mappings for a report type.
    - required params: `rt_id` (path), `apiType` (path)
- `GET /{apiType}/ReportTypes/GetReportTypesModel` — Retrieves all report types with associated asset types and inspection types.
    - required params: `apiType` (path)
- `GET /{apiType}/ReportTypes/GetRoleReportTypeMapByRtId/{rt_id}` — Retrieves role mappings for a report type.
    - required params: `rt_id` (path), `apiType` (path)
- `GET /{apiType}/ReportTypes/GetSectionGroupByReportType/{rt_id}` — Retrieves section groups for a report type.
    - required params: `rt_id` (path), `apiType` (path)

### `Role`  (4 GET endpoints)
- `GET /{apiType}/Role/Get` — Retrieves all roles available in the system.
    - required params: `apiType` (path)
- `GET /{apiType}/Role/Get/{module}`
    - required params: `module` (path), `apiType` (path)
- `GET /{apiType}/Role/GetRolesMappedToUser` — Retrieves all roles assigned to the current authenticated user.
    - required params: `apiType` (path)
- `GET /{apiType}/Role/GetRolesMappedToUser/{in_id}` — Retrieves all roles assigned to a specific user.
    - required params: `in_id` (path), `apiType` (path)

### `RoleFieldSecurity`  (1 GET endpoints)
- `GET /{apiType}/RoleFieldSecurity/Get/{fe_id}` — Retrieves all roles and their access permissions for a specific form field/element.
    - required params: `fe_id` (path), `apiType` (path)

### `RoleFormSecurity`  (1 GET endpoints)
- `GET /{apiType}/RoleFormSecurity/GetAllRolesAndFormAccess/{fm_id}` — Retrieves all roles and their access levels for a specific form.
    - required params: `fm_id` (path), `apiType` (path)

### `RoleInspectionTypeMap`  (2 GET endpoints)
- `GET /{apiType}/RoleInspectionTypeMap/GetAllMappedToRole/{rl_id}` — Retrieves all inspection types accessible to a specific role.
    - required params: `rl_id` (path), `apiType` (path)
- `GET /{apiType}/RoleInspectionTypeMap/GetAllMappedToUser/{in_id}` — Retrieves all inspection types accessible to a specific user based on their role assignments.
    - required params: `in_id` (path), `apiType` (path)

### `RoleModuleTypeMap`  (2 GET endpoints)
- `GET /{apiType}/RoleModuleTypeMap/Get` — Retrieves all module types accessible to the current authenticated user.
    - required params: `apiType` (path)
- `GET /{apiType}/RoleModuleTypeMap/Get/{in_id}` — Retrieves all module types accessible to a specific user.
    - required params: `in_id` (path), `apiType` (path)

### `RoleReportTypeMap`  (1 GET endpoints)
- `GET /{apiType}/RoleReportTypeMap/Get/{rt_id}` — Retrieves all roles that are mapped to a specific report type.
    - required params: `rt_id` (path), `apiType` (path)

### `ScheduleTaskDefinitions`  (13 GET endpoints)
- `GET /{apiType}/ScheduleTaskDefinitions` — Get all ScheduleTaskDefinitions
    - required params: `apiType` (path)
- `GET /{apiType}/ScheduleTaskDefinitions/GetInspectionTypes/{sch_id}` — Retrieves a list of inspection types associated with a specific schedule.
    - required params: `sch_id` (path), `apiType` (path)
- `GET /{apiType}/ScheduleTaskDefinitions/GetOpenInspectionCount/{sch_id}` — Retrieves the count of open inspections associated with a specific schedule.
    - required params: `sch_id` (path), `apiType` (path)
- `GET /{apiType}/ScheduleTaskDefinitions/GetOpenInspectionCount/{sch_id}/{it_id}` — Retrieves the count of open inspections associated with a specific schedule and inspection type.
    - required params: `sch_id` (path), `it_id` (path), `apiType` (path)
- `GET /{apiType}/ScheduleTaskDefinitions/GetScheduleTaskDefinitionByGuid/{sch_guid}` — Get ScheduleTaskDefinition by guid
    - required params: `sch_guid` (path), `apiType` (path)
- `GET /{apiType}/ScheduleTaskDefinitions/GetScheduleTaskDefinitionById/{sch_id}` — Get ScheduleTaskDefinition by id
    - required params: `sch_id` (path), `apiType` (path)
- `GET /{apiType}/ScheduleTaskDefinitions/GetScheduleTaskDefinitionByName/{sch_name}` — Get ScheduleTaskDefinition by name
    - required params: `sch_name` (path), `apiType` (path)
- `GET /{apiType}/ScheduleTaskDefinitions/GetScheduleTaskDefinitionByName/{sch_name}/{exact}` — Get ScheduleTaskDefinition by name
    - required params: `sch_name` (path), `exact` (path), `apiType` (path)
- `GET /{apiType}/ScheduleTaskDefinitions/GetUnassignedInspectionTypes` — Retrieves a list of Unassigned InspectionTypes.
    - required params: `apiType` (path)
- `GET /{apiType}/ScheduleTaskDefinitions/{sch_guid}` — Get ScheduleTaskDefinition by guid
    - required params: `sch_guid` (path), `apiType` (path)
- `GET /{apiType}/ScheduleTaskDefinitions/{sch_id}` — Get ScheduleTaskDefinition by id
    - required params: `sch_id` (path), `apiType` (path)
- `GET /{apiType}/ScheduleTaskDefinitions/{sch_name}` — Get ScheduleTaskDefinition by name
    - required params: `sch_name` (path), `apiType` (path)
- `GET /{apiType}/ScheduleTaskDefinitions/{sch_name}/{exact}` — Get ScheduleTaskDefinition by name
    - required params: `sch_name` (path), `exact` (path), `apiType` (path)

### `StructElementADEMap`  (3 GET endpoints)
- `GET /{apiType}/StructElementADEMap/GetMapForAde/{ade_id}` — Retrieves the federal element mapping for a specific agency-developed element.
    - required params: `ade_id` (path), `apiType` (path)
- `GET /{apiType}/StructElementADEMap/GetMappedADEs/{se_id}` — Retrieves all agency-developed elements (ADEs) mapped to a federal element as full element objects.
    - required params: `se_id` (path), `apiType` (path)
- `GET /{apiType}/StructElementADEMap/GetMapsForElement/{se_id}` — Retrieves all agency-developed element mappings for a specific federal element.
    - required params: `se_id` (path), `apiType` (path)

### `StructureElement`  (13 GET endpoints)
- `GET /{apiType}/StructureElement` — Retrieves all structure elements in the system, optionally including deleted elements.
    - required params: `apiType` (path)
- `GET /{apiType}/StructureElement/GetDefects/{StructElementId}` — Retrieves all defects mapped to a specific structure element.
    - required params: `StructElementId` (path), `apiType` (path)
- `GET /{apiType}/StructureElement/GetElements/{objectType}/{objectId}` — Retrieves structure elements for an asset or report
    - required params: `objectType` (path), `objectId` (path), `apiType` (path)
- `GET /{apiType}/StructureElement/GetElements/{objectType}/{objectId}/{asId}` — Retrieves structure elements for an asset or report with optional filtering by segment, element, and environment.
    - required params: `objectType` (path), `objectId` (path), `asId` (path), `apiType` (path)
- `GET /{apiType}/StructureElement/GetElements/{objectType}/{objectId}/{asId}/{segmentId}` — Retrieves structure elements for an asset or report with optional filtering by segment, element, and environment.
    - required params: `objectType` (path), `objectId` (path), `asId` (path), `apiType` (path)
- `GET /{apiType}/StructureElement/GetElements/{objectType}/{objectId}/{asId}/{segmentId}/{elementId}` — Retrieves structure elements for an asset or report with optional filtering by segment, element, and environment.
    - required params: `objectType` (path), `objectId` (path), `asId` (path), `apiType` (path)
- `GET /{apiType}/StructureElement/GetElements/{objectType}/{objectId}/{asId}/{segmentId}/{elementId}/{environmentId}` — Retrieves structure elements for an asset or report with optional filtering by segment, element, and environment.
    - required params: `objectType` (path), `objectId` (path), `asId` (path), `apiType` (path)
- `GET /{apiType}/StructureElement/GetPhysicalElements/{objectType}/{objectId}` — Retrieves all physical element mapped to a specific asset type.
    - required params: `objectType` (path), `objectId` (path), `apiType` (path)
- `GET /{apiType}/StructureElement/GetProtectiveSystems/{StructElementId}` — Retrieves all protective systems mapped to a specific structure element.
    - required params: `StructElementId` (path), `apiType` (path)
- `GET /{apiType}/StructureElement/GetSegments/{objectType}/{objectId}` — Retrieves structure segments for an asset or report, optionally filtered to a specific sub-asset.
    - required params: `objectType` (path), `objectId` (path), `apiType` (path)
- `GET /{apiType}/StructureElement/GetSegments/{objectType}/{objectId}/{seg_as_id}` — Retrieves structure segments for an asset or report, optionally filtered to a specific sub-asset.
    - required params: `objectType` (path), `objectId` (path), `apiType` (path)
- `GET /{apiType}/StructureElement/GetSubAssets/{as_id}` — Retrieves all sub-asset elements for a specific asset.
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/StructureElement/RetriveElementDetails/{subAssetId}/{elementId}` — Retrives location, material, comment and element description for given sub-asset id and element id
    - required params: `subAssetId` (path), `elementId` (path), `apiType` (path)

### `StructureElementAssetTypeMap`  (2 GET endpoints)
- `GET /{apiType}/StructureElementAssetTypeMap/GetMapForAssetType/{at_id}` — Retrieves all structure element mappings for an asset type.
    - required params: `at_id` (path), `apiType` (path)
- `GET /{apiType}/StructureElementAssetTypeMap/GetMapForElement/{se_id}` — Retrieves all asset type mappings for a structure element.
    - required params: `se_id` (path), `apiType` (path)

### `StructureElementDefectMap`  (6 GET endpoints)
- `GET /{apiType}/StructureElementDefectMap/GetChildDefects/{se_id}` — Retrieves all defects mapped to a specific physical element or protective system.
    - required params: `se_id` (path), `apiType` (path)
- `GET /{apiType}/StructureElementDefectMap/GetFilteredChildDefects/{se_id}/{object_id}/{object_type}/{ede_id}/{parent_as_id}` — Retrieves defects for a physical element or protective system, filtered by object context and ADE assignment.
    - required params: `se_id` (path), `object_id` (path), `object_type` (path), `ede_id` (path), `parent_as_id` (path), `apiType` (path)
- `GET /{apiType}/StructureElementDefectMap/GetParentElementForDefect/{defect_se_id}/{classFilter}` — Retrieves all parent elements (physical or protective systems) that can have a specific defect.
    - required params: `defect_se_id` (path), `classFilter` (path), `apiType` (path)
- `GET /{apiType}/StructureElementDefectMap/GetUnmappedDefectsByElement/{defect_se_id}` — Retrieves defects that are not yet mapped to a specific element.
    - required params: `defect_se_id` (path), `apiType` (path)
- `GET /{apiType}/StructureElementDefectMap/GetUnmappedPhysicalElements/{defect_se_id}` — Retrieves physical elements that are not yet mapped to a specific defect.
    - required params: `defect_se_id` (path), `apiType` (path)
- `GET /{apiType}/StructureElementDefectMap/GetUnmappedSystems/{defect_se_id}` — Retrieves protective systems that are not yet mapped to a specific defect.
    - required params: `defect_se_id` (path), `apiType` (path)

### `StructureElementProtectiveSystemMap`  (4 GET endpoints)
- `GET /{apiType}/StructureElementProtectiveSystemMap/GetChildren/{se_id}` — Retrieves all protective systems (children) associated with a physical element.
    - required params: `se_id` (path), `apiType` (path)
- `GET /{apiType}/StructureElementProtectiveSystemMap/GetMappedPhysicalParents/{ps_se_id}` — Retrieves all physical elements (parents) associated with a protective system.
    - required params: `ps_se_id` (path), `apiType` (path)
- `GET /{apiType}/StructureElementProtectiveSystemMap/GetUnmappedPhysicalElements/{ps_se_id}` — Retrieves physical elements not yet mapped to a protective system.
    - required params: `ps_se_id` (path), `apiType` (path)
- `GET /{apiType}/StructureElementProtectiveSystemMap/GetUnmappedSystemsByElement/{se_id}`
    - required params: `se_id` (path), `apiType` (path)

### `StructureLocations`  (2 GET endpoints)
- `GET /{apiType}/StructureLocations` — Retrieves all available structure element locations.
    - required params: `apiType` (path)
- `GET /{apiType}/StructureLocations/{sl_id}` — Retrieves a specific structure location by ID.
    - required params: `sl_id` (path), `apiType` (path)

### `StructureMaterial`  (2 GET endpoints)
- `GET /{apiType}/StructureMaterial` — Retrieves all available structure element materials.
    - required params: `apiType` (path)
- `GET /{apiType}/StructureMaterial/{sm_id}` — Retrieves a specific structure material by ID.
    - required params: `sm_id` (path), `apiType` (path)

### `TaskDefDefaultSectionMap`  (2 GET endpoints)
- `GET /{apiType}/TaskDefDefaultSectionMap/Get/{td_id}` — Retrieves all default section mappings for a task definition.
    - required params: `td_id` (path), `apiType` (path)
- `GET /{apiType}/TaskDefDefaultSectionMap/GetById/{td_id}/{ds_id}` — Retrieves a specific default section mapping.
    - required params: `td_id` (path), `ds_id` (path), `apiType` (path)

### `TaskDefDisplayProp`  (2 GET endpoints)
- `GET /{apiType}/TaskDefDisplayProp` — Retrieves all available display property definitions.
    - required params: `apiType` (path)
- `GET /{apiType}/TaskDefDisplayProp/{tdp_id}` — Retrieves a specific display property definition by ID.
    - required params: `tdp_id` (path), `apiType` (path)

### `TaskDefDisplayPropMap`  (1 GET endpoints)
- `GET /{apiType}/TaskDefDisplayPropMap/GetTaskDefinitionDisplayProps/{td_id}` — Retrieves all display property mappings for a specific task definition.
    - required params: `td_id` (path), `apiType` (path)

### `TaskDefinition`  (11 GET endpoints)
- `GET /{apiType}/TaskDefinition` — Get All TaskDefinitions
    - required params: `apiType` (path)
- `GET /{apiType}/TaskDefinition/CanDeleteFieldTaskDefinitionMap/{td_id}/{fe_id}` — Check if field-task definition mapping can be deleted (validation only, no actual deletion)
    - required params: `td_id` (path), `fe_id` (path), `apiType` (path)
- `GET /{apiType}/TaskDefinition/GetAllMaintenanceTypes` — Get all maintenance types
    - required params: `apiType` (path)
- `GET /{apiType}/TaskDefinition/GetByFormAndTaskType/{fm_id}/{ast_type}` — Get TaskDefinition by form and TaskType
    - required params: `fm_id` (path), `ast_type` (path), `apiType` (path)
- `GET /{apiType}/TaskDefinition/GetById/{td_id}` — Get TaskDefinition by id
    - required params: `td_id` (path), `apiType` (path)
- `GET /{apiType}/TaskDefinition/GetByTaskType/{ast_type}` — Get TaskDefinition for TaskType
    - required params: `ast_type` (path), `apiType` (path)
- `GET /{apiType}/TaskDefinition/GetByTaskTypeWithMapping/{ast_type}` — Get TaskDefinitions for TaskType, includes mapping to report types
    - required params: `ast_type` (path), `apiType` (path)
- `GET /{apiType}/TaskDefinition/GetFieldMap/{td_id}` — Get field mappings for a task definition
    - required params: `td_id` (path), `apiType` (path)
- `GET /{apiType}/TaskDefinition/GetMaintenanceTypeDetail` — Gets maintenance type detail.
    - required params: `apiType` (path)
- `GET /{apiType}/TaskDefinition/GetTaskDefinitionFields/{td_id}` — Get all fields associated with a task definition
    - required params: `td_id` (path), `apiType` (path)
- `GET /{apiType}/TaskDefinition/{td_id}` — Get TaskDefinition by id
    - required params: `td_id` (path), `apiType` (path)

### `TemplateControl`  (2 GET endpoints)
- `GET /{apiType}/TemplateControl/Get/{tp_id}` — Retrieves a specific template control by ID.
    - required params: `tp_id` (path), `apiType` (path)
- `GET /{apiType}/TemplateControl/GetAllTemplates` — Retrieves all available template control definitions.
    - required params: `apiType` (path)

### `Test`  (1 GET endpoints)
- `GET /{apiType}/Test/Get` — Tests HTTP GET request handling and API connectivity.
    - required params: `apiType` (path)

### `User`  (13 GET endpoints)
- `GET /{apiType}/User` — Get the user data
    - required params: `apiType` (path)
- `GET /{apiType}/User/GetDisplayName/{in_id}` — Get the display name of the specified in_id
    - required params: `in_id` (path), `apiType` (path)
- `GET /{apiType}/User/GetFullName/{in_id}` — Get the full name of the specified in_id
    - required params: `in_id` (path), `apiType` (path)
- `GET /{apiType}/User/GetUsersForUserGroup/{ug_id}` — Get all users for the specified user group
    - required params: `ug_id` (path), `apiType` (path)
- `GET /{apiType}/User/HasAssetReadAccess/{in_id}/{as_code}` — Returns true if the user has read access to an asset
    - required params: `in_id` (path), `as_code` (path), `apiType` (path)
- `GET /{apiType}/User/HasAssetReadAccess/{in_id}/{as_id}` — Returns true if the user has read access to an asset
    - required params: `in_id` (path), `as_id` (path), `apiType` (path)
- `GET /{apiType}/User/HasAssetTaskReadAccess/{in_id}/{ast_id}` — Returns true if the user has read access to an asset task
    - required params: `in_id` (path), `ast_id` (path), `apiType` (path)
- `GET /{apiType}/User/HasAssetTaskWriteAccess/{in_id}/{ast_id}` — Returns true if the user has write access to an asset task
    - required params: `in_id` (path), `ast_id` (path), `apiType` (path)
- `GET /{apiType}/User/HasAssetWriteAccess/{in_id}/{as_code}` — Returns true if the user has write access to an asset
    - required params: `in_id` (path), `as_code` (path), `apiType` (path)
- `GET /{apiType}/User/HasAssetWriteAccess/{in_id}/{as_id}` — Returns true if the user has write access to an asset
    - required params: `in_id` (path), `as_id` (path), `apiType` (path)
- `GET /{apiType}/User/HasFormReadAccess/{in_id}/{fm_id}` — Returns true if the user has read access to the form
    - required params: `in_id` (path), `fm_id` (path), `apiType` (path)
- `GET /{apiType}/User/HasFormWriteAccess/{in_id}/{fm_id}` — Returns true if the user has write access to the form
    - required params: `in_id` (path), `fm_id` (path), `apiType` (path)
- `GET /{apiType}/User/{in_id}` — Get a specific user data
    - required params: `in_id` (path), `apiType` (path)

### `UserGroups`  (5 GET endpoints)
- `GET /{apiType}/UserGroups/Get` — Retrieves all user groups in the system.
    - required params: `apiType` (path)
- `GET /{apiType}/UserGroups/GetUserGroupsWithAccessToAssetTask/{ast_guid}` — Retrieves user groups that have access to a specific asset task/inspection by GUID.
    - required params: `ast_guid` (path), `apiType` (path)
- `GET /{apiType}/UserGroups/GetUserGroupsWithAccessToAssetTask/{ast_id}` — Retrieves user groups that have access to a specific asset task/inspection.
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/UserGroups/GetUsersGroups` — Retrieves user groups for the current authenticated user.
    - required params: `apiType` (path)
- `GET /{apiType}/UserGroups/GetUsersGroups/{in_id}` — Retrieves user groups for a specific user.
    - required params: `in_id` (path), `apiType` (path)

### `UserProperty`  (2 GET endpoints)
- `GET /{apiType}/UserProperty/GetCategories` — Returns the localized list of user property categories.
    - required params: `apiType` (path)
- `GET /{apiType}/UserProperty/GetUserProperties` — Returns all user property definitions along with the current user's saved value,
    - required params: `apiType` (path)

### `UserRoleMap`  (2 GET endpoints)
- `GET /{apiType}/UserRoleMap/GetRolesMappedToUser/{in_id}` — Retrieves all roles assigned to a specific user.
    - required params: `in_id` (path), `apiType` (path)
- `GET /{apiType}/UserRoleMap/GetUsersMappedToRole/{rl_id}` — Retrieves all users assigned to a specific role.
    - required params: `rl_id` (path), `apiType` (path)

### `Value`  (6 GET endpoints)
- `GET /{apiType}/Value/GetValue/{ast_id}/{fe_id}` — Retrieves a single field value by report ID and field ID.
    - required params: `ast_id` (path), `fe_id` (path), `apiType` (path)
- `GET /{apiType}/Value/GetValue/{ast_id}/{fe_id}/{sub_asset_id}` — Retrieves a single field value by report ID and field ID.
    - required params: `ast_id` (path), `fe_id` (path), `sub_asset_id` (path), `apiType` (path)
- `GET /{apiType}/Value/GetValuesForFieldChoices` — Retrieves distinct field values for choice fields based on type member.
    - required params: `apiType` (path)
- `GET /{apiType}/Value/GetValuesForReport/{ast_id}` — Retrieves all field values for an inspection report.
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/Value/{ast_id}/{fe_id}` — Retrieves a single field value by report ID and field ID.
    - required params: `ast_id` (path), `fe_id` (path), `apiType` (path)
- `GET /{apiType}/Value/{ast_id}/{fe_id}/{sub_asset_id}` — Retrieves a single field value by report ID and field ID.
    - required params: `ast_id` (path), `fe_id` (path), `sub_asset_id` (path), `apiType` (path)

### `ValueConflict`  (1 GET endpoints)
- `GET /{apiType}/ValueConflict/GetValueConflicts/{ast_id}` — Retrieves all detected value conflicts for a specific inspection/maintenance report.
    - required params: `ast_id` (path), `apiType` (path)

### `VersionInformation`  (1 GET endpoints)
- `GET /{apiType}/VersionInformation` — Retrieves application version and build information.
    - required params: `apiType` (path)

### `WorkFlow`  (7 GET endpoints)
- `GET /{apiType}/WorkFlow` — Returns all WorkFlows
    - required params: `apiType` (path)
- `GET /{apiType}/WorkFlow/GetByInspectionType/{it_id}` — Returns the WorkFlows by Inspection Type
    - required params: `it_id` (path), `apiType` (path)
- `GET /{apiType}/WorkFlow/GetByReportType/{rt_id}` — Returns the Workflow by ReportType
    - required params: `rt_id` (path), `apiType` (path)
- `GET /{apiType}/WorkFlow/GetByType/{wf_type}` — Returns all WorkFlows for a Workflow Type
    - required params: `wf_type` (path), `apiType` (path)
- `GET /{apiType}/WorkFlow/GetForReports/{it_id}` — Returns the WorkFlows that are attached to ReportTypes
    - required params: `apiType` (path), `it_id` (path)
- `GET /{apiType}/WorkFlow/GetForTaskDefinition/{td_id}` — Returns the WorkFlow for a Task Definition
    - required params: `td_id` (path), `apiType` (path)
- `GET /{apiType}/WorkFlow/{wf_id}` — Returns specific WorkFlow
    - required params: `wf_id` (path), `apiType` (path)

### `WorkManagementInstance`  (3 GET endpoints)
- `GET /{apiType}/WorkManagementInstance/GetByAsId/{as_id}`
    - required params: `as_id` (path), `apiType` (path)
- `GET /{apiType}/WorkManagementInstance/GetByAstId/{ast_id}`
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/WorkManagementInstance/GetLinkedWorkMgmtInstances/{as_id}/{ast_id}/{td_id}` — Get linked maintenance tasks ast_id by as_Id, td_id
    - required params: `as_id` (path), `ast_id` (path), `td_id` (path), `apiType` (path)

### `WorkflowAction`  (4 GET endpoints)
- `GET /{apiType}/WorkflowAction` — Retrieves all workflow actions in the system.
    - required params: `apiType` (path)
- `GET /{apiType}/WorkflowAction/DefaultActionExists` — Checks whether a default workflow action is configured.
    - required params: `apiType` (path)
- `GET /{apiType}/WorkflowAction/GetDefaultAction` — Retrieves the default workflow action.
    - required params: `apiType` (path)
- `GET /{apiType}/WorkflowAction/{wfa_id}` — Retrieves a specific workflow action by ID.
    - required params: `wfa_id` (path), `apiType` (path)

### `WorkflowStage`  (13 GET endpoints)
- `GET /{apiType}/WorkflowStage` — Get all WorkFlowStages
    - required params: `apiType` (path)
- `GET /{apiType}/WorkflowStage/GetApplicableUsersForNextStage/{ast_guid}/{wfs_id}` — Returns a list of users that a report or asset task can be submitted to
    - required params: `ast_guid` (path), `wfs_id` (path), `apiType` (path)
- `GET /{apiType}/WorkflowStage/GetApplicableUsersForNextStage/{ast_id}/{wfs_id}` — Returns a list of users that a report or asset task can be submitted to
    - required params: `ast_id` (path), `wfs_id` (path), `apiType` (path)
- `GET /{apiType}/WorkflowStage/GetFirstWorkflowStages` — Gets the first stages of all WorkFlows
    - required params: `apiType` (path)
- `GET /{apiType}/WorkflowStage/GetFirstWorkflowStagesByTaskDefinition/{td_id}` — Return the first stage or stages by a Task Definition. Could be multiple first stages depending on the setup.
    - required params: `td_id` (path), `apiType` (path)
- `GET /{apiType}/WorkflowStage/GetInitialWorkflowStageByReportType/{rt_id}` — Gets the initial workflow stage for a report type
    - required params: `rt_id` (path), `apiType` (path)
- `GET /{apiType}/WorkflowStage/GetInitialWorkflowStageByWorkflow/{wf_id}` — Gets the initial workflow stage for a workflow
    - required params: `wf_id` (path), `apiType` (path)
- `GET /{apiType}/WorkflowStage/GetPossibleWorkFlowStages/{ast_guid}` — Gets the next workflow stage for a given AssetTask
    - required params: `ast_guid` (path), `apiType` (path)
- `GET /{apiType}/WorkflowStage/GetPossibleWorkFlowStages/{ast_id}` — Gets the next workflow stage for a given AssetTask
    - required params: `ast_id` (path), `apiType` (path)
- `GET /{apiType}/WorkflowStage/GetPossibleWorkFlowStages/{ast_id}/{wfa_id}` — Gets the next workflow stage for a given AssetTask
    - required params: `ast_id` (path), `wfa_id` (path), `apiType` (path)
- `GET /{apiType}/WorkflowStage/GetWorkflowsStagesAndItsChildren/{wf_id}` — Get a list of workflow stages and it's children by workflow id
    - required params: `wf_id` (path), `apiType` (path)
- `GET /{apiType}/WorkflowStage/InUse/{wf_id}` — Checks if a WorkflowStage is in use
    - required params: `wf_id` (path), `apiType` (path)
- `GET /{apiType}/WorkflowStage/{wfs_id}` — Get WorkFlowStage by id
    - required params: `wfs_id` (path), `apiType` (path)


## Top-level shortcut endpoints (non-prefixed)

- `GET /AssetElements` — Get the Asset Elements
- `GET /AssetTasks` — Get the Asset Tasks
- `GET /AssetTypes` — returns list of data based on odata query
- `GET /AssetValues` — Get the Asset Values
- `GET /AssetViewTree` — returns list of Assets based on odata query
- `GET /Assets` — returns list of data based on odata query
- `GET /Fields` — Get the Fields
- `GET /ReportElements` — Get the Report Elements
- `GET /ReportValues` — Get the Report Values