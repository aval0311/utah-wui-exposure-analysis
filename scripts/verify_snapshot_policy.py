"""Regression checks for snapshot integrity and network policy."""
import json, os, socket, sys, tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from wui.runtime import initialize_run, recipe_hash, sha256, REQUIRED_TABULAR_VECTOR_SOURCES

with tempfile.TemporaryDirectory(prefix='wui-policy-') as temporary:
    base=Path(temporary)
    assert base.resolve().parent == Path(tempfile.gettempdir()).resolve()
    repo=base/'repo'
    (repo/'notebooks').mkdir(parents=True)
    notebook=repo/'notebooks/utah_wui_exposure_analysis.ipynb'
    notebook.write_text(json.dumps({'cells':[{'cell_type':'code','metadata':{'original_cell':15},'source':'parameter=1'}]}))
    workspace=base/'workspace'
    (workspace/'data/processed').mkdir(parents=True)
    source=workspace/'data/processed/utah_three_county_2020_census_block_groups.gpkg'
    source.write_bytes(b'standin-source')
    derivative=workspace/'data/processed/derived.tif'
    derivative.write_bytes(b'standin-derivative')
    extra=[]
    for name in REQUIRED_TABULAR_VECTOR_SOURCES:
        path=workspace/name
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(b'immutable analytical source')
        extra.append((path,'source'))
    manifest={'recipe_sha256':recipe_hash(repo),'cache_inputs':[
        {'path':str(p.relative_to(workspace)),'sha256':sha256(p),'role':role}
        for p,role in [(source,'source'),(derivative,'derived'),*extra]]}
    (workspace/'snapshot_manifest.json').write_text(json.dumps(manifest))
    first=initialize_run(repo,str(workspace),'snapshot',False)[1]
    second=initialize_run(repo,str(workspace),'snapshot',False)[1]
    assert first!=second and first.is_dir() and second.is_dir()
    def rejects(fn,kind):
        try:fn()
        except kind:return
        raise AssertionError('Expected rejection did not occur')
    for path,_ in extra:
        path.write_bytes(b'changed numerical or vector source')
        rejects(lambda:initialize_run(repo,str(workspace),'snapshot',False),ValueError)
        rejects(lambda:initialize_run(repo,str(workspace),'snapshot',True),ValueError)
        path.write_bytes(b'immutable analytical source')
    incomplete=dict(manifest,cache_inputs=manifest['cache_inputs'][:-1])
    (workspace/'snapshot_manifest.json').write_text(json.dumps(incomplete))
    rejects(lambda:initialize_run(repo,str(workspace),'snapshot',True),ValueError)
    (workspace/'snapshot_manifest.json').write_text(json.dumps(manifest))
    source.write_bytes(b'corrupted')
    rejects(lambda:initialize_run(repo,str(workspace),'snapshot',False),ValueError)
    rejects(lambda:initialize_run(repo,str(workspace),'snapshot',True),ValueError)
    source.write_bytes(b'standin-source')
    derivative.write_bytes(b'changed')
    rejects(lambda:initialize_run(repo,str(workspace),'snapshot',False),ValueError)
    initialize_run(repo,str(workspace),'snapshot',True)
    derivative.write_bytes(b'standin-derivative')
    notebook.write_text(notebook.read_text().replace('parameter=1','parameter=2'))
    rejects(lambda:initialize_run(repo,str(workspace),'snapshot',False),ValueError)
    initialize_run(repo,str(workspace),'snapshot',True)
    rejects(lambda:socket.getaddrinfo('example.com',443),RuntimeError)
    (workspace/'snapshot_manifest.json').unlink()
    rejects(lambda:initialize_run(repo,str(workspace),'snapshot',False),FileNotFoundError)
print('PASS: unique run directories, source/derivative integrity, changed-recipe rejection, rebuild policy, missing manifest, and analytical network blocking.')

