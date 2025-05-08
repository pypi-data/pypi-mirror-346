from bclearer_core.constants.standard_constants import (
    DEFAULT_FOREIGN_TABLE_SUFFIX,
    DEFAULT_MASTER_TABLE_SUFFIX,
    DEFAULT_NULL_VALUE,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    inner_merge_dataframes,
)
from pandas import DataFrame, concat


class EaFullPackagesFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_full_packages = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_ea_nearest_packages()
        )

        next_level = self.__get_next_level(
            ea_full_packages=ea_full_packages
        )

        while (
            next_level.shape[0]
            > ea_full_packages.shape[0]
        ):
            ea_full_packages = (
                next_level
            )

            next_level = self.__get_next_level(
                ea_full_packages=ea_full_packages
            )

        return ea_full_packages

    @staticmethod
    def __get_next_level(
        ea_full_packages,
    ):
        next_level = inner_merge_dataframes(
            master_dataframe=ea_full_packages,
            master_dataframe_key_columns=[
                "child"
            ],
            merge_suffixes=[
                DEFAULT_MASTER_TABLE_SUFFIX,
                DEFAULT_FOREIGN_TABLE_SUFFIX,
            ],
            foreign_key_dataframe=ea_full_packages,
            foreign_key_dataframe_fk_columns=[
                "parent"
            ],
            foreign_key_dataframe_other_column_rename_dictionary={
                "child": "next_level_child",
                "object_type": "next_level_object_type",
            },
        )

        next_level = dataframe_filter_and_rename(
            dataframe=next_level,
            filter_and_rename_dictionary={
                "parent": "parent",
                "next_level_child": "child",
                "next_level_object_type": "object_type",
            },
        )

        next_level = next_level.fillna(
            DEFAULT_NULL_VALUE
        )

        next_level = next_level.loc[
            next_level["child"]
            != DEFAULT_NULL_VALUE
        ]

        next_level = concat(
            [
                ea_full_packages,
                next_level,
            ]
        )

        next_level = (
            next_level.drop_duplicates()
        )

        return next_level
