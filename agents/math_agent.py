from agents.base_agent import BaseAgent
from utils.llm import ask_gemini


class MathAgent(BaseAgent):
    name = "MathAgent"

    def handle(self, prompt: str, csv_path: str = None) -> str:
        instruction = (
            "You are a math solver. Solve concisely with clear steps. "
            "No greetings, no sign-offs, no encouragement.\n\n"
            f"Problem: {prompt}"
        )
        try:
            return f"[{self.name}] {ask_gemini(instruction)}"
        except Exception as e:
            return f"[{self.name}] Error reaching the model: {e}"