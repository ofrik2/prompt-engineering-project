"""
Dataset generation utilities for the Prompt Lab project.

For now this only defines the basic data structures and a very simple
placeholder dataset generator. We will expand this step by step.
"""

from dataclasses import dataclass
from typing import List, Literal


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
    For each task, create simple short/medium/long prompt variants.
    Right now this is very naive; we will improve it later.
    """
    variants: List[PromptVariant] = []

    for task in tasks:
        # Short: very minimal
        variants.append(
            PromptVariant(
                task_id=task.id,
                length="short",
                prompt_text=task.input_text,
            )
        )

        # Medium: add a simple instruction
        variants.append(
            PromptVariant(
                task_id=task.id,
                length="medium",
                prompt_text=f"Please answer the following question briefly:\n{task.input_text}",
            )
        )

        # Long: add more explanation/context (still simple for now)
        variants.append(
            PromptVariant(
                task_id=task.id,
                length="long",
                prompt_text=(
                    "You are an AI assistant participating in an academic experiment "
                    "on prompt engineering. Read the task carefully and provide a clear, "
                    "correct, and concise answer.\n\n"
                    f"Task: {task.input_text}\n\n"
                    "Answer:"
                ),
            )
        )

    return variants
