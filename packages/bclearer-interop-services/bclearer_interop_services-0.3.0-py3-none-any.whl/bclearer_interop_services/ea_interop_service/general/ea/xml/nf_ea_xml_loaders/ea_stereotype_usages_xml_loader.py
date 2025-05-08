from xml.etree.ElementTree import (
    Element,
)

from bclearer_interop_services.ea_interop_service.general.ea.xml.nf_ea_xml_adders.ea_stereotype_usages_xml_adder import (
    add_ea_stereotype_usages_to_xml_root_element,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from pandas import DataFrame


def map_and_xml_load_ea_stereotype_usages(
    stereotype_usage_with_names: DataFrame,
    xml_root_element: Element,
) -> Element:
    log_message(
        "Exporting stereotype usages"
    )

    xml_root_element = add_ea_stereotype_usages_to_xml_root_element(
        stereotype_usage_with_names=stereotype_usage_with_names,
        xml_root=xml_root_element,
    )

    return xml_root_element
