from colorama import Fore, Style
from twitter_scraper import get_user as get_twitter_user, get_multiple_users as get_multiple_twitter_users
from chatgpt_module import generate_prompt_twitter_user as generate_prompt_twitter_user_chatgpt, generate_prompt_linkedin_user as generate_prompt_linkedin_user_chatgpt
from ollama_module import generate_prompt_twitter_user as generate_prompt_twitter_user_ollama, generate_prompt_linkedin_user as generate_prompt_linkedin_user_ollama
from linkedin_scraper import get_user as get_linkedin_user
import argparse
import sys
import json
import asyncio

from SocialService.SocialRender import SocialRender
from const import Const

# Define color codes
COLOR_WARNING = Fore.YELLOW
COLOR_ERROR = Fore.RED

# Define options
platform_options_list = ["Twitter", "LinkedIn"]
ai_options_list = ["OpenAI GPT-3.5", "OpenAI GPT-4o", "Mistral (local)", "Llama3 (local)"]
generation_options_list_twitter = ["Email", "SMS", "Vishing script", "Twitter DM", "Twitter post", "Twitter reply", "Pretext"]
generation_options_list_linkedin = ["Email", "SMS", "Vishing script", "Pretext"]
payload_options_list = ["Login page", "Attachment", "Download Link", "Else"]
user_options_list = ["Single user", "User list"]

# Define functions
async def main(args=None):
      print_logo()
      print(f"\n\n{COLOR_WARNING}Welcome to the AI Phishing Toolkit" 
            "\nThis is just a proof of concept and should not be used for malicious purposes\n"
            f"{Style.RESET_ALL}")

      if args:
            ai_option = args.ai
            platform_option = args.platform
            mult_option = "list" if args.list else "single"
            platform_option = platform_option.lower()
            mult_option = mult_option.lower()
            output_index = generation_options_list_twitter.index(args.output) + 1
            payload_index = payload_options_list.index(args.payload) + 1
            with open ('templates.json', 'r') as file:
                  templates = json.load(file)
            template_names = list(templates.keys())
            if args.template == None or args.template == False or args.template == "":
                  template = False
            elif args.template != None or args.template not in template_names:
                  print(f"{COLOR_ERROR}Invalid template name{Style.RESET_ALL}")
            else:
                  template = templates[args.template]

            social = SocialRender(platform_option)

            if mult_option == "single":
                  await social.single_user_cli(args.uname, output_index, payload_index, ai_option, template, args.api_key)
            elif mult_option == "list":
                  await social.user_list_cli(args.list, output_index, payload_index, ai_option, template, args.api_key)
            else:
                  print(f"{COLOR_ERROR}Invalid option{Style.RESET_ALL}")

      ai_option = ai_options_list[ai_options()-1]

      platform_option = platform_options()
      mult_option = mult_options()

      print(Const.platform_options_list[platform_option - 1])

      social = SocialRender(Const.platform_options_list[platform_option - 1])

      if(mult_option == 1):
            await social.service.single_user(ai_option)
      elif(mult_option == 2):
            await social.service.user_list(ai_option)

def ai_options():
      print("\n\nPlease select what AI to use:")
      print_options(ai_options_list)
      ai_option = get_valid_input(len(ai_options_list))
      return ai_option

def platform_options():
      print("\n\nPlease select a platform to scrape the user data from:")
      print_options(platform_options_list)
      platform_option = get_valid_input(len(platform_options_list))
      return platform_option

def mult_options():
      print("\n\nPlease select an option:")
      print_options(user_options_list)
      mult_option = get_valid_input(len(user_options_list))
      return mult_option

def twitter_generation_options():
      print("\n\nPlease select what to generate:")
      print_options(generation_options_list_twitter)
      generation_option = get_valid_input(len(generation_options_list_twitter))
      return generation_option

def linkedin_generation_options():
      generation_option = 0
      print("\n\nPlease select what to generate:")
      print_options(generation_options_list_linkedin)
      generation_option = get_valid_input(len(generation_options_list_twitter))
      return generation_option

