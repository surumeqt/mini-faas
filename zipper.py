import base64
import io
import zipfile

def zip_files(event):
    """
    Zips multiple files passed in the event payload.
    Expected event schema:
    {
        "files": [
            {
                "name": "filename.txt",
                "content": "base64encodedcontent..."
            },
            ...
        ]
    }
    Returns:
    {
        "zip_file": "base64encodedzip...",
        "filename": "archive.zip"
    }
    """
    files = event.get("files", [])
    if not files:
        return {"error": "No files provided in payload"}
    
    zip_buffer = io.BytesIO()
    try:
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for file_info in files:
                name = file_info.get("name")
                content_b64 = file_info.get("content")
                if name and content_b64:
                    file_content = base64.b64decode(content_b64)
                    zip_file.writestr(name, file_content)
        
        zip_buffer.seek(0)
        zip_base64 = base64.b64encode(zip_buffer.getvalue()).decode("utf-8")
        
        return {
            "zip_file": zip_base64,
            "filename": "archive.zip"
        }
    except Exception as e:
        return {"error": f"Failed to zip files: {str(e)}"}
