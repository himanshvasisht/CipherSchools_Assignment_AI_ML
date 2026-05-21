from collections import defaultdict


def calculate_centrality(
    dependency_graph
):

    scores = defaultdict(int)

    for file, imports in dependency_graph.items():

        scores[file] += len(
            imports
        )

        for imp in imports:
            scores[file] += 1

    return dict(scores)