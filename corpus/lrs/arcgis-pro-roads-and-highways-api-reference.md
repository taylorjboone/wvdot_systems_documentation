# ArcGIS Roads and Highways — ArcGIS Pro API Reference

An exhaustive inventory of every programmable API surface that ArcGIS Roads and Highways
(R&H) exposes **in ArcGIS Pro**. Compiled from Esri documentation for ArcGIS Pro "latest"
(3.7) / ArcGIS Roads and Highways 12.x, September 2026.

R&H and ArcGIS Pipeline Referencing (APR) are two products packaged on one shared
implementation called **ArcGIS Location Referencing**. Esri documents nearly all of the
Pro-side API as Location Referencing, not as R&H. Where a call is really only meaningful
for one of the two products, that is called out; otherwise assume it is shared.

---

## 1. API surface map

There are only four programmable surfaces in Pro, and only one of them is a real,
public, full-coverage R&H API.

| # | Surface | Entry point | Public? | R&H coverage |
|---|---------|-------------|---------|--------------|
| 1 | **Geoprocessing / Python** | `arcpy.locref` (Location Referencing toolbox) | Yes | **Complete.** 49 tools. This is *the* Pro API for R&H. |
| 2 | Pro SDK for .NET — LRS | `ArcGIS.Desktop.LocationReferencing.dll` | **No** | None. Esri lists this assembly under "Extensions with no public API". |
| 3 | Pro SDK for .NET — core LR | `ArcGIS.Core.Data.LinearReferencing` | Yes | Generic routes/dynamic segmentation only. Does **not** read or write the LRS. |
| 4 | Core geoprocessing | `arcpy.lr` (Linear Referencing toolbox) | Yes | Generic route/event tools. Not LRS-aware. |

Everything else people call "the Roads and Highways API" — `/exts/LRServer`,
`geometryToMeasure`, `applyEdits`, locks — is the **ArcGIS Enterprise** REST API, served by
ArcGIS Server, not by Pro. Pro's role there is authoring and publishing the service.
Summarized in Appendix A for completeness.

### Version note that affects every code path

> "In ArcGIS Pro 3.8, the tools and toolsets in the Location Referencing toolbox will be
> moved to the Linear Referencing toolbox."
> — *An overview of the Location Referencing toolbox*

Assume the `arcpy.locref` alias is a migration risk at 3.8. Tool *names* are expected to
survive; the module alias is what moves.

---

## 2. `arcpy.locref` — complete tool reference

Toolbox alias: `locref`. Callable as `arcpy.locref.<ToolName>(...)` or
`arcpy.<ToolName>_locref(...)`.

Licensing is uniform across all 49 tools: **ArcGIS Location Referencing (ArcGIS Pipeline
Referencing or ArcGIS Roads and Highways)**, available at Basic, Standard and Advanced.
No tool is license-gated to one product.

Notation: `{param}` = optional. "Product" flags a tool that is only practically useful for
one product, based on what it operates on — Esri's own licensing table does not make this
distinction.

### 2.1 Top-level tools (16)

| Tool | Python | Product |
|------|--------|---------|
| Append Events | `AppendEvents` | Both |
| Append Routes | `AppendRoutes` | Both |
| Apply Event Behaviors | `ApplyEventBehaviors` | Both |
| Calculate Intersecting Route Measures | `CalculateIntersectingRouteMeasures` | Both |
| Calculate Route Concurrencies | `CalculateRouteConcurrencies` | Both |
| Delete Routes | `DeleteRoutes` | Both |
| Derive Event Measures | `DeriveEventMeasures` | Both |
| Generate Calibration Points | `GenerateCalibrationPoints` | Both |
| Generate Events | `GenerateEvents` | Both |
| Generate Intersections | `GenerateIntersections` | Both |
| Generate Routes | `GenerateRoutes` | Both |
| Overlay Events | `OverlayEvents` | Both |
| Remove Overlapping Centerlines | `RemoveOverlappingCenterlines` | Both |
| Reverse Line Orders | `ReverseLineOrders` | Both |
| Translate Event Measures | `TranslateEventMeasures` | Both |
| Update Measures From LRS | `UpdateMeasuresFromLRS` | Both |

---

#### AppendEvents
Appends event records from a table, layer or feature class to an existing LRS event feature class.

```python
arcpy.locref.AppendEvents(in_dataset, in_target_event, field_mapping, {load_type},
                          {generate_event_ids}, {generate_shapes},
                          {append_to_dominant_route}, {bypass_conflict_prevention})
```

| Param | Type | Req | Values |
|---|---|---|---|
| `in_dataset` | Table View | R | |
| `in_target_event` | Feature Layer | R | |
| `field_mapping` | Field Mappings | R | |
| `load_type` | String | O | `ADD`, `RETIRE_OVERLAPS`, `RETIRE_BY_EVENT_ID`, `REPLACE_BY_EVENT_ID` |
| `generate_event_ids` | Boolean | O | `GENERATE_EVENT_IDS`, `NO_GENERATE_EVENT_IDS` |
| `generate_shapes` | Boolean | O | **deprecated** |
| `append_to_dominant_route` | Boolean | O | `APPEND_TO_DOMINANT_ROUTE`, `NO_APPEND_TO_DOMINANT_ROUTE` |
| `bypass_conflict_prevention` | Boolean | O | `BYPASS_CONFLICT_PREVENTION`, `NO_BYPASS_CONFLICT_PREVENTION` |

#### AppendRoutes
Appends routes from an input polyline layer into an LRS Network.

```python
arcpy.locref.AppendRoutes(source_routes, in_lrs_network, route_id_field, route_name_field,
                          from_date_field, to_date_field, line_id_field, line_name_field,
                          line_order_field, field_map, load_type, load_field,
                          consider_existing_centerlines, allow_partial_loading)
```

| Param | Type | Req | Values |
|---|---|---|---|
| `source_routes` | Feature Layer | R | |
| `in_lrs_network` | Feature Layer | R | |
| `route_id_field` | Field | R | |
| `route_name_field` | Field | R | |
| `from_date_field` | Field | O | |
| `to_date_field` | Field | O | |
| `line_id_field` | Field | O | |
| `line_name_field` | Field | O | |
| `line_order_field` | Field | O | |
| `field_map` | Field Mappings | O | |
| `load_type` | String | O | `ADD`, `RETIRE_BY_ROUTE_ID`, `REPLACE_BY_ROUTE_ID` |
| `load_field` | String | O | `ROUTE_ID`, `ROUTE_NAME` |
| `consider_existing_centerlines` | Boolean | O | `CONSIDER`, `DO_NOT_CONSIDER` |
| `allow_partial_loading` | Boolean | O | `ALLOW`, `DO_NOT_ALLOW` |

