def filter_table_as_dictionary_by_column_values_list_not_matching(
    table_as_dictionary: dict,
    column_name: str,
    column_values_are_not: list,
) -> dict:
    filtered_dictionary = dict()

    for (
        key,
        row_dictionary,
    ) in table_as_dictionary.items():
        if (
            row_dictionary[column_name]
            not in column_values_are_not
        ):
            filtered_dictionary[key] = (
                row_dictionary
            )

    return filtered_dictionary
