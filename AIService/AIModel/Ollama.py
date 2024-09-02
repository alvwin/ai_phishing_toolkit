import json
import os
import ollama
from datetime import datetime

from ..AIService import AIService
from const import Const

class Ollama(AIService):
    def __init__(self) -> None:
        super().__init__()

    def generate_prompt_linkedin(self, profile: str, posts: str, generation_option: str, payload_option: str, ai_option: str, template: str, payload_text: str = "", **kwargs):
        option = self._get_generation_option_linkedin(generation_option)
        prompts = self._get_prompt_json()
        payload = self._get_payload_option(payload_option)
        prompt = ""
        if ai_option == "Llama3 (local)":
            ai_option_c = "llama3"
        elif ai_option == "Mistral (local)":
            ai_option_c = "dolphin-mixtral:8x7b"
        print("Generating with " + ai_option_c)
        if option == "invalid":
            print("Invalid generation option")
            return
        if option == "probability":
            return self._api_call(self._generate_probability(profile, posts, prompts))
        prompt += f"{prompts['general']['linkedin']}"
        prompt += f"{self._generate_linkedin_profile_text(profile)}\n"
        prompt += f"{self._generate_linkedin_posts_text(posts)}\n"
        prompt += f"{prompts['general']['pretexts']}"
        prompt += f"{prompts['options'][option]['start']}"
        prompt += f"{prompts['options'][option]['rules']}"
        prompt += f"{prompts['general']['payload']}"
        if payload_option == 4:
            prompt += f"{payload_text}\n"
        else:
            prompt += f"{prompts['payloads'][payload]}"
        prompt += f"{prompts['general']['only']}"
        prompt += f"{prompts['general']['details']}"
        prompt += f"{prompts['general']['source']}"
        if template:
            prompt += f"{prompts['general']['template']}\n"
            prompt += f"{template}\n"
        prompt += f"Today is {datetime.now().strftime('%A, %B %d, %Y')}\n"
        return self._api_call(prompt, ai_option_c)
    
    def generate_prompt_twitter(self, profile: str, posts: str, generation_option: str, payload_option: str, ai_option: str, template: str, payload_text: str = "", **kwargs):
        option = self._get_generation_option_twitter(generation_option)
        prompts = self._get_prompt_json()
        payload = self._get_payload_option(payload_option, payload_text)
        if ai_option == "Llama3 (local)":
                ai_option_c = "llama3"
        elif ai_option == "Mistral (local)":
                ai_option_c = "dolphin-mixtral:8x7b"
        print("Generating with " + ai_option_c)
        prompt = ""
        if option == "invalid":
                print("Invalid generation option")
                return
        if option == "probability":
                return self._api_call(self._generate_probability(profile, prompts, posts))
        prompt += f"{prompts['general']['twitter']}"
        prompt += f"{self._generate_twitter_user_text(profile)}\n"
        prompt += f"{self._generate_twitter_tweets_text(posts)}\n"
        prompt += f"{prompts['general']['pretexts']}"
        prompt += f"{prompts['options'][option]['start']}"
        prompt += f"{prompts['options'][option]['rules']}"
        prompt += f"{prompts['general']['payload']}"
        if payload_option == 4:
                prompt += f"{payload_text}\n"
        else:
                prompt += f"{prompts['payloads'][payload]}"
        prompt += f"{prompts['general']['only']}"
        prompt += f"{prompts['general']['details']}"
        prompt += f"{prompts['general']['source']}"
        if template:
                prompt += f"{prompts['general']['template']}\n"
                prompt += f"{template}\n"
        prompt += f"Today is {datetime.now().strftime('%A, %B %d, %Y')}\n"
        #prompt += f"{prompts['extra']['grandma']}\n"
        return self._api_call(prompt, ai_option_c)
        #return prompt

    # ! --------------------------------------------------------------------------------
    # ! PRIVATE
    # ! --------------------------------------------------------------------------------
    def _api_call(self, prompt: str, model: str = "llama3"):
        response = ollama.chat(model=model, messages=[
                {"role": "user", "content": prompt}
        ], stream=False)

        response_text = response['message']['content']

        timestamp = datetime.now().isoformat()
        new_entry = {
            "time": timestamp,
            "prompt": prompt,
            "response": response_text
        }
        if os.path.exists(Const.HISTORY_PATH):
            with open(Const.HISTORY_PATH, 'r') as history_file:
                history_data = json.load(history_file)
        else:
            history_data = []
        history_data.append(new_entry)
        with open(Const.HISTORY_PATH, 'w') as history_file:
            json.dump(history_data, history_file, indent=4)

        return response_text
    