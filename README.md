
# Prompt Engineering Project

This project provides a Python-based experimental framework for evaluating how
different prompting strategies and prompt lengths affect LLM performance on
constrained classification tasks.

The repository is designed to function both as:
- a **command-line tool** for running reproducible experiments, and
- a **Python package** that can be imported into other Python scripts.

This README is divided into two parts:
1. **Package usage and reproducibility**
2. **Experimental results and interpretation**

---

# Part I — Package Usage & Reproducibility

## Project Structure

The project follows a standard `src/`-based Python package layout:

```
prompt-engineering-project/
├── pyproject.toml
├── src/
│   └── prompt_lab/
├── config/
├── data/
├── results/
├── analysis_results/
└── README.md
```

All commands must be executed from the **project root directory**.

---

## Installation

```bash
git clone https://github.com/ofrik2/prompt-engineering-project.git
cd prompt-engineering-project

python -m venv .venv
source .venv/bin/activate

pip install -e .
```

Installing in editable mode registers the `prompt-lab` CLI command and allows the
project to be used as a Python package.

---

## Running the Project (CLI)

### Main entry point

```bash
prompt-lab full --provider dummy
```

This command:
1. Runs all experiments (baseline, few-shot, Chain-of-Thought)
2. Executes all analysis scripts
3. Generates plots and an HTML analysis report

---

## Choosing an LLM Provider

Supported providers:
- `dummy` — deterministic local stub (no API calls)
- `azure` — Azure OpenAI

Example:

```bash
prompt-lab full --provider azure
```

Command-line arguments override configuration values.

---

## Azure OpenAI Configuration

To use Azure OpenAI, create a `.env` file in the project root (based on
`.env.example`) and provide your own credentials:

```env
AZURE_OPENAI_ENDPOINT="https://<your-resource>.openai.azure.com/"
AZURE_OPENAI_API_KEY="<your-api-key>"
AZURE_OPENAI_API_VERSION="2024-02-15-preview"
AZURE_OPENAI_DEPLOYMENT="<deployment-name>"
```

---

## Using a Custom Dataset

Users may supply their own dataset in JSON format.

### Expected format

```json
[
  {
    "id": "task_001",
    "task_type": "sentiment",
    "prompt": "Classify the sentiment: I loved the movie.",
    "ground_truth": "positive"
  }
]
```

### Running with a custom dataset

```bash
prompt-lab full --provider dummy --dataset-path data/my_tasks.json
```

---

## Running Individual Stages

Run experiments only:

```bash
prompt-lab run-all --provider dummy
```

Run analysis only:

```bash
prompt-lab analyze
```

Generate the HTML report only:

```bash
prompt-lab report
```

---

## Using the Project as a Python Library

After installation (`pip install -e .`), the project can also be imported into
Python scripts:

```python
from prompt_lab.config.loader import load_config
from prompt_lab.pipeline import run_full_pipeline

cfg = load_config()
run_full_pipeline(cfg)
```

---

# Part II — Experimental Results & Interpretation

## Experimental Setup

We evaluate multiple prompting strategies on classification-style tasks that
require **exactly one-word outputs**. This constraint allows us to explicitly
study the interaction between semantic correctness and instruction-following.

### Prompting Strategies
- **Baseline**: a direct instruction without examples or reasoning.
- **Few-shot**: prompts augmented with a small number of input–output examples.
- **Chain-of-Thought (CoT)**: prompts encouraging explicit step-by-step reasoning.

### Prompt Length Variants
- Short
- Medium
- Long

---

## Evaluation Metrics

Correctness is defined using **exact string match** between the model output and
the ground-truth label. This intentionally penalizes both semantic errors and
violations of the one-word output constraint.

In addition to accuracy, we compute **embedding-based vector distances** between
model outputs and ground-truth answers. These distances provide a complementary
view of semantic deviation even when outputs are counted as incorrect due to
format violations.

---

## Results Overview

### Figure 1 — Overall Accuracy by Prompting Method

![Overall accuracy by method](analysis_results/overall_accuracy.png)

**Figure 1.** Overall exact-match accuracy for each prompting strategy across all
tasks. Baseline prompting achieves high accuracy, while few-shot prompting
slightly improves performance. Chain-of-Thought shows reduced accuracy under
strict output constraints.

---

### Figure 2 — Accuracy as a Function of Prompt Length

![Prompt length variation](analysis_results/prompt_variation_plot.png)

**Figure 2.** Accuracy as a function of prompt length for each prompting strategy.
Medium-length prompts consistently outperform both short and long prompts,
suggesting a balance between clarity and over-specification.

---

### Figure 3 — Method Disagreement Heatmap

![Method disagreement heatmap](analysis_results/method_disagreement_heatmap.png)

**Figure 3.** Pairwise disagreement rates between prompting strategies. Higher
values indicate that two methods frequently produce different answers for the
same task, even when their aggregate accuracies may be similar.

---

### Figure 4 — Chain-of-Thought Overthinking Effect

![CoT overthinking](analysis_results/cot_overthinking_plot.png)

**Figure 4.** Comparison of baseline and Chain-of-Thought accuracy across prompt
lengths. CoT frequently underperforms due to verbose outputs that violate the
one-word constraint, particularly for medium and long prompts.

---

### Figure 5 — Few-shot Improvement over Baseline

![Few-shot effect](analysis_results/fewshot_effect_plot.png)

**Figure 5.** Accuracy improvement achieved by few-shot prompting relative to the
baseline across prompt lengths. Few-shot prompting yields substantial gains for
short and medium prompts.

---

## Extended Discussion and Research Questions

### RQ1 — Instruction-following vs semantic competence

The Chain-of-Thought strategy often produces responses that are semantically
related to the correct answer but fail to comply with the strict output format.
This indicates that encouraging explicit reasoning can interfere with
instruction-following when the task requires minimal outputs.

This result highlights a tradeoff between **semantic competence** and
**format adherence**, suggesting that improved reasoning does not always translate
to improved task performance under constrained evaluation.

---

### RQ2 — Prompt length sensitivity is method-dependent

Prompt length affects prompting strategies in distinct ways. While baseline and
few-shot prompting benefit from moderate increases in prompt length, Chain-of-
Thought prompting degrades as prompts become longer. This degradation can be
attributed to instruction overload, where multiple competing directives reduce
the model’s ability to prioritize output constraints.

---

### RQ3 — Few-shot vs Chain-of-Thought under strict constraints

Few-shot prompting consistently outperforms Chain-of-Thought when output format is
strictly constrained. By providing concrete examples, few-shot prompts implicitly
teach both the task semantics and the expected output structure, reducing the
likelihood of verbose or malformed responses.

---

### RQ4 — Over-specification harms constrained tasks

Our results demonstrate that adding more instructions does not necessarily improve
performance. Overly long or detailed prompts increase the probability of violating
output constraints, particularly for tasks requiring short, categorical answers.
This finding supports the notion that **moderate prompt design** is often optimal.

---

## Conclusion

Overall, our experiments show that optimal prompting strategies depend not only on
task complexity but also on output constraints. In strictly constrained settings,
medium-length prompts and example-based prompting outperform reasoning-heavy
approaches such as Chain-of-Thought. These findings emphasize the importance of
aligning prompting strategies with both the task objective and evaluation
criteria.

---

## Reproducibility

All experimental results can be reproduced by running:

```bash
prompt-lab full --provider dummy
```

from the project root directory after installation.
