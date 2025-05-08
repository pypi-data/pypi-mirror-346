from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.elements.i_dual_element import (
    IDualElement,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.elements.i_null_element import (
    INullElement,
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
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from pandas import DataFrame


def rename_nf_ea_elements(
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
        __rename_nf_ea_element_using_input_tuple(
            ea_repository=ea_repository,
            input_tuple=input_tuple,
        )


def __rename_nf_ea_element_using_input_tuple(
    ea_repository: EaRepositories,
    input_tuple: tuple,
):
    element_guid = get_tuple_attribute_value_if_required(
        owning_tuple=input_tuple,
        attribute_name="guid",
    )

    new_ea_attribute_name = get_tuple_attribute_value_if_required(
        owning_tuple=input_tuple,
        attribute_name="new_name",
    )

    __rename_nf_ea_element(
        ea_repository=ea_repository,
        element_guid=element_guid,
        new_ea_element_name=new_ea_attribute_name,
    )


def __rename_nf_ea_element(
    ea_repository: EaRepositories,
    element_guid: str,
    new_ea_element_name: str,
):
    i_dual_repository = EaRepositoryMappers.get_i_dual_repository(
        ea_repository=ea_repository
    )

    i_dual_element = i_dual_repository.get_element_by_guid(
        element_ea_guid=element_guid
    )

    if isinstance(
        i_dual_element, INullElement
    ):
        log_message(
            element_guid
            + "Warning: Element not found"
        )

        return

    if not isinstance(
        i_dual_element, IDualElement
    ):
        raise TypeError

    old_ea_element_name = (
        i_dual_element.name
    )

    if (
        old_ea_element_name
        == new_ea_element_name
    ):
        log_message(
            element_guid
            + "Current name equals clean name for Element Name ("
            + old_ea_element_name
            + ")"
        )

    else:
        i_dual_element.name = (
            new_ea_element_name
        )

        i_dual_element.update()

        log_message(
            element_guid
            + " : Element Name changed ("
            + old_ea_element_name
            + ") to ("
            + new_ea_element_name
            + ")"
        )
