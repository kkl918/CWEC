import os, requests, datetime, requests, re, sys
from pathlib import Path
from bs4 import BeautifulSoup

MLN2_dat_txt = Path(r'\\203.64.168.116\raw_data\107ML_RTAWAC\MLN2_AWAC\N2_WAVE-RTMC.txt')
MLN2_vol_txt = Path(r'\\203.64.168.116\raw_data\107ML_RTAWAC\MLN2_AWAC\adam-MLN2_V.TXT')

MLN5_dat_txt = Path(r'\\203.64.168.116\raw_data\107ML_RTAWAC\MLN5_AWAC\N5_WAVE-RTMC.txt')
MLN5_vol_txt = Path(r'\\203.64.168.116\raw_data\107ML_RTAWAC\MLN5_AWAC\adam-MLN5_V.TXT')

ML_URL       = 'http://203.64.168.5/index.html' 
# ML_URL       = 'https://www.google.com.tw' 

HADCP_C1_txt = r'\\203.64.168.116\raw_data\108KH_TWPORT\HADCP-C1\2201_HADCP_KH-C1_SD.txt'
HADCP_C2_txt = r'\\203.64.168.116\raw_data\108KH_TWPORT\HADCP-C2\2201_HADCP_KH-C2_SD.txt'
KH_NS_txt    = r'\\203.64.168.116\raw_data\108KH_TWPORT\HADCP-NS\2201_HADCP_KH-NS_SD.txt'
KH_NW_txt    = r'\\203.64.168.116\raw_data\108KH_TWPORT\HADCP-NW\2201_HADCP_KH-NW_SD.txt'
KH_WH_txt    = r'\\203.64.168.116\raw_data\108KH_TWPORT\HADCP-W\2201_HADCP_KH-W_SD.txt'
KH_array     = [HADCP_C1_txt, HADCP_C2_txt, KH_NS_txt, KH_NW_txt, KH_WH_txt]

# DEBUG
# MLN2_dat_txt = Path(r'C:\Users\USER\Desktop\N2_WAVE-RTMC.txt')
# MLN2_vol_txt = Path(r'C:\Users\USER\Desktop\adam-MLN2_V.TXT')

# MLN5_dat_txt = Path(r'C:\Users\USER\Desktop\N5_WAVE-RTMC.txt')
# MLN5_vol_txt = Path(r'C:\Users\USER\Desktop\adam-MLN5_V.TXT')

