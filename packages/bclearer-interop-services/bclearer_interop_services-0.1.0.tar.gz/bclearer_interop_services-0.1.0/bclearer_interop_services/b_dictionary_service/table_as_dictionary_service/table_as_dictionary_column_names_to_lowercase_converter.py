def convert_table_as_dictionary_column_names_into_lowercase(
    table_as_dictionary: dict,
) -> dict:
    lowercase_table_as_dictionary = (
        dict()
    )

    for (
        row_index,
        row_dictionary,
    ) in table_as_dictionary.items():
        lowercase_row_dictionary = (
            dict()
        )

        for (
            column_name
        ) in row_dictionary:
            lowercase_row_dictionary[
                column_name.lower()
            ] = row_dictionary[
                column_name
            ]

        lowercase_table_as_dictionary[
            row_index
        ] = lowercase_row_dictionary

    return lowercase_table_as_dictionary
