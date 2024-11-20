import sys
sys.path.append('.')

import xarray as xr
import numpy as np

from iriscc.settings import SAFRAN_RAW_DIR

ds_grid = xr.open_dataset('/gpfs-calypso/scratch/globc/garcia/utils/tasmax_1d_21000101_21001231.nc')
lon_grid = ds_grid['lon'].values
lat_grid = ds_grid['lat'].values

ds = xr.open_dataset(SAFRAN_RAW_DIR / 'SAFRAN_2020080107_2021080106.nc')
lon = ds['LON'].values
lat = ds['LAT'].values
tas = ds['Tair'].values
time = ds.time.values

print(lat.min(), lat.max(), lat_grid.min(), lat_grid.max())
print(lon.min(), lon.max(), lon_grid.min(), lon_grid.max())

tas_grid = np.zeros(np.shape(lon_grid)) #changer les 0
print(np.shape(tas_grid))
