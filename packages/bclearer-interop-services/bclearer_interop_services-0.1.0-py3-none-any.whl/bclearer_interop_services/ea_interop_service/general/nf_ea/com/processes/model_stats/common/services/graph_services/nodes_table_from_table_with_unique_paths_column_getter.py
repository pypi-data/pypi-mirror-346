import pandas
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.constants import (
    LEVEL_COLUMN_NAME,
    NF_UUIDS_COLUMN_NAME,
)


def get_nodes_base_table_with_node_max_levels_from_paths_table(
    table_with_unique_paths_column: pandas.DataFrame,
    path_column_name: str,
) -> pandas.DataFrame:
    paths_list = (
        table_with_unique_paths_column[
            path_column_name
        ].tolist()
    )

    nodes_base_table_with_node_max_levels = __get_nodes_with_max_level(
        paths_list=paths_list
    )

    return nodes_base_table_with_node_max_levels


def __get_nodes_with_max_level(
    paths_list: list,
) -> pandas.DataFrame:

    nodes_dictionary_with_level_list = (
        {}
    )

    node_levels_list = []

    node_list = []

    for path in paths_list:
        for node in path:
            node_level = path.index(
                node
            )

            node_list.append(node)

            node_levels_list.append(
                node_level
            )

    nodes_dictionary_with_level_list[
        NF_UUIDS_COLUMN_NAME
    ] = node_list

    nodes_dictionary_with_level_list[
        LEVEL_COLUMN_NAME
    ] = node_levels_list

    nodes_dataframe = pandas.DataFrame.from_dict(
        nodes_dictionary_with_level_list
    )

    nodes_dataframe_max_level = (
        nodes_dataframe.groupby(
            [NF_UUIDS_COLUMN_NAME],
            as_index=False,
        )[LEVEL_COLUMN_NAME].max()
    )

    return nodes_dataframe_max_level
