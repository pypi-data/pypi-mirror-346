from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.nf_ea_sql_registries import (
    NfEaSqlRegistries,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.objects.ea_repositories import (
    EaRepositories,
)
from pandas import DataFrame


class NfEaSqlUniverses:
    def __init__(
        self,
        ea_tools_session_manager,
        ea_repository: EaRepositories,
    ):
        self.ea_tools_session_manager = (
            ea_tools_session_manager
        )

        self.ea_repository = (
            ea_repository
        )

        self.nf_ea_sql_registry = (
            NfEaSqlRegistries(self)
        )

    def __enter__(self):
        return self

    def __exit__(
        self,
        exception_type,
        exception_value,
        traceback,
    ):
        pass

    def export_dataframes(
        self, output_folder_name: str
    ):
        project_short_name = (
            self.ea_repository.short_name
        )

        self.nf_ea_sql_registry.export_dataframes(
            short_name=project_short_name,
            output_folder_name=output_folder_name,
        )

    def get_extended_ea_t_table_dataframe(
        self,
        ea_collection_type: EaCollectionTypes,
    ) -> DataFrame:
        extended_ea_t_table_dataframe = self.nf_ea_sql_registry.get_extended_ea_t_table_dataframe(
            ea_collection_type=ea_collection_type
        )

        return extended_ea_t_table_dataframe

    def add_ea_guids_to_ea_identifiers_for_objects(
        self,
    ):
        self.nf_ea_sql_registry.add_ea_guids_to_ea_identifiers_for_objects()

    def add_ea_guids_to_ea_identifiers_for_packages(
        self,
    ):
        self.nf_ea_sql_registry.add_ea_guids_to_ea_identifiers_for_packages()

    def get_last_ea_identifier_for_objects(
        self,
    ) -> int:
        last_ea_identifier_for_objects = (
            self.nf_ea_sql_registry.get_last_ea_identifier_for_objects()
        )

        return last_ea_identifier_for_objects

    def get_last_ea_identifier_for_packages(
        self,
    ) -> int:
        last_ea_identifier_for_packages = (
            self.nf_ea_sql_registry.get_last_ea_identifier_for_packages()
        )

        return last_ea_identifier_for_packages

    def get_last_ea_identifier_for_attributes(
        self,
    ) -> int:
        last_ea_identifier_for_attributes = (
            self.nf_ea_sql_registry.get_last_ea_identifier_for_attributes()
        )

        return last_ea_identifier_for_attributes
