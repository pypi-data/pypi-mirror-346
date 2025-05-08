def filter_table_as_dictionary_by_column_values_list(
    table_as_dictionary: dict,
    column_name: str,
    column_values: list,
) -> dict:
    filtered_dictionary = dict()

    for (
        key,
        row_dictionary,
    ) in table_as_dictionary.items():
        if (
            row_dictionary[column_name]
            in column_values
        ):
            filtered_dictionary[key] = (
                row_dictionary
            )

    return filtered_dictionary
