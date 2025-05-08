from bclearer_interop_services.file_system_service.files_of_extension_from_folder_getter import (
    get_all_files_of_extension_from_folder,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.relational_database_services.access_service import (
    get_access_database_connection,
)
from bclearer_interop_services.relational_database_services.access_service.access.xlsx_file_to_access_loader import (
    load_xlsx_file_to_access,
)
from bclearer_interop_services.relational_database_services.access_service.access_database_creator import (
    create_access_database_in_folder,
)


def export_all_xlsx_files_from_folder_to_access(
    xlsx_folder: Folders,
    database_already_exists: bool,
    new_database_name_if_not_exists: str = None,
    database_full_path_if_already_exists: str = None,
) -> None:
    if database_already_exists:
        access_database_full_path = database_full_path_if_already_exists
    else:
        access_database_full_path = create_access_database_in_folder(
            parent_folder_path=xlsx_folder.absolute_path_string,
            database_name=new_database_name_if_not_exists,
        )

    database_connection = get_access_database_connection(
        database_full_file_path=access_database_full_path,
    )

    xlsx_files_to_export = get_all_files_of_extension_from_folder(
        folder=xlsx_folder,
        dot_extension_string=".xlsx",
    )

    database_file = Files(
        absolute_path_string=access_database_full_path,
    )

    for (
        xlsx_file
    ) in xlsx_files_to_export:
        load_xlsx_file_to_access(
            temporary_csv_folder=xlsx_folder,
            database_file=database_file,
            xlsx_file=xlsx_file,
        )

    database_connection.close()
