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
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_element_types import (
    EaElementTypes,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_new_uuid,
)


def convert_typed_linked_table_to_classifiers_proxy_connectors(
    standard_table_dictionary: dict,
    nf_ea_com_dictionary: dict,
    input_linked_table_name: str,
    proxy_connectors_package_name: str,
    ea_packages_collection_type: NfEaComCollectionTypes,
    nf_ea_com_classifiers_collection_type: NfEaComCollectionTypes,
) -> dict:
    typed_linked_table = (
        standard_table_dictionary[
            input_linked_table_name
        ]
    )

    typed_linked_table_renaming_dictionary_for_proxy_connectors = {
        NfColumnTypes.NF_UUIDS.column_name: NfEaComColumnTypes.ELEMENTS_CLASSIFIER.column_name
    }

    typed_linked_table_filtered_and_renamed_for_proxy_connectors = dataframe_filter_and_rename(
        dataframe=typed_linked_table,
        filter_and_rename_dictionary=typed_linked_table_renaming_dictionary_for_proxy_connectors,
    )

    ea_packages_dataframe = (
        nf_ea_com_dictionary[
            ea_packages_collection_type
        ]
    )

    proxy_connectors_package_nf_uuid = (
        ea_packages_dataframe.loc[
            ea_packages_dataframe[
                NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name
            ]
            == proxy_connectors_package_name,
            NfColumnTypes.NF_UUIDS.column_name,
        ]
        .to_string(index=False)
        .strip()
    )

    typed_linked_table_filtered_and_renamed_for_proxy_connectors[
        NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE.column_name
    ] = (
        EaElementTypes.PROXY_CONNECTOR.type_name
    )

    typed_linked_table_filtered_and_renamed_for_proxy_connectors[
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name
    ] = (
        EaElementTypes.PROXY_CONNECTOR.type_name
    )

    typed_linked_table_filtered_and_renamed_for_proxy_connectors[
        NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT.column_name
    ] = proxy_connectors_package_nf_uuid

    ea_connectors_nf_uuids_column_name = (
        NfColumnTypes.NF_UUIDS.column_name
    )

    typed_linked_table_filtered_and_renamed_for_proxy_connectors[
        ea_connectors_nf_uuids_column_name
    ] = typed_linked_table_filtered_and_renamed_for_proxy_connectors.apply(
        lambda row: create_new_uuid(),
        axis=1,
    )

    nf_ea_com_dictionary = append_nf_ea_com_table(
        nf_ea_com_dictionary=nf_ea_com_dictionary,
        new_nf_ea_com_collection=typed_linked_table_filtered_and_renamed_for_proxy_connectors,
        nf_ea_com_collection_type=nf_ea_com_classifiers_collection_type,
    )

    return nf_ea_com_dictionary
