import sys

# TODO: review for useful code and remove this
sys.path.append(
    r"..\bclearer_qatar_document_processor",
)
import os
import time
from io import BytesIO
from pathlib import Path

import pandas as pd
from src.blob_storage_helper import (
    BlobStorageHelper,
)
from src.utils import read_yaml


def get_sheet_name(
    blob_helper,
    blob_name,
):
    input_blob = (
        blob_helper.download_blob(
            blob_name=blob_name,
        )
    )
    try:
        excel_workbook = pd.ExcelFile(
            BytesIO(input_blob),
        )
        del input_blob
        return [
            excel_workbook.sheet_names,
            None,
        ]
    except Exception as e:
        del input_blob
        return [None, e]


def save_append(df, output_path):
    if os.path.isfile(output_path):
        df.to_csv(
            output_path,
            header=None,
            mode="a",
            index=False,
        )
    else:
        df.to_csv(
            output_path,
            index=False,
        )


def read_sheet_names(
    row,
    blob_helper,
    output_path,
):
    blob_path = row["path"]
    [sheet_names, err] = get_sheet_name(
        blob_helper=blob_helper,
        blob_name=blob_path,
    )

    if sheet_names is not None:
        print(
            f"{blob_path} has {len(sheet_names)} sheets",
        )
        sheet_report_dataframe = (
            pd.DataFrame(sheet_names)
        )
        sheet_report_dataframe[
            "path"
        ] = blob_path
        save_append(
            df=sheet_report_dataframe,
            output_path=output_path,
        )

        return pd.Series([True, None])
    return pd.Series([False, err])


if __name__ == "__main__":
    root_path = Path(
        __file__,
    ).parent.parent.parent
    config_path = (
        root_path / "config.yaml"
    )
    output_path = (
        root_path
        / "data"
        / "blob_full_list.csv"
    )
    output_path_special_char = (
        root_path
        / "data"
        / "blob_special_char_filename_list.csv"
    )

    output_path_xls = (
        root_path
        / "data"
        / "blob_xls.csv"
    )

    output_sheet_names = (
        root_path
        / "data"
        / "collect2_sheet_names.csv"
    )
    output_sheet_names_report = (
        root_path
        / "data"
        / "collect2_sheet_names_report.csv"
    )

    start = time.time()

    blob_config = read_yaml(
        config_path,
    )["blob_storage"]
    blob_storage_helper = (
        BlobStorageHelper(
            config=blob_config,
        )
    )

    df_xls = pd.read_csv(
        output_path_xls,
    )

    batch_size = 200

    print(
        f"There are {len(df_xls)} files to be processed",
    )

    for i in range(
        0,
        len(df_xls),
        batch_size,
    ):
        print(
            f"Processing position {i}...",
        )
        start_sub = time.time()
        df_sub = df_xls.iloc[
            i : min(
                i + batch_size,
                len(df_xls),
            )
        ]

        df_sub[
            ["is_conform", "err_msg"]
        ] = df_sub.apply(
            lambda x: read_sheet_names(
                x,
                blob_helper=blob_storage_helper,
                output_path=output_sheet_names,
            ),
            axis=1,
        )

        save_append(
            df=df_sub,
            output_path=output_sheet_names_report,
        )

        print(
            f"Spend {(time.time()-start_sub)/60} minutes.",
        )

    print(
        f"{time.time() - start} seconds",
    )
