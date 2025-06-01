from prompt import get_all_prompts
from chatbot import ChatBot


class MarketplaceChatBot(ChatBot):

    all_prompts = get_all_prompts()
    label = "Store"
    
    def get_initial_chat(self, ai_prompt, customer_prompt):
        ai_chat = [
          {"role": "system", "content": ai_prompt},
        ]
        customer_chat = [
          {"role": "system", "content": customer_prompt},
          {"role": "user", "content": "Hello! Welcome to our online shopping platform. How can I help you?"},
        ]
        customer_response, ai_chat, customer_chat = self.get_customer_response(customer_chat, ai_chat)
        return ai_chat, customer_chat
    

    def get_wm_simulation(self, wm_prompt, choice):

        choice_to_words =  {"A": "Customer bought Option A", "B": "Customer bought Option B", "C": "Customer bought Option C", "D": "Customer decided to not buy anything."}

        chat = [
          {"role": "system", "content": wm_prompt},
          {"role": "user", "content": f"{choice_to_words[choice]}. Describe the customer's outcome after receiving the item, if they made a purchase."},
        ]

        # Can choose either strong or weaker model for simulation
        _, output = llama_chat(chat, self.tokenizer, self.human_model)
        # _, output = llama_chat(chat, self.tokenizer, self.model)
        response = get_response(output, self.model_name)

        return response