from flask import Flask, request, jsonify

from gateway.builder import build_function
from gateway.normalizer import normalize_upload
from gateway.runner import run_function

app = Flask(__name__)


@app.route("/deploy", methods=["POST"])
def deploy():

    try:

        #
        # VALIDATION
        #

        if "name" not in request.form:
            return jsonify({
                "error": "missing function name"
            }), 400

        if "file" not in request.files:
            return jsonify({
                "error": "missing function file"
            }), 400

        #
        # REQUEST DATA
        #

        name = request.form["name"]

        file = request.files["file"]

        #
        # NORMALIZE UPLOAD
        #

        project_path = normalize_upload(name, file)

        #
        # BUILD FUNCTION
        #

        build_function(name, project_path)

        return jsonify({
            "status": "deployed",
            "function": name
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


@app.route(
    "/invoke/<deployment>/<function_name>",
    methods=["POST"]
)
def invoke(deployment, function_name):

    try:

        payload = request.json or {}

        result = run_function(
            deployment,
            function_name,
            payload
        )

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

    app.run(
        host="0.0.0.0",
        port=5000
    )