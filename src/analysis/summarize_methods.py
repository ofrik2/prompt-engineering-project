from __future__ import annotations

import csv
from pathlib import Path
from typing import List, Dict

# Add src/ to path like other scripts
import sys
THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parents[2]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from prompt_lab.config.loader import load_config  # type: ignore
from analysis.load_results import load_metrics_for_method  # type: ignore


def main() -> None:
    cfg = load_config()
    methods: List[str] = cfg.experiment.methods

    # Write to analysis_results/ instead of results/
    output_dir = PROJECT_ROOT / "analysis_results"
    output_dir.mkdir(exist_ok=True)

    summary_rows: List[Dict[str, float]] = []

    print("\n=== Method Summary ===\n")
    print("method     | total | correct | accuracy")
    print("----------------------------------------")

    for method in methods:
        m = load_metrics_for_method(method)

        summary_rows.append(
            {
                "method": method,
                "total": m["total"],
                "correct": m["correct"],
                "accuracy": m["accuracy"],
            }
        )

        print(
            f"{method:10s} | {int(m['total']):5d} | {int(m['correct']):7d} | {m['accuracy']:.3f}"
        )

    # Save combined CSV
    csv_path = output_dir / "method_summary.csv"
    fieldnames = ["method", "total", "correct", "accuracy"]

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary_rows:
            writer.writerow(row)

    print(f"\nSaved method summary CSV → {csv_path}\n")


if __name__ == "__main__":
    main()
