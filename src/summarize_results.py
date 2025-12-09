from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List

from prompt_lab.config.loader import load_config


def load_metrics_for_method(results_dir: Path, method: str) -> Dict[str, float]:
    """
    Read <method>_metrics.csv and return a dict with keys:
    total, correct, accuracy.

    Example file format:
        total,correct,accuracy
        18,3,0.1666666667
    """
    metrics_path = results_dir / f"{method}_metrics.csv"
    if not metrics_path.exists():
        raise FileNotFoundError(f"Metrics file not found for method '{method}': {metrics_path}")

    with metrics_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        raise ValueError(f"No rows found in metrics file: {metrics_path}")

    row = rows[0]

    return {
        "total": float(row["total"]),
        "correct": float(row["correct"]),
        "accuracy": float(row["accuracy"]),
    }


def main() -> None:
    cfg = load_config()
    project_root = Path(__file__).resolve().parents[1]
    results_dir = project_root / cfg.experiment.output_dir

    methods: List[str] = cfg.experiment.methods

    summary: List[Dict[str, float]] = []

    print("Method comparison summary:")
    print("--------------------------")

    for method in methods:
        m = load_metrics_for_method(results_dir, method)
        summary.append(
            {
                "method": method,
                **m,
            }
        )
        print(
            f"{method:8s} | total={int(m['total'])} | correct={int(m['correct'])} | "
            f"accuracy={m['accuracy']:.3f}"
        )

    # Write combined CSV
    summary_path = results_dir / "method_summary.csv"
    with summary_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["method", "total", "correct", "accuracy"]
        )
        writer.writeheader()
        for row in summary:
            writer.writerow(row)

    print()
    print(f"Saved combined summary to: {summary_path}")


if __name__ == "__main__":
    main()
