from pathlib import Path
import csv

from prompt_lab.dataset.generator import generate_dummy_tasks, build_prompt_variants
from prompt_lab.methods.cot import CoTMethod, CoTConfig
from prompt_lab.evaluator.metrics import compute_accuracy
from prompt_lab.config.loader import load_config


def main() -> None:
    # Load configuration
    cfg = load_config()

    # Project root (one level above `src`)
    project_root = Path(__file__).resolve().parents[1]

    # Use output_dir from config
    results_dir = project_root / cfg.experiment.output_dir
    results_dir.mkdir(exist_ok=True)

    # 1. Prepare data
    tasks = generate_dummy_tasks()
    prompts = build_prompt_variants(tasks)
    truth_by_id = {t.id: t.ground_truth for t in tasks}

    # 2. Run CoT method using model settings from config
    cot = CoTMethod(
        model_name=cfg.model.model_name,
        temperature=cfg.model.temperature,
        max_tokens=cfg.model.max_tokens,
        config=CoTConfig(),
    )
    predictions = cot.run(prompts)

    predictions = cot.run(prompts)

    # 3. Evaluate
    eval_result = compute_accuracy(tasks, predictions)

    # 4. Save predictions
    predictions_path = results_dir / "cot_predictions.csv"
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

    # 5. Save metrics
    metrics_path = results_dir / "cot_metrics.csv"
    with metrics_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["total", "correct", "accuracy"])
        writer.writerow([eval_result.total, eval_result.correct, eval_result.accuracy])

    # 6. Print summary
    print("CoT experiment finished.")
    print(f"Total predictions:  {eval_result.total}")
    print(f"Correct predictions:{eval_result.correct}")
    print(f"Accuracy:           {eval_result.accuracy:.3f}")
    print(f"Predictions saved to: {predictions_path}")
    print(f"Metrics saved to:     {metrics_path}")


if __name__ == "__main__":
    main()
