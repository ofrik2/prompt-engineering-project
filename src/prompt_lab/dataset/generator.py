"""
Dataset generation utilities for the Prompt Lab project.

For now this only defines the basic data structures and a very simple
placeholder dataset generator. We will expand this step by step.
"""

from dataclasses import dataclass
from typing import List, Literal
from pathlib import Path
import json



TaskType = Literal["sentiment", "math", "logic"]
PromptLength = Literal["short", "medium", "long"]


@dataclass
class Task:
    """A single logical task/question with a ground-truth answer."""
    id: str
    task_type: TaskType
    input_text: str
    ground_truth: str


@dataclass
class PromptVariant:
    """A specific textual prompt for a given task (short/medium/long)."""
    task_id: str
    length: PromptLength
    prompt_text: str


def generate_dummy_tasks() -> List[Task]:
    """
    Return a very small hard-coded list of tasks.
    This is just to have something concrete to work with.
    We will replace/extend this later.
    """
    return [
        Task(
            id="sentiment_1",
            task_type="sentiment",
            input_text="I loved the movie, it was fantastic!",
            ground_truth="positive",
        ),
        Task(
            id="math_1",
            task_type="math",
            input_text="What is 7 + 5?",
            ground_truth="12",
        ),
        Task(
            id="logic_1",
            task_type="logic",
            input_text="If all A are B, and all B are C, are all A also C?",
            ground_truth="yes",
        ),
    ]


def build_prompt_variants(tasks: List[Task]) -> List[PromptVariant]:
    """
    For each task, create short/medium/long prompt variants WITH STRICT
    ANSWER-FORMAT ENFORCEMENT so that evaluation is reliable.
    """

    variants: List[PromptVariant] = []

    for task in tasks:
        # === Build the task-type–specific answer constraint block ===
        if task.task_type == "sentiment":
            format_block = (
                "Answer with EXACTLY ONE WORD: \"positive\" or \"negative\".\n"
                "Do NOT explain your answer.\n"
                "Only output the one-word label.\n"
            )
        elif task.task_type == "math":
            format_block = (
                "Provide ONLY the final numeric answer.\n"
                "Do NOT explain your calculation.\n"
                "Only output the number.\n"
            )
        elif task.task_type == "logic":
            format_block = (
                "Answer with EXACTLY ONE WORD: \"yes\" or \"no\".\n"
                "Do NOT explain your reasoning.\n"
                "Only output the one-word label.\n"
            )
        else:
            raise ValueError(f"Unknown task type: {task.task_type}")

        # === Short variant ===
        variants.append(
            PromptVariant(
                task_id=task.id,
                length="short",
                prompt_text=(
                    f"{task.input_text}\n\n"
                    f"{format_block}"
                    "Answer:"
                ),
            )
        )

        # === Medium variant ===
        variants.append(
            PromptVariant(
                task_id=task.id,
                length="medium",
                prompt_text=(
                    f"Please answer the following task.\n\n"
                    f"Task: {task.input_text}\n\n"
                    f"{format_block}"
                    "Answer:"
                ),
            )
        )

        # === Long variant ===
        variants.append(
            PromptVariant(
                task_id=task.id,
                length="long",
                prompt_text=(
                    "You are an AI assistant participating in an academic experiment on "
                    "prompt engineering. Follow ALL instructions carefully.\n\n"
                    f"Task: {task.input_text}\n\n"
                    f"{format_block}"
                    "Answer:"
                ),
            )
        )

    return variants


def load_tasks_from_json(path: str | Path) -> List[Task]:
    """
    Load tasks from a JSON file with a list of objects like:
    {
      "id": "...",
      "task_type": "...",
      "input_text": "...",
      "ground_truth": "..."
    }
    """
    p = Path(path)

    if not p.exists():
        raise FileNotFoundError(f"Task file not found: {p}")

    with p.open("r", encoding="utf-8") as f:
        raw_list = json.load(f)

    tasks: List[Task] = []

    for item in raw_list:
        tasks.append(
            Task(
                id=str(item["id"]),
                task_type=item["task_type"],      # Literal enforces allowed values at type level
                input_text=str(item["input_text"]),
                ground_truth=str(item["ground_truth"]),
            )
        )

    return tasks
