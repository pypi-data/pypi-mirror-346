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
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.common.list_adder import (
    add_list,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_object_column_types import (
    EaTObjectColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_element_types import (
    EaElementTypes,
)
from pandas import DataFrame, concat


class ThinEaElementsFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_elements = (
            self.__create_ea_elements()
        )

        ea_elements = self.__add_fields(
            ea_elements=ea_elements
        )

        ea_elements = self.__add_lists(
            ea_elements=ea_elements
        )

        return ea_elements

    def __create_ea_elements(
        self,
    ) -> DataFrame:
        ea_packages = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_packages()
        )

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        ea_packages_nf_uuids = dataframe_filter_and_rename(
            dataframe=ea_packages,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name
            },
        )

        ea_classifiers = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_classifiers()
        )

        ea_classifiers_nf_uuids = dataframe_filter_and_rename(
            dataframe=ea_classifiers,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name
            },
        )

        ea_elements = concat(
            [
                ea_packages_nf_uuids,
                ea_classifiers_nf_uuids,
            ]
        )

        return ea_elements

    def __add_lists(
        self, ea_elements: DataFrame
    ) -> DataFrame:
        supplier_place1_end_connectors_column_name = (
            NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name
        )

        extended_t_connector_dataframe = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.EXTENDED_T_CONNECTOR,
        )

        ea_elements = add_list(
            master_dataframe=ea_elements,
            foreign_key_dataframe=extended_t_connector_dataframe,
            foreign_key_dataframe_fk_columns=[
                "start_t_object_nf_uuids"
            ],
            master_dataframe_new_column_name=supplier_place1_end_connectors_column_name,
        )

        client_place2_end_connectors_column_name = (
            NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name
        )

        ea_elements = add_list(
            master_dataframe=ea_elements,
            foreign_key_dataframe=extended_t_connector_dataframe,
            foreign_key_dataframe_fk_columns=[
                "end_t_object_nf_uuids"
            ],
            master_dataframe_new_column_name=client_place2_end_connectors_column_name,
        )

        contained_ea_diagrams_column_name = (
            NfEaComColumnTypes.ELEMENTS_CONTAINED_EA_DIAGRAMS.column_name
        )

        extended_t_diagram_dataframe = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.EXTENDED_T_DIAGRAM,
        )

        ea_elements = add_list(
            master_dataframe=ea_elements,
            foreign_key_dataframe=extended_t_diagram_dataframe,
            foreign_key_dataframe_fk_columns=[
                "t_diagram_package_nf_uuids"
            ],
            master_dataframe_new_column_name=contained_ea_diagrams_column_name,
        )

        contained_ea_classifiers_column_name = (
            NfEaComColumnTypes.ELEMENTS_CONTAINED_EA_CLASSIFIERS.column_name
        )

        extended_t_object_dataframe = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.EXTENDED_T_OBJECT,
        )

        ea_classifiers = extended_t_object_dataframe.loc[
            extended_t_object_dataframe[
                EaTObjectColumnTypes.T_OBJECT_TYPES.nf_column_name
            ]
            != EaElementTypes.PACKAGE.type_name
        ]

        ea_elements = add_list(
            master_dataframe=ea_elements,
            foreign_key_dataframe=ea_classifiers,
            foreign_key_dataframe_fk_columns=[
                "t_object_package_nf_uuids"
            ],
            master_dataframe_new_column_name=contained_ea_classifiers_column_name,
        )

        return ea_elements

    def __add_fields(
        self, ea_elements: DataFrame
    ) -> DataFrame:
        extended_t_object_dataframe = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.EXTENDED_T_OBJECT,
        )

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        ea_object_type_column_name = (
            NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE.column_name
        )

        ea_element_components = left_merge_dataframes(
            master_dataframe=ea_elements,
            master_dataframe_key_columns=[
                nf_uuids_column_name
            ],
            merge_suffixes=[
                "_element",
                "_object",
            ],
            foreign_key_dataframe=extended_t_object_dataframe,
            foreign_key_dataframe_fk_columns=[
                nf_uuids_column_name
            ],
            foreign_key_dataframe_other_column_rename_dictionary={
                EaTObjectColumnTypes.T_OBJECT_TYPES.nf_column_name: ea_object_type_column_name
            },
        )

        ea_element_components = ea_element_components.fillna(
            EaElementTypes.PACKAGE.type_name
        )

        return ea_element_components
