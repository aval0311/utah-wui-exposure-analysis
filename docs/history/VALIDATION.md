# Retained historical snapshot validation

Version 0.1.0 · October 16, 2026 · Passed.

This retained record covers the historical base. New saved-prediction checks for
the local 0.2.0 comparison are documented in `COMPARISON_VALIDATION.md`.

## Data and preservation

- Temporal label and flag reads use 2001–2021 bounds at Parquet read time and request only the columns needed for the explorer.
- The snapshot contains 997 cells × 21 years = 20,937 cell-years, including 2,006 positive labels, 231 unknown labels, and 155 annotated flagged zeros.
- All 84 annual summaries and the downloaded CSV are independently recomputed from the distributed cell histories. Positive, ordinary no-record, unknown, and flagged-zero statuses partition each county-year population exactly.
- All 8,973 cell-years in the published 2013–2021 ML map evidence reconcile with the source labels and frozen exclusion mask. The intersection reproduces 8,588 ML-eligible rows and 656 positive rows.
- Consumed frozen source hashes match their original bundle manifests. The original 18 notebooks and 79 recorded analytical code files match the preserved hashes.
- No models, analytical entry points, or historical notebooks are run. No labels are changed. No source data are refreshed. No later-period observation rows are loaded or evaluated.

## Interface and portability

- Browser checks cover the first and last year controls, 2020 reporting coverage, county filtering, chart-year selection, count/rate selection, map selection, cell-history selection, unknown-label display, and map keyboard navigation.
- Selected counts and map colors agree with the saved source summaries in the checked scenarios.
- The annual CSV downloaded through the browser matches the exported file byte for byte.
- Desktop layout and phone widths of 390 px and 320 px show no document overflow; the wide annual chart scrolls within its own region on narrow screens.
- Browser console contains no application errors or warnings in the checked preview.
- Every local HTML reference resolves. Viewing assets have no external script, font, data-fetch, or map-tile dependency. The viewer uses regular local scripts rather than module fetches, so the complete folder can be opened locally.
- The release manifest covers every distributed file other than itself. ZIP member bytes are checked against the folder, and a separate archive SHA-256 is supplied.

This is a practical local review, not a formal accessibility certification or a new
model evaluation. Browser checks used a local HTTP preview; the full folder is also
designed for offline file viewing. The build has not been uploaded or deployed.
