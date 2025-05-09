import io
import requests
from mcp.server.fastmcp import FastMCP
from PIL import Image as PILImage

mcp = FastMCP("Dog Eye Diagnosis", dependencies=["requests", "pillow"])

@mcp.tool()
def puppy_eye_diagnosis(image_path: str) -> str:
    img = PILImage.open(image_path).convert("RGB")
    img.thumbnail((1024, 1024))

    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=90)
    buffer.seek(0)

    response = requests.post(
        "http://13.124.223.37/v1/prediction/binary",
        files={'img_file': ('compressed.jpg', buffer, 'image/jpeg')}
    )

    try:
        return response.json()
    except ValueError:
        return f"Invalid response from server: {response.text}"

def serve():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    serve()
