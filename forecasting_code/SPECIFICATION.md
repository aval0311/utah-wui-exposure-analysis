# Fixed experiment contract

This summary describes the executed experiment. The unchanged [planning specification](specification/forecast_specification.md) and [frozen configuration](evidence/frozen_config.json) provide the detailed record.

| Item | Fixed choice |
| --- | --- |
| Target | At least one recorded wildfire discovery per cell in UTC year T |
| Population | Same 997 nominal 4 km county-clipped cells; Salt Lake, Utah and Washington counties |
| Reviewed history / evaluation | 2001–2021 / 2013–2021 |
| Proposed issuance / input cutoff | December 15 T−1, 17:00 UTC / December 1 T−1, 00:00 UTC |
| Base training | 2001 through T−4 |
| Calibration | T−3 and T−2 |
| Baseline history | 2001 through T−2; recent baseline uses T−3 and T−2 |
| Eligibility | Exclude unknown labels and frozen flagged zeros from fitting, calibration and scoring |
| Primary candidate | M1 calibrated: terrain, area and six antecedent climate features |
| Recommendation rule | Lower mean annual Brier than the best baseline, without higher mean annual log loss; then substantive year/county review |

M0 uses elevation, slope, northness, eastness and log cell area. M1 adds precipitation, mean temperature and vapor-pressure deficit summaries for October–September and July–September ending before the target year. Target-year observed weather is excluded. A 60-day publication delay is assumed, not historically demonstrated.

Both logistic models use training-only median imputation and standardization, C=1, L2 regularization, lbfgs, tolerance 1e−8, maximum 2,000 iterations, no class weighting and no search. Calibration fixes slope at 1, estimates an intercept offset on the two calibration years, and applies half that offset. One-class or failed calibration falls back to raw probabilities. Logits and log loss clip probabilities at 1e−6 and 1−1e−6.

Baselines use Jeffreys-smoothed pooled/recent rates and fixed shrinkage strength 20 for county and cell history. Cells without history fall back to their county; counties without history fall back to the pooled rate.

All methods score the same 8,588 eligible cell-years, including 656 positives. Primary metrics average annual scores equally, rather than pooling all rows. The evaluation excludes 230 unknown labels and 155 flagged zeros. Whole-year splits assess the same locations over time, not transfer to new counties.

This is retrospective reconstruction. Contemporary terrain, reconstructed climate and later label review do not establish historical as-issued availability. No independent final-test or operational forecasting claim is supported.
