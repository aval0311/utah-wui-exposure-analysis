# Local package validation — October 18, 2026

- All 12 synthetic tests passed in the retained Windows Conda environment.
- Summary-only verification reproduced mean annual Brier scores and the 4.91% relative error increase; cell history won all nine years.
- The original experiment source matches the SHA-256 recorded in the completed run configuration.
- Copied source files were hash-checked before and after copying.
- No original observation tables were opened, no models were fitted, and no later-period observations were accessed during package preparation or tests.
- A fresh environment installation and full adapter-based real-data rerun were not performed. See ENVIRONMENT.md and REPRODUCIBILITY.md.
- The package was tested locally before publication. Publication adds this code package and presentation links; existing releases and analytical inputs remain unchanged.
