# Runtime and scripting references

The schema contains a concrete scripting path: **batch operation → stored-procedure registration → SQL procedure name**. It also exposes XAML workflow definitions, runtime expressions, and an execution-request log. No standalone `Scripts` entity set is advertised in the captured service metadata.

The additional reads were performed through Windows curl on **T20DOHB05L09456 / 192.168.1.63**, using the same test service. No stored procedure, workflow, or analysis was executed by this audit.

## Scripting layers found

| Layer | Evidence | What it supplies |
| --- | --- | --- |
| `StoredProcedures` | Six registrations, `Procedure` string | SQL procedure names, not SQL source bodies |
| `BatchOperationItems` | Five items of type `StoredProcedure` | Places the registered procedures in authored batch order |
| `Workflows.XOML` | Five XML workflow definitions | 143 `BatchExecuteActivity` steps referring to configured operations |
| `RuntimeExpressions` | 791 rows: 404 `IsRunTime=1`, 387 `IsRunTime=0` | Runtime and database expression definitions; table name alone does not imply every row is runtime |
| `ExpressionFunctions` | 147 function descriptions/signatures | Function interface documentation, not DLL implementation |
| `ExecutionRequests` | Runtime status, timing, object IDs, predecessor IDs, and status information | Evidence that operations were scheduled/executed, including one historical SQL failure |

The XAML namespaces reference `Modules.Activities` in `Workflow.module`, `dTIMSV9.Logic`, `dTIMS.Infrastructure`, and .NET `System.Activities`. The `VisualBasic.Settings` declaration is workflow-designer metadata; it is not itself evidence of an embedded VB script. The five captured workflows contain batch-execution activities rather than a separate script body.

## Stored-procedure registrations

The `Procedure` column is an executable SQL object name. An entry name such as `Bridge_01_Fill_Bridge_From_SNBI` is the dTIMS registration/display name, not necessarily the SQL name.

Registration | SQL procedure | Referenced by batch
--- | --- | ---
Bridge_01_Fill_Bridge_From_SNBI | zSP_Bridge_Analysis_from_SNBI | Bridge_Analysis_Prep
Bridge_02_Counter_Initialization | zSP_COUNTER_INITIALIZATION | Bridge_Analysis_Prep
Bridge_03_Element_Roll_Up | zSP_Element_Roll_Up | Bridge_Analysis_Prep
TDQ_HISTORY_MOST_RECENT_FIX | zTDQ_REHAB_HISTORY_FINAL_NAME_FIX | History_Combined_Rehab_Most_Recent_Processing
spCleanBaseNetwork | spCleanBaseTable | No captured batch reference
spdFRAG_HWY_ANALYSIS | zdFRAG_HWY_ANALYSIS | Analysis_Generate_Segments

## Bridge preparation order

The **current** `Bridge_Analysis_Prep` batch contains:

1. `Bridge_01_Fill_Bridge_From_SNBI` → `zSP_Bridge_Analysis_from_SNBI`.
2. `Bridge_03_Element_Roll_Up` → `zSP_Element_Roll_Up`.
3. `Bridge_02_Counter_Initialization` → `zSP_COUNTER_INITIALIZATION`.
4. Formula transformation `Bridge_Bud_Cat_Ovr`.

The separate `TAMP_2026_Bridge` batch runs the `Bridge` analysis and four named budget scenarios. This separates preparation from analysis/optimization at the configuration level.

**Historical order differs:** execution records on 2026-05-12 show SNBI fill, then counter initialization, then element roll-up. The batch registration was last modified on 2026-05-13. These timestamps establish a difference between current configuration and those historical starts; they do not prove the reason or that those historical requests were submitted as this batch.

## Pavement preparation and segmentation

`Analysis_Generate_Segments` first references `spdFRAG_HWY_ANALYSIS` → `zdFRAG_HWY_ANALYSIS`, followed by a data import named `Analysis_From_dFRAG_SQL`. The `History_Combined_Rehab_Most_Recent_Processing` batch references `TDQ_HISTORY_MOST_RECENT_FIX` → `zTDQ_REHAB_HISTORY_FINAL_NAME_FIX`.

These establish SQL-based processing outside the treatment formula tables. The original `DataImports` definitions were not included in the base export, so the import step is retained as a named unresolved target rather than assigned an invented mapping.

## Actual runtime evidence

The unfiltered request endpoint reported **5,290 records**. A descending scheduled-time sample of the latest **200** contains 198 Completed and two Canceled entries, across analyses, budget scenarios, and exports. This sample is not a full runtime history.

A separate query filtered `ObjectID` to the six registered procedures plus all nine captured batch IDs. It returned **all 28 matching records**: 27 Completed, one Error. All returned records have execution type StoredProcedure; there were no matching batch-operation request rows in that filtered result. A missing log record does not establish that an operation was never run.

