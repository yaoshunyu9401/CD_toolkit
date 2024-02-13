import os,sys,re
import platform
if platform.system().lower() == 'windows':
    spt_str = '\\'
elif platform.system().lower() == 'linux':
    spt_str = '/'

def get_list_A(file_dir,savedir):
    #file_dir='dataset\\A'
    filelist=[]
    folder_path = savedir
    #file_name = "某个.txt"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print('create:'+folder_path)

    files = os.listdir(file_dir)
    files.sort()
    # for root, dirs, files in os.walk(file_dir):
    #     filelist.append(root) #当前目录路径
    #     dirs #当前路径下所有子目录
    #     sorted(files) #当前路径下所有非目录子文件


    #filename = 'dataset\\list\\demo.txt'
    filename=savedir+spt_str+'demo.txt'

    with open(filename, 'w',encoding='utf-8') as f:
        for s in files:
            f.write(s + '\n')


    filename = savedir+spt_str+'test.txt'

    with open(filename, 'w',encoding='utf-8') as f:
        for s in files:
            f.write(s + '\n')

    filename = savedir+spt_str+'train.txt'

    with open(filename, 'w',encoding='utf-8') as f:
        for s in files:
            f.write(s + '\n')

    filename = savedir+spt_str+'val.txt'

    with open(filename, 'w',encoding='utf-8') as f:
        for s in files:
            f.write(s + '\n')
    # filename = 'datasetval.txt'
    #
    # with open(filename, 'w',encoding='utf-8') as f:
    #     for s in files:
    #         f.write(s + '\n')

work_dir = sys.argv[1]
#work_dir='dataset\\crop_256'
list_savedir = os.path.join(work_dir, 'list')
file_dir= os.path.join(work_dir, 'A')
#file_dir='dataset\\crop_256\\A'
#list_savedir='dataset\\crop_256\\list'
get_list_A(file_dir,list_savedir)