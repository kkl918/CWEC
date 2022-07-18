import tkinter as tk
from pathlib import Path
from tkinter import filedialog as fd

tk_root = tk.Tk()

tk_Path = fd.askopenfilename()

if tk_Path != '':
    x1 = float(input('經度上限:'))
    x2 = float(input('經度下限:'))
    y1 = float(input('緯度上限:'))
    y2 = float(input('緯度下限:'))
    # x1 = 120
    # x2 = 121
    # y1 = 21
    # y2 = 22
    print(tk_Path)


    dir_path  = tk_Path
    root_path      = Path(dir_path)
    xyz_file = r'{}\{}_{}_{}_{}.xyz'.format(str(root_path.parents[0]), str(x1), str(x2), str(y1), str(y2))
    


else:
    print('沒有選取資料夾')
    exit()

    # x1 = 120
    # x2 = 123
    # y1 = 21
    # y2 = 24

with open(dir_path, 'r')as f:
    with open(xyz_file,'w')as f_out:
        for single_line in f.readlines()[1:]:
            LON = float(single_line.split(',')[0])
            LAT = float(single_line.split(',')[1])
            DEP = float(single_line.split(',')[2])
            # print(single_line)
            if LON > x1 and LON < x2 and LAT > y1 and LAT < y2:
                f_out.write('{},{},{}\n'.format(LON, LAT, DEP))
                # print('{},{},{}\n'.format(LON, LAT, DEP))
    