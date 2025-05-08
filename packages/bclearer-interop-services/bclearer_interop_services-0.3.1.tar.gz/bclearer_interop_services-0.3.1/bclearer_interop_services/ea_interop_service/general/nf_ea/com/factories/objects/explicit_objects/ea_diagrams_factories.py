from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.levels.ea_packageable_objects_level_adder import (
    add_ea_packageable_objects_level,
)
from pandas import DataFrame


class EaDiagramsFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_diagrams = (
            self.__create_ea_diagrams()
        )

        ea_diagrams = self.__add_levels(
            ea_diagrams=ea_diagrams
        )

        return ea_diagrams

    def __create_ea_diagrams(
        self,
    ) -> DataFrame:
        ea_diagrams = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_diagrams()
        )

        return ea_diagrams

    def __add_levels(
        self, ea_diagrams: DataFrame
    ) -> DataFrame:
        ea_diagrams = add_ea_packageable_objects_level(
            dataframe=ea_diagrams,
            nf_ea_com_universe=self.nf_ea_com_universe,
        )

        return ea_diagrams
