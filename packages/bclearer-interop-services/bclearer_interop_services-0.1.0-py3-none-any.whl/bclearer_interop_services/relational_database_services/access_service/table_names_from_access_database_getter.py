from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.relational_database_services.access_service.access_database_connection_getter import (
    get_access_database_connection,
)


# TODO: OXi - Still to be reviewed
def get_table_names_from_access_database(
    target_database_file: Files,
) -> list:
    database_connection = get_access_database_connection(
        database_full_file_path=target_database_file.absolute_path_string,
    )

    database_cursor = (
        database_connection.cursor()
    )

    table_names = [
        table.table_name
        for table in database_cursor.tables()
        if "MSys"
        not in table.table_name
    ]

    return table_names
