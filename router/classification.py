def classify(prompt: str) -> str:
    """Decide which agent should handle prompt.
    Returns: 'MATH','DATA_ANALYSIS', or 'ML'
    """
    p = prompt.lower()
    ml_words = ["model", "predict", "train", "classification", "regression", "machine learning"]
    data_words = ["csv", "percent", "frequency", "compare", "average", "how many", "dataset"]
    math_words = ["solve", "derivative", "integral", "calculate", "simplify", "equation", "+", "-", "*", "^", "="]

    if any(w in p for w in ml_words):
        return "ML"
    if any(w in p for w in data_words):
        return "DATA_ANALYSIS"
    if any(w in p for w in math_words):
        return "MATH"
    return "MATH"  # default fallback for now