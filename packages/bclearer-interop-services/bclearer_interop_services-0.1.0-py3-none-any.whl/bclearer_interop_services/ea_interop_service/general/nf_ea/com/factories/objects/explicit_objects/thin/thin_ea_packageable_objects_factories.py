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
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_package_column_types import (
    EaTPackageColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from pandas import DataFrame, concat


class ThinEaPackageableObjectsFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_packageable_objects = (
            self.__create_ea_packageable_objects()
        )

        ea_packageable_objects = self.__add_fields(
            ea_packageable_objects=ea_packageable_objects
        )

        return ea_packageable_objects

    def __create_ea_packageable_objects(
        self,
    ) -> DataFrame:
        ea_elements = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_elements()
        )

        ea_diagrams = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_diagrams()
        )

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        ea_elements_nf_uuids = dataframe_filter_and_rename(
            dataframe=ea_elements,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name
            },
        )

        ea_diagrams_nf_uuids = dataframe_filter_and_rename(
            dataframe=ea_diagrams,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name
            },
        )

        ea_packageable_objects = concat(
            [
                ea_elements_nf_uuids,
                ea_diagrams_nf_uuids,
            ]
        )

        return ea_packageable_objects

    def __add_fields(
        self,
        ea_packageable_objects: DataFrame,
    ) -> DataFrame:
        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        parent_ea_element_column_name = (
            NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT.column_name
        )

        parent_ea_element_dataframe = (
            self.__get_parent_ea_element_dataframe()
        )

        ea_packageable_objects = left_merge_dataframes(
            master_dataframe=ea_packageable_objects,
            master_dataframe_key_columns=[
                nf_uuids_column_name
            ],
            merge_suffixes=[
                "_master",
                "_fields",
            ],
            foreign_key_dataframe=parent_ea_element_dataframe,
            foreign_key_dataframe_fk_columns=[
                nf_uuids_column_name
            ],
            foreign_key_dataframe_other_column_rename_dictionary={
                parent_ea_element_column_name: parent_ea_element_column_name
            },
        )

        ea_packageable_objects = ea_packageable_objects.fillna(
            DEFAULT_NULL_VALUE
        )

        return ea_packageable_objects

    def __get_parent_ea_element_dataframe(
        self,
    ) -> DataFrame:
        object_parent_ea_element_dataframe = (
            self.__get_object_parent_ea_element_dataframe()
        )

        diagram_parent_ea_element_dataframe = (
            self.__get_diagram_parent_ea_element_dataframe()
        )

        parent_ea_element_dataframe = concat(
            [
                object_parent_ea_element_dataframe,
                diagram_parent_ea_element_dataframe,
            ]
        )

        return (
            parent_ea_element_dataframe
        )

    def __get_object_parent_ea_element_dataframe(
        self,
    ):
        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        parent_ea_element_column_name = (
            NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT.column_name
        )

        extended_t_object_dataframe = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.EXTENDED_T_OBJECT,
        )

        extended_t_object_dataframe = dataframe_filter_and_rename(
            dataframe=extended_t_object_dataframe,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name,
                "t_object_package_ea_guids": "t_object_package_ea_guids",
            },
        )

        ea_packages = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_packages()
        )

        package_ea_guid_column_name = (
            EaTPackageColumnTypes.T_PACKAGE_EA_GUIDS.nf_column_name
        )

        extended_t_object_dataframe = left_merge_dataframes(
            master_dataframe=extended_t_object_dataframe,
            master_dataframe_key_columns=[
                "t_object_package_ea_guids"
            ],
            merge_suffixes=[
                "_object",
                "_package",
            ],
            foreign_key_dataframe=ea_packages,
            foreign_key_dataframe_fk_columns=[
                package_ea_guid_column_name
            ],
            foreign_key_dataframe_other_column_rename_dictionary={
                NfColumnTypes.NF_UUIDS.column_name: "t_object_package_nf_uuids"
            },
        )

        object_parent_ea_element_dataframe = dataframe_filter_and_rename(
            dataframe=extended_t_object_dataframe,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name,
                "t_object_package_nf_uuids": parent_ea_element_column_name,
            },
        )

        return object_parent_ea_element_dataframe

    def __get_diagram_parent_ea_element_dataframe(
        self,
    ):
        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        parent_ea_element_column_name = (
            NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT.column_name
        )

        extended_t_diagram_dataframe = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.EXTENDED_T_DIAGRAM,
        )

        diagram_parent_ea_element_dataframe = dataframe_filter_and_rename(
            dataframe=extended_t_diagram_dataframe,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name,
                "t_diagram_package_nf_uuids": parent_ea_element_column_name,
            },
        )

        return diagram_parent_ea_element_dataframe
