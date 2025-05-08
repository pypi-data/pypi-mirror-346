from pandas import DataFrame


def convert_dataframe_to_table_as_dictionary(
    dataframe: DataFrame,
) -> dict:
    table_as_dictionary = (
        dataframe.fillna("")
        .transpose()
        .to_dict()
    )

    return table_as_dictionary
