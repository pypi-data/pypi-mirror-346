from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.constants import (
    LEAVES_COLUMN_NAME,
    NF_UUIDS_COLUMN_NAME,
    PATHS_COLUMN_NAME,
    RELATION_TYPE_COLUMN_NAME,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.data_columns_to_nodes_base_table_adder import (
    add_data_columns_to_nodes_base_table,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.nodes_table_from_table_with_unique_paths_column_getter import (
    get_nodes_base_table_with_node_max_levels_from_paths_table,
)
from pandas import DataFrame


def get_full_dependency_analysis_nodes_table(
    ea_classifiers: DataFrame,
    ea_packages: DataFrame,
    ea_stereotypes: DataFrame,
    ea_stereotype_usage: DataFrame,
    full_dependencies_path_analysis_master_table: DataFrame,
) -> DataFrame:
    full_dependency_analysis_nodes_base_table_with_max_levels = get_nodes_base_table_with_node_max_levels_from_paths_table(
        table_with_unique_paths_column=full_dependencies_path_analysis_master_table,
        path_column_name=PATHS_COLUMN_NAME,
    )

    full_dependency_analysis_nodes_table = __add_data_to_nodes_table(
        full_dependencies_path_analysis_master_table=full_dependencies_path_analysis_master_table,
        full_dependency_analysis_nodes_and_nodes_max_level_table=full_dependency_analysis_nodes_base_table_with_max_levels,
        ea_classifiers=ea_classifiers,
        ea_packages=ea_packages,
        ea_stereotypes=ea_stereotypes,
        ea_stereotype_usage=ea_stereotype_usage,
    )

    return full_dependency_analysis_nodes_table


def __add_data_to_nodes_table(
    full_dependencies_path_analysis_master_table: DataFrame,
    full_dependency_analysis_nodes_and_nodes_max_level_table: DataFrame,
    ea_classifiers: DataFrame,
    ea_packages: DataFrame,
    ea_stereotypes: DataFrame,
    ea_stereotype_usage: DataFrame,
) -> DataFrame:
    nodes_table_with_data_columns = add_data_columns_to_nodes_base_table(
        nodes_base_table=full_dependency_analysis_nodes_and_nodes_max_level_table,
        ea_classifiers=ea_classifiers,
        ea_packages=ea_packages,
        ea_stereotypes=ea_stereotypes,
        ea_stereotype_usage=ea_stereotype_usage,
    )

    nodes_table_with_leaf_high_relation_types = __add_leaves_high_relation_type_to_nodes_table(
        full_dependencies_path_analysis_master_table=full_dependencies_path_analysis_master_table,
        nodes_table_with_data_columns=nodes_table_with_data_columns,
    )

    return nodes_table_with_leaf_high_relation_types


def __add_leaves_high_relation_type_to_nodes_table(
    full_dependencies_path_analysis_master_table: DataFrame,
    nodes_table_with_data_columns: DataFrame,
) -> DataFrame:
    foreign_key_name_column_names = {
        RELATION_TYPE_COLUMN_NAME: RELATION_TYPE_COLUMN_NAME,
    }

    nodes_dataframe_attributes_added = left_merge_dataframes(
        master_dataframe=nodes_table_with_data_columns,
        master_dataframe_key_columns=[
            NF_UUIDS_COLUMN_NAME
        ],
        merge_suffixes=["1", "2"],
        foreign_key_dataframe=full_dependencies_path_analysis_master_table,
        foreign_key_dataframe_fk_columns=[
            LEAVES_COLUMN_NAME
        ],
        foreign_key_dataframe_other_column_rename_dictionary=foreign_key_name_column_names,
    ).drop_duplicates(
        subset=NF_UUIDS_COLUMN_NAME
    )

    nodes_table_with_leaf_high_relation_types = nodes_dataframe_attributes_added.drop_duplicates(
        subset=NF_UUIDS_COLUMN_NAME
    )

    return nodes_table_with_leaf_high_relation_types
