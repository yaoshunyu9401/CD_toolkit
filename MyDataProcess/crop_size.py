#!coding=utf-8
import os,sys,re
from os import mkdir
from osgeo import gdal
import cv2
import numpy as np
#import utils
#from util.util import mkdir, mkdirs
import platform
if platform.system().lower() == 'windows':
    spt_str = '\\'
elif platform.system().lower() == 'linux':
    spt_str = '/'

'''
usage:
python crop_size.py [dir] [size]
python crop_size.py ./dataset 256
dir: str,路径下都是tif文件，label为argis将.shp导出的tif文件
├─change_label
│      340603相山区.tif
├─T1
│      340603相山区.img
└─T2
       340603相山区.tif
size: int, 裁切的大小
'''


if sys.argv[1] != None:
    path = sys.argv[1]
else:
    # path = r'E:\DATA\RemoteData\DSIFN-Dataset\train'
    path = r'dataset\\'


cropsize = int(sys.argv[2])
cropsize_x = cropsize
cropsize_y = cropsize
print(cropsize)
if len(sys.argv) == 4:
    pre = sys.argv[3]
else:
    pre = ''
'''usage:
python crop_size.py ./ 512
'''
# a=gdal.Open(r'D:\博士后研究\变化检测\bitcd\LEVIR-CD\samples\T2\340208三山区.tif')
# im_proj = a.GetProjection()
# ori_transform = a.GetGeoTransform()
#裁切图像,固定裁切尺寸
def mkdir(path):
    """create a single empty directory if it didn't exist

    Parameters:
        path (str) -- a single directory path
    """
    if not os.path.exists(path):
        os.makedirs(path)
def mkdirs(paths):
    """create empty directories if they don't exist

    Parameters:
        paths (str list) -- a list of directory paths
    """
    if isinstance(paths, list) and not isinstance(paths, str):
        for path in paths:
            mkdir(path)
    else:
        mkdir(paths)
