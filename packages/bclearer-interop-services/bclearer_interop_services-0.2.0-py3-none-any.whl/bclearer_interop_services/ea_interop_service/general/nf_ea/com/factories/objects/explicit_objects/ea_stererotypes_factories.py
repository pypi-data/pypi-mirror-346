from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.levels.ea_repositoried_objects_level_adder import (
    add_ea_repositoried_objects_level,
)
from pandas import DataFrame


class EaStereotypesFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_stereotypes = (
            self.__create_ea_stereotypes()
        )

        ea_stereotypes = self.__add_levels(
            ea_stereotypes=ea_stereotypes
        )

        return ea_stereotypes

    def __create_ea_stereotypes(
        self,
    ) -> DataFrame:
        ea_stereotypes = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_stereotypes()
        )

        return ea_stereotypes

    def __add_levels(
        self, ea_stereotypes: DataFrame
    ) -> DataFrame:
        ea_stereotypes = add_ea_repositoried_objects_level(
            dataframe=ea_stereotypes,
            nf_ea_com_universe=self.nf_ea_com_universe,
        )

        return ea_stereotypes
