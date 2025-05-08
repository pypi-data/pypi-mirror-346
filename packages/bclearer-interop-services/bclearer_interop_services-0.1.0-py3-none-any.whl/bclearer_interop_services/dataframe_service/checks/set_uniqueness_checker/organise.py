from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from pandas import DataFrame


def run_organise(
    set_table_duplicates: DataFrame,
    identity_set_indices: list,
    identification_indices: list,
) -> DataFrame:
    set_table_duplicates_copy = (
        set_table_duplicates.copy()
    )

    filtered_column_names = (
        identity_set_indices
        + identification_indices
    )

    filtered_set_table_duplicates = set_table_duplicates_copy.filter(
        items=filtered_column_names,
    )

    filtered_set_table_duplicates = filtered_set_table_duplicates.fillna(
        DEFAULT_NULL_VALUE,
    )

    grouped_set_table_duplicates = (
        filtered_set_table_duplicates.groupby(
            filtered_set_table_duplicates.columns.tolist(),
        )
        .size()
        .reset_index()
        .rename(columns={0: "count"})
    )

    grouped_set_table_duplicates[
        "parameter_names"
    ] = ", ".join(filtered_column_names)

    filtered_columns = grouped_set_table_duplicates.filter(
        items=filtered_column_names,
    )

    grouped_set_table_duplicates[
        "parameter_values"
    ] = filtered_columns.apply(
        lambda x: ", ".join(
            x.astype(str)
            .dropna()
            .values.tolist(),
        ),
        axis=1,
    )

    grouped_set_table_duplicates = grouped_set_table_duplicates.drop(
        columns=filtered_column_names,
    )

    return grouped_set_table_duplicates
