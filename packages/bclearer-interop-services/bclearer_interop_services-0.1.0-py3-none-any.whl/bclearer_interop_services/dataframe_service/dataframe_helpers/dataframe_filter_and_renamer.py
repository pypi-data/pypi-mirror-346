import pandas


def dataframe_filter_and_rename(
    dataframe: pandas.DataFrame,
    filter_and_rename_dictionary: dict,
) -> pandas.DataFrame:
    dataframe = dataframe.filter(
        items=filter_and_rename_dictionary.keys(),
    )

    dataframe = dataframe.rename(
        columns=filter_and_rename_dictionary,
    )

    return dataframe
