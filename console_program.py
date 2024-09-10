import argparse
import json
import asyncio
import logging

from SocialService.SocialRender import SocialRender
from Util.Const import Const
from Util.Helper import Helper
from Console.Logging import setup_logging

# Define functions
async def main(args=None):
      print_logo()
      print(f"\n\n{Const.COLOR_WARNING}Welcome to the AI Phishing Toolkit" 
            "\nThis is just a proof of concept and should not be used for malicious purposes\n"
            f"{Const.RESET_ALL}")

      if args:
            ai_option = args.ai
            platform_option = args.platform
            mult_option = "list" if args.list or args.list_company else "single"
            platform_option = platform_option.lower()
            mult_option = mult_option.lower()
            output_index = Const.generation_options_list_twitter.index(args.output) + 1
            payload_index = Const.payload_options_list.index(args.payload) + 1
            with open ('templates.json', 'r') as file:
                  templates = json.load(file)
            template_names = list(templates.keys())
            if args.template is None or args.template == False or args.template == "":
                  template = False
            elif args.template != None or args.template not in template_names:
                  print(f"{Const.COLOR_ERROR}Invalid template name{Const.RESET_ALL}")
            else:
                  template = templates[args.template]

            social = SocialRender(platform_option).service
            if mult_option == "single":
                  await social.single_user_cli(args.uname, output_index, payload_index, ai_option, template, args.api_key)
            elif mult_option == "list":
                  if platform_option.lower() != "linkedin":
                        await social.user_list_cli(args.list, output_index, payload_index, ai_option, template, args.api_key)
                  else:
                        if args.list_company:
                              await social.company_list_cli(args.list_company, output_index, payload_index, ai_option, template, args.api_key)
                        else:
                              await social.user_list_cli(args.list, output_index, payload_index, ai_option, template, args.api_key)
            else:
                  print(f"{Const.COLOR_ERROR}Invalid option{Const.RESET_ALL}")
            return

      ai_option = Const.ai_options_list[Helper.selection_options(Const.ai_options_list)-1]

      platform_option = Helper.selection_options(Const.platform_options_list)
      account_type = None
      if platform_option == 2:
            account_type = Helper.selection_options(Const.account_type_options_list)
           
      if account_type == 1: 
            mult_option = Helper.selection_options(Const.user_options_list)
      elif account_type == 2:
            mult_option = Helper.selection_options(Const.company_options_list)
      else: mult_option = Helper.selection_options(Const.user_options_list)
            
      social = SocialRender(Const.platform_options_list[platform_option - 1]).service

      if account_type == 2:
            if(mult_option == 1):
                  await social.single_company(ai_option)
                  return
            elif(mult_option == 2):
                  await social.company_list(ai_option)
                  return
      if(mult_option == 1):
            await social.single_user(ai_option)
      elif(mult_option == 2):
            await social.user_list(ai_option)

def print_logo():
      print("\n\n"
      f"{Const.COLOR_CYAN}   _____   ___  __________ __     __        __     __                 ___________            __   __    __  __   "
      f"\n  /  _  \ |   | \______   \  |__ |__| _____|  |__ |__| ____    ____   \__    ___/___   ____ |  | |  | _|__|/  |_ "
      f"\n /  /_\  \|   |  |     ___/  |  \|  |/  ___/  |  \|  |/    \  / ___\    |    | /  _ \ /  _ \|  | |  |/ /  \   __\\"
      f"\n/    |    \   |  |    |   |   Y  \  |\___ \|   Y  \  |   |  \/ /_/  >   |    |(  <_> |  <_> )  |_|    <|  ||  |  "
      f"\n\____|__  /___|  |____|   |___|  /__/____  >___|  /__|___|  /\___  /    |____| \____/ \____/|____/__|_ \__||__|  "
      f"\n        \/                     \/        \/     \/        \//_____/                                   \/         "
      f"{Const.RESET_ALL}")

if __name__ == "__main__":

      parser = argparse.ArgumentParser(description="AI Phishing Toolkit")
      parser.add_argument('-ai', choices=Const.ai_options_list, help='Select AI to use')
      parser.add_argument('-platform', choices=Const.platform_options_list, help='Select platform to scrape user data from')
      parser.add_argument('-list', help='Target multiple users (provide file path with username list)')
      parser.add_argument('-list-company', help='Target multiple company (provide file path with companies list)')
      parser.add_argument('-uname', help='Username of the single user to scrape')
      parser.add_argument('-company', help='Company of the single company to scrape')
      parser.add_argument('-output', choices=Const.generation_options_list_twitter, help='Specify what to generate')
      parser.add_argument('-payload', choices=Const.payload_options_list, help='Specify type of payload')
      parser.add_argument('-template', help='Specify a template to use', default=False)
      parser.add_argument('-api_key', help='API key for the AI service')
      args = parser.parse_args()

      logging_config = setup_logging(name=__name__)

      if not any(vars(args).values()):
            asyncio.run(main())
      else:
            if(args.platform and args.ai and args.output and args.payload and (args.list or args.uname or args.company or args.list_company)):
                  asyncio.run(main(args))
            else:
                  parser.print_help()