from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.relational_database_services.access_service.access_database_connection_getter import (
    get_access_database_connection,
)


# TODO: OXi - Still to be reviewed
def get_column_names_of_table_from_access_database(
    database_file: Files,
    table_name: str,
) -> list:
    database_connection = get_access_database_connection(
        database_full_file_path=database_file.absolute_path_string,
    )

    database_cursor = (
        database_connection.cursor()
    )

    column_names = [
        row.column_name
        for row in database_cursor.columns(
            table=table_name,
        )
    ]

    return column_names
