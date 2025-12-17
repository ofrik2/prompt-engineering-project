"""
Evaluation metrics for prompt-engineering experiments.

Right now we implement a very simple accuracy computation.
Later we can add:
- per-task-type accuracy
- confusion matrices for sentiment
- distance metrics, entropy, etc.
"""

from dataclasses import dataclass
from typing import List, Dict
import re

from prompt_lab.dataset.generator import Task
from prompt_lab.methods.baseline import BaselineResult


@dataclass
class EvaluationResult:
    """Aggregated metrics over a set of predictions."""
    total: int
    correct: int
    accuracy: float


def _normalize_label(s: str) -> str:
    """
    Normalize a 1-word label-style answer:
    - strip whitespace
    - lowercase
    - remove trailing punctuation/symbols (e.g., 'positive.' -> 'positive')
    """
    s = (s or "").strip().lower()
    # Remove one or more trailing non-word / non-dash chars
    # Examples: "positive." -> "positive", "true!!!" -> "true", "5," -> "5"
    s = re.sub(r"[^\w\-]+$", "", s)
    return s


def compute_accuracy(tasks: List[Task], predictions: List[BaselineResult]) -> EvaluationResult:
    """
    Compute accuracy = (# correct) / (# total).

    Matching is done by:
    - task_id
    - normalized string equality between predicted_answer and ground_truth
      (so harmless trailing punctuation doesn't make a correct answer wrong)
    """
    truth_by_id: Dict[str, str] = {t.id: t.ground_truth for t in tasks}

    total = 0
    correct = 0

    for p in predictions:
        total += 1
        gt = truth_by_id.get(p.task_id)

        if gt is None:
            # Unknown task_id – we just skip correctness, but still count in total
            continue

        pred_norm = _normalize_label(p.predicted_answer)
        gt_norm = _normalize_label(gt)

        if pred_norm == gt_norm:
            correct += 1

    accuracy = correct / total if total > 0 else 0.0
    return EvaluationResult(total=total, correct=correct, accuracy=accuracy)
