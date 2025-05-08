from pandas import DataFrame


def convert_dataframe_into_dictionary_of_rows(
    dataframe: DataFrame,
) -> dict:
    if dataframe.index.has_duplicates:
        dataframe.reset_index(
            inplace=True
        )

    dataframe_as_dictionary_of_rows = (
        dataframe.to_dict(
            orient="index"
        )
    )

    return (
        dataframe_as_dictionary_of_rows
    )
