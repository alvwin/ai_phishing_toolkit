class SocialRender:
    def __init__(self, social: str) -> None:
        if social.lower() == "twitter":
            from SocialService.Social.TwitterService import TwitterService
            return TwitterService()
        elif social.lower() == "linkedin":
            from SocialService.Social.LinkedinService import LinkedinService
            return LinkedinService()