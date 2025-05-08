from bclearer_interop_services.b_dictionary_service.table_as_dictionary_service.table_as_dictionary_to_dataframe_converter import (
    convert_table_as_dictionary_to_dataframe,
)
from networkx import to_pandas_edgelist
from pandas import DataFrame


def convert_graph_to_nodes_and_edges_tables(
    graph,
    node_id_column_name: str,
) -> tuple:
    nodes_table = extract_nodes_table_from_graph(
        graph=graph,
        node_id_column_name_to_be=node_id_column_name,
    )

    edges_table = (
        convert_graph_to_edges_table(
            graph=graph,
        )
    )

    return nodes_table, edges_table


def convert_graph_to_edges_table(
    graph,
) -> DataFrame:
    edges_table = to_pandas_edgelist(
        graph,
    )

    return edges_table


def extract_nodes_table_from_graph(
    graph,
    node_id_column_name_to_be: str,
) -> DataFrame:
    graph_nodes_dictionary = extract_nodes_table_as_dictionary_of_rows_from_graph(
        graph=graph,
        node_id_column_name_to_be=node_id_column_name_to_be,
    )

    graph_nodes_table = convert_table_as_dictionary_to_dataframe(
        table_as_dictionary=graph_nodes_dictionary,
    )

    return graph_nodes_table


def extract_nodes_table_as_dictionary_of_rows_from_graph(
    graph,
    node_id_column_name_to_be: str,
) -> dict:
    graph_nodes_dictionary_raw = dict(
        graph.nodes(data=True),
    )

    graph_nodes_dictionary = dict()

    for (
        graph_nodes_dictionary_key,
        graph_nodes_dictionary_row,
    ) in (
        graph_nodes_dictionary_raw.items()
    ):
        __add_node_id_column_to_nodes_dictionary(
            node_id_column_name=node_id_column_name_to_be,
            graph_nodes_dictionary_key=graph_nodes_dictionary_key,
            graph_nodes_dictionary_row=graph_nodes_dictionary_row,
            output_graph_nodes_dictionary=graph_nodes_dictionary,
        )

    return graph_nodes_dictionary


def __add_node_id_column_to_nodes_dictionary(
    node_id_column_name: str,
    graph_nodes_dictionary_key: str,
    graph_nodes_dictionary_row: dict,
    output_graph_nodes_dictionary: dict,
) -> None:
    new_graph_nodes_dictionary_row = {
        node_id_column_name: graph_nodes_dictionary_key,
    }

    new_graph_nodes_dictionary_row.update(
        graph_nodes_dictionary_row,
    )

    output_graph_nodes_dictionary[
        graph_nodes_dictionary_key
    ] = new_graph_nodes_dictionary_row
