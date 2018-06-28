import xarray as xar
import os
import matplotlib.pyplot as plt
import numpy as np
import pdb
import time
import math

__author__='Neil Lewis'


def open_experiment(exp_folder_name, start_file, end_file, file_name):

    base_dir = os.environ['GFDL_DATA']

    folder_list = ['run%04d' % m for m in range(start_file, end_file+1)] 
    files = [base_dir  + exp_folder_name+ '/' + folder_list[i] + '/' + file_name for i in range(len(folder_list))]

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


def calculate_static_energies(ds_in, cp=1005., g=9.8, Lv=2.5e6, moist=True):


    dse = cp * ds_in['temp'].values + g * ds_in['height'].values
    if moist:
        le  = Lv * ds_in['sphum'].values
        mse = dse + le

    dims = ds_in['temp'].dims

    ds_in['dse'] = (dims, dse)
    ds_in['dse'].attrs['units'] = 'J'
    if moist:
        ds_in['mse'] = (dims, mse)
        ds_in['mse'].attrs['units'] = 'J'
        ds_in['le']  = (dims, le)
        ds_in['le'].attrs['units'] = 'J'

    for se in ['dse','mse','le']:
        if moist != True:
            if se == 'mse' or se == 'le':
                break
        ds_in[se+'_vflux'] = (dims, ds_in[se].values * ds_in.vcomp.values)
        ds_in[se+'_vflux'].attrs['units'] = ['W m']


def mass_streamfunction(ds_in, earth_radius=6371000., grav=9.81):

    # unpack zonal mean meridional wind and zonal mean pressure 
    vcomp_zm = ds_in.vcomp.mean(('lon')).values
    pres_full_zm = ds_in.pres_full.mean(('lon')).values

    # compute integral component of psi at all pressure levels 
    KMAX = len(ds_in.pfull.values)
    psi = np.zeros_like(vcomp_zm)
    for k in range(0, KMAX):
        psi[:, KMAX-1-k, :] = np.trapz(vcomp_zm[:,KMAX-1-k:,:], x=pres_full_zm[:,KMAX-1-k:,:], axis=1)

    # multiply by pre-factor
    lat2 = np.broadcast_to(ds_in.lat.values, (KMAX, len(ds_in.lat.values)))
    psi = psi * 2 * np.pi * earth_radius / grav * np.cos(lat2 * np.pi / 180.)
    psi = -1 * psi / 1e+09

    # add to ds_in
    dims = tuple(x for x in ds_in.vcomp.dims if x!='lon')
    ds_in['psi'] = (dims, psi)
    ds_in.psi.attrs['units'] = '10^9 kg s^-1'


def roundup(x):
    return int(math.ceil(x / 10.0)) * 10

def rounddown(x):
    return int(math.floor(x / 10.0)) * 10
    

    

    
    

    
