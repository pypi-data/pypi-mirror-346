from bclearer_interop_services.ea_interop_service.general.ea.sql.ea_sql_registries import (
    EaSqlRegistries,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.objects.ea_repositories import (
    EaRepositories,
)
from pandas import DataFrame


class EaSqlUniverses:
    def __init__(
        self,
        ea_repository: EaRepositories,
    ):
        self.ea_sql_registry = (
            EaSqlRegistries(self)
        )

        self.ea_repository = (
            ea_repository
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
        self,
        project_short_name: str,
        output_folder_name: str,
    ):
        self.ea_sql_registry.export_dataframes(
            short_name=project_short_name,
            output_folder_name=output_folder_name,
        )

    def get_ea_t_table_dataframe(
        self,
        ea_collection_type: EaCollectionTypes,
    ) -> DataFrame:
        ea_t_table_dataframe = self.ea_sql_registry.get_ea_t_table_dataframe(
            self.ea_repository,
            ea_t_table_type=ea_collection_type,
        )

        return ea_t_table_dataframe
