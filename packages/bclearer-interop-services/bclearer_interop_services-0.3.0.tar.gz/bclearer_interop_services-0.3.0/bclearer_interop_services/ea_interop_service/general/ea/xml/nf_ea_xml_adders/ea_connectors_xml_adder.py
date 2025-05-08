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
from bclearer_interop_services.ea_interop_service.general.ea.xml.common_knowledge.maps.connector_types_to_destination_is_aggregate_mappings import (
    get_destination_is_aggregate_from_connector_type,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.common_knowledge.maps.connector_types_to_direction_strings_mappings import (
    get_direction_string_from_connector_type,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.common_knowledge.maps.ea_guids_to_ea_identifiers_for_connectors_mappings import (
    EaGuidsToEaIdentifiersForConnectorsMappings,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.common_knowledge.maps.ea_guids_to_ea_identifiers_for_objects_mappings import (
    EaGuidsToEaIdentifiersForObjectsMappings,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.nf_ea_xml_adders.nf_ea_xml_add_helpers import (
    add_xml_row_element_to_xml_table_element,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_additional_column_types import (
    NfEaComAdditionalColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.maps.nf_uuids_to_ea_guids_mappings import (
    NfUuidsToEaGuidsMappings,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_connector_column_types import (
    EaTConnectorColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from bclearer_interop_services.tuple_service.tuple_attribute_value_getter import (
    get_tuple_attribute_value_if_required,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_new_uuid,
)
from pandas import DataFrame


def add_ea_connectors_to_xml_root_element(
    ea_connectors: DataFrame,
    xml_root: Element,
    xml_element_for_connectors: Element,
    start_ea_identifier: int,
    stereotype_usage_with_names: DataFrame,
) -> tuple:
    if (
        xml_element_for_connectors
        is None
    ):
        xml_element_for_connectors = __create_xml_element_for_connectors(
            xml_root=xml_root
        )

    next_ea_identifier = (
        start_ea_identifier + 1
    )

    for (
        ea_connector_tuple
    ) in ea_connectors.itertuples():
        __add_ea_connector_to_xml_tree(
            ea_connector_tuple=ea_connector_tuple,
            ea_connector_identifier=next_ea_identifier,
            xml_element_for_connectors=xml_element_for_connectors,
            stereotype_usage_with_names=stereotype_usage_with_names,
        )

        next_ea_identifier += 1

    return (
        xml_root,
        xml_element_for_connectors,
        next_ea_identifier,
    )


def __create_xml_element_for_connectors(
    xml_root: Element,
) -> Element:
    xml_element_for_connectors = (
        SubElement(xml_root, "Table")
    )

    xml_element_for_connectors.set(
        "name",
        EaCollectionTypes.T_CONNECTOR.collection_name,
    )

    return xml_element_for_connectors


def __add_ea_connector_to_xml_tree(
    ea_connector_tuple: tuple,
    ea_connector_identifier: int,
    xml_element_for_connectors: Element,
    stereotype_usage_with_names: DataFrame,
):
    ea_connector_nf_uuid = get_tuple_attribute_value_if_required(
        owning_tuple=ea_connector_tuple,
        attribute_name=NfColumnTypes.NF_UUIDS.column_name,
    )

    original_ea_guid = get_tuple_attribute_value_if_required(
        owning_tuple=ea_connector_tuple,
        attribute_name=NfEaComAdditionalColumnTypes.ORIGINAL_EA_GUIDS.column_name,
    )

    ea_connector_name = get_tuple_attribute_value_if_required(
        owning_tuple=ea_connector_tuple,
        attribute_name=NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name,
    )

    ea_connector_notes = get_tuple_attribute_value_if_required(
        owning_tuple=ea_connector_tuple,
        attribute_name=NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NOTES.column_name,
    )

    ea_connector_type = get_tuple_attribute_value_if_required(
        owning_tuple=ea_connector_tuple,
        attribute_name=NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name,
    )

    ea_connector_supplier_nf_uuid = get_tuple_attribute_value_if_required(
        owning_tuple=ea_connector_tuple,
        attribute_name=NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name,
    )

    ea_connector_client_nf_uuid = get_tuple_attribute_value_if_required(
        owning_tuple=ea_connector_tuple,
        attribute_name=NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name,
    )

    ea_connector_supplier_ea_guid = NfUuidsToEaGuidsMappings.get_ea_guid(
        nf_uuid=ea_connector_supplier_nf_uuid
    )

    ea_connector_supplier_identifier = EaGuidsToEaIdentifiersForObjectsMappings.map.get_ea_identifier(
        ea_guid=ea_connector_supplier_ea_guid
    )

    ea_connector_client_ea_guid = NfUuidsToEaGuidsMappings.get_ea_guid(
        nf_uuid=ea_connector_client_nf_uuid
    )

    ea_connector_client_identifier = EaGuidsToEaIdentifiersForObjectsMappings.map.get_ea_identifier(
        ea_guid=ea_connector_client_ea_guid
    )

    ea_connector_destination_is_aggregate = get_destination_is_aggregate_from_connector_type(
        ea_connector_type
    )

    ea_connector_direction = get_direction_string_from_connector_type(
        ea_connector_type
    )

    if (
        original_ea_guid
        == DEFAULT_NULL_VALUE
    ):
        ea_connector_guid = (
            "{"
            + create_new_uuid()
            + "}"
        )

    else:
        ea_connector_guid = (
            original_ea_guid
        )

    if (
        ea_connector_name
        == DEFAULT_NULL_VALUE
    ):
        ea_connector_name = ""

    if (
        ea_connector_notes
        == DEFAULT_NULL_VALUE
    ):
        ea_connector_notes = ""

    stereotype_names = stereotype_usage_with_names[
        stereotype_usage_with_names[
            NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS.column_name
        ]
        == ea_connector_nf_uuid
    ][
        NfEaComColumnTypes.STEREOTYPE_NAMES.column_name
    ].values

    if len(stereotype_names) == 0:
        stereotype_name = ""
    else:
        stereotype_name = (
            stereotype_names[0]
        )

    names_to_values_map = {
        EaTConnectorColumnTypes.T_CONNECTOR_IDS.column_name: ea_connector_identifier,
        EaTConnectorColumnTypes.T_CONNECTOR_TYPES.column_name: ea_connector_type,
        EaTConnectorColumnTypes.T_CONNECTOR_NAMES.column_name: ea_connector_name,
        EaTConnectorColumnTypes.T_CONNECTOR_NOTES.column_name: ea_connector_notes,
        EaTConnectorColumnTypes.T_CONNECTOR_EA_GUIDS.column_name: ea_connector_guid,
        EaTConnectorColumnTypes.T_CONNECTOR_START_OBJECT_IDS.column_name: ea_connector_supplier_identifier,
        EaTConnectorColumnTypes.T_CONNECTOR_END_OBJECT_IDS.column_name: ea_connector_client_identifier,
        EaTConnectorColumnTypes.T_CONNECTOR_DIRECTIONS.column_name: ea_connector_direction,
        EaTConnectorColumnTypes.T_CONNECTOR_STEREOTYPES.column_name: stereotype_name,
        EaTConnectorColumnTypes.T_CONNECTOR_DEST_IS_AGGREGATE.column_name: ea_connector_destination_is_aggregate,
    }

    xml_extensions_map = {
        EaTConnectorColumnTypes.T_CONNECTOR_START_OBJECT_IDS.column_name: ea_connector_supplier_ea_guid,
        EaTConnectorColumnTypes.T_CONNECTOR_END_OBJECT_IDS.column_name: ea_connector_client_ea_guid,
    }

    add_xml_row_element_to_xml_table_element(
        xml_element_for_table=xml_element_for_connectors,
        xml_column_names_to_values_map=names_to_values_map,
        xml_extensions_map=xml_extensions_map,
    )

    if (
        ea_connector_nf_uuid
        != DEFAULT_NULL_VALUE
    ):
        NfUuidsToEaGuidsMappings.add_single_map(
            nf_uuid=ea_connector_nf_uuid,
            ea_guid=ea_connector_guid,
        )

    EaGuidsToEaIdentifiersForConnectorsMappings.map.add_single_map(
        ea_guid=ea_connector_guid,
        ea_identifier=ea_connector_identifier,
    )
