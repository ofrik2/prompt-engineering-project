from prompt_lab.dataset.generator import generate_dummy_tasks, build_prompt_variants
from prompt_lab.methods.baseline import BaselineMethod
from prompt_lab.evaluator.metrics import compute_accuracy


def main() -> None:
    # 1. Prepare data
    tasks = generate_dummy_tasks()
    prompts = build_prompt_variants(tasks)

    # 2. Run baseline method
    baseline = BaselineMethod()
    predictions = baseline.run(prompts)

    # 3. Evaluate
    eval_result = compute_accuracy(tasks, predictions)

    print(f"Total predictions: {eval_result.total}")
    print(f"Correct predictions: {eval_result.correct}")
    print(f"Accuracy: {eval_result.accuracy:.3f}")


if __name__ == "__main__":
    main()
