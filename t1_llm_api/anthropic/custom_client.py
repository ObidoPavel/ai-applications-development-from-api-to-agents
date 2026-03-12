import json
import aiohttp
import requests

from commons.models.message import Message
from commons.models.role import Role
from t1_llm_api.base_client import AIClient


class CustomAnthropicAIClient(AIClient):
    """
    Custom HTTP client for Anthropic's Claude API.

    This implementation uses raw HTTP requests (requests/aiohttp) instead of
    the official SDK, demonstrating how to interact with Claude's API directly
    and handle its Server-Sent Events (SSE) streaming format.
    """

    def response(self, messages: list[Message], **kwargs) -> Message:
        max_tokens = kwargs.get("max_tokens", 1024)
        headers = {
            "x-api-key": self._api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        api_messages = [m.to_dict() for m in messages]
        payload = {
            "model": self._model_name,
            "max_tokens": max_tokens,
            "system": self._system_prompt,
            "messages": api_messages,
        }
        response = requests.post(self._endpoint, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        content_blocks = data.get("content", [])
        if not content_blocks:
            raise ValueError("No content blocks in the response")
        content = "".join(
            b.get("text", "") for b in content_blocks if b.get("type") == "text"
        )
        print(content)
        return Message(Role.ASSISTANT, content)

    async def stream_response(self, messages: list[Message], **kwargs) -> Message:
        max_tokens = kwargs.get("max_tokens", 1024)
        headers = {
            "x-api-key": self._api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        api_messages = [m.to_dict() for m in messages]
        payload = {
            "model": self._model_name,
            "max_tokens": max_tokens,
            "system": self._system_prompt,
            "messages": api_messages,
            "stream": True,
        }
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
                        try:
                            data = json.loads(data_str)
                            if data.get("type") == "content_block_delta":
                                delta = data.get("delta", {})
                                if delta.get("type") == "text_delta" and delta.get("text"):
                                    text = delta["text"]
                                    parts.append(text)
                                    print(text, end="", flush=True)
                        except json.JSONDecodeError:
                            pass
        print()
        return Message(Role.ASSISTANT, "".join(parts))

