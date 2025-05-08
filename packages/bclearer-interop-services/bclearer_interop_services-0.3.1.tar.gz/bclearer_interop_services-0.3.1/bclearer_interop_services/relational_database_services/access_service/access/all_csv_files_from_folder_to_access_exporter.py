from bclearer_interop_services.file_system_service.files_of_extension_from_folder_getter import (
    get_all_files_of_extension_from_folder,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.relational_database_services.access_service import (
    get_access_database_connection,
)
from bclearer_interop_services.relational_database_services.access_service.access.csv_folder_to_database_loader import (
    load_database_with_table,
)
from bclearer_interop_services.relational_database_services.access_service.access_database_creator import (
    create_access_database_in_folder,
)


def export_all_csv_files_from_folder_to_access(
    csv_folder: Folders,
    database_already_exists: bool,
    new_database_name_if_not_exists: str = None,
    database_full_path_if_already_exists: str = None,
    export_table_column_register: bool = True,
) -> None:
    if database_already_exists:
        access_database_full_path = database_full_path_if_already_exists
    else:
        access_database_full_path = create_access_database_in_folder(
            parent_folder_path=csv_folder.absolute_path_string,
            database_name=new_database_name_if_not_exists,
        )

    database_connection = get_access_database_connection(
        database_full_file_path=access_database_full_path,
    )

    csv_files_to_export = get_all_files_of_extension_from_folder(
        folder=csv_folder,
        dot_extension_string=".csv",
    )

    for csv_file in csv_files_to_export:
        load_database_with_table(
            db_connection=database_connection,
            table_name=csv_file.base_name,
            csv_folder=csv_folder,
        )

    database_connection.close()
