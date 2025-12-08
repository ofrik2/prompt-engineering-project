"""
Compare baseline and CoT experiment metrics.

Reads:
- results/baseline_metrics.csv
- results/cot_metrics.csv

and prints a small comparison table.
"""

from pathlib import Path
import csv


def load_metrics(path: Path) -> dict[str, float]:
    """
    Load a metrics CSV with header: total,correct,accuracy
    and return a dict.
    """
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        row = next(reader)
        return {
            "total": float(row["total"]),
            "correct": float(row["correct"]),
            "accuracy": float(row["accuracy"]),
        }


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    results_dir = project_root / "results"

    baseline_path = results_dir / "baseline_metrics.csv"
    cot_path = results_dir / "cot_metrics.csv"

    if not baseline_path.exists() or not cot_path.exists():
        print("Missing metrics files. Run baseline and CoT experiments first.")
        print(f"Expected:\n  {baseline_path}\n  {cot_path}")
        return

    baseline = load_metrics(baseline_path)
    cot = load_metrics(cot_path)

    print("Method    | Total | Correct | Accuracy")
    print("--------------------------------------")
    print(
        f"Baseline  | {int(baseline['total']):5d} | "
        f"{int(baseline['correct']):7d} | {baseline['accuracy']:.3f}"
    )
    print(
        f"CoT       | {int(cot['total']):5d} | "
        f"{int(cot['correct']):7d} | {cot['accuracy']:.3f}"
    )


if __name__ == "__main__":
    main()
