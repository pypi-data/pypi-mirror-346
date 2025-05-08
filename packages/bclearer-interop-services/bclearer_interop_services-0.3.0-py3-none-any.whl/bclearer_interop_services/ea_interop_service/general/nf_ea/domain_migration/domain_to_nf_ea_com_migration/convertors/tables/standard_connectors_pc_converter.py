import numpy
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
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_connector_types import (
    EaConnectorTypes,
)


def convert_standard_typed_linked_table_to_connectors_pc(
    standard_table_dictionary: dict,
    nf_ea_com_dictionary: dict,
    input_linked_table_name: str,
    input_table_type_uuids_column_name: str,
    nf_ea_com_connectors_pc_collection_type: NfEaComCollectionTypes,
    nf_ea_com_classifiers_collection_type: NfEaComCollectionTypes,
) -> dict:
    standard_typed_linked_table = (
        standard_table_dictionary[
            input_linked_table_name
        ]
    )

    ea_connectors_pc_dataframe = standard_typed_linked_table.merge(
        right=nf_ea_com_dictionary[
            nf_ea_com_classifiers_collection_type
        ],
        how="left",
        left_on=NfColumnTypes.NF_UUIDS.column_name,
        right_on=NfEaComColumnTypes.ELEMENTS_CLASSIFIER.column_name,
    )

    ea_connectors_pc_dataframe_renaming_dictionary = {
        NfColumnTypes.NF_UUIDS.column_name
        + "_y": NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name,
        input_table_type_uuids_column_name: NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name,
    }

    ea_connectors_pc_dataframe_filtered_and_renamed = dataframe_filter_and_rename(
        dataframe=ea_connectors_pc_dataframe,
        filter_and_rename_dictionary=ea_connectors_pc_dataframe_renaming_dictionary,
    )

    ea_connectors_pc_dataframe_filtered_and_renamed[
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name
    ] = numpy.nan

    ea_connectors_pc_dataframe_filtered_and_renamed[
        NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name
    ] = (
        EaConnectorTypes.DEPENDENCY.type_name
    )

    nf_ea_com_dictionary = append_nf_ea_com_table(
        nf_ea_com_dictionary=nf_ea_com_dictionary,
        new_nf_ea_com_collection=ea_connectors_pc_dataframe_filtered_and_renamed,
        nf_ea_com_collection_type=nf_ea_com_connectors_pc_collection_type,
    )

    return nf_ea_com_dictionary
