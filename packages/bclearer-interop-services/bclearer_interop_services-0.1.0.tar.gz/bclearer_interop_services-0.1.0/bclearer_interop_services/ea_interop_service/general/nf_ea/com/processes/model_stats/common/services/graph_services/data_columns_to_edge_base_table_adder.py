from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.constants import (
    STEREOTYPE_NAMES_COLUMN_NAME,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services_promote_to_nf_common.dataframe_into_dictionary_of_rows_converter import (
    convert_dataframe_into_dictionary_of_rows,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services_promote_to_nf_common.dictionary_mergers import (
    left_merge_dictionaries_of_rows,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.nf_domains.standard_connector_table_column_types import (
    StandardConnectorTableColumnTypes,
)
from pandas import DataFrame


def add_data_columns_to_edge_base_table(
    edge_base_table: DataFrame,
    ea_connectors: DataFrame,
    ea_stereotypes: DataFrame,
    ea_stereotype_usage: DataFrame,
) -> DataFrame:
    edge_base_table_dictionary = convert_dataframe_into_dictionary_of_rows(
        dataframe=edge_base_table
    )

    ea_connectors_dictionary = convert_dataframe_into_dictionary_of_rows(
        dataframe=ea_connectors
    )

    ea_stereotypes_dictionary = convert_dataframe_into_dictionary_of_rows(
        dataframe=ea_stereotypes
    )

    ea_stereotype_usage_dictionary = convert_dataframe_into_dictionary_of_rows(
        dataframe=ea_stereotype_usage
    )

    edges_table_with_ea_connectors_data_dictionary = left_merge_dictionaries_of_rows(
        master_dictionary=edge_base_table_dictionary,
        master_dictionary_key_column=NfColumnTypes.NF_UUIDS.column_name,
        foreign_key_dictionary=ea_connectors_dictionary,
        foreign_key_dictionary_fk_column=NfColumnTypes.NF_UUIDS.column_name,
        foreign_key_dictionary_other_column_rename_dictionary={
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NOTES.column_name: NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NOTES.column_name,
        },
    )

    ea_stereotype_usage_with_stereotype_names_dictionary = left_merge_dictionaries_of_rows(
        master_dictionary=ea_stereotype_usage_dictionary,
        master_dictionary_key_column=StandardConnectorTableColumnTypes.STEREOTYPE_NF_UUIDS.column_name,
        foreign_key_dictionary=ea_stereotypes_dictionary,
        foreign_key_dictionary_fk_column=NfColumnTypes.NF_UUIDS.column_name,
        foreign_key_dictionary_other_column_rename_dictionary={
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name
        },
    )

    edges_table_with_data_columns_dictionary = left_merge_dictionaries_of_rows(
        master_dictionary=edges_table_with_ea_connectors_data_dictionary,
        master_dictionary_key_column=NfColumnTypes.NF_UUIDS.column_name,
        foreign_key_dictionary=ea_stereotype_usage_with_stereotype_names_dictionary,
        foreign_key_dictionary_fk_column=NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS.column_name,
        foreign_key_dictionary_other_column_rename_dictionary={
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: STEREOTYPE_NAMES_COLUMN_NAME
        },
    )

    edges_table_with_data_columns = DataFrame.from_dict(
        data=edges_table_with_data_columns_dictionary,
        orient="index",
    )

    edges_table_with_data_columns.fillna(
        value=DEFAULT_NULL_VALUE,
        inplace=True,
    )

    edges_table_with_data_columns.drop_duplicates(
        ignore_index=True, inplace=True
    )

    all_column_names_but_stereotype_names = (
        edges_table_with_data_columns.columns.tolist()
    )

    all_column_names_but_stereotype_names.remove(
        STEREOTYPE_NAMES_COLUMN_NAME
    )

    edges_table_with_data_columns = (
        edges_table_with_data_columns.groupby(
            all_column_names_but_stereotype_names
        )[
            STEREOTYPE_NAMES_COLUMN_NAME
        ]
        .apply(",".join)
        .reset_index()
    )

    return edges_table_with_data_columns
