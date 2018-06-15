#!/bin/bash
#PBS -N held_suarez_test_case
#PBS -l nodes=1:ppn=8
### Declare job non-rerunable
#PBS -r n
### resource limits: amount of memory and CPU time ([[h:]m:]s).
####PBS -l mem=850mb
#PBS -l walltime=0:60:00
### send me email when job begins, ends and fails
#PBS -m bea
#PBS -M jp492@exeter.ac.uk
### Queue name (default, ib, ...)
#PBS -q short
#############
HOME=$PBS_O_HOME
##export PATH=/usr/bin:$PATH
###env
source /etc/profile.d/modules.sh
export GFDL_ENV=ictp-argo
export GFDL_WORK=$HOME/gfdl_work
export GFDL_DATA=$HOME/gfdl_data
export GFDL_BASE=$HOME/isca
cd $HOME/isca
echo \"Working directory is $PBS_O_WORKDIR\"
##cd $PBS_O_WORKDIR
module load intel/2017
export PATH=/opt/ESMF/7.0.2/intel/2017/bin:$PATH
export LD_LIBRARY_PATH=/opt/ESMF/7.0.2/intel/2017/lib:$LD_LIBRARY_PATH
module load python
source $HOME/envs/isca2/bin/activate 
echo Running on host `hostname`
echo Time is `date`
echo Directory is `pwd`
cd $HOME/isca/exp/test_cases/held_suarez
python held_suarez_test_case.py --up-to --run 3 --num-cores 8 --log-file hs_job.log