#### ApplyEventBehaviors
Updates event locations for every event feature class registered with the input network,
according to the route edit that was performed. This is the engine behind the whole
behavior model in §3.

```python
arcpy.locref.ApplyEventBehaviors(in_route_features)
```

| Param | Type | Req |
|---|---|---|
| `in_route_features` | Feature Layer | R |

Derived outputs: `out_event_layers` (Feature Layer), `out_details_file` (Text File).

#### CalculateIntersectingRouteMeasures
Creates a table of all routes and measures at each intersection location.

```python
arcpy.locref.CalculateIntersectingRouteMeasures(in_intersection_feature_class, out_dataset, {tvd})
```

| Param | Type | Req |
|---|---|---|
| `in_intersection_feature_class` | Feature Layer | R |
| `out_dataset` | Table | R |
| `tvd` | Date | O |

`tvd` = temporal view date.

#### CalculateRouteConcurrencies
Calculates and reports concurrent route sections in an LRS Network.

```python
arcpy.locref.CalculateRouteConcurrencies(in_route_features, out_dataset, {tvd},
                                         {find_dominance}, {include_geometry})
```

| Param | Type | Req | Values |
|---|---|---|---|
| `in_route_features` | Feature Layer | R | |
| `out_dataset` | Table | R | |
| `tvd` | Date | O | |
| `find_dominance` | Boolean | O | `FIND_DOMINANCE`, `NO_FIND_DOMINANCE` |
| `include_geometry` | Boolean | O | `INCLUDE_GEOMETRY`, `EXCLUDE_GEOMETRY` |

#### DeleteRoutes
Deletes routes and associated data elements from the LRS Network.

```python
arcpy.locref.DeleteRoutes(in_route_features, {delete_associated_calibration_points},
                          {delete_associated_events}, {delete_associated_centerlines})
```

| Param | Type | Req | Values (default first where noted) |
|---|---|---|---|
| `in_route_features` | Feature Layer | R | |
| `delete_associated_calibration_points` | Boolean | O | `NO_DELETE_CALIBRATION_POINTS` (default), `DELETE_CALIBRATION_POINTS` |
| `delete_associated_events` | Boolean | O | `NO_DELETE_EVENTS` (default), `DELETE_EVENTS` |
| `delete_associated_centerlines` | Boolean | O | `NO_DELETE_CENTERLINES` (default), `DELETE_CENTERLINES` |

#### DeriveEventMeasures
Populates and updates `DerivedRouteID` and derived measure values on point and line events.

```python
arcpy.locref.DeriveEventMeasures(in_route_features, {update_all_events}, {event_layers})
```

| Param | Type | Req | Values |
|---|---|---|---|
| `in_route_features` | Feature Layer | R | |
| `update_all_events` | Boolean | O | `UPDATE_ALL` (default), `UPDATE_SOME` |
| `event_layers` | Feature Layer | O | |

#### GenerateCalibrationPoints
Generates calibration points for any route shape, including complex shapes.

```python
arcpy.locref.GenerateCalibrationPoints(in_polyline_features, route_id_field, from_date_field,
                                       to_date_field, in_calibration_point_feature_class,
                                       lrs_network, {calibration_direction},
                                       {calibration_method}, {from_measure_field},
                                       {to_measure_field})
```

| Param | Type | Req | Values |
|---|---|---|---|
| `in_polyline_features` | Feature Layer | R | |
| `route_id_field` | Field | R | |
| `from_date_field` | Field | R | |
| `to_date_field` | Field | R | |
| `in_calibration_point_feature_class` | Feature Layer | R | |
| `lrs_network` | String | R | |
| `calibration_direction` | String | O | `DIGITIZED_DIRECTION` (default), `MEASURE_DIRECTION` |
| `calibration_method` | String | O | `GEOMETRY_LENGTH` (default), `M_ON_ROUTE`, `ATTRIBUTE_FIELDS` |
| `from_measure_field` | Field | O | only with `ATTRIBUTE_FIELDS` |
| `to_measure_field` | Field | O | only with `ATTRIBUTE_FIELDS` |

#### GenerateEvents
Regenerates shapes for event features registered with an LRS Network.

```python
arcpy.locref.GenerateEvents(in_event_layer, {bypass_events_with_null_lrs_fields})
```

| Param | Type | Req | Values |
|---|---|---|---|
| `in_event_layer` | Feature Layer | R | |
| `bypass_events_with_null_lrs_fields` | Boolean | O | `NO_BYPASS_EVENTS_WITH_NULL_LRS_FIELDS` (default), `BYPASS_EVENTS_WITH_NULL_LRS_FIELDS` |

The bypass parameter is only available in a combined LRS + Utility Network deployment (APR).

#### GenerateIntersections
Generates new intersections and updates existing ones.

```python
arcpy.locref.GenerateIntersections(in_intersection_feature_class, {in_network_layer},
                                   {start_date}, {edited_by_current_user},
                                   {bypass_conflict_prevention})
```

| Param | Type | Req | Values |
|---|---|---|---|
| `in_intersection_feature_class` | Feature Layer | R | |
| `in_network_layer` | Feature Layer | O | |
| `start_date` | Date | O | |
| `edited_by_current_user` | Boolean | O | `CURRENT_USER` (default), `ALL_USERS` |
| `bypass_conflict_prevention` | Boolean | O | `NO_BYPASS_CONFLICT_PREVENTION` (default), `BYPASS_CONFLICT_PREVENTION` |

#### GenerateRoutes
Recreates shapes and applies calibration changes for route features in an LRS Network.

```python
arcpy.locref.GenerateRoutes(in_route_features, {record_calibration_changes})
```

| Param | Type | Req | Notes |
|---|---|---|---|
| `in_route_features` | Feature Layer | R | |
| `record_calibration_changes` | Boolean | O | **legacy — no longer supported** |

#### OverlayEvents
Overlays one or more line and point event layers onto a target network.

```python
arcpy.locref.OverlayEvents(in_route_features, event_layers, output_dataset,
                           {include_geometry}, {network_fields}, {address_block_split_type})
```

