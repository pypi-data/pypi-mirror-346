from bclearer_interop_services.excel_services.excel_facades import (
    ExcelFacades,
)


def extract_dataframe_from_excel_sheet(
    excel_file_path_and_name: str,
    excel_sheet_name: str,
):
    try:
        excel_facade = ExcelFacades(
            excel_file_path_and_name,
        )
        print(
            f"Successfully initialized ExcelFacade with file: {excel_file_path_and_name}",
        )

        excel_sheet_dataframe = excel_facade.read_sheet_to_dataframe(
            sheet_name=excel_sheet_name
        )

        return excel_sheet_dataframe

    except Exception as e:

        raise Exception(
            f"error reading sheet: {excel_sheet_name} in file file {excel_file_path_and_name} : {e}"
        )
