from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.nf_ea_sql_universes import (
    NfEaSqlUniverses,
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


class NfEaSqlUniverseManagers(
    NfManagers
):
    def __init__(
        self, ea_tools_session_manager
    ):
        NfManagers.__init__(self)

        self.ea_tools_session_manager = (
            ea_tools_session_manager
        )

        self.nf_ea_sql_universe_dictionary = (
            dict()
        )

    def get_extended_ea_t_table_dataframe(
        self,
        ea_repository: EaRepositories,
        ea_collection_type: EaCollectionTypes,
    ) -> DataFrame:
        nf_ea_sql_universe = self.__get_nf_ea_sql_universe(
            ea_repository=ea_repository
        )

        extended_ea_t_table_dataframe = nf_ea_sql_universe.get_extended_ea_t_table_dataframe(
            ea_collection_type=ea_collection_type
        )

        return extended_ea_t_table_dataframe

    def export_all_registries(
        self, output_folder_name: str
    ):
        for (
            ea_repository,
            nf_ea_sql_universe,
        ) in (
            self.nf_ea_sql_universe_dictionary.items()
        ):
            nf_ea_sql_universe.nf_ea_sql_registry.export_dataframes_to_new_database(
                short_name=ea_repository.short_name,
                output_folder_name=output_folder_name,
                database_basename="nf_ea_sql",
            )

    def create_or_update_summary_table(
        self,
        ea_repository: EaRepositories,
    ):
        nf_ea_sql_universe = self.__get_nf_ea_sql_universe(
            ea_repository=ea_repository
        )

        nf_ea_sql_universe.nf_ea_sql_registry.create_or_update_summary_table()

    def get_nf_ea_sql_universe(
        self,
        ea_repository: EaRepositories,
    ) -> NfEaSqlUniverses:
        nf_ea_sql_universe = self.__get_nf_ea_sql_universe(
            ea_repository=ea_repository
        )

        return nf_ea_sql_universe

    def __get_nf_ea_sql_universe(
        self,
        ea_repository: EaRepositories,
    ) -> NfEaSqlUniverses:
        if (
            ea_repository
            in self.nf_ea_sql_universe_dictionary
        ):
            return self.nf_ea_sql_universe_dictionary[
                ea_repository
            ]

        nf_ea_sql_universe = self.__create_nf_ea_sql_universe(
            ea_repository=ea_repository
        )

        self.nf_ea_sql_universe_dictionary[
            ea_repository
        ] = nf_ea_sql_universe

        return nf_ea_sql_universe

    def __create_nf_ea_sql_universe(
        self,
        ea_repository: EaRepositories,
    ) -> NfEaSqlUniverses:
        nf_ea_sql_universe = NfEaSqlUniverses(
            self.ea_tools_session_manager,
            ea_repository=ea_repository,
        )

        return nf_ea_sql_universe
