"""Portable paths, snapshot integrity, and release metadata."""
import ast
import hashlib
import ipaddress
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

CLASS_LABELS = ('Very Low', 'Low', 'Moderate', 'High', 'Very High')
CLASS_BREAKS = (0.2, 0.4, 0.6, 0.8)
_CONTRACTS = {}
_STATE = {}
REQUIRED_TABULAR_VECTOR_SOURCES = (
    'data/processed/utah_three_county_acs5_2024_block_groups_processed.csv',
    'data/raw/fire_hazard/historical_fire/inform_fodr_utah_fire_occurrences_through_2026.geojson',
)

def require_source_inventory(records):
    indexed = {r['path'].replace('\\', '/'): r for r in records}
    if len(indexed) != len(records):
        raise ValueError('Snapshot inventory contains duplicate paths.')
    for name in REQUIRED_TABULAR_VECTOR_SOURCES:
        if name not in indexed or indexed[name].get('role') != 'source':
            raise ValueError(f'Required analytical source is absent from the checksum inventory: {name}')


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def recipe_hash(repository):
    nb = json.loads((Path(repository)/'notebooks/utah_wui_exposure_analysis.ipynb').read_text(encoding='utf-8'))
    parts = [ast.dump(ast.parse(''.join(c['source'])), include_attributes=False)
             for c in nb['cells'] if c['cell_type']=='code'
             and 15 <= c.get('metadata',{}).get('original_cell',-1) <= 308
             and not 110 <= c['metadata']['original_cell'] <= 122]
    for name in ['history.py', 'diagnostics.py']:
        helper = Path(repository)/'src/wui'/name
        if helper.is_file():
            parts.append(name + '\n' + ast.dump(ast.parse(helper.read_text(encoding='utf-8')), include_attributes=False))
    return hashlib.sha256('\n'.join(parts).encode()).hexdigest()

def portable(value, root):
    if isinstance(value, Path):
        value = str(value)
    if isinstance(value, str):
        for raw in [str(Path(root)), Path(root).as_posix(), sys.prefix, sys.executable]:
            value = value.replace(raw, '<WORKSPACE>' if raw in [str(Path(root)), Path(root).as_posix()] else '<ENVIRONMENT>')
        return value.replace('\\','/')
    if isinstance(value, dict):
        return {str(k): portable(v,root) for k,v in value.items()}
    if isinstance(value, (tuple,list)):
        return [portable(v,root) for v in value]
    return value

def analytical_network_guard():
    """Allow local kernel/Dask connections; reject analytical internet access."""
    def audit(event, args):
        if event not in {'socket.connect','socket.getaddrinfo'}:
            return
        address = args[1] if event=='socket.connect' else args[0]
        host = address[0] if isinstance(address,tuple) else address
        if host in {'localhost',None,''}:
            return
        try:
            if ipaddress.ip_address(host).is_loopback:
                return
        except (ValueError,TypeError):
            pass
        raise RuntimeError('Snapshot validation blocked a non-local network connection.')
    sys.addaudithook(audit)

def initialize_run(repository, override, mode, rebuild):
    if mode not in {'snapshot','refresh'}:
        raise ValueError('DATA_MODE must be snapshot or refresh.')
    selected = override or os.environ.get('WUI_PROJECT_ROOT')
    root = Path(selected).expanduser().resolve() if selected else Path(repository).resolve()
    manifest_path = root/'snapshot_manifest.json'
    recipe = recipe_hash(repository)
    if mode=='snapshot':
        if not (root/'data/processed/utah_three_county_2020_census_block_groups.gpkg').is_file():
            raise FileNotFoundError('Set WUI_PROJECT_ROOT to the workspace containing the snapshot data.')
        if not manifest_path.is_file():
            raise FileNotFoundError('The versioned snapshot_manifest.json is required. Unpack the release data package.')
        manifest = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {}
        if not manifest.get('cache_inputs'):
            raise ValueError('The snapshot must include a nonempty input inventory.')
        if manifest and manifest.get('recipe_sha256')!=recipe and not rebuild:
            raise ValueError('Analytical code/settings changed. Set REBUILD_DERIVED=True to rebuild from retained sources.')
        require_source_inventory(manifest['cache_inputs'])
        for record in manifest.get('cache_inputs',[]):
            path = (root/record['path']).resolve()
            if not path.is_relative_to(root):
                raise ValueError('Snapshot input paths must stay within the selected workspace.')
            if not path.is_file():
                raise FileNotFoundError(f"Snapshot input missing: {record['path']}")
            if (not rebuild or record.get('role')=='source') and sha256(path)!=record['sha256']:
                raise ValueError(f"Cached analytical input changed: {record['path']}")
        analytical_network_guard()
    else:
        root.mkdir(parents=True,exist_ok=True)
        manifest = {}
    # Metadata paths are localized only inside the explicitly selected working copy.
    aliases = manifest.get('path_aliases',[])
    aliases = [*aliases, '<WORKSPACE>']
    for path in (root/'data').rglob('*'):
        if not path.is_file() or path.suffix.lower() not in {'.json','.csv','.txt'}:
            continue
        if 'portfolio_http_v1' in path.parts or path.relative_to(root).as_posix() in REQUIRED_TABULAR_VECTOR_SOURCES:
            continue
        old = path.read_text(encoding='utf-8-sig')
        new = old
        for alias in aliases:
            # JSON literals may escape Windows separators.
            new = new.replace(alias.replace('\\','\\\\'),root.as_posix())
            new = new.replace(alias,root.as_posix())
        if new!=old:
            path.write_text(new,encoding='utf-8')
    _CONTRACTS.clear()
    _STATE.update(root=root,repository=Path(repository),recipe=recipe,manifest=manifest)
    output = root/'outputs'/'publication'/f"{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}_{uuid.uuid4().hex[:8]}"
    output.mkdir(parents=True,exist_ok=False)
    return root,output,{'manifest_sha256':sha256(manifest_path) if manifest_path.exists() else None}