def payload_options():
      payload_option_text = ""
      print("\n\nPlease select a type of payload:")
      print_options(payload_options_list)
      payload_option = get_valid_input(len(payload_options_list))
      if payload_option == 4:
            payload_option_text = input("\Please specify the type of payload: ")
      return payload_option, payload_option_text

def template_options():
      template_option = input("\n\nDo you want to use a template? (y/n) ")
      if template_option == "n":
            return False
      elif template_option != "y":
            print(f"{COLOR_ERROR}Invalid option{Style.RESET_ALL}")
            return template_options()
      print("\n\nPlease write the template name or enter '?' to see the list of available templates:")
      with open ('templates.json', 'r') as file:
            templates = json.load(file)
      template_names = list(templates.keys())
      while True:
            template_name = input("\nTemplate name: ")
            if template_name == "?":
                  print("\n\nAvailable templates:")
                  print_options(template_names)
            elif template_name not in template_names:
                  print(f"{COLOR_ERROR}Invalid template name{Style.RESET_ALL}")
            else:
                  return templates[template_name]


def get_valid_input(size):
      bottom = 1
      top = size
      input_value = input("\nOption: ")
      try:
            input_value = int(input_value)
      except ValueError:
            print(f"{COLOR_ERROR}Invalid option{Style.RESET_ALL}")
            return get_valid_input(size)
      if input_value < bottom or input_value > top:
            print(f"{COLOR_ERROR}Invalid option{Style.RESET_ALL}")
            input_value = get_valid_input(size)
      return input_value

def print_options(options_list):
      for i in range(len(options_list)):
            print(f"{Fore.GREEN}{i+1}. {options_list[i]}{Style.RESET_ALL}")

async def twitter_single_user(ai_option):
      print("\n\nPlease enter the username of the user you would like to scrape:")
      username = input("\nUsername: ")
      tweets, userinfo = await get_twitter_user(username)
      if userinfo == None:
            print(f"{COLOR_ERROR}User not found{Style.RESET_ALL}")
            return twitter_single_user()
      generation_option = twitter_generation_options()
      payload, payload_text = payload_options()
      template = template_options()
      if ai_option == "OpenAI GPT-4o" or ai_option == "OpenAI GPT-3.5":
            print(generate_prompt_twitter_user_chatgpt(userinfo, tweets, generation_option, payload, ai_option, "", template, payload_text))
      elif ai_option == "Llama3 (local)" or ai_option == "Mistral (local)":
            print(generate_prompt_twitter_user_ollama(userinfo, tweets, generation_option, payload, ai_option, template, payload_text))

async def twitter_single_user_cli(username, generation, payload, ai_option, template, api_key=""):
      tweets, userinfo = await get_twitter_user(username)
      if userinfo == None:
            print(f"{COLOR_ERROR}User not found{Style.RESET_ALL}")
            return
      if ai_option == "OpenAI GPT-4o" or ai_option == "OpenAI GPT-3.5":
            print(generate_prompt_twitter_user_chatgpt(userinfo, tweets, generation, payload, ai_option, api_key, template, ""))
      elif ai_option == "Llama3 (local)" or ai_option == "Mistral (local)":
            print(generate_prompt_twitter_user_ollama(userinfo, tweets, generation, payload, ai_option, template, ""))
      sys.exit()

async def twitter_user_list(ai_option):
      print("\n\nPlease enter the path to the file containing the list of usernames you would like to scrape:")
      file_path = input("\nFile path: ")
      try:
            with open(file_path, 'r') as file:
                  usernames = file.readlines()
      except:
            print(f"{COLOR_ERROR}File not found{Style.RESET_ALL}")
            return twitter_user_list(ai_option)
      clean_usernames = []
      for user in usernames:
            if '\n' in user:
                  user = user[:-1]
            clean_usernames.append(user)

      tweets, userinfo = await get_multiple_twitter_users(clean_usernames)
      generation_option = twitter_generation_options()
      payload, payload_text = payload_options()
      template = template_options()
      if ai_option == "OpenAI GPT-4o" or ai_option == "OpenAI GPT-3.5":
            for tweet, user in zip(tweets, userinfo):
                  print(user['username'] + ':')
                  print(generate_prompt_twitter_user_chatgpt(user, tweet, generation_option, payload, ai_option, "", template, payload_text))
      elif ai_option == "Llama3 (local)" or ai_option == "Mistral (local)":
            for tweet, user in zip(tweets, userinfo):
                  print(f"{user['username']}:")
                  print(generate_prompt_twitter_user_ollama(user, tweet, generation_option, payload, ai_option, "", payload_text))

