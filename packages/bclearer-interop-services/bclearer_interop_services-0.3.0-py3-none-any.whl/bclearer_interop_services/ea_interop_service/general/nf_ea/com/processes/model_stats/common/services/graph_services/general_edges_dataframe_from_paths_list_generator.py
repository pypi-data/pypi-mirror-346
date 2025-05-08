import pandas
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.constants import (
    CLIENT_PLACE2_END_CONNECTORS_COLUMN_NAME,
    EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME,
    EA_OBJECT_NAME_COLUMN_NAME,
    IMPLICIT_DEPENDENCY_NAME,
    LEVEL_COLUMN_NAME,
    SOURCE_COLUMN_NAME,
    SUPPLIER_PLACE1_END_CONNECTORS_COLUMN_NAME,
    TARGET_COLUMN_NAME,
)


def get_full_dependency_analysis_edges_table(
    list_of_all_simple_paths: list,
    ea_connectors: pandas.DataFrame,
    ea_stereotypes: pandas.DataFrame,
    ea_stereotype_usage: pandas.DataFrame,
) -> pandas.DataFrame:
    edges_and_edges_max_level_table = __get_edges_and_edges_max_level_table(
        list_of_all_simple_paths=list_of_all_simple_paths
    )

    edges_table_with_connector_types_and_names = __add_connector_types_and_names_to_edges_table(
        edges_and_edges_max_level_table=edges_and_edges_max_level_table,
        ea_connectors=ea_connectors,
    )

    # edges_table_with_data_columns = \
    #     add_data_columns_to_edge_base_table(
    #         edge_base_table=edges_table_with_connector_types_and_names,
    #         ea_connectors=ea_connectors,
    #         ea_stereotypes=ea_stereotypes,
    #         ea_stereotype_usage=ea_stereotype_usage)

    full_dependency_analysis_edges_table = __mark_implicit_dependencies_in_edges_table(
        edges_table_with_data_columns=edges_table_with_connector_types_and_names
    )

    return full_dependency_analysis_edges_table


def __get_edges_and_edges_max_level_table(
    list_of_all_simple_paths: list,
) -> pandas.DataFrame:
    edges_dictionary = {}

    edges_level_list = []

    source_node_list = []

    target_node_list = []

    for (
        path
    ) in list_of_all_simple_paths:
        for (
            source_node,
            target_node,
        ) in zip(path[:-1], path[1:]):
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
        pandas.DataFrame.from_dict(
            edges_dictionary
        ).drop_duplicates()
    )

    edges_and_edges_max_level_table = (
        edges_dataframe.groupby(
            [
                SOURCE_COLUMN_NAME,
                TARGET_COLUMN_NAME,
            ],
            as_index=False,
        )[LEVEL_COLUMN_NAME].max()
    )

    return (
        edges_and_edges_max_level_table
    )


def __add_connector_types_and_names_to_edges_table(
    edges_and_edges_max_level_table: pandas.DataFrame,
    ea_connectors: pandas.DataFrame,
) -> pandas.DataFrame:
    foreign_key_name_column_names = {
        EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME: EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME,
        EA_OBJECT_NAME_COLUMN_NAME: EA_OBJECT_NAME_COLUMN_NAME,
    }

    edges_dataframe_attributes_added = left_merge_dataframes(
        master_dataframe=edges_and_edges_max_level_table,
        master_dataframe_key_columns=[
            SOURCE_COLUMN_NAME,
            TARGET_COLUMN_NAME,
        ],
        merge_suffixes=["1", "2"],
        foreign_key_dataframe=ea_connectors,
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

    edges_table_with_connector_types_and_names = dataframe_filter_and_rename(
        dataframe=edges_dataframe_attributes_added,
        filter_and_rename_dictionary=dataframe_columns_dictionary,
    )

    return edges_table_with_connector_types_and_names


def __mark_implicit_dependencies_in_edges_table(
    edges_table_with_data_columns: pandas.DataFrame,
) -> pandas.DataFrame:
    implicit_edges_value = {
        EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME: IMPLICIT_DEPENDENCY_NAME,
        EA_OBJECT_NAME_COLUMN_NAME: IMPLICIT_DEPENDENCY_NAME,
    }

    # This instruction also fills the nan's in the connector name column. We'll leave it like this for now.
    edges_table_with_data_columns.fillna(
        value=implicit_edges_value,
        inplace=True,
    )

    return edges_table_with_data_columns
