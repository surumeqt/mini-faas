import os
import shutil

from gateway.extractor import extract_zip


FUNCTIONS_DIR = "/app/functions"
BUILD_DIR = "/app/build"


def normalize_upload(name, uploaded_file):

    filename = uploaded_file.filename

    #
    # PERSISTENT STORAGE
    #

    function_source_dir = f"{FUNCTIONS_DIR}/{name}"

    #
    # TEMP BUILD STORAGE
    #

    function_build_dir = f"{BUILD_DIR}/{name}"

    #
    # CLEAN OLD DIRECTORIES
    #

    if os.path.exists(function_source_dir):
        shutil.rmtree(function_source_dir)

    if os.path.exists(function_build_dir):
        shutil.rmtree(function_build_dir)

    os.makedirs(function_source_dir, exist_ok=True)
    os.makedirs(function_build_dir, exist_ok=True)

    #
    # ZIP PROJECT
    #

    if filename.endswith(".zip"):

        zip_source_path = (
            f"{function_source_dir}/project.zip"
        )

        uploaded_file.save(zip_source_path)

        extract_zip(
            zip_source_path,
            function_source_dir
        )

        os.remove(zip_source_path)

    #
    # PYTHON FILE
    #

    elif filename.endswith(".py"):

        uploaded_file.save(
            f"{function_source_dir}/handler.py"
        )

        requirements_path = (
            f"{function_source_dir}/requirements.txt"
        )

        if not os.path.exists(requirements_path):

            with open(requirements_path, "w") as f:
                f.write("")

    #
    # NODE FILE
    #

    elif filename.endswith(".js"):

        uploaded_file.save(
            f"{function_source_dir}/index.js"
        )

        package_json = (
            f"{function_source_dir}/package.json"
        )

        if not os.path.exists(package_json):

            with open(package_json, "w") as f:

                f.write("""
{
  "name": "faas-function",
  "version": "1.0.0"
}
""")

    else:
        raise Exception("unsupported file type")

    #
    # COPY SOURCE → BUILD
    #

    shutil.copytree(
        function_source_dir,
        function_build_dir,
        dirs_exist_ok=True
    )

    return function_build_dir