"""
Baseline prompting method.

This version uses an LLMClient (currently DummyLLMClient by default)
to generate answers for each prompt.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from prompt_lab.dataset.generator import PromptVariant
from prompt_lab.utils.llm_client import (
    LLMClient,
    LLMRequest,
    LLMResponse,
    DummyLLMClient,
)


@dataclass
class BaselineResult:
    """
    Result of applying the baseline method to a single prompt.
    """
    task_id: str
    prompt_length: str
    prompt_text: str
    predicted_answer: str
    tokens_input: Optional[int] = None
    tokens_output: Optional[int] = None


class BaselineMethod:
    """
    Baseline prompting method.

    It:
    - receives prompt variants (short/medium/long)
    - sends each prompt to an LLMClient
    - returns the raw text as `predicted_answer`

    For now, we use DummyLLMClient by default, so no real API calls are made.
    Later, we can inject a real LLM client.
    """

    def __init__(
        self,
        model_name: str,
        temperature: float = 0.0,
        max_tokens: int = 256,
        llm_client: Optional[LLMClient] = None,
    ) -> None:
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        # If no client is given, fall back to a DummyLLMClient
        self._llm: LLMClient = llm_client or DummyLLMClient()

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
        Apply the baseline method to a list of prompt variants.

        For each prompt:
        - send it to the LLM client
        - store the response text as predicted_answer
        """
        results: List[BaselineResult] = []

        for p in prompts:
            response = self._call_llm(p.prompt_text)

            results.append(
                BaselineResult(
                    task_id=p.task_id,
                    prompt_length=p.length,
                    prompt_text=p.prompt_text,
                    predicted_answer=response.text,
                    tokens_input=response.tokens_input,
                    tokens_output=response.tokens_output,
                )
            )

        return results
