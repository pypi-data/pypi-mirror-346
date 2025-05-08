from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.collections.i_dual_connector_collection import (
    IDualConnectorCollection,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.connectors.i_dual_connector import (
    IDualConnector,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.elements.i_dual_element import (
    IDualElement,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.i_dual_repository import (
    IDualRepository,
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


def delete_nf_ea_connectors(
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
        __delete_nf_ea_connector_using_input_tuple(
            ea_repository=ea_repository,
            input_tuple=input_tuple,
        )


def __delete_nf_ea_connector_using_input_tuple(
    ea_repository: EaRepositories,
    input_tuple: tuple,
):
    connector_ea_guid = get_tuple_attribute_value_if_required(
        owning_tuple=input_tuple,
        attribute_name="guid",
    )

    __delete_nf_ea_connector(
        ea_repository=ea_repository,
        connector_ea_guid=connector_ea_guid,
    )


def __delete_nf_ea_connector(
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
        __delete_i_dual_connector(
            i_dual_repository=i_dual_repository,
            i_dual_connector=i_connector,
        )


def __delete_i_dual_connector(
    i_dual_repository: IDualRepository,
    i_dual_connector: IDualConnector,
):
    supplier_id = (
        i_dual_connector.supplier_id
    )

    supplier_element = i_dual_repository.get_element_by_id(
        element_id=supplier_id
    )

    if isinstance(
        supplier_element, IDualElement
    ):
        __delete_i_dual_connector_in_element(
            i_dual_element=supplier_element,
            i_dual_connector=i_dual_connector,
        )


def __delete_i_dual_connector_in_element(
    i_dual_element: IDualElement,
    i_dual_connector: IDualConnector,
):
    index_to_delete = __get_index_to_delete(
        i_dual_connector_collection=i_dual_element.connectors,
        connector_ea_guid=i_dual_connector.connector_guid,
    )

    i_dual_element.connectors.delete(
        index=index_to_delete
    )

    i_dual_element.connectors.refresh()

    i_dual_element.update()

    i_dual_element.refresh()


def __get_index_to_delete(
    i_dual_connector_collection: IDualConnectorCollection,
    connector_ea_guid: str,
) -> int:
    for index in range(
        i_dual_connector_collection.count
    ):
        connector_at_index = i_dual_connector_collection.get_at(
            index
        )

        if (
            connector_at_index.connector_guid
            == connector_ea_guid
        ):
            return index

    return -1
