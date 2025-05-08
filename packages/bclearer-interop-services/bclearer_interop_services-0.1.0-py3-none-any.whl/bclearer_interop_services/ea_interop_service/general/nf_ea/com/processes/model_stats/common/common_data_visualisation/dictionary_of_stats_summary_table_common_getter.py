import pandas
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.constants import (
    CONNECTED_PROXIES_NAME,
    EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME,
    EDGES_TABLE_NAME,
    FULL_DEPENDENCIES_NAME,
    LEAVES_COLUMN_NAME,
    NODES_COLUMN_NAME,
    NUMBER_OF_CONNECTED_PROXIES_EDGES,
    NUMBER_OF_EDGES,
    NUMBER_OF_LEAVES,
    NUMBER_OF_NODES,
    NUMBER_OF_PATHS,
    NUMBER_OF_ROOTS,
    PATH_LEVEL_DEPTH_COLUMN_NAME,
    PATH_LEVEL_MAX_DEPTH,
    PATHS_COLUMN_NAME,
    ROOTS_COLUMN_NAME,
    SUMMARY_TABLE_TABLE_NAME,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.data_processors.visualisation.summary_table_from_names_and_values_lists_creator import (
    create_summary_table_from_names_and_values_lists,
)


def get_dictionary_of_stats_summary_table_common(
    dictionary_of_stats_common: dict,
    output_summary_table_prefix: str,
) -> pandas.DataFrame:
    number_of_nodes = __get_number_of_nodes(
        dictionary_of_stats_common=dictionary_of_stats_common,
        output_summary_table_prefix=output_summary_table_prefix,
    )

    number_of_edges = __get_number_of_edges(
        dictionary_of_stats_common=dictionary_of_stats_common,
        output_summary_table_prefix=output_summary_table_prefix,
    )

    number_of_leaves = __get_number_of_leaves(
        dictionary_of_stats_common=dictionary_of_stats_common,
        output_summary_table_prefix=output_summary_table_prefix,
    )

    number_of_roots = __get_number_of_roots(
        dictionary_of_stats_common=dictionary_of_stats_common,
        output_summary_table_prefix=output_summary_table_prefix,
    )

    number_of_paths = __get_number_of_paths(
        dictionary_of_stats_common=dictionary_of_stats_common,
        output_summary_table_prefix=output_summary_table_prefix,
    )

    max_value_path_level = __get_max_value_path_level(
        dictionary_of_stats_common=dictionary_of_stats_common,
        output_summary_table_prefix=output_summary_table_prefix,
    )

    summary_names_list = [
        output_summary_table_prefix
        + "_"
        + NUMBER_OF_NODES,
        output_summary_table_prefix
        + "_"
        + NUMBER_OF_EDGES,
        output_summary_table_prefix
        + "_"
        + NUMBER_OF_LEAVES,
        output_summary_table_prefix
        + "_"
        + NUMBER_OF_ROOTS,
        output_summary_table_prefix
        + "_"
        + NUMBER_OF_PATHS,
        output_summary_table_prefix
        + "_"
        + PATH_LEVEL_MAX_DEPTH,
    ]

    summary_values_list = [
        number_of_nodes,
        number_of_edges,
        number_of_leaves,
        number_of_roots,
        number_of_paths,
        max_value_path_level,
    ]

    if (
        output_summary_table_prefix
        == CONNECTED_PROXIES_NAME
    ):
        number_of_connected_proxies_edges = __generate_number_of_connected_proxies_edges(
            dictionary_of_stats_common=dictionary_of_stats_common,
            output_summary_table_prefix=output_summary_table_prefix,
        )

        summary_names_list.insert(
            2,
            output_summary_table_prefix
            + "_"
            + NUMBER_OF_CONNECTED_PROXIES_EDGES,
        )

        summary_values_list.insert(
            2,
            number_of_connected_proxies_edges,
        )

        dictionary_of_stats_summary_table_common = create_summary_table_from_names_and_values_lists(
            names=summary_names_list,
            values=summary_values_list,
        )

    else:
        dictionary_of_stats_summary_table_common = create_summary_table_from_names_and_values_lists(
            names=summary_names_list,
            values=summary_values_list,
        )

    return dictionary_of_stats_summary_table_common


def __get_number_of_nodes(
    dictionary_of_stats_common: dict,
    output_summary_table_prefix: str,
) -> str:
    temporary_nodes_dataframe = (
        dictionary_of_stats_common[
            output_summary_table_prefix
            + "_"
            + NODES_COLUMN_NAME
        ].index
    )

    number_of_nodes = str(
        len(temporary_nodes_dataframe)
    )

    return number_of_nodes


def __get_number_of_edges(
    dictionary_of_stats_common: dict,
    output_summary_table_prefix: str,
) -> str:
    if (
        output_summary_table_prefix
        == CONNECTED_PROXIES_NAME
    ):
        temporary_edges_dataframe = dictionary_of_stats_common[
            output_summary_table_prefix
            + "_"
            + EDGES_TABLE_NAME
        ]

        filtered_edges_dataframe = temporary_edges_dataframe[
            ~temporary_edges_dataframe[
                EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME
            ].str.contains("_place_")
        ]

        number_of_edges = str(
            len(
                filtered_edges_dataframe
            )
        )

        return number_of_edges

    else:
        temporary_edges_dataframe = dictionary_of_stats_common[
            output_summary_table_prefix
            + "_"
            + EDGES_TABLE_NAME
        ].index

        number_of_edges = str(
            len(
                temporary_edges_dataframe
            )
        )

        return number_of_edges


def __generate_number_of_connected_proxies_edges(
    dictionary_of_stats_common: dict,
    output_summary_table_prefix: str,
) -> str:
    temporary_edges_dataframe = (
        dictionary_of_stats_common[
            output_summary_table_prefix
            + "_"
            + EDGES_TABLE_NAME
        ]
    )

    connected_proxies_edges = temporary_edges_dataframe[
        temporary_edges_dataframe[
            EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME
        ].str.contains("_place_")
    ]

    number_of_edges = str(
        len(connected_proxies_edges)
    )

    return number_of_edges


def __get_number_of_leaves(
    dictionary_of_stats_common: dict,
    output_summary_table_prefix: str,
) -> str:
    leaves_dataframe = (
        dictionary_of_stats_common[
            output_summary_table_prefix
            + "_"
            + LEAVES_COLUMN_NAME
        ].index
    )

    number_of_leaves = str(
        len(leaves_dataframe)
    )

    return number_of_leaves


def __get_number_of_roots(
    dictionary_of_stats_common: dict,
    output_summary_table_prefix: str,
) -> str:
    roots_dataframe = (
        dictionary_of_stats_common[
            output_summary_table_prefix
            + "_"
            + ROOTS_COLUMN_NAME
        ].index
    )

    number_of_roots = str(
        len(roots_dataframe)
    )

    return number_of_roots


def __get_number_of_paths(
    dictionary_of_stats_common: dict,
    output_summary_table_prefix: str,
) -> str:
    paths_dataframe = (
        dictionary_of_stats_common[
            output_summary_table_prefix
            + "_"
            + PATHS_COLUMN_NAME
        ].index
    )

    number_of_paths = str(
        len(paths_dataframe)
    )
    return number_of_paths


def __get_max_value_path_level(
    dictionary_of_stats_common: dict,
    output_summary_table_prefix: str,
) -> str:
    if (
        output_summary_table_prefix
        == FULL_DEPENDENCIES_NAME
    ):
        path_analysis_master_table = dictionary_of_stats_common[
            output_summary_table_prefix
            + "_"
            + SUMMARY_TABLE_TABLE_NAME
        ]

        if (
            path_analysis_master_table.empty
        ):
            path_level_max_depth = 0

        else:
            path_level_max_depth = str(
                path_analysis_master_table[
                    PATH_LEVEL_DEPTH_COLUMN_NAME
                ].max()
            )

        return path_level_max_depth

    else:
        paths_table = dictionary_of_stats_common[
            output_summary_table_prefix
            + "_"
            + PATHS_COLUMN_NAME
        ]

        path_level_max_depth = str(
            paths_table[
                PATH_LEVEL_DEPTH_COLUMN_NAME
            ].max()
        )

        return path_level_max_depth
