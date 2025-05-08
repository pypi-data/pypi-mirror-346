def deduplicate_table_as_dictionary_by_value(
    table_as_dictionary: dict,
) -> dict:
    deduplicated_dictionary = dict()

    for (
        key,
        row_dictionary,
    ) in table_as_dictionary.items():
        if (
            row_dictionary
            not in deduplicated_dictionary.values()
        ):
            deduplicated_dictionary[
                key
            ] = row_dictionary

    return deduplicated_dictionary
