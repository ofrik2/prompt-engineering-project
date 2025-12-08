"""
Chain-of-Thought (CoT) style prompting method.

For now this method:
- takes existing prompt variants
- wraps them with an instruction to "think step by step"
- uses the same dummy answers logic as the baseline

Later we will replace the dummy answers with real LLM calls.
"""

from dataclasses import dataclass
from typing import List

from prompt_lab.dataset.generator import PromptVariant
from prompt_lab.methods.baseline import BaselineResult  # reuse same result type


@dataclass
class CoTConfig:
    """
    Configuration options for the CoT method.

    This is very small for now, but we keep it so later we can add things like:
    - number of reasoning steps
    - whether to ask for explanation + final answer separately
    """
    add_prefix: bool = True
    add_suffix: bool = True


class CoTMethod:
    """
    Simple Chain-of-Thought style method.

    It modifies the prompt text a bit to encourage reasoning,
    but still returns dummy answers (for now).
    """

    def __init__(self, config: CoTConfig | None = None) -> None:
        self.config = config or CoTConfig()

    def _wrap_prompt_text(self, original: str) -> str:
        """Add CoT-style instructions around the original prompt."""
        parts: list[str] = []

        if self.config.add_prefix:
            parts.append(
                "You are an AI assistant. Let's think about this step by step."
            )

        parts.append(original)

        if self.config.add_suffix:
            parts.append(
                "Take a moment to reason carefully, then provide a clear final answer."
            )

        return "\n\n".join(parts)

    def run(self, prompts: List[PromptVariant]) -> List[BaselineResult]:
        """
        Apply the CoT method to a list of prompt variants.

        We reuse BaselineResult so we can evaluate CoT outputs
        with the same metrics function as the baseline.
        """
        results: List[BaselineResult] = []

        for p in prompts:
            # Build the CoT-style prompt
            cot_prompt_text = self._wrap_prompt_text(p.prompt_text)

            # For now we still use the same dummy answer logic as baseline.
            # Later, this will call the LLM and (hopefully) perform better.
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
                    prompt_text=cot_prompt_text,
                    predicted_answer=dummy_answer,
                )
            )

        return results
