from bclearer_interop_services.delimited_text.dataframe_dictionary_to_csv_files_writer import (
    write_dataframe_dictionary_to_csv_files,
)
from bclearer_interop_services.excel.excel_write import (
    save_table_in_excel,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)
from pandas import DataFrame


@run_and_log_function
def orchestrate_standard_tables_to_xlsx_migration(
    standard_tables_dictionary: dict,
    output_folder: Folders,
):
    write_dataframe_dictionary_to_csv_files(
        folder_name=output_folder.absolute_path_string,
        dataframes_dictionary=standard_tables_dictionary,
    )

    for (
        dataframe_name,
        dataframe,
    ) in (
        standard_tables_dictionary.items()
    ):
        __export_standard_table_as_xlsx(
            dataframe=dataframe,
            dataframe_name=dataframe_name,
            output_folder=output_folder,
        )


def __export_standard_table_as_xlsx(
    dataframe: DataFrame,
    dataframe_name: str,
    output_folder: Folders,
):
    xlsx_filepath = (
        output_folder.absolute_path_string
        + "\\"
        + dataframe_name
        + ".xlsx"
    )

    save_table_in_excel(
        table=dataframe,
        full_filename=str(
            xlsx_filepath
        ),
        sheet_name=dataframe_name,
    )
