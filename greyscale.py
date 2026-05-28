import base64
import io
from PIL import Image

def greyscale(event):
    """
    Converts the first uploaded image in the event payload to greyscale.
    Expected event schema:
    {
        "files": [
            {
                "name": "filename.jpg",
                "content": "base64encodedcontent..."
            },
            ...
        ]
    }
    Returns:
    {
        "image": "base64encodedgreyscaleimage..."
    }
    """
    files = event.get("files", [])
    if not files:
        return {"error": "No files provided in payload"}
    
    file_info = files[0]
    content_b64 = file_info.get("content")
    if not content_b64:
        return {"error": "No content found for the file"}
        
    try:
        # Decode the image data
        image_data = base64.b64decode(content_b64)
        input_image = Image.open(io.BytesIO(image_data))
        
        # Convert to greyscale
        greyscale_image = input_image.convert("L")
        
        # Save converted image to buffer
        output_buffer = io.BytesIO()
        img_format = input_image.format if input_image.format else "PNG"
        greyscale_image.save(output_buffer, format=img_format)
        output_buffer.seek(0)
        
        # Encode back to base64
        output_b64 = base64.b64encode(output_buffer.getvalue()).decode("utf-8")
        
        return {
            "image": output_b64
        }
    except Exception as e:
        return {"error": f"Failed to convert image: {str(e)}"}
