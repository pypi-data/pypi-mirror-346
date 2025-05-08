import pandas as python_data_analysis_library


# TODO, move merge with Sheet class methods
def save_table_in_excel(
    table: python_data_analysis_library.DataFrame,
    full_filename: str,
    sheet_name: str,
):
    writer = python_data_analysis_library.ExcelWriter(
        path=full_filename,
        engine="xlsxwriter",
    )

    table.to_excel(
        writer,
        sheet_name=sheet_name,
        index=False,
    )

    writer.close()
