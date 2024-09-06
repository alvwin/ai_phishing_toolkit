from twikit import Client
import sys
import configparser
import json
import getpass

from SocialService.SocialService import SocialService
from Util.Const import Const
from Util.Helper import Helper
from AIService.AIRender import AIRender

class TwitterService(SocialService):
    def __init__(self) -> None:
        pass

    async def single_user_cli(self, username: str, output: str, payload: str, ai: str, template: str, api_key: str = ""):
        tweets, userinfo = await self._get_user(username)
        if userinfo is None:
                print(f"{Const.COLOR_ERROR}User not found{Const.RESET_ALL}")
                return
        
        Ai = AIRender(ai).model

        print(Ai.generate_prompt_twitter(userinfo, tweets, output, payload, ai, api_key, template, ""))
        
        sys.exit()

    async def user_list_cli(self, file_path: str, output: str, payload: str, ai: str, template: str, api_key: str = ""):
        try:
            with open(file_path, 'r') as file:
                usernames = file.readlines()
        except Exception:
            print(f"{Const.COLOR_ERROR}File not found{Const.RESET_ALL}")
            return
        clean_usernames = []
        for user in usernames:
                if '\n' in user:
                    user = user[:-1]
                clean_usernames.append(user)
        tweets, userinfo = await self._get_multiple_twitter_users(clean_usernames)

        Ai = AIRender(ai).model

        for tweet, user in zip(tweets, userinfo):
            print(f"{user['username']}:")
            print(Ai.generate_prompt_twitter(user, tweet, output, payload, ai, template, api_key=api_key))

        sys.exit()

    async def single_user(self, ai: str):
        print("\n\nPlease enter the username of the user you would like to scrape:")
        username = input("\nUsername: ")
        tweets, userinfo = await self._get_user(username)
        if userinfo is None:
                print(f"{Const.COLOR_ERROR}User not found{Const.RESET_ALL}")
                return await self.single_user(ai)
        generation_option = self._twitter_generation_options()
        payload, payload_text = self._payload_options()
        template = self._template_options()

        Ai = AIRender(ai).model

        print(Ai.generate_prompt_twitter(userinfo, tweets, generation_option, payload, ai, template, payload_text, api_key=""))

    async def user_list(self, ai: str):
        print("\n\nPlease enter the path to the file containing the list of usernames you would like to scrape:")
        file_path = input("\nFile path: ")
        try:
            with open(file_path, 'r') as file:
                usernames = file.readlines()
        except Exception:
            print(f"{Const.COLOR_ERROR}File not found{Const.RESET_ALL}")
            return self.user_list(ai)
        clean_usernames = []
        for user in usernames:
            if '\n' in user:
                user = user[:-1]
            clean_usernames.append(user)

        tweets, userinfo = await self._get_multiple_users(clean_usernames)
        generation_option = self._twitter_generation_options()
        payload, payload_text = self._payload_options()
        template = self._template_options()

        Ai = AIRender(ai).model

        for tweet, user in zip(tweets, userinfo):
            print(user['username'] + ':')
            print(Ai.generate_prompt_twitter(user, tweet, generation_option, payload, ai, template, payload_text, api_key=""))

    # ! --------------------------------------------------------------------------------
    # ! PRIVATE
    # ! --------------------------------------------------------------------------------
    async def _get_user(self, name: str):
        client = Client('en-US')

        # try to login with stored cookie
        try:
            cookie = self._load_user_cookie()
            #print(client.set_cookies(cookie))
            print("Logged in from the last session")
        except Exception:
            # try to login with stored credentials
            try:
                username, email, password = self._load_login_info()
                print("Logged in with stored credentials")
            except Exception:
                print("No login info found. Please enter your login info:")
                username, email, password = self._get_login_info()
                if self._ask_save_credentials():
                    self._save_login_info(username, email, password)
            finally:
                try:
                    # save credentials
                    await client.login(
                        auth_info_1 = username,
                        auth_info_2 = email,
                        password = password
                    )
                    if self._ask_save_cookie():
                        self._save_user_cookie(client)
                except Exception as e:
                    print("An error occurred: " + str(e))
                    print("Please try logging in with a cookie")
                    cookie = input("Enter your cookie: ")
                    client.set_cookies(json.loads(cookie))
                    self._save_user_cookie(client)
        
        try:
            user = await client.get_user_by_screen_name(name)
        except Exception:
            return None, None
        user_id = user.id
        tweets = await client.get_user_tweets(user_id, 'Tweets', 2)
        for tweet in tweets:
            if tweet.retweeted_tweet:
                tweet.full_text = tweet.retweeted_tweet.full_text
        if len(tweets) > 5:
            tweets = tweets[:5]

        userinfo = {
            'user_id': user_id,
            'username': name,
            'location': user.location,
            'description': user.description,
            'can_dm': user.can_dm,
            'followers_count': user.followers_count,
            'following_count': user.following_count,
            'favourites_count': user.favourites_count,
            'listed_count': user.listed_count,
            'statuses_count': user.statuses_count,
            'media_count': user.media_count,
            'created_at': user.created_at
        }
        return tweets, userinfo

    def _load_user_cookie(self):
        config = configparser.ConfigParser(interpolation=None)
        config.read('config.ini')
        cookie = json.loads(config.get("twitter", "cookie"))
        if cookie:
            return cookie
        else:
            raise Exception("No cookie found in config file")

    def _load_login_info(self):
        config = configparser.ConfigParser(interpolation=None)
        config.read('config.ini')
        username = config.get("twitter", "username")
        email = config.get("twitter", "email")
        password = config.get("twitter", "password")
        if username and email and password:
            return username, email, password
        else:
            raise Exception("No login info found in config file")

    def _get_login_info(self):
        username = input("Enter your username: ")
        email = input("Enter your email: ")
        password = getpass.getpass("Enter your password: ")
        return username, email, password

    def _ask_save_credentials(self):
        save = input("Would you like to save your login credentials? (y/n): ")
        if save == "y":
            return True
        elif save == "n":
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'")
            return self._ask_save_credentials()

    def _save_login_info(self, username: str, email: str, password: str):
        config = configparser.ConfigParser(interpolation=None)
        config.read('config.ini')
        if not config.has_section('twitter'):
            config.add_section('twitter')
        config.set('twitter', 'username', username)
        config.set('twitter', 'email', email)
        config.set('twitter', 'password', password)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def _ask_save_cookie(self):
        save = input("Would you like to save your cookie? (y/n): ")
        if save == "y":
            return True
        elif save == "n":
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'")
            return self._ask_save_cookie()

    def _save_user_cookie(self, client: Client):
        config = configparser.ConfigParser(interpolation=None)
        config.read('config.ini')
        if not config.has_section('twitter'):
            config.add_section('twitter')
        config.set('twitter', 'cookie', json.dumps(client.get_cookies()))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    async def _get_multiple_users(self, userlist: list):
        client = Client('en-US')

        try:
            cookie = self._load_user_cookie()
            client.set_cookies(cookie)
            print("Logged in from the last session")
        except Exception:
            try:
                username, email, password = self._load_login_info()
                print("Logged in with stored credentials")
            except Exception:
                print("No login info found. Please enter your login info:")
                username, email, password = self._get_login_info()
                self._save_login_info(username, email, password)
            finally:
                await client.login(
                    auth_info_1 = username,
                    auth_info_2 = email,
                    password = password
                )
                self._save_user_cookie(client)

        tweetslist = []
        userinfolist = []
        for username in userlist:
            try:
                user = await client.get_user_by_screen_name(username)
            except Exception:
                print('User ' + username + ' not found')
                continue
            user_id = user.id
            tweets = await client.get_user_tweets(user_id, 'Tweets', 2)

            userinfo = {
                'user_id': user_id,
                'username': username,
                'location': user.location,
                'description': user.description,
                'can_dm': user.can_dm,
                'followers_count': user.followers_count,
                'following_count': user.following_count,
                'favourites_count': user.favourites_count,
                'listed_count': user.listed_count,
                'statuses_count': user.statuses_count,
                'media_count': user.media_count,
                'created_at': user.created_at
            }

            tweetslist.append(tweets)
            userinfolist.append(userinfo)
        return tweetslist, userinfolist

    def _twitter_generation_options(self):
        print("\n\nPlease select what to generate:")
        Helper.print_options(Const.generation_options_list_twitter)
        generation_option = Helper.get_valid_input(len(Const.generation_options_list_twitter))
        return generation_option
    
    def _payload_options(self):
        payload_option_text = ""
        print("\n\nPlease select a type of payload:")
        Helper.print_options(Const.payload_options_list)
        payload_option = Helper.get_valid_input(len(Const.payload_options_list))
        if payload_option == 4:
                payload_option_text = input("\Please specify the type of payload: ")
        return payload_option, payload_option_text
    
    def _template_options(self):
        template_option = input("\n\nDo you want to use a template? (y/n) ")
        if template_option == "n":
            return False
        elif template_option != "y":
            print(f"{Const.COLOR_ERROR}Invalid option{Const.RESET_ALL}")
            return self._template_options()
        print("\n\nPlease write the template name or enter '?' to see the list of available templates:")
        with open ('templates.json', 'r') as file:
            templates = json.load(file)
        template_names = list(templates.keys())
        while True:
            template_name = input("\nTemplate name: ")
            if template_name == "?":
                print("\n\nAvailable templates:")
                Helper.print_options(template_names)
            elif template_name not in template_names:
                print(f"{Const.COLOR_ERROR}Invalid template name{Const.RESET_ALL}")
            else:
                return templates[template_name]