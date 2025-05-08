def get_list_of_roots_from_multi_edged_directed_graph(
    multi_edged_directed_graph,
) -> list:
    roots = []

    for (
        node,
        depth,
    ) in (
        multi_edged_directed_graph.out_degree()
    ):
        if depth == 0:
            roots.append(node)

    return roots
