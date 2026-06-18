from agents.base_agent import BaseAgent

class MLAgent(BaseAgent):
    name = "MLAgent"

    def handle(self, prompt: str) -> str:
        return f"[{self.name}] received: '{prompt}' — routing successful (real ML logic coming in Phase 2)"