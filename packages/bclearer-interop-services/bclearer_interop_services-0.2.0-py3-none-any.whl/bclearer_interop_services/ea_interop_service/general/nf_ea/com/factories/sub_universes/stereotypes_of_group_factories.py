from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from pandas import DataFrame


class StereotypesOfGroupFactories:
    def __init__(
        self,
        nf_ea_com_universe,
        stereotype_group_name: str,
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

        self.stereotype_group_name = (
            stereotype_group_name
        )

    def create(self) -> DataFrame:
        ea_stereotype_groups = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_ea_stereotype_groups()
        )

        object_name_column_name = (
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name
        )

        ea_stereotype_group = ea_stereotype_groups.loc[
            ea_stereotype_groups[
                object_name_column_name
            ]
            == self.stereotype_group_name
        ]

        ea_stereotypes = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_ea_stereotypes()
        )

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        stereotype_ea_stereotype_group_column_name = (
            NfEaComColumnTypes.STEREOTYPE_EA_STEREOTYPE_GROUP.column_name
        )

        ea_stereotypes_of_group = left_merge_dataframes(
            master_dataframe=ea_stereotype_group,
            master_dataframe_key_columns=[
                nf_uuids_column_name
            ],
            merge_suffixes=[
                "_local",
                "_common",
            ],
            foreign_key_dataframe=ea_stereotypes,
            foreign_key_dataframe_fk_columns=[
                stereotype_ea_stereotype_group_column_name
            ],
            foreign_key_dataframe_other_column_rename_dictionary={
                nf_uuids_column_name: "stereotype_nf_uuids"
            },
        )

        ea_stereotypes_of_group = dataframe_filter_and_rename(
            dataframe=ea_stereotypes_of_group,
            filter_and_rename_dictionary={
                "stereotype_nf_uuids": nf_uuids_column_name
            },
        )

        return ea_stereotypes_of_group
