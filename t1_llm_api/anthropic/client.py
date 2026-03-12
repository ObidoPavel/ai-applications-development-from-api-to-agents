from anthropic import Anthropic, AsyncAnthropic

from commons.models.message import Message
from commons.models.role import Role
from t1_llm_api.base_client import AIClient


class AnthropicAIClient(AIClient):
    """
    Client for Anthropic's Claude API using the official SDK.

    This implementation uses the official Anthropic Python library to interact
    with Claude models, providing both synchronous and streaming response capabilities.

    Attributes:
        _client (Anthropic): Synchronous Anthropic client instance.
        _async_client (AsyncAnthropic): Asynchronous Anthropic client instance.
        Inherits all other attributes from AIClient.
    """

    def __init__(self, endpoint: str, model_name: str, api_key: str, system_prompt: str):
        super().__init__(endpoint, model_name, api_key, system_prompt)
        self._client = Anthropic(api_key=api_key)
        self._async_client = AsyncAnthropic(api_key=api_key)

    def response(self, messages: list[Message], **kwargs) -> Message:
        max_tokens = kwargs.get("max_tokens", 1024)
        api_messages = [m.to_dict() for m in messages]
        response = self._client.messages.create(
            model=self._model_name,
            max_tokens=max_tokens,
            system=self._system_prompt,
            messages=api_messages,
        )
        content = "".join(
            block.text
            for block in response.content
            if hasattr(block, "text") and block.text
        )
        print(content)
        return Message(Role.ASSISTANT, content)

    async def stream_response(self, messages: list[Message], **kwargs) -> Message:
        max_tokens = kwargs.get("max_tokens", 1024)
        api_messages = [m.to_dict() for m in messages]
        parts: list[str] = []
        async with self._async_client.messages.stream(
            model=self._model_name,
            max_tokens=max_tokens,
            system=self._system_prompt,
            messages=api_messages,
        ) as stream:
            async for event in stream:
                if event.type == "content_block_delta":
                    if hasattr(event, "delta") and event.delta.text:
                        parts.append(event.delta.text)
                        print(event.delta.text, end="", flush=True)
        print()
        return Message(Role.ASSISTANT, "".join(parts))
