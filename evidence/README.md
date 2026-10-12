# Validation evidence

Current release checks are summarized in **release_validation.json** and **release_validation.md**.
They identify the accepted run and the scope of each check.

- current_run_manifest.json: accepted execution, inputs, coverage, runtime, and acquisition activity.
- current_historical_occurrence_selection.json: reconciling event-type, date, and spatial selection.
- current_serial_dask_equivalence.json: independent serial comparison against the accepted Dask products.
- static_publication_checks.json: executed notebook, syntax, links, warnings, and path checks.
- browser_v3/: current local dashboard interaction report and screenshots.
- publication_revision_review.md: changes made in response to the publication audit.
- reference/serial_reference.json: retained independent serial implementation used for current comparison.

## Retained evidence

benchmark_summary.json, benchmark_runs/, benchmark_comparisons/, step4_report.txt,
matched_performance.png, historical_correctness.json, and historical_evidence_provenance.json
belong to the original matched composite experiment. They establish the reported historical
timing and memory tradeoff. They are not a new v3 benchmark.

history/v2/ contains the earlier release's execution, clean-environment, equivalence, and
browser reports. The current release's report separately describes reuse of that independently
created environment for a new execution. Historical browser and fullscreen checks do not by
themselves establish current public-deployment behavior.

environment-win-64-explicit.txt records the retained tested environment. The root environment.yml
is the portable environment specification; exact availability on another platform may differ.
