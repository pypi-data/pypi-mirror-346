from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
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
from pandas import DataFrame


class ThinEaClassifiersFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_classifiers = (
            self.__create_ea_classifiers()
        )

        ea_classifiers = self.__add_lists(
            ea_classifiers=ea_classifiers
        )

        return ea_classifiers

    def __create_ea_classifiers(
        self,
    ) -> DataFrame:
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

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        classifier_column_name = (
            NfEaComColumnTypes.ELEMENTS_CLASSIFIER.column_name
        )

        containing_ea_element_column_name = (
            NfEaComColumnTypes.CLASSIFIERS_CONTAINING_EA_ELEMENT.column_name
        )

        ea_classifiers = dataframe_filter_and_rename(
            dataframe=ea_classifiers,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name,
                "t_object_classifier_nf_uuids": classifier_column_name,
                "t_object_parent_nf_uuids": containing_ea_element_column_name,
            },
        )

        return ea_classifiers

    def __add_lists(
        self, ea_classifiers: DataFrame
    ) -> DataFrame:
        all_component_ea_attributes_column_name = (
            NfEaComColumnTypes.CLASSIFIERS_ALL_COMPONENT_EA_ATTRIBUTES.column_name
        )

        extended_t_attribute_dataframe = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.EXTENDED_T_ATTRIBUTE,
        )

        ea_classifiers = add_list(
            master_dataframe=ea_classifiers,
            foreign_key_dataframe=extended_t_attribute_dataframe,
            foreign_key_dataframe_fk_columns=[
                "attributed_t_object_nf_uuids"
            ],
            master_dataframe_new_column_name=all_component_ea_attributes_column_name,
        )

        all_component_ea_operations_column_name = (
            NfEaComColumnTypes.CLASSIFIERS_ALL_COMPONENT_EA_OPERATIONS.column_name
        )

        ea_classifiers[
            all_component_ea_operations_column_name
        ] = DEFAULT_NULL_VALUE

        return ea_classifiers
