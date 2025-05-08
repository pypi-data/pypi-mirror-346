import sys

from bclearer_interop_services.ea_interop_service.general.ea.com.i_dual_repository_creation_result_reporter import (
    report_i_dual_repository_creation_result,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.i_dual_repository import (
    IDualRepository,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.objects.ea_repositories import (
    EaRepositories,
)
from bclearer_interop_services.ea_interop_service.processes.i_dual_repository_creation_result_getter import (
    get_i_dual_repository_creation_result,
)
from bclearer_interop_services.ea_interop_service.session.ea_repository_mappers import (
    EaRepositoryMappers,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def create_ea_repository(
    ea_repository_file: Files,
    short_name: str,
) -> EaRepositories:
    i_dual_repository_creation_result = get_i_dual_repository_creation_result(
        ea_project_filename=ea_repository_file.absolute_path_string
    )

    report_i_dual_repository_creation_result(
        i_dual_repository_creation_result=i_dual_repository_creation_result,
        ea_project_filename=ea_repository_file.absolute_path_string,
    )

    i_dual_repository = (
        i_dual_repository_creation_result.i_dual_repository
    )

    if not isinstance(
        i_dual_repository,
        IDualRepository,
    ):
        log_message(
            message="Cannot create repository from "
            + ea_repository_file.absolute_path_string
        )

        sys.exit(-1)

    ea_repository = EaRepositories(
        ea_repository_file=ea_repository_file,
        short_name=short_name,
    )

    EaRepositoryMappers.store_map(
        ea_repository=ea_repository,
        i_dual_repository=i_dual_repository,
    )

    return ea_repository


def create_empty_ea_repository(
    short_name: str,
) -> EaRepositories:
    ea_repository = EaRepositories(
        short_name=short_name
    )

    return ea_repository
