# dTIMS Pavement Family Deterioration Coefficients

Source: `Analysis_Lookup_Perf_Coef` table from WVDOT dTIMS CT server
Total: **144 coefficient rows** across **18 families** and **8 indices**

## Family Key Structure

```
{PaveType}_{RehabType}_{TruckLoad}
```

| Component | Values | Description |
|-----------|--------|-------------|
| PaveType | BC, RC, OT | Bituminous Concrete, Rigid Concrete, Other |
| RehabType | Initial, Minor, Major | Last treatment category applied |
| TruckLoad | H, L | High (coal route or truck% >= 10%), Low |

## Curve Type Formulas

| Curve Type | Value | Formula | Count |
|------------|-------|---------|-------|
| Polynomial | 3 | `Index = Max + C1*age + C2*age^2` | 137 |
| Linear | 1 | `Index = Max + C1*age` | 3 |
| Sigmoid | 5 | `Index = Max - C1 * EXP(-(C2/age)^C3)` | 3 |
| Log | 2 | `Index = Max - EXP(C1 + C2 * C3^LOG(1/age))` | 1 |

## Condition Indices

| Code | Full Name |
|------|-----------|
| CCI | Composite |
| CSI | Concrete Slab |
| ECI | Enviornmental Cracking |
| JCI | Joint Condition |
| NCI | Net Cracking |
| PSI | Pavement Serviceability |
| RDI | Rut Depth |
| SCI | Structural Cracking |

## Asphalt (Bituminous Concrete) (BC) Families

### BC_Initial_H
Pavement: **BC** | Rehab: **Initial** | Truck: **H**

| Index | Curve Type | C1 | C2 | C3 | Formula |
|-------|------------|-----|-----|-----|---------|
| CCI | Polynomial | 0.0 | -0.005 | 0.0 | `5 + -0.005*age^2` |
| CSI | Polynomial | 0.0 | -0.005 | 0.0 | `5 + -0.005*age^2` |
| ECI | Polynomial | 0.0 | -0.004 | 0.0 | `5 + -0.004*age^2` |
| JCI | Polynomial | 0.0 | -0.003 | 0.0 | `5 + -0.003*age^2` |
| NCI | Polynomial | 0.0 | -0.005 | 0.0 | `5 + -0.005*age^2` |
| PSI | Polynomial | 0.0 | -0.005 | 0.0 | `5 + -0.005*age^2` |
| RDI | Polynomial | 0.0 | -0.004 | 0.0 | `5 + -0.004*age^2` |
| SCI | Sigmoid | 85.0 | 115.0 | 0.7 | `5 - 85.0*EXP(-(115.0/age)^0.7)` |

### BC_Initial_L
Pavement: **BC** | Rehab: **Initial** | Truck: **L**

| Index | Curve Type | C1 | C2 | C3 | Formula |
|-------|------------|-----|-----|-----|---------|
| CCI | Polynomial | 0.0 | -0.004 | 0.0 | `5 + -0.004*age^2` |
| CSI | Polynomial | 0.003 | -0.004 | 0.0 | `5 + 0.003*age + -0.004*age^2` |
| ECI | Sigmoid | 85.0 | 120.0 | 0.6 | `5 - 85.0*EXP(-(120.0/age)^0.6)` |
| JCI | Polynomial | 0.019 | -0.003 | 0.0 | `5 + 0.019*age + -0.003*age^2` |
| NCI | Polynomial | 0.0 | -0.003 | 0.0 | `5 + -0.003*age^2` |
| PSI | Polynomial | 0.0 | -0.004 | 0.0 | `5 + -0.004*age^2` |
| RDI | Polynomial | 0.0 | -0.004 | 0.0 | `5 + -0.004*age^2` |
| SCI | Polynomial | 0.0 | -0.003 | 0.0 | `5 + -0.003*age^2` |

### BC_Major_H
Pavement: **BC** | Rehab: **Major** | Truck: **H**

