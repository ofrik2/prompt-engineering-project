# Architecture Document

Project: Prompt Engineering Evaluation & Optimization System  
Author: YOUR_NAME_HERE  
Date: DATE_HERE

---

## 1. Purpose

This document describes the structure of the project and how the main parts of the code fit together.  
The system is a **research tool** that:

- generates tasks and prompts
- sends them to an LLM
- collects the answers
- evaluates the results

---

## 2. High-Level View

Main actors:

- **User (you)** – runs experiments and looks at results.
- **Prompt Lab (this project)** – Python package that controls everything.
- **LLM API** – external model (e.g., OpenAI) that actually answers prompts.
- **File system** – stores datasets, configs, and results.

Flow (very simplified):

1. You run a script (for example in the future: `python -m prompt_lab.run_experiment`).
2. The script:
   - loads config
   - loads or generates a dataset of tasks
   - applies different prompting methods (baseline, CoT, etc.)
   - sends prompts to the LLM
   - saves outputs and metrics to `results/`

---

## 3. Main Folders and What They Mean

- `src/prompt_lab/dataset/`  
  Code to **create or load datasets**:
  - tasks for sentiment, math, logic
  - different prompt lengths (short/medium/long)

- `src/prompt_lab/methods/`  
  Code for **different prompting strategies**:
  - baseline
  - Chain of Thought (CoT)
  - ReAct
  - Tree of Thoughts (ToT)
  - Few-shot

- `src/prompt_lab/evaluator/`  
  Code to **compute metrics**:
  - accuracy
  - maybe distance, entropy, cost
  - saves tables and maybe plots

- `src/prompt_lab/utils/`  
  Helpers:
  - logger
  - LLM client (calls the API)
  - shared small utilities

- `src/prompt_lab/config/`  
  Code to **load and validate config files** (which model, which methods, etc.).

- `data/`  
  Input datasets (JSON/CSV) – either created by us or saved for reuse.

- `results/`  
  Outputs: CSV/JSON with metrics, logs, plots.

---

## 4. Planned Data Objects (very high level)

Later in code we will probably have:

- `Task` – one question/problem + the correct answer.
- `PromptVariant` – how we phrase the task (short/medium/long).
- `RunResult` – what happened when we asked the LLM (answer, tokens, etc.).
- `MetricsSummary` – statistics over many results.

---

## 5. Next Steps

1. Implement a **dataset generator** in `src/prompt_lab/dataset/`.
2. Implement a **baseline prompting method** in `src/prompt_lab/methods/`.
3. Implement an **evaluator** to compute accuracy and save results.

This document is a starting point and can be expanded as the project grows.
