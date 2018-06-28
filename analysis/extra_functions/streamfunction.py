import xarray as xr


__author__='M. Cameron Rencurrel & Brian E. J. Rose'

#### Make path to own netCDF file
data='/Users/mcrencurrel/Desktop/HC_project_data/project_2_held_suarez_make_symmetric_False/HS_asym_avg.nc'

test_run=xr.open_dataset(data)

### open zonally averaged dataset using xarray and then plug into function
def overturning(run):
    import numpy as np
    

        
    mb_to_Pa = 10.
    cappa= 0.28571658640413355
    rearth= 6371220.0
    gravit = 9.80616
    # diff dummy variable to get dimensions for later
    dtheta = run.temp.diff(dim='pfull')
    
    dP = xr.DataArray(np.diff(run.pfull*mb_to_Pa),dims='pfull', coords={'pfull': dtheta.pfull})
    field = (run.vcomp * dP * np.cos(np.deg2rad(run.lat)))

    factor = 2*np.pi*rearth/gravit*1E-9
    if 'lon' in field.dims:
        field = field.mean(dim='lon')
    
    psi = np.cumsum( field, axis=field.get_axis_num('pfull'))*factor
    return psi

test=overturning(test_run)