def cropImg(crop_size,fileLists,out_dir,overlap=True):
    '''
    :param crop_size: 裁切边长
    :param path:
    :param out_dir:
    :param overlap: True 表示固定尺寸大小，边缘处裁切有重叠；False 表示边缘处裁切无重叠
    :return:
    '''
    before_path = fileLists[0]
    after_path = fileLists[1]
    #change_path = fileLists[2]
    print(before_path)
    print(after_path)
    #print(change_path)
    #E:\DATA\RemoteData\CD_Data_GZ\CD_Data_GZ\T1\P_GZ_test9_2010_1103_Level_18.tif
    if 'CD_Data_GZ' in before_path:
        fileName = pre + '_' + (os.path.split(before_path)[1]).rsplit('_',4)[0]
        print(fileName)
    # if 'Building_change' in before_path or '110108' in before_path:
    else:
        if pre == '':
            fileName = (os.path.split(before_path)[1]).split('.')[0]
        else:
            fileName = pre + '_' + (os.path.split(before_path)[1]).split('.')[0]
        print(fileName)
    fn_lists = []
    for n, path in enumerate(fileLists):
        print('path: ',path)
        in_ds = gdal.Open(path)			  # 读取要切的原图
        width = in_ds.RasterXSize                         # 获取数据宽度
        height = in_ds.RasterYSize                        # 获取数据高度
        print("open {} succeed".format(path))
        print('width: {},height: {}'.format(width, height))
        outbandsize = in_ds.RasterCount                   # 获取数据波段数
        im_proj = in_ds.GetProjection()                   # 获取投影信息
        datatype = in_ds.GetRasterBand(1).DataType
        if width >= crop_size and height >= crop_size:

            print('*'*20)
            print(height,width)
            if n != 2:
                # 读取原图中的每个波段
                in_band1 = in_ds.GetRasterBand(1)
                in_band2 = in_ds.GetRasterBand(2)
                in_band3 = in_ds.GetRasterBand(3)
            else:
                if outbandsize == 1:
                    in_band1 = in_ds.GetRasterBand(1)
                    in_band2 = in_band1
                    in_band3 = in_band1
                else:
                    in_band1 = in_ds.GetRasterBand(1)
                    in_band2 = in_ds.GetRasterBand(2)
                    in_band3 = in_ds.GetRasterBand(3)
            # 获取原图的原点坐标信息
            ori_transform = in_ds.GetGeoTransform()
            if not ori_transform:
                print('read tif file faild...{}'.format(path))
                raise AssertionError

            # 读取原图仿射变换参数值
            row_num = height // crop_size
            col_num = width // crop_size
            # if (width % crop_size != 0):
            #     col_num += 1
            # if (height % crop_size != 0):
            #     row_num += 1
            num = 1
            print("now croping ... ...")
            if overlap:  #
                for i in range(int(row_num)):
                    for j in range(int(col_num)):
                        #print('i,j: ',i,j)
                        offset_x = crop_size * j
                        offset_y = crop_size * i
                        block_xsize = min(width - offset_x, crop_size)
                        block_ysize = min(height - offset_y, crop_size)
                        top_left_x = ori_transform[0]  # 左上角x坐标
                        w_e_pixel_resolution = ori_transform[1]  # 东西方向像素分辨率
                        top_left_y = ori_transform[3]  # 左上角y坐标
                        n_s_pixel_resolution = ori_transform[5]  # 南北方向像素分辨率
                        #print('c_x,c_y,b_x,b_y: ',offset_x,offset_y,block_xsize,block_ysize)
                        try:
                            if block_xsize < crop_size and block_ysize == crop_size:
                                offset_x = max(0,width - crop_size)
                                out_band1 = in_band1.ReadAsArray(offset_x, offset_y, block_xsize, crop_size)
                                out_band2 = in_band2.ReadAsArray(offset_x, offset_y, block_xsize, crop_size)
                                out_band3 = in_band3.ReadAsArray(offset_x, offset_y, block_xsize, crop_size)
                            elif block_xsize == crop_size and block_ysize < crop_size:
                                offset_y = max(0,height - crop_size)
                                out_band1 = in_band1.ReadAsArray(offset_x, offset_y, crop_size, block_ysize)
                                out_band2 = in_band2.ReadAsArray(offset_x, offset_y, crop_size, block_ysize)
                                out_band3 = in_band3.ReadAsArray(offset_x, offset_y, crop_size, block_ysize)
                            elif block_xsize < crop_size and block_ysize < crop_size:
                                offset_x = max(0,width - crop_size)
                                offset_y = max(0,height - crop_size)
                                out_band1 = in_band1.ReadAsArray(offset_x, offset_y, block_xsize, block_ysize)
                                out_band2 = in_band2.ReadAsArray(offset_x, offset_y, block_xsize, block_ysize)
                                out_band3 = in_band3.ReadAsArray(offset_x, offset_y, block_xsize, block_ysize)
                            elif block_xsize == crop_size and block_ysize == crop_size:
                                out_band1 = in_band1.ReadAsArray(offset_x, offset_y, crop_size, crop_size)
                                out_band2 = in_band2.ReadAsArray(offset_x, offset_y, crop_size, crop_size)
                                out_band3 = in_band3.ReadAsArray(offset_x, offset_y, crop_size, crop_size)
                            # print('type:', type(out_band1))
                            # print('max: ', np.max(out_band1))
                            # print('min: ', np.min(out_band1))
                            #if float(len(out_band1[out_band1==0]) / (cropsize*cropsize)) <= 1.1:
                            if True:
                                # 获取Tif的驱动，为创建切出来的图文件做准备
                                gtif_driver = gdal.GetDriverByName("GTiff")
                                # 创建切出来的要存的文件
                                # if i == 0:
                                fn = out_dir[n] + '/' + '%s_%04d_%04d.tif' % (fileName, i, j)
                                if num % 10 == 0:
                                    print('{} saved done.'.format(fn))
                                num += 1
                                fn_lists.append(fn)
                                if not os.path.exists(fn):
                                    if n != 2:
                                        # out_ds = gtif_driver.Create(fn, crop_size, crop_size, 3, datatype)
                                        out_ds = gtif_driver.Create(fn, block_xsize, block_ysize, 3, datatype)
                                    else:
                                        # out_ds = gtif_driver.Create(fn, crop_size, crop_size, 1, datatype)
                                        out_ds = gtif_driver.Create(fn, block_xsize, block_ysize, 1, datatype)
                                    # 写入目标文件
                                    if n != 2:
                                        top_left_x = top_left_x + offset_x * w_e_pixel_resolution
                                        top_left_y = top_left_y + offset_y * n_s_pixel_resolution
                            # 将计算后的值组装为一个元组，以方便设置
                                        dst_transform = (top_left_x, ori_transform[1], ori_transform[2], top_left_y, ori_transform[4], ori_transform[5])
                            # 设置裁剪出来图的原点坐标
                                        out_ds.SetGeoTransform(dst_transform)
                            # 设置SRS属性（投影信息）
                                        out_ds.SetProjection(im_proj)
                                        out_ds.GetRasterBand(1).WriteArray(out_band1)
                                        out_ds.GetRasterBand(2).WriteArray(out_band2)
                                        out_ds.GetRasterBand(3).WriteArray(out_band3)
                                    else:
                                        # print('out_band1 type', type(out_band1))
                                        try:
                                            out_band1 = 0.114 * (np.array(out_band3)) + 0.587 * (
                                                np.array(out_band2)) + 0.299 * (
                                                            np.array(out_band1))
                                            # if np.max(out_band1) != 255:
                                            #print('out_band1 type: ',out_band1.shape)
                                            #print(out_band1)
                                            out_band1[out_band1 > 0] = 255
                                            out_band1[out_band1 == 0] = 0

                                            top_left_x = top_left_x + offset_x * w_e_pixel_resolution
                                            top_left_y = top_left_y + offset_y * n_s_pixel_resolution
                                            dst_transform = (top_left_x, ori_transform[1], ori_transform[2], top_left_y, ori_transform[4], ori_transform[5])
                                            out_ds.SetGeoTransform(dst_transform)
                                            out_ds.SetProjection(im_proj)
                                            out_ds.GetRasterBand(1).WriteArray(out_band1)
                                        except:
                                            pass
                                    # 将缓存写入磁盘
                                    out_ds.FlushCache()
                                    del out_ds
                        except:
                            print('top_x:{},top_y:{} croped faild...'.format(offset_x, offset_y))
    return fn_lists
