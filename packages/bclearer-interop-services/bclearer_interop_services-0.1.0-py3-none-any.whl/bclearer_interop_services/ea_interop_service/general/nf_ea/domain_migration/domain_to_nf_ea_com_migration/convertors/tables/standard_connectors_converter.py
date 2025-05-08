from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.dataframes.nf_ea_com_table_appender import (
    append_nf_ea_com_table,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.common.column_name_mappings.standard_connector_to_nf_ea_com_column_name_bimapping import (
    get_standard_connector_to_nf_ea_com_column_name_dictionary,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_new_uuid,
)


def convert_standard_linked_table_to_connectors(
    standard_table_dictionary: dict,
    nf_ea_com_dictionary: dict,
    input_linked_table_name: str,
    nf_ea_com_connectors_collection_type: NfEaComCollectionTypes,
    needs_uuid_generation: bool,
) -> dict:
    standard_linked_table_dataframe = (
        standard_table_dictionary[
            input_linked_table_name
        ]
    )

    if needs_uuid_generation:
        standard_linked_table_dataframe[
            NfColumnTypes.NF_UUIDS.column_name
        ] = standard_linked_table_dataframe.apply(
            lambda row: create_new_uuid(),
            axis=1,
        )

    ea_connector_dataframe_renaming_dictionary = (
        get_standard_connector_to_nf_ea_com_column_name_dictionary()
    )

    standard_linked_table_filtered_and_renamed_for_connectors = dataframe_filter_and_rename(
        dataframe=standard_linked_table_dataframe,
        filter_and_rename_dictionary=ea_connector_dataframe_renaming_dictionary,
    )

    nf_ea_com_dictionary = append_nf_ea_com_table(
        nf_ea_com_dictionary=nf_ea_com_dictionary,
        new_nf_ea_com_collection=standard_linked_table_filtered_and_renamed_for_connectors,
        nf_ea_com_collection_type=nf_ea_com_connectors_collection_type,
    )

    return nf_ea_com_dictionary
