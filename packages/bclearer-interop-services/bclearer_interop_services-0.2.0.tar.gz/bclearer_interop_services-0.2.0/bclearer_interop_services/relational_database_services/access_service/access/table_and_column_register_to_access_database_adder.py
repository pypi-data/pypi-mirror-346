from bclearer_interop_services.delimited_text.table_as_dictionary_to_csv_exporter import (
    export_table_as_dictionary_to_csv,
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
from bclearer_interop_services.relational_database_services.access_service.access.csv_folder_to_database_loader import (
    load_database_with_table,
)
from bclearer_interop_services.relational_database_services.access_service.column_names_of_table_from_access_database_getter import (
    get_column_names_of_table_from_access_database,
)
from bclearer_interop_services.relational_database_services.access_service.table_names_from_access_database_getter import (
    get_table_names_from_access_database,
)
from nf_common.code.services.reporting_service.reporters.log_file import (
    LogFiles,
)


# TODO: OXi - Still to be reviewed
def add_table_and_column_register_to_access_database(
    target_database_file: Files,
) -> None:
    table_names = get_table_names_from_access_database(
        target_database_file=target_database_file,
    )

    table_and_column_register_dictionary = (
        dict()
    )

    for (
        table_index,
        table_name,
    ) in enumerate(table_names):
        current_table_column_names = get_column_names_of_table_from_access_database(
            database_file=target_database_file,
            table_name=table_name,
        )

        table_and_column_register_dictionary[
            table_name
        ] = current_table_column_names

    table_as_dictionary = dict()

    table_as_dictionary_index = 0

    for (
        table_name,
        column_names,
    ) in (
        table_and_column_register_dictionary.items()
    ):
        for column_name in column_names:
            table_as_dictionary[
                table_as_dictionary_index
            ] = {
                "table_names": table_name,
                "column_names": column_name,
            }

            table_as_dictionary_index += (
                1
            )

    output_csv_file_name = (
        "table_register"
    )

    output_csv_folder = Folders(
        absolute_path_string=target_database_file.parent_absolute_path_string,
    )

    LogFiles.open_log_file(
        folder_path=output_csv_folder.absolute_path_string,
    )

    export_table_as_dictionary_to_csv(
        table_as_dictionary=table_as_dictionary,
        output_folder=output_csv_folder,
        output_file_base_name=output_csv_file_name,
    )

    database_connection = get_access_database_connection(
        database_full_file_path=target_database_file.absolute_path_string,
    )

    load_database_with_table(
        db_connection=database_connection,
        table_name=output_csv_file_name
        + ".csv",
        csv_folder=output_csv_folder,
    )
