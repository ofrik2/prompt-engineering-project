"""
LLM client abstraction for the Prompt Lab project.

- LLMRequest / LLMResponse dataclasses
- LLMClient abstract base
- DummyLLMClient: fake, deterministic responses (no network)
- OpenAILLMClient: real client using OpenAI's Python SDK (optional)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import os


@dataclass
class LLMRequest:
    """
    A simple request to an LLM.
    """
    model_name: str
    prompt: str
    temperature: float = 0.0
    max_tokens: int = 256


@dataclass
class LLMResponse:
    """
    A simple response from an LLM.
    """
    text: str
    tokens_input: Optional[int] = None
    tokens_output: Optional[int] = None


class LLMClient:
    """
    Abstract base class for LLM clients.
    """

    def complete(self, request: LLMRequest) -> LLMResponse:
        raise NotImplementedError("LLMClient.complete() must be implemented by subclasses.")


class DummyLLMClient(LLMClient):
    """
    A dummy LLM client used for testing the pipeline structure.
    """

    def complete(self, request: LLMRequest) -> LLMResponse:
        snippet = request.prompt[:80].replace("\n", " ")
        fake_text = (
            f"[DUMMY RESPONSE] I received a prompt starting with: '{snippet}...'. "
            f"This is a fake answer for model '{request.model_name}'."
        )

        return LLMResponse(
            text=fake_text,
            tokens_input=len(request.prompt.split()),
            tokens_output=len(fake_text.split()),
        )


class OpenAILLMClient(LLMClient):
    """
    Real LLM client using the OpenAI Python SDK.

    Expects an environment variable OPENAI_API_KEY to be set.
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        # Delay import so that dummy usage doesn't require openai installed
        try:
            from openai import OpenAI  # type: ignore
        except ImportError as e:
            raise ImportError(
                "The 'openai' package is not installed. "
                "Install it with: pip install openai"
            ) from e

        self._OpenAI = OpenAI
        self._api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self._api_key:
            raise ValueError(
                "OPENAI_API_KEY is not set. Please set it in your environment "
                "before using OpenAILLMClient."
            )

        # Create the underlying OpenAI client
        self._client = self._OpenAI(api_key=self._api_key)

    def complete(self, request: LLMRequest) -> LLMResponse:
        """
        Call OpenAI's chat completions endpoint with a simple user message.
        """
        # We assume model_name is a chat-capable model (gpt-4.1-mini, gpt-4o, etc.)
        resp = self._client.chat.completions.create(
            model=request.model_name,
            messages=[
                {"role": "user", "content": request.prompt},
            ],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        # Grab the first choice
        text = resp.choices[0].message.content or ""

        # The v1 SDK has 'usage' with token counts
        tokens_input = getattr(resp.usage, "prompt_tokens", None)
        tokens_output = getattr(resp.usage, "completion_tokens", None)

        return LLMResponse(
            text=text,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
        )
