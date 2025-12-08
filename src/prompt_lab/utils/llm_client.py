"""
LLM client abstraction for the Prompt Lab project.

Right now this module provides:
- data classes for request/response
- an abstract `LLMClient` interface
- a `DummyLLMClient` implementation that returns fake responses

Later, we can add a real implementation that talks to an actual API
(e.g., OpenAI) without changing the rest of the code.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMRequest:
    """
    A simple request to an LLM.

    For now we only support:
    - model_name: which model to use
    - prompt: full prompt text
    - temperature: sampling temperature
    - max_tokens: maximum tokens in the response
    """
    model_name: str
    prompt: str
    temperature: float = 0.0
    max_tokens: int = 256


@dataclass
class LLMResponse:
    """
    A simple response from an LLM.

    We keep it minimal:
    - text: the generated answer
    - tokens_input: estimated number of input tokens (optional)
    - tokens_output: estimated number of output tokens (optional)
    """
    text: str
    tokens_input: Optional[int] = None
    tokens_output: Optional[int] = None


class LLMClient:
    """
    Abstract base class for LLM clients.

    Later we can create concrete subclasses like:
    - OpenAILLMClient
    - AnthropicLLMClient
    and use them via this common interface.
    """

    def complete(self, request: LLMRequest) -> LLMResponse:
        """
        Execute a completion request.

        Subclasses MUST override this.
        """
        raise NotImplementedError("LLMClient.complete() must be implemented by subclasses.")


class DummyLLMClient(LLMClient):
    """
    A dummy LLM client used for testing the pipeline structure.

    It does NOT call any real API. It just returns a simple
    canned response that includes part of the prompt.
    """

    def complete(self, request: LLMRequest) -> LLMResponse:
        # Very naive "fake" answer: echo part of the prompt and add a note.
        snippet = request.prompt[:80].replace("\n", " ")
        fake_text = (
            f"[DUMMY RESPONSE] I received a prompt starting with: '{snippet}...'. "
            f"This is a fake answer for model '{request.model_name}'."
        )

        # We don't compute real tokens here, but we can return rough dummy values.
        return LLMResponse(
            text=fake_text,
            tokens_input=len(request.prompt.split()),
            tokens_output=len(fake_text.split()),
        )
