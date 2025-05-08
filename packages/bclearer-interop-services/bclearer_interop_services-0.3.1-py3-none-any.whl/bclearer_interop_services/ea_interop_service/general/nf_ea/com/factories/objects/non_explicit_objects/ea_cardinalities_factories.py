from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_cardinality_column_types import (
    EaTCardinalityColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from pandas import DataFrame


class EaCardinalitiesFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_cardinalities = (
            self.__create_ea_cardinalities()
        )

        return ea_cardinalities

    def __create_ea_cardinalities(
        self,
    ) -> DataFrame:
        extended_t_cardinality_dataframe = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.EXTENDED_T_CARDINALITY,
        )

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        t_cardinality_cardinality_nf_column_name = (
            EaTCardinalityColumnTypes.T_CARDINALITY_CARDINALITY.nf_column_name
        )

        ea_cardinalities = dataframe_filter_and_rename(
            dataframe=extended_t_cardinality_dataframe,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name,
                t_cardinality_cardinality_nf_column_name: "ea_cardinality",
            },
        )

        return ea_cardinalities
