from agents.base_agent import BaseAgent

class MathAgent(BaseAgent):
    name = "MathAgent"

    def handle(self, prompt: str) -> str:
        return f"[{self.name}] received: '{prompt}' — routing successful (real math logic coming in Phase 2)"
        