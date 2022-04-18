import os, webbrowser, time, pathlib, datetime, subprocess, requests, shutil, sys, line_msg
from pathlib import Path

today_str     = datetime.datetime.today().strftime("%Y%m%d")

NC_path      = r'\\203.64.168.116\External_IN\CWB\WRF\wi_3km\NC'
NC_path      = r'/mnt/CWEC2NAS/External_IN/CWB/WRF/wi_3km/NC'
NC_path      = Path(NC_path)

nas_path     = r'\\203.64.168.116\External_IN\CWB\WRF\wi_3km\RawData'                
nas_path     = r'/mnt/CWEC2NAS/External_IN/CWB/WRF/wi_3km/RawData'                
nas_path     = Path(nas_path)

day_list     = [(datetime.datetime.today()+ datetime.timedelta(days=-i)).strftime("%Y%m%d") for i in range(0,60)]


check_list   = [NC_path.joinpath(j[:6], 'wrf' + j + i + '.nc') for i in ['00', '06', '12', '18'] for j in day_list]
check_list   = [i for i in check_list  if not i.is_file()]

argu_list    = ['/home1/cwecA/CWB/WRF/Prog/wi/wrf2nc.csh {} {} {} {}'.format(i.stem[3:7], i.stem[7:9], i.stem[9:11], i.stem[11:13]) for i in check_list]

rawdir_list  = [nas_path.joinpath(i.stem[3:7] + i.stem[7:9], i.stem[3:7] + i.stem[7:9] + i.stem[9:11] + i.stem[11:13]) for i in check_list]

keys_list    = argu_list
values_list  = rawdir_list
zip_iterator = zip(keys_list, values_list)
check_dic    = dict(zip_iterator)



# print(len(argu_list))
# print(len(check_list))
# print(len(rawdir_list))
# print(rawdir_list)
# for i in check_list:
    # if i.stem[7:9] == '01':
    # print(i, i.is_file())



# for i in check_dic.keys():
    # print(check_dic[i])

lack_file    = []
exe_list     = []

# print(check_dic.keys())

for i in check_dic.keys():   
    # print(check_dic[i])
    exe_cmd = i.split(' ')
    # print(exe_cmd)
    if os.path.isdir(check_dic[i]):
        file_amount = len(os.listdir(check_dic[i]))    
        if file_amount > 84:
            exe_list.append('[{}], {}'.format(file_amount, i[39:]))
            # print('[{}], {}'.format(file_amount, i))
            print(i)
            subprocess.call(i, shell=True)
            
            
        else:
            lack_file.append('[{}/85], {}'.format(file_amount, i[39:])) 
    else:
        lack_file.append('[00/85], {}'.format(i[39:])) 

sort_t = []
for i in lack_file:
    t = i.split(',')[1].split(' ')[2:]
    nt = datetime.datetime(int(t[0]), int(t[1]), int(t[2]), int(t[3]), 00)
    sort_t.append(nt)

sort_lack = []
for j in sorted(sort_t):
    # print(j.strftime('%Y-%m-%d %H:%M:%S'))
    sort_lack.append(j.strftime('%Y-%m-%d %H:%M:%S')[:-6])

# print(sort_lack)
    
def daily_check():

    split_line  = '\n- - - - - - - - - - -\n'
    log_text    = '[Excute on {}]\n\n'.format(today_str)

    exe_header  = '已產生WRF清單\n(氣象局FTP檔案數量,日期)'
    lack_header = '{}\n未產生WRF清單\n(氣象局FTP檔案數量,日期)'.format(split_line)
    log_text   += exe_header + '\n' + lack_header + '\n'
    # print(exe_header)
    for i in exe_list:
        log_text += i+'\n'
        # print(i)

    # print(lack_header)
    for i in lack_file:
        log_text += i+'\n'
        # print(i)
    # print(log_text)
        
    print(log_text)

def week_check():
    split_line  = '\n- - - - - - - - - - -\n'
    log_text    = '[每周檢查WRF風場]\n(檢查時間{})'.format(today_str)

    lack_header = '{}未產生WRF清單\n(氣象局FTP檔案數量,日期)'.format(split_line)
    log_text   += lack_header + '\n'

    # for i in lack_file:
    for i in sort_lack:
        log_text += i+'\n'

        
    log_text += '未滿85無法產生風場，詳請聯繫資料提供者氣象局。'
    print(log_text)
    return(log_text)

if len(sys.argv) == 1:
    print('daily_check')
    daily_check()
    week_check()
else:
    pass
 #   if sys.argv[1] == '-week_check':
#        line_msg.auto_check(week_check())
        
