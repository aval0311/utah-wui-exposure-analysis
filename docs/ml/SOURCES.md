# Sources and historical availability

The release uses retained snapshots. The metadata review on October 16, 2026 checked source documentation; it did not refresh incident records or climate observations. [Source provenance](data/source_provenance.json) records the source file hashes, copied assets and presentation transformations.

| Source | Role and retained vintage | Interpretation |
| --- | --- | --- |
| NIFC InFORM public fire-occurrence layer | Primary recorded-wildfire label source, retained with the October 2026 baseline; only reviewed 2001–2021 labels support this release | Discovery-date cell-years; no-record labels are not verified absences. Status and source-system changes around 2020 cannot separate reporting changes from real fire variation. |
| State of Utah, SGID county boundaries | County service response acquired October 15, 2026; fixed three-county footprint in EPSG:26912 | Administrative study boundaries; county-clipped area varies. This is not a reconstruction of historical boundaries. |
| USGS 3DEP / National Elevation Dataset 1 arc-second | Retained 148-item catalog acquired October 15, 2026; aligned 30 m elevation, slope and aspect | Catalog publication dates span 2013–2026 and do not establish observation dates. Contemporary terrain is a static historical proxy. |
| John T. Abatzoglou, gridMET | Retrospective subset archive completed October 16, 2026; source days October 1, 1999 through September 30, 2020 | Supports target years 2001–2021 with pre-cutoff windows and an assumed 60-day release lag. Historical as-issued versions are unverified. |

The six climate features summarize precipitation, mean temperature and vapor-pressure deficit over the antecedent October–September year and July–September season. Area-weighted native climate-pixel intersections are used. The model does not acquire target-year weather. Neither the conservative lag nor a current archive proves what was available at every historical cutoff.

Public FPA FOD and agency/dispatch material used during reconciliation provide supporting checks, not a replacement primary label source or complete independent reporting census. Reporting participation was not obtained from all agencies. The final decision retains known reviewed labels, including flagged zeros, in training and calibration and excludes the frozen 155 flagged zeros from evaluation. There are 231 unknown development exclusions, of which 230 fall in the mapped years.

## Source citations

- [NIFC InFORM public layer metadata](https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/InFORM_FireOccurrence_Public/FeatureServer/0) identifies the incident fields. [NIFC reporting-system documentation](https://www.nifc.gov/programs/information-technology) explains InFORM, IRWIN and upstream reporting workflows; it does not establish completeness in this study.
- [State of Utah, SGID county boundaries](https://gis.utah.gov/products/sgid/boundaries/county/) identifies UGRC and the Lieutenant Governor's Office as stewards. Credit: State of Utah, SGID.
- [USGS 3D Elevation Program](https://www.usgs.gov/3d-elevation-program). Credit: U.S. Geological Survey. See the retained [terrain policy](data/terrain_policy.json) for transformations and the static-terrain assumption.
- Abatzoglou, J. T. (2013). Development of gridded surface meteorological data for ecological applications and modelling. International Journal of Climatology, 33, 121–131. [gridMET documentation and citation](https://www.climatologylab.org/gridmet.html); DOI 10.1002/joc.3413. The documentation identifies recent values as preliminary and describes the approximate 4 km spatial support.

Raw source archives are not included. The release contains original analysis summaries, cell-year prediction attributes, maps and selected provenance. [License and attribution notes](DATA_LICENSE.md) distinguish the project's material from source-provider conditions.
