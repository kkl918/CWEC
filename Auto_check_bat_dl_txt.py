import os, requests, datetime, requests, re, sys, time
from pathlib import Path

now          = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
month_str    = datetime.datetime.today().strftime("%Y%m")[2:]
KH_WH_txt    = r'\\203.64.168.116\raw_data\108KH_TWPORT\HADCP-W\{}_HADCP_KH-W_SD.txt'.format(month_str)

print(KH_WH_txt)

mylog = r'C:\Users\USER\Desktop\2205_HADCP_KH-W_SD_LOG.txt'

counter = 60
log     = [None] * counter

with open(mylog, 'w') as f_out:
    f_out.write(KH_WH_txt+'\n')
    
    while counter > 0:
        now    = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f_size = os.path.getsize(KH_WH_txt)
        f_out.write("檢查時間:{}, 檔案大小:{}\n".format(now,os.path.getsize(KH_WH_txt)))
        

        print("檢查時間:{}, 檔案大小:{}".format(now, f_size))
        
        time.sleep(60)
        # log[counter]   = f_size
        counter -= 1
        
# log.reverse()

