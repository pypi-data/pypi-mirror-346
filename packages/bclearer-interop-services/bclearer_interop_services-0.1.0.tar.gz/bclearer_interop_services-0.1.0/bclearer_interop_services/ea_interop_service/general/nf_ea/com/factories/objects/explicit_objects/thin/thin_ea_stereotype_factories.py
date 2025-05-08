from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_standardiser import (
    fill_up_all_empty_cells_with_default_null_value,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_stereotypes_column_types import (
    EaTStereotypesColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from pandas import DataFrame


class ThinEaStereotypesFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_stereotypes = (
            self.__create_ea_stereotypes()
        )

        ea_stereotypes = self.__add_fields(
            ea_stereotypes=ea_stereotypes
        )

        return ea_stereotypes

    def __create_ea_stereotypes(
        self,
    ) -> DataFrame:
        extended_t_stereotypes_dataframe = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.EXTENDED_T_STEREOTYPES,
        )

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        extended_t_stereotypes_group_names_column_name = (
            "stereotype_group_names"
        )

        ea_stereotypes = dataframe_filter_and_rename(
            dataframe=extended_t_stereotypes_dataframe,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name,
                extended_t_stereotypes_group_names_column_name: extended_t_stereotypes_group_names_column_name,
                EaTStereotypesColumnTypes.T_STEREOTYPES_APPLIES_TOS.nf_column_name: NfEaComColumnTypes.STEREOTYPE_APPLIES_TOS.column_name,
                EaTStereotypesColumnTypes.T_STEREOTYPES_STYLES.nf_column_name: NfEaComColumnTypes.STEREOTYPE_STYLE.column_name,
            },
        )

        return ea_stereotypes

    def __add_fields(
        self, ea_stereotypes: DataFrame
    ) -> DataFrame:
        ea_stereotypes = self.__replace_stereotype_group_name_with_link(
            ea_stereotypes=ea_stereotypes
        )

        return ea_stereotypes

    def __replace_stereotype_group_name_with_link(
        self, ea_stereotypes: DataFrame
    ) -> DataFrame:
        ea_stereotype_groups = (
            self.nf_ea_com_universe.get_ea_stereotype_groups()
        )

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        object_name_column_name = (
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name
        )

        stereotype_ea_stereotype_group_column_name = (
            NfEaComColumnTypes.STEREOTYPE_EA_STEREOTYPE_GROUP.column_name
        )

        ea_stereotypes = left_merge_dataframes(
            master_dataframe=ea_stereotypes,
            master_dataframe_key_columns=[
                "stereotype_group_names"
            ],
            merge_suffixes=[
                "_stereotype",
                "_stereotype_group",
            ],
            foreign_key_dataframe=ea_stereotype_groups,
            foreign_key_dataframe_fk_columns=[
                object_name_column_name
            ],
            foreign_key_dataframe_other_column_rename_dictionary={
                nf_uuids_column_name: stereotype_ea_stereotype_group_column_name
            },
        )

        ea_stereotypes = dataframe_filter_and_rename(
            dataframe=ea_stereotypes,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name,
                stereotype_ea_stereotype_group_column_name: stereotype_ea_stereotype_group_column_name,
                NfEaComColumnTypes.STEREOTYPE_APPLIES_TOS.column_name: NfEaComColumnTypes.STEREOTYPE_APPLIES_TOS.column_name,
                NfEaComColumnTypes.STEREOTYPE_STYLE.column_name: NfEaComColumnTypes.STEREOTYPE_STYLE.column_name,
            },
        )

        ea_stereotypes = fill_up_all_empty_cells_with_default_null_value(
            dataframe=ea_stereotypes
        )

        return ea_stereotypes
