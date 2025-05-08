from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.domain_to_nf_ea_com_migration.convertors.tables.standard_connectors_converter import (
    convert_standard_linked_table_to_connectors,
)


def convert_connector_tables(
    standard_tables_dictionary: dict,
    connector_base_names: list,
    nf_ea_com_dictionary: dict,
) -> dict:
    for (
        connector_base_name
    ) in connector_base_names:
        nf_ea_com_dictionary = __convert_connector_table(
            standard_tables_dictionary=standard_tables_dictionary,
            connector_base_name=connector_base_name,
            nf_ea_com_dictionary=nf_ea_com_dictionary,
        )

    return nf_ea_com_dictionary


def __convert_connector_table(
    standard_tables_dictionary: dict,
    connector_base_name: str,
    nf_ea_com_dictionary: dict,
) -> dict:
    nf_ea_com_dictionary = convert_standard_linked_table_to_connectors(
        standard_table_dictionary=standard_tables_dictionary,
        nf_ea_com_dictionary=nf_ea_com_dictionary,
        input_linked_table_name=connector_base_name,
        nf_ea_com_connectors_collection_type=NfEaComCollectionTypes.EA_CONNECTORS,
        needs_uuid_generation=False,
    )

    return nf_ea_com_dictionary
