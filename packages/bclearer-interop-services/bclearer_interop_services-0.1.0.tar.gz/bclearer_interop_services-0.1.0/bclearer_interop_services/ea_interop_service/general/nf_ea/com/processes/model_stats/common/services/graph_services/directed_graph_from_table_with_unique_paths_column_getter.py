from networkx import (
    DiGraph,
    empty_graph,
)
from pandas import DataFrame


def get_directed_graph_from_table_with_unique_paths_column(
    table_with_unique_paths_column: DataFrame,
    path_column_name: str,
) -> DiGraph:
    directed_graph = empty_graph(
        create_using=DiGraph
    )

    list_of_unique_paths = (
        table_with_unique_paths_column[
            path_column_name
        ].tolist()
    )

    list_of_edges = []

    # For this to work properly, the path should be directed leaf to root
    for path in list_of_unique_paths:
        for node_1, node_2 in zip(
            path[:-1], path[1:]
        ):
            edge = (node_1, node_2)

            directed_graph.add_edge(
                node_1, node_2
            )

            list_of_edges.append(edge)

    return directed_graph
