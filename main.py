from flask import Flask, request, jsonify

from gateway.builder import build_function
from gateway.normalizer import normalize_upload
from gateway.runner import run_function

app = Flask(__name__, static_folder="sangoku", static_url_path="")


@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response.headers["Access-Control-Allow-Private-Network"] = "true"
        return response


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    return response



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

        if request.files or request.form:
            payload = {}
            for key in request.form:
                payload[key] = request.form[key]
            
            files_list = []
            for file_key in request.files:
                for file in request.files.getlist(file_key):
                    if file.filename:
                        import base64
                        file_data = file.read()
                        encoded_data = base64.b64encode(file_data).decode("utf-8")
                        files_list.append({
                            "name": file.filename,
                            "content": encoded_data
                        })
            payload["files"] = files_list
        else:
            payload = request.get_json(force=True, silent=True) or {}

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