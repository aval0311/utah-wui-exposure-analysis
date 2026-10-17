# Saved ML comparison

Version 0.2.0 · Published snapshot · Findings added October 17, 2026.

Open `index.html` with the entire folder intact. Viewing works offline without
Python, Jupyter, external fonts, map tiles, or installed JavaScript packages.

## Explore the saved predictions

The historical panel retains reviewed labels for 2001–2021. The comparison panel
adds saved 2013–2021 conservative XGBoost probabilities alongside observed occurrence
on exactly the same evaluation cohort. Its year selector and chart update the shared
explorer year. The county filter and count/rate controls apply to both panels.

The optional raw XGBoost probability line is a sensitivity reference. Conservative
XGBoost remains the frozen probability recommendation and raw XGBoost remains the
ranking reference. This switch does not change model selection.

The map selector offers observed labels, conservative probability, and raw ranking.
The probability scale is fixed at 0–40% across counties and years. Raw rank percentiles
are not probabilities. Outlined top-decile cells retain the saved annual three-county
budget; filtering a county does not rerank cells or create a new budget.

Select a cell for its 21-year label history and nine-year saved prediction table.
Missing probabilities remain missing. Earlier years show no saved holdout predictions;
gray unavailable maps do not imply zero probability. One binary cell outcome cannot
establish calibration.

## Matching denominators

The original historical rate includes known reviewed labels, retaining flagged
zeros as label 0. The new comparison includes only the original saved
`eligibility=eligible` rows, excluding unknown labels and frozen flagged zeros
from both observations and predictions. No labels or training/calibration rules change.

The comparison contains 8,588 eligible cell-years and 656 positives, excluding 230
unknown-label and 155 flagged-zero rows within 2013–2021. The other unknown development
label occurs before 2013. The complete historical snapshot remains 20,937 cell-years.

For example, the combined historical rate for 2020 uses 112 / 875 = 12.80%, while the
ML comparison uses 112 / 874 = 12.81%. This denominator change reflects the documented
exclusion of one flagged zero, rather than a changed label or new prediction.

The comparison shows observed rate and mean saved probability, or observed positive
cells and the sum of saved probabilities (Σp). Σp is expected recorded-positive cells,
not incidents or particular cells predicted to burn. Linearity of expectation does
not require independent cells; it also supplies no uncertainty interval. The signed
gap is predicted minus observed in percentage points. County/year summaries are
descriptive, not independent performance tests. They do not replace the equal-weight
annual model-selection metrics in the frozen ML study.

## Findings from the saved comparison

The dashboard's findings section is a fixed summary of all three counties over
2013–2021. It does not change with the explorer filters. All numbers come from
`data/ml_annual_summary.csv`; no predictions or labels were added or changed.

Across 8,588 eligible cell-years, the 656 recorded positives give a pooled observed
rate of 7.64%. The mean conservative probability is 8.34%, or +0.70 percentage
points above the observed rate. Summed probabilities give 716.1 expected positive
cell-years. These are repeated cell-years, not distinct cells or incident counts.

Combined annual observed rates range from 4.73% to 12.81%, while mean conservative
probabilities range from 7.38% to 8.99%. Predictions exceed observations in eight
of nine years. The largest absolute combined annual gap occurs in 2020: 112
observed positives versus 74.4 expected in 874 eligible cells, or 12.81% versus
8.51% (predicted minus observed: −4.30 percentage points). The source transition
and 122 unknown labels prevent attributing this difference to a particular cause.

| County | Eligible cell-years | Observed positives | Observed rate | Mean conservative probability | Gap (pp) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Salt Lake | 1,321 | 71 | 5.37% | 6.22% | +0.85 |
| Utah | 3,546 | 230 | 6.49% | 7.02% | +0.53 |
| Washington | 3,721 | 355 | 9.54% | 10.35% | +0.81 |

Pooled rates divide summed positives or probabilities by summed eligible
cell-years, rather than averaging rounded annual rates. Each gap is calculated
before rounding. These descriptive pooled summaries do not replace the frozen
study's equal-weight annual selection metrics. Aggregate agreement alone does not
establish cell-level calibration, spatial discrimination, or forecasting skill.
County comparisons have no significance or causal claim. Development-year reuse,
dependent observations, reporting uncertainty, and exclusions still apply.

## Interpretation and provenance

These development years informed model and calibration choices. Each annual map
combines five saved geographic fits under a frozen specification, rather than a new
deployment model. They are not an independent final evaluation or future forecasts.

Reporting uncertainty, the 2020 source transition, unequal cell areas, non-WUI land,
and retrospective terrain/climate availability remain limitations. No-record labels
do not prove absence of fire. No property-loss, burn-severity, daily-danger, or
per-square-kilometer hazard estimate is provided.

The original largest-area-share county assignment, 75 m display simplification,
observation areas, and cell-year labels are retained.

- `data/ml_comparison.json` and `data/ml_comparison.js`: identical display data; nine-year per-cell arrays or null exclusions, plus 36 matched summaries.
- `data/ml_annual_summary.csv`: eligible counts, observations, conservative/raw means and Σp, signed gaps, exclusions, and saved top-decile counts.
- `data/saved_ml_map_attributes.csv`: byte-identical original ML map evidence.
- `data/ml_map_data_dictionary.json` and `data/ml_frozen_specification.json`: original definitions and frozen model specification.
- `data/ml_provenance.json`: exact source hashes, join and exclusion rules, aggregation definitions, and work performed.
- `data/timeline.json`, `data/timeline.js`, `data/annual_summary.csv`, and `data/provenance.json`: unchanged original historical snapshot.

Optional integrity check with Python 3.10 or later: `python -I -S verify.py`.
Source export code and the retained inputs are separate from this portable viewer.
The exporter for this comparison uses the Python standard library and the already
assembled snapshots, without opening analytical models, raw inputs, or notebooks.
No source refresh, fitting, calibration, inference, or later-period observation read
occurs. This snapshot is published at the historical timeline URL; see PUBLICATION.md.

Original code/documentation are MIT licensed. Underlying source terms and attribution
remain those documented in the historical README and ML source guide.
