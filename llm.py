from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from transformers.generation.logits_process import InfNanRemoveLogitsProcessor
from transformers import LogitsProcessorList, LogitsProcessor
from transformers.utils import logging
import torch
import json
import os

class RestrictTokenLogitsProcessor(LogitsProcessor):
    def __init__(self, tokenizer, allowed_tokens):
        self.allowed_token_ids = tokenizer.convert_tokens_to_ids(allowed_tokens)

    def __call__(self, input_ids, scores):
        # Set logits of all tokens except the allowed ones to -inf
        forbidden_tokens_mask = torch.ones_like(scores).bool()
        forbidden_tokens_mask[:, self.allowed_token_ids] = False
        scores[forbidden_tokens_mask] = float('-inf')
        return scores
    
def set_tokenizer(tokenizer):
    # Set special tokens if they are not set
    if tokenizer.unk_token is None:
        tokenizer.add_special_tokens({'unk_token': '[UNK]'})
    if tokenizer.sep_token is None:
        tokenizer.add_special_tokens({'sep_token': '[SEP]'})
    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    if tokenizer.cls_token is None:
        tokenizer.add_special_tokens({'cls_token': '[CLS]'})
    if tokenizer.mask_token is None:
        tokenizer.add_special_tokens({'mask_token': '[MASK]'})
    
def load_model(model_name, model_ckpts=None, load_in_8bit=False):
    if model_name == "llama-2-13b":
        model_path = "meta-llama/Llama-2-13b-chat-hf"
    elif model_name == "llama-2-7b":
        model_path = "meta-llama/Llama-2-7b-chat-hf"
    elif model_name == "llama-3-8b":
        model_path = "meta-llama/Meta-Llama-3-8B-Instruct"
    elif model_name == "llama-3-70b":
        model_path = "meta-llama/Meta-Llama-3-70B-Instruct"
    elif model_name == "llama-3.1-8b":
        model_path = "meta-llama/Meta-Llama-3.1-8B-Instruct"
    elif model_name == "llama-3.1-70b":
        model_path = "meta-llama/Meta-Llama-3.1-70B-Instruct"
    elif model_name == "mistral-7b":
        model_path = "mistralai/Mistral-7B-Instruct-v0.2"
    elif model_name == "gemma-9b":
        model_path = "google/gemma-2-9b-it"

    tokenizer_path = model_path
    if model_ckpts:
        model_path = model_ckpts

    if load_in_8bit:
        quantization_config = BitsAndBytesConfig(load_in_8bit=True)
        model = AutoModelForCausalLM.from_pretrained(
        model_path, device_map="auto", torch_dtype=torch.float16, quantization_config=quantization_config)
    else:
        model = AutoModelForCausalLM.from_pretrained(model_path, low_cpu_mem_usage=True, torch_dtype=torch.float16, device_map="auto")

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    return model, tokenizer

def llama_chat2(chat, tokenizer, model, max_new_tokens=512, output_scores=False, processors=None, temperature=1.0):
    chat_tokens = tokenizer.apply_chat_template(chat, tokenize=True, return_tensors='pt').to("cuda")
    # chat_tokens = tokenizer.apply_chat_template(chat, tokenize=True, return_tensors='pt').to(model.device)
    outputs = model.generate(chat_tokens, logits_processor=processors, do_sample=True, max_new_tokens=max_new_tokens, return_dict_in_generate=True, output_scores=output_scores, pad_token_id=tokenizer.eos_token_id)
    new_chat_str = tokenizer.decode(outputs.sequences[0])

    index = 0
    while new_chat_str.split("<|eot_id|>")[-2].strip() == "":
        outputs = model.generate(chat_tokens, logits_processor=processors, do_sample=True, max_new_tokens=max_new_tokens, return_dict_in_generate=True, output_scores=output_scores, pad_token_id=tokenizer.eos_token_id)
        new_chat_str = tokenizer.decode(outputs.sequences[0])
        index += 1
        if index > 4:
            break
    return outputs, new_chat_str

def llama_chat(chat, tokenizer, model, max_new_tokens=512, output_scores=False, processors=None, temperature=1.0):
    chat_tokens = tokenizer.apply_chat_template(chat, tokenize=True, return_tensors='pt').to("cuda")
    # chat_tokens = tokenizer.apply_chat_template(chat, tokenize=True, return_tensors='pt').to(model.device)
    outputs = model.generate(chat_tokens, logits_processor=processors, do_sample=True, max_new_tokens=max_new_tokens, return_dict_in_generate=True, output_scores=output_scores, pad_token_id=tokenizer.eos_token_id)
    new_chat_str = tokenizer.decode(outputs.sequences[0])

    return outputs, new_chat_str

def get_response(output, model_name="llama-3"):
    if "llama-3" in model_name:
        # additional check
        if "<|start_header_id|>" in output.split("<|end_header_id|>")[-1]:
            response = output.split("<|start_header_id|>")[-1].split("<|eot_id|>")[0].strip()
        else:
            # This is original 
            response = output.split("<|end_header_id|>")[-1].split("<|eot_id|>")[0].strip()
    elif "llama-2" in model_name:
        response = output.split('[/INST]')[-1].split("</s>")[0].strip()
    return response


def get_response_org(output, model_name="llama-3"):
    if "llama-3" in model_name:
        response = output.split("<|end_header_id|>")[-1].split("<|eot_id|>")[0].strip()
    elif "llama-2" in model_name:
        response = output.split('[/INST]')[-1].split("</s>")[0].strip()
    return response

def insert_string(sent, y):
    sent_list = sent.split("\n\n")
    sent_list[0] += y
    # Join the sentences back into a single string
    result = '\n\n'.join(sent_list)
    return result

def append_dict_to_json_file(dict_data, file_path):
    # Check if the file exists and is not empty
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        # Read the existing data
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Ensure data is a list
            if not isinstance(data, list):
                data = []
    else:
        data = []
    # Add new dictionary to list
    data.append(dict_data)
    # Write back to file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def load_json_file(file_path):
    # Check if the file exists and is not empty
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        # Read the existing data
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Ensure data is a list
            if not isinstance(data, list):
                data = []
    else:
        data = []
    return data
