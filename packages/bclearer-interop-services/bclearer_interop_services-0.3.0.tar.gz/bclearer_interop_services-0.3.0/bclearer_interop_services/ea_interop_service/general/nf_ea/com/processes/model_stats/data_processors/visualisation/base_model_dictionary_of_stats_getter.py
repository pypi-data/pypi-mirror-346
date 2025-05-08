from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.constants import (
    CONNECTOR_BY_TYPE_TABLE_NAME,
    EDGES_TABLE_NAME,
    LEAVES_COLUMN_NAME,
    NODES_COLUMN_NAME,
    OBJECTS_BY_TYPE_TABLE_NAME,
    PATHS_COLUMN_NAME,
    ROOTS_COLUMN_NAME,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.connectors_by_type_summary_table_getter import (
    get_connectors_by_type_summary_table,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.full_edges_table_getter import (
    get_full_edges_table,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.full_nodes_table_getter import (
    get_full_nodes_table,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.list_of_all_simple_paths_from_graph_getter import (
    get_list_of_all_simple_paths_from_graph,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.list_of_leaves_from_multi_edged_directed_graph_getter import (
    get_list_of_leaves_from_multi_edged_directed_graph,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.list_of_roots_from_directed_graph_getter import (
    get_list_of_roots_from_multi_edged_directed_graph,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.objects_by_type_summary_table_getter import (
    get_objects_by_type_summary_table,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.paths_and_path_depths_table_from_path_list_getter import (
    get_paths_and_path_depths_table_from_path_list,
)
from networkx import MultiDiGraph
from pandas import DataFrame


def get_base_model_dictionary_of_stats(
    base_model_multi_edged_directed_graph: MultiDiGraph,
    ea_classifiers: DataFrame,
    ea_packages: DataFrame,
    ea_connectors: DataFrame,
    ea_stereotypes: DataFrame,
    ea_stereotype_usage: DataFrame,
    output_summary_table_prefix: str,
) -> dict:
    base_model_list_of_leaves = get_list_of_leaves_from_multi_edged_directed_graph(
        multi_edged_directed_graph=base_model_multi_edged_directed_graph
    )

    base_model_list_of_roots = get_list_of_roots_from_multi_edged_directed_graph(
        multi_edged_directed_graph=base_model_multi_edged_directed_graph
    )

    base_model_list_of_all_simple_paths = get_list_of_all_simple_paths_from_graph(
        graph=base_model_multi_edged_directed_graph,
        roots=base_model_list_of_roots,
        leaves=base_model_list_of_leaves,
    )

    base_model_nodes_table = get_full_nodes_table(
        multi_edged_directed_graph=base_model_multi_edged_directed_graph,
        ea_classifiers=ea_classifiers,
        ea_packages=ea_packages,
        ea_stereotypes=ea_stereotypes,
        ea_stereotype_usage=ea_stereotype_usage,
    )

    base_model_edges_table = get_full_edges_table(
        multi_edged_directed_graph=base_model_multi_edged_directed_graph,
        ea_connectors=ea_connectors,
        ea_stereotypes=ea_stereotypes,
        ea_stereotype_usage=ea_stereotype_usage,
    )

    base_model_path_analysis_master_table = get_paths_and_path_depths_table_from_path_list(
        path_list=base_model_list_of_all_simple_paths
    )

    base_model_objects_by_type_summary_table = get_objects_by_type_summary_table(
        ea_classifiers=ea_classifiers
    )

    base_model_connectors_by_type_summary_table = get_connectors_by_type_summary_table(
        edges_table=base_model_edges_table
    )

    base_model_dictionary_of_stats = __get_base_model_dictionary_of_stats_from_stat_tables(
        nodes=base_model_nodes_table,
        edges=base_model_edges_table,
        leaves=base_model_list_of_leaves,
        roots=base_model_list_of_roots,
        paths=base_model_path_analysis_master_table,
        objects_by_type=base_model_objects_by_type_summary_table,
        connectors_by_type=base_model_connectors_by_type_summary_table,
        output_summary_table_prefix=output_summary_table_prefix,
    )

    return (
        base_model_dictionary_of_stats
    )


def __get_base_model_dictionary_of_stats_from_stat_tables(
    nodes: DataFrame,
    edges: DataFrame,
    leaves: list,
    roots: list,
    paths: DataFrame,
    objects_by_type: DataFrame,
    connectors_by_type: DataFrame,
    output_summary_table_prefix: str,
) -> dict:
    leaves_dataframe = DataFrame(
        data=leaves,
        columns=[
            output_summary_table_prefix
            + "_"
            + LEAVES_COLUMN_NAME
        ],
    )

    roots_dataframe = DataFrame(
        data=roots,
        columns=[
            output_summary_table_prefix
            + "_"
            + ROOTS_COLUMN_NAME
        ],
    )

    general_data_visualisation_dictionary = {
        output_summary_table_prefix
        + "_"
        + NODES_COLUMN_NAME: nodes,
        output_summary_table_prefix
        + "_"
        + EDGES_TABLE_NAME: edges,
        output_summary_table_prefix
        + "_"
        + LEAVES_COLUMN_NAME: leaves_dataframe,
        output_summary_table_prefix
        + "_"
        + ROOTS_COLUMN_NAME: roots_dataframe,
        output_summary_table_prefix
        + "_"
        + PATHS_COLUMN_NAME: paths,
        output_summary_table_prefix
        + "_"
        + OBJECTS_BY_TYPE_TABLE_NAME: objects_by_type,
        output_summary_table_prefix
        + "_"
        + CONNECTOR_BY_TYPE_TABLE_NAME: connectors_by_type,
    }

    return general_data_visualisation_dictionary
