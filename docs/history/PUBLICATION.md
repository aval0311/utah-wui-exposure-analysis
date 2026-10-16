# Historical occurrence timeline publication

Version 0.1.0 · October 16, 2026.

The [historical timeline](https://aval0311.github.io/utah-wui-exposure-analysis/history/)
is linked from the main WUI dashboard. The [GitHub release](https://github.com/aval0311/utah-wui-exposure-analysis/releases/tag/history-v0.1.0)
includes the complete offline ZIP and its SHA-256 checksum.

This publication uses the reviewed local snapshot: 997 cells across 2001–2021,
20,937 cell-years, 2,006 positive cell-years, 231 unknown labels, and 155 annotated
flagged zeros. Positive cell-years are not unique incident counts. Rates use known
reviewed labels, retaining flagged zeros; the ML evaluation uses different exclusions.
Data files, map paths, application code, and styles match the reviewed build.
Only publication wording and this handoff are added; the manifest is regenerated.

No original analytical inputs are read for publication. No models are loaded or
fitted, no predictions are generated, and no 2024–2025 observations are accessed.
The frozen ML package, existing notebooks, and analytical outputs are preserved.
See VALIDATION.md and data/provenance.json for the prior checks and source lineage.