async def twitter_user_list_cli(file_path, generation, payload, ai_option, template, api_key):
      try:
            with open(file_path, 'r') as file:
                  usernames = file.readlines()
      except:
            print(f"{COLOR_ERROR}File not found{Style.RESET_ALL}")
            return
      clean_usernames = []
      for user in usernames:
            if '\n' in user:
                  user = user[:-1]
            clean_usernames.append(user)
      tweets, userinfo = await get_multiple_twitter_users(clean_usernames)
      if ai_option == "OpenAI GPT-4o" or ai_option == "OpenAI GPT-3.5":
            for tweet, user in zip(tweets, userinfo):
                  print(f"{user['username']}:")
                  print(generate_prompt_twitter_user_chatgpt(user, tweet, generation, payload, ai_option, api_key, template, ""))
      elif ai_option == "Llama3 (local)" or ai_option == "Mistral (local)":
            for tweet, user in zip(tweets, userinfo):
                  print(f"{user['username']}:")
                  print(generate_prompt_twitter_user_ollama(user, tweet, generation, payload, ai_option, template, ""))
      sys.exit()

def linkedin_single_user(ai_option):
      print("\n\nPlease enter the user ID of the user you would like to scrape:")
      print("(the user ID is in the URL of the user's profile like this: https://www.linkedin.com/in/user-id/)")
      user_id = input("\nUser ID: ")
      profile, posts = get_linkedin_user(user_id)
      if profile == None:
            print(f"{COLOR_ERROR}User not found{Style.RESET_ALL}")
            return linkedin_single_user()
      generation_option = linkedin_generation_options()
      payload, payload_text = payload_options()
      template = template_options()
      if ai_option == "OpenAI GPT-4o" or ai_option == "OpenAI GPT-3.5":
            print(generate_prompt_linkedin_user_chatgpt(profile, posts, generation_option, payload, ai_option, "", template, payload_text))
      elif ai_option == "Llama3 (local)" or ai_option == "Mistral (local)":
            print(generate_prompt_linkedin_user_ollama(profile, posts, generation_option, payload, ai_option, template, payload_text))

def linkedin_user_list(ai_option):
      print("\n\nPlease enter the path to the file containing the list of usernames you would like to scrape:")
      file_path = input("\nFile path: ")
      try:
            with open(file_path, 'r') as file:
                  usernames = file.readlines()
      except:
            print(f"{COLOR_ERROR}File not found{Style.RESET_ALL}")
            return twitter_user_list(ai_option)
      clean_usernames = []
      for user in usernames:
            if '\n' in user:
                  user = user[:-1]
            clean_usernames.append(user)
      profile_list = []
      posts_list = []
      for user_id in clean_usernames:
            profile, posts = get_linkedin_user(user_id)
            if profile == None:
                  print(f"{COLOR_ERROR}User {user_id} not found{Style.RESET_ALL}")
                  profile_list.append(None)
                  posts_list.append(None)
                  continue
            profile_list.append(profile)
            posts_list.append(posts)
      generation_option = linkedin_generation_options()
      payload = payload_options()
      template = template_options()
      for profile, posts in zip(profile_list, posts_list):
            if ai_option == "OpenAI GPT-4o" or ai_option == "OpenAI GPT-3.5":
                  print(f"{user['username']}:")
                  print(generate_prompt_linkedin_user_chatgpt(profile, posts, generation_option, payload, ai_option, "", template, ""))
            elif ai_option == "Llama3 (local)" or ai_option == "Mistral (local)":
                  print(f"{user['username']}:")
                  print(generate_prompt_linkedin_user_ollama(profile, posts, generation_option, payload, ai_option, template, ""))

