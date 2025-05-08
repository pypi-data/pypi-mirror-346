from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.relational_database_services.access_service.access.dataframes_to_access_writer import (
    write_dataframes_to_access,
)
from bclearer_interop_services.relational_database_services.access_service.access_database_creator import (
    create_access_database_in_folder,
)


def export_tables_to_new_ms_access_database(
    database_name: str,
    dataframes_dictionary_keyed_on_string: dict,
    temporary_csv_folder: Folders,
    output_folder: Folders,
) -> None:
    database_file_path = create_access_database_in_folder(
        parent_folder_path=output_folder.absolute_path_string,
        database_name=database_name,
    )

    database_file = Files(
        absolute_path_string=database_file_path,
    )

    write_dataframes_to_access(
        dataframes_dictionary_keyed_on_string=dataframes_dictionary_keyed_on_string,
        database_file=database_file,
        temporary_csv_folder=temporary_csv_folder,
    )
