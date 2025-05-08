import os

import pandas as pd


# TODO: move to save functionality on workbook/excel facade
def convert_to_csv(xlsx_path):
    print(f"Reading {xlsx_path}")

    csv_path = xlsx_path.replace(
        ".XLSX",
        ".csv",
    )

    if not os.path.isfile(csv_path):
        try:
            df = pd.read_excel(
                xlsx_path,
            )
            df.to_csv(
                csv_path,
                index=False,
            )
            print(
                f"Converted {xlsx_path} to csv.",
            )
        except:
            print(
                f"Error converting {xlsx_path}",
            )
    else:
        print(
            "The .csv file already exists.",
        )


def convert_excel_to_csv(
    tables_folder_path,
):
    file_paths = [
        os.path.join(dp, f)
        for dp, dn, filenames in os.walk(
            tables_folder_path,
        )
        for f in filenames
        if os.path.splitext(f)[1]
        == ".XLSX"
    ]

    for file_path in file_paths:
        if file_path.endswith(".XLSX"):
            convert_to_csv(
                xlsx_path=file_path,
            )
        else:
            print(
                f"Found non excel file {file_path}",
            )
