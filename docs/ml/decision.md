# WUI ML v1 model decision

**Recommend XGBoost with conservative intercept calibration as the primary portfolio model for annual recorded wildfire occurrence probabilities. Keep raw XGBoost as the development ranking reference and sigmoid Random Forest as the comparison benchmark.**

This choice prioritizes average probability accuracy while retaining the evidence about location prioritization. It records a development recommendation and freezes its specification separately from the original baseline and selection. It does not create or deploy a newly fitted model.

The recommendation uses only the 2001–2021 development experiment. Its held-out annual results cover 2013–2021. The baseline and all previous results remain unchanged; 2022–2025 targets, features and predictions were not loaded or evaluated.

**Intended use.** Estimate the probability of at least one recorded wildfire discovery in a nominal 4 km cell during a UTC calendar year, within the Salt Lake, Utah and Washington county footprint. The original 997 cells are clipped to county boundaries. The geographic sample includes cells beyond mapped WUI; it is not restricted to WUI or burnable land. These probabilities do not measure a property’s chance of burning, fire spread, severity or daily fire danger.

**Decision evidence.** Each validation year combines five held-out geographic folds with 20 km blocks and 4 km exclusion buffers. For year T, base training uses 2001 through T−3 and calibration uses T−2 and T−1. All methods use the same 8,588 eligible validation cell-years and 656 recorded-positive cell-years. Unknown labels and the 155 flagged zeros remain excluded from evaluation. Original known labels, including flagged zeros, remain in training and calibration. The earlier exclusion sensitivity is retained separately.

The following values are equal-weight means across nine validation years. Lower Brier score, log loss and absolute annual bias are better; higher average precision and top-10% recall are better. Absolute annual bias is in percentage points. Captures are summed positive cell-years, not distinct incidents.

| Model or reference | Brier | Log loss | Absolute bias pp | Average precision | Top 10% recall | Captured positives |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| XGBoost conservative | 0.070814 | 0.265863 | 1.61 | 0.1303 | 17.42% | 112 |
| XGBoost raw | 0.071353 | 0.265970 | 2.26 | 0.1337 | 18.09% | 117 |
| XGBoost sigmoid | 0.070897 | 0.268494 | 1.73 | 0.1271 | 17.97% | 116 |
| Random Forest sigmoid | 0.071341 | 0.268581 | 2.20 | 0.1213 | 16.13% | 105 |
| Random Forest raw | 0.073579 | 0.273762 | 4.33 | 0.1246 | 16.79% | 108 |
| Random Forest conservative | 0.071880 | 0.269224 | 3.12 | 0.1225 | 16.53% | 106 |
| Past training rate | 0.071514 | 0.274233 | 2.80 | — | — | — |
| Past two-year calibration rate | 0.071582 | 0.276132 | 2.17 | — | — | — |

**Why this model.** Conservative XGBoost has the lowest mean Brier score, log loss and absolute annual bias among the six model variants. It improves Brier score over raw XGBoost in eight of nine years and over sigmoid Random Forest in six of nine. Raw XGBoost has the highest mean average precision and top-10% recall among these model variants, which is why it remains the ranking reference.

The conservative model’s Brier advantage over sigmoid XGBoost is only **0.000084**. It has better Brier score in four of nine individual years, and better log loss in seven. The preference reflects the combined probability evidence and the constrained one-offset calibration approach; it does not establish a statistically significant winner. Sigmoid Random Forest has a signed mean bias close to zero, but its larger mean absolute annual bias shows that overprediction and underprediction partly cancel.

**Value beyond simple forecasts.** The saved reference forecasts use the observed rate in permitted base-training rows or the preceding two calibration years, always in the permitted training geography. They never use the validation year’s rate. Each is constant within a spatial fold, although rates can differ across the stitched folds; assigning a top-decile location ranking to these references would be misleading.

Conservative XGBoost reduces mean Brier score by **0.98%** relative to the training-rate reference and **1.07%** relative to the two-year reference. These are ratios of mean Brier scores, not percentage-point gains in classification accuracy. It wins on annual Brier in **7/9** and **4/9** years, respectively. The average improvement is modest and uneven. It wins on log loss in **7/9** and **8/9** years.

