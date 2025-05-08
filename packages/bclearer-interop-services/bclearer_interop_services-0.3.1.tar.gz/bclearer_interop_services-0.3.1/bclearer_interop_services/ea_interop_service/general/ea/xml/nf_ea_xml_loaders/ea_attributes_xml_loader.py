from xml.etree.ElementTree import (
    Element,
)

from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.nf_ea_xml_adders.ea_attributes_xml_adder import (
    add_ea_attributes_to_xml_root_element,
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


def map_and_xml_load_ea_attributes(
    ea_attributes: DataFrame,
    ea_classifiers: DataFrame,
    start_ea_identifier: int,
    xml_root_element: Element,
) -> Element:
    log_message("Exporting attributes")

    ea_attributes = (
        ea_attributes.fillna(
            DEFAULT_NULL_VALUE
        )
    )

    __map_matched_ea_attributes(
        ea_attributes=ea_attributes
    )

    __load_unmatched_ea_attributes(
        ea_attributes=ea_attributes,
        ea_classifiers=ea_classifiers,
        start_ea_identifier=start_ea_identifier,
        xml_root_element=xml_root_element,
    )

    return xml_root_element


def __map_matched_ea_attributes(
    ea_attributes: DataFrame,
):
    NfUuidsToEaGuidsMappings.map_objects_from_dataframe(
        dataframe=ea_attributes
    )


def __load_unmatched_ea_attributes(
    ea_attributes: DataFrame,
    ea_classifiers: DataFrame,
    start_ea_identifier: int,
    xml_root_element: Element,
) -> Element:
    ea_guids_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
    )

    unmatched_ea_attributes = (
        ea_attributes.loc[
            ea_attributes[
                ea_guids_column_name
            ]
            == DEFAULT_NULL_VALUE
        ]
    )

    xml_root_element = add_ea_attributes_to_xml_root_element(
        ea_attributes=unmatched_ea_attributes,
        ea_classifiers=ea_classifiers,
        xml_root=xml_root_element,
        start_ea_identifier=start_ea_identifier,
    )

    return xml_root_element
