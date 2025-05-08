from xml.etree.ElementTree import (
    Element,
)

from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
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
from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.maps.nf_uuids_to_ea_guids_mappings import (
    NfUuidsToEaGuidsMappings,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_object_column_types import (
    EaTObjectColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_package_column_types import (
    EaTPackageColumnTypes,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_new_uuid,
)
from pandas import DataFrame, Series


def add_ea_package_to_xml_tree(
    ea_package_row: Series,
    index: int,
    nf_uuid_column_name: str,
    start_ea_identifier_for_new_packages: int,
    start_ea_identifier_for_new_objects: int,
    parent_column_name: str,
    name_column_name: str,
    containing_ea_package_guid: str,
    xml_element_for_packages: Element,
    xml_element_for_packages_as_objects: Element,
    recyclable_packages: DataFrame,
):
    package_was_added = add_ea_package_to_xml_tree_if_possible(
        nf_uuid=ea_package_row[
            nf_uuid_column_name
        ],
        ea_identifier_for_package=start_ea_identifier_for_new_packages
        + int(index),
        ea_identifier_for_object=start_ea_identifier_for_new_objects
        + int(index),
        xml_element_for_packages=xml_element_for_packages,
        xml_element_for_packages_as_objects=xml_element_for_packages_as_objects,
        containing_ea_package_guid=containing_ea_package_guid,
        ea_package_parent_nf_uuid=ea_package_row[
            parent_column_name
        ],
        ea_package_name=ea_package_row[
            name_column_name
        ],
    )

    if not package_was_added:
        recyclable_packages.loc[
            index
        ] = ea_package_row


def add_ea_package_to_xml_tree_if_possible(
    nf_uuid: str,
    ea_identifier_for_package: int,
    ea_identifier_for_object: int,
    ea_package_name: str,
    ea_package_parent_nf_uuid: str,
    containing_ea_package_guid: str,
    xml_element_for_packages: Element,
    xml_element_for_packages_as_objects: Element,
) -> bool:
    if (
        ea_package_parent_nf_uuid
        == DEFAULT_NULL_VALUE
    ):
        ea_package_parent_ea_guid = (
            containing_ea_package_guid
        )
    else:
        ea_package_parent_ea_guid = NfUuidsToEaGuidsMappings.get_ea_guid(
            ea_package_parent_nf_uuid
        )

    if (
        ea_package_parent_ea_guid
        == DEFAULT_NULL_VALUE
    ):
        return False

    ea_package_parent_ea_identifier = EaGuidsToEaIdentifiersForPackagesMappings.map.get_ea_identifier(
        ea_package_parent_ea_guid
    )

    if (
        ea_package_parent_ea_identifier
        == DEFAULT_NULL_VALUE
    ):
        return False

    ea_package_guid = (
        "{" + create_new_uuid() + "}"
    )

    names_to_values_map_for_package = {
        EaTPackageColumnTypes.T_PACKAGE_IDS.column_name: ea_identifier_for_package,
        EaTPackageColumnTypes.T_PACKAGE_NAMES.column_name: ea_package_name,
        EaTPackageColumnTypes.T_PACKAGE_EA_GUIDS.column_name: ea_package_guid,
        EaTPackageColumnTypes.T_PACKAGE_PARENT_IDS.column_name: ea_package_parent_ea_identifier,
    }

    names_to_values_map_for_package_as_object = {
        EaTObjectColumnTypes.T_OBJECT_IDS.column_name: ea_identifier_for_object,
        EaTObjectColumnTypes.T_OBJECT_TYPES.column_name: "Package",
        EaTObjectColumnTypes.T_OBJECT_NAMES.column_name: ea_package_name,
        EaTObjectColumnTypes.T_OBJECT_PACKAGE_IDS.column_name: ea_package_parent_ea_identifier,
        EaTObjectColumnTypes.T_OBJECT_PDATA1.column_name: ea_package_parent_ea_identifier,
        EaTObjectColumnTypes.T_OBJECT_CLASSIFIERS.column_name: "0",
        EaTObjectColumnTypes.T_OBJECT_EA_GUIDS.column_name: ea_package_guid,
    }

    # Since 'Parent_ID' and 'Package_ID' values are specific to XML import/export, it shouldn't be taken from enum.
    xml_extensions_map_for_packages = {
        EaTPackageColumnTypes.T_PACKAGE_PARENT_IDS.column_name: ea_package_parent_ea_guid
    }

    xml_extensions_map_for_objects = {
        EaTObjectColumnTypes.T_OBJECT_PACKAGE_IDS.column_name: ea_package_parent_ea_guid,
        EaTObjectColumnTypes.T_OBJECT_PDATA1.column_name: ea_package_guid,
    }

    add_xml_row_element_to_xml_table_element(
        xml_element_for_table=xml_element_for_packages,
        xml_column_names_to_values_map=names_to_values_map_for_package,
        xml_extensions_map=xml_extensions_map_for_packages,
    )

    add_xml_row_element_to_xml_table_element(
        xml_element_for_table=xml_element_for_packages_as_objects,
        xml_column_names_to_values_map=names_to_values_map_for_package_as_object,
        xml_extensions_map=xml_extensions_map_for_objects,
    )

    EaGuidsToEaIdentifiersForObjectsMappings.map.add_single_map(
        ea_guid=ea_package_guid,
        ea_identifier=ea_identifier_for_object,
    )

    EaGuidsToEaIdentifiersForPackagesMappings.map.add_single_map(
        ea_guid=ea_package_guid,
        ea_identifier=ea_identifier_for_package,
    )

    NfUuidsToEaGuidsMappings.add_single_map(
        nf_uuid=nf_uuid,
        ea_guid=ea_package_guid,
    )

    return True
