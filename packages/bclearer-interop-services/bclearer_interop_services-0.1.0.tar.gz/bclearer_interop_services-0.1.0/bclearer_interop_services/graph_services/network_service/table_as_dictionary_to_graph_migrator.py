from networkx import DiGraph


def migrate_table_as_dictionary_to_graph(
    table_as_dictionary: dict,
    source_id_column_name: str,
    target_id_column_name: str,
    edge_attribute_column_names: list = None,
    edge_type_name_and_value_dictionary: dict = None,
) -> DiGraph:
    edges_container = list()

    for (
        row_dictionary
    ) in table_as_dictionary.values():
        __add_row_dictionary_to_edges_container(
            edges_container=edges_container,
            row_dictionary=row_dictionary,
            edge_type_name_and_value_dictionary=edge_type_name_and_value_dictionary,
            edge_attribute_column_names=edge_attribute_column_names,
            source_id_column_name=source_id_column_name,
            target_id_column_name=target_id_column_name,
        )

    output_graph = DiGraph(
        edges_container,
    )

    return output_graph


def __add_row_dictionary_to_edges_container(
    edges_container: list,
    row_dictionary: dict,
    edge_type_name_and_value_dictionary: dict,
    edge_attribute_column_names: list,
    source_id_column_name: str,
    target_id_column_name: str,
) -> None:
    edge_attributes_dictionary = dict()

    if edge_type_name_and_value_dictionary:
        edge_attributes_dictionary.update(
            edge_type_name_and_value_dictionary,
        )

    if edge_attribute_column_names:
        for (
            edge_attribute_column_name
        ) in (
            edge_attribute_column_names
        ):
            edge_attributes_dictionary[
                edge_attribute_column_name
            ] = row_dictionary[
                edge_attribute_column_name
            ]

    edges_container.append(
        (
            row_dictionary[
                source_id_column_name
            ],
            row_dictionary[
                target_id_column_name
            ],
            edge_attributes_dictionary,
        ),
    )
