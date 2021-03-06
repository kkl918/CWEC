## 統計輸油作業通報

import os, shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog as fd

tk_root = tk.Tk()

tk_Path = fd.askdirectory()


if tk_Path != '':
    print(tk_Path)
    dst_path       = Path(r'C:\Users\USER\Desktop\輸油作業通報\IMGS')
    dst_path       = Path(r'\\203.64.168.112\oca專案辦公室\(2)輸油作業通報\TEST\9-12成果')

    dirpath        = tk_Path
    
    # pathlib.Path(dirpath.joinpath('')).mkdir(parents=True, exist_ok=True)
    root_path      = Path(dirpath)
    # print(dirpath.split('\\'))

    trans_type  = dirpath.split('/')[-1]
    trans_month = dirpath.split('/')[-2]


    sum_dic        = {}
    tatal_dic      = {}
    valid_dic      = {}
    sum_img        = 0

    img_list       = []
    


else:
    print('沒有選取資料夾')
    exit()
    # dst_path       = Path(r'C:\Users\USER\Desktop\輸油作業通報\IMGS')
    # dst_path       = Path(r'\\203.64.168.112\oca專案辦公室\(2)輸油作業通報\TEST\9-12成果')

    # dirpath        = r'C:\Users\USER\Desktop\輸油作業通報\111年02月\化學品'

    # root_path      = Path(dirpath)

    # trans_type  = dirpath.split('\\')[-1]
    # trans_month = dirpath.split('\\')[-2]


    # sum_dic        = {}
    # tatal_dic      = {}
    # valid_dic      = {}
    # sum_img        = 0

    # img_list       = []    
    # print(dirpath)


# 遞迴尋找照片
def iterfind_img(dir_path):
    for item in dir_path.iterdir():
        if item.is_file():
            center_name = item.parents[2].name
            ship_name   = item.parents[1].name
            img_name    = item.name
            
            sum_dic[work_center.name].append(item)
            
            global sum_img
            sum_img += 1
            
            img_list.append(item)
        else:
            # print(item)
            iterfind_img(item)
    


for work_day in root_path.iterdir():
    # print(work_day)
    for work_center in work_day.iterdir():
        sum_dic[work_center.name]   = []
        tatal_dic[work_center.name] = 0
        valid_dic[work_center.name] = 0
        

for work_day in root_path.iterdir():
    for work_center in work_day.iterdir():
        for work_ship in work_center.iterdir():
            if os.path.isdir(work_ship):
        
                img_dir = work_ship.joinpath('02.回報照片')
                if img_dir.exists():
                    pass
                    # print(img_dir)
                else:
                    img_dir.mkdir(parents=True, exist_ok=True)


                if len(os.listdir(img_dir)) == 0:
                    tatal_dic[work_center.name] += 1
                    print(work_center)
                else:
                    tatal_dic[work_center.name] += 1
                    valid_dic[work_center.name] += 1
                 
                iterfind_img(img_dir)    
                            # for img_path in img_dir.glob('**/*'):
                    # if img_path.is_file():
                        # center_name = img_path.parents[2].name
                        # ship_name   = img_path.parents[1].name
                        # img_name    = img_path.name
                        # sum_dic[work_center.name].append(img_name)
                        # sum_img += 1
                    # else:
                        # folder_path = img_path
                        # for img_path in folder_path.iterdir():
                            # print(img_path)
                  
                    
                # print(center_name, ship_name, img_path)
                # sp = img_path.__str__().split('\\') # split path by \
                # new_file_name = '{}_{}_{}_{}'.format(sp[-5], sp[-4], sp[-3], sp[-1])
                # print(sp)
                # print(sp[-5], new_file_name)
# print(sum_dic)
# print(len(sum_dic.keys())

# print(sum_dic)
for key in sum_dic.keys():
    for report_file in sum_dic[key]:
        sp = report_file.__str__().split('\\')                                # split path by \
        nn = '{}_{}_{}_{}_{}'.format(sp[-5], sp[-4], sp[-3], sp[-2], sp[-1])  # new name
        # print(dst_path.joinpath(nn))
        # print(report_file)
        # shutil.copy(report_file, dst_path.joinpath(nn))

    


# print(str(root_path.parents[0]))
print('單位照片總量,實際通報次數,應通報次數,通報率')
csv_file = r'{}\{}_{}.csv'.format(str(root_path.parents[0]), trans_month, trans_type)
with open(csv_file, 'w', encoding = 'utf-8-sig')as f:
    f.write('{}\n'.format(trans_month))
    f.write('單位名稱,照片總量,實際通報次數,應通報次數,通報率\n')
    for i in sum_dic.keys():
        
        print(  '{},{},{},{},{:.1%}'.format(  i, len(sum_dic[i]), valid_dic[i], tatal_dic[i], valid_dic[i]/tatal_dic[i]))
        f.write('{},{},{},{},{:.1%}\n'.format(i, len(sum_dic[i]), valid_dic[i], tatal_dic[i], valid_dic[i]/tatal_dic[i]))
    f.write('合計收到:{}張輸油通報照片'.format(sum_img))
print('合計收到:{}張輸油通報照片'.format(sum_img))

os.startfile(csv_file)
os.system("pause")