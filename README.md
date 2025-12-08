# Prompt Engineering Evaluation & Optimization System

This repository implements a hybrid **software + research** project for evaluating and improving
LLM prompt-engineering techniques (Baseline, Chain of Thought, ReAct, Tree of Thoughts, Few-shot).

## Repository Structure

- `src/prompt_lab/` — main Python package
  - `dataset/` — dataset generation and loading utilities
  - `methods/` — implementations of prompting strategies (baseline, CoT, ReAct, ToT, etc.)
  - `evaluator/` — metrics computation, aggregation, and reporting
  - `utils/` — shared helper functions
  - `config/` — configuration loading and validation
- `tests/` — unit and integration tests
- `data/` — input datasets (JSON/CSV)
- `results/` — experiment outputs (CSV, JSON, plots)
- `docs/` — PRD, architecture, and additional documentation
- `notebooks/` — analysis notebooks
- `config/` — configuration files (YAML/JSON)
- `assets/` — images and static resources

## Getting Started

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run tests:

   ```bash
   pytest
   ```

4. Run a simple demo experiment (to be implemented):

   ```bash
   python -m prompt_lab.demo
   ```

Detailed usage instructions will be added as the implementation progresses.
