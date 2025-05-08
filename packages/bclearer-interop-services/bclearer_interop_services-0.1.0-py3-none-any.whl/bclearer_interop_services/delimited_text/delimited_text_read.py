import filecmp
import os
import sys
from typing import List, Optional, Union

import pandas
from bclearer_interop_services.file_system_service.encoding.file_encoding_detector import (
    detect,
)


def get_table_from_csv_with_header(
    relative_filename: (
        str | os.PathLike
    ),
    file_encoding: str,
    sep: str = ",",
    custom_header: (
        list[str] | None
    ) = None,
    na_values: list[str] | None = None,
):
    if na_values is None:
        na_values = [""]

    read_csv_params = {
        "dtype": object,
        "encoding": file_encoding,
        "keep_default_na": False,
        "na_values": na_values,
        "sep": sep,
    }

    if custom_header:
        read_csv_params["header"] = None
        data_frame = pandas.read_csv(
            relative_filename,
            **read_csv_params,
        )
        data_frame.columns = (
            custom_header
        )

    else:
        data_frame = pandas.read_csv(
            relative_filename,
            **read_csv_params,
        )

    return data_frame


def get_table_from_csv_with_header_with_encoding_detection(
    relative_filename: str,
    custom_header: (
        list[str] | None
    ) = None,
):
    file_encoding = detect(
        relative_filename,
    )

    data_frame = (
        get_table_from_csv_with_header(
            relative_filename,
            file_encoding=file_encoding,
            custom_header=custom_header,
        )
    )

    return data_frame


def __check_if_read_was_successful(
    dataframe: pandas.DataFrame,
    source_relative_filename: str,
    file_encoding: str,
    sep: str,
):
    read_file_relative_filename = source_relative_filename.replace(
        ".csv",
        "_read.csv",
    )

    dataframe.to_csv(
        path_or_buf=read_file_relative_filename,
        encoding=file_encoding,
        sep=sep,
        index=False,
    )

    filecmp.clear_cache()

    read_was_successful = filecmp.cmp(
        source_relative_filename,
        read_file_relative_filename,
        shallow=False,
    )

    if read_was_successful:
        os.remove(
            read_file_relative_filename,
        )

        return

    sys.exit(
        "Load was terminated because data was corrupted while reading from "
        + source_relative_filename,
    )
