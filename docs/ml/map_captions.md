# WUI ML map captions

## Probability panels

Historical held-out probability of at least one recorded wildfire discovery within each county-clipped cell during the mapped UTC year. Conservative XGBoost uses the frozen terrain-plus-climate model and saved half-intercept calibration. Cell areas vary at county boundaries, so these probabilities do not measure hazard per square kilometre. Original-area predictions are shown; the area-16 sensitivity diagnostic is not mapped.

## Ranking panels

Raw XGBoost ranking percentile within the eligible three-county cohort for the mapped year; 100 is the highest rank and is not a probability. Outlines mark the original annual ceil(10% of eligible cells) budget shared across all three counties. Across 2013-2021, full 16 km² cells comprise 75.0% of eligible cell-years and 98.0% of top-decile selections for both raw and conservative probabilities. Observation area therefore affects ranking comparability; the values and membership remain unchanged.

## Shared scope and exclusions

Development uses 2001-2021; held-out annual maps are available for 2013-2021. Five geographic fits are combined within each year. The county footprint includes non-WUI land. Hatched unknown labels and flagged-zero exclusions have no prediction and must not be read as low risk. These historical development maps retain reporting and retrospective climate-availability limitations; they are not current fire-danger or property-loss forecasts. County panels have separate extents; coordinates are EPSG:26912.

## Area sensitivity figure

Setting only the frozen model area input to 16 km² changes clipped-cell conservative mean probability from 3.22% to 7.61% and replaces 96/863 conservative selections (11.1%) and 86/863 raw selections (10.0%) across nine years. This is a sensitivity diagnostic, not an area-normalized forecast or an accuracy improvement; all other inputs still describe the original cell.

## Development qualification

These development years informed model and calibration choices. The results describe observations held out from individual fits, rather than an independent final evaluation. Contemporary terrain is treated as a static historical proxy; historical as-issued terrain and climate availability is unverified.

## Annual map descriptions

### 2013

2013: 997 of 997 original cells have held-out predictions; 0 unknown-label and 0 flagged-zero cells are excluded. Outlines select 100 cells across the three-county cohort. In this year, full cells represent 75.6% of eligible cells and 99.0% of raw top-decile selections. Upper panels show conservative probabilities; lower panels show raw ranking percentiles. Original-area values are retained, and boundary-cell probabilities are not per-km² hazard measures. Development years informed model selection; terrain is a contemporary static proxy.

Geographic comparison among eligible cells: Salt Lake has mean conservative probability 7.19% and 8 raw top-decile cells; Utah has mean conservative probability 7.59% and 34 raw top-decile cells; Washington has mean conservative probability 10.59% and 58 raw top-decile cells. County averages do not imply uniform conditions within a county; the mapped pattern is clustered, and panel scales differ.

### 2014

2014: 997 of 997 original cells have held-out predictions; 0 unknown-label and 0 flagged-zero cells are excluded. Outlines select 100 cells across the three-county cohort. In this year, full cells represent 75.6% of eligible cells and 99.0% of raw top-decile selections. Upper panels show conservative probabilities; lower panels show raw ranking percentiles. Original-area values are retained, and boundary-cell probabilities are not per-km² hazard measures. Development years informed model selection; terrain is a contemporary static proxy.

Geographic comparison among eligible cells: Salt Lake has mean conservative probability 5.99% and 9 raw top-decile cells; Utah has mean conservative probability 6.93% and 17 raw top-decile cells; Washington has mean conservative probability 12.01% and 74 raw top-decile cells. County averages do not imply uniform conditions within a county; the mapped pattern is clustered, and panel scales differ.

### 2015

2015: 997 of 997 original cells have held-out predictions; 0 unknown-label and 0 flagged-zero cells are excluded. Outlines select 100 cells across the three-county cohort. In this year, full cells represent 75.6% of eligible cells and 98.0% of raw top-decile selections. Upper panels show conservative probabilities; lower panels show raw ranking percentiles. Original-area values are retained, and boundary-cell probabilities are not per-km² hazard measures. Development years informed model selection; terrain is a contemporary static proxy.

Geographic comparison among eligible cells: Salt Lake has mean conservative probability 6.03% and 10 raw top-decile cells; Utah has mean conservative probability 7.26% and 36 raw top-decile cells; Washington has mean conservative probability 9.58% and 54 raw top-decile cells. County averages do not imply uniform conditions within a county; the mapped pattern is clustered, and panel scales differ.

### 2016

2016: 997 of 997 original cells have held-out predictions; 0 unknown-label and 0 flagged-zero cells are excluded. Outlines select 100 cells across the three-county cohort. In this year, full cells represent 75.6% of eligible cells and 96.0% of raw top-decile selections. Upper panels show conservative probabilities; lower panels show raw ranking percentiles. Original-area values are retained, and boundary-cell probabilities are not per-km² hazard measures. Development years informed model selection; terrain is a contemporary static proxy.

