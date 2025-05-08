from bclearer_interop_services.excel_services.interop.xlsx_to_dataframe_dictionary_converter import (
    covert_xlxs_to_dataframe_dictionary,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.relational_database_services.access_service.access.dataframes_to_access_writer import (
    write_dataframes_to_access,
)


def load_xlsx_file_to_access(
    temporary_csv_folder: Folders,
    database_file: Files,
    xlsx_file: Files,
) -> None:
    sheet_dataframe_dictionary = covert_xlxs_to_dataframe_dictionary(
        xlsx_file=xlsx_file,
    )

    write_dataframes_to_access(
        dataframes_dictionary_keyed_on_string=sheet_dataframe_dictionary,
        database_file=database_file,
        temporary_csv_folder=temporary_csv_folder,
    )
