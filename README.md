# Prompt Engineering Project

## Overview

This project presents an experimental framework for systematically studying how
prompt engineering choices influence the behavior of Large Language Models (LLMs).
Rather than treating prompt engineering as a purely heuristic practice, this work
adopts an **academic–reflective approach** that critically examines when common
prompt engineering techniques help, when they hurt, and why.

The project focuses on the interaction between:
- prompt length,
- prompt content,
- prompting strategy (baseline, few-shot, Chain-of-Thought),
- and **strict output constraints**.

In many real-world systems, models are required to follow precise output formats.
Accordingly, this project treats **instruction-following as a first-class
objective**, not merely a side effect of semantic correctness.

The repository is designed to function both as:
1. a **reproducible experimental research framework**, and
2. a **usable Python package and command-line tool**.

---

# Part I — Package Usage, Design Rationale & Reproducibility

## Design Motivation

Prompt engineering is often presented as a collection of best practices, such as
using longer prompts or encouraging step-by-step reasoning. However, these
recommendations are highly context-dependent. In particular, little attention is
given to scenarios in which models must strictly adhere to output constraints
(e.g., producing exactly one word).

This project was designed to explicitly explore such settings. By enforcing
strict output constraints, we surface failure modes—such as verbosity,
overthinking, and instruction overload—that are often hidden in unconstrained
evaluations.

---

## Project Structure

```
prompt-engineering-project/
├── pyproject.toml
├── src/
│   └── prompt_lab/
│       ├── config/
│       ├── dataset/
│       ├── evaluator/
│       ├── methods/
│       ├── pipeline.py
│       └── cli.py
├── config/
├── data/
├── results/
├── analysis_results/
└── README.md
```

All commands should be executed from the **project root directory**.

---

## Installation

```bash
git clone https://github.com/ofrik2/prompt-engineering-project.git
cd prompt-engineering-project

python -m venv .venv
source .venv/bin/activate

pip install -e .
```

Installing the project in editable mode registers the `prompt-lab` CLI and enables
the framework to be imported as a Python package.

---

## Execution Modes: Dummy vs Azure

### Dummy Provider (Debugging & Validation)

```bash
prompt-lab full --provider dummy
```

The dummy provider returns deterministic placeholder outputs and does not require
any API keys or external services.

This mode was deliberately included to:
- verify installation correctness regardless of virtual environment,
- debug the experimental and analysis pipeline independently of model access,
- ensure reproducibility across machines.

Separating infrastructure validation from model behavior proved essential during
development.

---

### Azure OpenAI Provider (Real Experiments)

```bash
prompt-lab full --provider azure
```

This mode runs real experiments using Azure OpenAI. Users must create a `.env`
file in the project root:

```env
AZURE_OPENAI_ENDPOINT="https://<your-resource>.openai.azure.com/"
AZURE_OPENAI_API_KEY="<your-api-key>"
AZURE_OPENAI_API_VERSION="2024-02-15-preview"
AZURE_OPENAI_DEPLOYMENT="<deployment-name>"
```

Each user supplies their own credentials.

---
# Part II — Experimental Setup & Methodology

## Dataset and Task Design

The experiments are conducted on classification-style tasks with categorical
ground-truth labels. Each task is designed to require **exactly one-word
outputs**, such as `positive`, `negative`, `true`, or `false`.

This strict requirement allows us to study not only semantic correctness, but
also the model’s ability to follow instructions precisely.

The framework supports user-provided datasets in JSON format, enabling
independent experimentation beyond the provided examples.

---

## Prompting Strategies

We evaluate three prompting strategies:

- **Baseline prompting**: concise instructions without examples or explicit
  reasoning encouragement.
- **Few-shot prompting**: prompts augmented with example input–output pairs.
- **Chain-of-Thought (CoT) prompting**: prompts encouraging step-by-step reasoning.

---

## Prompt Manipulations

Importantly, the experiments do **not** only vary prompt length.

Across experiments, we manipulate:
- prompt **length** (short / medium / long),
- prompt **content**, including:
  - instruction explicitness,
  - inclusion of examples,
  - encouragement of reasoning.

This separation allows us to disentangle verbosity effects from structural
prompting effects.

---

## Evaluation Metrics

### Exact-Match Accuracy

Correctness is defined using **exact string match** between the model output and
the ground-truth label. Any deviation—including additional words—is counted as
incorrect.

This choice reflects our emphasis on instruction-following as a primary
objective.

### Semantic Distance (Auxiliary Analysis)

Embedding-based vector distances are computed to analyze semantic proximity
between outputs and ground-truth labels. These distances are used for
interpretation only and do not affect accuracy scores.

---
# Part III — Results, Research Questions, Discussion & Critical Reflection

## Overview of Results

The results presented in this section are derived from systematic comparisons
between prompting strategies, prompt lengths, and prompt content variations.
Rather than reporting results solely in terms of aggregate accuracy, we focus on
**patterns of failure, disagreement, and sensitivity**, which provide deeper
insight into model behavior.

---

## Figure-Based Results

### Figure 1 — Overall Accuracy by Prompting Strategy

![Overall accuracy](analysis_results/overall_accuracy.png)
![overall_accuracy.png](analysis_results/overall_accuracy.png)

*Figure 1.* Overall exact-match accuracy across prompting strategies. Few-shot
prompting slightly improves performance over the baseline. In contrast,
Chain-of-Thought (CoT) prompting exhibits a consistent drop in accuracy when strict
output constraints are enforced.

