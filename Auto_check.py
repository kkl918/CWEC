import os, requests, datetime, requests, re
from pathlib import Path
from bs4 import BeautifulSoup

MLN2_dat_txt = Path(r'\\203.64.168.116\raw_data\107ML_RTAWAC\MLN2_AWAC\N2_WAVE-RTMC.txt')
MLN2_vol_txt = Path(r'\\203.64.168.116\raw_data\107ML_RTAWAC\MLN2_AWAC\adam-MLN2_V.TXT')

MLN5_dat_txt = Path(r'\\203.64.168.116\raw_data\107ML_RTAWAC\MLN5_AWAC\N5_WAVE-RTMC.txt')
MLN5_vol_txt = Path(r'\\203.64.168.116\raw_data\107ML_RTAWAC\MLN5_AWAC\adam-MLN5_V.TXT')

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

def parse_KHurl():
    url   = 'http://cwec.twport.com.tw/index.php'
    res   = requests.get(url)
    soup  = BeautifulSoup(res.text, 'html.parser')
    
    
    re1              = re.compile(r'電壓').search(soup.text)
    
    date             = soup.text[re1.span()[1]+1:re1.span()[1]+17].replace('\t', '').replace(' ', '')[0:10]
    time             = soup.text[re1.span()[1]+1:re1.span()[1]+17].replace('\t', '').replace(' ', '')[10:]
    re1              = re.compile(r'西防波堤測站').search(soup.text)
    target           = soup.text[re1.span()[0]:re1.span()[1]+42].replace('\t', '').replace(' ', '').replace('xa0', '')
    
    wHADCP_name      = (''.join(target.split('\n')[0].split())[:6])
    wHADCP_vol       =(''.join(target.split('\n')[0].split())[6:10])
    
    nHADCP_name      = (''.join(target.split('\n')[1].split())[:6])
    nHADCP_vol       =(''.join(target.split('\n')[1].split())[6:10])
    y                = int(date.split('-')[0])
    m                = int(date.split('-')[1])
    d                = int(date.split('-')[2])
           
    hr               = int(time.split(':')[0])
    mins             = int(time.split(':')[1])
    HADCP_time       = datetime.datetime(y, m, d, hr, mins)   
    HADCP_time_delta = (datetime.datetime.now()-HADCP_time).total_seconds()/3600
    
    if HADCP_time_delta < 12:
        webHADCP_code     = 1
        webHADCP_status   = '高雄港網頁資料傳輸正常，最後更新時間({})'.format(HADCP_time)
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
        webHADCP_code     = -1
        webHADCP_status   = '高雄港網頁資料傳輸異常，最後更新時間({})'.format(HADCP_time)
        
    HADCP_stastus         = '{}\n{}\n{}\n{}\n'.format(HADCP_time, webHADCP_status, nHADCP_status, wHADCP_status)
    
    global HADCP_detil
    HADCP_detil           = '{}\n{}\n{}\n{}\n'.format(HADCP_time, webHADCP_status, nHADCP_status, wHADCP_status)
    
    # print(HADCP_time)
    # print(webHADCP_status)
    # print(nHADCP_status)
    # print(wHADCP_status)
 
    if webHADCP_code + nHADCP_code + wHADCP_code == 3:
        HADCP_stastus = '{}:高雄港海流測站正常(北站{}v,西站{}v)。'.format(HADCP_time, nHADCP_vol, wHADCP_vol)

        
    
    # print( HADCP_stastus)
    HADCP_stastus = '高雄港海流測站:\n{}'.format(HADCP_stastus)
    return(HADCP_stastus)

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
    dat_time  = [[j.split(' ')[1].replace(',', '') ,j.split(' ')[5].replace(',', ''),  j.split(' ')[7].replace(',', '')] for j in dat_array]
    mat_time  = [i for i in vol_time if i in dat_time]

    out_array = []
    for i in vol_time:
            for j in dat_time:
                if i[1] == j[0]:
                    out_array.append('{},{},{},{},{}'.format(i[0], i[1], i[2][:4], j[1], j[2]))
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
            HADCP_status = '{} {} 資料傳輸異常，超過{}小時未回傳電壓'.format(HADCP_time, name, 12)
        return(HADCP_status)
    else:
        name = os.path.split(txt)[1]
        HADCP_status = '{} {} 資料傳輸異常，回傳數值為空'.format(data[0], name)
        return(HADCP_status)
    
