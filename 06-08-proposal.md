# Project Proposal: Multiagent Routing System

**To:** Mr.Bandugula
**From:** Sriram Balasubramanian  
**Date:** June 8, 2026  
**Timeline:** 3 Weeks (Target: End of June)  
**Stack:** Python 3, VS Code, Claude SDK, GitHub

---

## 1. Project Overview
The objective is to build a centralized multiagent system that routes diverse user queries to specialized agents. The core layout consists of a prompt-based router and three distinct operational agents handling mathematics/vision, statistical/data analysis, and machine learning execution. 

The final end state for the month is a single execution interface where a user can supply an arbitrary prompt, dataset, or image, and receive an output from the correct agent.

---

## 2. System Architecture & Core Components

```
                [ User Prompt / CSV File / Screenshot ]
                                  │
                                  ▼
                        ┌──────────────────┐
                        │    Router AI     │ (Intent Classification)
                        └────────┬─────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
   [ Agent 1 ]             [ Agent 2 ]             [ Agent 3 ]
  Math & Vision           Data Analyst             ML Engineer
 (Calc / Images)          (CSV Stats)         (Classification / Reg)
```

### Component Breakdown

1. **The Router**
   * **Role:** Acts as the gateway entry point, evaluates user input intent via language-based classification and forwards the execution payload to the appropriate downstream agent.
2. **Agent 1: Math & Vision Specialist**
   * **Scope:** Arithmetic, algebraic expressions, exponents, and up to high school-level calculus (derivatives, basic integration, limits).
   * **Inputs:** Raw text or images
3. **Agent 2: Data Analyst**
   * **Scope:** Descriptive stats, query filters, and frequency distributions.
   * **Inputs:** CSV files
   * **Example Queries:** Finding the frequency of "X" given specific data boundaries, calculating percentages of women matching a condition, or evaluating direct categorical differentials (men vs. women across a metric).
4. **Agent 3: ML Engineer**
   * **Scope:** End-to-end model building. Instantiates, trains, and evaluates a model automatically based on a given dataset and target feature.
   * **Inputs:** CSV files

---

## 3. Technology Stack & Evaluation
Researched three development tracks for orchestrating this routing layer:
1. **LangChain:** Mature but introduces heavy, opinionated abstractions that can muddle low-level debugging.
2. **LangGraph:** Perfect for complex, cyclic state-machine loops, but presents a steeper learning curve that is not needed for a hub-and-spoke configuration.
3. **Claude SDK (Anthropic):** Native, highly performant tool-calling capabilities and excellent, first-class image/vision handling.

**Decision:** For Phase 1, I will implement using the Claude SDK combined with Python scripting. This gives minimal framework overhead abd predictable latency. If agent-to-agent feedback loops expand significantly in Phase 2 or 3, can transition the routing layer into a stateful **LangGraph** setup.

---

## 4. Proposed Repository Structure

```
multiagent-system/
├── .gitignore
├── .env.example
├── README.md
├── requirements.txt
├── main.py                    
│
├── router/
│   ├── __init__.py
│   └── classification.py      # LLM logic to analyze prompt intent
│
├── agents/
│   ├── __init__.py
│   ├── base_agent.py          # Shared abstract base classes
│   ├── math_agent.py          # Agent 1: Math operations
│   ├── analysis_agent.py      # Agent 2: Pandas operations
│   └── ml_agent.py            # Agent 3: Scikit-learn pipelines
│
└── utils/
    ├── __init__.py
    ├── helpers.py             # Data cleaning /image parsing
    └── validation.py          # CSV structural checks
```

---

## 5. 4-Week Phased Implementation Plan

### Phase 1: Core Framework, Repository Setup,Routing Wireframe (Week 1)
* **Goal:** Establish a baseline working pipeline.
* **Tasks:**
  * Initialize github repo and configure local environments in VS Code.
  * Implement the core router logic utilizing prompt-based intent classification via Claude.
  * Construct basic class skeletons for all three agents so they can receive inputs and return primitive, mocked responses.
  * Write main.py to build out a command line interface connecting user inputs to the router layer.
* **Deliverable:** A functional end-to-end local system where typing a mathematical prompt prints an execution statement tracking directly to Agent 1.

### Phase 2: Functional Depth & Algorithmic Implementation (Weeks 2)
* **Goal:** Build real utility into each downstream node.
* **Tasks:**
  * **Agent 1:** Implement Base64 image encoding for screenshot support. Build structured  prompt chaining to enable up to calculus derivations.
  * **Agent 2:** Build dynamic pandas processing logic capable of generating data filtering matrices, frequency tracking, and multivariable group comparisons.
  * **Agent 3:** Code automated data preparation pipelines (train/test splits, numerical scaling) using scikit-learn to handle basic classification such as Logistic Regression, Random Forests, and regression targets.
* **Deliverable:** The system successfully parses real, messy datasets and multi-step image based calculus queries.

### Phase 3: Model Optimization & Deep Learning Foundations (Week 3)
* **Goal:** Harden the system, investigate cost reduction layers, and implement fundamental models.
* **Tasks:**
  * Fine-tune systemic error handling for malformed CSV arrays or blurred screenshots.
  * **Learning Deep Dive 1:** Explore taking a Small Language Model (SLM) and fine-tuning it explicitly on a custom classification dataset to handle our router decisions locally, minimizing API latency and call costs.
  * **Learning Deep Dive 2:** Build a primitive language model architecture completely from scratch using Python/NumPy to deeply unpack attention mechanisms, tensor operations, and backpropagation patterns, feeding these back into our prompt architecture optimization.
* **Deliverable:** Production-ready multiagent pipeline, optimized infrastructure, and a final recorded walkthrough on loom.

---

## 6. Git Workflow & Collaboration Plan

To maintain clear execution states and keep Mr.Bandugula aligned as a reviewer, I will follow a clean branch-and-merge standard:
1. **Branch Initialization:** Push this finalized markdown file up on a dedicated branch named `proposal`.
2. **Review & Sync:** Open a Pull Request targeted directly into Vikram's branch for review, commentary, and alignment before executing code.
3. **Feature Branching:** Every distinct phase will map to its own short lived feature branch (`phase1-router`, `phase2-agents`) to isolate development tracking.
4. **Final Delivery:** Upon completion of all features at the close of the month, I will record and push a thorough loom video highlighting the execution paths, code architecture, and live prompt handling.
