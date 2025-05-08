from xml.etree.ElementTree import (
    Element,
)

from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.nf_ea_xml_adders.ea_connectors_xml_adder import (
    add_ea_connectors_to_xml_root_element,
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


def map_and_xml_load_ea_connectors(
    ea_connectors: DataFrame,
    start_ea_identifier: int,
    xml_root_element: Element,
    stereotype_usage_with_names: DataFrame,
    xml_element_for_connectors=None,
) -> tuple:
    log_message("Exporting connectors")

    ea_connectors = (
        ea_connectors.fillna(
            DEFAULT_NULL_VALUE
        )
    )

    __map_matched_ea_connectors(
        ea_connectors=ea_connectors
    )

    (
        xml_root,
        xml_element_for_connectors,
        start_ea_identifier_for_new_connectors,
    ) = __load_unmatched_ea_connectors(
        ea_connectors=ea_connectors,
        start_ea_identifier=start_ea_identifier,
        xml_root_element=xml_root_element,
        xml_element_for_connectors=xml_element_for_connectors,
        stereotype_usage_with_names=stereotype_usage_with_names,
    )

    return (
        xml_root,
        xml_element_for_connectors,
        start_ea_identifier_for_new_connectors,
    )


def __map_matched_ea_connectors(
    ea_connectors: DataFrame,
):
    NfUuidsToEaGuidsMappings.map_objects_from_dataframe(
        dataframe=ea_connectors
    )


def __load_unmatched_ea_connectors(
    ea_connectors: DataFrame,
    start_ea_identifier: int,
    xml_root_element: Element,
    xml_element_for_connectors: Element,
    stereotype_usage_with_names: DataFrame,
) -> tuple:
    ea_guids_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
    )

    unmatched_ea_connectors = (
        ea_connectors.loc[
            ea_connectors[
                ea_guids_column_name
            ]
            == DEFAULT_NULL_VALUE
        ]
    )

    (
        xml_root,
        xml_element_for_connectors,
        start_ea_identifier_for_new_connectors,
    ) = add_ea_connectors_to_xml_root_element(
        ea_connectors=unmatched_ea_connectors,
        xml_root=xml_root_element,
        xml_element_for_connectors=xml_element_for_connectors,
        start_ea_identifier=start_ea_identifier,
        stereotype_usage_with_names=stereotype_usage_with_names,
    )

    return (
        xml_root,
        xml_element_for_connectors,
        start_ea_identifier_for_new_connectors,
    )
