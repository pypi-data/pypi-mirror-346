from bclearer_interop_services.excel_services.object_model.excel_cell_coordinates import (
    CellCoordinates,
)
from openpyxl.cell.cell import (
    Cell as OpenpyxlCell,
)


class ExcelCells:
    def __init__(
        self,
        cell: OpenpyxlCell,
        cell_coordinates: CellCoordinates,
    ):
        self.cell = cell
        self.cell_value = cell.value
        self.cell_coordinate = (
            cell_coordinates
        )
        self.cell_row = cell.row

    @property
    def value(self):
        return self.cell.value

    @value.setter
    def value(self, value):
        self.cell.value = value

    @property
    def coordinate(self):
        return self.cell.coordinate
