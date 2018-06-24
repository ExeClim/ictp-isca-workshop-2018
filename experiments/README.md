# Models of Earth using Isca

## Projects

The `earth_projects` and `planetary_projects` folder each contain example experiments for the 9 group projects. These are not meant as exhaustive experiments, but are for each group to modify as the wish.

## Running on Argo

To run a given experiment on Argo, it **must not** be run on the log in node, but must be submitted to the job queue. To so this, use the command `sbatch` in the following way:

1. Create a python experiment file
2. Modify an existing job submission script to point to this experiment file
3. run `sbatch --reservation=grp01_4 NAME_OF_SUBMISSION_SCRIPT` on Argo
4. A file called `slurm-****.out` will then be created and updated as the script progresses.

Useful commands to check the status of jobs on Argo:

```
squeue -u `whoami`
``` 
will show the status of all jobs belonging to you (`whoami` returns your user name).

```
scontrol show jobid 5921
```
shows details about job number 5921. 

```
sinfo -p QUEUENAME
```
shows info about the nodes available in the queue named QUEUENAME (e.g. `long`)

```
scontrol show node node140
```
will show information about a specific node (e.g. node140).

```
scancel 1234
```
will cancel the pending or running job with jobid 1234.
```
quota -u `whoami`
```
will check your disk quota (20GB per account)

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
