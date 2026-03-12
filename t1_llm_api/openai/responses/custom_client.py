import json
import aiohttp
import requests

from commons.models.message import Message
from commons.models.role import Role
from t1_llm_api.openai.base import BaseOpenAIClient


class CustomOpenAIResponsesClient(BaseOpenAIClient):
    """
    Custom HTTP client for OpenAI Responses API.

    This implementation uses raw HTTP requests (requests/aiohttp) instead of
    the official SDK, demonstrating how to interact with the Responses API directly
    and handle its unique event-based streaming format.
    """

    def response(self, messages: list[Message], **kwargs) -> Message:
        headers = {
            "Authorization": self._api_key,
            "Content-Type": "application/json",
        }
        input_messages = [m.to_dict() for m in messages]
        payload = {
            "model": self._model_name,
            "input": input_messages,
            "instructions": self._system_prompt,
        }
        response = requests.post(self._endpoint, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        output_list = data.get("output", [])
        if not output_list:
            raise ValueError("No output in the response")
        content_parts = output_list[0].get("content", [])
        content = "".join(
            p.get("text", "") for p in content_parts if p.get("type") == "output_text"
        )
        print(content)
        return Message(Role.ASSISTANT, content)

    async def stream_response(self, messages: list[Message], **kwargs) -> Message:
        headers = {
            "Authorization": self._api_key,
            "Content-Type": "application/json",
        }
        input_messages = [m.to_dict() for m in messages]
        payload = {
            "model": self._model_name,
            "input": input_messages,
            "instructions": self._system_prompt,
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
                    if line_str.startswith("event: "):
                        event_type = line_str[7:]
                    elif line_str.startswith("data: "):
                        data_str = line_str[6:]
                        try:
                            data = json.loads(data_str)
                            if data.get("type") == "response.output_text.delta":
                                delta = data.get("delta", "")
                                if delta:
                                    parts.append(delta)
                                    print(delta, end="", flush=True)
                        except json.JSONDecodeError:
                            pass
        print()
        return Message(Role.ASSISTANT, "".join(parts))