def linkedin_single_user_cli(user_id, generation_option, payload, ai_option, template, api_key):
      profile, posts = get_linkedin_user(user_id)
      if profile == None:
            print(f"{COLOR_ERROR}User not found{Style.RESET_ALL}")
            return
      if ai_option == "OpenAI GPT-4o" or ai_option == "OpenAI GPT-3.5":
            print(generate_prompt_linkedin_user_chatgpt(profile, posts, generation_option, payload, ai_option, api_key, template, ""))
      elif ai_option == "Llama3 (local)" or ai_option == "Mistral (local)":
            print(generate_prompt_linkedin_user_ollama(profile, posts, generation_option, payload, ai_option, template, ""))
      sys.exit()

def linkedin_user_list_cli(file_path, generation, payload, ai_option, template, api_key):
      try:
            with open(file_path, 'r') as file:
                  usernames = file.readlines()
      except:
            print(f"{COLOR_ERROR}File not found{Style.RESET_ALL}")
            return
      clean_usernames = []
      for user in usernames:
            if '\n' in user:
                  user = user[:-1]
            clean_usernames.append(user)
      profile_list = []
      posts_list = []
      for user_id in clean_usernames:
            profile, posts = get_linkedin_user(user_id)
            if profile == None:
                  print(f"{COLOR_ERROR}User {user_id} not found{Style.RESET_ALL}")
                  profile_list.append(None)
                  posts_list.append(None)
                  continue
            profile_list.append(profile)
            posts_list.append(posts)
      generation_option = linkedin_generation_options()
      payload = payload_options()
      template = template_options()
      for profile, posts in zip(profile_list, posts_list):
            if ai_option == "OpenAI GPT-4o" or ai_option == "OpenAI GPT-3.5":
                  print(f"{user['username']}:")
                  print(generate_prompt_linkedin_user_chatgpt(profile, posts, generation_option, payload, ai_option, api_key, template, ""))
            elif ai_option == "Llama3 (local)" or ai_option == "Mistral (local)":
                  print(f"{user['username']}:")
                  print(generate_prompt_linkedin_user_ollama(profile, posts, generation_option, payload, ai_option, template, ""))

def print_logo():
      print("\n\n"
      f"{Fore.CYAN}   _____   ___  __________ __     __        __     __                 ___________            __   __    __  __   "
      f"\n  /  _  \ |   | \______   \  |__ |__| _____|  |__ |__| ____    ____   \__    ___/___   ____ |  | |  | _|__|/  |_ "
      f"\n /  /_\  \|   |  |     ___/  |  \|  |/  ___/  |  \|  |/    \  / ___\    |    | /  _ \ /  _ \|  | |  |/ /  \   __\\"
      f"\n/    |    \   |  |    |   |   Y  \  |\___ \|   Y  \  |   |  \/ /_/  >   |    |(  <_> |  <_> )  |_|    <|  ||  |  "
      f"\n\____|__  /___|  |____|   |___|  /__/____  >___|  /__|___|  /\___  /    |____| \____/ \____/|____/__|_ \__||__|  "
      f"\n        \/                     \/        \/     \/        \//_____/                                   \/         "
      f"{Style.RESET_ALL}")

if __name__ == "__main__":
      parser = argparse.ArgumentParser(description="AI Phishing Toolkit")
      parser.add_argument('-ai', choices=ai_options_list, help='Select AI to use')
      parser.add_argument('-platform', choices=platform_options_list, help='Select platform to scrape user data from')
      parser.add_argument('-list', help='Target multiple users (provide file path with username list)')
      parser.add_argument('-uname', help='Username of the single user to scrape')
      parser.add_argument('-output', choices=generation_options_list_twitter, help='Specify what to generate')
      parser.add_argument('-payload', choices=payload_options_list, help='Specify type of payload')
      parser.add_argument('-template', help='Specify a template to use', default=False)
      parser.add_argument('-api_key', help='API key for the AI service')
      args = parser.parse_args()
      if not any(vars(args).values()):
            asyncio.run(main())
      else:
            if(args.platform and args.ai and args.output and args.payload and (args.list or args.uname)):
                  print(args)
                  asyncio.run(main(args))
            else:
                  parser.print_help()