Geographic comparison among eligible cells: Salt Lake has mean conservative probability 5.61% and 7 raw top-decile cells; Utah has mean conservative probability 6.32% and 27 raw top-decile cells; Washington has mean conservative probability 9.95% and 66 raw top-decile cells. County averages do not imply uniform conditions within a county; the mapped pattern is clustered, and panel scales differ.

### 2017

2017: 948 of 997 original cells have held-out predictions; 2 unknown-label and 47 flagged-zero cells are excluded. Outlines select 95 cells across the three-county cohort. In this year, full cells represent 74.8% of eligible cells and 97.9% of raw top-decile selections. Upper panels show conservative probabilities; lower panels show raw ranking percentiles. Original-area values are retained, and boundary-cell probabilities are not per-km² hazard measures. Development years informed model selection; terrain is a contemporary static proxy.

Geographic comparison among eligible cells: Salt Lake has mean conservative probability 6.07% and 9 raw top-decile cells; Utah has mean conservative probability 6.63% and 24 raw top-decile cells; Washington has mean conservative probability 10.66% and 62 raw top-decile cells. County averages do not imply uniform conditions within a county; the mapped pattern is clustered, and panel scales differ.

### 2018

2018: 954 of 997 original cells have held-out predictions; 2 unknown-label and 41 flagged-zero cells are excluded. Outlines select 96 cells across the three-county cohort. In this year, full cells represent 75.3% of eligible cells and 97.9% of raw top-decile selections. Upper panels show conservative probabilities; lower panels show raw ranking percentiles. Original-area values are retained, and boundary-cell probabilities are not per-km² hazard measures. Development years informed model selection; terrain is a contemporary static proxy.

Geographic comparison among eligible cells: Salt Lake has mean conservative probability 7.14% and 19 raw top-decile cells; Utah has mean conservative probability 8.08% and 46 raw top-decile cells; Washington has mean conservative probability 9.02% and 31 raw top-decile cells. County averages do not imply uniform conditions within a county; the mapped pattern is clustered, and panel scales differ.

### 2019

2019: 931 of 997 original cells have held-out predictions; 0 unknown-label and 66 flagged-zero cells are excluded. Outlines select 94 cells across the three-county cohort. In this year, full cells represent 74.1% of eligible cells and 97.9% of raw top-decile selections. Upper panels show conservative probabilities; lower panels show raw ranking percentiles. Original-area values are retained, and boundary-cell probabilities are not per-km² hazard measures. Development years informed model selection; terrain is a contemporary static proxy.

Geographic comparison among eligible cells: Salt Lake has mean conservative probability 5.80% and 11 raw top-decile cells; Utah has mean conservative probability 6.49% and 26 raw top-decile cells; Washington has mean conservative probability 8.71% and 57 raw top-decile cells. County averages do not imply uniform conditions within a county; the mapped pattern is clustered, and panel scales differ.

### 2020

2020: 874 of 997 original cells have held-out predictions; 122 unknown-label and 1 flagged-zero cells are excluded. Outlines select 88 cells across the three-county cohort. In this year, full cells represent 73.5% of eligible cells and 98.9% of raw top-decile selections. Upper panels show conservative probabilities; lower panels show raw ranking percentiles. Original-area values are retained, and boundary-cell probabilities are not per-km² hazard measures. Development years informed model selection; terrain is a contemporary static proxy.

Geographic comparison among eligible cells: Salt Lake has mean conservative probability 6.17% and 10 raw top-decile cells; Utah has mean conservative probability 6.69% and 23 raw top-decile cells; Washington has mean conservative probability 11.12% and 55 raw top-decile cells. County averages do not imply uniform conditions within a county; the mapped pattern is clustered, and panel scales differ.

### 2021

2021: 893 of 997 original cells have held-out predictions; 104 unknown-label and 0 flagged-zero cells are excluded. Outlines select 90 cells across the three-county cohort. In this year, full cells represent 74.7% of eligible cells and 97.8% of raw top-decile selections. Upper panels show conservative probabilities; lower panels show raw ranking percentiles. Original-area values are retained, and boundary-cell probabilities are not per-km² hazard measures. Development years informed model selection; terrain is a contemporary static proxy.

Geographic comparison among eligible cells: Salt Lake has mean conservative probability 5.93% and 3 raw top-decile cells; Utah has mean conservative probability 7.15% and 24 raw top-decile cells; Washington has mean conservative probability 11.70% and 63 raw top-decile cells. County averages do not imply uniform conditions within a county; the mapped pattern is clustered, and panel scales differ.

[Sources](SOURCES.md) · [Cell-year attributes](data/map_attributes.csv) · [Field definitions](data/map_data_dictionary.json)
