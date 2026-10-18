# Utah wildfire forecasting: when cell history beat the model

**Forecasting code and reproducibility package.** A fixed retrospective experiment tested whether terrain and antecedent climate improved next-year recorded wildfire occurrence probabilities across 997 county-clipped cells in three Utah counties.

The smoothed cell-history baseline beat the primary calibrated logistic model in all nine evaluation years. Mean annual Brier error was 0.067681 versus 0.071007: the model's error was 4.91% higher. The decision was to retain the baseline as the retrospective reference, not tune until an ML model won.

## Start here: a five-minute review

1. Read [the experiment contract](SPECIFICATION.md) for the target, chronology, baselines and decision rule.
2. Run `python -I -S review.py`. This checks package hashes and recomputes the headline comparison from annual summary scores using only the standard library.
3. With the numerical environment installed, run `python -I run.py test`. Twelve synthetic tests exercise chronology, exclusions, baseline fallback, calibration, metrics, deterministic ties and overwrite protection. They do not read original observations or fit models.
4. Inspect [the original experiment code](reference/experiment.py): `role_labels`, `baselines`, `train`, `evaluate` and `verify` show the full implementation.

## Clean-environment validation

On October 18, 2026, the published package installed successfully from PyPI into a fresh Windows virtual environment using Python 3.14.7. All 12 synthetic tests, summary checks, and dependency checks passed. Numerical imports came from the new environment, with system site-packages excluded and user site disabled.

This validates the installation and synthetic/summary workflow on the tested configuration. The virtual environment shares the existing interpreter and standard library; other platforms and full real-data reproduction remain untested. See [validation evidence](VALIDATION.md) and [environment limits](ENVIRONMENT.md).

## What the code demonstrates

- Four historical baselines, plus two fixed L2 logistic models with raw and calibrated variants.
- Whole-year temporal separation; training-only imputation and scaling; a separate calibration interval.
- Predictions persisted and hashed before evaluation joins outcomes.
- Audited input allowlists, source hashes, fit membership ledgers and non-overwrite guards.
- Explicit distinction between retrospective development evidence and operational forecasting.

The original code is copied byte-for-byte and matches the code hash in the completed run's [frozen configuration](evidence/frozen_config.json). `run.py` is a new packaging adapter, not the code that generated the original findings. It changes paths and command access only. Package tests were added after the experiment; they are verification, not evidence of a prospective preregistration.

## What is reproducible here?

| Level | Included? | Meaning |
| --- | --- | --- |
| Inspect the fixed implementation | Yes | Original source, specification and actual frozen settings |
| Check synthetic contracts | Yes | Twelve tests without real observations |
| Recompute headline summary | Yes | Annual scores reproduce the reported means and nine-year comparison |
| Recompute metrics from cell-level predictions | No | Cell-level predictions and labels are not bundled |
| Retrain the original experiment | Conditional | Requires the exact separately preserved, audited development exports |
| Demonstrate operational forecasting skill | No | Historical input vintages are unverified; no independent final evaluation |

The included original verification JSON records a previous replay of 18 model artifacts and 36 baseline-year forecasts. This package does **not** rerun that replay without the original inputs. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for the opt-in rerun procedure and its limits.

## Evidence and scope

[Results](evidence/RESULTS.md), [annual scores](evidence/annual_metrics.csv), [method comparison](evidence/method_comparison.csv), and [county comparison](evidence/county_mean_annual_metrics.csv) are preserved outputs. No new fitting or evaluation was performed to make this package. No raw incidents, mixed-year matrices, protected-period observations or saved model binaries are bundled.

The target is at least one **recorded wildfire discovery** per cell per UTC year, not incidents, burned area or property loss. Reporting changes around 2020, reviewed exclusions, unequal cell areas, non-WUI land and unverified historical availability limit interpretation. The result applies to these features, models and development years; it does not imply climate is unimportant.

**2022–2025 observations remain untouched.** Existing XGBoost recommendations and published releases remain separate and unchanged.

## File guide

- `reference/`: unchanged experiment implementation and its original six tests.
- `tests/`: six additional synthetic regression tests.
- `specification/`: original planning specification, schedule, availability audit and pre-training contract metadata.
- `evidence/`: completed-run settings, summary scores and original verification record.
- `requirements.txt`, `ENVIRONMENT.md`: environment requirements and validation scope.
- `source_provenance.json`, `manifest.json`: copied-source lineage and package integrity.

The original planning documents retain their historical future-tense language and pending-authorization status. They are archival records; the completed-run settings and results document what was subsequently executed.
