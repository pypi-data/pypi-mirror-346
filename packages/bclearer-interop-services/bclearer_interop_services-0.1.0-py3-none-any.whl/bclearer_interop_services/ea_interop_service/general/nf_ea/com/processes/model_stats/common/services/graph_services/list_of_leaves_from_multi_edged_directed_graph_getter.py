def get_list_of_leaves_from_multi_edged_directed_graph(
    multi_edged_directed_graph,
) -> list:
    leaves = []

    for (
        node,
        depth,
    ) in (
        multi_edged_directed_graph.in_degree()
    ):
        if depth == 0:
            leaves.append(node)

    return leaves
