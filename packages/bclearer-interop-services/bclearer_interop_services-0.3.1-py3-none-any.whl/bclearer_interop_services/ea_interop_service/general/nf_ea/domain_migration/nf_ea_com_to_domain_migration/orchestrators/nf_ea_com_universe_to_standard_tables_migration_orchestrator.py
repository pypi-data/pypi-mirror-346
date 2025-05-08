from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.nf_ea_com_to_domain_migration.processes.nf_ea_com_to_standard_tables_dictionary_converter import (
    convert_nf_ea_com_to_standard_tables_dictionary,
)
from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)
from bclearer_interop_services.ea_interop_service.session.processes.creators.full_nf_ea_com_creation import (
    create_full_nf_ea_com,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)


@run_and_log_function
def orchestrate_nf_ea_com_universe_to_standard_tables_migration(
    ea_tools_session_manager: EaToolsSessionManagers,
    ea_repository_file: Files,
    short_name: str,
) -> dict:
    nf_ea_com_universe = __get_nf_ea_com_universe_from_ea_repository_file(
        ea_tools_session_manager=ea_tools_session_manager,
        ea_repository_file=ea_repository_file,
        short_name=short_name,
    )

    standard_tables_dictionary = convert_nf_ea_com_to_standard_tables_dictionary(
        nf_ea_com_universe=nf_ea_com_universe
    )

    return standard_tables_dictionary


def __get_nf_ea_com_universe_from_ea_repository_file(
    ea_tools_session_manager: EaToolsSessionManagers,
    ea_repository_file: Files,
    short_name: str,
) -> NfEaComUniverses:
    ea_repository = ea_tools_session_manager.create_ea_repository_using_file_and_short_name(
        ea_repository_file=ea_repository_file,
        short_name=short_name,
    )

    nf_ea_com_universe_manager = (
        ea_tools_session_manager.nf_ea_com_endpoint_manager.nf_ea_com_universe_manager
    )

    create_full_nf_ea_com(
        nf_ea_com_universe_manager=nf_ea_com_universe_manager,
        ea_repository=ea_repository,
    )

    nf_ea_com_universe = nf_ea_com_universe_manager.nf_ea_com_universe_dictionary[
        ea_repository
    ]

    return nf_ea_com_universe
