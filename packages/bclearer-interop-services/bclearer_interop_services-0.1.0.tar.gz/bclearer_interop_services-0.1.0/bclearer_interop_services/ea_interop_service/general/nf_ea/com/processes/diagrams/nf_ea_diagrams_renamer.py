from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.diagrams.i_dual_diagram import (
    IDualDiagram,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.diagrams.i_null_diagram import (
    INullDiagram,
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


def rename_nf_ea_diagrams(
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
        __rename_nf_ea_diagram_using_input_tuple(
            ea_repository=ea_repository,
            input_tuple=input_tuple,
        )


def __rename_nf_ea_diagram_using_input_tuple(
    ea_repository: EaRepositories,
    input_tuple: tuple,
):
    diagram_guid = get_tuple_attribute_value_if_required(
        owning_tuple=input_tuple,
        attribute_name="guid",
    )

    new_ea_attribute_name = get_tuple_attribute_value_if_required(
        owning_tuple=input_tuple,
        attribute_name="new_name",
    )

    __rename_nf_ea_diagram(
        ea_repository=ea_repository,
        diagram_guid=diagram_guid,
        new_ea_diagram_name=new_ea_attribute_name,
    )


def __rename_nf_ea_diagram(
    ea_repository: EaRepositories,
    diagram_guid: str,
    new_ea_diagram_name: str,
):
    i_dual_repository = EaRepositoryMappers.get_i_dual_repository(
        ea_repository=ea_repository
    )

    i_dual_diagram = i_dual_repository.get_diagram_by_guid(
        diagram_ea_guid=diagram_guid
    )

    if isinstance(
        i_dual_diagram, INullDiagram
    ):
        log_message(
            diagram_guid
            + "Warning: Diagram not found"
        )

        return

    if not isinstance(
        i_dual_diagram, IDualDiagram
    ):
        raise TypeError

    old_ea_diagram_name = (
        i_dual_diagram.name
    )

    if (
        old_ea_diagram_name
        == new_ea_diagram_name
    ):
        log_message(
            diagram_guid
            + "Current name equals clean name for Diagram Name ("
            + old_ea_diagram_name
            + ")"
        )

    else:
        i_dual_diagram.name = (
            new_ea_diagram_name
        )

        i_dual_diagram.update()

        log_message(
            diagram_guid
            + " : Diagram Name changed ("
            + old_ea_diagram_name
            + ") to ("
            + new_ea_diagram_name
            + ")"
        )
