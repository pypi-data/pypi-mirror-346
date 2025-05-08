from bclearer_core.nf.types.column_types import (
    ColumnTypes,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from pandas import DataFrame


class TableSubTypesFactories:
    def __init__(
        self,
        nf_ea_com_universe,
        table: DataFrame,
        type_column: ColumnTypes,
        object_types: list,
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

        self.table = table

        self.type_column = type_column

        self.object_types = object_types

    def create(self) -> DataFrame:
        table = self.table

        type_column_name = (
            self.type_column.column_name
        )

        object_types = self.object_types

        table_sub_types = table.loc[
            table[
                type_column_name
            ].isin(object_types)
        ]

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        table_sub_types = dataframe_filter_and_rename(
            dataframe=table_sub_types,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name
            },
        )

        return table_sub_types
