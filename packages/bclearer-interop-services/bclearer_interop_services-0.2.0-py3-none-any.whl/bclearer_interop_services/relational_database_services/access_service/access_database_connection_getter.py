import pyodbc


def get_access_database_connection(
    database_full_file_path: str,
) -> pyodbc.Connection:
    database_connection_string = (
        "Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
        + "Dbq="
        + database_full_file_path
        + ";"
    )

    database_connection = (
        pyodbc.connect(
            database_connection_string,
            autocommit=True,
        )
    )

    return database_connection
