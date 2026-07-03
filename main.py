from router.classification import classify
from agents.math_agent import MathAgent
from agents.analysis_agent import AnalysisAgent
from agents.ml_agent import MLAgent
from agents.research_agent import ResearchAgent
from agents.walkthrough_agent import WalkthroughAgent

AGENTS = {
    "MATH": MathAgent(),
    "DATA_ANALYSIS": AnalysisAgent(),
    "ML": MLAgent(),
    "RESEARCH": ResearchAgent(),
    "WALKTHROUGH": WalkthroughAgent(),
}

# Agents that operate on a CSV file (prompt for a path)
CSV_AGENTS = {"DATA_ANALYSIS", "ML"}


def run():
    print("Multiagent System (Phase 3) — type 'quit' to exit\n")
    while True:
        prompt = input("You: ").strip()
        if prompt.lower() in ("quit", "exit"):
            break

        route = classify(prompt)
        agent = AGENTS[route]
        print(f"Router → {route}")

        csv_path = None
        if route in CSV_AGENTS:
            while not csv_path:
                csv_path = input("Path to CSV file: ").strip()
                if not csv_path:
                    print("  (A file path is required for this agent.)")

        print(agent.handle(prompt, csv_path) + "\n")


if __name__ == "__main__":
    run()