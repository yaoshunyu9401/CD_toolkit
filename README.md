# Transformers�仯�������ģ��˵��

## ����˵��

�������ʵ�����Զ����ü���ʶ��ƴ�Ӳ�ת��Ϊshp�ļ����������Transformersģ��

�������bug����ϵyaoshunyu9401@gmail.com


![image](./images/network.png)

![image](./images/transformer.png)

## Requirements
```
Python 3.10
pytorch 1.13.0
torchvision 0.14.0
einops  0.6.1
gdal  3.4.3
tifffile 
```

## ����˵��
���ݼ�������������2022���2023���ң��Ӱ�񣬻���IWHR_data���ݼ������ݼ�������������

���ӣ�https://pan.baidu.com/s/1lh1yuX_DC7M9tpKl2S_s8A 
��ȡ�룺4cix

### ����׼��

```
"""
����Ӱ����ļ�����dateset�ڣ�
����T1
����T2
����label
����crop_256
"""
```
`T1`: t1 phase;

`T2`: t2 phase;

`label`: label maps, ���ִ��Ԥ���ڴ��ļ����·���������T1��T2ͬ����ͼ���ļ�
�����д�С��T1��T2ͬ����ͼ���ļ�һ�£���ͼ�񲻲���Ԥ��;

`crop_256`: contains `A, B, label, List and predict`, 
���ļ��м������ݿ����Զ����ɣ�����Ԥ������shp�ļ�Ҳ����ڴ��ļ�����.

### ���ݼ��ṹ

```
"""
Change detection data set with pixel-level binary labels��
����A
����B
����label
����list
"""
```


## ���нű�˵��

### Predict

���ļ�����`scripts`�ҵ�ѵ���ű�`run_server.sh` , ����ű��������Զ��ü���
��ȡ�ü����ͼƬ�б���ȡ���ݲ�����ǰ�򴫲�Ԥ�⣬��Ԥ����ͼ�߸�������ƴ�ӣ���
ת��Ϊshp�ļ������˵���С��ͼ�ߣ�ʵ�ֶ�ң��Ӱ����Զ���ͼ����ȡ����

������terminal������ `sh scripts/run_server.sh` (ע�⣺���python������·����·��
Ҫ��python��Ŀһ��).

`run_server.sh` ����ϸ��������:

```cmd
#!/usr/bin/env bash

gpus=0

data_name=application
net_G=base_transformer_pos_s4_dd8
split=test
project_name=CD_base_transformer_pos_s4_dd8_LEVIR_b8_lr0.01_train_val_200_linear
checkpoint_name=best_ckpt.pt
echo $(date +%T)
python MyDataProcess/crop_size.py ./dataset 256
python MyDataProcess/get_list.py ./dataset/crop_256
echo $(date +%T)
python image_forwrd_.py --split ${split} --net_G ${net_G} --checkpoint_name ${checkpoint_name} --gpu_ids ${gpus} --project_name ${project_name} --data_name ${data_name}
echo $(date +%T)
python MyDataProcess/result_process.py ./dataset/crop_256
echo $(date +%T)

```


