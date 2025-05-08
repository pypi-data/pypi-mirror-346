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
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_attribute_column_types import (
    EaTAttributeColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from pandas import DataFrame, concat


class ThinEaElementComponentsFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_element_components = (
            self.__create_ea_element_components()
        )

        ea_element_components = self.__add_fields(
            ea_element_components=ea_element_components
        )

        return ea_element_components

    def __create_ea_element_components(
        self,
    ) -> DataFrame:
        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        thin_ea_attributes_dataframe = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_attributes()
        )

        thin_ea_attributes_dataframe = dataframe_filter_and_rename(
            dataframe=thin_ea_attributes_dataframe,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name
            },
        )

        thin_ea_operations_dataframe = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_operations()
        )

        thin_ea_operations_dataframe = dataframe_filter_and_rename(
            dataframe=thin_ea_operations_dataframe,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name
            },
        )

        ea_element_components = concat(
            [
                thin_ea_attributes_dataframe,
                thin_ea_operations_dataframe,
            ]
        )

        return ea_element_components

    def __add_fields(
        self,
        ea_element_components: DataFrame,
    ) -> DataFrame:
        extended_t_attribute_dataframe = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.EXTENDED_T_ATTRIBUTE,
        )

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        attributed_t_object_nf_uuids_column_name = "attributed_t_object_nf_uuids"

        t_attribute_classifiers_t_object_nf_uuids_column_name = "t_attribute_classifiers_t_object_nf_uuids"

        t_attribute_scopes_column_name = (
            EaTAttributeColumnTypes.T_ATTRIBUTE_SCOPES.nf_column_name
        )

        t_attribute_defaults_column_name = (
            EaTAttributeColumnTypes.T_ATTRIBUTE_DEFAULTS.nf_column_name
        )

        t_attribute_types_column_name = (
            EaTAttributeColumnTypes.T_ATTRIBUTE_TYPES.nf_column_name
        )

        containing_ea_classifier_column_name = (
            NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name
        )

        classifying_ea_classifier_column_name = (
            NfEaComColumnTypes.ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER.column_name
        )

        uml_visibility_kind_column_name = (
            NfEaComColumnTypes.ELEMENT_COMPONENTS_UML_VISIBILITY_KIND.column_name
        )

        type_column_name = (
            NfEaComColumnTypes.ELEMENT_COMPONENTS_TYPE.column_name
        )

        default_column_name = (
            NfEaComColumnTypes.ELEMENT_COMPONENTS_DEFAULT.column_name
        )

        ea_element_components = left_merge_dataframes(
            master_dataframe=ea_element_components,
            master_dataframe_key_columns=[
                nf_uuids_column_name
            ],
            merge_suffixes=[
                "_master",
                "_fields",
            ],
            foreign_key_dataframe=extended_t_attribute_dataframe,
            foreign_key_dataframe_fk_columns=[
                nf_uuids_column_name
            ],
            foreign_key_dataframe_other_column_rename_dictionary={
                attributed_t_object_nf_uuids_column_name: containing_ea_classifier_column_name,
                t_attribute_classifiers_t_object_nf_uuids_column_name: classifying_ea_classifier_column_name,
                t_attribute_scopes_column_name: uml_visibility_kind_column_name,
                t_attribute_types_column_name: type_column_name,
                t_attribute_defaults_column_name: default_column_name,
            },
        )

        ea_element_components = fill_up_all_empty_cells_with_default_null_value(
            dataframe=ea_element_components
        )

        return ea_element_components
