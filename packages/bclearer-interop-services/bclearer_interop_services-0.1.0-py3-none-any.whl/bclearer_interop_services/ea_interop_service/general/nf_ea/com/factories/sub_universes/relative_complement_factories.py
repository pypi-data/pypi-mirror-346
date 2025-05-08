from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_focus_minus_matched_other_getter import (
    get_dataframe_focus_minus_matched_other,
)
from pandas import DataFrame


class RelativeComplementFactories:
    def __init__(
        self,
        nf_ea_com_universe,
        full_table: DataFrame,
        exception_table: DataFrame,
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

        self.full_table = full_table

        self.exception_table = (
            exception_table
        )

    def create(self) -> DataFrame:
        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        relative_complement = get_dataframe_focus_minus_matched_other(
            focus_dataframe=self.full_table,
            other_dataframe=self.exception_table,
            matched_column_name=nf_uuids_column_name,
        )

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        relative_complement = dataframe_filter_and_rename(
            dataframe=relative_complement,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name
            },
        )

        return relative_complement
