import xarray as xr
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeat

# Load the GRIB data
ds = xr.open_dataset('era5-monthly-ws10-JFM.grib', engine = 'cfgrib')
# Here the following steps:
# 1. Convert longitude from 0-360 to -180-180
# 2. Select only latitude and longitude for Europe
# 3. Do the annual mean
ds_sel = ds.assign_coords(longitude=(((ds.longitude + 180) % 360) - 180)).sortby('longitude').sel(latitude = slice(75, 35), longitude = slice(-20, 65)).groupby('time.year').mean(dim = 'time')  

# Climatology
ds_clim = ds_sel.mean(dim='year')
# Anomaly
ds_anom = ds_sel - ds_clim

# Read the coordinates from the file
coords = pd.read_csv('coords.csv')
for index, row in coords.iterrows():
    
    # Select the target point
    target = ds_anom.sel(longitude = row.lon, latitude = row.lat, method = 'nearest')
    # Stack the point
    x = ds_anom.stack(x = ('latitude','longitude'))

    # Function to compute the correlation: si10 is the name of the wind speed variable
    def pt_corr(x):
        cf = np.corrcoef(x.si10.values[:,0], target.si10.values)[0,1] 
        
        # In case of nan return -1 (not needed for ERA5 though)
        if np.isnan(cf):
            return(xr.DataArray(-1))
        else:
            return(xr.DataArray(cf))

    # Apply the correlation function over the stacked dimensions
    cm = x.groupby('x').apply(pt_corr)
    # Unstack
    cormap = cm.unstack('x')

    # PLOT
    fig = plt.figure(figsize=(10, 8))
    ax = plt.axes(projection=ccrs.Mollweide())
    im = cormap.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), levels = 23)
    ax.scatter(x = row.lon, y = row.lat, s = 200, color='black', marker='+', transform=ccrs.PlateCarree())
    ax.set_global()
    ax.coastlines(resolution='10m', color='black', linewidth=1)
    ax.set_extent([-10, 33, 35, 75])
    
    plt.savefig(f'out_{index:03}.png', dpi = 200)
    plt.close()

