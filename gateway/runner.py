import subprocess
import json


def run_function(image, payload):

    process = subprocess.run(
        ["docker", "run", "-i", "--rm", image],
        input=json.dumps(payload).encode(),
        stdout=subprocess.PIPE
    )

    return json.loads(process.stdout)