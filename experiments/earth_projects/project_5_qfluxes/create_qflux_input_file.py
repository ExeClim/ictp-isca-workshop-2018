import os
import sys

from netCDF4 import Dataset
import numpy as np

from isca import GFDL_BASE

sys.path.insert(0, os.path.join(GFDL_BASE, 'src', 'extra', 'python', 'scripts'))

import gauss_grid as gg

def output_qflux_field(file_name_out, lats, lons, latbs, lonbs, qflux_field):

    nlat = lats.shape[0]
    nlon = lons.shape[0]
    nlonb= lonbs.shape[0]
    nlatb= latbs.shape[0]

    warmpool_file = Dataset(file_name_out+'.nc', 'w', format='NETCDF3_CLASSIC')
    lat = warmpool_file.createDimension('lat', nlat)
    lon = warmpool_file.createDimension('lon', nlon)

    latb = warmpool_file.createDimension('latb', nlatb)
    lonb = warmpool_file.createDimension('lonb', nlonb)

    latitudes = warmpool_file.createVariable('lat','f4',('lat',))
    longitudes = warmpool_file.createVariable('lon','f4',('lon',))

    latitudebs = warmpool_file.createVariable('latb','f4',('latb',))
    longitudebs = warmpool_file.createVariable('lonb','f4',('lonb',))

    latitudes.units = 'degrees_N'.encode('utf-8')
    latitudes.cartesian_axis = 'Y'
    latitudes.edges = 'latb'
    latitudes.long_name = 'latitude'

    longitudes.units = 'degrees_E'.encode('utf-8')
    longitudes.cartesian_axis = 'X'
    longitudes.edges = 'lonb'
    longitudes.long_name = 'longitude'

    latitudebs.units = 'degrees_N'.encode('utf-8')
    latitudebs.cartesian_axis = 'Y'
    latitudebs.long_name = 'latitude edges'

    longitudebs.units = 'degrees_E'.encode('utf-8')
    longitudebs.cartesian_axis = 'X'
    longitudebs.long_name = 'longitude edges'

    warmpool_array_netcdf = warmpool_file.createVariable('ocean_qflux','f4',('lat','lon',))

    latitudes[:] = lats
    longitudes[:] = lons

    latitudebs[:] = latbs
    longitudebs[:] = lonbs

    warmpool_array_netcdf[:] = qflux_field

    warmpool_file.close()

def create_model_grid(t_res):

    t_res_dict = {
        'T42':{'nlon':128, 'nlat':64},
        'T85':{'nlon':256, 'nlat':128},
        'T170':{'nlon':512, 'nlat':256},
    }

    nlat = t_res_dict[t_res]['nlat']
    nlon = t_res_dict[t_res]['nlon']


    lons  = np.arange(0., 360., (360./nlon))
    lats, latb_temp  = gg.gaussian_latitudes(int(nlat/2))

    delta_lon=(lons[1]-lons[0])
    if np.all((lons[1:10]-lons[0:9]) == delta_lon):
        lonb = np.zeros((len(lons)+1))

        for lonb_idx in range(len(lons)):
            lonb[lonb_idx] = lons[lonb_idx]-delta_lon / 2.
        lonb[-1] = lons[-1] + delta_lon / 2.


    latb = [latb_entry[0] for latb_entry in latb_temp]
    latb.append(latb_temp[-1][1])

    latb = np.asarray(latb)

    return lons, lats, lonb, latb

def check_global_integral_near_zero(qflux_in, lon, lat, lonb, latb):

    lonb_1 = lonb[1::]
    lonb_2 = lonb[0:-1]

    delta_lon = lonb_1 - lonb_2

    latb_1 = latb[1::]
    latb_2 = latb[0:-1]

    delta_lat = latb_1 - latb_2

    delta_lon_2d, delta_lat_2d = np.meshgrid(delta_lon, delta_lat)
    lon_2d, latb_1_2d = np.meshgrid(lon,latb_1)
    lon_2d, latb_2_2d = np.meshgrid(lon,latb_2)

    xsize = np.absolute(np.deg2rad(delta_lon_2d))*(np.sin(np.deg2rad(latb_1_2d))-np.sin(np.deg2rad(latb_2_2d)))
    ysize = 1.

    area_array = xsize*ysize

    weighted_qflux = qflux_in * area_array

    global_average = np.mean(weighted_qflux) / np.mean(area_array)

    if global_average!=0.:
        print('warning - global average of qflux field is not exactly zero, but it = ', global_average)

def merlis_scheider_qflux(lons, lats, qflux_amp, qflux_width):

    lon_2d, lat_2d = np.meshgrid(lons,lats)


    qflux_out =  - qflux_amp*(1-2.*lat_2d**2/qflux_width**2) * np.exp(- ((lat_2d)**2/(qflux_width)**2))/np.cos(np.deg2rad(lat_2d))

    return qflux_out


if __name__=="__main__":

    t_res='T42'
    file_name_out = 'merlis_schneider_30_16'

    lons, lats, lonbs, latbs = create_model_grid(t_res)
    qflux_field = merlis_scheider_qflux(lons, lats, 30., 16.)
    check_global_integral_near_zero(qflux_field, lons, lats, lonbs, latbs)
    output_qflux_field(file_name_out, lats, lons, latbs, lonbs, qflux_field)


