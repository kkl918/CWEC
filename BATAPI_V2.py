##################################################################################
## Created on : 2021/12/17                                                      ##
## Author     : Chia-Ching Lin                                                  ##
## Target     : Batch Download Data                                             ##
## E-mail     : kakinglin@gail.com                                              ##
##                                                                              ##
## LOG        : /home1/cwecA/OPENDAP/cron.log                                   ##
## crontab    : 00 18 * * * /usr/bin/python3 /home1/cwecA/OPENDAP/BATAPI.py     ##
## Note       : 2021/12/25 offical release,2022/01/02 due to wget was baned ->V2##                           ##
##################################################################################

import os, webbrowser, time, pathlib, datetime, subprocess, requests, shutil
from pathlib import Path
print('\n\n*************************************************************************\n')

today     = datetime.datetime.today()
today_str = datetime.datetime.today().strftime("%Y%m%d")

# TEST
today_str = '20220122'


def init(DDD):
    global home_path 
    global day                  
    global UCURR             
    global VCURR             
    global data_type         
    global TWrange           
    global len_type          
    global Browser_DL_path           
    global Browser_DL_data 
    global wget_DL_path           
    global wget_DL_data           
    global correct_file_size 
    global url


    # 定義基本變數
    # home_path = r'/home/cwec9/Downloads'
    home_path = r'/home1/cwecA/Download/'
    day       = today_str 
    UCURR     = 'UCURR'
    VCURR     = 'VCURR'
    data_type = [UCURR, VCURR]                           
    TWrange   = '[0:1:119][0:1:0][440:1:920][280:1:600]' #定義範圍
    len_type  = len(data_type) 
    
    correct_file_size = 74135850

    Browser_DL_path   = Path(home_path)
    Browser_DL_data   = [Browser_DL_path.joinpath(i+'.{}00.nc.nc4'.format(day)) for i in data_type]

    wget_DL_path   = Path(home_path).joinpath('OPENDAP', day)                                      # 指定下載的路徑
    wget_DL_data   = [wget_DL_path.joinpath(i+'.{}.nc.nc4'.format(day)) for i in data_type]
    # Path.mkdir(wget_DL_path, parents=True, exist_ok=True)  
    

def log_write(text):
    with open(Path(home_path).joinpath('cron.log'), 'a') as f:
        f.write(text)

# 給類型自動開網頁下載，舊版不採用
def getData_web(types):
    # url  = 'https://oceanapi.cwb.gov.tw/opendap/OCM/{}/00/9999/{}.nc.nc4?{}%5B0:1:119%5D%5B0:1:0%5D%5B0:1:1160%5D%5B0:1:640%5D'.format(day, types, types.split('.')[0])
    url  = 'https://oceanapi.cwb.gov.tw/opendap/OCM/{}/00/9999/{}.{}00.nc.nc4?{}{}'.format(day, types, day, types, TWrange)
    print(url)
    webbrowser.open_new_tab(url)
    # print(type)

# 給類型以及位置WGET下載
def getData_wget(types, dst):
    DL_path   = Path(home_path).joinpath('OPENDAP', day)                                      # 指定下載的路徑
    DL_data   = [DL_path.joinpath(i+'.{}.nc.nc4'.format(day)) for i in data_type]
    Path.mkdir(DL_path, parents=True, exist_ok=True)     
    url  = 'https://oceanapi.cwb.gov.tw/opendap/OCM/{}/00/9999/{}.{}00.nc.nc4?{}{}'.format(day, types, day, types, TWrange)
    print(url)
    # print('{} {} {} {} {} {}'.format("wget", "--no-proxy", "-q", url, '-O',dst))

    result = subprocess.run(["wget", "--no-proxy", "-q", url, '-O',dst], stdout=subprocess.PIPE, universal_newlines=True)
    if result.stderr != None:
        print(result.stdout)
        print(result.stderr)

