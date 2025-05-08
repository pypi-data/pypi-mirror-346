import os.path
from sqlite3 import (
    Error,
    connect,
    version,
)

from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


def create_sqlite_database(
    sqlite_database_folder: Folders,
    sqlite_database_base_name: str,
) -> Files:
    database_connection = None

    database_file_path = os.path.join(
        sqlite_database_folder.absolute_path_string,
        sqlite_database_base_name
        + ".db",
    )

    try:
        database_connection = connect(
            database_file_path,
        )

        print(version)

    except Error as e:
        print(e)

    finally:
        if database_connection:
            database_connection.close()

    database_file = Files(
        absolute_path_string=database_file_path,
    )

    return database_file