def parse_KHurl_station():
    url   = 'http://cwec.twport.com.tw/index.php'
    
    try:
        r    = requests.head(ML_URL)
        code = r.status_code
        if code == 200:        
            res   = requests.get(url)
            soup  = BeautifulSoup(res.text, 'html.parser')


            content_array = [i for i in soup.text.split('\n') if i != '']

            ne = [[i, j] for i, j in enumerate(content_array) if j == '北堤東面']
            ns = [[i, j] for i, j in enumerate(content_array) if j == '北堤南面']
            ww = [[i, j] for i, j in enumerate(content_array) if j == '西堤']

            ne_status = [content_array[ne[0][0]+0], content_array[ne[0][0]+1].replace(' ',''), content_array[ne[0][0]+4].replace(' ','')]
            ns_status = [content_array[ns[0][0]+0], content_array[ns[0][0]+1].replace(' ',''), content_array[ns[0][0]+4].replace(' ','')]
            ww_status = [content_array[ww[0][0]+0], content_array[ww[0][0]+1].replace(' ',''), content_array[ww[0][0]+4].replace(' ','')]

            ne_time_list = [ int(i) for i in ne_status[1].split('-') + ne_status[2].split(':')]
            ns_time_list = [ int(i) for i in ns_status[1].split('-') + ns_status[2].split(':')]
            ww_time_list = [ int(i) for i in ww_status[1].split('-') + ww_status[2].split(':')]

            # print(ne_status, ne_status[1].split('-')+ ne_status[2].split(':'))
            # print(ns_status, ns_status[1].split('-')+ ns_status[2].split(':'))
            # print(ww_status, ww_status[1].split('-')+ ww_status[2].split(':'))


            ne_time  = datetime.datetime(ne_time_list[0], ne_time_list[1], ne_time_list[2], ne_time_list[3])
            ns_time  = datetime.datetime(ns_time_list[0], ns_time_list[1], ns_time_list[2], ns_time_list[3])
            ww_time  = datetime.datetime(ww_time_list[0], ww_time_list[1], ww_time_list[2], ww_time_list[3])

            ne_delta = (datetime.datetime.now()-ne_time).total_seconds()/3600
            ns_delta = (datetime.datetime.now()-ns_time).total_seconds()/3600
            ww_delta = (datetime.datetime.now()-ww_time).total_seconds()/3600

            ne_status.append(str(ne_delta)[:4])
            ns_status.append(str(ns_delta)[:4])
            ww_status.append(str(ww_delta)[:4])

            if float(ne_status[3]) < 12:
                # print('[OK] {}回傳正常({},{})'.format(ne_status[0], ne_status[1], ne_status[2]))
                ne_ = '{}資料回傳正常({},{})'.format(ne_status[0], ne_status[1], ne_status[2])
            else:
                # print('[ERROR] {}回傳異常({},{})'.format(ne_status[0], ne_status[1], ne_status[2]))
                ne_ = '{}資料回傳異常({},{})'.format(ne_status[0], ne_status[1], ne_status[2])
                
            if float(ns_status[3]) < 12:
                # print('[OK] {}回傳正常({},{})'.format(ns_status[0], ns_status[1], ns_status[2]))
                ns_ = '{}資料回傳正常({},{})'.format(ns_status[0], ns_status[1], ns_status[2])
            else:
                # print('[ERROR] {}回傳異常({},{})'.format(ns_status[0], ns_status[1], ns_status[2]))
                ns_ = '{}資料回傳異常({},{})'.format(ns_status[0], ns_status[1], ns_status[2])

            if float(ww_status[3]) < 12:
                # print('[OK] {}回傳正常({},{})'.format(ww_status[0], ww_status[1], ww_status[2]))
                ww_ = '{}資料回傳正常({},{})'.format(ww_status[0], ww_status[1], ww_status[2])
            else:
                # print('[ERROR] {}回傳異常({},{})'.format(ww_status[0], ww_status[1], ww_status[2]))
                ww_ = '{}資料回傳異常({},{})'.format(ww_status[0], ww_status[1], ww_status[2])

            return('\n\n{}\n\n{}\n\n{}\n\n'.format(ne_, ns_, ww_))
    
    except requests.ConnectionError:
        return('\n\n{}\n網頁異常\n\n'.format(url))

def parse_KHurl():
    # 這裡處理電壓供應模組
    url   = 'http://cwec.twport.com.tw/index.php'

    try:
        r    = requests.head(ML_URL)
        code = r.status_code
        if code == 200:   
            res   = requests.get(url)
            soup  = BeautifulSoup(res.text, 'html.parser')
              
            re1              = re.compile(r'電壓').search(soup.text)
            
            date             = soup.text[re1.span()[1]+1:re1.span()[1]+17].replace('\t', '').replace(' ', '')[0:10]
            time             = soup.text[re1.span()[1]+1:re1.span()[1]+17].replace('\t', '').replace(' ', '')[10:]
            re1              = re.compile(r'西防波堤測站').search(soup.text)
            target           = soup.text[re1.span()[0]:re1.span()[1]+42].replace('\t', '').replace(' ', '').replace('xa0', '')
            
            wHADCP_name      = (''.join(target.split('\n')[0].split())[:6])
            wHADCP_vol       = (''.join(target.split('\n')[0].split())[6:10])
            
            nHADCP_name      = (''.join(target.split('\n')[1].split())[:6])
            nHADCP_vol       = (''.join(target.split('\n')[1].split())[6:10])
            y                = int(date.split('-')[0])
            m                = int(date.split('-')[1])
            d                = int(date.split('-')[2])
                   
            hr               = int(time.split(':')[0])
            mins             = int(time.split(':')[1])
            HADCP_time       = datetime.datetime(y, m, d, hr, mins)   
            HADCP_time_delta = (datetime.datetime.now()-HADCP_time).total_seconds()/3600

            if HADCP_time_delta < 12:
                webHADCP_code     = 1
                webHADCP_status   = '高雄港網頁資料傳輸正常'
                if float(wHADCP_vol) < 11.5:
                    wHADCP_code   = -1
                    wHADCP_status = '{}電壓異常({})'.format(nHADCP_name, wHADCP_vol)
                    
                else:
                    wHADCP_code   = 1
                    wHADCP_status = '{}電壓正常({})'.format(wHADCP_name, wHADCP_vol)
                    
                if float(wHADCP_vol) < 11.5:   
                    nHADCP_code   = -1
                    nHADCP_status = '{}電壓異常({})'.format(nHADCP_name, nHADCP_vol)  
                else:
                    nHADCP_code   = 1
                    nHADCP_status = '{}電壓正常({})'.format(nHADCP_name, nHADCP_vol)
                    
            else:
                nHADCP_code       = -1
                nHADCP_status     = '{}最後一次回傳電壓({})'.format(nHADCP_name, nHADCP_vol)
                
                wHADCP_code       = -1
                wHADCP_status     = '{}最後一次回傳電壓({})'.format(wHADCP_name, wHADCP_vol)
                 
                webHADCP_code     = -1
                webHADCP_status   = '[***高雄港網頁電壓回傳異常***]，目前超過12小時未回傳'
                
            HADCP_stastus         = '\n\n網頁最後更新時間:{}\n\n{}\n\n{}\n\n{}\n\n{}\n'.format(HADCP_time, webHADCP_status, nHADCP_status, wHADCP_status, 'http://cwec.twport.com.tw/')
            
            global HADCP_detil
            HADCP_detil           = '{}\n\n{}\n\n{}\n\n{}\n'.format(HADCP_time, webHADCP_status, nHADCP_status, wHADCP_status)
            
            # print(HADCP_time)
            # print(webHADCP_status)
            # print(nHADCP_status)
            # print(wHADCP_status)
         
            if webHADCP_code + nHADCP_code + wHADCP_code == 3:
                HADCP_stastus = '電壓供應模組:正常({})\n\n北站電壓{}v,西站電壓{}v。'.format(HADCP_time, nHADCP_vol, wHADCP_vol)
            # print( HADCP_stastus)
            
            HADCP_stastus = '高雄港海流測站:\n\n{}{}'.format(HADCP_stastus, parse_KHurl_station())
            return(HADCP_stastus)
    except requests.ConnectionError:
        HADCP_detil = '\n\n{}\n***高雄港網頁異常***\n\n'.format(url)
        return(HADCP_detil)
        
