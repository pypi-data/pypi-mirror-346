from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.dataframes.nf_ea_com_table_appender import (
    append_nf_ea_com_table,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.common.column_name_mappings.standard_classifier_to_nf_ea_com_column_name_bimapping import (
    get_standard_classifier_to_nf_ea_com_column_name_dictionary,
)


def convert_standard_object_table_to_classifiers(
    standard_table_dictionary: dict,
    nf_ea_com_dictionary: dict,
    input_object_table_name: str,
    nf_ea_com_classifiers_collection_type: NfEaComCollectionTypes,
) -> dict:
    standard_object_table_renaming_dictionary = (
        get_standard_classifier_to_nf_ea_com_column_name_dictionary()
    )

    standard_object_table_filtered_and_renamed = dataframe_filter_and_rename(
        dataframe=standard_table_dictionary[
            input_object_table_name
        ],
        filter_and_rename_dictionary=standard_object_table_renaming_dictionary,
    )

    nf_ea_com_dictionary = append_nf_ea_com_table(
        nf_ea_com_dictionary=nf_ea_com_dictionary,
        new_nf_ea_com_collection=standard_object_table_filtered_and_renamed,
        nf_ea_com_collection_type=nf_ea_com_classifiers_collection_type,
    )

    return nf_ea_com_dictionary
