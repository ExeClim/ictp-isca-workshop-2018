# Models of Earth using Isca

## `qflux`: Parameterising the effect of ocean heat transport

Isca does not have a dynamic ocean.  The mixed layer at the bottom of the atmosphere has a heat capacity and so can heat up and cool down in response to:
- Sensible heat flux with the atmosphere
- Cooling via latent heat of evaporation for water leaving the surface to the atmosphere
- Radiative heating from incoming solar radiation and heating/cooling from longwave emission of the surface and atmosphere above.

There is, however, no horizontal or vertical heat transport as there is in the true climate, where oceanic currents provide a method of meridional heat transport.

We can parameterise the heat transport of the ocean with an analytic form \[Merlis et al (2013)\]
$$ \nabla \cot \mathbf{F_Q} =  \frac{Q_0}{\cos\theta}\left(1 - \frac{2\theta^2}{\theta_0^2} \right) \exp{\left(-\frac{\theta^2}{\theta_0^2} \right)}, $$
moving heat from the equator to the pole at constant rate.
$Q_0$ and $\theta_0$ are tuneable parameters that control the amplitude and size of equatorial warm pool respectively.

The experiment `qflux.py` runs two instances of the Isca model, with the q-flux parameterisation on and off.  If you wish, you can change the parameter values within the Python script.

To compile the code, after loading the Isca environment, at the command line type:

`$ python qflux.py --compile`

To run the experiments for a set number of months (in this case, 24) on a set number of cores (16 is optimal for this resolution), type (or submit a batch job to the cluster)

`$ python qflux.py --up-to --run 24 -n 16`

Output from these experiments can be found in `$GFDL_DATA/qflux_{on,off}` which we can analyse with the `qflux_analysis.py` script.