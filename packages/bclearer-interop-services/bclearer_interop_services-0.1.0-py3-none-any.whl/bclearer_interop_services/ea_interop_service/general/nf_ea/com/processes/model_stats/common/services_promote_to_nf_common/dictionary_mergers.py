from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)


def left_merge_dictionaries_of_rows(
    master_dictionary: dict,
    master_dictionary_key_column: str,
    foreign_key_dictionary: dict,
    foreign_key_dictionary_fk_column: str,
    foreign_key_dictionary_other_column_rename_dictionary: dict,
) -> dict:
    merged_dictionary = (
        master_dictionary.copy()
    )

    foreign_key_mapping_dictionary = {}

    for (
        foreign_key_dictionary_row
    ) in (
        foreign_key_dictionary.values()
    ):
        foreign_key_mapping_dictionary[
            foreign_key_dictionary_row.pop(
                foreign_key_dictionary_fk_column
            )
        ] = foreign_key_dictionary_row

    foreign_key_mapping_dictionary.pop(
        DEFAULT_NULL_VALUE, {}
    )

    for (
        merged_dictionary_index,
        merged_dictionary_row,
    ) in merged_dictionary.items():
        master_dictionary_key_value = merged_dictionary[
            merged_dictionary_index
        ][
            master_dictionary_key_column
        ]

        if (
            master_dictionary_key_value
            in foreign_key_mapping_dictionary
        ):
            for (
                foreign_key_column_name,
                merged_key_column_name,
            ) in (
                foreign_key_dictionary_other_column_rename_dictionary.items()
            ):
                merged_dictionary_row[
                    merged_key_column_name
                ] = foreign_key_mapping_dictionary[
                    master_dictionary_key_value
                ][
                    foreign_key_column_name
                ]

        else:
            for (
                foreign_key_column_name,
                merged_key_column_name,
            ) in (
                foreign_key_dictionary_other_column_rename_dictionary.items()
            ):
                merged_dictionary_row[
                    merged_key_column_name
                ] = DEFAULT_NULL_VALUE

    return merged_dictionary
