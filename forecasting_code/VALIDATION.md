# Package validation — October 18, 2026

## Clean dependency installation: passed

The published ZIP at commit `ba14f1b312fd47365e9e3240ce469a75d80b3f6e` was extracted into a separate review directory. A new Windows x64 virtual environment using Python 3.14.7 installed the pinned dependencies directly from PyPI with cache reuse disabled.

| Check | Result |
| --- | --- |
| Installation of five pinned direct dependencies | Passed |
| Synthetic suite | 12 tests passed |
| Summary-only verification | Passed; 0.067681 versus 0.071007 mean annual Brier, 4.91% relative model error increase, baseline wins all nine years |
| Original tested package integrity | All 26 manifest-listed files passed |
| Dependency consistency | `pip check`: no broken requirements |
| Import isolation | All five numerical libraries loaded from the new virtual environment |

System site-packages were excluded; user site was disabled. Inherited Conda/Python variables were removed and PATH restricted to the virtual environment and Windows directories for checks. The environment shares the existing conda-forge interpreter and standard library, as virtual environments normally do.

## Evidence

- [Machine-readable validation record](validation/clean_environment.json)
- [Synthetic test log](validation/synthetic_tests.log)
- [Summary verification log](validation/summary.log)
- [Dependency check log](validation/pip_check.log)
- [Resolved dependency versions](validation/resolved_dependencies.txt)

These logs record the tested 26-file package before this documentation update. The updated package manifest also covers these added evidence files. No training code, tests, requirements, saved scores or figures changed in this documentation update.

## Remaining limits

- Other operating systems, Python versions and Python distributions were not tested. This was not a fresh OS installation.
- Direct requirements are pinned; transitive dependencies remain resolver-dependent. The resolved-version record is environment-specific, not a portable lockfile.
- No preparation, training, real-data evaluation or model replay was performed. The optional exact-input adapter remains untested end to end.
- Synthetic tests exercise selected contracts; passing them does not demonstrate future forecasting performance or validate historical source availability.
- Initial pip bootstrapping encountered an execution-sandbox temporary-directory permission error; it succeeded outside that restriction without package changes.

## Preservation

The original experiment source still matches the code hash recorded in its frozen configuration. Original analytical inputs, published releases and 2022–2025 observations were untouched. This documentation update was reviewed locally before publication. It adds validation evidence without changing the analytical implementation or existing releases.
