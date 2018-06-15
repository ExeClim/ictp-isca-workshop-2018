import xarray as xar
import os
import matplotlib.pyplot as plt
import numpy as np
import pdb
import time

def open_experiment(exp_folder_name, start_file, end_file, file_name):

    base_dir = os.environ['GFDL_DATA']

    folder_list = ['run%04d' % m for m in range(start_file, end_file+1)] 
    files = [base_dir + '/' + exp_folder_name+ '/' + folder_list[i] + '/' + file_name for i in range(len(folder_list))]

    files_exist=[os.path.isfile(s) for s in files]

    if not(all(files_exist)):
        raise EOFError('EXITING BECAUSE OF MISSING FILES', [files[elem] for elem in range(len(files_exist)) if not files_exist[elem]])

    ds = xar.open_mfdataset(files, decode_times=False)

    return ds

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

    xsize = radius*np.absolute(np.deg2rad(dataset_in['delta_lon']))*np.cos(np.deg2rad(dataset_in['lat']))
    ysize = radius*np.absolute(np.deg2rad(dataset_in['delta_lat']))

    area_array = xsize*ysize

    dataset_in['area_array'] = (('lat','lon'), area_array.transpose('lat','lon'))
