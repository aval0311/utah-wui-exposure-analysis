# Release v3

## Changes

- Reorganized the notebook into overview, results summary, methods, configuration, twelve
  sequential phases, interpretation, limitations, future work, execution provenance, and a
  retained benchmark appendix.
- Corrected facility headings and explained phase inputs, decisions, validation, and outputs.
- Filtered historical occurrence processing to recorded wildfires in a stated date interval;
  added a reconciling selection ledger and separate county versus rectangle counts.
- Included ACS CSV and InFORM GeoJSON in required source checksum checks.
- Calculated observation-support and index-availability counts for both cached and rebuilt paths.
- Clarified facility screening labels and block-group demographic context.
- Replaced the sparse combined hazard overview with polygon-masked county panels.
- Synchronized the opening notebook and README summaries from the accepted run's tables.
- Documented the planned wildfire-occurrence probability model without presenting it as implemented.

## Validation scope

See evidence/release_validation.json for the accepted run, checks, results, and any remaining
publication steps. v3 uses its matching snapshot archive. It preserves source data provenance
while rebuilding analytical products under the revised code.

Earlier v1/v2 clean-environment and UI checks are retained as historical evidence. They do
not certify a new execution. The repeated performance benchmark also retains its original
frozen-input scope. Current full-grid serial/Dask comparison is recorded separately.

Public GitHub deployment and public snapshot upload are not performed by this package.
