from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.levels.ea_element_components_level_adder import (
    add_ea_element_component_level,
)
from pandas import DataFrame


class EaOperationsFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_operations = (
            self.__create_ea_operations()
        )

        ea_operations = self.__add_levels(
            ea_operations=ea_operations
        )

        return ea_operations

    def __create_ea_operations(
        self,
    ) -> DataFrame:
        ea_operations = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_operations()
        )

        return ea_operations

    def __add_levels(
        self, ea_operations: DataFrame
    ) -> DataFrame:
        ea_operations = add_ea_element_component_level(
            dataframe=ea_operations,
            nf_ea_com_universe=self.nf_ea_com_universe,
        )

        return ea_operations
