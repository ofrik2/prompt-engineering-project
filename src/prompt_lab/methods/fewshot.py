"""
Few-Shot prompting method for the Prompt Engineering project.

This method prepends a fixed set of example input/output pairs
to the prompt before sending it to the LLM client.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from prompt_lab.dataset.generator import PromptVariant, Task
from prompt_lab.methods.baseline import BaselineResult

# 🔧 FIXED: Import all required LLM-related classes
from prompt_lab.utils.llm_client import (
    DummyLLMClient,
    AzureOpenAILLMClient,
    LLMClient,
    LLMRequest,
    LLMResponse,
)


@dataclass
class FewShotExample:
    """A single example pair fed to the model."""
    input_text: str
    output_text: str


@dataclass
class FewShotConfig:
    """Configuration for Few-Shot prompting."""
    examples: List[FewShotExample]
    add_instruction: bool = True


class FewShotMethod:
    """
    Few-Shot prompting method.

    We prepend several demonstration examples before the user's prompt.
    """

    def __init__(
        self,
        model_name: str,
        temperature: float = 0.0,
        max_tokens: int = 256,
        config: FewShotConfig | None = None,
        llm_client: Optional[LLMClient] = None,
    ) -> None:
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.config = config or FewShotConfig(examples=[])
        self._llm: LLMClient = llm_client or DummyLLMClient()

    def _build_fewshot_prompt(self, original: str) -> str:
        """Build the few-shot formatted prompt as a string."""

        parts: list[str] = []

        if self.config.add_instruction:
            parts.append("Below are examples of correct responses. Follow the patterns.")

        # Add example demonstrations
        for ex in self.config.examples:
            parts.append(
                f"Input: {ex.input_text}\nOutput: {ex.output_text}"
            )

        # Add final user prompt
        parts.append(f"Input: {original}\nOutput:")

        return "\n\n".join(parts)

    def _call_llm(self, prompt_text: str) -> LLMResponse:
        """Send prompt to the LLM client."""
        req = LLMRequest(
            model_name=self.model_name,
            prompt=prompt_text,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return self._llm.complete(req)

    def run(self, prompts: List[PromptVariant]) -> List[BaselineResult]:
        """Apply Few-Shot prompting to a list of prompt variants."""
        results: List[BaselineResult] = []

        for p in prompts:
            fs_prompt = self._build_fewshot_prompt(p.prompt_text)
            response = self._call_llm(fs_prompt)

            results.append(
                BaselineResult(
                    task_id=p.task_id,
                    prompt_length=p.length,
                    prompt_text=fs_prompt,
                    predicted_answer=response.text,
                    tokens_input=response.tokens_input,
                    tokens_output=response.tokens_output,
                )
            )

        return results
