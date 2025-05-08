from sqlite3 import connect

from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from pandas import DataFrame


def write_dataframe_to_sqlite(
    dataframe: DataFrame,
    table_name: str,
    sqlite_database_file: Files,
    append: bool = False,
) -> None:
    if dataframe.empty:
        return

    existing_table_policy = "fail"

    # TODO: explore more connection parameters
    sqlite_database_connection = connect(
        database=sqlite_database_file.absolute_path_string,
    )

    if append:
        existing_table_policy = "append"

    # TODO: explore more writing parameters
    dataframe.to_sql(
        name=table_name,
        con=sqlite_database_connection,
        index=False,
        if_exists=existing_table_policy,
    )

    sqlite_database_connection.close()
