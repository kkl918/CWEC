


class CWEC:


def tool():
    import os, cv2, shutil, sys, re, matplotlib, subprocess
    from PIL import Image, ImageFont, ImageDraw 
    import matplotlib.pyplot as plt
    from pathlib import Path



def init():
    global par_path
    
    global TAG_path
    global TXT_path
    global JPG_path
    global case_name     
    global oil_type      
    global oil_amount     
    global oil_unit
    global oil_season
    global result_path
    global img_path
    global font
    global taged_path

    # print(__file__)
    par_path = os.path.dirname(__file__)
    p = [i.name for i in Path(par_path).parents]
    
    
    

    Fates         = "O:\loc_data\Taiwan\FATES"
    TXT_par       = Path(Fates)
    RAW_path      = par_path

    TAG_path      = os.path.join(par_path, 'TAGED')
    JPG_path      = os.path.join(par_path, 'TIME_OIL.png')
    result_path   = os.path.join(par_path, 'result.txt')
    case_name     = par_path.split('\\')[-1]
    
    oil_season    = case_name.split('_')[-1]
    oil_unit      = case_name.split('_')[-2]
    oil_amount    = case_name.split('_')[-3]
    oil_type      = case_name.split('_')[-4]

    # TXT_path      = os.path.join(Fates   , '{}-{}-{}-{}.txt'.format())
    TXT_name      = '{}-{}-{}.txt'.format(p[3],p[2],p[1])
    TXT_path      = TXT_par.joinpath(TXT_name)
    if not TXT_path.exists():
        print('[ERROR] File not exist : ' + str(TXT_path))
    
    if not os.path.isdir(TAG_path):
        os.mkdir(TAG_path)
        
    # print(case_name, oil_type, oil_amount)
    # print(case_name)


    ttf           = os.path.join(par_path, 'kaiu.ttf')
    font          = ImageFont.truetype(ttf, 48)

    img_path      = [os.path.join(RAW_path, i) for i in os.listdir(RAW_path) if i.endswith('jpg')]
    taged_path    = [] 


    # print(img_path)

def make_tag():
    for img in img_path:
        img_name      = img.split('\\')[-1][:-4]
        img_name_jpg  = img.split('\\')[-1]
        # print(img_name)
       
        img_year      = str(int(img_name.split('-')[-1][0:4])-1911)
        img_month     = img_name.split('-')[-1][4:6]
        img_date      = img_name.split('-')[-1][6:8]
        img_hour      = img_name.split('-')[-1][8:10]
        img_mins      = img_name.split('-')[-1][10:12]
        
        
        line_1_text   = "{}年{}月{}日 {}時{}分".format(img_year, img_month, img_date, img_hour, img_mins)
        line_2_text   = case_name.split('_')[1]
        line_3_text   = "{}，{}{}{}".format(oil_season, oil_type, oil_amount, oil_unit)
        w, h = font.getsize(line_1_text)
        line_space    = h*1.25
        
        work_img         = Image.open(img)
        init_x = 15
        init_y = 15        
        img_editable     = ImageDraw.Draw(work_img)
        img_editable.rectangle((init_x, init_y, init_x + w, init_y + h), fill='white')
        img_editable.text((init_x, init_y               ), line_1_text, (0, 0, 0), font=font)
        img_editable.text((init_x, init_y + line_space  ), line_2_text, (0, 0, 0), font=font)
        img_editable.text((init_x, init_y + 2*line_space), line_3_text, (0, 0, 0), font=font)
        
        done             = os.path.join(TAG_path, img_name_jpg)
        
        taged_path.append(done)
        work_img.save(done)

def make_video():
    video_path  = os.path.join(par_path, case_name+'.wmv')
    img_array = []
    for jpg in taged_path:
        
        shutil.copy(jpg, r'C:\Users\Public\tmp.jpg')
        
        img = cv2.imread(r'C:\Users\Public\tmp.jpg')
       
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
        os.remove(r'C:\Users\Public\tmp.jpg')
       
        

    out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'DIVX'), 3, size) 
    for i in range(len(img_array)):       
        out.write(img_array[i])
    out.release()


