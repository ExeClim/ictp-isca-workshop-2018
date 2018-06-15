import os

import f90nml

from isca import Namelist, DiagTable, GFDL_BASE

_filepath = os.path.dirname(os.path.realpath(__file__))

# A simple output diagnostic table.
diag_table = DiagTable()
diag_table.add_file('atmos_daily', 1, 'days', time_units='days')
diag_table.add_field('dynamics', 'ps', time_avg=True)
diag_table.add_field('dynamics', 'bk')
diag_table.add_field('dynamics', 'pk')
diag_table.add_field('dynamics', 'sphum', time_avg=True)
diag_table.add_field('dynamics', 'ucomp', time_avg=True)
diag_table.add_field('dynamics', 'vcomp', time_avg=True)
diag_table.add_field('dynamics', 'temp', time_avg=True)
diag_table.add_field('dynamics', 'vor', time_avg=True)
diag_table.add_field('dynamics', 'div', time_avg=True)
diag_table.add_field('atmosphere', 'precipitation', time_avg=True)
diag_table.add_field('mixed_layer', 't_surf', time_avg=True)
diag_table.add_field('rrtm_radiation', 'coszen', time_avg=True)
diag_table.add_field('rrtm_radiation', 'olr', time_avg=True)

# Load the namelist file into a namelist object
# this can then be easily modified in your experiment script
namelist = f90nml.read(os.path.join(_filepath, 'basic_isca.nml'))

inputfiles = [os.path.join(GFDL_BASE,'input/rrtm_input_files/ozone_1990.nc')]