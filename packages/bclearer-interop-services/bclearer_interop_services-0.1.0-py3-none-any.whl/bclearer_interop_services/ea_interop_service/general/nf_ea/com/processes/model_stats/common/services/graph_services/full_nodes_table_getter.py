from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.data_columns_to_nodes_base_table_adder import (
    add_data_columns_to_nodes_base_table,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.nodes_table_from_multi_edged_directed_graph_getter import (
    get_nodes_base_table_from_multi_edged_directed_graph,
)
from networkx import MultiDiGraph
from pandas import DataFrame


def get_full_nodes_table(
    multi_edged_directed_graph: MultiDiGraph,
    ea_classifiers: DataFrame,
    ea_packages: DataFrame,
    ea_stereotypes: DataFrame,
    ea_stereotype_usage: DataFrame,
) -> DataFrame:
    nodes_base_table = get_nodes_base_table_from_multi_edged_directed_graph(
        multi_edged_directed_graph=multi_edged_directed_graph
    )

    full_nodes_table = add_data_columns_to_nodes_base_table(
        nodes_base_table=nodes_base_table,
        ea_classifiers=ea_classifiers,
        ea_packages=ea_packages,
        ea_stereotypes=ea_stereotypes,
        ea_stereotype_usage=ea_stereotype_usage,
    )

    return full_nodes_table
