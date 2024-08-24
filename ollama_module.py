import ollama
import json
import os
from datetime import datetime

PROMPTS_PATH = 'prompts.json'
HISTORY_PATH = 'history.json'

def generate_prompt_twitter_user(userinfo, tweets, generation_option, payload_option, ai_option, template, payload_text=""):
      option = get_generation_option(generation_option)
      prompts = get_prompt_json()
      payload = get_payload_option(payload_option, payload_text)
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
            return api_call(generate_twitter_probability(userinfo, prompts, tweets))
      prompt += f"{prompts['general']['twitter']}"
      prompt += f"{generate_twitter_user_text(userinfo)}\n"
      prompt += f"{generate_twitter_tweets_text(tweets)}\n"
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
      return api_call(prompt, ai_option_c)
      #return prompt

def get_generation_option(generation_option):
      generation_option = int(generation_option)
      if generation_option == 1:
            return "email"
      elif generation_option == 2:
            return "SMS"
      elif generation_option == 3:
            return "vishing"
      elif generation_option == 4:
            return "DM"
      elif generation_option == 5:
            return "post"
      elif generation_option == 6:
            return "reply"
      elif generation_option == 7:
            return "pretext"
      elif generation_option == 8:
            return "probability"
      else:
            return "invalid"
      
def get_payload_option(payload_option, payload_text=""):
      payload_option = int(payload_option)
      if payload_option == 1:
            return "login_link"
      elif payload_option == 2:
            return "attachment"
      elif payload_option == 3:
            return "download_link"
      elif payload_option == 4:
            return "else"

      
def generate_twitter_user_text(userinfo):
      user_text = "Here is some useful information about the user's profile:\n"
      user_text += f"Username: {userinfo['username']}\n"
      user_text += f"Location: {userinfo['location']}\n"
      user_text += f"Description: {userinfo['description']}\n"
      user_text += f"Followers count: {userinfo['followers_count']}\n"
      user_text += f"Following count: {userinfo['following_count']}\n"
      user_text += f"Favourites count: {userinfo['favourites_count']}\n"
      user_text += f"Listed count: {userinfo['listed_count']}\n"
      user_text += f"Statuses count: {userinfo['statuses_count']}\n"
      user_text += f"Media count: {userinfo['media_count']}\n"
      user_text += f"Created at: {userinfo['created_at']}\n"
      return user_text

def generate_twitter_tweets_text(tweets):
      tweets_text = "Here are the user's most recent tweets:\n"
      if tweets == None:
            tweets_text += "The user has not tweeted anything yet\n"
      else:
            for tweet in tweets:
                  tweets_text += f"{tweet.created_at}\n"
                  tweets_text += f"{tweet.full_text}\n\n"
      return tweets_text

def get_prompt_json():
      with open(PROMPTS_PATH, 'r') as file:
            prompt = json.load(file)
      return prompt

def generate_twitter_probability(userinfo, prompts, tweets):
      prompt = f"{prompts['twitter']['calculate_probability']}\n"
      prompt += f"{generate_twitter_user_text(userinfo)}\n"
      prompt += f"{generate_twitter_tweets_text(tweets)}\n"
      return prompt

def api_call(prompt, model="llama3"):
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
      if os.path.exists(HISTORY_PATH):
            with open(HISTORY_PATH, 'r') as history_file:
                  history_data = json.load(history_file)
      else:
            history_data = []
      history_data.append(new_entry)
      with open(HISTORY_PATH, 'w') as history_file:
            json.dump(history_data, history_file, indent=4)

      return response_text

def generate_prompt_linkedin_user(profile, posts, generation_option, payload_option, ai_option, template, payload_text=""):
      option = get_generation_option_linkedin(generation_option)
      prompts = get_prompt_json()
      payload = get_payload_option(payload_option, payload_text)
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
            return api_call(generate_linkedin_probability(profile, posts, prompts))
      prompt += f"{prompts['general']['linkedin']}"
      prompt += f"{generate_linkedin_profile_text(profile)}\n"
      prompt += f"{generate_linkedin_posts_text(posts)}\n"
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
      return api_call(prompt, ai_option_c)

def generate_linkedin_profile_text(profile):
      profile_text = "Here is some useful information about the user:\n"
      profile_text += profile
      return profile_text

def generate_linkedin_posts_text(posts):
      posts_text = "Here are the user's most recent posts:\n"
      if posts == None:
            posts_text += "The user has not posted anything yet\n"
      else:
            posts_text += posts
      return posts_text

def get_generation_option_linkedin(generation_option):
      generation_option = int(generation_option)
      if generation_option == 1:
            return "email"
      elif generation_option == 2:
            return "SMS"
      elif generation_option == 3:
            return "vishing"
      elif generation_option == 4:
            return "pretext"
      elif generation_option == 5:
            return "probability"
      else:
            return "invalid"
      
def generate_linkedin_probability(profile, posts, prompts):
      prompt = f"{prompts['twitter']['calculate_probability']}\n"
      prompt += f"{generate_linkedin_profile_text(profile)}\n"
      prompt += f"{generate_linkedin_posts_text(posts)}\n"
      return prompt

#https://github.com/ollama/ollama-python
#ollama serve