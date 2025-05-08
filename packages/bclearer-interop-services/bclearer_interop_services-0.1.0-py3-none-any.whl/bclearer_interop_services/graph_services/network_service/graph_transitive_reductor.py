import sys

from bclearer_interop_services.graph_services.network_service.directed_graph_cycles_checker import (
    check_directed_graph_cycles,
)
from networkx import (
    DiGraph,
    transitive_reduction,
)


def transitively_reduce_graph(
    directed_graph: DiGraph,
    graph_name: str,
) -> DiGraph:
    directed_graph_cycles_list = check_directed_graph_cycles(
        directed_graph=directed_graph,
        graph_name=graph_name,
    )

    # TODO: Handle the below situation with a bespoke error
    if directed_graph_cycles_list:
        sys.exit(
            "ERROR: CYCLES FOUND IN DIRECTED GRAPH: "
            + graph_name
            + "\n"
            + str(
                directed_graph_cycles_list,
            ),
        )

    transitively_reduced_directed_graph = transitive_reduction(
        G=directed_graph,
    )

    transitively_reduced_directed_graph.add_nodes_from(
        directed_graph.nodes(data=True),
    )

    transitively_reduced_directed_graph.add_edges_from(
        (
            source,
            target,
            directed_graph.edges[
                source,
                target,
            ],
        )
        for source, target in transitively_reduced_directed_graph.edges
    )

    return transitively_reduced_directed_graph
