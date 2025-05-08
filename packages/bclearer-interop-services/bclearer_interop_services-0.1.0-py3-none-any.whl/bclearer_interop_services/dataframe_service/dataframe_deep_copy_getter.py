from pandas import DataFrame


def get_dataframe_deep_copy(
    dataframe: DataFrame,
) -> DataFrame:
    deep_copy_dataframe = (
        dataframe.copy(deep=True)
    )

    return deep_copy_dataframe
