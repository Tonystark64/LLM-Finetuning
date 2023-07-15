#! /bin/bash

# model_name_or_path=/path_to_llm/hf_llama_7b/ # or bloomz-7b1-mt
model_name_or_path=/home/calvinzhang/huggingface_models/bloom-1b1

train_file=/home/ryanzhang/nlp/mydata/HC3_train.json
validation_file=/home/ryanzhang/nlp/mydata/HC3_dev1k.json
# output_dir=/home/ryanzhang/nlp/models/saved_models
output_dir=/home/ryanzhang/nlp/models/HC3_ft
# mkdir -p ${output_dir}
mkdir -p ${output_dir}

cache_dir=/home/ryanzhang/nlp/models/HC3_ft_cache
mkdir -p ${cache_dir}
cutoff_len=512 # LLaMA suggests 1024


# #FT
torchrun --nproc_per_node 2 /home/ryanzhang/nlp/BELLE/train/src/train.py \
    --model_name_or_path ${model_name_or_path} \
    --deepspeed /home/ryanzhang/nlp/BELLE/train/configs/deepspeed_config.json \
    --train_file ${train_file} \
    --validation_file ${validation_file} \
    --per_device_train_batch_size 2 \
    --per_device_eval_batch_size 2 \
    --gradient_accumulation_steps 4 \
    --num_train_epochs 2 \
    --model_max_length ${cutoff_len} \
    --save_strategy "steps" \
    --save_total_limit 3 \
    --learning_rate 8e-6 \
    --weight_decay 0.00001 \
    --warmup_ratio 0.05 \
    --lr_scheduler_type "cosine" \
    --logging_steps 10 \
    --evaluation_strategy "steps" \
    --fp16 True \
    --seed 1234 \
    --gradient_checkpointing True \
    --cache_dir ${cache_dir} \
    --output_dir ${output_dir}



