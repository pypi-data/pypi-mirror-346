from xml.etree.ElementTree import (
    Element,
    SubElement,
)

from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.common_knowledge.maps.ea_guids_to_ea_identifiers_for_objects_mappings import (
    EaGuidsToEaIdentifiersForObjectsMappings,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.nf_ea_xml_adders.nf_ea_xml_add_helpers import (
    add_xml_row_element_to_xml_table_element,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.maps.nf_uuids_to_ea_guids_mappings import (
    NfUuidsToEaGuidsMappings,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_attribute_column_types import (
    EaTAttributeColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_new_uuid,
)
from pandas import DataFrame


def add_ea_attributes_to_xml_root_element(
    ea_attributes: DataFrame,
    ea_classifiers: DataFrame,
    xml_root: Element,
    start_ea_identifier: int,
) -> Element:
    nf_uuid_column = (
        NfColumnTypes.NF_UUIDS.column_name
    )

    object_name_column = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name
    )

    name_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name
    )

    default_column_name = (
        NfEaComColumnTypes.ELEMENT_COMPONENTS_DEFAULT.column_name
    )

    containing_classifier_column_name = (
        NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name
    )

    classifying_classifier_column_name = (
        NfEaComColumnTypes.ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER.column_name
    )

    nf_uuids_to_classifier_names_dataframe = DataFrame(
        ea_classifiers[
            [
                nf_uuid_column,
                object_name_column,
            ]
        ]
    )

    nf_uuids_to_classifier_names_map = nf_uuids_to_classifier_names_dataframe.set_index(
        nf_uuid_column
    )[
        object_name_column
    ].to_dict()

    xml_element_for_ea_attributes = (
        SubElement(xml_root, "Table")
    )

    xml_element_for_ea_attributes.set(
        "name",
        EaCollectionTypes.T_ATTRIBUTE.collection_name,
    )

    for (
        index,
        ea_attribute_row,
    ) in ea_attributes.iterrows():
        __add_ea_attribute_to_xml_tree(
            nf_uuids_to_classifier_names_map=nf_uuids_to_classifier_names_map,
            ea_attribute_identifier=start_ea_identifier
            + int(index),
            xml_element_for_ea_attributes=xml_element_for_ea_attributes,
            ea_attribute_value=ea_attribute_row[
                name_column_name
            ],
            ea_attribute_default=ea_attribute_row[
                default_column_name
            ],
            ea_attribute_container_nf_uuid=ea_attribute_row[
                containing_classifier_column_name
            ],
            ea_attribute_classifier_nf_uuid=ea_attribute_row[
                classifying_classifier_column_name
            ],
        )

    return xml_root


def __add_ea_attribute_to_xml_tree(
    nf_uuids_to_classifier_names_map: dict,
    ea_attribute_identifier: int,
    ea_attribute_value: str,
    ea_attribute_default: str,
    ea_attribute_classifier_nf_uuid: str,
    ea_attribute_container_nf_uuid: str,
    xml_element_for_ea_attributes: Element,
):
    try:
        ea_attribute_classifier_ea_guid = NfUuidsToEaGuidsMappings.get_ea_guid(
            ea_attribute_classifier_nf_uuid
        )

    except:
        ea_attribute_classifier_ea_guid = (
            ""
        )

    try:
        ea_attribute_classifier_id = EaGuidsToEaIdentifiersForObjectsMappings.map.get_ea_identifier(
            ea_attribute_classifier_ea_guid
        )

    except:
        ea_attribute_classifier_id = (
            None
        )

    try:
        ea_attribute_classifier_name = nf_uuids_to_classifier_names_map[
            ea_attribute_classifier_nf_uuid
        ]

    except:
        ea_attribute_classifier_name = (
            ""
        )

    ea_attribute_container_ea_guid = NfUuidsToEaGuidsMappings.get_ea_guid(
        ea_attribute_container_nf_uuid
    )

    ea_attribute_container_id = EaGuidsToEaIdentifiersForObjectsMappings.map.get_ea_identifier(
        ea_attribute_container_ea_guid
    )

    ea_attribute_guid = (
        "{" + create_new_uuid() + "}"
    )

    if (
        ea_attribute_default
        == DEFAULT_NULL_VALUE
    ):
        ea_attribute_default = ""

    names_to_values_map = {
        EaTAttributeColumnTypes.T_ATTRIBUTE_IDS.column_name: ea_attribute_identifier,
        EaTAttributeColumnTypes.T_ATTRIBUTE_OBJECT_IDS.column_name: ea_attribute_container_id,
        "Object_Type": "Attribute",
        EaTAttributeColumnTypes.T_ATTRIBUTE_TYPES.column_name: ea_attribute_classifier_name,
        EaTAttributeColumnTypes.T_ATTRIBUTE_NAMES.column_name: ea_attribute_value,
        EaTAttributeColumnTypes.T_ATTRIBUTE_DEFAULTS.column_name: ea_attribute_default,
        EaTAttributeColumnTypes.T_ATTRIBUTE_EA_GUIDS.column_name: ea_attribute_guid,
        EaTAttributeColumnTypes.T_ATTRIBUTE_CLASSIFIER_T_OBJECT_IDS.column_name: ea_attribute_classifier_id,
    }

    xml_extensions_map = {
        EaTAttributeColumnTypes.T_ATTRIBUTE_OBJECT_IDS.column_name: ea_attribute_container_ea_guid,
        EaTAttributeColumnTypes.T_ATTRIBUTE_CLASSIFIER_T_OBJECT_IDS.column_name: ea_attribute_classifier_ea_guid,
    }

    add_xml_row_element_to_xml_table_element(
        xml_element_for_table=xml_element_for_ea_attributes,
        xml_column_names_to_values_map=names_to_values_map,
        xml_extensions_map=xml_extensions_map,
    )

    EaGuidsToEaIdentifiersForObjectsMappings.map.add_single_map(
        ea_guid=ea_attribute_guid,
        ea_identifier=ea_attribute_identifier,
    )
