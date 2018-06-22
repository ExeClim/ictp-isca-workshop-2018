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
     'dt_atmos':300,
     'current_date' : [1,1,1,0,0,0],
     'calendar' : 'thirty_day'
    },

    'idealized_moist_phys_nml': {
        'do_damping': True,
        'turb':True,
        'mixed_layer_bc':True,
        'do_virtual' :False,
        'do_simple': False,
        'roughness_mom':3.21e-05,
        'roughness_heat':3.21e-05,
        'roughness_moist':3.21e-05,
        'two_stream_gray': False, #Use RRTM, not grey radiation:
        'do_rrtm_radiation':True,
        'convection_scheme': 'FULL_BETTS_MILLER', #Use the full Betts-miller convection schemei
    },

    'vert_turb_driver_nml': {
        'do_mellor_yamada': False,     # default: True
        'do_diffusivity': True,        # default: False
        'do_simple': False,            # default: False
        'constant_gust': 0.0,          # default: 1.0
        'use_tau': False
    },

    'diffusivity_nml': {
        'do_entrain':False,
        'do_simple': False,
    },

    'surface_flux_nml': {
        'use_virtual_temp': False,
        'do_simple': False,
        'old_dtaudv': True,
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
    },

    'betts_miller_nml': {
       'rhbm': .7   ,
       'do_simp': False,
       'do_shallower': True,
    },

    'lscale_cond_nml': {
        'do_simple':False,
        'do_evap':True
    },

    'sat_vapor_pres_nml': {
        'do_simple':False,
        'tcmin':  -223, #Make sure low temperature limit of saturation vapour pressure is low enough that it doesn't cause an error (note that this giant planet has no moisture anyway, so doesn't directly affect calculation.        
        'tcmax': 350.
    },

    'damping_driver_nml': {
        'do_rayleigh': True,
        'trayfric': -0.1,              # neg. value: time in *days*
        'sponge_pbottom':  150., #Setting the lower pressure boundary for the model sponge layer in Pa.
        'do_conserve_energy': True,
    },

    'rrtm_radiation_nml': {
        'do_read_ozone':False,
        'solr_cnst': 1360., #s set solar constant to 1360, rather than default of 1368.22
        'dt_rad': 3000, #Use 4320 as RRTM radiation timestep
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
        'valid_range_t':[10.,800.],
        'initial_sphum':[2.e-6],
        'vert_coord_option':'uneven_sigma',
        'surf_res':0.2, #Parameter that sets the vertical distribution of sigma levels
        'scale_heights' : 11.0,
        'exponent':7.0,
        'robert_coeff':0.03,
        'ocean_topog_smoothing':0.8,
    },
    'constants_nml': {
        'grav':9.80,
    },

})


#Step 4. Compile the fortran code
cb.compile()

#Number of cores to run the model on
NCORES=16

#Set the horizontal and vertical resolution to be used. 
RESOLUTION = 'T21', 40

earth_grav = 9.80

grav_earth_multiple = [2, 1.2, 1.]

for grav_scale in grav_earth_multiple:
    #Set up the experiment object, with the first argument being the experiment name.
    #This will be the name of the folder that the data will appear in.

    exp = Experiment('project_p2_rrtm_no_ozone_grav_earth_multiple_'+str(grav_scale), codebase=cb)
    exp.clear_rundir()

    exp.diag_table = diag
    exp.inputfiles = inputfiles

    exp.namelist = namelist.copy()

    exp.namelist['constants_nml']['pstd']     = 1.013250E+06 * grav_scale
    exp.namelist['constants_nml']['pstd_mks'] = 101325.0 * grav_scale
    exp.namelist['spectral_dynamics_nml']['reference_sea_level_press'] = 101325.0 * grav_scale
    exp.namelist['constants_nml']['grav'] = earth_grav * grav_scale
    exp.namelist['damping_driver_nml']['sponge_pbottom'] =  150. * grav_scale

    exp.set_resolution(*RESOLUTION)
    #Step 6. Run the fortran code

    try:
        exp.run(1, use_restart=False, num_cores=NCORES)
        for i in range(2,121):
            exp.run(i, num_cores=NCORES)
    except:
        pass
