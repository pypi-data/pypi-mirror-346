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
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.common.list_adder import (
    add_list,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_object_column_types import (
    EaTObjectColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_package_column_types import (
    EaTPackageColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_element_types import (
    EaElementTypes,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_new_uuid,
)
from pandas import DataFrame, isnull


class ThinEaPackagesFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_packages = (
            self.__create_ea_packages()
        )

        ea_packages = self.__add_lists(
            ea_packages=ea_packages
        )

        return ea_packages

    def __create_ea_packages(
        self,
    ) -> DataFrame:
        extended_t_object_dataframe = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.EXTENDED_T_OBJECT,
        )

        extended_t_package_dataframe = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.EXTENDED_T_PACKAGE,
        )

        package_ea_guid_column_name = (
            EaTPackageColumnTypes.T_PACKAGE_EA_GUIDS.nf_column_name
        )

        ea_packages = dataframe_filter_and_rename(
            dataframe=extended_t_package_dataframe,
            filter_and_rename_dictionary={
                package_ea_guid_column_name: package_ea_guid_column_name,
                "paths": "ea_package_path",
                "package_ea_guids_1": "parent_package_ea_guid",
                "package_names_1": "parent_package_name",
            },
        )

        ea_packages[
            NfEaComColumnTypes.PACKAGES_VIEW_TYPE.column_name
        ] = DEFAULT_NULL_VALUE

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        ea_packages = left_merge_dataframes(
            master_dataframe=ea_packages,
            master_dataframe_key_columns=[
                package_ea_guid_column_name
            ],
            merge_suffixes=[
                "_package",
                "_client",
            ],
            foreign_key_dataframe=extended_t_object_dataframe,
            foreign_key_dataframe_fk_columns=[
                EaTObjectColumnTypes.T_OBJECT_EA_GUIDS.nf_column_name
            ],
            foreign_key_dataframe_other_column_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name
            },
        )

        ea_packages[
            nf_uuids_column_name
        ] = ea_packages[
            nf_uuids_column_name
        ].apply(
            lambda nf_uuid: (
                create_new_uuid()
                if (isnull(nf_uuid))
                else nf_uuid
            )
        )

        return ea_packages

    def __add_lists(
        self, ea_packages: DataFrame
    ) -> DataFrame:
        contained_ea_packages_column_name = (
            NfEaComColumnTypes.PACKAGES_CONTAINED_EA_PACKAGES.column_name
        )

        extended_t_object_dataframe = self.nf_ea_com_universe.ea_tools_session_manager.nf_ea_sql_stage_manager.nf_ea_sql_universe_manager.get_extended_ea_t_table_dataframe(
            ea_repository=self.nf_ea_com_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.EXTENDED_T_OBJECT,
        )

        ea_package_objects = extended_t_object_dataframe.loc[
            extended_t_object_dataframe[
                EaTObjectColumnTypes.T_OBJECT_TYPES.nf_column_name
            ]
            == EaElementTypes.PACKAGE.type_name
        ]

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        ea_package_objects = dataframe_filter_and_rename(
            dataframe=ea_package_objects,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name,
                "t_object_package_ea_guids": "t_object_package_ea_guids",
            },
        )

        package_ea_guid_column_name = (
            EaTPackageColumnTypes.T_PACKAGE_EA_GUIDS.nf_column_name
        )

        ea_package_objects = left_merge_dataframes(
            master_dataframe=ea_package_objects,
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

        ea_packages = add_list(
            master_dataframe=ea_packages,
            foreign_key_dataframe=ea_package_objects,
            foreign_key_dataframe_fk_columns=[
                "t_object_package_nf_uuids"
            ],
            master_dataframe_new_column_name=contained_ea_packages_column_name,
        )

        return ea_packages
