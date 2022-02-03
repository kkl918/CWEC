import os, shutil, datetime
from pathlib import Path


def batWRF2cwec9():
    
    tomon_str = datetime.datetime.today().strftime("%Y%m")

    WRF_folder_path = r'\\203.64.168.116\External_IN\CWB\WRF\wi_3km\NC\{}'.format(tomon_str)
    DST_path        = r'O:\loc_data\Taiwan\WINDS'


    WRF_file_parh   = [Path(WRF_folder_path).joinpath(i)      for i in os.listdir(WRF_folder_path)]  
    WRF_file_array  = [Path(WRF_folder_path).joinpath(i).name for i in os.listdir(WRF_folder_path)]  
    DST_file_array  = [i for i in os.listdir(DST_path)]

    DL_list         = [i for i in WRF_file_parh if i.name not in DST_file_array]
    
    if len(DL_list) == 0:
        print('[WRF] Nothing new in 116.')
    else:
        for nc in DL_list:
            print('[{}]\nSRC : {}\nDST : {}\n\n'.format(nc.name, nc, Path(DST_path).joinpath(nc.name)))
            shutil.copy(nc, Path(DST_path).joinpath(nc.name))
