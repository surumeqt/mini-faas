from PIL import Image
import base64
import io


def change_background(event):

    input_path = "cat.png"

    image = Image.open(input_path)

    image = image.convert("RGBA")

    new_background = Image.new(
        "RGBA",
        image.size,
        (255, 0, 0, 255)
    )

    new_background.paste(
        image,
        (0, 0),
        image
    )

    output = io.BytesIO()

    new_background.save(
        output,
        format="PNG"
    )

    encoded = base64.b64encode(
        output.getvalue()
    ).decode()

    return {
        "image": encoded
    }