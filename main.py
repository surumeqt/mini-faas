from flask import Flask, request, jsonify
import os

from gateway.builder import build_function
from gateway.runner import run_function

app = Flask(__name__)


FUNCTIONS_DIR = "/app/functions"


@app.route("/deploy", methods=["POST"])
def deploy():

    try:

        if "name" not in request.form:
            return jsonify({
                "error": "missing function name"
            }), 400

        if "file" not in request.files:
            return jsonify({
                "error": "missing function file"
            }), 400

        name = request.form["name"]

        file = request.files["file"]

        os.makedirs(FUNCTIONS_DIR, exist_ok=True)

        path = f"{FUNCTIONS_DIR}/{name}.py"

        file.save(path)

        build_function(name, path)

        return jsonify({
            "status": "deployed",
            "function": name
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/invoke/<name>", methods=["POST"])
def invoke(name):

    try:

        payload = request.json or {}

        result = run_function(name, payload)

        if "error" in result:
            return jsonify(result), 404

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/")
def health():

    return jsonify({
        "status": "running"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)