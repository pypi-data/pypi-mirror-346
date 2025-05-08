from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.connectors.i_dual_connector import (
    IDualConnector,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.objects.ea_repositories import (
    EaRepositories,
)
from bclearer_interop_services.ea_interop_service.session.ea_repository_mappers import (
    EaRepositoryMappers,
)
from bclearer_interop_services.tuple_service.tuple_attribute_value_getter import (
    get_tuple_attribute_value_if_required,
)
from pandas import DataFrame


def highlight_nf_ea_connectors(
    ea_repository: EaRepositories,
    input_dataframe: DataFrame,
):
    input_dataframe = (
        input_dataframe.fillna(
            DEFAULT_NULL_VALUE
        )
    )

    for (
        input_tuple
    ) in input_dataframe.itertuples():
        __highlight_nf_ea_connector_using_input_tuple(
            ea_repository=ea_repository,
            input_tuple=input_tuple,
        )


def __highlight_nf_ea_connector_using_input_tuple(
    ea_repository: EaRepositories,
    input_tuple: tuple,
):
    connector_ea_guid = get_tuple_attribute_value_if_required(
        owning_tuple=input_tuple,
        attribute_name="guid",
    )

    __highlight_nf_ea_connector(
        ea_repository=ea_repository,
        connector_ea_guid=connector_ea_guid,
    )


def __highlight_nf_ea_connector(
    ea_repository: EaRepositories,
    connector_ea_guid: str,
):
    i_dual_repository = EaRepositoryMappers.get_i_dual_repository(
        ea_repository=ea_repository
    )

    i_connector = i_dual_repository.get_connector_by_guid(
        connector_ea_guid=connector_ea_guid
    )

    if isinstance(
        i_connector, IDualConnector
    ):
        __highlight_nf_i_dual_connector(
            i_dual_connector=i_connector
        )


def __highlight_nf_i_dual_connector(
    i_dual_connector: IDualConnector,
):
    i_dual_connector.color = 255

    i_dual_connector.width = 5

    i_dual_connector.update()
