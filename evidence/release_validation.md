# Release v3 validation

**Passed. Accepted run: 20261012T180540Z_eb3fdcb7.**

The delivered notebook executed all 158 code cells in a fresh kernel using
DATA_MODE="snapshot" and REBUILD_DERIVED=False, from a new extraction of the matching data
archive. It contains no recorded errors or Python warning outputs.

A preceding full derivative rebuild also completed. The default replay agrees exactly with
that rebuild on all four final rasters and six exported tables. A separate retained serial
implementation agrees with the accepted Dask result across all four outputs, with zero
differing valid pixels. The source comparison found no byte changes among
526 immutable source files.

The matching archive passed complete ZIP integrity verification. Its 1067
required analytical inputs and the recipe fingerprint passed pre-execution validation.
All recorded acquisition actions were snapshot reads; the kernel's external-network guard
was active. Browser libraries and basemap tiles remain online dependencies.

The accepted run's figures were visually reviewed. Browser checks covered desktop widths
1440 and 1366, mobile widths 390 and 360, short landscape layout, layer controls, basemaps,
opacity, contextual legend, popup bounds and scrolling, drawer/Escape behavior, reset, and
Fullscreen API entry/exit with both popup types. The browser report distinguishes the
tested rebuilt candidate from the final accepted HTML and records their comparison.

The prior independently created environment was reused with a new kernel and user-site
packages disabled; every pinned environment version still matched. This release did not
repeat environment installation or the historical matched benchmark.

Both protected locations retained their original file inventories, byte sizes, and
modification times. No repository update, Git commit, push, public deployment, or public
snapshot upload was performed.

Detailed measurements and scope appear in release_validation.json and the linked evidence
index. Follow RELEASE_HANDOFF.md for manual publication and public-site verification.
