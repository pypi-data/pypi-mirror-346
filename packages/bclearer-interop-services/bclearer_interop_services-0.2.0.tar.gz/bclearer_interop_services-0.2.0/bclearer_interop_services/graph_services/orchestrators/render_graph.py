from bclearer_interop_services.graph_services.network_service.object_model.Nodes import (
    Node,
)
from graphviz import Digraph


def render_graph():
    """Render in a graph_service output object pdf"""
    directed_graph = Digraph(
        comment="Directed Graph",
    )

    for (
        key,
        value,
    ) in Node._registry.items():
        directed_graph.node(
            str(value.node_uuid),
        )

        for (
            connected_node
        ) in value.connected_nodes:
            directed_graph.edge(
                str(value.node_uuid),
                str(
                    connected_node.node_uuid,
                ),
            )

    print(directed_graph)

    directed_graph.view()
