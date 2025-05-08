from bclearer_interop_services.excel_services.object_model.excel_columns import (
    ExcelColumns,
)
from bclearer_interop_services.excel_services.object_model.excel_rows import (
    ExcelRows,
)


class CellCoordinates:
    def __init__(
        self,
        row: ExcelRows,
        column: ExcelColumns,
    ):

        self.row = row
        self.column = column
