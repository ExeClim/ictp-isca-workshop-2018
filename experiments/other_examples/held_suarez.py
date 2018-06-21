import logging

import numpy as np

from isca import IscaCodeBase, DryCodeBase, Experiment, DiagTable, Namelist, FailedRunError, log
from isca.util import exp_progress, run_cli

expname = 'held_suarez_basic'
cb = DryCodeBase(repo='https://github.com/execlim/isca', commit='v1.0')


NDAYS = 10
NRUNS = 4                    # total sim time = NDAYS*NRUNS
RESOLUTION = 'T42', 25

held_suarez_configuration = {
    # TEMPERATURE PROFILE
    't_zero': 315,     # maximum surface temperature forcing
    't_strat': 200,    # statospheric temperature constant
    'delh': 60,        # equator-pole temperature gradient
    'delv': 10.,       # vertical potential temperature gradient

    # RELAXATION TIMESCALES
    'ka': -20,         # Newtonian cooling timescale in atmosphere
    'ks': -5,          # Newtonian cooling timescale at surface
    'kf': -1,          # Rayleigh friction (pos. = seconds, neg. = days)
    }

namelist = Namelist({
    # model settings
    'main_nml': {
        'dt_atmos': 900,
        'days': NDAYS,
        'calendar': 'no_calendar',
    },
    'spectral_dynamics_nml': {
        'damping_order': 2,  # hyperviscosity 2=del4, 4=del8.
        'reference_sea_level_press': 1.0e5,  # default: 101325
        'valid_range_t': [150., 400.],
        # choose coordinate system to set level 7 at ~ 100hPa
        'vert_coord_option': 'uneven_sigma',  # default: 'even_sigma'
        'scale_heights': 6.0,
        'exponent': 7.5,
        'surf_res': 0.5,
    },
    'atmosphere_nml': {
        'idealized_moist_model': False  # run in HS-mode
    },
    'hs_forcing_nml': held_suarez_configuration,

    # framework and IO config
    'diag_manager_nml': {
        # diagmanager gives a warning if you don't set this
        'mix_snapshot_average_fields': False
    },
    'fms_nml': {
        'domains_stack_size': 600000  # default: 0
    },
    'fms_io_nml': {
        'threading_write': 'single',  # default: multi
        'fileset_write': 'single',  # default: multi
    },
})

diag_table = DiagTable()

#diag_table.add_file('6hourly', 6*60*60, 'seconds', time_units='days')
#diag_table.add_file('hourly', 1, 'hours', time_units='days')
diag_table.add_file('daily', 1, 'days', time_units='days')

diag_table.add_field('dynamics', 'ps')
diag_table.add_field('dynamics', 'bk')
diag_table.add_field('dynamics', 'pk')
diag_table.add_field('dynamics', 'ucomp')
diag_table.add_field('dynamics', 'vcomp')
diag_table.add_field('dynamics', 'omega')
diag_table.add_field('dynamics', 'temp')
diag_table.add_field('dynamics', 'vor')
diag_table.add_field('dynamics', 'div')
diag_table.add_field('dynamics', 'height')
diag_table.add_field('dynamics', 'height_half')

diag_table.add_field('hs_forcing', 'teq')
diag_table.add_field('hs_forcing', 'tdt')


# output log to a file as well as the terminal
fh = logging.FileHandler('held_suarez.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log.addHandler(fh)


exp = Experiment(expname, codebase=cb)

exp.diag_table = diag_table
exp.namelist = namelist
exp.set_resolution(*RESOLUTION)
exp.clear_rundir()

run_cli(exp)

# try:
#     with exp_progress(exp) as pbar:
#         exp.run(1, use_restart=False, num_cores=16, nice_score=0)

#     for i in range(NRUNS - 1):
#         with exp_progress(exp, description='o%.0f b%.0f d{day}' % (o, b)) as pbar:
#             run = i + 2   # 0 index and we have already done run 1
#             exp.run(run, num_cores=16, nice_score=0, mpirun_opts=' --bind-to socket ')

#     exp.log.info('Integration complete. Compiling output.')
#     completed = True
#     notify('{} complete'.format(exp.name), 'isca')
# except FailedRunError as e:
#     # ignore a failed run and carry on with parameter sweep
#     notify('{}/{} failed'.format(exp.name, i+2), 'isca')
#     continue



# # finally:
# #     #exp.clear_datadir()
# #     if completed and did_run:
# #         exp.log.info('Output compiled.  Copying.')
# #         sh.cp(P(exp.datadir, 'run1', 'daily.nc'), P(baseexp.datadir, '%s.nc' % expname))
# #         exp.log.info('Copy complete.')
# #     exp.rm_workdir()
# #exp.rm_datadir()
