from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from pandas import DataFrame

filling_up_map = {
    "str": DEFAULT_NULL_VALUE,
    "object": DEFAULT_NULL_VALUE,
}


def fill_up_all_empty_cells_with_default_null_value(
    dataframe: DataFrame,
) -> DataFrame:
    columns = list(
        dataframe.columns.values,
    )

    for column in columns:
        col_type = str(
            dataframe[column].dtype,
        )

        dataframe = __fill_up_all_cells_in_column_with_default_null_value(
            dataframe,
            column,
            col_type,
        )

    return dataframe


def __fill_up_all_cells_in_column_with_default_null_value(
    dataframe: DataFrame,
    column: str,
    col_type,
):
    if col_type not in filling_up_map:
        return dataframe

    default_null_value = filling_up_map[
        col_type
    ]

    dataframe[column].fillna(
        value=default_null_value,
        inplace=True,
    )

    return dataframe
