# TODO - retire this

import pandas as pd


class Cell:
    def __init__(self, value):
        self.value = value


class Column:
    def __init__(self, cells):
        self.cells = [
            Cell(cell) for cell in cells
        ]


class Row:
    def __init__(self, cells):
        self.cells = [
            Cell(cell) for cell in cells
        ]


class Sheet:
    def __init__(self, dataframe):
        self.columns = [
            Column(dataframe[col])
            for col in dataframe.columns
        ]
        self.rows = [
            Row(dataframe.iloc[i])
            for i in range(
                len(dataframe),
            )
        ]


class Workbook:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_type = (
            file_path.split(".")[-1]
        )
        self.sheets = (
            self._load_sheets()
        )

    def _load_sheets(self):
        if self.file_type == "xlsx":
            excel_file = pd.ExcelFile(
                self.file_path,
                engine="openpyxl",
            )
        elif self.file_type == "xls":
            excel_file = pd.ExcelFile(
                self.file_path,
                engine="xlrd",
            )
        else:
            raise ValueError(
                "Unsupported file type. Please provide a .xls or .xlsx file.",
            )

        sheets = {}
        for (
            sheet_name
        ) in excel_file.sheet_names:
            dataframe = (
                excel_file.parse(
                    sheet_name,
                )
            )
            sheets[sheet_name] = Sheet(
                dataframe,
            )

        return sheets
