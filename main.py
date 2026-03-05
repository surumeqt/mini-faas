from flask import Flask, request, jsonify
import json
import os

from gateway.builder import build_function
from gateway.runner import run_function

app = Flask(__name__)

REGISTRY_FILE = "registry.json"

def load_registry():
    if not os.path.exists(REGISTRY_FILE):
        return {}
    with open(REGISTRY_FILE) as f:
        return json.load(f)


@app.route("/deploy", methods=["POST"])
def deploy():

    name = request.form["name"]
    file = request.files["file"]

    path = f"functions/{name}.py"
    os.makedirs("functions", exist_ok=True)

    file.save(path)

    build_function(name, path)

    return {"status": "deployed", "function": name}


@app.route("/invoke/<name>", methods=["POST"])
def invoke(name):

    registry = load_registry()

    if name not in registry:
        return {"error": "function not found"}, 404

    payload = request.json or {}

    result = run_function(registry[name], payload)

    return jsonify(result)


if __name__ == "__main__":
    app.run(port=5000)