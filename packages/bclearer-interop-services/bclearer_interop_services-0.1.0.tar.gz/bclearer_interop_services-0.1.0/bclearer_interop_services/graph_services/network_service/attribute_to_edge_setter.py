from networkx import set_edge_attributes


def set_attribute_to_edge(
    graph,
    edge: tuple,
    attribute_name: str,
    attribute_value,
) -> None:
    edge_to_default_attribute_name_and_value_dictionary = {
        edge: {
            attribute_name: attribute_value,
        },
    }

    set_edge_attributes(
        G=graph,
        values=edge_to_default_attribute_name_and_value_dictionary,
    )
