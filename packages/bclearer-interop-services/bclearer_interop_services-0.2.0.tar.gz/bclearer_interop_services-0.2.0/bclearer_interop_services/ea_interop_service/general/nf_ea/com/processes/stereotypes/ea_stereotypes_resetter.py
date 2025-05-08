from bclearer_interop_services.ea_interop_service.i_dual_objects.elements.i_dual_element import (
    IDualElement,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.i_dual_repository import (
    IDualRepository,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.packages.i_dual_package import (
    IDualPackage,
)
from bclearer_interop_services.ea_interop_service.session.ea_repository_mappers import (
    EaRepositoryMappers,
)
from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)
from bclearer_interop_services.ea_interop_service.session.processes.nf_ea_com_loaders.ea_repository_getter import (
    get_ea_repository,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def reset_all_stereotypes_using_manager(
    ea_tools_session_manager: EaToolsSessionManagers,
    ea_repository_file: Files,
):
    log_message(
        message="Resetting all stereotypes in "
        + ea_repository_file.base_name
    )

    ea_repository = get_ea_repository(
        ea_tools_session_manager=ea_tools_session_manager,
        ea_repository_file=ea_repository_file,
        short_name=ea_repository_file.base_name,
    )

    i_dual_repository = EaRepositoryMappers.get_i_dual_repository(
        ea_repository=ea_repository
    )

    __reset_all_stereotypes_in_dual_repository(
        i_dual_repository=i_dual_repository
    )


def __reset_all_stereotypes_in_dual_repository(
    i_dual_repository: IDualRepository,
):
    models = i_dual_repository.models

    for index in range(0, models.count):
        package = models.get_at(
            index=index
        )

        __reset_all_stereotypes_in_package_and_subpackages(
            i_dual_package=package
        )


def __reset_all_stereotypes_in_package_and_subpackages(
    i_dual_package: IDualPackage,
):
    log_message(
        message="Resetting stereotypes in package "
        + i_dual_package.name
    )

    __reset_all_stereotypes_in_package(
        i_dual_package=i_dual_package
    )

    packages = i_dual_package.packages

    for index in range(
        0, packages.count
    ):
        subpackage = packages.get_at(
            index=index
        )

        __reset_all_stereotypes_in_package_and_subpackages(
            i_dual_package=subpackage
        )


def __reset_all_stereotypes_in_package(
    i_dual_package: IDualPackage,
):
    elements = i_dual_package.elements

    for index in range(
        0, elements.count
    ):
        element = elements.get_at(
            index=index
        )

        __reset_all_stereotypes_for_element(
            element=element
        )

    connectors = (
        i_dual_package.connectors
    )

    for index in range(
        0, connectors.count
    ):
        connector = connectors.get_at(
            index=index
        )

        __reset_stereotype_in_ea_object(
            ea_object=connector
        )

    __reset_stereotype_in_ea_object(
        ea_object=i_dual_package
    )


def __reset_all_stereotypes_for_element(
    element: IDualElement,
):
    attributes = element.attributes

    for index in range(
        0, attributes.count
    ):
        attribute = attributes.get_at(
            index=index
        )

        __reset_stereotype_in_ea_object(
            ea_object=attribute
        )

    connectors = element.connectors

    for index in range(
        0, connectors.count
    ):
        connector = connectors.get_at(
            index=index
        )

        __reset_stereotype_in_ea_object(
            ea_object=connector
        )

    __reset_stereotype_in_ea_object(
        ea_object=element
    )


def __reset_stereotype_in_ea_object(
    ea_object: object,
):
    if hasattr(ea_object, "stereotype"):
        __reset_primary_stereotype_in_ea_object(
            ea_object=ea_object
        )

    if hasattr(
        ea_object, "stereotype_ex"
    ):
        __reset_stereotype_ex_in_ea_object(
            ea_object=ea_object
        )


def __reset_primary_stereotype_in_ea_object(
    ea_object: object,
):
    original_stereotype = (
        ea_object.stereotype
    )

    ea_object.stereotype = ""

    __try_update_ea_object(
        ea_object=ea_object
    )

    ea_object.stereotype = (
        original_stereotype
    )

    __try_update_ea_object(
        ea_object=ea_object
    )


def __reset_stereotype_ex_in_ea_object(
    ea_object: object,
):
    original_stereotype_ex = (
        ea_object.stereotype_ex
    )

    ea_object.stereotype_ex = ""

    __try_update_ea_object(
        ea_object=ea_object
    )

    ea_object.stereotype_ex = (
        original_stereotype_ex
    )

    __try_update_ea_object(
        ea_object=ea_object
    )


def __try_update_ea_object(
    ea_object: object,
):
    try:
        ea_object.update()

    except Exception as exception:
        log_message(
            message="Cannot update "
            + ea_object.name
            + " because of "
            + str(exception.args)
        )
