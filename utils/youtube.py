from youtube_transcript_api import YouTubeTranscriptApi
import re


def extract_video_id(url: str) -> str:
    """Pull the video ID from a YouTube URL (handles watch?v=, youtu.be, embed)."""
    patterns = [
        r"(?:v=|/watch\?v=)([0-9A-Za-z_-]{11})",
        r"(?:youtu\.be/)([0-9A-Za-z_-]{11})",
        r"(?:embed/)([0-9A-Za-z_-]{11})",
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    if re.fullmatch(r"[0-9A-Za-z_-]{11}", url.strip()):
        return url.strip()
    raise ValueError(f"Could not extract a video ID from: {url}")


def get_transcript(url: str):
    """Return a list of {text, start, duration} segments for a YouTube video."""
    video_id = extract_video_id(url)
    ytt_api = YouTubeTranscriptApi()
    fetched = ytt_api.fetch(video_id)
    return fetched.to_raw_data()


def transcript_to_text(segments) -> str:
    """Flatten transcript segments into plain text (no timestamps)."""
    return " ".join(seg["text"] for seg in segments)


def build_timestamped_text(segments) -> str:
    """Flatten transcript into text with [seconds] markers, so an LLM can
    reference specific moments. Example: '[4] This is a 3. [10] Your brain...'"""
    return " ".join(f"[{int(seg['start'])}] {seg['text']}" for seg in segments)


def format_timestamp(seconds: float) -> str:
    """Convert seconds to M:SS or H:MM:SS for display."""
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def extract_concepts(segments) -> list:
    """Use Gemini to pull the key concepts from a transcript. Returns a list of concept strings."""
    from utils.llm import ask_gemini
    import json

    text = transcript_to_text(segments)[:12000]

    prompt = (
        "Below is a transcript from an educational video. Identify the main concepts "
        "taught in it. Return ONLY a JSON array of short concept names (strings), "
        "no explanation, no markdown fences. Example: [\"backpropagation\", \"gradient descent\"]\n\n"
        f"Transcript:\n{text}"
    )
    raw = ask_gemini(prompt).strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return [raw]


def make_search_queries(concepts: list, topic: str) -> dict:
    """Generate arXiv search queries for ALL concepts in a SINGLE Gemini call.
    Returns a dict mapping concept -> query. Falls back to bare concepts on failure."""
    from utils.llm import ask_gemini
    import json

    concept_list = "\n".join(f"- {c}" for c in concepts)
    prompt = (
        f"A learner is studying '{topic}'. For each concept below, generate a concise "
        f"arXiv search query (3-6 words) to find relevant academic papers. Favor the "
        f"specific concept over the general topic.\n"
        f"Return ONLY a JSON object mapping each concept to its query, no markdown.\n"
        f'Example: {{"backpropagation": "backpropagation gradient neural nets"}}\n\n'
        f"Concepts:\n{concept_list}"
    )
    raw = ask_gemini(prompt).strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    try:
        mapping = json.loads(raw)
        # Ensure every concept has a query (fall back to the concept itself)
        return {c: mapping.get(c, c) for c in concepts}
    except json.JSONDecodeError:
        return {c: c for c in concepts}


def find_concept_segments(segments) -> list:
    """Use Gemini to map key concepts to the timestamp where each is explained.
    Returns a list of {concept, timestamp_seconds, why} dicts."""
    from utils.llm import ask_gemini
    import json

    timestamped = build_timestamped_text(segments)[:14000]

    prompt = (
        "Below is a video transcript. Each segment is prefixed with its start time "
        "in seconds, like [123]. Identify the most important concepts taught, and for "
        "each, give the timestamp (in seconds, taken from the [] markers) where that "
        "concept is FIRST explained, plus a one-sentence reason it matters.\n"
        "Return ONLY a JSON array, no markdown, in this exact shape:\n"
        '[{"concept": "...", "timestamp_seconds": 123, "why": "..."}]\n'
        "Order the array by timestamp ascending. Pick 5-8 of the most important moments.\n\n"
        f"Transcript:\n{timestamped}"
    )
    raw = ask_gemini(prompt).strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return [{"concept": "parse_error", "timestamp_seconds": 0, "why": raw[:200]}]