import pandas


def dataframes_have_same_columns(
    dataframe_1: pandas.DataFrame,
    dataframe_2: pandas.DataFrame,
):
    columns_1 = set(
        dataframe_1.columns.values,
    )

    columns_2 = set(
        dataframe_2.columns.values,
    )

    return columns_1 == columns_2
