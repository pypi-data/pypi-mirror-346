from bclearer_interop_services.graph_services.network_service.graph_transitive_reductor import (
    transitively_reduce_graph,
)
from networkx import (
    DiGraph,
    difference,
    is_isomorphic,
)
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def is_graph_minimal(
    directed_graph: DiGraph,
    graph_name: str,
) -> bool:
    transitively_reduced_graph = transitively_reduce_graph(
        directed_graph=directed_graph,
        graph_name=graph_name,
    )

    graph_and_reduction_are_isomorphic = is_isomorphic(
        G1=directed_graph,
        G2=transitively_reduced_graph,
    )

    extra_edges = list(
        difference(
            G=directed_graph,
            H=transitively_reduced_graph,
        ).edges(),
    )

    if (
        not graph_and_reduction_are_isomorphic
    ):
        __try_logging_message(
            message="WARNING: GRAPH '"
            + graph_name
            + "' IS NOT THE MINIMAL POSSIBLE GRAPH\n"
            + "Extra edges: "
            + str(extra_edges),
        )

    else:
        __try_logging_message(
            message="INFORMATION: Graph '"
            + graph_name
            + "' is the (transitive) minimal possible graph_service",
        )

    return graph_and_reduction_are_isomorphic


# TODO: nf_common - May be this exception could be added into nf_common?? Do we want that??
def __try_logging_message(
    message: str,
) -> None:
    try:
        log_message(message=message)

    except TypeError:
        pass


# ONLY FOR TESTING ##################################################
# if __name__ == '__main__':
#     # Example taken from: https://en.wikipedia.org/wiki/Transitive_reduction
#     graph_1 = \
#         DiGraph(
#             [(1, 2), (1, 3), (2, 4), (1, 4), (3, 4), (4, 5), (1, 5), (3, 5)]
#         )
#
#     # graph_1_transitive_reduction = \
#     #     transitively_reduce_graph(
#     #         directed_graph=graph_1,
#     #         graph_name='graph_1_transitive_reduction')
#
#     graphs_are_isomorphic = \
#         is_graph_minimal(
#             graph_service=graph_1,
#             graph_name='graph_1')
#######################################################################
