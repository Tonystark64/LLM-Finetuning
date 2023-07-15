## Please modify parameters in evaluate_zh.sh
#### You may click [C-Eval Dataset](https://cevalbenchmark.com/index.html) and then click **submit** in the top menu bar.
## parameter list
> 1. shot: few-shot learning from 0 to 5  
> 2. gpu: gpu index
> 3. split: test or val  
> 4. model_id: model name  
> 5. task: ceval  
> 6. base_model: pre-trained model  
> 7. OPENMODEL_PATH: trained model  


### Evaluation Mode 1
> adding --use_base in bash file  
> evaluate on pre-trained model only
### Evaluation Mode 2
> evaluate on trained model  
> no --use_base added in bash file
### Hint:
> 1. The process is run under backend, log is generated as files  
> 2. In the generated files, **.json holds predicted answers**, *[model_name]_ceval_[split]_[shot]-shot_record.txt* holds the **log** where you may check the errors and results.txt holds the overall accuracy rate. When **results.txt** is generated, the process is over.      
> 3. You do not need to modify --OPENMODEL_PATH if --use_base is added in bash  
> 4. **If LoRA model is to be evaluated, please first combine the weights**
