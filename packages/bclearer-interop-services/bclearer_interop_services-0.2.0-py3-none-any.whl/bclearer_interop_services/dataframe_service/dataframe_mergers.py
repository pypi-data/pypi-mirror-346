import pandas

STRINGIFIED_COLUMN_SUFFIX = "_string"


def left_merge_dataframes(
    master_dataframe: pandas.DataFrame,
    master_dataframe_key_columns: list,
    merge_suffixes: list,
    foreign_key_dataframe: pandas.DataFrame,
    foreign_key_dataframe_fk_columns: list,
    foreign_key_dataframe_other_column_rename_dictionary=None,
):
    if (
        foreign_key_dataframe_other_column_rename_dictionary
        is None
    ):
        foreign_key_dataframe_other_column_rename_dictionary = (
            dict()
        )

    return merge_dataframes(
        master_dataframe,
        master_dataframe_key_columns,
        "left",
        merge_suffixes,
        foreign_key_dataframe,
        foreign_key_dataframe_fk_columns,
        foreign_key_dataframe_other_column_rename_dictionary,
    )


def inner_merge_dataframes(
    master_dataframe: pandas.DataFrame,
    master_dataframe_key_columns: list,
    merge_suffixes: list,
    foreign_key_dataframe: pandas.DataFrame,
    foreign_key_dataframe_fk_columns: list,
    foreign_key_dataframe_other_column_rename_dictionary=None,
):
    if (
        foreign_key_dataframe_other_column_rename_dictionary
        is None
    ):
        foreign_key_dataframe_other_column_rename_dictionary = (
            dict()
        )

    return merge_dataframes(
        master_dataframe,
        master_dataframe_key_columns,
        "inner",
        merge_suffixes,
        foreign_key_dataframe,
        foreign_key_dataframe_fk_columns,
        foreign_key_dataframe_other_column_rename_dictionary,
    )


def outer_merge_dataframes(
    master_dataframe: pandas.DataFrame,
    master_dataframe_key_columns: list,
    merge_suffixes: list,
    foreign_key_dataframe: pandas.DataFrame,
    foreign_key_dataframe_fk_columns: list,
    foreign_key_dataframe_other_column_rename_dictionary=None,
):
    if (
        foreign_key_dataframe_other_column_rename_dictionary
        is None
    ):
        foreign_key_dataframe_other_column_rename_dictionary = (
            dict()
        )

    return merge_dataframes(
        master_dataframe,
        master_dataframe_key_columns,
        "outer",
        merge_suffixes,
        foreign_key_dataframe,
        foreign_key_dataframe_fk_columns,
        foreign_key_dataframe_other_column_rename_dictionary,
    )


def merge_dataframes(
    master_dataframe: pandas.DataFrame,
    master_dataframe_key_columns: list,
    how_to_merge: str,
    merge_suffixes: list,
    foreign_key_dataframe: pandas.DataFrame,
    foreign_key_dataframe_fk_columns: list,
    foreign_key_dataframe_other_column_rename_dictionary=None,
):
    if (
        foreign_key_dataframe_other_column_rename_dictionary
        is None
    ):
        foreign_key_dataframe_other_column_rename_dictionary = (
            dict()
        )

    master_dataframe_copy = (
        master_dataframe.copy()
    )

    foreign_key_dataframe_copy = (
        foreign_key_dataframe.copy()
    )

    stringified_master_dataframe_key_columns = stringify_columns_in_dataframe(
        master_dataframe_key_columns,
        master_dataframe_copy,
    )

    stringified_foreign_key_dataframe_fk_columns = stringify_columns_in_dataframe(
        foreign_key_dataframe_fk_columns,
        foreign_key_dataframe_copy,
    )

    foreign_key_dataframe_copy.rename(
        columns=foreign_key_dataframe_other_column_rename_dictionary,
        inplace=True,
    )

    foreign_key_dataframe_all_columns = (
        list(
            foreign_key_dataframe_other_column_rename_dictionary.values(),
        )
        + stringified_foreign_key_dataframe_fk_columns
    )

    foreign_key_dataframe_copy = foreign_key_dataframe_copy.filter(
        items=foreign_key_dataframe_all_columns,
    )

    master_dataframe_copy = master_dataframe_copy.merge(
        right=foreign_key_dataframe_copy,
        left_on=stringified_master_dataframe_key_columns,
        right_on=stringified_foreign_key_dataframe_fk_columns,
        how=how_to_merge,
        suffixes=merge_suffixes,
    )

    master_dataframe_copy.drop(
        columns=stringified_master_dataframe_key_columns
        + stringified_foreign_key_dataframe_fk_columns,
        inplace=True,
    )

    return master_dataframe_copy


def stringify_columns_in_dataframe(
    columns: list,
    dataframe: pandas.DataFrame,
):
    stringified_columns = list()

    for column in columns:
        stringified_column = (
            column
            + STRINGIFIED_COLUMN_SUFFIX
        )

        stringified_columns.append(
            stringified_column,
        )

        dataframe[
            stringified_column
        ] = dataframe[column].astype(
            str,
        )

    return stringified_columns
