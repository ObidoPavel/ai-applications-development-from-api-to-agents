from google import genai
from google.genai import types

from commons.models.message import Message
from commons.models.role import Role
from t1_llm_api.base_client import AIClient


class GeminiAIClient(AIClient):
    """
    Client for Google Gemini API using the official SDK.

    This implementation uses the official Google GenAI Python library to interact
    with Gemini models, providing both synchronous and streaming response capabilities.

    Attributes:
        _client (genai.Client): Google GenAI client instance.
        Inherits all other attributes from AIClient.
    """

    def __init__(self, endpoint: str, model_name: str, api_key: str, system_prompt: str):
        super().__init__(endpoint, model_name, api_key, system_prompt)
        self._client = genai.Client(api_key=api_key)

    def response(self, messages: list[Message], **kwargs) -> Message:
        max_tokens = kwargs.get("max_output_tokens", kwargs.get("max_tokens", 1024))
        contents = self._to_contents(messages)
        config = types.GenerateContentConfig(
            system_instruction=self._system_prompt,
            max_output_tokens=max_tokens,
        )
        response = self._client.models.generate_content(
            model=self._model_name,
            contents=contents,
            config=config,
        )
        content = response.text or ""
        print(content)
        return Message(Role.ASSISTANT, content)

    async def stream_response(self, messages: list[Message], **kwargs) -> Message:
        max_tokens = kwargs.get("max_output_tokens", kwargs.get("max_tokens", 1024))
        contents = self._to_contents(messages)
        config = types.GenerateContentConfig(
            system_instruction=self._system_prompt,
            max_output_tokens=max_tokens,
        )
        parts: list[str] = []
        async for chunk in self._client.aio.models.generate_content_stream(
            model=self._model_name,
            contents=contents,
            config=config,
        ):
            if chunk.text:
                parts.append(chunk.text)
                print(chunk.text, end="", flush=True)
        print()
        return Message(Role.ASSISTANT, "".join(parts))

    def _to_contents(self, messages: list[Message]) -> list[types.Content]:
        result: list[types.Content] = []
        for msg in messages:
            role = "model" if msg.role == Role.ASSISTANT else "user"
            result.append(
                types.Content(
                    role=role, parts=[types.Part.from_text(text=msg.content)]
                )
            )
        return result