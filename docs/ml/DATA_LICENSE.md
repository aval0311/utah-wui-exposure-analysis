# License and attribution

The [MIT license](LICENSE) applies to Adam Valentino's original code and documentation in this package. It does not replace third-party data terms. No provider logos, raw incident records, terrain tiles, boundary-service response or climate NetCDF files are bundled.

The map images, aggregate result tables and development cell-year attributes are project analysis outputs. Cite this project and acknowledge the underlying sources when reusing them. Maps use the derived county-clipped grid and no external basemap tiles. Included attributes use stable cell-year IDs, not named incident records.

## Source-specific notes

- **USGS 3DEP:** the [program page](https://www.usgs.gov/3d-elevation-program) states that 3DEP products are available without use restrictions. Credit U.S. Geological Survey. The program's statement does not license unrelated third-party material.
- **Utah county boundaries:** the [SGID dataset page](https://gis.utah.gov/products/sgid/boundaries/county/) states that the dataset has no use constraints or warranties and encourages attribution to State of Utah, SGID. The administrative boundaries do not represent exact legal boundaries.
- **gridMET:** the [provider documentation](https://www.climatologylab.org/gridmet.html) describes John Abatzoglou's waiver of copyright and related rights to the extent possible under law. Credit gridMET and the Abatzoglou (2013) paper identified in the source guide.
- **NIFC InFORM:** credit NIFC and contributing reporting agencies. The public layer metadata has an empty copyright field; this package does not treat that as a blanket license. Raw InFORM records are not redistributed here. Consult the [source service](https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/InFORM_FireOccurrence_Public/FeatureServer) when obtaining source records.

These notes document provider statements checked October 16, 2026 and the material actually distributed. They do not grant rights to unbundled source archives. Python, Jupyter and ReportLab are optional external tools and are not vendored in this release.
