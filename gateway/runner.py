import subprocess
import json

from gateway.database import get_connection


def get_image(name):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT image FROM functions WHERE name=%s",
        (name,)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if not result:
        return None

    return result[0]


def run_function(name, payload):

    image = get_image(name)

    if not image:
        return {
            "error": "function not found"
        }

    process = subprocess.run(
        ["docker", "run", "-i", "--rm", image],
        input=json.dumps(payload).encode(),
        stdout=subprocess.PIPE
    )

    return json.loads(process.stdout)