| Index | Curve Type | C1 | C2 | C3 | Formula |
|-------|------------|-----|-----|-----|---------|
| CCI | Polynomial | 0.0 | -0.006 | 0.0 | `5 + -0.006*age^2` |
| CSI | Sigmoid | 85.0 | 115.0 | 0.7 | `5 - 85.0*EXP(-(115.0/age)^0.7)` |
| ECI | Polynomial | 0.0 | -0.005 | 0.0 | `5 + -0.005*age^2` |
| JCI | Polynomial | 0.0 | -0.003 | 0.0 | `5 + -0.003*age^2` |
| NCI | Polynomial | 0.0 | -0.005 | 0.0 | `5 + -0.005*age^2` |
| PSI | Polynomial | 0.0 | -0.005 | 0.0 | `5 + -0.005*age^2` |
| RDI | Polynomial | 0.0 | -0.003 | 0.0 | `5 + -0.003*age^2` |
| SCI | Polynomial | 0.0 | -0.006 | 0.0 | `5 + -0.006*age^2` |

### BC_Major_L
Pavement: **BC** | Rehab: **Major** | Truck: **L**

| Index | Curve Type | C1 | C2 | C3 | Formula |
|-------|------------|-----|-----|-----|---------|
| CCI | Polynomial | 0.0 | -0.013 | 0.0 | `5 + -0.013*age^2` |
| CSI | Polynomial | 0.0 | -0.02 | 0.0 | `5 + -0.02*age^2` |
| ECI | Polynomial | 0.0 | -0.007 | 0.0 | `5 + -0.007*age^2` |
| JCI | Log | 3.1 | -11.5 | 1.7 | `5 - EXP(3.1 + -11.5*1.7^LOG(1/age))` |
| NCI | Polynomial | 0.0 | -0.014 | 0.0 | `5 + -0.014*age^2` |
| PSI | Polynomial | 0.0 | -0.012 | 0.0 | `5 + -0.012*age^2` |
| RDI | Polynomial | 0.0 | -0.004 | 0.0 | `5 + -0.004*age^2` |
| SCI | Polynomial | 0.0 | -0.014 | 0.0 | `5 + -0.014*age^2` |

### BC_Minor_H
Pavement: **BC** | Rehab: **Minor** | Truck: **H**

| Index | Curve Type | C1 | C2 | C3 | Formula |
|-------|------------|-----|-----|-----|---------|
| CCI | Polynomial | 0.0 | -0.007 | 0.0 | `5 + -0.007*age^2` |
| CSI | Polynomial | 0.008 | -0.007 | 0.0 | `5 + 0.008*age + -0.007*age^2` |
| ECI | Polynomial | 0.0 | -0.006 | 0.0 | `5 + -0.006*age^2` |
| JCI | Polynomial | 0.004 | -0.003 | 0.0 | `5 + 0.004*age + -0.003*age^2` |
| NCI | Polynomial | 0.0 | -0.008 | 0.0 | `5 + -0.008*age^2` |
| PSI | Polynomial | 0.0 | -0.007 | 0.0 | `5 + -0.007*age^2` |
| RDI | Polynomial | 0.0 | -0.004 | 0.0 | `5 + -0.004*age^2` |
| SCI | Polynomial | 0.0 | -0.007 | 0.0 | `5 + -0.007*age^2` |

### BC_Minor_L
Pavement: **BC** | Rehab: **Minor** | Truck: **L**

| Index | Curve Type | C1 | C2 | C3 | Formula |
|-------|------------|-----|-----|-----|---------|
| CCI | Polynomial | 0.0 | -0.006 | 0.0 | `5 + -0.006*age^2` |
| CSI | Polynomial | 0.0 | -0.006 | 0.0 | `5 + -0.006*age^2` |
| ECI | Polynomial | 0.0 | -0.006 | 0.0 | `5 + -0.006*age^2` |
| JCI | Polynomial | 0.0 | -0.003 | 0.0 | `5 + -0.003*age^2` |
| NCI | Polynomial | 0.0 | -0.01 | 0.0 | `5 + -0.01*age^2` |
| PSI | Polynomial | 0.0 | -0.005 | 0.0 | `5 + -0.005*age^2` |
| RDI | Polynomial | 0.0 | -0.004 | 0.0 | `5 + -0.004*age^2` |
| SCI | Polynomial | 0.0 | -0.009 | 0.0 | `5 + -0.009*age^2` |

