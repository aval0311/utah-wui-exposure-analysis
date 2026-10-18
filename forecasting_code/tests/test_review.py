import importlib.util
from pathlib import Path
import unittest
import numpy as np
import pandas as pd
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('review_reference',Path(__file__).resolve().parents[1]/'reference/experiment.py')
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)

class ReviewTests(unittest.TestCase):
    def test_all_folds_keep_training_and_calibration_separate(self):
        rows=pd.DataFrame({'year':range(2001,2022),'eligible':True,'status':'N','y':0})
        for t in range(2013,2022):
            train=e.role_labels(rows,t,'base_train');cal=e.role_labels(rows,t,'calibration')
            self.assertEqual(train.year.max(),t-4)
            self.assertEqual(set(cal.year),{t-3,t-2})
            self.assertFalse(set(train.year)&set(cal.year))

    def test_future_labels_do_not_change_cell_history_probabilities(self):
        rows=pd.DataFrame({'year':range(2001,2022),'eligible':True,'status':'N','y':0,'cell_id':'a','county':'A'})
        target=pd.DataFrame({'cell_id':['a'],'county':['A']})
        def predict(df):return e.baselines(e.role_labels(df,2017,'baseline_history'),e.role_labels(df,2017,'recent_history'),target)[0]
        original=predict(rows); rows.loc[rows.year.ge(2016),'y']=1
        for method,values in predict(rows).items():np.testing.assert_array_equal(values,original[method])

    def test_confident_wrong_predictions_have_larger_errors(self):
        frame=pd.DataFrame({'cell_id':['a','b'],'y':[0,1],'probability':[0.1,0.9],'study_area_km2':[1,1]})
        good=e.metrics(frame);frame['probability']=[0.9,0.1];bad=e.metrics(frame)
        self.assertAlmostEqual(good['brier'],0.01)
        self.assertAlmostEqual(bad['brier'],0.81)
        self.assertGreater(bad['log_loss'],good['log_loss'])

    def test_top_decile_ties_are_deterministic(self):
        frame=pd.DataFrame({'cell_id':['b','a'],'y':[0,1],'probability':[0.5,0.5],'study_area_km2':[1,1]})
        self.assertEqual(e.metrics(frame)['top_decile_captured'],1)
        self.assertEqual(e.metrics(frame.iloc[::-1])['top_decile_captured'],1)
        self.assertIn('no geographic skill',e.metrics(frame)['ranking_note'])

    def test_completed_run_rejected_before_reading_sources(self):
        with patch.object(e,'OUT',Path(__file__).parent),patch.object(e,'check_sources',side_effect=AssertionError('Must not read sources')):
            with self.assertRaisesRegex(ValueError,'Run directory exists'):e.prepare()

    def test_single_class_metrics_remain_undefined(self):
        frame=pd.DataFrame({'cell_id':['a','b'],'y':[0,0],'probability':[0.1,0.2],'study_area_km2':[1,1]})
        result=e.metrics(frame)
        self.assertTrue(np.isnan(result['roc_auc']))
        self.assertTrue(np.isnan(result['average_precision']))
        self.assertIn('single class',result['metric_note'])
