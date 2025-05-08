def add_static_column_value_to_table_as_dictionary(
    table_as_dictionary: dict,
    column_name: str,
    static_value,
) -> None:
    for (
        key,
        row_as_dictionary,
    ) in table_as_dictionary.items():
        __add_static_column_value_to_row(
            row_as_dictionary=row_as_dictionary,
            column_name=column_name,
            static_string_value=static_value,
        )


def __add_static_column_value_to_row(
    row_as_dictionary: dict,
    column_name: str,
    static_string_value,
) -> None:
    row_as_dictionary[column_name] = (
        static_string_value
    )
