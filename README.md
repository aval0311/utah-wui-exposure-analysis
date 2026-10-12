# Utah WUI exposure and relative wildfire hazard

A geospatial data-science portfolio project connecting a complete ETL pipeline to
county exposure estimates, transparent raster modeling, and an interactive dashboard
for Salt Lake, Utah, and Washington counties.

## Explore

- **[Analysis notebook](notebooks/utah_wui_exposure_analysis.ipynb):** saved results, methods, code, and checks.
- **[Dashboard](docs/index.html):** download the release and open this HTML file in a browser.
- **[Live deployment target](https://aval0311.github.io/utah-wui-exposure-analysis/):** serves v3 after this release is deployed; deployment is not performed by this package.
- **[County results](outputs/tables/county_exposure.csv)** and **[coverage diagnostics](outputs/tables/hazard_coverage.csv)**.
- **[Reproduction guide](data/README.md)** and **[publication handoff](RELEASE_HANDOFF.md)**.

GitHub's notebook preview displays saved figures and tables. Interactive exploration
uses the standalone dashboard. Browser libraries and basemap tiles require internet.

## Questions and contribution

1. Where does mapped high-risk WUI intersect Census block groups?
2. How do estimated population and housing overlap differ between counties?
3. Which facilities intersect or lie near those WUI polygons?
4. How do six environmental indicators combine into a relative hazard surface?
5. What computation-time and memory tradeoff does local parallel processing provide?

The pipeline preserves source snapshots, standardizes identifiers and spatial references,
performs overlap-safe vector analysis, aligns a 30 m raster grid, records missing-data
coverage, validates outputs, and exports a responsive Folium dashboard. Xarray and
rioxarray retain grid coordinates; Dask parallelizes the final composite with local workers.

## Results from the accepted release

<!-- RELEASE_RESULTS_START -->
Accepted snapshot run: **20261012T180540Z_eb3fdcb7**, completed **2026-10-12 UTC**.
This summary is synchronized from exported tables; new execution results appear later in the notebook.

| County | Estimated residents in mapped WUI | Estimated housing units | Share of county population |
|---|---:|---:|---:|
| Salt Lake | 4,552 | 1,523 | 0.38% |
| Utah | 6,464 | 1,640 | 0.92% |
| Washington | 8,176 | 3,770 | 4.16% |

Washington County has the largest estimated exposed population and the highest share of county residents within mapped WUI. These area-weighted estimates describe mapped WUI overlap, not population within a modeled hazard class.

The study footprint totals **13,927.71 km²**.

| Coverage category | Study area (%) |
|---|---:|
| Confirmed nonburnable (excluded by policy) | 17.10 |
| Missing or unrecognized FBFM40 class | 0.00 |
| Burnable: insufficient NDVI or NDMI observations | 2.59 |
| Burnable: missing another required component | 0.16 |
| Valid modeled burnable land | 80.15 |

County panels are polygon-masked. Nonburnable land and missing observations have separate exclusion categories.

Sensitivity uses **13,591** modeled sample pixels.

- Equal weights: **85.27%** class agreement; top-quintile Jaccard **0.631**.
- Half history influence, renormalized: **88.14%** class agreement; top-quintile Jaccard **0.867**.

These comparisons assess stability under assumed weights.

Historical selection retained **20,853 recorded wildfires** in the density rectangle, including **4,689 inside the county polygons**. Prescribed fires are excluded.

This complete snapshot run took **24.1 minutes**, measured from configuration through input verification, processing, and snapshot-inventory finalization. This single functional-validation timing is separate from the retained composite benchmark.

<!-- RELEASE_RESULTS_END -->

![County exposure](images/county_exposure.png)
![Relative hazard by county](images/hazard_overview.png)

## Methods and interpretation

Spatial analysis uses EPSG:26912. Population and housing estimates allocate 2024 ACS
five-year values by mapped WUI overlap with 2020 block groups. This assumes uniform
density within a block group; allocated margins of error omit spatial-allocation uncertainty.
Facility proximity is Euclidean distance. The one-mile screening flag is a project rule,
and popup demographic values describe the containing block group.

The relative score combines fuels (30%), vegetation dryness (20%), slope (15%), aspect
(10%), historical wildfire occurrence (15%), and human-activity indicators (10%).
The notebook explains transformations, thresholds, and rationale beside each phase.
These are explicit project assumptions. The continuous index is 1 + 9 × normalized score;
fixed boundaries at 0.2, 0.4, 0.6, and 0.8 define five descriptive classes.

Recorded InFORM wildfires are filtered to IncidentTypeCategory=WF, with discovery dates
from 1992-01-01 inclusive to 2026-09-30 exclusive (UTC). A documented bounding rectangle
retains surrounding events for density smoothing; actual county counts are reported separately.
Source vintages differ. This release provides a relative screening analysis rather than
calibrated probabilities of ignition, loss, or fire behavior.

## Quality and limitations

Checks cover geometry, joins, exact raster alignment, input checksums, temporal support,
nonburnable exclusions, coverage reconciliation, component formulas, and serial/Dask agreement.
See [current release evidence](evidence/release_validation.json) for completed checks and their scope.

- Confirmed nonburnable and incomplete cells are excluded for different reasons.
- HLS sampling and quality masks leave some burnable land without sufficient observations.
- MTBS perimeters are unavailable in this snapshot. The retained 60/40 history formulation
  assigns zero to the missing perimeter term and caps the component at 0.60.
- The canonical mask differs from independent county reconstruction at 208 cells (0.1872 km²
  in the retained footprint). Its original cause is unresolved; each run measures the difference.
- Infrastructure records can be incomplete or imprecise; shelter points do not establish
  operating status. Historical fire reporting is incomplete and varies over time.
- Weight sensitivity assesses stability. Predictive accuracy has not been established for this index.

![County coverage](images/county_coverage_diagnostics.png)

## Reproduce the analysis

Keep the notebook with src/, scripts/, and the environment specification. If the tested
wui-professional-314 environment already exists, activate it and select its kernel in JupyterLab.
To create the environment on another compatible machine:

    mamba env create -f environment.yml
    mamba activate wui-professional-314
    python -m ipykernel install --user --name wui-professional-314
    jupyter lab

Extract **wui-snapshot-publication-v3.zip** into a separate writable workspace. Set
WUI_PROJECT_ROOT before starting Jupyter, or set PROJECT_ROOT_OVERRIDE in the configuration
cell. Restart the kernel and run all cells. Full steps and checksum verification are in the
[data guide](data/README.md). Saved outputs and the dashboard can be reviewed without the snapshot.

Defaults are DATA_MODE="snapshot", REBUILD_DERIVED=False, and HPC_ENGINE="dask".
Snapshot execution uses retained sources and frozen responses. Refresh intentionally reacquires
sources and requires a Census API key through an environment variable or hidden prompt.
Rebuilding derivatives uses the selected acquisition mode and never silently enables downloads.
The snapshot network guard applies to the notebook kernel's Python socket calls; it is not an
operating-system or worker-process firewall.

Four local workers have a 4 GiB limit each. The client and upstream arrays need additional RAM;
the validated machine has approximately 32 GiB. Worker count and chunk size are configurable.
Allow space for the approximately 27 GB archive, extraction, derived products, and new outputs.
Preserve the downloaded archive as the immutable starting copy.

Each execution writes a unique outputs/publication/RUN_ID/ directory in the selected workspace.
After an accepted execution, export that run to update the package's dashboard, figures,
tables, notebook opening summary, and README together:

    python scripts/export_publication.py /path/to/workspace --run /path/to/workspace/outputs/publication/RUN_ID

Run current equivalence and browser checks before replacing release evidence. Recreate
release checksums after changes. Running notebook cells alone does not rewrite the
accepted-run summaries in the opening Markdown or README.

## Parallel-processing evidence

A retained matched experiment used identical frozen composite inputs, one warm-up, and five
measured runs per configuration. It predates v3's wildfire-only source selection.

| Configuration | Median compute/export | Median peak process-tree RSS |
|---|---:|---:|
| Rasterio/NumPy | 38.711 s | 2.960 GiB |
| Dask, 1 worker, 1024 × 1024 | 65.282 s | 2.268 GiB |
| Dask, 4 workers, 1024 × 1024 | 22.559 s | 5.252 GiB |
| Dask, 4 workers, 2048 × 2048 | 17.673 s | 5.510 GiB |

The selected configuration achieved **2.19× compute/export speedup**, or **1.90× including
cluster startup and teardown**, using approximately **1.86× memory**. All 96 retained output
comparisons passed. These warm-cache, local-host measurements apply to the recorded composite
workload. Upstream ETL remains conventional Python GIS; multi-node scaling is future work.
The [protocol](evidence/step4_report.txt) and [measurements](evidence/benchmark_summary.json)
document timing boundaries, hardware, and sampling limitations. Current equivalence evidence
is separate from that historical experiment.

## Planned machine-learning extension

Estimate the probability of **at least one new recorded wildfire ignition within a defined
geographic unit during a specified future period**. Resolution and forecast horizon will be
chosen after evaluating event frequency, source accuracy, and data availability. Development
will require multi-year, time-aligned predictors available at forecast issue time, observed
outcomes, appropriate no-recorded-ignition samples, calibration, and comparisons with simple
baselines. Evaluation will withhold future periods and geographic areas. The current weighted
score is not a training label. This capability is planned and is not implemented in this release.

## Package layout

- notebooks/: executed analysis and narrative.
- src/wui/: runtime, analytical helpers, parallel computation, validation, and publication support.
- scripts/: regression checks and publication export.
- data/: matching snapshot inventory, checksum, and acquisition guide.
- images/ and outputs/tables/: accepted-run figures and tables.
- docs/index.html: interactive dashboard for GitHub Pages.
- evidence/: current validation and explicitly retained historical evidence.

Original code and documentation use the [MIT License](LICENSE). Third-party datasets retain
their providers' terms and attribution requirements.
