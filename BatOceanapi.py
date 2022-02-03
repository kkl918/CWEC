########################################
## Created on : 2021/12/17            ##
## Author     : 林佳慶(Chia-Ching Lin)##
## Target     : 批次下載資料          ##
## E-mail     : kakinglin@gail.com    ##
## Note       : 2021/12/25 正式運行   ##
########################################

import os, webbrowser, time, pathlib, datetime, subprocess, requests
from pathlib import Path

today     = datetime.datetime.today()
today_str = datetime.datetime.today().strftime("%Y%m%d")
tomon_str = datetime.datetime.today().strftime("%Y%m")
print('Script run on {}'.format(today_str))

# 測試用
# deltaday  = datetime.timedelta(days=-5)
# today     = today + deltaday
# today_str = 20220102
# print("date and time:",today_str)

# 定義基本變數
day       = today_str 
day       = '20220102'
SALT      = 'SALT.{}00'.format(day)
SST       = 'SST.{}00'.format(day)
UCURR     = 'UCURR.{}00'.format(day)
VCURR     = 'VCURR.{}00'.format(day)
WL        = 'WL.{}00'.format(day)
TWrange   = '[0:1:119][0:1:0][440:1:920][280:1:600]'
data_type = [SALT , SST, UCURR, VCURR, WL]
data_type = [UCURR, VCURR]

# 指定下載的路徑
DL_path   = Path(r'C:\Users\USER\Downloads\test')
# DL_path   = Path(r'/home/linaro/Downloads').joinpath(today_str)
# DL_path   = Path(r'/home1/cwecA/OPENDAP').joinpath(today_str)
DL_data   = [DL_path.joinpath(i+'.nc.nc4') for i in data_type]

Path.mkdir(DL_path, parents=True, exist_ok=True)

def log_write(text):
    with open(DL_path.parents[0].joinpath('cron.log'), 'a') as f:
        f.write(text)

# 給類型自動開網頁下載
def getData_web(types):
    url  = 'https://oceanapi.cwb.gov.tw/opendap/OCM/{}/00/9999/{}.nc.nc4?{}{}'.format(day, types, types.split('.')[0], TWrange)
    # print(type)
    webbrowser.open_new_tab(url)

# 給類型自動開網頁下載
def getData_wget(types, dst):
    
    url  = 'https://oceanapi.cwb.gov.tw/opendap/OCM/{}/00/9999/{}.nc.nc4?{}{}'.format(day, types, types.split('.')[0], TWrange)
    url  = 'https://oceanapi.cwb.gov.tw/opendap/OCM/{}/00/9999/{}.nc.nc4?'.format(day, types)
    print(dst)
    print('{} {} {} {} {} {}'.format("wget", "--no-proxy", "-q", url, '-O',dst))

    result = subprocess.run(["wget", "--no-proxy", "-q", url, '-O',dst], stdout=subprocess.PIPE, universal_newlines=True)
    if result.stderr != None:
        print(result.stdout)
        print(result.stderr)

# 檢查五個類型資料批次下載
def BatDownload_nc(sleep_second):
    for index, data in enumerate(DL_data):    
        
        if not data.is_file() :           
            # print(data_type[index], DL_data[index].as_posix())
            # getData_web(data_type[index])  

            getData_wget(data_type[index], DL_data[index].as_posix())
            time.sleep(sleep_second)
        else:
            file_size =data.stat().st_size
            if int(file_size)<350000000:
                getData_wget(data_type[index], DL_data[index].as_posix())  
                time.sleep(sleep_second)

# 檢查一些
def BatWrork():
    delay_min       = 0.5  # 每次批次下載延遲多久(分鐘)
    file_sate       = 0  # 下載到幾個檔案(MAX=5)
    exe_counter     = 1  # 執行計數器
    exe_counter_max = 20 # 最多跑幾次
    
    while exe_counter <= exe_counter_max:
        file_sate   = 0  # 裡面要在宣告一次，每次跑回圈時數值歸零
        print('Script execute {} times.'.format(exe_counter))
        print('Get(file path, size): ')
        
        # 計算下載了幾個
        for nc in DL_data:
            if nc.is_file():
                file_size =nc.stat().st_size
                if file_size > 350000000:      
                    file_sate += 1
                    print(nc, ', size : ' + str(file_size))
        
        # # 湊滿五個迴圈終止，否則就執行批次下載
        if file_sate < 5 :
             BatDownload_nc(2)
        else:
            break
        print('Wait {} mins for next download.'.format(delay_min))
        
        print('- - - - - - - - - - - - - - - - -\n')
        
        # # 中斷延遲時間
        time.sleep(delay_min*60)
        exe_counter += 1
    
    # 關掉瀏覽器
    # os.system("taskkill /im chrome.exe /f")
    print('[OK] Get data.')

    
    if exe_counter < 20:
        log_write('[OK] Get data {}.\n'.format(today_str))
    else:	
        log_write('[ERROR] Check data {}.\n'.format(today_str))

def main():
    URL = 'https://oceanapi.cwb.gov.tw/opendap/OCM/{}/contents.html'.format(day)
    URL_status = requests.get(URL).status_code
    print(URL)
    if URL_status  == 200:
        BatWrork()
    else:
        print('[ERROR] URL not exist, status:{}.'.format(URL_status))
    print('Script End.\n\n')

main()

# Debug
# BatDownload_nc(2)
# crontab 
# 00 18 * * * /usr/bin/python3 /home1/cwecA/OPENDAP/BatOceanapi.py 
