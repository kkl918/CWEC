import datetime, os, sys, shutil, BATAPI_V3
from netCDF4 import Dataset
import numpy as np


def toady_str():
    today_str = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')
    return today_str


def date2str(t):
    day_str = datetime.datetime.strftime(t,'%Y%m%d')
    return day_str

    
# 給定一個整數(EX:10)，回傳今日起往前算10天的字串陣列
def day_plus(number):
    p_array = [None] * number
    
    today_str = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')
    # print("Today:{}".format(today_str))

    for i in range(0, number):
        var_t  =  datetime.datetime.now() + datetime.timedelta(hours=24*i)
        # print(date2str(var_t))
        p_array[i] = date2str(var_t)
    return p_array


# 給定一個整數(EX:10)，回傳今日起往回算10天的字串陣列
def day_minus(number):
    m_array = [None] * number
    
    today_str = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')
    # print("Today:{}".format(today_str))

    for i in range(0, number):
        var_t  =  datetime.datetime.now() - datetime.timedelta(hours=24*i)
        # print(date2str(var_t))
        m_array[i] = date2str(var_t)
    return m_array[1:]    

    
def ocm_time_list(n):
    NC_path_array = [None] * n
    abs_path = r'/mnt/CWEC2NAS/External_IN/CWB/OCM/NC'
    for index, i in enumerate(day_minus(n)):
        NC = "{}/{}/OCMweb{}.nc".format(abs_path, i[:-2], i)
        NC_path_array[index] = NC
        # print(NC)
    return(NC_path_array[:-1])



def check_fuction(NCs):
    check_result = {}
    for nc in NCs:
        if os.path.isfile(nc):
            lost_array = 120

            rootgrp = Dataset(nc, "r", format="NETCDF4")
            
            lat = rootgrp.variables['lat']
            lon = rootgrp.variables['lon']

            for i in range(1, 120):
                #print(i)
                u = rootgrp.variables['water_u'][i][0]
                v = rootgrp.variables['water_v'][i][0]    

                u_all_zeros = not np.any(u)
                v_all_zeros = not np.any(v)
                
                if u_all_zeros or v_all_zeros == 1:
                    lost_array -= 1
                    # print(i, time)
            print("[{}/120] {} ".format(lost_array, nc))            
            check_result[nc] = lost_array
        else:
            check_result[nc] = 0
            print("File not exit:{}".format(nc))
    return(check_result)
    
    
    
if __name__ == '__main__':
    
    if len(sys.argv) == 2:
        
        NCs    = ocm_time_list(int(sys.argv[1]))
        result = check_fuction(NCs)
        for file in result.keys():
            if result[file] < 120:
                ERday = file.split('/')[-1][6:14]
                print("\n[{}/120] {}\n".format(result[file], ERday))
                
                temp_folder = '/home1/cwecA/OPENDAP/{}'.format(ERday)
                print(temp_folder)
                # if os.path.isfile(file):
                    # os.remove(file)
                if os.path.isdir(temp_folder):
                    shutil.rmtree(temp_folder)
                if not os.path.isdir(temp_folder):
                    os.mkdir(temp_folder)
                
                BATAPI_V3.init(ERday)
                BATAPI_V3.one_day()

    