def cache_contract(root,mode,rebuild,stage,namespace):
    # The recipe covers upstream code and its literals before any cells execute.
    # Stage records add resolved settings, excluding changing file paths and runtime counters.
    keys = ('fire_hazard_hls_composite_minimum_observations',
            'fire_hazard_vegetation_dryness_index_weights',
            'fire_hazard_vegetation_dryness_normalization_bounds',
            'fire_hazard_components','fire_hazard_cell_size','fire_hazard_target_crs')
    values = {k:portable(namespace[k],root) for k in keys if k in namespace}
    _CONTRACTS[stage] = values
    expected = _STATE['manifest'].get('stage_settings',{}).get(stage)
    if mode=='snapshot' and expected is not None and values!=expected and not rebuild:
        raise ValueError(f'{stage}: resolved settings differ from the snapshot. Rebuild derivatives.')

def canonical_study_mask(root,mode,reconstructed,transform,crs):
    import numpy as np
    import rasterio
    path = Path(root)/'data/snapshots/publication/study_area_mask.tif'
    if mode=='refresh':
        path.parent.mkdir(parents=True,exist_ok=True)
        with rasterio.open(path,'w',driver='GTiff',width=reconstructed.shape[1],
                           height=reconstructed.shape[0],count=1,dtype='uint8',
                           crs=crs,transform=transform,nodata=None,compress='deflate') as dst:
            dst.write(reconstructed.astype('uint8'),1)
        mask=reconstructed
    else:
        with rasterio.open(path) as src:
            if src.shape!=reconstructed.shape or src.transform!=transform or src.crs!=rasterio.crs.CRS.from_user_input(crs):
                raise ValueError('Canonical study mask does not match the analysis grid.')
            values=src.read(1)
            if not np.isin(values,[0,1]).all():
                raise ValueError('Canonical study mask must contain only 0 and 1.')
            mask=values.astype(bool)
    changed=int(np.count_nonzero(mask!=reconstructed))
    info={'policy':'versioned canonical county footprint','sha256':sha256(path),
          'study_pixels':int(mask.sum()),'reconstructed_pixels':int(reconstructed.sum()),
          'reconstruction_differing_pixels':changed,'differing_area_km2':changed*900/1e6}
    print(f"Canonical mask: {info['study_pixels']:,} cells; reconstruction differs at {changed:,} cells.")
    return mask,info

def snapshot_inputs(root):
    """Hash binary inputs and immutable service records, excluding localized metadata."""
    root=Path(root)
    records=[]
    hls_derived={'aligned_scene_indices','processed_fmask','scaled_reflectance',
                 'scene_vegetation_indices','temporal_composites','vegetation_dryness_component'}
    for path in sorted((root/'data').rglob('*')):
        if not path.is_file():
            continue
        parts=set(path.parts)
        immutable_json=path.suffix=='.json' and bool(parts & {'portfolio_http_v1','stac_items','publication'})
        if path.suffix.lower() not in {'.tif','.tiff','.gpkg','.zip','.img','.shp','.shx','.dbf','.prj','.geojson'} and not immutable_json and path.relative_to(root).as_posix() not in REQUIRED_TABULAR_VECTOR_SOURCES:
            continue
        rel=path.relative_to(root).as_posix()
        derived=bool(parts & hls_derived) or 'fuel_hazard_component' in parts or rel.startswith(('data/interim/','data/processed/fire_hazard/'))
        if 'usgs_3dep_1arcsec_dem_tiles' in parts:
            derived=False
        records.append({'path':rel,'bytes':path.stat().st_size,
                        'role':'derived' if derived else 'source','sha256':sha256(path)})
    return records

def finish_contracts(root,mode,rebuild):
    root=Path(root)
    _STATE['manifest'].update(schema_version=2,recipe_sha256=_STATE['recipe'],
        stage_settings=_CONTRACTS,snapshot_version='wui-publication-v3',
        path_aliases=[root.as_posix()], cache_inputs=snapshot_inputs(root))
    (root/'snapshot_manifest.json').write_text(json.dumps(_STATE['manifest'],indent=2),encoding='utf-8')

