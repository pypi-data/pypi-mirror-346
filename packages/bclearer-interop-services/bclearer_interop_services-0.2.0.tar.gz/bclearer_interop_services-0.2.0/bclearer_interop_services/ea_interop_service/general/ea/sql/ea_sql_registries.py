from bclearer_core.nf.python_extensions.collections.nf_registries import (
    NfRegistries,
)
from bclearer_interop_services.ea_interop_service.general.ea.sql.ea_sql_service.ea_sql_dataframe_creator import (
    create_ea_sql_dataframe,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.objects.ea_repositories import (
    EaRepositories,
)
from pandas import DataFrame


class EaSqlRegistries(NfRegistries):
    def __init__(
        self, owning_ea_sql_universe
    ):
        NfRegistries.__init__(self)

        self.owning_ea_sql_universe = (
            owning_ea_sql_universe
        )

    def get_ea_t_table_dataframe(
        self,
        ea_repository: EaRepositories,
        ea_t_table_type: EaCollectionTypes,
    ) -> DataFrame:
        ea_t_table_dataframe = self.__get_ea_sql_dataframe(
            ea_repository=ea_repository,
            ea_collection_type=ea_t_table_type,
        )

        return ea_t_table_dataframe

    def __get_ea_sql_dataframe(
        self,
        ea_repository: EaRepositories,
        ea_collection_type: EaCollectionTypes,
    ) -> DataFrame:
        if (
            ea_collection_type
            in self.dictionary_of_collections
        ):
            return self.dictionary_of_collections[
                ea_collection_type
            ]

        ea_t_table_dataframe = create_ea_sql_dataframe(
            ea_repository=ea_repository,
            ea_collection_type=ea_collection_type,
        )

        self.dictionary_of_collections[
            ea_collection_type
        ] = ea_t_table_dataframe

        return ea_t_table_dataframe
