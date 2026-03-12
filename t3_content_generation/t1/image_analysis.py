import base64
from pathlib import Path

from commons.constants import OPENAI_HOST
from t3_content_generation._openai_client import OpenAIClientT3


# https://developers.openai.com/api/docs/guides/images-vision?format=url&lang=curl
# https://developers.openai.com/api/docs/guides/images-vision?format=base64-encoded

REMOTE_IMAGE_URL = "https://a-z-animals.com/media/2019/11/Elephant-male-1024x535.jpg"


def encode_image(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def run_image_analysis(
    print_request: bool = True, print_response: bool = True
) -> dict:
    logo_path = Path(__file__).resolve().parent / "logo.png"
    if not logo_path.is_file():
        raise FileNotFoundError(f"Local image not found: {logo_path}")

    base64_logo = encode_image(logo_path)
    content = [
        {
            "type": "image_url",
            "image_url": {"url": REMOTE_IMAGE_URL},
        },
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_logo}",
            },
        },
        {"type": "text", "text": "Generate a poem based on these images."},
    ]
    client = OpenAIClientT3(f"{OPENAI_HOST}/v1/chat/completions")
    return client.call(
        print_request=print_request,
        print_response=print_response,
        model="gpt-4o",
        messages=[{"role": "user", "content": content}],
    )


if __name__ == "__main__":
    run_image_analysis()
