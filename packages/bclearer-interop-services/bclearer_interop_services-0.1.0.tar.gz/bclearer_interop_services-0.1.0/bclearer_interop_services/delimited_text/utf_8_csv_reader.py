import filecmp
import os
import sys

import pandas
from bclearer_core.constants.standard_constants import (
    UTF_8_ENCODING_NAME,
)
from bclearer_interop_services.file_system_service.encoding import (
    detect,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)


def convert_utf_8_csv_with_header_file_to_dataframe(
    utf_8_csv_file: Files,
) -> pandas.DataFrame:
    dataframe = get_table_from_csv_with_header(
        relative_filename=utf_8_csv_file.absolute_path_string,
        file_encoding=UTF_8_ENCODING_NAME,
        sep=",",
    )

    return dataframe


def get_table_from_csv_with_header(
    relative_filename: str,
    file_encoding: str,
    sep: str,
):
    data_frame = pandas.read_csv(
        relative_filename,
        dtype=object,
        encoding=file_encoding,
        keep_default_na=False,
        na_values=[""],
        sep=sep,
    )

    return data_frame


def get_table_from_csv_with_header_with_encoding_detection(
    relative_filename: str,
):
    file_encoding = detect(
        relative_filename,
    )

    data_frame = pandas.read_csv(
        relative_filename,
        encoding=file_encoding,
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
