from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.constants import (
    EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME,
    EDGES_TABLE_NAME_SUFFIX,
    FULL_DEPENDENCIES_LEAVES_TABLE_NAME,
    FULL_DEPENDENCIES_ROOTS_TABLE_NAME,
    FULL_DEPENDENCIES_SUMMARY_TABLE_NAME,
    IMPLICIT_DEPENDENCY_NAME,
    IMPLICIT_EDGES_TABLE_NAME,
    LEAVES_COLUMN_NAME,
    LEAVES_TABLE_NAME_SUFFIX,
    NF_UUIDS_COLUMN_NAME,
    NODES_TABLE_NAME_SUFFIX,
    PATH_LEVEL_DEPTH_COLUMN_NAME,
    PATHS_COLUMN_NAME,
    RELATION_TYPE_COLUMN_NAME,
    ROOTS_COLUMN_NAME,
    ROOTS_TABLE_NAME_SUFFIX,
    SOURCE_COLUMN_NAME,
    TARGET_COLUMN_NAME,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.directed_graph_from_table_with_unique_paths_column_getter import (
    get_directed_graph_from_table_with_unique_paths_column,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.edges_table_from_table_with_unique_paths_column_getter import (
    get_edges_table_from_table_with_unique_paths_column,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.full_dependency_analysis_nodes_table_getter import (
    get_full_dependency_analysis_nodes_table,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.list_of_leaves_from_multi_edged_directed_graph_getter import (
    get_list_of_leaves_from_multi_edged_directed_graph,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.list_of_roots_from_directed_graph_getter import (
    get_list_of_roots_from_multi_edged_directed_graph,
)
from pandas import DataFrame


def get_high_relation_type_dictionary_of_stats(
    full_dependency_analysis_dictionary_of_stats_common: dict,
    ea_classifiers: DataFrame,
    ea_packages: DataFrame,
    ea_connectors: DataFrame,
    ea_stereotypes: DataFrame,
    ea_stereotype_usage: DataFrame,
    high_relation_type_name: str,
) -> dict:
    full_dependencies_path_analysis_master_table_filtered_to_high_relation_type = __get_full_dependencies_path_analysis_master_table_filtered_to_high_relation_type(
        full_dependency_analysis_dictionary_of_stats=full_dependency_analysis_dictionary_of_stats_common,
        high_relation_type_name=high_relation_type_name,
    )

    if (
        full_dependencies_path_analysis_master_table_filtered_to_high_relation_type.empty
    ):
        high_relation_type_dictionary_of_stats = __create_empty_high_relation_type_dictionary_of_stats(
            high_relation_type_name=high_relation_type_name
        )

        return high_relation_type_dictionary_of_stats

    else:
        high_relation_type_dictionary_of_stats = __create_not_empty_high_relation_type_dictionary_of_stats(
            full_dependencies_path_analysis_master_table_filtered_to_high_relation_type=full_dependencies_path_analysis_master_table_filtered_to_high_relation_type,
            ea_classifiers=ea_classifiers,
            ea_packages=ea_packages,
            ea_connectors=ea_connectors,
            ea_stereotypes=ea_stereotypes,
            ea_stereotype_usage=ea_stereotype_usage,
            high_relation_type_name=high_relation_type_name,
        )

        return high_relation_type_dictionary_of_stats


def __get_full_dependencies_path_analysis_master_table_filtered_to_high_relation_type(
    full_dependency_analysis_dictionary_of_stats: dict,
    high_relation_type_name: str,
) -> DataFrame:
    full_dependencies_path_analysis_master_table = full_dependency_analysis_dictionary_of_stats[
        FULL_DEPENDENCIES_SUMMARY_TABLE_NAME
    ]

    full_dependencies_path_analysis_master_table_filtered_to_high_relation_type = full_dependencies_path_analysis_master_table[
        full_dependencies_path_analysis_master_table[
            RELATION_TYPE_COLUMN_NAME
        ]
        == high_relation_type_name
    ]

    return full_dependencies_path_analysis_master_table_filtered_to_high_relation_type


def __create_empty_high_relation_type_dictionary_of_stats(
    high_relation_type_name: str,
) -> dict:
    nodes = DataFrame(
        columns=[NF_UUIDS_COLUMN_NAME]
    )
    edges = DataFrame(
        columns=[
            SOURCE_COLUMN_NAME,
            TARGET_COLUMN_NAME,
        ]
    )

    implicit_edges = DataFrame(
        columns=[
            SOURCE_COLUMN_NAME,
            TARGET_COLUMN_NAME,
        ]
    )

    leaves = DataFrame(
        columns=[LEAVES_COLUMN_NAME]
    )

    roots = DataFrame(
        columns=[ROOTS_COLUMN_NAME]
    )

    empty_high_relation_type_dictionary_of_stats = {
        high_relation_type_name
        + NODES_TABLE_NAME_SUFFIX: nodes,
        high_relation_type_name
        + EDGES_TABLE_NAME_SUFFIX: edges,
        high_relation_type_name
        + "_"
        + IMPLICIT_EDGES_TABLE_NAME: implicit_edges,
        high_relation_type_name
        + LEAVES_TABLE_NAME_SUFFIX: DataFrame(
            data=leaves,
            columns=[
                high_relation_type_name
                + "_"
                + FULL_DEPENDENCIES_LEAVES_TABLE_NAME
            ],
        ),
        high_relation_type_name
        + ROOTS_TABLE_NAME_SUFFIX: DataFrame(
            data=roots,
            columns=[
                high_relation_type_name
                + "-"
                + FULL_DEPENDENCIES_ROOTS_TABLE_NAME
            ],
        ),
    }

    return empty_high_relation_type_dictionary_of_stats


def __create_not_empty_high_relation_type_dictionary_of_stats(
    full_dependencies_path_analysis_master_table_filtered_to_high_relation_type: DataFrame,
    ea_classifiers: DataFrame,
    ea_packages: DataFrame,
    ea_connectors: DataFrame,
    ea_stereotypes: DataFrame,
    ea_stereotype_usage: DataFrame,
    high_relation_type_name: str,
) -> dict:
    graph = get_directed_graph_from_table_with_unique_paths_column(
        table_with_unique_paths_column=full_dependencies_path_analysis_master_table_filtered_to_high_relation_type,
        path_column_name=PATHS_COLUMN_NAME,
    )

    nodes = get_full_dependency_analysis_nodes_table(
        ea_classifiers=ea_classifiers,
        ea_packages=ea_packages,
        ea_stereotypes=ea_stereotypes,
        ea_stereotype_usage=ea_stereotype_usage,
        full_dependencies_path_analysis_master_table=full_dependencies_path_analysis_master_table_filtered_to_high_relation_type,
    )

    edges = get_edges_table_from_table_with_unique_paths_column(
        table_with_unique_paths_column=full_dependencies_path_analysis_master_table_filtered_to_high_relation_type,
        ea_connectors=ea_connectors,
        path_column_name=PATHS_COLUMN_NAME,
    )

    leaves = get_list_of_leaves_from_multi_edged_directed_graph(
        multi_edged_directed_graph=graph
    )

    roots = get_list_of_roots_from_multi_edged_directed_graph(
        multi_edged_directed_graph=graph
    )

    path_list = full_dependencies_path_analysis_master_table_filtered_to_high_relation_type.filter(
        items=[
            PATHS_COLUMN_NAME,
            PATH_LEVEL_DEPTH_COLUMN_NAME,
        ]
    )

    implicit_edges = edges[
        edges[
            EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME
        ]
        == IMPLICIT_DEPENDENCY_NAME
    ]

    high_relation_type_dictionary_of_stats = {
        high_relation_type_name
        + NODES_TABLE_NAME_SUFFIX: nodes,
        high_relation_type_name
        + EDGES_TABLE_NAME_SUFFIX: edges,
        high_relation_type_name
        + "_"
        + IMPLICIT_EDGES_TABLE_NAME: implicit_edges,
        high_relation_type_name
        + "_"
        + PATHS_COLUMN_NAME: path_list,
        high_relation_type_name
        + LEAVES_TABLE_NAME_SUFFIX: DataFrame(
            data=leaves,
            columns=[
                high_relation_type_name
                + "_"
                + FULL_DEPENDENCIES_LEAVES_TABLE_NAME
            ],
        ),
        high_relation_type_name
        + ROOTS_TABLE_NAME_SUFFIX: DataFrame(
            data=roots,
            columns=[
                high_relation_type_name
                + "-"
                + FULL_DEPENDENCIES_ROOTS_TABLE_NAME
            ],
        ),
    }

    return high_relation_type_dictionary_of_stats
