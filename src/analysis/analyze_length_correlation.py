from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean
from typing import Dict, List

import matplotlib.pyplot as plt

from analysis.load_results import load_all_methods  # uses PROJECT_ROOT inside


# Recompute PROJECT_ROOT here (same pattern as other scripts)
THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parents[2]


def main() -> None:
    output_dir = PROJECT_ROOT / "analysis_results"
    output_dir.mkdir(exist_ok=True)

    data: Dict[str, List[dict]] = load_all_methods()

    print("\n=== Output Length vs Correctness Analysis ===\n")

    summary_rows: List[Dict[str, float]] = []

    methods = sorted(data.keys())

    for method in methods:
        rows = data[method]

        lengths_correct: List[int] = []
        lengths_incorrect: List[int] = []

        for r in rows:
            # Approximate "length" as word count of predicted answer
            out_len = len(r["predicted_answer"].split())

            if r["is_correct"] == 1:
                lengths_correct.append(out_len)
            else:
                lengths_incorrect.append(out_len)

        if not lengths_correct or not lengths_incorrect:
            print(f"Method {method}: insufficient data (correct or incorrect set is empty).")
            continue

        avg_corr = mean(lengths_correct)
        avg_incorr = mean(lengths_incorrect)
        diff = avg_corr - avg_incorr

        print(f"Method: {method}")
        print(f"  avg length (correct)   = {avg_corr:.1f} words")
        print(f"  avg length (incorrect) = {avg_incorr:.1f} words")
        print(f"  difference (correct - incorrect) = {diff:+.1f}\n")

        summary_rows.append(
            {
                "method": method,
                "avg_len_correct": avg_corr,
                "avg_len_incorrect": avg_incorr,
                "diff_correct_minus_incorrect": diff,
                "n_correct": len(lengths_correct),
                "n_incorrect": len(lengths_incorrect),
            }
        )

    # ----- Save summary CSV -----
    csv_path = output_dir / "length_correlation_summary.csv"
    fieldnames = [
        "method",
        "avg_len_correct",
        "avg_len_incorrect",
        "diff_correct_minus_incorrect",
        "n_correct",
        "n_incorrect",
    ]

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary_rows:
            writer.writerow(row)

    print(f"Saved length correlation summary CSV → {csv_path}")

    # ----- Plot bar chart: avg length correct vs incorrect per method -----
    if summary_rows:
        methods_order = [row["method"] for row in summary_rows]
        correct_vals = [row["avg_len_correct"] for row in summary_rows]
        incorrect_vals = [row["avg_len_incorrect"] for row in summary_rows]

        x = range(len(methods_order))
        width = 0.35

        plt.figure(figsize=(8, 5))
        plt.bar([i - width / 2 for i in x], correct_vals, width=width, label="correct")
        plt.bar([i + width / 2 for i in x], incorrect_vals, width=width, label="incorrect")

        plt.title("Average Answer Length by Correctness and Method")
        plt.xlabel("Method")
        plt.ylabel("Average Answer Length (words)")
        plt.xticks(list(x), methods_order)
        plt.legend()
        plt.grid(axis="y")

        plot_path = output_dir / "length_correlation_plot.png"
        plt.savefig(plot_path, dpi=150, bbox_inches="tight")
        plt.close()

        print(f"Saved length correlation plot → {plot_path}\n")
    else:
        print("No methods with sufficient data to plot.\n")


if __name__ == "__main__":
    main()
