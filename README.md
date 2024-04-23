# Transformers for change detection in remote sensing images（change detection）

## Program description
This repository contains all the code needed to reproduce the paper:
A Renovated Framework of a Convolution Neural Network with Transformer for Detecting Surface Changes from High-Resolution Remote-Sensing Images

DOI：https://doi.org/10.3390/rs16071169

This program implements automated cropping, recognition, splicing and conversion into shp files. The network uses the CNN-Transformers architecture.

If you have any questions please contactyaoshunyu9401@gmail.com


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

## Data description
数据集内有两个区县2022年和2023年的遥感影像，还有IWHR_data数据集。数据集分享链接如下

链接：https://pan.baidu.com/s/1lh1yuX_DC7M9tpKl2S_s8A 
提取码：4cix

The link has expired. If you need data, please contact the author.

### data preparation

```
"""
The folders of the two periods of remote sensing images are in the dateset folder.；
├─T1
├─T2
├─label
└─crop_256
"""
```
`T1`: t1 phase;

`T2`: t2 phase;

`label`: label maps, if prediction is performed, image files with the same name as T1 and T2 will be placed in this folder.
, the row and column size is consistent with the image files with the same name as T1 and T2, this image does not participate in prediction;

`crop_256`: contains `A, B, label, List and predict`, 
This folder and its contents can be automatically generated, and the shp file of the final prediction result will also be placed under this folder.

### Dataset structure

```
"""
Change detection data set with pixel-level binary labels；
├─A
├─B
├─label
└─list
"""
```


## Instructions for running the script

### Predict
Find the training script `run_server.sh` in the `scripts` folder. This script integrates automatic cropping.
Obtain the cropped picture list, read the data and perform forward propagation prediction, assign coordinate splicing to the predicted image spots, and
Convert to shp file, filter out smaller patches, and realize automatic patch extraction and processing of remote sensing images

You can run `sh scripts/run_server.sh` in the terminal (note: check the python environment and path, path
It must be consistent with the python project).

 The details in `run_server.sh` are as follows

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
## citation

If you use this code for research, please cite our paper.

```
"""
@Article{rs16071169,
AUTHOR = {Yao, Shunyu and Wang, Han and Su, Yalu and Li, Qing and Sun, Tao and Liu, Changjun and Li, Yao and Cheng, Deqiang},
TITLE = {A Renovated Framework of a Convolution Neural Network with Transformer for Detecting Surface Changes from High-Resolution Remote-Sensing Images},
JOURNAL = {Remote Sensing},
VOLUME = {16},
YEAR = {2024},
NUMBER = {7},
ARTICLE-NUMBER = {1169},
URL = {https://www.mdpi.com/2072-4292/16/7/1169},
ISSN = {2072-4292},
DOI = {10.3390/rs16071169}
}
"""
```




