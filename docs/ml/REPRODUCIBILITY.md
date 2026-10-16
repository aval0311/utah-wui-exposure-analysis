# Reproducing the presentation

## Offline viewing and integrity

Open `index.html` after extracting the complete folder. It has no scripts, remote fonts, tracking, fetched data or CDN dependencies. Maps, text descriptions and county summaries are included locally. The PDF and notebook provide alternative views. External citation links are optional.

Python 3.10 or later is sufficient for the viewer. `python -I -S viewer.py --verify` checks every manifest-listed file against SHA-256 and size. `python -I -S viewer.py --build` deterministically rebuilds the HTML from included text, metadata and map descriptions. Both commands locate inputs relative to the script, so they work from another current directory. No packages need installing and no data are downloaded.

## Optional notebook and atlas rebuilding

Open `wui_ml_v1_snapshot.ipynb` with an ordinary Python Jupyter kernel. Keep the notebook in the release folder and retain `DATA_MODE = "snapshot"`. Its code imports only Python standard-library modules and IPython display helpers. It reads local saved tables, verifies hashes and embeds the nine maps; it performs no inference or fitting. Use JupyterLab and ipykernel in a separate environment if they are not already installed. See [tested viewer versions](data/viewer_environment.json); these are a test record, not requirements for viewing HTML.

The optional PDF builder is `tools/build_atlas.py`. It uses ReportLab 4.4.9 and the included images and descriptions. Run `python tools/build_atlas.py` in an environment containing ReportLab. The atlas is deterministic under the tested runtime. The HTML has semantic headings, meaningful image descriptions and native tables. The PDF adds searchable text to every page but is not certified as tagged PDF/UA.

During notebook execution, the viewer checks the notebook's cell sources and every other release file. The command-line verifier checks the entire notebook file, including saved outputs. Rerunning and saving the notebook may change output metadata and therefore its file checksum; retain the original ZIP as the release reference.

## Scope of analytical reproducibility

This is a verified snapshot and presentation release. It does not claim end-to-end model retraining from the files included here. The original frozen feature matrices, imputer/calibration splits, 45 model checkpoints, complete raw archives and analytical notebooks are retained separately. The [frozen specification](data/frozen_specification.json), [recorded analysis versions](data/analysis_environment.json) and [source hashes](data/source_provenance.json) identify the evidence lineage; they are not a complete installable training environment.

Reproducing the original fits would require those exact inputs and code, the original geospatial environment, and the dedicated 2001–2021 annual-backtest entry point with the preserved buffers, exclusions and calibration chronology. That is outside this publication release. Do not use a run-all command across historical experiment notebooks: earlier workflows include final-test execution beyond the scope of this package. No raw-data refresh, model fitting or final-test evaluation is needed to reproduce the presentation.

## Metric definitions

The model comparison uses equal-weight means across nine annual holdouts after combining spatial folds. Brier score is the mean squared error between predicted probability and a binary recorded-occurrence outcome; lower is better. About 1% improvement means a relative reduction in mean annual Brier versus past-rate forecasts. Top-decile recall is the share of recorded-positive cell-years captured within each annual selection budget. Pooled captures have different year weights from annual-average recall.

[Cell-year field definitions](data/map_data_dictionary.json) explain predictions and exclusions. Each row in `map_attributes.csv` is a fixed cell in one held-out year. Excluded rows have no prediction. The dictionary also describes geometry in the original GIS artifact; this release's CSV contains attributes only, and its maps are static images. [County summaries](data/county_map_summary.csv) are descriptive means and counts of eligible cells, not additional validation experiments.
