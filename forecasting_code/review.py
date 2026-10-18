"""Safe default: verify package integrity and reproduce summary comparisons."""
from pathlib import Path
import csv, hashlib, json
HERE=Path(__file__).resolve().parent
def verify():
    manifest=json.loads((HERE/'manifest.json').read_text())
    for name,digest in manifest.items():
        if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('Package file changed: '+name)
    with (HERE/'evidence/annual_metrics.csv').open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f))
    assert len(rows)==72 and {int(r['target_year']) for r in rows}==set(range(2013,2022))
    by_method={}
    for r in rows: by_method.setdefault(r['method_id'],[]).append(r)
    means={k:sum(float(r['brier']) for r in v)/9 for k,v in by_method.items()}
    with (HERE/'evidence/method_comparison.csv').open(newline='',encoding='utf-8') as f:
        for r in csv.DictReader(f): assert abs(means[r['method_id']]-float(r['mean_annual_brier']))<1e-12
    baseline={r['target_year']:float(r['brier']) for r in by_method['cell_history']}
    assert all(float(r['brier'])>baseline[r['target_year']] for r in by_method['M1_calibrated'])
    relative=100*(means['M1_calibrated']/means['cell_history']-1)
    print(f'Integrity passed: {len(manifest)} files. Recomputed from annual summary scores:')
    print(f'Cell history Brier {means["cell_history"]:.6f}; M1 calibrated {means["M1_calibrated"]:.6f}; relative error increase {relative:.2f}%.')
    print('Cell history wins all nine years. No observations read and no models fitted.')
if __name__=='__main__':verify()
