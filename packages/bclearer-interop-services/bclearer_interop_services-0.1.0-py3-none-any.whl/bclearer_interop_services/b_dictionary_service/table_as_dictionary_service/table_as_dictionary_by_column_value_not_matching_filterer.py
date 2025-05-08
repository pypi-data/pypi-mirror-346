from typing import Optional


def filter_table_as_dictionary_by_column_value_not_matching(
    table_as_dictionary: dict,
    column_name: str,
    column_value_is_not: str | None,
) -> dict:
    filtered_dictionary = dict()

    for (
        key,
        row_dictionary,
    ) in table_as_dictionary.items():
        if (
            row_dictionary[column_name]
            != column_value_is_not
        ):
            filtered_dictionary[key] = (
                row_dictionary
            )

    return filtered_dictionary
