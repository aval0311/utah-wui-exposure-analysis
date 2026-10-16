"""Export one completed run and synchronize the notebook/README release summary."""
import argparse,csv,json,shutil,sys
from pathlib import Path
import nbformat
repository=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(repository/'src'))
from wui.publication import add_phase_navigation, release_summary
from wui.runtime import portable
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('workspace',type=Path)
parser.add_argument('--run',type=Path,help='Completed run directory; defaults to latest passed run.')
args=parser.parse_args()
workspace=args.workspace.resolve()
passed=[]
for candidate in (workspace/'outputs/publication').iterdir():
    path=candidate/'run_manifest.json'
    if path.is_file() and json.loads(path.read_text(encoding='utf-8')).get('analytical_qa_passed'):
        passed.append(candidate)
if args.run:
    run=args.run.resolve()
elif passed:
    run=max(passed,key=lambda path:path.name)
else:
    raise SystemExit('No completed, passed run is available for publication.')
manifest=json.loads((run/'run_manifest.json').read_text(encoding='utf-8'))
if not manifest.get('analytical_qa_passed'):
    raise SystemExit('Only a passed analytical run can be exported.')
required=['county_exposure.csv','facility_proximity.csv','hazard_coverage.csv',
          'historical_occurrence_selection.json','county_exposure.png','facility_proximity.png',
          'hazard_overview.png','county_coverage_diagnostics.png',
          'dashboard/Utah_WUI_Exposure_Composite_Fire_Hazard_Dashboard.html']
for name in required:
    if not (run/name).is_file():raise SystemExit('Completed run lacks required publication output: '+name)
for folder in ['docs','images','outputs/tables','outputs/dashboard','evidence']:
    (repository/folder).mkdir(parents=True,exist_ok=True)
(repository/'docs/index.html').write_text(
    add_phase_navigation((run/required[-1]).read_text(encoding='utf-8')),
    encoding='utf-8', newline='\n')
for source in run.glob('*.png'):shutil.copy2(source,repository/'images'/source.name)
for source in run.glob('*.csv'):
    (repository/'outputs/tables'/source.name).write_text(portable(source.read_text(encoding='utf-8'),workspace),encoding='utf-8')
for name in ['run_manifest.json','hpc_result.json','sensitivity_weights.json','historical_occurrence_selection.json']:
    if (run/name).is_file():shutil.copy2(run/name,repository/'evidence'/('current_'+name))
summary=release_summary(run)
notebook=repository/'notebooks/utah_wui_exposure_analysis.ipynb'
nb=nbformat.read(notebook,as_version=4)
cell=next(c for c in nb.cells if c.id=='release-summary')
cell.source='<a id="release-results"></a>\n## Results at a glance\n\n'+summary+'\n![County exposure estimates](../images/county_exposure.png)\n'
nb.metadata['portfolio']['accepted_run']=manifest['run_id']
nbformat.write(nb,notebook)
readme=repository/'README.md'
text=readme.read_text(encoding='utf-8')
start,end='<!-- RELEASE_RESULTS_START -->','<!-- RELEASE_RESULTS_END -->'
if text.count(start)!=1 or text.count(end)!=1:raise SystemExit('README requires one release-summary marker pair.')
text=text.split(start)[0]+start+'\n'+summary+'\n'+end+text.split(end)[1]
readme.write_text(text,encoding='utf-8')
redirect='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=../../docs/index.html"><title>Utah WUI dashboard</title></head><body><p><a href="../../docs/index.html">Open the release dashboard</a>.</p></body></html>\n'
(repository/'outputs/dashboard/Utah_WUI_Exposure_Composite_Fire_Hazard_Dashboard.html').write_text(redirect,encoding='utf-8')
with (repository/'outputs/dashboard/Utah_WUI_Exposure_Composite_Fire_Hazard_Dashboard_Summary.csv').open('w',newline='',encoding='utf-8') as stream:
    writer=csv.DictWriter(stream,fieldnames=['RUN_ID','DATA_MODE','ENGINE','DASHBOARD','BYTES'])
    writer.writeheader();writer.writerow(dict(RUN_ID=run.name,DATA_MODE=manifest['data_mode'],ENGINE=manifest['engine'],
        DASHBOARD='docs/index.html',BYTES=(repository/'docs/index.html').stat().st_size))
(repository/'evidence/release_validation.json').write_text(json.dumps({
    'status':'awaiting release verification','accepted_run':manifest['run_id'],
    'analytical_qa_passed':True,'note':'Run current equivalence and browser checks before finalizing release evidence.'},indent=2))
print('Exported and synchronized accepted run:',manifest['run_id'])
