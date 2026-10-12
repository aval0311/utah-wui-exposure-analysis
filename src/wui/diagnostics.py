"""Windowed diagnostics calculated consistently for reused and rebuilt rasters."""
import numpy as np
import rasterio


def observation_support_count(count_path, study_mask, minimum):
    """Count study cells below the minimum, including cells with no observations."""
    total = 0
    with rasterio.open(count_path) as source:
        if source.shape != study_mask.shape:
            raise ValueError('Observation counts and study mask have different shapes.')
        for _, window in source.block_windows(1):
            r, c = int(window.row_off), int(window.col_off)
            h, w = int(window.height), int(window.width)
            counts = source.read(1, window=window)
            study = study_mask[r:r+h, c:c+w]
            valid = np.isfinite(counts)
            if source.nodata is not None:
                valid &= counts != source.nodata
            total += int(np.count_nonzero(study & (~valid | (counts < minimum))))
    return total


def index_availability_counts(ndvi_path, ndmi_path, study_mask):
    """Count disjoint normalized-index availability categories inside the study area."""
    result = dict(both=0, ndvi_only=0, ndmi_only=0, neither=0)
    with rasterio.open(ndvi_path) as a, rasterio.open(ndmi_path) as b:
        if (a.shape, a.transform, a.crs) != (b.shape, b.transform, b.crs) or a.shape != study_mask.shape:
            raise ValueError('Normalized indices and study mask must share one grid.')
        for _, window in a.block_windows(1):
            r, c = int(window.row_off), int(window.col_off)
            h, w = int(window.height), int(window.width)
            study = study_mask[r:r+h, c:c+w]
            av = a.read(1, window=window, masked=True)
            bv = b.read(1, window=window, masked=True)
            va = ~np.ma.getmaskarray(av) & np.isfinite(av.data)
            vb = ~np.ma.getmaskarray(bv) & np.isfinite(bv.data)
            for key, mask in [('both', va & vb), ('ndvi_only', va & ~vb),
                              ('ndmi_only', ~va & vb), ('neither', ~va & ~vb)]:
                result[key] += int(np.count_nonzero(study & mask))
    if sum(result.values()) != int(study_mask.sum()):
        raise AssertionError('Index availability counts must partition the study area.')
    return result
