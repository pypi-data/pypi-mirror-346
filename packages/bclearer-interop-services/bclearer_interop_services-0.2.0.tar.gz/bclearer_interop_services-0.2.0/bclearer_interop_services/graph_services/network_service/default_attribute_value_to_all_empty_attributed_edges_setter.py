from bclearer_interop_services.graph_services.network_service.attribute_to_edge_setter import (
    set_attribute_to_edge,
)
from networkx import DiGraph


def set_default_attribute_value_to_all_empty_attributed_edges(
    graph: DiGraph,
    default_attribute_name: str,
    default_attribute_value: str,
) -> None:
    empty_attributed_edges = [
        (source_node, target_node)
        for source_node, target_node, attribute_dictionary in graph.edges(
            data=True,
        )
        if attribute_dictionary
        == dict()
    ]

    for (
        empty_attributed_edge
    ) in empty_attributed_edges:
        set_attribute_to_edge(
            graph=graph,
            edge=empty_attributed_edge,
            attribute_name=default_attribute_name,
            attribute_value=default_attribute_value,
        )
