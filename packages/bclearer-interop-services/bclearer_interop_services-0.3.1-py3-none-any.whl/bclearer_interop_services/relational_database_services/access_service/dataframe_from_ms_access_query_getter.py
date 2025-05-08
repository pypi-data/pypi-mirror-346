import pandas
import pyodbc as odbc_library


def get_dataframe_from_ms_access_query(
    database_connection: odbc_library.Connection,
    sql_query: str,
) -> pandas.DataFrame:
    cursor = (
        database_connection.cursor()
    )

    cursor.execute(sql_query)

    records = cursor.fetchall()

    columns = [
        column[0]
        for column in cursor.description
    ]

    results = [
        tuple(row) for row in records
    ]

    dataframe = pandas.DataFrame(
        results,
        columns=columns,
        dtype=str,
    )

    return dataframe
