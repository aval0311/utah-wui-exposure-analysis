"""Check all-missing temporal windows and observation eligibility without data downloads."""
import ast,json,sys,warnings
from pathlib import Path
import numpy as np
nb=json.loads((Path(__file__).resolve().parents[1]/'notebooks/utah_wui_exposure_analysis.ipynb').read_text(encoding='utf-8'))
source=next(''.join(c['source']) for c in nb['cells'] if c.get('metadata',{}).get('original_cell')==15)
node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='supported_temporal_median')
ns={'np':np}
exec(compile(ast.Module(body=[node],type_ignores=[]),'<temporal median>','exec'),ns)
stack=np.array([[[np.nan,1,1,2]],[[np.nan,np.nan,3,4]],[[np.nan,np.nan,np.nan,6]]],dtype=np.float32)
with warnings.catch_warnings():
    warnings.simplefilter('error',RuntimeWarning)
    result=ns['supported_temporal_median'](stack,2)
np.testing.assert_allclose(result,np.array([[np.nan,np.nan,2,4]],dtype=np.float32),equal_nan=True)
assert result.dtype==np.float32
print('PASS: all-NaN and insufficient-observation cells remain NoData without RuntimeWarning; supported medians are correct.')

