def concatenate_dictionaries(
    dictionaries: list,
) -> dict:
    concatenated_dictionary = dict()

    for dictionary in dictionaries:
        concatenated_dictionary.update(
            dictionary
        )

    return concatenated_dictionary
