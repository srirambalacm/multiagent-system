"""Smoke tests for the multiagent system.
Run from the project root:  python -m tests.test_agents
Covers the offline/cheap paths. Video + LLM agents are exercised separately
(see test_video.py) since they consume API quota.
"""
import os
import sys

# Allow running from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

passed = 0
failed = 0


def check(name, condition):
    global passed, failed
    if condition:
        print(f"  PASS  {name}")
        passed += 1
    else:
        print(f"  FAIL  {name}")
        failed += 1


def test_router_keywords():
    print("\n[Router — keyword fallback]")
    from router.classification import classify_keywords
    check("ML intent", classify_keywords("build a model to predict price") == "ML")
    check("Data intent", classify_keywords("analyze this dataset") == "DATA_ANALYSIS")
    check("Math intent", classify_keywords("solve for x") == "MATH")


def test_analysis_agent():
    print("\n[Data Analyst Agent]")
    from agents.analysis_agent import AnalysisAgent
    agent = AnalysisAgent()
    # Missing file → graceful message, not a crash
    out = agent.handle("analyze", "does_not_exist.csv")
    check("Handles missing file gracefully", "Could not find" in out)
    # Real file → produces a profile
    if os.path.exists("sample_data.csv"):
        out = agent.handle("analyze", "sample_data.csv")
        check("Profiles a real CSV", "Data summary" in out)
    else:
        print("  SKIP  sample_data.csv not found")


def test_ml_agent():
    print("\n[ML Engineer Agent]")
    from agents.ml_agent import MLAgent
    agent = MLAgent()
    out = agent.handle("build a model", "does_not_exist.csv")
    check("Handles missing file gracefully", "Could not find" in out)
    if os.path.exists("sample_data.csv"):
        out = agent.handle("predict income", "sample_data.csv")
        check("Builds a model on a real CSV", "predict 'income'" in out or "Building a model" in out)
    else:
        print("  SKIP  sample_data.csv not found")


def test_youtube_utils():
    print("\n[YouTube utils — no network]")
    from utils.youtube import extract_video_id, format_timestamp
    check("Extracts ID from watch URL",
          extract_video_id("https://www.youtube.com/watch?v=aircAruvnKk") == "aircAruvnKk")
    check("Extracts ID from youtu.be",
          extract_video_id("https://youtu.be/aircAruvnKk") == "aircAruvnKk")
    check("Formats timestamp", format_timestamp(125) == "2:05")


if __name__ == "__main__":
    print("Running multiagent system tests...")
    test_router_keywords()
    test_analysis_agent()
    test_ml_agent()
    test_youtube_utils()
    print(f"\n{'='*40}\nResults: {passed} passed, {failed} failed\n{'='*40}")
    sys.exit(1 if failed else 0)