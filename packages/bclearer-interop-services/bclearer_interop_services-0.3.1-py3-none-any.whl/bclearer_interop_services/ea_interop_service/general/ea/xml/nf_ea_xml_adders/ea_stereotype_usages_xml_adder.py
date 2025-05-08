from xml.etree.ElementTree import (
    Element,
    SubElement,
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
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_xref_column_types import (
    EaTXrefColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_new_uuid,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from pandas import DataFrame


def add_ea_stereotype_usages_to_xml_root_element(
    stereotype_usage_with_names: DataFrame,
    xml_root: Element,
) -> Element:
    xml_element_for_stereotype_usages = SubElement(
        xml_root, "Table"
    )

    xml_element_for_stereotype_usages.set(
        "name",
        EaCollectionTypes.T_XREF.collection_name,
    )

    client_nf_uuid_column_name = (
        NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS.column_name
    )

    stereotype_nf_uuid_column_name = (
        "stereotype_nf_uuids"
    )

    stereotype_name_column_name = (
        NfEaComColumnTypes.STEREOTYPE_NAMES.column_name
    )

    stereotype_property_type_column_name = (
        NfEaComColumnTypes.STEREOTYPE_PROPERTY_TYPE.column_name
    )

    stereotype_usage_with_names_copy = (
        stereotype_usage_with_names.copy()
    )

    if (
        stereotype_property_type_column_name
        not in stereotype_usage_with_names_copy.columns
    ):
        stereotype_usage_with_names_copy[
            stereotype_property_type_column_name
        ] = str()

    for (
        index,
        stereotype_usage_row,
    ) in (
        stereotype_usage_with_names_copy.iterrows()
    ):
        __add_ea_stereotype_usage_to_xml_tree(
            client_nf_uuid=stereotype_usage_row[
                client_nf_uuid_column_name
            ],
            stereotype_nf_uuid=stereotype_usage_row[
                stereotype_nf_uuid_column_name
            ],
            stereotype_name=stereotype_usage_row[
                stereotype_name_column_name
            ],
            stereotype_property_type=stereotype_usage_row[
                stereotype_property_type_column_name
            ],
            xml_element_for_stereotype_usages=xml_element_for_stereotype_usages,
        )

    return xml_root


def __add_ea_stereotype_usage_to_xml_tree(
    client_nf_uuid: str,
    stereotype_nf_uuid: str,
    stereotype_name: str,
    stereotype_property_type: str,
    xml_element_for_stereotype_usages: Element,
):
    if not isinstance(
        stereotype_nf_uuid, str
    ):
        log_message(
            message="Cannot find stereotype of stereotype_usage for client: "
            + client_nf_uuid
        )

        return

    client_ea_guid = NfUuidsToEaGuidsMappings.get_ea_guid(
        client_nf_uuid
    )

    stereotype_ea_guid = NfUuidsToEaGuidsMappings.get_ea_guid(
        stereotype_nf_uuid
    )

    ea_xref_guid = (
        "{" + create_new_uuid() + "}"
    )

    stereotype_usage_description = (
        "@STEREO"
        + ";"
        + "Name="
        + stereotype_name
        + ";"
        + "GUID="
        + stereotype_ea_guid
        + ";"
        + "@ENDSTEREO"
    )

    names_to_values_map = {
        EaTXrefColumnTypes.T_XREF_EA_GUIDS.column_name: ea_xref_guid,
        EaTXrefColumnTypes.T_XREF_CLIENT_EA_GUIDS.column_name: client_ea_guid,
        EaTXrefColumnTypes.T_XREF_DESCRIPTIONS.column_name: stereotype_usage_description,
        EaTXrefColumnTypes.T_XREF_NAMES.column_name: "Stereotypes",
        EaTXrefColumnTypes.T_XREF_TYPES.column_name: stereotype_property_type,
    }

    add_xml_row_element_to_xml_table_element(
        xml_element_for_table=xml_element_for_stereotype_usages,
        xml_column_names_to_values_map=names_to_values_map,
    )
