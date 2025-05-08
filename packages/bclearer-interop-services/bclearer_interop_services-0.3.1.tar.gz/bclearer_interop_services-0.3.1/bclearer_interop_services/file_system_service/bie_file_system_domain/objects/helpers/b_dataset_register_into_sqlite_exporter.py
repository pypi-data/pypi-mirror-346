from bclearer_interop_services.b_dictionary_service.table_as_dictionary_service.table_as_dictionary_to_dataframe_converter import (
    convert_table_as_dictionary_to_dataframe,
)
from bclearer_interop_services.dataframe_service.all_cells_to_string_converter import (
    convert_all_cells_to_string,
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


def export_register_into_sqlite(
    register_object,
    output_folder: Folders,
    register_output_string_name_root: str,
    register_in_b_datasets_format: dict = None,
) -> None:
    if (
        not register_in_b_datasets_format
    ):
        register_in_b_datasets_format = (
            register_object.export_register_in_b_datasets_format()
        )

    log_message(
        message="STARTING PROCESS TO EXPORT TO SQLITE",
    )

    log_message(
        message="EXPORT TO SQLITE - Converting to dataframe",
    )

    dictionary_as_table = convert_table_as_dictionary_to_dataframe(
        table_as_dictionary=register_in_b_datasets_format,
    )

    log_message(
        message="EXPORT TO SQLITE - Normalising all dataframe cells to string type",
    )

    dictionary_as_table_string_cells = convert_all_cells_to_string(
        dataframe=dictionary_as_table,
    )

    sqlite_database_file = create_sqlite_database(
        sqlite_database_folder=output_folder,
        sqlite_database_base_name=register_output_string_name_root
        + "_register",
    )

    log_message(
        message="EXPORT TO SQLITE - Writing dataframe to SQLite database",
    )

    write_dataframe_to_sqlite(
        dataframe=dictionary_as_table_string_cells,
        table_name=register_output_string_name_root
        + "_register",
        sqlite_database_file=sqlite_database_file,
        append=False,
    )
