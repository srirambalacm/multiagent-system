from agents.base_agent import BaseAgent

class AnalysisAgent(BaseAgent):
    name = "AnalysisAgent"

    def handle(self, prompt: str) -> str:
        return f"[{self.name}] received: '{prompt}' — routing successful (real analysis logic coming in Phase 2)"