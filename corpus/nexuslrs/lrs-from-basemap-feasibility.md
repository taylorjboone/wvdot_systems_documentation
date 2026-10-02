# LRS From Base Map: A Feasibility Study

**Author:** Bennett Murphy
**Date:** 2023-07-04

Can LRS operations run directly against vector-tile basemap data instead of hitting REST services? This study says yes.

## Concepts
- **Basemaps** — default map layers made of raster/image tiles organized by x, y, z (z = zoom).
- **Vector tiles** — GIS data as vector graphics, not raster. With vector tiles, "you can act with the data making up the basemap super easy" since the DOT's data is already embedded.

## Accuracy Test
Tested three core LRS operations with a custom Go program — 10,000 random point operations per tile across zoom levels:
- Point → RouteID/Measure
- RouteID/Measure → Point
- RouteID/BMP/EMP → Line

**Result:** Zoom 14 tiles achieved **~4 ft average error** — matching the "1.9 ft/pixel resolution."

## Implementation
Tiles built with a custom branch of a Go library that correctly handles geometry-based properties during clipping. Full West Virginia basemap tile set grew from **117 MB → 150 MB** — an acceptable tradeoff.

## Conclusion
LRS operations work reliably from client-side vector-tile data, potentially removing the API dependency for many standard operations.
