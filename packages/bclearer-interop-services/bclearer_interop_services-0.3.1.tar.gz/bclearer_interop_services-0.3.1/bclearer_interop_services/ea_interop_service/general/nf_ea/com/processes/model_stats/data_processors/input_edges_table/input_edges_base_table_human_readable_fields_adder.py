from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.constants import (
    SOURCE_NAME_COLUMN_NAME,
    TARGET_NAME_COLUMN_NAME,
)
from pandas import DataFrame


def add_human_readable_fields_to_input_edges_base_table(
    input_edges_base_table: DataFrame,
    ea_classifiers: DataFrame,
) -> DataFrame:
    input_edges_human_readable_table = __add_source_name_to_input_edges_table(
        input_edges_table=input_edges_base_table,
        ea_classifiers=ea_classifiers,
    )

    input_edges_human_readable_table = __add_target_name_column_to_input_edges_table(
        input_edges_table=input_edges_human_readable_table,
        ea_classifiers=ea_classifiers,
    )

    return (
        input_edges_human_readable_table
    )


def __add_source_name_to_input_edges_table(
    input_edges_table: DataFrame,
    ea_classifiers: DataFrame,
) -> DataFrame:
    input_edges_base_table_with_source_name = left_merge_dataframes(
        master_dataframe=input_edges_table,
        master_dataframe_key_columns=[
            NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name
        ],
        merge_suffixes=["1", "2"],
        foreign_key_dataframe=ea_classifiers,
        foreign_key_dataframe_fk_columns=[
            NfColumnTypes.NF_UUIDS.column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: SOURCE_NAME_COLUMN_NAME
        },
    )

    return input_edges_base_table_with_source_name


def __add_target_name_column_to_input_edges_table(
    input_edges_table: DataFrame,
    ea_classifiers: DataFrame,
) -> DataFrame:
    input_edges_base_table_with_target_name = left_merge_dataframes(
        master_dataframe=input_edges_table,
        master_dataframe_key_columns=[
            NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name
        ],
        merge_suffixes=["1", "2"],
        foreign_key_dataframe=ea_classifiers,
        foreign_key_dataframe_fk_columns=[
            NfColumnTypes.NF_UUIDS.column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: TARGET_NAME_COLUMN_NAME
        },
    )

    return input_edges_base_table_with_target_name
