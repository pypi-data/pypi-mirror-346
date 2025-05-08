from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_connector_types_column_types import (
    EaTConnectorTypesColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from pandas import DataFrame


class EaConnectorTypesFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_connector_types = (
            self.__create_ea_connector_types()
        )

        return ea_connector_types

    def __create_ea_connector_types(
        self,
    ) -> DataFrame:
        extended_t_connector_types = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.EXTENDED_T_CONNECTORTYPES,
        )

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        connectortypes_connector_types_nf_column_name = (
            EaTConnectorTypesColumnTypes.T_CONNECTOR_TYPES_CONNECTOR_TYPES.nf_column_name
        )

        ea_object_name_nf_ea_com_column_name = (
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name
        )

        ea_connector_types = dataframe_filter_and_rename(
            dataframe=extended_t_connector_types,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name,
                connectortypes_connector_types_nf_column_name: ea_object_name_nf_ea_com_column_name,
            },
        )

        return ea_connector_types
