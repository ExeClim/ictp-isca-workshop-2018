import xarray as xar
import os
import matplotlib.pyplot as plt
import analyse_functions as af

#Details of first experiment to be analysed
exp_folder_name = 'project_3_omega_normal'
start_file = 1
end_file = 12
file_name = 'atmos_monthly.nc'

#Details of second experiment to be analysed
exp_folder_name_2 = 'project_3_omega_reversed'
start_file_2 = 1
end_file_2 = 12
file_name_2 = 'atmos_monthly.nc'

#Read in both as xarray datasets
dataset = af.open_experiment(exp_folder_name, start_file, end_file, file_name)
dataset_2 = af.open_experiment(exp_folder_name_2, start_file_2, end_file_2, file_name_2)

#Perform diff on datasets
dataset_diff = dataset - dataset_2

#Make plots of zonal-mean zonal wind in each dataset individually, and their differences
plt.figure()
dataset.ucomp.mean(('lon','time')).plot.contourf()
plt.ylim(dataset.pfull.max(), 0.)

plt.figure()
dataset_2.ucomp.mean(('lon','time')).plot.contourf()
plt.ylim(dataset_2.pfull.max(), 0.)

plt.figure()
dataset_diff.ucomp.mean(('lon','time')).plot.contourf()
plt.ylim(dataset_diff.pfull.max(), 0.)

plt.show()

