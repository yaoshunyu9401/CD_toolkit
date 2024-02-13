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
