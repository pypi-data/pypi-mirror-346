from networkx import (
    MultiDiGraph,
    all_simple_paths,
    is_empty,
)


def get_list_of_all_simple_paths_from_graph(
    graph: MultiDiGraph,
    roots: list,
    leaves: list,
) -> list:
    if is_empty(graph):
        all_paths = []

        return all_paths

    else:
        all_paths = []

        # for root_node in roots:
        # paths = \
        #     networkx.all_simple_paths(
        #         graph,
        #         root_node,
        #         leaves)

        #  A normal path always goes from root to all leaves.
        #  But our graph is a directed graph where the leaves are pointing up to the roots
        #  If we did it the normal way there would be no possible routes available.
        #  So we inverted it and calculated all the paths from the leaves to the roots.
        #  If is necessary to change it back, the original code is commented above
        for leaf_node in leaves:
            paths = all_simple_paths(
                graph, leaf_node, roots
            )

            all_paths.extend(paths)

        return all_paths
