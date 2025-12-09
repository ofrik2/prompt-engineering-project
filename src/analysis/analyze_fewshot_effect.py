from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt

from analysis.load_results import load_method_predictions  # uses PROJECT_ROOT inside


# Recompute PROJECT_ROOT here (like other scripts)
THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parents[2]


def accuracy_by_length(method: str) -> Dict[str, float]:
    """Compute accuracy per prompt_length for a given method."""
    rows = load_method_predictions(method)
    acc_by_len: Dict[str, float] = {}

    for length in ["short", "medium", "long"]:
        subset = [r for r in rows if r["prompt_length"] == length]
        if not subset:
            continue
        acc = sum(r["is_correct"] for r in subset) / len(subset)
        acc_by_len[length] = acc

    return acc_by_len


def main() -> None:
    output_dir = PROJECT_ROOT / "analysis_results"
    output_dir.mkdir(exist_ok=True)

    print("\n=== Few-shot Effect Analysis ===\n")

    baseline_acc = accuracy_by_length("baseline")
    fewshot_acc = accuracy_by_length("fewshot")

    summary_rows: List[Dict[str, float]] = []

    print("Accuracy by prompt length (baseline vs fewshot):")
    for length in ["short", "medium", "long"]:
        b = baseline_acc.get(length)
        f = fewshot_acc.get(length)
        if b is None or f is None:
            continue
        delta = f - b
        print(f"  {length:6s} → baseline={b:.3f}, fewshot={f:.3f}, fewshot-baseline={delta:+.3f}")
        summary_rows.append(
            {
                "prompt_length": length,
                "baseline_acc": b,
                "fewshot_acc": f,
                "delta_acc": delta,
            }
        )

    # ----- Save summary CSV -----
    csv_path = output_dir / "fewshot_effect_summary.csv"
    fieldnames = ["prompt_length", "baseline_acc", "fewshot_acc", "delta_acc"]

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary_rows:
            writer.writerow(row)

    print(f"\nSaved few-shot effect summary CSV → {csv_path}")

    # ----- Plot bar chart -----
    if summary_rows:
        lengths = [r["prompt_length"] for r in summary_rows]
        baseline_vals = [r["baseline_acc"] for r in summary_rows]
        fewshot_vals = [r["fewshot_acc"] for r in summary_rows]

        x = range(len(lengths))
        width = 0.35

        plt.figure(figsize=(8, 5))
        plt.bar([i - width / 2 for i in x], baseline_vals, width=width, label="baseline")
        plt.bar([i + width / 2 for i in x], fewshot_vals, width=width, label="fewshot")

        plt.title("Baseline vs Few-shot Accuracy by Prompt Length")
        plt.xlabel("Prompt Length")
        plt.ylabel("Accuracy")
        plt.xticks(list(x), lengths)
        plt.ylim(0, 1)
        plt.legend()
        plt.grid(axis="y")

        plot_path = output_dir / "fewshot_effect_plot.png"
        plt.savefig(plot_path, dpi=150, bbox_inches="tight")
        plt.close()

        print(f"Saved few-shot effect plot → {plot_path}\n")
    else:
        print("No overlapping per-length data for baseline and fewshot to plot.\n")


if __name__ == "__main__":
    main()
