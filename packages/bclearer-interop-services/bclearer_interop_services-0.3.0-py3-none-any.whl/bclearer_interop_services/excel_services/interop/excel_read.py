from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from pandas import read_excel


def convert_sheet_with_header_to_dataframe(
    file_name: str,
    sheet_name: str,
):
    try:
        dataframe = read_excel(
            io=file_name,
            dtype=object,
            sheet_name=sheet_name,
            header=0,
        )
        return dataframe
    except Exception as read_fail:
        log_message(
            message="Was not able to read from "
            + file_name
            + " because "
            + str(read_fail),
        )

        return DEFAULT_NULL_VALUE