def check_MLN2_data(MLN2_dat_txt, MLN2_vol_txt):
    MLN2 = parse_ML_txt(MLN2_dat_txt, MLN2_vol_txt)   
    MLN2_time = '{} {}\n'.format(MLN2.split(',')[0], MLN2.split(',')[1])
    MLN2_time = datetime.datetime(int(MLN2.split(',')[0].split('-')[0]), 
                                  int(MLN2.split(',')[0].split('-')[1]), 
                                  int(MLN2.split(',')[0].split('-')[2]),
                                  int(MLN2.split(',')[1].split(':')[0]), 
                                  int(MLN2.split(',')[1].split(':')[1]), 
                                  int(MLN2.split(',')[1].split(':')[2]))
    MLN2_time_delta = (datetime.datetime.now()-MLN2_time).total_seconds()/3600
    MLN2_vol  = MLN2.split(',')[2]
    MLN2_max  = MLN2.split(',')[3]
    MLN2_tp   = MLN2.split(',')[4]
    if float(MLN2_vol) > 11.5:
        MLN2_vol_code = 1
        MLN2_vol_txt  = "北二測站電壓({})正常。\n".format(MLN2_vol)  
        
    # -------------------------------------------------------------------------    
    
    if  float(MLN2_max) <= 0.8:
        MLN2_max_code = 1
        MLN2_max_txt  = "北二波高({})公尺測站正常。\n".format(MLN2_max)       

    elif  0.8 < float(MLN2_max) < 1.2:
        MLN2_max_code = 2
        MLN2_max_txt  = "北二測站測得波高{}公尺發出預警。\n".format(MLN2_max)
        

    else:
        MLN2_max_code = 3
        MLN2_max_txt  = "北二測站測得波高{}公尺發出警報。\n".format(MLN2_max)   
    
    # -------------------------------------------------------------------------    
       
    if  float(MLN2_tp) <= 7.3:
        MLN2_tp_code = 1
        MLN2_tp_txt  = "北二測站週期({})秒正常。\n".format(MLN2_tp)        

    elif  7.3 < float(MLN2_tp) < 8:
        MLN2_tp_code = 2
        MLN2_tp_txt  = "北二測站測得週期{}秒發出預警。\n".format(MLN2_tp)

    else:
        MLN2_tp_code = 3
        MLN2_tp_txt  = "北二測站測得週期{}秒發出警報。\n".format(MLN2_tp)   
    
    if MLN2_vol_code + MLN2_max_code + MLN2_tp_code != 3:
        # MLN2_code   = '[vol, max, tp] = {},{},{}'.format(MLN2_vol_code, MLN2_max_code, MLN2_tp_code)
        # print(MLN2_code)
        
        MLN2_sataus = '{}\n{}{}{}'.format(MLN2_time, MLN2_vol_txt, MLN2_max_txt, MLN2_tp_txt)
        
    else:
        MLN2_sataus = '{}:北二測站資料正常。'.format(MLN2_time)
    
    global MLN2_detail
    MLN2_detail = '{}\n{}{}{}'.format(MLN2_time, MLN2_vol_txt, MLN2_max_txt, MLN2_tp_txt)
    return(MLN2_time_delta, MLN2_sataus)

