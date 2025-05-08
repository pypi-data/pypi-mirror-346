from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.relational_database_services.access_service import (
    get_access_database_connection,
)
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from pandas import read_sql_query
from pyodbc import Connection


def read_access_into_dictionary_of_dataframes(
    input_access_database_file: Files,
) -> dict:
    log_message(
        message="Reading access database into dictionary of dataframes",
    )

    access_database_connection = get_access_database_connection(
        database_full_file_path=input_access_database_file.absolute_path_string,
    )

    cursor = (
        access_database_connection.cursor()
    )

    dictionary_of_dataframes = dict()

    for row in cursor.tables(
        tableType="TABLE",
    ):
        __add_access_table_to_dictionary_of_dataframes(
            dictionary_of_dataframes=dictionary_of_dataframes,
            row=row,
            access_database_connection=access_database_connection,
        )

    access_database_connection.close()

    return dictionary_of_dataframes


def __add_access_table_to_dictionary_of_dataframes(
    dictionary_of_dataframes: dict,
    row,
    access_database_connection: Connection,
) -> None:
    table_name = row.table_name

    query_string = (
        f"SELECT * FROM [{table_name}]"
    )

    dataframe = read_sql_query(
        sql=query_string,
        con=access_database_connection,
    )

    dictionary_of_dataframes[
        table_name
    ] = dataframe
