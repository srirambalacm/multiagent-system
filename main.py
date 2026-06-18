from router.classification import classify
from agents.math_agent import MathAgent
from agents.analysis_agent import AnalysisAgent
from agents.ml_agent import MLAgent

AGENTS = {
    "MATH": MathAgent(),
    "DATA_ANALYSIS": AnalysisAgent(),
    "ML": MLAgent(),
}

def run():
    print("Multiagent System (Phase 1) — type 'quit' to exit\n")
    while True:
        prompt = input("You: ").strip()
        if prompt.lower() in ("quit", "exit"):
            break
        route = classify(prompt)
        agent = AGENTS[route]
        print(f"Router → {route}")
        print(agent.handle(prompt) + "\n")

if __name__ == "__main__":
    run()