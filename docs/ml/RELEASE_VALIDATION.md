# Release validation

**Passed for local release 1.0.0, October 16, 2026.** This is a standalone retrospective development portfolio, using 2001–2021 evidence and 2013–2021 annual maps. It is ready for publication review. No hosted deployment was performed.

## Completed checks

| Check | Result |
| --- | --- |
| Release inventory | 50 files covered by SHA-256 and byte-size checks, plus the manifest itself |
| Local references | 127 HTML/Markdown links resolved inside the extracted folder or to valid local anchors |
| Frozen source copies | 24 byte-identical source copies, including all nine map PNGs |
| Snapshot notebook | 11 code cells executed successfully in a fresh kernel; no saved errors; all nine embedded maps equal the source bytes |
| Saved map evidence | 8,973 cell-years, 8,588 eligible rows, 656 recorded positives; parsed years end at 2021 |
| County descriptions | All 27 county-year summaries match eligible saved probabilities and top-decile counts |
| HTML portability | Relocated copy verified and rebuilt from another current directory with `python -I -S`; HTML bytes identical; no installed packages, remote fonts or scripts required |
| Integrity failure detection | Deliberately changing a copied evidence file caused verification to fail |
| Atlas | 11 pages with native searchable text; nine embedded maps retain original pixels; all pages visually reviewed; identical PDF rebuilt after relocation |
| Browser | Annual navigation and full-resolution map link worked; all nine images loaded; desktop and phone-width checks showed no document overflow; tables scroll within their own regions; no console errors or warnings |
| Public metadata | No absolute working-machine paths or private chat links in the distributed text files |
| Protected analysis | All 18 original notebooks and 19 output bundles preserved, along with code, source archives, environment and protected decision documents |
| Baseline | 1,077 inventoried files checked for size/mtime; five control files and five consumed assets rehashed; baseline repository remains clean |

The baseline notebook SHA-256 remains `13ff72d7367edbccbf5c12634f8a41ff1efaa3e46a874d692d60df3c7b002d5c`. The earlier full baseline archive hash audit remains the reference for that complete archive; this release check does not claim to rehash every baseline byte.

This step loaded no model objects, fitted no models and generated no model predictions. No 2024–2025 observation or prediction rows were parsed or evaluated. Older artifacts were hashed only to verify preservation.

## Interpretation and reproduction limits

These development years informed model and calibration choices. The package does not establish independent final performance, statewide transfer or operational readiness. Reporting coverage, the 2020 source transition, contemporary terrain, retrospective climate and unequal cell areas remain disclosed analytical limitations.

The [reproduction guide](REPRODUCIBILITY.md) distinguishes reproducing this presentation from rerunning the original training. The complete training inputs and fitted models are not part of this release. HTML supplies semantic headings, image descriptions and native tables; the PDF adds searchable captions but is not certified as tagged PDF/UA. Browser checks are practical layout checks, not a formal accessibility certification.

External citations were documented separately from the local-link checks. All viewing assets are local; no promise is made that external provider URLs will remain unchanged. [Publication handoff](PUBLISHING.md) describes the remaining hosting and portfolio-entry steps. Verify deployed links after upload.

Run `python -I -S viewer.py --verify` to check the distributed files. Keep the accompanying ZIP checksum and original archive as the release reference. [Source provenance](data/source_provenance.json) records copied hashes and presentation transformations.
