import xarray as xar
import os
import matplotlib.pyplot as plt
import analyse_functions as af

file_name = '/home/netapp-clima-scratch/sthomson/jra_55/jra_55_1958_2016_atmos_monthly_climatology.nc'

dataset = af.open_reanalysis(file_name)

dataset.ucomp.mean(('lon','time')).plot.contourf()
plt.ylim(dataset.pfull.max(), 0.)

dataset.temp.sel(pfull=1000.,method='nearest').groupby('months').mean('time').plot.contourf(col='months', col_wrap=4)

dataset.ucomp.groupby('seasons').mean(('lon','time')).plot.contourf(col='seasons', col_wrap=2)
plt.ylim(dataset.pfull.max(), 0.)

plt.show()


