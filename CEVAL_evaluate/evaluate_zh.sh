shot=5  # few-shot [0,5]整数
gpu=0  # 显卡id
split=test  # 评估测试集, val or test 
model_id=math15k1b1_lora_combined   # 待评估的模型
task=ceval  # 任务名称：ceval 不用改动
base_model="/home/calvinzhang/huggingface_models/bloom-1b1" # 基模型
OPENMODEL_PATH='/home/ryanzhang/nlp/models/math15k1b1_lora_combined' # 训练后的模型 --use_base时自动被base_model覆盖
# --use_base type: store_true 评估基模型时加的参数
echo gpu_idx-${gpu}-${model_id}_${task}_${split}_${shot}-shot
nohup python  evaluate_zh.py \
    		--base_model ${base_model} \
			--OPENMODEL_PATH ${OPENMODEL_PATH} \
			--gpu_idx ${gpu} \
			--model_id ${model_id} \
			--task ${task} \
			--shot ${shot} \
			--split ${split} \
			--show_detail  > ${model_id}_${task}_${split}_${shot}-shot_record.txt 2>&1 &
