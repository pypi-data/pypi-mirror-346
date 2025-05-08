from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.constants import (
    CLIENT_PLACE2_END_CONNECTORS_COLUMN_NAME,
    DEPENDENCY_NAME,
    EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME,
    EA_OBJECT_NAME_COLUMN_NAME,
    IMPLICIT_DEPENDENCY_NAME,
    LEVEL_COLUMN_NAME,
    SOURCE_COLUMN_NAME,
    SUPPLIER_PLACE1_END_CONNECTORS_COLUMN_NAME,
    TARGET_COLUMN_NAME,
)
from pandas import DataFrame


def get_edges_table_from_table_with_unique_paths_column(
    table_with_unique_paths_column: DataFrame,
    ea_connectors: DataFrame,
    path_column_name: str,
) -> DataFrame:
    paths_list = (
        table_with_unique_paths_column[
            path_column_name
        ].tolist()
    )

    edges_with_level = __generate_edges_dataframe_with_level(
        paths_list=paths_list
    )

    edges_with_attributes = __add_attributes_to_edges(
        edges_dataframe=edges_with_level,
        ea_connectors=ea_connectors,
    )

    full_dependencies_edges_dataframe = __add_values_to_implicit_edges(
        edges_with_attributes=edges_with_attributes
    )

    return full_dependencies_edges_dataframe


def __generate_edges_dataframe_with_level(
    paths_list: list,
) -> DataFrame:
    edges_dictionary = {}

    edges_level_list = []

    source_node_list = []

    target_node_list = []

    # It is assumed the path is directed from leaf to root
    for path in paths_list:
        for (
            source_node,
            target_node,
        ) in zip(
            path[:-1], path[1:]
        ):  # original: zip(path[1:], path[:-1])
            edge_level = path.index(
                target_node
            )

            source_node_list.append(
                source_node
            )

            target_node_list.append(
                target_node
            )

            edges_level_list.append(
                edge_level
            )

    edges_dictionary[
        SOURCE_COLUMN_NAME
    ] = source_node_list

    edges_dictionary[
        TARGET_COLUMN_NAME
    ] = target_node_list

    edges_dictionary[
        LEVEL_COLUMN_NAME
    ] = edges_level_list

    edges_dataframe = (
        DataFrame.from_dict(
            edges_dictionary
        ).drop_duplicates()
    )

    edges_dataframe_max_level = (
        edges_dataframe.groupby(
            [
                SOURCE_COLUMN_NAME,
                TARGET_COLUMN_NAME,
            ],
            as_index=False,
        )[LEVEL_COLUMN_NAME].max()
    )

    return edges_dataframe_max_level


def __add_attributes_to_edges(
    edges_dataframe: DataFrame,
    ea_connectors: DataFrame,
) -> DataFrame:
    ea_connectors_filtered = ea_connectors.loc[
        ea_connectors[
            EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME
        ]
        == DEPENDENCY_NAME
    ]

    foreign_key_name_column_names = {
        EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME: EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME,
        EA_OBJECT_NAME_COLUMN_NAME: EA_OBJECT_NAME_COLUMN_NAME,
    }

    edges_dataframe_attributes_added = left_merge_dataframes(
        master_dataframe=edges_dataframe,
        master_dataframe_key_columns=[
            SOURCE_COLUMN_NAME,
            TARGET_COLUMN_NAME,
        ],  # Previously: [TARGET_COLUMN_NAME, SOURCE_COLUMN_NAME]
        merge_suffixes=["1", "2"],
        foreign_key_dataframe=ea_connectors_filtered,
        foreign_key_dataframe_fk_columns=[
            SUPPLIER_PLACE1_END_CONNECTORS_COLUMN_NAME,
            CLIENT_PLACE2_END_CONNECTORS_COLUMN_NAME,
        ],
        foreign_key_dataframe_other_column_rename_dictionary=foreign_key_name_column_names,
    ).drop_duplicates()

    dataframe_columns_dictionary = {
        SOURCE_COLUMN_NAME: SOURCE_COLUMN_NAME,
        TARGET_COLUMN_NAME: TARGET_COLUMN_NAME,
        EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME: EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME,
        EA_OBJECT_NAME_COLUMN_NAME: EA_OBJECT_NAME_COLUMN_NAME,
        LEVEL_COLUMN_NAME: LEVEL_COLUMN_NAME,
    }

    edges_dataframe_with_ea_connectors_attributes = dataframe_filter_and_rename(
        dataframe=edges_dataframe_attributes_added,
        filter_and_rename_dictionary=dataframe_columns_dictionary,
    )

    return edges_dataframe_with_ea_connectors_attributes


def __add_values_to_implicit_edges(
    edges_with_attributes: DataFrame,
) -> DataFrame:
    implicit_edges_value = {
        EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME: IMPLICIT_DEPENDENCY_NAME,
        EA_OBJECT_NAME_COLUMN_NAME: IMPLICIT_DEPENDENCY_NAME,
    }

    edges_with_attributes.fillna(
        value=implicit_edges_value,
        inplace=True,
    )

    return edges_with_attributes
