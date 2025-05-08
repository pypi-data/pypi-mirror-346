from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_all_nan_with_empty_string_replacer import (
    replace_dataframe_all_nan_with_empty_string,
)
from pandas import DataFrame


def convert_all_cells_to_string(
    dataframe: DataFrame,
) -> DataFrame:
    dataframe_columns = (
        dataframe.columns.tolist()
    )

    replace_dataframe_all_nan_with_empty_string(
        dataframe=dataframe,
        columns=dataframe_columns,
    )

    for (
        dataframe_column
    ) in dataframe_columns:
        dataframe[dataframe_column] = (
            dataframe[
                dataframe_column
            ].astype(str)
        )

    return dataframe
