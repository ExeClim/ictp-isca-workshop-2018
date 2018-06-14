import xarray as xar
import os
import matplotlib.pyplot as plt
import analyse_functions as af

exp_folder_name = 'project_3_omega_normal'
start_file = 1
end_file = 12

file_name = 'atmos_monthly.nc'

dataset = af.open_experiment(exp_folder_name, start_file, end_file, file_name)

dataset.ucomp.mean(('lon','time')).plot.contourf()
plt.ylim(dataset.pfull.max(), 0.)

plt.show()


