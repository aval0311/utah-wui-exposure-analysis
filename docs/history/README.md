# Utah history and saved ML comparison

Published snapshot 0.2.0 · Reviewed history 2001–2021; saved ML holdouts 2013–2021.

**Start with [the saved ML comparison guide](ML_COMPARISON.md)** for the new charts,
map modes, exact evaluation cohort, and per-cell probability table. The historical
snapshot and its original denominator are retained. The historical notes below
describe that panel; the comparison guide explains the different ML denominator.

Open `index.html` in a browser with the whole folder intact. Viewing needs no Python,
Jupyter, account, network connection, or external JavaScript libraries. The links to
the published dashboard, ML case study, and source documentation require internet.

## Explore

- Filter all three counties or one county, then select a year with the slider, arrows, or chart.
- Switch between recorded-positive cell counts and the percentage of known reviewed cells.
- Read the annual table or download all 84 annual summaries: 21 years for the combined footprint and each of three county groups.
- Select a map cell, use the cell list, or use arrow keys and Enter within a map to inspect its 21 annual labels.

A positive cell has at least one recorded wildfire discovery in a UTC calendar year.
Multiple discoveries in the same cell-year still contribute one positive. The 2,006
positive cell-years are not a unique incident count or a count of distinct cells.

## Data and denominator

The snapshot contains 997 original county-union-clipped nominal 4 km cells in each of
21 years: 20,937 cell-years. There are 20,706 known reviewed labels, including 2,006
positive labels, and 231 unknown labels. The 155 frozen flagged zeros are a subset
of known reviewed zero labels, not a fifth label value or 155 additional rows.

The default historical rate is:

`recorded-positive cells / known reviewed cells × 100`

Unknown labels remain missing and are omitted from this denominator. Flagged zeros
retain their reviewed label 0 and remain included. Their flags are displayed separately.
This differs from the ML case study's evaluation cohort, which excludes the frozen
155 flagged zeros. The 2013–2021 intersection has been reconciled against every row
in the published ML map evidence. The new panel adds descriptive summaries of saved
predictions, without new fitting, inference, relabeling, or training/calibration changes.

## Geography and interpretation

County groups use the original grid's `primary_county`: the county with the largest
area share of a cell. A cross-county cell is counted once. These are cell groups,
not exact incident-county counts. The map panels have separate scales and show
EPSG:26912 geometry simplified by 75 m for display only; labels and original areas
are retained. The footprint includes non-WUI land and unequal cell areas.

No-record labels do not prove no fire occurred. Reporting uncertainty remains, and
the 2020 reporting-system transition cannot be separated from changes in true
occurrence using this evidence. Unknown labels are more common in 2020–2021.
The charts do not estimate property loss, daily fire danger, burn severity, or hazard
per square kilometer. They do not provide a future forecast.

## Provenance and reproduction

`data/provenance.json` records the exact frozen input hashes, selected columns,
read-time 2001–2021 filters, geometry transformation, and denominator definition.
`data/timeline.json` contains the portable cell histories, map paths, and summaries;
`data/timeline.js` contains the same data for browsers that block local-file fetches.
`data/annual_summary.csv` provides the annual values. `manifest.json` records the
SHA-256 and size of the distributed files, excluding itself.

With Python 3.10 or later, optionally run `python -I -S verify.py` to check file
integrity. Python is not required for viewing. See `VALIDATION.md` for completed
data and interface checks and their limits.

The original historical project retains its geospatial export code. The source
project for this comparison retains `tools/export_predictions.py`, using only the
Python standard library and the already assembled historical and ML snapshots.
Those retained source snapshots are separate from the portable viewer. No analytical
notebook is executed for this build.
Temporal reads load only 2001–2021. No 2022–2025 observation rows are loaded or evaluated.

Original explorer code and documentation are MIT licensed. Underlying source terms
remain separate. The labels derive from retained NIFC InFORM wildfire records;
county boundaries are credited to State of Utah, SGID. Provider attribution and
limitations are documented in the [ML source guide](https://aval0311.github.io/utah-wui-exposure-analysis/ml/#sources)
and [source license notes](https://aval0311.github.io/utah-wui-exposure-analysis/ml/DATA_LICENSE.md).
No raw incident records, precise incident locations, or provider logos are bundled.

This published snapshot has not been uploaded to GitHub or deployed.
