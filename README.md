## Introduction  
>1. The scripts are modified from [BELLE](https://github.com/LianjiaTech/BELLE) project v2  
>2. We modified some scripts to cater to our training purposes:
## Data Collection  
>1. The scripts inside [**crawler**](./crawler) folder are to collect posts from a forum website.   
## Preprocess  
>1. The *convert_to_conv_data.py* is to convert our customized JSON files so that they align with BELLE model.   
>2. For context-based question answering, we need to combine context and question into the new question field.    
>3. When context is missed, chatgpt or other ground true answers would have relatively regular pattern which can be used for filtering.
>4. When encountered *TypeError: TextEncodeInput must be Union[TextInputSequence, Tuple[InputSequence, InputSequence]]*, we may filter out NoneType data in our dataset.  

The converted format:  
```json
{
    "id": "dataset_name-index",
    "conversations": [
        {"from": "human", "value": "...question..."},
        {"from": "assistant", "value": "...answer..."}
    ]
}
{"id": "math-1", "conversations": [{"from": "human", "value": "题目：小明每天早上花费10分钟时间走到学校，如果小明家距离学校2公里，那么他每分钟走多少米？"}, {"from": "assistant", "value": "这是一个关于速度、路程、时间的数学问题。我们可以通过公式：速度＝路程÷时间 来解决。\n因为小明每天早上走2公里，所以他的路程为2千米。而他每天早上要花费10分钟时间走到学校，因此他的时间为10分钟，即600秒。\n所以小明每分钟走的距离为 2公里 / 600秒 = 0.0033公里/秒 或 3.3米/秒。\n答案：小明每分钟走3.3米。"}]}
{"id": "math-2", "conversations": [{"from": "human", "value": "题目：今天小明骑自行车从家到学校用了20分钟，回家用了25分钟。如果小明在上学和回家的路上的速度一样，那么他从家到学校的距离是学校到家的距离的百分之几？"}, {"from": "assistant", "value": "\n假设小明家到学校的距离为x千米，根据速度等于路程除以时间的公式，可以得出小明的速度为：家到学校的速度 = x / 20，学校到家的速度 = x / 25。因为小明在上学和回家的路上的速度一样，所以有：x / 20 = x / 25，解出 x = 5/4 千米。\n因此，家到学校的距离是学校到家的距离的百分之几，可以通过求比值得到：x / (5/4)x = 4/5 = 0.8，即小明从家到学校的距离是学校到家的距离的百分之80。"}]}
```
## Training   
>1. A Few lines are added to *train.py* to record training time and GPU utilization. While the regular training parameters can be modified in *run.sh*  
```python
# under main() function
start_training = time.time()
# ...
gpu_info_cmd = "nvidia-smi > " + os.path.join(training_args.output_dir,'GPU_info.txt')
# ...
trainer.train(resume_from_checkpoint=None)
os.system(gpu_info_cmd)
if training_args.use_lora:
# ...
training_elapse = int( time.time() - start_training )
print_rank_0("training time = {} seconds".format(training_elapse), log_file, global_rank)
```
>2. model_name_or_path specifies the path of pre-trained model  
>3. *cutoff_len* is set as 512 instead of default 1024   

>Full parameter fine-tuning  
>1. *run_ft.sh* needs to be renamed as *run.sh* after parameter update   

>LoRA  
>1. *run_lora.sh* needs to be renamed as *run.sh* after parameter update  
>2. When LoRA is used, remember to overwrite *adapter_model.bin* with the content of *pytorch_model.bin* while keeping the name unchanged. Otherwise it is equivalent to inference using the original pre-trained model.
## Inference
>The previous *inference.py* only supports generating inference on hard-coded samples. We modified it with extra features.  
>1. randomly select specified number of samples for inference 
>2. perform inference on validation dataset and export as JSON
>3. adding ground true answers for comparison
>4. evaluate performance of pre-trained models like Bloom
```python
# specify the number of randomly select samples
parser.add_argument('--test_num', type=int, default=5)
# perform inference on all samples in validation dataset 
parser.add_argument('--save_log', action="store_true")
# specify the path of exported JSON file
parser.add_argument('--write_data')
# ...
with open(args.test_set) as f:
    lines = f.readlines()
    choose = [random.randint(1,len(lines)-1) for i in range(args.test_num)]
    # choose = [153, 953, 820]
    if args.save_log:
        # normal practice: first 1000 as validation dataset
        choose = [i for i in range(1000)] 
    for counter in choose:
        data = json.loads(lines[counter])
        entry = "Human: \n " + data['conversations'][0]["value"]
        entry += " \n\nAssistant:\n"
        # question, index, ground true answer
        instruction_list.append([entry, data["id"], data['conversations'][1]["value"]])
# ...
# below line is to check the performance of pre-trained model
# remember to comment out if trained model is being evaluated
model = AutoModelForCausalLM.from_pretrained(args.model_name_or_path, torch_dtype=load_type)
# ...
# After decode, the generated text is a combination of question and answer which requires separation
generate_text = tokenizer.decode(generation_output,skip_special_tokens=True)
if args.save_log:
    question = generate_text[generate_text.find("Human:")+6:generate_text.find("Assistant:")].strip()
    answer = generate_text[generate_text.find("Assistant:")+10:].strip()
    item = {"id":instruction[1], "question": question, "answer":answer, "groundTrue":instruction[2]}
    f_write.write(json.dumps(item, ensure_ascii=False)+"\n") 
```
```JSON
{"id": "dolly-1", "question": "Virgin Australia, the trading name of Virgin Australia Airlines Pty Ltd, is an Australian-based airline. It is the largest airline by fleet size to use the Virgin brand. It commenced services on 31 August 2000 as Virgin Blue, with two aircraft on a single route. It suddenly found itself as a major airline in Australia's domestic market after the collapse of Ansett Australia in September 2001. The airline has since grown to directly serve 32 cities in Australia, from hubs in Brisbane, Melbourne and Sydney. When did Virgin Australia start operating?", "answer": "Virgin Australia started operations on August 31st, 2000", "groundTrue": "Virgin Australia commenced services on 31 August 2000 as Virgin Blue, with two aircraft on a single route."}
{"id": "dolly-2", "question": "Which is a species of fish? Tope or Rope", "answer": "Tope", "groundTrue": "Tope"}
```
under *inference.sh*, we may set CUDA_VISIBLE_DEVICES=1 as the id of idle GPU
## Interface  
>1. When encountered *ImportError: /lib64/libstdc++.so.6: version `GLIBCXX_3.4.29' not found*, we may check the associated Python library and rollback to previous version.
