import json
import aiohttp
import requests

from commons.models.message import Message
from commons.models.role import Role
from t1_llm_api.base_client import AIClient


class CustomGeminiAIClient(AIClient):
    """
    Custom HTTP client for Google Gemini API.

    This implementation uses raw HTTP requests (requests/aiohttp) instead of
    the official SDK, demonstrating how to interact with Gemini's API directly
    and handle its Server-Sent Events (SSE) streaming format.
    """

    def response(self, messages: list[Message], **kwargs) -> Message:
        max_tokens = kwargs.get("max_tokens", 1024)
        url = f"{self._endpoint}/{self._model_name}:generateContent"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self._api_key,
        }
        contents = [
            {
                "role": "model" if m.role == Role.ASSISTANT else "user",
                "parts": [{"text": m.content}],
            }
            for m in messages
        ]
        payload = {
            "system_instruction": {"parts": [{"text": self._system_prompt}]},
            "contents": contents,
            "generationConfig": {"maxOutputTokens": max_tokens},
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        candidates = data.get("candidates", [])
        if not candidates:
            raise ValueError("No candidates in the response")
        parts_list = candidates[0].get("content", {}).get("parts", [])
        content = "".join(p.get("text", "") for p in parts_list)
        print(content)
        return Message(Role.ASSISTANT, content)

    async def stream_response(self, messages: list[Message], **kwargs) -> Message:
        max_tokens = kwargs.get("max_tokens", 1024)
        url = f"{self._endpoint}/{self._model_name}:streamGenerateContent?alt=sse"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self._api_key,
        }
        contents = [
            {
                "role": "model" if m.role == Role.ASSISTANT else "user",
                "parts": [{"text": m.content}],
            }
            for m in messages
        ]
        payload = {
            "system_instruction": {"parts": [{"text": self._system_prompt}]},
            "contents": contents,
            "generationConfig": {"maxOutputTokens": max_tokens},
        }
        parts: list[str] = []
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                response.raise_for_status()
                async for line in response.content:
                    line_str = line.decode().strip()
                    if line_str.startswith("data: "):
                        data_str = line_str[6:]
                        try:
                            data = json.loads(data_str)
                            for c in data.get("candidates", []):
                                for p in c.get("content", {}).get("parts", []):
                                    if "text" in p:
                                        parts.append(p["text"])
                                        print(p["text"], end="", flush=True)
                        except json.JSONDecodeError:
                            pass
        print()
        return Message(Role.ASSISTANT, "".join(parts))