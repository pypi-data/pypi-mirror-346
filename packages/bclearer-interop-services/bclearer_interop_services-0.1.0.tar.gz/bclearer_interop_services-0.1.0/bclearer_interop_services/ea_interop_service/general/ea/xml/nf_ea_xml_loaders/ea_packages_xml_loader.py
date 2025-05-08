from xml.etree.ElementTree import (
    Element,
)

from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.nf_ea_xml_adders.ea_packages_xml_adder import (
    add_ea_packages_to_xml_root_element,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.maps.nf_uuids_to_ea_guids_mappings import (
    NfUuidsToEaGuidsMappings,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from pandas import DataFrame


def map_and_xml_load_ea_packages(
    ea_packages: DataFrame,
    start_ea_identifier_for_new_packages: int,
    start_ea_identifier_for_new_objects: int,
    xml_root_element: Element,
    xml_element_for_packages: Element,
    containing_ea_package_guid: str,
) -> tuple:
    log_message("Exporting packages")

    ea_packages = ea_packages.fillna(
        DEFAULT_NULL_VALUE
    )

    __map_matched_ea_packages(
        ea_packages=ea_packages
    )

    (
        xml_root,
        xml_element_for_packages_as_objects,
        start_ea_identifier_for_new_objects,
    ) = __load_unmatched_ea_packages(
        ea_packages=ea_packages,
        start_ea_identifier_for_new_packages=start_ea_identifier_for_new_packages,
        start_ea_identifier_for_new_objects=start_ea_identifier_for_new_objects,
        xml_root_element=xml_root_element,
        xml_element_for_packages=xml_element_for_packages,
        containing_ea_package_guid=containing_ea_package_guid,
    )

    return (
        xml_root,
        xml_element_for_packages_as_objects,
        start_ea_identifier_for_new_objects,
    )


def __map_matched_ea_packages(
    ea_packages: DataFrame,
):
    NfUuidsToEaGuidsMappings.map_objects_from_dataframe(
        dataframe=ea_packages
    )


def __load_unmatched_ea_packages(
    ea_packages: DataFrame,
    start_ea_identifier_for_new_packages: int,
    start_ea_identifier_for_new_objects: int,
    xml_root_element: Element,
    xml_element_for_packages: Element,
    containing_ea_package_guid: str,
) -> tuple:
    ea_guids_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
    )

    unmatched_ea_classifiers = (
        ea_packages.loc[
            ea_packages[
                ea_guids_column_name
            ]
            == DEFAULT_NULL_VALUE
        ]
    )

    (
        xml_root_element,
        xml_element_for_packages_as_objects,
        start_ea_identifier_for_new_objects,
    ) = add_ea_packages_to_xml_root_element(
        ea_packages=unmatched_ea_classifiers,
        xml_root=xml_root_element,
        xml_element_for_packages=xml_element_for_packages,
        start_ea_identifier_for_new_packages=start_ea_identifier_for_new_packages,
        start_ea_identifier_for_new_objects=start_ea_identifier_for_new_objects,
        containing_ea_package_guid=containing_ea_package_guid,
    )

    return (
        xml_root_element,
        xml_element_for_packages_as_objects,
        start_ea_identifier_for_new_objects,
    )
