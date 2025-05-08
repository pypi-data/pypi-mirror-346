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
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from pandas import DataFrame


class EaObjectStereotypesFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_object_stereotypes = (
            self.__create_ea_object_stereotypes()
        )

        ea_object_stereotypes = self.__add_fields(
            ea_object_stereotypes=ea_object_stereotypes
        )

        return ea_object_stereotypes

    def __create_ea_object_stereotypes(
        self,
    ) -> DataFrame:
        object_stereotypes_dataframe = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.OBJECT_STEREOTYPES,
        )

        ea_object_stereotypes = dataframe_filter_and_rename(
            dataframe=object_stereotypes_dataframe,
            filter_and_rename_dictionary={
                NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS.column_name: "ea_client",
                NfEaComColumnTypes.STEREOTYPE_PROPERTY_TYPE.column_name: NfEaComColumnTypes.STEREOTYPE_PROPERTY_TYPE.column_name,
                "stereotype_nf_uuids": "ea_stereotype",
            },
        )

        return ea_object_stereotypes

    def __add_fields(
        self,
        ea_object_stereotypes: DataFrame,
    ) -> DataFrame:
        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        thin_ea_stereotypes = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_stereotypes()
        )

        ea_object_stereotypes = left_merge_dataframes(
            master_dataframe=ea_object_stereotypes,
            master_dataframe_key_columns=[
                "ea_stereotype"
            ],
            merge_suffixes=[
                "_master",
                "_fields",
            ],
            foreign_key_dataframe=thin_ea_stereotypes,
            foreign_key_dataframe_fk_columns=[
                nf_uuids_column_name
            ],
            foreign_key_dataframe_other_column_rename_dictionary={
                NfEaComColumnTypes.STEREOTYPE_EA_STEREOTYPE_GROUP.column_name: NfEaComColumnTypes.STEREOTYPE_EA_STEREOTYPE_GROUP.column_name
            },
        )

        return ea_object_stereotypes
