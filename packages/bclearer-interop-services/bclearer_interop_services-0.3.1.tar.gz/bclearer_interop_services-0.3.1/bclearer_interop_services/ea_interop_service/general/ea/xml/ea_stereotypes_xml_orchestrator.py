from xml.etree.ElementTree import (
    Element,
)

from bclearer_interop_services.ea_interop_service.general.ea.xml.nf_ea_xml_adders.stereotypes_dataset_xml_preparer import (
    prepare_stereotypes_dataset_xml,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.nf_ea_xml_io_agents.xml_serialiser import (
    get_xml_string_as_bytes,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.nf_ea_xml_loaders.ea_stereotypes_xml_loader import (
    map_and_xml_load_ea_stereotypes,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from pandas import DataFrame


def orchestrate_ea_stereotypes_xml(
    ea_stereotypes: DataFrame,
):
    log_message(
        "Exporting stereotypes reference data xml."
    )

    (
        xml_root_element,
        xml_element_for_stereotypes_dataset,
    ) = (
        prepare_stereotypes_dataset_xml()
    )

    __map_and_load(
        ea_stereotypes=ea_stereotypes,
        xml_element_for_stereotypes_dataset=xml_element_for_stereotypes_dataset,
    )

    xml_string = get_xml_string_as_bytes(
        xml_root_element=xml_root_element
    )

    return xml_string


def __map_and_load(
    ea_stereotypes: DataFrame,
    xml_element_for_stereotypes_dataset: Element,
) -> Element:
    xml_root_element = map_and_xml_load_ea_stereotypes(
        ea_stereotypes=ea_stereotypes,
        xml_element_for_stereotypes_dataset=xml_element_for_stereotypes_dataset,
    )

    return xml_root_element
