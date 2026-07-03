class BaseAgent:
    name = "BaseAgent"

    def handle(self, prompt: str, csv_path: str = None) -> str:
        raise NotImplementedError