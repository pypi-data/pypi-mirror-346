from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.constants import (
    STATS_COLUMN_NAME,
    TOTALS_COLUMN_NAME,
)
from pandas import DataFrame


def create_summary_table_from_names_and_values_lists(
    names: list, values: list
) -> DataFrame:
    summary_table_dictionary = {
        STATS_COLUMN_NAME: names,
        TOTALS_COLUMN_NAME: values,
    }

    summary_table = DataFrame.from_dict(
        data=summary_table_dictionary
    )

    return summary_table
