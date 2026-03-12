import base64
import json
from pathlib import Path

import requests

from commons.constants import OPENAI_API_KEY, OPENAI_HOST


# https://developers.openai.com/api/docs/guides/audio#add-audio-to-your-existing-application

CHAT_COMPLETIONS_ENDPOINT = f"{OPENAI_HOST}/v1/chat/completions"


def run_speech_to_speech(
    question_audio_path: Path | None = None,
    output_path: Path | None = None,
    print_request: bool = True,
    print_response: bool = True,
) -> Path:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set")

    if question_audio_path is None:
        question_audio_path = Path(__file__).resolve().parent / "question.mp3"
    if not question_audio_path.is_file():
        raise FileNotFoundError(f"Audio file not found: {question_audio_path}")

    with open(question_audio_path, "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode("utf-8")

    content = [
        {
            "type": "input_audio",
            "input_audio": {
                "data": audio_base64,
                "format": "mp3",
            },
        },
    ]
    payload = {
        "model": "gpt-4o-audio-preview",
        "modalities": ["text", "audio"],
        "audio": {"voice": "ballad", "format": "mp3"},
        "messages": [{"role": "user", "content": content}],
    }
    if print_request:
        print(json.dumps({k: v if k != "messages" else [{"role": m["role"], "content": "[audio]"}] for k, v in payload.items()}, indent=2))

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        CHAT_COMPLETIONS_ENDPOINT,
        headers=headers,
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()

    if print_response:
        print(json.dumps(data, indent=2))

    message = data.get("choices", [{}])[0].get("message", {})
    audio_block = message.get("audio")
    if not audio_block or "data" not in audio_block:
        raise ValueError("No audio data in response")

    audio_bytes = base64.b64decode(audio_block["data"])
    if output_path is None:
        output_path = Path(__file__).resolve().parent / "speech_to_speech_response.mp3"
    output_path = Path(output_path)
    output_path.write_bytes(audio_bytes)
    return output_path


if __name__ == "__main__":
    path = run_speech_to_speech()
    print(f"Saved audio response to: {path}")
