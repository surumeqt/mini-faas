import subprocess

from gateway.detector import detect_runtime
from gateway.database import get_connection

from gateway.parser import (
    parse_python_functions,
    parse_node_functions
)


TEMPLATES_DIR = "/app/gateway/templates"


def build_function(name, project_path):

    #
    # DETECT RUNTIME
    #

    runtime = detect_runtime(project_path)

    #
    # SELECT TEMPLATE
    #

    if runtime == "python":

        template_path = (
            f"{TEMPLATES_DIR}/python.Dockerfile"
        )

        handler_file = "handler.py"

    elif runtime == "node":

        template_path = (
            f"{TEMPLATES_DIR}/node.Dockerfile"
        )

        handler_file = "index.js"

    else:

        raise Exception(
            "unsupported runtime"
        )

    #
    # COPY DOCKERFILE TEMPLATE
    #

    with open(template_path, "r") as src:

        dockerfile_content = src.read()

    dockerfile_path = (
        f"{project_path}/Dockerfile"
    )

    with open(dockerfile_path, "w") as dst:

        dst.write(dockerfile_content)

    #
    # BUILD IMAGE
    #

    image_name = f"faas_{name}"

    subprocess.run([
        "docker",
        "build",
        "-t",
        image_name,
        project_path
    ], check=True)

    #
    # SAVE FUNCTION METADATA
    #

    function_id = save_function_metadata(
        name=name,
        runtime=runtime,
        image=image_name
    )

    #
    # PARSE FUNCTIONS
    #

    handler_path = (
        f"{project_path}/{handler_file}"
    )

    if runtime == "python":

        parsed_functions = (
            parse_python_functions(
                handler_path
            )
        )

    elif runtime == "node":

        parsed_functions = (
            parse_node_functions(
                handler_path
            )
        )

    else:

        parsed_functions = []

    #
    # SAVE ENTRYPOINTS
    #

    clear_existing_entrypoints(
        function_id
    )

    for function_name in parsed_functions:

        if runtime == "python":

            entrypoint = (
                f"handler.{function_name}"
            )

        elif runtime == "node":

            entrypoint = (
                f"index.{function_name}"
            )

        else:

            continue

        save_function_entrypoint(
            function_id=function_id,
            function_name=function_name,
            entrypoint=entrypoint
        )


def save_function_metadata(
    name,
    runtime,
    image
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO functions (
            name,
            runtime,
            image
        )

        VALUES (%s, %s, %s)

        ON DUPLICATE KEY UPDATE
            runtime=%s,
            image=%s
    """, (
        name,
        runtime,
        image,
        runtime,
        image
    ))

    conn.commit()

    #
    # GET FUNCTION ID
    #

    cursor.execute("""
        SELECT id
        FROM functions
        WHERE name=%s
    """, (name,))

    result = cursor.fetchone()

    function_id = result[0]

    cursor.close()
    conn.close()

    return function_id


def clear_existing_entrypoints(
    function_id
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM function_entrypoints
        WHERE function_id=%s
    """, (
        function_id,
    ))

    conn.commit()

    cursor.close()
    conn.close()


def save_function_entrypoint(
    function_id,
    function_name,
    entrypoint
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO function_entrypoints (
            function_id,
            function_name,
            entrypoint
        )

        VALUES (%s, %s, %s)
    """, (
        function_id,
        function_name,
        entrypoint
    ))

    conn.commit()

    cursor.close()
    conn.close()