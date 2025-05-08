from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.levels.ea_elements_level_adder import (
    add_ea_element_level,
)
from pandas import DataFrame


class EaPackagesFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_packages = (
            self.__create_ea_packages()
        )

        ea_packages = self.__add_levels(
            ea_packages=ea_packages
        )

        return ea_packages

    def __create_ea_packages(
        self,
    ) -> DataFrame:
        ea_packages = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_packages()
        )

        return ea_packages

    def __add_levels(
        self, ea_packages: DataFrame
    ) -> DataFrame:
        ea_packages = add_ea_element_level(
            dataframe=ea_packages,
            nf_ea_com_universe=self.nf_ea_com_universe,
        )

        return ea_packages
