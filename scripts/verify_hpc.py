"""Check scientific edge cases and real multiprocess GeoTIFF export on a small grid."""
import json
import tempfile
from pathlib import Path
import os
import sys
for setting, relative in [('PROJ_DATA','Library/share/proj'),('PROJ_LIB','Library/share/proj'),('GDAL_DATA','Library/share/gdal')]:
    if (Path(sys.prefix)/relative).is_dir():
        os.environ[setting]=str(Path(sys.prefix)/relative)
if os.name=='nt':
    _native=Path(sys.prefix)/'Library/bin'
    if _native.is_dir():
        _dll_handle=os.add_dll_directory(str(_native))
        os.environ['PATH']=str(_native)+os.pathsep+os.environ.get('PATH','')

import numpy as np
import rasterio
from rasterio.transform import from_origin

import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from wui.hpc import hpc_composite_block, hpc_index_class_block, hpc_run_phase12, hpc_require_grid
import xarray as xr

HERE = Path(__file__).resolve().parent


def main():
    spec = json.loads((HERE.parent / 'evidence' / 'phase12_rules.json').read_text())
    rules = spec['analytical_rules']
    keys = rules['component_order']
    weights = dict(zip(keys, [0.3, 0.2, 0.15, 0.1, 0.15, 0.1], strict=True))
    shape = (513, 769)  # Uneven edges exercise partial chunks and TIFF tiles.
    rng = np.random.default_rng(2026)
    components = [rng.random(shape, dtype=np.float32) for _ in keys]
    fuels = np.full(shape, 101, dtype=np.float32)
    counts = np.full(shape, 3, dtype=np.float32)
    study = np.ones(shape, dtype=np.uint8)
    study[0, 0] = 0
    fuels[0, 1:4] = [91, 999, np.nan]
    counts[0, 1:6] = [0, 0, 0, 2, 3]
    components[0][0, 1:6] = -9999

    # Hand-specified precedence includes exclusions with simultaneous missing components.
    normalized, coverage = hpc_composite_block(
        *components, fuels, counts, counts, study,
        weights=tuple(weights.values()), nodata_values=(-9999,) * 6,
        burnable_codes=rules['burnable_codes'],
        nonburnable_codes=rules['confirmed_nonburnable_codes'],
        minimum_observations=3, output_nodata=-9999,
    )
    np.testing.assert_array_equal(coverage[0, :7], [0, 1, 2, 2, 3, 4, 5])
    valid = coverage == 5
    expected = np.zeros(int(valid.sum()), dtype=np.float64)
    for component, weight in zip(components, weights.values(), strict=True):
        expected += component[valid] * float(weight)
    np.testing.assert_array_equal(normalized[valid], expected.astype(np.float32))
    assert np.all(normalized[~valid] == -9999)

    # Float32 values nearest decimal bin boundaries intentionally differ from decimal bins.
    boundaries = []
    for boundary in [0.2, 0.4, 0.6, 0.8]:
        value = np.float32(boundary)
        boundaries.extend([np.nextafter(value, np.float32(-np.inf)), value,
                           np.nextafter(value, np.float32(np.inf))])
    boundary_values = np.array([0, *boundaries, 1, -9999, np.nan], dtype=np.float32)
    index, classes = hpc_index_class_block(boundary_values, -9999)
    np.testing.assert_array_equal(classes, [1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, -9999, -9999])
    np.testing.assert_array_equal(index[:14], 1.0 + boundary_values[:14] * 9.0)

    # Reject a shifted grid instead of allowing xarray to align or interpolate its cells.
    reference_grid = xr.DataArray(np.zeros((2, 2)), dims=('y', 'x'),
                                 coords={'y': [45, 15], 'x': [15, 45]})
    reference_grid = reference_grid.rio.write_crs('EPSG:26912').rio.write_transform(from_origin(0, 60, 30, 30))
    shifted_grid = reference_grid.assign_coords(x=[30, 60]).rio.write_transform(from_origin(15, 60, 30, 30))
    try:
        hpc_require_grid(shifted_grid, reference_grid, 'deliberately shifted grid')
    except ValueError:
        pass
    else:
        raise AssertionError('A half-pixel spatial shift was accepted.')

    with tempfile.TemporaryDirectory(prefix='hpc-check-', dir=HERE) as directory:
        root = Path(directory)
        profile = dict(driver='GTiff', width=shape[1], height=shape[0], count=1,
                       crs='EPSG:26912', transform=from_origin(228570, 4530600, 30, 30),
                       tiled=True, blockxsize=256, blockysize=256, compress='deflate')
        def write(name, array, nodata):
            path = root / f'{name}.tif'
            with rasterio.open(path, 'w', **profile, dtype=str(array.dtype), nodata=nodata) as dst:
                dst.write(array, 1)
            return path
        component_paths = {key: write(key, array, -9999)
                           for key, array in zip(keys, components, strict=True)}
        fuel_path = write('fuels', np.where(np.isfinite(fuels), fuels, -9999).astype('int16'), -9999)
        count_path = write('counts', counts.astype('uint16'), 0)
        mask_path = write('mask', study, None)
        outputs = {key: root / 'outputs' / f'{key}.tif' for key in (
            'normalized_hazard', 'continuous_index_1_10', 'hazard_class', 'coverage_reason')}
        labels = {1: 'Nonburnable', 2: 'Unknown fuel', 3: 'HLS support', 4: 'Other missing', 5: 'Modeled'}
        model = {'name': 'Test', 'version': 'test', 'coverage_labels': labels, 'study_pixels': int(study.sum())}
        config = {'chunk_shape': [256, 512], 'n_workers': 2, 'threads_per_worker': 1,
                  'processes': True, 'memory_limit': '2GiB', 'spill_directory': str(root / 'spill')}
        result = hpc_run_phase12(component_paths, weights, fuel_path, count_path, count_path,
                                mask_path, outputs, rules, model, config)
        expected_index, expected_classes = hpc_index_class_block(normalized, -9999)
        expected_arrays = {'normalized_hazard': normalized, 'continuous_index_1_10': expected_index,
                           'hazard_class': expected_classes, 'coverage_reason': coverage}
        descriptions = {'normalized_hazard': 'Normalized Composite Fire Hazard',
                        'continuous_index_1_10': 'Composite Fire Hazard Index (1-10)',
                        'hazard_class': 'Composite Fire Hazard Class', 'coverage_reason': None}
        expected_tags = {
            'normalized_hazard': {'MODEL_NAME': 'Test', 'MODEL_VERSION': 'test', 'WEIGHT_SUM': '1.0',
                                  'SCORE_MINIMUM': '0.0', 'SCORE_MAXIMUM': '1.0', 'AREA_OR_POINT': 'Area'},
            'continuous_index_1_10': {'AREA_OR_POINT': 'Area'},
            'hazard_class': {'1': 'Very Low', '2': 'Low', '3': 'Moderate', '4': 'High', '5': 'Very High',
                             'AREA_OR_POINT': 'Area'},
            'coverage_reason': {**{f'CODE_{code}': label for code, label in labels.items()}, 'AREA_OR_POINT': 'Area'},
        }
        for key, output in outputs.items():
            with rasterio.open(output) as src:
                np.testing.assert_array_equal(src.read(1), expected_arrays[key])
                assert src.transform == profile['transform'] and src.crs.to_epsg() == 26912
                assert src.block_shapes == [(256, 256)]
                assert src.nodata == (0 if key == 'coverage_reason' else -9999)
                assert src.descriptions == (descriptions[key],), (key, src.descriptions)
                assert src.tags() == expected_tags[key], (key, src.tags())
                assert src.tags(ns='IMAGE_STRUCTURE').get('PREDICTOR', '1') == ('1' if key == 'coverage_reason' else '3')
        assert result['coverage_counts'][1:] == np.bincount(coverage[study.astype(bool)], minlength=6)[1:].tolist()
        try:
            hpc_run_phase12(component_paths, weights, fuel_path, count_path, count_path,
                            mask_path, outputs, rules, model, config)
        except FileExistsError:
            pass
        else:
            raise AssertionError('Existing outputs were not protected.')
    print('PASS: coverage precedence, ordered float32 arithmetic, boundary classes, uneven chunks,')
    print('      multiprocess locked exports, exact geospatial metadata, and overwrite protection.')


if __name__ == '__main__':
    main()
