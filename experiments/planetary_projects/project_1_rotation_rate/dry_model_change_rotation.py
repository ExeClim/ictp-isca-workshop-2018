import os

import numpy as np

from isca import IscaCodeBase, DiagTable, Experiment, Namelist, GFDL_BASE

base_dir = os.path.dirname(os.path.realpath(__file__))

#Step 1: Point the python script to the location of the code (the bash environment variable GFDL_BASE is that directory)
cb = IscaCodeBase.from_directory(GFDL_BASE)

#Step 2. Provide the necessary inputs for the model to run:


inputfiles=[]

#Define the diagnostics we want to be output from the model
diag = DiagTable()
diag.add_file('atmos_monthly', 30, 'days', time_units='days')

#Tell model which diagnostics to write to those files
diag.add_field('dynamics', 'ps', time_avg=True)
diag.add_field('dynamics', 'bk')
diag.add_field('dynamics', 'pk')
diag.add_field('dynamics', 'zsurf')
diag.add_field('dynamics', 'sphum', time_avg=True)
diag.add_field('dynamics', 'ucomp', time_avg=True)
diag.add_field('dynamics', 'vcomp', time_avg=True)
diag.add_field('dynamics', 'temp', time_avg=True)
diag.add_field('dynamics', 'vor', time_avg=True)
diag.add_field('dynamics', 'div', time_avg=True)
diag.add_field('dynamics', 'height', time_avg=True)

#Step 3. Define the namelist options, which will get passed to the fortran to configure the model.
namelist = Namelist({
    'main_nml': {
        'dt_atmos': 600,
        'days': 30,
        'calendar': 'thirty_day',
        'current_date': [2000,1,1,0,0,0]
    },

    'atmosphere_nml': {
        'idealized_moist_model': False  # False for Newtonian Cooling.  True for Isca/Frierson
    },

    'spectral_dynamics_nml': {
        'damping_order'           : 4,                      # default: 2
        'water_correction_limit'  : 200.e2,                 # default: 0
        'reference_sea_level_press': 1.0e5,                  # default: 101325
        'valid_range_t'           : [100., 800.],           # default: (100, 500)
        'initial_sphum'           : 0.0,                  # default: 0
        'vert_coord_option'       : 'uneven_sigma',         # default: 'even_sigma'
        'scale_heights': 6.0,
        'exponent': 7.5,
        'surf_res': 0.5
    },

    # configure the relaxation profile
    'hs_forcing_nml': {
        't_zero': 315.,    # temperature at reference pressure at equator (default 315K)
        't_strat': 200.,   # stratosphere temperature (default 200K)
        'delh': 60.,       # equator-pole temp gradient (default 60K)
        'delv': 10.,       # lapse rate (default 10K)
        'eps': 0.,         # stratospheric latitudinal variation (default 0K)
        'sigma_b': 0.7,    # boundary layer friction height (default p/ps = sigma = 0.7)

        # negative sign is a flag indicating that the units are days
        'ka':   -40.,      # Constant Newtonian cooling timescale (default 40 days)
        'ks':    -4.,      # Boundary layer dependent cooling timescale (default 4 days)
        'kf':   -1.,       # BL momentum frictional timescale (default 1 days)

        'do_conserve_energy':   True,  # convert dissipated momentum into heat (default True)
    },

    'diag_manager_nml': {
        'mix_snapshot_average_fields': False
    },

    'fms_nml': {
        'domains_stack_size': 600000                        # default: 0
    },

    'fms_io_nml': {
        'threading_write': 'single',                         # default: multi
        'fileset_write': 'single',                           # default: multi
    },

    'constants_nml': {
        'omega':7.2921150e-5,
    },

})


#Step 4. Compile the fortran code
cb.compile()

#Number of cores to run the model on
NCORES=16

#Set the horizontal and vertical resolution to be used. 
RESOLUTION = 'T21', 25

earth_rot_rate = 7.2921150e-5

rotation_rates_earth_multiple = [1, 2, 0.5]

for rot_rate_scale in rotation_rates_earth_multiple:
    #Set up the experiment object, with the first argument being the experiment name.
    #This will be the name of the folder that the data will appear in.

    exp = Experiment('project_1_rotation_rate_earth_multiple_'+str(rot_rate_scale), codebase=cb)
    exp.clear_rundir()

    exp.diag_table = diag
    exp.inputfiles = inputfiles

    exp.namelist = namelist.copy()
    exp.namelist['constants_nml']['omega'] = earth_rot_rate * rot_rate_scale

    exp.set_resolution(*RESOLUTION)
    #Step 6. Run the fortran code

    exp.run(1, use_restart=False, num_cores=NCORES)
    for i in range(2,121):
        exp.run(i, num_cores=NCORES)
