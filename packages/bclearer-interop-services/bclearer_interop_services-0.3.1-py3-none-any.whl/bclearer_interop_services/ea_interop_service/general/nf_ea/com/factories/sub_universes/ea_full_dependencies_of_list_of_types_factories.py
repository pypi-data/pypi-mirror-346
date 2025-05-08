from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
from pandas import DataFrame


class EaFullDependenciesOfListOfTypesFactories:
    def __init__(
        self,
        nf_ea_com_universe,
        list_of_types: DataFrame,
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

        self.list_of_types = (
            list_of_types
        )

    def create(self) -> DataFrame:
        ea_full_dependencies = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_ea_full_dependencies()
        )

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        ea_full_dependencies_of_list_of_types = left_merge_dataframes(
            master_dataframe=self.list_of_types,
            master_dataframe_key_columns=[
                nf_uuids_column_name
            ],
            merge_suffixes=[
                "_local",
                "_common",
            ],
            foreign_key_dataframe=ea_full_dependencies,
            foreign_key_dataframe_fk_columns=[
                "provider"
            ],
            foreign_key_dataframe_other_column_rename_dictionary={
                "dependent": "dependent"
            },
        )

        ea_full_dependencies_of_list_of_types = ea_full_dependencies_of_list_of_types.fillna(
            DEFAULT_NULL_VALUE
        )

        ea_full_dependencies_of_list_of_types = ea_full_dependencies_of_list_of_types.loc[
            ea_full_dependencies_of_list_of_types[
                "dependent"
            ]
            != DEFAULT_NULL_VALUE
        ]

        ea_full_dependencies_of_list_of_types = (
            ea_full_dependencies_of_list_of_types.drop_duplicates()
        )

        ea_full_dependencies_of_list_of_types = dataframe_filter_and_rename(
            dataframe=ea_full_dependencies_of_list_of_types,
            filter_and_rename_dictionary={
                "dependent": nf_uuids_column_name
            },
        )

        return ea_full_dependencies_of_list_of_types
