# Helper - Prompt Log

This file contains all user prompts related to llm Helper, in chronological order.

---

## Session Date: December 6, 2025

### Prompt 1
```
You are an LLM research assistant tasked with exploring how large language models behave when working with long contexts. Your goal is to help analyze and interpret the model’s strengths and limitations in situations where important information may be hidden, diluted, compressed, or retrieved in different ways.

In this lab, you will examine how the amount, position, and organization of context influence the model’s ability to recall facts, answer questions accurately, and respond efficiently. You will also evaluate alternative strategies for managing context—such as selecting relevant information, compressing content, or maintaining structured external memory—and compare them to the results of providing full context directly.

Across the four experiments, your role is to observe patterns, highlight failures, and document insights about how the model interacts with different types of context. The goal is to build an intuitive and practical understanding of when long contexts help, when they hinder performance, and when retrieval or structured prompts become necessary.

Your outputs should focus on clarity, comparison, and interpretation. For each experiment, summarize what happens, identify the key behaviors that emerge, and explain what these behaviors suggest about the capabilities and limitations of current LLMs.

For now, just understand our needs and wait for my inputs.
```

---

### Prompt 2
```
First, lets create a Python helper module that will be used throughout all lab experiments to interact with an LLM hosted on Azure OpenAI.
The helper must Load all required configuration values from a .env file.

Expose a clean function such as llm_query(prompt: str) -> str that sends the user prompt to the Azure OpenAI ChatCompletion API, Handles response extraction and error management, Returns only the model’s final text output and Supports optional parameters: temperature, max_tokens.

Use python-dotenv to load the .env file.
Make the helper robust: Validate that all required env variables exist, Raise clear errors if configuration is missing, Handle API failures gracefully.
Do not hardcode any values; everything must come from environment variables.

Generate the full Python code for this helper module.
Add short documentation for this helper in Readme.md file within the helper directory.
```

---

### Prompt 3
```
create my .env actual file instead of the example one

ENDPOINT
************************

API_KEY
************************

DEPLOYMENT_NAME
gpt-4o

API_VERSION
2024-12-01-preview



after that, add to our module simple unit test for validation


```

---