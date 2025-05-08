from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.data_columns_to_edge_base_table_adder import (
    add_data_columns_to_edge_base_table,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.edges_base_table_from_multi_edged_directed_graph_getter import (
    get_edges_base_table_from_multi_edged_directed_graph,
)
from networkx import MultiDiGraph
from pandas import DataFrame


def get_full_edges_table(
    multi_edged_directed_graph: MultiDiGraph,
    ea_connectors: DataFrame,
    ea_stereotypes: DataFrame,
    ea_stereotype_usage: DataFrame,
) -> DataFrame:
    edges_base_table = get_edges_base_table_from_multi_edged_directed_graph(
        multi_edged_directed_graph=multi_edged_directed_graph
    )

    full_edges_table = add_data_columns_to_edge_base_table(
        edge_base_table=edges_base_table,
        ea_connectors=ea_connectors,
        ea_stereotypes=ea_stereotypes,
        ea_stereotype_usage=ea_stereotype_usage,
    )

    return full_edges_table
