from collections import defaultdict


def build_dependency_graph(
    files,
    parsed_results
):

    graph = defaultdict(list)

    for f, parsed in zip(
        files,
        parsed_results
    ):

        path = f["path"]

        imports = parsed.get(
            "imports",
            []
        )

        for imp in imports:

            graph[path].append(
                imp
            )

    return dict(graph)