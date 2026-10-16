# Publication handoff

This folder is the standalone ML entry point. Its HTML can be opened locally or served as static files. Nothing in this assembly step publishes content, changes the baseline repository, or modifies a remote branch.

For an eventual portfolio release, place the complete folder under a separate ML path, retain all relative paths, and link to its `index.html` and `README.md`. Keep the baseline notebook, inputs, existing dashboard and analytical outputs intact. Review the deployed links after upload; no hosted deployment is part of the local validation.

Suggested entry text: **ML v1 development case study** — annual recorded wildfire occurrence with spatial and temporal validation, probability calibration, ranking trade-offs and a clipped-area audit; development 2001–2021.

The publication copy adds no fitted models or later-period predictions. `release_manifest.json` identifies every distributed file; `data/source_provenance.json` records unchanged source-image and table hashes and documents transformed prose and metadata. Retain the ZIP checksum alongside the release download. The accompanying project citation gives author, title, version and date without inventing a DOI or claiming a hosted release already exists.

The next action is review and publication of this assembled copy. Model retraining and final-test evaluation are separate decisions and are not part of publication.