## Rigid Concrete (RC) Families

### RC_Initial_H
Pavement: **RC** | Rehab: **Initial** | Truck: **H**

| Index | Curve Type | C1 | C2 | C3 | Formula |
|-------|------------|-----|-----|-----|---------|
| CCI | Polynomial | 0.0 | -0.004 | 0.0 | `5 + -0.004*age^2` |
| CSI | Polynomial | 0.0 | -0.005 | 0.0 | `5 + -0.005*age^2` |
| ECI | Polynomial | 0.0 | -0.002 | 0.0 | `5 + -0.002*age^2` |
| JCI | Polynomial | 0.0 | -0.003 | 0.0 | `5 + -0.003*age^2` |
| NCI | Polynomial | 0.0 | -0.003 | 0.0 | `5 + -0.003*age^2` |
| PSI | Polynomial | 0.0 | -0.004 | 0.0 | `5 + -0.004*age^2` |
| RDI | Polynomial | 0.0 | -0.002 | 0.0 | `5 + -0.002*age^2` |
| SCI | Polynomial | 0.0 | -0.003 | 0.0 | `5 + -0.003*age^2` |

### RC_Initial_L
Pavement: **RC** | Rehab: **Initial** | Truck: **L**

| Index | Curve Type | C1 | C2 | C3 | Formula |
|-------|------------|-----|-----|-----|---------|
| CCI | Polynomial | 0.0 | -0.004 | 0.0 | `5 + -0.004*age^2` |
| CSI | Polynomial | 0.004 | -0.005 | 0.0 | `5 + 0.004*age + -0.005*age^2` |
| ECI | Polynomial | 0.0 | -0.002 | 0.0 | `5 + -0.002*age^2` |
| JCI | Polynomial | 0.009 | -0.003 | 0.0 | `5 + 0.009*age + -0.003*age^2` |
| NCI | Polynomial | 0.0 | -0.003 | 0.0 | `5 + -0.003*age^2` |
| PSI | Polynomial | 0.0 | -0.004 | 0.0 | `5 + -0.004*age^2` |
| RDI | Polynomial | 0.0 | -0.002 | 0.0 | `5 + -0.002*age^2` |
| SCI | Polynomial | 0.015 | -0.003 | 0.0 | `5 + 0.015*age + -0.003*age^2` |

### RC_Major_H
Pavement: **RC** | Rehab: **Major** | Truck: **H**

| Index | Curve Type | C1 | C2 | C3 | Formula |
|-------|------------|-----|-----|-----|---------|
| CCI | Polynomial | 0.0 | -0.004 | 0.0 | `5 + -0.004*age^2` |
| CSI | Polynomial | 0.0 | -0.006 | 0.0 | `5 + -0.006*age^2` |
| ECI | Polynomial | 0.0 | -0.003 | 0.0 | `5 + -0.003*age^2` |
| JCI | Polynomial | 0.0 | -0.003 | 0.0 | `5 + -0.003*age^2` |
| NCI | Polynomial | 0.0 | -0.006 | 0.0 | `5 + -0.006*age^2` |
| PSI | Polynomial | 0.0 | -0.004 | 0.0 | `5 + -0.004*age^2` |
| RDI | Polynomial | 0.0 | -0.003 | 0.0 | `5 + -0.003*age^2` |
| SCI | Polynomial | 0.0 | -0.006 | 0.0 | `5 + -0.006*age^2` |

### RC_Major_L
Pavement: **RC** | Rehab: **Major** | Truck: **L**

