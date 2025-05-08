import sys

from bclearer_interop_services.ea_interop_service.general.ea.com.i_dual_repository_creation_result_reporter import (
    report_i_dual_repository_creation_result,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.i_dual_repository import (
    IDualRepository,
)
from bclearer_interop_services.ea_interop_service.processes.i_dual_repository_creation_result_getter import (
    get_i_dual_repository_creation_result,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


class EaComUniverses:
    def __init__(
        self, ea_project_filename: str
    ):
        i_dual_repository_creation_result = get_i_dual_repository_creation_result(
            ea_project_filename=ea_project_filename
        )

        report_i_dual_repository_creation_result(
            i_dual_repository_creation_result=i_dual_repository_creation_result,
            ea_project_filename=ea_project_filename,
        )

        if not isinstance(
            i_dual_repository_creation_result.i_dual_repository,
            IDualRepository,
        ):
            log_message(
                message="Cannot create repository from "
                + ea_project_filename
            )

            sys.exit(-1)

        self.i_dual_repository = (
            i_dual_repository_creation_result.i_dual_repository
        )

        self.__open_project_report()

    def __enter__(self):
        return self

    def __exit__(
        self,
        exception_type,
        exception_value,
        traceback,
    ):
        self.close_project()

    def __open_project_report(self):
        log_message(
            "Instance GUID: "
            + self.i_dual_repository.instance_guid
        )

        log_message(
            "Connection string: "
            + self.i_dual_repository.connection_string
        )

        log_message(
            "Library version: "
            + str(
                self.i_dual_repository.library_version
            )
        )

    def close_project(self):
        log_message(
            "Closing EA Project: "
            + self.i_dual_repository.instance_guid
        )

        self.i_dual_repository.exit()

        log_message("EA Project Closed")
