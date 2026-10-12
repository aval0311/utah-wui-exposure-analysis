# Clean-environment validation — passed

The delivered release and matching data snapshot reproduced successfully in a new
Windows conda environment. The original environment specification resolved and
installed without edits. No notebook-code or scientific-data changes were required.

## What was tested

- Both supplied archives passed SHA-256 verification and were extracted into new directories.
- 306 packages were installed from conda-forge using a separate package cache.
- All 24 pinned requirements match environment.yml.
- A private Jupyter kernel used the new environment, with user-site packages disabled.
- Input integrity, temporal-median handling, snapshot policy, and real multiprocess
  Dask checks passed.
- The complete notebook ran with cleared outputs in snapshot mode in **24.4 minutes**
  (1465.568 seconds), including notebook input verification and
  finalization. Installation and preliminary tests are excluded from this timing.
- All four complete output rasters match the accepted release bit for bit, including
  their masks, with matching raster metadata.
- All six published CSV result tables match exactly.
- Saved notebook outputs contain no execution errors or runtime-warning outputs.

This is functional reproduction evidence from one run, not a new performance benchmark.
It uses the snapshot's retained data and reusable derivatives with the published defaults.

## Startup messages

The validation launcher logged two Jupyter startup messages: pyzmq selected a compatibility
thread for Windows event-loop support, and the kernel reported unencrypted TCP transport.
The private kernel used local loopback. Neither message prevented execution or changed
the analytical results. These were separate from the notebook's computation outputs.

## Files and remaining checks

The retained workspace and original Git repository were unchanged; the Git status remains
clean. The original release archives were preserved. The accompanying updated code ZIP
adds this validation evidence and updates its handoff notes. It uses the **same matching
data snapshot**, so another data download is unnecessary if you already have that archive.

The exact Windows package builds are recorded in environment-win-64-explicit.txt and
clean_environment_installed_packages.json, both under evidence/ in the updated code ZIP.
These are environment records; they are not cross-platform locks.

Full live refresh, a forced rebuild of every derivative, other operating systems,
public hosting, native fullscreen, and physical-phone behavior were not tested here.
The existing scientific limitations remain documented in the release.
