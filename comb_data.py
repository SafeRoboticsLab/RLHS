import json
import os
import random
import argparse

def load_all_json_with_substring(directory, substring):
    # List all files in the directory
    files = os.listdir(directory)
    
    # Filter files that contain the substring
    target_files = [f for f in files if substring in f]
    
    # Load and aggregate the JSON data from all matching files
    all_data = []
    for file_name in target_files:
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'r') as file:
            data = json.load(file)
        all_data.extend(data)
    
    return all_data

def write_json(data, output_file):
    with open(output_file, 'w') as file:
        json.dump(data, file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Support model: llama-2-7b, llama-2-13b, llama-3-8b, llama-3-70b
    parser.add_argument('--directory', default='./final_data/llama-2-7b')
    parser.add_argument('--substring', default='results_llama-2-7b_llama-3-70b')
    parser.add_argument('--rlhf_data_file', default='llama-2-7b-pref.json')

    args = parser.parse_args()

    data = load_all_json_with_substring(args.directory, args.substring)
    random.shuffle(data)
    path = f"{args.directory}/{args.substring}.json"
    write_json(data, path)

    for data in dataset:
        dialog = data["dialog"]
        data_dict = {}
        conversations = []
        for chat in dialog:
            if chat["role"] == "system":
                item = {"from": "system", "value": chat["content"]}
            elif chat["role"] == "user":
                item = {"from": "human", "value": chat["content"]}
            conversations.append(item)
        data_dict["conversations"] = conversations
        data_dict["chosen"] = {"from": "gpt", "value": data["chosen"]}
        data_dict["rejected"] = {"from": "gpt", "value": data["reject"]}
        rlhf_dataset.append(data_dict)

    final_path = f'{args.directory}/{args.rlhf_data_file}'
    write_json(rlhf_dataset, final_path)