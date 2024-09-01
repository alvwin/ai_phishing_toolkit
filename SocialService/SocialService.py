from abc import abstractmethod

from const import Const

class SocialService:
    def __init__(self) -> None:
        pass

    # ! --------------------------------------------------------------------------------
    # ! Private
    # ! --------------------------------------------------------------------------------

    def _print_options(self, options_list: list):
        for i in range(len(options_list)):
            print(f"{Const.GREEN}{i+1}. {options_list[i]}{Const.RESET_ALL}")

    def _get_valid_input(self, size: int):
        bottom = 1
        top = size
        input_value = input("\nOption: ")
        try:
            input_value = int(input_value)
        except ValueError:
            print(f"{Const.COLOR_ERROR}Invalid option{Const.RESET_ALL}")
            return self._get_valid_input(size)
        if input_value < bottom or input_value > top:
            print(f"{Const.COLOR_ERROR}Invalid option{Const.RESET_ALL}")
            input_value = self._get_valid_input(size)
        return input_value

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