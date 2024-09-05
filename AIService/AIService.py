from abc import abstractmethod
import json

from Util.Const import Const

class AIService:
    def __init__(self) -> None:
        pass
        
    # ! --------------------------------------------------------------------------------
    # ! Private
    # ! --------------------------------------------------------------------------------

    def _get_prompt_json(self):
        with open(Const.PROMPTS_PATH, 'r') as file:
            prompt = json.load(file)
        return prompt
    
    def _get_payload_option(self, payload_option: tuple | str):
        payload_option = int(payload_option[0] if type(payload_option) == tuple else payload_option)
        if payload_option == 1:
            return "login_link"
        elif payload_option == 2:
            return "attachment"
        elif payload_option == 3:
            return "download_link"
        elif payload_option == 4:
            return "else"

    # * Linkedin  
    def _get_generation_option_linkedin(self, generation_option: str):
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

    def _generate_linkedin_probability(self, profile: str, posts: str, prompts: dict):
        prompt = f"{prompts['twitter']['calculate_probability']}\n"
        prompt += f"{self._generate_linkedin_profile_text(profile)}\n"
        prompt += f"{self._generate_linkedin_posts_text(posts)}\n"
        return prompt
    
    def _generate_linkedin_profile_text(self, profile: str):
        profile_text = "Here is some useful information about the user:\n"
        profile_text += profile
        return profile_text

    def _generate_linkedin_posts_text(self, posts: str):
        posts_text = "Here are the user's most recent posts:\n"
        if posts == None:
            posts_text += "The user has not posted anything yet\n"
        else:
            posts_text += posts
        return posts_text
    
    # * Twitter
    def _get_generation_option_twitter(self, generation_option: str):
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
        
    def _generate_twitter_probability(self, userinfo: dict, prompts: dict, tweets):
        prompt = f"{prompts['twitter']['calculate_probability']}\n"
        prompt += f"{self._generate_twitter_user_text(userinfo)}\n"
        prompt += f"{self._generate_twitter_tweets_text(tweets)}\n"
        return prompt

    def _generate_twitter_user_text(self, userinfo: dict):
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

    def _generate_twitter_tweets_text(self, tweets):
        tweets_text = "Here are the user's most recent tweets:\n"
        if tweets == None:
            tweets_text += "The user has not tweeted anything yet\n"
        else:
            for tweet in tweets:
                tweets_text += f"{tweet.created_at}\n"
                tweets_text += f"{tweet.full_text}\n\n"
        return tweets_text

    # ! --------------------------------------------------------------------------------
    # ! Abstract
    # ! --------------------------------------------------------------------------------

    @abstractmethod
    def generate_prompt_linkedin(self, profile: str, posts: str, generation_option: str, payload_option: str, ai_option: str, template: str, payload_text: str = "", **kwargs):
        """
        generate_prompt_linkedin function
        """

    @abstractmethod
    def generate_prompt_twitter(self, profile: str, posts: str, generation_option: str, payload_option: str, ai_option: str, template: str, payload_text: str = "", **kwargs):
        """
        generate_prompt_linkedin function
        """
