from datetime import datetime
from pathlib import Path

import requests

from commons.constants import OPENAI_API_KEY, OPENAI_HOST


class Voice:
    alloy: str = 'alloy'
    ash: str = 'ash'
    ballad: str = 'ballad'
    coral: str = 'coral'
    echo: str = 'echo'
    fable: str = 'fable'
    nova: str = 'nova'
    onyx: str = 'onyx'
    sage: str = 'sage'
    shimmer: str = 'shimmer'


# https://developers.openai.com/api/docs/guides/text-to-speech
# Request:
# curl https://api.openai.com/v1/audio/speech \
#   -H "Authorization: Bearer $OPENAI_API_KEY" \
#   -H "Content-Type: application/json" \
#   -d '{
#     "model": "gpt-4o-mini-tts",
#     "input": "Why can't we say that black is white?",
#     "voice": "coral",
#     "instructions": "Speak in a cheerful and positive tone."
#   }' \
# Response:
#   bytes with audio


SPEECH_ENDPOINT = f"{OPENAI_HOST}/v1/audio/speech"


def run_text_to_speech(
    text: str = "Why can't we say that black is white?",
    voice: str = Voice.coral,
    instructions: str = "Speak in a cheerful and positive tone.",
    output_path: Path | None = None,
) -> Path:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set")

    payload = {
        "model": "gpt-4o-mini-tts",
        "input": text,
        "voice": voice,
        "instructions": instructions,
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        SPEECH_ENDPOINT,
        headers=headers,
        json=payload,
        timeout=60,
    )
    response.raise_for_status()

    if output_path is None:
        output_dir = Path(__file__).resolve().parent
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"speech_{timestamp}.mp3"
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(response.content)
    return output_path


if __name__ == "__main__":
    path = run_text_to_speech()
    print(f"Saved speech to: {path}")
