import argparse
import json
import datetime
import os

'''
{"question": "...", "human_answers":[...], "chatgpt_answers":[...], "source":"open_qa"}
{"instruction":"...", "context":"...", "response":"...", "category":"..."}
{"instruction":"...", "output":""}
'''

def main():
    
    # error_dict = ['我不知道', '我无法', 'sorry', '我不确定', '我不能']

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--orig_data",
    )
    parser.add_argument(
        "--write_data",
    )
    parser.add_argument(
        "--dataset_name",
    )
    args = parser.parse_args()
    f_write = open(args.write_data,"w")
    with open(args.orig_data) as f:
        lines = f.readlines()
        num_id = 1
        for line in lines:
            jump = False
            data = json.loads(line)
            if (len(data['output']) < 2):
                continue;
            try:
                if (len(data['instruction']) < 2):
                    continue
                '''
                for stop_word in error_dict:
                    if (stop_word in data['chatgpt_answers'][0]):
                        jump = True
                        break
                '''
            except TypeError:
                continue;
            if (jump): 
                continue
            conversations = [{"from": "human", "value": data['instruction']},{"from": "assistant", "value": data['output']}]
            # conversations = [{"from": "human", "value": data['input']},{"from": "assistant", "value": data['target']}]
            uniq_id = data['id'] if "id" in data else args.dataset_name+"-"+str(num_id)
            item = {"id":uniq_id, "conversations": conversations}
            f_write.write(json.dumps(item, ensure_ascii=False)+"\n")
            num_id += 1
    f_write.close()


if __name__ == "__main__":
    main()
