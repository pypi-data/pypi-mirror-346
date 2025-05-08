import csv
import os

from bclearer_interop_services.b_dictionary_service.table_as_dictionary_service.table_as_dictionary_to_dataframe_converter import (
    convert_table_as_dictionary_to_dataframe,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


def export_table_as_dictionary_to_csv(
    table_as_dictionary: dict,
    output_folder: Folders,
    output_file_base_name: str,
) -> None:
    dictionary_as_table = convert_table_as_dictionary_to_dataframe(
        table_as_dictionary=table_as_dictionary,
    )

    output_csv_file_full_path = os.path.join(
        output_folder.absolute_path_string,
        output_file_base_name + ".csv",
    )

    dictionary_as_table.to_csv(
        path_or_buf=output_csv_file_full_path,
        sep=",",
        quotechar='"',
        index=False,
        quoting=csv.QUOTE_ALL,
        escapechar="\\",
    )
