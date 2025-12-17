"""
Azure OpenAI LLM Client

This module provides a clean interface for querying Azure OpenAI's ChatCompletion API.
All configuration is loaded from environment variables using python-dotenv.
Supports multiple model deployments for comparative experiments.
"""

import os
from typing import Optional, Dict
from dotenv import load_dotenv
from openai import AzureOpenAI
from openai import OpenAIError, APIError, APIConnectionError, RateLimitError


class ConfigurationError(Exception):
    """Raised when required configuration is missing or invalid."""
    pass


def _load_configuration() -> dict:
    """
    Load and validate Azure OpenAI configuration from environment variables.

    Returns:
        dict: Configuration dictionary with all required values

    Raises:
        ConfigurationError: If any required environment variable is missing
    """
    # Load environment variables from .env file
    load_dotenv()

    # Required environment variables for primary model
    required_vars = {
        'AZURE_OPENAI_ENDPOINT': os.getenv('AZURE_OPENAI_ENDPOINT'),
        'AZURE_OPENAI_API_KEY': os.getenv('AZURE_OPENAI_API_KEY'),
        'AZURE_OPENAI_DEPLOYMENT_NAME': os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME'),
        'AZURE_OPENAI_API_VERSION': os.getenv('AZURE_OPENAI_API_VERSION'),
    }

    # Validate all required variables are present
    missing_vars = [key for key, value in required_vars.items() if not value]

    if missing_vars:
        raise ConfigurationError(
            f"Missing required environment variables: {', '.join(missing_vars)}\n"
            f"Please ensure these are set in your .env file."
        )

    # Optional secondary model configuration
    secondary_vars = [
        'AZURE_OPENAI_DEPLOYMENT_NAME_SECONDARY',
        'AZURE_OPENAI_ENDPOINT_SECONDARY',
        'AZURE_OPENAI_API_KEY_SECONDARY'
    ]

    has_all_secondary = all(os.getenv(var) for var in secondary_vars)
    if has_all_secondary:
        required_vars['AZURE_OPENAI_DEPLOYMENT_NAME_SECONDARY'] = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME_SECONDARY')
        required_vars['AZURE_OPENAI_ENDPOINT_SECONDARY'] = os.getenv('AZURE_OPENAI_ENDPOINT_SECONDARY')
        required_vars['AZURE_OPENAI_API_KEY_SECONDARY'] = os.getenv('AZURE_OPENAI_API_KEY_SECONDARY')
        required_vars['has_secondary_model'] = True
    else:
        required_vars['has_secondary_model'] = False

    return required_vars


def validate_configuration() -> Dict[str, any]:
    """
    Validate that all required configuration is present.

    Returns:
        dict: Configuration dictionary with validation status

    Raises:
        ConfigurationError: If configuration is invalid or missing
    """
    config = _load_configuration()
    return config


def get_available_models() -> Dict[str, str]:
    """
    Get a dictionary of available models and their deployment names.

    Returns:
        dict: Map of model identifiers to deployment names
    """
    config = _load_configuration()

    models = {
        'primary': config['AZURE_OPENAI_DEPLOYMENT_NAME']
    }

    if config.get('has_secondary_model'):
        models['secondary'] = config['AZURE_OPENAI_DEPLOYMENT_NAME_SECONDARY']

    return models


def get_client(model: Optional[str] = None) -> AzureOpenAI:
    """
    Get an AzureOpenAI client instance for direct API access.
    Useful for embeddings, custom calls, etc.

    Args:
        model: Which model configuration to use
               - None (default): Uses primary model
               - "primary": Uses primary model
               - "secondary": Uses secondary model

    Returns:
        AzureOpenAI: Configured client instance

    Raises:
        ConfigurationError: If required environment variables are missing
        ValueError: If model is invalid
    """
    config = _load_configuration()

    # Determine which configuration to use
    if model is None or model == "primary":
        endpoint = config['AZURE_OPENAI_ENDPOINT']
        api_key = config['AZURE_OPENAI_API_KEY']
    elif model == "secondary":
        if not config.get('has_secondary_model'):
            raise ValueError("Secondary model configuration is not available")
        endpoint = config['AZURE_OPENAI_ENDPOINT_SECONDARY']
        api_key = config['AZURE_OPENAI_API_KEY_SECONDARY']
    else:
        # Assume it's a deployment name, use primary config
        endpoint = config['AZURE_OPENAI_ENDPOINT']
        api_key = config['AZURE_OPENAI_API_KEY']

    # Create and return client
    return AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=config['AZURE_OPENAI_API_VERSION']
    )


