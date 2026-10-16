# Observation area and model interpretation

The original 997 nominal 4 km cells are clipped to the three-county footprint. Of these, 754 are effectively full 16 km² cells and 243 are smaller boundary cells. The maps estimate at least one recorded wildfire discovery within each original footprint.

Full cells make up 75.0% of eligible 2013–2021 cell-years and 98.0% of both raw and conservative top-decile slots: 846 of 863 selections. These are repeated annual selection slots, not distinct locations. No original prediction in cells below 12 km² enters either top decile.

Conservative probabilities average 3.22% in clipped cells against 3.03% recorded occurrence, versus 10.04% and 9.17% in full cells. The pooled clipped result hides underprediction in the 12-to-below-16 km² group: 6.40% predicted versus 8.09% observed. The smallest group has no recorded positives, which does not establish zero underlying risk.

## Frozen-model sensitivity

Setting only the area input to 16 km² raises the clipped-cell conservative mean to 7.61% and replaces 96 of 863 conservative selections (11.1%). Raw ranking replaces 86 selections (10.0%). Other inputs still describe the original footprint, so the changed predictions are a sensitivity diagnostic. They are not corrected forecasts, a causal effect or an accuracy improvement. The publication maps retain the original predictions and rankings.

Area does not explain the remaining 2020 shortfall. Full-cell conservative probabilities average 10.51%, against 15.73% recorded occurrence. Full cells account for 89.2% of the gap between recorded-positive counts and summed conservative probabilities; their predictions are unchanged by the area-input perturbation.

Area has the largest individual contribution in the saved model explanation. Contributions describe the fitted model and can share attribution with correlated predictors; they do not establish a causal driver. A separate target or exposure model would be needed to compare hazard on equal geographic support.

## Supporting evidence

- [Original area summaries](data/area_probability_summary.csv)
- [Annual area summaries](data/annual_area_summary.csv)
- [Sensitivity summaries](data/area_sensitivity_summary.csv)
- [Area-audit report](data/area_audit_summary.json)
- [Held-out feature importance](data/feature_importance.csv)
- [Interpretation report](data/interpretation_summary.json)

Full original notebooks and model checkpoints remain in the preserved analytical workspace. The publication package offers portable saved evidence without invoking those execution paths.
