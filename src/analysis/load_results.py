from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Dict, List

# --- Ensure src/ is on sys.path so `import prompt_lab...` works ---

THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parents[2]  # .../prompt-engineering-project
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from prompt_lab.config.loader import load_config  # type: ignore


def get_results_dir() -> Path:
    """Return the path to the results directory based on config."""
    cfg = load_config()
    return PROJECT_ROOT / cfg.experiment.output_dir


def load_method_predictions(method: str) -> List[dict]:
    """
    Load predictions for a single method from <method>_predictions.csv.

    Returns a list of dicts:
        {
          "task_id": str,
          "prompt_length": str,
          "prompt_text": str,
          "predicted_answer": str,
          "ground_truth": str,
          "is_correct": int (0/1),
        }
    """
    results_dir = get_results_dir()
    path = results_dir / f"{method}_predictions.csv"
    if not path.exists():
        raise FileNotFoundError(f"Predictions file not found for method '{method}': {path}")

    rows: List[dict] = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(
                {
                    "task_id": r["task_id"],
                    "prompt_length": r["prompt_length"],
                    "prompt_text": r["prompt_text"],
                    "predicted_answer": r["predicted_answer"],
                    "ground_truth": r["ground_truth"],
                    "is_correct": int(r["is_correct"]),
                }
            )
    return rows


def load_all_methods() -> Dict[str, List[dict]]:
    """
    Load predictions for all methods defined in config.experiment.methods.

    Returns:
        { method_name: [rows...] }
    """
    cfg = load_config()
    methods = cfg.experiment.methods
    return {m: load_method_predictions(m) for m in methods}


def load_metrics_for_method(method: str) -> Dict[str, float]:
    """
    Load summary metrics for a method from <method>_metrics.csv.

    Expected format:
        total,correct,accuracy
        18,3,0.1666666667
    """
    results_dir = get_results_dir()
    path = results_dir / f"{method}_metrics.csv"
    if not path.exists():
        raise FileNotFoundError(f"Metrics file not found for method '{method}': {path}")

    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        raise ValueError(f"No rows in metrics file: {path}")

    row = rows[0]
    return {
        "total": float(row["total"]),
        "correct": float(row["correct"]),
        "accuracy": float(row["accuracy"]),
    }
