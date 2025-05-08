from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.constants import (
    EDGES_TABLE_NAME_SUFFIX,
    IMPLICIT_EDGES_TABLE_NAME,
    LEAVES_TABLE_NAME_SUFFIX,
    NODES_TABLE_NAME_SUFFIX,
    NUMBER_OF_EDGES,
    NUMBER_OF_IMPLICIT_EDGES,
    NUMBER_OF_LEAVES,
    NUMBER_OF_NODES,
    NUMBER_OF_ROOTS,
    PATH_LEVEL_DEPTH_COLUMN_NAME,
    PATH_LEVEL_MAX_DEPTH,
    RELATION_TYPE_COLUMN_NAME,
    ROOTS_TABLE_NAME_SUFFIX,
    STATS_COLUMN_NAME,
    TOTALS_COLUMN_NAME,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.number_of_implicit_edges_collector import (
    get_number_of_implicit_edges,
)
from pandas import DataFrame


def get_dictionary_of_stats_summary_table_high_relation_type(
    full_dependencies_path_analysis_master_table: DataFrame,
    high_relation_type_dictionary_of_stats: dict,
    high_relation_type_name: str,
) -> DataFrame:
    temporary_dataframe = __generate_temporary_dataframe(
        full_dependencies_path_analysis_master_table=full_dependencies_path_analysis_master_table,
        high_relation_type_name=high_relation_type_name,
    )

    number_of_nodes = __get_number_of_nodes(
        relation_type_dictionary=high_relation_type_dictionary_of_stats,
        relation_type_name=high_relation_type_name,
    )

    number_of_edges = __get_number_of_edges(
        relation_type_dictionary=high_relation_type_dictionary_of_stats,
        relation_type_name=high_relation_type_name,
    )

    number_of_implicit_edges = get_number_of_implicit_edges(
        dictionary_of_dataframes=high_relation_type_dictionary_of_stats,
        dictionary_of_dataframes_table_name=high_relation_type_name
        + "_"
        + IMPLICIT_EDGES_TABLE_NAME,
    )

    number_of_leaves = __get_number_of_leaves(
        relation_type_dictionary=high_relation_type_dictionary_of_stats,
        relation_type_name=high_relation_type_name,
    )

    number_of_roots = __get_number_of_roots(
        relation_type_dictionary=high_relation_type_dictionary_of_stats,
        relation_type_name=high_relation_type_name,
    )

    max_value_path_level = __get_max_value_path_level(
        temporary_dataframe=temporary_dataframe
    )

    data_visualisation_summary_table = __generate_data_visualisation_summary_table(
        relation_type_name=high_relation_type_name,
        number_of_nodes=number_of_nodes,
        number_of_edges=number_of_edges,
        number_of_implicit_edges=number_of_implicit_edges,
        number_of_leaves=number_of_leaves,
        number_of_roots=number_of_roots,
        path_level_max_depth=max_value_path_level,
    )

    return (
        data_visualisation_summary_table
    )


def __generate_temporary_dataframe(
    full_dependencies_path_analysis_master_table: DataFrame,
    high_relation_type_name: str,
) -> DataFrame:

    full_dependencies_relations_dataframe_filtered = full_dependencies_path_analysis_master_table[
        full_dependencies_path_analysis_master_table[
            RELATION_TYPE_COLUMN_NAME
        ]
        == high_relation_type_name
    ]

    temporary_dataframe = DataFrame()

    temporary_dataframe[
        PATH_LEVEL_DEPTH_COLUMN_NAME
    ] = full_dependencies_relations_dataframe_filtered[
        PATH_LEVEL_DEPTH_COLUMN_NAME
    ]

    return temporary_dataframe


def __get_number_of_nodes(
    relation_type_dictionary: dict,
    relation_type_name: str,
) -> str:
    temporary_nodes_dataframe = (
        relation_type_dictionary[
            relation_type_name
            + NODES_TABLE_NAME_SUFFIX
        ].index
    )

    number_of_nodes = str(
        len(temporary_nodes_dataframe)
    )
    return number_of_nodes


def __get_number_of_edges(
    relation_type_dictionary: dict,
    relation_type_name: str,
) -> str:
    temporary_edges_dataframe = (
        relation_type_dictionary[
            relation_type_name
            + EDGES_TABLE_NAME_SUFFIX
        ].index
    )

    number_of_edges = str(
        len(temporary_edges_dataframe)
    )

    return number_of_edges


def __get_number_of_leaves(
    relation_type_dictionary: dict,
    relation_type_name: str,
) -> str:
    temporary_leaves_dataframe = (
        relation_type_dictionary[
            relation_type_name
            + LEAVES_TABLE_NAME_SUFFIX
        ].index
    )

    number_of_leaves = str(
        len(temporary_leaves_dataframe)
    )

    return number_of_leaves


def __get_number_of_roots(
    relation_type_dictionary: dict,
    relation_type_name: str,
) -> str:
    temporary_roots_dataframe = (
        relation_type_dictionary[
            relation_type_name
            + ROOTS_TABLE_NAME_SUFFIX
        ].index
    )

    number_of_roots = str(
        len(temporary_roots_dataframe)
    )

    return number_of_roots


def __get_max_value_path_level(
    temporary_dataframe: DataFrame,
) -> str:
    if temporary_dataframe.empty:
        path_level_max_depth = str(0)

        return path_level_max_depth

    else:
        path_level_max_depth = str(
            temporary_dataframe[
                PATH_LEVEL_DEPTH_COLUMN_NAME
            ].max()
        )
        return path_level_max_depth


def __generate_data_visualisation_summary_table(
    relation_type_name: str,
    number_of_nodes: str,
    number_of_edges: str,
    number_of_implicit_edges: str,
    number_of_leaves: str,
    number_of_roots: str,
    path_level_max_depth: str,
) -> DataFrame:
    summary_table_stats_names = [
        relation_type_name
        + "_"
        + NUMBER_OF_NODES,
        relation_type_name
        + "_"
        + NUMBER_OF_EDGES,
        relation_type_name
        + "_"
        + NUMBER_OF_IMPLICIT_EDGES,
        relation_type_name
        + "_"
        + NUMBER_OF_LEAVES,
        relation_type_name
        + "_"
        + NUMBER_OF_ROOTS,
        relation_type_name
        + "_"
        + PATH_LEVEL_MAX_DEPTH,
    ]

    summary_table_stats_totals = [
        number_of_nodes,
        number_of_edges,
        number_of_implicit_edges,
        number_of_leaves,
        number_of_roots,
        path_level_max_depth,
    ]

    summary_table_dictionary = {
        STATS_COLUMN_NAME: summary_table_stats_names,
        TOTALS_COLUMN_NAME: summary_table_stats_totals,
    }

    summary_table_dataframe = DataFrame.from_dict(
        data=summary_table_dictionary
    )

    return summary_table_dataframe
