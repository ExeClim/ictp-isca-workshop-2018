# Models of Earth using Isca

## Projects

The `earth_projects` and `planetary_projects` folder each contain example experiments for the 9 group projects. These are not meant as exhaustive experiments, but are for each group to modify as the wish.

## Running on Argo

To run a given experiment on Argo, it must be submitted to the queue. To do this:

## Analysis

Analysis is to be run on the Argo log-in node. Simple analysis scripts using `python` with the `xarray` module have been provided in the `analysis` folder:

* `analyse_single_experiment.py` reads in the data from a single experiment and makes simple plots
* `analyse_multiple_experiments.py` reads in data from 2 experiments and compares them
* `analyse_functions.py` is a collection of useful analysis functions, which you are encouraged to add things to.

If you don't want to use python, other programs are available:

* CDO - `module load cdo`
* Matlab (2011) - `module load matlab`
* Grads - `module load grads`
* ncl (5.2.1, 6.0.0, 6.3.0) - `module load ncl/6.3.0/gnu/4.4.7`
* R (2.15, 3.1.2, 3.3.1) - `module load R`
* IDL is **not available** on Argo