import matplotlib.pyplot as plt
import analyse_functions_neil as af
import matplotlib as mpl
import numpy as np 
from matplotlib.backends.backend_pdf import PdfPages

__author__='Neil Lewis'

# SET DEFAULT FOINT SIZE FOR PLOTTING 
mpl.rcParams['font.size'] = 22
mpl.rcParams['legend.fontsize'] = 'large'
mpl.rcParams['figure.titlesize'] = 'large'

# LOAD DATA 
exp_folder_name = 'frierson_eccentricity_0.0_20_obliq20.0_eqi_False' #'project_3_omega_normal'
start_file = 4
end_file = 6 # 59
file_name = 'atmos_monthly.nc'
dataset = af.open_experiment(exp_folder_name, start_file, end_file, file_name)

# CALCULATE MASS STREAMFUNCTION 
af.mass_streamfunction(dataset)
# time average
psi_mean = dataset.psi.mean(('time'))


#PLOT
# make figure
fig = plt.figure(1, figsize=(12,10))
ax = plt.gca()

# calculate contour levels
lb = af.rounddown(np.amin(psi_mean.values))
ub = af.roundup(np.amax(psi_mean.values))
c_levels = np.arange(lb, ub+1, 10)

# contour plot
cs=plt.contour(dataset['lat'].values, dataset['pfull'].values, psi_mean.values, colors='k', levels=c_levels, linewdiths=3)
plt.clabel(cs, cs.levels[::4], inline = 1, fmt = '%1.0f',fontsize=14)


#optional plot wind, comment this out for streamfunction only 
ucomp_mean = dataset.ucomp.mean(('lon','time'))
lb = af.rounddown(np.amin(ucomp_mean.values))
ub = af.roundup(np.amax(ucomp_mean.values))
if lb < 0:
    if abs(lb) > ub:
        ub = -1 * lb
    else:
        lb = -1 * ub
c_levels = np.arange(lb, ub+1, 5)
ucomp_mean.plot.contourf(levels=c_levels, cmap=plt.cm.RdBu_r, add_colorbar=True)

# make pressure axis go from surface to top
plt.ylim(dataset.pfull.max(), 0.)






plt.show()

# SAVE FIGURE TO PDF
#pdf_file = PdfPages('hadley_streamfunction.pdf')
#pdf_file.savefig(fig)
#pdf_file.close()

