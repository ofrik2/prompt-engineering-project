# Azure OpenAI Helper Module

A robust Python helper module for interacting with Azure OpenAI's ChatCompletion API. This module provides a clean, error-resistant interface for querying large language models with full configuration management through environment variables.

## Features

- **Environment-based configuration**: All settings loaded from `.env` file
- **Clean API**: Simple `llm_query()` function for LLM interactions
- **Robust error handling**: Validates configuration and handles API failures gracefully
- **Type hints**: Full type annotations for better IDE support
- **Flexible parameters**: Support for temperature, max_tokens, and system messages
- **No hardcoded values**: Everything configurable through environment variables

## Installation

### Required Dependencies

```bash
pip install openai python-dotenv
```

## Testing

To verify your installation and configuration, run the included validation test suite:

```bash
python azure_openai_helper\test_validation.py
```

### What the Tests Verify

The test suite performs three categories of validation:

1. **Configuration Validation**: Ensures all required environment variables are loaded correctly from `.env` and displays their values (with API key masking for security)

2. **Parameter Validation**: Tests input validation logic including:
   - Empty prompt rejection
   - Temperature range validation (0.0-2.0)
   - Max tokens positive integer validation

3. **End-to-End Query Test**: Makes an actual API call to Azure OpenAI with a simple prompt to verify:
   - Successful connection to your deployment
   - Proper API authentication
   - Response extraction and formatting

All tests must pass (shown with ✓) before using the helper in your experiments. This ensures configuration correctness and API connectivity without manual debugging.

## Configuration

Create a `.env` file in your project root with the following required variables:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_OPENAI_ENDPOINT` | Your Azure OpenAI resource endpoint | `https://myresource.openai.azure.com/` |
| `AZURE_OPENAI_API_KEY` | API key for authentication | `abc123...` |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Name of your deployed model | `gpt-4` |
| `AZURE_OPENAI_API_VERSION` | API version to use | `2024-02-15-preview` |

## Usage

### Basic Query

```python
from azure_openai_helper import llm_query

# Simple query
response = llm_query("What is the capital of France?")
print(response)
```

### With Optional Parameters

```python
from azure_openai_helper import llm_query

# Query with temperature control
response = llm_query(
    prompt="Write a creative story about a robot.",
    temperature=0.9,  # Higher temperature for more creativity
    max_tokens=500    # Limit response length
)
print(response)

# Query with system message
response = llm_query(
    prompt="Analyze this code for bugs.",
    system_message="You are an expert code reviewer.",
    temperature=0.3   # Lower temperature for more focused analysis
)
print(response)
```

### Configuration Validation

```python
from azure_openai_helper import validate_configuration

# Validate configuration before making queries
try:
    validate_configuration()
    print("Configuration is valid!")
except ConfigurationError as e:
    print(f"Configuration error: {e}")
```

## API Reference

### `llm_query(prompt, temperature=None, max_tokens=None, system_message=None)`

Query Azure OpenAI's ChatCompletion API.

**Parameters:**
- `prompt` (str): The user's input prompt to send to the LLM
- `temperature` (float, optional): Controls randomness (0.0-2.0). Lower is more deterministic. Default uses model's default.
- `max_tokens` (int, optional): Maximum number of tokens in the response. Default uses model's default.
- `system_message` (str, optional): System message to set context/behavior. Default is None.

**Returns:**
- `str`: The model's text response

**Raises:**
- `ConfigurationError`: If required environment variables are missing
- `ValueError`: If prompt is empty or parameters are invalid
- `APIError`: If the Azure OpenAI API returns an error
- `APIConnectionError`: If there's a connection issue
- `RateLimitError`: If rate limits are exceeded
- `OpenAIError`: For other API-related errors

### `validate_configuration()`

Validate that all required configuration is present.

**Returns:**
- `bool`: True if configuration is valid

**Raises:**
- `ConfigurationError`: If configuration is invalid or missing

## Error Handling

The module provides comprehensive error handling:

```python
from azure_openai_helper import llm_query, ConfigurationError
from openai import APIError, RateLimitError

try:
    response = llm_query("Hello, world!")
    print(response)
except ConfigurationError as e:
    print(f"Configuration problem: {e}")
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except APIError as e:
    print(f"API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

1. **Always use a `.env` file**: Keep sensitive credentials out of your code
2. **Validate configuration early**: Call `validate_configuration()` at startup
3. **Handle errors appropriately**: Implement try-except blocks for production code
4. **Use temperature wisely**: 
   - 0.0-0.3: Focused, deterministic tasks (analysis, extraction)
   - 0.4-0.7: Balanced responses (general questions)
   - 0.8-2.0: Creative tasks (storytelling, brainstorming)
5. **Set max_tokens**: Prevent unexpectedly long responses and control costs

## Example: Context Window Lab Integration

```python
from azure_openai_helper import llm_query

def run_experiment(context: str, question: str) -> str:
    """
    Run a context window experiment.
    
    Args:
        context: Background information/context
        question: Question to answer based on context
        
    Returns:
        Model's response
    """
    prompt = f"""Context:
{context}

Question: {question}

Answer:"""
    
    return llm_query(
        prompt=prompt,
        temperature=0.0,  # Deterministic for reproducible experiments
        max_tokens=200
    )

# Run experiment
context = "The sky is blue. Water is wet. Fire is hot."
question = "What color is the sky?"
answer = run_experiment(context, question)
print(answer)
```

## Troubleshooting

### "Missing required environment variables"
- Ensure your `.env` file exists in the project root
- Check that all required variables are set
- Verify no typos in variable names

### "Failed to initialize Azure OpenAI client"
- Verify your endpoint URL format (should end with `/`)
- Check that your API key is valid
- Ensure your deployment name matches your Azure resource

### "Connection error"
- Check your internet connection
- Verify the endpoint URL is correct
- Check if there are firewall restrictions

### "Rate limit exceeded"
- Implement retry logic with exponential backoff
- Reduce request frequency
- Consider upgrading your Azure OpenAI tier

## License

This helper module is part of the Context Window Labs research project.
