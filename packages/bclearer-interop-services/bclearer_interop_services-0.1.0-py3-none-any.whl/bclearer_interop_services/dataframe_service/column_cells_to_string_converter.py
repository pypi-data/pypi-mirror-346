import pandas


def convert_column_cells_to_string(
    column: str,
    dataframe: pandas.DataFrame,
) -> str:
    column_cells_as_string = "".join(
        dataframe[column]
        .astype(str)
        .tolist(),
    )

    return column_cells_as_string
