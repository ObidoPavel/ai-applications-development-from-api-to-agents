from openai import OpenAI, AsyncOpenAI

from commons.models.message import Message
from commons.models.role import Role
from t1_llm_api.openai.base import BaseOpenAIClient


class OpenAIResponsesClient(BaseOpenAIClient):
    """
    Client for OpenAI Responses API using the official SDK.

    This implementation uses the official OpenAI Python library to interact
    with the Responses API, which uses 'instructions' instead of system messages
    and 'input' instead of messages.

    Attributes:
        _client (OpenAI): Synchronous OpenAI client instance.
        _async_client (AsyncOpenAI): Asynchronous OpenAI client instance.
        Inherits all other attributes from BaseOpenAIClient.
    """

    def __init__(self, endpoint: str, model_name: str, system_prompt: str, api_key: str):
        super().__init__(endpoint, model_name, system_prompt, api_key)
        raw_key = api_key.replace("Bearer ", "") if api_key.startswith("Bearer ") else api_key
        self._client = OpenAI(api_key=raw_key)
        self._async_client = AsyncOpenAI(api_key=raw_key)

    def response(self, messages: list[Message], **kwargs) -> Message:
        input_messages = [m.to_dict() for m in messages]
        api_response = self._client.responses.create(
            model=self._model_name,
            input=input_messages,
            instructions=self._system_prompt,
        )
        content = api_response.output_text or ""
        print(content)
        return Message(Role.ASSISTANT, content)

    async def stream_response(self, messages: list[Message], **kwargs) -> Message:
        input_messages = [m.to_dict() for m in messages]
        parts: list[str] = []
        with self._client.responses.stream(
            model=self._model_name,
            input=input_messages,
            instructions=self._system_prompt,
            stream=True,
        ) as stream:
            for event in stream:
                if hasattr(event, "delta") and event.delta:
                    parts.append(event.delta)
                    print(event.delta, end="", flush=True)
        print()
        return Message(Role.ASSISTANT, "".join(parts))