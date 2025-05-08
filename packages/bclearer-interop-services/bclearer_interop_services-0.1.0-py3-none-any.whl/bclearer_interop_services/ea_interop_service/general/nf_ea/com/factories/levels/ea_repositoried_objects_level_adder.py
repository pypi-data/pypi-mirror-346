from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.common.level_adder import (
    add_level,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.levels.ea_explicit_objects_level_adder import (
    add_ea_explicit_objects_level,
)
from pandas import DataFrame


def add_ea_repositoried_objects_level(
    nf_ea_com_universe,
    dataframe: DataFrame,
) -> DataFrame:
    thin_ea_repositoried_objects = (
        nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_repositoried_objects()
    )

    dataframe = add_level(
        dataframe=dataframe,
        next_level_dataframe=thin_ea_repositoried_objects,
    )

    dataframe = (
        add_ea_explicit_objects_level(
            nf_ea_com_universe,
            dataframe=dataframe,
        )
    )

    return dataframe
