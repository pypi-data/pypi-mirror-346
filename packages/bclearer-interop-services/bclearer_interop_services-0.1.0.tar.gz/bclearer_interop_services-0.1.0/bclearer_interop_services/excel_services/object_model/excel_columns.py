# from bclearer_interop_services.excel_services.object_model.excel_cells import (
#     ExcelCells,
# )
from openpyxl.worksheet.worksheet import (
    Worksheet as OpenpyxlWorksheet,
)


class ExcelColumns:
    def __init__(
        self,
        sheet: OpenpyxlWorksheet,
        index: int,
    ):
        self.sheet = sheet
        self.index = index

    #
    # def __getitem__(
    #     self,
    #     row_index: int,
    # ):
    #     return ExcelCells(
    #         self.sheet.cell(
    #             row=row_index,
    #             column=self.index,
    #         ),
    #     )
    #
    # def __iter__(self):
    #     for row in self.sheet.iter_rows(
    #         min_col=self.index,
    #         max_col=self.index,
    #     ):
    #         yield ExcelCells(row[0])
