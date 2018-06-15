import numpy as np
import xarray as xr


class IscaSurfaceIntegrator:
    def __init__(self, dataset, radius=6371e3):
        self._coords = dataset.coords
        self.radius = radius

    @property
    def dlat(self):
        return xr.DataArray(
            data=self._coords['latb'].diff('latb').values,
            coords=[('lat', self._coords['lat'])],
            name='dlat')

    @property
    def dlon(self):
        return xr.DataArray(
            data=self._coords['lonb'].diff('lonb').values,
            coords=[('lon', self._coords['lon'])],
            name='dlon')

    @property
    def dA(self):
        coslat = np.cos(np.deg2rad(self._coords['lat']))
        dA = np.deg2rad(self.dlat)*np.deg2rad(self.dlon)*coslat*self.radius**2
        return dA


    def __call__(self, field):
        return self.integrate(field)

    def integrate(self, field):
        return (field*self.dA).sum(('lat', 'lon'))

    def mean(self, field):
        return self(field)/self(1.)


if __name__ == '__main__':
    # an example of using the surface integrator to calculate mean surface temperature
    import os
    import matplotlib
    matplotlib.use('Agg')  # prevent matplotlib from complaining that there is no $DISPLAY attached
    import matplotlib.pyplot as plt
    from isca import GFDL_DATA

    HOME = os.environ['HOME']
    indata = os.path.join(GFDL_DATA, 'project_4_rrtm_mld_20.0/run*/atmos_monthly.nc')
    outfile = os.path.join(HOME, 'meanT.pdf')

    with xr.open_mfdataset(indata, decode_times=False) as data:
        surf_int = IscaSurfaceIntegrator(data)
        fig, ax = plt.subplots(figsize=(6,4))
        # calculate the mean temperature in the bottom level of the atmosphere
        # nearest the surface
        meanT = data.temp.sel(pfull=data.pfull.max()).pipe(surf_int.mean) - 273.15
        rollingMean = meanT.rolling(time=3).mean()

        ax.plot(meanT.time, meanT, label=r'$\bar T$')
        ax.plot(rollingMean.time, rollingMean, label=r'$\bar T$ (3 month window)')

        ax.set_xlabel('Time (days)')
        ax.set_ylabel('Near Surface Temperature (deg. C)')
        ax.legend(loc='lower right')
        fig.savefig(outfile)
        print('Mean T figure saved to {}'.format(outfile))