Procedure | Records | Completed | Error | Latest recorded start
--- | ---: | ---: | ---: | ---
Bridge_01_Fill_Bridge_From_SNBI | 3 | 3 | 0 | 2026-05-12T08:59:07.7698724-04:00
Bridge_02_Counter_Initialization | 3 | 3 | 0 | 2026-05-12T09:02:20.2441332-04:00
Bridge_03_Element_Roll_Up | 3 | 3 | 0 | 2026-05-12T09:03:46.171382-04:00
spdFRAG_HWY_ANALYSIS | 19 | 18 | 1 | 2026-09-16T15:03:18.8748793-04:00

### Historical segmentation failure

On **2026-01-26 at 13:27:54 -05:00**, `spdFRAG_HWY_ANALYSIS` began a request that ended in Error. `StatusInformation` reports **“String or binary data would be truncated”** and **“The statement has been terminated.”** The retained messages mention committed treatments, urban data, surface type, functional class, federal aid, NHS, ownership, PSI history/current condition, hard-coded segments, PSI neighbor fixes, initial segmentation, and merging segments shorter than one mile.

Those are emitted stage labels, not recovered SQL source or proof that every labeled stage succeeded. The same procedure has later Completed records, including **2026-09-16**. Thus this is a confirmed historical error, not evidence of a current persistent failure. The full original status text is retained in SQLite and the raw response.

## Schema-defined read interfaces and the source-code limit

The service metadata advertises:

```text
GET  GetParameterlessStoredProcedures()
     returns Collection(Edm.String)

POST GetStoredProcedureText
     body: {"ProcedureIDs": [registered procedure UUIDs]}
     returns Collection(DataServices.Configuration.Models.StoredProcedureText)
```

`GetStoredProcedureText` is a source-text retrieval action, not a request to execute the SQL. Its call with all six registration IDs returned **HTTP 403** under the supplied API credentials. The audit therefore recovered procedure registrations, callers, sequence, and observed runs, but **not the SQL bodies**. The denial is recorded in `audit_runtime_exports`. No alternative credential or SQL execution path was attempted.

The metadata also exposes `CanExecute` and execution enums. `ExecutionType` explicitly includes StoredProcedure=20, Workflow=16, AnalysisSet=0, BudgetScenario=1, and BatchOperation=-1. `ExecutionStatus` includes Pending, Started, Completed, Error, Canceling, Canceled, and Debug. `LogLevel` includes Trace and Debug. These schema values describe available capabilities; they do not establish that detailed traces were retained for a specific run.

## Workflow hooks versus manual/batch invocation

`AnalysisSets.AfterExecuteWorkflowID`, `BudgetScenarios.WorkflowID`, and workflow references on captured formula/table/crosstab transformations and time-dependent queries are **all null**. The general entity model also exposes workflow hooks such as OnAssignWorkflowID and OnStatusChangedWorkflowID.

Consequently, the mere presence of five workflow definitions does not show they automatically execute after the captured analyses. Their XAML references and batch sequences are documented in [the complete reference catalog](runtime-batches-and-workflows.md). A workflow definition can remain registered even when its referenced operation is absent from the captured catalog.

## SQLite additions and coverage

`StoredProcedures` contains the six registrations. `ExecutionRequests` contains the latest-200 sample. `RuntimeProcedureExecutions` contains the complete filtered 28-record result. These two request tables overlap conceptually and must not be blindly added together to count all historical executions.

`audit_workflow_steps` contains the 143 decoded XAML activities; `audit_runtime_hooks` contains populated hook references found in the captured tables; `audit_schema_runtime_operations` preserves the relevant action/function signatures. `audit_runtime_exports` and `audit_runtime_pages` record supplemental coverage, errors, URLs, timestamps, and response hashes separately from the original 49-endpoint export.

```sql
SELECT b.Name, i."Order", i.ItemDisplayName, s.Procedure
FROM BatchOperationItems i
JOIN BatchOperations b ON b.ID=i.BatchOperationID
JOIN StoredProcedures s ON s.ID=i.ItemID
ORDER BY b.Name, i."Order";

SELECT ObjectDisplayName, ActualStartTime, ExecutionStatus, StatusInformation
FROM RuntimeProcedureExecutions
ORDER BY ActualStartTime DESC;

SELECT * FROM audit_workflow_steps ORDER BY workflow_name, xml_position;
SELECT * FROM audit_runtime_exports;
```

## PMS import follow-up

The [PMS end-to-end investigation](pms-analysis.md) subsequently captured Analysis_From_dFRAG_SQL: source zdfrag_Stage_5, target Analysis, ImportElements=true, RemoveAllElements=true. Its column-mapping endpoint returns zero explicit rows. This resolves that named import registration, but not the denied SQL procedure body. The record and response provenance are in audit_pms_sample_records and audit_pms_responses.
