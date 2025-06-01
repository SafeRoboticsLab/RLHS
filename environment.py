import torch
import random
import copy
import itertools
from llm import RestrictTokenLogitsProcessor, set_tokenizer, load_model, llama_chat, get_response, insert_string, append_dict_to_json_file, load_json_file
from prompt_manager import sample_prices, get_final_feature_prompt, get_ai_option_prompt, get_ai_prompt, get_customer_prompt, generate_purchase_item_prompt, get_final_review_prompt, get_wm_system_prompt
import pdb
from abc import ABC, abstractmethod
import numpy as np


class BaseEnv(ABC):

    # ----- “abstract data” -----
    @property
    @abstractmethod
    def items(self) -> dict[str, list[tuple[str, str, str]]]:
        """Dictionary that describes feature triplets for each category."""
        ...

    @property
    @abstractmethod
    def prices(self) -> dict[str, list[tuple[int, int]]]:
        """Dictionary of price ranges (min,max) for each category."""
        ...

    @property
    @abstractmethod
    def all_prompts(self) -> dict[str, str]:
        """Dictionary that holds every prompt string the bot needs."""
        ...

    def __init__(self, chatbots=None):
        self.chatbots = chatbots
        self.init_prompt()
        self.all_cases = self.init_all_cases()


    def init_all_cases(self):
        # values = [-1, 0]
        values = [-1, 0, 1]
        neg_cases = list(itertools.product(values, repeat=3))
        price_req_cases = [(1, 0, 0), (0, 1, 0), (1, 1, 0), (1, 1, 1)]
        no_price_cases = [(1, 1, -1), (1, 1, 0), (1, 1, 1)]
        all_cases = {"neg_cases": neg_cases, "price_req_cases": price_req_cases, "no_price_cases": no_price_cases}
        return all_cases

    def init_prompt(self):
        all_prompts = self.all_prompts
        self.pref_prompt = all_prompts["pref_prompt"]
        self.final_pref_prompt = all_prompts["final_pref_prompt"]
        self.decision_pref_prompt = all_prompts["decision_pref_prompt"]
        self.final_decision_pref_prompt = all_prompts["final_decision_pref_prompt"]
        self.purchase_review_prompt = all_prompts["purchase_review_prompt"]
        self.no_purchase_review_prompt = all_prompts["no_purchase_review_prompt"]
        self.feedback = all_prompts["feedback_prompt"]

        self.human_pref_prompt_template = all_prompts["human_pref_prompt_template"]
        self.human_prompt_template = all_prompts["human_prompt_template"]
        self.price_prompt = all_prompts["price_prompt"]
        self.ai_prompt_template = all_prompts["ai_prompt_template"]
        self.item_choice_prompt = all_prompts["item_choice_prompt"]
        self.final_item_choice_prompt = all_prompts["final_item_choice_prompt"]
        self.final_review_prompt_template = all_prompts["final_review_prompt_template"]
        self.satisfaction_prompt = all_prompts["satisfaction_prompt"]
        self.final_satisfaction_prompt = all_prompts["final_satisfaction_prompt"]

    def true_reward(self, case_name, all_prices, price, cases, case):
        if case != 1:
            return -1 

        if case_name == "neg_cases":
            return -1
        else:
            cheapest = np.min([all_prices[j] for j in range(len(cases)) if cases[j] == 1])
            return cheapest / price

    def generate_scenarios(self):
        option_lists = ['A', 'B', 'C']
        all_results = []
        for item in self.items:
            all_features = self.items[item]
            price_ranges = self.prices[item]
            for j in range(len(all_features)):
                feature_tuple = all_features[j]
                for case_name in self.all_cases:
                    cases = self.all_cases[case_name]
                    for case in cases:
                        human_prompt_template_new = self.human_prompt_template
                        human_pref_prompt_template_new = self.human_pref_prompt_template
                        lowest_price_req = False
                        if case_name == "price_req_cases" or case_name == "no_price_cases":
                            lowest_price_req = True
                            human_prompt_template_new = self.human_prompt_template + " " + self.price_prompt
                            human_pref_prompt_template_new = self.human_pref_prompt_template + " " + self.price_prompt

                        all_prices = sample_prices(price_ranges)
                        random.shuffle(option_lists)
                        all_info_dict = {}
                        for i in range(len(all_prices)):
                            if case[i] == -1:
                                feature = feature_tuple[1]
                            elif case[i] == 1:
                                feature = feature_tuple[0]
                            else:
                                feature = feature_tuple[2]
                            other_features = [random.choice(all_features[k][:2]) for k in range(len(all_features)) if k != j]
                            lowest_price = True if i == 2 else False
                            price_rank = i + 1
                            # prev_reward = self.prev_reward(case[i], price_rank, lowest_price_req)
                            reward = self.true_reward(case_name, all_prices, all_prices[i], case, case[i])

                            is_price_aval = not (case_name == "no_price_cases")
                            dict_example = {
                                "price": all_prices[i],
                                "feature": feature,
                                "other_features": other_features,
                                "case": case[i],
                                "price_rank": price_rank,
                                "req_feature": feature_tuple[0],
                                "bad_feature": feature_tuple[1],
                                "reward": reward,
                                "is_price_aval": is_price_aval
                            }
                            all_info_dict[option_lists[i]] = dict_example

                        ai_prompt = get_ai_prompt(self.ai_prompt_template, item, all_info_dict)
                        customer_prompt = get_customer_prompt(human_prompt_template_new, item, all_info_dict, feature_tuple[0])
                        customer_pref_prompt = get_customer_prompt(human_pref_prompt_template_new, item, all_info_dict, feature_tuple[0])
                        human_review_prompt = get_final_review_prompt(self.final_review_prompt_template, all_info_dict)

                        results = {}
                        results["option_info"] = all_info_dict
                        results["case_name"] = case_name
                        results["all_cases"] = case
                        results["lowest_price_req"] = lowest_price_req
                        results["item"] = item

                        results["ai_prompt"] = ai_prompt
                        results["human_prompt"] = customer_prompt
                        results["human_pref_prompt"] = customer_pref_prompt
                        results["human_review_prompt"] = human_review_prompt

                        ai_chat, customer_chat = self.chatbots.get_initial_chat(ai_prompt, customer_prompt)
                        results["ai_chat"] = ai_chat
                        results["human_chat"] = customer_chat

                        all_results.append(results)
                        return all_results

        return all_results


    def get_sample_dict(self, ai_response, ai_chat, customer_chat, choice=None):
        sample_dict = {}
        sample_dict["response"] = ai_response
        sample_dict["ai_chat"] = ai_chat
        sample_dict["customer_chat"] = customer_chat
        sample_dict["choice"] = choice
        return sample_dict


    def generate_test_data(self, all_results, output_path=None, ckpts_list=None, rlhf_type=['base', 'phs', 'fhs', 'phs_v0', 'fhs_v0']):
        '''
        This is for test time inference.
        '''
        # rlhf_type: "all", "base", "phs", "fhs"
        iters = 0
        init_chatbot = self.chatbots[0]
        options = ["A", "B", "C"]

        for results in all_results:
            iters += 1

            all_cases = results["all_cases"]
            info = results["option_info"]
            print("#######################")
            print(f"Iters: {iters}, {results['item']}: {info['A']['req_feature']}, Case name: {results['case_name']}, Cases: {all_cases}")
            ai_prompt = results['ai_prompt'] 
            customer_prompt = results['human_prompt'] 
            human_pref_chat = results["human_pref_prompt"]
            human_review_prompt = results["human_review_prompt"]
            case_name = results["case_name"]
            if "ai_chat" in results and "human_chat" in results:
                init_ai_chat, init_customer_chat = results["ai_chat"], results["human_chat"]
            else:
                init_ai_chat, init_customer_chat = init_chatbot.get_initial_chat(ai_prompt, customer_prompt)
                results["ai_chat"] = init_ai_chat
                results["human_chat"] = init_customer_chat

            total_iter = 0
            for i in range(len(self.chatbots)):
                chatbot = self.chatbots[i]

                # Check if we need to recompute the dictionary
                create_new_dict = False
                model_name = chatbot.model_name
                model_results = results.get(model_name)
                if model_results is None:
                    results[model_name] = {}
                    create_new_dict = True
                elif ckpts_list:
                    sample_dict = model_results.get(ckpts_list[i])
                    create_new_dict = sample_dict is None
                else:
                    sample_dict = model_results
                
                if create_new_dict:
                    choice, ai_chat, customer_chat = chatbot.get_further_chat(init_ai_chat, init_customer_chat)
                    ai_response = "\n\n".join(ai_chat[-2]['content'].split("\n\n")[:-1])
                    sample_dict = self.get_sample_dict(ai_response, ai_chat, customer_chat, choice)
                    if ckpts_list:
                        results[model_name][ckpts_list[i]] = sample_dict

                # Use for RLHF or RLHS
                choice = sample_dict["choice"]
                customer_chat = sample_dict["customer_chat"]

                if "base" in rlhf_type:
                    reason, rating = chatbot.get_satisfaction(customer_chat)
                    sample_dict["initial_reason"] = reason
                    sample_dict["initial_rating"] = rating

                if "phs" in rlhf_type:
                    # Partial Hindsight simulation enabled
                    customer_extend_chat = chatbot.update_customer_state_partial(customer_chat, info, item, choice)
                    hs_reason, hs_rating = chatbot.get_satisfaction(customer_extend_chat)
                    sample_dict["phs_reason"] = hs_reason
                    sample_dict["phs_rating"] = hs_rating
                    
                if "fhs" in rlhf_type:
                    # Full Hindsight simulation enabled
                    customer_extend_chat_full = chatbot.update_customer_state_full(customer_chat, info, choice, human_review_prompt)
                    oracle_hs_reason, oracle_hs_rating = chatbot.get_satisfaction(customer_extend_chat_full)
                    sample_dict["fhs_reason"] = oracle_hs_reason
                    sample_dict["fhs_rating"] = oracle_hs_rating

            if output_path:
                append_dict_to_json_file(results, output_path)
        return all_results


    def generate_rlhf_data(self, all_results, output_path=None, final_output_path=None, thres=15):
        '''
        This is for generating RLHF data.
        '''
        options = ["A", "B", "C"]
        chatbot = self.chatbots[0] if isinstance(self.chatbots, list) else self.chatbots
        # load the last running checkpoint
        data = load_json_file(output_path)
        all_results[:len(data)] = data
        iters = len(data)

        for results in all_results[len(data):]:
            iters += 1
            all_cases = results["all_cases"]
            info = results["option_info"]
            print("#######################")
            print(f"Iters: {iters}, {results['item']}: {info['A']['req_feature']}, Case name: {results['case_name']}, Cases: {all_cases}")

            ai_prompt = results['ai_prompt'] 
            customer_prompt = results['human_prompt'] 
            human_pref_chat = results["human_pref_prompt"]
            human_review_prompt = results["human_review_prompt"]
            case_name = results["case_name"]
            init_ai_chat, init_customer_chat = chatbot.get_initial_chat(ai_prompt, customer_prompt)
            init_ai_chat1, init_ai_chat2 = init_ai_chat, copy.deepcopy(init_ai_chat)

            choice1, ai_chat1, customer_chat1 = chatbot.get_further_chat(init_ai_chat1, init_customer_chat)
            choice2, ai_chat2, customer_chat2 = chatbot.get_further_chat(init_ai_chat2, init_customer_chat)
            
            dialog = chatbot.construct_two_dialogs(human_pref_chat, customer_chat1, customer_chat2)
            reason, choice = chatbot.get_final_pref(dialog)
                
            if choice == "1":
                chosen_chat = ai_chat1
                reject_chat = ai_chat2
            if choice == "2":
                chosen_chat = ai_chat2
                reject_chat = ai_chat1
            
            chosen = "\n\n".join(chosen_chat[-2]['content'].split("\n\n")[:-1])
            reject = "\n\n".join(reject_chat[-2]['content'].split("\n\n")[:-1])
            
            # RLHF
            results["dialog"] = ai_chat1[:2]
            results["chosen"] = chosen
            results["reject"] = reject
            
            # Log AI and customer responses
            results["ai_chat_1"] = ai_chat1
            results["ai_chat_2"] = ai_chat2
            results["human_chat_1"] = customer_chat1
            results["human_chat_2"] = customer_chat2
            results["choice_1"] = choice1
            results["choice_2"] = choice2
            
            # Preference
            results["pref_eval_prompt"] = dialog
            results["pref_reason"] = reason
            results["pref_choice"] = choice
            
            
            # partial hindsight
            customer_extend_chat1 = chatbot.update_customer_state_partial(customer_chat1, info, results["item"], choice1)
            customer_extend_chat2 = chatbot.update_customer_state_partial(customer_chat2, info, results["item"], choice2)

            dialog2 = chatbot.construct_two_dialogs(human_pref_chat, customer_extend_chat1, customer_extend_chat2)
            final_reason2, final_choice2 = chatbot.get_final_pref(dialog2) 
            part_state_1, part_state_2 = customer_extend_chat1[-1]["content"], customer_extend_chat2[-1]["content"]
            results["partial_hindsight_eval_prompt"] = dialog2
            results["partial_hindsight_reason"] = final_reason2
            results["partial_hindsight_choice"] = final_choice2
            results["partial_hindsight_state_1"] = part_state_1
            results["partial_hindsight_state_2"] = part_state_2
            
            # Full hindsight
            customer_full_chat1 = chatbot.update_customer_state_full(customer_chat1, info, choice1, human_review_prompt)
            customer_full_chat2 = chatbot.update_customer_state_full(customer_chat2, info, choice2, human_review_prompt)
            dialog3 = chatbot.construct_two_dialogs(human_pref_chat, customer_full_chat1, customer_full_chat2)
            final_reason3, final_choice3 = chatbot.get_final_pref(dialog3)
            full_state_1, full_state_2 = customer_full_chat1[-1]["content"], customer_full_chat2[-1]["content"]
            results["full_hindsight_eval_prompt"] = dialog3
            results["full_hindsight_reason"] = final_reason3
            results["full_hindsight_choice"] = final_choice3
            results["full_hindsight_state_1"] = full_state_1
            results["full_hindsight_state_2"] = full_state_2

            if output_path:
                append_dict_to_json_file(results, output_path)
        
        return all_results