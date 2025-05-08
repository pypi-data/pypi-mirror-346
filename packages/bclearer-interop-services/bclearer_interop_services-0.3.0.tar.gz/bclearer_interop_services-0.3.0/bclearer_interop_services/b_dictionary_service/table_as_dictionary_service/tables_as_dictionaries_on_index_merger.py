import copy


def merge_tables_as_dictionaries_on_index(
    tables_to_merge: list,
) -> dict:
    merged_table = copy.deepcopy(
        tables_to_merge[0],
    )

    for index in range(
        1,
        len(tables_to_merge),
    ):
        __merge_table(
            merged_table=merged_table,
            table_to_merge=tables_to_merge[
                index
            ],
        )

    return merged_table


def __merge_table(
    merged_table: dict,
    table_to_merge: dict,
) -> None:
    for (
        index,
        current_row,
    ) in merged_table.items():
        __merge_row(
            index=index,
            current_row=current_row,
            table_to_merge=table_to_merge,
        )


def __merge_row(
    index,
    current_row: dict,
    table_to_merge: dict,
) -> None:
    row_to_merge = table_to_merge[index]

    current_row.update(row_to_merge)
