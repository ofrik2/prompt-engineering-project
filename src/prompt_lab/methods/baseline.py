"""
Baseline prompting method.

For now this method does NOT call a real LLM.
It just shows how the structure will look like.
We will later replace the dummy parts with real API calls.
"""

from dataclasses import dataclass
from typing import List

from prompt_lab.dataset.generator import Task, PromptVariant


@dataclass
class BaselineResult:
    """
    Result of applying the baseline method to a single prompt.
    For now, this is very simple; we will expand it later.
    """
    task_id: str
    prompt_length: str
    prompt_text: str
    predicted_answer: str


class BaselineMethod:
    """
    Very simple baseline: just uses the prompt as-is.

    Later this class will be changed to:
    - call an LLM with the prompt_text
    - parse the response
    - return the answer + maybe reasoning
    """

    def run(self, prompts: List[PromptVariant]) -> List[BaselineResult]:
        """
        Apply the baseline method to a list of prompt variants.

        Right now:
        - We do NOT talk to an LLM.
        - We just return a dummy 'predicted_answer' so that
          we can test the rest of the pipeline structure.
        """
        results: List[BaselineResult] = []

        for p in prompts:
            # Very naive "smart" baseline:
            # We only know the task_id here, so we cheat a bit:
            # - if it's the math task, answer "12"
            # - if it's the sentiment task, answer "positive"
            # - otherwise, still use a dummy answer

            if p.task_id == "math_1":
                dummy_answer = "12"
            elif p.task_id == "sentiment_1":
                dummy_answer = "positive"
            else:
                dummy_answer = "DUMMY_ANSWER"

            results.append(
                BaselineResult(
                    task_id=p.task_id,
                    prompt_length=p.length,
                    prompt_text=p.prompt_text,
                    predicted_answer=dummy_answer,
                )
            )

        return results
