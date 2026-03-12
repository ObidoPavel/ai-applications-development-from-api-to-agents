import json
import aiohttp
import requests

from commons.models.message import Message
from commons.models.role import Role
from t1_llm_api.openai.base import BaseOpenAIClient


class CustomOpenAIClient(BaseOpenAIClient):
    """
    Custom HTTP client for OpenAI Chat Completions API.

    This implementation uses raw HTTP requests (requests/aiohttp) instead of
    the official SDK, providing more control over the HTTP layer and demonstrating
    how to interact with the API directly.
    """

    def response(self, messages: list[Message], **kwargs) -> Message:
        headers = {
            "Authorization": self._api_key,
            "Content-Type": "application/json",
        }
        api_messages = [{"role": Role.SYSTEM.value, "content": self._system_prompt}]
        api_messages.extend(m.to_dict() for m in messages)
        payload = {"model": self._model_name, "messages": api_messages}
        response = requests.post(self._endpoint, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        choices = data.get("choices", [])
        if not choices:
            raise ValueError("No choices in the response")
        content = choices[0].get("message", {}).get("content") or ""
        print(content)
        return Message(Role.ASSISTANT, content)

    async def stream_response(self, messages: list[Message], **kwargs) -> Message:
        """
        Get a streaming response using raw HTTP with Server-Sent Events (SSE).

        The response is streamed token-by-token using OpenAI's SSE format,
        with each chunk printed immediately as it arrives.

        Args:
            messages (list[Message]): The conversation history.
            **kwargs: Additional parameters for the API (currently unused).

        Returns:
            Message: The complete AI response message after all chunks are received.

        Note:
            The system prompt is automatically prepended to the messages.
            Each token is printed to stdout as it arrives.
            Uses Server-Sent Events (SSE) format where each line starts with "data: ".
        """
    async def stream_response(self, messages: list[Message], **kwargs) -> Message:
        headers = {
            "Authorization": self._api_key,
            "Content-Type": "application/json",
        }
        api_messages = [{"role": Role.SYSTEM.value, "content": self._system_prompt}]
        api_messages.extend(m.to_dict() for m in messages)
        payload = {"model": self._model_name, "messages": api_messages, "stream": True}
        parts: list[str] = []
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self._endpoint, headers=headers, json=payload
            ) as response:
                response.raise_for_status()
                async for line in response.content:
                    line_str = line.decode().strip()
                    if line_str.startswith("data: "):
                        data_str = line_str[6:]
                        if data_str == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data_str)
                            for choice in chunk.get("choices", []):
                                delta = choice.get("delta", {})
                                if "content" in delta and delta["content"]:
                                    parts.append(delta["content"])
                                    print(delta["content"], end="", flush=True)
                        except json.JSONDecodeError:
                            pass
        print()
        return Message(Role.ASSISTANT, "".join(parts))
