from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
import matplotlib.pyplot as plt


def main() -> None:
    """Generate a single summary figure: overall accuracy per method.

    Input:
      analysis_results/method_summary.csv
        columns: method, total, correct, accuracy

    Output:
      analysis_results/overall_accuracy.png
    """
    this_file = Path(__file__).resolve()
    project_root = this_file.parents[2]
    analysis_dir = project_root / "analysis_results"
    csv_path = analysis_dir / "method_summary.csv"
    out_path = analysis_dir / "overall_accuracy.png"

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Expected {csv_path} to exist. Run summarize_methods.py first (or run the full pipeline)."
        )

    df = pd.read_csv(csv_path)
    required = {"method", "accuracy"}
    if not required.issubset(df.columns):
        raise ValueError(
            f"method_summary.csv missing required columns. Found: {list(df.columns)}"
        )

    # Sort for stable plotting (highest accuracy first)
    df = df.sort_values("accuracy", ascending=False)

    plt.figure()
    plt.bar(df["method"], df["accuracy"])
    plt.title("Overall Exact-Match Accuracy by Prompting Method")
    plt.ylabel("Accuracy")
    plt.ylim(0, 1)

    # Add numeric labels above bars
    for i, (m, acc) in enumerate(zip(df["method"], df["accuracy"])):
        plt.text(i, float(acc) + 0.01, f"{float(acc):.3f}", ha="center", va="bottom")

    plt.tight_layout()
    analysis_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=200)
    plt.close()

    print(f"Saved overall accuracy plot → {out_path}")


if __name__ == "__main__":
    main()
