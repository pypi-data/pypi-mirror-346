from pandas import DataFrame


def replace_string_value_across_whole_dataframe(
    dataframe: DataFrame,
    old_value_as_string: str,
    new_value_as_string: str,
) -> DataFrame:
    cleaned_dataframe = dataframe.replace(
        to_replace=old_value_as_string,
        value=new_value_as_string,
        regex=True,
    )

    return cleaned_dataframe
