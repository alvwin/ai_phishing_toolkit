from Const import Const

class Helper:
    def __init__(self) -> None:
        pass

    # ! --------------------------------------------------------------------------------
    # ! Static
    # ! --------------------------------------------------------------------------------
    @staticmethod
    def print_options(self, options_list: list):
        for i in range(len(options_list)):
            print(f"{Const.GREEN}{i+1}. {options_list[i]}{Const.RESET_ALL}")

    def get_valid_input(self, size: int):
        bottom = 1
        top = size
        input_value = input("\nOption: ")
        try:
            input_value = int(input_value)
        except ValueError:
            print(f"{Const.COLOR_ERROR}Invalid option{Const.RESET_ALL}")
            return self.get_valid_input(size)
        if input_value < bottom or input_value > top:
            print(f"{Const.COLOR_ERROR}Invalid option{Const.RESET_ALL}")
            input_value = self.get_valid_input(size)
        return input_value