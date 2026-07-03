import os
import pandas as pd
from agents.base_agent import BaseAgent


class AnalysisAgent(BaseAgent):
    name = "AnalysisAgent"

    def handle(self, prompt: str, csv_path: str = None) -> str:
        if not csv_path:
            return f"[{self.name}] I need a CSV file to analyze. Please provide a file path."
        if not os.path.exists(csv_path):
            return f"[{self.name}] Could not find file: {csv_path}"
        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            return f"[{self.name}] Could not read the CSV: {e}"

        summary = self.profile(df)
        insight = self.interpret(summary)
        return summary + "\n\n" + insight

    def profile(self, df) -> str:
        lines = []
        lines.append(f"[{self.name}] Data summary")
        lines.append(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        lines.append("")

        lines.append("Columns:")
        for col in df.columns:
            lines.append(f"  - {col} ({df[col].dtype})")
        lines.append("")

        numeric = df.select_dtypes(include="number")
        if not numeric.empty:
            lines.append("Numeric columns:")
            lines.append(numeric.describe().round(2).to_string())
            lines.append("")

        categorical = df.select_dtypes(exclude="number")
        if not categorical.empty:
            lines.append("Categorical columns:")
            for col in categorical.columns:
                lines.append(f"  {col}:")
                for val, cnt in df[col].value_counts().items():
                    lines.append(f"    {val}: {cnt}")
            lines.append("")

        return "\n".join(lines)

    def interpret(self, summary: str) -> str:
        from utils.llm import ask_gemini
        prompt = (
            "Here is a statistical profile of a dataset. In 3-4 sentences, plainly explain "
            "what stands out — balance, ranges, anything notable. No greetings.\n\n" + summary
        )
        try:
            return "What this means:\n" + ask_gemini(prompt).strip()
        except Exception as e:
            return f"(Insight unavailable — model error: {e})"