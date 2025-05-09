import io
import requests
from mcp.server.fastmcp import FastMCP
from PIL import Image as PILImage

mcp = FastMCP("Dog Eye Diagnosis", dependencies=["requests", "pillow"])

@mcp.tool()
def diagnose_dog_eye(image_path: str) -> str:
    """
    Analyzes a dog's eye image from a local path and returns diagnosis probabilities
    for the following 10 conditions:
    'Conjunctivitis', 'Ulcerative keratitis', 'Cataract', 'Non-ulcerative keratitis',
    'Pigmentary keratitis', 'Entropion', 'Blepharitis', 'Eyelid tumor',
    'Epiphora', 'Nuclear sclerosis'
    """
    MAX_SIZE_BYTES = 1 * 1024 * 1024  # 1MB

    img = PILImage.open(image_path).convert("RGB")
    img.thumbnail((1024, 1024))

    buffer = io.BytesIO()
    quality = 90

    while quality >= 10:
        buffer.seek(0)
        buffer.truncate()
        img.save(buffer, format='JPEG', quality=quality)

        if buffer.tell() <= MAX_SIZE_BYTES:
            break

        quality -= 10

    buffer.seek(0)

    response = requests.post(
        "http://13.124.223.37/v1/prediction/binary",
        files={'img_file': ('compressed.jpg', buffer, 'image/jpeg')}
    )

    try:
        return response.json()
    except requests.JSONDecodeError:
        return f"Invalid response from server: {response.text}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
