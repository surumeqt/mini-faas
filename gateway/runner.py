import json
import subprocess

from gateway.database import get_connection


def run_function(
    deployment,
    function_name,
    payload
):

    #
    # GET FUNCTION METADATA
    #

    metadata = get_function_metadata(
        deployment,
        function_name
    )

    if metadata is None:

        return {
            "error": "function not found"
        }

    image = metadata["image"]

    runtime = metadata["runtime"]

    entrypoint = metadata["entrypoint"]

    #
    # PYTHON RUNTIME
    #

    if runtime == "python":

        module_name, callable_name = (
            entrypoint.split(".")
        )

        execution_script = f"""
import json
import sys
import importlib

payload = json.loads(
    sys.stdin.read()
)

module = importlib.import_module(
    "{module_name}"
)

target_function = getattr(
    module,
    "{callable_name}"
)

result = target_function(
    payload
)

print(
    json.dumps(result)
)
"""

        process = subprocess.run(

            [
                "docker",
                "run",
                "-i",
                "--rm",
                image,
                "python",
                "-c",
                execution_script
            ],

            input=json.dumps(payload).encode(),

            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    #
    # NODE.JS RUNTIME
    #

    elif runtime == "node":

        module_name, callable_name = (
            entrypoint.split(".")
        )

        execution_script = f"""
const fs = require('fs');

const payload = JSON.parse(
    fs.readFileSync(0, 'utf-8')
);

const mod = require('./{module_name}');

const result = mod['{callable_name}'](
    payload
);

console.log(
    JSON.stringify(result)
);
"""

        process = subprocess.run(

            [
                "docker",
                "run",
                "-i",
                "--rm",
                image,
                "node",
                "-e",
                execution_script
            ],

            input=json.dumps(payload).encode(),

            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    #
    # UNKNOWN RUNTIME
    #

    else:

        return {
            "error": (
                f"unsupported runtime: "
                f"{runtime}"
            )
        }

    #
    # HANDLE EXECUTION ERRORS
    #

    if process.returncode != 0:

        return {
            "error": (
                process.stderr.decode()
            )
        }

    #
    # PARSE RESULT
    #

    try:

        return json.loads(
            process.stdout.decode()
        )

    except Exception:

        return {
            "raw_output": (
                process.stdout.decode()
            )
        }


def get_function_metadata(
    deployment,
    function_name
):

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute("""
        SELECT
            f.image,
            f.runtime,
            fe.entrypoint

        FROM functions f

        JOIN function_entrypoints fe
        ON f.id = fe.function_id

        WHERE
            f.name = %s
        AND
            fe.function_name = %s
    """, (
        deployment,
        function_name
    ))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result