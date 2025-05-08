from bclearer_interop_services.ea_interop_service.nf_ea_common.objects.ea_repositories import (
    EaRepositories,
)
from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)


def get_ea_repository(
    ea_tools_session_manager: EaToolsSessionManagers,
    ea_repository_file: Files,
    short_name: str,
) -> EaRepositories:
    ea_repository = ea_tools_session_manager.create_ea_repository_using_file_and_short_name(
        ea_repository_file=ea_repository_file,
        short_name=short_name,
    )

    return ea_repository
