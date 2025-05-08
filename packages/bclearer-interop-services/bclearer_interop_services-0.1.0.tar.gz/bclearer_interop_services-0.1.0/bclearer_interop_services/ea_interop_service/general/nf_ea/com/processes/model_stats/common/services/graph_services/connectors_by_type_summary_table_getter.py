from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.constants import (
    EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME,
    SOURCE_COLUMN_NAME,
    TOTALS_COLUMN_NAME,
)
from pandas import DataFrame


def get_connectors_by_type_summary_table(
    edges_table: DataFrame,
) -> DataFrame:
    connectors_by_type_base_table = (
        edges_table.groupby(
            EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME
        )
        .count()
        .reset_index()
    )

    connectors_by_type_summary_table_renaming_dictionary = {
        EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME: EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME,
        SOURCE_COLUMN_NAME: TOTALS_COLUMN_NAME,
    }

    connectors_by_type_summary_table = dataframe_filter_and_rename(
        dataframe=connectors_by_type_base_table,
        filter_and_rename_dictionary=connectors_by_type_summary_table_renaming_dictionary,
    )
    return (
        connectors_by_type_summary_table
    )
