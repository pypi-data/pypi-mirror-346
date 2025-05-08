import networkx
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.constants import (
    FULL_DEPENDENCIES_EDGES_TABLE_NAME,
    FULL_DEPENDENCIES_LEAVES_TABLE_NAME,
    FULL_DEPENDENCIES_NODES_TABLE_NAME,
    FULL_DEPENDENCIES_PATHS_TABLE_NAME,
    FULL_DEPENDENCIES_ROOTS_TABLE_NAME,
    FULL_DEPENDENCIES_SUMMARY_TABLE_NAME,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.full_dependency_analysis_nodes_table_getter import (
    get_full_dependency_analysis_nodes_table,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.general_edges_dataframe_from_paths_list_generator import (
    get_full_dependency_analysis_edges_table,
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
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.data_processors.full_dependencies.full_dependencies_path_analysis_master_table_getter import (
    get_full_dependencies_path_analysis_master_table,
)
from pandas import DataFrame


def get_full_dependency_analysis_dictionary_of_stats_common(
    full_dependency_analysis_model_multi_edged_directed_graph: networkx.MultiDiGraph,
    ea_classifiers: DataFrame,
    ea_packages: DataFrame,
    ea_connectors: DataFrame,
    ea_stereotypes: DataFrame,
    ea_stereotype_usage: DataFrame,
) -> dict:
    full_dependency_analysis_list_of_leaves = get_list_of_leaves_from_multi_edged_directed_graph(
        multi_edged_directed_graph=full_dependency_analysis_model_multi_edged_directed_graph
    )

    full_dependency_analysis_list_of_roots = get_list_of_roots_from_multi_edged_directed_graph(
        multi_edged_directed_graph=full_dependency_analysis_model_multi_edged_directed_graph
    )

    full_dependency_analysis_list_of_all_simple_paths = get_list_of_all_simple_paths_from_graph(
        graph=full_dependency_analysis_model_multi_edged_directed_graph,
        roots=full_dependency_analysis_list_of_roots,
        leaves=full_dependency_analysis_list_of_leaves,
    )

    full_dependencies_path_analysis_master_table = get_full_dependencies_path_analysis_master_table(
        all_paths_list=full_dependency_analysis_list_of_all_simple_paths,
        ea_classifiers=ea_classifiers,
    )

    full_dependency_analysis_nodes_table = get_full_dependency_analysis_nodes_table(
        ea_classifiers=ea_classifiers,
        ea_packages=ea_packages,
        ea_stereotypes=ea_stereotypes,
        ea_stereotype_usage=ea_stereotype_usage,
        full_dependencies_path_analysis_master_table=full_dependencies_path_analysis_master_table,
    )

    full_dependency_analysis_edges_table = get_full_dependency_analysis_edges_table(
        list_of_all_simple_paths=full_dependency_analysis_list_of_all_simple_paths,
        ea_connectors=ea_connectors,
        ea_stereotypes=ea_stereotypes,
        ea_stereotype_usage=ea_stereotype_usage,
    )

    full_dependency_analysis_dictionary_of_stats_common = __get_full_dependency_analysis_dictionary_of_stats_common(
        nodes=full_dependency_analysis_nodes_table,
        edges=full_dependency_analysis_edges_table,
        leaves=full_dependency_analysis_list_of_leaves,
        roots=full_dependency_analysis_list_of_roots,
        paths=full_dependency_analysis_list_of_all_simple_paths,
        path_analysis_master_table=full_dependencies_path_analysis_master_table,
    )

    return full_dependency_analysis_dictionary_of_stats_common


def __get_full_dependency_analysis_dictionary_of_stats_common(
    nodes: DataFrame,
    edges: DataFrame,
    leaves: list,
    roots: list,
    paths: list,
    path_analysis_master_table: DataFrame,
) -> dict:
    nodes_dataframe = nodes

    edges_dataframe = edges

    leaves_dataframe = DataFrame(
        data=leaves,
        columns=[
            FULL_DEPENDENCIES_LEAVES_TABLE_NAME
        ],
    )

    roots_dataframe = DataFrame(
        data=roots,
        columns=[
            FULL_DEPENDENCIES_ROOTS_TABLE_NAME
        ],
    )

    paths_dictionary = {
        FULL_DEPENDENCIES_PATHS_TABLE_NAME: paths
    }

    paths_dataframe = (
        DataFrame.from_dict(
            paths_dictionary
        )
    )

    full_dependency_analysis_dictionary_of_stats_common = {
        FULL_DEPENDENCIES_NODES_TABLE_NAME: nodes_dataframe,
        FULL_DEPENDENCIES_EDGES_TABLE_NAME: edges_dataframe,
        FULL_DEPENDENCIES_LEAVES_TABLE_NAME: leaves_dataframe,
        FULL_DEPENDENCIES_ROOTS_TABLE_NAME: roots_dataframe,
        FULL_DEPENDENCIES_PATHS_TABLE_NAME: paths_dataframe,
        FULL_DEPENDENCIES_SUMMARY_TABLE_NAME: path_analysis_master_table,
    }

    return full_dependency_analysis_dictionary_of_stats_common
