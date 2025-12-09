from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt

from analysis.load_results import load_all_methods  # uses PROJECT_ROOT from there

# Recompute PROJECT_ROOT here as well, just like in analyze_prompt_variation
THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parents[2]


def main() -> None:
    output_dir = PROJECT_ROOT / "analysis_results"
    output_dir.mkdir(exist_ok=True)

    data: Dict[str, List[dict]] = load_all_methods()
    methods: List[str] = sorted(data.keys())

    print("\n=== Per-task, Per-prompt Method Comparison ===\n")

    # (task_id, prompt_length) -> { method: is_correct }
    table: Dict[Tuple[str, str], Dict[str, int]] = defaultdict(dict)

    for method, rows in data.items():
        for r in rows:
            key = (r["task_id"], r["prompt_length"])
            table[key][method] = r["is_correct"]

    # -------- Build detailed summary CSV --------

    summary_rows: List[dict] = []

    for (task_id, plen), method_map in sorted(table.items(), key=lambda x: (x[0][0], x[0][1])):
        # Ensure all methods have an entry (fill with 0 if missing)
        method_scores = {m: int(method_map.get(m, 0)) for m in methods}
        scores = list(method_scores.values())
        num_correct = sum(scores)

        if num_correct == len(methods):
            agreement_type = "all_correct"
        elif num_correct == 0:
            agreement_type = "all_wrong"
        elif num_correct == 1:
            agreement_type = "single_winner"
        else:
            agreement_type = "mixed_multi"

        winners = [m for m, c in method_scores.items() if c == 1]
        winners_str = "|".join(winners) if winners else ""

        row = {
            "task_id": task_id,
            "prompt_length": plen,
            **method_scores,
            "num_correct": num_correct,
            "winners": winners_str,
            "agreement_type": agreement_type,
        }
        summary_rows.append(row)

    # Write CSV
    summary_path = output_dir / "method_comparison_summary.csv"
    fieldnames = ["task_id", "prompt_length"] + methods + [
        "num_correct",
        "winners",
        "agreement_type",
    ]
    with summary_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary_rows:
            writer.writerow(row)

    print(f"Saved detailed method comparison CSV → {summary_path}")

    # -------- Build pairwise disagreement matrix --------

    # Counters for mismatches / total comparisons per pair
    mismatch_counts: Dict[Tuple[str, str], int] = defaultdict(int)
    pair_totals: Dict[Tuple[str, str], int] = defaultdict(int)

    for _, method_scores in table.items():
        for i, m1 in enumerate(methods):
            for j, m2 in enumerate(methods):
                if j <= i:
                    continue  # only upper triangle (i < j)
                s1 = int(method_scores.get(m1, 0))
                s2 = int(method_scores.get(m2, 0))
                pair = (m1, m2)
                pair_totals[pair] += 1
                if s1 != s2:
                    mismatch_counts[pair] += 1

    # Build matrix of disagreement rates
    n = len(methods)
    matrix = [[0.0 for _ in range(n)] for _ in range(n)]

    for i, m1 in enumerate(methods):
        for j, m2 in enumerate(methods):
            if i == j:
                matrix[i][j] = 0.0
            elif j > i:
                pair = (m1, m2)
                total = pair_totals.get(pair, 0)
                mismatches = mismatch_counts.get(pair, 0)
                matrix[i][j] = mismatches / total if total > 0 else 0.0
            else:
                # symmetric
                matrix[i][j] = matrix[j][i]

    # Save disagreement matrix CSV
    matrix_csv_path = output_dir / "method_disagreement_matrix.csv"
    with matrix_csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + methods)
        for i, m1 in enumerate(methods):
            row = [m1] + [f"{matrix[i][j]:.3f}" for j in range(n)]
            writer.writerow(row)

    print(f"Saved pairwise disagreement matrix CSV → {matrix_csv_path}")

    # -------- Plot heatmap --------

    plt.figure(figsize=(6, 5))
    plt.imshow(matrix, interpolation="nearest")
    plt.xticks(range(n), methods, rotation=45, ha="right")
    plt.yticks(range(n), methods)
    plt.title("Pairwise Disagreement Rate Between Methods")
    plt.colorbar(label="Disagreement rate (0–1)")

    for i in range(n):
        for j in range(n):
            plt.text(
                j,
                i,
                f"{matrix[i][j]:.2f}",
                ha="center",
                va="center",
                fontsize=8,
            )

    plt.tight_layout()

    heatmap_path = output_dir / "method_disagreement_heatmap.png"
    plt.savefig(heatmap_path, dpi=150)
    plt.close()

    print(f"Saved disagreement heatmap → {heatmap_path}\n")


if __name__ == "__main__":
    main()
