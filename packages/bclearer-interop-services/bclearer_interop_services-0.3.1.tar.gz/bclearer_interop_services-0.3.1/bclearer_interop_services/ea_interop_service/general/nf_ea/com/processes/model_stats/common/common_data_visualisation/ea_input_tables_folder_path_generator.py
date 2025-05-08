from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.services.file_folder_services.folder_selector_with_title_message import (
    select_folder_with_title_message,
)


def generate_ea_input_tables_folder_path() -> (
    str
):
    ea_input_tables_tables_folder = select_folder_with_title_message(
        title="EA_input_tables_folder"
    )

    ea_input_tables_tables_folder_path = (
        ea_input_tables_tables_folder.absolute_path_string
    )

    return ea_input_tables_tables_folder_path
