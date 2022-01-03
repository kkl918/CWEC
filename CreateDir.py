import os, shutil

par_path  = os.path.dirname(__file__)
NewName = input('New Folder Name : ')

DirName      = ['01.OIL','02.OIL(WEB)','03.CURRENT','05.風化結果','06.海氣象資料','07.SHP','08.專案檔','09.其他(事故位置圖,ZSV檔...)']
DirPathList  = [ os.path.join(par_path, i) for i in DirName ]

txt_path     = os.path.join(par_path, '新文字文件.txt')


DocName      = [i for i in os.listdir(par_path) if i.endswith('docx')][0]
DocPath      = os.path.join(par_path, DocName)

NewPath      = os.path.join(os.path.dirname(par_path), NewName)

NewPath_List = [os.path.join(NewPath, i) for i in DirName]
DocPath_New  = os.path.join(NewPath, DocName)
txt_path_New = os.path.join(NewPath, '新文字文件.txt')

for i in range(0,len(DirPathList)):
    print(DirPathList[i], '\t',NewPath_List[i])
    if os.path.isdir(DirPathList[i]):
        print(DirPathList[i], '\t',NewPath_List[i])
        shutil.copytree(DirPathList[i], NewPath_List[i])


if os.path.isfile(DocPath):
    print(DocPath,DocPath_New)
    shutil.copy(DocPath,DocPath_New)

if os.path.isfile(txt_path):
    print((txt_path,txt_path_New ))
    shutil.copy(txt_path,txt_path_New )

shutil.copy(__file__,os.path.join(NewPath, os.path.basename(__file__) ))


oil_path  = os.path.join(NewPath , '01.OIL')
work_dir  = [i for i in os.listdir(oil_path) if i != 'v6'][0]
work_path = os.path.join(oil_path, work_dir)

for item in os.listdir(work_path):
    item_path = os.path.join(work_path, item)
    if item == 'TAGED':
        shutil.rmtree(item_path)
    if item.endswith('jpg') or item.endswith('wmv'):
        os.remove(item_path)
