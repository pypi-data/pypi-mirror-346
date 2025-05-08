import pandas
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_split_constants import (
    EQUAL_ROWS_DATAFRAME_NAME,
    NON_EQUAL_ROWS_DATAFRAME_NAME,
)


def split_on_column_equality(
    dataframe: pandas.DataFrame,
    first_column_name: str,
    second_column_name: str,
) -> dict:
    dataframe_of_equal_rows = (
        dataframe.loc[
            dataframe[first_column_name]
            == dataframe[
                second_column_name
            ]
        ]
    )

    dataframe_of_non_equal_rows = (
        dataframe.loc[
            ~(
                dataframe[
                    first_column_name
                ]
                == dataframe[
                    second_column_name
                ]
            )
        ]
    )

    result_dictionary = {
        EQUAL_ROWS_DATAFRAME_NAME: dataframe_of_equal_rows,
        NON_EQUAL_ROWS_DATAFRAME_NAME: dataframe_of_non_equal_rows,
    }

    return result_dictionary
