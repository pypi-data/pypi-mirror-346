from pandas import DataFrame, concat


def concatenate_dictionary_of_dataframes(
    dataframe_dictionary: dict,
) -> DataFrame:
    dictionary_of_dataframes_list = []

    for (
        table_name,
        dataframe,
    ) in dataframe_dictionary.items():
        dictionary_of_dataframes_list.append(
            dataframe,
        )

    concatenated_dataframe = concat(
        dictionary_of_dataframes_list,
    ).reset_index(drop=True)

    return concatenated_dataframe
