# Snapshot data and reproducibility

This release uses **wui-snapshot-publication-v3.zip**, distributed separately from the code
package. Extract its data/ directory and snapshot_manifest.json into the same writable
workspace. The v1 archive alone does not carry the strengthened v3 integrity contract or
the matching rebuilt products.

**Public snapshot download:** pending the maintainer's upload. The adjacent
snapshot_download.json identifies the matching archive, size, and SHA-256. Saved notebook
outputs and the dashboard can be reviewed without downloading analytical inputs.

## Verify and execute

With the release environment active, verify the extracted workspace:

    python scripts/check_snapshot.py /path/to/workspace

Open the notebook from the complete code package. Select the tested kernel, set
PROJECT_ROOT_OVERRIDE to the extracted workspace (or set WUI_PROJECT_ROOT before
starting Jupyter), retain DATA_MODE="snapshot", restart the kernel, and run all cells.
The configuration follows the project overview rather than occupying the opening cell.

The notebook verifies input hashes and the analytical recipe before processing.
Required source checks explicitly include the ACS numerical CSV and InFORM GeoJSON,
alongside Census geometry, raster/archive sources, immutable service responses, and
the canonical study mask. A changed source fails even when REBUILD_DERIVED=True.
Only metadata with localized file paths is excluded from byte-level comparison.

The data workspace is writable. Intermediate metadata and derived rasters can be regenerated;
a unique run directory separates final outputs. Preserve the original archive as an immutable
starting point. The notebook kernel blocks external Python socket connections in snapshot
mode while allowing local Jupyter/Dask communication. This is not a worker or operating-system
firewall. Dashboard libraries and basemap tiles require internet.

## Retained inputs

| Source | Retained material | Role |
|---|---|---|
| Census and ACS | 2020 block-group GeoPackage; 2024 ACS numerical CSV and responses | Demographic exposure |
| Utah counties and WUI | Frozen service responses | Study area and WUI overlap |
| Facilities | Candidate inventories, requested IDs, and source responses | Facility proximity |
| HLS 2.0 | 2025 STAC records, retained bands, masks, indices, counts, and derivatives | Vegetation condition |
| LANDFIRE LF2025 | Source fuel/canopy products and aligned derivatives | Fuel proxy and nonburnable policy |
| USGS 3DEP | Frozen 148-record catalog, DEM tiles, and aligned terrain | Slope and aspect |
| InFORM | Immutable occurrence GeoJSON, including source event categories | Wildfire-only analytical selection |
| TIGER roads and Annual NLCD | Retained vector/raster sources | Human-activity proxies |
| Canonical study mask | Versioned binary footprint | Stable coverage denominator |

Prescribed-fire records remain in the unmodified source archive for provenance. The
analytical selection retains only WF records within the explicit discovery-date period
and density rectangle. The exported selection ledger reconciles exclusions and reports
actual county counts separately.

## Refresh and rebuild

DATA_MODE="refresh" intentionally reacquires source data. The Census API key comes from
CENSUS_API_KEY or a hidden prompt. Refresh is not required to reproduce this release and
can change source availability or results. Review revised observation periods and source
vintages before accepting a new release; the historical selection dates are explicit in
the historical-fire phase.

REBUILD_DERIVED=True in snapshot mode recomputes intermediates without live downloads.
Ordinary snapshot execution rejects a changed analytical recipe. A source-footprint or
observation-period extension requires a corresponding source acquisition and new snapshot.
The final manifest records source hashes and resolved stage settings after a completed run.

The terrain catalog accepts only a maximum 0.00001-degree variation per recomputed query
bound; larger extent changes require a new source catalog. Grid and coverage checks remain
mandatory. The canonical boundary discrepancy is disclosed in the notebook limitations.

## Distribution

Keep this large archive outside ordinary Git history. Upload it to a suitable data host,
retain the exact filename and checksum, and place the direct URL in snapshot_download.json
and this guide. Replace the pending-download notice only after verifying public access.
Provider terms and attribution requirements remain attached to their data.
