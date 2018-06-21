import xarray as xar
import os
import matplotlib.pyplot as plt
import analyse_functions as af
import numpy as np

file_name = '/home/netapp-clima-scratch/sthomson/hadisst/had_isst_195801-201512_atmos_monthly.nc'

dataset = af.open_reanalysis(file_name)

dataset.t_surf.groupby('months').mean('time').plot.contourf(col='months', col_wrap=4)


monthly_zonal_mean = dataset.t_surf.mean('lon').groupby('months').mean('time')

plt.figure()
for month_idx in range(12):
    plt.plot(monthly_zonal_mean.lat, monthly_zonal_mean[month_idx,:], label=str(month_idx))

plt.legend()

plt.title('Zonal mean hadisst vs time')
plt.xlabel('Latitude (degrees)')
plt.ylabel('SST (degrees C)')

fig = plt.figure()

lat_2d, months_2d = np.meshgrid(monthly_zonal_mean.lat, monthly_zonal_mean.months)

cf = plt.contourf(months_2d, lat_2d, monthly_zonal_mean)

fig.colorbar(cf)

plt.title('Zonal mean hadisst vs time')
plt.xlabel('Time (months)')
plt.ylabel('Latitude (degrees)')


plt.show()


