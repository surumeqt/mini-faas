import os


def detect_runtime(project_path):

    files = os.listdir(project_path)

    if "requirements.txt" in files:
        return "python"

    if "package.json" in files:
        return "node"

    raise Exception("unsupported runtime")