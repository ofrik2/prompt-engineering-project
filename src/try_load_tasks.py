from pathlib import Path

from prompt_lab.dataset.generator import load_tasks_from_json


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data" / "tasks_v1.json"

    tasks = load_tasks_from_json(data_path)

    print(f"Loaded {len(tasks)} tasks from {data_path}")
    for t in tasks:
        print(f"- {t.id} | {t.task_type} | {t.input_text} -> {t.ground_truth}")


if __name__ == "__main__":
    main()