def parse_KH_txt(txt):
    with open (txt, 'r', encoding='utf8') as f:
        vol_array = f.readlines()[-50:-1]
        # print(vol_array )
        if len(vol_array) > 0:
            # print([vol_array[-1].split(',')[0], vol_array[-1].split(',')[-1][:-1]])
            return([vol_array[-1].split(',')[0], vol_array[-1].split(',')[-1][:-1]])
        else:
            # print(['0000-01-01 00:00:00', '-1'])
            return(['0000-00-00 00:00:00', -1])
            
def parse_KH_txt_debug():        
    C1 = parse_KH_txt(HADCP_C1_txt)
    C2 = parse_KH_txt(HADCP_C2_txt)
    NS = parse_KH_txt(KH_NS_txt)
    NW = parse_KH_txt(KH_NW_txt)
    W  = parse_KH_txt(KH_WH )


    print('C1',C1[0], C1[1])
    print('C2',C2[0], C2[1])
    print('NS',NS[0], NS[1])
    print('NW',NW[0], NW[1])
    print('WH',WH[0], WH[1])
    
def parse_ML_txt(dat_txt, vol_txt):
    
    with open (vol_txt, 'r', encoding='utf8') as f:
        vol_array = f.readlines()[-50:-1]
        
    with open (dat_txt, 'r', encoding='utf8') as f:
        dat_array = f.readlines()[-50:-1]
        
    vol_time  = [i.replace(',',' ').replace('\n', '').split(' ')      for i in vol_array]
    dat_time  = [[j.split(' ')[0].replace(',', '') , j.split(' ')[1].replace(',', '') , j.split(' ')[5].replace(',', ''),  j.split(' ')[7].replace(',', '')] for j in dat_array]
    mat_time  = [i for i in vol_time if i in dat_time]

    out_array = []
    for i in vol_time:
            for j in dat_time:
                
                if i[0] == j[0] and i[1] == j[1]:
                    out_array.append('{},{},{},{},{}'.format(i[0], i[1], i[2][:4], j[2], j[3]))
    # print(dat_time)
    # print(vol_time)
    # print(out_array[-3:])
    if len(out_array) == 0:
        # return('2000-01-01,00:00:00,-1,-1,-1')
        error_out = '{},{},{},{},{}'.format(dat_time[-1][0], dat_time[-1][1], vol_time[2][:4][2], dat_time[-1][2], dat_time[-1][3])

        return(error_out)
        
    else:
        # print(out_array[-1])
        return(out_array[-1])
    
    
    
