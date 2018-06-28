import xarray as xar
import os
import matplotlib.pyplot as plt
import analyse_functions_neil as af
import numpy as np
import matplotlib as mpl
from matplotlib.backends.backend_pdf import PdfPages

__author__='Neil Lewis'

# SET DEFAULT FOINT SIZE FOR PLOTTING 
mpl.rcParams['font.size'] = 22
mpl.rcParams['legend.fontsize'] = 'large'
mpl.rcParams['figure.titlesize'] = 'large'

# LOAD DATA 
exp_folder_name = 'naka_eccentricity_0.0_20' #'project_3_omega_normal'
start_file = 10
end_file = 10 # 59
file_name = 'atmos_monthly.nc'
dataset = af.open_experiment(exp_folder_name, start_file, end_file, file_name)

# SET CONSTANTS
grav = 9.81
earth_radius = 6371000.

# CALCULATE MSE, DSE, LE, AND ASSOCIATED MERIDIONAL FLUXES 
af.calculate_static_energies(dataset, g=grav)

# TAKE ZONAL MEAN
pres_full_zm = dataset.pres_full.mean(('lon'))
# mse, dse, le
mse_flux_zm = dataset.mse_vflux.mean(('lon'))
dse_flux_zm = dataset.dse_vflux.mean(('lon'))
le_flux_zm  = dataset.le_vflux.mean(('lon'))


# INTEGRATE WITH PRE-FACTOR
# mse
int_mse_flux = 2 * np.pi * earth_radius * np.cos(dataset['lat'].values * np.pi / 180.) / grav * np.trapz(mse_flux_zm.values, x=pres_full_zm.values, axis=1)
int_mse_flux = np.mean(int_mse_flux, 0) / 1e15
# dse
int_dse_flux = 2 * np.pi * earth_radius * np.cos(dataset['lat'].values * np.pi / 180.) / grav * np.trapz(dse_flux_zm.values, x=pres_full_zm.values, axis=1)
int_dse_flux = np.mean(int_dse_flux, 0) / 1e15
# le
int_le_flux = 2 * np.pi * earth_radius * np.cos(dataset['lat'].values * np.pi / 180.) / grav * np.trapz(le_flux_zm.values, x=pres_full_zm.values, axis=1)
int_le_flux = np.mean(int_le_flux, 0) / 1e15


#PLOT
fig = plt.figure(1, figsize=(12,10))
ax = plt.gca()

ax.plot(dataset['lat'].values, int_mse_flux, color='k', linewidth=3, label=r'$MSE$')
ax.plot(dataset['lat'].values, int_dse_flux, color='tab:gray', linewidth=3, label=r'$DSE$')
ax.plot(dataset['lat'].values, int_le_flux, color='silver', linewidth=3, label=r'$L_{v}q$')

ax.grid(linestyle=':', alpha=0.5)
ax.tick_params(direction='in',
                bottom=True, top=True, left=True, right=True,
                labelbottom=True, labeltop=False, labelleft=True, labelright=False)
ax.set_xlabel(r'Latitude')
ax.set_ylabel(r'Flux (PW)')
ax.legend(loc='best', fontsize=19)



plt.show()

# SAVE FIGURE TO PDF
#pdf_file = PdfPages('mse_flux.pdf')
#pdf_file.savefig(fig)
#pdf_file.close()

