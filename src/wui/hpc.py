"""Chunked Phase 12 implementation, embedded verbatim in the delivered notebook."""
from contextlib import ExitStack
from pathlib import Path
import gc
import time
import uuid

import dask
import dask.array as da
import numpy as np
import rasterio
import rioxarray
import xarray as xr
from distributed import Client, LocalCluster, Lock


# Preserve NumPy's operation order inside each chunk, including float32 products.
def hpc_composite_block(*arrays, weights, nodata_values, burnable_codes,
                        nonburnable_codes, minimum_observations, output_nodata):
    """Build normalized hazard and disjoint coverage reasons for one aligned chunk."""
    components = arrays[:6]
    fuels, ndvi_counts, ndmi_counts, study = arrays[6:]
    study = study.astype(bool)

    # Require every component while keeping policy exclusion ahead of missing data.
    complete = study.copy()
    for values, nodata in zip(components, nodata_values, strict=True):
        complete &= np.isfinite(values) & (values != nodata)
    nonburnable = np.isin(fuels, nonburnable_codes)
    burnable = np.isin(fuels, burnable_codes)
    supported = ((ndvi_counts >= minimum_observations)
                 & (ndmi_counts >= minimum_observations))
    reason = np.zeros(study.shape, dtype=np.uint8)
    reason[study & nonburnable] = 1
    reason[study & ~(nonburnable | burnable)] = 2
    eligible = study & burnable
    reason[eligible & ~supported] = 3
    reason[eligible & supported & ~complete] = 4
    reason[eligible & supported & complete] = 5
    if np.any(study & (reason == 0)):
        raise AssertionError('Study-area coverage classification is incomplete.')

    # Use float64 accumulation of ordered float32 weighted terms, as in the baseline.
    valid = reason == 5
    normalized = np.full(study.shape, output_nodata, dtype=np.float32)
    if valid.any():
        combined = np.zeros(int(valid.sum()), dtype=np.float64)
        for values, weight in zip(components, weights, strict=True):
            combined += values[valid] * float(weight)
        normalized[valid] = np.clip(combined, 0.0, 1.0).astype(np.float32)
    return normalized, reason


# Apply the original transformations to the saved float32 normalized raster.
def hpc_index_class_block(normalized, nodata):
    """Create the continuous 1-10 index and the exact baseline hazard classes."""
    valid = np.isfinite(normalized) & (normalized != nodata)
    index = np.full(normalized.shape, nodata, dtype=np.float32)
    classes = np.full(normalized.shape, nodata, dtype=np.float32)
    index[valid] = 1.0 + normalized[valid] * 9.0

    # Keep Python-list bins and right=True; rounding or float32 bins changes classes.
    classes[valid] = np.digitize(
        normalized[valid], bins=[0.2, 0.4, 0.6, 0.8], right=True,
    ).astype(np.float32) + 1.0
    return index, classes


def hpc_coverage_count_block(reason):
    """Return six counts per chunk without gathering a full raster on the client."""
    return np.bincount(reason.ravel(), minlength=6).reshape(1, 1, 6)


# Reject spatial differences explicitly instead of allowing implicit realignment.
def hpc_require_grid(array, reference, label):
    """Require identical spatial dimensions, coordinates, CRS, and affine transform."""
    if not (array.dims == ('y', 'x') and array.shape == reference.shape
            and array.rio.crs == reference.rio.crs
            and array.rio.transform(recalc=False) == reference.rio.transform(recalc=False)
            and array.rio.bounds() == reference.rio.bounds()
            and array.rio.resolution() == reference.rio.resolution()):
        raise ValueError(f'Raster does not match the frozen analytical grid: {label}')
    xr.align(array, reference, join='exact', copy=False)


def hpc_open_raster(stack, path, chunk_shape, masked=False):
    """Open a lazily loaded single-band raster and close its owner after computation."""
    owner = rioxarray.open_rasterio(
        path, chunks={'band': 1, 'y': chunk_shape[0], 'x': chunk_shape[1]},
        masked=masked, mask_and_scale=False, cache=False, lock=False,
    )
    stack.callback(owner.close)
    if owner.sizes['band'] != 1:
        raise ValueError(f'Expected one raster band: {path}')
    array = owner.squeeze('band', drop=True)
    if not isinstance(array.data, da.Array):
        raise TypeError('Raster input is not backed by a Dask array.')
    return array


# Construct output metadata afresh so input band labels and tags cannot leak into exports.
def hpc_output_array(array, reference, nodata, description=None):
    """Attach the unchanged grid and output NoData to a lazy result."""
    result = xr.DataArray(array.data, dims=('y', 'x'),
                          coords={'y': reference.y, 'x': reference.x})
    # An explicit array name sets the band description without adding a long_name TIFF tag.
    result.name = description
    result = result.rio.write_crs(reference.rio.crs)
    result = result.rio.write_transform(reference.rio.transform(recalc=False))
    result = result.rio.write_nodata(nodata)
    return result


