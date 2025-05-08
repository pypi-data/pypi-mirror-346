from uuid import uuid1

import pandas


def add_uuid_column_to_dataframe(
    dataframe: pandas.DataFrame,
    column: str,
) -> pandas.DataFrame:
    dataframe[column] = dataframe.apply(
        lambda row: str(uuid1()), axis=1
    )

    first_column_uuid = dataframe.pop(
        column
    )

    dataframe.insert(
        0, column, first_column_uuid
    )

    return dataframe
