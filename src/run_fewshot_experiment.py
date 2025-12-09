from pathlib import Path
import csv

from prompt_lab.dataset.generator import (
    generate_dummy_tasks,
    build_prompt_variants,
    load_tasks_from_json,
)
from prompt_lab.methods.fewshot import FewShotMethod, FewShotConfig
from prompt_lab.methods.baseline import BaselineResult
from prompt_lab.evaluator.metrics import compute_accuracy
from prompt_lab.config.loader import load_config
from prompt_lab.utils.llm_client import DummyLLMClient, OpenAILLMClient


def main():
    cfg = load_config()
    project_root = Path(__file__).resolve().parents[1]

    # dataset
    if cfg.experiment.dataset == "dummy":
        tasks = generate_dummy_tasks()
    elif cfg.experiment.dataset == "file":
        tasks = load_tasks_from_json(project_root / cfg.experiment.dataset_path)
    else:
        raise ValueError("Unknown dataset type")

    prompts = build_prompt_variants(tasks)
    truth_by_id = {t.id: t.ground_truth for t in tasks}

    # choose LLM provider
    if cfg.model.provider == "openai":
        llm_client = OpenAILLMClient()
    else:
        llm_client = DummyLLMClient()

    # Few-shot config
    fs_config = FewShotConfig(examples=cfg.fewshot_examples)

    method = FewShotMethod(
        model_name=cfg.model.model_name,
        temperature=cfg.model.temperature,
        max_tokens=cfg.model.max_tokens,
        config=fs_config,
        llm_client=llm_client,
    )

    predictions = method.run(prompts)
    eval_result = compute_accuracy(tasks, predictions)

    results_dir = project_root / cfg.experiment.output_dir
    results_dir.mkdir(exist_ok=True)

    predictions_path = results_dir / "fewshot_predictions.csv"
    with predictions_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["task_id", "prompt_length", "prompt_text", "predicted_answer", "ground_truth", "is_correct"]
        )
        for p in predictions:
            gt = truth_by_id[p.task_id]
            writer.writerow([
                p.task_id, p.prompt_length, p.prompt_text, p.predicted_answer, gt, int(p.predicted_answer == gt)
            ])

    metrics_path = results_dir / "fewshot_metrics.csv"
    with metrics_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["total", "correct", "accuracy"])
        writer.writerow([eval_result.total, eval_result.correct, eval_result.accuracy])

    print("Few-shot experiment finished.")
    print(f"Accuracy: {eval_result.accuracy:.3f}")


if __name__ == "__main__":
    main()