def hpc_write_task(array, temporary_path, client, predictor, tags=None):
    """Prepare a locked Dask export; computation must finish before file promotion."""
    # Concurrent tasks may write different windows, but each TIFF has one writer at a time.
    # A distributed lock works across worker processes; a threading lock would not.
    return array.rio.to_raster(
        temporary_path, driver='GTiff', dtype=str(array.dtype),
        compress='deflate', predictor=predictor, tiled=True,
        blockxsize=256, blockysize=256, BIGTIFF='IF_SAFER',
        recalc_transform=False, tags=tags or {},
        lock=Lock(f'wui-write-{uuid.uuid4().hex}'), compute=False,
    )


def hpc_build_composite(component_paths, weights, fuel_path, ndvi_path, ndmi_path,
                        mask_path, output_paths, chunk_shape, client, rules, model):
    """Read aligned chunks, calculate two products, count coverage, and close exports."""
    temporary = {key: Path(output_paths[key]).with_suffix('.part.tif')
                 for key in ('normalized_hazard', 'coverage_reason')}
    with ExitStack() as stack:
        components = [hpc_open_raster(stack, path, chunk_shape)
                      for path in component_paths.values()]
        reference = components[0]
        supporting = [
            hpc_open_raster(stack, fuel_path, chunk_shape, masked=True),
            hpc_open_raster(stack, ndvi_path, chunk_shape, masked=True).fillna(0),
            hpc_open_raster(stack, ndmi_path, chunk_shape, masked=True).fillna(0),
            hpc_open_raster(stack, mask_path, chunk_shape),
        ]
        for label, array in zip(
            [*component_paths, 'aligned_fbfm40', 'ndvi_count', 'ndmi_count', 'study_mask'],
            [*components, *supporting], strict=True,
        ):
            hpc_require_grid(array, reference, label)

        # xarray keeps labeled y/x coordinates; Dask calls the NumPy kernel per chunk.
        normalized, coverage = xr.apply_ufunc(
            hpc_composite_block, *components, *supporting,
            input_core_dims=[[]] * 10, output_core_dims=[[], []],
            dask='parallelized', vectorize=False, join='exact',
            output_dtypes=[np.float32, np.uint8], keep_attrs=False,
            kwargs={
                'weights': tuple(float(weights[key]) for key in component_paths),
                'nodata_values': tuple(array.rio.nodata for array in components),
                'burnable_codes': tuple(rules['burnable_codes']),
                'nonburnable_codes': tuple(rules['confirmed_nonburnable_codes']),
                'minimum_observations': rules['minimum_ndvi_observations'],
                'output_nodata': rules['excluded_hazard_cells'],
            },
        )
        normalized = hpc_output_array(
            normalized, reference, rules['excluded_hazard_cells'],
            'Normalized Composite Fire Hazard',
        )
        coverage = hpc_output_array(coverage, reference, 0)
        normalized_task = hpc_write_task(normalized, temporary['normalized_hazard'], client, 3, {
            'MODEL_NAME': model['name'], 'MODEL_VERSION': model['version'],
            'WEIGHT_SUM': sum(weights.values()), 'SCORE_MINIMUM': 0.0, 'SCORE_MAXIMUM': 1.0,
        })
        coverage_task = hpc_write_task(coverage, temporary['coverage_reason'], client, 1, {
            f'CODE_{code}': label for code, label in model['coverage_labels'].items()
        })
        counts_task = coverage.data.map_blocks(
            hpc_coverage_count_block, dtype=np.int64, chunks=(1, 1, 6), new_axis=2,
        ).sum(axis=(0, 1), dtype=np.int64)

        # Submit exports and counts together so shared chunk calculations are reused.
        _, _, counts = dask.compute(normalized_task, coverage_task, counts_task)
        counts[0] = 0  # Outside-study cells do not contribute to the coverage summary.

    for key, temporary_path in temporary.items():
        if not temporary_path.is_file() or temporary_path.stat().st_size == 0:
            raise RuntimeError(f'Export was not materialized: {temporary_path}')
        temporary_path.replace(output_paths[key])
    if int(counts.sum()) != model['study_pixels'] or int(counts[5]) == 0:
        raise AssertionError('Coverage categories do not reconcile with the study-area mask.')
    return counts


