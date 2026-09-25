# Data

This repository does not include the complete raw, cached, intermediate, or processed geospatial datasets used by the analysis. The full workflow produces multiple gigabytes of raster and vector data, and several source datasets are maintained by external organizations.

The project notebook documents the source URLs, dataset versions, acquisition methods, local cache structure, validation rules, and processing steps required to reproduce the analysis.

## Publication Data Modes

The published notebook uses the following reproducibility-focused settings:

```python
census_geography_data_mode = "snapshot"
acs_data_mode = "snapshot"
fire_hazard_data_mode = "snapshot"
```

The `census_geography_data_mode = "snapshot"` setting loads the validated 2020 Census county and block-group boundaries used for the published analysis.

The `acs_data_mode = "snapshot"` setting loads the validated 2024 ACS 5-Year processed population and housing table used for the published analysis.

The `fire_hazard_data_mode = "snapshot"` setting reuses the validated fire-hazard source data and derived products used for the published analysis.

These settings prevent the published results from changing automatically when an upstream source is updated.

## Refreshing the Data

To intentionally update the analysis, use:

```python
census_geography_data_mode = "refresh"
acs_data_mode = "refresh"
fire_hazard_data_mode = "refresh"
```

The three refresh modes perform the following actions:

- `census_geography_data_mode = "refresh"` reacquires the required 2020 Census county and block-group boundaries.
- `acs_data_mode = "refresh"` requests the configured ACS population and housing variables. This mode requires a U.S. Census API key.
- `fire_hazard_data_mode = "refresh"` reacquires and rebuilds the configured environmental and fire-hazard source datasets and derived products. This mode may require substantial download time, processing time, disk space, and memory.

Refresh operations may change the analytical results. After refreshing the data, run the complete notebook, review all validation results, and document the new dataset versions.

## Primary Data Sources

| Analytical role | Dataset | Provider |
|---|---|---|
| Census geography | 2020 Census Block Groups | U.S. Census Bureau |
| Demographics | 2024 ACS 5-Year population and housing estimates | U.S. Census Bureau |
| Administrative boundaries | Utah county boundaries | Utah GIS |
| WUI exposure | Utah High-Risk WUI polygons | Utah GIS |
| Critical facilities | Hospitals, fire stations, law enforcement facilities, public schools, and emergency shelters | Utah GIS and FEMA |
| Vegetation condition | HLS L30/S30 Version 2.0, July–September 2025 | NASA and Microsoft Planetary Computer |
| Surface and canopy fuels | LF2025 FBFM40, canopy cover, and canopy bulk density | LANDFIRE |
| Terrain | USGS 3DEP 1 arc-second digital elevation model | U.S. Geological Survey |
| Historical fire | InFORM FODR fire-occurrence records; optional MTBS burned-area boundaries were unavailable during the publication run | NIFC, USFS, and USGS |
| Human ignition indicators | 2025 TIGER/Line roads and Annual NLCD 2025 land cover | U.S. Census Bureau and MRLC |

## Data Licensing

All source datasets remain subject to the licenses, terms, attribution requirements, and usage policies of their respective publishers. The [MIT License](../LICENSE) applies only to the original code and documentation in this repository and does not relicense external data.
