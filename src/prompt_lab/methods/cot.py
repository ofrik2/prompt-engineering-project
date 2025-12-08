"""
Chain-of-Thought (CoT) style prompting method.

This version uses an LLMClient (DummyLLMClient by default) to generate answers.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from prompt_lab.dataset.generator import PromptVariant
from prompt_lab.methods.baseline import BaselineResult
from prompt_lab.utils.llm_client import (
    LLMClient,
    LLMRequest,
    LLMResponse,
    DummyLLMClient,
)


@dataclass
class CoTConfig:
    """Configuration for the Chain-of-Thought method."""
    add_prefix: bool = True
    add_suffix: bool = True


class CoTMethod:
    """
    Simple Chain-of-Thought prompting method.

    It wraps the original prompt with CoT-style instructions
    and sends it to an LLM client.
    """

    def __init__(
        self,
        model_name: str,
        temperature: float = 0.0,
        max_tokens: int = 256,
        config: Optional[CoTConfig] = None,
        llm_client: Optional[LLMClient] = None,
    ) -> None:
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.config = config or CoTConfig()
        self._llm: LLMClient = llm_client or DummyLLMClient()

    def _wrap_prompt_text(self, original: str) -> str:
        """Add CoT-style instructions around the prompt text."""
        parts: list[str] = []

        if self.config.add_prefix:
            parts.append("You are an AI assistant. Let's think step by step.")

        parts.append(original)

        if self.config.add_suffix:
            parts.append(
                "Think carefully through the problem, then provide a concise final answer."
            )

        return "\n\n".join(parts)

    def _call_llm(self, prompt_text: str) -> LLMResponse:
        """Helper to send a single prompt to the LLM client."""
        req = LLMRequest(
            model_name=self.model_name,
            prompt=prompt_text,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return self._llm.complete(req)

    def run(self, prompts: List[PromptVariant]) -> List[BaselineResult]:
        """
        Apply the CoT method to a list of prompt variants.

        We reuse BaselineResult so we can evaluate CoT outputs
        with the same metrics function as the baseline.
        """
        results: List[BaselineResult] = []

        for p in prompts:
            cot_prompt_text = self._wrap_prompt_text(p.prompt_text)
            response = self._call_llm(cot_prompt_text)

            results.append(
                BaselineResult(
                    task_id=p.task_id,
                    prompt_length=p.length,
                    prompt_text=cot_prompt_text,
                    predicted_answer=response.text,
                    tokens_input=response.tokens_input,
                    tokens_output=response.tokens_output,
                )
            )

        return results
