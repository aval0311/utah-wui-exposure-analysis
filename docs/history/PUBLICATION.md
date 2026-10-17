# History and saved ML comparison publication

Version 0.2.0 · October 17, 2026.

The [updated timeline](https://aval0311.github.io/utah-wui-exposure-analysis/history/)
is linked prominently from the main WUI dashboard as “Timeline + ML comparison”.
The [release](https://github.com/aval0311/utah-wui-exposure-analysis/releases/tag/history-v0.2.0)
provides the offline viewer ZIP and SHA-256 checksum.

This release adds saved 2013–2021 geographic holdout predictions and reviewed
findings to the unchanged 2001–2021 historical data. All 8,973 saved rows reconcile;
the matched comparison uses 8,588 eligible cell-years and 656 positives, excluding
230 unknown labels and 155 frozen flagged-zero rows. No missing probability is
converted to zero. The original annual three-county ranking budget is retained.

The reviewed local application, styles, findings, and data are retained. Only
publication wording and this handoff change; the manifest is regenerated.
The findings are descriptive development evidence, not independent final
evaluation, operational readiness, or future forecasting performance.

No analytical sources, models, or notebooks are opened for publication. No fitting,
inference, source refresh, or 2024–2025 observation access occurs. The frozen ML
release remains byte-identical. Prior historical release history remains available.
See ML_COMPARISON.md, COMPARISON_VALIDATION.md, and data/ml_provenance.json.