def llm_query(
    prompt: str,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    system_message: Optional[str] = None,
    model: Optional[str] = None
) -> str:
    """
    Query Azure OpenAI's ChatCompletion API with a user prompt.

    Args:
        prompt: The user's input prompt to send to the LLM
        temperature: Controls randomness (0.0-2.0). Lower is more deterministic.
                    If None, uses the model's default.
        max_tokens: Maximum number of tokens in the response.
                   If None, uses the model's default.
        system_message: Optional system message to set context/behavior.
                       If None, no system message is included.
        model: Which model to use. Can be:
               - None (default): Uses primary model
               - "primary": Uses primary model (GPT-4o)
               - "secondary": Uses secondary model (Phi-4-mini-instruct)
               - Deployment name string: Uses that specific deployment

    Returns:
        str: The model's text response

    Raises:
        ConfigurationError: If required environment variables are missing
        ValueError: If prompt is empty or parameters are invalid
        APIError: If the Azure OpenAI API returns an error
        APIConnectionError: If there's a connection issue
        RateLimitError: If rate limits are exceeded
        OpenAIError: For other API-related errors
    """
    # Validate input
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")

    if temperature is not None and not (0.0 <= temperature <= 2.0):
        raise ValueError("Temperature must be between 0.0 and 2.0")

    if max_tokens is not None and max_tokens <= 0:
        raise ValueError("max_tokens must be a positive integer")

    # Load configuration
    try:
        config = _load_configuration()
    except ConfigurationError as e:
        raise ConfigurationError(f"Configuration error: {e}")

    # Determine which model to use
    use_secondary = False
    deployment_name = config['AZURE_OPENAI_DEPLOYMENT_NAME']

    if model == "secondary":
        if not config.get('has_secondary_model', False):
            raise ConfigurationError("Secondary model requested but not configured in .env")
        use_secondary = True
        deployment_name = config['AZURE_OPENAI_DEPLOYMENT_NAME_SECONDARY']
    elif model == "primary":
        use_secondary = False
    elif model is not None:
        # Assume it's a specific deployment name
        deployment_name = model
        # Check if it matches secondary config
        if config.get('has_secondary_model', False) and model == config.get('AZURE_OPENAI_DEPLOYMENT_NAME_SECONDARY'):
            use_secondary = True

    # Initialize Azure OpenAI client with appropriate credentials
    try:
        if use_secondary:
            # Azure AI Foundry uses a slightly different pattern
            # The endpoint for AI Foundry should not include the trailing path
            endpoint = config['AZURE_OPENAI_ENDPOINT_SECONDARY']
            # Remove any trailing slash or /models path
            if endpoint.endswith('/models'):
                endpoint = endpoint[:-7]
            elif endpoint.endswith('/models/'):
                endpoint = endpoint[:-8]

            client = AzureOpenAI(
                api_key=config['AZURE_OPENAI_API_KEY_SECONDARY'],
                api_version=config['AZURE_OPENAI_API_VERSION'],
                azure_endpoint=endpoint
            )
        else:
            client = AzureOpenAI(
                api_key=config['AZURE_OPENAI_API_KEY'],
                api_version=config['AZURE_OPENAI_API_VERSION'],
                azure_endpoint=config['AZURE_OPENAI_ENDPOINT']
            )
    except Exception as e:
        raise ConfigurationError(f"Failed to initialize Azure OpenAI client: {e}")

    # Build messages
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})

    # Build API parameters
    api_params = {
        "model": deployment_name,
        "messages": messages
    }

    if temperature is not None:
        api_params["temperature"] = temperature

    if max_tokens is not None:
        api_params["max_tokens"] = max_tokens

    # Make API call with error handling
    try:
        response = client.chat.completions.create(**api_params)

        # Extract and return the response text
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content
        else:
            raise APIError("No response choices returned from the API")

    except RateLimitError as e:
        raise RateLimitError(f"Rate limit exceeded: {e}")
    except APIConnectionError as e:
        raise APIConnectionError(f"Connection error: {e}")
    except APIError as e:
        raise

    except OpenAIError as e:
        raise OpenAIError(f"OpenAI error: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error during API call: {e}")
