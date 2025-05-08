from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.relational_database_services.sqlite_service.dataframe_to_sqlite_writer import (
    write_dataframe_to_sqlite,
)
from bclearer_interop_services.relational_database_services.sqlite_service.sqlite_database_creator import (
    create_sqlite_database,
)
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def export_dictionary_of_dataframes_to_sqlite(
    dictionary_of_dataframes: dict,
    sqlite_database_base_name: str,
    output_folder: Folders,
    sqlite_database_file: Files = None,
    database_exists: bool = False,
) -> Files:
    if not database_exists:
        log_message(
            message="Creating sqlite_service database",
        )

        sqlite_database_file = create_sqlite_database(
            sqlite_database_folder=output_folder,
            sqlite_database_base_name=sqlite_database_base_name,
        )

    __export_dataframes_to_sqlite_database(
        dictionary_of_dataframes=dictionary_of_dataframes,
        sqlite_database_file=sqlite_database_file,
    )

    return sqlite_database_file


def __export_dataframes_to_sqlite_database(
    dictionary_of_dataframes: dict,
    sqlite_database_file: Files,
):
    log_message(
        message="Exporting dataframes to sqlite_service database",
    )

    for (
        table_name,
        dataframe,
    ) in (
        dictionary_of_dataframes.items()
    ):
        write_dataframe_to_sqlite(
            dataframe=dataframe,
            table_name=table_name,
            sqlite_database_file=sqlite_database_file,
        )
