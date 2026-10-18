# Environment requirements

`review.py` uses Python standard-library modules only (Python 3.10+). Tests and the optional exact-input rerun require the numerical stack in `requirements.txt`.

The completed experiment recorded Python 3.14.7, NumPy 2.4.6, pandas 3.0.6, SciPy 1.18.0 and scikit-learn 1.9.1. PyArrow 25.0.0 was inspected in the retained environment during packaging; it was not recorded in the original frozen configuration. Exact package pins describe the inspected environment, not a claim that every platform can resolve these versions.

For an isolated environment with a compatible Python, the intended installation is:

```text
python -m venv .venv
# Activate the environment using your platform's normal command.
python -m pip install -r requirements.txt
python -I run.py test
```

A clean dependency installation **passed on Windows x64 with Python 3.14.7 on October 18, 2026**. A fresh virtual environment installed all five pinned dependencies from PyPI without cache reuse. All 12 synthetic tests and the summary check passed; `pip check` found no broken requirements. NumPy, pandas, SciPy, scikit-learn and PyArrow were confirmed to load from that environment. Inherited Conda/Python variables were removed and PATH was restricted to the virtual environment and Windows directories during checks.

The virtual environment shares the existing conda-forge Python interpreter and standard library. System site-packages were excluded and user site was disabled. This is a clean package installation on the same Windows machine, not a fresh operating system or independent Python distribution.

Requirements pin direct dependencies only. [Resolved dependencies](validation/resolved_dependencies.txt) record this successful installation, but are not a cross-platform lockfile or a replacement requirements file. Transitive resolution can change. Other Python versions, distributions and operating systems remain untested; the Python 3.10+ standard-library compatibility claim was not exercised on older interpreters. Numerical tolerances allow small floating-point differences; byte-identical reruns across platforms are not promised.

The first pip bootstrap attempt hit a sandbox temporary-directory permission error. Retrying outside that restriction succeeded without changing package code or the existing analytical environment. Full real-data stages were not run. See [VALIDATION.md](VALIDATION.md).

On Windows the original module prepends its interpreter's existing Conda DLL directories to the process PATH before numerical imports. Use `run.py test` rather than importing the original test module first. This does not modify system environment settings. Matplotlib is not needed: figure generation is outside this package.
