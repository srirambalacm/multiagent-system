class BaseAgent:
    name = "BaseAgent"

    def handle(self, prompt: str) -> str:
        raise NotImplementedError