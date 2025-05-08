from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.levels.ea_elements_level_adder import (
    add_ea_element_level,
)
from pandas import DataFrame


class EaClassifiersFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_classifiers = (
            self.__create_ea_classifiers()
        )

        ea_classifiers = self.__add_levels(
            ea_classifiers=ea_classifiers
        )

        return ea_classifiers

    def __create_ea_classifiers(
        self,
    ) -> DataFrame:
        ea_classifiers = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_classifiers()
        )

        return ea_classifiers

    def __add_levels(
        self, ea_classifiers: DataFrame
    ) -> DataFrame:
        ea_classifiers = add_ea_element_level(
            dataframe=ea_classifiers,
            nf_ea_com_universe=self.nf_ea_com_universe,
        )

        return ea_classifiers
