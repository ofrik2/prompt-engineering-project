from pathlib import Path
import csv

from prompt_lab.dataset.generator import (
    generate_dummy_tasks,
    build_prompt_variants,
    load_tasks_from_json,
)
from prompt_lab.methods.cot import CoTMethod, CoTConfig
from prompt_lab.evaluator.metrics import compute_accuracy
from prompt_lab.config.loader import load_config
from prompt_lab.utils.llm_client import DummyLLMClient, OpenAILLMClient



def main() -> None:
    # Load configuration
    cfg = load_config()

    # Project root (one level above `src`)
    project_root = Path(__file__).resolve().parents[1]

    # Use output_dir from config
    results_dir = project_root / cfg.experiment.output_dir
    results_dir.mkdir(exist_ok=True)

    # 1. Prepare data (choose source based on config)
    if cfg.experiment.dataset == "dummy":
        tasks = generate_dummy_tasks()
    elif cfg.experiment.dataset == "file":
        dataset_path = project_root / cfg.experiment.dataset_path
        tasks = load_tasks_from_json(dataset_path)
    else:
        raise ValueError(f"Unknown dataset type: {cfg.experiment.dataset!r}")

    prompts = build_prompt_variants(tasks)
    truth_by_id = {t.id: t.ground_truth for t in tasks}


    # 2. Choose LLM client based on config
    if cfg.model.provider == "openai":
        llm_client = OpenAILLMClient()
    elif cfg.model.provider == "dummy":
        llm_client = DummyLLMClient()
    else:
        raise ValueError(f"Unknown model provider: {cfg.model.provider!r}")

    # 3. Run CoT method
    cot = CoTMethod(
        model_name=cfg.model.model_name,
        temperature=cfg.model.temperature,
        max_tokens=cfg.model.max_tokens,
        config=CoTConfig(),
        llm_client=llm_client,
    )
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
