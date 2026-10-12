"""Explicit event, time, and spatial selection for the historical occurrence proxy."""
import pandas as pd


def select_wildfire_occurrences(frame, counties, start, end_exclusive):
    """Select recorded WF ignitions in a fixed period and county bounding rectangle.

    The rectangle retains surrounding records for density smoothing. County counts
    are reported separately; the resulting raster is masked to the study footprint.
    No claim of ignition probability follows from this descriptive event density.
    """
    required = {'IncidentTypeCategory', 'FireDiscoveryDateTime', 'OBJECTID', 'geometry'}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f'Historical occurrences lack required fields: {sorted(missing)}')
    if frame.crs is None or counties.crs is None:
        raise ValueError('Historical occurrences and county polygons require a CRS.')
    if frame['OBJECTID'].isna().any() or frame['OBJECTID'].duplicated().any():
        raise ValueError('Historical occurrence OBJECTIDs must be present and unique.')
    start_time, end_time = pd.Timestamp(start, tz='UTC'), pd.Timestamp(end_exclusive, tz='UTC')
    if end_time <= start_time:
        raise ValueError('The historical observation interval must have positive duration.')
    frame = frame.to_crs(counties.crs).copy()
    dates = pd.to_datetime(pd.to_numeric(frame['FireDiscoveryDateTime'], errors='coerce'),
                           unit='ms', utc=True, errors='coerce')
    types = frame['IncidentTypeCategory'].astype('string').str.strip().str.upper()
    wildfire = types.eq('WF').fillna(False)
    time_ok = dates.ge(start_time) & dates.lt(end_time)
    geometry_ok = frame.geometry.notna() & ~frame.geometry.is_empty
    geometry_ok &= frame.geometry.geom_type.eq('Point') & frame.geometry.is_valid
    eligible = frame.loc[wildfire & time_ok & geometry_ok].copy()
    left, bottom, right, top = counties.total_bounds
    selected = eligible.cx[left:right, bottom:top].copy()
    if selected.empty:
        raise ValueError('No recorded wildfire ignitions satisfy the selected interval and domain.')
    county_union = counties.geometry.union_all()
    inside = selected.geometry.intersects(county_union)
    selected_dates = dates.loc[selected.index]
    audit = {
        'event_definition': 'recorded wildfire ignition; IncidentTypeCategory=WF',
        'start_utc_inclusive': start_time.isoformat(),
        'end_utc_exclusive': end_time.isoformat(),
        'spatial_domain': 'combined county bounding rectangle; surrounding records retained for smoothing',
        'source_records': len(frame),
        'source_incident_types': {str(k): int(v) for k, v in types.fillna('MISSING').value_counts().items()},
        'excluded_non_wildfire_records': int((~wildfire).sum()),
        'wildfire_records_with_missing_dates': int((wildfire & dates.isna()).sum()),
        'wildfire_records_outside_period': int((wildfire & dates.notna() & ~time_ok).sum()),
        'wildfire_records_in_period_with_invalid_geometry': int((wildfire & time_ok & ~geometry_ok).sum()),
        'eligible_records_outside_rectangle': len(eligible) - len(selected),
        'selected_rectangle_records': len(selected),
        'selected_inside_counties': int(inside.sum()),
        'selected_outside_counties': int((~inside).sum()),
        'first_selected_discovery_utc': selected_dates.min().isoformat(),
        'last_selected_discovery_utc': selected_dates.max().isoformat(),
    }
    excluded = sum(audit[k] for k in [
        'excluded_non_wildfire_records', 'wildfire_records_with_missing_dates',
        'wildfire_records_outside_period', 'wildfire_records_in_period_with_invalid_geometry',
        'eligible_records_outside_rectangle'])
    if excluded + len(selected) != len(frame):
        raise AssertionError('Historical occurrence selection does not reconcile with the source.')
    return selected, audit
