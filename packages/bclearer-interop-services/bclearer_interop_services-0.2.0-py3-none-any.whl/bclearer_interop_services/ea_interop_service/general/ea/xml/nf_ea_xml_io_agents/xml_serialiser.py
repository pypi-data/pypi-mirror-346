import xml.etree.ElementTree
from xml.dom import minidom
from xml.etree.ElementTree import (
    Element,
)


def get_xml_string_as_bytes(
    xml_root_element: Element,
) -> bytes:
    tree_as_string = (
        xml.etree.ElementTree.tostring(
            xml_root_element
        )
    )

    xml_document = minidom.parseString(
        string=tree_as_string
    )

    pretty_xml_string_as_bytes = (
        xml_document.toprettyxml(
            encoding="utf-8",
            indent="   ",
        )
    )

    return pretty_xml_string_as_bytes


def serialise_xml(
    xml_root_element: Element,
    xml_file_full_path: str,
) -> None:
    pretty_xml_string = get_xml_string_as_bytes(
        xml_root_element=xml_root_element
    )

    with open(
        xml_file_full_path, "wb"
    ) as xml_file:
        xml_file.write(
            pretty_xml_string
        )

        xml_file.close()
