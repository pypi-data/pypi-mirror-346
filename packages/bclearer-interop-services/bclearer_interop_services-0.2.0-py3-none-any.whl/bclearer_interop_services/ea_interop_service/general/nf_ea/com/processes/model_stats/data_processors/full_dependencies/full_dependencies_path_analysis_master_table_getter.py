import numpy
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.constants import (
    ASSOCIATION_TYPE_NAME,
    CLASS_TYPE_NAME,
    EA_OBJECT_NAME_COLUMN_NAME,
    EA_OBJECT_TYPE_COLUMN_NAME,
    FIRST_CLASS_RELATION_NAME,
    HIGH_ORDER_TYPE_RELATION_NAME,
    LEAVES_COLUMN_NAME,
    LEAVES_NAME_COLUMN_NAME,
    LEAVES_TYPE_COLUMN_NAME,
    NF_UUIDS_COLUMN_NAME,
    OBJECT_TYPE_NAME,
    PATH_LEVEL_DEPTH_COLUMN_NAME,
    PATHS_COLUMN_NAME,
    PROXYCONNECTOR_TYPE_NAME,
    RELATION_TYPE_COLUMN_NAME,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.graph_services.paths_and_path_depths_table_from_path_list_getter import (
    get_paths_and_path_depths_table_from_path_list,
)
from pandas import DataFrame


def get_full_dependencies_path_analysis_master_table(
    all_paths_list: list,
    ea_classifiers: DataFrame,
) -> DataFrame:
    paths_and_path_depths_table = get_paths_and_path_depths_table_from_path_list(
        path_list=all_paths_list
    )

    path_analysis_master_table_with_leaves = __add_leaves_to_path_analysis_master_table(
        full_dependencies_path_analysis_master_table=paths_and_path_depths_table,
        all_paths_list=all_paths_list,
    )

    path_analysis_master_table_with_leaf_names_and_types = __add_leaf_names_and_types_to_path_analysis_master_table(
        full_dependencies_path_analysis_master_table=path_analysis_master_table_with_leaves,
        ea_classifiers=ea_classifiers,
    )

    full_dependencies_path_analysis_master_table = __add_leaf_high_relation_type_to_path_analysis_master_table(
        full_dependencies_path_analysis_master_table=path_analysis_master_table_with_leaf_names_and_types
    )

    return full_dependencies_path_analysis_master_table


def __add_leaves_to_path_analysis_master_table(
    full_dependencies_path_analysis_master_table: DataFrame,
    all_paths_list: list,
) -> DataFrame:
    paths_and_leaves_dictionary = {}

    list_of_paths = []

    list_of_leaves = []

    # Because we inverted the way the paths are calculated (now from leaves to roots) the leaves are the first
    #  element of the list of paths (path[0])
    for path in all_paths_list:
        list_of_paths.append(path)

        list_of_leaves.append(path[0])

    paths_and_leaves_dictionary[
        PATHS_COLUMN_NAME
    ] = list_of_paths

    paths_and_leaves_dictionary[
        LEAVES_COLUMN_NAME
    ] = list_of_leaves

    paths_and_leaves_table = (
        DataFrame.from_dict(
            paths_and_leaves_dictionary
        )
    )

    path_analysis_master_table_with_leaves = left_merge_dataframes(
        master_dataframe=full_dependencies_path_analysis_master_table,
        master_dataframe_key_columns=[
            PATHS_COLUMN_NAME
        ],
        merge_suffixes=["1", "2"],
        foreign_key_dataframe=paths_and_leaves_table,
        foreign_key_dataframe_fk_columns=[
            PATHS_COLUMN_NAME
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            LEAVES_COLUMN_NAME: LEAVES_COLUMN_NAME
        },
    )

    path_analysis_master_table_with_leaves_renaming_dictionary = {
        PATHS_COLUMN_NAME: PATHS_COLUMN_NAME,
        PATH_LEVEL_DEPTH_COLUMN_NAME: PATH_LEVEL_DEPTH_COLUMN_NAME,
        LEAVES_COLUMN_NAME: LEAVES_COLUMN_NAME,
    }

    path_analysis_master_table_with_leaves = dataframe_filter_and_rename(
        dataframe=path_analysis_master_table_with_leaves,
        filter_and_rename_dictionary=path_analysis_master_table_with_leaves_renaming_dictionary,
    )

    return path_analysis_master_table_with_leaves


def __add_leaf_names_and_types_to_path_analysis_master_table(
    full_dependencies_path_analysis_master_table: DataFrame,
    ea_classifiers: DataFrame,
) -> DataFrame:
    foreign_key_name_column_names = {
        EA_OBJECT_NAME_COLUMN_NAME: EA_OBJECT_NAME_COLUMN_NAME,
        EA_OBJECT_TYPE_COLUMN_NAME: EA_OBJECT_TYPE_COLUMN_NAME,
    }

    data_visualisation_table_with_object_information = left_merge_dataframes(
        master_dataframe=full_dependencies_path_analysis_master_table,
        master_dataframe_key_columns=[
            LEAVES_COLUMN_NAME
        ],
        merge_suffixes=["1", "2"],
        foreign_key_dataframe=ea_classifiers,
        foreign_key_dataframe_fk_columns=[
            NF_UUIDS_COLUMN_NAME
        ],
        foreign_key_dataframe_other_column_rename_dictionary=foreign_key_name_column_names,
    )

    data_visualisation_table_with_object_information_dictionary = {
        PATHS_COLUMN_NAME: PATHS_COLUMN_NAME,
        PATH_LEVEL_DEPTH_COLUMN_NAME: PATH_LEVEL_DEPTH_COLUMN_NAME,
        LEAVES_COLUMN_NAME: LEAVES_COLUMN_NAME,
        EA_OBJECT_NAME_COLUMN_NAME: LEAVES_NAME_COLUMN_NAME,
        EA_OBJECT_TYPE_COLUMN_NAME: LEAVES_TYPE_COLUMN_NAME,
    }

    full_dependencies_path_analysis_master_table = dataframe_filter_and_rename(
        dataframe=data_visualisation_table_with_object_information,
        filter_and_rename_dictionary=data_visualisation_table_with_object_information_dictionary,
    )

    return full_dependencies_path_analysis_master_table


def __add_leaf_high_relation_type_to_path_analysis_master_table(
    full_dependencies_path_analysis_master_table: DataFrame,
) -> DataFrame:
    high_relation_type = [
        FIRST_CLASS_RELATION_NAME,
        FIRST_CLASS_RELATION_NAME,
        HIGH_ORDER_TYPE_RELATION_NAME,
        HIGH_ORDER_TYPE_RELATION_NAME,
    ]

    high_relation_type_conditions = [
        (
            full_dependencies_path_analysis_master_table[
                LEAVES_TYPE_COLUMN_NAME
            ]
            == PROXYCONNECTOR_TYPE_NAME
        ),
        (
            full_dependencies_path_analysis_master_table[
                LEAVES_TYPE_COLUMN_NAME
            ]
            == ASSOCIATION_TYPE_NAME
        ),
        (
            full_dependencies_path_analysis_master_table[
                LEAVES_TYPE_COLUMN_NAME
            ]
            == CLASS_TYPE_NAME
        ),
        (
            full_dependencies_path_analysis_master_table[
                LEAVES_TYPE_COLUMN_NAME
            ]
            == OBJECT_TYPE_NAME
        ),
    ]

    full_dependencies_path_analysis_master_table[
        RELATION_TYPE_COLUMN_NAME
    ] = numpy.select(
        high_relation_type_conditions,
        high_relation_type,
    )

    return full_dependencies_path_analysis_master_table
