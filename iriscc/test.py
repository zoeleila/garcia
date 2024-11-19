import numpy as np
import xarray as xr
import pandas as pd

x = np.zeros(3)
print(x)
data = np.random.rand(4, 3)

locs = ["IA", "IL", "IN"]

times = pd.date_range("2000-01-01", periods=4)

foo = xr.DataArray(data, coords=[times, locs], dims=["time", "space"])
print(foo)