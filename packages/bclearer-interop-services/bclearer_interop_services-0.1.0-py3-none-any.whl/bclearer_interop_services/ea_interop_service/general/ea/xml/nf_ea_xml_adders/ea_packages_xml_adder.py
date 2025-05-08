import sys
from xml.etree.ElementTree import (
    Element,
    SubElement,
)

from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.nf_ea_xml_adders.ea_package_xml_adder import (
    add_ea_package_to_xml_tree,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from pandas import DataFrame


def add_ea_packages_to_xml_root_element(
    ea_packages: DataFrame,
    xml_root: Element,
    xml_element_for_packages: Element,
    start_ea_identifier_for_new_packages: int,
    start_ea_identifier_for_new_objects: int,
    containing_ea_package_guid: str,
    xml_element_for_packages_as_objects=None,
) -> tuple:
    nf_uuid_column_name = (
        NfColumnTypes.NF_UUIDS.column_name
    )

    name_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name
    )

    parent_column_name = (
        NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT.column_name
    )

    if (
        xml_element_for_packages_as_objects
        is None
    ):
        xml_element_for_packages_as_objects = __create_xml_element_for_packages_as_objects(
            xml_root=xml_root
        )

    index = 0

    recyclable_packages = DataFrame(
        columns=ea_packages.columns
    )

    for (
        index,
        ea_package_row,
    ) in ea_packages.iterrows():
        add_ea_package_to_xml_tree(
            ea_package_row=ea_package_row,
            index=index,
            nf_uuid_column_name=nf_uuid_column_name,
            xml_element_for_packages=xml_element_for_packages,
            xml_element_for_packages_as_objects=xml_element_for_packages_as_objects,
            containing_ea_package_guid=containing_ea_package_guid,
            start_ea_identifier_for_new_packages=start_ea_identifier_for_new_packages,
            start_ea_identifier_for_new_objects=start_ea_identifier_for_new_objects,
            parent_column_name=parent_column_name,
            name_column_name=name_column_name,
            recyclable_packages=recyclable_packages,
        )

    start_ea_identifier_for_new_objects += (
        index + 1
    )

    if len(recyclable_packages) == len(
        ea_packages
    ):
        log_message(
            message="Cannot import packages because of circularity within their parents"
        )

        sys.exit(-1)

    if len(recyclable_packages) > 0:
        add_ea_packages_to_xml_root_element(
            ea_packages=recyclable_packages,
            xml_root=xml_root,
            xml_element_for_packages=xml_element_for_packages,
            start_ea_identifier_for_new_packages=start_ea_identifier_for_new_packages,
            start_ea_identifier_for_new_objects=start_ea_identifier_for_new_objects,
            containing_ea_package_guid=containing_ea_package_guid,
            xml_element_for_packages_as_objects=xml_element_for_packages_as_objects,
        )

    start_ea_identifier_for_new_objects += (
        index + 1
    )

    return (
        xml_root,
        xml_element_for_packages_as_objects,
        start_ea_identifier_for_new_objects,
    )


def __create_xml_element_for_packages_as_objects(
    xml_root: Element,
) -> Element:
    xml_element_for_packages_as_objects = SubElement(
        xml_root, "Table"
    )

    xml_element_for_packages_as_objects.set(
        "name",
        EaCollectionTypes.T_OBJECT.collection_name,
    )

    return xml_element_for_packages_as_objects
