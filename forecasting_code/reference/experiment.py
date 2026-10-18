"""Fixed retrospective experiment. Read only audited development exports; write locally.

Commands: prepare, train, evaluate, verify. No project analytical imports or network I/O.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import warnings
import os
import sys

# Match Conda activation's DLL search order in this process only. No environment edits.
_prefix = Path(sys.prefix)
_bins = [_prefix, _prefix/'Library/mingw-w64/bin', _prefix/'Library/usr/bin',
         _prefix/'Library/bin', _prefix/'Scripts']
os.environ['PATH'] = os.pathsep.join(str(p) for p in _bins if p.exists()) + os.pathsep + os.environ.get('PATH','')

import numpy as np
import pandas as pd
import scipy
from scipy.optimize import brentq
from scipy.special import expit, logit
import sklearn
from sklearn.exceptions import ConvergenceWarning
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import average_precision_score, roc_auc_score

HERE = Path(__file__).resolve().parent
PLAN = HERE.parent
ROOT = PLAN.parent
OUT = HERE / 'run_002'
EPS = 1e-6
BASE = ['elevation_mean_m','slope_mean_deg','northness_mean','eastness_mean','log_study_area_km2']
CLIMATE = ['clim_pr_sum_antecedent_12mo_mm','clim_pr_sum_antecedent_jul_sep_mm',
           'clim_tmean_antecedent_12mo_c','clim_tmean_antecedent_jul_sep_c',
           'clim_vpd_mean_antecedent_12mo_kpa','clim_vpd_mean_antecedent_jul_sep_kpa']
FEATURES = {'M0': BASE, 'M1': BASE + CLIMATE}
BASELINES = ['pooled_history','recent_history','county_history','cell_history']
METHODS = BASELINES + ['M0_raw','M0_calibrated','M1_raw','M1_calibrated']
INPUTS = {
    'history':'historical_timeline_v1/dist/data/timeline.json',
    'terrain':'ml_outputs/terrain_064dcafd4cc0/terrain_features_by_cell.parquet',
    'climate':'ml_outputs/climate_features_ba80797440f5/climate_features_by_cell_year.parquet',
    'availability':'ml_outputs/climate_features_ba80797440f5/feature_year_availability.csv',
    'specification':'fire_occurrence_forecasting_v1/forecast_specification.md',
    'schedule':'fire_occurrence_forecasting_v1/experiment_schedule.csv',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def save_json(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False)+'\n', encoding='utf-8')


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def source_path(name):
    require(name in INPUTS, 'Source is not allowlisted')
    return ROOT / INPUTS[name]


def check_sources():
    review = read_json(PLAN/'data_contract_review/review_results.json')
    for rel in INPUTS.values():
        require(sha(ROOT/rel) == review['input_reads'][rel]['sha256_after'], 'Audited source changed: '+rel)
    return {rel:sha(ROOT/rel) for rel in INPUTS.values()}


def snapshots():
    config = read_json(OUT/'frozen_config.json')
    require(sha(HERE/'experiment.py') == config['code_sha256'], 'Experiment code changed after freeze')
    manifest = read_json(OUT/'input_manifest.json')
    for name, digest in manifest['snapshot_sha256'].items():
        require(sha(OUT/name) == digest, 'Snapshot changed: '+name)
    check_sources()
    return config, manifest


def prepare():
    require(not OUT.exists(), 'Run directory exists; preserve completed/partial run')
    source_hashes = check_sources()
    history = read_json(source_path('history'))
    require(history['years'] == list(range(2001,2022)), 'History scope')
    rows = []
    for cell in history['cells']:
        require(len(cell['status']) == 21 and set(cell['status']) <= set('PNFU'), 'Status sequence')
        for year, status in zip(history['years'],cell['status']):
            rows.append(dict(cell_id=cell['id'],year=year,county=cell['county'].upper(),status=status,
                             eligible=status in ['P','N'], y=1.0 if status=='P' else np.nan if status=='U' else 0.0))
    labels = pd.DataFrame(rows).sort_values(['year','cell_id']).reset_index(drop=True)
    terrain = pd.read_parquet(source_path('terrain'),columns=['cell_id','study_area_km2']+BASE[:-1])
    require(terrain.study_area_km2.gt(0).all(), 'Area must be positive')
    terrain['log_study_area_km2'] = np.log(terrain.study_area_km2)
    climate = pd.read_parquet(source_path('climate'),columns=['cell_id','year']+CLIMATE)
    require(climate.year.between(2001,2021).all(), 'Climate scope')
    x = labels[['cell_id','year','county']].merge(terrain,on='cell_id',validate='many_to_one').merge(climate,on=['cell_id','year'],validate='one_to_one')
    require(len(x)==20937 and x.cell_id.nunique()==997 and x.groupby('year').size().eq(997).all(), 'Feature population')
    require(not labels.duplicated(['cell_id','year']).any() and int(labels.eligible.sum())==20551, 'Labels population')
    require(not np.isinf(x[FEATURES['M1']].to_numpy()).any(), 'Infinite feature')
    avail = pd.read_csv(source_path('availability'))
    require(len(avail)==126 and avail.year.between(2001,2021).all(), 'Availability scope')
    avail['forecast_cutoff_utc'] = [f'{y-1}-12-01T00:00:00+00:00' for y in avail.year]
    require((pd.to_datetime(avail.assumed_available_utc,utc=True)<pd.to_datetime(avail.forecast_cutoff_utc,utc=True)).all(), 'Climate cutoff')
    schedule = pd.read_csv(source_path('schedule'))
    require(schedule.target_year.tolist()==list(range(2013,2022)), 'Forecast scope')
    OUT.mkdir()
    (OUT/'models').mkdir()
    labels.to_parquet(OUT/'labels_2001_2021.parquet',index=False)
    x.to_parquet(OUT/'features_2001_2021.parquet',index=False)
    avail.to_csv(OUT/'climate_lineage.csv',index=False)
    schedule.to_csv(OUT/'schedule.csv',index=False)
    save_json(OUT/'frozen_config.json', dict(
        experiment='retrospective_occurrence_v1',created_utc=now(),code_sha256=sha(HERE/'experiment.py'),
        authorization='User authorized retrospective training/evaluation on 2001-2021 with agreed assumptions and fixed specification; no publishing.',
        availability_track='retrospective_reconstruction',historical_as_issued_verified=False,
        target_years=list(range(2013,2022)),source_target_years=[2001,2021],forbidden_years=[2022,2023,2024,2025],
        features=FEATURES,methods=METHODS,primary_candidate='M1_calibrated',
        logistic=dict(C=1.0,l1_ratio=0.0,solver='lbfgs',fit_intercept=True,tol=1e-8,max_iter=2000,random_state=2026,class_weight=None),
        imputer='training-only median; no indicators',scaler='training-only mean and population standard deviation',
        calibration=dict(slope=1.0,shrinkage=0.5,clip=EPS,root_bracket=[-40,40],failure='raw'),
        baseline_shrinkage=20,year_roles='base 2001:T-4; calibration T-3:T-2; baselines 2001:T-2; forecast T',
        fixed_before_training=True,hyperparameter_search=False,
        runtime='Conda DLL directories prepended to process PATH; system and retained environment unchanged',
        versions=dict(python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,scipy=scipy.__version__,sklearn=sklearn.__version__)))
    snapshot_names=['labels_2001_2021.parquet','features_2001_2021.parquet','climate_lineage.csv','schedule.csv','frozen_config.json']
    save_json(OUT/'input_manifest.json',dict(source_sha256=source_hashes,snapshot_sha256={n:sha(OUT/n) for n in snapshot_names},scope='Only audited development-only exports; non-temporal terrain; no original mixed-year source reads'))
    print('Prepared scoped snapshots and froze configuration. No fits performed.',flush=True)


def role_labels(labels, target, role):
    require(2013<=target<=2021, 'Target outside allowed forecast years')
    intervals={'base_train':(2001,target-4),'calibration':(target-3,target-2),'baseline_history':(2001,target-2),'recent_history':(target-3,target-2)}
    require(role in intervals, 'Unknown fitting role')
    first,last=intervals[role]
    result=labels.loc[labels.year.between(first,last)&labels.eligible].copy()
    require(len(result)>0 and result.year.max()<=target-2 and result.status.isin(['P','N']).all(), 'Invalid fitting labels')
    return result


def calibration_offset(p,y):
    if len(np.unique(y))<2:
        return 0.0,'raw_fallback_one_class'
    z=logit(np.clip(p,EPS,1-EPS))
    try:
        a=brentq(lambda offset: float(np.sum(expit(z+offset)-y)), -40,40,xtol=1e-12)
        return float(a),'ok'
    except (ValueError,RuntimeError):
        return 0.0,'raw_fallback_optimization'


def calibrated(p,offset,status):
    return p.copy() if status!='ok' else expit(logit(np.clip(p,EPS,1-EPS))+0.5*offset)


def baselines(history,recent,target_x):
    require(history.eligible.all() and recent.eligible.all(), 'Baseline eligibility')
    pooled=float((history.y.sum()+0.5)/(len(history)+1))
    recent_p=float((recent.y.sum()+0.5)/(len(recent)+1)) if len(recent) else pooled
    county=history.groupby('county').y.agg(['sum','count'])
    county['probability']=(county['sum']+20*pooled)/(county['count']+20)
    cp=target_x.county.map(county.probability).fillna(pooled).to_numpy()
    cell=history.groupby('cell_id').y.agg(['sum','count'])
    sums=target_x.cell_id.map(cell['sum']).fillna(0).to_numpy()
    counts=target_x.cell_id.map(cell['count']).fillna(0).to_numpy()
    probabilities={'pooled_history':np.full(len(target_x),pooled),'recent_history':np.full(len(target_x),recent_p),
                   'county_history':cp,'cell_history':(sums+20*cp)/(counts+20)}
    return probabilities,dict(pooled=pooled,recent=recent_p,county=county.reset_index().to_dict('records'),cell=cell.reset_index().to_dict('records'))


def train():
    config,manifest=snapshots()
    require(not (OUT/'predictions.csv').exists() and not any((OUT/'models').iterdir()), 'Preserve existing fits; do not overwrite')
    x=pd.read_parquet(OUT/'features_2001_2021.parquet')
    labels=pd.read_parquet(OUT/'labels_2001_2021.parquet')
    predictions,memberships,fit_audit,missing=[],[],[],[]
    manifest_hash=sha(OUT/'input_manifest.json')
    for t in config['target_years']:
        target=x.loc[x.year.eq(t)].sort_values('cell_id').reset_index(drop=True)
        require(len(target)==997 and 'y' not in target and 'status' not in target,'Target features must not carry labels')
        role={name:role_labels(labels,t,name) for name in ['base_train','calibration','baseline_history','recent_history']}
        for name,data in role.items():
            member=data[['cell_id','year','county','status']].copy()
            member.insert(0,'target_year',t);member['role']=name
            memberships.append(member)
        require(role['base_train'].year.max()<role['calibration'].year.min(), 'Overlapping fitting periods')
        forecasts,counts=baselines(role['baseline_history'],role['recent_history'],target)
        save_json(OUT/'models'/f'{t}_baselines.json',counts)
        for model_name,columns in FEATURES.items():
            train_rows=role['base_train'].merge(x.drop(columns='county'),on=['cell_id','year'],validate='one_to_one').sort_values(['year','cell_id'])
            cal_rows=role['calibration'].merge(x.drop(columns='county'),on=['cell_id','year'],validate='one_to_one').sort_values(['year','cell_id'])
            require(train_rows[columns].notna().any().all(),'All-missing training predictor')
            pipeline=Pipeline([('imputer',SimpleImputer(strategy='median')),('scaler',StandardScaler()),('model',LogisticRegression(**config['logistic']))])
            with warnings.catch_warnings():
                warnings.simplefilter('error',ConvergenceWarning)
                pipeline.fit(train_rows[columns],train_rows.y.astype(int))
            cal_p=pipeline.predict_proba(cal_rows[columns])[:,1]
            p=pipeline.predict_proba(target[columns])[:,1]
            offset,status=calibration_offset(cal_p,cal_rows.y.to_numpy())
            forecasts[model_name+'_raw']=p
            forecasts[model_name+'_calibrated']=calibrated(p,offset,status)
            artifact=dict(target_year=t,model=model_name,features=columns,training_first=2001,training_last=t-4,
                          calibration_years=[t-3,t-2],training_rows=len(train_rows),calibration_rows=len(cal_rows),
                          imputation_medians=pipeline['imputer'].statistics_.tolist(),scaler_mean=pipeline['scaler'].mean_.tolist(),
                          scaler_scale=pipeline['scaler'].scale_.tolist(),coefficients=pipeline['model'].coef_[0].tolist(),
                          intercept=float(pipeline['model'].intercept_[0]),classes=pipeline['model'].classes_.tolist(),
                          n_iter=int(pipeline['model'].n_iter_[0]),calibration_offset=offset,calibration_status=status,
                          input_manifest_sha256=manifest_hash,fit_completed_utc=now())
            save_json(OUT/'models'/f'{t}_{model_name}.json',artifact)
            fit_audit.append({k:v for k,v in artifact.items() if k not in ['imputation_medians','scaler_mean','scaler_scale','coefficients','features','classes']})
            for name,data in [('base_train',train_rows),('calibration',cal_rows),('forecast',target)]:
                for col in columns:
                    missing.append(dict(target_year=t,model=model_name,role=name,feature=col,rows=len(data),missing=int(data[col].isna().sum())))
        for method,p in forecasts.items():
            require(np.isfinite(p).all() and ((p>=0)&(p<=1)).all(),'Invalid probability')
            frame=target[['cell_id','county','study_area_km2']].copy()
            frame['target_year']=t;frame['probability']=p;frame['method_id']=method
            frame['issue_utc']=f'{t-1}-12-15T17:00:00+00:00';frame['data_cutoff_utc']=f'{t-1}-12-01T00:00:00+00:00'
            frame['target_start_utc']=f'{t}-01-01T00:00:00+00:00';frame['target_end_utc']=f'{t+1}-01-01T00:00:00+00:00'
            frame['availability_track']='retrospective_reconstruction';frame['model_version']='retrospective_occurrence_v1'
            frame['input_manifest_hash']=manifest_hash
            frame['latest_training_label_year']=t-2 if method in BASELINES else t-4
            frame['latest_label_year_used']=t-2
            frame['calibration_years']='' if method in BASELINES else f'{t-3}|{t-2}'
            cols=FEATURES['M0' if method.startswith('M0') else 'M1'] if method not in BASELINES else []
            frame['prediction_status']=np.where(target[cols].isna().any(axis=1),'ok_with_training_median_imputation','ok') if cols else 'ok'
            frame['warnings']='Reconstructed inputs; historical vintages unverified; development evidence'
            predictions.append(frame)
        print(f'Saved {t} model artifacts; generated 8 methods for 997 cells.',flush=True)
    result=pd.concat(predictions,ignore_index=True)
    require(len(result)==9*997*8 and not result.duplicated(['cell_id','target_year','method_id']).any(),'Prediction coverage')
    require(not set(['y','status','eligible'])&set(result.columns),'Outcome leaked into prediction output')
    result.to_csv(OUT/'predictions.csv',index=False,float_format='%.17g')
    pd.concat(memberships,ignore_index=True).to_csv(OUT/'fit_membership.csv',index=False)
    pd.DataFrame(fit_audit).to_csv(OUT/'fit_audit.csv',index=False)
    pd.DataFrame(missing).to_csv(OUT/'fit_feature_missingness.csv',index=False)
    check_sources()
    save_json(OUT/'prediction_manifest.json',dict(saved_utc=now(),predictions_sha256=sha(OUT/'predictions.csv'),rows=len(result),
        model_fits=18,imputer_fits=18,scaler_fits=18,calibration_attempts=18,calibration_successes=sum(a['calibration_status']=='ok' for a in fit_audit),
        evaluation_started=False,source_sha256=manifest['source_sha256'],artifacts_sha256={str(p.relative_to(OUT)):sha(p) for p in sorted((OUT/'models').glob('*.json'))}))
    print('Predictions persisted and sealed before evaluation.',flush=True)


def metrics(group):
    y=group.y.to_numpy();p=group.probability.to_numpy();q=np.clip(p,EPS,1-EPS)
    both=len(np.unique(y))==2
    budget=math.ceil(0.10*len(group))
    ranked=group.sort_values(['probability','cell_id'],ascending=[False,True],kind='stable').head(budget)
    captured=int(ranked.y.sum());positives=int(y.sum())
    return dict(n=len(y),positives=positives,brier=float(np.mean((p-y)**2)),
                log_loss=float(-np.mean(y*np.log(q)+(1-y)*np.log1p(-q))),
                mean_probability=float(np.mean(p)),observed_rate=float(np.mean(y)),bias=float(np.mean(p-y)),
                expected_positive_cells=float(p.sum()),observed_expected_ratio=float(y.sum()/p.sum()) if p.sum()>0 else np.nan,
                average_precision=float(average_precision_score(y,p)) if both else np.nan,
                roc_auc=float(roc_auc_score(y,p)) if both else np.nan,
                metric_note='' if both else 'AP/AUC undefined: single class',
                top_decile_budget=budget,top_decile_captured=captured,top_decile_recall=captured/positives if positives else np.nan,
                ranking_note='Constant probabilities; tie order has no geographic skill' if np.ptp(p)==0 else 'Cell budget; ties by cell_id',
                area_weighted_brier=float(np.average((p-y)**2,weights=group.study_area_km2)))


def grouped_metrics(frame,keys):
    rows=[]
    for values,g in frame.groupby(keys,sort=True):
        if not isinstance(values,tuple):values=(values,)
        rows.append(dict(zip(keys,values))|metrics(g))
    return pd.DataFrame(rows)


def evaluate():
    snapshots()
    require(not (OUT/'evaluation_manifest.json').exists(),'Do not overwrite completed evaluation')
    pm=read_json(OUT/'prediction_manifest.json')
    require(sha(OUT/'predictions.csv')==pm['predictions_sha256'],'Predictions changed before evaluation')
    predictions=pd.read_csv(OUT/'predictions.csv',float_precision='round_trip')
    labels=pd.read_parquet(OUT/'labels_2001_2021.parquet').rename(columns={'year':'target_year'})
    # Outcome join occurs only after the prediction file and its manifest exist.
    joined=predictions.merge(labels[['cell_id','target_year','status','eligible','y']],on=['cell_id','target_year'],validate='many_to_one')
    scored=joined.loc[joined.eligible].copy()
    require(scored.groupby('method_id').size().eq(8588).all() and scored.groupby('method_id').y.sum().eq(656).all(),'Evaluation cohort mismatch')
    scored.to_csv(OUT/'scored_predictions.csv',index=False,float_format='%.17g')
    annual=grouped_metrics(scored,['method_id','target_year'])
    annual.to_csv(OUT/'annual_metrics.csv',index=False)
    grouped_metrics(scored,['method_id','target_year','county']).to_csv(OUT/'county_year_metrics.csv',index=False)
    # Pooled ranking across different years is not an annual allocation. Suppress it.
    pooled=grouped_metrics(scored,['method_id'])
    pooled=pooled.drop(columns=['top_decile_budget','top_decile_captured','top_decile_recall','ranking_note'])
    pooled.to_csv(OUT/'pooled_metrics.csv',index=False)
    mean=annual.groupby('method_id')[['brier','log_loss','bias','average_precision','roc_auc','top_decile_recall']].mean().add_prefix('mean_annual_').reset_index()
    mean=mean.sort_values('mean_annual_brier')
    mean.to_csv(OUT/'method_comparison.csv',index=False)
    stress=annual.assign(period=np.where(annual.target_year.ge(2020),'2020-2021','2013-2019')).groupby(['method_id','period'])[['brier','log_loss','bias']].mean().reset_index()
    stress.to_csv(OUT/'reporting_stress_metrics.csv',index=False)
    pairs=[]
    for baseline in BASELINES:
        ref=annual[annual.method_id.eq(baseline)].set_index('target_year')
        for method in METHODS:
            a=annual[annual.method_id.eq(method)].set_index('target_year')
            for year in a.index:
                pairs.append(dict(method_id=method,baseline=baseline,target_year=year,brier_difference=a.loc[year,'brier']-ref.loc[year,'brier'],log_loss_difference=a.loc[year,'log_loss']-ref.loc[year,'log_loss']))
    paired=pd.DataFrame(pairs);paired.to_csv(OUT/'paired_annual_differences.csv',index=False)
    paired.groupby(['method_id','baseline']).brier_difference.agg(['mean','min','max',lambda s:int(s.lt(0).sum())]).rename(columns={'<lambda_0>':'years_better'}).reset_index().to_csv(OUT/'paired_difference_summary.csv',index=False)
    calibration=[]
    for (method,period),g in scored.assign(period=np.where(scored.target_year.ge(2020),'2020-2021','2013-2019')).groupby(['method_id','period']):
        bins=np.minimum((g.probability.to_numpy()*10).astype(int),9)
        for b in range(10):
            v=g.loc[bins==b]
            calibration.append(dict(method_id=method,period=period,bin_lower=b/10,bin_upper=(b+1)/10,n=len(v),mean_probability=v.probability.mean(),observed_rate=v.y.mean()))
    pd.DataFrame(calibration).to_csv(OUT/'calibration_bins.csv',index=False)
    best=mean.loc[mean.method_id.isin(BASELINES)].iloc[0]
    primary=mean.set_index('method_id').loc['M1_calibrated']
    gate=bool(primary.mean_annual_brier<best.mean_annual_brier and primary.mean_annual_log_loss<=best.mean_annual_log_loss)
    save_json(OUT/'evaluation_manifest.json',dict(completed_utc=now(),prediction_manifest_sha256=sha(OUT/'prediction_manifest.json'),
        evaluation_rows_per_method=8588,positives_per_method=656,best_baseline_by_mean_annual_brier=best.method_id,
        primary_candidate='M1_calibrated',primary_passes_numerical_recommendation_gate=gate,
        recommendation_status='Requires year/county substantive review' if gate else 'Primary model fails fixed numerical gate; retain strongest baseline as development reference',
        claim='Retrospective development evidence only; not independent or operational forecast validation',
        protected_period_rows_loaded=0,published_files_modified=0))
    check_sources()
    print(mean.to_string(index=False),flush=True)
    print('Numerical recommendation gate:',gate,'; strongest baseline:',best.method_id,flush=True)


def verify():
    config,_=snapshots()
    pm=read_json(OUT/'prediction_manifest.json')
    require(sha(OUT/'predictions.csv')==pm['predictions_sha256'],'Prediction hash')
    for path,digest in pm['artifacts_sha256'].items():require(sha(OUT/path)==digest,'Model artifact changed')
    x=pd.read_parquet(OUT/'features_2001_2021.parquet')
    y=pd.read_parquet(OUT/'labels_2001_2021.parquet')
    pred=pd.read_csv(OUT/'predictions.csv',float_precision='round_trip')
    membership=pd.read_csv(OUT/'fit_membership.csv')
    verified=[]
    for t in config['target_years']:
        for role in ['base_train','calibration','baseline_history','recent_history']:
            expected=role_labels(y,t,role)
            actual=membership.loc[membership.target_year.eq(t)&membership.role.eq(role)]
            require(set(map(tuple,expected[['cell_id','year']].to_numpy()))==set(map(tuple,actual[['cell_id','year']].to_numpy())) and len(actual)==len(expected),'Membership mismatch')
        target=x.loc[x.year.eq(t)].sort_values('cell_id')
        for model,cols in FEATURES.items():
            artifact=read_json(OUT/'models'/f'{t}_{model}.json')
            training=role_labels(y,t,'base_train').merge(x,on=['cell_id','year'],validate='one_to_one')
            values=training[cols].to_numpy()
            med=np.nanmedian(values,axis=0)
            filled=np.where(np.isnan(values),med,values)
            mean=filled.mean(axis=0);scale=filled.std(axis=0);scale[scale==0]=1
            require(np.allclose(med,artifact['imputation_medians']) and np.allclose(mean,artifact['scaler_mean']) and np.allclose(scale,artifact['scaler_scale']),'Preprocessing is not training-only')
            def reconstruct(frame):
                v=frame[cols].to_numpy();v=np.where(np.isnan(v),med,v)
                return expit(((v-mean)/scale)@np.array(artifact['coefficients'])+artifact['intercept'])
            raw=reconstruct(target)
            for suffix,prob in [('raw',raw),('calibrated',calibrated(raw,artifact['calibration_offset'],artifact['calibration_status']))]:
                saved=pred.loc[pred.target_year.eq(t)&pred.method_id.eq(model+'_'+suffix)].sort_values('cell_id')
                require(np.allclose(prob,saved.probability,atol=1e-11,rtol=1e-10),'Model replay discrepancy')
            cal=role_labels(y,t,'calibration').merge(x,on=['cell_id','year'],validate='one_to_one')
            if artifact['calibration_status']=='ok':
                residual=np.sum(expit(logit(np.clip(reconstruct(cal),EPS,1-EPS))+artifact['calibration_offset'])-cal.y)
                require(abs(residual)<1e-6,'Calibration optimum discrepancy')
            verified.append(dict(target_year=t,model=model,training_only_preprocessing=True,artifact_replay=True,calibration_root=True))
        h=role_labels(y,t,'baseline_history');r=role_labels(y,t,'recent_history')
        pooled=(h.y.sum()+0.5)/(len(h)+1)
        recent=(r.y.sum()+0.5)/(len(r)+1)
        manual={method:[] for method in BASELINES}
        for row in target.itertuples():
            county=h[h.county.eq(row.county)];cell=h[h.cell_id.eq(row.cell_id)]
            cp=(county.y.sum()+20*pooled)/(len(county)+20)
            for method,value in zip(BASELINES,[pooled,recent,cp,(cell.y.sum()+20*cp)/(len(cell)+20)]):manual[method].append(value)
        for method,values in manual.items():
            saved=pred.loc[pred.target_year.eq(t)&pred.method_id.eq(method)].sort_values('cell_id')
            require(np.allclose(values,saved.probability,atol=1e-12),'Baseline replay discrepancy')
    scored=pd.read_csv(OUT/'scored_predictions.csv',float_precision='round_trip')
    annual=pd.read_csv(OUT/'annual_metrics.csv')
    for row in annual.itertuples():
        group=scored[scored.target_year.eq(row.target_year)&scored.method_id.eq(row.method_id)]
        require(abs(float(np.square(group.probability-group.y).mean())-row.brier)<1e-12,'Brier recomputation')
    require(len(pred)==71784 and len(scored)==68704,'Output row counts')
    check_sources()
    pd.DataFrame(verified).to_csv(OUT/'model_replay_checks.csv',index=False)
    save_json(OUT/'verification.json',dict(passed=True,models_replayed=18,baseline_years_replayed=36,annual_brier_scores_recomputed=72,
        training_only_preprocessing_verified=True,fit_membership_verified=True,source_hashes_unchanged=True,
        later_period_rows_loaded=0,new_fits_during_verification=0,completed_utc=now()))
    print('Verified 18 model artifacts, 36 baseline/year forecasts and 72 annual Brier scores without refitting.',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['prepare','train','evaluate','verify'])
    globals()[parser.parse_args().command]()