def migrate_legacy_facilities(root, layer_url):
    """Reconstruct the exact frozen candidate set from complete saved feature batches.

    Snapshot replay must not depend on floating-point serialization of a recomputed
    county query envelope. The union of saved requested IDs must match the returned
    features exactly; ambiguous or incomplete inventories stop execution.
    """
    import geopandas as gpd
    endpoint=layer_url.rstrip('/')+'/query'
    ids=set()
    features={}
    sources=[]
    for path in sorted((Path(root)/'data/snapshots/portfolio_http_v1').glob('*.json')):
        record=json.loads(path.read_text(encoding='utf-8'))
        if record.get('endpoint')!=endpoint:
            continue
        if hashlib.sha256(record['content'].encode()).hexdigest()!=record['sha256']:
            raise ValueError('Facility response checksum mismatch.')
        payload=json.loads(record['content'])
        if 'objectIds' in payload:
            ids.update(payload['objectIds'] or [])
        elif payload.get('type')=='FeatureCollection':
            for feature in payload['features']:
                properties=feature['properties']
                fid=next((v for k,v in properties.items() if k.lower() in {'objectid','fid'}),feature.get('id'))
                if fid is None:
                    raise ValueError('A frozen facility has no stable source identifier.')
                if fid in features and features[fid]!=feature:
                    raise ValueError('Conflicting facility snapshots require an explicit source-version selection.')
                features[fid]=feature
        sources.append(path.name)
    if not ids or set(features)!=ids:
        raise ValueError('Frozen facility feature batches do not match the complete requested-ID set.')
    print(f'Loaded {len(features):,} frozen candidates; requested-ID sets and response checksums reconcile.')
    frame=gpd.GeoDataFrame.from_features(list(features.values()),crs='EPSG:4326')
    save_facilities(root,layer_url,frame,sorted(ids))
    return frame

def facility_snapshot_path(root, layer_url):
    identity=hashlib.sha256(layer_url.rstrip('/').encode()).hexdigest()[:20]
    return Path(root)/'data/snapshots/publication'/f'facilities_{identity}.json'

def save_facilities(root,layer_url,frame,requested_ids):
    fields=[k for k in frame.columns if k.lower() in {'objectid','fid'}]
    if not fields or set(frame[fields[0]])!=set(requested_ids):
        raise ValueError('Facility results must match the complete requested-ID set.')
    value=json.loads(frame.to_json(drop_id=True))
    record={'endpoint':layer_url,'requested_ids':sorted(requested_ids),
            'acquired_utc':datetime.now(timezone.utc).isoformat(),'geojson':value}
    path=facility_snapshot_path(root,layer_url)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(record,ensure_ascii=False),encoding='utf-8')

def frozen_facilities(root,layer_url):
    import geopandas as gpd
    path=facility_snapshot_path(root,layer_url)
    if not path.is_file():
        raise FileNotFoundError('The versioned facility inventory is missing. Restore the snapshot package.')
    record=json.loads(path.read_text(encoding='utf-8'))
    if record['endpoint'].rstrip('/')!=layer_url.rstrip('/'):
        raise ValueError('Facility inventory source mismatch.')
    frame=gpd.GeoDataFrame.from_features(record['geojson']['features'],crs='EPSG:4326')
    fields=[k for k in frame.columns if k.lower() in {'objectid','fid'}]
    if not fields or set(frame[fields[0]])!=set(record['requested_ids']) or len(frame)!=len(record['requested_ids']):
        raise ValueError('Incomplete or duplicate frozen facility inventory.')
    print(f'Loaded {len(frame):,} verified frozen facility candidates.')
    return frame

def freeze_tnm_catalog(root,items,bbox,dataset,reported_total):
    if len(items)!=reported_total or len({v['sourceId'] for v in items})!=reported_total:
        raise ValueError('The complete TNM catalog pages must reconcile with the reported total.')
    record={'schema_version':1,'dataset':dataset,'bbox':list(map(float,bbox.split(','))),
            'reported_total':reported_total,'items':items,
            'acquired_utc':datetime.now(timezone.utc).isoformat()}
    path=Path(root)/'data/snapshots/publication/tnm_catalog.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(record),encoding='utf-8')

def frozen_tnm_catalog(root,bbox):
    record=json.loads((Path(root)/'data/snapshots/publication/tnm_catalog.json').read_text(encoding='utf-8'))
    # Sub-metre transformation differences must not select a new source inventory.
    # A materially different study extent requires a new catalog snapshot.
    if any(abs(float(a)-float(b))>0.00001 for a,b in zip(bbox.split(','),record['bbox'])):
        raise ValueError('Current grid extent differs from the frozen TNM catalog bounds. Use refresh.')
    items=record['items']
    if len(items)!=record['reported_total'] or len({v['sourceId'] for v in items})!=len(items):
        raise ValueError('Incomplete or duplicate frozen TNM catalog.')
    print(f"Loaded {len(items):,} frozen DEM catalog records; pages reconcile with the reported total.")
    return record


