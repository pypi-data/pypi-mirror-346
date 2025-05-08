from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.file_system_service.windows_file_system.runners.windows_file_system_utility_runner import (
    run_windows_file_system_utility,
)
from nf_common.code.services.b_app_runner_service.b_app_runner import (
    run_b_app,
)
from nf_common.code.services.log_environment_utility_service.common_knowledge.environment_log_level_types import (
    EnvironmentLogLevelTypes,
)

if __name__ == "__main__":
    run_b_app(
        app_startup_method=run_windows_file_system_utility,
        environment_log_level_type=EnvironmentLogLevelTypes.FILTERED,
        output_folder_prefix="",
        output_root_folder=Folders(
            absolute_path_string="",
        ),
        input_folder=Folders(
            absolute_path_string="",
        ),
        export_hierarchy_register=True,
        export_b_identity_register=True,
        export_to_access=True,
        export_to_sqlite=True,
    )
