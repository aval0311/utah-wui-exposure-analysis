# Comparison validation

Published snapshot 0.2.0 · October 16, 2026 · Passed.

Findings update · October 17, 2026: fixed pooled county summaries, annual ranges,
and the 2020 example were recomputed from the existing matched-summary CSV.
Pooled denominators, sums, percentages, and signed gaps use unrounded values.
The findings explicitly retain development-year, reporting, cohort, and unit
limitations. No underlying data, prediction values, or interaction code changed.

- All 8,973 original map rows join by exact cell ID/year and agree with the historical label or its exclusion. All prediction values, raw percentiles, and original top-decile memberships are retained.
- The original 8,588 eligible cell-years and 656 positives are reproduced. The 230 unknown-label and 155 flagged-zero map rows retain null predictions.
- All 36 county/year summaries, including rates, sums of probabilities, signed gaps, and selection counts, are independently reconstructed from the portable cell values. All 36 CSV rows agree.
- The exporter reproduces saved means, prevalence, and Brier values for 18 annual XGBoost model rows and saved mean probabilities/selection counts for all 27 county summaries. These are integrity checks, not a new model experiment.
- The original historical data files and all consumed source files retain their hashes. The original historical project and public repository are unchanged.
- Browser checks exercise matched 2020 denominators, raw-reference visibility, count/rate switching, comparison-year controls, cell-level predictions, missing unknown/flagged-zero predictions, unavailable pre-2013 years, probability/rank map modes, preserved ranking budgets after county filtering, and comparison-chart keyboard navigation.
- Salt Lake in 2019 retains its original 11 raw top-decile cells after filtering; no new county budget is calculated.
- The 2020 combined historical rate remains 112/875 = 12.80%, while the matched comparison is 112/874 = 12.81%, with 74.4 expected positive cells from saved conservative probabilities.
- Desktop and 390 px/320 px phone layouts show no document overflow. The wide charts and cell prediction table scroll within their own regions. No application console errors or warnings were observed.
- Local HTML references resolve and viewing has no external script, font, map-tile, or data-fetch dependency. JSON/JavaScript payloads agree, the file manifest is verified, and ZIP member bytes match the folder.

No model objects, raw source archives, or analytical notebook execution paths are
opened for this comparison. No fitting, calibration fitting, new inference, label
change, source refresh, or later-period observation read occurs. The maximum saved
prediction year is 2021. The 2024–2025 observations remain untouched.

Browser checks are practical functional/layout checks, not formal accessibility
certification. Results remain studied development evidence, not independent final
performance or future forecasts. See PUBLICATION.md for this published snapshot.
