from networkx import DiGraph


def get_graph_roots(
    graph: DiGraph,
    in_degree_based: bool,
) -> list:
    if in_degree_based:
        roots = [
            node
            for node, degree in graph.in_degree
            if degree == 0
        ]

        return roots

    roots = [
        node
        for node, degree in graph.out_degree
        if degree == 0
    ]

    return roots
