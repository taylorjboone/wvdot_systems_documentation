# PMS treatment catalog

Source: live test-service snapshot fetched through Windows host T20DOHB05L09456 on 2026-09-24. This is a static configuration audit; the proprietary dTIMS execution engine was not run.


Grouping follows the captured treatment-name prefixes (`PMS_` for pavement, `str_` for structures). All ordered rows are retained.

## PMS_County_Chip_Seal

Chip Seal for county routes

ID: `febe52da-6fab-4a9d-82f0-c9245fd84613`. Type: **Major**. IntervalYear: **3**. IsInitial: `1`. ApplyAfterInitial: `0`. Budget: **Rehabilition**.

### Trigger

[PMS_abfTRIG_County_Chip_Seal](expressions.md#e-c0226ede-40da-4205-a0f0-38d8e346b561)

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

### Ordered resets

Order | Variable | Filter | Reset expression
---: | --- | --- | ---
0 | PMS_nAAV_CND_ECI | (none) | [PMS_ancRES_ECI_CHIP_SEAL](expressions.md#e-fa36e4d4-2f5d-4372-b223-f083929bb4b0)
1 | PMS_nAAV_CND_SCI | (none) | [PMS_ancRES_SCI_CHIP_SEAL](expressions.md#e-22a19aac-e4c6-40e0-849a-afc86dc092fc)
2 | PMS_nAAV_CND_CCI | (none) | [PMS_ancRES_CCI_CHIP_SEAL](expressions.md#e-acb4e2c4-97bf-4f5e-9b94-908560724028)
3 | PMS_nAAV_AGE_ECI | (none) | [PMS_ancAGE_ECI_AGE_FROM_INDEX](expressions.md#e-a98afc4d-071a-4fc7-86ef-7840afcd83e8)
4 | PMS_nAAV_AGE_SCI | (none) | [PMS_ancAGE_SCI_AGE_FROM_INDEX](expressions.md#e-2ef1c4f5-220d-45a3-860d-d073db59ef9e)
5 | PMS_nAAV_AGE_CCI | (none) | [PMS_ancAGE_CCI_AGE_FROM_INDEX](expressions.md#e-2dbc899c-4c91-45a0-bd93-e02b1456b995)
6 | PMS_nAAV_CND_PCRK | (none) | [PMS_ancRES_PCRK](expressions.md#e-0a1d81b8-b54b-490f-9238-9e8cc47b9f96)
7 | PMS_nAAV_CND_RSL | (none) | [PMS_ancCND_RSL](expressions.md#e-7fbb09b7-c2ae-4497-8890-e69a5d3999b6)
8 | PMS_tDAV_Rehab_Type | (none) | [PMS_ancOBJ_ABS_Minor](expressions.md#e-8fa0a363-e9d0-4bc7-8324-822d97acb948)
9 | PMS_tDAV_Truck_Load | (none) | [PMS_ancTRF_Truck_Load](expressions.md#e-0a9b6cd0-79b4-4da2-a728-ab165b8fe547)
10 | PMS_nAAV_Yrly_Cost | (none) | [PMS_ancOBJ_AAV_Yrly_Cost_All](expressions.md#e-76d307ed-3427-462f-a79f-e16a387566dd)
11 | PMS_nDAV_CNT_MICROSURFACE | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
12 | PMS_tAAV_FLT_GFP | (none) | [PMS_ancCND_FLT_GFP](expressions.md#e-8696dc20-6bf3-44d2-b7c8-d93b39ae6fc3)
13 | PMS_tAAV_IRI_GFP | (none) | [PMS_ancCND_IRI_GFP](expressions.md#e-ab06bc85-2e62-4269-aeda-d8bd7144b6ad)
14 | PMS_tAAV_PCRK_GFP | (none) | [PMS_ancCND_PCRK_GFP](expressions.md#e-40e28ca8-4605-426b-8c97-7b2c1cc92571)
15 | PMS_tAAV_RUT_GFP | (none) | [PMS_ancCND_RUT_GFP](expressions.md#e-04c76ab6-b287-4c9d-9399-90033e4cc5e7)
16 | PMS_tAAV_MAP21_GFP | (none) | [PMS_ancCND_MAP21_GFP](expressions.md#e-0452c4fb-af93-4324-bc0b-4576e857ae86)
17 | PMS_nDAV_CNT_CHIP_SEALS | (none) | [PMS_ancRES_CNT_CHIP_SEAL](expressions.md#e-455714c1-bc1f-4743-a66e-1e1d92bee2cc)
18 | PMS_tAAV_YEARLY_TREATMENT | (none) | [PMS_ancRES_Yearly_Treatment](expressions.md#e-ed2f1535-a24f-4156-8dbe-8b5e7dda5f7b)

### Costs

Order | Filter | Financial expression | Economic expression
---: | --- | --- | ---
0 | (none) | [PMS_ancCOST_County_Chip_Seal](expressions.md#e-8711652e-c824-4e25-b85e-d6aa363f7c4b) | (none)

### Allowed subsequent treatments

Order | Treatment
---: | ---
1 | PMS_County_Chip_Seal
2 | PMS_County_MicroSurface
3 | PMS_County_Thick_Overlay
4 | PMS_County_Thin_Overlay
5 | PMS_PM_Crack_Seal
6 | PMS_PM_Cape_Seal
7 | PMS_PM_Ultra_Thin_Overlay
8 | PMS_Reconstruction

### Ancillary treatments

Order | Treatment
---: | ---

### Analysis-set membership

No captured membership.

Transitive configuration dependency closure: 719 records; query `audit_treatment_dependencies`.

## PMS_County_MicroSurface

Microsurfacing for county routes

ID: `80971e42-14d0-41b3-b566-59f6d59de612`. Type: **Major**. IntervalYear: **3**. IsInitial: `1`. ApplyAfterInitial: `0`. Budget: **9ef54d0a-bdbb-4b9b-ab3e-8277bd08b827**.

### Trigger

[PMS_abfTRIG_County_Microsurfacing](expressions.md#e-e7b820af-96b2-4779-92a3-1757809044e2)

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

### Ordered resets

Order | Variable | Filter | Reset expression
---: | --- | --- | ---
0 | PMS_nAAV_CND_ECI | (none) | [PMS_ancRES_ECI_MICROSURFACE](expressions.md#e-e87af607-69b3-4c46-96e2-5a91a4f471d0)
1 | PMS_nAAV_CND_PSI | (none) | [PMS_ancRES_PSI_MICROSURFACE](expressions.md#e-b0ed3473-2081-4c83-926d-0440557ed1b1)
2 | PMS_nAAV_CND_RDI | (none) | [PMS_ancRES_RDI_MICROSURFACE](expressions.md#e-9d879d4e-9d1d-4f51-8cec-2c9e391319a4)
3 | PMS_nAAV_CND_SCI | (none) | [PMS_ancRES_SCI_MICROSURFACE](expressions.md#e-2eeb79c4-579f-44e3-8bdc-3ea05f4369b5)
4 | PMS_nAAV_CND_CCI | (none) | [PMS_ancRES_CCI_MICROSURFACE](expressions.md#e-0db279f4-1eaf-41c8-9a50-5be54360cfed)
5 | PMS_nAAV_AGE_ECI | (none) | [PMS_ancAGE_ECI_AGE_FROM_INDEX](expressions.md#e-a98afc4d-071a-4fc7-86ef-7840afcd83e8)
6 | PMS_nAAV_AGE_PSI | (none) | [PMS_ancAGE_PSI_AGE_FROM_INDEX](expressions.md#e-af3d20fc-fa3b-4485-bcee-8714e4acca9f)
7 | PMS_nAAV_AGE_RDI | (none) | [PMS_ancAGE_RDI_AGE_FROM_INDEX](expressions.md#e-193bb441-a7ab-412f-9d12-ab4247b78d6a)
8 | PMS_nAAV_AGE_SCI | (none) | [PMS_ancAGE_SCI_AGE_FROM_INDEX](expressions.md#e-2ef1c4f5-220d-45a3-860d-d073db59ef9e)
9 | PMS_nAAV_AGE_CCI | (none) | [PMS_ancAGE_CCI_AGE_FROM_INDEX](expressions.md#e-2dbc899c-4c91-45a0-bd93-e02b1456b995)
10 | PMS_nAAV_CND_RSL | (none) | [PMS_ancCND_RSL](expressions.md#e-7fbb09b7-c2ae-4497-8890-e69a5d3999b6)
11 | PMS_nAAV_CND_IRI | (none) | [PMS_ancRES_IRI](expressions.md#e-1d4efdbd-03bf-4bc2-b189-da59dab901ae)
12 | PMS_nAAV_CND_PCRK | (none) | [PMS_ancCND_PCRK](expressions.md#e-b33b7403-ae8e-47b1-9bb8-a3b102200464)
13 | PMS_nAAV_CND_RUT | (none) | [PMS_ancCND_Rut](expressions.md#e-4f8cf211-5f31-4d5e-92dd-6f048cf7f6c6)
14 | PMS_tDAV_Rehab_Type | (none) | [PMS_ancOBJ_ABS_Minor](expressions.md#e-8fa0a363-e9d0-4bc7-8324-822d97acb948)
15 | PMS_tDAV_Truck_Load | (none) | [PMS_ancTRF_Truck_Load](expressions.md#e-0a9b6cd0-79b4-4da2-a728-ab165b8fe547)
16 | PMS_nAAV_Yrly_Cost | (none) | [PMS_ancOBJ_AAV_Yrly_Cost_All](expressions.md#e-76d307ed-3427-462f-a79f-e16a387566dd)
17 | PMS_tAAV_FLT_GFP | (none) | [PMS_ancCND_FLT_GFP](expressions.md#e-8696dc20-6bf3-44d2-b7c8-d93b39ae6fc3)
18 | PMS_tAAV_IRI_GFP | (none) | [PMS_ancCND_IRI_GFP](expressions.md#e-ab06bc85-2e62-4269-aeda-d8bd7144b6ad)
19 | PMS_tAAV_PCRK_GFP | (none) | [PMS_ancCND_PCRK_GFP](expressions.md#e-40e28ca8-4605-426b-8c97-7b2c1cc92571)
20 | PMS_tAAV_RUT_GFP | (none) | [PMS_ancCND_RUT_GFP](expressions.md#e-04c76ab6-b287-4c9d-9399-90033e4cc5e7)
21 | PMS_tAAV_MAP21_GFP | (none) | [PMS_ancCND_MAP21_GFP](expressions.md#e-0452c4fb-af93-4324-bc0b-4576e857ae86)
22 | PMS_nDAV_CNT_CHIP_SEALS | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
23 | PMS_nDAV_CNT_MICROSURFACE | (none) | [PMS_ancRES_CNT_MICROSURFACE](expressions.md#e-870fadb0-cdad-49eb-829f-599710b454e3)
24 | PMS_tAAV_YEARLY_TREATMENT | (none) | [PMS_ancRES_Yearly_Treatment](expressions.md#e-ed2f1535-a24f-4156-8dbe-8b5e7dda5f7b)

### Costs

Order | Filter | Financial expression | Economic expression
---: | --- | --- | ---
0 | (none) | [PMS_ancCOST_County_Microsurfacing](expressions.md#e-1cb4792b-85b4-401c-9b18-5bb049572af2) | (none)

### Allowed subsequent treatments

Order | Treatment
---: | ---
1 | PMS_County_Thick_Overlay
2 | PMS_County_Thin_Overlay
3 | PMS_PM_Ultra_Thin_Overlay
4 | PMS_Reconstruction
5 | PMS_Preservation
6 | PMS_Fair_Treatment_For_GFP_Analaysis_70P_Good

### Ancillary treatments

Order | Treatment
---: | ---

### Analysis-set membership

- DEL_STIP_2026_DISTRICT_009_Non_NHS; row `00f29526-4949-443e-afd7-167271320f9e`
- DEL_STIP_2026_DISTRICT_006_Non_NHS; row `f262a330-1f0a-4861-94fa-25d911746699`
- DEL_STIP_2026_DISTRICT_008_Non_NHS; row `f24c7e0b-86d2-4b4e-805a-2e4b0aac6b74`
- DEL_STIP_2026_DISTRICT_002_Non_NHS; row `13a782ef-b2f4-4376-b8af-45e85f53c008`
- DEL_STIP_2026_DISTRICT_010_Non_NHS; row `34ae2bb7-e1ef-45f5-9add-5b05e2ea67f1`
- DEL_STIP_2026_DISTRICT_003_Non_NHS; row `c3223653-c63c-49b2-9500-5e6d7a92af5f`
- DEL_STIP_2026_DISTRICT_007_Non_NHS; row `d0508bcf-8356-43c4-b105-8b85e71b19d2`
- DEL_STIP_2026_DISTRICT_001_Non_NHS; row `d9a66777-582b-44cb-8f5f-942ce21fa641`
- DEL_NonNHS_Routes; row `396d9ddd-c87b-4483-b10f-942fa9dde63a`
- DEL_STIP_2026_Non_NHS_ALL_NETWORK; row `81d12a9d-8d21-4193-a08e-c35fa4c2f425`
- DEL_STIP_2026_DISTRICT_004_Non_NHS; row `dd5d2677-630f-47af-b6a1-cb13393964bb`
- DEL_STIP_2026_DISTRICT_005_Non_NHS; row `64710ac4-1301-4ca6-a43c-d30e3a0d0229`

Transitive configuration dependency closure: 898 records; query `audit_treatment_dependencies`.

## PMS_County_Thick_Overlay

Thick Overlay for counties

ID: `d036c403-994d-4b20-82ae-e1d6653fe922`. Type: **Major**. IntervalYear: **6**. IsInitial: `1`. ApplyAfterInitial: `0`. Budget: **Rehabilition**.

### Trigger

[PMS_abfTRIG_County_Thick_Overlay](expressions.md#e-fa6d626c-f568-419c-b630-6c90ac7e8c7e)

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

### Ordered resets

Order | Variable | Filter | Reset expression
---: | --- | --- | ---
0 | PMS_nAAV_AGE_CSI | [PMS_abfOBJ_Concrete](expressions.md#e-ba469472-994d-4555-923b-c833047e7e8b) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
1 | PMS_nAAV_AGE_JCI | [PMS_abfOBJ_Concrete](expressions.md#e-ba469472-994d-4555-923b-c833047e7e8b) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
2 | PMS_nAAV_AGE_ECI | [PMS_abfOBJ_Asphalt](expressions.md#e-915f80f1-74d8-48c0-ab9f-fdffd05d547a) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
3 | PMS_nAAV_AGE_RDI | [PMS_abfOBJ_Asphalt](expressions.md#e-915f80f1-74d8-48c0-ab9f-fdffd05d547a) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
4 | PMS_nAAV_AGE_SCI | [PMS_abfOBJ_Asphalt](expressions.md#e-915f80f1-74d8-48c0-ab9f-fdffd05d547a) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
5 | PMS_nAAV_AGE_PSI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
6 | PMS_nAAV_AGE_CCI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
7 | PMS_nAAV_CND_CSI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
8 | PMS_nAAV_CND_JCI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
9 | PMS_nAAV_CND_ECI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
10 | PMS_nAAV_CND_RDI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
11 | PMS_nAAV_CND_SCI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
12 | PMS_nAAV_CND_PSI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
13 | PMS_nAAV_CND_CCI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
14 | PMS_nAAV_CND_IRI | (none) | [PMS_ancRES_IRI](expressions.md#e-1d4efdbd-03bf-4bc2-b189-da59dab901ae)
15 | PMS_nAAV_CND_PCRK | (none) | [PMS_ancRES_PCRK](expressions.md#e-0a1d81b8-b54b-490f-9238-9e8cc47b9f96)
16 | PMS_nAAV_CND_RUT | (none) | [PMS_ancCND_Rut](expressions.md#e-4f8cf211-5f31-4d5e-92dd-6f048cf7f6c6)
17 | PMS_nAAV_CND_RSL | (none) | [PMS_ancCND_RSL](expressions.md#e-7fbb09b7-c2ae-4497-8890-e69a5d3999b6)
18 | PMS_tDAV_Rehab_Type | (none) | [PMS_ancOBJ_ABS_Major](expressions.md#e-f5a30d2f-e3d8-4245-998f-1f9088ccbdc1)
19 | PMS_tDAV_Truck_Load | (none) | [PMS_ancTRF_Truck_Load](expressions.md#e-0a9b6cd0-79b4-4da2-a728-ab165b8fe547)
20 | PMS_nAAV_Yrly_Cost | (none) | [PMS_ancOBJ_AAV_Yrly_Cost_All](expressions.md#e-76d307ed-3427-462f-a79f-e16a387566dd)
21 | PMS_tAAV_FLT_GFP | (none) | [PMS_ancCND_FLT_GFP](expressions.md#e-8696dc20-6bf3-44d2-b7c8-d93b39ae6fc3)
22 | PMS_tAAV_IRI_GFP | (none) | [PMS_ancCND_IRI_GFP](expressions.md#e-ab06bc85-2e62-4269-aeda-d8bd7144b6ad)
23 | PMS_tAAV_PCRK_GFP | (none) | [PMS_ancCND_PCRK_GFP](expressions.md#e-40e28ca8-4605-426b-8c97-7b2c1cc92571)
24 | PMS_tAAV_RUT_GFP | (none) | [PMS_ancCND_RUT_GFP](expressions.md#e-04c76ab6-b287-4c9d-9399-90033e4cc5e7)
25 | PMS_tAAV_MAP21_GFP | (none) | [PMS_ancCND_MAP21_GFP](expressions.md#e-0452c4fb-af93-4324-bc0b-4576e857ae86)
26 | PMS_nDAV_CNT_CHIP_SEALS | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
27 | PMS_nDAV_CNT_MICROSURFACE | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
28 | PMS_tAAV_YEARLY_TREATMENT | (none) | [PMS_ancRES_Yearly_Treatment](expressions.md#e-ed2f1535-a24f-4156-8dbe-8b5e7dda5f7b)

### Costs

Order | Filter | Financial expression | Economic expression
---: | --- | --- | ---
0 | (none) | [PMS_ancCOST_County_Thick_Overlay](expressions.md#e-0d77d7ef-38b3-4e3b-b84f-72aa2c09158e) | (none)

### Allowed subsequent treatments

Order | Treatment
---: | ---
1 | PMS_County_Chip_Seal
2 | PMS_County_MicroSurface
3 | PMS_County_Thick_Overlay
4 | PMS_County_Thin_Overlay
5 | PMS_PM_Crack_Seal
6 | PMS_PM_Chip_Seal
7 | PMS_PM_Cape_Seal
8 | PMS_PM_Microsurfacing
9 | PMS_PM_Ultra_Thin_Overlay
10 | PMS_Reconstruction
11 | PMS_PM_Asphalt
12 | PMS_Fair_Treatment_For_GFP_Analaysis_70P_Good
12 | PMS_Fair_Treatment_For_GFP_Analaysis_70P_Good

### Ancillary treatments

Order | Treatment
---: | ---

### Analysis-set membership

- DEL_STIP_2026_DISTRICT_005_Non_NHS; row `5f05e5d5-706d-409d-a926-0b8dde3c9244`
- DEL_STIP_2026_DISTRICT_004_NHS_ONLY; row `3fe659a2-80c9-4e1d-8ead-0bfe1d89d904`
- DEL_STIP_2026_DISTRICT_010_Non_NHS; row `7e7987be-1aca-4290-b002-1b8df2de51e5`
- DEL_STIP_2026_DISTRICT_004_Non_NHS; row `0eb6b473-d8b5-45c1-863f-4169ad68703d`
- DEL_STIP_2026_Non_NHS_ALL_NETWORK; row `86d99f5c-01e7-4aa7-963f-457608d85ab6`
- DEL_NonNHS_Routes; row `1126f4b0-12c0-44cf-80b3-5035704030bd`
- DEL_STIP_2026_DISTRICT_007_Non_NHS; row `7db68639-a182-4421-892c-7fdcba29da39`
- DEL_STIP_2026_DISTRICT_008_Non_NHS; row `b4cc9d0c-b411-4b80-b035-8942c15a76a1`
- DEL_STIP_2026_DISTRICT_002_Non_NHS; row `cf7d9df6-c10a-4367-acdf-9ea49e3e5fb4`
- DEL_STIP_2026_DISTRICT_006_Non_NHS; row `fe87ced2-7f35-4e73-b635-9fa34e638b42`
- DEL_STIP_2026_DISTRICT_009_Non_NHS; row `4cc60324-d6ca-4838-918c-a70b2d4da1ab`
- DEL_STIP_2026_DISTRICT_001_Non_NHS; row `562b94c3-6997-4a97-b6a7-e9f646ad16d4`
- DEL_STIP_2026_DISTRICT_003_Non_NHS; row `b3bec1c8-d885-42c8-a42a-ff6bc3ffd34b`

Transitive configuration dependency closure: 915 records; query `audit_treatment_dependencies`.

## PMS_County_Thin_Overlay

Thin Overlay for county routes

ID: `69b9d202-05fe-4be9-865e-db35ede4eb9c`. Type: **Major**. IntervalYear: **6**. IsInitial: `1`. ApplyAfterInitial: `0`. Budget: **Rehabilition**.

### Trigger

[PMS_abfTRIG_County_Thin_Overlay](expressions.md#e-9a433234-e459-461d-a629-75b50a89f2e5)

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

### Ordered resets

Order | Variable | Filter | Reset expression
---: | --- | --- | ---
0 | PMS_nAAV_CND_ECI | (none) | [PMS_ancRES_ECI_THIN_OVERLAY](expressions.md#e-384514d5-5dee-4e86-a5c7-6bb5b3dd4a71)
1 | PMS_nAAV_CND_PSI | (none) | [PMS_ancRES_PSI_THIN_OVERLAY](expressions.md#e-3c2ad86c-8882-44b2-947a-aa1cd954f678)
2 | PMS_nAAV_CND_RDI | (none) | [PMS_ancRES_RDI_THIN_OVERLAY](expressions.md#e-4324d58a-d04d-4508-9ad6-ddadbbe810cf)
3 | PMS_nAAV_CND_SCI | (none) | [PMS_ancRES_SCI_THIN_OVERLAY](expressions.md#e-dbe9ae0c-cedb-480d-b047-f7941dbc4e62)
4 | PMS_nAAV_CND_CCI | (none) | [PMS_ancRES_CCI_THIN_OVERLAY](expressions.md#e-bf3aed6d-d0f5-4275-9a95-a7b9b5520e68)
5 | PMS_nAAV_AGE_ECI | (none) | [PMS_ancAGE_ECI_AGE_FROM_INDEX](expressions.md#e-a98afc4d-071a-4fc7-86ef-7840afcd83e8)
6 | PMS_nAAV_AGE_PSI | (none) | [PMS_ancAGE_PSI_AGE_FROM_INDEX](expressions.md#e-af3d20fc-fa3b-4485-bcee-8714e4acca9f)
7 | PMS_nAAV_AGE_RDI | (none) | [PMS_ancAGE_RDI_AGE_FROM_INDEX](expressions.md#e-193bb441-a7ab-412f-9d12-ab4247b78d6a)
8 | PMS_nAAV_AGE_SCI | (none) | [PMS_ancAGE_SCI_AGE_FROM_INDEX](expressions.md#e-2ef1c4f5-220d-45a3-860d-d073db59ef9e)
9 | PMS_nAAV_AGE_CCI | (none) | [PMS_ancAGE_CCI_AGE_FROM_INDEX](expressions.md#e-2dbc899c-4c91-45a0-bd93-e02b1456b995)
10 | PMS_nAAV_CND_IRI | (none) | [PMS_ancRES_IRI](expressions.md#e-1d4efdbd-03bf-4bc2-b189-da59dab901ae)
11 | PMS_nAAV_CND_PCRK | (none) | [PMS_ancRES_PCRK](expressions.md#e-0a1d81b8-b54b-490f-9238-9e8cc47b9f96)
12 | PMS_nAAV_CND_RUT | (none) | [PMS_ancCND_Rut](expressions.md#e-4f8cf211-5f31-4d5e-92dd-6f048cf7f6c6)
13 | PMS_nAAV_CND_RSL | (none) | [PMS_ancCND_RSL](expressions.md#e-7fbb09b7-c2ae-4497-8890-e69a5d3999b6)
14 | PMS_tDAV_Rehab_Type | (none) | [PMS_ancOBJ_ABS_Minor](expressions.md#e-8fa0a363-e9d0-4bc7-8324-822d97acb948)
15 | PMS_tDAV_Truck_Load | (none) | [PMS_ancTRF_Truck_Load](expressions.md#e-0a9b6cd0-79b4-4da2-a728-ab165b8fe547)
16 | PMS_nAAV_Yrly_Cost | (none) | [PMS_ancOBJ_AAV_Yrly_Cost_All](expressions.md#e-76d307ed-3427-462f-a79f-e16a387566dd)
17 | PMS_tAAV_FLT_GFP | (none) | [PMS_ancCND_FLT_GFP](expressions.md#e-8696dc20-6bf3-44d2-b7c8-d93b39ae6fc3)
18 | PMS_tAAV_IRI_GFP | (none) | [PMS_ancCND_IRI_GFP](expressions.md#e-ab06bc85-2e62-4269-aeda-d8bd7144b6ad)
19 | PMS_tAAV_PCRK_GFP | (none) | [PMS_ancCND_PCRK_GFP](expressions.md#e-40e28ca8-4605-426b-8c97-7b2c1cc92571)
20 | PMS_tAAV_RUT_GFP | (none) | [PMS_ancCND_RUT_GFP](expressions.md#e-04c76ab6-b287-4c9d-9399-90033e4cc5e7)
21 | PMS_tAAV_MAP21_GFP | (none) | [PMS_ancCND_MAP21_GFP](expressions.md#e-0452c4fb-af93-4324-bc0b-4576e857ae86)
22 | PMS_nDAV_CNT_CHIP_SEALS | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
23 | PMS_nDAV_CNT_MICROSURFACE | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
24 | PMS_tAAV_YEARLY_TREATMENT | (none) | [PMS_ancRES_Yearly_Treatment](expressions.md#e-ed2f1535-a24f-4156-8dbe-8b5e7dda5f7b)

### Costs

Order | Filter | Financial expression | Economic expression
---: | --- | --- | ---
0 | (none) | [PMS_ancCOST_County_Thin_Overlay](expressions.md#e-00f01427-122d-4794-b760-c616b79c8a00) | (none)

### Allowed subsequent treatments

Order | Treatment
---: | ---
1 | PMS_County_Chip_Seal
2 | PMS_County_MicroSurface
3 | PMS_County_Thick_Overlay
4 | PMS_County_Thin_Overlay
5 | PMS_PM_Crack_Seal
6 | PMS_PM_Cape_Seal
7 | PMS_PM_Ultra_Thin_Overlay
8 | PMS_Reconstruction
9 | PMS_PM_Asphalt
10 | PMS_Fair_Treatment_For_GFP_Analaysis_70P_Good

### Ancillary treatments

Order | Treatment
---: | ---

### Analysis-set membership

- DEL_STIP_2026_DISTRICT_001_Non_NHS; row `c602a0c3-47ac-422c-b0cd-0afe070c3cff`
- DEL_STIP_2026_DISTRICT_002_Non_NHS; row `23f234f3-d4ca-4b0c-b990-39ffb082522e`
- DEL_NonNHS_Routes; row `caacc8bf-bfbb-466a-bc0e-572a429ec4d3`
- DEL_STIP_2026_DISTRICT_004_Non_NHS; row `11311ab7-1fba-416c-9076-67bf8b5f908f`
- DEL_STIP_2026_DISTRICT_007_Non_NHS; row `920b0ab3-1419-440f-90cc-74f076689e36`
- DEL_STIP_2026_DISTRICT_009_Non_NHS; row `be8a622c-e1ce-4892-87b0-81f6e66d8a56`
- DEL_STIP_2026_DISTRICT_006_Non_NHS; row `be114a74-3c89-4333-9def-8ca040194a9a`
- DEL_STIP_2026_Non_NHS_ALL_NETWORK; row `fa15e418-3923-453d-8aed-9e49629a80cf`
- DEL_STIP_2026_DISTRICT_003_Non_NHS; row `e639b3cd-612f-4850-bd51-af58153f20f0`
- DEL_STIP_2026_DISTRICT_008_Non_NHS; row `c88abe4f-c75f-4948-84c3-b1cda906a226`
- DEL_STIP_2026_DISTRICT_005_Non_NHS; row `9d280fcf-4886-4af7-ad06-d78dea79f2df`
- DEL_STIP_2026_DISTRICT_010_Non_NHS; row `6444db29-b0d3-4d1e-83ec-f0f87685d00e`

Transitive configuration dependency closure: 903 records; query `audit_treatment_dependencies`.

## PMS_Fair_Treatment_For_GFP_Analaysis_70P_Good

PMS Interstate Treatment to move segments from fair to good

ID: `c3318fc6-2017-4d76-b1ec-3a0a515b546b`. Type: **Major**. IntervalYear: **0**. IsInitial: `1`. ApplyAfterInitial: `0`. Budget: **Rehabilition**.

### Trigger

[PMS_abfTRIG_Fair_Treatment_For_GFP_70P_Good](expressions.md#e-833ac796-64df-45c8-8802-30db1da8e5a7)

```text
GET_ANALVR(PMS_tAAV_MAP21_GFP) = 'FAIR'
```

### Ordered resets

Order | Variable | Filter | Reset expression
---: | --- | --- | ---
0 | PMS_nAAV_AGE_CSI | [PMS_abfOBJ_Concrete](expressions.md#e-ba469472-994d-4555-923b-c833047e7e8b) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
1 | PMS_nAAV_AGE_JCI | [PMS_abfOBJ_Concrete](expressions.md#e-ba469472-994d-4555-923b-c833047e7e8b) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
2 | PMS_nAAV_AGE_ECI | [PMS_abfOBJ_Asphalt](expressions.md#e-915f80f1-74d8-48c0-ab9f-fdffd05d547a) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
3 | PMS_nAAV_AGE_RDI | [PMS_abfOBJ_Asphalt](expressions.md#e-915f80f1-74d8-48c0-ab9f-fdffd05d547a) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
4 | PMS_nAAV_AGE_SCI | [PMS_abfOBJ_Asphalt](expressions.md#e-915f80f1-74d8-48c0-ab9f-fdffd05d547a) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
5 | PMS_nAAV_AGE_PSI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
6 | PMS_nAAV_AGE_CCI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
7 | PMS_nAAV_CND_CSI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
8 | PMS_nAAV_CND_JCI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
9 | PMS_nAAV_CND_ECI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
10 | PMS_nAAV_CND_RDI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
11 | PMS_nAAV_CND_SCI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
12 | PMS_nAAV_CND_PSI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
13 | PMS_nAAV_CND_CCI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
14 | PMS_nAAV_CND_IRI | (none) | [PMS_ancRES_IRI](expressions.md#e-1d4efdbd-03bf-4bc2-b189-da59dab901ae)
15 | PMS_nAAV_CND_PCRK | (none) | [PMS_ancRES_PCRK](expressions.md#e-0a1d81b8-b54b-490f-9238-9e8cc47b9f96)
16 | PMS_nAAV_CND_RUT | (none) | [PMS_ancCND_Rut](expressions.md#e-4f8cf211-5f31-4d5e-92dd-6f048cf7f6c6)
17 | PMS_nAAV_CND_RSL | (none) | [PMS_ancCND_RSL](expressions.md#e-7fbb09b7-c2ae-4497-8890-e69a5d3999b6)
18 | PMS_tDAV_Rehab_Type | (none) | [PMS_ancOBJ_ABS_Major](expressions.md#e-f5a30d2f-e3d8-4245-998f-1f9088ccbdc1)
19 | PMS_tDAV_Truck_Load | (none) | [PMS_ancTRF_Truck_Load](expressions.md#e-0a9b6cd0-79b4-4da2-a728-ab165b8fe547)
20 | PMS_nAAV_Yrly_Cost | (none) | [PMS_ancOBJ_AAV_Yrly_Cost_All](expressions.md#e-76d307ed-3427-462f-a79f-e16a387566dd)
21 | PMS_tAAV_FLT_GFP | (none) | [PMS_ancCND_FLT_GFP](expressions.md#e-8696dc20-6bf3-44d2-b7c8-d93b39ae6fc3)
22 | PMS_tAAV_IRI_GFP | (none) | [PMS_ancCND_IRI_GFP](expressions.md#e-ab06bc85-2e62-4269-aeda-d8bd7144b6ad)
23 | PMS_tAAV_PCRK_GFP | (none) | [PMS_ancCND_PCRK_GFP](expressions.md#e-40e28ca8-4605-426b-8c97-7b2c1cc92571)
24 | PMS_tAAV_RUT_GFP | (none) | [PMS_ancCND_RUT_GFP](expressions.md#e-04c76ab6-b287-4c9d-9399-90033e4cc5e7)
25 | PMS_tAAV_MAP21_GFP | (none) | [PMS_ancCND_MAP21_GFP](expressions.md#e-0452c4fb-af93-4324-bc0b-4576e857ae86)
26 | PMS_nDAV_CNT_CHIP_SEALS | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
27 | PMS_nDAV_CNT_MICROSURFACE | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
28 | PMS_tAAV_YEARLY_TREATMENT | (none) | [PMS_ancRES_Yearly_Treatment](expressions.md#e-ed2f1535-a24f-4156-8dbe-8b5e7dda5f7b)

### Costs

Order | Filter | Financial expression | Economic expression
---: | --- | --- | ---
0 | (none) | [PMS_ancCOST_Fair_Treatment_For_GFP_70P_Good](expressions.md#e-da0f020d-59d5-4245-bff5-ea7af562224f) | (none)

### Allowed subsequent treatments

Order | Treatment
---: | ---
1 | PMS_Fair_Treatment_For_GFP_Analaysis_70P_Good

### Ancillary treatments

Order | Treatment
---: | ---

### Analysis-set membership

- DEL_STIP_2026_INTERSTATES_ONLY; row `6bdac94e-9528-4a85-9e2d-4359e5039789`
- DEL_STIP_2026_NHS_ONLY_NO_INTERSTATE; row `af93030c-2db0-4865-8125-6c16a68acdf0`
- PMS_TURNPIKE; row `5a14305b-b7dd-4a2c-a654-9be6bfefd09d`
- DEL_STIP_2026_Non_NHS_ALL_NETWORK; row `e038b9d2-1560-449a-8c0c-9c8a44e11a13`

Transitive configuration dependency closure: 463 records; query `audit_treatment_dependencies`.

## PMS_Major_CPR_Diamond_Grind

Major Concrete Pavement Restoration plus Diamond Grinding

ID: `76157e12-3ac3-442e-b1dc-a49f4e159659`. Type: **Major**. IntervalYear: **6**. IsInitial: `1`. ApplyAfterInitial: `0`. Budget: **Rehabilition**.

### Trigger

[PMS_abfTRIG_Conc_Pvmt_Repair_Major](expressions.md#e-c7b6c5b3-3bbb-47a1-b07a-ce931ae48f32)

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

### Ordered resets

Order | Variable | Filter | Reset expression
---: | --- | --- | ---
0 | PMS_nAAV_AGE_JCI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
1 | PMS_nAAV_AGE_CSI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
2 | PMS_nAAV_AGE_PSI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
3 | PMS_nAAV_AGE_CCI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
4 | PMS_nAAV_CND_CSI | (none) | [PMS_ancOBJ_ABS_4_5_CSI](expressions.md#e-70de9024-06fd-424d-b31f-63a89bd17f0a)
5 | PMS_nAAV_CND_JCI | (none) | [PMS_ancOBJ_ABS_4_5_JCI](expressions.md#e-cdcff07f-7572-4870-b91d-a632deeca3f4)
6 | PMS_nAAV_CND_PSI | (none) | [PMS_ancOBJ_ABS_4_5_PSI](expressions.md#e-cf97cde2-65f1-41b2-a110-664314d91e08)
7 | PMS_nAAV_CND_CCI | (none) | [PMS_ancOBJ_ABS_4_5_CCI](expressions.md#e-6aa8fc26-24d2-4ddf-bf53-ea80f0bd69ae)
8 | PMS_nAAV_CND_IRI | (none) | [PMS_ancRES_IRI](expressions.md#e-1d4efdbd-03bf-4bc2-b189-da59dab901ae)
9 | PMS_nAAV_CND_PCRK | (none) | [PMS_ancRES_PCRK](expressions.md#e-0a1d81b8-b54b-490f-9238-9e8cc47b9f96)
10 | PMS_nAAV_CND_FLT | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
11 | PMS_nAAV_CND_RSL | (none) | [PMS_ancCND_RSL](expressions.md#e-7fbb09b7-c2ae-4497-8890-e69a5d3999b6)
12 | PMS_tDAV_Rehab_Type | (none) | [PMS_ancOBJ_ABS_Minor](expressions.md#e-8fa0a363-e9d0-4bc7-8324-822d97acb948)
13 | PMS_tDAV_Truck_Load | (none) | [PMS_ancTRF_Truck_Load](expressions.md#e-0a9b6cd0-79b4-4da2-a728-ab165b8fe547)
14 | PMS_nAAV_Yrly_Cost | (none) | [PMS_ancOBJ_AAV_Yrly_Cost_All](expressions.md#e-76d307ed-3427-462f-a79f-e16a387566dd)
15 | PMS_tAAV_FLT_GFP | (none) | [PMS_ancCND_FLT_GFP](expressions.md#e-8696dc20-6bf3-44d2-b7c8-d93b39ae6fc3)
16 | PMS_tAAV_IRI_GFP | (none) | [PMS_ancCND_IRI_GFP](expressions.md#e-ab06bc85-2e62-4269-aeda-d8bd7144b6ad)
17 | PMS_tAAV_PCRK_GFP | (none) | [PMS_ancCND_PCRK_GFP](expressions.md#e-40e28ca8-4605-426b-8c97-7b2c1cc92571)
18 | PMS_tAAV_RUT_GFP | (none) | [PMS_ancCND_RUT_GFP](expressions.md#e-04c76ab6-b287-4c9d-9399-90033e4cc5e7)
19 | PMS_tAAV_MAP21_GFP | (none) | [PMS_ancCND_MAP21_GFP](expressions.md#e-0452c4fb-af93-4324-bc0b-4576e857ae86)
20 | PMS_tAAV_YEARLY_TREATMENT | (none) | [PMS_ancRES_Yearly_Treatment](expressions.md#e-ed2f1535-a24f-4156-8dbe-8b5e7dda5f7b)

### Costs

Order | Filter | Financial expression | Economic expression
---: | --- | --- | ---
0 | (none) | [PMS_ancCOST_Conc_Pvmt_Repair_Major](expressions.md#e-2f1da24d-f199-4103-8e08-6c81d7c9c5c4) | (none)

### Allowed subsequent treatments

Order | Treatment
---: | ---
1 | PMS_PM_Saw_Seal_Joints
2 | PMS_Thin_Overlay
3 | PMS_Thick_Overlay
4 | PMS_Reconstruction
5 | PMS_Major_CPR_Diamond_Grind
6 | PMS_Minor_CPR_Diamond_Grind

### Ancillary treatments

Order | Treatment
---: | ---

### Analysis-set membership

- DEL_STIP_2026_Non_NHS_ALL_NETWORK; row `e4c41a5e-5df2-481d-8a76-073b111837a3`
- DEL_STIP_2026_DISTRICT_005_Non_NHS; row `24af41fe-306d-4182-8e69-08796166a191`
- DEL_STIP_2026_DISTRICT_004_Non_NHS; row `a18bc7ce-0dcb-4d63-9c3c-08a03c85c858`
- DEL_INTERSTATES_2023_10_YEARS; row `ae24c656-164b-40ba-8958-0d05565c4e12`
- PMS_APD; row `7147c1d8-1743-418a-8844-0d4071ac34bc`
- DEL_NonNHS_Routes; row `cda36c93-be63-4223-b3cc-0fca4f3a945c`
- DEL_STIP_2026_DISTRICT_003_Non_NHS; row `f6571fb9-24fc-43c5-84b1-1d2b343aeea9`
- DEL_STIP_2026_DISTRICT_004_NHS_ONLY; row `73bce459-54f4-40bd-a5aa-37ec8f3c6eb6`
- DEL_STIP_2026_DISTRICT_001_Non_NHS; row `3b9cd5ac-a3c0-4e09-9460-6f053406a527`
- DEL_STIP_2026_DISTRICT_010_NHS_ONLY; row `759dd395-c005-4144-952c-704eee235314`
- PMS_NHS; row `86b24ed3-427d-45c3-93ca-859baed2eb62`
- DEL_STIP_2026_NHS_ONLY_NO_INTERSTATE; row `c160b48c-49bb-4339-89b7-8befe319666b`
- DEL_APD_NO_I68_OR_OTHERS_USING_RIDICULOUS_PRICES; row `9b32cbbb-2251-4a4e-9ec1-9b0382b9236d`
- PMS_TURNPIKE; row `ebe08d26-1877-4257-bc1f-a3d7d2dd3edb`
- PMS_NON_NHS_NON_TURNPIKE; row `7f1b0804-6b5d-412e-822b-a548ebe8e5aa`
- DEL_STIP_2026_DISTRICT_009_Non_NHS; row `df7f5099-f510-452b-8387-a5be87bb91ab`
- DEL_STIP_2026_DISTRICT_001_NHS_ONLY; row `d2646ac0-f90b-4f6f-82e7-aef1d439ce56`
- DEL_STIP_2026_DISTRICT_002_Non_NHS; row `8cd310c7-bcc7-4ce9-a41f-b31634f2b095`
- DEL_STIP_2026_DISTRICT_003_NHS_ONLY; row `b25f3c8b-371f-499c-96ae-b3b41cb4031c`
- PMS_INTERSTATE; row `260896c1-5d6d-4197-83e0-b76fba15c5d2`
- PMS_NHS_TENTH; row `a5e03ae5-0173-477a-8c0c-b7c08c6f26fc`
- DEL_STIP_2026_DISTRICT_008_NHS_ONLY; row `d601d778-cded-4a59-b80f-b847b241ec13`
- DEL_STIP_2026_DISTRICT_006_NHS_ONLY; row `a63905dc-facb-4372-8959-cfe310da6a98`
- DEL_STIP_2026_DISTRICT_010_Non_NHS; row `68979c11-52a8-40b3-b961-d0a60e82d363`
- DEL_STIP_2026_DISTRICT_008_Non_NHS; row `ff0583fb-aa40-4976-bf5e-d307dad0738e`
- DEL_STIP_2026_DISTRICT_002_NHS_ONLY; row `4100be52-8a6f-457a-bcb8-e14b20e0dc23`
- DEL_STIP_2026_DISTRICT_005_NHS_ONLY; row `07cc0399-a931-46fe-a7d8-e6f32d3761b0`
- DEL_STIP_2026_DISTRICT_007_Non_NHS; row `b462ffc6-c041-4a50-8e9e-ebdc08751a04`
- DEL_STIP_2026_INTERSTATES_ONLY; row `723099c2-a99a-4cf4-a08b-ee6cdc82b6cc`
- DEL_STIP_2026_DISTRICT_009_NHS_ONLY; row `6ba79e1c-24a6-4f0c-b967-f35aa1df3b11`
- DEL_STIP_2026_DISTRICT_006_Non_NHS; row `a024866e-84fb-4eba-ad36-f96d90ba8b85`
- DEL_STIP_2026_DISTRICT_007_NHS_ONLY; row `e70d981f-bca6-41df-b950-fdc7e0d1f4dc`

Transitive configuration dependency closure: 1221 records; query `audit_treatment_dependencies`.

## PMS_Minor_CPR_Diamond_Grind

Minor Concrete Pavement Restoration plus Diamond Grinding

ID: `da5e1d05-7601-4dfb-9149-8d917883afc5`. Type: **Major**. IntervalYear: **6**. IsInitial: `1`. ApplyAfterInitial: `0`. Budget: **Rehabilition**.

### Trigger

[PMS_abfTRIG_Conc_Pvmt_Repair_Minor](expressions.md#e-f80971b8-1efc-4734-8090-d0e5faea14ff)

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

### Ordered resets

Order | Variable | Filter | Reset expression
---: | --- | --- | ---
0 | PMS_nAAV_AGE_JCI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
1 | PMS_nAAV_AGE_CSI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
2 | PMS_nAAV_AGE_PSI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
3 | PMS_nAAV_AGE_CCI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
4 | PMS_nAAV_CND_CSI | (none) | [PMS_ancOBJ_ABS_4_5_CSI](expressions.md#e-70de9024-06fd-424d-b31f-63a89bd17f0a)
5 | PMS_nAAV_CND_JCI | (none) | [PMS_ancOBJ_ABS_4_5_JCI](expressions.md#e-cdcff07f-7572-4870-b91d-a632deeca3f4)
6 | PMS_nAAV_CND_PSI | (none) | [PMS_ancOBJ_ABS_4_5_PSI](expressions.md#e-cf97cde2-65f1-41b2-a110-664314d91e08)
7 | PMS_nAAV_CND_CCI | (none) | [PMS_ancOBJ_ABS_4_5_CCI](expressions.md#e-6aa8fc26-24d2-4ddf-bf53-ea80f0bd69ae)
8 | PMS_nAAV_CND_IRI | (none) | [PMS_ancRES_IRI](expressions.md#e-1d4efdbd-03bf-4bc2-b189-da59dab901ae)
9 | PMS_nAAV_CND_PCRK | (none) | [PMS_ancRES_PCRK](expressions.md#e-0a1d81b8-b54b-490f-9238-9e8cc47b9f96)
10 | PMS_nAAV_CND_FLT | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
11 | PMS_nAAV_CND_RSL | (none) | [PMS_ancCND_RSL](expressions.md#e-7fbb09b7-c2ae-4497-8890-e69a5d3999b6)
12 | PMS_tDAV_Rehab_Type | (none) | [PMS_ancOBJ_ABS_Minor](expressions.md#e-8fa0a363-e9d0-4bc7-8324-822d97acb948)
13 | PMS_tDAV_Truck_Load | (none) | [PMS_ancTRF_Truck_Load](expressions.md#e-0a9b6cd0-79b4-4da2-a728-ab165b8fe547)
14 | PMS_nAAV_Yrly_Cost | (none) | [PMS_ancOBJ_AAV_Yrly_Cost_All](expressions.md#e-76d307ed-3427-462f-a79f-e16a387566dd)
15 | PMS_tAAV_FLT_GFP | (none) | [PMS_ancCND_FLT_GFP](expressions.md#e-8696dc20-6bf3-44d2-b7c8-d93b39ae6fc3)
16 | PMS_tAAV_IRI_GFP | (none) | [PMS_ancCND_IRI_GFP](expressions.md#e-ab06bc85-2e62-4269-aeda-d8bd7144b6ad)
17 | PMS_tAAV_PCRK_GFP | (none) | [PMS_ancCND_PCRK_GFP](expressions.md#e-40e28ca8-4605-426b-8c97-7b2c1cc92571)
18 | PMS_tAAV_RUT_GFP | (none) | [PMS_ancCND_RUT_GFP](expressions.md#e-04c76ab6-b287-4c9d-9399-90033e4cc5e7)
19 | PMS_tAAV_MAP21_GFP | (none) | [PMS_ancCND_MAP21_GFP](expressions.md#e-0452c4fb-af93-4324-bc0b-4576e857ae86)
20 | PMS_tAAV_YEARLY_TREATMENT | (none) | [PMS_ancRES_Yearly_Treatment](expressions.md#e-ed2f1535-a24f-4156-8dbe-8b5e7dda5f7b)

### Costs

Order | Filter | Financial expression | Economic expression
---: | --- | --- | ---
0 | (none) | [PMS_ancCOST_Conc_Pvmt_Repair_Minor](expressions.md#e-02562651-f8d5-49fb-a565-d6a66b98fe87) | (none)

### Allowed subsequent treatments

Order | Treatment
---: | ---
1 | PMS_Major_CPR_Diamond_Grind
2 | PMS_PM_Saw_Seal_Joints
3 | PMS_Thin_Overlay
4 | PMS_Thick_Overlay
5 | PMS_Reconstruction
6 | PMS_Minor_CPR_Diamond_Grind

### Ancillary treatments

Order | Treatment
---: | ---

### Analysis-set membership

- DEL_NonNHS_Routes; row `88cd4be4-169a-443c-9df2-06e7e7b0c81b`
- DEL_STIP_2026_DISTRICT_001_Non_NHS; row `76603e34-2a65-4f36-8e8c-0d7fa39f12e6`
- DEL_STIP_2026_DISTRICT_010_Non_NHS; row `fda02c0b-0e60-4052-b1ac-2dcd2d612938`
- PMS_NHS; row `3e321239-5ff7-4c40-ada6-2f96d404a310`
- DEL_STIP_2026_DISTRICT_002_Non_NHS; row `b93ed60a-38a7-48fe-ac5e-32109e422b36`
- PMS_TURNPIKE; row `dcafaa8b-ae1b-4273-a006-38f8f2223e40`
- DEL_STIP_2026_INTERSTATES_ONLY; row `7df8b6e8-bfe4-47f8-a87d-46114c562a67`
- PMS_INTERSTATE; row `a4ba34f9-a601-4271-9ecc-48ed6bb778c6`
- DEL_STIP_2026_DISTRICT_005_Non_NHS; row `de5ac9f7-2ccf-485f-b308-5a8d93e27298`
- DEL_STIP_2026_DISTRICT_005_NHS_ONLY; row `55799bad-e852-4b15-832a-70bde7a29aef`
- PMS_APD; row `c15be10f-46e1-4043-8937-7a9d2784517e`
- DEL_STIP_2026_DISTRICT_008_NHS_ONLY; row `2b8734a2-8ba9-47df-aea6-8df53cda7a26`
- DEL_STIP_2026_DISTRICT_001_NHS_ONLY; row `b64cba38-f490-46ae-9f95-962bfaea1556`
- DEL_STIP_2026_Non_NHS_ALL_NETWORK; row `2a7bdd27-4a1c-4ae5-aa9e-99e42c0736a6`
- DEL_STIP_2026_DISTRICT_009_NHS_ONLY; row `81193369-88a4-4b31-8e21-9b1953fd24fc`
- PMS_NHS_TENTH; row `2b242a40-6dfe-4f93-bb1f-a394571c96bf`
- DEL_STIP_2026_DISTRICT_008_Non_NHS; row `d4e2e517-86ec-4116-b3a4-a4b21ddbbcaf`
- DEL_STIP_2026_DISTRICT_009_Non_NHS; row `1cf77598-883f-458a-8889-a714b29c131c`
- DEL_STIP_2026_NHS_ONLY_NO_INTERSTATE; row `192b341e-9b8b-40f5-905a-b591a852b949`
- DEL_STIP_2026_DISTRICT_003_NHS_ONLY; row `5428d554-4f00-483c-ae06-b65091b4b0ff`
- DEL_STIP_2026_DISTRICT_007_NHS_ONLY; row `abca7e9a-da8b-4e8a-bec0-c428e326ebbe`
- PMS_NON_NHS_NON_TURNPIKE; row `e8854d72-a031-41b6-a141-c4cb4fa3cea3`
- DEL_STIP_2026_DISTRICT_006_NHS_ONLY; row `b0a2681b-12a5-4802-ae6e-ca3a350ea76d`
- DEL_INTERSTATES_2023_10_YEARS; row `11840e20-2c64-4c45-a01d-d13de095b684`
- DEL_STIP_2026_DISTRICT_004_Non_NHS; row `cc75850a-4093-466f-998f-d62c952b2c13`
- DEL_STIP_2026_DISTRICT_006_Non_NHS; row `81eaf0ee-b838-48d5-876b-d70ec73dffbe`
- DEL_STIP_2026_DISTRICT_007_Non_NHS; row `9be77e0e-e47b-4f8b-b3ae-df49c8ed1b9b`
- DEL_STIP_2026_DISTRICT_004_NHS_ONLY; row `378a8586-9d85-4523-9f4e-e8f04f35457b`
- DEL_STIP_2026_DISTRICT_010_NHS_ONLY; row `79bf719d-8ff9-46ea-8044-f04da87a03b9`
- DEL_APD_NO_I68_OR_OTHERS_USING_RIDICULOUS_PRICES; row `f146acd8-9b6e-4953-b5c4-f877076bf4fe`
- DEL_STIP_2026_DISTRICT_003_Non_NHS; row `5eb3faf4-74da-4a42-9b1f-fa61811c678f`
- DEL_STIP_2026_DISTRICT_002_NHS_ONLY; row `682a2818-6063-40f9-9687-fbed8be0056c`

Transitive configuration dependency closure: 1221 records; query `audit_treatment_dependencies`.

## PMS_PM_Asphalt

Preventative Maintenance on Asphalt

ID: `7432a91d-2890-4de1-b094-d1874616dd05`. Type: **Major**. IntervalYear: **0**. IsInitial: `1`. ApplyAfterInitial: `0`. Budget: **Rehabilition**.

### Trigger

[PMS_abfOBJ_False](expressions.md#e-b3fe6710-ecd4-46aa-ae5c-4696685576bf)

```text
FALSE
```

### Ordered resets

Order | Variable | Filter | Reset expression
---: | --- | --- | ---
0 | PMS_nAAV_CND_CCI | (none) | [PMS_ancCND_CCI_Annual](expressions.md#e-94dffbab-78c7-49ea-8e1c-83b282ff8d7e)
1 | PMS_tDAV_Rehab_Type | (none) | [PMS_ancOBJ_ABS_Minor](expressions.md#e-8fa0a363-e9d0-4bc7-8324-822d97acb948)
2 | PMS_tDAV_Truck_Load | (none) | [PMS_ancTRF_Truck_Load](expressions.md#e-0a9b6cd0-79b4-4da2-a728-ab165b8fe547)
3 | PMS_nAAV_Yrly_Cost | (none) | [PMS_ancOBJ_AAV_Yrly_Cost_All](expressions.md#e-76d307ed-3427-462f-a79f-e16a387566dd)
4 | PMS_tAAV_YEARLY_TREATMENT | (none) | [PMS_ancRES_Yearly_Treatment](expressions.md#e-ed2f1535-a24f-4156-8dbe-8b5e7dda5f7b)

### Costs

Order | Filter | Financial expression | Economic expression
---: | --- | --- | ---
0 | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3) | (none)

### Allowed subsequent treatments

Order | Treatment
---: | ---
1 | PMS_PM_Asphalt
2 | PMS_Thin_Overlay
3 | PMS_Thick_Overlay
4 | PMS_Reconstruction
5 | PMS_PM_Microsurfacing

### Ancillary treatments

Order | Treatment
---: | ---

### Analysis-set membership

- DEL_INTERSTATES_2023_10_YEARS; row `10bf5db3-7f69-4385-9601-7875739573dc`
- PMS_INTERSTATE; row `c0f65fb4-6f74-44c5-9356-8be00cd09587`
- PMS_TURNPIKE; row `23387fee-d875-4d3f-8e2a-b6af129bffdb`
- DEL_STIP_2026_INTERSTATES_ONLY; row `92bf0a2d-f436-480a-a2bd-e199cdb28aac`
- DEL_STIP_2026_Non_NHS_ALL_NETWORK; row `24286ac3-9590-472a-a494-f2e23db80aaf`
- PMS_APD; row `da981862-de8b-4bd5-960e-f8823a413ad2`
- DEL_APD_NO_I68_OR_OTHERS_USING_RIDICULOUS_PRICES; row `a3dc58be-03e9-4573-bf6b-fbf52312ffe7`
- DEL_STIP_2026_NHS_ONLY_NO_INTERSTATE; row `2ead0adf-26ed-474e-bdfa-fe7a356a3b4c`

Transitive configuration dependency closure: 376 records; query `audit_treatment_dependencies`.

## PMS_PM_Cape_Seal

Cape Seal

ID: `a7a1f76b-e693-4bc9-8bed-81c47682bd7d`. Type: **Major**. IntervalYear: **3**. IsInitial: `1`. ApplyAfterInitial: `0`. Budget: **Rehabilition**.

### Trigger

[PMS_abfTRIG_PM_Cape_Seal](expressions.md#e-7f35547c-7da4-4935-b6ca-075c0f150b4d)

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

### Ordered resets

Order | Variable | Filter | Reset expression
---: | --- | --- | ---
0 | PMS_nAAV_CND_ECI | (none) | [PMS_ancRES_ECI_CAPE_SEAL](expressions.md#e-d6cb9764-7364-4260-9f45-a7ccc543062b)
1 | PMS_nAAV_CND_SCI | (none) | [PMS_ancRES_SCI_CAPE_SEAL](expressions.md#e-91a5cbc0-4225-4276-b716-5cde0295c79e)
2 | PMS_nAAV_CND_CCI | (none) | [PMS_ancRES_CCI_CAPE_SEAL](expressions.md#e-399a9171-0c43-4440-95ad-64f491cbd646)
3 | PMS_nAAV_AGE_ECI | (none) | [PMS_ancAGE_ECI_AGE_FROM_INDEX](expressions.md#e-a98afc4d-071a-4fc7-86ef-7840afcd83e8)
4 | PMS_nAAV_AGE_SCI | (none) | [PMS_ancAGE_SCI_AGE_FROM_INDEX](expressions.md#e-2ef1c4f5-220d-45a3-860d-d073db59ef9e)
5 | PMS_nAAV_AGE_CCI | (none) | [PMS_ancAGE_CCI_AGE_FROM_INDEX](expressions.md#e-2dbc899c-4c91-45a0-bd93-e02b1456b995)
6 | PMS_nAAV_CND_PCRK | (none) | [PMS_ancRES_PCRK](expressions.md#e-0a1d81b8-b54b-490f-9238-9e8cc47b9f96)
7 | PMS_nAAV_CND_RSL | (none) | [PMS_ancCND_RSL](expressions.md#e-7fbb09b7-c2ae-4497-8890-e69a5d3999b6)
8 | PMS_tDAV_Rehab_Type | (none) | [PMS_ancOBJ_ABS_Minor](expressions.md#e-8fa0a363-e9d0-4bc7-8324-822d97acb948)
9 | PMS_tDAV_Truck_Load | (none) | [PMS_ancTRF_Truck_Load](expressions.md#e-0a9b6cd0-79b4-4da2-a728-ab165b8fe547)
10 | PMS_nAAV_Yrly_Cost | (none) | [PMS_ancOBJ_AAV_Yrly_Cost_All](expressions.md#e-76d307ed-3427-462f-a79f-e16a387566dd)
11 | PMS_tAAV_FLT_GFP | (none) | [PMS_ancCND_FLT_GFP](expressions.md#e-8696dc20-6bf3-44d2-b7c8-d93b39ae6fc3)
12 | PMS_tAAV_IRI_GFP | (none) | [PMS_ancCND_IRI_GFP](expressions.md#e-ab06bc85-2e62-4269-aeda-d8bd7144b6ad)
13 | PMS_tAAV_PCRK_GFP | (none) | [PMS_ancCND_PCRK_GFP](expressions.md#e-40e28ca8-4605-426b-8c97-7b2c1cc92571)
14 | PMS_tAAV_RUT_GFP | (none) | [PMS_ancCND_RUT_GFP](expressions.md#e-04c76ab6-b287-4c9d-9399-90033e4cc5e7)
15 | PMS_tAAV_MAP21_GFP | (none) | [PMS_ancCND_MAP21_GFP](expressions.md#e-0452c4fb-af93-4324-bc0b-4576e857ae86)
16 | PMS_nDAV_CNT_CHIP_SEALS | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
17 | PMS_nDAV_CNT_MICROSURFACE | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
18 | PMS_tAAV_YEARLY_TREATMENT | (none) | [PMS_ancRES_Yearly_Treatment](expressions.md#e-ed2f1535-a24f-4156-8dbe-8b5e7dda5f7b)

### Costs

Order | Filter | Financial expression | Economic expression
---: | --- | --- | ---
0 | (none) | [PMS_ancCOST_PM_Cape_Seal](expressions.md#e-5026ac2d-f5ac-421f-a1fd-edc893c79287) | (none)

### Allowed subsequent treatments

Order | Treatment
---: | ---
1 | PMS_PM_Crack_Seal
2 | PMS_PM_Chip_Seal
3 | PMS_PM_Cape_Seal
4 | PMS_PM_Microsurfacing
5 | PMS_PM_Ultra_Thin_Overlay
6 | PMS_Thin_Overlay
7 | PMS_Thick_Overlay
8 | PMS_Reconstruction

### Ancillary treatments

Order | Treatment
---: | ---

### Analysis-set membership

- DEL_STIP_2026_INTERSTATES_ONLY; row `be2a5304-b667-4e21-870c-94f5f1201c13`
- PMS_TURNPIKE; row `f7302c07-d960-47a3-831e-9a75430ea0c2`
- PMS_APD; row `6dd7a07f-0841-4cbc-8df6-9c2e8d72f99b`
- DEL_APD_NO_I68_OR_OTHERS_USING_RIDICULOUS_PRICES; row `85d4ac33-b8c7-473b-97a8-a609353075c3`
- PMS_NHS_TENTH; row `db480411-75a7-464a-b46f-a85ab90f7f5e`
- PMS_INTERSTATE; row `d2318801-d9d9-40f2-aefd-c274e102df10`
- DEL_INTERSTATES_2023_10_YEARS; row `339372cd-bc2a-47fd-9b65-f14a93201fe5`

Transitive configuration dependency closure: 985 records; query `audit_treatment_dependencies`.

## PMS_PM_Chip_Seal

Chip Seal

ID: `0ad8480b-f973-4b7b-b148-8dfc48ef06c4`. Type: **Major**. IntervalYear: **3**. IsInitial: `1`. ApplyAfterInitial: `0`. Budget: **Rehabilition**.

### Trigger

[PMS_abfTRIG_PM_Chip_Seal](expressions.md#e-b65f9808-6dea-411a-a508-ce89f87250bf)

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

### Ordered resets

Order | Variable | Filter | Reset expression
---: | --- | --- | ---
0 | PMS_nAAV_CND_ECI | (none) | [PMS_ancRES_ECI_CHIP_SEAL](expressions.md#e-fa36e4d4-2f5d-4372-b223-f083929bb4b0)
1 | PMS_nAAV_CND_SCI | (none) | [PMS_ancRES_SCI_CHIP_SEAL](expressions.md#e-22a19aac-e4c6-40e0-849a-afc86dc092fc)
2 | PMS_nAAV_CND_CCI | (none) | [PMS_ancRES_CCI_CHIP_SEAL](expressions.md#e-acb4e2c4-97bf-4f5e-9b94-908560724028)
3 | PMS_nAAV_AGE_ECI | (none) | [PMS_ancAGE_ECI_AGE_FROM_INDEX](expressions.md#e-a98afc4d-071a-4fc7-86ef-7840afcd83e8)
4 | PMS_nAAV_AGE_SCI | (none) | [PMS_ancAGE_SCI_AGE_FROM_INDEX](expressions.md#e-2ef1c4f5-220d-45a3-860d-d073db59ef9e)
5 | PMS_nAAV_AGE_CCI | (none) | [PMS_ancAGE_CCI_AGE_FROM_INDEX](expressions.md#e-2dbc899c-4c91-45a0-bd93-e02b1456b995)
6 | PMS_nAAV_CND_PCRK | (none) | [PMS_ancRES_PCRK](expressions.md#e-0a1d81b8-b54b-490f-9238-9e8cc47b9f96)
7 | PMS_nAAV_CND_RSL | (none) | [PMS_ancCND_RSL](expressions.md#e-7fbb09b7-c2ae-4497-8890-e69a5d3999b6)
8 | PMS_tDAV_Rehab_Type | (none) | [PMS_ancOBJ_ABS_Minor](expressions.md#e-8fa0a363-e9d0-4bc7-8324-822d97acb948)
9 | PMS_tDAV_Truck_Load | (none) | [PMS_ancTRF_Truck_Load](expressions.md#e-0a9b6cd0-79b4-4da2-a728-ab165b8fe547)
10 | PMS_nAAV_Yrly_Cost | (none) | [PMS_ancOBJ_AAV_Yrly_Cost_All](expressions.md#e-76d307ed-3427-462f-a79f-e16a387566dd)
11 | PMS_nDAV_CNT_MICROSURFACE | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
12 | PMS_tAAV_FLT_GFP | (none) | [PMS_ancCND_FLT_GFP](expressions.md#e-8696dc20-6bf3-44d2-b7c8-d93b39ae6fc3)
13 | PMS_tAAV_IRI_GFP | (none) | [PMS_ancCND_IRI_GFP](expressions.md#e-ab06bc85-2e62-4269-aeda-d8bd7144b6ad)
14 | PMS_tAAV_PCRK_GFP | (none) | [PMS_ancCND_PCRK_GFP](expressions.md#e-40e28ca8-4605-426b-8c97-7b2c1cc92571)
15 | PMS_tAAV_RUT_GFP | (none) | [PMS_ancCND_RUT_GFP](expressions.md#e-04c76ab6-b287-4c9d-9399-90033e4cc5e7)
16 | PMS_tAAV_MAP21_GFP | (none) | [PMS_ancCND_MAP21_GFP](expressions.md#e-0452c4fb-af93-4324-bc0b-4576e857ae86)
17 | PMS_nDAV_CNT_CHIP_SEALS | (none) | [PMS_ancRES_CNT_CHIP_SEAL](expressions.md#e-455714c1-bc1f-4743-a66e-1e1d92bee2cc)
18 | PMS_tAAV_YEARLY_TREATMENT | (none) | [PMS_ancRES_Yearly_Treatment](expressions.md#e-ed2f1535-a24f-4156-8dbe-8b5e7dda5f7b)

### Costs

Order | Filter | Financial expression | Economic expression
---: | --- | --- | ---
0 | (none) | [PMS_ancCOST_PM_Chip_Seal](expressions.md#e-4acfa0b2-0b40-4134-9fcd-21883b8c1c3c) | (none)

### Allowed subsequent treatments

Order | Treatment
---: | ---
1 | PMS_PM_Chip_Seal
2 | PMS_PM_Crack_Seal
3 | PMS_PM_Cape_Seal
4 | PMS_PM_Microsurfacing
5 | PMS_PM_Ultra_Thin_Overlay
6 | PMS_Thin_Overlay
7 | PMS_Thick_Overlay
8 | PMS_Reconstruction

### Ancillary treatments

Order | Treatment
---: | ---

### Analysis-set membership

- PMS_TURNPIKE; row `35ee2cf2-ba91-48c9-9ffa-1b7d19069edd`
- PMS_NHS_TENTH; row `12815f72-dd86-44ba-9a89-412956eae05d`
- PMS_INTERSTATE; row `6616304c-450f-4b58-a8ab-78c5ca5c3c9e`
- PMS_APD; row `31438113-1a1f-48f2-9a0f-be12e9378669`

Transitive configuration dependency closure: 974 records; query `audit_treatment_dependencies`.

## PMS_PM_Concrete

Preventative Maintenance on Concrete

ID: `caa01989-77c5-4d2c-ba89-fb43864de8b1`. Type: **Major**. IntervalYear: **5**. IsInitial: `1`. ApplyAfterInitial: `0`. Budget: **Rehabilition**.

### Trigger

[PMS_abfOBJ_False](expressions.md#e-b3fe6710-ecd4-46aa-ae5c-4696685576bf)

```text
FALSE
```

### Ordered resets

Order | Variable | Filter | Reset expression
---: | --- | --- | ---
0 | PMS_nAAV_CND_CCI | (none) | [PMS_ancCND_CCI_Annual](expressions.md#e-94dffbab-78c7-49ea-8e1c-83b282ff8d7e)
1 | PMS_tDAV_Rehab_Type | (none) | [PMS_ancOBJ_ABS_Minor](expressions.md#e-8fa0a363-e9d0-4bc7-8324-822d97acb948)
2 | PMS_tDAV_Truck_Load | (none) | [PMS_ancTRF_Truck_Load](expressions.md#e-0a9b6cd0-79b4-4da2-a728-ab165b8fe547)
3 | PMS_nAAV_Yrly_Cost | (none) | [PMS_ancOBJ_AAV_Yrly_Cost_All](expressions.md#e-76d307ed-3427-462f-a79f-e16a387566dd)
4 | PMS_tAAV_YEARLY_TREATMENT | (none) | [PMS_ancRES_Yearly_Treatment](expressions.md#e-ed2f1535-a24f-4156-8dbe-8b5e7dda5f7b)

### Costs

Order | Filter | Financial expression | Economic expression
---: | --- | --- | ---
0 | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3) | (none)

### Allowed subsequent treatments

Order | Treatment
---: | ---
1 | PMS_PM_Concrete
2 | PMS_Reconstruction
3 | PMS_Major_CPR_Diamond_Grind
4 | PMS_Minor_CPR_Diamond_Grind
5 | PMS_PM_Saw_Seal_Joints

### Ancillary treatments

Order | Treatment
---: | ---

### Analysis-set membership

- PMS_TURNPIKE; row `bb3dfb2e-136f-4616-b63d-2fbf6784dfc4`
- DEL_INTERSTATES_2023_10_YEARS; row `e04c0f75-824d-4d73-b898-3f16d45c80cd`
- DEL_APD_NO_I68_OR_OTHERS_USING_RIDICULOUS_PRICES; row `66fb88b9-630f-4b98-9bf4-7eba68456cd2`
- PMS_APD; row `1275da41-d5b2-4c20-b4f2-d6672c15ac42`
- PMS_INTERSTATE; row `ab9f1980-edca-4d22-b5f6-e1e6a6a1effd`

Transitive configuration dependency closure: 355 records; query `audit_treatment_dependencies`.

## PMS_PM_Crack_Seal

Crack Seal

ID: `c1ff7f9a-954f-4af7-8c12-8e9c2cdcc09b`. Type: **Major**. IntervalYear: **3**. IsInitial: `1`. ApplyAfterInitial: `0`. Budget: **Rehabilition**.

### Trigger

[PMS_abfTRIG_PM_Crack_Seal](expressions.md#e-44307b81-2222-4ae9-984a-543e62f4cbc6)

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

### Ordered resets

Order | Variable | Filter | Reset expression
---: | --- | --- | ---
0 | PMS_nAAV_AGE_ECI_Hold | (none) | [PMS_ancOBJ_ABS_4](expressions.md#e-714e7f1c-45e1-4caf-a4e8-c2a6b556a5ee)
1 | PMS_nAAV_AGE_JCI_Hold | (none) | [PMS_ancOBJ_ABS_4](expressions.md#e-714e7f1c-45e1-4caf-a4e8-c2a6b556a5ee)
2 | PMS_nAAV_AGE_CSI_Hold | (none) | [PMS_ancOBJ_ABS_4](expressions.md#e-714e7f1c-45e1-4caf-a4e8-c2a6b556a5ee)
3 | PMS_nAAV_AGE_SCI_Hold | (none) | [PMS_ancOBJ_ABS_4](expressions.md#e-714e7f1c-45e1-4caf-a4e8-c2a6b556a5ee)
4 | PMS_nAAV_AGE_CCI_Hold | (none) | [PMS_ancOBJ_ABS_4](expressions.md#e-714e7f1c-45e1-4caf-a4e8-c2a6b556a5ee)
5 | PMS_nAAV_CND_IRI | (none) | [PMS_ancRES_IRI](expressions.md#e-1d4efdbd-03bf-4bc2-b189-da59dab901ae)
6 | PMS_nAAV_CND_PCRK | (none) | [PMS_ancRES_PCRK](expressions.md#e-0a1d81b8-b54b-490f-9238-9e8cc47b9f96)
7 | PMS_nAAV_CND_RUT | (none) | [PMS_ancCND_Rut](expressions.md#e-4f8cf211-5f31-4d5e-92dd-6f048cf7f6c6)
8 | PMS_nAAV_CND_RSL | (none) | [PMS_ancCND_RSL](expressions.md#e-7fbb09b7-c2ae-4497-8890-e69a5d3999b6)
9 | PMS_nAAV_Yrly_Cost | (none) | [PMS_ancOBJ_AAV_Yrly_Cost_All](expressions.md#e-76d307ed-3427-462f-a79f-e16a387566dd)
10 | PMS_tAAV_FLT_GFP | (none) | [PMS_ancCND_FLT_GFP](expressions.md#e-8696dc20-6bf3-44d2-b7c8-d93b39ae6fc3)
11 | PMS_tAAV_IRI_GFP | (none) | [PMS_ancCND_IRI_GFP](expressions.md#e-ab06bc85-2e62-4269-aeda-d8bd7144b6ad)
12 | PMS_tAAV_PCRK_GFP | (none) | [PMS_ancCND_PCRK_GFP](expressions.md#e-40e28ca8-4605-426b-8c97-7b2c1cc92571)
13 | PMS_tAAV_RUT_GFP | (none) | [PMS_ancCND_RUT_GFP](expressions.md#e-04c76ab6-b287-4c9d-9399-90033e4cc5e7)
14 | PMS_tAAV_MAP21_GFP | (none) | [PMS_ancCND_MAP21_GFP](expressions.md#e-0452c4fb-af93-4324-bc0b-4576e857ae86)
15 | PMS_nDAV_CNT_CHIP_SEALS | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
16 | PMS_tAAV_YEARLY_TREATMENT | (none) | [PMS_ancRES_Yearly_Treatment](expressions.md#e-ed2f1535-a24f-4156-8dbe-8b5e7dda5f7b)

### Costs

Order | Filter | Financial expression | Economic expression
---: | --- | --- | ---
0 | (none) | [PMS_ancCOST_PM_Crack_Seal](expressions.md#e-0dd039d8-05fc-41d4-b306-553738a40641) | (none)

### Allowed subsequent treatments

Order | Treatment
---: | ---
1 | PMS_PM_Chip_Seal
2 | PMS_PM_Crack_Seal
3 | PMS_PM_Cape_Seal
4 | PMS_PM_Microsurfacing
5 | PMS_PM_Saw_Seal_Joints
6 | PMS_PM_Ultra_Thin_Overlay
7 | PMS_Thin_Overlay
8 | PMS_Thick_Overlay
9 | PMS_Reconstruction
10 | PMS_Major_CPR_Diamond_Grind
11 | PMS_Minor_CPR_Diamond_Grind

### Ancillary treatments

Order | Treatment
---: | ---

### Analysis-set membership

- PMS_TURNPIKE; row `20b79499-6985-4783-9a55-151f70d0f793`
- DEL_INTERSTATES_2023_10_YEARS; row `35a7c7c0-93d4-452f-8f8b-340efb792a08`
- PMS_INTERSTATE; row `8b4a8910-2a55-41ec-a24a-3cd554a191b8`
- PMS_APD; row `0a5a504d-22a0-4d04-80ff-b89e6035b71b`
- DEL_APD_NO_I68_OR_OTHERS_USING_RIDICULOUS_PRICES; row `08502dcd-acc8-40ac-bdc4-f97078f7cb6c`

Transitive configuration dependency closure: 973 records; query `audit_treatment_dependencies`.

## PMS_PM_Microsurfacing

Microsurfacing

ID: `6deaabbc-c677-4184-884b-e5244a95c37f`. Type: **Major**. IntervalYear: **2**. IsInitial: `1`. ApplyAfterInitial: `0`. Budget: **9ef54d0a-bdbb-4b9b-ab3e-8277bd08b827**.

### Trigger

[PMS_abfTRIG_PM_Microsurfacing](expressions.md#e-5c21d9f2-955a-4709-b673-2f052321a295)

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

### Ordered resets

Order | Variable | Filter | Reset expression
---: | --- | --- | ---
0 | PMS_nAAV_CND_ECI | (none) | [PMS_ancRES_ECI_MICROSURFACE](expressions.md#e-e87af607-69b3-4c46-96e2-5a91a4f471d0)
1 | PMS_nAAV_CND_PSI | (none) | [PMS_ancRES_PSI_MICROSURFACE](expressions.md#e-b0ed3473-2081-4c83-926d-0440557ed1b1)
2 | PMS_nAAV_CND_RDI | (none) | [PMS_ancRES_RDI_MICROSURFACE](expressions.md#e-9d879d4e-9d1d-4f51-8cec-2c9e391319a4)
3 | PMS_nAAV_CND_SCI | (none) | [PMS_ancRES_SCI_MICROSURFACE](expressions.md#e-2eeb79c4-579f-44e3-8bdc-3ea05f4369b5)
4 | PMS_nAAV_CND_CCI | (none) | [PMS_ancRES_CCI_MICROSURFACE](expressions.md#e-0db279f4-1eaf-41c8-9a50-5be54360cfed)
5 | PMS_nAAV_AGE_ECI | (none) | [PMS_ancAGE_ECI_AGE_FROM_INDEX](expressions.md#e-a98afc4d-071a-4fc7-86ef-7840afcd83e8)
6 | PMS_nAAV_AGE_PSI | (none) | [PMS_ancAGE_PSI_AGE_FROM_INDEX](expressions.md#e-af3d20fc-fa3b-4485-bcee-8714e4acca9f)
7 | PMS_nAAV_AGE_RDI | (none) | [PMS_ancAGE_RDI_AGE_FROM_INDEX](expressions.md#e-193bb441-a7ab-412f-9d12-ab4247b78d6a)
8 | PMS_nAAV_AGE_SCI | (none) | [PMS_ancAGE_SCI_AGE_FROM_INDEX](expressions.md#e-2ef1c4f5-220d-45a3-860d-d073db59ef9e)
9 | PMS_nAAV_AGE_CCI | (none) | [PMS_ancAGE_CCI_AGE_FROM_INDEX](expressions.md#e-2dbc899c-4c91-45a0-bd93-e02b1456b995)
10 | PMS_nAAV_CND_RSL | (none) | [PMS_ancCND_RSL](expressions.md#e-7fbb09b7-c2ae-4497-8890-e69a5d3999b6)
11 | PMS_nAAV_CND_IRI | (none) | [PMS_ancRES_IRI](expressions.md#e-1d4efdbd-03bf-4bc2-b189-da59dab901ae)
12 | PMS_nAAV_CND_PCRK | (none) | [PMS_ancCND_PCRK](expressions.md#e-b33b7403-ae8e-47b1-9bb8-a3b102200464)
13 | PMS_nAAV_CND_RUT | (none) | [PMS_ancCND_Rut](expressions.md#e-4f8cf211-5f31-4d5e-92dd-6f048cf7f6c6)
14 | PMS_tDAV_Rehab_Type | (none) | [PMS_ancOBJ_ABS_Minor](expressions.md#e-8fa0a363-e9d0-4bc7-8324-822d97acb948)
15 | PMS_tDAV_Truck_Load | (none) | [PMS_ancTRF_Truck_Load](expressions.md#e-0a9b6cd0-79b4-4da2-a728-ab165b8fe547)
16 | PMS_nAAV_Yrly_Cost | (none) | [PMS_ancOBJ_AAV_Yrly_Cost_All](expressions.md#e-76d307ed-3427-462f-a79f-e16a387566dd)
17 | PMS_tAAV_FLT_GFP | (none) | [PMS_ancCND_FLT_GFP](expressions.md#e-8696dc20-6bf3-44d2-b7c8-d93b39ae6fc3)
18 | PMS_tAAV_IRI_GFP | (none) | [PMS_ancCND_IRI_GFP](expressions.md#e-ab06bc85-2e62-4269-aeda-d8bd7144b6ad)
19 | PMS_tAAV_PCRK_GFP | (none) | [PMS_ancCND_PCRK_GFP](expressions.md#e-40e28ca8-4605-426b-8c97-7b2c1cc92571)
20 | PMS_tAAV_RUT_GFP | (none) | [PMS_ancCND_RUT_GFP](expressions.md#e-04c76ab6-b287-4c9d-9399-90033e4cc5e7)
21 | PMS_tAAV_MAP21_GFP | (none) | [PMS_ancCND_MAP21_GFP](expressions.md#e-0452c4fb-af93-4324-bc0b-4576e857ae86)
22 | PMS_nDAV_CNT_CHIP_SEALS | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
23 | PMS_nDAV_CNT_MICROSURFACE | (none) | [PMS_ancRES_CNT_MICROSURFACE](expressions.md#e-870fadb0-cdad-49eb-829f-599710b454e3)
24 | PMS_tAAV_YEARLY_TREATMENT | (none) | [PMS_ancRES_Yearly_Treatment](expressions.md#e-ed2f1535-a24f-4156-8dbe-8b5e7dda5f7b)

### Costs

Order | Filter | Financial expression | Economic expression
---: | --- | --- | ---
0 | (none) | [PMS_ancCOST_PM_Microsurfacing](expressions.md#e-d7e6a0ad-2b0d-4664-91ec-2103413fd043) | (none)

### Allowed subsequent treatments

Order | Treatment
---: | ---
1 | PMS_Preservation
2 | PMS_Thick_Overlay
3 | PMS_Thin_Overlay
4 | PMS_PM_Microsurfacing
5 | PMS_Fair_Treatment_For_GFP_Analaysis_70P_Good

### Ancillary treatments

Order | Treatment
---: | ---

### Analysis-set membership

- PMS_NHS_TENTH; row `e6097db2-0fb2-4c5e-8f73-038f07a35624`
- DEL_STIP_2026_DISTRICT_009_Non_NHS; row `b9f8336e-8382-4921-9ef1-09afd0c766f6`
- PMS_INTERSTATE; row `f33f8b44-b713-4db0-a1d6-23b00c20cb0d`
- DEL_NonNHS_Routes; row `b540ea12-ecac-4541-910d-2ccacae2c7ac`
- DEL_STIP_2026_DISTRICT_010_NHS_ONLY; row `91c16842-fd93-44e3-a620-3abe5a0694dd`
- PMS_TURNPIKE; row `bb7b53eb-e021-4e93-b2fb-4e9664216170`
- DEL_STIP_2026_DISTRICT_007_Non_NHS; row `e5ff73e3-ced0-4be8-84ce-4ec27df0a3df`
- PMS_NON_NHS_NON_TURNPIKE; row `dcf0fd2e-ec91-4e3a-b9fc-575a58e00690`
- DEL_STIP_2026_DISTRICT_007_NHS_ONLY; row `71c04958-b71f-41a9-be94-5b33d4e73424`
- DEL_STIP_2026_DISTRICT_002_Non_NHS; row `dd72f3f0-0512-4a02-ab67-653a921de534`
- DEL_STIP_2026_DISTRICT_003_Non_NHS; row `6aaa06a3-43ee-42af-8768-6bfc1c505d24`
- DEL_STIP_2026_NHS_ONLY_NO_INTERSTATE; row `4b9903f6-f364-48ee-b2f6-704d47c79c93`
- DEL_STIP_2026_DISTRICT_008_Non_NHS; row `246a5009-aa53-4ccc-89ad-708c1f9e5a37`
- DEL_STIP_2026_DISTRICT_009_NHS_ONLY; row `aa9fddb4-f357-4adb-890d-7147694ef983`
- DEL_STIP_2026_DISTRICT_003_NHS_ONLY; row `7cdf0f99-9f37-4eb6-b7ba-8415bc750e86`
- PMS_APD; row `7f1ce975-415c-40fd-9e84-86469312eff0`
- DEL_STIP_2026_DISTRICT_010_Non_NHS; row `aade6e46-5950-4f8f-bd73-8759503b29d1`
- DEL_INTERSTATES_2023_10_YEARS; row `5b1f1f4c-6dfc-48dc-95e1-90c64d6e5cec`
- DEL_STIP_2026_DISTRICT_006_Non_NHS; row `f17444e3-dd87-48cb-b47d-9679545cfb89`
- DEL_STIP_2026_Non_NHS_ALL_NETWORK; row `c1333f5e-43d5-4cb8-a0e1-9a313058169e`
- DEL_APD_NO_I68_OR_OTHERS_USING_RIDICULOUS_PRICES; row `6fd4f1a9-020c-475e-a7b4-9b81f576d3fd`
- DEL_STIP_2026_DISTRICT_005_Non_NHS; row `acd904fc-2169-4f14-8c8a-9d8c142e4900`
- DEL_STIP_2026_DISTRICT_006_NHS_ONLY; row `bda278f1-34ee-48a6-be80-a4a811986d7b`
- DEL_STIP_2026_DISTRICT_005_NHS_ONLY; row `e2fef7ca-516a-4c7c-9069-aa5d81a6a836`
- DEL_STIP_2026_INTERSTATES_ONLY; row `f007176e-0c40-4257-82e7-ae1dddabef97`
- DEL_STIP_2026_DISTRICT_004_Non_NHS; row `986daa41-9c26-490d-8b75-bfe9b34a56bf`
- DEL_STIP_2026_DISTRICT_002_NHS_ONLY; row `6e421a12-1512-4bfa-892c-c031b7e31f69`
- DEL_STIP_2026_DISTRICT_008_NHS_ONLY; row `41fa041e-4cf2-4689-98ee-daa75274d687`
- DEL_STIP_2026_DISTRICT_004_NHS_ONLY; row `74008ef2-efc3-45ef-852d-e454a7583e6c`
- DEL_STIP_2026_DISTRICT_001_NHS_ONLY; row `cf1926bf-012f-47b8-bdba-f58ca637c0b3`
- PMS_NHS; row `b3e50e2f-0db6-4d7f-bc85-f8923ee06dd0`
- DEL_STIP_2026_DISTRICT_001_Non_NHS; row `7528aaaf-33be-43e0-96bd-ff511d94d56f`

Transitive configuration dependency closure: 1224 records; query `audit_treatment_dependencies`.

## PMS_PM_Saw_Seal_Joints

Saw and Seal Joints

ID: `b0e9fe8f-dc12-4fd9-b1cc-5cdfc9d7668d`. Type: **Major**. IntervalYear: **6**. IsInitial: `1`. ApplyAfterInitial: `0`. Budget: **Rehabilition**.

### Trigger

[PMS_abfTRIG_PM_Saw_Seal_Joints](expressions.md#e-28f28e08-7b05-43bf-a28c-22d1286c6fc2)

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

### Ordered resets

Order | Variable | Filter | Reset expression
---: | --- | --- | ---
0 | PMS_nAAV_AGE_JCI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
1 | PMS_nAAV_CND_JCI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
2 | PMS_nAAV_CND_CCI | (none) | [PMS_ancRES_CCI_SAW_and_SEAL](expressions.md#e-c82e6892-be0e-48bf-a02b-e73e7029cbff)
3 | PMS_nAAV_CND_IRI | (none) | [PMS_ancRES_IRI](expressions.md#e-1d4efdbd-03bf-4bc2-b189-da59dab901ae)
4 | PMS_nAAV_CND_PCRK | (none) | [PMS_ancRES_PCRK](expressions.md#e-0a1d81b8-b54b-490f-9238-9e8cc47b9f96)
5 | PMS_nAAV_CND_RSL | (none) | [PMS_ancCND_RSL](expressions.md#e-7fbb09b7-c2ae-4497-8890-e69a5d3999b6)
6 | PMS_tDAV_Rehab_Type | (none) | [PMS_ancOBJ_ABS_Minor](expressions.md#e-8fa0a363-e9d0-4bc7-8324-822d97acb948)
7 | PMS_tDAV_Truck_Load | (none) | [PMS_ancTRF_Truck_Load](expressions.md#e-0a9b6cd0-79b4-4da2-a728-ab165b8fe547)
8 | PMS_nAAV_Yrly_Cost | (none) | [PMS_ancOBJ_AAV_Yrly_Cost_All](expressions.md#e-76d307ed-3427-462f-a79f-e16a387566dd)
9 | PMS_tAAV_FLT_GFP | (none) | [PMS_ancCND_FLT_GFP](expressions.md#e-8696dc20-6bf3-44d2-b7c8-d93b39ae6fc3)
10 | PMS_tAAV_IRI_GFP | (none) | [PMS_ancCND_IRI_GFP](expressions.md#e-ab06bc85-2e62-4269-aeda-d8bd7144b6ad)
11 | PMS_tAAV_PCRK_GFP | (none) | [PMS_ancCND_PCRK_GFP](expressions.md#e-40e28ca8-4605-426b-8c97-7b2c1cc92571)
12 | PMS_tAAV_RUT_GFP | (none) | [PMS_ancCND_RUT_GFP](expressions.md#e-04c76ab6-b287-4c9d-9399-90033e4cc5e7)
13 | PMS_tAAV_MAP21_GFP | (none) | [PMS_ancCND_MAP21_GFP](expressions.md#e-0452c4fb-af93-4324-bc0b-4576e857ae86)
14 | PMS_tAAV_YEARLY_TREATMENT | (none) | [PMS_ancRES_Yearly_Treatment](expressions.md#e-ed2f1535-a24f-4156-8dbe-8b5e7dda5f7b)

### Costs

Order | Filter | Financial expression | Economic expression
---: | --- | --- | ---
0 | (none) | [PMS_ancCOST_PM_Saw_Seal_Joints](expressions.md#e-0faa0748-1d4f-4baa-9f68-449391104e85) | (none)

### Allowed subsequent treatments

Order | Treatment
---: | ---
1 | PMS_PM_Saw_Seal_Joints
2 | PMS_PM_Crack_Seal
3 | PMS_Thin_Overlay
4 | PMS_Thick_Overlay
5 | PMS_Reconstruction
6 | PMS_Major_CPR_Diamond_Grind
7 | PMS_Minor_CPR_Diamond_Grind

### Ancillary treatments

Order | Treatment
---: | ---

### Analysis-set membership

- DEL_APD_NO_I68_OR_OTHERS_USING_RIDICULOUS_PRICES; row `a029ce90-f8e2-4d7f-ae95-14eb27c45bba`
- PMS_NHS_TENTH; row `dddb2f8e-31b7-4600-80c7-3443c6c10bfc`
- PMS_INTERSTATE; row `f6c502ea-5cad-4ef1-b8ee-498462ded2cd`
- PMS_TURNPIKE; row `581cb46d-ebfe-43d2-aa4a-795d62705c8b`
- PMS_APD; row `52154fe2-b6e4-4e42-8b1a-9e6770d3e003`
- DEL_INTERSTATES_2023_10_YEARS; row `c02ae3c6-6f3d-413c-8a6d-cf8ff208aee0`

Transitive configuration dependency closure: 976 records; query `audit_treatment_dependencies`.

## PMS_PM_Ultra_Thin_Overlay

Ultra Thin Overlay

ID: `cfbda0c3-3525-482c-8b12-be07eeeec34a`. Type: **Major**. IntervalYear: **4**. IsInitial: `1`. ApplyAfterInitial: `0`. Budget: **Rehabilition**.

### Trigger

[PMS_abfTRIG_PM_Ultra_Thin_Overlay](expressions.md#e-3dcfe007-7999-418b-bbf1-649aa56fb2f4)

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

### Ordered resets

Order | Variable | Filter | Reset expression
---: | --- | --- | ---
0 | PMS_nAAV_CND_ECI | (none) | [PMS_ancRES_ECI_ULTRA_THIN](expressions.md#e-354afb8c-179e-44cf-a7cd-0009306fe1e9)
1 | PMS_nAAV_CND_PSI | (none) | [PMS_ancRES_PSI_ULTRA_THIN](expressions.md#e-391639e4-c03a-4e75-bf5d-7df493d8dc58)
2 | PMS_nAAV_CND_RDI | (none) | [PMS_ancRES_RDI_ULTRA_THIN](expressions.md#e-da41ad22-f67a-47d1-9cdc-60e38ccf55a9)
3 | PMS_nAAV_CND_SCI | (none) | [PMS_ancRES_SCI_ULTRA_THIN](expressions.md#e-000dd3e3-7e0f-42f1-870e-d8ef825b70a4)
4 | PMS_nAAV_CND_CCI | (none) | [PMS_ancRES_CCI_ULTRA_THIN](expressions.md#e-2709c4c3-b9ba-4e73-a1bc-0e02c260d0af)
5 | PMS_nAAV_AGE_ECI | (none) | [PMS_ancAGE_ECI_AGE_FROM_INDEX](expressions.md#e-a98afc4d-071a-4fc7-86ef-7840afcd83e8)
6 | PMS_nAAV_AGE_PSI | (none) | [PMS_ancAGE_PSI_AGE_FROM_INDEX](expressions.md#e-af3d20fc-fa3b-4485-bcee-8714e4acca9f)
7 | PMS_nAAV_AGE_RDI | (none) | [PMS_ancAGE_RDI_AGE_FROM_INDEX](expressions.md#e-193bb441-a7ab-412f-9d12-ab4247b78d6a)
8 | PMS_nAAV_AGE_SCI | (none) | [PMS_ancAGE_SCI_AGE_FROM_INDEX](expressions.md#e-2ef1c4f5-220d-45a3-860d-d073db59ef9e)
9 | PMS_nAAV_AGE_CCI | (none) | [PMS_ancAGE_CCI_AGE_FROM_INDEX](expressions.md#e-2dbc899c-4c91-45a0-bd93-e02b1456b995)
10 | PMS_nAAV_CND_IRI | (none) | [PMS_ancRES_IRI](expressions.md#e-1d4efdbd-03bf-4bc2-b189-da59dab901ae)
11 | PMS_nAAV_CND_PCRK | (none) | [PMS_ancRES_PCRK](expressions.md#e-0a1d81b8-b54b-490f-9238-9e8cc47b9f96)
12 | PMS_nAAV_CND_RUT | (none) | [PMS_ancCND_Rut](expressions.md#e-4f8cf211-5f31-4d5e-92dd-6f048cf7f6c6)
13 | PMS_nAAV_CND_RSL | (none) | [PMS_ancCND_RSL](expressions.md#e-7fbb09b7-c2ae-4497-8890-e69a5d3999b6)
14 | PMS_tDAV_Rehab_Type | (none) | [PMS_ancOBJ_ABS_Minor](expressions.md#e-8fa0a363-e9d0-4bc7-8324-822d97acb948)
15 | PMS_tDAV_Truck_Load | (none) | [PMS_ancTRF_Truck_Load](expressions.md#e-0a9b6cd0-79b4-4da2-a728-ab165b8fe547)
16 | PMS_nAAV_Yrly_Cost | (none) | [PMS_ancOBJ_AAV_Yrly_Cost_All](expressions.md#e-76d307ed-3427-462f-a79f-e16a387566dd)
17 | PMS_tAAV_FLT_GFP | (none) | [PMS_ancCND_FLT_GFP](expressions.md#e-8696dc20-6bf3-44d2-b7c8-d93b39ae6fc3)
18 | PMS_tAAV_IRI_GFP | (none) | [PMS_ancCND_IRI_GFP](expressions.md#e-ab06bc85-2e62-4269-aeda-d8bd7144b6ad)
19 | PMS_tAAV_PCRK_GFP | (none) | [PMS_ancCND_PCRK_GFP](expressions.md#e-40e28ca8-4605-426b-8c97-7b2c1cc92571)
20 | PMS_tAAV_RUT_GFP | (none) | [PMS_ancCND_RUT_GFP](expressions.md#e-04c76ab6-b287-4c9d-9399-90033e4cc5e7)
21 | PMS_tAAV_MAP21_GFP | (none) | [PMS_ancCND_MAP21_GFP](expressions.md#e-0452c4fb-af93-4324-bc0b-4576e857ae86)
22 | PMS_nDAV_CNT_CHIP_SEALS | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
23 | PMS_nDAV_CNT_MICROSURFACE | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
24 | PMS_tAAV_YEARLY_TREATMENT | (none) | [PMS_ancRES_Yearly_Treatment](expressions.md#e-ed2f1535-a24f-4156-8dbe-8b5e7dda5f7b)

### Costs

Order | Filter | Financial expression | Economic expression
---: | --- | --- | ---
0 | (none) | [PMS_ancCOST_PM_Ultra_Thin_Overlay](expressions.md#e-ed5ccc87-740f-4148-b9c1-5f90250f6c6f) | (none)

### Allowed subsequent treatments

Order | Treatment
---: | ---
1 | PMS_PM_Crack_Seal
2 | PMS_PM_Chip_Seal
3 | PMS_PM_Cape_Seal
4 | PMS_PM_Microsurfacing
5 | PMS_PM_Ultra_Thin_Overlay
6 | PMS_Thin_Overlay
7 | PMS_Thick_Overlay
8 | PMS_Reconstruction

### Ancillary treatments

Order | Treatment
---: | ---

### Analysis-set membership

- PMS_TURNPIKE; row `524ac78e-ba28-40c9-8275-3f74f1ce5699`
- PMS_APD; row `0e4256c6-1c1a-4f1d-ac85-8e1d1b98acd8`
- PMS_NHS_TENTH; row `0dbed93c-427c-47c6-82c5-9310920661ad`
- PMS_INTERSTATE; row `2abbe470-f529-4b1d-856e-9417dba5cc2f`

Transitive configuration dependency closure: 957 records; query `audit_treatment_dependencies`.

## PMS_Preservation

Pavement Preservation Generic Treatment

ID: `0e0f12a3-e4a7-4d49-add9-ec4123a55169`. Type: **Major**. IntervalYear: **0**. IsInitial: `1`. ApplyAfterInitial: `0`. Budget: **Rehabilition**.

### Trigger

[PMS_abfTRIG_PM_Preservation](expressions.md#e-98f4613f-6f58-48ee-8059-baffb001aee8)

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

### Ordered resets

Order | Variable | Filter | Reset expression
---: | --- | --- | ---
0 | PMS_nAAV_AGE_ECI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
1 | PMS_nAAV_AGE_PSI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
2 | PMS_nAAV_AGE_RDI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
3 | PMS_nAAV_AGE_SCI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
4 | PMS_nAAV_AGE_JCI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
5 | PMS_nAAV_AGE_CSI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
6 | PMS_nAAV_AGE_CCI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
7 | PMS_nAAV_CND_ECI | (none) | [PMS_ancOBJ_ABS_4_5_ECI](expressions.md#e-128fcb68-54cb-47df-a378-5d5c8986e723)
8 | PMS_nAAV_CND_PSI | (none) | [PMS_ancOBJ_ABS_4_5_PSI](expressions.md#e-cf97cde2-65f1-41b2-a110-664314d91e08)
9 | PMS_nAAV_CND_RDI | (none) | [PMS_ancOBJ_ABS_4_5_RDI](expressions.md#e-666c1328-3e75-49b8-9cd6-b669a2378f2f)
10 | PMS_nAAV_CND_SCI | (none) | [PMS_ancOBJ_ABS_4_5_SCI](expressions.md#e-d316035d-473e-4fa0-b3ba-d36461157c6b)
11 | PMS_nAAV_CND_JCI | (none) | [PMS_ancOBJ_ABS_4_5_JCI](expressions.md#e-cdcff07f-7572-4870-b91d-a632deeca3f4)
12 | PMS_nAAV_CND_CSI | (none) | [PMS_ancOBJ_ABS_4_5_CSI](expressions.md#e-70de9024-06fd-424d-b31f-63a89bd17f0a)
13 | PMS_nAAV_CND_CCI | (none) | [PMS_ancOBJ_ABS_4_5_CCI](expressions.md#e-6aa8fc26-24d2-4ddf-bf53-ea80f0bd69ae)
14 | PMS_nAAV_CND_RSL | (none) | [PMS_ancCND_RSL](expressions.md#e-7fbb09b7-c2ae-4497-8890-e69a5d3999b6)
15 | PMS_tDAV_Rehab_Type | (none) | [PMS_ancOBJ_ABS_Minor](expressions.md#e-8fa0a363-e9d0-4bc7-8324-822d97acb948)
16 | PMS_tDAV_Truck_Load | (none) | [PMS_ancTRF_Truck_Load](expressions.md#e-0a9b6cd0-79b4-4da2-a728-ab165b8fe547)
17 | PMS_nAAV_Yrly_Cost | (none) | [PMS_ancOBJ_AAV_Yrly_Cost_All](expressions.md#e-76d307ed-3427-462f-a79f-e16a387566dd)
18 | PMS_tAAV_FLT_GFP | (none) | [PMS_ancCND_FLT_GFP](expressions.md#e-8696dc20-6bf3-44d2-b7c8-d93b39ae6fc3)
19 | PMS_tAAV_IRI_GFP | (none) | [PMS_ancCND_IRI_GFP](expressions.md#e-ab06bc85-2e62-4269-aeda-d8bd7144b6ad)
20 | PMS_tAAV_PCRK_GFP | (none) | [PMS_ancCND_PCRK_GFP](expressions.md#e-40e28ca8-4605-426b-8c97-7b2c1cc92571)
21 | PMS_tAAV_RUT_GFP | (none) | [PMS_ancCND_RUT_GFP](expressions.md#e-04c76ab6-b287-4c9d-9399-90033e4cc5e7)
22 | PMS_tAAV_MAP21_GFP | (none) | [PMS_ancCND_MAP21_GFP](expressions.md#e-0452c4fb-af93-4324-bc0b-4576e857ae86)
23 | PMS_tAAV_YEARLY_TREATMENT | (none) | [PMS_ancRES_Yearly_Treatment](expressions.md#e-ed2f1535-a24f-4156-8dbe-8b5e7dda5f7b)

### Costs

Order | Filter | Financial expression | Economic expression
---: | --- | --- | ---
0 | (none) | [PMS_ancCOST_PM_Prreservation](expressions.md#e-0c1a2284-4759-48ec-8cb3-7a6fd915fc4a) | (none)

### Allowed subsequent treatments

Order | Treatment
---: | ---
1 | PMS_PM_Crack_Seal
2 | PMS_PM_Chip_Seal
3 | PMS_PM_Cape_Seal
4 | PMS_PM_Microsurfacing
5 | PMS_PM_Ultra_Thin_Overlay
6 | PMS_Thin_Overlay
7 | PMS_Thick_Overlay
8 | PMS_Reconstruction

### Ancillary treatments

Order | Treatment
---: | ---

### Analysis-set membership

- DEL_STIP_2026_DISTRICT_004_NHS_ONLY; row `0adf731b-aed0-4ebf-aa0d-41d35d2abf22`
- DEL_STIP_2026_Non_NHS_ALL_NETWORK; row `89ee2bc8-4a26-49f6-bc26-543dcf6f9f59`
- DEL_STIP_2026_NHS_ONLY_NO_INTERSTATE; row `433b33ef-8b35-4044-afec-a59ba0c78b28`
- DEL_STIP_2026_INTERSTATES_ONLY; row `f44e8bbc-6c2b-49bd-9c7d-b3c9161c21e2`

Transitive configuration dependency closure: 1001 records; query `audit_treatment_dependencies`.

## PMS_Reconstruction

Reconstruction

ID: `fec90a29-c97a-4ed3-8d4c-de9c9a759e00`. Type: **Major**. IntervalYear: **4**. IsInitial: `1`. ApplyAfterInitial: `0`. Budget: **Rehabilition**.

### Trigger

[PMS_abfTRIG_Reconstruct](expressions.md#e-c31b4232-a667-41f9-b7bc-48e3035fa7f0)

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

### Ordered resets

Order | Variable | Filter | Reset expression
---: | --- | --- | ---
0 | PMS_nAAV_AGE_ECI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
1 | PMS_nAAV_AGE_PSI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
2 | PMS_nAAV_AGE_RDI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
3 | PMS_nAAV_AGE_SCI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
4 | PMS_nAAV_AGE_JCI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
5 | PMS_nAAV_AGE_CSI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
6 | PMS_nAAV_AGE_CCI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
7 | PMS_nAAV_CND_ECI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
8 | PMS_nAAV_CND_PSI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
9 | PMS_nAAV_CND_RDI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
10 | PMS_nAAV_CND_SCI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
11 | PMS_nAAV_CND_JCI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
12 | PMS_nAAV_CND_CSI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
13 | PMS_nAAV_CND_CCI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
14 | PMS_nAAV_CND_IRI | (none) | [PMS_ancCND_IRI](expressions.md#e-fe3e82d6-4c7e-43db-9766-fef084908311)
15 | PMS_nAAV_CND_PCRK | (none) | [PMS_ancCND_PCRK](expressions.md#e-b33b7403-ae8e-47b1-9bb8-a3b102200464)
16 | PMS_nAAV_CND_RUT | (none) | [PMS_ancCND_Rut](expressions.md#e-4f8cf211-5f31-4d5e-92dd-6f048cf7f6c6)
17 | PMS_nAAV_CND_FLT | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
18 | PMS_nAAV_CND_RSL | (none) | [PMS_ancCND_RSL](expressions.md#e-7fbb09b7-c2ae-4497-8890-e69a5d3999b6)
19 | PMS_tDAV_Pave_Type | (none) | [PMS_ancOBJ_ABS_BC](expressions.md#e-0dcb857c-950e-414b-8bc3-c18da79f8883)
20 | PMS_tDAV_Rehab_Type | (none) | [PMS_ancOBJ_ABS_Initial](expressions.md#e-4b58324a-2cad-4cd7-8036-b410e412ba6c)
21 | PMS_tDAV_Truck_Load | (none) | [PMS_ancTRF_Truck_Load](expressions.md#e-0a9b6cd0-79b4-4da2-a728-ab165b8fe547)
22 | PMS_nAAV_Yrly_Cost | (none) | [PMS_ancOBJ_AAV_Yrly_Cost_All](expressions.md#e-76d307ed-3427-462f-a79f-e16a387566dd)
23 | PMS_tAAV_FLT_GFP | (none) | [PMS_ancCND_FLT_GFP](expressions.md#e-8696dc20-6bf3-44d2-b7c8-d93b39ae6fc3)
24 | PMS_tAAV_IRI_GFP | (none) | [PMS_ancCND_IRI_GFP](expressions.md#e-ab06bc85-2e62-4269-aeda-d8bd7144b6ad)
25 | PMS_tAAV_PCRK_GFP | (none) | [PMS_ancCND_PCRK_GFP](expressions.md#e-40e28ca8-4605-426b-8c97-7b2c1cc92571)
26 | PMS_tAAV_RUT_GFP | (none) | [PMS_ancCND_RUT_GFP](expressions.md#e-04c76ab6-b287-4c9d-9399-90033e4cc5e7)
27 | PMS_tAAV_MAP21_GFP | (none) | [PMS_ancCND_MAP21_GFP](expressions.md#e-0452c4fb-af93-4324-bc0b-4576e857ae86)
28 | PMS_nDAV_CNT_CHIP_SEALS | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
29 | PMS_nDAV_CNT_MICROSURFACE | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
30 | PMS_tAAV_YEARLY_TREATMENT | (none) | [PMS_ancRES_Yearly_Treatment](expressions.md#e-ed2f1535-a24f-4156-8dbe-8b5e7dda5f7b)

### Costs

Order | Filter | Financial expression | Economic expression
---: | --- | --- | ---
0 | (none) | [PMS_ancCOST_Reconstruction](expressions.md#e-41eee71c-be07-412d-a666-98123d0648d2) | (none)

### Allowed subsequent treatments

Order | Treatment
---: | ---
1 | PMS_PM_Chip_Seal
2 | PMS_PM_Crack_Seal
3 | PMS_PM_Concrete
4 | PMS_PM_Microsurfacing
5 | PMS_PM_Ultra_Thin_Overlay
6 | PMS_Thin_Overlay
7 | PMS_Thick_Overlay
8 | PMS_Reconstruction
9 | PMS_PM_Asphalt
10 | PMS_PM_Cape_Seal

### Ancillary treatments

Order | Treatment
---: | ---

### Analysis-set membership

- DEL_APD_NO_I68_OR_OTHERS_USING_RIDICULOUS_PRICES; row `712282b7-b56e-4fb9-9fb9-1307f28ae711`
- PMS_INTERSTATE; row `3fe8fa51-2664-4826-ae8b-16c9a249d01a`
- DEL_INTERSTATES_2023_10_YEARS; row `07e0300b-2b15-443d-9e52-22de52fce4a8`
- DEL_NonNHS_Routes; row `edea099f-0087-4cc7-83bf-2848516e0fe8`
- DEL_STIP_2026_Non_NHS_ALL_NETWORK; row `0e6c35cb-0dc0-456e-95c3-2873aa18b422`
- PMS_TURNPIKE; row `45aeda1c-56f9-43f1-a15d-6074d0a9e577`
- PMS_NHS_TENTH; row `886315ad-ad15-4690-aea7-63a78326b35c`
- DEL_STIP_2026_INTERSTATES_ONLY; row `21ffd151-5db3-41de-9e90-8cb71bf15b23`
- DEL_STIP_2026_DISTRICT_004_NHS_ONLY; row `28d56016-b154-48e9-9e05-aa3675d64ebc`
- DEL_STIP_2026_NHS_ONLY_NO_INTERSTATE; row `93d8d62f-71a4-4b66-bfc1-e4f56518bd8e`
- PMS_APD; row `a7b7154d-2cce-4214-9f38-f1daf334e4e0`
- PMS_NHS; row `f0a7b6a4-91c3-4b55-aca2-f2b6ff816863`

Transitive configuration dependency closure: 1010 records; query `audit_treatment_dependencies`.

## PMS_Thick_Overlay

Thick Overlay

ID: `c30fdc0e-9415-4cff-b262-fc925dfeb449`. Type: **Major**. IntervalYear: **2**. IsInitial: `1`. ApplyAfterInitial: `0`. Budget: **Rehabilition**.

### Trigger

[PMS_abfTRIG_Major_HMA_Overlay](expressions.md#e-1fd310a5-e53d-436d-842f-bd66dc4a4105)

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

### Ordered resets

Order | Variable | Filter | Reset expression
---: | --- | --- | ---
0 | PMS_nAAV_AGE_CSI | [PMS_abfOBJ_Concrete](expressions.md#e-ba469472-994d-4555-923b-c833047e7e8b) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
1 | PMS_nAAV_AGE_JCI | [PMS_abfOBJ_Concrete](expressions.md#e-ba469472-994d-4555-923b-c833047e7e8b) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
2 | PMS_nAAV_AGE_ECI | [PMS_abfOBJ_Asphalt](expressions.md#e-915f80f1-74d8-48c0-ab9f-fdffd05d547a) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
3 | PMS_nAAV_AGE_RDI | [PMS_abfOBJ_Asphalt](expressions.md#e-915f80f1-74d8-48c0-ab9f-fdffd05d547a) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
4 | PMS_nAAV_AGE_SCI | [PMS_abfOBJ_Asphalt](expressions.md#e-915f80f1-74d8-48c0-ab9f-fdffd05d547a) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
5 | PMS_nAAV_AGE_PSI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
6 | PMS_nAAV_AGE_CCI | (none) | [PMS_ancOBJ_ABS_1](expressions.md#e-453c8a3e-bd87-46f5-8faa-3ac49163c144)
7 | PMS_nAAV_CND_CSI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
8 | PMS_nAAV_CND_JCI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
9 | PMS_nAAV_CND_ECI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
10 | PMS_nAAV_CND_RDI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
11 | PMS_nAAV_CND_SCI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
12 | PMS_nAAV_CND_PSI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
13 | PMS_nAAV_CND_CCI | (none) | [PMS_ancOBJ_ABS_5](expressions.md#e-219ae665-588b-4f92-a506-59c28873d542)
14 | PMS_nAAV_CND_IRI | (none) | [PMS_ancRES_IRI](expressions.md#e-1d4efdbd-03bf-4bc2-b189-da59dab901ae)
15 | PMS_nAAV_CND_PCRK | (none) | [PMS_ancRES_PCRK](expressions.md#e-0a1d81b8-b54b-490f-9238-9e8cc47b9f96)
16 | PMS_nAAV_CND_RUT | (none) | [PMS_ancCND_Rut](expressions.md#e-4f8cf211-5f31-4d5e-92dd-6f048cf7f6c6)
17 | PMS_nAAV_CND_RSL | (none) | [PMS_ancCND_RSL](expressions.md#e-7fbb09b7-c2ae-4497-8890-e69a5d3999b6)
18 | PMS_tDAV_Rehab_Type | (none) | [PMS_ancOBJ_ABS_Major](expressions.md#e-f5a30d2f-e3d8-4245-998f-1f9088ccbdc1)
19 | PMS_tDAV_Truck_Load | (none) | [PMS_ancTRF_Truck_Load](expressions.md#e-0a9b6cd0-79b4-4da2-a728-ab165b8fe547)
20 | PMS_nAAV_Yrly_Cost | (none) | [PMS_ancOBJ_AAV_Yrly_Cost_All](expressions.md#e-76d307ed-3427-462f-a79f-e16a387566dd)
21 | PMS_tAAV_FLT_GFP | (none) | [PMS_ancCND_FLT_GFP](expressions.md#e-8696dc20-6bf3-44d2-b7c8-d93b39ae6fc3)
22 | PMS_tAAV_IRI_GFP | (none) | [PMS_ancCND_IRI_GFP](expressions.md#e-ab06bc85-2e62-4269-aeda-d8bd7144b6ad)
23 | PMS_tAAV_PCRK_GFP | (none) | [PMS_ancCND_PCRK_GFP](expressions.md#e-40e28ca8-4605-426b-8c97-7b2c1cc92571)
24 | PMS_tAAV_RUT_GFP | (none) | [PMS_ancCND_RUT_GFP](expressions.md#e-04c76ab6-b287-4c9d-9399-90033e4cc5e7)
25 | PMS_tAAV_MAP21_GFP | (none) | [PMS_ancCND_MAP21_GFP](expressions.md#e-0452c4fb-af93-4324-bc0b-4576e857ae86)
26 | PMS_nDAV_CNT_CHIP_SEALS | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
27 | PMS_nDAV_CNT_MICROSURFACE | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
28 | PMS_tAAV_YEARLY_TREATMENT | (none) | [PMS_ancRES_Yearly_Treatment](expressions.md#e-ed2f1535-a24f-4156-8dbe-8b5e7dda5f7b)

### Costs

Order | Filter | Financial expression | Economic expression
---: | --- | --- | ---
0 | (none) | [PMS_ancCOST_Major_HMA_Overlay](expressions.md#e-115f0959-e7c1-4c63-932d-20977377f2a9) | (none)

### Allowed subsequent treatments

Order | Treatment
---: | ---
1 | PMS_PM_Crack_Seal
2 | PMS_PM_Chip_Seal
3 | PMS_PM_Cape_Seal
4 | PMS_PM_Microsurfacing
5 | PMS_PM_Ultra_Thin_Overlay
6 | PMS_Thin_Overlay
7 | PMS_Thick_Overlay
8 | PMS_Reconstruction
9 | PMS_PM_Asphalt
10 | PMS_Preservation
10 | PMS_Preservation
12 | PMS_Fair_Treatment_For_GFP_Analaysis_70P_Good

### Ancillary treatments

Order | Treatment
---: | ---

### Analysis-set membership

- DEL_STIP_2026_NHS_ONLY_NO_INTERSTATE; row `d89f28e6-38c8-41fe-a715-179ccc024ec7`
- DEL_STIP_2026_DISTRICT_002_NHS_ONLY; row `f73a991e-164d-45e9-9d00-1b3ac339bd35`
- DEL_STIP_2026_DISTRICT_007_NHS_ONLY; row `44ad2004-321f-49b7-819d-1f157dd9bc2d`
- DEL_STIP_2026_Non_NHS_ALL_NETWORK; row `331aea5a-98fd-4eb6-a36b-1f222cf7b7ff`
- DEL_STIP_2026_DISTRICT_003_NHS_ONLY; row `e72de4fb-0599-4e0c-9c82-261cdfeb7231`
- DEL_STIP_2026_INTERSTATES_ONLY; row `bd3e1d69-6a9b-403f-bf22-29345b57764f`
- DEL_STIP_2026_DISTRICT_008_NHS_ONLY; row `ed422b6e-5bc2-426a-8fea-37c5e161b9f4`
- PMS_NON_NHS_NON_TURNPIKE; row `cfc17dbe-2221-4e59-9958-3cd963e661c7`
- PMS_INTERSTATE; row `c2cc60a7-bd12-4f4e-b88e-3d1e56d60ff0`
- DEL_STIP_2026_DISTRICT_006_NHS_ONLY; row `1e1668fd-c918-4104-910e-3ea380ede7a4`
- DEL_APD_NO_I68_OR_OTHERS_USING_RIDICULOUS_PRICES; row `48e80197-74ca-48ee-ac3d-4783695e334d`
- DEL_NonNHS_Routes; row `4bb8d43d-dc68-4edc-b500-5ce0feb3fdb1`
- PMS_APD; row `7d886f0b-08b2-4dac-8ba0-61b688d926bd`
- PMS_NHS_TENTH; row `b16d4ac6-2cef-44a0-ad45-636dc963879f`
- DEL_STIP_2026_DISTRICT_009_NHS_ONLY; row `57e00197-28ab-465e-8ec1-6af3be57bb93`
- PMS_TURNPIKE; row `e0f10a52-3c0b-4083-b311-7bffd920ee6e`
- DEL_STIP_2026_DISTRICT_010_NHS_ONLY; row `1f9547ed-57c1-4349-be70-8add6568dd8c`
- DEL_STIP_2026_DISTRICT_001_NHS_ONLY; row `028ccfe2-b395-4e0a-99c3-bb0692facf1c`
- DEL_STIP_2026_DISTRICT_005_NHS_ONLY; row `0641c2aa-15a3-456c-9abe-c80106aaced9`
- DEL_INTERSTATES_2023_10_YEARS; row `d438064d-453d-459e-87ca-cfd42fda58eb`
- PMS_NHS; row `80f7ba07-d9fe-4d2d-b19a-f36d268ed961`

Transitive configuration dependency closure: 1156 records; query `audit_treatment_dependencies`.

## PMS_Thin_Overlay

Thin Overlay

ID: `0ee1fedb-16e6-4beb-b570-27f6754b8ded`. Type: **Major**. IntervalYear: **2**. IsInitial: `1`. ApplyAfterInitial: `0`. Budget: **Rehabilition**.

### Trigger

[PMS_abfTRIG_Minor_HMA_Overlay](expressions.md#e-141ccfde-fd66-42cc-9c25-6987370a25f2)

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

### Ordered resets

Order | Variable | Filter | Reset expression
---: | --- | --- | ---
0 | PMS_nAAV_CND_ECI | (none) | [PMS_ancRES_ECI_THIN_OVERLAY](expressions.md#e-384514d5-5dee-4e86-a5c7-6bb5b3dd4a71)
1 | PMS_nAAV_CND_PSI | (none) | [PMS_ancRES_PSI_THIN_OVERLAY](expressions.md#e-3c2ad86c-8882-44b2-947a-aa1cd954f678)
2 | PMS_nAAV_CND_RDI | (none) | [PMS_ancRES_RDI_THIN_OVERLAY](expressions.md#e-4324d58a-d04d-4508-9ad6-ddadbbe810cf)
3 | PMS_nAAV_CND_SCI | (none) | [PMS_ancRES_SCI_THIN_OVERLAY](expressions.md#e-dbe9ae0c-cedb-480d-b047-f7941dbc4e62)
4 | PMS_nAAV_CND_CCI | (none) | [PMS_ancRES_CCI_THIN_OVERLAY](expressions.md#e-bf3aed6d-d0f5-4275-9a95-a7b9b5520e68)
5 | PMS_nAAV_AGE_ECI | (none) | [PMS_ancAGE_ECI_AGE_FROM_INDEX](expressions.md#e-a98afc4d-071a-4fc7-86ef-7840afcd83e8)
6 | PMS_nAAV_AGE_PSI | (none) | [PMS_ancAGE_PSI_AGE_FROM_INDEX](expressions.md#e-af3d20fc-fa3b-4485-bcee-8714e4acca9f)
7 | PMS_nAAV_AGE_RDI | (none) | [PMS_ancAGE_RDI_AGE_FROM_INDEX](expressions.md#e-193bb441-a7ab-412f-9d12-ab4247b78d6a)
8 | PMS_nAAV_AGE_SCI | (none) | [PMS_ancAGE_SCI_AGE_FROM_INDEX](expressions.md#e-2ef1c4f5-220d-45a3-860d-d073db59ef9e)
9 | PMS_nAAV_AGE_CCI | (none) | [PMS_ancAGE_CCI_AGE_FROM_INDEX](expressions.md#e-2dbc899c-4c91-45a0-bd93-e02b1456b995)
10 | PMS_nAAV_CND_IRI | (none) | [PMS_ancRES_IRI](expressions.md#e-1d4efdbd-03bf-4bc2-b189-da59dab901ae)
11 | PMS_nAAV_CND_PCRK | (none) | [PMS_ancRES_PCRK](expressions.md#e-0a1d81b8-b54b-490f-9238-9e8cc47b9f96)
12 | PMS_nAAV_CND_RUT | (none) | [PMS_ancCND_Rut](expressions.md#e-4f8cf211-5f31-4d5e-92dd-6f048cf7f6c6)
13 | PMS_nAAV_CND_RSL | (none) | [PMS_ancCND_RSL](expressions.md#e-7fbb09b7-c2ae-4497-8890-e69a5d3999b6)
14 | PMS_tDAV_Rehab_Type | (none) | [PMS_ancOBJ_ABS_Minor](expressions.md#e-8fa0a363-e9d0-4bc7-8324-822d97acb948)
15 | PMS_tDAV_Truck_Load | (none) | [PMS_ancTRF_Truck_Load](expressions.md#e-0a9b6cd0-79b4-4da2-a728-ab165b8fe547)
16 | PMS_nAAV_Yrly_Cost | (none) | [PMS_ancOBJ_AAV_Yrly_Cost_All](expressions.md#e-76d307ed-3427-462f-a79f-e16a387566dd)
17 | PMS_tAAV_FLT_GFP | (none) | [PMS_ancCND_FLT_GFP](expressions.md#e-8696dc20-6bf3-44d2-b7c8-d93b39ae6fc3)
18 | PMS_tAAV_IRI_GFP | (none) | [PMS_ancCND_IRI_GFP](expressions.md#e-ab06bc85-2e62-4269-aeda-d8bd7144b6ad)
19 | PMS_tAAV_PCRK_GFP | (none) | [PMS_ancCND_PCRK_GFP](expressions.md#e-40e28ca8-4605-426b-8c97-7b2c1cc92571)
20 | PMS_tAAV_RUT_GFP | (none) | [PMS_ancCND_RUT_GFP](expressions.md#e-04c76ab6-b287-4c9d-9399-90033e4cc5e7)
21 | PMS_tAAV_MAP21_GFP | (none) | [PMS_ancCND_MAP21_GFP](expressions.md#e-0452c4fb-af93-4324-bc0b-4576e857ae86)
22 | PMS_nDAV_CNT_CHIP_SEALS | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
23 | PMS_nDAV_CNT_MICROSURFACE | (none) | [PMS_ancOBJ_ABS_Zero](expressions.md#e-06981d4e-9242-40ba-b645-98ea62ed4bb3)
24 | PMS_tAAV_YEARLY_TREATMENT | (none) | [PMS_ancRES_Yearly_Treatment](expressions.md#e-ed2f1535-a24f-4156-8dbe-8b5e7dda5f7b)

### Costs

Order | Filter | Financial expression | Economic expression
---: | --- | --- | ---
0 | (none) | [PMS_ancCOST_Minor_HMA_Overlay](expressions.md#e-e2cf5a47-96b8-45f4-8f0a-489a51b76369) | (none)

### Allowed subsequent treatments

Order | Treatment
---: | ---
1 | PMS_PM_Crack_Seal
2 | PMS_PM_Chip_Seal
3 | PMS_PM_Cape_Seal
4 | PMS_PM_Microsurfacing
5 | PMS_PM_Ultra_Thin_Overlay
6 | PMS_Thin_Overlay
7 | PMS_Thick_Overlay
8 | PMS_Reconstruction
9 | PMS_PM_Asphalt
10 | PMS_Preservation
11 | PMS_Fair_Treatment_For_GFP_Analaysis_70P_Good

### Ancillary treatments

Order | Treatment
---: | ---

### Analysis-set membership

- DEL_STIP_2026_DISTRICT_008_NHS_ONLY; row `9316554f-d621-47e7-8593-031311b0ee0d`
- DEL_STIP_2026_DISTRICT_007_NHS_ONLY; row `55febc5b-9de8-4dc7-8f11-198565e485a2`
- DEL_STIP_2026_DISTRICT_004_NHS_ONLY; row `6ac1af67-146c-40df-a1d5-4185365433d2`
- DEL_STIP_2026_DISTRICT_009_NHS_ONLY; row `78e9a930-3e30-490f-9112-51e08313f92d`
- DEL_STIP_2026_DISTRICT_006_NHS_ONLY; row `68d197e5-2035-4453-a246-6400bd9762cd`
- DEL_STIP_2026_NHS_ONLY_NO_INTERSTATE; row `b324b15e-88f1-4c74-99a9-6bddaaabb666`
- DEL_STIP_2026_Non_NHS_ALL_NETWORK; row `a5c521dd-dc2e-411d-831e-7fef851672ad`
- PMS_NON_NHS_NON_TURNPIKE; row `648fe573-d8ab-49bc-80e9-828f9b7c7d35`
- PMS_APD; row `556ab78d-e8e5-41da-800b-85d0a1fb0be2`
- PMS_NHS; row `f54749fc-3e1e-4fd7-b5d1-9e0a06834e39`
- DEL_STIP_2026_DISTRICT_010_NHS_ONLY; row `0547a618-7c88-4c27-84c0-a2223a11053c`
- DEL_STIP_2026_DISTRICT_001_NHS_ONLY; row `ed24e055-05d7-44b2-a533-aaec3730f027`
- DEL_STIP_2026_DISTRICT_002_NHS_ONLY; row `db77cdfb-cb57-4c87-b949-ac57a12611c0`
- DEL_STIP_2026_INTERSTATES_ONLY; row `a87def40-bad5-4b08-80d4-b0806de5bcab`
- PMS_NHS_TENTH; row `0d28eff1-c71f-420f-b161-b85922b32dbc`
- PMS_TURNPIKE; row `4fd6fbd6-98be-48fa-b8ab-bb27ac527416`
- DEL_STIP_2026_DISTRICT_003_NHS_ONLY; row `42770095-0556-4edf-afe7-d33bb8f4df7c`
- DEL_INTERSTATES_2023_10_YEARS; row `aca8c617-7a68-4fca-baa2-d39c40e115be`
- PMS_INTERSTATE; row `0be833c5-82a4-489c-99ae-d666565a9923`
- DEL_STIP_2026_DISTRICT_005_NHS_ONLY; row `60b00c0e-be34-4c94-9141-d8fc17569aec`
- DEL_NonNHS_Routes; row `46877263-87da-4ba2-9dad-e2f8d57e369f`
- DEL_APD_NO_I68_OR_OTHERS_USING_RIDICULOUS_PRICES; row `5897a9ad-aa01-4309-8ac0-ef024f046f0b`

Transitive configuration dependency closure: 1171 records; query `audit_treatment_dependencies`.
