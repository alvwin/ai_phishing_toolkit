class SocialRender:
    def __init__(self, social: str) -> None:
        if social.lower() == "twitter":
            from .Social.TwitterService import TwitterService
            self.service = TwitterService()
        elif social.lower() == "linkedin":
            from .Social.LinkedinService import LinkedinService
            self.service = LinkedinService()