import pyodbc as odbc_library


def get_all_user_tables_from_database(
    database_connection: odbc_library.Connection,
) -> list:
    table_names = list()

    cursor = (
        database_connection.cursor()
    )

    if "pyodbc" in str(
        type(database_connection),
    ):
        for row in cursor.tables(
            tableType="TABLE",
        ):
            table_names.append(
                (row.table_name, ""),
            )

        for row in cursor.tables(
            tableType="VIEW",
        ):
            table_names.append(
                (row.table_name, ""),
            )

    elif "sqlite3" in str(
        type(database_connection),
    ):
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table';",
        )

        table_names = cursor.fetchall()

    else:
        raise NotImplementedError(
            "Extension type not implemented.",
        )

    table_names.sort(reverse=False)

    return table_names
