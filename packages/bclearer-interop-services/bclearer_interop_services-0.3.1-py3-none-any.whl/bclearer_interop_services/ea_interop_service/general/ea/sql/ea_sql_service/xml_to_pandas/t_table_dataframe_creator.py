from xml.etree import ElementTree

import pandas
from bclearer_interop_services.ea_interop_service.general.ea.sql.ea_sql_service.xml_to_pandas.node_value_getter import (
    get_node_value,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def create_t_table_dataframe(
    t_table_as_xml_string: str,
    column_types_enum,
) -> pandas.DataFrame:
    log_message(
        message="creating dataframe using column type: "
        + str(column_types_enum)
    )

    t_table_dataframe_column_nf_names_dictionary = __get_t_table_dataframe_nf_column_names_dictionary(
        column_types_enum=column_types_enum
    )

    t_table_dataframe_column_ea_names_dictionary = __get_t_table_dataframe_column_names_dictionary(
        column_types_enum=column_types_enum
    )

    t_table_dataframe = __create_t_table_dataframe(
        t_table_as_xml_string=t_table_as_xml_string,
        nf_names_dictionary=t_table_dataframe_column_nf_names_dictionary,
        ea_names_dictionary=t_table_dataframe_column_ea_names_dictionary,
    )

    log_message(
        message="created dataframe using column type: "
        + str(column_types_enum)
    )

    return t_table_dataframe


def __get_t_table_dataframe_nf_column_names_dictionary(
    column_types_enum,
) -> dict:
    t_table_dataframe_column_names_dictionary = (
        {}
    )

    for (
        column_type
    ) in column_types_enum:
        column_name = (
            column_type.nf_column_name
        )

        t_table_dataframe_column_names_dictionary[
            column_type
        ] = column_name

    return t_table_dataframe_column_names_dictionary


def __get_t_table_dataframe_column_names_dictionary(
    column_types_enum,
) -> dict:
    t_table_dataframe_column_names_dictionary = (
        {}
    )

    for (
        column_type
    ) in column_types_enum:
        column_name = (
            column_type.column_name
        )

        t_table_dataframe_column_names_dictionary[
            column_type
        ] = column_name

    return t_table_dataframe_column_names_dictionary


def __create_t_table_dataframe(
    t_table_as_xml_string: str,
    nf_names_dictionary: dict,
    ea_names_dictionary: dict,
) -> pandas.DataFrame:
    xml_element_tree = (
        ElementTree.ElementTree(
            ElementTree.fromstring(
                t_table_as_xml_string
            )
        )
    )

    t_table_dictionary = {}

    for (
        dataset_node
    ) in xml_element_tree.getroot():
        t_table_dictionary = __process_dataset_node(
            dataset_node=dataset_node,
            table_dictionary=t_table_dictionary,
            nf_names_dictionary=nf_names_dictionary,
            ea_names_dictionary=ea_names_dictionary,
        )

    t_table_dataframe = (
        pandas.DataFrame.from_dict(
            data=t_table_dictionary,
            orient="index",
        )
    )

    if len(t_table_dictionary) == 0:
        t_table_dataframe = pandas.DataFrame(
            columns=list(
                nf_names_dictionary.values()
            )
        )

    return t_table_dataframe


def __process_dataset_node(
    dataset_node,
    table_dictionary: dict,
    nf_names_dictionary: dict,
    ea_names_dictionary: dict,
):
    for table_node in dataset_node:
        table_dictionary = __process_table_node(
            table_node=table_node,
            table_dictionary=table_dictionary,
            nf_names_dictionary=nf_names_dictionary,
            ea_names_dictionary=ea_names_dictionary,
        )

    return table_dictionary


def __process_table_node(
    table_node,
    table_dictionary: dict,
    nf_names_dictionary: dict,
    ea_names_dictionary: dict,
):
    current_row_count = 0

    for row_node in table_node:
        current_row_count = __process_row_node(
            row_node=row_node,
            table_dictionary=table_dictionary,
            current_row_count=current_row_count,
            nf_names_dictionary=nf_names_dictionary,
            ea_names_dictionary=ea_names_dictionary,
        )

    return table_dictionary


def __process_row_node(
    row_node,
    table_dictionary: dict,
    current_row_count: int,
    nf_names_dictionary: dict,
    ea_names_dictionary: dict,
):
    cell_value_dictionary = {}

    for (
        column_type,
        ea_name,
    ) in ea_names_dictionary.items():
        cell_value_dictionary[
            column_type
        ] = row_node.find(ea_name)

    t_row_dictionary = {}

    for (
        column_type,
        nf_name,
    ) in nf_names_dictionary.items():
        t_row_dictionary[nf_name] = (
            get_node_value(
                cell_value_dictionary[
                    column_type
                ]
            )
        )

    table_dictionary[
        current_row_count
    ] = t_row_dictionary

    current_row_count = (
        current_row_count + 1
    )

    return current_row_count
