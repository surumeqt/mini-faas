import ast


def parse_python_functions(file_path):

    with open(file_path, "r") as f:

        source = f.read()

    tree = ast.parse(source)

    functions = []

    for node in tree.body:

        if isinstance(node, ast.FunctionDef):

            functions.append(node.name)

    return functions