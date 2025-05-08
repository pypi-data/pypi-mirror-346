from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from pandas import read_excel


# TODO:move to excel facade
def covert_xlxs_to_dataframe_dictionary(
    xlsx_file: Files,
) -> dict:
    dataframe_dictionary = read_excel(
        xlsx_file.absolute_path_string,
        sheet_name=None,
        engine="openpyxl",
    )

    return dataframe_dictionary
