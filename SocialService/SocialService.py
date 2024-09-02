from abc import abstractmethod

from Util.Const import Const

class SocialService:
    def __init__(self) -> None:
        pass

    # ! --------------------------------------------------------------------------------
    # ! Abstract
    # ! --------------------------------------------------------------------------------
        
    @abstractmethod
    async def single_user_cli(self, username: str, output: str, payload: str, ai: str, template: str, api_key: str = ""):
        """
        single_user_cli function
        """

    @abstractmethod
    async def user_list_cli(self, file_path: str, output: str, payload: str, ai: str, template: str, api_key: str = ""):
        """
        user_list_cli function
        """

    @abstractmethod
    async def single_user(self, ai: str):
        """
        single_user function
        """

    @abstractmethod
    async def user_list(self, ai: str):
        """
        user_list function
        """