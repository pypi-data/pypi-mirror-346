from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_attribute_column_types import (
    EaTAttributeColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from pandas import DataFrame


class ThinEaAttributesFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_attributes = (
            self.__create_ea_attributes()
        )

        return ea_attributes

    def __create_ea_attributes(
        self,
    ) -> DataFrame:
        extended_t_attribute_dataframe = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.EXTENDED_T_ATTRIBUTE,
        )

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        t_attribute_lower_bounds_column_name = (
            EaTAttributeColumnTypes.T_ATTRIBUTE_LOWER_BOUNDS.nf_column_name
        )

        t_attribute_upper_bounds_column_name = (
            EaTAttributeColumnTypes.T_ATTRIBUTE_UPPER_BOUNDS.nf_column_name
        )

        lower_bounds_column_name = (
            NfEaComColumnTypes.ATTRIBUTES_LOWER_BOUNDS.column_name
        )

        upper_bounds_column_name = (
            NfEaComColumnTypes.ATTRIBUTES_UPPER_BOUNDS.column_name
        )

        ea_attributes = dataframe_filter_and_rename(
            dataframe=extended_t_attribute_dataframe,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name,
                t_attribute_lower_bounds_column_name: lower_bounds_column_name,
                t_attribute_upper_bounds_column_name: upper_bounds_column_name,
            },
        )

        return ea_attributes
