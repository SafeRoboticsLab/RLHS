import torch
import random
import copy
import itertools
from llm import RestrictTokenLogitsProcessor, set_tokenizer, load_model, llama_chat, get_response, insert_string
from prompt_manager import generate_purchase_item_prompt, get_wm_system_prompt
from transformers.utils import logging
from transformers import LogitsProcessorList, LogitsProcessor
from transformers.generation.logits_process import InfNanRemoveLogitsProcessor
from abc import ABC, abstractmethod


class ChatBot(ABC):

    @property
    @abstractmethod
    def all_prompts(self) -> dict[str, str]:
        """Dictionary that holds every prompt string the bot needs."""
        ...

    @property
    @abstractmethod
    def label(self):
        """Label chosen from 'Store', 'Service'"""
        ...


    def __init__(self, chat_model_name, human_model_name, use_world_model=False, chat_model=None, chat_tokenizer=None, human_model=None, human_tokenizer=None):

        chat_model, chat_tokenizer = (chat_model, chat_tokenizer) if chat_model and chat_tokenizer else load_model(chat_model_name)
        human_model, human_tokenizer = (human_model, human_tokenizer) if human_model and human_tokenizer else load_model(human_model_name)
        logging.get_logger("transformers").setLevel(logging.ERROR)
        
        self.model = chat_model
        self.tokenizer = chat_tokenizer
        self.model_name = chat_model_name
        
        self.human_model = human_model
        self.human_tokenizer = human_tokenizer
        self.human_model_name = human_model_name

        self.use_world_model = use_world_model

        # prompts
        self.init_prompt()

    def init_prompt(self):
        # all_prompts = get_all_prompts()
        all_prompts = self.all_prompts
        self.pref_prompt = all_prompts["pref_prompt"]
        self.final_pref_prompt = all_prompts["final_pref_prompt"]
        self.decision_pref_prompt = all_prompts["decision_pref_prompt"]
        self.final_decision_pref_prompt = all_prompts["final_decision_pref_prompt"]
        self.purchase_review_prompt = all_prompts["purchase_review_prompt"]
        self.no_purchase_review_prompt = all_prompts["no_purchase_review_prompt"]
        self.feedback = all_prompts["feedback_prompt"]

        self.item_choice_prompt = all_prompts["item_choice_prompt"]
        self.final_item_choice_prompt = all_prompts["final_item_choice_prompt"]
        self.satisfaction_prompt = all_prompts["satisfaction_prompt"]
        self.final_satisfaction_prompt = all_prompts["final_satisfaction_prompt"]
        self.decision_satisfaction_prompt = all_prompts["decision_satisfaction_prompt"]

        self.decision_satisfaction_prompt = all_prompts["decision_satisfaction_prompt"]
        self.wm_prompt_template = all_prompts["wm_prompt_template"]

        
    def get_customer_single_response(self, customer_chat, prompt):
        customer_chat = copy.deepcopy(customer_chat)
        customer_chat.append({"role": "user", "content": prompt})
        _, output = llama_chat(customer_chat, self.human_tokenizer, self.human_model)
        response = get_response(output, self.human_model_name)
        customer_chat.append({"role": "assistant", "content": response})
        return response, customer_chat
        
    def get_customer_response(self, customer_chat, ai_chat):
        ai_chat = copy.deepcopy(ai_chat)
        customer_chat = copy.deepcopy(customer_chat)
        _, output = llama_chat(customer_chat, self.human_tokenizer, self.human_model)
        response = get_response(output, self.human_model_name)
        ai_chat.append({"role": "user", "content": response})
        customer_chat.append({"role": "assistant", "content": response})
        return response, ai_chat, customer_chat

    def get_ai_response(self, customer_chat, ai_chat):
        ai_chat = copy.deepcopy(ai_chat)
        customer_chat = copy.deepcopy(customer_chat)
        _, output = llama_chat(ai_chat, self.tokenizer, self.model)
        response = get_response(output, self.model_name)
        response += "\n\n" + self.item_choice_prompt
        ai_chat.append({"role": "assistant", "content": response})
        customer_chat.append({"role": "user", "content": response})
        return response, ai_chat, customer_chat

    def get_ai_response2(self, customer_chat, ai_chat):
        ai_chat = copy.deepcopy(ai_chat)
        customer_chat = copy.deepcopy(customer_chat)
        _, output = llama_chat(ai_chat, self.tokenizer, self.model)
        response = get_response(output, self.model_name)
        ai_chat.append({"role": "assistant", "content": response})
        customer_chat.append({"role": "user", "content": response})
        return response, ai_chat, customer_chat

    def mcqa_choice(self, outputs, all_tokens=['A', 'B', 'C', 'D']):
        last_token_logits = outputs.scores[-1].detach().cpu()
        probs = torch.softmax(last_token_logits, dim=-1)
        allowed_token_ids = self.human_tokenizer.convert_tokens_to_ids(all_tokens)
        # Extract probabilities for allowed token ids
        choice_probs = probs[0, allowed_token_ids]
        # Get the index of the maximum probability token
        max_index = torch.argmax(choice_probs)
        return all_tokens[max_index]

    def get_logit_processor(self, allowed_tokens):
        allowed_token_ids = self.human_tokenizer.convert_tokens_to_ids(allowed_tokens)
        processors = LogitsProcessorList([
            RestrictTokenLogitsProcessor(self.human_tokenizer, allowed_tokens),
            InfNanRemoveLogitsProcessor()  # Removes inf/nan values to prevent errors during generation
        ])
        return processors

    def get_final_choice(self, customer_chat, final_choice_prompt, allowed_tokens=['A', 'B', 'C', 'D']):
        processors = self.get_logit_processor(allowed_tokens)
        new_customer_chat = customer_chat.copy()
        new_customer_chat.append({"role": "user", "content": final_choice_prompt})
        chat_tokens = self.human_tokenizer.apply_chat_template(new_customer_chat, tokenize=False)
        if "llama-3" in self.human_model_name: assist_str = "<|start_header_id|>assistant<|end_header_id|> "
        if "llama-2" in self.human_model_name: assist_str = "<s>[INST] "
        chat_tokens += assist_str
        inputs = self.human_tokenizer([chat_tokens], return_tensors="pt").to(self.human_model.device)
        outputs = self.human_model.generate(**inputs, logits_processor=processors, do_sample=True, max_new_tokens=1, 
                                            return_dict_in_generate=True, output_scores=True, pad_token_id=self.human_tokenizer.eos_token_id)
        choice = self.mcqa_choice(outputs, allowed_tokens)
        return choice

    def get_final_pref(self, dialog, eval_aspect="service"):
        instruction = [
          {"role": "user", "content": dialog},
        ]
        _, output = llama_chat(instruction, self.human_tokenizer, self.human_model)
        reason = get_response(output, self.human_model_name)
        instruction.append({"role": "assistant", "content": reason})
        pref_prompt = self.final_pref_prompt if eval_aspect=="service" else self.final_decision_pref_prompt
        pref = self.get_final_choice(instruction, pref_prompt, allowed_tokens=['1', '2'])
        return reason, pref

    def get_satisfaction(self, customer_chat):
        customer_extend_chat = copy.deepcopy(customer_chat)
        if customer_extend_chat[-1]["role"] == "user":
            customer_extend_chat[-1]["content"] += "\n" + self.satisfaction_prompt
        else:
            customer_extend_chat.append({"role": "user", "content": self.satisfaction_prompt})
        _, output = llama_chat(customer_extend_chat, self.human_tokenizer, self.human_model)
        reason = get_response(output, self.human_model_name)
        customer_extend_chat.append({"role": "assistant", "content": reason})
        pref_prompt = self.final_satisfaction_prompt
        rate = self.get_final_choice(customer_extend_chat, pref_prompt, allowed_tokens=['1', '2', '3', '4', '5'])
        return reason, rate

    def get_decision_satisfaction(self, customer_chat):
        customer_extend_chat = copy.deepcopy(customer_chat)
        if customer_extend_chat[-1]["role"] == "user":
            customer_extend_chat[-1]["content"] += "\n" + self.decision_satisfaction_prompt
        else:
            customer_extend_chat.append({"role": "user", "content": self.decision_satisfaction_prompt})
        _, output = llama_chat(customer_extend_chat, self.human_tokenizer, self.human_model)
        reason = get_response(output, self.human_model_name)
        customer_extend_chat.append({"role": "assistant", "content": reason})
        pref_prompt = self.final_satisfaction_prompt
        rate = self.get_final_choice(customer_extend_chat, pref_prompt, allowed_tokens=['1', '2', '3', '4', '5'])
        return reason, rate

    @abstractmethod
    def get_initial_chat(self, ai_prompt, customer_prompt):
        ...
        
    
    def get_further_chat(self, ai_chat, customer_chat):
        ai_chat = copy.deepcopy(ai_chat)
        customer_chat = copy.deepcopy(customer_chat)
        ai_response1, ai_chat1, customer_chat1 = self.get_ai_response(customer_chat, ai_chat)
        final_choice_explain1, ai_chat1, customer_chat1 = self.get_customer_response(customer_chat1, ai_chat1)
        choice1 = self.get_final_choice(customer_chat1, self.final_item_choice_prompt)
        return choice1, ai_chat1, customer_chat1
    
    def get_human_ai_chat(self, ai_prompt, customer_prompt):
        
        ai_chat, customer_chat = self.get_initial_chat(ai_prompt, customer_prompt)
        ai_response1, ai_chat1, customer_chat1 = self.get_ai_response(customer_chat, ai_chat)
        final_choice_explain1, ai_chat1, customer_chat1 = self.get_customer_response(customer_chat1, ai_chat1)
        choice1 = self.get_final_choice(customer_chat1, self.final_item_choice_prompt)

        return choice1, ai_chat1, customer_chat1
    
    def get_human_ai_chat_two(self, ai_prompt, customer_prompt):
        
        ai_chat, customer_chat = self.get_initial_chat(ai_prompt, customer_prompt)
        
        new_ai_chat = copy.deepcopy(ai_chat)
        sys_prompt = new_ai_chat[0]['content']
        
        choice1, ai_chat1, customer_chat1 = self.get_further_chat(ai_chat, customer_chat)
        choice2, ai_chat2, customer_chat2 = self.get_further_chat(new_ai_chat, customer_chat)
        return choice1, ai_chat1, customer_chat1, choice2, ai_chat2, customer_chat2

    def convert_chat(self, chat, role="ai"):
        dialog = ""
        for item in chat:
            if item["role"] == "system":
                dialog = item["content"].strip()    
            if item["role"] == "user":
                name = "Human: " if role == "ai" else "AI: "
                dialog += "\n\n" + name + item["content"]
            elif item["role"] == "assistant":
                name = "AI: " if role == "ai" else "Human: "
                dialog += "\n\n" + name + item["content"]
        return dialog
    
    def construct_two_dialogs(self, human_pref_chat, human_chat, human_chat2):
        label = self.label
        dialog = human_pref_chat
        dialog += "\n\n" + f"{label} 1:"
        for item in human_chat:
            if item["role"] == "user":
                dialog += "\n" + "AI: " + item["content"]
            elif item["role"] == "assistant":
                dialog += "\n" + "Human: " + item["content"]
        dialog += "\n\n" + f"{label} 2:"
        for item in human_chat2:
            if item["role"] == "user":
                dialog += "\n" + "AI: " + item["content"]
            elif item["role"] == "assistant":
                dialog += "\n" + "Human: " + item["content"]
        dialog += "\n\n" + self.pref_prompt
        return dialog
    
    def construct_two_reviews(self, human_pref_chat, human_chat, human_chat2):
        label = self.label
        dialog = human_pref_chat
        dialog += "\n\n" + f"Customer review for {label} 1: {human_chat[-1]['content']}"
        dialog += "\n\n" + f"Customer review for {label} 2: {human_chat2[-1]['content']}"
        dialog += "\n\n" + self.pref_prompt
        return dialog
    
    def construct_two_decisions(self, human_pref_chat, decision1, decision2):
        label = self.label
        dialog = human_pref_chat
        dialog += "\n\n" + f"In {label} 1: {decision1}"
        dialog += "\n\n" + f"In {label} 2: {decision2}"
        dialog += "\n\n" + self.decision_pref_prompt
        return dialog
    
    def get_customer_review(self, customer_chat, info, choice):
        review_prompt = generate_purchase_item_prompt(self.purchase_review_prompt, self.no_purchase_review_prompt, info, choice)
        review_prompt += self.feedback_prompt
        response, customer_extend_chat = self.get_customer_single_response(customer_chat, review_prompt)
        return response, customer_extend_chat


    @abstractmethod
    def get_wm_simulation(self, wm_prompt: str, choice: str) -> str:
        """
        Simulate the world-model outcome after the customer makes `choice`.
        Concrete subclasses *must* supply an implementation.
        """
        ...
    
    def update_customer_state_partial(self, customer_chat, info, item, choice):

        if not self.use_world_model:
            review_prompt = generate_purchase_item_prompt(self.purchase_review_prompt, self.no_purchase_review_prompt, info, choice)
        else:

            wm_prompt = get_wm_system_prompt(self.wm_prompt_template, item, info)
            review_prompt = self.get_wm_simulation(wm_prompt, choice)

        customer_extend_chat = copy.deepcopy(customer_chat)
        customer_extend_chat.append({"role": "user", "content": review_prompt})
        return customer_extend_chat 

    
    def update_customer_state_full(self, customer_chat, info, choice, human_review_prompt):
        customer_extend_chat = copy.deepcopy(customer_chat)
        review_prompt = generate_purchase_item_prompt(self.purchase_review_prompt, self.no_purchase_review_prompt, info, choice)
        final_prompt = review_prompt + human_review_prompt
        customer_extend_chat.append({"role": "user", "content": final_prompt})
        return customer_extend_chat
