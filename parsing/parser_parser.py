import ast


def parse_python_file(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)

    result = {
        "imports": set(),
        "classes": [],
        "functions": []
    }

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):
            for alias in node.names:
                result["imports"].add(alias.name)

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                result["imports"].add(node.module)

        elif isinstance(node, ast.ClassDef):

            class_source = ast.get_source_segment(source, node)

            result["classes"].append({
                "name": node.name,
                "source": class_source
            })

        elif isinstance(node, ast.FunctionDef):

            func_source = ast.get_source_segment(source, node)

            result["functions"].append({
                "name": node.name,
                "source": func_source
            })

    return {
        "imports": list(result["imports"]),
        "classes": result["classes"],
        "functions": result["functions"]
    }