import pandas


def run_check(
    set_table: pandas.DataFrame,
    identity_set_indices: list,
) -> pandas.DataFrame:
    set_table_copy = set_table.copy()

    for (
        identity_set_index
    ) in identity_set_indices:
        set_table_copy[
            identity_set_index
        ] = set_table_copy[
            identity_set_index
        ].astype(
            str,
        )

    set_table_duplicates = set_table_copy[
        set_table_copy.duplicated(
            subset=identity_set_indices,
            keep=False,
        )
    ]

    if set_table_duplicates.empty:
        return None

    return set_table_duplicates
