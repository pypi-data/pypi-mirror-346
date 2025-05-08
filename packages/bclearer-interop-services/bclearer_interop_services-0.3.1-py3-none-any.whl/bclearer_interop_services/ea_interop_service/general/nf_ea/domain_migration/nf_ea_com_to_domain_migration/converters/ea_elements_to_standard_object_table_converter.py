from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.common.column_name_mappings.standard_classifier_to_nf_ea_com_column_name_bimapping import (
    get_nf_ea_com_column_name_to_standard_classifier_dictionary,
)


def convert_ea_elements_to_standard_object_table(
    nf_ea_com_universe: NfEaComUniverses,
    nf_ea_com_classifiers_collection_type: NfEaComCollectionTypes,
    standard_tables_dictionary: dict,
    input_object_table_name: str,
) -> dict:
    ea_elements = nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections[
        nf_ea_com_classifiers_collection_type
    ]

    standard_object_table_renaming_dictionary = (
        get_nf_ea_com_column_name_to_standard_classifier_dictionary()
    )

    nf_ea_com_table_filtered_and_renamed = dataframe_filter_and_rename(
        dataframe=ea_elements,
        filter_and_rename_dictionary=standard_object_table_renaming_dictionary,
    )

    standard_tables_dictionary[
        input_object_table_name
    ] = nf_ea_com_table_filtered_and_renamed

    return standard_tables_dictionary
