def remove_table_as_dictionary_column(
    table_as_dictionary: dict,
    column_name: str,
) -> None:
    for (
        row_index,
        row_dictionary,
    ) in table_as_dictionary.items():
        del row_dictionary[column_name]
