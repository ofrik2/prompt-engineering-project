from prompt_lab.dataset.generator import generate_dummy_tasks, build_prompt_variants
from prompt_lab.methods.baseline import BaselineMethod


def main() -> None:
    tasks = generate_dummy_tasks()
    prompts = build_prompt_variants(tasks)

    baseline = BaselineMethod()
    results = baseline.run(prompts)

    for r in results:
        print(f"Task: {r.task_id} | length={r.prompt_length}")
        print(f"Prompt:\n{r.prompt_text}")
        print(f"Predicted answer: {r.predicted_answer}")
        print("-" * 40)


if __name__ == "__main__":
    main()
