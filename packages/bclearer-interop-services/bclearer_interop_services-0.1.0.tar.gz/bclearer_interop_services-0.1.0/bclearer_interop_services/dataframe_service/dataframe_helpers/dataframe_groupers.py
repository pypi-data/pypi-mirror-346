import pandas
from pandas.core.groupby import (
    SeriesGroupBy,
)


def group_and_sum_dataframe(
    dataframe: pandas.DataFrame,
    grouped_by_column_names_list: list,
    column_to_sum_name: str,
    result_column_name: str,
) -> pandas.DataFrame:
    group_by_series = __create_group_series(
        dataframe=dataframe,
        grouped_by_column_names_list=grouped_by_column_names_list,
        column_to_group_name=column_to_sum_name,
    )

    grouped_dataframe = (
        group_by_series.agg(
            {result_column_name: "sum"},
        ).reset_index()
    )

    return grouped_dataframe


def __create_group_series(
    dataframe: pandas.DataFrame,
    grouped_by_column_names_list: list,
    column_to_group_name: str,
) -> SeriesGroupBy:
    group_by_series = dataframe.groupby(
        grouped_by_column_names_list,
    )[column_to_group_name]

    return group_by_series
