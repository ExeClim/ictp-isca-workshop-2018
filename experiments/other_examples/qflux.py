
from isca import Experiment, IscaCodeBase, GFDL_BASE
from isca.util import run_cli

from config import diag_table, namelist, inputfiles

codebase = IscaCodeBase.from_directory(GFDL_BASE)

experiments = [
    ('qflux_on', {
        'mixed_layer_nml': {'do_qflux': True},
        'qflux_nml': {'qflux_amp': 30.0, 'qflux_width': 16.0}
    }),
    ('qflux_off', {'mixed_layer_nml': {'do_qflux': False}})
    ]

exps = []
for exp_name, parameters in experiments:
    exp = Experiment(exp_name, codebase=codebase)

    # Get some basic paramters from config.py.  We'll copy the Namelist,
    # DiagTable and input files list so for multiple Experiments in the
    # same file, each has their own version that can be edited independently.
    exp.diag_table = diag_table.copy()
    exp.namelist = namelist.copy()
    exp.inputfiles = inputfiles[::]

    exp.set_resolution('T42', 40)
    exp.update_namelist(parameters)
    exps.append(exp)

run_cli(exps)