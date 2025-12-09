"""
Project-wide LLM abstraction.

- LLMRequest / LLMResponse dataclasses
- LLMClient abstract base
- DummyLLMClient: fake, deterministic responses (for development)
- AzureOpenAILLMClient: adapter around the azure_openai_helper package
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import os


@dataclass
class LLMRequest:
    model_name: str
    prompt: str
    temperature: float = 0.0
    max_tokens: int = 256


@dataclass
class LLMResponse:
    text: str
    tokens_input: Optional[int] = None
    tokens_output: Optional[int] = None


class LLMClient:
    """Abstract base class for LLM clients."""

    def complete(self, request: LLMRequest) -> LLMResponse:
        raise NotImplementedError


class DummyLLMClient(LLMClient):
    """Fake client for development and testing."""

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


class AzureOpenAILLMClient(LLMClient):
    """
    Real client that uses your azure_openai_helper package to talk to Azure OpenAI.
    """

    def __init__(self, model_name: Optional[str] = None) -> None:
        # Import your helper here
        try:
            from azure_openai_helper import (
                llm_query,
                validate_configuration,
                ConfigurationError,
            )
        except ImportError as e:
            raise ImportError(
                "Could not import 'azure_openai_helper'. "
                "Make sure the azure_openai_helper folder is in your project root "
                "and has an __init__.py file."
            ) from e

        # Validate configuration and keep references
        try:
            self._config = validate_configuration()
        except ConfigurationError as e:
            raise ValueError(
                f"Azure OpenAI configuration is invalid: {e}"
            ) from e

        self._llm_query = llm_query
        # If a specific deployment name / label is passed, remember it.
        # Otherwise, the helper will use the primary deployment by default.
        self._model_name = model_name

    def complete(self, request: LLMRequest) -> LLMResponse:
        # Decide which "model" to pass to the helper:
        # - if request.model_name is set, prefer it
        # - otherwise, fall back to the model name from __init__
        model_to_use = request.model_name or self._model_name

        text = self._llm_query(
            prompt=request.prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            system_message=None,
            model=model_to_use,
        )

        # The helper doesn't currently expose token-level usage, so we keep them None.
        return LLMResponse(
            text=text,
            tokens_input=None,
            tokens_output=None,
        )
