from pathlib import Path

import requests

from commons.constants import OPENAI_API_KEY, OPENAI_HOST


# https://developers.openai.com/api/docs/guides/speech-to-text

TRANSCRIPTIONS_ENDPOINT = f"{OPENAI_HOST}/v1/audio/transcriptions"


def transcribe_audio(
    audio_path: Path,
    model: str = "whisper-1",
    print_response: bool = True,
) -> str:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set")

    with open(audio_path, "rb") as f:
        files = {"file": (audio_path.name, f, "audio/mpeg")}
        data = {"model": model}
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        response = requests.post(
            TRANSCRIPTIONS_ENDPOINT,
            headers=headers,
            files=files,
            data=data,
            timeout=60,
        )

    response.raise_for_status()
    result = response.json()
    text = result.get("text", "")
    if print_response:
        print(f"[{model}] {text}")
    return text


def run_speech_to_text(
    audio_path: Path | None = None,
    print_response: bool = True,
) -> dict[str, str]:
    if audio_path is None:
        audio_path = Path(__file__).resolve().parent / "audio_sample.mp3"
    if not audio_path.is_file():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    results = {}
    for model in ("whisper-1", "gpt-4o-transcribe"):
        results[model] = transcribe_audio(
            audio_path, model=model, print_response=print_response
        )
    return results


if __name__ == "__main__":
    run_speech_to_text()