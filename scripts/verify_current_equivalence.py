"""Compare the retained serial algorithm with the current full-pipeline Dask output."""
import os,sys,json,gc,time
from pathlib import Path
from contextlib import ExitStack
import argparse
repository=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('workspace',type=Path)
parser.add_argument('--run',type=Path)
args=parser.parse_args()
sys.path.insert(0,str(repository/'src'))
for setting,relative in [('PROJ_DATA','Library/share/proj'),('PROJ_LIB','Library/share/proj'),('GDAL_DATA','Library/share/gdal')]:
    os.environ[setting]=str(Path(sys.prefix)/relative)
if os.name=='nt':
    _handle=os.add_dll_directory(str(Path(sys.prefix)/'Library/bin'))
import numpy as np
import rasterio
from wui.validation import hpc_compare_output,hpc_digest
workspace=args.workspace.resolve()
run=args.run.resolve() if args.run else max((r for r in (workspace/'outputs/publication').iterdir() if (r/'run_manifest.json').is_file()),key=lambda p:p.name)
if not run.is_relative_to(workspace):raise ValueError('Run must be inside the chosen workspace.')
run_manifest=json.loads((run/'run_manifest.json').read_text())
if not run_manifest.get('analytical_qa_passed'):raise ValueError('Run has not passed analytical QA.')
result=json.loads((run/'hpc_result.json').read_text())
source=json.loads((repository/'evidence/reference/serial_reference.json').read_text(encoding='utf-8'))
reference=run/'serial_equivalence'
reference.mkdir(exist_ok=False)
def cell(i):return source['cells'][str(i)]
actual={k:workspace/v for k,v in result['outputs'].items()}
paths={k:reference/v.name for k,v in actual.items()}
spec=source
inputs={k:workspace/v for k,v in source['supporting_inputs'].items()}
with rasterio.open(run/'study_area_mask.tif') as src:
    study=src.read(1).astype(bool)
    transform=src.transform
with rasterio.open(actual['normalized_hazard']) as src:
    profile=src.profile.copy()
    profile['predictor']=int(src.tags(ns='IMAGE_STRUCTURE').get('PREDICTOR','1'))
    tags=src.tags()
namespace=dict(Path=Path,np=np,rasterio=rasterio,gc=gc,time=time,ExitStack=ExitStack,
    HPC_ENGINE='rasterio',HPC_SETUP_STAGES={},
    fire_hazard_alignment_study_area_mask=study,
    fire_hazard_alignment_width=study.shape[1],fire_hazard_alignment_height=study.shape[0],
    fire_hazard_alignment_transform=transform,fire_hazard_target_crs='EPSG:26912',
    fire_hazard_nodata_value=-9999.0,fire_hazard_component_profile=profile,
    fire_hazard_model_name=tags['MODEL_NAME'],fire_hazard_model_version=tags['MODEL_VERSION'],
    final_weight_sum=1.0,
    fire_hazard_final_component_paths={k:workspace/v['path'] for k,v in result['current_inputs'].items()},
    fire_hazard_final_component_weights=run_manifest['weights'],
    fire_hazard_final_normalized_path=paths['normalized_hazard'],
    fire_hazard_final_index_path=paths['continuous_index_1_10'],
    fire_hazard_final_class_path=paths['hazard_class'],final_coverage_path=paths['coverage_reason'],
    final_fbfm40_path=inputs['aligned_fbfm40'],
    fire_hazard_hls_ndvi_observation_count_path=inputs['ndvi_observation_count'],
    fire_hazard_hls_ndmi_observation_count_path=inputs['ndmi_observation_count'],
    fire_hazard_hls_composite_minimum_observations=3,
    final_burnable_codes=tuple(spec['analytical_rules']['burnable_codes']),
    CONFIRMED_NONBURNABLE_CODES=tuple(spec['analytical_rules']['confirmed_nonburnable_codes']),
    final_coverage_counts=np.zeros(6,dtype=np.int64))
with rasterio.open(actual['coverage_reason']) as src:
    namespace['COVERAGE_LABELS']={int(k.split('_')[1]):v for k,v in src.tags().items() if k.startswith('CODE_')}
exec(compile(cell(313),'<retained serial helpers>','exec'),namespace)
started=time.perf_counter()
exec(compile(cell(322),'<retained serial composite>','exec'),namespace)
exec(compile(cell(324),'<retained serial derived products>','exec'),namespace)
comparisons={k:hpc_compare_output(actual[k],paths[k],0.0) for k in actual}
passed=all(v['passed'] and v['bitwise_differing_valid_pixels']==0 for v in comparisons.values())
from wui.runtime import portable
record=portable({'status':'passed' if passed else 'failed',
    'scope':'Current full-pipeline inputs, serial versus Dask; not a matched benchmark',
    'run_id':run.name,'serial_seconds':time.perf_counter()-started,'comparisons':comparisons},workspace)
(repository/'evidence/current_serial_dask_equivalence.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print({k:dict(passed=v['passed'],mask_mismatches=v['mask_mismatches'],different_pixels=v['bitwise_differing_valid_pixels']) for k,v in comparisons.items()},flush=True)
if not passed:raise AssertionError('Current serial/Dask outputs differ.')

