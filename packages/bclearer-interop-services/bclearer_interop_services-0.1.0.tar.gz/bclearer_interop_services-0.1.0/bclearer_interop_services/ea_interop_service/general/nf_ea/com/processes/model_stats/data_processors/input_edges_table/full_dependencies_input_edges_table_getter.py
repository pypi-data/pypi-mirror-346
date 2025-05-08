from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.constants import (
    DEPENDENT_COLUMN_NAME,
    IMPLICIT_DEPENDENCY_NAME,
    PROVIDER_COLUMN_NAME,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.data_processors.input_edges_table.input_edges_base_table_human_readable_fields_adder import (
    add_human_readable_fields_to_input_edges_base_table,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_connector_types import (
    EaConnectorTypes,
)
from pandas import DataFrame


def get_full_dependencies_input_edges_table(
    ea_full_dependencies: DataFrame,
    ea_classifiers: DataFrame,
    ea_connectors: DataFrame,
) -> DataFrame:
    full_dependencies_input_edges_base_table = __get_full_dependencies_input_edges_base_table(
        ea_full_dependencies=ea_full_dependencies,
        ea_connectors=ea_connectors,
    )

    full_dependencies_input_edges_human_readable_table = add_human_readable_fields_to_input_edges_base_table(
        input_edges_base_table=full_dependencies_input_edges_base_table,
        ea_classifiers=ea_classifiers,
    )

    return full_dependencies_input_edges_human_readable_table


def __get_full_dependencies_input_edges_base_table(
    ea_full_dependencies: DataFrame,
    ea_connectors: DataFrame,
) -> DataFrame:
    full_dependencies_input_edges_base_table = dataframe_filter_and_rename(
        dataframe=ea_full_dependencies,
        filter_and_rename_dictionary={
            DEPENDENT_COLUMN_NAME: NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name,
            PROVIDER_COLUMN_NAME: NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name,
        },
    )

    full_dependencies_input_edges_base_table = left_merge_dataframes(
        master_dataframe=full_dependencies_input_edges_base_table,
        master_dataframe_key_columns=[
            NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name,
            NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name,
        ],
        merge_suffixes=["1", "2"],
        foreign_key_dataframe=ea_connectors,
        foreign_key_dataframe_fk_columns=[
            NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name,
            NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name,
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name: NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name,
            NfColumnTypes.NF_UUIDS.column_name: NfColumnTypes.NF_UUIDS.column_name,
        },
    )

    full_dependencies_input_edges_base_table.loc[
        full_dependencies_input_edges_base_table[
            NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name
        ]
        != EaConnectorTypes.DEPENDENCY.type_name,
        NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name,
    ] = IMPLICIT_DEPENDENCY_NAME

    return full_dependencies_input_edges_base_table
