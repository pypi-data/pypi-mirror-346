from typing import List

from pandas import DataFrame


def set_dataframe_columns_to_default_value(
    dataframe: DataFrame,
    column_names: list[str],
    default_cell_value: str,
) -> None:
    for column_name in column_names:
        dataframe[column_name] = (
            default_cell_value
        )