| Param | Type | Req | Values |
|---|---|---|---|
| `in_route_features` | Feature Layer | R | |
| `event_layers` | Feature Layer (list) | R | |
| `output_dataset` | Table | R | |
| `include_geometry` | Boolean | O | `INCLUDE_GEOMETRY`, `EXCLUDE_GEOMETRY` |
| `network_fields` | Field (list) | O | |
| `address_block_split_type` | String | O | `NEAREST_ADDRESS_POINT`, `PROPORTIONAL` |

`address_block_split_type` is the R&H / Address Data Management path.

#### RemoveOverlappingCenterlines
Removes overlapping centerline sections so overlapping geometry shares one common centerline.

```python
arcpy.locref.RemoveOverlappingCenterlines(in_centerline_features)
```

| Param | Type | Req |
|---|---|---|
| `in_centerline_features` | Feature Layer | R |

Derived outputs: `updated_centerline_features`, `out_details_file`.

#### ReverseLineOrders
Reverses the line order for all routes in a line.

```python
arcpy.locref.ReverseLineOrders(in_route_features)
```

| Param | Type | Req |
|---|---|---|
| `in_route_features` | Feature Layer | R |

Derived outputs: `updated_route_features`, `out_details_file`, `out_derived_route_features`.

#### TranslateEventMeasures
Translates m-values of a point or line event layer from one linear referencing method to another.

```python
arcpy.locref.TranslateEventMeasures(in_source_event, in_target_route_features,
                                    out_target_event, {in_concurrent_route_matching})
```

| Param | Type | Req | Values |
|---|---|---|---|
| `in_source_event` | Feature Layer | R | |
| `in_target_route_features` | Feature Layer | R | |
| `out_target_event` | Feature Class | R | |
| `in_concurrent_route_matching` | String | O | `ANY`, `ROUTE_ID`, `ALL` |

Desktop equivalent of the REST `translate` operation.

#### UpdateMeasuresFromLRS
Populates or updates route and measure attributes on any point or line features.

```python
arcpy.locref.UpdateMeasuresFromLRS(lrs_network, lrs_date, in_features, route_id_field,
                                   from_measure_field, {to_measure_field}, {to_route_id_field},
                                   {route_name_field}, {to_route_name_field}, {search_tolerance})
```

| Param | Type | Req | Notes |
|---|---|---|---|
| `lrs_network` | Feature Layer | R | routes layer with IDs, names, measures |
| `lrs_date` | Date | R | temporal view definition |
| `in_features` | Feature Layer | R | point or line features to update |
| `route_id_field` | Field | R | |
| `from_measure_field` | Field | R | measure (point) or start measure (line) |
| `to_measure_field` | Field | O | lines only |
| `to_route_id_field` | Field | O | lines only |
| `route_name_field` | Field | O | |
| `to_route_name_field` | Field | O | lines only |
| `search_tolerance` | Double | O | |

Desktop equivalent of the REST `geometryToMeasure` operation.

---

### 2.2 Configuration toolset — top level (4)

#### ConfigureAddressFeatureClasses — **R&H**
Configures Address Range and Site Address Point feature classes from the Address Data
Management solution for use with an LRS.

```python
arcpy.locref.ConfigureAddressFeatureClasses(in_address_range_features, left_from_address_field,
                                            left_to_address_field, right_from_address_field,
                                            right_to_address_field, in_site_address_features,
                                            address_number_field, address_range_road_name_field,
                                            site_address_road_name)
```
All nine parameters required. Types: Feature Layer for `in_address_range_features` and
`in_site_address_features`, Field for the rest.

#### ConfigureUtilityNetworkFeatureClass — **APR, deprecated**
Replaced by Configure Utility Network Feature Classes.

```python
arcpy.locref.ConfigureUtilityNetworkFeatureClass(in_feature_class, route_id_field,
                                                 from_measure_field, to_measure_field)
```
All required. `in_feature_class` Feature Layer; rest Field.

#### ConfigureUtilityNetworkFeatureClasses — **APR**
Configures the Utility Network Pipeline Line, Device and Junction feature classes for LRS use.

```python
arcpy.locref.ConfigureUtilityNetworkFeatureClasses(in_line_features, line_route_id_field,
                                                   line_from_measure_field, line_to_measure_field,
                                                   in_device_features, device_route_id_field,
                                                   device_measure_field, in_junction_features,
                                                   junction_route_id_field, junction_measure_field)
```
All ten parameters required.

#### RemoveLRSEntity
Removes an LRS entity from an input geodatabase workspace.

```python
arcpy.locref.RemoveLRSEntity(in_workspace, lrs_entity_type, lrs_entity_name)
```

| Param | Type | Req | Values |
|---|---|---|---|
| `in_workspace` | Workspace | R | |
| `lrs_entity_type` | String | R | `LRS`, `NETWORK`, `EVENT`, `INTERSECTION`, `UN_FEATURE_CLASS`, `ADDRESS_FEATURE_CLASS` |
| `lrs_entity_name` | String | R | |

Derived output: `out_workspace`.

---

### 2.3 Configuration › LRS toolset (3)

#### CreateLRS
Creates an LRS and the minimum schema items: centerline, calibration point, redline
feature classes and the centerline sequence table.

```python
arcpy.locref.CreateLRS(in_workspace, lrs_name, centerline_feature_class_name,
                       calibration_point_feature_class_name, redline_feature_class_name,
                       centerline_sequence_table_name, spatial_reference, {xy_tolerance},
                       {z_tolerance}, {xy_resolution}, {z_resolution})
```

| Param | Type | Req |
|---|---|---|
| `in_workspace` | Workspace / Feature Dataset | R |
| `lrs_name` | String | R |
| `centerline_feature_class_name` | String | R |
| `calibration_point_feature_class_name` | String | R |
| `redline_feature_class_name` | String | R |
| `centerline_sequence_table_name` | String | R |
| `spatial_reference` | Spatial Reference | R |
| `xy_tolerance` / `z_tolerance` / `xy_resolution` / `z_resolution` | Linear Unit | O |

#### CreateLRSFromExistingDataset
Registers existing datasets as an LRS. This signature is the authoritative statement of
the R&H core schema contract.

```python
arcpy.locref.CreateLRSFromExistingDataset(lrs_name,
    centerline_feature_class, centerline_centerline_id_field,
    centerline_sequence_table, centerline_sequence_centerline_id_field,
    centerline_sequence_route_id_field, centerline_sequence_from_date_field,
    centerline_sequence_to_date_field, centerline_sequence_network_id_field,
    calibration_point_feature_class, calibration_point_measure_field,
    calibration_point_from_date_field, calibration_point_to_date_field,
    calibration_point_route_id_field, calibration_point_network_id_field,
    redline_feature_class, redline_from_measure_field, redline_to_measure_field,
    redline_route_id_field, redline_route_name_field, redline_effective_date_field,
    redline_activity_type_field, redline_network_id_field)
```