def line_msg(text): 
    url     = "https://notify-api.line.me/api/notify"
    token   = "FGKqZNLaKj5Wjr9cpvHHkgs98Yi5c5wYlqtNEnQYiyj"
    headers = {"Authorization" : "Bearer "+ token}

    message = "\n{}".format(text)

    payload = {"message" : message}
    r = requests.post(url,headers=headers,params=payload)
    print('LineBot msg.')

def chech_HADCP(txt):
    data = parse_KH_txt(txt)
    name = os.path.split(txt)[1][11:-7]
    # print(data)
    if data[1] != -1:
        # print(data[0], data[1])
        y    = int(data[0].split(' ')[0].split('-')[0])
        m    = int(data[0].split(' ')[0].split('-')[1])
        d    = int(data[0].split(' ')[0].split('-')[2])
        hrs  = int(data[0].split(' ')[1].split(':')[0])
        mins = int(data[0].split(' ')[1].split(':')[1])
        sec  = int(data[0].split(' ')[1].split(':')[2])

        HADCP_voltahe    = float(data[1])
        HADCP_time       = datetime.datetime(y, m, d, hrs, mins ,sec)
        HADCP_time_delta = (datetime.datetime.now()-HADCP_time).total_seconds()/3600
        if HADCP_time_delta < 12:
            if HADCP_voltahe < 11.5:
                HADCP_status = '{} {} 電壓異常({})'.format(                  HADCP_time, name, str(HADCP_voltahe))
            else:    
                HADCP_status = '{} {} 電壓正常({})'.format(                  HADCP_time, name, str(HADCP_voltahe))
        else:
            HADCP_status = '{} {} 資料傳輸異常***超過{}小時未回傳電壓***'.format(HADCP_time, name, 12)
        return(HADCP_status)
    else:
        name = os.path.split(txt)[1]
        HADCP_status = '{} {} 資料傳輸異常，回傳數值為空'.format(data[0], name)
        return(HADCP_status)
    
def check_MLN2_data(MLN2_dat_txt, MLN2_vol_txt, name):
    MLN2      = parse_ML_txt(MLN2_dat_txt, MLN2_vol_txt)   
    # print(MLN2)
    MLN2_time = '{} {}\n'.format(MLN2.split(',')[0], MLN2.split(',')[1])
    MLN2_time = datetime.datetime(int(MLN2.split(',')[0].split('-')[0]), 
                                  int(MLN2.split(',')[0].split('-')[1]), 
                                  int(MLN2.split(',')[0].split('-')[2]),
                                  int(MLN2.split(',')[1].split(':')[0]), 
                                  int(MLN2.split(',')[1].split(':')[1]), 
                                  int(MLN2.split(',')[1].split(':')[2]))
    MLN2_time_delta = (datetime.datetime.now()-MLN2_time).total_seconds()/3600
    # print(MLN2)
    MLN2_vol  = MLN2.split(',')[2]
    MLN2_max  = MLN2.split(',')[3]
    MLN2_tp   = MLN2.split(',')[4]
    
    if float(MLN2_vol) > 11.5:
        MLN2_vol_code = 1
        MLN2_vol_txt  = "{}測站電壓({})正常。\n".format(name, MLN2_vol)
    else:
        MLN2_vol_code = 2
        MLN2_vol_txt  = "[***異常***]{}測站電壓({})。\n".format(name,MLN2_vol)        
    # -------------------------------------------------------------------------    
    
    if  float(MLN2_max) <= 0.8:
        MLN2_max_code = 1
        MLN2_max_txt  = "{}波高({})公尺測站正常。\n".format(name, MLN2_max)       

    elif  0.8 < float(MLN2_max) < 1.2:
        MLN2_max_code = 2
        MLN2_max_txt  = "{}測站測得波高{}公尺發出預警。\n".format(name, MLN2_max)
        

    else:
        MLN2_max_code = 3
        MLN2_max_txt  = "{}測站測得波高{}公尺發出警報。\n".format(name, MLN2_max)   
    
    # -------------------------------------------------------------------------    
       
    if  float(MLN2_tp) <= 7.3:
        MLN2_tp_code = 1
        MLN2_tp_txt  = "{}測站週期({})秒正常。\n".format(name, MLN2_tp)        

    elif  7.3 < float(MLN2_tp) < 8:
        MLN2_tp_code = 2
        MLN2_tp_txt  = "{}測站測得週期{}秒發出預警。\n".format(name, MLN2_tp)

    else:
        MLN2_tp_code = 3
        MLN2_tp_txt  = "{}測站測得週期{}秒發出警報。\n".format(name, MLN2_tp)   
    
    if MLN2_vol_code + MLN2_max_code + MLN2_tp_code != 3:
        # MLN2_code   = '[vol, max, tp] = {},{},{}'.format(MLN2_vol_code, MLN2_max_code, MLN2_tp_code)
        # print(MLN2_code)
        
        MLN2_sataus = '{}\n{}{}{}'.format(MLN2_time, MLN2_vol_txt, MLN2_max_txt, MLN2_tp_txt)
        
    else:
        MLN2_sataus = '{}測站資料正常({})。'.format(name, MLN2_time)
    
    # global MLN2_detail
    MLN2_detail = '{}\n{}{}{}'.format(MLN2_time, MLN2_vol_txt, MLN2_max_txt, MLN2_tp_txt)
    
    return(MLN2_time_delta, MLN2_sataus, MLN2_time, MLN2_detail)

