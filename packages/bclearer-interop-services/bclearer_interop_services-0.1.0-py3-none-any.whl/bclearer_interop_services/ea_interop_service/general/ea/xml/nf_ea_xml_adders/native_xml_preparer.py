from xml.etree.ElementTree import (
    Element,
    SubElement,
)

from bclearer_interop_services.ea_interop_service.general.ea.xml.common_knowledge.maps.ea_guids_to_ea_identifiers_for_objects_mappings import (
    EaGuidsToEaIdentifiersForObjectsMappings,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.common_knowledge.maps.ea_guids_to_ea_identifiers_for_packages_mappings import (
    EaGuidsToEaIdentifiersForPackagesMappings,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.nf_ea_xml_adders.nf_ea_xml_add_helpers import (
    add_xml_row_element_to_xml_table_element,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_package_column_types import (
    EaTPackageColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_new_uuid,
)

ROOT_PACKAGE_NAME = (
    "Native XML Import Package"
)


def prepare_native_xml(
    object_ea_identifier_for_import_package: int,
    package_ea_identifier_for_import_package: int,
    default_model_package_ea_guid: str,
) -> tuple:
    (
        xml_root_element,
        xml_root_element_guid,
    ) = __set_xml_root_element(
        default_model_package_ea_guid=default_model_package_ea_guid
    )

    xml_element_for_packages = __add_import_package(
        xml_root_element=xml_root_element,
        xml_root_element_guid=xml_root_element_guid,
        object_ea_identifier=object_ea_identifier_for_import_package,
        package_ea_identifier=package_ea_identifier_for_import_package,
        default_model_package_ea_guid=default_model_package_ea_guid,
    )

    return (
        xml_root_element,
        xml_root_element_guid,
        xml_element_for_packages,
    )


def __set_xml_root_element(
    default_model_package_ea_guid: str,
) -> tuple:
    xml_root_element = Element(
        "Package"
    )

    xml_root_element.set(
        "name", ROOT_PACKAGE_NAME
    )

    if (
        default_model_package_ea_guid
        is None
    ):
        xml_root_element_guid = (
            "{"
            + create_new_uuid()
            + "}"
        )
    else:
        xml_root_element_guid = default_model_package_ea_guid

    xml_root_element.set(
        "guid", xml_root_element_guid
    )

    return (
        xml_root_element,
        xml_root_element_guid,
    )


def __add_import_package(
    xml_root_element: Element,
    xml_root_element_guid: str,
    object_ea_identifier: int,
    package_ea_identifier: int,
    default_model_package_ea_guid: str,
) -> Element:
    xml_element_for_packages = (
        SubElement(
            xml_root_element, "Table"
        )
    )

    xml_element_for_packages.set(
        "name",
        EaCollectionTypes.T_PACKAGE.collection_name,
    )

    names_to_values_map = {
        EaTPackageColumnTypes.T_PACKAGE_IDS.column_name: package_ea_identifier,
        EaTPackageColumnTypes.T_PACKAGE_NAMES.column_name: ROOT_PACKAGE_NAME,
        EaTPackageColumnTypes.T_PACKAGE_EA_GUIDS.column_name: xml_root_element_guid,
    }

    add_xml_row_element_to_xml_table_element(
        xml_element_for_table=xml_element_for_packages,
        xml_column_names_to_values_map=names_to_values_map,
    )

    if (
        default_model_package_ea_guid
        is None
    ):
        EaGuidsToEaIdentifiersForObjectsMappings.map.add_single_map(
            ea_identifier=object_ea_identifier,
            ea_guid=xml_root_element_guid,
        )

        EaGuidsToEaIdentifiersForPackagesMappings.map.add_single_map(
            ea_identifier=package_ea_identifier,
            ea_guid=xml_root_element_guid,
        )

    return xml_element_for_packages
