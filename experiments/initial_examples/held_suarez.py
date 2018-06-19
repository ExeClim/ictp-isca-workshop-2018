import os

import numpy as np

from isca import IscaCodeBase, DiagTable, Experiment, Namelist, GFDL_BASE

base_dir = os.path.dirname(os.path.realpath(__file__))

#Step 1: Point the python script to the location of the code (the bash environment variable GFDL_BASE is that directory)
cb = IscaCodeBase.from_directory(GFDL_BASE)

#Step 2. Provide the necessary inputs for the model to run:

#Input files (none required for simple Held Suarez, so the list is empty)
inputfiles=[]

#Define the diagnostics we want to be output from the model
diag = DiagTable()
#We might want monthly output, so the file name will be 'atmos_monthly', and the timescale for the averaging window is 30 days.
diag.add_file('atmos_monthly', 30, 'days', time_units='days')
#We might also want daily output, so add that too:
diag.add_file('atmos_daily', 1, 'days', time_units='days')

#Tell model which diagnostics to write to those files
#The format is:
#diag.add_field(MODULE_NAME, VARIABLE_NAME, time_avg=True or False, files=LIST_OF_WHICH_FILES TO INCLUDE THIS VARIABLE IN (default is all files)

diag.add_field('dynamics', 'ps', time_avg=True)
diag.add_field('dynamics', 'bk')
diag.add_field('dynamics', 'pk')
diag.add_field('dynamics', 'zsurf')
diag.add_field('dynamics', 'sphum', time_avg=True)
diag.add_field('dynamics', 'ucomp', time_avg=True)
diag.add_field('dynamics', 'vcomp', time_avg=True)
diag.add_field('dynamics', 'temp', time_avg=True)
diag.add_field('dynamics', 'vor', time_avg=True, files=['atmos_monthly']) #This will only include vorticity output in atmos_monthly
diag.add_field('dynamics', 'div', time_avg=True, files = ['atmos_daily']) #This will only include divergence output in atmos_daily
diag.add_field('dynamics', 'height', time_avg=True)

#Step 3. Define the namelist options, which will get passed to the fortran to configure the model.

#The namelist object is a dictionary, with keys that are the namelist names, e.g. 'main_nml', 'atmosphere_nml'. 
#Those keys then correspond to individual dictionaries that are the namelist options for that namelist.

namelist = Namelist({
    'main_nml': {
        'dt_atmos': 600,
        'days': 30,
        'calendar': 'thirty_day',
        'current_date': [2000,1,1,0,0,0]
    },

    'atmosphere_nml': {
        'idealized_moist_model': False  # False for Newtonian Cooling.  True for model with 'full physics'
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
    }
})


if __name__=="__main__":
    #Step 4. Compile the fortran code
    cb.compile()

    #Step 5. Prepare the experiment object, including experiment name
    
    #Number of cores to run the model on
    NCORES=4 

    #Set the horizontal and vertical resolution to be used. 
    #Format is 'T**', n_levels
    # where ** is the spectral resolution, e.g. 'T21' and n_levels is the number of vertical levels to be used
    RESOLUTION = 'T21', 25

    #Set up the experiment object, with the first argument being the experiment name.
    #This will be the name of the folder that the data will appear in.

    exp = Experiment('held_suarez_example_experiment', codebase=cb)
    exp.clear_rundir()

    exp.diag_table = diag
    exp.inputfiles = inputfiles

    exp.namelist = namelist.copy()

    exp.set_resolution(*RESOLUTION)
    
    #Step 6. Run the fortran code
    #The model is run in small chunks, one chunk per `exp.run` command.
    #The length of time corresponding to each chunk is set in `main_nml` above. 
    #The current example will therefore run 12 sets of 30 days.

    exp.run(1, use_restart=False, num_cores=NCORES)
    for i in range(2,13):
        exp.run(i, num_cores=NCORES)