def check_MLN5_data(MLN5_dat_txt, MLN5_vol_txt):
    MLN5 = parse_ML_txt(MLN5_dat_txt, MLN5_vol_txt)
    MLN5_time = '{} {}\n'.format(MLN5.split(',')[0], MLN5.split(',')[1]) 
    MLN5_time = datetime.datetime(int(MLN5.split(',')[0].split('-')[0]), 
                                  int(MLN5.split(',')[0].split('-')[1]), 
                                  int(MLN5.split(',')[0].split('-')[2]),
                                  int(MLN5.split(',')[1].split(':')[0]), 
                                  int(MLN5.split(',')[1].split(':')[1]), 
                                  int(MLN5.split(',')[1].split(':')[2]))

    MLN5_time_delta = (datetime.datetime.now()-MLN5_time).total_seconds()/3600
    MLN5_vol  = MLN5.split(',')[2]
    MLN5_max  = MLN5.split(',')[3]
    MLN5_tp   = MLN5.split(',')[4]
    if float(MLN5_vol) > 11.5:
        MLN5_vol_code = 1
        MLN5_vol_txt  = "北五測站電壓({})正常。\n".format(MLN5_vol) 
        
    # -------------------------------------------------------------------------    
    
    if  float(MLN5_max) <= 0.8:
        MLN5_max_code = 1
        MLN5_max_txt  = "北五波高({})公尺測站正常。\n".format(MLN5_max)        

    elif  0.8 < float(MLN5_max) < 1.2:
        MLN5_max_code = 2
        MLN5_max_txt  = "北五測站測得波高{}公尺發出預警。\n".format(MLN5_max)   

    else:
        MLN5_max_code = 3
        MLN5_max_txt  = "北五測站測得波高{}公尺發出警報。\n".format(MLN5_max) 
    
    # -------------------------------------------------------------------------
        
    if  float(MLN5_tp) <= 6:
        MLN5_tp_code = 1
        MLN5_tp_txt  = "北五週期({})秒測站正常。\n".format(MLN5_tp)        

    elif  6 < float(MLN5_max) < 8:
        MLN5_tp_code = 2
        MLN5_tp_txt  = "北五測站測得週期{}秒發出預警。\n".format(MLN5_tp)   

    else:
        MLN5_tp_code = 3
        MLN5_tp_txt  = "北五測站測得週期{}秒發出警報。\n".format(MLN5_tp)    

    if MLN5_vol_code + MLN5_max_code + MLN5_tp_code != 3:
        MLN5_code   = '[vol, max, tp] = {},{},{}'.format(MLN5_vol_code, MLN5_max_code, MLN5_tp_code)
        # print(MLN5_code)
        
        MLN5_sataus = '{}\n{}{}{}'.format(MLN5_time, MLN5_vol_txt, MLN5_max_txt, MLN5_tp_txt)     
        
     
    else:
        MLN5_sataus = '{}:北五測站資料正常。'.format(MLN5_time)

    global MLN5_detail
    MLN5_detail = '{}\n{}{}{}'.format(MLN5_time, MLN5_vol_txt, MLN5_max_txt, MLN5_tp_txt)    

    return(MLN5_time_delta, MLN5_sataus)

def Bat_ML_check():
    [MLN2_time_delta, MLN2_sataus] = check_MLN2_data(MLN2_dat_txt, MLN2_vol_txt)
    [MLN5_time_delta, MLN5_sataus] = check_MLN5_data(MLN5_dat_txt, MLN5_vol_txt)
    
    if MLN2_time_delta > 12:
        MLN2_sataus = '北二測站超過{}小時無數據回傳\n最後回傳時間{}\n'.format(12,MLN2_time)


    if MLN5_time_delta > 12:
        MLN5_sataus = '北五測站超過{}小時無數據回傳\n最後回傳時間{}\n'.format(12,MLN5_time)   


    ML_text = '麥寮港即時波浪系統:\n\n{}\n\n{}'.format(MLN2_sataus, MLN5_sataus)
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
    
webHADCP_status = parse_KHurl()
dbHADCP_status  = Bat_check_HADCP()
ML_status       = Bat_ML_check()
realtime_status = '{}\n\n{}'.format(ML_status, webHADCP_status)



print(realtime_status)
log(print_detail())
# print(dbHADCP_status)
line_msg(realtime_status)