# for (root, dirs, files) in os.walk(path):
T1_lists, T2_lists, change_lists = [], [], []

for dir in os.listdir(path):
    save_A_path = path + '/crop_' + str(cropsize) + '/A'
    save_B_path = path + '/crop_' + str(cropsize) + '/B'
    save_label_path = path + '/crop_' + str(cropsize) + '/label'
    mkdirs(save_A_path)
    mkdirs(save_B_path)
    mkdirs(save_label_path)
    dir_list = []
    root = os.path.join(path,dir)
    print('root: ',root)
    try:
        for file in os.listdir(root):
            # print('file: ',file)
            file_path = os.path.join(root,file)
            # print('filepath',file_path)
            if 'T1' in file_path and (file_path.endswith('.tif') or file_path.endswith('.jpg') or file_path.endswith('.png') or file_path.endswith('.img')):
                T1_lists.append(file_path)
                print('T1 dirs open succeed')
                # print('file_path: ', file_path)
            elif 'T2' in file_path and (file_path.endswith('.tif') or file_path.endswith('.jpg') or file_path.endswith('.png') or file_path.endswith('.img')):
                T2_lists.append(file_path)
                print('T2 dirs open succeed')
                # print('file_path: ', file_path)
            elif 'label' in (file_path).rsplit(spt_str,2)[1] and (file_path.endswith('.tif') or file_path.endswith('.jpg') or file_path.endswith('.png') or file_path.endswith('.bmp')or file_path.endswith('.img')):
                # if file_path.endswith('.tif'):
                #     jpgpath = tif2jpg(file_path)
                #     file_path = jpgpath
                change_lists.append(file_path)
                print('label dirs open succeed')
                print('file_path: ', file_path)
    except:
        pass

print(sorted(T1_lists))
print(sorted(T2_lists))
print(sorted(change_lists))

for i in range(len(T1_lists)):
    print(i)
    abc = [T1_lists[i],T2_lists[i]]#,change_lists[i]]
    print(abc)
     #             fileLists = [before,after,change]
    cropImg(crop_size=cropsize,fileLists=abc,out_dir=[save_A_path,save_B_path,save_label_path])
    #cropImg2(crop_size=cropsize,path=abc,out_dir=[save_A_path,save_B_path,save_label_path])
