# Proposed next calendar year occurrence forecast

## Target and issuance

For each of the original 997 county-clipped nominal 4 km cells, estimate the probability of at least one recorded wildfire discovery in UTC calendar year T, conditional on information available at the forecast cutoff. The target interval is [January 1 T 00:00 UTC, January 1 T+1 00:00 UTC). Preserve the reviewed WF definition, original cell IDs, EPSG:26912 geometry and Salt Lake, Utah and Washington footprint.

Issue at **December 15 T−1, 17:00 UTC** (10:00 a.m. Mountain Standard Time). Freeze inputs at **December 1 T−1, 00:00 UTC**. The two-week interval is for checks, computation and local review; information arriving during it waits for the next issue. This is one fixed annual forecast, with no midyear update in version 1.

For example, a development forecast of 2021 would freeze inputs on December 1, 2020 and issue December 15, 2020. This is a proposed schedule, not evidence that such a forecast existed. A future 2027 issue would be December 15, 2026, but no 2027 inputs or predictions are authorized or built here. Missing authorization for later years must not be bypassed by silently substituting old observations into a current forecast.

The outcome is recorded cell occurrence, not ignition count, burned area, spread, fire danger, loss or WUI-only risk. A no-record label does not establish no fire. Unequal cell areas affect occurrence opportunity; include area and retain small cells. The geometry includes non-WUI land.

## Information contract

Every input needs a measurement interval, source version, publication timestamp, local acquisition timestamp, revision status and transformation lineage. Both the end of the measurement interval and publication must precede the cutoff; an already archived source version must be reproducible. Acquisition today does not prove historical availability. Unknown publication time fails strict as-issued eligibility.

Use two separately labeled tracks:

1. **Retrospective reconstruction:** contemporary static terrain, the existing antecedent climate reconstruction and reviewed historical labels, with the assumptions disclosed. This can test predictive usefulness under chronological separation after separate training authorization.
2. **Strict as-issued replay:** only sources and labels with demonstrated pre-cutoff vintages. This track is blocked until its availability ledger passes. Do not label reconstructed results operational hindcasts.

Climate windows stay fixed: October 1 T−2 through September 30 T−1 for the 12-month features; July 1 through September 30 T−1 for summer features. Their conservative physical end is October 1 T−1 at 07:00 UTC. A 60-day assumed lag ends November 30 at 07:00 UTC, before the December 1 cutoff. This is a reconstruction assumption, not a release guarantee. No observed weather in T, full-year T−1 weather, full-record climatology or future-filled interpolation is allowed.

For labels, the latest candidate year for fitting is **T−2**, allowing almost eleven months after its end before cutoff. This maturation allowance is a proposed assumption, not verified latency. In strict replay, every contributing label and its coverage decision must actually have been available by cutoff. If not, stop and revise the schedule before fitting; do not silently admit late revisions. Evaluation labels can mature after the forecast, but cannot feed its model or calibration.

## Candidate methods

Keep scope modest and fixed before fitting. Use unweighted Bernoulli outcomes without oversampling or class reweighting, because probability quality is primary.

| Method | Proposed definition |
| --- | --- |
| Pooled historical rate | (S+0.5)/(N+1), using eligible history through T−2; Jeffreys smoothing avoids exact zero or one. |
| Recent historical rate | Same formula using T−3 and T−2 only; fall back to pooled if no eligible rows. |
| County rate | (S_county + 20 × pooled_rate)/(N_county + 20), through T−2; fixed shrinkage strength 20. Use frozen primary-county assignment. |
| Cell history rate | (S_cell + 20 × county_rate)/(N_cell + 20), through T−2; fall back to county for no cell history. This tests persistence at these same locations. |
| Modest model M0 | L2 logistic regression with intercept and five inputs: elevation_mean_m, slope_mean_deg, northness_mean, eastness_mean, log(study_area_km2). |
| Modest model M1 | M0 plus all six existing antecedent climate predictors, for retrospective reconstruction only until their vintages pass. |

For both logistic models, fix regularization C=1, no interactions, no feature selection, no early stopping and no hyperparameter search. Median imputation followed by mean/standard-deviation scaling is fitted exclusively on base-training years. Positive area is required before taking log. A predictor entirely missing in base training blocks that model arm; do not borrow a later median. Zero-variance columns receive scale 1. Missingness remains visible in QA, not a newly optimized predictor.

Fit base models through T−4 and reserve T−3 and T−2 for calibration. Preserve both raw probabilities and a prespecified intercept-only calibration with slope 1 and half of the fitted offset applied, analogous to the frozen conservative rule. Calibrated M1 is the proposed primary candidate; raw M0/M1 and calibrated M0 are diagnostic comparisons. If calibration has only one class or optimization fails, use the raw probabilities and record the fallback. Clip probabilities to [0.000001, 0.999999] for log loss and logits. Do not tune shrinkage.

Baselines deliberately use all eligible history available through T−2, including the model's calibration years. They are strong information-matched alternatives, not restricted to the shorter base-training interval. All methods predict and score identical target-year rows. Existing XGBoost is background evidence; its saved predictions and fitted objects are not transferable forecasts under this new schedule.

## Label and population rules

Forecast all 997 cells, preserving a separate prediction status for feature failures. Score only known reviewed target-year labels outside the frozen flagged-zero mask. For this new experiment, exclude unknown and flagged-zero rows from base fitting, calibration and baseline counts as well; preserve original label values and masks. This differs from the frozen ML training policy and must be recorded, not back-applied to it. Do not estimate unknown labels or recode them as zero.

These reviewed exclusions are retrospective QA. Their historical availability must be audited for strict replay; future review knowledge cannot silently determine historical training membership. Score-time exclusions may use reviewed outcome quality, but results then describe that reviewed cohort and can be selection-biased. Report all excluded denominators and forecast coverage. No 2025 burnable, vegetation or imagery mask enters geometry, features or eligibility.

## Output contract and reporting

Any later local prototype should write one row per cell and target year with cell_id, target_year, issue_utc, data_cutoff_utc, target_start_utc, target_end_utc, probability, method_id, availability_track, model_version, input_manifest_hash, latest_training_label_year, calibration_years, prediction_status and warnings. Save probabilities before joining evaluation labels. Include feature lineage and fit-membership ledgers separately. No forecasts are generated by this package.

Primary score: equal-weight mean of nine annual unweighted Brier scores, with each baseline evaluated identically. Also report annual and pooled Brier, log loss, mean probability minus observed rate, observed/expected positive cells, calibration plots, average precision and ROC AUC where both classes exist. Undefined metrics remain missing with reasons. Ranking uses ceil(0.10 × eligible cells), probability descending then cell_id ascending; ties in constant baselines carry no geographic skill claim. This is a cell budget, not an area budget.

Show all year and county breakdowns, feature missingness, and 2020–2021 separately as a reporting-transition stress check. Do not discard those years. Secondary area-weighted scores answer a different question and must be labeled. With nine studied years, report paired annual score differences and their range; avoid row-independent significance tests or claims of independent validation. A model earns a recommendation only if it beats the strongest baseline on mean annual Brier without worse mean log loss, and its year/county failures are substantively acceptable. Otherwise retain a baseline or conclude that useful improvement was not demonstrated.
