"""
Run a simple baseline experiment end-to-end:

- generate a small dummy dataset
- build short/medium/long prompt variants
- run the BaselineMethod on all prompts
- compute accuracy
- save detailed predictions and metrics to the `results/` folder

This is a first concrete "experiment script" that we can later extend
or replace by a more generic experiment runner.
"""

from pathlib import Path
import csv

from prompt_lab.dataset.generator import generate_dummy_tasks, build_prompt_variants
from prompt_lab.methods.baseline import BaselineMethod
from prompt_lab.evaluator.metrics import compute_accuracy


def main() -> None:
    # Figure out project root (one level above `src`)
    project_root = Path(__file__).resolve().parents[1]
    results_dir = project_root / "results"
    results_dir.mkdir(exist_ok=True)

    # 1. Prepare data
    tasks = generate_dummy_tasks()
    prompts = build_prompt_variants(tasks)

    # Build a simple lookup: task_id -> ground_truth
    truth_by_id = {t.id: t.ground_truth for t in tasks}

    # 2. Run baseline method
    baseline = BaselineMethod()
    predictions = baseline.run(prompts)

    # 3. Evaluate
    eval_result = compute_accuracy(tasks, predictions)

    # 4. Save detailed predictions to CSV
    predictions_path = results_dir / "baseline_predictions.csv"
    with predictions_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "task_id",
                "prompt_length",
                "prompt_text",
                "predicted_answer",
                "ground_truth",
                "is_correct",
            ]
        )
        for p in predictions:
            gt = truth_by_id.get(p.task_id, "")
            is_correct = (p.predicted_answer == gt)
            writer.writerow(
                [
                    p.task_id,
                    p.prompt_length,
                    p.prompt_text,
                    p.predicted_answer,
                    gt,
                    int(is_correct),
                ]
            )

    # 5. Save metrics to CSV
    metrics_path = results_dir / "baseline_metrics.csv"
    with metrics_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["total", "correct", "accuracy"])
        writer.writerow([eval_result.total, eval_result.correct, eval_result.accuracy])

    # 6. Print a short summary to the console
    print("Baseline experiment finished.")
    print(f"Total predictions:  {eval_result.total}")
    print(f"Correct predictions:{eval_result.correct}")
    print(f"Accuracy:           {eval_result.accuracy:.3f}")
    print(f"Predictions saved to: {predictions_path}")
    print(f"Metrics saved to:     {metrics_path}")


if __name__ == "__main__":
    main()
