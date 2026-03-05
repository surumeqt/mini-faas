import os
import subprocess
import json

REGISTRY_FILE = "registry.json"


def build_function(name, file_path):

    build_dir = f"build/{name}"
    os.makedirs(build_dir, exist_ok=True)

    handler_dst = f"{build_dir}/handler.py"

    with open(file_path, "rb") as src, open(handler_dst, "wb") as dst:
        dst.write(src.read())

    dockerfile = f"""
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

    update_registry(name, image_name)


def update_registry(name, image):

    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE) as f:
            registry = json.load(f)
    else:
        registry = {}

    registry[name] = image

    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)