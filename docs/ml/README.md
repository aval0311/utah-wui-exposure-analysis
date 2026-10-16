# Utah wildfire occurrence modeling

Adam Valentino · ML v1 publication package 1.0.0 · October 16, 2026

This portfolio case study compares Random Forest and XGBoost for annual recorded wildfire occurrence within county-clipped cells in Salt Lake, Utah and Washington counties. Development uses 2001–2021; the annual maps cover 2013–2021. Conservative XGBoost is the probability recommendation, with raw XGBoost retained as the ranking reference.

**Start with [the offline portfolio viewer](index.html).** Extract the entire package and open `index.html` in a browser. All figures, descriptions and tables work offline. No Python, Jupyter, accounts, API keys or model installation is required. External source citations need internet only when followed.

## Read and explore

- [Portfolio narrative](narrative.md)
- [Map atlas with searchable descriptions](wui_ml_v1_atlas.pdf)
- [Executed snapshot notebook](wui_ml_v1_snapshot.ipynb)
- [Frozen model decision](decision.md) and [exact specification](data/frozen_specification.json)
- [Area-audit findings](AREA_AUDIT.md) and [all map captions](map_captions.md)
- [Sources and vintages](SOURCES.md), [reproducibility](REPRODUCIBILITY.md), [release validation](RELEASE_VALIDATION.md)
- [License and attribution](DATA_LICENSE.md), [citation](CITATION.cff), [publication handoff](PUBLISHING.md)

These years informed model selection, so the comparison is development evidence rather than an independent final evaluation. The roughly 1% relative improvement in mean Brier score over past-rate references is modest. Recorded occurrence depends on reporting and cell area; the maps do not estimate property loss, daily fire danger or hazard per unit area.

## Check the package

With Python 3.10 or later, run `python -I -S viewer.py --verify` from the extracted folder. This uses only the Python standard library. To reproduce the HTML, run `python -I -S viewer.py --build` and then verify again. The same commands work with an absolute path to `viewer.py` from another working directory.

The package contains saved development evidence and presentation code. It contains no fitted model objects, raw incident archive, climate rasters or 2024–2025 observations. Full training reproduction is a separate scope described in the reproduction guide. The verified descriptive baseline remains available at the [existing portfolio](https://aval0311.github.io/utah-wui-exposure-analysis/).
