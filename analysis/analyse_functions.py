import xarray as xar
import os
import matplotlib.pyplot as plt
import numpy as np
import pdb
import time
import calendar_calc as cal

def open_experiment(exp_folder_name, start_file, end_file, file_name):
    """Simple function to open netcdf files as one dataset object in xarray"""

    base_dir = os.environ['GFDL_DATA']

    folder_list = ['run%04d' % m for m in range(start_file, end_file+1)] 
    files = [base_dir + '/' + exp_folder_name+ '/' + folder_list[i] + '/' + file_name for i in range(len(folder_list))]

    files_exist=[os.path.isfile(s) for s in files]

    if not(all(files_exist)):
        raise EOFError('EXITING BECAUSE OF MISSING FILES', [files[elem] for elem in range(len(files_exist)) if not files_exist[elem]])

    ds = xar.open_mfdataset(files, decode_times=False)  

    add_extra_time_axes(ds, file_name)

    return ds

def open_reanalysis(file_path):
    """Simple function to open netcdf files as one dataset object in xarray"""

    files = [file_path]

    files_exist=[os.path.isfile(s) for s in files]

    if not(all(files_exist)):
        raise EOFError('EXITING BECAUSE OF MISSING FILES', [files[elem] for elem in range(len(files_exist)) if not files_exist[elem]])

    ds = xar.open_dataset(files[0],decode_times = False)

    add_extra_time_axes(ds, files[0])

    return ds

def add_extra_time_axes(ds_in, file_name):
    """Function that adds extra time axes to xarray coordinates, making actions such as 
    `groupby('seasons').mean('time')` possible, even with the model's 360_day calendar.
    """

    if 'atmos_monthly' in file_name:
        ds_in.attrs['data_type']='monthly'
    elif 'atmos_daily' in file_name:
        ds_in.attrs['data_type']='daily' 

    try:
        calendar_type = ds_in.time.calendar_type
    except:
        calendar_type = ds_in.time.calendar

    date_arr = cal.day_number_to_date(ds_in.time, calendar_type=calendar_type, units_in=ds_in.time.units)

    seasons_arr = cal.month_to_season(date_arr.month, ds_in.attrs['data_type'])

    ds_in.coords['dayofyear'] = (('time'),date_arr.dayofyear)
    ds_in.coords['months'] = (('time'),date_arr.month)
    ds_in.coords['years'] = (('time'),date_arr.year)
    ds_in.coords['seasons'] = (('time'), seasons_arr)

    ds_in.coords['seq_days'] = (('time'),cal.recurring_to_sequential(date_arr.dayofyear))    
    ds_in.coords['seq_months'] = (('time'),cal.recurring_to_sequential(date_arr.month))
    ds_in.coords['seq_years'] = (('time'),cal.recurring_to_sequential(date_arr.year))    
    ds_in.coords['seq_seasons'] = (('time'),cal.recurring_to_sequential(seasons_arr))


def global_average_lat_lon(ds_in, var_name):

    try:
        ds_in['area_array']
    except KeyError:
        cell_area(ds_in)

    weighted_data = ds_in[var_name]*ds_in['area_array']

    area_average = weighted_data.mean(('lat', 'lon')) / ds_in['area_array'].mean(('lat','lon'))

    var_in_dims = ds_in[var_name].dims

    var_out_dims = tuple(x for x in var_in_dims if x!='lat' and x!='lon')

    ds_in[var_name+'_area_av'] = (var_out_dims, area_average)

def cell_area(dataset_in, radius = 6371.e3):

    lonb = dataset_in['lonb']
    latb = dataset_in['latb']

    lonb_1 = lonb[1::].values
    lonb_2 = lonb[0:-1].values

    delta_lon = lonb_1 - lonb_2

    latb_1 = latb[1::].values
    latb_2 = latb[0:-1].values

    delta_lat = latb_1 - latb_2

    dataset_in['delta_lon'] = (('lon'), delta_lon)
    dataset_in['delta_lat'] = (('lat'), delta_lat)

    dataset_in['latb_1'] = (('lat'), latb_1)
    dataset_in['latb_2'] = (('lat'), latb_2)

    xsize = radius*np.absolute(np.deg2rad(dataset_in['delta_lon']))*(np.sin(np.deg2rad(dataset_in['latb_1']))-np.sin(np.deg2rad(dataset_in['latb_2'])))
    ysize = radius

    area_array = xsize*ysize

    dataset_in['area_array'] = (('lat','lon'), area_array.transpose('lat','lon'))