**Ranking trade-off.** Each method selects ceil(10% of eligible cells) per year, totaling 863 selected cell-years. Conservative XGBoost captures 112 recorded positives compared with 117 for raw and 116 for sigmoid. Annual-average recall falls from 18.09% to 17.42%, a 0.67 percentage-point reduction from raw. Pooled recall is 117/656 = 17.84% for raw and 112/656 = 17.07% for conservative; these pooled ratios have different year weights from the annual means.

Conservative calibration adds 72 and removes 72 cell-years from the priority lists, spanning 118 distinct cells. The entering observations contain four positives and the leaving observations contain nine. Annual membership overlap is 81.1%–97.9%. Capture improves in two years, ties in three and declines in four. Washington County accounts for the net loss of five positives. These counts are descriptive and do not establish suppression benefit or the cost of a missed event.

All 45 within-fold rankings remain identical. Changes arise because the separately fitted geographic folds receive different offsets before their held-out predictions are combined. A single strictly increasing calibrator on one final model would preserve that model’s internal ranking, subject to clipping or numerical ties. The development ranking reference therefore must not be presented as proof that a deployed model needs two conflicting priority maps.

**The unresolved 2020 limitation.** The observed rate was 12.81%, while raw XGBoost averaged 10.72%, conservative XGBoost 8.51% and sigmoid XGBoost 6.22%. Conservative calibration worsened Brier score from 0.112208 to 0.113131. Its top-10% capture nevertheless improved from 16 to 17 positives, illustrating that probability accuracy and a particular ranking budget can move in different directions. The method does not solve abrupt changes in recorded rates; the evidence cannot separate reporting changes from real occurrence changes. Do not switch methods retrospectively by year or apply a blanket upward adjustment.

**Frozen ML v1 specification.** Use the existing 20 terrain and antecedent-climate predictors and the original XGBoost candidate: 346 trees, depth 5, minimum child weight 20, L2 penalty 20, learning rate 0.03, row and column subsampling 0.8, no L1 penalty, no class reweighting or resampling, histogram CPU training and random seed 2026. Median imputation is fitted on base-training rows only. County, coordinates, IDs and target year are not added as predictors. Keep the original label policies, spatial exclusions and annual chronology.

Fit the calibration intercept only on the preceding two-year calibration block, keeping the logit slope fixed at one, then apply half the fitted intercept. Clip raw probabilities to [0.000001, 0.999999] as in the saved protocol. The 0.5 factor stays fixed; it is not an estimated optimum. No hyperparameter, shrinkage, feature-window or threshold search is added. The exact feature order, parameters and calibration rule are recorded in `decision.json` alongside the saved tables.

The climate inputs remain an authorized retrospective gridMET reconstruction using pre-January-1 windows and a 60-day assumed release lag. They do not prove what historical archive versions were available at each cutoff. Terrain-only and climate comparisons from earlier experiments support the development history, but their different dates and cohorts are not mixed into this decision table as directly comparable scores.

**How to present ML v1.** Use conservative XGBoost as the named probability model and describe raw XGBoost as the ranking sensitivity reference. Present sigmoid Random Forest and both simple past-rate forecasts as benchmarks. Describe the output as recorded-occurrence susceptibility within the three-county footprint. Keep the common-cohort exclusions, incomplete reporting coverage and retrospective availability limitations alongside the results. Spatial buffers and repeated folds do not establish independent observations or an untouched validation sample.

**Milestone recorded at decision time (now completed).** Build the portfolio interpretation and clearly labeled held-out development maps using the frozen recommendation, showing both probability accuracy and ranking sensitivity. Keep 2024–2025 closed. A later single-model fit needs its own explicit training/calibration design; fitting on every 2001–2021 label and then calibrating on those same fitted observations would not preserve the validated separation. New independent evidence would be needed for stronger future-performance claims.

**Decision scope.** This is a retrospective model-development decision based on previously examined years and chosen configurations. No significance claim, statewide transfer claim, operational readiness claim or revision of the original final benchmark is made. No agency outreach is required to complete this portfolio version.

**Publication evidence.** Read the [annual comparison](data/annual_comparison.csv), [ranking trade-off](data/ranking_tradeoff.csv), [exact frozen specification](data/frozen_specification.json), and [reproduction scope](REPRODUCIBILITY.md). This publication copy preserves the decision and numerical values while replacing working-machine links. The original decision remains unchanged.
