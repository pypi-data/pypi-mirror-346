from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_xref_column_types import (
    EaTXrefColumnTypes,
)
from pandas import DataFrame


def initialise_nf_ea_com_dictionary() -> (
    dict
):
    nf_ea_com_dictionary = dict()

    nf_ea_com_dictionary[
        NfEaComCollectionTypes.EA_PACKAGES
    ] = DataFrame(
        columns=[
            NfColumnTypes.NF_UUIDS.column_name,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name,
            NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT.column_name,
            NfEaComColumnTypes.PACKAGES_VIEW_TYPE.column_name,
        ]
    )

    nf_ea_com_dictionary[
        NfEaComCollectionTypes.EA_CLASSIFIERS
    ] = DataFrame(
        columns=[
            NfColumnTypes.NF_UUIDS.column_name,
            NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE.column_name,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name,
            NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT.column_name,
            NfEaComColumnTypes.ELEMENTS_CLASSIFIER.column_name,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NOTES.column_name,
        ]
    )

    nf_ea_com_dictionary[
        NfEaComCollectionTypes.EA_ATTRIBUTES
    ] = DataFrame(
        columns=[
            NfColumnTypes.NF_UUIDS.column_name,
            NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name,
            NfEaComColumnTypes.ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER.column_name,
            NfEaComColumnTypes.ELEMENT_COMPONENTS_UML_VISIBILITY_KIND.column_name,
            NfEaComColumnTypes.ELEMENT_COMPONENTS_TYPE.column_name,
            NfEaComColumnTypes.ELEMENT_COMPONENTS_DEFAULT.column_name,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name,
        ]
    )

    nf_ea_com_dictionary[
        NfEaComCollectionTypes.EA_CONNECTORS
    ] = DataFrame(
        columns=[
            NfColumnTypes.NF_UUIDS.column_name,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name,
        ]
    )

    nf_ea_com_dictionary[
        NfEaComCollectionTypes.EA_CONNECTORS_PC
    ] = DataFrame(
        columns=[
            NfColumnTypes.NF_UUIDS.column_name,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name,
        ]
    )

    nf_ea_com_dictionary[
        NfEaComCollectionTypes.EA_STEREOTYPE_GROUPS
    ] = DataFrame(
        columns=[
            NfColumnTypes.NF_UUIDS.column_name,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name,
        ]
    )

    nf_ea_com_dictionary[
        NfEaComCollectionTypes.EA_STEREOTYPES
    ] = DataFrame(
        columns=[
            NfColumnTypes.NF_UUIDS.column_name,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name,
        ]
    )

    nf_ea_com_dictionary[
        NfEaComCollectionTypes.STEREOTYPE_USAGE
    ] = DataFrame(
        columns=[
            EaTXrefColumnTypes.T_XREF_CLIENT_EA_GUIDS.nf_column_name,
            "stereotype_guids",
            NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS.column_name,
            "stereotype_nf_uuids",
        ]
    )

    nf_ea_com_dictionary[
        "ea_attributes_order"
    ] = DataFrame(
        columns=[
            NfColumnTypes.NF_UUIDS.column_name,
            "naming_space_names",
            "attribute_order",
        ]
    )

    return nf_ea_com_dictionary
