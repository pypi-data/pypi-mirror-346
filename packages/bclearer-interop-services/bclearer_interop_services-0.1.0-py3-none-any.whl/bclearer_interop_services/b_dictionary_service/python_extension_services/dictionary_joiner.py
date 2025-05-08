def join_dictionaries(
    dictionaries: list,
) -> dict:
    joined_dictionary = dict()

    for dictionary in dictionaries:
        joined_dictionary.update(
            dictionary,
        )

    return joined_dictionary
