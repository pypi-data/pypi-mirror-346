from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.levels.ea_stereotypeable_objects_level_adder import (
    add_ea_stereotypeable_objects_level,
)
from pandas import DataFrame


class EaConnectorsFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_connectors = (
            self.__create_ea_connectors()
        )

        ea_connectors = self.__add_levels(
            ea_connectors=ea_connectors
        )

        return ea_connectors

    def __create_ea_connectors(
        self,
    ) -> DataFrame:
        ea_connectors = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_connectors()
        )

        return ea_connectors

    def __add_levels(
        self, ea_connectors: DataFrame
    ) -> DataFrame:
        ea_connectors = add_ea_stereotypeable_objects_level(
            dataframe=ea_connectors,
            nf_ea_com_universe=self.nf_ea_com_universe,
        )

        return ea_connectors
