# from bclearer_interop_services.excel_services.object_model.excel_cells import (
#     ExcelCells,
# )
from openpyxl.worksheet.worksheet import (
    Worksheet as OpenpyxlWorksheet,
)


class ExcelRows:
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
    #     col_index: int,
    # ):
    #     return ExcelCells(
    #         self.sheet.cell(
    #             row=self.index,
    #             column=col_index,
    #         ),
    #     )
    #
    # def __iter__(self):
    #     for cell in self.sheet[
    #         self.index
    #     ]:
    #         yield ExcelCells(cell)