# 檢查len_type個類型資料批次下載
def BatDownload_by_wget():

    
    for index, data in enumerate(DL_data):    
        
        if not data.is_file() :           
            # print(data_type[index], DL_data[index].as_posix()) 
            
            getData_wget(data_type[index], DL_data[index].as_posix())
            
        else:
            file_size = data.stat().st_size
            # print('Current File Size : '+str(file_size))
            if int(file_size)<correct_file_size:
                
                getData_wget(data_type[index], DL_data[index].as_posix())  
        time.sleep(2)
        
        
def BatDownload_by_browser():

    for index, data in enumerate(Browser_DL_data): 

        print(data, data.is_file())
        if not data.is_file() : 
            getData_web(data_type[index])
        else:
            file_size = data.stat().st_size
            print("\n{}/{}\n".format(file_size, correct_file_size))
            if int(file_size)<correct_file_size:    
                os.remove(data_type[index])
                getData_web(data_type[index])
                    
            elif int(file_size) == correct_file_size:
                os.system("pkill -f firefox")
        time.sleep(2)
        
def line_msg(text):
    url     = "https://notify-api.line.me/api/notify"
    token   = "ITtPUaLkwQBHkA3o9hgvLfH9vwfMJPnOYCY0vKpP4XN"
    headers = {"Authorization" : "Bearer "+ token}

    message = "Check OCM nc files by cwecA@cwec115, {}: {}\n".format(today_str, text)

    payload = {"message" : message}
    r = requests.post(url,headers=headers,params=payload)

def mergeBYday_wget(day):
    U    = r'{}/{}/UCURR.{}.nc.nc4'            .format(home_path, day, day)
    V    = r'{}/{}/VCURR.{}.nc.nc4'            .format(home_path, day, day)
    fn   = r'{}/{}/temp{}.nc'                  .format(home_path, day, day)
    dump = r'{}/{}/dump.nc'                    .format(home_path, day, day)
    out  = r'{}/{}/OCMweb{}.nc'                .format(home_path, day, day)
     
    mon  = r'/mnt/CWEC2NAS/External_IN/CWB/OCM/NC/{}'.format(day[0:6])
    nas  = r'/mnt/CWEC2NAS/External_IN/CWB/OCM/NC/{}/OCMweb{}.nc'.format(day[0:6], day)


    # MonthFolder = Path(mon)
    # Path.mkdir(MonthFolder, parents=True, exist_ok=True)

    if os.path.isfile(U) and os.path.isfile(U):
        # print(U, V, fn)
        subprocess.run(["ncks", "-A", U, fn], stdout=subprocess.PIPE, universal_newlines=True)
        subprocess.run(["ncks", "-A", V, fn], stdout=subprocess.PIPE, universal_newlines=True)
        subprocess.run(['ncrename', '-h', '-O', '-v', 'UCURR,water_u', fn], stdout=subprocess.PIPE, universal_newlines=True)
        subprocess.run(['ncrename', '-h', '-O', '-v', 'VCURR,water_v', fn], stdout=subprocess.PIPE, universal_newlines=True)
        subprocess.call('{} {} {} {}'.format('ncdump', fn, '>', dump), shell=True)
        subprocess.run(['sed', '-i', "s/int time/double time/g", dump], stdout=subprocess.PIPE, universal_newlines=True)
        subprocess.call('{} {} {} {}'.format('ncgen', dump, "-o", out), shell=True)
        if os.path.isfile(out):
            if not os.path.isdir(mon):
                os.mkdir(mon)
        shutil.copy(out, nas)
        print('[Done] {}'.format(day))
        # if result.stderr != None:
            # print(result.stdout)
            # print(result.stderr)
    else:
        print('[merge error] File not exist.\n{}\n{}\n'.format(U, V))
        
