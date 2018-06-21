import xarray as xar
import os
import matplotlib.pyplot as plt
import analyse_functions as af

exp_folder_name = 'project_6_aquaplanet_obliq_23.439'
start_file = 1
end_file = 120

file_name = 'atmos_monthly.nc'

dataset = af.open_experiment(exp_folder_name, start_file, end_file, file_name)

dataset.ucomp.mean(('lon','time')).plot.contourf()
plt.ylim(dataset.pfull.max(), 0.)

af.global_average_lat_lon(dataset, 't_surf')
plt.figure()
dataset.t_surf_area_av.plot.line()

af.global_average_lat_lon(dataset, 'temp')
plt.figure()
dataset.temp_area_av.transpose('pfull', 'time').plot.contourf()
plt.ylim(dataset.pfull.max(), 0.)


dataset.t_surf.groupby('seasons').mean('time').plot.contourf(col='seasons', col_wrap=2)

dataset.ucomp.groupby('seasons').mean(('lon','time')).plot.contourf(col='seasons', col_wrap=2)
plt.ylim(dataset.pfull.max(), 0.)

plt.show()


