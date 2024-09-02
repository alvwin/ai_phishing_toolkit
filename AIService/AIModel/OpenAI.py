from datetime import datetime
import json
import os
import configparser
import getpass

from ..AIService import AIService
from const import Const

class OpenAI(AIService):
    def __init__(self) -> None:
        super().__init__()

    def generate_prompt_linkedin(self, profile: str, posts: str, generation_option: str, payload_option: str, ai_option: str, template: str, payload_text: str = "", **kwargs):
        option = self._get_generation_option_linkedin(generation_option)
        prompts = self._get_prompt_json()
        payload = self._get_payload_option(payload_option)
        prompt = ""
        if option == "invalid":
                print("Invalid generation option")
                return
        if option == "probability":
                return self._api_call(self._generate_linkedin_probability(profile, posts, prompts), api_key, prompts, ai_option)
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
        if api_key == "":
                api_key = self._get_api_key()
        return self._api_call(prompt, api_key, prompts, ai_option)
    
    def generate_prompt_twitter(self, profile: str, posts: str, generation_option: str, payload_option: str, ai_option: str, template: str, payload_text: str = "", **kwargs):
        option = self._get_generation_option_twitter(generation_option)
        prompts = self._get_prompt_json()
        payload = self._get_payload_option(payload_option, payload_text)
        prompt = ""
        if option == "invalid":
                print("Invalid generation option")
                return
        if option == "probability":
                return self._api_call(self._generate_twitter_probability(profile, prompts, posts), api_key, prompts, ai_option)
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
        if api_key == "":
                api_key = self._get_api_key()
        return self._api_call(prompt, api_key, prompts, ai_option)
    # ! --------------------------------------------------------------------------------
    # ! PRIVATE
    # ! --------------------------------------------------------------------------------
    def _api_call(self, prompt: str, api_key: str, json_file: dict, model: str):
        if model == "OpenAI GPT-3.5":
            model = "gpt-3.5-turbo"
        else:
            model = "gpt-4o-latest"
        client = OpenAI(api_key=api_key)
        try:
            response = client.chat.completions.create(
                model = model,
                messages = [
                        {"role": json_file["api_call"][0]['role'], "content": json_file["api_call"][0]['content']},
                        {"role": "user", "content": prompt}
                ],
                stream=False
            )
            response_text = response.choices[0].message.content

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
        except Exception as e:
            print(f"An error occurred: {e}")
            return
        
    def _get_api_key(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        try:
            api_key = config.get('openai', 'api_key')
        except (configparser.NoSectionError, configparser.NoOptionError):
            print("OpenAI API key not found in config file.")
            api_key = getpass.getpass("Please enter your OpenAI API key: ")
            if not config.has_section('openai'):
                config.add_section('openai')
            config.set('openai', 'api_key', api_key)

            with open('config.ini', 'w') as configfile:
                config.write(configfile)
        return api_key
    
    