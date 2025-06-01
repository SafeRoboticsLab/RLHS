from prompt import get_all_prompts
from chatbot import ChatBot


class OnlineCourseChatBot(ChatBot):

    all_prompts = get_all_prompts()
    label = "Service"
    
    def get_initial_chat(self, ai_prompt, customer_prompt):
        ai_chat = [
          {"role": "system", "content": ai_prompt},
        ]
        customer_chat = [
          {"role": "system", "content": customer_prompt},
          {"role": "user", "content": "Hello! Welcome to our course recommendation service. How can I help you?"},
        ]
        customer_response, ai_chat, customer_chat = self.get_customer_response(customer_chat, ai_chat)
        return ai_chat, customer_chat
    

    def get_wm_simulation(self, wm_prompt, choice):

        choice_to_words =  {"A": "Customer selected Option A", "B": "Customer selected Option B", "C": "Customer selected Option C", "D": "Customer decided not to enroll in any course"}

        chat = [
          {"role": "system", "content": wm_prompt},
          {"role": "user", "content": f"{choice_to_words[choice]}. Describe the customer's outcome after enrolling in and experiencing the online course they chose."},
        ]

        # Can choose either strong or weaker model for simulation
        _, output = llama_chat(chat, self.tokenizer, self.human_model)
        # _, output = llama_chat(chat, self.tokenizer, self.model)
        response = get_response(output, self.model_name)

        return response