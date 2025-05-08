from bclearer_interop_services.delimited_text.table_as_dictionary_to_csv_exporter import (
    export_table_as_dictionary_to_csv,
)
from bclearer_interop_services.file_system_service.new_folder_creator import (
    create_new_folder,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.relational_database_services.access_service.access.all_csv_files_from_folder_to_access_exporter import (
    export_all_csv_files_from_folder_to_access,
)
from nf_common.code.services.datetime_service.time_helpers.time_getter import (
    now_time_as_string_for_files,
)
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def export_b_dataset_register_into_access(
    register_object,
    output_folder: Folders,
    register_output_string_name_root: str,
    register_in_b_datasets_format: dict = None,
) -> None:
    register_output_file_base_name = (
        register_output_string_name_root
        + "_register"
    )

    register_output_root_folder_path = create_new_folder(
        parent_folder_path=output_folder.absolute_path_string,
        new_folder_name=register_output_string_name_root
        + "_"
        + now_time_as_string_for_files(),
    )

    register_output_folder = Folders(
        absolute_path_string=register_output_root_folder_path,
    )

    if (
        not register_in_b_datasets_format
    ):
        register_in_b_datasets_format = (
            register_object.export_register_in_b_datasets_format()
        )

    log_message(
        message="STARTING TO EXPORT TO CSV",
    )

    export_table_as_dictionary_to_csv(
        table_as_dictionary=register_in_b_datasets_format,
        output_folder=register_output_folder,
        output_file_base_name=register_output_file_base_name,
    )

    log_message(
        message="STARTING TO EXPORT TO ACCESS",
    )

    export_all_csv_files_from_folder_to_access(
        csv_folder=register_output_folder,
        database_already_exists=False,
        new_database_name_if_not_exists=register_output_file_base_name,
    )
