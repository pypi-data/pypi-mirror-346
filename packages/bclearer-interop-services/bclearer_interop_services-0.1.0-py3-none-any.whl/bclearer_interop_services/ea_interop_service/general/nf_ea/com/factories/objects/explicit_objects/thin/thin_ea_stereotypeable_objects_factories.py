from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.common.list_adder import (
    add_list,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from pandas import DataFrame, concat


class ThinEaStereotypeableObjectsFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_stereotypeable_objects = (
            self.__create_ea_stereotypeable_objects()
        )

        ea_stereotypeable_objects = self.__add_lists(
            ea_stereotypeable_objects=ea_stereotypeable_objects
        )

        return ea_stereotypeable_objects

    def __create_ea_stereotypeable_objects(
        self,
    ) -> DataFrame:
        ea_packageable_objects = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_packageable_objects()
        )

        ea_connectors = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_connectors()
        )

        ea_element_components = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_element_components()
        )

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        ea_packageable_objects_nf_uuids = dataframe_filter_and_rename(
            dataframe=ea_packageable_objects,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name
            },
        )

        ea_connectors_nf_uuids = dataframe_filter_and_rename(
            dataframe=ea_connectors,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name
            },
        )

        ea_element_components = dataframe_filter_and_rename(
            dataframe=ea_element_components,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name
            },
        )

        ea_stereotypeable_objects = concat(
            [
                ea_packageable_objects_nf_uuids,
                ea_connectors_nf_uuids,
                ea_element_components,
            ]
        )

        return ea_stereotypeable_objects

    def __add_lists(
        self,
        ea_stereotypeable_objects: DataFrame,
    ) -> DataFrame:
        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        ea_object_stereotypes_column_name = (
            NfEaComColumnTypes.STEREOTYPEABLE_OBJECTS_EA_OBJECT_STEREOTYPES.column_name
        )

        stereotype_usage_dataframe = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.OBJECT_STEREOTYPES,
        )

        self.nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections[
            NfEaComCollectionTypes.STEREOTYPE_USAGE
        ] = stereotype_usage_dataframe

        stereotype_usage_dataframe = stereotype_usage_dataframe.rename(
            columns={
                "stereotype_nf_uuids": nf_uuids_column_name
            }
        )

        ea_stereotypeable_objects = add_list(
            master_dataframe=ea_stereotypeable_objects,
            foreign_key_dataframe=stereotype_usage_dataframe,
            foreign_key_dataframe_fk_columns=[
                NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS.column_name
            ],
            master_dataframe_new_column_name=ea_object_stereotypes_column_name,
        )

        return ea_stereotypeable_objects