def hpc_build_index_classes(output_paths, chunk_shape, client, nodata):
    """Reopen saved float32 scores and export both derived products lazily."""
    temporary = {key: Path(output_paths[key]).with_suffix('.part.tif')
                 for key in ('continuous_index_1_10', 'hazard_class')}
    with ExitStack() as stack:
        normalized = hpc_open_raster(stack, output_paths['normalized_hazard'], chunk_shape)
        index, classes = xr.apply_ufunc(
            hpc_index_class_block, normalized, kwargs={'nodata': nodata},
            input_core_dims=[[]], output_core_dims=[[], []],
            dask='parallelized', vectorize=False, output_dtypes=[np.float32, np.float32],
            keep_attrs=False,
        )
        index = hpc_output_array(index, normalized, nodata, 'Composite Fire Hazard Index (1-10)')
        classes = hpc_output_array(classes, normalized, nodata, 'Composite Fire Hazard Class')
        index_task = hpc_write_task(index, temporary['continuous_index_1_10'], client, 3)
        class_task = hpc_write_task(classes, temporary['hazard_class'], client, 3, {
            '1': 'Very Low', '2': 'Low', '3': 'Moderate', '4': 'High', '5': 'Very High',
        })
        dask.compute(index_task, class_task)
    for key, temporary_path in temporary.items():
        if not temporary_path.is_file() or temporary_path.stat().st_size == 0:
            raise RuntimeError(f'Export was not materialized: {temporary_path}')
        temporary_path.replace(output_paths[key])
    gc.collect()


def hpc_run_phase12(component_paths, weights, fuel_path, ndvi_path, ndmi_path,
                    mask_path, output_paths, rules, model, config):
    """Run both stages in one timed call with cluster startup and teardown separated."""
    if tuple(component_paths) != tuple(rules['component_order']) or len(component_paths) != 6:
        raise ValueError('The frozen six-component order must be preserved.')
    if not np.isclose(sum(weights.values()), 1.0, atol=1e-9):
        raise ValueError('Component weights must sum to 1.0.')
    if rules['minimum_ndvi_observations'] != rules['minimum_ndmi_observations']:
        raise ValueError('This frozen model requires the same HLS threshold for both counts.')
    chunk_shape = tuple(config['chunk_shape'])
    if len(chunk_shape) != 2 or any(not isinstance(n, int) or n < 256 or n % 256 for n in chunk_shape):
        raise ValueError('Chunk dimensions must be positive multiples of the 256-pixel TIFF tiles.')
    for path in output_paths.values():
        path = Path(path)
        if path.exists() or path.with_suffix('.part.tif').exists():
            raise FileExistsError(f'Choose a new run directory; output already exists: {path}')
        path.parent.mkdir(parents=True, exist_ok=True)
    spill_directory = Path(config['spill_directory'])
    spill_directory.mkdir(parents=True, exist_ok=True)
    stages = {}
    started = time.perf_counter_ns()

    # The cluster is local to this run and closes even when a calculation or export fails.
    with LocalCluster(
        n_workers=config['n_workers'], threads_per_worker=config['threads_per_worker'],
        processes=config['processes'], memory_limit=config['memory_limit'],
        local_directory=str(spill_directory), dashboard_address=None, host='127.0.0.1',
        silence_logs=40,
    ) as cluster, Client(cluster) as client:
        client.wait_for_workers(config['n_workers'])
        ready = time.perf_counter_ns()
        stages['cluster_startup'] = {'start_ns': started, 'end_ns': ready, 'seconds': (ready-started)/1e9}
        workers = client.scheduler_info()['workers']
        worker_config = {address: {'nthreads': details['nthreads'], 'memory_limit': details['memory_limit']}
                         for address, details in workers.items()}
        print(f'-> Dask workers ready: {len(workers)}; chunks: {chunk_shape}', flush=True)

        # Include input opening, graph construction, actual computation, four exports,
        # saved-score rereading, coverage checks, file promotion, and final cleanup.
        start = time.perf_counter_ns()
        counts = hpc_build_composite(
            component_paths, weights, fuel_path, ndvi_path, ndmi_path, mask_path,
            output_paths, chunk_shape, client, rules, model,
        )
        composite_end = time.perf_counter_ns()
        hpc_build_index_classes(output_paths, chunk_shape, client, rules['excluded_hazard_cells'])
        end = time.perf_counter_ns()
        stages['primary_compute_export'] = {'start_ns': start, 'end_ns': end, 'seconds': (end-start)/1e9}
        stages['composite_and_coverage'] = {'start_ns': start, 'end_ns': composite_end, 'seconds': (composite_end-start)/1e9}
        stages['index_and_class'] = {'start_ns': composite_end, 'end_ns': end, 'seconds': (end-composite_end)/1e9}
        teardown_start = time.perf_counter_ns()
    closed = time.perf_counter_ns()
    stages['cluster_teardown'] = {'start_ns': teardown_start, 'end_ns': closed, 'seconds': (closed-teardown_start)/1e9}
    return {'coverage_counts': counts.tolist(), 'stages': stages, 'config': dict(config),
            'workers': worker_config, 'outputs': {key: str(path) for key, path in output_paths.items()},
            'purpose': 'Current Phase 12 execution; repeated benchmark evidence is separate.'}
