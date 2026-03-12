import base64
from datetime import datetime

from commons.constants import OPENAI_HOST
from t3_content_generation._openai_client import OpenAIClientT3


# https://developers.openai.com/api/reference/resources/images/methods/generate
# ---
# Request:
# curl -X POST "https://api.openai.com/v1/images/generations" \
#     -H "Authorization: Bearer $OPENAI_API_KEY" \
#     -H "Content-type: application/json" \
#     -d '{
#         "model": "gpt-image-1",
#         "prompt": "smiling catdog."
#     }'
# Response:
# {
#   "created": 1699900000,
#   "data": [
#     {
#       "b64_json": Qt0n6ArYAEABGOhEoYgVAJFdt8jM79uW2DO...,
#     }
#   ]
# }

import base64
from datetime import datetime
from pathlib import Path

from commons.constants import OPENAI_HOST
from t3_content_generation._openai_client import OpenAIClientT3


# https://developers.openai.com/api/reference/resources/images/methods/generate
# ---
# Request:
# curl -X POST "https://api.openai.com/v1/images/generations" \
#     -H "Authorization: Bearer $OPENAI_API_KEY" \
#     -H "Content-type: application/json" \
#     -d '{
#         "model": "gpt-image-1",
#         "prompt": "smiling catdog."
#     }'
# Response:
# {
#   "created": 1699900000,
#   "data": [
#     {
#       "b64_json": Qt0n6ArYAEABGOhEoYgVAJFdt8jM79uW2DO...,
#     }
#   ]
# }


def run_gpt_image_generation(
    prompt: str = "Smiling catdog",
    output_dir: Path | None = None,
    print_request: bool = True,
    print_response: bool = True,
) -> Path:
    client = OpenAIClientT3(f"{OPENAI_HOST}/v1/images/generations")
    result = client.call(
        print_request=print_request,
        print_response=print_response,
        model="gpt-image-1",
        prompt=prompt,
    )
    if not result.get("data") or "b64_json" not in result["data"][0]:
        raise ValueError("No base64 image in response")

    b64_data = result["data"][0]["b64_json"]
    image_bytes = base64.b64decode(b64_data)

    if output_dir is None:
        output_dir = Path(__file__).resolve().parent
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"gpt_image_{timestamp}.png"
    output_path.write_bytes(image_bytes)
    return output_path


if __name__ == "__main__":
    path = run_gpt_image_generation()
    print(f"Saved image to: {path}")
