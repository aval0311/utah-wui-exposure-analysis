"""Small regression cases for event selection and cache-independent coverage counts."""
from pathlib import Path
import os, sys, tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
if os.name=='nt':
    _dll=os.add_dll_directory(str(Path(sys.prefix)/'Library/bin'))
    os.environ['PROJ_DATA']=str(Path(sys.prefix)/'Library/share/proj')
    os.environ['GDAL_DATA']=str(Path(sys.prefix)/'Library/share/gdal')
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.transform import from_origin
from shapely.geometry import Point, box
from wui.history import select_wildfire_occurrences
from wui.diagnostics import observation_support_count, index_availability_counts

counties=gpd.GeoDataFrame({'NAME':['A','B']},geometry=[box(0,0,2,2),box(8,0,10,2)],crs='EPSG:26912')
def ms(day):return int(pd.Timestamp(day,tz='UTC').timestamp()*1000)
frame=gpd.GeoDataFrame({'OBJECTID':range(1,8),
    'IncidentTypeCategory':['WF','RX','WF','WF','WF','WF','WF'],
    'FireDiscoveryDateTime':[ms('2020-01-01'),ms('2020-01-01'),ms('2020-01-01'),
                             ms('2021-01-01'),None,ms('2020-01-01'),ms('2019-12-31')]},
    geometry=[Point(1,1),Point(1,1),Point(5,1),Point(1,1),Point(1,1),Point(12,1),Point(1,1)],crs=counties.crs)
selected,audit=select_wildfire_occurrences(frame,counties,'2020-01-01','2021-01-01')
assert selected.OBJECTID.tolist()==[1,3]
assert audit['selected_inside_counties']==1 and audit['selected_outside_counties']==1
assert audit['excluded_non_wildfire_records']==1
assert audit['wildfire_records_with_missing_dates']==1
assert audit['wildfire_records_outside_period']==2
assert audit['eligible_records_outside_rectangle']==1
duplicate=frame.copy();duplicate.loc[1,'OBJECTID']=1
try:select_wildfire_occurrences(duplicate,counties,'2020-01-01','2021-01-01')
except ValueError:pass
else:raise AssertionError('Duplicate source identifiers were accepted.')

with tempfile.TemporaryDirectory(prefix='wui-diagnostics-') as tmp:
    directory=Path(tmp)
    profile=dict(driver='GTiff',height=2,width=3,count=1,dtype='float32',
                 crs='EPSG:26912',transform=from_origin(0,60,30,30),nodata=-9999.)
    arrays={'ndvi':[[.2,.3,-9999],[-9999,.6,.7]],'ndmi':[[.4,-9999,.5],[-9999,.6,.7]],
            'count':[[3,2,0],[4,3,0]]}
    for name,values in arrays.items():
        with rasterio.open(directory/(name+'.tif'),'w',**profile) as dst:
            dst.write(np.array(values,dtype='float32'),1)
    study=np.array([[True,True,True],[True,True,False]])
    availability=index_availability_counts(directory/'ndvi.tif',directory/'ndmi.tif',study)
    assert availability=={'both':2,'ndvi_only':1,'ndmi_only':1,'neither':1}
    assert observation_support_count(directory/'count.tif',study,3)==2
    # Identical counts on a second read establish the cache/rebuild reporting contract.
    assert index_availability_counts(directory/'ndvi.tif',directory/'ndmi.tif',study)==availability
print('PASS: wildfire-only selection, half-open dates, source reconciliation, explicit surrounding domain, duplicate rejection, and measured index/support counts.')
