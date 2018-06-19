import os

import numpy as np

from isca import IscaCodeBase, DiagTable, Experiment, Namelist, GFDL_BASE

base_dir = os.path.dirname(os.path.realpath(__file__))
# a CodeBase can be a directory on the computer,
# useful for iterative development
cb = IscaCodeBase.from_directory(GFDL_BASE)

# or it can point to a specific git repo and commit id.
# This method should ensure future, independent, reproducibility of results.
# cb = IscaCodeBase.from_repo(repo='https://github.com/ExeClim/Isca', commit='86893cc')

# compilation depends on computer specific settings.  The $GFDL_ENV
# environment variable is used to determine which `$GFDL_BASE/src/extra/env` file
# is used to load the correct compilers.  The env file is always loaded from
# $GFDL_BASE and not the checked out git repo.

# create an Experiment object to handle the configuration of model parameters
# and output diagnostics

inputfiles = [os.path.join(GFDL_BASE,'input/rrtm_input_files/ozone_1990.nc'),os.path.join(GFDL_BASE,'input/land_masks/era_land_t21.nc')]

#Tell model how to write diagnostics
diag = DiagTable()
diag.add_file('atmos_monthly', 30, 'days', time_units='days')

#Tell model which diagnostics to write
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
diag.add_field('rrtm_radiation', 'coszen', time_avg=True)

#Empty the run directory ready to run

#Define values for the 'core' namelist
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
        'convection_scheme': 'FULL_BETTS_MILLER', #Use the full Betts-miller convection schemei
        'land_option': 'input',                      #Use land mask from input file
        'land_file_name': 'INPUT/era_land_t21.nc',   #Tell model where to find input file
        'land_roughness_prefactor': 10.0,            #How much rougher to make land than ocean
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
        'old_dtaudv': True,
        'land_evap_prefactor':0.7,
    },

    'atmosphere_nml': {
        'idealized_moist_model': True
    },

    'mixed_layer_nml': {
        'tconst' : 285.,
        'prescribe_initial_dist':True,
        'evaporation':True,
        'depth': 20., #Use shallow mixed-layer depth
        'albedo_value': 0.25, #set albedo value
        'do_qflux' : False, #Do not use prescribed form for q-fluxes
        'land_option' : 'input',              #Tell mixed layer to get land mask from input file
        'land_h_capacity_prefactor' : 0.1,    #What factor to multiply mixed-layer depth by over land.
        'land_albedo_prefactor' : 1.3,        #What factor to multiply ocean albedo by over land
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
        'solday':90,
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
        'num_levels':40,
        'valid_range_t':[100.,800.],
        'initial_sphum':[2.e-6],
        'vert_coord_option':'uneven_sigma',
        'surf_res':0.2, #Parameter that sets the vertical distribution of sigma levels
        'scale_heights' : 11.0,
        'exponent':7.0,
        'robert_coeff':0.03,
        'ocean_topog_smoothing':0.8,
    },

    'spectral_init_cond_nml': {
        'topog_file_name' : 'era_land_t21.nc', #Name of land input file, which will also contain topography if generated using Isca's `land_file_generator_fn.py' routine.
        'topography_option' : 'input', #Tell model to get topography from input file
    },

    'constants_nml': {
        'omega':7.2921150e-5,
    },

})

#Lets do a run!
if __name__=="__main__":
    cb.compile()

    NCORES=16
    RESOLUTION = 'T21', 40
    omega_values_list = ['normal', 'reversed']
    omega_normal = 7.2921150e-5

    for omega_value in omega_values_list:

        if omega_value=='reversed':
            omega_passed = -omega_normal
        else:
            omega_passed = omega_normal


        exp = Experiment('project_3_omega_'+str(omega_value), codebase=cb)
        exp.clear_rundir()

        exp.diag_table = diag
        exp.inputfiles = inputfiles

        exp.namelist = namelist.copy()
        exp.namelist['constants_nml']['omega'] = omega_passed

        exp.set_resolution(*RESOLUTION)

        exp.run(1, use_restart=False, num_cores=NCORES)
        for i in range(2,241):
            exp.run(i, num_cores=NCORES)
