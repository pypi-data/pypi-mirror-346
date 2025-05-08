import os

import pandas as pd
from bclearer_interop_services.excel_services.object_model.excel_workbooks import (
    ExcelWorkbooks,
)
from bclearer_interop_services.file_system_service.objects.wrappers.path_wrappers import (
    PathWrappers,
)


class ExcelFacades:
    def __init__(self, file_path):

        self.file_path = PathWrappers(
            file_path
        )

        self.file_extension = (
            self.file_path.suffix()
        )

        self.workbook = ExcelWorkbooks(
            self.file_path,
            self.file_extension,
        )

    def read_cell(
        self,
        sheet_name: str,
        row_index: int,
        column_index: int,
    ):
        sheet = self.workbook.sheet(
            sheet_name,
        )

        cell = sheet.cell(
            row_index, column_index
        )

        return cell.value

    def read_sheet_to_dataframe(
        self,
        sheet_name: str,
        header_row_number: int = 1,
    ) -> pd.DataFrame:

        sheet = self.workbook.sheet(
            sheet_name,
        )

        # Convert the sheet rows into a list of lists (representing rows)
        sheet_dataframe = sheet.read_to_dataframe(
            header_row_number=header_row_number
        )

        return sheet_dataframe

    def write_cell(
        self,
        sheet_name,
        row_index,
        column_index,
        value,
    ):
        sheet = self.workbook.sheet(
            sheet_name,
        )
        sheet.cell(
            row_index, column_index
        ).value = value

    # TODO: this is not doing anything more than write cell, but later can introduce edit history feature through this
    def update_cell(
        self,
        sheet_name,
        row_index,
        column_index,
        value,
    ):

        self.write_cell(
            sheet_name,
            row_index,
            column_index,
            value,
        )

    def save(self, file_path=None):

        if file_path is None:
            file_path = (
                self.workbook.file_path
            )

        directory = os.path.dirname(
            file_path
        )

        if (
            directory
            and not os.path.exists(
                directory
            )
        ):
            os.makedirs(directory)

        self.workbook.save(file_path)
