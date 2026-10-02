# Formula catalog

Source: live test-service snapshot fetched through Windows host T20DOHB05L09456 on 2026-09-24. This is a static configuration audit; the proprietary dTIMS execution engine was not run.


UUIDs are replaced with captured object names only in the readable version. Original expressions below remain authoritative.

<a id="e-2a8f0106-5d97-4488-aa31-9186e43af67a"></a>

## Analysis_Com_Trt_Length

Source: `dTIMSExpressions` / `2a8f0106-5d97-4488-aa31-9186e43af67a`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(bdffb1fd-105e-455e-9895-a03a9dc2c3fb) - Get_Field(f78c831a-77dc-4adb-aed8-b23145eee671)
```

<a id="e-1e6bcee8-72b1-4cba-a5fe-3bf64dee5f93"></a>

## Analysis_Defined_Segments_Length

Source: `dTIMSExpressions` / `1e6bcee8-72b1-4cba-a5fe-3bf64dee5f93`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(fc111b8f-79c8-4978-b812-5b1f3ceae06b) - Get_Field(feff7669-2905-47f1-a9d2-4b5215e27f7c)
```

<a id="e-64bc3769-4eca-4308-97a1-65670fba0d93"></a>

## Analysis_Length

Source: `dTIMSExpressions` / `64bc3769-4eca-4308-97a1-65670fba0d93`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(97733840-0ead-4282-964d-b1c17220ff40) - Get_Field(cb6fa5ef-7385-4b2a-b6e8-71fd2391d526)
```

<a id="e-bd0a2a30-edcc-447b-b917-4c398c6c3781"></a>

## Base_Length

Source: `dTIMSExpressions` / `bd0a2a30-edcc-447b-b917-4c398c6c3781`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(ac767fbe-1fab-44f1-9dd3-842efb9136cf) - Get_Field(8b3a09b6-a8f1-429f-927d-32f2d5d501a6)
```

<a id="e-9ea5227f-79c7-43d7-9033-174bb04c5890"></a>

## Climbing_Lanes_Length

Source: `dTIMSExpressions` / `9ea5227f-79c7-43d7-9033-174bb04c5890`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(f3e27ef4-65e3-4343-9057-a60eb1291f61) - Get_Field(ebeea600-f9e8-4e73-9c2b-dccad6d0feb9)
```

<a id="e-f69faaf2-c0e8-4ab0-8494-df0618574f48"></a>

## Coal_Routes_Length

Source: `dTIMSExpressions` / `f69faaf2-c0e8-4ab0-8494-df0618574f48`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(793018c6-41bb-4944-be3e-b8362422b79d) - Get_Field(a1a28393-1d29-4247-918f-ae1e88947b30)
```

<a id="e-1d9ff93f-0f64-44a8-a0a4-91259f0933d0"></a>

## Condition_Current_Length

Source: `dTIMSExpressions` / `1d9ff93f-0f64-44a8-a0a4-91259f0933d0`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(68e2a23a-e072-4171-b908-e03e30c58043) - Get_Field(c0b7ca10-5308-4653-a40e-0a696d1a242c)
```

<a id="e-89030c80-47d3-4c3c-83a8-9e458731743a"></a>

## Condition_History_Historic_Length

Source: `dTIMSExpressions` / `89030c80-47d3-4c3c-83a8-9e458731743a`.



Readable:
```text
Get_Field(To)-Get_Field(From)
```

Original:
```text
Get_Field(7068be28-23d6-48fa-b7f2-e0704b5bc33d)-Get_Field(5b5dedec-3d4a-41f7-93dd-c872a291dabb)
```

<a id="e-8402ff94-b794-4f69-a190-4e830560cba8"></a>

## County_01_Barbour_Analysis

Source: `dTIMSExpressions` / `8402ff94-b794-4f69-a190-4e830560cba8`.

Analysis filter for Barbour

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='01' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='01' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-ae7f584b-a022-4bff-a227-0f603da46e5c"></a>

## County_02_Berkeley_Analysis

Source: `dTIMSExpressions` / `ae7f584b-a022-4bff-a227-0f603da46e5c`.

Analysis filter for Berkeley

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='02' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='02' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-2e6e7554-0efc-40e6-812f-66084d946853"></a>

## County_03_Boone_Analysis

Source: `dTIMSExpressions` / `2e6e7554-0efc-40e6-812f-66084d946853`.

Analysis filter for Boone

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='03' AND
 (NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
 (NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='03' AND
 (NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
 (NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-02c08ef4-36fa-4bdb-bda2-15fb544c6408"></a>

## County_04_Braxton_Analysis

Source: `dTIMSExpressions` / `02c08ef4-36fa-4bdb-bda2-15fb544c6408`.

Analysis filter for Braxton

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='04' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='04' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-daaeaa34-19a1-461a-9861-2ae69201fcc6"></a>

## County_05_Brooke_Analysis

Source: `dTIMSExpressions` / `daaeaa34-19a1-461a-9861-2ae69201fcc6`.

Analysis filter for Brooke

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='05' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='05' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-5e50cd53-1426-4e00-83e3-bbced84d232d"></a>

## County_06_Cabell_Analysis

Source: `dTIMSExpressions` / `5e50cd53-1426-4e00-83e3-bbced84d232d`.

Analysis filter for Cabell

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='06' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='06' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-6cfefe5f-c34c-4c4c-83f6-e04d94031603"></a>

## County_07_Calhoun_Analysis

Source: `dTIMSExpressions` / `6cfefe5f-c34c-4c4c-83f6-e04d94031603`.

Analysis filter for Calhoun

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='07' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='07' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-485b0cfa-992e-4398-bffa-5890d52beeb7"></a>

## County_08_Clay_Analysis

Source: `dTIMSExpressions` / `485b0cfa-992e-4398-bffa-5890d52beeb7`.

Analysis filter for Clay

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='08' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='08' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-488cb5ac-8256-4c64-86c6-da20594cc1be"></a>

## County_09_Doddridge_Analysis

Source: `dTIMSExpressions` / `488cb5ac-8256-4c64-86c6-da20594cc1be`.

Analysis filter for Doddridge

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='09' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='09' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-f4453a9e-3ffc-4e48-beb8-4783f3828cc1"></a>

## County_10_Fayette_Analysis

Source: `dTIMSExpressions` / `f4453a9e-3ffc-4e48-beb8-4783f3828cc1`.

Analysis filter for Fayette

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='10' AND
 (NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
 (NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='10' AND
 (NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
 (NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-dfaa4760-2aa0-4b81-8765-8bb6ee17a943"></a>

## County_11_Gilmer_Analysis

Source: `dTIMSExpressions` / `dfaa4760-2aa0-4b81-8765-8bb6ee17a943`.

Analysis filter for Gilmer

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='11' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0)
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='11' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0)
```

<a id="e-e98488b6-3307-4c2a-ad29-87b9ec978129"></a>

## County_12_Grant_Analysis

Source: `dTIMSExpressions` / `e98488b6-3307-4c2a-ad29-87b9ec978129`.

Analysis filter for Grant

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='12' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='12' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-5b27eace-88fe-41b4-b5d3-da9b6d4e7893"></a>

## County_13_Greenbrier_Analysis

Source: `dTIMSExpressions` / `5b27eace-88fe-41b4-b5d3-da9b6d4e7893`.

Analysis filter for Greenbrier

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='13' AND
 NOT  Get_Exp(PMS_abfOBJ_IM_Funds) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='13' AND
 NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-660637a0-d1b5-4bcf-a93e-e3768b313407"></a>

## County_14_Hampshire_Analysis

Source: `dTIMSExpressions` / `660637a0-d1b5-4bcf-a93e-e3768b313407`.

Analysis filter for Hampshire

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='14' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='14' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-791c8723-395a-47fd-96f0-3e6889229ccf"></a>

## County_15_Hancock_Analysis

Source: `dTIMSExpressions` / `791c8723-395a-47fd-96f0-3e6889229ccf`.

Analysis filter for Hancock

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='15' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='15' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-6a8d3da0-fb2c-4519-945d-c90ec974df31"></a>

## County_16_Hardy_Analysis

Source: `dTIMSExpressions` / `6a8d3da0-fb2c-4519-945d-c90ec974df31`.

Analysis filter for Hardy

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='16' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='16' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-822a4a71-8b75-4294-8b40-7078d44d1a06"></a>

## County_17_Harrison_Analysis

Source: `dTIMSExpressions` / `822a4a71-8b75-4294-8b40-7078d44d1a06`.

Analysis filter for Harrison

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='17' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='17' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-1d618361-b62a-4144-9f06-579d05bb2620"></a>

## County_18_Jackson_Analysis

Source: `dTIMSExpressions` / `1d618361-b62a-4144-9f06-579d05bb2620`.

Analysis filter for Jackson

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='18' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0)
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='18' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0)
```

<a id="e-ac55db6d-4658-449a-a2f4-48a58bf3e634"></a>

## County_19_Jefferson_Analysis

Source: `dTIMSExpressions` / `ac55db6d-4658-449a-a2f4-48a58bf3e634`.

Analysis filter for Jefferson

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='19' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='19' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-3b6154ef-86af-4104-a3ee-fbd11325e7d9"></a>

## County_20_Kanawha_Analysis

Source: `dTIMSExpressions` / `3b6154ef-86af-4104-a3ee-fbd11325e7d9`.

Analysis filter for Kanawha

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='20' AND
 (NOT   Get_Exp(PMS_abfOBJ_IM_Funds)) AND
 (NOT   IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
AND Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='20' AND
 (NOT   Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
 (NOT   IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
AND Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1))
```

<a id="e-d41f4888-a463-4736-a4cb-81aea6574868"></a>

## County_21_Lewis_Analysis

Source: `dTIMSExpressions` / `d41f4888-a463-4736-a4cb-81aea6574868`.

Analysis filter for Lewis

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='21' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='21' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-8fe5e452-01a0-44ce-ac7c-95d9faba5e37"></a>

## County_22_Lincoln_Analysis

Source: `dTIMSExpressions` / `8fe5e452-01a0-44ce-ac7c-95d9faba5e37`.

Analysis filter for Lincoln

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='22' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='22' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-ad5c9a37-7226-40d9-8318-6cf05fb30ee4"></a>

## County_23_Logan_Analysis

Source: `dTIMSExpressions` / `ad5c9a37-7226-40d9-8318-6cf05fb30ee4`.

Analysis filter for Logan

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='23' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='23' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-44d7a61b-6e4f-4e2b-9043-b3149c4f1547"></a>

## County_24_McDowell_Analysis

Source: `dTIMSExpressions` / `44d7a61b-6e4f-4e2b-9043-b3149c4f1547`.

Analysis filter for McDowell

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='24' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='24' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-44e2d8fa-27c5-4d2d-97e7-4425b0c60f16"></a>

## County_25_Marion_Analysis

Source: `dTIMSExpressions` / `44e2d8fa-27c5-4d2d-97e7-4425b0c60f16`.

Analysis filter for Marion

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='25' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='25' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-da11c971-1b51-4ee7-a964-69221ecacc5c"></a>

## County_26_Marshall_Analysis

Source: `dTIMSExpressions` / `da11c971-1b51-4ee7-a964-69221ecacc5c`.

Analysis filter for Marshall

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='26' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1)
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='26' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1)
```

<a id="e-d4895b73-1029-4ece-b629-afc551223f61"></a>

## County_27_Mason_Analysis

Source: `dTIMSExpressions` / `d4895b73-1029-4ece-b629-afc551223f61`.

Analysis filter for Mason

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='27' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='27' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-34789d4e-1b4e-4943-9961-8b3efa31847d"></a>

## County_28_Mercer_Analysis

Source: `dTIMSExpressions` / `34789d4e-1b4e-4943-9961-8b3efa31847d`.

Analysis filter for Mercer

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='28' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='28' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-dbb79324-8a2a-4f9c-95e5-e9e0874b697f"></a>

## County_29_Mineral_Analysis

Source: `dTIMSExpressions` / `dbb79324-8a2a-4f9c-95e5-e9e0874b697f`.

Analysis filter for Mineral

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='29' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='29' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-4020fb52-8ee8-4f8b-ae22-f14d88ae7207"></a>

## County_30_Mingo_Analysis

Source: `dTIMSExpressions` / `4020fb52-8ee8-4f8b-ae22-f14d88ae7207`.

Analysis filter for Mingo

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='30' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='30' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-350c98b6-2e79-4895-9e9b-0b44c6a9b02f"></a>

## County_31_Monongalia_Analysis

Source: `dTIMSExpressions` / `350c98b6-2e79-4895-9e9b-0b44c6a9b02f`.

Analysis filter for Monongalia.  Includes NHS Routes (No Interstates)

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='31' AND
(NOT    Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT    IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
AND Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='31' AND
(NOT    Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT    IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
AND Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1))
```

<a id="e-46d16e3f-0d61-4e8d-9342-388f998c22b2"></a>

## County_31_Monongalia_Analysis_Removed_NHS_Routes

Source: `dTIMSExpressions` / `46d16e3f-0d61-4e8d-9342-388f998c22b2`.

Analysis filter for Monongalia

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='31' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0))) AND NOT  
(Get_Field(Name)='31200190000NB-008.990-1' OR
Get_Field(Name)='31200190000nb-009.300-1' OR
Get_Field(Name)='31200190000nb-011.200-1' OR
Get_Field(Name)='31200190000nb-011.200-1' OR
Get_Field(Name)='31200190000nb-011.260-1' OR
Get_Field(Name)='31200190000nb-011.340-1' OR
Get_Field(Name)='31200190000nb-011.600-1' OR
Get_Field(Name)='31200190000nb-011.800-1' OR
Get_Field(Name)='31200190000nb-014.500-1' OR
Get_Field(Name)='31200190000nb-015.100-1' OR
Get_Field(Name)='31200190000nb-016.490-1' OR
Get_Field(Name)='31201190000nb-010.150-1' OR
Get_Field(Name)='31201190000nb-012.800-1' OR
Get_Field(Name)='31201190000nb-016.000-1' OR
Get_Field(Name)='31201190000nb-018.200-1' OR
Get_Field(Name)='3130007000000-000.000-1' OR
Get_Field(Name)='3130007000000-005.000-1' OR
Get_Field(Name)='3130007000000-010.000-1' OR
Get_Field(Name)='3130007000000-015.000-1' OR
Get_Field(Name)='3130007000000-020.000-1' OR
Get_Field(Name)='3130007000000-025.000-1' OR
Get_Field(Name)='3130043000000-000.000-1' OR
Get_Field(Name)='3130705000000-000.000-1' OR
Get_Field(Name)='3140857000000-006.210-1')
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='31' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0))) AND NOT  
(Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='31200190000NB-008.990-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='31200190000nb-009.300-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='31200190000nb-011.200-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='31200190000nb-011.200-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='31200190000nb-011.260-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='31200190000nb-011.340-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='31200190000nb-011.600-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='31200190000nb-011.800-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='31200190000nb-014.500-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='31200190000nb-015.100-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='31200190000nb-016.490-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='31201190000nb-010.150-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='31201190000nb-012.800-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='31201190000nb-016.000-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='31201190000nb-018.200-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='3130007000000-000.000-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='3130007000000-005.000-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='3130007000000-010.000-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='3130007000000-015.000-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='3130007000000-020.000-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='3130007000000-025.000-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='3130043000000-000.000-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='3130705000000-000.000-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='3140857000000-006.210-1')
```

<a id="e-9687e769-3776-4722-ab54-778fc2ac780f"></a>

## County_32_Monroe_Analysis

Source: `dTIMSExpressions` / `9687e769-3776-4722-ab54-778fc2ac780f`.

Analysis filter for Monroe

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='32' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='32' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-a0b91bd6-b3fc-4d1d-b14a-ecb0820895d7"></a>

## County_33_Morgan_Analysis

Source: `dTIMSExpressions` / `a0b91bd6-b3fc-4d1d-b14a-ecb0820895d7`.

Analysis filter for Morgan

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='33' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='33' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-20ed539d-a664-4dfa-ad79-05e726fd97cb"></a>

## County_34_Nicholas_Analysis

Source: `dTIMSExpressions` / `20ed539d-a664-4dfa-ad79-05e726fd97cb`.

Analysis filter for Nicholas

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='34' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='34' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-694a98c5-ca96-4155-b30c-3d732ea253f0"></a>

## County_35_Ohio_Analysis

Source: `dTIMSExpressions` / `694a98c5-ca96-4155-b30c-3d732ea253f0`.

Analysis filter for Ohio

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='35' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='35' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-4761cfd5-0b8a-418b-afec-f91f1052b6bb"></a>

## County_36_Pendleton_Analysis

Source: `dTIMSExpressions` / `4761cfd5-0b8a-418b-afec-f91f1052b6bb`.

Analysis filter for Pendleton

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='36' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='36' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-f0fc2bac-0970-4b5c-ba79-b62351aa89cc"></a>

## County_37_Pleasants_Analysis

Source: `dTIMSExpressions` / `f0fc2bac-0970-4b5c-ba79-b62351aa89cc`.

Analysis filter for Pleasants

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='37' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='37' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-a4de0390-bbdf-48bf-b645-71822c459873"></a>

## County_38_Pocahontas_Analysis

Source: `dTIMSExpressions` / `a4de0390-bbdf-48bf-b645-71822c459873`.

Analysis filter for Pocahontas

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='38' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='38' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-0fc8a94e-62b8-4e15-9ce1-fe3eb1bc3d13"></a>

## County_39_Preston_Analysis

Source: `dTIMSExpressions` / `0fc8a94e-62b8-4e15-9ce1-fe3eb1bc3d13`.

Analysis filter for Preston

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='39' AND
(NOT   Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT   IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
AND Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1))

```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='39' AND
(NOT   Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT   IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
AND Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1))

```

<a id="e-f30a6de4-5d4c-4ca8-ab53-114d4a6008c8"></a>

## County_39_Preston_Analysis_Removed_NHS_Routes

Source: `dTIMSExpressions` / `f30a6de4-5d4c-4ca8-ab53-114d4a6008c8`.

Analysis filter for Preston

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='39' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='39' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-bd30c4fb-7213-48d2-b9f3-78cfa3930ab5"></a>

## County_40_Putnam_Analysis

Source: `dTIMSExpressions` / `bd30c4fb-7213-48d2-b9f3-78cfa3930ab5`.

Analysis filter for Putnam

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='40' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='40' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-a8d54937-e5b8-443b-b005-17a8de8da907"></a>

## County_41_Raleigh_Analysis

Source: `dTIMSExpressions` / `a8d54937-e5b8-443b-b005-17a8de8da907`.

Analysis filter for Raleigh

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='41' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='41' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-5c58a6f2-81c4-49ab-b5d1-2c29ced6ee97"></a>

## County_42_Randolph_Analysis

Source: `dTIMSExpressions` / `5c58a6f2-81c4-49ab-b5d1-2c29ced6ee97`.

Analysis filter for Randolph

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='42' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='42' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-b77eedbb-d624-4547-ac35-4d2738cc1522"></a>

## County_43_Ritchie_Analysis

Source: `dTIMSExpressions` / `b77eedbb-d624-4547-ac35-4d2738cc1522`.

Analysis filter for Ritchie

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='43' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='43' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-8ffd0937-cf01-4c9d-bd79-8988010e0019"></a>

## County_44_Roane_Analysis

Source: `dTIMSExpressions` / `8ffd0937-cf01-4c9d-bd79-8988010e0019`.

Analysis filter for Roane

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='44' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='44' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-819e0dfc-edaa-4550-a250-648560c30e98"></a>

## County_45_Summers_Analysis

Source: `dTIMSExpressions` / `819e0dfc-edaa-4550-a250-648560c30e98`.

Analysis filter for Summers

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='45' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='45' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-130f4ca1-6d04-410f-ada2-fe9c18041ba8"></a>

## County_46_Taylor_Analysis

Source: `dTIMSExpressions` / `130f4ca1-6d04-410f-ada2-fe9c18041ba8`.

Analysis filter for Taylor

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='46' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='46' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-ce5aecbf-46e3-48c4-8a04-45f981cc5a58"></a>

## County_47_Tucker_Analysis

Source: `dTIMSExpressions` / `ce5aecbf-46e3-48c4-8a04-45f981cc5a58`.

Analysis filter for Tucker

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='47' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='47' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-52597624-4e31-4c80-9bea-d54f41bcfbe2"></a>

## County_48_Tyler_Analysis

Source: `dTIMSExpressions` / `52597624-4e31-4c80-9bea-d54f41bcfbe2`.

Analysis filter for Tyler

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='48' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='48' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-9936b8cf-ca39-43c0-9c8d-5d0f0caddb9e"></a>

## County_49_Upshur_Analysis

Source: `dTIMSExpressions` / `9936b8cf-ca39-43c0-9c8d-5d0f0caddb9e`.

Analysis filter for Upshur

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='49' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='49' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-894c641f-4a89-4e89-b2c9-0b05e381b55c"></a>

## County_50_Wayne_Analysis

Source: `dTIMSExpressions` / `894c641f-4a89-4e89-b2c9-0b05e381b55c`.

Analysis filter for Wayne

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='50' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='50' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-f634b212-1395-4ea2-976b-277f8d016467"></a>

## County_51_Webster_Analysis

Source: `dTIMSExpressions` / `f634b212-1395-4ea2-976b-277f8d016467`.

Analysis filter for Webster

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='51' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='51' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-0bf83cf5-c243-464e-9e8a-df65dfc8e7a2"></a>

## County_52_Wetzel_Analysis

Source: `dTIMSExpressions` / `0bf83cf5-c243-464e-9e8a-df65dfc8e7a2`.

Analysis filter for Wetzel

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='52' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='52' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-f876f723-6937-429c-b6f1-94415ca01475"></a>

## County_53_Wirt_Analysis

Source: `dTIMSExpressions` / `f876f723-6937-429c-b6f1-94415ca01475`.

Analysis filter for Wirt

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='53' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='53' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-7cf072ec-2ecb-4da0-a341-1199e3a7c70c"></a>

## County_54_Wood_Analysis

Source: `dTIMSExpressions` / `7cf072ec-2ecb-4da0-a341-1199e3a7c70c`.

Analysis filter for Wood

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='54' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='54' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-1ba5e7aa-a1fa-455f-a4aa-230a455cf35a"></a>

## County_55_Wyoming_Analysis

Source: `dTIMSExpressions` / `1ba5e7aa-a1fa-455f-a4aa-230a455cf35a`.

Analysis filter for Wyoming

Readable:
```text
 LEFT(Get_Field(County),Get_Number(2))='55' AND
(NOT  Get_Exp(PMS_abfOBJ_IM_Funds)) AND
(NOT  IFDEFAULT(Get_Field(COND_YEAR))) AND
 Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2))='55' AND
(NOT  Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7)) AND
(NOT  IFDEFAULT(Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) AND
 Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-fb2ac2c8-ef58-48b8-a38b-954cdd6f5a2e"></a>

## Current_Rehab_Length

Source: `dTIMSExpressions` / `fb2ac2c8-ef58-48b8-a38b-954cdd6f5a2e`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(1186b781-5ac1-483f-aa25-1cdc02c2faae) - Get_Field(2be87ab2-deb2-4863-aebd-e6100f5e9892)
```

<a id="e-1fe2f8d3-ae39-446f-9f02-c05c851d10e5"></a>

## DEL_APD

Source: `dTIMSExpressions` / `1fe2f8d3-ae39-446f-9f02-c05c851d10e5`.

4/4/2023: Making an APD Section that does not include I-68 or other unwanted sections.

Readable:
```text
Get_Exp(PMS_abfOBJ_Valid_Analysis_Section) AND
IF(Get_Field(Sign)='1',FALSE,TRUE) AND
Get_Field(Spec_Sys) = '10' AND
NOT      Get_Exp(PMS_abfOBJ_I68)
AND NOT           
(Get_Field(Name)='1630055000000-011.090-1' OR
Get_Field(Name)='1630055000000-038.500-1' OR
Get_Field(Name)='1230093000000-001.540-1' OR 
Get_Field(Name)='1630055000000-034.150-1' OR
Get_Field(Name)='4730032000000-010.400-1' OR
Get_Field(Name)='4730032000000-014.790-1' OR
Get_Field(Name)='4730093000000-000.000-1' OR
Get_Field(Name)='42200330000EB-007.900-1' OR
Get_Field(Name)='42202190000NB-045.700-1' OR
Get_Field(Name)='42202190000NB-047.500-1' OR
Get_Field(Name)='47202190000NB-000.000-1' OR
Get_Field(Name)='47202190000NB-005.000-1' OR
Get_Field(Name)='47202190000NB-009.000-1' OR
Get_Field(Name)='47202190000NB-010.000-1' OR
Get_Field(Name)='47202190000NB-011.000-1' OR
Get_Field(Name)='47202190000NB-012.000-1' OR
Get_Field(Name)='47202190000NB-013.000-1' OR
Get_Field(Name)='47202190000NB-014.000-1' OR
Get_Field(Name)='47202190000NB-015.000-1' OR 
Get_Field(Name)='42202190000NB-052.820-1' OR
Get_Field(Name)='42202190000NB-053.820-1' OR
Get_Field(Name)='42202190000NB-054.500-1')
```

Original:
```text
Get_Exp(d7d1be3c-b7bc-4ff7-b551-6f8730fbb39c) AND
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='1',FALSE,TRUE) AND
Get_Field(51f41088-b57b-4756-9b09-b108c4a81640) = '10' AND
NOT      Get_Exp(4c811992-2c2d-42c6-b156-c4d16973b739)
AND NOT           
(Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='1630055000000-011.090-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='1630055000000-038.500-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='1230093000000-001.540-1' OR 
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='1630055000000-034.150-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='4730032000000-010.400-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='4730032000000-014.790-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='4730093000000-000.000-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='42200330000EB-007.900-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='42202190000NB-045.700-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='42202190000NB-047.500-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='47202190000NB-000.000-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='47202190000NB-005.000-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='47202190000NB-009.000-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='47202190000NB-010.000-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='47202190000NB-011.000-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='47202190000NB-012.000-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='47202190000NB-013.000-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='47202190000NB-014.000-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='47202190000NB-015.000-1' OR 
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='42202190000NB-052.820-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='42202190000NB-053.820-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='42202190000NB-054.500-1')
```

<a id="e-aef270de-a987-4df1-9853-7faa4086e8c9"></a>

## DEL_District_001_NHS_Database_Expression

Source: `dTIMSExpressions` / `aef270de-a987-4df1-9853-7faa4086e8c9`.

NHS + MISLABELED APD ROUTES.

Readable:
```text
(Get_Exp(County_03_Boone_Analysis) OR
Get_Exp(County_08_Clay_Analysis) OR
Get_Exp(County_20_Kanawha_Analysis) OR
Get_Exp(County_27_Mason_Analysis) OR
Get_Exp(County_40_Putnam_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NHS'
```

Original:
```text
(Get_Exp(2e6e7554-0efc-40e6-812f-66084d946853) OR
Get_Exp(485b0cfa-992e-4398-bffa-5890d52beeb7) OR
Get_Exp(3b6154ef-86af-4104-a3ee-fbd11325e7d9) OR
Get_Exp(d4895b73-1029-4ece-b629-afc551223f61) OR
Get_Exp(bd30c4fb-7213-48d2-b9f3-78cfa3930ab5)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NHS'
```

<a id="e-95087272-914d-40ed-b54f-aaf1be90ab06"></a>

## DEL_District_001_Non_NHS_Database_Expression

Source: `dTIMSExpressions` / `95087272-914d-40ed-b54f-aaf1be90ab06`.

Database Expression for District 1 Non-NHS Analysis Set

Readable:
```text
(Get_Exp(County_03_Boone_Analysis) OR
Get_Exp(County_08_Clay_Analysis) OR
Get_Exp(County_20_Kanawha_Analysis) OR
Get_Exp(County_27_Mason_Analysis) OR
Get_Exp(County_40_Putnam_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NON_NHS'
```

Original:
```text
(Get_Exp(2e6e7554-0efc-40e6-812f-66084d946853) OR
Get_Exp(485b0cfa-992e-4398-bffa-5890d52beeb7) OR
Get_Exp(3b6154ef-86af-4104-a3ee-fbd11325e7d9) OR
Get_Exp(d4895b73-1029-4ece-b629-afc551223f61) OR
Get_Exp(bd30c4fb-7213-48d2-b9f3-78cfa3930ab5)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NON_NHS'
```

<a id="e-22dc046d-d747-4949-8ccb-3dfcea7dc77a"></a>

## DEL_District_002_NHS_Database_Expression

Source: `dTIMSExpressions` / `22dc046d-d747-4949-8ccb-3dfcea7dc77a`.

Database Expression for District 2 Analysis Set

Readable:
```text
Get_Exp(PMS_abfOBJ_Valid_Analysis_Section)
AND
Get_Field(TAMP_CLASS) = 'NHS'
AND
Get_Field(Dist)='02'
AND 
(NOT            Get_Exp(PMS_abfOBJ_IM_Funds))
```

Original:
```text
Get_Exp(d7d1be3c-b7bc-4ff7-b551-6f8730fbb39c)
AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NHS'
AND
Get_Field(df7e2acc-a05b-47dd-bb81-87b419d02677)='02'
AND 
(NOT            Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7))
```

<a id="e-31a563ea-5e4c-46dc-bad5-596d6457eeea"></a>

## DEL_District_002_Non_NHS_Database_Expression

Source: `dTIMSExpressions` / `31a563ea-5e4c-46dc-bad5-596d6457eeea`.

Database Expression for District 2 Non-NHS Analysis Set

Readable:
```text
(Get_Exp(County_06_Cabell_Analysis) OR
Get_Exp(County_22_Lincoln_Analysis) OR
Get_Exp(County_23_Logan_Analysis) OR
Get_Exp(County_30_Mingo_Analysis) OR
Get_Exp(County_50_Wayne_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NON_NHS'
```

Original:
```text
(Get_Exp(5e50cd53-1426-4e00-83e3-bbced84d232d) OR
Get_Exp(8fe5e452-01a0-44ce-ac7c-95d9faba5e37) OR
Get_Exp(ad5c9a37-7226-40d9-8318-6cf05fb30ee4) OR
Get_Exp(4020fb52-8ee8-4f8b-ae22-f14d88ae7207) OR
Get_Exp(894c641f-4a89-4e89-b2c9-0b05e381b55c)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NON_NHS'
```

<a id="e-b259ebe2-7fee-4cee-8935-568c33ff2e0d"></a>

## DEL_District_003_NHS_Database_Expression

Source: `dTIMSExpressions` / `b259ebe2-7fee-4cee-8935-568c33ff2e0d`.

Database Expression for District 3 NHS Analysis Set

Readable:
```text
(Get_Exp(County_07_Calhoun_Analysis) OR
Get_Exp(County_18_Jackson_Analysis) OR
Get_Exp(County_37_Pleasants_Analysis) OR
Get_Exp(County_43_Ritchie_Analysis) OR
Get_Exp(County_44_Roane_Analysis) OR
Get_Exp(County_53_Wirt_Analysis) OR
Get_Exp(County_54_Wood_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NHS'
```

Original:
```text
(Get_Exp(6cfefe5f-c34c-4c4c-83f6-e04d94031603) OR
Get_Exp(1d618361-b62a-4144-9f06-579d05bb2620) OR
Get_Exp(f0fc2bac-0970-4b5c-ba79-b62351aa89cc) OR
Get_Exp(b77eedbb-d624-4547-ac35-4d2738cc1522) OR
Get_Exp(8ffd0937-cf01-4c9d-bd79-8988010e0019) OR
Get_Exp(f876f723-6937-429c-b6f1-94415ca01475) OR
Get_Exp(7cf072ec-2ecb-4da0-a341-1199e3a7c70c)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NHS'
```

<a id="e-1c41a1b4-e5c0-45f8-af29-7b9aa261cada"></a>

## DEL_District_003_Non_NHS_Database_Expression

Source: `dTIMSExpressions` / `1c41a1b4-e5c0-45f8-af29-7b9aa261cada`.

Database Expression for District 3 Non-NHS Analysis Set

Readable:
```text
(Get_Exp(County_07_Calhoun_Analysis) OR
Get_Exp(County_18_Jackson_Analysis) OR
Get_Exp(County_37_Pleasants_Analysis) OR
Get_Exp(County_43_Ritchie_Analysis) OR
Get_Exp(County_44_Roane_Analysis) OR
Get_Exp(County_53_Wirt_Analysis) OR
Get_Exp(County_54_Wood_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NON_NHS'
```

Original:
```text
(Get_Exp(6cfefe5f-c34c-4c4c-83f6-e04d94031603) OR
Get_Exp(1d618361-b62a-4144-9f06-579d05bb2620) OR
Get_Exp(f0fc2bac-0970-4b5c-ba79-b62351aa89cc) OR
Get_Exp(b77eedbb-d624-4547-ac35-4d2738cc1522) OR
Get_Exp(8ffd0937-cf01-4c9d-bd79-8988010e0019) OR
Get_Exp(f876f723-6937-429c-b6f1-94415ca01475) OR
Get_Exp(7cf072ec-2ecb-4da0-a341-1199e3a7c70c)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NON_NHS'
```

<a id="e-58cdc23a-44fe-476c-a40f-4f939e8f242c"></a>

## DEL_District_004_NHS_Database_Expression

Source: `dTIMSExpressions` / `58cdc23a-44fe-476c-a40f-4f939e8f242c`.

NHS + MISLABELED APD ROUTES.

Readable:
```text
(
    Get_Exp(County_09_Doddridge_Analysis) OR
    Get_Exp(County_17_Harrison_Analysis) OR
    Get_Exp(County_25_Marion_Analysis) OR
    Get_Exp(County_31_Monongalia_Analysis) OR
    Get_Exp(County_39_Preston_Analysis) OR
    Get_Exp(County_46_Taylor_Analysis)
) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NHS'
```

Original:
```text
(
    Get_Exp(488cb5ac-8256-4c64-86c6-da20594cc1be) OR
    Get_Exp(822a4a71-8b75-4294-8b40-7078d44d1a06) OR
    Get_Exp(44e2d8fa-27c5-4d2d-97e7-4425b0c60f16) OR
    Get_Exp(350c98b6-2e79-4895-9e9b-0b44c6a9b02f) OR
    Get_Exp(0fc8a94e-62b8-4e15-9ce1-fe3eb1bc3d13) OR
    Get_Exp(130f4ca1-6d04-410f-ada2-fe9c18041ba8)
) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NHS'
```

<a id="e-91e2863d-e079-4630-b4c0-8d7ffd9728cf"></a>

## DEL_District_004_Non_NHS_Database_Expression

Source: `dTIMSExpressions` / `91e2863d-e079-4630-b4c0-8d7ffd9728cf`.

Database Expression for District 4 Non-NHS Analysis Set

Readable:
```text
(Get_Exp(County_09_Doddridge_Analysis) OR
Get_Exp(County_17_Harrison_Analysis) OR
Get_Exp(County_25_Marion_Analysis) OR
Get_Exp(County_31_Monongalia_Analysis) OR
Get_Exp(County_39_Preston_Analysis) OR
Get_Exp(County_46_Taylor_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NON_NHS'
```

Original:
```text
(Get_Exp(488cb5ac-8256-4c64-86c6-da20594cc1be) OR
Get_Exp(822a4a71-8b75-4294-8b40-7078d44d1a06) OR
Get_Exp(44e2d8fa-27c5-4d2d-97e7-4425b0c60f16) OR
Get_Exp(350c98b6-2e79-4895-9e9b-0b44c6a9b02f) OR
Get_Exp(0fc8a94e-62b8-4e15-9ce1-fe3eb1bc3d13) OR
Get_Exp(130f4ca1-6d04-410f-ada2-fe9c18041ba8)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NON_NHS'
```

<a id="e-40271a56-6a48-4411-9e88-761afa068431"></a>

## DEL_District_005_NHS_Database_Expression

Source: `dTIMSExpressions` / `40271a56-6a48-4411-9e88-761afa068431`.

District 5 NHS (No Interstate) Routes

Readable:
```text
(Get_Exp(County_02_Berkeley_Analysis) OR
Get_Exp(County_12_Grant_Analysis) OR
Get_Exp(County_14_Hampshire_Analysis) OR
Get_Exp(County_16_Hardy_Analysis) OR
Get_Exp(County_19_Jefferson_Analysis) OR
Get_Exp(County_29_Mineral_Analysis) OR
Get_Exp(County_33_Morgan_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NHS'
```

Original:
```text
(Get_Exp(ae7f584b-a022-4bff-a227-0f603da46e5c) OR
Get_Exp(e98488b6-3307-4c2a-ad29-87b9ec978129) OR
Get_Exp(660637a0-d1b5-4bcf-a93e-e3768b313407) OR
Get_Exp(6a8d3da0-fb2c-4519-945d-c90ec974df31) OR
Get_Exp(ac55db6d-4658-449a-a2f4-48a58bf3e634) OR
Get_Exp(dbb79324-8a2a-4f9c-95e5-e9e0874b697f) OR
Get_Exp(a0b91bd6-b3fc-4d1d-b14a-ecb0820895d7)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NHS'
```

<a id="e-f81d7449-885e-402c-ad71-e2e1d1cc0a08"></a>

## DEL_District_005_Non_NHS_Database_Expression

Source: `dTIMSExpressions` / `f81d7449-885e-402c-ad71-e2e1d1cc0a08`.

Database Expression for District 5 Non-NHS Analysis Set

Readable:
```text
(Get_Exp(County_02_Berkeley_Analysis) OR
Get_Exp(County_12_Grant_Analysis) OR
Get_Exp(County_14_Hampshire_Analysis) OR
Get_Exp(County_16_Hardy_Analysis) OR
Get_Exp(County_19_Jefferson_Analysis) OR
Get_Exp(County_29_Mineral_Analysis) OR
Get_Exp(County_33_Morgan_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NON_NHS'
```

Original:
```text
(Get_Exp(ae7f584b-a022-4bff-a227-0f603da46e5c) OR
Get_Exp(e98488b6-3307-4c2a-ad29-87b9ec978129) OR
Get_Exp(660637a0-d1b5-4bcf-a93e-e3768b313407) OR
Get_Exp(6a8d3da0-fb2c-4519-945d-c90ec974df31) OR
Get_Exp(ac55db6d-4658-449a-a2f4-48a58bf3e634) OR
Get_Exp(dbb79324-8a2a-4f9c-95e5-e9e0874b697f) OR
Get_Exp(a0b91bd6-b3fc-4d1d-b14a-ecb0820895d7)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NON_NHS'
```

<a id="e-e4c8d4f9-fff1-4c71-8f2b-267e728cc26c"></a>

## DEL_District_006_NHS_Database_Expression

Source: `dTIMSExpressions` / `e4c8d4f9-fff1-4c71-8f2b-267e728cc26c`.

District 6 NHS (No Interstate) Routes

Readable:
```text
(Get_Exp(County_05_Brooke_Analysis) OR
Get_Exp(County_15_Hancock_Analysis) OR
Get_Exp(County_26_Marshall_Analysis) OR
Get_Exp(County_35_Ohio_Analysis) OR
Get_Exp(County_48_Tyler_Analysis) OR
Get_Exp(County_52_Wetzel_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NHS'
```

Original:
```text
(Get_Exp(daaeaa34-19a1-461a-9861-2ae69201fcc6) OR
Get_Exp(791c8723-395a-47fd-96f0-3e6889229ccf) OR
Get_Exp(da11c971-1b51-4ee7-a964-69221ecacc5c) OR
Get_Exp(694a98c5-ca96-4155-b30c-3d732ea253f0) OR
Get_Exp(52597624-4e31-4c80-9bea-d54f41bcfbe2) OR
Get_Exp(0bf83cf5-c243-464e-9e8a-df65dfc8e7a2)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NHS'
```

<a id="e-9ef8c395-dfc7-4fc7-9d63-db833ca059b8"></a>

## DEL_District_006_Non_NHS_Database_Expression

Source: `dTIMSExpressions` / `9ef8c395-dfc7-4fc7-9d63-db833ca059b8`.

Database Expression for District 6 Non-NHS Analysis Set

Readable:
```text
(Get_Exp(County_05_Brooke_Analysis) OR
Get_Exp(County_15_Hancock_Analysis) OR
Get_Exp(County_26_Marshall_Analysis) OR
Get_Exp(County_35_Ohio_Analysis) OR
Get_Exp(County_48_Tyler_Analysis) OR
Get_Exp(County_52_Wetzel_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NON_NHS'
```

Original:
```text
(Get_Exp(daaeaa34-19a1-461a-9861-2ae69201fcc6) OR
Get_Exp(791c8723-395a-47fd-96f0-3e6889229ccf) OR
Get_Exp(da11c971-1b51-4ee7-a964-69221ecacc5c) OR
Get_Exp(694a98c5-ca96-4155-b30c-3d732ea253f0) OR
Get_Exp(52597624-4e31-4c80-9bea-d54f41bcfbe2) OR
Get_Exp(0bf83cf5-c243-464e-9e8a-df65dfc8e7a2)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NON_NHS'
```

<a id="e-00d98fc8-9994-4c85-9349-f17245deed30"></a>

## DEL_District_007_NHS_Database_Expression

Source: `dTIMSExpressions` / `00d98fc8-9994-4c85-9349-f17245deed30`.

District 7 NHS (No Interstate) Routes

Readable:
```text
(Get_Exp(County_01_Barbour_Analysis) OR
Get_Exp(County_04_Braxton_Analysis) OR
Get_Exp(County_11_Gilmer_Analysis) OR
Get_Exp(County_21_Lewis_Analysis) OR
Get_Exp(County_49_Upshur_Analysis) OR
Get_Exp(County_51_Webster_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NHS'
```

Original:
```text
(Get_Exp(8402ff94-b794-4f69-a190-4e830560cba8) OR
Get_Exp(02c08ef4-36fa-4bdb-bda2-15fb544c6408) OR
Get_Exp(dfaa4760-2aa0-4b81-8765-8bb6ee17a943) OR
Get_Exp(d41f4888-a463-4736-a4cb-81aea6574868) OR
Get_Exp(9936b8cf-ca39-43c0-9c8d-5d0f0caddb9e) OR
Get_Exp(f634b212-1395-4ea2-976b-277f8d016467)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NHS'
```

<a id="e-db5dfdc4-b416-45d7-8d0c-a24b3f867905"></a>

## DEL_District_007_Non_NHS_Database_Expression

Source: `dTIMSExpressions` / `db5dfdc4-b416-45d7-8d0c-a24b3f867905`.

Database Expression for District 7 Non-NHS Analysis Set

Readable:
```text
(Get_Exp(County_01_Barbour_Analysis) OR
Get_Exp(County_04_Braxton_Analysis) OR
Get_Exp(County_11_Gilmer_Analysis) OR
Get_Exp(County_21_Lewis_Analysis) OR
Get_Exp(County_49_Upshur_Analysis) OR
Get_Exp(County_51_Webster_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NON_NHS'
```

Original:
```text
(Get_Exp(8402ff94-b794-4f69-a190-4e830560cba8) OR
Get_Exp(02c08ef4-36fa-4bdb-bda2-15fb544c6408) OR
Get_Exp(dfaa4760-2aa0-4b81-8765-8bb6ee17a943) OR
Get_Exp(d41f4888-a463-4736-a4cb-81aea6574868) OR
Get_Exp(9936b8cf-ca39-43c0-9c8d-5d0f0caddb9e) OR
Get_Exp(f634b212-1395-4ea2-976b-277f8d016467)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NON_NHS'
```

<a id="e-b1fec88a-c4e5-44ed-9183-75d4c756f95d"></a>

## DEL_District_008_NHS_Database_Expression

Source: `dTIMSExpressions` / `b1fec88a-c4e5-44ed-9183-75d4c756f95d`.

District 8 NHS (No Interstate) Routes

Readable:
```text
(Get_Exp(County_36_Pendleton_Analysis) OR
Get_Exp(County_38_Pocahontas_Analysis) OR
Get_Exp(County_42_Randolph_Analysis) OR
Get_Exp(County_47_Tucker_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NHS'
```

Original:
```text
(Get_Exp(4761cfd5-0b8a-418b-afec-f91f1052b6bb) OR
Get_Exp(a4de0390-bbdf-48bf-b645-71822c459873) OR
Get_Exp(5c58a6f2-81c4-49ab-b5d1-2c29ced6ee97) OR
Get_Exp(ce5aecbf-46e3-48c4-8a04-45f981cc5a58)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NHS'
```

<a id="e-c9c815c3-d26c-49a1-bc81-a204b0c8493d"></a>

## DEL_District_008_Non_NHS_Database_Expression

Source: `dTIMSExpressions` / `c9c815c3-d26c-49a1-bc81-a204b0c8493d`.

Database Expression for District 8 Non-NHS Analysis Set

Readable:
```text
(Get_Exp(County_36_Pendleton_Analysis) OR
Get_Exp(County_38_Pocahontas_Analysis) OR
Get_Exp(County_42_Randolph_Analysis) OR
Get_Exp(County_47_Tucker_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NON_NHS'
```

Original:
```text
(Get_Exp(4761cfd5-0b8a-418b-afec-f91f1052b6bb) OR
Get_Exp(a4de0390-bbdf-48bf-b645-71822c459873) OR
Get_Exp(5c58a6f2-81c4-49ab-b5d1-2c29ced6ee97) OR
Get_Exp(ce5aecbf-46e3-48c4-8a04-45f981cc5a58)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NON_NHS'
```

<a id="e-6cd0cd44-dc64-413c-a73a-f2223163e991"></a>

## DEL_District_009_NHS_Database_Expression

Source: `dTIMSExpressions` / `6cd0cd44-dc64-413c-a73a-f2223163e991`.

District 9 NHS (No Interstate) Routes

Readable:
```text
(Get_Exp(County_10_Fayette_Analysis) OR
Get_Exp(County_13_Greenbrier_Analysis) OR
Get_Exp(County_32_Monroe_Analysis) OR
Get_Exp(County_34_Nicholas_Analysis) OR
Get_Exp(County_45_Summers_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NHS'
```

Original:
```text
(Get_Exp(f4453a9e-3ffc-4e48-beb8-4783f3828cc1) OR
Get_Exp(5b27eace-88fe-41b4-b5d3-da9b6d4e7893) OR
Get_Exp(9687e769-3776-4722-ab54-778fc2ac780f) OR
Get_Exp(20ed539d-a664-4dfa-ad79-05e726fd97cb) OR
Get_Exp(819e0dfc-edaa-4550-a250-648560c30e98)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NHS'
```

<a id="e-4709b919-7ce7-4c37-aaf3-52d130015a34"></a>

## DEL_District_009_Non_NHS_Database_Expression

Source: `dTIMSExpressions` / `4709b919-7ce7-4c37-aaf3-52d130015a34`.

Database Expression for District 9 Non-NHS Analysis Set

Readable:
```text
(Get_Exp(County_10_Fayette_Analysis) OR
Get_Exp(County_13_Greenbrier_Analysis) OR
Get_Exp(County_32_Monroe_Analysis) OR
Get_Exp(County_34_Nicholas_Analysis) OR
Get_Exp(County_45_Summers_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NON_NHS'
```

Original:
```text
(Get_Exp(f4453a9e-3ffc-4e48-beb8-4783f3828cc1) OR
Get_Exp(5b27eace-88fe-41b4-b5d3-da9b6d4e7893) OR
Get_Exp(9687e769-3776-4722-ab54-778fc2ac780f) OR
Get_Exp(20ed539d-a664-4dfa-ad79-05e726fd97cb) OR
Get_Exp(819e0dfc-edaa-4550-a250-648560c30e98)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NON_NHS'
```

<a id="e-3c0275b8-d567-48c6-97e3-c996ff408f40"></a>

## DEL_District_010_NHS_Database_Expression

Source: `dTIMSExpressions` / `3c0275b8-d567-48c6-97e3-c996ff408f40`.

District 10 NHS (No Interstate) Routes

Readable:
```text
(Get_Exp(County_24_McDowell_Analysis) OR
Get_Exp(County_28_Mercer_Analysis) OR
Get_Exp(County_41_Raleigh_Analysis) OR
Get_Exp(County_55_Wyoming_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NHS'
```

Original:
```text
(Get_Exp(44d7a61b-6e4f-4e2b-9043-b3149c4f1547) OR
Get_Exp(34789d4e-1b4e-4943-9961-8b3efa31847d) OR
Get_Exp(a8d54937-e5b8-443b-b005-17a8de8da907) OR
Get_Exp(1ba5e7aa-a1fa-455f-a4aa-230a455cf35a)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NHS'
```

<a id="e-fe33241b-45e8-4b2b-8e8a-bbed58b31741"></a>

## DEL_District_010_Non_NHS_Database_Expression

Source: `dTIMSExpressions` / `fe33241b-45e8-4b2b-8e8a-bbed58b31741`.

Database Expression for District 10 Non-NHS Analysis Set

Readable:
```text
(Get_Exp(County_24_McDowell_Analysis) OR
Get_Exp(County_28_Mercer_Analysis) OR
Get_Exp(County_41_Raleigh_Analysis) OR
Get_Exp(County_55_Wyoming_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NON_NHS'
```

Original:
```text
(Get_Exp(44d7a61b-6e4f-4e2b-9043-b3149c4f1547) OR
Get_Exp(34789d4e-1b4e-4943-9961-8b3efa31847d) OR
Get_Exp(a8d54937-e5b8-443b-b005-17a8de8da907) OR
Get_Exp(1ba5e7aa-a1fa-455f-a4aa-230a455cf35a)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NON_NHS'
```

<a id="e-90b0557e-bbc6-4630-9399-3f92d8361038"></a>

## DEL_District_10_Database_Expression

Source: `dTIMSExpressions` / `90b0557e-bbc6-4630-9399-3f92d8361038`.

Database Expression for District 10 Analysis Set

Readable:
```text
(Get_Exp(County_24_McDowell_Analysis) OR
Get_Exp(County_28_Mercer_Analysis) OR
Get_Exp(County_41_Raleigh_Analysis) OR
Get_Exp(County_55_Wyoming_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NON_NHS'
```

Original:
```text
(Get_Exp(44d7a61b-6e4f-4e2b-9043-b3149c4f1547) OR
Get_Exp(34789d4e-1b4e-4943-9961-8b3efa31847d) OR
Get_Exp(a8d54937-e5b8-443b-b005-17a8de8da907) OR
Get_Exp(1ba5e7aa-a1fa-455f-a4aa-230a455cf35a)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NON_NHS'
```

<a id="e-9f7666d2-dc9b-4795-9766-1f582e509a8e"></a>

## DEL_District_4_Database_Expression

Source: `dTIMSExpressions` / `9f7666d2-dc9b-4795-9766-1f582e509a8e`.

Database Expression for District 4 Analysis Set

Readable:
```text
(Get_Exp(County_09_Doddridge_Analysis) OR
Get_Exp(County_17_Harrison_Analysis) OR
Get_Exp(County_25_Marion_Analysis) OR
Get_Exp(County_31_Monongalia_Analysis) OR
Get_Exp(County_39_Preston_Analysis) OR
Get_Exp(County_46_Taylor_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NON_NHS'

```

Original:
```text
(Get_Exp(488cb5ac-8256-4c64-86c6-da20594cc1be) OR
Get_Exp(822a4a71-8b75-4294-8b40-7078d44d1a06) OR
Get_Exp(44e2d8fa-27c5-4d2d-97e7-4425b0c60f16) OR
Get_Exp(350c98b6-2e79-4895-9e9b-0b44c6a9b02f) OR
Get_Exp(0fc8a94e-62b8-4e15-9ce1-fe3eb1bc3d13) OR
Get_Exp(130f4ca1-6d04-410f-ada2-fe9c18041ba8)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NON_NHS'

```

<a id="e-4299044c-eb0c-4c9c-82a8-29ba5ab88e66"></a>

## DEL_District_5_Database_Expression

Source: `dTIMSExpressions` / `4299044c-eb0c-4c9c-82a8-29ba5ab88e66`.

Database Expression for District 5 Analysis Set

Readable:
```text
(Get_Exp(County_02_Berkeley_Analysis) OR
Get_Exp(County_12_Grant_Analysis) OR
Get_Exp(County_14_Hampshire_Analysis) OR
Get_Exp(County_16_Hardy_Analysis) OR
Get_Exp(County_19_Jefferson_Analysis) OR
Get_Exp(County_29_Mineral_Analysis) OR
Get_Exp(County_33_Morgan_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NON_NHS'
```

Original:
```text
(Get_Exp(ae7f584b-a022-4bff-a227-0f603da46e5c) OR
Get_Exp(e98488b6-3307-4c2a-ad29-87b9ec978129) OR
Get_Exp(660637a0-d1b5-4bcf-a93e-e3768b313407) OR
Get_Exp(6a8d3da0-fb2c-4519-945d-c90ec974df31) OR
Get_Exp(ac55db6d-4658-449a-a2f4-48a58bf3e634) OR
Get_Exp(dbb79324-8a2a-4f9c-95e5-e9e0874b697f) OR
Get_Exp(a0b91bd6-b3fc-4d1d-b14a-ecb0820895d7)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NON_NHS'
```

<a id="e-faf3caa9-b3c5-4db2-b81a-34650bb1576b"></a>

## DEL_District_6_Database_Expression

Source: `dTIMSExpressions` / `faf3caa9-b3c5-4db2-b81a-34650bb1576b`.

Database Expression for District 6 Analysis Set

Readable:
```text
(Get_Exp(County_05_Brooke_Analysis) OR
Get_Exp(County_15_Hancock_Analysis) OR
Get_Exp(County_26_Marshall_Analysis) OR
Get_Exp(County_35_Ohio_Analysis) OR
Get_Exp(County_48_Tyler_Analysis) OR
Get_Exp(County_52_Wetzel_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NON_NHS'
```

Original:
```text
(Get_Exp(daaeaa34-19a1-461a-9861-2ae69201fcc6) OR
Get_Exp(791c8723-395a-47fd-96f0-3e6889229ccf) OR
Get_Exp(da11c971-1b51-4ee7-a964-69221ecacc5c) OR
Get_Exp(694a98c5-ca96-4155-b30c-3d732ea253f0) OR
Get_Exp(52597624-4e31-4c80-9bea-d54f41bcfbe2) OR
Get_Exp(0bf83cf5-c243-464e-9e8a-df65dfc8e7a2)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NON_NHS'
```

<a id="e-a84a6f46-6760-46e7-8980-4038e1eb8c6d"></a>

## DEL_District_7_Database_Expression

Source: `dTIMSExpressions` / `a84a6f46-6760-46e7-8980-4038e1eb8c6d`.

Database Expression for District 7 Analysis Set

Readable:
```text
(Get_Exp(County_01_Barbour_Analysis) OR
Get_Exp(County_04_Braxton_Analysis) OR
Get_Exp(County_11_Gilmer_Analysis) OR
Get_Exp(County_21_Lewis_Analysis) OR
Get_Exp(County_49_Upshur_Analysis) OR
Get_Exp(County_51_Webster_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NON_NHS'
```

Original:
```text
(Get_Exp(8402ff94-b794-4f69-a190-4e830560cba8) OR
Get_Exp(02c08ef4-36fa-4bdb-bda2-15fb544c6408) OR
Get_Exp(dfaa4760-2aa0-4b81-8765-8bb6ee17a943) OR
Get_Exp(d41f4888-a463-4736-a4cb-81aea6574868) OR
Get_Exp(9936b8cf-ca39-43c0-9c8d-5d0f0caddb9e) OR
Get_Exp(f634b212-1395-4ea2-976b-277f8d016467)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NON_NHS'
```

<a id="e-d80fec5e-be9e-4885-8cc4-c38e366492a1"></a>

## DEL_District_8_Database_Expression

Source: `dTIMSExpressions` / `d80fec5e-be9e-4885-8cc4-c38e366492a1`.

Database Expression for District 8 Analysis Set

Readable:
```text
(Get_Exp(County_36_Pendleton_Analysis) OR
Get_Exp(County_38_Pocahontas_Analysis) OR
Get_Exp(County_42_Randolph_Analysis) OR
Get_Exp(County_47_Tucker_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NON_NHS'
```

Original:
```text
(Get_Exp(4761cfd5-0b8a-418b-afec-f91f1052b6bb) OR
Get_Exp(a4de0390-bbdf-48bf-b645-71822c459873) OR
Get_Exp(5c58a6f2-81c4-49ab-b5d1-2c29ced6ee97) OR
Get_Exp(ce5aecbf-46e3-48c4-8a04-45f981cc5a58)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NON_NHS'
```

<a id="e-7fbb56d4-3391-48fa-bff9-37b7dbb31973"></a>

## DEL_District_9_Database_Expression

Source: `dTIMSExpressions` / `7fbb56d4-3391-48fa-bff9-37b7dbb31973`.

Database Expression for District 9 Analysis Set

Readable:
```text
(Get_Exp(County_10_Fayette_Analysis) OR
Get_Exp(County_13_Greenbrier_Analysis) OR
Get_Exp(County_32_Monroe_Analysis) OR
Get_Exp(County_34_Nicholas_Analysis) OR
Get_Exp(County_45_Summers_Analysis)) AND
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NON_NHS'
```

Original:
```text
(Get_Exp(f4453a9e-3ffc-4e48-beb8-4783f3828cc1) OR
Get_Exp(5b27eace-88fe-41b4-b5d3-da9b6d4e7893) OR
Get_Exp(9687e769-3776-4722-ab54-778fc2ac780f) OR
Get_Exp(20ed539d-a664-4dfa-ad79-05e726fd97cb) OR
Get_Exp(819e0dfc-edaa-4550-a250-648560c30e98)) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NON_NHS'
```

<a id="e-13904bd2-6a40-406e-a508-273c64d90e69"></a>

## DEL_Entire_WV_Roadway_Network_Database_Expression

Source: `dTIMSExpressions` / `13904bd2-6a40-406e-a508-273c64d90e69`.

Database Expression for entire WV Roadway Network.  All Interstates, APD's, NHS, and Non-NHS Routes (No Turnpike)

Readable:
```text
Get_Exp(DEL_INTERSTATES) OR
Get_Exp(DEL_APD) OR
Get_Exp(DEL_NHS) OR
Get_Exp(DEL_District_001_Non_NHS_Database_Expression) OR
Get_Exp(DEL_District_002_Non_NHS_Database_Expression) OR
Get_Exp(DEL_District_4_Database_Expression) OR
Get_Exp(DEL_District_5_Database_Expression) OR
Get_Exp(DEL_District_6_Database_Expression) OR
Get_Exp(DEL_District_7_Database_Expression) OR
Get_Exp(DEL_District_8_Database_Expression) OR
Get_Exp(DEL_District_9_Database_Expression) OR
Get_Exp(DEL_District_10_Database_Expression) AND
Get_Field(Length)>=Get_Number(0.5)
```

Original:
```text
Get_Exp(1388bd80-c1cd-464d-826b-3bc859d85e4d) OR
Get_Exp(1fe2f8d3-ae39-446f-9f02-c05c851d10e5) OR
Get_Exp(00ff6471-2cf4-49cd-a7bb-86d83c082dd4) OR
Get_Exp(95087272-914d-40ed-b54f-aaf1be90ab06) OR
Get_Exp(31a563ea-5e4c-46dc-bad5-596d6457eeea) OR
Get_Exp(9f7666d2-dc9b-4795-9766-1f582e509a8e) OR
Get_Exp(4299044c-eb0c-4c9c-82a8-29ba5ab88e66) OR
Get_Exp(faf3caa9-b3c5-4db2-b81a-34650bb1576b) OR
Get_Exp(a84a6f46-6760-46e7-8980-4038e1eb8c6d) OR
Get_Exp(d80fec5e-be9e-4885-8cc4-c38e366492a1) OR
Get_Exp(7fbb56d4-3391-48fa-bff9-37b7dbb31973) OR
Get_Exp(90b0557e-bbc6-4630-9399-3f92d8361038) AND
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>=Get_Number(0.5)
```

<a id="e-1388bd80-c1cd-464d-826b-3bc859d85e4d"></a>

## DEL_INTERSTATES

Source: `dTIMSExpressions` / `1388bd80-c1cd-464d-826b-3bc859d85e4d`.

Analysis Sections for Interstate

Readable:
```text
Get_Exp(PMS_abfOBJ_Valid_Analysis_Section) AND Get_Exp(PMS_abfOBJ_IM_Funds) AND Get_Field(Lane) = Get_Number(1)
```

Original:
```text
Get_Exp(d7d1be3c-b7bc-4ff7-b551-6f8730fbb39c) AND Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7) AND Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1)
```

<a id="e-90b14ebc-d9ce-4101-bc05-3c906d157f29"></a>

## DEL_InterstateAnalysis_2023_03_22

Source: `dTIMSExpressions` / `90b14ebc-d9ce-4101-bc05-3c906d157f29`.

Analysis Sections for Interstate

Readable:
```text
Get_Exp(PMS_abfOBJ_Valid_Analysis_Section) AND 
Get_Exp(DEL_INTERSTATES)
AND Get_Field(Lane) = Get_Number(1)
```

Original:
```text
Get_Exp(d7d1be3c-b7bc-4ff7-b551-6f8730fbb39c) AND 
Get_Exp(1388bd80-c1cd-464d-826b-3bc859d85e4d)
AND Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1)
```

<a id="e-da016672-c63b-49d0-815f-78d7af33c91d"></a>

## DEL_Minimum_Cost_Allowable_PSI

Source: `dTIMSExpressions` / `da016672-c63b-49d0-815f-78d7af33c91d`.

Tells dTIMS what strats are acceptable based on PSI for the minimum cost analysis.

Readable:
```text

//modified April 11, 2025 to allow shorter analysis periods.
//next time a minimum cost optimization is executed, we will need to fix this.
TRUE
//GET_ANALVAR_4_YR(PMS_nAAV_CND_PSI,10)>=4.0 AND
//GET_ANALVAR_4_YR(PMS_nAAV_CND_PSI,9)>=4.0 AND
//GET_ANALVA
```

Original:
```text

//modified April 11, 2025 to allow shorter analysis periods.
//next time a minimum cost optimization is executed, we will need to fix this.
TRUE
//GET_ANALVAR_4_YR(PMS_nAAV_CND_PSI,10)>=4.0 AND
//GET_ANALVAR_4_YR(PMS_nAAV_CND_PSI,9)>=4.0 AND
//GET_ANALVA
```

<a id="e-00ff6471-2cf4-49cd-a7bb-86d83c082dd4"></a>

## DEL_NHS

Source: `dTIMSExpressions` / `00ff6471-2cf4-49cd-a7bb-86d83c082dd4`.

NHS + MISLABELED APD ROUTES.

Readable:
```text
Get_Exp(PMS_abfOBJ_Valid_Analysis_Section) AND (LEFT(Get_Field(Fed_Aid),Get_Number(1))='2' OR LEFT(Get_Field(Fed_Aid),Get_Number(1))='4') AND (NOT   Get_Exp(PMS_abfOBJ_IM_Funds))


//PMS_abfOBJ_Valid_Analysis_Section AND
//((Analysis->Fed_Aid='2' 
//AND (NOT    DEL_APD) 
//AND (NOT    PMS_abfOBJ_IM_Funds)) OR
//DEL_NHS_MISLABELED_APD_ROUTES)

```

Original:
```text
Get_Exp(d7d1be3c-b7bc-4ff7-b551-6f8730fbb39c) AND (LEFT(Get_Field(e8613014-fa1e-4da2-ae75-c77b722d9c37),Get_Number(1))='2' OR LEFT(Get_Field(e8613014-fa1e-4da2-ae75-c77b722d9c37),Get_Number(1))='4') AND (NOT   Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7))


//PMS_abfOBJ_Valid_Analysis_Section AND
//((Analysis->Fed_Aid='2' 
//AND (NOT    DEL_APD) 
//AND (NOT    PMS_abfOBJ_IM_Funds)) OR
//DEL_NHS_MISLABELED_APD_ROUTES)

```

<a id="e-7405dd33-0dfd-4c13-9b8a-a4e0e661af5e"></a>

## DEL_NHS_MISLABELED_APD_ROUTES

Source: `dTIMSExpressions` / `7405dd33-0dfd-4c13-9b8a-a4e0e661af5e`.

Routes that are tagged APD but are not.

Readable:
```text
(Get_Field(Name)='1630055000000-011.090-1' OR 
Get_Field(Name)='1230093000000-001.540-1' OR 
Get_Field(Name)='1630055000000-034.150-1' OR
Get_Field(Name)='4730032000000-010.400-1' OR
Get_Field(Name)='4730032000000-014.790-1' OR
Get_Field(Name)='4730093000000-000.000-1' OR
Get_Field(Name)='42200330000EB-007.900-1' OR
Get_Field(Name)='42202190000NB-045.700-1' OR
Get_Field(Name)='42202190000NB-047.500-1' OR
Get_Field(Name)='47202190000NB-000.000-1' OR
Get_Field(Name)='47202190000NB-009.000-1') 
```

Original:
```text
(Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='1630055000000-011.090-1' OR 
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='1230093000000-001.540-1' OR 
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='1630055000000-034.150-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='4730032000000-010.400-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='4730032000000-014.790-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='4730093000000-000.000-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='42200330000EB-007.900-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='42202190000NB-045.700-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='42202190000NB-047.500-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='47202190000NB-000.000-1' OR
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='47202190000NB-009.000-1') 
```

<a id="e-028ef125-310a-4e0d-ad9b-8b2eca64c5e1"></a>

## DEL_Non_NHS_Routes_Data_Base_Expression

Source: `dTIMSExpressions` / `028ef125-310a-4e0d-ad9b-8b2eca64c5e1`.

Database Expression for District 1 Non-NHS Analysis Set

Readable:
```text
Get_Field(Length)>= IF(Get_Field(Com_Year)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(TAMP_CLASS) = 'NON_NHS'
```

Original:
```text
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)>= IF(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>Get_Number(0),Get_Number(0),Get_Number(1)) AND
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NON_NHS'
```

<a id="e-2bf30be5-2e0e-45ec-885d-e43b3ca73acf"></a>

## DEL_STIP_ROUTES

Source: `dTIMSExpressions` / `2bf30be5-2e0e-45ec-885d-e43b3ca73acf`.

Created this on 9/3/2024 after BMS/ PMS Meeting for STIP Routes ID's.  To be provided by Chris Kessel upcoming.

Readable:
```text
(Get_Field(Name)='04100790000NB-044.600-1') OR
(Get_Field(Name)=Get_Number(4100790000)-Get_Number(53.9)-Get_Number(1))

```

Original:
```text
(Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='04100790000NB-044.600-1') OR
(Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)=Get_Number(4100790000)-Get_Number(53.9)-Get_Number(1))

```

<a id="e-e08e76fd-343b-4c5f-b129-a754c27806af"></a>

## DEL_dFRAG_ATTEMPT

Source: `dTIMSExpressions` / `e08e76fd-343b-4c5f-b129-a754c27806af`.



Readable:
```text
IF(Get_Field(IRI_MEAN)>Get_Number(170),'POOR',
IF(Get_Field(IRI_MEAN)<Get_Number(171) AND Get_Field(IRI_MEAN)>Get_Number(95),'FAIR',
'GOOD'))
```

Original:
```text
IF(Get_Field(ef70c8d6-cd41-494d-9a98-59f2ef40aa4b)>Get_Number(170),'POOR',
IF(Get_Field(ef70c8d6-cd41-494d-9a98-59f2ef40aa4b)<Get_Number(171) AND Get_Field(ef70c8d6-cd41-494d-9a98-59f2ef40aa4b)>Get_Number(95),'FAIR',
'GOOD'))
```

<a id="e-11d2cf14-42d0-4f24-a84d-e0c58b6f9105"></a>

## GIS_02_Bridge_Expression_At_Numeric

Source: `dTIMSExpressions` / `11d2cf14-42d0-4f24-a84d-e0c58b6f9105`.

At fix as a number for Bridge table and GIS Integration 02

Readable:
```text
IF(LTRIM(RTRIM(Get_Field(Name))) = '05A088' OR 
    LTRIM(RTRIM(Get_Field(Name))) = '20A292' OR 
    LTRIM(RTRIM(Get_Field(Name))) = '20A363' OR 
    LTRIM(RTRIM(Get_Field(Name))) = '24A391' OR 
    LTRIM(RTRIM(Get_Field(Name))) = '31A160' OR 
    LTRIM(RTRIM(Get_Field(Name))) = '31A337' OR 
    LTRIM(RTRIM(Get_Field(Name))) = '44A065' OR 
    LTRIM(RTRIM(Get_Field(Name))) = '44A191' OR 
    LTRIM(RTRIM(Get_Field(Name))) = '45A072' OR 
    LTRIM(RTRIM(Get_Field(Name))) = '54A039' OR
    LTRIM(RTRIM(Get_Field(Name))) = '54A907' OR
    LTRIM(RTRIM(Get_Field(Name))) = '55A111' OR
    LTRIM(RTRIM(Get_Field(Name))) = '55X002'
,
    Get_Field(At) + Get_Number(0.1)
,
    Get_Field(At)
)
```

Original:
```text
IF(LTRIM(RTRIM(Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5))) = '05A088' OR 
    LTRIM(RTRIM(Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5))) = '20A292' OR 
    LTRIM(RTRIM(Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5))) = '20A363' OR 
    LTRIM(RTRIM(Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5))) = '24A391' OR 
    LTRIM(RTRIM(Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5))) = '31A160' OR 
    LTRIM(RTRIM(Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5))) = '31A337' OR 
    LTRIM(RTRIM(Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5))) = '44A065' OR 
    LTRIM(RTRIM(Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5))) = '44A191' OR 
    LTRIM(RTRIM(Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5))) = '45A072' OR 
    LTRIM(RTRIM(Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5))) = '54A039' OR
    LTRIM(RTRIM(Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5))) = '54A907' OR
    LTRIM(RTRIM(Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5))) = '55A111' OR
    LTRIM(RTRIM(Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5))) = '55X002'
,
    Get_Field(fb5537e8-9dbb-4861-932c-248d8b4f2af4) + Get_Number(0.1)
,
    Get_Field(fb5537e8-9dbb-4861-932c-248d8b4f2af4)
)
```

<a id="e-20a6b852-94fa-4074-b74d-6ef65a7dfcb5"></a>

## GIS_02_Bridge_Expression_Roadname

Source: `dTIMSExpressions` / `20a6b852-94fa-4074-b74d-6ef65a7dfcb5`.

Fix Roadname for bridges that need to be put on zROAD

Readable:
```text
IF(Get_Field(Name) = '01A011' OR 
    Get_Field(Name) = '10A129' OR 
    Get_Field(Name) = '20A400' OR 
    Get_Field(Name) = '20A345' OR 
    Get_Field(Name) = '24A007' OR 
    Get_Field(Name) = '27A109' OR 
    Get_Field(Name) = '29A087' OR 
    Get_Field(Name) = '30A184' OR 
    Get_Field(Name) = '31A159' OR 
    Get_Field(Name) = '31A160' OR 
    Get_Field(Name) = '31A905' OR 
    Get_Field(Name) = '31A906' OR 
    Get_Field(Name) = '33A079' OR 
    Get_Field(Name) = '37A015' OR 
    Get_Field(Name) = '40A162' OR 
    Get_Field(Name) = '45A072' OR 
    Get_Field(Name) = '45A073' OR 
    Get_Field(Name) = '50A136' OR 
    Get_Field(Name) = '50A121' OR 
    Get_Field(Name) = '54A169' OR 
    Get_Field(Name) = '54A260' OR 
    Get_Field(Name) = '01A100' OR 
    Get_Field(Name) = '20A534' OR 
    Get_Field(Name) = '20A399' OR 
    Get_Field(Name) = '30A240' OR 
    Get_Field(Name) = '41A234' OR
	Get_Field(Name) = '10A209' OR
	Get_Field(Name) = '23A361' OR
	Get_Field(Name) = '23A376' OR
	Get_Field(Name) = '23A378' OR
	Get_Field(Name) = '23A353' OR
	Get_Field(Name) = '39A901' OR
	Get_Field(Name) = '41A309' OR
	Get_Field(Name) = '02A152' OR
	Get_Field(Name) = '05A088' OR
	Get_Field(Name) = '08A054' OR
	Get_Field(Name) = '10A079' OR
	Get_Field(Name) = '10A295' OR
	Get_Field(Name) = '20A951' OR
	Get_Field(Name) = '20A545' OR
	Get_Field(Name) = '20A952' OR
	Get_Field(Name) = '21A227' OR
	Get_Field(Name) = '23A071' OR
	Get_Field(Name) = '27A180' OR
	Get_Field(Name) = '28A324' OR
	Get_Field(Name) = '28A346' OR
	Get_Field(Name) = '28A347' OR
	Get_Field(Name) = '28A313' OR
	Get_Field(Name) = '28A325' OR
	Get_Field(Name) = '41A237' OR
	Get_Field(Name) = '41A238' OR
	Get_Field(Name) = '41A266' OR
	Get_Field(Name) = '43A196' OR
	Get_Field(Name) = '43A133' OR
	Get_Field(Name) = '44A065' OR
	Get_Field(Name) = '52A028'
,
    'zROAD'
,
Get_Field(RoadName)
)

```

Original:
```text
IF(Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '01A011' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '10A129' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '20A400' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '20A345' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '24A007' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '27A109' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '29A087' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '30A184' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '31A159' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '31A160' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '31A905' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '31A906' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '33A079' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '37A015' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '40A162' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '45A072' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '45A073' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '50A136' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '50A121' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '54A169' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '54A260' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '01A100' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '20A534' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '20A399' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '30A240' OR 
    Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '41A234' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '10A209' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '23A361' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '23A376' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '23A378' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '23A353' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '39A901' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '41A309' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '02A152' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '05A088' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '08A054' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '10A079' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '10A295' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '20A951' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '20A545' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '20A952' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '21A227' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '23A071' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '27A180' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '28A324' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '28A346' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '28A347' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '28A313' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '28A325' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '41A237' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '41A238' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '41A266' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '43A196' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '43A133' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '44A065' OR
	Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '52A028'
,
    'zROAD'
,
Get_Field(e51a2f79-7d5c-456b-848e-18295b9df678)
)

```

<a id="e-f3f18d91-5e37-4582-a05a-4ab67c1264c9"></a>

## HPMS_Length

Source: `dTIMSExpressions` / `f3f18d91-5e37-4582-a05a-4ab67c1264c9`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(28dc2d35-b7d1-43c2-9c05-abd0038df767) - Get_Field(b25a49b0-8da7-4c12-923a-4d4ad84e8b72)
```

<a id="e-597691c3-522b-4e89-af5c-291d52c6ea86"></a>

## History_Combined_Rehab_Length

Source: `dTIMSExpressions` / `597691c3-522b-4e89-af5c-291d52c6ea86`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(407f11b0-b9ab-469f-95ff-7f64b21d2374) - Get_Field(119f817c-9f11-439a-ac57-5bfaf75f97cc)
```

<a id="e-756f1d8e-2c2d-4686-b286-6fe8d10db45d"></a>

## History_Combined_Rehab_Most_Recent_Length

Source: `dTIMSExpressions` / `756f1d8e-2c2d-4686-b286-6fe8d10db45d`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(6ab2aedd-9253-4b3c-9813-ae46599d79ca) - Get_Field(82b3c40c-2922-4321-8836-2951f5f2ecd8)
```

<a id="e-02432edd-3632-4599-81ca-a6e72abd42bf"></a>

## NHS_XLXS_Length

Source: `dTIMSExpressions` / `02432edd-3632-4599-81ca-a6e72abd42bf`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(c730e5c0-1e7b-4dde-a83b-0867da1c0a56) - Get_Field(7cb92cbf-d493-40db-8ef7-a4a77dca529b)
```

<a id="e-22866c66-a014-45f3-966e-f7b30471141b"></a>

## New497

Source: `dTIMSExpressions` / `22866c66-a014-45f3-966e-f7b30471141b`.



Readable:
```text
Get_Number(0)
```

Original:
```text
Get_Number(0)
```

<a id="e-0ae0a72c-3da2-42a6-a329-33927c3123a3"></a>

## New993

Source: `dTIMSExpressions` / `0ae0a72c-3da2-42a6-a329-33927c3123a3`.



Readable:
```text
IF(Get_Exp(PMS_ancOBJ_Pave_type_Initial) = 'BC', MIN(IF(Get_Field(ECI)>Get_Number(0),Get_Field(ECI),Get_Number(99)), MIN(IF(Get_Field(PSI)>Get_Number(0),Get_Field(PSI),Get_Number(99)), MIN(IF(Get_Field(RDI)>Get_Number(0),Get_Field(RDI),Get_Number(99)), IF(Get_Field(SCI)>Get_Number(0),Get_Field(SCI),Get_Number(99))) ) ), IF(Get_Exp(PMS_ancOBJ_Pave_type_Initial) = 'RC', MIN(IF(Get_Field(CSI)>Get_Number(0),Get_Field(CSI),Get_Number(99)), MIN(IF(Get_Field(JCI)>Get_Number(0),Get_Field(JCI),Get_Number(99)), IF(Get_Field(PSI)>Get_Number(0),Get_Field(PSI),Get_Number(99))) ) , -Get_Number(1)) )
```

Original:
```text
IF(Get_Exp(09c7fde6-cc65-4701-9ecc-e3e705983d08) = 'BC', MIN(IF(Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>Get_Number(0),Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4),Get_Number(99)), MIN(IF(Get_Field(1eca4d42-a141-4b12-8457-f11b987a6710)>Get_Number(0),Get_Field(1eca4d42-a141-4b12-8457-f11b987a6710),Get_Number(99)), MIN(IF(Get_Field(be1a4d5a-ea19-4e1a-a61d-c1b792828006)>Get_Number(0),Get_Field(be1a4d5a-ea19-4e1a-a61d-c1b792828006),Get_Number(99)), IF(Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>Get_Number(0),Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04),Get_Number(99))) ) ), IF(Get_Exp(09c7fde6-cc65-4701-9ecc-e3e705983d08) = 'RC', MIN(IF(Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5)>Get_Number(0),Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5),Get_Number(99)), MIN(IF(Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050)>Get_Number(0),Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050),Get_Number(99)), IF(Get_Field(1eca4d42-a141-4b12-8457-f11b987a6710)>Get_Number(0),Get_Field(1eca4d42-a141-4b12-8457-f11b987a6710),Get_Number(99))) ) , -Get_Number(1)) )
```

<a id="e-8b1e2da5-ae16-44a8-9152-211013c96408"></a>

## NoTurnpike

Source: `dTIMSExpressions` / `8b1e2da5-ae16-44a8-9152-211013c96408`.

Turnpike excluded from analysis


Readable:
```text
LEFT(Get_Field(c7a4dd0d-cfe2-4d16-900a-c16bd6142654),Get_Number(3)) <> 'S03'
//Bridge->OWNER <> '31'
```

Original:
```text
LEFT(Get_Field(c7a4dd0d-cfe2-4d16-900a-c16bd6142654),Get_Number(3)) <> 'S03'
//Bridge->OWNER <> '31'
```

<a id="e-0dfe7497-ea82-47a8-87ca-239def1b0b07"></a>

## PMS_EXP_AADT_YEAR_NUMERIC

Source: `dTIMSExpressions` / `0dfe7497-ea82-47a8-87ca-239def1b0b07`.

Convert AADT Year to a number

Readable:
```text
VAL(Get_Field(AADT_YEAR))
```

Original:
```text
VAL(Get_Field(a4c5b335-a108-4b56-87ed-845e3183670b))
```

<a id="e-95efa0ab-4761-42a4-b4c1-8fd14954e36f"></a>

## PMS_EXP_BaseFromEdit

Source: `dTIMSExpressions` / `95efa0ab-4761-42a4-b4c1-8fd14954e36f`.

Change From for 41300030000WB: 40.461000, 2330010000000: 38.440000

Readable:
```text
IF(Get_Field(Name) = '41300030000WB', ROUND(Get_Field(From),Get_Number(3)),
IF(Get_Field(Name) = '2330010000000', ROUND(Get_Field(From),Get_Number(3)),
Get_Field(From)))

```

Original:
```text
IF(Get_Field(8bb1e67c-c8e7-453a-bdc5-ed14912d0594) = '41300030000WB', ROUND(Get_Field(8b3a09b6-a8f1-429f-927d-32f2d5d501a6),Get_Number(3)),
IF(Get_Field(8bb1e67c-c8e7-453a-bdc5-ed14912d0594) = '2330010000000', ROUND(Get_Field(8b3a09b6-a8f1-429f-927d-32f2d5d501a6),Get_Number(3)),
Get_Field(8b3a09b6-a8f1-429f-927d-32f2d5d501a6)))

```

<a id="e-6a7fe45e-da93-4828-bb72-bb1024709eee"></a>

## PMS_EXP_ESAL_Annual

Source: `RuntimeExpressions` / `6a7fe45e-da93-4828-bb72-bb1024709eee`.

Calculates ESALs

Readable:
```text
IF(TRUE,Get_Number(0),
IF(Get_Field(Avg_Truck_Per) < Get_Number(0) OR Get_Field(ADT_20_Yr_Factor) < Get_Number(0) OR Get_Field(ADT) < Get_Number(0) OR Get_Field(ESAL_Factor) < Get_Number(0), -Get_Number(1), ( ( ( Get_Field(Avg_Truck_Per)/Get_Number(100)) * ( ( Get_Field(ADT_20_Yr_Factor) * ( GET_ANALVR(PMS_nAAV_TRF_ADT) / Get_Number(2)) ) + ( GET_ANALVR(PMS_nAAV_TRF_ADT) / Get_Number(2)) ) / Get_Number(2))  * Get_Number(20) * Get_Number(365)) * Get_Field(ESAL_Factor))
)
```

Original:
```text
IF(TRUE,Get_Number(0),
IF(Get_Field(70867d8a-ae65-4c30-a015-fd1290026be2) < Get_Number(0) OR Get_Field(1b880838-6c85-436b-98cc-c91b317e5c16) < Get_Number(0) OR Get_Field(8c63c2ca-4d7c-41c5-8632-e26685bf488e) < Get_Number(0) OR Get_Field(55a8237e-400d-4d29-9fe1-04405db7883a) < Get_Number(0), -Get_Number(1), ( ( ( Get_Field(70867d8a-ae65-4c30-a015-fd1290026be2)/Get_Number(100)) * ( ( Get_Field(1b880838-6c85-436b-98cc-c91b317e5c16) * ( GET_ANALVR(674cee68-8d0f-4f42-8ec1-227bcc6bb6a4) / Get_Number(2)) ) + ( GET_ANALVR(674cee68-8d0f-4f42-8ec1-227bcc6bb6a4) / Get_Number(2)) ) / Get_Number(2))  * Get_Number(20) * Get_Number(365)) * Get_Field(55a8237e-400d-4d29-9fe1-04405db7883a))
)
```

<a id="e-0c6232ef-4b03-4282-9cb6-0f89e472f025"></a>

## PMS_EXP_ESAL_Initial

Source: `dTIMSExpressions` / `0c6232ef-4b03-4282-9cb6-0f89e472f025`.

Calculates ESALs

Readable:
```text
IF(Get_Field(Avg_Truck_Per) < Get_Number(0) OR Get_Field(ADT_20_Yr_Factor) < Get_Number(0) OR Get_Field(ADT) < Get_Number(0) OR Get_Field(ESAL_Factor) < Get_Number(0), -Get_Number(1), ( ( ( Get_Field(Avg_Truck_Per)/Get_Number(100)) * ( ( Get_Field(ADT_20_Yr_Factor) * ( Get_Field(ADT) / Get_Number(2)) ) + ( Get_Field(ADT) / Get_Number(2)) ) / Get_Number(2))  * Get_Number(20) * Get_Number(365)) * Get_Field(ESAL_Factor))
```

Original:
```text
IF(Get_Field(cd9a4348-f45a-4a0e-bebb-822e9ed3aed0) < Get_Number(0) OR Get_Field(b6811242-3da5-4f6e-8a97-fda32769223c) < Get_Number(0) OR Get_Field(cfa94697-b716-4fc1-a695-19b524eab35f) < Get_Number(0) OR Get_Field(a07c22cd-de80-4ce7-b93e-f87143dec48c) < Get_Number(0), -Get_Number(1), ( ( ( Get_Field(cd9a4348-f45a-4a0e-bebb-822e9ed3aed0)/Get_Number(100)) * ( ( Get_Field(b6811242-3da5-4f6e-8a97-fda32769223c) * ( Get_Field(cfa94697-b716-4fc1-a695-19b524eab35f) / Get_Number(2)) ) + ( Get_Field(cfa94697-b716-4fc1-a695-19b524eab35f) / Get_Number(2)) ) / Get_Number(2))  * Get_Number(20) * Get_Number(365)) * Get_Field(a07c22cd-de80-4ce7-b93e-f87143dec48c))
```

<a id="e-cc2fa8e1-ff3c-43e5-ab58-b5a4b2d111f3"></a>

## PMS_EXP_Pave_Type_Rd_Inv

Source: `dTIMSExpressions` / `cc2fa8e1-ff3c-43e5-ab58-b5a4b2d111f3`.



Readable:
```text
IF(Get_Field(Surf_Typ) = '12' OR Get_Field(Surf_Typ) = '13','RC',IF(Get_Field(Surf_Typ) = '10' OR Get_Field(Surf_Typ) = '11','BC','OT'))
```

Original:
```text
IF(Get_Field(4a6cb5a6-2a5b-4828-bcbc-138f331a5868) = '12' OR Get_Field(4a6cb5a6-2a5b-4828-bcbc-138f331a5868) = '13','RC',IF(Get_Field(4a6cb5a6-2a5b-4828-bcbc-138f331a5868) = '10' OR Get_Field(4a6cb5a6-2a5b-4828-bcbc-138f331a5868) = '11','BC','OT'))
```

<a id="e-ba036846-3ec8-4f68-ab81-aa542c16175a"></a>

## PMS_EXP_TABS_Empty

Source: `dTIMSExpressions` / `ba036846-3ec8-4f68-ab81-aa542c16175a`.



Readable:
```text
''
```

Original:
```text
''
```

<a id="e-bfa4b97d-ca33-4ce8-9ba3-29d8cd635cb8"></a>

## PMS_EXP_YEAR_IMPROVED_NUMBER

Source: `dTIMSExpressions` / `bfa4b97d-ca33-4ce8-9ba3-29d8cd635cb8`.

Year Improved as a Number

Readable:
```text
VAL(Get_Field(Year_Improved))
```

Original:
```text
VAL(Get_Field(bf58d492-fcc4-4bf0-b840-16e82efb7ce0))
```

<a id="e-201058d9-91c4-4b9b-a5bd-d13e2f364fd9"></a>

## PMS_EXP_tCategory

Source: `RuntimeExpressions` / `201058d9-91c4-4b9b-a5bd-d13e2f364fd9`.



Readable:
```text
IF(ISEMPTY(Get_Field(Sign)) Or IFDEFAULT(Get_Field(Sign)),'',IF(Get_Field(Budget_Category_Override) = 'Interstate_Poor',IF(GET_ANALVR(PMS_nAAV_CND_PSI) < Get_Number(3.4),'P','G'),IF(Get_Field(Budget_Category_Override) = 'APD_Poor',IF(GET_ANALVR(PMS_nAAV_CND_PSI) < Get_Number(3.4),'P','G'),IF(Get_Field(Budget_Category_Override) = 'US_Poor',IF(GET_ANALVR(PMS_nAAV_CND_PSI) < Get_Number(3.4),'P','G'),IF(Get_Field(Budget_Category_Override) = 'WV_Poor',IF(GET_ANALVR(PMS_nAAV_CND_PSI) < Get_Number(3.4),'P','G'),IF(Get_Field(Budget_Category_Override) = 'NHS_Poor',IF(GET_ANALVR(PMS_nAAV_CND_PSI) < Get_Number(3.4), 'P', 'G'),IF(Get_Field(Budget_Category_Override) = 'County_Poor',IF(GET_ANALVR(PMS_nAAV_CND_PSI) < Get_Number(2.2),'P','G'),'')))))))
```

Original:
```text
IF(ISEMPTY(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)) Or IFDEFAULT(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)),'',IF(Get_Field(8007a74e-31a9-43b9-9bc9-b472225b1a46) = 'Interstate_Poor',IF(GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) < Get_Number(3.4),'P','G'),IF(Get_Field(8007a74e-31a9-43b9-9bc9-b472225b1a46) = 'APD_Poor',IF(GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) < Get_Number(3.4),'P','G'),IF(Get_Field(8007a74e-31a9-43b9-9bc9-b472225b1a46) = 'US_Poor',IF(GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) < Get_Number(3.4),'P','G'),IF(Get_Field(8007a74e-31a9-43b9-9bc9-b472225b1a46) = 'WV_Poor',IF(GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) < Get_Number(3.4),'P','G'),IF(Get_Field(8007a74e-31a9-43b9-9bc9-b472225b1a46) = 'NHS_Poor',IF(GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) < Get_Number(3.4), 'P', 'G'),IF(Get_Field(8007a74e-31a9-43b9-9bc9-b472225b1a46) = 'County_Poor',IF(GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) < Get_Number(2.2),'P','G'),'')))))))
```

<a id="e-b8a56232-3815-4a55-a6d9-5c112fcab80e"></a>

## PMS_EXP_tCategory_Initial

Source: `dTIMSExpressions` / `b8a56232-3815-4a55-a6d9-5c112fcab80e`.



Readable:
```text
IF(ISEMPTY(Get_Field(Sign)) Or IFDEFAULT(Get_Field(Sign)),'',IF(Get_Field(Sign) = '1',IF(Get_Field(PSI) < Get_Number(3.4),'P','G'),IF(Get_Field(Sign) = '2',IF(Get_Field(PSI) < Get_Number(3.4),'P','G'),IF(Get_Field(Sign) = '3',IF(Get_Field(PSI) < Get_Number(3.4),'P','G'),IF(Get_Field(Sign) = '4',IF(Get_Field(PSI) < Get_Number(2.2),'P','G'),'')))))
```

Original:
```text
IF(ISEMPTY(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)) Or IFDEFAULT(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)),'',IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) = '1',IF(Get_Field(1eca4d42-a141-4b12-8457-f11b987a6710) < Get_Number(3.4),'P','G'),IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) = '2',IF(Get_Field(1eca4d42-a141-4b12-8457-f11b987a6710) < Get_Number(3.4),'P','G'),IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) = '3',IF(Get_Field(1eca4d42-a141-4b12-8457-f11b987a6710) < Get_Number(3.4),'P','G'),IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) = '4',IF(Get_Field(1eca4d42-a141-4b12-8457-f11b987a6710) < Get_Number(2.2),'P','G'),'')))))
```

<a id="e-95ae4ad6-21c0-4617-8d4d-35d88889bc3b"></a>

## PMS_Exp_Bud_Cat_Override

Source: `dTIMSExpressions` / `95ae4ad6-21c0-4617-8d4d-35d88889bc3b`.



Readable:
```text
IF(Get_Field(TAMP_CLASS) = 'NHS','Pavement_NHS',
IF(Get_Field(TAMP_CLASS) = 'TP','Pavement_Turnpike','Pavement_Non_NHS'))

//IF(LEFT(Analysis->Fed_Aid,1.0)='1' OR LEFT(Analysis->Fed_Aid,1.0) ='2',
//    'Pavement_NHS',
//    'Pavement_Non_NHS'
//)
```

Original:
```text
IF(Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'NHS','Pavement_NHS',
IF(Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834) = 'TP','Pavement_Turnpike','Pavement_Non_NHS'))

//IF(LEFT(Analysis->Fed_Aid,1.0)='1' OR LEFT(Analysis->Fed_Aid,1.0) ='2',
//    'Pavement_NHS',
//    'Pavement_Non_NHS'
//)
```

<a id="e-3dda9f9c-3fd8-4c1d-9658-d4f7ea79afb4"></a>

## PMS_Exp_Com_Cost

Source: `dTIMSExpressions` / `3dda9f9c-3fd8-4c1d-9658-d4f7ea79afb4`.



Readable:
```text
IF(Get_Field(STIP_CN_COST) > -Get_Number(1),Get_Field(STIP_CN_COST), -Get_Number(1)) 
```

Original:
```text
IF(Get_Field(370da2e6-424b-4308-867a-05afa860cf22) > -Get_Number(1),Get_Field(370da2e6-424b-4308-867a-05afa860cf22), -Get_Number(1)) 
```

<a id="e-c72a47b2-af4c-4098-ace8-9a8945f0507e"></a>

## PMS_Exp_Com_Year

Source: `dTIMSExpressions` / `c72a47b2-af4c-4098-ace8-9a8945f0507e`.



Readable:
```text
IF(YEAR(Get_Field(STIP_END_DATE)) > Get_Number(2019),YEAR(Get_Field(STIP_END_DATE)) - Get_Number(2019), -Get_Number(1)) 
```

Original:
```text
IF(YEAR(Get_Field(49ecaefc-4cd6-4d0a-a801-ee7c919c73e9)) > Get_Number(2019),YEAR(Get_Field(49ecaefc-4cd6-4d0a-a801-ee7c919c73e9)) - Get_Number(2019), -Get_Number(1)) 
```

<a id="e-2b408860-2850-4d26-9931-ee9179d4a17c"></a>

## PMS_Exp_Cond_Year_1998

Source: `dTIMSExpressions` / `2b408860-2850-4d26-9931-ee9179d4a17c`.



Readable:
```text
Get_Number(1998)
```

Original:
```text
Get_Number(1998)
```

<a id="e-baab2760-1c6a-4cf7-a4c3-f6bcd3a54afa"></a>

## PMS_Exp_Cond_Year_2000

Source: `dTIMSExpressions` / `baab2760-1c6a-4cf7-a4c3-f6bcd3a54afa`.



Readable:
```text
Get_Number(2000)
```

Original:
```text
Get_Number(2000)
```

<a id="e-54133ea3-5e43-424d-8abf-7fe7d478b22c"></a>

## PMS_Exp_Cond_Year_2002

Source: `dTIMSExpressions` / `54133ea3-5e43-424d-8abf-7fe7d478b22c`.



Readable:
```text
Get_Number(2002)
```

Original:
```text
Get_Number(2002)
```

<a id="e-eb6be70b-ba79-44d8-b06a-30b8f990c0a8"></a>

## PMS_Exp_Cond_Year_2004

Source: `dTIMSExpressions` / `eb6be70b-ba79-44d8-b06a-30b8f990c0a8`.



Readable:
```text
Get_Number(2004)
```

Original:
```text
Get_Number(2004)
```

<a id="e-109e3b8f-7aa6-4d3a-b062-1e3fa316ba65"></a>

## PMS_Exp_Cond_Year_2006

Source: `dTIMSExpressions` / `109e3b8f-7aa6-4d3a-b062-1e3fa316ba65`.



Readable:
```text
Get_Number(2006)
```

Original:
```text
Get_Number(2006)
```

<a id="e-e05450db-b880-4dd0-a527-7a64e5428755"></a>

## PMS_Exp_Cond_Year_2008

Source: `dTIMSExpressions` / `e05450db-b880-4dd0-a527-7a64e5428755`.



Readable:
```text
Get_Number(2008)
```

Original:
```text
Get_Number(2008)
```

<a id="e-338d9b05-d340-441e-a899-51b3f3979ac6"></a>

## PMS_Exp_Cond_Year_2010

Source: `dTIMSExpressions` / `338d9b05-d340-441e-a899-51b3f3979ac6`.



Readable:
```text
Get_Number(2010)
```

Original:
```text
Get_Number(2010)
```

<a id="e-06ed58de-209d-431b-8320-1de6cbf02f77"></a>

## PMS_Exp_Cond_Year_2011

Source: `dTIMSExpressions` / `06ed58de-209d-431b-8320-1de6cbf02f77`.



Readable:
```text
Get_Number(2011)
```

Original:
```text
Get_Number(2011)
```

<a id="e-90acfbce-709e-4fab-81c8-9d7a06eeb98b"></a>

## PMS_Exp_Cond_Year_2012

Source: `dTIMSExpressions` / `90acfbce-709e-4fab-81c8-9d7a06eeb98b`.



Readable:
```text
Get_Number(2012)
```

Original:
```text
Get_Number(2012)
```

<a id="e-78adf387-5d8a-405b-a98a-60bc386ddea5"></a>

## PMS_Exp_Cond_Year_2013

Source: `dTIMSExpressions` / `78adf387-5d8a-405b-a98a-60bc386ddea5`.



Readable:
```text
Get_Number(2013)
```

Original:
```text
Get_Number(2013)
```

<a id="e-aeb003f3-be3a-4973-a87a-95557c18baba"></a>

## PMS_Exp_Cond_Year_2014

Source: `dTIMSExpressions` / `aeb003f3-be3a-4973-a87a-95557c18baba`.



Readable:
```text
Get_Number(2014)
```

Original:
```text
Get_Number(2014)
```

<a id="e-4d935f88-18f2-402b-8e64-6e25763e474f"></a>

## PMS_Exp_Cond_Year_2015

Source: `dTIMSExpressions` / `4d935f88-18f2-402b-8e64-6e25763e474f`.



Readable:
```text
Get_Number(2015)
```

Original:
```text
Get_Number(2015)
```

<a id="e-220228ba-3fcd-4c37-af6b-9c0104bdaef2"></a>

## PMS_Exp_Cond_Year_2016

Source: `dTIMSExpressions` / `220228ba-3fcd-4c37-af6b-9c0104bdaef2`.



Readable:
```text
Get_Number(2016)
```

Original:
```text
Get_Number(2016)
```

<a id="e-c138e676-30df-436d-b8e7-0e64e63b3473"></a>

## PMS_Exp_Cond_Year_2017

Source: `dTIMSExpressions` / `c138e676-30df-436d-b8e7-0e64e63b3473`.



Readable:
```text
Get_Number(2017)
```

Original:
```text
Get_Number(2017)
```

<a id="e-1f15bfca-77db-41e1-b522-518e87d8dd0d"></a>

## PMS_Exp_Sign_System_RSL_Threshold

Source: `dTIMSExpressions` / `1f15bfca-77db-41e1-b522-518e87d8dd0d`.



Readable:
```text
RTRIM(IF(RTRIM(Get_Field(Spec_Sys)) = '10' AND RTRIM(Get_Field(Sign)) = '2', '10', Get_Field(Sign)))
```

Original:
```text
RTRIM(IF(RTRIM(Get_Field(51f41088-b57b-4756-9b09-b108c4a81640)) = '10' AND RTRIM(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)) = '2', '10', Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)))
```

<a id="e-2601d5f4-cf8b-474b-8a23-9052454c1b46"></a>

## PMS_Exp_Surf_Type_Backup

Source: `dTIMSExpressions` / `2601d5f4-cf8b-474b-8a23-9052454c1b46`.



Readable:
```text
Get_Field(Surf_Typ)
```

Original:
```text
Get_Field(28ac1edb-7847-4852-8fe6-c9b951410aee)
```

<a id="e-311f3b1a-7669-4156-980e-45d4a94f7e0e"></a>

## PMS_Exp_Surf_Type_Code

Source: `dTIMSExpressions` / `311f3b1a-7669-4156-980e-45d4a94f7e0e`.



Readable:
```text
IF(IFDEFAULT(Get_Field(SURF_TYPE_ARAN)) OR EMPTY(Get_Field(SURF_TYPE_ARAN)),Get_Field(Surf_Typ_Backup), IF(Get_Field(SURF_TYPE_ARAN) = 'ASP','11',IF(Get_Field(SURF_TYPE_ARAN) = 'CON','12',Get_Field(Surf_Typ_Backup))))
```

Original:
```text
IF(IFDEFAULT(Get_Field(71b500e1-7511-45a9-99d9-63ba6ce36a6f)) OR EMPTY(Get_Field(71b500e1-7511-45a9-99d9-63ba6ce36a6f)),Get_Field(761fa58d-63e7-4c4c-ba1b-f3b772cc805f), IF(Get_Field(71b500e1-7511-45a9-99d9-63ba6ce36a6f) = 'ASP','11',IF(Get_Field(71b500e1-7511-45a9-99d9-63ba6ce36a6f) = 'CON','12',Get_Field(761fa58d-63e7-4c4c-ba1b-f3b772cc805f))))
```

<a id="e-0fc3ed90-1ee8-4ea3-b174-87839b7b9692"></a>

## PMS_Exp_TAMP_CLASS_NHS

Source: `dTIMSExpressions` / `0fc3ed90-1ee8-4ea3-b174-87839b7b9692`.

NHS

Readable:
```text
'NHS'
```

Original:
```text
'NHS'
```

<a id="e-ca9b8938-3d75-407d-82d6-4efee25f1098"></a>

## PMS_Exp_TAMP_CLASS_NON_NHS

Source: `dTIMSExpressions` / `ca9b8938-3d75-407d-82d6-4efee25f1098`.

NON NHS

Readable:
```text
'NON_NHS'
```

Original:
```text
'NON_NHS'
```

<a id="e-19d3b6de-ed29-486d-a933-8d83aabd657e"></a>

## PMS_Exp_TAMP_CLASS_TURNPIKE

Source: `dTIMSExpressions` / `19d3b6de-ed29-486d-a933-8d83aabd657e`.

TURN PIKE

Readable:
```text
'TP'
```

Original:
```text
'TP'
```

<a id="e-bd8588a0-a143-4a06-9b91-2063dd3948c9"></a>

## PMS_Exp_Text_Default

Source: `dTIMSExpressions` / `bd8588a0-a143-4a06-9b91-2063dd3948c9`.

Text Default

Readable:
```text
''
```

Original:
```text
''
```

<a id="e-39292a76-a572-44cc-87f8-d560bde11c84"></a>

## PMS_Exp_Total_Miles_APD

Source: `dTIMSExpressions` / `39292a76-a572-44cc-87f8-d560bde11c84`.



Readable:
```text
Get_Number(777.033)
```

Original:
```text
Get_Number(777.033)
```

<a id="e-14c3ef12-759b-4a65-b16b-d34a331725c6"></a>

## PMS_Exp_Total_Miles_County

Source: `dTIMSExpressions` / `14c3ef12-759b-4a65-b16b-d34a331725c6`.



Readable:
```text
Get_Number(14317.85)
```

Original:
```text
Get_Number(14317.85)
```

<a id="e-0887554d-0770-4605-be75-50af1a7c2d83"></a>

## PMS_Exp_Total_Miles_Interstate

Source: `dTIMSExpressions` / `0887554d-0770-4605-be75-50af1a7c2d83`.



Readable:
```text
Get_Number(869.82)
```

Original:
```text
Get_Number(869.82)
```

<a id="e-b50bf686-5aae-4889-a20f-889da3162570"></a>

## PMS_Exp_Total_Miles_NHS

Source: `dTIMSExpressions` / `b50bf686-5aae-4889-a20f-889da3162570`.



Readable:
```text
Get_Number(1683.79)
```

Original:
```text
Get_Number(1683.79)
```

<a id="e-a69abb03-e9eb-47d1-805e-23cd82419ced"></a>

## PMS_Exp_Total_Miles_NHSall

Source: `dTIMSExpressions` / `a69abb03-e9eb-47d1-805e-23cd82419ced`.



Readable:
```text
Get_Number(1845.51)
```

Original:
```text
Get_Number(1845.51)
```

<a id="e-e4dc18b8-c261-4f0c-84d0-a321b2744b18"></a>

## PMS_Exp_Total_Miles_US

Source: `dTIMSExpressions` / `e4dc18b8-c261-4f0c-84d0-a321b2744b18`.



Readable:
```text
Get_Number(1794.342)
```

Original:
```text
Get_Number(1794.342)
```

<a id="e-5c02ed19-7c48-48d1-8a37-3600f59f90d4"></a>

## PMS_Exp_Total_Miles_WV

Source: `dTIMSExpressions` / `5c02ed19-7c48-48d1-8a37-3600f59f90d4`.



Readable:
```text
Get_Number(3739.333)
```

Original:
```text
Get_Number(3739.333)
```

<a id="e-23f301f1-83fb-4b77-9aa5-0723c715bf85"></a>

## PMS_Exp_cOne

Source: `dTIMSExpressions` / `23f301f1-83fb-4b77-9aa5-0723c715bf85`.

Exp Character One

Readable:
```text
'1'
```

Original:
```text
'1'
```

<a id="e-15ad4062-dd41-4006-a587-64388f3ad481"></a>

## PMS_Expression_Analysis_Curve

Source: `dTIMSExpressions` / `15ad4062-dd41-4006-a587-64388f3ad481`.



Readable:
```text
'$Performance_Curves'
```

Original:
```text
'$Performance_Curves'
```

<a id="e-2b0af820-692c-4ee0-b08b-45b02ba761b3"></a>

## PMS_Expression_Analysis_File_Name

Source: `dTIMSExpressions` / `2b0af820-692c-4ee0-b08b-45b02ba761b3`.

File name of Analysis Parameters spreadsheet

Readable:
```text
'dTIMS Analysis Parameters.xls'
```

Original:
```text
'dTIMS Analysis Parameters.xls'
```

<a id="e-05fcd0d3-2d0b-4b45-bd5e-a4d7bef200c5"></a>

## PMS_Expression_Analysis_File_Path

Source: `dTIMSExpressions` / `05fcd0d3-2d0b-4b45-bd5e-a4d7bef200c5`.

File path to Parameters spreadsheet in Asset Management folder

Readable:
```text
'C:\Client\WVDOT\2019-06 - Pavements\'
```

Original:
```text
'C:\Client\WVDOT\2019-06 - Pavements\'
```

<a id="e-f13cb0e2-d7d7-4923-b7ab-49658bd2df2f"></a>

## PMS_Expression_Analysis_File_Path_Local_Gary

Source: `dTIMSExpressions` / `f13cb0e2-d7d7-4923-b7ab-49658bd2df2f`.



Readable:
```text
'C:\Client\West Virginia\dTIMS CT Enterprise\'
```

Original:
```text
'C:\Client\West Virginia\dTIMS CT Enterprise\'
```

<a id="e-50d782d3-0e25-442a-acb9-f26d373f34e6"></a>

## PMS_Expression_Analysis_File_Path_WV

Source: `dTIMSExpressions` / `50d782d3-0e25-442a-acb9-f26d373f34e6`.

File path to Asset Management folder on WV Server

Readable:
```text
'\\otb6nas01\DOTShared\OMshares\Asset Management\dTIMS Parameter XTAB\'
```

Original:
```text
'\\otb6nas01\DOTShared\OMshares\Asset Management\dTIMS Parameter XTAB\'
```

<a id="e-441e40e1-1425-4d78-96b1-90be608cf41b"></a>

## PMS_Expression_Analysis_File_Path_WV2

Source: `dTIMSExpressions` / `441e40e1-1425-4d78-96b1-90be608cf41b`.



Readable:
```text
'\\otb6nas01\DOT Shared\omshares\Asset Management\dTIMS Parameter XTAB\'
```

Original:
```text
'\\otb6nas01\DOT Shared\omshares\Asset Management\dTIMS Parameter XTAB\'
```

<a id="e-ab655025-f6da-47fd-8b16-a9cdb081c6eb"></a>

## PMS_Expression_Analysis_RSL_Thresholds

Source: `dTIMSExpressions` / `ab655025-f6da-47fd-8b16-a9cdb081c6eb`.



Readable:
```text
'$RSL_Thresholds'
```

Original:
```text
'$RSL_Thresholds'
```

<a id="e-31e510c2-32de-4f57-9bd3-e01e5e7d0241"></a>

## PMS_Expression_Analysis_Treatment_Cost

Source: `dTIMSExpressions` / `31e510c2-32de-4f57-9bd3-e01e5e7d0241`.

'$TreatmentCost13' or '$Treament_Costs'

Readable:
```text
'$TreatmentCost16'
```

Original:
```text
'$TreatmentCost16'
```

<a id="e-3ad27ab2-7930-4d6e-952f-83789f20d0c1"></a>

## PMS_Expression_Analysis_Treatment_Trigger

Source: `dTIMSExpressions` / `3ad27ab2-7930-4d6e-952f-83789f20d0c1`.

'$Treatment_Triggers_CCI' or '$Treatment_Triggers_All_Index' or '$Treatment_Triggers_All_Index_Modified' or '$Treatment_Triggers_PSI'

Readable:
```text
'$Treatment_Triggers_CCI'
```

Original:
```text
'$Treatment_Triggers_CCI'
```

<a id="e-618f1aa7-56bd-4f3d-9a64-c2abc661a84b"></a>

## PMS_Expression_Bridge_BCO

Source: `dTIMSExpressions` / `618f1aa7-56bd-4f3d-9a64-c2abc661a84b`.

Bridge Budget Category Override

Readable:
```text
IF(Get_Field(NHS)='0','Bridge_NON_NHS','Bridge_NHS')
```

Original:
```text
IF(Get_Field(ff652eda-e73c-48a8-bd20-fd6e80950604)='0','Bridge_NON_NHS','Bridge_NHS')
```

<a id="e-95b8c579-66e6-40f8-a0fa-78469c7f6039"></a>

## PMS_Expression_Rehab_Type

Source: `dTIMSExpressions` / `95b8c579-66e6-40f8-a0fa-78469c7f6039`.

Fix Rehab Type to Initial if Rehab Year is null

Readable:
```text
IF(IFDEFAULT(Get_Field(REHAB_COMPLETION_YEAR)) OR 
LTRIM(RTRIM(Get_Field(REHAB_ACTIVITY)))='' OR
IFDEFAULT(Get_Field(REHAB_ACTIVITY)),'Initial',Get_Field(REHAB_ACTIVITY))
```

Original:
```text
IF(IFDEFAULT(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b)) OR 
LTRIM(RTRIM(Get_Field(9dd3677c-6072-4c3f-b12e-cd65909e2f83)))='' OR
IFDEFAULT(Get_Field(9dd3677c-6072-4c3f-b12e-cd65909e2f83)),'Initial',Get_Field(9dd3677c-6072-4c3f-b12e-cd65909e2f83))
```

<a id="e-569a7f27-29da-42a8-a34f-a17c337fc8dd"></a>

## PMS_FILTER_CONDITION_HISTORY_YEAR_2015

Source: `dTIMSExpressions` / `569a7f27-29da-42a8-a34f-a17c337fc8dd`.

FILTER_CONDITION_HISTORY_YEAR_2015

Readable:
```text
Get_Field(COND_YEAR)=Get_Number(2015)
```

Original:
```text
Get_Field(b975671a-6c35-4b6d-bb06-103f1e87370d)=Get_Number(2015)
```

<a id="e-1f17645c-7fbb-467d-bdd8-dc007942e511"></a>

## PMS_FILTER_CONDITION_HISTORY_YEAR_2016

Source: `dTIMSExpressions` / `1f17645c-7fbb-467d-bdd8-dc007942e511`.

FILTER_CONDITION_HISTORY_YEAR_2016

Readable:
```text
Get_Field(COND_YEAR)=Get_Number(2016)
```

Original:
```text
Get_Field(b975671a-6c35-4b6d-bb06-103f1e87370d)=Get_Number(2016)
```

<a id="e-33063f7f-516b-46cf-90fe-9bc2c7c35b1d"></a>

## PMS_FILTER_CONDITION_HISTORY_YEAR_2017

Source: `dTIMSExpressions` / `33063f7f-516b-46cf-90fe-9bc2c7c35b1d`.

FILTER_CONDITION_HISTORY_YEAR_2017

Readable:
```text
Get_Field(COND_YEAR)=Get_Number(2017)
```

Original:
```text
Get_Field(b975671a-6c35-4b6d-bb06-103f1e87370d)=Get_Number(2017)
```

<a id="e-cbf2f3e7-ca7f-49b3-84ff-16f5fdc1e51e"></a>

## PMS_FILTER_CONDITION_HISTORY_YEAR_2018

Source: `dTIMSExpressions` / `cbf2f3e7-ca7f-49b3-84ff-16f5fdc1e51e`.

FILTER_CONDITION_HISTORY_YEAR_2018

Readable:
```text
Get_Field(COND_YEAR)=Get_Number(2018)
```

Original:
```text
Get_Field(b975671a-6c35-4b6d-bb06-103f1e87370d)=Get_Number(2018)
```

<a id="e-0e98e4d1-4a8c-4845-a6a2-83c11e3dc30d"></a>

## PMS_FILTER_CONDITION_HISTORY_YEAR_2019

Source: `dTIMSExpressions` / `0e98e4d1-4a8c-4845-a6a2-83c11e3dc30d`.

FILTER_CONDITION_HISTORY_YEAR_2019

Readable:
```text
Get_Field(COND_YEAR)=Get_Number(2019)
```

Original:
```text
Get_Field(b975671a-6c35-4b6d-bb06-103f1e87370d)=Get_Number(2019)
```

<a id="e-db678ca2-499a-4054-95f6-a09c4146f3d3"></a>

## PMS_FILTER_CONDITION_HISTORY_YEAR_2020

Source: `dTIMSExpressions` / `db678ca2-499a-4054-95f6-a09c4146f3d3`.

FILTER_CONDITION_HISTORY_YEAR_2020

Readable:
```text
Get_Field(COND_YEAR)=Get_Number(2020)
```

Original:
```text
Get_Field(b975671a-6c35-4b6d-bb06-103f1e87370d)=Get_Number(2020)
```

<a id="e-d31880a8-27f6-4936-b3c6-1d234a50758d"></a>

## PMS_FILTER_CONDITION_HISTORY_YEAR_2021

Source: `dTIMSExpressions` / `d31880a8-27f6-4936-b3c6-1d234a50758d`.

FILTER_CONDITION_HISTORY_YEAR_2021

Readable:
```text
Get_Field(COND_YEAR)=Get_Number(2021)
```

Original:
```text
Get_Field(b975671a-6c35-4b6d-bb06-103f1e87370d)=Get_Number(2021)
```

<a id="e-f089af7e-d8b7-43a3-bcbf-ca63f592030d"></a>

## PMS_FILTER_CONDITION_HISTORY_YEAR_2022

Source: `dTIMSExpressions` / `f089af7e-d8b7-43a3-bcbf-ca63f592030d`.

FILTER_CONDITION_HISTORY_YEAR_2022

Readable:
```text
Get_Field(COND_YEAR)=Get_Number(2022)
```

Original:
```text
Get_Field(b975671a-6c35-4b6d-bb06-103f1e87370d)=Get_Number(2022)
```

<a id="e-53b75b61-7bad-4bf4-bf17-5aa14011c6a7"></a>

## PMS_FILTER_CONDITION_HISTORY_YEAR_2023

Source: `dTIMSExpressions` / `53b75b61-7bad-4bf4-bf17-5aa14011c6a7`.

FILTER_CONDITION_HISTORY_YEAR_2023

Readable:
```text
Get_Field(COND_YEAR)=Get_Number(2023)
```

Original:
```text
Get_Field(b975671a-6c35-4b6d-bb06-103f1e87370d)=Get_Number(2023)
```

<a id="e-e1a1733e-dddf-4364-bdbb-3d73389ac0ef"></a>

## PMS_FILTER_CONDITION_HISTORY_YEAR_2024

Source: `dTIMSExpressions` / `e1a1733e-dddf-4364-bdbb-3d73389ac0ef`.

FILTER_CONDITION_HISTORY_YEAR_2024

Readable:
```text
Get_Field(COND_YEAR)=Get_Number(2024)
```

Original:
```text
Get_Field(b975671a-6c35-4b6d-bb06-103f1e87370d)=Get_Number(2024)
```

<a id="e-d508ff8a-c284-4ae7-adde-7eff8d2a550b"></a>

## PMS_FILTER_CONDITION_HISTORY_YEAR_2025

Source: `dTIMSExpressions` / `d508ff8a-c284-4ae7-adde-7eff8d2a550b`.

FILTER_CONDITION_HISTORY_YEAR_2025

Readable:
```text
Get_Field(COND_YEAR)=Get_Number(2025)
```

Original:
```text
Get_Field(b975671a-6c35-4b6d-bb06-103f1e87370d)=Get_Number(2025)
```

<a id="e-25c6dad5-eaef-48a7-9369-6d35feb38b9b"></a>

## PMS_FX_SurfType_Edit

Source: `dTIMSExpressions` / `25c6dad5-eaef-48a7-9369-6d35feb38b9b`.

Convert to Surface type text (Table code attribute)

Readable:
```text
STR(ROUND(Get_Field(SURF_TYPE_FLOAT),Get_Number(1)))
```

Original:
```text
STR(ROUND(Get_Field(de2ac408-d549-48af-84ca-1957b9d0945e),Get_Number(1)))
```

<a id="e-d869e09f-4927-4fcc-adae-3a0456b81887"></a>

## PMS_Filter_2007

Source: `dTIMSExpressions` / `d869e09f-4927-4fcc-adae-3a0456b81887`.



Readable:
```text
Get_Field(Name)='2007'
```

Original:
```text
Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b)='2007'
```

<a id="e-dac6389f-9b0a-4d24-8cfc-a6b2c433e932"></a>

## PMS_History_Combined_Rehab_Most_Recent_Name

Source: `dTIMSExpressions` / `dac6389f-9b0a-4d24-8cfc-a6b2c433e932`.

Fix History combined rehab most recent name.

Readable:
```text
Get_Field(RoadName) + '-' +
SUBSTR(LTRIM(RTRIM(STR(Get_Field(From)+Get_Number(1000.0001)))),Get_Number(2),Get_Number(7)) + '-' + 
LTRIM(RTRIM(STR(Get_Field(Completion_Year))))
```

Original:
```text
Get_Field(cd28954c-d613-487f-bb70-317d83404ca0) + '-' +
SUBSTR(LTRIM(RTRIM(STR(Get_Field(82b3c40c-2922-4321-8836-2951f5f2ecd8)+Get_Number(1000.0001)))),Get_Number(2),Get_Number(7)) + '-' + 
LTRIM(RTRIM(STR(Get_Field(e7db11df-e230-43ae-9ee8-f5b98786a168))))
```

<a id="e-d5775bb6-fb3e-4570-91b2-032a7f8f60bd"></a>

## PMS_Int_From

Source: `dTIMSExpressions` / `d5775bb6-fb3e-4570-91b2-032a7f8f60bd`.



Readable:
```text
GET_FROMADD(Get_Perspective(Base))
```

Original:
```text
GET_FROMADD(Get_Perspective(9fca3362-b670-4590-9960-0e511aed59c4))
```

<a id="e-507e4a81-f74e-44ab-b4c2-b172d62b8a05"></a>

## PMS_Int_Road

Source: `dTIMSExpressions` / `507e4a81-f74e-44ab-b4c2-b172d62b8a05`.



Readable:
```text
GET_BASEELEMID(Get_Perspective(Base))
```

Original:
```text
GET_BASEELEMID(Get_Perspective(9fca3362-b670-4590-9960-0e511aed59c4))
```

<a id="e-7b5bada9-dff3-4893-ae44-61a0924153f7"></a>

## PMS_Int_To

Source: `dTIMSExpressions` / `7b5bada9-dff3-4893-ae44-61a0924153f7`.



Readable:
```text
GET_TOADD(Get_Perspective(Base))
```

Original:
```text
GET_TOADD(Get_Perspective(9fca3362-b670-4590-9960-0e511aed59c4))
```

<a id="e-1eee24af-44c5-400e-87c1-6720d0a41e63"></a>

## PMS_abfOBJ_Analysis_TAMP_INT_PROJECT_LENGTH

Source: `dTIMSExpressions` / `1eee24af-44c5-400e-87c1-6720d0a41e63`.

2019 TAMP Analysis - Interstate Project Length Analysis

Readable:
```text
Get_Field(Sign) = '1' AND NOT   Get_Exp(PMS_abfOBJ_I68) AND Get_Field(Lane) = '1' AND Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) = '1' AND NOT   Get_Exp(4c811992-2c2d-42c6-b156-c4d16973b739) AND Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = '1' AND Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-22c0ca76-8d43-44bf-bb29-6a5789dd3bdc"></a>

## PMS_abfOBJ_Analysis_TAMP_INT_Tenth

Source: `dTIMSExpressions` / `22c0ca76-8d43-44bf-bb29-6a5789dd3bdc`.

 MAP 21 Tenth Mile Interstate

Readable:
```text
Get_Field(Sign) = '1' AND NOT   Get_Exp(PMS_abfOBJ_I68) AND Get_Field(Lane) = '2' AND Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) = '1' AND NOT   Get_Exp(4c811992-2c2d-42c6-b156-c4d16973b739) AND Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = '2' AND Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-7d15d62f-586e-4d05-bd08-7dabbc0df8e5"></a>

## PMS_abfOBJ_Analysis_TAMP_NHS_COMBINED

Source: `dTIMSExpressions` / `7d15d62f-586e-4d05-bd08-7dabbc0df8e5`.

TAMP 2024 NHS Combined

Readable:
```text
(Get_Field(Sign) = '1' OR LEFT(Get_Field(Fed_Aid),Get_Number(1))='2' OR LEFT(Get_Field(Fed_Aid),Get_Number(1))='4' ) AND 
Get_Field(Lane) = '1' AND 
(
    Get_Field(Com_Year) >= Get_Number(1) OR 
    (
        Get_Field(IRI_Mean) >= Get_Number(0) AND 
        (
        (Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR 
        (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0))
        )
    )
)
AND NOT      Get_Exp(PMS_abfOBJ_TP)
```

Original:
```text
(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) = '1' OR LEFT(Get_Field(e8613014-fa1e-4da2-ae75-c77b722d9c37),Get_Number(1))='2' OR LEFT(Get_Field(e8613014-fa1e-4da2-ae75-c77b722d9c37),Get_Number(1))='4' ) AND 
Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = '1' AND 
(
    Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0) >= Get_Number(1) OR 
    (
        Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND 
        (
        (Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR 
        (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0))
        )
    )
)
AND NOT      Get_Exp(c1fcd884-076e-40e8-a2ce-c59e6f7fd0b9)
```

<a id="e-16197fde-220b-41a6-bab9-c7c9795d6fc2"></a>

## PMS_abfOBJ_Analysis_TAMP_NHS_COMBINED_TENTH

Source: `dTIMSExpressions` / `16197fde-220b-41a6-bab9-c7c9795d6fc2`.

TAMP 2019 NHS Combined - Tenth Mile

Readable:
```text
(Get_Field(Sign) = '1' OR LEFT(Get_Field(Fed_Aid),Get_Number(1))='2' OR LEFT(Get_Field(Fed_Aid),Get_Number(1))='4') AND 
Get_Field(Lane) = '2' AND 
Get_Field(IRI_Mean) >= Get_Number(0) AND 
(
(Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR 
(Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0))
)

```

Original:
```text
(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) = '1' OR LEFT(Get_Field(e8613014-fa1e-4da2-ae75-c77b722d9c37),Get_Number(1))='2' OR LEFT(Get_Field(e8613014-fa1e-4da2-ae75-c77b722d9c37),Get_Number(1))='4') AND 
Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = '2' AND 
Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND 
(
(Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR 
(Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0))
)

```

<a id="e-d081a60d-2336-49ea-9f80-dbf2b6875169"></a>

## PMS_abfOBJ_Analysis_TAMP_NON_INT_NHS

Source: `dTIMSExpressions` / `d081a60d-2336-49ea-9f80-dbf2b6875169`.



Readable:
```text
 IF((LEFT(Get_Field(Fed_Aid),Get_Number(1))='2' OR LEFT(Get_Field(Fed_Aid),Get_Number(1))='4') AND  NOT   Get_Exp(PMS_abfOBJ_IM_Funds),TRUE,FALSE) AND Get_Field(Lane) = Get_Number(1) AND 
 Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND 
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
 IF((LEFT(Get_Field(e8613014-fa1e-4da2-ae75-c77b722d9c37),Get_Number(1))='2' OR LEFT(Get_Field(e8613014-fa1e-4da2-ae75-c77b722d9c37),Get_Number(1))='4') AND  NOT   Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7),TRUE,FALSE) AND Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1) AND 
 Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-d59437d8-9f72-43f4-84f8-c8ba02c86f07"></a>

## PMS_abfOBJ_Analysis_TAMP_NON_INT_NHS_Tenth

Source: `dTIMSExpressions` / `d59437d8-9f72-43f4-84f8-c8ba02c86f07`.

Map 21 Non Interstate NHS Tenth Mile

Readable:
```text
IF((LEFT(Get_Field(Fed_Aid),Get_Number(1))='2' OR LEFT(Get_Field(Fed_Aid),Get_Number(1))='4') AND  NOT    Get_Exp(PMS_abfOBJ_IM_Funds),TRUE,FALSE) AND Get_Field(Lane) = Get_Number(2) AND
Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0) AND
((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
```

Original:
```text
IF((LEFT(Get_Field(e8613014-fa1e-4da2-ae75-c77b722d9c37),Get_Number(1))='2' OR LEFT(Get_Field(e8613014-fa1e-4da2-ae75-c77b722d9c37),Get_Number(1))='4') AND  NOT    Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7),TRUE,FALSE) AND Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(2) AND
Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND
((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
```

<a id="e-ef4a2d1b-2435-4055-aaaa-35edfb225a35"></a>

## PMS_abfOBJ_Analysis_TAMP_NON_NHS

Source: `dTIMSExpressions` / `ef4a2d1b-2435-4055-aaaa-35edfb225a35`.

TAMP 2021 Non NHS

Readable:
```text
Get_Field(TAMP_CLASS)='NON_NHS' AND 
Get_Field(Lane) = '1' AND 
(
    Get_Field(Com_Year) >= Get_Number(1) OR
    (
        Get_Field(IRI_Mean) >= Get_Number(0) AND 
        Get_Field(Rut_Mean) >= Get_Number(0) AND 
        ((Get_Field(CSI) >= Get_Number(0) AND Get_Field(JCI) >= Get_Number(0)) OR 
        (Get_Field(ECI)>=Get_Number(0) AND Get_Field(SCI)>=Get_Number(0)))
    )
)
```

Original:
```text
Get_Field(30893e2c-e624-4622-9fcf-ddf510ede834)='NON_NHS' AND 
Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = '1' AND 
(
    Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0) >= Get_Number(1) OR
    (
        Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND 
        Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0) AND 
        ((Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) AND Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0)) OR 
        (Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)>=Get_Number(0) AND Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)>=Get_Number(0)))
    )
)
```

<a id="e-edb6276b-7e92-46a2-b06e-0ca5f4ba04d3"></a>

## PMS_abfOBJ_Analysis_Test

Source: `dTIMSExpressions` / `edb6276b-7e92-46a2-b06e-0ca5f4ba04d3`.

Analysis test

Readable:
```text
Get_Field(RoadName) = '42200330000EB' OR
Get_Field(RoadName) = '1940017000000' OR
Get_Field(RoadName) = '2340018000000'
```

Original:
```text
Get_Field(74348a00-8c80-440d-92be-aec83d0050e4) = '42200330000EB' OR
Get_Field(74348a00-8c80-440d-92be-aec83d0050e4) = '1940017000000' OR
Get_Field(74348a00-8c80-440d-92be-aec83d0050e4) = '2340018000000'
```

<a id="e-89f605eb-5896-4f3b-bf54-244e6a6ad2b9"></a>

## PMS_abfOBJ_Analysis_Test_Tenth_Mile

Source: `dTIMSExpressions` / `89f605eb-5896-4f3b-bf54-244e6a6ad2b9`.

Analysis Test Tenth Mile

Readable:
```text
(Get_Field(RoadName) = '0140011000000' OR
Get_Field(RoadName) = '02100810000NB' OR
Get_Field(RoadName) = '02100810000SB') AND Get_Field(Lane)=Get_Number(2)
```

Original:
```text
(Get_Field(74348a00-8c80-440d-92be-aec83d0050e4) = '0140011000000' OR
Get_Field(74348a00-8c80-440d-92be-aec83d0050e4) = '02100810000NB' OR
Get_Field(74348a00-8c80-440d-92be-aec83d0050e4) = '02100810000SB') AND Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15)=Get_Number(2)
```

<a id="e-915f80f1-74d8-48c0-ab9f-fdffd05d547a"></a>

## PMS_abfOBJ_Asphalt

Source: `RuntimeExpressions` / `915f80f1-74d8-48c0-ab9f-fdffd05d547a`.



Readable:
```text
GET_ANALVR(PMS_tDAV_Pave_Type) = 'BC'
```

Original:
```text
GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) = 'BC'
```

<a id="e-ed85c601-a662-40d6-b7ad-e303e159c594"></a>

## PMS_abfOBJ_BC_Initial_H

Source: `RuntimeExpressions` / `ed85c601-a662-40d6-b7ad-e303e159c594`.



Readable:
```text
GET_ANALVR(PMS_tDAV_Pave_Type) = 'BC' AND GET_ANALVR(PMS_tDAV_Rehab_Type) = 'Initial' AND GET_ANALVR(PMS_tDAV_Truck_Load) = 'H'
```

Original:
```text
GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) = 'BC' AND GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) = 'Initial' AND GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) = 'H'
```

<a id="e-8ad4877a-f933-462c-bc02-4e36c0724983"></a>

## PMS_abfOBJ_BC_Initial_L

Source: `RuntimeExpressions` / `8ad4877a-f933-462c-bc02-4e36c0724983`.



Readable:
```text
GET_ANALVR(PMS_tDAV_Pave_Type) = 'BC' AND GET_ANALVR(PMS_tDAV_Rehab_Type) = 'Initial' AND GET_ANALVR(PMS_tDAV_Truck_Load) = 'L'
```

Original:
```text
GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) = 'BC' AND GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) = 'Initial' AND GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) = 'L'
```

<a id="e-4f4e80d8-1191-49e7-ab93-f2b69921e289"></a>

## PMS_abfOBJ_BC_Major_H

Source: `RuntimeExpressions` / `4f4e80d8-1191-49e7-ab93-f2b69921e289`.



Readable:
```text
GET_ANALVR(PMS_tDAV_Pave_Type) = 'BC' AND GET_ANALVR(PMS_tDAV_Rehab_Type) = 'Major' AND GET_ANALVR(PMS_tDAV_Truck_Load) = 'H'
```

Original:
```text
GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) = 'BC' AND GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) = 'Major' AND GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) = 'H'
```

<a id="e-013831ee-be8b-4f38-8326-e538edd7eec4"></a>

## PMS_abfOBJ_BC_Major_L

Source: `RuntimeExpressions` / `013831ee-be8b-4f38-8326-e538edd7eec4`.



Readable:
```text
GET_ANALVR(PMS_tDAV_Pave_Type) = 'BC' AND GET_ANALVR(PMS_tDAV_Rehab_Type) = 'Major' AND GET_ANALVR(PMS_tDAV_Truck_Load) = 'L'
```

Original:
```text
GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) = 'BC' AND GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) = 'Major' AND GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) = 'L'
```

<a id="e-690eee27-7d30-4204-8c9f-023e90cd9476"></a>

## PMS_abfOBJ_BC_Minor_H

Source: `RuntimeExpressions` / `690eee27-7d30-4204-8c9f-023e90cd9476`.



Readable:
```text
GET_ANALVR(PMS_tDAV_Pave_Type) = 'BC' AND GET_ANALVR(PMS_tDAV_Rehab_Type) = 'Minor' AND GET_ANALVR(PMS_tDAV_Truck_Load) = 'H'
```

Original:
```text
GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) = 'BC' AND GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) = 'Minor' AND GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) = 'H'
```

<a id="e-00fa23cc-f5c1-4a60-afe4-0b98324b08db"></a>

## PMS_abfOBJ_BC_Minor_L

Source: `RuntimeExpressions` / `00fa23cc-f5c1-4a60-afe4-0b98324b08db`.



Readable:
```text
GET_ANALVR(PMS_tDAV_Pave_Type) = 'BC' AND GET_ANALVR(PMS_tDAV_Rehab_Type) = 'Minor' AND GET_ANALVR(PMS_tDAV_Truck_Load) = 'L'
```

Original:
```text
GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) = 'BC' AND GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) = 'Minor' AND GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) = 'L'
```

<a id="e-4fe43cd4-0b33-4b05-85fc-d4eedad0e37b"></a>

## PMS_abfOBJ_CO

Source: `dTIMSExpressions` / `4fe43cd4-0b33-4b05-85fc-d4eedad0e37b`.

Routes eligible for Interstate Maintenance funds

Readable:
```text
IF(Get_Field(Sign) = '4',TRUE,FALSE)
```

Original:
```text
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) = '4',TRUE,FALSE)
```

<a id="e-298f95f6-6a69-41e7-930a-6d6585535b4b"></a>

## PMS_abfOBJ_CO_Analysis

Source: `dTIMSExpressions` / `298f95f6-6a69-41e7-930a-6d6585535b4b`.

CO Routes Analysis Sections

Readable:
```text
Get_Exp(PMS_abfOBJ_Valid_Analysis_Section) AND Get_Exp(PMS_abfOBJ_CO)
```

Original:
```text
Get_Exp(d7d1be3c-b7bc-4ff7-b551-6f8730fbb39c) AND Get_Exp(4fe43cd4-0b33-4b05-85fc-d4eedad0e37b)
```

<a id="e-6fa1ef61-d228-4a7b-b87c-fbe41225713d"></a>

## PMS_abfOBJ_Com_Year

Source: `dTIMSExpressions` / `6fa1ef61-d228-4a7b-b87c-fbe41225713d`.



Readable:
```text
YEAR(Get_Field(STIP_END_DATE)) >=Get_Number(2018)
```

Original:
```text
YEAR(Get_Field(49ecaefc-4cd6-4d0a-a801-ee7c919c73e9)) >=Get_Number(2018)
```

<a id="e-ba469472-994d-4555-923b-c833047e7e8b"></a>

## PMS_abfOBJ_Concrete

Source: `RuntimeExpressions` / `ba469472-994d-4555-923b-c833047e7e8b`.



Readable:
```text
GET_ANALVR(PMS_tDAV_Pave_Type) = 'RC'
```

Original:
```text
GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) = 'RC'
```

<a id="e-c47245c5-a573-4225-898f-8a3ac728bdee"></a>

## PMS_abfOBJ_D4_Analysis

Source: `dTIMSExpressions` / `c47245c5-a573-4225-898f-8a3ac728bdee`.

Valid Analysis for D4 Primaries

Readable:
```text
Get_Exp(PMS_abfOBJ_Valid_Analysis_Section) AND Get_Exp(PMS_abfOBJ_District4_Primary) 
```

Original:
```text
Get_Exp(d7d1be3c-b7bc-4ff7-b551-6f8730fbb39c) AND Get_Exp(35212cbb-8aa4-4220-8a17-f10e0d261918) 
```

<a id="e-35212cbb-8aa4-4220-8a17-f10e0d261918"></a>

## PMS_abfOBJ_District4_Primary

Source: `dTIMSExpressions` / `35212cbb-8aa4-4220-8a17-f10e0d261918`.

All D4 US Routes for Analysis

Readable:
```text
IF(Get_Field(Dist) ='4' AND Get_Field(Sign)='2',TRUE,FALSE) 
```

Original:
```text
IF(Get_Field(df7e2acc-a05b-47dd-bb81-87b419d02677) ='4' AND Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='2',TRUE,FALSE) 
```

<a id="e-b3fe6710-ecd4-46aa-ae5c-4696685576bf"></a>

## PMS_abfOBJ_False

Source: `dTIMSExpressions` / `b3fe6710-ecd4-46aa-ae5c-4696685576bf`.

False

Readable:
```text
FALSE
```

Original:
```text
FALSE
```

<a id="e-4c811992-2c2d-42c6-b156-c4d16973b739"></a>

## PMS_abfOBJ_I68

Source: `dTIMSExpressions` / `4c811992-2c2d-42c6-b156-c4d16973b739`.

I-68 for inclusion in APD and exclusion from IM funding

Readable:
```text
IF(Get_Field(Sign) = '1' AND Get_Field(Rte) = '68',TRUE,FALSE)
```

Original:
```text
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) = '1' AND Get_Field(d1013dc9-2130-457f-a607-a73bc1dd3537) = '68',TRUE,FALSE)
```

<a id="e-1be07652-db7b-492b-8923-a471bbd309e7"></a>

## PMS_abfOBJ_IM_Funds

Source: `dTIMSExpressions` / `1be07652-db7b-492b-8923-a471bbd309e7`.

Routes eligible for Interstate Maintenance funds

Readable:
```text
IF(LEFT(Get_Field(Sign),Get_Number(1)) = '1' AND (NOT  Get_Exp(PMS_abfOBJ_TP)),TRUE,FALSE)
```

Original:
```text
IF(LEFT(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c),Get_Number(1)) = '1' AND (NOT  Get_Exp(c1fcd884-076e-40e8-a2ce-c59e6f7fd0b9)),TRUE,FALSE)
```

<a id="e-d7ace869-9170-4122-99c7-2f2f61968499"></a>

## PMS_abfOBJ_IS_US

Source: `dTIMSExpressions` / `d7ace869-9170-4122-99c7-2f2f61968499`.

Sections included in Interstate & US

Readable:
```text
IF((Get_Field(Sign) ='1' OR Get_Field(Sign) = '2') ,TRUE,FALSE)
```

Original:
```text
IF((Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) ='1' OR Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) = '2') ,TRUE,FALSE)
```

<a id="e-abceed82-d21c-4966-a4b5-7a6e028bcd23"></a>

## PMS_abfOBJ_IS_US_Analysis

Source: `dTIMSExpressions` / `abceed82-d21c-4966-a4b5-7a6e028bcd23`.



Readable:
```text
Get_Exp(PMS_abfOBJ_Valid_Analysis_Section) AND Get_Exp(PMS_abfOBJ_IS_US)
```

Original:
```text
Get_Exp(d7d1be3c-b7bc-4ff7-b551-6f8730fbb39c) AND Get_Exp(d7ace869-9170-4122-99c7-2f2f61968499)
```

<a id="e-b2f53720-cf55-42d0-9a54-d4e1a3429669"></a>

## PMS_abfOBJ_IS_US_WV

Source: `dTIMSExpressions` / `b2f53720-cf55-42d0-9a54-d4e1a3429669`.

Sections included in Interstate, US, & WV

Readable:
```text
IF((Get_Field(Sign) ='1' OR Get_Field(Sign) = '2' OR Get_Field(Sign) = '3') ,TRUE,FALSE)
```

Original:
```text
IF((Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) ='1' OR Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) = '2' OR Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) = '3') ,TRUE,FALSE)
```

<a id="e-a97d5dd6-0a84-4364-9b83-f0749985772b"></a>

## PMS_abfOBJ_IS_US_WV_Analysis

Source: `dTIMSExpressions` / `a97d5dd6-0a84-4364-9b83-f0749985772b`.



Readable:
```text
Get_Exp(PMS_abfOBJ_Valid_Analysis_Section) AND Get_Exp(PMS_abfOBJ_IS_US_WV)
```

Original:
```text
Get_Exp(d7d1be3c-b7bc-4ff7-b551-6f8730fbb39c) AND Get_Exp(b2f53720-cf55-42d0-9a54-d4e1a3429669)
```

<a id="e-ae49292b-a4e1-43fa-a70c-e0b952c182ad"></a>

## PMS_abfOBJ_InterstateAnalysis

Source: `dTIMSExpressions` / `ae49292b-a4e1-43fa-a70c-e0b952c182ad`.

Analysis Sections for Interstate

Readable:
```text
Get_Exp(PMS_abfOBJ_Valid_Analysis_Section) AND Get_Exp(PMS_abfOBJ_IM_Funds) AND Get_Field(Lane) = Get_Number(1)
```

Original:
```text
Get_Exp(d7d1be3c-b7bc-4ff7-b551-6f8730fbb39c) AND Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7) AND Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1)
```

<a id="e-5a1a31cf-80f4-44c8-abaf-e73b5006ae6e"></a>

## PMS_abfOBJ_NHS

Source: `dTIMSExpressions` / `5a1a31cf-80f4-44c8-abaf-e73b5006ae6e`.

NHS Expression

Readable:
```text
IF((LEFT(Get_Field(Fed_Aid),Get_Number(1))='2' OR LEFT(Get_Field(Fed_Aid),Get_Number(1))='4') AND NOT      
Get_Exp(DEL_APD) AND NOT      
Get_Exp(PMS_abfOBJ_IM_Funds),TRUE,FALSE)
```

Original:
```text
IF((LEFT(Get_Field(e8613014-fa1e-4da2-ae75-c77b722d9c37),Get_Number(1))='2' OR LEFT(Get_Field(e8613014-fa1e-4da2-ae75-c77b722d9c37),Get_Number(1))='4') AND NOT      
Get_Exp(1fe2f8d3-ae39-446f-9f02-c05c851d10e5) AND NOT      
Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7),TRUE,FALSE)
```

<a id="e-be7c81a0-4f52-431a-93c0-7806cd4524dd"></a>

## PMS_abfOBJ_NHS_Analysis

Source: `dTIMSExpressions` / `be7c81a0-4f52-431a-93c0-7806cd4524dd`.



Readable:
```text
Get_Exp(PMS_abfOBJ_Valid_Analysis_Section) AND Get_Exp(PMS_abfOBJ_NHS)
```

Original:
```text
Get_Exp(d7d1be3c-b7bc-4ff7-b551-6f8730fbb39c) AND Get_Exp(5a1a31cf-80f4-44c8-abaf-e73b5006ae6e)
```

<a id="e-befb48a6-7b27-4dad-9e9d-be27d0d18cde"></a>

## PMS_abfOBJ_NHS_Non_Interstate

Source: `dTIMSExpressions` / `befb48a6-7b27-4dad-9e9d-be27d0d18cde`.

NHS Non Interstate

Readable:
```text
IF((LEFT(Get_Field(Fed_Aid),Get_Number(1))='2' OR LEFT(Get_Field(Fed_Aid),Get_Number(1))='4') AND  NOT    Get_Exp(PMS_abfOBJ_IM_Funds),TRUE,FALSE) AND Get_Field(Lane) = Get_Number(1)
AND Get_Field(IRI_Mean) >= Get_Number(0) AND Get_Field(Rut_Mean) >= Get_Number(0)
```

Original:
```text
IF((LEFT(Get_Field(e8613014-fa1e-4da2-ae75-c77b722d9c37),Get_Number(1))='2' OR LEFT(Get_Field(e8613014-fa1e-4da2-ae75-c77b722d9c37),Get_Number(1))='4') AND  NOT    Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7),TRUE,FALSE) AND Get_Field(d9e83b68-1af7-4dd7-8adf-17ad85280d15) = Get_Number(1)
AND Get_Field(27134121-7932-4a33-8c47-a44035638fed) >= Get_Number(0) AND Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c) >= Get_Number(0)
```

<a id="e-4896a6a1-cc30-4aa6-9272-f6c2e8ddbc1c"></a>

## PMS_abfOBJ_NHSall

Source: `dTIMSExpressions` / `4896a6a1-cc30-4aa6-9272-f6c2e8ddbc1c`.

NHS Expression

Readable:
```text
IF(LEFT(Get_Field(Fed_Aid),Get_Number(1))='2' OR LEFT(Get_Field(Fed_Aid),Get_Number(1))='1' OR LEFT(Get_Field(Fed_Aid),Get_Number(1))='7' OR LEFT(Get_Field(Fed_Aid),Get_Number(1))='4' ,TRUE,FALSE)
```

Original:
```text
IF(LEFT(Get_Field(e8613014-fa1e-4da2-ae75-c77b722d9c37),Get_Number(1))='2' OR LEFT(Get_Field(e8613014-fa1e-4da2-ae75-c77b722d9c37),Get_Number(1))='1' OR LEFT(Get_Field(e8613014-fa1e-4da2-ae75-c77b722d9c37),Get_Number(1))='7' OR LEFT(Get_Field(e8613014-fa1e-4da2-ae75-c77b722d9c37),Get_Number(1))='4' ,TRUE,FALSE)
```

<a id="e-e08363c3-4432-4f42-9be5-0e62047f7477"></a>

## PMS_abfOBJ_NHSall_Analysis

Source: `dTIMSExpressions` / `e08363c3-4432-4f42-9be5-0e62047f7477`.



Readable:
```text
Get_Exp(PMS_abfOBJ_Valid_Analysis_Section) AND Get_Exp(PMS_abfOBJ_NHSall)
```

Original:
```text
Get_Exp(d7d1be3c-b7bc-4ff7-b551-6f8730fbb39c) AND Get_Exp(4896a6a1-cc30-4aa6-9272-f6c2e8ddbc1c)
```

<a id="e-b42ef03d-e67c-4ea5-8db6-81604addf907"></a>

## PMS_abfOBJ_NonNHS

Source: `dTIMSExpressions` / `b42ef03d-e67c-4ea5-8db6-81604addf907`.

All Non NHS Routes Excluding CO Routes

Readable:
```text
NOT    (Get_Exp(PMS_abfOBJ_NHSall) OR Get_Exp(PMS_abfOBJ_TP))


//IF((Analysis->Sign='2' AND Analysis->Fed_Aid <> '2') OR
//   (Analysis->Sign='3' AND Analysis->Fed_Aid <> '2') OR
//   (Analysis->Sign='4' AND Analysis->Fed_Aid = '3')
//,TRUE,FALSE)
```

Original:
```text
NOT    (Get_Exp(4896a6a1-cc30-4aa6-9272-f6c2e8ddbc1c) OR Get_Exp(c1fcd884-076e-40e8-a2ce-c59e6f7fd0b9))


//IF((Analysis->Sign='2' AND Analysis->Fed_Aid <> '2') OR
//   (Analysis->Sign='3' AND Analysis->Fed_Aid <> '2') OR
//   (Analysis->Sign='4' AND Analysis->Fed_Aid = '3')
//,TRUE,FALSE)
```

<a id="e-739b38cb-0037-49d1-9445-6fc4f0e74587"></a>

## PMS_abfOBJ_NonNHSAnalysis

Source: `dTIMSExpressions` / `739b38cb-0037-49d1-9445-6fc4f0e74587`.



Readable:
```text
Get_Exp(PMS_abfOBJ_Valid_Analysis_Section) AND Get_Exp(PMS_abfOBJ_NonNHS)
```

Original:
```text
Get_Exp(d7d1be3c-b7bc-4ff7-b551-6f8730fbb39c) AND Get_Exp(b42ef03d-e67c-4ea5-8db6-81604addf907)
```

<a id="e-3b4d7bfc-1f61-4129-98ca-77d527dc8db4"></a>

## PMS_abfOBJ_RC_Initial_H

Source: `RuntimeExpressions` / `3b4d7bfc-1f61-4129-98ca-77d527dc8db4`.



Readable:
```text
GET_ANALVR(PMS_tDAV_Pave_Type) = 'RC' AND GET_ANALVR(PMS_tDAV_Rehab_Type) = 'Initial' AND GET_ANALVR(PMS_tDAV_Truck_Load) = 'H'
```

Original:
```text
GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) = 'RC' AND GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) = 'Initial' AND GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) = 'H'
```

<a id="e-e0c16931-d57e-44f1-b012-ad8e44d11cbe"></a>

## PMS_abfOBJ_RC_Initial_L

Source: `RuntimeExpressions` / `e0c16931-d57e-44f1-b012-ad8e44d11cbe`.



Readable:
```text
GET_ANALVR(PMS_tDAV_Pave_Type) = 'RC' AND GET_ANALVR(PMS_tDAV_Rehab_Type) = 'Initial' AND GET_ANALVR(PMS_tDAV_Truck_Load) = 'L'
```

Original:
```text
GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) = 'RC' AND GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) = 'Initial' AND GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) = 'L'
```

<a id="e-a0915cf4-27a3-4e6d-89ff-09ab2064a119"></a>

## PMS_abfOBJ_RC_Major_H

Source: `RuntimeExpressions` / `a0915cf4-27a3-4e6d-89ff-09ab2064a119`.



Readable:
```text
GET_ANALVR(PMS_tDAV_Pave_Type) = 'RC' AND GET_ANALVR(PMS_tDAV_Rehab_Type) = 'Major' AND GET_ANALVR(PMS_tDAV_Truck_Load) = 'H'
```

Original:
```text
GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) = 'RC' AND GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) = 'Major' AND GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) = 'H'
```

<a id="e-36b593a1-3af9-40f9-ab3e-16b13fff68ac"></a>

## PMS_abfOBJ_RC_Major_L

Source: `RuntimeExpressions` / `36b593a1-3af9-40f9-ab3e-16b13fff68ac`.



Readable:
```text
GET_ANALVR(PMS_tDAV_Pave_Type) = 'RC' AND GET_ANALVR(PMS_tDAV_Rehab_Type) = 'Major' AND GET_ANALVR(PMS_tDAV_Truck_Load) = 'L'
```

Original:
```text
GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) = 'RC' AND GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) = 'Major' AND GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) = 'L'
```

<a id="e-2ec04573-98c1-4857-aa38-9b2f54248dd3"></a>

## PMS_abfOBJ_RC_Minor_H

Source: `RuntimeExpressions` / `2ec04573-98c1-4857-aa38-9b2f54248dd3`.



Readable:
```text
GET_ANALVR(PMS_tDAV_Pave_Type) = 'RC' AND GET_ANALVR(PMS_tDAV_Rehab_Type) = 'Minor' AND GET_ANALVR(PMS_tDAV_Truck_Load) = 'H'
```

Original:
```text
GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) = 'RC' AND GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) = 'Minor' AND GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) = 'H'
```

<a id="e-db61024b-8046-4dce-807a-42db8a93fe90"></a>

## PMS_abfOBJ_RC_Minor_L

Source: `RuntimeExpressions` / `db61024b-8046-4dce-807a-42db8a93fe90`.



Readable:
```text
GET_ANALVR(PMS_tDAV_Pave_Type) = 'RC' AND GET_ANALVR(PMS_tDAV_Rehab_Type) = 'Minor' AND GET_ANALVR(PMS_tDAV_Truck_Load) = 'L'
```

Original:
```text
GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) = 'RC' AND GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) = 'Minor' AND GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) = 'L'
```

<a id="e-6b48d00e-66b3-4840-9e09-4ef127f47ceb"></a>

## PMS_abfOBJ_RSL_CCI

Source: `RuntimeExpressions` / `6b48d00e-66b3-4840-9e09-4ef127f47ceb`.



Readable:
```text
Get_Exp(PMS_ancCND_CCI_RSL) < GET_ANALVR(PMS_nAAV_CND_RSL)
```

Original:
```text
Get_Exp(ea0596f8-2e1b-4a7b-9a8a-3cbddb992f82) < GET_ANALVR(93a9dd02-8d95-4df2-bc7b-99a91b86029c)
```

<a id="e-f4fd9cb2-05bf-4d3d-9510-57fd8ad280c5"></a>

## PMS_abfOBJ_RSL_CSI

Source: `RuntimeExpressions` / `f4fd9cb2-05bf-4d3d-9510-57fd8ad280c5`.



Readable:
```text
GET_ANALVR(PMS_tDAV_Pave_Type) = 'RC' AND Get_Exp(PMS_ancCND_CSI_RSL) < GET_ANALVR(PMS_nAAV_CND_RSL)
```

Original:
```text
GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) = 'RC' AND Get_Exp(1de251ee-bc69-4d3a-9fa7-7c09071eca38) < GET_ANALVR(93a9dd02-8d95-4df2-bc7b-99a91b86029c)
```

<a id="e-26473620-5978-4df6-9857-7965f92dfe55"></a>

## PMS_abfOBJ_RSL_ECI

Source: `RuntimeExpressions` / `26473620-5978-4df6-9857-7965f92dfe55`.



Readable:
```text
GET_ANALVR(PMS_tDAV_Pave_Type) = 'BC' AND Get_Exp(PMS_ancCND_ECI_RSL) < GET_ANALVR(PMS_nAAV_CND_RSL)
```

Original:
```text
GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) = 'BC' AND Get_Exp(f80bc936-95cf-4aa7-8d49-ffacd24fb8ed) < GET_ANALVR(93a9dd02-8d95-4df2-bc7b-99a91b86029c)
```

<a id="e-e03d2676-899e-403b-8725-10b8b3b1370b"></a>

## PMS_abfOBJ_RSL_JCI

Source: `RuntimeExpressions` / `e03d2676-899e-403b-8725-10b8b3b1370b`.



Readable:
```text
GET_ANALVR(PMS_tDAV_Pave_Type) = 'RC' AND Get_Exp(PMS_ancCND_JCI_RSL) < GET_ANALVR(PMS_nAAV_CND_RSL)
```

Original:
```text
GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) = 'RC' AND Get_Exp(88b8dd8a-42ee-482b-99bd-adb6d378ad87) < GET_ANALVR(93a9dd02-8d95-4df2-bc7b-99a91b86029c)
```

<a id="e-27808033-ed35-4925-949a-9130829a523c"></a>

## PMS_abfOBJ_RSL_RDI

Source: `RuntimeExpressions` / `27808033-ed35-4925-949a-9130829a523c`.



Readable:
```text
Get_Exp(PMS_ancCND_RDI_RSL) < GET_ANALVR(PMS_nAAV_CND_RSL)
```

Original:
```text
Get_Exp(9b84a780-f71e-4bf0-97f0-82c235067efe) < GET_ANALVR(93a9dd02-8d95-4df2-bc7b-99a91b86029c)
```

<a id="e-9d8fe7a5-40e7-4ad2-8930-58fc04013895"></a>

## PMS_abfOBJ_RSL_SCI

Source: `RuntimeExpressions` / `9d8fe7a5-40e7-4ad2-8930-58fc04013895`.



Readable:
```text
GET_ANALVR(PMS_tDAV_Pave_Type) = 'BC' AND Get_Exp(PMS_ancCND_SCI_RSL) < GET_ANALVR(PMS_nAAV_CND_RSL)
```

Original:
```text
GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) = 'BC' AND Get_Exp(743b5c2f-8470-429c-9665-795ce12ccc8c) < GET_ANALVR(93a9dd02-8d95-4df2-bc7b-99a91b86029c)
```

<a id="e-c1fcd884-076e-40e8-a2ce-c59e6f7fd0b9"></a>

## PMS_abfOBJ_TP

Source: `dTIMSExpressions` / `c1fcd884-076e-40e8-a2ce-c59e6f7fd0b9`.

Exclude WVTP from analysis

Readable:
```text
IF(Get_Field(Sign) = '1' AND Get_Field(Rte) = '0077' AND Get_Field(Supp) = '16',TRUE,FALSE) OR 
(
    Get_Field(Name) = '41100640000EB-117.930-1' OR 
    Get_Field(Name) = '41100640000EB-120.800-1' OR
    Get_Field(Name) = '41100640000EB-124.530-1' OR
    Get_Field(Name) = '41100640000EB-129.890-1' OR
    Get_Field(Name) = '41100640000EB-133.000-1' 
)
```

Original:
```text
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) = '1' AND Get_Field(d1013dc9-2130-457f-a607-a73bc1dd3537) = '0077' AND Get_Field(f5e7bd00-45b2-409f-9bc0-8cf6f35570a4) = '16',TRUE,FALSE) OR 
(
    Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b) = '41100640000EB-117.930-1' OR 
    Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b) = '41100640000EB-120.800-1' OR
    Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b) = '41100640000EB-124.530-1' OR
    Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b) = '41100640000EB-129.890-1' OR
    Get_Field(e62e9b1d-1075-4c24-926d-89fcff8c015b) = '41100640000EB-133.000-1' 
)
```

<a id="e-295a4cec-7744-4cce-ad7b-470c6cb4f56c"></a>

## PMS_abfOBJ_True

Source: `dTIMSExpressions` / `295a4cec-7744-4cce-ad7b-470c6cb4f56c`.

True

Readable:
```text
TRUE
```

Original:
```text
TRUE
```

<a id="e-c9f60f0c-4eac-44bf-8667-d89455ba6e68"></a>

## PMS_abfOBJ_US

Source: `dTIMSExpressions` / `c9f60f0c-4eac-44bf-8667-d89455ba6e68`.

US Routes that are not APD

Readable:
```text
IF(Get_Field(Sign) = '2' AND Get_Field(Spec_Sys)<>'10',TRUE,FALSE)
```

Original:
```text
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) = '2' AND Get_Field(51f41088-b57b-4756-9b09-b108c4a81640)<>'10',TRUE,FALSE)
```

<a id="e-e63d3235-72c4-411c-b69c-4b4ea2c845a1"></a>

## PMS_abfOBJ_US_Analysis

Source: `dTIMSExpressions` / `e63d3235-72c4-411c-b69c-4b4ea2c845a1`.

US route Analysis

Readable:
```text
Get_Exp(PMS_abfOBJ_Valid_Analysis_Section) AND Get_Exp(PMS_abfOBJ_US)
```

Original:
```text
Get_Exp(d7d1be3c-b7bc-4ff7-b551-6f8730fbb39c) AND Get_Exp(c9f60f0c-4eac-44bf-8667-d89455ba6e68)
```

<a id="e-d7d1be3c-b7bc-4ff7-b551-6f8730fbb39c"></a>

## PMS_abfOBJ_Valid_Analysis_Section

Source: `dTIMSExpressions` / `d7d1be3c-b7bc-4ff7-b551-6f8730fbb39c`.

Analysis sections valid for analysis

Readable:
```text
Get_Field(Com_Year)>= Get_Number(1) OR
(
    (
    (Get_Field(Surf_Wd) > Get_Number(0) AND
    (Get_Exp(PMS_ancOBJ_Pave_type_Initial) = 'BC' OR Get_Exp(PMS_ancOBJ_Pave_type_Initial) = 'RC') AND 
    ( NOT     IFDEFAULT(Get_Field(CSI)) OR Get_Field(CSI) >= Get_Number(0) OR Get_Field(ECI) >= Get_Number(0) OR Get_Field(JCI) >= Get_Number(0) OR 
    Get_Field(PSI) >= Get_Number(0) OR Get_Field(RDI) >= Get_Number(0) OR Get_Field(SCI) >= Get_Number(0))) 
    OR ( NOT     IFDEFAULT(Get_Field(Com_Year)))
    )
    AND LEFT(Get_Field(Supp),Get_Number(2)) <> '17'
)
```

Original:
```text
Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)>= Get_Number(1) OR
(
    (
    (Get_Field(cf5fc56b-610b-4438-9053-583b01cc5d4f) > Get_Number(0) AND
    (Get_Exp(09c7fde6-cc65-4701-9ecc-e3e705983d08) = 'BC' OR Get_Exp(09c7fde6-cc65-4701-9ecc-e3e705983d08) = 'RC') AND 
    ( NOT     IFDEFAULT(Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5)) OR Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5) >= Get_Number(0) OR Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4) >= Get_Number(0) OR Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050) >= Get_Number(0) OR 
    Get_Field(1eca4d42-a141-4b12-8457-f11b987a6710) >= Get_Number(0) OR Get_Field(be1a4d5a-ea19-4e1a-a61d-c1b792828006) >= Get_Number(0) OR Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04) >= Get_Number(0))) 
    OR ( NOT     IFDEFAULT(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)))
    )
    AND LEFT(Get_Field(f5e7bd00-45b2-409f-9bc0-8cf6f35570a4),Get_Number(2)) <> '17'
)
```

<a id="e-8aa00f9f-b137-4f05-8875-62bdeeb0cc77"></a>

## PMS_abfOBJ_WV

Source: `dTIMSExpressions` / `8aa00f9f-b137-4f05-8875-62bdeeb0cc77`.

WV Routes

Readable:
```text
IF(Get_Field(Sign) = '3',TRUE,FALSE)
```

Original:
```text
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) = '3',TRUE,FALSE)
```

<a id="e-6716a493-182f-49bb-b909-12e73f72bf83"></a>

## PMS_abfOBJ_WVTP_Analysis

Source: `dTIMSExpressions` / `6716a493-182f-49bb-b909-12e73f72bf83`.

TP Analysis

Readable:
```text
Get_Exp(PMS_abfOBJ_Valid_Analysis_Section) AND Get_Exp(PMS_abfOBJ_TP)
```

Original:
```text
Get_Exp(d7d1be3c-b7bc-4ff7-b551-6f8730fbb39c) AND Get_Exp(c1fcd884-076e-40e8-a2ce-c59e6f7fd0b9)
```

<a id="e-1011dd54-dd28-4674-92df-c2f8371a051e"></a>

## PMS_abfOBJ_WV_Analysis

Source: `dTIMSExpressions` / `1011dd54-dd28-4674-92df-c2f8371a051e`.

WV Routes Analysis Sections

Readable:
```text
Get_Exp(PMS_abfOBJ_Valid_Analysis_Section) AND Get_Exp(PMS_abfOBJ_WV)
```

Original:
```text
Get_Exp(d7d1be3c-b7bc-4ff7-b551-6f8730fbb39c) AND Get_Exp(8aa00f9f-b137-4f05-8875-62bdeeb0cc77)
```

<a id="e-c7b6c5b3-3bbb-47a1-b07a-ce931ae48f32"></a>

## PMS_abfTRIG_Conc_Pvmt_Repair_Major

Source: `RuntimeExpressions` / `c7b6c5b3-3bbb-47a1-b07a-ce931ae48f32`.

Trigger for Concrete Pavement Repair Major

Readable:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(Com_Year),MAX(Get_Field(COM_YR_2),MAX(Get_Field(COM_YR_3),Get_Field(COM_YR_4)))),
(Get_Field(Com_Trt) = 'PMS_Major_CPR_Diamond_Grind' AND Get_Field(Com_Year) = YR)  OR
(Get_Field(COM_TRT_2) = 'PMS_Major_CPR_Diamond_Grind' AND Get_Field(COM_YR_2) = YR)  OR
(Get_Field(COM_TRT_3) = 'PMS_Major_CPR_Diamond_Grind' AND Get_Field(COM_YR_3) = YR)  OR
(Get_Field(COM_TRT_4) = 'PMS_Major_CPR_Diamond_Grind' AND Get_Field(COM_YR_4) = YR)
,
Get_Field(Length) >= Get_Number(3) AND Get_Exp(PMS_abfOBJ_Concrete) AND 
(
(
    GET_ANALVR(PMS_nAAV_CND_PSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','MAJOR_CPR_DG_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_PSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','MAJOR_CPR_DG_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_JCI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_LOWER','KEY','MAJOR_CPR_DG_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_JCI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_UPPER','KEY','MAJOR_CPR_DG_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_CSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_LOWER','KEY','MAJOR_CPR_DG_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_CSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_UPPER','KEY','MAJOR_CPR_DG_1',TRUE))
)                                                                           
OR                                                                          
(                                                                           
    GET_ANALVR(PMS_nAAV_CND_PSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','MAJOR_CPR_DG_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_PSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','MAJOR_CPR_DG_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_JCI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_LOWER','KEY','MAJOR_CPR_DG_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_JCI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_UPPER','KEY','MAJOR_CPR_DG_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_CSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_LOWER','KEY','MAJOR_CPR_DG_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_CSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_UPPER','KEY','MAJOR_CPR_DG_2',TRUE))
)                                                                           
OR                                                                          
(                                                                           
    GET_ANALVR(PMS_nAAV_CND_PSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','MAJOR_CPR_DG_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_PSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','MAJOR_CPR_DG_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_JCI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_LOWER','KEY','MAJOR_CPR_DG_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_JCI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_UPPER','KEY','MAJOR_CPR_DG_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_CSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_LOWER','KEY','MAJOR_CPR_DG_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_CSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_UPPER','KEY','MAJOR_CPR_DG_3',TRUE))
)
)
)
```

Original:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0),MAX(Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),MAX(Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)))),
(Get_Field(ec965cc6-5ed5-4591-bf5b-1c0885ef785e) = 'PMS_Major_CPR_Diamond_Grind' AND Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0) = YR)  OR
(Get_Field(a2875f19-2f5a-4d09-920c-208664ff67c8) = 'PMS_Major_CPR_Diamond_Grind' AND Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) = YR)  OR
(Get_Field(63019b8f-f66e-4853-8d0c-1c15c7a59395) = 'PMS_Major_CPR_Diamond_Grind' AND Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) = YR)  OR
(Get_Field(262093c5-ae74-44bd-9f4d-264b6096b917) = 'PMS_Major_CPR_Diamond_Grind' AND Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86) = YR)
,
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) >= Get_Number(3) AND Get_Exp(ba469472-994d-4555-923b-c833047e7e8b) AND 
(
(
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','MAJOR_CPR_DG_1',TRUE)) AND
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','MAJOR_CPR_DG_1',TRUE)) AND
    GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_LOWER','KEY','MAJOR_CPR_DG_1',TRUE)) AND
    GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_UPPER','KEY','MAJOR_CPR_DG_1',TRUE)) AND
    GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_LOWER','KEY','MAJOR_CPR_DG_1',TRUE)) AND
    GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_UPPER','KEY','MAJOR_CPR_DG_1',TRUE))
)                                                                           
OR                                                                          
(                                                                           
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','MAJOR_CPR_DG_2',TRUE)) AND
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','MAJOR_CPR_DG_2',TRUE)) AND
    GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_LOWER','KEY','MAJOR_CPR_DG_2',TRUE)) AND
    GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_UPPER','KEY','MAJOR_CPR_DG_2',TRUE)) AND
    GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_LOWER','KEY','MAJOR_CPR_DG_2',TRUE)) AND
    GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_UPPER','KEY','MAJOR_CPR_DG_2',TRUE))
)                                                                           
OR                                                                          
(                                                                           
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','MAJOR_CPR_DG_3',TRUE)) AND
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','MAJOR_CPR_DG_3',TRUE)) AND
    GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_LOWER','KEY','MAJOR_CPR_DG_3',TRUE)) AND
    GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_UPPER','KEY','MAJOR_CPR_DG_3',TRUE)) AND
    GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_LOWER','KEY','MAJOR_CPR_DG_3',TRUE)) AND
    GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_UPPER','KEY','MAJOR_CPR_DG_3',TRUE))
)
)
)
```

<a id="e-f80971b8-1efc-4734-8090-d0e5faea14ff"></a>

## PMS_abfTRIG_Conc_Pvmt_Repair_Minor

Source: `RuntimeExpressions` / `f80971b8-1efc-4734-8090-d0e5faea14ff`.

Concrete Pavement Repair Minor

Readable:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(Com_Year),MAX(Get_Field(COM_YR_2),MAX(Get_Field(COM_YR_3),Get_Field(COM_YR_4)))),
(Get_Field(Com_Trt) = 'PMS_Minor_CPR_Diamond_Grind' AND Get_Field(Com_Year) = YR)  OR
(Get_Field(COM_TRT_2) = 'PMS_Minor_CPR_Diamond_Grind' AND Get_Field(COM_YR_2) = YR)  OR
(Get_Field(COM_TRT_3) = 'PMS_Minor_CPR_Diamond_Grind' AND Get_Field(COM_YR_3) = YR)  OR
(Get_Field(COM_TRT_4) = 'PMS_Minor_CPR_Diamond_Grind' AND Get_Field(COM_YR_4) = YR)
,
Get_Field(Length) >= Get_Number(3) AND Get_Exp(PMS_abfOBJ_Concrete) AND 
(
(
    GET_ANALVR(PMS_nAAV_CND_PSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','MINOR_CPR_DG_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_PSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','MINOR_CPR_DG_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_JCI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_LOWER','KEY','MINOR_CPR_DG_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_JCI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_UPPER','KEY','MINOR_CPR_DG_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_CSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_LOWER','KEY','MINOR_CPR_DG_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_CSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_UPPER','KEY','MINOR_CPR_DG_1',TRUE))
)                                                                           
OR                                                                          
(                                                                           
    GET_ANALVR(PMS_nAAV_CND_PSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','MINOR_CPR_DG_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_PSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','MINOR_CPR_DG_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_JCI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_LOWER','KEY','MINOR_CPR_DG_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_JCI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_UPPER','KEY','MINOR_CPR_DG_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_CSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_LOWER','KEY','MINOR_CPR_DG_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_CSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_UPPER','KEY','MINOR_CPR_DG_2',TRUE))
)                                                                           
OR                                                                          
(                                                                           
    GET_ANALVR(PMS_nAAV_CND_PSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','MINOR_CPR_DG_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_PSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','MINOR_CPR_DG_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_JCI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_LOWER','KEY','MINOR_CPR_DG_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_JCI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_UPPER','KEY','MINOR_CPR_DG_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_CSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_LOWER','KEY','MINOR_CPR_DG_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_CSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_UPPER','KEY','MINOR_CPR_DG_3',TRUE))
)
)
)
```

Original:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0),MAX(Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),MAX(Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)))),
(Get_Field(ec965cc6-5ed5-4591-bf5b-1c0885ef785e) = 'PMS_Minor_CPR_Diamond_Grind' AND Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0) = YR)  OR
(Get_Field(a2875f19-2f5a-4d09-920c-208664ff67c8) = 'PMS_Minor_CPR_Diamond_Grind' AND Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) = YR)  OR
(Get_Field(63019b8f-f66e-4853-8d0c-1c15c7a59395) = 'PMS_Minor_CPR_Diamond_Grind' AND Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) = YR)  OR
(Get_Field(262093c5-ae74-44bd-9f4d-264b6096b917) = 'PMS_Minor_CPR_Diamond_Grind' AND Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86) = YR)
,
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) >= Get_Number(3) AND Get_Exp(ba469472-994d-4555-923b-c833047e7e8b) AND 
(
(
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','MINOR_CPR_DG_1',TRUE)) AND
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','MINOR_CPR_DG_1',TRUE)) AND
    GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_LOWER','KEY','MINOR_CPR_DG_1',TRUE)) AND
    GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_UPPER','KEY','MINOR_CPR_DG_1',TRUE)) AND
    GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_LOWER','KEY','MINOR_CPR_DG_1',TRUE)) AND
    GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_UPPER','KEY','MINOR_CPR_DG_1',TRUE))
)                                                                           
OR                                                                          
(                                                                           
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','MINOR_CPR_DG_2',TRUE)) AND
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','MINOR_CPR_DG_2',TRUE)) AND
    GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_LOWER','KEY','MINOR_CPR_DG_2',TRUE)) AND
    GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_UPPER','KEY','MINOR_CPR_DG_2',TRUE)) AND
    GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_LOWER','KEY','MINOR_CPR_DG_2',TRUE)) AND
    GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_UPPER','KEY','MINOR_CPR_DG_2',TRUE))
)                                                                           
OR                                                                          
(                                                                           
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','MINOR_CPR_DG_3',TRUE)) AND
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','MINOR_CPR_DG_3',TRUE)) AND
    GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_LOWER','KEY','MINOR_CPR_DG_3',TRUE)) AND
    GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_UPPER','KEY','MINOR_CPR_DG_3',TRUE)) AND
    GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_LOWER','KEY','MINOR_CPR_DG_3',TRUE)) AND
    GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_UPPER','KEY','MINOR_CPR_DG_3',TRUE))
)
)
)
```

<a id="e-c0226ede-40da-4205-a0f0-38d8e346b561"></a>

## PMS_abfTRIG_County_Chip_Seal

Source: `RuntimeExpressions` / `c0226ede-40da-4205-a0f0-38d8e346b561`.

Chip Seal Trigger Expression for counties

Readable:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(Com_Year),MAX(Get_Field(COM_YR_2),MAX(Get_Field(COM_YR_3),Get_Field(COM_YR_4)))),
(Get_Field(Com_Trt) = 'PMS_County_Chip_Seal' AND Get_Field(Com_Year) = YR)  OR
(Get_Field(COM_TRT_2) = 'PMS_County_Chip_Seal' AND Get_Field(COM_YR_2) = YR)  OR
(Get_Field(COM_TRT_3) = 'PMS_County_Chip_Seal' AND Get_Field(COM_YR_3) = YR)  OR
(Get_Field(COM_TRT_4) = 'PMS_County_Chip_Seal' AND Get_Field(COM_YR_4) = YR)
,
Get_Field(Length) >= Get_Number(0.5) AND Get_Exp(PMS_abfOBJ_Asphalt) AND GET_ANALVR(PMS_nDAV_CNT_CHIP_SEALS) <= Get_Number(2) AND 
Get_Field(Sign) <> '1' AND (NOT             Get_Exp(PMS_abfOBJ_I68)) AND
GET_ANALVR(PMS_nAAV_TRF_ADT) < Get_Number(1000) AND 
GET_ANALVR(PMS_nAAV_CND_CCI) > Get_Number(2.8) AND GET_ANALVR(PMS_nAAV_CND_CCI) < Get_Number(4) AND
Get_Field(Lanes_Total)<=Get_Number(1))
```

Original:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0),MAX(Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),MAX(Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)))),
(Get_Field(ec965cc6-5ed5-4591-bf5b-1c0885ef785e) = 'PMS_County_Chip_Seal' AND Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0) = YR)  OR
(Get_Field(a2875f19-2f5a-4d09-920c-208664ff67c8) = 'PMS_County_Chip_Seal' AND Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) = YR)  OR
(Get_Field(63019b8f-f66e-4853-8d0c-1c15c7a59395) = 'PMS_County_Chip_Seal' AND Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) = YR)  OR
(Get_Field(262093c5-ae74-44bd-9f4d-264b6096b917) = 'PMS_County_Chip_Seal' AND Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86) = YR)
,
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) >= Get_Number(0.5) AND Get_Exp(915f80f1-74d8-48c0-ab9f-fdffd05d547a) AND GET_ANALVR(7014cb8f-5c5e-4f86-a714-76ec0a7d79a1) <= Get_Number(2) AND 
Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) <> '1' AND (NOT             Get_Exp(4c811992-2c2d-42c6-b156-c4d16973b739)) AND
GET_ANALVR(674cee68-8d0f-4f42-8ec1-227bcc6bb6a4) < Get_Number(1000) AND 
GET_ANALVR(b17f394f-57fd-4efb-8e0e-787d545e45f5) > Get_Number(2.8) AND GET_ANALVR(b17f394f-57fd-4efb-8e0e-787d545e45f5) < Get_Number(4) AND
Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)<=Get_Number(1))
```

<a id="e-e7b820af-96b2-4779-92a3-1757809044e2"></a>

## PMS_abfTRIG_County_Microsurfacing

Source: `RuntimeExpressions` / `e7b820af-96b2-4779-92a3-1757809044e2`.

Microsurfacing Trigger Expression for counties

Readable:
```text
IF(IS_COMMITTED() AND 
    YR <= MAX(Get_Field(Com_Year),MAX(Get_Field(COM_YR_2),MAX(Get_Field(COM_YR_3),Get_Field(COM_YR_4)))),
    (Get_Field(Com_Trt) = 'PMS_County_MicroSurface' AND Get_Field(Com_Year) = YR)  OR
    (Get_Field(COM_TRT_2) = 'PMS_County_MicroSurface' AND Get_Field(COM_YR_2) = YR)  OR
    (Get_Field(COM_TRT_3) = 'PMS_County_MicroSurface' AND Get_Field(COM_YR_3) = YR)  OR
    (Get_Field(COM_TRT_4) = 'PMS_County_MicroSurface' AND Get_Field(COM_YR_4) = YR)
    ,
    Get_Field(Length) >= Get_Number(0.5) AND 
    Get_Exp(PMS_abfOBJ_Asphalt) AND 
    GET_TRTYR('PMS_County_Thick_Overlay') > Get_Number(0) AND 
    YR-GET_TRTYR('PMS_County_Thick_Overlay') >=Get_Number(5) AND 
    YR-GET_TRTYR('PMS_County_Thick_Overlay') <=Get_Number(7)
)

```

Original:
```text
IF(IS_COMMITTED() AND 
    YR <= MAX(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0),MAX(Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),MAX(Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)))),
    (Get_Field(ec965cc6-5ed5-4591-bf5b-1c0885ef785e) = 'PMS_County_MicroSurface' AND Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0) = YR)  OR
    (Get_Field(a2875f19-2f5a-4d09-920c-208664ff67c8) = 'PMS_County_MicroSurface' AND Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) = YR)  OR
    (Get_Field(63019b8f-f66e-4853-8d0c-1c15c7a59395) = 'PMS_County_MicroSurface' AND Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) = YR)  OR
    (Get_Field(262093c5-ae74-44bd-9f4d-264b6096b917) = 'PMS_County_MicroSurface' AND Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86) = YR)
    ,
    Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) >= Get_Number(0.5) AND 
    Get_Exp(915f80f1-74d8-48c0-ab9f-fdffd05d547a) AND 
    GET_TRTYR('PMS_County_Thick_Overlay') > Get_Number(0) AND 
    YR-GET_TRTYR('PMS_County_Thick_Overlay') >=Get_Number(5) AND 
    YR-GET_TRTYR('PMS_County_Thick_Overlay') <=Get_Number(7)
)

```

<a id="e-fa6d626c-f568-419c-b630-6c90ac7e8c7e"></a>

## PMS_abfTRIG_County_Thick_Overlay

Source: `RuntimeExpressions` / `fa6d626c-f568-419c-b630-6c90ac7e8c7e`.

Thick Overlay Trigger Expression for counties

Readable:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(Com_Year),MAX(Get_Field(COM_YR_2),MAX(Get_Field(COM_YR_3),Get_Field(COM_YR_4)))),
(Get_Field(Com_Trt) = 'PMS_County_Thick_Overlay' AND Get_Field(Com_Year) = YR)  OR
(Get_Field(COM_TRT_2) = 'PMS_County_Thick_Overlay' AND Get_Field(COM_YR_2) = YR)  OR
(Get_Field(COM_TRT_3) = 'PMS_County_Thick_Overlay' AND Get_Field(COM_YR_3) = YR)  OR
(Get_Field(COM_TRT_4) = 'PMS_County_Thick_Overlay' AND Get_Field(COM_YR_4) = YR)
,
Get_Field(Length) >= Get_Number(0.5) AND 
Get_Exp(PMS_abfOBJ_Asphalt) AND
(
    (
    GET_ANALVR(PMS_nAAV_CND_CCI) < Get_Number(1)
    AND
    Get_Field(IRI_Mean) > Get_Number(150)
    )
    OR
    (
        (Get_Field(Patch_L)+Get_Field(Patch_M)+Get_Field(Patch_H)) / (Get_Field(Length)*Get_Number(5280)*Get_Number(8))*Get_Number(100) >= Get_Number(15)
    )
)
AND Get_Field(ADT)>=Get_Number(200))

```

Original:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0),MAX(Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),MAX(Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)))),
(Get_Field(ec965cc6-5ed5-4591-bf5b-1c0885ef785e) = 'PMS_County_Thick_Overlay' AND Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0) = YR)  OR
(Get_Field(a2875f19-2f5a-4d09-920c-208664ff67c8) = 'PMS_County_Thick_Overlay' AND Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) = YR)  OR
(Get_Field(63019b8f-f66e-4853-8d0c-1c15c7a59395) = 'PMS_County_Thick_Overlay' AND Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) = YR)  OR
(Get_Field(262093c5-ae74-44bd-9f4d-264b6096b917) = 'PMS_County_Thick_Overlay' AND Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86) = YR)
,
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) >= Get_Number(0.5) AND 
Get_Exp(915f80f1-74d8-48c0-ab9f-fdffd05d547a) AND
(
    (
    GET_ANALVR(b17f394f-57fd-4efb-8e0e-787d545e45f5) < Get_Number(1)
    AND
    Get_Field(27134121-7932-4a33-8c47-a44035638fed) > Get_Number(150)
    )
    OR
    (
        (Get_Field(81d3110b-8b04-4a29-9b73-7010aa197b64)+Get_Field(9b3567a4-2e02-4f9e-a51d-e048a6d570d9)+Get_Field(9b73e2a0-0cbe-440d-a90b-c38f7a7cec38)) / (Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c)*Get_Number(5280)*Get_Number(8))*Get_Number(100) >= Get_Number(15)
    )
)
AND Get_Field(8c63c2ca-4d7c-41c5-8632-e26685bf488e)>=Get_Number(200))

```

<a id="e-9a433234-e459-461d-a629-75b50a89f2e5"></a>

## PMS_abfTRIG_County_Thin_Overlay

Source: `RuntimeExpressions` / `9a433234-e459-461d-a629-75b50a89f2e5`.

Thin Overlay Trigger Expression for counties

Readable:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(Com_Year),MAX(Get_Field(COM_YR_2),MAX(Get_Field(COM_YR_3),Get_Field(COM_YR_4)))),
(Get_Field(Com_Trt) = 'PMS_County_Thin_Overlay' AND Get_Field(Com_Year) = YR)  OR
(Get_Field(COM_TRT_2) = 'PMS_County_Thin_Overlay' AND Get_Field(COM_YR_2) = YR)  OR
(Get_Field(COM_TRT_3) = 'PMS_County_Thin_Overlay' AND Get_Field(COM_YR_3) = YR)  OR
(Get_Field(COM_TRT_4) = 'PMS_County_Thin_Overlay' AND Get_Field(COM_YR_4) = YR)
,
Get_Field(Length) >= Get_Number(0.5) AND 
Get_Exp(PMS_abfOBJ_Asphalt) AND
GET_ANALVR(PMS_nAAV_CND_CCI) >=Get_Number(1) AND GET_ANALVR(PMS_nAAV_CND_CCI) <= Get_Number(2) AND
//PMS_nAAV_CND_IRI >=95.0 AND Analysis->IRI_Mean <= 250.0 AND
Get_Field(ADT) >=Get_Number(250)
)

```

Original:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0),MAX(Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),MAX(Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)))),
(Get_Field(ec965cc6-5ed5-4591-bf5b-1c0885ef785e) = 'PMS_County_Thin_Overlay' AND Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0) = YR)  OR
(Get_Field(a2875f19-2f5a-4d09-920c-208664ff67c8) = 'PMS_County_Thin_Overlay' AND Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) = YR)  OR
(Get_Field(63019b8f-f66e-4853-8d0c-1c15c7a59395) = 'PMS_County_Thin_Overlay' AND Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) = YR)  OR
(Get_Field(262093c5-ae74-44bd-9f4d-264b6096b917) = 'PMS_County_Thin_Overlay' AND Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86) = YR)
,
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) >= Get_Number(0.5) AND 
Get_Exp(915f80f1-74d8-48c0-ab9f-fdffd05d547a) AND
GET_ANALVR(b17f394f-57fd-4efb-8e0e-787d545e45f5) >=Get_Number(1) AND GET_ANALVR(b17f394f-57fd-4efb-8e0e-787d545e45f5) <= Get_Number(2) AND
//PMS_nAAV_CND_IRI >=95.0 AND Analysis->IRI_Mean <= 250.0 AND
Get_Field(8c63c2ca-4d7c-41c5-8632-e26685bf488e) >=Get_Number(250)
)

```

<a id="e-833ac796-64df-45c8-8802-30db1da8e5a7"></a>

## PMS_abfTRIG_Fair_Treatment_For_GFP_70P_Good

Source: `RuntimeExpressions` / `833ac796-64df-45c8-8802-30db1da8e5a7`.

Trigger for Fair Treatment for GFP 70% Good analysis

Readable:
```text
GET_ANALVR(PMS_tAAV_MAP21_GFP) = 'FAIR'
```

Original:
```text
GET_ANALVR(f3617859-d9ab-41c8-af85-b90df5193e91) = 'FAIR'
```

<a id="e-1fd310a5-e53d-436d-842f-bd66dc4a4105"></a>

## PMS_abfTRIG_Major_HMA_Overlay

Source: `RuntimeExpressions` / `1fd310a5-e53d-436d-842f-bd66dc4a4105`.

Trigger for Major HMA Overlay

Readable:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(Com_Year),MAX(Get_Field(COM_YR_2),MAX(Get_Field(COM_YR_3),Get_Field(COM_YR_4)))),
(Get_Field(Com_Trt) = 'PMS_Thick_Overlay' AND Get_Field(Com_Year) = YR)  OR
(Get_Field(COM_TRT_2) = 'PMS_Thick_Overlay' AND Get_Field(COM_YR_2) = YR)  OR
(Get_Field(COM_TRT_3) = 'PMS_Thick_Overlay' AND Get_Field(COM_YR_3) = YR)  OR
(Get_Field(COM_TRT_4) = 'PMS_Thick_Overlay' AND Get_Field(COM_YR_4) = YR)
,
Get_Field(Length) >= Get_Number(0.5) AND 
Get_Exp(PMS_abfOBJ_Asphalt) AND
(
(
    GET_ANALVR(PMS_nAAV_CND_PSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','THICK_OVL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_PSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','THICK_OVL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_SCI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','THICK_OVL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_SCI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','THICK_OVL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_ECI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','THICK_OVL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_ECI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','THICK_OVL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_RDI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','THICK_OVL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_RDI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','THICK_OVL_1',TRUE)) 
)                                                                           
OR                                                                          
(                                                                           
    GET_ANALVR(PMS_nAAV_CND_PSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','THICK_OVL_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_PSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','THICK_OVL_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_SCI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','THICK_OVL_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_SCI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','THICK_OVL_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_ECI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','THICK_OVL_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_ECI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','THICK_OVL_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_RDI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','THICK_OVL_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_RDI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','THICK_OVL_2',TRUE)) 
)                                                                           
OR                                                                          
(                                                                           
    GET_ANALVR(PMS_nAAV_CND_PSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','THICK_OVL_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_PSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','THICK_OVL_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_SCI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','THICK_OVL_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_SCI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','THICK_OVL_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_ECI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','THICK_OVL_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_ECI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','THICK_OVL_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_RDI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','THICK_OVL_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_RDI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','THICK_OVL_3',TRUE)) 
)
)
)
```

Original:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0),MAX(Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),MAX(Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)))),
(Get_Field(ec965cc6-5ed5-4591-bf5b-1c0885ef785e) = 'PMS_Thick_Overlay' AND Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0) = YR)  OR
(Get_Field(a2875f19-2f5a-4d09-920c-208664ff67c8) = 'PMS_Thick_Overlay' AND Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) = YR)  OR
(Get_Field(63019b8f-f66e-4853-8d0c-1c15c7a59395) = 'PMS_Thick_Overlay' AND Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) = YR)  OR
(Get_Field(262093c5-ae74-44bd-9f4d-264b6096b917) = 'PMS_Thick_Overlay' AND Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86) = YR)
,
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) >= Get_Number(0.5) AND 
Get_Exp(915f80f1-74d8-48c0-ab9f-fdffd05d547a) AND
(
(
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','THICK_OVL_1',TRUE)) AND
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','THICK_OVL_1',TRUE)) AND
    GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','THICK_OVL_1',TRUE)) AND
    GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','THICK_OVL_1',TRUE)) AND
    GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','THICK_OVL_1',TRUE)) AND
    GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','THICK_OVL_1',TRUE)) AND
    GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','THICK_OVL_1',TRUE)) AND
    GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','THICK_OVL_1',TRUE)) 
)                                                                           
OR                                                                          
(                                                                           
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','THICK_OVL_2',TRUE)) AND
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','THICK_OVL_2',TRUE)) AND
    GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','THICK_OVL_2',TRUE)) AND
    GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','THICK_OVL_2',TRUE)) AND
    GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','THICK_OVL_2',TRUE)) AND
    GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','THICK_OVL_2',TRUE)) AND
    GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','THICK_OVL_2',TRUE)) AND
    GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','THICK_OVL_2',TRUE)) 
)                                                                           
OR                                                                          
(                                                                           
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','THICK_OVL_3',TRUE)) AND
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','THICK_OVL_3',TRUE)) AND
    GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','THICK_OVL_3',TRUE)) AND
    GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','THICK_OVL_3',TRUE)) AND
    GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','THICK_OVL_3',TRUE)) AND
    GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','THICK_OVL_3',TRUE)) AND
    GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','THICK_OVL_3',TRUE)) AND
    GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','THICK_OVL_3',TRUE)) 
)
)
)
```

<a id="e-141ccfde-fd66-42cc-9c25-6987370a25f2"></a>

## PMS_abfTRIG_Minor_HMA_Overlay

Source: `RuntimeExpressions` / `141ccfde-fd66-42cc-9c25-6987370a25f2`.

Trigger for Minor HMA Overlay

Readable:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(Com_Year),MAX(Get_Field(COM_YR_2),MAX(Get_Field(COM_YR_3),Get_Field(COM_YR_4)))),
(Get_Field(Com_Trt) = 'PMS_Thin_Overlay' AND Get_Field(Com_Year) = YR)  OR
(Get_Field(COM_TRT_2) = 'PMS_Thin_Overlay' AND Get_Field(COM_YR_2) = YR)  OR
(Get_Field(COM_TRT_3) = 'PMS_Thin_Overlay' AND Get_Field(COM_YR_3) = YR)  OR
(Get_Field(COM_TRT_4) = 'PMS_Thin_Overlay' AND Get_Field(COM_YR_4) = YR)
,
Get_Field(Length) >= Get_Number(0.5) AND 
Get_Exp(PMS_abfOBJ_Asphalt) AND
(
(
    GET_ANALVR(PMS_nAAV_CND_PSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','THIN_OVL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_PSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','THIN_OVL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_SCI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','THIN_OVL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_SCI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','THIN_OVL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_ECI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','THIN_OVL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_ECI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','THIN_OVL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_RDI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','THIN_OVL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_RDI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','THIN_OVL_1',TRUE)) 
)                                                                           
OR                                                                          
(                                                                           
    GET_ANALVR(PMS_nAAV_CND_PSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','THIN_OVL_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_PSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','THIN_OVL_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_SCI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','THIN_OVL_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_SCI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','THIN_OVL_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_ECI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','THIN_OVL_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_ECI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','THIN_OVL_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_RDI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','THIN_OVL_2',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_RDI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','THIN_OVL_2',TRUE)) 
)                                                                           
OR                                                                          
(                                                                           
    GET_ANALVR(PMS_nAAV_CND_PSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','THIN_OVL_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_PSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','THIN_OVL_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_SCI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','THIN_OVL_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_SCI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','THIN_OVL_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_ECI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','THIN_OVL_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_ECI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','THIN_OVL_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_RDI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','THIN_OVL_3',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_RDI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','THIN_OVL_3',TRUE)) 
)                                                                           
OR                                                                          
(                                                                           
    GET_ANALVR(PMS_nAAV_CND_PSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','THIN_OVL_4',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_PSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','THIN_OVL_4',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_SCI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','THIN_OVL_4',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_SCI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','THIN_OVL_4',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_ECI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','THIN_OVL_4',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_ECI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','THIN_OVL_4',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_RDI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','THIN_OVL_4',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_RDI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','THIN_OVL_4',TRUE))
)
)
)
```

Original:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0),MAX(Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),MAX(Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)))),
(Get_Field(ec965cc6-5ed5-4591-bf5b-1c0885ef785e) = 'PMS_Thin_Overlay' AND Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0) = YR)  OR
(Get_Field(a2875f19-2f5a-4d09-920c-208664ff67c8) = 'PMS_Thin_Overlay' AND Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) = YR)  OR
(Get_Field(63019b8f-f66e-4853-8d0c-1c15c7a59395) = 'PMS_Thin_Overlay' AND Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) = YR)  OR
(Get_Field(262093c5-ae74-44bd-9f4d-264b6096b917) = 'PMS_Thin_Overlay' AND Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86) = YR)
,
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) >= Get_Number(0.5) AND 
Get_Exp(915f80f1-74d8-48c0-ab9f-fdffd05d547a) AND
(
(
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','THIN_OVL_1',TRUE)) AND
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','THIN_OVL_1',TRUE)) AND
    GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','THIN_OVL_1',TRUE)) AND
    GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','THIN_OVL_1',TRUE)) AND
    GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','THIN_OVL_1',TRUE)) AND
    GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','THIN_OVL_1',TRUE)) AND
    GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','THIN_OVL_1',TRUE)) AND
    GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','THIN_OVL_1',TRUE)) 
)                                                                           
OR                                                                          
(                                                                           
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','THIN_OVL_2',TRUE)) AND
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','THIN_OVL_2',TRUE)) AND
    GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','THIN_OVL_2',TRUE)) AND
    GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','THIN_OVL_2',TRUE)) AND
    GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','THIN_OVL_2',TRUE)) AND
    GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','THIN_OVL_2',TRUE)) AND
    GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','THIN_OVL_2',TRUE)) AND
    GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','THIN_OVL_2',TRUE)) 
)                                                                           
OR                                                                          
(                                                                           
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','THIN_OVL_3',TRUE)) AND
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','THIN_OVL_3',TRUE)) AND
    GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','THIN_OVL_3',TRUE)) AND
    GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','THIN_OVL_3',TRUE)) AND
    GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','THIN_OVL_3',TRUE)) AND
    GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','THIN_OVL_3',TRUE)) AND
    GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','THIN_OVL_3',TRUE)) AND
    GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','THIN_OVL_3',TRUE)) 
)                                                                           
OR                                                                          
(                                                                           
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','THIN_OVL_4',TRUE)) AND
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','THIN_OVL_4',TRUE)) AND
    GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','THIN_OVL_4',TRUE)) AND
    GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','THIN_OVL_4',TRUE)) AND
    GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','THIN_OVL_4',TRUE)) AND
    GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','THIN_OVL_4',TRUE)) AND
    GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','THIN_OVL_4',TRUE)) AND
    GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','THIN_OVL_4',TRUE))
)
)
)
```

<a id="e-faef9933-2cb9-4772-a0bc-4ee6e0b7040a"></a>

## PMS_abfTRIG_PM_Asphalt

Source: `RuntimeExpressions` / `faef9933-2cb9-4772-a0bc-4ee6e0b7040a`.

Trigger for PM Asphalt

Readable:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(Com_Year),MAX(Get_Field(COM_YR_2),MAX(Get_Field(COM_YR_3),Get_Field(COM_YR_4)))),
(Get_Field(Com_Trt) = 'PMS_PM_Asphalt' AND Get_Field(Com_Year) = YR)  OR
(Get_Field(COM_TRT_2) = 'PMS_PM_Asphalt' AND Get_Field(COM_YR_2) = YR)  OR
(Get_Field(COM_TRT_3) = 'PMS_PM_Asphalt' AND Get_Field(COM_YR_3) = YR)  OR
(Get_Field(COM_TRT_4) = 'PMS_PM_Asphalt' AND Get_Field(COM_YR_4) = YR)
,
Get_Field(Length) >= Get_Number(0.5) AND 
Get_Exp(PMS_abfOBJ_Asphalt) AND 
Get_Exp(PMS_abfTRIG_Trt_Timing_PM_Wait) AND 
Get_Exp(PMS_abfTRIG_Trt_Timing_NonPM_Wait)
)
```

Original:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0),MAX(Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),MAX(Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)))),
(Get_Field(ec965cc6-5ed5-4591-bf5b-1c0885ef785e) = 'PMS_PM_Asphalt' AND Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0) = YR)  OR
(Get_Field(a2875f19-2f5a-4d09-920c-208664ff67c8) = 'PMS_PM_Asphalt' AND Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) = YR)  OR
(Get_Field(63019b8f-f66e-4853-8d0c-1c15c7a59395) = 'PMS_PM_Asphalt' AND Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) = YR)  OR
(Get_Field(262093c5-ae74-44bd-9f4d-264b6096b917) = 'PMS_PM_Asphalt' AND Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86) = YR)
,
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) >= Get_Number(0.5) AND 
Get_Exp(915f80f1-74d8-48c0-ab9f-fdffd05d547a) AND 
Get_Exp(20f92128-c805-452f-9d9b-74dd509841dd) AND 
Get_Exp(f2d024b7-d3bc-4baf-884e-f0b3c93a6967)
)
```

<a id="e-7f35547c-7da4-4935-b6ca-075c0f150b4d"></a>

## PMS_abfTRIG_PM_Cape_Seal

Source: `RuntimeExpressions` / `7f35547c-7da4-4935-b6ca-075c0f150b4d`.

Trigger for PM Cape Seal

Readable:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(Com_Year),MAX(Get_Field(COM_YR_2),MAX(Get_Field(COM_YR_3),Get_Field(COM_YR_4)))),
(Get_Field(Com_Trt) = 'PMS_PM_Cape_Seal' AND Get_Field(Com_Year) = YR)  OR
(Get_Field(COM_TRT_2) = 'PMS_PM_Cape_Seal' AND Get_Field(COM_YR_2) = YR)  OR
(Get_Field(COM_TRT_3) = 'PMS_PM_Cape_Seal' AND Get_Field(COM_YR_3) = YR)  OR
(Get_Field(COM_TRT_4) = 'PMS_PM_Cape_Seal' AND Get_Field(COM_YR_4) = YR)
,
Get_Field(Length) >= Get_Number(0.5) AND 
Get_Exp(PMS_abfOBJ_Asphalt) AND 
Get_Field(Sign) <> '1' AND 
(NOT      Get_Exp(PMS_abfOBJ_I68)) AND
(
    GET_ANALVR(PMS_nAAV_CND_PSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','CAPE_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_PSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','CAPE_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_SCI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','CAPE_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_SCI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','CAPE_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_ECI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','CAPE_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_ECI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','CAPE_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_RDI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','CAPE_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_RDI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','CAPE_SEAL_1',TRUE)) 
)
)
```

Original:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0),MAX(Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),MAX(Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)))),
(Get_Field(ec965cc6-5ed5-4591-bf5b-1c0885ef785e) = 'PMS_PM_Cape_Seal' AND Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0) = YR)  OR
(Get_Field(a2875f19-2f5a-4d09-920c-208664ff67c8) = 'PMS_PM_Cape_Seal' AND Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) = YR)  OR
(Get_Field(63019b8f-f66e-4853-8d0c-1c15c7a59395) = 'PMS_PM_Cape_Seal' AND Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) = YR)  OR
(Get_Field(262093c5-ae74-44bd-9f4d-264b6096b917) = 'PMS_PM_Cape_Seal' AND Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86) = YR)
,
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) >= Get_Number(0.5) AND 
Get_Exp(915f80f1-74d8-48c0-ab9f-fdffd05d547a) AND 
Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) <> '1' AND 
(NOT      Get_Exp(4c811992-2c2d-42c6-b156-c4d16973b739)) AND
(
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','CAPE_SEAL_1',TRUE)) AND
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','CAPE_SEAL_1',TRUE)) AND
    GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','CAPE_SEAL_1',TRUE)) AND
    GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','CAPE_SEAL_1',TRUE)) AND
    GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','CAPE_SEAL_1',TRUE)) AND
    GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','CAPE_SEAL_1',TRUE)) AND
    GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','CAPE_SEAL_1',TRUE)) AND
    GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','CAPE_SEAL_1',TRUE)) 
)
)
```

<a id="e-b65f9808-6dea-411a-a508-ce89f87250bf"></a>

## PMS_abfTRIG_PM_Chip_Seal

Source: `RuntimeExpressions` / `b65f9808-6dea-411a-a508-ce89f87250bf`.

Trigger for PM Chip Seal

Readable:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(Com_Year),MAX(Get_Field(COM_YR_2),MAX(Get_Field(COM_YR_3),Get_Field(COM_YR_4)))),
(Get_Field(Com_Trt) = 'PMS_PM_Chip_Seal' AND Get_Field(Com_Year) = YR)  OR
(Get_Field(COM_TRT_2) = 'PMS_PM_Chip_Seal' AND Get_Field(COM_YR_2) = YR)  OR
(Get_Field(COM_TRT_3) = 'PMS_PM_Chip_Seal' AND Get_Field(COM_YR_3) = YR)  OR
(Get_Field(COM_TRT_4) = 'PMS_PM_Chip_Seal' AND Get_Field(COM_YR_4) = YR)
,
Get_Field(Length) >= Get_Number(0.5) AND 
Get_Exp(PMS_abfOBJ_Asphalt) AND GET_ANALVR(PMS_nDAV_CNT_CHIP_SEALS) <= Get_Number(2) AND 
Get_Field(Sign) <> '1' AND (NOT         Get_Exp(PMS_abfOBJ_I68)) AND
GET_ANALVR(PMS_nAAV_TRF_ADT) < Get_Number(1000) AND 
(
    GET_ANALVR(PMS_nAAV_CND_PSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','CHIP_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_PSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','CHIP_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_SCI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','CHIP_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_SCI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','CHIP_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_ECI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','CHIP_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_ECI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','CHIP_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_RDI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','CHIP_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_RDI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','CHIP_SEAL_1',TRUE))
) AND
Get_Field(Lanes_Total)<=Get_Number(1)
)
```

Original:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0),MAX(Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),MAX(Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)))),
(Get_Field(ec965cc6-5ed5-4591-bf5b-1c0885ef785e) = 'PMS_PM_Chip_Seal' AND Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0) = YR)  OR
(Get_Field(a2875f19-2f5a-4d09-920c-208664ff67c8) = 'PMS_PM_Chip_Seal' AND Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) = YR)  OR
(Get_Field(63019b8f-f66e-4853-8d0c-1c15c7a59395) = 'PMS_PM_Chip_Seal' AND Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) = YR)  OR
(Get_Field(262093c5-ae74-44bd-9f4d-264b6096b917) = 'PMS_PM_Chip_Seal' AND Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86) = YR)
,
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) >= Get_Number(0.5) AND 
Get_Exp(915f80f1-74d8-48c0-ab9f-fdffd05d547a) AND GET_ANALVR(7014cb8f-5c5e-4f86-a714-76ec0a7d79a1) <= Get_Number(2) AND 
Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) <> '1' AND (NOT         Get_Exp(4c811992-2c2d-42c6-b156-c4d16973b739)) AND
GET_ANALVR(674cee68-8d0f-4f42-8ec1-227bcc6bb6a4) < Get_Number(1000) AND 
(
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','CHIP_SEAL_1',TRUE)) AND
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','CHIP_SEAL_1',TRUE)) AND
    GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','CHIP_SEAL_1',TRUE)) AND
    GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','CHIP_SEAL_1',TRUE)) AND
    GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','CHIP_SEAL_1',TRUE)) AND
    GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','CHIP_SEAL_1',TRUE)) AND
    GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','CHIP_SEAL_1',TRUE)) AND
    GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','CHIP_SEAL_1',TRUE))
) AND
Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)<=Get_Number(1)
)
```

<a id="e-c34ffc8e-1693-4eaf-aec2-be381e56d727"></a>

## PMS_abfTRIG_PM_Concrete

Source: `RuntimeExpressions` / `c34ffc8e-1693-4eaf-aec2-be381e56d727`.

Trigger for PM Concrete

Readable:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(Com_Year),MAX(Get_Field(COM_YR_2),MAX(Get_Field(COM_YR_3),Get_Field(COM_YR_4)))),
(Get_Field(Com_Trt) = 'PMS_PM_Concrete' AND Get_Field(Com_Year) = YR)  OR
(Get_Field(COM_TRT_2) = 'PMS_PM_Concrete' AND Get_Field(COM_YR_2) = YR)  OR
(Get_Field(COM_TRT_3) = 'PMS_PM_Concrete' AND Get_Field(COM_YR_3) = YR)  OR
(Get_Field(COM_TRT_4) = 'PMS_PM_Concrete' AND Get_Field(COM_YR_4) = YR)
,
Get_Field(Length) >= Get_Number(0.5) AND 
Get_Exp(PMS_abfOBJ_Concrete) AND 
Get_Exp(PMS_abfTRIG_Trt_Timing_PM_Wait) AND 
Get_Exp(PMS_abfTRIG_Trt_Timing_NonPM_Wait)
)
```

Original:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0),MAX(Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),MAX(Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)))),
(Get_Field(ec965cc6-5ed5-4591-bf5b-1c0885ef785e) = 'PMS_PM_Concrete' AND Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0) = YR)  OR
(Get_Field(a2875f19-2f5a-4d09-920c-208664ff67c8) = 'PMS_PM_Concrete' AND Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) = YR)  OR
(Get_Field(63019b8f-f66e-4853-8d0c-1c15c7a59395) = 'PMS_PM_Concrete' AND Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) = YR)  OR
(Get_Field(262093c5-ae74-44bd-9f4d-264b6096b917) = 'PMS_PM_Concrete' AND Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86) = YR)
,
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) >= Get_Number(0.5) AND 
Get_Exp(ba469472-994d-4555-923b-c833047e7e8b) AND 
Get_Exp(20f92128-c805-452f-9d9b-74dd509841dd) AND 
Get_Exp(f2d024b7-d3bc-4baf-884e-f0b3c93a6967)
)
```

<a id="e-44307b81-2222-4ae9-984a-543e62f4cbc6"></a>

## PMS_abfTRIG_PM_Crack_Seal

Source: `RuntimeExpressions` / `44307b81-2222-4ae9-984a-543e62f4cbc6`.

Trigger for Crack Seal

Readable:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(Com_Year),MAX(Get_Field(COM_YR_2),MAX(Get_Field(COM_YR_3),Get_Field(COM_YR_4)))),
(Get_Field(Com_Trt) = 'PMS_PM_Crack_Seal' AND Get_Field(Com_Year) = YR)  OR
(Get_Field(COM_TRT_2) = 'PMS_PM_Crack_Seal' AND Get_Field(COM_YR_2) = YR)  OR
(Get_Field(COM_TRT_3) = 'PMS_PM_Crack_Seal' AND Get_Field(COM_YR_3) = YR)  OR
(Get_Field(COM_TRT_4) = 'PMS_PM_Crack_Seal' AND Get_Field(COM_YR_4) = YR)
,
Get_Field(Length) >= Get_Number(0.5) AND 
Get_Exp(PMS_abfOBJ_Asphalt) AND
(
    GET_ANALVR(PMS_nAAV_CND_PSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','CRACK_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_PSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','CRACK_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_SCI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','CRACK_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_SCI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','CRACK_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_ECI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','CRACK_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_ECI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','CRACK_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_RDI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','CRACK_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_RDI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','CRACK_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_JCI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_LOWER','KEY','CRACK_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_JCI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_UPPER','KEY','CRACK_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_CSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_LOWER','KEY','CRACK_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_CSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_UPPER','KEY','CRACK_SEAL_1',TRUE))
)
)
```

Original:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0),MAX(Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),MAX(Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)))),
(Get_Field(ec965cc6-5ed5-4591-bf5b-1c0885ef785e) = 'PMS_PM_Crack_Seal' AND Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0) = YR)  OR
(Get_Field(a2875f19-2f5a-4d09-920c-208664ff67c8) = 'PMS_PM_Crack_Seal' AND Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) = YR)  OR
(Get_Field(63019b8f-f66e-4853-8d0c-1c15c7a59395) = 'PMS_PM_Crack_Seal' AND Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) = YR)  OR
(Get_Field(262093c5-ae74-44bd-9f4d-264b6096b917) = 'PMS_PM_Crack_Seal' AND Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86) = YR)
,
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) >= Get_Number(0.5) AND 
Get_Exp(915f80f1-74d8-48c0-ab9f-fdffd05d547a) AND
(
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','CRACK_SEAL_1',TRUE)) AND
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','CRACK_SEAL_1',TRUE)) AND
    GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','CRACK_SEAL_1',TRUE)) AND
    GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','CRACK_SEAL_1',TRUE)) AND
    GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','CRACK_SEAL_1',TRUE)) AND
    GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','CRACK_SEAL_1',TRUE)) AND
    GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','CRACK_SEAL_1',TRUE)) AND
    GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','CRACK_SEAL_1',TRUE)) AND
    GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_LOWER','KEY','CRACK_SEAL_1',TRUE)) AND
    GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_UPPER','KEY','CRACK_SEAL_1',TRUE)) AND
    GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_LOWER','KEY','CRACK_SEAL_1',TRUE)) AND
    GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_UPPER','KEY','CRACK_SEAL_1',TRUE))
)
)
```

<a id="e-5c21d9f2-955a-4709-b673-2f052321a295"></a>

## PMS_abfTRIG_PM_Microsurfacing

Source: `RuntimeExpressions` / `5c21d9f2-955a-4709-b673-2f052321a295`.

Trigger for PM Microsurfacing

Readable:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(Com_Year),MAX(Get_Field(COM_YR_2),MAX(Get_Field(COM_YR_3),Get_Field(COM_YR_4)))),
(Get_Field(Com_Trt) = 'PMS_PM_Microsurfacing' AND Get_Field(Com_Year) = YR)  OR
(Get_Field(COM_TRT_2) = 'PMS_PM_Microsurfacing' AND Get_Field(COM_YR_2) = YR)  OR
(Get_Field(COM_TRT_3) = 'PMS_PM_Microsurfacing' AND Get_Field(COM_YR_3) = YR)  OR
(Get_Field(COM_TRT_4) = 'PMS_PM_Microsurfacing' AND Get_Field(COM_YR_4) = YR)
,
    Get_Field(Length) >= Get_Number(3) AND 
    (
    (
    (Get_Exp(PMS_abfOBJ_Asphalt) AND GET_TRTYR('PMS_Thin_Overlay') > Get_Number(0) AND YR-GET_TRTYR('PMS_Thin_Overlay') >=Get_Number(5) AND YR-GET_TRTYR('PMS_Thin_Overlay') <=Get_Number(7) ) OR
    (Get_Exp(PMS_abfOBJ_Asphalt) AND GET_TRTYR('PMS_Thick_Overlay') > Get_Number(0) AND YR-GET_TRTYR('PMS_Thick_Overlay') >=Get_Number(5) AND YR-GET_TRTYR('PMS_Thick_Overlay') <=Get_Number(7) ) OR
    (Get_Exp(PMS_abfOBJ_Asphalt) AND GET_TRTYR('PMS_Reconstruction') > Get_Number(0) AND YR-GET_TRTYR('PMS_Reconstruction') >=Get_Number(5) AND YR-GET_TRTYR('PMS_Reconstruction') <=Get_Number(7) )
    )
    
    OR
    (
    Get_Exp(PMS_abfOBJ_Asphalt) AND GET_ANALVR(PMS_nDAV_CNT_MICROSURFACE) <= Get_Number(1) AND
    (
        GET_ANALVR(PMS_nAAV_CND_PSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','MICRO_1',TRUE)) AND
        GET_ANALVR(PMS_nAAV_CND_PSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','MICRO_1',TRUE)) AND
        GET_ANALVR(PMS_nAAV_CND_SCI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','MICRO_1',TRUE)) AND
        GET_ANALVR(PMS_nAAV_CND_SCI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','MICRO_1',TRUE)) AND
        GET_ANALVR(PMS_nAAV_CND_ECI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','MICRO_1',TRUE)) AND
        GET_ANALVR(PMS_nAAV_CND_ECI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','MICRO_1',TRUE)) AND
        GET_ANALVR(PMS_nAAV_CND_RDI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','MICRO_1',TRUE)) AND
        GET_ANALVR(PMS_nAAV_CND_RDI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','MICRO_1',TRUE))
    )
    )
    )
)

```

Original:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0),MAX(Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),MAX(Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)))),
(Get_Field(ec965cc6-5ed5-4591-bf5b-1c0885ef785e) = 'PMS_PM_Microsurfacing' AND Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0) = YR)  OR
(Get_Field(a2875f19-2f5a-4d09-920c-208664ff67c8) = 'PMS_PM_Microsurfacing' AND Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) = YR)  OR
(Get_Field(63019b8f-f66e-4853-8d0c-1c15c7a59395) = 'PMS_PM_Microsurfacing' AND Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) = YR)  OR
(Get_Field(262093c5-ae74-44bd-9f4d-264b6096b917) = 'PMS_PM_Microsurfacing' AND Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86) = YR)
,
    Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) >= Get_Number(3) AND 
    (
    (
    (Get_Exp(915f80f1-74d8-48c0-ab9f-fdffd05d547a) AND GET_TRTYR('PMS_Thin_Overlay') > Get_Number(0) AND YR-GET_TRTYR('PMS_Thin_Overlay') >=Get_Number(5) AND YR-GET_TRTYR('PMS_Thin_Overlay') <=Get_Number(7) ) OR
    (Get_Exp(915f80f1-74d8-48c0-ab9f-fdffd05d547a) AND GET_TRTYR('PMS_Thick_Overlay') > Get_Number(0) AND YR-GET_TRTYR('PMS_Thick_Overlay') >=Get_Number(5) AND YR-GET_TRTYR('PMS_Thick_Overlay') <=Get_Number(7) ) OR
    (Get_Exp(915f80f1-74d8-48c0-ab9f-fdffd05d547a) AND GET_TRTYR('PMS_Reconstruction') > Get_Number(0) AND YR-GET_TRTYR('PMS_Reconstruction') >=Get_Number(5) AND YR-GET_TRTYR('PMS_Reconstruction') <=Get_Number(7) )
    )
    
    OR
    (
    Get_Exp(915f80f1-74d8-48c0-ab9f-fdffd05d547a) AND GET_ANALVR(1e9fd63b-174d-4d69-8033-e23c4fd3340b) <= Get_Number(1) AND
    (
        GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','MICRO_1',TRUE)) AND
        GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','MICRO_1',TRUE)) AND
        GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','MICRO_1',TRUE)) AND
        GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','MICRO_1',TRUE)) AND
        GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','MICRO_1',TRUE)) AND
        GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','MICRO_1',TRUE)) AND
        GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','MICRO_1',TRUE)) AND
        GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','MICRO_1',TRUE))
    )
    )
    )
)

```

<a id="e-98f4613f-6f58-48ee-8059-baffb001aee8"></a>

## PMS_abfTRIG_PM_Preservation

Source: `RuntimeExpressions` / `98f4613f-6f58-48ee-8059-baffb001aee8`.

Trigger for PM Preservation

Readable:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(Com_Year),MAX(Get_Field(COM_YR_2),MAX(Get_Field(COM_YR_3),Get_Field(COM_YR_4)))),
(Get_Field(Com_Trt) = 'PMS_Preservation' AND Get_Field(Com_Year) = YR)  OR
(Get_Field(COM_TRT_2) = 'PMS_Preservation' AND Get_Field(COM_YR_2) = YR)  OR
(Get_Field(COM_TRT_3) = 'PMS_Preservation' AND Get_Field(COM_YR_3) = YR)  OR
(Get_Field(COM_TRT_4) = 'PMS_Preservation' AND Get_Field(COM_YR_4) = YR)
,
Get_Field(Length) >= Get_Number(0.5) AND 
Get_Exp(PMS_abfOBJ_Asphalt) AND 
(Get_Exp(PMS_abfTRIG_Trt_Timing_PM_Wait) OR Get_Exp(PMS_abfTRIG_Trt_Timing_NonPM_Wait)) AND
(
    GET_ANALVR(PMS_nAAV_CND_PSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','PRESERVATION_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_PSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','PRESERVATION_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_SCI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','PRESERVATION_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_SCI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','PRESERVATION_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_ECI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','PRESERVATION_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_ECI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','PRESERVATION_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_RDI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','PRESERVATION_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_RDI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','PRESERVATION_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_JCI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_LOWER','KEY','PRESERVATION_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_JCI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_UPPER','KEY','PRESERVATION_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_CSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_LOWER','KEY','PRESERVATION_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_CSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_UPPER','KEY','PRESERVATION_1',TRUE))
)
)
```

Original:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0),MAX(Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),MAX(Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)))),
(Get_Field(ec965cc6-5ed5-4591-bf5b-1c0885ef785e) = 'PMS_Preservation' AND Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0) = YR)  OR
(Get_Field(a2875f19-2f5a-4d09-920c-208664ff67c8) = 'PMS_Preservation' AND Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) = YR)  OR
(Get_Field(63019b8f-f66e-4853-8d0c-1c15c7a59395) = 'PMS_Preservation' AND Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) = YR)  OR
(Get_Field(262093c5-ae74-44bd-9f4d-264b6096b917) = 'PMS_Preservation' AND Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86) = YR)
,
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) >= Get_Number(0.5) AND 
Get_Exp(915f80f1-74d8-48c0-ab9f-fdffd05d547a) AND 
(Get_Exp(20f92128-c805-452f-9d9b-74dd509841dd) OR Get_Exp(f2d024b7-d3bc-4baf-884e-f0b3c93a6967)) AND
(
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','PRESERVATION_1',TRUE)) AND
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','PRESERVATION_1',TRUE)) AND
    GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','PRESERVATION_1',TRUE)) AND
    GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','PRESERVATION_1',TRUE)) AND
    GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','PRESERVATION_1',TRUE)) AND
    GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','PRESERVATION_1',TRUE)) AND
    GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','PRESERVATION_1',TRUE)) AND
    GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','PRESERVATION_1',TRUE)) AND
    GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_LOWER','KEY','PRESERVATION_1',TRUE)) AND
    GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_UPPER','KEY','PRESERVATION_1',TRUE)) AND
    GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_LOWER','KEY','PRESERVATION_1',TRUE)) AND
    GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_UPPER','KEY','PRESERVATION_1',TRUE))
)
)
```

<a id="e-28f28e08-7b05-43bf-a28c-22d1286c6fc2"></a>

## PMS_abfTRIG_PM_Saw_Seal_Joints

Source: `RuntimeExpressions` / `28f28e08-7b05-43bf-a28c-22d1286c6fc2`.

Trigger for PM Saw and Seal Joints

Readable:
```text
IF(IS_COMMITTED(),
(Get_Field(Com_Trt) = 'PMS_PM_Saw_Seal_Joints' AND Get_Field(Com_Year) = YR)  OR
(Get_Field(COM_TRT_2) = 'PMS_PM_Saw_Seal_Joints' AND Get_Field(COM_YR_2) = YR)  OR
(Get_Field(COM_TRT_3) = 'PMS_PM_Saw_Seal_Joints' AND Get_Field(COM_YR_3) = YR)  OR
(Get_Field(COM_TRT_4) = 'PMS_PM_Saw_Seal_Joints' AND Get_Field(COM_YR_4) = YR)
,
Get_Field(Length) >= Get_Number(3) AND 
Get_Exp(PMS_abfOBJ_Concrete) AND
(
    GET_ANALVR(PMS_nAAV_CND_PSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','SAW_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_PSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','SAW_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_JCI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_LOWER','KEY','SAW_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_JCI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_UPPER','KEY','SAW_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_CSI) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_LOWER','KEY','SAW_SEAL_1',TRUE)) AND
    GET_ANALVR(PMS_nAAV_CND_CSI) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_UPPER','KEY','SAW_SEAL_1',TRUE))
)
)
```

Original:
```text
IF(IS_COMMITTED(),
(Get_Field(ec965cc6-5ed5-4591-bf5b-1c0885ef785e) = 'PMS_PM_Saw_Seal_Joints' AND Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0) = YR)  OR
(Get_Field(a2875f19-2f5a-4d09-920c-208664ff67c8) = 'PMS_PM_Saw_Seal_Joints' AND Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) = YR)  OR
(Get_Field(63019b8f-f66e-4853-8d0c-1c15c7a59395) = 'PMS_PM_Saw_Seal_Joints' AND Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) = YR)  OR
(Get_Field(262093c5-ae74-44bd-9f4d-264b6096b917) = 'PMS_PM_Saw_Seal_Joints' AND Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86) = YR)
,
Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) >= Get_Number(3) AND 
Get_Exp(ba469472-994d-4555-923b-c833047e7e8b) AND
(
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','SAW_SEAL_1',TRUE)) AND
    GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','SAW_SEAL_1',TRUE)) AND
    GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_LOWER','KEY','SAW_SEAL_1',TRUE)) AND
    GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_UPPER','KEY','SAW_SEAL_1',TRUE)) AND
    GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d) >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_LOWER','KEY','SAW_SEAL_1',TRUE)) AND
    GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d) <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_UPPER','KEY','SAW_SEAL_1',TRUE))
)
)
```

<a id="e-3dcfe007-7999-418b-bbf1-649aa56fb2f4"></a>

## PMS_abfTRIG_PM_Ultra_Thin_Overlay

Source: `RuntimeExpressions` / `3dcfe007-7999-418b-bbf1-649aa56fb2f4`.

Trigger for PM Ultra Thin Overlay

Readable:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(Com_Year),MAX(Get_Field(COM_YR_2),MAX(Get_Field(COM_YR_3),Get_Field(COM_YR_4)))),
(Get_Field(Com_Trt) = 'PMS_PM_Ultra_Thin_Overlay' AND Get_Field(Com_Year) = YR)  OR
(Get_Field(COM_TRT_2) = 'PMS_PM_Ultra_Thin_Overlay' AND Get_Field(COM_YR_2) = YR)  OR
(Get_Field(COM_TRT_3) = 'PMS_PM_Ultra_Thin_Overlay' AND Get_Field(COM_YR_3) = YR)  OR
(Get_Field(COM_TRT_4) = 'PMS_PM_Ultra_Thin_Overlay' AND Get_Field(COM_YR_4) = YR)
,
FALSE
)
//PMS_abfOBJ_Asphalt AND
//(
//    PMS_nAAV_CND_PSI >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','ULTRA_THIN_1',TRUE)) AND
//    PMS_nAAV_CND_PSI <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','ULTRA_THIN_1',TRUE)) AND
//    PMS_nAAV_CND_SCI >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','ULTRA_THIN_1',TRUE)) AND
//    PMS_nAAV_CND_SCI <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','ULTRA_THIN_1',TRUE)) AND
//    PMS_nAAV_CND_ECI >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','ULTRA_THIN_1',TRUE)) AND
//    PMS_nAAV_CND_ECI <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','ULTRA_THIN_1',TRUE)) AND
//    PMS_nAAV_CND_RDI >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','ULTRA_THIN_1',TRUE)) AND
//    PMS_nAAV_CND_RDI <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','ULTRA_THIN_1',TRUE)) AND
//    PMS_nAAV_CND_JCI >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_LOWER','KEY','ULTRA_THIN_1',TRUE)) AND
//    PMS_nAAV_CND_JCI <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_UPPER','KEY','ULTRA_THIN_1',TRUE)) AND
//    PMS_nAAV_CND_CSI >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_LOWER','KEY','ULTRA_THIN_1',TRUE)) AND
//    PMS_nAAV_CND_CSI <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_UPPER','KEY','ULTRA_THIN_1',TRUE))
//)
//)
```

Original:
```text
IF(IS_COMMITTED() AND 
YR <= MAX(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0),MAX(Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),MAX(Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)))),
(Get_Field(ec965cc6-5ed5-4591-bf5b-1c0885ef785e) = 'PMS_PM_Ultra_Thin_Overlay' AND Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0) = YR)  OR
(Get_Field(a2875f19-2f5a-4d09-920c-208664ff67c8) = 'PMS_PM_Ultra_Thin_Overlay' AND Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) = YR)  OR
(Get_Field(63019b8f-f66e-4853-8d0c-1c15c7a59395) = 'PMS_PM_Ultra_Thin_Overlay' AND Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) = YR)  OR
(Get_Field(262093c5-ae74-44bd-9f4d-264b6096b917) = 'PMS_PM_Ultra_Thin_Overlay' AND Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86) = YR)
,
FALSE
)
//PMS_abfOBJ_Asphalt AND
//(
//    PMS_nAAV_CND_PSI >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_LOWER','KEY','ULTRA_THIN_1',TRUE)) AND
//    PMS_nAAV_CND_PSI <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','PSI_UPPER','KEY','ULTRA_THIN_1',TRUE)) AND
//    PMS_nAAV_CND_SCI >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_LOWER','KEY','ULTRA_THIN_1',TRUE)) AND
//    PMS_nAAV_CND_SCI <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','SCI_UPPER','KEY','ULTRA_THIN_1',TRUE)) AND
//    PMS_nAAV_CND_ECI >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_LOWER','KEY','ULTRA_THIN_1',TRUE)) AND
//    PMS_nAAV_CND_ECI <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','ECI_UPPER','KEY','ULTRA_THIN_1',TRUE)) AND
//    PMS_nAAV_CND_RDI >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_LOWER','KEY','ULTRA_THIN_1',TRUE)) AND
//    PMS_nAAV_CND_RDI <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','RDI_UPPER','KEY','ULTRA_THIN_1',TRUE)) AND
//    PMS_nAAV_CND_JCI >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_LOWER','KEY','ULTRA_THIN_1',TRUE)) AND
//    PMS_nAAV_CND_JCI <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','JCI_UPPER','KEY','ULTRA_THIN_1',TRUE)) AND
//    PMS_nAAV_CND_CSI >= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_LOWER','KEY','ULTRA_THIN_1',TRUE)) AND
//    PMS_nAAV_CND_CSI <= VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Triggers','CSI_UPPER','KEY','ULTRA_THIN_1',TRUE))
//)
//)
```

<a id="e-c31b4232-a667-41f9-b7bc-48e3035fa7f0"></a>

## PMS_abfTRIG_Reconstruct

Source: `RuntimeExpressions` / `c31b4232-a667-41f9-b7bc-48e3035fa7f0`.

Trigger for Reconstruction

Readable:
```text
IF(IS_COMMITTED() AND 
    YR <= MAX(Get_Field(Com_Year),MAX(Get_Field(COM_YR_2),MAX(Get_Field(COM_YR_3),Get_Field(COM_YR_4)))),
    (Get_Field(Com_Trt) = 'PMS_Reconstruction' AND Get_Field(Com_Year) = YR)  OR
    (Get_Field(COM_TRT_2) = 'PMS_Reconstruction' AND Get_Field(COM_YR_2) = YR)  OR
    (Get_Field(COM_TRT_3) = 'PMS_Reconstruction' AND Get_Field(COM_YR_3) = YR)  OR
    (Get_Field(COM_TRT_4) = 'PMS_Reconstruction' AND Get_Field(COM_YR_4) = YR)
,
    IF(Get_Exp(PMS_abfOBJ_IM_Funds),
        Get_Field(Length) >= Get_Number(0.5) AND 
        (
            IF(GET_ANALVR(PMS_tDAV_Pave_Type)='RC',
            (GET_ANALVR(PMS_nAAV_CND_PSI) >= Get_Number(0) AND GET_ANALVR(PMS_nAAV_CND_PSI) <= Get_Number(1)) OR
            (GET_ANALVR(PMS_nAAV_CND_CSI) >= Get_Number(0) AND GET_ANALVR(PMS_nAAV_CND_CSI) <= Get_Number(1)) OR
            (GET_ANALVR(PMS_nAAV_CND_JCI) >= Get_Number(0) AND GET_ANALVR(PMS_nAAV_CND_JCI) <= Get_Number(1)) 
        ,
            (GET_ANALVR(PMS_nAAV_CND_PSI) >= Get_Number(0) AND GET_ANALVR(PMS_nAAV_CND_PSI) <= Get_Number(1)) OR
            (GET_ANALVR(PMS_nAAV_CND_ECI) >= Get_Number(0) AND GET_ANALVR(PMS_nAAV_CND_ECI) <= Get_Number(1)) OR
            (GET_ANALVR(PMS_nAAV_CND_ECI) >= Get_Number(0) AND GET_ANALVR(PMS_nAAV_CND_SCI) <= Get_Number(1)) 
        )
        )
    ,
    FALSE
    )
)
```

Original:
```text
IF(IS_COMMITTED() AND 
    YR <= MAX(Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0),MAX(Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),MAX(Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)))),
    (Get_Field(ec965cc6-5ed5-4591-bf5b-1c0885ef785e) = 'PMS_Reconstruction' AND Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0) = YR)  OR
    (Get_Field(a2875f19-2f5a-4d09-920c-208664ff67c8) = 'PMS_Reconstruction' AND Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) = YR)  OR
    (Get_Field(63019b8f-f66e-4853-8d0c-1c15c7a59395) = 'PMS_Reconstruction' AND Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) = YR)  OR
    (Get_Field(262093c5-ae74-44bd-9f4d-264b6096b917) = 'PMS_Reconstruction' AND Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86) = YR)
,
    IF(Get_Exp(1be07652-db7b-492b-8923-a471bbd309e7),
        Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) >= Get_Number(0.5) AND 
        (
            IF(GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2)='RC',
            (GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) >= Get_Number(0) AND GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) <= Get_Number(1)) OR
            (GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d) >= Get_Number(0) AND GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d) <= Get_Number(1)) OR
            (GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb) >= Get_Number(0) AND GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb) <= Get_Number(1)) 
        ,
            (GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) >= Get_Number(0) AND GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) <= Get_Number(1)) OR
            (GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) >= Get_Number(0) AND GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) <= Get_Number(1)) OR
            (GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) >= Get_Number(0) AND GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) <= Get_Number(1)) 
        )
        )
    ,
    FALSE
    )
)
```

<a id="e-f2d024b7-d3bc-4baf-884e-f0b3c93a6967"></a>

## PMS_abfTRIG_Trt_Timing_NonPM_Wait

Source: `RuntimeExpressions` / `f2d024b7-d3bc-4baf-884e-f0b3c93a6967`.



Readable:
```text
IF(LEN(RTRIM(GET_LASTMAJTRT())) > Get_Number(0), IF(LEFT(RTRIM(GET_LASTMAJTRT()),Get_Number(2)) <> 'PM', YR - GET_TRTYR(GET_LASTMAJTRT()) >= Get_Number(5) AND YR - GET_TRTYR(GET_LASTMAJTRT()) <= Get_Number(7), FALSE), IF(Get_Field(REHAB_COMPLETION_YEAR) > Get_Number(0),(YR + GSTART_YR - Get_Number(1)) - Get_Field(REHAB_COMPLETION_YEAR) >= Get_Number(5) AND (YR + GSTART_YR - Get_Number(1)) - Get_Field(REHAB_COMPLETION_YEAR) <= Get_Number(7), FALSE))
```

Original:
```text
IF(LEN(RTRIM(GET_LASTMAJTRT())) > Get_Number(0), IF(LEFT(RTRIM(GET_LASTMAJTRT()),Get_Number(2)) <> 'PM', YR - GET_TRTYR(GET_LASTMAJTRT()) >= Get_Number(5) AND YR - GET_TRTYR(GET_LASTMAJTRT()) <= Get_Number(7), FALSE), IF(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b) > Get_Number(0),(YR + GSTART_YR - Get_Number(1)) - Get_Field(42cf662a-e349-4837-a84e-43b002a7661b) >= Get_Number(5) AND (YR + GSTART_YR - Get_Number(1)) - Get_Field(42cf662a-e349-4837-a84e-43b002a7661b) <= Get_Number(7), FALSE))
```

<a id="e-20f92128-c805-452f-9d9b-74dd509841dd"></a>

## PMS_abfTRIG_Trt_Timing_PM_Wait

Source: `RuntimeExpressions` / `20f92128-c805-452f-9d9b-74dd509841dd`.



Readable:
```text
IF(LEFT(RTRIM(GET_LASTMAJTRT()),Get_Number(2)) = 'PM', YR - GET_TRTYR(GET_LASTMAJTRT()) > IF(GET_LASTMAJTRT() = 'PM_Crack_Seal',Get_Number(3),Get_Number(5)), TRUE)
```

Original:
```text
IF(LEFT(RTRIM(GET_LASTMAJTRT()),Get_Number(2)) = 'PM', YR - GET_TRTYR(GET_LASTMAJTRT()) > IF(GET_LASTMAJTRT() = 'PM_Crack_Seal',Get_Number(3),Get_Number(5)), TRUE)
```

<a id="e-52fb3718-9639-4250-b7f5-63c1eb51435c"></a>

## PMS_ancAGE_AGE_CCI

Source: `RuntimeExpressions` / `52fb3718-9639-4250-b7f5-63c1eb51435c`.



Readable:
```text
GET_ANALVR(PMS_nAAV_AGE_CCI) + IF(GET_ANALVR(PMS_nAAV_AGE_CCI_Hold) < Get_Number(1), Get_Number(1), Get_Number(0))
```

Original:
```text
GET_ANALVR(dbff2024-5a05-488a-abea-fe9179944b39) + IF(GET_ANALVR(a5634802-7249-4bce-b939-625d67347a21) < Get_Number(1), Get_Number(1), Get_Number(0))
```

<a id="e-be41e33a-81f9-448b-81b2-2a0cc906a77a"></a>

## PMS_ancAGE_AGE_CCI_Hold

Source: `RuntimeExpressions` / `be41e33a-81f9-448b-81b2-2a0cc906a77a`.



Readable:
```text
IF(GET_ANALVR(PMS_nAAV_AGE_CCI_Hold) > Get_Number(1), GET_ANALVR(PMS_nAAV_AGE_CCI_Hold) - Get_Number(1), Get_Number(0))
```

Original:
```text
IF(GET_ANALVR(a5634802-7249-4bce-b939-625d67347a21) > Get_Number(1), GET_ANALVR(a5634802-7249-4bce-b939-625d67347a21) - Get_Number(1), Get_Number(0))
```

<a id="e-c4aa8d38-f625-4222-8ffd-9c11b41acddc"></a>

## PMS_ancAGE_AGE_CSI

Source: `RuntimeExpressions` / `c4aa8d38-f625-4222-8ffd-9c11b41acddc`.



Readable:
```text
GET_ANALVR(PMS_nAAV_AGE_CSI) + IF(GET_ANALVR(PMS_nAAV_AGE_CSI_Hold) < Get_Number(1), Get_Number(1), Get_Number(0))
```

Original:
```text
GET_ANALVR(ceb172c5-9f2e-4040-bffc-324947a67e7a) + IF(GET_ANALVR(095ef27c-f9cb-42f8-a40f-5363d8eabcbc) < Get_Number(1), Get_Number(1), Get_Number(0))
```

<a id="e-e65294ca-6bcf-44d6-9377-bed09272fb9f"></a>

## PMS_ancAGE_AGE_CSI_Hold

Source: `RuntimeExpressions` / `e65294ca-6bcf-44d6-9377-bed09272fb9f`.



Readable:
```text
IF(GET_ANALVR(PMS_nAAV_AGE_CSI_Hold) > Get_Number(1), GET_ANALVR(PMS_nAAV_AGE_CSI_Hold) - Get_Number(1), Get_Number(0))
```

Original:
```text
IF(GET_ANALVR(095ef27c-f9cb-42f8-a40f-5363d8eabcbc) > Get_Number(1), GET_ANALVR(095ef27c-f9cb-42f8-a40f-5363d8eabcbc) - Get_Number(1), Get_Number(0))
```

<a id="e-2501dd7f-0fd8-4039-a9ce-f294712ccaf0"></a>

## PMS_ancAGE_AGE_ECI

Source: `RuntimeExpressions` / `2501dd7f-0fd8-4039-a9ce-f294712ccaf0`.



Readable:
```text
GET_ANALVR(PMS_nAAV_AGE_ECI) + IF(GET_ANALVR(PMS_nAAV_AGE_ECI_Hold) < Get_Number(1), Get_Number(1), Get_Number(0))
```

Original:
```text
GET_ANALVR(981a9f97-9ace-4e10-a597-d06bd9fd5df2) + IF(GET_ANALVR(647adf29-aea1-4447-b9d3-b28df2320882) < Get_Number(1), Get_Number(1), Get_Number(0))
```

<a id="e-d69678d8-a883-43c1-aa08-eb9e32270717"></a>

## PMS_ancAGE_AGE_ECI_Hold

Source: `RuntimeExpressions` / `d69678d8-a883-43c1-aa08-eb9e32270717`.



Readable:
```text
IF(GET_ANALVR(PMS_nAAV_AGE_ECI_Hold) > Get_Number(1), GET_ANALVR(PMS_nAAV_AGE_ECI_Hold) - Get_Number(1), Get_Number(0))
```

Original:
```text
IF(GET_ANALVR(647adf29-aea1-4447-b9d3-b28df2320882) > Get_Number(1), GET_ANALVR(647adf29-aea1-4447-b9d3-b28df2320882) - Get_Number(1), Get_Number(0))
```

<a id="e-017d27c7-3195-4d2f-a0d9-c9d21581aabb"></a>

## PMS_ancAGE_AGE_Initial

Source: `RuntimeExpressions` / `017d27c7-3195-4d2f-a0d9-c9d21581aabb`.



Readable:
```text
MIN((GSTART_YR - Get_Field(REHAB_COMPLETION_YEAR)),Get_Number(15))
```

Original:
```text
MIN((GSTART_YR - Get_Field(42cf662a-e349-4837-a84e-43b002a7661b)),Get_Number(15))
```

<a id="e-de5b6de5-f4b4-4e88-bf4e-34dbb5cbfe93"></a>

## PMS_ancAGE_AGE_JCI

Source: `RuntimeExpressions` / `de5b6de5-f4b4-4e88-bf4e-34dbb5cbfe93`.



Readable:
```text
GET_ANALVR(PMS_nAAV_AGE_JCI) + IF(GET_ANALVR(PMS_nAAV_AGE_JCI_Hold) < Get_Number(1), Get_Number(1), Get_Number(0))
```

Original:
```text
GET_ANALVR(d467ebc5-1588-4efb-a9e0-e7f8374b1e33) + IF(GET_ANALVR(2621d56b-8544-4061-b347-69e8dd4deb75) < Get_Number(1), Get_Number(1), Get_Number(0))
```

<a id="e-56fa4833-7747-43f0-bf78-5ecaf8e4eea0"></a>

## PMS_ancAGE_AGE_JCI_Hold

Source: `RuntimeExpressions` / `56fa4833-7747-43f0-bf78-5ecaf8e4eea0`.



Readable:
```text
IF(GET_ANALVR(PMS_nAAV_AGE_JCI_Hold) > Get_Number(1), GET_ANALVR(PMS_nAAV_AGE_JCI_Hold) - Get_Number(1), Get_Number(0))
```

Original:
```text
IF(GET_ANALVR(2621d56b-8544-4061-b347-69e8dd4deb75) > Get_Number(1), GET_ANALVR(2621d56b-8544-4061-b347-69e8dd4deb75) - Get_Number(1), Get_Number(0))
```

<a id="e-ead3a220-af7d-4faa-835c-f05131b58cff"></a>

## PMS_ancAGE_AGE_PSI

Source: `RuntimeExpressions` / `ead3a220-af7d-4faa-835c-f05131b58cff`.



Readable:
```text
GET_ANALVR(PMS_nAAV_AGE_PSI) + Get_Number(1)
```

Original:
```text
GET_ANALVR(963cad98-9956-4ef6-a261-11b0358133b5) + Get_Number(1)
```

<a id="e-1263f400-86b1-4d57-a754-99584937fac5"></a>

## PMS_ancAGE_AGE_RDI

Source: `RuntimeExpressions` / `1263f400-86b1-4d57-a754-99584937fac5`.



Readable:
```text
GET_ANALVR(PMS_nAAV_AGE_RDI) + Get_Number(1)
```

Original:
```text
GET_ANALVR(6426b3ef-fc9a-45ad-a2c3-6146882e9d20) + Get_Number(1)
```

<a id="e-70e13ebd-e481-49a1-ac3d-1290864cde14"></a>

## PMS_ancAGE_AGE_SCI

Source: `RuntimeExpressions` / `70e13ebd-e481-49a1-ac3d-1290864cde14`.



Readable:
```text
GET_ANALVR(PMS_nAAV_AGE_SCI) + IF(GET_ANALVR(PMS_nAAV_AGE_SCI_Hold) < Get_Number(1), Get_Number(1), Get_Number(0))
```

Original:
```text
GET_ANALVR(c4865c39-9e55-4179-85e9-0cc0c3e09081) + IF(GET_ANALVR(77d1104c-3673-4417-8e58-8319b376aea3) < Get_Number(1), Get_Number(1), Get_Number(0))
```

<a id="e-a59ac201-bc10-45a7-ae9e-a0956b017997"></a>

## PMS_ancAGE_AGE_SCI_Hold

Source: `RuntimeExpressions` / `a59ac201-bc10-45a7-ae9e-a0956b017997`.



Readable:
```text
IF(GET_ANALVR(PMS_nAAV_AGE_SCI_Hold) > Get_Number(1), GET_ANALVR(PMS_nAAV_AGE_SCI_Hold) - Get_Number(1), Get_Number(0))
```

Original:
```text
IF(GET_ANALVR(77d1104c-3673-4417-8e58-8319b376aea3) > Get_Number(1), GET_ANALVR(77d1104c-3673-4417-8e58-8319b376aea3) - Get_Number(1), Get_Number(0))
```

<a id="e-2dbc899c-4c91-45a0-bd93-e02b1456b995"></a>

## PMS_ancAGE_CCI_AGE_FROM_INDEX

Source: `RuntimeExpressions` / `2dbc899c-4c91-45a0-bd93-e02b1456b995`.

Calculate Age of CCI from index value

Readable:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(PMS_ancCND_CCI_CURVE_TYPE),Get_Exp(PMS_ancCND_CCI_C1),Get_Exp(PMS_ancCND_CCI_C2),Get_Exp(PMS_ancCND_CCI_C3),Get_Number(5),GET_ANALVR(PMS_nAAV_CND_CCI))
```

Original:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(e74cebb4-cda1-4d51-9c31-f8cd54604e15),Get_Exp(44a47215-d351-4f75-81f1-703b3ef604cd),Get_Exp(5e549021-fc5b-40c7-921b-78219a2f29d2),Get_Exp(62f4d7c4-9bb4-4084-a852-d579469e981e),Get_Number(5),GET_ANALVR(b17f394f-57fd-4efb-8e0e-787d545e45f5))
```

<a id="e-d75dc3dc-8544-4b2f-837e-292a9ec6a457"></a>

## PMS_ancAGE_CCI_AGE_FROM_THRESHOLD

Source: `RuntimeExpressions` / `d75dc3dc-8544-4b2f-837e-292a9ec6a457`.

Calculate age from threshold value for RSL

Readable:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(PMS_ancCND_CCI_CURVE_TYPE),Get_Exp(PMS_ancCND_CCI_C1),Get_Exp(PMS_ancCND_CCI_C2),Get_Exp(PMS_ancCND_CCI_C3),Get_Number(5),Get_Exp(PMS_ancCND_CCI_RSL_THRESHOLD))
```

Original:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(e74cebb4-cda1-4d51-9c31-f8cd54604e15),Get_Exp(44a47215-d351-4f75-81f1-703b3ef604cd),Get_Exp(5e549021-fc5b-40c7-921b-78219a2f29d2),Get_Exp(62f4d7c4-9bb4-4084-a852-d579469e981e),Get_Number(5),Get_Exp(65f11d13-7a03-4056-a545-c4ef68123d33))
```

<a id="e-c29814e7-3233-48a5-a284-183854515370"></a>

## PMS_ancAGE_CSI_AGE_FROM_INDEX

Source: `RuntimeExpressions` / `c29814e7-3233-48a5-a284-183854515370`.



Readable:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(PMS_ancCND_CSI_CURVE_TYPE),Get_Exp(PMS_ancCND_CSI_C1),Get_Exp(PMS_ancCND_CSI_C2),Get_Exp(PMS_ancCND_CSI_C3),Get_Number(5),GET_ANALVR(PMS_nAAV_CND_CSI))
```

Original:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(65f9f34b-3948-438d-9248-d26a6ca2bf9b),Get_Exp(e49463f2-1e92-4128-ad51-984a6d1ccb43),Get_Exp(9a7b2084-7141-4803-b9c4-66533fc9d8ff),Get_Exp(fa4fc3b8-293b-4ef7-8af8-6edc8a771ef7),Get_Number(5),GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d))
```

<a id="e-187ac954-c846-4acc-9de6-a55bb9504037"></a>

## PMS_ancAGE_CSI_AGE_FROM_THRESHOLD

Source: `RuntimeExpressions` / `187ac954-c846-4acc-9de6-a55bb9504037`.



Readable:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(PMS_ancCND_CSI_CURVE_TYPE),Get_Exp(PMS_ancCND_CSI_C1),Get_Exp(PMS_ancCND_CSI_C2),Get_Exp(PMS_ancCND_CSI_C3),Get_Number(5),Get_Exp(PMS_ancCND_CSI_RSL_THRESHOLD))
```

Original:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(65f9f34b-3948-438d-9248-d26a6ca2bf9b),Get_Exp(e49463f2-1e92-4128-ad51-984a6d1ccb43),Get_Exp(9a7b2084-7141-4803-b9c4-66533fc9d8ff),Get_Exp(fa4fc3b8-293b-4ef7-8af8-6edc8a771ef7),Get_Number(5),Get_Exp(3eefe522-b2d3-41d9-ad60-bef35694f1aa))
```

<a id="e-a98afc4d-071a-4fc7-86ef-7840afcd83e8"></a>

## PMS_ancAGE_ECI_AGE_FROM_INDEX

Source: `RuntimeExpressions` / `a98afc4d-071a-4fc7-86ef-7840afcd83e8`.



Readable:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(PMS_ancCND_ECI_CURVE_TYPE),Get_Exp(PMS_ancCND_ECI_C1),Get_Exp(PMS_ancCND_ECI_C2),Get_Exp(PMS_ancCND_ECI_C3),Get_Number(5),GET_ANALVR(PMS_nAAV_CND_ECI))
```

Original:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(67e40a83-bc9f-4f62-9ea2-22b4b2c56110),Get_Exp(7e2f27db-a947-43ff-bb98-437d2de31444),Get_Exp(a4917ee6-8076-4b6a-82f5-1b7d9982ad0b),Get_Exp(d32472b5-b486-4aa5-ac24-4aac7cfb469d),Get_Number(5),GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8))
```

<a id="e-3b7a3658-5731-42cd-8e5a-00517c1d5609"></a>

## PMS_ancAGE_ECI_AGE_FROM_THRESHOLD

Source: `RuntimeExpressions` / `3b7a3658-5731-42cd-8e5a-00517c1d5609`.



Readable:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(PMS_ancCND_ECI_CURVE_TYPE),Get_Exp(PMS_ancCND_ECI_C1),Get_Exp(PMS_ancCND_ECI_C2),Get_Exp(PMS_ancCND_ECI_C3),Get_Number(5),Get_Exp(PMS_ancCND_ECI_RSL_THRESHOLD))
```

Original:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(67e40a83-bc9f-4f62-9ea2-22b4b2c56110),Get_Exp(7e2f27db-a947-43ff-bb98-437d2de31444),Get_Exp(a4917ee6-8076-4b6a-82f5-1b7d9982ad0b),Get_Exp(d32472b5-b486-4aa5-ac24-4aac7cfb469d),Get_Number(5),Get_Exp(a582028b-3a04-4ea3-ad38-b8aea6ab865a))
```

<a id="e-406b0cec-a9f1-4d25-a5aa-fad3184b4f0b"></a>

## PMS_ancAGE_JCI_AGE_FROM_INDEX

Source: `RuntimeExpressions` / `406b0cec-a9f1-4d25-a5aa-fad3184b4f0b`.



Readable:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(PMS_ancCND_JCI_CURVE_TYPE),Get_Exp(PMS_ancCND_JCI_C1),Get_Exp(PMS_ancCND_JCI_C2),Get_Exp(PMS_ancCND_JCI_C3),Get_Number(5),GET_ANALVR(PMS_nAAV_CND_JCI))
```

Original:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(03b63a24-1685-4775-b6d2-d9d95d796ab1),Get_Exp(77358d9c-32c1-4cda-a188-e4e53037b889),Get_Exp(aced2001-8a85-4914-a80d-0bc858832b38),Get_Exp(f2a5c081-0c70-48c5-9762-10815e24ca8e),Get_Number(5),GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb))
```

<a id="e-33c5ead4-7b9b-4755-bbf0-1a2e72e0d94e"></a>

## PMS_ancAGE_JCI_AGE_FROM_THRESHOLD

Source: `RuntimeExpressions` / `33c5ead4-7b9b-4755-bbf0-1a2e72e0d94e`.



Readable:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(PMS_ancCND_JCI_CURVE_TYPE),Get_Exp(PMS_ancCND_JCI_C1),Get_Exp(PMS_ancCND_JCI_C2),Get_Exp(PMS_ancCND_JCI_C3),Get_Number(5),Get_Exp(PMS_ancCND_JCI_RSL_THRESHOLD))
```

Original:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(03b63a24-1685-4775-b6d2-d9d95d796ab1),Get_Exp(77358d9c-32c1-4cda-a188-e4e53037b889),Get_Exp(aced2001-8a85-4914-a80d-0bc858832b38),Get_Exp(f2a5c081-0c70-48c5-9762-10815e24ca8e),Get_Number(5),Get_Exp(30db2e9c-f0a4-4b16-b915-b1fc288b7788))
```

<a id="e-af3d20fc-fa3b-4485-bcee-8714e4acca9f"></a>

## PMS_ancAGE_PSI_AGE_FROM_INDEX

Source: `RuntimeExpressions` / `af3d20fc-fa3b-4485-bcee-8714e4acca9f`.



Readable:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(PMS_ancCND_PSI_CURVE_TYPE),Get_Exp(PMS_ancCND_PSI_C1),Get_Exp(PMS_ancCND_PSI_C2),Get_Exp(PMS_ancCND_PSI_C3),Get_Number(5),GET_ANALVR(PMS_nAAV_CND_PSI))
```

Original:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(17d2a601-da54-4580-980b-33f85f640b76),Get_Exp(d1b6733c-a79d-48cd-a31d-27b4c0073712),Get_Exp(63c8390a-6580-4358-85f7-e547c4fee0ba),Get_Exp(79e5e0b0-4200-422b-8535-98b7a8cd9d4c),Get_Number(5),GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44))
```

<a id="e-e1db4a5b-aca3-4b8e-8cb1-eddbb664a0ac"></a>

## PMS_ancAGE_PSI_AGE_FROM_THRESHOLD

Source: `RuntimeExpressions` / `e1db4a5b-aca3-4b8e-8cb1-eddbb664a0ac`.



Readable:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(PMS_ancCND_PSI_CURVE_TYPE),Get_Exp(PMS_ancCND_PSI_C1),Get_Exp(PMS_ancCND_PSI_C2),Get_Exp(PMS_ancCND_PSI_C3),Get_Number(5),Get_Exp(PMS_ancCND_PSI_RSL_THRESHOLD))
```

Original:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(17d2a601-da54-4580-980b-33f85f640b76),Get_Exp(d1b6733c-a79d-48cd-a31d-27b4c0073712),Get_Exp(63c8390a-6580-4358-85f7-e547c4fee0ba),Get_Exp(79e5e0b0-4200-422b-8535-98b7a8cd9d4c),Get_Number(5),Get_Exp(34f9912f-4c09-4215-89bc-d618fefa95e1))
```

<a id="e-193bb441-a7ab-412f-9d12-ab4247b78d6a"></a>

## PMS_ancAGE_RDI_AGE_FROM_INDEX

Source: `RuntimeExpressions` / `193bb441-a7ab-412f-9d12-ab4247b78d6a`.



Readable:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(PMS_ancCND_RDI_CURVE_TYPE),Get_Exp(PMS_ancCND_RDI_C1),Get_Exp(PMS_ancCND_RDI_C2),Get_Exp(PMS_ancCND_RDI_C3),Get_Number(5),GET_ANALVR(PMS_nAAV_CND_RDI))
```

Original:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(0eea476a-532b-4694-af9e-b1dbb333b085),Get_Exp(8f127ce9-f811-444d-a301-79602909dd96),Get_Exp(057ac914-2bc4-4a37-8dad-ebf6a43261e5),Get_Exp(9d84a96d-0bc9-4de3-b4ec-b5627c5c925e),Get_Number(5),GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff))
```

<a id="e-6aa9eb45-9551-4bc3-aaea-8b23c30bf5eb"></a>

## PMS_ancAGE_RDI_AGE_FROM_THRESHOLD

Source: `RuntimeExpressions` / `6aa9eb45-9551-4bc3-aaea-8b23c30bf5eb`.



Readable:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(PMS_ancCND_RDI_CURVE_TYPE),Get_Exp(PMS_ancCND_RDI_C1),Get_Exp(PMS_ancCND_RDI_C2),Get_Exp(PMS_ancCND_RDI_C3),Get_Number(5),Get_Exp(PMS_ancCND_RDI_RSL_THRESHOLD))
```

Original:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(0eea476a-532b-4694-af9e-b1dbb333b085),Get_Exp(8f127ce9-f811-444d-a301-79602909dd96),Get_Exp(057ac914-2bc4-4a37-8dad-ebf6a43261e5),Get_Exp(9d84a96d-0bc9-4de3-b4ec-b5627c5c925e),Get_Number(5),Get_Exp(e40492b6-33b5-4312-abfc-f846c2103d16))
```

<a id="e-2ef1c4f5-220d-45a3-860d-d073db59ef9e"></a>

## PMS_ancAGE_SCI_AGE_FROM_INDEX

Source: `RuntimeExpressions` / `2ef1c4f5-220d-45a3-860d-d073db59ef9e`.



Readable:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(PMS_ancCND_SCI_CURVE_TYPE),Get_Exp(PMS_ancCND_SCI_C1),Get_Exp(PMS_ancCND_SCI_C2),Get_Exp(PMS_ancCND_SCI_C3),Get_Number(5),GET_ANALVR(PMS_nAAV_CND_SCI))
```

Original:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(a8f46b77-c07c-4d9f-a1aa-ad7fc8951798),Get_Exp(65ab65d5-6019-412f-9ac8-a844ed507692),Get_Exp(5f220dc4-d862-4a14-9435-c7548f2ba9f1),Get_Exp(0fb1a984-fb16-46f3-a9aa-a917b5c6fc55),Get_Number(5),GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673))
```

<a id="e-4fb2afe3-0860-4110-a0c8-f7137db0407c"></a>

## PMS_ancAGE_SCI_AGE_FROM_THRESHOLD

Source: `RuntimeExpressions` / `4fb2afe3-0860-4110-a0c8-f7137db0407c`.



Readable:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(PMS_ancCND_SCI_CURVE_TYPE),Get_Exp(PMS_ancCND_SCI_C1),Get_Exp(PMS_ancCND_SCI_C2),Get_Exp(PMS_ancCND_SCI_C3),Get_Number(5),Get_Exp(PMS_ancCND_SCI_RSL_THRESHOLD))
```

Original:
```text
DAL_DCG_AGEFROMINDEX(Get_Exp(a8f46b77-c07c-4d9f-a1aa-ad7fc8951798),Get_Exp(65ab65d5-6019-412f-9ac8-a844ed507692),Get_Exp(5f220dc4-d862-4a14-9435-c7548f2ba9f1),Get_Exp(0fb1a984-fb16-46f3-a9aa-a917b5c6fc55),Get_Number(5),Get_Exp(87339c27-eb9d-47cb-99a4-9f091d53609c))
```

<a id="e-37912066-8e12-42a1-bb03-66cd52069a87"></a>

## PMS_ancCAV_CAV_Yearly_Miles_Poor

Source: `RuntimeExpressions` / `37912066-8e12-42a1-bb03-66cd52069a87`.



Readable:
```text
GET4CAV_PV(PMS_nDAV_Yearly_Miles_Poor)
```

Original:
```text
GET4CAV_PV(feed448c-5ddc-4db8-bcd8-b078e7f63440)
```

<a id="e-94dffbab-78c7-49ea-8e1c-83b282ff8d7e"></a>

## PMS_ancCND_CCI_Annual

Source: `RuntimeExpressions` / `94dffbab-78c7-49ea-8e1c-83b282ff8d7e`.



Readable:
```text
MAX(IF(GET_ANALVR(PMS_tDAV_Pave_Type) = 'BC', 
        MIN(GET_ANALVR(PMS_nAAV_CND_ECI), MIN(GET_ANALVR(PMS_nAAV_CND_PSI), MIN(GET_ANALVR(PMS_nAAV_CND_RDI), GET_ANALVR(PMS_nAAV_CND_SCI)) ) ) , 
    IF(GET_ANALVR(PMS_tDAV_Pave_Type) = 'RC', MIN(GET_ANALVR(PMS_nAAV_CND_CSI), MIN(GET_ANALVR(PMS_nAAV_CND_JCI), GET_ANALVR(PMS_nAAV_CND_PSI)) ) ,
    -Get_Number(1)) )
    - Get_Number(0.5), Get_Number(0))
```

Original:
```text
MAX(IF(GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) = 'BC', 
        MIN(GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8), MIN(GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44), MIN(GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff), GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673)) ) ) , 
    IF(GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) = 'RC', MIN(GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d), MIN(GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb), GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44)) ) ,
    -Get_Number(1)) )
    - Get_Number(0.5), Get_Number(0))
```

<a id="e-44a47215-d351-4f75-81f1-703b3ef604cd"></a>

## PMS_ancCND_CCI_C1

Source: `RuntimeExpressions` / `44a47215-d351-4f75-81f1-703b3ef604cd`.

Return CCI Coef 1 

Readable:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C1','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_CCI',TRUE))
```

Original:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C1','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_CCI',TRUE))
```

<a id="e-5e549021-fc5b-40c7-921b-78219a2f29d2"></a>

## PMS_ancCND_CCI_C2

Source: `RuntimeExpressions` / `5e549021-fc5b-40c7-921b-78219a2f29d2`.

CCI Coef 2

Readable:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C2','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_CCI',TRUE))
```

Original:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C2','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_CCI',TRUE))
```

<a id="e-62f4d7c4-9bb4-4084-a852-d579469e981e"></a>

## PMS_ancCND_CCI_C3

Source: `RuntimeExpressions` / `62f4d7c4-9bb4-4084-a852-d579469e981e`.

CCI coef 3

Readable:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C3','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_CCI',TRUE))
```

Original:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C3','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_CCI',TRUE))
```

<a id="e-e74cebb4-cda1-4d51-9c31-f8cd54604e15"></a>

## PMS_ancCND_CCI_CURVE_TYPE

Source: `RuntimeExpressions` / `e74cebb4-cda1-4d51-9c31-f8cd54604e15`.

CCI curve type 

Readable:
```text
DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','CURVE_TYPE','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_CCI',TRUE)
```

Original:
```text
DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','CURVE_TYPE','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_CCI',TRUE)
```

<a id="e-578c4796-95a5-4bd9-8570-107663e586da"></a>

## PMS_ancCND_CCI_INDEX_FROM_AGE

Source: `RuntimeExpressions` / `578c4796-95a5-4bd9-8570-107663e586da`.



Readable:
```text
MAX(DAL_DCG_INDEXFROMAGE(Get_Exp(PMS_ancCND_CCI_CURVE_TYPE),Get_Exp(PMS_ancCND_CCI_C1),Get_Exp(PMS_ancCND_CCI_C2),Get_Exp(PMS_ancCND_CCI_C3),Get_Number(5),GET_ANALVR(PMS_nAAV_AGE_CCI)),Get_Number(0))
```

Original:
```text
MAX(DAL_DCG_INDEXFROMAGE(Get_Exp(e74cebb4-cda1-4d51-9c31-f8cd54604e15),Get_Exp(44a47215-d351-4f75-81f1-703b3ef604cd),Get_Exp(5e549021-fc5b-40c7-921b-78219a2f29d2),Get_Exp(62f4d7c4-9bb4-4084-a852-d579469e981e),Get_Number(5),GET_ANALVR(dbff2024-5a05-488a-abea-fe9179944b39)),Get_Number(0))
```

<a id="e-8a43f0ff-40b1-47eb-b158-816d67f1068b"></a>

## PMS_ancCND_CCI_INDEX_FROM_AGE_Orig

Source: `RuntimeExpressions` / `8a43f0ff-40b1-47eb-b158-816d67f1068b`.



Readable:
```text
IF(Get_Exp(PMS_ancCND_CCI_CURVE_TYPE) = 'Linear', Get_Number(5) + Get_Exp(PMS_ancCND_CCI_C1) * GET_ANALVR(PMS_nAAV_AGE_CCI), 
IF(Get_Exp(PMS_ancCND_CCI_CURVE_TYPE) = 'Log', Get_Number(5) - EXP(Get_Exp(PMS_ancCND_CCI_C1) + Get_Exp(PMS_ancCND_CCI_C2) * Get_Exp(PMS_ancCND_CCI_C3)**LOG10(Get_Number(1)/GET_ANALVR(PMS_nAAV_AGE_CCI))),
IF(Get_Exp(PMS_ancCND_CCI_CURVE_TYPE) = 'Polynomial', Get_Number(5) + Get_Exp(PMS_ancCND_CCI_C1) * GET_ANALVR(PMS_nAAV_AGE_CCI) + Get_Exp(PMS_ancCND_CCI_C2) * GET_ANALVR(PMS_nAAV_AGE_CCI)**Get_Number(2), 
IF(Get_Exp(PMS_ancCND_CCI_CURVE_TYPE) = 'Power', Get_Number(5) + Get_Exp(PMS_ancCND_CCI_C1) * GET_ANALVR(PMS_nAAV_AGE_CCI)**Get_Exp(PMS_ancCND_CCI_C2), 
IF(Get_Exp(PMS_ancCND_CCI_CURVE_TYPE) = 'Sigmoid', Get_Number(5) - Get_Exp(PMS_ancCND_CCI_C1) * EXP(-(Get_Exp(PMS_ancCND_CCI_C2) / GET_ANALVR(PMS_nAAV_AGE_CCI))**Get_Exp(PMS_ancCND_CCI_C3)), 
IF(Get_Exp(PMS_ancCND_CCI_CURVE_TYPE) = 'Polynomial3', Get_Number(5) + Get_Exp(PMS_ancCND_CCI_C1) * GET_ANALVR(PMS_nAAV_AGE_CCI) + Get_Exp(PMS_ancCND_CCI_C2) * GET_ANALVR(PMS_nAAV_AGE_CCI)**Get_Number(2) + Get_Exp(PMS_ancCND_CCI_C3) * GET_ANALVR(PMS_nAAV_AGE_CCI)**Get_Number(3),
Get_Number(0)))))))
```

Original:
```text
IF(Get_Exp(e74cebb4-cda1-4d51-9c31-f8cd54604e15) = 'Linear', Get_Number(5) + Get_Exp(44a47215-d351-4f75-81f1-703b3ef604cd) * GET_ANALVR(dbff2024-5a05-488a-abea-fe9179944b39), 
IF(Get_Exp(e74cebb4-cda1-4d51-9c31-f8cd54604e15) = 'Log', Get_Number(5) - EXP(Get_Exp(44a47215-d351-4f75-81f1-703b3ef604cd) + Get_Exp(5e549021-fc5b-40c7-921b-78219a2f29d2) * Get_Exp(62f4d7c4-9bb4-4084-a852-d579469e981e)**LOG10(Get_Number(1)/GET_ANALVR(dbff2024-5a05-488a-abea-fe9179944b39))),
IF(Get_Exp(e74cebb4-cda1-4d51-9c31-f8cd54604e15) = 'Polynomial', Get_Number(5) + Get_Exp(44a47215-d351-4f75-81f1-703b3ef604cd) * GET_ANALVR(dbff2024-5a05-488a-abea-fe9179944b39) + Get_Exp(5e549021-fc5b-40c7-921b-78219a2f29d2) * GET_ANALVR(dbff2024-5a05-488a-abea-fe9179944b39)**Get_Number(2), 
IF(Get_Exp(e74cebb4-cda1-4d51-9c31-f8cd54604e15) = 'Power', Get_Number(5) + Get_Exp(44a47215-d351-4f75-81f1-703b3ef604cd) * GET_ANALVR(dbff2024-5a05-488a-abea-fe9179944b39)**Get_Exp(5e549021-fc5b-40c7-921b-78219a2f29d2), 
IF(Get_Exp(e74cebb4-cda1-4d51-9c31-f8cd54604e15) = 'Sigmoid', Get_Number(5) - Get_Exp(44a47215-d351-4f75-81f1-703b3ef604cd) * EXP(-(Get_Exp(5e549021-fc5b-40c7-921b-78219a2f29d2) / GET_ANALVR(dbff2024-5a05-488a-abea-fe9179944b39))**Get_Exp(62f4d7c4-9bb4-4084-a852-d579469e981e)), 
IF(Get_Exp(e74cebb4-cda1-4d51-9c31-f8cd54604e15) = 'Polynomial3', Get_Number(5) + Get_Exp(44a47215-d351-4f75-81f1-703b3ef604cd) * GET_ANALVR(dbff2024-5a05-488a-abea-fe9179944b39) + Get_Exp(5e549021-fc5b-40c7-921b-78219a2f29d2) * GET_ANALVR(dbff2024-5a05-488a-abea-fe9179944b39)**Get_Number(2) + Get_Exp(62f4d7c4-9bb4-4084-a852-d579469e981e) * GET_ANALVR(dbff2024-5a05-488a-abea-fe9179944b39)**Get_Number(3),
Get_Number(0)))))))
```

<a id="e-1d79b6dc-7923-483f-9d27-33ca3d53c739"></a>

## PMS_ancCND_CCI_Initial

Source: `dTIMSExpressions` / `1d79b6dc-7923-483f-9d27-33ca3d53c739`.



Readable:
```text
IF(Get_Exp(PMS_ancOBJ_Pave_type_Initial) = 'BC', MIN(IF(IFDEFAULT(Get_Field(ECI)), Get_Number(99), Get_Field(ECI)) , MIN(IF(IFDEFAULT(Get_Field(PSI)), Get_Number(99), Get_Field(PSI)), MIN(IF(IFDEFAULT(Get_Field(RDI)), Get_Number(99), Get_Field(RDI)), IF(IFDEFAULT(Get_Field(SCI)), Get_Number(99), Get_Field(SCI))) ) ) , IF(Get_Exp(PMS_ancOBJ_Pave_type_Initial) = 'RC', MIN(IF(IFDEFAULT(Get_Field(CSI)), Get_Number(99), Get_Field(CSI)), MIN(IF(IFDEFAULT(Get_Field(JCI)), Get_Number(99), Get_Field(JCI)), IF(IFDEFAULT(Get_Field(PSI)), Get_Number(99), Get_Field(PSI))) ) , -Get_Number(1)) )
```

Original:
```text
IF(Get_Exp(09c7fde6-cc65-4701-9ecc-e3e705983d08) = 'BC', MIN(IF(IFDEFAULT(Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)), Get_Number(99), Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)) , MIN(IF(IFDEFAULT(Get_Field(1eca4d42-a141-4b12-8457-f11b987a6710)), Get_Number(99), Get_Field(1eca4d42-a141-4b12-8457-f11b987a6710)), MIN(IF(IFDEFAULT(Get_Field(be1a4d5a-ea19-4e1a-a61d-c1b792828006)), Get_Number(99), Get_Field(be1a4d5a-ea19-4e1a-a61d-c1b792828006)), IF(IFDEFAULT(Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)), Get_Number(99), Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04))) ) ) , IF(Get_Exp(09c7fde6-cc65-4701-9ecc-e3e705983d08) = 'RC', MIN(IF(IFDEFAULT(Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5)), Get_Number(99), Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5)), MIN(IF(IFDEFAULT(Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050)), Get_Number(99), Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050)), IF(IFDEFAULT(Get_Field(1eca4d42-a141-4b12-8457-f11b987a6710)), Get_Number(99), Get_Field(1eca4d42-a141-4b12-8457-f11b987a6710))) ) , -Get_Number(1)) )
```

<a id="e-477c7140-728e-4354-bec3-0a2497666f72"></a>

## PMS_ancCND_CCI_Initial_Old

Source: `dTIMSExpressions` / `477c7140-728e-4354-bec3-0a2497666f72`.



Readable:
```text
IF(Get_Exp(PMS_ancOBJ_Pave_type_Initial) = 'BC', MIN(IF(IFDEFAULT(Get_Field(ECI)), Get_Number(99), Get_Field(ECI)) , MIN(IF(IFDEFAULT(Get_Field(PSI)), Get_Number(99), Get_Field(PSI)), MIN(IF(IFDEFAULT(Get_Field(RDI)), Get_Number(99), Get_Field(RDI)), IF(IFDEFAULT(Get_Field(SCI)), Get_Number(99), Get_Field(SCI))) ) ) , IF(Get_Exp(PMS_ancOBJ_Pave_type_Initial) = 'RC', MIN(IF(IFDEFAULT(Get_Field(CSI)), Get_Number(99), Get_Field(CSI)), MIN(IF(IFDEFAULT(Get_Field(JCI)), Get_Number(99), Get_Field(JCI)), IF(IFDEFAULT(Get_Field(PSI)), Get_Number(99), Get_Field(PSI))) ) , -Get_Number(1)) )
```

Original:
```text
IF(Get_Exp(09c7fde6-cc65-4701-9ecc-e3e705983d08) = 'BC', MIN(IF(IFDEFAULT(Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)), Get_Number(99), Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)) , MIN(IF(IFDEFAULT(Get_Field(1eca4d42-a141-4b12-8457-f11b987a6710)), Get_Number(99), Get_Field(1eca4d42-a141-4b12-8457-f11b987a6710)), MIN(IF(IFDEFAULT(Get_Field(be1a4d5a-ea19-4e1a-a61d-c1b792828006)), Get_Number(99), Get_Field(be1a4d5a-ea19-4e1a-a61d-c1b792828006)), IF(IFDEFAULT(Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)), Get_Number(99), Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04))) ) ) , IF(Get_Exp(09c7fde6-cc65-4701-9ecc-e3e705983d08) = 'RC', MIN(IF(IFDEFAULT(Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5)), Get_Number(99), Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5)), MIN(IF(IFDEFAULT(Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050)), Get_Number(99), Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050)), IF(IFDEFAULT(Get_Field(1eca4d42-a141-4b12-8457-f11b987a6710)), Get_Number(99), Get_Field(1eca4d42-a141-4b12-8457-f11b987a6710))) ) , -Get_Number(1)) )
```

<a id="e-ea0596f8-2e1b-4a7b-9a8a-3cbddb992f82"></a>

## PMS_ancCND_CCI_RSL

Source: `RuntimeExpressions` / `ea0596f8-2e1b-4a7b-9a8a-3cbddb992f82`.



Readable:
```text
MAX(Get_Exp(PMS_ancAGE_CCI_AGE_FROM_THRESHOLD) - Get_Exp(PMS_ancAGE_CCI_AGE_FROM_INDEX), Get_Number(0))
```

Original:
```text
MAX(Get_Exp(d75dc3dc-8544-4b2f-837e-292a9ec6a457) - Get_Exp(2dbc899c-4c91-45a0-bd93-e02b1456b995), Get_Number(0))
```

<a id="e-65f11d13-7a03-4056-a545-c4ef68123d33"></a>

## PMS_ancCND_CCI_RSL_THRESHOLD

Source: `dTIMSExpressions` / `65f11d13-7a03-4056-a545-c4ef68123d33`.



Readable:
```text
IF(Get_Field(Sign)='1',Get_Number(2.5),
IF(Get_Field(Sign)='2',Get_Number(2),
IF(Get_Field(Sign)='3',Get_Number(1.5),
IF(Get_Field(Sign)='4',Get_Number(1),Get_Number(2.5)))))
```

Original:
```text
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='1',Get_Number(2.5),
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='2',Get_Number(2),
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='3',Get_Number(1.5),
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='4',Get_Number(1),Get_Number(2.5)))))
```

<a id="e-e49463f2-1e92-4128-ad51-984a6d1ccb43"></a>

## PMS_ancCND_CSI_C1

Source: `RuntimeExpressions` / `e49463f2-1e92-4128-ad51-984a6d1ccb43`.



Readable:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C1','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_CSI',TRUE))
```

Original:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C1','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_CSI',TRUE))
```

<a id="e-9a7b2084-7141-4803-b9c4-66533fc9d8ff"></a>

## PMS_ancCND_CSI_C2

Source: `RuntimeExpressions` / `9a7b2084-7141-4803-b9c4-66533fc9d8ff`.



Readable:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C2','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_CSI',TRUE))
```

Original:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C2','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_CSI',TRUE))
```

<a id="e-fa4fc3b8-293b-4ef7-8af8-6edc8a771ef7"></a>

## PMS_ancCND_CSI_C3

Source: `RuntimeExpressions` / `fa4fc3b8-293b-4ef7-8af8-6edc8a771ef7`.



Readable:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C3','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_CSI',TRUE))
```

Original:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C3','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_CSI',TRUE))
```

<a id="e-65f9f34b-3948-438d-9248-d26a6ca2bf9b"></a>

## PMS_ancCND_CSI_CURVE_TYPE

Source: `RuntimeExpressions` / `65f9f34b-3948-438d-9248-d26a6ca2bf9b`.



Readable:
```text
DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','CURVE_TYPE','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_CSI',TRUE)
```

Original:
```text
DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','CURVE_TYPE','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_CSI',TRUE)
```

<a id="e-dce9c83f-1cf5-42f9-a9f8-20b5e9210a0d"></a>

## PMS_ancCND_CSI_INDEX_FROM_AGE

Source: `RuntimeExpressions` / `dce9c83f-1cf5-42f9-a9f8-20b5e9210a0d`.



Readable:
```text
IF(GET_ANALVR(PMS_tDAV_Pave_Type) <>'RC',Get_Number(0),
MAX(DAL_DCG_INDEXFROMAGE(Get_Exp(PMS_ancCND_CSI_CURVE_TYPE),Get_Exp(PMS_ancCND_CSI_C1),Get_Exp(PMS_ancCND_CSI_C2),Get_Exp(PMS_ancCND_CSI_C3),Get_Number(5),GET_ANALVR(PMS_nAAV_AGE_CSI)),Get_Number(0))
)
```

Original:
```text
IF(GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) <>'RC',Get_Number(0),
MAX(DAL_DCG_INDEXFROMAGE(Get_Exp(65f9f34b-3948-438d-9248-d26a6ca2bf9b),Get_Exp(e49463f2-1e92-4128-ad51-984a6d1ccb43),Get_Exp(9a7b2084-7141-4803-b9c4-66533fc9d8ff),Get_Exp(fa4fc3b8-293b-4ef7-8af8-6edc8a771ef7),Get_Number(5),GET_ANALVR(ceb172c5-9f2e-4040-bffc-324947a67e7a)),Get_Number(0))
)
```

<a id="e-dc93c619-354f-448a-9cfa-361ef9bda2c4"></a>

## PMS_ancCND_CSI_Initial

Source: `RuntimeExpressions` / `dc93c619-354f-448a-9cfa-361ef9bda2c4`.



Readable:
```text
IF(GET_ANALVR(PMS_tDAV_Pave_Type)<>'RC',Get_Number(0),
IF(Get_Field(REHAB_COMPLETION_YEAR)>=Get_Field(COND_YEAR), IF(Get_Field(REHAB_TYPE)='Initial',Get_Number(5), 
IF(Get_Field(REHAB_TYPE)='Major',Get_Number(5),Get_Number(4.5))),Get_Field(CSI)) + (IF(Get_Field(REHAB_TYPE)='Initial',Get_Number(0.0026), 
IF(Get_Field(REHAB_TYPE)='Major',-Get_Number(0.0291),Get_Number(0.0189))) * (GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR))) + 
IF(Get_Field(REHAB_TYPE)='Initial',-Get_Number(0.0026), IF(Get_Field(REHAB_TYPE)='Major',-Get_Number(0.0032),-Get_Number(0.0094))) * 
(GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR)))**Get_Number(2) + 
IF(Get_Field(REHAB_TYPE)='Initial',Get_Number(2E-05), IF(Get_Field(REHAB_TYPE)='Major',Get_Number(4E-05),Get_Number(0.0001))) * 
(GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR)))**Get_Number(3))
)
```

Original:
```text
IF(GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2)<>'RC',Get_Number(0),
IF(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b)>=Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',Get_Number(5), 
IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',Get_Number(5),Get_Number(4.5))),Get_Field(20df0c89-1630-43f6-abae-98ab5f5827f5)) + (IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',Get_Number(0.0026), 
IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',-Get_Number(0.0291),Get_Number(0.0189))) * (GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) + 
IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',-Get_Number(0.0026), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',-Get_Number(0.0032),-Get_Number(0.0094))) * 
(GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c)))**Get_Number(2) + 
IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',Get_Number(2E-05), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',Get_Number(4E-05),Get_Number(0.0001))) * 
(GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c)))**Get_Number(3))
)
```

<a id="e-1de251ee-bc69-4d3a-9fa7-7c09071eca38"></a>

## PMS_ancCND_CSI_RSL

Source: `RuntimeExpressions` / `1de251ee-bc69-4d3a-9fa7-7c09071eca38`.



Readable:
```text
MAX(Get_Exp(PMS_ancAGE_CSI_AGE_FROM_THRESHOLD) - Get_Exp(PMS_ancAGE_CSI_AGE_FROM_INDEX), Get_Number(0))
```

Original:
```text
MAX(Get_Exp(187ac954-c846-4acc-9de6-a55bb9504037) - Get_Exp(c29814e7-3233-48a5-a284-183854515370), Get_Number(0))
```

<a id="e-3eefe522-b2d3-41d9-ad60-bef35694f1aa"></a>

## PMS_ancCND_CSI_RSL_THRESHOLD

Source: `dTIMSExpressions` / `3eefe522-b2d3-41d9-ad60-bef35694f1aa`.



Readable:
```text
IF(Get_Field(Sign)='1',Get_Number(2.5),
IF(Get_Field(Sign)='2',Get_Number(2),
IF(Get_Field(Sign)='3',Get_Number(1.5),
IF(Get_Field(Sign)='4',Get_Number(1),Get_Number(2.5)))))
```

Original:
```text
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='1',Get_Number(2.5),
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='2',Get_Number(2),
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='3',Get_Number(1.5),
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='4',Get_Number(1),Get_Number(2.5)))))
```

<a id="e-7e2f27db-a947-43ff-bb98-437d2de31444"></a>

## PMS_ancCND_ECI_C1

Source: `RuntimeExpressions` / `7e2f27db-a947-43ff-bb98-437d2de31444`.



Readable:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C1','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_ECI',TRUE))
```

Original:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C1','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_ECI',TRUE))
```

<a id="e-a4917ee6-8076-4b6a-82f5-1b7d9982ad0b"></a>

## PMS_ancCND_ECI_C2

Source: `RuntimeExpressions` / `a4917ee6-8076-4b6a-82f5-1b7d9982ad0b`.



Readable:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C2','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_ECI',TRUE))
```

Original:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C2','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_ECI',TRUE))
```

<a id="e-d32472b5-b486-4aa5-ac24-4aac7cfb469d"></a>

## PMS_ancCND_ECI_C3

Source: `RuntimeExpressions` / `d32472b5-b486-4aa5-ac24-4aac7cfb469d`.



Readable:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C3','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_ECI',TRUE))
```

Original:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C3','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_ECI',TRUE))
```

<a id="e-67e40a83-bc9f-4f62-9ea2-22b4b2c56110"></a>

## PMS_ancCND_ECI_CURVE_TYPE

Source: `RuntimeExpressions` / `67e40a83-bc9f-4f62-9ea2-22b4b2c56110`.



Readable:
```text
DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','CURVE_TYPE','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_ECI',TRUE)
```

Original:
```text
DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','CURVE_TYPE','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_ECI',TRUE)
```

<a id="e-a62bae96-cffa-4264-b3d0-e93ebe17b687"></a>

## PMS_ancCND_ECI_INDEX_FROM_AGE

Source: `RuntimeExpressions` / `a62bae96-cffa-4264-b3d0-e93ebe17b687`.



Readable:
```text
MAX(DAL_DCG_INDEXFROMAGE(Get_Exp(PMS_ancCND_ECI_CURVE_TYPE),Get_Exp(PMS_ancCND_ECI_C1),Get_Exp(PMS_ancCND_ECI_C2),Get_Exp(PMS_ancCND_ECI_C3),Get_Number(5),GET_ANALVR(PMS_nAAV_AGE_ECI)),Get_Number(0))
```

Original:
```text
MAX(DAL_DCG_INDEXFROMAGE(Get_Exp(67e40a83-bc9f-4f62-9ea2-22b4b2c56110),Get_Exp(7e2f27db-a947-43ff-bb98-437d2de31444),Get_Exp(a4917ee6-8076-4b6a-82f5-1b7d9982ad0b),Get_Exp(d32472b5-b486-4aa5-ac24-4aac7cfb469d),Get_Number(5),GET_ANALVR(981a9f97-9ace-4e10-a597-d06bd9fd5df2)),Get_Number(0))
```

<a id="e-944e39aa-54bc-4509-bd7a-b120d512a0fb"></a>

## PMS_ancCND_ECI_Initial

Source: `RuntimeExpressions` / `944e39aa-54bc-4509-bd7a-b120d512a0fb`.



Readable:
```text
IF(IFDEFAULT(Get_Field(ECI)),Get_Number(0),
IF(Get_Field(REHAB_COMPLETION_YEAR)>=Get_Field(COND_YEAR),
IF(Get_Field(REHAB_TYPE)='Initial',Get_Number(5), 
IF(Get_Field(REHAB_TYPE)='Major',Get_Number(5),Get_Number(4.5))),Get_Field(ECI)) + (IF(Get_Field(REHAB_TYPE)='Initial',-Get_Number(0.0266), IF(Get_Field(REHAB_TYPE)='Major',-Get_Number(0.1404),-Get_Number(0.1289))) * (GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR))) + IF(Get_Field(REHAB_TYPE)='Initial',Get_Number(3E-05), IF(Get_Field(REHAB_TYPE)='Major',-Get_Number(0.0014),-Get_Number(0.002))) * (GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR)))**Get_Number(2) + IF(Get_Field(REHAB_TYPE)='Initial',-Get_Number(5E-05), IF(Get_Field(REHAB_TYPE)='Major',Get_Number(4E-05),Get_Number(0))) * (GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR)))**Get_Number(3))
)
```

Original:
```text
IF(IFDEFAULT(Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)),Get_Number(0),
IF(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b)>=Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c),
IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',Get_Number(5), 
IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',Get_Number(5),Get_Number(4.5))),Get_Field(bcd53054-70e8-4b9e-8f55-cbce550777b4)) + (IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',-Get_Number(0.0266), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',-Get_Number(0.1404),-Get_Number(0.1289))) * (GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) + IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',Get_Number(3E-05), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',-Get_Number(0.0014),-Get_Number(0.002))) * (GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c)))**Get_Number(2) + IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',-Get_Number(5E-05), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',Get_Number(4E-05),Get_Number(0))) * (GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c)))**Get_Number(3))
)
```

<a id="e-f80bc936-95cf-4aa7-8d49-ffacd24fb8ed"></a>

## PMS_ancCND_ECI_RSL

Source: `RuntimeExpressions` / `f80bc936-95cf-4aa7-8d49-ffacd24fb8ed`.



Readable:
```text
MAX(Get_Exp(PMS_ancAGE_ECI_AGE_FROM_THRESHOLD) - Get_Exp(PMS_ancAGE_ECI_AGE_FROM_INDEX), Get_Number(0))
```

Original:
```text
MAX(Get_Exp(3b7a3658-5731-42cd-8e5a-00517c1d5609) - Get_Exp(a98afc4d-071a-4fc7-86ef-7840afcd83e8), Get_Number(0))
```

<a id="e-a582028b-3a04-4ea3-ad38-b8aea6ab865a"></a>

## PMS_ancCND_ECI_RSL_THRESHOLD

Source: `dTIMSExpressions` / `a582028b-3a04-4ea3-ad38-b8aea6ab865a`.



Readable:
```text
IF(Get_Field(Sign)='1',Get_Number(2.5),
IF(Get_Field(Sign)='2',Get_Number(2),
IF(Get_Field(Sign)='3',Get_Number(1.5),
IF(Get_Field(Sign)='4',Get_Number(1),Get_Number(2.5)))))
```

Original:
```text
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='1',Get_Number(2.5),
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='2',Get_Number(2),
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='3',Get_Number(1.5),
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='4',Get_Number(1),Get_Number(2.5)))))
```

<a id="e-aaf51da0-8aee-4880-8b21-151258584a8f"></a>

## PMS_ancCND_FLT

Source: `RuntimeExpressions` / `aaf51da0-8aee-4880-8b21-151258584a8f`.

Faulting

Readable:
```text
GET_ANALVR(PMS_nAAV_CND_FLT)
```

Original:
```text
GET_ANALVR(eeec27ce-e315-49ee-ab9c-31fb47e68655)
```

<a id="e-8696dc20-6bf3-44d2-b7c8-d93b39ae6fc3"></a>

## PMS_ancCND_FLT_GFP

Source: `RuntimeExpressions` / `8696dc20-6bf3-44d2-b7c8-d93b39ae6fc3`.

Faulting Good Fair Poor

Readable:
```text
IF(GET_ANALVR(PMS_nAAV_CND_FLT) < Get_Number(0.1), 'GOOD', IF(GET_ANALVR(PMS_nAAV_CND_FLT)>Get_Number(0.15),'POOR','FAIR'))
```

Original:
```text
IF(GET_ANALVR(eeec27ce-e315-49ee-ab9c-31fb47e68655) < Get_Number(0.1), 'GOOD', IF(GET_ANALVR(eeec27ce-e315-49ee-ab9c-31fb47e68655)>Get_Number(0.15),'POOR','FAIR'))
```

<a id="e-3e9f36e6-ebfa-45bf-a570-107faa16ef44"></a>

## PMS_ancCND_FLT_Initialize

Source: `RuntimeExpressions` / `3e9f36e6-ebfa-45bf-a570-107faa16ef44`.

Faulting Initialization

Readable:
```text
IF(Get_Exp(PMS_abfOBJ_Concrete),
    IF(IFDEFAULT(Get_Field(Fault_Mean)) OR Get_Field(Fault_Mean)<Get_Number(0),
        Get_Number(0),
    Get_Field(Fault_Mean)
    )
    ,
    Get_Number(0)
)
```

Original:
```text
IF(Get_Exp(ba469472-994d-4555-923b-c833047e7e8b),
    IF(IFDEFAULT(Get_Field(2db1acf8-dd8a-4f49-bfa2-e4d83186fba4)) OR Get_Field(2db1acf8-dd8a-4f49-bfa2-e4d83186fba4)<Get_Number(0),
        Get_Number(0),
    Get_Field(2db1acf8-dd8a-4f49-bfa2-e4d83186fba4)
    )
    ,
    Get_Number(0)
)
```

<a id="e-fe3e82d6-4c7e-43db-9766-fef084908311"></a>

## PMS_ancCND_IRI

Source: `RuntimeExpressions` / `fe3e82d6-4c7e-43db-9766-fef084908311`.

Calculate IRI from PSI

Readable:
```text
IF(GET_ANALVR(PMS_nAAV_CND_PSI) > Get_Number(0),
    MIN(Get_Number(65)+(LOG(GET_ANALVR(PMS_nAAV_CND_PSI)/Get_Number(5))/-Get_Number(0.0066)),Get_Number(500)),
    Get_Number(500)
)

```

Original:
```text
IF(GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) > Get_Number(0),
    MIN(Get_Number(65)+(LOG(GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44)/Get_Number(5))/-Get_Number(0.0066)),Get_Number(500)),
    Get_Number(500)
)

```

<a id="e-ab06bc85-2e62-4269-aeda-d8bd7144b6ad"></a>

## PMS_ancCND_IRI_GFP

Source: `RuntimeExpressions` / `ab06bc85-2e62-4269-aeda-d8bd7144b6ad`.

IRI Good Fair Poor

Readable:
```text
IF(GET_ANALVR(PMS_nAAV_CND_IRI) < Get_Number(95), 'GOOD', IF(GET_ANALVR(PMS_nAAV_CND_IRI)>Get_Number(170),'POOR','FAIR'))
```

Original:
```text
IF(GET_ANALVR(3ae48bd7-f227-491a-88ba-510a2e180f5d) < Get_Number(95), 'GOOD', IF(GET_ANALVR(3ae48bd7-f227-491a-88ba-510a2e180f5d)>Get_Number(170),'POOR','FAIR'))
```

<a id="e-30c3e49f-060e-4d6f-ad43-7a810b8695e9"></a>

## PMS_ancCND_IRI_Initialize

Source: `dTIMSExpressions` / `30c3e49f-060e-4d6f-ad43-7a810b8695e9`.

Initialize IRI Variable

Readable:
```text
IF(IFDEFAULT(Get_Field(IRI_Mean)) AND Get_Field(PSI) > Get_Number(0),
    Get_Number(65)+(LOG(Get_Field(PSI)/Get_Number(5))/-Get_Number(0.0066))
,
    IF(IFDEFAULT(Get_Field(IRI_Mean)) AND (IFDEFAULT(Get_Field(PSI)) OR Get_Field(PSI) <= Get_Number(0)),
    Get_Number(0),
    Get_Field(IRI_Mean)
    )
)

```

Original:
```text
IF(IFDEFAULT(Get_Field(27134121-7932-4a33-8c47-a44035638fed)) AND Get_Field(1eca4d42-a141-4b12-8457-f11b987a6710) > Get_Number(0),
    Get_Number(65)+(LOG(Get_Field(1eca4d42-a141-4b12-8457-f11b987a6710)/Get_Number(5))/-Get_Number(0.0066))
,
    IF(IFDEFAULT(Get_Field(27134121-7932-4a33-8c47-a44035638fed)) AND (IFDEFAULT(Get_Field(1eca4d42-a141-4b12-8457-f11b987a6710)) OR Get_Field(1eca4d42-a141-4b12-8457-f11b987a6710) <= Get_Number(0)),
    Get_Number(0),
    Get_Field(27134121-7932-4a33-8c47-a44035638fed)
    )
)

```

<a id="e-77358d9c-32c1-4cda-a188-e4e53037b889"></a>

## PMS_ancCND_JCI_C1

Source: `RuntimeExpressions` / `77358d9c-32c1-4cda-a188-e4e53037b889`.



Readable:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C1','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_JCI',TRUE))
```

Original:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C1','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_JCI',TRUE))
```

<a id="e-aced2001-8a85-4914-a80d-0bc858832b38"></a>

## PMS_ancCND_JCI_C2

Source: `RuntimeExpressions` / `aced2001-8a85-4914-a80d-0bc858832b38`.



Readable:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C2','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_JCI',TRUE))
```

Original:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C2','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_JCI',TRUE))
```

<a id="e-f2a5c081-0c70-48c5-9762-10815e24ca8e"></a>

## PMS_ancCND_JCI_C3

Source: `RuntimeExpressions` / `f2a5c081-0c70-48c5-9762-10815e24ca8e`.



Readable:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C3','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_JCI',TRUE))
```

Original:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C3','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_JCI',TRUE))
```

<a id="e-03b63a24-1685-4775-b6d2-d9d95d796ab1"></a>

## PMS_ancCND_JCI_CURVE_TYPE

Source: `RuntimeExpressions` / `03b63a24-1685-4775-b6d2-d9d95d796ab1`.



Readable:
```text
DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','CURVE_TYPE','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_JCI',TRUE)
```

Original:
```text
DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','CURVE_TYPE','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_JCI',TRUE)
```

<a id="e-b7b74b73-7c42-44c2-a5ea-eb650a3fa094"></a>

## PMS_ancCND_JCI_INDEX_FROM_AGE

Source: `RuntimeExpressions` / `b7b74b73-7c42-44c2-a5ea-eb650a3fa094`.



Readable:
```text
IF(GET_ANALVR(PMS_tDAV_Pave_Type) <>'RC',Get_Number(0),
MAX(DAL_DCG_INDEXFROMAGE(Get_Exp(PMS_ancCND_JCI_CURVE_TYPE),Get_Exp(PMS_ancCND_JCI_C1),Get_Exp(PMS_ancCND_JCI_C2),Get_Exp(PMS_ancCND_JCI_C3),Get_Number(5),GET_ANALVR(PMS_nAAV_AGE_JCI)),Get_Number(0)))
```

Original:
```text
IF(GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) <>'RC',Get_Number(0),
MAX(DAL_DCG_INDEXFROMAGE(Get_Exp(03b63a24-1685-4775-b6d2-d9d95d796ab1),Get_Exp(77358d9c-32c1-4cda-a188-e4e53037b889),Get_Exp(aced2001-8a85-4914-a80d-0bc858832b38),Get_Exp(f2a5c081-0c70-48c5-9762-10815e24ca8e),Get_Number(5),GET_ANALVR(d467ebc5-1588-4efb-a9e0-e7f8374b1e33)),Get_Number(0)))
```

<a id="e-162b0c4f-c6ce-410f-98b1-b0a9901654d9"></a>

## PMS_ancCND_JCI_Initial

Source: `RuntimeExpressions` / `162b0c4f-c6ce-410f-98b1-b0a9901654d9`.



Readable:
```text
IF(GET_ANALVR(PMS_tDAV_Pave_Type) <> 'RC',Get_Number(0),
IF(Get_Field(REHAB_COMPLETION_YEAR)>=Get_Field(COND_YEAR), IF(Get_Field(REHAB_TYPE)='Initial',Get_Number(5), 
IF(Get_Field(REHAB_TYPE)='Major',Get_Number(5),Get_Number(4.5))),Get_Field(JCI)) + (IF(Get_Field(REHAB_TYPE)='Initial',Get_Number(0.0026), 
IF(Get_Field(REHAB_TYPE)='Major',-Get_Number(0.0291),Get_Number(0.0189))) * (GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR))) + 
IF(Get_Field(REHAB_TYPE)='Initial',-Get_Number(0.0026), IF(Get_Field(REHAB_TYPE)='Major',-Get_Number(0.0032),-Get_Number(0.0094))) * 
(GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR)))**Get_Number(2) + 
IF(Get_Field(REHAB_TYPE)='Initial',Get_Number(2E-05), IF(Get_Field(REHAB_TYPE)='Major',Get_Number(4E-05),Get_Number(0.0001))) * 
(GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR)))**Get_Number(3))
)
```

Original:
```text
IF(GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) <> 'RC',Get_Number(0),
IF(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b)>=Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',Get_Number(5), 
IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',Get_Number(5),Get_Number(4.5))),Get_Field(55bf1979-2b98-41ae-ba50-eb1a09e9b050)) + (IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',Get_Number(0.0026), 
IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',-Get_Number(0.0291),Get_Number(0.0189))) * (GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) + 
IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',-Get_Number(0.0026), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',-Get_Number(0.0032),-Get_Number(0.0094))) * 
(GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c)))**Get_Number(2) + 
IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',Get_Number(2E-05), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',Get_Number(4E-05),Get_Number(0.0001))) * 
(GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c)))**Get_Number(3))
)
```

<a id="e-88b8dd8a-42ee-482b-99bd-adb6d378ad87"></a>

## PMS_ancCND_JCI_RSL

Source: `RuntimeExpressions` / `88b8dd8a-42ee-482b-99bd-adb6d378ad87`.



Readable:
```text
MAX(Get_Exp(PMS_ancAGE_JCI_AGE_FROM_THRESHOLD) - Get_Exp(PMS_ancAGE_JCI_AGE_FROM_INDEX), Get_Number(0))
```

Original:
```text
MAX(Get_Exp(33c5ead4-7b9b-4755-bbf0-1a2e72e0d94e) - Get_Exp(406b0cec-a9f1-4d25-a5aa-fad3184b4f0b), Get_Number(0))
```

<a id="e-30db2e9c-f0a4-4b16-b915-b1fc288b7788"></a>

## PMS_ancCND_JCI_RSL_THRESHOLD

Source: `dTIMSExpressions` / `30db2e9c-f0a4-4b16-b915-b1fc288b7788`.



Readable:
```text
IF(Get_Field(Sign)='1',Get_Number(2.5),
IF(Get_Field(Sign)='2',Get_Number(2),
IF(Get_Field(Sign)='3',Get_Number(1.5),
IF(Get_Field(Sign)='4',Get_Number(1),Get_Number(2.5)))))
```

Original:
```text
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='1',Get_Number(2.5),
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='2',Get_Number(2),
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='3',Get_Number(1.5),
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='4',Get_Number(1),Get_Number(2.5)))))
```

<a id="e-0452c4fb-af93-4324-bc0b-4576e857ae86"></a>

## PMS_ancCND_MAP21_GFP

Source: `RuntimeExpressions` / `0452c4fb-af93-4324-bc0b-4576e857ae86`.

Map 21 GFP

Readable:
```text
IF(Get_Exp(PMS_abfOBJ_Concrete),
     IF(GET_ANALVR(PMS_tAAV_IRI_GFP)= 'GOOD' AND GET_ANALVR(PMS_tAAV_PCRK_GFP) = 'GOOD' AND GET_ANALVR(PMS_tAAV_FLT_GFP) = 'GOOD',
    'GOOD'
    ,
        IF((GET_ANALVR(PMS_tAAV_IRI_GFP) ='POOR' AND (GET_ANALVR(PMS_tAAV_PCRK_GFP) = 'POOR' OR GET_ANALVR(PMS_tAAV_FLT_GFP) = 'POOR')) OR
            (GET_ANALVR(PMS_tAAV_PCRK_GFP) ='POOR' AND  (GET_ANALVR(PMS_tAAV_IRI_GFP) = 'POOR' OR GET_ANALVR(PMS_tAAV_FLT_GFP) = 'POOR')) OR 
             (GET_ANALVR(PMS_tAAV_FLT_GFP) ='POOR' AND  (GET_ANALVR(PMS_tAAV_IRI_GFP) = 'POOR' OR GET_ANALVR(PMS_tAAV_PCRK_GFP) = 'POOR')) ,    
            'POOR',
            'FAIR'
          )    
    )
    ,
    IF(GET_ANALVR(PMS_tAAV_IRI_GFP)= 'GOOD' AND GET_ANALVR(PMS_tAAV_PCRK_GFP) = 'GOOD' AND GET_ANALVR(PMS_tAAV_RUT_GFP) = 'GOOD',
    'GOOD'
    ,
        IF((GET_ANALVR(PMS_tAAV_IRI_GFP) ='POOR' AND (GET_ANALVR(PMS_tAAV_PCRK_GFP) = 'POOR' OR GET_ANALVR(PMS_tAAV_RUT_GFP) = 'POOR')) OR
            (GET_ANALVR(PMS_tAAV_PCRK_GFP) ='POOR' AND  (GET_ANALVR(PMS_tAAV_IRI_GFP) = 'POOR' OR GET_ANALVR(PMS_tAAV_RUT_GFP) = 'POOR')) OR 
             (GET_ANALVR(PMS_tAAV_RUT_GFP) ='POOR' AND  (GET_ANALVR(PMS_tAAV_IRI_GFP) = 'POOR' OR GET_ANALVR(PMS_tAAV_PCRK_GFP) = 'POOR')) ,    
            'POOR',
            'FAIR'
          )    
    )
)  
```

Original:
```text
IF(Get_Exp(ba469472-994d-4555-923b-c833047e7e8b),
     IF(GET_ANALVR(2b099e68-5f1a-442f-be4a-1755c71bd29a)= 'GOOD' AND GET_ANALVR(710f6af1-41a9-4fd8-b855-c96f1e578de1) = 'GOOD' AND GET_ANALVR(543300fc-1652-4e2d-a701-28d145bb4dca) = 'GOOD',
    'GOOD'
    ,
        IF((GET_ANALVR(2b099e68-5f1a-442f-be4a-1755c71bd29a) ='POOR' AND (GET_ANALVR(710f6af1-41a9-4fd8-b855-c96f1e578de1) = 'POOR' OR GET_ANALVR(543300fc-1652-4e2d-a701-28d145bb4dca) = 'POOR')) OR
            (GET_ANALVR(710f6af1-41a9-4fd8-b855-c96f1e578de1) ='POOR' AND  (GET_ANALVR(2b099e68-5f1a-442f-be4a-1755c71bd29a) = 'POOR' OR GET_ANALVR(543300fc-1652-4e2d-a701-28d145bb4dca) = 'POOR')) OR 
             (GET_ANALVR(543300fc-1652-4e2d-a701-28d145bb4dca) ='POOR' AND  (GET_ANALVR(2b099e68-5f1a-442f-be4a-1755c71bd29a) = 'POOR' OR GET_ANALVR(710f6af1-41a9-4fd8-b855-c96f1e578de1) = 'POOR')) ,    
            'POOR',
            'FAIR'
          )    
    )
    ,
    IF(GET_ANALVR(2b099e68-5f1a-442f-be4a-1755c71bd29a)= 'GOOD' AND GET_ANALVR(710f6af1-41a9-4fd8-b855-c96f1e578de1) = 'GOOD' AND GET_ANALVR(0941b34a-af87-4427-a9be-71fc98e80ff0) = 'GOOD',
    'GOOD'
    ,
        IF((GET_ANALVR(2b099e68-5f1a-442f-be4a-1755c71bd29a) ='POOR' AND (GET_ANALVR(710f6af1-41a9-4fd8-b855-c96f1e578de1) = 'POOR' OR GET_ANALVR(0941b34a-af87-4427-a9be-71fc98e80ff0) = 'POOR')) OR
            (GET_ANALVR(710f6af1-41a9-4fd8-b855-c96f1e578de1) ='POOR' AND  (GET_ANALVR(2b099e68-5f1a-442f-be4a-1755c71bd29a) = 'POOR' OR GET_ANALVR(0941b34a-af87-4427-a9be-71fc98e80ff0) = 'POOR')) OR 
             (GET_ANALVR(0941b34a-af87-4427-a9be-71fc98e80ff0) ='POOR' AND  (GET_ANALVR(2b099e68-5f1a-442f-be4a-1755c71bd29a) = 'POOR' OR GET_ANALVR(710f6af1-41a9-4fd8-b855-c96f1e578de1) = 'POOR')) ,    
            'POOR',
            'FAIR'
          )    
    )
)  
```

<a id="e-655ec16f-dbb3-4e03-96d8-f2af4498adcb"></a>

## PMS_ancCND_NCI_Initial

Source: `RuntimeExpressions` / `655ec16f-dbb3-4e03-96d8-f2af4498adcb`.



Readable:
```text
IF(Get_Field(REHAB_COMPLETION_YEAR)>=Get_Field(COND_YEAR), IF(Get_Field(REHAB_TYPE)='Initial',Get_Number(5), IF(Get_Field(REHAB_TYPE)='Major',Get_Number(5),Get_Number(4.5))),Get_Field(NCI)) + (IF(Get_Field(REHAB_TYPE)='Initial',Get_Number(0.007), IF(Get_Field(REHAB_TYPE)='Major',Get_Number(0.0089),Get_Number(0.0655))) * (GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR))) + IF(Get_Field(REHAB_TYPE)='Initial',-Get_Number(0.0029), IF(Get_Field(REHAB_TYPE)='Major',-Get_Number(0.0119),-Get_Number(0.0515))) * (GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR)))**Get_Number(2))
```

Original:
```text
IF(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b)>=Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',Get_Number(5), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',Get_Number(5),Get_Number(4.5))),Get_Field(cd5328e5-235e-491c-9d45-7a32be9717c3)) + (IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',Get_Number(0.007), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',Get_Number(0.0089),Get_Number(0.0655))) * (GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) + IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',-Get_Number(0.0029), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',-Get_Number(0.0119),-Get_Number(0.0515))) * (GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c)))**Get_Number(2))
```

<a id="e-b33b7403-ae8e-47b1-9bb8-a3b102200464"></a>

## PMS_ancCND_PCRK

Source: `RuntimeExpressions` / `b33b7403-ae8e-47b1-9bb8-a3b102200464`.

Percent Cracking

Readable:
```text
IF(Get_Exp(PMS_abfOBJ_Asphalt),
    IF(Get_Field(Sign) = '1',
        Get_Number(0.15) * Get_Exp(PMS_ancAGE_AGE_SCI),
    IF(Get_Field(Sign)<>'1' and Get_Field(HPMS) ='1',
        Get_Number(0.37) * Get_Exp(PMS_ancAGE_AGE_SCI),
        Get_Number(0.56) * Get_Exp(PMS_ancAGE_AGE_SCI))
       )
    ,
    IF(Get_Field(Sign) = '1',
        Get_Number(0.15) * Get_Exp(PMS_ancAGE_AGE_CCI),
    IF(Get_Field(Sign)<>'1' and Get_Field(HPMS) ='1',
        Get_Number(0.37) * Get_Exp(PMS_ancAGE_AGE_CCI),
        Get_Number(0.56) * Get_Exp(PMS_ancAGE_AGE_CCI))
    )
)
```

Original:
```text
IF(Get_Exp(915f80f1-74d8-48c0-ab9f-fdffd05d547a),
    IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) = '1',
        Get_Number(0.15) * Get_Exp(70e13ebd-e481-49a1-ac3d-1290864cde14),
    IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)<>'1' and Get_Field(7da5a5a8-cf02-45c1-bea8-97599fc41064) ='1',
        Get_Number(0.37) * Get_Exp(70e13ebd-e481-49a1-ac3d-1290864cde14),
        Get_Number(0.56) * Get_Exp(70e13ebd-e481-49a1-ac3d-1290864cde14))
       )
    ,
    IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) = '1',
        Get_Number(0.15) * Get_Exp(52fb3718-9639-4250-b7f5-63c1eb51435c),
    IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)<>'1' and Get_Field(7da5a5a8-cf02-45c1-bea8-97599fc41064) ='1',
        Get_Number(0.37) * Get_Exp(52fb3718-9639-4250-b7f5-63c1eb51435c),
        Get_Number(0.56) * Get_Exp(52fb3718-9639-4250-b7f5-63c1eb51435c))
    )
)
```

<a id="e-40e28ca8-4605-426b-8c97-7b2c1cc92571"></a>

## PMS_ancCND_PCRK_GFP

Source: `RuntimeExpressions` / `40e28ca8-4605-426b-8c97-7b2c1cc92571`.

Percent Cracking Good Fair Poor

Readable:
```text
IF(Get_Exp(PMS_abfOBJ_Asphalt),
    IF(GET_ANALVR(PMS_nAAV_CND_PCRK) < Get_Number(5), 'GOOD', IF(GET_ANALVR(PMS_nAAV_CND_PCRK)>Get_Number(20),'POOR','FAIR'))
    ,
    IF(GET_ANALVR(PMS_nAAV_CND_PCRK) < Get_Number(5), 'GOOD', IF(GET_ANALVR(PMS_nAAV_CND_PCRK)>Get_Number(15),'POOR','FAIR'))
)
```

Original:
```text
IF(Get_Exp(915f80f1-74d8-48c0-ab9f-fdffd05d547a),
    IF(GET_ANALVR(af5bdd9f-eefc-48c3-bd24-ffd829d416fb) < Get_Number(5), 'GOOD', IF(GET_ANALVR(af5bdd9f-eefc-48c3-bd24-ffd829d416fb)>Get_Number(20),'POOR','FAIR'))
    ,
    IF(GET_ANALVR(af5bdd9f-eefc-48c3-bd24-ffd829d416fb) < Get_Number(5), 'GOOD', IF(GET_ANALVR(af5bdd9f-eefc-48c3-bd24-ffd829d416fb)>Get_Number(15),'POOR','FAIR'))
)
```

<a id="e-d1b6733c-a79d-48cd-a31d-27b4c0073712"></a>

## PMS_ancCND_PSI_C1

Source: `RuntimeExpressions` / `d1b6733c-a79d-48cd-a31d-27b4c0073712`.



Readable:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C1','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_PSI',TRUE))
```

Original:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C1','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_PSI',TRUE))
```

<a id="e-63c8390a-6580-4358-85f7-e547c4fee0ba"></a>

## PMS_ancCND_PSI_C2

Source: `RuntimeExpressions` / `63c8390a-6580-4358-85f7-e547c4fee0ba`.



Readable:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C2','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_PSI',TRUE))
```

Original:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C2','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_PSI',TRUE))
```

<a id="e-79e5e0b0-4200-422b-8535-98b7a8cd9d4c"></a>

## PMS_ancCND_PSI_C3

Source: `RuntimeExpressions` / `79e5e0b0-4200-422b-8535-98b7a8cd9d4c`.



Readable:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C3','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_PSI',TRUE))
```

Original:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C3','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_PSI',TRUE))
```

<a id="e-17d2a601-da54-4580-980b-33f85f640b76"></a>

## PMS_ancCND_PSI_CURVE_TYPE

Source: `RuntimeExpressions` / `17d2a601-da54-4580-980b-33f85f640b76`.



Readable:
```text
DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','CURVE_TYPE','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_PSI',TRUE)
```

Original:
```text
DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','CURVE_TYPE','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_PSI',TRUE)
```

<a id="e-59b5c182-f146-4e8e-a5a1-7f60794af229"></a>

## PMS_ancCND_PSI_INDEX_FROM_AGE

Source: `RuntimeExpressions` / `59b5c182-f146-4e8e-a5a1-7f60794af229`.



Readable:
```text
IF(DAL_DCG_INDEXFROMAGE(Get_Exp(PMS_ancCND_PSI_CURVE_TYPE),Get_Exp(PMS_ancCND_PSI_C1),Get_Exp(PMS_ancCND_PSI_C2),Get_Exp(PMS_ancCND_PSI_C3),Get_Number(5),GET_ANALVR(PMS_nAAV_AGE_PSI))<=Get_Number(0)
,
Get_Number(0)
,
DAL_DCG_INDEXFROMAGE(Get_Exp(PMS_ancCND_PSI_CURVE_TYPE),Get_Exp(PMS_ancCND_PSI_C1),Get_Exp(PMS_ancCND_PSI_C2),Get_Exp(PMS_ancCND_PSI_C3),Get_Number(5),GET_ANALVR(PMS_nAAV_AGE_PSI))
)
```

Original:
```text
IF(DAL_DCG_INDEXFROMAGE(Get_Exp(17d2a601-da54-4580-980b-33f85f640b76),Get_Exp(d1b6733c-a79d-48cd-a31d-27b4c0073712),Get_Exp(63c8390a-6580-4358-85f7-e547c4fee0ba),Get_Exp(79e5e0b0-4200-422b-8535-98b7a8cd9d4c),Get_Number(5),GET_ANALVR(963cad98-9956-4ef6-a261-11b0358133b5))<=Get_Number(0)
,
Get_Number(0)
,
DAL_DCG_INDEXFROMAGE(Get_Exp(17d2a601-da54-4580-980b-33f85f640b76),Get_Exp(d1b6733c-a79d-48cd-a31d-27b4c0073712),Get_Exp(63c8390a-6580-4358-85f7-e547c4fee0ba),Get_Exp(79e5e0b0-4200-422b-8535-98b7a8cd9d4c),Get_Number(5),GET_ANALVR(963cad98-9956-4ef6-a261-11b0358133b5))
)
```

<a id="e-10d57536-503d-4d5b-8cc5-2a67e5835864"></a>

## PMS_ancCND_PSI_Initial

Source: `RuntimeExpressions` / `10d57536-503d-4d5b-8cc5-2a67e5835864`.



Readable:
```text
IF(Get_Field(REHAB_COMPLETION_YEAR)>=Get_Field(COND_YEAR), IF(Get_Field(REHAB_TYPE)='Initial',Get_Number(5), IF(Get_Field(REHAB_TYPE)='Major',Get_Number(5),Get_Number(4.5))),Get_Field(PSI)) + IF(GET_ANALVR(PMS_tDAV_Pave_Type) = 'BC', (IF(Get_Field(REHAB_TYPE)='Initial',-Get_Number(0.0266), IF(Get_Field(REHAB_TYPE)='Major',-Get_Number(0.1404),-Get_Number(0.1289))) * (GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR))) + IF(Get_Field(REHAB_TYPE)='Initial',Get_Number(3E-05), IF(Get_Field(REHAB_TYPE)='Major',-Get_Number(0.0014),-Get_Number(0.002))) * (GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR)))**Get_Number(2) + IF(Get_Field(REHAB_TYPE)='Initial',-Get_Number(5E-05), IF(Get_Field(REHAB_TYPE)='Major',Get_Number(4E-05),Get_Number(0))) * (GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR)))**Get_Number(3)),
	(IF(Get_Field(REHAB_TYPE)='Initial',Get_Number(0.0026), IF(Get_Field(REHAB_TYPE)='Major',-Get_Number(0.0291),Get_Number(0.0189))) * (GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR))) + IF(Get_Field(REHAB_TYPE)='Initial',-Get_Number(0.0026), IF(Get_Field(REHAB_TYPE)='Major',-Get_Number(0.0032),-Get_Number(0.0094))) * (GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR)))**Get_Number(2) + IF(Get_Field(REHAB_TYPE)='Initial',Get_Number(2E-05), IF(Get_Field(REHAB_TYPE)='Major',Get_Number(4E-05),Get_Number(0.0001))) * (GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR)))**Get_Number(3)))
```

Original:
```text
IF(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b)>=Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',Get_Number(5), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',Get_Number(5),Get_Number(4.5))),Get_Field(1eca4d42-a141-4b12-8457-f11b987a6710)) + IF(GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) = 'BC', (IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',-Get_Number(0.0266), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',-Get_Number(0.1404),-Get_Number(0.1289))) * (GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) + IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',Get_Number(3E-05), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',-Get_Number(0.0014),-Get_Number(0.002))) * (GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c)))**Get_Number(2) + IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',-Get_Number(5E-05), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',Get_Number(4E-05),Get_Number(0))) * (GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c)))**Get_Number(3)),
	(IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',Get_Number(0.0026), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',-Get_Number(0.0291),Get_Number(0.0189))) * (GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) + IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',-Get_Number(0.0026), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',-Get_Number(0.0032),-Get_Number(0.0094))) * (GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c)))**Get_Number(2) + IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',Get_Number(2E-05), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',Get_Number(4E-05),Get_Number(0.0001))) * (GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c)))**Get_Number(3)))
```

<a id="e-d99aa3f7-1a4d-42ad-a07d-e600ebb133e8"></a>

## PMS_ancCND_PSI_RSL

Source: `RuntimeExpressions` / `d99aa3f7-1a4d-42ad-a07d-e600ebb133e8`.



Readable:
```text
MAX(Get_Exp(PMS_ancAGE_PSI_AGE_FROM_THRESHOLD) - Get_Exp(PMS_ancAGE_PSI_AGE_FROM_INDEX), Get_Number(0))
```

Original:
```text
MAX(Get_Exp(e1db4a5b-aca3-4b8e-8cb1-eddbb664a0ac) - Get_Exp(af3d20fc-fa3b-4485-bcee-8714e4acca9f), Get_Number(0))
```

<a id="e-34f9912f-4c09-4215-89bc-d618fefa95e1"></a>

## PMS_ancCND_PSI_RSL_THRESHOLD

Source: `dTIMSExpressions` / `34f9912f-4c09-4215-89bc-d618fefa95e1`.



Readable:
```text
IF(Get_Field(Sign)='1',Get_Number(2.5),
IF(Get_Field(Sign)='2',Get_Number(2),
IF(Get_Field(Sign)='3',Get_Number(1.5),
IF(Get_Field(Sign)='4',Get_Number(1),Get_Number(2.5)))))
```

Original:
```text
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='1',Get_Number(2.5),
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='2',Get_Number(2),
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='3',Get_Number(1.5),
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='4',Get_Number(1),Get_Number(2.5)))))
```

<a id="e-8f127ce9-f811-444d-a301-79602909dd96"></a>

## PMS_ancCND_RDI_C1

Source: `RuntimeExpressions` / `8f127ce9-f811-444d-a301-79602909dd96`.



Readable:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C1','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_RDI',TRUE))
```

Original:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C1','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_RDI',TRUE))
```

<a id="e-057ac914-2bc4-4a37-8dad-ebf6a43261e5"></a>

## PMS_ancCND_RDI_C2

Source: `RuntimeExpressions` / `057ac914-2bc4-4a37-8dad-ebf6a43261e5`.



Readable:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C2','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_RDI',TRUE))
```

Original:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C2','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_RDI',TRUE))
```

<a id="e-9d84a96d-0bc9-4de3-b4ec-b5627c5c925e"></a>

## PMS_ancCND_RDI_C3

Source: `RuntimeExpressions` / `9d84a96d-0bc9-4de3-b4ec-b5627c5c925e`.



Readable:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C3','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_RDI',TRUE))
```

Original:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C3','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_RDI',TRUE))
```

<a id="e-0eea476a-532b-4694-af9e-b1dbb333b085"></a>

## PMS_ancCND_RDI_CURVE_TYPE

Source: `RuntimeExpressions` / `0eea476a-532b-4694-af9e-b1dbb333b085`.



Readable:
```text
DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','CURVE_TYPE','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_RDI',TRUE)
```

Original:
```text
DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','CURVE_TYPE','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_RDI',TRUE)
```

<a id="e-4241f9d0-0932-4f66-bf42-53667d2cf18c"></a>

## PMS_ancCND_RDI_INDEX_FROM_AGE

Source: `RuntimeExpressions` / `4241f9d0-0932-4f66-bf42-53667d2cf18c`.



Readable:
```text
IF(GET_ANALVR(PMS_tDAV_Pave_Type)='RC',Get_Number(0),
MAX(DAL_DCG_INDEXFROMAGE(Get_Exp(PMS_ancCND_RDI_CURVE_TYPE),Get_Exp(PMS_ancCND_RDI_C1),Get_Exp(PMS_ancCND_RDI_C2),Get_Exp(PMS_ancCND_RDI_C3),Get_Number(5),GET_ANALVR(PMS_nAAV_AGE_RDI)),Get_Number(0))
)
```

Original:
```text
IF(GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2)='RC',Get_Number(0),
MAX(DAL_DCG_INDEXFROMAGE(Get_Exp(0eea476a-532b-4694-af9e-b1dbb333b085),Get_Exp(8f127ce9-f811-444d-a301-79602909dd96),Get_Exp(057ac914-2bc4-4a37-8dad-ebf6a43261e5),Get_Exp(9d84a96d-0bc9-4de3-b4ec-b5627c5c925e),Get_Number(5),GET_ANALVR(6426b3ef-fc9a-45ad-a2c3-6146882e9d20)),Get_Number(0))
)
```

<a id="e-4225f404-5bcd-4741-83c1-5e018f1ad2e2"></a>

## PMS_ancCND_RDI_Initial

Source: `RuntimeExpressions` / `4225f404-5bcd-4741-83c1-5e018f1ad2e2`.



Readable:
```text
IF(GET_ANALVR(PMS_tDAV_Pave_Type)='RC',Get_Number(0),
IF(Get_Field(REHAB_COMPLETION_YEAR)>=Get_Field(COND_YEAR), 
IF(Get_Field(REHAB_TYPE)='Initial',Get_Number(5), IF(Get_Field(REHAB_TYPE)='Major',Get_Number(5),Get_Number(4.5))),Get_Field(RDI)) + 
(IF(Get_Field(REHAB_TYPE)='Initial',-Get_Number(0.0266), IF(Get_Field(REHAB_TYPE)='Major',-Get_Number(0.1404),-Get_Number(0.1289))) * 
(GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR))) + 
IF(Get_Field(REHAB_TYPE)='Initial',Get_Number(3E-05), IF(Get_Field(REHAB_TYPE)='Major',-Get_Number(0.0014),-Get_Number(0.002))) * 
(GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR)))**Get_Number(2) +
IF(Get_Field(REHAB_TYPE)='Initial',-Get_Number(5E-05), IF(Get_Field(REHAB_TYPE)='Major',Get_Number(4E-05),Get_Number(0))) *
(GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR)))**Get_Number(3))
)
```

Original:
```text
IF(GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2)='RC',Get_Number(0),
IF(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b)>=Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c), 
IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',Get_Number(5), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',Get_Number(5),Get_Number(4.5))),Get_Field(be1a4d5a-ea19-4e1a-a61d-c1b792828006)) + 
(IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',-Get_Number(0.0266), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',-Get_Number(0.1404),-Get_Number(0.1289))) * 
(GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) + 
IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',Get_Number(3E-05), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',-Get_Number(0.0014),-Get_Number(0.002))) * 
(GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c)))**Get_Number(2) +
IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',-Get_Number(5E-05), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',Get_Number(4E-05),Get_Number(0))) *
(GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c)))**Get_Number(3))
)
```

<a id="e-9b84a780-f71e-4bf0-97f0-82c235067efe"></a>

## PMS_ancCND_RDI_RSL

Source: `RuntimeExpressions` / `9b84a780-f71e-4bf0-97f0-82c235067efe`.



Readable:
```text
MAX(Get_Exp(PMS_ancAGE_RDI_AGE_FROM_THRESHOLD) - Get_Exp(PMS_ancAGE_RDI_AGE_FROM_INDEX), Get_Number(0))
```

Original:
```text
MAX(Get_Exp(6aa9eb45-9551-4bc3-aaea-8b23c30bf5eb) - Get_Exp(193bb441-a7ab-412f-9d12-ab4247b78d6a), Get_Number(0))
```

<a id="e-e40492b6-33b5-4312-abfc-f846c2103d16"></a>

## PMS_ancCND_RDI_RSL_THRESHOLD

Source: `dTIMSExpressions` / `e40492b6-33b5-4312-abfc-f846c2103d16`.



Readable:
```text
IF(Get_Field(Sign)='1',Get_Number(2.5),
IF(Get_Field(Sign)='2',Get_Number(2),
IF(Get_Field(Sign)='3',Get_Number(1.5),
IF(Get_Field(Sign)='4',Get_Number(1),Get_Number(2.5)))))
```

Original:
```text
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='1',Get_Number(2.5),
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='2',Get_Number(2),
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='3',Get_Number(1.5),
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='4',Get_Number(1),Get_Number(2.5)))))
```

<a id="e-7fbb09b7-c2ae-4497-8890-e69a5d3999b6"></a>

## PMS_ancCND_RSL

Source: `RuntimeExpressions` / `7fbb09b7-c2ae-4497-8890-e69a5d3999b6`.



Readable:
```text
ROUND(IF(GET_ANALVR(PMS_tDAV_Pave_Type) = 'BC', DAL_DCG_MIN10(Get_Exp(PMS_ancCND_CCI_RSL),Get_Exp(PMS_ancCND_ECI_RSL),Get_Exp(PMS_ancCND_PSI_RSL),Get_Exp(PMS_ancCND_RDI_RSL),Get_Exp(PMS_ancCND_SCI_RSL),Get_Number(999),Get_Number(999),Get_Number(999),Get_Number(999),Get_Number(999)), 
	DAL_DCG_MIN10(Get_Exp(PMS_ancCND_CCI_RSL),Get_Exp(PMS_ancCND_JCI_RSL),Get_Exp(PMS_ancCND_PSI_RSL),Get_Exp(PMS_ancCND_RDI_RSL),Get_Exp(PMS_ancCND_CSI_RSL),Get_Number(999),Get_Number(999),Get_Number(999),Get_Number(999),Get_Number(999))),Get_Number(0))
```

Original:
```text
ROUND(IF(GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) = 'BC', DAL_DCG_MIN10(Get_Exp(ea0596f8-2e1b-4a7b-9a8a-3cbddb992f82),Get_Exp(f80bc936-95cf-4aa7-8d49-ffacd24fb8ed),Get_Exp(d99aa3f7-1a4d-42ad-a07d-e600ebb133e8),Get_Exp(9b84a780-f71e-4bf0-97f0-82c235067efe),Get_Exp(743b5c2f-8470-429c-9665-795ce12ccc8c),Get_Number(999),Get_Number(999),Get_Number(999),Get_Number(999),Get_Number(999)), 
	DAL_DCG_MIN10(Get_Exp(ea0596f8-2e1b-4a7b-9a8a-3cbddb992f82),Get_Exp(88b8dd8a-42ee-482b-99bd-adb6d378ad87),Get_Exp(d99aa3f7-1a4d-42ad-a07d-e600ebb133e8),Get_Exp(9b84a780-f71e-4bf0-97f0-82c235067efe),Get_Exp(1de251ee-bc69-4d3a-9fa7-7c09071eca38),Get_Number(999),Get_Number(999),Get_Number(999),Get_Number(999),Get_Number(999))),Get_Number(0))
```

<a id="e-04c76ab6-b287-4c9d-9399-90033e4cc5e7"></a>

## PMS_ancCND_RUT_GFP

Source: `RuntimeExpressions` / `04c76ab6-b287-4c9d-9399-90033e4cc5e7`.

Rut Good Fair Poor

Readable:
```text
IF(GET_ANALVR(PMS_nAAV_CND_RUT) < Get_Number(0.2), 'GOOD', IF(GET_ANALVR(PMS_nAAV_CND_RUT)>Get_Number(0.4),'POOR','FAIR'))
```

Original:
```text
IF(GET_ANALVR(f3e74fb6-1f0d-42f0-afe1-f83662c8c3ed) < Get_Number(0.2), 'GOOD', IF(GET_ANALVR(f3e74fb6-1f0d-42f0-afe1-f83662c8c3ed)>Get_Number(0.4),'POOR','FAIR'))
```

<a id="e-33765a3e-e46b-4c74-938c-0b09f833886c"></a>

## PMS_ancCND_RUT_Initialize

Source: `dTIMSExpressions` / `33765a3e-e46b-4c74-938c-0b09f833886c`.

Initialize Rut Variable

Readable:
```text
IF(IFDEFAULT(Get_Field(Rut_Mean)) and Get_Field(RDI) > Get_Number(0),
       ((Get_Number(5)-Get_Field(RDI))/Get_Number(6.65))**(Get_Number(1)/Get_Number(1.41))
,
    IF(IFDEFAULT(Get_Field(Rut_Mean)) and (IFDEFAULT(Get_Field(RDI)) or Get_Field(RDI) <= Get_Number(0) or Get_Field(Rut_Mean)< Get_Number(0)),
    Get_Number(0),
    Get_Field(Rut_Mean)
    )
)
```

Original:
```text
IF(IFDEFAULT(Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c)) and Get_Field(be1a4d5a-ea19-4e1a-a61d-c1b792828006) > Get_Number(0),
       ((Get_Number(5)-Get_Field(be1a4d5a-ea19-4e1a-a61d-c1b792828006))/Get_Number(6.65))**(Get_Number(1)/Get_Number(1.41))
,
    IF(IFDEFAULT(Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c)) and (IFDEFAULT(Get_Field(be1a4d5a-ea19-4e1a-a61d-c1b792828006)) or Get_Field(be1a4d5a-ea19-4e1a-a61d-c1b792828006) <= Get_Number(0) or Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c)< Get_Number(0)),
    Get_Number(0),
    Get_Field(f8bd4e90-5596-4b91-8202-8b8770acaf1c)
    )
)
```

<a id="e-4f8cf211-5f31-4d5e-92dd-6f048cf7f6c6"></a>

## PMS_ancCND_Rut

Source: `RuntimeExpressions` / `4f8cf211-5f31-4d5e-92dd-6f048cf7f6c6`.

Rut

Readable:
```text
((Get_Number(5)-GET_ANALVR(PMS_nAAV_CND_RDI))/Get_Number(6.65))**(Get_Number(1)/Get_Number(1.41))
```

Original:
```text
((Get_Number(5)-GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff))/Get_Number(6.65))**(Get_Number(1)/Get_Number(1.41))
```

<a id="e-65ab65d5-6019-412f-9ac8-a844ed507692"></a>

## PMS_ancCND_SCI_C1

Source: `RuntimeExpressions` / `65ab65d5-6019-412f-9ac8-a844ed507692`.



Readable:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C1','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_SCI',TRUE))
```

Original:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C1','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_SCI',TRUE))
```

<a id="e-5f220dc4-d862-4a14-9435-c7548f2ba9f1"></a>

## PMS_ancCND_SCI_C2

Source: `RuntimeExpressions` / `5f220dc4-d862-4a14-9435-c7548f2ba9f1`.



Readable:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C2','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_SCI',TRUE))
```

Original:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C2','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_SCI',TRUE))
```

<a id="e-0fb1a984-fb16-46f3-a9aa-a917b5c6fc55"></a>

## PMS_ancCND_SCI_C3

Source: `RuntimeExpressions` / `0fb1a984-fb16-46f3-a9aa-a917b5c6fc55`.



Readable:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C3','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_SCI',TRUE))
```

Original:
```text
VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','C3','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_SCI',TRUE))
```

<a id="e-a8f46b77-c07c-4d9f-a1aa-ad7fc8951798"></a>

## PMS_ancCND_SCI_CURVE_TYPE

Source: `RuntimeExpressions` / `a8f46b77-c07c-4d9f-a1aa-ad7fc8951798`.



Readable:
```text
DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','CURVE_TYPE','KEY',GET_ANALVR(PMS_tDAV_Pave_Type) + '_' + GET_ANALVR(PMS_tDAV_Rehab_Type) + '_' + GET_ANALVR(PMS_tDAV_Truck_Load) + '_SCI',TRUE)
```

Original:
```text
DAL_DCG_STLOOKUP('Analysis_Lookup_Perf_Coef','CURVE_TYPE','KEY',GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2) + '_' + GET_ANALVR(2bd5f4a4-a022-41c7-addf-e2f58dc002ad) + '_' + GET_ANALVR(995b8200-bdf4-4234-81ed-0a42a8648127) + '_SCI',TRUE)
```

<a id="e-15450a71-28ce-48cc-ab6d-b85b1e31ffd6"></a>

## PMS_ancCND_SCI_INDEX_FROM_AGE

Source: `RuntimeExpressions` / `15450a71-28ce-48cc-ab6d-b85b1e31ffd6`.



Readable:
```text
MAX(DAL_DCG_INDEXFROMAGE(Get_Exp(PMS_ancCND_SCI_CURVE_TYPE),Get_Exp(PMS_ancCND_SCI_C1),Get_Exp(PMS_ancCND_SCI_C2),Get_Exp(PMS_ancCND_SCI_C3),Get_Number(5),GET_ANALVR(PMS_nAAV_AGE_SCI)),Get_Number(0))
```

Original:
```text
MAX(DAL_DCG_INDEXFROMAGE(Get_Exp(a8f46b77-c07c-4d9f-a1aa-ad7fc8951798),Get_Exp(65ab65d5-6019-412f-9ac8-a844ed507692),Get_Exp(5f220dc4-d862-4a14-9435-c7548f2ba9f1),Get_Exp(0fb1a984-fb16-46f3-a9aa-a917b5c6fc55),Get_Number(5),GET_ANALVR(c4865c39-9e55-4179-85e9-0cc0c3e09081)),Get_Number(0))
```

<a id="e-a42a12a8-dd50-4e3f-ad1f-ce1ab73e421b"></a>

## PMS_ancCND_SCI_Initial

Source: `RuntimeExpressions` / `a42a12a8-dd50-4e3f-ad1f-ce1ab73e421b`.



Readable:
```text
IF(IFDEFAULT(Get_Field(SCI)),Get_Number(0),
IF(Get_Field(REHAB_COMPLETION_YEAR)>=Get_Field(COND_YEAR),
IF(Get_Field(REHAB_TYPE)='Initial',Get_Number(5), 
IF(Get_Field(REHAB_TYPE)='Major',Get_Number(5),Get_Number(4.5))),Get_Field(SCI)) + (IF(Get_Field(REHAB_TYPE)='Initial',-Get_Number(0.0266), IF(Get_Field(REHAB_TYPE)='Major',-Get_Number(0.1404),-Get_Number(0.1289))) * (GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR))) + IF(Get_Field(REHAB_TYPE)='Initial',Get_Number(3E-05), IF(Get_Field(REHAB_TYPE)='Major',-Get_Number(0.0014),-Get_Number(0.002))) * (GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR)))**Get_Number(2) + IF(Get_Field(REHAB_TYPE)='Initial',-Get_Number(5E-05), IF(Get_Field(REHAB_TYPE)='Major',Get_Number(4E-05),Get_Number(0))) * (GSTART_YR - MAX(Get_Field(REHAB_COMPLETION_YEAR), Get_Field(COND_YEAR)))**Get_Number(3))
)
```

Original:
```text
IF(IFDEFAULT(Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)),Get_Number(0),
IF(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b)>=Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c),
IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',Get_Number(5), 
IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',Get_Number(5),Get_Number(4.5))),Get_Field(03732942-74d5-4ee7-83c5-b79614da3a04)) + (IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',-Get_Number(0.0266), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',-Get_Number(0.1404),-Get_Number(0.1289))) * (GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c))) + IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',Get_Number(3E-05), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',-Get_Number(0.0014),-Get_Number(0.002))) * (GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c)))**Get_Number(2) + IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Initial',-Get_Number(5E-05), IF(Get_Field(1814a3dd-89fc-4217-88e2-ab43eefbce5b)='Major',Get_Number(4E-05),Get_Number(0))) * (GSTART_YR - MAX(Get_Field(42cf662a-e349-4837-a84e-43b002a7661b), Get_Field(9feb6ad7-8d91-4e7b-babf-2c759d780a6c)))**Get_Number(3))
)
```

<a id="e-743b5c2f-8470-429c-9665-795ce12ccc8c"></a>

## PMS_ancCND_SCI_RSL

Source: `RuntimeExpressions` / `743b5c2f-8470-429c-9665-795ce12ccc8c`.



Readable:
```text
MAX(Get_Exp(PMS_ancAGE_SCI_AGE_FROM_THRESHOLD) - Get_Exp(PMS_ancAGE_SCI_AGE_FROM_INDEX), Get_Number(0))
```

Original:
```text
MAX(Get_Exp(4fb2afe3-0860-4110-a0c8-f7137db0407c) - Get_Exp(2ef1c4f5-220d-45a3-860d-d073db59ef9e), Get_Number(0))
```

<a id="e-87339c27-eb9d-47cb-99a4-9f091d53609c"></a>

## PMS_ancCND_SCI_RSL_THRESHOLD

Source: `dTIMSExpressions` / `87339c27-eb9d-47cb-99a4-9f091d53609c`.



Readable:
```text
IF(Get_Field(Sign)='1',Get_Number(2.5),
IF(Get_Field(Sign)='2',Get_Number(2),
IF(Get_Field(Sign)='3',Get_Number(1.5),
IF(Get_Field(Sign)='4',Get_Number(1),Get_Number(2.5)))))
```

Original:
```text
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='1',Get_Number(2.5),
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='2',Get_Number(2),
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='3',Get_Number(1.5),
IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)='4',Get_Number(1),Get_Number(2.5)))))
```

<a id="e-127e222a-3225-4a3a-aee1-356c08fa40c5"></a>

## PMS_ancCOST_Budget_Miles_Poor

Source: `RuntimeExpressions` / `127e222a-3225-4a3a-aee1-356c08fa40c5`.



Readable:
```text
IF(GET_ANALVR(PMS_tAAV_Category) = 'P',GET_LENGTH(Get_Perspective(Analysis))/IF(ISEMPTY(Get_Field(Sign)) OR IFDEFAULT(Get_Field(Sign)),Get_Number(1),IF(Get_Field(Budget_Category_Override) = 'Interstate_Poor',Get_Exp(PMS_Exp_Total_Miles_Interstate),IF(Get_Field(Budget_Category_Override) = 'APD_Poor',Get_Exp(PMS_Exp_Total_Miles_APD),IF(Get_Field(Budget_Category_Override) = 'US_Poor',Get_Exp(PMS_Exp_Total_Miles_US),IF(Get_Field(Budget_Category_Override) = 'WV_Poor',Get_Exp(PMS_Exp_Total_Miles_WV),IF(Get_Field(Budget_Category_Override) = 'County_Poor',Get_Exp(PMS_Exp_Total_Miles_County),IF(Get_Field(Budget_Category_Override) = 'NHS_Poor',Get_Exp(PMS_Exp_Total_Miles_NHS),Get_Number(1)))))))),Get_Number(0)) * Get_Number(100)
```

Original:
```text
IF(GET_ANALVR(15f52fa4-a938-4537-894a-189e39260297) = 'P',GET_LENGTH(Get_Perspective(068b15eb-cb1d-4b9c-bf8f-882734ecfc1c))/IF(ISEMPTY(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)) OR IFDEFAULT(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)),Get_Number(1),IF(Get_Field(8007a74e-31a9-43b9-9bc9-b472225b1a46) = 'Interstate_Poor',Get_Exp(0887554d-0770-4605-be75-50af1a7c2d83),IF(Get_Field(8007a74e-31a9-43b9-9bc9-b472225b1a46) = 'APD_Poor',Get_Exp(39292a76-a572-44cc-87f8-d560bde11c84),IF(Get_Field(8007a74e-31a9-43b9-9bc9-b472225b1a46) = 'US_Poor',Get_Exp(e4dc18b8-c261-4f0c-84d0-a321b2744b18),IF(Get_Field(8007a74e-31a9-43b9-9bc9-b472225b1a46) = 'WV_Poor',Get_Exp(5c02ed19-7c48-48d1-8a37-3600f59f90d4),IF(Get_Field(8007a74e-31a9-43b9-9bc9-b472225b1a46) = 'County_Poor',Get_Exp(14c3ef12-759b-4a65-b16b-d34a331725c6),IF(Get_Field(8007a74e-31a9-43b9-9bc9-b472225b1a46) = 'NHS_Poor',Get_Exp(b50bf686-5aae-4889-a20f-889da3162570),Get_Number(1)))))))),Get_Number(0)) * Get_Number(100)
```

<a id="e-a646494c-8a9a-40e5-8931-01ac02634f74"></a>

## PMS_ancCOST_Budget_Miles_Poor_NHSall

Source: `RuntimeExpressions` / `a646494c-8a9a-40e5-8931-01ac02634f74`.



Readable:
```text
IF(GET_ANALVR(PMS_nAAV_CND_PSI) < Get_Number(3.4), GET_LENGTH(Get_Perspective(Analysis))/ Get_Exp(PMS_Exp_Total_Miles_NHSall), Get_Number(0)) *Get_Number(100)
```

Original:
```text
IF(GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) < Get_Number(3.4), GET_LENGTH(Get_Perspective(068b15eb-cb1d-4b9c-bf8f-882734ecfc1c))/ Get_Exp(a69abb03-e9eb-47d1-805e-23cd82419ced), Get_Number(0)) *Get_Number(100)
```

<a id="e-2f1da24d-f199-4103-8e08-6c81d7c9c5c4"></a>

## PMS_ancCOST_Conc_Pvmt_Repair_Major

Source: `RuntimeExpressions` / `2f1da24d-f199-4103-8e08-6c81d7c9c5c4`.



Readable:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(COM_YR_2) OR YR=Get_Field(COM_YR_3) OR YR=Get_Field(COM_YR_4)),
    IF(YR=Get_Field(COM_YR_2),Get_Field(Com_Cost_2),
    IF(YR=Get_Field(COM_YR_3),Get_Field(Com_Cost_3),
    IF(YR=Get_Field(COM_YR_4),Get_Field(Com_Cost_4),Get_Number(0))))
    ,
    Get_Field(Length) * 
    IF(IFDEFAULT(Get_Field(Lanes_Total)),Get_Number(2),Get_Field(Lanes_Total)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','Major_CPR_Diamond_Grind' + '_' + '1' +'_' + GET_ANALVR(PMS_tDAV_Pave_Type),TRUE))
    * Get_Exp(PMS_ancCOST_Inflation)
)


```

Original:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) OR YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) OR YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)),
    IF(YR=Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),Get_Field(8122f017-da56-4071-96cc-6c232d8c8911),
    IF(YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(3432d1c0-3be8-411d-b152-cc2ca54734ee),
    IF(YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86),Get_Field(0f501102-10d5-4938-8a1c-f181c66fa722),Get_Number(0))))
    ,
    Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) * 
    IF(IFDEFAULT(Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)),Get_Number(2),Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','Major_CPR_Diamond_Grind' + '_' + '1' +'_' + GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2),TRUE))
    * Get_Exp(0aa0db60-e10a-4140-bc34-386cf64c4aee)
)


```

<a id="e-02562651-f8d5-49fb-a565-d6a66b98fe87"></a>

## PMS_ancCOST_Conc_Pvmt_Repair_Minor

Source: `RuntimeExpressions` / `02562651-f8d5-49fb-a565-d6a66b98fe87`.



Readable:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(COM_YR_2) OR YR=Get_Field(COM_YR_3) OR YR=Get_Field(COM_YR_4)),
    IF(YR=Get_Field(COM_YR_2),Get_Field(Com_Cost_2),
    IF(YR=Get_Field(COM_YR_3),Get_Field(Com_Cost_3),
    IF(YR=Get_Field(COM_YR_4),Get_Field(Com_Cost_4),Get_Number(0))))
    ,
    Get_Field(Length) * 
    IF(IFDEFAULT(Get_Field(Lanes_Total)),Get_Number(2),Get_Field(Lanes_Total)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','Minor_CPR_Diamond_Grind' + '_' + '1' +'_' + GET_ANALVR(PMS_tDAV_Pave_Type),TRUE))
    * Get_Exp(PMS_ancCOST_Inflation)
)

```

Original:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) OR YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) OR YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)),
    IF(YR=Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),Get_Field(8122f017-da56-4071-96cc-6c232d8c8911),
    IF(YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(3432d1c0-3be8-411d-b152-cc2ca54734ee),
    IF(YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86),Get_Field(0f501102-10d5-4938-8a1c-f181c66fa722),Get_Number(0))))
    ,
    Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) * 
    IF(IFDEFAULT(Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)),Get_Number(2),Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','Minor_CPR_Diamond_Grind' + '_' + '1' +'_' + GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2),TRUE))
    * Get_Exp(0aa0db60-e10a-4140-bc34-386cf64c4aee)
)

```

<a id="e-8711652e-c824-4e25-b85e-d6aa363f7c4b"></a>

## PMS_ancCOST_County_Chip_Seal

Source: `RuntimeExpressions` / `8711652e-c824-4e25-b85e-d6aa363f7c4b`.

Cost Expression for Chip Seal for counties

Readable:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(COM_YR_2) OR YR=Get_Field(COM_YR_3) OR YR=Get_Field(COM_YR_4)),
    IF(YR=Get_Field(COM_YR_2),Get_Field(Com_Cost_2),
    IF(YR=Get_Field(COM_YR_3),Get_Field(Com_Cost_3),
    IF(YR=Get_Field(COM_YR_4),Get_Field(Com_Cost_4),Get_Number(0))))
    ,
    Get_Field(Length) * 
        IF(IFDEFAULT(Get_Field(Lanes_Total)),Get_Number(2),Get_Field(Lanes_Total)) * 
        VAL(DAL_DCG_STLOOKUP('DEL_Analysis_Lookup_CountyTrt_Costs','DEL_Cost_Per_Lane_Mile','DEL_KEY','PMS_County_Chip_Seal' + '_'+ 
        LEFT(Get_Field(County),Get_Number(2)),TRUE)) * Get_Exp(PMS_ancCOST_Inflation))
```

Original:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) OR YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) OR YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)),
    IF(YR=Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),Get_Field(8122f017-da56-4071-96cc-6c232d8c8911),
    IF(YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(3432d1c0-3be8-411d-b152-cc2ca54734ee),
    IF(YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86),Get_Field(0f501102-10d5-4938-8a1c-f181c66fa722),Get_Number(0))))
    ,
    Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) * 
        IF(IFDEFAULT(Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)),Get_Number(2),Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)) * 
        VAL(DAL_DCG_STLOOKUP('DEL_Analysis_Lookup_CountyTrt_Costs','DEL_Cost_Per_Lane_Mile','DEL_KEY','PMS_County_Chip_Seal' + '_'+ 
        LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2)),TRUE)) * Get_Exp(0aa0db60-e10a-4140-bc34-386cf64c4aee))
```

<a id="e-1cb4792b-85b4-401c-9b18-5bb049572af2"></a>

## PMS_ancCOST_County_Microsurfacing

Source: `RuntimeExpressions` / `1cb4792b-85b4-401c-9b18-5bb049572af2`.

Cost Expression for Microsurfacing for county routes

Readable:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(COM_YR_2) OR YR=Get_Field(COM_YR_3) OR YR=Get_Field(COM_YR_4)),
    IF(YR=Get_Field(COM_YR_2),Get_Field(Com_Cost_2),
    IF(YR=Get_Field(COM_YR_3),Get_Field(Com_Cost_3),
    IF(YR=Get_Field(COM_YR_4),Get_Field(Com_Cost_4),Get_Number(0))))
    ,
    Get_Field(Length) * 
    IF(IFDEFAULT(Get_Field(Lanes_Total)),Get_Number(2),Get_Field(Lanes_Total)) * 
    VAL(DAL_DCG_STLOOKUP('DEL_Analysis_Lookup_CountyTrt_Costs','DEL_Cost_Per_Lane_Mile','DEL_KEY',
    'PMS_County_MicroSurface' + '_'+ LEFT(Get_Field(County),Get_Number(2)),TRUE))
     * Get_Exp(PMS_ancCOST_Inflation))
```

Original:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) OR YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) OR YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)),
    IF(YR=Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),Get_Field(8122f017-da56-4071-96cc-6c232d8c8911),
    IF(YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(3432d1c0-3be8-411d-b152-cc2ca54734ee),
    IF(YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86),Get_Field(0f501102-10d5-4938-8a1c-f181c66fa722),Get_Number(0))))
    ,
    Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) * 
    IF(IFDEFAULT(Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)),Get_Number(2),Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)) * 
    VAL(DAL_DCG_STLOOKUP('DEL_Analysis_Lookup_CountyTrt_Costs','DEL_Cost_Per_Lane_Mile','DEL_KEY',
    'PMS_County_MicroSurface' + '_'+ LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2)),TRUE))
     * Get_Exp(0aa0db60-e10a-4140-bc34-386cf64c4aee))
```

<a id="e-0d77d7ef-38b3-4e3b-b84f-72aa2c09158e"></a>

## PMS_ancCOST_County_Thick_Overlay

Source: `RuntimeExpressions` / `0d77d7ef-38b3-4e3b-b84f-72aa2c09158e`.

Cost Expression for Thick Overlay county routes

Readable:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(COM_YR_2) OR YR=Get_Field(COM_YR_3) OR YR=Get_Field(COM_YR_4)),
    IF(YR=Get_Field(COM_YR_2),Get_Field(Com_Cost_2),
    IF(YR=Get_Field(COM_YR_3),Get_Field(Com_Cost_3),
    IF(YR=Get_Field(COM_YR_4),Get_Field(Com_Cost_4),Get_Number(0))))
    ,
    Get_Field(Length) * 
    IF(IFDEFAULT(Get_Field(Lanes_Total)),Get_Number(2),Get_Field(Lanes_Total)) * 
    VAL(DAL_DCG_STLOOKUP('DEL_Analysis_Lookup_CountyTrt_Costs','DEL_Cost_Per_Lane_Mile','DEL_KEY',
    'PMS_County_Thick_Overlay' + '_'+ 
    LEFT(Get_Field(County),Get_Number(2)),TRUE))
     * Get_Exp(PMS_ancCOST_Inflation) *
    IF(LEFT(Get_Field(Sign),Get_Number(1))='1',Get_Number(1.2),Get_Number(1)))
```

Original:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) OR YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) OR YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)),
    IF(YR=Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),Get_Field(8122f017-da56-4071-96cc-6c232d8c8911),
    IF(YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(3432d1c0-3be8-411d-b152-cc2ca54734ee),
    IF(YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86),Get_Field(0f501102-10d5-4938-8a1c-f181c66fa722),Get_Number(0))))
    ,
    Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) * 
    IF(IFDEFAULT(Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)),Get_Number(2),Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)) * 
    VAL(DAL_DCG_STLOOKUP('DEL_Analysis_Lookup_CountyTrt_Costs','DEL_Cost_Per_Lane_Mile','DEL_KEY',
    'PMS_County_Thick_Overlay' + '_'+ 
    LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2)),TRUE))
     * Get_Exp(0aa0db60-e10a-4140-bc34-386cf64c4aee) *
    IF(LEFT(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c),Get_Number(1))='1',Get_Number(1.2),Get_Number(1)))
```

<a id="e-00f01427-122d-4794-b760-c616b79c8a00"></a>

## PMS_ancCOST_County_Thin_Overlay

Source: `RuntimeExpressions` / `00f01427-122d-4794-b760-c616b79c8a00`.

Cost Expression for County route Thin Overlay

Readable:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(COM_YR_2) OR YR=Get_Field(COM_YR_3) OR YR=Get_Field(COM_YR_4)),
    IF(YR=Get_Field(COM_YR_2),Get_Field(Com_Cost_2),
    IF(YR=Get_Field(COM_YR_3),Get_Field(Com_Cost_3),
    IF(YR=Get_Field(COM_YR_4),Get_Field(Com_Cost_4),Get_Number(0))))
    ,
    Get_Field(Length) * 
    IF(IFDEFAULT(Get_Field(Lanes_Total)),Get_Number(2),Get_Field(Lanes_Total)) * 
    VAL(DAL_DCG_STLOOKUP('DEL_Analysis_Lookup_CountyTrt_Costs','DEL_Cost_Per_Lane_Mile','DEL_KEY',
    'PMS_County_Thin_Overlay' + '_'+ 
    LEFT(Get_Field(County),Get_Number(2)),TRUE))
     * Get_Exp(PMS_ancCOST_Inflation))
```

Original:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) OR YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) OR YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)),
    IF(YR=Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),Get_Field(8122f017-da56-4071-96cc-6c232d8c8911),
    IF(YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(3432d1c0-3be8-411d-b152-cc2ca54734ee),
    IF(YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86),Get_Field(0f501102-10d5-4938-8a1c-f181c66fa722),Get_Number(0))))
    ,
    Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) * 
    IF(IFDEFAULT(Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)),Get_Number(2),Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)) * 
    VAL(DAL_DCG_STLOOKUP('DEL_Analysis_Lookup_CountyTrt_Costs','DEL_Cost_Per_Lane_Mile','DEL_KEY',
    'PMS_County_Thin_Overlay' + '_'+ 
    LEFT(Get_Field(1e5d3dad-fda7-4fa8-8b19-8dd87a7cb96c),Get_Number(2)),TRUE))
     * Get_Exp(0aa0db60-e10a-4140-bc34-386cf64c4aee))
```

<a id="e-da0f020d-59d5-4245-bff5-ea7af562224f"></a>

## PMS_ancCOST_Fair_Treatment_For_GFP_70P_Good

Source: `RuntimeExpressions` / `da0f020d-59d5-4245-bff5-ea7af562224f`.

Cost of the Fair treatment

Readable:
```text
    Get_Field(Length) * 
    IF(IFDEFAULT(Get_Field(Lanes_Total)),Get_Number(2),Get_Field(Lanes_Total)) * Get_Number(300000) * Get_Exp(PMS_ancCOST_Inflation) *
    IF(LEFT(Get_Field(Sign),Get_Number(1))='1',Get_Number(1.2),Get_Number(1))

//300000 is the thick overlay cost
```

Original:
```text
    Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) * 
    IF(IFDEFAULT(Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)),Get_Number(2),Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)) * Get_Number(300000) * Get_Exp(0aa0db60-e10a-4140-bc34-386cf64c4aee) *
    IF(LEFT(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c),Get_Number(1))='1',Get_Number(1.2),Get_Number(1))

//300000 is the thick overlay cost
```

<a id="e-0aa0db60-e10a-4140-bc34-386cf64c4aee"></a>

## PMS_ancCOST_Inflation

Source: `RuntimeExpressions` / `0aa0db60-e10a-4140-bc34-386cf64c4aee`.



Readable:
```text
((Get_Number(1) + GINFLATION ) ** (YR  - Get_Number(1)))
```

Original:
```text
((Get_Number(1) + GINFLATION ) ** (YR  - Get_Number(1)))
```

<a id="e-115f0959-e7c1-4c63-932d-20977377f2a9"></a>

## PMS_ancCOST_Major_HMA_Overlay

Source: `RuntimeExpressions` / `115f0959-e7c1-4c63-932d-20977377f2a9`.



Readable:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(COM_YR_2) OR YR=Get_Field(COM_YR_3) OR YR=Get_Field(COM_YR_4)),
    IF(YR=Get_Field(COM_YR_2),Get_Field(Com_Cost_2),
    IF(YR=Get_Field(COM_YR_3),Get_Field(Com_Cost_3),
    IF(YR=Get_Field(COM_YR_4),Get_Field(Com_Cost_4),Get_Number(0))))
    ,
    Get_Field(Length) * 
    IF(IFDEFAULT(Get_Field(Lanes_Total)),Get_Number(2),Get_Field(Lanes_Total)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','Thick_Overlay' + '_' + '1' +'_' + GET_ANALVR(PMS_tDAV_Pave_Type),TRUE))
     * Get_Exp(PMS_ancCOST_Inflation)
     * IF(LEFT(Get_Field(Sign),Get_Number(1))='1',Get_Number(1.2),Get_Number(1))
)


```

Original:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) OR YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) OR YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)),
    IF(YR=Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),Get_Field(8122f017-da56-4071-96cc-6c232d8c8911),
    IF(YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(3432d1c0-3be8-411d-b152-cc2ca54734ee),
    IF(YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86),Get_Field(0f501102-10d5-4938-8a1c-f181c66fa722),Get_Number(0))))
    ,
    Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) * 
    IF(IFDEFAULT(Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)),Get_Number(2),Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','Thick_Overlay' + '_' + '1' +'_' + GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2),TRUE))
     * Get_Exp(0aa0db60-e10a-4140-bc34-386cf64c4aee)
     * IF(LEFT(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c),Get_Number(1))='1',Get_Number(1.2),Get_Number(1))
)


```

<a id="e-e2cf5a47-96b8-45f4-8f0a-489a51b76369"></a>

## PMS_ancCOST_Minor_HMA_Overlay

Source: `RuntimeExpressions` / `e2cf5a47-96b8-45f4-8f0a-489a51b76369`.



Readable:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(COM_YR_2) OR YR=Get_Field(COM_YR_3) OR YR=Get_Field(COM_YR_4)),
    IF(YR=Get_Field(COM_YR_2),Get_Field(Com_Cost_2),
    IF(YR=Get_Field(COM_YR_3),Get_Field(Com_Cost_3),
    IF(YR=Get_Field(COM_YR_4),Get_Field(Com_Cost_4),Get_Number(0))))
    ,
    Get_Field(Length) * 
    IF(IFDEFAULT(Get_Field(Lanes_Total)),Get_Number(2),Get_Field(Lanes_Total)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','Thin_Overlay' + '_' + '1' +'_' + GET_ANALVR(PMS_tDAV_Pave_Type),TRUE))
    * Get_Exp(PMS_ancCOST_Inflation)
)

```

Original:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) OR YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) OR YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)),
    IF(YR=Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),Get_Field(8122f017-da56-4071-96cc-6c232d8c8911),
    IF(YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(3432d1c0-3be8-411d-b152-cc2ca54734ee),
    IF(YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86),Get_Field(0f501102-10d5-4938-8a1c-f181c66fa722),Get_Number(0))))
    ,
    Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) * 
    IF(IFDEFAULT(Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)),Get_Number(2),Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','Thin_Overlay' + '_' + '1' +'_' + GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2),TRUE))
    * Get_Exp(0aa0db60-e10a-4140-bc34-386cf64c4aee)
)

```

<a id="e-5026ac2d-f5ac-421f-a1fd-edc893c79287"></a>

## PMS_ancCOST_PM_Cape_Seal

Source: `RuntimeExpressions` / `5026ac2d-f5ac-421f-a1fd-edc893c79287`.



Readable:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(COM_YR_2) OR YR=Get_Field(COM_YR_3) OR YR=Get_Field(COM_YR_4)),
    IF(YR=Get_Field(COM_YR_2),Get_Field(Com_Cost_2),
    IF(YR=Get_Field(COM_YR_3),Get_Field(Com_Cost_3),
    IF(YR=Get_Field(COM_YR_4),Get_Field(Com_Cost_4),Get_Number(0))))
    ,
    Get_Field(Length) * 
    IF(IFDEFAULT(Get_Field(Lanes_Total)),Get_Number(2),Get_Field(Lanes_Total)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','PM_Cape_Seal' + '_' + '1' +'_' + GET_ANALVR(PMS_tDAV_Pave_Type),TRUE))
     * Get_Exp(PMS_ancCOST_Inflation)
)

```

Original:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) OR YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) OR YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)),
    IF(YR=Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),Get_Field(8122f017-da56-4071-96cc-6c232d8c8911),
    IF(YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(3432d1c0-3be8-411d-b152-cc2ca54734ee),
    IF(YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86),Get_Field(0f501102-10d5-4938-8a1c-f181c66fa722),Get_Number(0))))
    ,
    Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) * 
    IF(IFDEFAULT(Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)),Get_Number(2),Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','PM_Cape_Seal' + '_' + '1' +'_' + GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2),TRUE))
     * Get_Exp(0aa0db60-e10a-4140-bc34-386cf64c4aee)
)

```

<a id="e-4acfa0b2-0b40-4134-9fcd-21883b8c1c3c"></a>

## PMS_ancCOST_PM_Chip_Seal

Source: `RuntimeExpressions` / `4acfa0b2-0b40-4134-9fcd-21883b8c1c3c`.



Readable:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(COM_YR_2) OR YR=Get_Field(COM_YR_3) OR YR=Get_Field(COM_YR_4)),
    IF(YR=Get_Field(COM_YR_2),Get_Field(Com_Cost_2),
    IF(YR=Get_Field(COM_YR_3),Get_Field(Com_Cost_3),
    IF(YR=Get_Field(COM_YR_4),Get_Field(Com_Cost_4),Get_Number(0))))
    ,
    Get_Field(Length) * 
    IF(IFDEFAULT(Get_Field(Lanes_Total)),Get_Number(2),Get_Field(Lanes_Total)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','PM_Chip_Seal' + '_' + '1' +'_' + GET_ANALVR(PMS_tDAV_Pave_Type),TRUE))
    * Get_Exp(PMS_ancCOST_Inflation)
)

```

Original:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) OR YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) OR YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)),
    IF(YR=Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),Get_Field(8122f017-da56-4071-96cc-6c232d8c8911),
    IF(YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(3432d1c0-3be8-411d-b152-cc2ca54734ee),
    IF(YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86),Get_Field(0f501102-10d5-4938-8a1c-f181c66fa722),Get_Number(0))))
    ,
    Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) * 
    IF(IFDEFAULT(Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)),Get_Number(2),Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','PM_Chip_Seal' + '_' + '1' +'_' + GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2),TRUE))
    * Get_Exp(0aa0db60-e10a-4140-bc34-386cf64c4aee)
)

```

<a id="e-0dd039d8-05fc-41d4-b306-553738a40641"></a>

## PMS_ancCOST_PM_Crack_Seal

Source: `RuntimeExpressions` / `0dd039d8-05fc-41d4-b306-553738a40641`.



Readable:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(COM_YR_2) OR YR=Get_Field(COM_YR_3) OR YR=Get_Field(COM_YR_4)),
    IF(YR=Get_Field(COM_YR_2),Get_Field(Com_Cost_2),
    IF(YR=Get_Field(COM_YR_3),Get_Field(Com_Cost_3),
    IF(YR=Get_Field(COM_YR_4),Get_Field(Com_Cost_4),Get_Number(0))))
    ,
    Get_Field(Length) * 
    IF(IFDEFAULT(Get_Field(Lanes_Total)),Get_Number(2),Get_Field(Lanes_Total)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','PM_Crack_Seal' + '_' + '1' +'_' + GET_ANALVR(PMS_tDAV_Pave_Type),TRUE))
    * Get_Exp(PMS_ancCOST_Inflation)
)

```

Original:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) OR YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) OR YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)),
    IF(YR=Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),Get_Field(8122f017-da56-4071-96cc-6c232d8c8911),
    IF(YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(3432d1c0-3be8-411d-b152-cc2ca54734ee),
    IF(YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86),Get_Field(0f501102-10d5-4938-8a1c-f181c66fa722),Get_Number(0))))
    ,
    Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) * 
    IF(IFDEFAULT(Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)),Get_Number(2),Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','PM_Crack_Seal' + '_' + '1' +'_' + GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2),TRUE))
    * Get_Exp(0aa0db60-e10a-4140-bc34-386cf64c4aee)
)

```

<a id="e-d7e6a0ad-2b0d-4664-91ec-2103413fd043"></a>

## PMS_ancCOST_PM_Microsurfacing

Source: `RuntimeExpressions` / `d7e6a0ad-2b0d-4664-91ec-2103413fd043`.



Readable:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(COM_YR_2) OR YR=Get_Field(COM_YR_3) OR YR=Get_Field(COM_YR_4)),
    IF(YR=Get_Field(COM_YR_2),Get_Field(Com_Cost_2),
    IF(YR=Get_Field(COM_YR_3),Get_Field(Com_Cost_3),
    IF(YR=Get_Field(COM_YR_4),Get_Field(Com_Cost_4),Get_Number(0))))
    ,
    Get_Field(Length) * 
    IF(IFDEFAULT(Get_Field(Lanes_Total)),Get_Number(2),Get_Field(Lanes_Total)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','PM_Micro_Surfacing' + '_' + '1' +'_' + GET_ANALVR(PMS_tDAV_Pave_Type),TRUE))
    * Get_Exp(PMS_ancCOST_Inflation)
)

```

Original:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) OR YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) OR YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)),
    IF(YR=Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),Get_Field(8122f017-da56-4071-96cc-6c232d8c8911),
    IF(YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(3432d1c0-3be8-411d-b152-cc2ca54734ee),
    IF(YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86),Get_Field(0f501102-10d5-4938-8a1c-f181c66fa722),Get_Number(0))))
    ,
    Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) * 
    IF(IFDEFAULT(Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)),Get_Number(2),Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','PM_Micro_Surfacing' + '_' + '1' +'_' + GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2),TRUE))
    * Get_Exp(0aa0db60-e10a-4140-bc34-386cf64c4aee)
)

```

<a id="e-0c1a2284-4759-48ec-8cb3-7a6fd915fc4a"></a>

## PMS_ancCOST_PM_Prreservation

Source: `RuntimeExpressions` / `0c1a2284-4759-48ec-8cb3-7a6fd915fc4a`.



Readable:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(COM_YR_2) OR YR=Get_Field(COM_YR_3) OR YR=Get_Field(COM_YR_4)),
    IF(YR=Get_Field(COM_YR_2),Get_Field(Com_Cost_2),
    IF(YR=Get_Field(COM_YR_3),Get_Field(Com_Cost_3),
    IF(YR=Get_Field(COM_YR_4),Get_Field(Com_Cost_4),Get_Number(0))))
    ,
    Get_Field(Length) * 
    IF(IFDEFAULT(Get_Field(Lanes_Total)),Get_Number(2),Get_Field(Lanes_Total)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','PM_Preservation' + '_' + '1' +'_' + GET_ANALVR(PMS_tDAV_Pave_Type),TRUE))
    * Get_Exp(PMS_ancCOST_Inflation)
)

```

Original:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) OR YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) OR YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)),
    IF(YR=Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),Get_Field(8122f017-da56-4071-96cc-6c232d8c8911),
    IF(YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(3432d1c0-3be8-411d-b152-cc2ca54734ee),
    IF(YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86),Get_Field(0f501102-10d5-4938-8a1c-f181c66fa722),Get_Number(0))))
    ,
    Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) * 
    IF(IFDEFAULT(Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)),Get_Number(2),Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','PM_Preservation' + '_' + '1' +'_' + GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2),TRUE))
    * Get_Exp(0aa0db60-e10a-4140-bc34-386cf64c4aee)
)

```

<a id="e-0faa0748-1d4f-4baa-9f68-449391104e85"></a>

## PMS_ancCOST_PM_Saw_Seal_Joints

Source: `RuntimeExpressions` / `0faa0748-1d4f-4baa-9f68-449391104e85`.



Readable:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(COM_YR_2) OR YR=Get_Field(COM_YR_3) OR YR=Get_Field(COM_YR_4)),
    IF(YR=Get_Field(COM_YR_2),Get_Field(Com_Cost_2),
    IF(YR=Get_Field(COM_YR_3),Get_Field(Com_Cost_3),
    IF(YR=Get_Field(COM_YR_4),Get_Field(Com_Cost_4),Get_Number(0))))
    ,
    Get_Field(Length) * 
    IF(IFDEFAULT(Get_Field(Lanes_Total)),Get_Number(2),Get_Field(Lanes_Total)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','PM_Saw_Seal_Joints' + '_' + '1' +'_' + GET_ANALVR(PMS_tDAV_Pave_Type),TRUE))
    * Get_Exp(PMS_ancCOST_Inflation)
)

```

Original:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) OR YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) OR YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)),
    IF(YR=Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),Get_Field(8122f017-da56-4071-96cc-6c232d8c8911),
    IF(YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(3432d1c0-3be8-411d-b152-cc2ca54734ee),
    IF(YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86),Get_Field(0f501102-10d5-4938-8a1c-f181c66fa722),Get_Number(0))))
    ,
    Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) * 
    IF(IFDEFAULT(Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)),Get_Number(2),Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','PM_Saw_Seal_Joints' + '_' + '1' +'_' + GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2),TRUE))
    * Get_Exp(0aa0db60-e10a-4140-bc34-386cf64c4aee)
)

```

<a id="e-ed5ccc87-740f-4148-b9c1-5f90250f6c6f"></a>

## PMS_ancCOST_PM_Ultra_Thin_Overlay

Source: `RuntimeExpressions` / `ed5ccc87-740f-4148-b9c1-5f90250f6c6f`.



Readable:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(COM_YR_2) OR YR=Get_Field(COM_YR_3) OR YR=Get_Field(COM_YR_4)),
    IF(YR=Get_Field(COM_YR_2),Get_Field(Com_Cost_2),
    IF(YR=Get_Field(COM_YR_3),Get_Field(Com_Cost_3),
    IF(YR=Get_Field(COM_YR_4),Get_Field(Com_Cost_4),Get_Number(0))))
    ,
    Get_Field(Length) * 
    IF(IFDEFAULT(Get_Field(Lanes_Total)),Get_Number(2),Get_Field(Lanes_Total)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','PM_Ultra_Thin_Overlay' + '_' + '1' +'_' + GET_ANALVR(PMS_tDAV_Pave_Type),TRUE))
    * Get_Exp(PMS_ancCOST_Inflation)
)

```

Original:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) OR YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) OR YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)),
    IF(YR=Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),Get_Field(8122f017-da56-4071-96cc-6c232d8c8911),
    IF(YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(3432d1c0-3be8-411d-b152-cc2ca54734ee),
    IF(YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86),Get_Field(0f501102-10d5-4938-8a1c-f181c66fa722),Get_Number(0))))
    ,
    Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) * 
    IF(IFDEFAULT(Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)),Get_Number(2),Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','PM_Ultra_Thin_Overlay' + '_' + '1' +'_' + GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2),TRUE))
    * Get_Exp(0aa0db60-e10a-4140-bc34-386cf64c4aee)
)

```

<a id="e-41eee71c-be07-412d-a666-98123d0648d2"></a>

## PMS_ancCOST_Reconstruction

Source: `RuntimeExpressions` / `41eee71c-be07-412d-a666-98123d0648d2`.



Readable:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(COM_YR_2) OR YR=Get_Field(COM_YR_3) OR YR=Get_Field(COM_YR_4)),
    IF(YR=Get_Field(COM_YR_2),Get_Field(Com_Cost_2),
    IF(YR=Get_Field(COM_YR_3),Get_Field(Com_Cost_3),
    IF(YR=Get_Field(COM_YR_4),Get_Field(Com_Cost_4),Get_Number(0))))
    ,
    Get_Field(Length) * 
    IF(IFDEFAULT(Get_Field(Lanes_Total)),Get_Number(2),Get_Field(Lanes_Total)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','Reconstruction' + '_' + '1' +'_' + GET_ANALVR(PMS_tDAV_Pave_Type),TRUE))
    * Get_Exp(PMS_ancCOST_Inflation)
)

```

Original:
```text
IF(IS_COMMITTED() AND (YR = Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) OR YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) OR YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)),
    IF(YR=Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c),Get_Field(8122f017-da56-4071-96cc-6c232d8c8911),
    IF(YR=Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e),Get_Field(3432d1c0-3be8-411d-b152-cc2ca54734ee),
    IF(YR=Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86),Get_Field(0f501102-10d5-4938-8a1c-f181c66fa722),Get_Number(0))))
    ,
    Get_Field(341dd9ab-1806-43f7-9bb4-018bcb00657c) * 
    IF(IFDEFAULT(Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)),Get_Number(2),Get_Field(a8b9fa2f-4bcc-4e31-9603-a1de6f7b1da5)) * 
    VAL(DAL_DCG_STLOOKUP('Analysis_Lookup_Trt_Costs','Cost_Per_Lane_Mile','KEY','Reconstruction' + '_' + '1' +'_' + GET_ANALVR(aa88ec97-1b2a-4089-813b-3c1c4ca7f4f2),TRUE))
    * Get_Exp(0aa0db60-e10a-4140-bc34-386cf64c4aee)
)

```

<a id="e-76d307ed-3427-462f-a79f-e16a387566dd"></a>

## PMS_ancOBJ_AAV_Yrly_Cost_All

Source: `RuntimeExpressions` / `76d307ed-3427-462f-a79f-e16a387566dd`.



Readable:
```text
GST_COST_F
```

Original:
```text
GST_COST_F
```

<a id="e-453c8a3e-bd87-46f5-8faa-3ac49163c144"></a>

## PMS_ancOBJ_ABS_1

Source: `dTIMSExpressions` / `453c8a3e-bd87-46f5-8faa-3ac49163c144`.



Readable:
```text
Get_Number(1)
```

Original:
```text
Get_Number(1)
```

<a id="e-714e7f1c-45e1-4caf-a4e8-c2a6b556a5ee"></a>

## PMS_ancOBJ_ABS_4

Source: `dTIMSExpressions` / `714e7f1c-45e1-4caf-a4e8-c2a6b556a5ee`.



Readable:
```text
Get_Number(4)
```

Original:
```text
Get_Number(4)
```

<a id="e-93753108-e599-4f24-98a3-c23af811031b"></a>

## PMS_ancOBJ_ABS_4_5

Source: `dTIMSExpressions` / `93753108-e599-4f24-98a3-c23af811031b`.



Readable:
```text
Get_Number(4.5)
```

Original:
```text
Get_Number(4.5)
```

<a id="e-6aa8fc26-24d2-4ddf-bf53-ea80f0bd69ae"></a>

## PMS_ancOBJ_ABS_4_5_CCI

Source: `RuntimeExpressions` / `6aa8fc26-24d2-4ddf-bf53-ea80f0bd69ae`.



Readable:
```text
MAX(Get_Number(4.5), GET_ANALVR(PMS_nAAV_CND_CCI))
```

Original:
```text
MAX(Get_Number(4.5), GET_ANALVR(b17f394f-57fd-4efb-8e0e-787d545e45f5))
```

<a id="e-70de9024-06fd-424d-b31f-63a89bd17f0a"></a>

## PMS_ancOBJ_ABS_4_5_CSI

Source: `RuntimeExpressions` / `70de9024-06fd-424d-b31f-63a89bd17f0a`.



Readable:
```text
MAX(Get_Number(4.5), GET_ANALVR(PMS_nAAV_CND_CSI))
```

Original:
```text
MAX(Get_Number(4.5), GET_ANALVR(52c46a28-963d-4573-b52c-c83bddc90e7d))
```

<a id="e-128fcb68-54cb-47df-a378-5d5c8986e723"></a>

## PMS_ancOBJ_ABS_4_5_ECI

Source: `RuntimeExpressions` / `128fcb68-54cb-47df-a378-5d5c8986e723`.



Readable:
```text
MAX(Get_Number(4.5), GET_ANALVR(PMS_nAAV_CND_ECI))
```

Original:
```text
MAX(Get_Number(4.5), GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8))
```

<a id="e-cdcff07f-7572-4870-b91d-a632deeca3f4"></a>

## PMS_ancOBJ_ABS_4_5_JCI

Source: `RuntimeExpressions` / `cdcff07f-7572-4870-b91d-a632deeca3f4`.



Readable:
```text
MAX(Get_Number(4.5), GET_ANALVR(PMS_nAAV_CND_JCI))
```

Original:
```text
MAX(Get_Number(4.5), GET_ANALVR(64b7d597-74ce-456d-9695-d8d8f9cd1cbb))
```

<a id="e-cf97cde2-65f1-41b2-a110-664314d91e08"></a>

## PMS_ancOBJ_ABS_4_5_PSI

Source: `RuntimeExpressions` / `cf97cde2-65f1-41b2-a110-664314d91e08`.



Readable:
```text
MAX(Get_Number(4.5), GET_ANALVR(PMS_nAAV_CND_PSI))
```

Original:
```text
MAX(Get_Number(4.5), GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44))
```

<a id="e-666c1328-3e75-49b8-9cd6-b669a2378f2f"></a>

## PMS_ancOBJ_ABS_4_5_RDI

Source: `RuntimeExpressions` / `666c1328-3e75-49b8-9cd6-b669a2378f2f`.



Readable:
```text
MAX(Get_Number(4.5), GET_ANALVR(PMS_nAAV_CND_RDI))
```

Original:
```text
MAX(Get_Number(4.5), GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff))
```

<a id="e-d316035d-473e-4fa0-b3ba-d36461157c6b"></a>

## PMS_ancOBJ_ABS_4_5_SCI

Source: `RuntimeExpressions` / `d316035d-473e-4fa0-b3ba-d36461157c6b`.



Readable:
```text
MAX(Get_Number(4.5), GET_ANALVR(PMS_nAAV_CND_SCI))
```

Original:
```text
MAX(Get_Number(4.5), GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673))
```

<a id="e-219ae665-588b-4f92-a506-59c28873d542"></a>

## PMS_ancOBJ_ABS_5

Source: `dTIMSExpressions` / `219ae665-588b-4f92-a506-59c28873d542`.



Readable:
```text
Get_Number(5)
```

Original:
```text
Get_Number(5)
```

<a id="e-0dcb857c-950e-414b-8bc3-c18da79f8883"></a>

## PMS_ancOBJ_ABS_BC

Source: `dTIMSExpressions` / `0dcb857c-950e-414b-8bc3-c18da79f8883`.



Readable:
```text
'BC'
```

Original:
```text
'BC'
```

<a id="e-4b58324a-2cad-4cd7-8036-b410e412ba6c"></a>

## PMS_ancOBJ_ABS_Initial

Source: `dTIMSExpressions` / `4b58324a-2cad-4cd7-8036-b410e412ba6c`.



Readable:
```text
'Initial'
```

Original:
```text
'Initial'
```

<a id="e-f5a30d2f-e3d8-4245-998f-1f9088ccbdc1"></a>

## PMS_ancOBJ_ABS_Major

Source: `dTIMSExpressions` / `f5a30d2f-e3d8-4245-998f-1f9088ccbdc1`.



Readable:
```text
'Major'
```

Original:
```text
'Major'
```

<a id="e-8fa0a363-e9d0-4bc7-8324-822d97acb948"></a>

## PMS_ancOBJ_ABS_Minor

Source: `dTIMSExpressions` / `8fa0a363-e9d0-4bc7-8324-822d97acb948`.



Readable:
```text
'Minor'
```

Original:
```text
'Minor'
```

<a id="e-d89954a1-e259-4680-b157-3d9dad1174b5"></a>

## PMS_ancOBJ_ABS_Minus_1

Source: `dTIMSExpressions` / `d89954a1-e259-4680-b157-3d9dad1174b5`.



Readable:
```text
INT(-Get_Number(1))
```

Original:
```text
INT(-Get_Number(1))
```

<a id="e-06981d4e-9242-40ba-b645-98ea62ed4bb3"></a>

## PMS_ancOBJ_ABS_Zero

Source: `dTIMSExpressions` / `06981d4e-9242-40ba-b645-98ea62ed4bb3`.



Readable:
```text
Get_Number(0)
```

Original:
```text
Get_Number(0)
```

<a id="e-03c7ee64-6d4a-4909-a619-59147534bd6a"></a>

## PMS_ancOBJ_Pave_Area_sq_yds

Source: `dTIMSExpressions` / `03c7ee64-6d4a-4909-a619-59147534bd6a`.



Readable:
```text
(GET_LENGTH(Get_Perspective(Analysis)) * Get_Number(1760)) * (Get_Field(Surf_Wd) / Get_Number(3))
```

Original:
```text
(GET_LENGTH(Get_Perspective(068b15eb-cb1d-4b9c-bf8f-882734ecfc1c)) * Get_Number(1760)) * (Get_Field(cf5fc56b-610b-4438-9053-583b01cc5d4f) / Get_Number(3))
```

<a id="e-09c7fde6-cc65-4701-9ecc-e3e705983d08"></a>

## PMS_ancOBJ_Pave_type_Initial

Source: `dTIMSExpressions` / `09c7fde6-cc65-4701-9ecc-e3e705983d08`.

Initialize the Pavement Type

Readable:
```text
IF(Get_Field(SURF_TYPE_ARAN) ='JCP' OR Get_Field(SURF_TYPE_ARAN)='CRC','RC','BC')
//IF(LEFT(Analysis->Surf_Typ,2.0) = '12','RC',
//IF(LEFT(Analysis->Surf_Typ,2.0) = '11','BC','OT'))
```

Original:
```text
IF(Get_Field(71b500e1-7511-45a9-99d9-63ba6ce36a6f) ='JCP' OR Get_Field(71b500e1-7511-45a9-99d9-63ba6ce36a6f)='CRC','RC','BC')
//IF(LEFT(Analysis->Surf_Typ,2.0) = '12','RC',
//IF(LEFT(Analysis->Surf_Typ,2.0) = '11','BC','OT'))
```

<a id="e-d16f64d2-f26d-4aa8-bb85-3857251e23af"></a>

## PMS_ancPV_Benefit_All

Source: `RuntimeExpressions` / `d16f64d2-f26d-4aa8-bb85-3857251e23af`.



Readable:
```text
GET4CAV_PVDIFF(PMS_nAAV_CND_CCI,0,PMS_nAAV_TRF_ADT,0.2)

```

Original:
```text
GET4CAV_PVDIFF(b17f394f-57fd-4efb-8e0e-787d545e45f5,0,674cee68-8d0f-4f42-8ec1-227bcc6bb6a4,0.2)

```

<a id="e-def28d45-4d9f-4720-b9af-a77db1fc32a8"></a>

## PMS_ancPV_Benefit_All_PSI

Source: `RuntimeExpressions` / `def28d45-4d9f-4720-b9af-a77db1fc32a8`.



Readable:
```text
GET4CAV_PVDIFF(PMS_nAAV_CND_PSI,0,PMS_nAAV_TRF_ADT,0.2)
```

Original:
```text
GET4CAV_PVDIFF(42943fcd-a7b1-425f-aed1-c54c6f59bf44,0,674cee68-8d0f-4f42-8ec1-227bcc6bb6a4,0.2)
```

<a id="e-e79762c9-ae53-4ae1-8051-22c136d9a34f"></a>

## PMS_ancPV_Benefit_Min_Cost

Source: `RuntimeExpressions` / `e79762c9-ae53-4ae1-8051-22c136d9a34f`.



Readable:
```text
IF(IS_DN() OR IS_MO(),Get_Number(0),Get_Number(2000000) - GET_ANALVR(PMS_nCAV_PV_COST))
```

Original:
```text
IF(IS_DN() OR IS_MO(),Get_Number(0),Get_Number(2000000) - GET_ANALVR(e8d463f4-2c24-430d-a55f-83e509dd5ed9))
```

<a id="e-49f25264-5236-46ff-b36a-b7f14616107d"></a>

## PMS_ancPV_Cost

Source: `RuntimeExpressions` / `49f25264-5236-46ff-b36a-b7f14616107d`.



Readable:
```text
GET4CAV_PV(PMS_nAAV_Yrly_Cost)/GET_LENGTH(Get_Perspective(Analysis))
```

Original:
```text
GET4CAV_PV(478feca0-b1fe-4c3e-8e60-3e84fdaee7c2)/GET_LENGTH(Get_Perspective(068b15eb-cb1d-4b9c-bf8f-882734ecfc1c))
```

<a id="e-399a9171-0c43-4440-95ad-64f491cbd646"></a>

## PMS_ancRES_CCI_CAPE_SEAL

Source: `RuntimeExpressions` / `399a9171-0c43-4440-95ad-64f491cbd646`.

Reset CCI for Cape Seal

Readable:
```text
MIN(GET_ANALVR(PMS_nAAV_CND_CCI) + Get_Number(0.25),Get_Number(5))
```

Original:
```text
MIN(GET_ANALVR(b17f394f-57fd-4efb-8e0e-787d545e45f5) + Get_Number(0.25),Get_Number(5))
```

<a id="e-acb4e2c4-97bf-4f5e-9b94-908560724028"></a>

## PMS_ancRES_CCI_CHIP_SEAL

Source: `RuntimeExpressions` / `acb4e2c4-97bf-4f5e-9b94-908560724028`.

Reset CCI for Chip Seal

Readable:
```text
MIN(GET_ANALVR(PMS_nAAV_CND_CCI) + Get_Number(0.5),Get_Number(5))
```

Original:
```text
MIN(GET_ANALVR(b17f394f-57fd-4efb-8e0e-787d545e45f5) + Get_Number(0.5),Get_Number(5))
```

<a id="e-0db279f4-1eaf-41c8-9a50-5be54360cfed"></a>

## PMS_ancRES_CCI_MICROSURFACE

Source: `RuntimeExpressions` / `0db279f4-1eaf-41c8-9a50-5be54360cfed`.

Reset CCI for Micro-Surface

Readable:
```text
MIN(GET_ANALVR(PMS_nAAV_CND_CCI) + Get_Number(0.75),Get_Number(5))
```

Original:
```text
MIN(GET_ANALVR(b17f394f-57fd-4efb-8e0e-787d545e45f5) + Get_Number(0.75),Get_Number(5))
```

<a id="e-c82e6892-be0e-48bf-a02b-e73e7029cbff"></a>

## PMS_ancRES_CCI_SAW_and_SEAL

Source: `RuntimeExpressions` / `c82e6892-be0e-48bf-a02b-e73e7029cbff`.

Reset CCI for Cape Seal

Readable:
```text
MIN(GET_ANALVR(PMS_nAAV_CND_CCI) + Get_Number(1),Get_Number(5))
```

Original:
```text
MIN(GET_ANALVR(b17f394f-57fd-4efb-8e0e-787d545e45f5) + Get_Number(1),Get_Number(5))
```

<a id="e-bf3aed6d-d0f5-4275-9a95-a7b9b5520e68"></a>

## PMS_ancRES_CCI_THIN_OVERLAY

Source: `RuntimeExpressions` / `bf3aed6d-d0f5-4275-9a95-a7b9b5520e68`.

Reset CCI for Thin Overlay

Readable:
```text
MIN(GET_ANALVR(PMS_nAAV_CND_CCI) + Get_Number(1.25),Get_Number(5))
```

Original:
```text
MIN(GET_ANALVR(b17f394f-57fd-4efb-8e0e-787d545e45f5) + Get_Number(1.25),Get_Number(5))
```

<a id="e-2709c4c3-b9ba-4e73-a1bc-0e02c260d0af"></a>

## PMS_ancRES_CCI_ULTRA_THIN

Source: `RuntimeExpressions` / `2709c4c3-b9ba-4e73-a1bc-0e02c260d0af`.

Reset CCI for Ultra Thin

Readable:
```text
MIN(GET_ANALVR(PMS_nAAV_CND_CCI) + Get_Number(1),Get_Number(5))
```

Original:
```text
MIN(GET_ANALVR(b17f394f-57fd-4efb-8e0e-787d545e45f5) + Get_Number(1),Get_Number(5))
```

<a id="e-455714c1-bc1f-4743-a66e-1e1d92bee2cc"></a>

## PMS_ancRES_CNT_CHIP_SEAL

Source: `RuntimeExpressions` / `455714c1-bc1f-4743-a66e-1e1d92bee2cc`.

Reset Chip Seal Count following a Chip Seal

Readable:
```text
GET_ANALVR(PMS_nDAV_CNT_CHIP_SEALS) + Get_Number(1)
```

Original:
```text
GET_ANALVR(7014cb8f-5c5e-4f86-a714-76ec0a7d79a1) + Get_Number(1)
```

<a id="e-870fadb0-cdad-49eb-829f-599710b454e3"></a>

## PMS_ancRES_CNT_MICROSURFACE

Source: `RuntimeExpressions` / `870fadb0-cdad-49eb-829f-599710b454e3`.

Count of Consecutive Microsurfaces

Readable:
```text
GET_ANALVR(PMS_nDAV_CNT_MICROSURFACE) + Get_Number(1)
```

Original:
```text
GET_ANALVR(1e9fd63b-174d-4d69-8033-e23c4fd3340b) + Get_Number(1)
```

<a id="e-d6cb9764-7364-4260-9f45-a7ccc543062b"></a>

## PMS_ancRES_ECI_CAPE_SEAL

Source: `RuntimeExpressions` / `d6cb9764-7364-4260-9f45-a7ccc543062b`.

Reset ECI for Cape Seal

Readable:
```text
MIN(GET_ANALVR(PMS_nAAV_CND_ECI) + Get_Number(0.25),Get_Number(5))
```

Original:
```text
MIN(GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) + Get_Number(0.25),Get_Number(5))
```

<a id="e-fa36e4d4-2f5d-4372-b223-f083929bb4b0"></a>

## PMS_ancRES_ECI_CHIP_SEAL

Source: `RuntimeExpressions` / `fa36e4d4-2f5d-4372-b223-f083929bb4b0`.

Reset ECI for Chip Seal

Readable:
```text
MIN(GET_ANALVR(PMS_nAAV_CND_ECI) + Get_Number(0.5),Get_Number(5))
```

Original:
```text
MIN(GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) + Get_Number(0.5),Get_Number(5))
```

<a id="e-e87af607-69b3-4c46-96e2-5a91a4f471d0"></a>

## PMS_ancRES_ECI_MICROSURFACE

Source: `RuntimeExpressions` / `e87af607-69b3-4c46-96e2-5a91a4f471d0`.

Reset ECI for Micro-Surface

Readable:
```text
MIN(GET_ANALVR(PMS_nAAV_CND_ECI) + Get_Number(0.75),Get_Number(5))
```

Original:
```text
MIN(GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) + Get_Number(0.75),Get_Number(5))
```

<a id="e-384514d5-5dee-4e86-a5c7-6bb5b3dd4a71"></a>

## PMS_ancRES_ECI_THIN_OVERLAY

Source: `RuntimeExpressions` / `384514d5-5dee-4e86-a5c7-6bb5b3dd4a71`.

Reset ECI for Thin Overlay

Readable:
```text
MIN(GET_ANALVR(PMS_nAAV_CND_ECI) + Get_Number(1.25),Get_Number(5))
```

Original:
```text
MIN(GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) + Get_Number(1.25),Get_Number(5))
```

<a id="e-354afb8c-179e-44cf-a7cd-0009306fe1e9"></a>

## PMS_ancRES_ECI_ULTRA_THIN

Source: `RuntimeExpressions` / `354afb8c-179e-44cf-a7cd-0009306fe1e9`.

Reset ECI for Ultra Thin

Readable:
```text
MIN(GET_ANALVR(PMS_nAAV_CND_ECI) + Get_Number(1),Get_Number(5))
```

Original:
```text
MIN(GET_ANALVR(1fe36102-5f0a-41e4-9dcc-748a3dbe57a8) + Get_Number(1),Get_Number(5))
```

<a id="e-1d4efdbd-03bf-4bc2-b189-da59dab901ae"></a>

## PMS_ancRES_IRI

Source: `RuntimeExpressions` / `1d4efdbd-03bf-4bc2-b189-da59dab901ae`.

Reset IRI following a treatment

Readable:
```text
MIN(IF(GET_ANALVR(PMS_nAAV_CND_PSI) > Get_Number(0),
    MIN(Get_Number(65)+(LOG(GET_ANALVR(PMS_nAAV_CND_PSI)/Get_Number(5))/-Get_Number(0.0066)),Get_Number(500)),
    Get_Number(500)
    )
    ,
    GET_ANALVR(PMS_nAAV_CND_IRI)
    )
```

Original:
```text
MIN(IF(GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) > Get_Number(0),
    MIN(Get_Number(65)+(LOG(GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44)/Get_Number(5))/-Get_Number(0.0066)),Get_Number(500)),
    Get_Number(500)
    )
    ,
    GET_ANALVR(3ae48bd7-f227-491a-88ba-510a2e180f5d)
    )
```

<a id="e-0a1d81b8-b54b-490f-9238-9e8cc47b9f96"></a>

## PMS_ancRES_PCRK

Source: `RuntimeExpressions` / `0a1d81b8-b54b-490f-9238-9e8cc47b9f96`.



Readable:
```text
MIN(IF(Get_Exp(PMS_abfOBJ_Asphalt),
    IF(Get_Field(Sign) = '1',
        Get_Number(0.15) * Get_Exp(PMS_ancAGE_AGE_SCI),
    IF(Get_Field(Sign)<>'1' and Get_Field(HPMS) ='1',
        Get_Number(0.37) * Get_Exp(PMS_ancAGE_AGE_SCI),
        Get_Number(0.56) * Get_Exp(PMS_ancAGE_AGE_SCI))
       )
    ,
    IF(Get_Field(Sign) = '1',
        Get_Number(0.15) * Get_Exp(PMS_ancAGE_AGE_CCI),
    IF(Get_Field(Sign)<>'1' and Get_Field(HPMS) ='1',
        Get_Number(0.37) * Get_Exp(PMS_ancAGE_AGE_CCI),
        Get_Number(0.56) * Get_Exp(PMS_ancAGE_AGE_CCI))
    )
    )
,
    GET_ANALVR(PMS_nAAV_CND_PCRK)
)
```

Original:
```text
MIN(IF(Get_Exp(915f80f1-74d8-48c0-ab9f-fdffd05d547a),
    IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) = '1',
        Get_Number(0.15) * Get_Exp(70e13ebd-e481-49a1-ac3d-1290864cde14),
    IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)<>'1' and Get_Field(7da5a5a8-cf02-45c1-bea8-97599fc41064) ='1',
        Get_Number(0.37) * Get_Exp(70e13ebd-e481-49a1-ac3d-1290864cde14),
        Get_Number(0.56) * Get_Exp(70e13ebd-e481-49a1-ac3d-1290864cde14))
       )
    ,
    IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c) = '1',
        Get_Number(0.15) * Get_Exp(52fb3718-9639-4250-b7f5-63c1eb51435c),
    IF(Get_Field(68ed04d3-e37e-47c8-9610-e9889a47647c)<>'1' and Get_Field(7da5a5a8-cf02-45c1-bea8-97599fc41064) ='1',
        Get_Number(0.37) * Get_Exp(52fb3718-9639-4250-b7f5-63c1eb51435c),
        Get_Number(0.56) * Get_Exp(52fb3718-9639-4250-b7f5-63c1eb51435c))
    )
    )
,
    GET_ANALVR(af5bdd9f-eefc-48c3-bd24-ffd829d416fb)
)
```

<a id="e-b0ed3473-2081-4c83-926d-0440557ed1b1"></a>

## PMS_ancRES_PSI_MICROSURFACE

Source: `RuntimeExpressions` / `b0ed3473-2081-4c83-926d-0440557ed1b1`.

Reset PSI for Microsurface

Readable:
```text
MIN(GET_ANALVR(PMS_nAAV_CND_PSI) + Get_Number(0.75),Get_Number(5))
```

Original:
```text
MIN(GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) + Get_Number(0.75),Get_Number(5))
```

<a id="e-3c2ad86c-8882-44b2-947a-aa1cd954f678"></a>

## PMS_ancRES_PSI_THIN_OVERLAY

Source: `RuntimeExpressions` / `3c2ad86c-8882-44b2-947a-aa1cd954f678`.

Reset PSI for Thin Overlay

Readable:
```text
MIN(GET_ANALVR(PMS_nAAV_CND_PSI) + Get_Number(1.25),Get_Number(5))
```

Original:
```text
MIN(GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) + Get_Number(1.25),Get_Number(5))
```

<a id="e-391639e4-c03a-4e75-bf5d-7df493d8dc58"></a>

## PMS_ancRES_PSI_ULTRA_THIN

Source: `RuntimeExpressions` / `391639e4-c03a-4e75-bf5d-7df493d8dc58`.

Reset PSI for Ultra Thin 

Readable:
```text
MIN(GET_ANALVR(PMS_nAAV_CND_PSI) + Get_Number(1),Get_Number(5))
```

Original:
```text
MIN(GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) + Get_Number(1),Get_Number(5))
```

<a id="e-9d879d4e-9d1d-4f51-8cec-2c9e391319a4"></a>

## PMS_ancRES_RDI_MICROSURFACE

Source: `RuntimeExpressions` / `9d879d4e-9d1d-4f51-8cec-2c9e391319a4`.

Reset RDI for Microsurface

Readable:
```text
MIN(GET_ANALVR(PMS_nAAV_CND_RDI) + Get_Number(0.75),Get_Number(5))
```

Original:
```text
MIN(GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) + Get_Number(0.75),Get_Number(5))
```

<a id="e-4324d58a-d04d-4508-9ad6-ddadbbe810cf"></a>

## PMS_ancRES_RDI_THIN_OVERLAY

Source: `RuntimeExpressions` / `4324d58a-d04d-4508-9ad6-ddadbbe810cf`.

Reset RDI for Thin Overlay

Readable:
```text
MIN(GET_ANALVR(PMS_nAAV_CND_RDI) + Get_Number(1.25),Get_Number(5))
```

Original:
```text
MIN(GET_ANALVR(1c8052d3-a00c-4ee0-92c2-62b48f14baff) + Get_Number(1.25),Get_Number(5))
```

<a id="e-da41ad22-f67a-47d1-9cdc-60e38ccf55a9"></a>

## PMS_ancRES_RDI_ULTRA_THIN

Source: `RuntimeExpressions` / `da41ad22-f67a-47d1-9cdc-60e38ccf55a9`.



Readable:
```text
MIN(GET_ANALVR(PMS_nAAV_CND_PSI) + Get_Number(1),Get_Number(5))
```

Original:
```text
MIN(GET_ANALVR(42943fcd-a7b1-425f-aed1-c54c6f59bf44) + Get_Number(1),Get_Number(5))
```

<a id="e-91a5cbc0-4225-4276-b716-5cde0295c79e"></a>

## PMS_ancRES_SCI_CAPE_SEAL

Source: `RuntimeExpressions` / `91a5cbc0-4225-4276-b716-5cde0295c79e`.

Reset SCI for Cape Seal

Readable:
```text
MIN(GET_ANALVR(PMS_nAAV_CND_SCI) + Get_Number(0.25),Get_Number(5))
```

Original:
```text
MIN(GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) + Get_Number(0.25),Get_Number(5))
```

<a id="e-22a19aac-e4c6-40e0-849a-afc86dc092fc"></a>

## PMS_ancRES_SCI_CHIP_SEAL

Source: `RuntimeExpressions` / `22a19aac-e4c6-40e0-849a-afc86dc092fc`.

Reset SCI for Chip Seal

Readable:
```text
MIN(GET_ANALVR(PMS_nAAV_CND_SCI) + Get_Number(0.5),Get_Number(5))
```

Original:
```text
MIN(GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) + Get_Number(0.5),Get_Number(5))
```

<a id="e-2eeb79c4-579f-44e3-8bdc-3ea05f4369b5"></a>

## PMS_ancRES_SCI_MICROSURFACE

Source: `RuntimeExpressions` / `2eeb79c4-579f-44e3-8bdc-3ea05f4369b5`.

Reset SCI for Micro-surface

Readable:
```text
MIN(GET_ANALVR(PMS_nAAV_CND_SCI) + Get_Number(0.75),Get_Number(5))
```

Original:
```text
MIN(GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) + Get_Number(0.75),Get_Number(5))
```

<a id="e-dbe9ae0c-cedb-480d-b047-f7941dbc4e62"></a>

## PMS_ancRES_SCI_THIN_OVERLAY

Source: `RuntimeExpressions` / `dbe9ae0c-cedb-480d-b047-f7941dbc4e62`.

Reset SCI for Thin Overlay

Readable:
```text
MIN(GET_ANALVR(PMS_nAAV_CND_SCI) + Get_Number(1.25),Get_Number(5))
```

Original:
```text
MIN(GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) + Get_Number(1.25),Get_Number(5))
```

<a id="e-000dd3e3-7e0f-42f1-870e-d8ef825b70a4"></a>

## PMS_ancRES_SCI_ULTRA_THIN

Source: `RuntimeExpressions` / `000dd3e3-7e0f-42f1-870e-d8ef825b70a4`.

Reset SCI for Ultra Thin

Readable:
```text
MIN(GET_ANALVR(PMS_nAAV_CND_SCI) + Get_Number(1),Get_Number(5))
```

Original:
```text
MIN(GET_ANALVR(ee3c6523-7a74-4ecc-a9ad-b6e016071673) + Get_Number(1),Get_Number(5))
```

<a id="e-ed2f1535-a24f-4156-8dbe-8b5e7dda5f7b"></a>

## PMS_ancRES_Yearly_Treatment

Source: `RuntimeExpressions` / `ed2f1535-a24f-4156-8dbe-8b5e7dda5f7b`.

Reset the Yearly Treatment Variable

Readable:
```text
GET_LASTMAJTRT()
```

Original:
```text
GET_LASTMAJTRT()
```

<a id="e-bdc90f36-8bfb-4a9b-bef3-1ae1613029d7"></a>

## PMS_ancTRF_ADT

Source: `RuntimeExpressions` / `bdc90f36-8bfb-4a9b-bef3-1ae1613029d7`.



Readable:
```text
GET_ANALVR(PMS_nAAV_TRF_ADT) * ( Get_Number(1) + Get_Field(ADT_20_Yr_Factor)/Get_Number(100))
```

Original:
```text
GET_ANALVR(674cee68-8d0f-4f42-8ec1-227bcc6bb6a4) * ( Get_Number(1) + Get_Field(1b880838-6c85-436b-98cc-c91b317e5c16)/Get_Number(100))
```

<a id="e-0a9b6cd0-79b4-4da2-a728-ab165b8fe547"></a>

## PMS_ancTRF_Truck_Load

Source: `dTIMSExpressions` / `0a9b6cd0-79b4-4da2-a728-ab165b8fe547`.



Readable:
```text
IF(IFDEFAULT(Get_Field(Coal_Rte_Id)),'L','H')
//IF(ISEMPTY(Analysis->Coal_Rte_Id),IF(nAAV_ESAL < 10000000.0,'L','H'),'H')
```

Original:
```text
IF(IFDEFAULT(Get_Field(3a5f9259-5c3b-4c4d-8894-2bdfcc5b105b)),'L','H')
//IF(ISEMPTY(Analysis->Coal_Rte_Id),IF(nAAV_ESAL < 10000000.0,'L','H'),'H')
```

<a id="e-108538e3-484e-42e5-bb48-e76b7b756d9a"></a>

## PMS_ancTRF_Truck_Load_Initial

Source: `dTIMSExpressions` / `108538e3-484e-42e5-bb48-e76b7b756d9a`.



Readable:
```text
IF(NOT   IFDEFAULT(Get_Field(Coal_Rte_Id)),'H','L')
//IF(ISEMPTY(Analysis->Coal_Rte_Id),IF(Analysis->ESALs < 10000000.0,'L','H'),'H')
```

Original:
```text
IF(NOT   IFDEFAULT(Get_Field(3a5f9259-5c3b-4c4d-8894-2bdfcc5b105b)),'H','L')
//IF(ISEMPTY(Analysis->Coal_Rte_Id),IF(Analysis->ESALs < 10000000.0,'L','H'),'H')
```

<a id="e-1b43e0c5-22b1-4e86-963c-377af181892f"></a>

## PMS_dFRAG_Direction

Source: `dTIMSExpressions` / `1b43e0c5-22b1-4e86-963c-377af181892f`.



Readable:
```text
VAL(GET_FROMADD(Get_Perspective(Base)))
```

Original:
```text
VAL(GET_FROMADD(Get_Perspective(9fca3362-b670-4590-9960-0e511aed59c4)))
```

<a id="e-b27bd60a-10d6-4f0a-9499-c219755c9ad4"></a>

## PMS_dFRAG_FILTER

Source: `dTIMSExpressions` / `b27bd60a-10d6-4f0a-9499-c219755c9ad4`.

dFRAG Filter

Readable:
```text
Get_Field(Name) <> 'ZROAD' AND Get_Field(Name) <> 'new64' 
```

Original:
```text
Get_Field(8bb1e67c-c8e7-453a-bdc5-ed14912d0594) <> 'ZROAD' AND Get_Field(8bb1e67c-c8e7-453a-bdc5-ed14912d0594) <> 'new64' 
```

<a id="e-14d4c279-7a5e-4792-9e9d-35be701b0112"></a>

## PMS_dFRAG_Route_as_Root

Source: `dTIMSExpressions` / `14d4c279-7a5e-4792-9e9d-35be701b0112`.



Readable:
```text
GET_ELEMENTID(Get_Perspective(Base))
```

Original:
```text
GET_ELEMENTID(Get_Perspective(9fca3362-b670-4590-9960-0e511aed59c4))
```

<a id="e-d6c280b9-08b6-4412-8c88-1bd9308fd46f"></a>

## Pavement_Lanes_Length

Source: `dTIMSExpressions` / `d6c280b9-08b6-4412-8c88-1bd9308fd46f`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(e1c06351-9be6-4d02-a492-daac5baa6236) - Get_Field(a30eefc6-658a-4f42-b992-eaf03cc12742)
```

<a id="e-d9a9f566-e0e8-450f-9dae-cd5988571def"></a>

## RI_GIS_AADT_Length

Source: `dTIMSExpressions` / `d9a9f566-e0e8-450f-9dae-cd5988571def`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(7771306f-b3c8-4557-a851-802704bfbe07) - Get_Field(414db9a1-6582-42ac-9f5c-8648e8ee5636)
```

<a id="e-48053d78-2406-407c-a849-961bc44a26ec"></a>

## RI_GIS_ACCESS_CONTROL_Length

Source: `dTIMSExpressions` / `48053d78-2406-407c-a849-961bc44a26ec`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(de2aac9e-5e4b-49ef-bc45-1928b374dbf8) - Get_Field(c8fd1442-f1e6-456d-aebc-474b969ce041)
```

<a id="e-faa52a14-17a3-4593-bedb-95a6ec94b0da"></a>

## RI_GIS_COUNTY_Length

Source: `dTIMSExpressions` / `faa52a14-17a3-4593-bedb-95a6ec94b0da`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(c32d4dff-a9bc-48e8-8437-89574578c007) - Get_Field(84974615-01db-4e3b-907a-4556fd801ae3)
```

<a id="e-a838b1bb-aa89-4aa6-97c4-240b6864c7ae"></a>

## RI_GIS_CRTS_Length

Source: `dTIMSExpressions` / `a838b1bb-aa89-4aa6-97c4-240b6864c7ae`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(a775b0fe-e8c6-45e1-afb3-0da06dc78782) - Get_Field(8f1ccbf0-de76-4571-88bb-2ea1614afb57)
```

<a id="e-ff880aa8-b7dd-40b0-ba46-b78537b4317d"></a>

## RI_GIS_DISTRICT_Length

Source: `dTIMSExpressions` / `ff880aa8-b7dd-40b0-ba46-b78537b4317d`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(0e399b3e-8cd6-44a7-8753-489856449cb2) - Get_Field(45f110f1-a269-4f7a-921d-363a2c113ae2)
```

<a id="e-ee7dca5b-54c9-4180-9bd2-bb91ed85ac61"></a>

## RI_GIS_FACILITY_Length

Source: `dTIMSExpressions` / `ee7dca5b-54c9-4180-9bd2-bb91ed85ac61`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(e26099e2-1cfc-4fe9-952d-1193d71a5c09) - Get_Field(a3c71ef8-78e8-405b-ba9b-931dd47464f3)
```

<a id="e-a3b55fe2-c69e-43ee-905e-7c34c9daeb48"></a>

## RI_GIS_FED_AID_Length

Source: `dTIMSExpressions` / `a3b55fe2-c69e-43ee-905e-7c34c9daeb48`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(955d047f-f260-490f-a14e-2d9a29b737d0) - Get_Field(a8bdf418-676c-4e6f-b356-fbdd59812abc)
```

<a id="e-fe5e66f7-8e34-4119-9816-89a2763cfff6"></a>

## RI_GIS_FED_FOREST_Length

Source: `dTIMSExpressions` / `fe5e66f7-8e34-4119-9816-89a2763cfff6`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(dda3c855-ced4-4672-a8bc-c03ecef573ce) - Get_Field(cb3c3540-d4ec-4733-8d6c-cb69f7d193a6)
```

<a id="e-c4086b2f-1ae1-4afb-bfc4-22fbce0f94c1"></a>

## RI_GIS_FUNC_CLASS_Length

Source: `dTIMSExpressions` / `c4086b2f-1ae1-4afb-bfc4-22fbce0f94c1`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(a2d19c72-15e6-4204-96b9-abf4f460845a) - Get_Field(c8687a83-4a35-4c54-baf7-bfb20e57bf5f)
```

<a id="e-17201d93-29bb-47b4-a5f6-a9c4a8272fc8"></a>

## RI_GIS_GRADE_WIDTH_Length

Source: `dTIMSExpressions` / `17201d93-29bb-47b4-a5f6-a9c4a8272fc8`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(a1b8b0ae-267e-4514-b282-426b8bedda8e) - Get_Field(0c500229-dbf1-446d-b81b-795d07a654c3)
```

<a id="e-445d0699-6708-4d3c-af8e-7ee06da59734"></a>

## RI_GIS_HPMS_Length

Source: `dTIMSExpressions` / `445d0699-6708-4d3c-af8e-7ee06da59734`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(aafef273-ae26-4bea-80a6-2fd643ab905c) - Get_Field(3091737a-6434-4701-ae0f-86503a4e0984)
```

<a id="e-a81c5051-e690-4d3b-becc-3413ba8d3e84"></a>

## RI_GIS_LANES_Length

Source: `dTIMSExpressions` / `a81c5051-e690-4d3b-becc-3413ba8d3e84`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(69a256a1-b4fb-40de-9582-87f888b788e1) - Get_Field(f7f3fafa-78e5-4741-8992-ee18bd27f694)
```

<a id="e-b9c8c027-87be-4758-8726-86855b63aee1"></a>

## RI_GIS_MEDIAN_Length

Source: `dTIMSExpressions` / `b9c8c027-87be-4758-8726-86855b63aee1`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(db9ad42f-efef-494a-8880-0872dbb4bb32) - Get_Field(b78659a8-ff84-4af6-9ddd-bfd94b6b97e7)
```

<a id="e-03989bb8-1bba-41bc-ae7f-9582e2f833b6"></a>

## RI_GIS_NHS_Length

Source: `dTIMSExpressions` / `03989bb8-1bba-41bc-ae7f-9582e2f833b6`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(d3f2ec8a-9ee4-4ad0-af06-8655987651e7) - Get_Field(860bb689-cfb2-4f97-be22-f06c4898c68b)
```

<a id="e-eb36a57a-dbd8-45ca-a9c6-ae5c2556d83a"></a>

## RI_GIS_OWNERSHIP_Length

Source: `dTIMSExpressions` / `eb36a57a-dbd8-45ca-a9c6-ae5c2556d83a`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(13ddd45f-5d5f-406f-8b81-58f918d81ad6) - Get_Field(66d6683d-5d1f-4219-9faa-b7323c44fe0c)
```

<a id="e-2271b5a7-dbbd-4fd3-ac84-21b20cece25c"></a>

## RI_GIS_PEAK_LANES_Length

Source: `dTIMSExpressions` / `2271b5a7-dbbd-4fd3-ac84-21b20cece25c`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(afaf191b-ac06-448a-b704-e56c8745ccfa) - Get_Field(b4f0d83b-6fcf-4183-ad09-f9d4e9a788c3)
```

<a id="e-0432bbad-2a8b-4007-b085-2631ea06055b"></a>

## RI_GIS_SPECIAL_SYSTEM_Length

Source: `dTIMSExpressions` / `0432bbad-2a8b-4007-b085-2631ea06055b`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(81935e02-4ecc-4305-921a-c2c1a2e55a1e) - Get_Field(a623f565-30b7-4088-8d93-0a5007e10031)
```

<a id="e-e771ae6e-66bc-4756-9cfb-3fa7b0b59044"></a>

## RI_GIS_SURF_TYPE_Length

Source: `dTIMSExpressions` / `e771ae6e-66bc-4756-9cfb-3fa7b0b59044`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(fdbd2c43-7300-4c2c-ae16-1ba0b327557d) - Get_Field(0d9398ff-01b9-411f-98d7-6bff0de4ae07)
```

<a id="e-3dafdd5f-5585-42b8-ab48-be9ae6b5a89a"></a>

## RI_GIS_SURF_WID_Length

Source: `dTIMSExpressions` / `3dafdd5f-5585-42b8-ab48-be9ae6b5a89a`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(a21d23f2-dbcd-4f81-91e2-54951582c1d8) - Get_Field(8564ab5e-d207-47c7-9681-6c92beb545b5)
```

<a id="e-3beac598-d587-447b-afd4-a25a69f1e02e"></a>

## RI_GIS_TRAFFIC_Length

Source: `dTIMSExpressions` / `3beac598-d587-447b-afd4-a25a69f1e02e`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(f7eb3fd9-b1ba-47a6-9366-aa76e7e45fd1) - Get_Field(8321e158-c967-4559-b7bb-7fc2191c28a2)
```

<a id="e-89609efa-3f2b-42b4-81d1-688b8508235a"></a>

## RI_GIS_TRUCK_ROUTE_Length

Source: `dTIMSExpressions` / `89609efa-3f2b-42b4-81d1-688b8508235a`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(2d9a4c7a-1b0c-4075-8632-4eabbf4bf4ce) - Get_Field(ec23165c-110c-4a7a-aec5-f2c199c4015e)
```

<a id="e-c0d757d7-3503-4b6a-a8c9-75dfa4d285de"></a>

## RI_GIS_URBAN_CODE_Length

Source: `dTIMSExpressions` / `c0d757d7-3503-4b6a-a8c9-75dfa4d285de`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(1358ad66-2e62-4e76-aedf-c71707141bfe) - Get_Field(808ca311-a9fe-4110-85b5-cecd37004da2)
```

<a id="e-31cf6239-5d18-4ae7-a47d-418f2f47c49b"></a>

## RI_GIS_URBAN_Length

Source: `dTIMSExpressions` / `31cf6239-5d18-4ae7-a47d-418f2f47c49b`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(c4e533d6-0bd1-4519-bbbf-6cc1a7a428a7) - Get_Field(734d13d3-e641-4013-81cc-7fdced9e2af6)
```

<a id="e-0d284ae3-a28c-4154-8fc7-9c3d4b20c3a5"></a>

## RI_GIS_WV_FUNC_CLASS_Length

Source: `dTIMSExpressions` / `0d284ae3-a28c-4154-8fc7-9c3d4b20c3a5`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(cf1be2f2-4b58-4cd5-952a-4b4ade209840) - Get_Field(8f3f1da9-3fe3-4c0e-992f-b0a1ecebf882)
```

<a id="e-1c567494-c61f-4e09-aa07-54895ba9b8bd"></a>

## RI_GIS_YEAR_IMPROVED_Length

Source: `dTIMSExpressions` / `1c567494-c61f-4e09-aa07-54895ba9b8bd`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(0cc394b1-c04b-43da-a6c1-1619da64193a) - Get_Field(aed5f0ee-7f4d-4d64-b041-1fcb7281035b)
```

<a id="e-09dc7644-0b0a-4858-902c-e8b8762ebeb7"></a>

## Rehab_History_1998

Source: `dTIMSExpressions` / `09dc7644-0b0a-4858-902c-e8b8762ebeb7`.

Rehab records up to 1998

Readable:
```text
Get_Field(COMPLETION_YEAR) < Get_Number(1998)
```

Original:
```text
Get_Field(46679c8f-0648-4f1f-84d2-a961553a38a8) < Get_Number(1998)
```

<a id="e-0653837a-2c67-4709-b6cb-afc63a718cae"></a>

## Rehab_History_2000

Source: `dTIMSExpressions` / `0653837a-2c67-4709-b6cb-afc63a718cae`.

Rehab records up to 2000

Readable:
```text
Get_Field(COMPLETION_YEAR) < Get_Number(2000)
```

Original:
```text
Get_Field(46679c8f-0648-4f1f-84d2-a961553a38a8) < Get_Number(2000)
```

<a id="e-c3f733da-2d52-413f-81bf-8c0d74659200"></a>

## Rehab_History_2002

Source: `dTIMSExpressions` / `c3f733da-2d52-413f-81bf-8c0d74659200`.

Rehab records up to 2002

Readable:
```text
Get_Field(COMPLETION_YEAR) < Get_Number(2002)
```

Original:
```text
Get_Field(46679c8f-0648-4f1f-84d2-a961553a38a8) < Get_Number(2002)
```

<a id="e-f77a4927-3a48-4155-8674-58c3999d9154"></a>

## Rehab_History_2004

Source: `dTIMSExpressions` / `f77a4927-3a48-4155-8674-58c3999d9154`.

Rehab records up to 2004

Readable:
```text
Get_Field(COMPLETION_YEAR) < Get_Number(2004)
```

Original:
```text
Get_Field(46679c8f-0648-4f1f-84d2-a961553a38a8) < Get_Number(2004)
```

<a id="e-355d722a-0f0b-47e0-bb59-ac48b8e4f816"></a>

## Rehab_History_2006

Source: `dTIMSExpressions` / `355d722a-0f0b-47e0-bb59-ac48b8e4f816`.

Rehab records up to 2006

Readable:
```text
Get_Field(COMPLETION_YEAR) < Get_Number(2006)
```

Original:
```text
Get_Field(46679c8f-0648-4f1f-84d2-a961553a38a8) < Get_Number(2006)
```

<a id="e-179aa7d1-21aa-4c83-a91c-e963753c3270"></a>

## Rehab_History_2008

Source: `dTIMSExpressions` / `179aa7d1-21aa-4c83-a91c-e963753c3270`.

Rehab records up to 2008

Readable:
```text
Get_Field(COMPLETION_YEAR) < Get_Number(2008)
```

Original:
```text
Get_Field(46679c8f-0648-4f1f-84d2-a961553a38a8) < Get_Number(2008)
```

<a id="e-401e4f75-a165-4135-be37-b33cc32ef0f2"></a>

## Rehab_History_2010

Source: `dTIMSExpressions` / `401e4f75-a165-4135-be37-b33cc32ef0f2`.

Rehab records up to 2010

Readable:
```text
Get_Field(COMPLETION_YEAR) < Get_Number(2010)
```

Original:
```text
Get_Field(46679c8f-0648-4f1f-84d2-a961553a38a8) < Get_Number(2010)
```

<a id="e-1c2916dd-26b3-4797-838d-72cf07388357"></a>

## Rehab_History_2011

Source: `dTIMSExpressions` / `1c2916dd-26b3-4797-838d-72cf07388357`.

Rehab records up to 2011

Readable:
```text
Get_Field(COMPLETION_YEAR) < Get_Number(2011)
```

Original:
```text
Get_Field(46679c8f-0648-4f1f-84d2-a961553a38a8) < Get_Number(2011)
```

<a id="e-7097c9a2-6e71-44d7-b5a2-13a2dae342e7"></a>

## Rehab_History_2012

Source: `dTIMSExpressions` / `7097c9a2-6e71-44d7-b5a2-13a2dae342e7`.

Rehab records up to 2012

Readable:
```text
Get_Field(COMPLETION_YEAR) < Get_Number(2012)
```

Original:
```text
Get_Field(46679c8f-0648-4f1f-84d2-a961553a38a8) < Get_Number(2012)
```

<a id="e-0ead5aa4-dccc-4dea-8b5c-619b30d6a8c3"></a>

## Rehab_History_2013

Source: `dTIMSExpressions` / `0ead5aa4-dccc-4dea-8b5c-619b30d6a8c3`.

Rehab records up to 2013

Readable:
```text
Get_Field(COMPLETION_YEAR) < Get_Number(2013)
```

Original:
```text
Get_Field(46679c8f-0648-4f1f-84d2-a961553a38a8) < Get_Number(2013)
```

<a id="e-7df5317d-e00e-4da9-b489-6b8e3ca84235"></a>

## Rehab_History_2014

Source: `dTIMSExpressions` / `7df5317d-e00e-4da9-b489-6b8e3ca84235`.

Rehab records up to 2014

Readable:
```text
Get_Field(COMPLETION_YEAR) < Get_Number(2014)
```

Original:
```text
Get_Field(46679c8f-0648-4f1f-84d2-a961553a38a8) < Get_Number(2014)
```

<a id="e-d93a7941-b290-4ebc-822a-b2a8be0dd75d"></a>

## Rehab_History_2015

Source: `dTIMSExpressions` / `d93a7941-b290-4ebc-822a-b2a8be0dd75d`.

Rehab records up to 2015

Readable:
```text
Get_Field(COMPLETION_YEAR) < Get_Number(2015)
```

Original:
```text
Get_Field(46679c8f-0648-4f1f-84d2-a961553a38a8) < Get_Number(2015)
```

<a id="e-479a13f2-24ee-4140-abc4-8bc7a6ceaabd"></a>

## Rehab_History_2016

Source: `dTIMSExpressions` / `479a13f2-24ee-4140-abc4-8bc7a6ceaabd`.

Rehab records up to 2016

Readable:
```text
Get_Field(COMPLETION_YEAR) < Get_Number(2016)
```

Original:
```text
Get_Field(46679c8f-0648-4f1f-84d2-a961553a38a8) < Get_Number(2016)
```

<a id="e-622388d3-e027-4ac9-9749-a10d4d5438e7"></a>

## Road_Inventory_Length

Source: `dTIMSExpressions` / `622388d3-e027-4ac9-9749-a10d4d5438e7`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(8b68d4d6-3ae2-492c-8908-230d84597128) - Get_Field(f441bc39-5af4-4232-aca3-55477623ea3b)
```

<a id="e-09623d70-e1e2-4579-b367-26d5ece92e35"></a>

## STIP_Length

Source: `dTIMSExpressions` / `09623d70-e1e2-4579-b367-26d5ece92e35`.



Readable:
```text
Get_Field(To) - Get_Field(From)
```

Original:
```text
Get_Field(f60cb3b3-6ac4-45f5-bee5-f4a0a685a49c) - Get_Field(61927ca9-f989-4a99-bbaa-a67c875134ff)
```

<a id="e-cb1933dc-c413-4f53-b835-9fbeaa842a17"></a>

## STR_abfOBJ_Exclude_Strategies

Source: `RuntimeExpressions` / `cb1933dc-c413-4f53-b835-9fbeaa842a17`.

Exclude committed strategies that do not exactly match the pattern in the analysis master table.

Readable:
```text
    IF(IS_DN() OR IS_MO() OR NOT      IS_COMMITTED(),FALSE,
    GET_ANALVAR_4_YR(str_tAAV_Last_Major_Treatment,Get_Field(COM_YEAR)) <> Get_Field(COM_TRT) OR
    IF(Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) >Get_Number(0),GET_ANALVAR_4_YR(str_tAAV_Last_Major_Treatment,Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470)) <> Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f),FALSE) OR
    IF(Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) >Get_Number(0),GET_ANALVAR_4_YR(str_tAAV_Last_Major_Treatment,Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627)) <> Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e),FALSE) OR
    IF(Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) >Get_Number(0),GET_ANALVAR_4_YR(str_tAAV_Last_Major_Treatment,Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b)) <> Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066),FALSE)
)

```

Original:
```text
    IF(IS_DN() OR IS_MO() OR NOT      IS_COMMITTED(),FALSE,
    GET_ANALVAR_4_YR(ce9417f9-47e5-43a2-b923-77ece779c7ab,Get_Field(d62be030-874b-4177-9d41-e00645ac75d8)) <> Get_Field(30f7c9cd-b358-449a-9268-0e08a7acd1c0) OR
    IF(Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) >Get_Number(0),GET_ANALVAR_4_YR(ce9417f9-47e5-43a2-b923-77ece779c7ab,Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470)) <> Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f),FALSE) OR
    IF(Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) >Get_Number(0),GET_ANALVAR_4_YR(ce9417f9-47e5-43a2-b923-77ece779c7ab,Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627)) <> Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e),FALSE) OR
    IF(Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) >Get_Number(0),GET_ANALVAR_4_YR(ce9417f9-47e5-43a2-b923-77ece779c7ab,Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b)) <> Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066),FALSE)
)

```

<a id="e-4eafdcfe-4dab-411f-8b3e-1253479d8bc0"></a>

## pms_abfOBJ_Exclude_Strategies

Source: `RuntimeExpressions` / `4eafdcfe-4dab-411f-8b3e-1253479d8bc0`.

Exclude Strategies from optimization if they do not exactly match the committed treatments for committed treatments only.

Readable:
```text
IF(IS_DN() OR IS_MO() OR NOT  IS_COMMITTED(),FALSE,
GET_ANALVAR_4_YR(PMS_tAAV_YEARLY_TREATMENT,Get_Field(Com_Year)) <> Get_Field(Com_Trt) OR
IF(Get_Field(COM_YR_2) >Get_Number(0),GET_ANALVAR_4_YR(PMS_tAAV_YEARLY_TREATMENT,Get_Field(COM_YR_2)) <> Get_Field(COM_TRT_2),FALSE) OR
IF(Get_Field(COM_YR_3) >Get_Number(0),GET_ANALVAR_4_YR(PMS_tAAV_YEARLY_TREATMENT,Get_Field(COM_YR_3)) <> Get_Field(COM_TRT_3),FALSE) OR
IF(Get_Field(COM_YR_4) >Get_Number(0),GET_ANALVAR_4_YR(PMS_tAAV_YEARLY_TREATMENT,Get_Field(COM_YR_4)) <> Get_Field(COM_TRT_4),FALSE)
)
```

Original:
```text
IF(IS_DN() OR IS_MO() OR NOT  IS_COMMITTED(),FALSE,
GET_ANALVAR_4_YR(3057f1cc-736e-4f9a-8c6d-430b10fa23c2,Get_Field(99da8883-fa56-4a3a-8250-05908e2250c0)) <> Get_Field(ec965cc6-5ed5-4591-bf5b-1c0885ef785e) OR
IF(Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c) >Get_Number(0),GET_ANALVAR_4_YR(3057f1cc-736e-4f9a-8c6d-430b10fa23c2,Get_Field(7cda51a9-1134-418f-b584-29a838ef7b0c)) <> Get_Field(a2875f19-2f5a-4d09-920c-208664ff67c8),FALSE) OR
IF(Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e) >Get_Number(0),GET_ANALVAR_4_YR(3057f1cc-736e-4f9a-8c6d-430b10fa23c2,Get_Field(d77526c0-dc48-4ac7-ace1-dbeac6434f5e)) <> Get_Field(63019b8f-f66e-4853-8d0c-1c15c7a59395),FALSE) OR
IF(Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86) >Get_Number(0),GET_ANALVAR_4_YR(3057f1cc-736e-4f9a-8c6d-430b10fa23c2,Get_Field(10a8e247-bddb-4c25-bcbb-b2d091dfed86)) <> Get_Field(262093c5-ae74-44bd-9f4d-264b6096b917),FALSE)
)
```

<a id="e-8cf826d8-c6ea-4d32-81c3-d8349ad9cbdc"></a>

## str_NHS

Source: `dTIMSExpressions` / `8cf826d8-c6ea-4d32-81c3-d8349ad9cbdc`.



Readable:
```text
Get_Field(BUDGET_CATEGORY_OVERRIDE) = 'Bridge_NHS'
```

Original:
```text
Get_Field(1e19aa1d-5535-4ae8-9469-9f82ba2191da) = 'Bridge_NHS'
```

<a id="e-bf6d606c-bc24-474f-83c0-434700239dee"></a>

## str_Non_NHS

Source: `dTIMSExpressions` / `bf6d606c-bc24-474f-83c0-434700239dee`.

Non NHS

Readable:
```text
Get_Field(BUDGET_CATEGORY_OVERRIDE) <> 'Bridge_NHS'
```

Original:
```text
Get_Field(1e19aa1d-5535-4ae8-9469-9f82ba2191da) <> 'Bridge_NHS'
```

<a id="e-e9d9bc55-d0ca-47e3-9b23-6146b75a9cad"></a>

## str_abfOBJ_Analysis_Test_Set

Source: `dTIMSExpressions` / `e9d9bc55-d0ca-47e3-9b23-6146b75a9cad`.

Analysis Test Set

Readable:
```text
Get_Field(Name) = '13A152' OR
Get_Field(Name) = '41A151'
```

Original:
```text
Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '13A152' OR
Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '41A151'
```

<a id="e-10d8f1ef-fe98-439f-8430-19d6835c871f"></a>

## str_abfOBJ_Analysis_Test_Validation

Source: `dTIMSExpressions` / `10d8f1ef-fe98-439f-8430-19d6835c871f`.

Analysis Test Set

Readable:
```text
Get_Field(Name)='04A116' OR
Get_Field(Name)='17A241' OR
Get_Field(Name)='41A168' OR
Get_Field(Name)='15A041' OR
Get_Field(Name) = '17A087' OR
Get_Field(Name) = '18A127' OR 
Get_Field(Name) = '20A070'

```

Original:
```text
Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5)='04A116' OR
Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5)='17A241' OR
Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5)='41A168' OR
Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5)='15A041' OR
Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '17A087' OR
Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '18A127' OR 
Get_Field(646052f1-530e-4b84-a7cd-efde93ad55d5) = '20A070'

```

<a id="e-88f66303-a920-4d8d-95c0-cf3c69f9134b"></a>

## str_abfOBJ_CLV

Source: `dTIMSExpressions` / `88f66303-a920-4d8d-95c0-cf3c69f9134b`.

Is the structure a culvert?

Readable:
```text
Get_Field(CULV_RATE)<>'N'
```

Original:
```text
Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)<>'N'
```

<a id="e-64178621-7d6f-4a22-b042-c90c69c530a8"></a>

## str_abfOBJ_DK_GTE_6

Source: `RuntimeExpressions` / `64178621-7d6f-4a22-b042-c90c69c530a8`.

Deck Condition >= 6

Readable:
```text
GET_ANALVR(str_nAAV_CND_DK) >= Get_Number(6) AND 
GET_TRTYR('str_DECK_OVERLAY')<>YR AND 
GET_TRTYR('str_DECK_PATCH')<>YR AND
GET_TRTYR('str_DECK_REHAB')<>YR AND 
GET_TRTYR('str_DECK_REPLACE')<>YR
```

Original:
```text
GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903) >= Get_Number(6) AND 
GET_TRTYR('str_DECK_OVERLAY')<>YR AND 
GET_TRTYR('str_DECK_PATCH')<>YR AND
GET_TRTYR('str_DECK_REHAB')<>YR AND 
GET_TRTYR('str_DECK_REPLACE')<>YR
```

<a id="e-37631066-ccb9-4c01-bb25-d4a13db5a8b6"></a>

## str_abfOBJ_District_8

Source: `dTIMSExpressions` / `37631066-ccb9-4c01-bb25-d4a13db5a8b6`.

District 4, NHS, Poor

Readable:
```text
Get_Field(f1f6cdeb-84ed-4fd9-be8d-ce161bdb0e3d)= '8' AND 
LEFT(Get_Field(NHS),Get_Number(1))='Y' AND
Get_Field(GFP) = 'P'
```

Original:
```text
Get_Field(f1f6cdeb-84ed-4fd9-be8d-ce161bdb0e3d)= '8' AND 
LEFT(Get_Field(ff652eda-e73c-48a8-bd20-fd6e80950604),Get_Number(1))='Y' AND
Get_Field(6e7edd08-8801-4903-9058-21e5eca4da87) = 'P'
```

<a id="e-af81cede-aef1-4772-88a8-e6c4af9320d8"></a>

## str_abfOBJ_JNT

Source: `dTIMSExpressions` / `af81cede-aef1-4772-88a8-e6c4af9320d8`.

Does the structure have Deck Joints?

Readable:
```text
Get_Field(ELEM_300_QUANTITY)>Get_Number(0) OR 
Get_Field(ELEM_301_QUANTITY)>Get_Number(0) OR 
Get_Field(ELEM_302_QUANTITY)>Get_Number(0) OR 
Get_Field(ELEM_303_QUANTITY)>Get_Number(0) OR 
Get_Field(ELEM_304_QUANTITY)>Get_Number(0) OR 
Get_Field(ELEM_305_QUANTITY)>Get_Number(0) OR 
Get_Field(ELEM_306_QUANTITY)>Get_Number(0)
```

Original:
```text
Get_Field(9aedad63-77e7-447a-8c44-21a89ae03440)>Get_Number(0) OR 
Get_Field(4b504462-b48a-473c-925c-d7a8705fb230)>Get_Number(0) OR 
Get_Field(286fae98-ad52-46cc-adab-7d5978b28ac0)>Get_Number(0) OR 
Get_Field(0caab4da-a7c0-4635-a19e-e82950b8b8fc)>Get_Number(0) OR 
Get_Field(56ab8060-0651-4223-b119-3043fe5a0abc)>Get_Number(0) OR 
Get_Field(87443be7-82d6-4927-9f74-a8e47f9602b0)>Get_Number(0) OR 
Get_Field(33c2b855-eefa-4211-b1c0-a5600d95c61f)>Get_Number(0)
```

<a id="e-54c18a5c-cdfd-43cd-ac8b-0b094ccdcecc"></a>

## str_abfOBJ_Owner_StateHighwayAgency

Source: `dTIMSExpressions` / `54c18a5c-cdfd-43cd-ac8b-0b094ccdcecc`.

Owner: State Highway Agency only

Readable:
```text
LEFT(Get_Field(c7a4dd0d-cfe2-4d16-900a-c16bd6142654),Get_Number(3)) <> 'S01'
```

Original:
```text
LEFT(Get_Field(c7a4dd0d-cfe2-4d16-900a-c16bd6142654),Get_Number(3)) <> 'S01'
```

<a id="e-c4d2c71a-fe8a-455f-a3db-176724ab0ec5"></a>

## str_abfOBJ_SUB_GTE_6

Source: `RuntimeExpressions` / `c4d2c71a-fe8a-455f-a3db-176724ab0ec5`.

Substructure  Condition >= 6

Readable:
```text
GET_ANALVR(str_nAAV_CND_SUB) >= Get_Number(6) AND GET_TRTYR('str_SUBSTRUCTURE_REHAB')<>YR
```

Original:
```text
GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2) >= Get_Number(6) AND GET_TRTYR('str_SUBSTRUCTURE_REHAB')<>YR
```

<a id="e-5796df0c-f0d1-453d-8357-aabc03828ac4"></a>

## str_abfOBJ_SUP_GTE_6

Source: `RuntimeExpressions` / `5796df0c-f0d1-453d-8357-aabc03828ac4`.

Superstructure Condition >= 6

Readable:
```text
GET_ANALVR(str_nAAV_CND_SUP) >= Get_Number(6) AND GET_TRTYR('str_SUPERSTRUCTURE_REHAB')<>YR
```

Original:
```text
GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8) >= Get_Number(6) AND GET_TRTYR('str_SUPERSTRUCTURE_REHAB')<>YR
```

<a id="e-8b0e4832-dd88-45cf-8a50-705a8044de7a"></a>

## str_abfOBJ_True

Source: `dTIMSExpressions` / `8b0e4832-dd88-45cf-8a50-705a8044de7a`.

Analysis Test Set

Readable:
```text
TRUE
```

Original:
```text
TRUE
```

<a id="e-185f2983-5788-48bd-bcf6-56afc8261b00"></a>

## str_abfOBJ_Turnpike

Source: `dTIMSExpressions` / `185f2983-5788-48bd-bcf6-56afc8261b00`.

Turnpike excluded from analysis


Readable:
```text
LEFT(Get_Field(c7a4dd0d-cfe2-4d16-900a-c16bd6142654),Get_Number(3)) = 'S03'
```

Original:
```text
LEFT(Get_Field(c7a4dd0d-cfe2-4d16-900a-c16bd6142654),Get_Number(3)) = 'S03'
```

<a id="e-514e13aa-7148-4136-9203-bdfcf0248f0b"></a>

## str_abfTRG_BKAMPP

Source: `RuntimeExpressions` / `514e13aa-7148-4136-9203-bdfcf0248f0b`.

Trigger for BKAMPP

Readable:
```text
IF(IS_COMMITTED() AND Get_Field(COM_YEAR)=YR AND Get_Field(COM_TRT)='str_BKAMPP',
    TRUE
    ,
    GET_ANALVR(str_nAAV_TRF_ADT)>Get_Number(3000) AND
    Get_Field(CULV_RATE)='N' AND 
    GET_ANALVR(str_nAAV_CND_SUB)<=Get_Number(7) AND
    GET_ANALVR(str_nAAV_CND_SUB)>=Get_Number(6) AND
    GET_ANALVR(str_nAAV_CND_SUP)>=Get_Number(6) AND 
    GET_ANALVR(str_nAAV_CND_SUP)<=Get_Number(7) AND
    GET_ANALVR(str_nAAV_CND_DK)>=Get_Number(6) AND 
    GET_ANALVR(str_nAAV_CND_DK)<=Get_Number(7) AND 
    LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C')
```

Original:
```text
IF(IS_COMMITTED() AND Get_Field(d62be030-874b-4177-9d41-e00645ac75d8)=YR AND Get_Field(30f7c9cd-b358-449a-9268-0e08a7acd1c0)='str_BKAMPP',
    TRUE
    ,
    GET_ANALVR(5354dc5d-c869-4579-8ae4-eb60a9c12614)>Get_Number(3000) AND
    Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' AND 
    GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)<=Get_Number(7) AND
    GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)>=Get_Number(6) AND
    GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)>=Get_Number(6) AND 
    GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)<=Get_Number(7) AND
    GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)>=Get_Number(6) AND 
    GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)<=Get_Number(7) AND 
    LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C')
```

<a id="e-14a949b8-2079-468b-8de4-7f48d4491d82"></a>

## str_abfTRG_CULVERT_REHAB

Source: `RuntimeExpressions` / `14a949b8-2079-468b-8de4-7f48d4491d82`.

Trigger for Culvert Rehab Treatment

Readable:
```text
IF(Get_Field(CULV_RATE)<>'N',
    GET_ANALVR(str_nAAV_CND_CVT)=Get_Number(5) AND 
    GET_ANALVR(str_nDAV_CT_CVT_REHAB)<Get_Number(1) AND 
    LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C',
    FALSE)
    
//Bridge->BRIDGE_TYPE<>'Concrete Cont Culvert'
//removed 2026-05-08 temporary measure
```

Original:
```text
IF(Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)<>'N',
    GET_ANALVR(fb31bbaf-26dc-4b1f-9e1b-31000f7ee770)=Get_Number(5) AND 
    GET_ANALVR(b7aad387-e270-431f-8bf2-4e520a51aa61)<Get_Number(1) AND 
    LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C',
    FALSE)
    
//Bridge->BRIDGE_TYPE<>'Concrete Cont Culvert'
//removed 2026-05-08 temporary measure
```

<a id="e-0307e901-dd2c-4459-9191-a9f3e0b85646"></a>

## str_abfTRG_CULVERT_REPLACEMENT

Source: `RuntimeExpressions` / `0307e901-dd2c-4459-9191-a9f3e0b85646`.

Trigger for Culvert Replacement

Readable:
```text
Get_Field(CULV_RATE)<> 'N' AND GET_ANALVR(str_nAAV_CND_CVT)<=Get_Number(4) 
```

Original:
```text
Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)<> 'N' AND GET_ANALVR(fb31bbaf-26dc-4b1f-9e1b-31000f7ee770)<=Get_Number(4) 
```

<a id="e-efd94559-069c-4003-99b3-9adcbfed6a21"></a>

## str_abfTRG_DECK_OVERLAY

Source: `RuntimeExpressions` / `efd94559-069c-4003-99b3-9adcbfed6a21`.

Trigger for Deck Overlay

Readable:
```text
IF(Get_Field(CULV_RATE)='N' AND IS_COMMITTED(),
    (
        Get_Field(COM_YEAR)=YR AND Get_Field(COM_TRT)='str_STR_MTCE' AND
        (
        Get_Field(COM_TRT_2)='str_DECK_OVERLAY' OR
        Get_Field(COM_TRT_3)='str_DECK_OVERLAY' OR 
        Get_Field(COM_TRT_4)='str_DECK_OVERLAY' OR
        Get_Field(COM_TRT_5)='str_DECK_OVERLAY')
    )
    OR
    (
        Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) =YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f) ='str_STR_MTCE' AND
        (
        Get_Field(ebbc3e10-5dd9-4e71-ad67-74b5ba13bfcd)='str_DECK_OVERLAY' OR
        Get_Field(39c10537-8525-4c42-acb9-d5d079549f51)='str_DECK_OVERLAY' OR 
        Get_Field(aa2bb7e0-c193-43a0-b873-55028a6b4a97)='str_DECK_OVERLAY' OR
        Get_Field(5aa4674b-28ab-45b4-9a3e-0046121321ba)='str_DECK_OVERLAY')
    ) 
    OR
    (
        Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) =YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e) ='str_STR_MTCE' AND
        (
        Get_Field(bc6e9d36-4cf4-4634-a7e3-bf7279551208)='str_DECK_OVERLAY' OR
        Get_Field(c8c4be3e-b718-4519-ab88-fdd18ef20e24)='str_DECK_OVERLAY' OR 
        Get_Field(8e11bd4b-a952-4f78-9eff-759dea0073da)='str_DECK_OVERLAY' OR
        Get_Field(026fe3ff-21d1-400d-a170-08962f1cd29e)='str_DECK_OVERLAY')
    )
    OR
    (
        Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) =YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066) ='str_STR_MTCE' AND
        (
        Get_Field(2203185a-fb64-4f8d-a076-d0d5f9ba0930)='str_DECK_OVERLAY' OR
        Get_Field(8e7c8042-efdf-412e-b812-68345b4440ce)='str_DECK_OVERLAY' OR 
        Get_Field(a1fcdfda-6c28-4c51-bcd6-952e671db7cd)='str_DECK_OVERLAY' OR
        Get_Field(d26a67bc-6d3c-4836-ac39-a694f421fbb3)='str_DECK_OVERLAY')
    )
    ,
    Get_Field(CULV_RATE)='N' AND 
    GET_ANALVR(str_nAAV_CND_DK)<=Get_Number(5) AND
    GET_ANALVR(str_nAAV_CND_DK)>Get_Number(4) AND
    (GET_ANALVR(str_nAAV_CND_SUP)>=Get_Number(5) OR GET_ANALVR(str_nAAV_CND_SUP) = -Get_Number(1)) AND
    (GET_ANALVR(str_nAAV_CND_SUB)>=Get_Number(5) OR GET_ANALVR(str_nAAV_CND_SUB) = -Get_Number(1)) AND
    GET_ANALVR(str_nDAV_CT_DECK_OVERLAY)<=Get_Number(2) AND
    GET_ANALVR(str_nAAV_CND_DK_LIFE)<=Get_Number(0)
    AND LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C' )
```

Original:
```text
IF(Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' AND IS_COMMITTED(),
    (
        Get_Field(d62be030-874b-4177-9d41-e00645ac75d8)=YR AND Get_Field(30f7c9cd-b358-449a-9268-0e08a7acd1c0)='str_STR_MTCE' AND
        (
        Get_Field(4c06d943-9c6f-4f56-a854-8b32874f3150)='str_DECK_OVERLAY' OR
        Get_Field(42468b1b-19ff-4bb8-91be-d32a8a45006f)='str_DECK_OVERLAY' OR 
        Get_Field(131f88ca-12ec-4428-8f07-65bf2eec7eef)='str_DECK_OVERLAY' OR
        Get_Field(669eef45-c4e7-41d6-b434-ba2c1a49fb32)='str_DECK_OVERLAY')
    )
    OR
    (
        Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) =YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f) ='str_STR_MTCE' AND
        (
        Get_Field(ebbc3e10-5dd9-4e71-ad67-74b5ba13bfcd)='str_DECK_OVERLAY' OR
        Get_Field(39c10537-8525-4c42-acb9-d5d079549f51)='str_DECK_OVERLAY' OR 
        Get_Field(aa2bb7e0-c193-43a0-b873-55028a6b4a97)='str_DECK_OVERLAY' OR
        Get_Field(5aa4674b-28ab-45b4-9a3e-0046121321ba)='str_DECK_OVERLAY')
    ) 
    OR
    (
        Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) =YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e) ='str_STR_MTCE' AND
        (
        Get_Field(bc6e9d36-4cf4-4634-a7e3-bf7279551208)='str_DECK_OVERLAY' OR
        Get_Field(c8c4be3e-b718-4519-ab88-fdd18ef20e24)='str_DECK_OVERLAY' OR 
        Get_Field(8e11bd4b-a952-4f78-9eff-759dea0073da)='str_DECK_OVERLAY' OR
        Get_Field(026fe3ff-21d1-400d-a170-08962f1cd29e)='str_DECK_OVERLAY')
    )
    OR
    (
        Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) =YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066) ='str_STR_MTCE' AND
        (
        Get_Field(2203185a-fb64-4f8d-a076-d0d5f9ba0930)='str_DECK_OVERLAY' OR
        Get_Field(8e7c8042-efdf-412e-b812-68345b4440ce)='str_DECK_OVERLAY' OR 
        Get_Field(a1fcdfda-6c28-4c51-bcd6-952e671db7cd)='str_DECK_OVERLAY' OR
        Get_Field(d26a67bc-6d3c-4836-ac39-a694f421fbb3)='str_DECK_OVERLAY')
    )
    ,
    Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' AND 
    GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)<=Get_Number(5) AND
    GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)>Get_Number(4) AND
    (GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)>=Get_Number(5) OR GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8) = -Get_Number(1)) AND
    (GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)>=Get_Number(5) OR GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2) = -Get_Number(1)) AND
    GET_ANALVR(45fd84e7-4367-49de-919f-f8bf01e12c6f)<=Get_Number(2) AND
    GET_ANALVR(27eddee2-190d-4175-ba2f-ed3bfa8ecb75)<=Get_Number(0)
    AND LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C' )
```

<a id="e-1a105d30-6f2f-4869-9da7-0acdf2483d52"></a>

## str_abfTRG_DECK_PATCH

Source: `RuntimeExpressions` / `1a105d30-6f2f-4869-9da7-0acdf2483d52`.

Trigger for Deck Patch

Readable:
```text
IF(Get_Field(CULV_RATE)='N' AND IS_COMMITTED(),
    (
        Get_Field(COM_YEAR)=YR AND Get_Field(COM_TRT)='str_STR_MTCE' AND
        (
        Get_Field(COM_TRT_2)='str_DECK_PATCH' OR
        Get_Field(COM_TRT_3)='str_DECK_PATCH' OR 
        Get_Field(COM_TRT_4)='str_DECK_PATCH' OR
        Get_Field(COM_TRT_5)='str_DECK_PATCH')
    )
    OR
    (
        Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) =YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f) ='str_STR_MTCE' AND
        (
        Get_Field(ebbc3e10-5dd9-4e71-ad67-74b5ba13bfcd)='str_DECK_PATCH' OR
        Get_Field(39c10537-8525-4c42-acb9-d5d079549f51)='str_DECK_PATCH' OR 
        Get_Field(aa2bb7e0-c193-43a0-b873-55028a6b4a97)='str_DECK_PATCH' OR
        Get_Field(5aa4674b-28ab-45b4-9a3e-0046121321ba)='str_DECK_PATCH')
    ) 
    OR
    (
        Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) =YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e) ='str_STR_MTCE' AND
        (
        Get_Field(bc6e9d36-4cf4-4634-a7e3-bf7279551208)='str_DECK_PATCH' OR
        Get_Field(c8c4be3e-b718-4519-ab88-fdd18ef20e24)='str_DECK_PATCH' OR 
        Get_Field(8e11bd4b-a952-4f78-9eff-759dea0073da)='str_DECK_PATCH' OR
        Get_Field(026fe3ff-21d1-400d-a170-08962f1cd29e)='str_DECK_PATCH')
    )
    OR
    (
        Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) =YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066) ='str_STR_MTCE' AND
        (
        Get_Field(2203185a-fb64-4f8d-a076-d0d5f9ba0930)='str_DECK_PATCH' OR
        Get_Field(8e7c8042-efdf-412e-b812-68345b4440ce)='str_DECK_PATCH' OR 
        Get_Field(a1fcdfda-6c28-4c51-bcd6-952e671db7cd)='str_DECK_PATCH' OR
        Get_Field(d26a67bc-6d3c-4836-ac39-a694f421fbb3)='str_DECK_PATCH')
    )
    ,
    GET_ANALVR(str_nDAV_CT_DECK_PATCH) = Get_Number(0) AND
    Get_Field(CULV_RATE)='N' AND 
    GET_ANALVR(str_nAAV_CND_DK)>=Get_Number(6) AND 
    (GET_ANALVR(str_nAAV_CND_SUP)>=Get_Number(6) OR GET_ANALVR(str_nAAV_CND_SUP) = -Get_Number(1)) AND 
    (GET_ANALVR(str_nAAV_CND_SUB)>=Get_Number(6) OR GET_ANALVR(str_nAAV_CND_SUB)=-Get_Number(1)) AND 
    (GET_ANALVR(str_AAV_ELEM_1080_CS3)+GET_ANALVR(str_AAV_ELEM_1080_CS4))>Get_Number(5) AND  
    (GET_ANALVR(str_AAV_ELEM_1080_CS3)+GET_ANALVR(str_AAV_ELEM_1080_CS4))<=Get_Number(15)
    AND LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C')
```

Original:
```text
IF(Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' AND IS_COMMITTED(),
    (
        Get_Field(d62be030-874b-4177-9d41-e00645ac75d8)=YR AND Get_Field(30f7c9cd-b358-449a-9268-0e08a7acd1c0)='str_STR_MTCE' AND
        (
        Get_Field(4c06d943-9c6f-4f56-a854-8b32874f3150)='str_DECK_PATCH' OR
        Get_Field(42468b1b-19ff-4bb8-91be-d32a8a45006f)='str_DECK_PATCH' OR 
        Get_Field(131f88ca-12ec-4428-8f07-65bf2eec7eef)='str_DECK_PATCH' OR
        Get_Field(669eef45-c4e7-41d6-b434-ba2c1a49fb32)='str_DECK_PATCH')
    )
    OR
    (
        Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) =YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f) ='str_STR_MTCE' AND
        (
        Get_Field(ebbc3e10-5dd9-4e71-ad67-74b5ba13bfcd)='str_DECK_PATCH' OR
        Get_Field(39c10537-8525-4c42-acb9-d5d079549f51)='str_DECK_PATCH' OR 
        Get_Field(aa2bb7e0-c193-43a0-b873-55028a6b4a97)='str_DECK_PATCH' OR
        Get_Field(5aa4674b-28ab-45b4-9a3e-0046121321ba)='str_DECK_PATCH')
    ) 
    OR
    (
        Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) =YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e) ='str_STR_MTCE' AND
        (
        Get_Field(bc6e9d36-4cf4-4634-a7e3-bf7279551208)='str_DECK_PATCH' OR
        Get_Field(c8c4be3e-b718-4519-ab88-fdd18ef20e24)='str_DECK_PATCH' OR 
        Get_Field(8e11bd4b-a952-4f78-9eff-759dea0073da)='str_DECK_PATCH' OR
        Get_Field(026fe3ff-21d1-400d-a170-08962f1cd29e)='str_DECK_PATCH')
    )
    OR
    (
        Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) =YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066) ='str_STR_MTCE' AND
        (
        Get_Field(2203185a-fb64-4f8d-a076-d0d5f9ba0930)='str_DECK_PATCH' OR
        Get_Field(8e7c8042-efdf-412e-b812-68345b4440ce)='str_DECK_PATCH' OR 
        Get_Field(a1fcdfda-6c28-4c51-bcd6-952e671db7cd)='str_DECK_PATCH' OR
        Get_Field(d26a67bc-6d3c-4836-ac39-a694f421fbb3)='str_DECK_PATCH')
    )
    ,
    GET_ANALVR(1c49a685-77ed-481e-aaef-6f715ffd9d64) = Get_Number(0) AND
    Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' AND 
    GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)>=Get_Number(6) AND 
    (GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)>=Get_Number(6) OR GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8) = -Get_Number(1)) AND 
    (GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)>=Get_Number(6) OR GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)=-Get_Number(1)) AND 
    (GET_ANALVR(53bec880-322b-4ac1-a03a-c79fb354c4fb)+GET_ANALVR(454eb22e-95d5-4589-9f60-860fbaaff091))>Get_Number(5) AND  
    (GET_ANALVR(53bec880-322b-4ac1-a03a-c79fb354c4fb)+GET_ANALVR(454eb22e-95d5-4589-9f60-860fbaaff091))<=Get_Number(15)
    AND LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C')
```

<a id="e-531f547a-a5ea-4ab2-aa61-e23ff53484af"></a>

## str_abfTRG_DECK_REHAB

Source: `RuntimeExpressions` / `531f547a-a5ea-4ab2-aa61-e23ff53484af`.

Trigger for Deck Rehab

Readable:
```text
IF(Get_Field(CULV_RATE)='N' AND IS_COMMITTED(),
    (
        Get_Field(COM_YEAR)=YR AND Get_Field(COM_TRT)='str_STR_MTCE' AND
        (
        Get_Field(COM_TRT_2)='str_DECK_REHAB' OR
        Get_Field(COM_TRT_3)='str_DECK_REHAB' OR 
        Get_Field(COM_TRT_4)='str_DECK_REHAB' OR
        Get_Field(COM_TRT_5)='str_DECK_REHAB')
    )
    OR
    (
        Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) =YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f) ='str_STR_MTCE' AND
        (
        Get_Field(ebbc3e10-5dd9-4e71-ad67-74b5ba13bfcd)='str_DECK_REHAB' OR
        Get_Field(39c10537-8525-4c42-acb9-d5d079549f51)='str_DECK_REHAB' OR 
        Get_Field(aa2bb7e0-c193-43a0-b873-55028a6b4a97)='str_DECK_REHAB' OR
        Get_Field(5aa4674b-28ab-45b4-9a3e-0046121321ba)='str_DECK_REHAB')
    ) 
    OR
    (
        Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) =YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e) ='str_STR_MTCE' AND
        (
        Get_Field(bc6e9d36-4cf4-4634-a7e3-bf7279551208)='str_DECK_REHAB' OR
        Get_Field(c8c4be3e-b718-4519-ab88-fdd18ef20e24)='str_DECK_REHAB' OR 
        Get_Field(8e11bd4b-a952-4f78-9eff-759dea0073da)='str_DECK_REHAB' OR
        Get_Field(026fe3ff-21d1-400d-a170-08962f1cd29e)='str_DECK_REHAB')
    )
    OR
    (
        Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) =YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066) ='str_STR_MTCE' AND
        (
        Get_Field(2203185a-fb64-4f8d-a076-d0d5f9ba0930)='str_DECK_REHAB' OR
        Get_Field(8e7c8042-efdf-412e-b812-68345b4440ce)='str_DECK_REHAB' OR 
        Get_Field(a1fcdfda-6c28-4c51-bcd6-952e671db7cd)='str_DECK_REHAB' OR
        Get_Field(d26a67bc-6d3c-4836-ac39-a694f421fbb3)='str_DECK_REHAB')
    )
    ,
    Get_Field(CULV_RATE)='N' AND
    GET_ANALVR(str_nAAV_CND_DK)<=Get_Number(5) AND GET_ANALVR(str_nAAV_CND_DK)>Get_Number(4) AND 
    (GET_ANALVR(str_nAAV_CND_SUP)>=Get_Number(5) OR GET_ANALVR(str_nAAV_CND_SUP) = -Get_Number(1)) AND 
    (GET_ANALVR(str_nAAV_CND_SUB)>=Get_Number(5) OR GET_ANALVR(str_nAAV_CND_SUB) = -Get_Number(1)) AND 
    GET_ANALVR(str_nDAV_CT_DK_REHAB)<=Get_Number(1)
    AND LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C')
```

Original:
```text
IF(Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' AND IS_COMMITTED(),
    (
        Get_Field(d62be030-874b-4177-9d41-e00645ac75d8)=YR AND Get_Field(30f7c9cd-b358-449a-9268-0e08a7acd1c0)='str_STR_MTCE' AND
        (
        Get_Field(4c06d943-9c6f-4f56-a854-8b32874f3150)='str_DECK_REHAB' OR
        Get_Field(42468b1b-19ff-4bb8-91be-d32a8a45006f)='str_DECK_REHAB' OR 
        Get_Field(131f88ca-12ec-4428-8f07-65bf2eec7eef)='str_DECK_REHAB' OR
        Get_Field(669eef45-c4e7-41d6-b434-ba2c1a49fb32)='str_DECK_REHAB')
    )
    OR
    (
        Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) =YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f) ='str_STR_MTCE' AND
        (
        Get_Field(ebbc3e10-5dd9-4e71-ad67-74b5ba13bfcd)='str_DECK_REHAB' OR
        Get_Field(39c10537-8525-4c42-acb9-d5d079549f51)='str_DECK_REHAB' OR 
        Get_Field(aa2bb7e0-c193-43a0-b873-55028a6b4a97)='str_DECK_REHAB' OR
        Get_Field(5aa4674b-28ab-45b4-9a3e-0046121321ba)='str_DECK_REHAB')
    ) 
    OR
    (
        Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) =YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e) ='str_STR_MTCE' AND
        (
        Get_Field(bc6e9d36-4cf4-4634-a7e3-bf7279551208)='str_DECK_REHAB' OR
        Get_Field(c8c4be3e-b718-4519-ab88-fdd18ef20e24)='str_DECK_REHAB' OR 
        Get_Field(8e11bd4b-a952-4f78-9eff-759dea0073da)='str_DECK_REHAB' OR
        Get_Field(026fe3ff-21d1-400d-a170-08962f1cd29e)='str_DECK_REHAB')
    )
    OR
    (
        Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) =YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066) ='str_STR_MTCE' AND
        (
        Get_Field(2203185a-fb64-4f8d-a076-d0d5f9ba0930)='str_DECK_REHAB' OR
        Get_Field(8e7c8042-efdf-412e-b812-68345b4440ce)='str_DECK_REHAB' OR 
        Get_Field(a1fcdfda-6c28-4c51-bcd6-952e671db7cd)='str_DECK_REHAB' OR
        Get_Field(d26a67bc-6d3c-4836-ac39-a694f421fbb3)='str_DECK_REHAB')
    )
    ,
    Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' AND
    GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)<=Get_Number(5) AND GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)>Get_Number(4) AND 
    (GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)>=Get_Number(5) OR GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8) = -Get_Number(1)) AND 
    (GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)>=Get_Number(5) OR GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2) = -Get_Number(1)) AND 
    GET_ANALVR(b2fa169b-0126-424b-8fc8-93723939a1b4)<=Get_Number(1)
    AND LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C')
```

<a id="e-151050ed-3016-4c9b-9fb3-235cca9ca715"></a>

## str_abfTRG_DECK_REPLACE

Source: `RuntimeExpressions` / `151050ed-3016-4c9b-9fb3-235cca9ca715`.

Trigger for Deck Replace

Readable:
```text
IF(Get_Field(CULV_RATE)='N' AND IS_COMMITTED(),
    (
        Get_Field(COM_YEAR)=YR AND Get_Field(COM_TRT)='str_STR_MTCE' AND
        (
        Get_Field(COM_TRT_2)='str_DECK_REPLACE' OR
        Get_Field(COM_TRT_3)='str_DECK_REPLACE' OR 
        Get_Field(COM_TRT_4)='str_DECK_REPLACE' OR
        Get_Field(COM_TRT_5)='str_DECK_REPLACE')
    )
    OR
    (
        Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) =YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f) ='str_STR_MTCE' AND
        (
        Get_Field(ebbc3e10-5dd9-4e71-ad67-74b5ba13bfcd)='str_DECK_REPLACE' OR
        Get_Field(39c10537-8525-4c42-acb9-d5d079549f51)='str_DECK_REPLACE' OR 
        Get_Field(aa2bb7e0-c193-43a0-b873-55028a6b4a97)='str_DECK_REPLACE' OR
        Get_Field(5aa4674b-28ab-45b4-9a3e-0046121321ba)='str_DECK_REPLACE')
    ) 
    OR
    (
        Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) =YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e) ='str_STR_MTCE' AND
        (
        Get_Field(bc6e9d36-4cf4-4634-a7e3-bf7279551208)='str_DECK_REPLACE' OR
        Get_Field(c8c4be3e-b718-4519-ab88-fdd18ef20e24)='str_DECK_REPLACE' OR 
        Get_Field(8e11bd4b-a952-4f78-9eff-759dea0073da)='str_DECK_REPLACE' OR
        Get_Field(026fe3ff-21d1-400d-a170-08962f1cd29e)='str_DECK_REPLACE')
    )
    OR
    (
        Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) =YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066) ='str_STR_MTCE' AND
        (
        Get_Field(2203185a-fb64-4f8d-a076-d0d5f9ba0930)='str_DECK_REPLACE' OR
        Get_Field(8e7c8042-efdf-412e-b812-68345b4440ce)='str_DECK_REPLACE' OR 
        Get_Field(a1fcdfda-6c28-4c51-bcd6-952e671db7cd)='str_DECK_REPLACE' OR
        Get_Field(d26a67bc-6d3c-4836-ac39-a694f421fbb3)='str_DECK_REPLACE')
    )
    ,
    Get_Field(CULV_RATE)='N' AND 
    GET_ANALVR(str_nAAV_CND_DK)>-Get_Number(1)  AND
    GET_ANALVR(str_nAAV_CND_DK)<=Get_Number(4)  AND 
    (GET_ANALVR(str_nAAV_CND_SUP)>=Get_Number(5) OR GET_ANALVR(str_nAAV_CND_SUP) = -Get_Number(1)) AND 
    (GET_ANALVR(str_nAAV_CND_SUB)>=Get_Number(5) OR GET_ANALVR(str_nAAV_CND_SUB) = -Get_Number(1)) AND 
    GET_ANALVR(str_nDAV_CT_DECK_REPLACE)<=Get_Number(2)
    AND LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C')
```

Original:
```text
IF(Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' AND IS_COMMITTED(),
    (
        Get_Field(d62be030-874b-4177-9d41-e00645ac75d8)=YR AND Get_Field(30f7c9cd-b358-449a-9268-0e08a7acd1c0)='str_STR_MTCE' AND
        (
        Get_Field(4c06d943-9c6f-4f56-a854-8b32874f3150)='str_DECK_REPLACE' OR
        Get_Field(42468b1b-19ff-4bb8-91be-d32a8a45006f)='str_DECK_REPLACE' OR 
        Get_Field(131f88ca-12ec-4428-8f07-65bf2eec7eef)='str_DECK_REPLACE' OR
        Get_Field(669eef45-c4e7-41d6-b434-ba2c1a49fb32)='str_DECK_REPLACE')
    )
    OR
    (
        Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) =YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f) ='str_STR_MTCE' AND
        (
        Get_Field(ebbc3e10-5dd9-4e71-ad67-74b5ba13bfcd)='str_DECK_REPLACE' OR
        Get_Field(39c10537-8525-4c42-acb9-d5d079549f51)='str_DECK_REPLACE' OR 
        Get_Field(aa2bb7e0-c193-43a0-b873-55028a6b4a97)='str_DECK_REPLACE' OR
        Get_Field(5aa4674b-28ab-45b4-9a3e-0046121321ba)='str_DECK_REPLACE')
    ) 
    OR
    (
        Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) =YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e) ='str_STR_MTCE' AND
        (
        Get_Field(bc6e9d36-4cf4-4634-a7e3-bf7279551208)='str_DECK_REPLACE' OR
        Get_Field(c8c4be3e-b718-4519-ab88-fdd18ef20e24)='str_DECK_REPLACE' OR 
        Get_Field(8e11bd4b-a952-4f78-9eff-759dea0073da)='str_DECK_REPLACE' OR
        Get_Field(026fe3ff-21d1-400d-a170-08962f1cd29e)='str_DECK_REPLACE')
    )
    OR
    (
        Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) =YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066) ='str_STR_MTCE' AND
        (
        Get_Field(2203185a-fb64-4f8d-a076-d0d5f9ba0930)='str_DECK_REPLACE' OR
        Get_Field(8e7c8042-efdf-412e-b812-68345b4440ce)='str_DECK_REPLACE' OR 
        Get_Field(a1fcdfda-6c28-4c51-bcd6-952e671db7cd)='str_DECK_REPLACE' OR
        Get_Field(d26a67bc-6d3c-4836-ac39-a694f421fbb3)='str_DECK_REPLACE')
    )
    ,
    Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' AND 
    GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)>-Get_Number(1)  AND
    GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)<=Get_Number(4)  AND 
    (GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)>=Get_Number(5) OR GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8) = -Get_Number(1)) AND 
    (GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)>=Get_Number(5) OR GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2) = -Get_Number(1)) AND 
    GET_ANALVR(56a680b6-13bd-4b2e-a21f-df55b5cfbb9a)<=Get_Number(2)
    AND LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C')
```

<a id="e-f2746237-bf2f-458a-a776-c6a246b5ca11"></a>

## str_abfTRG_DECK_SEAL

Source: `RuntimeExpressions` / `f2746237-bf2f-458a-a776-c6a246b5ca11`.

Trigger for Deck Seal

Readable:
```text
IF(Get_Field(CULV_RATE)='N' AND IS_COMMITTED(),
    (
        Get_Field(COM_YEAR)=YR AND Get_Field(COM_TRT)='str_STR_MTCE' AND
        (
        Get_Field(COM_TRT_2)='str_DECK_SEAL' OR
        Get_Field(COM_TRT_3)='str_DECK_SEAL' OR 
        Get_Field(COM_TRT_4)='str_DECK_SEAL' OR
        Get_Field(COM_TRT_5)='str_DECK_SEAL')
    )
    OR
    (
        Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) =YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f) ='str_STR_MTCE' AND
        (
        Get_Field(ebbc3e10-5dd9-4e71-ad67-74b5ba13bfcd)='str_DECK_SEAL' OR
        Get_Field(39c10537-8525-4c42-acb9-d5d079549f51)='str_DECK_SEAL' OR 
        Get_Field(aa2bb7e0-c193-43a0-b873-55028a6b4a97)='str_DECK_SEAL' OR
        Get_Field(5aa4674b-28ab-45b4-9a3e-0046121321ba)='str_DECK_SEAL')
    ) 
    OR
    (
        Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) =YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e) ='str_STR_MTCE' AND
        (
        Get_Field(bc6e9d36-4cf4-4634-a7e3-bf7279551208)='str_DECK_SEAL' OR
        Get_Field(c8c4be3e-b718-4519-ab88-fdd18ef20e24)='str_DECK_SEAL' OR 
        Get_Field(8e11bd4b-a952-4f78-9eff-759dea0073da)='str_DECK_SEAL' OR
        Get_Field(026fe3ff-21d1-400d-a170-08962f1cd29e)='str_DECK_SEAL')
    )
    OR
    (
        Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) =YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066) ='str_STR_MTCE' AND
        (
        Get_Field(2203185a-fb64-4f8d-a076-d0d5f9ba0930)='str_DECK_SEAL' OR
        Get_Field(8e7c8042-efdf-412e-b812-68345b4440ce)='str_DECK_SEAL' OR 
        Get_Field(a1fcdfda-6c28-4c51-bcd6-952e671db7cd)='str_DECK_SEAL' OR
        Get_Field(d26a67bc-6d3c-4836-ac39-a694f421fbb3)='str_DECK_SEAL')
    )
    ,
    IF(GET_ANALVR(str_nDAV_CT_DECK_SEAL)<Get_Number(1),
        GET_ANALVR(str_nAAV_CND_DK)>=Get_Number(6.01) AND 
        (GET_ANALVR(str_nAAV_CND_SUP)>=Get_Number(6) OR GET_ANALVR(str_nAAV_CND_SUP) =-Get_Number(1)) AND
        (GET_ANALVR(str_nAAV_CND_SUB)>=Get_Number(6) OR GET_ANALVR(str_nAAV_CND_SUB) = -Get_Number(1)) AND 
        (LEFT(Get_Field(WEARING_SURFACE_TYPE),Get_Number(1))='0' OR IFDEFAULT(Get_Field(WEARING_SURFACE_TYPE))) AND 
        LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C'
        ,
        GET_ANALVR(str_nAAV_CND_DK)>=Get_Number(6.01) AND 
        (GET_ANALVR(str_nAAV_CND_SUP)>=Get_Number(6) OR GET_ANALVR(str_nAAV_CND_SUP) = -Get_Number(1)) AND
        (GET_ANALVR(str_nAAV_CND_SUB)>=Get_Number(6) OR GET_ANALVR(str_nAAV_CND_SUB) =-Get_Number(1)) AND
        (LEFT(Get_Field(WEARING_SURFACE_TYPE),Get_Number(1))='0' OR IFDEFAULT(Get_Field(WEARING_SURFACE_TYPE))) AND
        GET_ANALVR(str_nAAV_AGE_WS)>=Get_Number(1) AND
        GET_ANALVR(str_AAV_ELEM_1130_CS3)+GET_ANALVR(str_AAV_ELEM_1130_CS4)>Get_Number(30)
        AND LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C')
        )
```

Original:
```text
IF(Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' AND IS_COMMITTED(),
    (
        Get_Field(d62be030-874b-4177-9d41-e00645ac75d8)=YR AND Get_Field(30f7c9cd-b358-449a-9268-0e08a7acd1c0)='str_STR_MTCE' AND
        (
        Get_Field(4c06d943-9c6f-4f56-a854-8b32874f3150)='str_DECK_SEAL' OR
        Get_Field(42468b1b-19ff-4bb8-91be-d32a8a45006f)='str_DECK_SEAL' OR 
        Get_Field(131f88ca-12ec-4428-8f07-65bf2eec7eef)='str_DECK_SEAL' OR
        Get_Field(669eef45-c4e7-41d6-b434-ba2c1a49fb32)='str_DECK_SEAL')
    )
    OR
    (
        Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) =YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f) ='str_STR_MTCE' AND
        (
        Get_Field(ebbc3e10-5dd9-4e71-ad67-74b5ba13bfcd)='str_DECK_SEAL' OR
        Get_Field(39c10537-8525-4c42-acb9-d5d079549f51)='str_DECK_SEAL' OR 
        Get_Field(aa2bb7e0-c193-43a0-b873-55028a6b4a97)='str_DECK_SEAL' OR
        Get_Field(5aa4674b-28ab-45b4-9a3e-0046121321ba)='str_DECK_SEAL')
    ) 
    OR
    (
        Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) =YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e) ='str_STR_MTCE' AND
        (
        Get_Field(bc6e9d36-4cf4-4634-a7e3-bf7279551208)='str_DECK_SEAL' OR
        Get_Field(c8c4be3e-b718-4519-ab88-fdd18ef20e24)='str_DECK_SEAL' OR 
        Get_Field(8e11bd4b-a952-4f78-9eff-759dea0073da)='str_DECK_SEAL' OR
        Get_Field(026fe3ff-21d1-400d-a170-08962f1cd29e)='str_DECK_SEAL')
    )
    OR
    (
        Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) =YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066) ='str_STR_MTCE' AND
        (
        Get_Field(2203185a-fb64-4f8d-a076-d0d5f9ba0930)='str_DECK_SEAL' OR
        Get_Field(8e7c8042-efdf-412e-b812-68345b4440ce)='str_DECK_SEAL' OR 
        Get_Field(a1fcdfda-6c28-4c51-bcd6-952e671db7cd)='str_DECK_SEAL' OR
        Get_Field(d26a67bc-6d3c-4836-ac39-a694f421fbb3)='str_DECK_SEAL')
    )
    ,
    IF(GET_ANALVR(53a78417-71fe-42fe-a886-1f7d9d8828b2)<Get_Number(1),
        GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)>=Get_Number(6.01) AND 
        (GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)>=Get_Number(6) OR GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8) =-Get_Number(1)) AND
        (GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)>=Get_Number(6) OR GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2) = -Get_Number(1)) AND 
        (LEFT(Get_Field(49c34f39-82d9-49c3-86ed-0176d17e3a9c),Get_Number(1))='0' OR IFDEFAULT(Get_Field(49c34f39-82d9-49c3-86ed-0176d17e3a9c))) AND 
        LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C'
        ,
        GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)>=Get_Number(6.01) AND 
        (GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)>=Get_Number(6) OR GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8) = -Get_Number(1)) AND
        (GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)>=Get_Number(6) OR GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2) =-Get_Number(1)) AND
        (LEFT(Get_Field(49c34f39-82d9-49c3-86ed-0176d17e3a9c),Get_Number(1))='0' OR IFDEFAULT(Get_Field(49c34f39-82d9-49c3-86ed-0176d17e3a9c))) AND
        GET_ANALVR(226eb77f-d010-4568-b39b-acbd649aa6c2)>=Get_Number(1) AND
        GET_ANALVR(f4f23edc-9d5d-47b7-95aa-5f2f7b2185b8)+GET_ANALVR(f48f853b-addf-4a1e-bd24-dd4c31f38a08)>Get_Number(30)
        AND LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C')
        )
```

<a id="e-b53af283-1f39-450c-8cc1-77cdbbe07cfb"></a>

## str_abfTRG_JOINT_REPLACE

Source: `RuntimeExpressions` / `b53af283-1f39-450c-8cc1-77cdbbe07cfb`.

Trigger for Joint Replace

Readable:
```text
IF(Get_Field(CULV_RATE)='N' AND IS_COMMITTED(),
    (
        Get_Field(COM_YEAR)=YR AND Get_Field(COM_TRT)='str_STR_MTCE' AND
        (
        Get_Field(COM_TRT_2)='str_JOINT_REPLACE' OR
        Get_Field(COM_TRT_3)='str_JOINT_REPLACE' OR 
        Get_Field(COM_TRT_4)='str_JOINT_REPLACE' OR
        Get_Field(COM_TRT_5)='str_JOINT_REPLACE')
    )
    OR
    (
        Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) =YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f) ='str_STR_MTCE' AND
        (
        Get_Field(ebbc3e10-5dd9-4e71-ad67-74b5ba13bfcd)='str_JOINT_REPLACE' OR
        Get_Field(39c10537-8525-4c42-acb9-d5d079549f51)='str_JOINT_REPLACE' OR 
        Get_Field(aa2bb7e0-c193-43a0-b873-55028a6b4a97)='str_JOINT_REPLACE' OR
        Get_Field(5aa4674b-28ab-45b4-9a3e-0046121321ba)='str_JOINT_REPLACE')
    ) 
    OR
    (
        Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) =YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e) ='str_STR_MTCE' AND
        (
        Get_Field(bc6e9d36-4cf4-4634-a7e3-bf7279551208)='str_JOINT_REPLACE' OR
        Get_Field(c8c4be3e-b718-4519-ab88-fdd18ef20e24)='str_JOINT_REPLACE' OR 
        Get_Field(8e11bd4b-a952-4f78-9eff-759dea0073da)='str_JOINT_REPLACE' OR
        Get_Field(026fe3ff-21d1-400d-a170-08962f1cd29e)='str_JOINT_REPLACE')
    )
    OR
    (
        Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) =YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066) ='str_STR_MTCE' AND
        (
        Get_Field(2203185a-fb64-4f8d-a076-d0d5f9ba0930)='str_JOINT_REPLACE' OR
        Get_Field(8e7c8042-efdf-412e-b812-68345b4440ce)='str_JOINT_REPLACE' OR 
        Get_Field(a1fcdfda-6c28-4c51-bcd6-952e671db7cd)='str_JOINT_REPLACE' OR
        Get_Field(d26a67bc-6d3c-4836-ac39-a694f421fbb3)='str_JOINT_REPLACE')
    )
    ,    Get_Field(CULV_RATE)='N' AND 
    (GET_ANALVR(str_nAAV_CND_DK)>=Get_Number(5.5) OR GET_ANALVR(str_nAAV_CND_DK) =-Get_Number(1)) AND
    (GET_ANALVR(str_nAAV_CND_SUP)>=Get_Number(5.5) OR GET_ANALVR(str_nAAV_CND_SUP) =-Get_Number(1)) AND
    (GET_ANALVR(str_nAAV_CND_SUB)>=Get_Number(5.5) OR GET_ANALVR(str_nAAV_CND_SUB) =-Get_Number(1)) AND
    Get_Exp(str_abfOBJ_JNT) AND
    ((GET_ANALVR(str_AAV_ELEM_300_CS3)+GET_ANALVR(str_AAV_ELEM_300_CS4))>Get_Number(20) OR 
    (GET_ANALVR(str_AAV_ELEM_301_CS3)+GET_ANALVR(str_AAV_ELEM_301_CS4))>Get_Number(20) OR   
    (GET_ANALVR(str_AAV_ELEM_302_CS3)+GET_ANALVR(str_AAV_ELEM_302_CS4))>Get_Number(20) OR 
    (GET_ANALVR(str_AAV_ELEM_303_CS3)+GET_ANALVR(str_AAV_ELEM_303_CS4))>Get_Number(20) OR 
    (GET_ANALVR(str_AAV_ELEM_304_CS3)+GET_ANALVR(str_AAV_ELEM_304_CS4))>Get_Number(20) OR
    (GET_ANALVR(str_AAV_ELEM_305_CS3)+GET_ANALVR(str_AAV_ELEM_305_CS4))>Get_Number(20) OR 
    (GET_ANALVR(str_AAV_ELEM_306_CS3)+GET_ANALVR(str_AAV_ELEM_306_CS4))>Get_Number(20))
    AND LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C')
```

Original:
```text
IF(Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' AND IS_COMMITTED(),
    (
        Get_Field(d62be030-874b-4177-9d41-e00645ac75d8)=YR AND Get_Field(30f7c9cd-b358-449a-9268-0e08a7acd1c0)='str_STR_MTCE' AND
        (
        Get_Field(4c06d943-9c6f-4f56-a854-8b32874f3150)='str_JOINT_REPLACE' OR
        Get_Field(42468b1b-19ff-4bb8-91be-d32a8a45006f)='str_JOINT_REPLACE' OR 
        Get_Field(131f88ca-12ec-4428-8f07-65bf2eec7eef)='str_JOINT_REPLACE' OR
        Get_Field(669eef45-c4e7-41d6-b434-ba2c1a49fb32)='str_JOINT_REPLACE')
    )
    OR
    (
        Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) =YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f) ='str_STR_MTCE' AND
        (
        Get_Field(ebbc3e10-5dd9-4e71-ad67-74b5ba13bfcd)='str_JOINT_REPLACE' OR
        Get_Field(39c10537-8525-4c42-acb9-d5d079549f51)='str_JOINT_REPLACE' OR 
        Get_Field(aa2bb7e0-c193-43a0-b873-55028a6b4a97)='str_JOINT_REPLACE' OR
        Get_Field(5aa4674b-28ab-45b4-9a3e-0046121321ba)='str_JOINT_REPLACE')
    ) 
    OR
    (
        Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) =YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e) ='str_STR_MTCE' AND
        (
        Get_Field(bc6e9d36-4cf4-4634-a7e3-bf7279551208)='str_JOINT_REPLACE' OR
        Get_Field(c8c4be3e-b718-4519-ab88-fdd18ef20e24)='str_JOINT_REPLACE' OR 
        Get_Field(8e11bd4b-a952-4f78-9eff-759dea0073da)='str_JOINT_REPLACE' OR
        Get_Field(026fe3ff-21d1-400d-a170-08962f1cd29e)='str_JOINT_REPLACE')
    )
    OR
    (
        Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) =YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066) ='str_STR_MTCE' AND
        (
        Get_Field(2203185a-fb64-4f8d-a076-d0d5f9ba0930)='str_JOINT_REPLACE' OR
        Get_Field(8e7c8042-efdf-412e-b812-68345b4440ce)='str_JOINT_REPLACE' OR 
        Get_Field(a1fcdfda-6c28-4c51-bcd6-952e671db7cd)='str_JOINT_REPLACE' OR
        Get_Field(d26a67bc-6d3c-4836-ac39-a694f421fbb3)='str_JOINT_REPLACE')
    )
    ,    Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' AND 
    (GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)>=Get_Number(5.5) OR GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903) =-Get_Number(1)) AND
    (GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)>=Get_Number(5.5) OR GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8) =-Get_Number(1)) AND
    (GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)>=Get_Number(5.5) OR GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2) =-Get_Number(1)) AND
    Get_Exp(af81cede-aef1-4772-88a8-e6c4af9320d8) AND
    ((GET_ANALVR(bb237542-c49f-47fc-8b30-5087beb8b3e7)+GET_ANALVR(f53ec4ee-84a2-4951-95d5-85645f3c610e))>Get_Number(20) OR 
    (GET_ANALVR(f708c328-863a-4123-858a-054acc31a694)+GET_ANALVR(8ca14d11-25c7-4066-8211-7ea26fc2c16d))>Get_Number(20) OR   
    (GET_ANALVR(24512d9d-1d93-4f4e-b2dc-01add4760b83)+GET_ANALVR(6ceafe1a-746f-454f-920b-aa2c1fdf4636))>Get_Number(20) OR 
    (GET_ANALVR(14583ddf-987a-4258-ad09-e2e34ef3767a)+GET_ANALVR(1348c087-28be-49ed-9b43-67895062ff57))>Get_Number(20) OR 
    (GET_ANALVR(ed7115cf-e74e-4b3c-bd80-6bf72d394a50)+GET_ANALVR(ec0a9854-38d7-467d-9b18-0b80f0d47b2a))>Get_Number(20) OR
    (GET_ANALVR(f175d017-bf6f-4ec4-ae5d-31a49b921363)+GET_ANALVR(8032a6bb-d289-475b-b7d5-02afa4f7c548))>Get_Number(20) OR 
    (GET_ANALVR(c347bb77-f366-42d3-86c3-7520131241fe)+GET_ANALVR(d157f99d-c22e-4037-89ca-36b004f0f4b7))>Get_Number(20))
    AND LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C')
```

<a id="e-b58df906-35cd-48c8-b38b-72594636e41e"></a>

## str_abfTRG_PAINT_REPLACE

Source: `RuntimeExpressions` / `b58df906-35cd-48c8-b38b-72594636e41e`.

Trigger Paint Replace Treatment

Readable:
```text
IF(Get_Field(CULV_RATE)='N' AND IS_COMMITTED(),
    (
        Get_Field(COM_YEAR)=YR AND Get_Field(COM_TRT)='str_STR_MTCE' AND
        (
        Get_Field(COM_TRT_2)='str_PAINT_REPLACE' OR
        Get_Field(COM_TRT_3)='str_PAINT_REPLACE' OR 
        Get_Field(COM_TRT_4)='str_PAINT_REPLACE' OR
        Get_Field(COM_TRT_5)='str_PAINT_REPLACE')
    )
    OR
    (
        Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) =YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f) ='str_STR_MTCE' AND
        (
        Get_Field(ebbc3e10-5dd9-4e71-ad67-74b5ba13bfcd)='str_PAINT_REPLACE' OR
        Get_Field(39c10537-8525-4c42-acb9-d5d079549f51)='str_PAINT_REPLACE' OR 
        Get_Field(aa2bb7e0-c193-43a0-b873-55028a6b4a97)='str_PAINT_REPLACE' OR
        Get_Field(5aa4674b-28ab-45b4-9a3e-0046121321ba)='str_PAINT_REPLACE')
    ) 
    OR
    (
        Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) =YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e) ='str_STR_MTCE' AND
        (
        Get_Field(bc6e9d36-4cf4-4634-a7e3-bf7279551208)='str_PAINT_REPLACE' OR
        Get_Field(c8c4be3e-b718-4519-ab88-fdd18ef20e24)='str_PAINT_REPLACE' OR 
        Get_Field(8e11bd4b-a952-4f78-9eff-759dea0073da)='str_PAINT_REPLACE' OR
        Get_Field(026fe3ff-21d1-400d-a170-08962f1cd29e)='str_PAINT_REPLACE')
    )
    OR
    (
        Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) =YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066) ='str_STR_MTCE' AND
        (
        Get_Field(2203185a-fb64-4f8d-a076-d0d5f9ba0930)='str_PAINT_REPLACE' OR
        Get_Field(8e7c8042-efdf-412e-b812-68345b4440ce)='str_PAINT_REPLACE' OR 
        Get_Field(a1fcdfda-6c28-4c51-bcd6-952e671db7cd)='str_PAINT_REPLACE' OR
        Get_Field(d26a67bc-6d3c-4836-ac39-a694f421fbb3)='str_PAINT_REPLACE')
    )
    ,    
    LEFT(Get_Field(NHS),Get_Number(1))='1' AND 
    Get_Field(CULV_RATE)='N' AND  
    (GET_ANALVR(str_nAAV_CND_DK)>Get_Number(5) OR GET_ANALVR(str_nAAV_CND_DK) =-Get_Number(1)) AND 
    (GET_ANALVR(str_nAAV_CND_SUP)>Get_Number(5) OR GET_ANALVR(str_nAAV_CND_SUP) =-Get_Number(1)) AND 
    (GET_ANALVR(str_nAAV_CND_SUB)>Get_Number(5) OR GET_ANALVR(str_nAAV_CND_SUB) =-Get_Number(1)) AND
    GET_ANALVR(str_AAV_ELEM_515_CS3)+GET_ANALVR(str_AAV_ELEM_515_CS4)>Get_Number(20)
    AND LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C')
```

Original:
```text
IF(Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' AND IS_COMMITTED(),
    (
        Get_Field(d62be030-874b-4177-9d41-e00645ac75d8)=YR AND Get_Field(30f7c9cd-b358-449a-9268-0e08a7acd1c0)='str_STR_MTCE' AND
        (
        Get_Field(4c06d943-9c6f-4f56-a854-8b32874f3150)='str_PAINT_REPLACE' OR
        Get_Field(42468b1b-19ff-4bb8-91be-d32a8a45006f)='str_PAINT_REPLACE' OR 
        Get_Field(131f88ca-12ec-4428-8f07-65bf2eec7eef)='str_PAINT_REPLACE' OR
        Get_Field(669eef45-c4e7-41d6-b434-ba2c1a49fb32)='str_PAINT_REPLACE')
    )
    OR
    (
        Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) =YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f) ='str_STR_MTCE' AND
        (
        Get_Field(ebbc3e10-5dd9-4e71-ad67-74b5ba13bfcd)='str_PAINT_REPLACE' OR
        Get_Field(39c10537-8525-4c42-acb9-d5d079549f51)='str_PAINT_REPLACE' OR 
        Get_Field(aa2bb7e0-c193-43a0-b873-55028a6b4a97)='str_PAINT_REPLACE' OR
        Get_Field(5aa4674b-28ab-45b4-9a3e-0046121321ba)='str_PAINT_REPLACE')
    ) 
    OR
    (
        Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) =YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e) ='str_STR_MTCE' AND
        (
        Get_Field(bc6e9d36-4cf4-4634-a7e3-bf7279551208)='str_PAINT_REPLACE' OR
        Get_Field(c8c4be3e-b718-4519-ab88-fdd18ef20e24)='str_PAINT_REPLACE' OR 
        Get_Field(8e11bd4b-a952-4f78-9eff-759dea0073da)='str_PAINT_REPLACE' OR
        Get_Field(026fe3ff-21d1-400d-a170-08962f1cd29e)='str_PAINT_REPLACE')
    )
    OR
    (
        Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) =YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066) ='str_STR_MTCE' AND
        (
        Get_Field(2203185a-fb64-4f8d-a076-d0d5f9ba0930)='str_PAINT_REPLACE' OR
        Get_Field(8e7c8042-efdf-412e-b812-68345b4440ce)='str_PAINT_REPLACE' OR 
        Get_Field(a1fcdfda-6c28-4c51-bcd6-952e671db7cd)='str_PAINT_REPLACE' OR
        Get_Field(d26a67bc-6d3c-4836-ac39-a694f421fbb3)='str_PAINT_REPLACE')
    )
    ,    
    LEFT(Get_Field(ff652eda-e73c-48a8-bd20-fd6e80950604),Get_Number(1))='1' AND 
    Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' AND  
    (GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)>Get_Number(5) OR GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903) =-Get_Number(1)) AND 
    (GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)>Get_Number(5) OR GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8) =-Get_Number(1)) AND 
    (GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)>Get_Number(5) OR GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2) =-Get_Number(1)) AND
    GET_ANALVR(7caba84c-5af2-4de1-aec3-c8cc44e239f9)+GET_ANALVR(45cc163b-7547-4c6f-a0fa-c952651c697c)>Get_Number(20)
    AND LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C')
```

<a id="e-7ab5a508-d805-4c80-8502-a329d8631b7a"></a>

## str_abfTRG_PAINT_SPOT

Source: `RuntimeExpressions` / `7ab5a508-d805-4c80-8502-a329d8631b7a`.

Trigger Spot Paint Treatment

Readable:
```text
IF(Get_Field(CULV_RATE)='N' AND IS_COMMITTED(),
    (
        Get_Field(COM_YEAR)=YR AND Get_Field(COM_TRT)='str_STR_MTCE' AND
        (
        Get_Field(COM_TRT_2)='str_PAINT_SPOT' OR
        Get_Field(COM_TRT_3)='str_PAINT_SPOT' OR 
        Get_Field(COM_TRT_4)='str_PAINT_SPOT' OR
        Get_Field(COM_TRT_5)='str_PAINT_SPOT')
    )
    OR
    (
        Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) =YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f) ='str_STR_MTCE' AND
        (
        Get_Field(ebbc3e10-5dd9-4e71-ad67-74b5ba13bfcd)='str_PAINT_SPOT' OR
        Get_Field(39c10537-8525-4c42-acb9-d5d079549f51)='str_PAINT_SPOT' OR 
        Get_Field(aa2bb7e0-c193-43a0-b873-55028a6b4a97)='str_PAINT_SPOT' OR
        Get_Field(5aa4674b-28ab-45b4-9a3e-0046121321ba)='str_PAINT_SPOT')
    ) 
    OR
    (
        Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) =YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e) ='str_STR_MTCE' AND
        (
        Get_Field(bc6e9d36-4cf4-4634-a7e3-bf7279551208)='str_PAINT_SPOT' OR
        Get_Field(c8c4be3e-b718-4519-ab88-fdd18ef20e24)='str_PAINT_SPOT' OR 
        Get_Field(8e11bd4b-a952-4f78-9eff-759dea0073da)='str_PAINT_SPOT' OR
        Get_Field(026fe3ff-21d1-400d-a170-08962f1cd29e)='str_PAINT_SPOT')
    )
    OR
    (
        Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) =YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066) ='str_STR_MTCE' AND
        (
        Get_Field(2203185a-fb64-4f8d-a076-d0d5f9ba0930)='str_PAINT_SPOT' OR
        Get_Field(8e7c8042-efdf-412e-b812-68345b4440ce)='str_PAINT_SPOT' OR 
        Get_Field(a1fcdfda-6c28-4c51-bcd6-952e671db7cd)='str_PAINT_SPOT' OR
        Get_Field(d26a67bc-6d3c-4836-ac39-a694f421fbb3)='str_PAINT_SPOT')
    )
    ,    LEFT(Get_Field(NHS),Get_Number(1))='1' AND 
    Get_Field(CULV_RATE)='N' AND 
    (GET_ANALVR(str_nAAV_CND_DK)>Get_Number(5) OR GET_ANALVR(str_nAAV_CND_DK)=-Get_Number(1)) AND 
    (GET_ANALVR(str_nAAV_CND_SUP)>Get_Number(5) OR GET_ANALVR(str_nAAV_CND_SUP)=-Get_Number(1)) AND 
    (GET_ANALVR(str_nAAV_CND_SUB)>Get_Number(5) OR GET_ANALVR(str_nAAV_CND_SUB)=-Get_Number(1)) AND 
    GET_ANALVR(str_AAV_ELEM_515_CS3)+GET_ANALVR(str_AAV_ELEM_515_CS4)>Get_Number(5) AND  
    GET_ANALVR(str_AAV_ELEM_515_CS3)+GET_ANALVR(str_AAV_ELEM_515_CS4)<=Get_Number(15) AND 
    GET_ANALVR(str_nDAV_CT_SPOT_PAINT)<=Get_Number(2)
    AND  LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C')
```

Original:
```text
IF(Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' AND IS_COMMITTED(),
    (
        Get_Field(d62be030-874b-4177-9d41-e00645ac75d8)=YR AND Get_Field(30f7c9cd-b358-449a-9268-0e08a7acd1c0)='str_STR_MTCE' AND
        (
        Get_Field(4c06d943-9c6f-4f56-a854-8b32874f3150)='str_PAINT_SPOT' OR
        Get_Field(42468b1b-19ff-4bb8-91be-d32a8a45006f)='str_PAINT_SPOT' OR 
        Get_Field(131f88ca-12ec-4428-8f07-65bf2eec7eef)='str_PAINT_SPOT' OR
        Get_Field(669eef45-c4e7-41d6-b434-ba2c1a49fb32)='str_PAINT_SPOT')
    )
    OR
    (
        Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) =YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f) ='str_STR_MTCE' AND
        (
        Get_Field(ebbc3e10-5dd9-4e71-ad67-74b5ba13bfcd)='str_PAINT_SPOT' OR
        Get_Field(39c10537-8525-4c42-acb9-d5d079549f51)='str_PAINT_SPOT' OR 
        Get_Field(aa2bb7e0-c193-43a0-b873-55028a6b4a97)='str_PAINT_SPOT' OR
        Get_Field(5aa4674b-28ab-45b4-9a3e-0046121321ba)='str_PAINT_SPOT')
    ) 
    OR
    (
        Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) =YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e) ='str_STR_MTCE' AND
        (
        Get_Field(bc6e9d36-4cf4-4634-a7e3-bf7279551208)='str_PAINT_SPOT' OR
        Get_Field(c8c4be3e-b718-4519-ab88-fdd18ef20e24)='str_PAINT_SPOT' OR 
        Get_Field(8e11bd4b-a952-4f78-9eff-759dea0073da)='str_PAINT_SPOT' OR
        Get_Field(026fe3ff-21d1-400d-a170-08962f1cd29e)='str_PAINT_SPOT')
    )
    OR
    (
        Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) =YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066) ='str_STR_MTCE' AND
        (
        Get_Field(2203185a-fb64-4f8d-a076-d0d5f9ba0930)='str_PAINT_SPOT' OR
        Get_Field(8e7c8042-efdf-412e-b812-68345b4440ce)='str_PAINT_SPOT' OR 
        Get_Field(a1fcdfda-6c28-4c51-bcd6-952e671db7cd)='str_PAINT_SPOT' OR
        Get_Field(d26a67bc-6d3c-4836-ac39-a694f421fbb3)='str_PAINT_SPOT')
    )
    ,    LEFT(Get_Field(ff652eda-e73c-48a8-bd20-fd6e80950604),Get_Number(1))='1' AND 
    Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' AND 
    (GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)>Get_Number(5) OR GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)=-Get_Number(1)) AND 
    (GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)>Get_Number(5) OR GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)=-Get_Number(1)) AND 
    (GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)>Get_Number(5) OR GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)=-Get_Number(1)) AND 
    GET_ANALVR(7caba84c-5af2-4de1-aec3-c8cc44e239f9)+GET_ANALVR(45cc163b-7547-4c6f-a0fa-c952651c697c)>Get_Number(5) AND  
    GET_ANALVR(7caba84c-5af2-4de1-aec3-c8cc44e239f9)+GET_ANALVR(45cc163b-7547-4c6f-a0fa-c952651c697c)<=Get_Number(15) AND 
    GET_ANALVR(524ce9e2-a329-4f01-b403-cb50182b7b7a)<=Get_Number(2)
    AND  LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C')
```

<a id="e-fbeef5d3-3fb2-4741-b641-094b73d676ff"></a>

## str_abfTRG_STRUCTURE_REPLACEMENT

Source: `RuntimeExpressions` / `fbeef5d3-3fb2-4741-b641-094b73d676ff`.

Trigger for Structure Replacement

Readable:
```text
IF(IS_COMMITTED(),
    (
        (Get_Field(COM_YEAR)=YR AND Get_Field(COM_TRT)='str_STRUCTURE_REPLACEMENT') OR
        (Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470)=YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f)='str_STRUCTURE_REPLACEMENT') OR
        (Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627)=YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e)='str_STRUCTURE_REPLACEMENT') OR
        (Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b)=YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066)='str_STRUCTURE_REPLACEMENT')
    )
    ,
    Get_Field(CULV_RATE)='N' AND 
    ((GET_ANALVR(str_nAAV_CND_SUP)<=Get_Number(5) AND GET_ANALVR(str_nAAV_CND_SUB)<=Get_Number(4) AND GET_ANALVR(str_nAAV_CND_DK)<=Get_Number(5)) 
    OR 
    (GET_ANALVR(str_nAAV_CND_SUB)<=Get_Number(3) AND GET_ANALVR(str_nAAV_CND_SUB) > -Get_Number(1) ) )
)
```

Original:
```text
IF(IS_COMMITTED(),
    (
        (Get_Field(d62be030-874b-4177-9d41-e00645ac75d8)=YR AND Get_Field(30f7c9cd-b358-449a-9268-0e08a7acd1c0)='str_STRUCTURE_REPLACEMENT') OR
        (Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470)=YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f)='str_STRUCTURE_REPLACEMENT') OR
        (Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627)=YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e)='str_STRUCTURE_REPLACEMENT') OR
        (Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b)=YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066)='str_STRUCTURE_REPLACEMENT')
    )
    ,
    Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' AND 
    ((GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)<=Get_Number(5) AND GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)<=Get_Number(4) AND GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)<=Get_Number(5)) 
    OR 
    (GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)<=Get_Number(3) AND GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2) > -Get_Number(1) ) )
)
```

<a id="e-7fc751cf-88f9-4a18-aacb-0cc1ccd50626"></a>

## str_abfTRG_STR_MTCE

Source: `RuntimeExpressions` / `7fc751cf-88f9-4a18-aacb-0cc1ccd50626`.

Trigger for Structure Maintenance

Readable:
```text
Get_Field(CULV_RATE)='N' 
AND 
(Get_Exp(str_abfTRG_DECK_SEAL) OR 
Get_Exp(str_abfTRG_DECK_OVERLAY) OR
Get_Exp(str_abfTRG_DECK_REPLACE) OR 
Get_Exp(str_abfTRG_DECK_PATCH) OR 
Get_Exp(str_abfTRG_DECK_REHAB) OR 
Get_Exp(str_abfTRG_SUPER_REHAB) OR 
Get_Exp(str_abfTRG_SUBSTRUCTURE_REHAB) OR 
Get_Exp(str_abfTRG_JOINT_REPLACE) OR 
Get_Exp(str_abfTRG_PAINT_SPOT) OR 
Get_Exp(str_abfTRG_PAINT_REPLACE))
AND LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C'
```

Original:
```text
Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' 
AND 
(Get_Exp(f2746237-bf2f-458a-a776-c6a246b5ca11) OR 
Get_Exp(efd94559-069c-4003-99b3-9adcbfed6a21) OR
Get_Exp(151050ed-3016-4c9b-9fb3-235cca9ca715) OR 
Get_Exp(1a105d30-6f2f-4869-9da7-0acdf2483d52) OR 
Get_Exp(531f547a-a5ea-4ab2-aa61-e23ff53484af) OR 
Get_Exp(cefe6466-a3a1-4109-98cd-1185b639ca28) OR 
Get_Exp(7fd185f5-dc4f-4451-8f7a-534aea3bb4b7) OR 
Get_Exp(b53af283-1f39-450c-8cc1-77cdbbe07cfb) OR 
Get_Exp(7ab5a508-d805-4c80-8502-a329d8631b7a) OR 
Get_Exp(b58df906-35cd-48c8-b38b-72594636e41e))
AND LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C'
```

<a id="e-7fd185f5-dc4f-4451-8f7a-534aea3bb4b7"></a>

## str_abfTRG_SUBSTRUCTURE_REHAB

Source: `RuntimeExpressions` / `7fd185f5-dc4f-4451-8f7a-534aea3bb4b7`.

Trigger for Substructure Rehabilitation

Readable:
```text
IF(Get_Field(CULV_RATE)='N' AND IS_COMMITTED(),
    (
        Get_Field(COM_YEAR)=YR AND (Get_Field(COM_TRT)='str_STR_MTCE' OR Get_Field(COM_TRT)='str_SUPER_REPLACEMENT') AND
        (
        Get_Field(COM_TRT_2)='str_SUBSTRUCTURE_REHAB' OR
        Get_Field(COM_TRT_3)='str_SUBSTRUCTURE_REHAB' OR 
        Get_Field(COM_TRT_4)='str_SUBSTRUCTURE_REHAB' OR
        Get_Field(COM_TRT_5)='str_SUBSTRUCTURE_REHAB')
    )
    OR
    (
        Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) =YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f) ='str_STR_MTCE' AND
        (
        Get_Field(ebbc3e10-5dd9-4e71-ad67-74b5ba13bfcd)='str_SUBSTRUCTURE_REHAB' OR
        Get_Field(39c10537-8525-4c42-acb9-d5d079549f51)='str_SUBSTRUCTURE_REHAB' OR 
        Get_Field(aa2bb7e0-c193-43a0-b873-55028a6b4a97)='str_SUBSTRUCTURE_REHAB' OR
        Get_Field(5aa4674b-28ab-45b4-9a3e-0046121321ba)='str_SUBSTRUCTURE_REHAB')
    ) 
    OR
    (
        Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) =YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e) ='str_STR_MTCE' AND
        (
        Get_Field(bc6e9d36-4cf4-4634-a7e3-bf7279551208)='str_SUBSTRUCTURE_REHAB' OR
        Get_Field(c8c4be3e-b718-4519-ab88-fdd18ef20e24)='str_SUBSTRUCTURE_REHAB' OR 
        Get_Field(8e11bd4b-a952-4f78-9eff-759dea0073da)='str_SUBSTRUCTURE_REHAB' OR
        Get_Field(026fe3ff-21d1-400d-a170-08962f1cd29e)='str_SUBSTRUCTURE_REHAB')
    )
    OR
    (
        Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) =YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066) ='str_STR_MTCE' AND
        (
        Get_Field(2203185a-fb64-4f8d-a076-d0d5f9ba0930)='str_SUBSTRUCTURE_REHAB' OR
        Get_Field(8e7c8042-efdf-412e-b812-68345b4440ce)='str_SUBSTRUCTURE_REHAB' OR 
        Get_Field(a1fcdfda-6c28-4c51-bcd6-952e671db7cd)='str_SUBSTRUCTURE_REHAB' OR
        Get_Field(d26a67bc-6d3c-4836-ac39-a694f421fbb3)='str_SUBSTRUCTURE_REHAB')
    )
    ,    
    Get_Field(CULV_RATE)='N' AND 
    GET_ANALVR(str_nAAV_CND_SUB)<=Get_Number(5) AND
    GET_ANALVR(str_nAAV_CND_SUB)> -Get_Number(1) AND
    (GET_ANALVR(str_nAAV_CND_SUP)>=Get_Number(5) OR GET_ANALVR(str_nAAV_CND_SUP)=-Get_Number(1)) AND
    (GET_ANALVR(str_nAAV_CND_DK)>=Get_Number(5) OR GET_ANALVR(str_nAAV_CND_DK)=-Get_Number(1)) AND 
    GET_ANALVR(str_nDAV_CT_SUB_REHAB)<Get_Number(1)
    AND LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C')
```

Original:
```text
IF(Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' AND IS_COMMITTED(),
    (
        Get_Field(d62be030-874b-4177-9d41-e00645ac75d8)=YR AND (Get_Field(30f7c9cd-b358-449a-9268-0e08a7acd1c0)='str_STR_MTCE' OR Get_Field(30f7c9cd-b358-449a-9268-0e08a7acd1c0)='str_SUPER_REPLACEMENT') AND
        (
        Get_Field(4c06d943-9c6f-4f56-a854-8b32874f3150)='str_SUBSTRUCTURE_REHAB' OR
        Get_Field(42468b1b-19ff-4bb8-91be-d32a8a45006f)='str_SUBSTRUCTURE_REHAB' OR 
        Get_Field(131f88ca-12ec-4428-8f07-65bf2eec7eef)='str_SUBSTRUCTURE_REHAB' OR
        Get_Field(669eef45-c4e7-41d6-b434-ba2c1a49fb32)='str_SUBSTRUCTURE_REHAB')
    )
    OR
    (
        Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) =YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f) ='str_STR_MTCE' AND
        (
        Get_Field(ebbc3e10-5dd9-4e71-ad67-74b5ba13bfcd)='str_SUBSTRUCTURE_REHAB' OR
        Get_Field(39c10537-8525-4c42-acb9-d5d079549f51)='str_SUBSTRUCTURE_REHAB' OR 
        Get_Field(aa2bb7e0-c193-43a0-b873-55028a6b4a97)='str_SUBSTRUCTURE_REHAB' OR
        Get_Field(5aa4674b-28ab-45b4-9a3e-0046121321ba)='str_SUBSTRUCTURE_REHAB')
    ) 
    OR
    (
        Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) =YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e) ='str_STR_MTCE' AND
        (
        Get_Field(bc6e9d36-4cf4-4634-a7e3-bf7279551208)='str_SUBSTRUCTURE_REHAB' OR
        Get_Field(c8c4be3e-b718-4519-ab88-fdd18ef20e24)='str_SUBSTRUCTURE_REHAB' OR 
        Get_Field(8e11bd4b-a952-4f78-9eff-759dea0073da)='str_SUBSTRUCTURE_REHAB' OR
        Get_Field(026fe3ff-21d1-400d-a170-08962f1cd29e)='str_SUBSTRUCTURE_REHAB')
    )
    OR
    (
        Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) =YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066) ='str_STR_MTCE' AND
        (
        Get_Field(2203185a-fb64-4f8d-a076-d0d5f9ba0930)='str_SUBSTRUCTURE_REHAB' OR
        Get_Field(8e7c8042-efdf-412e-b812-68345b4440ce)='str_SUBSTRUCTURE_REHAB' OR 
        Get_Field(a1fcdfda-6c28-4c51-bcd6-952e671db7cd)='str_SUBSTRUCTURE_REHAB' OR
        Get_Field(d26a67bc-6d3c-4836-ac39-a694f421fbb3)='str_SUBSTRUCTURE_REHAB')
    )
    ,    
    Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' AND 
    GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)<=Get_Number(5) AND
    GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)> -Get_Number(1) AND
    (GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)>=Get_Number(5) OR GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)=-Get_Number(1)) AND
    (GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)>=Get_Number(5) OR GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)=-Get_Number(1)) AND 
    GET_ANALVR(a8d41be9-a47c-453a-9945-05e09eca34fc)<Get_Number(1)
    AND LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C')
```

<a id="e-17b3bf91-eea0-427b-b4c1-376f99a2e2da"></a>

## str_abfTRG_SUPERSTRUCTURE_REPLACEMENT

Source: `RuntimeExpressions` / `17b3bf91-eea0-427b-b4c1-376f99a2e2da`.

Trigger for Superstructure Replacement

Readable:
```text

IF(IS_COMMITTED(),
    (
        (Get_Field(COM_YEAR)=YR AND Get_Field(COM_TRT)='str_SUPER_REPLACEMENT') OR
        (Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470)=YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f)='str_SUPER_REPLACEMENT') OR
        (Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627)=YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e)='str_SUPER_REPLACEMENT') OR
        (Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b)=YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066)='str_SUPER_REPLACEMENT')
    )
,
    Get_Field(CULV_RATE)='N' AND 
    (
    (
    GET_ANALVR(str_nAAV_CND_SUP)<=Get_Number(4) AND
    GET_ANALVR(str_nAAV_CND_SUP) > -Get_Number(1) AND 
    (GET_ANALVR(str_nAAV_CND_SUB)>=Get_Number(5) OR GET_ANALVR(str_nAAV_CND_SUB) =-Get_Number(1)) AND 
    (GET_ANALVR(str_nAAV_CND_DK)>=Get_Number(5) OR GET_ANALVR(str_nAAV_CND_DK)=-Get_Number(1))
    )
    OR 
    GET_ANALVR(str_nAAV_CND_SUP)<=Get_Number(3))
    AND NOT      Get_Exp(str_abfTRG_STRUCTURE_REPLACEMENT)
    AND LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C'
)
```

Original:
```text

IF(IS_COMMITTED(),
    (
        (Get_Field(d62be030-874b-4177-9d41-e00645ac75d8)=YR AND Get_Field(30f7c9cd-b358-449a-9268-0e08a7acd1c0)='str_SUPER_REPLACEMENT') OR
        (Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470)=YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f)='str_SUPER_REPLACEMENT') OR
        (Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627)=YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e)='str_SUPER_REPLACEMENT') OR
        (Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b)=YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066)='str_SUPER_REPLACEMENT')
    )
,
    Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' AND 
    (
    (
    GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)<=Get_Number(4) AND
    GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8) > -Get_Number(1) AND 
    (GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)>=Get_Number(5) OR GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2) =-Get_Number(1)) AND 
    (GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)>=Get_Number(5) OR GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)=-Get_Number(1))
    )
    OR 
    GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)<=Get_Number(3))
    AND NOT      Get_Exp(fbeef5d3-3fb2-4741-b641-094b73d676ff)
    AND LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C'
)
```

<a id="e-cefe6466-a3a1-4109-98cd-1185b639ca28"></a>

## str_abfTRG_SUPER_REHAB

Source: `RuntimeExpressions` / `cefe6466-a3a1-4109-98cd-1185b639ca28`.

Trigger for Superstructure Rehabilitation

Readable:
```text
IF(Get_Field(CULV_RATE)='N' AND IS_COMMITTED(),
    (
        Get_Field(COM_YEAR)=YR AND Get_Field(COM_TRT)='str_STR_MTCE' AND
        (
        Get_Field(COM_TRT_2)='str_SUPERSTRUCTURE_REHAB' OR
        Get_Field(COM_TRT_3)='str_SUPERSTRUCTURE_REHAB' OR 
        Get_Field(COM_TRT_4)='str_SUPERSTRUCTURE_REHAB' OR
        Get_Field(COM_TRT_5)='str_SUPERSTRUCTURE_REHAB')
    )
    OR
    (
        Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) =YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f) ='str_STR_MTCE' AND
        (
        Get_Field(ebbc3e10-5dd9-4e71-ad67-74b5ba13bfcd)='str_SUPERSTRUCTURE_REHAB' OR
        Get_Field(39c10537-8525-4c42-acb9-d5d079549f51)='str_SUPERSTRUCTURE_REHAB' OR 
        Get_Field(aa2bb7e0-c193-43a0-b873-55028a6b4a97)='str_SUPERSTRUCTURE_REHAB' OR
        Get_Field(5aa4674b-28ab-45b4-9a3e-0046121321ba)='str_SUPERSTRUCTURE_REHAB')
    ) 
    OR
    (
        Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) =YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e) ='str_STR_MTCE' AND
        (
        Get_Field(bc6e9d36-4cf4-4634-a7e3-bf7279551208)='str_SUPERSTRUCTURE_REHAB' OR
        Get_Field(c8c4be3e-b718-4519-ab88-fdd18ef20e24)='str_SUPERSTRUCTURE_REHAB' OR 
        Get_Field(8e11bd4b-a952-4f78-9eff-759dea0073da)='str_SUPERSTRUCTURE_REHAB' OR
        Get_Field(026fe3ff-21d1-400d-a170-08962f1cd29e)='str_SUPERSTRUCTURE_REHAB')
    )
    OR
    (
        Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) =YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066) ='str_STR_MTCE' AND
        (
        Get_Field(2203185a-fb64-4f8d-a076-d0d5f9ba0930)='str_SUPERSTRUCTURE_REHAB' OR
        Get_Field(8e7c8042-efdf-412e-b812-68345b4440ce)='str_SUPERSTRUCTURE_REHAB' OR 
        Get_Field(a1fcdfda-6c28-4c51-bcd6-952e671db7cd)='str_SUPERSTRUCTURE_REHAB' OR
        Get_Field(d26a67bc-6d3c-4836-ac39-a694f421fbb3)='str_SUPERSTRUCTURE_REHAB')
    )
    ,    
    Get_Field(CULV_RATE)='N' AND 
    GET_ANALVR(str_nAAV_CND_SUP)<=Get_Number(5) AND
    GET_ANALVR(str_nAAV_CND_SUP)> -Get_Number(1) AND
    (GET_ANALVR(str_nAAV_CND_SUB)>=Get_Number(5) OR GET_ANALVR(str_nAAV_CND_SUB)=-Get_Number(1)) AND
    (GET_ANALVR(str_nAAV_CND_DK)>=Get_Number(5) OR GET_ANALVR(str_nAAV_CND_DK)=-Get_Number(1)) AND
    GET_ANALVR(str_nDAV_CT_SUPER_REHAB)<Get_Number(1)
    AND LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C')
```

Original:
```text
IF(Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' AND IS_COMMITTED(),
    (
        Get_Field(d62be030-874b-4177-9d41-e00645ac75d8)=YR AND Get_Field(30f7c9cd-b358-449a-9268-0e08a7acd1c0)='str_STR_MTCE' AND
        (
        Get_Field(4c06d943-9c6f-4f56-a854-8b32874f3150)='str_SUPERSTRUCTURE_REHAB' OR
        Get_Field(42468b1b-19ff-4bb8-91be-d32a8a45006f)='str_SUPERSTRUCTURE_REHAB' OR 
        Get_Field(131f88ca-12ec-4428-8f07-65bf2eec7eef)='str_SUPERSTRUCTURE_REHAB' OR
        Get_Field(669eef45-c4e7-41d6-b434-ba2c1a49fb32)='str_SUPERSTRUCTURE_REHAB')
    )
    OR
    (
        Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) =YR AND Get_Field(b935a9a4-c904-4979-9458-c7496c505d8f) ='str_STR_MTCE' AND
        (
        Get_Field(ebbc3e10-5dd9-4e71-ad67-74b5ba13bfcd)='str_SUPERSTRUCTURE_REHAB' OR
        Get_Field(39c10537-8525-4c42-acb9-d5d079549f51)='str_SUPERSTRUCTURE_REHAB' OR 
        Get_Field(aa2bb7e0-c193-43a0-b873-55028a6b4a97)='str_SUPERSTRUCTURE_REHAB' OR
        Get_Field(5aa4674b-28ab-45b4-9a3e-0046121321ba)='str_SUPERSTRUCTURE_REHAB')
    ) 
    OR
    (
        Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) =YR AND Get_Field(17eaf42f-ffdc-48af-a2f7-98da2eb7ed7e) ='str_STR_MTCE' AND
        (
        Get_Field(bc6e9d36-4cf4-4634-a7e3-bf7279551208)='str_SUPERSTRUCTURE_REHAB' OR
        Get_Field(c8c4be3e-b718-4519-ab88-fdd18ef20e24)='str_SUPERSTRUCTURE_REHAB' OR 
        Get_Field(8e11bd4b-a952-4f78-9eff-759dea0073da)='str_SUPERSTRUCTURE_REHAB' OR
        Get_Field(026fe3ff-21d1-400d-a170-08962f1cd29e)='str_SUPERSTRUCTURE_REHAB')
    )
    OR
    (
        Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) =YR AND Get_Field(7b1fa0de-7e17-4fd1-b34a-42d87c5e2066) ='str_STR_MTCE' AND
        (
        Get_Field(2203185a-fb64-4f8d-a076-d0d5f9ba0930)='str_SUPERSTRUCTURE_REHAB' OR
        Get_Field(8e7c8042-efdf-412e-b812-68345b4440ce)='str_SUPERSTRUCTURE_REHAB' OR 
        Get_Field(a1fcdfda-6c28-4c51-bcd6-952e671db7cd)='str_SUPERSTRUCTURE_REHAB' OR
        Get_Field(d26a67bc-6d3c-4836-ac39-a694f421fbb3)='str_SUPERSTRUCTURE_REHAB')
    )
    ,    
    Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N' AND 
    GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)<=Get_Number(5) AND
    GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)> -Get_Number(1) AND
    (GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)>=Get_Number(5) OR GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)=-Get_Number(1)) AND
    (GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)>=Get_Number(5) OR GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)=-Get_Number(1)) AND
    GET_ANALVR(bf187931-c39d-452c-8f15-8754771e30cf)<Get_Number(1)
    AND LEFT(Get_Field(a0050ddd-04d3-434f-936b-edfe6eee815f),Get_Number(1)) <>'C')
```

<a id="e-31d489ca-a200-4b4e-88f0-2e6ec80d039d"></a>

## str_ancAGE_DECK

Source: `RuntimeExpressions` / `31d489ca-a200-4b4e-88f0-2e6ec80d039d`.

Deck Age

Readable:
```text
IF(GET_ANALVR(str_nAAV_AGE_DECK)<Get_Number(0),GET_ANALVR(str_nAAV_AGE_DECK),GET_ANALVR(str_nAAV_AGE_DECK)+Get_Number(1))
```

Original:
```text
IF(GET_ANALVR(95344405-5ad1-4b61-b8c1-ec673596fb16)<Get_Number(0),GET_ANALVR(95344405-5ad1-4b61-b8c1-ec673596fb16),GET_ANALVR(95344405-5ad1-4b61-b8c1-ec673596fb16)+Get_Number(1))
```

<a id="e-e0716548-80b6-4a91-9a85-f256e44c214e"></a>

## str_ancAGE_DECK_INITIALIZE

Source: `dTIMSExpressions` / `e0716548-80b6-4a91-9a85-f256e44c214e`.

Initialize the Deck age

Readable:
```text
IF(IFDEFAULT(Get_Field(AGE_DECK)) OR Get_Field(DECK_RATE)='N',-Get_Number(1),Get_Field(AGE_DECK))
```

Original:
```text
IF(IFDEFAULT(Get_Field(c1c27ae0-784e-48a7-bab9-e95cce8e32a3)) OR Get_Field(a945c2eb-6da7-474a-9578-818228787db6)='N',-Get_Number(1),Get_Field(c1c27ae0-784e-48a7-bab9-e95cce8e32a3))
```

<a id="e-eaeaa13f-edf8-4629-a812-bb457bff4b0b"></a>

## str_ancAGE_JOINT

Source: `RuntimeExpressions` / `eaeaa13f-edf8-4629-a812-bb457bff4b0b`.

Joint Age

Readable:
```text
IF(GET_ANALVR(str_nAAV_AGE_JT)< Get_Number(0), GET_ANALVR(str_nAAV_AGE_JT),GET_ANALVR(str_nAAV_AGE_JT)+Get_Number(1))
```

Original:
```text
IF(GET_ANALVR(020c1fda-e1fb-4392-bf66-2e3d63e765fc)< Get_Number(0), GET_ANALVR(020c1fda-e1fb-4392-bf66-2e3d63e765fc),GET_ANALVR(020c1fda-e1fb-4392-bf66-2e3d63e765fc)+Get_Number(1))
```

<a id="e-c477c7f9-9230-473b-801d-4cd60802fd3e"></a>

## str_ancAGE_JOINT_INITIALIZE

Source: `dTIMSExpressions` / `c477c7f9-9230-473b-801d-4cd60802fd3e`.

Initialize the Joint age

Readable:
```text
IF(IFDEFAULT(Get_Field(AGE_JOINTS)),-Get_Number(1),Get_Field(AGE_JOINTS))    
```

Original:
```text
IF(IFDEFAULT(Get_Field(fbb754ec-917e-48e2-a9e2-90ef9bd5d32a)),-Get_Number(1),Get_Field(fbb754ec-917e-48e2-a9e2-90ef9bd5d32a))    
```

<a id="e-7d857d75-8323-48b3-a77d-24858636f67b"></a>

## str_ancAGE_PAINT

Source: `RuntimeExpressions` / `7d857d75-8323-48b3-a77d-24858636f67b`.

Paint Age

Readable:
```text
IF(GET_ANALVR(str_nAAV_AGE_PT)< Get_Number(0), GET_ANALVR(str_nAAV_AGE_PT),GET_ANALVR(str_nAAV_AGE_PT)+Get_Number(1))
```

Original:
```text
IF(GET_ANALVR(2429de8f-4fad-48f9-9dc1-dd77477d9ced)< Get_Number(0), GET_ANALVR(2429de8f-4fad-48f9-9dc1-dd77477d9ced),GET_ANALVR(2429de8f-4fad-48f9-9dc1-dd77477d9ced)+Get_Number(1))
```

<a id="e-68f00d6f-74a3-4a9a-8ec2-d552eae4c082"></a>

## str_ancAGE_PAINT_INITIALIZE

Source: `dTIMSExpressions` / `68f00d6f-74a3-4a9a-8ec2-d552eae4c082`.

Initialize the Paint age

Readable:
```text
IF(IFDEFAULT(Get_Field(AGE_PAINT)),-Get_Number(1),Get_Field(AGE_PAINT))    
```

Original:
```text
IF(IFDEFAULT(Get_Field(0b83499c-e39c-47c3-ba2f-645cf61e39b6)),-Get_Number(1),Get_Field(0b83499c-e39c-47c3-ba2f-645cf61e39b6))    
```

<a id="e-76bee3f3-2148-4a9d-a4e1-800ed77aea03"></a>

## str_ancAGE_WS

Source: `RuntimeExpressions` / `76bee3f3-2148-4a9d-a4e1-800ed77aea03`.

Wearing Surface Age

Readable:
```text
IF(GET_ANALVR(str_nAAV_AGE_WS)< Get_Number(0), GET_ANALVR(str_nAAV_AGE_WS),GET_ANALVR(str_nAAV_AGE_WS)+Get_Number(1))
```

Original:
```text
IF(GET_ANALVR(226eb77f-d010-4568-b39b-acbd649aa6c2)< Get_Number(0), GET_ANALVR(226eb77f-d010-4568-b39b-acbd649aa6c2),GET_ANALVR(226eb77f-d010-4568-b39b-acbd649aa6c2)+Get_Number(1))
```

<a id="e-01ff580f-135c-4592-a7fd-fe0bcd1faaf9"></a>

## str_ancAGE_WSURF_INITIALIZE

Source: `dTIMSExpressions` / `01ff580f-135c-4592-a7fd-fe0bcd1faaf9`.

Initialize the Wearing Surface age

Readable:
```text
IF(IFDEFAULT(Get_Field(AGE_WEARING_SURFACE)),-Get_Number(1),Get_Field(AGE_WEARING_SURFACE))
    
```

Original:
```text
IF(IFDEFAULT(Get_Field(c7a24a6a-766d-4fca-b26e-f1653de907bd)),-Get_Number(1),Get_Field(c7a24a6a-766d-4fca-b26e-f1653de907bd))
    
```

<a id="e-3ce9d44b-5083-4a8b-9461-39ec73ab58de"></a>

## str_ancCND_CCR

Source: `RuntimeExpressions` / `3ce9d44b-5083-4a8b-9461-39ec73ab58de`.

Composite Condition Rating 

Readable:
```text
IF(Get_Field(CULV_RATE) <> 'N',
    GET_ANALVR(str_nAAV_CND_CVT) * Get_Number(1)
    ,
    GET_ANALVR(str_nAAV_CND_DK) * Get_Number(0.3) +
    GET_ANALVR(str_nAAV_CND_SUP) * Get_Number(0.35) +  
    GET_ANALVR(str_nAAV_CND_SUB) * Get_Number(0.35)
)

//change 2026-05-08 - all the values were the same and this needs to be totally redone
//IF(Bridge->STRUCTURE_TYPE ='11',
//    IF(Bridge->STRUCTURE_MATERIAL='1',
//        str_nAAV_CND_CVT * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','CVT','KEY','111',TRUE)) +
//        str_nAAV_CND_DK * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','DK','KEY','111',TRUE)) +
//        str_nAAV_CND_SUP * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUP','KEY','111',TRUE)) +  
//        str_nAAV_CND_SUB * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUB','KEY','111',TRUE)) 
//        ,
//           IF(Bridge->STRUCTURE_MATERIAL='9',
//                str_nAAV_CND_CVT * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','CVT','KEY','119',TRUE)) +
//                str_nAAV_CND_DK * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','DK','KEY','119',TRUE)) +
//                str_nAAV_CND_SUP * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUP','KEY','119',TRUE)) +  
//                str_nAAV_CND_SUB * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUB','KEY','119',TRUE))
//                ,
//                str_nAAV_CND_CVT * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','CVT','KEY','118',TRUE)) +
//                str_nAAV_CND_DK * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','DK','KEY','118',TRUE)) +
//                str_nAAV_CND_SUP * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUP','KEY','118',TRUE)) +  
//                str_nAAV_CND_SUB * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUB','KEY','118',TRUE))
//            )
//        )
//,
//str_nAAV_CND_CVT * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','CVT','KEY',Bridge->STRUCTURE_TYPE,TRUE)) +
//str_nAAV_CND_DK * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','DK','KEY',Bridge->STRUCTURE_TYPE,TRUE)) +
//str_nAAV_CND_SUP * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUP','KEY',Bridge->STRUCTURE_TYPE,TRUE)) +  
//str_nAAV_CND_SUB * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUB','KEY',Bridge->STRUCTURE_TYPE,TRUE)) 
//)
//IF(Bridge->STRUCTURE_TYPE ='11',
//    IF(Bridge->STRUCTURE_MATERIAL='1',
//        str_nAAV_CND_CVT * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','CVT','KEY','111',TRUE)) +
//        str_nAAV_CND_DK * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','DK','KEY','111',TRUE)) +
//        str_nAAV_CND_SUP * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUP','KEY','111',TRUE)) +  
//        str_nAAV_CND_SUB * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUB','KEY','111',TRUE)) 
//        ,
//           IF(Bridge->STRUCTURE_MATERIAL='9',
//                str_nAAV_CND_CVT * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','CVT','KEY','119',TRUE)) +
//                str_nAAV_CND_DK * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','DK','KEY','119',TRUE)) +
//                str_nAAV_CND_SUP * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUP','KEY','119',TRUE)) +  
//                str_nAAV_CND_SUB * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUB','KEY','119',TRUE))
//                ,
//                str_nAAV_CND_CVT * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','CVT','KEY','118',TRUE)) +
//                str_nAAV_CND_DK * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','DK','KEY','118',TRUE)) +
//                str_nAAV_CND_SUP * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUP','KEY','118',TRUE)) +  
//                str_nAAV_CND_SUB * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUB','KEY','118',TRUE))
//            )
//        )
//,
//str_nAAV_CND_CVT * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','CVT','KEY',Bridge->STRUCTURE_TYPE,TRUE)) +
//str_nAAV_CND_DK * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','DK','KEY',Bridge->STRUCTURE_TYPE,TRUE)) +
//str_nAAV_CND_SUP * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUP','KEY',Bridge->STRUCTURE_TYPE,TRUE)) +  
//str_nAAV_CND_SUB * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUB','KEY',Bridge->STRUCTURE_TYPE,TRUE)) 
//)
```

Original:
```text
IF(Get_Field(176ba749-8358-42b7-97b0-5fe542dac530) <> 'N',
    GET_ANALVR(fb31bbaf-26dc-4b1f-9e1b-31000f7ee770) * Get_Number(1)
    ,
    GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903) * Get_Number(0.3) +
    GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8) * Get_Number(0.35) +  
    GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2) * Get_Number(0.35)
)

//change 2026-05-08 - all the values were the same and this needs to be totally redone
//IF(Bridge->STRUCTURE_TYPE ='11',
//    IF(Bridge->STRUCTURE_MATERIAL='1',
//        str_nAAV_CND_CVT * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','CVT','KEY','111',TRUE)) +
//        str_nAAV_CND_DK * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','DK','KEY','111',TRUE)) +
//        str_nAAV_CND_SUP * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUP','KEY','111',TRUE)) +  
//        str_nAAV_CND_SUB * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUB','KEY','111',TRUE)) 
//        ,
//           IF(Bridge->STRUCTURE_MATERIAL='9',
//                str_nAAV_CND_CVT * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','CVT','KEY','119',TRUE)) +
//                str_nAAV_CND_DK * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','DK','KEY','119',TRUE)) +
//                str_nAAV_CND_SUP * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUP','KEY','119',TRUE)) +  
//                str_nAAV_CND_SUB * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUB','KEY','119',TRUE))
//                ,
//                str_nAAV_CND_CVT * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','CVT','KEY','118',TRUE)) +
//                str_nAAV_CND_DK * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','DK','KEY','118',TRUE)) +
//                str_nAAV_CND_SUP * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUP','KEY','118',TRUE)) +  
//                str_nAAV_CND_SUB * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUB','KEY','118',TRUE))
//            )
//        )
//,
//str_nAAV_CND_CVT * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','CVT','KEY',Bridge->STRUCTURE_TYPE,TRUE)) +
//str_nAAV_CND_DK * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','DK','KEY',Bridge->STRUCTURE_TYPE,TRUE)) +
//str_nAAV_CND_SUP * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUP','KEY',Bridge->STRUCTURE_TYPE,TRUE)) +  
//str_nAAV_CND_SUB * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUB','KEY',Bridge->STRUCTURE_TYPE,TRUE)) 
//)
//IF(Bridge->STRUCTURE_TYPE ='11',
//    IF(Bridge->STRUCTURE_MATERIAL='1',
//        str_nAAV_CND_CVT * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','CVT','KEY','111',TRUE)) +
//        str_nAAV_CND_DK * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','DK','KEY','111',TRUE)) +
//        str_nAAV_CND_SUP * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUP','KEY','111',TRUE)) +  
//        str_nAAV_CND_SUB * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUB','KEY','111',TRUE)) 
//        ,
//           IF(Bridge->STRUCTURE_MATERIAL='9',
//                str_nAAV_CND_CVT * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','CVT','KEY','119',TRUE)) +
//                str_nAAV_CND_DK * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','DK','KEY','119',TRUE)) +
//                str_nAAV_CND_SUP * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUP','KEY','119',TRUE)) +  
//                str_nAAV_CND_SUB * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUB','KEY','119',TRUE))
//                ,
//                str_nAAV_CND_CVT * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','CVT','KEY','118',TRUE)) +
//                str_nAAV_CND_DK * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','DK','KEY','118',TRUE)) +
//                str_nAAV_CND_SUP * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUP','KEY','118',TRUE)) +  
//                str_nAAV_CND_SUB * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUB','KEY','118',TRUE))
//            )
//        )
//,
//str_nAAV_CND_CVT * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','CVT','KEY',Bridge->STRUCTURE_TYPE,TRUE)) +
//str_nAAV_CND_DK * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','DK','KEY',Bridge->STRUCTURE_TYPE,TRUE)) +
//str_nAAV_CND_SUP * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUP','KEY',Bridge->STRUCTURE_TYPE,TRUE)) +  
//str_nAAV_CND_SUB * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CCR_Weights','SUB','KEY',Bridge->STRUCTURE_TYPE,TRUE)) 
//)
```

<a id="e-c84c19b6-6e15-4f27-91f5-11f668a38606"></a>

## str_ancCND_CCR_WEIGHT

Source: `RuntimeExpressions` / `c84c19b6-6e15-4f27-91f5-11f668a38606`.

Compostie Condition Index Weight

Readable:
```text
IF(GET_ANALVR(str_nAAV_TRF_ADT)<=Get_Number(30),
Get_Number(0.1),
IF(GET_ANALVR(str_nAAV_TRF_ADT)>=Get_Number(10000),
Get_Number(1),
Get_Number(0.1405)*LOG(GET_ANALVR(str_nAAV_TRF_ADT))-Get_Number(0.3856)
)
)
```

Original:
```text
IF(GET_ANALVR(5354dc5d-c869-4579-8ae4-eb60a9c12614)<=Get_Number(30),
Get_Number(0.1),
IF(GET_ANALVR(5354dc5d-c869-4579-8ae4-eb60a9c12614)>=Get_Number(10000),
Get_Number(1),
Get_Number(0.1405)*LOG(GET_ANALVR(5354dc5d-c869-4579-8ae4-eb60a9c12614))-Get_Number(0.3856)
)
)
```

<a id="e-bc468763-d27e-451d-966f-2f6d53434d32"></a>

## str_ancCND_CULV_INITIALIZE

Source: `dTIMSExpressions` / `bc468763-d27e-451d-966f-2f6d53434d32`.

Initialize the Culvert Condition Rating

Readable:
```text
IF(Get_Field(CULV_RATE) ='N',-Get_Number(1),VAL(Get_Field(CULV_RATE)))
    
```

Original:
```text
IF(Get_Field(176ba749-8358-42b7-97b0-5fe542dac530) ='N',-Get_Number(1),VAL(Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)))
    
```

<a id="e-586beb4a-c36d-40cc-af16-3ef538f3ec43"></a>

## str_ancCND_CVT

Source: `RuntimeExpressions` / `586beb4a-c36d-40cc-af16-3ef538f3ec43`.

Culvert Condition Rating

Readable:
```text
IF(Get_Field(CULV_RATE)='N',-Get_Number(1),
IF(LEFT(Get_Field(STRUCTURE_MATERIAL),Get_Number(1)) ='S',
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CR_Life','YR'+SUBSTR(LTRIM(RTRIM(STR(Get_Number(100)+MAX(GET_ANALVR(str_nAAV_CND_CVT_COUNTER),Get_Number(0))))),Get_Number(2),Get_Number(2)),'KEY','CUL_S_'+GET_ANALVR(str_tDAV_CVT_MARKOV),TRUE))
,
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CR_Life','YR'+SUBSTR(LTRIM(RTRIM(STR(Get_Number(100)+MAX(GET_ANALVR(str_nAAV_CND_CVT_COUNTER),Get_Number(0))))),Get_Number(2),Get_Number(2)),'KEY','CUL_C_'+GET_ANALVR(str_tDAV_CVT_MARKOV),TRUE))
)
)
```

Original:
```text
IF(Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N',-Get_Number(1),
IF(LEFT(Get_Field(c51519d3-b3df-4130-82e8-70433ec40976),Get_Number(1)) ='S',
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CR_Life','YR'+SUBSTR(LTRIM(RTRIM(STR(Get_Number(100)+MAX(GET_ANALVR(b43e1666-bfe2-4e21-9d2d-c3c258517768),Get_Number(0))))),Get_Number(2),Get_Number(2)),'KEY','CUL_S_'+GET_ANALVR(cb2d765e-8767-485f-ade6-1aa539cc9b09),TRUE))
,
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CR_Life','YR'+SUBSTR(LTRIM(RTRIM(STR(Get_Number(100)+MAX(GET_ANALVR(b43e1666-bfe2-4e21-9d2d-c3c258517768),Get_Number(0))))),Get_Number(2),Get_Number(2)),'KEY','CUL_C_'+GET_ANALVR(cb2d765e-8767-485f-ade6-1aa539cc9b09),TRUE))
)
)
```

<a id="e-775a390c-8bcc-471c-8d1f-eaa45ddb2274"></a>

## str_ancCND_CVT_COUNTER

Source: `RuntimeExpressions` / `775a390c-8bcc-471c-8d1f-eaa45ddb2274`.

Culvert Counter

Readable:
```text
IF(GET_ANALVR(str_nAAV_CND_CVT_LIFE)>Get_Number(0) OR GET_ANALVR(str_nAAV_CND_CVT_COUNTER)<Get_Number(0),GET_ANALVR(str_nAAV_CND_CVT_COUNTER),MIN(GET_ANALVR(str_nAAV_CND_CVT_COUNTER)+Get_Number(1),Get_Number(50)))
```

Original:
```text
IF(GET_ANALVR(6a4e10ff-cfa7-4a87-bd6f-e74531434ec0)>Get_Number(0) OR GET_ANALVR(b43e1666-bfe2-4e21-9d2d-c3c258517768)<Get_Number(0),GET_ANALVR(b43e1666-bfe2-4e21-9d2d-c3c258517768),MIN(GET_ANALVR(b43e1666-bfe2-4e21-9d2d-c3c258517768)+Get_Number(1),Get_Number(50)))
```

<a id="e-33a2bfc2-4016-4df9-8f4d-7a7dd652278e"></a>

## str_ancCND_CVT_COUNTER_INITIALIZE

Source: `dTIMSExpressions` / `33a2bfc2-4016-4df9-8f4d-7a7dd652278e`.

Initialize the Culvert Counter

Readable:
```text
IF(Get_Field(CULV_RATE)='N',-Get_Number(1),Get_Field(COUNTER_INIT_CULVERT))
```

Original:
```text
IF(Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N',-Get_Number(1),Get_Field(88392ec0-77e7-49f6-8403-479bca927149))
```

<a id="e-c1535fea-ff90-4e0e-9c72-1d93d0c2c305"></a>

## str_ancCND_CVT_LIFE

Source: `RuntimeExpressions` / `c1535fea-ff90-4e0e-9c72-1d93d0c2c305`.

Culvert Life Deterioration

Readable:
```text
IF(GET_ANALVR(str_nAAV_CND_CVT_LIFE)>Get_Number(0),GET_ANALVR(str_nAAV_CND_CVT_LIFE)-Get_Number(1),Get_Number(0))
```

Original:
```text
IF(GET_ANALVR(6a4e10ff-cfa7-4a87-bd6f-e74531434ec0)>Get_Number(0),GET_ANALVR(6a4e10ff-cfa7-4a87-bd6f-e74531434ec0)-Get_Number(1),Get_Number(0))
```

<a id="e-675027b5-2cf5-4c0e-8372-201937c8bebc"></a>

## str_ancCND_CVT_LIFE_INITIALIZE

Source: `dTIMSExpressions` / `675027b5-2cf5-4c0e-8372-201937c8bebc`.

Initialize the Culvert Life

Readable:
```text
Get_Number(0)
```

Original:
```text
Get_Number(0)
```

<a id="e-65401d9e-7723-4c4c-a984-e91bcc29014f"></a>

## str_ancCND_CVT_MARKOV

Source: `dTIMSExpressions` / `65401d9e-7723-4c4c-a984-e91bcc29014f`.

Deck Markov Variable to initialize which deterioration curve to use.  Set to the value of the original deck rating.

Readable:
```text
IF(Get_Field(CULV_RATE)='N','1',Get_Field(CULV_RATE))
```

Original:
```text
IF(Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N','1',Get_Field(176ba749-8358-42b7-97b0-5fe542dac530))
```

<a id="e-91164d27-0370-4723-8e7c-bfc9c7be72c3"></a>

## str_ancCND_DECK

Source: `RuntimeExpressions` / `91164d27-0370-4723-8e7c-bfc9c7be72c3`.

Deck Condition Rating

Readable:
```text
IF(Get_Field(CULV_RATE)<>'N' OR (Get_Field(DECK_RATE) ='N' AND YR=Get_Number(1)) OR GET_ANALVR(str_nAAV_CND_DK)=-Get_Number(1),-Get_Number(1),
IF(LEFT(Get_Field(WEARING_SURFACE_DECK_PROTECTION),Get_Number(1)) <>'0',
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CR_Life','YR'+SUBSTR(LTRIM(RTRIM(STR(Get_Number(100)+MAX(GET_ANALVR(str_nAAV_CND_DK_COUNTER),Get_Number(0))))),Get_Number(2),Get_Number(2)),'KEY','DCK_P_'+GET_ANALVR(str_tDAV_DECK_MARKOV),TRUE))
,
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CR_Life','YR'+SUBSTR(LTRIM(RTRIM(STR(Get_Number(100)+MAX(GET_ANALVR(str_nAAV_CND_DK_COUNTER),Get_Number(0))))),Get_Number(2),Get_Number(2)),'KEY','DCK_'+GET_ANALVR(str_tDAV_DECK_MARKOV),TRUE))
)
)
```

Original:
```text
IF(Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)<>'N' OR (Get_Field(a945c2eb-6da7-474a-9578-818228787db6) ='N' AND YR=Get_Number(1)) OR GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)=-Get_Number(1),-Get_Number(1),
IF(LEFT(Get_Field(2136885d-b660-4e28-95a7-ba16d67837da),Get_Number(1)) <>'0',
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CR_Life','YR'+SUBSTR(LTRIM(RTRIM(STR(Get_Number(100)+MAX(GET_ANALVR(192db204-710e-481c-a984-71a262984b6f),Get_Number(0))))),Get_Number(2),Get_Number(2)),'KEY','DCK_P_'+GET_ANALVR(fd77f23e-cf7d-4b1d-8cb6-6476101d80c0),TRUE))
,
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CR_Life','YR'+SUBSTR(LTRIM(RTRIM(STR(Get_Number(100)+MAX(GET_ANALVR(192db204-710e-481c-a984-71a262984b6f),Get_Number(0))))),Get_Number(2),Get_Number(2)),'KEY','DCK_'+GET_ANALVR(fd77f23e-cf7d-4b1d-8cb6-6476101d80c0),TRUE))
)
)
```

<a id="e-0c813358-57c7-4628-9769-4399737e4bf1"></a>

## str_ancCND_DECK_COUNTER

Source: `RuntimeExpressions` / `0c813358-57c7-4628-9769-4399737e4bf1`.

Deck Counter

Readable:
```text
IF(GET_ANALVR(str_nAAV_CND_DK_LIFE)>Get_Number(0) OR GET_ANALVR(str_nAAV_CND_DK_COUNTER) <Get_Number(0),GET_ANALVR(str_nAAV_CND_DK_COUNTER),MIN(GET_ANALVR(str_nAAV_CND_DK_COUNTER) + Get_Number(1),Get_Number(50)))
```

Original:
```text
IF(GET_ANALVR(27eddee2-190d-4175-ba2f-ed3bfa8ecb75)>Get_Number(0) OR GET_ANALVR(192db204-710e-481c-a984-71a262984b6f) <Get_Number(0),GET_ANALVR(192db204-710e-481c-a984-71a262984b6f),MIN(GET_ANALVR(192db204-710e-481c-a984-71a262984b6f) + Get_Number(1),Get_Number(50)))
```

<a id="e-fb5abfff-3fc4-4013-9339-209f7da8da1f"></a>

## str_ancCND_DECK_COUNTER_INITIALIZE

Source: `RuntimeExpressions` / `fb5abfff-3fc4-4013-9339-209f7da8da1f`.

Initialize the Deck Counter

Readable:
```text
IF((Get_Field(DECK_RATE)='N' AND YR=Get_Number(1)) OR GET_ANALVR(str_nAAV_CND_DK_COUNTER)=-Get_Number(1),-Get_Number(1),Get_Field(COUNTER_INIT_DECK))
```

Original:
```text
IF((Get_Field(a945c2eb-6da7-474a-9578-818228787db6)='N' AND YR=Get_Number(1)) OR GET_ANALVR(192db204-710e-481c-a984-71a262984b6f)=-Get_Number(1),-Get_Number(1),Get_Field(c77a244a-75f4-40e3-87fe-12c77e36558b))
```

<a id="e-e7714750-4afe-4a2f-8c39-06769a8ee295"></a>

## str_ancCND_DECK_DET_MOD

Source: `dTIMSExpressions` / `e7714750-4afe-4a2f-8c39-06769a8ee295`.

Set Deck Deterioration Modification Factor

Readable:
```text
Get_Number(1)
//modified 2026-05-08 since they are always 1
//IF(Bridge->CRTS_ROUTE,
//    // CRTS
//    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Det_Mod_Factors','DECK','KEY','CRTS',TRUE)),
//IF(// commercial route
//    Bridge->TYPE_OF_TRAFFIC = '3' OR Bridge->TYPE_OF_TRAFFIC = '5' OR Bridge->TYPE_OF_TRAFFIC = '6' OR Bridge->TYPE_OF_TRAFFIC='7',
//    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Det_Mod_Factors','DECK','KEY','COMROUTE',TRUE))
//    ,
//    // district
//    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Det_Mod_Factors','DECK','KEY',Bridge->PARRENT_ASSET,TRUE))
//    )
//)
```

Original:
```text
Get_Number(1)
//modified 2026-05-08 since they are always 1
//IF(Bridge->CRTS_ROUTE,
//    // CRTS
//    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Det_Mod_Factors','DECK','KEY','CRTS',TRUE)),
//IF(// commercial route
//    Bridge->TYPE_OF_TRAFFIC = '3' OR Bridge->TYPE_OF_TRAFFIC = '5' OR Bridge->TYPE_OF_TRAFFIC = '6' OR Bridge->TYPE_OF_TRAFFIC='7',
//    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Det_Mod_Factors','DECK','KEY','COMROUTE',TRUE))
//    ,
//    // district
//    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Det_Mod_Factors','DECK','KEY',Bridge->PARRENT_ASSET,TRUE))
//    )
//)
```

<a id="e-dbc23835-7a35-4f7f-9c2e-956ba68892dd"></a>

## str_ancCND_DECK_INITIALIZE

Source: `dTIMSExpressions` / `dbc23835-7a35-4f7f-9c2e-956ba68892dd`.

Initialize the Deck Condition Rating

Readable:
```text
IF(Get_Field(DECK_RATE) ='N' OR Get_Field(CULV_RATE) <> 'N',-Get_Number(1),VAL(Get_Field(DECK_RATE)))
    
```

Original:
```text
IF(Get_Field(a945c2eb-6da7-474a-9578-818228787db6) ='N' OR Get_Field(176ba749-8358-42b7-97b0-5fe542dac530) <> 'N',-Get_Number(1),VAL(Get_Field(a945c2eb-6da7-474a-9578-818228787db6)))
    
```

<a id="e-6f159147-1542-4713-b935-b5e064648ec9"></a>

## str_ancCND_DECK_LIFE

Source: `RuntimeExpressions` / `6f159147-1542-4713-b935-b5e064648ec9`.

Deck Life Deterioration

Readable:
```text
IF(GET_ANALVR(str_nAAV_CND_DK_LIFE)>Get_Number(0), GET_ANALVR(str_nAAV_CND_DK_LIFE)-Get_Number(1),Get_Number(0))
```

Original:
```text
IF(GET_ANALVR(27eddee2-190d-4175-ba2f-ed3bfa8ecb75)>Get_Number(0), GET_ANALVR(27eddee2-190d-4175-ba2f-ed3bfa8ecb75)-Get_Number(1),Get_Number(0))
```

<a id="e-5554ef7b-ea52-498b-ac16-e629fea09152"></a>

## str_ancCND_DECK_LIFE_INITIALIZE

Source: `dTIMSExpressions` / `5554ef7b-ea52-498b-ac16-e629fea09152`.

Initialize the Deck Life

Readable:
```text
Get_Number(0)
```

Original:
```text
Get_Number(0)
```

<a id="e-6ea96080-56d2-42ab-8b7a-fc01dcf965b5"></a>

## str_ancCND_DECK_MARKOV

Source: `dTIMSExpressions` / `6ea96080-56d2-42ab-8b7a-fc01dcf965b5`.

Deck Markov Variable to initialize which deterioration curve to use.  Set to the value of the original deck rating.

Readable:
```text
IF(Get_Field(DECK_RATE)='N','1',Get_Field(DECK_RATE))
```

Original:
```text
IF(Get_Field(a945c2eb-6da7-474a-9578-818228787db6)='N','1',Get_Field(a945c2eb-6da7-474a-9578-818228787db6))
```

<a id="e-a720de1e-035e-4be4-9627-ce87a8ff48aa"></a>

## str_ancCND_GFP

Source: `RuntimeExpressions` / `a720de1e-035e-4be4-9627-ce87a8ff48aa`.

Good Fair Poor of the structure

Readable:
```text
IF(GET_ANALVR(str_nAAV_CND_STR_COND)<=Get_Number(4),'POOR',IF(GET_ANALVR(str_nAAV_CND_STR_COND)>Get_Number(6),'GOOD','FAIR'))
```

Original:
```text
IF(GET_ANALVR(c809b016-2ffb-480b-8fed-d6b0487b72f4)<=Get_Number(4),'POOR',IF(GET_ANALVR(c809b016-2ffb-480b-8fed-d6b0487b72f4)>Get_Number(6),'GOOD','FAIR'))
```

<a id="e-b11bc4d9-76a9-4b0a-b83e-1ed289a2e2b4"></a>

## str_ancCND_STR_COND

Source: `RuntimeExpressions` / `b11bc4d9-76a9-4b0a-b83e-1ed289a2e2b4`.

Structural Condition

Readable:
```text
IF(Get_Field(CULV_RATE)<>'N',
    GET_ANALVR(str_nAAV_CND_CVT),
IF(Get_Field(DECK_RATE) <> 'N' and Get_Field(SUP_RATE) <> 'N' and Get_Field(SUB_RATE) <> 'N',
    MIN(GET_ANALVR(str_nAAV_CND_DK),MIN(GET_ANALVR(str_nAAV_CND_SUP),GET_ANALVR(str_nAAV_CND_SUB))),
IF(Get_Field(DECK_RATE) = 'N' and Get_Field(SUP_RATE) <> 'N' and Get_Field(SUB_RATE) <> 'N',
    MIN(GET_ANALVR(str_nAAV_CND_SUP),GET_ANALVR(str_nAAV_CND_SUB)),
IF(Get_Field(DECK_RATE) = 'N' and Get_Field(SUP_RATE) = 'N' and Get_Field(SUB_RATE) <> 'N',
    GET_ANALVR(str_nAAV_CND_SUB),
IF(Get_Field(DECK_RATE) = 'N' and Get_Field(SUP_RATE) <> 'N' and Get_Field(SUB_RATE) = 'N',
    GET_ANALVR(str_nAAV_CND_SUP),
IF(Get_Field(DECK_RATE) <> 'N' and Get_Field(SUP_RATE) <> 'N' and Get_Field(SUB_RATE) = 'N',
    MIN(GET_ANALVR(str_nAAV_CND_DK),GET_ANALVR(str_nAAV_CND_SUP)),
    MIN(GET_ANALVR(str_nAAV_CND_DK),MIN(GET_ANALVR(str_nAAV_CND_SUP),GET_ANALVR(str_nAAV_CND_SUB)))
))))))
```

Original:
```text
IF(Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)<>'N',
    GET_ANALVR(fb31bbaf-26dc-4b1f-9e1b-31000f7ee770),
IF(Get_Field(a945c2eb-6da7-474a-9578-818228787db6) <> 'N' and Get_Field(0515dd52-296b-4201-b684-f311c6351c28) <> 'N' and Get_Field(710ed755-0a0b-4140-be95-783a88323b81) <> 'N',
    MIN(GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903),MIN(GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8),GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2))),
IF(Get_Field(a945c2eb-6da7-474a-9578-818228787db6) = 'N' and Get_Field(0515dd52-296b-4201-b684-f311c6351c28) <> 'N' and Get_Field(710ed755-0a0b-4140-be95-783a88323b81) <> 'N',
    MIN(GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8),GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)),
IF(Get_Field(a945c2eb-6da7-474a-9578-818228787db6) = 'N' and Get_Field(0515dd52-296b-4201-b684-f311c6351c28) = 'N' and Get_Field(710ed755-0a0b-4140-be95-783a88323b81) <> 'N',
    GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2),
IF(Get_Field(a945c2eb-6da7-474a-9578-818228787db6) = 'N' and Get_Field(0515dd52-296b-4201-b684-f311c6351c28) <> 'N' and Get_Field(710ed755-0a0b-4140-be95-783a88323b81) = 'N',
    GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8),
IF(Get_Field(a945c2eb-6da7-474a-9578-818228787db6) <> 'N' and Get_Field(0515dd52-296b-4201-b684-f311c6351c28) <> 'N' and Get_Field(710ed755-0a0b-4140-be95-783a88323b81) = 'N',
    MIN(GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903),GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)),
    MIN(GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903),MIN(GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8),GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)))
))))))
```

<a id="e-6c2f41da-fbe6-4dbb-a618-6986ac38dc7b"></a>

## str_ancCND_SUB

Source: `RuntimeExpressions` / `6c2f41da-fbe6-4dbb-a618-6986ac38dc7b`.

Substructure Condition Rating

Readable:
```text
IF(Get_Field(CULV_RATE)<>'N' OR (Get_Field(SUB_RATE) = 'N' AND YR=Get_Number(1)) OR GET_ANALVR(str_nAAV_CND_SUB)<Get_Number(0),-Get_Number(1),
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CR_Life','YR'+SUBSTR(LTRIM(RTRIM(STR(Get_Number(100)+MAX(GET_ANALVR(str_nAAV_CND_SUB_COUNTER),Get_Number(0))))),Get_Number(2),Get_Number(2)),'KEY','SUB_'+GET_ANALVR(str_tDAV_SUB_MARKOV),TRUE))
)
 
```

Original:
```text
IF(Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)<>'N' OR (Get_Field(710ed755-0a0b-4140-be95-783a88323b81) = 'N' AND YR=Get_Number(1)) OR GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)<Get_Number(0),-Get_Number(1),
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CR_Life','YR'+SUBSTR(LTRIM(RTRIM(STR(Get_Number(100)+MAX(GET_ANALVR(65241048-afde-4c67-998f-fc998cfc9c5e),Get_Number(0))))),Get_Number(2),Get_Number(2)),'KEY','SUB_'+GET_ANALVR(9ec17ca2-4bc4-478e-8ecd-58d3acfd31aa),TRUE))
)
 
```

<a id="e-d6105f8c-e395-4ab6-b0b6-8326c1d31802"></a>

## str_ancCND_SUB_COUNTER

Source: `RuntimeExpressions` / `d6105f8c-e395-4ab6-b0b6-8326c1d31802`.

Substructure Counter

Readable:
```text
IF(GET_ANALVR(str_nAAV_CND_SUB_LIFE)>Get_Number(0) OR GET_ANALVR(str_nAAV_CND_SUB_COUNTER)<Get_Number(0),GET_ANALVR(str_nAAV_CND_SUB_COUNTER),MIN(GET_ANALVR(str_nAAV_CND_SUB_COUNTER)+Get_Number(1),Get_Number(50)))
```

Original:
```text
IF(GET_ANALVR(9e01da2a-67c4-42ab-b823-1022fb5f6a69)>Get_Number(0) OR GET_ANALVR(65241048-afde-4c67-998f-fc998cfc9c5e)<Get_Number(0),GET_ANALVR(65241048-afde-4c67-998f-fc998cfc9c5e),MIN(GET_ANALVR(65241048-afde-4c67-998f-fc998cfc9c5e)+Get_Number(1),Get_Number(50)))
```

<a id="e-1bf23945-9b49-4212-8252-5a09e40f64c3"></a>

## str_ancCND_SUB_COUNTER_INITIALIZE

Source: `dTIMSExpressions` / `1bf23945-9b49-4212-8252-5a09e40f64c3`.

Initialize the Substructure Counter

Readable:
```text
IF(Get_Field(SUB_RATE)='N',-Get_Number(1),Get_Field(COUNTER_INIT_SUB))
```

Original:
```text
IF(Get_Field(710ed755-0a0b-4140-be95-783a88323b81)='N',-Get_Number(1),Get_Field(61aa9226-3ee6-47c7-9db5-82b3aed7e54d))
```

<a id="e-840dbc7f-5efc-4ced-8aeb-d7e6740ecac8"></a>

## str_ancCND_SUB_COUNTER_RESET

Source: `dTIMSExpressions` / `840dbc7f-5efc-4ced-8aeb-d7e6740ecac8`.

Reset Counter

Readable:
```text
Get_Number(0)
```

Original:
```text
Get_Number(0)
```

<a id="e-859cbd10-b271-4d77-b4fb-c8e4b812583d"></a>

## str_ancCND_SUB_DET_MOD

Source: `dTIMSExpressions` / `859cbd10-b271-4d77-b4fb-c8e4b812583d`.

Set Substructure Deterioration Modification Factor

Readable:
```text
Get_Number(1)
//modifed 2026-05-08 they are all 1
//IF(Bridge->CRTS_ROUTE,
//// CRTS
////VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Det_Mod_Factors','SUBSTRUCTURE','KEY','CRTS',TRUE)),
//IF(// commercial route
//    Bridge->TYPE_OF_TRAFFIC = '3' OR Bridge->TYPE_OF_TRAFFIC = '5' OR Bridge->TYPE_OF_TRAFFIC = '6' OR Bridge->TYPE_OF_TRAFFIC='7',
//    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Det_Mod_Factors','SUBSTRUCTURE','KEY','COMROUTE',TRUE))
//    ,
//    // district
//    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Det_Mod_Factors','SUBSTRUCTURE','KEY',Bridge->PARRENT_ASSET,TRUE))
//    )
//)
```

Original:
```text
Get_Number(1)
//modifed 2026-05-08 they are all 1
//IF(Bridge->CRTS_ROUTE,
//// CRTS
////VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Det_Mod_Factors','SUBSTRUCTURE','KEY','CRTS',TRUE)),
//IF(// commercial route
//    Bridge->TYPE_OF_TRAFFIC = '3' OR Bridge->TYPE_OF_TRAFFIC = '5' OR Bridge->TYPE_OF_TRAFFIC = '6' OR Bridge->TYPE_OF_TRAFFIC='7',
//    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Det_Mod_Factors','SUBSTRUCTURE','KEY','COMROUTE',TRUE))
//    ,
//    // district
//    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Det_Mod_Factors','SUBSTRUCTURE','KEY',Bridge->PARRENT_ASSET,TRUE))
//    )
//)
```

<a id="e-3883d043-bf41-4517-b161-7516ab4a5f2a"></a>

## str_ancCND_SUB_INITIALIZE

Source: `dTIMSExpressions` / `3883d043-bf41-4517-b161-7516ab4a5f2a`.

Initialize the Substructure Condition Rating

Readable:
```text
IF(Get_Field(SUB_RATE) ='N' OR Get_Field(CULV_RATE) <> 'N',-Get_Number(1),VAL(Get_Field(SUB_RATE)))
    
```

Original:
```text
IF(Get_Field(710ed755-0a0b-4140-be95-783a88323b81) ='N' OR Get_Field(176ba749-8358-42b7-97b0-5fe542dac530) <> 'N',-Get_Number(1),VAL(Get_Field(710ed755-0a0b-4140-be95-783a88323b81)))
    
```

<a id="e-d96c0b34-5a76-4799-81a5-4f1de41c08e3"></a>

## str_ancCND_SUB_LIFE

Source: `RuntimeExpressions` / `d96c0b34-5a76-4799-81a5-4f1de41c08e3`.

Substructure Life Deterioration

Readable:
```text
IF(GET_ANALVR(str_nAAV_CND_SUB_LIFE)>Get_Number(0), GET_ANALVR(str_nAAV_CND_SUB_LIFE)-Get_Number(1),Get_Number(0))
```

Original:
```text
IF(GET_ANALVR(9e01da2a-67c4-42ab-b823-1022fb5f6a69)>Get_Number(0), GET_ANALVR(9e01da2a-67c4-42ab-b823-1022fb5f6a69)-Get_Number(1),Get_Number(0))
```

<a id="e-2c86074d-dc1c-41c2-bfbe-2cdb3b223772"></a>

## str_ancCND_SUB_LIFE_INITIALIZE

Source: `dTIMSExpressions` / `2c86074d-dc1c-41c2-bfbe-2cdb3b223772`.

Initialize the Substructure Life

Readable:
```text
Get_Number(0)
```

Original:
```text
Get_Number(0)
```

<a id="e-08dc40df-4b97-4310-91d3-4fc415a43e89"></a>

## str_ancCND_SUB_MARKOV

Source: `dTIMSExpressions` / `08dc40df-4b97-4310-91d3-4fc415a43e89`.

Substructure Markov Variable to initialize which deterioration curve to use.  Set to the value of the original substructure rating.

Readable:
```text
IF(Get_Field(SUB_RATE)='N','1',Get_Field(SUB_RATE))
```

Original:
```text
IF(Get_Field(710ed755-0a0b-4140-be95-783a88323b81)='N','1',Get_Field(710ed755-0a0b-4140-be95-783a88323b81))
```

<a id="e-9b0569c3-abb8-41c8-a823-011bf4e8e118"></a>

## str_ancCND_SUP

Source: `RuntimeExpressions` / `9b0569c3-abb8-41c8-a823-011bf4e8e118`.

Superstructure Condition Rating

Readable:
```text
IF(Get_Field(CULV_RATE)<>'N' OR (Get_Field(SUP_RATE) = 'N' AND YR=Get_Number(1)) OR GET_ANALVR(str_nAAV_CND_SUP) < Get_Number(0),-Get_Number(1),
IF(LEFT(Get_Field(STRUCTURE_MATERIAL),Get_Number(1)) ='S',
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CR_Life','YR'+SUBSTR(LTRIM(RTRIM(STR(Get_Number(100)+MAX(GET_ANALVR(str_nAAV_CND_SUP_COUNTER),Get_Number(0))))),Get_Number(2),Get_Number(2)),'KEY','SUP_S_'+GET_ANALVR(str_tDAV_SUP_MARKOV),TRUE))
,
IF(LEFT(Get_Field(STRUCTURE_MATERIAL),Get_Number(3)) ='C03' OR LEFT(Get_Field(STRUCTURE_MATERIAL),Get_Number(3)) ='C04' OR LEFT(Get_Field(STRUCTURE_MATERIAL),Get_Number(3)) ='C05',
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CR_Life','YR'+SUBSTR(LTRIM(RTRIM(STR(Get_Number(100)+MAX(GET_ANALVR(str_nAAV_CND_SUP_COUNTER),Get_Number(0))))),Get_Number(2),Get_Number(2)),'KEY','SUP_P_'+GET_ANALVR(str_tDAV_SUP_MARKOV),TRUE))
,
IF(LEFT(Get_Field(STRUCTURE_MATERIAL),Get_Number(1)) ='T',
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CR_Life','YR'+SUBSTR(LTRIM(RTRIM(STR(Get_Number(100)+MAX(GET_ANALVR(str_nAAV_CND_SUP_COUNTER),Get_Number(0))))),Get_Number(2),Get_Number(2)),'KEY','SUP_T_'+GET_ANALVR(str_tDAV_SUP_MARKOV),TRUE))
,
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CR_Life','YR'+SUBSTR(LTRIM(RTRIM(STR(Get_Number(100)+MAX(GET_ANALVR(str_nAAV_CND_SUP_COUNTER),Get_Number(0))))),Get_Number(2),Get_Number(2)),'KEY','SUP_R_'+GET_ANALVR(str_tDAV_SUP_MARKOV),TRUE))
)
)
)
)
```

Original:
```text
IF(Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)<>'N' OR (Get_Field(0515dd52-296b-4201-b684-f311c6351c28) = 'N' AND YR=Get_Number(1)) OR GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8) < Get_Number(0),-Get_Number(1),
IF(LEFT(Get_Field(c51519d3-b3df-4130-82e8-70433ec40976),Get_Number(1)) ='S',
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CR_Life','YR'+SUBSTR(LTRIM(RTRIM(STR(Get_Number(100)+MAX(GET_ANALVR(3eac3442-23fa-4048-89dd-6e03f85c54b4),Get_Number(0))))),Get_Number(2),Get_Number(2)),'KEY','SUP_S_'+GET_ANALVR(2f50c10a-8fc3-40f2-8e19-e824c6608348),TRUE))
,
IF(LEFT(Get_Field(c51519d3-b3df-4130-82e8-70433ec40976),Get_Number(3)) ='C03' OR LEFT(Get_Field(c51519d3-b3df-4130-82e8-70433ec40976),Get_Number(3)) ='C04' OR LEFT(Get_Field(c51519d3-b3df-4130-82e8-70433ec40976),Get_Number(3)) ='C05',
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CR_Life','YR'+SUBSTR(LTRIM(RTRIM(STR(Get_Number(100)+MAX(GET_ANALVR(3eac3442-23fa-4048-89dd-6e03f85c54b4),Get_Number(0))))),Get_Number(2),Get_Number(2)),'KEY','SUP_P_'+GET_ANALVR(2f50c10a-8fc3-40f2-8e19-e824c6608348),TRUE))
,
IF(LEFT(Get_Field(c51519d3-b3df-4130-82e8-70433ec40976),Get_Number(1)) ='T',
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CR_Life','YR'+SUBSTR(LTRIM(RTRIM(STR(Get_Number(100)+MAX(GET_ANALVR(3eac3442-23fa-4048-89dd-6e03f85c54b4),Get_Number(0))))),Get_Number(2),Get_Number(2)),'KEY','SUP_T_'+GET_ANALVR(2f50c10a-8fc3-40f2-8e19-e824c6608348),TRUE))
,
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_CR_Life','YR'+SUBSTR(LTRIM(RTRIM(STR(Get_Number(100)+MAX(GET_ANALVR(3eac3442-23fa-4048-89dd-6e03f85c54b4),Get_Number(0))))),Get_Number(2),Get_Number(2)),'KEY','SUP_R_'+GET_ANALVR(2f50c10a-8fc3-40f2-8e19-e824c6608348),TRUE))
)
)
)
)
```

<a id="e-d63f56a4-756d-401c-8f7b-12d46ce49de5"></a>

## str_ancCND_SUPER_INITIALIZE

Source: `dTIMSExpressions` / `d63f56a4-756d-401c-8f7b-12d46ce49de5`.

Initialize the Suprestructure Condition Rating

Readable:
```text
IF(Get_Field(SUP_RATE) ='N' OR Get_Field(CULV_RATE) <> 'N',-Get_Number(1),VAL(Get_Field(SUP_RATE)))
    
```

Original:
```text
IF(Get_Field(0515dd52-296b-4201-b684-f311c6351c28) ='N' OR Get_Field(176ba749-8358-42b7-97b0-5fe542dac530) <> 'N',-Get_Number(1),VAL(Get_Field(0515dd52-296b-4201-b684-f311c6351c28)))
    
```

<a id="e-f171ae68-dbca-4ff8-a85d-7a0fd8d6b2fe"></a>

## str_ancCND_SUP_COUNTER

Source: `RuntimeExpressions` / `f171ae68-dbca-4ff8-a85d-7a0fd8d6b2fe`.

Superstructure Counter

Readable:
```text
IF(GET_ANALVR(str_nAAV_CND_SUP_LIFE)>Get_Number(0) OR GET_ANALVR(str_nAAV_CND_SUP_COUNTER)<Get_Number(0),GET_ANALVR(str_nAAV_CND_SUP_COUNTER),MIN(GET_ANALVR(str_nAAV_CND_SUP_COUNTER) + Get_Number(1),Get_Number(50)))
```

Original:
```text
IF(GET_ANALVR(114a6e07-b45f-41a2-aae0-5b758da2be11)>Get_Number(0) OR GET_ANALVR(3eac3442-23fa-4048-89dd-6e03f85c54b4)<Get_Number(0),GET_ANALVR(3eac3442-23fa-4048-89dd-6e03f85c54b4),MIN(GET_ANALVR(3eac3442-23fa-4048-89dd-6e03f85c54b4) + Get_Number(1),Get_Number(50)))
```

<a id="e-6f29f86d-dbb5-4753-8c62-94cf98ab8d34"></a>

## str_ancCND_SUP_COUNTER_INITIALIZE

Source: `dTIMSExpressions` / `6f29f86d-dbb5-4753-8c62-94cf98ab8d34`.

Initialize the Superstructure Counter

Readable:
```text
IF(Get_Field(SUP_RATE)='N',-Get_Number(1),Get_Field(COUNTER_INIT_SUPER))
```

Original:
```text
IF(Get_Field(0515dd52-296b-4201-b684-f311c6351c28)='N',-Get_Number(1),Get_Field(fb619ac9-32c7-44a8-ae5f-2781e4d8ceac))
```

<a id="e-4c4f7afe-0bc0-4b0e-a6f4-156c9f2e6e35"></a>

## str_ancCND_SUP_COUNTER_RESET

Source: `dTIMSExpressions` / `4c4f7afe-0bc0-4b0e-a6f4-156c9f2e6e35`.

Reset Counter

Readable:
```text
Get_Number(0)
```

Original:
```text
Get_Number(0)
```

<a id="e-8a8318f4-1288-43ba-b660-4278c4ecf544"></a>

## str_ancCND_SUP_DET_MOD

Source: `dTIMSExpressions` / `8a8318f4-1288-43ba-b660-4278c4ecf544`.

Set Superstructure Deterioration Modification Factor

Readable:
```text
Get_Number(1)
//modifed 2026-05-08 all were 1 anyway
//IF(Bridge->CRTS_ROUTE,
//    // CRTS
//    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Det_Mod_Factors','SUPERSTRUCTURE','KEY','CRTS',TRUE)),
//IF(// commercial route
//    Bridge->TYPE_OF_TRAFFIC = '3' OR Bridge->TYPE_OF_TRAFFIC = '5' OR Bridge->TYPE_OF_TRAFFIC = '6' OR Bridge->TYPE_OF_TRAFFIC='7',
//    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Det_Mod_Factors','SUPERSTRUCTURE','KEY','COMROUTE',TRUE))
//    ,
//    // district
//    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Det_Mod_Factors','SUPERSTRUCTURE','KEY',Bridge->PARRENT_ASSET,TRUE))
//    )
//)
```

Original:
```text
Get_Number(1)
//modifed 2026-05-08 all were 1 anyway
//IF(Bridge->CRTS_ROUTE,
//    // CRTS
//    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Det_Mod_Factors','SUPERSTRUCTURE','KEY','CRTS',TRUE)),
//IF(// commercial route
//    Bridge->TYPE_OF_TRAFFIC = '3' OR Bridge->TYPE_OF_TRAFFIC = '5' OR Bridge->TYPE_OF_TRAFFIC = '6' OR Bridge->TYPE_OF_TRAFFIC='7',
//    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Det_Mod_Factors','SUPERSTRUCTURE','KEY','COMROUTE',TRUE))
//    ,
//    // district
//    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Det_Mod_Factors','SUPERSTRUCTURE','KEY',Bridge->PARRENT_ASSET,TRUE))
//    )
//)
```

<a id="e-9fdc10a9-32f0-486f-91f5-411b68a047f1"></a>

## str_ancCND_SUP_LIFE

Source: `RuntimeExpressions` / `9fdc10a9-32f0-486f-91f5-411b68a047f1`.

Superstructure Life Deterioration

Readable:
```text
IF(GET_ANALVR(str_nAAV_CND_SUP_LIFE)>Get_Number(0), GET_ANALVR(str_nAAV_CND_SUP_LIFE)-Get_Number(1),Get_Number(0))
```

Original:
```text
IF(GET_ANALVR(114a6e07-b45f-41a2-aae0-5b758da2be11)>Get_Number(0), GET_ANALVR(114a6e07-b45f-41a2-aae0-5b758da2be11)-Get_Number(1),Get_Number(0))
```

<a id="e-40e5ce85-66fa-4360-ac91-a06eba6c4b7d"></a>

## str_ancCND_SUP_LIFE_INITIALIZE

Source: `dTIMSExpressions` / `40e5ce85-66fa-4360-ac91-a06eba6c4b7d`.

Initialize the Superstructure Life

Readable:
```text
Get_Number(0)
```

Original:
```text
Get_Number(0)
```

<a id="e-a8792e4f-cf4c-4b28-8804-380c15a70668"></a>

## str_ancCND_SUP_MARKOV

Source: `dTIMSExpressions` / `a8792e4f-cf4c-4b28-8804-380c15a70668`.

Superstructure Markov Variable to initialize which deterioration curve to use.  Set to the value of the original superstructure rating.

Readable:
```text
IF(Get_Field(SUP_RATE)='N','1',Get_Field(SUP_RATE))
```

Original:
```text
IF(Get_Field(0515dd52-296b-4201-b684-f311c6351c28)='N','1',Get_Field(0515dd52-296b-4201-b684-f311c6351c28))
```

<a id="e-c19cae83-7ea6-4f78-84e7-66111a70bf6a"></a>

## str_ancCND_WCCR

Source: `RuntimeExpressions` / `c19cae83-7ea6-4f78-84e7-66111a70bf6a`.

Weighted Compostie Condition Rating

Readable:
```text
GET_ANALVR(str_nAAV_CND_CCR) * GET_ANALVR(str_nAAV_CND_CCR_WT) * Get_Number(1)
```

Original:
```text
GET_ANALVR(488c7763-e676-4d56-b376-b450bcb37f06) * GET_ANALVR(d8a94de1-7c4c-4628-ba9e-1675a3058eb6) * Get_Number(1)
```

<a id="e-e99807e1-6e6c-4d65-84b0-81a8af590756"></a>

## str_ancCST_BKAMPP

Source: `RuntimeExpressions` / `e99807e1-6e6c-4d65-84b0-81a8af590756`.

BKAMPP Cost

Readable:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
IF(IS_COMMITTED() AND  YR = Get_Field(COM_YEAR) AND Get_Field(COM_COST) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Number(0),
//otherwise calculate it
(
    (Get_Field(ELEM_300_QUANTITY)+Get_Field(ELEM_301_QUANTITY)+
     Get_Field(ELEM_302_QUANTITY)+Get_Field(ELEM_303_QUANTITY)+
     Get_Field(ELEM_304_QUANTITY)+Get_Field(ELEM_305_QUANTITY)+
     Get_Field(ELEM_306_QUANTITY)) * 
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','JOINT_REPLACE',TRUE)) +
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','JOINT_REPLACE',TRUE)) +
    GET_ANALVR(str_nDAV_DECK_AREA)* VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','BKAMPP',TRUE)) +
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','BKAMPP',TRUE))
)
* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1))) 
* IF(GET_ANALVR(str_nDAV_DECK_AREA) >Get_Number(25000),Get_Number(0.5),
  IF(GET_ANALVR(str_nDAV_DECK_AREA) >Get_Number(15000),Get_Number(0.65),Get_Number(1)))
))))


```

Original:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
IF(IS_COMMITTED() AND  YR = Get_Field(d62be030-874b-4177-9d41-e00645ac75d8) AND Get_Field(709339b0-b77b-464c-acf5-d05a5a08c50d) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Number(0),
//otherwise calculate it
(
    (Get_Field(9aedad63-77e7-447a-8c44-21a89ae03440)+Get_Field(4b504462-b48a-473c-925c-d7a8705fb230)+
     Get_Field(286fae98-ad52-46cc-adab-7d5978b28ac0)+Get_Field(0caab4da-a7c0-4635-a19e-e82950b8b8fc)+
     Get_Field(56ab8060-0651-4223-b119-3043fe5a0abc)+Get_Field(87443be7-82d6-4927-9f74-a8e47f9602b0)+
     Get_Field(33c2b855-eefa-4211-b1c0-a5600d95c61f)) * 
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','JOINT_REPLACE',TRUE)) +
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','JOINT_REPLACE',TRUE)) +
    GET_ANALVR(d546e0a3-b9fc-4676-a220-97982070928f)* VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','BKAMPP',TRUE)) +
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','BKAMPP',TRUE))
)
* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1))) 
* IF(GET_ANALVR(d546e0a3-b9fc-4676-a220-97982070928f) >Get_Number(25000),Get_Number(0.5),
  IF(GET_ANALVR(d546e0a3-b9fc-4676-a220-97982070928f) >Get_Number(15000),Get_Number(0.65),Get_Number(1)))
))))


```

<a id="e-f66e55e5-f706-4b9a-982f-300a34a09663"></a>

## str_ancCST_CULVERT_REHAB

Source: `RuntimeExpressions` / `f66e55e5-f706-4b9a-982f-300a34a09663`.

Cost of the Culvert Rehab Treatment

Readable:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
// this is a major so it is 0, com cost or calculated
IF(IS_COMMITTED() AND  YR = Get_Field(COM_YEAR) AND Get_Field(COM_COST) >= Get_Number(0),Get_Field(COM_COST),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297),
//otherwise calculate it
( 
    GET_ANALVR(str_nDAV_DECK_AREA)*VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','CULVERT_REHAB',TRUE))
    + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','CULVERT_REHAB',TRUE))
) * ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1)))
))))
```

Original:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
// this is a major so it is 0, com cost or calculated
IF(IS_COMMITTED() AND  YR = Get_Field(d62be030-874b-4177-9d41-e00645ac75d8) AND Get_Field(709339b0-b77b-464c-acf5-d05a5a08c50d) >= Get_Number(0),Get_Field(709339b0-b77b-464c-acf5-d05a5a08c50d),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297),
//otherwise calculate it
( 
    GET_ANALVR(d546e0a3-b9fc-4676-a220-97982070928f)*VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','CULVERT_REHAB',TRUE))
    + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','CULVERT_REHAB',TRUE))
) * ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1)))
))))
```

<a id="e-765b1a26-a514-4920-a00b-0fd0a9a2714c"></a>

## str_ancCST_CULVERT_REPLACEMENT

Source: `RuntimeExpressions` / `765b1a26-a514-4920-a00b-0fd0a9a2714c`.

Cost of the Culvert Replacement Treatment

Readable:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
// this is a major so it is 0, com cost or calculated
IF(IS_COMMITTED() AND  YR = Get_Field(COM_YEAR) AND Get_Field(COM_COST) >= Get_Number(0),Get_Field(COM_COST),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297),
//otherwise calculate it
(
    GET_ANALVR(str_nDAV_DECK_AREA) * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','CULVERT_REPLACE',TRUE))
    + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','CULVERT_REPLACE',TRUE))
)* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1)))
))))
```

Original:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
// this is a major so it is 0, com cost or calculated
IF(IS_COMMITTED() AND  YR = Get_Field(d62be030-874b-4177-9d41-e00645ac75d8) AND Get_Field(709339b0-b77b-464c-acf5-d05a5a08c50d) >= Get_Number(0),Get_Field(709339b0-b77b-464c-acf5-d05a5a08c50d),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297),
//otherwise calculate it
(
    GET_ANALVR(d546e0a3-b9fc-4676-a220-97982070928f) * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','CULVERT_REPLACE',TRUE))
    + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','CULVERT_REPLACE',TRUE))
)* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1)))
))))
```

<a id="e-ebf02ccc-64e4-42c4-aba7-6e2ea378f16d"></a>

## str_ancCST_DECK_OVERLAY

Source: `RuntimeExpressions` / `ebf02ccc-64e4-42c4-aba7-6e2ea378f16d`.

Cost of a Deck Overlay

Readable:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
IF(IS_COMMITTED() AND  YR = Get_Field(COM_YEAR) AND Get_Field(COM_COST) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Number(0),
//otherwise calculate it
(
    GET_ANALVR(str_nDAV_DECK_AREA) *  VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','DECK_OVERLAY',TRUE))
    + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','DECK_OVERLAY',TRUE))
)
* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1)))
))))
```

Original:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
IF(IS_COMMITTED() AND  YR = Get_Field(d62be030-874b-4177-9d41-e00645ac75d8) AND Get_Field(709339b0-b77b-464c-acf5-d05a5a08c50d) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Number(0),
//otherwise calculate it
(
    GET_ANALVR(d546e0a3-b9fc-4676-a220-97982070928f) *  VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','DECK_OVERLAY',TRUE))
    + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','DECK_OVERLAY',TRUE))
)
* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1)))
))))
```

<a id="e-98b378cd-246b-4a1c-b495-c5f6721e757e"></a>

## str_ancCST_DECK_PATCH

Source: `RuntimeExpressions` / `98b378cd-246b-4a1c-b495-c5f6721e757e`.

Cost of a Deck Patch

Readable:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
IF(IS_COMMITTED() AND  YR = Get_Field(COM_YEAR) AND Get_Field(COM_COST) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Number(0),
//otherwise calculate it
    (
    (GET_ANALVR(str_AAV_ELEM_1080_CS3)+GET_ANALVR(str_AAV_ELEM_1080_CS4))*
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','DECK_PATCH',TRUE))
     + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','DECK_PATCH',TRUE))
    )
*((Get_Number(1)+GINFLATION)**(YR-Get_Number(1)))
))))
```

Original:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
IF(IS_COMMITTED() AND  YR = Get_Field(d62be030-874b-4177-9d41-e00645ac75d8) AND Get_Field(709339b0-b77b-464c-acf5-d05a5a08c50d) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Number(0),
//otherwise calculate it
    (
    (GET_ANALVR(53bec880-322b-4ac1-a03a-c79fb354c4fb)+GET_ANALVR(454eb22e-95d5-4589-9f60-860fbaaff091))*
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','DECK_PATCH',TRUE))
     + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','DECK_PATCH',TRUE))
    )
*((Get_Number(1)+GINFLATION)**(YR-Get_Number(1)))
))))
```

<a id="e-3eaa8949-195e-4b96-aed2-86dc0b3b78fa"></a>

## str_ancCST_DECK_REHAB

Source: `RuntimeExpressions` / `3eaa8949-195e-4b96-aed2-86dc0b3b78fa`.

Cost of a Deck Rehab

Readable:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
IF(IS_COMMITTED() AND  YR = Get_Field(COM_YEAR) AND Get_Field(COM_COST) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Number(0),
//otherwise calculate it
    (
    GET_ANALVR(str_nDAV_DECK_AREA)* VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','DECK_OVERLAY',TRUE))+
    (Get_Field(ELEM_300_QUANTITY)+Get_Field(ELEM_301_QUANTITY)+Get_Field(ELEM_302_QUANTITY)+Get_Field(ELEM_303_QUANTITY)+
     Get_Field(ELEM_304_QUANTITY)+Get_Field(ELEM_305_QUANTITY)+Get_Field(ELEM_306_QUANTITY)) * 
     VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','JOINT_REPLACE',TRUE))
     + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','DECK_OVERLAY',TRUE))
     )
     *((Get_Number(1)+GINFLATION)**(YR-Get_Number(1)))
))))
```

Original:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
IF(IS_COMMITTED() AND  YR = Get_Field(d62be030-874b-4177-9d41-e00645ac75d8) AND Get_Field(709339b0-b77b-464c-acf5-d05a5a08c50d) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Number(0),
//otherwise calculate it
    (
    GET_ANALVR(d546e0a3-b9fc-4676-a220-97982070928f)* VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','DECK_OVERLAY',TRUE))+
    (Get_Field(9aedad63-77e7-447a-8c44-21a89ae03440)+Get_Field(4b504462-b48a-473c-925c-d7a8705fb230)+Get_Field(286fae98-ad52-46cc-adab-7d5978b28ac0)+Get_Field(0caab4da-a7c0-4635-a19e-e82950b8b8fc)+
     Get_Field(56ab8060-0651-4223-b119-3043fe5a0abc)+Get_Field(87443be7-82d6-4927-9f74-a8e47f9602b0)+Get_Field(33c2b855-eefa-4211-b1c0-a5600d95c61f)) * 
     VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','JOINT_REPLACE',TRUE))
     + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','DECK_OVERLAY',TRUE))
     )
     *((Get_Number(1)+GINFLATION)**(YR-Get_Number(1)))
))))
```

<a id="e-8e1e3752-d931-46bb-a896-c769346b4e83"></a>

## str_ancCST_DECK_REPLACE

Source: `RuntimeExpressions` / `8e1e3752-d931-46bb-a896-c769346b4e83`.

Cost of a Deck Seal

Readable:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
IF(IS_COMMITTED() AND  YR = Get_Field(COM_YEAR) AND Get_Field(COM_COST) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Number(0),
//otherwise calculate it
(
    GET_ANALVR(str_nDAV_DECK_AREA) * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','DECK_REPLACE',TRUE))
    + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','DECK_REPLACE',TRUE))
)
* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1))) 
))))
```

Original:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
IF(IS_COMMITTED() AND  YR = Get_Field(d62be030-874b-4177-9d41-e00645ac75d8) AND Get_Field(709339b0-b77b-464c-acf5-d05a5a08c50d) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Number(0),
//otherwise calculate it
(
    GET_ANALVR(d546e0a3-b9fc-4676-a220-97982070928f) * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','DECK_REPLACE',TRUE))
    + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','DECK_REPLACE',TRUE))
)
* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1))) 
))))
```

<a id="e-97eb5929-40ae-4c4f-a517-8ece9ee284fd"></a>

## str_ancCST_DECK_SEAL

Source: `RuntimeExpressions` / `97eb5929-40ae-4c4f-a517-8ece9ee284fd`.

Cost of a Deck Seal

Readable:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
IF(IS_COMMITTED() AND  YR = Get_Field(COM_YEAR) AND Get_Field(COM_COST) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Number(0),
//otherwise calculate it
(
    GET_ANALVR(str_nDAV_DECK_AREA) * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','DECK_SEAL',TRUE))
    + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','DECK_SEAL',TRUE))
)
* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1))) 
))))
```

Original:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
IF(IS_COMMITTED() AND  YR = Get_Field(d62be030-874b-4177-9d41-e00645ac75d8) AND Get_Field(709339b0-b77b-464c-acf5-d05a5a08c50d) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Number(0),
//otherwise calculate it
(
    GET_ANALVR(d546e0a3-b9fc-4676-a220-97982070928f) * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','DECK_SEAL',TRUE))
    + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','DECK_SEAL',TRUE))
)
* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1))) 
))))
```

<a id="e-fa8bba11-c3c7-4678-b098-a3c934bd778b"></a>

## str_ancCST_JOINT_REPLACE

Source: `RuntimeExpressions` / `fa8bba11-c3c7-4678-b098-a3c934bd778b`.

Cost of a Joint Replace

Readable:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
IF(IS_COMMITTED() AND  YR = Get_Field(COM_YEAR) AND Get_Field(COM_COST) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Number(0),
//otherwise calculate it
(
    (Get_Field(ELEM_300_QUANTITY)+Get_Field(ELEM_301_QUANTITY)+Get_Field(ELEM_302_QUANTITY)+Get_Field(ELEM_303_QUANTITY)+
    Get_Field(ELEM_304_QUANTITY)+Get_Field(ELEM_305_QUANTITY)+Get_Field(ELEM_306_QUANTITY)) * 
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','JOINT_REPLACE',TRUE))
    + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','JOINT_REPLACE',TRUE))
)
* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1))) 
))))
```

Original:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
IF(IS_COMMITTED() AND  YR = Get_Field(d62be030-874b-4177-9d41-e00645ac75d8) AND Get_Field(709339b0-b77b-464c-acf5-d05a5a08c50d) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Number(0),
//otherwise calculate it
(
    (Get_Field(9aedad63-77e7-447a-8c44-21a89ae03440)+Get_Field(4b504462-b48a-473c-925c-d7a8705fb230)+Get_Field(286fae98-ad52-46cc-adab-7d5978b28ac0)+Get_Field(0caab4da-a7c0-4635-a19e-e82950b8b8fc)+
    Get_Field(56ab8060-0651-4223-b119-3043fe5a0abc)+Get_Field(87443be7-82d6-4927-9f74-a8e47f9602b0)+Get_Field(33c2b855-eefa-4211-b1c0-a5600d95c61f)) * 
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','JOINT_REPLACE',TRUE))
    + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','JOINT_REPLACE',TRUE))
)
* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1))) 
))))
```

<a id="e-46bbec94-1e29-446f-98f7-4037eccf72c7"></a>

## str_ancCST_PAINT_REPLACE

Source: `RuntimeExpressions` / `46bbec94-1e29-446f-98f7-4037eccf72c7`.

Cost of a Paint Replace

Readable:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
IF(IS_COMMITTED() AND  YR = Get_Field(COM_YEAR) AND Get_Field(COM_COST) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Number(0),
//otherwise calculate it
(
    Get_Field(ELEM_515_QUANTITY) * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','PAINT_REPLACE',TRUE))
    + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','PAINT_REPLACE',TRUE))
)
* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1)))
))))
```

Original:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
IF(IS_COMMITTED() AND  YR = Get_Field(d62be030-874b-4177-9d41-e00645ac75d8) AND Get_Field(709339b0-b77b-464c-acf5-d05a5a08c50d) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Number(0),
//otherwise calculate it
(
    Get_Field(d16f20d2-56ee-4107-944e-fa25388c7c32) * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','PAINT_REPLACE',TRUE))
    + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','PAINT_REPLACE',TRUE))
)
* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1)))
))))
```

<a id="e-25edc5d6-2365-4ed7-85d5-9aa59dac53ae"></a>

## str_ancCST_PAINT_SPOT

Source: `RuntimeExpressions` / `25edc5d6-2365-4ed7-85d5-9aa59dac53ae`.

Cost of a Spot Paint

Readable:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
IF(IS_COMMITTED() AND  YR = Get_Field(COM_YEAR) AND Get_Field(COM_COST) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Number(0),
//otherwise calculate it
(
    (GET_ANALVR(str_AAV_ELEM_515_CS3) + GET_ANALVR(str_AAV_ELEM_515_CS4))* 
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','PAINT_SPOT_PAINT',TRUE))
    + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','PAINT_SPOT_PAINT',TRUE))
)
* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1))) 
))))
```

Original:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
IF(IS_COMMITTED() AND  YR = Get_Field(d62be030-874b-4177-9d41-e00645ac75d8) AND Get_Field(709339b0-b77b-464c-acf5-d05a5a08c50d) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Number(0),
//otherwise calculate it
(
    (GET_ANALVR(7caba84c-5af2-4de1-aec3-c8cc44e239f9) + GET_ANALVR(45cc163b-7547-4c6f-a0fa-c952651c697c))* 
    VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','PAINT_SPOT_PAINT',TRUE))
    + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','PAINT_SPOT_PAINT',TRUE))
)
* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1))) 
))))
```

<a id="e-199a1dcd-ae81-4a89-b359-fe4731f96d0c"></a>

## str_ancCST_STRUCTURE_REPLACEMENT

Source: `RuntimeExpressions` / `199a1dcd-ae81-4a89-b359-fe4731f96d0c`.

Cost of a Structure Replacement

Readable:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
// this is a major so it is 0, com cost or calculated
IF(IS_COMMITTED() AND  YR = Get_Field(COM_YEAR) AND Get_Field(COM_COST) >= Get_Number(0),Get_Field(COM_COST),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297),
//otherwise calculate it
(
    GET_ANALVR(str_nDAV_DECK_AREA) * 
    IF(LEFT(Get_Field(NHS),Get_Number(1)) = '1', 
        VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','STRUCTURE_REPLACEMENT',TRUE)),
        VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST_Non_NHS','KEY','STRUCTURE_REPLACEMENT',TRUE))
    )
    + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','STRUCTURE_REPLACEMENT',TRUE))
)
* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1)))
))))
```

Original:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
// this is a major so it is 0, com cost or calculated
IF(IS_COMMITTED() AND  YR = Get_Field(d62be030-874b-4177-9d41-e00645ac75d8) AND Get_Field(709339b0-b77b-464c-acf5-d05a5a08c50d) >= Get_Number(0),Get_Field(709339b0-b77b-464c-acf5-d05a5a08c50d),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297),
//otherwise calculate it
(
    GET_ANALVR(d546e0a3-b9fc-4676-a220-97982070928f) * 
    IF(LEFT(Get_Field(ff652eda-e73c-48a8-bd20-fd6e80950604),Get_Number(1)) = '1', 
        VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','STRUCTURE_REPLACEMENT',TRUE)),
        VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST_Non_NHS','KEY','STRUCTURE_REPLACEMENT',TRUE))
    )
    + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','STRUCTURE_REPLACEMENT',TRUE))
)
* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1)))
))))
```

<a id="e-07f6b268-dbd7-4d7d-a2dc-56aa97776c57"></a>

## str_ancCST_STR_MTCE

Source: `RuntimeExpressions` / `07f6b268-dbd7-4d7d-a2dc-56aa97776c57`.

Cost of Structure Maintenance

Readable:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
// this is a major so it is 0, com cost or calculated
IF(IS_COMMITTED() AND  YR = Get_Field(COM_YEAR) AND Get_Field(COM_COST) >= Get_Number(0),Get_Field(COM_COST),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297),
//otherwise calculate it
// here str maintenance always costs 0 if not committed, if -1 the anc treatments calculate the cost
Get_Number(0)
))))
```

Original:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
// this is a major so it is 0, com cost or calculated
IF(IS_COMMITTED() AND  YR = Get_Field(d62be030-874b-4177-9d41-e00645ac75d8) AND Get_Field(709339b0-b77b-464c-acf5-d05a5a08c50d) >= Get_Number(0),Get_Field(709339b0-b77b-464c-acf5-d05a5a08c50d),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297),
//otherwise calculate it
// here str maintenance always costs 0 if not committed, if -1 the anc treatments calculate the cost
Get_Number(0)
))))
```

<a id="e-81be3885-5be2-4553-a5f0-9926600dfcd7"></a>

## str_ancCST_SUBSTRUCTURE_REHAB

Source: `RuntimeExpressions` / `81be3885-5be2-4553-a5f0-9926600dfcd7`.

Cost of a Substructure Rehabilitation

Readable:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
IF(IS_COMMITTED() AND  YR = Get_Field(COM_YEAR) AND Get_Field(COM_COST) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Number(0),
//otherwise calculate it
(
    (GET_ANALVR(str_nDAV_DECK_AREA) * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','SUBSTRUCTURE_REHABILITATION',TRUE))) +
    IF(Get_Exp(str_abfOBJ_DK_GTE_6),
    (MAX((GET_ANALVR(str_AAV_ELEM_1080_CS3)+GET_ANALVR(str_AAV_ELEM_1080_CS4))*VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','DECK_PATCH',TRUE)),
    GET_ANALVR(str_nDAV_DECK_AREA) * Get_Number(0.05) * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','DECK_PATCH',TRUE)))),Get_Number(0)) +
    IF(Get_Exp(str_abfOBJ_SUP_GTE_6),(GET_ANALVR(str_nDAV_DECK_AREA) * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','SUPERSTRUCTURE_REHABILITATION',TRUE)) * Get_Number(0.08)),Get_Number(0))
    + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','SUBSTRUCTURE_REHABILITATION',TRUE))
 )
* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1)))
))))
```

Original:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
IF(IS_COMMITTED() AND  YR = Get_Field(d62be030-874b-4177-9d41-e00645ac75d8) AND Get_Field(709339b0-b77b-464c-acf5-d05a5a08c50d) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Number(0),
//otherwise calculate it
(
    (GET_ANALVR(d546e0a3-b9fc-4676-a220-97982070928f) * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','SUBSTRUCTURE_REHABILITATION',TRUE))) +
    IF(Get_Exp(64178621-7d6f-4a22-b042-c90c69c530a8),
    (MAX((GET_ANALVR(53bec880-322b-4ac1-a03a-c79fb354c4fb)+GET_ANALVR(454eb22e-95d5-4589-9f60-860fbaaff091))*VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','DECK_PATCH',TRUE)),
    GET_ANALVR(d546e0a3-b9fc-4676-a220-97982070928f) * Get_Number(0.05) * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','DECK_PATCH',TRUE)))),Get_Number(0)) +
    IF(Get_Exp(5796df0c-f0d1-453d-8357-aabc03828ac4),(GET_ANALVR(d546e0a3-b9fc-4676-a220-97982070928f) * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','SUPERSTRUCTURE_REHABILITATION',TRUE)) * Get_Number(0.08)),Get_Number(0))
    + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','SUBSTRUCTURE_REHABILITATION',TRUE))
 )
* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1)))
))))
```

<a id="e-eeba8f54-031b-42c3-bd53-084f947597d1"></a>

## str_ancCST_SUPERSTRUCTURE_REPLACEMENT

Source: `RuntimeExpressions` / `eeba8f54-031b-42c3-bd53-084f947597d1`.

Cost of a Superstructure Replacement

Readable:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
// this is a major so it is 0, com cost or calculated
IF(IS_COMMITTED() AND  YR = Get_Field(COM_YEAR) AND Get_Field(COM_COST) >= Get_Number(0),Get_Field(COM_COST),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297),
//otherwise calculate it
(
    GET_ANALVR(str_nDAV_DECK_AREA) * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','SUPERSTRUCTURE_REPLACEMENT',TRUE))
     + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','SUPERSTRUCTURE_REPLACEMENT',TRUE))
)
* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1)))
))))
```

Original:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
// this is a major so it is 0, com cost or calculated
IF(IS_COMMITTED() AND  YR = Get_Field(d62be030-874b-4177-9d41-e00645ac75d8) AND Get_Field(709339b0-b77b-464c-acf5-d05a5a08c50d) >= Get_Number(0),Get_Field(709339b0-b77b-464c-acf5-d05a5a08c50d),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297),
//otherwise calculate it
(
    GET_ANALVR(d546e0a3-b9fc-4676-a220-97982070928f) * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','SUPERSTRUCTURE_REPLACEMENT',TRUE))
     + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','SUPERSTRUCTURE_REPLACEMENT',TRUE))
)
* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1)))
))))
```

<a id="e-dc46bfbb-04b2-4931-a8d2-bf19b6e712fc"></a>

## str_ancCST_SUPER_REHAB

Source: `RuntimeExpressions` / `dc46bfbb-04b2-4931-a8d2-bf19b6e712fc`.

Cost of a Superstructure Rehabilitation

Readable:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
IF(IS_COMMITTED() AND  YR = Get_Field(COM_YEAR) AND Get_Field(COM_COST) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Number(0),
//otherwise calculate it
(
    GET_ANALVR(str_nDAV_DECK_AREA) * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','SUPERSTRUCTURE_REHABILITATION',TRUE)) +
    IF(Get_Exp(str_abfOBJ_DK_GTE_6) AND GET_TRTYR('str_SUBSTRUCTURE_REHAB')<> YR,(MAX((GET_ANALVR(str_AAV_ELEM_1080_CS3)+GET_ANALVR(str_AAV_ELEM_1080_CS4))*VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','DECK_PATCH',TRUE)),
     GET_ANALVR(str_nDAV_DECK_AREA) * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','DECK_PATCH',TRUE)))),Get_Number(0)) +
    IF(Get_Exp(str_abfOBJ_SUB_GTE_6),(GET_ANALVR(str_nDAV_DECK_AREA) * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','SUBSTRUCTURE_REHABILITATION',TRUE)) * Get_Number(0.08)),Get_Number(0))
    + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','SUPERSTRUCTURE_REHABILITATION',TRUE)) 
)
* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1)))
))))
```

Original:
```text
// only the major treatments will have com_cost, all anc will be 0 if com_cost is 0 or filled in with a value.
// if com_cost is -1, then dTIMS Must calculate it
IF(IS_COMMITTED() AND  YR = Get_Field(d62be030-874b-4177-9d41-e00645ac75d8) AND Get_Field(709339b0-b77b-464c-acf5-d05a5a08c50d) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(ebd49918-51ec-4880-bf1e-43957ea03470) AND Get_Field(aa4edc6e-cf46-4895-a624-d6872a1d2831) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(5b9f5ba9-96e5-4142-8937-2967a698b627) AND Get_Field(0a3cea6e-60b6-4ffe-a4fe-38175ddb668b) >= Get_Number(0),Get_Number(0),
IF(IS_COMMITTED() AND  YR = Get_Field(a3bfaf6a-f1be-4956-b39b-22b81d17626b) AND Get_Field(b93333cf-ecb6-4e03-84ab-e955853e3297) >= Get_Number(0),Get_Number(0),
//otherwise calculate it
(
    GET_ANALVR(d546e0a3-b9fc-4676-a220-97982070928f) * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','SUPERSTRUCTURE_REHABILITATION',TRUE)) +
    IF(Get_Exp(64178621-7d6f-4a22-b042-c90c69c530a8) AND GET_TRTYR('str_SUBSTRUCTURE_REHAB')<> YR,(MAX((GET_ANALVR(53bec880-322b-4ac1-a03a-c79fb354c4fb)+GET_ANALVR(454eb22e-95d5-4589-9f60-860fbaaff091))*VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','DECK_PATCH',TRUE)),
     GET_ANALVR(d546e0a3-b9fc-4676-a220-97982070928f) * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','DECK_PATCH',TRUE)))),Get_Number(0)) +
    IF(Get_Exp(c4d2c71a-fe8a-455f-a3db-176724ab0ec5),(GET_ANALVR(d546e0a3-b9fc-4676-a220-97982070928f) * VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','UNIT_COST','KEY','SUBSTRUCTURE_REHABILITATION',TRUE)) * Get_Number(0.08)),Get_Number(0))
    + VAL(DAL_DCG_STLOOKUP('Bridge_Lookup_Treatment_Costs','INITIAL_COST','KEY','SUPERSTRUCTURE_REHABILITATION',TRUE)) 
)
* ((Get_Number(1)+GINFLATION)**(YR-Get_Number(1)))
))))
```

<a id="e-90e1952a-cd7f-468b-8b28-9ce8a46e07d0"></a>

## str_ancCST_YEARLY_COST

Source: `RuntimeExpressions` / `90e1952a-cd7f-468b-8b28-9ce8a46e07d0`.

Yearly Cost

Readable:
```text
GST_COST_F
```

Original:
```text
GST_COST_F
```

<a id="e-f2e8a9c7-a9f6-4c61-b8d2-4d8e26534540"></a>

## str_ancOBJ_ZERO

Source: `dTIMSExpressions` / `f2e8a9c7-a9f6-4c61-b8d2-4d8e26534540`.

ZERO

Readable:
```text
Get_Number(0)
```

Original:
```text
Get_Number(0)
```

<a id="e-7f8a11ec-079a-42ee-9606-2dd1e313d3a4"></a>

## str_ancPV_BENEFIT

Source: `RuntimeExpressions` / `7f8a11ec-079a-42ee-9606-2dd1e313d3a4`.

PV Benefit

Readable:
```text
GET4CAV_PVDIFF(str_nAAV_CND_WCCR,0,str_nAAV_CND_WCCR,0) 
```

Original:
```text
GET4CAV_PVDIFF(466143cc-3eee-41d4-b9a3-7bda22ec6b50,0,466143cc-3eee-41d4-b9a3-7bda22ec6b50,0) 
```

<a id="e-ce9c1712-b589-4014-8a8d-6d2aeddf4641"></a>

## str_ancPV_COST

Source: `RuntimeExpressions` / `ce9c1712-b589-4014-8a8d-6d2aeddf4641`.

PV Cost

Readable:
```text
GET4CAV_PV(str_nAAV_CST_YEARLY_COST) / GET_ANALVR(str_nDAV_DECK_AREA)
```

Original:
```text
GET4CAV_PV(738f24e5-820c-4de7-8907-5e3ff7f2d7ca) / GET_ANALVR(d546e0a3-b9fc-4676-a220-97982070928f)
```

<a id="e-9dae7fbe-3ebf-44b9-8a5e-a9b55e640413"></a>

## str_ancRES_0

Source: `dTIMSExpressions` / `9dae7fbe-3ebf-44b9-8a5e-a9b55e640413`.

Reset of 0

Readable:
```text
Get_Number(0)
```

Original:
```text
Get_Number(0)
```

<a id="e-90c07159-00f0-4e65-96ef-a07b1415d3ca"></a>

## str_ancRES_1

Source: `dTIMSExpressions` / `90c07159-00f0-4e65-96ef-a07b1415d3ca`.

Reset of 1

Readable:
```text
Get_Number(1)
```

Original:
```text
Get_Number(1)
```

<a id="e-d15144c6-f8d5-45ec-94dc-b7728ed64141"></a>

## str_ancRES_10

Source: `dTIMSExpressions` / `d15144c6-f8d5-45ec-94dc-b7728ed64141`.

Reset of 10

Readable:
```text
Get_Number(10)
```

Original:
```text
Get_Number(10)
```

<a id="e-ff08d453-878e-486a-966a-3e7392a5ffca"></a>

## str_ancRES_5

Source: `dTIMSExpressions` / `ff08d453-878e-486a-966a-3e7392a5ffca`.

Reset of 5

Readable:
```text
Get_Number(5)
```

Original:
```text
Get_Number(5)
```

<a id="e-ae94a1e1-6b2f-4a93-8322-f02c14c471c9"></a>

## str_ancRES_8

Source: `dTIMSExpressions` / `ae94a1e1-6b2f-4a93-8322-f02c14c471c9`.

Reset of 8

Readable:
```text
Get_Number(8)
```

Original:
```text
Get_Number(8)
```

<a id="e-936de252-dc57-4df7-ac88-82f760637cd9"></a>

## str_ancRES_COUNT_CVT_REHAB

Source: `RuntimeExpressions` / `936de252-dc57-4df7-ac88-82f760637cd9`.

Reset Culvert Rehab Count

Readable:
```text
GET_ANALVR(str_nDAV_CT_CVT_REHAB)+Get_Number(1)
```

Original:
```text
GET_ANALVR(b7aad387-e270-431f-8bf2-4e520a51aa61)+Get_Number(1)
```

<a id="e-c1e32604-7fce-4513-ad69-fe6c93b1cac3"></a>

## str_ancRES_COUNT_CVT_REPLACE

Source: `RuntimeExpressions` / `c1e32604-7fce-4513-ad69-fe6c93b1cac3`.

Reset the Culvert Replace Count after a Culvert Replace

Readable:
```text
GET_ANALVR(str_nDAV_CT_CVT_REPLACE)+Get_Number(1)
```

Original:
```text
GET_ANALVR(1833163d-abfc-44fa-8428-555d329ad87a)+Get_Number(1)
```

<a id="e-7bd80240-3bca-43f1-8b2c-d741e6943c03"></a>

## str_ancRES_COUNT_DECK_OVERLAY

Source: `RuntimeExpressions` / `7bd80240-3bca-43f1-8b2c-d741e6943c03`.

Reset the Deck OverlayCount after a Deck Overlay

Readable:
```text
GET_ANALVR(str_nDAV_CT_DECK_OVERLAY)+Get_Number(1)
```

Original:
```text
GET_ANALVR(45fd84e7-4367-49de-919f-f8bf01e12c6f)+Get_Number(1)
```

<a id="e-18e1cfff-8500-42e4-b517-b7a9391682f7"></a>

## str_ancRES_COUNT_DECK_PATCH

Source: `RuntimeExpressions` / `18e1cfff-8500-42e4-b517-b7a9391682f7`.

Reset the Deck Patch Count after a Deck Patch

Readable:
```text
GET_ANALVR(str_nDAV_CT_DECK_PATCH)+ Get_Number(1)
```

Original:
```text
GET_ANALVR(1c49a685-77ed-481e-aaef-6f715ffd9d64)+ Get_Number(1)
```

<a id="e-0f1b6e63-2104-4eee-aaf0-490ed96be009"></a>

## str_ancRES_COUNT_DECK_REHAB

Source: `RuntimeExpressions` / `0f1b6e63-2104-4eee-aaf0-490ed96be009`.

Reset the Deck OverlayCount after a Deck Overlay

Readable:
```text
GET_ANALVR(str_nDAV_CT_DK_REHAB)+Get_Number(1)
```

Original:
```text
GET_ANALVR(b2fa169b-0126-424b-8fc8-93723939a1b4)+Get_Number(1)
```

<a id="e-ba9fd832-0df3-491f-bf7b-66d6a3acb047"></a>

## str_ancRES_COUNT_DECK_REPLACE

Source: `RuntimeExpressions` / `ba9fd832-0df3-491f-bf7b-66d6a3acb047`.

Reset the Deck Replace Count after a Deck Replace

Readable:
```text
GET_ANALVR(str_nDAV_CT_DECK_REPLACE)+Get_Number(1)
```

Original:
```text
GET_ANALVR(56a680b6-13bd-4b2e-a21f-df55b5cfbb9a)+Get_Number(1)
```

<a id="e-a5a31cb2-c398-469a-b302-604205ddd111"></a>

## str_ancRES_COUNT_DECK_SEAL

Source: `RuntimeExpressions` / `a5a31cb2-c398-469a-b302-604205ddd111`.

Reset the Deck Count after a Deck Seal

Readable:
```text
GET_ANALVR(str_nDAV_CT_DECK_SEAL)+Get_Number(1)
```

Original:
```text
GET_ANALVR(53a78417-71fe-42fe-a886-1f7d9d8828b2)+Get_Number(1)
```

<a id="e-bf737267-d710-49b8-be93-f60fc21692b2"></a>

## str_ancRES_COUNT_PAINT_REPLACE

Source: `RuntimeExpressions` / `bf737267-d710-49b8-be93-f60fc21692b2`.

Reset the Spot Paint Count after Painting

Readable:
```text
GET_ANALVR(str_nDAV_CT_PAINT_REPLACE)
```

Original:
```text
GET_ANALVR(e46a8d01-f162-4213-a8f2-6b42491ab409)
```

<a id="e-4e8854ab-1697-4f7b-ae37-722b5b1346fd"></a>

## str_ancRES_COUNT_SPOT_PAINT

Source: `RuntimeExpressions` / `4e8854ab-1697-4f7b-ae37-722b5b1346fd`.

Reset the Spot Paint Count after a Spot Painting

Readable:
```text
GET_ANALVR(str_nDAV_CT_SPOT_PAINT) +Get_Number(1)
```

Original:
```text
GET_ANALVR(524ce9e2-a329-4f01-b403-cb50182b7b7a) +Get_Number(1)
```

<a id="e-92c97c58-72a4-4a1c-a1b4-e595aa9f3bb4"></a>

## str_ancRES_COUNT_SUB_PLUS_1

Source: `RuntimeExpressions` / `92c97c58-72a4-4a1c-a1b4-e595aa9f3bb4`.

Reset Substructure Count Plus 1

Readable:
```text
GET_ANALVR(str_nDAV_CT_SUB_REHAB)+Get_Number(1)
```

Original:
```text
GET_ANALVR(a8d41be9-a47c-453a-9945-05e09eca34fc)+Get_Number(1)
```

<a id="e-a12f03c7-22ce-4292-b46d-b6f7545bba2a"></a>

## str_ancRES_COUNT_SUB_REHAB

Source: `RuntimeExpressions` / `a12f03c7-22ce-4292-b46d-b6f7545bba2a`.

Reset Substructure Count for a Superstructure Rehabilitation

Readable:
```text
GET_ANALVR(str_nDAV_CT_SUB_REHAB)+Get_Number(1)
```

Original:
```text
GET_ANALVR(a8d41be9-a47c-453a-9945-05e09eca34fc)+Get_Number(1)
```

<a id="e-84eccc7f-c5e1-46c2-b1ba-5273d2954e58"></a>

## str_ancRES_COUNT_SUPER_REHAB

Source: `RuntimeExpressions` / `84eccc7f-c5e1-46c2-b1ba-5273d2954e58`.

Reset Superstructure Count for a Superstructure Rehabilitation

Readable:
```text
GET_ANALVR(str_nDAV_CT_SUPER_REHAB)+Get_Number(1)
```

Original:
```text
GET_ANALVR(bf187931-c39d-452c-8f15-8754771e30cf)+Get_Number(1)
```

<a id="e-892863c6-9252-4230-9dd9-a6a075510547"></a>

## str_ancRES_CVT_CND_PLUS_3

Source: `RuntimeExpressions` / `892863c6-9252-4230-9dd9-a6a075510547`.

Reset Culver Condition Plus 3 after a reline

Readable:
```text
MIN(GET_ANALVR(str_nAAV_CND_CVT)+Get_Number(3),Get_Number(9))
```

Original:
```text
MIN(GET_ANALVR(fb31bbaf-26dc-4b1f-9e1b-31000f7ee770)+Get_Number(3),Get_Number(9))
```

<a id="e-a07185d0-3daf-4988-bcef-771de21435f2"></a>

## str_ancRES_CVT_CND_REPLACE

Source: `RuntimeExpressions` / `a07185d0-3daf-4988-bcef-771de21435f2`.

Reset Culver Condition Plus 3 after a reline

Readable:
```text
MIN(GET_ANALVR(str_nAAV_CND_CVT)+Get_Number(3),Get_Number(9))
```

Original:
```text
MIN(GET_ANALVR(fb31bbaf-26dc-4b1f-9e1b-31000f7ee770)+Get_Number(3),Get_Number(9))
```

<a id="e-d3e2453b-1795-4ac9-8790-b25263a967ea"></a>

## str_ancRES_CVT_COUNTER

Source: `dTIMSExpressions` / `d3e2453b-1795-4ac9-8790-b25263a967ea`.

Reset Counter after a change in condition

Readable:
```text
Get_Number(0)
```

Original:
```text
Get_Number(0)
```

<a id="e-64f8667f-338e-4d6a-9d14-c1780cc4b036"></a>

## str_ancRES_CVT_MARKOV

Source: `RuntimeExpressions` / `64f8667f-338e-4d6a-9d14-c1780cc4b036`.

Reset MARKOV following treatment

Readable:
```text
IF(Get_Field(CULV_RATE)='N','1',LTRIM(RTRIM(STR(GET_ANALVR(str_nAAV_CND_CVT)))))
```

Original:
```text
IF(Get_Field(176ba749-8358-42b7-97b0-5fe542dac530)='N','1',LTRIM(RTRIM(STR(GET_ANALVR(fb31bbaf-26dc-4b1f-9e1b-31000f7ee770)))))
```

<a id="e-8e338ca3-424f-46c8-bd91-247e215aa4ae"></a>

## str_ancRES_DECK_CND_PLUS_1

Source: `RuntimeExpressions` / `8e338ca3-424f-46c8-bd91-247e215aa4ae`.

Reset Substructure Condition Plus 1 after Superstructure Replacement

Readable:
```text
IF(GET_ANALVR(str_nAAV_CND_DK)<=Get_Number(6),GET_ANALVR(str_nAAV_CND_DK)+Get_Number(1),GET_ANALVR(str_nAAV_CND_DK))
```

Original:
```text
IF(GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)<=Get_Number(6),GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)+Get_Number(1),GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903))
```

<a id="e-eada4c26-58df-447d-adc3-d22a62506b75"></a>

## str_ancRES_DECK_CND_PLUS_2

Source: `RuntimeExpressions` / `eada4c26-58df-447d-adc3-d22a62506b75`.

Reset Deck Condition Plus 2 after a Rehab

Readable:
```text
GET_ANALVR(str_nAAV_CND_DK)+Get_Number(2)
```

Original:
```text
GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)+Get_Number(2)
```

<a id="e-0610076a-e6a3-4bea-a99b-e7c04d8f022e"></a>

## str_ancRES_DECK_CND_REHAB

Source: `RuntimeExpressions` / `0610076a-e6a3-4bea-a99b-e7c04d8f022e`.

Reset Deck Condition after a Rehab

Readable:
```text
MIN(GET_ANALVR(str_nAAV_CND_DK)+Get_Number(2),Get_Number(8))
```

Original:
```text
MIN(GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)+Get_Number(2),Get_Number(8))
```

<a id="e-e18bb531-f36b-4e5d-814a-7f0e41ae5963"></a>

## str_ancRES_DECK_COUNTER

Source: `dTIMSExpressions` / `e18bb531-f36b-4e5d-814a-7f0e41ae5963`.

Reset Counter after a change in condition

Readable:
```text
IF(Get_Field(DECK_RATE)='N',-Get_Number(1),Get_Number(0))
```

Original:
```text
IF(Get_Field(a945c2eb-6da7-474a-9578-818228787db6)='N',-Get_Number(1),Get_Number(0))
```

<a id="e-655a7401-13d6-4e89-8d36-cd7a1a577c82"></a>

## str_ancRES_DECK_MARKOV

Source: `RuntimeExpressions` / `655a7401-13d6-4e89-8d36-cd7a1a577c82`.

Reset MARKOV following treatment

Readable:
```text
IF(GET_ANALVR(str_nAAV_CND_DK) <=Get_Number(0),'1',LTRIM(RTRIM(STR(GET_ANALVR(str_nAAV_CND_DK)))))
```

Original:
```text
IF(GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903) <=Get_Number(0),'1',LTRIM(RTRIM(STR(GET_ANALVR(3f3a9dd3-061d-4be1-b6d0-e8f0f3a7b903)))))
```

<a id="e-fdad58cd-7850-4971-9bdd-44cb86a71ed6"></a>

## str_ancRES_JT_AGE_MINUS_5

Source: `RuntimeExpressions` / `fdad58cd-7850-4971-9bdd-44cb86a71ed6`.

Reset Joint Age Minus 5

Readable:
```text
IF(GET_ANALVR(str_nAAV_AGE_JT)>=Get_Number(0),MAX(GET_ANALVR(str_nAAV_AGE_JT)-Get_Number(5),Get_Number(0)),GET_ANALVR(str_nAAV_AGE_JT))
```

Original:
```text
IF(GET_ANALVR(020c1fda-e1fb-4392-bf66-2e3d63e765fc)>=Get_Number(0),MAX(GET_ANALVR(020c1fda-e1fb-4392-bf66-2e3d63e765fc)-Get_Number(5),Get_Number(0)),GET_ANALVR(020c1fda-e1fb-4392-bf66-2e3d63e765fc))
```

<a id="e-07d5780b-c84c-434f-b262-78534745ae6a"></a>

## str_ancRES_LMT_CULVERT_REHAB

Source: `dTIMSExpressions` / `07d5780b-c84c-434f-b262-78534745ae6a`.

Reset Last Major Treatment to Culvert_Rehab

Readable:
```text
'str_CULVERT_REHAB'
```

Original:
```text
'str_CULVERT_REHAB'
```

<a id="e-3d40d2a1-e6a4-4351-b93b-2a25e5b67982"></a>

## str_ancRES_LMT_CULVERT_REPLACE

Source: `dTIMSExpressions` / `3d40d2a1-e6a4-4351-b93b-2a25e5b67982`.

Reset Last Major Treatment to Culvert_Replace

Readable:
```text
'str_CULVERT_REPLACEMENT'
```

Original:
```text
'str_CULVERT_REPLACEMENT'
```

<a id="e-fec02752-b533-4022-93ca-d7d504e349b5"></a>

## str_ancRES_LMT_str_STRUCTURE_REPLACEMENT

Source: `dTIMSExpressions` / `fec02752-b533-4022-93ca-d7d504e349b5`.

Reset Last Major Treatment to str_STRUCTURE_REPLACEMENT

Readable:
```text
'str_STRUCTURE_REPLACEMENT'
```

Original:
```text
'str_STRUCTURE_REPLACEMENT'
```

<a id="e-1bdb021f-13c9-4c4f-9481-568a2cff692d"></a>

## str_ancRES_LMT_str_STR_MTCE

Source: `dTIMSExpressions` / `1bdb021f-13c9-4c4f-9481-568a2cff692d`.

Reset Last Major Treatment to STR_MTCE

Readable:
```text
'str_STR_MTCE'
```

Original:
```text
'str_STR_MTCE'
```

<a id="e-d3c38508-5daa-4c18-a898-10665d85d24b"></a>

## str_ancRES_LMT_str_SUPER_REPLACEMENT

Source: `dTIMSExpressions` / `d3c38508-5daa-4c18-a898-10665d85d24b`.

Reset Last Major Treatment to str_STRUCTURE_REPLACEMENT

Readable:
```text
'str_SUPER_REPLACEMENT'
```

Original:
```text
'str_SUPER_REPLACEMENT'
```

<a id="e-341937ec-3191-4a8a-a0bd-c55149f9e256"></a>

## str_ancRES_PAINT_CS1_SPOT

Source: `RuntimeExpressions` / `341937ec-3191-4a8a-a0bd-c55149f9e256`.

Reset CS1 with CS1 + CS3 for spot paint

Readable:
```text
GET_ANALVR(str_AAV_ELEM_515_CS1) + GET_ANALVR(str_AAV_ELEM_515_CS3)
```

Original:
```text
GET_ANALVR(09d1110f-48ff-442c-aca2-0d1020ef618f) + GET_ANALVR(7caba84c-5af2-4de1-aec3-c8cc44e239f9)
```

<a id="e-e5e41ca2-77c5-4555-a684-01abb90946a7"></a>

## str_ancRES_PAINT_CS2_SPOT

Source: `RuntimeExpressions` / `e5e41ca2-77c5-4555-a684-01abb90946a7`.

Reset CS2 with CS2 + CS4 for spot paint

Readable:
```text
GET_ANALVR(str_AAV_ELEM_515_CS2) + GET_ANALVR(str_AAV_ELEM_515_CS4)
```

Original:
```text
GET_ANALVR(4b1a45de-6c89-46bb-9e4e-ce75aed28cd9) + GET_ANALVR(45cc163b-7547-4c6f-a0fa-c952651c697c)
```

<a id="e-4d3cc533-e316-4bc7-81f2-fcb393ba3a42"></a>

## str_ancRES_PT_AGE_MINUS_10

Source: `RuntimeExpressions` / `4d3cc533-e316-4bc7-81f2-fcb393ba3a42`.

Reset Paint Age Minus 10

Readable:
```text
MAX(Get_Number(0),IF(GET_ANALVR(str_nAAV_AGE_PT) >=Get_Number(0),MAX(GET_ANALVR(str_nAAV_AGE_PT)-Get_Number(10),Get_Number(0)),GET_ANALVR(str_nAAV_AGE_PT)))
```

Original:
```text
MAX(Get_Number(0),IF(GET_ANALVR(2429de8f-4fad-48f9-9dc1-dd77477d9ced) >=Get_Number(0),MAX(GET_ANALVR(2429de8f-4fad-48f9-9dc1-dd77477d9ced)-Get_Number(10),Get_Number(0)),GET_ANALVR(2429de8f-4fad-48f9-9dc1-dd77477d9ced)))
```

<a id="e-ba68262c-b60f-43fb-a8e4-3bb4c144ef87"></a>

## str_ancRES_PT_AGE_MINUS_5

Source: `RuntimeExpressions` / `ba68262c-b60f-43fb-a8e4-3bb4c144ef87`.

Reset Paint Age Minus 5

Readable:
```text
IF(GET_ANALVR(str_nAAV_AGE_PT) >=Get_Number(0),MAX(GET_ANALVR(str_nAAV_AGE_PT)-Get_Number(5),Get_Number(0)),GET_ANALVR(str_nAAV_AGE_PT))
```

Original:
```text
IF(GET_ANALVR(2429de8f-4fad-48f9-9dc1-dd77477d9ced) >=Get_Number(0),MAX(GET_ANALVR(2429de8f-4fad-48f9-9dc1-dd77477d9ced)-Get_Number(5),Get_Number(0)),GET_ANALVR(2429de8f-4fad-48f9-9dc1-dd77477d9ced))
```

<a id="e-2c4a39ec-b035-41de-9e87-75be0280c001"></a>

## str_ancRES_SUBSTRUCTURE_COUNTER

Source: `dTIMSExpressions` / `2c4a39ec-b035-41de-9e87-75be0280c001`.

Reset Substructure Counter after a change in condition

Readable:
```text
IF(Get_Field(SUB_RATE)='N',-Get_Number(1),Get_Number(0))
```

Original:
```text
IF(Get_Field(710ed755-0a0b-4140-be95-783a88323b81)='N',-Get_Number(1),Get_Number(0))
```

<a id="e-af7d3cd3-189a-48ab-ad41-cf122d6d55b8"></a>

## str_ancRES_SUB_AGE_MINUS_5

Source: `RuntimeExpressions` / `af7d3cd3-189a-48ab-ad41-cf122d6d55b8`.

Reset Substructure Age Minus 5

Readable:
```text
IF(GET_ANALVR(str_nAAV_AGE_JT)>=Get_Number(0),MAX(GET_ANALVR(str_nAAV_AGE_JT)-Get_Number(5),Get_Number(0)),GET_ANALVR(str_nAAV_AGE_JT))
```

Original:
```text
IF(GET_ANALVR(020c1fda-e1fb-4392-bf66-2e3d63e765fc)>=Get_Number(0),MAX(GET_ANALVR(020c1fda-e1fb-4392-bf66-2e3d63e765fc)-Get_Number(5),Get_Number(0)),GET_ANALVR(020c1fda-e1fb-4392-bf66-2e3d63e765fc))
```

<a id="e-c6532423-2012-4894-8ee5-775c0e9a650a"></a>

## str_ancRES_SUB_CND_PLUS_1

Source: `RuntimeExpressions` / `c6532423-2012-4894-8ee5-775c0e9a650a`.

Reset Substructure Condition Plus 1 after Superstructure Replacement

Readable:
```text
IF(GET_ANALVR(str_nAAV_CND_SUB)<=Get_Number(6),GET_ANALVR(str_nAAV_CND_SUB)+Get_Number(1),GET_ANALVR(str_nAAV_CND_SUB))
```

Original:
```text
IF(GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)<=Get_Number(6),GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)+Get_Number(1),GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2))
```

<a id="e-d0f130c5-c12c-490f-b0c0-ff38e3a57be3"></a>

## str_ancRES_SUB_CND_PLUS_2

Source: `RuntimeExpressions` / `d0f130c5-c12c-490f-b0c0-ff38e3a57be3`.

Reset Substructure Condition Plus 1 after Superstructure Replacement

Readable:
```text
MIN(GET_ANALVR(str_nAAV_CND_SUB)+Get_Number(2),Get_Number(9))
```

Original:
```text
MIN(GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)+Get_Number(2),Get_Number(9))
```

<a id="e-39836a75-fdb3-4e01-8cdd-13bdab92b81c"></a>

## str_ancRES_SUB_MARKOV

Source: `RuntimeExpressions` / `39836a75-fdb3-4e01-8cdd-13bdab92b81c`.

Reset MARKOV following treatment

Readable:
```text
IF(GET_ANALVR(str_nAAV_CND_SUB)<=Get_Number(1),'1',LTRIM(RTRIM(STR(GET_ANALVR(str_nAAV_CND_SUB)))))
```

Original:
```text
IF(GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)<=Get_Number(1),'1',LTRIM(RTRIM(STR(GET_ANALVR(11650d6f-43bf-471e-a938-54048f5a11a2)))))
```

<a id="e-6ba49140-9dec-4c74-b332-6b39d566604a"></a>

## str_ancRES_SUPER_COUNTER

Source: `dTIMSExpressions` / `6ba49140-9dec-4c74-b332-6b39d566604a`.

Reset the Superstructure Counter

Readable:
```text
IF(Get_Field(SUP_RATE)='N',-Get_Number(1),Get_Number(0))
```

Original:
```text
IF(Get_Field(0515dd52-296b-4201-b684-f311c6351c28)='N',-Get_Number(1),Get_Number(0))
```

<a id="e-d58182f1-6b97-477f-998f-bfacf4b4adea"></a>

## str_ancRES_SUPER_REHAB

Source: `RuntimeExpressions` / `d58182f1-6b97-477f-998f-bfacf4b4adea`.

Reset Superstructure Condition for a Superstructure Rehabilitation

Readable:
```text
GET_ANALVR(str_nAAV_CND_SUP)+Get_Number(2)
```

Original:
```text
GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)+Get_Number(2)
```

<a id="e-7c252c7e-c6d2-4ab2-8f4b-40aa538fa19e"></a>

## str_ancRES_SUP_CND_PLUS_1

Source: `RuntimeExpressions` / `7c252c7e-c6d2-4ab2-8f4b-40aa538fa19e`.

Reset Superstructure Condition Plus 1

Readable:
```text
IF(GET_ANALVR(str_nAAV_CND_SUP)<=Get_Number(6),GET_ANALVR(str_nAAV_CND_SUP)+Get_Number(1),IF(GET_ANALVR(str_nAAV_CND_SUP)>Get_Number(6),GET_ANALVR(str_nAAV_CND_SUP),GET_ANALVR(str_nAAV_CND_SUP)))
```

Original:
```text
IF(GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)<=Get_Number(6),GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)+Get_Number(1),IF(GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)>Get_Number(6),GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8),GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)))
```

<a id="e-93b09fce-9be0-47a6-bbdf-8a3600ca60bc"></a>

## str_ancRES_SUP_CND_PLUS_2

Source: `RuntimeExpressions` / `93b09fce-9be0-47a6-bbdf-8a3600ca60bc`.

Reset Superstructure Condition Plus 2

Readable:
```text
IF(GET_ANALVR(str_nAAV_CND_SUP)<=Get_Number(6),GET_ANALVR(str_nAAV_CND_SUP)+Get_Number(2),IF(GET_ANALVR(str_nAAV_CND_SUP)<=Get_Number(7),GET_ANALVR(str_nAAV_CND_SUP)+Get_Number(2)-(Get_Number(8)-GET_ANALVR(str_nAAV_CND_SUP)),IF(GET_ANALVR(str_nAAV_CND_SUP)<Get_Number(8),GET_ANALVR(str_nAAV_CND_SUP)+Get_Number(1)-(Get_Number(8)-GET_ANALVR(str_nAAV_CND_SUP)),GET_ANALVR(str_nAAV_CND_SUP))))
```

Original:
```text
IF(GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)<=Get_Number(6),GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)+Get_Number(2),IF(GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)<=Get_Number(7),GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)+Get_Number(2)-(Get_Number(8)-GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)),IF(GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)<Get_Number(8),GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)+Get_Number(1)-(Get_Number(8)-GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)),GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8))))
```

<a id="e-7bf14a3d-a09b-4317-9ca5-09abd48867fa"></a>

## str_ancRES_SUP_MARKOV

Source: `RuntimeExpressions` / `7bf14a3d-a09b-4317-9ca5-09abd48867fa`.

Reset MARKOV following treatment

Readable:
```text
IF(GET_ANALVR(str_nAAV_CND_SUP) < Get_Number(1),'1',LTRIM(RTRIM(STR(GET_ANALVR(str_nAAV_CND_SUP)))))
```

Original:
```text
IF(GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8) < Get_Number(1),'1',LTRIM(RTRIM(STR(GET_ANALVR(55dcd4f2-c911-42fe-9154-cba35cb10fc8)))))
```

<a id="e-4fe97019-596b-4b61-b9ee-b2bea5717564"></a>

## str_ancRES_WS_AGE_MINUS_5

Source: `RuntimeExpressions` / `4fe97019-596b-4b61-b9ee-b2bea5717564`.

Reset Wearing Surface Age for a Deck Seal

Readable:
```text
MAX(GET_ANALVR(str_nAAV_AGE_WS) - Get_Number(5),Get_Number(0))
```

Original:
```text
MAX(GET_ANALVR(226eb77f-d010-4568-b39b-acbd649aa6c2) - Get_Number(5),Get_Number(0))
```

<a id="e-a34cccf7-5b55-4b85-98a9-f699aef322d0"></a>

## str_ancTRF_ADT

Source: `RuntimeExpressions` / `a34cccf7-5b55-4b85-98a9-f699aef322d0`.

Traffic ADT

Readable:
```text
GET_ANALVR(str_nAAV_TRF_ADT) * Get_Number(1.02)
```

Original:
```text
GET_ANALVR(5354dc5d-c869-4579-8ae4-eb60a9c12614) * Get_Number(1.02)
```

<a id="e-a34c2a48-0d66-4817-bb33-9d2d832ad968"></a>

## str_ancTRF_ADT_INITIALIZE

Source: `dTIMSExpressions` / `a34c2a48-0d66-4817-bb33-9d2d832ad968`.

Initialize ADT 

Readable:
```text
IF(IFDEFAULT(Get_Field(ADT)) OR Get_Field(ADT) <= Get_Number(0), Get_Number(100),Get_Field(ADT))
```

Original:
```text
IF(IFDEFAULT(Get_Field(ffe68e09-e9f1-40ff-8efa-58cf5a382403)) OR Get_Field(ffe68e09-e9f1-40ff-8efa-58cf5a382403) <= Get_Number(0), Get_Number(100),Get_Field(ffe68e09-e9f1-40ff-8efa-58cf5a382403))
```

<a id="e-6e433015-58a6-4d47-ae8a-cc88fe7e70f1"></a>

## str_anc_AAV_Elem_1080_CS1_All

Source: `RuntimeExpressions` / `6e433015-58a6-4d47-ae8a-cc88fe7e70f1`.

Predict CS1 in Future Years


Readable:
```text
IF(Get_Field(ELEM_1080_QUANTITY)>Get_Number(0),
    GET_ANALVAR_4_YR(str_AAV_ELEM_1080_CS1,YR-Get_Number(1))*(Get_Exp(str_anc_AAV_Elem_1080_CS1_P1)-MIN(Get_Exp(str_anc_AAV_Elem_1080_CS1_FACTOR)*GET_ANALVR(str_AAV_ELEM_1080_Counter)/Get_Number(100),Get_Number(1))),Get_Number(0))
```

Original:
```text
IF(Get_Field(56df5f38-8963-4729-9821-1948e051b920)>Get_Number(0),
    GET_ANALVAR_4_YR(b0325986-565f-4dc9-9ee7-c37d3f531a04,YR-Get_Number(1))*(Get_Exp(a5935f2b-0fc3-436c-8f61-319dfccccb3b)-MIN(Get_Exp(3a623220-924f-408f-b647-c92a203bae86)*GET_ANALVR(d8852ad3-65b5-4c17-84fe-0cd35aa62884)/Get_Number(100),Get_Number(1))),Get_Number(0))
```

<a id="e-3a623220-924f-408f-b647-c92a203bae86"></a>

## str_anc_AAV_Elem_1080_CS1_FACTOR

Source: `RuntimeExpressions` / `3a623220-924f-408f-b647-c92a203bae86`.

Return CS1 Deterioration Factor for Elem 1080

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','FACTOR','Name','1080_CS1',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','FACTOR','Name','1080_CS1',TRUE))
```

<a id="e-fe2807b1-ac5a-4be1-aa30-60958f21392e"></a>

## str_anc_AAV_Elem_1080_CS1_Initialize

Source: `dTIMSExpressions` / `fe2807b1-ac5a-4be1-aa30-60958f21392e`.

Initialize ELEM 1080 CS1

Readable:
```text
IF(Get_Field(ELEM_1080_QUANTITY)>Get_Number(0),Get_Field(ELEM_1080_CS1)/Get_Field(ELEM_1080_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(56df5f38-8963-4729-9821-1948e051b920)>Get_Number(0),Get_Field(9a355f8c-096d-43cd-b02d-25f24485b79c)/Get_Field(56df5f38-8963-4729-9821-1948e051b920)*Get_Number(100),Get_Number(0))
```

<a id="e-a5935f2b-0fc3-436c-8f61-319dfccccb3b"></a>

## str_anc_AAV_Elem_1080_CS1_P1

Source: `RuntimeExpressions` / `a5935f2b-0fc3-436c-8f61-319dfccccb3b`.

Return CS1 P1 for Element 1080

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS1','Name','1080_CS1',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS1','Name','1080_CS1',TRUE))
```

<a id="e-2987c551-ac96-4c0e-b0c3-551ecc8ac825"></a>

## str_anc_AAV_Elem_1080_CS2_All

Source: `RuntimeExpressions` / `2987c551-ac96-4c0e-b0c3-551ecc8ac825`.

Predict CS2 in Future Years

Readable:
```text
IF(Get_Field(ELEM_1080_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_1080_CS2,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_1080_CS2_P2)+GET_ANALVAR_4_YR(str_AAV_ELEM_1080_CS1,YR-Get_Number(1))-GET_ANALVR(str_AAV_ELEM_1080_CS1),Get_Number(0))
```

Original:
```text
IF(Get_Field(56df5f38-8963-4729-9821-1948e051b920)>Get_Number(0),GET_ANALVAR_4_YR(cb7d38d8-016f-4634-b0af-2f9fbb5f01d9,YR-Get_Number(1))*Get_Exp(a3276821-c6d3-4dce-b666-55149ca339ae)+GET_ANALVAR_4_YR(b0325986-565f-4dc9-9ee7-c37d3f531a04,YR-Get_Number(1))-GET_ANALVR(b0325986-565f-4dc9-9ee7-c37d3f531a04),Get_Number(0))
```

<a id="e-bf4d8843-d222-4a91-8723-9b54c599f713"></a>

## str_anc_AAV_Elem_1080_CS2_Initialize

Source: `dTIMSExpressions` / `bf4d8843-d222-4a91-8723-9b54c599f713`.

Initialize ELEM 1080 CS2

Readable:
```text
IF(Get_Field(ELEM_1080_QUANTITY)>Get_Number(0),Get_Field(ELEM_1080_CS2)/Get_Field(ELEM_1080_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(56df5f38-8963-4729-9821-1948e051b920)>Get_Number(0),Get_Field(9951d365-44b3-4e8d-854a-65e9128c84b2)/Get_Field(56df5f38-8963-4729-9821-1948e051b920)*Get_Number(100),Get_Number(0))
```

<a id="e-a3276821-c6d3-4dce-b666-55149ca339ae"></a>

## str_anc_AAV_Elem_1080_CS2_P2

Source: `RuntimeExpressions` / `a3276821-c6d3-4dce-b666-55149ca339ae`.

Return CS2 P2 for Element 1080

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS2','Name','1080_CS2',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS2','Name','1080_CS2',TRUE))
```

<a id="e-343a0369-d419-45b8-80c1-003e7b0e5157"></a>

## str_anc_AAV_Elem_1080_CS2_P3

Source: `RuntimeExpressions` / `343a0369-d419-45b8-80c1-003e7b0e5157`.

Return CS2 P3 for Element 1080

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','1080_CS2',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','1080_CS2',TRUE))
```

<a id="e-09ff446e-6bd0-48e9-8ac4-57f048a3eb93"></a>

## str_anc_AAV_Elem_1080_CS3_All

Source: `RuntimeExpressions` / `09ff446e-6bd0-48e9-8ac4-57f048a3eb93`.

Predict CS3 in Future Years

Readable:
```text
IF(Get_Field(ELEM_1080_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_1080_CS3,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_1080_CS3_P3)+GET_ANALVAR_4_YR(str_AAV_ELEM_1080_CS2,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_1080_CS2_P3),Get_Number(0))
```

Original:
```text
IF(Get_Field(56df5f38-8963-4729-9821-1948e051b920)>Get_Number(0),GET_ANALVAR_4_YR(53bec880-322b-4ac1-a03a-c79fb354c4fb,YR-Get_Number(1))*Get_Exp(c9e62946-9204-476b-9761-68fd802c57f9)+GET_ANALVAR_4_YR(cb7d38d8-016f-4634-b0af-2f9fbb5f01d9,YR-Get_Number(1))*Get_Exp(343a0369-d419-45b8-80c1-003e7b0e5157),Get_Number(0))
```

<a id="e-787f5044-7379-4edd-aae2-7a2e757d129a"></a>

## str_anc_AAV_Elem_1080_CS3_Initialize

Source: `dTIMSExpressions` / `787f5044-7379-4edd-aae2-7a2e757d129a`.

Initialize ELEM 1080 CS3

Readable:
```text
IF(Get_Field(ELEM_1080_QUANTITY)>Get_Number(0),Get_Field(ELEM_1080_CS3)/Get_Field(ELEM_1080_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(56df5f38-8963-4729-9821-1948e051b920)>Get_Number(0),Get_Field(4f62eda2-3351-47f8-b5fb-f1ac14d7a8b2)/Get_Field(56df5f38-8963-4729-9821-1948e051b920)*Get_Number(100),Get_Number(0))
```

<a id="e-c9e62946-9204-476b-9761-68fd802c57f9"></a>

## str_anc_AAV_Elem_1080_CS3_P3

Source: `RuntimeExpressions` / `c9e62946-9204-476b-9761-68fd802c57f9`.

Return CS3 P3 for Element 1080

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','1080_CS3',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','1080_CS3',TRUE))
```

<a id="e-09bf9414-c525-4af4-9388-51580d9cc3df"></a>

## str_anc_AAV_Elem_1080_CS3_P4

Source: `RuntimeExpressions` / `09bf9414-c525-4af4-9388-51580d9cc3df`.

Return CS3 P4 for Element 1080

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS4','Name','1080_CS3',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS4','Name','1080_CS3',TRUE))
```

<a id="e-691de05d-0f4a-4941-834f-5d2705886427"></a>

## str_anc_AAV_Elem_1080_CS4_All

Source: `RuntimeExpressions` / `691de05d-0f4a-4941-834f-5d2705886427`.

Predict CS4 in Future Years

Readable:
```text
IF(Get_Field(ELEM_1080_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_1080_CS4,YR-Get_Number(1))+GET_ANALVAR_4_YR(str_AAV_ELEM_1080_CS3,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_1080_CS3_P4),Get_Number(0))
```

Original:
```text
IF(Get_Field(56df5f38-8963-4729-9821-1948e051b920)>Get_Number(0),GET_ANALVAR_4_YR(454eb22e-95d5-4589-9f60-860fbaaff091,YR-Get_Number(1))+GET_ANALVAR_4_YR(53bec880-322b-4ac1-a03a-c79fb354c4fb,YR-Get_Number(1))*Get_Exp(09bf9414-c525-4af4-9388-51580d9cc3df),Get_Number(0))
```

<a id="e-bfbe3968-e5e7-4a36-af75-c2913a1a27f2"></a>

## str_anc_AAV_Elem_1080_CS4_Initialize

Source: `dTIMSExpressions` / `bfbe3968-e5e7-4a36-af75-c2913a1a27f2`.

Initialize ELEM 1080 CS4

Readable:
```text
IF(Get_Field(ELEM_1080_QUANTITY)>Get_Number(0),Get_Field(ELEM_1080_CS4)/Get_Field(ELEM_1080_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(56df5f38-8963-4729-9821-1948e051b920)>Get_Number(0),Get_Field(c97ab4f7-c248-4c2c-a463-f36c0f4a0247)/Get_Field(56df5f38-8963-4729-9821-1948e051b920)*Get_Number(100),Get_Number(0))
```

<a id="e-52cf8682-4d2a-4777-adab-6252f31bbd08"></a>

## str_anc_AAV_Elem_1080_Counter_All

Source: `RuntimeExpressions` / `52cf8682-4d2a-4777-adab-6252f31bbd08`.

Increment the Elem 1080 Counter


Readable:
```text
MIN(GET_ANALVR(str_AAV_ELEM_1080_Counter)+Get_Number(1),Get_Number(50))
```

Original:
```text
MIN(GET_ANALVR(d8852ad3-65b5-4c17-84fe-0cd35aa62884)+Get_Number(1),Get_Number(50))
```

<a id="e-661996cc-13dd-4db8-989b-757e9c6c68d8"></a>

## str_anc_AAV_Elem_1130_CS1_All

Source: `RuntimeExpressions` / `661996cc-13dd-4db8-989b-757e9c6c68d8`.

Predict CS1 in Future Years

Readable:
```text
IF(Get_Field(ELEM_1130_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_1130_CS1,YR-Get_Number(1))*(Get_Exp(str_anc_AAV_Elem_1130_CS1_P1)-MIN(Get_Exp(str_anc_AAV_Elem_1130_CS1_FACTOR)*GET_ANALVR(str_AAV_ELEM_1130_Counter)/Get_Number(100),Get_Number(1))),Get_Number(0))
```

Original:
```text
IF(Get_Field(c1f78423-32d6-423c-b986-b5855431bbb3)>Get_Number(0),GET_ANALVAR_4_YR(7e1f5c6a-5d85-4454-8753-ed3f0a0c7e57,YR-Get_Number(1))*(Get_Exp(7cc4e4e3-0bc2-407d-8d57-2ff27832904c)-MIN(Get_Exp(ac2fc182-692d-4236-86bc-bce44a597b33)*GET_ANALVR(09cf07aa-7c71-4d62-a0f4-d8ca78cc198d)/Get_Number(100),Get_Number(1))),Get_Number(0))
```

<a id="e-ac2fc182-692d-4236-86bc-bce44a597b33"></a>

## str_anc_AAV_Elem_1130_CS1_FACTOR

Source: `RuntimeExpressions` / `ac2fc182-692d-4236-86bc-bce44a597b33`.

Return CS1 Deterioration Factor for Elem 1130

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','FACTOR','Name','1130_CS1',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','FACTOR','Name','1130_CS1',TRUE))
```

<a id="e-74d42212-ee6e-4fe7-99c0-46ca2dc2cff7"></a>

## str_anc_AAV_Elem_1130_CS1_Initialize

Source: `dTIMSExpressions` / `74d42212-ee6e-4fe7-99c0-46ca2dc2cff7`.

Initialize ELEM 1130 CS1

Readable:
```text
IF(Get_Field(ELEM_1130_QUANTITY)>Get_Number(0),Get_Field(ELEM_1130_CS1)/Get_Field(ELEM_1130_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(c1f78423-32d6-423c-b986-b5855431bbb3)>Get_Number(0),Get_Field(6c651ff3-1bb8-4041-979e-f9f2eec4fd3c)/Get_Field(c1f78423-32d6-423c-b986-b5855431bbb3)*Get_Number(100),Get_Number(0))
```

<a id="e-7cc4e4e3-0bc2-407d-8d57-2ff27832904c"></a>

## str_anc_AAV_Elem_1130_CS1_P1

Source: `RuntimeExpressions` / `7cc4e4e3-0bc2-407d-8d57-2ff27832904c`.

Return CS1 P1 for Element 1130

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS1','Name','1130_CS1',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS1','Name','1130_CS1',TRUE))
```

<a id="e-85b06186-d325-4842-ae08-2d533a5f54a3"></a>

## str_anc_AAV_Elem_1130_CS2_All

Source: `RuntimeExpressions` / `85b06186-d325-4842-ae08-2d533a5f54a3`.

Predict CS2 in Future Years

Readable:
```text
IF(Get_Field(ELEM_1130_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_1130_CS2,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_1130_CS2_P2)+GET_ANALVAR_4_YR(str_AAV_ELEM_1130_CS1,YR-Get_Number(1))-GET_ANALVR(str_AAV_ELEM_1130_CS1),Get_Number(0))
```

Original:
```text
IF(Get_Field(c1f78423-32d6-423c-b986-b5855431bbb3)>Get_Number(0),GET_ANALVAR_4_YR(d4ec2fc2-ba02-437d-99d9-61868339cc5c,YR-Get_Number(1))*Get_Exp(019c9927-2b1e-4af0-a33a-a35575975a68)+GET_ANALVAR_4_YR(7e1f5c6a-5d85-4454-8753-ed3f0a0c7e57,YR-Get_Number(1))-GET_ANALVR(7e1f5c6a-5d85-4454-8753-ed3f0a0c7e57),Get_Number(0))
```

<a id="e-09b5500b-fe63-44c5-a5e5-d81b11da42ef"></a>

## str_anc_AAV_Elem_1130_CS2_Initialize

Source: `dTIMSExpressions` / `09b5500b-fe63-44c5-a5e5-d81b11da42ef`.

Initialize ELEM 1130 CS2

Readable:
```text
IF(Get_Field(ELEM_1130_QUANTITY)>Get_Number(0),Get_Field(ELEM_1130_CS2)/Get_Field(ELEM_1130_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(c1f78423-32d6-423c-b986-b5855431bbb3)>Get_Number(0),Get_Field(545fa213-71de-4368-ab91-f4ff330ffb6d)/Get_Field(c1f78423-32d6-423c-b986-b5855431bbb3)*Get_Number(100),Get_Number(0))
```

<a id="e-019c9927-2b1e-4af0-a33a-a35575975a68"></a>

## str_anc_AAV_Elem_1130_CS2_P2

Source: `RuntimeExpressions` / `019c9927-2b1e-4af0-a33a-a35575975a68`.

Return CS2 P2 for Element 1130

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS2','Name','1130_CS2',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS2','Name','1130_CS2',TRUE))
```

<a id="e-8a0e2873-0607-42c4-85a0-71334e1c8902"></a>

## str_anc_AAV_Elem_1130_CS2_P3

Source: `RuntimeExpressions` / `8a0e2873-0607-42c4-85a0-71334e1c8902`.

Return CS2 P3 for Element 1130

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','1130_CS2',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','1130_CS2',TRUE))
```

<a id="e-3693f71e-9afe-4a9f-ba1d-fd4324f464a9"></a>

## str_anc_AAV_Elem_1130_CS3_All

Source: `RuntimeExpressions` / `3693f71e-9afe-4a9f-ba1d-fd4324f464a9`.

Predict CS3 in Future Years

Readable:
```text
IF(Get_Field(ELEM_1130_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_1130_CS3,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_1130_CS3_P3)+GET_ANALVAR_4_YR(str_AAV_ELEM_1130_CS2,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_1130_CS2_P3),Get_Number(0))
```

Original:
```text
IF(Get_Field(c1f78423-32d6-423c-b986-b5855431bbb3)>Get_Number(0),GET_ANALVAR_4_YR(f4f23edc-9d5d-47b7-95aa-5f2f7b2185b8,YR-Get_Number(1))*Get_Exp(98650c3e-5552-470c-8a15-0257f8026bea)+GET_ANALVAR_4_YR(d4ec2fc2-ba02-437d-99d9-61868339cc5c,YR-Get_Number(1))*Get_Exp(8a0e2873-0607-42c4-85a0-71334e1c8902),Get_Number(0))
```

<a id="e-a449ace6-ab2a-49f5-913a-7b43fa79d650"></a>

## str_anc_AAV_Elem_1130_CS3_Initialize

Source: `dTIMSExpressions` / `a449ace6-ab2a-49f5-913a-7b43fa79d650`.

Initialize ELEM 1130 CS3

Readable:
```text
IF(Get_Field(ELEM_1130_QUANTITY)>Get_Number(0),Get_Field(ELEM_1130_CS3)/Get_Field(ELEM_1130_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(c1f78423-32d6-423c-b986-b5855431bbb3)>Get_Number(0),Get_Field(e8db8045-e9b3-4486-b23c-60725e6d681a)/Get_Field(c1f78423-32d6-423c-b986-b5855431bbb3)*Get_Number(100),Get_Number(0))
```

<a id="e-98650c3e-5552-470c-8a15-0257f8026bea"></a>

## str_anc_AAV_Elem_1130_CS3_P3

Source: `RuntimeExpressions` / `98650c3e-5552-470c-8a15-0257f8026bea`.

Return CS3 P3 for Element 1130

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','1130_CS3',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','1130_CS3',TRUE))
```

<a id="e-5d66b9fa-01ec-4f2f-ad93-be16c4bd77ab"></a>

## str_anc_AAV_Elem_1130_CS3_P4

Source: `RuntimeExpressions` / `5d66b9fa-01ec-4f2f-ad93-be16c4bd77ab`.

Return CS3 P4 for Element 1130

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS4','Name','1130_CS3',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS4','Name','1130_CS3',TRUE))
```

<a id="e-9645eda8-9990-4ce4-9ad0-2ddcd7e6ed5e"></a>

## str_anc_AAV_Elem_1130_CS4_All

Source: `RuntimeExpressions` / `9645eda8-9990-4ce4-9ad0-2ddcd7e6ed5e`.

Predict CS4 in Future Years

Readable:
```text
IF(Get_Field(ELEM_1130_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_1130_CS4,YR-Get_Number(1))+GET_ANALVAR_4_YR(str_AAV_ELEM_1130_CS3,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_1130_CS3_P4),Get_Number(0))
```

Original:
```text
IF(Get_Field(c1f78423-32d6-423c-b986-b5855431bbb3)>Get_Number(0),GET_ANALVAR_4_YR(f48f853b-addf-4a1e-bd24-dd4c31f38a08,YR-Get_Number(1))+GET_ANALVAR_4_YR(f4f23edc-9d5d-47b7-95aa-5f2f7b2185b8,YR-Get_Number(1))*Get_Exp(5d66b9fa-01ec-4f2f-ad93-be16c4bd77ab),Get_Number(0))
```

<a id="e-241c08b7-7862-4bc3-8c2f-0cbfc503cdcc"></a>

## str_anc_AAV_Elem_1130_CS4_Initialize

Source: `dTIMSExpressions` / `241c08b7-7862-4bc3-8c2f-0cbfc503cdcc`.

Initialize ELEM 1130 CS4

Readable:
```text
IF(Get_Field(ELEM_1130_QUANTITY)>Get_Number(0),Get_Field(ELEM_1130_CS4)/Get_Field(ELEM_1130_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(c1f78423-32d6-423c-b986-b5855431bbb3)>Get_Number(0),Get_Field(94077a8a-46d0-4e31-9203-3b75cf8afd93)/Get_Field(c1f78423-32d6-423c-b986-b5855431bbb3)*Get_Number(100),Get_Number(0))
```

<a id="e-5f956b9a-1fbc-4993-9b5c-fef2fddef1e3"></a>

## str_anc_AAV_Elem_1130_Counter_All

Source: `RuntimeExpressions` / `5f956b9a-1fbc-4993-9b5c-fef2fddef1e3`.

Increment the Elem 1130 Counter


Readable:
```text
MIN(GET_ANALVR(str_AAV_ELEM_1130_Counter)+Get_Number(1),Get_Number(50))
```

Original:
```text
MIN(GET_ANALVR(09cf07aa-7c71-4d62-a0f4-d8ca78cc198d)+Get_Number(1),Get_Number(50))
```

<a id="e-e57f5c85-d949-4656-b976-17b1fb75954c"></a>

## str_anc_AAV_Elem_300_CS1_All

Source: `RuntimeExpressions` / `e57f5c85-d949-4656-b976-17b1fb75954c`.

Predict CS1 in Future Years

Readable:
```text
IF(Get_Field(ELEM_300_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_300_CS1,YR-Get_Number(1))*(Get_Exp(str_anc_AAV_Elem_300_CS1_P1)-MIN(Get_Exp(str_anc_AAV_Elem_300_CS1_FACTOR)*GET_ANALVR(str_AAV_ELEM_300_Counter)/Get_Number(100),Get_Number(1))),Get_Number(0))
```

Original:
```text
IF(Get_Field(9aedad63-77e7-447a-8c44-21a89ae03440)>Get_Number(0),GET_ANALVAR_4_YR(61744dc1-277d-4fec-a8e3-cce8e31ebaeb,YR-Get_Number(1))*(Get_Exp(a493fd0c-f859-48a9-9b16-b97a39f83589)-MIN(Get_Exp(6f9e4192-1fdd-40d4-9776-f73ae1d5d281)*GET_ANALVR(630a68e4-8c22-44dc-a92c-d5e5e012b1ac)/Get_Number(100),Get_Number(1))),Get_Number(0))
```

<a id="e-6f9e4192-1fdd-40d4-9776-f73ae1d5d281"></a>

## str_anc_AAV_Elem_300_CS1_FACTOR

Source: `RuntimeExpressions` / `6f9e4192-1fdd-40d4-9776-f73ae1d5d281`.

Return CS1 Deterioration Factor for Elem 300

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','FACTOR','Name','300_CS1',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','FACTOR','Name','300_CS1',TRUE))
```

<a id="e-4c6461f4-d64b-47b2-9ffb-8d565072a006"></a>

## str_anc_AAV_Elem_300_CS1_Initialize

Source: `dTIMSExpressions` / `4c6461f4-d64b-47b2-9ffb-8d565072a006`.

Initialize ELEM 300 CS1

Readable:
```text
IF(Get_Field(ELEM_300_QUANTITY)>Get_Number(0),Get_Field(ELEM_300_CS1)/Get_Field(ELEM_300_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(9aedad63-77e7-447a-8c44-21a89ae03440)>Get_Number(0),Get_Field(f39d1c31-aad6-4c63-bd1b-5c8d013dd909)/Get_Field(9aedad63-77e7-447a-8c44-21a89ae03440)*Get_Number(100),Get_Number(0))
```

<a id="e-a493fd0c-f859-48a9-9b16-b97a39f83589"></a>

## str_anc_AAV_Elem_300_CS1_P1

Source: `RuntimeExpressions` / `a493fd0c-f859-48a9-9b16-b97a39f83589`.

Return CS1 P1 for Element 300

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS1','Name','300_CS1',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS1','Name','300_CS1',TRUE))
```

<a id="e-b3f06f19-8c95-4dd5-bdcf-0128c7cd526b"></a>

## str_anc_AAV_Elem_300_CS21_All

Source: `RuntimeExpressions` / `b3f06f19-8c95-4dd5-bdcf-0128c7cd526b`.

Predict CS2 in Future Years

Readable:
```text
IF(Get_Field(ELEM_300_QUANTITY)>Get_Number(0),
GET_ANALVAR_4_YR(str_AAV_ELEM_300_CS2,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_300_CS2_P2)+GET_ANALVAR_4_YR(str_AAV_ELEM_300_CS1,YR-Get_Number(1))-
GET_ANALVR(str_AAV_ELEM_300_CS1),Get_Number(0))
```

Original:
```text
IF(Get_Field(9aedad63-77e7-447a-8c44-21a89ae03440)>Get_Number(0),
GET_ANALVAR_4_YR(0e387c7a-fc84-4a7c-a208-e970a49c5453,YR-Get_Number(1))*Get_Exp(7dc6d7bd-667d-496f-bb5b-75b8355ec724)+GET_ANALVAR_4_YR(61744dc1-277d-4fec-a8e3-cce8e31ebaeb,YR-Get_Number(1))-
GET_ANALVR(61744dc1-277d-4fec-a8e3-cce8e31ebaeb),Get_Number(0))
```

<a id="e-53d43b36-df86-4997-8e89-d2c0889369da"></a>

## str_anc_AAV_Elem_300_CS2_All

Source: `RuntimeExpressions` / `53d43b36-df86-4997-8e89-d2c0889369da`.

Predict CS2 in Future Years

Readable:
```text
IF(Get_Field(ELEM_300_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_300_CS2,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_300_CS2_P2)+GET_ANALVAR_4_YR(str_AAV_ELEM_300_CS1,YR-Get_Number(1))-GET_ANALVR(str_AAV_ELEM_300_CS1),Get_Number(0))
```

Original:
```text
IF(Get_Field(9aedad63-77e7-447a-8c44-21a89ae03440)>Get_Number(0),GET_ANALVAR_4_YR(0e387c7a-fc84-4a7c-a208-e970a49c5453,YR-Get_Number(1))*Get_Exp(7dc6d7bd-667d-496f-bb5b-75b8355ec724)+GET_ANALVAR_4_YR(61744dc1-277d-4fec-a8e3-cce8e31ebaeb,YR-Get_Number(1))-GET_ANALVR(61744dc1-277d-4fec-a8e3-cce8e31ebaeb),Get_Number(0))
```

<a id="e-40a844c1-abe9-4bfe-9bcb-21ae8c1efe02"></a>

## str_anc_AAV_Elem_300_CS2_Initialize

Source: `dTIMSExpressions` / `40a844c1-abe9-4bfe-9bcb-21ae8c1efe02`.

Initialize ELEM 300 CS2

Readable:
```text
IF(Get_Field(ELEM_300_QUANTITY)>Get_Number(0),Get_Field(ELEM_300_CS2)/Get_Field(ELEM_300_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(9aedad63-77e7-447a-8c44-21a89ae03440)>Get_Number(0),Get_Field(cd1fd232-963d-4c14-8d0a-0cd3cc2914d6)/Get_Field(9aedad63-77e7-447a-8c44-21a89ae03440)*Get_Number(100),Get_Number(0))
```

<a id="e-7dc6d7bd-667d-496f-bb5b-75b8355ec724"></a>

## str_anc_AAV_Elem_300_CS2_P2

Source: `RuntimeExpressions` / `7dc6d7bd-667d-496f-bb5b-75b8355ec724`.

Return CS2 P2 for Element 300

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS2','Name','300_CS2',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS2','Name','300_CS2',TRUE))
```

<a id="e-336472c8-8773-4527-8e6f-93ec742d12c8"></a>

## str_anc_AAV_Elem_300_CS2_P3

Source: `RuntimeExpressions` / `336472c8-8773-4527-8e6f-93ec742d12c8`.

Return CS2 P3 for Element 300

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','300_CS2',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','300_CS2',TRUE))
```

<a id="e-7e74a78d-4332-4323-a16d-c53320a46acf"></a>

## str_anc_AAV_Elem_300_CS3_All

Source: `RuntimeExpressions` / `7e74a78d-4332-4323-a16d-c53320a46acf`.

Predict CS3 in Future Years

Readable:
```text
IF(Get_Field(ELEM_300_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_300_CS3,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_300_CS3_P3)+GET_ANALVAR_4_YR(str_AAV_ELEM_300_CS2,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_300_CS2_P3),Get_Number(0))
```

Original:
```text
IF(Get_Field(9aedad63-77e7-447a-8c44-21a89ae03440)>Get_Number(0),GET_ANALVAR_4_YR(bb237542-c49f-47fc-8b30-5087beb8b3e7,YR-Get_Number(1))*Get_Exp(9ee3305b-c1c7-4efe-a70a-246ed769c44e)+GET_ANALVAR_4_YR(0e387c7a-fc84-4a7c-a208-e970a49c5453,YR-Get_Number(1))*Get_Exp(336472c8-8773-4527-8e6f-93ec742d12c8),Get_Number(0))
```

<a id="e-ed353ea2-f188-4e67-af52-41c59e0b7a30"></a>

## str_anc_AAV_Elem_300_CS3_Initialize

Source: `dTIMSExpressions` / `ed353ea2-f188-4e67-af52-41c59e0b7a30`.

Initialize ELEM 300 CS3

Readable:
```text
IF(Get_Field(ELEM_300_QUANTITY)>Get_Number(0),Get_Field(ELEM_300_CS3)/Get_Field(ELEM_300_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(9aedad63-77e7-447a-8c44-21a89ae03440)>Get_Number(0),Get_Field(9ddc9b50-5506-486e-aa57-b007b2aba4a4)/Get_Field(9aedad63-77e7-447a-8c44-21a89ae03440)*Get_Number(100),Get_Number(0))
```

<a id="e-9ee3305b-c1c7-4efe-a70a-246ed769c44e"></a>

## str_anc_AAV_Elem_300_CS3_P3

Source: `RuntimeExpressions` / `9ee3305b-c1c7-4efe-a70a-246ed769c44e`.

Return CS3 P3 for Element 300

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','300_CS3',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','300_CS3',TRUE))
```

<a id="e-1f15d142-916e-4537-9ea1-3eb66e0d9387"></a>

## str_anc_AAV_Elem_300_CS3_P4

Source: `RuntimeExpressions` / `1f15d142-916e-4537-9ea1-3eb66e0d9387`.

Return CS3 P4 for Element 300

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS4','Name','300_CS3',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS4','Name','300_CS3',TRUE))
```

<a id="e-82c9ae46-9f4a-4198-92d2-43caaa2e8aed"></a>

## str_anc_AAV_Elem_300_CS4_All

Source: `RuntimeExpressions` / `82c9ae46-9f4a-4198-92d2-43caaa2e8aed`.

Predict CS4 in Future Years

Readable:
```text
IF(Get_Field(ELEM_300_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_300_CS4,YR-Get_Number(1))+GET_ANALVAR_4_YR(str_AAV_ELEM_300_CS3,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_300_CS3_P4),Get_Number(0))
```

Original:
```text
IF(Get_Field(9aedad63-77e7-447a-8c44-21a89ae03440)>Get_Number(0),GET_ANALVAR_4_YR(f53ec4ee-84a2-4951-95d5-85645f3c610e,YR-Get_Number(1))+GET_ANALVAR_4_YR(bb237542-c49f-47fc-8b30-5087beb8b3e7,YR-Get_Number(1))*Get_Exp(1f15d142-916e-4537-9ea1-3eb66e0d9387),Get_Number(0))
```

<a id="e-b95c5674-8cae-480d-af07-06417d08f81f"></a>

## str_anc_AAV_Elem_300_CS4_Initialize

Source: `dTIMSExpressions` / `b95c5674-8cae-480d-af07-06417d08f81f`.

Initialize ELEM 300 CS4

Readable:
```text
IF(Get_Field(ELEM_300_QUANTITY)>Get_Number(0),Get_Field(ELEM_300_CS4)/Get_Field(ELEM_300_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(9aedad63-77e7-447a-8c44-21a89ae03440)>Get_Number(0),Get_Field(6dc8144b-21ec-4f27-9008-614d16257866)/Get_Field(9aedad63-77e7-447a-8c44-21a89ae03440)*Get_Number(100),Get_Number(0))
```

<a id="e-6515fe98-c2b9-4e01-a503-3f820a07622f"></a>

## str_anc_AAV_Elem_300_Counter_All

Source: `RuntimeExpressions` / `6515fe98-c2b9-4e01-a503-3f820a07622f`.

Increment the Elem 300 Counter


Readable:
```text
MIN(GET_ANALVR(str_AAV_ELEM_300_Counter)+Get_Number(1),Get_Number(50))
```

Original:
```text
MIN(GET_ANALVR(630a68e4-8c22-44dc-a92c-d5e5e012b1ac)+Get_Number(1),Get_Number(50))
```

<a id="e-e773cca1-343f-417e-a11b-bf5c073fa7aa"></a>

## str_anc_AAV_Elem_301_CS1_All

Source: `RuntimeExpressions` / `e773cca1-343f-417e-a11b-bf5c073fa7aa`.

Predict CS1 in Future Years

Readable:
```text
IF(Get_Field(ELEM_301_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_301_CS1,YR-Get_Number(1))*(Get_Exp(str_anc_AAV_Elem_301_CS1_P1)-MIN(Get_Exp(str_anc_AAV_Elem_301_CS1_FACTOR)*GET_ANALVR(str_AAV_ELEM_301_Counter)/Get_Number(100),Get_Number(1))),Get_Number(0))
```

Original:
```text
IF(Get_Field(4b504462-b48a-473c-925c-d7a8705fb230)>Get_Number(0),GET_ANALVAR_4_YR(fe91dd43-6b4b-41b9-a462-b3ad21a6c071,YR-Get_Number(1))*(Get_Exp(fe1b3683-48c7-434e-a27e-12d0ea93ca0b)-MIN(Get_Exp(2a07cfd1-795d-4e49-8b34-77871ae993ce)*GET_ANALVR(f4912ed8-a86c-4fb9-b08f-ff201b994d07)/Get_Number(100),Get_Number(1))),Get_Number(0))
```

<a id="e-2a07cfd1-795d-4e49-8b34-77871ae993ce"></a>

## str_anc_AAV_Elem_301_CS1_FACTOR

Source: `RuntimeExpressions` / `2a07cfd1-795d-4e49-8b34-77871ae993ce`.

Return CS1 Deterioration Factor for Elem 301

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','FACTOR','Name','301_CS1',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','FACTOR','Name','301_CS1',TRUE))
```

<a id="e-49713f59-7a7c-457b-907e-66c9ee547131"></a>

## str_anc_AAV_Elem_301_CS1_Initialize

Source: `dTIMSExpressions` / `49713f59-7a7c-457b-907e-66c9ee547131`.

Initialize ELEM 301 CS1

Readable:
```text
IF(Get_Field(ELEM_301_QUANTITY)>Get_Number(0),Get_Field(ELEM_301_CS1)/Get_Field(ELEM_301_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(4b504462-b48a-473c-925c-d7a8705fb230)>Get_Number(0),Get_Field(1ca2c1e8-5a16-4187-b631-eadde7dcab74)/Get_Field(4b504462-b48a-473c-925c-d7a8705fb230)*Get_Number(100),Get_Number(0))
```

<a id="e-fe1b3683-48c7-434e-a27e-12d0ea93ca0b"></a>

## str_anc_AAV_Elem_301_CS1_P1

Source: `RuntimeExpressions` / `fe1b3683-48c7-434e-a27e-12d0ea93ca0b`.

Return CS1 P1 for Element 301

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS1','Name','301_CS1',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS1','Name','301_CS1',TRUE))
```

<a id="e-aa9fd4fa-a436-4bfd-95c5-1c2c783b734b"></a>

## str_anc_AAV_Elem_301_CS21_All

Source: `RuntimeExpressions` / `aa9fd4fa-a436-4bfd-95c5-1c2c783b734b`.

Predict CS2 in Future Years

Readable:
```text
IF(Get_Field(ELEM_301_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_301_CS2,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_301_CS2_P2)+GET_ANALVAR_4_YR(str_AAV_ELEM_301_CS1,YR-Get_Number(1))-GET_ANALVR(str_AAV_ELEM_301_CS1),Get_Number(0))
```

Original:
```text
IF(Get_Field(4b504462-b48a-473c-925c-d7a8705fb230)>Get_Number(0),GET_ANALVAR_4_YR(3b780c2e-ad74-4e0f-92bc-b1e73324876c,YR-Get_Number(1))*Get_Exp(876cc1f5-82c1-4b15-984e-8f41776c7e74)+GET_ANALVAR_4_YR(fe91dd43-6b4b-41b9-a462-b3ad21a6c071,YR-Get_Number(1))-GET_ANALVR(fe91dd43-6b4b-41b9-a462-b3ad21a6c071),Get_Number(0))
```

<a id="e-d11b9055-b27a-49c5-b15f-0d25571eacf8"></a>

## str_anc_AAV_Elem_301_CS2_All

Source: `RuntimeExpressions` / `d11b9055-b27a-49c5-b15f-0d25571eacf8`.

Predict CS2 in Future Years

Readable:
```text
IF(Get_Field(ELEM_301_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_301_CS2,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_301_CS2_P2)+GET_ANALVAR_4_YR(str_AAV_ELEM_301_CS1,YR-Get_Number(1))-GET_ANALVR(str_AAV_ELEM_301_CS1),Get_Number(0))
```

Original:
```text
IF(Get_Field(4b504462-b48a-473c-925c-d7a8705fb230)>Get_Number(0),GET_ANALVAR_4_YR(3b780c2e-ad74-4e0f-92bc-b1e73324876c,YR-Get_Number(1))*Get_Exp(876cc1f5-82c1-4b15-984e-8f41776c7e74)+GET_ANALVAR_4_YR(fe91dd43-6b4b-41b9-a462-b3ad21a6c071,YR-Get_Number(1))-GET_ANALVR(fe91dd43-6b4b-41b9-a462-b3ad21a6c071),Get_Number(0))
```

<a id="e-e46068d4-8688-4875-ba4d-51894fa4dfba"></a>

## str_anc_AAV_Elem_301_CS2_Initialize

Source: `dTIMSExpressions` / `e46068d4-8688-4875-ba4d-51894fa4dfba`.

Initialize ELEM 301 CS2

Readable:
```text
IF(Get_Field(ELEM_301_QUANTITY)>Get_Number(0),Get_Field(ELEM_301_CS2)/Get_Field(ELEM_301_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(4b504462-b48a-473c-925c-d7a8705fb230)>Get_Number(0),Get_Field(db2ad7ce-e3d4-4254-bf1b-15910d70d4c3)/Get_Field(4b504462-b48a-473c-925c-d7a8705fb230)*Get_Number(100),Get_Number(0))
```

<a id="e-876cc1f5-82c1-4b15-984e-8f41776c7e74"></a>

## str_anc_AAV_Elem_301_CS2_P2

Source: `RuntimeExpressions` / `876cc1f5-82c1-4b15-984e-8f41776c7e74`.

Return CS2 P2 for Element 301

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS2','Name','301_CS2',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS2','Name','301_CS2',TRUE))
```

<a id="e-20257787-aa11-40fc-97fa-2cede88ead66"></a>

## str_anc_AAV_Elem_301_CS2_P3

Source: `RuntimeExpressions` / `20257787-aa11-40fc-97fa-2cede88ead66`.

Return CS2 P3 for Element 301

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','301_CS2',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','301_CS2',TRUE))
```

<a id="e-783cfeb6-9323-4f18-a8b7-c4a00db2dd24"></a>

## str_anc_AAV_Elem_301_CS3_All

Source: `RuntimeExpressions` / `783cfeb6-9323-4f18-a8b7-c4a00db2dd24`.

Predict CS3 in Future Years

Readable:
```text
IF(Get_Field(ELEM_301_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_301_CS3,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_301_CS3_P3)+GET_ANALVAR_4_YR(str_AAV_ELEM_301_CS2,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_301_CS2_P3),Get_Number(0))
```

Original:
```text
IF(Get_Field(4b504462-b48a-473c-925c-d7a8705fb230)>Get_Number(0),GET_ANALVAR_4_YR(f708c328-863a-4123-858a-054acc31a694,YR-Get_Number(1))*Get_Exp(6aed1bc5-b50d-4d9a-b369-0adc22cbbe8d)+GET_ANALVAR_4_YR(3b780c2e-ad74-4e0f-92bc-b1e73324876c,YR-Get_Number(1))*Get_Exp(20257787-aa11-40fc-97fa-2cede88ead66),Get_Number(0))
```

<a id="e-af0899e9-6bdc-4a40-b369-16d70908136c"></a>

## str_anc_AAV_Elem_301_CS3_Initialize

Source: `dTIMSExpressions` / `af0899e9-6bdc-4a40-b369-16d70908136c`.

Initialize ELEM 301 CS3

Readable:
```text
IF(Get_Field(ELEM_301_QUANTITY)>Get_Number(0),Get_Field(ELEM_301_CS3)/Get_Field(ELEM_301_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(4b504462-b48a-473c-925c-d7a8705fb230)>Get_Number(0),Get_Field(8e12764e-830b-4326-9953-3473fc65ffef)/Get_Field(4b504462-b48a-473c-925c-d7a8705fb230)*Get_Number(100),Get_Number(0))
```

<a id="e-6aed1bc5-b50d-4d9a-b369-0adc22cbbe8d"></a>

## str_anc_AAV_Elem_301_CS3_P3

Source: `RuntimeExpressions` / `6aed1bc5-b50d-4d9a-b369-0adc22cbbe8d`.

Return CS3 P3 for Element 301

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','301_CS3',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','301_CS3',TRUE))
```

<a id="e-a9f276c6-8f48-4708-803e-b556afba7d4e"></a>

## str_anc_AAV_Elem_301_CS3_P4

Source: `RuntimeExpressions` / `a9f276c6-8f48-4708-803e-b556afba7d4e`.

Return CS3 P4 for Element 301

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS4','Name','301_CS3',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS4','Name','301_CS3',TRUE))
```

<a id="e-7d740df1-fd71-4bbc-9733-21b9c84ad3ac"></a>

## str_anc_AAV_Elem_301_CS4_All

Source: `RuntimeExpressions` / `7d740df1-fd71-4bbc-9733-21b9c84ad3ac`.

Predict CS4 in Future Years

Readable:
```text
IF(Get_Field(ELEM_301_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_301_CS4,YR-Get_Number(1))+GET_ANALVAR_4_YR(str_AAV_ELEM_301_CS3,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_301_CS3_P4),Get_Number(0))
```

Original:
```text
IF(Get_Field(4b504462-b48a-473c-925c-d7a8705fb230)>Get_Number(0),GET_ANALVAR_4_YR(8ca14d11-25c7-4066-8211-7ea26fc2c16d,YR-Get_Number(1))+GET_ANALVAR_4_YR(f708c328-863a-4123-858a-054acc31a694,YR-Get_Number(1))*Get_Exp(a9f276c6-8f48-4708-803e-b556afba7d4e),Get_Number(0))
```

<a id="e-6e8277a1-b46e-4277-9228-b25b9473fda0"></a>

## str_anc_AAV_Elem_301_CS4_Initialize

Source: `dTIMSExpressions` / `6e8277a1-b46e-4277-9228-b25b9473fda0`.

Initialize ELEM 301 CS4

Readable:
```text
IF(Get_Field(ELEM_301_QUANTITY)>Get_Number(0),Get_Field(ELEM_301_CS4)/Get_Field(ELEM_301_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(4b504462-b48a-473c-925c-d7a8705fb230)>Get_Number(0),Get_Field(af0b6b14-b96d-464d-98db-e67ad73190d4)/Get_Field(4b504462-b48a-473c-925c-d7a8705fb230)*Get_Number(100),Get_Number(0))
```

<a id="e-ed1c9993-f230-4f13-a185-11203329af89"></a>

## str_anc_AAV_Elem_301_Counter_All

Source: `RuntimeExpressions` / `ed1c9993-f230-4f13-a185-11203329af89`.

Increment the Elem 301 Counter


Readable:
```text
MIN(GET_ANALVR(str_AAV_ELEM_301_Counter)+Get_Number(1),Get_Number(50))
```

Original:
```text
MIN(GET_ANALVR(f4912ed8-a86c-4fb9-b08f-ff201b994d07)+Get_Number(1),Get_Number(50))
```

<a id="e-bda4af28-f237-4863-9064-298a5c921712"></a>

## str_anc_AAV_Elem_302_CS1_All

Source: `RuntimeExpressions` / `bda4af28-f237-4863-9064-298a5c921712`.

Predict CS1 in Future Years

Readable:
```text
IF(Get_Field(ELEM_302_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_302_CS1,YR-Get_Number(1))*(Get_Exp(str_anc_AAV_Elem_302_CS1_P1)-MIN(Get_Exp(str_anc_AAV_Elem_302_CS1_FACTOR)*GET_ANALVR(str_AAV_ELEM_302_Counter)/Get_Number(100),Get_Number(1))),Get_Number(0))
```

Original:
```text
IF(Get_Field(286fae98-ad52-46cc-adab-7d5978b28ac0)>Get_Number(0),GET_ANALVAR_4_YR(a993a5d8-e060-4d00-89a1-ecf0f24d16f8,YR-Get_Number(1))*(Get_Exp(fb1ba7ff-d2c6-4673-84b0-1f41649e5218)-MIN(Get_Exp(a2dfd6f1-27f0-42d9-aeda-261b18f5faa1)*GET_ANALVR(1a1c9e0b-e193-45e1-97b9-777d5eb24a76)/Get_Number(100),Get_Number(1))),Get_Number(0))
```

<a id="e-a2dfd6f1-27f0-42d9-aeda-261b18f5faa1"></a>

## str_anc_AAV_Elem_302_CS1_FACTOR

Source: `RuntimeExpressions` / `a2dfd6f1-27f0-42d9-aeda-261b18f5faa1`.

Return CS1 Deterioration Factor for Elem 302

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','FACTOR','Name','302_CS1',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','FACTOR','Name','302_CS1',TRUE))
```

<a id="e-abae4bb9-162e-4e43-8d0d-76a2799058fe"></a>

## str_anc_AAV_Elem_302_CS1_Initialize

Source: `dTIMSExpressions` / `abae4bb9-162e-4e43-8d0d-76a2799058fe`.

Initialize ELEM 302 CS1

Readable:
```text
IF(Get_Field(ELEM_302_QUANTITY)>Get_Number(0),Get_Field(ELEM_302_CS1)/Get_Field(ELEM_302_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(286fae98-ad52-46cc-adab-7d5978b28ac0)>Get_Number(0),Get_Field(9b3682b2-270c-4835-9685-646811af492c)/Get_Field(286fae98-ad52-46cc-adab-7d5978b28ac0)*Get_Number(100),Get_Number(0))
```

<a id="e-fb1ba7ff-d2c6-4673-84b0-1f41649e5218"></a>

## str_anc_AAV_Elem_302_CS1_P1

Source: `RuntimeExpressions` / `fb1ba7ff-d2c6-4673-84b0-1f41649e5218`.

Return CS1 P1 for Element 302

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS1','Name','302_CS1',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS1','Name','302_CS1',TRUE))
```

<a id="e-802e2b2e-11d3-48dd-bfe1-82a3268ee8b4"></a>

## str_anc_AAV_Elem_302_CS2_All

Source: `RuntimeExpressions` / `802e2b2e-11d3-48dd-bfe1-82a3268ee8b4`.

Predict CS2 in Future Years

Readable:
```text
IF(Get_Field(ELEM_302_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_302_CS2,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_302_CS2_P2)+GET_ANALVAR_4_YR(str_AAV_ELEM_302_CS1,YR-Get_Number(1))-GET_ANALVR(str_AAV_ELEM_302_CS1),Get_Number(0))
```

Original:
```text
IF(Get_Field(286fae98-ad52-46cc-adab-7d5978b28ac0)>Get_Number(0),GET_ANALVAR_4_YR(3cada5ae-8166-4436-81d8-0aef0f53f639,YR-Get_Number(1))*Get_Exp(fcde01f5-378a-492b-9325-3aafb82cd77e)+GET_ANALVAR_4_YR(a993a5d8-e060-4d00-89a1-ecf0f24d16f8,YR-Get_Number(1))-GET_ANALVR(a993a5d8-e060-4d00-89a1-ecf0f24d16f8),Get_Number(0))
```

<a id="e-15024b78-a017-47d3-a923-42fec1a368b6"></a>

## str_anc_AAV_Elem_302_CS2_Initialize

Source: `dTIMSExpressions` / `15024b78-a017-47d3-a923-42fec1a368b6`.

Initialize ELEM 302 CS2

Readable:
```text
IF(Get_Field(ELEM_302_QUANTITY)>Get_Number(0),Get_Field(ELEM_302_CS2)/Get_Field(ELEM_302_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(286fae98-ad52-46cc-adab-7d5978b28ac0)>Get_Number(0),Get_Field(6c0335d0-1c34-4729-8b85-f1fdc6a95c06)/Get_Field(286fae98-ad52-46cc-adab-7d5978b28ac0)*Get_Number(100),Get_Number(0))
```

<a id="e-fcde01f5-378a-492b-9325-3aafb82cd77e"></a>

## str_anc_AAV_Elem_302_CS2_P2

Source: `RuntimeExpressions` / `fcde01f5-378a-492b-9325-3aafb82cd77e`.

Return CS2 P2 for Element 302

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS2','Name','302_CS2',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS2','Name','302_CS2',TRUE))
```

<a id="e-e4de1531-3460-4a59-8630-29f6a49a4744"></a>

## str_anc_AAV_Elem_302_CS2_P3

Source: `RuntimeExpressions` / `e4de1531-3460-4a59-8630-29f6a49a4744`.

Return CS2 P3 for Element 302

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','302_CS2',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','302_CS2',TRUE))
```

<a id="e-c9893fc9-2e3f-4b1a-85ab-c4500766a7e7"></a>

## str_anc_AAV_Elem_302_CS3_All

Source: `RuntimeExpressions` / `c9893fc9-2e3f-4b1a-85ab-c4500766a7e7`.

Predict CS3 in Future Years

Readable:
```text
IF(Get_Field(ELEM_302_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_302_CS3,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_302_CS3_P3)+GET_ANALVAR_4_YR(str_AAV_ELEM_302_CS2,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_302_CS2_P3),Get_Number(0))
```

Original:
```text
IF(Get_Field(286fae98-ad52-46cc-adab-7d5978b28ac0)>Get_Number(0),GET_ANALVAR_4_YR(24512d9d-1d93-4f4e-b2dc-01add4760b83,YR-Get_Number(1))*Get_Exp(e99710fa-c20f-4751-8fb3-fe2188c85d05)+GET_ANALVAR_4_YR(3cada5ae-8166-4436-81d8-0aef0f53f639,YR-Get_Number(1))*Get_Exp(e4de1531-3460-4a59-8630-29f6a49a4744),Get_Number(0))
```

<a id="e-281b2d73-f094-4199-af92-7da606dc5183"></a>

## str_anc_AAV_Elem_302_CS3_Initialize

Source: `dTIMSExpressions` / `281b2d73-f094-4199-af92-7da606dc5183`.

Initialize ELEM 302 CS3

Readable:
```text
IF(Get_Field(ELEM_302_QUANTITY)>Get_Number(0),Get_Field(ELEM_302_CS3)/Get_Field(ELEM_302_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(286fae98-ad52-46cc-adab-7d5978b28ac0)>Get_Number(0),Get_Field(c229a68b-ebd5-4b9e-b872-579743ab4286)/Get_Field(286fae98-ad52-46cc-adab-7d5978b28ac0)*Get_Number(100),Get_Number(0))
```

<a id="e-e99710fa-c20f-4751-8fb3-fe2188c85d05"></a>

## str_anc_AAV_Elem_302_CS3_P3

Source: `RuntimeExpressions` / `e99710fa-c20f-4751-8fb3-fe2188c85d05`.

Return CS3 P3 for Element 302

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','302_CS3',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','302_CS3',TRUE))
```

<a id="e-ec64fb6f-fcfe-4948-9ddd-08c3fb6f860f"></a>

## str_anc_AAV_Elem_302_CS3_P4

Source: `RuntimeExpressions` / `ec64fb6f-fcfe-4948-9ddd-08c3fb6f860f`.

Return CS3 P4 for Element 302

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS4','Name','302_CS3',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS4','Name','302_CS3',TRUE))
```

<a id="e-6c81d7e2-c340-48bc-bcd0-907750ee2ad6"></a>

## str_anc_AAV_Elem_302_CS4_All

Source: `RuntimeExpressions` / `6c81d7e2-c340-48bc-bcd0-907750ee2ad6`.

Predict CS4 in Future Years

Readable:
```text
IF(Get_Field(ELEM_302_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_302_CS4,YR-Get_Number(1))+GET_ANALVAR_4_YR(str_AAV_ELEM_302_CS3,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_302_CS3_P4),Get_Number(0))
```

Original:
```text
IF(Get_Field(286fae98-ad52-46cc-adab-7d5978b28ac0)>Get_Number(0),GET_ANALVAR_4_YR(6ceafe1a-746f-454f-920b-aa2c1fdf4636,YR-Get_Number(1))+GET_ANALVAR_4_YR(24512d9d-1d93-4f4e-b2dc-01add4760b83,YR-Get_Number(1))*Get_Exp(ec64fb6f-fcfe-4948-9ddd-08c3fb6f860f),Get_Number(0))
```

<a id="e-1ff6b804-5335-45de-8bf1-e26e80e36107"></a>

## str_anc_AAV_Elem_302_CS4_Initialize

Source: `dTIMSExpressions` / `1ff6b804-5335-45de-8bf1-e26e80e36107`.

Initialize ELEM 302 CS4

Readable:
```text
IF(Get_Field(ELEM_302_QUANTITY)>Get_Number(0),Get_Field(ELEM_302_CS4)/Get_Field(ELEM_302_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(286fae98-ad52-46cc-adab-7d5978b28ac0)>Get_Number(0),Get_Field(3aa4e356-9991-4222-8693-02b3f6be7226)/Get_Field(286fae98-ad52-46cc-adab-7d5978b28ac0)*Get_Number(100),Get_Number(0))
```

<a id="e-7e9ad9ff-91de-4432-9393-e9a3fc966426"></a>

## str_anc_AAV_Elem_302_Counter_All

Source: `RuntimeExpressions` / `7e9ad9ff-91de-4432-9393-e9a3fc966426`.

Increment the Elem 302 Counter


Readable:
```text
MIN(GET_ANALVR(str_AAV_ELEM_302_Counter)+Get_Number(1),Get_Number(50))
```

Original:
```text
MIN(GET_ANALVR(1a1c9e0b-e193-45e1-97b9-777d5eb24a76)+Get_Number(1),Get_Number(50))
```

<a id="e-b5fd0bb8-e276-40a1-98b9-d8b4e5782e75"></a>

## str_anc_AAV_Elem_303_CS1_All

Source: `RuntimeExpressions` / `b5fd0bb8-e276-40a1-98b9-d8b4e5782e75`.

Predict CS1 in Future Years

Readable:
```text
IF(Get_Field(ELEM_303_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_303_CS1,YR-Get_Number(1))*(Get_Exp(str_anc_AAV_Elem_303_CS1_P1)-MIN(Get_Exp(str_anc_AAV_Elem_303_CS1_FACTOR)*GET_ANALVR(str_AAV_ELEM_303_Counter)/Get_Number(100),Get_Number(1))),Get_Number(0))
```

Original:
```text
IF(Get_Field(0caab4da-a7c0-4635-a19e-e82950b8b8fc)>Get_Number(0),GET_ANALVAR_4_YR(8eef7ab1-d910-4dbb-82ae-f25a9ce1794f,YR-Get_Number(1))*(Get_Exp(632090eb-578c-4897-85ad-13ba7a315b82)-MIN(Get_Exp(d23a953d-de1c-4f65-9c5f-a5fcc5984b74)*GET_ANALVR(cc7b8df3-6141-4631-be74-4d6e8e3b64f4)/Get_Number(100),Get_Number(1))),Get_Number(0))
```

<a id="e-d23a953d-de1c-4f65-9c5f-a5fcc5984b74"></a>

## str_anc_AAV_Elem_303_CS1_FACTOR

Source: `RuntimeExpressions` / `d23a953d-de1c-4f65-9c5f-a5fcc5984b74`.

Return CS1 Deterioration Factor for Elem 303

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','FACTOR','Name','303_CS1',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','FACTOR','Name','303_CS1',TRUE))
```

<a id="e-a5a85f70-b235-4376-a7fd-acbd979fc1f3"></a>

## str_anc_AAV_Elem_303_CS1_Initialize

Source: `dTIMSExpressions` / `a5a85f70-b235-4376-a7fd-acbd979fc1f3`.

Initialize ELEM 303 CS1

Readable:
```text
IF(Get_Field(ELEM_303_QUANTITY)>Get_Number(0),Get_Field(ELEM_303_CS1)/Get_Field(ELEM_303_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(0caab4da-a7c0-4635-a19e-e82950b8b8fc)>Get_Number(0),Get_Field(b7233f4c-658e-41e3-9614-845f249e4d55)/Get_Field(0caab4da-a7c0-4635-a19e-e82950b8b8fc)*Get_Number(100),Get_Number(0))
```

<a id="e-632090eb-578c-4897-85ad-13ba7a315b82"></a>

## str_anc_AAV_Elem_303_CS1_P1

Source: `RuntimeExpressions` / `632090eb-578c-4897-85ad-13ba7a315b82`.

Return CS1 P1 for Element 303

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS1','Name','303_CS1',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS1','Name','303_CS1',TRUE))
```

<a id="e-d038eb0c-1e58-44eb-b9a0-76016229e50d"></a>

## str_anc_AAV_Elem_303_CS2_All

Source: `RuntimeExpressions` / `d038eb0c-1e58-44eb-b9a0-76016229e50d`.

Predict CS2 in Future Years

Readable:
```text
IF(Get_Field(ELEM_303_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_303_CS2,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_303_CS2_P2)+GET_ANALVAR_4_YR(str_AAV_ELEM_303_CS1,YR-Get_Number(1))-GET_ANALVR(str_AAV_ELEM_303_CS1),Get_Number(0))
```

Original:
```text
IF(Get_Field(0caab4da-a7c0-4635-a19e-e82950b8b8fc)>Get_Number(0),GET_ANALVAR_4_YR(97cf5fcd-2ca3-45f7-b1a7-6279a15b0eaf,YR-Get_Number(1))*Get_Exp(b3b89a8c-5179-423d-b2d1-dbd8eff03280)+GET_ANALVAR_4_YR(8eef7ab1-d910-4dbb-82ae-f25a9ce1794f,YR-Get_Number(1))-GET_ANALVR(8eef7ab1-d910-4dbb-82ae-f25a9ce1794f),Get_Number(0))
```

<a id="e-d15c2987-c6e1-483d-979f-67cfb2f75857"></a>

## str_anc_AAV_Elem_303_CS2_Initialize

Source: `dTIMSExpressions` / `d15c2987-c6e1-483d-979f-67cfb2f75857`.

Initialize ELEM 303 CS2

Readable:
```text
IF(Get_Field(ELEM_303_QUANTITY)>Get_Number(0),Get_Field(ELEM_303_CS2)/Get_Field(ELEM_303_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(0caab4da-a7c0-4635-a19e-e82950b8b8fc)>Get_Number(0),Get_Field(b98e4ac6-93a0-49e4-9c0d-2b942858acf3)/Get_Field(0caab4da-a7c0-4635-a19e-e82950b8b8fc)*Get_Number(100),Get_Number(0))
```

<a id="e-b3b89a8c-5179-423d-b2d1-dbd8eff03280"></a>

## str_anc_AAV_Elem_303_CS2_P2

Source: `RuntimeExpressions` / `b3b89a8c-5179-423d-b2d1-dbd8eff03280`.

Return CS2 P2 for Element 303

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS2','Name','303_CS2',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS2','Name','303_CS2',TRUE))
```

<a id="e-84535867-f3e9-41c7-8318-56c7ac415dbb"></a>

## str_anc_AAV_Elem_303_CS2_P3

Source: `RuntimeExpressions` / `84535867-f3e9-41c7-8318-56c7ac415dbb`.

Return CS2 P3 for Element 303

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','303_CS2',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','303_CS2',TRUE))
```

<a id="e-4f4f8a48-c13b-4928-bb1e-0a1cea80c891"></a>

## str_anc_AAV_Elem_303_CS3_All

Source: `RuntimeExpressions` / `4f4f8a48-c13b-4928-bb1e-0a1cea80c891`.

Predict CS3 in Future Years

Readable:
```text
IF(Get_Field(ELEM_303_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_303_CS3,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_303_CS3_P3)+GET_ANALVAR_4_YR(str_AAV_ELEM_303_CS2,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_303_CS2_P3),Get_Number(0))
```

Original:
```text
IF(Get_Field(0caab4da-a7c0-4635-a19e-e82950b8b8fc)>Get_Number(0),GET_ANALVAR_4_YR(14583ddf-987a-4258-ad09-e2e34ef3767a,YR-Get_Number(1))*Get_Exp(a729cc09-7460-49a7-bbe1-d4ed4796eef3)+GET_ANALVAR_4_YR(97cf5fcd-2ca3-45f7-b1a7-6279a15b0eaf,YR-Get_Number(1))*Get_Exp(84535867-f3e9-41c7-8318-56c7ac415dbb),Get_Number(0))
```

<a id="e-826ea815-01f4-447c-9188-ed0463f82cb2"></a>

## str_anc_AAV_Elem_303_CS3_Initialize

Source: `dTIMSExpressions` / `826ea815-01f4-447c-9188-ed0463f82cb2`.

Initialize ELEM 303 CS3

Readable:
```text
IF(Get_Field(ELEM_303_QUANTITY)>Get_Number(0),Get_Field(ELEM_303_CS3)/Get_Field(ELEM_303_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(0caab4da-a7c0-4635-a19e-e82950b8b8fc)>Get_Number(0),Get_Field(1ff3ff08-2fa3-4a1f-8c61-e997d9a02341)/Get_Field(0caab4da-a7c0-4635-a19e-e82950b8b8fc)*Get_Number(100),Get_Number(0))
```

<a id="e-a729cc09-7460-49a7-bbe1-d4ed4796eef3"></a>

## str_anc_AAV_Elem_303_CS3_P3

Source: `RuntimeExpressions` / `a729cc09-7460-49a7-bbe1-d4ed4796eef3`.

Return CS3 P3 for Element 303

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','303_CS3',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','303_CS3',TRUE))
```

<a id="e-4fc0f8cb-fec5-4928-84a8-f4fd113124c2"></a>

## str_anc_AAV_Elem_303_CS3_P4

Source: `RuntimeExpressions` / `4fc0f8cb-fec5-4928-84a8-f4fd113124c2`.

Return CS3 P4 for Element 303

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS4','Name','303_CS3',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS4','Name','303_CS3',TRUE))
```

<a id="e-a829042e-af1a-4323-9983-54404e815f84"></a>

## str_anc_AAV_Elem_303_CS4_All

Source: `RuntimeExpressions` / `a829042e-af1a-4323-9983-54404e815f84`.

Predict CS4 in Future Years

Readable:
```text
IF(Get_Field(ELEM_303_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_303_CS4,YR-Get_Number(1))+GET_ANALVAR_4_YR(str_AAV_ELEM_303_CS3,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_303_CS3_P4),Get_Number(0))
```

Original:
```text
IF(Get_Field(0caab4da-a7c0-4635-a19e-e82950b8b8fc)>Get_Number(0),GET_ANALVAR_4_YR(1348c087-28be-49ed-9b43-67895062ff57,YR-Get_Number(1))+GET_ANALVAR_4_YR(14583ddf-987a-4258-ad09-e2e34ef3767a,YR-Get_Number(1))*Get_Exp(4fc0f8cb-fec5-4928-84a8-f4fd113124c2),Get_Number(0))
```

<a id="e-254045e1-566f-4a36-b58a-db77ade88507"></a>

## str_anc_AAV_Elem_303_CS4_Initialize

Source: `dTIMSExpressions` / `254045e1-566f-4a36-b58a-db77ade88507`.

Initialize ELEM 303 CS4

Readable:
```text
IF(Get_Field(ELEM_303_QUANTITY)>Get_Number(0),Get_Field(ELEM_303_CS4)/Get_Field(ELEM_303_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(0caab4da-a7c0-4635-a19e-e82950b8b8fc)>Get_Number(0),Get_Field(6fd8f6f9-059d-4de1-b72a-fb46ab52ac12)/Get_Field(0caab4da-a7c0-4635-a19e-e82950b8b8fc)*Get_Number(100),Get_Number(0))
```

<a id="e-93363010-699d-44f3-b7f2-fc11d72907da"></a>

## str_anc_AAV_Elem_303_Counter_All

Source: `RuntimeExpressions` / `93363010-699d-44f3-b7f2-fc11d72907da`.

Increment the Elem 303 Counter


Readable:
```text
MIN(GET_ANALVR(str_AAV_ELEM_303_Counter)+Get_Number(1),Get_Number(50))
```

Original:
```text
MIN(GET_ANALVR(cc7b8df3-6141-4631-be74-4d6e8e3b64f4)+Get_Number(1),Get_Number(50))
```

<a id="e-f2f6453b-9565-4d67-bb57-ec27dc331a75"></a>

## str_anc_AAV_Elem_304_CS1_All

Source: `RuntimeExpressions` / `f2f6453b-9565-4d67-bb57-ec27dc331a75`.

Predict CS1 in Future Years

Readable:
```text
IF(Get_Field(ELEM_304_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_304_CS1,YR-Get_Number(1))*(Get_Exp(str_anc_AAV_Elem_304_CS1_P1)-MIN(Get_Exp(str_anc_AAV_Elem_304_CS1_FACTOR)*GET_ANALVR(str_AAV_ELEM_304_Counter)/Get_Number(100),Get_Number(1))),Get_Number(0))
```

Original:
```text
IF(Get_Field(56ab8060-0651-4223-b119-3043fe5a0abc)>Get_Number(0),GET_ANALVAR_4_YR(8c793ecf-ce40-451c-a5a9-ab003541faa0,YR-Get_Number(1))*(Get_Exp(c1959b47-2f51-44c7-8ba3-2ce2d2b00e12)-MIN(Get_Exp(15930a45-5bf9-4114-b47e-3d6c14a4e46e)*GET_ANALVR(35087a05-3fb8-4f93-8e46-497e0d6d6721)/Get_Number(100),Get_Number(1))),Get_Number(0))
```

<a id="e-15930a45-5bf9-4114-b47e-3d6c14a4e46e"></a>

## str_anc_AAV_Elem_304_CS1_FACTOR

Source: `RuntimeExpressions` / `15930a45-5bf9-4114-b47e-3d6c14a4e46e`.

Return CS1 Deterioration Factor for Elem 304

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','FACTOR','Name','304_CS1',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','FACTOR','Name','304_CS1',TRUE))
```

<a id="e-39eb6900-5968-4dc6-b068-cdfb91247a07"></a>

## str_anc_AAV_Elem_304_CS1_Initialize

Source: `dTIMSExpressions` / `39eb6900-5968-4dc6-b068-cdfb91247a07`.

Initialize ELEM 304 CS1

Readable:
```text
IF(Get_Field(ELEM_304_QUANTITY)>Get_Number(0),Get_Field(ELEM_304_CS1)/Get_Field(ELEM_304_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(56ab8060-0651-4223-b119-3043fe5a0abc)>Get_Number(0),Get_Field(e7d69f80-902e-45e8-a07b-2b9e43b410e9)/Get_Field(56ab8060-0651-4223-b119-3043fe5a0abc)*Get_Number(100),Get_Number(0))
```

<a id="e-c1959b47-2f51-44c7-8ba3-2ce2d2b00e12"></a>

## str_anc_AAV_Elem_304_CS1_P1

Source: `RuntimeExpressions` / `c1959b47-2f51-44c7-8ba3-2ce2d2b00e12`.

Return CS1 P1 for Element 304

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS1','Name','304_CS1',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS1','Name','304_CS1',TRUE))
```

<a id="e-052031af-ffbf-409f-a36b-205a5bd2f6f3"></a>

## str_anc_AAV_Elem_304_CS2_All

Source: `RuntimeExpressions` / `052031af-ffbf-409f-a36b-205a5bd2f6f3`.

Predict CS2 in Future Years

Readable:
```text
IF(Get_Field(ELEM_304_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_304_CS2,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_304_CS2_P2)+GET_ANALVAR_4_YR(str_AAV_ELEM_304_CS1,YR-Get_Number(1))-GET_ANALVR(str_AAV_ELEM_304_CS1),Get_Number(0))
```

Original:
```text
IF(Get_Field(56ab8060-0651-4223-b119-3043fe5a0abc)>Get_Number(0),GET_ANALVAR_4_YR(ce1c86aa-c150-4f5f-b229-78e4e9e75d82,YR-Get_Number(1))*Get_Exp(f8f46518-1198-41e9-ae9c-6044c46a1c74)+GET_ANALVAR_4_YR(8c793ecf-ce40-451c-a5a9-ab003541faa0,YR-Get_Number(1))-GET_ANALVR(8c793ecf-ce40-451c-a5a9-ab003541faa0),Get_Number(0))
```

<a id="e-1f90b82e-29db-42bb-a86b-04275f609fd5"></a>

## str_anc_AAV_Elem_304_CS2_Initialize

Source: `dTIMSExpressions` / `1f90b82e-29db-42bb-a86b-04275f609fd5`.

Initialize ELEM 304 CS2

Readable:
```text
IF(Get_Field(ELEM_304_QUANTITY)>Get_Number(0),Get_Field(ELEM_304_CS2)/Get_Field(ELEM_304_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(56ab8060-0651-4223-b119-3043fe5a0abc)>Get_Number(0),Get_Field(f8de6244-3bee-4413-bdfe-e382a5ea0973)/Get_Field(56ab8060-0651-4223-b119-3043fe5a0abc)*Get_Number(100),Get_Number(0))
```

<a id="e-f8f46518-1198-41e9-ae9c-6044c46a1c74"></a>

## str_anc_AAV_Elem_304_CS2_P2

Source: `RuntimeExpressions` / `f8f46518-1198-41e9-ae9c-6044c46a1c74`.

Return CS2 P2 for Element 304

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS2','Name','304_CS2',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS2','Name','304_CS2',TRUE))
```

<a id="e-65b49c37-9194-4f36-93c2-e142b84b9ddc"></a>

## str_anc_AAV_Elem_304_CS2_P3

Source: `RuntimeExpressions` / `65b49c37-9194-4f36-93c2-e142b84b9ddc`.

Return CS2 P3 for Element 304

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','304_CS2',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','304_CS2',TRUE))
```

<a id="e-0d97afdd-460a-4068-9cfd-5d4d1ceece8a"></a>

## str_anc_AAV_Elem_304_CS3_All

Source: `RuntimeExpressions` / `0d97afdd-460a-4068-9cfd-5d4d1ceece8a`.

Predict CS3 in Future Years

Readable:
```text
IF(Get_Field(ELEM_304_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_304_CS3,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_304_CS3_P3)+GET_ANALVAR_4_YR(str_AAV_ELEM_304_CS2,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_304_CS2_P3),Get_Number(0))
```

Original:
```text
IF(Get_Field(56ab8060-0651-4223-b119-3043fe5a0abc)>Get_Number(0),GET_ANALVAR_4_YR(ed7115cf-e74e-4b3c-bd80-6bf72d394a50,YR-Get_Number(1))*Get_Exp(4f67ca89-57c3-47e2-8680-21af803aec52)+GET_ANALVAR_4_YR(ce1c86aa-c150-4f5f-b229-78e4e9e75d82,YR-Get_Number(1))*Get_Exp(65b49c37-9194-4f36-93c2-e142b84b9ddc),Get_Number(0))
```

<a id="e-9cf6bf6e-be41-4eea-8895-1116ff641063"></a>

## str_anc_AAV_Elem_304_CS3_Initialize

Source: `dTIMSExpressions` / `9cf6bf6e-be41-4eea-8895-1116ff641063`.

Initialize ELEM 304 CS3

Readable:
```text
IF(Get_Field(ELEM_304_QUANTITY)>Get_Number(0),Get_Field(ELEM_304_CS3)/Get_Field(ELEM_304_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(56ab8060-0651-4223-b119-3043fe5a0abc)>Get_Number(0),Get_Field(b23967f7-d778-4a0e-89ba-b20e02e88b73)/Get_Field(56ab8060-0651-4223-b119-3043fe5a0abc)*Get_Number(100),Get_Number(0))
```

<a id="e-4f67ca89-57c3-47e2-8680-21af803aec52"></a>

## str_anc_AAV_Elem_304_CS3_P3

Source: `RuntimeExpressions` / `4f67ca89-57c3-47e2-8680-21af803aec52`.

Return CS3 P3 for Element 304

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','304_CS3',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','304_CS3',TRUE))
```

<a id="e-0c45f7c8-85da-40a0-85d7-d92a234b5867"></a>

## str_anc_AAV_Elem_304_CS3_P4

Source: `RuntimeExpressions` / `0c45f7c8-85da-40a0-85d7-d92a234b5867`.

Return CS3 P4 for Element 304

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS4','Name','304_CS3',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS4','Name','304_CS3',TRUE))
```

<a id="e-a8a45885-e8f2-4252-92f3-5118c8c8bc0f"></a>

## str_anc_AAV_Elem_304_CS4_All

Source: `RuntimeExpressions` / `a8a45885-e8f2-4252-92f3-5118c8c8bc0f`.

Predict CS4 in Future Years

Readable:
```text
IF(Get_Field(ELEM_304_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_304_CS4,YR-Get_Number(1))+GET_ANALVAR_4_YR(str_AAV_ELEM_304_CS3,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_304_CS3_P4),Get_Number(0))
```

Original:
```text
IF(Get_Field(56ab8060-0651-4223-b119-3043fe5a0abc)>Get_Number(0),GET_ANALVAR_4_YR(ec0a9854-38d7-467d-9b18-0b80f0d47b2a,YR-Get_Number(1))+GET_ANALVAR_4_YR(ed7115cf-e74e-4b3c-bd80-6bf72d394a50,YR-Get_Number(1))*Get_Exp(0c45f7c8-85da-40a0-85d7-d92a234b5867),Get_Number(0))
```

<a id="e-2cb4b998-4891-44c0-b886-b77e9638e607"></a>

## str_anc_AAV_Elem_304_CS4_Initialize

Source: `dTIMSExpressions` / `2cb4b998-4891-44c0-b886-b77e9638e607`.

Initialize ELEM 304 CS4

Readable:
```text
IF(Get_Field(ELEM_304_QUANTITY)>Get_Number(0),Get_Field(ELEM_304_CS4)/Get_Field(ELEM_304_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(56ab8060-0651-4223-b119-3043fe5a0abc)>Get_Number(0),Get_Field(4d53fbfe-3aef-4f44-97b2-9685c40c6e02)/Get_Field(56ab8060-0651-4223-b119-3043fe5a0abc)*Get_Number(100),Get_Number(0))
```

<a id="e-46e60f65-a43a-40e2-ac0a-8b8f096b18c4"></a>

## str_anc_AAV_Elem_304_Counter_All

Source: `RuntimeExpressions` / `46e60f65-a43a-40e2-ac0a-8b8f096b18c4`.

Increment the Elem 304 Counter


Readable:
```text
MIN(GET_ANALVR(str_AAV_ELEM_304_Counter)+Get_Number(1),Get_Number(50))
```

Original:
```text
MIN(GET_ANALVR(35087a05-3fb8-4f93-8e46-497e0d6d6721)+Get_Number(1),Get_Number(50))
```

<a id="e-443cd903-9061-438a-b1a2-0824eeeffe47"></a>

## str_anc_AAV_Elem_305_CS1_All

Source: `RuntimeExpressions` / `443cd903-9061-438a-b1a2-0824eeeffe47`.

Predict CS1 in Future Years

Readable:
```text
IF(Get_Field(ELEM_305_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_305_CS1,YR-Get_Number(1))*(Get_Exp(str_anc_AAV_Elem_305_CS1_P1)-MIN(Get_Exp(str_anc_AAV_Elem_305_CS1_FACTOR)*GET_ANALVR(str_AAV_ELEM_305_Counter)/Get_Number(100),Get_Number(1))),Get_Number(0))
```

Original:
```text
IF(Get_Field(87443be7-82d6-4927-9f74-a8e47f9602b0)>Get_Number(0),GET_ANALVAR_4_YR(d5c8d5ab-51a3-47ac-b0bb-d0e61336a787,YR-Get_Number(1))*(Get_Exp(54d65bb2-c195-4022-88c5-d5149e5aafa2)-MIN(Get_Exp(9e3b567f-f1ea-41ec-aec5-92aeeed6488d)*GET_ANALVR(b43d1ce9-c8fe-434b-bbf0-7c2c7bb968eb)/Get_Number(100),Get_Number(1))),Get_Number(0))
```

<a id="e-9e3b567f-f1ea-41ec-aec5-92aeeed6488d"></a>

## str_anc_AAV_Elem_305_CS1_FACTOR

Source: `RuntimeExpressions` / `9e3b567f-f1ea-41ec-aec5-92aeeed6488d`.

Return CS1 Deterioration Factor for Elem 305

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','FACTOR','Name','305_CS1',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','FACTOR','Name','305_CS1',TRUE))
```

<a id="e-893e0578-dd7e-4d2e-983a-e0b231599f04"></a>

## str_anc_AAV_Elem_305_CS1_Initialize

Source: `dTIMSExpressions` / `893e0578-dd7e-4d2e-983a-e0b231599f04`.

Initialize ELEM 305 CS1

Readable:
```text
IF(Get_Field(ELEM_305_QUANTITY)>Get_Number(0),Get_Field(ELEM_305_CS1)/Get_Field(ELEM_305_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(87443be7-82d6-4927-9f74-a8e47f9602b0)>Get_Number(0),Get_Field(fad212de-c208-4743-937e-82c391be77fe)/Get_Field(87443be7-82d6-4927-9f74-a8e47f9602b0)*Get_Number(100),Get_Number(0))
```

<a id="e-54d65bb2-c195-4022-88c5-d5149e5aafa2"></a>

## str_anc_AAV_Elem_305_CS1_P1

Source: `RuntimeExpressions` / `54d65bb2-c195-4022-88c5-d5149e5aafa2`.

Return CS1 P1 for Element 305

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS1','Name','305_CS1',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS1','Name','305_CS1',TRUE))
```

<a id="e-0cb18c87-d46c-4bc0-a59c-c5dcd1b71b89"></a>

## str_anc_AAV_Elem_305_CS2_All

Source: `RuntimeExpressions` / `0cb18c87-d46c-4bc0-a59c-c5dcd1b71b89`.

Predict CS2 in Future Years

Readable:
```text
IF(Get_Field(ELEM_305_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_305_CS2,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_305_CS2_P2)+GET_ANALVAR_4_YR(str_AAV_ELEM_305_CS1,YR-Get_Number(1))-GET_ANALVR(str_AAV_ELEM_305_CS1),Get_Number(0))
```

Original:
```text
IF(Get_Field(87443be7-82d6-4927-9f74-a8e47f9602b0)>Get_Number(0),GET_ANALVAR_4_YR(1c7df5e5-9b38-43d8-8cb0-9ff7806f03af,YR-Get_Number(1))*Get_Exp(e0eae20b-dcb8-49e2-b935-3aa2959db6e1)+GET_ANALVAR_4_YR(d5c8d5ab-51a3-47ac-b0bb-d0e61336a787,YR-Get_Number(1))-GET_ANALVR(d5c8d5ab-51a3-47ac-b0bb-d0e61336a787),Get_Number(0))
```

<a id="e-42f8084d-3c5e-497f-aa0d-06df71831bdd"></a>

## str_anc_AAV_Elem_305_CS2_Initialize

Source: `dTIMSExpressions` / `42f8084d-3c5e-497f-aa0d-06df71831bdd`.

Initialize ELEM 305 CS2

Readable:
```text
IF(Get_Field(ELEM_305_QUANTITY)>Get_Number(0),Get_Field(ELEM_305_CS2)/Get_Field(ELEM_305_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(87443be7-82d6-4927-9f74-a8e47f9602b0)>Get_Number(0),Get_Field(c9539e80-6aa8-4346-b1d0-56f01ecba14f)/Get_Field(87443be7-82d6-4927-9f74-a8e47f9602b0)*Get_Number(100),Get_Number(0))
```

<a id="e-e0eae20b-dcb8-49e2-b935-3aa2959db6e1"></a>

## str_anc_AAV_Elem_305_CS2_P2

Source: `RuntimeExpressions` / `e0eae20b-dcb8-49e2-b935-3aa2959db6e1`.

Return CS2 P2 for Element 305

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS2','Name','305_CS2',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS2','Name','305_CS2',TRUE))
```

<a id="e-e10e55e3-40e5-4140-94e1-ac8340793b38"></a>

## str_anc_AAV_Elem_305_CS2_P3

Source: `RuntimeExpressions` / `e10e55e3-40e5-4140-94e1-ac8340793b38`.

Return CS2 P3 for Element 305

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','305_CS2',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','305_CS2',TRUE))
```

<a id="e-affc2759-8ce7-42e0-99b0-9b62bdbc3b5c"></a>

## str_anc_AAV_Elem_305_CS3_All

Source: `RuntimeExpressions` / `affc2759-8ce7-42e0-99b0-9b62bdbc3b5c`.

Predict CS3 in Future Years

Readable:
```text
IF(Get_Field(ELEM_305_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_305_CS3,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_305_CS3_P3)+GET_ANALVAR_4_YR(str_AAV_ELEM_305_CS2,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_305_CS2_P3),Get_Number(0))
```

Original:
```text
IF(Get_Field(87443be7-82d6-4927-9f74-a8e47f9602b0)>Get_Number(0),GET_ANALVAR_4_YR(f175d017-bf6f-4ec4-ae5d-31a49b921363,YR-Get_Number(1))*Get_Exp(ae4962eb-762c-42ca-b5b8-5b375f5ee720)+GET_ANALVAR_4_YR(1c7df5e5-9b38-43d8-8cb0-9ff7806f03af,YR-Get_Number(1))*Get_Exp(e10e55e3-40e5-4140-94e1-ac8340793b38),Get_Number(0))
```

<a id="e-064259bb-a5b0-4d84-bb6b-a052f37b64d8"></a>

## str_anc_AAV_Elem_305_CS3_Initialize

Source: `dTIMSExpressions` / `064259bb-a5b0-4d84-bb6b-a052f37b64d8`.

Initialize ELEM 305 CS3

Readable:
```text
IF(Get_Field(ELEM_305_QUANTITY)>Get_Number(0),Get_Field(ELEM_305_CS3)/Get_Field(ELEM_305_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(87443be7-82d6-4927-9f74-a8e47f9602b0)>Get_Number(0),Get_Field(fa2cd4b4-95c8-4dc3-b74e-4952dad6c893)/Get_Field(87443be7-82d6-4927-9f74-a8e47f9602b0)*Get_Number(100),Get_Number(0))
```

<a id="e-ae4962eb-762c-42ca-b5b8-5b375f5ee720"></a>

## str_anc_AAV_Elem_305_CS3_P3

Source: `RuntimeExpressions` / `ae4962eb-762c-42ca-b5b8-5b375f5ee720`.

Return CS3 P3 for Element 305

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','305_CS3',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','305_CS3',TRUE))
```

<a id="e-b52e8e1d-3be9-4462-b24c-e765c03a7365"></a>

## str_anc_AAV_Elem_305_CS3_P4

Source: `RuntimeExpressions` / `b52e8e1d-3be9-4462-b24c-e765c03a7365`.

Return CS3 P4 for Element 305

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS4','Name','305_CS3',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS4','Name','305_CS3',TRUE))
```

<a id="e-a5249a22-c80f-4a9b-ac90-b83c8c80808a"></a>

## str_anc_AAV_Elem_305_CS4_All

Source: `RuntimeExpressions` / `a5249a22-c80f-4a9b-ac90-b83c8c80808a`.

Predict CS4 in Future Years

Readable:
```text
IF(Get_Field(ELEM_305_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_305_CS4,YR-Get_Number(1))+GET_ANALVAR_4_YR(str_AAV_ELEM_305_CS3,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_305_CS3_P4),Get_Number(0))
```

Original:
```text
IF(Get_Field(87443be7-82d6-4927-9f74-a8e47f9602b0)>Get_Number(0),GET_ANALVAR_4_YR(8032a6bb-d289-475b-b7d5-02afa4f7c548,YR-Get_Number(1))+GET_ANALVAR_4_YR(f175d017-bf6f-4ec4-ae5d-31a49b921363,YR-Get_Number(1))*Get_Exp(b52e8e1d-3be9-4462-b24c-e765c03a7365),Get_Number(0))
```

<a id="e-3229233e-e7c8-434f-828f-953ecedfb349"></a>

## str_anc_AAV_Elem_305_CS4_Initialize

Source: `dTIMSExpressions` / `3229233e-e7c8-434f-828f-953ecedfb349`.

Initialize ELEM 305 CS4

Readable:
```text
IF(Get_Field(ELEM_305_QUANTITY)>Get_Number(0),Get_Field(ELEM_305_CS4)/Get_Field(ELEM_305_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(87443be7-82d6-4927-9f74-a8e47f9602b0)>Get_Number(0),Get_Field(13a0c624-91c0-4a33-8260-bb86cba08167)/Get_Field(87443be7-82d6-4927-9f74-a8e47f9602b0)*Get_Number(100),Get_Number(0))
```

<a id="e-e4f0cd50-b896-4c93-9e0e-5e037cb9f9f7"></a>

## str_anc_AAV_Elem_305_Counter_All

Source: `RuntimeExpressions` / `e4f0cd50-b896-4c93-9e0e-5e037cb9f9f7`.

Increment the Elem 305 Counter


Readable:
```text
MIN(GET_ANALVR(str_AAV_ELEM_305_Counter)+Get_Number(1),Get_Number(50))
```

Original:
```text
MIN(GET_ANALVR(b43d1ce9-c8fe-434b-bbf0-7c2c7bb968eb)+Get_Number(1),Get_Number(50))
```

<a id="e-1e237a85-fdb9-4cf6-afbf-7ce26164677d"></a>

## str_anc_AAV_Elem_306_CS1_All

Source: `RuntimeExpressions` / `1e237a85-fdb9-4cf6-afbf-7ce26164677d`.

Predict CS1 in Future Years

Readable:
```text
IF(Get_Field(ELEM_306_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_306_CS1,YR-Get_Number(1))*(Get_Exp(str_anc_AAV_Elem_306_CS1_P1)-MIN(Get_Exp(str_anc_AAV_Elem_306_CS1_FACTOR)*GET_ANALVR(str_AAV_ELEM_306_Counter)/Get_Number(100),Get_Number(1))),Get_Number(0))
```

Original:
```text
IF(Get_Field(33c2b855-eefa-4211-b1c0-a5600d95c61f)>Get_Number(0),GET_ANALVAR_4_YR(b77e1377-73eb-4987-935c-0b00a714be05,YR-Get_Number(1))*(Get_Exp(aa4dd329-e566-4daf-8516-75129b8cc36a)-MIN(Get_Exp(11a65f89-7783-4c52-b25b-3bf411c475f0)*GET_ANALVR(e7eafdf0-b896-452b-8598-c957aa0a8928)/Get_Number(100),Get_Number(1))),Get_Number(0))
```

<a id="e-11a65f89-7783-4c52-b25b-3bf411c475f0"></a>

## str_anc_AAV_Elem_306_CS1_FACTOR

Source: `RuntimeExpressions` / `11a65f89-7783-4c52-b25b-3bf411c475f0`.

Return CS1 Deterioration Factor for Elem 306

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','FACTOR','Name','306_CS1',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','FACTOR','Name','306_CS1',TRUE))
```

<a id="e-549a516f-0efc-418b-a310-61095fbd1ed6"></a>

## str_anc_AAV_Elem_306_CS1_Initialize

Source: `dTIMSExpressions` / `549a516f-0efc-418b-a310-61095fbd1ed6`.

Initialize ELEM 306 CS1

Readable:
```text
IF(Get_Field(ELEM_306_QUANTITY)>Get_Number(0),Get_Field(ELEM_306_CS1)/Get_Field(ELEM_306_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(33c2b855-eefa-4211-b1c0-a5600d95c61f)>Get_Number(0),Get_Field(eb963e75-5273-45f7-b708-c8effc9682a6)/Get_Field(33c2b855-eefa-4211-b1c0-a5600d95c61f)*Get_Number(100),Get_Number(0))
```

<a id="e-aa4dd329-e566-4daf-8516-75129b8cc36a"></a>

## str_anc_AAV_Elem_306_CS1_P1

Source: `RuntimeExpressions` / `aa4dd329-e566-4daf-8516-75129b8cc36a`.

Return CS1 P1 for Element 306

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS1','Name','306_CS1',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS1','Name','306_CS1',TRUE))
```

<a id="e-eaee8e53-24d8-4157-a04d-e59a64e829fb"></a>

## str_anc_AAV_Elem_306_CS2_All

Source: `RuntimeExpressions` / `eaee8e53-24d8-4157-a04d-e59a64e829fb`.

Predict CS2 in Future Years

Readable:
```text
IF(Get_Field(ELEM_306_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_306_CS2,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_306_CS2_P2)+GET_ANALVAR_4_YR(str_AAV_ELEM_306_CS1,YR-Get_Number(1))-GET_ANALVR(str_AAV_ELEM_306_CS1),Get_Number(0))
```

Original:
```text
IF(Get_Field(33c2b855-eefa-4211-b1c0-a5600d95c61f)>Get_Number(0),GET_ANALVAR_4_YR(770ace05-eb51-431e-99da-6857e44f95ed,YR-Get_Number(1))*Get_Exp(e12ce34d-805e-4661-89b1-0f9028d97dae)+GET_ANALVAR_4_YR(b77e1377-73eb-4987-935c-0b00a714be05,YR-Get_Number(1))-GET_ANALVR(b77e1377-73eb-4987-935c-0b00a714be05),Get_Number(0))
```

<a id="e-67442f40-82fc-42df-bcbf-6205c8523b3f"></a>

## str_anc_AAV_Elem_306_CS2_Initialize

Source: `dTIMSExpressions` / `67442f40-82fc-42df-bcbf-6205c8523b3f`.

Initialize ELEM 306 CS2

Readable:
```text
IF(Get_Field(ELEM_306_QUANTITY)>Get_Number(0),Get_Field(ELEM_306_CS2)/Get_Field(ELEM_306_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(33c2b855-eefa-4211-b1c0-a5600d95c61f)>Get_Number(0),Get_Field(94752073-0721-4ff5-85b0-9c3467d857fb)/Get_Field(33c2b855-eefa-4211-b1c0-a5600d95c61f)*Get_Number(100),Get_Number(0))
```

<a id="e-e12ce34d-805e-4661-89b1-0f9028d97dae"></a>

## str_anc_AAV_Elem_306_CS2_P2

Source: `RuntimeExpressions` / `e12ce34d-805e-4661-89b1-0f9028d97dae`.

Return CS2 P2 for Element 306

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS2','Name','306_CS2',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS2','Name','306_CS2',TRUE))
```

<a id="e-0b950939-dc9f-4a00-b948-65e7f153433a"></a>

## str_anc_AAV_Elem_306_CS2_P3

Source: `RuntimeExpressions` / `0b950939-dc9f-4a00-b948-65e7f153433a`.

Return CS2 P3 for Element 306

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','306_CS2',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','306_CS2',TRUE))
```

<a id="e-ed68a4b7-16a2-4228-ab38-8f91e894ef31"></a>

## str_anc_AAV_Elem_306_CS3_All

Source: `RuntimeExpressions` / `ed68a4b7-16a2-4228-ab38-8f91e894ef31`.

Predict CS3 in Future Years

Readable:
```text
IF(Get_Field(ELEM_306_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_306_CS3,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_306_CS3_P3)+GET_ANALVAR_4_YR(str_AAV_ELEM_306_CS2,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_306_CS2_P3),Get_Number(0))
```

Original:
```text
IF(Get_Field(33c2b855-eefa-4211-b1c0-a5600d95c61f)>Get_Number(0),GET_ANALVAR_4_YR(c347bb77-f366-42d3-86c3-7520131241fe,YR-Get_Number(1))*Get_Exp(6ea0569a-b57e-4e51-a474-7a8db439e106)+GET_ANALVAR_4_YR(770ace05-eb51-431e-99da-6857e44f95ed,YR-Get_Number(1))*Get_Exp(0b950939-dc9f-4a00-b948-65e7f153433a),Get_Number(0))
```

<a id="e-fd465a23-bbce-46a3-b02e-6f82fdd44e72"></a>

## str_anc_AAV_Elem_306_CS3_Initialize

Source: `dTIMSExpressions` / `fd465a23-bbce-46a3-b02e-6f82fdd44e72`.

Initialize ELEM 306 CS3

Readable:
```text
IF(Get_Field(ELEM_306_QUANTITY)>Get_Number(0),Get_Field(ELEM_306_CS3)/Get_Field(ELEM_306_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(33c2b855-eefa-4211-b1c0-a5600d95c61f)>Get_Number(0),Get_Field(a7301dd0-3d3e-4e22-9e2d-e74c906d8b9a)/Get_Field(33c2b855-eefa-4211-b1c0-a5600d95c61f)*Get_Number(100),Get_Number(0))
```

<a id="e-6ea0569a-b57e-4e51-a474-7a8db439e106"></a>

## str_anc_AAV_Elem_306_CS3_P3

Source: `RuntimeExpressions` / `6ea0569a-b57e-4e51-a474-7a8db439e106`.

Return CS3 P3 for Element 306

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','306_CS3',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','306_CS3',TRUE))
```

<a id="e-a81762cb-e700-4d9f-a82d-7ba8c2e2d5ca"></a>

## str_anc_AAV_Elem_306_CS3_P4

Source: `RuntimeExpressions` / `a81762cb-e700-4d9f-a82d-7ba8c2e2d5ca`.

Return CS3 P4 for Element 306

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS4','Name','306_CS3',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS4','Name','306_CS3',TRUE))
```

<a id="e-f26f4bd6-c32f-4025-a579-96df354a9c4f"></a>

## str_anc_AAV_Elem_306_CS4_All

Source: `RuntimeExpressions` / `f26f4bd6-c32f-4025-a579-96df354a9c4f`.

Predict CS4 in Future Years

Readable:
```text
IF(Get_Field(ELEM_306_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_306_CS4,YR-Get_Number(1))+GET_ANALVAR_4_YR(str_AAV_ELEM_306_CS3,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_306_CS3_P4),Get_Number(0))
```

Original:
```text
IF(Get_Field(33c2b855-eefa-4211-b1c0-a5600d95c61f)>Get_Number(0),GET_ANALVAR_4_YR(d157f99d-c22e-4037-89ca-36b004f0f4b7,YR-Get_Number(1))+GET_ANALVAR_4_YR(c347bb77-f366-42d3-86c3-7520131241fe,YR-Get_Number(1))*Get_Exp(a81762cb-e700-4d9f-a82d-7ba8c2e2d5ca),Get_Number(0))
```

<a id="e-8cbea2dd-d780-488b-af4f-0e293f7b2fa1"></a>

## str_anc_AAV_Elem_306_CS4_Initialize

Source: `dTIMSExpressions` / `8cbea2dd-d780-488b-af4f-0e293f7b2fa1`.

Initialize ELEM 306 CS4

Readable:
```text
IF(Get_Field(ELEM_306_QUANTITY)>Get_Number(0),Get_Field(ELEM_306_CS4)/Get_Field(ELEM_306_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(33c2b855-eefa-4211-b1c0-a5600d95c61f)>Get_Number(0),Get_Field(efcea7dc-ea46-4dee-a688-620d99242a52)/Get_Field(33c2b855-eefa-4211-b1c0-a5600d95c61f)*Get_Number(100),Get_Number(0))
```

<a id="e-ad107b20-7440-49e0-b68e-9a567397c017"></a>

## str_anc_AAV_Elem_306_Counter_All

Source: `RuntimeExpressions` / `ad107b20-7440-49e0-b68e-9a567397c017`.

Increment the Elem 306 Counter


Readable:
```text
MIN(GET_ANALVR(str_AAV_ELEM_306_Counter)+Get_Number(1),Get_Number(50))
```

Original:
```text
MIN(GET_ANALVR(e7eafdf0-b896-452b-8598-c957aa0a8928)+Get_Number(1),Get_Number(50))
```

<a id="e-81b2341d-c404-414a-9d04-54fd9cd9323c"></a>

## str_anc_AAV_Elem_515_CS1_All

Source: `RuntimeExpressions` / `81b2341d-c404-414a-9d04-54fd9cd9323c`.

Predict CS1 in Future Years

Readable:
```text
IF(Get_Field(ELEM_515_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_515_CS1,YR-Get_Number(1))*(Get_Exp(str_anc_AAV_Elem_515_CS1_P1)-MIN(Get_Exp(str_anc_AAV_Elem_515_CS1_FACTOR)*GET_ANALVR(str_AAV_ELEM_515_Counter)/Get_Number(100),Get_Number(1))),Get_Number(0))
```

Original:
```text
IF(Get_Field(d16f20d2-56ee-4107-944e-fa25388c7c32)>Get_Number(0),GET_ANALVAR_4_YR(09d1110f-48ff-442c-aca2-0d1020ef618f,YR-Get_Number(1))*(Get_Exp(93087264-8a3a-49a5-9cd5-666ae876f0e2)-MIN(Get_Exp(00f01ac2-6ebe-452b-9714-c92e92ad8054)*GET_ANALVR(3e7cb478-1de4-4cbe-b8cc-dfa80aef9697)/Get_Number(100),Get_Number(1))),Get_Number(0))
```

<a id="e-00f01ac2-6ebe-452b-9714-c92e92ad8054"></a>

## str_anc_AAV_Elem_515_CS1_FACTOR

Source: `RuntimeExpressions` / `00f01ac2-6ebe-452b-9714-c92e92ad8054`.

Return CS1 Deterioration Factor for Elem 515

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','FACTOR','Name','515_CS1',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','FACTOR','Name','515_CS1',TRUE))
```

<a id="e-09aa0704-55ea-46a1-bc23-d6555c6cca97"></a>

## str_anc_AAV_Elem_515_CS1_Initialize

Source: `dTIMSExpressions` / `09aa0704-55ea-46a1-bc23-d6555c6cca97`.

Initialize ELEM 515 CS1

Readable:
```text
IF(Get_Field(ELEM_515_QUANTITY)>Get_Number(0),Get_Field(ELEM_515_CS1)/Get_Field(ELEM_515_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(d16f20d2-56ee-4107-944e-fa25388c7c32)>Get_Number(0),Get_Field(56abc2b6-6c58-4837-a65f-7e2701688d4e)/Get_Field(d16f20d2-56ee-4107-944e-fa25388c7c32)*Get_Number(100),Get_Number(0))
```

<a id="e-93087264-8a3a-49a5-9cd5-666ae876f0e2"></a>

## str_anc_AAV_Elem_515_CS1_P1

Source: `RuntimeExpressions` / `93087264-8a3a-49a5-9cd5-666ae876f0e2`.

Return CS1 P1 for Element 515

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS1','Name','515_CS1',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS1','Name','515_CS1',TRUE))
```

<a id="e-08605497-211e-494c-ae63-d191198bac49"></a>

## str_anc_AAV_Elem_515_CS2_All

Source: `RuntimeExpressions` / `08605497-211e-494c-ae63-d191198bac49`.

Predict CS2 in Future Years

Readable:
```text
IF(Get_Field(ELEM_515_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_515_CS2,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_515_CS2_P2)+GET_ANALVAR_4_YR(str_AAV_ELEM_515_CS1,YR-Get_Number(1))-GET_ANALVR(str_AAV_ELEM_515_CS1),Get_Number(0))
```

Original:
```text
IF(Get_Field(d16f20d2-56ee-4107-944e-fa25388c7c32)>Get_Number(0),GET_ANALVAR_4_YR(4b1a45de-6c89-46bb-9e4e-ce75aed28cd9,YR-Get_Number(1))*Get_Exp(d25b6a6d-d274-40e4-85e8-fa07ea0694b4)+GET_ANALVAR_4_YR(09d1110f-48ff-442c-aca2-0d1020ef618f,YR-Get_Number(1))-GET_ANALVR(09d1110f-48ff-442c-aca2-0d1020ef618f),Get_Number(0))
```

<a id="e-eb39b9e2-652b-4d29-a7c3-35c8405ed5ad"></a>

## str_anc_AAV_Elem_515_CS2_Initialize

Source: `dTIMSExpressions` / `eb39b9e2-652b-4d29-a7c3-35c8405ed5ad`.

Initialize ELEM 515 CS2

Readable:
```text
IF(Get_Field(ELEM_515_QUANTITY)>Get_Number(0),Get_Field(ELEM_515_CS2)/Get_Field(ELEM_515_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(d16f20d2-56ee-4107-944e-fa25388c7c32)>Get_Number(0),Get_Field(610095e1-8ee9-4043-8b41-d32cab08ec2f)/Get_Field(d16f20d2-56ee-4107-944e-fa25388c7c32)*Get_Number(100),Get_Number(0))
```

<a id="e-d25b6a6d-d274-40e4-85e8-fa07ea0694b4"></a>

## str_anc_AAV_Elem_515_CS2_P2

Source: `RuntimeExpressions` / `d25b6a6d-d274-40e4-85e8-fa07ea0694b4`.

Return CS2 P2 for Element 515

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS2','Name','515_CS2',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS2','Name','515_CS2',TRUE))
```

<a id="e-0d246353-2550-48d1-b949-0eb132405a6c"></a>

## str_anc_AAV_Elem_515_CS2_P3

Source: `RuntimeExpressions` / `0d246353-2550-48d1-b949-0eb132405a6c`.

Return CS2 P3 for Element 515

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','515_CS2',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','515_CS2',TRUE))
```

<a id="e-49bbe2ff-3016-41a3-a9b4-0ab07585d589"></a>

## str_anc_AAV_Elem_515_CS3_All

Source: `RuntimeExpressions` / `49bbe2ff-3016-41a3-a9b4-0ab07585d589`.

Predict CS3 in Future Years

Readable:
```text
IF(Get_Field(ELEM_515_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_515_CS3,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_515_CS3_P3)+GET_ANALVAR_4_YR(str_AAV_ELEM_515_CS2,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_515_CS2_P3),Get_Number(0))
```

Original:
```text
IF(Get_Field(d16f20d2-56ee-4107-944e-fa25388c7c32)>Get_Number(0),GET_ANALVAR_4_YR(7caba84c-5af2-4de1-aec3-c8cc44e239f9,YR-Get_Number(1))*Get_Exp(b2ee1f2c-0953-44fe-9ef3-965095d915ab)+GET_ANALVAR_4_YR(4b1a45de-6c89-46bb-9e4e-ce75aed28cd9,YR-Get_Number(1))*Get_Exp(0d246353-2550-48d1-b949-0eb132405a6c),Get_Number(0))
```

<a id="e-10836530-20dc-46eb-968f-4e99143fc8f0"></a>

## str_anc_AAV_Elem_515_CS3_Initialize

Source: `dTIMSExpressions` / `10836530-20dc-46eb-968f-4e99143fc8f0`.

Initialize ELEM 515 CS3

Readable:
```text
IF(Get_Field(ELEM_515_QUANTITY)>Get_Number(0),Get_Field(ELEM_515_CS3)/Get_Field(ELEM_515_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(d16f20d2-56ee-4107-944e-fa25388c7c32)>Get_Number(0),Get_Field(5ef09756-feee-43c9-82c4-162cb591dc8e)/Get_Field(d16f20d2-56ee-4107-944e-fa25388c7c32)*Get_Number(100),Get_Number(0))
```

<a id="e-b2ee1f2c-0953-44fe-9ef3-965095d915ab"></a>

## str_anc_AAV_Elem_515_CS3_P3

Source: `RuntimeExpressions` / `b2ee1f2c-0953-44fe-9ef3-965095d915ab`.

Return CS3 P3 for Element 515

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','515_CS3',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS3','Name','515_CS3',TRUE))
```

<a id="e-1bcd2920-3754-4c06-8dfb-02d2caad1a71"></a>

## str_anc_AAV_Elem_515_CS3_P4

Source: `RuntimeExpressions` / `1bcd2920-3754-4c06-8dfb-02d2caad1a71`.

Return CS3 P4 for Element 515

Readable:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS4','Name','515_CS3',TRUE))
```

Original:
```text
VAL(DAL_DCG_TLOOKUP('Bridge_Analysis_Lookup_Element_Curves','CS4','Name','515_CS3',TRUE))
```

<a id="e-c9e6d5da-a7f7-4624-9206-4dcf99ff1845"></a>

## str_anc_AAV_Elem_515_CS4_All

Source: `RuntimeExpressions` / `c9e6d5da-a7f7-4624-9206-4dcf99ff1845`.

Predict CS4 in Future Years

Readable:
```text
IF(Get_Field(ELEM_515_QUANTITY)>Get_Number(0),GET_ANALVAR_4_YR(str_AAV_ELEM_515_CS4,YR-Get_Number(1))+GET_ANALVAR_4_YR(str_AAV_ELEM_515_CS3,YR-Get_Number(1))*Get_Exp(str_anc_AAV_Elem_515_CS3_P4),Get_Number(0))
```

Original:
```text
IF(Get_Field(d16f20d2-56ee-4107-944e-fa25388c7c32)>Get_Number(0),GET_ANALVAR_4_YR(45cc163b-7547-4c6f-a0fa-c952651c697c,YR-Get_Number(1))+GET_ANALVAR_4_YR(7caba84c-5af2-4de1-aec3-c8cc44e239f9,YR-Get_Number(1))*Get_Exp(1bcd2920-3754-4c06-8dfb-02d2caad1a71),Get_Number(0))
```

<a id="e-8b5a8c7c-4a69-4db5-8645-59bf92e1464f"></a>

## str_anc_AAV_Elem_515_CS4_Initialize

Source: `dTIMSExpressions` / `8b5a8c7c-4a69-4db5-8645-59bf92e1464f`.

Initialize ELEM 515 CS4

Readable:
```text
IF(Get_Field(ELEM_515_QUANTITY)>Get_Number(0),Get_Field(ELEM_515_CS4)/Get_Field(ELEM_515_QUANTITY)*Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(d16f20d2-56ee-4107-944e-fa25388c7c32)>Get_Number(0),Get_Field(e04638fe-59c0-46f3-9121-0373a87e65b8)/Get_Field(d16f20d2-56ee-4107-944e-fa25388c7c32)*Get_Number(100),Get_Number(0))
```

<a id="e-c86fb657-16d8-4d82-89cb-e6fd0258ffa1"></a>

## str_anc_AAV_Elem_515_Counter_All

Source: `RuntimeExpressions` / `c86fb657-16d8-4d82-89cb-e6fd0258ffa1`.

Increment the Elem 515 Counter


Readable:
```text
MIN(GET_ANALVR(str_AAV_ELEM_515_Counter)+Get_Number(1),Get_Number(50))
```

Original:
```text
MIN(GET_ANALVR(3e7cb478-1de4-4cbe-b8cc-dfa80aef9697)+Get_Number(1),Get_Number(50))
```

<a id="e-c2cfca67-6079-427b-b67b-66a023b4bdcc"></a>

## str_anc_OBJ_One

Source: `dTIMSExpressions` / `c2cfca67-6079-427b-b67b-66a023b4bdcc`.

One

Readable:
```text
Get_Number(1)
```

Original:
```text
Get_Number(1)
```

<a id="e-d5d0408c-3f4b-4e67-87f0-db4ab4649e95"></a>

## str_anc_RES_ELEM_1080_CS1_100

Source: `dTIMSExpressions` / `d5d0408c-3f4b-4e67-87f0-db4ab4649e95`.

Reset CS1 to 100 if the quantity is > 0

Readable:
```text
IF(Get_Field(ELEM_1080_QUANTITY)>Get_Number(0),Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(56df5f38-8963-4729-9821-1948e051b920)>Get_Number(0),Get_Number(100),Get_Number(0))
```

<a id="e-8ac64326-c92e-4be6-90cf-f64a17840213"></a>

## str_anc_RES_ELEM_1080_CS1_PATCH

Source: `RuntimeExpressions` / `8ac64326-c92e-4be6-90cf-f64a17840213`.

Reset CS1 to 100 if the quantity is > 0

Readable:
```text
IF(Get_Field(ELEM_1080_QUANTITY)>Get_Number(0),
    GET_ANALVR(str_AAV_ELEM_1080_CS1) + GET_ANALVR(str_AAV_ELEM_1080_CS3)+ GET_ANALVR(str_AAV_ELEM_1080_CS4)
,
Get_Number(0))
```

Original:
```text
IF(Get_Field(56df5f38-8963-4729-9821-1948e051b920)>Get_Number(0),
    GET_ANALVR(b0325986-565f-4dc9-9ee7-c37d3f531a04) + GET_ANALVR(53bec880-322b-4ac1-a03a-c79fb354c4fb)+ GET_ANALVR(454eb22e-95d5-4589-9f60-860fbaaff091)
,
Get_Number(0))
```

<a id="e-d13100c3-691b-469f-9148-983f2cbe512a"></a>

## str_anc_RES_ELEM_1130_CS1_100

Source: `dTIMSExpressions` / `d13100c3-691b-469f-9148-983f2cbe512a`.

Reset CS1 to 100 if the quantity is > 0

Readable:
```text
IF(Get_Field(ELEM_1130_QUANTITY)>Get_Number(0),Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(c1f78423-32d6-423c-b986-b5855431bbb3)>Get_Number(0),Get_Number(100),Get_Number(0))
```

<a id="e-11651337-019a-46ee-abed-ce179e92c656"></a>

## str_anc_RES_ELEM_300_CS1_100

Source: `dTIMSExpressions` / `11651337-019a-46ee-abed-ce179e92c656`.

Reset CS1 to 100 if the quantity is > 0

Readable:
```text
IF(Get_Field(ELEM_300_QUANTITY)>Get_Number(0),Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(9aedad63-77e7-447a-8c44-21a89ae03440)>Get_Number(0),Get_Number(100),Get_Number(0))
```

<a id="e-87e1f2fc-889e-4bfd-9d4c-0c04b0ac00b2"></a>

## str_anc_RES_ELEM_301_CS1_100

Source: `dTIMSExpressions` / `87e1f2fc-889e-4bfd-9d4c-0c04b0ac00b2`.

Reset CS1 to 100 if the quantity is > 0

Readable:
```text
IF(Get_Field(ELEM_301_QUANTITY)>Get_Number(0),Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(4b504462-b48a-473c-925c-d7a8705fb230)>Get_Number(0),Get_Number(100),Get_Number(0))
```

<a id="e-32cd159a-7d6f-43ed-bfa0-8f503403b4ea"></a>

## str_anc_RES_ELEM_302_CS1_100

Source: `dTIMSExpressions` / `32cd159a-7d6f-43ed-bfa0-8f503403b4ea`.

Reset CS1 to 100 if the quantity is > 0

Readable:
```text
IF(Get_Field(ELEM_302_QUANTITY)>Get_Number(0),Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(286fae98-ad52-46cc-adab-7d5978b28ac0)>Get_Number(0),Get_Number(100),Get_Number(0))
```

<a id="e-9edfea07-ae41-457a-a6e7-e590f28713aa"></a>

## str_anc_RES_ELEM_303_CS1_100

Source: `dTIMSExpressions` / `9edfea07-ae41-457a-a6e7-e590f28713aa`.

Reset CS1 to 100 if the quantity is > 0

Readable:
```text
IF(Get_Field(ELEM_303_QUANTITY)>Get_Number(0),Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(0caab4da-a7c0-4635-a19e-e82950b8b8fc)>Get_Number(0),Get_Number(100),Get_Number(0))
```

<a id="e-2fc6e930-2fc3-4af0-98e3-9d77cce32b83"></a>

## str_anc_RES_ELEM_304_CS1_100

Source: `dTIMSExpressions` / `2fc6e930-2fc3-4af0-98e3-9d77cce32b83`.

Reset CS1 to 100 if the quantity is > 0

Readable:
```text
IF(Get_Field(ELEM_304_QUANTITY)>Get_Number(0),Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(56ab8060-0651-4223-b119-3043fe5a0abc)>Get_Number(0),Get_Number(100),Get_Number(0))
```

<a id="e-7e0ab062-d674-4d2d-8e27-310320ef5779"></a>

## str_anc_RES_ELEM_305_CS1_100

Source: `dTIMSExpressions` / `7e0ab062-d674-4d2d-8e27-310320ef5779`.

Reset CS1 to 100 if the quantity is > 0

Readable:
```text
IF(Get_Field(ELEM_305_QUANTITY)>Get_Number(0),Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(87443be7-82d6-4927-9f74-a8e47f9602b0)>Get_Number(0),Get_Number(100),Get_Number(0))
```

<a id="e-3a9f0a16-970e-42f1-9de4-0a97a7441376"></a>

## str_anc_RES_ELEM_306_CS1_100

Source: `dTIMSExpressions` / `3a9f0a16-970e-42f1-9de4-0a97a7441376`.

Reset Elem 306 CS1 to 100 if exists

Readable:
```text
IF(Get_Field(ELEM_306_QUANTITY)>Get_Number(0),Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(33c2b855-eefa-4211-b1c0-a5600d95c61f)>Get_Number(0),Get_Number(100),Get_Number(0))
```

<a id="e-47efa9b8-0f4d-41a5-b398-2358e7e0d55d"></a>

## str_anc_RES_ELEM_515_CS1_100

Source: `dTIMSExpressions` / `47efa9b8-0f4d-41a5-b398-2358e7e0d55d`.

Reset CS1 to 100 if the quantity is > 0

Readable:
```text
IF(Get_Field(ELEM_515_QUANTITY)>Get_Number(0),Get_Number(100),Get_Number(0))
```

Original:
```text
IF(Get_Field(d16f20d2-56ee-4107-944e-fa25388c7c32)>Get_Number(0),Get_Number(100),Get_Number(0))
```

<a id="e-8e7e4c3c-6484-4c5a-9ba3-5da32586cf20"></a>

## str_anc_RES_ELEM_515_CS1_34

Source: `RuntimeExpressions` / `8e7e4c3c-6484-4c5a-9ba3-5da32586cf20`.

Reset Elem 515 CS1 to the sum of CS1, CS3, and CS4

Readable:
```text
GET_ANALVR(str_AAV_ELEM_515_CS1)+GET_ANALVR(str_AAV_ELEM_515_CS3)+GET_ANALVR(str_AAV_ELEM_515_CS4)
```

Original:
```text
GET_ANALVR(09d1110f-48ff-442c-aca2-0d1020ef618f)+GET_ANALVR(7caba84c-5af2-4de1-aec3-c8cc44e239f9)+GET_ANALVR(45cc163b-7547-4c6f-a0fa-c952651c697c)
```

<a id="e-3ae6f6a8-880c-4613-9e37-5f9b2aeb1d8e"></a>

## str_anc_RES_ELEM_515_CS1_All

Source: `RuntimeExpressions` / `3ae6f6a8-880c-4613-9e37-5f9b2aeb1d8e`.

Reset Elem 515 CS1 to the sum of all condition states

Readable:
```text
GET_ANALVR(str_AAV_ELEM_515_CS1)+GET_ANALVR(str_AAV_ELEM_515_CS2)+GET_ANALVR(str_AAV_ELEM_515_CS3)+GET_ANALVR(str_AAV_ELEM_515_CS4)
```

Original:
```text
GET_ANALVR(09d1110f-48ff-442c-aca2-0d1020ef618f)+GET_ANALVR(4b1a45de-6c89-46bb-9e4e-ce75aed28cd9)+GET_ANALVR(7caba84c-5af2-4de1-aec3-c8cc44e239f9)+GET_ANALVR(45cc163b-7547-4c6f-a0fa-c952651c697c)
```

<a id="e-e4261379-3d35-4309-bbc4-83a7bb241aa3"></a>

## str_anctAAV_Last_Major_Treatment

Source: `dTIMSExpressions` / `e4261379-3d35-4309-bbc4-83a7bb241aa3`.

Set it to an empty string.

Readable:
```text
''
```

Original:
```text
''
```
