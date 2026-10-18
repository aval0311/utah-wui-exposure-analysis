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

A clean installation has not been tested. The package is tested in the retained Windows Conda environment; requirements are direct dependencies, not a complete transitive lock or OS/BLAS specification. Numerical tolerances allow small floating-point differences; byte-identical reruns across platforms are not promised.

On Windows the original module prepends its interpreter's existing Conda DLL directories to the process PATH before numerical imports. Use `run.py test` rather than importing the original test module first. This does not modify system environment settings. Matplotlib is not needed: figure generation is outside this package.