This result already suggests that prompting strategies commonly believed to
improve reasoning may be misaligned with tasks that require precise instruction
following.

---

### Figure 2 — Effect of Prompt Length

![Prompt length variation](analysis_results/prompt_variation_plot.png)

*Figure 2.* Accuracy as a function of prompt length. Medium-length prompts
consistently outperform both short and long prompts across strategies.

This finding challenges the simplistic assumption that longer prompts always
provide better guidance. Instead, excessive verbosity appears to introduce
instruction overload.

---

### Figure 3 — Method Disagreement Analysis

![Method disagreement](analysis_results/method_disagreement_heatmap.png)

*Figure 3.* Pairwise disagreement rates between prompting strategies. High
disagreement indicates that different prompting strategies often lead the model
to qualitatively different answers for the same task, even when their overall
accuracies appear similar.

This analysis highlights that accuracy alone can obscure substantial behavioral
differences.

---

### Figure 4 — Chain-of-Thought Overthinking

![CoT overthinking](analysis_results/cot_overthinking_plot.png)

*Figure 4.* Comparison of baseline and Chain-of-Thought accuracy across prompt
lengths. CoT frequently produces verbose outputs that violate the one-word output
constraint, particularly for medium and long prompts.

We refer to this failure mode as *overthinking*.

---

### Figure 5 — Few-shot Prompting Effect

![Few-shot effect](analysis_results/fewshot_effect_plot.png)

*Figure 5.* Accuracy improvement achieved by few-shot prompting relative to the
baseline. The improvement is most pronounced for short and medium prompts, where
examples help clarify both task semantics and output format.

---

## Research Questions and Interpretations

The following research questions were formulated during the analysis process.
They go beyond the basic assignment instructions and reflect independent
exploration and critical thinking.

---

### RQ1 — Does improved reasoning harm instruction-following under strict output constraints?

**Observation:**  
Chain-of-Thought prompting often produces responses that are semantically related
to the correct answer but fail to satisfy the one-word output requirement.

**Interpretation:**  
Encouraging explicit reasoning shifts the model’s focus from producing an answer
to producing an explanation. In tasks with strict output constraints, this tradeoff
results in lower exact-match accuracy despite reasonable semantic competence.

**Insight:**  
Improved reasoning does not necessarily translate to improved task performance
when instruction-following is the primary objective.

---

### RQ2 — Is prompt length sensitivity uniform across prompting strategies?

**Observation:**  
Prompt length affects prompting strategies differently. Baseline and few-shot
prompting benefit from moderate increases in prompt length, while Chain-of-Thought
performance degrades as prompts become longer.

**Interpretation:**  
Long prompts introduce competing instructions and increase cognitive load, making
it harder for the model to prioritize output constraints.

**Insight:**  
Optimal prompt length is strategy-dependent; a single “best length” does not exist
across methods.

---

### RQ3 — Few-shot vs Chain-of-Thought: which is more robust under strict constraints?

**Observation:**  
Few-shot prompting consistently outperforms Chain-of-Thought prompting in tasks
requiring one-word outputs.

**Interpretation:**  
Few-shot examples implicitly encode both semantic intent and expected output
structure, whereas Chain-of-Thought explicitly encourages verbosity.

**Insight:**  
When output format matters, structural guidance via examples is more effective
than encouraging reasoning.

---

### RQ4 — Does adding more instructions always improve performance?

**Observation:**  
Long and highly detailed prompts often lead to lower accuracy across strategies.

**Interpretation:**  
Over-specification can dilute critical instructions, causing the model to violate
output constraints.

**Insight:**  
More instruction is not inherently better; concise and well-scoped prompts can be
more effective.

---

### RQ5 — Can disagreement analysis reveal insights beyond accuracy metrics?

**Observation:**  
High disagreement rates are observed even between methods with similar accuracy.

**Interpretation:**  
Different prompting strategies may succeed on different subsets of tasks, leading
to qualitatively distinct failure modes.

**Insight:**  
Disagreement analysis provides a complementary lens for understanding model
behavior that is not captured by aggregate accuracy alone.

---

## Extended Discussion

Taken together, these findings suggest that prompt engineering must be evaluated
in the context of task constraints and evaluation criteria. Strategies that
encourage reasoning and verbosity may be beneficial for open-ended generation but
can be counterproductive for constrained classification tasks.

The consistent advantage of medium-length prompts indicates a balance between
clarity and over-specification. Similarly, the strong performance of few-shot
prompting highlights the importance of implicit structure over explicit reasoning.

---

## Critical Reflection on Methodology

While the methodology effectively isolates prompt design effects, it has several
limitations:

- Exact-match accuracy underestimates semantic competence.
- Results may vary across models or domains.
- The study focuses on constrained tasks and may not generalize to free-form
  generation.

Nevertheless, the chosen methodology is well-suited for analyzing instruction-
following behavior and prompt sensitivity in controlled settings.

---

## Conclusion

This project demonstrates that prompt engineering is highly context-dependent.
More reasoning, more instructions, or longer prompts do not universally improve
performance. Instead, effective prompting requires aligning prompt design with
task constraints and evaluation objectives.

---

## Reproducibility

All results reported in this section can be reproduced by running:

```bash
prompt-lab full --provider dummy
```
