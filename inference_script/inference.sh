#! /bin/bash

model_name_or_path=/home/calvinzhang/huggingface_models/bloom-560m
ckpt_path=/home/ryanzhang/nlp/models/HC3_ft560
test_set=/home/ryanzhang/nlp/mydata/HC3_dev1k.json
test_num=5
write_data=/home/ryanzhang/nlp/inference_json/bloom-560m_HC3_ft.json

CUDA_VISIBLE_DEVICES=1 python /home/ryanzhang/nlp/BELLE/train/src/inference.py \
    --model_name_or_path ${model_name_or_path} \
    --ckpt_path ${ckpt_path} \
    --test_set ${test_set} \
    --test_num ${test_num} \
    --save_log  \
    --write_data ${write_data}
