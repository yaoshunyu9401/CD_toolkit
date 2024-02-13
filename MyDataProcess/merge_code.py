#coding:utf-8
import os

import glob
from osgeo import gdal, ogr, osr


def get_prj(file_dir,file_dir2):
    driver = gdal.GetDriverByName("GTiff")
    #file_dir='dataset\\A'
    filelist=[]
    for root, dirs, files in os.walk(file_dir):
        filelist.append(root) #当前目录路径
        dirs #当前路径下所有子目录
        files #当前路径下所有非目录子文件

    #file_dir2='dataset\\predict\\'


    for index in range(len(files)) :
        datasetA=gdal.Open(file_dir+'//'+files[index])
        im_width = datasetA.RasterXSize #栅格矩阵的列数
        im_height = datasetA.RasterYSize #栅格矩阵的行数
        im_bands = datasetA.RasterCount #波段数
        im_geotrans = datasetA.GetGeoTransform()#获取仿射矩阵信息
        im_proj = datasetA.GetProjection()#获取投影信息

        dst_ds = gdal.Open(file_dir2+'//'+files[index], gdal.GA_Update)
        dst_ds.SetProjection(im_proj)
        dst_ds.SetGeoTransform(im_geotrans)
        dst_ds.GetRasterBand(1).SetNoDataValue(0)

        del datasetA
        del dst_ds

def attibute_table(lyr,save_shp,filter_area):
    lydefn = lyr.GetLayerDefn()
    spatialref = lyr.GetSpatialRef()  # 获取空间坐标系
    geomtype = lydefn.GetGeomType()  # 文件类型（point，polyline，polygon等）
    driver = ogr.GetDriverByName("ESRI Shapefile")  # 创建shp驱动
    out_shp = driver.CreateDataSource(save_shp)  # 创建文件，文件命名为字段属性值+输入的文件名。
    if spatialref == None:
        print(save_shp,' have none spatialref')
    else:
        print(save_shp,'\n',spatialref)
    outlayer = out_shp.CreateLayer('out_new', srs=spatialref, geom_type=geomtype)
    for k in range(0, lydefn.GetFieldCount()):
        fieldDefn = lydefn.GetFieldDefn(k)
        outlayer.CreateField(fieldDefn)
    outlayerDefn = outlayer.GetLayerDefn()

    feature = lyr.GetNextFeature()
    while feature:
        # 读取ID、cover字段值
        id = feature.GetFieldAsString('id')
        area = feature.GetFieldAsString('Area')
        if id != '0' :#and area >= 1000:
            outFeature = ogr.Feature(outlayerDefn)
            geom = feature.GetGeometryRef()
            area = geom.GetArea()  # 计算面积
            m_area = (area / (0.0089 ** 2)) * 1e+6  # 单位由十进制度转为米
            m_area = m_area * 0.81571
            if m_area >= filter_area:
                # print('area： {}'.format(m_area))
                outFeature.SetField('Area', m_area)  # 将面积添加到属性表中
                outlayer.SetFeature(outFeature)
                outFeature.SetGeometry(geom)
                outlayer.CreateFeature(outFeature)
        # 清除缓存并获取下一个要素
        feature.Destroy()
        feature = lyr.GetNextFeature()

    feature = None
    outFeature = None
    out_shp = None



# 设置工作目录和tif文件夹路径
def prdeict_shp(work_dir,shpname,filter_area):
    #work_dir = 'dataset\\'
    tif_dir = os.path.join(work_dir, 'predict')
    shp_file =  os.path.join(work_dir,shpname+'.shp')
    print(shp_file)
    saveshp =  os.path.join(work_dir,shpname+'_save.shp')


    # 获取tif文件列表
    tif_files = glob.glob(os.path.join(tif_dir, '*.tif'))

    # 设置输出shp文件的空间参考和几何信息
    spatial_ref = osr.SpatialReference()
    spatial_ref.ImportFromEPSG(4326)
    driver = ogr.GetDriverByName('ESRI Shapefile')
    out_ds = driver.CreateDataSource(shp_file)
    out_layer = out_ds.CreateLayer('output', spatial_ref, ogr.wkbPolygon)


    # out_ds2 = driver.CreateDataSource(save_shp_file)
    # saveshp = out_ds2.CreateLayer('output', spatial_ref, ogr.wkbPolygon)

    # 设置输出shp文件的属性表
    field_defn = ogr.FieldDefn('id', ogr.OFTInteger)
    out_layer.CreateField(field_defn)
    tif_file=tif_files[0]
    area = ogr.FieldDefn('Area', ogr.OFTInteger64)
    area.SetWidth(32)
    area.SetPrecision(16)  # 设置面积精度,小数点后16位
    out_layer.CreateField(area)
    # 将每个tif文件转化为多边形并添加到输出shp文件中
    for i, tif_file in enumerate(tif_files):
        # 打开tif文件
        ds = gdal.Open(tif_file)

        band = ds.GetRasterBand(1)
        nodata = band.GetNoDataValue()
        transform = ds.GetGeoTransform()

        # 将像素值为1的区域转化为多边形
        #print(band.GetMaskBand())

        # 设置多边形的属性值


        gdal_polygonize = gdal.Polygonize(band, band.GetMaskBand(), out_layer, 0, [], callback=None)

        #gdal_polygonize = gdal.Polygonize(band, None, out_layer, 0, [], callback=None)
        gdal_polygonize = None

        #feature = out_layer.GetFeature(i)
        #feature.SetField('id', i)
        #out_layer.SetFeature(feature)
        # 释放资源
        ds = None
    attibute_table(out_layer,saveshp,filter_area)
    # 保存输出shp文件
    out_ds.SyncToDisk()
    out_ds = None


