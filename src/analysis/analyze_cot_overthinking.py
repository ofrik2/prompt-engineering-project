from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt

from analysis.load_results import load_method_predictions  # uses PROJECT_ROOT inside


# Recompute PROJECT_ROOT here (same pattern as other scripts)
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

    print("\n=== CoT Overthinking Analysis ===\n")

    # ----- 1. Per-length accuracy baseline vs CoT -----
    baseline_acc = accuracy_by_length("baseline")
    cot_acc = accuracy_by_length("cot")

    per_length_rows: List[Dict[str, float]] = []

    print("Accuracy by prompt length (baseline vs CoT):")
    for length in ["short", "medium", "long"]:
        b = baseline_acc.get(length)
        c = cot_acc.get(length)
        if b is None or c is None:
            continue
        delta = c - b
        print(f"  {length:6s} → baseline={b:.3f}, cot={c:.3f}, cot-baseline={delta:+.3f}")
        per_length_rows.append(
            {
                "type": "per_length",
                "prompt_length": length,
                "baseline_acc": b,
                "cot_acc": c,
                "delta_acc": delta,
            }
        )

    # ----- 2. Task-level flips (improved / worsened / same) -----
    baseline_rows = load_method_predictions("baseline")
    cot_rows = load_method_predictions("cot")

    # Map (task_id, prompt_length) -> is_correct
    base_map: Dict[Tuple[str, str], int] = {
        (r["task_id"], r["prompt_length"]): r["is_correct"] for r in baseline_rows
    }
    cot_map: Dict[Tuple[str, str], int] = {
        (r["task_id"], r["prompt_length"]): r["is_correct"] for r in cot_rows
    }

    improved = 0  # baseline 0, cot 1
    worsened = 0  # baseline 1, cot 0
    same = 0      # baseline == cot

    for key, b_corr in base_map.items():
        if key not in cot_map:
            continue
        c_corr = cot_map[key]
        if b_corr == c_corr:
            same += 1
        elif b_corr == 0 and c_corr == 1:
            improved += 1
        elif b_corr == 1 and c_corr == 0:
            worsened += 1

    total = improved + worsened + same

    if total > 0:
        improved_frac = improved / total
        worsened_frac = worsened / total
        same_frac = same / total

        print("\nPer (task, length) comparison baseline vs CoT:")
        print(f"  improved (0→1): {improved} ({improved_frac:.2%})")
        print(f"  worsened (1→0): {worsened} ({worsened_frac:.2%})")
        print(f"  same:           {same} ({same_frac:.2%})")
    else:
        improved_frac = worsened_frac = same_frac = 0.0
        print("\nNo overlapping (task, length) data between baseline and CoT.")

    # Row for flips summary
    flip_row = {
        "type": "flip_counts",
        "prompt_length": "",
        "baseline_acc": "",
        "cot_acc": "",
        "delta_acc": "",
        "improved": improved,
        "worsened": worsened,
        "same": same,
        "total": total,
        "improved_frac": improved_frac,
        "worsened_frac": worsened_frac,
        "same_frac": same_frac,
    }

    # ----- 3. Save summary CSV -----

    csv_path = output_dir / "cot_overthinking_summary.csv"
    fieldnames = [
        "type",
        "prompt_length",
        "baseline_acc",
        "cot_acc",
        "delta_acc",
        "improved",
        "worsened",
        "same",
        "total",
        "improved_frac",
        "worsened_frac",
        "same_frac",
    ]

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        # per-length rows
        for row in per_length_rows:
            # ensure all keys exist for consistency
            full_row = {k: "" for k in fieldnames}
            full_row.update(row)
            writer.writerow(full_row)
        # flips row
        writer.writerow(flip_row)

    print(f"\nSaved CoT overthinking summary CSV → {csv_path}")

    # ----- 4. Plot: accuracy by length (baseline vs CoT) -----

    lengths = [r["prompt_length"] for r in per_length_rows]
    baseline_vals = [r["baseline_acc"] for r in per_length_rows]
    cot_vals = [r["cot_acc"] for r in per_length_rows]

    if lengths:
        plt.figure(figsize=(8, 5))

        plt.plot(lengths, baseline_vals, marker="o", label="baseline")
        plt.plot(lengths, cot_vals, marker="o", label="cot")

        plt.title("Baseline vs CoT Accuracy by Prompt Length")
        plt.xlabel("Prompt Length")
        plt.ylabel("Accuracy")
        plt.ylim(0, 1)
        plt.grid(True)
        plt.legend()

        plot_path = output_dir / "cot_overthinking_plot.png"
        plt.savefig(plot_path, dpi=150, bbox_inches="tight")
        plt.close()

        print(f"Saved CoT overthinking plot → {plot_path}\n")
    else:
        print("No per-length data available to plot.\n")


if __name__ == "__main__":
    main()
