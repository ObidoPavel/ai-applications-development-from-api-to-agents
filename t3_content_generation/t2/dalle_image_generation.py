from commons.constants import OPENAI_HOST
from t3_content_generation._openai_client import OpenAIClientT3


class Size:
    """
    The size of the generated image.
    """
    square: str = '1024x1024'
    height_rectangle: str = '1024x1792'
    width_rectangle: str = '1792x1024'


class Style:
    """
    The style of the generated image. Must be one of vivid or natural.
     - Vivid causes the model to lean towards generating hyper-real and dramatic images.
     - Natural causes the model to produce more natural, less hyper-real looking images.
    """
    natural: str = "natural"
    vivid: str = "vivid"


class Quality:
    """
    The quality of the image that will be generated.
     - ‘hd’ creates images with finer details and greater consistency across the image.
    """
    standard: str = "standard"
    hd: str = "hd"


# https://developers.openai.com/api/reference/resources/images/methods/generate
# Request:
# curl https://api.openai.com/v1/images/generations \
#   -H "Content-Type: application/json" \
#   -H "Authorization: Bearer $OPENAI_API_KEY" \
#   -d '{
#     "model": "dall-e-3",
#     "prompt": "smiling catdog",
#     "size": "1024x1024",
#     "style": "natural",
#     "quality": "standard"
#   }'

from commons.constants import OPENAI_HOST
from t3_content_generation._openai_client import OpenAIClientT3


class Size:
    """
    The size of the generated image.
    """
    square: str = '1024x1024'
    height_rectangle: str = '1024x1792'
    width_rectangle: str = '1792x1024'


class Style:
    """
    The style of the generated image. Must be one of vivid or natural.
     - Vivid causes the model to lean towards generating hyper-real and dramatic images.
     - Natural causes the model to produce more natural, less hyper-real looking images.
    """
    natural: str = "natural"
    vivid: str = "vivid"


class Quality:
    """
    The quality of the image that will be generated.
     - 'hd' creates images with finer details and greater consistency across the image.
    """
    standard: str = "standard"
    hd: str = "hd"


# https://developers.openai.com/api/reference/resources/images/methods/generate
# Request:
# curl https://api.openai.com/v1/images/generations \
#   -H "Content-Type: application/json" \
#   -H "Authorization: Bearer $OPENAI_API_KEY" \
#   -d '{
#     "model": "dall-e-3",
#     "prompt": "smiling catdog",
#     "size": "1024x1024",
#     "style": "natural",
#     "quality": "standard"
#   }'


def run_dalle_image_generation(
    prompt: str = "Smiling catdog",
    size: str = Size.square,
    style: str = Style.natural,
    quality: str = Quality.standard,
    print_request: bool = True,
    print_response: bool = True,
) -> dict:
    client = OpenAIClientT3(f"{OPENAI_HOST}/v1/images/generations")
    return client.call(
        print_request=print_request,
        print_response=print_response,
        model="dall-e-3",
        prompt=prompt,
        size=size,
        style=style,
        quality=quality,
    )


if __name__ == "__main__":
    result = run_dalle_image_generation()
    if result.get("data"):
        url = result["data"][0].get("url")
        if url:
            print(f"Generated image URL: {url}")