from openai import OpenAI, AsyncOpenAI

from commons.models.message import Message
from commons.models.role import Role
from t1_llm_api.openai.base import BaseOpenAIClient


class OpenAIClient(BaseOpenAIClient):
    """
    Client for OpenAI Chat Completions API using the official SDK.

    This implementation uses the official OpenAI Python library to interact
    with the Chat Completions API, providing both synchronous and streaming
    response capabilities.

    Attributes:
        _client (OpenAI): Synchronous OpenAI client instance.
        _async_client (AsyncOpenAI): Asynchronous OpenAI client instance.
        Inherits all other attributes from BaseOpenAIClient.
    """

    def __init__(self, endpoint: str, model_name: str, system_prompt: str, api_key: str):
        super().__init__(endpoint, model_name, system_prompt, api_key)
        self._client = OpenAI(api_key=api_key.replace("Bearer ", "") if api_key.startswith("Bearer ") else api_key)
        self._async_client = AsyncOpenAI(api_key=api_key.replace("Bearer ", "") if api_key.startswith("Bearer ") else api_key)

    def response(self, messages: list[Message], **kwargs) -> Message:
        api_messages = [{"role": Role.SYSTEM.value, "content": self._system_prompt}]
        api_messages.extend(m.to_dict() for m in messages)
        response = self._client.chat.completions.create(
            model=self._model_name,
            messages=api_messages,
        )
        content = response.choices[0].message.content or ""
        print(content)
        return Message(Role.ASSISTANT, content)

    async def stream_response(self, messages: list[Message], **kwargs) -> Message:
        api_messages = [{"role": Role.SYSTEM.value, "content": self._system_prompt}]
        api_messages.extend(m.to_dict() for m in messages)
        stream = await self._async_client.chat.completions.create(
            model=self._model_name,
            messages=api_messages,
            stream=True,
        )
        parts: list[str] = []
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                delta = chunk.choices[0].delta.content
                parts.append(delta)
                print(delta, end="", flush=True)
        print()
        return Message(Role.ASSISTANT, "".join(parts))
