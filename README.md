# ERA5 spatial correlation: source code
Source code for the video https://www.youtube.com/watch?v=xpBijQev-4s

[![Youtube video](http://img.youtube.com/vi/xpBijQev-4s/0.jpg)](http://www.youtube.com/watch?v=xpBijQev-4s)

The code is written in Python and it is very easy. The data is freely available (after a [registration to the Copernicus Data Store](https://cds.climate.copernicus.eu/)) and can be downloaded using the script `download.py`. 

To read the GRIB with xarray you need the [`cfgrib` package](https://github.com/ecmwf/cfgrib) (available on PIP, anaconda, etc.)

The computation of the correlation is very naive, I have the strong feeling that it might be improved and possibly distributed in case of large datasets using `dask`. 
