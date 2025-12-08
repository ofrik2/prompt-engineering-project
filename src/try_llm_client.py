from prompt_lab.utils.llm_client import LLMRequest, DummyLLMClient


def main() -> None:
    client = DummyLLMClient()

    request = LLMRequest(
        model_name="dummy-model",
        prompt="Explain in one sentence what prompt engineering is.",
        temperature=0.0,
        max_tokens=64,
    )

    response = client.complete(request)

    print("=== Dummy LLM Client Demo ===")
    print("Request model   :", request.model_name)
    print("Request prompt  :", request.prompt)
    print("---")
    print("Response text   :", response.text)
    print("Tokens (input)  :", response.tokens_input)
    print("Tokens (output) :", response.tokens_output)


if __name__ == "__main__":
    main()
