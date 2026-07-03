import re
from utils.llm import ask_gemini

VALID = {"MATH", "DATA_ANALYSIS", "ML", "RESEARCH", "WALKTHROUGH"}

_YOUTUBE_RE = re.compile(r"(youtube\.com/watch|youtu\.be/)")


def classify(prompt: str) -> str:
    """Route a prompt to an agent. Tries the LLM first, falls back to keywords."""
    # Hard rule: any prompt with a YouTube link is a video task, never MATH/ML/DATA.
    if _YOUTUBE_RE.search(prompt):
        return _classify_video_intent(prompt)

    instruction = (
        "You are a router for a multi-agent system. Read the user's request and "
        "reply with EXACTLY ONE of these labels and nothing else:\n"
        "MATH - solving equations, calculus, arithmetic, math problems\n"
        "DATA_ANALYSIS - profiling, summarizing, or describing a dataset/CSV\n"
        "ML - training or building a predictive model from data\n\n"
        f"Request: {prompt}\n\nLabel:"
    )
    try:
        answer = ask_gemini(instruction).strip().upper()
        for label in {"MATH", "DATA_ANALYSIS", "ML"}:
            if label in answer:
                return label
        return classify_keywords(prompt)
    except Exception:
        return classify_keywords(prompt)


def _classify_video_intent(prompt: str) -> str:
    """A YouTube URL is present — decide RESEARCH vs WALKTHROUGH."""
    instruction = (
        "A user shared a YouTube video. Classify their intent as exactly one word.\n"
        "RESEARCH: they want to learn the subject in depth — related papers, concepts, "
        "background reading, a concept map. Keywords: understand, learn, papers, research, concepts.\n"
        "WALKTHROUGH: they want to navigate THIS video efficiently — which parts to watch, "
        "key moments, timestamps, skip to the important bits. Keywords: walk through, key moments, "
        "timestamps, watch, parts.\n"
        "If they want to go BEYOND the video to the broader topic, choose RESEARCH. "
        "If they want to move THROUGH the video itself, choose WALKTHROUGH.\n"
        "Reply with exactly one word: RESEARCH or WALKTHROUGH.\n\n"
        f"Request: {prompt}\n\nAnswer:"
    )
    try:
        answer = ask_gemini(instruction).strip().upper()
        if "WALKTHROUGH" in answer:
            return "WALKTHROUGH"
        if "RESEARCH" in answer:
            return "RESEARCH"
    except Exception:
        pass
    p = prompt.lower()
    walk = ["walk", "key moment", "timestamp", "important part", "which part", "navigate", "skip to", "watch"]
    if any(w in p for w in walk):
        return "WALKTHROUGH"
    return "RESEARCH"

def classify_keywords(prompt: str) -> str:
    """Keyword router — fallback when the LLM is unavailable."""
    p = prompt.lower()
    ml_words = ["model", "predict", "train", "classification", "regression", "machine learning"]
    data_words = ["csv", "percent", "frequency", "compare", "average", "how many",
                  "dataset", "analyze", "analysis", "summarize", "profile"]
    math_words = ["solve", "derivative", "integral", "calculate", "simplify", "equation", "*", "^", "="]

    if any(w in p for w in ml_words):
        return "ML"
    if any(w in p for w in data_words):
        return "DATA_ANALYSIS"
    if any(w in p for w in math_words):
        return "MATH"
    return "MATH"