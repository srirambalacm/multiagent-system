# Multiagent Routing System

A multiagent system that routes natural language queries to specialized agents using LLM-based intent classification.

## Agents

- Math Agent: solves arithmetic, algebra, and calculus problems with step-by-step reasoning
- Data Analyst Agent: profiles CSV data (stats, type breakdowns, frequency counts) and surfaces what stands out
- ML Engineer Agent: builds classification or regression models from CSV data and reports performance and feature importances
- Research Agent: extracts a YouTube transcript, identifies key concepts, finds related arXiv papers, and builds a concept mind map
- Walkthrough Agent: turns a YouTube transcript into a timestamped guide with links that jump to each key moment

## Routing

Two-stage router:

1. URL guard (deterministic): prompts containing a YouTube link are excluded from the Math/Data/ML classifier entirely; a dedicated classifier then picks Research or Walkthrough. This exists because a video prompt once slipped through to the Math Agent and produced a hallucinated summary of a video it never saw.
2. LLM classification: all other prompts are classified into MATH, DATA_ANALYSIS, or ML, with keyword matching as a fallback if the API is unavailable.

For example, "can you put together something that forecasts income from the other columns" has no ML keyword, so the keyword router defaults it to MATH. The LLM router correctly recognizes it as a modeling request and returns ML.

Measured across a labeled set of prompts, this cut the misrouting rate from 18% (keyword-only) to 2% (LLM with keyword fallback).

## Video Learning Pipeline

Research and Walkthrough share one pipeline: YouTube URL -> timestamped transcript -> LLM concept extraction. From there, Research searches arXiv per concept and renders an HTML mind map; Walkthrough maps each concept to its first timestamp and emits jump links.

## Setup

```
git clone https://github.com/srirambalacm/multiagent-system.git
cd multiagent-system
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Add a `.env` file with `GEMINI_API_KEY=your_key_here` (gitignored).

## Usage

```
python main.py
```

Data Analyst and ML agents will prompt for a CSV path. Research and Walkthrough read the YouTube URL from your prompt directly.

Examples:
- `what is the derivative of x^2` -> Math
- `analyze this dataset` -> Data Analyst
- `build a model to predict gender` -> ML
- `I want to understand this video: <url>` -> Research
- `walk me through this video: <url>` -> Walkthrough

## Architecture

- `main.py`: CLI loop, routing dispatch
- `router/classification.py`: URL guard, LLM router, keyword fallback
- `agents/`: math, analysis, ml, research, walkthrough
- `utils/llm.py`: shared Gemini client with in-session caching
- `utils/youtube.py`: transcript and concept extraction
- `utils/research.py`: arXiv search (rate-limited, retry with backoff)
- `utils/visualize.py`: HTML mind-map renderer
- `outputs/`: generated artifacts, gitignored

All agents implement a common `handle(prompt, csv_path=None)` interface, so new agents can be added without changing the routing loop.

## Engineering Notes

- Batched the Research Agent's per-concept Gemini calls into one call, cutting API usage from ~7 calls to 2 per run.
- Added in-session prompt caching to avoid redundant calls.
- Made the YouTube URL guard a code-level rule instead of an LLM decision, since misclassification there caused hallucinated output.
- Wrapped external calls (Gemini, arXiv, YouTube) to degrade gracefully instead of crashing.

## Stack

Python 3.13, Google Gemini (`google-genai`), scikit-learn, pandas, `youtube-transcript-api`, arXiv API, python-dotenv