All 23 parameters required. Field type constraints:

| Field group | Required type |
|---|---|
| centerline id (both sides) | GUID, types must match |
| route id (centerline sequence / calibration point / redline) | GUID or text, types must match |
| from/to date fields | Date |
| network id fields | Short integer |
| calibration point measure, redline from/to measure | Double |
| redline route name | Text |
| redline activity type | Short integer |

Centerline, calibration point and redline feature classes must reside in a feature
dataset; redline must be z-enabled.

#### ModifyLRS
Modifies an existing LRS. Same field set as above, all optional, plus:

```python
arcpy.locref.ModifyLRS(in_workspace, current_lrs_name, {new_lrs_name},
                       {centerline_feature_class}, {centerline_centerline_id_field},
                       {centerline_sequence_table}, {centerline_sequence_centerline_id_field},
                       {centerline_sequence_route_id_field}, {centerline_sequence_from_date_field},
                       {centerline_sequence_to_date_field}, {centerline_sequence_network_id_field},
                       {calibration_point_feature_class}, {calibration_point_measure_field},
                       {calibration_point_from_date_field}, {calibration_point_to_date_field},
                       {calibration_point_route_id_field}, {calibration_point_network_id_field},
                       {redline_feature_class}, {redline_from_measure_field},
                       {redline_to_measure_field}, {redline_route_id_field},
                       {redline_route_name_field}, {redline_effective_date_field},
                       {redline_activity_type_field}, {redline_network_id_field},
                       {conflict_prevention}, {move_to_feature_dataset})
```

| Param | Type | Values |
|---|---|---|
| `conflict_prevention` | String | `AS_IS`, `ENABLE`, `DISABLE` |
| `move_to_feature_dataset` | Boolean | `MOVE`, `DO_NOT_MOVE` |

---

### 2.4 Configuration › LRS Network toolset (7)

#### ConfigureLookupTable
Configures a lookup table for one or more fields used in a multifield route ID.

```python
arcpy.locref.ConfigureLookupTable(in_feature_class, lookup_table, field_applied_to,
                                  lookup_key, {lookup_display}, {allow_any_lookup_value})
```

| Param | Type | Req | Values |
|---|---|---|---|
| `in_feature_class` | Feature Layer | R | |
| `lookup_table` | Table View | R | |
| `field_applied_to` | String | R | |
| `lookup_key` | String | R | |
| `lookup_display` | String | O | |
| `allow_any_lookup_value` | Boolean | O | `DO_NOT_ALLOW_ANY_VALUE` (default), `ALLOW_ANY_VALUE` |

#### ConfigureRouteDominanceRules
Configures rules that determine the dominant route where routes are concurrent.

```python
arcpy.locref.ConfigureRouteDominanceRules(in_feature_class, configure_type, rule_name,
                                          updated_rule_name, source_table_name, fields,
                                          order_method, order_type, prioritized_exceptions)
```

| Param | Type | Req | Values |
|---|---|---|---|
| `in_feature_class` | Feature Layer | R | |
| `configure_type` | String | R | `ADD`, `UPDATE`, `DELETE` |
| `rule_name` | String | R | |
| `updated_rule_name` | String | O | |
| `source_table_name` | String | O | |
| `fields` | String | O | |
| `order_method` | String | O | `LESSER` (default), `GREATER` |
| `order_type` | String | O | `ALPHANUMERIC` (default), `NUMERIC` |
| `prioritized_exceptions` | String | O | |

#### CreateLRSNetwork

```python
arcpy.locref.CreateLRSNetwork(in_path, lrs_name, network_name, route_id_field,
                              route_name_field, from_date_field, to_date_field,
                              {derive_from_line_network}, {line_network_name},
                              {include_fields_to_support_lines}, {line_id_field},
                              {line_name_field}, {line_order_field}, {measure_unit})
```

| Param | Type | Req | Values |
|---|---|---|---|
| `in_path` | Workspace / Feature Dataset | R | |
| `lrs_name`, `network_name` | String | R | |
| `route_id_field`, `route_name_field`, `from_date_field`, `to_date_field` | String | R | |
| `derive_from_line_network` | Boolean | O | `DERIVE`, `DO_NOT_DERIVE` |
| `line_network_name` | String | O | |
| `include_fields_to_support_lines` | Boolean | O | `INCLUDE`, `DO_NOT_INCLUDE` |
| `line_id_field`, `line_name_field`, `line_order_field` | String | O | |
| `measure_unit` | String | O | `MILES`, `INCHES`, `FEET`, `YARDS`, `NAUTICAL_MILES`, `INTFEET`, `INTMILES`, `MILLIMETERS`, `CENTIMETERS`, `METERS`, `KILOMETERS`, `DECIMETERS` |

#### CreateLRSNetworkFromExistingDataset

```python
arcpy.locref.CreateLRSNetworkFromExistingDataset(in_feature_class, lrs_name, route_id_field,
                                                 route_name_field, from_date_field, to_date_field,
                                                 derive_from_line_network, line_network_name,
                                                 include_fields_to_support_lines, line_id_field,
                                                 line_name_field, line_order_field,
                                                 route_id_configuration, individual_route_id_fields)
```

| Param | Type | Req | Values |
|---|---|---|---|
| `in_feature_class` | Feature Layer | R | |
| `lrs_name` | String | R | |
| `route_id_field`, `from_date_field`, `to_date_field` | Field | R | |
| `route_name_field` | Field | O | |
| `derive_from_line_network` | Boolean | O | `DERIVE`, `DO_NOT_DERIVE` |
| `line_network_name` | String | O | |
| `include_fields_to_support_lines` | Boolean | O | `INCLUDE`, `DO_NOT_INCLUDE` |
| `line_id_field`, `line_name_field`, `line_order_field` | Field | O | |
| `route_id_configuration` | String | O | `AUTOGENERATED_ROUTE_ID`, `SINGLE_FIELD_ROUTE_ID`, `MULTI_FIELD_ROUTE_ID` |
| `individual_route_id_fields` | Field | O | |

#### ModifyLRSNetwork
Same shape, everything optional, `AS_IS` added to every enum.

