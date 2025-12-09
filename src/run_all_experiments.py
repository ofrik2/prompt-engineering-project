from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from prompt_lab.config.loader import load_config  # type: ignore


def main() -> None:
    """
    Run all experiment scripts for the methods listed in config.experiment.methods.

    For example, if your config has:
        experiment:
          methods: ["baseline", "cot", "fewshot"]

    This script will sequentially run:
        python src/run_baseline_experiment.py
        python src/run_cot_experiment.py
        python src/run_fewshot_experiment.py
    """
    # This file is in src/, so src_dir is its parent
    src_dir = Path(__file__).resolve().parent

    # Load config to know which methods to run
    cfg = load_config()
    methods = list(cfg.experiment.methods)

    # Map method name -> script filename
    script_map = {
        "baseline": "run_baseline_experiment.py",
        "cot": "run_cot_experiment.py",
        "fewshot": "run_fewshot_experiment.py",
    }

    print("\n=== Running all experiments from config.experiment.methods ===")
    print(f"Methods: {methods}\n")

    for method in methods:
        script_name = script_map.get(method)
        if script_name is None:
            print(f"[WARN] No script mapped for method '{method}', skipping.")
            continue

        script_path = src_dir / script_name
        if not script_path.exists():
            print(f"[WARN] Script not found for method '{method}': {script_path}, skipping.")
            continue

        print(f"--- Running {method} experiment: {script_path} ---")
        try:
            subprocess.run([sys.executable, str(script_path)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Experiment for method '{method}' failed with exit code {e.returncode}.")
            # Continue to the next method instead of stopping everything
            continue

    print("\nAll configured experiments finished (or were skipped if missing).\n")


if __name__ == "__main__":
    main()
