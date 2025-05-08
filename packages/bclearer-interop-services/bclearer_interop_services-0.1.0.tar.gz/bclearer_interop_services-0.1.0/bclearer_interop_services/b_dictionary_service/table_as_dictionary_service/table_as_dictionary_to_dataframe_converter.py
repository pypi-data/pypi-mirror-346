from pandas import DataFrame


def convert_table_as_dictionary_to_dataframe(
    table_as_dictionary: dict,
) -> DataFrame:
    output_dataframe = DataFrame(
        table_as_dictionary,
    )

    output_dataframe = (
        output_dataframe.transpose()
    )

    output_dataframe = (
        output_dataframe.reset_index(
            drop=True,
        )
    )

    return output_dataframe