```python
arcpy.locref.ModifyLRSNetwork(in_feature_class, {route_id_field}, {route_name_field},
                              {from_date_field}, {to_date_field}, {derive_from_line_network},
                              {line_network_name}, {include_fields_to_support_lines},
                              {line_id_field}, {line_name_field}, {line_order_field},
                              {route_id_configuration}, {individual_route_id_fields})
```

| Param | Values |
|---|---|
| `derive_from_line_network` | `AS_IS`, `DERIVE`, `DO_NOT_DERIVE` |
| `include_fields_to_support_lines` | `AS_IS`, `INCLUDE`, `DO_NOT_INCLUDE` |
| `route_id_configuration` | `AS_IS`, `AUTOGENERATED_ROUTE_ID`, `SINGLE_FIELD_ROUTE_ID`, `MULTI_FIELD_ROUTE_ID` |

#### ModifyNetworkCalibrationRules
Controls how measure gaps are calibrated on a network.

```python
arcpy.locref.ModifyNetworkCalibrationRules(in_feature_class, {calibration_rule},
                                           {calibration_offset}, {update_measure_cartorealign})
```

| Param | Type | Req | Values |
|---|---|---|---|
| `in_feature_class` | Feature Layer | R | |
| `calibration_rule` | String | O | `AS_IS`, `ADDING_EUCLIDEAN_DISTANCE`, `STEPPING_INCREMENT`, `ADDING_INCREMENT` |
| `calibration_offset` | Double | O | increment for adding/stepping increment |
| `update_measure_cartorealign` | String | O | `AS_IS`, `ENABLE`, `DISABLE` |

Derived output: `out_feature_class`.

#### ModifyRouteIdPadding
Modifies padding, null and length properties for fields that are part of a multifield route ID.

```python
arcpy.locref.ModifyRouteIdPadding(in_feature_class, route_id_padding)
```

`route_id_padding` is a Value Table; each row is semicolon-separated:

| Column | Type | Values |
|---|---|---|
| Field | text | |
| Length | integer | |
| Variable Length | boolean | true / false |
| Enable Padding | boolean | true / false |
| Padding Character | text | |
| Padding Location | enum | `LEFT`, `RIGHT`, `LEFT_AND_RIGHT` |
| Pad if Null | boolean | true / false |
| Allow Null Values | boolean | true / false |

---

### 2.5 Configuration › LRS Event toolset (12)

#### ConfigureExternalEventWithLRS
Associates event data stored in an *external* system with an LRS. Its signature is the
canonical, complete declaration of an LRS event, including all seven behavior rules.

```python
arcpy.locref.ConfigureExternalEventWithLRS(in_event, parent_network, event_name,
    event_id_field, route_id_field, measure_field, {geometry_type}, {to_measure_field},
    {from_date_field}, {to_date_field}, {event_spans_routes}, {to_route_id_field},
    {store_route_name}, {route_name_field}, {to_route_name_field}, {calibrate_rule},
    {retire_rule}, {extend_rule}, {reassign_rule}, {realign_rule}, {reverse_rule},
    {carto_realign_rule})
```

| Param | Type | Req | Values |
|---|---|---|---|
| `in_event` | Table View | R | |
| `parent_network` | Feature Layer | R | |
| `event_name` | String | R | |
| `event_id_field`, `route_id_field`, `measure_field` | Field | R | |
| `geometry_type` | String | O | `POINT` (default), `LINE` |
| `to_measure_field`, `from_date_field`, `to_date_field` | Field | O | |
| `event_spans_routes` | String | O | `AS_IS` (default), `NO_SPANS_ROUTES`, `SPANS_ROUTES` |
| `to_route_id_field` | Field | O | |
| `store_route_name` | String | O | `AS_IS` (default), `NO_STORE_ROUTE_NAME`, `STORE_ROUTE_NAME` |
| `route_name_field`, `to_route_name_field` | Field | O | |
| `calibrate_rule` | String | O | `STAY_PUT` (default), `RETIRE`, `MOVE` |
| `retire_rule` | String | O | `STAY_PUT` (default), `RETIRE`, `MOVE`, `SNAP` |
| `extend_rule` | String | O | `STAY_PUT` (default), `RETIRE`, `MOVE`, `COVER` |
| `reassign_rule` | String | O | `STAY_PUT` (default), `RETIRE`, `MOVE`, `SNAP` |
| `realign_rule` | String | O | `STAY_PUT` (default), `RETIRE`, `MOVE`, `SNAP`, `COVER` |
| `reverse_rule` | String | O | `STAY_PUT` (default), `RETIRE`, `MOVE` |
| `carto_realign_rule` | String | O | `HONOR_ROUTE_MEASURE` (default) |

#### ConfigureExternalEventBehaviorsWithLRS
Configures an external event in an LRS without connecting to the external event system.

```python
arcpy.locref.ConfigureExternalEventBehaviorsWithLRS(event_name, parent_network, {geometry_type},
    {calibrate_rule}, {retire_rule}, {extend_rule}, {reassign_rule}, {realign_rule},
    {reverse_rule}, {carto_realign_rule})
```
Same enumerations as above; `event_name` (String) and `parent_network` (Feature Layer) required.

#### CreateLRSEvent
Creates line or point events for an existing LRS Network.

```python
arcpy.locref.CreateLRSEvent(parent_network, event_name, geometry_type, event_id_field,
                            route_id_field, from_date_field, to_date_field, loc_error_field,
                            measure_field, to_measure_field, event_spans_routes,
                            to_route_id_field, store_route_name, route_name_field,
                            to_route_name_field)
```

| Param | Type | Req | Values |
|---|---|---|---|
| `parent_network` | Feature Layer | R | |
| `event_name` | String | R | |
| `geometry_type` | String | O | `POINT` (default), `LINE` |
| `event_id_field`, `route_id_field`, `from_date_field`, `to_date_field`, `loc_error_field`, `measure_field` | String | R | |
| `to_measure_field` | String | O | |
| `event_spans_routes` | Boolean | O | `NO_SPANS_ROUTES` (default), `SPANS_ROUTES` |
| `to_route_id_field` | String | O | |
| `store_route_name` | Boolean | O | `NO_STORE_ROUTE_NAME` (default), `STORE_ROUTE_NAME` |
| `route_name_field`, `to_route_name_field` | String | O | |

#### CreateLRSEventFromExistingDataset
Registers an existing feature class as an LRS event. Identical parameter list to
`CreateLRSEvent` except `in_feature_class` (Feature Layer) replaces `event_name` +
`geometry_type`, and field parameters are `Field` rather than `String`.

