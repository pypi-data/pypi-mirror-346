from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.attributes.i_dual_attribute import (
    IDualAttribute,
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


def rename_nf_ea_attributes(
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
        __rename_nf_ea_attribute_using_input_tuple(
            ea_repository=ea_repository,
            input_tuple=input_tuple,
        )


def __rename_nf_ea_attribute_using_input_tuple(
    ea_repository: EaRepositories,
    input_tuple: tuple,
):
    attribute_guid = get_tuple_attribute_value_if_required(
        owning_tuple=input_tuple,
        attribute_name="guid",
    )

    new_ea_attribute_name = get_tuple_attribute_value_if_required(
        owning_tuple=input_tuple,
        attribute_name="new_name",
    )

    __rename_nf_ea_attribute(
        ea_repository=ea_repository,
        attribute_guid=attribute_guid,
        new_ea_attribute_name=new_ea_attribute_name,
    )


def __rename_nf_ea_attribute(
    ea_repository: EaRepositories,
    attribute_guid: str,
    new_ea_attribute_name: str,
):
    i_dual_repository = EaRepositoryMappers.get_i_dual_repository(
        ea_repository=ea_repository
    )

    i_attribute = i_dual_repository.get_attribute_by_guid(
        attribute_guid=attribute_guid
    )

    if isinstance(
        i_attribute, IDualAttribute
    ):
        __rename_nf_i_dual_attribute(
            i_dual_attribute=i_attribute,
            new_ea_attribute_name=new_ea_attribute_name,
        )

    else:
        log_message(
            attribute_guid
            + "Warning: Attribute not found"
        )


def __rename_nf_i_dual_attribute(
    i_dual_attribute: IDualAttribute,
    new_ea_attribute_name: str,
):
    old_ea_attribute_name = (
        i_dual_attribute.name
    )

    if (
        old_ea_attribute_name
        == new_ea_attribute_name
    ):
        log_message(
            i_dual_attribute.attribute_guid
            + "Current name equals clean name for Attribute Name ("
            + old_ea_attribute_name
            + ")"
        )

    else:
        i_dual_attribute.name = (
            new_ea_attribute_name
        )

        i_dual_attribute.update()

        log_message(
            i_dual_attribute.attribute_guid
            + " : Attribute Name changed ("
            + old_ea_attribute_name
            + ") to ("
            + new_ea_attribute_name
            + ")"
        )
