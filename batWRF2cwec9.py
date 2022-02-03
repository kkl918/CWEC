import os, shutil, socket, datetime
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

def remove_old_wind():
    path            = r'O:\loc_data\Taiwan\WINDS'
    tomon_str       = datetime.datetime.today().strftime("%Y%m")
    tomon_minus1    = tomon_str[:4]
    # print(tomon_minus1+str(int(tomon_minus1[4:])-1))
    print(tomon_minus1+str(int(tomon_str[3:])-1))
    WRF_folder_path = [Path(path).joinpath(i).name for i in os.listdir(path) if i.endswith('nc') and i[3:9]==tomon_str] 
    # print(WRF_folder_path)

batWRF2cwec9()
# remove_old_wind()
os.system('pause')

