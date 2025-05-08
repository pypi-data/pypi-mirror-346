from pandas import DataFrame


def replace_dataframe_all_nan_with_empty_string(
    dataframe: DataFrame,
    columns: list = None,
) -> DataFrame:
    if not columns:
        columns = (
            dataframe.columns.tolist()
        )

    for dataframe_column in columns:
        dataframe[
            dataframe_column
        ].fillna(value="", inplace=True)

    return dataframe
