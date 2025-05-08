from bclearer_interop_services.ea_interop_service.general.ea.sql.ea_sql_universes import (
    EaSqlUniverses,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.objects.ea_repositories import (
    EaRepositories,
)
from bclearer_interop_services.ea_interop_service.session.nf_ea_com_endpoint.orchestrators.nf_managers import (
    NfManagers,
)
from pandas import DataFrame


class EaSqlUniverseManagers(NfManagers):
    def __init__(self):
        NfManagers.__init__(self)

        self.ea_sql_universe_dictionary = (
            dict()
        )

    def get_ea_t_table_dataframe(
        self,
        ea_repository: EaRepositories,
        ea_collection_type: EaCollectionTypes,
    ) -> DataFrame:
        ea_sql_universe = self.__get_ea_sql_universe(
            ea_repository=ea_repository
        )

        ea_t_table_dataframe = ea_sql_universe.get_ea_t_table_dataframe(
            ea_collection_type=ea_collection_type
        )

        return ea_t_table_dataframe

    def export_all_registries(
        self, output_folder_name: str
    ):
        for (
            ea_repository,
            ea_sql_universe,
        ) in (
            self.ea_sql_universe_dictionary.items()
        ):
            ea_sql_universe.ea_sql_registry.export_dataframes_to_new_database(
                short_name=ea_repository.short_name,
                output_folder_name=output_folder_name,
                database_basename="ea_sql",
            )

    def create_or_update_summary_table(
        self,
        ea_repository: EaRepositories,
    ):
        ea_sql_universe = self.__get_ea_sql_universe(
            ea_repository=ea_repository
        )

        ea_sql_universe.ea_sql_registry.create_or_update_summary_table()

    def __get_ea_sql_universe(
        self,
        ea_repository: EaRepositories,
    ) -> EaSqlUniverses:
        if (
            ea_repository
            in self.ea_sql_universe_dictionary
        ):
            return self.ea_sql_universe_dictionary[
                ea_repository
            ]

        ea_sql_universe = self.__create_ea_sql_universe(
            ea_repository=ea_repository
        )

        self.ea_sql_universe_dictionary[
            ea_repository
        ] = ea_sql_universe

        return ea_sql_universe

    @staticmethod
    def __create_ea_sql_universe(
        ea_repository: EaRepositories,
    ) -> EaSqlUniverses:
        ea_sql_universe = EaSqlUniverses(
            ea_repository=ea_repository
        )

        return ea_sql_universe
