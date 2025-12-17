"""
Public interface for the azure_openai_helper package.
"""

from .llm_client import (
    llm_query,
    validate_configuration,
    ConfigurationError,
    get_available_models,
)

__all__ = [
    "llm_query",
    "validate_configuration",
    "ConfigurationError",
    "get_available_models",
]
