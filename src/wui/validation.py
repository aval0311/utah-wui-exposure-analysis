import hashlib
import importlib.metadata
import json
import platform
import psutil
import pandas as pd
import sys
import os
import numpy as np
import rasterio
from pathlib import Path
def hpc_digest(path):
    result = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()

def hpc_require(condition, message):
    if not condition:
        raise RuntimeError(message)

def hpc_environment():
    versions = {}
    for name in ("numpy", "rasterio", "pandas", "psutil", "geopandas", "pyproj", "dask", "distributed", "xarray", "rioxarray"):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = None
    with rasterio.Env():
        gdal_cache = rasterio.env.get_gdal_config("GDAL_CACHEMAX")
    return {
        "python": sys.version, "executable": sys.executable, "platform": platform.platform(),
        "packages": versions, "gdal": rasterio.__gdal_version__, "proj": rasterio.__proj_version__,
        "gdal_cachemax_bytes": gdal_cache, "logical_cpus": psutil.cpu_count(),
        "physical_cpus": psutil.cpu_count(logical=False), "ram_bytes": psutil.virtual_memory().total,
        "environment_variables": {name: os.environ.get(name) for name in (
            "PROJ_DATA", "PROJ_LIB", "GDAL_DATA", "GDAL_CACHEMAX", "GDAL_NUM_THREADS", "OMP_NUM_THREADS",
            "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")},
        "cpu_affinity": psutil.Process().cpu_affinity() if hasattr(psutil.Process(), 'cpu_affinity') else None,
    }

def hpc_compare_output(actual_path, expected_path, tolerance):
    metrics = {"mask_mismatches": 0, "invalid_value_mismatches": 0, "valid_pixels": 0,
               "numeric_differing_pixels": 0, "bitwise_differing_valid_pixels": 0,
               "pixels_exceeding_tolerance": 0, "max_absolute_difference": 0.0,
               "absolute_difference_sum": 0.0, "squared_difference_sum": 0.0,
               "actual_sum": 0.0, "reference_sum": 0.0,
               "actual_minimum": None, "actual_maximum": None,
               "reference_minimum": None, "reference_maximum": None}
    with rasterio.open(actual_path) as actual, rasterio.open(expected_path) as reference:
        checks = {
            "crs": actual.crs == reference.crs, "transform": actual.transform == reference.transform,
            "shape": actual.shape == reference.shape, "bounds": actual.bounds == reference.bounds,
            "dtype": actual.dtypes == reference.dtypes, "nodata": actual.nodatavals == reference.nodatavals,
            "band_count": actual.count == reference.count, "descriptions": actual.descriptions == reference.descriptions,
            "tags": actual.tags() == reference.tags(), "compression": actual.compression == reference.compression,
            "block_shapes": actual.block_shapes == reference.block_shapes,
            "predictor": actual.tags(ns="IMAGE_STRUCTURE").get("PREDICTOR", "1") == reference.tags(ns="IMAGE_STRUCTURE").get("PREDICTOR", "1"),
        }
        metrics["metadata_checks"] = checks
        hpc_require(checks["shape"] and checks["band_count"], "Cannot compare differently shaped outputs.")
        for _, window in reference.block_windows(1):
            a, b = actual.read(1, window=window), reference.read(1, window=window)
            av = np.isfinite(a) & (a != actual.nodata)
            bv = np.isfinite(b) & (b != reference.nodata)
            metrics["mask_mismatches"] += int(np.count_nonzero(av != bv))
            invalid = ~av & ~bv
            metrics["invalid_value_mismatches"] += int(np.count_nonzero(a[invalid] != b[invalid]))
            valid = av & bv
            if not valid.any():
                continue
            xraw, yraw = a[valid], b[valid]
            x, y = xraw.astype("float64"), yraw.astype("float64")
            difference = np.abs(x - y)
            metrics["valid_pixels"] += len(x)
            metrics["numeric_differing_pixels"] += int(np.count_nonzero(x != y))
            if xraw.dtype == yraw.dtype == np.dtype("float32"):
                metrics["bitwise_differing_valid_pixels"] += int(np.count_nonzero(xraw.view("uint32") != yraw.view("uint32")))
            else:
                metrics["bitwise_differing_valid_pixels"] += int(np.count_nonzero(xraw != yraw))
            metrics["pixels_exceeding_tolerance"] += int(np.count_nonzero(difference > tolerance))
            metrics["max_absolute_difference"] = max(metrics["max_absolute_difference"], float(difference.max()))
            metrics["absolute_difference_sum"] += float(difference.sum())
            metrics["squared_difference_sum"] += float(np.square(difference).sum())
            metrics["actual_sum"] += float(x.sum())
            metrics["reference_sum"] += float(y.sum())
            for prefix, values in (("actual", x), ("reference", y)):
                low, high = float(values.min()), float(values.max())
                old_low, old_high = metrics[prefix + "_minimum"], metrics[prefix + "_maximum"]
                metrics[prefix + "_minimum"] = low if old_low is None else min(old_low, low)
                metrics[prefix + "_maximum"] = high if old_high is None else max(old_high, high)
        metrics["profile"] = {"dtype": actual.dtypes[0], "nodata": actual.nodata,
                              "block_shape": actual.block_shapes[0], "compression": actual.compression.value,
                              "predictor": actual.tags(ns="IMAGE_STRUCTURE").get("PREDICTOR", "1")}
    count = metrics["valid_pixels"]
    metrics["mean_absolute_difference"] = metrics.pop("absolute_difference_sum") / count if count else None
    metrics["rmse"] = float(np.sqrt(metrics.pop("squared_difference_sum") / count)) if count else None
    metrics["actual_mean"] = metrics.pop("actual_sum") / count if count else None
    metrics["reference_mean"] = metrics.pop("reference_sum") / count if count else None
    metrics["passed"] = all(checks.values()) and count > 0 and all(metrics[key] == 0 for key in ("mask_mismatches", "invalid_value_mismatches", "pixels_exceeding_tolerance"))
    metrics["atol"] = tolerance
    metrics["rtol"] = 0.0
    metrics["sha256"] = hpc_digest(actual_path)
    metrics["reference_sha256"] = hpc_digest(expected_path)
    metrics["file_bytes_identical"] = metrics["sha256"] == metrics["reference_sha256"]
    metrics["path"] = str(actual_path)
    metrics["reference_path"] = str(expected_path)
    return metrics
