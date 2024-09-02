class AIRender:
    def __init__(self, model: str) -> None:
        if model.lower() == "openai gpt-4o" or model.lower() == "openai gpt-3.5":
            from .AIModel.OpenAI import OpenAI
            self.model = OpenAI()
        elif model.lower() == "llama3 (local)" or model.lower() == "mistral (local)":
            from .AIModel.Ollama import Ollama
            self.model = Ollama()