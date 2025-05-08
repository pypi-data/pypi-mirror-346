from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.levels.ea_element_components_level_adder import (
    add_ea_element_component_level,
)
from pandas import DataFrame


class EaAttributesFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_attributes = (
            self.__create_ea_attributes()
        )

        ea_attributes = self.__add_levels(
            ea_attributes=ea_attributes
        )

        return ea_attributes

    def __create_ea_attributes(
        self,
    ) -> DataFrame:
        ea_attributes = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_attributes()
        )

        return ea_attributes

    def __add_levels(
        self, ea_attributes: DataFrame
    ) -> DataFrame:
        ea_attributes = add_ea_element_component_level(
            dataframe=ea_attributes,
            nf_ea_com_universe=self.nf_ea_com_universe,
        )

        return ea_attributes
