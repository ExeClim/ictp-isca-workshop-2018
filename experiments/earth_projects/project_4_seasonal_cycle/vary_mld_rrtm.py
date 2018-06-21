import os

import numpy as np

from isca import IscaCodeBase, DiagTable, Experiment, Namelist, GFDL_BASE

base_dir = os.path.dirname(os.path.realpath(__file__))

#Step 1: Point the python script to the location of the code (the bash environment variable GFDL_BASE is that directory)
cb = IscaCodeBase.from_directory(GFDL_BASE)

#Step 2. Provide the necessary inputs for the model to run:


inputfiles = [os.path.join(GFDL_BASE,'input/rrtm_input_files/ozone_1990.nc')]

#Define the diagnostics we want to be output from the model
diag = DiagTable()
diag.add_file('atmos_monthly', 30, 'days', time_units='days')

#Tell model which diagnostics to write to those files
diag.add_field('dynamics', 'ps', time_avg=True)
diag.add_field('dynamics', 'bk')
diag.add_field('dynamics', 'pk')
diag.add_field('dynamics', 'zsurf')
diag.add_field('atmosphere', 'precipitation', time_avg=True)
diag.add_field('mixed_layer', 't_surf', time_avg=True)
diag.add_field('dynamics', 'sphum', time_avg=True)
diag.add_field('dynamics', 'ucomp', time_avg=True)
diag.add_field('dynamics', 'vcomp', time_avg=True)
diag.add_field('dynamics', 'temp', time_avg=True)
diag.add_field('dynamics', 'vor', time_avg=True)
diag.add_field('dynamics', 'div', time_avg=True)
diag.add_field('dynamics', 'height', time_avg=True)



#Step 3. Define the namelist options, which will get passed to the fortran to configure the model.
namelist = Namelist({
    'main_nml':{
     'days'   : 30,
     'hours'  : 0,
     'minutes': 0,
     'seconds': 0,
     'dt_atmos':720,
     'current_date' : [1,1,1,0,0,0],
     'calendar' : 'thirty_day'
    },

    'idealized_moist_phys_nml': {
        'do_damping': True,
        'turb':True,
        'mixed_layer_bc':True,
        'do_virtual' :False,
        'do_simple': True,
        'roughness_mom':3.21e-05,
        'roughness_heat':3.21e-05,
        'roughness_moist':3.21e-05,
        'two_stream_gray': False, #Use RRTM, not grey radiation:
        'do_rrtm_radiation':True,
        'convection_scheme': 'FULL_BETTS_MILLER' #Use the full Betts-miller convection scheme
    },

    'vert_turb_driver_nml': {
        'do_mellor_yamada': False,     # default: True
        'do_diffusivity': True,        # default: False
        'do_simple': True,             # default: False
        'constant_gust': 0.0,          # default: 1.0
        'use_tau': False
    },

    'diffusivity_nml': {
        'do_entrain':False,
        'do_simple': True,
    },

    'surface_flux_nml': {
        'use_virtual_temp': False,
        'do_simple': True,
        'old_dtaudv': True
    },

    'atmosphere_nml': {
        'idealized_moist_model': True
    },

    #Use a large mixed-layer depth, and the Albedo of the CTRL case in Jucker & Gerber, 2017
    'mixed_layer_nml': {
        'tconst' : 285.,
        'prescribe_initial_dist':True,
        'evaporation':True,
        'albedo_value': 0.25, #set albedo value
        'do_qflux' : False, #Do not use prescribed form for q-fluxes
    },

    'betts_miller_nml': {
       'rhbm': .7   ,
       'do_simp': False,
       'do_shallower': True,
    },

    'lscale_cond_nml': {
        'do_simple':True,
        'do_evap':True
    },

    'sat_vapor_pres_nml': {
        'do_simple':True
    },

    'damping_driver_nml': {
        'do_rayleigh': True,
        'trayfric': -0.5,              # neg. value: time in *days*
        'sponge_pbottom':  150., #Setting the lower pressure boundary for the model sponge layer in Pa.
        'do_conserve_energy': True,
    },

    'rrtm_radiation_nml': {
        'do_read_ozone':True,
        'ozone_file':'ozone_1990',
        'solr_cnst': 1360., #s set solar constant to 1360, rather than default of 1368.22
        'dt_rad': 4320, #Use 4320 as RRTM radiation timestep
    },

    # FMS Framework configuration
    'diag_manager_nml': {
        'mix_snapshot_average_fields': False  # time avg fields are labelled with time in middle of window
    },

    'fms_nml': {
        'domains_stack_size': 600000                        # default: 0
    },

    'fms_io_nml': {
        'threading_write': 'single',                         # default: multi
        'fileset_write': 'single',                           # default: multi
    },

    'spectral_dynamics_nml': {
        'damping_order': 4,
        'water_correction_limit': 200.e2,
        'reference_sea_level_press':1.0e5,
        'valid_range_t':[100.,800.],
        'initial_sphum':[2.e-6],
        'vert_coord_option':'uneven_sigma',
        'surf_res':0.2, #Parameter that sets the vertical distribution of sigma levels
        'scale_heights' : 11.0,
        'exponent':7.0,
        'robert_coeff':0.03
    }
})

#Step 4. Compile the fortran code
cb.compile()

#Number of cores to run the model on
NCORES=16

#Set the horizontal and vertical resolution to be used. 
RESOLUTION = 'T21', 18

mld_values_list = [20.,5.]

for mld_value in mld_values_list:
    #Set up the experiment object, with the first argument being the experiment name.
    #This will be the name of the folder that the data will appear in.

    exp = Experiment('project_4_rrtm_mld_'+str(mld_value), codebase=cb)
    exp.clear_rundir()

    exp.diag_table = diag
    exp.inputfiles = inputfiles

    exp.namelist = namelist.copy()
    exp.namelist['mixed_layer_nml']['depth'] = mld_value

    exp.set_resolution(*RESOLUTION)
    #Step 6. Run the fortran code

    exp.run(1, use_restart=False, num_cores=NCORES)
    for i in range(2,121):
        exp.run(i, num_cores=NCORES)
