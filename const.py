from colorama import Fore, Style

class Const:
    COLOR_WARNING = Fore.YELLOW
    COLOR_ERROR = Fore.RED

    RESET_ALL = Style.RESET_ALL

    PROMPTS_PATH = 'prompts.json'
    HISTORY_PATH = 'history.json'

    platform_options_list = ["Twitter", "LinkedIn"]
    ai_options_list = ["OpenAI GPT-3.5", "OpenAI GPT-4o", "Mistral (local)", "Llama3 (local)"]
    generation_options_list_twitter = ["Email", "SMS", "Vishing script", "Twitter DM", "Twitter post", "Twitter reply", "Pretext"]
    generation_options_list_linkedin = ["Email", "SMS", "Vishing script", "Pretext"]
    payload_options_list = ["Login page", "Attachment", "Download Link", "Else"]
    user_options_list = ["Single user", "User list"]