def mergeBYday_browser(day):
    U    = r'{}/UCURR.{}00.nc.nc4'            .format(home_path, day)
    V    = r'{}/VCURR.{}00.nc.nc4'            .format(home_path, day)
    fn   = r'{}/temp{}.nc'                  .format(home_path, day)
    dump = r'{}/dump.nc'                    .format(home_path, day)
    out  = r'{}/OCMweb{}.nc'                .format(home_path, day)
     
    mon  = r'/mnt/CWEC2NAS/External_IN/CWB/OCM/NC/{}'.format(day[0:6])
    nas  = r'/mnt/CWEC2NAS/External_IN/CWB/OCM/NC/{}/OCMweb{}.nc'.format(day[0:6], day)


    # MonthFolder = Path(mon)
    # Path.mkdir(MonthFolder, parents=True, exist_ok=True)

    if os.path.isfile(U) and os.path.isfile(U):
        # print(U, V, fn)
        subprocess.run(["ncks", "-A", U, fn], stdout=subprocess.PIPE, universal_newlines=True)
        subprocess.run(["ncks", "-A", V, fn], stdout=subprocess.PIPE, universal_newlines=True)
        subprocess.run(['ncrename', '-h', '-O', '-v', 'UCURR,water_u', fn], stdout=subprocess.PIPE, universal_newlines=True)
        subprocess.run(['ncrename', '-h', '-O', '-v', 'VCURR,water_v', fn], stdout=subprocess.PIPE, universal_newlines=True)
        subprocess.call('{} {} {} {}'.format('ncdump', fn, '>', dump), shell=True)
        subprocess.run(['sed', '-i', "s/int time/double time/g", dump], stdout=subprocess.PIPE, universal_newlines=True)
        subprocess.call('{} {} {} {}'.format('ncgen', dump, "-o", out), shell=True)
        print('{} {} {} {}'.format('ncgen', dump, "-o", out))
        if os.path.isfile(out):
            if not os.path.isdir(mon):
                os.mkdir(mon)
        shutil.copy(out, nas)
        print('[Done] {}'.format(day))
        # if result.stderr != None:
            # print(result.stdout)
            # print(result.stderr)
    else:
        print('[merge error] File not exist.\n{}\n{}\n'.format(U, V))        

def BatWrork():
    delay_min       = 0.5  # 每次批次下載延遲多久(分鐘)
    file_sate       = 0    # 下載到幾個檔案(MAX=5)
    exe_counter     = 1    # 執行計數器
    exe_counter_max = 20   # 最多跑幾次
    
    while exe_counter <= exe_counter_max:
        file_sate   = 0  # 裡面要在宣告一次，每次跑回圈時數值歸零
        print('Script execute {} times.'.format(exe_counter))
        print('Get(file path, size): ')
        
        # 計算下載了幾個，檔案大小
        for nc in Browser_DL_data:
            if nc.is_file():
                file_size =nc.stat().st_size
                if file_size >= correct_file_size:      
                    file_sate += 1
                    print(nc, ', size : ' + str(file_size))
        
        # # 湊滿len_type個迴圈終止，否則就執行批次下載
        if file_sate < len_type :
             # BatDownload_by_wget()
             BatDownload_by_browser()
        else:
            break
        print('Wait {} mins for next download.'.format(delay_min))
        
        print('- - - - - - - - - - - - - - - - -\n')
        
        # # 中斷延遲時間
        time.sleep(delay_min*60)
        exe_counter += 1
    
    # 關掉瀏覽器
    # os.system("pkill -f firefox")
    print('[OK] Get data.\n\n')

    
    if exe_counter < 20:
        log_write('[OK] Get data {}({}).\n\n'.format(today_str, exe_counter))
        # line_msg('OK')
    else:	
        log_write('[ERROR] Check data {}.\n'.format(today_str))
        line_msg('***ERROR***')
    
def DEBUG_USE():
    for i in range(1,5):
        today     = datetime.datetime.today()
        init(today)
        deltaday  = datetime.timedelta(days=-i)
        today     = today + deltaday
        today_str = today.strftime("%Y%m%d")
        day       = today_str
        print("date and time:",day)
        init(day)
        print(DL_data)
        # main()




def main():
    init(today_str)
    URL = 'https://oceanapi.cwb.gov.tw/opendap/OCM/{}/contents.html'.format(day)
    URL_status = requests.get(URL).status_code
    
    if URL_status  == 200:
        BatWrork()
        mergeBYday_browser(day)
    else:
        print('[ERROR] URL not exist, status:{}.'.format(URL_status))


main()
# DEBUG_USE2()
print('Script End.\n\n')

