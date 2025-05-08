from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.dataframes.nf_ea_com_table_appender import (
    append_nf_ea_com_table,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.nf_domains.standard_attribute_table_column_types import (
    StandardAttributeTableColumnTypes,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_new_uuid,
)


def convert_standard_attribute_table_to_attributes(
    standard_table_dictionary: dict,
    nf_ea_com_dictionary: dict,
    input_attribute_table_name: str,
    ea_attributes_collection_type: NfEaComCollectionTypes,
) -> dict:
    attribute_table_column_names_to_ea_attributes_column_names_dictionary = {
        StandardAttributeTableColumnTypes.ATTRIBUTED_OBJECT_UUIDS.column_name: NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name,
        StandardAttributeTableColumnTypes.ATTRIBUTE_TYPE_UUIDS.column_name: NfEaComColumnTypes.ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER.column_name,
        StandardAttributeTableColumnTypes.UML_VISIBILITY_KIND.column_name: NfEaComColumnTypes.ELEMENT_COMPONENTS_UML_VISIBILITY_KIND.column_name,
        StandardAttributeTableColumnTypes.ATTRIBUTE_VALUES.column_name: NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name,
    }

    attribute_table = (
        standard_table_dictionary[
            input_attribute_table_name
        ]
    )

    attribute_table_filtered_for_ea_attributes = dataframe_filter_and_rename(
        dataframe=attribute_table,
        filter_and_rename_dictionary=attribute_table_column_names_to_ea_attributes_column_names_dictionary,
    )

    ea_attributes_nf_uuids_column_name = (
        NfColumnTypes.NF_UUIDS.column_name
    )

    attribute_table_filtered_for_ea_attributes[
        ea_attributes_nf_uuids_column_name
    ] = attribute_table_filtered_for_ea_attributes.apply(
        lambda row: create_new_uuid(),
        axis=1,
    )

    nf_ea_com_dictionary = append_nf_ea_com_table(
        nf_ea_com_dictionary=nf_ea_com_dictionary,
        new_nf_ea_com_collection=attribute_table_filtered_for_ea_attributes,
        nf_ea_com_collection_type=ea_attributes_collection_type,
    )

    return nf_ea_com_dictionary
