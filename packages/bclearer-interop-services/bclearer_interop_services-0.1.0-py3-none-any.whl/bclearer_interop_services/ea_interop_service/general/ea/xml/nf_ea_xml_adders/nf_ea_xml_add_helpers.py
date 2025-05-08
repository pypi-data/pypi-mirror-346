from xml.etree.ElementTree import (
    Element,
    SubElement,
)


def add_xml_row_element_to_xml_data_reference_table_element(
    xml_element_for_table: Element,
    xml_column_names_to_values_map: dict,
):
    __add_xml_row_element_to_xml_table_element(
        xml_element_for_table=xml_element_for_table,
        xml_column_names_to_values_map=xml_column_names_to_values_map,
        row_name="DataRow",
        add_extensions=False,
    )


def add_xml_row_element_to_xml_table_element(
    xml_element_for_table: Element,
    xml_column_names_to_values_map: dict,
    xml_extensions_map=None,
):
    __add_xml_row_element_to_xml_table_element(
        xml_element_for_table=xml_element_for_table,
        xml_column_names_to_values_map=xml_column_names_to_values_map,
        row_name="Row",
        add_extensions=True,
        xml_extensions_map=xml_extensions_map,
    )


def __add_xml_row_element_to_xml_table_element(
    xml_element_for_table: Element,
    xml_column_names_to_values_map: dict,
    row_name: str,
    add_extensions: bool,
    xml_extensions_map=None,
):
    if xml_extensions_map is None:
        xml_extensions_map = {}

    xml_element_for_row = SubElement(
        xml_element_for_table, row_name
    )

    for (
        name,
        value,
    ) in (
        xml_column_names_to_values_map.items()
    ):
        xml_element_for_column = (
            SubElement(
                xml_element_for_row,
                "Column",
            )
        )

        xml_element_for_column.set(
            "name", str(name)
        )

        xml_element_for_column.set(
            "value", str(value)
        )

    if add_extensions:
        xml_element_for_extension = (
            SubElement(
                xml_element_for_row,
                "Extension",
            )
        )

        for (
            name,
            value,
        ) in xml_extensions_map.items():
            xml_element_for_extension.set(
                name, value
            )
