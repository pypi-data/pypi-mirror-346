from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from networkx import (
    MultiDiGraph,
    from_pandas_edgelist,
)
from pandas import DataFrame


def build_multi_edged_directed_graph_from_input_edges_table(
    input_edges_table: DataFrame,
    edge_source_column_name: str,
    edge_target_column_name: str,
    edge_type_column_name: str,
    ea_classifiers: DataFrame,
    is_full_dependencies_edges_table: bool,
) -> MultiDiGraph:
    multi_edge_directed_graph = from_pandas_edgelist(
        input_edges_table,
        source=edge_source_column_name,
        target=edge_target_column_name,
        edge_attr=edge_type_column_name,
        create_using=MultiDiGraph(),
        edge_key=NfColumnTypes.NF_UUIDS.column_name,
    )

    if (
        is_full_dependencies_edges_table
        and input_edges_table.empty
    ):
        return multi_edge_directed_graph

    list_of_classifiers = ea_classifiers[
        NfColumnTypes.NF_UUIDS.column_name
    ].tolist()

    multi_edge_directed_graph.add_nodes_from(
        list_of_classifiers
    )

    return multi_edge_directed_graph
