def get_table_as_dictionary_unique_values_of_column(
    table_as_dictionary: dict,
    column_name: str,
) -> list:
    unique_values = list()

    for (
        row_dictionary
    ) in table_as_dictionary.values():
        __add_column_value_to_list_if_unique(
            unique_values=unique_values,
            row_dictionary=row_dictionary,
            column_name=column_name,
        )

    return unique_values


def __add_column_value_to_list_if_unique(
    unique_values: list,
    row_dictionary: dict,
    column_name: str,
) -> None:
    current_column_value = (
        row_dictionary[column_name]
    )

    if (
        current_column_value
        not in unique_values
    ):
        unique_values.append(
            current_column_value,
        )
