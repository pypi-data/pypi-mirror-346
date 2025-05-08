from pandas import DataFrame


def replace_column_value_separator_in_dataframe_column(
    dataframe: DataFrame,
    column_name: str,
    old_separator: str,
    new_separator: str,
) -> DataFrame:
    dataframe[column_name] = dataframe[
        column_name
    ].str.replace(
        old_separator,
        new_separator,
    )

    return dataframe
