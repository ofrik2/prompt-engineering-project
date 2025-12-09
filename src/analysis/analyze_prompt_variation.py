from __future__ import annotations

import csv
import sys
from pathlib import Path
from statistics import stdev
from typing import Dict, List

import matplotlib.pyplot as plt

# --- Ensure imports ---
THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parents[2]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from analysis.load_results import load_all_methods  # type: ignore


def main():
    output_dir = PROJECT_ROOT / "analysis_results"
    output_dir.mkdir(exist_ok=True)

    data = load_all_methods()

    summary_rows = []
    plot_data = {}

    print("\n=== Prompt Variation Analysis ===\n")

    for method, rows in data.items():
        acc_by_length: Dict[str, float] = {}

        for length in ["short", "medium", "long"]:
            subset = [r for r in rows if r["prompt_length"] == length]
            if subset:
                acc = sum(r["is_correct"] for r in subset) / len(subset)
                acc_by_length[length] = acc

        if not acc_by_length:
            print(f"Method {method}: no data")
            continue

        accuracies = list(acc_by_length.values())
        sensitivity = stdev(accuracies) if len(accuracies) > 1 else 0.0

        # Print summary
        print(f"Method: {method}")
        for length, acc in acc_by_length.items():
            print(f"  {length:6s} → accuracy={acc:.3f}")
        print(f"  Prompt sensitivity (stddev) = {sensitivity:.4f}\n")

        # Save row
        summary_rows.append({
            "method": method,
            **acc_by_length,
            "sensitivity": sensitivity
        })

        plot_data[method] = acc_by_length

    # Save summary CSV
    csv_path = output_dir / "prompt_variation_summary.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["method", "short", "medium", "long", "sensitivity"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary_rows:
            writer.writerow(row)

    print(f"Saved CSV → {csv_path}")

    # Create plot
    plt.figure(figsize=(8, 5))

    for method, acc_map in plot_data.items():
        lengths = ["short", "medium", "long"]
        values = [acc_map.get(l, None) for l in lengths]
        plt.plot(lengths, values, marker="o", label=method)

    plt.title("Accuracy by Prompt Length per Method")
    plt.xlabel("Prompt Length")
    plt.ylabel("Accuracy")
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(True)

    plot_path = output_dir / "prompt_variation_plot.png"
    plt.savefig(plot_path, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Saved plot → {plot_path}\n")


if __name__ == "__main__":
    main()
