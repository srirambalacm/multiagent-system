# Multiagent Routing System

Multiagent system that routes user queries to specialized agents based on intent.
A central router classifies each request and dispatches it to the correct agent.

## Agents

- **Math & Vision Agent** — arithmetic, algebra, and up to high-school calculus, accepts text and images
- **Data Analyst Agent** — descriptive stats, frequency counts, and group comparisons on CSV data
- **ML Engineer Agent** — builds classification and regression models from CSV data

## Project Status

**Phase 1 (current):** Working router with keyword-based intent classification and
mocked agent responses, runnable end to end through CLI.

## Setup
git clone https://github.com/srirambalacm/multiagent-system.git
cd multiagent-system
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

## Usage

python main.py

Type a prompt and the router will classify it and route to the correct agent.
Type quit to exit.

## Stack

Python 3.13 · Claude SDK · scikit-learn · pandas · GitHub