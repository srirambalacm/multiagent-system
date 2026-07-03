# Multiagent Routing System

A multiagent system that routes natural-language queries to specialized agents based on intent.
A central router classifies each request and dispatches it to the agent best suited to handle it.

## Agents

- **Math Agent** — solves arithmetic, algebra, and calculus problems with step-by-step reasoning (LLM-based)
- **Data Analyst Agent** — profiles CSV data (descriptive stats, type breakdowns, frequency counts) and generates an interpretation of what stands out
- **ML Engineer Agent** — builds classification or regression models from CSV data and reports performance/feature importances
- **Research Agent** — takes a learning goal anchored to a YouTube video: extracts the transcript, identifies the key concepts, finds related arXiv papers, and builds a concept mind map (saved as JSON + a rendered HTML visual)
- **Walkthrough Agent** — analyzes a YouTube video's transcript and produces a timestamped guide to its key moments, each with a one-line explanation and a link that jumps directly to that second of the video

## Project Status

**Phase 3 (current):** Two learning-focused agents added on top of a shared YouTube
transcript pipeline. Video-bearing prompts are routed deterministically to prevent
misrouting. Outputs are saved as file artifacts (JSON / HTML) in `outputs/`.

**Phase 2:** LLM-based intent routing with keyword fallback; Math, Data Analyst, and
ML agents fully implemented. *(complete)*

**Phase 1:** Keyword-based router with mocked agent responses. *(complete)*

## Routing

The router works in two stages:

1. **URL guard (deterministic).** If a prompt contains a YouTube link, it is a video
   task by definition — routing never falls through to the Math/Data/ML agents. A
   dedicated classifier then decides between RESEARCH (understand the topic: papers,
   concept map) and WALKTHROUGH (navigate the video: key moments, timestamps).
2. **LLM intent classification.** All other prompts are classified by an LLM into
   MATH / DATA_ANALYSIS / ML, with the original keyword router retained as a fallback
   when the API is unavailable.

**Example — a prompt the keyword router misroutes:**

> "can you put together something that forecasts income from the other columns"

| Router | Result |
|--------|--------|
| Keyword | `MATH` (no ML keyword present → defaults to math) |
| LLM | `ML` (correctly recognizes a modeling request) |

**Why the URL guard exists:** during testing, a video prompt that slipped through to
the Math Agent produced a confident, detailed summary of a video the agent had never
accessed — a hallucination. Constraining URL-bearing prompts in code (rather than
trusting classification alone) removes that failure mode entirely.

## The Video Learning Pipeline

Both learning agents share one foundation:
YouTube URL → timestamped transcript → LLM concept extraction
│                            │
Walkthrough Agent                  Research Agent
key moments + jump links        arXiv search per concept
(JSON artifact)                 mind map (JSON + HTML visual)

- Transcripts are fetched with `youtube-transcript-api` (timestamps preserved).
- The Research Agent generates one focused arXiv query per concept, deduplicates
  papers across concepts, and renders the result as a standalone HTML mind map.
- The Walkthrough Agent maps each key concept to the timestamp where it is first
  explained and emits `youtube.com/watch?v=ID&t=Ns` links that open the video at
  that exact moment.

## Setup
git clone https://github.com/srirambalacm/multiagent-system.git
cd multiagent-system
py -3.13 -m venv .venv
..venv\Scripts\Activate.ps1
pip install -r requirements.txt

Create a `.env` file with your API key (gitignored — never committed):
GEMINI_API_KEY=your_key_here

## Usage
python main.py

Type a prompt and the router will classify it and dispatch to the correct agent.
The Data Analyst and ML Engineer agents will ask for a CSV file path. The Research
and Walkthrough agents read the YouTube URL directly from your prompt.
Type `quit` to exit.

**Try these:**

- `what is the derivative of x^2` → Math
- `analyze this dataset` → Data Analyst (give it `sample_data.csv`)
- `build a model to predict gender` → ML (classification)
- `forecast income from the other columns` → ML (regression)
- `I want to understand this video: <YouTube URL>` → Research (mind map + papers)
- `walk me through this video: <YouTube URL>` → Walkthrough (timestamped key moments)

## Architecture
main.py                    CLI loop, routing dispatch
router/classification.py   URL guard + LLM router + keyword fallback
agents/                    math, analysis, ml, research, walkthrough (+ base_agent)
utils/llm.py               shared Gemini client with in-session caching
utils/youtube.py           transcript extraction, concept extraction, timestamping
utils/research.py          arXiv search (rate-limited, retry with backoff)
utils/visualize.py         HTML mind-map renderer
outputs/                   generated artifacts (JSON / HTML), gitignored

All agents share a common `handle(prompt, csv_path=None)` interface, so the router
dispatches uniformly and new agents can be added without changing the loop.

## Engineering Notes

Decisions made along the way that shaped the system:

- **Batched LLM calls.** The Research Agent originally made one Gemini call per
  concept to generate search queries. These are now batched into a single call,
  cutting the agent's API usage from ~7 calls to 2 per run.
- **In-session prompt caching.** Identical prompts within a session return cached
  results instead of re-hitting the API (`utils/llm.py`).
- **Deterministic routing for critical constraints.** The YouTube URL guard is a
  code-level rule, not an LLM judgment — classification errors on video prompts
  previously caused hallucinated output, so that path is now impossible.
- **Graceful degradation.** Every external call (Gemini, arXiv, YouTube) is wrapped
  so failures return a readable message instead of crashing: the LLM router falls
  back to keywords, the Data Analyst returns its statistical profile even if the
  insight layer fails, and arXiv requests retry with backoff per its rate guidance.
- **API etiquette.** arXiv requests carry a descriptive User-Agent and a 3-second
  spacing between calls, per their published terms of use.

## Stack

Python 3.13 · Google Gemini (`google-genai`) · scikit-learn · pandas ·
`youtube-transcript-api` · arXiv API · python-dotenv