def Bat_ML_check():
    # 這裡抓RAW DATA
    global MLN2_detail
    global MLN5_detail
    [MLN2_time_delta, MLN2_sataus, MLN2_time, MLN2_detail] = check_MLN2_data(MLN2_dat_txt, MLN2_vol_txt, '北二')
    [MLN5_time_delta, MLN5_sataus, MLN5_time, MLN5_detail] = check_MLN2_data(MLN5_dat_txt, MLN5_vol_txt, '北五')
    
    
    
    if MLN2_time_delta > 12:
        MLN2_sataus = '***北二測站超過{}小時無數據回傳***\n最後回傳時間{}\n'.format(12,MLN2_time)


    if MLN5_time_delta > 12:
        MLN5_sataus = '***北五測站超過{}小時無數據回傳***\n最後回傳時間{}\n'.format(12,MLN5_time)   


    # 這裡檢查網頁
    try:
        r    = requests.head(ML_URL)
        code = r.status_code
        
        if code == 200:
            ML_URL_status = "麥寮港網頁:正常".format(code)
        else:
            ML_URL_status = "麥寮港網頁:***異常***(除錯代碼{})".format(code)
        # prints the int of the status code. Find more at httpstatusrappers.com :)
    except requests.ConnectionError:
        ML_URL_status = "麥寮港網頁:***異常***\n{}".format(ML_URL)
        # print("[麥寮港網頁異常]:{}".format(ML_URL))  
    ML_text = '麥寮港即時波浪系統:\n\n{}\n\n{}\n\n{}'.format(ML_URL_status, MLN2_sataus, MLN5_sataus)
    return(ML_text)

def Bat_check_HADCP():
    HADCP_dic = {}
    HADCP_status = '\n高雄港海流測站(資料庫回傳)\n'
    for i in KH_array:
        # print(chech_HADCP(i))
        HADCP_status += chech_HADCP(i)
        HADCP_status += '\n'
    HADCP_status += '\n'
    # print('\n')
    return(HADCP_status)   

def print_detail():
    print('\n* * * * * * * * * *\n')
    print(MLN2_detail)
    print(MLN5_detail, '\n')
    print(HADCP_detil, '\n')
    
    return('\n* * * * * * * * * *\n{}\n{}\n{}\n'.format(MLN2_detail, MLN5_detail, HADCP_detil))

def log(text):
    with open(r'C:\Users\USER\Documents\LOG\auto_check.txt', 'a', encoding='utf8') as logs:
        logs.write(text)
    
def day_check():
    webHADCP_status = parse_KHurl()
    dbHADCP_status  = Bat_check_HADCP()
    ML_status       = Bat_ML_check()
    sss             = '\n\n- - - - - - - - - 分隔線 - - - - - - - -\n\n'
    realtime_status = '{}{}{}{}'.format(ML_status, sss, webHADCP_status, dbHADCP_status)

    print(realtime_status)
    log(print_detail())
    line_msg(realtime_status)


day_check()

# if __name__ == '__main__':

    # if len(sys.argv) < 2:
        # webHADCP_status = parse_KHurl()
        # dbHADCP_status  = Bat_check_HADCP()
        # ML_status       = Bat_ML_check()
        # sss             = '\n\n- - - - - - - - - 分隔線 - - - - - - - -\n\n' 
        # realtime_status = '{}{}{}'.format(ML_status, sss,webHADCP_status)
        # print(realtime_status)
        # sys.exit()
    
    # elif sys.argv[1] == 'day':
        # day_check()

    # elif sys.argv[1] == 'hour':
        # print(sys.argv[1])

