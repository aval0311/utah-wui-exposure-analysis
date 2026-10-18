# Reproduction and input boundaries

## Safe review without original inputs

Run `python -I -S review.py` to check the manifest and summary arithmetic. Run `python -I run.py test` for synthetic tests. Neither command searches the original workspace or opens observation files. The standard-library check averages existing annual scores; it does not recompute cell-level metrics.

## Optional exact-input rerun

No real-data stages were run during packaging. These commands are intended only for the owner with the preserved development exports and authorization to rerun. A reviewer without those exports cannot retrain from this ZIP alone.

```text
python -I run.py prepare --workspace "PATH_TO_PRESERVED_WORKSPACE" --run-name reproduction_01
python -I run.py train --workspace "PATH_TO_PRESERVED_WORKSPACE" --run-name reproduction_01
python -I run.py evaluate --workspace "PATH_TO_PRESERVED_WORKSPACE" --run-name reproduction_01
python -I run.py verify --workspace "PATH_TO_PRESERVED_WORKSPACE" --run-name reproduction_01
```

The workspace must contain these exact relative paths, matching hashes in the archived contract review:

| Path | Purpose |
| --- | --- |
| `historical_timeline_v1/dist/data/timeline.json` | Reviewed 2001–2021 labels, cells and eligibility statuses |
| `ml_outputs/terrain_064dcafd4cc0/terrain_features_by_cell.parquet` | Static terrain and original cell area |
| `ml_outputs/climate_features_ba80797440f5/climate_features_by_cell_year.parquet` | Development-only antecedent climate predictors |
| `ml_outputs/climate_features_ba80797440f5/feature_year_availability.csv` | Assumed availability ledger |
| `fire_occurrence_forecasting_v1/forecast_specification.md` | Original fixed specification |
| `fire_occurrence_forecasting_v1/experiment_schedule.csv` | Original nine-fold schedule |

Do not substitute mixed-period source tables or unreviewed exports. No network fetching, automatic source discovery or year-range option is provided. The original input-hash checks remain active, and preparation checks the exact 2001–2021 population and 2013–2021 schedule. The wrapper is a convenience boundary, not a security sandbox against deliberate source-code modification.

New outputs go only to `package/runs/RUN_NAME`. Preparation refuses an existing run directory; fitting and evaluation also guard their existing outputs. Verification can rewrite verification reports in that new reproduction directory, but does not refit. Original completed runs are never used as output directories by the wrapper.

The original code is unchanged. The wrapper redirects its source workspace, contract-metadata directory and output directory. Its code-hash freeze still refers to the unchanged reference file. Preserve the ZIP and manifest; rerunning with edited code creates a different experiment and must not be represented as the original run.

The archived review's pending-authorization wording predates the authorized completed experiment. It is included for lineage and exact source hashes, not as the current execution status. The source review may include hashes for other audited metadata; the experiment accessor uses only its six named inputs.

## Limits

The adapter's full real-data rerun has not been exercised during packaging. Original evidence records the successful experiment and replay; synthetic tests validate selected contracts, not every branch or a clean-room end-to-end reconstruction. Historical source vintages and reporting completeness remain unverified. Later-period observations, raw archives, prediction rows and model artifacts are intentionally absent.
