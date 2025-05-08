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
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.explicit_objects.thin.ea_model_factory.ea_model_factory import (
    get_ea_models,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_attribute_column_types import (
    EaTAttributeColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_connector_column_types import (
    EaTConnectorColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_diagram_column_types import (
    EaTDiagramColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_object_column_types import (
    EaTObjectColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_operation_column_types import (
    EaTOperationColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_package_column_types import (
    EaTPackageColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_stereotypes_column_types import (
    EaTStereotypesColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from pandas import DataFrame, concat


class ThinEaExplicitObjectsFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_explicit_objects = (
            self.__create_ea_explicit_objects()
        )

        ea_explicit_objects = self.__add_fields(
            ea_explicit_objects=ea_explicit_objects
        )

        return ea_explicit_objects

    def __create_ea_explicit_objects(
        self,
    ) -> DataFrame:
        ea_repositoried_objects = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_repositoried_objects()
        )

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        ea_repositoried_objects_nf_uuids = dataframe_filter_and_rename(
            dataframe=ea_repositoried_objects,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name
            },
        )

        ea_explicit_objects = concat(
            [
                ea_repositoried_objects_nf_uuids
            ]
        )

        return ea_explicit_objects

    def __add_fields(
        self,
        ea_explicit_objects: DataFrame,
    ) -> DataFrame:
        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        object_name_column_name = (
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name
        )

        object_notes_column_name = (
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NOTES.column_name
        )

        object_guid_column_name = (
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
        )

        names_and_notes_dataframe = (
            self.__get_names_and_notes_dataframe()
        )

        ea_explicit_objects = left_merge_dataframes(
            master_dataframe=ea_explicit_objects,
            master_dataframe_key_columns=[
                nf_uuids_column_name
            ],
            merge_suffixes=[
                "_master",
                "_fields",
            ],
            foreign_key_dataframe=names_and_notes_dataframe,
            foreign_key_dataframe_fk_columns=[
                nf_uuids_column_name
            ],
            foreign_key_dataframe_other_column_rename_dictionary={
                object_name_column_name: object_name_column_name,
                object_notes_column_name: object_notes_column_name,
                object_guid_column_name: object_guid_column_name,
            },
        )

        return ea_explicit_objects

    def __get_names_and_notes_dataframe(
        self,
    ) -> DataFrame:
        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        object_name_column_name = (
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name
        )

        object_notes_column_name = (
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NOTES.column_name
        )

        object_guid_column_name = (
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
        )

        extended_t_object_dataframe = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.EXTENDED_T_OBJECT,
        )

        object_names_and_notes_dataframe = dataframe_filter_and_rename(
            dataframe=extended_t_object_dataframe,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name,
                EaTObjectColumnTypes.T_OBJECT_NAMES.nf_column_name: object_name_column_name,
                EaTObjectColumnTypes.T_OBJECT_NOTES.nf_column_name: object_notes_column_name,
                EaTObjectColumnTypes.T_OBJECT_EA_GUIDS.nf_column_name: object_guid_column_name,
            },
        )

        ea_models = get_ea_models(
            nf_ea_com_universe=self.nf_ea_com_universe
        )

        model_names_and_notes_dataframe = dataframe_filter_and_rename(
            dataframe=ea_models,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name,
                "ea_model_names": object_name_column_name,
                "ea_model_notes": object_notes_column_name,
                EaTPackageColumnTypes.T_PACKAGE_EA_GUIDS.nf_column_name: object_guid_column_name,
            },
        )

        extended_t_diagram_dataframe = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.EXTENDED_T_DIAGRAM,
        )

        diagram_names_and_notes_dataframe = dataframe_filter_and_rename(
            dataframe=extended_t_diagram_dataframe,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name,
                EaTDiagramColumnTypes.T_DIAGRAM_NAMES.nf_column_name: object_name_column_name,
                EaTDiagramColumnTypes.T_DIAGRAM_NOTES.nf_column_name: object_notes_column_name,
                EaTDiagramColumnTypes.T_DIAGRAM_EA_GUIDS.nf_column_name: object_guid_column_name,
            },
        )

        extended_t_connectors_dataframe = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.EXTENDED_T_CONNECTOR,
        )

        connectors_names_and_notes_dataframe = dataframe_filter_and_rename(
            dataframe=extended_t_connectors_dataframe,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name,
                EaTConnectorColumnTypes.T_CONNECTOR_NAMES.nf_column_name: object_name_column_name,
                EaTConnectorColumnTypes.T_CONNECTOR_NOTES.nf_column_name: object_notes_column_name,
                EaTConnectorColumnTypes.T_CONNECTOR_EA_GUIDS.nf_column_name: object_guid_column_name,
            },
        )

        extended_t_stereotypes_dataframe = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.EXTENDED_T_STEREOTYPES,
        )

        stereotypes_names_and_notes_dataframe = dataframe_filter_and_rename(
            dataframe=extended_t_stereotypes_dataframe,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name,
                EaTStereotypesColumnTypes.T_STEREOTYPES_NAMES.nf_column_name: object_name_column_name,
                EaTStereotypesColumnTypes.T_STEREOTYPES_DESCRIPTIONS.nf_column_name: object_notes_column_name,
                EaTStereotypesColumnTypes.T_STEREOTYPES_EA_GUIDS.nf_column_name: object_guid_column_name,
            },
        )

        extended_t_attribute_dataframe = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.EXTENDED_T_ATTRIBUTE,
        )

        t_attribute_names_nf_column_name = (
            EaTAttributeColumnTypes.T_ATTRIBUTE_NAMES.nf_column_name
        )

        t_attribute_notes_nf_column_name = (
            EaTAttributeColumnTypes.T_ATTRIBUTE_NOTES.nf_column_name
        )

        t_attribute_ea_guids_nf_column_name = (
            EaTAttributeColumnTypes.T_ATTRIBUTE_EA_GUIDS.nf_column_name
        )

        attribute_names_and_notes_dataframe = dataframe_filter_and_rename(
            dataframe=extended_t_attribute_dataframe,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name,
                t_attribute_names_nf_column_name: object_name_column_name,
                t_attribute_notes_nf_column_name: object_notes_column_name,
                t_attribute_ea_guids_nf_column_name: object_guid_column_name,
            },
        )

        extended_t_operation_dataframe = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.EXTENDED_T_OPERATION,
        )

        t_operation_names_nf_column_name = (
            EaTOperationColumnTypes.T_OPERATION_NAMES.nf_column_name
        )

        t_operation_notes_nf_column_name = (
            EaTOperationColumnTypes.T_OPERATION_NOTES.nf_column_name
        )

        t_operation_ea_guids_nf_column_name = (
            EaTOperationColumnTypes.T_OPERATION_EA_GUIDS.nf_column_name
        )

        operation_names_and_notes_dataframe = dataframe_filter_and_rename(
            dataframe=extended_t_operation_dataframe,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name,
                t_operation_names_nf_column_name: object_name_column_name,
                t_operation_notes_nf_column_name: object_notes_column_name,
                t_operation_ea_guids_nf_column_name: object_guid_column_name,
            },
        )

        names_and_notes_dataframe = concat(
            [
                object_names_and_notes_dataframe,
                model_names_and_notes_dataframe,
                diagram_names_and_notes_dataframe,
                connectors_names_and_notes_dataframe,
                stereotypes_names_and_notes_dataframe,
                attribute_names_and_notes_dataframe,
                operation_names_and_notes_dataframe,
            ]
        )

        return names_and_notes_dataframe
