import ast
import re


def parse_python_functions(file_path):

    with open(file_path, "r") as f:

        source = f.read()

    tree = ast.parse(source)

    functions = []

    for node in tree.body:

        if isinstance(node, ast.FunctionDef):

            functions.append(node.name)

    return functions


def parse_node_functions(file_path):

    with open(file_path, "r") as f:

        source = f.read()

    functions = []

    #
    # function hello() {}
    #

    normal_pattern = (
        r"function\s+"
        r"([a-zA-Z_][a-zA-Z0-9_]*)"
        r"\s*\("
    )

    normal_matches = re.findall(
        normal_pattern,
        source
    )

    functions.extend(normal_matches)

    #
    # const hello = () => {}
    #

    arrow_pattern = (
        r"const\s+"
        r"([a-zA-Z_][a-zA-Z0-9_]*)"
        r"\s*=\s*"
        r"\("
    )

    arrow_matches = re.findall(
        arrow_pattern,
        source
    )

    functions.extend(arrow_matches)

    #
    # REMOVE DUPLICATES
    #

    return list(set(functions))