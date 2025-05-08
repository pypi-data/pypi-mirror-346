from bclearer_core.constants.standard_constants import (
    DEFAULT_FOREIGN_TABLE_SUFFIX,
    DEFAULT_MASTER_TABLE_SUFFIX,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_focus_minus_matched_other_getter import (
    get_dataframe_focus_minus_matched_other,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    inner_merge_dataframes,
)
from pandas import DataFrame, concat


class IntersectionAndSymmetricDifferenceFactories:
    def __init__(
        self,
        nf_ea_com_universe,
        input_table_1: DataFrame,
        input_table_2: DataFrame,
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

        self.input_table_1 = (
            input_table_1
        )

        self.input_table_2 = (
            input_table_2
        )

    def create(self) -> DataFrame:
        table_1 = (
            self.__get_filtered_table(
                table=self.input_table_1
            )
        )

        table_2 = (
            self.__get_filtered_table(
                table=self.input_table_2
            )
        )

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        intersection = inner_merge_dataframes(
            master_dataframe=table_1,
            master_dataframe_key_columns=[
                nf_uuids_column_name
            ],
            merge_suffixes=[
                DEFAULT_MASTER_TABLE_SUFFIX,
                DEFAULT_FOREIGN_TABLE_SUFFIX,
            ],
            foreign_key_dataframe=table_2,
            foreign_key_dataframe_fk_columns=[
                nf_uuids_column_name
            ],
        )

        intersection["match_types"] = (
            "intersection"
        )

        symmetric_difference_in_table_1 = get_dataframe_focus_minus_matched_other(
            focus_dataframe=table_1,
            other_dataframe=table_2,
            matched_column_name=nf_uuids_column_name,
        )

        symmetric_difference_in_table_1[
            "match_types"
        ] = (
            "in "
            + self.input_table_1.name
            + " only"
        )

        symmetric_difference_in_table_2 = get_dataframe_focus_minus_matched_other(
            focus_dataframe=table_2,
            other_dataframe=table_1,
            matched_column_name=nf_uuids_column_name,
        )

        symmetric_difference_in_table_2[
            "match_types"
        ] = (
            "in "
            + self.input_table_2.name
            + " only"
        )

        intersection_and_symmetric_difference = concat(
            [
                intersection,
                symmetric_difference_in_table_1,
                symmetric_difference_in_table_2,
            ]
        )

        return intersection_and_symmetric_difference

    @staticmethod
    def __get_filtered_table(
        table: DataFrame,
    ) -> DataFrame:
        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        filtered_table = table.filter(
            items=[nf_uuids_column_name]
        )

        return filtered_table
