from twikit import Client
import json
import getpass
import configparser

# get Login info from user
def get_login_info():
      username = input("Enter your username: ")
      email = input("Enter your email: ")
      password = getpass.getpass("Enter your password: ")
      return username, email, password

# save login info to config file
def save_login_info(username, email, password):
      config = configparser.ConfigParser(interpolation=None)
      config.read('config.ini')
      if not config.has_section('twitter'):
            config.add_section('twitter')
      config.set('twitter', 'username', username)
      config.set('twitter', 'email', email)
      config.set('twitter', 'password', password)
      with open('config.ini', 'w') as configfile:
                  config.write(configfile)

# load login info from config file
def load_login_info():
      config = configparser.ConfigParser(interpolation=None)
      config.read('config.ini')
      username = config.get("twitter", "username")
      email = config.get("twitter", "email")
      password = config.get("twitter", "password")
      if username and email and password:
            return username, email, password
      else:
            raise Exception("No login info found in config file")

# save user cookie to config file
def save_user_cookie(client):
      config = configparser.ConfigParser(interpolation=None)
      config.read('config.ini')
      if not config.has_section('twitter'):
            config.add_section('twitter')
      config.set('twitter', 'cookie', json.dumps(client.get_cookies()))
      with open('config.ini', 'w') as configfile:
                  config.write(configfile)
      
# load user cookie from config file
def load_user_cookie():
      config = configparser.ConfigParser(interpolation=None)
      config.read('config.ini')
      cookie = json.loads(config.get("twitter", "cookie"))
      if cookie:
            return cookie
      else:
            raise Exception("No cookie found in config file")
      
def ask_save_credentials():
      save = input("Would you like to save your login credentials? (y/n): ")
      if save == "y":
            return True
      elif save == "n":
            return False
      else:
            print("Invalid input. Please enter 'y' or 'n'")
            return ask_save_credentials()
      
def ask_save_cookie():
      save = input("Would you like to save your cookie? (y/n): ")
      if save == "y":
            return True
      elif save == "n":
            return False
      else:
            print("Invalid input. Please enter 'y' or 'n'")
            return ask_save_cookie()

# get single user
def get_user(name):
      client = Client('en-US')

      # try to login with stored cookie
      try:
            cookie = load_user_cookie()
            print(client.set_cookies(cookie))
            print("Logged in from the last session")
      except:
            # try to login with stored credentials
            try:
                  username, email, password = load_login_info()
                  print("Logged in with stored credentials")
            except:
                  print("No login info found. Please enter your login info:")
                  username, email, password = get_login_info()
                  if ask_save_credentials():
                        save_login_info(username, email, password)
            finally:
                  # save credentials
                  client.login(
                        auth_info_1 = username,
                        auth_info_2 = email,
                        password = password
                  )
                  if ask_save_cookie():
                        save_user_cookie(client)
      
      # get user info
      try:
            user = client.get_user_by_screen_name(name)
      except:
            return None, None
      user_id = user.id
      tweets = client.get_user_tweets(user_id, 'Tweets', 2)
      for tweet in tweets:
            if tweet.retweeted_tweet:
                  tweet.full_text = tweet.retweeted_tweet.full_text
      if len(tweets) > 5:
            tweets = tweets[:5]
      # for tweet in tweets:
      #       print(tweet.full_text)
      #       print("---")
      #       print(tweet.text)
      #       print("================")

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

def get_multiple_users(userlist):
      client = Client('en-US')

      try:
            cookie = load_user_cookie()
            client.set_cookies(cookie)
            print("Logged in from the last session")
      except:
            try:
                  username, email, password = load_login_info()
                  print("Logged in with stored credentials")
            except:
                  print("No login info found. Please enter your login info:")
                  username, email, password = get_login_info()
                  save_login_info(username, email, password)
            finally:
                  client.login(
                        auth_info_1 = username,
                        auth_info_2 = email,
                        password = password
                  )
                  save_user_cookie(client)

      tweetslist = []
      userinfolist = []
      for username in userlist:
            try:
                  user = client.get_user_by_screen_name(username)
            except:
                  print('User ' + username + ' not found')
                  continue
            user_id = user.id
            tweets = client.get_user_tweets(user_id, 'Tweets', 2)

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