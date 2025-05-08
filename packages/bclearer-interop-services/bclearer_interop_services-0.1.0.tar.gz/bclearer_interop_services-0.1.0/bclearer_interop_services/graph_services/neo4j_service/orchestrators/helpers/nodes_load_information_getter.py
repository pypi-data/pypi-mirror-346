from neo4j_service.constants.GraphDataObjectTypes import (
    GraphObjectTypes,
)
from neo4j_service.orchestrators.helpers.read_cypher_queries import (
    read_cypher_query_from_file,
)


def get_graph_object_load_information(
    csv_file_path,
    query_file_path,
    graph_object_type: GraphObjectTypes,
):
    query = read_cypher_query_from_file(
        query_file_path,
    )

    object_info = [
        {
            "csv_file": csv_file_path,
            "query": query,
        },
    ]

    if (
        graph_object_type
        == GraphObjectTypes.NODES
    ):
        nodes_info = {
            "nodes_info": object_info,
        }
        return nodes_info

    if (
        graph_object_type
        == GraphObjectTypes.EDGES
    ):
        edges_info = {
            "edges_info": object_info,
        }
        return edges_info
