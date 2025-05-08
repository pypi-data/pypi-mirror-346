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
from pandas import DataFrame, concat


class ThinEaRepositoriedObjectsFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_repositoried_objects = (
            self.__create_ea_repositoried_objects()
        )

        ea_repositoried_objects = self.__add_fields(
            ea_repositoried_objects=ea_repositoried_objects
        )

        return ea_repositoried_objects

    def __create_ea_repositoried_objects(
        self,
    ) -> DataFrame:
        ea_stereotypeable_objects = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_stereotypeable_objects()
        )

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        ea_stereotypeable_objects_nf_uuids = dataframe_filter_and_rename(
            dataframe=ea_stereotypeable_objects,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name
            },
        )

        ea_stereotypes = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_stereotypes()
        )

        ea_stereotypes_nf_uuids = dataframe_filter_and_rename(
            dataframe=ea_stereotypes,
            filter_and_rename_dictionary={
                nf_uuids_column_name: nf_uuids_column_name
            },
        )

        ea_repositoried_objects = concat(
            [
                ea_stereotypeable_objects_nf_uuids,
                ea_stereotypes_nf_uuids,
            ]
        )

        return ea_repositoried_objects

    @staticmethod
    def __add_fields(
        ea_repositoried_objects: DataFrame,
    ) -> DataFrame:
        ea_repository_column_name = (
            NfEaComColumnTypes.REPOSITORIED_OBJECTS_EA_REPOSITORY.column_name
        )

        ea_repositoried_objects[
            ea_repository_column_name
        ] = DEFAULT_NULL_VALUE

        return ea_repositoried_objects