def oil_remain():
    # Time(hours) Surface WaterColumn Ashore Evaporated Stranded
    t_array = []
    s_array = []
    w_array = []
    a_array = []
    e_array = []

    time_stamp = 0
    
    # test only
    # path     = r'C:\Users\kk\Downloads\110OCA-LIDIA-1208-125.txt'
    # JPG_path = r'C:\Users\kk\Downloads\test.png'
    path  = TXT_path
    font = {'family' : 'DFKai-SB',
    'weight' : 'bold',
    'size'  : '16'}
    plt.rc('font', **font) # pass in the font dict as kwargs
    plt.rc('axes',unicode_minus=False)
    with open(path, 'r', encoding = 'utf8') as f:
        lines   = f.readlines()[7:]
        line_NN = len(lines)-1
        # print(line_NN)
        counter = 0
        for index, single_line in enumerate(lines):
            
            
            temp = ','.join(single_line[:-1].split())

            t_array.append(float(temp.split(',')[0]))
            s_array.append(float(temp.split(',')[1]))
            w_array.append(float(temp.split(',')[2]))
            a_array.append(float(temp.split(',')[3]))
            e_array.append(float(temp.split(',')[4]))
            oil_sum = float(temp.split(',')[1]) + float(temp.split(',')[2]) + float(temp.split(',')[3]) + float(temp.split(',')[4])
            # print(index, temp)
            
            if index == line_NN:
 
                Surface       = round(float(temp.split(',')[1]),2)
                Surface_P     = round(float(temp.split(',')[1])/oil_sum*100,2)
                
                WaterColumn   = round(float(temp.split(',')[2]),2)
                WaterColumn_P = round(float(temp.split(',')[2])/oil_sum*100,2)
                
                Ashore        = round(float(temp.split(',')[3]),2)
                Ashore_P      = round(float(temp.split(',')[3])/oil_sum*100,2)
                
                Evaporated    = round(float(temp.split(',')[4]),2)
                Evaporated_P  = round(float(temp.split(',')[4])/oil_sum*100,2)
                # print('\n- - - - - - - -\n')
                # print("其中{}公噸({}%)海水表面殘存於海水表面，{}公噸({}%)因海水擾動混入海水中，{}公噸({}%)殘存於岸際，{}公噸({}%)揮發至大氣中".format(Surface,Surface_P, WaterColumn, WaterColumn_P, Ashore, Ashore_P, Evaporated, Evaporated_P))
                # print('\n- - - - - - - -\n')
                result_string = "其中{}公噸({}%)海水表面殘存於海水表面，{}公噸({}%)因海水擾動混入海水中，{}公噸({}%)殘存於岸際，{}公噸({}%)揮發至大氣中".format(Surface,Surface_P, WaterColumn, WaterColumn_P, Ashore, Ashore_P, Evaporated, Evaporated_P)
                with open(result_path, 'w') as r:
                    r.write(result_string)
            if float(temp.split(',')[1]) == 0 and counter == 0:
                time_stamp =  float(temp.split(',')[0])
                counter = 1         
                print('time_stamp :',time_stamp)            
                print('oil_sum    :',oil_sum)
                
    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())   
    fig, ax = plt.subplots(1, figsize=(12, 6))
    ax.plot(t_array, s_array, label='海表面', color = 'g'    , marker='o', linestyle='dashed')
    ax.plot(t_array, w_array, label='海水中', color = 'b'    , marker='>', linestyle='dashed')
    ax.plot(t_array, a_array, label='岸際'  , color = 'brown', marker='^', linestyle='dashed')
    ax.plot(t_array, e_array, label='揮發'  , color = 'c'    , marker='D', linestyle='dashed')
    ax.set_ylabel(oil_unit, fontsize=18)
    ax.set_xlabel('時間(小時)', fontsize=18)
    # ax.legend(fancybox=True,bbox_to_anchor=(1, 1))
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=5, fancybox=True)
    ax.set_title("油品隨時間質量平衡圖\n{}，{}{}，{}小時\n".format(oil_type, oil_amount, oil_unit , "24"), fontsize=32, pad=20,fontweight="bold")
    ax.grid(True)
    # manager = plt.get_current_fig_manager()
    # manager.full_screen_toggle()
    # plt.show()  
   
    fig.savefig(JPG_path,bbox_inches='tight')    
    # print(s_array)

def open_txt():
    subprocess.run([r'C:\Program Files\Notepad++\notepad++.exe', result_path], stdout=subprocess.PIPE, universal_newlines=True)

def main():
    init()
    make_tag()
    make_video()
    oil_remain()
    open_txt()
    # os.system("pause")




    