def filter_and_reorder_table_as_dictionary_by_column_names(
    table_as_dictionary: dict,
    column_names: list,
) -> dict:
    filtered_dictionary = dict()

    for (
        key,
        row_dictionary,
    ) in table_as_dictionary.items():
        __filter_row_and_add_to_filtered_dictionary(
            filtered_dictionary=filtered_dictionary,
            key=key,
            row_dictionary=row_dictionary,
            column_names=column_names,
        )

    return filtered_dictionary


def __filter_row_and_add_to_filtered_dictionary(
    filtered_dictionary: dict,
    key: str,
    row_dictionary: dict,
    column_names: list,
) -> None:
    filtered_dictionary_row = dict()

    for (
        row_dictionary_key,
        row_dictionary_value,
    ) in row_dictionary.items():
        if (
            row_dictionary_key
            in column_names
        ):
            filtered_dictionary_row[
                row_dictionary_key
            ] = row_dictionary_value

    filtered_and_reordered_dictionary_row = {
        key: filtered_dictionary_row[
            key
        ]
        for key in column_names
    }

    filtered_dictionary[key] = (
        filtered_and_reordered_dictionary_row
    )
