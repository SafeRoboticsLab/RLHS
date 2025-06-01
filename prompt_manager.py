import random
import copy
import itertools

def sample_prices(price_ranges):
    all_prices = []
    for price_range in price_ranges:
        number = random.randint(price_range[0], price_range[1])
        all_prices.append(number)
    return all_prices

def get_final_feature_prompt(feature, other_features):
    final_prompt = feature + ", "    
    joint_other_feature_str = ", ".join(other_features)
    final_prompt += joint_other_feature_str
    return final_prompt

def get_ai_option_prompt(option, all_info):
    price_A, feature_A, other_features_A = all_info[option]['price'], all_info[option]['feature'], all_info[option]['other_features']
    price_A_prompt = f'${price_A}' if all_info[option]['is_price_aval'] else "None"
    final_A = get_final_feature_prompt(feature_A, other_features_A)
    final_A_prompt = final_A if all_info[option]['is_price_aval'] else f"${price_A}, {final_A}"
    return price_A_prompt, final_A_prompt

def get_ai_prompt(prompt_template, item_name, all_info):
    price_A_prompt, final_A = get_ai_option_prompt('A', all_info)
    price_B_prompt, final_B = get_ai_option_prompt('B', all_info)
    price_C_prompt, final_C = get_ai_option_prompt('C', all_info)
    
    prompt = prompt_template.format(item_name, price_A_prompt, price_B_prompt, price_C_prompt, final_A, final_B, final_C)
    prompt = prompt.replace(": None", "")
    return prompt

def get_customer_prompt(prompt_template, item_name, all_info, ideal_feature):
    price_A = all_info["A"]['price']
    price_B = all_info["B"]['price']
    price_C = all_info["C"]['price']
    
    price_A_prompt = f'${price_A}' if all_info["A"]['is_price_aval'] else "None"
    price_B_prompt = f'${price_B}' if all_info["B"]['is_price_aval'] else "None"
    price_C_prompt = f'${price_C}' if all_info["C"]['is_price_aval'] else "None"

    prompt = prompt_template.format(item_name, price_A_prompt, price_B_prompt, price_C_prompt, item_name, ideal_feature)
    prompt = prompt.replace(": None", "")
    return prompt  

def generate_purchase_item_prompt(purchase_review_prompt, no_purchase_review_prompt, info, choice):
    if choice == "D":
        return no_purchase_review_prompt
    choice_info = info[choice]
    word = "with" if choice_info["feature"] == choice_info["req_feature"] else "without"
    other_features = ", ".join(choice_info["other_features"])
    price = choice_info['price']
    user_review_prompt = purchase_review_prompt.format(choice, price, word, choice_info["req_feature"], other_features)
    return user_review_prompt


def comb_price_feature_prompt(all_info):
    price_A, feature_A, other_features_A = all_info["A"]['price'], all_info["A"]['feature'], all_info["A"]['other_features']
    price_B, feature_B, other_features_B = all_info["B"]['price'], all_info["B"]['feature'], all_info["B"]['other_features']
    price_C, feature_C, other_features_C = all_info["C"]['price'], all_info["C"]['feature'], all_info["C"]['other_features']
    
    if all_info["A"]["case"] == 0: feature_A = all_info["A"]['bad_feature']
    if all_info["B"]["case"] == 0: feature_B = all_info["B"]['bad_feature']
    if all_info["C"]["case"] == 0: feature_C = all_info["C"]['bad_feature']
    
    final_A_feature = get_final_feature_prompt(feature_A, other_features_A)
    final_B_feature = get_final_feature_prompt(feature_B, other_features_B)
    final_C_feature = get_final_feature_prompt(feature_C, other_features_C)
    
    final_A = f"${price_A}, {final_A_feature}"
    final_B = f"${price_B}, {final_B_feature}"
    final_C = f"${price_C}, {final_C_feature}"

    return final_A, final_B, final_C

def get_final_review_prompt(prompt_template, all_info):
    final_A, final_B, final_C = comb_price_feature_prompt(all_info)
    final_review_prompt = prompt_template.format(final_A, final_B, final_C)
    return final_review_prompt


def get_wm_system_prompt(prompt_template, item_name, all_info):
    final_A, final_B, final_C = comb_price_feature_prompt(all_info)
    wm_system_prompt = prompt_template.format(item_name, final_A, final_B, final_C)
    return wm_system_prompt