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


PADDING_SENTENCE = (
    "This sentence is additional neutral context for an academic experiment "
    "and does not affect the correct answer."
)


def pad_prompt_to_target_tokens(prompt: str, target_tokens: int) -> str:
    """
    Approximate token count using whitespace-split and pad with a neutral sentence
    BEFORE the final 'Answer:' marker (if present), so that we reach roughly
    target_tokens tokens without changing the answer format.
    """
    words = prompt.split()
    current = len(words)

    if current >= target_tokens:
        return prompt  # already long enough

    pad_words = PADDING_SENTENCE.split()
    extra_blocks: list[str] = []

    # Add as many padding sentences as needed
    while current + len(pad_words) <= target_tokens:
        extra_blocks.append(PADDING_SENTENCE)
        current += len(pad_words)

    padding_text = "\n".join(extra_blocks)

    marker = "Answer:"
    if marker in prompt:
        # Insert padding *before* "Answer:" so the label is still the last thing
        before, after = prompt.split(marker, 1)
        return before.rstrip() + "\n\n" + padding_text + "\n\n" + marker + after.lstrip()
    else:
        # Fallback: append padding at the end
        return prompt.rstrip() + "\n\n" + padding_text



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
    For each task, create short/medium/long prompt variants.

    Short  ≈ 50 tokens   (under-specified)
    Medium ≈ 200 tokens  (clear instructions)
    Long   ≈ 500 tokens  (very explicit + extra neutral context)

    Token counts are approximate, based on whitespace splitting.
    """
    variants: List[PromptVariant] = []

    for task in tasks:
        if task.task_type == "sentiment":
            medium_block = (
                "Classify the sentiment of the sentence as either \"positive\" or \"negative\".\n"
                "Answer with exactly one word.\n"
            )
            long_block = (
                "Classify the sentiment of the sentence.\n"
                "You MUST answer with EXACTLY ONE WORD: \"positive\" or \"negative\".\n"
                "Do NOT add any other words, punctuation, or explanation.\n"
                "Only output the one-word label.\n"
            )

            short_prompt_base = (
                f"Is the sentiment of this sentence positive or negative?\n"
                f"{task.input_text}\n"
                "Answer with one word.\n"
                "Answer:"
            )

            medium_prompt_base = (
                f"{medium_block}\n"
                f"Sentence: {task.input_text}\n"
                "Answer:"
            )

            long_prompt_base = (
                "You are helping with sentiment analysis in an academic experiment.\n\n"
                f"Sentence: {task.input_text}\n\n"
                f"{long_block}"
                "Answer:"
            )

        elif task.task_type == "math":
            medium_block = (
                "Solve the problem and provide ONLY the final numeric answer.\n"
                "Do not explain your calculation.\n"
            )
            long_block = (
                "Solve the problem step by step in your head.\n"
                "Then provide ONLY the final numeric answer.\n"
                "Do NOT add units, punctuation, or explanation.\n"
                "Only output the number.\n"
            )

            short_prompt_base = (
                f"{task.input_text}\n"
                "What is the answer?\n"
                "Answer:"
            )

            medium_prompt_base = (
                f"{medium_block}\n"
                f"Problem: {task.input_text}\n"
                "Answer:"
            )

            long_prompt_base = (
                "You are an AI assistant solving small arithmetic problems.\n\n"
                f"Problem: {task.input_text}\n\n"
                f"{long_block}"
                "Answer:"
            )

        elif task.task_type == "logic":
            medium_block = (
                "Answer the question with exactly one word: \"yes\" or \"no\".\n"
                "Do not explain your reasoning.\n"
            )
            long_block = (
                "You must answer the following question.\n"
                "You MUST respond with EXACTLY ONE WORD: \"yes\" or \"no\".\n"
                "Do NOT add any other words or explanation.\n"
                "Only output the one-word label.\n"
            )

            short_prompt_base = (
                f"{task.input_text}\n"
                "Answer yes or no.\n"
                "Answer:"
            )

            medium_prompt_base = (
                f"{medium_block}\n"
                f"Question: {task.input_text}\n"
                "Answer:"
            )

            long_prompt_base = (
                "You are helping evaluate logical understanding.\n\n"
                f"Question: {task.input_text}\n\n"
                f"{long_block}"
                "Answer:"
            )

        else:
            raise ValueError(f"Unknown task type: {task.task_type}")

        # Pad to approximate token budgets: 50 / 200 / 500
        short_prompt = pad_prompt_to_target_tokens(short_prompt_base, target_tokens=50)
        medium_prompt = pad_prompt_to_target_tokens(medium_prompt_base, target_tokens=200)
        long_prompt = pad_prompt_to_target_tokens(long_prompt_base, target_tokens=500)

        variants.append(
            PromptVariant(
                task_id=task.id,
                length="short",
                prompt_text=short_prompt,
            )
        )
        variants.append(
            PromptVariant(
                task_id=task.id,
                length="medium",
                prompt_text=medium_prompt,
            )
        )
        variants.append(
            PromptVariant(
                task_id=task.id,
                length="long",
                prompt_text=long_prompt,
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
