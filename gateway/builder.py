import os
import subprocess

from gateway.database import get_connection


def build_function(name, file_path):

    build_dir = f"build/{name}"

    os.makedirs(build_dir, exist_ok=True)

    handler_dst = f"{build_dir}/handler.py"

    with open(file_path, "rb") as src, open(handler_dst, "wb") as dst:
        dst.write(src.read())

    dockerfile = """
FROM python:3.11-slim

WORKDIR /app

COPY handler.py .

CMD ["python","-c","import handler,sys,json;print(json.dumps(handler.handler(json.loads(sys.stdin.read()))))"]
"""

    with open(f"{build_dir}/Dockerfile", "w") as f:
        f.write(dockerfile)

    image_name = f"faas_{name}"

    subprocess.run([
        "docker",
        "build",
        "-t",
        image_name,
        build_dir
    ])

    save_metadata(name, image_name)


def save_metadata(name, image):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO functions (name, image)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE image=%s
    """, (name, image, image))

    conn.commit()

    cursor.close()
    conn.close()