```python
arcpy.locref.CreateLRSEventFromExistingDataset(parent_network, in_feature_class, event_id_field,
    route_id_field, from_date_field, to_date_field, loc_error_field, measure_field,
    to_measure_field, event_spans_routes, to_route_id_field, store_route_name,
    route_name_field, to_route_name_field)
```

#### ModifyLRSEvent

```python
arcpy.locref.ModifyLRSEvent(in_feature_class, event_id_field, route_id_field, from_date_field,
                            to_date_field, loc_error_field, measure_field, {to_measure_field},
                            {event_spans_routes}, {to_route_id_field}, {store_route_name},
                            {route_name_field}, {to_route_name_field})
```

| Param | Values |
|---|---|
| `event_spans_routes` | `AS_IS`, `NO_SPANS_ROUTES`, `SPANS_ROUTES` |
| `store_route_name` | `AS_IS`, `STORE_ROUTE_NAME`, `NO_STORE_ROUTE_NAME` |

#### ModifyEventBehaviorRules
Modifies event behavior rules for a registered event layer or feature class.

```python
arcpy.locref.ModifyEventBehaviorRules(in_feature_class, {calibrate_rule}, {retire_rule},
                                      {extend_rule}, {reassign_rule}, {realign_rule},
                                      {reverse_rule}, {carto_realign_rule})
```

| Param | Values |
|---|---|
| `calibrate_rule` | `STAY_PUT`, `RETIRE`, `MOVE` |
| `retire_rule` | `STAY_PUT`, `RETIRE`, `MOVE`, `SNAP` |
| `extend_rule` | `STAY_PUT`, `RETIRE`, `MOVE`, `COVER` |
| `reassign_rule` | `STAY_PUT`, `RETIRE`, `MOVE`, `SNAP` |
| `realign_rule` | `STAY_PUT`, `RETIRE`, `MOVE`, `SNAP`, `COVER` |
| `reverse_rule` | `STAY_PUT`, `RETIRE`, `MOVE` |
| `carto_realign_rule` | `HONOR_ROUTE_MEASURE`, `HONOR_REFERENT_LOCATION` |

Note this tool exposes `HONOR_REFERENT_LOCATION`, which the external-event tools do not.

#### EnableDerivedMeasureFields / DisableDerivedMeasureFields

```python
arcpy.locref.EnableDerivedMeasureFields(in_feature_class, {derived_route_id_field},
                                        {derived_route_name_field}, {derived_from_measure_field},
                                        {derived_to_measure_field})
arcpy.locref.DisableDerivedMeasureFields(in_feature_class)
```
Disable removes the derived-field registration from `Lrs_Metadata`; it does not drop the
columns. Derived output on both: `out_feature_class`.

#### EnableReferentFields / DisableReferentFields

```python
arcpy.locref.EnableReferentFields(in_feature_class, {from_referent_method_field},
                                  {from_referent_location_field}, {from_referent_offset_field},
                                  {to_referent_method_field}, {to_referent_location_field},
                                  {to_referent_offset_field}, {offset_units})
arcpy.locref.DisableReferentFields(in_feature_class)
```

`offset_units`: `MILES` (default), `INCHES`, `FEET`, `YARDS`, `NAUTICAL_MILES`, `INTFEET`,
`INTMILES`, `MILLIMETERS`, `CENTIMETERS`, `METERS`, `KILOMETERS`, `DECIMETERS`.

Disable removes referent column info from `Lrs_Metadata` but preserves the columns.

#### EnableStationingFields / DisableStationingFields — **APR-oriented**

```python
arcpy.locref.EnableStationingFields(in_feature_class, {station_field}, {back_station_field},
                                    {station_direction_field}, {station_measure_units},
                                    {decreasing_station_values})
arcpy.locref.DisableStationingFields(in_feature_class)
```

`station_measure_units` takes the same unit list as `offset_units`.
`decreasing_station_values` is a comma-separated string. Stationing must be enabled before
it can be disabled. Documented for both products; stationing is the engineering-station
model used by pipeline workflows.

---

### 2.6 Configuration › LRS Intersection toolset (3)

#### CreateLRSIntersection

```python
arcpy.locref.CreateLRSIntersection(parent_network, network_description_field,
                                   intersection_feature_class_name, intersecting_layers,
                                   {consider_z}, {z_tolerance})
```

| Param | Type | Req | Values |
|---|---|---|---|
| `parent_network` | Feature Layer | R | |
| `network_description_field` | Field | R | |
| `intersection_feature_class_name` | String | R | |
| `intersecting_layers` | Value Table | R | Intersection Layer; ID Field; Description Field; Name Separator |
| `consider_z` | Boolean | O | `CONSIDER_Z`, `DO_NOT_CONSIDER_Z` |
| `z_tolerance` | Double | O | |

#### CreateLRSIntersectionFromExistingDataset

```python
arcpy.locref.CreateLRSIntersectionFromExistingDataset(parent_network, network_description_field,
    in_feature_class, intersection_id_field, intersection_name_field, route_id_field,
    feature_id_field, feature_class_name_field, from_date_field, to_date_field,
    intersecting_layers, consider_z, z_tolerance, measure_field)
```
All required except `consider_z` and `z_tolerance`.

#### ModifyLRSIntersection

```python
arcpy.locref.ModifyLRSIntersection(in_feature_class, intersection_id_field,
    intersection_name_field, route_id_field, feature_id_field, feature_class_name_field,
    from_date_field, to_date_field, intersecting_layers, measure_field)
```
`in_feature_class` required; everything else optional.

---

### 2.7 Data Products toolset (4)

The Python names diverge sharply from the tool labels here — three of four use an `LR`
abbreviation the UI label does not.

| Tool label | Python name |
|---|---|
| Generate Linear Referenced Feature Count | `GenerateLRFeatureCount` |
| Generate Linear Referenced Length Summary | `GenerateLRLengthSummary` |
| Generate Linear Referenced Route Log | `GenerateLRRouteLog` |
| Generate LRS Data Product | `GenerateLrsDataProduct` |

#### GenerateLrsDataProduct
Transforms LRS data into a length, route log or feature count product, driven by a template file.

```python
arcpy.locref.GenerateLrsDataProduct(in_template, in_route_features, effective_date, {units},
                                    {boundary_features}, {summary_field},
                                    {exclude_null_summary_rows}, {output_format}, {out_file},
                                    {out_table})
```

