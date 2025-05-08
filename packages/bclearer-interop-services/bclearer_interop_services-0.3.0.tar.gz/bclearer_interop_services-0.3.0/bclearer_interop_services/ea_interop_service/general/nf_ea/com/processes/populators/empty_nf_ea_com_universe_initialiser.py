import importlib
import os

import pyodbc
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from pandas import (
    DataFrame,
    read_sql_query,
)


def create_empty_nf_ea_com_dictionary_of_collections() -> (
    dict
):
    database_connection = (
        __get_database_connection()
    )

    dictionary_of_collections = __import_tables_from_database(
        database_connection=database_connection
    )

    return dictionary_of_collections


def __get_database_connection():
    module = importlib.import_module(
        name="bclearer_interop_services.ea_interop_service.resources.templates"
    )

    module_path_string = (
        module.__path__._path[0]
    )

    resource_full_file_name = (
        os.path.join(
            module_path_string,
            "empty_nf_ea_com.accdb",
        )
    )

    database_connection = __connect_with_access_database(
        access_database_full_path=resource_full_file_name
    )

    return database_connection


def __connect_with_access_database(
    access_database_full_path: str,
) -> pyodbc.Connection:
    access_driver = r"{Microsoft Access Driver (*.mdb, *.accdb)}"

    connection_string = (
        r"Driver={};DBQ={}".format(
            access_driver,
            access_database_full_path,
        )
    )

    database_connection = (
        pyodbc.connect(
            connection_string
        )
    )

    return database_connection


def __import_tables_from_database(
    database_connection: pyodbc.Connection,
) -> dict:
    table_names_list = __import_table_names_list_from_database(
        database_connection=database_connection
    )

    dictionary_of_input_dataframes = __get_dictionary_of_tables_from_database(
        table_names_list=table_names_list,
        database_connection=database_connection,
    )

    return (
        dictionary_of_input_dataframes
    )


def __get_dictionary_of_tables_from_database(
    table_names_list: list,
    database_connection: pyodbc.Connection,
) -> dict:
    dictionary_of_dataframes = {}

    for table_name in table_names_list:
        __add_table_to_dictionary(
            table_name=table_name,
            database_connection=database_connection,
            dictionary_of_dataframes=dictionary_of_dataframes,
        )

    return dictionary_of_dataframes


def __add_table_to_dictionary(
    table_name: str,
    database_connection: pyodbc.Connection,
    dictionary_of_dataframes: dict,
):
    dataframe = __import_dataframe_from_database(
        table_name=table_name,
        database_connection=database_connection,
    )

    collection_type = NfEaComCollectionTypes.get_collection_type_from_name(
        name=table_name
    )

    if not collection_type:
        raise NotImplementedError()

    dictionary_of_dataframes[
        collection_type
    ] = dataframe


def __import_table_names_list_from_database(
    database_connection: pyodbc.Connection,
) -> list:
    table_names_list_name = (
        "table_name_list"
    )

    select_query = (
        "SELECT * FROM {}".format(
            table_names_list_name
        )
    )

    # table_names_dataframe = (
    #     read_sql_query(
    #         select_query,
    #         database_connection,
    #     )
    # )
    #
    # list_of_table_names = (
    #     table_names_dataframe[
    #         "name"
    #     ].tolist()
    # )
    cursor = (
        database_connection.cursor()
    )
    cursor.execute(select_query)
    rows = cursor.fetchall()

    list_of_table_names = [
        row[0] for row in rows
    ]

    return list_of_table_names


def __import_dataframe_from_database(
    table_name: str,
    database_connection: pyodbc.Connection,
) -> DataFrame:
    select_query = (
        f"SELECT * FROM {table_name}"
    )

    # Execute the query using pyodbc
    cursor = (
        database_connection.cursor()
    )
    cursor.execute(select_query)

    # Fetch the data and column names
    rows = cursor.fetchall()
    columns = [
        column[0]
        for column in cursor.description
    ]

    # Convert to a pandas DataFrame
    dataframe = DataFrame.from_records(
        rows, columns=columns
    )

    return dataframe


# def __import_dataframe_from_database(
#     table_name: str,
#     database_connection: pyodbc.Connection,
# ) -> DataFrame:
#     select_query = (
#         "SELECT * FROM {}".format(
#             table_name
#         )
#     )
#
#     dataframe = read_sql_query(
#         select_query,
#         database_connection,
#     )
#
#     return dataframe
