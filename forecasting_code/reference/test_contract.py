"""Synthetic contract tests; no real data access and no model training."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
import pandas as pd
from scipy.special import logit

spec=importlib.util.spec_from_file_location('forecast_experiment',Path(__file__).with_name('experiment.py'))
e=importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)


class ContractTests(unittest.TestCase):
    def test_out_of_scope_target_and_source_rejected(self):
        for year in [2000,2022,2023,2024,2025]:
            with self.assertRaises(ValueError):e.role_labels(pd.DataFrame(),year,'base_train')
        with self.assertRaises(ValueError):e.source_path('unapproved_mixed_year_source')

    def test_roles_exclude_recent_and_future_outcomes(self):
        rows=pd.DataFrame({'year':range(2001,2022),'eligible':True,'status':'N','y':0})
        for role,first,last in [('base_train',2001,2009),('calibration',2010,2011),('baseline_history',2001,2011)]:
            selected=e.role_labels(rows,2013,role)
            self.assertEqual(selected.year.tolist(),list(range(first,last+1)))
            altered=rows.copy();altered.loc[altered.year.ge(2012),'y']=1
            pd.testing.assert_frame_equal(selected,e.role_labels(altered,2013,role))

    def test_unknown_and_flagged_excluded(self):
        rows=pd.DataFrame({'year':[2001]*3,'eligible':[True,False,False],'status':['P','F','U'],'y':[1,0,np.nan]})
        selected=e.role_labels(rows,2013,'base_train')
        self.assertEqual(len(selected),1)
        self.assertEqual(selected.status.iloc[0],'P')

    def test_offset_matches_constant_probability_solution(self):
        a,status=e.calibration_offset(np.full(10,0.2),np.array([1]*4+[0]*6))
        self.assertEqual(status,'ok')
        self.assertAlmostEqual(a,float(logit(0.4)-logit(0.2)),places=10)
        result=e.calibrated(np.array([0.2]),a,status)[0]
        self.assertGreater(result,0.2);self.assertLess(result,0.4)

    def test_calibration_fallback_preserves_raw(self):
        raw=np.array([0.2,0.4]);offset,status=e.calibration_offset(raw,np.array([0,0]))
        np.testing.assert_array_equal(e.calibrated(raw,offset,status),raw)

    def test_baseline_zero_history_fallback(self):
        h=pd.DataFrame({'eligible':[True,True],'county':['A','A'],'cell_id':['a','a'],'y':[0,1]})
        target=pd.DataFrame({'county':['A','B'],'cell_id':['new_a','new_b']})
        probabilities,_=e.baselines(h,h.iloc[:0],target)
        for values in probabilities.values():np.testing.assert_allclose(values,0.5)


if __name__=='__main__':unittest.main()
