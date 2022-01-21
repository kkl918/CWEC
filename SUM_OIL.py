## 統計輸油作業通報

import os
from pathlib import Path

kk = '110年12月'

dirpath        = r'C:\Users\USER\Desktop\輸油作業通報\{}'.format(kk)
root_path      = Path(dirpath)

sum_dic        = {}
tatal_dic      = {}
valid_dic      = {}
sum_img        = 0

for work_day in root_path.iterdir():
    for work_center in work_day.iterdir():
        sum_dic[work_center.name]   = []
        tatal_dic[work_center.name] = 0
        valid_dic[work_center.name] = 0
        

for work_day in root_path.iterdir():
    for work_center in work_day.iterdir():
        for work_ship in work_center.iterdir():
            img_dir = work_ship.joinpath('02.回報照片')
            if img_dir.exists():
                pass
                # print(img_dir)
            else:
                img_dir.mkdir(parents=True, exist_ok=True)


            if len(os.listdir(img_dir)) == 0:
                tatal_dic[work_center.name] += 1
            else:
                tatal_dic[work_center.name] += 1
                valid_dic[work_center.name] += 1
                
            for img_path in img_dir.glob('**/*'):
                
                center_name = img_path.parents[2].name
                ship_name   = img_path.parents[1].name
                img_name    = img_path.name
                sum_dic[work_center.name].append(img_name)
                sum_img += 1
                
                # print(center_name, ship_name, img_path)
# print(sum_dic)
# print(len(sum_dic.keys())

print(kk)
print('單位照片總量,實際通報次數,應通報次數,通報率')
csv_file = r'C:\Users\USER\Desktop\{}.csv'.format(kk)
with open(csv_file, 'w', encoding = 'utf-8-sig')as f:
    f.write('{}\n'.format(kk))
    f.write('單位名稱,照片總量,實際通報次數,應通報次數,通報率\n')
    for i in sum_dic.keys():
        
        print(  '{},{},{},{},{:.1%}'.format(  i, len(sum_dic[i]), valid_dic[i], tatal_dic[i], valid_dic[i]/tatal_dic[i]))
        f.write('{},{},{},{},{:.1%}\n'.format(i, len(sum_dic[i]), valid_dic[i], tatal_dic[i], valid_dic[i]/tatal_dic[i]))
    f.write('合計收到:{}張輸油通報照片'.format(sum_img))
print('合計收到:{}張輸油通報照片'.format(sum_img))