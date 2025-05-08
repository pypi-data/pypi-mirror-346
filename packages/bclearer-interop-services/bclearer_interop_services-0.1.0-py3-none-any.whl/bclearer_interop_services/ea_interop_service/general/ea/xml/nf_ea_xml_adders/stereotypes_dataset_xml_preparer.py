from xml.etree.ElementTree import (
    Element,
    SubElement,
)

from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)


def prepare_stereotypes_dataset_xml() -> (
    tuple
):
    xml_root_element = (
        __set_xml_root_element()
    )

    xml_element_for_stereotypes_dataset = __add_stereotypes_dataset(
        xml_root_element=xml_root_element
    )

    return (
        xml_root_element,
        xml_element_for_stereotypes_dataset,
    )


def __set_xml_root_element() -> Element:
    xml_root_element = Element(
        "RefData"
    )

    xml_root_element.set(
        "version", "1.0"
    )

    xml_root_element.set(
        "exporter", "EA.25"
    )

    return xml_root_element


def __add_stereotypes_dataset(
    xml_root_element: Element,
) -> Element:
    xml_element_for_stereotypes_dataset = SubElement(
        xml_root_element, "DataSet"
    )

    xml_element_for_stereotypes_dataset.set(
        "name", "Stereotypes"
    )

    xml_element_for_stereotypes_dataset.set(
        "table",
        EaCollectionTypes.T_STEREOTYPES.collection_name,
    )

    xml_element_for_stereotypes_dataset.set(
        "filter",
        "Stereotype='#Stereotype#' and AppliesTo='#AppliesTo#'",
    )

    return xml_element_for_stereotypes_dataset