| Param | Type | Req | Values |
|---|---|---|---|
| `in_template` | File | R | |
| `in_route_features` | Feature Layer | R | |
| `effective_date` | Date | R | |
| `units` | String | O | full unit list |
| `boundary_features` | Feature Layer | O | |
| `summary_field` | Field | O | |
| `exclude_null_summary_rows` | Boolean | O | `EXCLUDE`, `DO_NOT_EXCLUDE` |
| `output_format` | String | O | `CSV`, `TABLE` |
| `out_file` | File | O | |
| `out_table` | Table | O | |

#### GenerateLRRouteLog

```python
arcpy.locref.GenerateLRRouteLog(in_route_features, effective_date, {log_fields},
                                {merge_coincident_events}, {location_fields}, {referent_location},
                                {referent_features}, {referent_field}, {offset_units},
                                {output_format}, {out_file}, {out_table})
```

| Param | Type | Values |
|---|---|---|
| `log_fields` | Value Table | Layer; Field |
| `merge_coincident_events` | Boolean | `MERGE`, `DO_NOT_MERGE` |
| `location_fields` | Value Table | Layer; Field |
| `referent_location` | String | `NONE`, `NEAREST_UPSTREAM`, `NEAREST` |
| `referent_features` | Feature Layer | |
| `referent_field` | Field | |
| `offset_units` | String | full unit list |
| `output_format` | String | `CSV`, `TABLE` |

#### GenerateLRLengthSummary

```python
arcpy.locref.GenerateLRLengthSummary(in_route_features, effective_date, units,
                                     {summary_fields}, {length_fields},
                                     {exclude_null_summary_rows},
                                     {calculate_length_for_dominant_routes},
                                     {output_format}, {out_file}, {out_table})
```
`units` is **required** here (unlike `GenerateLrsDataProduct`).

#### GenerateLRFeatureCount

```python
arcpy.locref.GenerateLRFeatureCount(in_route_features, effective_date, {summary_fields},
                                    {feature_count_layers}, {exclude_null_summary_rows},
                                    {output_format}, {out_file}, {out_table})
```
Defaults: `exclude_null_summary_rows` = `EXCLUDE`, `output_format` = `CSV`.

---

## 3. Event behavior model

The behavior model is the semantic core of R&H. `ApplyEventBehaviors` executes it;
`ModifyEventBehaviorRules` and the two `ConfigureExternalEvent*` tools configure it.

### 3.1 The seven rules

| Rule | Effect |
|---|---|
| **Stay Put** | Preserves the event's x,y location; measures can change. |
| **Move** | Preserves the event's measures; x,y location can change. |
| **Retire** | Preserves both measure and x,y; the event is retired (visible only when rolled back before its retire date). |
| **Snap** | Preserves location along the route by snapping to a reassigned or abandoned route; m-values and route references can change. |
| **Cover** | Changes both measure and geographic location so the event spans the entire edited section. |
| **Honor Route Measure** | Preserves the event measure, or changes it proportionally to the route measure change. Cartographic realignment only. |
| **Honor Referent Location** | Changes both measure and geographic location to maintain the referent location. Cartographic realignment only. |

### 3.2 Activity → permitted rules

Derived from the GP tool parameter enumerations, which are authoritative on what is legal.

| Route activity | Rule parameter | Permitted values | Default |
|---|---|---|---|
| Calibrate Route | `calibrate_rule` | Stay Put, Retire, Move | Stay Put |
| Retire Route | `retire_rule` | Stay Put, Retire, Move, Snap | Stay Put |
| Extend Route | `extend_rule` | Stay Put, Retire, Move, Cover | Stay Put |
| Reassign Route | `reassign_rule` | Stay Put, Retire, Move, Snap | Stay Put |
| Realign Route | `realign_rule` | Stay Put, Retire, Move, Snap, Cover | Stay Put |
| Reverse Route | `reverse_rule` | Stay Put, Retire, Move | Stay Put |
| Cartographic Realign | `carto_realign_rule` | Honor Route Measure, Honor Referent Location | Honor Route Measure |

Cartographic realignment is disjoint from the other six: it never accepts the Stay Put /
Move / Retire / Snap / Cover family.

---

## 4. Pro editing operations (Location Referencing tab)

These are the interactive operations that *produce* the edits the API above consumes.
They have no public programmatic entry point (see §5), but they define the operation
vocabulary the whole system is built around.

**Route operations:** create route · extend route · retire route or portion of route ·
reassign route or portion (split / merge) · realign route · reverse route calibration ·
calibrate route.

**Centerline operations:** split centerline at a clicked location · split centerline at a
measure location · merge centerlines · delete centerlines.

**Event operations:** Add Point Event tool · Add Line Event tool · feature creation and
edit workflows · attribute-table-based create and edit.

### Process Edits

The **Process Edits** command updates events, intersections and routes affected by route
edits, and supports Pro's undo/redo. It runs a fixed geoprocessing chain:

| Network type | Chain |
|---|---|
| Line network with a derived network | Generate Intersections → Apply Event Behaviors → Generate Routes → Derive Event Measures |
| Non-line network, or line network without a derived network | Generate Intersections → Apply Event Behaviors |

That chain is the closest thing Esri publishes to a specification of "commit an LRS edit",
and it is reproducible verbatim from `arcpy.locref`.

---

## 5. ArcGIS Pro SDK for .NET

### 5.1 `ArcGIS.Desktop.LocationReferencing.dll` — no public API

The Pro SDK ships the LRS assembly, but Esri lists it under **"Extensions with no public
API"**. There is no supported .NET entry point for creating routes, applying event
behaviors, editing calibration, or driving the Location Referencing tab from an add-in.

Practical consequence: a Pro add-in that needs R&H functionality must shell out to
`arcpy.locref` geoprocessing tools (via `Geoprocessing.ExecuteToolAsync`), or call the
Enterprise `LRServer` REST API.

### 5.2 `ArcGIS.Core.Data.LinearReferencing` — public, but not LRS

This namespace covers generic linear referencing: routes, measures, events and dynamic
segmentation. It has no knowledge of the LRS data model (no centerline sequence, no
calibration points, no temporality, no behaviors).

