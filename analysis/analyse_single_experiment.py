import xarray as xar
import os
import matplotlib.pyplot as plt
import analyse_functions as af

#Folder name where data lies. Script will assume this data is in $GFDL_DATA directory
exp_folder_name = 'held_suarez_example_experiment'
#exp_folder_name = 'frierson_grey_rad_example_experiment'

#First month to be used
start_file = 1
#Final month to be used
end_file = 24

#Name of individual netcdf files to include. Example for monthly data.
file_name = 'atmos_monthly.nc'

#Open netcdf files as an xarray dataset object
dataset = af.open_experiment(exp_folder_name, start_file, end_file, file_name)

#Time and zonally average zonal wind and make contour plot
dataset.ucomp.mean(('lon','time')).plot.contourf()
plt.ylim(dataset.pfull.max(), 0.)
plt.title('Time-averaged zonal-mean zonal wind')

#Perform area mean of atmospheric temperatures and make contour plot
af.global_average_lat_lon(dataset, 'temp')
plt.figure()
dataset.temp_area_av.transpose('pfull', 'time').plot.contourf()
plt.ylim(dataset.pfull.max(), 0.)
plt.title('Time and height evolution of area-mean atmospheric temperature')

#Monthly-mean temp at 250hPa
dataset.temp.sel(pfull=250.,method='nearest').groupby('months').mean('time').plot.contourf(col='months', col_wrap=4)

#Seasonal mean zonal-mean zonal-wind
dataset.ucomp.groupby('seasons').mean(('lon','time')).plot.contourf(col='seasons', col_wrap=2)
plt.ylim(dataset.pfull.max(), 0.)

plt.show()


