import pandas
from bclearer_interop_services.dataframe_service.checks.set_uniqueness_checker.check import (
    run_check,
)
from bclearer_interop_services.dataframe_service.checks.set_uniqueness_checker.organise import (
    run_organise,
)
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def run_check_set_uniqueness(
    set_table: pandas.DataFrame,
    identity_set_indices: list,
    identification_indices: list,
) -> dict:
    log_message(
        "start index uniqueness check",
    )

    set_table_duplicates = run_check(
        set_table,
        identity_set_indices,
    )

    if set_table_duplicates is None:
        log_message(
            "no duplicates were found by index uniqueness check",
        )
        return None

    log_message(
        "some duplicates were found by index uniqueness check",
    )

    log_message(
        "start organise data for uniqueness check",
    )

    summary_table = run_organise(
        set_table_duplicates,
        identity_set_indices,
        identification_indices,
    )

    log_message("end organise")

    table_dictionary = {
        "set_table_duplicates": set_table_duplicates,
        "summary_table": summary_table,
    }

    log_message(
        "stop index uniqueness check",
    )

    return table_dictionary