| Type | Role |
|---|---|
| `RouteInfo` | Route feature class metadata. `RouteIDFieldName`, `GetRouteFeatureClass()`, `LocateFeatures()` |
| `EventInfo` | Base class for event table info |
| `PointEventInfo` | `PointEventInfo(eventTable, routeIdFieldName, measureFieldName, offsetFieldName)` |
| `LineEventInfo` | `LineEventInfo(eventTable, routeIdFieldName, fromMeasureFieldName, toMeasureFieldName, offsetFieldName)` |
| `RouteEventSource` | Dynamic feature class joining routes + events. `GetDefinition()`, `GetErrors()` |
| `RouteEventSourceDefinition` | Metadata for `RouteEventSource`; inherits `FeatureClassDefinition`. `GetFields()` |
| `RouteEventSourceOptions` | Base dynamic-segmentation options |
| `PointEventSourceOptions` | `AngleType`, `ComplementAngle`, `AddErrorField` |
| `LineEventSourceOptions` | `IsPositiveOffsetOnRight` |
| `EventTableConfiguration` | Base config for creating event tables |
| `PointEventTableConfiguration` | Point event table config |
| `LineEventTableConfiguration` | `KeepAllFields`, `MDirectionOffset` |
| `RouteEventSourceError` | Locating errors raised during `RouteEventSource` creation |

Documented SDK snippets: create a routes feature class via DDL · create an events table via
DDL · read route info from an M-aware polyline feature class · read event info · build a
`RouteEventSource` for point events · build one for line events · locate features along
routes (`routeInfo.LocateFeatures(featureClass, tolerance, eventTableConfiguration)`).

---

## 6. `arcpy.lr` — core Linear Referencing toolbox

Not R&H, no Location Referencing license, no LRS awareness. Listed because Pro 3.8 merges
the `locref` tools into this toolbox, and because these are the fallbacks when there is no
LRS.

| Tool | Description |
|---|---|
| Calibrate Routes | Recalculates route measures using points. |
| Create Routes | Creates routes from existing lines; inputs sharing a common identifier are merged into one route. |
| Dissolve Route Events | Removes redundancy from event tables or splits multi-attribute tables. |
| Locate Features Along Routes | Computes where input features intersect routes; writes position data to a new event table. |
| Make Route Event Layer | Creates a temporary feature layer from routes + route events. |
| Overlay Route Events | Overlays two event tables producing their union or intersection. |
| Transform Route Events | Converts event measures from one route reference to another. |

---

## Appendix A — `LRServer` REST API (Enterprise, not Pro)

What Pro authors and publishes. Included so the Pro-side inventory is not mistaken for the
whole product. Base URL: `https://<server>/rest/services/<service>/MapServer/exts/LRServer`.
Requires an ArcGIS Location Referencing license; introduced at 10.6.

**Root operations:** Apply Edits · Create Version · Delete Version · Reconcile Version ·
Query Edit Log.

**Child resources:** All Layers · Network Layer · Event Layer · Centerline Layer ·
Centerline Sequence Table · Calibration Point Layer · Intersection Layer · Redline Layer ·
Non-LRS Layer · Utility Network Layer · Address Layers · Locks.

**Configuration resources:** Get/Set Calibration Configuration ·
Get/Set Cartographic Realignment Configuration.

**Network layer operations:** `geometryToMeasure` · `measureToGeometry` ·
`geometryToReferent` · `referentToGeometry` · `translate` · `concurrencies` ·
`queryAttributeSet` · `checkEvents` · `deriveEventMeasures` · `applyEventBehaviors` ·
`appendRoutes` · `appendEvents` · `generateRoutes` · `generateEvents` ·
`generateCalibrationPoints` · `generateIntersections` · `overlayEvents` ·
`relocateEvent` · `exportNetwork` · `queryLookupTable` · `queryRouteAssociations` ·
`removeOverlappingCenterlines` · `updateMeasuresFromLRS`.

**Event layer operations:** `geometryToStation` · `stationToGeometry`.

**Lock operations:** `queryLocks` · `acquireLocks` · `releaseLocks`.

Every REST operation has a `arcpy.locref` counterpart except the lock and versioning
operations, which are server/branch-versioning concerns with no desktop equivalent.

---

## Appendix B — Version and deprecation notes

| Item | Note |
|---|---|
| Location Referencing toolbox | Moves into the Linear Referencing toolbox at ArcGIS Pro 3.8 |
| `AppendEvents.generate_shapes` | Deprecated |
| `GenerateRoutes.record_calibration_changes` | Legacy, no longer supported |
| `ConfigureUtilityNetworkFeatureClass` | Deprecated; replaced by `ConfigureUtilityNetworkFeatureClasses` |
| `GenerateEvents.bypass_events_with_null_lrs_fields` | Only in a combined LRS + Utility Network deployment |
| `ArcGIS.Desktop.LocationReferencing.dll` | No public API as of Pro 3.7 |

---

## Sources

- [An overview of the Location Referencing toolbox](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/location-referencing/an-overview-of-the-location-referencing-toolbox.html)
- [Location Referencing toolbox licensing](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/location-referencing/location-referencing-toolbox-licensing.html)
- [Configuration toolset](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/location-referencing/an-overview-of-the-configuration-toolset.html) · [LRS](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/location-referencing/an-overview-of-the-lrs-toolset.html) · [LRS Event](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/location-referencing/an-overview-of-the-lrs-event-toolset.html) · [LRS Network](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/location-referencing/an-overview-of-the-lrs-network-toolset.html) · [LRS Intersection](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/location-referencing/an-overview-of-the-lrs-intersection-toolset.html) · [Data Products](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/location-referencing/an-overview-of-the-data-products-toolset.html)
- [ArcPy modules](https://doc.esri.com/en/arcgis-pro/latest/arcpy/get-started/arcpy-modules.html)
- [Introduction to ArcGIS Roads and Highways](https://doc.esri.com/en/arcgis-pro/latest/help/production/roads-highways/what-is-roads-and-highways.html)
- [Quick tour of ArcGIS Roads and Highways](https://doc.esri.com/en/arcgis-pro/latest/help/production/roads-highways/a-quick-tour-of-esri-roads-and-highways.html)
- [Event behavior](https://doc.esri.com/en/arcgis-pro/latest/help/production/roads-highways/what-is-event-behavior.html)
- [Process route edits](https://doc.esri.com/en/arcgis-pro/latest/help/production/roads-highways/process-lrs-edits.html)
- [ProConcepts: Linear Referencing (Pro SDK)](https://doc.esri.com/en/arcgis-pro/latest/sdk/api-reference/conceptdocs/docs/ProConcepts-Linear-Referencing.html)
- [ArcGIS Pro SDK for .NET (assembly list)](https://github.com/Esri/arcgis-pro-sdk)
- [An overview of the Linear Referencing toolbox](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/linear-referencing/an-overview-of-the-linear-referencing-toolbox.html)
- [Linear Referencing Service (LRServer) REST API](https://developers.arcgis.com/rest/services-reference/enterprise/linear-referencing-service/)
