from pathlib import Path

from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_orchestration_services.log_environment_utility_service.loggers.environment_logger import (
    log_filtered_environment,
)
from bclearer_orchestration_services.reporting_service.reporters.log_file import (
    LogFiles,
)
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    log_timing_header,
)


def set_up_logger_and_output_folder_for_domain_migration(
    output_folder: Folders,
):
    output_path = Path(
        output_folder.absolute_path_string
    )

    output_path.mkdir(
        parents=True, exist_ok=True
    )

    LogFiles.open_log_file(
        folder_path=output_path
    )

    log_timing_header()

    log_filtered_environment()


def end_domain_migration():
    LogFiles.close_log_file()
