import os
from dotenv import load_dotenv
from google import genai

_here = os.path.dirname(__file__)
_root = os.path.dirname(_here)
load_dotenv(os.path.join(_root, ".env"))
load_dotenv(os.path.join(_root, "agents", ".env"))

_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

MODEL = "gemini-3.5-flash"

# identical prompts return the cached result
# instead of making a duplicate API call 
_cache = {}


def ask_gemini(prompt: str, use_cache: bool = True) -> str:
    """Send a prompt to Gemini and return the text response.
    Caches identical prompts within a session to conserve quota."""
    if use_cache and prompt in _cache:
        return _cache[prompt]
    response = _client.models.generate_content(model=MODEL, contents=prompt)
    text = response.text
    if use_cache:
        _cache[prompt] = text
    return text