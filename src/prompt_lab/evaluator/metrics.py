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

from prompt_lab.dataset.generator import Task
from prompt_lab.methods.baseline import BaselineResult


@dataclass
class EvaluationResult:
    """Aggregated metrics over a set of predictions."""
    total: int
    correct: int
    accuracy: float


def compute_accuracy(tasks: List[Task], predictions: List[BaselineResult]) -> EvaluationResult:
    """
    Compute simple accuracy = (# correct) / (# total).

    Matching is done by:
    - task_id
    - exact string equality between predicted_answer and ground_truth

    For now, this is intentionally simple.
    """
    # Build a lookup dictionary: task_id -> ground_truth
    truth_by_id: Dict[str, str] = {t.id: t.ground_truth for t in tasks}

    total = 0
    correct = 0

    for p in predictions:
        total += 1
        gt = truth_by_id.get(p.task_id)

        if gt is None:
            # Unknown task_id – we just skip correctness, but still count in total
            continue

        if p.predicted_answer == gt:
            correct += 1

    accuracy = correct / total if total > 0 else 0.0
    return EvaluationResult(total=total, correct=correct, accuracy=accuracy)
