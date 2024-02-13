#from MyDataProcess import merge_code
import merge_code
import os,sys,re
import platform
if platform.system().lower() == 'windows':
    spt_str = '\\'
elif platform.system().lower() == 'linux':
    spt_str = '/'

work_dir = sys.argv[1]
#work_dir='dataset\\crop_256'
list_savedir = os.path.join(work_dir, 'list')
file_dir= os.path.join(work_dir, 'A')
#file_dir='dataset\\crop_256\\A'
#list_savedir='dataset\\crop_256\\list'
#get_list.get_list_A(file_dir,list_savedir)


'''


'''
#work_dir='dataset\\crop_256'
#file_dir='dataset\\crop_256\\A'
pre_savedir=os.path.join(work_dir, 'predict')

#pre_savedir='dataset\\crop_256\\predict\\'
#file_dir= os.path.join(work_dir, 'A')
dirs=os.listdir(pre_savedir)
filename=dirs[0].split('_')[0]
print(file_dir)
print(pre_savedir)
merge_code.get_prj(file_dir,pre_savedir)
filter_area=1000
merge_code.prdeict_shp(work_dir,filename+filter_area.__str__(),filter_area)



