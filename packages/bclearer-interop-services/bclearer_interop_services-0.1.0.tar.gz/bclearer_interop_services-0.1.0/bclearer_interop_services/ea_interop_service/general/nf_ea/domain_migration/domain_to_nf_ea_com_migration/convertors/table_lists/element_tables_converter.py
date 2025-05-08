from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.domain_to_nf_ea_com_migration.convertors.tables.standard_classifiers_converter import (
    convert_standard_object_table_to_classifiers,
)


def convert_element_tables(
    standard_tables_dictionary: dict,
    element_base_names: list,
    nf_ea_com_dictionary: dict,
    collection_type: NfEaComCollectionTypes,
) -> dict:
    for (
        object_base_name
    ) in element_base_names:
        nf_ea_com_dictionary = __convert_element_table(
            standard_tables_dictionary=standard_tables_dictionary,
            object_base_name=object_base_name,
            nf_ea_com_dictionary=nf_ea_com_dictionary,
            collection_type=collection_type,
        )

    return nf_ea_com_dictionary


def __convert_element_table(
    standard_tables_dictionary: dict,
    object_base_name: str,
    nf_ea_com_dictionary: dict,
    collection_type: NfEaComCollectionTypes,
) -> dict:
    nf_ea_com_dictionary = convert_standard_object_table_to_classifiers(
        standard_table_dictionary=standard_tables_dictionary,
        nf_ea_com_dictionary=nf_ea_com_dictionary,
        input_object_table_name=object_base_name,
        nf_ea_com_classifiers_collection_type=collection_type,
    )

    return nf_ea_com_dictionary
