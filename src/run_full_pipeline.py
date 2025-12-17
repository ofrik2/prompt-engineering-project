from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run_step(description: str, script_rel_path: str) -> None:
    """Run a Python script (relative to project root) as a subprocess."""
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / script_rel_path

    print(f"\n=== {description} ===")
    print(f"Running: {sys.executable} {script_path}\n")

    try:
        subprocess.run([sys.executable, str(script_path)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Step failed: {description}")
        print(f"Exit code: {e.returncode}")
        # Stop the pipeline on first failure
        sys.exit(e.returncode)


def main() -> None:
    """
    Run the full pipeline:
      1. All experiments (baseline, CoT, few-shot)
      2. All analysis scripts
      3. HTML report generation
    """
    print("\n##############################")
    print("#  LLM Prompting Full Pipeline")
    print("##############################\n")

    # 1) Run all experiments according to config.experiment.methods
    run_step(
        "Step 1: Running all experiments (baseline / CoT / few-shot)",
        "src/run_all_experiments.py",
    )

    # 2) Run analysis scripts
    run_step(
        "Step 2: Summarizing methods",
        "src/analysis/summarize_methods.py",
    )

    run_step(
        "Step 3: Plotting overall accuracy by method",
        "src/analysis/plot_overall_accuracy.py",
    )

    run_step(
        "Step 4: Analyzing prompt variation",
        "src/analysis/analyze_prompt_variation.py",
    )

    run_step(
        "Step 5: Comparing methods per task (and disagreement matrix)",
        "src/analysis/compare_methods_per_task.py",
    )

    run_step(
        "Step 6: Analyzing CoT overthinking",
        "src/analysis/analyze_cot_overthinking.py",
    )

    run_step(
        "Step 7: Analyzing few-shot effect",
        "src/analysis/analyze_fewshot_effect.py",
    )


    # 3) Generate HTML report
    run_step(
        "Step 8: Generating HTML analysis report",
        "src/analysis/generate_html_report.py",
    )

    print("\n✅ Full pipeline finished successfully.")
    print("   - Results CSVs:       results/")
    print("   - Analysis artefacts: analysis_results/")
    print("   - HTML report:        analysis_results/report.html\n")


if __name__ == "__main__":
    main()
