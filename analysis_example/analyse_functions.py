import xarray as xar
import os
import matplotlib.pyplot as plt

def open_experiment(exp_folder_name, start_file, end_file, file_name):

    base_dir = os.environ['GFDL_DATA']

    folder_list = ['run%04d' % m for m in range(start_file, end_file+1)] 
    files = [base_dir + '/' + exp_folder_name+ '/' + folder_list[i] + '/' + file_name for i in range(len(folder_list))]

    files_exist=[os.path.isfile(s) for s in files]

    if not(all(files_exist)):
        raise EOFError('EXITING BECAUSE OF MISSING FILES', [files[elem] for elem in range(len(files_exist)) if not files_exist[elem]])

    ds = xar.open_mfdataset(files, decode_times=False)

    return ds