| Index | Curve Type | C1 | C2 | C3 | Formula |
|-------|------------|-----|-----|-----|---------|
| CCI | Polynomial | 0.0 | -0.004 | 0.0 | `5 + -0.004*age^2` |
| CSI | Polynomial | 0.004 | -0.006 | 0.0 | `5 + 0.004*age + -0.006*age^2` |
| ECI | Polynomial | 0.0 | -0.007 | 0.0 | `5 + -0.007*age^2` |
| JCI | Polynomial | 0.011 | -0.003 | 0.0 | `5 + 0.011*age + -0.003*age^2` |
| NCI | Polynomial | 0.0 | -0.009 | 0.0 | `5 + -0.009*age^2` |
| PSI | Polynomial | 0.0 | -0.003 | 0.0 | `5 + -0.003*age^2` |
| RDI | Polynomial | 0.0 | -0.005 | 0.0 | `5 + -0.005*age^2` |
| SCI | Polynomial | 0.0 | -0.007 | 0.0 | `5 + -0.007*age^2` |

### RC_Minor_H
Pavement: **RC** | Rehab: **Minor** | Truck: **H**

| Index | Curve Type | C1 | C2 | C3 | Formula |
|-------|------------|-----|-----|-----|---------|
| CCI | Linear | -0.1 | 0.0 | 0.0 | `5 + -0.1*age` |
| CSI | Polynomial | 0.002 | -0.006 | 0.0 | `5 + 0.002*age + -0.006*age^2` |
| ECI | Polynomial | 0.0 | -0.008 | 0.0 | `5 + -0.008*age^2` |
| JCI | Polynomial | 0.0 | -0.003 | 0.0 | `5 + -0.003*age^2` |
| NCI | Polynomial | 0.0 | -0.009 | 0.0 | `5 + -0.009*age^2` |
| PSI | Linear | -0.1 | 0.0 | 0.0 | `5 + -0.1*age` |
| RDI | Polynomial | 0.0 | -0.005 | 0.0 | `5 + -0.005*age^2` |
| SCI | Polynomial | 0.0 | -0.008 | 0.0 | `5 + -0.008*age^2` |

### RC_Minor_L
Pavement: **RC** | Rehab: **Minor** | Truck: **L**

| Index | Curve Type | C1 | C2 | C3 | Formula |
|-------|------------|-----|-----|-----|---------|
| CCI | Polynomial | 0.0 | -0.005 | 0.0 | `5 + -0.005*age^2` |
| CSI | Polynomial | 0.0 | -0.006 | 0.0 | `5 + -0.006*age^2` |
| ECI | Polynomial | 0.0 | -0.003 | 0.0 | `5 + -0.003*age^2` |
| JCI | Linear | -0.1 | 0.0 | 0.0 | `5 + -0.1*age` |
| NCI | Polynomial | 0.0 | -0.004 | 0.0 | `5 + -0.004*age^2` |
| PSI | Polynomial | 0.0 | -0.004 | 0.0 | `5 + -0.004*age^2` |
| RDI | Polynomial | 0.0 | -0.004 | 0.0 | `5 + -0.004*age^2` |
| SCI | Polynomial | 0.0 | -0.003 | 0.0 | `5 + -0.003*age^2` |

## Other (OT) Families

All OT families have zero coefficients (no deterioration modeled).

## Notes

- All indices use a 0-5 scale where 5 = best condition
- Maximum (initial value) is 5.0 for all curves
- Most polynomial curves have C1=0 (pure quadratic decay: `5 + C2*age^2` with C2 negative)
- Some polynomial curves have positive C1 (slight initial improvement before decay)
- Sigmoid (Weibull) curves model delayed onset deterioration (stays near 5 then drops)
- Linear curves produce constant annual deterioration (C1 per year)
- OT (Other) families have all-zero coefficients; no deterioration is modeled
- NCI (Network Condition Index) is labeled 'Not Predicted' in dTIMS equations
- CCI has its own independent curve per family (dTIMS does not compute CCI as MIN)
