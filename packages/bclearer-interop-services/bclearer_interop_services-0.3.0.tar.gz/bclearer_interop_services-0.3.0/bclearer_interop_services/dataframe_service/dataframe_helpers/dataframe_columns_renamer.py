import pandas


def rename_dataframe_columns(
    dataframe: pandas.DataFrame,
    mappings: dict,
) -> pandas.DataFrame:
    renamed_dataframe = (
        dataframe.rename(
            columns=mappings,
        )
    )

    return renamed_dataframe
