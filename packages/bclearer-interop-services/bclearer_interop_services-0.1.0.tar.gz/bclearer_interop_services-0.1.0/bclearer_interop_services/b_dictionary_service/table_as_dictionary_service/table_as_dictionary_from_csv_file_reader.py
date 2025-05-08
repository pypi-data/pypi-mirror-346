from bclearer_interop_services.b_dictionary_service.table_as_dictionary_service.dataframe_to_table_as_dictionary_converter import (
    convert_dataframe_to_table_as_dictionary,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from pandas import read_csv


def read_table_as_dictionary_from_csv_file(
    csv_file: Files,
) -> dict:
    csv_file_as_table = read_csv(
        csv_file.absolute_path_string,
        sep=",",
        dtype=str,
    )

    csv_file_as_dictionary = convert_dataframe_to_table_as_dictionary(
        dataframe=csv_file_as_table,
    )

    return csv_file_as_dictionary
