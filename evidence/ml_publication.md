# ML v1 GitHub publication

Publication date: October 16, 2026. Package version: 1.0.0.

The [ML case study](https://aval0311.github.io/utah-wui-exposure-analysis/ml/)
is published alongside the [descriptive dashboard](https://aval0311.github.io/utah-wui-exposure-analysis/).
The [versioned GitHub release](https://github.com/aval0311/utah-wui-exposure-analysis/releases/tag/ml-v1.0.0)
provides the original ZIP and its SHA-256 checksum.

## Publication scope

The complete validated package is copied byte for byte into `docs/ml/`.
Its [50-file manifest](../docs/ml/release_manifest.json) and original validation record
remain intact. The repository README now links to the ML study and describes its results
and limits. The existing descriptive notebook, dashboard, inputs, code, and analytical
outputs are unchanged.

Git attributes disable text conversion inside the immutable ML package so that a Git
checkout preserves its checksums on Windows as well as other platforms. `docs/.nojekyll`
serves the package as static files, preserving the original Markdown, JSON, and other
download paths. The root [repository manifest](../release_file_checksums.json) covers
tracked publication files as stored by Git; the ML package has its own byte-level manifest.

## Pre-publication checks

- All 51 package files match the locally validated release, including its manifest.
- The 50 distributed artifacts pass `python -I -S docs/ml/viewer.py --verify`.
- All 127 package-local HTML/Markdown references resolve; the nine maps and their text descriptions are present.
- The saved notebook contains 11 executed code cells, no error outputs, and nine embedded maps matching the published PNGs. Its sources retain snapshot mode; no notebook execution is required for publication.
- The release ZIP matches its accompanying checksum and contains the same package files.
- Existing tracked repository files are unchanged except for the README and repository checksum manifest. The original 18 analytical notebooks and recorded analytical code hashes are preserved.
- Git-staged package bytes match the original release, and the repository manifest matches the Git-staged files.

The package's [assembly validation](../docs/ml/RELEASE_VALIDATION.md) documents its prior
relocation, HTML/PDF rebuilding, notebook execution, and browser checks. Those checks
were completed during assembly and are not presented as a new analytical run.

Publication does not refresh sources, load fitted models, fit or tune models, generate
predictions, or evaluate later-period observations. Development evidence remains limited
to 2001–2021. The case study retains the approximately 1% relative Brier improvement,
reporting uncertainty, area effects, and retrospective climate limitations. It does not
establish independent final performance or operational readiness.
