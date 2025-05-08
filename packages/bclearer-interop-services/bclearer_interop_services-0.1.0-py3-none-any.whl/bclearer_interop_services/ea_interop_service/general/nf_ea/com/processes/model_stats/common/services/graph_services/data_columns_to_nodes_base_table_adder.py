from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
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
    PACKAGE_NAMES_COLUMN_NAME,
    STEREOTYPE_NAMES_COLUMN_NAME,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.nf_domains.standard_connector_table_column_types import (
    StandardConnectorTableColumnTypes,
)
from pandas import DataFrame


def add_data_columns_to_nodes_base_table(
    nodes_base_table: DataFrame,
    ea_classifiers: DataFrame,
    ea_packages: DataFrame,
    ea_stereotypes: DataFrame,
    ea_stereotype_usage: DataFrame,
) -> DataFrame:
    ea_classifiers_with_package_names = left_merge_dataframes(
        master_dataframe=ea_classifiers,
        master_dataframe_key_columns=[
            NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT.column_name
        ],
        merge_suffixes=["1", "2"],
        foreign_key_dataframe=ea_packages,
        foreign_key_dataframe_fk_columns=[
            NfColumnTypes.NF_UUIDS.column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: PACKAGE_NAMES_COLUMN_NAME
        },
    )

    renaming_dictionary = {
        NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE.column_name: NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE.column_name,
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name,
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NOTES.column_name: NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NOTES.column_name,
        PACKAGE_NAMES_COLUMN_NAME: PACKAGE_NAMES_COLUMN_NAME,
    }

    nodes_table_with_ea_classifiers_data = left_merge_dataframes(
        master_dataframe=nodes_base_table,
        master_dataframe_key_columns=[
            NfColumnTypes.NF_UUIDS.column_name
        ],
        merge_suffixes=["1", "2"],
        foreign_key_dataframe=ea_classifiers_with_package_names,
        foreign_key_dataframe_fk_columns=[
            NfColumnTypes.NF_UUIDS.column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary=renaming_dictionary,
    )

    ea_stereotype_usage_with_stereotype_names = left_merge_dataframes(
        master_dataframe=ea_stereotype_usage,
        master_dataframe_key_columns=[
            StandardConnectorTableColumnTypes.STEREOTYPE_NF_UUIDS.column_name
        ],
        merge_suffixes=["1", "2"],
        foreign_key_dataframe=ea_stereotypes,
        foreign_key_dataframe_fk_columns=[
            NfColumnTypes.NF_UUIDS.column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name
        },
    )

    nodes_table_with_stereotypes_data = left_merge_dataframes(
        master_dataframe=nodes_table_with_ea_classifiers_data,
        master_dataframe_key_columns=[
            NfColumnTypes.NF_UUIDS.column_name
        ],
        merge_suffixes=["1", "2"],
        foreign_key_dataframe=ea_stereotype_usage_with_stereotype_names,
        foreign_key_dataframe_fk_columns=[
            NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS.column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: STEREOTYPE_NAMES_COLUMN_NAME
        },
    )

    nodes_table_with_stereotypes_data.fillna(
        value=DEFAULT_NULL_VALUE,
        inplace=True,
    )

    nodes_table_with_data_columns = nodes_table_with_stereotypes_data.drop_duplicates(
        ignore_index=True
    )

    all_column_names_but_stereotype_names = (
        nodes_table_with_data_columns.columns.tolist()
    )

    if (
        nodes_table_with_data_columns.empty
    ):
        nodes_table_with_data_columns = DataFrame(
            columns=all_column_names_but_stereotype_names
        )

        return nodes_table_with_data_columns

    all_column_names_but_stereotype_names.remove(
        STEREOTYPE_NAMES_COLUMN_NAME
    )

    nodes_table_with_data_columns = (
        nodes_table_with_data_columns.groupby(
            all_column_names_but_stereotype_names
        )[
            STEREOTYPE_NAMES_COLUMN_NAME
        ]
        .apply(",".join)
        .reset_index()
    )

    return nodes_table_with_data_columns
