from .Const import Const

class Helper:
    def __init__(self) -> None:
        pass

    # ! --------------------------------------------------------------------------------
    # ! Static
    # ! --------------------------------------------------------------------------------
    @staticmethod
    def print_options(options_list: list):
        for i in range(len(options_list)):
            print(f"{Const.COLOR_GREEN}{i+1}. {options_list[i]}{Const.RESET_ALL}")

    @staticmethod
    def get_valid_input(size: int):
        bottom = 1
        top = size
        input_value = input("\nOption: ")
        try:
            input_value = int(input_value)
        except ValueError:
            print(f"{Const.COLOR_ERROR}Invalid option{Const.RESET_ALL}")
            return Helper.get_valid_input(size)
        if input_value < bottom or input_value > top:
            print(f"{Const.COLOR_ERROR}Invalid option{Const.RESET_ALL}")
            input_value = Helper.get_valid_input(size)
        return input_value
    
    @staticmethod
    def selection_options(options: list):
        if not options:
            raise ValueError("Options list cannot be empty")
        print("\n\nPlease select an option:")
        Helper.print_options(options)
        return Helper.get_valid_input(len(options))