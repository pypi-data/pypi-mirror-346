import pandas


def split_dataframe(
    dataframe: pandas.DataFrame,
    column_to_split_on: str,
) -> dict:
    dataframe_split_dictionary = dict()

    for (
        value_split,
        dataframe_split,
    ) in dataframe.groupby(
        column_to_split_on,
    ):
        dataframe_split_dictionary[
            value_split
        ] = dataframe_split

    return dataframe_split_dictionary
