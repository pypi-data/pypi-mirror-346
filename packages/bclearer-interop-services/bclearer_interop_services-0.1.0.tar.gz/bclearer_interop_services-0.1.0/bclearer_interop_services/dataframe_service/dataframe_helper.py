import uuid

import pandas
from bclearer_core.constants.nf_common_global_constants import (
    UUIDS_COLUMN_NAME,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_uuid_from_canonical_format_string,
)

PARENT_DATAFRAME_SUFFIX = (
    "_merge_parent"
)


def drop_duplicated_parent_columns(
    dataframe: pandas.DataFrame,
):
    drop_columns_by_marker(
        dataframe,
        PARENT_DATAFRAME_SUFFIX,
    )


def drop_columns_by_marker(
    dataframe: pandas.DataFrame,
    drop_marker: str,
):
    for (
        column
    ) in dataframe.columns.values:
        if drop_marker in column:
            dataframe.drop(
                column,
                axis=1,
                inplace=True,
            )


def add_fk_uuids(
    base_dataframe: pandas.DataFrame,
    parent_register_dataframe: pandas.DataFrame,
    base_column_foreign_key: str,
    parent_column_key: str,
    fk_uuid_column: str,
    remove_fk_after_uuidification,
):
    base_dataframe_columns = list(
        base_dataframe.columns,
    )

    if remove_fk_after_uuidification:
        base_dataframe_columns.remove(
            base_column_foreign_key,
        )

    merged_dataframe = base_dataframe.merge(
        right=parent_register_dataframe,
        left_on=base_column_foreign_key,
        how="left",
        right_on=parent_column_key,
        suffixes=[
            "",
            PARENT_DATAFRAME_SUFFIX,
        ],
    )

    base_dataframe_columns.append(
        fk_uuid_column,
    )

    if (
        UUIDS_COLUMN_NAME
        in base_dataframe_columns
    ):
        merged_dataframe.rename(
            columns={
                UUIDS_COLUMN_NAME
                + PARENT_DATAFRAME_SUFFIX: fk_uuid_column,
            },
            inplace=True,
        )
    else:
        merged_dataframe.rename(
            columns={
                UUIDS_COLUMN_NAME: fk_uuid_column,
            },
            inplace=True,
        )

    fk_uuidified_dataframe = (
        merged_dataframe.loc[
            :,
            base_dataframe_columns,
        ]
    )

    return fk_uuidified_dataframe


def add_parent_table_columns(
    base_dataframe: pandas.DataFrame,
    parent_register_dataframe: pandas.DataFrame,
    base_column_foreign_keys: list,
    parent_column_keys: list,
):
    merged_dataframe = base_dataframe.merge(
        right=parent_register_dataframe,
        how="left",
        left_on=base_column_foreign_keys,
        right_on=parent_column_keys,
        suffixes=[
            "",
            PARENT_DATAFRAME_SUFFIX,
        ],
    )

    drop_duplicated_parent_columns(
        merged_dataframe,
    )

    return merged_dataframe


def add_type_column_to_dataframe(
    dataframe: pandas.DataFrame,
    col_name: str,
    col_position,
    default_value: uuid,
):
    dataframe.insert(
        col_position,
        col_name,
        default_value,
    )

    return dataframe


def move_uuid_col_to_front(
    dataframe: pandas.DataFrame,
    uuid_column: str,
):
    columns = list(dataframe)

    columns.insert(
        0,
        columns.pop(
            columns.index(uuid_column),
        ),
    )

    dataframe = dataframe.loc[
        :,
        columns,
    ]

    return dataframe


def deduplicate(
    dataframe: pandas.DataFrame,
    columns: list,
):
    stringified_columns = list()

    for column in columns:
        stringified_column = (
            "stringified_" + column
        )

        dataframe[
            stringified_column
        ] = dataframe[column].astype(
            str,
        )

        stringified_columns.append(
            stringified_column,
        )

    dataframe.drop_duplicates(
        subset=stringified_columns,
        inplace=True,
    )

    dataframe.drop(
        columns=stringified_columns,
        inplace=True,
    )


def stringify_uuid_columns(
    dataframe: pandas.DataFrame,
    columns: list,
):
    for column in columns:
        dataframe[column] = dataframe[
            column
        ].astype(str)


def unstringify_uuid_columns(
    dataframe: pandas.DataFrame,
    columns: list,
):
    for column in columns:
        dataframe[column] = dataframe[
            column
        ].apply(
            lambda x: create_uuid_from_canonical_format_string(
                x,
            ),
        )


def drop_empty_columns(
    df: pandas.DataFrame,
) -> pandas.DataFrame:
    """Drops columns from the DataFrame that are either entirely empty or have an empty header.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
    -------
        pd.DataFrame: A DataFrame with the empty or unnamed columns removed.

    """
    # Step 1: Drop columns with completely empty headers (None or empty string)
    df = df.loc[
        :,
        df.columns.notna()
        & (df.columns != ""),
    ]

    # Step 2: Drop columns where all values are NaN or None
    df = df.dropna(axis=1, how="all")

    return df
